# Missing identity fields in split matching: isolated investigation

2026-11-05. Scope: candidate-to-question matching only. No change to extraction, evidence filing, the ruler or the stopped seven-day run.

## Observed class

In the stopped split run snapshot, 46 candidates were checked; none supplied `measure`. Seventeen were merged, all on a `part_of` relation; no collision judge was invoked for these unkeyed candidates. All 17 candidate texts and the exact existing-question texts shown in the saved Jev requests were read. Eleven events concerned FY2028 revenue candidates merged into FY2027 questions; they include repeated reports. The others include overlapping capital spending, acquisitions and event milestones, so opening every candidate is not a sound repair. Seq 1209: FY2028 company total was merged into FY2027 Data Center segment, despite both texts and the year being visible to Jev. `part_of` permits either direction; the code treats it as new inside old. The existing D190/D248/D258 collision judge is only offered peers with equal typed measures; this split path has no measure.

## Candidate design to test

When the candidate lacks a measure and the configured collision judge is enabled, send the existing judge the candidate and each existing question that Jev proposes for merger (`same_quantity_or_event` or `part_of`) above its existing threshold. The judge applies D248's same-outcome / analyst tracking test. Only its `same_question` permits a merge. A different question stays new; an unkeyed later-period answer stays new because the existing successor code cannot establish its direction without the identity fields. This does not reject a question for missing a date or a measure and does not infer significance in code. No collision setting preserves the existing Jev-only path. No prompt changes are proposed.

The scope is a real architecture change to matching: it broadens where the existing judge is used. A true duplicate may exist outside Jev's proposed matches; this design does not claim to fix that class. The same stored candidate can be proposed against several old questions, so all proposed matches are reviewed, not merely the first one. The answer must include each shown ID exactly once; an incomplete answer must not silently open or merge anything.

## State × event

| State/event | Action and write | Time basis |
| --- | --- | --- |
| No candidate, or no proposed same/part match | Existing path; no new judge request | Original item and ledger snapshot |
| Unkeyed candidate, proposed matches, judge returns all answers | Merge to an open peer the judge calls the same; otherwise open new; evidence follows existing writer | Original item and latest committed pre-item ledger |
| Judge refuses, transport fails, answer incomplete or repeats an ID | Refuse the matching operation; do not produce a decision or write | Same item on any retry |
| Candidate has typed measure, or judge not configured | Existing behavior | Unchanged |
| Restart, changed config or another writer | The run owns snapshot and retry; this change writes no separate state | Caller supplies its snapshot and configuration |

## Value × reader and checks

| Value | Writer and reader | Constraint |
| --- | --- | --- |
| Candidate and peer texts | Existing handover/store → collision judge | Same evidence and question visible to matcher, no invented key |
| Judge relations | Existing model call → matcher → `matching.check` → writer | All proposed peer IDs exactly once; same-question may merge, others do not |
| Match decision and evidence links | Existing matcher → writer → next item | Same existing shapes; no new storage fields |
| Dates and measures | Existing source / preparation → matcher | Missing fields never cause a rejection; existing typed path unchanged |

New path passes existing model schema, match target list, open-question and write checks; the split path also permits no ladder/date. D258's component merge is retained when the judge says the existing question covers it. D167 prohibits a case-specific list or a code judgement of importance. D248's question identity is the same outcome and separate analyst tracking, not a blanket fiscal-year rule.

## Proof sequence

Run `scripts/preflight.py` on the stored frozen control. First send four archived real candidate/target pairs to the unchanged collision request: the decisive error, a broad/subset spending example, a population variant, and an event milestone. This asks whether the already existing judge can make the relevant distinction; it cannot establish overall quality. Then replay every affected stored merge with recorded or faked judge outcomes to prove routing and count affected cases; compare same, distinct, other period, omitted answer, and typed/Jev-only controls. A fresh chronological slice is needed to see new questions alter later snapshots and prevent duplicates; stored independent rows cannot demonstrate that. No live run, production configuration or frozen gold changes during this work.

