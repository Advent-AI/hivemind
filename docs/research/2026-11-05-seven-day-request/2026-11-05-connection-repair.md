# Split extraction connection repair

> **Update, 2026-11-05 (D375 on main):** Alex confirmed that each item must read the latest committed library, including earlier same-day writes. A and B share that snapshot; the next item waits for the preceding write. References below to a day-start A/B snapshot and the proposed summed-probability matcher are historical investigation, not the current design. The current experiment design is in `fresh-context-poc-design.md`. The experiment is not accepted or running; recovery, subject identity and source/metadata accuracy remain to be verified.

Alex asked to fix the connection completely and asked what is being tested. Two separate actual calls read the same item and day-start library: A proposes a new viewpoint and its own evidence, B files evidence to existing viewpoints. The real matcher compares A with the live ledger at writing time; the real writer stores each outcome; the next day uses the committed state. Score A's topic-opening behavior and B's helpful evidence separately, and trace the joined result. No single count of records is an efficacy score. The signed frozen gold and historical scores do not change; golden-v5 has only two articles in this seven-day window. Semantic same-topic labels must be reviewed against each exact snapshot; unlabelled new topics are not automatically wrong.

## Stored-data census and mechanisms

Full stopped snapshot: 89 articles with handovers; A 49 questions and 395 raw evidence, B 221 raw evidence; 34 questions written, every one has blank date and no rungs, and none receives ladder judgement. Code in `split_seven_day_poc.build_handover` explicitly sets all three to empty even where the model/author supplied a check date. This is our wiring error, not a model failure. A metadata-only request did not receive A's `how_and_when_to_check`, so it could not carry the information forward.

The bridge dropped 11 quotes for failing byte-for-byte source matching. Five are source-equivalent after canonical punctuation/case normalization. For all five, `extraction.repair_quote` finds a source passage whose normalized text equals the model's entire quote. Four further passages are repairable under the older fuzzy rule but do not match in normalized form; three cannot be repaired. Example 1293 repair adds a trailing 'In', so do not silently use fuzzy repair here. Eight B items have no shown existing-question home; a human must determine which are genuinely helpful, and A may have independently retained the same matter. Among retained evidence, 28 same-normalized-quote groups are a lead, not proof of duplicate matters.

One added `identity_check` refused the actual matcher’s merge at seq 1293. The candidate asks whether Amazon uses NVIDIA NVLink Fusion, and v97 tracks NVIDIA's NVLink Fusion customer deployments. Jev judged `part_of`; the POC rejected because candidate subject AMZN differs from v97's NVDA. In a replay of the saved answer through the real existing matcher check, there are no refusals and it merges to v97. This is a cross-company connected matter, not proof all cross-company merges are valid. Remove the POC-specific categorical veto and use the actual matcher; review the merge trace, never hardcode importance or force a cross-subject merge.

A duplicate question v72/v73: actual candidate was compared to v72, and Jev selected `same_quantity_or_event` with 0.43 and assigned 0.29 to `part_of`. Both relations have the same merge action; code separately requires 0.5 in either class and opens another question. On all 3,130 recorded candidate-comparison responses, only this case has a top choice of either same/part with neither individually at 0.5 but their sum at least 0.5. A second comparison (v74 vs v70) crosses the combined probability but its top choice is a different period; do not fold different periods into the same action by code. Proposed POC-only option: when the top choice is same or part, sum their model probabilities to evaluate the existing 0.5 merge threshold; retain existing identity conflict checks and default production behavior. Replaying stored answers can prove the observed duplication flips and count every other changed comparison; it does not establish general false-positive rate or overall quality.

## Events and values

