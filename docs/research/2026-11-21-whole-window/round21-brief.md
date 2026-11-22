Council R, round 21 (read-only): the product version of the version-2 link question (D705). Read `WORDING-V2.md` §5 (design and its
four tables) and the code: `git diff -- src/hivemind/config.py src/hivemind/views/links.py tests/test_links.py
tests/test_frozen_questions_and_judgement.py` against the working tree (the linking version itself is uncommitted; review the parts
that add `link_questions`, `READS_V2`, `SIGN_V2`, `QUESTION_SETS`, the builders' `version` and its three callers, the new tests and
the pin), `poc/config/poc-v120.json`, `docs/research/2026-11-20-production-readiness/dependency-design/DESIGN.md` §0 (the versions line).

$0 evidence: the full suite 380 passed (2 new tests); `mutants.log` (13 of 13 caught: the 7 July mutants, one anchor moved with the
builders, and 6 for the version: READS, SIGN and correction ignoring the configured version; an unknown version and the field on
another engine accepted; a version-2 text drifting by one word); `v120-replay-{1,2,3}.log` (poc-v120 over the whole window, its link
jobs answered only by each probe draw's own answers by request hash: 17 of 17 met in each draw, nothing else asked, equal to old-2);
config checksums: poc-v119 aa577d68c3148864 (equal to the July test's records), poc-v118 4f2aad7d25dae54d (equal to old-2's).
One detail: the version-2 READS text carries the probe's bytes exactly, including the missing full stop before "When either question"
(v1 ends its sentence with ")"); kept so the product equals what was measured.

Answer with file and line: is the version correctly isolated (no change to poc-v119 or poc-v118 behaviour; no other reader of the
field); are the tests and mutants decisive; anything that blocks using poc-v120 as the linked arm of the paid design? Verdict: READY or
NOT READY. Out of scope: the paid design itself (next round).
