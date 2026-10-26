# Clickable Idea card and analyst TLDR — D186

The default local API uses `poc-v26-idea`: the original two requests for decomposition/mapping are unchanged, followed by an isolated `idea-summary-v1` call. The final call only returns `{"summary": "..."}` and cannot change selected theses, claims or graph relations. The same model/provider and reasoning effort are retained. The card opens analysis on click, Enter or Space; the separate action button is gone. The full summary is first in the drawer.

## Evidence and scope

- Frozen current example: `Nvidia will beat earning next quarter`, 2026-08-15, ten selected theses. Offline replay proves both original requests are identical and every chosen ID, part, claim, relation and evaluation is unchanged. Final context contains only those ten theses' dated states.
- The three old summaries recite library judgement labels. All three isolated summaries lead with a clear discretionary take, identify the demand/earnings gap and retain the difference between annual expectations and a quarterly surprise. They are still generic in places; one says “judged neutral.” This small example is not broad analyst-quality or mapping acceptance.
- Final-call input: 862 system characters, 14,588 payload characters and 3,683 measured prompt tokens. The original mapping remains 1,439 + 4,927 characters / 2,010 prompt tokens. The extra input is the chosen theses' actual conditions and reasoning, previously absent.
- Added-call latencies: 2.0, 2.2, 2.7 seconds; median 2.2 seconds. Added-call estimated costs: $0.000411, $0.000407, $0.000409. These are configured-rate estimates, not an invoice.
- Six final comparison calls cost $0.002499; twelve earlier development calls cost $0.006871. The live browser added only one new summary call: 3,683 input / 83 output tokens, 2.3 seconds, estimated $0.000410. The two original calls replayed from cache. Service archive increased from two to three rows; source ledgers did not change.
- Three protected source database hashes still equal `docs/research/2026-10-26-library-ui/baseline.json`.

## Why the summary is separate

Both combined-prompt development arms are retained, not enabled. The first omitted the total-revenue driver from the chosen set in 3/3 samples; the second mislabelled total revenue as a direct earnings match in 1/3 samples. Rich assessment text and claim uncertainty were changing relevance decisions. Rather than keep tuning the mapping prompt, the final design leaves it untouched and gives the already-fixed selection to a summary-only call. The JSON schema cannot express a selection change.

## Verification

154 product Python tests, 33 UI tests, ten UI mutation checks, lint and formatting pass. The missing-summary-call mutant fails the three-call assertion; the future-state mutant fails the real historical Neutral/Bearish assertion. Preflight on scratch copies reports 754 extraction answers, 250 matching records and 159 enum checks; historical extraction refusals are unchanged and not an Idea measurement.

Browser checks: click card, Enter, Space, animated close, focus restored to card, drag without opening, no separate button, summary first in drawer, current composite retained, cached resubmission. A close click sent while the drawer was still sliding did not land; waiting for the visible transition to finish verifies the normal close path. No product change was made for that automation timing.

An initial `pytest -q` accidentally discovered five retired experiment copies under reports and failed collection on removed `ingestion_groups`; the product suite is `pytest tests -q`, which passes. No experiment was restored or changed to make collection pass.

Artifacts: `isolated-summary/` holds exact requests, all six raw answers and the fixed selection; `live-response.json` is the browser's actual response. `card-preview.png` and `analysis-preview.png` show the final UI. Nothing was committed, pushed or deployed.
