# Tests for severity_exact_match code evaluator
# docs/evaluators/severity_exact_match.py — scores 1 when predicted severity equals the gold severity.

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

perform_eval = load_evaluator("severity_exact_match")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def score(run, example=None):
    return perform_eval(run, example)["severity_exact_match"]


# ---------------------------------------------------------------------------
# Data-driven cases (editable by non-developers in
# tests/fixtures/severity_exact_match.json)
# ---------------------------------------------------------------------------

_CASES = load_cases("severity_exact_match")


@pytest.mark.parametrize("case", _CASES, ids=[case_id(c) for c in _CASES])
def test_fixture_cases(case):
    run, example = case_to_run_example(case)
    assert score(run, example) == case["expected_score"]


# ---------------------------------------------------------------------------
# Technical edge cases (input shapes the JSON fixtures can't express)
# ---------------------------------------------------------------------------

class TestNestedOutput:
    def test_prediction_nested_under_output_key(self):
        run = make_run(make_prediction(severity="major", wrap="output"))
        example = make_example(make_gold(severity="major"))
        assert score(run, example) == 1

    def test_prediction_nested_under_prediction_key_not_supported(self):
        run = make_run(make_prediction(severity="major", wrap="prediction"))
        example = make_example(make_gold(severity="major"))
        assert score(run, example) == 0


class TestJsonStringInput:
    def test_outputs_as_json_string(self):
        run = make_run(make_prediction(severity="none", as_json=True))
        example = make_example(make_gold(severity="none"))
        assert score(run, example) == 1

    def test_malformed_json_string_treated_as_missing_prediction(self):
        run = make_run("{not valid json}")
        example = make_example(make_gold(severity="major"))
        assert score(run, example) == 0


class TestMissingKeys:
    def test_model_missing_gold_present_returns_0(self):
        run = make_run(make_prediction())
        example = make_example(make_gold(severity="minor"))
        assert score(run, example) == 0

    def test_both_missing_returns_0(self):
        run = make_run(make_prediction())
        example = make_example(make_gold())
        assert score(run, example) == 0


class TestExampleNone:
    def test_example_none_returns_0_even_if_reference_outputs_exist(self):
        gold = make_gold(severity="major")
        run = make_run(make_prediction(severity="major"), reference_outputs=gold)
        assert score(run, example=None) == 0
