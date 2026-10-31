The prompt’s largest difference is its **keep/reject procedure**: it treats the four kinds as a required gate, while the standard says they describe what kept evidence usually looks like and that the analyst’s judgment decides.

For example, a useful new statement that does not fit one of the four prompt kinds can be rejected before the model asks whether it changes the answer to a research question. The prompt also has the opposite risk: a statement can pass a broad kind and the reject list without being judged for its incremental value.

This is a read-only comparison of [the version 4 standard](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html), [role-v53](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v53.txt), [categories-v53](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/categories-v53.json), the v53 schema and user-message builder in [extraction.py](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/extraction.py), and the two supplied complete requests. No files were edited.

**Important limit:** I cannot honestly call the table below the requested complete sentence-by-sentence audit. It covers the main decision-bearing clauses and the requested reverse-direction boundaries, but it does **not** provide a separate row for every example, every formatting instruction, or every schema enum. I have therefore kept the conclusions as a partial audit rather than presenting it as exhaustive.

## Part A — Prompt clauses checked against the standard

Standard quotations are exact excerpts. “Opening — next step” marks opening findings, including D248 changes; it does not imply an instruction to change them now. A category’s “read” block is treated as a reading instruction, not automatically as an instruction to keep everything it names.

| ID | Prompt quote | Standard line | Class | Reason |
|---|---|---|---|---|
| A1 | “Your first job is evidence: find every material statement in the item.” | §5.1: “从第一段读到最后一段，分析员会记的都留。” | CONSISTENT | Both direct a full read for evidence, although “material” needs the standard’s test. |
| A2 | “A material statement is one of four kinds.” | §5.1: “它们通常是下面四类之一；四类描述的是会记的陈述长什么样，不是‘属于四类就一定留’，留不留由上面的规则判。” | CONTRADICTS | The prompt makes the four descriptions a closed definition; the standard says they are usual descriptions and the preceding judgment decides. |
| A3 | “The company's own figure, guidance or decision” | §5.1: “公司自己的数字、指引或决定” | CONSISTENT | The named kind corresponds to the standard’s first kind, subject to the general keep test. |
| A4 | “A customer's, supplier's, competitor's or partner's action or reported figure with a size, date or name” | §5.1: “客户、供应商、竞争者、伙伴的有规模、有日期或有名字的动作，以及它们公布的数字” | NARROWER | The prompt attaches “with a size, date or name” to reported figures as well as actions; the standard’s sentence attaches it to actions and separately names published figures. |
| A5 | “that bears on the company's demand, supply, input costs, competition, prices or products” | §5.1: “问题不限于库里已有的，也不限于本公司：客户、供应商、竞争者、监管、宏观都算” | NARROWER | The listed channels leave out other possible research questions, including cash and credit risk; whether a particular omitted channel is material still requires judgment. |
| A6 | “A named party's new claim or estimate about the company or its industry” | §5.1: “具名一方的主张或估计”；“一件新发生的事、一个新数字、一个新的具体判断，是增量，不能漏” | NARROWER | The prompt adds an explicit company-or-industry restriction to the kind. |
| A7 | “A policy or regulatory decision or step” | §5.1: “政策或监管的决定或步骤” | CONSISTENT | The categories use the same words. |
| A8 | “Go through the item from its first paragraph to its last.” | §5.1: “从第一段读到最后一段” | CONSISTENT | The direction matches. |
| A9 | “For each statement, name its kind and check it against the list below; take it only when it has a kind and nothing on the list applies.” | §5.1: “留不留由上面的规则判”；§5.3: “不在清单上的句子，用 5.1 的规则逐句判（分析员会不会记）” | CONTRADICTS | Passing a kind and avoiding a listed rejection replaces the analyst’s incremental-value judgment, while lacking a kind becomes a veto. |
| A10 | “Most of an item is background” | §5.1: “整体倾向谨慎，对增量敏感。杂音很大，不是什么都要抽” | CONSISTENT | The cautious direction is supported, although the standard does not call all noise background. |
| A11 | “a page with eight such statements yields eight evidence items, not a selection” | §5.1: “一页有八条就是八条，不挑” | CONSISTENT | The stopping instruction matches. |
| A12 | “reject these, even when a named party states them, and everything that has no kind” | §5.2: “下面的不留清单不能用来删掉分析员会记的陈述”；§5.3: “不在清单上的句子，用 5.1 的规则逐句判（分析员会不会记）” | CONTRADICTS | The categorical veto omits the boundary-first procedure and adds rejection for not fitting a kind. |
| A13 | “a product feature, performance, compatibility, retail price or content detail that gives no business scale … even with a figure” | §5.3: “没有业务规模的产品、游戏、驱动、跑分细节” | CONSISTENT | The basic product-detail rejection corresponds to the table row. |
| A14 | “unless it is a competitor's claim against the company's product” | §5.3: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判” | CONSISTENT | Both protect a competitor’s comparison from this particular rejection and leave judgment to the keep rule. |
| A15 | “the company's own claim to beat rivals is still a product detail” | §5.3: “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判” | NARROWER | The standard names the competitor comparison boundary but does not state a blanket veto for the company’s own comparison; a new, useful claim still has to be assessed under §5.1. |
| A16 | “a partner's or customer's adoption or integration … are not product details” | §5.3: “伙伴、客户采用或集成的动作不是产品细节（5.1 第 2 类）” | CONSISTENT | The exception matches the boundary. |
| A17 | “a change to the plan, configuration or timing of the product that carries the company's value … [is] not product details” | §5.1: “一个在追这家公司的分析员，读到会在本周笔记里写下来，因为它让某个问题的答案更可能或更不可能。” | NO-SOURCE | The standard has no general carve-out for every change of this form; its product-progress examples do not establish an automatic exemption for all such changes. |
| A18 | “an investor's position or trade, a share-price move or the market value” | §5.3: “股价涨跌、投资人仓位、技术面”；“在研公司的估值倍数、市值、孤零零的目标价可选” | NARROWER | The blanket market-value rejection removes an explicitly optional item. |
| A19 | “though the news a move reacts to is kept” | §5.3: “股价反应背后的那条新闻不能用这一行删掉，按 5.1 判” | WIDER | The standard protects the news from this row but still requires the §5.1 judgment; the prompt says it is kept. |
| A20 | “another company's valuation, share price or deals that touch none of the company's markets” | §5.3: “和公司所有市场都无关的别家公司的估值、股价、交易” | CONSISTENT | The restriction follows the additional rejection row. |
| A21 | “common knowledge an analyst following the company already has, unless it gives a figure and a specific account” | §5.1: “这类陈述没有数字和具体的叙事就不收。” | CONSISTENT | The basic exception matches for the specified common-knowledge class; the exception alone does not dispense with the overall keep test. |
| A22 | “framing or background, general risks or unargued verdicts, political or strategic views” | §5.3: “作者的一般性风险清单和没有推导的看法”；“记者的背景和框架”；“没有数字也没有决定的政治、战略表态” | CONTRADICTS | The prompt folds several independently bounded rows into “common knowledge,” so its single escape clause can apply differently from the standard’s separate boundaries. |
| A23 | “an official's order, law, bill or ruling is kind (4), not a view” | §5.3: “官员宣布的政策步骤不能用这一行删掉，按 5.1 判（第 4 类）” | CONSISTENT | It prevents the political-view row from automatically removing a policy step. |
| A24 | “the same fact or arrangement said again in other words … is one evidence item” | §2: “一条记录一个陈述，一件事用几句话说仍是一条” | CONSISTENT | The within-item consolidation matches; cross-item matching remains out of scope. |
| A25 | “a quote that only characterizes” | §5.3: “只有形容的引语” | CONSISTENT | The rejection matches. |
| A26 | “company boilerplate, bylines, forward-looking-statement text” | §5.3: “模板”；“署名、作者简介、经纪商页脚、前瞻性声明、广告” | CONSISTENT | These named items are within the standard’s template row. |
| A27 | “Copy its quote verbatim, without translation.” | §2: “记逐字引文” | CONSISTENT | The verbatim requirement is sourced; the standard excerpt does not separately discuss translation. |
| A28 | “write a standalone summary … who did or said what, how much and for which period” | §5.4: “一条记录单独读要能懂”；“六格里只填这一条用得上的” | NARROWER | It names four dimensions but omits conditions and prediction versus occurrence, and does not say to fill only applicable dimensions. |
| A29 | “Identify the speaker and, for a retelling, the original speaker and statement day.” | §2: “说话人、原始说话人和原始日期（不知道就写不知道，不填报道日）” | NARROWER | The role sentence frames original attribution as a retelling task; the schema descriptions partially repair this but do not remove the wording tension. |
| A30 | “fact for official actions, published actual figures or completed transactions” | §5.5: “正式动作、公布的实际数字、完成的交易” | CONSISTENT | The fact examples match that row when no higher row applies. |
| A31 | “party_statement for company guidance, management statements or officials' remarks” | §5.5: “公司的指引、管理层的表态、官员的讲话” | CONSISTENT | The named examples match. |
| A32 | “third_party_view for analyst, media or expert opinions” | §5.5: “分析师、媒体、专家的看法和估计” | NARROWER | The role explicitly names opinions but does not include estimates in this tier sentence. |
| A33 | “rumour for claims the item credits to unnamed sources or calls unconfirmed” | §5.5: “文章说来自没具名的人，或文章自己说未经证实（即使说的是一项公告或一个数）” | NARROWER | The prompt omits the explicit priority over an announcement or figure and the separate residual no-source row. |
| A34 | “an announcement or completed deal the item reports is a fact even when the reporter names no source” | §5.5: “文章报道的公告或已完成的交易（即使记者没写出处）”；“一句话同时符合两行时，取表里上面那行” | NARROWER | The fact rule is sourced, but the prompt does not say that an explicitly unnamed-source or unconfirmed claim takes precedence. |
| A35 | “Use only this item's information.” | §4: “主体、量或事件、时间依据都能在原文找到。” | CONSISTENT | For source-supported claims and candidate details, the instruction follows the standard’s source requirement. |
| A36 | “Report plans as plans; do not infer committed funding, orders, deliveries or revenue.” | §5.4: “指引、预计、商谈、传闻不等于已实现、已签约” | CONSISTENT | It preserves the distinction between plans and completed or committed outcomes. |
| A37 | “Open a candidate only for one of four reasons” | §3: “开题理由是 D184 定的四类，D236 把主驱动量扩到产品节点，所以写成五类。” | CONSISTENT | The prompt uses four enum reasons, with the standard’s two main-driver classes sharing one reason. |
| A38 | “the date by which the generation of the company's own product that carries that quantity launches or starts shipping” | §3 B: “哪天走到能带来收入的那一步（通常是开始出货）；发布、送样是它的证据” | WIDER | **Opening — next step.** The prompt allows launch as the question’s endpoint, while the standard normally treats launch as evidence for the revenue-producing step. |
| A39 | “industry_aggregate: one aggregate quantity for one calendar year” | §3 D: “任何一家公司之外、好几家都会受它影响的量或价格” | NARROWER | **Opening — next step.** Aggregate spending is only part of the standard’s shared quantity, which also includes prices and rates. |
| A40 | “or an equity stake whose size is stated and is not yet completed” | §3 C: “写明规模、尚未完成的入股或收购” | NARROWER | **Opening — next step.** The prompt names an equity stake but does not explicitly include a sized, pending acquisition. |
| A41 | “an obligation a universe company takes on in its own name” | §3: “任何公司自己的量是那家公司的问题，私营公司也算”；“名单外不能忽略” | NARROWER | **Opening — next step.** Restricting this reason to a universe company can exclude an otherwise eligible company outside the supplied list. |
| A42 | “whether or not the item gives its amount” | §3 C: “规模要大到能改变公司的收入、利润、现金或信用风险才开” | WIDER | **Opening — next step.** Lack of a stated amount is allowed, but the prompt omits the separate company-scale test for a single transaction. |
| A43 | “Its own borrowing, its own leases and a completed or unsized investment are not obligations.” | §3 C: “Its own borrowing, its own leases and a completed or unsized investment are not obligations” | CONSISTENT | The wording is the standard’s quoted rule for this opening reason. |
| A44 | “Not yet signed: a yes/no question … at most 18 months out.” | §3 C: “还没签：是非两档”；“检查日最多在文章后 18 个月” | CONSISTENT | **Opening — next step.** The shape and horizon correspond, subject to the missing scale test. |
| A45 | “Already taken on, as one deal or as a programme: a financing_amount question … at the company's next annual filing” | §3 C: “已经承担（一笔或一个计划）：金额，五档”；“已承担的按下一份年报” | CONSISTENT | **Opening — next step.** The form matches, subject to the missing scale test. |
| A46 | “A different population, source, estimate, wording or direction of a question is the same question; a different quantity, period or decision is another.” | §4: “同一个结果能判掉两题，就是同一题；答案能分开走、而且分析员会分别下注的，才是另一题” | CONTRADICTS | **Opening — next step.** The prompt uses differences in fields as the test; the standard uses whether the same outcome settles them and whether separate bets are warranted. |
| A47 | “A pending regulatory decision may lack a date; use the current fiscal year-end as its due date.” | §3 E: “文章没写日期的待决监管事项，用本财年末”；“这个日期是研究员定的检查日，要标明” | NARROWER | **Opening — next step.** The prompt supplies the date but does not require marking it as the analyst’s chosen check date. |
| A48 | “Do not propose theses about quarterly figures or guidance, undated subjects such as moats or strategy, executive appointments, shareholder votes or bylaws, routine litigation procedure, or buyback authorisations.” | §4: “季度数字和季度指引”；“没日期的‘护城河’‘战略’”；“高管任免、股东投票、回购授权；章程”；“例行诉讼程序” | CONSISTENT | **Opening — next step.** The listed exclusions correspond to the not-open list. |
| A49 | “One thesis concerns one figure for a named period or one event. Separate independently meaningful outcomes.” | §3: “一个问题只问一个量的一个期间，或一件事；能各自朝相反方向走、而且分析员会分别下注的部分要分开” | NARROWER | **Opening — next step.** “Independently meaningful” is weaker than the standard’s two-part test of separate outcomes and separate bets. |
| A50 | “A five-rung asset ladder runs from Strongly bullish through Bullish, Neutral and Bearish to Strongly bearish, meaning good or bad for the business.” | §3: “标的问题的档描述业务结果” | CONTRADICTS | **Opening — next step.** The prompt prescribes sentiment labels; the standard says to describe business outcomes. |
| A51 | “A research group is one ongoing matter … It usually spans companies and themes.” | §2: “一件正在进行的事……把几个问题组织在一起，常常跨公司。” | CONSISTENT | The definition follows the ledger description. |
| A52 | “A company's own … financial lines … carry no group … unless the line itself tracks such a matter.” | §2: “公司自己的报表行……不带研究组，除非这一行本身就在追这样一件事” | CONSISTENT | The role includes the standard’s exception. |
| A53 | `[Research groups] “None yet.”` | §2: “研究组……把几个问题组织在一起” | CONTRADICTS | The v53 request hides stored groups; saying none exist is stronger than saying none are shown. |
| A54 | “leave group_refs empty for a company's own financial lines.” | §2: “不带研究组，除非这一行本身就在追这样一件事” | NARROWER | The fixed user block omits the exception that the role includes. |
| A55 | “Return empty arrays only for a page with no business content.” | §5.1: “杂音很大，不是什么都要抽”；§5.3: “不在清单上的句子，用 5.1 的规则逐句判（分析员会不会记）” | CONTRADICTS | A page can contain business content but no statement the standard would keep and no qualifying candidate. |
| A56 | Schema `speaker`: “Who says it in this item: the outlet, the author or the person quoted.” | §2: “说话人、原始说话人和原始日期” | CONSISTENT | The field asks for the immediate speaker separately from the original party. |
| A57 | Schema `original_who`: “The party whose statement, figure or action it is, even when the item reports it without attribution” | §5.4: “原始判断者；是本人估计还是别人实测” | CONSISTENT | The instruction preserves the original party even in an unquoted retelling. |
| A58 | Schema `original_who`: “the outlet or author only for its own estimate, analysis or unnamed-source report.” | §5.5: “文章说来自没具名的人”；§5.4: “原始判断者” | CONTRADICTS | Naming the outlet as the original party for an unnamed-source report can replace the actual, unknown source with the relay. |
| A59 | Schema `original_day`: “empty when the item gives none or only a month” | §5.4: “原始发言日不知道就写不知道，不能填报道日” | CONSISTENT | It preserves an unknown exact day. |
| A60 | Schema `original_day`: “the publication day only when the item is that party's own release, filing, call or analysis.” | §5.4: “原始发言日不知道就写不知道，不能填报道日” | NARROWER | A party’s own document can retell an earlier statement; the wording can assign publication day without establishing that it is the original statement day. |
| A61 | Schema `opens_as`: `main_driver`, `industry_aggregate`, `policy_stage`, `binding_obligation` | §3 D: “开题理由叫 shared_quantity”；“现行提示词和代码还叫 industry_aggregate，按这一页改” | NARROWER | **Opening — next step.** The enum retains the old name and the role defines it more narrowly than the signed shared-quantity class. |
| A62 | T7: “Officially or company-confirmed events are facts” | §5.5: “文章报道的公告或已完成的交易（即使记者没写出处）” | NARROWER | Read alone, the category block suggests confirmation is needed, while the role and standard also allow a reported announcement or completed deal without named confirmation. |
| A63 | T8: “The author's forecasts and price targets with their figures” | §5.3: “孤零零的目标价可选”；“有假设、有推导、有时点的条件估值要留” | WIDER | As a reading target it is not necessarily a keep command, but it does not distinguish optional isolated targets from required supported conditional valuations. |
| A64 | T8: “Not the author's general arguments or risk lists.” | §5.1: “不是常识的，是新信息，比如一份新报告的判断……照上面的规则判，分析员会记就留。” | NARROWER | A blanket exclusion of general arguments can remove a new, useful analytical judgment; the standard rejects general risks and unsupported views, not every argument. |

