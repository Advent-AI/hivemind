**Seeded questions are the right first diagnostic, provided we describe it as a test of evidence delivery and judgment—not a full test of the clean product.**

For example, supplying an operating-margin question lets us see whether c8 delivers the facts needed to answer it. It cannot show whether the clean system would have opened that question itself. The seeds also change the context c8 reads, so a score against the old system is informative but does not isolate one change.

1. **The seeded test:** Use the 22 questions only in an isolated measurement library, with the existing judge as a measuring tool. Report unanswered questions and q23 separately, alongside the final score. D370 retired those presets as an active starting library; it does not establish that Alex approved using them as a test fixture. [D370](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3998)

2. **Scoring only self-opened questions is premature as the main test.** It would omit questions the system failed to open and could make its result look better. A reviewed mapping can be a supplementary analysis, showing which questions were opened and judged. The existing scorer still requires all 22 seed questions even when a mapping is supplied. [Scorer](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py:36)

3. **Alex should decide:** may we temporarily supply the 22 historical questions in an isolated test to measure whether the clean steps deliver useful evidence to the existing judge? My recommendation is yes, with the result labeled as conditional on those questions being supplied.

4. **I would not adopt the proposed rule.** Requiring every improvement to predict a flipped judgment is too narrow: a fix may prevent a false attribution or preserve a qualification without flipping one of these particular answers. Instead, require each proposed change to show its expected effect on the reader or final judgment, and test that effect where possible.

**Recommendation: close Step 1 on c8 and ask Alex to authorize the isolated seeded diagnostic as the first end-to-end test.**