"""Hồi quy recipe replica, query poison, selection/test gate và checkpoint/resume."""

from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import torch

from core.mt_bicl_inputs import training_membership
from core.mt_bicl_reference import SequentialBetaOracle
from core.mt_bicl_replica_io import (configure, load_checkpoint, path_for, read, rng_state,
                                     save_checkpoint, tree_hash, write)
from core.mt_bicl_replica_learner import make_optimizer, optimizer_step, tensor_hash
from core.mt_bicl_replica_metrics import SEEDS, STEPS, selection
from core.mt_bicl_replica_preparation import checked_oracle, corpus
from core.mt_bicl_replica_sampling import BetaTaskSimulator, train_feature_pool
from core.mt_bicl_replica_student import CASES, PAIRED, DistilledStudent, collate_packets, pack_input, query_losses
from core.mt_bicl_replica_training import batch, open_test, restore, snapshot
from core.mt_bicl_student import DistilledStudent as ServingStudent
from core.mt_bicl_teacher import BetaBernoulliTeacher
from core.historical_h02_data import complete_audit

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    """D/C/query nhỏ không gắn dữ liệu thị trường, q là sidecar loss."""
    return {"prior": [{"task_id":"P","observations":[{"observation_id":"P0","x":[0.,1.,0.,0.],"y":0},
        {"observation_id":"P1","x":[1.,0.,0.,0.],"y":1}]}],
        "target":{"task_id":"T","observations":[]},"query":{"observation_id":"Q","x":[0.,0.,1.,0.]}}


