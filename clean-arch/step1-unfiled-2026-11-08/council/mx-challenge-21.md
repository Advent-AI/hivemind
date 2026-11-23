# Council mx, round 22: Alex is inactive (D509; D439 in force); the six-call test's design before the send

Alex answered D508's question with: "修改goal，我要睡觉了，下来你自行按照我的准则操作，需要深度的审视每一轮run 用council" (D509 in `docs/DECISIONS-log.md`). From
here a choice that would have gone to him is yours and mine to settle, recorded citing D439. You and I already agreed on this test
(your round 21); this round is its design, before anything is sent.

Read `docs/research/2026-11-14-use-acceptance/effect/EFFECT-TEST-DESIGN.md`, `effect_test.py` (after the reviewed
`docs/research/2026-11-04-filing-end-to-end/one_test.py`), and `brief-stance.md`. The dry run's output: the control rebuilt with the
frozen judge's setting and schema has the stored archive key; the inserted block is character for character the text the judge saw
for e379 under v3; six calls, worst case $0.054, ceiling $0.25. You can run the dry check yourself (it sends nothing and writes
nothing): `python3 docs/research/2026-11-14-use-acceptance/effect/effect_test.py poc/data/clean-lean-week-2026-11-14/week-r2/c1
poc/data/clean-effect-test-2026-11-15/v7-e379 --view v7 --add e379 --from-view v3`.

Name only what would make the result wrong or unreadable:
1. **The two requests:** is the control the bytes the run sent (rebuilt by `model.build_request`, refused unless the archive key
   matches), and does the treatment differ in the one block and the count only? Is the head of the list the right place for a
   statement from an article earlier than the question's first?
2. **Sending straight through the transport** (as `one_test.py` did): three fresh samples a condition, no archive lookup. Anything
   that makes them not comparable (caching of the shared prefix; order; time)?
3. **The reading:** `firm` / `qualified` / `not_yes` and `uses_precedent`, by a reader of each family not told there are two
   conditions. Do these definitions measure a loss of confidence without merely detecting a citation? Is "names a risk that MIIT
   withholds approval" the right line between firm and qualified for a judgement whose stored reasons already carry caveats?
4. **The outcomes:** moved; confidence fell; inconclusive. Too easy to reach "fell" (two of three against two of three with three
   sends)? Too hard? Does any path let an inconclusive result be read as "no effect"?
5. **Scope under D439:** is this step within what Alex has taken up, and within the ceiling.

Then say whether the six calls may go. End with: "Council position: <...>".
