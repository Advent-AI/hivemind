The core problem is that **the new system cannot reliably turn an important, complicated matter into a question it can actually answer**. For example, it opened cloud-company spending as one topic covering two years, then declined to answer it because neither year was identified as the main one.

This is deeper than a faulty refusal: the first step writes the topic, and the later step must turn it into one answerable question. Their rules do not yet provide a reliable way to handle a matter with several independently meaningful parts. I would treat this as the **leading explanation for the latest failure**, not as a proven explanation for every product defect. Facts failing to reach existing questions remain a separate, established problem.

The evidence carrying that conclusion is:

1. **The product goal is an answer informed by the facts that can change it.** That is the phase’s stated end-to-end goal; it is not enough for a step to keep facts or write plausible-looking questions. The same document establishes an earlier filing failure in the old system: indirect facts were missed, while the judge could reason from them when shown them. That is measured evidence for the old path, not proof that every failure in the new path has the same cause. [Filing phase, §§1–2](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md)

2. **The latest week shows the problem directly.** One run opened 13 topics; the answer-writing step declined 9 of 39 attempts across four topics. Both spending topics covering two years were declined in all three attempts. The matching and judge were not run, so the effect on final answers was not measured. The view that cloud spending deserved a question is a reader’s judgement. [Second-week result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/RESULT.md)

3. **The refusal is partly the agreed design working as written.** Alex chose to judge the main part and decline a topic with no main part; the cost of leaving two real bets unanswered was recorded as an open defect. He also chose to keep two sides of the same bet together. Those choices do not establish how to handle two separately tracked years. This is a design boundary, not evidence that the model simply ignored an instruction. [D397 and D436](/Users/lchingen/hivemind/docs/DECISIONS-log.md)

4. **The problem recurs, but its size is not a general rate.** Across stored material, six topics whose question asked two things were declined in all three attempts. A separate boundary study identified cloud spending and a memory price as two worthwhile matters lost outright; other cases were disputed or judged not worth opening. These include repeated news and different readings. [Result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/RESULT.md), [boundary study](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/NO-MAIN-BOUNDARY-STUDY.md)

5. **Other faults are real and prevent a clean pass.** Agreed errors include a question that lost the guarantee’s name and omitted parts that should be shown as unjudged. Across four readings, the kinds of agreed fault changed; the record does not demonstrate one repair that removes them all. An audit also found that “the topic’s wording” is undefined in the request. This weakens any claim that multi-part topics are the sole technical cause. [Gate map](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/FIRST-GATE-MAP.md), [prompt audit](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/PROMPT-AUDIT-TWO-CLASSES.md)

6. **The new system has not shown an end-to-end win.** In the July comparison, it retained 51 of 55 decisive facts for its lost questions, yet lost those graded answers before judgement; the old system also lost at opening. The comparison was small, with unresolved reader disagreements, and does not rank the systems. [Full census](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md)

**What would show I am wrong:** a source-by-source reading of the stored declined topics showing that the apparently separate parts are usually one bet, not worth tracking, or already answered adequately elsewhere. Equally, if the missing questions would not affect any useful judgement while a different recurring failure does, that failure should take priority.

**The last two days partly aimed at this, but also circled.** D466 explicitly stopped repeated sentence changes after the score did not move; D473 and D479 record further failed candidates. D483 then correctly shifted attention toward what a reader receives. The recent week and D555–D558 exposed the connection between topic shape and refusal, but the subsequent search for small fixes to separate answer-writing faults has not produced a product-relevant repair. D544 chose the new path as the direction of work, not as a demonstrated better system. [Decision log](/Users/lchingen/hivemind/docs/DECISIONS-log.md)

Candidates I considered and rejected as the *one* core problem:

- **“The judge is wrong.”** The latest diagnostic did not run it; earlier evidence is insufficient to make that the main cause.
- **“Facts are not delivered.”** Confirmed in individual new-system cases, but not shown to explain the latest missing questions. [Lean log, §§11–12](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/LEAN-LOG.md)
- **“The pass rules are too strict.”** Some readings are disputed, but agreed faults remain even on the favourable reading.
- **“Just split every topic.”** The boundary study shows that this would also produce questions about matters readers judged unworthy.

**One next step:** a $0, source-by-source review of the stored declined matters, including the unworthy controls, to decide which parts an analyst would track separately and whether each could become an answerable question without creating trivia. Its falsifier is that the worthwhile multi-part matters cannot be distinguished from the controls by an independently reviewable reason. This would inform a design; it would not prove a change works.

The product choice is Alex’s: **when one important matter contains two separately tracked figures, should the product show one topic with two judged questions, open two topics, or leave it unanswered?** I recommend one topic with two judged questions when the figures are genuinely separate bets, while keeping two sides of the same bet together. That recommendation needs the stored-case review first. Finishing the latest week would test the answers that exist, but its own design says it cannot answer this missing-question issue. [Completion design](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/COMPLETION-DESIGN.md)

Position: The highest-priority unresolved problem is the handoff from an important matter to answerable questions; its full product impact remains to be established.

