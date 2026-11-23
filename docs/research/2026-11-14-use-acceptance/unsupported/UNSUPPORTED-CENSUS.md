# When does the judge give an answer its evidence does not support? A census of the stored readings (D518, under D439), 2026-11-15, $0

Scripts: `inventory_earlier_readings.py` (every answer of the two earlier readings that both first readers did not pass, from the
readers' stored files; `inventory-earlier-readings.json`), `class-by-judgement.json` (the kind of each, written by hand after reading
every one), `tally_unsupported.py` (the counts). Nothing was sent to a model and nothing in either system changed.

## The answer

**Of 438 stored answers that two reader families have read, 36 were settled as unsupported or as resting on too little. 31 of the
36 are one situation: a question that asks for an amount, judged on days when nothing the judge was shown is enough to size it.**
The judge must still name a band, so it names one; the readers say the evidence prefers none. These are 438 readings of answers,
many of them the same question on successive days, not 438 independent cases: the 31 sit on eight question paths and three matters.
On the largest such question the timing is exact: in four runs, every answer of the first five days fails (19 of 20 for this reason,
one for another), and from the day the first sized amount is in view the readers pass every one of the 31 later answers. That is
the observed timing and the readers' verdicts; it does not prove the amount's arrival caused the change, or that every later
scaling is right.

Three more of the 36 are a second situation: the evidence sizes part of the answer and the judge closes the gap with a number of its
own (a discount of one-fifth, a growth rate of 25%, a scaling ratio), and that number decides the band. This is the kind found in
both later readings, and it is the one answer of the fresh week that both teams fail.

## What was read

| Reading | Judge and questions | Answers read | Settled unsupported | Settled "too little to prefer a band" | Not settled against the answer |
|---|---|---|---|---|---|
| Baseline (D426) | the frozen judge on hand-written questions, July window, three runs, every day's answer | 159 | 4 | 7 | 1 unresolved; 2 split and settled as supported |
| Stage B (D429) | the frozen judge on the new system's own questions, July window, three runs, every day's answer | 236 | 4 | 19 | 12 unresolved; 5 split and settled as supported |
| Trial (D485) | last answers of one run of each system, July window | 21 | 1 | 0 | 3 failed by one team only |
| Fresh week (D489) | last answers of one run of each system | 22 | 1 | 0 | 5 failed by one team only |
| | | **438** | **10** | **26** | 28: 13 unresolved, 7 split at first and settled as supported, 8 failed by one team only |

"Settled" is by each reading's own rule: both first readers, or both third readers where the first differed. The two earlier readings
are taken from their stored reader files and their recorded results (`clean-arch/step4-2026-11-10/stage_b/RESULT.md`,
`STAGE_B_RESULT.md`), where every answer a reader called unsupported was already read by hand; they are not read again here. The
eight answers of the two later readings were read here against their requests. The readings differ in what they read (every day's
answer against last answers only), so the 438 are not one sample and 8% is not a rate for the product.

## By what the answer did

