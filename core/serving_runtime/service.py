"""Điều phối job serving bền vững, không dùng global graph/config mutable của Flask."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import threading
import time
from typing import Any, Callable

from core.historical_evaluation_journal import load
from core.prior_run_lock import PriorRunLock
from core.serving_contracts import ServingJob, ServingRequest
from core.serving_registry import CONFIG_VERSION, REGISTRY_VERSION, required_resources
from core.unified_contracts import digest
from core.variant_registry import execution_order, get_variant
from core.serving_runtime.resources import Resources, VERSION, default_models, validate_models
from core.serving_runtime.quota import Quota, Waiting, Unknown, Failed, Stopped
from core.serving_runtime.runner import Runner, safe_error
from core.serving_runtime.store import Store
from core.serving_runtime.transport import Calls, GroqHTTP


class Service:
    """Mỗi job có provider/client/config riêng; chỉ ledger quota và scheduler được chia sẻ."""

    def __init__(self, root: Path, *, provider_factory: Callable | None = None,
                 sender_factory: Callable = GroqHTTP, resources_factory: Callable = Resources,
                 clock=time.time, state_root: Path | None = None) -> None:
        self.root = root.resolve()
        self.store = Store(state_root or root)
        self.quota = Quota(self.store.root/"quota.sqlite3", clock)
        self.clock = clock
        if provider_factory is None:
            from core.serving_runtime.providers import AsOfProvider
            provider_factory = AsOfProvider
        self.provider_factory, self.sender_factory, self.resources_factory = provider_factory, sender_factory, resources_factory
        self.tasks: dict[str, threading.Thread] = {}
        self.mutex = threading.RLock()

    def preflight(self, spec: ServingRequest, key: str) -> dict:
        """Cấu trúc đúng chưa đủ: nguồn, miền, model/options và credential đều phải sẵn sàng."""
        request = spec.document()
        blockers, points = [], []
        try:
            resources = self.resources_factory(self.root)
            resources.verify()
        except (ValueError, OSError, KeyError):
            blockers.append({"code": "RESOURCES_NOT_READY", "message": "Cần cài hoặc khôi phục đúng resource release serving"})
            resources = None
        if resources is not None:
            try:
                points = resources.points(request)
            except ValueError:
                blockers.append({"code": "SUPPORT_MISMATCH", "message": "Mã/ngày/khung/ngôn ngữ hoặc số point ngoài miền công bố"})
        try:
            validate_models(request["models"])
        except ValueError:
            blockers.append({"code": "MODEL_NOT_RELEASED", "message": "Model/options không thuộc ABI/token policy đã mở"})
        from core.groq_pacing import tokenizer_cached
        if not tokenizer_cached():
            blockers.append({"code": "TOKENIZER_NOT_READY", "message": "Cần tokenizer o200k đã cache để admission token trước API"})
        if not key:
            blockers.append({"code": "CREDENTIAL_MISSING", "message": "Cần API key Groq trong cấu hình server"})
        plan = execution_order(request["variant_ids"])
        return {"version": "variant_serving_v1", "registry_version": REGISTRY_VERSION,
            "status": "blocked" if blockers else "ready", "run_enabled": not blockers,
            "request_sha256": spec.sha256, "requested_ids": request["variant_ids"], "execution_plan": plan,
            "blockers": blockers, "points": points, "resource_version": VERSION,
            "support": resources.document()["support"] if resources else None,
            "planned_decision_slots": len(points)*len(plan)*request["repeats"],
            "estimated_max_api_attempts": len(points)*(2+len(plan)*request["repeats"])*3,
            "quota_policy": "CONSERVATIVE_SINGLE_POOL_ALL_SERVING_JOBS_KEYS_AND_MODELS"}

    def create(self, spec: ServingRequest, key: str, owner: str, *, background: bool = True) -> str:
        """Key được copy vào client riêng, không ghi reservation/config/log."""
        checked = self.preflight(spec, key)
        if not checked["run_enabled"]:
            raise ValueError("Preflight chưa đạt")
        source = self.sources()
        resources = self.resources_factory(self.root).document()
        request = spec.document()
        config = {"version": CONFIG_VERSION, "registry_version": REGISTRY_VERSION, "runner_version": "serving_runner_v1",
            "provider_version": VERSION, "source_sha256": digest(source), "calendar_sha256": digest(resources["support"]["calendar"]),
            "support_sha256": digest(resources["support"]), "credential_scope_sha256": self.quota.credential_scope(key),
            "resources": {name: resources["resources"][name] for name in required_resources(request["variant_ids"])},
            "prompt_versions": {**{name: "shared_upstream_v1/"+name for name in ("indicator", "pattern", "trend", "alpha", "sentiment")},
                **{name: ("" if name == "original_fix" else "causal_common_v1/")+get_variant(name).profile for name in checked["execution_plan"]}}}
        snapshot = digest({"resource_bindings": resources["bindings"], "points": checked["points"]})
        job = ServingJob.create(spec, config, snapshot, owner)
        self.store.create(job, checked["points"], source)
        identifier = job.document()["run_id"]
        if background:
            self.start(identifier, key, owner)
        return identifier

    def _guard(self, reservation: dict, resources: Any) -> None:
        """Source/resource thay đổi thì dừng trước HTTP mới, không tự cập nhật pin để resume."""
        identifier = reservation["job"]["run_id"]
        if self.store.control(identifier)["stop_requested"]:
            raise Stopped()
        if self.sources() != reservation["source"]:
            raise ValueError("Source serving khác identity job")
        resources.verify()

    def sources(self) -> dict:
        """Identity gồm code và runtime SDK/scientific, không chỉ tên model hoặc profile."""
        from core.unified_experiment import source_identity, runtime_identity
        from importlib.metadata import version
        return {"files": source_identity(self.root), "runtime": {**runtime_identity(),
            **{name:version(name) for name in ("httpx","jsonschema","matplotlib","tiktoken","hmmlearn","scikit-learn")}}}

    def start(self, identifier: str, key: str, owner: str) -> bool:
        """Resume idempotent dưới khóa thread và khóa OS; không reset UUID hoặc slot."""
        reservation = self.store.reservation(identifier, owner)
        if self.quota.credential_scope(key) != reservation["job"]["identity"]["config"]["credential_scope_sha256"]:
            raise ValueError("Credential không khớp job cũ")
        with self.mutex:
            if identifier in self.tasks and self.tasks[identifier].is_alive():
                return False
            if self.store.status(identifier)["state"] == "completed":
                return False
            generation = self.store.control(identifier)["generation"]
            worker = threading.Thread(target=self.work, args=(identifier, str(key), owner),
                                      kwargs={"resume_generation": generation}, daemon=True,
                                      name="serving-"+identifier)
            self.tasks[identifier] = worker
            worker.start()
        return True

    def work(self, identifier: str, key: str, owner: str, *, wait: bool = True, resume_generation: int | None = None) -> None:
        """Không retry mù timeout; waiting/quota có heartbeat và có thể dừng giữa các lượt chờ."""
        reservation = self.store.reservation(identifier, owner)
        directory = self.store.path(identifier)
        sender = None
        try:
            with PriorRunLock(directory/"worker", reservation["job"]["identity_sha256"]):
                if self.quota.credential_scope(key) != reservation["job"]["identity"]["config"]["credential_scope_sha256"]:
                    raise ValueError("Credential khác identity job")
                if resume_generation is not None:
                    self.store.control(identifier, False, expected_generation=resume_generation)
                resources = self.resources_factory(self.root)
                self._guard(reservation, resources)
                request = reservation["job"]["identity"]["request"]
                provider = self.provider_factory(self.root, reservation["points"], request["models"], request["variant_ids"])
                # Lỗi PIT/selector/facts phải được phát hiện trước vision đầu tiên.
                for point in reservation["points"]:
                    provider.validate_point(point)
                sender = self.sender_factory(str(key))
                calls = Calls(directory, identifier, self.quota, sender, lambda: self._guard(reservation, resources), clock=self.clock)
                runner = Runner(self.store, reservation, calls, provider)
                while True:
                    self.store.status(identifier, "running")
                    try:
                        runner.tick()
                        self.store.status(identifier, "completed")
                        break
                    except Waiting as waiting:
                        self.store.status(identifier, "partial", safe_error("QUOTA_EXCEEDED", True), waiting.until)
                        if not wait:
                            return
                        while self.clock() < waiting.until:
                            runner.guard_stop()
                            time.sleep(min(.5, max(.01, waiting.until-self.clock())))
        except Stopped:
            self.store.status(identifier, "stopped")
        except Unknown:
            self.store.status(identifier, "unknown", safe_error("UNKNOWN_ATTEMPT"))
        except Failed as error:
            code = str(error) if str(error) in ("INVALID_MODEL_OUTPUT", "INTEGRITY_FAILURE") else "PROVIDER_FAILURE"
            self.store.status(identifier, "failed", safe_error(code))
        except RuntimeError as error:
            if str(error) != "Run đang được tiến trình khác giữ khóa OS":
                self.store.status(identifier, "failed", safe_error("INTERNAL_ERROR"))
        except (ValueError, AssertionError, OSError, KeyError):
            self.store.status(identifier, "failed", safe_error("INTEGRITY_FAILURE"))
        except Exception:
            self.store.status(identifier, "failed", safe_error("INTERNAL_ERROR"))
        finally:
            if sender is not None:
                sender.close()

    def result(self, identifier: str, owner: str) -> dict:
        """GET không tạo client/provider/model; chỉ đọc journal và metadata đã durable."""
        reservation = self.store.reservation(identifier, owner)
        calls = type("ReadCalls", (), {"quota": self.quota})()
        runner = Runner(self.store, reservation, calls, None, read_only=True)
        status = self.store.status(identifier)
        if status["state"] in ("running", "partial") and self.store.control(identifier)["stop_requested"]:
            status["state"] = "stop_requested"
        result = runner.public(status)
        result["worker_alive"] = bool(identifier in self.tasks and self.tasks[identifier].is_alive())
        return result
