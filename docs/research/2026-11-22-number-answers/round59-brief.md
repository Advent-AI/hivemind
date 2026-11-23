# Council round 59 (Council B on the D744 second re-read, and a re-rank from the goal): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read.

## Material
- `docs/research/2026-11-22-number-answers/BLIND3-RESULT.md`, §1–§5.
- Run folder `poc/data/judging-v13s-blind3-2026-11-22/`:
  - `reread2-key.json`, `reread2-packets/T*.{md,claude.json,codex.json}`;
  - `reread2-adjudication/T*`;
  - `REREAD2-TALLY.json`, `reread2-controls/`.
- Registration: `SMALL-DESIGN.md` §5 to its [D744] block.
- Code and format: `calc_small.py` (`QUALIFIERS`, S1); `render_v13.py` (`v13s_schema` qualifier field and description).
- Rulings D741 (especially ruling 3).
- Earlier council: `codex-r56*.md`, `codex-r57.md`, `codex-r58.md`.
- The goal: D725 (unreliable number answers; Alex: "don't hallucinate with the numbers … get this right"). The registered next step
  after a clean blind test is the paid re-send of the 36 requests, which measures gpt-6-luna.

Out of scope: the frozen ruler, the production configuration, any paid run.

## Questions
1. **Is the second re-read scored right?** That covers five controls passing, the STOP on T10 F11 ("an estimated $750 billion",
   qualifier "none", which the enum forces), and the STOP on S having zero usable replies. Is the F11 finding a format gap (description
   versus closed enum), as I claim?
2. **Re-rank from the goal.** In five readings the writer side has been clean since run 3. The checker is unchanged since D742. The
   readers now pass five controls. The remaining stops are:
   - a small format gap (qualifier list);
   - a substantive judgement weakness on S: both writers size a data-center share of total capex that the passages do not support.
   What does the goal now need?
   - (a) Fix the qualifier gap with a case and a mutant, then run one more full $0 blind run with fresh writers, to see whether S's
     weakness recurs.
   - (b) Fix the qualifier gap, then go to Alex with the paid re-send request, carrying the S weakness as a registered disclosure the
     paid run must measure.
   - (c) Something else, for example a request change on how a supported bound must be shown, or making an unsupported share an
     unresolved answer.
   Which is honest under the registration and the rule that a stop goes back to council and then to Alex? Which avoids running for the
   sake of running?
3. **For the qualifier gap:** add "estimated" to the closed list, or change the description to say only listed qualifiers are recorded?
   Which matches the standard and the code with the least change?
4. **Anything missed.**

Return a numbered report: findings marked serious / minor / wording, with citations, then one recommendation and its falsifier.
