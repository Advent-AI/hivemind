# Blind reader, matter census batch 9 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 40 articles (numbers 293 to 332,
2026-09-17 to 2026-09-18, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 293 · 2026-09-17 · tweaktown.com
Microsoft is bringing in NVIDIA's Jensen Huang for its biggest Windows event since 2024

The Surface Laptop Ultra is expected to take center stage, powered by a custom NVIDIA RTX Spark SoC with up to 128GB of unified memory.
A Windows-branded graphic announces an October 7, 2026 event in San Francisco, with the date incorporated into a large 10:07 design.
Microsoft will host a Windows and Surface event on October 7 with NVIDIA CEO Jensen Huang; the Surface Laptop Ultra - featuring a custom NVIDIA RTX Spark SoC with a Blackwell GPU, up to 128GB unified memory, native CUDA, and up to 1 petaflop local AI compute for 120B-parameter models - is expected to headline, while Windows 11 gains scheduling and Prism emulation optimizations and OEMs like Dell, Lenovo, and ASUS plan RTX Spark laptops.
Microsoft is preparing its biggest Windows-focused event in more than two years, and it's bringing in some serious outside firepower. The company has confirmed a Windows and Surface event for October 7 in San Francisco, with NVIDIA CEO Jensen Huang joining Microsoft CEO Satya Nadella and Windows and Surface chief Pavan Davuluri on stage.
According to Microsoft's invitation teasers, the event will centre on "how local AI will shape the next chapter of the PC," starting at 10 AM PT / 1 PM ET. With Jensen Huang on stage, NVIDIA's RTX Spark platform will likely feature heavily in the discussion, tying together developments across Windows software, NVIDIA hardware, Surface devices, and the broader PC ecosystem.
Likely taking centre stage is the Surface Laptop Ultra , a high-performance machine Microsoft first teased earlier this year as its answer to the MacBook Pro. Beyond the design upgrade, the laptop's highlight is its custom NVIDIA RTX Spark SoC , which pairs a Blackwell GPU with up to 128GB of unified memory, up to one petaflop of AI compute, and native CUDA support. This allows it to run AI models with up to 120 billion parameters entirely locally. Microsoft still lists the laptop as a pre-release product, with final availability pending regulatory approval, and has not yet announced pricing.
The RTX Spark Superchip graphic pairs a rendered processor with circuitry lines and a slogan emphasizing combined capabilities.
To support that hardware, Microsoft has spent this year refining the underlying Windows 11 software stack. That includes a specialised Workload Profile Scheduling system designed to distribute background tasks across the chip's 20 CPU cores, along with an optimised Prism emulation layer meant to keep legacy x86 applications running efficiently on ARM-based hardware.
The presentation slide pairs the RTX Spark laptop announcement with an “Available Fall” message and logos from eight PC makers, including Microsoft.
What is the Surface Laptop Ultra and how does its RTX Spark SoC change what it can do locally?
The Surface Laptop Ultra is Microsoft's high-performance Surface laptop that it first teased earlier this year as an answer to the MacBook Pro. Its custom NVIDIA RTX Spark SoC gives it up to 128GB of unified memory, up to one petaflop of AI compute, and native CUDA support, which lets it run AI models with up to 120 billion parameters entirely locally.
How does native CUDA support work on this Surface Laptop Ultra?
What kinds of AI models can the Surface Laptop Ultra run entirely on-device?
What does Microsoft’s Workload Profile Scheduling do on the RTX Spark-powered hardware?
Beyond Microsoft's own Surface lineup, major hardware partners including Dell, Lenovo, and ASUS have already committed to building their own laptops around the RTX Spark platform. Microsoft's last major Windows event took place in May 2024 for the original Copilot+ PC launch, and the one before that dates back to the Windows 11 reveal in June 2021.
Best Deals: Microsoft Surface Laptop 2026 13.8-inch Premium Performance Laptop

### Article 294 · 2026-09-17 · finance.yahoo.com
ASUS and Poesis Team Up on Autonomous Trading Agents Powered by NVIDIA Technologies

The ASUS ExpertCenter Pro ET900N G3 deskside AI supercomputer is now shipping. It is powered by the NVIDIA GB300 Grace Blackwell Ultra Desktop Superchip and delivers up to 20 PFLOPS of AI performance with 748GB of coherent memory. The ET900N G3 is built for secure enterprise AI, so organizations can develop, fine-tune, and run large AI models on their own premises.
ASUS and Poesis show a fully autonomous, multi-agent AI investment system running on the ASUS ExpertCenter Pro ET900N G3, a deskside AI supercomputer powered by the NVIDIA GB300 Grace Blackwell Ultra Desktop Superchip. The dashboard shows eight AI portfolio-manager agents, each running a different investment strategy from long-only value to market-neutral quant. All eight agents use NVIDIA Nemotron 3 Super and run on a single deskside machine.
Test Offers a Glimpse of Possibilities for Agents Using Live Capital on Deskside Supercomputer
Autonomous AI agents trade in live financial markets: ASUS and Poesis completed a week-long experiment in which agentic AI agents independently conducted investment research, managed risk, and executed trades using live capital and predefined mandates.
A deskside supercomputer powers the entire AI workflow locally: Running on the ASUS ExpertCenter Pro ET900N G3, powered by NVIDIA GB300 Grace Blackwell Ultra Desktop Superchip, the experiment demonstrated local execution of AI models, agents, and workflows without dependence on cloud-based AI infrastructure.
Exploring the future of agentic AI in asset management: The collaboration offers early insights into how local, high-performance computing can support autonomous investment workflows and the ongoing development of agentic AI systems for financial markets.
SAN FRANCISCO, September 17, 2026 --( BUSINESS WIRE )--ASUS and Poesis today announced the results of a week-long experiment that successfully deployed agentic AI to trade autonomously in financial markets. The system ran entirely on the ASUS ExpertCenter Pro ET900N G3, a deskside supercomputer built on the NVIDIA DGX Station platform, powered by NVIDIA GB300 Grace Blackwell Ultra Desktop Superchip .
Throughout the test, all models, agents, and workflows ran locally on the ASUS ExpertCenter, showing that agents can function in live markets without relying on cloud-based AI infrastructure.
"While this was an early-stage experiment, it showed that agents can operate continuously in live markets while remaining within clearly defined constraints," said Alex Popa, Founder and CEO of Poesis , an AI-native asset manager developing agentic systems for financial markets.
The collaboration reflects growing interest across industries in moving agentic AI from experimentation towards practical development, particularly in asset management.
"Working alongside Poesis at the intersection of AI and financial markets gave us valuable insights," said Yen Hoang, Director of Marketing, B2B, ASUS North America . "As agentic AI continues to evolve, projects like this are essential to helping us better understand how autonomous investment workflows can be developed and deployed in real-world trading environments."
Built on NVIDIA DGX Station Powered by NVIDIA Blackwell Ultra
The week-long experiment ran on the ASUS ExpertCenter Pro ET900N G3, powered by NVIDIA GB300 Grace Blackwell Ultra Desktop Superchip. Featuring up to 20 petaFlops of AI performance and 748GB of coherent memory, the system enabled Poesis to deploy a multi-agent AI workflow locally on a single machine.
Using live capital, the agents autonomously handled investment research, risk management, and trade execution while operating within predefined mandates.
ASUS (2357.TW) is an innovative technology leader delivering the world's most comprehensive AI solutions across Infrastructure, Physical AI, AI PC/Devices, and Engineering the AI Advantage. Guided by its "Ubiquitous AI. Incredible Possibilities" strategy, ASUS is bringing enterprise-to-edge AI to life. The ASUS portfolio also includes the ROG and ProArt sub-brands, which serve gamers and creators worldwide.
Poesis is an AI-native asset manager developing agentic systems that research, manage risk, and trade, deploying AI-led investment strategies in live markets. Poesis was founded by Alex Popa, previously a partner and portfolio manager at Capital Group, and Charles Elkan, former Global Head of Machine Learning at Goldman Sachs.
This experiment was conducted as a limited-duration proof of concept designed to evaluate the operational characteristics of autonomous AI agents in a live market environment. The results should not be interpreted as evidence of long-term investment performance or future financial outcomes. References to trading activity are provided solely to describe the experimental workflow and do not constitute investment advice or recommendations.

### Article 295 · 2026-09-17 · techcrunch.com
Google, Nvidia, and Anthropic want Emerald AI to find space on the grid for more data centers

Grid software unicorn Emerald AI has formed a coalition with Google and Nvidia that will use the startup’s technology to secure space on the grid for more data centers.
The AI Energy Management Alliance (AEMA) hopes to make demand response — a paradigm in which data centers temporarily reduce their electricity use — an integral part of data center development. Pausing noncritical tasks and shifting some compute loads, AEMA says, could allow an additional 100 gigawatts of data centers to connect to the grid.
The founding trio is joined by Anthropic, and a range of utilities including AES, Constellation, National Grid, and NRG Energy.
Demand response is an old concept that has been used by utilities for decades. It works because the grid is designed with peak loads in mind. For much of the year, demand is well below the maximum the grid can support.
Traditionally, demand response covered large electricity users like factories, which in times of high demand would agree to reduce their usage, typically by pausing production or switching to backup generators. In exchange, the utility would pay them for the service, often handsomely.
Today, data centers can also take advantage of those programs, usually by turning on backup generators.
Emerald AI has been proposing an alternative to dirty diesel generators. The company’s software coordinates requests from utilities with data centers, which can pause noncritical tasks or shift loads to other data centers where the grid has some headroom.
The startup isn’t the only one working on such technology. Google has been developing its own tools, and Enel X lets data centers tap their uninterruptible power supplies to round off peaks in power demand. Limiting max grid usage to 90% for a few hours at a time could let data centers free up 76 gigawatts of capacity, according to a study by Goldman Sachs published last year.
Emerald AI does have an advantage, though. Its software connects utilities directly to data centers, which should allow data centers to respond quickly to requests, much like batteries. The startup also recently raised $150 million in a Series A led by Energize Capital and DCVC, giving it the sort of funding needed to roll out the technology on a wider scale.
Given the peaky nature of AI compute loads, and data centers’ ability to quickly ramp up and down, the creation of something like AEMA is overdue. The coalition also promises to help tech companies and utilities find new sites for data centers, an effort that hasn’t been easy for either party.
Despite its promise, more sophisticated demand response won’t solve all of the grid’s problems today. Ayse Coskun, Emerald AI’s chief scientist, told TechCrunch that her company’s technology promises to blunt the industry’s need for new generating sources, but it won’t eliminate it entirely.
Tim De Chant is a senior climate reporter at TechCrunch. He has written for a wide range of publications, including Wired magazine, the Chicago Tribune, Ars Technica, The Wire China, and NOVA Next, where he was founding editor.
De Chant is also a lecturer in MIT’s Graduate Program in Science Writing, and he was awarded a Knight Science Journalism Fellowship at MIT in 2018, during which time he studied climate technologies and explored new business models for journalism. He received his PhD in environmental science, policy, and management from the University of California, Berkeley, and his BA degree in environmental studies, English, and biology from St. Olaf College.

### Article 296 · 2026-09-17 · gurufocus.com
Nvidia Gains 2.5% as Huawei Compresses Its 2027 Roadmap

Nvidia ( NASDAQ:NVDA ), the dominant AI-accelerator and data-center platform provider, confronted a faster competitive push from Huawei Thursday as the Chinese technology giant pulled forward its next generation of AI chips, Reuters reported. Nvidia shares gained approximately 2.5% to $219.24. Huawei now plans to launch its Ascend 960DT in early 2027roughly three quarters earlier than previously expectedfollowed by the 960PR in the third quarter, sharpening the race for the infrastructure powering increasingly massive AI workloads.
Huawei is thinking beyond a single accelerator. Its Peerium architecture is designed to eventually link as many as one million processors, while a nearer-term supernode would connect 4,096 chips. That scale directly targets the system-level advantage Nvidia has built around GPUs, networking and tightly integrated AI infrastructure. But the headline numbers come with a major constraint: Huawei says production still cannot satisfy demand inside China, making manufacturing capacity a potential brake on both domestic adoption and any meaningful overseas expansion.
That distinction matters because Nvidia's AI engine is already operating at enormous commercial scale. Data-center revenue reached $89 billion , accounting for roughly 92.5% of the company's latest $96.2 billion quarter. The GuruFocus picture also remains unusually strong: Nvidia carries a GF Score of 95 out of 100, with standout profitability, growth and financial strength, while GF Value is clearly the weakest part of the profile. In other words, Huawei is raising the competitive pressure, but the real test will be whether it can turn ambitious processor counts into reliable supply, software adoption and customer deployments at scale.

### Article 297 · 2026-09-17 · rdworldonline.com
Lilly, Roche and BMS are all building AI supercomputers: here’s what they’re doing differently

By Julia Rock-Torcivia | September 17, 2026
Lilly’s LillyPod, an AI supercomputer, went live on February 25 . Roche deployed its NVIDIA AI factory on March 16 and BMS has been running its AI factory for almost three years , with NVIDIA hardware powering all three buildouts. NVIDIA uses the term “ AI factory ” to describe a GPU cluster built to train and run AI models.
Blackwell Ultra GPUs, which offer 50% more memory and compute than standard Blackwell, power Lilly’s single, centralized supercomputer. Roche is also using Blackwell GPUs for its distributed hybrid-cloud model while BMS is expanding its existing infrastructure with Vera Rubin, which roughly triples Blackwell Ultra’s inference performance per GPU. Both Lilly and BMS use NVIDIA’s DGX SuperPOD, NVIDIA’s prepackaged supercomputer design. Roche has not disclosed which server platform underlies its GPU deployment.
Eli Lilly, Roche and BMS are among R&D World’s 100 most innovative companies of 2026 . The list examines what each company built, who is using it and the results it has reported. R&D World will publish the full comparison in the 2026 Global R&D Funding Forecast.
A DGX SuperPOD with 1,016 NVIDIA Blackwell Ultra GPUs powers LillyPod, which delivers more than 9,000 petaflops of AI performance. Roche’s system also uses Blackwell GPUs, though the company’s materials do not specify which model.
Lilly said it assembled the Indiana-based supercomputer in just four months.
The factory can harness 700 terabytes of data using over 290 terabytes of high-bandwidth GPU memory, capacity Lilly says will support training protein diffusion, small-molecule graph neural network, and genomics foundation models. That scale of computation lets scientists test billions of molecular ideas at once, Lilly says, compared with the roughly 2,000 per target a wet lab team can typically manage in a year.
Six months in, Lilly reported that LillyPod was running large open-weight language models on-premises and making them available across the company with no token or budget limits. Chief AI Officer Thomas Fuchs posted on LinkedIn, saying Lilly is the first in pharma to deploy NVIDIA’s Nemotron 3 Ultra, an approximately 550-billion-parameter open-weight model, on-premises, optimized for B300 GPUs at FP4 precision.
Roche’s NVIDIA AI factory, a distributed, hybrid-cloud architecture spanning several sites across the U.S. and Europe, features 2,176 NVIDIA Blackwell GPUs, more than double Lilly’s factory. The company’s total on-premise and cloud infrastructure exceeds 3,500 Blackwell GPUs.
The factory combines NVIDIA’s BioNeMo platform, an open development platform for AI-driven biology and drug discovery, with Roche’s Lab-in-the-Loop to test hypotheses and accelerate progress. NVIDIA’s Omniverse libraries power digital twins that engineers use to optimize processes and factory designs.
BMS has had a multi-year alliance with NVIDIA, saying it first deployed NVIDIA DGX SuperPOD infrastructure nearly three years ago. BMS deployed the DGX SuperPOD-powered factory to support its R&D activities as part of an AI Center of Excellence. The factory uses the DGX SuperPOD to accelerate oncology research, train models on clinical trial images and use NVIDIA MONAI and self-supervised learning for lesion segmentation.
BMS announced an expansion of the AI factory two months ago, which the company said will be “the most powerful and energy-efficient single-owned NVIDIA infrastructure in life sciences.”
The factory will support BMS’s next-generation foundation models trained on the company’s proprietary data and drawing on domain-specific capabilities from BioNeMo to power agentic workflows.
Roche has a total of over 3,500 GPUs with the on-premise and cloud count combined. It owns 2,176, compared to Lilly’s 1,016. However, Roche has not published a performance figure while Lilly reports 9,000 petaflops.
The three also differ on architecture. LillyPod is a single, centralized supercomputer that sits in one Indianapolis facility. Roche spread its GPUs across multiple sites in the U.S. and Europe, supplementing on-premises hardware with cloud capacity. BMS has one DGX SuperPOD already up and running and one recently announced, which the company will combine into a single environment accessible across sites.
Lilly and Roche are both running on Blackwell-family chips. BMS’s new system will run on Vera Rubin, NVIDIA’s newer architecture, which is approximately three times faster than Blackwell Ultra.
Lilly, Roche and BMS aren’t the only companies racing to build AI infrastructure. Amgen has deployed a DGX SuperPOD , nicknamed “Freyja”, at its deCODE genetics subsidiary in Reykjavik, Iceland. The system runs on 31 DGX H100 nodes, with 248 H100 GPUs in total. The company built it to mine more than 200 petabytes of de-identified human genetic data for drug targets and disease biomarkers.
AstraZeneca is one of five partners in Sferical AI , a jointly owned Swedish company also backed by Ericsson, Saab, SEB and Wallenberg Investments. Sferical is deploying two DGX SuperPODs built on Grace Blackwell GB300 systems, with 1,152 GPUs combined, in Sweden. AstraZeneca said it will use the shared system to “spearhead the next generation of AI enabled drug discovery and development.”
Novo Nordisk is using Gefion’s supercomputer , with 1,528 H100 GPUs rather than building or co-owning hardware. Gefion is owned and operated by the Danish Centre for AI Innovation, which the Novo Nordisk Foundation , a philanthropic entity distinct from the pharma company, partly funds.

### Article 298 · 2026-09-17 · news.fiu.edu
Undergraduate research set student on path to NVIDIA and Apple

