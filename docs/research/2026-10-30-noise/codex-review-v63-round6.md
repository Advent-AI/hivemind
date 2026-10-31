The current text follows the standard’s main test, but its drop examples can still steer the model to discard evidence the standard keeps. For example, a newly reported shortage can describe a long-standing situation and still be new information an analyst would record.

I audited only [review-core-v63.txt](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise/review-core-v63.txt) against [the Chinese version 4 standard](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html). I treated optional items as permissible to omit, as requested. The classifications below describe what the text instructs or risks; they are not claims that a measured run caused each error.

One point about the round-5 description: **the sentence beginning “Never drop a statement that touches …” is not in v63**, nor is it in v61. I cannot judge its exact wording from the current file. The current keep-list header is a general test, not an explicit restatement of §6’s core definition.

### Opening and newness test

1. **“Before you return the answer, check it once.”**  
   **Source:** §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”.  
   **CONSISTENT** — The final check is a procedure for applying the standard, although the standard does not itself prescribe a final-pass instruction.

2. **“Read each evidence item back as the analyst following the company and keep it when you would write it in this week's notes because it makes some question's answer more or less likely, about the company or its customers, suppliers, competitors, regulators or the economy.”**  
   **Source:** §5.1: “一个在追这家公司的分析员，读到会在本周笔记里写下来，因为它让某个问题的答案更可能或更不可能”; “客户、供应商、竞争者、监管、宏观都算”.  
   **CONSISTENT** — This carries the standard’s test and scope.

3. **“Ask first whether it is new: repeated common knowledge, a long-standing situation retold and an unargued view are noise”**  
   **Source:** §5.1: “判一句话之前先问：这是新信息吗？”; “重复常识、描述长期状况、泛泛的看法，是杂音”; “一个新的具体判断，是增量，不能漏”.  
   **WIDER-DROP** — “An unargued view” can include a new, specific judgment that §5.1 says to assess as new information, even if the article does not show its derivation.

4. **“guidance, and a forecast or a plan still in force, keep their place even when retold.”**  
   **Source:** §5.3: “重提的季度指引和仍然有效的预测、计划按本来分量”.  
   **CONSISTENT** — It protects the standard’s specified retold material, although “guidance” is broader than the page’s explicit “季度指引”; I cannot conclude from that wording alone that it necessarily keeps a rejected item.

5. **“These usually fail that check:”**  
   **Source:** §5.3: “不在清单上的句子，用 5.1 的规则逐句判”; §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”.  
   **CONSISTENT** — “Usually” makes the list subordinate to the analyst’s test, provided the individual rows and their boundaries are applied correctly.

### Drop list and every example

6. **“background the analyst already knew: an arrangement already in place, described again”**  
   **Source:** §5.1: “常识，就是跟这家公司的分析员读这篇之前就已经知道的”; §5.3: “已知事实的重述”.  
   **CONSISTENT** — A genuinely known arrangement merely repeated is within the standard’s background rule, subject to its retold-guidance and forecast boundaries.

7. **“the company's history”**, including **“the company was founded in 1998”** and **“the product line launched in 2020”**  
   **Source:** §5.3: “记者的背景和框架”; “公司成立于 1998 年”; “A100 2020 年上市”.  
   **CONSISTENT** — The examples are old history used as background, rather than newly reported product progress.  
   **Example provenance and generality:** The first example is on the page in translation; the second is an adaptation of the named-product example, not an exact page example. Both are general in wording.

8. **“A development the item reports without making clear that it is old is not a retelling”**  
   **Source:** §5.3: “抽取看不到库，只能从文字和日期看”; “看不出是旧事的不算重提”.  
   **CONSISTENT** — This carries the explicit boundary.

9. **“and a forecast is never one”**  
   **Source:** §5.3: “仍然有效的预测、计划按本来分量”; “看不出是旧事的不算重提”.  
   **NARROWER-DROP** — The text exempts every forecast from being a retelling, whereas the explicit protection covers forecasts still in force and material that does not appear old; a clearly expired, retold forecast is not given that blanket exemption.

