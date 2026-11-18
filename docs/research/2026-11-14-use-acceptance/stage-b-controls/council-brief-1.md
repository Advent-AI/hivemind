# Independent review (read-only, $0): a new reference for the final-answer test's control line

You are an independent reviewer for the hivemind project (repository `/Users/lchingen/hivemind`). Read-only: edit nothing, run no model
call, start no run. Your report is a lead. Every finding cites the file and the line it rests on.

**The task.** Alex chose (D658) to rewrite the reference of the final-answer test's control line (Stage B line 3, D428) for the questions the
new system asks. The design is `NEW-REFERENCE-DESIGN.md` in this folder. Review it against the primary material, not against the design's own
summary:
- the decisions: search `/Users/lchingen/hivemind/docs/DECISIONS-log.md` for "## D658 ", "## D592 ", "## D575 ", "## D428 ", "## D430 ",
  "## D261 ", "## D262 " and "## D3 ";
- the frozen judgement ruler: `/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/ruler-v1.md`, `reader-brief.md` and
  `questions-v1.json`;
- the line as built: `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/control_theses.py`, `control-reader-brief.md`,
  `STAGE_B_RESULT.md` and `CONTROL_TRACE.md`;
- `CENSUS.md` and `DESIGN-SHORTFALL.md` in this folder;
- `/Users/lchingen/hivemind/AGENTS.md` §7.1 (the frozen ruler, "A new gold").

**Out of scope:** the ladder step's prompt, gate 1, cost, and any change to the frozen ruler's files (they must not change).

**Answer, in order:**
1. **Does the design do what Alex chose** (D658's question and options, in the record), and nothing wider? Does any part edit, or weaken, a
   frozen piece?
2. **The material.** Is the frozen 14-day packet right for this reference, rather than the evidence the judge was shown? Name what each choice
   measures and what it cannot.
3. **The reference rule.** Reader B's answer as the reference, A as the noise record, third readers on every disagreement, splits to Alex. Is this
   sound under AGENTS §7.1, D262 and D658? Which alternative, if any, is better, and why?
4. **Fitting risk.** Can the reference be fitted, knowingly or not, to the judge's stored answers, at any step (build, read, reconcile, sign,
   shown-check, score)? What closes it?
5. **Population and timing.** Is applying it first to the stored baseline (questions written by the luna configuration) worth doing now, or does
   only an astra Stage B run decide anything? What would each result change?
6. **Missing rows.** Anything the state × event table or the procedure leaves blank. For example: a control whose question the system wrote with
   rungs that leave a gap; an event's "Ruled out" rung; the material-shown check for a reference with no decisive items; no_view; Ohio.

End with one line: `READY` or `NOT READY: <the smallest change>`.