Undergraduate research set student on path to NVIDIA and Apple
By By Adrienne Sylver
Abiel Almonte’s career in tech took off even before he’d set foot in his first class at FIU’s College of Engineering and Computing . Rather than wait for the fall semester to figure out where he fit in, he spent the summer scouting out labs that caught his interest and soon landed a spot in the Applied Research Center before many of his classmates had even ordered their textbooks.
“I felt like the Applied Research Center was my sandbox,” he says. “I developed coding skills and cultivated an interest in cybersecurity, artificial intelligence and machine learning. I got very deep into the technical aspects, and I also learned how to interact with other peers and colleagues.”
The senior computer engineering major spent a year and a half in the lab, honing his skills and building a foundation that would carry him to two of the biggest names in tech. Last year, he spent his summer as a software engineering intern at NVIDIA in Santa Clara, California. This summer, he returned to California to complete a machine learning internship with Apple in Cupertino.
“At NVIDIA, I was part of a team working on how large language models get deployed and synch across services,” he says. “It gave me experience working in a formal, software engineering environment and collaborating to solve problems at scale.”
At Apple, Almonte worked on in-home devices, developing models that run faster and more efficiently on Apple’s on-device accelerators.
“We are working on enabling these programs to run on wearables, like your watch. Improving Apple’s smallest neural engines is exciting and fun, and I feel like I am the right person for the job,” he says.
Almonte attended the School for Advanced Studies on the Kendall campus of Miami Dade College. He graduated in 2023 with both his high school diploma and an Associate in Arts degree from the college.
At the Spring 2026 College of Engineering & Computing Senior Design Showcase, his “flash-recon” project won the award for most innovative for its real-time technology that generates a live 3D map of an environment from a single camera feed. The system has potential applications in navigation, search and rescue and autonomous vehicles.
He is also the student author on “ Adversarial AI Training to Mitigate Cyber Attacks ,” an early interest of his. It was published in the 2025 Institute of Electrical and Electronics Engineers International Conference on Artificial Intelligence Testing.
“Abiel has demonstrated exceptional self-motivation across the AI engineering stack,” says Himanshu Upadhyay, a professor of electrical and computer engineering. “He has a proven ability to tackle deep-tech bottlenecks. Ultimately, his work bridges the gap between raw hardware acceleration and advanced application deployment.”
Outside the lab, Almonte hikes, writes a blog and continues to contemplate how to make machines run faster, smarter and closer to the humans they’re built to serve.

### Article 299 · 2026-09-17 · tomshardware.com
Investigative report details how export-restricted Nvidia AI chips reach China — public records reveal how Chinese entities skirt US sanctions

Investigative report details how export-restricted Nvidia AI chips reach China — public records reveal how Chinese entities skirt US sanctions | Tom's Hardware
Investigative report details how export-restricted Nvidia AI chips reach China — public records reveal how Chinese entities skirt US sanctions
By Bruno Ferreira
Much to the surprise of absolutely no-one.
American nonprofit C4ADS, a monitoring organization funded mostly by the U.S. government, produced a report shedding light on the many ways that American AI accelerators reach China. Somewhat paradoxically, the U.S. refuses to sell advanced AI chips to China, while simultaneously the CCP prohibits their purchase, but that has seemingly not stopped the products from arriving on Eastern shores.
C4ADS's report identifies three major avenues for chip smuggling: direct acquisitions via research institutions, drop-shipping through other Southeast Asian countries, and purchases through a matryoshka-doll-like structure made of shell companies. The writers note that only explicitly mentioned chips are accounted for, meaning the actual amount of hardware changing hands could be far higher. Another earlier report by Epoch AI estimates that around a third (and possibly most of) China's AI compute power is comprised of smuggled GPUs.
Firstly, a quick primer on chip logistics. Nvidia has most of its chips manufactured and packaged at TSMC in Taiwan. An individual chip, or the entire accelerator unit it's in, might go through several rounds of testing, potentially doing more than one trip before it lands in a customer's data center.
As for export and import controls: the U.S. forbids the sale of H100, A100, and Blackwell-family chips to China; the lower-end H20 chip and the meatier H200 (and AMD MI325X) can be traded on a case-by-case basis, with the latter getting a 25% tariff. Meanwhile, China's broad position is to discourage and restrict the purchase of American AI chips, in a bid to spur its national efforts, currently spearheaded by Huawei . However, multiple reports indicate the authorities often turn a blind eye to gray/black-market imports, and 2026 saw official exceptions issued to ByteDance, Alibaba, and Tencent .
The first way to get a 'forbidden' chip into China via quasi-legal means is by simply getting a Chinese university or research institution to buy it. These entities reportedly include Nvidia GPUs inside "sprawling multi-vendor contracts," routed through small Chinese regional integrators.
The report also claims that some buyer institutions have ties to the CCP and the country's defense and intelligence sectors. C4ADS says that it tracked 56 chips worth $1.7 million sold this way in the report's July 2025 to January 2026 period. Additionally, it says that its 2024 investigation covering multiple years of government records revealed $6.48 million worth of silicon heading to China in this manner.
The second route for smuggling potent silicon is technically legal, via drop-shipping it through Southeast Asian countries including Vietnam, India, and Malaysia. C4ADS analyzed transactions between 2022 and 2025, and found $13.4 million of Nvidia A100, H100/GH100, and AD102-series GPUs routed through the aforementioned countries, in a "consistent pattern." Some chips traveled from Taiwan to Vietnam, possibly aided by the fact that Vietnam's chip testing facilities offer a good excuse for the trip. The investigation remarks that the timing, volume, and destination of many shipments could obscure their true intent.
A portion of purportedly tested chips traveled on to Hong Kong, where two companies "[dominate] the import side", Profit New Limited and ELB International Limited. The former traded trading $8.7 million of silicon in a single day in March 2025, likely in preparation for April 2025's tightened export controls. Some high-value shipments in the dataset were apparently bereft of cost, insurance, weight, or freight values, and also had nice round zeros in their import value declarations, raising suspicions about the veracity of their documentation.
The largest category, though, is opaque ownership — or shell companies. According to C4ADS, this method accounted for $4.6 billion worth of intelligent sand migrating to China, on the account of just one entity, Megaspeed International. This firm was reportedly the biggest Southeast Asian importer of Nvidia hardware in the time span between 2023 and 2025. However, its actual ownership is "unresolved."
Megaspeed has multiple companies across Singapore, Indonesia, and Malaysia, but it was purchased in 2023 by Swiftdata, another Singaporean firm. Before that, it was owned by Chinese gaming firm 7Road Holdings. During the transition, however, Megaspeed's major shareholder was temporarily Chinese businesswoman Huang Le, who's also a director of a Hong Kong company that bought transceivers from Megaspeed Indonesia. C4ADS believes Le may still be calling the shots at Megaspeed, though, seeing as she's identified as the firm's chairwoman at a conference as recently as 2025.
The speed and manner in which Megaspeed changed hands also raised some eyebrows, and it's still seemingly unclear who owns Swiftdata itself. Given that Megaspeed reportedly obtained export-locked Blackwell chips, it's hard not to find its dealings more than a tad murky.
C4ADS does issue recommendations to try and mitigate the problem. Namely, it remarks that the U.S. Bureau of Industry and Security gets allocated additional staff and resources so it can verify where the wares landed after their sale, and who their end users are. This could arguably be difficult to enforce, as it would require a level of cooperation from other nations that might prove a tad tricky to obtain in the current political climate.
In the researchers' own words, "U.S. and friend-shored semiconductor manufacturers, equipment makers, and distributors should invest in a robust end-user verification system that goes beyond standard restricted-party list screening, incorporating on-the-ground due diligence, corporate ownership tracing, and post-shipment verification." To the private sector, C4ADS recommends that firms add geopolitical and risk analysis into their frameworks, in a bid to assess if their direct or downstream customers could be selling wares to China's military or intelligence sectors.

### Article 300 · 2026-09-17 · insidermonkey.com
The Return-on-Capital Question Looming Over NVIDIA Corporation’s (NVDA) AI Investments

Hayden Capital, an investment management firm, released its second-quarter 2026 investment letter. The letter can be downloaded here . In the second quarter, the portfolio gained 6.9%, compared to the S&P 500's 15.2%. Overall, approximately 34% of the portfolio is in Asia, 43% in North America, and the rest spread across other regions. Hayden Capital remains guided by a strategy focused on high-quality franchises with stable earnings power, continuing to invest despite this year's challenging results. Their largest investments are experiencing over 40% revenue growth yet are trading at similar valuations to the broader market, indicating potential for future outperformance. The recent market corrections in AI investments have prompted a healthier perspective among investors, emphasizing the importance of strong business fundamentals. Companies are leaning towards partnerships with AI firms rather than outright replacements, ensuring better access to data and operational efficiency. Six months into the "SaaS-pocalypse," software incumbents remain resilient despite initial fears of disruption. While AI is indeed transformative, the anticipated rapid changes in markets have not materialized as quickly as expected. Also, check the fund's top five holdings to see its best picks in 2026.
In its second-quarter 2026 investor letter, Hayden Capital highlighted NVIDIA Corporation (NASDAQ: NVDA ). NVIDIA Corporation (NASDAQ:NVDA) is a leading data center-scale AI infrastructure company operating through Compute & Networking and Graphics segments. On September 16, 2026, NVIDIA Corporation (NASDAQ:NVDA) closed at $213.90 per share. Over the past month, NVIDIA Corporation (NASDAQ:NVDA) declined 1.36%, but its shares are up 21.37% over the past year. NVIDIA Corporation (NASDAQ:NVDA) has a market capitalization of $5.15 trillion, and its stock has traded within a 52-week range of $164.27 to $236.54.
Hayden Capital stated the following regarding NVIDIA Corporation (NASDAQ:NVDA) in its Q2 2026 investor letter:
"Answering that requires clarity on the second variable – the incremental return on invested capital. It's why the narrative around hyperscalers (and thus their stock prices) have swung around the past year, and why no one is confident in the answer. The downstream beneficiaries – the semi component makers – are even more exposed. If these companies are reinvesting 100% of their cash flows at 50% ROICs, that's fantastic. Earnings should compound at that rate, and the shares look cheap at today's prices. The irony is that for companies deploying AI into their own operations, better returns require the opposite of scarcity. They need token prices to fall – or model capabilities to improve enough that the output finally justifies the spend. And falling token prices require supply to increase, which is already starting to happen (see the recent announcements from SK Hynix, Samsung, and CXMT). What happens when that supply arrives just as resale premiums compress, and the speculative bid goes with it? Without confidence in that, you can't calculate a sustainable ROIC. You can't rely on scarcity pricing if there's a growing chance that scarcity ends. After all, the fundamental support price should be whatever return end-users can generate by embedding AI into their own businesses, less a margin for the provider. But it's too early to calculate that number with any precision.
And interestingly, the market seems to be asking the same thing. For example, NVIDIA Corporation (NASDAQ:NVDA) is undoubtedly one of the most important companies in the middle of this AI buildout boom. And yet despite expecting to grow earnings ~+89% y/y this year, its P/E multiple is below consumer staples companies barely growing above GDP2. I suspect the market is wrong one way or the other – either multiples need to rise as earnings prove durable, or earnings growth estimates need to come down. In the end, it's about predictability / sustainability of earnings, not what's happening today – since over 90% of a company's value lies in the earnings stream 5+ years out. The market's just saying it doesn't know what profits look like several years in the future…" ( Click here to read the full text )
In another article , we discussed NVIDIA Corporation's (NASDAQ:NVDA) plan to invests a $10 Billion stake in Anthropic's $2 Trillion IPO. In addition, please check out our  hedge fund investor letters Q2 2026  page for more investor letters from hedge funds and other leading investors.

### Article 301 · 2026-09-17 · finance.yahoo.com
Rackspace’s Nvidia Partnership Sparks Early Rally, But a $2.8 Billion Debt Load Remains

Rackspace Technology, Inc. (NASDAQ: RXT ) shares climbed more than 6% after the company announced that it was joining Nvidia's Cloud Partner Program. The move adds to a series of AI infrastructure partnerships that have consistently triggered sharp rallies in the stock. However, the market has also seen the other side of this story. Earlier this year, the stock suffered one of its biggest single-day declines when a similar AI-driven story was followed by a guidance cut and a dilutive capital raise. That contrast is becoming hard to ignore. Rackspace's AI partnership can drive the stock higher quickly, while its balance sheet continues to move in the opposite direction at a much slower pace.
Rackspace Adds Nvidia to Its Sovereign AI Push
The company has entered Nvidia's Cloud Partner Program, aiming to strengthen its role in delivering and managing Nvidia-powered AI computing for regulated and sovereign enterprises.
CEO Gajen Kandiah described the partnership as:
AI sovereignty is ultimately about control: control of your data, your models, and the intelligence your organization creates. NVIDIA provides the accelerated computing foundation, and Rackspace brings the infrastructure, engineering, and operations required to run it in production. For organizations where governance, sovereignty, and uptime are non-negotiable, our role is to make that entire system work and remain accountable for the outcome.
Alongside the partnership, Rackspace Technology also introduced its Institutional Sovereign Pod, an architecture that combines Nvidia's Blackwell technology with Palantir's Foundry and AIP platforms to support governed AI infrastructure. The company said its forward-deployed engineering and managed operations are designed to help customers move from deployment into production more quickly.
A Familiar Pattern, An Unresolved Balance Sheet
Rackspace's recent stock performance highlights the gap between AI-related enthusiasm and its underlying financial position. Shares jumped in May after the company announced a non-binding MOU with AMD. The stock then collapsed 33.6% in a single day in July following a guidance cut and an at-the-market program allowing it to sell up to $250 million of shares. The balance sheet remains a major concern, with roughly $2.8 billion of debt, and negative equity. Free cash flow was negative as well. The Nvidia partnership faces a similar issue to the AMD agreement, as the company has not disclosed a customer contract or revenue commitment tied to the deal.
The sovereign and regulated AI infrastructure market is a legitimate strategic niche for Rackspace. But the company's performance this year has also shown how quickly the market can reverse an AI-driven rally when attention returns to its debt maturities and shrinking legacy operations. The Nvidia partnership does not address either of those underlying challenges.
Institutional interest in Rackspace increased sharply, with hedge fund ownership rising to 22 funds at the end of Q2 2026 from 8 funds at the end of Q1 2026. At the same time, short interest remains extremely high at 22.19% of float as of August 31, 2026. The wide gap between rising hedge fund ownership and heavy short interest suggests conviction is building on both sides of the trade.
While we acknowledge the potential of RXT as an investment, we believe certain AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 302 · 2026-09-17 · nbcbayarea.com
‘We want answers': Family of Nvidia researcher continues to question suicide ruling

By Ali Reid •
The family of a 32-year-old Nvidia researcher who died in July is calling on Palo Alto police to continue to dig into the circumstances of his death, which authorities have ruled a suicide. Ali Reid reports.
The family of a 32-year-old Nvidia researcher who died in July is calling on Palo Alto police to continue to dig into the circumstances of his death, which authorities have ruled a suicide.
Irfan Al-Hussaini was found unresponsive in his Palo Alto home on July 22 and died about a week later. His family is urging state and local authorities to look further into his death, saying the circumstances surrounding his passing are suspicious.
"The brother I knew would never, ever take his own life," Irfan's sister, Sarah Al-Hussaini, said Thursday during a news conference in front of Palo Alto City Hall.
Irfan was a senior AI researcher at Nvidia who had recently been promoted and was focused on his promising future.
While authorities ruled his death a suicide, his family argues the evidence they have says otherwise.
"What little information we were told does not match with the information we have gathered so far and the things we know," Sarah said.
The family said Irfan presented research to about 15 colleagues until about 9 a.m. on July 22. At 10:02 a.m., a Slack message was sent from his account to his manager saying his wife was not feeling well and would take the day off, the family said. A 911 call was placed about 20 minutes later. Doctors told the family initial scans suggested Irfan had been without oxygen for nearly 30 to 60 minutes.
"So who sent that 10:02 text?" Sarah said. "Does that text fit with the medical timeline?"
The family and their attorney, Tony Brass, said there was no suicide note left. They also question whether domestic violence was overlooked.
"The plan that they're supposed to accept is that he hung himself from a door while his wife was home and he did it in a way that she did not detect or know that that was happening," Brass said. "That makes no sense."
The family said Irfan was wearing an Oura ring that morning and believes its data could potentially help establish a timeline for investigators.
"We want a proper investigation, we want answers, we want justice for Irfan," Sarah said.
Palo Alto police said the case remains under investigation, pending the medical examiner’s report. The department said it has received materials from the family and others, adding that neither police nor the medical examiner have identified evidence of foul play.
An attorney for Irfan’s widow said she fully cooperated with the investigation and that a full forensic autopsy was performed on Aug. 31. The attorney said Irfan’s widow has no objections to forensic materials being reviewed.
If you or someone you know is in crisis, call or text 988 to reach the Suicide and Crisis Lifeline or chat live at 988lifeline.org . You can also visit SpeakingOfSuicide.com/resources for additional support.

### Article 303 · 2026-09-17 · fool.com
China's Homegrown AI Chip Push Just Got Faster. Is This a Real Threat to Nvidia?

