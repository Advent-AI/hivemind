**The new “Never drop” sentence does not match §6: it can keep noise that the standard rejects.** For example, an old, familiar revenue figure could “touch” revenue and contain a figure, yet §5.1 still asks whether an analyst would record it and §5.3 can reject it as background. The sentence also leaves out two limits in §6: the matter must not be small for the company, and another company’s own operating figures are supporting rather than core.

The audit below is against the current [review-core-v62.txt](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise/review-core-v62.txt) and the [Chinese version 4 standard](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html). I use **WIDER-DROP** only for a possible loss of required evidence, not for the loss of an optional item. Where the text can be read in more than one way, I flag the risk rather than claim a measured outcome.

## Clause-by-clause audit

The standard quotations are exact; the English audit text is quoted exactly. A classification describes the clause as written, including its interaction with the surrounding instructions.

### Opening test

| Text under audit | Standard line and section | Classification and reason |
|---|---|---|
| “Before you return the answer, check it once.” | §5.1: “从第一段读到最后一段，分析员会记的都留。” | **NO-SOURCE** — The standard requires the outcome but does not itself prescribe this final review procedure. |
| “Read each evidence item back as the analyst following the company and keep it when you would write it in this week's notes because it makes some question's answer more or less likely, about the company or its customers, suppliers, competitors, regulators or the economy.” | §5.1: “一个在追这家公司的分析员，读到会在本周笔记里写下来，因为它让某个问题的答案更可能或更不可能。” and “客户、供应商、竞争者、监管、宏观都算”。 | **CONSISTENT** — This carries the analyst test and its stated reach; the later keep list also names partners. |
| “Ask first whether it is new: repeated common knowledge, a long-standing situation retold and an unargued view are noise;” | §5.1: “重复常识、描述长期状况、泛泛的看法，是杂音”；D243 item 6: “文字或日期看不出是旧事的不算重提”。 | **WIDER-DROP** — A situation that began long ago can still contain a new, useful assertion; the clause does not itself carry the oldness boundary, although a later clause partly restores it. |
| “guidance, and a forecast or a plan still in force, keep their place even when retold.” | D243 item 6: “重提的季度指引和仍然有效的预测、计划按本来分量”。 | **CONSISTENT** — It protects the specified retold items, although “guidance” is broader than the standard’s “季度指引.” |

### Drop list and its boundaries

