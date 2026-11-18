# Review round 10, confirmation only (read-only, $0)

Your round 9 (`tools-review-codex-9.md`) asked for two changes. A Claude reader's round 9 asked for bookkeeping, design wording and two
D431 points. D675's "Round 9" entry in `docs/DECISIONS-log.md` records how each was fixed. It is committed at 547ea98e.

Check, citing file and line, only that each of those points is fixed:
- `stage0/d400_reader_lines.py`: exhausted sessions are terminal, and a missing session makes the draw's lines 1–5 "not measured";
- `stage0/step2_lines.py`: `CONTENT_ONLY` is in both key prompts;
- `DESIGN-1.6.md`: no leftover attribution sentence, and the key and eligibility wording match the code;
- `stage0/d431_reading.py`: packet field parity, and terminal missing sessions.

End with `READY` (the §1.6 tools may read the run's outputs) or `NOT READY: <the smallest changes>`. Keep it under about 200 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
