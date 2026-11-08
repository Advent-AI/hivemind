**The design is not ready for the probe.** For example, it would count a margin figure as successfully handled even if it was left unlinked, although Alex said to put it under the existing revenue view.

The [round 3 findings](clean-arch/step1-unfiled-2026-11-08/council/o-codex.md) now stand as follows:

1. **Scope — mostly resolved.** Retention is limited to useful figures; the final request still needs to apply that limit.
2. **Later linking — improved, not fully resolved.** The cap is gone and failed comparisons have a retry plan. The independent case-by-case probe does not specify a check that retained figures actually reach a later view.
3. **Fields and readers — mostly resolved.** The missing handoff fields and balance classification are specified.
4. **Events — mostly resolved for this probe.** Persistence is explicitly outside its scope; the later-link check above remains open.
5. **Value check — not resolved.** A substring can still match the wrong number: `2.1` passes inside `12.1`. An unlinked useful figure can therefore be kept with the wrong value. The check needs a defined numeric boundary and a real-data check for valid formats it rejects.
6. **Evaluation — not resolved.** The reference is specified but not shown as independently reviewed; the scorer test is still a prerequisite, not evidence of a passing test. Also, “zero in 14 of 16 cases” remains ambiguous across three draws despite the instruction to sum them. Define how a case passes across its draws.
7. **View definition — resolved.** §11.3 consistently includes competitive position.

Two further serious evaluation gaps remain in [§11.4](clean-arch/STEP1-CONDITIONS-DESIGN.md):

- **Margin:** [Alex’s ruling](clean-arch/step1-unfiled-2026-11-08/LOG.md) requires filing it under the existing revenue view. The reference accepts an unlinked condition instead, so it can pass a failure of that ruling.
- **Unwanted material:** the supplier anchor checks only that no thesis opens, although Alex said to drop the supplier statement. The cash ruling is also absent. The probe could pass while retaining either as a condition.

Wording: update the arm description to include §11, which takes precedence over §10.

**NOT READY — blockers: verify later linking; fix the value boundary; complete and independently review the evaluation reference, scoring test, and three-draw decision rule; and test the margin, supplier, and cash rulings as decided.**

