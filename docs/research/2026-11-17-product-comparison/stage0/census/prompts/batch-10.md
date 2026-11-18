# Blind reader, matter census batch 10 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 40 articles (numbers 333 to 372,
2026-09-18 to 2026-09-19, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 333 · 2026-09-18 · channelinsider.com
Huawei’s Atlas 960 SuperPoD Takes Aim at Nvidia’s AI Lead

Huawei is accelerating its Ascend 960 chips and scaling its Atlas 960 SuperPoD as it builds a broader AI infrastructure alternative to Nvidia.
Huawei is not trying to catch Nvidia one chip at a time. Its latest strategy is to connect thousands of processors into increasingly large systems and compete at the infrastructure level instead.
The AI giant unveiled the Atlas 960E SuperPoD and accelerated the launch of its Ascend 960DT AI chip to the first quarter of 2027. The system can scale to 4,096 NPUs and is designed to integrate computing, networking, memory, storage, and software into a single AI infrastructure platform.
Huawei is positioning the stack as an alternative to Nvidia, but limited chip supply and Nvidia’s widely used CUDA software remain major barriers to broader adoption.
Huawei accelerates its Ascend 960 roadmap
According to Huawei , development of Ascend 960 has exceeded expectations. The Ascend 960DT now scheduled for the first quarter of 2027, three quarters earlier than originally planned. Meanwhile, the Ascend 960PR is expected in the third quarter.
The company also plans to introduce a new Ascend generation each year, with the Ascend 970 and 980 scheduled for 2028 and 2029, respectively.
Reuters reported that Huawei is already struggling to produce enough AI computing equipment to satisfy demand in China. Rotating chairman Eric Xu said the company therefore has no plans for a large-scale overseas expansion for now.
Atlas 960E puts scale and interconnects at the center
The Atlas 960E SuperPoD combines Ascend 960 chips with Huawei’s UnifiedBus interconnect and Hi-ONE near-packaged optics technology.
According to Huawei, a single system can scale to 4,096 NPUs and deliver 8 EFLOPS of FP8 compute performance with up to 1 petabyte of high-bandwidth memory. Huawei said the system uses 5,500 Hi-ONE optical engines instead of the 48,000 800G optical modules that would traditionally be needed to connect the NPUs.
The company claims the design cuts power consumption by more than 550 kilowatts and provides 99.8% system availability.
The 4,096-NPU figure applies to a single SuperPoD, not Huawei’s larger scaling ambitions. Huawei said multiple SuperPoDs can be connected into a SuperCluster supporting up to 512,000 NPUs, while a multi-rail topology could eventually extend that architecture to 1 million NPUs.
TechCrunch noted that Huawei had previously discussed an Atlas 960 system containing 15,488 Ascend 960 chips. The different configurations underscore Huawei’s broader emphasis on scaling AI compute through increasingly large interconnected systems.
For now, Huawei’s strategy is less about relying on a single accelerator and more about improving aggregate performance by connecting large numbers of processors.
Huawei is also building out its software ecosystem
Nvidia’s biggest advantage is not limited to its GPUs. Its CUDA software platform has become deeply embedded in AI development, creating another hurdle for competing hardware providers.
Huawei is trying to narrow that software gap through CANN, its Compute Architecture for Neural Networks.
The company said CANN has moved to sustained, community-driven open-source development and now has more than 5,200 monthly active developers. Huawei also highlighted that Ascend supports more than 90 third-party open-source projects, including PyTorch, Triton, vLLM, and veRL. More than 40 models have been natively pretrained on Ascend and CANN.
Reuters noted that Nvidia still retains a major software advantage through CUDA, despite Huawei’s efforts to grow Ascend adoption.
Huawei’s infrastructure push creates a bigger channel opportunity
Huawei’s strategy extends the AI hardware race well beyond accelerator chips. Systems containing thousands of NPUs also require high-speed optical networking, storage, power management, cooling, and increasingly sophisticated integration between those components.
That could create a broader opportunity for infrastructure vendors and partners as AI deployments become larger and more complex. Channel Insider has previously reported that AI adoption is exposing network readiness gaps , creating demand for partners capable of modernizing the infrastructure supporting increasingly data-intensive workloads.
Power and cooling are becoming part of that equation as well. As AI clusters become denser, data center operators are facing higher energy and thermal requirements, with AI-ready cooling becoming another part of the infrastructure stack that infrastructure partners may need to address.
Customers evaluating systems at this scale are therefore not simply choosing processors. They are weighing an entire stack, including networking capacity, software compatibility, energy requirements, support, and suppliers’ ability to deliver hardware at the required scale.
Huawei still faces substantial hurdles. Nvidia’s CUDA ecosystem remains well-established, while Huawei has acknowledged that its current production capacity is insufficient to meet demand in China, limiting its plans for large-scale overseas expansion.
The Atlas 960E therefore matters as much for its architecture as its raw specifications. If AI competition continues to shift toward massive interconnected systems, the companies supplying networking, optics, storage, cooling, and integration for those accelerators could become increasingly important to how the AI infrastructure market develops.
DeepSeek reportedly plans to deploy 160,000 Huawei AI chips at a data center in Inner Mongolia , a project that could further expand Huawei’s role in China’s AI infrastructure market.
Kezia Jungco is a technology writer and researcher specializing in artificial intelligence, data analytics, CRM software, cloud infrastructure, cybersecurity, and emerging business technologies. With more than five years of experience evaluating software platforms and technology solutions, she helps business leaders understand the tools and trends shaping the future of work.
Kezia has extensive hands-on experience testing and analyzing generative AI platforms, chatbots, natural language processing (NLP) tools, CRM systems, and business software. Her work focuses on translating complex technologies into practical insights that help organizations make informed decisions about technology adoption, operational efficiency, and digital transformation.
As a staff writer for TechnologyAdvice, Kezia covers AI innovation, business applications of machine learning, data-driven technologies, cloud computing, cybersecurity, and sales technology. Her background in journalism, research, and education enables her to combine rigorous analysis with clear, accessible reporting for both enterprise and consumer audiences.
Kezia holds a bachelor's degree in Development Communication with a major in Development Journalism from the University of the Philippines Los Baños. She has also completed professional training in artificial intelligence, data privacy, and information security. Her work has been featured in TechnologyAdvice, TechRepublic, eWeek, Datamation, and Selling Signals, where she helps readers navigate a rapidly evolving technology landscape with practical, research-driven guidance.

### Article 334 · 2026-09-18 · qz.com
NVIDIA and Google are launching a coalition to make AI data centers flex their power use

NVIDIA, Google $GOOGL , and Emerald AI announced the launch of the AI Energy Management Alliance, a coalition aimed at getting AI data centers to dynamically manage their electricity consumption in response to grid conditions, with the goal of securing faster connections to the power grid in return.
The alliance, called AEMA, wants data centers to function as controllable resources rather than facilities with fixed, unchanging electricity demand. A flexible data center can adjust its grid draw by shifting computing workloads, discharging battery storage, using on-site generation, or responding to grid emergencies, the group said.
In exchange for making those commitments, AEMA is pressing grid operators and utilities to grant data center projects faster and larger grid connections. Under AEMA's framework, the group would develop common standards for technical specifications, measurable performance benchmarks, and data sharing between facilities and grid operators, while also establishing upfront expectations for how data centers behave during voltage events or calls to reduce load, the group said.
Emerald AI CEO Varun Sivaram explained the problem the coalition is trying to solve, according to Engadget . Getting a new data center onto the grid can take ten years or longer, Sivaram noted, because utilities are obligated to guarantee sufficient capacity for peak demand periods. Yet average grid utilization hovers around 50%, which means data centers willing to flex their consumption could tap into substantial headroom on the existing network without forcing expensive new buildout.
AEMA is technology-neutral and performance-based, focusing on measurable outcomes — response speed, duration, predictability, and behavior during emergencies — rather than specific hardware or software, the group said. The coalition also plans to advocate for policies that recognize grid-responsive demand in state capitals and Washington.
The announcement comes as AI data centers have faced mounting public and political opposition. Roughly 70% of Americans would object to a data center being built in their community , citing strain on local power resources and higher utility bills as their leading concerns. Community opposition stalled or halted 48 projects representing more than $156 billion in planned construction last year alone, according to Data Center Watch data cited by Fortune.
The broader grid strain has been years in the making. Interconnection queues were already backlogged before data centers began requesting gigawatts of capacity, and utilities built for stable, predictable demand are struggling to accommodate the pace of expansion .
NVIDIA and Emerald AI said they are already working with energy and infrastructure partners on AI facilities that can respond to grid conditions in real time. AEMA will expand that work by bringing technology, energy, and policy stakeholders together around models intended for deployment across the U.S., the group said.

### Article 335 · 2026-09-18 · fool.com
Prediction: This Much Nvidia (NVDA) Stock Bought Today Could Be Worth $28,560 by 2030

Semiconductor giant Nvidia (NASDAQ: NVDA) has been a hot stock for some time now -- for good reason. It has averaged annualized gains of 52% over the past 15 years. That was enough to turn a single $10,000 investment 15 years ago into a stake worth $5.9 million (with dividends reinvested) or $5.4 million (without the reinvestment of dividends).
What if you buy into it today, though? How big could your stake in it become by, say, 2030? Let's take a look.
Let's start with a caveat: Whatever estimate we come up with will be just that -- an estimate. It will be based on the stock's growth rate -- which over the past three years has averaged nearly 70% per year! Over the past one year, it has gained nearly 20%. (That 20% might seem puny, but remember that over many decades, the stock market has averaged annual gains of close to 10% . So a 20% gain is still pretty good.)
But how quickly will Nvidia grow over the coming four years? Well, let's pick a number between that 20% and the longer-term rate of 52%. Let's say 30%.
The stock recently traded at about $214 per share. If it gains 30% annually for four years, it will end up priced around $611 per share. That would be a total gain of 185.6%. Under that scenario, if you put $10,000 into it now, by September 2030, your stake would be worth about $28,560 -- and that's without counting or reinvesting its dividends, which are currently $0.25 per share quarterly.
Here are some things to keep in mind regarding that estimate of a 185% gain:
Nvidia could keep growing at 50% over the coming years, giving you a much bigger gain.
Nvidia shares could also plunge in the coming years. This could be due to some unforeseen problem with the company, a slowdown in its business, or simply due to the stock market crashing. The U.S. stock market does crash now and then -- though so far, it has always eventually recovered from those downturns and gone on to set new highs. That's why it's good to be a long-term investor. Note, too, that when the market pulls back, growth stocks like Nvidia often fall extra hard (typically before eventually recovering).
Much will depend on how well Nvidia executes its strategies, and on that count, there's much to be optimistic about:
Nvidia's recent purchase of Hugging Face will give it access to a large developer ecosystem as competition in AI hardware increases. (More than 200,000 companies use Hugging Face to work with AI models.)
The company recently reported terrific second-quarter results, with revenue up 106% year over year to $96 billion, and revenue from data centers up 117% to $89 billion.
The stock seems undervalued, trading at a forward price-to-earnings (P/E) ratio of 23, well below its five-year average of 34, and a price-to-cash-flow ratio of 30, well below its five-year average of 51.

### Article 336 · 2026-09-18 · cbsnews.com
Nvidia CEO Jensen Huang calls for AI to be developed "as fast as we can"

Nvidia CEO Jensen Huang calls for AI to be developed "as fast as we can"
By Faris Tanyos
Faris Tanyos is a news editor for CBSNews.com, where he writes and edits stories and tracks breaking news. He previously worked as a digital news producer at several local news stations up and down the West Coast.
The CEO of the world's largest chipmaker told CBS News that tech companies should push forward with the development of artificial intelligence despite recent warnings from worried industry leaders that there may be a need to pull back due to unease about where the technology could be headed.
"We should go as fast as we can irrespective of anybody else," Nvidia founder and CEO Jensen Huang told CBS News senior business and technology correspondent Jo Ling Kent in an interview airing this weekend on "Sunday Morning," when asked if AI development needs to slow down.
"We're going to go as fast as we can, but we would never ever, and never should, ship products before they're ready, deliver products that are unsafe," Huang said. "And nobody's expecting us to do that. But everybody's expecting us to succeed and help America be as prosperous as possible."
The Santa Clara-based Nvidia, the world's most valuable company with a market capitalization above $5 trillion, has achieved its growth with the help of the AI boom.
However, concern has grown in recent weeks over the speed at which AI is developing, with some calling for guardrails and government regulation.
The conversation was spurred in part by Jacob Coxon, a researcher at AI giant Anthropic who publicly resigned his position earlier this month, saying that AI companies are rushing to innovate at the expense of proper security protocols. Coxon told CBS News that without such intervention, AI could one day pose a threat to humanity. The Trump administration has so far generally been dismissive of those fears.
Days later, Anthropic CEO Dario Amodei appeared to echo some of Coxon's concerns, telling Kent in an interview that "for too long the industry lied to people about the fact that this technology had risks," and saying the technology was developing at an "exponential" rate.
"It doesn't mean we need to panic today. It doesn't mean we need to shut it all down," Amodei said , but added that it is "a warning sign that we need to slow down."
Watch Jo Ling Kent's interview with Jensen Huang on Sept. 20 on " Sunday Morning ."

### Article 337 · 2026-09-18 · fool.com
Apple, Nvidia, Microsoft, Alphabet, and Amazon: I Ranked the 5 Largest Companies by Market Cap, and 1 Stands Above the Rest

Size isn't everything when it comes to a company, but it's certainly something. There are some competitive advantages that can only come with size, like more buying power and bigger marketing budgets.
And this got me thinking: Do most investors fully appreciate just how big the world's biggest publicly traded companies today are? I went digging for these very details. While there was nothing surprising about the names that topped the list, I was blown away by just how big these outfits have gotten, and was in outright awe of how enormous the stock market's biggest companies have become in such a relatively short time.
Cutting straight to the chase, here's the list, from biggest to least big of the big.
Alphabet (NASDAQ: GOOG) (NASDAQ: GOOGL)
Data source: Finviz.
There's an obvious common thread here: These are all technology companies . This makes sense, of course. Technology is driving the world's biggest and fastest changes. The companies that have perfected their contribution to the technological landscape are perfectly positioned to gain the most.
That said, it would be wrong to not point out that most of these outfits' total growth has happened just since the advent of modern-day artificial intelligence. A mere five years ago, for instance, Apple's market capitalization was just under $2.5 trillion, as was Microsoft's. Like Amazon's, Alphabet's was under $2 trillion in September 2021.
Perhaps the most jaw-dropping growth during this five-year stretch, however, has come from Nvidia, which has expanded more than tenfold from a market cap of just over $500 billion. Give credit to the fact that Nvidia's processing chips are at the heart of the majority of the world's AI data centers -- an industry that largely didn't exist until after the public launch of ChatGPT in late 2022.
That being said, although the stock market's biggest names at any given time have always been considerably bigger than even the next-nearest outfits in terms of total size, the market's top heaviness has reached shocking levels of late. The five biggest companies now collectively account for 30% of the S&P 500 's (SNPINDEX: ^GSPC) combined market cap.
And speaking of uncomfortable imbalances, the prolonged gains of the aforementioned tech stocks -- along with a bunch of other technology names -- have dramatically skewed the S&P 500's overall sector allocation. Nearly 40% of the index's current value consists of technology tickers.
Size doesn't guarantee anything about a megacap company's future performance, of course, even if it was a strong fiscal performance that resulted in its achieving that size in the first place. Things change, like Nvidia, which displaced Apple as the world's then-biggest publicly traded company back in 2024.
Two decades ago, oil giant ExxonMobil (NYSE: XOM) was the world's most valuable company, followed by industrial powerhouse General Electric (before its 2024 breakup). Three decades ago, beverage behemoth Coca-Cola (NYSE: KO) boasted the world's then-biggest market cap of $130 billion, followed by ExxonMobil, then technology giant Intel (NASDAQ: INTC).
Things don't change particularly quickly, though, and they certainly don't change quickly enough to justify avoiding any given company's stock simply because it's the biggest outfit at any given time. Coca-Cola has still performed well since 1996. Ditto for how ExxonMobil has done since 2006.
Nvidia, Amazon, Apple, and all the rest are apt to continue performing well for the foreseeable future, too, even if they will eventually, almost inevitably, fall out of the top five. Indeed, given the artificial intelligence industry's plans for continued expansion and the subsequently unyielding demand for AI processing chips, Nvidia could conceivably perform well enough to remain in the top five for the foreseeable future before eventually being displaced. It could still be a plenty-bullish ride in the meantime.
In any case, I suspect these five companies will remain in the top 10 for at least the next couple of years, and maybe even the next three to five years, if things go well. Just don't be surprised if that starts to measurably change after that point.

### Article 338 · 2026-09-18 · fool.com
Will Micron Follow Nvidia and Give Investors a Huge Dividend Hike?

Once upon a time, semiconductor stocks were solid dividend payers.
Before the AI boom, many of these household names paid yields that were significantly higher than the S&P 500 , a reflection of the earlier perception of chip stocks as cyclical companies that rewarded investors with dividends as much as growth.
Nvidia's ( NVDA +2.55% ) yield topped 2% shortly after it launched its dividend in 2012, and Broadcom's was hovering above 3% for much of this decade. Intel was a dividend powerhouse with a yield of 3%-4% for much of the 2010s, before axing the payout to invest in its turnaround.
As chip stock prices have soared, yields have fallen, and most of these companies have ignored their dividend, choosing to invest in growth instead.
Nvidia's dividend yield had shrunk to as little as $0.01 a share, or a yield of 0.02%, but the company recently rewarded investors with a 2,400% dividend hike, raising its dividend to $0.25 per share, or a yield of 0.5%.
That may not sound like much but for longtime shareholders and other investors with large Nvidia holdings, that represents a huge windfall. With a market cap of $5.3 trillion, Nvidia is handing out roughly $25 billion in annual dividend payments.
Given the soaring profits in the semiconductor sector , Nvidia is unlikely to be the last chip stock to make that move. Another obvious candidate appears to be Micron ( MU +4.20% ) , which is one of the three big memory chip stocks, along with Samsung and SK Hynix .
Micron currently pays a quarterly dividend of $0.15, giving it a yield of just 0.06%.
Like Nvidia, Micron has seen profits skyrocket in the AI era, benefiting from the shortage in memory chips, and the stock is up more than 1,000% in the last two years.
The company initiated its dividend in 2021, shortly before a cyclical downturn in the memory sector that led to steep losses for the company. Today, however, Micron is far more profitable than it's ever been, with a net income of $50.5 billion over the last four quarters, and that's growing rapidly. That means Micron has a dividend payout ratio of just 1.1%, meaning it only returns one cent out of every dollar it earns in profits.
Micron could easily raise its dividend by 10x or 25x as Nvidia just did, and doing so could give the stock another leg up. Based on its price-to-earnings ratio, Micron stock is actually cheap, trading at a forward P/E of less than 7 based on fiscal 2027 expected earnings. That adds an incentive to hike the dividend as low valuations create opportunity for high yield.
Companies primarily spend profits on share buybacks, dividends, debt reduction, or some kind of business expansion like capital expenditures or acquisitions. Micron has big plans to expand, recently breaking ground on a $100 billion facility in upstate New York to be completed over the next 20-plus years, but the company can fund all of that with just a portion of next year's expected profits.
It's spent more than $9 billion to pay down debt this year, reducing its debt burden to just $5 billion, and it now has $25 billion in cash on its balance sheet.
The company has only spent modestly on share buybacks as well, despite the stock's ostensibly low valuation.
Will Micron hike its dividend?
Micron will eventually have to put the windfall from the memory bottleneck to use and share buybacks or dividend payments are the two most obvious choices.
Some combination of the two would make sense. Memory is notoriously cyclical and the company may be wary of overspending on returning capital to shareholders, but there's a way to do it prudently, as Nvidia has done. Doing so would take advantage of its valuation.
Micron could 10x both its dividend and share repurchases, and still have the vast majority of its cash flow available to invest in the business, or save for a rainy day.
Increasing the dividend and buybacks would reward investors and send a message that management still sees the stock as cheap, even after its parabolic rise. Such a move could give the stock a meaningful jolt, and that would be welcome news for investors as well.
By Jeremy Bowman – Sep 18, 2026 at 12:30PM EST
Micron is enjoying a huge windfall from the memory shortage. A dividend increase would make sense as a way to spend that cash.

