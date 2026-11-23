# How large is the gap? Result of the census over everything the new system kept in the fresh week (D507), 2026-11-15

Design: `CLASS-CENSUS-DESIGN.md` (version 2, frozen before any reader). First readers: `codex-class-part1..6.jsonl`,
`claude-class-part1..6.jsonl`. Candidates and the instrument's check: `class_candidates.py`, `candidates-first.txt`,
`class-candidates.json`. The fresh pair: `*-class-settle-*.jsonl`. Tally: `tally_class.py`, `tally-class.txt`; the one hand merge:
`class-merges.json`. The run: the new system's stored fresh-week draw of D489 (567 kept statements, seven questions, 37 judgements).
Cost: $0; nothing was sent to a model and nothing changed in the system.

## The size, as this reading found it

| | |
|---|---|
| kept statements read against the seven questions (each by both families, all seven questions marked) | 567 |
| links the system made (a judge is shown exactly these) | 196 |
| candidates: listed for a question by a first reader and not linked to it | 63 (17 by both families, 16 Codex only, 30 Claude only) |
| **confirmed missing** (both fresh readers, shown everything the judge had and the article: in the article, not shown, bears) | **5 statements: 3 fact-and-question pairs, in 3 of the 7 questions** |
| open (the fresh readers differ) | 23 candidate statement-and-question pairs (not 23 distinct facts: some repeat one fact) |
| dropped (both: does not bear, or both: already shown) | 35 |

**The confirmed count is a minimum found by this reading, not a complete census, and one week of seven questions gives no general
rate.** A fact neither first reader listed is not found. The 23 open pairs are uncertainty, not an upper bound on what is missing.
Links and missing facts are different units: three beside 196 does not show the gap to be small.

## The three confirmed missing facts (each read by hand in the stored request)

1. **Supply commitments (v2; its last answer: the top band, $200 billion or more).** The CEO said NVIDIA would double the number of
   chips it sells next year (2027): three statements from three articles, one fact (the merge and its reason are in
   `class-merges.json`). Two were linked to no question, one to the Vera Rubin question. The request holds the CFO's 70% outlook and a
   conditional "could double if supply allowed", not this forecast. The readers: twice the chips needs more secured supply; the top
   band more likely to hold. Chip sales are not a figure for purchase commitments: the bearing is by a step of reasoning.
2. **Approval of Blackwell sales to China (v3; its last answer: still open).** "Washington has not said whether the card may be shipped
   to China at all": that the RTX Pro 5500's exemption is industry executives' reading, not a U.S. position. Linked to the RTX Pro
   5500 question only. The request holds the executives' expectation, not Washington's silence. The readers: the U.S. half is
   unsettled even for this chip; "yes" less likely. The statement is about the RTX Pro 5500 and the question about Blackwell sales
   more broadly: its bearing is an inference, not a ruling on Blackwell exports.
3. **MIIT's approval of RTX Pro 5500 purchases (v7; its last answer: yes).** "In September 2025, Beijing told firms to stop buying
   Nvidia's RTX Pro 6000D." Read at article 163, six articles before this question opened at 169, and linked to the export question.
   The request holds no earlier stop order. The readers: a precedent on a sibling chip from the same authority; "yes" less certain.
   **This one bears against the answer the judgement gave.**

By kind: two were linked to another question while the question they also bear on was open; one was read before its question
existed and was already linked to another question, so the later-linking step did not reconsider it (see the correction below).

## The open band (23)

- 13: one fresh reader says the fact bears and the other that it does not (the per-gigawatt figures and a per-gigawatt cost estimate
  under the credit-support question; Micron's capacity and memory tightness under supply commitments; Huawei's and Alibaba's chips, a
  scholar's view of China's chip shortage, a state dinner and a spokesperson's remark under the RTX Pro 5500 question; two others).
- 10: they differ on whether the judge already had it. Five of these are the 70% growth outlook repeated by other outlets, which the
  supply-commitments request does state (read by hand in D506): delivered in substance, though left open by the rule.
- The two families' bars differ throughout: of the 63 candidates, the fresh Codex reader marked 53 as bearing and the fresh Claude
  reader 34. Where "an analyst reasons onward" stops is not settled by these readers.

## The earlier finding did not hold with a second pair

D506's finding (the per-gigawatt revenue opportunity under the credit-support question) stands under D506's rule: four readers
confirmed it there. Under this census's rule it is an open lead: the first readers listed it again (one statement by both families,
one by Claude) and a new fresh pair split. One says it sizes the supported capacity; the other that a product's revenue per gigawatt
is not a credit-support amount and that the top answer already holds, a reason that sets aside the design's own test (a fact that
changes how likely an answer is counts). Both results are on record. The split is a reading problem, not two settled standards.

