# Blind reader, matter census batch 3 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 35 articles (numbers 71 to 105,
2026-09-10 to 2026-09-10, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 71 · 2026-09-10 · gurufocus.com
Nvidia Makes Bold Move to Expand Global AI Empire

Nvidia ( NASDAQ:NVDA ) is working with Australian cloud partners on up to 2 gigawatts of AI computing capacity by 2027, expanding the chipmaker's ecosystem beyond selling processors into designing AI factories.
The program involves sites designed to host several generations of Nvidia DSX infrastructure. Partners include IREN ( NASDAQ:IREN ), Sharon AI, Firmus, ResetData, Megaport, CDC, NEXTDC and AirTrunk.
DSX combines hardware, networking and software compatible with Nvidia's CUDA ecosystem. Nvidia argues that software improvements can make the infrastructure more productive and durable, allowing operators to treat compute capacity as an investable, revenue-generating asset.
Nvidia Builds an Australian AI Factory Network
IREN plans to apply the DSX reference architecture across its development portfolio, including its 800-megawatt Bundey campus in South Australia. The vertically integrated approach gives IREN control over power, construction and operations, potentially helping it bring capacity online at scale.
Sharon AI plans to deploy up to 68,000 Nvidia GPUs, while other partners are preparing data centers, powered shells and connectivity for accelerated computing. The network will support multiple Nvidia chip generations rather than a single product cycle.
Demand will come from companies building models and applications locally. Atlassian plans to use Nvidia's Nemotron open models, datasets and tools to customize multimodal applications and enhance Rovo, its workplace AI platform.
For Nvidia investors, the announcement demonstrates how the company can influence infrastructure decisions long before chips are installed. Standardizing facilities around DSX and CUDA could encourage customers to remain inside Nvidia's ecosystem when they upgrade equipment or expand capacity.
Execution still matters. Two gigawatts represents an upper target, not completed capacity. Partners must secure power, financing, equipment and customers while meeting construction deadlines. If the projects arrive on schedule and maintain strong utilization, Australia could become both a domestic AI hub and another durable demand channel for Nvidia.

### Article 72 · 2026-09-10 · fool.com
An Nvidia Move Just Put AMD and Intel on the Defensive

Nvidia ( NVDA +2.55% ) has played a pioneering role in the field of artificial intelligence (AI) thanks to its graphics processing units (GPUs), whose massive parallel computing power has enabled the training of popular large language models (LLMs).
Importantly, Nvidia has maintained its dominance in the AI chip market, as evidenced by its recent results that showed a significant jump in revenue and earnings . The good news for Nvidia investors is that it is pulling the right strings to ensure that it continues to dominate this lucrative market. The company's entry into the server central processing unit (CPU) market is one such move, which has put this market's heavyweights -- Intel and Advanced Micro Devices -- on the defensive.
AMD and Intel have a big reason to be worried right now
Server CPUs are in high demand right now, primarily due to the shift toward agentic AI and inference workloads in data centers. AMD notes that the server CPU market's revenue could increase at an annual rate of 50% through 2030, creating a $220 billion revenue opportunity by the end of the decade.
AMD and Intel have traditionally dominated the server CPU market. They manufacture chips based on the x86 architecture. However, the growing demand for agentic AI and inference workloads has triggered a shift toward Arm -based chips owing to their low power consumption and higher efficiency. Nvidia is capitalizing on this trend.
The AI bellwether's Vera server CPU is designed on Arm's architecture. The important thing to note is that Nvidia sees healthy demand for its stand-alone Vera server CPU. CFO Colette Kress remarked on Nvidia's August earnings call :
Today, we are in full production of our next-generation Vera CPU. As a stand-alone product, Vera expands our TAM even further. Vera completes agentic task, 1.8x faster on the spec benchmark and provides 5x the bandwidth per watt than any other data center CPU.
Kress added that the Vera CPU will be deployed by "every major hyperscaler, neocloud, AI lab, and system OEM." The company is already shipping this product to key customers and expects to sell $20 billion worth of Vera CPUs this year. What's more, Nvidia expects its Vera CPU revenue to double next year.
So, Nvidia's chip poses a clear threat to AMD and Intel, especially as the share of x86 server processors shrinks. Tom's Hardware noted in June that Arm-based servers account for 45% of the data center market's revenue share. Nvidia's prediction that its server CPU revenue will double next year suggests that Arm-based processors are on track to capture a larger share of this market, which doesn't bode well for Intel and AMD.
Nvidia's continued AI chip dominance and valuation should send the stock soaring
Nvidia stock has jumped just 21% in 2026, while AMD and Intel have clocked solid triple-digit gains. However, that could change in the future due to Nvidia's stronger growth and improving prospects.
Also, Nvidia is the better AI stock to buy in this cohort owing to its significantly cheaper valuation. It has a price-to-earnings ratio of 29, lower than AMD's reading of 122 and Intel's earnings multiple of 88.
Nvidia's significantly lower valuation suggests it has greater upside potential than Intel and AMD. Moreover, Nvidia's move into the server CPU market could stifle AMD and Intel's growth, giving investors another terrific reason to buy Nvidia stock before it steps on the gas.
By Harsh Chauhan – Sep 10, 2026 at 1:06PM EST

### Article 73 · 2026-09-10 · zacks.com
NVIDIA vs. AMD After Earnings: Which AI Stock Should You Buy Now?

NVIDIA vs. AMD After Earnings: Which AI Stock Should You Buy Now?
NVIDIA's Data Center revenues jumped 117%, while total sales rose 106% in fiscal Q2 2027.
AMD's Data Center sales doubled, with Q3 revenues projected to grow 41% year over year.
NVIDIA's 63.7% net margin and 24.26 forward P/E compare with AMD's 15.6% and 69.59.
NVIDIA’s AI Growth Surges as Data Center Demand Rises
NVIDIA’s Data Center business has remained the primary growth engine. Data Center revenues were $89 billion in the fiscal second quarter of 2027, up 117% year over year and 18% quarter over quarter, according to the company’s Aug. 26 press release. Overall, NVIDIA generated $96.2 billion in revenues, up 106% year over year and 18% sequentially.
Alongside rapid revenue growth, NVIDIA exhibited strong profitability. During the quarter, NVIDIA’s GAAP and non-GAAP gross margins both came in at 75% compared with roughly 72.5% a year ago. The company is also translating rapid revenue growth into even faster earnings growth, supported by continued gains in operating income.
NVIDIA now projects revenues of around $108 billion, plus or minus 2%, for the fiscal third quarter of 2027, up 12% sequentially from the midpoint. Thus, NVIDIA’s growth trajectory remains robust, while its cutting-edge Vera Rubin platform is in full production, indicating that the company is well-poised to gain from the next phase of AI infrastructure spending.
AMD’s Strong Data Center Growth Bolsters Its AI Ambitions
The Data Center segment was the primary driver of AMD’s revenue growth, with sales doubling from the same period a year ago in the second quarter of 2026, according to the company’s Aug. 4 press release. Total revenues reached $11.5 billion, up 50% year over year and 13% from the previous quarter.
Strong demand for AMD’s EPYC server processors boosted revenue growth. At the same time, the company’s Helios platform has entered its initial ramp-up phase, while its Instinct accelerators continue to scale rapidly. Consequently, AMD projects third-quarter 2026 revenues to reach $13 billion, plus or minus $300 million. At the midpoint, this would represent 41% year-over-year growth and a 13% sequential increase.
AMD also expects Data Center revenues to improve further in the latter half of 2026, and profitability is projected to improve steadily. The company projects a 56% non-GAAP gross margin in the third quarter, indicating continued progress in margin expansion.
NVIDIA vs. AMD: Why NVDA Is the Stronger AI Stock to Buy Now
The rollout of NVIDIA’s advanced Vera Rubin platform, strong margins, and sheer dominance in AI infrastructure, driven largely by Data Center growth, are expected to support a positive movement in its shares. AMD, meanwhile, is closing the gap through strong Data Center growth, expanding AI accelerator sales, and improving profitability.
Despite AMD’s growing momentum with its EPYC server processors and Instinct accelerators, NVIDIA’s full-stack platform gives the company a competitive edge as AI infrastructure spending increases. With a larger AI infrastructure footprint, NVIDIA remains the market leader.
Moreover, NVIDIA’s net profit margin of 63.7% versus AMD’s 15.6% highlights NVIDIA’s greater efficiency in converting revenues into bottom-line earnings. Therefore, NVIDIA remains the stronger buy, backed by superior profitability, AI infrastructure leadership and full-stack platform advantage.
Additionally, NVIDIA appears more attractively valued than AMD. By price-to-earnings ratio, NVDA trades at 24.26 forward earnings compared with AMD’s 69.59 forward earnings multiple.
NVIDIA currently has a Zacks Rank #1 (Strong Buy), while AMD has a Zacks Rank #3 (Hold). You can see the complete list of today’s Zacks Rank #1 stocks here .

### Article 74 · 2026-09-10 · benzinga.com
Nvidia CEO Jensen Huang Said Nvidia Compute Is 'Fungible, Durable and Highly Rentable' — Now Oracle CEO Stands Impressed as 4-Year Old GPUs Fetch 20% Premium

Nvidia CEO Jensen Huang Said Nvidia Compute Is 'Fungible, Durable and Highly Rentable' — Now Oracle CEO Stands Impressed as 4-Year Old GPUs Fetch 20% Premium
Oracle Corp. (NYSE: ORCL ) has echoed Nvidia Corp (NASDAQ: NVDA ) CEO Jensen Huang's bullish view on AI hardware longevity .
Oracle Says Older GPUs Are Gaining Value
During Oracle's fiscal 2027 first-quarter earnings call, CEO Clay Magouyrk highlighted the continued strength of the company's AI infrastructure business.
"GPU longevity and value continue to impress," Magouyrk said. He added that all the GPU capacity coming up for renewal in the quarter was either renewed or resold at a 20% premium to previous contracts, with most of those GPUs being at least four years old.
"We see a long useful life with increasing value for the AI capacity we're deploying," Magouyrk said.
Magouyrk also said the company delivered 850 megawatts of AI capacity containing more than 300,000 GPUs since the end of its previous quarter.
First-quarter deliveries were nearly three times Oracle's fourth-quarter figure and represented 73% of the capacity delivered throughout the prior fiscal year.
Oracle also closed more than $30 billion in additional AI contracts during the quarter without requiring additional capital, while GPU utilization remained extremely high at 97.9%.
The comments come days after Huang reiterated his view that AI computing should be viewed as a productive asset rather than rapidly depreciating technology.
"NVIDIA compute is fungible, durable and highly rentable," Huang wrote on X . "It is a productive, revenue-generating asset."
Huang has also argued that Nvidia's older hardware can remain useful for years . In August, he said Nvidia's A100 GPUs are "mission-capable from 2020 through 2029."
Nvidia has partnered with major investment firms, including Apollo Global Management (NYSE: APO ), BlackRock Inc. (NYSE: BLK ), Blackstone Inc. (NYSE: BX ), Brookfield Asset Management (NYSE: BAM ), Goldman Sachs (NYSE: GS ) and KKR & Co. Inc . (NYSE: KKR ), to help mobilize more than $500 billion in capital over time.
Oracle Q1 Earnings Beat Estimates
Oracle reported quarterly earnings of $1.92 per share, topping the analyst consensus estimate of $1.74 by 10.34%.
Quarterly revenue came in at $19.35 billion, ahead of the Street estimate of $19.14 billion and up from $14.93 billion in the year-ago quarter.
For the second quarter, Oracle expects revenue growth of 30% to 34% and cloud revenue growth of 65% to 71%, while forecasting adjusted earnings per share of $1.85 to $1.93.
Price Action: Oracle closed at $152.94, down 5.38% on Thursday. The shares rose 4.13% to $159.26 in after-hours trading, according to Benzinga Pro .
Benzinga Edge Stock Rankings place Oracle in the 96th percentile for Growth, while its price trends indicate short-term upside but continued weakness over the medium and long term.

### Article 75 · 2026-09-10 · fool.com
Nvidia's CEO Called the Dip Months Ago. Here Is How the Trade Played Out.

On June 8, Nvidia ( NVDA +2.55% ) CEO Jensen Huang called the sharp technology sector sell-off that occurred in early June a buying opportunity. Speaking to reporters in Seoul that day, Huang said the artificial intelligence (AI) infrastructure build-out was still in its early stages. So, investors should be "very happy because now you can buy at a discount."
His call seems to have been spot on so far. From its opening price on June 8 to the close of trading on Sept. 4, Nvidia's stock gained about 9.6%, compared with a roughly 3.7% gain for the S&P 500 ( ^GSPC +0.81% ) over the same period.
However, investors should note that Nvidia's shares did not immediately move higher after Huang's comments.
Huang was not identifying the bottom of the slump
On June 29, Nvidia fell to an intraday low of $189.80, almost 10% below its June 8 opening price. A $10,000 investment made at the June 8 open would have at that point been worth about $9,030.
The stock then spent several weeks recovering. However, its biggest move came after Nvidia reported results for its fiscal 2027 second quarter, which ended July 26. That report came out after the market closed on Aug. 26, and shares jumped 8.7% on Aug. 27. On Sept. 4, Nvidia closed at $230.36.
Hence, most of the gains made by the stock since Huang's June comments came only after Nvidia gave investors fresh evidence that its AI growth story remained strong.
Nvidia's results strengthened Huang's argument
Nvidia's revenue surged 106% year over year to $96.2 billion in its fiscal second quarter, while data center revenue jumped 117% to $89 billion. Management also guided for third-quarter revenue of $108 billion, plus or minus 2%.
Management's preliminary expectation is for revenue to grow by about 70% in its fiscal 2028. Wall Street's previous consensus expectation was for revenue growth of roughly 44% for fiscal 2028. Management also said this outlook is based on its production being supply-constrained, suggesting that demand remains stronger than the company's ability to supply AI computing systems.
These results have strengthened Huang's June argument. Nvidia's fiscal Q2 results and outlook now provide significantly more evidence that AI infrastructure spending still has room to grow.
Is Nvidia still available at a discount?
Nvidia's valuation still seems reasonable considering its expected growth. The stock is trading at roughly 24.7 times its expected fiscal 2027 earnings of $9.31 per share. The multiple falls to about 14.9 times based on the fiscal 2028 earnings estimate of $15.46 per share.
There are risks, however. Nvidia expects its gross margin to slip from the 75% it was last quarter to roughly 71% to 72% in the fourth quarter as the memory shortage and higher component prices raise its costs. The company's fiscal third-quarter guidance also assumes that it will sell no data center chips to customers in China.
Huang's June call has proven fairly accurate so far. While he did not identify the exact bottom of the dip in Nvidia's stock, it has since outperformed the broader market. The company's latest results provided much stronger support for the fundamental argument behind the CEO's call.
Jensen Huang saw opportunities in June's tech sector sell-off, but the next few months told a more complicated story for Nvidia.
By Manali Pradhan, CFA – Sep 10, 2026 at 2:26PM EST

