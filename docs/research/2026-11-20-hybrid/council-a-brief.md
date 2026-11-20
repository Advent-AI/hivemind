# Council A on J2, the judge's next version (read-only, $0)

You are an independent reviewer of a design, before any send. Read the primary material cold and form your own view before reading the
design's conclusions.

**Alex's request (2026-11-20):** "可以啊，你现在开始做hybrid system 的构建和测试，不要犯了和做新系统一样的错误到最后才发现问题". He agreed to fix
first the old system's judge reasoning errors, as a new judge version, with a council review before any test of a few cents. The plan:
`docs/research/2026-11-20-hybrid/PLAN.md`.

**Read, in this order:**
1. `docs/research/2026-11-20-hybrid/census/rejected-answers.md`: 49 rejected or split answers, with the judge's reasons and both
   readers' reasons.
2. `docs/research/2026-11-20-hybrid/census/CENSUS.md`: Claude's classification.
3. `src/hivemind/prompts/judging-v7.txt` (the frozen judge) and `src/hivemind/views/judging.py`, `schema_for` (lines 54–75 and
   `STANCE_FIELDS`).
4. The ruler and the decisions it rests on:
   - `docs/research/2026-11-01-e2e-loop/judgement-gold/reader-brief.md`;
   - `ruler-v1.md`;
   - D260 and D263 in `docs/DECISIONS-log.md` (search "## D260", "## D263").
5. `poc/data/hybrid-2026-11-20/account/*.json`: the judge model's own account of 24 targets.
6. `docs/research/2026-11-20-hybrid/DESIGN-J2.md` and the arms `docs/research/2026-11-20-hybrid/arms/J2a.txt`, `J2b.txt` and
   `*.order.json`. Diff them against `judging-v7.txt`.
7. `docs/research/2026-11-20-hybrid/judge_probe.py`, the harness.

**Challenge:**
1. **The census.**
   - Is the split between "reader-threshold splits" (23, set aside) and "rejected by both" (24, the target) right?
   - Is any of the 24 not a judge error, but a reader error or missing material?
   - Re-classify 5 of the 24 yourself and compare.
2. **The field-order finding.**
   - Verify it from the code and from 3 stored answers. The raw `response_json` content is in each draw's archive; `judge_probe.stored()`
     shows how to find it.
   - Is it a plausible mechanism for the boundary-crossing arithmetic, or a coincidence?
   - Does the D260 record show the intended order?
3. **The arms.**
   - Does each J2b sentence trace to the reader brief, D260/D263 or the extraction standard, without widening them?
   - Does any sentence contradict a D263 behaviour of the frozen gold: guided growth carried forward, untested targets discounted,
     sizing from a comparable, deriving from accounting identities? Could it bring back D260's v5 stickiness?
   - Are the check's examples fitted to the bench (AGENTS §6: a prompt serves every company)?
4. **The probe and its rule.**
   - Are the pass lines attainable, and are they meaningful against v7's own re-send noise?
   - Is the regression guard on the frozen judgement gold (the r9-frozen-v108 draws, `poc/data/e2e-r9-frozen-v108-2026-11-03/`)
     the right guard, and is it buildable from stored requests?
   - What is missing that would let a bad J2 pass, or that would only show at the end-to-end slice?
5. **One thing the plan may be getting wrong**, in the light of the new system's history: the problems found only at the end.

**Out of scope:** extraction, opening questions, clean Steps 2–3, cost, and any edit to the frozen ruler's files.

Answer in under 500 words: findings with file and line, then a last line `CONSENSUS: <one sentence>` or `DISAGREE: <one sentence>`.
