# Why the clean system misses questions end to end: root causes (council loop, 2026-11-11)

Run with the `council-loop` skill. Alex, 2026-11-11, after Step 2 stopped (Step 2 log §17): "好考试下一步然后跑council review 结果找问题根因".
The next step named there: trace the clean system's end-to-end misses that no one has traced, since a miss traced to Step 2 is
what would reopen it.

## 0. Frame

- **Objective.** For every question the clean system gets wrong on the frozen judgement ruler in the seeded end-to-end test (D392,
  three draws, `clean-arch/e2e-2026-11-09/stage2-result.txt`), the mechanism and the step that owns it. Two misses are untraced:
  the China share question (q17) in draw 3 and the FY2028 revenue question (q22) in draw 2.
- **Pass line.** None: this is a diagnosis (AGENTS §1). What it must deliver per miss: the mechanism traced on the record, its
  owner, the cheapest proof, and whether it is the product's problem or the measurement's.
- **Reference system.** Production's frozen v108 run in the same hours (the control draws of D392).
- **Ruler.** The judgement ruler (AGENTS §7.1, piece 3): `gold-v1.json` sha256 `636c056d…`, scored by `score_judgement.py`; a numeric
  question agrees when the gold's range overlaps the band of the rung chosen at the window end, 2026-07-14.
- **Constraints.** Production, the judge and the ruler are frozen. Step 4's ladder step is another session's work: no edit to
  `clean-arch/step4-2026-11-10/`. No change to any step in this round: the round ends at causes.
- **Budget.** Stored data first, at no cost. Re-sends of saved judge requests at a few cents, each after an independent read.

## 1. Census (no model call)

| Question | Clean misses (of 3 draws) | Production misses (of 3) | Cause |
|---|---|---|---|
| Capital spending (q12) | 3 | 3 | traced before (D394): Step 1 does not write the cash-flow identity |
| Ohio guarantee (q23) | 2 | 2 | traced before (Step 1's open defect 1): the unsigned guarantee folded into an aggregate thesis |
| China share (q17) | 1 (draw 3) | 2 | untraced: this round |
| FY2028 revenue (q22) | 1 (draw 2) | 0 | untraced: this round |

Both untraced questions sit on a rung line. China: the line is 1% and the draws' estimates run from 0.5% to 3% (gold 1 to 8%).
FY2028: every draw anchors on the consensus of about $554 billion, $4 billion above the $550 billion line (gold $560 to $640
billion). The window-end rung differs between clean draws on 6 of 22 questions; on 4 the gold range covers both rungs, so only these
two cost a point. A judgement changes the previous rung in 11% of later judgements (8% in production).

The three draws replay offline, every judge request answered from its saved archive (239, 269 and 251 requests; `control-d{1,2,3}/`).

## 2. Mechanism, traced on the record

**China share, draw 3.** The report that China will let Alibaba, ByteDance and DeepSeek buy fewer than 200,000 H200s reached every
draw's request on 2026-07-08 (checked by text). Draws 1 and 2 moved from rung 5 to 4 that day and held 4; draw 3 held 5 to the end.
No H200 price is in any request, so nothing lets the judge turn the 200,000 chips into dollars against the 1% line (about $500
million of a market sized at about $50 billion). Found at no cost (`refusal_census.py`): draw 3's first answer that day was rung 4;
the frozen check refused it for naming the export-controls theme as a dependency, and the re-asked answer was rung 5. Over the six
draws the check refused and re-asked 65 judgements (clean 10, 16, 18; production 10, 5, 6), 42 of them for this one slip on this
question; the re-ask changed the rung 8 times, 5 on this question, and two of those changes held to a ruler miss (clean draw 3,
production draw 4). A Step 1 recall difference was also found and set aside: the $2.5 billion smuggling statement of 2026-07-14 was
written in draw 2 only; draw 1 lacks it and agrees, and draw 3's rung was set six days before it arrived.

**FY2028 revenue, draw 2.** On 2026-07-10 a Trefis line ("about 32% a year for the next few years") took the question to rung 3 in
clean draws 1 and 2 and production draw 4 (production draw 3 went to 5). Draw 1 came back to 2 on 07-13, draw 3 on 07-14, draw 2 never.
Draw 2's saved window-end answer also misreads its own figure ("$553 billion … still below the rung-2 boundary"). The question
depends on no other question, so the FY2027 conclusion is not shown to it; the hyperscaler-spending themes (2027 at $1 trillion or
more) are shown in every draw.

## 3. Council A (`council/a-claude.md`, `a-codex.md`, `b-challenge.md`, `b-codex.md`)

Both members, written apart, found the judge's choice at a boundary in both cases and differed on the proofs. Codex's first proofs
(the 07-14 China request with the smuggling item added by hand; the 07-10 FY2028 request with and without the Trefis line) were
withdrawn by Codex on challenge: one aims at an item that arrived after the rung was set, the other re-measures what the judge's
reasons already state. Codex's corrections to the reading rule were taken (refusals reported apart, outcomes not covered reported
as not decided, wording as a lead and not a rate).

