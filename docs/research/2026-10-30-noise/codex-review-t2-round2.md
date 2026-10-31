The current text still risks dropping evidence the standard allows, especially optional old figures and post-earnings price reactions, and newly reported facts about long-running situations.

For example, the standard says a retold past actual figure is optional, while the review tells the model to keep an item “only when” it is new. The exceptions protect several important cases, but they do not resolve that conflict.

I audited only the [current review text](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise/review-core-t2.txt) against [version 4 of the standard](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html). The labels describe what the wording can cause, not a measured model result. “These usually fail” is a tendency rather than an absolute ban; where I flag a wider drop, the concern is that the example or test can steer the model to discard something the standard keeps or permits.

### Opening instruction

1. **“Before you return the answer, check it once.”**  
   Standard: §5.1, “从第一段读到最后一段，分析员会记的都留。一页有八条就是八条，不挑”.  
   **CONSISTENT.** A final check does not itself change what qualifies as evidence, though it can only review items already in the list.

2. **“Read each evidence item back as the analyst following the company and keep it only when you would write it in this week's notes”**  
   Standard: §5.1, “一个在追这家公司的分析员，读到会在本周笔记里写下来，因为它让某个问题的答案更可能或更不可能”; §6, “留不留都不扣分”.  
   **WIDER-DROP.** The analyst test reflects §5.1, but “only when” leaves no explicit room for the optional items §6 allows either to be kept or omitted.

3. **“it is new (a fresh event, figure or specific judgement)”**  
   Standard: §5.1, “一件新发生的事、一个新数字、一个新的具体判断，是增量，不能漏”; §5.3, “重提的过去实际数可选；重提的季度指引和仍然有效的预测、计划按本来分量”.  
   **WIDER-DROP.** Making newness a condition for every item conflicts with the explicit treatment of retold actuals and still-effective guidance, forecasts and plans.

4. **“and it makes some question's answer more or less likely, about the company or its customers, suppliers, competitors, regulators or the economy.”**  
   Standard: §5.1, “问题不限于库里已有的，也不限于本公司：客户、供应商、竞争者、监管、宏观都算”; §6, “帮助理解市场预期，省略不损害论证；留不留都不扣分”.  
   **WIDER-DROP.** The scope follows §5.1, but making an effect on an answer mandatory can exclude optional material that helps explain market expectations.

5. **“These usually fail that check:”**  
   Standard: §5.2, “下面的不留清单不能用来删掉分析员会记的陈述”; §5.3, “先看那一行的‘边界’” is expressed in §6 as “先看那一行的‘边界’一列”.  
   **CONSISTENT.** “Usually” leaves room for the analyst test, although each example still needs to preserve its standard boundary.

### Background and familiar claims

6. **“background the analyst already knew”**  
   Standard: §5.1, “常识，就是跟这家公司的分析员读这篇之前就已经知道的”; “不是常识的，是新信息……分析员会记就留”.  
   **CONSISTENT.** This correctly identifies prior common knowledge as the relevant condition.

7. **“an arrangement already in place, described again”**  
   Standard: §5.3, “重提的季度指引和仍然有效的预测、计划按本来分量”; §5.1, “不是常识的，是新信息……照上面的规则判”.  
   **WIDER-DROP.** An existing arrangement can be part of a still-effective plan or contain a newly reported fact, so its existence and repetition do not alone settle the decision.

8. **“a long-standing situation”**  
   Standard: §5.1, “CFO 说十年前建的工厂仍满负荷”; “不是常识的，是新信息……分析员会记就留”.  
   **WIDER-DROP.** A newly reported fact about a long-standing situation can be evidence, as the factory example shows.

9. **“the company's history”**  
   Standard: §5.3, “记者的背景和框架”; boundary: “没有数字和具体叙事的主张和背景不收；怎么分见 5.1”.  
   **WIDER-DROP.** History as a subject is broader than the standard’s rejected background and can contain a new, relevant fact.

10. **“the company was founded in 1998”**  
    Standard: §5.3, “公司成立于 1998 年”.  
    **CONSISTENT.** This is the standard’s own rejected background example.

11. **“the product line launched in 2020”**  
    Standard: §5.3, “A100 2020 年上市”; boundary: “没有数字和具体叙事的主张和背景不收；怎么分见 5.1”.  
    **CONSISTENT.** As a bare historical launch date, it parallels the standard’s example; whether a fuller statement is new and relevant would still need context.