### Examples not individually audited

The role’s examples are part of the request. The table above does not individually classify all of them, including the product, share-price, common-knowledge, transaction, and ladder examples. Their inclusion in the quoted prompt file is not a substitute for the row-by-row example audit requested.

## Part B — Standard rules absent or weaker in the prompt

The distinctions below concern the extraction call. A rule being absent from the prompt does not by itself prove that a particular answer was wrong.

### Keep procedure and incomplete evidence

| Standard rule, quoted exactly | Prompt gap |
|---|---|
| §5.1: “一个在追这家公司的分析员，读到会在本周笔记里写下来，因为它让某个问题的答案更可能或更不可能。” | The prompt says “material” but does not state this deciding test. |
| §5.1: “判一句话之前先问：这是新信息吗？它让哪个问题的答案变了？” | The prompt does not explicitly ask either question for each statement. |
| §5.1: “四类描述的是会记的陈述长什么样，不是‘属于四类就一定留’” | The prompt reverses this relationship by using kinds as a gate. |
| Flow: “先看那一行的‘边界’一列：写着‘不能用这一行删掉’或‘要留’的，按第 5.1 节判，留下的走下面；写着‘可选’的归可选；其余不留” | The prompt does not give the complete boundary-first order or the optional outcome. |
| §5.2: “预测、传闻、反证、远期、条件情景都是证据” | The prompt does not state this complete set. |
| §5.2: “不因为‘还没发生’‘不是官方’‘离现在远’‘和我们方向相反’就不留” | These protections are absent as a general rule. |
| §5.2: “有名有姓的动作缺金额、缺日期也是证据” | The examples imply some incomplete actions can survive, but the explicit protection is absent. |
| §5.2: “下面的不留清单不能用来删掉分析员会记的陈述” | The prompt instead says to reject whenever a list item applies. |