### Article 76 · 2026-09-10 · gurufocus.com
Nvidia Just Made an Australia AI Move That Could Be Much Bigger Than Investors Think

Nvidia Corp. ( NVDA , Financials ), the semiconductor company best known for its artificial intelligence chips , is planning an Australian expansion that could reshape the country's data center market.
The company is working with Firmus, CDC, NEXTDC and AirTrunk to build as much as 2 gigawatts of AI computing capacity by 2027. That number stands out.
Australia currently has about 1.6 GW of computing capacity, according to Data Centres Australia research cited by Reuters. Nvidia's proposed buildout could therefore exceed the country's entire existing load.
The facilities will use Nvidia's DSX platform and are intended to support growing demand for AI models, applications and autonomous agents.
NEXTDC Ltd. (NXT, Financials), the Australian data center operator, is among the public companies positioned to participate in the expansion.
But more computing also means more pressure on electricity grids and water supplies. Australia has been attracting large data center investments while regulators and communities increasingly question their environmental footprint.
For investors, the next test is whether Australia can add power infrastructure quickly enough to support Nvidia's ambitions. AI demand may be strong, but electricity availability could decide how much of the planned 2 GW actually gets built.

### Article 77 · 2026-09-10 · cnbc.com
Chinese Nvidia rival Enflame soars 206% on stock market debut as AI demand stays hot

Chinese chipmaker Enflame, which is developing domestic alternatives to U.S. rivals like Nvidia, has seen its stock soar 206% after debuting in Shanghai.
The company saw huge demand , with its initial retail offering drawing orders for over 6,000 times the shares available before it reallocated more stock to that group.
Enflame, which is backed by tech giant Tencent, is considered one of China's so-called "four little dragons" of AI chipmaking and is the last of that group to go public.
The other three all surged on listing, and have remained higher since. In December, MetaX soared nearly 700% on its first day of trading, while Moore Threads gained over 400% on its trading debut. Biren jumped 76% on its IPO in January.
Investors are betting on the ability of domestic AI chipmakers to replace Nvidia in China. International chipmakers led by Nvidia accounted for nearly 60% of China's AI accelerator market in 2025, according to IDC data cited in Enflame's prospectus , translated by CNBC.
Nvidia has seen its exports in China's data center compute market shuttered by U.S. export controls and Beijing's lukewarm interest in importing advanced chips as the country pursues tech self-sufficiency.
China's semiconductor buildout is accelerating. Goldman Sachs said in an August report that growing foundation models and AI applications in China were driving development across AI chips, foundries, memory and advanced packaging.
The analysts expect China's semiconductor capital spending to reach $82 billion by 2030, driven by capacity expansion in memory and advanced nodes amid a growing generative AI trend.
Local startups such as Moonshot AI's Kimi K3 closed the gap to the frontier with leading U.S. models, and Chinese AI systems are seeing growing uptake across the globe. Rival Z.ai said its GLM-5.3-Flash model runs entirely on China-made chips . Analysts said the company likely used a combination of chips from leading Chinese domestic player Huawei, as well as chips from Enflame and other local companies.
Alibaba is also developing its own AI chips and accompanying software, as well as optimizing systems for leading Chinese models.
Founded in 2018, Enflame is building AI processors as China looks to boost its efforts in model building amid major capability gains from domestic developers.
Enflame said it plans to use proceeds from the listing to develop and commercialize its fifth- and sixth-generation AI chips, as it seeks to match the performance of high-end products from international rivals.
The company reported revenue of 990 million yuan ($147 million) in 2025, up from 722 million yuan a year earlier, but has yet to turn a profit.
Tech hardware has become a key driver of Chinese stock performance in recent months.
In July, shares of chipmaker CXMT, which makes dynamic random-access memory (DRAM) chips, a key feature of some AI systems, soared nearly 466% in their debut on Shanghai's tech-heavy STAR Market, making CXMT the most valuable China-listed company.

### Article 78 · 2026-09-10 · gurufocus.com
Piper Sandler Drops Hot Take On Nvidia Stock

Piper Sandler is urging investors to buy Nvidia ( NASDAQ:NVDA ), calling it the outright leader in AI compute and among the market's cheapest stocks.
Analyst David O'Connor initiated coverage with a Buy rating and $300 price target. He estimates Nvidia controls 80% of the AI-compute market and 50% of unit shipments, giving it unmatched scale as compute demand expands.
The call arrived as Nvidia shares fell about 2% Thursday amid rising Treasury yields and higher oil prices. That disconnect highlights the analyst's long-term thesis: macro pressure does not change the company's competitive position.
Why Piper Sandler Sees More Nvidia Upside
O'Connor argues Nvidia preserves its lead by releasing next-generation products faster than rivals. Its Vera Rubin rollout appears on schedule and could account for approximately 20% of fiscal third-quarter 2027 data-center revenue. Grace Blackwell systems are expected to supply the remainder.
Agentic AI drives demand. More autonomous systems require greater computing capacity, while rising GPU rental prices suggest supply remains tight. O'Connor expects shortages to continue for another two to three years, supporting pricing and limiting the threat from competing accelerators.
He also believes fears that application-specific integrated circuits will take significant inference share are exaggerated because overall demand is expanding much faster than available supply.
Piper Sandler projects Nvidia revenue growing at a 47% compound annual rate, with earnings per share increasing at a similar pace to $30 in fiscal 2030. At roughly 14 times estimated fiscal 2028 earnings, O'Connor considers the stock unusually inexpensive relative to its growth.
Investors must still watch product execution, supply expansion and competition. Yet Piper Sandler's central argument is unusually direct: Nvidia combines dominant market share, rapid product launches and accelerating earnings with a valuation that does not fully reflect that leadership.

### Article 79 · 2026-09-10 · fool.com
Nvidia Returned $26 Billion to Shareholders Last Quarter Alone. Here's What That Buys You as an Investor.

Nvidia 's ( NVDA +2.55% ) report for the second quarter of its 2027 fiscal year showed that the company is still enjoying incredible growth in conjunction with artificial intelligence (AI) demand trends. The fiscal quarter, which wrapped on July 26, saw the business record non-GAAP (adjusted) earnings per share of $2.22 on revenue of $96.22 billion. For reference, the average analyst estimate had modeled adjusted per-share earnings of $2.10 on revenue of $92.17 billion.
Along with its fiscal Q2 report, Nvidia also announced that it had returned $26 billion to shareholders in the quarter -- with $20 billion coming in the form of buybacks and $6 billion in the form of dividend payments. What does that mean for shareholders?
How should investors view Nvidia's dividend right now?
With the first-quarter report it published in May, Nvidia announced it was raising its quarterly dividend to $0.25 per share -- marking a 2,400% increase. While the payout increase is huge on a percentage basis and substantially boosts returned income as a component of owning Nvidia stock, the dividend payout still isn't big enough to make a huge difference in the near term.
For example, the company's dividend payout in the second quarter would have come out to $250 if you owned 1,000 shares of Nvidia stock. If you had your dividends set up to be rolled into new stock purchases through a dividend reinvestment program ( DRIP ), it would have added another full share and some change to your holdings.
To put things in perspective, 1,000 shares of Nvidia would be worth roughly $226,000 as of this writing. In other words, $250 worth of dividend payments on a position of that size is far from being a game changer. In the near term, it won't buy you much.
On the other hand, there is potential for the company's dividend payouts and enrollment in a DRIP to make a real difference over the long term. Nvidia's dramatic payout increase earlier this year suggests that the company is interested in making dividends a meaningful component of stock ownership, and it wouldn't be surprising to see the company deliver another meaningful payout next year.
The potential hike probably won't be anywhere close to this year's 2,400% raise, but it doesn't have to be. With the stock's dividend yield currently sitting at roughly 0.4%, the payout is still relatively small compared to the company's current share price -- but there's still big potential for its dividend program to reward long-term shareholders.
What do Nvidia's buybacks mean for investors?
Nvidia bought back $20 billion worth of shares in fiscal Q2 -- a figure that might look massive at first glance, but one that should be viewed in the context of the company's overall size. With Nvidia's market capitalization currently sitting at roughly $5.44 trillion, the company's $20 billion buyback doesn't look particularly significant as a one-off event.
The shares that Nvidia bought back last quarter were retired, which reduces the company's total shares outstanding -- and increases earnings per share due to the lower share count. With the company issuing roughly $4 billion in shares to employees as part of its stock-based compensation plans in the quarter, the net size of its buybacks in the quarter is actually around $16 billion. Taken in isolation, this net buyback amount looks relatively small -- but the good news is that Nvidia is still reducing its share count even after accounting for stock-based compensation.
Nvidia's business is hugely profitable thanks to its category-leading artificial intelligence hardware and software, and the company doesn't need to rely on stock sales to fund its operations. The buybacks in Q2 aren't a game changer, but the AI leader still has roughly $99 billion in authorizations for additional buybacks -- and it could move to repurchase shares more aggressively if it comes to think that the valuation picture becomes substantially more attractive.
What's $26 billion in the grand scheme of things?
Returned income isn't a central component of Nvidia stock ownership right now. While that could change in the coming years, the company is still very much in growth mode. Using its cash generation to fund internal development, acquisitions, and investments is probably a much better use of capital than returning money to shareholders, so the relatively small significance of $26 billion in returned income last quarter shouldn't be taken as a negative.
By Keith Noonan – Sep 10, 2026 at 6:30PM EST
The company's $6 billion in distributed dividends marked its largest ever payout, but the stock's yield is still relatively low.
The company's $20 billion in buybacks last quarter will help boost earnings per share, but it won't have a dramatic impact.

### Article 80 · 2026-09-10 · datacentremagazine.com
Inside NVIDIA's Ambitious Plan for AI Factories in Australia

Inside NVIDIA's Ambitious Plan for AI Factories in Australia
By Saffron Humphreys
NVIDIA has confirmed it is working with eight Australian cloud and infrastructure providers to build data centre capacity capable of hosting its DSX AI factory platform .
The move would more than double the country's current 1.6GW of computing capacity, according to industry group Data Centres Australia. NVIDIA is targeting up to 2 gigawatts (GW) of new capacity by 2027.
Firmus , Sharon AI , IREN , Megaport , ResetData , CDC , NEXTDC and AirTrunk are the companies collaborating with NVIDIA for the expansion. Each will operate AI factories on land, power and shell capacity designed to host multiple generations of NVIDIA compute.
NVIDIA will supply the DSX platform itself, along with accelerated computing, networking, software and ecosystem support.
The figures behind the announcement give a sense of how fast Australia's AI infrastructure market is moving:
Up to 2GW of new AI factory capacity is targeted by 2027
Australia's existing data centre capacity stands at roughly 1.6GW
IREN's Bundey campus in South Australia is being scaled towards 800 megawatts
CDC already operates more than 550MW across Australia and New Zealand, with a further 800MW under construction
Raj Mirpuri , NVIDIA's Vice President of Global AI Clouds and Infrastructure Ecosystem, says: "AI factories turn energy into intelligence: the essential resource of the AI economy."
AI factories turn energy into intelligence: the essential resource of the AI economy.
"NVIDIA DSX is a full-stack platform compatible with the CUDA ecosystem and enhanced through software over the life of the infrastructure, making AI factories more productive, fungible and durable – and a new investable asset class.
"Through our partnerships with Australian NCPs, this infrastructure can support multiple generations of NVIDIA compute and expand local access to accelerated computing and NVIDIA Nemotron open models, helping Australian innovators build AI at home."
Firmus, one of the earliest movers in the group, is expanding its existing Project Southgate initiative to develop NVIDIA-powered AI factories across Australia and the wider Asia-Pacific region.
Oliver Curtis , Co-founder and Co-CEO of Firmus, says the project marks a concrete step for the country's compute ambitions: "Project Southgate represents a tangible commitment to building Australia's AI future.
"Together with NVIDIA, we are developing AI factories that will give Australian businesses, researchers and innovators access to world-class computing capacity at home, while positioning Australia to meet growing AI demand across Asia-Pacific."
IREN is pairing NVIDIA's DSX reference architecture with its own power, land, data centre and GPU deployment operations.
Daniel Roberts , Co-founder and Co-CEO of IREN, says: "Building AI infrastructure at scale requires integrating every layer: data centres, compute and software.
"Combining IREN's vertically integrated platform with the NVIDIA DSX AI factory reference architecture provides a repeatable blueprint to bring capacity online at scale.
"We are applying that blueprint across our development portfolio, bringing IREN's proven international delivery and operating experience to our 800-megawatt Bundey campus in South Australia."
Sovereign compute for research and enterprise
ResetData is positioning itself around data residency and sovereign compute for government, research and enterprise customers.
Marcel Zalloua , Co-founder and Joint CEO of the sovereign AI hosting company, says: "At ResetData, we've proven that when Australian businesses and researchers like the team at ProCan at the Children's Medical Research Institute have access to high-performance compute, they can deliver industry-leading results.
"That is why we are proud to partner with NVIDIA and develop the sovereign, purpose-built infrastructure solutions that will accelerate Australian expertise and empower local businesses with the tools needed to compete and innovate on the global stage."
CDC, the Infratil-owned operator, is one of the larger capacity holders in the group.
"CDC operates more than 550 megawatts of capacity across Australia and New Zealand, with a further 800 megawatts under construction and additional growth planned to support world-leading, high-density workloads for critical infrastructure," says Greg Boorer , Founder and CEO of CDC.
"Our facilities use 100% renewable electricity and incorporate pioneering zero water advanced cooling technologies certified for NVIDIA accelerated computing infrastructure."
NVIDIA says the expanded capacity would give local developers greater access to accelerated computing and its Nemotron open models, naming Heidi and Atlassian among the organisations already building regional AI applications on Australian infrastructure.
Our facilities use 100% renewable electricity and incorporate pioneering zero water advanced cooling technologies certified for NVIDIA accelerated computing infrastructure.
An Australian AI infrastructure developer expanding its Project Southgate initiative on NVIDIA's DSX reference architecture, targeting hyperscale and AI-native demand across Australia and Asia-Pacific through 2026 and beyond.
A NASDAQ-listed Australian neocloud that signed a six-year, 72MW compute collaboration with NVIDIA in mid-2026, taking its total AI factory capacity to 132MW and supporting up to 40,000 Grace Blackwell GB300 GPUs.
A vertically integrated power, land and GPU deployment operator applying the DSX reference architecture across its development portfolio, including its 800-megawatt Bundey campus in South Australia.
An Australian-founded global software-defined network provider expanding NVIDIA compute access through subsidiary Latitude.sh, bringing AI inference closer to users to reduce latency.
An Australian AI cloud platform delivering NVIDIA accelerated computing with local data residency for enterprise, government and research customers, including medical researchers at ProCan.
An Infratil-owned operator running over 550MW of renewable-powered capacity across Australia and New Zealand, with 800MW more under construction using zero-water cooling technology.
An ASX-listed colocation provider developing liquid-cooled, high-density AI-ready facilities on the DSX platform, interconnected with major global cloud platforms.
A regional hyperscale data centre operator expanding AI-ready powered shells with direct-to-chip liquid cooling to support high-density AI workloads across Asia-Pacific.
Vice President of Global AI clouds and Infrastructure Ecosystem

