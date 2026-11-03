# 我到底看到了什么（证据清单，2026-11-04）

每条：看到的事实、数字、在哪能查、谁核过。v108 = 冻结版三遍（`poc/data/e2e-r9-frozen-v108-2026-11-03/d1..d3`），v94 = 上一版三遍
（`../hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94/d1..d3`）。

## A. 一道题该收的东西，模型没挂上

**E1 博通 → 自研芯片题。** 两个事实：博通季度 AI 芯片营收 108 亿美元、下季指引 160 亿。金标拿它们估"2026 年云厂商自研芯片花费"，给 600–850 亿。

| | 含这两个数的记录 | 挂到自研芯片题 | 判断最后选的区间 |
|---|---|---|---|
| v94 d1 / d2 / d3 | 7 / 7 / 7 | 2 / 2 / 0 | 400–600 亿 / 600–800 亿 / 低于 400 亿 |
| v108 d1 / d2 / d3 | 9 / 7 / 7 | 0 / 0 / 0 | 低于 400 亿 ×3 |

挂上的两遍，这两个数进了判断请求、被引用；没挂上的四遍，判断都低了。查法：Codex r2 §5 的脚本（我读过），`evidence_links where view_id='v16'`。核过：Codex、我。

**E2 同一篇里，模型把博通挂到了哪。** v108 d1 `call_id=818`：模型写了 5 条，e2 / e3 / e4（博通营收、CEO 说"增长来自定制 AI 加速器需求"、160 亿指引）
全挂总收入题，e5（目标价）空。查法：`archive.sqlite` 的 `model_calls` 818 的 `answer_json`。核过：我、Codex。

**E3 季度财报 → 全年题。** v108 d1 `call_id=214`（7 月 6 日一篇重讲一季度财报的文章）：数据中心季度收入 752.5 亿、总收入 816 亿和每股收益、二季度营收
指引 910 亿、毛利率指引 75%、现金流——模型都写了，链接全空，全被当"没家"扔掉；同一篇只有"分析师一致预期全年增长"一条挂上了。同一篇文章在 v108 d2、d3
里，季度数字又挂上了。查法：`call_id=214` 的回答 + `handovers` 里这篇的 `dropped`。核过：我、Codex。

**E4 这种"写了不挂"有多常见。** 公司自己的财报实绩或量化指引，写了却链接全空：六遍共 130 条（v94 30 / 27 / 18，v108 23 / 19 / 13），127 条最后被扔。
查法：Codex r3 逐条分类（遍历全部 243 次抽取回答的 `links == []`）。核过：Codex 逐条；我抽看过例子。

**E5 没家被扔的总量。** v108 每遍写 711 / 725 / 673 条，因没家被扔 145 / 160 / 111 条（约两成）；v94 141 / 130 / 113。查法：`nohome_census.py`。核过：脚本。

## B. 请求是怎么写的

**E6 一道题的收件说明只写"答案是什么"。** 冻结请求里：
- 自研芯片题："takes: spend_total figures, guidance, estimates and revisions for Spending on custom AI silicon (ASICs) at cloud providers in calendar 2026, this question's period 2026-01-01..2026-12-31"
- 总收入题："takes: total_revenue figures, guidance, estimates and revisions for Nvidia FY2027 total revenue, this question's period 2026-02-01..2027-01-31"

系统提示词："the narrowest open question whose takes line covers it"。开题规则："Do not propose theses about quarterly figures or guidance"。`links` 定义里
有"or through the demand, supply, competition or pricing behind its answer"，也有"an estimate for another period … is filed under it when no open question
covers that period"（只说估计，没说实绩），以及兜底："when no specific question is connected, a statement that moves the demand, supply, competition or
pricing behind the company's results goes to the company-wide revenue question of its period"。查法：`broadcom-request-v108-d1-call818.json`。核过：我、Codex。

**E7 模型本人怎么说（规则原文放进问题，独立问两次）。** 第 1 次：v16 收的是"Spending on custom AI silicon at cloud providers"，博通营收"not a
supplier's revenue"，按兜底挂了总收入。第 2 次："I should have linked e2 to v16 as well"。查法：`probe-broadcom-filing-with-rule.txt`。局限：去掉了
结构化输出；两次各自独立，不是追问说服；是事后解释。

## C. 结构怎么把读错变成损失

**E8 挂不上就扔。** 代码：没链接的证据记 `no home` 扔掉（`extraction.py` 的交接处）。E3、E4、E5 都经过这一步。

**E9 代码删上级链接。** `extraction.narrowest_links`：一条同时挂了题和它的上级题，只留下级。v108 每遍受影响 31 / 27 / 40 条（v94 178 / 218 / 185）。
确有误删：博通那篇 e1"总收入 816 亿、数据中心 752 亿"挂了总收入和数据中心，只剩数据中心；Marvell"750 亿机会"挂份额和自研芯片，删了份额。判断读的是
"它依赖的题的结论"，依赖存的是"数据中心题依赖总收入题"，所以总收入题读不到数据中心题。查法：`pruning_census.py`、`dependencies` 表、`judging.py`。核过：我、Codex。

**E10 收容所搬家。** 总收入题链接：v94 52 / 52 / 71，v108 143 / 135 / 140；数据中心收入题：v94 179 / 209 / 210，v108 96 / 113 / 92。两道加起来两版差不多。
v108 d1 总收入 143 条里（抽读）有一季度营收被多家重复报、英伟达生态小新闻（Palantir 用 Nemotron 4 条、LangChain 5 条）、别家公司（博通）。查法：
`sink_census.py`、`e2e-funnel-r9-frozen-v108.txt`。核过：脚本 + 我抽读。

**E11 兜底是怎么来的。** 上一版每道数字题说明结尾都有"以及背后的需求、供给、竞争、定价"——间接材料能进窄题，但数据中心收入题成了收容所。去掉结尾、
不加兜底（v74f）：杂音 53，但 82 条该收的写了没题挂，辅助 95 → 70；去掉结尾、加兜底（v74h → 冻结的 v74i）：辅助回来，收容所搬到总收入。
查法：`../2026-11-01-e2e-loop/design-v78-fields.md` §13。核过：我（当时的测量）。

## D. 量具本身的毛病（所以上面的数字只当方向）

**E12** 我按"文章编号 + 词重合"对照金标：同一事实换家媒体认不出、相似的话会认错、同一材料编号里金标用的可能是另一个数（Codex r1、r2）。所以"挂对
177 / 459"之类只当方向，不当结论。

## 为什么我推荐那条规则

E1–E4 是同一个样子：分析师会拿来估答案的东西（代理、季度、驱动），模型不挂，因为 E6 里一道题被写成"它的答案是哪个数"。E11 说明兜底是为补这个洞
才加的，E10 说明它成了收容所。E8、E9 说明一旦没挂上或挂得不全，代码直接丢掉。所以要改的是"一道题收什么"的定义，并且不再让代码因为上下级删用途、
不再有收容所。

## 什么结果能证明我错了

改了"一道题收什么"的写法、去掉兜底后，在 E2、E3 那几篇存档上重发：
- 博通的数还是不进自研芯片题 → 不是定义的问题，是别的（比如模型不认"供应商营收能推买方花费"这个经济关系）。
- 季度财报还是空链接 → 是别的句子在起作用（比如"不要为季度开题"被读成"不要挂季度数"）。
- 不该收的背景和小新闻挂进了更多题 → 规则放得太宽，杂音会涨，这条路要收窄。