### Article 339 · 2026-09-18 · fool.com
Step Aside, Nvidia: 1 Reason Why Meta Platforms Could Be the Best AI Stock to Buy in 2026.

The market has crowned Nvidia ( NVDA +2.55% ) one of the top artificial intelligence (AI) stocks out there. In the past five years, its shares have rocketed 865% higher (as of Sept. 16). And the business -- the largest in the world by market cap -- is currently worth a staggering $5.2 trillion.
Nvidia sells the most widely used AI processors at the foundation of the data center build-out . As a result, its financial performance since the AI megatrend took shape has been jaw-dropping. Over the last three years, its net income surged almost tenfold. It's extremely difficult not to be bullish on this company.
However, investors can find one valid reason that supports the case for Meta Platforms ( META -0.83% ) being the best AI stock to buy in 2026. It all comes down to questioning where the value from this AI revolution will eventually accrue.
It's a realistic possibility that in the long run, the chips, data centers, cloud computing platforms, and AI models all become commoditized. This means that there will be minimal differentiation between the offerings of the various competitors in each of those arenas. Consequently, a logical argument can be made that most of the value will eventually accrue to the application layer, benefiting the businesses that create products, services, and experiences enabled by AI for end users.
Think about the internet revolution that took off in the 1990s. The companies that built the fiber optic infrastructure that supports the internet can't hold a candle to the enterprises that actually leveraged the new technology to serve people in new ways.
Household names today, like Amazon , Alphabet , Meta Platforms , Uber , and Airbnb , created entirely new experiences, building thriving businesses in the process. These are extremely valuable companies.
Another insightful way of viewing this situation is to consider Apple and the iPhone. For the average person, this hardware device line elegantly allows access to the digital world without requiring them to be technologically proficient. When it comes to AI, consumers want the technology embedded in things that simply work. Most folks don't want to have to figure out on their own how to use AI.
Meta's massive ecosystem puts it in a favorable position
Meta owns some of the most popular platforms on Earth. Across its family of apps, it has 3.6 billion daily active users. This gives it incredible reach. If the value in AI is going to accrue to the application layer, it makes sense that the company with the most dominant apps is in a position to be a winner.
Meta is already leveraging AI to boost engagement among its users. And for its advertising customers, its AI tools are improving the effectiveness of marketing campaigns.
Further adding to Meta's strong competitive position is its thriving advertising platform. The business benefits from a scaled ad ecosystem, network effects, a treasure trove of user data, and strong user engagement, all of which position it to monetize free AI usage better than other companies.
Unlike enterprises, which will gladly pay for AI offerings if they offer the promise of boosting employee productivity, consumers don't necessarily have the willingness to pay money for these kinds of tools. The data backs up this claim. According to a study by the Bank of America Institute, only 3% of households with accounts at that bank are paying for AI services. Layering advertising onto those offerings seems to be the best way to profit from providing consumer AI products and services for free.
Meta is leaning in. It recently launched Muse , an AI agent that can handle various tasks on behalf of users. Founder and CEO Mark Zuckerberg says he wants the company to introduce what he calls "personal superintelligence." During its second-quarter earnings call, he asserted that it wouldn't be surprising if, in five years, billions of people were using AI agents daily. Muse is a step in that direction.
Investors should also take advantage of Meta's current valuation. This "Magnificent Seven" stock trades at a forward price-to-earnings ratio that's below 20. Maybe the market believes Meta isn't positioned well in the AI race. However, I think that view will prove to be incorrect over the coming years, as the business is able to gain financially from its AI efforts.
Shareholders who buy today will benefit from rising earnings and improving sentiment.
In the long run, the infrastructure powering the AI boom could become commoditized, with more of the value going to the businesses creating applications.
By Neil Patel – Sep 18, 2026 at 8:16AM EST
Given Nvidia’s mind-boggling earnings growth driven by GPU demand, it’s understandable that investors view this company as the top AI bet.
The businesses that introduced popular customer-facing applications during the internet revolution captured tremendous value.
Meta Platforms should be able to monetize free consumer AI usage better than other companies thanks to its massive user base, its advertising ecosystem, and its vast trove of user data.

### Article 340 · 2026-09-18 · gurufocus.com
Nvidia CEO Sends Strong Signal to Investors

Nvidia ( NASDAQ:NVDA ) CEO Jensen Huang says the company expects to sell roughly twice as many chips next year as it does this year, offering one of his strongest signals yet that AI demand remains far from exhausted.
I expect Nvidia to sell twice as many chips as this next year as we do this year, Huang told reporters Thursday at a summit in Scotland with King Charles III.
The reason for that is because AI has, has so much contribution to the benefits of different industries, different economies, and you can see that in almost every single country that we're in, people want to invest in AI.
The forecast adds to Nvidia's increasingly aggressive outlook for the next several quarters.
The company recently said it expects roughly 70% growth in the fiscal year ending January 2028, which would put annual revenue around $673 billion.
Nvidia does not disclose total chip unit shipments, making Huang's volume forecast difficult to translate directly into revenue. But the company's most important products include its data-center GPUs, particularly Blackwell and next-generation Rubin systems.
Huang said last fall that Nvidia had shipped about 6 million Blackwell GPUs over four quarters.
The comments come as investors debate whether hyperscaler spending and model-training demand can continue growing at the breakneck pace seen during the first phase of the AI buildout.
Huang's forecast strengthens the argument that demand remains broad enough to absorb a huge increase in supply.
For investors, the key question is not simply whether Nvidia can double chip volumes, but what that mix looks like.
Higher shipments of premium Blackwell and Rubin systems could support enormous revenue growth, while greater unit volume at lower average selling prices would produce a different margin outcome.
Investors should also watch manufacturing capacity, networking attach rates and whether customers continue committing capital beyond 2027.
Nvidia is planning for substantially more hardware demand, not a plateau.The risk is execution. Doubling chip volume requires suppliers, packaging capacity and customers to scale alongside Nvidia. If AI infrastructure spending slows before that capacity is absorbed, the company could face greater pressure on utilization and pricing.

### Article 341 · 2026-09-18 · tedmag.com
Emerald AI, Google, NVIDIA Form Flexible Data Center Alliance

SANTA CLARA, Calif. — AI factories are the infrastructure of the intelligence era. Scaling them responsibly will depend as much on innovation across the grid as inside the data center.
Today, Emerald AI , Google and NVIDIA announced the launch of the AI Energy Management Alliance (AEMA) , a first-of-its-kind coalition advancing data centers that can dynamically manage their electricity use in response to grid conditions.
This power flexibility can help unlock faster, larger connections for AI infrastructure while supporting the energy systems and communities that make its growth possible. Getting more watts out of existing infrastructure reduces environmental impacts per watt and supports energy affordability.
The objective is clear: build AI infrastructure that doesn’t just connect to the grid but works with it.
Power has become a defining constraint on the expansion of U.S. AI infrastructure.
Traditional interconnection processes were designed around facilities with flat, static electricity demand. They weren’t built for computing infrastructure capable of responding intelligently when the power system is constrained.
A flexible data center can adjust its electricity drawn from the grid in several ways — shifting computing workloads, discharging storage, using paired generation or responding to system contingencies. These capabilities allow a large electricity customer to serve as a controllable resource rather than an inflexible load.
Used effectively, flexibility can make more efficient use of existing grid capacity, reduce demand during periods of system stress, and avoid or defer costly infrastructure upgrades. It can also give utilities and grid operators greater confidence to connect AI facilities on shorter timelines.
Technology-Neutral, Performance-Based Requirements
AEMA is technology-neutral and performance-based. Its focus is on the measurable service a facility can deliver — including response speed, duration, predictability and behavior during an emergency — rather than the specific hardware or software used.
Reliability remains paramount. The alliance’s principles call for:
Defining ride-through, curtailment and contingency-response obligations before a facility connects — meaning the alliance is setting clear rules for facilities regarding staying connected during brief grid disturbances, reducing power use when needed and responding to emergencies.
Standardizing technical requirements, performance metrics and operational data sharing.
Creating faster, risk-adjusted pathways for customers that make credible and verifiable flexibility commitments.
Allocating interconnection costs in a way that reflects actual system impacts and benefits, such as avoided upgrades and improved ramping capability.
These measures can reduce uncertainty for developers while giving system operators the information and control needed to preserve reliability.
Convening the Full AI and Power Value Chain
AEMA convenes the full value chain across computing and power — including AI platforms, infrastructure providers, data center operators, technology companies, power producers, utilities and regional grid operators.
The founding members will be joined by launch partners from across the ecosystem. Together, AEMA will develop technical and operational approaches, collaborate with utilities on interconnection solutions and advocate for policies that recognize grid-responsive demand.
AI factories transform energy and data into intelligence. Power-flexible design gives them the potential to support the grid as they do it.
NVIDIA and Emerald AI are already working with energy and infrastructure leaders on AI factories that can respond to grid conditions in real time. AEMA will broaden that work by bringing the technology, energy and policy communities together around models that can be deployed across the U.S.
The rules governing power for AI are being written now. By creating a common framework for performance, reliability and collaboration, AEMA aims to help the U.S. build the infrastructure of intelligence at the speed and sustainability the moment demands.
Learn more about AEMA and membership opportunities.

### Article 342 · 2026-09-18 · fool.com
Jensen Huang Calls Nvidia the "World's First and Only Growth Value Stock," Pointing to Its 70% Revenue Growth Forecast Next Year. Here's Why That Framing Matters for How Investors Price NVDA.

Jensen Huang Calls Nvidia the "World's First and Only Growth Value Stock," Pointing to Its 70% Revenue Growth Forecast Next Year. Here's Why That Framing Matters for How Investors Price NVDA.
Speaking at Goldman Sachs ' Communacopia + Technology Conference on Sept. 10, Nvidia (NASDAQ: NVDA) CEO Jensen Huang highlighted a series of growth forecasts for his company and the artificial intelligence (AI) market at large. Notably, Huang doubled down on his projection that the world's annual AI infrastructure spending would land between $3 trillion and $4 trillion by 2030. For reference, market research firm Gartner projects that global AI infrastructure spending will total roughly $1.48 billion.
At the conference, Huang also reiterated the guidance that Nvidia issued with its fiscal Q2 report earlier this month for sales growth of 70% in its next fiscal year. He went on to describe Nvidia as the "world's first and only growth value stock." What does that mean for investors?
What should investors make of Huang's "growth value" framing?
Huang has done an incredible job guiding Nvidia's growth, turning it into the most important player in the AI hardware space and the world's most valuable company by market cap. He's undoubtedly a visionary leader and one of this century's most important and influential figures.
At the same time, it would probably be a stretch to call Nvidia the world's first and only "growth value stock." With the benefit of hindsight, many of history's biggest tech winners could have been placed in the category at various points in their growth trajectories -- and there are probably other stocks on the market right now that could also justifiably fit in it.
On the other hand, Huang isn't wrong to point out the unusual nature of Nvidia's current valuation profile relative to its growth. Despite its incredible valuation run-up and megacap size, traditional valuation metrics suggest Nvidia could be significantly undervalued.
Nvidia is currently trading at roughly 23 times this year's expected earnings and roughly 12.5 times expected sales. Given the company's stellar growth rates this year, the stock actually looks quite cheap based on those valuation metrics. The company grew revenue 106% year over year in the second quarter, and adjusted net income surged by 118%.
The company is on track for massive growth this year, but valuation multiples that look low compared to the business's rates of sales and earnings expansion would make sense if the business were on track for big performance drop-offs next year and beyond. That doesn't appear to be the case.
With Nvidia guiding for roughly 70% revenue growth in fiscal 2028 and gross margins of 72% to 73%, the business is seemingly poised for another year of strong sales and earnings growth. The company has also tended to be conservative in its guidance. With that in mind, there are good reasons to think that Huang is correct to highlight the striking "growth value" characteristic of his company's stock.
Jensen Huang Calls Nvidia the "World's First and Only Growth Value Stock," Pointing to Its 70% Revenue Growth Forecast Next Year. Here's Why That Framing Matters for How Investors Price NVDA. was originally published by The Motley Fool

### Article 343 · 2026-09-18 · finance.yahoo.com
Jim Cramer Said This AI Firm Has More Orders Than “Almost Anybody” Other Than NVIDIA

For custom chip designer Broadcom Inc. (NASDAQ: AVGO ), the debate is all about whether the demand for AI products will sustain and grow. It is among the few firms capable of designing custom AI chips that big technology firms rely on to supplement NVIDIA's high-power and expensive AI chips. Anthropic CEO Dario Amodei's latest remarks about the need to slow down AI development due to safety concerns have generated quite a buzz, and Cramer discussed what Broadcom Inc. (NASDAQ:AVGO)'s CEO told him when asked about AI infrastructure development losing traction:
"What's refuted by Hock Tan, of course, maybe Hock Tan is one of the biggest providers of semis, other than NVIDIA, and when I asked him about, give me a prediction about the AI slowdown, would there be one, he said, not in the least. We see the demand for compute infrastructure for development of AI and inference as extremely strong and durable. So I know those stocks were the most heavily hammered, other than the fiber stocks. But David, when you listen to what Hock Tan said last night on Mad Money, you are inclined to do buying.
"I think David, you recognize, and a lot of people don't, when you're speaking about Hock Tan, whom I had on, you're talking about a 1.6 trillion dollar company. This isn't just someone. . .worried about what orders are going to be. . .this man has more orders than almost anybody other than Jensen Huang. So I think Carl, when we get very, very negative we still have to rely on the facts And the facts do not support there are some people who are very worried about mankind, I did not get the mankind worry when I spoke yesterday."
The CNBC TV host's remarks about Broadcom Inc. (NASDAQ:AVGO) sit right at the center of the debate for the firm. This debate is about whether it will be able to continue to capture additional orders for custom AI chips. Looking at the third quarter earnings, released on September 2nd, the growth narrative appears to be quite strong.
It boosts Cramer's claims of Broadcom Inc. (NASDAQ:AVGO) experiencing strong orders, as during the quarter, the firm's revenue grew by 86%, AI semiconductor revenue jumped by 221% and fiscal year 2026 guidance implied 186% annual AI revenue growth. Not to mention, CEO Tan reaffirmed that Broadcom Inc. (NASDAQ:AVGO) could pull in $115 billion in annual AI chip sales in 2027 and a whopping $230 billion in 2028.
Yet, while Tan, and Cramer, remain optimistic about the firm's orders, the fourth quarter guide did leave investors wanting more. For the fiscal Q4, Broadcom Inc. (NASDAQ:AVGO) guided $34.8 billion in revenue which missed analyst estimates of $35.03 billion. Not to mention, the firm guided Q4 gross margin at 73% which marked a five point annual drop due to a higher mix of XPU sales. XPUs need more memory chips and the memory market is experiencing historic prices due to hot AI demand. Coupled with the fact that estimates have suggested that 71% of Broadcom Inc. (NASDAQ:AVGO) 's fiscal 2027 and 2028 XPU deployment could rely on OpenAI and Anthropic, the firm could experience headwinds. In other words, a huge portion of the orders might be from firms that are now calling for a slowdown in AI development.
What do the hedge funds think? Well, in Q2, 170 out of the 1,006 finds tracked by Insider Monkey had held a stake in Broadcom Inc. (NASDAQ:AVGO). This marked a slight drop over the 163 out of 1,022 funds in Q1. Notable exits included Third Point and Two Sigma Advisors . As for the valuation, the stock trades at a forward P/E ratio of 18 which is lower than NVIDIA's 23.42.

### Article 344 · 2026-09-18 · fool.com
Global AI Infrastructure Spending Will Hit $31.6 Trillion by 2050. This Is the Stock That Could Benefit the Most

Artificial intelligence (AI) infrastructure spending isn't showing any signs of slowing down. Industry bellwether Nvidia ( NVDA +2.55% ) noted on its August earnings call that the top five U.S. hyperscalers alone are on track to clock $800 billion in capital expenditure this year.
Even better, Nvidia projects that this figure will jump to $1.3 trillion in 2027. What's worth noting is that Nvidia's estimate doesn't include the spending by neocloud providers and AI labs, such as OpenAI and Anthropic. So, the overall spending on AI infrastructure could be much larger. Importantly, these robust spending levels seem sustainable for the long run.
Consulting firm PwC recently noted that cumulative AI infrastructure spending through 2050 could reach $31.6 trillion. A closer look at this report will tell us that this is great news for Nvidia for a very simple reason.
Chip upgrades should ensure healthy demand for Nvidia's chips
PwC points out that spending on chips and other hardware will account for a major share of this $31.6 trillion outlay. The consulting firm notes that around 70% of AI infrastructure spending is currently going toward information and communications technology (ICT) equipment, including chips.
However, that proportion will rise to 93% by 2050. This acceleration will be driven by the need to upgrade chip equipment every few years. It is also worth noting that the annual outlay on AI data center infrastructure could increase from around $800 billion in 2026 to $1.8 trillion in 2050.
It is easy to see why PwC sees chip upgrades driving elevated AI infrastructure spending levels over the long run. Every new generation of chips brings about improvements in computing power while reducing power consumption. Nvidia, for instance, claims that its latest Vera Rubin chip systems will consume 2x the power of the preceding Blackwell chips, but will deliver a 10x increase in performance per watt, according to CNBC.
So, hyperscalers, neocloud providers, and AI labs can get more value for every dollar they spend on upgraded chip systems, thereby lowering the cost of running workloads. As a result, Nvidia's core data center business can sustain healthy long-term growth, driven by chip upgrade cycles.
The company has generated $164 billion in revenue from its data center segment in the first six months of fiscal 2027. That translates into an annual run rate of just under $330 billion for the full year. The $1.8 trillion annual revenue opportunity cited by PwC suggests that Nvidia's data center business still has significant room for growth, especially given its impressive market share.
Nvidia controls an estimated 80% of the AI accelerator market, according to semiconductor industry tracker Silicon Analysts. Importantly, the company is taking steps to ensure it remains the dominant player in this space. It anticipates a big jump in server processor revenue , a market that it has just entered.
Additionally, the company is strengthening its ecosystem by partnering with MediaTek and Marvell Technology to connect custom AI processors with Nvidia's rack-scale server systems. So, I won't be surprised to see Nvidia win big from the $1.8 trillion annual spending on AI data center infrastructure in the long run.
Here are some no-brainer reasons to buy the stock
PwC's long-term AI infrastructure forecast clearly indicates that investments in AI data centers aren't a one-time thing. Chip upgrades will be needed to run more complex AI models, as well as to run AI inference applications that require more compute because of their advanced reasoning capability.
So, Nvidia's primary growth engine is going to keep running over the long run. At the same time, Nvidia is focused on tapping the massive addressable opportunity in emerging areas such as physical AI. As a result, it is easy to see why analysts have become more bullish about Nvidia's long-term growth prospects.
NVDA EPS LT Growth Estimates data by YCharts
A projected annual long-term earnings growth rate of over 50% is indeed healthy, considering that Nvidia is the largest company in the world. Moreover, Nvidia remains undervalued when its growth potential is taken into account. This is evident from its price/earnings-to-growth ratio ( PEG ratio ) of just 0.45, based on the annual earnings growth it could clock over the next five years, according to Yahoo! Finance.
The PEG ratio is calculated by dividing a company's trailing earnings multiple by its projected annual earnings growth. A reading below 1 suggests that the stock is undervalued, and Nvidia sits well below that threshold. So, Nvidia remains a solid long-term investment for anyone looking to add a growth stock to their portfolio, as the enormous investments in AI data center infrastructure can ensure years of healthy earnings growth for the company.
By Harsh Chauhan – Sep 18, 2026 at 11:52AM EST
Nvidia remains the leader in the AI chip market, and the secular growth of this space will ensure terrific long-term growth for the company.

