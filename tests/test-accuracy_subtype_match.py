"""Unit tests for docs/evaluators/accuracy_subtype_match.py"""

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

perform_eval = load_evaluator("accuracy_subtype_match")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def score(run, example=None):
    return perform_eval(run, example)["accuracy_subtype_match"]


# ---------------------------------------------------------------------------
# Data-driven cases (editable by non-developers in
# tests/fixtures/accuracy_subtype_match.json)
# ---------------------------------------------------------------------------

_CASES = load_cases("accuracy_subtype_match")


@pytest.mark.parametrize("case", _CASES, ids=[case_id(c) for c in _CASES])
def test_fixture_cases(case):
    run, example = case_to_run_example(case)
    assert score(run, example) == case["expected_score"]


# ---------------------------------------------------------------------------
# Technical edge cases (input shapes the JSON fixtures can't express)
# ---------------------------------------------------------------------------

class TestNestedOutput:
    def test_prediction_nested_under_output_key(self):
        run = make_run(make_prediction(subtype="none", wrap="output"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1

    def test_prediction_nested_under_prediction_key(self):
        run = make_run(make_prediction(subtype="none", wrap="prediction"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1

    def test_mismatch_with_nested_output(self):
        run = make_run(make_prediction(subtype="mistranslation", wrap="output"))
        example = make_example(make_gold(subtype="omission"))
        assert score(run, example) == 0


class TestJsonStringInput:
    def test_outputs_as_json_string_match(self):
        run = make_run(make_prediction(subtype="none", as_json=True))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1

    def test_malformed_json_string_treated_as_empty(self):
        # Malformed JSON → _as_dict returns {} → predicted is ""
        # Gold is also missing → ""  → both "" → match → 1
        run = make_run("{not valid json}")
        example = make_example(make_gold())
        assert score(run, example) == 1

    def test_malformed_json_vs_real_gold_returns_0(self):
        run = make_run("{not valid json}")
        example = make_example(make_gold(subtype="mistranslation"))
        assert score(run, example) == 0


class TestMissingKeys:
    def test_both_keys_missing_match(self):
        # Neither side has accuracy_subtype → both normalise to "" → match
        run = make_run(make_prediction())
        example = make_example(make_gold())
        assert score(run, example) == 1


class TestExampleNoneFallback:
    def test_gold_read_from_run_reference_outputs(self):
        gold = make_gold(subtype="mistranslation")
        run = make_run(make_prediction(subtype="mistranslation"), reference_outputs=gold)
        assert score(run, example=None) == 1

    def test_mismatch_via_run_reference_outputs(self):
        gold = make_gold(subtype="none")
        run = make_run(make_prediction(subtype="mistranslation"), reference_outputs=gold)
        assert score(run, example=None) == 0
