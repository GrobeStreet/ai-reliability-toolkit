# Agensi listing draft — AI Reliability Audit

Status: prepared for creator review; not submitted or approved by Agensi.

## Listing fields

- Name: AI Reliability Audit
- Creator: Bobby Morong (RCV Labs)
- Suggested launch price: Free pilot. This is a recommendation, not a live price.
- Suggested category: Research & Analysis; verify available categories in the form.
- Summary: Audit AI evaluation claims, compare paired results, and identify missing evidence. Get a scoped scorecard that separates measured findings from proposed tests, with uncertainty matched to the study design.
- Tags: ai, evaluation, reliability, statistics, reproducibility
- Keywords: benchmark audit, paired comparison, correctness flips, calibration, uncertainty
- Use cases: review benchmark claims; compare paired outcomes; plan missing measurements; assess a declared release gate

## Description

Turn an AI reliability question into a clear evidence scorecard. Define the
decision and acceptance thresholds, inspect available records, calculate
supported comparisons, and identify the smallest useful next test.

The method distinguishes measured results, source inspection, reported claims,
and missing evidence. It checks whether uncertainty calculations respect paired
items and clusters, whether robustness transformations preserve the required
answer, and whether labels exist for accuracy and calibration claims.

You receive findings with denominators, assumptions, limitations, a decision
against your stated criteria when evidence supports one, and a next action.
Without usable data or execution tools, you receive an audit plan. Equal
aggregate accuracy does not become an unsupported invariance claim.

Included: audit instructions, statistical reference, synthetic paired-results
example, report template, and MIT license. The public source remains available.
This is an instruction-based procedure, not an installed test runner,
independent scientific review, certification, or guarantee of readiness.

## Compatibility note

Requires an agent that can load the complete SKILL.md and its bundled text
references. Reading and audit planning need no API key or external service.
Dataset calculations require the host's code/data tools; model evaluations need
separately configured execution tools, access and budget. No runtime scripts or
dependencies are bundled. Local validation used Python 3.13 for the supporting
calculations; installation through Agensi and other agent hosts is not tested.
Do not advertise universal compatibility from format compliance alone.

## See it in action

Request: "Two conditions each scored 50%. Is the model invariant? The paired
correctness records are q1 true/false, q2 false/true, q3 true/true, q4 false/false.
We have no model outputs or release criteria."

Result: Caution — descriptive comparison only. Original accuracy is 2/4 (50%)
and rotated accuracy is 2/4 (50%), producing 0 percentage points of accuracy
drift. Correctness changes on 2/4 original items (50%). Equal accuracy hides
item-level changes and does not establish equivalence or invariance.
Underlying-answer changes and calibration are not measured because answers,
probabilities, and matched outcomes are missing. The upstream model run and
labels are not independently verified. There are four original items, not eight
independent cases, and no justified population uncertainty or release verdict.
Next: inspect the questions, answers, grading, and transformation validity;
then define use-specific thresholds before collecting a holdout. This is a
synthetic worked example calculated from supplied records, not a client result.

## Submission route and open items

Agensi's website submission form is https://www.agensi.io/dashboard/submit .
Its docs also describe an Agensi connector with creator_status and submit_skill
preview/confirmation tools. That connector is not exposed in this session.
Creator account, Creator Mode, display-name availability, current terms, and
actual marketplace compatibility remain unverified. Paid publication also
requires payout setup; no payout changes or terms acceptance are included here.

Use the files listed in `package-manifest.json`, flattened to its destination
paths, as one package. Keep this listing draft and build script outside it.
Run `python3 submission/build_package.py > /tmp/agensi-staging.json` from
the repository root with Python 3.9 or newer. The build script validates
relative references and produces a text-file staging JSON, not a direct API request or
ZIP. A web upload requires creating a ZIP from these exact selected files.

The existing source is public and MIT-licensed. A free pilot can test discovery
and useful runs without implying that marketplace protection makes this source
exclusive. Consider a paid edition only after there is additional differentiated
value and observed demand. No revenue or traffic forecast is established here.

Documentation checked November 16, 2026:

- https://www.agensi.io/docs/packaging
- https://www.agensi.io/docs/submit-on-the-website
- https://www.agensi.io/docs/submit-from-your-agent

## Validation record

The selected package contains one SKILL.md and four supporting text files
(about 19 KB total). Structure and reference checks passed. Deliberate unsafe
paths, duplicate destinations, absent references, and missing frontmatter were
rejected. A fresh-context supplied-records scenario preserved the distinction
between aggregate accuracy and correctness changes and did not infer readiness.
The separate engine reproduced the worked-example values locally. These are
packaging and behavioral checks, not Agensi approval or independent validation.