### Article 345 · 2026-09-18 · barchart.com
IBM Once Held Nvidia's Spot as Tech's Biggest Name. The Stock Just Crashed 25%. Here's the Comeback Case.

Comeback stories can be some of the most interesting and perplexing setups in the stock market.
That is especially true in tech, where yesterday's leaders can quickly look outdated once the next big trend takes over. AI has already reshaped investor attention, but not every opportunity has to come from the newest or fastest-growing name. For dividend investors, an established company that can adapt, improve its growth profile, and keep rewarding shareholders can offer a very different kind of opportunity.
That's exactly what makes International Business Machines (IBM) worth looking at today. The storied stock has struggled this year, but parts of the business are starting to change, so much so that the potential for a grand comeback is becoming harder to ignore.
IBM Is Betting on AI and Hybrid Cloud for Its Comeback
International Business Machines is one of the oldest names in tech. At one point, IBM was almost synonymous with business technology, as its computers became a backbone for many large companies. It sold mainframes, business minicomputers, office equipment, and eventually personal computers.
In fact, during its heyday, the company held the position that Nvidia (NVDA) occupies today. It was that big.
But a lot has changed since then. After losing traction in the personal computer space and struggling to adapt to new software trends, the mighty "Big Blue" lost its spot and watched competitors capture the market share it once controlled.
Today, IBM is trying to make a comeback by repositioning itself in the new era of technology. The company's software business is once again catching investors' attention, and Red Hat is a big reason why.
Red Hat gives IBM a better position in the hybrid cloud. Many companies run their applications across private systems and public clouds. Its OpenShift platform helps businesses integrate applications across these environments, which is becoming more important as large companies expand their AI workloads.
IBM is now taking that strategy a step further by combining Red Hat with its own AI tools and infrastructure. This gives the company a bigger role in helping businesses build and manage AI across increasingly complex IT systems.
That gives IBM a clearer path to growth, but the real test is whether that strategy is translating into stronger financial performance.
Why Did IBM Stock Fall?
Let's start with IBM's annual performance snapshot.
So far, it's been looking good. Revenue grew around 8% in its latest annual report, while net income has improved significantly by 76%.
However, the chart above shows a massive sell-off around July 2026, and the reasons are in the company's 10-Q for the second quarter of 2026.
First, IBM expected a year-over-year decline because the z17 mainframe launch back in June 2025 set the bar too high. But it was worse than expected, as Infrastructure segment revenue and segment profit fell 7.4% and 13.4%, respectively.
Second, management admitted that several large deals didn't close on schedule, while some clients have shifted spending toward servers, storage, and memory to lock in supply-constrained hardware before expected price increases. That helped IBM's Distributed Infrastructure business, which grew 37% for its best quarter on record, but it pulled money away from the more lucrative mainframe deals.
Overall, management says that Q2 performance was "below their expectations," disappointing market experts. And so, the stock fell more than 25% after the report.
But the recovery case isn't entirely gone.
Why IBM's Recovery Narrative Is Still Intact
According to management, the Q2 problems stem from deal timing and its own execution.
Crucially, the clients that are paying for its services are still there. IBM's business is built around large enterprises that often have lengthy sales cycles, complex deployments, and multiyear technology commitments. So as long as those relationships remain intact, revenue recovery will be a matter of time. Right now, it's just being shuffled further out in the year.
And, again, Red Hat remains a big part of this recovery strategy. OpenShift helps IBM compete in hybrid cloud, while its AI tools give customers another reason to keep using the company's services.
So, yes, this quarter's optics were bad, but it could be worse, and the recovery narrative is still in play as long as IBM can turn its existing customer relationships and AI and cloud businesses into real revenue growth. Ultimately, this quarter is either just a temporary speed bump or a sign of things to come. We'll have to see.
IBM's recovery may still be uneven, but the dividend gives investors something more consistent to work with.
The company pays a forward annual dividend of $6.76, which translates to a current forward yield of approximately 2.72%. But its dividend payout ratio is only around 55%, meaning just over half of its earnings go to dividends, leaving plenty of room for reinvestment and dividend growth.
Speaking of dividend growth, the company has raised its dividends for 31 consecutive years, making it a Dividend Aristocrat and giving income investors a long track record of growing payouts. Overall, the company's consistent shareholder returns add another layer to IBM's comeback story, especially as the rest of the business continues to find its footing.
Based on the numbers, even Wall Street is taking IBM's recovery more seriously.
A consensus among 24 analysts rates IBM stock a "Moderate Buy", with as much as 54% upside over the next year. Even through the Q2 crash, analysts have maintained an overall buy rating, meaning they see the recent setbacks as temporary.
Better yet, IBM stock is now trading at just 20x forward price-to-earnings. Compared with the sector median of 28x, IBM looks cheap.
IBM's comeback still needs time to play out, but the case for owning it is becoming increasingly interesting. The company is rebuilding around areas where it already has deep relationships with large businesses and where demand is still growing. That's a viable business model, and one that can sustain tremendous growth if everything plays out right.
That makes IBM a fascinating recovery story to watch. If the company can keep improving without losing its income appeal, the stock could become increasingly difficult for investors to ignore.
On the date of publication, Rick Orford did not have (either directly or indirectly) positions in any of the securities mentioned in this article. All information and data in this article is solely for informational purposes. This article was originally published on Barchart.com

### Article 346 · 2026-09-18 · mobileworldlive.com
Nvidia CEO predicts chip sales will double next year

By Michael Robuck
Nvidia CEO Jensen Huang ( pictured ) reportedly tipped the company’s chip sales to double in 2027, driven by the increased adoption of AI across various industries.
Bloomberg reported Huang made the prediction yesterday (17 September) during an event in the UK hosted by King Charles III. Nvidia is the biggest seller of AI accelerators, which are chips used to develop and power AI models.
Nvidia does not disclose chip sales in its financial results, but in its most recent earnings stated it expects 70% revenue growth in fiscal 2028, amounting to $673 billion.
Get breaking news, exclusive insight, and expert analysis - before anyone else.
While the US and the world at large grapple with the prospect of slowing the development of AI models due to concerns they may be dangerous, Huang has remained a staunch proponent.
He reportedly said companies must take responsibility and make sure their AI software and services are safe before releasing them.
NBC News reported US President Donald Trump called Huang during an AI event on 14 September to voice his full support for unfettered development.
- Mike Robuck is the U.S. Editor at Mobile World Live. He joined the Mobile World Live staff in February of 2022. Prior to joining GSMA, he was editor of FierceTelecom and of Light Reading’s Telco Transformation microsite. He has a long history of reporting on the telecommunications industry.
By Kavit Majithia
By Chris Donkin
By Amiya Johar

### Article 347 · 2026-09-18 · benzinga.com
Ross Gerber Sees Jensen Huang’s Charisma As Part Of Nvidia’s Edge, Says ‘This Is Why I Own Nvidia’ After Dreamforce Exchange With Marc Benioff: 'Big is Unnecessary'

Ross Gerber Sees Jensen Huang’s Charisma As Part Of Nvidia’s Edge, Says ‘This Is Why I Own Nvidia’ After Dreamforce Exchange With Marc Benioff: 'Big is Unnecessary'
Investor Ross Gerber highlighted Nvidia Corp.'s CEO Jensen Huang's charisma at Salesforce Inc.'s Dreamforce 2026, saying a playful exchange with Salesforce CEO Marc Benioff showed part of what he sees in Nvidia's leadership.
"This is why I own Nvidia," Gerber wrote in an X post on Wednesday while sharing the clip. Salesforce listed Huang among its main Dreamforce keynote speakers. Gerber, CEO of Gerber Kawasaki, has remained bullish on Nvidia and in August said the stock could eventually reach $450 after the chipmaker's second-quarter results.
Investor and writer Trung Phan described the Dreamforce moment as a potential "Benioff frame-mog," slang for being physically overshadowed by someone with a larger frame. Huang turned the height difference into a joke.
"Look, I'm very good friends with both of you guys…I always feel like I need to stand on a chair…I just wanna let you guys know that when I'm on an airplane, I'm a lot more comfortable than you guys. And so, through human evolution, they realized that big is unnecessary. There's about a million years of evolution between you and me," Huang said, addressing Benioff.
https://twitter.com/GerberKawasaki/status/2100400274074738784
Dreamforce Spotlights Nvidia's Growing AI Role
Nvidia's Dreamforce recap said Huang walked into the crowd with Benioff alongside him as they discussed AI's next phase. Salesforce also unveiled Koa, its first CRM reasoning model for Agentforce, built on Nvidia Nemotron 3 Super and running inside Salesforce infrastructure.
Gerber has repeatedly tied his Nvidia optimism to Huang and the company's execution. In May, he urged investors to "pay attention" to Nvidia and Micron Technology Inc. as Huang described AI infrastructure as the beginning of a decade-long buildout. After Nvidia's August earnings, Gerber called the company "undervalued."
Nvidia Growth Reinforces Gerber's Bullish View
Nvidia last month reported a fiscal second-quarter revenue of $96.2 billion, up 106% year over year. Data Center revenue rose 117% to $89 billion, while the company forecast third-quarter revenue of $108 billion, plus or minus 2%.
Huang also used Dreamforce to argue that AI spending remains strong. He said companies are rapidly building Nvidia-powered "AI factories" and described the infrastructure spending flywheel as "really, really flying."

### Article 348 · 2026-09-18 · finance.yahoo.com
NVIDIA Vs Intel Corporation (NASDAQ:INTC): Here’s The One Jim Cramer Likes

Chip maker Intel Corporation (NASDAQ: INTC ) has become one of the hottest stocks in today's market with year-to-date gains and valuation both being richer than AI GPU giant NVIDIA. The shares are up by more than 170% year-to-date while the forward P/E ratio of 54.64 is also higher than NVIDIA's 23.58. In his morning appearance on the 15th, Cramer discussed Intel Corporation (NASDAQ:INTC) and insisted that NVIDIA's GPUs would experience greater demand:
"No, I want to get it off the plate. I mean I think that Intel's doing so well. But Intel's CPU, and people are more focused on GPU, which is Jensen, than CPU. Because we are going to have robots and we are going to have autonomous driving, no matter what."
With the shares closing 7.7% higher on Thursday, the CNBC TV host discussed Intel Corporation (NASDAQ:INTC) in a series of tweets:
"Intel is now at last reacting to the work of Lip-Bu Tan post the destruction of its stock at the hands of Situational Unawareness. The stock lapped up the secondary. I think the foundry is key to American securityTTTTTTT
"Club name Intel, everyone knows as my fave, isn't done."
The bit about agentic AI CPUs has driven Intel Corporation (NASDAQ:INTC)'s narrative significantly in 2026. The firm's second quarter results saw its data center and server business's revenue sit at $6.26 billion to beat analyst estimates of $5.37 billion. The growth for the business was 59% which suprassed overall revenue growth of 25%.
Additionally, unlike NVIDIA, Intel Corporation (NASDAQ:INTC) can also rely on its foundry business to generate tailwinds. The firm is currently aiming to establish a foothold in the global contract chip fabrication market through the Intel Foundry business. On this front, CEO Lip-Bu Tan outlined that the firm was optimistic about volume production for the next-generation 14A chip manufacturing process technology. The movement in Intel Corporation (NASDAQ:INTC)'s shares on Thursday also came as news started floating around of the firm potentially partnering up with Korea's SK hynix to manufacture memory chips in the US. The report came from Reuters, and SK hynix later clarified that nothing had been finalized.
At the same time, while the data center business is booming, the large scale capital expenditure requirements for setting up chip foundries mean that Intel Corporation (NASDAQ:INTC) continues to pour its profits into Foundry. During Q2, the segment reported a $2.1 billion operating loss while external customer revenue represented 5% of the $5.8 billion overall revenue. External customer revenue is a key metric for the foundry business's success, as it determines market penetration. Not to mention, the strong share price performance has led to some, such as Piper Sandler, to warn that near-term upside might be limited.
For NVIDIA Corporation (NASDAQ: NVDA ), the narrative is tied to AI chip demand. The importance of sustained demand was clear at Salesforce's Dreamforce conference, where CEO Jensen Huang insisted that AI development did not have to slow down. His remarks followed Anthropic's Dario Amodei, who outlined that safety concerns necessitated a slowdown, but Huang countered by arguing that labs with safety concerns should delay launching products until said concerns had been resolved, instead of pushing for a broader slowdown.
Huang's comments came as NVIDIA Corporation (NASDAQ:NVDA)'s data center revenue doubled to $89 billion in Q2 for a 117% bump and its Q3 guidance implied a 117% annual revenue growth. Yet, with the FY28 guidance implying a growth slowdown to 70%, the timeline might be uncertain for the robotics and other tailwinds Cramer discussed. Piper Sandler is quite optimistic about NVIDIA, though, as it initiated coverage with an Overweight rating and a $300 price target on the back of 80% share in AI compute and other factors.
Looking at hedge fund sentiment, 285 funds held a stake in NVIDIA Corporation (NASDAQ:NVDA) during Q2, which was significantly higher than the 138 that had owned a stake in Intel, according to Insider Monkey's data. Short interest as a percentage of float was higher for Intel at 2.88% compared to 1.29% for NVIDIA Corporation (NASDAQ:NVDA).

### Article 349 · 2026-09-18 · gurufocus.com
Nvidia CEO Delivers Stunning Prediction About Chip Sales

Nvidia ( NASDAQ:NVDA ) CEO Jensen Huang expects the company to sell roughly twice as many chips next year as it does this year, pointing to continued demand for artificial intelligence technology across industries.
Huang made the projection while attending an AI-focused meeting hosted by King Charles III in Scotland. He said businesses and governments in many countries continue to invest in AI because of its potential economic benefits.
The forecast comes after Nvidia projected about $673 billion in revenue for fiscal 2028, representing growth of roughly 70% from the prior year. The company does not disclose its total chip sales volume, making the unit-growth outlook difficult to compare directly with its revenue forecast.
Nvidia's portfolio includes data-center graphics processors such as Blackwell and Rubin, along with CPUs, networking chips and processors used in robotics and vehicles. Huang previously said the company shipped six million Blackwell GPUs over four quarters.
Huang also joined executives from Google DeepMind, OpenAI and Anthropic at the Scotland meeting, where discussions included AI safety and product testing.

### Article 350 · 2026-09-18 · computerweekly.com
Nvidia Doesn't Sell Chips. It Sells a Flywheel

Nvidia Doesn't Sell Chips. It Sells a Flywheel
Nvidia's greatest invention maybe building a business that continuously manufactures demand for its own products
By Judah Taub
Nvidia is now one of the most valuable companies in history. The standard explanation is straightforward: it built the world's best AI chips, created CUDA , executed brilliantly under Jensen Huang and arrived at precisely the right moment.
All of that is true. It is also incomplete. Nvidia's greatest invention may not be a semiconductor. It may be a business that continuously manufactures demand for its own products.
For decades, investors have explained successful technology companies using familiar ideas: economies of scale, network effects and switching costs. Nvidia certainly benefits from all three. But they don't fully explain why its lead has become so difficult to challenge.
The company has built something different. Call it a recursive moat.
A network effect makes an existing product more valuable as more people use it. A recursive moat goes one step further. It creates entirely new demand for the product itself. Every success strengthens the system that produces the next success.
That is exactly what Nvidia has built.
Better GPUs attract the world's best AI researchers. Those researchers found the next generation of AI companies. Those companies build products that convince thousands of other businesses to adopt AI. Every successful AI application increases global demand for computing infrastructure. That demand generates the profits Nvidia uses to build the next generation of chips.
The loop doesn't merely repeat. It compounds. But Nvidia is no longer content to let this happen naturally. It has begun accelerating the flywheel itself.
Over the past several years Nvidia has invested in frontier model companies, robotics startups, enterprise software firms and infrastructure providers. It has partnered with hyperscalers, helped finance AI factories, worked with infrastructure investors and, increasingly, supported customers building massive compute clusters.
Viewed individually, these deals appear unrelated. Viewed together, they reveal a coherent strategy. Nvidia isn't simply investing in promising companies, it is investing in tomorrow's demand for Nvidia.
Every startup it helps build is a future customer. Every AI factory it helps finance becomes another buyer of Nvidia hardware. Every successful AI application inspires hundreds of entrepreneurs to launch companies of their own.
Its customers don't simply consume its products. They create the next generation of customers. CUDA demonstrates the same principle. Most people think of CUDA as a software toolkit. Strategically, it is an engine for manufacturing demand.
Developers learn CUDA because companies use Nvidia hardware. Universities teach CUDA because industry demands it. Researchers publish using CUDA because the ecosystem already exists. Software libraries expand because millions of developers contribute to them.
Every new participant makes Nvidia more valuable for the next. The ecosystem continuously reinforces itself. This is why Nvidia's competitive advantage extends far beyond semiconductors.
Competitors often ask the wrong question: Can we build a chip that is ten percent faster?
Perhaps they can.
But they would still need to reproduce two decades of software, developers, universities, research, cloud integrations, networking, startup investments, infrastructure partnerships and financing relationships. They would have to recreate the system. That is vastly harder than reproducing the product.
There is a broader lesson here. The Industrial Revolution rewarded companies that built better factories. The internet rewarded companies that built better networks. The AI era may reward companies that build systems capable of generating their own future demand. Nvidia may simply be the first example.
Entrepreneurs often ask how to acquire the next customer. The more interesting question is how every customer can make the business stronger for the one that follows. Products improve, platforms scale, but recursive ecosystems do something more powerful, they manufacture demand. That may prove to be Nvidia's greatest invention.
Judah Taub is founder and managing partner of Hetz Ventures, former Israeli intelligence officer, and adviser to governments on AI, cybersecurity and defense strategy.

### Article 351 · 2026-09-18 · qz.com
Jensen Huang forecasts Nvidia chip sales to double in 2027

The Nvidia CEO made the projection at a summit convened by King Charles III in Scotland, citing AI demand across industries and economies
Nvidia $NVDA CEO Jensen Huang forecast on Thursday that the company will sell twice as many chips next year as it does this year, pointing to AI investment across industries and countries as the driver of continued growth.
"I expect Nvidia to sell twice as many chips this next year as we do this year," Huang told reporters on the sidelines of a summit convened by King Charles III in Scotland, according to Bloomberg . "The reason for that is because AI has so much contribution to the benefits of different industries, different economies, and you can see that in almost every single country that we're in, people want to invest in AI."
The forecast adds to an already bullish financial outlook. Last month, Nvidia projected revenue growth of 70% in its next fiscal year, and the company said at the time that revenue could double if supply were sufficient to meet demand, according to Bloomberg. That projection — roughly $673 billion for the fiscal year ending January 2028 — sent analyst expectations higher, according to CNBC.
Nvidia does not disclose the total number of chips it sells. While its data center GPUs — including the Blackwell and Rubin lines — are its most prominent products, the company's portfolio spans a wide range of semiconductors: CPUs, switch chips, optical networking chips, laptop processors, chips for robotics and automotive applications, and the processor powering Nintendo's Switch 2 gaming console.
Nvidia stock gained as much as 2.8% in Thursday trading in New York.
Huang was at the Scotland summit alongside representatives from Google $GOOGL DeepMind, OpenAI, and Anthropic, where the group addressed AI safety — a subject that has surged to the forefront of public debate following warnings from AI researchers that the most advanced systems have grown beyond human control. Huang said companies bear responsibility for ensuring their products are safe before release.
"When a product is not safe, we should hold it back and keep engineering it," Huang said. "If it's not ready, just hold it back. You should go as fast as you can, but no faster than that."
The Scotland summit came days after Huang appeared onstage at the All-In Summit in Los Angeles , where President Donald Trump phoned in live to dismiss AI safety concerns as "a hoax." Trump called data centers "the oil of the next 20, 25 years" and told Huang, "I'm with you all the way." Huang had challenged the empirical basis of safety warnings at that event, saying predictions about AI risk were "not grounded in science."

