# Council round 58 (Council B on the D743 re-read): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read.

## Material
- `docs/research/2026-11-22-number-answers/BLIND3-RESULT.md`, §4 (the re-read).
- Run folder `poc/data/judging-v13s-blind3-2026-11-22/`:
  - `reread-key.json`, `reread-packets/Q*.{md,claude.json,codex.json}`;
  - `reread-adjudication/Q*.{md,claude.json,codex.json}`;
  - `REREAD-TALLY.json`.
- Registration: `SMALL-DESIGN.md` §5, the [D742] and [D743] blocks.
- The builders: `blind_test.py` (`READER_BRIEF`, `packets`), `blind_reread.py`, `blind_adjudicate.py` (`HEADER`, `build`).
- Earlier council: `codex-r57.md`.

Out of scope: the frozen ruler, the production configuration, any paid run.

## What I see
The range repair works on both controls, and Q07 is no longer marked for the range. The re-read still stops as written. Both readers
marked Q10's "plus or minus 2%" midpoint as number misread, and both adjudicators rejected it under the schema rule. The readers'
packets hold the user text and the answer, but not the format rules. The adjudication packets hold them and say "allowing what the
format rules permit". Both stops caused by the instrument come from that one gap.

## Questions
1. **Is the re-read scored right as registered?** That covers the STOP on Q10, both controls passing, and the claim that C-overlap's
   shared "two forecasts" mark is my control's stale text, outside the range rule it tests.
2. **The proposed structural rule.** The readers' packet carries the same format material as the adjudication packet: the system text,
   every schema description, and definitions that allow what the format rules permit.
   - Is this the right fix for the class, rather than another clause per finding?
   - What could it break? For example, readers anchoring on format permissions and missing real misreads.
   - What control would show it works?
3. **The next step.** Alex is active and authorized one re-read. Should a second blinded re-read under the structural rule go to Alex for
   authorization? Or does the evidence now argue for another path, for example taking the result to Alex as is, or a full fourth run?
   Weigh the reader judgement noise on S (the 90% share reply flipped between reader sets) when you answer.
4. Anything missed.

Return a numbered report: findings marked serious / minor / wording, with citations, then one recommendation and its falsifier.