### Article 81 · 2026-09-10 · fool.com
Nvidia Is Suddenly Outpacing the S&P 500. Expect That to Continue.

Nvidia ( NVDA +2.55% ) had a sluggish start to the year, but its rally ahead of earnings gained momentum when the company reported solid results. It's felt long overdue, but the chipmaker is once again outpacing the S&P 500 with a 23% year-to-date return.
Investors should expect Nvidia to continue beating the S&P 500, as it has done for many years. Strong financial results and the continuation of the artificial intelligence supercycle are two major reasons why.
It's very hard to find a company that generates substantial revenue and can still deliver accelerating growth rates. The company earned $96.2 billion in its fiscal 2027 second quarter, representing a 106% year-over-year growth rate. Based on guidance , the chipmaker will soon bring in more than $100 billion per quarter.
All of those earnings also come with impressive margins. Net income more than doubled year over year, reaching $59.7 billion in the process. Nvidia has consistently shown that the AI supercycle is gaining momentum. People have called it a bubble for a while, but with Nvidia anticipating 70% year-over-year revenue growth in its fiscal 2028, the bubble concerns have become quiet murmurs.
Even the company's valuation is solid. It trades at a 25.4 forward P/E ratio and has a PEG ratio below 0.60. Nvidia's fundamentals are improving at a faster rate than its stock price, suggesting its valuation could become even more attractive when it reports earnings again later in the year.
Nvidia earns higher quarterly profits than most chipmakers generate in quarterly revenue. That gives investors an idea of how much market share Nvidia has over the competition, and as the AI boom accelerates, Nvidia is well-positioned to increase its lead.
Its Vera Rubin platform is about to show up in future results, and it's not just hyperscalers driving the demand.
"This time last year, one lab alone was driving the buildout; today, we have a golden age of new AI labs and start-ups, multiple frontier labs scaling in parallel," Jensen Huang said in the Q2 FY27 press release.
Huang also touted the arrival of physical AI when describing Nvidia's opportunity. While it's not an exclusive opportunity for Nvidia, the AI chipmaker is better positioned than any other company. Its GPUs are the technological bedrock, regardless of which companies figure out physical AI the fastest.
Nvidia's position, strengthening fundamentals, and reasonable valuation make it an easy pick that could outperform the S&P 500 over an extended period. Nvidia's sluggish start was a fluke that investors have rightly called out, as evidenced by the recent accumulation.
By Marc Guberti – Sep 10, 2026 at 6:07AM EST

### Article 82 · 2026-09-10 · hlth.com
Verily Secures NVIDIA Investment to Advance Precision Health AI Platform

By Company Type
Verily Health has secured a strategic equity investment from NVIDIA to accelerate development and commercial deployment of its precision health AI infrastructure. The investment builds on an operational collaboration between the companies established in October 2025 and follows Verily’s transition to an independent entity earlier this year.
A central focus of the relationship is the Verily Pre Platform, which serves as a data and technical foundation for research and health system operations. Pre is designed to harmonize fragmented clinical information into FHIR-native, AI-ready datasets for life sciences organizations, healthcare providers and researchers.
Verily is integrating NVIDIA’s accelerated computing technologies into the platform, including NVIDIA B200 GPUs, the NeMo generative AI framework, Parabricks for secondary genomic analysis and RAPIDS data science libraries. The infrastructure is intended to help researchers using Pre Workbench process multimodal biomedical datasets and train AI models more efficiently.
NVIDIA’s technology will also support the scaling of Forecast 1.0, Verily’s proprietary multimodal foundation model. Forecast 1.0 combines genomic sequencing data with longitudinal electronic health record flowsheets to predict long-term chronic disease risk trajectories and organ decompensation.
The investment will additionally support Verily Me, the company’s patient engagement offering, including its conversational AI companion, Violet. The platform is designed to support preventive care and guide patients through longitudinal chronic disease management.
The relationship with NVIDIA comes as Verily continues to develop its position as an independent healthcare technology company, with Alphabet remaining a non-controlling minority stakeholder. Access to NVIDIA’s accelerated computing infrastructure is expected to support increasingly compute-intensive biomedical and multi-omics AI applications.
“We are pleased to welcome NVIDIA as a new investor in Verily. These investments strengthen our ability to pursue the opportunity ahead,” said Stephen Gillett, Chairman and CEO of Verily. “Together, these investments and the continued support of our current investors accelerate our vision to build a trusted foundation for healthcare, bringing together the information and intelligence needed to power better decisions and unlock the full potential of AI across the healthcare ecosystem”.
HLTH Inc. is a dynamic community delivering unique value to the healthcare industry through a mix of unparalleled global events, inspirational content, and impact-driven initiatives.
Any communication that claims to represent HLTH or any third party offering discounted hotel rooms or attendee lists is NOT AFFILIATED with HLTH and should be considered fraudulent . Please book your accommodations only through HLTH’s official channels to ensure authenticity and security.

### Article 83 · 2026-09-10 · gurufocus.com
Nvidia Just Put Palantir at the Center of a Massive AI Bet

Palantir Technologies Inc. ( PLTR , Financials ), the data analytics and artificial intelligence software company , is getting a bigger test from one of the most important names in AI.
Nvidia is working with Palantir to deploy a sovereign AI stack across critical supply chains, starting with Nvidia's own internal operations. That detail matters.
Palantir is not simply selling another software contract. Nvidia is putting the technology into its own workflows first, giving the partnership a high-profile proving ground.
The two companies have already been working together on operational AI. Palantir's platform combines its Ontology software with Nvidia's accelerated computing, CUDA-X libraries and Nemotron models to help companies and government agencies use AI on sensitive data and complex operations.
Sovereign AI is becoming more important as governments and companies try to keep strategic data, models and infrastructure under tighter local control. Nvidia has also been pushing sovereign AI systems for U.S. agencies and critical infrastructure operators.
For Palantir investors, the real opportunity is what happens after Nvidia. If the deployment works well inside one of the world's largest AI companies, it could give Palantir a stronger case when competing for similar projects across defense, manufacturing and government.

### Article 84 · 2026-09-10 · fool.com
Nvidia Has $96 Billion in Quarterly Revenue. Here's Why the Stock Is Still a Buy.

Nvidia ( NVDA +2.55% ) has seen revenue go parabolic during the artificial intelligence (AI) boom, climbing more than 11-fold since 2022 to $303 billion on a trailing-12-month basis. In fiscal Q2, which ended July 26, it posted $96 billion in revenue, up 106% year over year. That's rare growth at this scale -- but the bigger takeaway isn't what's already in the books. It's what management says comes next.
The company is guiding for roughly 70% revenue growth in fiscal 2028, and its next major chipset platform, Vera Rubin, is already shipping. Here's why this $5.4 trillion market-cap stock still looks like a no-brainer buy.
Nvidia's opportunity goes well beyond the hyperscalers
Demand from hyperscalers like Amazon , Alphabet , and Microsoft continues to drive a big portion of Nvidia's data center business. Last quarter, hyperscalers generated nearly $49 billion in revenue -- about half of Nvidia's total revenue. On top of that, Amazon Web Services said it plans to deploy an additional 2 million GPUs through fiscal 2029, which reinforces long-term demand visibility.
But Nvidia revealed even stronger growth outside these core customers. Revenue from neocloud (specialized AI clouds), industrial, and enterprise customers rose 138% year over year to $40 billion, outpacing hyperscaler growth. That matters because hyperscalers are increasingly touting the capabilities of their in-house chips, potentially presenting a risk to Nvidia over time.
Nvidia's push to diversify its customer base is working. The $40 billion in non-hyperscaler revenue includes sovereign government buyers, regional cloud providers, and AI start-ups. Many of these customers don't want to design chips themselves; they want a proven, end-to-end platform that includes compute, networking, and software, and it's clearly opening up a massive opportunity for Nvidia to extend its leadership.
Wall Street is still underestimating Nvidia's growth
Nvidia stock trades at about 15 times next year's earnings estimate, which is a bargain for the leading AI chip supplier growing this quickly.
A big driver of next year's growth will be Nvidia's new Vera Rubin computing platform, which began shipping in early August. It is ramping up quickly and is expected to total 20% of Nvidia's data center revenue in fiscal Q3.
Even with its gross margin under pressure from higher memory prices, the setup for investors looks very attractive. Analysts currently project $411 billion in revenue for fiscal 2027, followed by a 65% jump to $678 billion in fiscal 2028.
However, Nvidia's guidance implies about $700 billion in revenue next year. This means Nvidia's fiscal 2027 earnings may also come in ahead of Wall Street estimates, implying the stock is even cheaper than its 15x forward (one-year) earnings multiple.
The risk is that data center spending may not rise in a straight line, with constraints like power availability and potential regulation that could slow the build-out and demand for Nvidia's chips. But Nvidia still looks like a business that can be meaningfully larger years from now -- and that's why the stock remains compelling.
Nvidia's next AI platform is already shipping -- and its 2028 growth outlook could be far bigger than Wall Street expects.
By John Ballard – Sep 10, 2026 at 4:39PM EST
The stock is trading at 15 times next year's consensus earnings estimate, even as analysts' current revenue estimate doesn't line up with management's guidance.

### Article 85 · 2026-09-10 · tradingview.com
SpaceX Stock Chases 3-Week Winning Streak: CFO Says ‘Very Strong’ Nvidia Alliance Could Fuel 10-GW AI Push

/ SpaceX Stock Chases 3-Week Winning Streak: CFO Says ‘Very Strong’ Nvidia Alliance Could Fuel 10-GW AI Push
SpaceX Stock Chases 3-Week Winning Streak: CFO Says ‘Very Strong’ Nvidia Alliance Could Fuel 10-GW AI Push
SpaceX plans to expand terrestrial AI compute capacity from just over 2 GW in 2026 to 5-10 GW in 2027.
Johnsen said SpaceX has visibility into the power, facilities and permits needed for the buildout, with electricity emerging as AI’s main constraint.
SpaceX sees sustained demand for compute, with Johnsen saying “almost everybody” in the AI industry has approached the company.
SpaceX CFO Bret Johnsen said that the company’s “very strong” relationship with Nvidia could support its access to key AI processors as it prepares to expand its terrestrial computing capacity from just over 2 gigawatts at the end of 2026 to between five and 10 gigawatts in 2027.
SPCX stock is on track for its third consecutive weekly gain, rising about 0.2% so far this week.
Speaking at Goldman Sachs’ Communacopia + Technology Conference late Thursday, Johnsen reiterated that SpaceX will rely exclusively on Nvidia hardware for its expanding AI infrastructure. “We came out and talked about the fact that we’re NVIDIA exclusive,” Johnsen said.
During SpaceX’s first public earnings call last month, CEO Elon Musk said the company had chosen to build its data-center infrastructure exclusively on Nvidia because it viewed the chipmaker’s Vera Rubin architecture as the best AI computing platform available.
“That strong relationship, we hope, certainly will translate into good allocation from a compute perspective because that’s the piece that we don’t control,” Johnsen said.
The CFO added that SpaceX has visibility into the power, facilities and permits needed to support its 2027 target. He said Musk’s earlier prediction that electricity would become AI’s principal constraint was already playing out across the industry.
“It feels like almost everybody,” he said. “There might be one company that hasn’t called us, and we haven’t called them.” SpaceX does not expect the AI boom to slow next year, with Johnsen predicting demand will continue “up and to the right in a meaningful way.”
The company already has major compute relationships with Anthropic and Google. Their disclosed agreements are worth $26 billion annually if fully performed, with Google’s capacity package including access to about 110,000 Nvidia GPUs.
SpaceX signed another hosting deal with an undisclosed customer earlier this month that is expected to generate about $1.11 billion per month beginning Dec.1, or about $13 billion in annual recurring revenue. Johnsen said the agreement gave the company “even more conviction” in its $100 billion year-end ARR target.
Most of SpaceX’s hosting agreements carry commitments of about six months, allowing the company to generate revenue today while retaining flexibility to redirect capacity toward Grok and its other AI products. “You do not want to get in a situation where you constrain your own products…because you were giving away the compute forever,” Johnsen said.
He also said that the economics reduce the risk of SpaceX’s substantial infrastructure spending. “The risk related to these investments for us is dramatically less when we are in less than a one-year payback mode,” Johnsen said, adding that older Nvidia GPU generations continue to command strong pricing.
Nvidia also owns nearly 123 million SpaceX shares, a holding valued at almost $21 billion at the end of June.
SpaceX Stock Eyes $195 On Bullish Pattern
Frank Cappelleri, founder and president of CappThesis, identified a potential bullish cup-and-handle pattern in SpaceX shares, with a higher low near $130 and a handle forming since mid-August. A confirmed breakout above $150 would complete the setup and point to a measured-move target of about $195, which is 32% above current levels and near the stock’s post-IPO highs.
Shares briefly hit $154.70 on Thursday before paring gains to 0.4%, leaving the breakout unconfirmed, though the stock outperformed the S&P 500 and Dow, which both fell about 0.6%. Cappelleri also highlighted SpaceX’s position above its rising 20-day and newly formed 50-day moving averages as constructive signals.
The gain followed SpaceX’s 104th Falcon 9 launch of 2026, which carried a classified U.S. Space Force payload. However, expiring post-IPO lockups could pressure the rally: only about 2.6 billion of SpaceX’s more than 13 billion shares currently trade publicly, with another 2.3 billion set to become eligible by year-end.
How Do Retail Traders Feel About SpaceX?
On Stocktwits, retail sentiment for SpaceX has been ‘bearish’ over the past week amid ‘low’ message volume.
One user said , “$SPCX another day another rejection at $150. Another 3.4% of shares are getting unlocked Aug 20. More sell pressure.”
Another user said, “If $SPCX keeps holding the $145–146 area and starts reclaiming $150+, I think this base gets more and more legitimate.”
SPCX stock has declined 8% over the past three months.

