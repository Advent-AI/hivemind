# Review round 15, confirmation only (read-only, $0)

Round 14 (`tools-review-codex-14.md`) found two more malformed-input cases. Instead of a fourth patch, the scorer now refuses malformed
readings at entry: `validate_readings` in `stage0/score_comparison.py`, called right after `verify_inputs`. The per-item diagnostics remain
for any other failure. D675's last entry records this; it is committed (see `git log -1`).

Check, citing file and line:
1. Does `validate_readings` accept everything `mark_cards.readings` writes? Read that function, and `stage0/chain-dry-run.txt`.
2. Does it refuse your round-13 and round-14 cases?
3. Is any value or verdict changed for well-formed readings?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