10. **“a typical claim that is common knowledge, without a figure and a specific account: that a firm leads or competes, that demand is strong or supply tight”**  
    **Source:** §5.1: “谁领先、谁在竞争、需求强、供给紧、融资难这类说法”; “这类陈述没有数字和具体的叙事就不收”.  
    **CONSISTENT** — This matches the common-knowledge rule, but only when the claim is actually common knowledge.  
    **Example provenance and generality:** The four types appear on the page in translation and apply across industries.

11. **“a general risk”**, with **“if demand slows it would hurt”**  
    **Source:** §5.3: “作者的一般性风险清单和没有推导的看法”; “如果 AI 退潮会受伤”.  
    **CONSISTENT** — The example is an unelaborated general risk.  
    **Example provenance and generality:** It adapts the page’s example rather than quoting it; it is general across industries.

12. **“a figure alone does not lift it”**, with **“the leading soft-drink brand has held 40% of its market for years”**, **“in an article about a bank”**  
    **Source:** §5.1: “有数字也要过上面的规则”; “英特尔多年领先，占 CPU 市场 59%”; “和英伟达的问题关系不大，分析员不会记”.  
    **CONSISTENT** — The example illustrates that a number does not make an unrelated, long-known claim useful.  
    **Example provenance and generality:** The soft-drink and bank example is invented, not on the standard page; its lesson is transferable, although its setting names particular industries.

13. **“while a dated forecast of a shortage, a price or demand is not such a claim”**, with **“the steelmaker expects the shortage to peak next year and last until 2028”**  
    **Source:** §5.1: “内存厂说 2027 年短缺最严重，持续到 2030”; §5.2: “预测、传闻、反证、远期、条件情景都是证据”.  
    **CONSISTENT** — A specific dated forecast must be judged as evidence rather than rejected as a generic shortage claim.  
    **Example provenance and generality:** The steelmaker example adapts the page’s memory-shortage example; it is not itself on the page and uses an industry-specific setting.

14. **“a product, game, driver or benchmark detail with no business scale”**, with **“the card draws 415 watts”** and **“a benchmark score”**  
    **Source:** §5.3: “没有业务规模的产品、游戏、驱动、跑分细节”; “这张卡 415W”; “Geekbench 跑分”; boundary: “对手拿它和本公司产品比的说法不能用这一行删掉”.  
    **CONSISTENT** as a drop category, **with a boundary risk** — A scale-free detail may be rejected, but a competitor comparison using that detail must still be judged under §5.1.  
    **Example provenance and generality:** Both adapt page examples; the card and benchmark are technology-specific, so they do not read the same way across all four company types.

15. **“an unargued view”**, with **“the stock is a hold”**  
    **Source:** §5.3: “作者的一般性风险清单和没有推导的看法”; “这只股票该持有”; §5.1: “一份新报告的判断……分析员会记就留”.  
    **WIDER-DROP** — The stock recommendation is a valid reject example, but the broader phrase can also catch a new, specific reported judgment that the analyst would record.  
    **Example provenance and generality:** The stock example is on the page in translation and is general.

16. **“a quote that only characterises”**, with **“a pivotal moment”**  
    **Source:** §5.3: “只有形容的引语”; “a pivotal moment”; D243 item 10: “只有形容的引语不收”.  
    **CONSISTENT** — This is the decided reject category and the exact page example.  
    **Example provenance and generality:** The example is on the page and is general.

17. **“a share-price move or an investor's position”**, with **“shares fell 13% this month”**  
    **Source:** §5.3: “股价涨跌、投资人仓位、技术面”; “本月跌 13%”; boundary: “股价反应背后的那条新闻不能用这一行删掉”.  
    **CONSISTENT** — The price move and position are reject categories, while the news behind a move must still be assessed.  
    **Example provenance and generality:** The example is on the page in translation and is general.