### Article 352 · 2026-09-18 · finance.yahoo.com
Nvidia-Backed Cloud Platform Nscale Files For IPO — NVDA Stock In Focus

London-headquartered Nscale is seeking a New York Stock Exchange listing under the ticker symbol NSCL.
Revenue surged to $140.6 million for the first six months of 2026, up from $10.4 million a year earlier, while net losses expanded to $1.02 billion.
The firm maintains close partnerships with Nvidia, Microsoft, and Anthropic.
London-based AI data center company Nscale has filed publicly for an initial public offering (IPO) in New York to acquire the infrastructure needed to meet the global demand for artificial intelligence compute power.
The company, a neocloud provider that rents out AI computing resources, plans to list its shares on the New York Stock Exchange under the ticker symbol NSCL. Goldman Sachs Group Inc., JPMorgan Chase & Co., and Morgan Stanley are leading the offering.
The company did not disclose the size and scope of its listing in its filings. However, a Bloomberg report cited that the company is seeking to raise as much as $3 billion in the IPO.
According to regulatory filings with the U.S. Securities and Exchange Commission, Nscale reported rapid top-line growth alongside escalating losses. For the six-month period ending June 30, the company generated $140.6 million in revenue, up significantly from $10.4 million during the same period in the prior year. However, net losses expanded to $1.02 billion for the period, compared to $368.9 million in the previous year.
Originally spun off from a cryptocurrency mining enterprise in early 2024, Nscale reached a private valuation of around $14.6 billion following a March Series C funding round.
Data Infrastructure And Industry Partnerships
Nscale manages hyperscale AI hubs located in Norway, Portugal, Texas, and West Virginia, controlling over 10 gigawatts of power capacity as of August 2026. The firm holds about $103 billion in total contract value. Major commitments include a $45-billion agreement with Anthropic to utilize compute resources at Nscale's flagship Monarch Compute Campus in West Virginia.
The company also maintains deep operational ties with Nvidia Corp., which holds a stake of more than 5% through warrants issued during a 2025 financing round. Nscale explicitly highlighted its hardware reliance on Nvidia as a primary risk factor in its SEC paperwork.
Nscale's board includes prominent industry figures, including former Meta Platforms Inc. (META) executives Sheryl Sandberg and Nick Clegg. Major shareholders owning 5% or more of the company include investment firm Aker, Sandton Capital Partners, and a trust linked to founder and Chief Executive Officer Josh Payne.

### Article 353 · 2026-09-18 · futurumgroup.com
Cisco and NVIDIA Bring Splunk AI to Enterprises

Publication Date: September 18, 2026
Cisco and NVIDIA expanded their partnership to bring Splunk AI into customer-controlled environments. Local deployment addresses sovereignty requirements, while the broader security and cost-management announcements leave operational results to be demonstrated.
The Cisco–NVIDIA relationship and local Splunk AI deployment.
Sovereignty requirements and the need for hybrid data access.
Token spending visibility and changes to platform pricing.
Agentic security operations and Splunk’s development agreement with AWS.
The News: Cisco introduced Cisco AI POD for Splunk at Splunk .conf in Denver on September 15, 2026, extending its NVIDIA partnership to support self-managed Splunk AI. The AI POD and AI Assistant are available now; Agent Launchpad is due later this year, with NVIDIA Nemotron models following in the coming months.
The company also announced Tokenomics capabilities, expanded Agent Observability into its cloud offerings, and added agentic security and Exposure Analytics capabilities. Splunk and AWS agreed to multi-year joint security development, while Activity-Based Pricing is scheduled for this fall.
Analyst Take: Cisco’s most consequential move here is bringing Splunk AI to customers who need to keep sensitive data in their own environments. The NVIDIA partnership provides the infrastructure for that step, while support for local and cloud environments reflects the different restrictions customers place on their data. Customers now have more options for deploying AI, although allowing agents to take on more security work still requires evidence of their effectiveness.
NVIDIA Gives Splunk AI a Way Into the Data Center
The Cisco–NVIDIA partnership extends Splunk AI to customers that previously could not use it because their sensitive data had to remain outside the cloud. Cisco AI POD for Splunk brings together Cisco infrastructure, NVIDIA accelerated computing, and Splunk’s Kubernetes-native runtime in a configuration validated for Splunk workloads.
Customers can also deploy the software on their own infrastructure, with implementation support available from partners. The rollout remains incomplete: AI Assistant is available now, while Agent Launchpad is due later this year, and NVIDIA Nemotron models will follow in the coming months. For buyers, the immediate benefit is access to local Splunk AI, and deployment decisions should reflect what the companies can deliver today.
Hybrid Support Reflects How Customers Must Handle Data
Some organizations have no option but to move sensitive data to the cloud, regardless of the AI capabilities available there. Splunk AI now supports on-premises, private cloud, and air-gapped environments, while Agent Observability also extends into Splunk Observability Cloud and Cisco Cloud Control. These deployment options are particularly relevant to the healthcare, finance, and government organizations whose data must remain within their own environments.
Federated Search extensions to AWS CloudWatch Lake and Databricks, together with MCP-enabled Catalog Discovery, address another part of the problem by helping teams find and analyze distributed data without first migrating it. Customers should assess deployment and data access together, since keeping AI within an approved environment is useful only if it can reach the information needed for its work.
Customers Need to Know What Their Agents Cost
Tokenomics tackles a familiar budgeting problem: spending that becomes apparent only when the invoice arrives. It tracks token expenditure across agents and employee use of Claude Code, Codex, and Cursor, with consumption forecasting through Cisco Deep Time Series Model still to come.
Agent Observability brings spending information together with performance evaluation and runtime guardrails intended to block unsafe or inaccurate actions. Activity-Based Pricing adds a further consideration this fall, when Splunk plans to give search and ingest equal weight in its pricing. Buyers should use these capabilities to assess the cost of individual workloads before deciding whether wider agent adoption makes financial sense.
AWS and Splunk Still Have Details to Provide
The AWS agreement sets a direction for joint security development, although customers still need to know which products it will produce and when. Splunk’s expanded Agentic SOC Workforce covers detection engineering, threat hunting, investigation, response, and governance, with more than 1,300 security integrations.
Exposure Analytics adds asset coverage and historical context, but the announcement gives buyers no quantified measure of the resulting improvement in security operations. The Futurum Group’s 1H 2026 Cybersecurity Market Sizing & Five-Year Forecast projects $77 billion in incremental annual spending by CY2031 across Cloud Security, Security Operations & GRC, Data Security, and Application Security. Cisco is pursuing a substantial opportunity, and earning more responsibility inside the SOC will require evidence that these capabilities improve investigations while keeping analysts in control.
Will Agent Launchpad and NVIDIA Nemotron models arrive within the announced windows, and which local workflows will each support at release?
How effectively will Federated Search and MCP-enabled Catalog Discovery provide relevant context across data sources that customers keep in separate environments?
When will Tokenomics forecasting become available, and how accurately will it project consumption before a billing period ends?
What will Activity-Based Pricing mean for customers with different search and ingest patterns?
Can the Essentials and Premier security editions demonstrate reduced alert noise and faster remediation while preserving analyst control?
Which products will emerge from the AWS agreement, and when will customers be able to evaluate them?
See the complete announcement on Splunk AI and its expanded security capabilities on Cisco’s website.
Cisco Q4 FY 2026 Earnings Point to Broader AI Infrastructure Demand
Cisco Live 2026: Platform, Silicon, and Security for the Agentic Era
Can Cisco Widen Splunk’s Agentic SOC Capabilities With WideField?
Fernando Montenegro serves as the Vice President & Practice Lead for Cybersecurity & Resilience at The Futurum Group. In this role, he leads the development and execution of the Cybersecurity research agenda, working closely with the team to drive the practice's growth. His research focuses on addressing critical topics in modern cybersecurity. These include the multifaceted role of AI in cybersecurity, strategies for managing an ever-expanding attack surface, and the evolution of cybersecurity architectures toward more platform-oriented solutions.
Before joining The Futurum Group, Fernando held senior industry analyst roles at Omdia, S&P Global, and 451 Research. His career also includes diverse roles in customer support, security, IT operations, professional services, and sales engineering. He has worked with pioneering Internet Service Providers, established security vendors, and startups across North and South America.
Fernando holds a Bachelor’s degree in Computer Science from Universidade Federal do Rio Grande do Sul in Brazil and various industry certifications. Although he is originally from Brazil, he has been based in Toronto, Canada, for many years.
Futurum Research examines IBM’s Q3 FY 2026 earnings, including software execution, infrastructure deal recovery, sovereign AI demand, and consulting delivery efficiency....
Futurum Research analyzes SAP’s Q3 FY 2026 earnings, examining AI-led cloud migration, enterprise data integration, and the shift toward adoption-based economics....
WEKA and Smartbird announced a strategic partnership to deliver sovereign managed AI infrastructure for regulated enterprises in government, healthcare, and financial services, combining NeuralMesh software with dedicated clusters....
SCSK Security launched a vendor-neutral Zero Trust Architecture Design Service using MITRE ATT&CK and NIST standards to help enterprises justify investments and optimize multi-cloud security over 3-6 months....
Western Digital's Q1 FY2027 revenue surged 55% to $4.38 billion with non-GAAP EPS jumping 161% to $4.64, driven by hyperscaler and cloud AI-storage investments positioning the company to capitalize on...

### Article 354 · 2026-09-19 · supercarblondie.com
We could see the world's first $10 trillion company arrive in less than two years

We could see the world's first $10 trillion company arrive in less than two years
A company worth $10 trillion once sounded like something that belonged in a sci-fi movie, but we could be getting surprisingly close to that milestone.
One company already has a market capitalization of around $5.3 trillion, thanks largely to the huge demand for the chips powering the artificial intelligence boom.
Now, one new analysis suggests the company could potentially double in value and become the world’s first $10 trillion company as early as 2028.
And the numbers behind the prediction are pretty wild.
Nvidia has become one of the biggest winners of the AI revolution , with its graphics processing units, or GPUs, providing much of the computing power needed to train and run today’s AI systems.
The company’s chips are used across massive data centers , and demand has remained so strong that customers have been ordering computing equipment well ahead of when they actually need it.
That has given Nvidia unusually strong visibility into future demand.
According to The Motley Fool , Nvidia’s CFO Colette Kress said during the company’s fiscal 2027 second-quarter earnings call that the company was expecting 70 percent revenue growth for fiscal 2028, which ends in January 2028.
That’s a huge number for any company, let alone one already worth more than $5 trillion.
The math behind a $10 trillion Nvidia
The prediction becomes easier to understand when you look at the numbers.
Wall Street analysts expect Nvidia to generate around $411 billion in revenue in fiscal 2027.
If the company then achieved the 70 percent growth rate it has forecast for fiscal 2028, that would push annual revenue to nearly $700 billion.
The Motley Fool analysis then assumes Nvidia could convert around 60 percent of that revenue into net income, resulting in roughly $419 billion in profit.
At that point, Nvidia would not necessarily need an enormous valuation premium to reach the $10 trillion mark.
A $10 trillion market capitalization divided by approximately $419 billion in earnings works out at around 24 times earnings.
That’s roughly in line with the valuation multiple used for the S&P 500 in the analysis, meaning Nvidia could theoretically reach the milestone without investors having to value it at some extraordinary level.
Of course, that’s a projection rather than a guarantee.
Nvidia would need to maintain enormous growth while continuing to benefit from the world’s seemingly insatiable appetite for AI computing power.
Competition, changing AI technology, a slowdown in data center spending , or a shift in investor sentiment could all change the picture.
But if Nvidia delivers the growth it has projected, the world’s first $10 trillion company could arrive much sooner than many people might expect.
And with Nvidia already sitting at around $5.3 trillion, it would only need to roughly double from its current valuation to get there.
Daisy is a technology and automotive journalist covering artificial intelligence, consumer tech, Apple news, cryptocurrency, emerging technologies, and transportation innovation. Since joining the team in 2025, she has reported on everything from AI-powered startups and major iOS updates to viral car stories and the latest developments shaping transportation and the digital economy.
Drawing on her background in automotive journalism and a degree in History and Journalism from Goldsmiths, University of London, Daisy specializes in breaking down complex topics into clear, engaging reporting for a global audience. Her work spans cutting-edge technology, innovative vehicles, and the people driving change across both industries.
Daisy has gained first-hand access to some of the world's most talked-about technologies and innovators, including meeting Tesla's Optimus humanoid robot during its first European appearance in London. She has also discussed the future of space exploration with an astronaut, bringing unique insights and real-world perspectives to her coverage of emerging technology.

### Article 355 · 2026-09-19 · xda-developers.com
I tested the leaked DLSS 5, and it's doing something to old games that Nvidia probably didn't intend

By Abhinav Raj
It has been almost twenty days since it came out, but the internet is mysteriously torn on the subject of DLSS 5 . On one hand, it has been touted as perhaps one of the worst uses of artificial intelligence in gaming , being one that deviates from artistic intent in video game design and slaps a filter on everything that makes it look like an AI interpretation of what the game should be.
On the other hand, YouTube videos featuring the use of the new Neural Rendering feature have been stacking up millions upon millions of views. It's clear that whether you love Nvidia's latest "AI black magic" or hate it, there's no ignoring it. So I've decided to stop ignoring it and test it on three of my most beloved old games to see what it can bring to the table.
The Witcher 3: Wild Hunt
With DLSS 5, it finally seems like Geralt's mutations have reached his face after eighty years of monster hunting. This is a game that I have returned to more times than I can count, always finding something I had not seen before, and that is exactly why it sits at the heart of this test. I wanted to know what the world of the Witcher would feel like when it's rendered photorealistically , and whether that made it more immersive or less. It also happens to be the most face-forward title on this list, so it is also where reconstruction is likeliest to read "wrong".
Well, so, it did. Geralt, quite simply, was not the Geralt any fan of the trilogy would recognize. The skin is overly defined, waxy, and precisely the uncanny valley nightmare I came searching for. It's a stranger wearing Geralt's face, and every bit of it feels like a masquerade.
This should've been enough for me to drop the feature altogether, but Triss absolutely ruined the verdict beyond any standards of measure. In a latern-lit dialogue in the shipyard with Djikstra set within the same universe that failed Geralt so badly, neural rendering flattered her instead.
Why? That's something I cannot answer with absolute certainty. I can only speculate as to why, since Nvidia has published next to nothing about what these models were trained on. My best guess is that a conventionally human face gives reconstruction something familiar to reach for, while a mutated Witcher that's pallid and scarred by design sits outside whatever the model considers a face. If that is indeed what's happening, then DLSS 5 is not neutral about art direction at all, which seems to be the one of the primary concerns of the community at large.
By Rich Edmonds
There's finally something creepier than the Joker in Gotham City
Batman: Arkham Knight is a game that possibly rivals The Witcher 3 in terms of its contemporary relevance. The game came out in 2015 when I was just readying myself for high school, and the weeks leading to its launch were also the weeks that this game was the only thing that was ever talked about in gaming enthusiast circles. It also predates DLSS, so it takes the cruder inject route rather than the clean swap that others on the list rely on.
What the model, and the method produced together, was something that should've bothered me, but it left me impressed instead. Gotham City in particular is where DLSS 5 would shine the best, because it's got everything that photorealism stands to gain immensely from. Rain on the surface, overcast skies, wet asphalt throwing back the lights on the street, and the ominous ambience in general that adds to the eeriness of the atmosphere.
Purists would argue that it violates every rule of artistic intent and transgresses a boundary that AI should never, and yet, to me, it produced the Batman the way I always imagined him, being heavier and more flesh than silhouette, with a hint of Ben Affleck in the face that you'll never see me complain about. Perhaps the creepiest thing here is Batman himself, and with a touch of neural rendering, he looks every bit as fearsome as Gotham needs him to be.
By Samarveer Singh
The wasteland has got a texture pack from hell, and it oddly suits it
When Metro Exodus first came out, I was just a 19-year-old with an Xbox One X, which happened to be the only device in my home with a dedicated GPU. As such, this was a world that I was familiar with before I ever got around to experiencing it on the PC. It's one of the reasons why it's here on this list at all, because the lighting, volumetric skies and particle geometry make it a good measure of what neural rendering can do for an old title.
For me, it simply works. This is a first-person shooter that draws most of its vibe from its atmosphere, and that's precisely one aspect that DLSS 5 has a potential to add depth into. The dessicated corpses gain definition, snow breaks into grains, and the leather and buckles on Artyom's gauntlet have an aspect of wear and tear that I had never noticed. For me, it's definitely improved the visuals, and for a game like this, that's an automatic upgrade.
So, is it a nightmare or is it refreshing?
It seems to be a bit of both, and which one gamers get depends on what's actually on the screen. You can make it elevate the rain effects, particle geometry, add depth to atmosphere, and make near about any other visual more photoreal in a way that it makes a decade-old title flattering, but if you point it at a face you know too well, it has a chance of handing you a total stranger.
It's also definitely worth noting that what I tested was a leaked build injected through ReShade and RenoDX, with one title relying on a cruder route because it came out before DLSS was a thing at all. The official implementation , whenever it arrives properly on my Ada Lovelace GPU, will almost certainly behave differently, and I'm hoping probably better. After all, in all likelihood, Nvidia didn't expect their neural rendering trick reserved for the Blackwell series to be used on old games on a 40-series GPU like this.

### Article 356 · 2026-09-19 · cryptonews.net
Matt Hougan Compares Tokenization’s Rise to Nvidia’s Early AI Surge

