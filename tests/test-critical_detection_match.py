# Tests for critical_detection_match code evaluator
# docs/evaluators/critical_detection_match.py — scores 1 only when BOTH predicted and gold severity are 'critical'.

import pytest

from conftest import (
    case_id,
    case_to_run_example,
    load_cases,
    load_evaluator,
    make_example,
    make_gold,
    make_prediction,
    make_run,
)

perform_eval = load_evaluator("critical_detection_match")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def score(run, example=None):
    return perform_eval(run, example)["critical_detection_match"]


# ---------------------------------------------------------------------------
# Data-driven cases (editable by non-developers in
# tests/fixtures/critical_detection_match.json)
# ---------------------------------------------------------------------------

_CASES = load_cases("critical_detection_match")


@pytest.mark.parametrize("case", _CASES, ids=[case_id(c) for c in _CASES])
def test_fixture_cases(case):
    run, example = case_to_run_example(case)
    assert score(run, example) == case["expected_score"]


# ---------------------------------------------------------------------------
# Technical edge cases (input shapes the JSON fixtures can't express)
# ---------------------------------------------------------------------------

class TestBothCritical:
    def test_both_critical_returns_1(self):
        run = make_run(make_prediction(severity="critical"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1


class TestBothNonCritical:
    def test_both_minor_returns_0(self):
        run = make_run(make_prediction(severity="minor"))
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0

    def test_both_different_non_critical_returns_0(self):
        # Neither side is critical → 0 regardless of how they compare
        run = make_run(make_prediction(severity="major"))
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0


class TestMismatch:
    def test_predicted_critical_gold_non_critical_returns_0(self):
        run = make_run(make_prediction(severity="critical"))
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0

    def test_predicted_non_critical_gold_critical_returns_0(self):
        run = make_run(make_prediction(severity="minor"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 0


class TestNormalization:
    def test_severity_case_insensitive(self):
        run = make_run(make_prediction(severity="CRITICAL"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1

    def test_severity_whitespace_trimmed(self):
        run = make_run(make_prediction(severity="  critical  "))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1


class TestNestedOutput:
    def test_prediction_nested_under_output_key(self):
        run = make_run(make_prediction(severity="critical", wrap="output"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1

    def test_prediction_nested_under_prediction_key(self):
        run = make_run(make_prediction(severity="minor", wrap="prediction"))
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0


class TestJsonStringInput:
    def test_outputs_as_json_string(self):
        run = make_run(make_prediction(severity="critical", as_json=True))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1

    def test_malformed_json_treated_as_non_critical(self):
        # Malformed JSON → {} → no severity key → "" → not critical → 0
        run = make_run("{bad json}")
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0


class TestMissingKeys:
    def test_both_severity_missing_returns_0(self):
        # Both default to "" → neither is critical → 0
        run = make_run(make_prediction())
        example = make_example(make_gold())
        assert score(run, example) == 0


class TestExampleNoneFallback:
    def test_gold_from_run_reference_outputs(self):
        gold = make_gold(severity="critical")
        run = make_run(make_prediction(severity="critical"), reference_outputs=gold)
        assert score(run, example=None) == 1

    def test_mismatch_via_run_reference_outputs(self):
        gold = make_gold(severity="critical")
        run = make_run(make_prediction(severity="minor"), reference_outputs=gold)
        assert score(run, example=None) == 0