18. **“another company's valuation, share price or deal that touches none of the company's markets”**  
    **Source:** §5.3, D238: “another company's valuation, share price or deals that touch none of the company's markets”; “别家公司的动作和经营数字不能用这一行删掉，它们留不留按 5.1 的规则判”.  
    **CONSISTENT** — The wording reproduces the D238 rejection, subject to its explicit boundary for other-company actions and operating figures.

19. **“a second item for the same fact (keep the fuller one).”**  
    **Source:** §5.3: “同一事实的复述”; “一篇稿子用五句话说一个部署是一条”.  
    **CONSISTENT** for avoiding duplicate evidence; **NO-SOURCE** for the particular tie-break **“keep the fuller one”** — The cited row says to keep one fact, but does not specify that the fuller item always wins.

### Keep list

20. **“Keep these whenever they move such a question; none is dropped for the reasons above:”**  
    **Source:** §5.1: “因为它让某个问题的答案更可能或更不可能”; §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”.  
    **CONSISTENT**, but incomplete as a guard — It uses the correct test, yet does not explicitly protect every kind of core or supporting evidence from an overlapping drop description.

21. **“a forecast, a rumour, a counter-example, a distant or conditional statement”**  
    **Source:** §5.2: “预测、传闻、反证、远期、条件情景都是证据”; “不因为‘还没发生’‘不是官方’‘离现在远’‘和我们方向相反’就不留”.  
    **CONSISTENT** — These are the standard’s incomplete-evidence boundaries, subject to the header’s relevance test.

22. **“a named party's action without an amount or a date”**  
    **Source:** §5.2: “有名有姓的动作缺金额、缺日期也是证据，分量可以低一点”; §5.1: “三者有一个就够”.  
    **CONSISTENT** — It carries D240’s protection for an otherwise relevant named action.

23. **“a customer's, supplier's, competitor's or partner's action or reported figure”**  
    **Source:** §5.1: “客户、供应商、竞争者、伙伴的有规模、有日期或有名字的动作，以及它们公布的数字”; §6: “别家公司自己的经营数字（收入、利润率、积压订单）” are supporting.  
    **CONSISTENT** — Other companies’ reported operating figures are **present** in this keep list, so they are not an omission in v63; they still depend on the opening relevance test.

24. **“a competitor's comparison against the company's product”**  
    **Source:** §5.3: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT** — It carries the product-detail boundary.

25. **“a partner's or customer's adoption or integration”**  
    **Source:** §5.3: “伙伴、客户采用或集成的动作不是产品细节”; §6: “一家银行选用对手系统”; “伙伴把公司模型集成进政府系统”.  
    **CONSISTENT** — It carries the adoption and integration boundary.

26. **“the launch, shipment, delay or cancellation of a product that sells or will sell at scale”**  
    **Source:** Glossary, 七类驱动: “产品周期：发布、出货、试验、获批、延期”; §6: “对公司规模来说是小事的” is supporting; §5.1: “分析员会记的都留”.  
    **WIDER-DROP risk** — The new scale condition excludes a smaller product’s relevant milestone from this explicit protection even though §6 can keep company-small matters as supporting; the general opening test still covers it, so exclusion from this list is not itself an unconditional instruction to drop it.

27. **“and a change to the plan or configuration of the product that carries the company's value”**  
    **Source:** §6: “它承载价值的那一代产品及其配置、过渡方案”; §5.1: “分析员会记的都留”.  
    **CONSISTENT** for the named core case, **with an omission risk** — It protects changes to the value-carrying product, but does not explicitly protect relevant changes to other products that can qualify as supporting.

28. **“the company's decision to change what its product costs”**  
    **Source:** §5.1: “公司取消软件订阅费，生产使用免费”; glossary: “定价与装机：公司能收多少价、存量多大”; “供给与投入：能做出多少、成本多少”.  
    **WIDER-DROP risk** — This protects the company’s own pricing decision but removes explicit protection for relevant product-price changes made by other parties and for changes in input costs; those remain covered by the general test and, for named parties’ actions, another keep-list item.

