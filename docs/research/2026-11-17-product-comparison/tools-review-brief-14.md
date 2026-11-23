# Review round 14, confirmation only (read-only, $0)

Rounds 11 to 13 found gaps of one kind: a diagnostic that fails on an invalid or too-small reading takes other diagnostics with it.
Instead of a third patch, one structural rule was made. It is committed at a9696395 and recorded in D675's last entry:
- every printed item is computed on its own (`PRINTED_ITEMS` in `stage0/score_comparison.py`);
- on an early verdict, `printed_items_tolerant` flags by name each item that fails and keeps the rest;
- the verdict itself is decided before any diagnostic.

Check, citing file and line:
1. Does the rule close the class, not only your round-13 example?
2. Is anything left in the scorer that could stop an invalid or too-small verdict from printing?
3. Did the restructuring change any value printed beside a lead, loss or no-winner verdict?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
