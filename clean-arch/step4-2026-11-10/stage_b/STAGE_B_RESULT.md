# Stage B result: the frozen judge on the ladder step's own questions (2026-11-12)

**Stage B does not pass.** Line 3, the control theses, is unexercised: 4 controls are eligible with reader B's material shown,
fewer than the 8 the design requires ("else the control is unexercised and Stage B cannot pass"). The four agree with reader B.
On the judgements themselves, lines 1 and 2 and the figure and yes/no lines are met on all three readings; the last-judgement
line is met on two readings and missed on the strictest (3 of 24 when unresolved verdicts count as UNSUPPORTED). **Stage A has
not passed** (D426); nothing here changes that.

Run: three draws, 236 judgements, $0.4161 (`poc/data/clean-stage-b-2026-11-11/`). Reading: `poc/data/clean-stage-b-reading-2026-11-12/`
(the plan `STAGE_B_READING.md`, reviewed five times, `council/kv`–`kz`). Counts: `result/stage-b-count.txt`, `result/control-count.txt`.

## The lines (D428, D430; the design's §8)

| line | result |
|---|---|
| 1, no draw incomplete | met |
| 2, nine in ten laddered theses judged | met: 26 of 26 (u1 9 of 9, u2 8 of 8, u3 9 of 9) |
| 3, control theses | **unexercised**: eligible 7 (literal reading 4); with reader B's material shown 4, all 4 agreeing; fewer than 8 |
| figure, UNSUPPORTED at most baseline + 5 points | met: 3/88 (3.4%) against 12.7%; 3/95 (3.2%) against 12.5%; 10/95 (10.5%) against 14.4% |
| yes/no, UNSUPPORTED at most 5% | met: 1/117 (0.9%); 1/122 (0.8%); 6/122 (4.9%, at the line) |
| last judgements, at most one in ten UNSUPPORTED | met 0/21, met 0/24, **missed 3/24 (12.5%)** on the strictest reading; INSUFFICIENT 2 beside |

The three readings are: unresolved left out; unresolved counted SUPPORTED; unresolved counted UNSUPPORTED.

## The controls of the reading

- Trial: all six planted answers passed (both families UNSUPPORTED with the stored rung named), covering the three tests.
- Reading: both families caught 6 of 6 planted answers, naming the stored rung. Repeats: two read the same by both families;
  one (u2 v5 #5) read UNSUPPORTED both times by Codex and SUPPORTED both times by Claude, consistent within each family.
- The families differ on 22 of 236 stored judgements (9%; the void line is a third). Both third readers ruled each; they agreed
  on 10 and split on 12. On 9 of the 12 each third reader sided with its own family's first reader; on 3 (u1 v8 #4, u2 v5 #2,
  #4) each sided with the other family's (the council-loop skill's trap, "model readers carry their family's threshold", holds
  for most of the splits).
- Hours: Codex 0.3, Claude 2.4 (estimate 3.5 each). Codex reads with few visible reasoning tokens, as in the baseline (same
  setting, comparable). Three Claude sessions reported one shell command each on their own packet (a size check, a grep);
  none opened another file; their rows are kept and disclosed (`stage-b-reading-claude-sessions-notes.md`).

## Against the baseline (the frozen judge on hand-written ladders)

| | baseline (159) | Stage B (236) |
|---|---|---|
| figure UNSUPPORTED, unresolved left out | 4/52 (7.7%) | 3/88 (3.4%) |
| yes/no UNSUPPORTED, unresolved left out | 0/99 | 1/117 |
| INSUFFICIENT | 7 | 19, all figure questions |
| unresolved | 1 | 12 |
| all UNSUPPORTED, unresolved counted UNSUPPORTED | 5/152 (3.3%) | 16/217 (7.4%) |
| last judgements | 16 of 16 SUPPORTED | 21 of 26 SUPPORTED, 3 unresolved, 2 INSUFFICIENT |

With the unresolved left out or counted SUPPORTED, Stage B's UNSUPPORTED share is no higher than the baseline's; counted
UNSUPPORTED, it is higher overall (7.4% against 3.3%), though the figure and yes/no lines Alex set are each still met (council B,
`council/la-codex.md`). Its INSUFFICIENT and unresolved verdicts are higher on every reading. A share no worse than the
baseline's would not show the ladders sound (the plan's limits).

