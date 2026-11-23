# Council round 63 (Council B on the D747 re-read's result): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line. Read the primary
files, not only the summaries.

## Context
- **Alex's ruling D747** is in `docs/DECISIONS-log.md`, last entry. The registered re-read is in
  `docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`, last block [D747], with council round 62's changes.
- **The result** is `docs/research/2026-11-22-number-answers/BLIND4-RESULT.md` §6. The run folder is
  `poc/data/judging-v13s-blind4-2026-11-23/`:
  - `reread-key.json`, `REREAD-TALLY.json`, `reread-reasons.json`;
  - the first readings: `reread-packets/W0?.codex.json` and `W0?.claude.json`;
  - the adjudications: `reread-adjudication/W03|W06|W07.(codex|claude).json`;
  - the packets: `reread-packets/W0?.md`.
- **Earlier context:** `BLIND4-RESULT.md` §1–5, `codex-r61.md`, `codex-r61b.md`, `codex-r62.md`, and D746 in the decision log.
- **The product goal** (D725): don't hallucinate with the numbers. The paid re-send stays on hold until an E writer repair passes a
  clean $0 test (D746).
- **The code checks** are in `calc_small.py` (D738: the code refuses only what the calculation's structure decides; indirect forms go
  to readers).

## Out of scope
The frozen ruler and gold files, production configuration, other modules, any spending, any file edit.

## Questions
1. **Is the FAIL real?** Read W07's answer, `poc/data/judging-v13s-blind4-2026-11-23/S/answers/claude.json`, beside its request. Is
   the upheld part-above-whole defect right? Why did the code accept it? Is the defect class common in the 18 stored blind replies
   (third run and targeted test), as far as their reasons and figures show?
2. **The three splits (T10, T15 and U02's support vote).** For each, which side applies D747's words right? Is any split a gap in the
   words (a clause read two ways), or is it single-reader variation on a boundary answer? Did the registration's "must settle" lines
   ask for more than readers can deliver? Check the earlier readings of the same answers.
3. **Claude's reflection** (`claude-r63.md`): attack its conclusions. They are: no further reader round; the next step is the E writer
   repair plus one design question about rung-setting bounds stated only in prose; one $0 writer test with lines only on stable
   readings. What does it miss? Which conclusion is weaker than it looks?
4. **One recommendation and one test** for what goes to Alex next, with what result would move the decision. Reject options that
   re-measure the same thing.

Return a numbered report: findings marked serious / minor / wording, with citations, then one recommendation and one test.
