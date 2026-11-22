# Council round 44: are two code-review "bugs" real problems? (read-only, short)

Work read-only. Read `AGENTS.md` ("Authority and scope", §3, §7.3) first. Report in English, briefly.

## Context

The repository's owner, Alex, asked for a code review of commit range `95cf8da7..3ba40d8f`.
- **What the commit adds:** a paused "linking" version (`src/hivemind/views/links.py`, poc-v119 and poc-v120) and a citation judge
  version Alex chose not to adopt (judging-v12, poc-v121; D712–D719).
- **What the product is:** `poc/config/poc-v118.json`, which uses neither.
- **What the reviewer did:** reported two bugs and fixed them in the working tree, uncommitted. The diff is in
  `docs/research/2026-11-22-code-review/review-fixes.diff`.
- **Alex's challenge:** are these real problems, or nitpicking? Step back and converge.

The two "bugs":
1. `scripts/replay.py` (and `clean-arch/e2e-comparison-2026-11-13/budget_replay.py`) ran poc-v121 when someone named it. The fix adds
   `refuse_unadopted_judging`.
2. `src/hivemind/views/round.py` caught only `links.Refused` from `links.choose`. The fix records any other exception as an article
   failure (`linking_failed`), as matching does.

Claude's position, written before yours: `docs/research/2026-11-22-code-review/claude-r44.md`. Read the decisions it cites in
`docs/DECISIONS-log.md`: D359, D694 (§0), D712, D719, D723.

## Questions

1. For each bug: is it a real problem for the product or for any named use? Name the concrete failure, who would hit it, and how
   likely it is. Is the fix right, harmful or unnecessary? Check Claude's claim that the second fix can turn a budget-ceiling stop
   inside the link step into an article failure that lets a run continue. Read `round.py`, `links.py` and the budget transport in
   `budget_replay.py`.
2. Is any of the eight "recorded, not fixed" findings in D723 a real product risk? Answer in one line each, or "none".
3. Step back: does `3ba40d8f` change poc-v118's behaviour in any way? Look at the shared files: `judging.py`, `model.py`
   (`check_schema` `maxItems`), `scripts/preflight.py`, `store.py`, `writing.py`, `round.py`, `config.py`, `parallel_day.py`. Cite
   what you read.
4. The converged action: keep, revert or change each of the two fixes and the three clean-ups. Add nothing new unless it is a real
   product risk.

Out of scope: redesigning the linking version, the frozen ruler, prompts.

## Output

- A verdict line per bug: REAL, NOT A PROBLEM, or FIX HARMFUL.
- Answers to 1–4, each citing a file and line.
- One converged action list.
