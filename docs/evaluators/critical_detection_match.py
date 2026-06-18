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
    """Score 1 only when both predicted and gold severity are 'critical'."""
    outputs = run["outputs"]
    reference_outputs = (example or {}).get("outputs") or run.get("reference_outputs") or {}

    predicted_severity = _normalize_label(
        _pick(_prediction(outputs), "severity", "gold_severity")
    )
    gold_severity = _normalize_label(
        _pick(_as_dict(reference_outputs), "gold_severity", "severity")
    )

    predicted_is_critical = predicted_severity == "critical"
    gold_is_critical = gold_severity == "critical"

    return {"critical_detection_match": int(predicted_is_critical and gold_is_critical)}
