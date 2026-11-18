"""Kiểm receipt FIN09, slot identity và quota một org không mạng."""
import unittest

from core.finalize_budget_archive import fingerprints, match
from core.finalize_budget_quota import capacity_windows, charge, summarize, window
from core.finalize_budget_study import MODEL_DECISION, MODEL_VISION, slot_row
from core.groq_pacing import MODEL_LIMITS


class FinalizeBudgetTests(unittest.TestCase):
    def test_fingerprint_separates_picture_options_and_message(self) -> None:
        def body(image: str, words: str, max_tokens: int) -> dict:
            return {"model": MODEL_VISION, "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": [{"type": "text", "text": words},
                    {"type": "image_url", "image_url": {"url": image}}]}]}

        first = fingerprints(body("data:image/png;base64,AA==", "Tăng", 960))
        for image, words, cap, field in (("data:image/png;base64,AB==", "Tăng", 960, "images"),
                                         ("data:image/png;base64,AA==", "Giảm", 960, "messages"),
                                         ("data:image/png;base64,AA==", "Tăng", 480, "options")):
            other = fingerprints(body(image, words, cap))
            self.assertEqual({k for k in first if first[k] != other[k]}, {field, "wire"})

    def test_exact_match_still_requires_same_repeat_and_verified_parents(self) -> None:
        body = {"wire": "1"*64}
        old = {"fingerprints": body, "status": 200, "repair": False}
        self.assertEqual(match(body, old, parents_verified=True)[0], "REUSE")
        self.assertEqual(match(body, old, parents_verified=False)[0], "NEW")
        self.assertEqual(match(body, old, parents_verified=True, conditional=True)[0], "NEW")
        self.assertEqual(match(body, {**old, "repair": True}, parents_verified=True)[0], "NEW")
        self.assertEqual(match({"wire": "2"*64}, old, parents_verified=True)[0], "NEW")
        self.assertEqual(match(None, old, parents_verified=True)[0], "BYPASS")

    def test_unknown_is_reserved_until_reconciled_and_bounded_by_window(self) -> None:
        body = {"wire": "1"*64}
        old = {"fingerprints": body, "status": "UNKNOWN", "repair": False}
        self.assertEqual(match(body, old, parents_verified=True)[0], "UNKNOWN")
        self.assertEqual(match(body, old, parents_verified=True, conditional=True)[0], "NEW")
        row = {"id": "a", "started_at": 1000, "status": "UNKNOWN", "total_tokens": 12, "reserved_tokens": 999}
        self.assertEqual(charge(row), 999)
        self.assertEqual(window([row, row, {**row, "id": "b", "status": "NOT_SENT"}], 1060, 61),
                         {"requests": 1, "tokens_charged_or_reserved": 999, "unknown": 1})
        self.assertEqual(window([row], 1061, 61)["requests"], 0)
        self.assertEqual(window([row], 999, 61)["requests"], 0)
        with self.assertRaises(ValueError):
            window([row, {**row, "reserved_tokens": 998}], 1060, 61)

    def test_retry_repair_and_smoke_caps_are_separate(self) -> None:
        body = {"model": MODEL_DECISION, "max_tokens": 960, "messages": [{"role": "user", "content": "Fixture"}],
                "response_format": {"type": "json_schema"}}
        research = slot_row("RESEARCH", "forecast/FPT/u0/r0/original_common", "original_common", body, None,
                            conditional=True, parents_verified=False, dependencies={})
        smoke = slot_row("SMOKE", "forecast/FPT/u0/r0/original_common", "original_common", body, None,
                         conditional=True, parents_verified=False, dependencies={})
        bypass = slot_row("RESEARCH", "forecast/FPT/u0/r0/C2", "C2", None, None,
                          conditional=True, parents_verified=False, dependencies={}, bypass_reason="INSUFFICIENT_EVIDENCE")
        limits = {"assumed_limits": MODEL_LIMITS[MODEL_DECISION], "local_estimated_day_tokens_remaining": 0,
                  "local_estimated_day_requests_remaining": 0}
        total = summarize([research, smoke, bypass], {"models": dict.fromkeys(MODEL_LIMITS, limits)},
                          {"original_common": {"p50": 1200, "p95": 1400}})
        self.assertEqual(total["RESEARCH"]["states"], {"NEW": 1, "BYPASS": 1})
        self.assertEqual(total["SMOKE"]["models"][MODEL_DECISION]["max_attempts"], 3)
        self.assertGreater(research["all_attempts_reserve_tokens"], 3*research["attempt_reserve_tokens"])
        self.assertEqual(total["RESEARCH"]["models"][MODEL_DECISION]["historical_usage_p95_scenario"], 1400)
        self.assertEqual(bypass["attempt_reserve_tokens"], 0)

    def test_capacity_does_not_multiply_org(self) -> None:
        quota = {"assumed_limits": MODEL_LIMITS[MODEL_DECISION], "local_estimated_day_tokens_remaining": 196083,
                 "local_estimated_day_requests_remaining": 998}
        self.assertEqual(capacity_windows(0, 0, quota), 0)
        self.assertEqual(capacity_windows(196083, 998, quota), 1)
        self.assertEqual(capacity_windows(196084, 998, quota), 2)
        self.assertEqual(capacity_windows(196083, 1999, quota), 3)


if __name__ == "__main__":
    unittest.main()
