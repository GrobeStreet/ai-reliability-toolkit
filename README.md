# AI Reliability Toolkit

A Claude-oriented audit procedure for AI outputs, benchmark results, and
statistical claims. It helps an agent define a decision, inspect the evidence,
and execute supported measurements when data and tools are available.

**This repository contains instructions and statistical reference notes, not
an automated evaluation harness or an independent certification service.**

## Use

Load `skills/ai-reliability-audit/SKILL.md` in a compatible skill/plugin host.
The plugin manifest is under `.claude-plugin/`. Installation interfaces differ
by host; use your host's documented skill or repository-plugin installation.

Example requests:
- "Plan a reliability audit for this classifier; we have no labeled data yet."
- "Compare these paired model results and explain the uncertainty."
- "Check whether this benchmark claim can be reproduced."
- "Assess this feature against our declared failure threshold."

The method separates **measured**, **source-inspected**, **reported by others**,
**proposed**, **not measured**, and **not applicable** evidence. Without data
or execution tools it produces an audit plan, not fabricated test results.

## What it covers

- Decision-specific scope, thresholds, sampling units, and holdout boundaries.
- Performance with uncertainty justified by the sampling design.
- Declared robustness transformations and repeat consistency.
- Calibration only when matched outcome labels are available.
- Reproducibility records and explicit failed or incomplete reproduction.
- Ship / Caution / Not-ready decisions tied to evidence and the intended use.

The detailed formulas and limitations are in the skill's
`references/metrics.md`. In particular, answer flips and correctness flips are
different, and a small accuracy drift does not establish equivalence.

## Worked example

See [examples/insufficient-evidence.md](examples/insufficient-evidence.md)
for the expected response when a user supplies a claim without usable data.
This is a synthetic example, not a client engagement or independent study.

## Separate software

[Eval Invariance Engine](https://github.com/GrobeStreet/eval-invariance-engine)
is a separate Python diagnostic for paired correctness under cyclic option
rotations. Its version, inputs, limitations and test results must be inspected
separately; installing this skill does not install or validate that package.

## Author and license

Bobby Morong (RCV Labs). MIT. AI assistance in authoring is not independent
review, and use of this method does not establish production readiness.

## Marketplace preparation

A single-skill Agensi submission draft, included-file manifest, and offline
packaging check are under [submission/](submission/agensi-listing.md).
The skill includes a paired-results example and report template. Preparation
does not mean the listing is submitted, approved, or tested through Agensi.