### Article 86 · 2026-09-10 · finance.yahoo.com
Amazon Triples Its NVIDIA GPU Orders to 3 Million Chips as AI Demand Surges

Amazon.com, Inc. (NASDAQ: AMZN ) and NVIDIA Corporation (NASDAQ: NVDA ) announced an expanded deal on August 26 that will bring an additional 2 million Nvidia GPU processors to Amazon data centers, building on AWS's earlier plan to add more than 1 million NVIDIA GPUs starting in 2026. The new processors, which include NVIDIA's Blackwell Ultra, Rubin and Rubin Ultra GPUs, are expected to arrive in Amazon Web Services data centers in 2027 and 2028.
The agreement goes far beyond simply purchasing more GPUs, with the expanded deal encompassing deeper collaboration across AI factories, CPUs, networking infrastructure, open models, data processing, and robotics, defining it as a larger infrastructure partnership instead of a single hardware order. That scale reflects how important the Amazon-NVIDIA partnership has become to both companies' AI strategies: NVIDIA Corporation (NASDAQ:NVDA) gains a massive buyer as the company targets more than $1 trillion in Blackwell and Rubin revenue through 2027, while Amazon.com, Inc. (NASDAQ:AMZN) secures the compute capacity required to continue scaling AWS's AI infrastructure business.
Notably, Amazon's increased NVIDIA order comes as the company expands its own competitive custom-silicon business. Amazon's internal chip range, which includes Trainium AI accelerators, Graviton CPUs, and Nitro networking chips, is reported to have reached a $25 billion annualized revenue run rate. Separately, Amazon says it has secured more than $225 billion in revenue commitments for Trainium, including major multi-year commitments from Anthropic and OpenAI.
The announcement's scale, with plans for more than 3 million total GPUs in a five-month period, reflects how swiftly AI infrastructure commitments have grown across the industry's major participants this year. The deal strengthens Amazon's position as one of NVIDIA's largest customers at a time when cloud providers are scrambling to secure chip supply years in advance. It will likely take until 2027 or 2028, when the newly ordered chips arrive, to determine whether that spending converts into the AI-driven cloud growth that investors are betting on.
Hedge fund ownership increased in both companies. Amazon.com, Inc. (NASDAQ:AMZN)'s ownership interest increased from 353 funds in the first quarter to 369 in the second, with Arrow Street Capital as its largest hedge fund shareholder through a $9.6 billion stake. NVIDIA Corporation (NASDAQ:NVDA) had a similar gain, from 275 to 285, with Fisher Asset Management as its top stakeholder at $18.1 billion, showing that both companies remain heavily held by institutional investors.
The case for Amazon.com, Inc. (NASDAQ:AMZN) is based on obtaining years of processor capacity at a time when AI infrastructure demand shows no signs of diminishing, offering AWS a clearer route to scaling its AI cloud business without supply restrictions becoming a bottleneck. The broader scope of the partnership suggests a developing strategic relationship rather than a one-off hardware purchase, and Amazon's concurrent buildout of its own Trainium and Graviton silicon shows that it's not wholly dependent on NVIDIA Corporation (NASDAQ:NVDA), giving it negotiating leverage and a hedge against future supply or pricing risk. Meanwhile, AWS's plan to deploy an additional 2 million NVIDIA GPUs adds visibility to demand, supporting the company's own outlook of $1 trillion in Blackwell and Rubin revenue by 2027.
The case for caution begins with the scale and duration of the investment. The chips won't arrive until 2027 and 2028, so any AI-driven growth this deal is supposed to support is a long-term gamble rather than a short-term catalyst, and AI infrastructure need can shift drastically over that span. Amazon's expanding internal silicon business begs the longer-term question of how long its reliance on NVIDIA will last, as a company developing competitive chips has an incentive to reduce its reliance on external suppliers over time.
This broadened partnership highlights the amount of capital both companies are ready to spend for a multi-year AI infrastructure buildout. Amazon.com, Inc. (NASDAQ:AMZN) appears to be the clearer near-term beneficiary, obtaining both chip supply and validation of its AI cloud strategy, while NVIDIA Corporation (NASDAQ:NVDA) receives another major multi-year demand signal from one of the world's largest cloud providers. Investors in both companies should keep an eye on how AWS's AI infrastructure revenue trends as the new chips arrive in 2027, since that will be the clearest test of whether this commitment translates into real cloud growth. Investors should also keep note on how quickly Amazon's internal silicon business scales relative to its external NVIDIA purchases, as this will indicate how the balance of power in this partnership evolves over time.
While we acknowledge the potential of AMZN as an investment, we believe certain AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 87 · 2026-09-10 · fool.com
Here's Where Wall Street Analysts See Nvidia's Share Price Going

It would be an understatement to say that Wall Street is bullish on Nvidia ( NVDA +2.55% ) .
The artificial intelligence (AI) chip manufacturer announced its second-quarter results on Aug. 26, and they were stunning. Revenue of $96.2 billion was more than double that of the same quarter a year ago. Diluted earnings per share of $2.46 rose 128% from last year and were $0.12 higher than the average analyst estimate.
So I just checked the latest data on price targets, which are Wall Street analysts' official predictions of where the stock will be in 12 to 18 months, based on historical and projected earnings. Suffice it to say that, on average, analysts see Nvidia's stock rising, and fast.
The average price target for Nvidia among Wall Street analysts is $327, which is about 42% above the current price of $230. Such an increase in the share price would not be unprecedented for this stock, of course. It's up 34% over the past 52 weeks and more than 900% over the past five years. That rapid rise has brought the company's market cap to a whopping $5.56 trillion, making it the largest publicly traded company in the world by market cap.
Analysts' price targets for Nvidia vary widely, ranging from $220 (Argus Research clearly believes the shares will lose value) to $515, the target set by Raymond James . Most analysts put the stock's forward price somewhere between $300 and $350.
The vast majority of analysts recommend a buy or strong buy
Of 60 analysts, 48 currently have a buy recommendation on the stock, and another nine have a strong buy. Deutsche Bank recommends a hold.
In recent days -- soon after the company's Q2 results came out -- J.P. Morgan analyst Harlan Sur raised his target for the stock from $280 to $320. If the average price target proves correct, the chipmaker's market cap would soar to nearly $8 trillion.
Can it go that high? Well, Nvidia's management sees revenue rising to $108 billion in the third quarter, and expects full-year revenue to soar 70% over last year, which is much higher than the 44% growth consensus projection from analysts.
And one last data point: Revenue from data centers came in at $89 million for the second quarter, up 117% from a year ago. That suggests the massive AI infrastructure build-out is already generating revenue and is not just a hopeful promise for the future. That might reassure investors that this stock has strong upside potential.
Matthew Benjamin is a contributing Motley Fool stock market and investing analyst covering publicly-traded companies across all sectors. Prior to The Motley Fool, Matt was a senior markets expert at an investing newsletter in Baltimore, an editorial consultant to the World Bank and the International Monetary Fund (IMF), and an economics correspondent at Bloomberg News. He holds a B.A. from Bucknell University and an M.A. from New York University. Fun fact: Matt has met every Federal Reserve Chair from Paul Volcker through Jerome Powell.
By Matthew Benjamin – Sep 10, 2026 at 5:30AM EST

### Article 88 · 2026-09-10 · barchart.com
NVDA Stock Alert: What to Know as Nvidia Faces DOJ Probe

Nvidia (NVDA) stock inched lower on Sept. 10 following reports that the U.S. Department of Justice (DOJ) is intensifying its regulatory scrutiny of the titan's $17 billion deal with artificial intelligence (AI) startup Groq.
As investors reacted to the DOJ news, NVDA tanked below its 20-day moving average (MA) today, indicating the downward momentum may sustain in the near term.
Nvidia CEO Jensen Huang Just Called CrowdStrike Its Top Security Partner. How to Play CRWD Stock Here.
Google Plans to Build Mammoth Solar Farm on an Abandoned Coal Mine. This Penny Stock Just Won the Deal.
At the time of writing, Nvidia shares are up more than 15% versus the start of this year.
What the DOJ Probe Means for Nvidia Stock
The Department of Justice is investigating whether Nvidia structured its agreement with Groq to avoid antitrust scrutiny.
Announced last year as a non-exclusive technology licensing deal, the arrangement also brought Groq's chief executive Jonathan Ross and other senior executives to Nvidia, while Groq remained independent.
The DOJ reportedly opened its inquiry shortly after the deal was announced and has since issued Nvidia a formal request for information.
The development is bearish for NVDA shares because it adds regulatory uncertainty around the titan's aggressive expansion across the AI ecosystem.
Potential fines and tighter scrutiny of future deals could also limit Nvidia's ability to consolidate technology and talent, potentially weighing on investor sentiment.
Should You Buy the Dip in NVDA Shares?
The recent pullback in Nvidia stock may actually be a compelling buying opportunity for long-term investors since the DOJ is reportedly unlikely to force the deal to be unwound.
Plus, the company's dominant market positioning remains unmatched, driven by massive enterprise demand for its artificial intelligence chips and robust 66% operating margins.
Trading at about 24x forward earnings — well below its historic five-year valuation averages — the AI stock's risk-reward profile favors buying on the dip.
A small 0.46% dividend yield makes Nvidia even more attractive to own for the long term.
How Wall Street Recommends Playing Nvidia
Wall Street analysts remain bullish as ever on NVDA stock for the next 12 months.
According to Barchart, the consensus rating on Nvidia sits at "Strong Buy," with the mean price target of about $325 indicating potential upside of roughly 45% from current levels.

### Article 89 · 2026-09-10 · fool.com
70% Revenue Growth for Nvidia Next Year May Make It the Best Stock to Buy In the Market

When companies speak, investors need to listen to what they say. While the market may have one notion or conception about a stock, when a trustworthy company says something to the contrary, investors should pay attention.
That's what I think is happening with Nvidia ( NVDA +2.55% ) stock right now, as the market isn't very convinced about the company's next year's prospects despite management telling investors that it expects 70% revenue growth.
This mismatch makes Nvidia among the best stocks to buy in the market right now, as the implications of it growing 70% next year make the stock an absolute bargain at today's levels.
During Nvidia's second-quarter earnings call, CFO Collette Kress gave guidance that Nvidia's revenue will grow by 70% next fiscal year. This assumes a supply constrained state, which I think is a safe bet thanks to memory chip shortages and AI budgets continuing to rise. Furthermore, Nvidia has pretty much undershot every projection it has provided investors since the AI race began in 2023, so this is likely the floor of where the company expects to grow.
Regardless of whether it's the floor, 70% growth for any company is impressive, let alone Nvidia, which is the world's largest company by market cap, valued at more than $5 billion.
For this fiscal year, Wall Street analysts expect $9.31 in earnings per share. Nvidia's earnings and revenue have grown in lockstep, so it's safe to assume the company's earnings will also rise by about 70%. This projects Nvidia to have EPS of $15.83.Right now, Nvidia trades for 29 times earnings, which is pretty cheap compared to where it has traded over the past three years.
Regardless, if Nvidia achieves earnings per share of $15.83 and has a valuation of 29 times earnings, that would price the stock at nearly $460 per share. Currently, Nvidia trades for about $230 per share, so this clearly projects it's a double.
If you can find a stock that's slated to double with a fairly high certainty and in less than two years, then there's really no question as to whether the stock is a buy or not. Nvidia is among the best stocks to invest in right now, and the market hasn't priced in any of 2027's growth yet. That's a rare opportunity for investors, and now is the time to pounce on it .
By Keithen Drury – Sep 10, 2026 at 3:30AM EST

### Article 90 · 2026-09-10 · wccftech.com
NVIDIA DGX Spark “AI Supercomputer” Impressions – The Future of AI Computing In Tiny Boxes

