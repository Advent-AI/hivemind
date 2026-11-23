**I withdraw my proposed audit as the next step.** The stored facts support Claude’s objection: most of the examples I checked would not help answer the seven questions the clean system actually opened. Checking more of them against those same questions is unlikely to decide how the reader should see Nvidia’s main numbers.

I recommend a different $0 test: reconstruct a small, source-checked financial record from the facts already kept, then see whether it gives a reader a usable picture of revenue and margin. This tests an existing Alex-approved use of the facts and gives the council evidence before it decides whether to pursue standing questions.

### 1. What the unread facts can decide

I sampled 24 of the 382 unlinked statements in the [clean judge store](/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week-r2/c1/judge/draw-c1/views.sqlite), including company figures as well as other statements. The sample includes:

- `e206`: the $406.05 billion FY2027 revenue consensus.
- `e553`: the $111.3 billion quarterly consensus above the company’s guided range.
- `e174`: AMD’s revenue and data-center results.
- `e212`: Microsoft’s planned deployment of AMD Helios.
- `e10` and `e245`: product and partnership announcements without a financial scale.

The first two help a reader understand Nvidia’s revenue expectations. The AMD items could inform competition or revenue analysis, depending on the question. None has an obvious direct bearing on the clean system’s credit-support, supply-commitment, China-permission, Rubin-shipment, hyperscaler-spending, acquisition-closing or RTX-approval questions. That is consistent with Claude’s sample, although my sample has a different population and does not independently verify his 13/17 counts.

My original audit could still identify an occasional missed link—for example, a supply figure that actually changes the answer to the commitments question. It **cannot decide how to track annual revenue and margin when no such question exists**. I should have recognized that before recommending it.

Alex already approved keeping useful company figures with their type, source and period, using them as evidence when a related view opens and as a reference for judgements. That gives us a concrete reason to test the record itself. It does not settle whether a financial record alone replaces a question. [Step 1 log §17](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:472)

### 2. Challenge to Claude’s standing-question test

The comparison would test a real but narrower question: **does adding these particular four questions to c8’s existing library change what c8 opens and links on these articles?** It holds the article and request constant while changing the library. It would not isolate the cause of c20’s failure: c20 created revenue questions *during the same answer* under a different request, while this test presents them as already existing. A positive or negative result would be useful evidence about library state, not proof of why c20 made its decision.

The standing questions are presets in the ordinary sense. D370 removed the 22 artificial preset questions and retained actual existing research as context. D490 authorized a test of *opening* three financial questions from stored articles; it did not explicitly authorize adopting automatically generated standing questions. An artificial state can be used as a labelled diagnostic, but D490 should not be represented as approval for that product design. [D370 and D490](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3998)

The proposed test also leaves important gaps:

- It cannot guarantee no duplicate later: the model may open a differently worded revenue question despite a standing one. That must be read from answers, not assumed.
- Linking the company’s figures does not establish that peer news is correctly filed. At step 35, c20 linked a Sandisk revenue statement to Nvidia revenue; it needs a relevance reading, not a ban on all peer evidence. [Probe answers](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/main-numbers/answers-listing-stage1.txt:165)
- Four standing questions include FY2027 margin, although the original three target matters did not. Production’s dropped 74% margin guidance makes it worth examining, but its usefulness and scope must be judged, not presumed.
- The test does not show whether the answer-options step can construct usable answers or whether the judge can support its conclusions from the linked evidence.

The proposed stop line can fire, but it cannot reliably demonstrate safety with four or five sends. At five sends, **3/5 versus 0/5** meets “most to none,” despite substantial uncertainty; **4/5 versus 2/5** meets the pooled halving idea in a single cell. Conversely, a consequential reduction such as **4/5 to 2/5** need not trigger the per-case “most to none” rule, and pooling can hide one damaged question behind unrelated ones. Controls that do not open often enough must be inconclusive; a non-failure must not be called a pass without a predeclared tolerance and enough observations to distinguish it from c8’s spread.

Production’s article 35 is a fair **second observation of the same visible pattern**, not a second controlled test. Its stored handover opens no candidate and files Rubin full production under data-center revenue `v4`; its revenue questions were already present. But production uses a different request and a different library, including a segment question absent from the proposed four. It cannot separate the date doubt from the filing effect. [Production records](/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week/p1/prod/views.sqlite)

### 3. One next step

**Test: a $0 reconstruction of the financial record from the stored week.** Before reading outcomes, select examples covering FY2027 and FY2028 revenue and margin, including actuals, company guidance, third-party expectations, and repeated or conflicting reports. For each, trace the stored figure back to its article and record measure, company or segment, fiscal period, actual/guidance/estimate, original speaker, date, and source. Have an independent reader try to answer: “What does the company say, what does the market expect, and what changed?” Report missing, ambiguous and duplicated fields as well as usable ones.

**Refutation:** if the retained records cannot reconstruct those distinctions faithfully for the selected examples, or the reader cannot recover a useful picture without guessing, this route is not ready as the next improvement without first addressing the demonstrated omissions. A successful reconstruction would show **feasibility on stored data only**. It would not prove that a conditions record replaces revenue questions, changes a judgement, improves production, or satisfies a forward-run acceptance.

The standing-question experiment remains a candidate after this check, with its preset status and product implications explicit. It should not be launched under this read-only assignment.

Council position: Withdraw the existing-question delivery audit as the next step; first test whether the already-kept financial facts can form a faithful, usable company record. The standing-question proposal is a useful diagnostic of library-state effects, but neither its proposed stop line nor D490 establishes that automatically preset questions are safe or approved for the product.