# Hybrid system: build and test plan (2026-11-20, D681)

**Alex, 2026-11-20:** "可以啊，你现在开始做hybrid system 的构建和测试，不要犯了和做新系统一样的错误到最后才发现问题". This was his reply to
the proposal to fix, first, the old system's judge reasoning errors as a new judge version: a council review first, then a test of a few
cents (`docs/research/2026-11-19-merge-council/RESULT.md`, "Where the old system loses").

## The new system's mistakes, and the guard for each
| Mistake | Where it showed | Guard in this plan |
|---|---|---|
| Steps were tuned on their own scores. The hand-off broke and was found at the end: Step 1's questions refused by the ladder, 19–27 of 60 (D432) | the release comparison, D676 | Every change is accepted only by its effect on final answers, read by blind readers on the analyst matter list. An end-to-end slice runs in week 1, not at the end |
| The attainable verdict was not computed: $145 spent on a knowable result | D676 | The ceilings are below, computed before any send |
| A policy removed matters by construction (company figures, D382), and it was known only at the end | D676 | Alex decides the figure questions for the hybrid now (below) |
| Lines with no source, or that the change could not move (the merge test's P2) | D680 | Every line names its source and the change that can move it |
| Choices made on the test set, and fix-and-rerun loops | council-loop traps | Designed on the stored failures of 09-07..09-20 (dev). Accepted once on a window the design never saw, with its matter list built blind before any hybrid output is read |

## What the hybrid is
| Piece | From | Status |
|---|---|---|
| Opening questions and their answer choices | Old (poc-v118) | Unchanged |
| Reading articles | Old extraction (control arm) or clean Step 1 c8 (hybrid arm) | c8's effect on final answers is measured end to end, not assumed. On the 32 matters, old's losses are not reading losses |
| Judging | Frozen judging-v7, then a new version (J2) | The change; Alex opened it on 2026-11-20 |
| Clean Steps 2–3 | Not in the first build | Added only if a measured loss calls for them |

## Attainable, on the frozen 32 matters (from the stored readings, $0)
- **Old serves 10.**
- **The judge fix can add M08 and M14.** Old opened each in 3 of 3 draws, and the readers rejected every answer for reasoning:
  - adding amounts that overlap;
  - a cumulative estimate taken for an outstanding balance;
  - a five-company or company-forecast figure taken for a four-company answer.
- **M30 (+1)** only if company figures are kept.
- **M05, M09 and M25** (served in 1 of 3 draws) and the **17 never opened** move only with opening, not the judge.
- **The release lead** (D665: a − b ≥ 5 and a ≥ 2b against old) is out of reach for the judge fix alone, with a ≤ 3. The judge fix is a
  quality gain. A release needs phase 2, opening.
- **If D382 applies to the hybrid** (no company-figure questions), old keeps 5–6 matters the hybrid cannot serve, and the hybrid loses by
  construction. Hence Alex's decision now.

## Phase 1: the judge (J2)
1. **$0 census.** Every answer of the 5 stored draws that the readers rejected or split, among the questions rated worth tracking. The
   same frozen judge answered old-1..3 and new-2..3. Each is classified by mechanism, from the readers' reasons and the judge's own:
   - overlap or arithmetic;
   - range against the answer's own estimate;
   - scope (other companies, year or measure);
   - source weight (a company's own forecast over independent ones);
   - missing material;
   - the boundary between two ranges;
   - other.

   The largest class is the target.
2. **Mechanism.** The whole judge request is read for 10 cases. The model's own account is taken on up to 10, at a cent each.
3. **Design.** A prompt audit of judging-v7 against the judgement ruler (`ruler-v1.md`) and the standards. The levers are structural
   first, for example a required estimate field whose chosen range code checks. Every sentence names its source, or goes to Alex.
4. **Council A** on the design: an independent Codex read, then challenge rounds to consensus.
5. **$0 checks.**
   - Stored requests are rebuilt byte for byte.
   - A synthetic answer passes every code check.
   - J2 sits beside judging-v7. The production default and the frozen tests stay unchanged, apart from the code that admits a second
     version.
6. **A probe of cents.**
   - The stored final requests of the failing cases are re-sent with J2, 3 times each.
   - As many supported answers are re-sent as controls, which must not regress.
   - Blind readers mark them, mixed with the archived answers.
   - **Pass:** the decision rule in `DESIGN-J2.md` (targets, controls and the frozen gold, each against v7's re-send).
7. **A production-path check, then the end-to-end test in week 1** (revised after councils A and F).
   - The production path is verified at $0: a two-day replay of old-2 gives 72/72 requests byte-identical to old's, starting from
     production's own queue.
   - The end-to-end test of a judge change is a **judge-only replay of the whole window from 07-01**, with old's links, sources and
     relations fixed. Each arm, v7 and the candidate, builds its own conclusions, citations, theme effects and queue.
   - A slice from a 09-06 copy would carry every earlier wrong rung into both arms (council F).
   - Readers mark every answer at 09-20. The 32 matters are counted as dev.
   - Cost: about $2 per draw and arm, from archived tokens. The c8 reading arm is a separate later test.
8. **Acceptance** on a fresh window, run once on Alex's word.

## Phase 2: opening
- A census of why the 17 matters were never opened, after phase 1's end-to-end slice. It is not designed now.
- **Status (2026-11-20):**
  - The census ran (D686).
  - Alex kept company-figure questions in the hybrid (D687).
  - Council M found no credible path to D665's lead through opening changes alone (D688), so no opening test is sent.
  - Alex chose option 1 (D689): poc-v118 stays production, and the hybrid's release line is paused.

## Status after D689 (2026-11-20)
- Council N (`council-n-*`, a fresh Codex thread, consensus) closed the judge line and the c8 reading line for now (D543). Nothing
  is sent, and D198 is unchanged.
- **The judge reopens** on eight eligible failures on fresh questions (never read by the design, counted once across draws), with
  matched controls and a source-checked summary of the omitted facts (D198 option 2). The D198 choice and its price then go to Alex.
- **c8 reopens** on a traced decisive fact that old missed, c8 delivers, and that could change a named final answer.
- **A future test's pass criteria** (proposed, not confirmed):
  - net repairs on distinct final forecasts, backed by both readers in 2 of 3 same-day pairs;
  - at least 4 at 8 targets;
  - no lost control and no added refusal;
  - frozen agreement at least v7's, with China share 3 of 3.

## Limits
- The frozen ruler is unchanged.
- No paid send before the council and the $0 checks.
- Phase 1 through step 6 costs about $1. Step 7's estimate is written before it runs.
- Nothing is pushed or deployed.
