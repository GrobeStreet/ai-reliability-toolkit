"""Offline paired-result check. Read one JSON object from stdin; emit JSON.

Python 3.9+, standard library only. No network, file access, model calls or
dependencies. Expected metrics are supplied claims, not independent truth.
"""
import hashlib
import json
import math
import platform
import sys

VERSION = "0.3.0"
MAX_BYTES = 20_000_000
MAX_ROWS = 100_000


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key: " + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError("non-finite JSON constant: " + value)


def rate(value, name):
    if type(value) not in (int, float) or not 0 <= value <= 1 or not math.isfinite(value):
        raise ValueError(name + " must be a finite number between 0 and 1")
    return value


def analyze(document):
    if not isinstance(document, dict):
        raise ValueError("input must be an object containing rows")
    allowed = {"rows", "expected_metrics", "criteria", "criteria_predeclared"}
    if set(document) - allowed:
        raise ValueError("unknown input field(s): " + ", ".join(sorted(set(document) - allowed)))
    rows = document.get("rows")
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ROWS:
        raise ValueError("rows must be a non-empty list of at most 100000 cells")
    cells = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"item_id", "condition", "correct"}:
            raise ValueError("every row needs exactly item_id, condition and correct")
        for field in ("item_id", "condition"):
            value = row[field]
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ValueError(field + " must be a non-empty string without outer whitespace")
        if type(row["correct"]) is not bool:
            raise ValueError("correct must be a JSON boolean, never a string or number")
        pair = (row["item_id"], row["condition"])
        if pair in cells:
            raise ValueError("duplicate item/condition cell")
        cells[pair] = row["correct"]
    items = sorted({i for i, _ in cells})
    conditions = sorted({c for _, c in cells})
    if len(conditions) < 2:
        raise ValueError("at least two conditions are required")
    if len(cells) != len(items) * len(conditions):
        raise ValueError("every item must appear exactly once in every condition")
    n = len(items)
    successes = {c: sum(cells[i, c] for i in items) for c in conditions}
    accuracy = {c: successes[c] / n for c in conditions}
    changed = [i for i in items if len({cells[i, c] for c in conditions}) > 1]
    metrics = {"n_items": n, "per_condition_accuracy": accuracy,
               "max_drift": (max(successes.values()) - min(successes.values())) / n,
               "correctness_flip_rate": len(changed) / n}
    reproduction = {"status": "not_checked", "scope": "supplied-result arithmetic only",
                    "upstream_model_run": "not independently reproduced"}
    if "expected_metrics" in document:
        expected = document["expected_metrics"]
        if not isinstance(expected, dict) or set(expected) != set(metrics):
            raise ValueError("expected_metrics must contain exactly the four reported metric fields")
        if type(expected["n_items"]) is not int or expected["n_items"] < 1:
            raise ValueError("expected n_items must be a positive integer")
        ea = expected["per_condition_accuracy"]
        if not isinstance(ea, dict) or set(ea) != set(conditions):
            raise ValueError("expected accuracy conditions must match the input")
        checks = {"n_items": expected["n_items"] == n}
        for c in conditions:
            checks["accuracy:" + c] = math.isclose(
                rate(ea[c], "expected accuracy"), accuracy[c], rel_tol=0, abs_tol=1e-12)
        for key in ("max_drift", "correctness_flip_rate"):
            checks[key] = math.isclose(rate(expected[key], key), metrics[key],
                                       rel_tol=0, abs_tol=1e-12)
        reproduction.update(status="matches_supplied_expectations" if all(checks.values()) else "mismatch",
                            checks=checks, absolute_tolerance=1e-12)
    criteria_result = {"status": "not_assessed", "reason": "no predeclared criteria supplied"}
    predeclared = document.get("criteria_predeclared", False)
    if type(predeclared) is not bool:
        raise ValueError("criteria_predeclared must be a boolean")
    if "criteria" in document:
        criteria = document["criteria"]
        mapping = {"max_accuracy_drift": "max_drift",
                   "max_correctness_flip_rate": "correctness_flip_rate"}
        if not isinstance(criteria, dict) or not criteria or set(criteria) - set(mapping):
            raise ValueError("criteria supports max_accuracy_drift and max_correctness_flip_rate only")
        for name, value in criteria.items():
            rate(value, name)
        if predeclared:
            checks = {name: {"observed": metrics[mapping[name]], "maximum": limit,
                             "met": metrics[mapping[name]] <= limit}
                      for name, limit in criteria.items()}
            criteria_result = {"status": "observed_criteria_met" if all(c["met"] for c in checks.values())
                               else "observed_criterion_failed", "checks": checks,
                               "predeclaration": "user asserted; not independently verified"}
        else:
            criteria_result["reason"] = "criteria supplied without asserted predeclaration"
    canonical = [{"item_id": i, "condition": c, "correct": cells[i, c]}
                 for i in items for c in conditions]
    canonical_bytes = json.dumps(canonical, ensure_ascii=False, sort_keys=True,
                                separators=(",", ":")).encode("utf-8")
    return {"schema_version": "1", "tool_version": VERSION,
            "evidence_status": "calculated from supplied data", "metrics": metrics,
            "counts": {"original_items": n, "condition_cells": len(cells),
                       "items_with_correctness_changes": len(changed)},
            "changed_item_ids": changed, "reproduction": reproduction,
            "observed_criteria": criteria_result, "readiness": "not_assessed",
            "canonical_rows_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
            "not_measured": ["underlying-answer changes", "calibration", "transformation validity",
                             "independent upstream model execution", "population uncertainty"],
            "limitations": ["Correctness changes are not underlying-answer changes.",
                            "No sampling model or uncertainty interval is inferred.",
                            "Low drift does not establish invariance, equivalence or readiness.",
                            "Expected metrics are supplied claims; a match checks arithmetic only."]}


def main():
    raw = sys.stdin.buffer.read(MAX_BYTES + 1)
    try:
        if len(raw) > MAX_BYTES:
            raise ValueError("input exceeds 20 MB")
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_object,
                              parse_constant=invalid_constant)
        result = analyze(document)
        result["execution"] = {"input_sha256": hashlib.sha256(raw).hexdigest(),
                               "python": platform.python_version(),
                               "implementation": platform.python_implementation()}
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False, allow_nan=False)
        print()
        return 1 if result["reproduction"]["status"] == "mismatch" else 0
    except (ValueError, UnicodeError, RecursionError) as error:
        json.dump({"error": str(error), "readiness": "not_assessed"}, sys.stderr)
        print(file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
