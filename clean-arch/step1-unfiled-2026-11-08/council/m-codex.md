**The design is not ready for a probe.** It captures Alex’s direction, but it does not yet say how a useful financial figure survives, reaches a later view, and is judged without losing its source or meaning.

For example, a forecast can be repeated by another outlet, revised by its author, and later followed by an actual result. Those are three different relationships; the draft does not specify all three.

**Serious findings**

1. **The scope exceeds Alex’s decision.** He approved keeping a *useful* company financial figure without a view. The draft defines every company measure as a condition and checks that all are captured. It needs the existing relevance judgment, including for cash flow; a fixed metric or industry list would be hard-coding. His earlier cash decision concerns the particular figures and context shown. [Design §§1–4](../../STEP1-CONDITIONS-DESIGN.md), [Alex’s decision](../LOG.md)

2. **The handoff to a later view is missing.** Alex explicitly said a retained figure becomes evidence when a related view opens. Step 1 sees open views, not saved conditions; the draft specifies no search, relevance judgment, link write, or reader for a view opened later. Step 4’s measure-and-period match cannot substitute for establishing relevance.

3. **Fields and readers are incomplete.** The record lacks a standalone statement, original speaker versus reporting speaker, source identity, tier, date text or unknown-date rules, and explicit scope and qualifications. Those matter for comparison, saving, and judging. “Actual = past period” also misses a current balance. Specify each field, its possible inputs, nulls, and every reader, including evidence and condition readers. [Existing handoff](../../PRD.md)

4. **The event table is incomplete.** Define distinct-party forecasts, restatements, forecast-to-actual, repeated processing, failed comparison, interrupted writes, concurrent writers and later linking. Preserve each repeat’s text and source, apply the existing best-match and tie rule, and retain revisions without overwriting history. A figure with the same value and party is not necessarily the same statement. [Repeat decision](../../PRD.md)

5. **The new path has no mapped checks.** Specify quote verification and unsupported claims, condition and thesis ID/link validation, empty links versus dropped evidence, and the unchanged retry-once format policy. Define how a mixed statement containing a financial figure and other evidence is represented without losing either part or duplicating it.

6. **Evaluation and the probe are under-specified.** Counting conditions as kept does not prove the old scorer can match them or that they reach its existing readers. Preserve historical scoring, test any adapter, and report separately what it measures; D373 still requires scoring unchanged and disclosing disputes. The new evaluation needs a sourced, independently reviewed reference before scoring. “Views not worse” and “noise not worse” need populations and decision rules. Both datasets have prior exposure. [Design §§7–8](../../STEP1-CONDITIONS-DESIGN.md)

7. **The proposed thesis definition is too closed.** Its list of mechanisms and requirement that the source itself state the reason can exclude a defensible analyst view. Alex asked for a reason, not that particular closed list. A financial measure with a stated reason can be a view; the do-not-open wording must say so. D208’s old seeded hierarchy is not restored by this design, and D370’s removal of preset questions and report import remains in force.

**Wording-level:** distinguish a reported actual from a forecast, and a forecast’s author from its reporter. Avoid calling the four rulings universal.

After these contracts are completed, a fresh independent review should recheck every row. **Only then can the small probe be designed; fixes to the prose alone do not make it ready.**