| Kind | Settled (of 36) | Unsupported / too little | Where | Not settled |
|---|---|---|---|---|
| **N. An amount is asked; nothing shown is enough to size the total (no amount, like deal to scale from, or accounting identity for it; a part may be loosely sized, as "multi-billion"); a band is named anyway** | **31 (86%)** | 5 / 26 | 8 question paths on 3 matters: the total of credit support (19), custom-chip spending (9), memory capacity added in 2027 (3) | 4 |
| **B. Part of the answer is sized; a step of the judge's own closes the gap and decides the band** | 3 (8%) | 3 / 0 | supply commitments scaled by the revenue ratio; credit support cut to one-fifth "for timing"; data-center revenue with a 25% fourth-quarter growth | 10 |
| C. A figure held flat or carried from the previous answer without being derived again | 0 | | | 4 |
| S. An event with three outcomes; "still open" chosen because neither other outcome is settled today (the new system's questions only) | 1 | 1 / 0 | Kyber shipping | 7 |
| O. One of a kind | 1 | 1 / 0 | money already spent counted as still owed | 3 |

Unsupported alone (10): N 5, B 3, S 1, O 1. Nine of the ten are questions that ask for an amount. The "not settled" column holds
answers left unresolved, answers the first readers split on that were settled as supported, and answers one team alone failed.

N and B are two situations of the evidence (nothing enough to size the total; part sized). They are not shown to be two mechanisms
in the model: an N answer can also rest on an invented bridge, and a B answer on an inference no number explains. One of the three
settled B answers (supply commitments scaled by the revenue ratio) is one where my own earlier read supported the answer against
both first readers; the disagreement stands beside the class.

**The clearest picture (kind N).** "What total of credit support will NVIDIA have committed?" opens on 2026-07-01, when the news says
only that NVIDIA will back two partners' capacity (40,000 and 170,000 GPUs), with no dollar figure. For five days the judge answers
"below $5 billion" or "$1 to 5 billion"; the readers say nothing prefers any band. On 2026-07-06 one partner discloses a $4.88
billion backstop; the judge scales it to the other partner by GPU count, and from that day both families pass every answer of the
question (31 of 31 in the four runs).

| Run | 07-01 to 07-05 | 07-06 to 07-14 |
|---|---|---|
| baseline, run 1 | 4 too little, 1 unsupported (another reason) | 7 of 7 pass |
| baseline, run 3 | 3 too little, 2 unsupported | 7 of 7 pass |
| Stage B, run 1 | 5 too little | 8 of 8 pass |
| Stage B, run 3 | 5 too little | 9 of 9 pass |

The other two matters of kind N never receive an amount in the window: custom-chip spending (only one of four programmes is sized,
as "multi-billion") and memory capacity (a timing statement only). Their answers stay "too little" to the last day (2 of Stage B's 26
last answers).

**Kind B, the same deal in two runs.** At the end of the July window both systems hold the credit-support question with the same
$4.88 billion comparable. One run scales it to the second partner and cuts the result to one-fifth "for timing": $9 billion, the
fourth band. The other scales it to half the second partner's target: $15.25 billion, the fifth band. No statement gives either
fraction. Both teams fail the first; one team fails the second.

## Which words of the judge's instructions produce it (`src/hivemind/prompts/judging-v7.txt`, frozen)

| Kind | The instruction | Reading |
|---|---|---|
| N | "Return the rung's one-based position"; "State the implied figure or date"; "Missing confirmation alone is not grounds for the lowest or highest rung"; "A commitment or deal that is announced but not sized is sized from its disclosed comparable ...; a figure no one states is derived from the accounting identities in the evidence when they allow it." | **Missing, as a narrow observation.** The instructions say how to size a figure from a like deal or an identity, and forbid the lowest band for want of confirmation. They do not say what to return when the evidence cannot size a band; the answer form still requires one. This is not a full diagnosis: some N answers choose the lowest band because a higher amount is not established, which the existing instruction already forbids. The band differs by run (below $5 billion in the baseline's runs, $1 to 5 billion in Stage B's). |
| B | "A target for a product with no shipments yet is discounted by default"; "... scaled by capacity or units"; "a run-rate that carries the guided growth forward" | **Abstract, for the size of a permitted discount or scaling.** A discount or a growth is required, its size is left open, and each run supplies its own (one-fifth; half; 25%). Nothing here shows that a stated fraction would be the right general answer. |
| S | "'not established' is a statement of confidence, never a reason to stay", against the new system's three-outcome events (D409) | Not read here: the earlier reading left it unresolved between the families. |

Earlier decisions on the same ground: an obligation question opens whether or not the article gives its amount (D238, in the frozen
extraction standard), so the credit-support question is right to exist before any amount does; the judge's sizing from a like deal
and its discount for an unshipped product were written from the frozen reference's own reasoning (D263); the rule against the lowest
band for want of confirmation dates from D151 (two of 465 answers); "not yet judged" exists only for a question read from Alex's own
memo that has no linked evidence yet (D59), which does not decide the case of a question with relevant but insufficient evidence;
the new system marks an amount question's bands "no reference figure when the question opened" when its opening
article gives none (D398, 7 to 9 of 18 such questions).

## What it costs a reader, where the product is judged

- At the end of the July window, where the frozen judgement reference measures the answer: all 16 last answers of the baseline pass;
  of Stage B's 26, 21 pass, 2 are "too little" (kind N) and 3 are unresolved; the trial has one settled unsupported last answer of
  21 and the fresh week one of 22, both kind B.
- Kind N costs a reader in a question's first days, and for as long as no amount arrives: the answer shown is a band nothing
  supports, and it moves when the first amount arrives (from the first or second band to the fourth).
- Kind B costs a reader at any time: the band rests on a fraction or a rate the judge chose, and another run chooses another.
- Both sit in the judge, which the two systems share. Nothing here bears on which system carries forward.

## What this census does not show

- A rate: the earlier readings read every day's answer of 16 and 26 questions; a few questions carry the counts (19 of the 31 are one
  question in four runs).
- That the readers are right: two model families, whose bars differ (one family alone fails 8 answers of the two later readings; the
  families split on 22 of Stage B's 236).
- That a change would help. No change has been written or tried, and the judge is frozen.
- The judge's own account of why it names a band with nothing sized, or how it picks a fraction: not asked.

## The stop condition (council round 8), applied

A single situation does account for a counted share: kind N, 31 of 36. What is not established is a common cause, or a correction
that removes that share on stored cases without harming the answers that pass. So nothing is built on this census alone.

## Council (reflection thread "my", round 9): consensus, with corrections

The council ran both scripts (36 settled, 31 of kind N, reproduced) and read six of the hand classes against the readers' reasons;
all six stand. Its corrections are in this page: the 438 are readings, not independent cases; N means nothing sufficient to size the
total; the "not settled" column is split into its three parts; "missing" and "abstract" are narrow readings, not a diagnosis; D59
does not cover this case; the timing on the credit-support question is stated as observed, not as cause. **Decided under D439
(D519):** four neutral accounts from the judge on stored answers (two of kind N on different matters, two of kind B), each request
rebuilt and checked against its stored identity, ceiling $0.10; the raw accounts go back to the council before any design; the line
stops if they show no common, actionable instruction or missing input.
