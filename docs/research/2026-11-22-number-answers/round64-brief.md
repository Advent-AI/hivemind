# Council round 64 (before any writer of the D749 test is sent): independent review of the request change, the registration and the harness, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## Context
- **Alex's decisions:** D745, D747, D748 and D749 in `docs/DECISIONS-log.md` (the last entries), with his words.
- **The request change.** `docs/research/2026-11-22-number-answers/judging-v13s.txt` line 9 against the kept D745 text,
  `judging-v13s-d745.txt` line 9. Only line 9 differs.
- **The registration.** `docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`, the last block [D749].
- **The harness.** `docs/research/2026-11-22-number-answers/blind5.py`, which reuses `blind4.py` (`build`, `check`, `_display`,
  `REREAD_BRIEF`) and `blind_rules.py`. Adjudication goes through `blind_adjudicate.py`, default paths.
- **The evidence behind the repair:**
  - `BLIND4-RESULT.md` §1–6;
  - the saved E replies `poc/data/judging-v13s-blind4-2026-11-23/E/answers/*.json` and
    `poc/data/judging-v13s-blind3-2026-11-22/E/answers/*.json`;
  - council rounds 61–63 (`codex-r61.md`, `codex-r61b.md`, `codex-r62.md`, `codex-r63.md`).
- **The prompt principles** are in `AGENTS.md` §6:
  - the prompt carries the standard, not new rules;
  - it serves every company and never the bench;
  - never grow a prompt to fix quality without a written reason;
  - read the whole request as the model reads it;
  - check before the send.

## Questions
1. **Prompt audit of line 9, read in the whole system text and schema descriptions** (`poc/data/judging-v13s-blind4-2026-11-23/E/schema.json`
   shows them). Check each clause in both directions against D745, D747 and D749 and the existing sentences:
   - the discount sentences in bullets 2 and 3;
   - "not established … never a reason to stay";
   - "Missing confirmation alone is not grounds …";
   - "A consensus or guidance figure by itself keeps the judgement at the reference's rung";
   - the schema's `answers/why`.

   For each clause, say whether it is consistent, contradicts, keeps wider, keeps narrower or has no source. Is it general (no
   company, product or bench wording)? Is the growth justified? Is there a smaller change that does the same job?
2. **Read as the model reads it**, what will a writer do on E (management's "more than double" sits exactly on the $40B line, for a
   product not yet shipping)? On S? On P-v8? Does the change risk withholding P-v8, the supported case, or pushing every
   boundary case to "unresolved"? Use the saved replies as the cases.
3. **The registration and harness:**
   - the controls and their expected readings, including the floor control matched on its type and F12;
   - the pass, fail and inconclusive rules;
   - the reasons record;
   - each control packet carrying its own request;
   - the check that the built system text holds the repair;
   - whether the tally does what the registration says.
4. **Can this test change the next decision?** Name anything that makes it unable to.

Return a numbered report: findings marked serious / minor / wording, with citations, then a verdict: send as is, send with listed
changes, or do not send.
