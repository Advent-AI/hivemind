# NAVER admission: one-source comparison

The changed extraction prompt retained the announced NAVER expansion in **3/3** fresh samples; the original prompt did so in **2/3**. This supports the change on this source and frozen context, not a general extraction acceptance. The default remains v23/T6-v10.

For example, the treatment asks whether the planned GAK Sejong expansion reaches 200 MW by December 31, 2028. Its evidence still calls this a plan. It does not claim that NVIDIA has received an order or recognized revenue.

## What changed

`role-v11.txt` starts from the business question, then distinguishes an annual metric from an announced milestone whose completion criterion contains a number. It removes the automatic numeric-question recipe. It contains no NAVER-specific names, quantities or dates. The system message shrank from 6,739 to 6,567 characters; measured extraction input fell from 7,121 to 7,074 tokens per call.

Only the system message differs between arms. The source, pre-NAVER library, category instructions, JSON schema, provider/model/settings, matching and writer are identical. The existing annual-metric horizon remains: replaying the previously failed 2028 capacity answer still rejects it. The test uses `poc-v24-admission-test.json`, which selects v11 only for T6; other categories and the default configuration are unchanged.

## Every sample

| Sample | Material project information retained under the right question | Proposed / retained questions | Retained evidence | Dropped items | Extraction input / output tokens | Round seconds |
|---|---|---|---|---|---|---|
| Control 1 | Yes | 2 / 1 | 2 | 1 | 7,121 / 2,053 | 20.01 |
| Treatment 1 | Yes | 1 / 1 | 1 | 0 | 7,074 / 943 | 11.57 |
| Treatment 2 | Yes | 1 / 1 | 1 | 0 | 7,074 / 929 | 10.62 |
| Control 2 | Yes | 2 / 1 | 1 | 2 | 7,121 / 1,982 | 19.05 |
| Control 3 | No | 0 / 0 | 1 | 0 | 7,121 / 529 | 7.01 |
| Treatment 3 | Yes | 1 / 1 | 2 | 0 | 7,074 / 1,193 | 12.05 |

Controls 1 and 2 retained a valid project milestone but also proposed an annual 2028 capacity question. The unchanged horizon rule discarded that extra question; Control 2 also lost its solely linked evidence. Control 3 omitted the project question and 2028 deadline, attaching a platform-use statement to the existing Rubin production-shipment question instead. The original failure therefore is not deterministic, and its exact capacity-only output did not recur in these three controls.

All treatments retained the 200 MW target, 2028 deadline and source evidence under one valid project milestone. Each created a project group and membership separate from SK's project and Rubin production, without relying on a required name or group count. Treatment 3 also retained the funding statement as conditional: NAVER still needed to finalize financing, and NVIDIA's planned investment remained subject to closing conditions. No treatment asserted a completed order, delivery or revenue.

The assessment is an assistant's reading of the source and all six raw answers, not an independent judge or a statistical reliability estimate. Its labels and reasons are in assessments.json (local artifact: `../../../docs/research/2026-10-25-naver-admission/assessments.json`); samples.json (local artifact: `samples.json`) retains the raw outputs, accepted handovers and resulting records. summary.json (local artifact: `summary.json`) is generated from the preserved run and those explicit labels by summarize.py (local artifact: `../../../docs/research/2026-10-25-naver-admission/summarize.py`).

## Execution and isolation

- Normal sequential dispatch, extraction, matching and writing at sequence 22; six fresh ledgers and archives from the same frozen prefix. No daily judging or live concurrency comparison.
- 12 physical requests, no retries or unknown usage. Standard list-price estimate: **$0.009831**. Conservative guard accounting: **$0.031480**, under the registered $0.60 ceiling. These are different accounting methods, not two bills.
- All **124 protected databases** had unchanged hashes: 122 working files and two earlier experiment databases.
- Preflight over copied stored data judged 754 extraction answers and 250 matching records. Matching had zero refusals/skips; all 159 prompt enum checks passed. The historical schema-check mismatch on one Jev answer and existing extraction refusals were unchanged from the control, not newly introduced passes.
- **156 tests passed** in the experimental worktree; the separately published sequential branch also passed its **123 existing product/corpus tests**. The offline whole-harness check proved wiring using stored responses; it did not count toward the six live samples.
- A read-only code review found that the initial experiment fingerprint omitted transport/budget dependencies. Those files were added before live execution. A scratch mutation then refused the run before credentials or a budget journal were opened. The original review and proof are preserved.

The complete source, databases, request manifest, provider traces and budget journal stay in this dated local report directory; they are not copied into the working library. The prompt is a tested candidate, not promoted production behavior. Wider sources and repeated downstream usage remain unmeasured.