### Every §5.3 row and boundary

| Row and exact standard boundary | Prompt status |
|---|---|
| “没有业务规模的产品、游戏、驱动、跑分细节” — “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判”；“伙伴、客户采用或集成的动作不是产品细节” | Both named boundaries appear; the prompt adds the separate product-plan carve-out and own-comparison veto. |
| “股价涨跌、投资人仓位、技术面” — “股价反应背后的那条新闻不能用这一行删掉，按 5.1 判”；“‘财报后股价反应’可选”；“在研公司的估值倍数、市值、孤零零的目标价可选”；“别的股价涨跌照旧不留” | The news boundary is stronger in the prompt (“is kept”); the optional items are missing, and market value is categorically rejected. |
| “作者的一般性风险清单和没有推导的看法” — “有假设、有推导、有时点的条件估值要留” | The prompt has a conditional-valuation example, but does not state the three conditions or the required-keep boundary. |
| “记者的背景和框架” — “没有数字和具体叙事的主张和背景不收；怎么分见 5.1” | The common-knowledge wording is present, but the distinction between new information and known background is not stated with the same test. |
| “没有数字也没有决定的政治、战略表态” — “官员宣布的政策步骤不能用这一行删掉，按 5.1 判（第 4 类）” | The policy-step boundary appears; grouping all political or strategic views under the common-knowledge escape clause weakens the row’s distinct test. |
| “同一事实的复述” | Same-item consolidation is present. Cross-item storage and matching are outside this audit. |
| “已知事实的重述” — “重提的过去实际数可选；重提的季度指引和仍然有效的预测、计划按本来分量；看不出是旧事的不算重提” | This entire distinction is absent. |
| “模板” | Some examples appear; unrelated page content, advertising, author biographies, broker footers, and recommendations are not all named. |
| “只有形容的引语” | Present. |
| “新加坡转运案件的概况和被告个人资产” — “可选，收不收都不扣分” | The optional treatment is absent. |
| “和公司所有市场都无关的别家公司的估值、股价、交易” — “别家公司的动作和经营数字不能用这一行删掉，它们留不留按 5.1 的规则判。” | The rejection appears; the explicit protection for actions and operating figures is only partly represented by kind 2. |
| “不在清单上的句子，用 5.1 的规则逐句判（分析员会不会记）” | Missing; the prompt substitutes a kind-plus-list test. |

