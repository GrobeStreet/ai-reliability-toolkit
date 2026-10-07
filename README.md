# AI Reliability Toolkit

A Claude plugin that turns Claude into a rigorous, honesty-first auditor of AI outputs and statistical claims.

Most people *produce* AI output. This plugin lets Claude *verify* it — the way a careful scientist would — and return a verdict you can defend.

## What it does

When you ask whether an AI output, model, feature, benchmark, or a statistical/scientific claim is reliable, trustworthy, or ready to ship, the plugin runs a structured audit and returns a **Ship / Caution / Not-ready** verdict backed by numbers and uncertainty — never a bare assertion.

The audit covers:

- **Accuracy with confidence intervals** — Wilson intervals for rates, bootstrap for everything else. No point estimate without its uncertainty.
- **Robustness** — does the answer survive meaning-preserving perturbations (paraphrase, case, whitespace, option-order shuffle)?
- **Consistency** — does it give the same answer run to run?
- **Calibration** — does stated confidence match observed correctness (Brier, ECE)? Overconfidence is flagged.
- **Reproducibility** — for papers and benchmarks: re-derive the result, check the analysis choices, and record a provenance ledger instead of taking the number on faith.

The governing principle is **measure, never assert**: a demo is not production, and a point estimate is not proof.

## Installation

Add this repository as a plugin in Claude Code / Claude Desktop (Settings → Plugins → install from a Git repository), pointing at:

```
https://github.com/GrobeStreet/ai-reliability-toolkit
```

Once installed, the `ai-reliability-audit` skill loads automatically whenever a request matches (see below).

## How to use it

Just ask, in plain language:

- "Is this model output reliable enough to ship?"
- "Stress-test this classifier for me."
- "Can I trust this benchmark result?"
- "Audit this paper's main claim — does it reproduce?"
- "Run a reliability audit on this feature."

Claude loads the audit method and walks the evaluation, ending in an honest scorecard.

## What's inside

- **Skill: AI Reliability Audit** (`skills/ai-reliability-audit/SKILL.md`) — the method Claude follows, with the detailed statistics (confidence intervals, calibration, perturbation taxonomy, minimum-N tables) in `references/metrics.md`, loaded on demand.

## Going further

This plugin runs the method by hand or in lightweight scripts, which is ideal for a single output or a small test set. For **automated, repeatable evaluation at scale** — a drop-in Python harness that computes the intervals, runs the full perturbation suite, measures consistency and calibration, and emits a self-contained HTML scorecard across providers — see the **AI Reliability Test Kit**:

https://digitalvaultcourses.gumroad.com/l/ai-reliability-test-kit

## Author

Built by Bobby Morong (RCV Labs) — reproducibility-first diligence for AI and statistical claims.

## License

MIT