## Probe finding: direction is also ambiguous in the existing judge prompt

The four first probes returned distinct for 1209 and 1227, and same for 1243 and 1250. A second probe on the actual multi-peer request for all 17 stored merges returned a wrong new destination on 1251: the candidate asks for the share of revenue from all financed customers, and v32 asks if one named customer's financing arrangement is signed. The judge called them the same because the existing question is an instance of the broader candidate. Its own reason states the reverse direction. For 1250 the two draws also disagree about whether two aggregate spending populations are one question; this case needs semantic review, and one draw is not a stability score.

The collision-v2 request calls a single instance under a plan the same question without stating which of CANDIDATE and THESIS is the broader plan. Under D258, the *candidate* part is filed under the existing question, not vice versa. A trial `collision-v3` will replace this phrase to identify the direction and state that one existing instance alone does not establish that a broader candidate is covered. It makes no industry or company rule. Compare characters and token counts; first probe 1251 and controls, then send the same historical 17 multi-peer requests to v3. No default configuration changes. This is a proposed improvement, not an accepted outcome.

The v3 system prompt has 1,235 characters against v2's 1,179. On exact 1209 text its provider-reported complete input was 852 tokens against 846 for v2; that includes the unchanged schema and user message. Five one-peer probes and 17 multi-peer calls returned: 1209 distinct; 1251 distinct from both possible old homes; 1243 merged into the original transaction. Sixteen of the 17 old merge events became `new` in their original independent contexts and one stayed merged. This is not a count of topics or an accuracy score: the saved contexts contain none of the new writes, and a model decides their semantic correctness. 1250 changed between v2 draws; v3's distinction of total and data-center spending was read against both questions.

## Chronological two-item check

The remaining uncertainty is whether the first new FY2028 question prevents an identical second candidate being opened. Use the actual Aug 28 68-question seed ledger, saved A candidates and source-verified A passages for items 1209 and 1213, actual Jev + collision-v3 matching and actual writer, in a separate new ledger. Load the latest committed snapshot between items. This is a targeted matching/writer check, not an extraction or B test, and skips the other intervening articles; it cannot represent the complete seven-day run. It requires new model calls because the second item's question library changes. It must show the first new question and whether the second candidate finds that exact written question. The prompt, configuration, seed data and saved source requests must be fixed before sending.

Result: the seed and input file SHA-256 values matched the original manifest. Item 1209 created v70 for FY2028 total revenue; item 1213 saw v70 in its 69-question snapshot and the actual matcher merged its candidate into v70. The actual writer stored eight evidence records on v70. Both rounds succeeded. One sample of two selected articles is not a stability estimate and does not replay intervening articles, extraction, B, or daily judgment. Artifacts: `poc/data/matching-identity-two-items-2026-11-05/` in this worktree.

Offline verification: 226 passed and 61 skipped in the full suite; after a test assertion was clarified, 41 matching and frozen-ruler tests passed. The original matching code, substituted in a scratch copy, failed the decisive new-question assertion because it wrote no new question. The original frozen-control preflight replayed 243 extraction answers and 170 matching records; two matching records lacking the archive were skipped. Its two archived schema-refusal rows, seven source refusals and five duplicate-source merges are historical, and it does not exercise the split prompts or prove collision-v3. The separate v3 requests were checked against the real collision schema.

The working tree carries copies of the seven-day experiment's pre-existing uncommitted `config.py`, `model.py`, `matching.py`, `round.py`, `writing.py`, `judging.py` and `poc-v118.json` so the tests use that actual runtime. They are baseline copies, not part of this matching fix. No experiment or main worktree files, running ledgers, frozen gold, or default configurations were modified. The fix still needs a deliberately configured successor run before it can affect that seven-day diagnostic; the paused run cannot be resumed under modified runtime hashes.