## 4. Probe (`PROBE.md`, `resend.py`; 18 sends, $0.043)

Reviewed twice before the send (`council/sender-review-codex.md`: four serious findings, closed; `sender-review-r2-codex.md`: two
residual ones, closed by one rule, every file the probe writes is created new and each outcome is also printed to the log). Sent on
my reading after the second review.

| Case | Rungs | By the rule fixed beforehand |
|---|---|---|
| A. draw 3, China share, 07-08, the refused first request | 4, 5, 5 (all three refused again for the same slip) | the re-ask drew the more common answer: **the refusal is not shown to be the cause** |
| F. the same with the re-ask note | 4, 5, 5 | the note not shown to matter |
| B. draw 1, China share, 07-08 | 4, 4, 4 (one refused for the same slip) | draw 1's and draw 3's inputs that day differ in what they produce (a lead) |
| C. draw 3, China share, 07-14 | 4, 5, 5 | the window-end answer is itself open |
| D. draw 2, FY2028 revenue, 07-14 | 3, 3, 3 | with E, the two requests differ in what they produce (a lead) |
| E. draw 3, FY2028 revenue, 07-14 | 2, 2, 2 | |

**Regression of my own reading:** the refusal looked like the cause of the China miss; the sends refute that as stated.

**Traced after the sends, no cost.**
- China, draws 1 and 3 on 07-08: the export-controls theme shows "Yes" in all three draws; the Data Center dependency is rung 2 in
  both. Both previous conclusions are rung 5, but draw 3's already holds the frame "1% of about $50 billion is about $500 million; the
  evidence does not establish that level", and draw 3's rung-5 answers repeat it almost word for word. About eight evidence items
  differ each way.
- FY2028, draws 2 and 3 on 07-14: both previous conclusions are rung 3 with the same 32% frame. Draw 3's request holds, and draw 2's
  lacks, the second "41% in calendar 2027" record (draw 2's Step 1 filed it under the FY2027 question only), "roughly $1 trillion of
  Blackwell and Vera Rubin revenue visibility across 2026 and 2027", and five infrastructure-supplier records; draw 2 alone holds an
  unattributed "GPU shipments to grow 26% a year". Draw 3's answers lean on the "41% in calendar 2027" and the infrastructure demand;
  draw 2's call the 41% "a higher-growth view rather than a quantified revision to the 32% trajectory". The re-sends do not repeat the
  saved misreading of $553 billion.
- What Step 1 files under a question, compared between draws (`share of one draw's statements under a question that another draw also
  files there`, matched by article and wording): 74% at the median of 19 questions; FY2028 revenue is the lowest, 47% (12, 19 and 24
  statements). This counts differences in saved records, not how many matter.

## 5. Council B (`council/c-challenge.md`, `c-codex.md`) and verdict

Consensus: **no more sends.** A hand-built request could size one difference among several and would not change what goes to Alex.
Codex narrowed my claims, all taken:
- China: the same window-end request gave both answers (4, 5, 5), so the judge's own variation at the line is shown directly; that
  the input differences or the repeated $500 million frame caused draw 3's answer is not shown.
- FY2028: 3 of 3 against 3 of 3 is a strong lead that the two requests differ in what they produce; which difference does it is not shown.
- The missing H200 price limits what can be computed; it does not by itself explain the answer.
- The refusal stays as an observed defect of the frozen judge (the export-controls theme named as a dependency of the China question:
  42 of 65 refusals in six draws; the re-ask changed the rung 8 times), without assigning the two misses to it.
- Step 2: no part of either miss traces to it.

**Verdict.** Neither miss has a single proven cause. Both are questions whose estimate sits on a rung line, where three things move the
window-end rung: the frozen judge's own variation (shown on one request), what Step 1 files under the question in that draw (FY2028:
the least stable question, 47% shared between draws), and the judge's earlier reasoning shown again as the previous conclusion (seen
repeated, effect not shown). Nothing here is a Step 2 cause, so Step 2 stays closed (Step 2 log §17). No change is proposed: the one
concrete Step 1 slip (a "calendar 2027" figure filed under FY2027 only) is one record in one draw, and the larger items open now are
elsewhere (Step 4, and the unseeded measurement's unopened questions).

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| Refusal re-ask | Draw 3's China miss came from a refused rung-4 answer re-asked into rung 5 | none; the refused first request re-sent 3 times, with the note 3 times | 4, 5, 5 and 4, 5, 5 | refuted as the cause |
| Window-end requests | Each miss is the judge's coin flip on its own request | none; four saved requests re-sent 3 times each | China 07-14: 4, 5, 5 (open); FY2028: 3, 3, 3 against 2, 2, 2 (requests differ) | China: partly; FY2028: no |
