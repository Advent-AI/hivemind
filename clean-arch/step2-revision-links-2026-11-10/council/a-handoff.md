# Council A: what is the fix for a revision relation that files a record under the wrong question, and how is it measured (independent investigation; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Investigate independently; Claude is investigating the same material in parallel and you will challenge each other afterwards.
Read the record cold and do not assume earlier conclusions are right.

## Objective and pass line
Alex, 2026-11-10, after the result in clean-arch/step2-edge-effect-2026-11-10/RESULT.md and this question put to him: "when B is
judged a later version of A, should B automatically be put under every question A is under? Not automatically (my suggestion) /
keep it": **"okay take your suggestion what is the fix and how to measure get your council skill ready to propose"**.
So the council owes him one proposal: the fix, and how it is measured. No pass line is set; any number you propose is "proposed, not
confirmed". Nothing is to be built or sent in this round.

## Constraints
- Repository /Users/lchingen/hivemind, branch clean-arch. AGENTS.md governs (read sections 1, 2, 3, 5, 7.1, 7.2, 7.3 and 11).
- Frozen and not to change: production (src/hivemind, poc-v108/v116 configurations, the judge, the matching and writing code), the
  ruler (AGENTS 7.1). The clean path's Jev wording is not to be tuned (the council of 2026-11-09 and Alex's acceptance).
- The clean path: clean-arch/PRD.md sections 5 and 6 (Step 2 compare, Step 3 save); clean-arch/step2/compare.py;
  clean-arch/step3/library.py; the experimental writer between the library and the frozen judge, clean-arch/e2e-2026-11-09/adapter.py
  (the only writer of evidence and links on the clean path; clean-arch/step4-2026-11-10/DESIGN.md says Stage B will write "as the
  Stage 2 adapter writes them"). adapter.py is pinned by hash in earlier measurements' frozen lists (e2e-2026-11-09/stage2-frozen.sha256,
  unseeded-2026-11-10/unseeded-frozen.sha256).
- Out of scope: Step 1, the ladder step of Step 4, the frozen judge's own quality, Jev's prompt, any new model call in the product.
- Code owns identity, never importance (AGENTS section 2). No case-fitted rule, no probability cut-off, no hand list.

## Primary materials
- The rule in code: clean-arch/e2e-2026-11-09/adapter.py, Adapter.article (the loop after store.revise); its origin,
  src/hivemind/views/writing.py lines 240-266 with revision_refused (lines 88-105); what the judge prints,
  src/hivemind/views/judging.py (the "later version" line) and src/hivemind/views/store.py (revision_of, evidence_in_force).
- Decisions: docs/DECISIONS-log.md D168, D202, D203, D204 (search "## D202"); docs/DECISIONS.md D381, D391, D392, D395.
- The measurement so far: clean-arch/step2-edge-effect-2026-11-10/ (RESULT.md, PROTOCOL.md, edge_replay.py, inheritance_census.py) and
  poc/data/clean-step2-edge-effect-2026-11-10/ (inheritance-census.json, control/, remove-relation/, judge-probe-1/).
- The three saved draws: poc/data/clean-e2e-2026-11-09/stage2-clean-d{1,2,3} (trace.sqlite), -segment-2/step2/library.json,
  judged/ (draw 3: judged-2/) with views.sqlite, archive.sqlite, judge-requests.json. Source readers' labels of draw 1's 30 relations:
  reports/step2-revision-census-2026-11-09/comparison-after-challenge.json and RESULTS.md.
- Step 2 history: clean-arch/step2-validation-2026-11-07/LOG.md sections 12 to 15; the council-loop skill,
  .claude/skills/council-loop/SKILL.md (its trap list).

## Deliver
1. The mechanism, traced on one record end to end with ids and line numbers: which code writes the link, on whose decision, and
   what need the rule was meant to serve when D202 chose it. Count on the three saved draws what the rule did (you may query the
   sqlite files and json read-only): links it alone wrote, and for each whether the same statement was already under that question
   through another record.
2. Candidate fixes, ranked, at least two besides "never carry the link" (structural: where the rule lives, what is written, what the
   judge is shown; not wording). For each: what it changes in what is written, what it could lose (name the concrete loss case: a
   true later version of a statement a question holds that Step 1 did not file there), which prior decision it amends, its fit with
   the constraints, and the cheapest decisive check on stored data.
3. How to measure the chosen fix, in this order: what is exact and free on the three saved draws; what needs independent readers and
   how they are kept blind; what, if anything, is worth a paid send, with the number of calls and what it can still decide given
   that the class is about 1% of links and the one traced judgement did not change. Say what result would stop the fix.
4. Facts and hypotheses kept apart, with files and numbers cited.
Under 900 words.