| Text under audit | Standard line and section | Classification and reason |
|---|---|---|
| “These usually fail that check:” | §5.3: “先看那一行的‘边界’一列” (§6 procedure); §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”。 | **CONSISTENT** — “Usually” leaves room for the boundaries, provided the specific rows do not override them. |
| “background the analyst already knew: an arrangement already in place, described again;” | §5.3: “记者的背景和框架”；D243 item 6: “文字或日期看不出是旧事的不算重提”。 | **WIDER-DROP** — “Already in place” does not by itself establish that the description is a retelling or that its current condition is known. |
| “the company's history ("the company was founded in 1998"; "the product line launched in 2020").” | §5.3: “公司成立于 1998 年”；“A100 2020 年上市”。 | **CONSISTENT** — These correspond to the standard’s background examples; the second is generalized from a named product. |
| “A development the item reports without making clear that it is old is not a retelling,” | D243 item 6: “文字或日期看不出是旧事的不算重提”。 | **CONSISTENT** — It carries the stated boundary. |
| “and a forecast is never one;” | D243 item 6: “仍然有效的预测、计划按本来分量”；§5.3: “重提的过去实际数可选”。 | **NARROWER-DROP** — The standard protects forecasts still in force; this exception also protects a retold forecast that has expired, although the opening test may still reject it. |
| “a typical claim that is common knowledge, without a figure and a specific account: that a firm leads or competes, that demand is strong or supply tight,” | §5.1: “谁领先、谁在竞争、需求强、供给紧、融资难这类说法” and “这类陈述没有数字和具体的叙事就不收”。 | **CONSISTENT** — The clause preserves the standard’s common-knowledge condition. |
| “a general risk ("if demand slows it would hurt");” | §5.3: “作者的一般性风险清单和没有推导的看法”；example “如果 AI 退潮会受伤”。 | **CONSISTENT** — The example is a generalized version of the standard’s risk example. |
| “a figure alone does not lift it ("the leading soft-drink brand has held 40% of its market for years", in an article about a bank),” | §5.1: “有数字也要过上面的规则”；example “英特尔多年领先，占 CPU 市场 59%”。 | **CONSISTENT** — A number alone does not pass the analyst test; the soft-drink example is newly written, not on the page. |
| “while a dated forecast of a shortage, a price or demand is not such a claim ("the steelmaker expects the shortage to peak next year and last until 2028");” | §5.1: “内存厂说 2027 年短缺最严重，持续到 2030”；§5.2: “预测、传闻、反证、远期、条件情景都是证据”。 | **NARROWER-DROP** — A date alone does not establish that every shortage, price or demand forecast passes §5.1; the example is adapted, not on the page. |
| “a product, game, driver or benchmark detail with no business scale ("the card draws 415 watts"; "a benchmark score");” | §5.3: “没有业务规模的产品、游戏、驱动、跑分细节”；examples “这张卡 415W”；“Geekbench 跑分”。 | **CONSISTENT** — The drop class and examples trace to the page; its exceptions must still be read with the later keep list. |
| “an unargued view or a quote that only characterises ("the stock is a hold"; "a pivotal moment");” | §5.3: “作者的一般性风险清单和没有推导的看法”；“只有形容的引语”；examples “这只股票该持有”；“a pivotal moment”。 | **CONSISTENT** — Both examples match the two standard rows. |
| “a share-price move or an investor's position ("shares fell 13% this month");” | §5.3: “股价涨跌、投资人仓位、技术面”；example “本月跌 13%”；boundary “财报后股价反应”可选。 | **CONSISTENT** — The example follows the row; dropping an earnings reaction is allowed because it is optional. |
| “another company's valuation, share price or deal that touches none of the company's markets;” | §5.3: “和公司所有市场都无关的别家公司的估值、股价、交易”不留；“别家公司的动作和经营数字不能用这一行删掉”。 | **CONSISTENT** — The D238 row is reproduced with its market boundary. |
| “a second item for the same fact (keep the fuller one).” | §5.3: “同一事实的复述”；example “一篇稿子用五句话说一个部署是一条”。 | **NO-SOURCE** — Combining repeated expressions of one fact is sourced, but “keep the fuller one” is an additional selection rule not stated in this row. |

### New core guard

| Text under audit | Standard line and section | Classification and reason |
|---|---|---|
| “Never drop a statement that touches the company's revenue, profit, financing or credit risk, demand, the progress of the product that carries its value, or the supply and price of its key inputs, and carries a figure, a settled state (signed, announced, started, approved, cancelled, delayed to a date) or a forecast for a stated period.” | §6: “碰到关键判断，并且带着能定位答案的信息”；“对公司不是小事，也不是别家公司自己的经营数字”；§6 procedure: “先判留不留按 5.1 判分析员会不会记”；§5.1: “有数字也要过上面的规则”。 | **NARROWER-DROP** — It makes contact with a subject plus a figure, state or period forecast an unconditional keep, bypassing the analyst test and the drop boundaries, and omits §6’s small-matter and other-company limits. |

The guard also is **not an exact copy of the core definition**. The standard says “关键产品进度” and then includes “它承载价值的那一代产品及其配置、过渡方案”; the guard refers to “the product that carries its value” without explicitly covering configuration or transition arrangements. It also omits a settled decision date from the standard’s examples of a settled state. Those omissions do not by themselves prove a loss, because the opening test and later keep list can still retain the evidence.

### Keep list and closing instruction

