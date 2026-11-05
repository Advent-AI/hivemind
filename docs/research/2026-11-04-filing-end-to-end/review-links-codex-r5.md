**The filing text and request builder are ready, but the amended decision rule is not. Three serious issues remain.**

1. **Two new noise statements can escape review entirely.**  
   The script reviews increased noise only when the question’s total increase has `p < 5%`. In an in-memory diagnostic using stored statements, I added two irrelevant DeepSeek statements to the Vera CPU question in two of three answers. Noise rose **0 → 4 links**, but `p = 19.925%`, so neither statement reached the reader. All aggregate development checks still passed. The proposed “two noise statements fails” rule cannot protect cases its reading list omits. [Review trigger]( /Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/decide.py:140)

2. **“Sampling” and “caused by the new rule” overlap.**  
   The calibration already contains the problem: for rack-price fact `i216`, the definition-only variant sends it to the correct question once, the wrong question once, and nowhere once; control delivers it correctly **3/3**. That satisfies class (b), because another variant answer files it correctly. It can also satisfy class (a), because an instruction causes the wrong filing. No precedence or evidence requirement resolves that conflict. Independent readers can therefore excuse or count the same loss. Occasional success does not establish that the rule caused no harm. [Classification definitions](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:36)

3. **Class (c) exempts incorrect moves, not just unavoidable one-home choices.**  
   Its definition requires only that the receiving question also uses the fact in the gold. It does not require that the move obey the narrowest-question rule. I checked two stored product-launch facts, `i219` and `i133`: moving their links from the launch question (`v7`) to total revenue (`v1`) loses **two distinct facts**, previously delivered **3/3** and **2/3**. Both qualify for class (c), because the gold also uses them for total revenue—even though choosing that broader question violates the proposed filing instructions. These losses would be explicitly exempted. [Exemption](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:38)

The other requested checks passed: call 204’s split preserves both links after production merging; the three new examples introduce no serious inconsistency; all **69 original requests and 138 arm requests** rebuilt successfully, with only the specified description and three role edits changed. The earlier **v9 17 → 9** counterexample now reaches review through three individual fact losses.

The test is **not ready** until the review list covers sparse noise increases and the three classifications cannot excuse rule-caused harm.

No files were edited and no model calls were sent.