The acceleration within the AI space has sparked a revolution in the PC segment. We have seen major chipmakers embark on the "AI PC" journey, which involves dedicated client designs that mix Windows applications with dedicated and local AI subsystems, and then we have dedicated boxes for AI, which are made primarily for local acceleration of models and agents.
Last year, NVIDIA introduced its DGX Spark PC , the first PC of its kind to tackle LLMs and Agents in what is dubbed to be an "AI Supercomputer". Soon after the launch, other manufacturers started to label their own Mini PCs as dedicated AI boxes while competition rose from other camps. In short, the DGX Spark was the first to spark the local AI box movement, and a year later, we have finally got the opportunity to try it out ourselves.
NVIDIA DGX Spark - Specs & The GB10 Dissection
NVIDIA's DGX Spark was the first system to be announced with the GB10 Superchip. The same chip will be equipped on the upcoming RTX Spark platforms , which are headed for launch next month.
NVIDIA refers to GB10 as a Superchip, and it scales the Grace Blackwell architecture down to Mini developer PCs and workstations.
The idea behind DGX Spark was to design a Mini AI Supercomputer with the Blackwell GPU architecture. To make this happen, NVIDIA developed the GB10 Superchip, which combines innovations from data centers, such as NVFP4, CUDA, SLANG, TensorRT, vLLM, CX-7 NIC, NVLINK C2C, TMEM, and more, down to a Mini PC platform that utilizes a small form factor, made possible using multi-die packaging tech, a very low-power C2C interface, and Unified Memory Architecture (UMA).
As a result, the DGX Spark Workstation was built, which offers the following key features and benefits:
GB10 Grace Blackwell Superchip: Accelerates AI, Data Science, Compute, Rendering & Visualization
128GB Coherent Unified System Memory: Works with Large AI models up to 200 billion parameters; fine-tune models of up to 70 billion parameters
ConnectX-7 Networking: Connect two DGX Spark systems to work with models of up to 405 B parameters
DGX Base OS and NVIDIA AI Software Stack: Seamlessly move workloads from DGX Spark to DGX Cloud or any accelerated data center or cloud infrastructure
So let's dive into the specifications of the GB10 Superchip. First up, we have the SoC composition, which shows that the chip itself is composed of two dielets: an S-Dielet which houses the CPU, memory subsystem, etc, and a G-Dielet which houses the GPU core. These two dielets are packaged together using Advanced 2.5D packaging and are fabricated on TSMC's 3nm process technology.
The CPU is based on the ARM Arch v9.2 architecture with 20 cores in total. There are 2 clusters of 10 cores each, and each core has a private L2 cache and a 16 MB L3 cache per cluster, so 32 MB in total. The first cluster is based on the Cortex-X925 design, and the second cluster is based on the Cortex-A725 design.
The GPU is based on the GB100 Blackwell architecture and is considered an iGPU since it is on the same package and silicon. It features 5th Gen Tensor Cores with DLSS 4 support and RTX Ray Tracing cores. It produces up to 31 TFLOPs of FP32 and 1000 TOPS of NVFP4 (FP4) compute for AI workloads. The GPU also gets an additional 24 MB of L2 cache.
Moving into the memory system, the NVIDIA GB10 Superchip SOC features support for 256b LPDDR5x (UMA) with up to 9400 MT/s speeds, enabling up to 301 GB/s of raw bandwidth, and up to 128 GB of maximum capacity. The system fabric is a high-performance coherent fabric that offers support for the CHI-E Coherency Protocol. The GPU has access to the entire system bandwidth of 600 GB/s (Aggregate) over the C2X interface.
There's also 16 MB of System Level Cache, which serves as L4 for the CPU and enables power-efficient data-sharing between the multiple engines on the SoC. The C2C interface is also high-bandwidth and low-power, enabled through NVIDIA's NVLINK architecture.
On the connectivity side, NVIDIA's GB10 Superchip SoC offers PCIe, USB, Ethernet over PCIe, and drives up to 4 concurrent displays (3 DP + 1 HDMI) at up to 4K @120Hz with DP Alt-mode, and up to 8K @ 120Hz with HDMI 2.1a. Security features include Dual Secure Root support, SROOT processor, OSROOT processor, and support for both fTPM and discrete TPM. The whole chip has a TDP of 140W.
The following is the block diagram of the NVIDIA GB10 Superchip SoC:
Scalability is also another fun aspect of the GB10 Superchip. You can connect multiple GB10 chips through NVIDIA's ConnectX Technology and scale throughput, bandwidth, and DRAM capacities to support larger AI models. The ConnectX NIC is connected to the GB10 SoC using a PCIe Gen5 x8 interface, and the units communicate with each other using Ethernet.
NVIDIA calls the GB10 Superchip SoC a successful collaboration between them and MediaTek since the CPU IP is from MediaTek. The chip underwent extensive performance modeling of GPU memory traffic into MediaTek's memory subsystem.
The NVIDIA DGX Spark comes equipped with 4 TB of NVMe storage, which is very fast and runs at Gen5x4 speeds.
Setting up the NVIDIA DGX Spark could be tricky for beginners, but NVIDIA provides setup guides for most of the basic functionality.
The tricky part is that if you're coming from Windows platforms, then getting used to NVIDIA DGX OS, which is based on Ubuntu 24.04.4 (LTS), will take some time.
At launch, the DGX Spark shipped without most basic applications, which needed to be installed separately, but with the latest units, the Spark PC comes with DGX Dashboard and NVIDIA Sync already set up. These two are essential applications to monitor the status of your Spark PCs.
If you need to install them, then setting up DGX Dashboard and NVIDIA Sync will hardly take 15-30 minutes through the onboard terminal, since all you have to do is copy/paste and follow the steps in the playbooks .
Out of the box, the PC comes pre-installed with Firefox, Firmware Updater, and basic apps that you will find on other Linux distros, though updated to match the DGX Spark theme. Also, on the first boot, the Spark will download an update, which will take some time (around 45 minutes in our case).
The settings menu lets you configure various aspects, including the resolution. Running a 4K display at 240Hz was no issue, and you can also find the full updates menu here, which will ensure that the software and apps are running the latest builds.
Most of the action on the DGX Spark is either done in the terminal app or JupyterLab. The lab interface can be booted directly from the DGX Dashboard, which also offers a separate update menu for local apps. The DGX Dashboard offers a nice visualization of the system memory and GPU utilization.
Since we had another Spark at our disposal, we used the Connect-X7 cable to stack them up into one cluster. You can do this either through the terminal (manual) or leave it to NVIDIA's Sync app, which was more effective. The playbook was straightforward, and we had the two DGX Spark PCs running on a single IP through the 200 Gbps network.
The Sync app also evaluates the network speed through a short test, and after that, you are all set up to run local models in a dual cluster config that has access to 256 GB of memory.
You can stack as many DGX Spark units as you like; we have heard examples of up to 18, but NVIDIA says that you can stack many more. Given that model sizes continue to expand while becoming faster, two or four DGX Spark PCs should be the sweet spot for local AI developers.
Now, we move on to the benchmarks. The NVIDIA DGX Spark doesn't stack the CPU cores or the GPU cores, so you are limited to just one Spark when evaluating basic benchmarks. We managed to run Geekbench 7 on our system.
In single-core tests, the DGX Spark scores 2568 points, while in multi-core tests, it scores 23,656 points.
DGX Spark Geekbench 7 ST
The single-core performance of the DGX Spark's 20-Core Arm CPU is decent. It ends up being faster than the Ryzen AI MAX+ 395, which operates at up to 5.1 GHz, while the DGX Spark runs much slower.
DGX Spark Geekbench 7 MT
In multi-core, the DGX Spark sees a much better result, coming close to x86 desktop offerings with higher thread counts, and sitting ahead of the mobile SoCs. The chip used by the incoming RTX Spark PCs will also feature a similar CPU but with optimized clocks, so expect better results on that versus the DGX Spark, which is geared at 24/7 workstation and developer usage.
For gaming, we tried Cyberpunk 2077 running on Steam using the Proton 11.0 "Experimental" release and the Steam Linux Runtime 4.0. We followed the guide that was already available on Reddit a few months back, and were able to get the game running in perfect state with all RTX capabilities enabled.
I first wanted a taste of the native GPU capabilities that the GB10 Superchip had to offer. It has the same core count as the RTX 5070, but since we are TDP-limited to 140W, which shares the budget with the memory and the CPU, you are looking at around 90-100W for the GPU to work with.
At 1440p with the RT Ultra preset, we got 28.70 FPS, and at 1080p, we got 59.34 FPS. Using High settings at 1080p without RT on a DGX Spark yields over 100 FPS, while AMD's Ryzen AI MAX+ is only capable of around 80-90 FPS.
But then there are some nice additions such as the same DLSS MFG, DLSS 4.5 Transformer, and DLSS 4.5 Ray Reconstruction support as the RTX 50 series family. With these features enabled, we got up to 95.15 FPS at 1440p using the RT Ultra preset, and 140 FPS at 1080p.
Once again, this is just a taste of things to come with the RTX Spark PCs, which will offer better optimizations and support on the Windows OS.
AI Benchmarks - Local, AI Agents, & Multi-Cluster Performance
We have been testing various LLMs across various devices. NVIDIA's DGX Spark is our first look at a dedicated AI box, and we wanted to see if its AI performance was suitable enough for most devs in this segment.
While there are plenty of AI LLMs and various inference engines to test, we wanted to see how the performance stacked up across the most widely used models. For this purpose, we went to see the models that are widely popular but also relatively new on Hugging Face, and ran them in llama.cpp. NVIDIA provides playbooks to set up all sorts of inference engines such as llama.cpp, vLLM, LM Studio, and more.
Based on our previous tests, we found llama.cpp to have the least amount of overhead when running LLMs. With that said, there are benefits to using a certain inference engine, and LLM usage will vary based on the type of output you require.
The NVIDIA DGX Spark delivered solid figures across various weights. The single-node tests were done on models spanning from 4B up to 120B (GPT-OSS). DGX Spark is really speedy in terms of token generation, but it's also a beast at prompt processing, given its tiny size.
We also tested a few MoE (Mixture of Experts) models, which are essentially LLMs with a massive knowledge capacity of a huge model but with the fast processing speed of a much smaller model. Our tests featured both single-node and multi-node (2 x DGX Spark) benchmarks. Here, the latest DeepSeek V4 Flash with NVFP4 (transformers loaded) offers us 21.3 TPS on a single node and 59.13 TPS on the dual-clustered node. That's more than 2x speed thanks to the 256 GB of available VRAM for this 284 billion parameter model.
In MiniMax-M2.5 (4-bit), we were unable to fit it inside a single Spark, but the dual Spark cluster offered us 40.12 TPS of generation speed. Other models such as NVIDIA's open-source Nemotron 3 Super with 120 billion parameters also ran decently on the clustered setup.
DGX Spark Token Generation Speed In MoE Models
Now it is very important to have the right software and support backing up these models. That's where tuning and optimization come in. NVIDIA has been fine-tuning LLM performance along with the Agent capabilities of its DGX/RTX platforms . The company recently rolled out the latest updates, which will be available this month, offering even faster performance on leading inference platforms and giving users 1-click installation options for Agentic AI platforms such as OpenClaw and more.
We also tried a little bit of GenAI using various models through ComfyUI such as Flux.2 and SDXL Turbo which were easy to setup since NVIDIA also provides a full guide on setting up ComfyUI locally. The image processing speeds were good, producing 6-7 (1024x1024) images within a minute.
In terms of Thermals, the NVIDIA DGX Spark does get a bit toasty, but you will hardly ever hear its fans running. The exhaust heat is noticeable, but only when you're really pushing the device to its full potential. We recorded idle temperatures of 48C and peak temperatures hitting 81C on our unit.
As for power, while the DGX Spark is rated to go up to 140W, we hardly ever saw it pulling over 100 Watts of power even in Prefill Heavy scenarios. The average power for a single Spark is close to 80W, and when paired, the second system usually hovers at 5-10W lower than the main Spark.
The NVIDIA DGX Spark did not just arrive as another compact workstation. It arrived as the machine that defined a category.
What we have here is the original local AI box: a quiet, wall-outlet-powered system that treats 70-billion-parameter fine-tuning and 200-billion-parameter inference as everyday work rather than a data-center reservation.
The GB10 itself is the real story. Two tightly coupled dielets, 128 GB of coherent unified memory, NVLink-C2C, fifth-generation Tensor Cores, and a ConnectX-7 fabric that lets two units become a 256 GB cluster in minutes. That combination is why a 284-billion-parameter DeepSeek V4 Flash jumps from 21 TPS on one Spark to 59 TPS on two, and why models that simply will not fit on a single node suddenly become usable.
The NVIDIA Guides and various playbooks came in very handy, but I often found them to be a little bit outdated. Most weren't a simple copy/paste job as they were said to be, and I had to go through various repos and forums to make sure the model I was running was the best fit for the Spark.
The software stack: DGX OS, the Dashboard, NVIDIA Sync, and the growing library of one-click playbooks turns what could have been a Linux-only science project into something a developer can actually live with after the first-boot update.
While the DGX Spark is not designed around gaming, the hardware hints at what the incoming RTX Spark platforms will deliver. Cyberpunk 2077 at 1440p with full ray tracing and DLSS 4 Multi Frame Generation reaching 95 FPS on a sub-100W envelope is a respectable preview.
The main event, though, remains local agents, large-context RAG, & multi-node experimentation without leaving the desk. Thermals stay civilized, fans stay quiet, and real-world power draw rarely exceeds 80–100 W. Those numbers matter. They mean you can run a pair of Sparks overnight without thinking about the electricity bill or the noise.
A year later, the DGX Spark still feels like the reference design everyone else is measuring against. It is not the cheapest way to run local models, costing a wallet-breaking $4699 right now for a single piece, but it is the most coherent, most scalable, and most future-proof small-form-factor AI workstation currently available. When the RTX Spark variants land next month, they will inherit the same silicon with better clocks and a more familiar OS. Until then, the original Spark remains the machine that proved a personal AI supercomputer could actually sit on a desk and work.
You can find additional information about our hardware review process and ethics policy here.

### Article 91 · 2026-09-10 · techcrunch.com
Jensen Huang explains why Nvidia will grow an astounding 70% next year