The decided optional ecosystem figures are also absent: **“生态数字（论文数、获奖、下载量、开发者人数、大会人数）可选”**. That is an optional treatment, not an instruction to have the model assign weight.

### Meaning and source

| Standard rule, quoted exactly | Prompt gap |
|---|---|
| §5.4: “六格里只填这一条用得上的” | The role does not state applicability. |
| §5.4, 谁: “原始判断者；是本人估计还是别人实测” | Schema asks for the original party, but does not explicitly preserve estimate versus independent measurement. |
| §5.4, 什么: “业务、指标或动作” | Partly present in `one_line`. |
| §5.4, 多少: “金额、比例、数量” | Partly present as “how much.” |
| §5.4, 哪个期间: “预测或事实覆盖的期间”；“余下时间不改成全年” | The prompt asks for the period but does not give the remaining-period boundary. |
| §5.4, 什么条件: “推导的假设；计划、上限、‘最多’” | The summary instruction does not require assumptions or caps. |
| §5.4, 预测还是已发生: “指引、预计、商谈、传闻不等于已实现、已签约” | Plans are protected, but the full set and uncertainty are not explicitly required in the summary. |
| §5.4: “条件不能只放在旁边另一条里” | The prompt asks for a standalone summary but does not explicitly require its conditions to remain in that record. |
| §5.4: “没有来源证实的结论，可以作为分析员的推断写出，但不能写成来源说的事实” | The distinction between a marked analyst inference and a source claim is absent. |
| §5.5 row 1: “文章说来自没具名的人，或文章自己说未经证实（即使说的是一项公告或一个数）” | The prompt names unnamed and unconfirmed claims but omits the explicit precedence case. |
| §5.5 row 2: “正式动作、公布的实际数字、完成的交易；文章报道的公告或已完成的交易（即使记者没写出处）” | Present, but without the table’s priority order. |
| §5.5 row 3: “公司的指引、管理层的表态、官员的讲话” | Present. |
| §5.5 row 4: “分析师、媒体、专家的看法和估计” | “Opinions” appear in the role; estimates are not explicitly included in that tier sentence. |
| §5.5 row 5: “以上都不是、又没有出处的说法” | The residual unattributed-claim rule is absent. |
| §5.5: “一句话同时符合两行时，取表里上面那行” | The priority rule is absent. |
| §5.5: “按主要说法定层，次要部分的性质写进摘要；不拆成两条，除非是两件事” | Mixed records have no explicit tier or summary instruction. |

