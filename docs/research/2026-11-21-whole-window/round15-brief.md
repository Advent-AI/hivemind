Council R, round 15 (read-only), on your round-14 findings (`codex-r14.md`). Alex approved a $0.10 ceiling for the census (D700,
last entry of `docs/DECISIONS-log.md`). Read the changed files: `DESIGN.md` §3; `expected_links.py` → `expected-links.md` / `.json`
(R 1, W 43, O 61); `read_census.py` (rewritten); `window_test.py` (`census_pass`, `july_answers`, `census_reuse_dry`); the logs
`scorer-checks.log`, `census-reuse-dry.log`, `preflight-window.log`.

What changed:
1. Scorer: refuses unless given exactly draws 1, 2, 3, each with `draw.json` counted; refuses a missing READS answer; the known
   positive is right only with the registered direction and the sign together. $0 checks in `scorer-checks.log`: no draws refused;
   folders without draw.json refused; a missing answer refused; fake "reads" answers: 129 wrong, gate FAIL; a control with only the
   known positive: gate PASS; the known positive with sign opposite, or reversed: gate FAIL.
2. July samples: draw n answers the two seq-148 jobs with July linked-n's answers (matched by request hash) and buys nothing there;
   a draw is counted only when both were reused. `census-reuse-dry`: both reused, v9 reads v14 together proposed, complete, equal to
   old-2.
3. Registration: R is the known positive only; the CPU-to-total pairs and the credit-support-to-revenue pairs moved to O (the shown
   v1/v2 evidence ties credit support to product revenue); W keeps only pairs whose shown material names no connection. Please check
   the W list against the material each pair was shown (the READS requests are in any census-dry archive copy; the thesis texts are
   built by `jev_matching.thesis_text`, the candidate state by `candidate_state`).
4. Preflight over old-2's full archive and ledger (`preflight-window.log`): matching 1,277 judged, 3 refused (final-state artefacts:
   later successions of v28 and v14, v40 closed at 09-20), 10 skipped; the `neither` pass replays with the state of its time.

Answer with file and line: does each round-14 finding hold as fixed; is any W pair wrong given the material shown; anything else
blocking three sequential census draws under $0.10. Verdict: READY FOR THE CENSUS SEND or NOT READY.
