# Review round 16, confirmation only (read-only, $0)

Round 15 (`tools-review-codex-15.md`) found two holes in `validate_readings`'s closed set. They are fixed (`git log -1`), with my own
pass over every field the scorer reads:
- a split must be a list of two marks;
- a cover must be a JSON boolean or "split";
- duplicate counts may not exceed ids;
- a mapped matter must be on the frozen list, and its questions must be a list;
- each control must be a list.

Check, citing file and line:
1. Is there any field `verdict` or a printed item reads that `validate_readings` does not hold to an exact type or closed set?
2. Does `mark_cards.readings` still pass? `stage0/chain-dry-run.txt` was refreshed under the new check.
3. Is any value or verdict changed for well-formed readings?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words. Report only a case that changes a verdict, a
printed value, or a refusal; do not report wording.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