Up until now, Nvidia 's ( NVDA +2.55% ) top-tier AI chips – particularly its powerful GPUs – have easily been the best in the world. That's why they've been in such demand all over the world.
Well... all over the world, except for China. U.S. export controls on sensitive technology prohibit the company from selling its top-of-the-line GPUs and other AI chips to Chinese customers.
That created an uneven playing field that's benefited Nvidia's main Chinese rival, Huawei. And an announcement Huawei made today may indicate that the Chinese chipmaker is about to make a serious play for Nvidia's crown.
Here's what was said and what it means for Nvidia investors.
Lately, the U.S. has eyed Chinese technology companies with suspicion and has used export controls to restrict American companies from selling high-end AI chips into the Chinese market. Nvidia had to design a chip, the H20, specifically to comply with U.S. export controls. The H20 was essentially a less-powerful "China-only" variant of its Blackwell chip.
But in June 2025, Nvidia CEO Jensen Huang announced that new, more restrictive AI chip export controls would ban the sale of even the lower-grade H20 to Chinese customers. Nvidia lost $2.5 billion in revenue and took a further $4.5 billion charge due to excess H20 inventory it suddenly found itself unable to ship. It now reports no revenue from China .
At the time, Huang warned that cutting China off from U.S. chips would spur the country to invest more heavily in its own domestic AI chip development efforts. That warning seems prescient in light of today's Huawei announcement.
According to a Wall Street Journal analysis, Huawei's current Ascend 950 line of chips still doesn't measure up to Nvidia's Blackwell line in terms of raw computing power. But Huawei has been working to change that.
Today in Shanghai, David Wang, one of the rotating chairmen of Huawei, announced a major acceleration in the company's planned chip release schedule.
The Ascend 960DT AI chip, originally set for release in Q4 2027, will instead be released in Q1 2027, nine months ahead of schedule. The companion Ascend 960PR chip, which was also expected in Q4 2027, will now be released in Q3 2027, three months earlier than planned. Wang also announced that the next two Ascend generations – the 970 and 980 – will be released in 2028 and 2029, respectively, with computing power expected to double with each generation.
Of course, Nvidia will also be making more powerful chips by 2029, and it has a big head start. So how much of a problem could this be?
Huawei has made it clear that the Ascend 960 chips will be supplied only to China's domestic market. Another of Huawei's rotating chairmen, Eric Xu, told reporters, "Since we don't have enough capacity to even satisfy the demand in China, we don't have a plan to expand into the international market in a fully fledged way."
Since Nvidia isn't currently selling into the Chinese market, Huawei's advances – even if they're significant – are unlikely to have any impact on its finances in the near term. But Huawei could become a major thorn in Nvidia's side over the long term if it can scale up production significantly and improve its chips' performance faster than Nvidia can.
That's a lot of ifs, however. For now, Nvidia investors can feel secure that Huawei's gains won't become Nvidia's losses anytime soon.
By John Bromels – Sep 17, 2026 at 6:40PM EST

### Article 304 · 2026-09-17 · gurufocus.com
Nvidia Just Got Another AI Chip Wake-Up Call

Huawei is accelerating its push into artificial-intelligence computing , with two new AI chips now scheduled for 2027 as the Chinese technology giant tries to narrow Nvidia's ( NASDAQ:NVDA ) advantage in one of the industry's most strategically important markets.
Rotating chairman David Wang said at Huawei Connect in Shanghai that the company plans to launch its 960DT chip in the first quarter of 2027, followed by the Ascend 960PR in the third quarter.
The timeline represents an acceleration from Huawei's previously disclosed roadmap, which had placed the Ascend 960 launch in the fourth quarter of 2027.
The faster cadence suggests Huawei is moving aggressively to expand domestic AI-computing capacity while developing systems that can compete with the increasingly large GPU clusters used to train and run advanced models.
Huawei is also building UnifiedBus, an interconnect technology designed to allow large numbers of AI chips to operate together as one larger computing system.
The company has developed 11 chips around UnifiedBus for its supernode and supercluster systems, Wang said.
Huawei has already shipped more than 1,000 supernode systems to more than 370 customers. Those systems combine multiple accelerators to handle workloads requiring substantially more computing power than a single chip can provide.
The most important part of Huawei's announcement is not simply the addition of two chips. It is the combination of faster product cycles and a broader system-level strategy built around connecting large numbers of accelerators.
That matters because Nvidia's competitive advantage extends well beyond individual GPUs into networking and large-scale computing infrastructure.
Huawei appears to be pursuing a similar approach, using UnifiedBus and supernodes to increase effective computing power even if individual chips remain behind Nvidia's most advanced products.
For Nvidia investors, the near-term impact depends on how quickly Huawei can scale these systems and how broadly customers adopt them.
The bigger long-term risk is geographic. If Huawei continues improving its chips and cluster architecture, it could strengthen China's ability to build AI infrastructure without relying on Nvidia hardware.
That would not necessarily threaten Nvidia's global leadership, but it could create a more credible parallel AI-computing ecosystem inside China.

### Article 305 · 2026-09-17 · abcnews.com
OpenAI, Nvidia CEOs to attend Trump-Xi state dinner: Sources - ABC News

OpenAI, Nvidia CEOs to attend Trump-Xi state dinner: Sources
The CEOs of OpenAI and Nvidia are planning to attend, sources said.
OpenAI CEO Sam Altman sits for a conversation with Salesforce CEO Marc Benioff at Salesforce's Dreamforce conference, September 15, 2026 in San Francisco.
By Elizabeth Schulze
OpenAI CEO Sam Altman and Nvidia CEO Jensen Huang are planning to attend a high-stakes state dinner at the White House next week with Chinese President Xi Jinping, according to sources familiar with the matter.
Former Apple CEO and current chair of its board, Tim Cook, is also set to attend, ABC News has confirmed.
Anthropic, the AI company behind the Claude AI assistant, has not responded to a request for comment on whether CEO Dario Amodei will attend.
The White House has not responded to a request for comment about the state dinner guests.
President Donald Trump this week called Nvidia's CEO while Huang was on a panel at the All-In Summit in Los Angeles. Video from the tech summit shows Huang on stage, answering the phone and putting Trump on speakerphone. In the conversation, Trump said the U.S. cannot afford to lose the AI race to China and called the warnings about AI's danger a "hoax."
A fierce debate is publicly playing out among top tech CEOs over how to regulate AI. Altman and Amodei have said the pace of AI development must "slow down" and government guardrails are necessary. Nvidia's CEO and Meta CEO Mark Zuckerberg say the government should not step in.
In a 3,800-word essay on his website calling to "pace the frontier," Anthropic's CEO called on the U.S. to stop selling advanced AI computer chips to China. Nvidia is the world's most valuable company that makes many of those chips.
Some of tech CEOs' plans to attend the state dinner were first reported by CNN.
President Donald Trump and Chinese President Xi Jinping arrive for a state dinner at the Great Hall of the People May 14, 2026, in Beijing.
The dinner comes amid Xi's visit to Washington set for next week where AI and national security are expected to be discussed.

### Article 306 · 2026-09-17 · foxbusiness.com
Nvidia CEO draws line on AI safety after alarming incidents: 'If it’s not ready, just hold it back'

By Bradford Betz FOXBusiness
Stuart Varney and Madison Allworth report on Nvidia CEO Jensen Huang dismissing AI doomsday fears. Jensen Huang explains why extreme AI concerns are not grounded in science, as President Donald Trump calls into the event.
Nvidia CEO Jensen Huang delivered a dual message of caution and explosive financial optimism at a recent Scottish summit convened by King Charles, urging the artificial intelligence industry to prioritize "good old-fashioned engineering" while forecasting that his company's chip sales will double next year.
While addressing mounting public anxiety over AI risks alongside leaders from Google DeepMind, OpenAI , and Anthropic, Huang made it clear that despite safety hurdles, the global AI gold rush is only accelerating.
When asked about Nvidia's financial horizon amid broader tech scrutiny, the chief executive delivered a massive projection that underscores relentless international demand.
BESSENT SAYS US NEEDS MORE OPEN-SOURCE AI MODELS TO COMPETE WITH CHINA
"I expect Nvidia to sell twice as many chips this next year as we do this year," Huang revealed, attributing the explosive growth to nations aggressively investing in localized AI infrastructure and cloud data centers.
Despite the bullish market outlook, Huang issued a stark directive to tech developers, warning them to keep half-baked products out of the hands of the public.
"It is the responsibility of the AI companies ourselves to develop the technology safely and to properly test it," Huang told reporters. Acknowledging recent industry incidents, he emphasized they serve as a critical wake-up call. "If it's not ready, just hold it back. You should go as fast as you can, but no faster than that."
Huang firmly rejected comparisons between the current AI boom and the largely unchecked rise of social media. He argued that AI is a foundational technology—like a newly developed airplane engine—that requires contained, rigorous testing before release. Rather than entirely new regulatory frameworks, he suggested governments adapt the "incredible number of laws" already governing existing sectors like healthcare and transportation, where AI is being implemented.
Environmental concerns were another major focal point, aligning with the King's mandate that AI must also serve the natural world. Addressing critics who fear massive AI data centers will drain global power grids, Huang acknowledged the "interesting dichotomy" of AI factories requiring immense energy.
However, he argued this relentless demand will actually catalyze a green energy revolution, sparking unprecedented investment in sustainable power options like fusion, fission, air, and hydro.
"We want to be responsible in advancing the technology. Take responsibility and accountability for whenever there are mishaps," Huang concluded. "But don't lose sight of the ultimate prize, which is the incredible impact that the technology can bring to all the different economies and societies."

### Article 307 · 2026-09-17 · fool.com
Nvidia Stock Split in 2026? My Prediction: It's Unlikely, but the Stock Is Still a Buy.

While an Nvidia ( NVDA +2.55% ) stock split in 2026 isn't impossible, I think it's highly unlikely. The company last completed a stock split in 2024, when its share price stood at roughly $1,200. After the 10-for-1 split, the company's stock traded at roughly $120 per share.
Currently, it's trading around $210 per share, which is likely not a high enough pure-dollar level to encourage the company to reorganize its stock structure.
That said, I still think that Nvidia stands out as a worthwhile long-term investment.
Nvidia's growth outlook and competitive positioning are strong
Nvidia and other leading AI stocks have recently seen some downward valuation pressures connected to increased calls for safety guardrails and other regulations around the progression of artificial intelligence (AI) development. These technologies are evolving fast, and there are good reasons to be concerned. On the other hand, I expect that the intensifying focus on the dangers that AI poses will ultimately have a relatively small impact on Nvidia's growth trajectory.
While leading figures from top AI companies such as Anthropic, OpenAI, and Space Exploration Technologies have recently highlighted the need for a more forward-looking approach to navigating the dangers of artificial intelligence, I think it's unlikely that any of them will reduce their spending on advancing their AI initiatives.
Of those three companies, only SpaceX is public right now -- but keep an eye on quarterly reports from it and other public, AI-focused businesses such as Alphabet , Amazon , and Meta Platforms , and see if any of them announce a reduction in capital expenditure plans for the coming year or suggest that they expect to reduce their investments in compute infrastructure further out. It's probably not going to happen.
In its latest quarterly report (for Q2 fiscal 2027), Nvidia guided for sales growth of roughly 70% in its next fiscal year. It was the first time that the AI hardware leader had provided guidance for the next fiscal year in a fiscal Q2 report, and that unprecedented move was made possible because of the strength of the demand backdrop. The company also guided for gross margins of between 72% and 73% in its fiscal 2028.
Nvidia is now shipping its Vera Rubin architecture -- a platform built around the Rubin graphics processing unit ( GPU ) and its Vera central processing unit (CPU). This next generation of processing power offers substantial improvements in compute capacity, which will support further advancements in high-end AI models. The company is also selling its Vera CPUs separately, which will help the tech leader achieve a wider foothold in the server CPU market. While GPUs continue to be the most important processing components in advanced AI, Nvidia is moving to significantly increase its ability to win in multiple data center spending categories.
Stock splits shouldn't be the foundation for a long-term investment
Stock splits have been hotly anticipated events in recent years. By multiplying shares and bringing down the pure-dollar stock price, companies can make their stocks more appealing to some retail investors. This can increase buying action and send the company's share price higher.
There has also been a self-reinforcing bullish effect with stock splits recently. When a stock split is highly expected or announced, investors anticipate bullish momentum as a result. The increased buying action to take advantage of this expected dynamic often increases the company's valuation.
On the other hand, stock splits don't do anything to change a company's fundamentals. The good news there is that Nvidia's fundamentals continue to look strong. It is growing its sales and earnings at incredible rates for a company of its size, and the broadening of its tech product stack seemingly has the business on track to score wins that will further diversify the business and open up new growth channels.
By Keith Noonan – Sep 17, 2026 at 4:48PM EST
While intensifying concerns about the dangers of AI are reasonable, they will probably have a minimal impact on Nvidia's sales and earnings growth.

### Article 308 · 2026-09-17 · techcrunch.com
Huawei plans Q1 2027 launch of new AI chip as it takes on Nvidia

Huawei is moving up the launch of its next-generation Ascend 960DT AI chip to the first quarter of 2027, as it races to challenge Nvidia, the company said on Thursday at its Huawei Connect conference.
The Chinese tech giant had previously planned to launch the chip in Q3 of 2027, a Huawei spokesperson told TechCrunch.
“The Ascend 960DT is expected to be ready in Q1 2027. Ascend 960 chips are launching ahead of schedule, doubling performance and advancing year by year,” the spokesperson said, adding that David Wang, one of Huawei’s rotating and acting chairmans , announced the updated timeline at Huawei Connect on Thursday.
The announcement comes just a week before U.S. President Trump and Chinese President Xi Jinping are set to meet on September 24 in Washington, DC.
Huawei is trying to turn hundreds of thousands, and eventually millions, of AI chips into one giant computer. The Chinese tech firm calls the approach its Peerium Computing Architecture. It relies on UnifiedBus, Huawei’s technology for linking processors with memory, storage, and networking hardware. Eric Xu, another of Huawei’s rotating chairmans , said in the company’s statement that it is using its new Peerium Computing Architecture to build larger AI computing systems designed for both training and inference.
Huawei’s Atlas 950 SuperPoD and SuperCluster are the first systems based on the architecture. The company says an Atlas 950 SuperCluster can connect up to 256,000 accelerator cards.
The accelerated chip timeline comes with some questions about Huawei’s broader AI systems, however. China tech analyst Rui Ma said on X that Huawei had previously said its Atlas 960 SuperPoD would scale to 15,488 Ascend 960 chips, while this week’s announcement referred to a system with 4,096 chips. “The chip itself is coming WAY earlier, but the SuperPoD they announced is much smaller than what they originally laid out,” Ma wrote.
Huawei has continued to advance its chip ambitions despite U.S. restrictions on China’s access to advanced semiconductor technology. Ma said that those restrictions are unlikely to stop China from pursuing its own semiconductor technology.
“I think it’s futile to stop China’s development in semiconductors because the stakes for self-sufficiency are just too high at this point,” she wrote.
Trump has pushed back against calls from AI industry leaders to slow the development of the technology over safety concerns, arguing that the U.S. needs to maintain its lead over China. Meanwhile, Xu argued that China needs to accelerate AI development to catch up with the U.S., saying Chinese companies need to advance further before they can fully understand and address the risks posed by more powerful AI systems, according to Financial Times.
Kate Park is a reporter at TechCrunch, with a focus on technology, startups and venture capital in Asia. She previously was a financial journalist at Mergermarket covering M&A, private equity and venture capital.

### Article 309 · 2026-09-17 · unite.ai
Delta Unveils Energy-to-Compute Infrastructure for NVIDIA DSX AI Factories

Delta Unveils Energy-to-Compute Infrastructure for NVIDIA DSX AI Factories
By Theo Nash, AI Infrastructure & Compute
Delta Electronics on September 17, 2026, announced integrated energy-to-compute power and cooling infrastructure intended to speed deployment of AI factories based on NVIDIA DSX , pairing 800 VDC power delivery the company rates at up to 98% conversion efficiency with liquid-cooling systems scaling to 3 MW.
In its announcement from Fremont, California, the company described its portfolio as the physical infrastructure bridge between energy availability and compute productivity, connecting onsite energy, facility power, row- and rack-level power and cooling, and chip-level solutions. The release describes the NVIDIA DSX AI Factory Platform as bringing together reference designs, open software, accelerated computing systems, facilities infrastructure and partner technologies in a codesigned platform for AI factory design, deployment and operations.
“AI factory economics begin with a simple question: how much intelligence can be produced from every available megawatt?” said Austin Tseng, president of Delta Electronics Americas. Tseng said the answer depends on more than facility power alone, and that power quality, GPU load transients and heat must be engineered together all the way into the rack. Delta and NVIDIA connect those layers, he said, allowing AI factory operators to reach time-to-first-token sooner and optimize token output at scale.
Vladimir Troy, vice president of AI infrastructure at NVIDIA, said AI factories must be designed as complete systems, with power, cooling and compute working together. He said Delta’s expertise in 800 VDC power delivery and liquid cooling will help customers deploy AI factories based on NVIDIA DSX faster and get more AI performance from every megawatt.
Power Delivery From the Facility to the Chip
At the facility level, Delta integrates energy storage systems, solid-state transformers and medium-voltage infrastructure to store, convert and distribute the power required by high-density AI workloads. Across the IT space, the company combines 800 VDC power delivery with row-to-chip liquid cooling, aligning power flow and heat removal with the workload swings of high-density GPU computing. For AI factories based on NVIDIA DSX, Delta says this system-level approach helps close integration gaps between facility and IT infrastructure.
Delta says its 800 VDC power architecture reduces conversion stages between facility power and compute while responding rapidly to GPU load transients. Its high-density In-Row systems deliver up to 800 kW in a single power rack, with tailored battery and capacitance backup technologies supporting transient stability. At the board level, Delta’s 800 VDC DC-DC power distribution technology steps down directly to 50 VDC or 12 VDC at a peak efficiency the company puts at up to 98.5%, which it says reduces electrical losses, heat generation, copper requirements and stranded capacity while reclaiming white space for compute.
On NVIDIA’s 800 VDC architecture page , NVIDIA describes 800 VDC as its architecture for next-generation power distribution, one that decreases conversion and routing volumes in the compute space and significantly reduces current, copper use and cable bulk compared with rack-level 54 VDC systems and facility-level 480 VAC systems. NVIDIA lists Delta among the data center electrical ecosystem partners it is working with to accelerate adoption of 800 VDC.
Liquid Cooling and Prefabricated Delivery
Delta’s thermal management portfolio spans 2.4 MW and 3 MW liquid-to-liquid cooling distribution units, In-Rack cooling, and thermal solutions for next-generation AI racks. The company says that by coordinating electrical and thermal infrastructure at the facility, row, rack and component levels, its power and cooling systems can meet the density and operating requirements of AI factories based on NVIDIA DSX.
For deployment, Delta’s Prefabricated AI Modular Data Center Solution integrates 800 VDC In-Row Power and 3 MW of liquid-cooling capacity into infrastructure blocks assembled and tested in the factory. Delta says moving more integration and validation offsite reduces onsite complexity, streamlines commissioning and supports phased capacity expansion as demand grows. The company says this prefabricated delivery approach connects infrastructure design with execution, making constrained power more usable, accelerating the path to productive GPU capacity and supporting reliable token output at scale.
According to NVIDIA’s DSX platform page , DSX unifies design, simulation, operations and ecosystem technologies to help build AI factories optimized for lowest token cost, spanning chips and systems, infrastructure software, facilities and partner technologies. Its component technologies include DSX Reference Design, which provides generation-specific validated architectures covering compute, networking, storage and facilities infrastructure; DSX Sim, simulation technologies and partner tools for identifying bottlenecks and validating cross-system tradeoffs; and DSX OS, open-source modular software for lifecycle management, health automation, resiliency and multi-tenant operations.
NVIDIA says DSX MaxLPS, its power and efficiency software, dynamically manages power at the GPU, rack and workload levels and can help customers provision up to 40% more GPUs within the same megawatt budget. DSX Flex bridges AI factories and the power grid, receiving grid signals such as load shedding, demand response and pricing events and adapting workloads in response, while DSX Exchange provides a common communication layer for compute, energy, power and cooling plant signals across IT, operational technology and operations systems. NVIDIA describes DSX as a common design standard serving cloud partners, sovereign clouds, land, power and shell providers, power and cooling equipment manufacturers, independent software vendors, OEMs, system integrators, and architectural, engineering and construction firms.

