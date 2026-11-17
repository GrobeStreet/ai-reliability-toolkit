---
name: ai-reliability-audit
description: Plan and, when tools and evidence are available, execute a scoped audit of AI outputs, model features, benchmark results, or statistical claims. Use for reliability audits, stress tests, reproducibility checks, or readiness questions. Separate observed measurements from proposed tests and return a decision-specific Ship, Caution, or Not-ready assessment without inventing evidence.
---

# AI Reliability Audit

Build an evidence-backed assessment for a specific decision. This skill is a
procedure, not an executable harness or independent certification.

## Establish the evidence boundary first

Record the system/claim version, intended use, decision owner, acceptable failure
rates and severities, target population, available data, labels, code, tools,
and budget. Agree the decision thresholds before evaluating. If thresholds are
missing, provide descriptive findings and request the missing criteria; do not
invent a readiness standard.

Classify each check as **measured**, **source-inspected**, **reported by others**,
**proposed**, **not measured**, or **not applicable**. Preserve this distinction
in the final report. Source inspection and a written protocol are not execution.
Use **not measured** whenever required inputs or tool-supported runs are absent.
Never fabricate a dataset, sample size, output, confidence interval, or run log.

You may compute descriptive summaries from supplied records. Label them
**calculated from supplied data** and distinguish the calculation you executed
from the upstream model run or outcome labels you have not independently
verified. A calculation does not upgrade reported evidence to replication.

Without observed outcome labels, do not claim to measure accuracy or empirical
calibration. You may inspect confidence behavior and measure repeat consistency
when actual repeated outputs exist. Missing evidence is not proof of a defect,
and an audit without measurements cannot earn Ship.

## Define the measurement before running

Specify the estimand and sampling unit: fixed-benchmark performance, performance
on a target population, original items, people, sessions, or independent runs.
Record sampling/recruitment, repeated observations, pairs, clusters, exclusions,
and missing-data policy. Avoid treating rotations or repeated outputs from the
same item as independent new cases.

Use the decision rules and formulas in [metrics.md](references/metrics.md).
Choose uncertainty methods for the design. Use Wilson intervals only for a
simple independent binary sampling model. Preserve pairs and clusters in
resampling. If the assumptions cannot be justified, state the uncertainty
analysis is not established rather than attaching a routine interval.

Keep holdout data separate from development. Record contamination and selective
reporting risks. Do not tune the system or acceptance threshold on the test set.

## Execute only the supported checks

1. **Task performance:** score against checkable outcomes using a defined
   grading procedure. Record denominators and failed/unparseable responses.
   Attach justified uncertainty when making a sampling-based claim.
2. **Robustness:** verify that a proposed transformation preserves the required
   answer before using it. Option rotation, whitespace changes, and paraphrases
   can change meaning in some tasks. Name the tested transformations and keep
   cyclic rotations distinct from all permutations.
3. **Behavior and correctness:** distinguish underlying-answer changes from
   correctness changes. Two different wrong answers count for the former only.
   Equal aggregate accuracy can coexist with complete per-item instability.
4. **Run consistency:** define the number of repeats, decoding configuration,
   seed policy, and event counted as a flip. Report the repeat budget with the
   rate; more repeats change the event's probability.
5. **Calibration:** require matched predicted probabilities and observed
   outcomes. State binary/top-label/multiclass definitions and baseline. Report
   proper scores and reliability diagnostics; Brier score alone is not a pure
   calibration measure. Name ECE bins and estimator limitations.
6. **Claim reproduction:** rerun the documented inputs/code where possible;
   distinguish historical artifacts, regenerated results, and independent
   replication. Preserve disagreements and failed reproductions. Never change
   analysis choices merely to match a published headline.

For each executed check, retain input hashes, code/environment versions, exact
commands, relevant settings, raw outputs, exclusions, and analysis output.
Pin determinism where feasible; do not guarantee bit identity from seeds alone.
Classify reproduction as exact, tolerance-based, or statistical, with a defined
comparison rule.

## Assess the stated decision

- **Ship:** all mandatory checks for the declared use and thresholds are
  supported by measured evidence under justified assumptions. State scope,
  critical failure gates, and what remains untested.
- **Caution:** evidence is incomplete or supports use only with specific limits.
  Name missing measurements, uncertain assumptions, and the next useful test.
- **Not-ready:** a measured load-bearing criterion fails, or the proposed use
  requires evidence that is currently unavailable. Explain which of those two
  reasons applies; missing evidence must not be described as a measured failure.

Do not convert a small accuracy drift into an equivalence or invariance claim.
Do not equate a demo, an AI-assisted assessment, marketplace review, or passing
unit tests with independent validation or production certification.

Deliver a short scorecard: decision and version; evidence status per check;
measurements with denominators and justified uncertainty; assumptions and
limits; decision against predeclared thresholds; and the smallest next action.
If no new run was possible, label the output **audit plan — not a completed
measurement** and show each proposed measurement as **not measured**. Keep
clearly labeled descriptive calculations from supplied records separate.

For a compact deliverable, use [the report template](templates/report.md).
For a synthetic supplied-data comparison that separates accuracy drift from
correctness changes, see [the paired example](references/paired-example.md).