### Opening — next step

These are listed because the user requested them; they are not findings about matching against the existing library.

| Standard rule, quoted exactly | Prompt gap |
|---|---|
| §4: “它的答案可能改变仓位” | The prompt says “important” but does not state the investment test. |
| §4: “写得出‘这个结果会改变哪项收入、利润、现金或信用风险、竞争位置’吗？” | The worth-tracking test is not explicit. |
| §4: “其他问题的答案不变，只有这一题相反，而对业务的判断确实不同？” | The independence scenario test is absent. |
| §4: “有一个日期和一份公开材料能把答案放进事先固定的档吗？” | Public material and verifiable rungs appear, but the test is not presented as an admission test. |
| §4: “这一条在抽取时只对同一篇文章里提出的几个问题判” | The prompt’s broad identity rule does not give the standard’s same-outcome test for candidates within the article. |
| §4: “主体、量或事件、时间依据都能在原文找到” | Source support is weaker than this explicit three-part writing check. |
| §4: “算谁、不算谁、算什么写清楚；支出、融资、担保、订单、收入不混” | This scope check is absent. |
| §4: “原文支持这个期间，不把几年的平均写成今年” | This period check is absent. |
| §3 C / §4: “规模要大到能改变公司的收入、利润、现金或信用风险才开” | D248’s single-transaction, product, and project scale test is absent. |
| §3 B: “发布、送样是它的证据，只有会分别下注的里程碑……各一题” | The prompt permits launch as an endpoint and lacks the separate-bet milestone test. |
| §3 D: “任何一家公司之外、好几家都会受它影响的量或价格” | The prompt’s aggregate-only wording omits prices and rates. |
| §3 C: “写明规模、尚未完成的入股或收购” | Pending acquisitions are not explicitly included. |
| §4 not-open list: “同一段指引里的每一行”；“后年及以后的年度量（约束性义务除外）” | The prompt broadly says not every line and gives a current/next-year limit, but does not state these boundaries as clearly. |
| §4 not-open list: “客户的部署计划……除非改变供应商自己的现金或信用风险” | Present in substance. |
| §4 not-open list: “把远期年度预测改装成事件” | Present. |
| §4 not-open list: “同一个量的另一个估计、另一种口径、另一个来源” | The prompt names these differences, but its blanket identity rule lacks the standard’s same-result test. |

