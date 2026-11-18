**Do not send c16 as frozen.** Version 2 addresses several problems in the first audit, but the selected cases do not exercise the central comparison guard, and the decision rules can report a pass when the candidate’s answers are refused or the duplicate checks are unexercised.

For example, none of the three “two-year comparison” cases asks the model to open a valid shared-price question comparing one year with another. Two are marked “link” and one “nothing to open.” A candidate that opens no comparison question at all could therefore pass that guard. [Selection](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/identity-probe/selection.json:90)

1. **Version 2 needs a blind re-audit.** It narrows population, removes the unsupported company examples and makes the unsigned-deal example conditional on materiality. Those changes answer several first-audit findings. But the available blind audit is of **version 1**, so it does not establish that version 2 is consistent. [First blind audit](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/identity-probe/audit-c16-blind.md)

   Two specific points need review:

   - The new “same thesis” class begins **“when the same result settles both”**, then includes a later deadline while an earlier one is open. A shipment by 2027 and a shipment by 2028 can produce different yes/no answers. The standard nevertheless says the later deadline is evidence while the earlier question is open; that boundary needs to be stated without making it depend on the same-result test. [Candidate](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c16-system.txt:125), [standard](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:348)
   - The candidate gives **two** examples for the “another thesis” class across two different boundaries—another year and an unsigned deal—not two examples for each boundary. Check the examples and categories against AGENTS §6, the whole request and schema. The text also still assigns comparison with the open library to Step 1, a departure from the standard’s allocation that the design discloses but does not resolve.

   The extra sentence about a comparison is grounded in the standard’s example, but it is still a hypothesis that the model will apply it correctly. The **1,694-character system-text growth** also needs a real cut-or-justify review; “cuts are levers too” does not show why no existing instruction can be merged or removed.

2. **The selected articles are too concentrated to support the stated general conclusion.**

   - The four T2 articles describe the **same OpenAI financing/backstop story**. Twelve sends are repeated samples of one underlying case, not four independent deals. They can diagnose that case but cannot establish general handling of unsigned transactions.
   - T1’s four articles repeat related hyperscaler spending forecasts, and every expected answer is “open.” Include independently sourced quantities and cases where a different-year figure **should not** open because it lacks independent investment significance or cannot be checked.
   - T3 has **no positive case requiring one new, valid year-over-year shared-price question**. Add such cases, plus cases that should link or should not open. Read both split and **dropped** valid comparisons; the current failure definition catches only two new questions or an improper new question.
   - T4’s expected links need case-by-case confirmation. In particular, forecast sales are not automatically identical to a first-shipment question; the source, outcome and independent significance must establish the relation.

   The selection hash matches the design, and the fixed July 14 library is a useful controlled input. It remains a **snapshot test**, not an evolving-library replay.

3. **The frozen lines can pass vacuously or give an unsupported verdict.**

   - **T4:** the design does not require any minimum number of its four articles to be exercised. All could be unexercised, yet the regression line would have no failures.
   - **T3 and memory:** a refusal or malformed answer counts as “no failure.” If c16 refuses every answer, it can appear to preserve comparisons and avoid duplicates. The memory guard can also pass **0 versus 0**, giving no evidence that the prior regression was avoided.
   - **Targets:** +4 of 12 is a 33-point difference, but the 12 sends in T2 repeat one underlying deal. The design gives no null or uncertainty calculation for +4, +2 or the guard thresholds. It can count repeated reports as if they were independent cases. A result of **+1 for both targets** is labelled failure even if the small sample cannot distinguish it from variation.
   - **Verdict:** one target can pass while the other is merely unchanged, provided it is not negative. That may be reasonable for a single-class exploratory probe, but it does not demonstrate the proposed clause improves *both* boundaries. State the class-specific conclusion and use **inconclusive** for inadequate exercise or sample evidence.

   Require successful, checkable answers in both arms; predeclare minimum exercised positive and negative controls; count valid comparison questions as well as unwanted splits; and make missing, refused or unrun cases **unexercised/inconclusive**, not successful guards. Keep each article and underlying story visible in the result.

4. **The preflight and spending claims need qualification.** The version-2 output says 30 cases build with only the two texts differing. It does not show the required `scripts/preflight.py` replay, its judged populations or skipped cases; the design still lists that as before-send work. A synthetic answer for one capex case also does not prove all expected response shapes pass the checks. [Version-2 preflight output](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/identity-probe/preflight-identity-v2.output.txt), [design](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/identity-probe/PROBE-DESIGN.md:68)

   **$2.65 is an estimate**, based on assumed token use. The probe harness reserves against a $4 run ceiling, but a request admitted before an overrun can finish afterward; an unexpected provider charge can exceed its reservation. The ledger is also local to that process. Thus **about $22.4 is the planned ceiling, not a guaranteed maximum**. Record actual cost, stop on an incomplete budgeted population, and do not score an interrupted probe as a pass. [Probe harness](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:132)

Before sending, revise the candidate, obtain a blind audit of **version 2 or its successor**, replace or augment the concentrated selection, and freeze a new reviewed design with exercised controls, meaningful denominators, explicit inconclusive outcomes and complete preflight evidence. Keep the repeatedly used memory and capex articles as regression guards, not tuning material.

**Council position: Do not send the frozen c16 probe; correct the identity wording, select cases that exercise both opening and merging, and review new decision rules and preflight before any paid call.**