"""Emit synthetic benchmark results from a deterministic position-biased toy.

Run standalone with Python 3.9+. No network, imports from the package, model
services, external files, environment variables or nondeterminism.
"""
import json


def demo():
    questions = [("q1", "2+2=?", ["4", "5"], "4"),
                 ("q2", "2+3=?", ["4", "5"], "5")]
    rows = []
    for condition, shift in (("original", 0), ("rotated", 1)):
        for item_id, question, options, correct_answer in questions:
            displayed = options[shift:] + options[:shift]
            # The toy always emits A, regardless of the question. The question
            # text remains here so the example's semantic validity is inspectable.
            predicted_answer = displayed[0]
            rows.append({"item_id": item_id, "condition": condition,
                         "correct": predicted_answer == correct_answer})
    return {"rows": rows,
            "expected_metrics": {"n_items": 2,
                "per_condition_accuracy": {"original": 0.5, "rotated": 0.5},
                "max_drift": 0.0, "correctness_flip_rate": 1.0}}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
