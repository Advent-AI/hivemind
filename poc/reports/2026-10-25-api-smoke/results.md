# Isolated API smoke: passed; 10x acceleration is not established

All 36 live requests returned schema-valid responses with usage and the requested pinned model. There were no retries or unknown-usage outcomes. All 122 pre-existing database files and sidecars have identical before/after SHA-256 hashes; no additional database files appeared under `poc/data`. New archives, raw responses, accounting and source snapshots are confined to this test directory. Nothing was merged or activated in production.

This tests ordinary API concurrency, **not OpenAI's asynchronous Batch API**. The [registered plan](../../../docs/research/2026-10-25-api-smoke/plan.md) links the official API, model and pricing documentation. The actual Batch API supports the selected OpenAI model, but its 24-hour completion window is not a seconds-level speed guarantee, and it does not serve Jev.

## Every sample

Two fixed stored requests per provider, three samples, two fresh serial controls and one fresh two-worker arm per sample. Order rotates. Each arm has its own empty archive. Four complete request hashes were reproduced using current builders before any paid request. Speed ratio is the mean of the two serial times divided by the concurrent time, separately for each sample.

| Stage | Sample | Serial A, seconds | Serial B, seconds | Concurrent, seconds | Ratio |
|---|---:|---:|---:|---:|---:|
| Extraction | 1 | 50.767 | 31.772 | 42.399 | 0.97x |
| Extraction | 2 | 43.613 | 41.151 | 37.198 | 1.14x |
| Extraction | 3 | 42.306 | 42.968 | 39.440 | 1.08x |
| Jev | 1 | 1.066 | 1.399 | 0.695 | 1.77x |
| Jev | 2 | 1.598 | 1.043 | 0.462 | 2.86x |
| Jev | 3 | 1.869 | 1.151 | 2.006 | 0.75x |

Median of sample ratios: **1.08x extraction; 1.77x Jev**. One extraction is much larger than the other, limiting the overlap benefit. These two-request measurements do not predict whole-day throughput. A concurrent sample was slower for each provider; no consistent speed guarantee follows.

Token-based Standard list-price estimate: **$0.041837**. The guard's deliberately conservative usage charge is **$0.127629**, below the **$1.50** cap; this is not a provider invoice. The guard reserves the cost before dispatch and retains unresolved reservations. Exactly 18 OpenAI and 18 Jev calls ran; returned models were `gpt-6-luna` and `jev-1.14.0`.

## Answer variation and its limits

- The two serial controls agreed on all **27/27 Jev categorical comparisons**. Concurrent versus either serial control agreed on **26/27**. These are repeated comparisons of nine choice questions, not 27 independent cases.
- The difference was sample 2, call 577, `rel__v4`: a candidate about Compute & Networking revenue versus a gross-margin thesis. The answer moved from `different` to `same_matter_different_quantity` (0.51 versus 0.47). The identical request hash rules out a changed prompt or stale context in this provider test. This alone does not establish that concurrency caused the sampling difference.
- Code trace: `views/jev_matching.py:213` selects only `same_quantity_or_event` for its first identity branch; the later branch selects `same_quantity_other_period`. Neither observed label selects either branch. `same_matter_different_quantity` appears elsewhere in `src` only in its criterion definition. The raw label changes the recorded explanation, not those branch conditions. This is a code trace, not an end-to-end ledger equivalence claim.
- Membership probabilities varied by at most 0.01 and remained 0.01–0.02, below the existing 0.5 threshold. This sample does not exercise successful group joins.
- The nonempty extraction returned **6–9 candidates, 10–15 evidence items and 1–3 group declarations** across the nine fresh calls. Serial controls already differ. The other extraction was empty in all nine calls. Raw counts or exact text equality cannot serve as the semantic acceptance standard.

The selected Jev calls also do not exercise positive merge, replacement or group-join decisions. Existing golds were not changed or scored against unrelated fresh IDs. A small end-to-end comparison with meaningful positive cases remains necessary before expanding the run or merging.

## Verification and safety fixes

- Full suite: **152 passed**, including nine new accounting/cancellation checks with real temporary SQLite storage.
- Five scratch mutants failed the intended assertions: omit in-flight cost, release unknown usage, dispatch after cancellation, defer a later worker's failure, and incorrect cost units. Full tracebacks are in `mutants-final-v2.json`.
- Read-only review found two race windows before live execution: cancellation between reservation and dispatch, and a later worker's validation failure blocked behind an earlier result. Both were corrected and re-reviewed; follow-up review (local artifact: `../../../docs/research/2026-10-25-api-smoke/code-review-2.txt`) found no serious issue.
- Preflight ran against three isolated copies. Refusal counts match the preceding preflight; 250 matching records were judged with no refusals or skipped records, and all 148 enum checks were present. The older extraction refusals remain visible in `preflight.txt`.
- `summary.json` is generated by `poc/concurrency_study/summarize.py`; `manifest.json`, `run.log`, `protected-before.json` and the per-arm archives retain the measured inputs and results. Raw databases remain local and ignored by Git.

## Reasoning refresh

Read the PRDs in their required order, 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 00. Universe, classification, Config and dispatch behavior are unchanged. Extraction receives unchanged full requests. The library's ordering, grouping, matching and write contracts are unchanged because this smoke does not write product records. Final verdict, pull and human review are not exercised or changed. The system overview's serial-equivalence requirement remains the gate for a later ingestion test. No new inconsistency caused by this slice required a page/PRD edit; D173 and CURRENT_STATE record the experimental boundary and next task.