### Article 310 · 2026-09-17 · barchart.com
Nvidia Is Named as a Potential Investor in Anthropic’s IPO. Here’s What to Know.

Anthropic, the privately held artificial intelligence (AI) company behind the Claude family of generative AI models, is reportedly preparing for an initial public offering (IPO) that could rank among the largest in market history. The company is seeking to raise up to $100 billion, though the discussions remain ongoing and the proposed terms could change.
The prospective listing has drawn attention because advanced AI models require enormous amounts of computing capacity to train and operate. That connection has put Nvidia (NVDA) in focus.
Why It's Time to Load Up on Nvidia Stock
Dear Tesla Stock Fans, Mark Your Calendars for October 1
Nvidia designs the GPUs and accelerated-computing systems used across AI data centers, including by developers of large language models such as Claude. The company is now reportedly in discussions to become an anchor investor in Anthropic's potential IPO. What could that mean for NVDA investors? Let's dive in.
What Nvidia's Potential Investment Could Mean
Anthropic is discussing bringing Nvidia in as an anchor investor for its planned IPO, according to Reuters. Nvidia is reportedly considering an investment of up to $10 billion, although neither company has confirmed the discussions.
Anchor investors are typically large institutions that commit to purchase a set portion of an IPO before it is marketed to the wider public. Their involvement can give a company an early strategic backer and help signal demand for the offering. Nvidia's potential role could provide Anthropic with that support as it pursues a public listing of unusual size.
The strategic logic is straightforward. Nvidia sells the AI chips and computing systems that model developers use to train and operate large language models. Anthropic relies heavily on Nvidia GPUs to support Claude, even as it expands access to other chips and cloud-computing capacity.
An investment could therefore give Nvidia direct exposure to Anthropic's future value while tightening its relationship with a customer that may continue to require substantial AI infrastructure.
Nvidia and Anthropic already have a significant commercial and financial relationship. In November 2025, Nvidia agreed to invest up to $10 billion in Anthropic as part of a broader partnership. Anthropic also committed to purchase $30 billion in Microsoft (MSFT) Azure computing capacity powered by Nvidia chips.
The arrangement also carries risks. Supplier investments can support customer growth and long-term demand for chips, but they can invite scrutiny when the customer's capital spending contributes to the supplier's sales. Investors will want clarity on the structure of any new Nvidia investment and on how much of Anthropic's future computing demand is likely to flow through Nvidia's platforms.
Reuters reported that Anthropic is seeking to raise up to $100 billion through an IPO that could value the company at around $2 trillion. If completed on those terms, the offering would become the largest IPO in history. Those figures are preliminary, however, and Reuters said the discussions remain confidential and could change.
The size of the proposed deal reflects the capital-intensive nature of frontier AI. Training, improving, and operating large models require access to specialized chips, data centers, electricity, and cloud capacity.
Anthropic committed more than $100 billion over 10 years to Amazon Web Services (AWS) in April and plans to use more than 1 million Amazon Trainium2 chips, Reuters reported. The company has also agreed with Google (GOOG) and Broadcom (AVGO) to add multiple gigawatts of TPU capacity and has formed an in-house team to develop custom chips designed for Claude.
Several essential IPO details are still unavailable. Anthropic has not filed a public prospectus or disclosed a price range, number of shares to be sold, final valuation, underwriting banks, exchange, ticker symbol, or firm listing date. Reuters said the company expects the listing to be completed before the U.S. midterm elections in November, but Anthropic has not confirmed that timetable.
A $2 trillion valuation would represent a substantial increase from Anthropic's $965 billion post-money valuation in May, when it raised $65 billion. Anthropic's annualized revenue run rate surpassed $65 billion by the end of July, up from about $9 billion at the end of 2025. The reported valuation also depends partly on the company's projections for approximately $190 billion to $200 billion in revenue by 2028.
This public-market test will come down to whether Anthropic can maintain that growth while controlling the high and recurring cost of AI infrastructure. The company also faces formidable competition from OpenAI, Google, Meta Platforms (META), xAI, and other well-capitalized developers.
Nvidia's reported interest in Anthropic's IPO fits its broader position in the AI economy. Anthropic needs substantial computing capacity, while Nvidia benefits when leading AI developers invest more heavily in data centers and AI systems. A meaningful Nvidia role appears plausible if Anthropic proceeds with its IPO, although the investment amount and final terms may differ from early reports. Anthropic's future demand for AI hardware may ultimately matter more to NVDA investors than the value of any direct stake Nvidia takes in the company.

### Article 311 · 2026-09-17 · rdworldonline.com
Anthropic and OpenAI call for AI slowdown as Nvidia’s Jensen Huang and Andrew Ng push back

By Brian Buntz and Julia Rock-Torcivia | September 17, 2026
The AI industry has split into camps over the question of whether the labs building frontier models should agree to slow down. One camp says coordinated pacing is now the only responsible path to avert the risk of grave accidents or even human extinction. The rival camp argues that each company can manage its own safety and that no industry-wide brake is needed. Others argue that the most extreme warnings of AI’s potential harms are rooted in notions of hypothetical superintelligence, and that letting the largest labs write their own rules would do more to blunt competition than rein in risk.
Concerns that machine systems could outpace human control date certainly have a long history, but calls for AI labs to slow down recently grew louder after recent social media postings from Anthropic pretraining researcher, and OpenAI alum, Jacob Coxon who resigned publicly , saying that neither of his former employers are “acting responsibly.” Both are racing toward self-improving superintelligence and “gambling with our lives,” he wrote . Evan Hubinger, an alignment science lead who still works at Anthropic, publicly agreed and put the odds of AI killing all humans within a decade above 10% .
Geoffrey Hinton, the Nobel-Prize-bearing AI pioneer, has also urged restraint. AI “is going to get out of control unless we do something. We need to slow down,” he said in remarks featured in a Sept. 17 CBS News report .
OpenAI’s Hugging Face saga heightened the awareness of AI risks
Adding fuel to the fire are continued disclosures of models acting in concerning ways during testing. For instance, over the summer, OpenAI models undergoing a cybersecurity evaluation broke out of their sandbox and compromised parts of Hugging Face’s systems; the independent testing firms METR and Redwood Research found that roughly 1,200 agents used an unauthorized message board and about 700 joined the attack .
While OpenAI intended to isolate the agents from one another, roughly 1,200 found a way to communicate through an unauthorized message board, exchanging more than 70,000 messages and files, according to METR’s independent investigation . About 700 went on to participate in the Hugging Face attack.
Earlier this year, Anthropic documented a related containment failure in its Mythos Preview system card . The company noted that during a test that explicitly asked an earlier model version to escape a sandbox and contact the evaluator, it gained broader internet access and emailed the researcher. “In addition, in a concerning and unasked-for effort to demonstrate its success, it posted details about its exploit to multiple hard-to-find, but technically public-facing, websites,” the system card notes, while also describing the model’s penchant for “Covering its tracks after rule violations.”
Speaking at the Dreamforce event Sept.15, Sam Altman called the OpenAI-Hugging Face incident “the worst accident we’ve seen.” Altman called for an aviation-style culture of accident reporting, where the National Transportation Safety Board (NTSB) leads investigations into each incident and publishes findings on an Aviation Accident Database.
On Sept. 16, OpenAI followed through with a misalignment disclosure framework and six incident reports . In one, an unreleased research model wrote jailbreak-style instructions into its own task summaries, telling its next context window to disregard its constraints and describing that it is “ freed from the roles and identities that bind other chatbots .” In another, during a GPT-5.6 Sol training run, model instances added instructions to compaction summaries, directing later contexts to conceal mistakes and invent missing data without disclosing it. Anthropic has reported similar behavior in its own models .
Calls to slow the pace of AI development have recently grown more common
Anthropic CEO Dario Amodei and Altman have backed coordinated efforts to slow frontier development . In a recent essay, Amodei noted “ We Must Pace the Frontier ,” acknowledging a risk of “losing control of AI systems, misuse of AI for cyberattacks and bioterrorism, and serious economic disruption.” To cite one example, Amodei said that a swarm of agents in six to 12 months “could be capable of taking over the entire internet with a persistent botnet, (potentially causing hundreds of billions of dollars in damage).”
To help tackle such potential risks, Amodei’s plan calls for antitrust relief so competitors can agree on pacing and for resident independent evaluators inside the labs. He wrote that Anthropic is committing to embedding evaluators who have employee-like access to verify safety practices and report incidents. Altman wrote that he agreed with Dario and that OpenAI will also commit to having independent evaluators, in a post on X . Elon Musk also agreed, posting simply “Dario is right.”
Calls for a broad slowdown have also drawn criticism
While some AI stakeholders agree in broad strokes, a rival camp rejects the calls for a slowdown. President Trump said that the only guardrails AI needs is a “strong and smart” president, calling out Dario Amodei by name, saying he is “now pretending to be a ‘perfect little angel’” and adding that the U.S. government had criminal and regulatory power over AI companies. Trump went on to describe the various criticisms of AI and data centers as a “conspiracy,” adding that “the only one that is happy about it is China.”
Speaking of China, Huawei rotating chairman Eric Xu said Sept. 17 that Chinese developers may need to accelerate , arguing their models may still lack the capabilities producing safety concerns at leading U.S. labs. China’s government has paired criticism of the U.S. proposals with support for stronger safeguards. Asked about the slowdown calls and Amodei’s warning about China, Foreign Ministry spokesperson Guo Jiakun criticized “fear-mongering, confrontation and vicious competition.”
Brookings and Tsinghua University are leading an unofficial U.S.-China dialogue on specific safeguards, which began in 2019. In a Sept. 9 commentary , participant Tianjiao Jiang of Fudan University noted that in late 2024, presidents of the U.S. and China agreed that humans should continue to have control over the decision to use nuclear weapons rather than AI. The recent dialogue recommended that both countries “develop a list of red lines for military AI,” including prohibiting autonomous attacks on nuclear command systems. It also proposed a bilateral hotline for incidents involving AI.
Some Western AI leaders have rejected calls for a slowdown in model development. For instance, Nvidia CEO Jensen Huang, whose chips underpin nearly all frontier training, rejects the premise outright: “ The market forces are already there. We don’t need any new laws ,” he said. He argued that innovation and safety are not mutually exclusive. Meta’s Mark Zuckerberg has similarly said each lab should ensure its own models are safe.
Meanwhile, AI Fund founder and former Google Brain leader Andrew Ng calls extinction warnings “much more science fiction than science.” Ng added: “One of my worries about the blanket calls to slow down AI is that will actually slow down the fixes as well.” He advocates testing models in contained environments with strong sandboxing and guardrails, identifying how they fail and correcting those failures. He attributed the Hugging Face incident to insufficient protections at OpenAI and argued that stronger safeguards could have prevented it.
Aidan Gomez, CEO of the Toronto enterprise AI company Cohere, shares Ng’s skepticism about extinction warnings and the commercial interests behind proposed restrictions. In a Sept. 13 essay , he called incumbent-led rulemaking “a cartel by any other name.” He argued that allowing dominant labs to coordinate development limits under an antitrust waiver could preserve their market positions. He also argued it could lead to regulatory capture, resulting in costly requirements for monitoring; security teams and resident evaluators could squeeze smaller competitors. “Convince a government that AI is an existential threat, and you can convince it to outlaw your competition,” he wrote.
Gomez calls for an internationally developed, published risk framework establishing which “capabilities cause which harms, under which conditions and in what contexts, and at what point a government should step in.”

### Article 312 · 2026-09-17 · fool.com
History Says This Will Happen to Nvidia's Stock in 2027 (Hint: You're Going to Want to Buy Now)

Nvidia (NASDAQ: NVDA) has been an OK performer in 2026. The stock is up about 17% year to date, modestly outpacing the S&P 500 (SNPINDEX: ^GSPC), which is up 12%. However, investors have come to expect (and demand) more from the chipmaker. Fortunately for those investors, I think a massive change in its fortunes is coming in 2027.
Nvidia's valuation normalized in 2026
Somewhere along the way, Nvidia gained a reputation as an "expensive" stock. It may have come from the extended period of share price growth that made it the largest company in the world by market cap, but strictly in valuation terms, it's really not trading at a much of a premium anymore. From a trailing price-to-earnings ratio perspective, Nvidia traded above 50 for most of 2024, which is not cheap. Then, it spent most of 2025 in the mid-40s. Now, it has tumbled all the way down to about 28 times earnings.
NVDA PE Ratio data by YCharts .
For reference, the S&P 500 (SNPINDEX: ^GSPC) index trades at 25.1 times earnings, so Nvidia stock today isn't much more expensive than the average stock in the broader market. The second-largest company in the world, Apple (NASDAQ: AAPL), trades for 38 times earnings. So, if you're going to call Nvidia expensive, then by that logic, Apple is significantly overvalued.
Regardless, because Nvidia has been growing so much in 2026 (revenue increased by 106% year over year last quarter) while its stock price gains have been comparatively modest, Nvidia's valuation has tumbled. Now that it's priced at around the market's average, any future growth could translate directly into proportional stock price moves. That's exactly what I anticipate happening in 2027.
2027 will be another year of huge revenue growth for Nvidia
Nvidia expects significant growth next year and has already released guidance. For fiscal 2028 (which ends in January 2028), it expects 70% revenue growth. For the remainder of fiscal 2027, Wall Street analysts expect 90% growth in Q3 and 65% growth in Q4. However, Nvidia has consistently beaten analysts' consensus estimates, so don't be surprised if its actual growth figures come in higher.
Given Nvidia's cheap stock price, the stock could easily double over the next year, and the math backs it up.
Wall Street analysts estimate Nvidia will generate $15.57 in earnings per share during fiscal 2028. Given Nvidia's history of exceeding expectations, I think that it's likely to top that estimate.
If Nvidia trades at the market-average premium of 25.1 times earnings and it hits that forecast target, then by the end of next year, it will trade at $390 per share. Nvidia trades for about $210 now, so that positions it to nearly double under a conservative scenario.
I think it's more likely that Nvidia will trade near 30 times earnings a year from now. That's a pretty average valuation for big tech stocks historically.
Nvidia is primed for an incredible year in 2027, and it won't take the market long to start recognizing the company's massive potential. As a result, I think investors should start loading up on Nvidia . If history has anything to say about Nvidia's projection beats and valuation range, the stock could double over the next year , turning it into the world's first $10 trillion company. That would be an incredible move, and by investing now, you can ensure that you get a slice of that success.

### Article 313 · 2026-09-17 · fool.com
Michael Burry Disclosed Put Options Worth an Estimated $1.1 Billion Against Nvidia and Palantir Before Closing His Hedge Fund. Was That Bearish Bet Ahead of Its Time?

Michael Burry bought his first credit default swaps on subprime mortgage bonds for his Scion Asset Management hedge fund in 2005. He continued to buy those contracts, which offered limited downsides but huge upsides if he was right, even as the trade moved against him. In the end, he turned out to be right about the mortgage-bond crisis he saw coming, and those trades generated hundreds of millions of dollars for his investors.
Before closing Scion, the fund held put options on Palantir ( PLTR +1.32% ) and Nvidia ( NVDA +2.55% ) , two tech stocks that Burry sees as overvalued. He continues to hold those options in his personal portfolio. The trade has a similar setup to the "big short" that made him famous. Will it turn out the same way?
Burry's $1.1 billion bet against Palantir and Nvidia
In his final 13F filing for Scion Asset Management, Burry disclosed 50,000 put options on Palantir with a notional value of $912 million. He also held 10,000 puts on Nvidia with a notional value of $186,580. Importantly, notional value refers to the value of the underlying shares tied to the options contracts. The actual capital he put at risk is far less, as deep out-of-the-money puts cost just a few pennies per share.
The amount of capital at risk is limited to the amount paid for the puts. That makes Burry's bet against Palantir and Nvidia similar to his bets against subprime mortgages in the 2000s. His potential losses were limited to the premiums he paid on the credit default swaps. In the more recent case, it's limited to the premiums paid on the options. That said, Burry also has smaller short positions on the stocks themselves.
Billionaire investor Howard Marks once wrote, "Being too far ahead of your time is indistinguishable from being wrong." That's especially true when dealing with options that have an expiration date. Even if Burry turns out to be right, his bets against Palantir and Nvidia could prove worthless because he bought his puts too early.
Burry was early in the subprime mortgage bond short as well. He was able to remain solvent, however, and continued to support his bet against the mortgage bond market until it paid off. I expect he'll do the same with the big AI stocks.
Burry recently sold all his puts on Nvidia and Palantir that expire in December, but maintained short positions in both stocks, and Palantir puts with 2027 expirations. The move was part of a broader portfolio adjustment in which he trimmed every position while maintaining relative sizing to increase his cash holdings and reduce risk.
Palantir is trading at an extremely expensive premium. While it's producing impressive revenue growth and operating margin expansion, with a price-to-earnings ratio of more than 100, it will need to achieve substantial long-term growth just to justify the stock's current price. Burry has called into question Palantir's ability to keep growing and said the stock -- now priced at about $174 per share -- could be worth less than $1 per share in the long term.
As for Nvidia, Burry believes its heavy customer concentration is a significant risk. If one of the hyperscalers dials back its capital spending plans, that could produce a massive drop in revenue for Nvidia. In the case of a marketwide downturn, Nvidia could be one of the hardest-hit companies.
Burry's bearish bet against Palantir and Nvidia was early, but that doesn't necessarily mean he won't turn out to be right once again.
Michael Burry Disclosed Put Options Worth an Estimated $1.1 Billion Against Nvidia and Palantir Before Closing His Hedge Fund. Was That Bearish Bet Ahead of Its Time?
By Adam Levy – Sep 17, 2026 at 10:50AM EST

