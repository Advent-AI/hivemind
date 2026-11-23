# Review round 7: the §1.6 design, v5 (read-only, $0; D672's condition)

`DESIGN-1.6.md` is now v5. It answers round 6: Codex's `tools-review-codex-6.md` and a Claude reader's points, both summarised in D675's
last entries in `docs/DECISIONS-log.md`. Some of it is already built in `stage0/`:
- `eligibility.py`: `section_inputs`, `verified`, and finished draws are recorded;
- `d400_code_check.py`;
- `score_comparison.py`: `printed_beside` and `floors_per_draw`.

Check v5 and that built code:
1. Is every round-6 point answered?
2. Is anything left that would change a pass or fail, or what a reader sees?

End with `BUILD AS WRITTEN` or `CHANGE: <the smallest changes>`. Keep it under about 350 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`, except its six `<draw>/run.json` files.
