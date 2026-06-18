# Tests for critical_agreement code evaluator
# docs/evaluators/critical_agreement.py — scores 1 only when BOTH predicted and gold severity are 'critical'.

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

perform_eval = load_evaluator("critical_agreement")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def score(run, example=None):
    return perform_eval(run, example)["critical_agreement"]


# ---------------------------------------------------------------------------
# Data-driven cases (editable by non-developers in
# tests/fixtures/critical_agreement.json)
# ---------------------------------------------------------------------------

_CASES = load_cases("critical_agreement")


@pytest.mark.parametrize("case", _CASES, ids=[case_id(c) for c in _CASES])
def test_fixture_cases(case):
    run, example = case_to_run_example(case)
    assert score(run, example) == case["expected_score"]


# ---------------------------------------------------------------------------
# Technical edge cases (input shapes the JSON fixtures can't express)
# ---------------------------------------------------------------------------

class TestNestedOutput:
    def test_prediction_nested_under_output_key(self):
        run = make_run(make_prediction(severity="critical", wrap="output"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1

    def test_prediction_nested_under_prediction_key_not_supported(self):
        # This evaluator only reads outputs["output"] or top-level outputs keys.
        # A nested outputs["prediction"] payload is treated as missing severity.
        run = make_run(make_prediction(severity="critical", wrap="prediction"))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 0


class TestJsonStringInput:
    def test_outputs_as_json_string(self):
        run = make_run(make_prediction(severity="critical", as_json=True))
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 1

    def test_malformed_json_treated_as_non_critical(self):
        run = make_run("{bad json}")
        example = make_example(make_gold(severity="critical"))
        assert score(run, example) == 0


class TestMissingKeys:
    def test_both_severity_missing_returns_0(self):
        run = make_run(make_prediction())
        example = make_example(make_gold())
        assert score(run, example) == 0


class TestExampleNone:
    def test_example_none_returns_0_even_if_reference_outputs_exist(self):
        # This evaluator does not read run["reference_outputs"].
        gold = make_gold(severity="critical")
        run = make_run(make_prediction(severity="critical"), reference_outputs=gold)
        assert score(run, example=None) == 0