12. **“a typical claim without a figure and a specific account”**  
    Standard: §5.1, “这类陈述没有数字和具体的叙事就不收”; “不是常识的，是新信息……照上面的规则判”.  
    **WIDER-DROP.** “Typical” does not explicitly say the analyst already knew the claim, so the wording can catch a new specific judgment that lacks a figure.

13. **“that a firm leads or competes”**  
    Standard: §5.1, “谁领先、谁在竞争” are examples of “常识”.  
    **CONSISTENT.** These match the standard when they restate what the analyst already knew.

14. **“that demand is strong or supply tight”**  
    Standard: §5.1, “需求强、供给紧” are examples of “常识”; “不是常识的，是新信息……分析员会记就留”.  
    **CONSISTENT.** These match the standard as familiar general claims, but a new specific demand or supply observation still needs the analyst test.

15. **“a general risk”**  
    Standard: §5.3, “作者的一般性风险清单和没有推导的看法”.  
    **CONSISTENT.** A general risk without a developed account matches the rejected class.

16. **“if demand slows it would hurt”**  
    Standard: §5.3, “如果 AI 退潮会受伤”; §5.2, “不因为……‘离现在远’……就不留”.  
    **CONSISTENT.** The bare conditional is analogous to the standard’s unsupported general-risk example, although a conditional statement is not rejected merely for being conditional.

17. **“a figure alone does not lift it”**  
    Standard: §5.1, “有数字也要过上面的规则”.  
    **CONSISTENT.** A number does not by itself replace the analyst’s relevance judgment.

18. **“the leading carmaker has held a third of its home market for a decade”**  
    Standard: §5.1, “作者说‘英特尔多年领先，占 CPU 市场 59%’，和英伟达的问题关系不大，分析员不会记”.  
    **NO-SOURCE.** This resembles the standard’s example but omits its reason for rejection—limited relevance to the company under study—so the facts given do not establish the same judgment.

### Product details, views and market prices

19. **“a product, game, driver or benchmark detail with no business scale”**  
    Standard: §5.3, “没有业务规模的产品、游戏、驱动、跑分细节”; boundary: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT.** The class matches the standard, and the later text separately protects competitor comparisons and adoption or integration.

20. **“the card draws 415 watts”**  
    Standard: §5.3, “这张卡 415W”.  
    **CONSISTENT.** This is a translation of the standard’s rejected detail example.

21. **“a benchmark score”**  
    Standard: §5.3, “Geekbench 跑分”; boundary: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT.** A bare benchmark score matches the example, while the later comparison exception protects the stated boundary.

22. **“a general view”**  
    Standard: §5.3, “作者的一般性风险清单和没有推导的看法”; boundary: “有假设、有推导、有时点的条件估值要留”.  
    **WIDER-DROP.** “General view” is broader than the standard’s unsupported view and does not itself state the valuation boundary.

23. **“a quote that only characterises”**  
    Standard: §5.3, “只有形容的引语”; decided item 10, “只有形容的引语不收”.  
    **CONSISTENT.** This carries D243 item 10.

24. **“the stock is a hold”**  
    Standard: §5.3, “这只股票该持有”.  
    **CONSISTENT.** This translates the standard’s example of an unsupported view.

25. **“a pivotal moment”**  
    Standard: §5.3, “a pivotal moment”.  
    **CONSISTENT.** This is the standard’s exact example of a quotation that only characterises.

26. **“a share-price move”**  
    Standard: §5.3, “‘财报后股价反应’可选”; “别的股价涨跌照旧不留”.  
    **WIDER-DROP.** The broad class includes the post-earnings reaction that the standard makes optional.

27. **“an investor's position”**  
    Standard: §5.3, “股价涨跌、投资人仓位、技术面”; example “Burry 做空”.  
    **CONSISTENT.** This matches the rejected class.

28. **“shares fell 13% this month”**  
    Standard: §5.3, “本月跌 13%”; boundary: “‘财报后股价反应’可选”.  
    **CONSISTENT.** The bare monthly move mirrors the standard’s example; the text still omits the optional post-earnings boundary.

29. **“another company's valuation, share price or deal that touches none of the company's markets”**  
    Standard: §5.3, “和公司所有市场都无关的别家公司的估值、股价、交易”不留; “别家公司的动作和经营数字不能用这一行删掉”.  
    **CONSISTENT.** This now follows the D238 row’s specified categories and market boundary.

