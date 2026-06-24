import json
import re


def _model_payload(run):
    out = None
    try:
        out = run["outputs"]["output"]
    except (KeyError, TypeError):
        try:
            out = run["outputs"]
        except (KeyError, TypeError):
            return {}
    content = None
    if isinstance(out, str):
        content = out
    elif isinstance(out, dict):
        c = out.get("content")
        if isinstance(c, str):
            content = c
        elif isinstance(c, list):
            content = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
        elif "accuracy_subtype" in out or "severity" in out:
            return out
    if not content:
        return {}
    text = content.strip()
    fenced = re.search(r"`{3,}(?:json)?\s*(.*?)`{3,}", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        first_obj = re.search(r"\{.*?\}", text, re.DOTALL)
        if first_obj:
            try:
                return json.loads(first_obj.group(0))
            except Exception:
                return {}
    return {}


def _norm(value):
    return str(value).strip().lower() if value is not None else ""


def _gold(example, key):
    try:
        return example["outputs"].get(key)
    except (KeyError, TypeError):
        return None


def perform_eval(run, example):
    payload = _model_payload(run)
    model_severity = _norm(payload.get("severity"))
    gold_severity = _norm(_gold(example, "gold_severity"))

    if gold_severity != "critical":
        return {"critical_agreement": None}

    if not model_severity:
        return {"critical_agreement": 0}

    score = 1 if model_severity == "critical" else 0
    return {"critical_agreement": score}
