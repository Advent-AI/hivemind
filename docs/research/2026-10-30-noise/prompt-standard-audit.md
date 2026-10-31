# The extraction request (role-v53, poc-v69) against the signed standard (version 4), clause by clause — 2026-10-30

Alex, 2026-10-30: "你需要同时仔细检查prompt和判法准则矛盾的问题，出现很多次了，你应该要做很细的检查".

What was read: everything the model reads for one item — `role-v53.txt` (system), `categories-v53.json` (the T1–T11 "what" and "read"
blocks), the fixed sentences of the user message (`extraction._build_prompt_english`), the schema's field descriptions (`FIELD_NOTES`,
version 53) and enums — against `docs/prd/05-extraction-standard.html` version 4 (§2–§5, the flow at the top, the 12 + 7 decided items).
Two complete requests as sent are beside this file (`request-t7.txt`, `request-t8.txt`).

Two readers, apart: Claude, clause by clause; Codex read-only and blind to Claude's list (`codex-audit-prompt.md` → `codex-audit.md`,
66 clause rows). Every finding below was checked against both texts by Claude; "found by" says who found it first: C (Claude), X (Codex),
CX (both).

Why the earlier check missed the largest one: `ledger-standard/prompt-audit-v29.md` (2026-10-29, 2.9 KB) judged "四类陈述和例子" consistent
as a block. Each kind does have a source; what contradicts the standard is the procedure that makes the kinds decide. A clause-level read
of the procedure sentences, not of the kinds' wording, is what finds it.

## 1. Keep or reject (the noise class — this slice)