class ReplicaTests(unittest.TestCase):
    """Không chạy teacher fit thị trường, pilot hoặc optimizer production."""

    @classmethod
    def setUpClass(cls) -> None:
        """Đọc corpus recipe tĩnh; simulator nhận đúng731 vector fixture."""
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        torch.set_num_threads(1)
        cls.protocol = json.loads((ROOT/"docs/plan/week11/mt_bicl_replica_full_r1.json").read_bytes())
        cls.teacher = BetaBernoulliTeacher([1/16]*16)
        cls.simulator = BetaTaskSimulator([1/16]*16, {"vectors":[[0.,1.,0.,1.]]*731,"source_outcomes_used":False}, cls.protocol["corpus"])

    def test_training_contract_is_full_recipe(self) -> None:
        """Không biến replica thành một seed hoặc early stopping."""
        t = self.protocol["training"]
        self.assertEqual(t["model_seeds"], [17,42,73])
        self.assertFalse(t["metric_early_stop"])
        self.assertEqual((t["optimizer_steps_per_seed"],t["checkpoint_every_steps"]), (5000,250))
        self.assertEqual(self.protocol["teacher"]["fit"]["max_iterations"],1000)
        self.assertFalse(self.protocol["authorization"]["llm_api"])

    def test_sampler_random_access_resume_order(self) -> None:
        """Truy cập batch theo thứ tự khác không đổi episode hoặc sidecar."""
        a = self.simulator.episode("train",128,model_seed=42)
        self.simulator.episode("train",3,model_seed=17)
        self.assertEqual(a,self.simulator.episode("train",128,model_seed=42))
        with self.assertRaises(ValueError):
            self.simulator.episode("train",640000,model_seed=42)
        with self.assertRaises(ValueError):
            self.simulator.episode("train",1,model_seed=0)

    def test_swap_changes_only_prior_labels(self) -> None:
        """C/query/x và identity vẫn cùng cặp, không redraw để tăng eligible."""
        for index in (0,4500,4999):
            pair = self.simulator.pair("validation_swap",index)
            a,b = deepcopy(pair["input_a"]),deepcopy(pair["input_b"])
            self.assertEqual(a["target"],b["target"])
            self.assertEqual(a["query"],b["query"])
            for task in [*a["prior"],*b["prior"]]:
                for row in task["observations"]:
                    row.pop("y")
            self.assertEqual(a,b)

    def test_query_latent_poison_is_rejected(self) -> None:
        """Teacher và encoder không nhận nhãn query hoặc latent ngoài schema."""
        for case in CASES:
            data=fixture();data["query"]["y"]=1
            with self.assertRaises(ValueError):
                pack_input(data,packing=case)
        data=fixture();data["latent_theta"]=.9
        with self.assertRaises(ValueError):
            self.teacher.predict(data)

    def test_teacher_matches_independent_oracle(self) -> None:
        """Oracle dùng chuỗi Bernoulli độc lập, cả pooled và hierarchical."""
        reference=SequentialBetaOracle([1/16]*16)
        for pooled in (False,True):
            _,error=checked_oracle(self.teacher,reference,fixture(),pooled=pooled)
            self.assertLessEqual(error,1e-12)

    def test_training_batch_uses_visible_posterior_not_latent(self) -> None:
        """Poison sidecar thật không ảnh hưởng packet huấn luyện."""
        row=self.simulator.episode("train",0,model_seed=17)
        row["sidecar"]={"theta":[float("nan")],"query_y":99}
        with patch.object(self.simulator,"episode",return_value=row):
            packets=batch({"simulator":self.simulator,"teacher":self.teacher},1,17)
        self.assertEqual(len(packets),128)
        self.assertEqual(packets[0]["teacher_q"],self.teacher.predict(row["input"])["probability"])

    def test_bank_pool_does_not_read_future_outcomes(self) -> None:
        """Feature pool chỉ đọc train đã đóng, kể cả bank có outcome tương lai poison."""
        bank=json.loads((ROOT/"outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/inputs/dense_bank.json").read_bytes())["payload"]
        member=training_membership(bank)
        expected=train_feature_pool(bank,member)
        for row in bank["records"]:
            if row["split"]!="train":row["outcome"]={"poison":float("nan")}
        self.assertEqual(expected,train_feature_pool(bank,member))

    def test_paired_student_is_serving_compatible(self) -> None:
        """Weights replica PAIRED nạp strict vào serving class, output CPU trùng."""
        torch.manual_seed(17)
        replica=DistilledStudent().eval()
        serving=ServingStudent().eval()
        serving.load_state_dict(replica.state_dict(),strict=True)
        data=collate_packets([pack_input(fixture())],torch.device("cpu"))
        with torch.inference_mode():
            self.assertTrue(torch.equal(replica(data["values"],data["roles"],data["slots"],data["padding"]),
                                        serving(data["values"],data["roles"],data["slots"],data["padding"])))

    def test_loss_has_no_gradient_outside_query_for_both_packings(self) -> None:
        """Đối chứng69 và paired37 đều che nhãn/loss context đúng recipe."""
        for case in CASES:
            model=DistilledStudent(case)
            data=collate_packets([pack_input(fixture(),packing=case,teacher_q=.7)],torch.device("cpu"))
            logits=model(data["values"],data["roles"],data["slots"],data["padding"])
            gradient,=torch.autograd.grad(query_losses(logits,data).mean(),logits)
            mask=torch.ones_like(gradient,dtype=torch.bool);mask[0,data["queries"][0]]=False
            self.assertEqual(int(torch.count_nonzero(gradient[mask])),0)

    def test_checkpoint_resume_replays_optimizer_and_rng(self) -> None:
        """Một step fixture CPU: resume phải trùng model/optimizer/RNG, không production train."""
        device=configure(17,cuda=False)
        model=DistilledStudent();optimizer=make_optimizer(model)
        packets=[pack_input(fixture(),teacher_q=.7)]*2
        optimizer_step(model,optimizer,packets,2,device)
        payload=deepcopy(snapshot(model,optimizer,seed=17,step=1,binding="binding",uuid="uuid",physical=2))
        optimizer_step(model,optimizer,packets,2,device)
        expected=tree_hash(snapshot(model,optimizer,seed=17,step=2,binding="binding",uuid="uuid",physical=2))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"checkpoint.pt"
            pointer=save_checkpoint(path,payload)
            state=load_checkpoint(path,pointer)
            fresh=DistilledStudent();opt=make_optimizer(fresh)
            restore(fresh,opt,state,binding="binding",uuid="uuid",seed=17,physical=2)
            optimizer_step(fresh,opt,packets,2,device)
            self.assertEqual(expected,tree_hash(snapshot(fresh,opt,seed=17,step=2,binding="binding",uuid="uuid",physical=2)))
            with self.assertRaises(ValueError):
                restore(fresh,opt,state,binding="changed",uuid="uuid",seed=17,physical=2)
            path.write_bytes(b"corrupted")
            with self.assertRaises(ValueError):
                load_checkpoint(path,pointer)

    def test_orphan_checkpoint_is_not_overwritten(self) -> None:
        """Chỉ adopt đúng payload đầy đủ; không chỉ so weights rồi bỏ qua optimizer."""
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"orphan.pt"
            value={"model":torch.tensor([1.]),"optimizer":{"step":3},"rng":rng_state()}
            pointer=save_checkpoint(path,value)
            self.assertEqual(pointer,save_checkpoint(path,value))
            value["optimizer"]["step"]=4
            with self.assertRaises(ValueError):save_checkpoint(path,value)

    def test_selection_requires_all_sixty_and_preserves_ties(self) -> None:
        """Không promote checkpoint đầu đạt gate hoặc P&L tốt hơn."""
        rows=[{"seed":seed,"step":step,"checkpoint":{"seed":seed,"step":step},"report":{},
               "assessment":{"eligible":True,"mechanism_status":"PASS","market_2021":{"macro_log_loss":.5,"macro_brier":.2}}}
              for seed in SEEDS for step in STEPS]
        with self.assertRaises(ValueError):selection(rows[:1])
        result=selection(list(reversed(rows)))
        self.assertEqual((result["global_candidate_or_none"]["seed"],result["global_candidate_or_none"]["step"]),(17,250))
        for row in rows:row["assessment"].update(eligible=False,mechanism_status="FAIL")
        self.assertEqual(selection(rows)["status"],"NO_ELIGIBLE_CHECKPOINT")

    def test_no_test_open_before_selected_durable_seal(self) -> None:
        """NO_ELIGIBLE không decode synthetic test hoặc outcome2022."""
        seal={"status":"NO_ELIGIBLE_CHECKPOINT"}
        with patch("core.mt_bicl_replica_training.read",return_value=seal) as mocked:
            with self.assertRaises(ValueError):open_test(ROOT,{},seal)
            self.assertEqual(mocked.call_count,1)

    def test_namespace_and_immutable_envelope(self) -> None:
        """Không ghi ra namespace khác hoặc reseal artifact cũ để resume."""
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve()
            with self.assertRaises(ValueError):path_for(root,"../../outside")
            path=path_for(root,"fixture.json");write(path,{"status":"one"})
            with self.assertRaises(ValueError):write(path,{"status":"two"})
            value=json.loads(path.read_bytes());value["payload"]["status"]="poison";path.write_text(json.dumps(value))
            with self.assertRaises(ValueError):read(path)

    def test_extended_index_and_nine_symbol_audit_rebuild_without_network(self) -> None:
        """Cold audit từ responses đã lưu; lịch2181 không thiếu ngày grid hoặc đổi nguồn cũ."""
        original=(ROOT/"data/historical/VNINDEX.csv").read_bytes()
        with patch("core.historical_h02_data.requests.get",side_effect=AssertionError("Không được tải lại")):
            audit=complete_audit(ROOT)
        self.assertTrue(audit["index_ready"])
        self.assertEqual((audit["index_rows"],audit["verified_overlap_rows"]),(2181,249))
        self.assertEqual(audit["grid_dates_missing"],[])
        self.assertEqual(len(audit["symbols"]),9)
        self.assertEqual(next(r for r in audit["symbols"] if r["symbol"]=="BHN")["excluded_prefix_rows"],673)
        self.assertEqual(audit["economic_acceptance"],"PENDING_EXECUTION_DATA")
        self.assertEqual(original,(ROOT/"data/historical/VNINDEX.csv").read_bytes())

    def test_protocol_source_and_data_pins_match_worktree(self) -> None:
        """Không gửi lệnh train với protocol băm nhầm source hoặc dữ liệu."""
        from core.mt_bicl_replica_io import file_hash
        for names in (self.protocol["source_sha256"],self.protocol["data_sha256"]):
            for name,expected in names.items():
                self.assertEqual(file_hash(ROOT/name),expected,name)


if __name__ == "__main__":
    unittest.main()
