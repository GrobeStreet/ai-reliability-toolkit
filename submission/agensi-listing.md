# AI Benchmark Audit: Robustness & Reproducibility

**Draft preview — not published.**

Suggested price: **$19 one-time**. Version 0.3.0.

## Summary

Check paired benchmark results for hidden correctness changes, reproduce an offline example, and get an evidence-based report. Includes a Python calculator, input validation, and a reusable audit template.

## Description

A benchmark score can stay unchanged while individual items switch between correct and incorrect. This skill helps your agent find those changes and explain what the evidence actually supports.

Supply item IDs, condition names and correctness labels. The included offline calculator validates complete pairing, reports accuracy by condition, measures accuracy drift and correctness changes, and checks supplied expected metrics. It records input hashes and execution details so the arithmetic can be checked again.

For reproducibility, an included deterministic toy benchmark generates predictions, grades them and reproduces its expected results. The guided protocol then identifies what would be needed to reproduce a real model benchmark: data, grading, model version, environment and execution records.

Your output is a concise scorecard with measured or calculated findings, missing evidence, assumptions and the smallest useful next check. Without sufficient inputs or execution tools, the agent returns a descriptive review or audit plan.

## Included

- A focused benchmark-audit workflow and statistical reference
- Standalone Python paired-result calculator with strict input validation
- A runnable toy benchmark plus supplied-data example and reference outputs
- A reusable report template and reproduction checklist

## Compatibility

Use with an Agensi-connected agent that loads bundled text resources. Python 3.9+ and local code execution are required for the included calculations and toy reproduction. No pip dependencies, model API key or network calls are needed by the scripts. Without code execution, the skill provides a descriptive review or audit plan. Installation through Agensi is pending verification.

## Limits

This is not an automatic rerun of arbitrary model benchmarks, independent scientific validation, a calibration measurement from unlabeled data, or a production-readiness certificate. Correctness changes do not reveal underlying-answer changes. The calculator does not infer population confidence intervals. Real model reproduction requires separate data and execution access. Agent and platform charges are separate from this purchase.

## See it in action

**Request:** Reproduce the included toy benchmark, compare original and rotated results, and tell me whether equal accuracy proves invariance. No release thresholds have been provided.

**Result:** The offline toy always selects option A for two arithmetic questions. After swapping each question’s two options, accuracy remains 1/2 (50%) in both conditions, giving 0 percentage points of accuracy drift. Both original items change correctness: 2/2 (100%). The calculation matches the supplied expected metrics. Equal aggregate accuracy therefore hides item-level correctness changes; it does not establish invariance or equivalence.

The toy’s generation and grading are inspectable in the bundled source, and the scripts reproduce the author-generated reference calculation. This is synthetic execution, not a real-model study or independent replication. No population uncertainty or readiness decision is established. For a real benchmark, the next action is to inspect transformation validity, answer labels, grading and run provenance, then define intended-use thresholds. The general correctness-only calculator does not measure underlying-answer changes or calibration.

## Permissions

- Read user-supplied benchmark records
- Run the two supplied Python scripts in temporary files, with standard input/output
- Write the requested analysis report if the host supports file output

## Public source

Public MIT-licensed source is available on GitHub. Purchase is for convenient delivery through Agensi; the listing does not claim exclusive ownership of the public method.

https://github.com/GrobeStreet/ai-reliability-toolkit