## The instrument's own check

- Of the 196 links the system made, the first readers also list: Codex 126 (64%), Claude 108 (55%). About four in ten of the
  statements the system files under a question are not answer-bearing for a reader family: the system files more widely than these
  readers would. This census did not examine whether such statements belong there.
- Who listed the candidates first: of the 17 both families listed, 1 is confirmed, 4 open, 12 dropped; of 30 Claude only, 3
  confirmed, 13 open, 14 dropped; of 16 Codex only, 1 confirmed, 6 open, 9 dropped.
- One reader session printed the folder's file names on entering it (names only; it reports opening nothing else).

## What this result may and may not be said to show

- Shown, for one stored week and draw: at least three kept facts that both fresh readers say bear on a question never reached its
  judge, in three of seven questions; one of them bears against the judgement's answer; twenty-three more candidates are undecided
  between two reader bars.
- Not shown: that any judgement would have changed (not measured); a rate for the system in general; that the gap is isolated (a
  low confirmed count is a minimum); anything about production or about which system carries forward.

## Council (thread mx, round 21; `clean-arch/step1-unfiled-2026-11-08/council/mx-challenge-20.md`, `mx-codex-21.md`): consensus, with corrections

- Stated as: three confirmed fact-and-question pairs in three questions, from five statements; 23 unresolved candidate pairs; a
  minimum. Corrected in this page: the 23 are pairs, not distinct facts; "small beside 196 links" compared different units and is
  removed; the D506 finding is not disproved, both results stand; the bearing of two of the three facts is by inference and is said
  so.
- The families' split is not handed to Alex as a ruler to set: one fresh reader's reason ("the top answer already holds") departs
  from the written test.
- **The one test to offer, his to open (it sends):** the effect on the judgement, on the strongest case only. The RTX Pro 5500
  question answered "yes" without the earlier report that Beijing had told firms to stop buying the related RTX Pro 6000D. The
  stored last request of that question re-sent as stored and re-sent with that one stored statement added in the judge's own
  format (its id, source, date and quote), three sends each on the same day: six judge calls, about one cent at the published rates
  (the stored call: 5,628 tokens in, 2,514 out), ceiling $0.25. The control is rebuilt byte for byte first; what counts as a
  meaningful loss of confidence in "yes" is written before the send (citing the new fact is not enough); all six answers are read
  blind to their condition. A difference inside the control's own variation, or none, is inconclusive, not proof of no effect; a
  directional difference in three sends is a bounded signal on this request, not the size of the effect on the product.

## Lessons

1. **Count in one unit.** The draft set three facts beside 196 links and 23 pairs beside them as if they measured one thing.
2. **A finding is the output of its rule and its readers.** The same fact was confirmed by four readers under one rule and split by
   two under the next; neither erases the other, and a result that rests on two fresh readers says so.
3. **Check a reader's reason against the written test.** One fresh reader dropped facts because the answer was already on its top
   band, though the brief counts a change in likelihood; a mark given for a reason outside the test is noted as such.
4. **After a census, test the effect where the product is judged, on the strongest case first.** Six calls on the one fact that
   opposes a stored answer decide more than a wider reading of all 23.

## Correction (2026-11-15, found by the reflection council "my", round 3, and checked in the stored run)

This page said that nothing in the new system files an earlier statement under a question opened later, and that a judge is shown
the statements linked "when their articles were read". Both are wrong as written. **The new system has a later-linking step**
(`clean-arch/step3/library.py`, `link_later`): when a question opens, the system checks the earlier groups of statements (a
statement with its repeats) **whose original statement arrived without a question** (a batch that fails twice stays pending and is
tried again; none stayed pending in this run). In this week: seven calls, 516 group-and-question checks, 2 linked (both to the Vera
Rubin question); of the 196 links, 194 were made when the statement's article was read and 2 by this step. **A group whose original
arrived under another question is excluded, even if the new question also needs it:** e379 (the group `163:e3` in the stored
library) arrived linked to the export question at article 163, so it was not among the 166 checked when the RTX Pro 5500 question
opened at article 169. The counts and findings of this page do not change; the description of the cause does: the
case is "linked elsewhere and so never reconsidered", not "nothing looks back". Production does not link an earlier record to a
question opened later (D456: none of 3,225 links in six draws points back; a later article that repeats the fact can still deliver
it; `clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md`, which found that in those draws, on the graded
questions of the July window, such unlinked facts cost no final answer).
