**The page is close, but it needs several corrections before Alex reads it.** The most important is that D513 describes the new system’s look-back rule too broadly: the code checks whether a statement group’s **original record arrived without a link**, not whether the group has no link now.

For example, a group that arrived unlinked can gain a link later and still be considered for another newly opened question. Conversely, a group whose original arrived linked is excluded even if a later member has different links. The code works on groups, not every individual statement. [Later-linking code](/Users/lchingen/hivemind/clean-arch/step3/library.py:77)

**D513 and the page’s look-back claims**

D513’s core correction is right: the system does look back, and the stored run records seven checks, 516 group–question judgements and two later links. The specific missing fact is also consistent with the code: its group, `163:e3`, arrived linked to `clean-3`, so the later check for `clean-7` did not reconsider that group. The stored record uses `163:e3`; `e379` is the judge-side identifier. [Stored library](/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week-r2/c1/step2/library.json)

Please correct D513 and the page from “every earlier statement with no link” / “one already filed elsewhere is not looked at again” to:

> When a question opens, the system checks earlier groups whose original statement arrived without a question. A group whose original arrived under another question is excluded, even if the new question also needs it.

Also qualify “is judged”: failed batches can remain pending and be retried. They did not remain pending in this stored run.

The old-system sentence also needs care. D456 found **no links back to earlier records** among 3,225 links in six draws. A later article can repeat the same fact and deliver it, which happened in the traced Kyber example. Say “does not link the earlier record,” rather than “never receives what came before.” D456’s no-answer-loss conclusion is limited to the eligible, graded questions and stored window; it is not a general finding about all unlinked facts. [D456 trace](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md)

**Other page corrections**

- **The six answers:** only the three answers that received the added fact could mark it against “yes.” Say “all six stayed ‘yes’; all three given the fact marked it against ‘yes’.”
- **“Has been run only by its own test scripts”:** I cannot establish that exhaustive claim from the records read. Replace it with the supported, more useful fact: **the clean path is not integrated with production storage**. [Clean README](/Users/lchingen/hivemind/clean-arch/README.md)
- **Opening losses:** the claim is supportable with its boundaries, but cite D452–D455’s census rather than D456 alone: on **seven graded questions in the July comparison**, no eligible judgement disagreed with the frozen reference; recorded losses occurred before judging under the study’s ordering. Some matches and eligibility calls were unresolved, and production also had missing links behind opening losses. Avoid “both systems generally lose most at opening.” [Full-run census](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md)
- **“235 articles … starting with no questions”:** supported for this comparison. The 232/3 exposure disclosure is correct.
- **“389 … so shown to no judge”:** retain the week-end condition in that table label: “389 had no question at week’s end.” The existing count does not independently prove what every earlier request contained.
- **“The old system is the one running today”:** the record establishes the **replay default**, not live service status. Name it as the current default configuration unless live operation is independently verified.
- **“The product gives no direct answer … at all”:** say the **new system gave no separate answer on those figures in this week**. D505 governs their treatment, but “at all” is broader than the observed run.

**Advice and comparison**

The revised advice is supported: keep the default, keep both paths, and do not infer a winner. I would soften **“ten small steps … none could move this choice”** to “ten small steps taught us about financial figures and delivery, but did not decide which system to carry forward.” Some steps could have produced decision-relevant evidence; their actual results did not decide it.

The comparison is described at the right level for Alex to authorize **designing** it, provided the page says a design could still conclude the proposed test cannot distinguish the systems. Three runs per system show some variation; they do not guarantee a decisive comparison or replace the clean path’s existing acceptance requirements.

I would **remove “in the order of $17.”** It is a linear extrapolation from a one-week, one-draw setup; a two-week run may have different article counts, growing context, retries and charges. The earlier two-week proposal estimated about **$22 with a $35 reservation ceiling**, using different assumptions. Neither is a validated estimate for the proposed design. Say the cost and ceiling will be calculated from the selected articles and reviewed before any send. [Earlier design](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/ACCEPTANCE-DESIGN.md)

For plain words, replace “registered comparison” with “a comparison whose questions, pass conditions and budget are written down before it runs.” Replace “frozen” and “acceptance” with “kept unchanged for comparison” and “has not passed its required tests.” Explain “statement group” only where needed for the look-back example.

**The page is ready after these named edits**, rather than as version 2. The advice itself need not change.

Council position: Keep the revised advice and prepare the comparison design for Alex; correct D513’s original-record eligibility rule, the six-answer wording and the bounded historical claims, and remove the unreviewed $17 estimate before leaving the page for him.