30. **“a second item for the same fact (keep the fuller one)”**  
    Standard: §5.3, “同一事实的复述”; “一篇稿子用五句话说一个部署是一条”.  
    **NO-SOURCE.** One item for the same fact follows the standard, but the instruction to choose “the fuller one” is not stated on the page and does not say to preserve relevant differences between the two accounts.

### Exceptions and return instruction

The introductory wording applies to every exception below:

> **“These are not by themselves reasons to drop; judge them by the check:”**

Standard: §5.2, “不因为‘还没发生’‘不是官方’‘离现在远’‘和我们方向相反’就不留”; §5.1, “留不留由上面的规则判”.  
**CONSISTENT.** Unlike the round-one wording, this does not automatically keep every item in the exception list.

31. **“a forecast”**  
    Standard: §5.2, “预测、传闻、反证、远期、条件情景都是证据”.  
    **CONSISTENT.** Being a forecast is not itself a reason to drop an item.

32. **“a rumour”**  
    Standard: §5.2, “不因为……‘不是官方’……就不留”.  
    **CONSISTENT.** Unconfirmed status alone is not a reason to drop it.

33. **“a counter-example”**  
    Standard: §5.2, “一个真实的反例可能比十个顺风数字更重要”.  
    **CONSISTENT.** Evidence is not rejected merely because it points against the current direction.

34. **“a distant or conditional statement”**  
    Standard: §5.2, “远期、条件情景都是证据”; “不因为……‘离现在远’……就不留”.  
    **CONSISTENT.** Distance or conditionality alone does not justify a drop.

35. **“a named party's action without an amount or a date”**  
    Standard: §5.2, “有名有姓的动作缺金额、缺日期也是证据，分量可以低一点”.  
    **CONSISTENT.** This preserves D240’s protection against dropping an action solely for a missing amount or date.

36. **“guidance, a forecast or a plan still in force, even when retold”**  
    Standard: §5.3, “重提的季度指引和仍然有效的预测、计划按本来分量”.  
    **WIDER-DROP.** The exception is helpful, but sending retold items back through an opening test that says “only when” new can still reject the very retellings the standard preserves.

37. **“a customer's, supplier's or competitor's action or reported figure”**  
    Standard: §5.1, “客户、供应商、竞争者、伙伴的有规模、有日期或有名字的动作，以及它们公布的数字”; §5.3, “别家公司的动作和经营数字不能用这一行删掉”.  
    **CONSISTENT.** The named parties and figures are protected from being dropped merely because they concern another company; partners and other companies are not explicitly named here.

38. **“a competitor's comparison against the company's product”**  
    Standard: §5.3, “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”; §6, “对手自己模拟的 2.4 倍性能比较”.  
    **CONSISTENT.** This restores the product-detail boundary that protects a potentially supporting comparison.

39. **“a partner's or customer's adoption or integration”**  
    Standard: §5.3, “伙伴、客户采用或集成的动作不是产品细节（5.1 第 2 类）”.  
    **CONSISTENT.** This protects the standard’s named boundary.

40. **“the launch, shipment, delay or cancellation of a product”**  
    Standard: glossary, “产品周期：发布、出货、试验、获批、延期”; §5.1, “留不留由上面的规则判”.  
    **CONSISTENT.** The text makes these events reasons for consideration, not automatic keeps; cancellation is also reflected in §5.4’s “NVL72x2 取消归产品进度”.

41. **“a change to the plan or configuration of the product that carries the company's value”**  
    Standard: §6, “它承载价值的那一代产品及其配置、过渡方案”.  
    **CONSISTENT.** This protects a kind of product information the standard identifies as potentially central.

42. **“a change to what a product costs”**  
    Standard: §5.1, “公司取消软件订阅费，生产使用免费”; glossary, “定价与装机：公司能收多少价”.  
    **CONSISTENT.** This protects relevant pricing changes without making all of them automatic keeps.

43. **“a policy or regulatory step”**  
    Standard: §5.3, “官员宣布的政策步骤不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT.** The text preserves the boundary and applies the analyst test.

44. **“a valuation with its assumptions, derivation and date”**  
    Standard: §5.3, “有假设、有推导、有时点的条件估值要留”.  
    **CONSISTENT.** The exception now includes all three elements named in the standard.

45. **“the news behind a share-price move”**  
    Standard: §5.3, “股价反应背后的那条新闻不能用这一行删掉，按 5.1 判”.  
    **CONSISTENT.** This carries the boundary for the underlying news, though it does not cover the optional post-earnings price reaction itself.

