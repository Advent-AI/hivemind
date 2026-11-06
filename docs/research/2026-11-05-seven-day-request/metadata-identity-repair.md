# Preserve every A evidence item through record preparation

On 2026-11-05, the seven-day run stopped on item sequence 1207 after two completed items. The A answer proposed one question with 15 evidence passages. Record preparation returned metadata only for e1 and e9. This was a complete provider response (`finish_reason=stop`), not output truncation. The real model's continuation said it intentionally selected only passages directly related to the launch, dropping the 13 it considered background or context. The A call had already selected those passages, and record preparation's task is attribution, not a second significance filter. Raw request, provider response, answers and probe are preserved under the failed run and `metadata-probe-1207/`.

Census: in this new run one metadata answer covered all 3 requested IDs and the next covered 2 of 15; the first processed item had no new question and no metadata call. The previous 89 stored handovers have 49 candidates; the saved previous metadata calls met their earlier adapter contract. One failure in two metadata calls is a diagnostic, not a population rate. No source evidence is to be thrown away or assigned an invented tier merely because preparation omitted an ID. Separately, the existing source check still refuses a purported quotation that cannot be located in the article, and records the refusal; this repair does not change that contract.

## Contract and events

The A answer defines the complete candidate/evidence IDs. The preparation request asks for attribution and optional research fields for every supplied ID and does not select, omit, or rank them. The response is keyed by those exact IDs; each key is required in the structured schema, so the provider cannot return a seemingly valid partial array. Code compares the exact set, preserves each source passage, and refuses duplicate, missing or unknown identifiers. The response must still be read against the article; structural completeness does not prove the speaker, date or tier is correct. Question worth, supporting relevance and interpretation remain the original A call's decisions. Missing dates or optional ladders do not block a question.

| Event | State and action |
| --- | --- |
| No A questions | No preparation call; B and writer proceed. |
| A questions and evidence | Required schema keys correspond exactly to the A positions; the raw request and reply are saved. |
| Missing/unknown/invalid metadata or service failure | Stop visibly with raw A, B and provider response preserved; never substitute an attribution or discard A evidence. |
| Original two items already written | A successor experiment copies the stopped ledger and saved artifacts, records the exact parent run and runtime change, and retains completion records. It does not replay their writes. |
| Failed item | Verify its article, pre-item snapshot, A/B request bytes and provider responses; reuse exact A/B answers. Reissue only the changed record-preparation request, and preserve the original partial metadata under its own name. |
| Input, original A/B prompt or pre-item snapshot differs | Refuse reuse; retain parent run. Do not silently restart from a different state. |
| Writer committed before interruption | The ledger's completion marker decides; no duplicate write. |
| Later items | Read the preceding actual commit. A and B retain the same per-item snapshot; prompt and provider answer identity are pinned. |

Readers: candidate fields go to the actual matcher/writer and later question snapshot; evidence attribution and date go to the actual writer and judgement. The frozen gold and standard are unchanged. The only changed model task is preparation's obligation to describe each already-selected item; A and B prompts are unchanged.

Proof before another paid call: replay all 89 saved complete old answers through backward-compatible input normalization; reconstruct 1207 with a synthetic complete response and verify that all 15 A evidence reach the handover unchanged, plus B evidence. Mutate one missing or extra ID and show refusal. Compare the parent A/B requests and responses byte-for-byte with the fork's originals, and show the fork's ledger and completion records match the stopped parent before proceeding. Then re-send only item 1207's changed preparation request, inspect the raw response and source, and resume the successor experiment. Preserve and report the reader's existing 1 MB failure and the pilot's mixed-source-tier defects; the seven-day test remains diagnostic, not full production acceptance.

## Actual affected call

The original A and B wire requests, saved provider outputs, input article and pre-item library were checked against the current request builder; both requests are identical. Only record preparation was re-sent, in `poc/data/split-metadata-repair-1207-v1/`. It returned all 15 required evidence IDs. All 15 A passages and one B passage passed through the adapter with no drops. The saved partial original is not overwritten. System instruction length fell from 1,530 to 1,501 characters; the structured response gained one required key per A evidence. This is one real sample, not a reliability score.

A direct reading of the original article and all returned attributions found unresolved classification risk: e4 combines the journalist's framing and Charles Rose's recollection while the whole item receives `party_statement`; e6 and e7 include the journalist's comparative framing while the whole items receive `fact`. These are kept as trace findings, not silently corrected and not used to claim semantic accuracy. The candidate's approximate source-backed planned date is kept with its provenance; the model returned no ladder. The already recorded 1 MB reader limit and mixed actual/guidance item remain unresolved.