## Part C — Contradictions inside the request

| Prompt texts | Tension |
|---|---|
| “take it only when it has a kind and nothing on the list applies” versus “a partner's or customer's adoption or integration … [is] not product details” | An adoption is protected from one rejection row but can still be rejected by the kind gate if it lacks the stated size, date, or name. |
| “an announcement or completed deal the item reports is a fact even when the reporter names no source” versus “rumour for claims the item credits to unnamed sources or calls unconfirmed” | An announcement explicitly attributed to unnamed sources fits both; the request does not give the standard’s priority order. |
| Role: “unless the line itself tracks such a matter” versus user block: “leave group_refs empty for a company's own financial lines” | The role allows an exception that the fixed user block omits. |
| “Return empty arrays only for a page with no business content” versus “reject these … and everything that has no kind” | A page with business content can consist entirely of rejected statements, leaving the model with incompatible output directions. |
| “a question that is already open is folded into it by code afterwards” versus “[Research groups] None yet” | The request correctly acknowledges hidden existing questions but asserts that no research groups exist even though the same ledger-blind request hides them. |
| T7: “Officially or company-confirmed events are facts” versus the role’s “an announcement or completed deal the item reports is a fact even when the reporter names no source” | The category sentence suggests a narrower fact test than the role supplies. |
| T8: “Not the author's general arguments or risk lists” versus the role’s “A named party's new claim or estimate about the company or its industry” | A new analytical argument can satisfy the role’s claim kind while being excluded by the category block. |
| Role: “for a retelling, the original speaker and statement day” versus schema `original_who`: “even when the item reports it without attribution” | The schema requires original attribution for narrated actions; the role’s phrasing can make it sound limited to attributed retellings. |

## Part D — Five findings most likely to change what is kept

This ranking is a **reasoned assessment of prompt reach**, not a measured count or a demonstrated share of errors.

1. **The four-kind gate replaces the keep test.** It can reject useful new information outside the named kinds and admit in-kind statements that do not change any research answer.
2. **The reject list lacks the standard’s boundary-first procedure.** A protected statement can be discarded under a broad rejection before the model applies the analyst’s judgment.
3. **Common knowledge is conflated with several other rejection classes.** A single “figure and a specific account” escape clause can cause the model to treat risks, views, political statements, and background differently from their separate standard boundaries.
4. **The empty-array instruction requires output for any business content.** A page containing only rejected business statements has no answer that satisfies both that instruction and the keep rule.
5. **T8 excludes the author’s general arguments as a class.** That can remove a new analytical judgment the standard would retain when an analyst would record it.

The remaining work for the requested audit is the exhaustive clause-and-example inventory, including every T1–T11 block, fixed user-message clause, and schema enum. I have not measured the impact of these differences or inspected model answers to establish which ones caused observed errors.