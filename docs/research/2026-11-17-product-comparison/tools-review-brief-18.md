# Review round 18, confirmation only (read-only, $0)

Rounds 11–17 all drew findings from one mechanism: a malformed readings file gets past the entry check. I stopped patching cases (AGENTS
§1) and made one structural rule (`git log -1`, D675's last entry):
- `validate_readings` in `stage0/score_comparison.py` walks the whole readings file top down, as one closed contract matching exactly
  what `mark_cards.readings` writes;
- every container's type is checked before it is read;
- it runs first in `verdict`, before `verify_inputs`;
- round 17's cases are fixed: the first-day map and each card's `opened` are required, and an unreadable named input is a refusal.

Check, citing file and line:
1. Is there a readings file that passes `validate_readings` and then either crashes the scorer or changes a verdict or printed value
   against what its well-formed reading would give? Give the file.
2. Does a readings file written by `mark_cards.readings` from a valid key and rounds still pass? See `stage0/chain-dry-run.txt`.
3. Is any value or verdict changed for well-formed readings?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words. Report only a case of kind 1, 2 or 3.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
