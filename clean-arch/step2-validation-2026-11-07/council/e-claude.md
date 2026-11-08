# Council B, round 3: forward simulation done. Challenge the recommendation (read-only)

Following your round-2 advice: `forward_sim.py` runs Step 2 in article order against the library each decision would really see,
using real Jev J0 decisions (`forward-sim.json`). Every merged item, all 102 of them, was blind-read by two readers against its
receiving records and the dossier (`loss-answer-G/H-*`). The 48 never-labelled pairs Jev called repeats were labelled
(`v3-answer-E/F-*`): 24 same statement, 17 different fact, 6 disputed.

**Forward simulation (282 items → 180 records)**

| Measure | Result |
|---|---|
| The record holding a true earlier same-statement found in the search results | 112/113 |
| True repeats in the results that Jev left unmerged (duplicates) | 14 |
| Merged | 102 |
| ... of which no receiving record is the same statement | 9 (my read: 3 clear, 6 arguable) |
| ... of which a source is wrongly cited on an extra record | 10 |
| ... of which both readers say a material fact is lost that is held nowhere else | 66 (agreement 93/102) |

My hand-read of a random 12 of those 66: 3 material (Q1 net income and margin; Q2 guidance "±2%, assumes no China"; the Taiwan raid on
Supermicro bundled into a Singapore record), 3 moderate, 6 trivial. In a random 4 of the readers' no-loss items, there was no loss in
all 4. Estimate: about a quarter to a third of merges lose something an analyst would want. Readers over-flag.

**Stricter repeat question.** I probed a J2 arm on the 102 merges ($0.004). Its same_statement means "adds nothing an analyst would keep",
and a new choice, same_with_new_fact, keeps the record.
- Merges fell from 102 to 22.
- All 3 material and all 3 moderate losses were kept.
- 5 of 6 trivial were also kept, as were 3 of 4 no-loss items.
- Wrong merges: 1 of 3 clear cases fixed.

So Jev cannot separate trivial from material additions any better than the readers can. A materiality gate in Step 2 either loses facts
or throws away most of the deduplication.

**Recommendation to Alex: group, don't discard.**
- A repeat joins the existing record's group: its source is added (Alex's rule), and its own text is kept inside the group with its own
  id. The original record is never rewritten.
- The judge treats a group as one piece of evidence: the first statement plus the later retellings' details.
- This needs no materiality gate. Step 2 then decides only identity ("same story?"), and importance is left to the judge (AGENTS §2:
  code owns identity, never importance).
- Nothing is lost by construction.
- What remains: wrong groups (3 clear and 6 arguable of 102), where an item sits in the wrong group but its text survives, and 14 missed
  repeats.

Options shown to Alex:
- (e) group, recommended;
- (a) merge only pure retellings: measured, merges fall from 102 to 22;
- (c) no merging;
- the current rule, source only: measured to lose facts in about a quarter to a third of merges.

**Dossier picture.** The Kyber question goes from 34 items to 6 records; the largest group holds 14 retellings of SemiAnalysis's delay
report. The credit-support question goes from 46 to 20.

**Next test after he picks (e):**
1. Simulate the judge's input on the 3 predeclared dossiers, before and after, with nothing lost.
2. Take on the next class, wrong groups and missed repeats: J0 against J1 on the forward path, scored on the corrected labels.

Challenge:
1. Is grouping really loss-free, given that the judge may discount a grouped increment (for example NVL576 hidden in an NVL144 group)?
2. Does the evidence justify recommending (e) over (a)?
3. Is there anything I would be overclaiming to Alex?

Under 350 words.
