# Council N: what "the judge and reading fixes stay quality work" means now, and whether any next action is worth taking (independent investigation; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Investigate independently. Claude is writing its own position in parallel, and you will challenge each other afterwards. Read the
record cold and do not assume earlier conclusions are right, including Claude's.

## What Alex decided (2026-11-20)
Claude put three options to Alex after council M (D688, `docs/DECISIONS-log.md` near line 10274). Option 1, recommended, in the
Chinese Claude sent: "旧系统继续上线，混合系统暂停冲'比旧系统强'这一关。判答案和读文章的改进还可以接着做，但算作提升质量，不再当作上线的理由。"
(Keep the old system, poc-v118, in production. Pause the hybrid's push to beat old. The judge and reading improvements may continue,
as quality work, no longer as a reason to release.)

Alex replied: "1. 好你去做，review deeply with council before your actions, don't haste into making actions".

## Objective
Decide, before any action, what option 1 concretely requires, and the one next action, if any.
- Keeping poc-v118 needs no change. Pausing the release line is a record.
- The open part is "the judge and reading improvements continue as quality work". Decide whether any judge or reading step now has a
  result that could change a decision (D543: close a path that has no such result left). If one does, name one recommendation and
  one test. If none does, say so, and say what would reopen each line.
- There is no release line now. Propose the quality measure, labelled "proposed, not confirmed".

## Constraints
- The frozen ruler (AGENTS §7.1) and the frozen production configuration `poc/config/poc-v118.json` never change. A new version of a
  production piece exists only when Alex opens it.
  - The judge is judging-v7 (D354). Alex opened a new judge version, J2, in D681.
  - D198 (what the judge reads: the evidence in view, and a previous conclusion that "carries" the rest) is Alex's decision.
  - The extraction prompt is frozen at v74i (D274).
- Alex is active, so a choice that changes what the system does goes to him, as options with a recommendation (AGENTS, "Authority and
  scope").
- **Spend.** Check this yourself. The last D439 tally in `docs/DECISIONS-log.md` is about $39.29 of $40, at D647 (near line 8912).
  - Later spends cite Alex's own authorizations: D655 ("你测试吧", about $6), D664 (the comparison), D679 (the merge test, $5
    ledger) and D681 (the hybrid).
  - D682 opened the `phase1b` ledger "inside D439's $40".
  - Ledgers: `poc/data/hybrid-2026-11-20/ledger/phase1.json` ($2.64 of $3) and `phase1b.json` ($0.36 of $2).
  - Say what headroom, if any, the council has for paid sends without Alex's word.
- **Out of scope:**
  - the clean path (the new system);
  - opening changes for release (closed by D688);
  - other companies' figures (only if Alex asks);
  - any edit to the frozen ruler or the gold.

## Primary materials
- `docs/research/2026-11-20-hybrid/PLAN.md`.
- `DESIGN-J2.md`, all of it. In particular results 1–7, "The fresh test", "The fresh census and council J", and the D198 options near
  line 274.
- `OPENING-CENSUS.md` and `census/CENSUS.md`.
- The council files `council-*-codex.md` and `reflection-k-*.md`.
- `docs/research/2026-11-19-merge-council/RESULT.md` (the c8 reading result and its cost).
- In `docs/DECISIONS-log.md`: D198 (search "## D198"), D260, D354, D543, D665, and D676–D688.
- Data: `poc/data/hybrid-2026-11-20/` (probe, deck, marks and score files, `freshpool.json`, `window/`, `prodpath/`).
- The judge's prompt and the code that builds its request: search `src/hivemind/` for "Previous conclusion" and `build_prompt`.

## Questions
1. **The judge.** Four angles failed (J2a, J2b, removing the previous conclusion, H1 the heading only). Is the remaining evidence a
   quality defect worth taking to Alex as a D198 question?
   - What is established: 0 of 13 move with the previous conclusion even on full evidence; 8 of 13 move without it, with 0 of 8
     controls moving.
   - What is not: net 4 jointly supported repairs against 5 required, and the frozen gold at 44.3 against 45.0, with d3-q17
     regressed.
   - If it is worth taking, what single test could decide it, given that the design has read every big numeric bet on this corpus
     (the fresh census found 1 target against 8 needed)? Consider a fresh window, the whole-window judge-only replay (about $3.3 per
     draw and arm), and D198 option 2 (a summary of the omitted evidence in place of the carried derivation). Give each test's cost,
     and what result would move the decision.
2. **Untested within D198:** moving the previous conclusion earlier in the request (named by reflection K). Is it a sourced lever, or
   a guess after H1's failure?
3. **Reading (c8).** Old's losses on the 32 matters are not reading losses (merge `RESULT.md`), and c8 adds about $24 to old's about
   $9 over 82 days. Is there any reading quality target with a measurable effect on final answers? If not, should the line close?
4. **Anything Claude has dropped:** a production defect inside old that is root-caused and in a module Alex has taken up. AGENTS §1
   says such a defect is never parked. An example to check: the D260 stance-field order that never ran (D681).
5. **The exit.** Name one recommendation and one test, or a close with its reopening conditions. What should go to Alex, and in what
   form?

## Deliver
- Facts and hypotheses kept apart, with files and numbers cited.
- Each claim says what would falsify it.
- End with CONSENSUS-READY: <one line> or OPEN: <one line>.
- Under 800 words.
