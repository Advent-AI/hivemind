**Choose (a), with a narrower first question: can typed fields expose a wrong question without rejecting a correct one?** I support a $0 audit, not a decision to build a new Step 1 version.

For example, a field saying “2027 compared with 2026” could distinguish a comparison from a two-year span. But a field cannot decide by itself whether the analyst should open that question, or whether two facts describe one investment question. A typed answer can also repeat the model’s mistake in a tidier form.

The audit should read the stored source and answer for every affected case, plus correct questions and the D441 memory and capex neighbours. For each proposed field, show:

- What value the existing answer actually supplies, including **unknown** or contradictory values.
- Whether code could detect the error from those values alone, without a human supplying the right interpretation.
- Whether detection would merely refuse an answer or could recover the missing question.
- What correct questions the check would reject, and what each rejection would cost the final judgment.

Include the failed Stage A examples, but do not count all five as upstream defects: [the original diagnosis](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:57) identifies two of the three “two figures” declines as **Step 4’s wrong refusal**, even though the input mentions a second figure. The typed event change also accompanied three other changes in Stage A; its result is useful evidence, not proof that a typed Step 1 contract will work.

I would fix two accounting issues before using the trace to select a design:

1. **The “seven breaches” count does not reconcile with the table.** Excluding the two memory cases where the reason is described as a breach but the opening decision remains judgment, the table labels three capex, one memory, two Ohio and three financing cases as breaches: **nine**, not seven. The two financing questions described as parts of a total also need particular care: the earlier [control trace](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/CONTROL_TRACE.md) leaves open whether the narrower programme is a product error or a consequence of the broad matching rule. Reconcile the cases against the standard rather than simply changing the total.
2. **The q18 correction needs a procedure check.** [Design v4](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/DESIGN.md) lists unresolved eligibility before “not eligible.” If the family split is on the same-question part of eligibility, the new rule that a different deadline settles the outcome may be sensible, but it must be shown to follow the frozen procedure or disclosed as a departure. Report both counts until that is resolved.

I would not go directly to (b): D426 stopped further tuning on those 44 theses, and the evidence does not yet show that revisiting Step 4 is the highest-impact repair. The audit may instead show that some errors belong there.

D414 demonstrates a narrower success: once the relevant annual period is already identified, code can calculate a consistent date. It does not establish that code can choose the period, identify the same obligation, or decide whether a comparison deserves its own question. c11 is also a warning rather than a verdict against every schema: its required field was accompanied by other wording, stored answers lacked the field, and its small probe had regressions. [c11 record](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:2020)

**Stop the typed-unit line** if the audit needs invented field values to demonstrate a catch, mainly produces refusals without a path to recover the question, or cannot distinguish correct comparisons and related evidence from invalid combinations. A $0 audit can establish feasibility and risk; it cannot establish how a model would fill a new schema or the effect on final judgments.

Council position: Audit a narrowly specified typed-unit contract on stored losses and correct controls before deciding whether any new Step 1 version is justified.