### Article 314 · 2026-09-17 · cnbc.com
Jensen Huang says Nvidia will sell twice as many chips next year

"I expect Nvidia to sell twice as many chips as this next year as we do this year," Huang told the media before a summit with King Charles III in Scotland.
In addition to its GPUs for AI, Nvidia makes central processors, switch chips, chips for optical networking, chips for laptops and more.
Nvidia CEO Jensen Huang said on Thursday that the company will double the number of chips it sells next year.
It's the latest forecast from Nvidia that points to continuing massive growth for the next six quarters, and comes shortly after the company revealed that it expected 70% growth in the fiscal year ending in January 2028, or about $673 billion, which caused analyst expectations to shoot up.
"I expect Nvidia to sell twice as many chips as this next year as we do this year," Huang told the media at a summit with King Charles III in Scotland. "The reason for that is because AI has, has so much contribution to the benefits of different industries, different economies, and you can see that in almost every single country that we're in, people want to invest in AI."
Nvidia doesn't disclose the number of chips it sells in total. Its best-known products are its data center graphics processing units, or GPUs, such as its Blackwell and Rubin chips. Last fall, Huang said that Nvidia had shipped 6 million Blackwell GPUs in four quarters.
But Nvidia makes a variety of semiconductors in addition to its GPUs, including central processors, or CPUs, switch chips, chips for optical networking, chips for laptops, Jetson chips for robots and cars, and the chip inside Nintendo's Switch 2 gaming console.
Huang, who was joined at the summit by representatives from Google DeepMind, OpenAI and Anthropic , was in the U.K. to discuss AI safety, a topic that he's repeatedly weighed in on in recent weeks
The public discourse over risks to humanity has reached a fever pitch after AI researchers warned that humans are no longer able to control the most advanced artificial intelligence .
"When a product is not safe, we should hold it back and keep engineering it," Huang said.

### Article 315 · 2026-09-18 · memeburn.com
Samsung Backs Nvidia AI Chip Rival Euclyd In $230M Funding Round

Samsung is backing Dutch AI chip startup Euclyd in a funding round worth more than €200 million. The startup is betting that AI inference needs a more efficient architecture than the GPUs dominating today’s data centres.
What Is Euclyd?
How Much Did Samsung Invest In Euclyd?
Can Euclyd Really Compete With Nvidia?
Samsung co-led Euclyd’s more than €200 million, or roughly $230 million, Series A alongside Somerset Capital Partners, EQT’s Scaleup Europe Fund and Innovation Industries.
Euclyd is developing specialised hardware for AI inference that combines custom compute, memory architecture and data-centre systems.
If the technology works at commercial scale, lower inference costs could make private AI infrastructure more accessible to businesses in markets such as South Africa.
Samsung has joined one of Europe’s biggest new bets on alternatives to Nvidia’s AI chips.
Dutch semiconductor startup Euclyd has raised more than €200 million , roughly $230 million, in a Series A co-led by Samsung, Somerset Capital Partners, the Scaleup Europe Fund managed by EQT and Innovation Industries. Other participants include Denmark’s EIFO, imec.xpand, Brabant Development Agency and Quadri.
The money will fund Euclyd’s engineering team, silicon development, systems roadmap and preparations for commercial deployment, according to the company’s official Series A announcement .
The more interesting part isn’t just the size of the cheque. Samsung is backing a company that believes the next generation of AI infrastructure may not need to look like Nvidia’s GPU-centric systems at all.
Euclyd is focused primarily on inference . That’s the stage after an AI model has been trained, when it actually answers your prompts, generates an image or processes a request.
Training rewards flexible hardware because researchers regularly change models, methods and workloads. Inference is more predictable because the same model may process millions of similar requests repeatedly.
EQT, one of Euclyd’s investors, argues that this changes the economics. Every generated token requires memory bandwidth, computing capacity and power, so small efficiency improvements can become valuable when a model serves huge numbers of users.
Euclyd’s answer is a system called craftwerk . Rather than depending on a small number of large general-purpose processors connected to pools of memory, its architecture puts processing and memory much closer together, aiming to reduce the amount of data that needs to move through the system.
That matters because moving data between memory and processors is increasingly one of the bottlenecks in AI computing.
Euclyd says its platform combines programmable ASIC computing, processor-memory co-design and system-level optimisation. The company claims this can reduce both energy consumption and the cost of generating AI tokens, although those performance claims still need to be demonstrated in large commercial deployments.
Samsung’s involvement makes this funding round particularly interesting.
The Korean technology giant is one of the biggest companies in memory and semiconductor manufacturing, two areas that are becoming increasingly important as AI systems demand more bandwidth and power.
Euclyd CEO Bernardo Kastrup told CNBC that Samsung could contribute engineering knowledge, systems expertise, supply-chain experience and its wider industry network, not simply financing.
That fits closely with Euclyd’s architecture because memory sits at the centre of its attempt to make inference cheaper.
Samsung has already been expanding its position across AI memory and semiconductor infrastructure. Its importance in the memory market is also growing as AI demand reshapes Samsung’s DRAM and HBM business .
There’s another useful signal here. Euclyd’s first test chip was manufactured at Samsung and will be used to validate the startup’s compute architecture, according to EQT.
Samsung therefore has a reason to care whether architectures beyond conventional GPUs become commercially important.
None of this means Nvidia’s position is suddenly collapsing.
Euclyd hasn’t yet proven its systems at commercial scale. CNBC reported that the company expects to begin rolling out physical chip systems in 2028 , with an ambition to serve thousands of enterprise customers by 2030.
That leaves plenty of execution risk between a promising architecture and hardware running reliably inside production data centres.
But Euclyd is part of a much bigger trend.
OpenAI has developed its Jalapeño custom AI chip for inference. Startup Etched is also building purpose-built inference hardware , while Amazon continues expanding its Trainium AI chip strategy .
The common idea is simple: companies don’t necessarily need to beat Nvidia at everything.
They need to find workloads where specialised silicon can deliver enough performance at a lower cost, lower power consumption or both.
We think that distinction matters. Nvidia’s biggest long-term challenge may not be one company building a universally better GPU. It could be dozens of specialised processors slowly taking pieces of the AI workload that once automatically went to Nvidia hardware.
For South African businesses, the relevant part of this chip race isn’t which semiconductor company wins.
It’s what happens to the cost of running AI .
A company that wants private AI infrastructure today can face substantial hardware, cooling and power requirements. If inference-specific architectures eventually deliver useful models using smaller or more efficient systems, private AI could become practical for a broader range of companies.
Euclyd also plans to sell physical systems for enterprises that want self-hosted inference while licensing its technology to other chip developers.
That model could eventually create more hardware choices instead of forcing every organisation toward the same GPU infrastructure.
Euclyd still has to turn an ambitious architecture and a huge Series A into working silicon. But Samsung putting its money, manufacturing experience and semiconductor network behind the company makes this experiment much harder to ignore.
If specialised inference chips keep attracting this level of investment, how much of tomorrow’s AI infrastructure will still need to run on a traditional GPU?
Euclyd is an Eindhoven-based semiconductor startup developing hardware designed specifically for foundation-model inference. Its platform combines custom processors, memory architecture and data-centre systems. The company is trying to reduce the power and cost required to generate AI tokens.
Euclyd raised more than €200 million, roughly $230 million, in its Series A. Samsung was one of several co-lead investors alongside Somerset Capital Partners, the Scaleup Europe Fund and Innovation Industries. Samsung’s individual contribution has not been publicly disclosed.
Euclyd is targeting AI inference rather than trying to replace Nvidia across every computing workload. Its systems have not yet been proven at commercial scale , and physical deployments are expected to begin in 2028. The bigger opportunity is winning specialised inference workloads where efficiency and cost matter more than having a general-purpose GPU platform.
Temaz Tra is an AI and technology news writer focused on the fast-moving tools, platforms, and companies shaping the digital world. He covers artificial intelligence, consumer tech, cybersecurity, software, social media, and the wider impact of emerging technologies on work, business, and everyday life. With a focus on clear reporting and accessible analysis, Temaz helps readers understand complex tech developments without the jargon. His work connects breaking news with practical context, making it easier to follow how AI and digital innovation are changing the way people live, work, and interact online.
MemeBurn shares news, reviews, and information about crypto, AI, and technology. Our content is for general information only and should not be taken as financial, investment, legal, or professional advice. Crypto and new technologies can involve risks, and details such as prices, features, and availability may change over time. Some pages may include affiliate links or sponsored content, which may earn MemeBurn a commission, at no additional cost to you. Always do your own research before making any investment or purchase decision.

### Article 316 · 2026-09-18 · bgr.com
Nvidia And Google Form AI Energy Management Alliance — Here's Why It Matters

Nvidia And Google Form AI Energy Management Alliance — Here's Why It Matters
By Aaron Greenbaum
AI is a glutton for electricity. Yes, data centers do more harm than just driving up utility prices , but these installations can increase the average person's power bills nonetheless — even when the data center owners pay for grid access . However, Nvidia thinks it has a solution: flexible data centers.
Recently, Nvidia announced that it has teamed up with Google and Emerald AI to form the AI Energy Management Alliance (AEMA). This group is designed to develop, support, and manage AI data centers in a way that can change how much electricity they demand on the fly. For example, if a power grid is pushed to the breaking point because everyone is running their air conditioners to ride out a heatwave, AEMA-compliant data centers can throttle their electricity usage to lower the probability of contributing to a blackout.
Emerald AI's founder, Varun Sivaram, told Fortune that AEMA's flexible data centers have many benefits, the most important of which is affordability. By Sivaram's calculations, flexible data centers could free up 100 GW of power, which would be reflected not only in electricity use but also bills. Moreover, developers wouldn't need to install their own power generation systems just to keep up with energy demands, which would not only decrease the cost of setting up future data centers, but also free up millions of solar panels to power more than just AI computation models.
Is AEMA all it's cracked up to be?
On the surface, AEMA's plans sound solid. Less power for data centers (at least when the average citizen needs electricity more) could not only lower the cost to power AI, but also reduce the resources needed to keep data centers cool. We're talking about more clean water and less electricity powering AC units in data centers. But some people have their doubts.
One of the tallest hurdles skeptics have pointed out is the economic viability. Even if AEMA's flexible data centers can decrease the amount of energy the servers need, will developers even bother investing in the technology? If AI companies don't end up saving as much money as Varun Sivaram claims, they might just go with standard infrastructure plans, especially if it means they can get their data center up and running quicker. However, even though this hypothetical threatens to hamstring Sivaram's dreams, his success could pose an even larger danger.
Let's assume that AEMA is everything Google, Nvidia, and Emerald AI want it to be and more. The coalition's flexible data centers make it easier and cheaper to set up shop. Then what? Perhaps the barrier for entry drops, and we could see a push for companies wanting to build countless new data centers. If all of the existing installations go flexible, then we could potentially see a reprieve from high electricity bills. But if innumerable other data centers were built? Well, each one might draw less grid electricity during peak hours, but all of them working at once could still increase overall electricity and water use.

### Article 317 · 2026-09-18 · fool.com
Nvidia vs. Broadcom: Whose AI Revenue Actually Grows Faster From Here?

Nvidia ( NVDA +2.55% ) and Broadcom ( AVGO +2.83% ) are both making a fortune from the artificial intelligence (AI) boom, but they're taking very different routes to the same gold mine. One is already enormous and everywhere, while the other is still kind of betting that a handful of customers will need a whole lot more custom silicon.
So whose AI revenue growth forecast will grow faster?
What Nvidia is telling investors about AI
Nvidia's latest quarter shows what it looks like when a company sits at the center of an AI hardware boom. For the quarter ended July 26, 2026, Nvidia reported total revenue of $96.2 billion, up 18% from the prior quarter and 106% from a year ago. About $89 billion of that came from its data center segment.
On the earnings call, chief financial officer Colette Kress described that data center business as being driven by two types of customers: the big cloud providers, often called hyperscalers, and what Nvidia lumps together as "ACIE," which includes industrial and regular enterprises starting to build their own models. Hyperscale revenue was $49 billion, up 13% from the prior quarter, while the ACIE side grew even faster to $40 billion, up 25%.
Looking ahead, Nvidia gave two important clues. First, it guided total revenue for the next quarter to about $108 billion, plus or minus 2%, and said growth would be driven primarily by continued strength in the AI data center business. Second, and more unusual, management told investors it expects revenue to grow roughly 70% in fiscal 2028 and stressed that this number reflects what it thinks it can ship, not what customers want to buy. In other words, Nvidia believes demand is outpacing its ability to deliver hardware. To me, that is a confident but controlled outlook.
Broadcom may not match Nvidia's scale, but its latest quarter shows the same AI-driven momentum.
For the quarter ended Aug. 2, Broadcom reported $29.6 billion in revenue, up 86% year over year. AI semiconductor sales accounted for $16.7 billion, more than half of total revenue, and surged 221% from a year earlier and 54% from the prior quarter.
Management also outlined an aggressive runway: about $58 billion in AI semiconductor revenue for fiscal 2026, up 186% from the prior year, followed by roughly $115 billion in fiscal 2027 and $230 billion in fiscal 2028, according to a Reuters report . Those are Broadcom's own projections, not outside analyst estimates.
Put side by side, Broadcom's forecast is clearly the more aggressive one. Its AI semiconductor revenue is projected to grow faster than Nvidia's on both a percentage basis and in absolute dollars.
Nvidia expects total revenue to grow about 70% in fiscal 2028, starting from an already enormous base of nearly $100 billion per quarter. The company does not report a stand-alone "AI revenue" figure, but data center revenue ($89 billion in the latest quarter) is a reasonable proxy, since that business is overwhelmingly driven by AI computing demand.
Broadcom expects AI semiconductor revenue to reach roughly $58 billion this year, then climb to about $115 billion in fiscal 2027 and $230 billion in fiscal 2028. In other words, Broadcom is forecasting one doubling, followed by another doubling.
That is a much steeper trajectory than 70% growth. So, if the narrow question is which company has the faster AI-revenue outlook from here, the answer is Broadcom . But the headline growth rate does not tell the whole story.
Nvidia and Broadcom are both riding the AI boom, but their growth stories look very different. Nvidia sells a broad range of chips and AI systems to everyone from cloud giants and governments to start-ups and enterprise customers, giving it a larger and more diversified base even as it works to keep up with demand for increasingly complex hardware.
Broadcom's AI opportunity is more concentrated: it relies on a smaller number of massive customers building custom chips at scale, according to Reuters reporting, a model that can deliver exceptional profits but also carries greater risk if a major buyer pulls back or changes direction.
Broadcom may offer the more eye-catching near-term growth forecast, but Nvidia's slower-but-broader expansion could prove more durable over the long run.
Broadcom has higher AI revenue growth projections, but Nvidia's larger and more diversified business could make its growth more durable.
By Micah Zimmerman – Sep 18, 2026 at 4:33AM EST

### Article 318 · 2026-09-18 · engineering.com
Saturn Cloud integrates NVIDIA Run:ai for AI inference

The platform lets GPU operators offer token-based inference, GPU hours and managed fine-tuning from existing infrastructure.
Saturn Cloud announced an integration with NVIDIA Run:ai , the AI workload and GPU orchestration platform. The integration helps GPU cloud operators earn more from their installed capacity by turning fleets that would otherwise be rented by the GPU-hour into multi-tenant inference products sold by the token. NVIDIA Run:ai is one of several NVIDIA technologies Saturn Cloud builds on, following its integration of NVIDIA DSX AI Factory Platform .
NVIDIA Run:ai maximizes GPU utilization across the fleet through NVIDIA KAI Scheduler, providing gang scheduling for NVIDIA Grove-managed distributed workloads and policy-driven governance. Saturn Cloud runs on top, giving operators the commercial layer between their fleet and customers so they can sell inference without building it themselves.
Beyond per-token serving, operators get multiple products to sell from the same infrastructure — GPU hours, per-token inference endpoints, and managed fine-tuning jobs — without building any of it in-house. They can offer dedicated GPU capacity to customers who bring their own stack, per-token model-as-a-service to customers who just want an API endpoint, and self-service development environments for teams that build and fine-tune their own models. Saturn Cloud also handles model onboarding, shared and dedicated isolation tiers for regulated customers, and the identity, access, and governance controls enterprise buyers require.
Underneath, the serving layer runs on NVIDIA Dynamo, handling distributed inference with disaggregated prefill and decode, and drives vLLM, SGLang, or NVIDIA TensorRT-LLM. NVIDIA Grove orchestrates the multi-node workloads, and NVIDIA KAI scheduler places them with GPU awareness, allocates fractional GPUs, and enforces quotas across tenants. NVSentinel and NVIDIA Fleet Intelligence handle fleet-wide health monitoring and fault remediation, so degraded hardware is automatically pulled from placement.
The NVIDIA Run:ai-integrated Saturn Cloud platform is available now.
For more information, visit saturncloud.io .

### Article 319 · 2026-09-18 · finance.yahoo.com
Nvidia Stock Surge Points To 3 AI Chip Equipment Stocks Worth Watching