| id | prompt, quoted | standard, quoted | verdict | by |
|---|---|---|---|---|
| N1 | role L4 "A material statement is one of four kinds." | §5.1 "它们通常是下面四类之一；四类描述的是会记的陈述长什么样，不是'属于四类就一定留'，留不留由上面的规则判"; record convention "四类只是金标里的标签，不进账本，不影响留不留" | CONTRADICTS: the kinds become the definition of what is kept | CX |
| N2 | role L5 "For each statement, name its kind and check it against the list below; take it only when it has a kind and nothing on the list applies." | §5.3 end "不在清单上的句子，用 5.1 的规则逐句判（分析员会不会记）"; flow "分析员会记 → 留为证据" | CONTRADICTS: a statement on no list row is kept when it has a kind; the standard judges it by the analyst test. The model's own account names this sentence for an officer's pay (kind 1), a model release (kind 1), a partner's reactor (kind 2), a tie-up restated (kind 2), an IRR scenario and a fund manager's verdict (kind 3), an export ban in force for years (kind 4) (`probes/`, quoted in §5 below) | CX |
| N3 | role L6 "reject these, even when a named party states them, and everything that has no kind" | §5.2 "下面的不留清单不能用来删掉分析员会记的陈述" (D240: "a reject rule never removes what the standard keeps") | CONTRADICTS (reverse side of N2): lacking a kind becomes a veto | X |
| N4 | the standard's deciding question is absent | §5.1 "整体倾向谨慎，对增量敏感……判一句话之前先问：这是新信息吗？它让哪个问题的答案变了？一件新发生的事、一个新数字、一个新的具体判断，是增量，不能漏；重复常识、描述长期状况、泛泛的看法，是杂音" (D243) | MISSING | CX |
| N5 | role L10 "common knowledge … unless it gives a figure and a specific account" | §5.1 "这类陈述没有数字和具体的叙事就不收"; "有数字也要过上面的规则：作者说'英特尔多年领先，占 CPU 市场 59%'，和英伟达的问题关系不大，分析员不会记" | CONTRADICTS: a necessary condition is written as a sufficient one. The model kept exactly the standard's own example (Intel 59%) and named the figure as the reason | CX |
| N6 | role L10 "(an official's order, law, bill or ruling is kind (4), not a view)" | §5.3 political row, boundary "官员宣布的政策步骤不能用这一行删掉，按 5.1 判（第 4 类）" | WIDER: the standard protects a policy step from this row and then judges it by 5.1; the prompt, with N2, keeps every policy mention, including a ban in force for years retold as background | C |
| N7 | role L10 folds four rows into one "common knowledge" entry with one escape clause | §5.3 rows "作者的一般性风险清单和没有推导的看法" (boundary "有假设、有推导、有时点的条件估值要留"), "记者的背景和框架", "没有数字也没有决定的政治、战略表态" | CONTRADICTS (structure): one escape clause replaces three different boundaries | X |
| N8 | the "已知事实的重述" row is absent | §5.3 "已知事实的重述：两个月后再说一遍 Q1 收入、指引、已公布的回购"；boundary "重提的过去实际数可选；重提的季度指引和仍然有效的预测、计划按本来分量；看不出是旧事的不算重提" (D243 item 6) | MISSING: restated partnerships, a policy in force, last quarter's results retold have no row; with N2 they are kept | CX |
| N9 | fixed closing sentence "Return empty arrays only for a page with no business content." (`extraction.EMPTY_LINE_FROM`, D199) | §5.1 "杂音很大，不是什么都要抽"; nothing in §2–§5 requires a page with business content to yield a statement | CONTRADICTS: a page with business content and nothing an analyst would note (a game-driver blog, a monthly game list) cannot be answered empty. Census: 31 of 118 dev articles have no core or supporting gold entry; v53 keeps 68 statements a draw on them (20 of 31 answers non-empty; three draws: 63 gold not-kept, 95 outside the gold, 46 optional) | CX |
| N10 | T6 read "Events, including executive changes, acquisitions, new products, buybacks, partnerships, investments and financing guarantees; published operating figures; amounts and timetables." | §5.3 product row (a product without business scale is not kept); §4 not-open list "高管任免"; §5.1 keep rule | WIDER: the reading target names executive changes and new products as things to read out with no keep test beside them; the officer-pay and open-model-release statements come from T6 items | C |
| N11 | T7 read "What happened, when and who was involved; attribution, including the original source and statement day; quoted figures." | §5.1 keep rule; "有数字也要过上面的规则" | WIDER: "what happened" and "quoted figures" with no keep test | C |
| N12 | T8 read "the facts and figures the author cites, with their original attribution" | §5.3 "已知事实的重述"; "有数字也要过上面的规则" | WIDER: every cited fact and figure, including the restated quarter and the market-share background of stock articles | C |
| N13 | T8 read "Not the author's general arguments or risk lists." | §5.1 "不是常识的，是新信息，比如一份新报告的判断……分析员会记就留"; §5.3 row "作者的一般性风险清单和没有推导的看法" | NARROWER: "general arguments" can remove a new argued judgement; the row rejects general risk lists and unargued views | X |
| N14 | role L7 "the company's own claim to beat rivals is still a product detail" | §5.3 product row, boundary names only "对手拿它和本公司产品比的说法" | NO-SOURCE (a rule the standard does not state) | CX |
| N15 | role L7 "retail price" and the example "a retailer marks one model down by $50" | §5.3 product row "没有业务规模的产品、游戏、驱动、跑分细节" (examples: wattage, benchmarks, interfaces, support cycles) | NO-SOURCE for retail price; a rival's price cut is kind 2 in §5.1 ("对手在欧洲降价 15%") | C |
| N16 | role L8 "a share-price move or the market value" | §5.3 "在研公司的估值倍数、市值、孤零零的目标价可选" | NARROWER on an optional item (no score effect: optional entries are never penalised) | CX |
| N17 | role L8 "though the news a move reacts to is kept" | §5.3 "股价反应背后的那条新闻不能用这一行删掉，按 5.1 判" | WIDER: protected from the row, then still judged by 5.1 | X |
| N18 | role L13 "company boilerplate, bylines, forward-looking-statement text." | §5.3 模板 "署名、作者简介、经纪商页脚、前瞻性声明、广告；页面上和本文无关的内容（相关文章预告、推荐列表、别的新闻标题）" | NARROWER (one gold not-kept "template" kept in three draws) | CX |
| N19 | role L11 "the same fact … told in several sentences … is one evidence item" | §5.3 同一事实的复述, boundary "标题和正文说同一件事"; record convention "标题里的说法和正文是同一条证据" | CONSISTENT in rule, NARROWER on the title. The rule exists and the model, asked, says it applied and was not followed (one AI Compute Partnership page: e1 and e3 the same programme): a per-send lapse, not a missing rule | C |
| N20 | §5.2 protections are absent as a set | §5.2 "预测、传闻、反证、远期、条件情景都是证据……不因为'还没发生''不是官方''离现在远''和我们方向相反'就不留……有名有姓的动作缺金额、缺日期也是证据" | MISSING. Not a source of noise, but the guard any change to N1–N3 needs: without it, removing the kind gate can drop forecasts, rumours and unsized named actions | X |
| N21 | T2 read "risks and changes described in risk factors" | §5.3 "作者的一般性风险清单" applies to authors; a company's changed risk factor is kind 1 | WIDER only for unchanged risk-factor text (few periodic reports in the bench) | C |
| N22 | T4 read "the focus of analysts' follow-up questions" | no line | NO-SOURCE (no call transcript in the bench) | C |

