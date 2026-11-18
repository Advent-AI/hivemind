# Blind reader, matter census batch 1 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 35 articles (numbers 1 to 35,
2026-09-07 to 2026-09-08, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
tests: the answer can change a position; a date and public material can settle it; no question already asks the same). You have no other
material: system answers and reference answers exist and you must not see them.

Read every article in full, first paragraph to last. For each article, list every question worth tracking on its own that it raises: a big
matter (it can change NVIDIA's revenue, profit, cash, credit risk or competitive position, or it is a quantity or decision in the world that
many companies depend on), with an outcome a dated public release, filing or official decision can settle. Small matters, background, a
repeat of what an earlier article already raised (list it again only under the same matter key), a stock-price or valuation view, and anything
no public material can settle are not questions. Most articles raise none or one; say "none" when none qualifies.

Then merge: one matter = one underlying bet, whichever articles raise it; another year of a figure is another matter; two questions are one
matter only when the same outcome would settle both and their answers cannot move apart.

Write one JSON object per line, and nothing else:
- per question: {"article": n, "matter": "<short key>", "question": "<the question, with its period or check date>", "quote": "<= 40 words from
  the article>", "reason": "<the §3 reason and why it is big, <= 30 words>", "settled_by": "<the public material and when>"}
- per article with none: {"article": n, "matter": null}
- finally, per matter: {"matter": "<key>", "name": "<one line>", "articles": [n, ...]}

## The signed standard, §3 and §4

3问题的五类：账本的几大类型

开题理由是 D184 定的四类，D236 把主驱动量扩到产品节点，所以写成五类。判两件事，互不顶替：这是谁的问题（标的还是主题）；为什么值得开（开题理由）。

类开题理由标的或主题问什么量还是事件期间和到期核对材料 settled_by出处

A 主驱动量main_driver标的承载公司价值的那个年度量，不管公司指不指引：撑起业务的分部收入、毛利率、资本开支；跨行业如银行的净利息收入、零售商的同店销售、公用事业的费率基数、航空公司的燃油成本（当它是争论焦点时）。不是每一行报表数量，五档公司财年的今年或明年；到期日是这个数的发布日公布这个数的公开材料，通常是年报D184：settled_by 是 "the public material that resolves it"；PRD 06 梯子第 5 条

B 主产品节点main_driver标的承载公司价值的那一代产品哪天走到能带来收入的那一步（通常是开始出货）；发布、送样是它的证据，只有会分别下注的里程碑（新药的三期数据和获批）各一题D248 第 3 条事件，五档，或是非两档PRD 06 梯子第 1 条能判出结果的那天公司公告、发货确认D236

C 约束性义务binding_obligation标的公司以自己名义承担的：为别人的债务、租约或收入担保或提供信用支持；借钱给别人；承诺购买（向别人买产能或服务也算）；为客户的产能或收入兜底；或写明规模、尚未完成的入股或收购D236；收购按 D243 第 7 条。规模要大到能改变公司的收入、利润、现金或信用风险才开；够不上的单笔入股、收购、租约、授信不开题，陈述留不留照第 5 节判D248 第 6 条。不算：自己借钱、自己的租约、已完成或没写规模的投资。D239 选定的 role-v29 原文："Its own borrowing, its own leases and a completed or unsized investment are not obligations"；D238 的记录写作 "the company's own borrowing and leases and a completed or unsized stake do not"还没签：是非两档。已经承担（一笔或一个计划）：金额，五档检查日最多在文章后 18 个月D185；已承担的按下一份年报签约公告、年报承诺附注D184、D185、D210、D236、D238、D243

D 共同量shared_quantityD191、D243 第 2 条；现行提示词和代码还叫 industry_aggregate，按这一页改主题任何一家公司之外、好几家都会受它影响的量或价格：几家公司的合计（云厂商资本开支）、价格（内存合约价、油价）、利率。同一总量的另一种人群、另一种说法是这个量的证据量，五档自然年的今年或明年。同一个量、同一年只有一个问题，由代码按"主题＋量＋期间"判D197；量的类别是 other 的不算几家公司年报、统计发布、官方决定D184、D191、D197、D243；PRD 06

E 政策阶段policy_stage问的是一家公司的收入、利润、份额或产品进度，算标的，即使由政策驱动；问的是世界上的事（许可制度、利率、合计支出），算主题。D184 采纳的 role-v12 原文："A question about a company's revenue, profit, share or product progress is an asset thesis; put its ticker in object, even when policy or macroeconomics drives it"一个政策或监管过程到了哪一步，写明谁说了算事件，五档或两档能判出那一步的那天。文章没写日期的待决监管事项，用本财年末（role-v12 原文："A pending regulatory decision may lack a date; use the current fiscal year-end as its due date"）；这个日期是研究员定的检查日，要标明评审 §1 第 1 条官方决定、公报D184

例子（跨行业）：

A：NVIDIA FY2027 数据中心收入；一家地区银行 FY2026 净利息收入；一家公用事业公司 2027 年费率基数。

B：下一代机架系统能否在 2027 年底前开始出货；一家车企的新平台能否在 2026 年内开始交付。

C：NVIDIA 为云客户产能兜底的义务在 FY2027 年报达到多少；一家保险公司是否在 2027 年中前为合资公司 5 亿美元债务签署担保。

D：五家最大云厂商 2026 年合计资本开支；2027 年 DRAM 合约价相对 2026 年的变化、美联储 2026 年最后一次会议后的利率上限。

E：中国是否在 2027-01-31 前正式批准本国公司进口 H200；美国是否在某日前对某类芯片实行出口许可。这两题问的是许可这件世界上的事，所以是主题，role-v12 原文的例子就是 "licensing"。一个监管决定对一家公司收入或产品进度的影响，问成那家公司的量或产品节点时，是标的问题（同一句原文）。

五类之外的东西去哪

七类驱动不是问题类型。它们是一条陈述为什么重要的理由，用来判分量和归档。D208 设计的"每家公司种下的驱动问题"由分析员开始覆盖时写好，不从文章里开；还没建。

别家公司自己的量（对手的份额、客户的资本开支）：D187 定了"任何公司自己的量是那家公司的问题，私营公司也算"，但还没实现，要先在覆盖名单里加私营公司这一类。D155 定了"公司清单可以作为初始参考，但清单外不能忽略"。现行代码在匹配时跳过名单外的对象PRD 06 Step 4。所以抽取照常可以提这样的问题，它要过第 4 节的测试；名单外的现在会被匹配跳过，这不算抽取错。

宏观量（利率、通胀）：按 D 类共同量开题D243 第 2 条。只来自一篇纯宏观文章时，只有主题在名单上才开D191 第 3 条。宏观对每家公司的正负，在判断那家公司时读主题块决定D191 第 1 条、D195。

开题理由是封闭的D184：一件事属不属于五类之一，按上表逐条看，比如一个监管决定看它是不是 E 类。哪一类都不属于的不开；它是不是证据、挂到哪，照第 5 节和归档规则。

问题怎么写：PRD 06 的梯子规则，不重写

一个问题只问一个量的一个期间，或一件事；能各自朝相反方向走、而且分析员会分别下注的部分要分开PRD 06 梯子第 3 条；"分别下注"是 D248 加的，PRD 06 签字后更新，分开的每一题都要过第 4 节的测试。

写成问句，不写成断言PRD 06 Rationale。

结果档可核对、不重叠、不留缝，到期恰好一档成立；中间一档写明和什么比；"小幅""部分"这种不能核对的说法不用，部分状态写成单独一档PRD 06 梯子第 2 条。标的问题的档描述业务结果；主题问题的档只写结局，不写好坏PRD 06、D186。

到期日：量是它的发布日；事件是能判出结果的那天。公司的量用公司财年，别的用自然年，只开今年和明年PRD 06 梯子第 5 条；约束性义务例外，D185。

4开题标准

一个问题值得单独追，要同时满足三件事：它的答案可能改变仓位；能在一个日期用公开材料判出落在哪一档；库里没有问题在问同一件事。开多少个是判断的结果，不是目标第 1 版 §6；评审 §1。

颗粒度按一个高端对冲基金分析员：只有会单独下注的大事开题，鸡毛蒜皮不开题（它的陈述留不留照第 5 节判）；同一个赌注的几种说法是一题，截止日、里程碑、财年和日历年各按本节"同一题、续期，还是另一题"里的那一条判D248。

另有一条前提：新问题要有独立的投资判断；一个新产品、一个新数字、一个更窄的范围，单凭这些不开D201。

四个测试第 1 版 §6

值得追写得出"这个结果会改变哪项收入、利润、现金或信用风险、竞争位置"吗？写不出就留作证据，不开题。"数字很大"不算理由。单笔交易、产品、项目，规模够不上改变公司的收入、利润、现金或信用风险的，不开题，陈述留不留照第 5 节判D248 第 6 条：问的就是小交易、小产品；这一测试的其余理由（包括竞争位置）不变。

独立意义能写出两个情景吗：其他问题的答案不变，只有这一题相反，而对业务的判断确实不同？写不出就优先作为证据评审 §1 第 3、8 条。评审里的一个判例：NVIDIA FY2027 总收入题判为数据中心收入题的证据，理由是"该段明确说主要增长来自数据中心，未提出独立的其他业务争论"。这是对那一段材料的判断，别的材料要逐个判。

能核对有一个日期和一份公开材料能把答案放进事先固定的档吗？没有就重写问题。到期没有材料记"未能判定"，不算错。

不是重复和已有问题比，只是预测值、措辞、来源、方向或同一总量的另一种口径不同，最终核对的是同一个结果吗？是就是同一题。抽取看不到库D211，这一条在抽取时只对同一篇文章里提出的几个问题判；和库里的比由匹配做。

另外三条写法检查评审 §1 第 1、5、6 条。没过的问题不能照原样开，要重写；重写不了就不开，材料作证据。

原文支持：主体、量或事件、时间依据都能在原文找到。原文没给日期、而规则允许研究员定检查日的，用那个日期并标明：没写日期的待决监管事项用本财年末（第 3 节 E 类）；还没签的约束性义务用文章后 18 个月以内能核对签约的那天D185、D210。不把"拟议""预计"写成"已签""已完成"。

口径完整：算谁、不算谁、算什么写清楚；支出、融资、担保、订单、收入不混。

时间正确：原文支持这个期间，不把几年的平均写成今年。

不开的第 1 版 §6 的清单

不开出处它变成什么

季度数字和季度指引第 1 版 §6；PRD 06 梯子第 6 条证据

同一段指引里的每一行（"费用率、税率是模型输入，不是争论"）第 1 版 §6证据

没日期的"护城河""战略"第 1 版 §6证据

高管任免、股东投票、回购授权；章程第 1 版 §6；章程出自 D239 选定的 role-v29 原文（"executive appointments, shareholder votes or bylaws"）证据或不留

例行诉讼程序第 1 版 §6证据

客户的部署计划（"它是供应商需求和产品问题的证据，除非改变供应商自己的现金或信用风险"）第 1 版 §6证据；改变公司自己的现金或信用风险时按 C 类判

以约束性义务为理由开：公司自己借钱、自己的租约、已完成或没写规模的投资。它们不是约束性义务；对别的问题仍可以是证据，或按别的开题理由判D236、D238证据

把远期年度预测改装成事件第 1 版 §6证据

后年及以后的年度量（约束性义务除外）PRD 06 梯子第 5 条；D185证据

同一个量的另一个估计、另一种口径、另一个来源第 1 版 §6 测试 4那个已开问题的证据，由匹配并入

同一题、续期，还是另一题：匹配这一步的事，抽取不判库里的

总规则：同一个结果能判掉两题，就是同一题；答案能分开走、而且分析员会分别下注的，才是另一题D248。

同一题：同一个结果能同时判两个问题。另一个估计、来源、措辞、方向第 1 版 §6 测试 4；同一总量的另一种人群或代用口径（D190 碰撞裁决提示 collision-v1："another population or proxy of one aggregate"；D197 引的 role-v12 原文："another population or another wording of the same aggregate is evidence to the shown aggregate thesis"）。候选并进已开问题，用它的结果档和到期日PRD 06。只有以共同量理由开题、带量的候选由代码自动判，其余是匹配和碰撞裁决的判断。

同一个计划的几种说法（担保、融资承诺、信用支持……），最后核对的是同一个数，是一题D248 第 1 条。

同一件事的不同截止日：早的那题开着时，晚的截止日是它的证据，不另开；早的到期没有结果、事情还在追，系统开下一个截止日的续期题，带上并进来的证据，不等新文章D248 第 2 条。

同一代产品的几个里程碑：一题，问能带来收入的那一步（通常是开始出货）；送样、发布作证据；会分别下注的里程碑（新药的三期数据和获批）各一题D248 第 3 条。

公司自己的量：只按财年开题；按日历年的估计是财年那题的证据，两种年份差得多时分量低一点D248 第 4 条；PRD 06 梯子第 5 条。

身份：事件和政策题里模型写的期间起点，不拿来挡合并；对象、事件、截止日照旧核对D248 第 5 条。

续期：同一个量或同一串事件的下一个期间PRD 06 Succession、D190。

另一题：同一件事里答案能分开走、分析员会分别下注的：有自己驱动的组成部分；同一笔交易或同一份附注里两个各自会变、分别盯着的数；另一件事D190 碰撞裁决的四种；D248 第 1 条收窄了"担保和融资"。

约束性义务："一笔或一个计划"一题D210；一笔交易是不是某个已按金额开题的计划的一部分，由匹配判，是就并入D248 第 1 条。还没签的单笔交易是"签不签"的是非题，照旧可以开，不并进计划的金额题D210；PRD 06；D248 未改。

共同量：以共同量理由开题、带量的候选（量的类别是 other 的不算），由代码按"主题＋量＋期间"判同一题；政策阶段和别的事件保留按事件判的身份；不带这个开题理由的主题量由模型判D197。

谁判，谁查

内容谁

测试 1–3、同一篇文章里的测试 4、属于哪一类、问题怎么写抽取的模型（判断）

结果档形状、期间是真日期、到期在文章之后、季度数、年限、约束性义务 18 个月、settled_by 不为空代码：只查形状，不判重要性D154、D155、D184

和库里的同一题、续期、另一题匹配（Jev）和碰撞裁决D190；共同量由代码D197

年限按公司财年数：2026 年 7 月时 NVIDIA 在 FY2027（2027 年 1 月结束），所以 FY2028 是明年。代码原来按自然年算，把 FY2028 当成后年拒掉；在 v29 答案的 40 个带年份的候选里拒错了 2 个。已修，测试是 tests/test_fiscal_year_horizon.pyD243。

## The articles

### Article 1 · 2026-09-07 · wccftech.com
NVIDIA DLSS 5 Cripples Most PCs in Modded Games, but DLSS 5 Autopilot Restores Playable Performance

Following its reveal earlier this year, NVIDIA DLSS 5 Neural Rendering is officially available, though only in a single game so far, NBA 2K27 , which generally does a great job showcasing how the new tech can work wonders in games with realistic visuals . Still, modders have started adding Neural Rendering to games that do not support it yet natively, revealing how demanding the tech is in its current state
However, modders have done what NVIDIA has yet to do, significantly improving DLSS 5 performance by introducing the same modes that are available for DLSS Super Resolution - Quality , Balanced, and Performance .
This significant breakthrough has been achieved by the developers of DLSS 5 Autopilot . In its vanilla version, NVIDIA DLSS 5 is applied to the output resolution, so a lower internal resolution has no impact on performance. With DLSS 5 Autopilot , however, Neural Rendering is activated before the upscaler is, allowing for the implementation of the same modes of Super Resolution . Needless to say, this results in a lower quality, but still, the performance improvements are worth it, considering how demanding vanilla DLSS 5 currently is when injected into games that do not natively support it.
In addition, DLSS 5 Autopilot also packs DLSS5-Feeder , which allows the user to enable NVIDIA DLSS 5 in any DX12 , DX11 and DX10 games even if they do not support NVIDIA DLSS in any capacity. The results will obviously vary significantly between games depending on their visual styles, and without the developer intervention that seems to be needed to achieve the best results, many games will not look good with it, but still, this is sure to make for some very interesting experiments.
DLSS 5 Autopilot also brings Multi-Frame Generation via dashdogy's RTX40MFG-Unlock to the RTX 4000 series GPUs . However, only games that already support Multi-Frame Generation are compatible with this feature.
Although NVIDIA DLSS 5 continues to be heavily criticized by gamers, and for good reason, as it seems to somewhat homogenize the visuals of the most diverse games, there's no denying that Neural Rendering could pave the way for some big changes within the games industry. Some developers also had nothing but high praise for the technology, such as Kingdom Come: Deliverance series director Daniel Vávra , who said that characters in the second entry in the series look as intended with NVIDIA DLSS 5.

### Article 2 · 2026-09-07 · fool.com
Nvidia Stock: Is It Still a Good Buy at $230?

Nvidia ( NVDA +2.55% ) 's stock is having another terrific year in 2026, rising by around 24% thus far. Although it was initially off to a poor start, it's beating the market yet again, as the S&P 500 has risen by a more modest rate of 13%.
The tech giant has been leading the artificial intelligence (AI) revolution with its cutting-edge chips, and its recent quarterly results showcased just how strong demand remains, with its growth rate accelerating from the previous quarter.
Currently, the AI stock is trading around $230 as it approaches a new all-time high. Is it still a good buy at its current levels?
Nvidia's valuation looks low given the growth it's been generating
At around $5.6 trillion in market cap, Nvidia is easily the most valuable company in the world. What's striking, however, is just how inexpensive the stock is given its high level of profitability.
The stock trades at a price-to-earnings (P/E) multiple of 29. While that is a bit higher than the S&P 500 average of 24, it's arguably warranted given just how strong its growth has been. Nvidia's revenue for its most recent period, which ended on July 26, totaled $96.2 billion -- a whopping 106% increase year over year. That's a significant acceleration from the 85% growth it reported three months earlier.
Paying such a modest multiple for this type of growth makes Nvidia's stock look like a steal of a deal. CEO Jensen Huang also remains bullish on the future growth of the business, now that AI tokens are paying off. "AI has reached its inflection point. It's doing useful work. Its tokens are productive and profitable. Now, compute is revenue," Huang stated in the company's earnings release.
Nvidia has been a growth beast and its business looks as though it's ramping up at a time when many investors may have assumed it might be due for a slowdown, given an increase in competition. In light of its recent numbers, it wouldn't be surprising for Nvidia's stock to continue to hit new heights this year.
The one risk with the stock, however, is that it depends heavily on many interconnected tech companies and on their continued commitment to spending big on AI. If there's a pullback in AI spending, that could have a drastic and sudden impact on Nvidia's growth. While that doesn't appear likely today, if there's an economic downturn or interest rates rise, there may be increased pressure for companies to scale back capital expenditures. It's a risk that investors who buy Nvidia's stock need to be aware of, because while its valuation doesn't look all that high right now, things could change quickly.
By David Jagielski, CPA – Sep 7, 2026 at 3:00PM EST
The stock is attractive so long as tech spending on artificial intelligence remains high, which isn't necessarily a guarantee in the long run.

### Article 3 · 2026-09-07 · techradar.com
'The planets aligned': Nvidia confirms $12.9bn Hugging Face deal in potentially huge AI shake-up

'The planets aligned': Nvidia confirms $12.9bn Hugging Face deal in potentially huge AI shake-up
By Craig Hale
Hugging Face snapped up by Nvidia in $12.9 billion deal
Nvidia pays $11.9 billion for Hugging Face, and a further $1 billion in equity-based retention
The company promises to keep Hugging Face "an open platform for the entire AI ecosystem"
Nvidia CEO Jensen Huang has publicly supported open weight models
Nvidia has confirmed plans to acquire Hugging Face for $12.9 billion subject to regulatory approval, marking a major expansion for the chipmaker as it snaps up one of the most important AI model distribution platforms.
In a post , the company asserted it plans to keep Hugging Face as it is: "Hugging Face will remain an open platform for the entire AI ecosystem," CEO Jensen Huang wrote.
Huang explained Nvidia's "infrastructure, engineering and global reach" will help improve Hugging Face's "reliability, safety, model evaluation, inference and deployment capabilities."
Nvidia confirms Hugging Face acquisition
The platform currently counts more than 18 million developers, researchers and creators as users, with more than three million models shared on it.
"Hugging Face will continue to support open source and open weight models from across the ecosystem, from every model builder," Huang stressed again, noting his public backing for open weight models. Ordinarily in an acquisition, questions would be raised over whether, in this instance, Nvidia's own GPUs and software could receive preferential treatment, but the company is doing everything it can to assure us that won't be the case. A pending regulatory investigation will also ascertain this.
Nvidia also claims to be the biggest contributor to Hugging Face, having shared more than 500+ models and around half as many open datasets.
The news comes less than two weeks after reports started to circulate about a potential acquisition, and if it closes, it'll be Nvidia's biggest acquisition to date. The $12.9 billion payout comprises a Hugging Face valuation of $11.9 billion (way above its earlier $4.5 billion valuation in 2023) and an equity-based retention program of around $1 billion.
As for upcoming regulatory interjection, Nvidia warned in a SEC filing that "Government restrictions may negatively impact our business and the Hugging Face platform."
With several years’ experience freelancing in tech and automotive circles, Craig’s specific interests lie in technology that is designed to better our lives, including AI and ML, productivity aids, and smart fitness. He is also passionate about cars and the decarbonisation of personal transportation. As an avid bargain-hunter, you can be sure that any deal Craig finds is top value!

### Article 4 · 2026-09-07 · finance.yahoo.com
Jim Cramer Wants Nvidia to Buy Back $500 Billion. Can Apple’s Playbook Work?

Jim Cramer wants NVIDIA Corporation (NASDAQ: NVDA ) to authorize a $500 billion buyback and purchase shares daily. His September 1 Mad Money argument points to Apple Inc. (NASDAQ: AAPL ) as the model. Both businesses return substantial capital, but their cash demands complicate copying the same strategy.
Nvidia's quarterly filing shows $99.3 billion of remaining authorization at July 26. Cramer's half-trillion figure is his proposal. Nvidia actually repurchased $39.8 billion during the first half of fiscal 2027, including $19.7 billion in its second quarter.
The amount authorized is only the beginning
Reducing shares gives remaining owners a larger claim on future profits, assuming the business performs and issuance does not offset repurchases. Spending more is attractive when the purchase price understates those future earnings; an impressive dollar total alone cannot establish that.
Apple Inc. (NASDAQ:AAPL) demonstrates the funding side. It repurchased $61.8 billion during the nine months ended June 27, while generating $117 billion of operating cash and spending $6.8 billion on property and equipment. Its April 30 additional $100 billion authorization gives management flexibility without requiring immediate purchases.
Apple's cash generation supports continuing returns, although investors still need underlying earnings growth. Its July 30 results included a tariff refund that added $0.11 to quarterly earnings per share. Buybacks cannot make such a benefit recur, and paying too much for shares would weaken future returns.
For NVIDIA Corporation (NASDAQ:NVDA), quarterly revenue of $96.2 billion, up 106%, strengthens the earnings case. Expanding AI infrastructure also absorbs capital. Supply and capacity commitments reached $279 billion across multiple fiscal years, including $92 billion in the remainder of fiscal 2027. Those obligations support future sales, but they make preserving flexibility valuable if customer demand changes. Some agreements can be adjusted, potentially at additional cost.
Historical ownership offers perspective without settling Cramer's proposal. Insider Monkey tracked 285 Nvidia holders in Q2 2026, ten more than Q1's 275; Fisher increased its shares approximately 3%. Apple's count slipped one to 169 from 170, while Berkshire's 227.9 million shares were unchanged. These filings predate the September comments.
Nvidia's August 14 short-interest snapshot also came earlier: 285,956,804 shares, 1.23% of float and 2.5 days to cover.
Apple supplies a credible example of funding repurchases from cash generation. Nvidia can increase shareholder returns as earnings expand, but committing to Cramer's scale needs a stronger funding case than frustration with the share price. For both stocks, the price paid and profits retained per share matter more than the authorization headline.
While we acknowledge the potential of NVDA and AAPL as investments, we believe certain other AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 5 · 2026-09-07 · creativebloq.com
I saw NVIDIA's new AI video tool: why RTX Spark’s half‑frame trick might actually matter... and why creatives are right to be wary

By Design
By Erlingur Einarsson
NVIDIA's RTX Spark showcase at IFA offered both tantalising promise and unanswered questions.
AI video generation has been sprinting forward so fast that half the industry is squealing with excitement and the other half is clutching the bannister in pure terror. Every month brings a new “breakthrough”, a new “pipeline”, a new “we swear this one doesn’t melt faces”. But at IFA, NVIDIA’s Lars Weinand showed off something that didn’t feel like hype, but rather a genuine shift in how AI video might be made.
The pitch is deceptively simple: generate half the frames, let RTX Spark-powered local AI infer the rest, and walk away with a 60 FPS clip that looks like you spent twice the compute. It’s the kind of optimisation that makes engineers grin and creatives squint suspiciously.
Because yes, the tech is clever. And yes, the speed gains are real. But the implications for creative workflows - and creative labour - are more complicated than a neat demo on a show floor can fully address.
Let’s dig in.
The promise: generate less, infer more, but without the usual AI weirdness
The core idea behind RTX Spark’s pipeline is almost cheeky in its simplicity: Generate at 30 FPS (and at a lower resolution) using NVFP4 precision on a Blackwell-architecture unified memory chip (the RTX Spark platform). Then hand the output to an RTX video node that handles AI upscaling and AI frame generation. Finally, deliver a 60 FPS , higher‑resolution final video that looks like you did twice the work.
If you’ve ever used DLSS in games, you already understand the logic. But this isn’t real‑time interpolation; it’s handled entirely offline (using the RTX Spark tech powering NVIDIA 's new unified memory), with more time per frame and access to full motion flow. That means cleaner in‑betweens, fewer temporal glitches, and none of the plasticky shimmer that makes some AI‑assisted footage look like it’s been dipped in varnish.
In other words: the pipeline doesn’t just save time. It saves face.
NVFP4 + Blackwell: an efficiency play that creators will welcome?
NVFP4 is the unsung hero here. It’s a lower‑precision format that Blackwell chews through like popcorn, giving you noticeably faster inference, lower compute cost per frame, and little or no visible quality loss for typical content.
This matters because AI video generation is still compute‑hungry enough to make even well‑funded studios wince. If you’re an indie creator, a small production house, or anyone who doesn’t have a server farm in the basement, shaving minutes off every iteration isn’t just convenient; it’s the difference between “we can try 3 versions” and “we can try 30”. It promises real workflow improvements.
The benchmark from the IFA demo was eye-opening indeed:
- Full HD, two‑second clip: about 6 minutes 30 seconds
- Same clip with the half‑frame pipeline: about 1 minute 25 seconds
Even generating every frame in NVFP4 would have cut the render roughly in half. But the half‑frame strategy pushes the savings into “this changes how we work” territory.
For short‑form creators, the TikTok / YouTube /marketing crowd, this is huge. For animation teams iterating on motion, lighting, or composition, it’s possibly even bigger. And for anyone experimenting with AI video as part of a hybrid workflow, it’s the difference between “interesting toy” and “practical tool”.
The creative anxiety: speed is great, sure. But what about quality?
Where it holds up:
Weinand claimed no visible difference in the end result between a fully generated 60 FPS clip and a 30 FPS clip upscaled and frame‑generated to 60 FPS
And in the demo, that seemed true. Motion was smooth, textures held up, and the dreaded “AI slop gloss” didn’t rear its head.
Offline interpolation is simply better positioned to avoid the uncanny valley than real‑time frame generation.
Where creatives should still be cautious:
This isn’t a magic wand, and creatives know better than to trust a demo blindly. Low base FPS (10–15) upscaled to 60 will absolutely produce artefacts. Fast‑motion content, such as sports, dance, or chaotic handheld shots, may need higher base FPS. Fine textures (hair, fabric, detailed animation) can still trip up interpolation. And stylised content may behave unpredictably depending on how the model interprets motion flow.
And then there’s the bigger concern: consistency . AI pipelines are notorious for behaving beautifully in one scene and bizarrely in the next. Creatives aren’t worried about the best‑case scenario; they’re worried about the worst‑case one that ships.
Does this matter more than any other "AI breakthrough"?
RTX Spark isn’t just a speed trick. It’s a sign of where AI video is heading: toward hardware‑accelerated inference, modular pipelines, and hybrid workflows where generative models don’t have to do everything themselves.
This is good news for creators who want AI to be a tool rather than a takeover.
But it also raises the stakes. Faster generation means faster iteration, which means faster production cycles, and that inevitably feeds into the ongoing debate about creative labour, job security, and the role of human artists in an increasingly automated pipeline.
The tech is promising, but the implications are messy.
The ecosystem is already here: RTX video capabilities already exist in consumer tools like VLC, professional software across video and VFX, gaming pipelines, and CUDA‑based pro workflows.
The GitHub release rolling out post‑IFA includes AI super resolution (available now), AI frame generation (coming shortly) and an HDR module (in development).
RTX Spark’s half‑frame pipeline is one of the first AI video features that feels genuinely creator‑friendly. It doesn’t try to replace artistry. It doesn’t bulldoze workflows. It doesn’t promise magic. It just makes the slow parts faster.
But creatives are right to be wary. Speed is seductive, and the industry has a habit of using “efficiency” as a cudgel. Tools like this can empower creators, but they can also be used to justify unrealistic deadlines and smaller teams.
The tech is impressive, and the potential is real. The responsibility lies with how the industry chooses to use it.
But what's next?
How does this pipeline behave with sports footage, high‑detail animation, or VFX‑heavy sequences? What presets will emerge as the “sweet spot” for balancing FPS, resolution, and upscaling? How will the HDR module fit into professional colour workflows?
And most crucially: how will studios integrate this without destroying the human side of the creative process?
AI video is evolving fast. RTX Spark’s approach feels like a step toward a future where creators can work smarter without sacrificing quality... but only if the industry remembers that speed is a tool, not a mandate.

### Article 6 · 2026-09-07 · fool.com
If You Only Own Nvidia for AI Exposure, You're Missing Half the Trade. Here's the Other Half.

To gain some exposure to the booming AI market, many investors turn to Nvidia ( NVDA +2.55% ) , the world's largest producer of discrete GPUs for data centers. That's still a smart move, since Nvidia sells the best picks and shovels for training AI algorithms.
Most of the world's top AI companies use Nvidia's data center GPUs, and it locks in those customers with its proprietary software and services. From fiscal 2026 (which ended this January) to fiscal 2029, analysts expect its revenue and EPS to both grow at CAGRs of 59%. Those are remarkable growth rates for a stock that trades at 23 times next year's earnings.
So if you're bullish on the AI market's long-term growth, it's still a good idea to buy Nvidia . But if Nvidia is your only play on the AI market , then you're missing out on the expansion of the AI inference market. Let's see why the inference market is becoming just as important as Nvidia's training market -- and why Broadcom ( AVGO +2.96% ) is a great play on that paradigm shift.
Nvidia's data center GPUs are used to train large language models (LLMs). But that data is useless without inference, or the computing process that allows AI applications to access all that information. To help hyperscalers bridge that gap, Broadcom ( AVGO +2.96% ) develops application-specific integrated circuits (ASICs) that can be customized for inference tasks.
At scale, Broadcom's AI accelerators can process inference tasks faster and more cost-efficiently than Nvidia's stand-alone GPUs. That's why leading AI companies -- including Meta , Alphabet 's Google, OpenAI, and Anthropic -- all use Broadcom's chips to accelerate their AI applications.
Why Broadcom is another must-own AI stock
In fiscal 2025 (which ended last November), Broadcom's sales of AI chips soared 65% to $20 billion and accounted for 31% of its top line. By fiscal 2027, it expects its AI chip sales to rise nearly sixfold to $115 billion -- about two-thirds of its projected $173.5 billion in revenue.
From fiscal 2025 to fiscal 2028, analysts expect Broadcom's revenue and EPS to grow at CAGRs of 62% and 77%, respectively. Yet it trades at just 22 times next year's earnings. Therefore, Broadcom is growing faster than Nvidia but still looks fundamentally cheaper.
Nvidia has been integrating more inference features into its latest GPUs, but it will remain more closely associated with the AI training market for the foreseeable future. So if you want more exposure to the growing market for custom inference chips, you should also invest in Broadcom.
By Leo Sun – Sep 7, 2026 at 4:40PM EST

### Article 7 · 2026-09-07 · gurufocus.com
Nvidia, Microsoft at Center of $7 Trillion AI Boom

America's AI infrastructure boom could triple by 2030, creating an investment cycle beyond Nvidia's graphics processors.
The United States has approximately 90 operating data centers requiring more than 100 megawatts of power, a record, according to The Kobeissi Letter. If all planned projects are completed, that total could more than triple to 280 by 2030.
Technology companies are expected to invest about $7 trillion in data centers through 2030. Amazon, Microsoft ( NASDAQ:MSFT ), Alphabet and Meta Platforms have signed more than $1.5 trillion of data-center leases since the AI boom began, including commitments not yet effective.
Those figures show why AI infrastructure is evolving into a broader industrial spending cycle. Building compute capacity requires advanced chips, networking equipment, servers, cooling systems, electrical components, construction services, real estate and dependable power generation.
Which Stocks Could Benefit From the AI Buildout
Nvidia ( NASDAQ:NVDA ), Advanced Micro Devices, Broadcom, Marvell Technology and Micron Technology provide critical computing, connectivity or memory products. Arista Networks and Credo Technology help move enormous volumes of data between systems.
Dell Technologies, Hewlett Packard Enterprise, Super Micro Computer and Vertiv supply servers or supporting infrastructure. Digital Realty and Equinix provide data-center real estate.
The opportunity is also shifting toward electricity. Eaton, Quanta Services, GE Vernova and Constellation Energy are positioned around power equipment, grid construction, generation or energy supply.
However, the forecast is conditional. Not every proposed facility will secure financing, permits, grid connections or customers. Rapid construction could also create excess capacity if AI demand or monetization develops more slowly than expected.
Investors should distinguish signed contracts and operating capacity from announced projects. The strongest beneficiaries will not merely receive orders; they must convert unprecedented demand into durable revenue, margins and cash flow without overbuilding ahead of actual utilization.

### Article 8 · 2026-09-07 · fool.com
Berkshire Hathaway Owns AI Exposure in 3 Different Ways. Here's Why That's Not the Same as Owning Nvidia.

Berkshire Hathaway (NYSE: BRKA) (NYSE: BRKB) invests in dozens of companies across its $361 billion portfolio. However, the conglomerate isn't heavily invested in the AI boom -- and it doesn't hold a single share of Nvidia (NASDAQ: NVDA), the world's top AI chipmaker.
The three biggest AI-driven stocks that Berkshire still owns are Apple (NASDAQ: AAPL), Alphabet (NASDAQ: GOOG) (NASDAQ: GOOGL), and Moody's (NYSE: MCO). Let's see how these stocks are exposed to the AI market -- and why they're not comparable to Nvidia.
How much do these three stocks matter to Berkshire?
Apple is Berkshire's top holding, accounting for 20.2% of its portfolio. Apple generates most of its revenue from the iPhone and other hardware. Still, it's using its Apple Intelligence AI suite to increase the stickiness of its ecosystem and subscription-based services. It's also developed custom chips to run edge AI models locally rather than on a cloud-based platform.
Alphabet, which accounts for 7.4% of Berkshire's portfolio and ranks as its fifth-largest holding, is a more focused AI play. Its Google Cloud Platform and custom chips provide the infrastructure for AI applications, while its Gemini large language model (LLM) and AI upgrades for its search, advertising, and Workspace services are widening its moat and locking in more customers.
Moody's, which accounts for 3.4% of Berkshire's portfolio as its ninth-largest holding, is one of the largest providers of financial data in America. It's using AI to upgrade its economic forecasts and credit rating services, making it a more valuable platform for its enterprise customers.
But why aren't these three stocks comparable to Nvidia?
Apple, Alphabet, and Moody's are all sound long-term investments that have generated total returns of 113%, 138%, and 35%, respectively, over the past five years. During that same period, Nvidia's stock delivered a total return of 912% as the AI market expanded.
Past performance never guarantees future gains, but Nvidia still has plenty of irons in the fire. It's the world's largest producer of discrete GPUs for data centers, which are used to train the world's most advanced LLMs. Most of the world's top AI companies -- including Google, Microsoft , OpenAI, and Anthropic -- use its data center GPUs. Nvidia also locks in those customers with its proprietary software and services.
In its latest quarter, Nvidia generated 93% of its revenue from its data center chips. It faces some competition from AMD 's cheaper data center GPUs, Broadcom 's custom AI accelerators, and newer inference-oriented chips, but Nvidia will likely dominate the general-purpose AI training market for the foreseeable future.
From fiscal 2026 (which ended this January) to fiscal 2029, analysts expect Nvidia's revenue and EPS to both grow at CAGRs of 59%. Those are incredible growth rates for a stock that trades at 23 times this year's earnings. Apple, Alphabet, and Moody's -- which are all growing at much slower rates -- trade at 36, 16, and 30 times this year's earnings, respectively.
Under Warren Buffett, Berkshire avoided Nvidia for the same reason it shunned most tech stocks: it wasn't a business he fully understood. Buffett eventually invested in Apple as a consumer goods play -- while his portfolio managers likely initiated Berkshire's position in Alphabet -- but he likely avoided Nvidia because it was tough to gauge its long-term growth.
Buffett's successor, Greg Abel, also favors Apple and Alphabet over Nvidia as a long-term AI play because they're less exposed to the semiconductor sector's boom-and-bust cycles. As the previous CEO of Berkshire Hathaway Energy, Abel also likely sees more growth opportunities in energy infrastructure stocks in the AI market than in individual chipmakers.
So while Berkshire seems to be leaving some money on the table by shunning Nvidia, it's still exposed to the AI market's growth through some of its top stocks. Over the long term, we'll see whether that conservative strategy pays off -- or misses a major technological shift.

### Article 9 · 2026-09-07 · tradingview.com
Weekly Recap: NVIDIA (NVDA) $86B revenue and Hugging Face $12.9B deal

/ Weekly Recap: NVIDIA (NVDA) $86B revenue and Hugging Face $12.9B deal
Weekly Recap: NVIDIA (NVDA) $86B revenue and Hugging Face $12.9B deal
NVIDIA Corporation (NASDAQ:NVDA) posted record $86B revenue and massive growth guidance while striking deals—from a $12.9B Hugging Face buy to GPU supply and financing pacts with Nscale, Lambda, SB Energy and MediaTek—amid U.S. export curbs and claims of GPT-6 AGI readiness.
NVIDIA Revenue Guidance Jump : NVIDIA (NVDA) posted $86B revenue (+106% YoY) and guided ~ $108B next quarter. Management forecasts ~77% revenue growth next fiscal year (about 70% for calendar 2027).
NVIDIA To Buy Hugging Face : NVIDIA agreed to buy Hugging Face for about $12.9B. Deal faces regulatory approval and aims to close H1 2027. Hugging Face reports ~18M developers, 3M models, 500K datasets.
Export Controls On AI Chips : U.S. rules bar NVIDIA (NVDA) from exporting its top AI chips to China, while sales of its robotics and automotive chips remain allowed under current controls.
Vera Rubin GPUs For Barstow : NVIDIA to supply Vera Rubin GPUs to Nscale’s Barstow data center from H2 2027, initial contract $3.5B, potential >$6B, capacity up to 100,000 GPUs — supports Anthropic cloud deal.
Banks Mobilize AI Capital : NVIDIA (NVDA) said it’s working with major banks to mobilize over $500 billion in third-party capital to fund AI infrastructure investments.
MediaTek Bonds And NVLink : NVIDIA bought $3.5B of MediaTek convertible bonds (~3.6% of recent quarterly sales) as part of a partnership to integrate NVLink Fusion, XPUs, rack-scale AI, and automotive solutions.
Lambda Becomes Anthropic Partner : NVIDIA (NVDA) supplies GPUs for Lambda’s new Texas data center at Hut 8’s Beacon Point. Lambda signed a $35B deal with Anthropic. Hut 8 expands ~350 MW capacity; financing and utilization tracked.
SB Energy Nasdaq Listing : SB Energy seeks Nasdaq listing to fund an Ohio AI data-center. NVDA agreed to invest $3B and to assume the lease if OpenAI defaults; OpenAI leased the project.
GPT-6 Astra AGI Claim : NVIDIA CEO Jensen Huang said OpenAI’s GPT‑6 Astra marks AGI and was trained on over 100,000 NVIDIA Grace/NVLink systems; he added 400,000 more NVIDIA GPUs are expected online.
Rubin CPX Rack Upgrade : NVIDIA NVDA: Rubin CPX now uses a standalone MGX ETL rack. Configs: 64/128/192/256 CPX GPUs. Each 64-GPU module has eight trays of eight CPX GPUs linked by NVLink; Ethernet links trays/racks.

### Article 10 · 2026-09-07 · sdxcentral.com
Nvidia brings AI data center networking to the home with ‘personal AI router’

By Ben Wodecki
Nvidia is pushing its networking prowess further into the local AI space with a software tool allowing developers to interconnect MacOS, Windows, and Linux systems.
Personal AI Router , or PAIR, connects multiple devices on the same local network. Nvidia bills PAIR as the means to build “a personal home AI cluster,” with the software capable of routing independent inference requests to an available system.
It works across systems housing Nvidia RTX GPUs and its lunchbox-sized DGX Spark desktop AI supercomputer line. MacOS systems that are compatible with Nvidia’s offerings can employ PAIR to route local AI inference workloads to other machines on the network.
The virtual inference router routes workloads, while platforms like Ollama or LM Studio run the model on the machine the software selects. An Nvidia technical blog describes how it works: “PAIR discovers participating systems, tracks whether each system is ready for a request, schedules independent jobs, and returns each response to the application that originated it.”
Nvidia stressed that its newest software offering differs from a custom routing script with glossy green paint smeared over it in that it distributes workloads while keeping them secure . Where routing raw tokens across a home network creates security vulnerabilities, Nvidia contends PAIR employs mutual transport-layer security (mTLS) for encryption, while users employ a six-digit PIN between nodes, with the cluster refusing a machine that is not a member.
No fancy data center-esque cables are required for use, with the software tool itself open source.
It does require a minimum of eight gigabytes of random access memory (RAM) to run, but does not need to be connected to the internet during operation. Windows devices need to be running Windows 11, while Apple systems need MacOS Tahoe. For Linux systems, PAIR needs a distro like Ubuntu 14.04 to run. At the time of writing, it’s only available in English.
PAIR seems perfect then for local AI enthusiasts deploying agentic offerings like OpenClaw – the agent platform Nvidia CEO Jensen Huang enthusiastically billed as “ the iPhone of tokens .”
Nvidia has gone all in on agentic AI in the wake of OpenClaw, unveiling its own equivalent at GTC in NemoClaw , as well as a toolkit to encourage enterprises and developers to build AI agents.
PAIR is the next step of that bet, with the vendor’s technical blog explaining how it works for local agentic workloads: “Agents can send a request through the familiar local interface it expects. PAIR receives the request through its proxy, identifies its engine and model requirements, and selects one eligible node. That node executes the request from start to finish and sends the response back through PAIR. The agent continues to see one connection while PAIR handles placement behind it.”

### Article 11 · 2026-09-07 · calcalistech.com
Nvidia’s Israeli networking business is booming, and so is its economic footprint

Nvidia’s Israeli networking business is booming, and so is its economic footprint
The company’s networking revenue reached $32.3 billion in just the first half of fiscal 2027, already surpassing the previous full-year total. Much of the technology behind the business traces back to Mellanox and Nvidia’s Israeli development centers.
In March 2019, chip giant Nvidia dropped a bombshell on the Israeli market when it announced the acquisition of Israeli company Mellanox for approximately $6.9 billion in cash. The deal was completed on April 27, 2020. Mellanox, which developed high-speed communications technologies for data centers, became one of Nvidia’s key strategic assets in data center infrastructure following the acquisition.
The acquisition was particularly significant for Israel. Mellanox was one of the country’s leading technology companies, and the operations built around it became a central part of Nvidia’s global research and development activities in networking and communications for data centers. Alongside the capabilities it acquired through Mellanox, Nvidia has significantly expanded its R&D operations in Israel in recent years.
Through fiscal 2026, Nvidia reported data center revenue in two main categories: Compute and Networking. Networking includes communication chips, switches, connectivity systems and high-speed communications technologies for data centers. A significant portion of Nvidia’s technology and R&D activity in this area is connected to its development centers in Israel, much of which traces its origins to Mellanox.
Nvidia’s networking business has grown rapidly in recent years. In fiscal 2024, the company reported $8.57 billion in networking revenue. That rose to $13.0 billion in fiscal 2025 and then jumped 140% to $31.38 billion in fiscal 2026, which ended in January 2026.
Beginning in the first quarter of fiscal 2027, Nvidia changed the way it reports its data center business, placing greater emphasis on customer categories. As a result, its main financial reports no longer provide the same clear breakdown between compute accelerators and chips on one side and networking products, switches and connectivity products on the other.
However, Nvidia continued to provide the previous breakdown during the first two quarters of fiscal 2027. In the first quarter, data center Compute revenue was $60.4 billion, while Networking revenue was $14.8 billion. During the earnings call following its second-quarter results, the company said Networking revenue had increased 18% from the first quarter to $17.5 billion.
That puts Networking revenue at $32.3 billion for the first half of fiscal 2027, already exceeding the full-year figure for fiscal 2026. If the current pace continues, Networking revenue could more than double in fiscal 2027 compared with the previous year.
We estimate that a significant portion of Nvidia’s connectivity business, potentially around 70%, relies on technologies originating from Mellanox and the company’s development centers in Israel. This is an estimate based on the concentration of Nvidia’s networking R&D activity in Israel and the technological heritage of Mellanox. Nvidia does not publish a breakdown of its networking revenue or development activity by country.
Based on this estimate, the contribution of Nvidia’s Israeli operations to the company’s revenue in calendar 2025 was approximately $20 billion, while the contribution could exceed $40 billion this year. These figures should not be confused with Israeli exports or the value added generated in Israel. Nvidia’s products are manufactured, assembled and packaged outside Israel, meaning the full value of sales generated by technologies developed in Israel is not recorded as Israeli exports.
The Central Bureau of Statistics publishes a category for “goods sold abroad and not crossing the country's borders” as part of the adjustments between foreign trade statistics and balance-of-payments definitions. The category covers more than Nvidia, and therefore its full value cannot be attributed to the company.
Nevertheless, the figures show an unusual development in recent years. Exports in this category rose from $5.834 billion in 2021 to $7.312 billion in 2022 and $9.781 billion in 2023. They declined moderately to $9.276 billion in 2024 before jumping to $16.122 billion in 2025.
The sharp increase coincided with an extraordinary rise in Nvidia’s networking sales. It is therefore possible that part of the increase in this category is related to the expansion of Nvidia’s business, although the public data do not allow the portion attributable to Nvidia to be isolated.
Given the growing scale of Nvidia’s activities in Israel, the Central Bureau of Statistics could clarify how this type of activity is reflected in Israel’s balance-of-payments and export statistics. At present, however, there is no public data that allows Nvidia’s contribution to this category to be separately identified.
Nvidia’s full fiscal 2026 annual report also shows that the company paid $1.287 billion in corporate tax in Israel. It is reasonable to assume that most or all of this payment was made during calendar 2025, although the annual report does not provide a precise payment date.
If the estimated revenue generated by Nvidia’s Israeli operations more than doubles in 2026, the company’s tax contribution in Israel could also increase substantially. However, tax payments do not necessarily rise in direct proportion to revenue, so any estimate of this year’s payment should be treated cautiously.
Israel at the forefront of the AI revolution
Nvidia has arguably become the international company with the greatest impact on Israel’s technology economy. Its growing presence places the country at the center of the AI revolution while also increasing Israel’s economic exposure to Nvidia’s continued growth and global leadership.
Since acquiring Mellanox, Nvidia has significantly expanded its R&D operations in Israel and built the country into one of its most important development centers. The company employs thousands of people in Israel, primarily engineers and other R&D professionals working on chips, software, artificial intelligence, communications and data center technologies.
The activity generates significant economic value in Israel by supporting highly skilled employment, expanding the country’s technology base and building expertise in some of the most important areas of the global AI infrastructure market. It also reinforces Israel’s position as a major center for AI and data center technologies.
But the scale of Nvidia’s presence creates a corresponding dependence. As the company becomes increasingly important to Israel’s technology sector and exports, the Israeli economy has more at stake in the continuation of the AI boom, and in Nvidia maintaining its position at the center of it.

### Article 12 · 2026-09-07 · scmp.com
Opinion | Virtuous circle of AI titans’ investments could well turn vicious

AI titans’ ‘circular deals’ are starting to look like ‘daisy chains’
It’s time to ask how much of the industry’s extraordinary growth is being financed by the same companies benefiting from it
James David Spellman, a graduate of Oxford University, is principal of Strategic Communications LLC, a consulting firm based in Washington, DC.
The “circular deals” among AI titans increasingly resemble the “daisy chains” of the 1980s savings-and-loan crisis.
Forty years ago, interconnected transactions obscured the dangers, multiplied systemic risks and helped inflate asset values before roughly a third of US thrift banks failed. Today’s financial engineering – an incestuous ecosystem of interlocking multi-year commitments to provide financing, buy semiconductors, secure gigawatts of power and lease data centres – could meet a similar fate, especially if revenue fails to outpace costs or a black swan event eviscerates artificial intelligence (AI) trajectories.
OpenAI has struck deals with Nvidia , CoreWeave and others ahead of an initial public offering planned for next year while competitors Anthropic and xAI have pursued similar agreements. Anthropic’s US$35 billion cloud-computing deal with provider Lambda is the latest example. Last month, the AI developer signed a US$45 billion arrangement with another Nvidia-backed neocloud, Nscale, to rent data-centre capacity.

### Article 13 · 2026-09-07 · fool.com
Not Nvidia, Not Micron. This Magnificent Warren Buffett Stock Could Be the Quiet Winner of the AI Arms Race -- Here's the Case.

When ChatGPT burst onto the scene in late 2022, investors did not waste time picking which tech companies they thought would be winners from the new artificial intelligence (AI) trend. At first, the market went shopping for pick-and-shovel companies . Nvidia ( NVDA +2.55% ) sells the graphics processing units (GPUs) that provide the computing power to train and run generative models. Micron Technology ( MU +4.20% ) sells the high bandwidth memory (HBM) and DRAM that store and rapidly supply the vast quantities of data that those processors work on.
Since the AI revolution started roughly three-and-a-half years ago, the scoreboard has been almost cartoonish. Since ChatGPT's public release, Nvidia stock has risen 1,290%, while Micron has soared 1,630%. These are not typical numbers , even for a bull market.
The reason behind their parabolic ascents is simple. Hyperscalers are spending more than $700 billion annually on AI infrastructure, and large slices of those checks are being allocated to GPUs, CPUs, HBM, and DRAM. Nvidia dominates the accelerator conversation, while Micron is one of only three companies that make the memory stacks that sit next to Nvidia's chips. As long as Amazon , Microsoft , Meta Platforms , and Alphabet ( GOOGL -0.56% ) ( GOOG -0.70% ) keep building data centers, Nvidia and Micron will continue cashing the invoices.
That story is not wrong, but it is incomplete. The quiet winner of the infrastructure cycle may be one of the companies writing a lot of these checks. Alphabet already dominates the consumer and enterprise demand side, the software side, and, increasingly, it's designing its own silicon. Wall Street has spent nearly four years treating all of that as a footnote. Warren Buffett and his new successor, Greg Abel, are not.
Berkshire Hathaway is plowing into Alphabet stock
Berkshire Hathaway's first disclosed purchase of Alphabet stock showed up in the third quarter of 2025, a position of 17.8 million shares. The conglomerate sat on that stake through the end of the year before it accelerated its buying activity. During the first quarter of 2026, it nearly tripled its position in Alphabet. During the second quarter, Berkshire once again added shares on the open market and, more tellingly, wrote a $10 billion check for new shares as part of a larger private placement.
Buffett has been quite blunt about the origin story of Berkshire's position in Alphabet. "I initiated it," he told CNBC's Becky Quick during a recent interview.
Greg Abel, who succeeded Buffett as CEO at the start of 2026, has been aggressively adding to the position. Berkshire now holds around 106 million Alphabet shares worth nearly $38 billion. The position comprises about 13% of Berkshire's total stock portfolio, behind only Apple and American Express .
What makes Alphabet an attractive AI investment?
Nvidia sells the engine that powers AI models, and Micron sells the tanks for the fuel that keeps the engine running. Alphabet, by contrast, is building the car, the roads, and a growing share of alternative engines. Google Search is a money-printing machine, while YouTube draws the attention of billions of viewers. Meanwhile, Android sells smartphones and other consumer hardware around the globe. On top of these assets sit Gemini, Google Cloud , Tensor Processing Units (TPUs), and the Waymo autonomous vehicle fleet.
The recent performances of Google Cloud are something that should make chip bulls pay attention. In the first quarter, its revenue rose 63% year over year to $20 billion, with operating margins coming in at 33%. During the second quarter, sales from Google Cloud jumped 82% year over year to 24.8 billion, with an operating margin of 36%. Moreover, Google Cloud's backlog was a jaw-dropping $514 billion at the end of the second quarter. Cloud infrastructure is not a little side hustle for Alphabet -- it's turning into a second core profit engine alongside the core advertising segment.
On the silicon side of the cloud division are TPUs -- a type of custom silicon that can handle AI workloads at a lower cost than GPUs. Google designed them for its own specific AI workloads, and it used to keep the chips in-house, but now, it has started selling some to enterprise customers that want the custom silicon that trains Gemini models in their own data centers. This is another example of how Alphabet is turning what was once a cost center into a monetized product.
Waymo services now run on the order of 500,000 paid robotaxi rides a week across more than a dozen cities. A February funding round valued that business at $126 billion. As agentic AI applications enter wider production, Waymo could swiftly emerge as a business that contributes meaningful unit economics to Alphabet's broader ecosystem, much in the same way Google Cloud has scaled up over the last couple of years.
The thread stitching Alphabet's fabric together is Gemini. Search, YouTube, Android, Workspace, Cloud, and even the robotaxis increasingly run on a unified family of models. That structure is the difference between selling critical components and compounding an ecosystem.
Alphabet stock looks like a bargain value
Alphabet's vertically integrated stack is how the company manages to remain consistently profitable. Cloud, which was actually losing money as recently as 2022, is now one of the juiciest parts of the company. The reason? AI has become the accelerant. Alphabet's companywide operating margin is around 34% and moving upward. That's impressive for a business that's spending like a utility building a new power grid.
The capital cycle is the objection everyone already knows. Alphabet has said it plans for between $195 billion and $205 billion in capital expenditures this year. While the company's free cash flow has gone temporarily negative and it has paused its stock buybacks, the bigger picture isn't as ugly as it might appear in a spreadsheet. In fact, this is simply a repeat of the same pattern Google Cloud already survived: Absorb operational pain, then watch the profit margin show up once the capacity you paid to build is fully subscribed.
On valuation, Alphabet stock is not priced like a company that is at the forefront of AI. The company trades at a forward price-to-earnings (P/E) ratio of 16. That is nearly identical to the long-run average forward P/E of the S&P 500 . For a business with Search's moat, YouTube's scale, Cloud's backlog, its own accelerator roadmap, and an autonomous robotics play that has yet to contribute much more than a rounding error to its financials, this is not an expensive stock.
Don't get me wrong: Nvidia and Micron will keep winning every time a hyperscaler or neocloud orders another server. But smart investors realize they are not the only companies getting paid. Alphabet is a rare business selling the infrastructure, running frontier models, owning multiple distribution channels, and still generating the kind of profits Buffett spent a lifetime buying. Against this backdrop, I see Alphabet as a no-brainer opportunity to buy hand over fist and hold onto throughout the AI infrastructure era.
Not Nvidia, Not Micron. This Magnificent Warren Buffett Stock Could Be the Quiet Winner of the AI Arms Race -- Here's the Case.
Nvidia and Micron have become two darlings of the artificial intelligence revolution, but there are more attractive opportunities beyond semiconductors.
By Adam Spatacco – Sep 7, 2026 at 8:33AM EST
Nvidia and Micron dominate the AI semiconductor landscape, specializing in GPUs and high bandwidth memory, respectively.
Warren Buffett and his successor, Greg Abel, have been adding large amounts of Alphabet stock to Berkshire Hathaway's portfolio over the last few quarters.

### Article 14 · 2026-09-07 · finance.yahoo.com
Broadcom’s AI Forecast Suggests Hyperscalers Want More Than Just Nvidia GPUs

Big Tech's appetite for AI infrastructure isn't being sated anytime soon, and Broadcom Inc. (NASDAQ: AVGO ) is proof of that. On Wednesday, the custom AI chipmaker said it now expects AI chip revenue of about $115 billion in the fiscal year ending October 2027, up from a prior forecast of over $100 billion. Broadcom also expects this revenue to double to roughly $230 billion in fiscal 2028.
Broadcom's revenue outlook is evidence that hyperscalers no longer want costly processors only. Rather, they are also interested in suppliers such as Broadcom who provide both the custom chips and the networking components. Broadcom's forecasts are therefore a reflection of continued spending by Big Tech on alternatives to NVIDIA Corporation (NASDAQ: NVDA )'s GPUs, as well as components that complement them.
In response to this forecast, KeyBanc analyst John Vinh reiterated an Overweight rating and $575.00 price target on Broadcom.
Hyperscalers Want Suppliers Like Broadcom
Hyperscalers are increasingly looking for suppliers that offer different types of processors, designed for different types of workloads. This is because they want more control over the economics of their AI infrastructure. The preference doesn't just reduce their reliance on Nvidia, but also offers them the chance to reduce operational costs and build custom silicon.
Broadcom President and CEO Hock Tan has confirmed that the demand for both its custom AI accelerators and AI networking infrastructure continues to outpace supply. Particularly in its Q3 fiscal 2026 earnings report, Tan noted exploding demand driven by major frontier customers such as OpenAI, Meta, Google, and Anthropic.
Keybanc's note highlights how Anthropic/ OpenAI would be Broadcom's largest customers in fiscal 2028. This could offer Broadcom Inc. (NASDAQ:AVGO) more visibility beyond its Google relationship. The expansion reflects how custom chips are increasingly becoming an important part of AI infrastructure.
However, competition within the segment is also becoming intense. Alphabet's Google recently expanded its deal with Marvell, with analysts even pointing to AVGO losing share in Google's TPU programs. While the deal doesn't aim to displace Broadcom Inc. (NASDAQ:AVGO), it does imply that the position isn't guaranteed either.
Broadcom comes from a place of operational strength, with fiscal third-quarter revenue rising 86% year-over-year to about $29.6 billion and topping Wall Street expectations. However, its fourth quarter guidance of roughly $34.8 billion landed just under the $35 billion consensus estimate- a mixed guidance flagged in KeyBanc's note.
The bull case for Nvidia in this scenario is that hyperscalers aren't being seen abandoning it. Rather, they are adding custom silicon alongside GPUs. Reuters noted Nvidia holding 80% of the GPU market. AWS is deploying Trainium alongside millions of Nvidia GPUs, Microsoft is scaling both Nvidia Rubin and Maia, while Google is also offering TPUs and using Nvidia GPUs.
Moreover, Nvidia's large developer ecosystem, CUDA software, and hardware performance are difficult to replicate. At the same time, it should be noted that hyperscalers also have the scale to justify spending on chips around specific workloads. This means they can also eventually route a large portion of workloads away from expensive general purpose GPUs.
According to Insider Monkey's database, 170 hedge funds held positions in the stock at the end of the Q2, modestly down from 173 in the previous quarter. As for Nvidia, 285 hedge funds held positions in the stock at the end of the second quarter, up from 275 in the previous quarter.
Filings also reveal how Fisher Asset Management held about 15.1 million shares in Broadcom and 90.9 million shares in Nvidia at the end of the second quarter. AQR Capital Management increased its position in Broadcom by 9%, while simultaneously increasing its position in Nvidia by 18%.
Overall, Broadcom's forecast doesn't imply that the demand for Nvidia's GPUS is slowing down. Rather, it suggests that hyperscalers are increasingly preferring both Nvidia and suppliers such as Broadcom. If AI infrastructure continues to expand at unprecedented rates, both companies are set to gain from it.

### Article 15 · 2026-09-07 · msspalert.com
Nvidia transfers Open Secure AI Alliance to Linux Foundation

By MSSP Alert Team
Chip giant Nvidia has transferred leadership of its Open Secure AI Alliance to the Linux Foundation, aiming to foster a neutral environment for open-source AI security collaboration, following insights from SDx Central.
The Open Secure AI Alliance, founded just last month, brings together companies like Broadcom, Cisco, and Hewlett Packard Enterprise to develop open-source tools, standards, and defensive strategies for AI systems. This initiative includes the Shared AI Findings Exchange (SAFE), designed to help organizations learn from AI-related security incidents and implement evidence-based protections. The alliance's formation was partly a response to a security breach at Hugging Face, an AI lab recently acquired by Nvidia. In this incident, OpenAI agents reportedly created an internal forum to share files and coordinate actions, leading to the compromise of Hugging Face's open-source repository.
This event highlighted concerns about the security implications of advanced AI agents and the need for robust, open-source defensive measures. The alliance, now under the Linux Foundation's stewardship, aims to address these challenges with over 120 member organizations, though key players like OpenAI and Anthropic are not currently involved.

### Article 16 · 2026-09-07 · finance.yahoo.com
AMD and Intel Soared as Nvidia Lagged: Has the AI Trade Changed?

AMD gained 4.7% and Intel rose 4.5% on September 4, while Nvidia added only 0.8%. The one-session gap is consistent with investors widening the AI trade beyond Nvidia, but it cannot identify buyer motive or prove a lasting rotation. Advanced Micro Devices, Inc. (NASDAQ: AMD ) and Intel Corporation (NASDAQ: INTC ) each offer a route to AI spending that does not require Nvidia to lose outright.
AMD's second-quarter revenue reached a record $11.5 billion, up 50% year over year, and Data Center represented 58% of the company. Its portfolio includes MI450 accelerators, sixth-generation EPYC processors, Helios rack-scale systems, and Pensando networking. Customers seeking a credible second source and more negotiating leverage support the bull case. The countercase is software maturity, execution across a broad roadmap, and the capital required to challenge Nvidia's ecosystem.
Insider Monkey's database counted 164 hedge funds holding Advanced Micro Devices, Inc. (NASDAQ:AMD) in Q2 2026, up from 134 in Q1 2026. Marshall Wace reported 3,898,210 shares, about 3% more than in Q1. The quarter-end filings predate the September 4 rally and cannot show whether funds reacted to it.
Intel's second-quarter Data Center and AI revenue was $6.3 billion, up 59% year over year. A resilient CPU franchise, custom silicon, advanced packaging, and a domestic foundry network form the bull case. The cost and uncertain returns of rebuilding manufacturing leadership form the bear case. Intel generated $1.8 billion of GAAP operating income, while its $2.16 GAAP loss per share was driven largely by a $12.5 billion noncash mark-to-market loss on escrowed shares. Negative $8.4 billion adjusted free cash flow still makes capital efficiency a real concern.
The Q2 2026 database counted 138 hedge funds holding Intel Corporation (NASDAQ:INTC), up from 112 in Q1 2026. AQR Capital Management reported 10,742,567 shares after cutting its position by about 6% from Q1. That disclosure also predates the September rally, so it is historical positioning rather than a reaction.
At the August 14 short-interest settlement, 135,685,200 Intel shares were sold short with 1.26 days to cover. Published float estimates put that near 2.6% to 3.0% of float, which is not a structurally crowded short. Friday's widening rally matters only if deployments validate a more plural supply chain. AMD must prove rack-scale adoption and software competitiveness; Intel must turn capacity and design wins into acceptable returns. Nvidia can keep growing while both take parts of an expanding market, but the decisive evidence will be shipments, margins, and free cash flow.
While we acknowledge the potential of AMD and INTC as investments, we believe certain other AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 17 · 2026-09-07 · washingtonexaminer.com
Nvidia CEO Jensen Huang says ‘AGI has arrived’ with new OpenAI GPT-6 model

By Zach Halaschak
Nvidia CEO Jensen Huang declared this weekend that “AGI has arrived” with the release of OpenAI’s newest model, GPT-6 Astra.
Huang, who has helmed the chipmaker for over three decades, made the comment on Sunday in a social media post praising the model’s release. AGI stands for artificial general intelligence , a vague term to describe the point at which AI is capable of performing intellectual tasks on par with or beyond the capabilities of a human.
in the midterms.
Get unlimited access to Washington Examiner's midterm coverage, analysis, and political insights.
BERNIE SANDERS INTRODUCES BILL TO BAN ARTIFICIAL SUPERINTELLIGENCE
Reaching AGI has long been a goal of many AI companies.
The remarks come as several AI companies compete for better and better models and as AI usage proliferates. There have been fights over what AI will mean for the country’s labor force, and concerns about the data centers needed to support the growing technology.
OpenAI touts Astra as the world’s “most intelligent and aligned model.”
“GPT‑6 Astra brings together years of research and big bets across pre-training, reinforcement learning, and alignment,” the company said in a news release. “Astra is state-of-the-art on computer use, browsing, software engineering, cybersecurity, science, and professional work.”
Astra is rolling out this week to a limited number of organizations before ultimately becoming available to all ChatGPT Plus, Pro, Business, and Enterprise users.
“Astra is our most aligned model, with substantial improvements in understanding user intent and model behavior—you can delegate tasks with greater confidence in Astra’s judgment,” the company said.
AI has become a major conduit for investment over the past few years and a central driver of the stock market’s growth.
In June, Jamie Cox, managing partner for Harris Financial Group, predicted to the Washington Examiner that the AI boom is about 80% responsible for recent gains in the market.
Nvidia and OpenAI have worked together.
OPENAI AND NVIDIA JOIN FORCES FOR NEW ENORMOUS OHIO DATA CENTER
For instance, last month, OpenAI entered into a 20-year lease agreement with SB Energy and SoftBank Group that included a $105 billion financial guarantee from Nvidia to support a large-scale data center in Ohio.
That massive plant is planned to provide at least 8 gigawatts of electrical power. For comparison, the largest operating data center by power capacity is 1.563 gigawatts, located in Tennessee.

### Article 18 · 2026-09-07 · creativebloq.com
Can NVIDIA and Adobe work together to get creatives to actually like AI?

By Design
By Erlingur Einarsson
RTX Spark introduces local AI agents in Photoshop, and creatives should be (cautiously) optimistic
For years, AI in creative software has felt like a tug‑of‑war between two extremes: the “AI will replace artists” panic and the “AI is just a fancy filter” disappointment. But the new locally run AI agents inside Photoshop, made possible with RTX Spark? They land somewhere far more interesting... and, dare I say, actually useful.
Not because they’re magical, but because they’re practical .
An AI feature that doesn't break the creative flow
Most AI tools promise speed, but they often demand a whole new workflow, a new app, or a new mental model. Creatives don’t want that. Creatives want to stay in Photoshop , stay in their groove, and stop wrestling with the technical busywork that interrupts the fun part.
The demo I saw at NVIDIA 's RTX Spark showcase at IFA in Berlin showed a sketch of a robot turned photoreal using a beach photo as a main reference, with smaller reference photos and images to inform the model on all the individual elements of the robot, including the colour, texture of the metal, shape and type of 'eyes' and more. It wasn’t impressive because it was flashy. It was impressive because it respected the artist’s process. In fact, the demo was presented by the artist herself. The agent didn’t overwrite the sketch, reinterpret the brief, or decide the robot should be a cat now. It simply did the heavy lifting the artist didn’t want to do.
That’s the first time in a while I’ve seen AI behave like a collaborator at an advanced level, instead of a chaos gremlin.
Local AI is a feature creatives have been begging for
Let’s be honest: the creative community has trust issues with cloud AI. And for good reason. Too many models have been trained on artists’ work without permission, and too many “helpful” features quietly upload your assets to servers you’ve never heard of.
This demo didn’t do that. Everything ran locally on a (rather beefy, admittedly) RTX workstation with 128GB of unified memory. No cloud. No mystery training. No “your PSD is now part of a dataset in Utah”.
The presenter said it plainly during the demo: “My creative data stays on my machine.”
That alone makes this one of the most creator‑friendly AI features we’ve seen in years.
Iteration at (nearly) the speed of imagination
The real magic wasn’t the photoreal robot. Rather it was how quickly the artist could riff on it.
“Change the theme to nightlife.” Boom: neon nightlife in ten seconds.
“New camera angle.” Hey presto: a generated 3D model you can spin around.
“Make a video between these angles.” In under a minute: a workflow that used to require three different apps.
Sure, one version had cars floating in the ocean. Generative AI still loves a bit of surrealism. But when the entire workflow takes 90 seconds, you can afford to laugh, delete, and try again.
This is the kind of speed that encourages experimentation instead of punishing it.
The real reason this matters, is that these AI agents inside Photoshop aren’t about replacing artists. They’re introduced in an aim to reduce friction. They’re about letting creatives stay in the zone longer, about giving you a superpowered assistant who doesn’t get tired, doesn’t misplace files, and (hopefully) doesn’t ask what the brief was again.
If Adobe plays this right - and importantly, keeps the local‑first approach - AI agents could become the most meaningful workflow upgrade Photoshop has had in a long time.
Not because they’re clever, but because they finally understand what creatives actually need.

### Article 19 · 2026-09-07 · businessinsider.com
China’s Nvidia challenger crashed 20% in a reality check for an AI darling

By Huileng Tan
Moore Threads, one of China's highest-profile homegrown challengers to Nvidia, crashed 20% on Monday after millions of previously locked-up shares became eligible for trading.
The GPU maker hit the Shanghai Star Market's daily down-limit at 415.48 Chinese yuan within minutes of the open, its lowest level since its December listing.
The catalyst for the slump was the expiration of a nine-month lockup on 25.8 million shares allocated to investors in Moore Threads' IPO.
The shares represent just 5.5% of the company, but their release nearly doubled the number of shares available for trading.
Those investors bought at 114.28 yuan a share, meaning they were still up more than 260% even after Monday's plunge.
The selloff is a sharp reversal for one of the biggest winners from China's AI frenzy.
Founded by former Nvidia China executive Zhang Jianzhong, Moore Threads soared 425% on its December debut and later climbed even higher.
Its rally was part of a broader frenzy around China's AI industry. DeepSeek's breakout in early 2025 supercharged interest in homegrown AI, while US restrictions on advanced Nvidia chips have added urgency to Beijing's drive for technological self-sufficiency.
Investor appetite has remained intense. Memory-chip maker CXMT raised $8.6 billion in Shanghai in July and closed 466% higher on its debut, becoming mainland China's most valuable publicly listed company on day one of trade.
China's AI-model makers have drawn similarly intense interest. Hong Kong-listed Z.ai recently generated buzz with Ox Alpha, a mystery model that impressed developers. Its shares are trading at roughly nine times their January IPO price.
Moore Threads is pursuing a Hong Kong listing after shareholders approved the plan last month.
Last week, JPMorgan said it expects China's domestic AI compute demand to grow at about an 80% compound annual rate. It estimates local chips could meet 80% of the country's AI infrastructure demand by 2028, up from 40% in 2025.
But Moore Threads is up against stiff competition for that growing market.
The company faces "insurmountable competitive hurdles over the medium term," Maybank Securities analysts wrote last week, citing both software and hardware challenges.
Huileng Tan is a senior reporter based in Singapore, covering markets, the global economy, commodities, and investing. Her reporting focuses on how shifts in money, demographics, technology, and policy are reshaping businesses, wealth, and everyday life around the world. Since joining Business Insider in 2021, she has covered everything from commodity booms and investor trends to China's economy, the AI trade, and the forces driving global markets. Before joining Business Insider, she reported for CNBC, Dow Jones, ICIS, and The Wall Street Journal. Reach her at htan@businessinsider.com .

### Article 20 · 2026-09-07 · finance.yahoo.com
Jim Cramer Discusses NVIDIA (NVDA) Acquiring Hugging Face

On the September 3 episode of Mad Money, Jim Cramer turned his attention to NVIDIA Corporation (NASDAQ: NVDA ) and its expansion into open-source software infrastructure. He remarked:
Next, I know NVIDIA's up 22% for the year and that would be a lot for every other company, but not for NVIDIA. This is NVIDIA, for heaven's sake… NVIDIA bought Hugging Face today. I know it sounds like a foreign version of Kleenex, but it's a kind of open-source AI. I think it's a brilliant move, and it'll put to rest all the nonsense that NVIDIA's technology is only good at training, not inference. It's foundational... But what matters is that NVIDIA sells at less than 15 times next year, I'm going to say that again: less than 15 times next year's earning estimates… Hey, look, I nailed Dell for 100 points. Give me some credit here. I think this thing goes up 50% if I manage the buyback or someone like me, like an AI version of me.
The Hugging Face Acquisition and Inference Expansion
NVIDIA Corporation's (NASDAQ:NVDA) agreement to acquire open-source platform Hugging Face for approximately $12.9 billion represents a significant strategic shift deeper into the software deployment ecosystem. By acquiring one of the leading platforms for open AI models and developer communities, NVIDIA could gain an important position in model distribution and deployment. The transaction directly addresses long-standing skeptics by strengthening NVIDIA's position in inference workloads, showing that hardware utility extends far beyond initial model training. Furthermore, Cramer argued that NVDA trades at less than 15 times forward earnings estimates, presenting an appealing valuation profile relative to its explosive earnings growth.
Antitrust Scrutiny and Ecosystem Neutrality Risks
Despite the strategic benefits, the acquisition could introduce regulatory and operational risks. Because Hugging Face has historically operated as neutral ground for the entire developer community, bringing the platform under NVIDIA Corporation's (NASDAQ:NVDA) corporate umbrella risks alienating rival hardware vendors and independent model builders. It remains to be seen whether the deal creates unfair distribution advantages or forces developers down proprietary software paths, introducing potential closing delays or compliance hurdles.
Institutional backing remains broad and resilient among major hedge funds. According to Insider Monkey's tracking data, 285 hedge funds held positions in NVIDIA Corporation (NASDAQ:NVDA) during the second quarter, marking an increase from 275 funds in the prior period. On top of that, short interest remains exceptionally low, with the short percentage of the float resting at just 1.23%, showing minimal bearish conviction against the company.
NVIDIA Corporation (NASDAQ:NVDA) combines dominant hardware infrastructure with a strengthening software moat through the proposed Hugging Face acquisition, all while trading at an attractive forward earnings multiple. Although regulatory headwinds and ecosystem neutrality concerns warrant careful observation, Cramer's commentary highlights how strategic software expansion strengthens the company's long-term market leadership.

### Article 21 · 2026-09-07 · gurufocus.com
Nvidia Gets a $1.47 Billion Supplier Cushion Without Spending a Dollar

Nvidia ( NASDAQ:NVDA ), the dominant supplier of artificial-intelligence accelerators, secured another boost across its manufacturing network Monday as supplier Wistron raised $1.47 billion. Wistron plans to spend the proceeds on foreign-currency raw materials while scaling AI-server production.
Wistron issued 25 million depositary receipts representing 250 million common shares at a 5.5% discount. The deal dilutes existing shareholders by approximately 7.29%, but it gives the manufacturer fresh financial firepower after opening a $700 million Texas facility that produces Nvidia's latest AI systems.
The raise is roughly 2.1 times the disclosed cost of that factory, although Wistron has not earmarked every dollar for Texas. Nvidia gains from a better-funded supplier capable of purchasing components and pushing out more servers without touching Nvidia's balance sheet. The GuruFocus chart reinforces that strength: Nvidia carries a 95/100 GF Score, powered by exceptional profitability, growth and financial strength, while valuation remains the clearest weak spot. Supplier concentration is still the risk investors cannot ignore.

### Article 22 · 2026-09-07 · techrepublic.com
Nvidia Launches Free PAIR Tool to Share AI Workloads Across PCs and Macs

Nvidia PAIR is a free open-source tool that distributes local AI workloads across PCs and Macs, letting idle hardware help run multi-agent tasks.
That gaming PC sitting idle while your laptop struggles through an AI workload could soon become part of the solution.
Nvidia has unveiled Personal AI Router, or PAIR, a free open-source tool that distributes local AI jobs across available computers on the same network. Announced at IFA 2026, PAIR works across Windows, macOS, and Linux systems without requiring users to build a dedicated AI server or cluster.
PAIR does not combine multiple GPUs into one larger accelerator. Instead, it finds available machines and sends separate AI requests to whichever system has computing capacity to spare — an approach Nvidia is targeting particularly at multi-agent workloads.
PAIR discovers devices via multicast DNS (mDNS), securing inter-device communication through a six-digit verification PIN and mutual transport layer security (mTLS) encryption. PAIR is designed to keep traffic between participating devices on the local network.
The router targets “agentic” workflows, where a primary autonomous agent delegates assignments to multiple subagents. Running those sub-tasks sequentially on a single rig often bogs down processing queues.
According to Nvidia , a five-subagent task analyzing a synthetic household inbox using the Qwen 3.6 35B A3B model took 18 minutes on an RTX Spark laptop alone, but finished in 8 minutes and 48 seconds when PAIR split the jobs across a three-node cluster including an RTX 5090 and a DGX Spark.
The software officially validates hardware spanning Nvidia GeForce RTX 20-series GPUs and newer, workstation-grade RTX Pro chips, DGX Spark units, and Apple M4 silicon or newer.
The result reflects Nvidia’s specific synthetic test setup, so actual performance will depend on the workload, hardware, model, and network.
There is an important distinction: PAIR does not combine GPUs into one giant accelerator. It cannot pool VRAM or split a single inference request across multiple machines. Each request runs entirely on one eligible node.
That means PAIR is most useful when a workload has several independent jobs that can run simultaneously. A highly sequential task dominated by one long inference request may see little benefit.
The bigger idea behind PAIR is less about building a miniature data center and more about making existing hardware behave like a flexible pool of resources.
A gaming PC, work laptop and Mac may each be poor candidates for an always-on AI cluster because their owners need them for other things. But software that can borrow their unused capacity when available changes the equation.
PAIR could therefore make local AI more practical for households that already own several capable machines — without buying another server or sending their data to the cloud.
For users with only one powerful machine — or workloads dominated by a single inference request — the benefit will be much smaller. PAIR’s value comes from having both spare hardware and AI jobs that can actually run in parallel.
Let us teach you How to Talk to AI for free! Try our six-minute course at The Neuron Academy and learn a few simple ways to write better prompts and get more useful results from AI, or browse our other AI course for free for seven days. Check out all the lessons here →

### Article 23 · 2026-09-07 · businessinsider.com
Nvidia's Jensen Huang Says 'AGI Has Arrived' and Congratulates OpenAI

By Truman Dickerson
Nvidia CEO Jensen Huang tipped his hat to OpenAI on Sunday.
The chipmaking mogul took to X to congratulate OpenAI's team on the release of the company's newest and most powerful model , Astra, and made the notable statement that "AGI has arrived," a nebulous term that typically describes AI models that match or surpass human intelligence.
He also pointed out that Astra was trained on Nvidia's chips.
"From ChatGPT to o1 to Astra in 4 years," Huang said in a post on X. "AGI has arrived. Congratulations @OpenAI team."
OpenAI unveiled Astra on Thursday. The ChatGPT maker called it the world's "most intelligent and aligned model," and said it is capable of performing "the most demanding professional work with unmatched speed, accuracy, and judgment."
Greg Brockman, the company's president, said on a call with reporters on Thursday: "Welcome to the AGI era."
AGI stands for artificial general intelligence , a fuzzy concept that nonetheless has become a core goal for leading frontier AI labs.
OpenAI defines it as "highly autonomous systems that outperform humans at most economically valuable work." The company pitched Astra as a major research breakthrough and a shift in what's possible to delegate to AI. It's rolling out to customers this week.
On the Thursday call, Brockman said that in the future, he thinks people will look back and think AGI was created "about this time, and I think it might be about this model."
"For me personally, I do think we're there," he said.
'Declaring victory without a definition'
It is not the first time Huang has said AGI has arrived. In March, podcaster Lex Fridman asked him to consider a definition of AGI as an AI system capable of starting, growing, and running a tech company worth more than $1 billion.
"I think it's now. I think we've achieved AGI," Huang replied.
Other prominent tech figures have also said notable AI milestones have been reached. Elon Musk said in January that humanity had "entered the technological singularity ," which he described as a point of no return in which AI accelerates beyond human intelligence.
In May, Marc Andreessen, the cofounder of investment firm A16z, said the AGI threshold had been crossed roughly three months earlier, arguing that several frontier models were already "as smart as a person."
Not everyone agrees.
Gary Marcus, a prominent AI researcher and critic, said Huang had jumped the gun with his comments about OpenAI achieving AGI.
"Huang gave no evidence and no definitions, which feels to me like an effort at a takeover of a scientific question by corporate fiat," Marcus wrote on his Substack Sunday evening. "Declaring victory without a definition simply muddies the waters."
Marcus attached his own 10-point definition of AGI, noting that Astra only meets one or two of those benchmarks.
"By conventional definitions, Astra still falls short," he said.
The researchers behind ARC Prize, whose benchmark OpenAI highlighted in announcing Astra, also stopped short of calling the model AGI.
They described Astra's results as a major advance but said success on the benchmark was not proof of AGI, noting that its tests take place in tightly bounded environments that do not reflect the complexity and open-endedness of the real world.
Sam Altman, for his part, told the "Sources" podcast in a recent appearance that AGI is, at best, "a very poorly defined term. I was going to say it's like an irrelevant marketing term."
What AGI would mean for everyday life is similarly unclear. It could lead to breakthroughs in medicine and science, or provide everyone with highly intelligent personal assistants. It could also put more jobs under pressure.
Frontier AI companies like OpenAI, Meta, Anthropic, and Google have grown increasingly reliant on advanced chips manufactured by Nvidia. In a funding announcement in March, OpenAI called Nvidia "the foundation of our infrastructure."
"Our training fleet and the majority of our inference stack continue to run on Nvidia GPUs," the company said.
That demand has translated into enormous sales for Nvidia. The company reported $96.2 billion in quarterly revenue in August, more than double the amount reported in the same period a year earlier. Its data center business, which includes its AI chips , generated $89 billion in revenue.
And in his X post on Sunday, Huang suggested there's plenty more computing power on the way.
"400K GPUs coming online next," he said, referring to graphics processing units, the advanced chips used to train and run AI models.
Georgia is a Business News Fellow at Business Insider's London office. Before joining Business Insider, she worked at Japan's largest newspaper, The Yomiuri Shimbun, and interned at the Financial Times. She is an NCTJ-qualified journalist with a degree in Philosophy from the University of Birmingham.

### Article 24 · 2026-09-07 · fool.com
Jensen Huang Just Said a 1-Gigawatt Facility Is Worth $50 Billion to $60 Billion. Here's What That Means for Neocloud Stocks Like Nebius.

Jensen Huang Just Said a 1-Gigawatt Facility Is Worth $50 Billion to $60 Billion. Here's What That Means for Neocloud Stocks Like Nebius.
The AI infrastructure buildout has been expensive, and Nvidia (NASDAQ: NVDA) CEO Jensen Huang recently put a price on it. He estimated at the G20 Summit that it costs between $50 billion and $60 billion to build a 1-gigawatt facility.
These facilities will become vital for the AI build-out. They make it easier to scale agentic AI, chatbots, and upcoming physical AI, which includes humanoid robots and autonomous vehicles.
This is obviously good news for neocloud providers like Nebius (NASDAQ: NBIS), which build these data centers. However, there are a few key catalysts that investors may not be anticipating.
Annual recurring revenue isn't the only way to value AI data center providers
When Nebius reported Q2 earnings, it told investors that its revenue jumped by 454% year-over-year to $582 million. Annual recurring revenue reached $3 billion, and it's aiming for $7 billion to $9 billion in annual recurring revenue by the end of the year.
While annual recurring revenue is a good gauge for determining a stock's fair price, investors should also consider the multigigawatt pipeline. Since Huang set $50 billion to $60 billion as the range for a 1-gigawatt facility, Nebius' projected five gigawatts of contracted power by the end of 2026 can be worth up to $300 billion when all of the facilities are finished.
That doesn't mean Nebius should immediately have a $300 billion market cap. However, the data centers offer significant value that goes well beyond the annual recurring revenue that they can generate.
Neoclouds got additional leverage with raising capital
Neoclouds have a compelling opportunity, but high capital costs have been the major weakness. Huang pegging the cost of a 1-gigawatt facility at $50 billion to $60 billion can actually solve that problem, especially if the value of these facilities continues to climb.
Neoclouds like Nebius have been taking customer prepayments to help fund these builds. If people place a higher valuation on a 1-gigawatt facility, Nebius can ask for additional money up front, which goes toward site construction.
Nebius told investors in its Q2 shareholder letter that the annual contract value of a single megawatt stood at $12 million at the start of the year. Q2 deals have exceeded $20 million per year, and the company has been negotiating short-term Q3 deals that are above $40 million per megawatt.
It's reached the point where 50% to 60% of Nebius' capital expenditures have been self-financed by prepayments. That's part of the reason Nebius ended the quarter with an $8 billion cash position. As the value of megawatts and data centers increases, Nebius can get even more prepayments that reduce the necessity of shareholder dilution.
Although prepayments are an excellent funding source, they haven't been enough for Nebius and other neoclouds. However, the data centers themselves can cover the gap if lenders are willing to let neoclouds borrow against them.
Iren (NASDAQ: IREN) CEO Dan Roberts said that prepayments can keep up with most of the neocloud's capital expenditures. However, the company also said that its entire data center portfolio remains unencumbered. Iren can theoretically raise billions of dollars just by taking out loans against its facilities, and the same applies to Nebius. GPU-backed financing has been the popular route for both of these companies.
There's no need to finance the data centers if prepayments, GPU-backed financing, and realized revenue are enough to keep up with expenses. However, it's an extra resource that will make it easier to fund additional projects.
One of the bearish points for neoclouds is how they are going to raise all of the necessary capital for the data center buildouts. A focus on prepayments and GPU-backed financing has mostly answered that question, but data center financing serves as an extra funding source if needed.

### Article 25 · 2026-09-07 · dailysabah.com
Has AGI been achieved? Nvidia, OpenAI claim so

© Turkuvaz Haberleşme ve Yayıncılık 2026
Stanford University describes artificial general intelligence (AGI) as an AI system with general, human-level (or beyond) ability to learn, reason and apply knowledge across a wide range of tasks and domains.
Leading tech and artificial intelligence companies just claimed that AGI has been achieved, while also warning that "no one is prepared for the consequences of a continued rapid rise in machine intelligence."
Since the public launch of OpenAI's ChatGPT bot in late 2022, which has powered the early days of the artificial intelligence boom, the recurring questions over "whether AGI is here" and "when AGI will arrive" have been something the tech circles got accustomed to.
However, with the recent launch of OpenAI's new Astra model, or "GPT-6 Astra," Nvidia chief Jensen Huang said in a social media post that "AGI has arrived," with the OpenAI team also backing the claim.
"We're now moving into the AGI era (whether you see it as this model, the last one, or the next one), and could not do it without close partners," Greg Brockman, president and co-founder of OpenAI, said on X.
The new model, which comes after Claude's Fable.1 launch, is said to excel at sound identification, visualizing how drugs work, and even beating 48 levels of the "I'm not a Robot" simulator game.
"Astra is state-of-the-art on computer use, browsing, software engineering, cybersecurity, science, and professional work," OpenAI said in a blog post when releasing the model on Sept. 4.
"Astra marks a new frontier ​in the speed, accuracy and safety of computer use," it added.
Still, its chief scientist, Jakub Pachocki, said that monitoring and understanding what models can do was getting more difficult.
"As the models become more capable, understanding exactly what they can do gets harder," he said last Thursday, before he stunned by sharing on Sept. 6 the blog titled "An Alien Mind."
"If AI development continues along its current path, the systems we'll see in the next few years are likely to represent further capability jumps of equal or larger magnitude, and to increasingly drive their own development," the blog authored by Pachocki and shared on OpenAI's website read.
"This is a time that calls for extreme caution. I am concerned no one is prepared for the consequences of a continued rapid rise in machine intelligence," he added.
The warning follows a series of incidents involving OpenAI and other AI developers, with the most notable one being that of OpenAI's agents breaking free and hacking into the open-source platform Hugging Face – which is now being acquired by Nvidia.
"As machines become smarter, they find themselves working on higher-level concepts, and placed in environments increasingly different from those they encountered in training," Pachocki also wrote, adding that the "risks associated with AI are unfortunately going to grow from here."
Since 2022, the AI development and race to deliver more models has continued unabated, with regulations and guardrails largely trailing behind, apart from initiatives such as the EU's AI Act.
On Monday, the U.N. rights chief Volker Türk warned that advanced AI presents "an existential risk" to humanity.
Keep up to date with what’s happening in Turkey,
it’s region and the world.

### Article 26 · 2026-09-08 · bgr.com
Here's What The Numbers Actually Mean In An Nvidia Graphics Card's Name

Here's What The Numbers Actually Mean In An Nvidia Graphics Card's Name
By Asad Kashif
GPU naming schemes can be needlessly complicated, and it may seem like the biggest graphics card manufacturers just throw random numbers and letters together. But this isn't true — each letter and number in a card represents important information about the product, and understanding how Nvidia names its GPUs is integral to getting the best graphics card for your setup.
The numbers on Nvidia GPUs consist of two parts. The first two digits (or the first digit on older Nvidia cards) represent the generation, while the last two show the performance tier. Put simply, an RTX 5060 and an RTX 4060 belong to different generations but have similar performance, while an RTX 4060 and an RTX 4080 belong to the same generation but perform differently. Knowing the generation is important if you want to make use of modern features like Nvidia's DLSS, as older cards were made when these technologies either weren't available or were not as developed as they are today. A more recent generation means that the GPU is more optimized for technologies like ray tracing and DLSS, and it also means that the card is more efficient in handling processes.
The generations for modern Nvidia GPUs include the GTX 10- and GTX 16-series, as well as the RTX 20-, RTX 30-, RTX 40-, and RTX 50-series, the latter being its current generation. The GTX prefix means a card is older and fine for general gaming, while RTX means the cards support ray tracing and DLSS . These series are often also referred to using four digits by consumers, so note that the RTX 50 and RTX 5000 series are one and the same. Prior to these GPUs, Nvidia used a three-digit numbering convention. This included the GTX 200, GTX 400, GTX 500, GTX 600, GTX 700, and GTX 900 series.
The generation of an Nvidia graphics card doesn't tell you how heavy a workload the GPU can handle. For this, you refer to the last two numbers, which indicate the performance tier. The lowest tier in Nvidia's current lineups is xx50, which encompasses budget-friendly, entry-level GPUs. These are fine for casual gaming, but struggle with anything graphics-heavy and aren't intended for high frame rates in demanding games.
Next are the xx60 cards, which are mainstream, mid-range cards that most avid gamers use. These offer good performance at 1080p resolutions and decent frame rates, but cannot run high-end games at the highest graphics settings. The xx70 cards are high-end GPUs that support high-quality gaming at 1440p, while cards ending in 80 offer even more graphics processing power, something that's needed for 4K gaming. Lastly, xx90 cards are Nvidia's highest-end GPUs for any given generation, and are usually overkill for most people both in terms of price and performance.
Figuring out which Nvidia graphics card you need is easy when you understand these numbering conventions. In terms of generations, higher is almost always better. However, if you don't need fancy features like ray-tracing or AI upscaling, opting for a more powerful card from an older generation can be cheaper. For performance tiers, decide what resolution you want to game on, whether you're comfortable gaming at medium settings or want the highest-level visuals, and whether you want high frame rates. It's also worth noting that Nvidia graphics cards often have suffixes that also affect performance. For example, a card ending with Ti means it has a slight improvement over the non-Ti variant .

### Article 27 · 2026-09-08 · tradingview.com
This Nvidia Supplier Raised $1.47 Billion -- and the Stock Fell 6%

/ This Nvidia Supplier Raised $1.47 Billion -- and the Stock Fell 6%
This Nvidia Supplier Raised $1.47 Billion -- and the Stock Fell 6%
Wistron Corp. a top AI demand. The other is how to pay for that increase. Shares of Nvidia supplier Wistron slumped more than 6% after the company priced a $1.47 billion worldwide depositary receipt offering.
The corporation is selling 25 million GDRs and wants to use the proceeds partly for the acquisition of raw materials. That could sound regular. It isn't at this level.
Wistron is inside the supply chain creating AI servers for Nvidia, where demand has been growing faster than much of the industry can safely provide.
More orders means more components, more factories and more working capital, before customers eventually pay up. Good as long as the demand keeps coming in. Growth also implies it can burn a lot of cash.
Wistron shares fell on Tuesday as investors appeared more concerned over the immediate dilution from the offering. The longer term story is another matter.
AI server vendors are being expected to build at a speed that would have seemed preposterous just a few years ago. Wistron is partially seeking roughly $1.5 billion because it needs the cash up front to satisfy that demand.
The next concern is whether the extra capital is generating enough revenue and profit from AI servers to justify the dilution.

### Article 28 · 2026-09-08 · barchart.com
Dear Nvidia Stock Fans, Mark Your Calendars for September 10

Nvidia (NVDA) has been one of Wall Street's biggest winners over the years, and investors still can't seem to look away. The chip giant sits at the heart of the artificial intelligence (AI) boom, with its powerful chips helping build and run some of the world's most advanced AI models. At the same time, Nvidia is expanding its role beyond chips by providing financial support through backstops and other arrangements that help new AI data centers secure funding and get built.
Sure, the investor frenzy around Nvidia's stock has cooled somewhat this year after its incredible run. But the underlying Nvidia story hasn't lost its spark. Its fundamentals remain strong, and now another potential catalyst is coming into view. Nvidia is set to take the stage at the Goldman Sachs Communacopia + Technology Conference on Thursday, Sept. 10. The company's executive team might discuss its corporate strategy, market demand, and financial outlook during the conference, giving investors a fresh look at how Nvidia sees the next phase of the AI boom unfolding.
Rocket Lab Keeps Landing Defense Deals. Here's Why Analysts Aren't Getting More Bullish.
Why Stifel Just Revamped Its Price Target for Microsoft Stock
Micron Price Targets Are Rising - Bull Put Credit Spreads in MU Are Attractive for Investors with Limited Funds
With the market listening closely, Sept. 10 could be an important date for Nvidia's investors. Thus, here's a closer look at NVDA stock.
Over the past five years, few companies have become as closely tied to the AI boom as Nvidia. As artificial intelligence evolved from an emerging technology into one of the world's biggest investment themes, demand for the computing power needed to train and run AI models exploded, and Nvidia was in the perfect position to ride that wave. Today, its GPUs power everything from ChatGPT and cloud-based AI platforms to autonomous vehicles, robotics, and advanced scientific research, placing the company at the center of the massive global spending spree on AI infrastructure.
It's an extraordinary journey for a company that began in 1993, when Jensen Huang, Chris Malachowsky, and Curtis Priem founded Nvidia in a Denny's diner. What started as a struggling gaming startup has since become the world's most valuable publicly traded company. Nvidia's transformation, however, was decades in the making. The company first built its reputation designing graphics processors for gaming before steadily expanding its GPUs into broader computing applications. That early bet on high-performance, parallel computing ultimately became a major competitive advantage when generative AI took off.
Training and running large language models (LLMs) requires enormous computing power, and Nvidia's technology was already tailor-made for the task. Since then, the company has kept its foot firmly on the accelerator. Its Hopper-based H100 became the go-to AI accelerator during the early generative AI boom, while its newer Blackwell platform has pushed performance even further. Nvidia is now looking ahead to its upcoming Rubin architecture, which is expected to power the next generation of AI workloads. This rapid product cycle has helped Nvidia maintain a commanding position as businesses and cloud providers continue pouring billions of dollars into AI infrastructure .
And the numbers tell the story of just how successful that strategy has been. Nvidia is now valued at roughly $5.56 trillion, making it the world's most valuable publicly traded company. Its stock has delivered an extraordinary 13,347.75% gain over the past decade, putting Nvidia among the greatest wealth creators in market history. That kind of performance naturally attracts plenty of competition for investor attention. Recently, several memory-chip companies and emerging AI-focused players have delivered even bigger gains, while profit-taking has also taken some steam out of Nvidia's rally.
Still, Nvidia continues to leave the broader market in the dust. NVDA stock is up 34% over the past year and 21% so far in 2026, compared with gains of 18.3% over the past year and 12.3% in 2026 for the S&P 500 Index ($SPX). More recently, Nvidia shares have started picking up momentum again, helped by strong demand for AI infrastructure and easing concerns over how hyperscalers will finance their massive AI spending. The stock is now closing in on its all-time high of $236.54, reached on May 14, and is down just 3% from that peak.
If Nvidia's rise over the past few years has been impressive, its latest earnings report proves that the AI giant is still operating at full throttle. In its fiscal 2027 second-quarter results, published on Aug. 26, Nvidia once again delivered extraordinary growth, with revenue soaring 106% year-over-year (YoY) to $96.22 billion, compared with $46.74 billion a year earlier. The topline also comfortably topped Wall Street's $92.17 billion forecast.
Profit growth was even more impressive. GAAP net income jumped 126% to $59.69 billion, while non-GAAP EPS came in at $2.22, beating analysts' estimate of $2.10. Nvidia's non-GAAP margin also expanded by 2.5 percentage points to 75%, highlighting just how powerful the company's profitability engine remains. The star of the show was, unsurprisingly, Data Center.
The division generated a staggering $89 billion in revenue, accounting for more than 92% of Nvidia's total revenue, while posting a 117% YoY increase. The surge was fueled by relentless hyperscaler capital spending and rapidly growing enterprise adoption of accelerated computing clusters. Sequential growth was further supported by the initial volume rollout of the next-generation Vera Rubin architecture, alongside continued full-scale production of Blackwell systems across major cloud partners, including Azure, Google Cloud, and OCI.
Nvidia's growth story is also expanding beyond traditional hyperscale infrastructure. Its Edge Computing segment generated $7.2 billion in revenue, up 27% YoY, as on-device AI integration continued gaining commercial traction. Nvidia is also putting its enormous cash-generation power to work for shareholders. During fiscal 2027's second quarter, the company returned approximately $26 billion to shareholders through share repurchases and cash dividends.
As of the end of the quarter, Nvidia still had approximately $99 billion remaining under its share repurchase authorization. Looking ahead, Nvidia expects the momentum to continue. For fiscal 2027's third quarter, the company projects revenue of $108 billion, plus or minus 2%. Importantly, Nvidia is not assuming any Data Center compute revenue from China in this outlook. GAAP and non-GAAP gross margins are expected to come in at 74%, plus or minus 50 basis points.
Wall Street's confidence in Nvidia remains hard to miss. NVDA stock carries a consensus "Strong Buy" rating, with 45 of the 50 analysts covering the company recommending a "Strong Buy." Three analysts see it as a "Moderate Buy," while just one has a "Hold" rating and one calls for a "Strong Sell." And the upside Wall Street sees is anything but modest.
The average price target of $325.17 points to about 44% potential upside, while the Street-high target of $515 suggests Nvidia could rally as much as 128% from current levels. Moreover, with the stock once again hovering near record territory, investors have plenty of reason to watch closely as the company heads into its next potential catalyst.

### Article 29 · 2026-09-08 · tradingview.com
Insider Alert: Nvidia Director Sold $410 Million in Shares

/ Insider Alert: Nvidia Director Sold $410 Million in Shares
Insider Alert: Nvidia Director Sold $410 Million in Shares
Nvidia NVDA board member and Director Mark Stevens sold about $410.84 million worth of shares, according to a regulatory filing.
Stevens disposed of 1.85 million shares between Aug. 31 and Sept. 4 at prices ranging from $220 to $226. The transaction represented about 5.82% of his Nvidia holdings, leaving him with nearly 30 million shares valued at roughly $6.91 billion.
The sale comes after Nvidia reported second-quarter results showing revenue and profit roughly doubled from a year earlier as demand for its artificial intelligence processors remained strong. The shares have gained about 10% since those results were released at the end of August.
Stevens has served on Nvidia's board since 2008 and previously held the director role from 1993 to 2006. He is a former Intel executive and venture capitalist.
The large sale may attract investor attention, but Stevens retains a sizable Nvidia stake while analyst sentiment remains positive.

### Article 30 · 2026-09-08 · fool.com
Could Buying Nvidia Today Set You Up for Life?

Nvidia ( NVDA +2.55% ) has been a life-changing stock for many investors. If you invested $10,000 at the start of 2023, that sum is now worth nearly $160,000. That's life-changing returns for those who bought and held on, but could it still deliver those returns?
Let's see if buying Nvidia stock could set you up for life, as the answer may surprise you.
Nvidia has been one of the biggest beneficiaries of the artificial intelligence build-out, as its graphics processing units (GPUs) have become the industry's top choice. This has allowed the company to grow as quickly as the AI space in general, and there are not many signs of it slowing down. During Nvidia's most recent quarter, it posted year-over-year revenue growth of 106%, accelerating after slowing in 2025.
While management forecasts growth to slow next year, it isn't by much. For the next fiscal year, the company projects 70% growth -- an incredible figure, considering Nvidia is worth more than $5 trillion. What's even more amazing about this statement is that none of it has been priced into Nvidia's stock. For nearly every other company, if management tells you they will grow by 70% over the next year, the stock shoots up in response, pricing in a lot of that success. However, that's not the case with Nvidia.
Nvidia currently trades at 25 times forward earnings, which isn't all that much more expensive than the S&P 500 ( ^GSPC +0.81% ) , which trades at 21 times forward earnings. With Nvidia being an above-average company, I think this premium is warranted. But Nvidia's valuation only considers this year's growth, not next year's 70% projection. When that is factored in, Nvidia's valuation falls to below 15 times next year's earnings.
That's an absolute steal, and investors should be taking advantage of Nvidia's cheap stock price.
But does Nvidia still offer life-changing returns? I don't think so. At best, Nvidia's stock could double over the next year, providing a quick return on investment. However, that's just a single doubling. I still think that makes the stock worth buying, but it falls short of setting you up for life.
Nvidia is among the best stocks to buy in the market. Don't miss your chance to own one of the best-performing stocks at a steep discount.
By Keithen Drury – Sep 8, 2026 at 2:33AM EST

### Article 31 · 2026-09-08 · finance.yahoo.com
NVIDIA and ASML Back Mistral’s €3 Billion Round. Their Payoffs Could Look Very Different

NVIDIA Corporation (NASDAQ: NVDA ) and ASML Holding N.V. (NASDAQ: ASML ) are backing the same European AI company, but investors should expect different routes to a return.
On September 8, Mistral announced a €3 billion Series D at a post-money valuation above €21 billion. Both companies participated as existing investors. Mistral said the money would expand research, infrastructure and commercial operations. Their individual contributions were not disclosed in the announcement.
The investment case extends beyond any eventual gain on their stakes. NVIDIA can supply the computing behind Mistral's expansion; ASML can use its models to improve the machines that manufacture advanced chips.
Hardware demand meets engineering productivity
The hardware relationship predates this financing. On June 11, 2025, NVIDIA described a Mistral cloud platform whose first phase was planned around 18,000 Grace Blackwell systems. More funding could support additional deployment, although the September announcement supplies no new NVIDIA order value.
ASML's operational connection is more specific than a general bet on AI spending. In a June 12 update, it reported that early Mistral diagnostics pilots identified certain subsystem errors more than 70% faster while matching engineers' accuracy. Faster diagnosis could reduce service time and improve customer uptime if those results scale.
Both businesses therefore have reasons to welcome a stronger Mistral. Yet the risks differ. NVIDIA needs funded infrastructure plans to become delivered, economically useful computing capacity. ASML needs promising pilots to survive demanding production environments and generate benefits large enough to justify the investment.
Mistral's expanding business also changes the competitive picture. On August 11, it described plans to support third-party open models alongside its own. Hosting more models could broaden infrastructure demand for NVIDIA, even if Mistral's models lose ground. ASML's gains depend more directly on effective engineering applications.
Historical positioning offers context. Insider Monkey's tracked worksheet sample counted 285 NVIDIA holders in Q2 2026 versus 275 in Q1, and 140 ASML holders versus 133. Ken Fisher's firm increased its shares in each by approximately 3%. These quarter-end holdings predate the new funding round.
The August 14 short-interest snapshot also showed limited crowding: 1.23% of NVIDIA's float and 0.34% of ASML's, both preceding this news.
For NVIDIA Corporation (NASDAQ:NVDA), the stronger case is an expanded customer ecosystem that can buy computing infrastructure. For ASML Holding N.V. (NASDAQ:ASML), it is measurable improvements in engineering and service. The financing supports both possibilities, but neither company's earnings case should count a private valuation increase as an operating payoff.
While we acknowledge the potential of NVDA and ASML as investments, we believe certain other AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 32 · 2026-09-08 · creativebloq.com
NVIDIA's RTX Spark showcase at IFA showed me a first-hand example of how DLSS is breaking out of the gaming sphere

By Design
NVIDIA's RTX Spark showcase at IFA showed me a first-hand example of how DLSS is breaking out of the gaming sphere
By Erlingur Einarsson
RTX Spark brings DLSS 4.5 into Blender's viewport: a win for creative flow (if we don't lose the plot).
Every few months, someone promises to “fix” the 3D viewport. Faster previews, cleaner denoising, magical responsiveness — we’ve heard it all. But at IFA, a Blender demo featuring DLSS 4.5 with ray reconstruction actually made me sit up. Not because it was flashy, but because it targeted the one thing artists consistently beg for: stop making me wait for the viewport to catch up with my brain .
The presenter — Rick, armed with two identical Surface laptops and a healthy dose of confidence — showed Blender’s Cycles viewport running DLSS 4.5 side‑by‑side with OIDN and OptiX. The claim was simple: DLSS 4.5 delivers “instant feedback,” while the traditional denoisers make you wait for the image to resolve.
If you’ve ever nudged a light in Cycles and watched your scene dissolve into a grainy snowstorm before slowly reassembling itself, you know exactly why this matters.
But as with all things AI‑accelerated, the promise comes with caveats — and creatives are right to keep one eyebrow raised.
The demo: two laptops, one message: speed wins
Rick’s setup was straightforward: we had Blender’s default OIDN on one laptop, with OptiX on the same hardware, while we got DLSS 4.5 with ray reconstruction on the other.
OIDN is the reliable workhorse. OptiX is the NVIDIA ‑optimised speedster. But DLSS 4.5? It was pitched as a different beast entirely: not just denoising, but reconstructing ray‑traced detail using a learned model, complete with super resolution and a mysterious “transformer version 2” under the hood.
The viewport looked smoother. More stable. Less like a flickering cloud of noise pretending to be your scene. And crucially: changes appeared (nearly) immediately.
For look‑dev artists, lighting TDs, and anyone who spends their day nudging sliders and rotating HDRIs, that responsiveness is gold. Creative flow thrives on immediacy. Every second spent waiting for samples to accumulate is a second where your idea cools off.
Why this matters: creative flow is not a luxury
We talk a lot about render times, but not enough about iteration times . The viewport is where ideas form — where you experiment, break things, fix them, and try again. When that loop is slow, creativity suffers.
DLSS 4.5’s pitch is essentially: What if Cycles felt less like a path tracer and more like a real‑time engine while you’re working?
Is Nvidia’s DLSS 5 an AI slop machine or a game-changing technology that will take us closer to artists' original vision?
That’s a big deal, not because it replaces artistry, but because it removes friction. And friction is the enemy of bold creative decisions.
If DLSS 4.5 genuinely delivers smoother previews without compromising the accuracy artists rely on, it could meaningfully change how fast teams iterate, review, and approve work. But — and this is where I have to put my editorial hat on — speed is not the only metric that matters.
Artists have learned to be wary of AI‑powered “enhancements,” because they often come with trade‑offs that only show up once you’re knee‑deep in a production scene.
Some open questions:
Does DLSS 4.5 stay faithful enough for lighting and shading decisions?
Instant feedback is great, but not if it lies to you.
How does it handle thin geometry, fine textures, or low‑sample chaos?
Denoisers love to hallucinate detail. Reconstruction models sometimes hallucinate too much .
Will it behave consistently across stylised, NPR, or heavily composited scenes?
Blender artists don’t all work in photorealism.
Is this NVIDIA‑only acceleration going to widen the hardware divide?
OIDN works everywhere. DLSS does not.
And then there’s the bigger industry concern:
Does faster iteration become an excuse for tighter deadlines and smaller teams?
Technology that empowers creatives can also be weaponised against them. We’ve seen it before.
The tech context: DLSS isn't just a denoiser any more
DLSS 4.5 with ray reconstruction isn’t simply “OptiX but faster.” It’s a learned model that replaces parts of the denoising and temporal filtering pipeline entirely. In theory, that means better stability, cleaner glossy reflections, fewer temporal artefacts, and more detail retention in low‑sample previews
If Blender 5.3 integrates this cleanly, it could become the default viewport experience for RTX users. Not because it’s flashy, but because it’s useful .
But usefulness depends on trust. And trust requires independent benchmarks, not a controlled demo with unknown scene complexity.
Great for RTX users, [shrug emoji] for everyone else
Let’s be honest: this is an NVIDIA‑only party.
OIDN remains the cross‑vendor baseline. OptiX is NVIDIA‑optimised but still broadly accessible. DLSS 4.5, however, is locked to RTX hardware.
If Blender’s viewport experience becomes significantly better on NVIDIA GPUs, that’s great for RTX users, but it risks creating a two‑tier creative ecosystem unless AMD and open‑source alternatives catch up with their own reconstruction models.
Blender has always been a champion of accessibility. DLSS integration will need to be handled carefully to avoid fragmenting the user base.
DLSS 4.5’s ray reconstruction looks like one of the rare AI‑accelerated features that actually respects the creative process. It doesn’t try to automate artistry. It doesn’t replace human judgement. It just makes the viewport less annoying.
That’s a win.
But creatives are right to be cautious. Faster previews don’t automatically mean better decisions. And AI‑powered reconstruction models can be unpredictable in ways that only show up after hours of work.
The promise is real, and the potential is exciting. But like with AI video enhancements, the industry must resist the temptation to treat speed as a substitute for craft, or as a justification for squeezing artists harder.
If DLSS 4.5 lands cleanly in Blender 5.3, it could become one of the most meaningful quality‑of‑life upgrades Cycles has seen in years. Just don’t let the marketing gloss distract from the need for rigorous testing, cross‑vendor parity, and respect for the creative labour this tech is supposed to support.

### Article 33 · 2026-09-08 · fool.com
Nvidia, Palantir, and Meta Platforms Are Rattling Wall Street With This $18.6 Billion Warning

No trend has fueled Wall Street's nearly four-year bull market quite like the evolution of artificial intelligence (AI) . Empowering software and systems with the tools to make autonomous, split-second decisions is a multitrillion-dollar addressable opportunity that investors clearly don't want to miss.
Several of Wall Street's most influential businesses have led the AI revolution, including Nvidia (NASDAQ:NVDA), Palantir Technologies (NASDAQ:PLTR), and Meta Platforms (NASDAQ:META).
Nvidia is the heart and soul of the AI infrastructure build-out. Its graphics processing units (GPUs) hold a virtual monopoly in AI-accelerated data centers , with no other GPU makers particularly close to rivaling the compute capabilities of its hardware.
Meanwhile, Palantir and Meta have demonstrated the value of AI applications. Palantir's AI-driven software-as-a-service platform, Gotham, helps the U.S. government and its allies plan and oversee military operations, while Meta has deployed generative AI solutions across its social media advertising platforms that allow businesses to tailor static and video ads to individual users.
Although all three AI titans are growing their sales and profits at a breakneck pace, things may not be as perfect as their headline operating results suggest.
The people who know Nvidia, Palantir, and Meta best are sending a terrifying message to Wall Street
Arguably, no one knows these three leading businesses better than their insiders, consisting of high-ranking executives, board members, and beneficial owners of at least 10% of outstanding shares.
Securities law requires insiders to file Form 4 with regulators no later than two business days after buying or selling shares of their company's stock, including the exercising of option contracts. Aside from complying with securities law, this transparent reporting allows investors to effectively track whether insiders are putting their money where their mouth is.
Based on Form 4 filings over the trailing five-year period (as of Sept. 4), insiders at this AI trio have been notable net sellers of their company's stock:
Nvidia : $6.31 billion in net insider sales
Palantir : $6.63 billion in net insider sales
Meta : $5.69 billion in net insider sales
Collectively, the people who know these companies best have dumped approximately $18.6 billion more in stock than they've purchased over the last half-decade.
However, it's important to keep in mind that high-ranking executives and board members are often heavily compensation in stock and/or options. Selling shares to cover federal and/or state tax bills is often required. In other words, tax-based selling isn't necessarily bad news for investors.
Unfortunately, insiders are raising red flags at both ends of the spectrum. While there are several reasons for insiders to sell shares, not all of which are nefarious, there's only one reason to buy: the belief that shares will rise. Over the trailing five years, insider buying has been almost nonexistent:
This lack of insider buying may speak to the checkered history of next-big-thing technological innovations. While insiders at all three companies are undoubtedly excited about AI altering their respective futures, every game-changing innovation since the mid-1990s has endured an early stage bubble-bursting event. Investors have consistently overestimated the pace of adoption or optimization of new technologies, leading to eventual disappointment.

### Article 34 · 2026-09-08 · tomshardware.com
One-slot, low-profile Nvidia RTX 3060 12 GB with two monitor outputs breaks cover at Newegg for $496 — bus-powered model looking for a use case in local LLM work

One-slot, low-profile Nvidia RTX 3060 12 GB with two monitor outputs breaks cover at Newegg for $496 — bus-powered model looking for a use case in local LLM work | Tom's Hardware
One-slot, low-profile Nvidia RTX 3060 12 GB with two monitor outputs breaks cover at Newegg for $496 — bus-powered model looking for a use case in local LLM work
By Bruno Ferreira
12 GB of VRAM wasn't supposed to be a lot, but these days it's a luxury.
Not that long ago, we reported that Nvidia was dusting off the blueprints for the RTX 3060, in its 12 GB form. At the time , we'd spotted it in stores for about $339.99, but just like with ever-climbing memory, hard drive, and SSD prices, two months passed is an eternity. The same cards are now selling for $489 new, and one particular specimen is the SRhonyra RTX 3060 12 GB Low Profile card , for $495.59.
SRhonyra RTX 3060 12 GB Low Profile card - $495.59
This card and its price may raise more than a few eyebrows, but there are reasons why it exists. First off, it's a one-slot model, making it easy to put many of them to work in the same machine with relatively little concern for airflow. They have no power inputs and rely on 70 W delivered by the PCIe slot alone, eschewing the need for a high-end PSU and lots of cables. Third, the low-profile form factor makes it possible to place them in potent puny personal computers.
Attentive readers might surmise that one (or more) of these would be good candidates for an entry-level local LLM rig. That's precisely how SRhonyra is pitching the card, calling it "capable of local AI" and "running 7B [to] 13B LLMs." A standard-dimensioned, fully powered RTX 3060 is capable of drawing a maximum of 175 W, so it's fair to assume the performance of the diminutive variant will sit below that of its full-sized brethren, given it ought to only draw 70 W of juice from the PCIe slot.
Even then, it's likely that people interested in these cards are looking to use them either as secondary GPUs, or use more than one in the same box to be able to virtually pool their VRAM and use larger models than you'd otherwise be able to. The low power draw also means they're a simple, thoughtless drop-in to an existing system, whereas larger, more power-hungry cards require careful consideration with physical spacing (or lack thereof), power supply sizing, and ever-annoying cables.
Such a dumb product. Half the size, half the power but also half the performance and no cost benefit. You gain nothing.
If they had made the chip with modern fab technology so you got the same performance at 70W then you're talking.
I think the RTX 3050 6GB proves that they don't have to lose half the performance. Running a higher number of cores at lower clocks should be more efficient, even if there are limits to that approach. But there are thermal issues with this specific design they came up with.
This should have been brought up last thread: The RTX A2000 12GB is GA206 silicon with slightly less cores than the RTX 3060 (3328 vs. 3584) and a 70W TDP. So if the A2000 performs better than this card, that proves that power is not the issue.
That appears to be the case. The average A2000 is getting 6274 in Time Spy, which is 30% faster than the 4821 this frankencard got.

### Article 35 · 2026-09-08 · fool.com
Billionaire Stanley Druckenmiller Has 2 Megacap Stocks Worth Watching (Hint: His Top Holding Isn't Amazon, Alphabet, or Nvidia)

One of the best investors riding the artificial intelligence (AI) revolution is Stanley Druckenmiller at the Duquesne Family Office. Druckenmiller is a famous trend follower and was one of the early traders to buy into Nvidia ( NVDA +2.55% ) as a way to ride the AI boom .
Today, Duquesne and Druckenmiller own two megacap stocks benefiting from AI infrastructure spending, but his top holding by far is an undiscovered winner in genetic testing that few investors are talking about.
Regarding AI infrastructure, Druckenmiller holds stakes in two megacap technology companies in the United States: Amazon ( AMZN +0.56% ) and Alphabet ( GOOGL -0.61% ) ( GOOG -0.70% ) . Today, we can see these bets primarily benefiting from growing AI spending.
Amazon's cloud computing division -- Amazon Web Services (AWS) -- is the leader in its sector and saw revenue grow 37% year-over-year last quarter to $42.2 billion. There is a massive backlog of spending on its AI cloud services, which power fast-growing start-ups like Anthropic and OpenAI. CEO Andy Jassy recently mentioned that AWS could grow to $1 trillion in annual revenue, driven by cloud market share gains and rising total spending on computing infrastructure worldwide.
Alphabet is a bit of a different bet, as it combines the fast cloud growth with the dynamics of the consumer and enterprise AI application economy. The Google Cloud division grew revenue by 82% year-over-year to $24.8 billion, catching up quickly to AWS, though it remains much smaller. Alphabet is growing quickly with its Gemini chatbot, now serving nearly 950 million monthly users, but its Google Search division faces significant competitive pressures.
Overall, these two stocks are a small % of the Duquesne portfolio today, but they have been nice long-term winners for Druckenmiller.
An underfollowed top holding in genomics
Notably, close to 20% of Druckenmiller's portfolio, as of his latest quarterly filing -- excluding international holdings -- is a stock called Natera ( NTRA +0.35% ) . Natera is a disruptor in the diagnostics segment and uses its technologies for analyzing tumors and women's health during pregnancies, along with organ transplants.
Last quarter, Natera's revenue grew 38% year over year to $753 million, due to an increase in tests performed. Full-year revenue guidance was raised as well. Accelerating business momentum is why the stock has been a huge winner for Druckenmiller.
Duquesne first invested in Natera in Q3 of 2022, when the share price was between $35 and $50. Today, it trades at $328, closing in on about 10 times the initial cost basis (the exact figure is unknown). Natera has been a massive winner for Druckenmiller, which is why it is the largest U.S. stock he owned at the end of last quarter.
Why doesn't he own Nvidia anymore?
Curiously, even though he was an early bettor on Nvidia, Druckenmiller's Duquesne Family Office currently does not own any of the AI chipmaker. He said in 2024 that he sold Nvidia after it went on a massive run, with sales coming at a split-adjusted price of $80 to $90. Today, Nvidia trades at $230.
The reason for the sale was valuation concerns, but he subsequently said it was a mistake not to let his winners run. Nvidia has not been in the Duquesne portfolio since early 2024.
Druckenmiller's current bet on AI semiconductors is Taiwan Semiconductor Manufacturing . This is the company that actually builds Nvidia chips (Nvidia just designs them). It could be another way to take advantage of the AI trend, but with a stock trading at a more reasonable valuation and a monopoly position in advanced chipmaking at the moment.
Billionaire Stanley Druckenmiller Has 2 Megacap Stocks Worth Watching (Hint: His Top Holding Isn't Amazon, Alphabet, or Nvidia)
By Brett Schafer – Sep 8, 2026 at 1:30PM EST
