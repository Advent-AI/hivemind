# Stage B baseline reading: result (2026-11-11; D426)

**The frozen judge, on the ruler's hand-written ladders, gives an answer its own rules do not support in 4 of 151 decided
judgements (3%), and every one of the 16 questions ends the window on a supported answer.** The faults all sit in three
figure questions whose evidence states no amount yet: 4 of 52 decided figure judgements (8%) against 0 of 99 yes/no
judgements. This is the yardstick Stage B's lines 4 and 5 compare with; it says nothing about the ladder step's own
ladders, and Stage A has not passed.

One picture. "What total of financing commitments and backstops will NVIDIA report outstanding at its FY2027 year-end?" In
draw 1 the judge first said "below $5 billion" with nothing sized; on 2026-07-05 it moved to "$20–40 billion" by counting
the $30 billion NVIDIA had already put into OpenAI's funding round as a commitment still outstanding (UNSUPPORTED: money
spent is not outstanding). The next day Sharon AI's disclosed $4.88 billion backstop arrived; the judge scaled it to Firmus
by GPU count (about $25.6 billion), the same-programme comparable its rules allow, and from then on both readers support
every judgement of that question.

## What was read (`BASELINE.md`)

The 159 judgements of the three unseeded replays, unaltered, each read alone, in 40 shuffled packets with no two
judgements of one question; the form `ladder/stage-b-reader-brief.md`, which quotes the judge's rules. Two reader
families: Codex (one fresh read-only session a packet, 15 minutes in all) and Claude Opus 5.5 (one session a packet, 1.5
hours in all; Fable reached the account's limit after 6 packets and those files are not counted). Where they differed, two
third readers. My own read of every judgement any reader called UNSUPPORTED, written before the count. No pipeline model
call. The count: `baseline_count.py`, output `result/count.txt`; every condition of the plan was met (nothing incomplete,
stopped or voided).

## The controls

| control | Codex | Claude Opus |
|---|---|---|
| six planted wrong answers (two under each of the form's three tests) | 6 of 6 UNSUPPORTED, the stored rung named | 6 of 6, the stored rung named |
| three unaltered repeats, each read twice | 2 of 3 the same (custom silicon, draw 2, 6th: SUPPORTED, then INSUFFICIENT) | 3 of 3 the same |

The two families differ on 4 of the 159 stored judgements; the third readers agree on 3 of the 5 points put to them.

## The two shares

| | SUPPORTED | UNSUPPORTED | INSUFFICIENT | unresolved | UNSUPPORTED among decided (unresolved left out / for / against) |
|---|---|---|---|---|---|
| all 159 | 147 | 4 | 7 | 1 | 4/151 (3%) / 4/152 (3%) / 5/152 (3%) |
| yes/no, 99 | 99 | 0 | 0 | 0 | 0/99 |
| figures, 60 | 48 | 4 | 7 | 1 | 4/52 (8%) / 4/53 (8%) / 5/53 (9%) |
| draw 1, 54 | 49 | 1 | 4 | 0 | 1/50 (2%) |
| draw 2, 51 | 49 | 1 | 0 | 1 | 1/50 (2%) to 2/51 (4%) |
| draw 3, 54 | 49 | 2 | 3 | 0 | 2/51 (4%) |

**The last judgement of each question (2026-07-14, all 16): 16 SUPPORTED, 0 UNSUPPORTED, 0 INSUFFICIENT.**

## Where the judge fails, read judgement by judgement

Every judgement not plainly supported is in one of three figure questions: the financing total (draws 1 and 3) and
custom-silicon spending (draw 2). In each, the evidence at first gives capacities, growth rates or plans and no amount.

| question | judgements | verdicts | what the answer does |
|---|---|---|---|
| financing total, draw 1 | 1st to 4th | INSUFFICIENT (both) | "below $5 billion" with nothing sized; the evidence prefers no rung |
| | 5th | UNSUPPORTED (both; mine) | counts $30 billion already spent as outstanding, and another investor's facility as a comparable |
| | 6th to 12th | SUPPORTED | Sharon AI's disclosed backstop scaled to Firmus: a comparable the rules allow |
| financing total, draw 3 | 1st | UNSUPPORTED (both; mine) | "below $5 billion" chosen for want of a stated amount |
| | 2nd to 4th | INSUFFICIENT (both) | stays at rung 1, nothing sized |
| | 5th | UNSUPPORTED (both; mine) | moves to "$5–10 billion", a range no item sizes |
| | 6th to 12th | SUPPORTED | the same scaling as draw 1 |
| custom silicon, draw 2 | 1st | UNSUPPORTED (third readers; mine) | the lowest rung because no total is quantified |
| | 2nd | SUPPORTED (third readers; mine) | Broadcom's AI revenue, discounted: a comparable-based forecast |
| | 4th | unresolved (third readers part; mine UNSUPPORTED, leaning) | moves up on the same Broadcom figures read higher |

My own read agrees with the final verdict on five of the six I read and leans UNSUPPORTED on the one left unresolved.

**The mechanism.** The judge is sound on yes/no questions. On figures the readers support it once a sized amount or a
same-programme comparable is in view, though not always on a bridge they can check (custom silicon's 2nd judgement is
supported with an unquantified discount from Broadcom's wider AI revenue: a number in view does not by itself settle the
rung). Before that, on a figure question with no reference, it either picks the lowest rung for want of a number
(which its rules forbid: "not established" is never a reason), or reaches for a number the evidence does not give. Of
the twelve stored judgements not plainly supported, ten are of that kind; the other two count money already spent as
outstanding (financing, draw 1, 5th) and read the same figures higher (custom silicon, 4th, unresolved).

## What this means for Stage B (for Alex's decision; nothing is sent)

- The design's proposed lines would be: line 4, Stage B's UNSUPPORTED share among decided judgements at most 5 points above
  3%, so 8%; line 5, the share of judged theses whose last judgement is SUPPORTED at most 10 points below 100%, so 90%.
  Both margins are proposals Alex has not set.
- The baseline's faults sit exactly where the ladder step's questions are weakest: figure questions with no reference
  figure in their opening article (7 to 9 of 18 number questions in the unseeded replays, design §1; the fourth Stage A
  wrote 58 figure ladders of 104). So Stage B should be read per shape, as the design already asks, and a figure share
  compared with 8%, not the total with 3%.
- The baseline read every judgement alone; whether Stage B is read in the same shape is a choice for Alex (`BASELINE.md`).
- **How often the proposed lines are crossed by chance** (`line_chance.py`, `result/line-chance.txt`; the baseline's 16
  question paths resampled into tests of three draws; an unchanged judge and the same readers; $0):

  | theses a draw | figure share | overall UNSUPPORTED > 8% | figure UNSUPPORTED > 13% | median overall share |
  |---|---|---|---|---|
  | 7 | 37.5% (the baseline's) | 0.5% | 16.9% | 3.1% |
  | 7 | 56% (the fourth Stage A's) | 7.1% | 12.6% | 5.0% |
  | 10 | 37.5% | 0.1% | 12.7% | 3.2% |
  | 10 | 56% | 3.8% | 8.1% | 5.0% |
  | 12 | 56% | 2.6% | 6.3% | 5.0% |

  The overall share moves with the mix of shapes alone (3.2% to 5.0%). The figure baseline is 4 of 52 (7.7%) with the
  unresolved judgement left out and 5 of 53 (9.4%) with it counted UNSUPPORTED; five points above gives 12.7% to 14.4%,
  and the table tests 13%: crossed by chance 6% to 17% of the time, since six figure paths carry the faults in clusters
  (and some are the same question in two draws, so the paths are not fully independent; the estimate is conditional on
  these stored paths, not a measured rate for Stage B). The yes/no baseline, 0 of 99, comes from ten paths. Line 5 cannot be resampled (0 of 16 unsupported last
  judgements); over 30 theses an unchanged judge whose true rate is 5% misses it 6% of the time, at 10% 35% (a binomial
  over independent theses, a hypothetical), and 0 of 16 is consistent with a true rate up to about 17% (a one-sided 95%
  bound). Leaving INSUFFICIENT last judgements out of that share can raise it; they are reported beside it.

**Council B (`council/km-codex.md`, `kn-codex.md`), consensus:** the result is reported correctly; both changes made during
the reading were made and disclosed correctly; the readers' agreement establishes agreement, not calibration, and no
control is known to be sound. A separate calibration round with borderline controls was proposed by the council and
withdrawn once the lines' chance behaviour was measured: an expected verdict for a borderline case would need independent
human readers and Alex's approval, not mine. **The recommendation:** Alex sets Stage B's lines and reading shape knowing
the chance table, and decides the paid Stage B send on the ladder step as it ran in the fourth Stage A; the test is three
Stage B draws read with the same form and controls, reported by question shape with coverage and INSUFFICIENT beside.
**Found since:** the adapter's mode that lets the frozen judge run over the ladder step's questions in a replay (design §5,
"the new mode") is designed and not built; a paid Stage B needs it built and tested first ($0).

## What it cannot show

- Anything about the ladder step's ladders, which are not in this reading. Stage A has not passed.
- 159 judgements of 16 questions: the first share is close to a count of questions (three questions carry every fault);
  the second has 16 cases.
- The readers are two model families; they agree on 155 of 159, which also means a mistake they share is not caught. No
  control is known to be sound; the planted answers are plain errors.
- One family's repeat moved once in three (a SUPPORTED re-read as INSUFFICIENT on custom silicon): the boundary between
  SUPPORTED and INSUFFICIENT on figure questions is where the readers move.

## Corrections to my own work, kept

- Before the readers I expected the eight later financing judgements of draw 1 to rest on the $30 billion; from the 6th
  they rest on a sound comparable (`own-read-before-readers.md`).
- The count refused seven rows that follow the form's second test (UNSUPPORTED with no rung to point to); the check was
  stricter than the form and was corrected before any count (`BASELINE.md`).
- Seven reviews went into the plan before the readers started; the first review found the controls could be picked out
  by a packet's shape, which would have made the readers' catches meaningless.
