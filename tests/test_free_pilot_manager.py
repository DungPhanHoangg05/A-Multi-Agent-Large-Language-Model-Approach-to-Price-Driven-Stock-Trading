"""Kiểm phục hồi một lệnh bằng raw/journal fixture; chặn mọi kết nối mạng."""

from copy import deepcopy
from datetime import datetime, timezone
import base64
import hashlib
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from core.bayesian_memory import atomic_write_json
from core.free_pilot_assets import DIRECTORY, INPUTS, DOC
from core.free_pilot_manager import manage, next_phase, phase_result, snapshot, START, END
from core.free_pilot_recovery import recovery_action, pending_action, replay_durable_success
from core.historical_evaluation_audit import serializer, serialized_body, verify_decision
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import digest
from core.historical_signals import digest as legacy_digest

ROOT = Path(__file__).resolve().parents[1]
CONFIG = load(ROOT / DOC / "historical_evaluation_protocol.json")["inference"]["config"]


class RecoveryTests(unittest.TestCase):
    """Mỗi fixture có đúng năm ledger và identity riêng, không thể nhập vào pilot thật."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / DIRECTORY
        self.book = RunBook(self.directory, {"fixture": True})
        self.slot = "graph/FPT-2023-08-17/u0/pattern"
        self.inputs = {"source": {"org": 3, "point": "FPT-2023-08-17/u0"}}
        self.messages = "Nội dung fixture kiểm replay"
        graph = serializer({"model": "qwen/qwen3.8-27b", "temperature": 0., "max_tokens": 960,
                            "service_tier": "on_demand", "client_options": CONFIG["client_options"]["graph"]})
        self.body = serialized_body(graph, self.messages)
        for i in range(1, 6):
            atomic_write_json(self.directory / f"usage/org{i}.json", {"requests": []})

    def unknown(self, status: int | str | None = 503, *, payload: dict | None = None) -> dict:
        if self.book.path(self.slot).exists():
            last = load(self.book.path(self.slot))["attempts"][-1]
            if last.get("authorization") is None:
                self.book.reconcile(last["attempt_id"], "Chỉ authorize fixture")
        with self.assertRaises(RuntimeError):
            self.book.execute(self.slot, self.inputs, lambda _: (_ for _ in ()).throw(RuntimeError("Fixture interruption")))
        doc = load(self.book.path(self.slot))
        if status is None:
            return doc
        attempt = doc["attempts"][-1]["attempt_id"]
        role = self.slot.split("/")[-1]
        point = self.inputs.get("source", {}).get("point") or self.inputs["request"]["point_id"]
        row = {"id": str(uuid4()), "checkpoint_attempt_id": attempt, "status": status,
               "point_id": point, "branch_id": role, "run_signature": self.book.signature}
        if isinstance(status, int):
            payload = payload or ({"choices": [{"message": {"content": "REPORT_FIXTURE"}}]} if status == 200 else {"error": {"message": "over capacity"}})
            body = json.dumps(payload, ensure_ascii=False).encode()
            raw = {"status": status, "headers": {}, "body_base64": base64.b64encode(body).decode(),
                   "slot": {k: row[k] for k in ("checkpoint_attempt_id", "point_id", "branch_id", "run_signature")},
                   "request_body_sha256": digest(self.body), "request_legacy_body_sha256": legacy_digest(self.body)}
            path = self.directory / "http" / (row["id"] + ".json")
            save(path, raw)
            row.update(historical_raw={"path": path.relative_to(self.directory).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
                       improvement_audit={"request": {"canonical_body_sha256": legacy_digest(self.body)},
                           "response": {"body_sha256": hashlib.sha256(body).hexdigest(), "canonical_sha256": legacy_digest(payload)}})
        path = self.directory / "usage/org3.json"
        ledger = json.loads(path.read_bytes()); ledger["requests"].append(row)
        atomic_write_json(path, ledger)
        return doc

    def test_selects_current_uuid_after_old_attempt_was_already_reconciled(self) -> None:
        old = self.unknown(); current = self.unknown()
        action = pending_action(self.book, now=100.)
        self.assertNotEqual(action["attempt_id"], old["attempts"][-1]["attempt_id"])
        self.assertEqual(action["attempt_id"], current["attempts"][-1]["attempt_id"])
        self.assertEqual(action["http_count"], 2)
        self.assertEqual(action["resume_at"], 160.)

    def test_authorized_current_uuid_is_not_reconciled_twice(self) -> None:
        doc = self.unknown()
        self.book.reconcile(doc["attempts"][-1]["attempt_id"], "Fixture")
        self.assertEqual(pending_action(self.book)["kind"], "READY")

    def test_transient_retry_continues_after_three_and_after_restart(self) -> None:
        for _ in range(7): self.unknown()
        for _ in range(2):
            action=pending_action(self.book,now=100.)
            self.assertEqual(action['kind'],'RETRY')
            self.assertEqual(action['http_count'],7)
            self.assertEqual(action['resume_at'],1000.)

    def test_200_can_replay_at_third_attempt_without_fourth_http(self) -> None:
        self.unknown(); self.unknown(); self.unknown(200)
        self.assertEqual(pending_action(self.book)["kind"], "REPLAY")

    def test_raw_tampering_and_wrong_org_are_rejected(self) -> None:
        self.unknown()
        path = self.directory / "usage/org3.json"
        ledger = json.loads(path.read_bytes())
        raw = self.directory / ledger["requests"][0]["historical_raw"]["path"]
        original = raw.read_bytes(); raw.write_bytes(b"corrupt")
        with self.assertRaises(ValueError): pending_action(self.book)
        raw.write_bytes(original)
        atomic_write_json(self.directory / "usage/org2.json", ledger)
        atomic_write_json(path, {"requests": []})
        with self.assertRaisesRegex(ValueError, "org/point"):
            pending_action(self.book)

    def test_no_dispatch_and_quota_wait_keep_reserves(self) -> None:
        doc = self.unknown(None)
        path = self.directory / "usage/org3.json"
        started = datetime.fromisoformat(doc["attempts"][-1]["started_at"]).timestamp()
        atomic_write_json(path, {"requests": [], "last_stop": {"reason": "DAILY_QUOTA", "at": started + 1,
            "resume_not_before_utc": datetime.fromtimestamp(started + 3600, timezone.utc).isoformat()}})
        before = snapshot(self.directory)
        self.assertEqual(pending_action(self.book, now=started+2)["resume_at"], started+3602)
        self.assertEqual(snapshot(self.directory), before)

    def test_429_uses_provider_reset(self) -> None:
        self.unknown(429)
        path = self.directory / "usage/org3.json"
        ledger = json.loads(path.read_bytes()); ledger["requests"][0]["retry_until"] = 5000.
        atomic_write_json(path, ledger)
        self.assertEqual(pending_action(self.book, now=100.)["resume_at"], 5001.)

    def test_earlier_success_does_not_authorize_another_request(self) -> None:
        self.unknown(200); self.unknown(503)
        with self.assertRaisesRegex(ValueError, "HTTP200 ở attempt trước"):
            pending_action(self.book)

    def test_401_and_ambiguous_transport_do_not_auto_retry(self) -> None:
        self.unknown(401)
        with self.assertRaises(ValueError): pending_action(self.book)

    def test_ambiguous_dispatch_is_not_retried_even_if_old_authorization_exists(self) -> None:
        doc = self.unknown(None)
        self.book.reconcile(doc["attempts"][-1]["attempt_id"], "Fixture")
        row = {"id":str(uuid4()), "status":None, "checkpoint_attempt_id":doc["attempts"][-1]["attempt_id"],
               "run_signature":self.book.signature, "branch_id":"pattern", "point_id":self.inputs["source"]["point"]}
        atomic_write_json(self.directory/'usage/org3.json', {"requests":[row]})
        with self.assertRaises(ValueError): pending_action(self.book)

    def test_transport_recovery_requires_matching_durable_diagnostic(self) -> None:
        doc = self.unknown("transport_error")
        with self.assertRaises(FileNotFoundError): pending_action(self.book)
        row = json.loads((self.directory/'usage/org3.json').read_bytes())["requests"][0]
        path = self.directory/'diagnostics'/(row['id']+'.json')
        diagnostic = {"request_record_id":row['id'], "run_uuid":self.book.uuid, "run_signature":self.book.signature,
                      "checkpoint_attempt_id":doc['attempts'][-1]['attempt_id'], "provider_outcome":"UNKNOWN",
                      "point_id":row['point_id'], "role":None, "exception_chain":[{"class":"httpx.ReadTimeout"}],
                      "sources":{"fixture":True}}
        save(path, diagnostic)
        with patch('core.historical_transport_observer.source_bindings',return_value={'fixture':True}):
            self.assertEqual(pending_action(self.book)['kind'], 'RETRY')
            diagnostic['checkpoint_attempt_id']='wrong'; save(path,diagnostic)
            with self.assertRaises(ValueError): pending_action(self.book)

    def test_missing_ledger_is_not_zero_quota(self) -> None:
        self.unknown(None)
        (self.directory / "usage/org5.json").unlink()
        with self.assertRaises(FileNotFoundError): pending_action(self.book)

    def test_multiple_pending_slots_stop_instead_of_guessing_uuid(self) -> None:
        self.unknown()
        self.slot = "graph/FPT-2023-08-17/u0/trend"
        self.unknown()
        with self.assertRaisesRegex(ValueError, "Nhiều slot"):
            pending_action(self.book)

    def test_vision_recovery_uses_same_uuid_and_zero_network(self) -> None:
        from core.free_pilot_runtime import PilotClients
        doc = self.unknown(200)
        client = PilotClients.__new__(PilotClients)
        client.book, client.data = self.book, Mock(protocol={"inference": {"config": CONFIG}})
        before = snapshot(self.directory)
        def invoke(attempt: str) -> dict:
            self.assertEqual(attempt, doc["attempts"][-1]["attempt_id"])
            _, model = client.models(3)
            return {"report": model.invoke(self.messages).content}
        with patch("socket.socket.connect", side_effect=AssertionError("Không được gọi mạng")), replay_durable_success():
            output = self.book.execute(self.slot, self.inputs, invoke, validate=lambda value: self.assertTrue(self.book.verify_only))
        self.assertEqual(output, {"report": "REPORT_FIXTURE"})
        final = load(self.book.path(self.slot))
        self.assertEqual(len(final["attempts"]), 1)
        self.assertEqual(final["attempts"][-1]["status"], "complete")
        self.assertEqual(snapshot(self.directory), before)

    def test_decision_recovery_checks_schema_raw_body_and_frozen_validator(self) -> None:
        from core.free_pilot_runtime import PilotClients
        schema = {"type": "object", "properties": {"decision": {"enum": ["LONG", "SHORT"]}}, "required": ["decision"], "additionalProperties": False}
        request = {"model": "openai/gpt-oss-20b", "temperature": 0., "max_tokens": 960, "service_tier": "on_demand",
                   "client_options": CONFIG["client_options"]["agent"], "point_id": "FPT-2023-08-17",
                   "messages": [{"role": "user", "content": self.messages}], "structured": {"schema": schema}}
        self.slot = "pilot/FPT_point/Original_common"
        self.inputs = {"org": 3, "request": request}
        model = serializer({k: request[k] for k in ("model", "temperature", "max_tokens", "service_tier", "client_options")})
        self.body = serialized_body(model, self.messages, schema)
        doc = self.unknown(200, payload={"choices": [{"message": {"content": '{"decision":"SHORT"}'}}]})
        client = PilotClients.__new__(PilotClients); client.book = self.book
        before = snapshot(self.directory)
        with patch("socket.socket.connect", side_effect=AssertionError("Không được gọi mạng")), replay_durable_success():
            response = self.book.execute(self.slot, self.inputs,
                lambda a: client.decision(3, request, a, "Original_common"),
                validate=lambda v: verify_decision(self.book, v, "Original_common", fixture=False, request=request))
        self.assertEqual(response["request_id"], doc["attempts"][-1]["attempt_id"])
        self.assertEqual(response["reply"]["decision"], "SHORT")
        self.assertEqual(snapshot(self.directory), before)


class ManagerTests(unittest.TestCase):
    """Kiểm thứ tự phase và resume đầu-cuối bằng worker mô phỏng cách ly."""
    def test_single_command_restarts_503_then_shared_collect_verify(self) -> None:
        fixture = RecoveryTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        fixture.unknown()
        root, book = fixture.root, fixture.book
        units = [{"id": "unit" + str(i)} for i in range(48)]
        save(root / INPUTS, {"units": units})
        save(book.directory / "campaign.json", {"deadline_epoch": time.time()+172800})
        for path in (DOC / "README.md", DOC / "historical_reevaluation_plan.md"):
            (root/path).write_text(START + "\n\n" + END, encoding="utf-8")
        stages = []
        from core.historical_evaluation_protocol import PRIMARY
        def popen(command: list, worker_root: Path, handle: object) -> Mock:
            stage = command[-1]; stages.append(stage)
            if stages == ['shared']:
                fixture.unknown()
                handle.write('Fixture HTTP503 trong worker\n')
                return Mock(poll=Mock(return_value=1),returncode=1)
            if stage == "shared":
                book.execute(fixture.slot, fixture.inputs, lambda _: {"fixture": True})
                for unit in units: book.execute("shared/"+unit["id"], {}, lambda _: {"fixture": True})
                book.execute("shared_manifest", {}, lambda _: {"fixture": True})
                result = {"run_uuid": book.uuid, "count": 48, "shared": {u["id"]: "fixture" for u in units}}
            elif stage == "collect":
                for unit in units:
                    for branch in (*PRIMARY, "Fact_Anchor"):
                        book.execute("pilot/"+unit["id"]+"/"+branch, {}, lambda _: {"fixture": True})
                    book.execute("label/"+unit["id"], {}, lambda _: {"fixture": True})
                result = {"run_uuid": book.uuid, "status": "P05_PENDING", "forecast_slots": 336, "planned_points": 48}
            else:
                result = {"run_uuid": book.uuid, "status": "P05_COLD_PASS", "forecast_slots": 336, "planned_points": 48}
                save(book.directory/"pilot_collection_receipt.json", {**result,
                     "slots": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (book.directory/"slots").glob('*.json')},
                     "usage": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (book.directory/"usage").glob('*.json')}})
            handle.write(json.dumps(result)+"\n")
            return Mock(poll=Mock(return_value=0), returncode=0)
        # Binding receipt supervisor dùng file này, source giả chỉ có trong thư mục fixture.
        from core.free_pilot_manager import CONFIG as MANAGER_CONFIG
        save(root/MANAGER_CONFIG, {"fixture": True})
        with patch("core.free_pilot_manager.preflight", return_value={"fixture": True}), \
                patch("core.free_pilot_manager.identity", return_value={"fixture": True}), \
                patch("core.free_pilot_manager.launch_worker", side_effect=popen), \
                patch("core.free_pilot_manager.wait_until") as wait, \
                patch.dict(os.environ, {f"GROQ_ORG_{i}_API_KEY": 'fixture-'+str(i) for i in range(1,6)}), \
                patch("socket.socket.connect", side_effect=AssertionError("Không được gọi mạng")):
            result = manage(root)
            self.assertEqual(result["status"], "P05_COLD_PASS")
            self.assertEqual(stages, ["shared", "shared", "collect", "verify"])
            self.assertEqual(wait.call_count, 2)
            before = snapshot(book.directory)
            old_owner=json.loads((book.directory/'manager/run.owner.json').read_bytes())
            save(root/MANAGER_CONFIG,{'fixture':True,'revision':2})
            with patch('core.free_pilot_manager.preflight',return_value={'fixture':True,'revision':2}):
                manage(root)
            self.assertEqual(stages, ["shared", "shared", "collect", "verify", "verify"])
            self.assertEqual(snapshot(book.directory), before)
            self.assertEqual(json.loads((book.directory/'manager/run.owner.json').read_bytes())['run_signature'],old_owner['run_signature'])

    def test_worker_transport_reaches_fifth_request_preserving_native_budget_and_timeouts(self) -> None:
        import test_historical_reset_recovery as legacy
        from core import historical_transport_observer as observer
        from core.free_pilot_recovery import supervisor_transport_policy
        helper=legacy.RecoveryTests(); self.addCleanup(helper.doCleanups)
        state=helper.fixture(['reset']*4+['ok'])
        with supervisor_transport_policy(), patch.object(legacy,'observe_transport',observer.observe_transport):
            for _ in range(4):
                with self.assertRaises(legacy.PilotStop):
                    state.run()
                state.book.reconcile(load(state.book.path('fixture/trend'))['attempts'][-1]['attempt_id'],'Fixture retry liên tục')
            state.run()
        rows=state.pacer.state['requests']
        self.assertEqual(len(state.calls),5)
        self.assertEqual([r['status'] for r in rows],['transport_error']*4+[200])
        self.assertEqual(len({body for body,_ in state.calls}),1)
        self.assertTrue(all(timeout==observer.RECOVERY_POLICY['timeouts'] for _,timeout in state.calls))
        self.assertTrue(all(r['historical_transport_policy']['max_http_per_slot'] is None for r in rows))
        self.assertTrue(all(r['historical_transport_policy']['max_http_per_attempt']==3 for r in rows))

    def test_partial_exit_zero_is_rejected(self) -> None:
        with TemporaryDirectory() as folder:
            path=Path(folder)/'worker.log'
            path.write_text(json.dumps({"status":"PARTIAL","run_uuid":"fixture","planned_points":48,"forecast_slots":1}))
            with self.assertRaises(ValueError):
                phase_result(path, "collect", Mock(uuid="fixture"), [{"id":"one"}])

    def test_changed_supervisor_source_or_revoked_grant_cannot_start_worker(self) -> None:
        from core.free_pilot_manager import preflight, profile, CONFIG as MANAGER_CONFIG
        from core.free_pilot_assets import GRANT
        config=profile(ROOT); grant=load(ROOT/GRANT)
        bad=deepcopy(config); bad['sources']['scripts/run_free_pilot.py']['sha256']='bad'
        with patch('core.free_pilot_manager.anchored',return_value=bad), self.assertRaises(ValueError):
            preflight(ROOT)
        grant['api']=False
        with patch('core.free_pilot_manager.anchored',side_effect=lambda r,p: config if p==MANAGER_CONFIG else grant), \
                patch('core.free_pilot_manager.verify_locked'), self.assertRaises(ValueError):
            preflight(ROOT)

    def test_cli_setup_error_is_brief_and_does_not_start_worker(self) -> None:
        from scripts.run_free_pilot import main
        with patch.object(sys,'argv',['run_free_pilot.py']), \
                patch('core.free_pilot_manager.manage',side_effect=ValueError('Fixture source không khớp')), \
                patch('core.free_pilot_manager.launch_worker') as launch, \
                patch('sys.stderr'), self.assertRaises(SystemExit) as stop:
            main()
        self.assertEqual(stop.exception.code,2)
        launch.assert_not_called()

    def test_cli_second_terminal_does_not_launch_duplicate_worker(self) -> None:
        from scripts.run_free_pilot import main
        with patch.object(sys,'argv',['run_free_pilot.py']), \
                patch('core.free_pilot_manager.manage',side_effect=RuntimeError('Run đang được tiến trình khác giữ khóa OS')), \
                patch('core.free_pilot_manager.launch_worker') as launch:
            main()
        launch.assert_not_called()

    def test_orphan_worker_keeps_os_lock_until_manager_can_resume(self) -> None:
        from core.free_pilot_manager import run_lock
        busy=Mock(); busy.__enter__=Mock(side_effect=RuntimeError('Run đang được tiến trình khác giữ khóa OS'))
        ready=Mock(); ready.__enter__=Mock(); ready.__exit__=Mock()
        with patch('core.free_pilot_manager.PriorRunLock',side_effect=[busy,ready]) as acquire, \
                patch('core.free_pilot_manager.time.sleep') as sleep, \
                patch('core.free_pilot_manager.write_status'):
            with run_lock(ROOT,{}):
                pass
        self.assertEqual(acquire.call_count,2)
        sleep.assert_called_once_with(5.)
        ready.__exit__.assert_called_once()


if __name__ == "__main__":
    unittest.main()