Matt Hougan Compares Tokenization’s Rise to Nvidia’s Early AI Surge
19 September 2026 05:32, UTC
Matt Hougan says tokenization is entering a longer phase of financial adoption , comparing its early trajectory with NVIDIA’s AI rise.
His view comes as the SEC opens a regulated route for tokenized stocks and S&P Global agrees to acquire OpenZeppelin.
Together, the developments show how blockchain infrastructure is moving deeper into traditional markets while DeFi and onchain assets gain institutional attention.
Tokenization has moved closer to the center of U.S. financial-market development, giving Bitwise CIO Matt Hougan a fresh reason to compare the sector with the early stages of the artificial-intelligence boom. On September 17, Hougan argued that the world is moving onchain and described tokenization as a multi-year transformation rather than a short-lived market theme.
His comparison focuses on timing. ChatGPT launched in November 2022 while NVIDIA traded around $16. About a year later, NVIDIA had reached $46, a 176% increase, making the scale of the AI opportunity more visible. Hougan noted that NVIDIA now trades around $219 and used that progression to argue that recognizing a major shift does not mean the opportunity has already passed .
Alerts, real-time prices, and market news — all in one app
4.8 based on 40K reviews in the App Store and Google Play
Tokenization is a mega trend. Just today, the SEC created a pathway for tokenized stocks to trade in the US, S&P acquired @OpenZeppelin, and DeFi assets are ripping. If you had doubts before, today should put them to rest. The world is moving onchain.
— Matt Hougan (@Matt_Hougan) September 17, 2026
For tokenization, he pointed to recent developments as evidence that adoption is moving beyond experimentation. The SEC’s latest action provides a regulated path for certain venues to trade tokenized U.S. stocks on blockchain-based infrastructure. The framework covers tokenized NMS stocks that preserve shareholder rights such as dividends and voting, while synthetic products that only track stock prices remain outside the exemption. Issuers also receive a 30-day period to object to third-party tokenization.
Tokenization Gains A U.S. Regulatory Path
The SEC’s temporary exemption lasts up to five years and applies under specific conditions, including limits around participating venues, securities and trading activity. The agency said the framework is intended to facilitate innovation while it considers broader policy. This creates a clearer lane for companies developing blockchain-based equity infrastructure.
The regulatory move arrived alongside S&P Global’s agreement to acquire OpenZeppelin, adding another institutional signal. OpenZeppelin’s smart-contract technology supports major stablecoins, tokenized funds and DeFi applications. The company says its contracts have facilitated more than $37 trillion in transferred value and that it has completed more than 900 security engagements.
NVIDIA Parallel Highlights Tokenization’s Early Stage
Hougan’s analogy rests on the idea that technology megatrends can continue expanding after investors first recognize them. He argues that tokenization has already attracted attention, but its broader financial impact may still be developing as regulated trading, security standards and institutional infrastructure converge.
The comparison does not establish that tokenization will follow NVIDIA’s price path. Instead, it highlights Hougan’s view that blockchain-based financial rails can become a long-duration market transition . As traditional financial firms add tokenized products and established infrastructure providers enter the sector, the onchain model is gaining more connections to conventional capital markets.

### Article 357 · 2026-09-19 · barchart.com
Here’s Another Little-Known Firm Jensen Huang’s Nvidia Is Quietly Backing

Nvidia (NVDA) has invested in another AI name most investors have never heard of. This time it's Cohere, a Toronto-based company in talks to raise up to $3 billion. According to a Bloomberg report, the round would value the company at $20 billion. That is nearly triple the $7 billion valuation it carried just a year ago. If it closes, it would be the largest funding round ever for a private Canadian startup. What I find interesting is where the funding is coming from. The Canadian government is putting in money directly, and Germany is in talks to join too.
​Cohere isn't chasing consumers the way most AI names do. Companies like OpenAI build chatbots for regular people. Cohere builds AI that banks, governments, and hospitals can run on their own servers. This keeps their data inside the building. That pitch is called "sovereign AI," and it's landed Cohere deals with the Royal Bank of Canada, Oracle (ORCL), and Bell Canada. Its flagship product, a platform called North, lets these clients deploy AI agents inside their own walls. The numbers explain the interest. Annual recurring revenue nearly quadrupled to $240 million in 2025, up from $62 million a year earlier.
'Even Though It's Bad for Berkshire' Billionaire Charlie Munger Said to Skip Insurance Because 'You're Paying for the Other Fellow's Frauds'
MediaTek Is Stepping Up Competition Against Qualcomm With a New 2-Nanometer Chip. What This Means for QCOM Stock.
Dear Tesla Stock Fans, Mark Your Calendars for September 30
Jensen Huang has spent years telling every government not to outsource their artificial intelligence and to build their own instead. Cohere is that idea turned into a product. Its models are built to run on Nvidia's stack, and one runs on a single Nvidia H100 chip. So every bank or agency that adopts Cohere could also create demand for Nvidia hardware. The more sovereign AI spreads, the more chips Nvidia sells. By backing Cohere, Nvidia is funding its own demand rather than just liking what the business has to offer. This is a similar move to what Jensen has already done with Nebius (NBIS) and CoreWeave (CRWV). As of last month, the company's equity portfolio was worth over $63 billion.
Nvidia operates as a leading AI infrastructure company. It designs GPUs, networking solutions, and software used in data centers, gaming, and automotive applications. It operates through two segments. The Graphics segment includes GeForce GPUs for gaming and PCs, Quadro and Nvidia RTX GPUs for enterprise workstation graphics, and Omniverse Enterprise software for building and operating metaverse and 3D internet applications. The Compute & Networking segment consists of Data Center accelerated computing platforms. Founded in 1993, the company is headquartered in Santa Clara, California.
NVDA stock posted a 29% gain over the past year, but its performance fell short of the broader semiconductor sector. The iShares Semiconductor ETF (SOXX) gained 101% during the same period. A similar pattern has continued this year. Nvidia is up approximately 18% on a year-to-date (YTD) basis, whereas the ETF has surged around 72%.
As of this writing, Nvidia is the most valuable company in the world, worth well over $5 trillion. Yet its valuation looks reasonable to me. The forward GAAP price-to-earnings (P/E) of 21.96x sits nearly 58% below its 5-year average of 52.15x. Similarly, the forward price-to-sales (P/S) ratio of 12.82x is roughly 35% below its 5-year average of 19.79x. So the stock is trading at a steep discount even as growth holds up. The EPS outlook looks strong, especially for a company this size. Analysts expect earnings to grow 95% in 2027, 67% in 2028, 34% in 2029, and 12% in 2030. The pace slows each year, but that is expected from a much larger base, and the trajectory remains positive throughout.
The balance sheet is exceptional, with $62.47 billion in cash against just $38.86 billion in debt. That leaves Nvidia net cash positive by over $23 billion, giving it plenty of room to keep funding companies like Cohere. Each of those bets quietly points more customers toward Nvidia's chips. With the multiples sitting below their historical norms and growth looking strong, I don't see much for investors to worry about here.
Nvidia reported its second-quarter fiscal 2027 earnings on Aug. 27. Revenue for the quarter rose to a record $96.2 billion, more than double year-over-year (YoY). The earnings per share came in at $2.22, comfortably beating the Wall Street consensus of $2.08. CFO Colette Kress reported profitability and margin levels, saying GAAP and non-GAAP gross margins were both 75%, largely unchanged from last quarter due to a similar product mix. The company's operating expenses were up 10% and 11% sequentially, primarily due to high compute infrastructure costs and compensation and benefits costs. Kress added that Hopper H200 shipments to China represented less than 1% of total data center revenue in Q2, reflecting the continued impact of U.S. export restrictions. The firm also registered a $7.8 billion gain on its equity portfolio in the second quarter.
Looking forward, Nvidia expects third-quarter revenue of $108 billion, plus or minus 2%, which implies a range of about $106 billion to $110 billion. The company also guided for gross margins of 74%, plus or minus 50 basis points, and operating expenses of $9.2 billion on a GAAP basis. On a positive front, management said Vera Rubin shipments began in August and that the new platform is already seeing purchase orders from major hyperscalers.
On Sept. 10, Goldman Sachs analyst James Schneider reiterated a "Buy" rating on NVDA stock and assigned a price target of $300. The analyst has given his "Buy" rating due to a combination of factors tied to the company's long-term AI positioning and execution. He believes the company has a major advantage because its AI chips, networking equipment, and software work together as a complete system. As improvements in chip performance become harder to achieve, companies are investigating how to get more computing power and efficiency from their AI spending, which benefits Nvidia. Similarly, Bernstein analyst Stacy Rasgon maintained a "Buy" rating on Nvidia and set a price target of $400.
Based on 50 Wall Street analysts with coverage, NVDA stock holds a consensus "Strong Buy" rating. The mean target price of $326.09 implies an additional 49% upside from current levels. The lowest price target is $180. The high price target of $515 shows investor confidence in the long-term prospects of the company.

### Article 358 · 2026-09-19 · fool.com
Applied Materials vs. Nvidia: Which Tech Stock Is a Better Buy in 2026?

As the digital world expands, investors are looking for the best ways to profit from the chips powering everything from smartphones to artificial intelligence. With that in mind, should you choose Applied Materials ( AMAT +3.90% ) or Nvidia ( NVDA +2.55% ) ?
Applied Materials provides the specialized equipment needed to build modern chips, while Nvidia designs the high-performance hardware that processes AI workloads. Both companies are central to the global tech ecosystem, but they occupy different stages of the production cycle. This comparison looks at their business models and financials to help you decide.
Applied Materials sells materials engineering solutions used to manufacture chips and advanced displays. It serves the global semiconductor industry , focusing on foundry, logic, and memory markets. Two major customers accounted for roughly 19% and 15% of net revenue in its most recent fiscal year.
In the fiscal year ended Oct. 26, 2025, according to its latest annual report, revenue reached nearly $28.4 billion. This was an increase of approximately 4.4% compared with the prior year. The company reported net income of roughly $7 billion, which resulted in a net margin of about 24.7%, representing the portion of revenue remaining after all expenses.
As of Applied Materials' October 2025 balance sheet, the debt-to-equity ratio was approximately 0.3. This ratio measures total debt against shareholder equity to evaluate financial leverage, with lower numbers generally suggesting less risk. The current ratio was nearly 2.6, meaning short-term assets comfortably covered short-term liabilities. Free cash flow, which is cash from operations minus capital expenditures, was close to $5.7 billion in the fiscal year ended Oct. 26, 2025.
Nvidia designs hardware and software for accelerated computing, primarily serving data centers and AI researchers. It relies on third-party foundries for all its manufacturing needs, and two direct customers accounted for nearly 22% and 14% of its total revenue in the latest fiscal year. These partnerships are crucial for its ongoing dominance in the broader technology sector, but customer concentration like this adds a layer of risk to the business.
In the fiscal year ended Jan. 25, 2026, according to its latest annual report, revenue reached approximately $215.9 billion. This was a massive increase of nearly 65.5% compared with the prior year. Net income came in at roughly $120.1 billion, representing a net margin of close to 55.6%, indicating the company kept over half of its revenue as profit during the period.
According to Nvidia's latest annual report, the debt-to-equity ratio was roughly 0.1 as of its January 2026 balance sheet. This suggests very little debt relative to its equity. Its current ratio was approximately 3.9, indicating strong liquidity and the ability to meet upcoming obligations. Free cash flow was nearly $96.7 billion in the fiscal year ended Jan. 25, 2026.
Applied Materials faces significant exposure to shifting U.S. and international export controls, especially regarding China. It recently reached a $252 million settlement in February 2026 related to prior exports to Semiconductor Manufacturing International. The business is also sensitive to the capital investment cycles of its limited customer base, while intellectual property theft and cybersecurity threats remain persistent concerns.
Nvidia relies heavily on a small number of third-party suppliers like Taiwan Semiconductor Manufacturing ( TSM +2.34% ) for its production needs. Any geopolitical conflict in the regions where these suppliers operate could severely disrupt the supply of its advanced chips. Evolving export restrictions have previously caused inventory write-offs, and the company also faces ongoing antitrust inquiries and legal challenges related to its revenue disclosures.
Nvidia appears cheaper based on forward P/E , which uses future earnings estimates, while Applied Materials looks more attractive when measured by its P/S ratio .
While they share an industry, these companies couldn't be more different. Nvidia is the biggest company in the world , and it's been putting up eye-popping growth despite facing extremely tough comparisons.
Applied Materials simply isn't in the same league, and its shares are also more expensive on a forward basis. The chip designer's stock has also vastly outperformed Applied Materials'.
That being said, the artificial intelligence boom is showing potential signs of slowing, and that would have a massive impact on Nvidia's growth. Current and former frontier lab employees have recently spoken out against AI in extremely dire ways (I'm paraphrasing, but basically, "It's going to kill us all if we don't stop it."). Now, that could mean lots of potential things, including we get murdered by robot overlords, at which point Nvidia's earnings will cease to matter. On the other hand, it could actually be masking a different problem: The AI, it turns out, is not very good, and they need a reason to cease developing it because they cannot continue to light money on fire. If AI development slows or stops, that's very bad news for Nvidia.
Furthermore, the potential AI murderbot issue has recently attracted the attention of lawmakers in Congress. Regulation or even the threat of it would likely have a negative impact on Nvidia shares.
I think Nvidia's fortunes are so inextricably linked to the AI boom that if anything disrupts the rosy AI narrative, Nvidia shareholders will be feeling the pain. Applied Materials is boring and safe. Sign me up.
Erin Kennedy has spent over 15 years editing and publishing in the financial media space. Her longtime goal has been to help educate people on topics in finance that can seem uninteresting or too complex, and she embraces a reader-centered mindset. Erin has worked on stock recommendations, newsletters, articles, reports, and commentaries, in addition to managing several sites. She likes investing in relatively boring equities and ETFs, with the occasional spicy stock thrown in for good measure. Erin holds a bachelor’s degree from the University of Michigan and likes to watch old F1 races for fun.
Nvidia's 55.6% net margin dwarfs Applied Materials' 24.7%, but one trades at a steep valuation premium while the other faces customer concentration risk.
By Erin Kennedy – Updated Sep 19, 2026 at 9:15PM EST
Nvidia continues to dominate the artificial intelligence infrastructure market with massive revenue growth and high net margins.

### Article 359 · 2026-09-19 · tomsguide.com
Nvidia says 'local AI is here' — and it could change how you use AI at home

By Type
Nvidia says 'local AI is here' — and it could change how you use AI at home
By Amanda Caswell
Adel El Hallak, senior director of product management for Nvidia AI, shared his thoughts with me about the future of AI
Adel el Hallak has a DGX Spark sitting in his house. It runs AI jobs overnight, and if he forgets to give it something to do before bed, he feels bad about it.
"At home I feel guilty if I don't kick off my job for it to work on all night," el Hallak, Nvidia 's VP of Product, tells Tom's Guide. "It doesn't make noise. And I feel guilty if I don't do that for something on a personal front — because it's plugged in anyway."
It's a small, endearing detail from a wide-ranging interview — but it also points at where AI is headed, particularly local AI. Because when the person in charge of Nvidia's AI product strategy is already living with a personal AI computer in his home, treating it more like an appliance than a server, it could mean a lot of us will be doing the same thing in just a few years.
Right now, most people interact with AI through a browser or app. That means, when you prompt ChatGPT or Perplexity or any other AI assistant, your data travels to a data center, and a response comes back. It works, but there's a cost — both financially and in terms of privacy . Every question you ask, every document you upload and every personal detail you share lives on someone else's infrastructure.
El Hallak thinks local AI changes that equation. "I could run a good enough model on my system at home," he said. Essentially, if the model runs on hardware you own, your data never leaves your house, and there's no monthly subscription.
The math is worth thinking about. Nvidia's DGX Spark currently retails for $4,699 — not cheap by any measure. But a ChatGPT Plus subscription runs $20 per month, or $240 per year. Over five years, that's $1,200 — and you still don't own anything. The Spark, meanwhile, runs unlimited queries with no per-token billing, no usage caps, and no internet required.
That's not an apples-to-apples comparison, of course. GPT-6 and Claude are significantly more capable than the open-source models you'd run locally on a Spark. But for a growing number of tasks — summarizing documents, drafting emails, searching your own files, running a coding assistant — a local model with 128GB of memory and access to Nvidia's full CUDA stack is more than enough.
The DGX Spark launched last October as what Nvidia called "the world's smallest AI supercomputer." At the time, it was squarely aimed at developers, researchers, and data scientists. It runs Linux. It weighs 2.6 pounds. It's the size of a Mac Mini.
But the ecosystem building around it is starting to look more consumer-friendly. As I wrote last month, Perplexity just launched Portable Computer , which packages a local AI model, agent tools, app connectors, and a sandboxed runtime into a single system that runs on DGX Spark hardware. Every task starts on your machine. If the local model hits something it can't handle, it asks your permission before sending that one step to the cloud. Your files stay put.
El Hallak sees this as a trend, not an outlier. He pointed to harness providers — the companies building the software layer between a model and a user — making setup dramatically easier. "You're not doing installs via a command line or a pip install," he said. "They're making it easier — like the old days of using Windows and setting up an application. They're bringing it back to a GUI."
If that sounds familiar, it should. It's the same arc that turned network-attached storage from a hobbyist pursuit into something Synology sells at Best Buy . The hardware existed for years before the software made it approachable.
The RTX Spark laptops change the picture
The DGX Spark desktop is the proof of concept. But the real consumer play may be what's coming next: RTX Spark laptops, which pack the same GB10 silicon into notebook form and are expected to ship this fall from Dell , HP , Lenovo , Asus , MSI, Acer , and others. Microsoft is building a Surface Laptop Ultra around the chip .
These aren't AI-only machines — they run Windows 11 , play games, and handle conventional laptop workloads. But their 128GB of unified memory means they can also run large language models that would choke any current consumer GPU. The laptop version of what el Hallak has sitting on his desk at home, but without the Linux-only limitation.
"The fact that you will have the model running locally with a harness and a runtime that are made easier to install — I think it's going to really usher in local AI," el Hallak said.
The real argument isn't performance — it's ownership
El Hallak told a story from the enterprise world that translates perfectly to consumers: "There was a point where people were proud of the leaderboards and how many tokens they're using. Then somebody in their IT department got their bills, and all of a sudden I became a cost optimizer."
Anyone who's watched their Claude usage creep up — or hit the limits of a free tier — knows the feeling. And as AI agents get more capable and start touching more personal data (your calendar, your email, your finances), the question of where that processing happens isn't theoretical anymore.
"Local AI is just going to bring more tokens, and tokens equate to intelligence," el Hallak said. "When you pair intelligence with a harness, you're able to do things, and then the runtime secures it."
Or, as he put it more casually: "Data centers in the house."
Amanda Caswell is the AI Editor at Tom's Guide and one of today’s leading voices in AI and technology.
A celebrated contributor to various news outlets, her sharp insights and relatable storytelling have earned her a loyal readership. Amanda’s work has been recognized with prestigious honors, including outstanding contribution to media.
Known for her ability to bring clarity to even the most complex topics, Amanda seamlessly blends innovation and creativity, inspiring readers to embrace the power of AI and emerging technologies.
As a certified prompt engineer, she continues to push the boundaries of how humans and AI can work together.
Beyond her journalism career, Amanda is a long-distance runner and mom of three. She lives in New Jersey.

### Article 360 · 2026-09-19 · finance.yahoo.com
Nvidia Stock And 2 US AI Infrastructure Plays Tied To Federal Defense Spending

