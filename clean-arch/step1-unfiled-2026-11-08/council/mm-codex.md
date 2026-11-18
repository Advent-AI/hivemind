**My recommendation is to investigate how the clean path chooses the period of a question, starting with the missing 2027-versus-2026 memory comparison.** It is absent in all three clean draws and all three production draws. A repair that restores the right comparison could give the final judge a question to answer in three more clean draws. That is an upper bound, not a measured gain: we do not yet know that the facts would reach it or that its answer would agree.

I would not adopt Claude’s deadline-code proposal yet. The regulatory default is in the standard, but choosing the original product deadline and identifying a later slip require reading and judgment. The clean census also gives that proposal a smaller demonstrated opportunity than the missing memory question.

1. **Census recount**

   I checked the production matches and the 23 matched-question records in [eligibility-facts.json](/Users/lchingen/hivemind/poc/data/clean-e2e-comparison-2026-11-13/eligibility-facts.json), the independent eligibility answers, and the clean path’s [control count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/result/control-count.txt). Applying the stated outcome order to the seven graded questions gives the same totals as [RESULT.md](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/RESULT.md):

   | Outcome across three draws | Production | Clean |
   |---|---:|---:|
   | Agrees | 3 | 4 |
   | Not opened in the reference’s shape | 7 | 9 |
   | Opened with a different deadline | 6 | 2 |
   | Opened with different scope or only part of the question | 3 | 4 |
   | Unresolved | 2 | 2 |
   | **Total** | **21** | **21** |

   Per draw, the agreement counts are **1, 1, 1** for production and **1, 2, 1** for clean. The two production unresolved cases are q13; the two clean unresolved cases are q08 and q18 in the first draw. The clean control file lists matched questions; the absence classifications also depend on the recorded matching, so they are not established by that file alone.

   The claim that every *eligible* graded answer agrees is supported. It does **not** establish that judging is generally sound: only seven answers were eligible across both paths, and the outcome procedure stops at opening before tracing missing facts. Separately, Stage B did not pass, and its control line had only four eligible questions with the required material shown, below the eight required. The two systems ran on different days, so this is an exploratory census, not D427’s same-day acceptance comparison.

2. **Candidates ranked by expected effect**

   1. **Question period and comparison selection.** q05 is missing in **6/6** draws, including **3/3** clean draws. q04 is also missing in two clean draws and q13 in one. These are potentially different mechanisms, so I would first trace the memory question rather than assume one fix covers them all. D441 is a strong warning: the previous year change separated capex years but moved the memory comparison toward 2026; it stopped after opening memory questions less often, **17/54 versus 28/54**. Do not retune that failed change on the same articles. [D441](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4885)
   2. **Event date and scope selection.** In the clean path, q18 has one wrong-deadline loss, q23 one, and q08 has two scope losses; its first draw is unresolved. Even a perfect date-only repair cannot recover q08 where the question also restricts the people who may import. Production’s six deadline-only losses show a substantial broader problem, but they do not prove the same upside for the clean candidate.
   3. **Obligation scope.** The clean path misses q09 in all three draws: two questions cover only part of the total and one is not opened in the required shape. It may have comparable upside to memory, but the census alone does not establish a common repair or whether broadening would produce the right analyst question. Trace the source and existing plan first.
   4. **Final-answer and ladder defects.** These remain required for production readiness, even though this seven-question census found no eligible disagreement. Stage A has not passed; Stage B’s last-answer line misses on the strictest reading, and its control line was unexercised. The census is too small and selective to dismiss those defects. [Current state](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:276)

   The cheapest next test is a **read-only replay and trace of the stored memory cases**, including the article, the full request, raw answers and subsequent question creation, with the stopped D441 results beside them. Count how often each distinct mechanism occurs and check nearby comparisons that must remain separate. Only propose a repair if one mechanism explains the losses; then replay it on stored cases and check whether it also damages the capex and other period questions.

3. **Claude’s deadline rules**

   - **Pending regulatory decision:** The [standard’s §3 E](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:280) says an undated pending regulatory decision uses the current fiscal year-end and marks it as a researcher-set check date. That conditional default is explicit. Calculating the year-end from a correctly identified fiscal calendar can be deterministic. Deciding whether the source actually has no applicable date, whether it is a pending regulatory decision, and whose fiscal calendar applies still requires interpretation. q08 also has a scope error, so correcting its date alone would not make those two production questions eligible.
   - **Product node:** The standard asks about the revenue-producing milestone and says that, **while an earlier-deadline question is open**, a later deadline is evidence; a successor is opened after expiry if the matter remains active. [Standard §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:345) It does **not** state a general rule that code must always select the original planned date when the first article already reports a slip. Determining which milestone is revenue-producing, whether two dates refer to the same event, and whether a prior question exists are not mere date arithmetic. Applying “planned date” to every such case risks fitting the Kyber example.
   - **Unsigned obligations:** Claude is right to leave the model’s date unchanged under this proposal. The standard permits a check date **within 18 months**; it does not prescribe June 30 or a universal exact day. Code can check the bound and date shape. Selecting a meaningful check date remains a judgment.

   Before implementing any date rule, run it at no cost over **all stored event questions**, not just the three examples. Compare the source, existing open question, proposed date and final question; include explicitly dated regulation, undated regulation, already-slipped products, multiple independently bettable milestones, and obligations. Stop if the needed inputs are absent or ambiguous, if it changes an already-open question’s identity, if it fails to improve the decisive real case, or if it moves other valid questions to unsupported dates. A higher count against these seven questions alone is not sufficient.

4. **q23**

   This is a **measurement concern to disclose under D373**, not proof that the product chose an invalid date. The standard allows an unsigned obligation’s check date within 18 months; the reference chose June 30, while production chose July 1 in two draws and December 31 in one. Those dates can all satisfy the standard while failing the exact event-deadline eligibility rule.

   D430 explicitly requires exact event deadlines for Stage B controls, and this census adopted that rule in its design; its stated scope is Stage B, so its application here is a **measurement choice**, not a new product requirement. Exact dates also matter substantively: a signing on July 1 can make the two answers differ. Record the limitation beside the unchanged score, distinguish the one-day and six-month differences, and do not silently treat either as the same question. [D430](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4784), [D373](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4023)

Council position: Investigate the missing memory comparison first; do not implement the proposed event-deadline code without a broader source-to-answer trace and counterexample test.