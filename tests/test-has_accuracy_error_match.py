"""Unit tests for docs/evaluators/has_accuracy_error_match.py"""

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

perform_eval = load_evaluator("has_accuracy_error_match")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def score(run, example=None):
    return perform_eval(run, example)["has_accuracy_error_match"]


# ---------------------------------------------------------------------------
# Data-driven cases (editable by non-developers in
# tests/fixtures/has_accuracy_error_match.json)
# ---------------------------------------------------------------------------

_CASES = load_cases("has_accuracy_error_match")


@pytest.mark.parametrize("case", _CASES, ids=[case_id(c) for c in _CASES])
def test_fixture_cases(case):
    run, example = case_to_run_example(case)
    assert score(run, example) == case["expected_score"]


# ---------------------------------------------------------------------------
# Technical edge cases (input shapes the JSON fixtures can't express)
# ---------------------------------------------------------------------------

class TestBothNoError:
    def test_both_none_returns_1(self):
        # "none" subtype means no accuracy error present
        run = make_run(make_prediction(subtype="none"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1


class TestBothHaveError:
    def test_both_have_error_same_subtype_returns_1(self):
        run = make_run(make_prediction(subtype="omission"))
        example = make_example(make_gold(subtype="omission"))
        assert score(run, example) == 1

    def test_both_have_error_different_subtypes_returns_1(self):
        # Presence of *any* error is what matters, not the specific subtype
        run = make_run(make_prediction(subtype="addition"))
        example = make_example(make_gold(subtype="omission"))
        assert score(run, example) == 1


class TestMismatch:
    def test_predicted_none_gold_has_error_returns_0(self):
        run = make_run(make_prediction(subtype="none"))
        example = make_example(make_gold(subtype="mistranslation"))
        assert score(run, example) == 0

    def test_predicted_has_error_gold_none_returns_0(self):
        run = make_run(make_prediction(subtype="untranslated"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 0


class TestNormalization:
    def test_case_insensitive_none(self):
        run = make_run(make_prediction(subtype="NONE"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1

    def test_whitespace_trimmed_none(self):
        run = make_run(make_prediction(subtype="  none  "))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1


class TestNestedOutput:
    def test_prediction_nested_under_output_key(self):
        run = make_run(make_prediction(subtype="omission", wrap="output"))
        example = make_example(make_gold(subtype="omission"))
        assert score(run, example) == 1

    def test_prediction_nested_under_prediction_key(self):
        run = make_run(make_prediction(subtype="none", wrap="prediction"))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1


class TestJsonStringInput:
    def test_outputs_as_json_string_no_error(self):
        run = make_run(make_prediction(subtype="none", as_json=True))
        example = make_example(make_gold(subtype="none"))
        assert score(run, example) == 1

    def test_malformed_json_treated_as_has_error(self):
        # Malformed JSON → {} → subtype "" → not "none" → has_error=True
        # Gold also missing key → "" → not "none" → has_error=True → match
        run = make_run("{bad json}")
        example = make_example(make_gold())
        assert score(run, example) == 1


class TestMissingKeys:
    def test_both_keys_missing_treated_as_has_error_match(self):
        # Missing key → "" → not "none" → both have_error=True → match → 1
        run = make_run(make_prediction())
        example = make_example(make_gold())
        assert score(run, example) == 1


class TestExampleNoneFallback:
    def test_gold_from_run_reference_outputs_no_error(self):
        gold = make_gold(subtype="none")
        run = make_run(make_prediction(subtype="none"), reference_outputs=gold)
        assert score(run, example=None) == 1

    def test_mismatch_via_run_reference_outputs(self):
        gold = make_gold(subtype="none")
        run = make_run(make_prediction(subtype="untranslated"), reference_outputs=gold)
        assert score(run, example=None) == 0
