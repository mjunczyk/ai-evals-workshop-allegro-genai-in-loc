import json


def _as_dict(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _prediction(outputs):
    data = _as_dict(outputs)
    if "output" in data:
        nested = _as_dict(data["output"])
        if nested:
            return nested
    if "prediction" in data:
        nested = _as_dict(data["prediction"])
        if nested:
            return nested
    return data


def _pick(mapping, *keys):
    if not mapping:
        return None
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _normalize_label(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def perform_eval(run, example=None):
    """Score 1 when predicted Accuracy subtype matches the gold subtype."""
    outputs = run["outputs"]
    reference_outputs = (example or {}).get("outputs") or run.get("reference_outputs") or {}

    predicted = _normalize_label(
        _pick(_prediction(outputs), "accuracy_subtype", "gold_accuracy_subtype")
    )
    gold = _normalize_label(
        _pick(_as_dict(reference_outputs), "gold_accuracy_subtype", "accuracy_subtype")
    )

    return {"accuracy_subtype_match": int(predicted == gold)}