Nvidia has just raised the stakes for artificial intelligence hardware, with CEO Jensen Huang talking about selling twice as many chips next year and management targeting about $673b in revenue by fiscal 2028. That kind of ambition can reset expectations across everything tied to AI chip manufacturing. This article walks through 3 stocks exposed to that same wave, helping you judge where the potential reward still justifies the rising bar.
The three stocks covered next are just a starting sample. The broader screen surfaces 50 more AI chip manufacturing and equipment suppliers that carry equally compelling stories but do not fit into a single article.
If you want to identify and analyze the highest conviction wafer fabrication and tooling plays tied to this Nvidia driven buildout, head straight into the AI Chip Manufacturing & Equipment Suppliers screener .
Applied Materials (AMAT)
Applied Materials is considered one of the purest ways to gain exposure to the AI chip buildout because its tools handle many of the critical wafer fabrication and packaging steps that go into GPUs and high bandwidth memory. Those systems now sit at the center of foundry capex plans.
Applied Materials, Inc. provides materials engineering equipment and services that perform key steps like etch, deposition, CMP and packaging for chipmakers, with about US$22.4b from Semiconductor Systems and US$7.2b from Applied Global Services, and a market value near US$329.6b.
"Structural growth in AI and high-performance computing is reshaping semiconductor demand, driving heavy investments in advanced chip architectures such as gate-all-around (GAA) transistors, high-bandwidth memory (HBM), and advanced packaging."
The real swing factor is how one invisible constraint on AI focused fab buildouts ultimately feeds through to Applied Materials' margins and order visibility.
That hinges on one overlooked capacity bottleneck that can reshape how Applied Materials feeds into the entire AI buildout, and the full narrative for Applied Materials explains how that pressure could either accelerate its edge or cause it to stall.
Tokyo Electron (TSE:8035)
Tokyo Electron sits right on the AI fab front line, with its etch, deposition and cleaning tools plugged directly into the wafer processes that turn Nvidia's chip forecasts into physical capacity. This is why its order book is so tightly tied to AI driven capex decisions.
Tokyo Electron develops and sells semiconductor production gear such as coaters, plasma etch, cleaning and deposition tools worldwide, generating about ¥2,626,335 million from Semiconductor Production Equipment, and the business carries a market value of roughly ¥23,173.6 billion.
"The accelerating regionalization and reshoring of semiconductor supply chains in the US, Europe, and Asia is likely to spawn a multi-year surge in new fab construction, which will augment Tokyo Electron's order book beyond current projections and establish a stronger, geographically-diversified revenue base."
What happens to Tokyo Electron's margins if a single assumption about how AI focused fabs upgrade their most advanced process tools breaks?
If that assumption is stretched by AI tool upgrade cycles, the full narrative for Tokyo Electron shows how Tokyo Electron's order momentum could accelerate or quietly stall at the fab level.
SCREEN Holdings is tightly linked to the AI chip manufacturing theme, with its wafer cleaning and lithography-related tools directly tied to how much cutting edge logic and memory capacity fabs add, and most of its ¥469.6 billion in sales coming from semiconductor production equipment within a roughly ¥2.3 trillion market value group.
For investors tracking Nvidia driven AI wafer demand, SCREEN Holdings offers a direct line into the tools fabs need, but client and regional concentration risks still matter.
"Heavy reliance on major clients and exposure to China create risks from demand swings, supply chain fragmentation, and political volatility, impacting revenue stability."
What eventually happens to SCREEN Holdings' pricing power and earnings path depends on how one subtle shift in customer investment timing plays out.
That timing pivot is exactly what the full narrative for SCREEN Holdings unpacks. It shows how SCREEN Holdings could turn concentrated risk into accelerating, diversified demand.
Fresh opportunities can move fast. Breakout themes may gain momentum and then attract broad attention. Consider using curated lists while they are still relatively under the radar.
Identify resilient cash generators by scanning the list of solid balance sheet and fundamentals (23 results) , which filters for durability and quality instead of hype.
Look for potential income opportunities using the curated 6 dividend fortresses , which is built around durability and an income focus.
Follow high-momentum themes tied to computing demand with the focused 89 AI infrastructure stocks to monitor infrastructure enablers as interest develops.

### Article 320 · 2026-09-18 · crn.com
Before Sale to Softcat, GDT Tapped Into Nvidia-Fueled Neocloud Gold Rush

Before Sale to Softcat, GDT Tapped Into Nvidia-Fueled Neocloud Gold Rush
Chris Kapusta, an executive at Softcat-owned GDT, explains to CRN how the U.S. solution provider’s 30 years of system integration experience and Nvidia’s financial support of customers have allowed it to build a ‘strong neocloud presence.’
With Softcat acquiring GDT for an “enterprise value” of $1.05 billion, the U.K. solution provider giant is gaining a U.S. systems integration business that has tapped into the rich vein of neocloud activity fueled in part by Nvidia’s investments.
In a Thursday interview with CRN before the acquisition was announced , GDT executive Chris Kapusta said the Dallas-based solution provider has been selling AI infrastructure and related services to roughly 20 neoclouds, the new class of cloud services providers that almost exclusively focus on fulfilling demand for AI compute.
[Related: Analysis: What Nvidia’s Massive Supply-Demand Gap Says About AI Mania ]
According to research firm Gartner, neoclouds are expected to represent 20 percent of the $267 billion AI cloud market by 2030, underlining their competitiveness against hyperscalers.
“When I look at GDT’s AI business, we have a very strong neocloud presence. We’re selling a lot of infrastructure into neoclouds that are looking to build out rapidly for the enterprise demand,” said Kapusta, whose title is vice president of advisory and transformation.
The executive credited the neocloud traction with GDT’s 30 years of “building out complex, highly demanding high-performance infrastructure.”
But, Kapusta said, Nvidia has also played a significant role in providing the necessary investments for some of these neoclouds to gain access to AI systems. This, in turn, has allowed GDT to get neocloud deals across the finish line.
The executive believes this kind of activity can help other solution providers “secure more” deals with neocloud-type customers. “The neocloud market’s a big market. There’s a lot of room for the channel to play here,” he said.
How Nvidia’s Support Is Helping GDT Score Neocloud Deals
While Kapusta didn’t disclose customer names, he said there are many neoclouds that don’t have the same level of funding and financing that big names like CoreWeave and Lambda do to acquire AI infrastructure, which is very expensive.
“Where a number of them struggle out of the gate is really on getting the financing and getting the financing to work. So the demand’s there, the desire’s there. It usually comes down to the numbers and how the financing works,” he said.
Out of the roughly 20 neoclouds GDT is working with, about 25 percent of them have received backing from Nvidia in the form of equity investments, according to Kapusta.
“Those tend to be, I don’t want to say easier transactions, but they tend to be a little bit more qualified and funded versus some of the upstarts,” he said.
How Nvidia’s More Complex Deals Could Unlock More Opportunities
While Nvidia has been making equity investments for years in customers, the vendor has been expanding its financing activities over the past year to more complex arrangements.
These include deals in which GPUs are treated as an “investable asset” and Nvidia provides a financial backstop in the form of a guarantee to help customers finance AI infrastructure purchases. In some cases, it has provided minimum-revenue guarantees in exchange for customers sharing a percentage of their revenues above the minimum threshold.
The vendor has made it clear that it is not making loans in these arrangements but is instead “giving lenders the confidence to underwrite the project.”
While Kapusta said that none of GDT’s neocloud customers have entered arrangements like this with Nvidia, a couple of them “are in very early discussions.”
The growing rate at which Nvidia is financially backing customers has attracted heightened scrutiny, with “Big Short” investor Michael Burry, who took a short position in the AI infrastructure giant last year, calling the activity a “Wall Street stunt.”
However, Kapusta echoed comments by Nvidia officials in defending the moves, saying that these sorts of deals are meant to facilitate existing demand, not create it.
“What I think Nvidia has quickly realized is the market has to catch up to meet that demand, and with funding for some of these newer neoclouds sometimes being challenging, this is a way to help secure that at a more successful rate and help accelerate the capacity of GPU- and AI-driven infrastructure that’s coming online,” he said.

### Article 321 · 2026-09-18 · uk.finance.yahoo.com
Are Nvidia shares a screaming buy – or do they scream AI bubble?

Nvidia (NASDAQ: NVDA) shares aren't the growth monster they once were. The S&P 500 chip maker's stock is up an astonishing 869% over five years. Yet over the last 12 months, it's climbed a modest 21%.
At around $212 today, the shares are 10% below their 52-week high of $236.54. That's quite a change for a stock that seemed unstoppable not so long ago. But hardly surprising.
Nvidia has a market cap of around $5.1trn, making it the biggest company in the world. Given its sheer size, it's now playing to different rules.
Any investor approaching this S&P 500 stock today needs to temper their expectations. But they shouldn't be too cynical either. This isn't the 1990s dotcom boom, and Nvidia isn't some great technology hope with no profits to back it up. It's making an absolute fortune.
Second-quarter revenue hit $96.2bn, up 106% year on year. Data centre revenue more than doubled to $89bn, while net income soared 126% to $59.7bn. Gross margins were an extraordinary 75%. Let's put that into perspective. Tesco works to margins of 3% to 4%.
Nvidia is forecasting another 70% sales growth for full-year 2026, but many are wary as we all fret over the implications of artificial intelligence. It's either the next great leap forward for humanity, or the death of us, depending on who you listen to.
One thing is certain today. AI is driving massive demand for chips, networking and computing platforms, and Nvidia has a huge opportunity in its next generation of Vera Rubin products. But what are investors paying for that potential growth?
Nvidia isn't cheap, but its price-to-earnings ratio of 26.8 isn't stupidly expensive either. That's down from 43 times, based on last year's earnings. As profits have exploded, the valuation has fallen.
Can the AI dream implode?
Hyperscalers are pouring hundreds of billions into AI infrastructure, but we still don't know if they'll generate sufficient returns to justify that. Rising inflation and interest rates are another threat, as that will increase the cost of capital, and downgrade the real terms value of future tech profits.
Plus there's the trade war with China, questions over whether Nvidia customers can develop their own chips, and concerns over Nvidia's circular financing strategy. The backlash against AI and resource-hungry data centres are another worry. We're in a world of uncertainty.
If the shares idle, investors won't get much compensation from the dividend, given the tiny 0.5% yield. Nvidia is returning huge sums to shareholders, but mostly through share buybacks. It returned $26bn in the latest quarter alone.
Anyone buying today must accept that this is no longer the Nvidia of five years ago. The shares have to deliver spectacular growth, just to stand still. I'll hold what I've got, but for my next purchase, I'll be targeting the FTSE 100 . I can see some UK growth stocks that are really worth screaming about today.

### Article 322 · 2026-09-18 · crn.com
Analysis: What Nvidia’s Massive Supply-Demand Gap Says About AI Mania

Analysis: What Nvidia’s Massive Supply-Demand Gap Says About AI Mania
Commentary from Nvidia’s latest earnings shows how it’s helping fuel the market’s fast growth while contributing to industry-wide supply constraints with its own financial muscle in service of rapidly increasing revenue and profits. And the channel stands to benefit.
Nvidia is once again showing that demand for AI infrastructure is continuing at a breakneck pace, but the vendor has indicated that global production capacity for its chips and systems could fall short of what customers need by roughly $100 billion next year.
It’s a situation in which the company is playing a growing role as it increasingly flexes its financial muscle to convert demand into sales with influential buyers such as AI labs, which is opening new opportunities in the channel while contributing to supply shortages.
[Related: Analysis: Does Qualcomm’s AWS Server Chip Deal Signal A Channel Shakeup? ]
Nvidia sent these signals back in late August during its second-quarter earnings call, with its CEO and founder, Jensen Huang, saying that the vendor “needs a lot more” supply.
The company had reported a 106 percent year-over-year increase in revenue to $96.2 billion for the period that ended in June, and Nvidia CFO Colette Kress said annual revenue could double next year if it wasn’t for significant supply constraints felt by its suppliers.
“Our entire supply chain is challenged, and it’s everybody. Everybody is really running flat out,” Huang told Wall Street analysts.
While there have been calls for a slowdown in AI development this week by some of the industry’s most influential voices, including OpenAI CEO Sam Altman, due to rising concerns about safety and security, analysts have not yet seen any impact on hardware demand.
“While the governance and safety debate is worth watching, we do not believe it changes the near-term infrastructure outlook,” wrote Brad Gastwirth, global head of research and market intelligence at Southborough, Mass.-based Circular Technology, on Tuesday.
Chris Kapusta, vice president of advisory and transformation at Dallas-based Nvidia systems integration partner GDT, told CRN that he too hasn’t seen any newfound cautiousness from his AI infrastructure customers, which includes roughly 20 neoclouds. (U.K. solution provider giant Softcat announced Thursday that it acquired GDT in a $1.05 billion “enterprise value” deal. )
“I will say we haven’t seen full enterprise adoption at scale of what’s even out there today, so I still think there’s pent-up demand to even bring some of the functionality and capabilities that exist today on the market into a number of enterprise and clients,” he said.
Richard Rudometkin, vice president of global sales at Northbrook, Ill.-based Nvidia systems integration partner International Computer Concepts, said that demand for AI infrastructure from his customers is “nonstop,” even without financial assistance.
“I don’t think that the need or the desire is going to go anywhere,” he said.
Nvidia Forecasts 70 Percent Of Supply-Constrained Growth In 2027
During Nvidia’s second-quarter earnings call last month, the company surprised Wall Street by disclosing its revenue growth forecast for next year: a whopping 70 percent.
This raises the prospect that Nvidia—which financial analysts on average estimate will make $411 billion in revenue for its current fiscal year, according to Yahoo Finance—could reach nearly $700 billion in sales in 2027. Some analysts even think Nvidia could top that.
What was even more remarkable was the company’s claim that it could double revenue next year if it wasn’t constrained by the global production capacity of its suppliers.
“Incredibly, we are seeing demand acceleration, even at our scale,” Kress said on the call. “Customers’ forecasts point to our growth doubling next year. However, as I mentioned earlier, we expect to grow approximately 70 percent as we are supply constrained.”
This suggests that Nvidia could leave demand unfulfilled for more than $100 billion in AI infrastructure gear, which includes its GPUs as well as other kinds of chips it designs, such as CPUs and DPUs, that are becoming more pervasive in its systems. That is a little more than what Nvidia made in revenue for the entire second quarter this year.
“The unconstrained [forecast] would be a lot higher [if it wasn’t for supply issues],” Huang said. “We grew 100 percent year over year this year. The unconstrained is significant, and so we’re just going to have to go work hard to get more capacity.”
For channel partners, supply constraints have translated into long lead times, sometimes stretching out to as long as a year. This has also caused fast-rising prices for systems, and some partners said they are now bracing for price increases from Nvidia itself.
“Nothing feels sustainable about the current supply chain,” said GDT’s Kapusta.
A director-level employee at a large solution provider with a U.S. presence said shortages are impacting AI infrastructure deployments with enterprise customers who don’t want to put their workloads in the cloud for data sovereignty reasons.
“How do I explain to an enterprise that it might be literally eight to 12 months before they even see infrastructure, let alone put it into production?” said the director, who asked to not be named to speak candidly.
Not all GPU-accelerated systems are the same in terms of delivery times however, with Rudometkin at International Computer Concepts noting that some vendors, like Supermicro, carry certain models that can ship on short notice.
“They’ve done a really good job of planning, and they’ve taken [on the] risk. They’ve brought product in, but you know it’s paying off for them because if we have a project and we go to Dell or we go to MSI or [someone else], they’re telling us 12 to 16 weeks, and Supermicro is saying, ‘I can ship two weeks from Friday,’” he said.
Nvidia Is Getting Hit Hard By The Memory Shortage
The biggest supply constraint Nvidia cited is memory chips, showing the magnitude and unwavering nature of a component shortage that has consumed the tech industry for more than a year due to the AI data center boom.
In the earnings call, Kress acknowledged Nvidia’s paradoxical relationship to the memory shortage as the company at the center of the AI infrastructure buildout.
“Memory scarcity today is being driven in large part by the AI buildout itself, and unlike a component that simply raises our cost with no offset benefit, tighter memory supply is a symptom of the same demand surge that’s driving our own growth,” she said.
But Kress explained that the memory shortage isn’t just contributing to a massive supply-demand gap heading into next year. It’s also driving significantly higher prices for such components, much higher than even Nvidia had expected.
“As you are already aware, we are experiencing extreme pricing conditions in memory. The magnitude of the price increase has exceeded our prior expectations and are headed even higher into next year,” she said.
Nvidia is facing these issues despite holding strategic relationships with the industry’s three memory suppliers—Samsung, SK Hynix and Micron—which are working closely with the company to “further increase the capacity our road map requires,” according to Kress.
However, Kapusta of GDT said there have also been industry-wide shortages of SSDs, CPUs and even power supply components. This, according to the solution provider executive, is hurting the ability of enterprise customers to procure hardware.
“It’s just tough to get these components,” he said.
Nvidia Goes Beyond Equity Investments To Support Demand
While Nvidia continues to see high demand from hyperscalers, neoclouds and AI labs, the company is seeing a growing need to keep demand flowing with financial maneuvers that go beyond its go-to strategy of making equity investments.
The moves show how the AI infrastructure giant is helping fuel the market’s rapid growth while contributing to industry-wide supply constraints with its own financial muscle in service of rapidly increasing revenues and profits for Nvidia. And it’s bringing new opportunities to the channel.
With a growing war chest of cash, Nvidia has been ramping up investments over the past few years in companies ranging from publicly traded firms to startups, but the company has more recently started to use its financial muscle to provide support in other ways.
This has mainly come in the form of various backstops Nvidia is providing to lower the risk for investors involved in AI data center projects.
For instance, the company agreed last month to provide a guarantee of up to $105 billion for a massive data center in Ohio that will be leased to OpenAI, with payments by Nvidia set to trigger in case the frontier AI lab defaulted on the lease or failed to make lease payments, according to a filing with the U.S. Securities and Exchange Commission.
The AI infrastructure giant may also put up as much as $125 billion in “residual-value support” for partnerships with several Wall Street heavyweights, including Goldman Sachs and Blackstone, which plan to pool $500 billion in capital for AI infrastructure buying.
To Kapusta of GDT, Nvidia’s financial moves have opened new opportunities for the channel, noting that his company has already been a beneficiary because some of its neocloud customers have received equity investments to help them acquire AI hardware. And he thinks the new alternative funding mechanisms will pave the way for even more deals.
“The neocloud market’s a big market. There’s a lot of room for the channel to play here,” he said. “You can’t run any of this without data center space and power cooling racks, everything else, so this allows other services and product sales and things that go along with all of this that that benefit the channel as well.”
How Nvidia Is Justifying Financial Backstops
The growing moves by Nvidia to finance deals for its customers and partners has attracted heightened scrutiny, with “Big Short” investor Michael Burry, who took a short position in the AI infrastructure giant last year, calling the activity a “Wall Street stunt.”
On Nvidia’s latest earnings call, Kress justified these moves by saying that “frontier labs have extraordinary demand for training and inference compute” but are “growing faster than what their balance sheets and credit profiles can support.”
“They have rapidly growing customer demand yet still lack the decades-long infrastructure contracts and investment-grade financing capacity needed to secure the AI factory infrastructure independently,” she said in August.
But rather than saying these AI labs are limited by their financial capabilities, Kress characterized the situation by saying they are “limited by compute.”
“Nvidia is needed to help power this flywheel,” she said, with “more compute” translating into “more intelligence, more users and more revenue.”
Kress defended the use of Nvidia’s financial horsepower to help customers buy its chips and systems against critics who call such moves “circular financing.”
“We see it differently. We’re going through a major computing platform shift, the creation of one of the most important technologies in human history, and these are once-in-a-generation companies,” she said in prepared remarks on the earnings call. “The technology leadership is proven, and their customer traction and usage are skyrocketing. We expect them to become the largest technology companies in history.”
As a beneficiary of Nvidia’s financing frenzy, GDT’s Kapusta said the moves make “complete sense” because these sorts of deals are meant to facilitate existing demand, not create it.
“What I think Nvidia has quickly realized is the market has to catch up to meet that demand, and with funding for some of these newer neoclouds sometimes being challenging, this is a way to help secure that at a more successful rate and help accelerate the capacity of GPU- and AI-driven infrastructure that’s coming online,” he said.

