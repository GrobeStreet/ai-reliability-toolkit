# Reliability assessment: [system/claim and version]

**Scope:** [intended use, decision owner, target population]
**Mode:** [audit plan / descriptive supplied-data analysis / executed evaluation]
**Evidence available:** [inputs, provenance, labels, tools, unavailable evidence]
**Decision criteria:** [predeclared thresholds and critical-failure gates, or missing]

| Check | Evidence status | Measurement and denominator | Assumptions / limits |
|---|---|---|---|
| Task performance | [status] | [value, n, or not measured] | [grading and sampling] |
| Robustness | [status] | [transformation, pairs, failures] | [semantic validity] |
| Correctness / answer changes | [status] | [event definition and original-item n] | [distinguish events] |
| Calibration | [status] | [definition, score, n, or not measured] | [labels and probabilities] |
| Reproduction | [status] | [executed comparison, or not measured] | [historical vs regenerated vs independent] |

Use only measured, source-inspected, reported by others, proposed, not measured,
not applicable, or calculated from supplied data as applicable. Never leave
placeholder values that look like actual measurements. Add uncertainty only
when the sampling/assignment design and method justify it; name the sampling
unit, pair/cluster treatment, method, seed and resample budget when used.

**Decision:** [Ship / Caution / Not-ready], limited to [declared use/version].
Explain each mandatory criterion. Separate missing evidence from measured
failure. If criteria are absent, give descriptive findings without a readiness
verdict. An audit plan without measurements cannot earn Ship.

**Smallest next action:** [specific missing measurement or bounded fix]
**Reproduction record:** [input hashes, code/environment versions, commands,
settings, raw outputs, exclusions, and exact/tolerance/statistical rule]