46. **“Return only the items you keep.”**  
    Standard: §5.1, “分析员会记的都留。一页有八条就是八条，不挑”; §6, “留不留都不扣分”.  
    **CONSISTENT.** This is an output instruction and does not independently define what to keep.

### Rules the exceptions omit

- **Optional evidence.** §6 says “财报后股价反应；在研公司的估值倍数、市值、孤零零的目标价；生态数字；重提的过去实际数；新加坡案件” are optional. The review does not say that any of these may be kept; its price and background examples, together with the mandatory newness test, can remove some of them.

- **Other companies’ operating figures.** §5.3 says “别家公司的动作和经营数字不能用这一行删掉，它们留不留按 5.1 的规则判”; §6 names “别家公司自己的经营数字（收入、利润率、积压订单）” as supporting. The exception names customers, suppliers and competitors, but not a partner’s figures or relevant figures from another company outside that list. The current D238 clause is properly limited, so this is an omitted protection rather than the round-one blanket ban on other-party news.

- **New information about a familiar or long-running situation.** §5.1 says “不是常识的，是新信息，比如一份新报告的判断、一个新的市场数据、刚发生的事的细节……分析员会记就留”, and gives “CFO 说十年前建的工厂仍满负荷”. No exception expressly protects that kind of newly reported fact from “a long-standing situation” or “the company's history”.

- **The general limit on every reject rule.** §5.2 says “下面的不留清单不能用来删掉分析员会记的陈述”. The review says exceptions are judged by the analyst check, but does not expressly say that a listed drop example cannot override evidence the analyst would write down.

### Internal tensions

- **Newness versus retold plans and guidance.** “keep it only when” “it is new” conflicts with “guidance, a forecast or a plan still in force, even when retold”, because the latter is still judged by the former check.

- **Long-standing situations versus new facts.** “a long-standing situation” usually fails, while a “fresh event, figure or specific judgement” passes the newness part of the check; a newly reported figure about a long-standing situation fits both descriptions.

- **General views versus forecasts and valuations.** “a general view” usually fails, while “a forecast” and “a valuation with its assumptions, derivation and date” are not by themselves reasons to drop. A general-sounding forecast or valuation can fit both descriptions, and the text does not explicitly connect the view rule to the valuation boundary.

- **Price moves versus the general analyst test.** “a share-price move” usually fails, but the opening test has no optional category. A post-earnings reaction can therefore be treated as a drop even though the standard permits keeping it.

### Example provenance and generality

The text contains eight quoted examples:

| Exact example | On the standard page? | Generality |
|---|---|---|
| “the company was founded in 1998” | Yes, translated from “公司成立于 1998 年”. | General. |
| “the product line launched in 2020” | Adapted from “A100 2020 年上市”, not the same example verbatim. | Product-specific; it does not read naturally for every bank or drug maker. |
| “if demand slows it would hurt” | Adapted from “如果 AI 退潮会受伤”, not verbatim. | General. |
| “the leading carmaker has held a third of its home market for a decade” | No; resembles the Intel example but changes the company and omits its relevance context. | Industry-specific: a carmaker does not read the same across the four requested sectors. |
| “the card draws 415 watts” | Yes, translated from “这张卡 415W”. | Hardware-specific; it does not read the same across the four sectors. |
| “a benchmark score” | Adapted from “Geekbench 跑分”, not verbatim. | Computing-oriented; it does not read naturally across all four sectors. |
| “the stock is a hold” | Yes, translated from “这只股票该持有”. | General for a publicly traded company. |
| “a pivotal moment” | Yes, exact. | General. |
| “shares fell 13% this month” | Yes, translated from “本月跌 13%”. | General for a publicly traded company. |

The header says eight examples, but the table contains **nine**; all nine quoted examples in the current file are listed.

### Three findings most likely to drop real evidence

1. **Mandatory newness conflicts with the standard’s retelling and optional rules.** A still-effective plan or retold guidance can be rejected by “only when” new, despite the later exception; a retold actual can also be removed although it is optional.

2. **“A long-standing situation” is too broad.** It can steer the model away from a newly reported, relevant fact about an old condition—the kind illustrated by the standard’s factory operating at full capacity.

3. **The share-price rule omits the post-earnings boundary.** “A share-price move” includes a reaction after earnings, which §5.3 and §6 explicitly allow as optional. This is an optional-item loss, not a claim that every price move must be kept.