# Council rounds on the run plan: what each round taught

## Round 1 (v1, 2026-11-17)

- **Codex:** NOT READY, 5 points. **Claude reviewer:** NOT READY, 5 changes.
- **Taught:**
  - I wrote the plan from memory of the launchers, not from their code. Four launch blockers would each have stopped or skewed a paid run:
    - Step 1 stopping at 300 calls;
    - the answer-choice step still on luna;
    - production ignoring the exclusions;
    - the judge stopping at the last article.
  - The time estimate (15 s an article) came from the old system's extraction, not the new system's Step 1 (26 to 34 s).
  - A carve-out (the company's figures outside N) came from one reader's position, not from D665's text.
  - **Lesson:** read every launcher a plan names before the plan is written, and cite a measured rate for every estimate.

## Round 2 (v2, 2026-11-17)

- **Codex:** NOT READY. **Claude reviewer:** NOT READY, 7 changes.
- **Taught:**
  - Fixes named in prose still failed against the code:
    - the astra check would refuse every retried request (`ladder_step.py:378` appends the refusal note);
    - `rg` skips SQLite files when searching a directory;
    - the runaway rule would stop a healthy production draw, since the sealed v34 run's cost per article rose from $0.0026 in early July to
      $0.0077 by August;
    - one shared ledger lets an old-system stop end three 20-hour new-system draws.
  - Two points promised in `triage-1.md` (a long-run checkpoint, and a rule for a draw that cannot finish) were missing from v2.
  - D665 items dropped between versions: D428's limits, the sign test, D431 for both systems, and the versions manifest.
- **Lesson:**
  - A fix stated in a plan is not a fix. One mechanism (prose fixes checked by readers rather than by the code they describe) has drawn
    findings for two rounds.
  - **The structural rule** (AGENTS §1, "stop answering findings: propose one structural rule"):
    - v3 states each requirement and its proof.
    - Prose review ends when a round finds no design-level gap.
    - Everything build-level is checked on the built artifacts at the stage-0 freeze review: code with its tests and mutants, the frozen
      files and the dry runs. That review gates the first paid send.

## Round 3 (v3, 2026-11-17)

- **Codex:** NOT READY, 5 design gaps. **Claude reviewer:** NOT READY, 5 design gaps. Under the new rule, both reported design-level gaps
  only. Every round-2 point was resolved except as below.
- **Agreed gaps** (both reviewers, or one with no counter):
  - an unfinished draw could still produce a verdict;
  - a shared ledger lets one draw's stop end its siblings (a change to D449 and D666 that needs a recorded replacement);
  - the replay exception was by kind, not by actual use;
  - the guardrail share departed from D428's decided-only measure;
  - there was no absolute late-stage stop;
  - "same question" and duplicates were undefined;
  - Step 2's lines had no pass rule;
  - the matching was not blind.
- **Taught:** the findings narrowed from launch blockers (round 1), to prose fixes contradicted by code (round 2), to rule definitions
  (round 3). The structural rule held: no build-level churn this round.
- **v4:**
  - one ledger per draw with absolute guards;
  - no release verdict without six complete draws;
  - the exception by actual use, classified per folder before the hits are read;
  - D428's measure, with the other marks reported beside;
  - the same-question rule, with `duplicate` as a worth mark;
  - Step 2's lines as hard checks with their pass lines;
  - blind X/Y mapping.

## Round 4 (v4, 2026-11-17)

- **Codex:** NOT READY, 4 points. **Claude reviewer:** NOT READY, 2 gaps. Both found every round-3 gap resolved.
- **New:**
  - replacement draws were unspecified (eligibility, timing, spend);
  - split marks against the "exercised" minimum;
  - duplicates counting toward the 30-question minimum;
  - a Step 2 line without enough cases;
  - the duplicate's direction in a same-bet pair (without it both questions could be marked duplicate, and a system loses a served matter);
  - census roots missing `tests/`, `poc/mock` and `poc/ui` (9, 561 and 78 in-span ids).
- **Taught:** the findings are now edge cases of rules already written; none reopened a rule. The duplicate-direction gap was a rule the
  earlier reading (A2) already had and v4 dropped. The lesson of round 1 recurs in small form: carry over the earlier instrument's exact
  wording, not a paraphrase.
- **v5:**
  - at most one replacement per system, for a non-system cause, under the same manifest, window and guard, by a council decision before
    launch (guards at most $360);
  - splits resolved in each counting, with "exercised" counting unsplit cards only;
  - distinct bets for the minimum;
  - an unmeasured Step 2 line cannot clear release;
  - the earlier-opened question is the original, and cards list questions in opening order;
  - the whole checkout and every worktree searched, test fixtures and mock data counted as reads.

## Round 5 (v5, 2026-11-17)

- **Codex:** NOT READY, 2 points. **Claude reviewer:** NOT READY, 2 gaps.
- **Points:**
  - replacement timing against D431's same-day rule (the reviewers split: the send day, or the window);
  - the split rule (v5 contradicted itself between "enters the denominators" and "reported beside"; a split with an insufficient mark;
    which way the old system's splits resolve; whether an unexercised subgroup can breach);
  - source copies named by filename. Seven full corpus copies sit under other names, so read literally every article would be excluded and
    N = 0.
- **Taught:**
  - A rule fixed by naming files instead of stating the property breaks on the first file with another name. Define by content.
  - When two reviewers read a decision differently, D439 takes the cheaper, reversible course, here no replacement counting toward the
    verdict, rather than another round.
- **v6:**
  - no replacement counts;
  - a split resolves to a mark its readers gave, per counting (the new system's cards most favourable in counting 1, the old system's least
    favourable, and the reverse in counting 2), with a resolved insufficient mark outside the decided denominators;
  - an unexercised subgroup cannot breach and gives "no practical winner";
  - source copies defined by content (≥ 90% of the source's rows by id and content sha);
  - git-ignored files searched.

## Round 6 (v6, 2026-11-17)

- **Codex:** NOT READY, 3 points. **Claude reviewer:** NOT READY, 4 gaps. Two gaps were raised by both:
  - the loss verdict against the unexercised-subgroup clause;
  - "same day" not holding for the counted draws themselves (a 20-hour draw crosses midnight).
- **Also:**
  - Codex: the content exemption exempted whole files, so a trace table beside a corpus table would escape.
  - Claude reviewer: the 90% test classed the earlier corpus builds (`items-window*.sqlite`, 2,205 rows) as selections, and so excluded 527
    of 1,619 scored articles.
  - Claude reviewer: mapping splits had no resolution order.
- **Taught:**
  - The coverage threshold was a second name-like proxy, a number fitted to the copies seen rather than the property. Corpus storage is a
    property of the table (its columns), not of its size.
  - A rule borrowed from a shorter run (D431's one calendar day, written for 14-day draws) must be restated for the run at hand, or it
    silently voids it.
- **v7:**
  - raw corpus rows of any items-schema table are exempt, and every other table and file is searched;
  - mapping splits resolve per counting (covers > does not cover);
  - an unexercised subgroup blocks only a lead, and the loss's a/b condition needs no guardrail;
  - "same day" for this run: the six draws are launched within one hour and run concurrently, in-draw redos count, every counted send falls
    within 72 h, and a breach is diagnostic.

## Round 7 (v7, 2026-11-17)

- **Claude reviewer:** READY. All five round-6 gaps were resolved, and there was no new design gap. The reviewer checked every small corpus-schema
  table in the checkout and the worktrees: no read is hidden on the current data.
- **Codex:** NOT READY, 2 points:
  - D431's timing needs an explicit recorded decision before any send;
  - the exemption should cover documented corpus storage only (a probe's selection can share the columns), and line 68 still excluded
    source copies.
- **Taught:**
  - A rule that is safe on today's data (the reviewer's check) is not yet a rule that is safe by construction.
  - Freeze the list of what is exempt, not a test for it.
- **v8:**
  - only documented builds, matched by id set (`corpus-builds.json`, frozen before the hits are read);
  - the leftover line removed;
  - the Stage A reading named by its path;
  - the decisions drafted as D667 (`D667-draft.md`), to be recorded before any paid send.
- **Round 8 goes to Codex only.** The Claude reviewer found v7 READY, and v8 changes only what Codex raised.

## Round 8 (v8 and D667-draft, 2026-11-17, Codex only)

- **Codex:** the D431 timing point is resolved. NOT READY on three points:
  - an id-set match could exempt a probe that reused a whole corpus;
  - the D667 draft dropped the replay exemption's conditions;
  - the draft's "any fix" contradicted the plan's launcher-only repair.
- **Taught:** a summary of a rule (the decision draft) loses conditions the rule had. Copy the rule's full conditions into the record; do
  not paraphrase them (the same lesson as round 4).
- **v9:**
  - verified raw copies only, with use always a read through the user's own trace;
  - the full replay rule copied into D667;
  - the launcher-only exception carried.

## Round 9 (v9 and D667-draft, Codex only)

- **Codex:** all round-7 and round-8 points are resolved. One mismatch remained: D667's "only these" omitted §1.2's other two exclusions (the
  search index and this comparison's own files).
- **Fixed:** D667 now says §1.2 governs the whole census and lists all four exclusions.
- **Taught:** the same lesson as round 8, one level down. A closed list in a record must be the rule's whole list.