Washington just put AI and defense infrastructure back under a spotlight, with plans for an "AI Force" and an AI tsar signaling fresh attention on chips, cloud capacity and contractors that can plug into federal demand. That shift could reshape where capital flows next and it creates both openings and risks for investors watching AI-related equities. This article unpacks 3 US-listed large caps exposed to this policy theme and explains how each stock connects to the AI and defense spending story.
The stocks covered below are only a small sample of the opportunities that fit this federal AI and defense infrastructure theme. The broader screen surfaced 37 more US-listed large caps with similarly detailed stories that are not broken out in this article.
If you want to identify which contractors, chip suppliers and cloud players look most compelling on value, quality and future potential, head straight to the US Federal AI & Defense Infrastructure Contractors screener .
NVIDIA is the clearest pure play on the AI Force theme, since its GPUs, networking gear and software already underpin the heavy compute that federal and defense workloads rely on, which makes the business a natural focal point for investors tracking US AI infrastructure spending.
NVIDIA runs a data center scale AI hardware and software platform, with Compute & Networking generating about US$275.4b and Graphics around US$27.6b in revenue, and the stock carries a roughly US$5.36t market value that reflects this central AI infrastructure role.
"Uptake of an open-source/cheaper/better platform than Nvidia's CUDA would heavily undermine Nvidia's moat and enable any sizeable firm to directly engage semiconductor manufacturers, such as TSMC, to produce their own chips, stealing away Nvidia's high margin products."
What happens to NVIDIA's AI infrastructure edge if a single key assumption about developer loyalty quietly shifts over the next few years?
That loyalty question sits at the center of the full narrative for NVIDIA , which maps how CUDA risk, AI Force demand and valuation could be decoupling beneath the surface.
Broadcom (AVGO)
Broadcom is one of the clearest ways to access the US Federal AI and Defense Infrastructure theme, supplying custom chips, networking hardware and private cloud software that power AI data centers, secure communications and mission critical systems for both commercial hyperscalers and public sector buyers.
Broadcom generates about US$59.4b from Semiconductor Solutions and US$29.7b from Infrastructure Software, combining AI focused hardware with VMware powered private cloud tools. The stock carries a market value near US$1.71t.
Broadcom has become a key supplier behind the scenes of large AI and cloud platforms, which makes it highly relevant if federal agencies rely on those providers to build out any formal AI Force capability.
"Broadcom benefits from that outcome regardless of which AI model wins, which cloud provider gains share, or which software platform becomes dominant."
The main question for investors is what happens to that broad advantage if a quiet shift in how customers build and secure AI infrastructure starts to matter more.
That quiet shift is exactly what the full narrative for Broadcom unpacks, showing where Broadcom's AI and defense role could be accelerating or quietly capped.
Cerebras Systems is the pure-play AI hardware story in this screen, with wafer-scale processors built specifically for giant inference and training workloads that look a lot like the centralized government and defense AI projects investors are watching.
Cerebras Systems generates about US$680.7 million from Semiconductors and has a market value near US$47.1b, reflecting its role in dedicated AI compute infrastructure.
"Its Wafer-Scale Engine 3 (WSE-3) is a single, giant, uncut piece of silicon... By keeping the wafer intact, Cerebras keeps 44 gigabytes of lightning-fast SRAM memory mere nanometers away from the compute cores, which eliminates the severe latency penalties that occur when traditional GPUs have to retrieve data from external memory pools."
The key issue for Cerebras Systems is what happens to that AI infrastructure promise if one unseen pressure on its economics suddenly bites.
That pressure is exactly what the full narrative for Cerebras Systems pulls apart so you can see whether Cerebras Systems' wafer scale bet is accelerating or quietly constrained.
Fresh opportunities move first, then the crowd arrives. Spot potential breakouts while they are still under the radar for now and before momentum gets fully caught. Act now.
Spot cash generative under-the-radar leaders early by running the 33 high quality undervalued stocks while pricing still reflects caution, not crowded optimism, and potential mispricing remains in play.
Ride structural demand in electrification and infrastructure by scanning the 17 top copper producer stocks and focus on producers that could benefit if volumes and pricing regain momentum.
Position ahead of possible robotics momentum by using the curated 95 robotics and automation stocks and focus on operators tied to automation, manufacturing upgrades and real productivity gains.

### Article 361 · 2026-09-19 · finance.yahoo.com
Nvidia (NVDA) Forms Alliance To Build A Power Flexible AI Data Center

NVIDIA (NasdaqGS:NVDA), Google, and Emerald AI have created the AI Energy Management Alliance to coordinate electricity use in AI data centers.
The alliance has started building what it calls the first purpose-built power-flexible AI data center, designed to adjust consumption with grid needs.
AEMA plans to publish shared frameworks for grid-responsive data centers with input from utilities, regulators, and large AI infrastructure users.
The formation of AEMA and the power-flexible data center project is worth weighing against the rest of our NVIDIA findings. We have also flagged 2 warning signs (1 major) for NVIDIA.
NVIDIA is far from the only company exposed to this push toward grid-aware AI infrastructure, so it is worth scanning 88 AI infrastructure stocks .
NVIDIA operates as a data center scale AI infrastructure provider across the US, Asia, Europe, and other regions. As a result, any shift toward power-flexible facilities directly affects how its hardware and software fit into future grid-aware computing projects.
Why does a power-flexible data center matter for NVIDIA investors?
Electricity availability has become a practical ceiling for AI data centers, so any credible way to align compute usage with grid conditions directly supports NVIDIA's AI infrastructure ambitions. If AEMA can show that GPU heavy sites can flex demand without hurting performance, it helps keep large AI deployments politically and operationally acceptable.
Does this shift the NVIDIA Narrative or mostly reinforce it?
The existing Narrative highlights "rising data center constraints" and power bottlenecks as risks to long term AI infrastructure spending. AEMA leans into that by treating power flexibility as part of the full stack, alongside GPUs, networking and software. Rather than changing the story, it backs the catalyst that NVIDIA can sell more energy efficient, grid aware architectures into those constraints.
What has to happen next for this alliance to really matter for NVIDIA?
The inflection point is whether the first power-flexible facility in Manassas actually secures faster grid interconnection terms or preferential tariffs by late 2026. Concrete regulatory wins or standardized "grid responsive" design templates would show AEMA is more than marketing and could influence how future DSX style AI factories are specified and approved.
Market coverage focuses on NVIDIA's big quarterly figures, rather than on how solid the underlying earnings engine really is. Internal checks point to something important in the quality of those profits. See what our checks flag about the quality of NVIDIA's earnings .

### Article 362 · 2026-09-19 · korben.info
Huawei moves up its Ascend 960 AI chips to overtake Nvidia in China

Huawei moves up its Ascend 960 AI chips to overtake Nvidia in China
China is in the process of shutting the door on Nvidia, and Huawei fully intends to grab the spot. The Shenzhen-based group announced this Thursday, during its Connect conference in Shanghai, that its next AI chip, the Ascend 960DT, would launch as early as Q1 2027, nine months earlier than planned, with the 960PR variant following in Q3.
For context, these accelerators are the processors that train and run ChatGPT and its peers in data centers. Nvidia reigns over pretty much everywhere else, except precisely in China, where US sanctions block its most powerful models and where Beijing is pushing its tech giants toward local suppliers anyway.
Sure, the spec sheet won't shake up much at Nvidia, whose upcoming Rubin promises around 17 petaflops of compute while the Ascend 960 claims 2 in the same format, with 288GB of memory and 9.6TB/s of bandwidth, roughly double the current generation.
But Huawei doesn't intend to fight chip against chip. Its UnifiedBus technology, presented as the key to its future systems, links processors, memory and networking in a way that lets up to a million chips work together, as if the whole thing formed a single giant computer.
So rather than chasing the perfect chip, Huawei stacks them: its Atlas 960 SuperPoD, a cluster of more than 4,000 accelerators linked together via fiber optics, is meant to compensate through sheer numbers for what each chip concedes to the American company.
One small detail though: this machine is notably more modest than the 15,000-chip monster mentioned last year. The chip is arriving earlier, but the cluster has shrunk.
Except that here's the thing, nobody knows who's fabricating these chips or with what equipment, since sanctions have shut Huawei out of Taiwanese foundry TSMC. Complete mystery. The group even admits it isn't producing enough to meet Chinese demand.
The announcement also comes right before the planned meeting between Donald Trump and Xi Jinping, and Huawei is already promising what's next: an Ascend 970 in 2028, then a 980 in 2029, with a doubling of performance at each generation.
To tackle Nvidia's other fortress, the CUDA software layer that all AI developers are used to, the company is also open-sourcing its in-house equivalent, CANN, already compatible with widely used tools like PyTorch.
In short, the China-US war is as scary as it is fascinating from a technological standpoint.
No paywall or programmatic ads. If the site is useful to you and you want it to remain free and independent, you can support it on Patreon.

### Article 363 · 2026-09-19 · fool.com
Better Artificial Intelligence (AI) Stock Pick for 2027: Nvidia versus Micron

Nvidia ( NVDA +2.55% ) and Micron Technology ( MU +4.20% ) are two of the biggest companies in the world. Nvidia holds the top spot, sitting at a $5.3 trillion valuation. Micron currently sits at 13th place worldwide, with a $1.1 trillion valuation. These companies are also two of the biggest beneficiaries of the artificial intelligence (AI) build-out, and with that expected to ramp up again in 2027, these two are in a prime position to benefit.
But which stock stands to benefit more? Let's take a look at these two and see which stock makes the most sense for your investment dollars.
Nvidia and Micron are partners in the AI arms race. Micron makes memory chips, including DRAM memory that's utilized inside Nvidia GPUs . Micron's DRAM chips are also utilized in several other competitors' products, and demand for these products continues to rise.
Nvidia forecasts that the big five AI hyperscalers will spend nearly $800 billion on data center capital expenditures during 2026. Next year, that figure is projected to rise to $1.3 trillion. That's a lot of GPUs from Nvidia, filled with memory chips from Micron. There is huge demand for each company's product, but there is a stark difference in the long-term demand curve for each.
Part of the reason Micron is among the best-performing stocks in the market this year is the supply state of the memory chip industry. Currently, demand outpaces supply, which is causing a price crunch in the memory chip market. This is causing Micron's downstream clients to pay more for the product, while Micron makes a fortune on higher prices. This effect will last until more supply is available or demand falls. With demand continuing to rise, the only logical path is for supply to increase, and Micron is doing so by building more production facilities, which are likely to come online sometime in mid-2027 and throughout 2028. However, Micron's management team has told investors that they shouldn't expect the tightness in the memory chip market to subside until 2028.
That places Micron in the driver's seat through 2027, giving it the edge over Nvidia.
Nvidia and Micron both expect huge growth next year
During Nvidia's latest conference call, it made the bombshell announcement that it expects 70% revenue growth next year, far exceeding analyst expectations. Micron hasn't given any forward guidance, but with the memory chip market still constrained, it's likely to be another banner year. Wall Street analysts estimate Micron will put up 88% growth, edging out Nvidia.
Both are expected to grow at a strong pace next year, although Micron still has the edge here.
Micron and Nvidia operate on separate fiscal calendars. Micron's fiscal year begins in September, while Nvidia's starts in February. That makes it a bit hard to directly compare valuations, but there's enough information here to give investors a general picture. Micron trades at a dirt cheap 6.25 times fiscal year 2027 earnings.
Nvidia trades at an also-cheap 14 times fiscal 2028 earnings (ending January 2028), giving Micron the edge in this category, too.
So, Micron is cheaper, growing faster, and its industry is expected to boom in 2027 more than Nvidia's. That should make Micron a no-brainer over Nvidia, right?
I think the key here is 2027 versus the next three years. In 2027, I fully expect Micron to be a better stock to own than Nvidia, although they are both fantastic investments. However, once the memory chip supply crunch is sorted out, Nvidia's high demand will remain while Micron's may falter or take a step back.
So, if you're looking for immediate upside, Micron is the best bet . If you're looking for better performance over the next three to five years, then I think Nvidia is the better pick .
By Keithen Drury – Sep 19, 2026 at 11:30AM EST

### Article 364 · 2026-09-19 · korben.info
AI data centers: Google and Nvidia promise to modulate power use to avoid blackouts

AI data centers: Google and Nvidia promise to modulate power use to avoid blackouts
Google, Nvidia and Emerald AI, a young American company specializing in data center energy management, launched the AI Energy Management Alliance this week, a coalition of about twenty players aiming to teach AI data centers to modulate their power consumption based on the state of the grid.
A flexible data center, in their vocabulary, slows down, pauses or shifts its least urgent computations during the few hours when the grid is under strain, typically on a heatwave evening when every air conditioner in the country is running at once, instead of continuously drawing power the way all data centers do today.
In exchange for this goodwill, the companies are demanding faster grid connections. It's worth noting that in the United States, a new data center can wait up to ten years before being connected to the grid, a delay that's become completely absurd at a time when everyone wants to build AI factories.
Emerald AI's boss, Varun Sivaram, puts forward a fairly striking figure: flexible data centers during critical hours could free up around a hundred gigawatts on the existing American grid, roughly the output of a hundred nuclear reactors, without building a single power plant. No small feat.
The logic holds up, since the American electrical grid is on average only used at half its capacity. It was sized to absorb peaks. The rest of the time, it sits idle.
Around the founding trio, there's quite a lineup: Anthropic, OpenAI's rival which develops Claude, but also energy companies like Constellation, National Grid and NRG Energy. The alliance mainly wants to define common standards, so that grid operators know what they can require from a data center before hooking it up.
Except, none of this actually addresses the other complaints leveled at data centers: water consumption for some of the older ones, nuisances for nearby residents, and rising electricity bills. Discontent is growing in the United States, and this alliance still looks a lot like a charm offensive aimed at keeping construction going.
Emerald AI, by the way, isn't a neutral referee in this story: the startup happens to sell the software that orchestrates this flexibility, and it just raised 150 million dollars at a valuation exceeding a billion.
The first full-scale test is set for later this year in Virginia, where Nvidia, Emerald AI and hosting provider Digital Realty will power up a nearly 100-megawatt site capable of scaling back on demand.
No paywall or programmatic ads. If the site is useful to you and you want it to remain free and independent, you can support it on Patreon.

### Article 365 · 2026-09-19 · moomoo.com
NVIDIA Vice President Ian Buck: The Evolution of Computing Power in the Era of Agentic AI from the Perspective of the Vera Rubin Platform

