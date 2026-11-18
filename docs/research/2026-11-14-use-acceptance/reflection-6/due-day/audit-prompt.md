You are an independent, read-only auditor of a model request. No conclusion is preferred. Do not edit files or start runs.

**The request.**
- `clean-arch/step4-2026-11-10/ladder/candidate-system.txt` is the frozen system text.
- `docs/research/2026-11-14-use-acceptance/reflection-6/due-day/candidate-system-v2.txt` is a proposed version that changes one clause
  ("for an obligation already taken on" becomes "for the amount of an obligation already taken on").
- The closing check `clean-arch/step4-2026-11-10/ladder/candidate-closing.txt` and the schema `candidate-schema.json` are unchanged.

**The standard for due days.** Read in `docs/DECISIONS-log.md`: D403, D210, D185 and D414 (search for "## D403 ", "## D210 ", "## D185 ",
"## D414 "). Read also the clean step's design table rows on due days in `clean-arch/step4-2026-11-10/DESIGN.md` (around line 285 to
292) and the reader brief's D row in `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md` (the line starting "| `D` |").

**Audit:**
1. **Every sentence of the proposed request that decides a due day or its basis** (system, closing, schema). Give each a verdict
   against the standard: consistent, contradicts, keeps wider, keeps narrower, or no source. Do the same for the frozen request's
   version of the changed clause.
2. **The cases**, one line each: what day would the proposed request give, against the frozen one?
   - a binding-obligation topic asking whether a signed acquisition completes, with a stated check date in the topic;
   - the same topic with no stated date, only a period;
   - a binding obligation's amount at the next annual filing (purchase commitments);
   - an unsigned deal's signing;
   - a guarantee becoming final, with a stated date.
   Does any sentence still push the completion of a signed deal to the next annual filing? Does the change open a gap where no rule
   gives a day?
3. **Readers:** does the reader brief's D row, unchanged, now contradict the proposed request on any case? Say which way.

Be concise. End with one line: CONSISTENT CHANGE, or NOT CONSISTENT: <the reason>.
