# Review round 22, confirmation only (read-only, $0)

Round 21 (`tools-review-codex-21.md`) found no verdict or report change from edited derived files. It found one gap: the import path
was not restored after a failure during setup.

The fix is in `git log -1` and D675's last entry. `score` in `stage0/score_comparison.py` and `scored` in `stage0/rebuild.py` now:
- save the path before their first import;
- restore it on every exit.

The dry run (`stage0/chain-dry-run.txt`) adds a failed setup, a missing confirmation record, and shows the path restored after it.

Check, citing file and line:
1. Is the import path restored on every exit, including a failure before or during setup?
2. Has anything you confirmed in round 21 changed?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 150 words. Report only a case of kind 1 or 2.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