NVIDIA Vice President Ian Buck believes that agents eliminate the human‑interaction bottleneck, pushing computing power into a state of high‑frequency, full‑load operation. Ian Buck pointed out that the key to reducing AI costs does not lie in lowering GPU prices, but in achieving a 10‑ to 30‑fold performance leap with each new generation, thereby directly diluting the per‑token cost. Meanwhile, industry benchmarks have shifted from single‑card computing power to "tokens per megawatt throughput."
Reconstructing the Logic of Hardware Cost Reduction in the AI Era
"The most effective way to reduce per‑token costs is by no means lowering GPU prices or using low‑cost networks; rather, it is to deliver dramatically improved computational performance with each new generation. If the performance of a node or rack is increased by a factor of 10 to 30, this boost directly amplifies the numerator in the cost‑per‑token formula, thereby reducing the overall per‑token cost across the entire data center."
Traditional IT procurement practices seek to control costs by driving down the unit price of hardware. However, in the AI‑powered factory era, computing performance is improving exponentially—by a factor of 10 to 30—exerting a far greater impact on total cost of ownership than minor adjustments to chip prices. Consequently, boosting performance to reduce the per‑unit cost of computing power is far more effective than simply purchasing lower‑priced hardware.
Agentic AI eliminates human intervention, leading to a dramatic surge in computational resource consumption.
"Agents have removed humans from this interaction loop, and the rate at which computational resources are consumed now depends entirely on the speed with which agents self‑reflect and generate new reasoning. Previously, service designers could leverage the latency inherent in human reading and typing to schedule computing power; today, however, agents pose and process questions with extraordinary rapidity. In the AgentX benchmark, computational demand has increased by a factor of 100 on purely numerical tasks."
The shift from chat‑based models to agentic AI has ushered in a paradigm change in computing‑power requirements. Traditionally, cloud‑service scheduling rested on the assumption that human reaction and input speeds are inherently limited; by contrast, agents eliminate the human‑in‑the‑loop buffer, driving compute resources into a seamless, high‑frequency, fully loaded state.
The core metrics for evaluating AI chips have shifted.
"For each generation of compute‑power products, we focus not just on raw token‑level performance; the single most critical metric is total token throughput per megawatt (MW). By improving this metric, we can enhance the AI factory's ability to generate revenue."
The AI hardware evaluation framework is undergoing a major reshaping. Industry benchmarks have shifted from chasing single-chip FLOPs or single-card performance scores to assessing data center energy‑conversion efficiency—measured in tokens per megawatt. The core value of computing power is no longer confined to peak performance; instead, it is increasingly defined by how effectively energy is translated into tangible revenue.
Unlock 40% of hidden capacity in data centers through software.
"By dynamically managing power consumption at both the rack and firmware levels via software, ensuring it never exceeds the threshold, it is possible to deploy up to 40% more racks within the same power‑budget envelope, directly boosting throughput to 1.2 billion tokens per second."
The traditional static deployment model, which reserves power capacity based on the hardware's peak power consumption, has been disrupted. Under conditions of constrained power supply, leveraging software‑defined power technologies such as MaxLPS enables a 40% increase in GPU deployment density within the existing power envelope—without the need to build new data centers or secure additional power allocations.
Ian Buck: Examining the Evolution of Computing Power in the Age of Agentic AI from the Perspective of the Vera Rubin Platform
Paradigm Shift: From 2023 Chat Benchmarks to Agent-Based AI Workloads
Ian Buck: Today, I'll share how we're advancing infrastructure in the era of agent-based AI—an evolution that fundamentally ushers in a new age of reasoning. From my perspective, I'll offer some insights and introduce the innovative technologies we're developing, giving this community a glimpse into the products we're building. At the same time, I'll provide an in-depth overview of Vera Rubin, highlighting the profound transformations that have taken place over the past few years—and even just within the last year—as well as the high-level strategies we've adopted to address them.
I believe the field of computing is extraordinarily broad. Ian and Dr. Patterson have explained how computing has transformed his perspective, tracing its evolution from early magnetic-core memory all the way to today and into the future. This vividly illustrates the critical importance of both computational infrastructure and computational power: transforming data, deriving insights through computation, producing results, and then feeding those results back to further transform the data. This, in essence, is the very nature of value creation. Storing information is important, and transmitting it is equally vital, but value emerges precisely in the act of computation—and in the process of turning raw data into actionable insights.
From our perspective, this platform is truly massive. I've been with NVIDIA for nearly 26 years, and it all began, of course, with the launch of an entirely new computing platform—CUDA. Since then, its scope of applications has expanded dramatically. This chart illustrates the diversity of users leveraging our GPUs, spanning hyperscale cloud providers, AI-native companies, startups, leading AI research labs, enterprise customers, and edge‑based deployments. It also reflects the convergence of AI models and traditional simulation‑based computing—indeed, a synergy between the two, as they now reinforce one another.
Today, Hugging Face hosts over 3 million models, with roughly 3,000 of them accounting for about 90% of all downloads. Model diversity continues to grow, as workloads expand from computer vision to physical sciences, life sciences, speech, natural language processing, and robotics. We offer AI models for quantum computing and simulation, as well as cutting-edge multimodal models that are exploring entirely new architectures. Complementing these are comprehensive libraries and applications for computational modeling, spanning areas such as computational lithography, decision-making, medical imaging, weather analysis, and genomics.
Computing has become an indispensable capability across scientific research, industrial production, consumer interactions, and enterprise computing, spanning both AI and simulation. Today, we host more than 8,000 major CUDA‑enabled applications on these platforms, and we have been building this ecosystem for roughly 25 years.
What is the current situation? This is Vera Rubin. It was designed to be the next-generation reasoning and agent platform. Clearly, we continue to support large-scale training—this is also one of our core capabilities. But what truly brings all this to life is the AI Factory, and Vera Rubin was built specifically for that purpose.
It is built on a robust ecosystem. Globally, we can trace more than 10 million developers who are building on NVIDIA GPUs. This ecosystem spans cloud service providers, network operators, OEMs, and ODMs. Over 300 leading companies have established supply chains to help deliver this platform, and witnessing it all unfold is truly remarkable.
It boasts exceptionally high general-purpose interoperability. I believe this is one of the key reasons it can deliver tremendous value and support worldwide: you provide a computing platform capable of running all workloads and every type of model—whether open-source, proprietary, or state-of-the-art. It supports pre-training, fine-tuning, inference, agent-based AI, and accelerated computing, with all these capabilities invoked concurrently within agent‑centric workloads.
Moreover, it boasts exceptional durability. David noted that the GPUs in GCP are still delivering the original Volta architecture, which dates back nearly a decade. You can still see the value being generated by the GPUs we launched ten years ago. In fact, if you track the hourly instance rental rates for the A100—released at the onset of the COVID‑19 pandemic—you'll find that they have not declined over time but have instead risen, with demand remaining robust.
So what changes have occurred at the software level? The most significant shift has been in the nature of the workloads. Early, extensive benchmarking was conducted using Chat, which in 2023 represented a groundbreaking workload and later became the foundation for benchmarks like MLPerf Inference. At the time, it typically involved around 1,000 input tokens, with KV cache sizes—covering system prompts and other user‑provided data—often hovering around 4,000 tokens. Users interacted with it through multi‑turn dialogues: you'd pose a question, receive a response, then follow up with additional queries, averaging roughly three rounds of conversation. This embodied a human‑in‑the‑loop paradigm; while agents were not yet present, this approach laid the groundwork for benchmarking and for assessing how well such workloads perform—whether on models like DeepSeek or on closed‑source interfaces akin to ChatGPT.
Today, intelligent agents powered by AI are fundamentally different, presenting challenges that far exceed our expectations. Their requirements are extremely demanding, with performance improvements on the numerical level reaching as much as 100-fold. This is based on data from the AgentX benchmark; while it may not be representative of all cases, comparing today's benchmarks to earlier inference tasks reveals that the average input size has grown to 142,000 tokens. Moreover, these inputs are highly dynamic—you must support short sequences ranging from 1K, 10K, and 100K up to 142K, 200K, and even longer. Each input length necessitates an entirely new suite of operator‑kernel optimizations, fine‑tuning, and mathematical‑computational adjustments, significantly escalating the complexity of software optimization.
The size of the KV cache has grown to be exceptionally large. Models now support as many as one million tokens. You may start with a small cache, but as the agent engages in multiple rounds of interaction—no longer involving humans in the loop, but rather the agent continuously posing and answering its own questions—the context keeps accumulating. Today, all these KV caches must be managed across the entire data center.
Finally, the number of interaction rounds has grown explosively. Previously, service designers could rely on the fact that humans needed to take time to read the response before providing the next prompt, which made task scheduling relatively straightforward. Now, however, the agent has removed humans from this loop, and the rate at which computational resources are consumed depends entirely on how quickly the agent can self‑iterate—a pace that is extremely rapid.
In the AgentX benchmark, they configured only about four sub‑agents, whereas in our production services we operate with tens of thousands of agents, all of which require intelligent routing. The model must now make decisions and invoke these diverse sub‑agents across the entire platform, while ensuring that the KV cache is preserved at every stage.
If we examine the structure of the workload, we find it far more complex. In the past, it simply involved token input, model execution, and token output; today, it encompasses scheduling CPUs and managing dynamic Kubernetes containers via Helm charts. We have an LLM tasked with processing context and observational data, another layer dedicated to inference, and yet another layer responsible for determining which sub‑agents or tools to invoke in the next round.
Finally, we must run all these tools: some are CPU‑based, some require GPUs, some perform symbolic computation, and others leverage accelerated computing. On top of this, we have CPU clusters managing and monitoring security and governance. We don't want agents to hallucinate, form incorrect beliefs, or waste time and token‑funding, as that could bring the system down. All of this needs to be managed within memory‑based context windows, which has in turn caused the context window—serving as the model's working knowledge base—to grow explosively.
This was Vera Rubin's original design vision. When we unveiled it, we weren't talking about launching a single chip or reducing the cost of an individual LLM model; rather, our goal was to enable the execution of entire workloads.
On the foundational platform front, Vera Rubin NVL72 builds upon the groundwork we laid for Grace Blackwell and extends its capabilities. To achieve even greater speed from a user‑token perspective, we've also integrated an acceleration package based on Groq LPU technology. For these high‑value workloads, we can further boost platform performance.
On top of this, the agent's CPU is critical. We must be able to execute all tool invocations and computations quickly, efficiently, and at full capacity, ensuring that results are delivered to users without delay. We absolutely do not want the CPU to bottleneck the performance of the entire tech stack.
Finally, all KV caches must be managed within intelligent storage. As diverse contexts flow throughout the system, all data needs to be governed, managed, and integrated into a software-defined network, while also enabling indexing and vector search on the KV cache during backend optimization. That's why we've launched BlueField for storage, collaborating with all storage partners building these systems by providing them with our SmartNICs and computing platforms.
Now let's turn to large-scale networks. These models are so massive that a single GPU simply cannot accommodate them. In fact, decoupled inference has become the norm today. We discussed Dynamo software last year, and it is now widely adopted. Developers are separating the prefill phase from the decode phase and managing all KV caches on top of this architecture, thereby achieving optimal token rates and throughput. Connecting all these components requires robust network infrastructure. Of course, such infrastructure can also be leveraged during reinforcement learning and post-training phases.
These are the results of the newly released SemiAnalysis agent benchmark run on Vera Rubin. Through full‑stack co‑design across the entire ecosystem—spanning both open‑source and proprietary models—it delivers a 30‑fold increase in AI‑factory throughput for agent workloads. In fact, depending on where you fall along the Pareto curve, performance gains in certain scenarios can soar as high as 60‑fold.
On the left is the total token throughput per megawatt (MW). All of these data centers are constrained by their power consumption limits, measured in megawatts. For each generation of our products, we focus not only on absolute token performance; the key metric is total token throughput per megawatt. Improving this metric enhances the AI factory's ability to generate revenue.
If you're running a model like DeepSeek v4, you'll want to aim for a throughput of over 100 tokens per second to compute the answer and return it quickly. In fact, you might even push this further to 200–250 tokens per second, allowing the agent to engage in deeper reasoning and deliver results more swiftly within 65 rounds of interaction—without keeping users waiting too long.
In addition, we must reduce the cost per million tokens. This chart compares the token-generation costs of Grace Blackwell and Vera Rubin. As you can see, thanks to performance gains, costs have dropped significantly. The most effective way to cut costs is to deliver stronger performance with each new generation. If I simply lower the price of GPU chips or adopt lower‑cost networks, I'm only improving a small part of this massive data center. But if I boost the performance of that node or rack by a factor of 10 or 30, that improvement directly feeds into the numerator of the cost equation, thereby reducing the per‑token cost across the entire data center.
Ultimate Latency and Throughput: Groq LPU Integration with the Olympus Core
What can we do if we want to think faster and more proactively, while also enabling rapid interaction? In many application scenarios, intelligent agents play a pivotal role, and we aim to place them on the critical path—for real-time business analytics or cutting-edge computing. We can further enhance Vera Rubin's performance. From Blackwell to Vera Rubin, we've improved the overall user‑interaction experience. But if we seek the ultimate leap—scaling from hundreds of tokens per second to thousands of tokens per second per user—we can leverage Groq technology to unlock even greater performance.
These are the latest test results. For models with 100K‑token long contexts, such as Gemma 4 or Qwen 3.8, we achieve 3,400 tokens per user per second on Gemma 4 and 2,529 tokens per user per second on Qwen 3.8. In long‑context scenarios, these throughput rates are truly remarkable. The longer the context, the more the model must retrieve the entire conversation history to generate each new token, which increases computational overhead—but this is also essential for agent‑based applications.
Tool invocation is critically important. Globally, there is not only a shortage of data centers and GPUs, but also a shortage of CPUs. Although previously users relied on Grace CPUs connected to Blackwell for tool execution, we are now seeing growing demand for efficient, high‑performance, purpose‑built CPUs tailored for agent‑based computing. We have repurposed the CPUs originally attached to Rubin GPUs and built dedicated Vera CPU racks.
What is Vera? It features NVIDIA's custom-designed Olympus core. Its design goal is to deliver high performance, providing answers at the fastest possible speed while each core operates at full capacity. We achieved this through our custom-built Olympus core.
To ensure all cores operate at full speed without creating bottlenecks, the inter‑core bandwidth is exceptionally high. This is a large, monolithic compute die in which each core can access memory without traversing multiple hops across chiplets, resulting in extremely low memory access latency. Paired with an LPDDR memory subsystem, it not only delivers low power consumption but also achieves latency that is 40% lower than other solutions on the market. In CPU‑centric workloads, memory latency often dominates performance.
This differs from the CPU performance landscape prior to the cloud era. In the past, CPUs boasted high single-threaded performance but had relatively few cores, resulting in lower overall throughput. By contrast, in the pre‑AI cloud computing era, the key metric shifted to the cost per core, driving up core counts while relegating single-threaded performance to a secondary concern. This explains the explosive growth in core numbers: at the time, cloud service customers were primarily focused on the price per core for workloads such as web hosting and database operations.
Vera is designed to keep its 188 cores (176 cores when SMT is enabled) operating at high throughput while maintaining strong single-threaded performance, ensuring that token latency remains unaffected.
These results were validated by Signal65 using Stanford University's Terminal Bench benchmark. In over 80 test cases, we ran the CPU‑bound tasks of Terminal Bench, and Vera demonstrated a 1.6‑fold performance improvement. The agent's speed in executing tool calls increased by 60%, while its throughput for core agent tasks such as compiling code, running Git, and performing code verification improved by up to 2×.
Customers have already begun seeking to deploy this product. Perplexity Space found that task execution is often constrained by the speed of sandbox creation. By introducing Vera, they observed a 1.5-fold increase in the overall speed of sandbox initialization, rapid computation, and shutdown.
ClickHouse is a real-time analytical database widely adopted by leading research labs for security and governance; they ran its public benchmark suite on Vera and achieved top rankings.
Vera has now been officially released, with early adopters including Oracle Cloud Infrastructure (OCI) and several system vendors.
NVLink is a key enabler for high‑speed AI and inference workloads. From the absence of NVLink to 8‑way interconnects and now to the full NVLink 72, it has dramatically improved the Pareto performance curve. NVIDIA is a networking‑technology company, and through the NVLink Fusion program, we are making NVLink accessible to all. Chip designers simply need to develop their own XPU accelerator chips; by partnering with NVIDIA, they can integrate our NVLink Chiplet IP and NVHBM technology, seamlessly connecting to the complete NVLink ecosystem.
Early partners include the startup The Matrix, which is adopting NVLink Fusion for its next-generation Raptor XPU to connect Vera and NVLink Switch racks, building a complete NVLink 72 architecture that incorporates The Matrix chip. Amazon AWS and Annapurna Labs are also collaborating with us to integrate custom IP into the base die of NVHBM, unlocking 30% to 40% of computing resources on their custom chips while leveraging NVIDIA SerDes to achieve higher bandwidth and lower latency.
At the data center level, as we focus on improving inference efficiency per megawatt (MW) or per gigawatt (GW), a key challenge is determining how many GPUs can be accommodated within a given data center. Workload power consumption profiles are dynamic; even for DeepSeek‑R1, GPU power draw fluctuates between 600 W and 1,900 W across different stages, resulting in underutilization of allocated power resources.
To address this issue, we have collaborated with the ecosystem to develop software called MaxLPS (Max Land Power Shell). MaxLPS can dynamically manage and cap power consumption at both the rack and firmware levels, spanning Vera, Rubin, and NVSwitch tiers. By integrating with data center management software, operators can deploy up to 40% more racks within the same power envelope—for example, expanding from 4,000 to 5,600 racks in a gigawatt‑scale data center—while boosting token throughput to 1.2 billion tokens per second.
Lambda has validated this software stack, and Dave Ward notes that, for the same megawatt (MW) capacity, deployable GPU density has improved significantly—by approximately 25% on the B200 and by as much as 40% on the Vera Rubin.
Looking Ahead: Delivering the AI Infrastructure Roadmap on an Annual Cadence
NVIDIA remains committed to advancing its roadmap on a strict one-year cycle. Following Vera Rubin, our next presentation will introduce Vera Rubin Ultra, followed by the Feynman architecture and Feynman Ultra. You can rest assured that NVIDIA will maintain its annual release cadence, steadily driving forward the development of AI token factories, inference capabilities, and data-center‑scale intelligent‑agent infrastructure.
Thank you very much for your time.
Source of this article: Andy730

### Article 366 · 2026-09-19 · fool.com
Semiconductor Stocks to Buy and Hold Through 2030

The artificial intelligence (AI) build-out has made chip companies some of the fastest-growing large businesses in the world. Nvidia ( NVDA +2.55% ) grew revenue 106% year over year in its most recent quarter. Broadcom ( AVGO +2.83% ) grew 86%.
Micron Technology ( MU +4.20% ) more than quadrupled its sales. Even Marvell Technology ( MRVL +3.85% ) , the group's smallest, grew 37%.
But holding a stock through 2030 is a different bet than chasing last quarter's growth. AI spending will likely cool at some point over the next four years. What matters then is where in the chip supply chain the profits hold up.
Here's what each one has to keep doing for a four-year hold to work.
Nvidia's revenue in the fiscal second quarter of 2027 (ended July 26) rose 106% year over year to $96.2 billion, with $89 billion of that coming from data centers. In late August, management told analysts it expects revenue to grow approximately 70% in fiscal 2028 -- an outlook it called limited by supply, not demand.
At about $212 as of this writing, shares trade at about 14 times fiscal 2028's estimated earnings. That price, I'd argue, stops giving Nvidia credit after next year.
The job through 2030 is to stay the platform AI computing runs on (the chips, the networking, and the software) even as its biggest customers fund custom alternatives.
Broadcom is the company building many of those alternatives. Its AI semiconductor revenue reached $16.7 billion in the fiscal third quarter of 2026 (ended Aug. 2), 221% higher than a year earlier -- and still accelerating, with growth of 54% from the prior quarter alone. Custom accelerators (chips designed with a single customer) made up 73% of it.
CEO Hock Tan told analysts earlier this month that Broadcom has secured the supply to double AI revenue to about $115 billion in fiscal 2027 -- and to $230 billion the year after.
The stock trades at about 18 times fiscal 2027's expected earnings. The four-year job here is delivery: a short list of AI labs and cloud giants taking billions of dollars of chips on schedule, year after year.
Marvell runs the same strategy at a fraction of Broadcom's scale. Revenue reached $2.7 billion in its fiscal second quarter of 2027 (ended Aug. 1), and data center revenue grew 46%.
And CEO Matt Murphy now expects about $18 billion of revenue in fiscal 2028, up from around $12 billion this fiscal year, with the custom business more than doubling along the way.
Marvell is also the most expensive of the four, at about 33 times its expected fiscal 2028 earnings. That price-to-earnings multiple only works if the design wins behind those forecasts keep ramping on time.
Micron: the cheapest, and the most cyclical
Micron sells the memory all of that AI hardware depends on, and right now that is arguably the supply chain's most profitable place. Revenue in its fiscal third quarter of 2026 (ended May 28) came to $41.5 billion, over four times the year-earlier total. Its non-GAAP (adjusted) gross margin reached 84.9%, up from 39% a year earlier. And guidance for the fiscal fourth quarter, which ended in early September, calls for about $50 billion of revenue.
Yet at about $928 as of this writing, shares cost only about 6 times analysts' fiscal 2027 earnings estimates, the group's lowest price-to-earnings multiple by far. In other words, investors are already betting these margins shrink. After all, memory prices have cycled for decades, and I think some of that doubt is fair.
Selling a business earning at this level seems premature. But this deep into memory's profitable stretch, I wouldn't put new money in at today's price, either.
Which of these, then, would I buy and hold through 2030?
Nvidia and Broadcom are my anchors. Both sit where the supply chain's most durable profits appear to be. And both can grow into their prices if most of the demand they have guided for shows up.
Marvell is a buy as well, though I'd keep it the smallest of the three, because more of its growth still has to convert from bookings into revenue.
Of course, if AI spending turns down hard before 2030, all four stocks could fall together, whatever their valuation multiples. All four fell between 5% and 10% in a single week this month, so a four-year holder should expect stretches far worse than that. I'd buy Nvidia, Broadcom, and Marvell today. Micron, I view as a hold.
These chipmakers trade anywhere from 6 to 33 times their expected earnings for this fiscal year or next -- and the cheapest one is the one I'd be most careful buying.
By Daniel Sparks – Sep 19, 2026 at 5:17AM EST
Nvidia grew revenue 106% year over year to $96.2 billion in its latest quarter, and management is forecasting about 70% revenue growth in fiscal 2028.
Broadcom says it has already secured the manufacturing supply to double its AI chip revenue to about $115 billion next fiscal year.
Micron trades at about 6 times analysts' fiscal 2027 earnings estimates, a price that assumes today's record memory profits fade.

### Article 367 · 2026-09-19 · bgr.com
This Nvidia GPU Costs 10x More Than A PlayStation 5 Pro

This Nvidia GPU Costs 10x More Than A PlayStation 5 Pro
By Aaron Greenbaum
If you've been wanting to upgrade your computer, you've probably been holding off on buying a graphics card because component prices are currently insane. It's no secret that the more powerful a graphics card is, the higher its monetary cost , but prices have been increasing exponentially as of late and show no sign of stopping, especially for the most sought-after GPUs.
Last year, Nvidia's current flagship graphics card, the RTX 5090 , launched at a semi-respectable price of $1,999. Fast forward to the beginning of this month, and the cost of a 5090 had climbed to at least $5,000. As of the week of September 13, 2026, stores such as Newegg are selling RTX 5090s for around $9,000. Some even now have price tags bordering on $14,000 (I think they were updated while I wrote this article). For comparison, a PlayStation 5 Pro costs $899 through the PlayStation Store .
You might be thinking that since the RTX 5090 is more powerful than the PS5 Pro, it should cost significantly more. True, but the Nvidia RTX 5060 Ti and 5070 are also more powerful than that console , and Newegg sells most of these graphics cards for anywhere between $500 and $900. You can upgrade your gaming computer to surpass a PlayStation 5 Pro for less than the price of a PS5 Digital Edition.
Not everything is as it seems.
Your first instinct is probably to point an accusatory finger at Newegg. However, if you look closely, you might notice that very few of the exorbitantly priced RTX 5090 GPUs on Newegg's storefront originate from the retailer. Instead, most of these cards are sold through third-party stores that simply use Newegg as a middleman. Some of these sellers are based in Canada, others in the U.S., but most seem to hail from Hong Kong. On the bright side, all these purchases offer free shipping, but that's a cold comfort given their asking prices.
All of these facts leave us with one nagging question: Why are RTX 5090 prices increasing to the point where you need a mortgage? TechRadar theorizes this could be the result of engineered FOMO. Rumors have been swirling about AI server manufacturers buying GPUs by the pallet, complete with images, which is justification enough to buy an RTX 5090 at whatever price sellers set. However, as the outlet points out, many of these pictures seem AI-generated, which could mean the people selling 5090s through Newegg (and other sites) are trying to create the illusion of scarcity to drive up prices. Or maybe someone made the pictures as a joke, and the sellers latched on because they thought they could profit off it. Either way, we do not recommend buying RTX 5090s for $9,000 or more. Use your money wisely and buy a cheaper alternative .

### Article 368 · 2026-09-19 · gurufocus.com
NVIDIA Executives Sell Shares for Tax Obligations Amid AI Discus

