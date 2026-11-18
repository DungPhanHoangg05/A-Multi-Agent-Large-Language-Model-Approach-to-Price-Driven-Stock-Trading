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
from core.finalize_serving_profile import PENDING, RECEIPT_SHA256, SCIENTIFIC_STATUS, VERSION as FINALIZED, method_profile
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
                 clock=time.time, state_root: Path | None = None, finalize_fixture: bool = False) -> None:
        self.root = root.resolve()
        self.store = Store(state_root or root)
        self.quota = Quota(self.store.root/"quota.sqlite3", clock)
        self.clock = clock
        if provider_factory is None:
            from core.serving_runtime.providers import AsOfProvider
            provider_factory = AsOfProvider
        self.provider_factory, self.sender_factory, self.resources_factory = provider_factory, sender_factory, resources_factory
        if finalize_fixture and sender_factory is GroqHTTP:
            raise ValueError("Preview FIN08 chỉ dùng sender fixture")
        self.finalize_fixture = finalize_fixture
        self.tasks: dict[str, threading.Thread] = {}
        self.mutex = threading.RLock()

    def preflight(self, spec: ServingRequest, key: str) -> dict:
        """Cấu trúc đúng chưa đủ: nguồn, miền, model/options và credential đều phải sẵn sàng."""
        request = spec.document()
        blockers, points = [], []
        finalized = request["version"] == FINALIZED
        if finalized and not self.finalize_fixture:
            blockers.append({"code": PENDING, "message": "Cần nghiệm thu FIN10 trước khi chạy hosted profile finalize"})
        try:
            resources = self.resources(request)
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
        result = {"version": request["version"], "registry_version": REGISTRY_VERSION,
            "status": "blocked" if blockers else "ready", "run_enabled": not blockers,
            "request_sha256": spec.sha256, "requested_ids": request["variant_ids"], "execution_plan": plan,
            "blockers": blockers, "points": points, "resource_version": getattr(resources, "version", VERSION),
            "support": resources.document()["support"] if resources else None,
            "planned_decision_slots": len(points)*len(plan)*request["repeats"],
            "estimated_max_api_attempts": len(points)*(2+len(plan)*request["repeats"])*3,
            "quota_policy": "CONSERVATIVE_SINGLE_POOL_ALL_SERVING_JOBS_KEYS_AND_MODELS"}
        if finalized:
            result.update(scientific_status=SCIENTIFIC_STATUS, context_receipt_sha256=RECEIPT_SHA256,
                          execution_scope="OFFLINE_FIXTURE" if self.finalize_fixture else PENDING)
        return result

    def create(self, spec: ServingRequest, key: str, owner: str, *, background: bool = True) -> str:
        """Key được copy vào client riêng, không ghi reservation/config/log."""
        checked = self.preflight(spec, key)
        if not checked["run_enabled"]:
            raise ValueError("Preflight chưa đạt")
        source = self.sources()
        request = spec.document()
        resource_provider = self.resources(request)
        resources = resource_provider.document()
        finalized = request["version"] == FINALIZED
        config = {"version": CONFIG_VERSION, "registry_version": REGISTRY_VERSION, "runner_version": FINALIZED if finalized else "serving_runner_v1",
            "provider_version": getattr(resource_provider, "version", VERSION), "source_sha256": digest(source), "calendar_sha256": digest(resources["support"]["calendar"]),
            "support_sha256": digest(resources["support"]), "credential_scope_sha256": self.quota.credential_scope(key),
            "resources": {name: resources["resources"][name] for name in required_resources(request["variant_ids"])},
            "prompt_versions": {**{name: (FINALIZED if finalized else "shared_upstream_v1")+"/"+name for name in ("indicator", "pattern", "trend", "alpha", "sentiment")},
                **{name: method_profile(name) if finalized else ("" if name == "original_fix" else "causal_common_v1/")+get_variant(name).profile for name in checked["execution_plan"]}}}
        snapshot = digest({"resource_bindings": resources["bindings"], "points": checked["points"]})
        job = ServingJob.create(spec, config, snapshot, owner)
        self.store.create(job, checked["points"], source)
        identifier = job.document()["run_id"]
        if background:
            self.start(identifier, key, owner)
        return identifier

    def resources(self, request: dict | None = None) -> Any:
        """Mỗi lượt kiểm dùng resource riêng; provider mới có thể bind snapshot trong request."""
        if request is not None and request["version"] == FINALIZED:
            from core.finalize_serving_resources import FinalizedResources
            return FinalizedResources(self.root)
        return self.resources_factory(self.root)

    def provider(self, reservation: dict) -> Any:
        """Factory mặc định giữ ABI as-of; subclass live truyền snapshot đã khóa riêng."""
        request = reservation["job"]["identity"]["request"]
        if request["version"] == FINALIZED:
            from core.finalize_serving_provider import FinalizedProvider
            return FinalizedProvider(self.resources(request), reservation["points"], request["models"], request["variant_ids"])
        return self.provider_factory(self.root, reservation["points"], request["models"], request["variant_ids"])

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
                request = reservation["job"]["identity"]["request"]
                if request["version"] == FINALIZED and not self.finalize_fixture:
                    raise ValueError("Chưa cấp hosted cho profile finalized")
                resources = self.resources(request)
                self._guard(reservation, resources)
                provider = self.provider(reservation)
                # Lỗi PIT/selector/facts phải được phát hiện trước vision đầu tiên.
                for point in reservation["points"]:
                    provider.validate_point(point)
                sender = self.sender_factory(str(key))
                calls = Calls(directory, identifier, self.quota, sender, lambda: self._guard(reservation, resources),
                              clock=self.clock, total_prompt_guard=request["version"] == FINALIZED)
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
        # Ngôn ngữ request là ngôn ngữ hiển thị; projection nghiên cứu VI giữ nguyên byte.
        result['generation_language'] = 'vi'
        result['display_language'] = reservation['job']['identity']['request']['language']
        result["worker_alive"] = bool(identifier in self.tasks and self.tasks[identifier].is_alive())
        if result["version"] == FINALIZED:
            result.update(scientific_status=SCIENTIFIC_STATUS, context_receipt_sha256=RECEIPT_SHA256,
                          execution_scope="OFFLINE_FIXTURE")
        return result

    def catalog(self, owner: str) -> list[dict]:
        """Danh mục chỉ gồm backtest thuộc owner; không mở provider hoặc outcome."""
        rows = []
        for path in sorted(self.store.root.iterdir()):
            if not path.is_dir(): continue
            try:
                reservation = self.store.reservation(path.name,owner)
            except PermissionError:
                continue
            job = reservation['job']; request = job['identity']['request']
            if request['mode'] == 'backtest':
                rows.append({'id':job['run_id'],'kind':'serving_backtest','label':', '.join(request['symbols'])+' · '+request['start_date']+' — '+request['end_date'],
                    'status':self.store.status(job['run_id'])['state'],'points':len(reservation['points']),'repeats':request['repeats']})
        return rows

    def evaluation(self, identifier: str, owner: str, query: dict[str,str]) -> dict:
        """GET đánh giá thuần từ checkpoint; giá chỉ mở sau đủ common support, không inference."""
        reservation = self.store.reservation(identifier,owner)
        request = reservation['job']['identity']['request']
        files = ['core/serving_runtime/evaluation.py', 'core/free_pilot_statistics.py',
                 'core/unified_analysis/analysis.py', 'core/backtest_engine.py', 'utils/target_contract.py']
        if request['version'] == FINALIZED:
            from core.finalize_serving_evaluation import evaluate, prices
            files.append('core/finalize_serving_evaluation.py')
        else:
            from core.serving_runtime.evaluation import evaluate, prices
        public = self.result(identifier,owner)
        book = Runner(self.store,reservation,None,None,read_only=True)
        def loader() -> dict:
            # Khóa cả code metric đã dùng khi tạo job; không tái chứng nhận job cũ bằng evaluator mới.
            state = self.sources()
            if state['runtime'] != reservation['source']['runtime']: raise ValueError('Runtime evaluator khác job')
            sealed = reservation['source']['files']; current = state['files']
            for name in files:
                if current.get(name) != sealed.get(name): raise ValueError('Evaluator source khác job')
            return prices(self.root,reservation,book.outcomes(),self.resources(request))
        return evaluate(reservation,public,book.outcomes(),query,loader)
