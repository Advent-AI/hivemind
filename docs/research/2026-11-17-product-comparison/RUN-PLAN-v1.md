# The product comparison that decides release (D665): run plan, version 1

**Alex:**
- D664: "no need for budget … run your council to determine".
- After D665: "okay then you should write a run plan and monitor it carefully and don't scope drift".

**Read as:** his word to run this comparison once this plan passes its council review. Nothing outside this plan is started. The rule it applies is
`clean-arch/PRD.md` §1.5, as D665 wrote it, and this plan does not change it.

## 0. Scope

**In:**
- one comparison: poc-v118 against the new system, from empty at 2026-07-01, three draws each;
- the blind matter census;
- the council's reading;
- the verdict by D665's rule;
- the report to Alex.

**Out, and recorded but not acted on during the run:**
- any prompt or answer-choice change (D662's hold);
- model trials;
- live-store, planner or integration work;
- D658;
- other weeks or companies;
- any "while we are here" fix.

A defect the run exposes is written to `FINDINGS.md` with its evidence, and goes to Alex with the verdict.

## 1. What is fixed before the first paid send (stage 0, $0)

1. **The systems.**
   - **Old:** poc-v118, as `run_fresh.py prod` runs it (`budget_replay`).
   - **New:** the clean pipeline, as `run_fresh.py clean` runs it: Step 1 c8, Steps 2 and 3, cases, the answer-choice step and the frozen judge.
     The answer-choice step runs on **gpt-6-astra** (D648, Alex: "那就用astra 吧"), with the frozen request unchanged; v5.5 is excluded (D656).
   - **The one code change this plan makes.** `run_fresh.py`'s frozen-configuration check accepts exactly one named, hashed variant,
     `astra-frozen`, which is the frozen configuration with the ladder model set to gpt-6-astra. It refuses anything else. The change comes with a
     test and a mutant. The code default (`stage_a.SETTING`, luna) is not edited.
   - Every file's sha256 goes in `manifest.json`. No package or prompt file changes while a run is live (AGENTS §9).
2. **The articles.**
   - The production list for 2026-07-01 to 09-20 is built through each system's own entry. `fresh_week_inputs.py` is generalised to a date range,
     with no other change.
   - The two lists must match in items, order and text sha, or nothing is written.
   - The manifest and its sha are recorded.
3. **The exposure census** (the full one D665 requires). Every input id in the scored range is matched against every past artifact:
   - every run folder under `poc/data`;
   - every research packet or reader file under `docs/research` and `clean-arch`;
   - the Stage A, Stage B and takeover cases.

   Each hit is classed by what used it (development, tuning, reading or measurement) and by system.
   - **The scored span** is 2026-07-20 to the last week with no development or tuning exposure for either system, at most 09-20. Articles
     with any such exposure inside the span go on the exclusion list, which is frozen and applied to both systems.
   - **The old system's own sealed run** (poc-v34, to 08-28) is listed as exposure only where it fed a change to poc-v118. That is traced from
     the decision log.
4. **The verdict rule** (`verdict-rule.json`, hashed): D665's rule, with the numbers written out.
   - **Practical lead:** a − b ≥ max(3, ⌈0.15·N⌉) and a ≥ 2b, under both split countings. Every guardrail subgroup must meet its frozen minimum
     and pass.
   - **Practical loss:** the mirror, or a guardrail breach under both countings.
   - **No practical winner:** everything else.
   - **Too small:** N < 20 matters, or fewer than 30 questions per system per draw in the guardrail sample.
   - **Invalid:** a planted wrong answer accepted; fewer than 3 of 4 supported controls accepted; or fewer than 2 of 3 repeats marked the same.
   - **Guardrails:** the unsupported share for figures, the unsupported share for yes/no questions, and the not-worth-tracking share. Each needs
     at least 10 cards per system across the three draws, and none may be more than 10 points above the old system's.
   - **Printed beside the verdict, not deciding:** D428's limits; the sign test and interval, labelled illustrative; the frozen-reference reading
     of 07-01 to 07-14 (D431); the proposed absolute floors.
5. **The reading's instruments,** written and hashed:
   - the census brief;
   - the mapping brief;
   - the card template;
   - the council-marking protocol, Deck 1's, with its fixes;
   - the control specifications;
   - the seeds;
   - the scorer `score_comparison.py` with its tests.
6. **Preflight** (AGENTS §5). Every stored answer of the latest runs of both systems is replayed through the current checks, and the refusals
   are read. A dry run of both launchers uses fake answers.

## 2. Stage 1: the slice

- **What runs:** one draw of each system over 2026-07-01 to 07-07, on its own ledger.
- **Checks before the full run:**
  - every article completes, or only the one failure the runner allows;
  - no refusal storm (no more than 5% refused);
  - spend and time per article fall inside 1.5 times the estimate in §6;
  - the first answer-choice request names gpt-6-astra and carries the frozen request bytes;
  - the old system's day files are complete.
- **If a check fails:** stop, write it to `RUN-LOG.md`, and fix only what the plan names (the launcher). Anything else goes back to Alex.

## 3. Stage 2: the full run

- **What runs:** three draws of each system, 2026-07-01 to the end of the scored span, all six at once on one shared ledger. They are launched
  detached, each with its log and pid (AGENTS §9). The slice's draw is not reused.
- **Stop rules,** run_fresh's own:
  - a crash, a dead launcher, a configuration other than the hashed one, a budget refusal, or a component stopped after its one redo stops the
    run;
  - a stop is diagnosed before any relaunch;
  - at most one relaunch per draw, recorded.

## 4. Stage 3: the blind matter census (runs during stage 2; it reads articles only)

- **Sampling:** per scored week, 40 articles drawn by a frozen seed from the manifest, less the exclusions, read in full. This is week reading
  A1's method (`../2026-11-14-use-acceptance/week/brief-A1.md`).
- **Readers:** Codex (memories off) and Claude (closed command line) list each week's big matters apart, in fresh closed sessions.
- **Merging:** code merges the lists, and the matters both families list form the core list.
  - A matter only one family lists goes to two third readers with its articles. It joins the list if both say yes.
  - The company's own financial figures form a separate reported row (D505).
- **Frozen,** with its sha, before any system output is read.

## 5. Stage 4: the reading; stage 5: the verdict

1. **The libraries are read at the cutoff, 2026-09-20** (or the span's last day): every question each system-draw holds, open or closed, with its
   latest answer.
2. **Mapping.**
   - Both families, apart, map each listed matter to each system-draw's question: opened, narrower, broader or missed. This is reading A2's form
     (`../2026-11-14-use-acceptance/week/brief-A2.md`).
   - Disagreements go to two third readers. A split is counted both ways.
3. **Cards** (Deck 1's template, with system labels hidden and order shuffled):
   - every question mapped as **opened** to a listed matter;
   - plus a guardrail sample of 35 questions per system-draw, drawn by a frozen seed;
   - plus controls in every batch of about 40 cards: 2 planted wrong answers (a rung moved, one per system), 2 supported controls confirmed first by
     a separate reader, and 2 hidden repeats.
4. **The council marks every card** by Deck 1's protocol: two closed readers, two debate rounds, and splits left as "cannot tell". Then
   `score_comparison.py`:
   - a matter is **served** by a system-draw when it is mapped opened and both families mark the card worth tracking and supported;
   - a matter is served by a system when it is served in at least 2 of 3 draws;
   - the score computes a, b and N, and the guardrails, under both countings, and applies `verdict-rule.json`.
5. **The report to Alex:**
   - the verdict first;
   - the counts, every split card listed for his spot check, and the figures printed beside the verdict;
   - `FINDINGS.md`;
   - the cost and the time.

   **No release engineering resumes until he answers.**

## 6. Estimates (from measured rates; labelled estimates, checked at the slice)

- **New system, per draw.**
  - Step 1 at about $0.0089 an article (the carried run), for about 2,800 articles from 07-01 to 09-20 (about 240 a week by the production
    selection): about $25.
  - Matching about $7, the judge about $2, and the answer-choice step on astra about $10.
  - **About $45 a draw.** Step 1 runs article by article, at about 15 s each: about 12 hours a draw.
- **Old system, per draw.** About $8, scaled from the poc-v34 run's $5.80 for 07-01 to 08-28, and a few hours.
- **The whole run:** about $160 and about 12 to 15 hours of wall clock with the six draws at once. Alex set no budget (D664). The shared ledger's
  ceiling is $250, a guard against a runaway and not a budget; reaching it stops the run and goes to Alex.
- **The reading:** about 40 to 50 matters by 2 systems by 3 draws, plus about 210 guardrail cards and the controls, so about 500 cards. With
  two readers and debates, that is about 1,200 closed sessions on the operator's subscriptions, 6 at a time: about 6 to 10 hours.

## 7. Monitoring (what I watch, and what I do)

- **The run:**
  - a `Monitor` on each draw's `run.json` states and the shared ledger. Every completed day, every stop, crash, refusal and redo is an event;
  - a 20-minute heartbeat check of spend against the estimate's curve, articles done per draw, and the time per day.
  - **If spend runs above 1.5 times the curve,** or a draw falls 50% behind the others: stop the run and diagnose it. The diagnosis is written
    to `RUN-LOG.md`, and the run is not relaunched unless the cause is the launcher.
- **The reading:**
  - every session is logged in `launches.jsonl`, and void sessions are rerun once;
  - the planted controls are checked as each batch closes. A batch that misses a plant is reread once by fresh sessions, and if it misses again,
    the reading is invalid.
- **`RUN-LOG.md`:** one dated row per event and per check, with numbers. It is reported to Alex as results land.

## 8. Returns to Alex

- the verdict, whichever it is;
- a stop whose cause is not the launcher;
- the exposure census leaving fewer than 4 scored weeks (too small to reach 20 matters);
- spend reaching the $250 guard;
- no verdict by 2026-12-01 (D665).