Every item in this list inherits the exact introductory condition:

> “Keep these whenever they move such a question; none is dropped for the reasons above:”

Its trace is §5.1: “分析员会记的都留”, and §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”。 **CONSISTENT** as a conditional instruction: the categories are not automatically sufficient by themselves.

| Text under audit | Standard line and section | Classification and reason |
|---|---|---|
| “a forecast, a rumour, a counter-example, a distant or conditional statement;” | §5.2: “预测、传闻、反证、远期、条件情景都是证据”。 | **CONSISTENT** — It lists all five protected forms subject to the introductory analyst test. |
| “a named party's action without an amount or a date;” | §5.2: “有名有姓的动作缺金额、缺日期也是证据，分量可以低一点”。 | **CONSISTENT** — Missing an amount or date alone is not a reason to drop. |
| “the company's own figure, guidance or decision;” | §5.1: “公司自己的数字、指引或决定”。 | **CONSISTENT** — It carries the first kind. |
| “a customer's, supplier's, competitor's or partner's action or reported figure;” | §5.1: “客户、供应商、竞争者、伙伴的有规模、有日期或有名字的动作，以及它们公布的数字”。 | **CONSISTENT** — The list expressly includes other companies’ reported figures, conditional on the analyst test. |
| “a competitor's comparison against the company's product;” | §5.3: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”。 | **CONSISTENT** — It carries the product-detail boundary. |
| “a partner's or customer's adoption or integration;” | §5.3: “伙伴、客户采用或集成的动作不是产品细节”。 | **CONSISTENT** — It carries the adoption and integration boundary. |
| “the launch, shipment, delay or cancellation of a product, and a change to the plan or configuration of the product that carries the company's value;” | Glossary, 七类驱动: “产品周期：发布、出货、试验、获批、延期”；§6: “它承载价值的那一代产品及其配置、过渡方案”。 | **CONSISTENT** — The named events and configuration changes trace to the product-cycle and core descriptions; cancellation also appears in §6’s settled states. |
| “a change to what a product costs;” | Glossary, 七类驱动: “定价与装机：公司能收多少价” and “供给与投入：能做出多少、成本多少”。 | **CONSISTENT** — It has a source, though “what a product costs” can mean either its selling price or its production cost. |
| “a policy or regulatory step;” | §5.3: “官员宣布的政策步骤不能用这一行删掉，按 5.1 判”；§5.1: “政策或监管的决定或步骤”。 | **CONSISTENT** — It carries the policy boundary. |
| “a valuation with its assumptions, derivation and date;” | §5.3: “有假设、有推导、有时点的条件估值要留”。 | **CONSISTENT** — It carries the three stated elements, subject to the list’s introductory relevance condition. |
| “the news behind a share-price move.” | §5.3: “股价反应背后的那条新闻不能用这一行删掉，按 5.1 判”。 | **CONSISTENT** — It carries the boundary rather than protecting the price move itself. |
| “Return only the items you keep.” | §5.1: “分析员会记的都留”；§5.3: “其余不留” in the §6 procedure. | **CONSISTENT** — It directs the output to contain the retained evidence. |

## Standard protections missing or incomplete in the keep list