Consistent (no change): the walk from the first paragraph to the last and "a page with eight such statements yields eight evidence
items" (§5.1, D199); the four kinds' wording and examples as descriptions (§5.1; the kind-3 valuation example matches "带推导的条件估值");
the product row's competitor-comparison and adoption boundaries; the D238 row; the characterising-quote row (D243 item 10); verbatim
quotes (D236); "report plans as plans".

## 2. Record fields (the next class)

| id | prompt, quoted | standard, quoted | verdict | by |
|---|---|---|---|---|
| F1 | role L17 "Identify the speaker and, for a retelling, the original speaker and statement day." against schema `original_who` "even when the item reports it without attribution" | §2 "说话人、原始说话人和原始日期（不知道就写不知道，不填报道日）"; §5.4 谁 | internal CONTRADICTION (role narrower than schema) | CX |
| F2 | schema `original_who` "the outlet or author only for its own estimate, analysis or unnamed-source report" | §5.4 谁 "原始判断者"; signed gold's who column "一位未具名高管（对《金融时报》说）" | CONTRADICTS for an unnamed-source report: the relay is named as the original party | X |
| F3 | schema `original_day` "the publication day only when the item is that party's own release, filing, call or analysis" | §5.4 "原始发言日不知道就写不知道，不能填报道日" | NARROWER: a party's own document can retell an earlier statement | X |
| F4 | role L17 tier sentence: no order, no mixed-record rule, no residual row | §5.5 "一句话同时符合两行时，取表里上面那行" (D243 item 9); row 5 "以上都不是、又没有出处的说法 → 传闻"; "按主要说法定层，次要部分的性质写进摘要" | NARROWER (role-v55 moved the table to the schema and was refuted on its small sample, loop log row 32) | CX |
| F5 | T7 what "Officially or company-confirmed events are facts" | §5.5 row 2 "文章报道的公告或已完成的交易（即使记者没写出处）" | NARROWER, against the role's own sentence | X |
| F6 | role L16 one_line "who did or said what, how much and for which period" | §5.4 six cells incl. "什么条件：推导的假设；计划、上限、'最多'" and "预测还是已发生"; "条件不能只放在旁边另一条里" | NARROWER: the condition cell is not asked for (the summary-line defect: 11 of 102 lose a condition) | CX |
| F7 | role L18 "do not infer committed funding, orders, deliveries or revenue" | §5.4 "没有来源证实的结论，可以作为分析员的推断写出，但不能写成来源说的事实" (D218) | NARROWER (forbids a marked inference) | CX |
| F8 | schema field `event_time`, required, no description | no reader in the pipeline (handoff plan T1) | NO-SOURCE field: the true day went here instead of `original_day` under v51 | C |

## 3. Opening (the step after this one; listed, not changed now)