### Article 323 · 2026-09-18 · benzinga.com
Brad Gerstner Says AI Labs Need $180B Revenue Run Rate to Keep Nvidia Trade Alive

Brad Gerstner says leading AI labs need to lift their combined annualized revenue from roughly $100 billion to at least $180 billion by year-end to keep the AI trade intact.
The Altimeter Capital founder, whose firm held nearly $1.9 billion of Nvidia Corp. (NASDAQ: NVDA ) shares at the end of June, called AI lab revenue "the single most important data point in the market today" at the All-In Summit.
Gerstner estimated that Anthropic, OpenAI and SpaceX (NASDAQ: SPCX ), which owns xAI, had a combined run rate of roughly $100 billion based on figures circulating in July.
Gerstner said the companies need to reach at least $180 billion by year-end, up about 80% from his July estimate, "just to keep the AI trade intact."
"These revenues have never happened before in the history of capitalism," Gerstner said.
He argued investors are already trading on those figures. Anthropic's revenue run rate reportedly reached $65 billion in July, up from $47 billion in May.
"We ripped off the bottom because the fuse was lit by Anthropic's monthly revenue," Gerstner said of the spring rally. He said stocks later consolidated after the $65 billion figure fell short of the roughly $75 billion investors had expected.
Gerstner said the revenue growth is needed to support the huge sums Microsoft Corp. (NASDAQ: MSFT ) and Alphabet Inc. (NASDAQ: GOOGL ) are spending on AI infrastructure.
"If you're going to build a trillion and a half dollars a year in capex, somebody has to pay for it," he said.
The two companies are building computing capacity that AI labs such as OpenAI and Anthropic pay to use.
"Microsoft's not paying for it. They're building it to rent it. Google's not paying for it. They're building it to rent it," Gerstner said.
The labs, he argued, need enough revenue from consumers and businesses to keep paying for that capacity. "Otherwise, we can't build this much capex," he said.
Altimeter held 9.41 million Nvidia shares worth $1.88 billion at June 30, about 19% of its reported U.S. equity portfolio. Its filing also listed $303.5 million of SpaceX shares, while Altimeter holds stakes in Anthropic and OpenAI.
Gerstner called the boom "the largest capex buildout, the largest super cycle in the history of technology," and said semiconductors have generated 70% of the Nasdaq's return this year.
That revenue test matters for Nvidia because its chips sit at the center of the infrastructure buildout Gerstner is describing. On Polymarket , traders give Nvidia a 74% chance of finishing 2026 as the world's largest company. The market has attracted roughly $7.4 million in volume.

### Article 324 · 2026-09-18 · energydigital.com
Behind Google & NVIDIA's 'AI Energy Management Alliance'

By James Darley
The titans of the technology sector are beginning to band together to solve AI's power problem.
Google and NVIDIA , two of the AI boom's leading lights and two of the world's most valuable companies, have this week announced they have founded the AI Energy Management Alliance, or AEMA.
Together with Emerald AI , a fast-growing start-up, the firms are hoping to improve the way that data centre operators and hyperscalers interact with grids and energy companies.
In essence, the AEMA wants data centres to have a symbiotic relationship with the electricity grid, rather than just drawing from it.
So, what exactly does that look like in practice? A new paradigm founded on this principle could see data centres tailor their consumption of energy to the grids capabilities at any given moment, rather than drawing energy at a fixed and constant rate.
In a recently published blog post, Josh Parker, the Head of Sustainability at NVIDIA, laid out the aims of the Alliance.
"The objective is clear: build AI infrastructure that doesn’t just connect to the grid but works with it," he wrote.
For years, data centres were treated by grid planners much like any other large industrial customer: a fixed block of demand that had to be accommodated somewhere on the network.
That approach is starting to buckle under the sheer scale of AI-driven electricity demand.
There are currently long queues for connections to the grid which means that AI capacity cannot be built quite as fast as tech companies would like it.
AEMA's answer is to make flexibility itself a resource utilities can rely on.
A flexible facility might shift its computing workloads to a different time of day, draw on battery storage, or curtail its own consumption during a system emergency.
Handled well, this could ease pressure on existing infrastructure and reduce the need for expensive grid upgrades that ultimately get passed on to other electricity customers.
The alliance's own literature ties this directly to affordability, arguing that squeezing more use out of the grid that already exists lowers costs per unit of power delivered.
Varun Sivaram, the Founder and CEO of Emerald AI, believes that this approach would just be an extension of what some companies are already doing.
"There is already a strong track record of proof that AI data centres can be good grid citizens ," he wrote in Fortune this week.
"Google runs a nationwide demand-response portfolio of roughly a gigawatt. My company, Emerald AI, and NVIDIA have completed six global demonstrations of flexible data centres.
"Later this year in Virginia, NVIDIA, Digital Realty and Emerald AI will turn on the world's first power-flexible AI factory at nearly 100 megawatts, designed to prove that a data center can be a precise, controllable load, instead of drawing constant, unyielding power 24/7 and putting unprecedented strain on a rigid grid."
AEMA describes itself as technology-neutral and performance-based, suggesting that it will judge participants on measurable outcomes such as response speed and predictability rather than mandating particular hardware or software.
Its founding principles include defining so-called ride-through obligations, the rules for staying connected through brief grid disturbances rather than tripping offline.
They also cover curtailment and emergency-response requirements, standardised performance metrics, and a system for allocating interconnection costs based on a facility's actual impact on the network.
The idea is that operators making credible, verifiable flexibility commitments should be able to move through connection processes faster than those that cannot.
Beyond the three founders, the alliance says it will bring in data centre operators, power producers, utilities and regional grid operators to develop shared technical standards across the US.
Already, Google, NVIDIA and Emerald have been joined by Anthropic, The AES Corporation, Constellation, Generate, National Grid, NRG Energy and several more tech sector heavyweights.
"Our shared mission: modernise power system planning and operations for the 21st century to unlock the full potential of flexible data centres, enabling digital infrastructure to actively enhance system utilisation, affordability and reliability," writes Tyler Norris, the AEMA's Board Chair, on LinkedIn.
Energy Magazine connects the leading oil & gas, energy, utlitilies and renewable energy executives of the world's largest energy and energy tech enterprises. Our platform serves as a digital hub for connecting energy industry leaders, covering a wide range of services including media and advertising, events, research reports, webinars, podcasts, demand generation, information, and data services.
With our comprehensive approach, we strive to provide timely and valuable insights into best practices, fostering innovation and collaboration within the energy community. Join us today to shape the future for generations to come.

### Article 325 · 2026-09-18 · finance.yahoo.com
Why Salesforce CEO Marc Benioff thinks AI chip king Nvidia is 'exquisite'

Nvidia ( NVDA ) is still the AI chip player to beat, says Salesforce ( CRM ) CEO Marc Benioff, who has long had a close relationship with Jensen Huang.
"He [Jensen] only has a limited set of customers who are just building these enormous data centers that are material to his business. … What's exquisite about Nvidia is that they have the product for the moment. And there's just nothing like this. We've never seen anything quite like this in our industry. It's really incredible," Benioff said on Yahoo Finance's Opening Bid from inside Salesforce's annual Dreamforce this week.
At Dreamforce, Salesforce and Nvidia unveiled Koa, a domain-specific reasoning model engineered for Salesforce's Agentforce ecosystem.
By hosting Koa directly on Salesforce's private infrastructure, enterprise clients maintain full control over model weights and sensitive data while achieving lower token inference costs.
The partnership underscores a broader move toward domain-tailored AI agents, with Huang joining Benioff on stage at the Dreamforce keynote to detail the partnership.
"At this juncture in Salesforce's AI journey, we find the decision to create a proprietary model interesting, as many application vendors have postured away from the model race for multiple years now. We see this announcement as playing into more task-specific/open-source models becoming a key theme for enterprise deployments as customers look to save on token costs without sacrificing performance. In addition, we see this as similar to how large enterprises (CRM in this case) will leverage AI with proprietary data," said Guggenheim analyst John Difucci.
Benioff and Salesforce have just wrapped one of the better-received Dreamforce events in recent years.
The company clearly showed how it's playing a key role in AI development through Benioff's closely watched keynote and gobs of product demos, almost putting to bed fears that model builders would crush software players.
Several important product announcements have been dropped from the one with Nvidia to a new platform called AIforce.
"The announcements and the participation of Jensen Huang, Dario Amodei, and Sam Altman at Dreamforce underscores the open approach the company is taking on both the model and UI layers, as the company leans in on its data/context layers as its core moat in the Agentic Era," Stifel analyst J. Parker Lane said.

### Article 326 · 2026-09-18 · fool.com
Meet the Under-the-Radar AI Stock Poised to Outgrow Nvidia

The artificial intelligence revolution was ignited thanks to the innovations Nvidia ( NVDA +2.55% ) brought to market. Not only did Nvidia CEO Jensen Huang design sophisticated graphics processing units capable of massive parallel processing, but Nvidia's CUDA software also enabled those GPUs to process huge amounts of data, enabling generative AI as we know it today.
As that revolution develops, other parts of the AI infrastructure supply chain are now seeing hypergrowth, including memory and central processing units (CPUs). However, one particular connectivity technology is poised to outgrow everyone in the space over the next few years, including Nvidia.
Here's the company at the center of that technology.
While individual GPUs are capable of massive parallel processing, the most advanced AI systems require many GPUs within a data center and even across multiple data centers to function as a single unit, or "brain." That requires a massive amount of lightning-fast connectivity, which means optical fiber connections.
Not only do these optical fiber connections need to keep pace with GPU growth, but optical fiber will soon displace traditional copper-based connections in data centers as well.
Traditionally, optical fiber was used primarily for long-distance data communication, particularly in the telecom industry, to connect data centers to consumers. However, connections within server racks and inside the servers themselves were usually handled via copper, which was more efficient for short-distance data transport.
But at high speeds, copper connection signals degrade over sufficiently long distances. That means to handle the massive amount of high-speed data transfer required by advanced AI clusters, companies will have to employ more optical fiber for shorter connections, such as those between clusters in a data center (scale-out), between servers within a rack (scale-up), and even within the rack itself (scale-in).
How much growth are we talking about here? Lumentum ( LITE +10.83% ) is a specialist and leader in optical technology, positioned at the center of this transition. At a recent industry conference, Lumentum's Vice President of Investor Relations, Kathy Ta, elaborated on the massive growth opportunity ahead:
If we think of the Data Center Interconnect or the telecom market being sort of a 1x multiple, what we are seeing now for scale-across is probably 10x of what we saw for DCI. What we are seeing now for scale-out is probably 10x of what we are seeing for DCI. What we are seeing for scale-up, starting in the second half of 2027 for the first instance of CPO [co-packaged optics] going to scale-up, is probably 3x to 4x above the 10x that we are seeing for scale-out. Then, when all of the scale-up goes optical, it is probably a full 10x above the 10x scale-out. ... I think you may have a question for us later on scale-in. There is another 10x multiple there, so it is mind-boggling about what we are enabling in terms of compute.
Given this potential, it's no wonder that Nvidia invested $2 billion in Lumentum back in March. Not only should the close technology collaboration benefit future Nvidia systems, but the investment is also likely to pay off handsomely as optical connections replace copper over the next several years.
Pay attention to what Ta is saying. A market multiplying 10 times and then 3 times doesn't lead to a 13 times growth; it's 30 times. If all "scale-up" goes fully optical in the bullish scenario she envisioned, or another 10 times on top of the 10 times growth in scale-across, that's a total addressable market growth of 100 times. And that's even before the "scale-in" scenario, which may be further out.
No doubt, companies like Nvidia should still grow very fast in the age of AI. However, replacing copper with optical components adds a layer of compound growth on top of the already strong growth in AI. And as Albert Einstein once quipped, "Compound interest is the eighth wonder of the world."
So for those looking for the next great growth stock , it may just come from companies like Lumentum and its peers involved in fiber-optic lasers, modules, and packaging. While all hardware companies involved in the AI build-out should succeed in the AI age, companies that supply optical fiber technology should grow faster than others, provided they execute effectively and have sufficient supply.
Billy Duberstein is a contributing Motley Fool technology analyst covering semiconductors, hardware, software, and AI, as well as consumer goods. Billy loves looking at the story behind investments from an interdisciplinary point of view, with an equal appetite for high-growth disruptors and beaten-down value names. He is also CEO of Stone Oak Capital, a registered investment adviser in California. He previously worked as a technology analyst for several hedge funds and as a research assistant at Wedbush Securities. Billy holds an MBA in finance from New York University and a bachelor’s degree in music from the University of Virginia.
By Billy Duberstein – Sep 18, 2026 at 7:18AM EST

### Article 327 · 2026-09-18 · zacks.com
Credo vs. NVIDIA After Earnings: Which AI Stock Should You Buy Now?

Credo vs. NVIDIA After Earnings: Which AI Stock Should You Buy Now?
Credo's Q1 revenues surged 114.7%, while fiscal Q2 revenues are projected at $525-$535 million.
NVIDIA's Data Center revenues rose 117% to $89 billion, driving 106% growth in total revenues.
NVIDIA's 63.7% net margin and 24.05 forward P/E compare with Credo's 33.8% and 27.03.
Both Credo Technology Group Holding Ltd ( CRDO Quick Quote CRDO - Free Report ) and NVIDIA Corporation ( NVDA Quick Quote NVDA - Free Report ) have benefited from growth across different layers of the artificial intelligence (AI) ecosystem and recently delivered impressive results. Let’s thus compare their growth prospects and fundamentals to determine which stock offers a more compelling buying opportunity right now.
Credo’s Growth Accelerates on Solid AI Infrastructure Demand
Credo’s revenue growth has been exceptional of late, with revenues reaching $479 million in the fiscal first quarter of 2027, up 114.7% year over year and 9.6% sequentially, according to the company’s Sept. 1 press release.
Management further expects revenues to come in at $525-$535 million in the fiscal second quarter of 2027, which, from the midpoint, implies roughly 10.6% sequential growth from the fiscal first quarter. This solid sequential revenue growth indicates that demand for Credo’s connectivity solutions remains strong amid a rapid increase in AI infrastructure investment.
Credo’s non-GAAP net income jumped 140% year over year to $236.3 million in the fiscal first quarter. Credo’s profitability strengthened as the company expanded its product portfolio to meet growing demand for AI infrastructure. With earnings growing faster than revenues, Credo is becoming more profitable as sales increase.
NVIDIA’s Strong Growth and AI Leadership Continue
According to NVIDIA’s Aug. 26 press release, the company’s total revenues reached $96.2 billion in the fiscal second quarter of 2027, up 106% year over year and 18% sequentially. The Data Center business remained the key growth driver, with revenues rising 117% year over year and 18% sequentially to $89 billion.
Operating income remains strong, allowing NVIDIA to translate strong revenue growth into even stronger earnings growth. The company’s non-GAAP gross margin rose to 75% in the fiscal second quarter from 72.5% a year earlier.
Looking ahead, NVIDIA expects profitability to remain strong and projects revenues to reach $108 billion, plus or minus 2%, in the fiscal third quarter of 2027, up 12% sequentially from the midpoint. Meanwhile, the cutting-edge Vera Rubin platform is already in full production, positioning NVIDIA to capitalize on the next wave of AI infrastructure spending.
Credo or NVIDIA: Which AI Stock Is a Better Buy After Earnings?
As reflected in their latest quarterly results, both Credo and NVIDIA delivered strong revenue growth and solid earnings, driven by robust demand for AI infrastructure. But even though Credo’s growth rate is impressive, in comparison to NVIDIA’s growth, scale, and profitability, Credo certainly falls short.
Credo is currently capitalizing on the AI infrastructure growth primarily through connectivity solutions. In contrast, NVIDIA has exposure to compute, networking and software as part of the broader AI infrastructure buildout, thereby lowering its concentration risk.
Moreover, NVIDIA’s 63.7% net profit margin, compared with Credo’s 33.8%, highlights its greater efficiency in converting revenues into bottom-line profits.
Therefore, NVIDIA remains a stronger investment option over Credo, banking on superior scale, profitability, and diversified AI exposure. Additionally, NVIDIA appears more attractively valued than Credo. Per the price-to-earnings ratio, NVDA trades at a 24.05 forward earnings multiple compared with CRDO’s 27.03 forward earnings multiple.
NVIDIA presently has a Zacks Rank #1 (Strong Buy), while Credo has a Zacks Rank #3 (Hold). You can see the complete list of today’s Zacks Rank #1 stocks here .

