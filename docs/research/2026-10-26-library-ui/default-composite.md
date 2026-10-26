# D188: default composite score on Idea cards

Alex requested that the composite chart become a default Idea-card requirement. The two stored Idea mappings have identical dates: one has a matching manual trial, one does not. The existing writer compares exact idea text and date against a single build-time configuration. The API returns no composite plan. The current three-thesis example has usable histories but no matching configuration. This is a missing general response contract, not missing chart data.

## Decision and scope

Retain D185's equal-weight mean of distinct signed drivers and its current-basket historical interpretation. Retain D186's separation from matching: the existing final assessment call now returns summary plus a composite plan; the original decomposition/mapping requests and selected IDs stay unchanged. No fourth call, ledger writes, new research groups, ingestion change or manual query registry.

The model selects one representative per underlying economic driver, from the chosen theses only. Revenue forecasts at total/segment/product levels for one demand channel must not multiply its weight; repeated capex estimates/financing for the same demand backdrop do not become independent drivers. Select by relevance and coverage, not the currently favourable score. It may exclude an irrelevant, overlapping, temporally unhelpful or directionally ambiguous thesis, with a reason. Every chosen thesis must occur exactly once as representative or exclusion. The model identifies whether the first or last rung of each representative supports the user's claim. Full ordered ladder conditions make this meaningful without relying on numeric UI orientation. No free-form weights; all available representatives weigh equally.

Code validates the partition, identities, endpoint enum and text before returning versioned `reading.composite`. Code supplies the date and immutable question, not the model. The frontend converts the endpoint to its existing displayed-score orientation and computes the same D185 historical mean. For binary ladders the two ends map to +2/-2 support. Missing assessments do not become zero. Empty plans show axes with no line and an unavailable score. No coverage needs no model call. Legacy responses remain readable; explicit historical manual trials remain a compatibility path, not the default.

## State × event

| State/event | Result and date |
|---|---|
| Pending / failed request | Existing progress / error card; no fabricated chart |
| Covered Idea, final call succeeds | Validated plan plus summary; code pins request as_of; chart on default card |
| No chosen or no directionally useful thesis | Empty plan with exclusions; no invented zero |
| Missing assessment on a past day | Average available representatives only, with coverage; no future values |
| All assessments missing | Null score, no line |
| Overlap or negative idea | One representative per driver; explicit supporting endpoint |
| Invalid IDs, duplicates, omitted chosen thesis, invalid endpoint | Reject at writer; no silent repaired plan |
| Model/transport failure or English retry | Existing error/retry path; count all calls; do not silently use manual plan |
| Replay or range change | Same fixed response basket applied to historical states; not a historical record of old baskets |
| New idea/day/selection; concurrent requests | New exact archived request and request-owned plan; no cross-request reuse |
| Legacy response/config | Existing summary and explicitly configured manual trial stay compatible |

## Value × reader / new path × old checks

| Value | Source, owner and readers |
|---|---|
| Ordered ladder conditions | Stored immutable rungs → new final-call context only; old summary context unchanged |
| Representatives/endpoints/exclusions | Final model JSON → writer's closed schema and complete-partition validator |
| Date/question/method/version | Code → API and frontend validator; never model-invented |
| Numeric score/coverage/history | One shared frontend calculator → card, replay chart and detail contribution table |
| New prompt/default config | Versioned new files → API/Docker; provider/model unchanged; old files immutable |

Preserve existing schema, English, unknown-ID, claim, archive and historical-date checks. Add complete-partition and endpoint validation. UI tests use real three-thesis and ten-thesis responses and the full collected histories; assert original 0 → 0.5 → 0 calculation, the new +0.5 case, negative-direction inversion, empty plans, missing assessment, out-of-date identity and no exact-query gate. Mutants must catch double counting, orientation reversal and future leakage. Browser verifies the real default request and detail breakdown.

## Verification and prompt audit

The old final call can only return summary. Its payload omits ordered ladder ends; an automatic direction cannot be recovered reliably from a single current label. New output adds a bounded plan rather than another call. Remove old per-part narrative from the new context because it is repeated assessment prose; retain typed coverage and selected dated state reasons. New prompt length and measured tokens are reported against the old prompt. The output budget rises only for the new version to hold explicit decisions, under a $0.10 experiment reservation.

Before paid work, run preflight on copies. Freeze the two actual contexts and a labelled negative-claim variant using the same three selected theses; run three fresh old-summary controls and three new-plan samples per context. Inspect all samples for grounded summaries, overlap, relevance and direction; preserve failures and do not tune a scored acceptance set. This is a focused development check, not broad investment-model acceptance. First two model requests are checked byte-identical. No source database changes; full suite once on final code; refresh docs by D22 then docs/check.py last.

## Schema correction before activation

The first three v27 candidate samples produced one duplicate disposition: v3 appeared in both drivers and excluded. All ten selected identities were correctly present in the context; the raw reason referred to its repeated appearance across part lists. Two separate output lists let the same identity be written twice. The writer refused the third sample and the run stopped after six calls ($0.003670 estimated); v27 is not enabled.

The corrected v28 schema has one required property per chosen thesis ID. Its value is either a driver or an exclusion. Unknown and missing keys fail JSON validation; the writer converts each property into exactly one API entry. This removes the whole duplicate/missing-identity class at the representation boundary. Prompt v3 removes the now-code-owned uniqueness sentence; portfolio logic stays the same. The total spending reservation remains $0.10; at most 24 comparison calls across the stopped arm and corrected arm, plus the bounded live smoke, fit within it.

## Polarity correction

The keyed-schema arm completed all 18 calls. It eliminated duplicate/missing IDs in all nine candidate answers, but one of three negative-claim answers selected the high-capex end while its own reason said that end opposed a revenue miss. v28 is not enabled. The same prompt asked the model to combine the user's direction with the economic effect, and one answer omitted the inversion. The final v29 contract separates the named outcome, whether the user predicts higher/lower, and the driver end that raises that outcome. Code performs the lower-claim inversion exactly once. No extra call or numerical model weight is added. Selection remains discretionary and its observed variation is reported separately. The spending ceiling remains $0.10 across these attempts.

The outcome-format arm still selected the low-revenue endpoint for two positive earnings samples. The final candidate replaces ambiguous first/last output words with the supplied endpoint position ID, sends only the two endpoint conditions, and enables low reasoning for the final assessment only. The first two calls keep their original settings. Output allowance is 4,000 tokens for reasoning plus the structured response; the total experiment spending ceiling remains $0.10. This is a measured configuration tradeoff, not a silent provider/model switch.

## Final contract and reasoning refresh

Final default: `poc-v30-idea`, `idea-summary-v5`, low reasoning for the third call only. The model writes the named outcome, user direction, and one required disposition per chosen identity; representatives copy the explicit position of one supplied endpoint. Code validates it, converts lower claims once, and binds canonical questions and as_of. Numeric calculation remains the shared UI function. Earlier candidate schemas remain historical configurations, not defaults.

D22 order reviewed: universe, classification and dispatch unchanged; Config records the new version/settings; extraction and thesis-library writes/matching are untouched; final verdict, pull mode and review pool are untouched; system glossary names the new read-only score. Existing page/PRD examples and acceptance rules do not change. The inconsistent current statements were the default config, summary-only response and manual-only chart; their owners and linked summaries now describe the default response capability. Results and limits are in the report. No foundation group-association rule changed.