Founder, CEO, and tireless Nvidia hype man Jensen Huang told attendees at the Goldman Sachs Communacopia + Technology conference on Thursday why his company’s AI domination — and revenues — will continue its record-breaking growth streak through the end of next year.
He can see the future.
There’s been endless hand-wringing over whether Nvidia’s party will end as it faces increasing competition for GPUs and AI chips from all directions: the hyperscalers (Amazon, Microsoft, and Google, each building their own) and the AI labs (Anthropic and OpenAI, which are building their own), as well as from newly public competitor Cerebras and startups such as Etched .
“Most people think Nvidia builds a chip. I mean, you need airplanes to ship what we build,” Huang said, adding that the company continues to battle a perception from its early days. Nvidia invented the GPU, which back then were largely sold to consumers to improve PC gaming. “One GPU now is not $399. It’s $8.5 million dollars. That’s one GPU, all connected with NVLink, 2 million parts, right? 250,000 kilowatts. That’s a GPU, and we ship thousands of them.”
He added that orders for just one product, a computer system that combines 36 Grace CPUs with 72 Blackwell GPUs, is currently experiencing 27% month-to-month sales growth.
Huang didn’t limit his bullish view to current sales though. He took the opportunity to reiterate Nvidia’s revenue outlook for next year — guidance the company provided last month when it reported yet another record-breaking revenue quarter. That’s when he first said revenue could grow by 70% next year.
“I think we could grow 70% year over year. We’re confident about that,” Huang said again on Thursday. Analysts expect the company to end its current fiscal year at about $400 billion in revenue. So 70% growth would mean around $680 billion next year.
Huang explained why he’s confident: His company is so embedded in every area of AI that he believes he can see the future.
“Nvidia runs every model. Every single lab can use us,” the CEO said, mentioning that this includes models from Anthropic, OpenAI, and Google, as well as open-weight offerings. “We are a foundational platform of the AI ecosystem, foundational platform of the AI industry.”
Nvidia’s fingers extend all the way from its suppliers, such as memory chip makers, to data center projects and startups.
“We’re tracking every single gigawatt of land, power, shell around the world. Literally everything on the planet,” he said. (“Shell” refers to the shell of a data center building before it is outfitted with computers).
“I mean, just think about all my partners. How many neoclouds are reporting back to us? How many OEMs are reporting back to us? How many clouds are reporting back to us? How many AI-native companies are reporting back to us? We’re working with everybody, and so we kind of know where everything is,” he said.
That comment led to inevitable questions about Nvidia’s so-called circular deals, in which it invests in companies that turn around and buy its wares. Such schemes famously contributed to the downfall of a previous generation of internet build-out suppliers like Lucent Technologies .
Huang had a simple, albeit cheeky, response. “Well, it’s not circular because we put a little bit of money in, and a lot of money comes back.” He went on to joke, “I look at the spreadsheet, we put in $1 and $100 comes back in. Is that circular? If that is, let’s do more of that.”
Quips aside, he insisted that before any of these companies gets an investment, Nvidia makes sure it has real contracts generating revenue from customers. All told, he said he’s seen $100 billion worth of such contracts, “I’m not taking any risks. … I need a sure thing.”
Time will tell whether Nvidia’s stronghold on AI can really persist long term. If there’s one golden rule of the tech industry, it’s that all big things get disrupted. Right now, even Huang admits that much of AI’s growth is coming from AI-native startups that are raising vast sums and spending most of that cash on their own AI use. As the AI industry matures, expect companies to become more efficient in how they use infrastructure and tokens.
But for now, Nvidia has its finger in every pie and sees another year of plenty in its future.

### Article 92 · 2026-09-10 · thenextweb.com
Nvidia and Palantir are selling a sovereign AI stack, starting with Nvidia’s own supply chain

Nvidia and Palantir have announced today a joint product for running AI over corporate supply chains without handing the underlying data to anyone else, and the first customer is Nvidia, which is using it on its own.
It pairs Palantir’s Foundry, its Artificial Intelligence Platform and its Ontology with Nvidia’s open Nemotron models and cuOpt optimisation software, packaged as something Palantir calls its Sovereign AI Operating System reference architecture.
It can be deployed on-premises, in a cloud, or in a colocation facility, with Dell, Cisco, Rackspace and Nebius named as partners.
The use case is real, and the number that explains it is 1.3 million: the count of parts in a single Nvidia Vera Rubin rack. Tracking that many components across suppliers, and working out which constraint is the one actually holding up a build, is a genuine optimisation problem rather than a slide.
“Supply chains are the operating system of the physical economy, and AI factories are among the most complex systems ever built,” said Jensen Huang, founder and CEO of NVIDIA.
The word to examine is sovereign. In this product it means the customer keeps control and ownership of its proprietary data, which is a meaningful commitment and is nothing.
It does not mean the customer controls the ontology that structures that data, the models that reason over it, the optimisation software, the accelerators underneath, or the two American companies that supply all four. Sovereignty over the contents, dependency on the machinery.
Europe has spent the week arguing about precisely this distinction, mostly without naming it. Nvidia signed eight Australian data centre operators to build local capacity described as sovereign AI, where the racks are Australian, and the stack is American.
The Commission proposed procurement rules with a European preference framework whose scope for software is undecided, having already produced Made in EU rules that reached concrete and aluminium and left cloud hosting alone.
And Germany answered the question in the sharpest available form. Berlin ruled out Palantir for military decision support in April, and is now evaluating 30 alternatives, mostly from German suppliers, with a prototype due in 2027.
France’s intelligence service is dropping Palantir for a homegrown rival. Paris and Berlin have pledged to build a European competitor, and German officials promptly worried that would be another dependency .
A company launching a product with sovereign in the name, in the same month two European governments are unpicking their dependence on it, has read the market correctly.
Whether the product answers the objection is a different question. European resistance to Palantir has rarely been about where the data sits.
It has been about who holds the analytical layer, what happens to access in a diplomatic dispute, and whether a supplier that is deeply embedded with the US government is the right place to run a national security function. A deployment model that puts the servers in your building does not change any of those.
Alex Karp’s own description is worth quoting for connoisseurs.
“NVIDIA has arguably the most valuable, intricate and complex supply chain in the world. Our sovereign stack, powered by Nemotron models and Ontology, is delivering capabilities that exceed the frontier while providing alpha protection qualities unavailable otherwise,” said Alex Karp, cofounder and CEO of Palantir Technologies.
“We are very proud of our partnership and its cornerstone role in the sovereign AI revolution.”
For a European manufacturer, the practical question is narrower and more useful than the geopolitics. This is a serious tool for a serious problem, offered by the company that has the hardest version of that problem and is using it internally.
That is a stronger reference than most enterprise software ever gets. It is also a deeper commitment than buying a licence, because an ontology is not a thing you swap out later.

### Article 93 · 2026-09-10 · fool.com
Nvidia's Jensen Huang Claims AGI Has Arrived. Here's How to Invest.

The term artificial general intelligence, or AGI, has been around for decades. It was first used in 1997 by physicist Mark Avrum Gubrud to describe fully automated military production. Researcher Ben Goertzel popularized the term in the early 2000s, giving it its current meaning as a description for AI technology that can self-initiate a broad range of tasks, similar to how humans operate.
Messaging surrounding AGI can be confusing and, at times, misleading. Last year, for example, Sam Altman, the CEO of OpenAI , told reporters that AGI is no longer a very useful term, stressing that the language is used more for marketing than serious technical discussion. A year later, OpenAI released its GPT-6 Astra model, boasting that humanity has now "entered the AGI era."
Adding to the fray, Nvidia ( NVDA +2.55% ) CEO Jensen Huang congratulated OpenAI on its milestone. With the model's release, Huang wrote explicitly that "AGI has arrived." But when you dig deeper, Huang's comments seem to simply indicate that GPT-6 Astra might kick-start the AGI revolution, not that the model is AGI in and of itself. "When we look back, people will think it's about this time and about this model," OpenAI President Greg Brockman said.
Has AGI, in fact, arrived? Here's what market experts have to say.
Artificial general intelligence should create a new capex wave
Wall Street analysts are similarly unconvinced that GPT-6 Astra represents a true AGI breakthrough, though many agree that the model release could officially put AI companies on track to realize AGI down the road.
Rich Privorotsky, an analyst at Goldman Sachs , stressed that GPT-6 "stands out" because it can reshape the demand curve by delivering significantly more intelligence. More intelligence, not lower pricing, is what Privorotsky believes will kick-start the AGI era.
"Price decline is one thing, but a real breakthrough in intelligence will once again change the demand curve," Privorotsky explains. "It will force all other labs to catch up, keep the spending cycle energized, and reactivate the belief that 'there is something better worth building.'"
This analysis is very bullish for AI infrastructure providers like Nvidia, regardless of whether GPT-6 Astra is true AGI. Privorotsky is essentially saying that OpenAI's breakthrough will initiate another capex spending cycle, benefiting suppliers to the industry, especially GPU manufacturers .
An August report from Goldman Sachs suggested that global AI investment will exceed $1 trillion in 2026. Projections for 2027 call for 30% to 50% year-over-year growth, with global AI spending perhaps reaching $1.5 trillion. The bank foresees more than half of that spending being dedicated solely to GPUs.
Whether GPT-6 Astra represents true AGI or not is up for debate. The model clearly beats humans on many difficult intellectual benchmarks. The model has the potential to replace a large amount of human work, at least on paper. But whether the model can actually handle a broad array of highly intellectual human tasks autonomously remains to be seen. More scaling and real-world proof points are necessary.
The AGI debate for GPT-6 Astra, however, is largely besides the point from an investor perspective. The investor takeaway here is simple: Rapid model advances continually renew competition, lighting a fire under other AI developers to advance their models as quickly as possible. That requires increased capex, a direct benefit to critical suppliers like Nvidia.
By Ryan Vanzo – Sep 10, 2026 at 8:45PM EST

### Article 94 · 2026-09-10 · fool.com
Not Nvidia. Not Broadcom. But This Semiconductor Stock Is Set to Grow Faster Than Any Other Major AI Chipmaker Through the End of the Decade.

Nvidia ( NVDA +2.55% ) and Broadcom ( AVGO +2.83% ) reported very positive results in their most recent earnings statements. Not only are they seeing very strong demand for their artificial intelligence (AI) chips, but they both expect that growth to continue for the foreseeable future.
Indeed, demand for semiconductors appears to have a very long runway ahead, as a growing share of hyperscalers' budgets shifts toward buying more chips to outfit new data centers and replace old servers.
And while both of the biggest AI chipmakers have the potential to grow very quickly through the end of the decade, a smaller silicon slinger could grow even faster as its revenue accelerates during the next few years.
As mentioned, both Nvidia and Broadcom expect to keep producing very strong revenue growth.
Nvidia more than doubled its top line last quarter, producing a whopping $96 billion in revenue. Chief Financial Officer Colette Kress said she expects the company's annual revenue to increase by 70% next year, noting that the outlook is the result of limited chip supply. Its biggest bottleneck is memory, for which it made a significant up-front purchase commitment last quarter to facilitate supply expansion.
Likewise, Broadcom reported revenue growth of 86% last quarter, and management expects that growth to accelerate to 93% next quarter. Its AI chips are driving the gains, with AI-related revenue up 221% last quarter. Growing demand for custom silicon solutions instead of Nvidia graphics processing units (GPUs) is helping Broadcom's XPU processor business. Of course, Nvidia doesn't seem to be suffering too much.
But another custom artificial intelligence chipmaker could end up growing faster during the next few years. Marvell Technology ( MRVL +4.36% ) expects a significant ramp-up in its XPU business along with related AI chips. While management is currently forecasting revenue growth of 45% for the current year, it expects that to accelerate to 50% next year and grow even faster in fiscal 2029 (which falls primarily in the 2028 calendar year).
With just $12 billion in expected revenue for fiscal 2027, the company is significantly smaller than Nvidia ($411 billion in expected revenue) or Broadcom ($106 billion in expected revenue). That means a few new deals with big tech companies can have a huge impact on its growth. And it's showing excellent progress in doing just that. As a result, I expect it to produce better overall average revenue growth through the end of the decade than either Broadcom or Nvidia.
During Marvell's second-quarter earnings call, Chief Executive Officer Matt Murphy told analysts the custom AI chip business will accelerate in the back half of the year. "We remain confident that this business will more than double year over year in fiscal 2028 and accelerate significantly in fiscal 2029," he added.
The primary near-term driver is likely its deal with Microsoft ( MSFT +1.22% ) , which includes designing the company's Maia line of chips. Microsoft is reportedly planning a big step up with Maia 300, using it for more of its internal AI workload. Microsoft is reportedly looking to fill an order of 300,000 chips in 2027.
Alphabet ( GOOG -0.77% ) ( GOOGL -0.61% ) presents another big potential customer for Marvell. Marvell signed a deal with Google to expand its existing partnership to include a range of products, including "AI inference accelerators, storage controllers, network interface controllers, memory interface controllers, and near-memory compute." The deal also provides warrants to Alphabet to purchase shares of Marvell based on revenue targets totaling up to $120 billion through fiscal 2033.
The company is in active discussions with all the hyperscalers for custom chips, and what it calls XPU attach, chips that help make custom silicon chips even more efficient at scale (network interfaces, scale-up fabrics, and co-processors). With the expansive Alphabet deal and a growing relationship with Microsoft, it could find more of its chips in big data centers over the next few years.
The stock trades at a premium to both Nvidia and Broadcom. That reflects the expectations for revenue to accelerate and earnings to follow suit. Analysts on average expect earnings per share (EPS) to climb from $4.20 this year to $6.72 next year to $10.28 in 2029. The forward price-to-earnings (P/E) ratio of 53 for the stock reflects those expectations for accelerating earnings growth. And that EPS acceleration can continue through the end of the decade, making it an attractive opportunity for investors.
Not Nvidia. Not Broadcom. But This Semiconductor Stock Is Set to Grow Faster Than Any Other Major AI Chipmaker Through the End of the Decade.
By Adam Levy – Sep 10, 2026 at 4:30AM EST

### Article 95 · 2026-09-10 · fool.com
Nvidia Is One of the Most Profitable Businesses in the World. Here's Why the Stock Is Worth $311 a Share Right Now -- 39% More Than Its Share Price.

Nvidia Is One of the Most Profitable Businesses in the World. Here's Why the Stock Is Worth $311 a Share Right Now -- 39% More Than Its Share Price.
What are the most profitable companies in the world? Well, it all depends on how you define "profitable." Google's parent, Alphabet , rakes in the most total profits globally, at about $195.6 billion over the past 12 months. For profits per employee, per one report, the Federal National Mortgage Association , known as Fannie Mae, is on top, at $2.07 million per worker. Then there's net profit margin -- the percentage of revenue that a company keeps as profit. On that count, Nvidia (NASDAQ: NVDA) has an astonishing profit margin of 64%.
Nvidia is easily one of the most profitable companies in the world. Let me explain why its stock may be worth around $311 per share -- some 39% higher than its share price at this writing.
Once known for its gaming chips, Nvidia has pivoted profitably, becoming the largest provider of chips for data centers used in artificial intelligence (AI) -- while still making chips to power games and computers. It's also a software company, focused on robotics and AI, and it offers networking tools, as well. And it's known for data center platforms such as Blackwell, Hopper, and Rubin. (Those are the names of famous mathematicians and scientists -- David Blackwell, Grace Hopper, and Vera Rubin.)
It's also helping smaller companies afford AI infrastructure via a new AI compute infrastructure financing platform. And it's broadening the scope of its offerings, such as by adding custom AI processors and partnering with an optical interconnect technology provider. Most recently, it agreed to acquire Hugging Face, home to a key AI platform reportedly used by more than 18 million developers and 200,000 companies.
In a nutshell, Nvidia is increasingly involved in all kinds of fast-growing -- and highly profitable -- technologies.
It's therefore not surprising that the stock has rocketed upward, averaging annual gains of 65% over the past decade. With all that, you might expect the stock to be overvalued. But that doesn't seem to be the case.
Its forward-looking price-to-earnings (P/E) ratio of 25.1 for example, is well below the five-year average of 34.4, and its price-to-cash flow ratio of 31.4 is well below the five-year average of 50.8. This rapidly growing company appears undervalued.
How undervalued is hard to say, because valuations are always dependent on estimates and assumptions -- of future growth rates, future revenue amounts, and so on. But let's take a stab at it.
Consider the forward P/E of 25.1, which is lower than the five-year average. If we assume that the average of 34.4 is a more reasonable valuation, then the corresponding stock price would be about $311 per share. In other words, given the expected earnings over the coming year, if Nvidia's stock were trading at a forward P/E of 34.4, the share price would be $311.
You can do similar calculations with other measures, such as the price-to-sales ratio or price-to- cash flow ratio, and you'll end up with similarly higher estimated prices for Nvidia. We needn't focus too closely on any of them and can just take away that the shares seem undervalued, making the thought of investing in Nvidia even more appealing. Those buying now are likely to profit along with the company.