| id | prompt, quoted | standard, quoted | verdict | by |
|---|---|---|---|---|
| O1 | role L21 main_driver "launches or starts shipping" | §3 B "哪天走到能带来收入的那一步（通常是开始出货）；发布、送样是它的证据" (D248 item 3) | WIDER (launch as an endpoint: "Will Nvidia launch Kyber" beside "begin shipping") | CX |
| O2 | role L21 "industry_aggregate: one aggregate quantity for one calendar year"; enum `industry_aggregate` | §3 D "任何一家公司之外、好几家都会受它影响的量或价格"; "现行提示词和代码还叫 industry_aggregate，按这一页改" (B1, D191, D243 item 2) | NARROWER: prices and rates cannot open — the DRAM contract-price must-open is opened in no draw | CX |
| O3 | role L21 binding_obligation "an equity stake whose size is stated and is not yet completed" | §3 C "写明规模、尚未完成的入股或收购" (D243 item 7) | NARROWER: acquisitions absent — the $12.9B Hugging Face acquisition (test set) is opened in no draw though its statement is kept every draw | CX |
| O4 | role L21 "whether or not the item gives its amount"; no scale test | §3 C / §4 test 1 "规模要大到能改变公司的收入、利润、现金或信用风险才开" (D248 item 6) | WIDER | CX |
| O5 | §4 tests 1–3 and the granularity sentence are absent | §4 "写得出'这个结果会改变哪项收入、利润、现金或信用风险、竞争位置'吗"; "其他问题的答案不变，只有这一题相反"; "只有会单独下注的大事开题，鸡毛蒜皮不开题" | MISSING | CX |
| O6 | role L23 "a different quantity, period or decision is another" | §4 "同一个结果能判掉两题，就是同一题；答案能分开走、而且分析员会分别下注的，才是另一题"; deadlines (D248 item 2) | CONTRADICTS (within one article: Kyber by 2027 and by 2028) | CX |
| O7 | role L28 "Separate independently meaningful outcomes." | §3 "能各自朝相反方向走、而且分析员会分别下注的部分要分开" | NARROWER test, WIDER splitting | CX |
| O8 | role L21 "an obligation a universe company takes on" | §3 "名单外不能忽略" (D155, D187) | NARROWER | X |
| O9 | role L33 sentiment rung labels | §3 "标的问题的档描述业务结果" (D186; B15: code still requires the labels) | known conflict B15, code-owned | X |

## 4. Other request text

| id | text | verdict | by |
|---|---|---|---|
| R1 | user block "[Research groups] None yet." under a ledger-blind version | wrong statement: the groups are hidden, not absent (no effect on what is kept) | X |
| R2 | user block "leave group_refs empty for a company's own financial lines" against the role's "unless the line itself tracks such a matter" | internal inconsistency (§2 has the exception) | X |
| R3 | role L1 "folded into it by code afterwards" | matching and the collision judge (models) fold candidates; code only for shared quantities (§2, D190, D197) | C |

## 5. The model's account (9 probes on stored role-v53 answers, run U draw 1)

| case | kept because (the model's quote) | list line it checked, and why it did not apply |
|---|---|---|
| an officer's pay terms (8-K) | kind (1) "The company's own figure, guidance or decision" | product-detail line: "not a product detail" (no row for pay) |
| an open model's release | kind (1) "decision" | product-detail line: "a release, not a feature" |
| a partner's reactor going critical | kind (2) "a dated, quantified figure about a partner's reactor" | — |
| a chip tie-up restated in a stock article | kind (2) "a named partner tie-up" | product-detail line; "in hindsight … no size, date or business scale" |
| export bans "already implemented" | kind (4) | common-knowledge line: "an official's order … is kind (4)" |
| "Intel … holds more than 59% of total CPU market share" | (quotes the article) | common-knowledge line: "gives a specific figure" |
| a research firm's modelled neocloud margins | kind (3) | common-knowledge line: "specific figures and a modelled relationship" |
| a fund manager's verdict on a delay | kind (3) | common-knowledge line: "a named expert's specific claim" |
| two records of one programme | — | same-fact line: "It did apply … should have been consolidated" |

Eight of nine: a kind, and no list row that stops it (N2, with N5 or N6 as the escape). One: a rule that exists and was not followed (N19).
The three probes of 2026-10-30 (`ledger-standard/fields-2026-10-30/probe-noise1..3.txt`) say the same: kind (3) plus "a specific
account"; the adoption carve-out of L7.

## 6. What the noise arm changes, and what it leaves

The noise arm takes N1–N9 (one decision: what keeps a statement, including when a page may be empty), guarded by N20. N10–N12 (the
category reading targets) are left for a second arm if the first leaves T6/T7/T8 noise standing, so their effect can be told apart.
N13–N18, N21, N22 are small or optional-only and are fixed where an arm already touches the same sentence. F1–F8 are the next class;
O1–O9 the opening step.
