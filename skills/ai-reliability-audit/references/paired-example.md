# Worked example: equal accuracy, changed correctness

This is a synthetic demonstration calculated from supplied records. It is not
a live model evaluation, customer result, or independent validation study.

## Request

Compare these two conditions. Can I call the model invariant because accuracy
did not change? IDs define the same original item across conditions. No model
outputs, grading logs, population sampling design, or release criteria exist.

| Item | Original correct | Rotated correct |
|---|---|---|
| q1 | true | false |
| q2 | false | true |
| q3 | true | true |
| q4 | false | false |

## Example response

**Caution — descriptive comparison only.** Both conditions score 2/4 (50%),
so observed accuracy drift is 0 percentage points. Correctness changes on
q1 and q2: 2/4 original items (50%). Equal accuracy therefore hides item-level
correctness changes. These records do not establish equivalence or invariance.

| Check | Evidence status | Finding |
|---|---|---|
| Accuracy per condition | Calculated from supplied data | Original 2/4; rotated 2/4 |
| Accuracy drift | Calculated from supplied data | 0 percentage points |
| Correctness changes | Calculated from supplied data | 2/4 original items; 50% |
| Underlying-answer changes | Not measured | Actual answer texts/identities absent |
| Calibration | Not measured | Matched probabilities and outcomes absent |
| Transformation validity | Not measured | Original questions/options absent |
| Upstream model run and labels | Reported by others | No independent execution or grading check |
| Population uncertainty | Not established | Four synthetic records and no sampling design |
| Release decision | Not assessed | Intended use and acceptance thresholds absent |

The paired structure has four original items, not eight independent cases.
Do not attach an independent-binomial interval to the eight condition rows.
The smallest next action is to inspect questions, options, answers, and grading
for these four items, establish whether rotation preserves the required answer,
and define the use-specific acceptance criteria before collecting a holdout.

## Optional software reproduction

The separate Eval Invariance Engine 0.4.0 contains this fixture and a generated
report. It is not installed by this skill. In a deliberately installed source
checkout of engine commit `27da19d9206e76b94e6f9bb4d48aba44b70dc019`, run:

```bash
invariance-check report examples/paired_results.json --json
```

The committed fixture has deliberately shuffled rows. Its report records
`n_items=4`, `max_drift=0.0`, and `correctness_flip_rate=0.5`. Its exploratory
paired-item bootstrap uses 2,000 draws, seed 0, and yields a drift interval
of [0.0, 0.75]. This illustrates a computation on synthetic data; it does not
justify population inference or a production decision. The illustrative
3-percentage-point drift threshold is not a user's release criterion.

Source: https://github.com/GrobeStreet/eval-invariance-engine/tree/27da19d9206e76b94e6f9bb4d48aba44b70dc019/examples