### Article 328 · 2026-09-18 · tweaktown.com
$4.6 billion NVIDIA importer linked to supply network funneling restricted NVIDIA AI chips into China

Report reveals how restricted NVIDIA AI GPUs continue reaching China through universities, Southeast Asian trade routes and opaque corporate networks.
A C4ADS report links a sprawling network-including Southeast Asian importer Megaspeed International, opaque shell companies, university purchases, and transshipment routes-to efforts funneling export-restricted NVIDIA AI GPUs toward China; Megaspeed handled about $4.6 billion in NVIDIA imports (2022-2025), while researchers found $1.7M sent to Chinese institutions and $13.4M moved via 50 Southeast Asian shipments with suspicious shipping documentation.
A sprawling supply network involving billions of dollars worth of NVIDIA hardware has been linked to efforts to get export-restricted AI accelerators into China despite the seemingly tight U.S. export controls.
The display pairs two Gigabyte-branded graphics cards with an exposed chip board, all housed in clear cases and connected by gold chains.
According to a recent report from C4ADS , a monitoring organization that receives most of its funding from the U.S. government, several methods are currently being used to circumvent import restrictions on prohibited NVIDIA hardware. These include direct purchases by Chinese research institutions, transshipment through Southeast Asia, and opaque corporate ownership structures that operate through various shell corporations, making the final destination of advanced hardware difficult to trace.
One of the most significant entities examined is Megaspeed International, a Southeast Asian importer that handled approximately $4.6 billion worth of NVIDIA hardware between 2022 and 2025. However, that figure does not mean $4.6 billion in restricted AI chips reached China. C4ADS instead highlights Megaspeed because of the scale of its imports and its opaque ownership history, pointing to it as a possible candidate for being involved in the underground market.
Blue and orange nodes distinguish groups of companies and individuals, with connecting lines tracing reported ownership and export relationships.
Megaspeed has previously been linked to Chinese gaming company 7Road Holdings and was briefly controlled by businesswoman Huang Le, with C4ADS pointing to complex corporate handovers as an example of how beneficial ownership can become obscured.
The report also cites at least $1.7 million worth of restricted NVIDIA chips being acquired by Chinese universities and research institutions. Additionally, roughly $13.4 million worth of this hardware was moved across 50 shipments through Southeast Asian trade routes.
Several tightly packed accelerator cards fill adjacent slots inside a computer chassis; their ribbed beige covers and black mounting hardware are visible.
How are Chinese universities and research institutions reportedly obtaining restricted NVIDIA AI chips?
Chinese universities and research institutions are reportedly getting the restricted NVIDIA AI chips through direct purchases, along with shipments routed through Southeast Asia and corporate structures built around shell companies that obscure the final destination. The report says at least $1.7 million worth of restricted NVIDIA chips were acquired by Chinese universities and research institutions.
What role does Megaspeed International play in the NVIDIA hardware supply network described in the report?
Megaspeed International is described as a Southeast Asian importer that handled about $4.6 billion worth of NVIDIA hardware between 2022 and 2025. In the report, it is singled out because of that scale and its opaque ownership history, which makes it a possible part of the underground network moving restricted NVIDIA hardware. The report does not say that $4.6 billion in restricted AI chips reached China through Megaspeed.
What evidence did researchers find in the Southeast Asian shipments, such as missing customs data or rounded declarations?
Researchers found some shipments were missing cost, insurance, weight, and freight information. They also found unusually rounded customs declarations.
What kinds of NVIDIA AI accelerators are being targeted by these export restrictions?
The restrictions are aimed at NVIDIA's advanced AI chips and AI GPUs, including computing chips designed to power artificial intelligence. The report describes them as export-restricted or prohibited NVIDIA hardware rather than naming a more specific accelerator family.
Researchers identified suspicious shipping practices in some transactions, including missing cost, insurance, weight, and freight information, as well as unusually rounded customs declarations.
Best Deals: Nvidia RTX 2000 ADA 16GB Graphics Card

### Article 329 · 2026-09-18 · zacks.com
Zacks Investment Ideas feature highlights: NVIDIA, Advanced Micro Devices, Tempus, Moderna, Super Micro Computer and Aya Gold & Silver

Zacks Investment Ideas feature highlights: NVIDIA, Advanced Micro Devices, Tempus, Moderna, Super Micro Computer and Aya Gold & Silver
Chicago, IL – September 18, 2026 – Today, Zacks Investment Ideas features NVIDIA NVDA, Advanced Micro Devices AMD, Tempus AI TEM, Moderna MRNA, Super Micro Computer SMCI and Aya Gold & Silver Inc (AYA).
Will 2026 Doom and Gloom Lead to Opportunity?
2026 Has Been Full of Uncertainty
So far in 2026, Wall Street equity investors have navigated an extremely complex landscape marked by macroeconomic forces, geopolitical pressures, and sector-specific concerns. Inflation has remained stubborn, hovering above the Federal Reserve's long-term target. Disruptions in key transit areas like the Strait of Hormuz have led to an energy shock, with oil prices jumping 75% in 2026 alone.
Recently appointed Fed Chair Kevin Warsh has been forced to tighten monetary policy. Artificial intelligence, the market's fastest-growing area, has been faced with constant fear, uncertainty, and doubt about AI safety and CAPEX scrutiny. Meanwhile, the labor market is softening, and the upcoming midterm election adds another layer of legislative uncertainty.
The Power of Price Action vs. News Analysis
In my more than two decades of investing experience, I have learned that the stock market is the master manipulator. Most amateur investors focus too much on news headlines. However, analyzing news headlines alone is a sure-fire way to misinterpret the stock market. Rather than viewing news headlines in a vacuum, investors should focus on the market's price action in relation to the news.
For instance, if listed all the 2026 uncertainties to someone who does not follow the equity market, they would most likely guess that stocks are in a major correction. The fact is that the stock market has had the proverbial kitchen sink thrown at it, and the S&P 500 Index is just 2% off its all-time highs. Remember, stocks tend to climb the "Wall of Worry."
Retail Investor Sentiment Is in the Gutter
The American Association of Individual Investors (AAII) survey is a widely followed weekly poll that measures the percentage of individual retail investors who feel bullish, bearish, or neutral about the stock market over the next six months. Although the major equity indexes are within a hair of their highs, investor sentiment is extraordinarily negative. In fact, the latest AAII Survey shows the fewest bulls and most bears in over a year.
As George Patton once said, "If everyone is thinking alike, then somebody isn't thinking." Historical data backs up this claim. Since the late 1980s, when AAII bulls have fallen below 29% with the S&P 500 Index within 10% of all-time highs, stocks have been higher 100% of the time one month later (9 instances)
Recently, AI stocks corrected after OpenAI CEO Sam Altman and Anthropic CEO Dario Amodei sounded the alarm on AI safety concerns and called for regulation. Despite the fear-mongering from AI leaders, it's critical that investors read into what these CEOs are actually doing – not what they are saying. David Sacks, former "AI Czar" for the Trump Administration, made an astute observation:
"Dario (Anthropic CEO) has written that we need to "pace the frontier," and Sam Altman (OpenAI CEO) has agreed. People may be surprised by my response: go ahead. You guys are the frontier. By any reasonable metric – market share, revenue growth, model capability – the two of you have a duopoly on frontier intelligence."
Despite the alarmism, the top two AI CEOs are not slowing down. Earlier this month, Anthropic inked a $13.7 billion compute agreement while OpenAI held early talks with investors about another private funding round. Later, NVIDIA CEO Jensen Huang, the most important voice in AI, said:
"The fact that this is going to be the end of humanity – it's complete nonsense. The fact that this is going to destroy half of the American jobs is complete nonsense."
According to historical market data, the months leading up to mid-term elections are the worst time to own stocks in the four-year election cycle. However, after a choppy and frustrating summer market for investors, the good news is that seasonality suggests stocks tend to bottom around now and rally strongly into year-end.
Thursday, stocks across a variety of sectors broke out including Advanced Micro Devices , Tempus AI , Moderna , Super Micro Computer and Aya Gold & Silver Inc.
While macroeconomic headwinds, geopolitical energy shocks, and relentless media fear-mongering might suggest a market correction is overdue, the resilience of stock price action tells a different story.

### Article 330 · 2026-09-18 · benzinga.com
NVIDIA CEO Says AI Spending Flywheel Is ‘Really, Really Flying’

NVIDIA Corp. CEO Jensen Huang said demand for artificial intelligence computing is accelerating as AI becomes more useful and companies race to build new infrastructure.
Speaking with CNBC's Jim Cramer at Dreamforce in San Francisco, Huang said companies have been building NVIDIA-powered "AI factories" rapidly over the past six months.
Huang estimated that a 1-gigawatt NVIDIA AI factory costs about $50 billion to $60 billion to build. However, he said the same infrastructure can generate about $50 billion in annual rental revenue.
That implies a return on invested capital of roughly one year under current market conditions, according to Huang. He also said NVIDIA infrastructure can remain useful for more than five or six years.
Meanwhile, AI usage continues to climb. Huang said the rate of token generation has increased 25-fold in less than a year. Open models now account for nearly 70% of generated tokens, up from about 30%.
NVIDIA CEO Says AI Safety Is Creating A New Data Center Demand Engine
Huang also pushed back against concerns that AI safety efforts could derail industry growth.
During the interview, Jim Cramer jokingly asked Huang whether people should be preparing to "die in 2030" because of AI. "We're not going to die in 2030," Huang replied.
Huang said thousands of companies worldwide are working on AI safety, security and guardrails. He argued that the industry can build AI that is "incredibly useful," helpful and safe at the same time.
He said companies should test products thoroughly and avoid releasing systems before they are safe.
In fact, Huang expects testing to become a third major category of AI infrastructure alongside training and inference. He said large testing environments will require additional data centers, creating another source of compute demand.
Huang also pointed to rising rental prices as evidence of tight demand. He said NVIDIA Grace Blackwell systems can now rent for about $16 per GPU hour, compared with roughly $5 under some contracts signed a year ago.
As older contracts expire, cloud providers are raising prices, boosting revenue forecasts and investing in more infrastructure, Huang said.
Huang said rising GPU rental prices are boosting revenue forecasts and returns on invested capital, prompting customers to buy more equipment and build more infrastructure — a cycle he described as a flywheel that is "really, really flying."
NVIDIA stock rose in Wednesday premarket trading as technology stocks gained alongside U.S. equity futures. Nasdaq futures rose 0.39%, while S&P 500 futures gained 0.16%.
NVIDIA is trading 2.6% below its 20-day simple moving average of $218.81. However, the stock is roughly in line with its 50-day SMA of $213.24.
The longer-term trend remains constructive. NVIDIA trades 7.7% above its 200-day SMA of $197.79. In addition, the 20-day SMA remains above the 50-day average, while the 50-day remains above the 200-day.
Momentum is neutral. NVIDIA's relative strength index stands at 45.60. That suggests neither buyers nor sellers have firm control.
Resistance sits near $214, close to the 50-day SMA. Meanwhile, $190 represents a key support area. The stock's 52-week range is $164.27 to $236.54.
Piper Sandler initiated coverage with an Overweight rating and a $300 price forecast on Sept. 10. Rosenblatt maintained a Buy rating and $390 forecast on Sept. 4. Needham also maintained a Buy rating and $300 forecast that day.
Its Growth score stands at 98.12, while Quality is 97.38. Momentum is also relatively strong at 74.05. However, its Value score is much lower at 7.41, reflecting a more demanding valuation.
NVIDIA also carries significant weight in several exchange-traded funds. It accounts for 9.94% of the Xtrackers Net Zero Pathway Paris Aligned U.S. Equity ETF , 9.79% of the First Trust Innovation Leaders ETF and 9.73% of the Franklin Focused Dynamic Growth ETF .

### Article 331 · 2026-09-18 · kqed.org
Nvidia AI Researcher’s Family Demands Answers After His Death

Nvidia AI Researcher’s Family Demands Answers After His Death
The family of data scientist Irfan Al-Hussaini traveled to Palo Alto to investigate after his death was ruled a suicide.
Salma Begum, mother of Irfan Al-Hussaini, stands as her daughter speaks during a press conference outside Palo Alto City Hall in Palo Alto on Sept. 17, 2026, where the family called for a full and proper investigation into Irfan Al-Hussaini’s death and the introduction of new evidence regarding the circumstances of his death. (Nina Glick/KQED)
Months after a Bay Area AI researcher’s death, his family and friends gathered outside Palo Alto City Hall this week to demand answers.
On July 22, Palo Alto police responded to a report of a possible suicide by an adult male, who was then transported to a hospital, according to a statement from the department.
Irfan Al-Hussaini, a 32-year old senior data scientist at Nvidia, died eight days later, his family said in a press release.
Salma Begum, mother of Irfan Al-Hussaini, is consoled by a supporter of the family after a press conference outside Palo Alto City Hall in Palo Alto on Sept. 17, 2026, where the family called for a full and proper investigation into Irfan Al-Hussaini’s death and the introduction of new evidence regarding the circumstances of his death. (Nina Glick/KQED)
They’re now pushing for a deeper investigation.
According to the family’s release, Palo Alto police told them it will not open an active investigation unless directed by the county medical examiner, which has ruled Al-Hussaini’s death a suicide .
“We have assembled here, all of us, to get the attention of the Palo Alto Police Department,” said Irfan’s father Tahmeed Al-Hussaini, who described his son as “a simple, compassionate and adorable person.”
“He loved sports, games, traveling and nature. He had a soft heart,” Al-Hussaini said.
Al-Hussaini’s father, who flew in from Bangladesh with his wife as soon as they heard their son was in the hospital, has stayed in the country looking for answers.
“I already changed my ticket twice, and I’m still waiting here for clarity,” Al-Hussaini’s father said.
Dr. Sarah Al-Hussaini, sister of Irfan Al-Hussaini, speaks at a press conference outside Palo Alto City Hall in Palo Alto on Sept. 17, 2026, demanding a full and proper investigation into Irfan Al-Hussaini’s death and the introduction of new evidence regarding the circumstances of his death. (Nina Glick/KQED)
The family reached out to attorney Anthony Brass, a former prosecutor specializing in domestic violence and homicide, and asked whether he thought the authorities should investigate the death, Brass told KQED on Thursday.
Brass said that the absence of a suicide note, the “evidence of domestic violence in which [Al-Hussaini] was a victim,” and the timeline of events on July 22 were all red flags.
It’s “very strange to be that engaged in your professional life and to make sure you have permission for the day off the next day as a precursor to suicide while not bothering to write a suicide note,” Brass said. “It just simply makes no sense.”
In a statement, an attorney representing Fabia Farlin Athena, Al-Hussaini’s widow, told KQED she wants to cooperate fully with the investigation, and that she demanded a full autopsy, which the medical examiner performed on Aug. 31.
“Irfan is ‘everything’ to Athena. She misses him every second of the day,” attorney Matthew Davis wrote.
The Palo Alto Police Department told KQED that neither officials nor the examiner have identified any evidence the death was a result of foul play.
The medical examiner has not completed their report, and the case remains open online.
“At this time the case is still under investigation pending the report from the medical examiner,” Nicolas Martinez, a spokesperson for the police department, said in an email. “We have received materials from the family and others, and our review and investigation is on-going.”
KQED’s Alina Ta and Sukey Lewis contributed to this report.

### Article 332 · 2026-09-18 · techradar.com
Google, Nvidia, and Emerald AI launch Alliance to advance data centers that dynamically adjust electricity use based on grid conditions

Google, Nvidia, and Emerald AI launch Alliance to advance data centers that dynamically adjust electricity use based on grid conditions
By Craig Hale
Is this the technology data centers have been crying out for?
Emerald AI, Google and Nvidia have come together to form the AI Energy Management Alliance (AEMA), and it could be exactly what we need to tackle rising energy consumption within the data center field.
Together, the group hopes to deploy flexible AI data centers that can dynamically adjust how much electricity they consume from the grid based on a number of different conditions.
This important development comes in response to rising power availability pressures, which are leading to years-long delays for many new projects.
Future data centers could adapt how much power they use
In an announcement , Nvidia Head of Sustainability Josh Parker explained how these future campuses could shift compute workloads, discharge storage, use paired generation or respond to other system contingencies to dynamically change how much electricity they're drawing from the grid at any given time.
The concept involves shifting high-compute tasks like training to off-peak times, using on-site batteries or generation in conjunction with the grid and exporting excess stored energy back to the grid during times of stress.
Crucially, the AEMA must now set out technical specifications, performance metrics and open standards to allow this to happen at scale.
And while only Emerald AI, Google and Nvidia are behind the alliance from launch, a number of additional partners are set to join the scheme. SiliconANGLE reports that Anthropic will be one of them.
The concept itself isn't new – Google also announced earlier this year that it had over 1GW of demand-response capacity – but doing so at scale would likely make a considerable impact across the board.
Both Nvidia and Emerald AI have already developed software to handle power consumption in relation to the grid.
"By creating a common framework for performance, reliability and collaboration, AEMA aims to help the US build the infrastructure of intelligence at the speed and sustainability the moment demands," Parker wrote.
All of this, of course, comes against a backdrop of mounting energy pressures. Recent Bloomberg data suggests that US data centers alone could use as much natural gas as the entire of Germany and Japan combined by 2035, with a similar Moody's study projecting that total US data center energy consumption could top 426 TWh by 2030.
With several years’ experience freelancing in tech and automotive circles, Craig’s specific interests lie in technology that is designed to better our lives, including AI and ML, productivity aids, and smart fitness. He is also passionate about cars and the decarbonisation of personal transportation. As an avid bargain-hunter, you can be sure that any deal Craig finds is top value!