On September 19, 2026, NVIDIA Corp NVDA made headlines as several executives, including CEO Jensen Huang, sold a total of 160,000 shares to cover tax liabilities related to restricted stock units (RSUs). This sale was disclosed in a Form 4 filed with the SEC, where Huang had 45,728 shares withheld at a price of $212.17 each, totaling approximately $9.7 million. Additionally, CFO Colette Kress sold 34,918 shares on the open market, generating around $7.65 million as part of a pre-established trading plan. Following these transactions, NVIDIA’s stock price rose by 1.34%, closing at $222.27 with a market cap of $5.36 trillion.
GF Value™ verdict: NVIDIA is currently 43.2% undervalued, with a GF Value™ of $391.63 compared to its current price of $222.27.
Insider activity: Over the past three months, insiders have sold shares worth approximately $660.67 million.
The recent share sales by NVIDIA executives were primarily to cover tax obligations related to RSUs, a common practice among corporate leaders. These transactions are significant as they reflect the executives' financial management strategies and their commitment to fulfilling tax responsibilities. Notably, the sales were not indicative of a lack of confidence in the company's future, as evidenced by the subsequent rise in NVIDIA's stock price.
NVIDIA is a leading supplier of accelerated computing and AI infrastructure, specializing in graphics processing units (GPUs) and data-center-scale systems. The company has a market cap of $5.36 trillion and operates within the technology sector, specifically in the semiconductors industry. NVIDIA's innovative products, including its GeForce GPUs for gaming and AI applications, position it as a key player in the rapidly evolving tech landscape.
According to GuruFocus, NVIDIA's GF Value™ is calculated at $391.63, suggesting that the stock is currently undervalued by approximately 43.2% compared to its market price of $222.27. This substantial margin of safety indicates that investors may find a favorable entry point at the current price level. The company's P/E ratio (TTM) stands at 28.1x, significantly lower than its 5-year median P/E of 56.08x, further supporting the notion of undervaluation. For more details, visit the GF Value™ page .
The GF Score™ is a comprehensive measure that evaluates a company's financial strength, profitability, growth potential, valuation, and momentum. NVIDIA's GF Score™ of 95/100 reflects its robust performance across various metrics, particularly in profitability and growth, where it ranks 10/10. However, its valuation rank is lower at 4/10, indicating potential concerns about its current market valuation despite its strong fundamentals.
NVIDIA's strengths lie in its exceptional profitability and growth rankings, showcasing its ability to generate strong earnings and expand its market presence. However, the lower valuation rank suggests that investors should exercise caution regarding its current price relative to intrinsic value. For further insights, check out the NVDA stock page .
NVIDIA is held by 33 gurus, with 12 adding to their positions and 20 trimming their stakes in recent quarters. This mixed activity indicates a cautious sentiment among institutional investors. Additionally, insider selling has amounted to approximately $660.67 million over the past three months, which, while substantial, is primarily related to tax obligations rather than a lack of confidence in the company's future prospects.
The current undervaluation of NVIDIA, as indicated by its GF Value™ and strong GF Score™, presents a compelling case for investors to consider the stock. However, the mixed signals from insider activity and the potential for valuation concerns suggest that investors should conduct thorough due diligence before making any decisions. For more information, visit the NVDA stock page .
NVIDIA's GF Score™ is 95/100, indicating a strong overall performance across various financial metrics.
NVIDIA is currently 43.2% undervalued, with a GF Value™ of $391.63 compared to its current price of $222.27.
NVIDIA's P/E ratio (TTM) is 28.1x, significantly lower than its 5-year median P/E of 56.08x, suggesting it may be undervalued relative to its historical performance.

### Article 369 · 2026-09-19 · wccftech.com
AMD Targets NVIDIA Vera In Latest EPYC Venice “Agentic AI” Benchmarks, Zen 6 Leads With 20% Higher Per-Core & Over 2x Gains In Platform-Level Performance

AMD has shared new benchmarks of its 6th Gen EPYC Venice CPUs in Agentic AI workloads against the competition from Intel & NVIDIA.
AMD Leads The Agentic AI CPU Race With Strong 6th Gen EPYC Venice Numbers, NVIDIA Vera Targeted
In its latest blog post , AMD has published a new whitepaper in which it provides a performance overview of its server EPYC CPUs. Launched during the Advancing AI 2026 event, AMD's 6th Gen EPYC Venice CPUs feature disruptive performance with their new Zen 6 cores, which deliver faster performance per core, faster overall performance throughput, and leading efficiency.
As the chips roll out to data centers across the globe, AMD is providing a look at the performance capabilities across various benchmarks, mainly focusing on Agentic AI workflows.
The first benchmark that we will be taking a look at is the Per-Core Performance measured within SPEC 2026. Here, the AMD 6th Gen EPYC Venice CPUs provide a 20% uplift over NVIDIA's 88-Core Vera CPU. Per-Core performance is a metric that is essential for AI inferencing tasks and latency-sensitive workloads such as databases, user-interactive services, live translations, and specific phases of Agentic AI.
In SPECrate 2026 Integer testing, the AMD EPYC 9996 server CPU delivers 1.2 times the per-core performance of an Nvidia Vera-based platform and 2.24 times its platform-level performance. Across enterprise and cloud-native testing – including server-side Java, OpenSSL, MongoDB, Redis, NGINX and transaction processing – AMD testing reports gains of 2.4x to 3.7x.
Against the Intel® Xeon 6980P processor, the AMD EPYC 9996 server CPU delivers 1.8x to 3.13x performance advantages across molecular dynamics, materials modeling and weather forecasting. In a modeled 100-kilowatt rack, it delivers an estimated 3.4 times the throughput of a Vera-based platform.
In the overall SPEC 2026 suite, AMD compares the performance of its 6th and 5th Gen EPYC CPUs against other leading data center chips such as NVIDIA's Vera, Amazon's AWS Graviton5, & Intel's Xeon 6980P . Here, the 5th Gen EPYC CPUs with 192 cores provide a 37% gain over NVIDIA Vera & the 6th Gen EPYC Venice CPU with 256 cores provides a 2.37x gain.
Moving over to Agentic AI-specific benchmark tests, AMD's EPYC 9006 Server CPUs drive a 12% gain in per-core performance benchmarks, with the a4 subtests' performance averaging at 20%. AMD used a 96-core EPYC Venice chip against the 88-core NVIDIA Vera chip .
The lead is shown as high as 2.01x in per-core performance tests such as stockfish_r, while many tests show a lead over 30%.
Another aspect in which the AMD 6th Gen EPYC CPUs lead is memory bandwidth. The higher the memory bandwidth, the faster the generative AI and model inference performance would be. It also means faster simulation, graph analytics, and enterprise database systems. The sustained memory bandwidth was measured using the STREAM Triad benchmark.
AMD's EPYC Venice delivered 18% faster memory bandwidth versus NVIDIA's Vera thanks to its 16-channel memory design, which supports up to 12,800 MT/s RDIMM modules. This provides the platform with 1.6 TB/s of memory bandwidth versus 1.2 TB/s bandwidth on the NVIDIA Vera CPUs (using LPDDR5x).
Despite the higher core count (96 vs 88), the AMD EPYC Venice cores get access to 8% higher bandwidth than NVIDIA Vera's 88 cores.
AMD also highlights the Enterprise/Cloud-Native workload performance where not only the 6th Gen, but also the 5th Gen EPYC CPUs provide competitive performance against Intel & Amazon offerings. The AMD EPYC 9996 Server CPU delivers platform-level performance increases of 2.4x for server-side Java, 2.5x for OpenSSL, 3.5x for MongoDB with YCSB, 2.9x for Redis Benchmark, 3.7x for NGINX with WRK, and 2.6x for transaction processing systems based on TPC-C kit when normalized to an Intel Xeon 6980P (128C)-powered system.
Same goes for HPC workloads where AMD is the leading x86 CPU provider, driving up to a 2x gain with its 5th Gen EPYC and over 3x gains with its 6th Gen EPYC CPUs versus Intel's latest Xeon 6 family.
Lastly, AMD is showcasing the rack-level system performance measured within a 100kW power budget. The EPYC 6th and 5th Gen CPUs are pitted against Intel Xeon and NVIDIA Vera, with the former providing a 2.3x uplift and the latter providing a 3.4x uplift versus NVIDIA Vera.
The launch of AMD's EPYC Venice has been a critical milestone for the company. The chip paves the way for its leadership within the Agentic AI space while boosting traditional Enterprise, Cloud, and HPC workloads. And it doesn't stop there; the 6th Gen EPYC family is going to feature a very broad spectrum of chips, each designed to perfectly fit today's most demanding workloads.

### Article 370 · 2026-09-19 · fool.com
Sam Altman Admits the AI Industry Has Done "a Terrible Job" Explaining Its Benefits Amid Growing Backlash. Should That Worry Nvidia and Microsoft Investors?

Its enormous need for electricity, its massive physical footprint, and, most recently, concerns that it could inadvertently cause catastrophic problems have pushed the artificial intelligence (AI) business out of favor, along with leading AI stocks like Nvidia ( NVDA +2.55% ) , Microsoft ( MSFT +1.22% ) , and Alphabet ( GOOG -0.77% ) ( GOOGL -0.61% ) .
OpenAI CEO and co-founder Sam Altman thinks he knows why, too. In a recent interview with Bloomberg, Altman suggested the industry itself has done "a terrible job" of explaining AI's benefits to ordinary Americans. And perhaps he's right.
The question is: What does this mean for shareholders of the companies at the heart of the AI revolution? It certainly seems like a problem.
But it isn't.
Users always eventually find the best tool for the job
Don't misunderstand. The artificial intelligence business has much to figure out about connecting with customers. In that regard, Altman is right -- the industry has done a terrible job of selling itself to the public. Blame the ambiguity of ChatGPT's and Gemini's interfaces, mostly. It seems too good to be true that these platforms can simply do whatever you ask them to do; a simple "getting started" guidebook would certainly help.
Trust the marketplace of ideas, though. The good ones always rise to the top, and the best ones displace the merely good ones. Consumers and corporations will eventually vote with their dollars for the best ones, but only after they organically see real value.
Think about Apple 's ( AAPL -1.29% ) iPhone, first introduced back in 2007. It was far from the first smartphone, which was introduced back in the mid-1990s. It was the first smartphone to truly click with consumers for its ease of use, sparking a flurry of follow-ons that would eventually become an unexpected centerpiece of people's lives. Today, Pew Research reports more than 90% of U.S. adults own a smartphone.
The advent of Meta Platforms ' ( META -0.83% ) Facebook is another example of a consumer-driven, organic mainstreaming. It wasn't the first social networking platform. That honor largely belongs to MySpace, which launched in 2003 with respectable early growth. Facebook simply surpassed MySpace's user headcount in 2008, despite only becoming available to users outside of universities and colleges in 2006. Users just liked it better.
The point is, people eventually embrace any and all useful technologies, even if they're poorly explained. Artificial intelligence is unlikely to be any different. It's just going to take some time, largely because most AI users will insist on learning to use the tech themselves at their own pace, as they did with the internet and computers. To this end, Precedence Research still predicts the global AI market is set to grow at an average annualized pace of 18.7% through 2035.
This still doesn't answer another (perhaps more important) question. That is, which AI platform will most of the crowd end up falling in love with? That's also the norm for consumer-facing technologies . Again, think of Apple's iPhone, or Alphabet's dominant search engine, Google.
From this perspective, while the artificial intelligence industry as a whole will eventually draw a large crowd of regular users, one of these platforms will become the favorite. The others will end up like MySpace, Yahoo, or early smartphone pioneer BlackBerry ( BB +3.70% ) .
Sam Altman Admits the AI Industry Has Done "a Terrible Job" Explaining Its Benefits Amid Growing Backlash. Should That Worry Nvidia and Microsoft Investors?
By James Brumley – Sep 19, 2026 at 4:30AM EST
The battle for AI supremacy shouldn't crimp the industry's demand for the appropriately capable underlying hardware and infrastructure.

### Article 371 · 2026-09-19 · investorplace.com
Slower AI Models Could Mean Faster Growth Somewhere Else

Slower AI Models Could Mean Faster Growth Somewhere Else
By Luke Lango , InvestorPlace Senior Investment Analyst
Editor’s note: “Slower AI Models Could Mean Faster Growth Somewhere Else” was previously published in August 2026 with the title, “Nvidia Took Claude From 30% to 100% – Without Building a Better Model.” It has since been updated to include the most relevant information available.
On one of AI’s toughest interactive tests, Claude solved fewer than one in three challenges.
Then Nvidia ( NVDA ) surrounded the same model family with better memory, outside tools, a structured work loop, and a supervisor that stepped in whenever Claude got stuck.
The system solved every challenge – and its score jumped from 30.2% to 100% .
Nvidia changed other parts of the test setup, too, so this was not a perfect apples-to-apples comparison. Still, the result points toward a major shift in the AI market.
We first covered this result last month. It matters even more now .
With the industry’s safety push dominating headlines – and some labs signaling a more deliberate pace on their most capable releases – the central question in AI has changed: how much value can be unlocked around the models that already exist?
According to Nvidia, a lot.
Today’s best models may already contain more useful intelligence than their surrounding systems allow them to express. And the companies that turn that capability into dependable, cost-effective – and now, provably safe – workflows could become some of the next major AI winners.
Powerful AI Agents Still Need Guardrails
Today’s AI agents are pretty good at sprints. Marathons are where they lose the plot.
Give Claude or GPT a short assignment. It can browse the web, write some code, pull information from another app, and come back with an answer.
But long projects are a different story. Imagine asking an agent to migrate a company’s financial software, redesign a supply chain, or optimize thousands of lines of GPU code. The work may require hundreds of decisions made over hours or days.
Frontier models still struggle with that kind of sustained work. They lose context. Repeat old mistakes. Chase dead ends. Occasionally become so confused that they damage the project they were supposed to complete – and we’re left to try to clean up the mess.
Nvidia’s Agentic Variation Operators system, or AVO, was designed to keep that from happening.
AVO gives the model persistent memory and its own repeated cycle of planning, acting, testing, and revising. Nvidia also added a supervising agent that watches the work and nudges the main agent when it gets stuck or starts exploring an unproductive path.
Think of it as a talented employee with a good project-management system and an experienced boss nearby.
The intelligence was already there.
Nvidia helped it stay organized long enough to finish the job.
AI Safety Is Becoming Its Own Infrastructure Layer
For the first few years of this boom, the model leaderboard commanded almost all the attention.
Which lab had the best reasoning score? Which model had the largest context window or wrote the cleanest code?
Those are still important questions; better models still retain a huge competitive advantage.
But the new safety push is expanding the market around the model.
Independent evaluators can’t do their jobs from the outside. They need access – model checkpoints to probe, environments to test in, and the logs that show how a system actually behaved. Companies deploying agents need something different: control. An audit trail behind every action, a clear point where a human takes over, and software that can stop or redirect an AI the moment something goes wrong.
Those safeguards have to remain active after the model launches, too.
A company will want to know:
If the system can recover safely after a mistake
That requires real infrastructure: software that watches the agent, systems that secure it, memory that records what it did – plus simulation platforms and an enormous amount of testing.
It also requires more compute.
Each independent evaluation runs the model again. Each monitor adds another layer of processing. Simulations, safety checks, recovery loops… all of it consumes more infrastructure.
The labs may take more time before releasing their most capable systems.
But the work surrounding those systems – proving them safe before launch, watching them after – keeps expanding.
AI Safety Gets More Serious When Machines Start Moving
AI safety becomes a much bigger issue when intelligence leaves the screen.
A coding assistant can generate a bad line of software. A human can review it, reject it, and run the task again.
A robot operating on a factory floor deals with physical consequences.
It may be carrying a heavy part through a crowded warehouse, inches from expensive equipment – and people. A bad decision can cause serious damage.
That raises the bar dramatically.
A useful robot needs far more than a capable model.
It needs cameras and sensors to understand its surroundings. Control software has to translate a decision into precise movement. Simulation tools must expose the system to unusual situations before it encounters them in the real world.
The robot also needs a plan for the moments when things go sideways. If it loses track of an object, it has to know how to reacquire it. If a person steps into its path, it has to stop or reroute instantly. It has to recognize when it’s out of its depth and call for help. And afterward, it has to be able to prove it acted safely at every step.
Those requirements are becoming central to commercial robotics.
Factories and warehouses are not waiting for a robot that can do everything a person can do. They need machines that can perform a handful of useful tasks reliably, repeatedly, and safely.
Stronger AI guardrails can help unlock those deployments. That makes safety more than a regulatory cost.
Better AI Infrastructure Changes Both Safety and Economics
Performance is only half the equation, though. Companies also care what it costs to finish the job.
As Databricks CEO Ali Ghodsi explained to TechCrunch , two agent systems built around the same model can produce dramatically different bills. Choose the wrong setup, and the same task may cost roughly twice as much to complete.
A clumsy workflow sends a routine job to an expensive frontier model when a smaller one would do. Poor memory leads the system to reread huge amounts of old information again and again.
A better setup preserves what matters, sends each task to the right model, and eliminates unnecessary loops.
Safety systems add work of their own. But they can also unlock far more valuable tasks.
A company may happily accept a little more processing overhead if the result is an agent – or robot – it can trust with meaningful work.
Better systems can lower the cost of each completed task and reduce expensive failures, making more jobs worth automating.
In another Nvidia experiment, AVO tested more than 500 approaches to improving a piece of GPU software and saved 40 separate versions before beating a leading implementation by as much as 10.5%.
The agent kept experimenting, checking, and revising until it found a better answer.
Every loop consumed compute. Every successful result made that compute more valuable.
Frontier releases may slow at the margin. The market around them won’t.
Physical AI Startups Are Building the Layer Between Models and Machines
The public market remains focused on the largest model labs and the companies supplying their chips.
But much of the work required to bring AI safely into the physical world is happening inside smaller, private companies.
They are collecting robot-training data.
Building simulation software.
Developing machine vision, control systems, and safety layers.
Creating the tools that let robots learn new tasks and operate around people.
This is the “second layer” of the AI boom: companies taking raw intelligence and applying it to specific industries, factory floors, warehouses, and machines.
The safety turn could make that layer even more valuable.
A more deliberate frontier race gives robotics companies time to improve reliability, integrate monitoring, and turn today’s models into systems that businesses can actually deploy.
That brings me to one private company I have called the “ Nvidia of Robotics .”
For a limited time, everyday investors can claim a stake with as little as $500 . But the opportunity is set to close to new investors on Monday, Sept. 21 .
Get the name, the full investment details, and everything you need to claim your stake before the window closes on Monday .
No paywall . No credit card required .
Article printed from InvestorPlace Media, https://investorplace.com/hypergrowthinvesting/2026/09/nvidia-took-claude-from-30-to-100-without-building-a-better-model/.
By Luke Lango and the InvestorPlace Research Staff

### Article 372 · 2026-09-19 · fool.com
If You'd Invested $1,000 in Nvidia's 1999 IPO, Here's How Much You'd Have Today

Nvidia ( NVDA +2.55% ) is one of the most successful stocks in history. Since launching its IPO in 1999, the stock has earned unprecedented returns, especially considering the 27-year time frame. So high are the gains that an investment of $1,000 at that time would deliver millions.
The semiconductor stock launched its IPO on Jan. 22, 1999, at a split-adjusted price of $0.025 per share. At the time, that would have bought 40,000 split-adjusted shares worth $5.32 million. Add in the dividend income over that time, and the overall total grows to $5.70 million.
Nvidia made its initial fortune as a leader in graphics cards. It later moved on to GPUs and, later, AI accelerators, which have made it an industry-leading chip stock. With that, it won the AI training race , or at least the first phase of it.
Earning returns from the investor perspective was much simpler, as investing in Jensen Huang's vision early on involved both foresight and luck. However, the hardest part was probably holding the stock, even during Nvidia's downturns.
Nvidia stock lost more than 50% of its value five times in its history. During the dotcom bust and the 2008 financial crisis, that decline exceeded 85%. Keeping the faith during such times can be tough, but if a company offers a vision that can succeed over time, one may find the discipline to hold.
Admittedly, investors are unlikely to earn comparable returns by buying Nvidia today. Still, this stock's history is important to investors hoping to find the next Nvidia.
Comparable returns to Nvidia's are not guaranteed. Nonetheless, if one finds a high-quality company and invests early, holding for years and riding out downturns could yield massive returns over the long term.
By Will Healy – Updated Sep 19, 2026 at 6:45AM EST
