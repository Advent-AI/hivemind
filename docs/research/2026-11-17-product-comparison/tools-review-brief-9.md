# Review round 9, confirmation (read-only, $0; D672's condition)

Round 8 (`tools-review-codex-8.md` and a Claude reader) asked for changes. They are recorded in D675's last entries in
`docs/DECISIONS-log.md` and made in:
- `stage0/d400_reader_lines.py`, `stage0/step2_lines.py`, `stage0/d431_reading.py` and their tests;
- `stage0/census/census_readers.py` (`run`: a timeout is now a void);
- `DESIGN-1.6.md` v7.

Check, citing file and line, only:
1. Is each round-8 point fixed as recorded?
2. Did a fix break anything that changes a pass or fail, or what a reader sees?

End with `READY` (the §1.6 tools may read the run's outputs) or `NOT READY: <the smallest changes>`. Keep it under about 300 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`, except its six `<draw>/run.json` files.
