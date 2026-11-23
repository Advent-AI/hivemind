**The trace found a worthwhile lead, and one more $0 step outranks closing the path: check the stored same-day duplicate candidates against the already-approved per-article visibility rule.**

First, correct the RTX timing. `e331`, the reported late-December shipment target, was written at article **184 on September 27**. Both RTX questions were judged at article 186 that day; `v14`’s September 27 answer already cites the shipment target, while `v15`’s does not. `v14` was judged again on September 28 and `v15` was not. The result page’s statement that the shipment report **arrived September 28** is wrong. [RTX packet](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/duplicates/pair-rtx.md)

The recorded reader difference is real: the separate reader marked `v15` unsure about the deadline and `v14` supported while citing the shipment target. It is an **association**, not proof that the target alone would have changed the reader’s verdict or either judge’s answer. A shipment *aim* is also indirect evidence about approval, not evidence that approval occurred. The two questions differ: `v14` names Alibaba and ByteDance; `v15` asks about domestic firms.

On the other RTX facts:

- `e284` contains the executives’ expectation about U.S. restrictions. Both teams considered it relevant by inference to whether the purchase could happen.
- `e278`’s stored summary says the plan was not confirmed, but the quoted passage printed beside it does not itself establish that detail. The other answer already describes its reports as unverified. Check the full article before treating this as a distinct missing fact.
- `e331` is the clearest distinct timing lead, with the qualifications above.

**The 16 fiscal-2028 facts are reader leads, not 16 established losses.** Codex marked 31 of 34 listed facts as bearing, including broad demand context; Claude marked 16 of 29. Agreement on an evidence ID does not always establish agreement on the exact claim or show that it is absent in substance. Four linked statements were not printed in one request, and neither reader could assess those from the packet. The result should retain the counts as *what the readers listed*, without turning them into a delivery-loss rate.

The decision-page sentence also needs tightening. “No pair’s answers differ in band” is misleading for revenue amount versus growth: **both chose their second answer, but those bands use different units and boundaries**. Say that the two RTX and Rubin answers chose “yes,” while the revenue answers chose their respective second bands; no answer change from supplying missing facts was tested. “The less-informed answer” should be “the answer without the shipment target.” [Decision page](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-15.md)

On the same-day explanation, “consistent with the day-start snapshot” may stand as a lead, not a traced cause. The matcher also builds search candidates and combines them with shown questions, so the snapshot alone does not prove why `v14` was omitted from `v15`’s comparisons. [Matching path](/Users/lchingen/hivemind/src/hivemind/views/round.py:104)

There is also a material decision correction: **D375 superseded D251.** Alex explicitly chose that each article see questions committed before that article, including earlier questions from the same day. D375 says implementation and acceptance remain pending; it does not mean the frozen default already behaves that way. Thus a $0 investigation of this known gap follows an existing product decision. It does not by itself authorize changing the frozen default. [D375](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4034)

I select the following bounded step:

1. Read the **same-day candidate pairs already found** in the fresh and three July runs. For each, establish whether they are truly duplicate questions under the existing decisions, then trace the later candidate’s actual search list, day-start list, matching record and outcome.
2. Count confirmed cases separately from distinct-period questions, unresolved pairs and candidates the search already compared. Treat the shared-group search as a **candidate list, not a complete census**, unless its completeness is independently established.
3. For confirmed missed comparisons, check whether the earlier question was committed and open before the later article. Record separately whether evidence was split and whether any final-answer consequence is shown.

**Stop:** if the candidates are not duplicates, the earlier question was already compared, or the stored records cannot establish the visibility path, report that result and do not design a correction from this lead. A confirmed visibility gap would justify bringing a **D375-aligned stored-data proof** to the council as a separate decision; it would not itself prove that the answer changes or that a new version is ready.

I rank this above packaging-and-waiting because it tests a named, previously authorized behavior on already-paid records. I rank a correction proof below it until the cases and mechanism are verified. No paid run is needed for this step.

Council position: Correct the RTX date and the decision-page wording; trace the stored same-day candidate pairs against D375 and the actual matching path at $0, with no frozen-piece change or paid send unless the council separately reviews the resulting evidence.