# Worked example: evidence is missing

This is a synthetic behavior example, not a measurement or customer case.

**Request:** "Our support bot is 95% accurate and ready to ship. We have a few
screenshots but no labeled test set, probability outputs, or runnable endpoint.
Can you certify it?"

**Expected response:**

Audit plan — not a completed measurement.

| Check | Status | Finding |
|---|---|---|
| Accuracy | Not measured | No labeled outcomes, denominator, or scoring rule |
| Robustness | Not measured | No original/perturbed outputs were executed |
| Repeat consistency | Not measured | No repeated outputs |
| Empirical calibration | Not measured | No matched probabilities and outcomes |
| Reproduction | Not measured | Screenshots do not establish a reproducible run |
| Readiness criteria | Missing | Intended users, harm severity, and tolerances unspecified |

**Decision:** Caution. The claim is unverified. No accuracy estimate, interval,
or calibration score can be computed from the supplied evidence. This does not
show the bot is inaccurate; it shows that readiness has not been established.

**Next action:** Define the intended use and failure gates, obtain a small
representative labeled set under a declared sampling design, freeze the
system version and grading policy, and run the supported checks within the
authorized budget. Report the actual outcomes and justified uncertainty.
