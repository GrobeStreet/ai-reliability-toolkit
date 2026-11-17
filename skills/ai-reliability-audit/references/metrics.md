# Reliability metrics and design limits

Use these notes to choose an analysis. They do not make an unsupported
sampling model valid. Separate observed facts from statistical inference.

## 1. Estimand, unit, and provenance

For a fixed set of deterministic benchmark outputs, the observed accuracy is
an exact summary of that set. An interval for a broader population requires a
sampling model. A stochastic-run claim requires repeated runs and a defined
run-generating process.

Declare the independent unit. Several rotations of one question, several
sessions from one person, or repeated outputs from the same item are dependent.
Preserve item/person clusters and A/B pairing throughout analysis.
State missing-response and parsing policies before inspecting results.
Retain item IDs; reject duplicated or incomplete comparison cells rather than
silently pairing rows by their order.

## 2. Independent binary rates

For N independent binary outcomes, k successes, p_hat = k/N, a Wilson score
interval with z = 1.96 is:

```text
center = (p_hat + z*z/(2*N)) / (1 + z*z/N)
half = z * sqrt(p_hat*(1-p_hat)/N + z*z/(4*N*N)) / (1 + z*z/N)
interval = [center-half, center+half]
```

N must be positive. Example: 46/50 = 92%, Wilson 95% interval approximately
80.8–97.0%. State both the denominator and the independence/population
assumptions. Do not count four rotations of 50 questions as 200 independent
questions. A binomial interval does not account for label errors, biased
sampling, grader errors, or distribution shift.

For dependent observations, choose a design-aware method, such as resampling
whole original items. If there are few clusters, acknowledge that nominal
coverage may be poor. No routine interval certifies reliability.

## 3. Comparisons and bootstrap

For two systems tested on the same items, estimate the paired difference.
Report the effect, its interval, and a design-appropriate comparison, such as
McNemar's test for paired binary outcomes when its conditions fit.
Overlap of two marginal confidence intervals is not a paired test.

A paired item bootstrap samples original item IDs with replacement and carries
all systems/conditions/repeats for each sampled ID together. Recompute the
statistic per resample. For clustered people or sessions, resample the actual
independent cluster instead. Use stratification or a different method when
the design requires it.

Report the method, number of resamples (normally at least 2,000), seed, target,
and assumptions. Percentile bootstrap is not automatically appropriate for
every metric. A max-over-conditions statistic, boundary estimate, small sample,
selection procedure, or dependent series may require a different treatment.
More resamples reduce Monte Carlo error, not design bias.

A point estimate below a tolerance is not evidence of equivalence. Establish
equivalence only with a prespecified tolerance and valid design/uncertainty
procedure. Otherwise report a descriptive threshold comparison.

## 4. Precision and power planning

Do not claim an MDE from a formula using only N and a single accuracy estimate.
Power planning requires a design, significance level, desired power, target
effect, and relevant variance parameters. Paired binary designs additionally
depend on discordant pairs.

For estimation, specify the desired interval width and use a validated
design-specific calculation or simulation. Distinguish a rough planning
approximation from an achieved precision guarantee. If the required inputs
or implementation are absent, label power/MDE **not calculated**.

## 5. Robustness and repeat consistency

Check that every transformation preserves the intended answer. Reordering
options with references such as "all of the above" may change the task.
Whitespace changes can alter code or structured inputs. Paraphrases need
semantic checks. Limit conclusions to the tested transformations.

Define metrics explicitly:
- **Answer flip rate:** fraction of original items whose canonical predicted
  answer changes at least once across the declared conditions.
- **Correctness flip rate:** fraction whose correct/incorrect status changes
  at least once. Wrong-to-wrong answer changes are invisible here.
- **Accuracy drift:** maximum minus minimum condition-level accuracy.

A model may have zero accuracy drift and 100% correctness flips.
Boolean correctness data cannot recover underlying-answer flips.
Resample whole items for sampling-based uncertainty; keep any repeat budget
and stochastic-run variability distinct from question-sampling variability.
Do not infer memorization or contamination from order sensitivity alone.

## 6. Calibration requires observed outcomes

Match probabilities to a clearly defined event and observed labels.
Without labels, report confidence distributions or stability, not empirical
calibration. Consistency is not correctness.

For a binary event, Brier score is mean((p-y)^2), y in {0,1}. A constant
0.5 forecast has score 0.25 for this binary definition. Also compare an
appropriate prevalence-based baseline. For multiclass probabilities,
state the chosen normalization; the common summed squared error is not
the same metric as binary correctness-confidence scoring.

Brier score and log loss reflect more than calibration, so interpret them
with reliability diagnostics rather than calling either a pure calibration
score. A reliability diagram compares mean probability with observed event
frequency in bins. State bin definitions, counts, and uncertainty assumptions.

ECE is a binned, sample-weighted average of absolute confidence/outcome gaps.
State bin edges, weighting, and whether it is top-label or classwise. ECE can
change with the binning and sample size; examine sensitivity before making a
strong claim. Sparse bins and label noise limit conclusions.

## 7. Reproducibility and readiness

Record data/model revisions, input/output hashes, code commit, command,
environment, precision/device, seeds, decoding settings, and exceptions.
Distinguish:
- exact artifact verification;
- reruns within declared numeric tolerances;
- repeated stochastic results under a specified distribution/comparison rule;
- external independent replication.

Seeds alone do not ensure bit-identical GPU or hosted-model results. A
historical artifact cannot retroactively gain execution provenance from later
version pins.

Tie readiness to the use case's prespecified thresholds and failure severity.
Missing checks remain **not measured**. A reported run is not an independently
verified run, and source inspection is not runtime execution.