| Event/state | Behavior |
| --- | --- |
| Day start | A and B see the same actual prior-day library, including topics written in preceding days. |
| A or B reply | Preserve full request/answer and original source; source quote is copied exactly or, only when normalized whole passages match, restored to the exact source passage. Unverifiable passages remain dropped with a reason; they do not erase the question or other evidence. |
| A returns a question | Metadata call reads its question, `how_and_when_to_check` and article. `year`, exact `due_day`, date basis and rungs are optional; no required missing field becomes a refusal or fabricated value. Preserve approximate date as the analyst's actual words, not an exact date. |
| Date/ladder absent | Record question and evidence; no made-up judgment. Existing daily judgment runs only when a usable ladder exists. |
| Date/ladder present | Preserve values with their source/analyst basis; allow ladder judgment. An analyst check date does not automatically settle/close a new topic merely by arriving; resolution requires evidence. The POC keeps these topics open until a verified resolution workflow exists. |
| A/B overlap | Preserve distinct summaries and links. Exact shared source is not an independent source. Do not collapse different claims because they share a quote; identity of meaning remains a model/reader decision. |
| Matching, failure, resume | Matching uses the actual existing matcher plus the opt-in aggregated-action rule; no extra categorical issuer gate. Persist raw outputs and each matching record. Refused or failed work is visible and cannot be silently counted as a pass. Resume only if source, prompt, snapshot and configuration identity match. |
| Day completes | Only actually written subjects enter the next day's input. A later article carrying new evidence remains eligible for that topic. |

| Value | Writer/source | Readers |
| --- | --- | --- |
| Question, evidence and rationale | A answer; source-verified exact quotes | actual matcher, writer, next-day A/B input and trace |
| Existing-topic evidence | B answer and same start-of-day snapshot | actual matcher/writer; downstream evidence reader |
| Subject | Metadata model; dynamic research subject identity if not in prior lookup | matcher, writer, day-start reader; no research significance list |
| Optional date, basis, year, ladder | Metadata model reads A and source; blank when not known | actual writer, day-start prompt, judging and POC close policy |
| Match output | actual Jev, optional summed merge-action probability | existing code checks, writer and future day |
| Same-source provenance | source ID, each evidence record and raw answer | judge/reader; same-quote does not imply independent source or automatically same matter |

## Proof before a new paid run

1. Run the three stored decisive cases on copied ledgers at zero cost: seq 1293's saved decision no longer refuses; 1211's saved probabilities merge v73 into v72 under opt-in only; 1207's source-equivalent quote is restored as exact full source. Replay all 11 dropped quotes, all 3,130 relation responses and all recorded dates/rungs; record flipped counts and unchanged semantic uncertainty. Negative mutations must fail, and product default stays unchanged.
2. Fake metadata/source input proves known date, unknown date, analyst check date and unavailable/available rungs travel correctly; no empty value blocks a valid question. The real writer must preserve a new question and evidence and show it to the next day's A and B. Prove a no-date/no-ladder question remains, and a valid ladder is judged using a fake external model. Test known dates don't close unresolved experimental topics on passing date.
3. Review code/design independently. Preflight the stored archive and the actual changed metadata request at zero cost; only the affected new metadata request changes a model call. Re-send the minimum affected source-backed model calls and read actual question, original article, metadata, links and outputs. Replay the first day on the real path before any seven-day measurement. Do not claim gold coverage for unreviewed articles.

## Independent review correction

The prior proposal to sum same-topic and part-of probabilities is withdrawn: `part_of` is symmetric in the model schema while the writing direction matters, and periods can require different outcomes. The one saved crossing is not enough to prove a general merge rule. Topic equivalence still needs a separate general design; do not lower or reweight scores around that case.

The source count is 11 refused quotes: five normalize exactly to the complete source passage and are restored by the adapter; of the other six, three produce a broader fuzzy-repair candidate and three do not. The two sets of five/four/three in the first paragraph were a counting error. The three broader fuzzy candidates and three unverifiable ones are not silently rewritten by this change. A source excerpt must be returned verbatim, with model summary and attribution retained and the original answer stored. This fix solves the five punctuation-equivalent refusals, not the other six.

Removing the cross-issuer veto allows the saved seq 1293 answer to reach the existing real matcher without a refusal; it does not prove every cross-company merge correct. Same-source overlapping A/B summaries remain separate; absent an explicit same-claim relation, a downstream judge may overcount them. Dynamic object identity also requires that future article lookup actually includes those questions; the observed next-day result for two theme questions is not proof for dynamic company questions. Re-run after the adapter, subject lookup, same-source treatment, and crash semantics are fully designed and tested; do not call partial fixes full acceptance.
