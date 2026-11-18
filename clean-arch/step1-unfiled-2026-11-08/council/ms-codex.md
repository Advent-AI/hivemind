**The full run does not clear the path to production, but I would not skip Stage B on the reasoning given in the reflection.** The “at most five controls” count covers only the seven-question census. Stage B also includes three Rubin controls, which could bring the favourable count to **eight**. Their eligibility and, for two, whether all the material was shown remain disputed.

For example, one reader says the Rubin question requires confirmation by NVIDIA and is therefore narrower than reader B’s question; the other says confirmation only describes how to find the answer. That disagreement affects whether the control counts.

1. **Census and Stage A**

   The [census result](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md) is consistent with the saved [outcomes](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/full-eligibility-answers/census-outcomes.json) for the seven graded questions: settled agreements are clean **2/1/0** and production **1/1/1**. Including the disputed eligible answers gives clean **2/2/1** and production **2/2/2**. The saved rows support the reported opening and eligibility outcomes; the unresolved cases must remain visible rather than being treated as settled.

   The [Stage A report](/Users/lchingen/hivemind/poc/data/clean-e2e-full-2026-11-13/stage-a/report.txt) records 40 fresh theses and 120 attempts, with one attempt refused twice. Under the favourable and unfavourable treatments, its stored counts are **32/22** and **19/13** for “right / right by a ladder.” D452’s thresholds for 40 are **32 and 26**, so line 5 is missed under both treatments. The report also records lines 1–4 missed and line 6 met under both.

   There is an accounting caveat: the current [accounting code](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/accounting.py:190) still applies the original **35/28** thresholds when it prints the verdict. The verdict happens to be the same under D452’s **32/26** thresholds, but the printed verdict alone does not implement the agreed calculation.

   I did **not independently rebuild every reader packet and ruling**. In particular, I cannot independently certify the reported **79 matched inputs, 73 agreements, six matching disputes, 28 eligibility views, 17 eligibility disputes, 70 disputed Stage A marks, or 66 sends sent to third readers** from my read. The stored Stage A result does contain **41 unresolved points**, and I verified that count. The census report also does not itself print the promised literal due-day count alongside the full results; the individual saved outcomes contain literal-day labels.

2. **What Stage B could still decide**

   The run cannot be D427’s production acceptance: D451 explicitly made it diagnostic, and Stage A has missed its lines. But that does **not** make the fresh Stage B reading pointless. It could still establish whether the frozen judge’s answers on these fresh questions meet the separate figure, yes/no and final-answer conditions. Its earlier baseline used hand-written ladders; it does not prove performance on these fresh ladders.

   For line 3, the three settled graded controls plus two disputed graded controls plus **three disputed q07 controls** give a potential upper bound of **eight**, not five. The q07 answers agree with reader B if those controls qualify; two also have disputed material-shown marks. Eight is therefore a **favourable unresolved-case possibility**, not eight established controls. The settled count remains below eight, and the precise line-3 result needs the agreed treatment of those disputes and the reviewed fresh mapping.

   I would **continue the D452 reading**, including its controls and trial, rather than record line 3 unexercised as a settled fact or depart from the plan now. It cannot change this run into D427 acceptance, but it can change the evidence about whether the judge works on the new questions. [Stage B’s rule](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md:70) includes q07 and requires eight eligible controls with the material shown.

3. **The loss traces**

   **Read the extracted and linked marks.** The opening classification is correct under the first-applicable rule, but the agreed [census design](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/DESIGN.md:63) also requires each item’s marks and other applicable causes. Those observations can show whether fixing the question would expose a second problem: for example, the right question might then exist but still never receive a decisive fact. Calling the marks “not read” is an honest current limitation, not completion of the planned trace.

4. **Path to the production goal and the next angle**

   The sample does not show the clean path outperforming production. Both lose many of the seven graded answers because the required question is absent or differs in scope or deadline; among the settled eligible answers, neither has a recorded disagreement. That last observation concerns a small selected set and does **not** establish that judging is sound in general.

   Stage A separately shows that the new questions and answer choices are not reliable enough to meet their lines: even the favourable reading finds an answer choice that accepts every outcome and a price question turned into a threshold already crossed. The reader disagreements also leave material uncertainty about how several rules should be applied.

   My single next angle is **how a source becomes a question with the right scope and deadline**. First complete the planned loss traces, then compare the source, the question created, and its answer choices for the lost cases across both systems. The test is whether that trace identifies a general cause covering a meaningful share of the losses, including any downstream missing facts, before proposing a change. The current results identify where answers are lost; they do not yet prove the mechanism or a remedy.

Council position: Continue the committed Stage B reading and complete the loss traces; do not claim this diagnostic run can clear D427. Use the completed traces to investigate question scope and deadline as the next single angle.

