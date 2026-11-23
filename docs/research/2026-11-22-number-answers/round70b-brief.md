# Council round 70b (confirmation before the one-time paid send): read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 70 (`docs/research/2026-11-22-number-answers/codex-r70.md`) said "send with listed changes". The changes are recorded in
`PAID-GATE.md`, the last section "D753":
- `paid_gate.py`: `renamed_text`, `named_in_text`, `normalise` and `card_view`, with `card_lines` passing `base['shown']`;
- `reader-brief-v13s.md`, new beside `reader-brief-v13.md`;
- `assemble_readings.py`: `split_exact` and `third_exact`.

The authorization is one-time and cannot be redone.

## Check
1. **Does each change do what round 70 asked, and nothing more?**
   - Read the diff against the earlier code (`paid_gate.py` around `normalise` and `card_view`).
   - Render the six D751 answers (`poc/data/judging-v13s-blind7-2026-11-23/{S,E,P-v8}/answers/*.json`, with each case's `item.json` as
     the plan item) through `card_lines` in memory. Confirm the previously lost passages and figure references are now shown and
     resolve, and that no value changed.
2. **Does the new reader brief carry D747 and D753 faithfully,** with the four questions, the verdict lines and the third-reader rule
   unchanged? Does it name no case?
3. **Is anything left that would waste the send:** the plan pin, the cap, the authorization path, the launch command and the log
   outside the run folder?
4. **Verdict:** send, or do not send (with the blocking reason).

Return a short numbered report with citations, then the verdict.
