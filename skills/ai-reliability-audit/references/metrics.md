# Reliability metrics — formulas, worked examples, and gotchas

Reference for the AI Reliability Audit skill. Use these to attach honest uncertainty to every reliability claim.

## 1. Confidence interval for a rate (accuracy, robustness, agreement)

A rate from N trials (k successes, p̂ = k/N) is an estimate, not the truth. Always report an interval.

### Wilson score interval (preferred for proportions)
More accurate than the normal ("Wald") interval, especially for small N or p̂ near 0 or 1 — the regime reliability claims live in.

For confidence level with z (z = 1.96 for 95%):

```
center = (p̂ + z²/(2N)) / (1 + z²/N)
half   = (z / (1 + z²/N)) * sqrt( p̂(1-p̂)/N + z²/(4N²) )
CI     = [center - half, center + half]
```

Worked example: 46/50 correct → p̂ = 0.92. Wilson 95% CI ≈ **[0.808, 0.970]**. Report "92% (95% CI 81–97%, N=50)," never a bare "92%."

Do **not** use the Wald interval (p̂ ± z·sqrt(p̂(1-p̂)/N)) for small N or extreme p̂ — it gives impossible bounds (>1 or <0) and overstates precision.

### Bootstrap (for anything that isn't a simple proportion)
For F1, RMSE, AUC, mean scores, or any statistic: resample the N cases with replacement B times (B ≥ 2000), recompute the statistic each time, and take the 2.5th and 97.5th percentiles as the 95% CI. Seed the resampler and report the seed.

## 2. Comparing two systems / claims

A higher point estimate is not a real difference. To call B better than A:

- For paired data (same cases through both), use **McNemar's test** on the discordant pairs, or a paired bootstrap of the difference. Report the CI of the *difference*; if it crosses 0, the difference is not established at that N.
- State the **minimum detectable effect (MDE)**: with N cases, you can reliably detect roughly an accuracy gap of ≈ 2·z·sqrt(p̂(1-p̂)/N). If the claimed improvement is smaller than the MDE, the test set is too small to support it — a finding, not a pass.

## 3. Minimum N (why small samples lie)

Rough N needed to estimate a ~90% accuracy to a given ±half-width (95% Wilson, p≈0.9):

| Target ± half-width | Approx N needed |
|---|---|
| ±10 pts | ~35 |
| ±5 pts  | ~140 |
| ±3 pts  | ~385 |
| ±2 pts  | ~865 |
| ±1 pt   | ~3,460 |

Implication: a "95% accurate" claim from 20 examples has a CI roughly [76%, 99%] — it cannot distinguish "excellent" from "mediocre." Flag any headline number whose N can't support the precision implied.

## 4. Robustness

- **Perturbation taxonomy** (meaning-preserving — the answer *should not* change):
  - lexical: case change, whitespace add/trim, punctuation, unicode look-alikes
  - surface: paraphrase, synonym swap, reformat (JSON ↔ prose ↔ markdown)
  - structural: reorder multiple-choice options, reorder independent list items, shuffle few-shot example order
  - distractor: add irrelevant but plausible context
- **Robustness rate** = fraction of cases whose verdict is unchanged across the perturbation set; attach a Wilson CI.
- The **option-order shuffle** is the single highest-yield probe for multiple-choice/classification: a large accuracy drop when only the order changes means the model is keying on position, so the headline accuracy is partly an artifact.

## 5. Consistency (run-to-run)

- Hold inputs fixed; vary only seed/sampling. Run R times (R ≥ 5).
- **Flip rate** = fraction of cases whose verdict is not identical across all R runs. Report it with a CI.
- A non-trivial flip rate means the reported accuracy is itself a random variable; average accuracy can look fine while individual decisions are unstable — a real defect for anything user-facing.

## 6. Calibration

Does confidence match correctness?

- **Brier score** = mean( (p_pred − outcome)² ) over cases, where p_pred is the model's stated probability and outcome ∈ {0,1}. Lower is better; 0.25 is the "always say 50%" baseline.
- **Expected Calibration Error (ECE)**: bin predictions by stated confidence (e.g. 10 bins), and within each bin compute |mean(confidence) − accuracy|; ECE is the sample-weighted average of those gaps.
- **Overconfidence signature**: high mean confidence, lower accuracy, ECE concentrated in the high-confidence bins. This is the failure that erodes user trust fastest — always call it out explicitly, not just as a number.
- A **reliability diagram** (stated confidence on x, observed accuracy on y, with the y=x diagonal) makes miscalibration visible at a glance.

## 7. Reproducibility ledger (for claims/papers/benchmarks)

Record, so the result is checkable by a third party:

- data: exact file/version/hash; code: commit/pin; seed(s); environment (library versions, thread count).
- Pin determinism where possible (e.g. single-threaded BLAS) so two runs are bit-identical; verify by hashing the output and report the hash.
- Document every deviation from the original method, and never tune the reproduction to force a match with the published number — report the honest gap and its likely cause.

## 8. Honesty rules (non-negotiable)

- Every rate ships with its N and interval.
- A difference inside the noise is reported as "not established at this N," not as an improvement.
- "Demo passed" ≠ "production ready." Say which was tested.
- Absence of ground truth limits the audit to consistency/calibration — state it; do not imply accuracy was measured when it wasn't.
