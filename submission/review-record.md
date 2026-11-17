# Version 0.3.0 pre-submission review

Prepared November 16, 2026. This records local checks and AI-assisted reviews,
not independent scientific validation or marketplace approval.

1. **Technical review:** examined scripts, input validation, scientific limits,
   examples and isolated execution. Found a floating-point threshold-boundary
   defect: 5/10 versus 8/10 produced 0.30000000000000004 and incorrectly failed
   a 0.3 inclusive maximum. Fixed by calculating spread from integer success
   counts before dividing; added a regression test. Also corrected the earlier
   PR comment about using Caution when readiness criteria are absent.
2. **Buyer/promise review:** checked the paid listing against actual package
   functionality, source availability, permission disclosures and compatibility.
   No material local-functionality mismatch found. The outstanding launch check
   is actual delivery through Agensi and a connected-agent execution.
3. **Fresh-context use:** ran both scripts unchanged from temporary files. The
   toy reproduced 1/2 accuracy in both conditions with 2/2 correctness changes.
   A separate four-item supplied-records task yielded 2/4 in both conditions,
   0 drift, and 2/4 flips. Against supplied maxima of 0.03 drift and 0.10 flips,
   the report distinguished the passing drift check from the failing flip
   check, preserved source/label limitations and identified the next check.

Automated local suite: 13 tests, covering invalid data, incomplete/duplicate
pairs, repeated JSON keys, nonfinite values, expected-result mismatch, criterion
boundaries, multi-condition event counting, stable row hashes, reference output
agreement, package structure and isolated execution. Both scripts parse with
Python 3.9 grammar and import standard-library modules only. Maximum script
size is under the platform's 20 KB guideline.

Price, title, summary and demonstration are stored once in listing.json;
the readable preview is rendered from those fields. Required field lengths
and full demonstration length were checked. Seller pages were checked for
pricing, fee/payout mechanics, refunds, allowed links, licensing and packaging.
No performance, customer, review, demand or revenue claims were fabricated.

Remaining: creator sign-in, actual platform preview, payout onboarding, source
disclosure acceptance, name availability, upload/scan, review outcome and a
delivered-agent run. The user requested a preview before submission. No emails
or marketplace publication are part of these completed local checks.