### Article 96 · 2026-09-10 · fool.com
Advanced Micro Devices vs. Nvidia: Which Semiconductor Stock Is a Better Buy in 2026?

As the artificial intelligence revolution matures, investors are weighing the long-term potential of Advanced Micro Devices ( AMD +3.09% ) against the market dominance of Nvidia ( NVDA +2.55% ) to see which chipmaker offers more value.
AMD operates as a flexible challenger, providing essential chips for data centers and gaming consoles while expanding its presence in the AI accelerator market. Nvidia remains the industry titan, leveraging a comprehensive platform of hardware and software to dominate the accelerated computing landscape. Both companies are critical to the modern digital economy, but they offer different risk profiles.
Advanced Micro Devices designs high-performance computing products ranging from data center processors to gaming consoles. Among semiconductor stocks , its MI450 GPU deal with OpenAI and chips for Microsoft ( MSFT +1.22% ) highlight its growing AI presence. Relying on a small number of large customers for a majority of sales adds a layer of risk to the business.
In the fiscal year ended Dec. 27, 2025, according to its latest annual report, revenue reached nearly $34.6 billion. This represented growth of approximately 34.3% compared with the prior fiscal year. Net income was roughly $4.3 billion, yielding a net margin of close to 12.5%, a significant improvement over the prior year's net margin of about 6.4%.
As of its December 2025 balance sheet, the debt-to-equity ratio is approximately 0.1x, indicating the company maintains a conservative level of borrowing. The current ratio is roughly 2.9x, while free cash flow, which is cash from operations minus capital expenditures, reached nearly $5.5 billion. Note that stock-based compensation represented roughly 21.2% of operating cash flow, which inflates reported cash generation since SBC is a non-cash expense added back in the cash flow statement.
Nvidia provides the accelerated computing platforms that underpin the current boom in artificial intelligence. Its data center infrastructure and software are used by major cloud service providers and AI model developers to host advanced applications. The company also maintains a strong presence in the automotive industry through its DRIVE platform, which supports hundreds of partners including various OEMs.
According to its latest annual report, in the fiscal year ended Jan. 25, 2026, revenue reached approximately $215.9 billion. This represents a 65.5% increase year over year, driven by intense demand for AI chips. Net income for the period was roughly $120.1 billion, resulting in a net margin of close to 55.6%.
As of the January 2026 balance sheet, Nvidia reported a debt-to-equity ratio of nearly 0.1x. The current ratio is roughly 3.9x, while free cash flow for the fiscal year ended Jan. 25, 2026, was approximately $96.7 billion. This massive cash generation provides the company with significant flexibility to reinvest in research or return capital to shareholders.
AMD faces intense competition from Intel ( INTC +5.74% ) and Nvidia, including a recent partnership between those two rivals that could pressure its market share. The company relies heavily on TSMC for manufacturing, while geopolitical tensions and U.S. export controls on advanced chips to China have led to inventory charges. Ongoing litigation regarding securities laws also poses a potential financial and regulatory hurdle.
Nvidia is also vulnerable to tightening U.S. export controls, which have already restricted its data center sales in China. Competition is evolving as major cloud customers like Amazon ( AMZN +0.56% ) , Microsoft, and Alphabet ( GOOGL -0.61% ) develop their own AI chips in-house. Additionally, antitrust regulators in several jurisdictions are scrutinizing its sales practices and market dominance.
Nvidia appears significantly cheaper than its rival based on its Forward P/E , which uses future earnings estimates, though its P/S ratio remains slightly higher.
I'd go with Nvidia, and it's not a close call. Nvidia just posted one of the most extraordinary quarters in the history of the semiconductor industry. Revenue more than doubled year over year, data center demand is accelerating rather than plateauing, and the company guided for another massive jump in the quarter ahead. Jensen Huang's observation that AI has reached its inflection point (that its tokens are now productive and profitable) captures why the demand behind these numbers is not a temporary surge.
AMD deserves credit for its own impressive run. Data center sales more than doubled year over year, an Anthropic partnership adds long-term credibility, and AMD is cementing its position as the primary alternative to Nvidia in the AI chip market. For a long-term investor who wants AI chip exposure at a lower price point, AMD is a reasonable choice.
But "the primary alternative to Nvidia" is a very different position than being Nvidia. The gap in scale, ecosystem depth, and customer lock-in between these two companies is enormous and widening. For a long-term investor, owning the company that the entire AI industry is built around is a stronger foundation than owning its closest competitor.
Sara Appino is a contributing writer at The Motley Fool. Previously she held roles at McGraw-Hill Education, Sourcebooks, and The Field Museum of Natural History. A graduate of the University of Chicago and Northwestern University’s Medill School of Journalism, Sara also managed a surf and yoga retreat in Costa Rica for nearly a decade and helped launch a nonprofit English language program in her community there.
By Sara Appino – Updated Sep 10, 2026 at 2:31PM EST
Advanced Micro Devices has expanded its footprint in AI infrastructure through strategic partnerships and new GPU deployments.
Nvidia maintains exceptional dominance in the data center market with net margins exceeding 50% and massive cash generation.

### Article 97 · 2026-09-10 · insidermonkey.com
Heavy Investment Sustains NVIDIA’s (NVDA) AI Leadership

Barometer Capital Management , an independent asset and wealth management firm, released its second-quarter 2026 investor letter. The letter can be downloaded here . The second quarter experienced significant volatility driven by macro and headline risks. Concurrently, an upcoming Federal Reserve leadership transition contributed to policy uncertainty, and rising inflation concerns re-emerged, resulting in choppy, headline-driven price movements throughout the period. During the quarter, the firm adopted defensive postures in response to rising risks; however, the market showed resilience, absorbing shocks without following a clear downward trend. Although volatility challenged strategies aimed at capturing durable trends, emerging leadership in specific sectors provided hope. The Barometer Tactical Equity Pool reflected strength in Industrials, IT, and Financials, encouraging a patient approach aligned with robust areas. Industrials and Financials were the leading contributors to the Barometer Tactical Balanced Pool. The Barometer Global Macro Pool struggled in a challenging, non-trending environment, where gains in international equities were outweighed by losses in precious metals and the Pool's short position. Despite ongoing risks such as inflation and geopolitical tensions, the outlook is cautiously optimistic, with readiness to capitalize on clearer trends as they develop. Also, check the fund's top five holdings to see its best picks in 2026.
In its second-quarter 2026 investor letter, Barometer Capital Management highlighted NVIDIA Corporation (NASDAQ: NVDA ) as a top contributor. NVIDIA Corporation (NASDAQ:NVDA) is a leading data center-scale AI infrastructure company operating through Compute & Networking and Graphics segments. On September 09, 2026, NVIDIA Corporation (NASDAQ:NVDA) closed at $223.67 per share. Over the past month, NVIDIA Corporation (NASDAQ:NVDA) declined 0.83%, but its shares are up 26.10% over the past year. NVIDIA Corporation (NASDAQ:NVDA) has a market capitalization of $5.40 trillion, and its stock has traded within a 52-week range of $164.27 to $236.54.
Barometer Capital Management stated the following regarding NVIDIA Corporation (NASDAQ:NVDA) in its Q2 2026 investor letter:
"Information Technology contributed, driven by a new position in Lam Research (LRCX) and an addition to NVIDIA Corporation (NASDAQ:NVDA) as semiconductors reasserted leadership. NVIDIA, for its part, remained the dominant compute platform for artificial intelligence and benefited from continued heavy investment by hyperscalers and enterprises building out data center capacity. Between them, the two positions captured both the chips at the center of the AI build-out and the equipment that makes them."
In another article , we discussed NVIDIA Corporation (NASDAQ:NVDA) and highlighted its $20 billion Groq bet. In addition, please check out our  hedge fund investor letters Q2 2026  page for more investor letters from hedge funds and other leading investors.

### Article 98 · 2026-09-10 · fool.com
Not Nvidia, Not Palantir. This Might Be September's Most Important AI Infrastructure Stock.

When it comes to artificial intelligence (AI), two names seem to get more airtime than their peers: Nvidia ( NVDA +2.55% ) and Palantir Technologies ( PLTR +1.32% ) . Over the current earnings season, investors have already gotten thorough downloads on how Nvidia and Palantir are performing. Spoiler alert: They both look unstoppable.
However, the company I think sits at the tightest choke-point in the entire AI infrastructure build-out is Micron Technology ( MU +4.20% ) . The memory shortage has become the bottleneck that tech sector CEOs are talking about out loud . While Micron won't report its results till the end of the month, Nvidia and Palantir have already signaled the cycle is running in its favor.
Nvidia and Palantir confirmed the AI build-out continues
Nvidia's latest earnings report was the kind of print that resets conversations. Total revenue was $96.2 billion, more than double what it took in during the year-ago quarter. Data center sales reached $89 billion, up 117% year over year. Naturally, hyperscalers still matter a lot to Nvidia's data center segment. Big tech customers comprised $48.7 billion of the company's data center sales. The faster-growing slice, however, was its " ACIE group" -- AI clouds, industrial customers, and enterprises. This market segment generated $40.3 billion in revenue, up 138% year over year and 25% from the prior quarter.
Palantir is achieving in software what Nvidia is in hardware. During the second quarter, its revenue surged 93% year over year to $1.9 billion. Sales from the U.S. commercial segment jumped 149% year over year to $764 million. Given this momentum, management raised full-year revenue guidance to a little over $8.2 billion, implying 82% growth.
Palantir's Artificial Intelligence Platform (AIP) is not a pilot project anymore. Fortune 500 companies are embedding Palantir's platforms -- Foundry, Gotham, and Apollo -- into their daily operations, and the company's bookings suggest its sales acceleration will continue.
These two reports were not isolated. Nvidia and Palantir are proving that both the hardware layer and the software layer of the AI revolution are still expanding at paces that most on Wall Street would have called unsustainable even just two years ago.
Upstream dollars are now flowing downstream
The growth displayed by Nvidia and Palantir is excellent news for Micron because the AI stack is vertical. You can't sell more data center GPUs or more enterprise software platforms without putting a lot more high bandwidth memory (HBM) into the equation. Nvidia itself has made this abundantly clear. Last quarter, the company boosted its supply and capacity commitments through its fiscal 2032 by $160 billion to a total of $279 billion, with management saying the bulk of those commitments are for memory purchases.
Hyperscalers and AI-cloud operators continue to place enormous orders for Nvidia's GPUs. Software companies like Palantir then sell platforms and services that make these GPUs useful within production environments. The subtle beneficiary here is Micron, because every extra new accelerator installed and every AI deployment needs incremental stacks of HBM.
Micron is one of only three companies that can deliver these key types of memory at scale. DRAM pricing has soared because AI data centers are gobbling up a huge portion of available production. This shows how upstream success does not stay upstream. Downstream in the AI value chain, it manifests as tighter supply and better pricing for component makers like Micron.
The market could recalibrate its view of Micron on Sept. 30
Micron reports its fiscal 2026 fourth-quarter results after the closing bell on Sept. 30. The consensus estimates among Wall Street analysts are that it will report $50.8 billion in revenue and about $31.28 in earnings per share (EPS). The reason Micron could actually beat these forecasts is that pricing and product mix keep moving in its favor. Next-generation HBM4 is ramping up for the next wave of Nvidia systems, while conventional DRAM supply remains tight.
To me, Micron's valuation story is a curiosity. On a trailing-12-month basis, Micron stock may look expensive because its earnings explosion is still catching up to the stock price. On a forward price-to-earnings (P/E) basis, however, Micron is trading more like a cyclical industrial stock as opposed to a company positioned in the middle of a multiyear infrastructure boom.
Nvidia and Palantir are already priced like true AI winners -- deservedly so. On a forward earnings basis, Micron remains priced like a commoditized memory producer that investors expect to eventually repeat its familiar boom-and-bust cycle. Yet memory is now a scarce resource, and every GPU produced and every enterprise AI system deployed needs it to function. If Micron merely delivers what Wall Street expects and then confirms that demand remains robust, its valuation multiple has significant room to expand alongside its still-rising earnings. That is why, in this particular month, Micron looks like the most important AI infrastructure stock.
By Adam Spatacco – Sep 10, 2026 at 2:04PM EST

### Article 99 · 2026-09-10 · gurufocus.com
Nvidia Slides 2.5% as $2 Billion Chip Startup Adopts NVLink Fusion

Nvidia Corporation ( NASDAQ:NVDA ), the AI-accelerator and data-center powerhouse, slid 2.5% to $217.97 Thursday morning even as $2 billion chip startup d-Matrix joined its NVLink Fusion ecosystem. The startup plans to connect its Raptor inference processors directly to Nvidia's rack-scale infrastructure, widening the reach of Nvidia's technology beyond its own chips.
D-Matrix aims to complete Raptor's final design in 2026 before compatible racks arrive in 2027. The processors are built for speed-sensitive applications including coding assistants, chatbots and voice agents. Investors received no details on financial terms, purchase commitments or expected shipment volumes, leaving the immediate revenue impact unclear.
NVLink Fusion allows custom processors and accelerators to operate alongside Nvidia's GPUs, networking, memory and rack technology. Rival chips may enter the rack, but Nvidia still wants to own the system connecting everything together. That strategy looks crucial when data centers generate roughly 92.5% of the company's latest $96.2 billion quarterly revenue . The picture reinforces the market's broader confidence: Nvidia's GF Score of 96 out of 100 is powered by standout profitability, growth, financial strength and momentum, while valuation remains its clearest weak spot.

