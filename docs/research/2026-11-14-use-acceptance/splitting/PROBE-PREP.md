# The split probe's $0 preparation (council round 161 → round 162), 2026-11-16

Nothing has been sent. The frozen answer-choice step's files are unchanged.

## The population (12 topics outside the 44; `probe_split.TOPICS`, fixed before any send)

Round 162 found the first population used the 44, on which D426 stopped tuning the step. A census showed 7 of its 13 topics were
among them (M, four C1, both C2), not only the two named. Every topic, and both plants, now comes from outside the 44, and the check
refuses a topic of the 44 by description (`descriptions_of_the_44`).

| Group | Topics | Rule |
|---|---|---|
| T | week 10-06 c1/clean-12 (global AI capex 2026 and 2027), c1/clean-4 (the five largest hyperscalers' capex 2026 and 2027) | the two stored one-quantity-two-open-years topics, declined in every stored send |
| C1 | fortnight c1/clean-11, c1/clean-9 and c1/clean-13; July c3/clean-5, c2/clean-5 and c1/clean-7 | census topics outside the 44 naming exactly two years, every stored send a ladder for one of them, most sends first. Derived again by code, and 3 of the 6 have both years open (c1/clean-9, c1/clean-13, c3/clean-5) |
| C2 | July c3/clean-7 (commodity DRAM, with the shortage and graphics memory as second sides), c2/clean-10 (custom-ASIC against GPU purchases) | the two topics outside the 44 that both blind readers of the D436 reading called one bet with a second side |
| C3 | July c1/clean-2 (the Intel stake), c1/clean-11 (Firmus) | the guards |
| M | none | the several-products memory topic's only stored instance is one of the 44. The probe does not exercise that path (a stated limit) |

## The check (`probe_split.py check` → `check-output.txt`, `check-passed.json`)

- **12 of 12** frozen requests equal their stored first request (sha256), with keys in the same order.
- **12 of 12** split first requests differ from the frozen one only in the schema's `no_ladder` and the system text's decline list
  (exactly `ladder_split.SYSTEM_REPLACEMENTS`). Each yearly re-ask differs from the split first request only by the yearly line.
- The **7** stored frozen ladders among them pass the step's checks.
- On both T topics, a synthetic split decline fits the schema and passes the checks. Three mutants are refused: an ended year, a
  split named again in a yearly re-ask, and stray periods.
- **Spend:**
  - at most 72 calls in the frozen arm and 216 in the split arm (a send, its one resend, and two yearly re-asks each resent);
  - with the transport's three attempts a call, at most 216 and 648 attempts;
  - the sum of their worst-case reserves, if every attempt were made at its worst: $2.94 and $8.94 (resends estimated as the
    request plus an answer at the output cap, 16,000 tokens at 4 bytes a token);
  - caps of $0.15 and $0.25 (together $0.40). Each attempt is reserved at its own worst cost before it is sent, so an arm stops at
    its cap, and a stopped arm is NOT MEASURED;
  - a guard stops every later attempt once an answer costs more than its reserve;
  - the stored charges of this step average $0.0008 a call (at most $0.0017), so the probe is expected near $0.10.
  - The bound holds while every charge stays within its reserve.

## The reading and the verdict (DESIGN.md v4 §3, §0b item 4, §0c item 3)

- **`reading_split.py`** builds one Stage A run folder of the items:
  - every yearly ladder of T and M, each with `split: {asked_year, asked_separately}`;
  - every C1 ladder of both arms, with `split: null`;
  - two plants made from stored frozen ladders outside the 44: `plant|1` asks the base year (fortnight c1/clean-9's 2027 question
    rewritten for 2026, given as a yearly item), and `plant|2` drops a limit (July c3/clean-7's "commodity DRAM" asked as "DRAM").
  - The key sits outside the repository. Item order is shuffled, and arms are not named.
- **The briefs:** `stage-a-reader-brief.md` plus `split-brief.md`. `split-brief.md` explains how a yearly item is read, and adds `BY`
  (asks a base year) and `LQ` (drops a limit). `split-third-reader-brief.md` and `reading_split.py disputes` give the third readers the
  `BY` and `LQ` points, marks shown as a and b. The gate marks' disputes use Stage A's own collector.
- **`score_split.py`:**
  - **the counts** (T at least 2 of 3 each; no control naming the case or changing kind). They refuse an arm without every topic and
    pass exactly once.
  - **then the reading's vetoes,** under both countings of unresolved points. The reading must hold exactly the items its sends give,
    and the key exactly those, or it is void.
  - **The verdict** is lead, negative, inconclusive or void. A failed count is negative whatever the reading.
  - **A stated limit:** yearly items exist only in the split arm and carry `split`, so readers can tell those items' arm. Arm names are
    hidden, and C1 items of both arms are read alike.

## Proofs

- **Tests:** 18 for the probe (`test_split_probe.py`: the send of both arms through the real runners with a fake transport, the
  refusal of a changed request, the counts, the reading, the verdicts and the third readers' packet), and 52 for the build.
- **The whole suite passes:** 346 tests, 261 in the new system's folders, and the frozen checks.
- **Mutants: 36 of 36** (`all-mutants.txt`). Three were missed at first, and each was caught once a test was added:
  - a T topic passing with one success;
  - the third readers seeing which family marked what;
  - the check not refusing a topic of the 44.
- **A gap closed:** the made-up yearly answers had written units outside the schema (`USD billion`). The fake model had skipped the
  schema check that `model.call` makes, so this was never caught. Every made-up answer is now checked against the schema
  (`test_every_made_up_answer_fits_the_schema_production_validates_against`), and the probe's synthetic split is too.
- **The prompt audit:** `PROMPT-AUDIT.md`, five blind rounds, the last with no finding the change introduced.
