Council R, round 13 (read-only). Alex chose A after the July test (D699, `docs/DECISIONS-log.md`, last entry): measure the linking
version poc-v119 over the whole release window against poc-v118, the measurement designed with the council at $0 first; the paid send
waits for your pass and a ceiling Alex names.

Read:
- `docs/research/2026-11-21-whole-window/DESIGN.md` (version 1, the whole design) and `window_test.py` (the harness so far).
- `neither.log` and the census printed in it (the $0 whole-window pass, results in DESIGN.md §2 once filled).
- The July record it builds on: `docs/research/2026-11-20-production-readiness/dependency-design/` (DESIGN.md, TEST-PLAN.md,
  july_test.py, JULY-RESULT.md, reading-rule.md) and the July sequences' stored link answers
  (`poc/data/july-link-test-2026-11-21/linked-{1,2,3}/archive.sqlite`, call ids 8738 and 8739).
- The code paths named in DESIGN.md §1 for the claim that no request other than a reader's judgement carries another question's
  conclusion: `src/hivemind/placement.py` (question_lines, takes), `src/hivemind/views/jev_matching.py` (candidate_state,
  thesis_text), `src/hivemind/views/matching.py` (describe_view), `src/hivemind/views/judging.py` (build_prompt, themes_in_force),
  `src/hivemind/views/links.py`, `src/hivemind/views/round.py`, `src/hivemind/views/writing.py`.
- AGENTS.md (§1, §2, §5, §7.2, §7.3), PRD 06 (`docs/prd/06-views.md`, dependency section, line 134), D537 and D368 in the log.

Out of scope: the frozen ruler, extraction, filing, the theme block, the old system's other defects, anything outside the linking
version's measurement.

Answer, with file and line for each point:
1. Is the paired shape (old-2 continued, only changed requests bought) sound for Alex's four questions? Is the claim in §1 that no
   other request carries a judgement true in the code? Name any path it misses (a judgement read by extraction, matching, closing,
   the theme block, idea routes, the day's queue, judgement ids in a request).
2. The coin-flip finding (§3): is the reading of the July probabilities right, and is the census the right cheapest proof before
   buying judgements? Is its decision rule (3 of 3, margin 0.10) sound, or does it judge nothing?
3. The census harness (`census` in window_test.py): does handing the writer no link keep every later request equal to old-2's (no
   other effect of a proposal: the `changed` set, the graph check, the `proposed`/`committed` records)? Any way it can buy something
   other than a link job? Is a $0.10 ceiling with Jev reserved at 64K x 3 sound for three parallel draws?
4. The paid run (§4) and reading rule (§5): what is missing or wrong (arms, retirement point for controls, the stored path as a
   control, rule B's generalisation, the pass line, the null of a comparison over one window)?
5. Verdict: READY FOR THE CENSUS SEND, or NOT READY with the findings that block it. The paid run gets its own round after the census.

Results already in hand ($0): the `neither` pass equals old-2 in every table over all 1,884 articles (DESIGN.md §2, neither.log); 14
openings, 105 eligible pairs; `census-dry` (every pair answered "reads", writer handed no link) equals old-2 with 105 links proposed and
0 written (census-dry.log); its mutant (links written) stops on 07-01 (census-mutant.log).
