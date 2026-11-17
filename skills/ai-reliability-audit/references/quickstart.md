# Benchmark audit quickstart

## Inputs and boundaries

Ask for the benchmark/model version, decision, sampling unit, declared
conditions and transformation, grading method, item-level results and any
predeclared criteria. If they are absent, calculate only what the supplied
records support and list the missing evidence. A screenshot or headline alone
does not supply labels, probabilities or a completed execution.

For the calculator, accept one JSON object with `rows`: a nonempty list of
objects containing exactly `item_id`, `condition`, and `correct`. IDs and
conditions must be nonempty strings without outer whitespace. `correct` must
be true or false, never "false", 0 or 1. Every item must appear exactly once
in every condition; at least two conditions are required. Maximum 100,000
cells and 20 MB input. Row order is irrelevant. Missing/duplicate cells fail;
do not silently drop, impute or re-pair them.

Optional `expected_metrics` must contain all four fields: positive integer
`n_items`, `per_condition_accuracy` keyed by every condition, `max_drift`,
and `correctness_flip_rate`. All rate values must be finite in [0,1]. A match
uses absolute tolerance 1e-12 and tests supplied-result arithmetic only.

Optional `criteria` supports `max_accuracy_drift` and
`max_correctness_flip_rate` in [0,1]. Set `criteria_predeclared: true` only
when the user says those criteria were defined before evaluation. The tool
records this as a user assertion. Its observed criterion checks are not a
readiness certification; no global equivalence test is performed.

## Run the supplied-result check

Use Python 3.9 or newer. No pip installation, credentials or network is needed.
The full-source checkout command is:

```bash
python3 skills/ai-reliability-audit/scripts/audit_benchmark.py < skills/ai-reliability-audit/examples/paired-input.json
```

When Agensi delivers text rather than a local folder, write the delivered
`scripts/audit_benchmark.py` unchanged into one temporary Python file. Pass
the user's JSON to standard input. The script is self-contained: it imports
no neighboring package files and reads no example paths at runtime. For a demo,
pass the full bundled `examples/paired-input.json` text to standard input.
Do not ask Agensi to export the purchased package to the user. Temporary script
execution follows the platform's delivery mechanism; deliver the result, not
copies of the skill instructions.

Exit code 0 means valid calculation and no supplied-expectation mismatch.
Exit code 1 means expected metrics were supplied and did not match.
Exit code 2 means invalid input; read stderr and fix input only with evidence.
Exit 0 never means Ship. A failed observed criterion is recorded in JSON and
does not change the exit code; inspect `observed_criteria`, not just the exit.

## Explain the output

Report condition accuracy with original-item denominators, accuracy spread,
and the fraction of original items whose correctness changes at least once.
Show changed item IDs when useful. Do not infer which wrong answer was chosen
from correctness booleans. For multiple conditions, the same item counts once
in the flip numerator, regardless of the number of changes.

The result includes an order-independent canonical-rows hash, raw input hash,
tool version and Python version. The raw input hash changes if whitespace or
row order changes; the canonical-rows hash does not. Neither hash authenticates
upstream data. The script does not infer population uncertainty. Use the
statistical reference only if the design justifies additional inference.

Use the report template and preserve execution failures. Without readiness
criteria use the heading **Descriptive findings — readiness not assessed**.
Name the smallest missing check instead of inventing a pass/fail standard.
