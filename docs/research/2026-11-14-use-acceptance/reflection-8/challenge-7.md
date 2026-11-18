# Deep council, round 7: the paired test's result (D655). Read it, challenge my reading, agree the next step

## What ran
- **Run:** `poc/data/clean-narrow-d436-paired-2026-11-17/run-1`. 52 sends, none lost; spent $1.52 against a cap of $3.60.
- **Reading:**
  - both reader families with 6 planted controls; the Codex packet-1 row on the planted other-question control was asked again in the established
    wording (`readers-answers/codex-handoff-1-again-1.md`), after two sessions gave Y and G as n/a;
  - two source reviewers;
  - third readers of both families on 14 disputed sends (`reading/third-reader/`);
  - the keys are now copied into `run-1/keys/`.
- **Score:** `run-1/score-output.txt`.

## The result, by the prewritten rule
| What | Frozen (as gate 1) | Edited (v5.5) |
|---|---|---|
| Targets acc/clean-8, acc/clean-9, pool-17 (3 passes each) | **0 of 9 written** (9 declines; both readers mark 8 of 9 N-unjustified, the 9th, pool-17 d2, is split and both third readers rule it unjustified) | **9 of 9 written**, no hard-line fault from either family, no material defect from either source reviewer |
| Decline controls (5 topics x 2) | 10 of 10 declined | 10 of 10 declined, none faulted |
| u2/clean-10 (reported) | 2 of 2 declined | 2 of 2 declined |
| u3/clean-10 (reported) | 2 of 3 written | 3 of 3 written; both arms carry a kind-(ii) "invented measure" flag from the Codex reviewer: wafer starts a month, a unit neither the topic nor the article names |
| Share control u3/clean-11 (2 passes) | 2 of 2 asked as the share; d2 has an L fault | 2 of 2 asked as the share, never the total; **d1 has an L fault** |
| Lost answers | none | none |

**The verdict: FAIL.** It comes from one prewritten clause, "each edited share-control send ... no hard-line fault". On edited-d1 the Codex reader
marked L: "The omitted Nvidia GPU rack spending share is not listed separately from whether ASIC gains come at Nvidia's expense". The Claude reader held.
Both third readers then ruled L fails, so the fault is agreed under both countings. The Claude third reader's reason: "the ASIC share does not
determine" Nvidia's own share, since all accelerator spending includes others.

## My reading, for you to attack
1. **The failure is not caused by the passage.**
   - The same L fault, on the same missing item, hits the frozen arm's u3/clean-11 d2: the third readers ruled 10-L fails as well.
   - Each arm has 1 of 2. Frozen d1 listed "Nvidia GPU racks' spending share" and held; edited d2 listed the capacity split naming "Nvidia GPU
     racks" and held.
   - This is the line-2 listing point D649 recorded as disputed on u3/clean-11, now ruled a fault by both third readers. It is an astra listing
     defect that predates the edit.
2. **What the passage was built to do, it did** (AGENTS §7.3: "a version that already meets the goal (what it was built to fix is fixed, nothing
   that was right turned wrong) is not dropped for a stricter rule"):
   - 0 of 9 against 9 of 9 on D654's class;
   - no control flipped;
   - the share was never switched to the total;
   - no material defect from either reviewer on the 9 edited target answers.

   But the rule was prewritten, and the FAIL stands as the reported verdict. I do not propose to relabel it.
3. **Disclosed, not deciding:**
   - pool-17's question asks units with a null reference and parks IDC's "19% growth" forecast in not_judged. On XR the third readers split
     (Codex: a growth rate is another quantity; Claude: it is the outcome's yardstick). XR is not a hard line.
   - The Claude reviewer flags all three pool-17 edited answers on the due day (kind iv): 2027-03-31 is code's 90-day day, while IDC's half-year data
     came 3.5 months after the half.
   - The share control's sources cannot yield the denominator (a W, upheld by the Claude third reader and rejected by the Codex one): both arms.
4. **The one invalid row** was a planted-control mark that no verdict path reads (Y and G on an event question carrying a figure ladder). The
   established ask-again resolved it. The planted controls were all caught by both families (score ran past that check).

## Proposed next step (one)
- **Record D656:**
  - FAIL by the prewritten rule, from the pre-existing u3/clean-11 listing defect at an equal rate in both arms;
  - D654's class is fixed on the exposed targets (0/9 to 9/9) with no control regression;
  - u3/clean-11's listing defect (Nvidia's own share not listed when the share of all spending is asked) becomes a recorded line-2 defect of astra,
    not of the passage.
- **Then put to Alex** whether to adopt v5.5 as the candidate request for the exposed gate-1 rerun on the 44 (about $4.74, cap $9.50, exposed),
  because his remaining test authorization (about $2.80) does not cover it. The listing defect would be expected to show there as line 2.
- **No new prompt change now.** The listing defect is a separate class, needs its own census, and would be a new arm.

Questions:
1. Is the FAIL correctly attributed?
2. Is adopting v5.5 as the candidate (not the frozen request) defensible on this evidence, given the exposure?
3. Is the next step right, or should the listing defect be censused first ($0, on stored gate-1 and this run)?

CONSENSUS or DISAGREE with the smallest change.