- **A new specific qualitative judgment or detail.** §5.1 says “一件新发生的事、一个新数字、一个新的具体判断，是增量，不能漏” and gives “旧型号 GPU 的租金在涨” as an example. The keep list names reported figures and actions, but does not expressly name a new qualitative observation by a named party. The broad opening test can protect it; the “long-standing situation” or “unargued view” language could nevertheless pull the other way.
- **An existing condition described with a new, useful assertion.** §5.1 expressly includes “CFO 说十年前建的工厂仍满负荷”. The keep list protects named actions but does not explicitly protect a current status or claim about a long-existing asset. The drop clause “an arrangement already in place, described again” can be read too broadly against it.
- **Trial, approval and transition arrangements for a key product.** The glossary includes “试验、获批”, and §6 includes “过渡方案”. The list names launch, shipment, delay, cancellation, plan and configuration, and also has a general policy-step protection; it does not explicitly name a product trial or transition arrangement. This is a coverage risk, not proof those items must be dropped.
- **The full D243 item 6 boundary.** The list’s general “forecast” protection is broad, but it does not explicitly distinguish a forecast or plan **still in force** from an expired one. The opening does carry “still in force”; the later “a forecast is never one” contradicts that distinction.
- **Pricing and installed base as distinct drivers.** The glossary states “定价与装机：公司能收多少价、存量多大，如售价、费率、利差、装机量、存量客户”. “a change to what a product costs” covers price ambiguously but does not name installed base or existing customers. The general analyst test can keep them, so this is an omission of explicit coverage, not an automatic drop.

**Other companies’ reported operating figures are not omitted:** “a customer's, supplier's, competitor's or partner's action or reported figure” covers them. §6 explicitly gives “别家公司自己的经营数字（收入、利润率、积压订单）” as supporting, and §5.3 says they cannot be dropped using the D238 unrelated-valuation row.

## Internal contradictions

1. **Unconditional guard versus the analyst and noise tests.** “Never drop a statement that touches … and carries a figure” conflicts with “a figure alone does not lift it” and the opening instruction to reject repeated common knowledge. A familiar numbered claim can meet both instructions.
2. **All forecasts versus forecasts still in force.** “a forecast is never one” conflicts with “a forecast or a plan still in force” as the protected retelling. The first also covers expired forecasts.
3. **Background already in place versus protected current information.** “an arrangement already in place, described again” can conflict with “A development … without making clear that it is old is not a retelling” and with “a named party's action without an amount or a date”. The text does not clearly separate an old arrangement’s origin from a new statement about its current state.
4. **“None is dropped for the reasons above” versus the unconditional guard.** The keep-list introduction makes its items conditional on moving a question, whereas the immediately preceding guard says “Never drop” based on topic and information shape alone. The text gives no explicit priority when those tests disagree.

## Example provenance and generality

The examples “the company was founded in 1998”, “the card draws 415 watts”, “the stock is a hold”, “a pivotal moment”, and “shares fell 13% this month” correspond to examples on the standard page. “a benchmark score” generalizes its “Geekbench 跑分” example.

These are **not literal examples on the standard page**:

- “the product line launched in 2020” — generalized from “A100 2020 年上市”.
- “if demand slows it would hurt” — generalized from “如果 AI 退潮会受伤”.
- “the leading soft-drink brand has held 40% of its market for years”, in an article about a bank — adapted from the Intel/NVIDIA example, with a different company context and number.
- “the steelmaker expects the shortage to peak next year and last until 2028” — adapted from the memory-shortage example, with a different industry and periods.

The **card and benchmark examples are hardware-specific**; they illustrate a general rule but do not themselves read the same for a bank, drug maker, retailer and chip maker. The steelmaker and soft-drink examples are also industry-specific, though neither names the covered company. I cannot infer from the text alone whether these examples bias model behavior.

## Three findings most likely to lose real evidence

These are risks from the wording, not measured losses:

1. **An established arrangement can be mistaken for old news.** “an arrangement already in place, described again” does not distinguish a genuinely repeated fact from a new report about the arrangement’s current condition. The standard’s “CFO 说十年前建的工厂仍满负荷” shows why that distinction matters.
2. **The opening label for a long-standing situation is broader than the standard’s boundary.** “a long-standing situation retold” is followed later by the oldness boundary, but a reader can apply the noise label before deciding whether the current statement contains a new observation.
3. **New qualitative information is not explicitly protected in the keep list.** The standard protects “一个新的具体判断” and gives “旧型号 GPU 的租金在涨”; the list’s emphasis on actions and reported figures leaves such a statement more exposed to “unargued view” or background language.