### Article 100 · 2026-09-10 · tradingview.com
Michael Burry Dumps Nvidia and Palantir Put Options in Fresh Risk Warning

Michael Burry (Trades, Portfolio) is reducing exposure across his portfolio, including his bearish options tied to Nvidia (NVDA) and Palantir PLTR , as he keeps more cash available amid changing market conditions.
Burry said he reduced risk during September and closed out December 2026 put options on both companies rather than extending those trades. He said he would prefer to hold some cash while assessing the market through the fall.
His largest long holdings by position size remain Lululemon LULU , Molina Healthcare (MOH) and MercadoLibre (MELI), although he has reduced the size of his long positions. Burry said the ranking of his holdings has otherwise stayed intact.
On the short side, Oracle ORCL , Palantir and Nebius NBIS remain his three biggest positions, followed by Nvidia and the iShares Semiconductor ETF (SOXX).
Burry also said he is monitoring weakness in the Dollar Spot Index and expects to discuss currencies in a future post. Retail sentiment for Palantir remained bearish, while Nvidia sentiment shifted from neutral to bearish on Stocktwits.

### Article 101 · 2026-09-10 · gurufocus.com
Nvidia Stock Falls. DOJ Probes $20 Billion Groq Deal

Nvidia ( NASDAQ:NVDA ) shares dipped about 1% early Thursday as a U.S. Justice Department review examined whether its $20 billion arrangement with AI chip startup Groq was designed to limit antitrust scrutiny, Bloomberg reported, citing people familiar with the matter.
The inquiry focuses on a transaction unveiled in December that gave Nvidia access to Groq's technology while allowing the startup to continue operating separately. Groq Chief Executive Jonathan Ross and Chief Operating Officer Sunny Madra subsequently moved to Nvidia.
The structure has attracted attention from U.S. lawmakers, who have questioned whether the arrangement amounts to an acquisition that could reduce competition in the artificial-intelligence chip industry.
The Justice Department began examining the transaction earlier this year as part of a broader antitrust review, according to the report. The licensing arrangement was also previously reported by The New York Times, and the investigation could conclude without any enforcement action.
Nvidia has defended the transaction, saying the agreement allows it to provide Groq technology across its ecosystem while leaving Groq's cloud operation independently funded and operating.

### Article 102 · 2026-09-10 · gurufocus.com
Michael Burry Makes Surprising Nvidia, Palantir Move

Michael Burry is scaling back his market exposure and raising cash ahead of what the Big Short investor expects to be an eventful period for stocks this fall.
Burry said Wednesday that he reduced every position in his portfolio during September. He also closed put options expiring in December 2026 on Nvidia ( NASDAQ:NVDA ) and Palantir Technologies ( NASDAQ:PLTR ), choosing not to replace them with contracts carrying later expiration dates.
Put options generally increase in value when their underlying securities decline. Exiting those contracts reduces the amount of capital Burry has directly committed to betting against the two prominent artificial-intelligence stocks.
The move does not mean Burry has abandoned his broader bearish view of the AI trade. Palantir remains his second-largest short position, while Nvidia ranks fourth, based on the position order he disclosed.
Oracle is still Burry's largest short holding, followed by Palantir and Nebius Group. Nvidia and the iShares Semiconductor ETF complete his five biggest bearish positions.
Burry's long portfolio also became smaller, although its ranking remained unchanged. Lululemon Athletica, Molina Healthcare and MercadoLibre continue to represent his three largest bullish positions.
The investor said the reductions left him with additional cash that he is content to hold while waiting for greater clarity. He also predicted that markets would become particularly interesting during the fall, suggesting that the retreat reflects caution rather than a decisive shift toward optimism.
Burry is separately monitoring renewed weakness in the Dollar Spot Index and said he plans to examine the currency market in a future post.
Retail traders remain cautious toward his two highest-profile short targets. Stocktwits sentiment for Palantir stayed bearish over the previous day, while Nvidia sentiment deteriorated from neutral to bearish.
For investors, the central signal is broader than Burry's decision to close two sets of puts. One of Wall Street's most prominent contrarians is maintaining substantial short exposure while cutting the size of every position and preserving cash, giving himself room to respond if market conditions deteriorate.

### Article 103 · 2026-09-10 · fool.com
Nvidia Will Pay Its Next Cash Dividend on Oct. 1. Here's How Many Shares of Nvidia (NVDA) Stock You'd Need for $10,000 in Yearly Dividends.

In its second-quarter fiscal 2027 release, Nvidia ( NVDA +2.55% ) said that it would pay a cash dividend of $0.25 per share on Oct. 1 to all shareholders as of record on Sept. 10. It marks the second consecutive quarter Nvidia is paying a $0.25 per share dividend -- up 2,400% from its previous quarterly payout of just $0.01 per share.
Nvidia is far from high-yield territory, but it's showing more commitment to its dividend. For context, Nvidia now yields more than Apple , Alphabet , and Meta Platforms , while some megacap growth stocks like Amazon , Tesla , and Space Exploration Technologies don't even pay dividends.
Here's how many shares of Nvidia you'd need to generate $10,000 in yearly dividends and why investors can expect that number to drop in the coming years.
The power of holding dividend growth stocks over the long term
At $0.25 per quarter or $1 per share per year, simple math tells us that it would take 10,000 Nvidia shares to generate $10,000 in yearly dividend income. At $225.73 per share as of market close on Sept. 8, a 10,000-share Nvidia position would be valued at a staggering $2,257,300. Meaning at this stage, Nvidia isn't a good stock for investors whose primary objective is to generate passive income. But it could become the perfect dividend growth stock over time.
Companies that steadily grow their earnings, and in turn their dividends, can benefit long-term investors through a combination of unrealized capital gains and growing passive income. JPMorgan Chase ( JPM +1.08% ) is a textbook example. The stock yields 1.7% today, based on its $1.50-per-share quarterly dividend. But investors who bought the stock 10 years ago are getting a high yield on their initial investment because the company has increased its dividend year after year, and the payout has more than tripled over that period, while the stock price has more than quintupled. Investors who bought the stock 10 years ago at around $67 per share would be producing a yield on cost of 9%, which is today's annual payout of $6 per share divided by the cost basis of $67 per share. This example showcases the power of buying a company whose growing earnings justify a higher share price and, in turn, more dividends for shareholders, which puts the dividend-income-earning power of the initial investment in ultra-high-yield territory.
Nvidia is laying the groundwork for recurring revenue
A common mistake is assuming a stock is a good or bad source of passive income based solely on its current dividend yield. A far better approach is to ask whether a company has the runway for future earnings growth that justifies higher dividend raises and, in turn, increases the passive income generated by that initial investment. I could see Nvidia's dividend increasing significantly in the years to come, driven by management's commitment to returning cash to shareholders and new opportunities in artificial intelligence (AI) data centers.
On its fiscal Q2 2027 earnings call, Nvidia said it has returned 60% of free cash flow (FCF) to shareholders so far this fiscal year -- ahead of its 50% target. But even with the dividend raise, buybacks were more than 3 times higher than dividend payments in Q2. Nvidia is generating so much FCF that it can easily afford to grow its dividends while still aggressively buying back its stock. That's reason alone to expect another dividend hike.
However, the runway for Nvidia to become a reliable dividend growth stock has more to do with its evolving business model than its current capital return program. If AI adoption continues, Nvidia will become less dependent on one-off cyclical hardware sales and become a far more consistent business, ideally suited for steady dividend growth. Nvidia's CUDA software and leading graphics processing units (GPUs) already gave it an enviable edge in data center computing power. But its Vera Rubin platform expands that moat by adding a rack-scale solution that goes beyond GPUs to include central processing units and networking.
Nvidia is controlling a larger share of the data center market with the goal of providing the most efficient computing at the lowest cost -- making it a foundational AI infrastructure provider. The market is recognizing this position, as evidenced by a recent $500 billion partnership between Nvidia and six financial institutions to raise capital for investments in Nvidia AI computing infrastructure, which can be sold to enterprises, AI labs, AI start-ups, and cloud companies.
If overall computing demand and the pool of customers using Nvidia's hardware and software increase, then Nvidia will pave the way for steadily growing FCF from new demand and from swapping out older racks with its latest platforms. As AI infrastructure matures, the pace of Nvidia's revenue growth would likely slow, but it could remain a moderate-growth cash cow that steadily grows its earnings and, in turn, its dividends.
Nvidia remains the top AI stock to buy now
It takes 10,000 Nvidia shares to generate $10,000 in yearly dividend income, but that's only based on the company's present payout. If Nvidia quadruples its dividend over the next decade -- which it could afford to do today if it didn't buy back stock -- then investors would only need to buy 2,500 shares to generate $10,000 in yearly dividend income.
Nvidia is a good lesson in why long-term dividend investors should focus more on expected dividend growth than on present yield alone. Nvidia went years without raising its dividend and only recently made a sizable increase. But based on its capital return plan, management's commentary on recent earnings calls and investor presentations, and where I think the business is headed, Nvidia transitioning from a high-flying growth stock to a balanced dividend growth stock makes a ton of sense. This is why Nvidia remains a great buy for investors looking for a reliable AI stock to anchor their portfolios.
Nvidia Will Pay Its Next Cash Dividend on Oct. 1. Here's How Many Shares of Nvidia (NVDA) Stock You'd Need for $10,000 in Yearly Dividends.
By Daniel Foelber – Sep 10, 2026 at 11:10AM EST
Nvidia is generating gobs of free cash flow that could pave a transition from a hypergrowth stock to a more consistent dividend growth stock.
Long-term investors should focus on the income-generating potential during the lifetime of an asset rather than what it yields today.

### Article 104 · 2026-09-10 · finance.yahoo.com
Nvidia Just Gave Its Dividend a Massive Raise but Does It Even Matter?

NVDA's dividend jumped 25x from $0.01 to $0.25 per share, yet its 0.018% yield confirms this remains a capital-appreciation stock, not an income play.
In Q2 FY2027, NVIDIA funneled $20 billion into buybacks versus $6 billion in dividends, making the payout essentially rounding error against total returns.
CFO Colette Kress confirmed NVIDIA returned 60% of free cash flow year-to-date, already outpacing the company's 50%-or-more annual target.
Just released. Our analysts combed the entire stock market and named the ten best stocks to buy right now, and NVIDIA made the cut. Enter your email to see the other nine names and why NVDA earned its spot. The report is free. Enter your email and see the full list.
The single metric worth isolating on NVIDIA ( NASDAQ:NVDA ) is the dividend itself, and specifically what fraction of total capital return it represents.
NVIDIA's quarterly cash payout jumped from $0.01 per share at the March 11, 2026 ex-date to $0.25 per share at the June 4 ex-date. Trailing twelve-month payments total $0.53; the annualized forward rate is $1.00. That split between trailing and forward is the fingerprint of a fresh raise.
In Q2 FY2027, NVIDIA returned $26 billion to shareholders: $20 billion through share repurchases and $6 billion through the quarterly dividend. Across all of FY2026, dividends were $974 million of $41.1 billion in total returns, set against $96.58 billion in full-year free cash flow. The check is rounding error.
The next payment lands October 1, 2026, following declaration on August 26, 2026 and an ex-dividend date of September 10, 2026. CFO Colette Kress told investors NVIDIA has "returned 60% on a year-to-date basis" against a plan to return 50% or more of free cash flow. Shares changed hands at $218.42, off 2.24% intraday but up 874.85% over five years.
Why NVDA Made Our Top 10 List
And NVDA made the cut. See who else did.
A bullish signal would be another authorization stacked onto the $99.0 billion remaining under buyback authorization, plus successive dividend hikes as strategic spending gets funded; Kress cited "nearly 50 billion in the Frontier AI Labs". A bearish read would be capital returns easing as $279.0 billion in Vera Rubin supply commitments consume cash. All of that spend has to be powered, cooled, and networked by somebody, which is why we mapped seven suppliers behind the buildout in a free AI infrastructure report.
NVIDIA remains a capital-appreciation story with a token dividend attached; a buyer chasing the 0.018% yield has misunderstood what they own.
If you have cash sitting in your account right now, give this two minutes. After more than two decades of helping investors beat the market, our top analysts at 24/7 Wall St. put together a definitive report on the Top 10 Stocks To Buy Today. And NVDA was one of them.

### Article 105 · 2026-09-10 · sdxcentral.com
Nvidia’s Groq deal facing DOJ probe amid regulator scrutiny into acqui-hires: report

By Ben Wodecki
Nvidia’s deal with Groq is back in the spotlight amid reports that the Department of Justice (DOJ) could look into the deal.
The New York Times reports that DOJ officials have sent a formal request for information to Nvidia regarding the deal. An investigation commenced following its disclosure in late December, with antitrust officials reportedly looking into whether the chip giant sought to skirt an antitrust probe.
Nvidia billed the deal as a “nonexclusive licensing agreement” that saw Groq founder and then CEO Jonathan Ross jump across to Nvidia, along with several key members of the Groq team.
Exact terms were not disclosed, though a reported $20 billion was spent on the apparent licensing deal providing the green light for Groq’s low-latency processors to be integrated into Nvidia’s so-called AI factory architecture.
Nvidia quickly went on to debut the Groq 3 language processing unit (LPU) , which forms the basis of the LPX rack-scale platform designed as a complementary add-on for operators running Nvidia's flagship NVL72 to want power low-latency AI inference workloads. The platform recently entered full production ahead of an anticipated launch later this year.
" The Groq story is a prime example of the American system working as designed to promote innovation, reward entrepreneurs, and benefit consumers," Nvidia spokesperson John Rizzo told the Times. “The law is designed to encourage America’s start-up ecosystem and promote the fundamental rights of inventors and workers to pursue their dreams.”
Nvidia has previously fallen foul of antitrust regulators with its $40 billion attempt to buy Arm in 2022. One Nvidia deal that will face the wrath of the regulator will be its recently announced $12.9 billion bid for open source AI repository monolith Hugging Face .
The GRoq probe comes amid a Federal Trade Commission (FTC) examination into big tech’s love for acqui-hires. Chairman Andrew Ferguson told Bloomberg in February that it wants to ensure such deals “are not an attempt to get around” its merger review process.
Nvidia’s Groq ransack hasn’t stopped the startup from pressing on, with Meta’s former lead network engineer recently joining as head of network and data center engineering.