29. **“a policy or regulatory step”**  
    **Source:** §5.1: “政策或监管的决定或步骤”; §5.3: “官员宣布的政策步骤不能用这一行删掉”.  
    **CONSISTENT** — It carries the policy boundary.

30. **“a valuation with its assumptions, derivation and date”**  
    **Source:** §5.3: “有假设、有推导、有时点的条件估值要留”; §6: “给出可检验的估值假设”.  
    **CONSISTENT** — It carries the explicit conditional-valuation boundary.

31. **“the news behind a share-price move”**  
    **Source:** §5.3: “股价反应背后的那条新闻不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT** — It carries the boundary rather than protecting the price move itself.

32. **“Return only the items you keep.”**  
    **Source:** §5.1: “分析员会记的都留”; §5.3: “其余不留” as applied through the page’s procedure.  
    **CONSISTENT** — This is an output instruction for the keep decision, not a new criterion for deciding importance.

### Rules not explicitly protected by the keep list

The opening test is broad enough to cover these; the issue is that a model applying the more concrete drop examples may not recognize them as exceptions.

- **The company’s own figures, guidance and decisions.** §5.1 explicitly lists “公司自己的数字、指引或决定”, and §6 includes core financial and business information. Removing the v61 item removes an explicit counterweight when a new company figure is presented amid background or describes an existing situation. The officer-pay noise example does not establish that every company figure should be protected automatically; the standard still requires the analyst test.
- **New specific judgments, including a new report’s assessment.** §5.1 says “一个新的具体判断，是增量，不能漏” and gives “一份新报告的判断” as an example. The broad “unargued view” drop can overlap it.
- **Relevant product milestones below sales scale, and trials or approvals.** The glossary includes “试验、获批” as well as launch, shipment and delay, and §6 permits a company-small matter to be supporting. The narrowed launch item does not explicitly protect these cases.
- **Input supply, input prices, demand, and pricing or installed-base information as such.** The glossary identifies all of them as paths by which information matters. Some are covered indirectly by forecasts, reported figures or named-party actions, but a new relevant observation can still resemble the generic “demand is strong or supply tight” drop example.
- **Other-company operating figures are not omitted.** “a customer's, supplier's, competitor's or partner's action or reported figure” covers them expressly, and the D238 drop row is restricted to valuation, share price or deals unrelated to all company markets.

### Internal tensions

- **New specific judgment versus “unargued view.”** The opening’s broad rejection can conflict with its own instruction to keep what changes an answer; a specific new judgment need not contain a derivation to be useful.
- **Retold forecasts still in force versus “a forecast is never one.”** The first phrase distinguishes forecasts still in force; the later phrase treats every forecast as incapable of being a retelling.
- **General analyst test versus the narrowed product list.** The opening can keep a relevant smaller-product milestone, while the explicit product exception names only one that sells or will sell at scale. That is a competing cue, not a formal blanket ban.
- **D238 boundary versus the general other-company figure protection.** These are compatible when read carefully, but a model that applies “another company's … deal” as a broad other-company rejection can miss the immediately relevant “action or reported figure” elsewhere in the prompt.

The three findings most likely to make the model drop real evidence are:

1. **“an unargued view” is broader than the standard’s rejection of generic views.** It can catch a new, specific judgment that §5.1 says to assess and keep if the analyst would note it.
2. **The scale restriction on product milestones removes an explicit safeguard for smaller but relevant product developments.** §6 allows a company-small matter to be supporting, and the glossary also names trials and approvals.
3. **Removing the company’s own figure, guidance or decision from the explicit keep list leaves those core and supporting items dependent on the abstract opening test.** This is especially risky when a new figure or decision is embedded in text that also describes an established situation.