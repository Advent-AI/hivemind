# Council round 3: design version 3

Version 3 is `NEW-REFERENCE-DESIGN-v3.md` in this folder (a read-only copy). It answers your round-2 review and the Claude family's review of
version 2, condensed in `council-claude-2.md`. Its change list is §14. Its structural rule against fitting is §0.

Check each of your round-2 findings against version 3:
1. **The event comparison:** `outcome_on_due_day`, and "cannot tell" excluded.
2. **The signing closed set,** including invalid rows, no_view and his own answer.
3. **The access boundary for every participant:** inline prompts, logs checked for both families, the closed key set, the judgement-text check.
4. **The failure states.**
5. **The items-only brief, the validity schema, the null baselines** (now with their own verdicts), **the line against A, and the predictions.**

Then look for anything new that version 3 introduces:
- the stripping rule;
- the kind and unit derivation;
- `outcome_on_due_day` as an addition outside the brief file;
- PASS requiring the judge to beat every baseline;
- Ohio dropped.

Out of scope: the ladder step's prompt, gate 1, and cost. The frozen ruler's files must not change. End with `READY` or `NOT READY: <the smallest
change>`.
