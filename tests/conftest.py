"""
Shared test-data builder helpers for evaluator unit tests.

Quick reference
---------------
make_prediction(subtype=..., severity=..., wrap=None, as_json=False)
    Build an outputs payload (what the model predicted).
    wrap="output"      → {"output": {...}}
    wrap="prediction"  → {"prediction": {...}}
    as_json=True       → serialise the whole thing to a JSON string

make_gold(subtype=..., severity=...)
    Build a gold/reference outputs dict (uses "gold_" prefixed keys).

make_run(outputs, reference_outputs=None)
    Wrap prediction + optional reference into a run dict.

make_example(outputs)
    Wrap gold outputs into an example dict.

load_cases(name) / case_to_run_example(case) / case_id(case)
    Load and convert plain-English JSON mockup data from tests/fixtures/.
    These let non-technical users add test cases by editing JSON only.
"""

import importlib.util
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Evaluator loading
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent
_EVALUATORS_DIR = _REPO_ROOT / "docs" / "evaluators"


def load_evaluator(name: str):
    """Import an evaluator module from docs/evaluators/<name>.py and return its
    ``perform_eval`` callable.

    Raises a clear, actionable error if the evaluator file is missing (e.g. after
    a repository restructure) instead of a cryptic FileNotFoundError raised deep
    inside the import machinery at collection time.
    """
    path = _EVALUATORS_DIR / f"{name}.py"
    if not path.is_file():
        raise FileNotFoundError(
            f"Evaluator '{name}' not found at {path}. "
            f"Expected it under {_EVALUATORS_DIR}. "
            "If the evaluators moved, update tests/conftest.py:_EVALUATORS_DIR."
        )
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load evaluator spec for '{name}' from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.perform_eval


# ---------------------------------------------------------------------------
# Prediction payload
# ---------------------------------------------------------------------------

def make_prediction(
    subtype: str | None = None,
    severity: str | None = None,
    wrap: str | None = None,
    as_json: bool = False,
):
    """Return an outputs value suitable for run["outputs"].

    Parameters
    ----------
    subtype:
        Value for the ``accuracy_subtype`` key.
    severity:
        Value for the ``severity`` key.
    wrap:
        If ``"output"`` wrap payload under an ``output`` key.
        If ``"prediction"`` wrap under a ``prediction`` key.
        ``None`` (default) leaves the payload flat.
    as_json:
        Serialise the result to a JSON string instead of returning a dict.
    """
    inner: dict = {}
    if subtype is not None:
        inner["accuracy_subtype"] = subtype
    if severity is not None:
        inner["severity"] = severity

    if wrap == "output":
        data: dict = {"output": inner}
    elif wrap == "prediction":
        data = {"prediction": inner}
    else:
        data = inner

    return json.dumps(data) if as_json else data


# ---------------------------------------------------------------------------
# Gold / reference payload
# ---------------------------------------------------------------------------

def make_gold(
    subtype: str | None = None,
    severity: str | None = None,
) -> dict:
    """Return a gold outputs dict (uses ``gold_`` prefixed keys)."""
    data: dict = {}
    if subtype is not None:
        data["gold_accuracy_subtype"] = subtype
    if severity is not None:
        data["gold_severity"] = severity
    return data


# ---------------------------------------------------------------------------
# run / example containers
# ---------------------------------------------------------------------------

def make_run(outputs, reference_outputs=None) -> dict:
    """Assemble a *run* dict as the evaluators expect it.

    Parameters
    ----------
    outputs:
        The model-predicted payload (dict or JSON string).
    reference_outputs:
        Optional gold dict placed at ``run["reference_outputs"]``.
        Useful when testing the ``example=None`` fallback path.
    """
    run: dict = {"outputs": outputs}
    if reference_outputs is not None:
        run["reference_outputs"] = reference_outputs
    return run


def make_example(outputs: dict) -> dict:
    """Assemble an *example* dict as the evaluators expect it."""
    return {"outputs": outputs}


# ---------------------------------------------------------------------------
# Friendly fixture loading (for non-technical editors)
# ---------------------------------------------------------------------------
#
# Business-level test cases live as plain JSON in tests/fixtures/<name>.json.
# Each case mirrors the workshop dataset columns (see docs/datasets/Czech):
#
#   id, source, target            -> human-readable context (optional)
#   predicted_accuracy_subtype    -> what the model/judge answered
#   predicted_severity            -> what the model/judge answered
#   gold_accuracy_subtype         -> the correct answer (dataset gold_*)
#   gold_severity                 -> the correct answer (dataset gold_*)
#   expected_score                -> 1 if it should MATCH, else 0
#
# A null value means "this field is missing" (key omitted from the payload).

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_cases(name: str) -> list[dict]:
    """Read tests/fixtures/<name>.json and return its list of cases.

    The top-level ``_README`` key (editor instructions) is ignored.
    """
    path = _FIXTURES_DIR / f"{name}.json"
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data["cases"]


def case_to_run_example(case: dict) -> tuple[dict, dict]:
    """Turn a friendly fixture case into (run, example) the evaluators expect.

    Reads the ``predicted_*`` / ``gold_*`` fields. Missing or ``null`` fields
    are simply omitted from the payloads.
    """
    run = make_run(
        make_prediction(
            subtype=case.get("predicted_accuracy_subtype"),
            severity=case.get("predicted_severity"),
        )
    )
    example = make_example(
        make_gold(
            subtype=case.get("gold_accuracy_subtype"),
            severity=case.get("gold_severity"),
        )
    )
    return run, example


def case_id(case: dict) -> str:
    """Human-readable label for a parametrized case (shown in test reports)."""
    return case.get("name") or case.get("id") or "case"