## What the traces show (my own read of all 17 judgements a reader calls UNSUPPORTED, and the INSUFFICIENT clusters)

The disputed and INSUFFICIENT verdicts sit on eight of the 26 questions (five matters, some asked in more than one draw), in
three patterns. Council B read two judgements of each and found the patterns real; the right rung in the disputed cases is not
established:

1. **"Still open" chosen because nothing is settled yet (Kyber, u1 v6 and u2 v5; 7 judgements).** The ladder step writes an
   event in three outcomes (Yes, Ruled out, Still open). The judge keeps "Still open" because neither a shipment nor a formal
   delay is established today, which its own rules forbid ("'not established' is a statement of confidence, never a reason to
   stay"). On the due day "Still open" needs NVIDIA silent about a slip for a whole year, the least likely outcome. The
   baseline's events had two outcomes, so this could not happen there. u1 v6 also carries a ladder defect Stage A recorded: a
   "during calendar 2027" event due 2028-12-31. The faulty reason is real; the right rung is not settled: a reported 2028
   shipment does not establish that NVIDIA will make the formal announcement "Ruled out" needs. My read is UNSUPPORTED on all
   seven; the families split and the third readers split, so these are my reading, not seven settled errors.
2. **Figure questions the evidence cannot size (u1 v1, u3 v1, u1 v8, u2 v7, u3 v10; 19 INSUFFICIENT).** The questions opened
   with no reference figure ("no reference figure when the question opened") and, in the INSUFFICIENT judgements, the evidence
   shown holds no comparable: NVIDIA's credit support to cloud partners (later judgements do use a disclosed backstop as a
   comparable), the hyperscalers' custom-chip revenue (which is not broken out in the evidence shown), HBM wafer capacity added
   in 2027. The judge picks a range anyway; readers call it INSUFFICIENT. The 19 repeat a few questions day after day.
3. **A figure carried forward instead of re-derived (u2 v7, $28bn of custom-accelerator spend; u3 v8, supply commitments).**
   u2 v7 keeps $28bn without deriving it, beside Broadcom's AI revenue ($10.8bn a quarter, $16bn guided), which the evidence does
   not split by buyer; my read that a share of it crosses $30bn adds an assumption the evidence does not hold. u3 v8 keeps $119bn
   flat, then scales it by revenue growth to rung 5; the evidence shown does not establish that commitments move with revenue,
   and readers, third readers and I disagree on whether that scaling is allowed. Neither alternative figure is established.

## Line 3, what failed

Of the 16 controls, the Ohio question is listed apart. Of the other 15:
- **8 are not eligible on the question**: 6 are not the same question as the ruler's (both readers, or both third readers on
  u2/clean-3), and on 2 the third readers split (u1/clean-6, which also has another due day, and u1/clean-11). The judged
  question asks about another quantity, scope or period than the hand-written ruler question. **Where that difference is made
  is not yet traced** (council B): the matching rule that paired them deliberately counts a part of a total, or the same event
  under another deadline, as the same matter (`unseeded-2026-11-10/MATCHING-v2.md`), and the ladder step writes the judged
  question and due day after Step 1, so the difference may come from Step 1, from the ladder step, or from the pairing's breadth. This is how Step 1 cuts a
  matter into theses: the diagnosis Alex chose next (D432).
- Of the 7 eligible, **3 had part of reader B's decisive material not shown to the judge** by 2026-07-14 (u1/clean-4 and
  u3/clean-6, q13; u2/clean-4, q04); where it was lost (linked and not shown, or never linked) is not yet traced.
- The 4 with the material shown all agree with reader B.
- **The trace (done, `CONTROL_TRACE.md`, checked by `council/lb-codex.md`):** most question differences are already in the
  Step 1 thesis (a programme inside a total, the article's reported date, a later milestone), kept by the ladder step; one is the
  ladder's wording and one is both. Two controls miss exact statements Step 1 stored with no link to any thesis (a supplier's
  growth forecast, the memory share of spending), though the capex thesis was open; the third missing statement left no record.
  These are leads for the Step 1 diagnosis (D432), not an established attribution.

## Limits

One send of three draws; daily judgements repeat questions (236 are not 236 independent tests); the planted answers are plain
errors; the third readers split by family on 12, so the strict readings move with that split; the control count compares 4
cases. Stage A has not passed.
