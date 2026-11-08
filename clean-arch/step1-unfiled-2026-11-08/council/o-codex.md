**The design is not ready for the probe.** A useful forecast can still fail to become evidence for a later view, and the proposed evaluation does not yet tell us how to judge the result.

For example, if 61 figures are stored, the relevant forecast can fall outside the 60 candidates. A failed comparison can also leave it unlinked permanently.

**Round 2 findings:**

1. **Scope — mostly resolved.** The design limits retention to figures judged useful in context. The final request still needs to apply that rule.
2. **Later linking — not resolved.** The larger search and one retry reduce the gap, but the 60-item limit and a twice-failed batch can leave relevant figures unlinked. No later recovery is defined.
3. **Fields and readers — mostly resolved.** Section 10.3 specifies the missing source fields, separate dates and handoff; balance is now an actual.
4. **Events — partly resolved.** The no-view search and missing events are specified. The unresolved later-link failure remains; persistence is explicitly outside this probe.
5. **Old checks — not resolved.** The digit-group check does not establish that a value matches its passage: `1.2` can pass against `2.1`, and digits may come from different passages. It can also reject equivalent presentations such as billions versus millions. This can wrongly keep or discard figures.
6. **Evaluation — not resolved.** Section 10.6 sets populations and thresholds, but the new reference is still described as something to be created and reviewed. The scorer test is specified, not demonstrated. The rules also do not say how the three draws are combined for the thresholds, so different readings can produce different decisions.
7. **View definition — improved, still needs a boundary.** Section 10.7 distinguishes a past explanation from a testable view, but requires movement of a financial quantity while §3 also includes competitive position. The build needs one consistent definition.

**Wording:** The document title says v2 while its status says v3.

**NOT READY — blockers: incomplete later linking, an unreliable value check, and an unfinished evaluation reference and scoring rules.**

