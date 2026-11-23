# Blind reader, matter census batch 6 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 40 articles (numbers 173 to 212,
2026-09-14 to 2026-09-15, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 173 · 2026-09-14 · NVIDIA Corporation
Perplexity Portable Computer Is Now Available on Windows, Powered by NVIDIA RTX | NVIDIA Blog

Perplexity’s local agent platform now supports Windows RTX PCs, giving more users a way to run private AI workflows without cloud credits.
As local models become more capable, AI agents can handle more work directly on a PC while keeping sensitive information on the device.
Portable Computer is a local version of the agent Perplexity Computer that plans and carries out multistep tasks. Accelerated by NVIDIA GPUs, it uses local models to analyze data, bring together information across files and handle recurring work. Sensitive information stays on device, and locally completed work doesn’t consume Perplexity Computer credits. Users can also orchestrate work up to cloud models for more advanced research and reasoning.
Today, Perplexity is adding Portable Computer in the Perplexity app for Windows on compatible NVIDIA GeForce RTX PCs and NVIDIA RTX PRO Workstations , bringing powerful agentic AI to more Windows PC users. The release builds on existing support for NVIDIA DGX Spark systems and RTX PCs running Linux .
Perplexity brings local and cloud AI together in one app, letting users work with sensitive files on their PCs and take advantage of Computer’s built-in tools such as the built-in browser and proprietary SPACE sandbox.
For tasks that call for more advanced reasoning, Portable Computer can also identify when a task needs cloud support, asking the user for permission before sending information off-device.
The app simplifies setup with a local model, such as Qwen 3.8 27B, that is post-trained to work with Perplexity Computer and optimized for NVIDIA RTX GPUs. Users can put the agent to work without having to research models or configure the complex software stack typically required to run local AI.
Connectors for Microsoft Outlook, OneDrive, Word, Google Drive, Gmail, Slack and GitHub extend that experience across the files and apps already part of users’ daily workflows.
Engineering: Review open pull requests in a connected GitHub project, organize them by status and identify next steps. Computer can also flag outdated documentation and submit proposed updates for review.
Finance: Point Computer at two years of brokerage summaries, consolidated 1099s and tax returns, and have it trace the recurring holdings creating the most avoidable fees and tax drag, with every figure cited to the exact file and page — all without a document ever reaching a chatbot.
Startups: Ask Computer why activation went flat, and the agent analyzes the funnel export locally to find where new signups drop off between install and first completed task, then posts the top insights straight to the team’s Slack channel.
Portable Computer is available for NVIDIA GeForce RTX and RTX PRO GPUs with 24GB or more of VRAM. NVIDIA DGX Station support is expected to come soon.
🧠Z.ai’s GLM 5.3 Flash provides impressive performance and visual intelligence at low cost, optimized for DGX Station and dual DGX Spark systems.
🐋DeepSeek-v4.1 Flash significantly reduces key-value cache memory demands and operating costs for complex AI agent workloads, delivering remarkable intelligence per dollar.
⚡Qwen has released Qwen3.8-Flash-Next , an open-weight multimodal mixture-of-experts model, and an early preview of Qwen4, which can run locally on a single DGX Spark with NVFP4 and punches well above its weight.
👾GLM 5.3 is Z.ai’s 744-billion-parameter flagship model, tuned for agent sessions that run for hours on DGX Station and a cluster of four DGX Spark systems.

### Article 174 · 2026-09-14 · NVIDIA Corporation
NVIDIA Expands Open Source CUDA-Q Platform for Fault-Tolerant Quantum Computing | NVIDIA Newsroom

NVIDIA Expands Open Source CUDA-Q Platform for Fault-Tolerant Quantum Computing | NVIDIA Newsroom
NVIDIA Expands Open Source CUDA-Q Platform for Fault-Tolerant Quantum Computing
September 14, 2026
The NVIDIA CUDA-Q platform now includes the CUDA-Q Logical orchestration layer, giving the quantum industry an open, programmable way to design and test fault-tolerant quantum computing applications in areas such as drug discovery, financial modeling and materials development.
Fermilab used CUDA-Q Logical to accelerate fault-tolerant architecture development from five months to three weeks — a 7x speedup.
QUOPS is a benchmark for the future of quantum computing, measuring the readiness of fault-tolerant quantum hardware for practical applications. Developed by Sandia National Laboratories, QUOPS is now available in NVIDIA CUDA-Q.
NVIDIA today announced an expansion of the NVIDIA CUDA-Q ™ open source platform with CUDA-Q Logical, an orchestration layer that provides a programmable, verifiable approach to developing useful applications for fault-tolerant quantum computers.
Fault-tolerant quantum processors with logical qubits are essential for useful quantum computing, allowing systems to overcome the errors inherent in physical qubits so they can execute the larger computations needed for practical applications such as drug discovery, financial modeling and materials development.
However, developing applications for such systems is a tedious, time-consuming codesign challenge: A change to an algorithm, error-correction code, hardware architecture or other QPU component can significantly change the resources needed to run any given application.
With CUDA-Q Logical, researchers can now design and orchestrate the many components required for fault-tolerant quantum computing applications, easily switching between options to identify optimal system configurations for performance with logical qubits.
“Quantum computing is maturing into an era of logical qubits, and researchers need an open, customizable platform capable of representing all aspects of a fault-tolerant system,” said Timothy Costa, vice president and general manager of quantum at NVIDIA. “The addition of CUDA-Q Logical provides power and flexibility to explore fully integrated, co-optimized systems regardless of qubit type and architecture — drastically shortening the timeline to useful quantum-GPU supercomputing.”
CUDA-Q Logical is already being used by QPU makers and labs including Fermi National Accelerator Laboratory, Infleqtion , IQM Quantum Computers, QCDesign Quantum Motion and Sandia National Laboratories.
Using CUDA-Q Logical, Iceberg Quantum modeled its fault-tolerant architecture for Diraq’s qubits, showing how 1,000 logical qubits can be created with just 150,000 physical qubits, roughly 10x fewer than Diraq’s previous estimates. CUDA-Q Logical gave an unprecedented way to rapidly assess potential implementations of Iceberg’s architecture, helping dramatically reduce the hardware needed for useful, fault-tolerant quantum computing.
Fermilab Uses CUDA-Q Logical to Explore Fault-Tolerant Applications
In early work, Fermilab researchers used CUDA-Q Logical to validate prior results and evaluate physical qubits, runtimes and other resource requirements across different error-correction approaches and quantum hardware.
Fermilab transformed complicated fault-tolerant system designs into a repeatable and verifiable computational workflow, accelerating fault-tolerant algorithm development from five months to three weeks, a 7x speedup.
“Fault-tolerant quantum computing is the path to unlocking new scientific discovery, but getting there will require researchers to codesign algorithm, error correction, architectures and hardware together,” said Anna Grassellino, chief technology officer at Fermilab and director of the Superconducting Quantum Materials and Systems Center. “Using CUDA-Q Logical, our team explored combinations of these resources in just three weeks, compared with what would have typically taken about five months of building specialized infrastructure.”
Sandia Creates Benchmark for Future of Quantum Computing
QUOPS is a new, independent cross-platform benchmark developed by Sandia National Laboratories that measures the progress quantum computing systems are making toward utility-scale applications.
With Sandia’s QUOPS, the industry now has access to a hardware-agnostic, open method to benchmark progress toward shared goals for fault-tolerant quantum computers. Historically, progress in quantum computing has been measured primarily through advances in physical qubits — increasing qubit counts, improving fidelity and extending coherence.
“At Sandia, we can’t wait to see fault-tolerant quantum computers helping to solve problems of national importance for the Department of Energy and the United States,” said Timothy Proctor, co-director of Sandia National Laboratories’ Quantum Performance Laboratory. “Our mission right now is to bring that about sooner, by accelerating our industry partners’ progress. To do that, we, and other quantum computing stakeholders, have to be able to track and forecast the growth of quantum computer abilities. We created QUOPS to do exactly that, and we’re excited to see it used by quantum computing vendors and customers.”
Sandia shared early results in a preprint posted ahead of IEEE Quantum Week, reporting initial QUOPS benchmarks for QPUs from Google, IBM and Quantinuum . A QUOPS reference implementation is available in NVIDIA CUDA-Q.
Expanding the Quantum-GPU Supercomputing Platform
The ecosystem is also adopting NVIDIA’s larger lineup of quantum computing technologies for turning qubits into useful quantum-GPU supercomputers.
Diraq used NVIDIA Ising, the world’s first family of open models for building and deploying AI for useful quantum computing, to calibrate its silicon-based qubit processor.
Companies are integrating their quantum processors with GPU supercomputing using NVIDIA NVQLink ™, the open system architecture for tightly coupling quantum processors with GPU supercomputers. With NVQLink:
Anyon Computing developed a new quantum control system.
Quandela developed a QPU-GPU architecture.
Quantum Machines ran a demo of integrating state-of-the-art supercomputing resources with qubits at the Israeli Quantum Computing Center.
The NVIDIA CUDA-Q open development platform continues to be adopted across the quantum computing ecosystem:
BlueQubit launched the Quantum Flywheel grant program for researchers, to give them access to NVIDIA accelerated computing through CUDA-Q.
Qedma Quantum Computing and QCentroid each integrated their technology with CUDA-Q to support quantum error correction and mitigation, as well as the deployment of quantum applications.
The quantum ecosystem is also working with NVIDIA to develop new and improved quantum applications:
IonQ announced progress on DQAOA-GPT, a quantum generative AI framework, using NVIDIA accelerated computing.
MITRE published work on building GPU-accelerated digital twins of quantum sensors.
Phasecraft is using NVIDIA cuQuantum to generate the largest-known variational quantum eigensolver emulated molecular database.
UCLA and Caltech are advancing the design of control sequences needed to run quantum applications.
CUDA-Q Logical is now available through GitHub . Explore the QUOPS repository .
Learn more by reading these papers on CUDA-Q Logical and QUOPS .
Certain statements in this press release including, but not limited to, statements as to: expectations with respect to quantum computing; expectations with respect to growth, performance, availability, and benefits of NVIDIA’s products, services and technologies, and related trends and drivers; expectations with respect to NVIDIA’s third party arrangements, including with its collaborators and partners; expectations with respect to technology developments, and related trends and drivers; projected market growth and trends; expectations with respect to AI and related industries; and other statements that are not historical facts are forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended, which are subject to the “safe harbor” created by those sections based on management’s beliefs and assumptions and on information currently available to management and are subject to risks and uncertainties that could cause results to be materially different than expectations. Important factors that could cause actual results to differ materially include: global economic and political conditions; NVIDIA’s reliance on third parties to manufacture, assemble, package and test NVIDIA’s products; the impact of technological development and competition; development of new products and technologies or enhancements to NVIDIA’s existing products and technologies; market acceptance of NVIDIA’s products or NVIDIA’s partners’ products; design, manufacturing or software defects; changes in consumer preferences or demands; changes in industry standards and interfaces; unexpected loss of performance of NVIDIA’s products or technologies when integrated into systems; NVIDIA’s ability to realize the potential benefits of business investments or acquisitions; and changes in applicable laws and regulations, as well as other factors detailed from time to time in the most recent reports NVIDIA files with the Securities and Exchange Commission, or SEC, including, but not limited to, its Annual Report on Form 10-K and Quarterly Reports on Form 10-Q. Copies of reports filed with the SEC are posted on NVIDIA’s website and are available from NVIDIA without charge. These forward-looking statements are not guarantees of future performance and speak only as of the date hereof, and, except as required by law, NVIDIA disclaims any obligation to update these forward-looking statements to reflect future events or circumstances.
Aaron Groff
NVIDIA CUDA-Q
Certain statements in this press release including, but not limited to, statements as to: expectations with respect to quantum computing; expectations with respect to growth, performance, availability, and benefits of NVIDIA’s products, services and technologies, and related trends and drivers; expectations with respect to NVIDIA’s third party arrangements, including with its collaborators and partners; expectations with respect to technology developments, and related trends and drivers; projected market growth and trends; expectations with respect to AI and related industries; and other statements that are not historical facts are forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended, which are subject to the “safe harbor” created by those sections based on management’s beliefs and assumptions and on information currently available to management and are subject to risks and uncertainties that could cause results to be materially different than expectations. Important factors that could cause actual results to differ materially include: global economic and political conditions; NVIDIA’s reliance on third parties to manufacture, assemble, package and test NVIDIA’s products; the impact of technological development and competition; development of new products and technologies or enhancements to NVIDIA’s existing products and technologies; market acceptance of NVIDIA’s products or NVIDIA’s partners’ products; design, manufacturing or software defects; changes in consumer preferences or demands; changes in industry standards and interfaces; unexpected loss of performance of NVIDIA’s products or technologies when integrated into systems; NVIDIA’s ability to realize the potential benefits of business investments or acquisitions; and changes in applicable laws and regulations, as well as other factors detailed from time to time in the most recent reports NVIDIA files with the Securities and Exchange Commission, or SEC, including, but not limited to, its Annual Report on Form 10-K and Quarterly Reports on Form 10-Q. Copies of reports filed with the SEC are posted on NVIDIA’s website and are available from NVIDIA without charge. These forward-looking statements are not guarantees of future performance and speak only as of the date hereof, and, except as required by law, NVIDIA disclaims any obligation to update these forward-looking statements to reflect future events or circumstances.

### Article 175 · 2026-09-14 · news.crunchbase.com
Y Combinator Still Busiest Startup Investor In August As Nvidia Ramps Up Its Dealmaking Pace

August was another big month for startup funding, and the most active investor rankings were once again dominated by familiar names.
Always-busy Y Combinator was the most active backer of U.S.-based startups by deal count, while General Catalyst led or co-led the most rounds of $5 million or more, Crunchbase data shows.
Chip giant Nvidia , meanwhile, sharply accelerated its dealmaking, ranking among the most active and highest-spending investors for the month. The chip giant participated in nine disclosed rounds of at least $5 million — marking its busiest month for investing since at least the beginning of 2025 — and led or co-led financings collectively valued at $1.3 billion.
The flurry of activity came as global venture funding reached $42 billion in August , up 122% year over year, with seven companies raising billion-dollar-plus rounds last month.
Below, we rank August’s most active startup investors across several categories, including lead backers, prolific venture dealmakers, highest spenders and seed investors.
San Francisco-based General Catalyst ranked as the most active lead investor in rounds of $5 million or more, leading or co-leading five such deals. Its largest was the $1.1 billion Series A for River AI , which provides custom AI fine-tuning for businesses. General Catalyst also led or co-led a $116 million Series E for Cityblock Health , along with three seed rounds ranging from $10 million to $25 million, Crunchbase data shows.
Andreessen Horowitz , Sequoia Capital and S3 Ventures tied for second, with four lead or co-lead deals each.
The scale of those rounds varied considerably. The four deals that Andreessen led or co-led totaled more than $1.15 billion, driven by an $800 million Series C for defense tech company Castelion and a $300 million Series A for AI infrastructure startup Volta .
Sequoia’s four led or co-led deals totaled $1.3 billion, including a $1 billion Series B for nuclear energy startup Valar Atomics .
When we widen the ranking to include both lead and non-lead participation in rounds of $5 million or more, Y Combinator once again takes the top spot.
The accelerator participated in at least 18 such deals in August, per Crunchbase data. As we’ve noted in previous rankings, Y Combinator commonly invests as a non-lead backer in follow-on rounds for companies that previously went through its program.
Andreessen Horowitz ranked second with 13 deals, followed by General Catalyst with 10. Alumni Ventures and Nvidia tied for fourth with nine each.
Nvidia’s rise in the investor rankings is particularly notable. The Santa Clara, California-based chip giant participated in only four U.S. rounds of $5 million or more in July and one in August 2025. Seven of its nine qualifying investments last month went to companies categorized as AI-focused in Crunchbase, including River AI, Poolside , Groq , Starcloud and Generalist AI .
The August burst extends a notable increase in Nvidia’s venture dealmaking pace this year. Crunchbase data shows that by mid-August, it had participated in a record 59 known startup funding rounds in 2026 , already surpassing its 53 investments in all of 2025. It had also led or co-led at least 11 private-company financings this year, underscoring its growing role as both a technology supplier to and financial backer of the AI startup ecosystem.
RA Capital Management and Sequoia were next in our August rankings, each with seven U.S. startup investments of $5 million or more. RA Capital’s portfolio reflected its life sciences focus, with August deals including LifeMine Therapeutics , AusperBio , Expedition Therapeutics , Infinimmune and Abcuro .
The rankings change again when we look at lead investors associated with the highest aggregate deal values.
For August, Coatue was the apparent spendiest lead investor, thanks to its role leading Databricks ’ $5 billion deal. The round, the month’s largest, valued the data and AI company at $190 billion.
JPMorganChase and Valor Equity Partners followed, each leading or co-leading rounds with an aggregate value of $2.37 billion, as both were listed as lead investors in defense manufacturing startup Hadrian ’s $1.37 billion Series D and home battery provider Base Power ’s $1 billion Series D.
Nvidia and Sequoia came next, each with $1.3 billion in led or co-led rounds. Nvidia’s total came from Poolside’s $1 billion financing and Volta’s $300 million Series A, while Sequoia led or co-led four rounds, topped by the Valar Atomics financing.
General Catalyst and Andreessen also crossed the $1 billion mark, with approximately $1.26 billion and $1.15 billion, respectively, in aggregate led round value.
As always, this is an approximation of spending rather than a tally of capital actually contributed. Investors rarely disclose how much each participant put into a round, although lead investors generally contribute a substantial share.
At seed, Y Combinator was again the most prolific investor, backing at least 12 U.S.-headquartered companies in August.
Orbital Edge Accelerator ranked second with eight seed investments, all announced as part of the same August cohort. NMotion and Techstars followed with six seed deals each, while SV Angel 1 recorded five. (It’s important to note that seed rankings are especially subject to change, since smaller financings often take longer to be reported and added to the Crunchbase dataset.)
August’s rankings tell a now-familiar story: A relatively small group of large venture firms continues to dominate by deal count, while a handful of megadeals determines who tops the spending ranks. But Nvidia’s acceleration this year also illustrates how corporate investors — particularly those with a direct stake in the AI ecosystem — are becoming increasingly prominent alongside traditional venture firms.
Global Venture Funding Jumps 122% In August As Streak Of Billion-Dollar Deals Continues
No Summer Doldrums For Active Startup Investors In July
This analysis covers reported investments in U.S.-headquartered companies and is based on Crunchbase data pulled Sept. 10, 2026. Rankings for active venture and lead investors include rounds of $5 million or more. Seed rankings include angel, pre-seed, seed and equity crowdfunding rounds.
Funding data is subject to reporting lags, which are typically most pronounced at the seed stage.
Stay up to date with recent funding rounds, acquisitions, and more with the
False claims about customers, revenue and AI capabilities can expose founders to personal securities-fraud liability, with D&O insurance offering...
California companies have scooped up more than three-fourths of all U.S. startup funding this year. That, per Crunchbase data, is an apparent record...

### Article 176 · 2026-09-14 · crn.com
Cornelis Mounts Scale-Up Challenge To Nvidia, Teases Potential Qualcomm Tie-Up

Cornelis Mounts Scale-Up Challenge To Nvidia, Teases Potential Qualcomm Tie-Up
The Intel spin-off opens a new front in its challenge to Nvidia with its entry into scale-up networking, which is meant to give companies building rack-scale AI computing platforms an open alternative to the latter company’s proprietary NVLink interconnect.
Intel spin-off Cornelis Networks is expanding beyond its scale-out networking business to challenge Nvidia in an area that is critical to rack-scale AI computing and is helping the larger vendor gain support from AI chip rivals: scale-up networking.
The Wayne, Pa.-based startup announced on Monday that its scale-up move has the potential backing of Qualcomm and that it has also raised $205 million in new funding from investors. The fresh capital will support the development of future scale-up and scale-out products as well as manufacturing and customer deployments for its new CN6000 family of scale-out products.
[Related: Exclusive: Nvidia Networking Rival Cornelis Gives Channel Supply Reprieve For AI Buildout ]
While Cornelis didn’t share any details about what it called a “collaboration” with Qualcomm, leaders from both companies signaled the potential to integrate their technologies together. Qualcomm plans to debut its first rack-scale platform this year with its AI200 accelerator chip, with successor products to come out in the following years.
“[Cornelis’ networking strategy] plays into a lot with what the Qualcomm team is doing on the accelerator and CPU compute side,” Cornelis CEO Lisa Spelman (pictured) told CRN in an interview. “We see a lot of shared vision on the challenges in AI infrastructure, challenges customers are facing, and a lot of opportunity and potential for our technologies to knit together and address those challenges for customers.”
Tony Pialis, general manager of Qualcomm’s data center business, said Cornelis’ “vision for an open, programmable fabric aligns” with the need to improve utilization and AI economics with a “more integrated approach across compute, memory and networking.”
“Giving customers more choice and flexibility across the infrastructure stack will be critical as AI moves toward rack-scale architecture,” he said in a statement.
Pialis is expected to join Spelman for her keynote at the AI Infra Summit this week.
Cornelis Scale-Up Products Could Give Channel More Options
Unlike Cornelis’ traditional scale-out networking business , which is focused on high-speed interconnects for servers across large clusters, the company’s foray into scale-up networking, which enables high-speed connections between processors inside rack-scale systems, may not result in channel-ready products directly from the startup.
Instead, Cornelis will use its newly revealed Active Compute Fabric architecture to give firms building rack-scale computing platforms like Qualcomm an alternative to Nvidia’s proprietary NVLink interconnect technology. This could over time give solution providers more choices in the kinds of rack-scale platforms and configurations they can offer to customers.
“I think there’s a world in which some of these channel players become mechanisms for rack delivery and servicing of that enterprise,” Spelman said.
Qualcomm has not yet announced a partner program for its data center business, though a tech analyst recently told CRN this could eventually happen as enterprise AI needs grow.
An executive at a large U.S. systems integrator told CRN that many of his enterprise customers would welcome new data center suppliers who embrace open standards because it could potentially help them with product choice, supply and pricing.
“Open architecture is something which many customers would like to get their hands on just because it allows them to work agnostically across the different vendors,” said the executive, who asked to not be identified because he was not authorized to speak on behalf of his company without prior approval.
“If you’re not married to one architecture, there are cost implications as well. There are availability implications as well, and the dependencies implication as well. So from a purely business point of view, this is great,” he added.
Cornelis Stands Up To Nvidia With Open Alternative
The challenge for Cornelis is that Nvidia has spent more than a year promoting its proprietary NVLink interconnect technology as the de facto method for scale-up networking to competitors building rack-scale solutions with their own accelerator chips. Such chips are posing a growing threat to Nvidia’s traditional GPU business.
Several companies have signed up so far to support NVlink, including Amazon Web Services, Arm and even Qualcomm, giving Nvidia a way to remain a crucial supplier for the AI infrastructure market and opening another revenue stream.
But even before Cornelis announced its plan to make scale-up products, there has been a growing movement by major tech companies to support an NVlink alternative. This has mainly been through the UALink Consortium, a group that is developing specifications for its open, namesake Ultra Accelerator Link standard.
“We think this is the perfect time to jump into this market. There is still much to be settled,” Spelman said, adding that the company also plans to use the Active Compute Fabric for future scale-out networking products, which will support the Ultra Ethernet standard.
Members of the UALink Consortium include major tech companies such as Amazon Web Services, AMD, Apple, Google, HPE, Intel and Microsoft as well as smaller players like Cornelis, which plans to support UAL as well as another open standard called ESUN for scale-up products.
“There are so many other compute solutions, accelerators, GPUs, XPUs that need scale-up capabilities as they build out their rack-level technology and need partners that are really focused on delivering to open standards,” Spelman said.
Cornelis Says New Architecture Will Improve Utilization
Another way Cornelis hopes to stand apart from Nvidia is how its Active Compute Fabric has been designed to improve compute utilization within rack-scale platforms.
The startup said this is accomplished by integrating programmable compute into the architecture, which allows the network to “operate on data as it moves through the system, adapt to changing workloads, offload collective operations and take on new functions as AI algorithms and software evolve.”
“We’re driving AI-capable compute into your [network interface card] and into your switch, and so you can think of this as not just compute in your network, but it is a whole other pool of compute that is meant to deliver the AI workload,” Spelman said.

### Article 177 · 2026-09-14 · zacks.com
NVIDIA vs. Oracle: Which AI Stock Is the Better Buy After Earnings?

Both NVIDIA Corporation NVDA and Oracle Corporation ORCL have benefited from the artificial intelligence (AI) boom, with strong demand for AI infrastructure and cloud driving their latest earnings results. But which AI stock looks like a better buy now? Let's explore –
NVIDIA's Strong Earnings Cement Its AI Leadership
NVIDIA's revenues reached $96.2 billion in the fiscal second quarter of 2027, representing a 106% year-over-year increase and an 18% rise sequentially, according to the company's Aug. 26 press release. The Data Center segment remained NVIDIA's primary growth driver. Data Center revenues came in at $89 billion, up 117% year over year and 18% from the previous quarter.
NVIDIA also maintained strong profitability alongside rapid revenue growth. During the quarter, the company's GAAP and non-GAAP gross margins both stood at 75%, up from 72.5% a year ago. The company continues to convert strong revenue growth into even stronger earnings growth, helped by ongoing gains in operating income.
Looking ahead, NVIDIA expects revenues to reach approximately $108 billion, plus or minus 2%, in the fiscal third quarter of 2027, representing 12% sequential growth from the midpoint. With NVIDIA's growth momentum remaining strong, and the advanced Vera Rubin platform already in full production, the company is well-positioned to capitalize on the next wave of AI infrastructure spending.
Oracle Delivers Exceptional Growth on Cloud and AI Demand
Given its size, Oracle's revenue growth has been impressive, reaching $19.3 billion in the fiscal first quarter of 2027, up 30% year over year, driven by ongoing customer migration to cloud-based solutions, according to the company's Sept. 10 press release.
Oracle's Cloud Infrastructure (IaaS) revenues reached $7.4 billion, up 121% year over year, while Cloud Applications revenues rose 10% to $4.2 billion. The expanding IaaS business positions Oracle to benefit from the increasing demand for AI infrastructure, while the company gets a stable recurring-revenue base through SaaS.
Oracle further expects revenues to grow 30-34% in the fiscal second quarter of 2027 and reach at least $90 billion for the full year. Additionally, the company's $664 billion in remaining performance obligations, up $209 billion from the previous year, provides strong visibility into future growth. At the same time, Oracle's rapid growth is accompanied by an increase in profitability. The company's non-GAAP operating income rose 31% to $8.2 billion in the fiscal first quarter.
Explosive Data Center growth, strong margins, and a robust outlook reinforce NVIDIA's position as a top beneficiary of the continuing AI infrastructure boom. Similarly, strong cloud and AI demand is driving Oracle's growth, while its growing backlog and improving profitability support a positive outlook.
However, Oracle's heavy capital spending to expand its Cloud Infrastructure business led to negative free cash flow of $5 billion in the first fiscal quarter and increased financial pressure on the company. Anyhow, Oracle's debt-to-equity ratio of 175.2% is significantly higher than NVIDIA's 14.1%, suggesting greater financial leverage and possibly greater downside risk during economic downturns.
Moreover, NVIDIA appears more efficient at generating profits from shareholders' equity than Oracle. This is because NVIDIA's return on equity (ROE) of 97.5% exceeds Oracle's ROE of 70.2%.
Therefore, NVIDIA appears to be the better buy following earnings than Oracle, with lower financial leverage and higher profitability supporting a more favorable outlook. NVIDIA currently has a Zacks Rank #1 (Strong Buy), while Oracle has a Zacks Rank #3 (Hold). You can see the complete list of today's Zacks Rank #1 stocks here.

### Article 178 · 2026-09-14 · tomshardware.com
Nvidia's RTX 5090 vanishes from online retail in the US — third-party sellers now demand as much as $9,500 for Nvidia's fastest GPU

Nvidia's RTX 5090 vanishes from online retail in the US — third-party sellers now demand as much as $9,500 for Nvidia's fastest GPU
By Jake Roach
In less than a week, first-party inventory of the RTX 5090 has almost completely evaporated.
Nvidia's fastest gaming graphics card, the RTX 5090, has been on a tear of price increases over the past several weeks. However, over the past week, the available inventory has dwindled. Now, you can only find the RTX 5090 from third-party sellers at online retailers like Newegg and Amazon , commanding anywhere from $6,500 to $9,500 (or even higher) for Team Green's best GPU .
At Newegg, the cheapest RTX 5090 is the MSI Ventus 3X that's available from Slava Computers (a relatively new seller with 239 ratings and a 2.8 out of 5 rating at the time of writing) for $6,449. On Amazon, you can get the Asus TUF Gaming OC for $6,395 from Joes Tech Shop, a seller with an 81% positive rating. However, among the most recent reviews are a string of one-star reviews about orders never being fulfilled. The cost goes much higher, as well. The first result for "RTX 5090" on Newegg , for example, surfaces the MSI Ventus 3X OC for $8,699.
In June, the median price for an RTX 5090 was $4,299. At the beginning of September, we logged the lowest online price at $5,199 in our GPU price tracker . Now, in less than two weeks, the available stock has completely disappeared online, and the options available from third-party sellers have ballooned in price once again.
Naturally, we don't recommend buying from one of these third-party sellers. The RTX 5090 is selling at a vastly inflated price, but more importantly, we've seen no shortage of scams around high-ticket items like the RTX 5090. In January, 42 Amazon customers were duped into a scam involving a $999 RTX 5090 , instead receiving a fanny pack in place of the GPU. Earlier this month, an online seller scammed two buyers with the RTX 5090, selling phantom graphics cards with the core and memory removed on the secondhand market for prices near MSRP.
The one exception to RTX 5090 inventory is Micro Center, which still has cards available around the average selling price. At a local Micro Center we checked, the cheapest in-stock option was $4,299. Micro Center has exclusively sold graphics cards in-person for several years, insulating it from online buyouts like what appears to be going on right now.
As usual, the reason why there's so much demand for the RTX 5090 is fairly obvious: AI. The RTX 5090 holds the GB202 GPU and 32GB of GDDR7 memory. For context, Nvidia's RTX Pro 5000 48GB comes with the same GPU with a third fewer shader units enabled, and lower memory bandwidth compared to the RTX 5090, and sells for between $7,000 and $9,000. In that context, the RTX 5090 starts to look attractive for building an AI server, even at $5,000 (or more) apiece.
At the same time, the RTX 5090 remains the fastest gaming graphics card on the market according to the testing in our GPU benchmark hierarchy . That's even more true now with Nvidia's launch of DLSS 5 Neural Rendering, which the RTX 5090 can fully capitalize on (though, thankfully, we've found playable performance on lower-end cards in our extensive DLSS 5 testing ).
We've reached out to Nvidia for comment on whether it has any plans to stabilize inventory. We'll update this story when we hear back.
Once again reality shows you can't circumvent the laws of economics. If a manufacturer doesn't raise prices to equalize demand with supply, the shelves will run bare, and black-market / grey-market scalpers will do it for them.
I have a 4080S. You can probably get one for $800. Why is the 5090 50% better performance than the 4080S, yet 700% higher price? The logic ain't logicing.
A $20M Rolls Royce Boattail is only 10% faster than my car, yet costs 200X as much. And you can add integrated graphics to a CPU for about $15, and get a substantial portion of the performance of your 4080. Whoever said the price-performance curve must be linear?
Not in the US.
The cheapest one of those babies demands $1500 or a kidney, whichever is more expensive.
That's a misanalogy. The Rolls Royce, you're paying for the status symbol, not the product. The price differential is status, which really is a special kind of stupid. But that's a conversation for another day. In the case of the 4080S/5090, you're paying for the product in both cases. I get that the price-performance curve isn't linear. But If it was 50% better performance for an 120% higher price, that would be different. 50% better performance for 700% higher price. The math logic aint logicing
I live in Canada. I can get a 4080S here probably for $1200 CAD, I converted to american dollars
I was looking on Amazon a few min ago and there are 2 models of RTX 4090 for 1799. While less ram and slightly slower I am surprised either way.
That's a misanalogy. The Rolls Royce, you're paying for the status symbol, not the product.
I'd argue that most 5090 buyers are paying for status as well. In any case, the integrated graphic - 4080S comparison is certainly apt. I'll also note that, if you compare MSRPs, the 5090 is only 100% higher than the 4080s. Which reinforces my point: no amount of online grousing can circumvent the laws of economics. When there are more buyers than sellers, the price is going to rise. That logic is indeed ineluctable.
I don't disagree with your point about economics at all, but MSRP to MSRP comparisons are pointless because neither one is at MSRP. Obviously the prices are as high are they are because people are willing to pay that. What I just can't understand is why someone is willing to pay 700% more price for a 50% better performance. I guess if you have more money than god and rock solid fire inusrance on your house, go ahead, but I can't imagine that this is the masses of people buying a 5090. I also don't think most of them are purchased for status. None of this makes any sense
I don't disagree with your point about economics at all...What I just can't understand is why someone is willing to pay 700% more price for a 50% better performance.... I can't imagine that this is the masses of people buying a 5090. I also don't think most of them are purchased for status. None of this makes any sense
Phrased that way, your question indeed makes sense, but the answer is simple. Most of the 5090 buyers are looking for AI usage, not video games, where the doubling of memory (and near tripling of memory bandwidth) is what counts the most.

### Article 179 · 2026-09-14 · foxbusiness.com
Trump calls Nvidia CEO Jensen Huang during summit, dismisses AI fears as 'hoax'

By Sophia Compton FOXBusiness
Vertiv CEO Giordano Albertazzi discusses the demand for artificial intelligence infrastructure and explains why warnings about AI development will not slow down the buildout on ‘The Claman Countdown.’
Nvidia CEO Jensen Huang received a surprise phone call from President Donald Trump on Monday, in which the president dismissed fears that AI poses an existential threat to humanity and argued against calls to slow frontier AI development.
While speaking on stage at the All-In Summit in Los Angeles, Huang answered the call and placed Trump on speakerphone for the audience of thousands, as shown in a video of the event shared by the All-In Podcast .
"I’m telling you, it’s all a hoax," Trump said. "The data centers are great, and they make people wealthy, and they make states wealthy, and it's the oil of the next 20–25 years."
Trump said critics are "playing right into the hands of a lot of people that don't want to see it happen."
TRUMP RESPONDS TO RISING AI SAFETY CONCERNS, INSISTS TECH WILL BE 'MORE GOOD THAN BAD'
"That could be political people. It could also be China. And we're not going to let that happen," Trump said.
The president also rejected the idea that AI could pose an existential threat to humanity.
"The robots are not going to be taking over the world," the president added.
Separately on Monday, Trump shared a series of Truth Social posts defending AI development and criticizing calls for increased regulation.
"AI taking over the World , destroying Humanity, and all other things bad, is a HOAX," Trump wrote.
TECH CEO WARNS CENTRALIZED AI POWER COULD LEAD TO 'COUNTERFEIT' HUMANS, TECHNOCRATS SEEKING CONTROL
Trump's remarks come as the debate over AI safety intensifies across Silicon Valley and Washington.
Anthropic CEO Dario Amodei published an essay over the weekend urging the industry to "slow the pace" of frontier AI development.
Amodei argued that while AI could deliver enormous benefits, companies should strengthen safeguards as the technology becomes increasingly capable.
"AI brings risks, and because it is such a powerful technology , these risks are serious. I’ve written a lot about them too. They include the risk of losing control of AI systems, misuse of AI for cyberattacks and bioterrorism, and serious economic disruption," Amodei wrote.
SAM ALTMAN IDENTIFIES TWO BIGGEST RISKS FACING AI'S FUTURE
The essay also drew support from OpenAI CEO Sam Altman and SpaceX CEO Elon Musk.
"Dario is right," Musk wrote on X.
Altman echoed the sentiment, writing: "I agree with Dario that we need to pace the frontier. This has been a primary topic of discussions we've had at OpenAI in recent weeks."
Nvidia could not immediately be reached by FOX Business for comment.

### Article 180 · 2026-09-14 · tomshardware.com
Nvidia, Palantir, and others restrict advanced AI model usage over privacy concerns, report claims — 'paranoia' rising over customer intellectual property

Nvidia, Palantir, and others restrict advanced AI model usage over privacy concerns, report claims — 'paranoia' rising over customer intellectual property | Tom's Hardware
Nvidia, Palantir, and others restrict advanced AI model usage over privacy concerns, report claims — 'paranoia' rising over customer intellectual property
By Oliver Haslam
Zero data retention policies and air-gapped servers have become vital to some big AI users.
Anthropic and OpenAI are both facing uncomfortable questions from some large AI customers over concerns about how proprietary data may be used to train AI models. Some companies are so worried that they have begun demanding assurances about how their data is handled or going so far as to place limitations on which models their employees can use, and for which tasks, The Information reports. They fear that models may be trained on their intellectual property and information.
The issue can be traced back to a June change by Anthropic. Following the change to its flagship Fable model's policies, Anthropic can now retain customer data. The company argues that it only does so to ensure that Fable isn't being misused. But some companies have raised concerns that it means sensitive business data will be caught up in the sweep.
While both OpenAI and Anthropic point out that they don't train their models on the information given to them by companies with specific enterprise contracts by default, that doesn't tell the full story. Both companies do collect metadata from the same corporate customers, and while information on exactly what that metadata contains is hard to come by, OpenAI notes that it's only used “to better understand how our services are used." Anthropic also argues that any data it collects about how customers use its products is aggregated and anonymized. And that metadata isn't used to train models.
Regardless, there are still concerns over a perceived lack of clarity about what is collected. Telecoms outfit C Spire has agreements with both OpenAI and Anthropic that prevent either from using its data to train models, the report says.
However, the contracts do allow both OpenAI and Anthropic to collect C Spire technical usage data. C Spire believes that includes information about what applications AI models are connected to as well as usage data. It also worries that the AI companies may collect information about what their models get up to between generating responses.
For its part, OpenAI says that it does not use this "chain-of-thought" data to train its models. But C Spire still believes it needs a better understanding of what data is being collected, the report adds. It argues that neither AI company is being clear in its explanations.
One solution to any privacy concerns could be to use air-gapped servers, something aerospace company Northrop Grumman has already chosen to do. The Information reports that the company runs open-source AI models on its own air-gapped servers rather than trusting the likes of OpenAI and Anthropic.
Alternatively, Microsoft is already trying to take advantage of any data privacy concerns by tempting OpenAI and Anthropic customers to its own secure AI platforms. Microsoft's isolated cloud environments run AI models on private servers that don't send any data to external AI companies. But this approach is costly, and the report notes that at least one customer is still considering Microsoft's alternative approach.
Pharmaceutical company Novo Nordisk has taken a slightly different approach. While it continues to use Anthropic's Claude for some tasks, it has a ban on allowing any proprietary data to be used by the model.
It's clear that a lack of trust has the potential to cost AI companies real money, and in one instance, it already has. The same report notes that a large U.S. utility company has already canceled its plans to test Anthropic's Fable. The utility company wanted to know if Fable could run its core power infrastructure but ultimately pulled the plug over Anthropic's refusal to agree to a nonrevocable zero data retention (ZDR) policy.
Nvidia has also decided to use Fable for tasks that don't require it to gain access to sensitive data. The company points to the same lack of ZDR guarentees as the reason. Instead, Nvidia uses its own in-house AI solution for tasks that it deems too sensitive for Anthropic's model. Nvidia CEO Jensen Huang has famously remarked that its employees should use AI tokens worth half their annual salary every year.
Toms Hardware reached out to Nvidia for comment but did not receive one by publication.
Northrop Grumman is more accurately a defense contractor. Aerospace, yes, known for such but not nearly all they do.
I think the world has an expectation that OpenAI, Anthropic, and any other cloud AI provider can and should have the means to discover malicious uses, report on it (transparency), and stop the abuse. Anthropic just released a report on several threat actors that they caught and most part stopped. True NZD makes this much harder.
Just goes back to the on-prem (and remember that you can run your own private cloud) vs. public cloud debate in IT, which is decades old now.

### Article 181 · 2026-09-14 · zacks.com
NVIDIA vs. Marvell: Which AI Infrastructure Stock Is the Better Buy?

NVIDIA vs. Marvell: Which AI Infrastructure Stock Is the Better Buy?
NVIDIA Q2 fiscal 2027 revenues surged 106% to $96.22B, with data center sales up 117% to $89.02B.
Marvell expects fiscal 2028 revenues to rise about 50% to $18B as custom AI programs and networking ramp up.
NVIDIA trades at 16.78X forward P/E versus Marvell's 41.74X, supporting the article's better-buy call.
NVIDIA Corporation ( NVDA Quick Quote NVDA - Free Report ) and Marvell Technology, Inc. ( MRVL Quick Quote MRVL - Free Report ) are two major beneficiaries of the rapid expansion of AI data centers. NVIDIA leads the market in AI accelerators and networking, while Marvell has built strong positions in custom silicon, optical connectivity and data center switching. Their relationship has also become more interesting following the 2026 NVLink Fusion partnership.
Both companies delivered exceptional results in the latest reported quarter, but their valuations and risk profiles are now very different. So, which AI infrastructure stock offers the better investment opportunity today?
Let’s find out.
NVIDIA: The AI Leader With Stronger Financial Muscle
NVIDIA continues to deliver outstanding financial results. In the second quarter of fiscal 2027, revenues surged 106% year over year to $96.22 billion, while non-GAAP earnings per share (EPS) jumped 120% to $2.22. Non-GAAP gross margin expanded 250 basis points to 75%.
NVIDIA remains the clear leader in AI infrastructure. Cloud providers, enterprises and governments continue to invest billions of dollars in building AI data centers, and NVIDIA's graphics processing units (GPUs) remain the preferred choice for training and running advanced AI models.
NVIDIA's Blackwell and Vera Rubin AI platforms are seeing strong customer adoption due to their superior performance and energy efficiency. The company is also strengthening its position beyond GPUs through networking products such as InfiniBand, Spectrum-X Ethernet and NVLink, enabling it to capture a larger portion of AI infrastructure spending.
NVIDIA's latest quarterly numbers highlight this leadership. During the second quarter of fiscal 2027, the data center business generated $89.02 billion in revenues, accounting for more than 92% of total sales. The segment’s revenues climbed 117% year over year and 18% sequentially, driven by rapid deployment of Blackwell and Vera Rubin systems and growing networking demand.
Another key advantage is NVIDIA's software ecosystem. CUDA, along with its expanding AI software portfolio, creates high switching costs for customers, making it difficult for competitors to take market share. This competitive advantage extends well beyond hardware and should continue supporting long-term growth.
As AI adoption expands from model training to large-scale inference and enterprise deployment, NVIDIA is positioned to benefit across every major phase of the AI investment cycle. Four top hyperscalers — Amazon, Alphabet, Microsoft and Meta Platforms — alone are expected to spend roughly $720 billion to $745 billion on capital expenditures in 2026, with a large portion directed toward AI infrastructure. The company expects fiscal 2028 revenues to grow approximately 70%, although supply remains a constraint.
Nonetheless, NVIDIA does face risks. The company faces rising memory costs, which are expected to pressure gross margins. It expects non-GAAP gross margin to fall toward 71%-72% in the fourth quarter of fiscal 2027 before recovering to 72%-73% in fiscal 2028. China restrictions, competition and supply-chain dependence are additional challenges.
MRVL is becoming an increasingly important player in AI infrastructure, particularly in networking, optical connectivity and custom AI silicon. In the second quarter of fiscal 2027, Marvell’s revenues soared 36.5% year over year to a record level of $2.74 billion, while non-GAAP EPS surged 40.3% to 94 cents.
Marvell’s data center end market remained the major contributor to the outstanding second-quarter performance. The data center revenues climbed 46% year over year to $2.17 billion. The company expects fiscal 2027 revenues to grow approximately 45% year over year to nearly $12 billion and fiscal 2028 revenues to increase roughly 50% to $18 billion, driven mainly by booming AI demand.
Another growth driver is Marvell’s custom AI chip business. During the second-quarter earnings call, management forecasted that custom revenues would more than double in fiscal 2028 as multiple hyperscaler programs ramp up into production. This positions Marvell to benefit from the growing interest in custom AI accelerators among cloud companies.
Marvell Technology, Inc. Price, Consensus and EPS Surprise
The company is also expanding through acquisitions and partnerships. Its collaboration with NVIDIA around NVLink Fusion, optics and AI-RAN creates new growth opportunities in AI infrastructure. The partnership could position Marvell to capture more scale-up networking opportunities as AI clusters become larger and require significantly more bandwidth. Marvell’s recent acquisition of Polariton Technologies, XConn Technologies and Celestial AI is likely to strengthen its capabilities across the data center infrastructure, optical connectivity and AI scale-up technologies.
Nonetheless, Marvell isn't without risks. Its communications and other business segment remains somewhat volatile, with third-quarter revenues expected to decline in the low-to-mid teens year over year. Its non-GAAP gross margin of 58.9% is also well below NVIDIA's 75%. Much of Marvell's upside depends on successful custom-silicon programs and continued hyperscaler spending, creating execution and customer-concentration risks.
NVDA vs. MRVL: Which Has a Better Growth Profile?
Both companies will benefit from the surging demand for AI chips, but NVIDIA’s growth profile appears stronger in the near term.
The Zacks Consensus Estimate for NVDA’s current fiscal 2027 revenues and EPS indicates a year-over-year surge of 87.4% and 93.5%, respectively. The consensus mark for fiscal 2028 revenues and EPS signifies a year-over-year increase of 63.2% and 63.8%, respectively.
By contrast, estimates for Marvell’s fiscal 2027 point to more modest 46.3% revenue growth and a 46.8% EPS increase. For fiscal 2028, revenues are estimated to grow 48.4%, while EPS is expected to increase 57.5%.
Despite MRVL's spectacular 177.9% YTD gain compared with 17.1% for NVDA, NVIDIA currently offers the more attractive earnings valuation. NVIDIA trades at a forward 12-month price-to-earnings (P/E) multiple of 16.78 versus 41.74 for Marvell. This is a major difference considering that both companies are benefiting from the same broad AI infrastructure spending wave.
Marvell's premium valuation reflects its accelerating growth outlook and the market's enthusiasm for custom silicon, optical connectivity and AI networking. However, investors are already paying heavily for that future growth. NVIDIA, in contrast, combines much stronger absolute earnings, significantly higher margins, enormous cash generation and a broad AI platform with a much lower P/E multiple.
The valuation gap gives NVIDIA a stronger risk-reward profile. Marvell may deliver faster percentage growth from a smaller revenue base, but its stock already reflects substantial optimism.
Conclusion: NVDA Is the Better Buy Today
Both NVIDIA and Marvell are well-positioned to benefit from the massive AI infrastructure buildout happening across hyperscalers, enterprises and sovereign AI projects. MRVL is building strong momentum in AI networking, optical connectivity and custom AI chips, making it an attractive long-term AI growth story.
However, NVDA seems the better investment bet right now. The company continues to dominate AI computing with industry-leading GPUs, networking platforms, software ecosystems and rapidly expanding AI infrastructure solutions. NVIDIA is also delivering superior revenue growth and profitability while trading at a lower valuation multiple than Marvell.
Currently, NVIDIA sports a Zacks Rank #1 (Strong Buy), making it a must-pick compared with Marvell, which has a Zacks Rank #3 (Hold). You can see the complete list of today’s Zacks #1 Rank stocks here .

### Article 182 · 2026-09-14 · qz.com
Palantir, Nvidia, Booz Allen restrict Anthropic and OpenAI models

Palantir $PLTR Technologies, Nvidia $NVDA , and Booz Allen Hamilton are restricting or threatening to drop advanced AI models from Anthropic and OpenAI unless the labs provide stronger data protections, according to Reuters . The Information first reported the story, citing people familiar with the matter.
The core concern is that model providers could retain or extract value from customers' sensitive corporate information. Palantir has pressed Anthropic to provide guarantees of zero data retention before making its models available through Palantir 's software, according to Reuters. Nvidia restricts Anthropic's models to less sensitive internal tasks, preferring its own Nemotron models for proprietary work; Booz Allen, meanwhile, has forbidden staff from running Anthropic's commercial model on cybersecurity projects that touch proprietary data.
The pushback intensified after Anthropic introduced a 30-day data retention policy in June tied to the rollout of its Fable 5 model, saying it needed usage logs to detect sophisticated attacks that unfold across multiple sessions. Anthropic said at the time that it would not use the retained data to train its models, but the policy drew objections from enterprise customers, particularly those in regulated industries. OpenAI has faced related scrutiny over claims it may have trained models on user data, according to Reuters.
Anthropic responded by announcing Enterprise Frontier Safeguards, a system that allows enterprise customers to store activity data in their own cloud infrastructure — including Amazon $AMZN S3, Azure Blob Storage, or Google $GOOGL Cloud Storage — under their own encryption keys. Automated safety monitoring still scans for misuse, but no human review by Anthropic employees is required, the company said. The system is rolling out to customers in phases, with broader availability targeted for later this fall.
Neither AI lab trains on customer data by default, Reuters reported, though both collect anonymized metadata for product improvement unless companies choose to opt in.
The restrictions reflect a broader shift that Palantir CEO Alex Karp has described publicly. Last week, Palantir and Nvidia unveiled a platform pairing Palantir 's software with Nvidia 's open Nemotron models, designed to let organizations run AI on their own data without exposing it to outside model providers. Nvidia is the first customer for the supply-chain application of that technology, according to Benzinga .
Microsoft $MSFT , for its part, is seizing on the anxiety among enterprise customers to market its own AI products and segmented cloud infrastructure to prospective clients.

### Article 183 · 2026-09-14 · pro.thestreet.com
Why I Bought Nvidia Into Monday’s AI Panic

Why I Bought Nvidia Into Monday’s AI Panic
The AI selloff has investors running. I’m doing the opposite.
It’s ugly out there Monday morning. Shares of chip designers, chip manufacturers and all AI-related companies were hit with steep declines on Monday after several executives at leading U.S.-based AI companies called for slowing the pace of this kind of technological development amid concerns over potential risks to humanity.
The beatdown started in Asia. Softbank ( SFTBY ), a large investor in OpenAI, was down more than 13% on Monday in Tokyo. In Seoul, memory chip makers SK Hynix ( SKHY ) and Samsung Electronics ( SSNLF ) gave up more than 6% and 4%, respectively. Taiwan Semiconductor ( TSM ) was trading nearly 4% lower as well. Taiwan Semi is currently the second-largest holding in the Sarge-folio.
It’s true. My Sarge-folio bought some Nvidia ( NVDA ) Monday morning. Yes, we’re in a lot of chip and AI stocks. Sure, we’re getting punched in the nose on these at the moment. It’s also true that we’re up nicely since initiation on almost all of those names. Not that I know that this dip is the one to buy. It’s that I do know that Nvidia will remain at the forefront of the cloud-based, autonomous automation, artificial intelligence revolution.
Won’t spending on AI slow down now that key players are worried about a human extinction event? Maybe. Probably. The fact is also this: The bad guys will continue to develop this technology. The good guys are going to be forced to develop the same technology just to keep the bad guys in check. The lines between what is a good guy and who is a bad guy may change often going forward.
The fact is that these horses have left the barn. The cat is out of the bag. If the U.S. or Chinese or Russian or other militaries are concerned about near-peer adversaries gaining advantage, they won’t be able to “slow the pace.” If criminal enterprises are going to try to gain an advantage, then law enforcement will be forced to try to keep up. A lot of dough is going to go into the development of AI for nefarious purposes whether we like it or not.
Those who might be on the side of legitimate business or countering those nefarious efforts are going to require the same kinds of funding that goes into ripping off or threatening the masses. I don’t like it either, but it’s too late to go back and try something else.
Again. Just three weeks ago, Nvidia reported its fiscal second-quarter financial results. The company posted adjusted EPS of $2.22 on revenue of $96.22 billion. That beat Wall Street by more than $4.0 billion and was good for year-over-year growth of 106%.
For the current quarter, CEO Jensen Huang’s firm projected revenue of $108.0 billion (+/-2%) vs. consensus for $104.6 billion. That would be good for growth of roughly 90% and Nvidia Is known for beating its guidance.
Of the 42 analysts that I know to cover NVDA, 35 have already revised their earnings estimates higher for the current quarter since it started.
Readers will see that NVDA opened just below its 50-day simple moving average (SMA) and just below the lower trendline of our Andrews’ Pitchfork model. I added at that line during the pre-opening session.
I will also add below that level after publication at least once. Will I admit I’m wrong? You know I will (I always do), but not until this stock loses its 200-day SMA at $197.
At the time of publication, Guilfoyle was long TSM and NVDA equity.
By Stephen Guilfoyle

### Article 184 · 2026-09-14 · gurufocus.com
Elon Musk Just Made a Huge Nvidia AI Prediction About Space

Elon Musk expects SpaceX to put Nvidia ( NASDAQ:NVDA ) artificial intelligence computing systems into orbit next year, potentially extending the chipmaker's technology beyond conventional data centers, according to a Monday post on X.
Musk said he expects SpaceX to deploy Nvidia's Vera Rubin NVL72 platform in space during 2027. The system combines 72 Rubin graphics processing units with 36 Vera central processing units, along with networking and data-processing components.
SpaceX Chief Financial Officer Bret Johnsen previously said the company relies on Nvidia chips for its planned orbital computing effort. He also indicated that the partnership could help SpaceX secure the chip supply needed for the project.
The initial satellites are targeted for launch in 2027, with additional deployments planned for 2028. SpaceX intends to modify the spacecraft platform used for newer Starlink satellites, replacing communications hardware with computing equipment and increasing solar-generation capacity.

### Article 185 · 2026-09-14 · businessinsider.com
Trump called Nvidia CEO Jensen Huang mid-interview to rip AI doomerism: 'The robots will not be taking over'

By Geoff Weiss
Nvidia CEO Jensen Huang got a call from President Donald Trump in the middle of his interview to swat down AI doomer predictions.
On Monday at the All-In Summit in Los Angeles, Huang's talk was interrupted by a phone call from President Donald Trump, who called AI doomerism "a hoax."
"The robots will not be taking over," Trump said via speakerphone, adding that while "we have to be a little bit careful," the US shouldn't stop AI advancement.
The debate on AI safety has roiled Silicon Valley, especially after Jacob Coxon , a former Anthropic researcher, announced last week he resigned from the lab, writing on X that the people building AI "believe that it could kill us all by the end of the decade."
During the talk, Huang praised a former Anthropic researcher for speaking out on AI safety and also said the notion that the technology poses an existential threat is unscientific.
Weighing in, Huang called AI safety "paramount" and said that the US can still move fast.
"America is able to lead — and to do it safely," he said.
Huang said Coxon showed "great courage" by coming forward. He also said there's a difference between exposing existing problems within a company and making predictions about the future.
"I think the whistleblowing is fine. I think the scientific prediction about the future is less fine because it's not grounded on science, obviously," Huang said.
Huang said he doesn't know what Coxon witnessed inside Anthropic and suggested the industry's frontier labs are undergoing a difficult transition from research to engineering organizations.
The Nvidia CEO's comments are consistent with his established views. He's previously pushed back on what he's called "science fiction" scenarios that scare people away from investing in technology that could make AI safer.
Trump also posted on Truth Social on Monday, saying that he was "breaking another Hoax — That AI is going to take over, consume, and destroy the World."
Nvidia did not immediately respond to a request for comment from Business Insider.

### Article 186 · 2026-09-14 · tradingview.com
Nvidia's Customer Concentration Problem: CFO Says 'We Get Paid Twice'

Nvidia Corp ‘s NVDA AI revenue comes from just a handful of buyers. CFO Colette Kress hopes to turn that customer concentration risk into recurring revenue by getting paid once for GPUs and again when they generate compute income.
Three direct customers generated 44% ($78.2 billion) of Nvidia’s $177.8 billion revenue in the first half of fiscal 2027—up from two customers driving 35% a year earlier.
That rising concentration underscores how heavily Nvidia’s growth relies on a handful of tech giants. Even as Data Center revenue surged 117% year-over-year to $89 billion last quarter, Nvidia is now pushing to broaden who consumes its compute, not just who buys its GPUs.
Nvidia Wants to Get ‘Paid Twice’
Enter Nvidia’s “neocloud” strategy.
Under the model, Nvidia sells data center infrastructure to AI cloud providers and backs them with cloud-service agreements to help finance capacity. In exchange, Nvidia takes a cut of the rental revenue when third parties use that compute.
CFO Colette Kress summarized the strategy on the earnings call: "In this model, we get paid twice—once on the hardware sale and again through the share of rental revenue."
By capturing that secondary stream, Nvidia moves from simply supplying AI infrastructure to sharing in the ongoing economics of AI demand.
Nvidia expects non-hyperscaler businesses — including sovereign AI, regional neoclouds, enterprises, edge computing and air-gapped data centers — to represent roughly half of its Data Center business.
The company’s neocloud agreements are designed to help unlock that market. Nvidia’s commitments under the new model totaled $36 billion as of July 26. They typically span six years, and decline as third-party customers, or Nvidia itself, consume capacity.
That creates a potentially powerful feedback loop: Nvidia sells GPUs to expand the customer base, the expanded customer base drives utilization, and Nvidia gets another revenue stream from that utilization.
For investors, the bigger story is not simply whether Nvidia can keep selling more GPUs. It is whether the company can turn its dominant hardware position into a recurring claim on the broader AI economy.
Watch neocloud utilization, revenue-sharing growth and the expansion of non-hyperscaler demand. If those accelerate, Nvidia’s customer concentration could become less of a weakness — and another source of leverage.

### Article 187 · 2026-09-14 · fool.com
Prediction: The Next Nvidia-Backed Stock to Go Parabolic Could Be Hiding in Plain Sight

Nvidia ( NVDA +2.55% ) runs an artificial intelligence (AI) empire. You might think of the company as an AI chip designer, making the graphics processing units (GPUs) needed for key AI tasks like model training. But Nvidia has expanded beyond the chip to create entire systems and designs platforms for specific industries, such as healthcare. On top of this, the company aims to play a role in every part of the AI ecosystem, and that's reflected in its latest move: its offer to acquire AI open-source platform Hugging Face.
All of this suggests Nvidia has a keen understanding of the AI space, offering it the ability to identify other companies likely to excel. And those companies may be found in Nvidia's investment portfolio. The AI giant right now is invested in eight companies, according to its latest 13F filing to the Securities and Exchange Commission.
My prediction is that one of these players, a company that's hiding in plain sight, will be the next Nvidia-backed stock to go parabolic. Let's check it out.
Nvidia's understanding of the AI industry
As mentioned, Nvidia, thanks to the broad role it plays in AI, has what it takes to identify potential winners in the space. The company understands the products and services likely to drive the next phases of the AI boom and works with a variety of other AI players across specialty areas. These partnerships have helped Nvidia get to know every angle of the AI story.
Now, let's consider the Nvidia-backed stock that could be set to soar. And this player is CoreWeave ( CRWV +4.11% ) , a specialized cloud company that has been working closely with Nvidia for several years. CoreWeave's business is actually very closely linked to demand for Nvidia's GPUs: CoreWeave offers customers access to these top chip systems. The company has built up a fleet of Nvidia GPUs, and customers can rent them for a short period of time or for a long-term project.
This has proven to be an excellent business, with CoreWeave's revenue soaring. In the latest quarter, revenue surged 112% to a record high of $2.6 billion, and backlog reached $104 billion. And the company said it won more than $25 billion in net new customer commitments in the early days of the third quarter.
"Our near-term capacity remains effectively sold out," chief executive officer Michael Intrator said during the recent earnings call. "That is translating into signed commitments on increasingly favorable terms from a broadening set of customers and is positioning CoreWeave to gain market share for years to come."
CoreWeave, due to its close relationship with Nvidia, has been the first to make the chip giant's new systems -- from Blackwell to Blackwell Ultra -- generally available to customers. And Nvidia has even pledged to buy any capacity through April 2032 that hasn't been used. So Nvidia clearly has confidence in CoreWeave's prospects.
Investors have worried about CoreWeave's debt, something that's been necessary to build out infrastructure. In the latest quarter, the company's loss deepened, and interest expenses climbed to $640 million from $267 million in the year-earlier period.
But it's important to note that this investment is necessary for the company to keep up with demand and generate growth. So what does this mean for you as an investor? CoreWeave is an investment that involves some risk, so if you're a cautious investor or focus on value stocks, this probably isn't the right choice for you.
If you're an aggressive investor, though, you might give CoreWeave a second look. The company, as a key partner of Nvidia, is well-positioned to gain ground in the high-growth field of AI. It's already demonstrated enormous growth, and the message from leaders throughout the market is that AI demand is going strong. This is likely to continue as AI is applied to more real-world uses.
And that's why I predict that the next Nvidia-backed stock to go parabolic, a company hiding in plain sight, is CoreWeave.
By Adria Cimino – Sep 14, 2026 at 5:10AM EST

### Article 188 · 2026-09-14 · cnbc.com
Trump phones Nvidia’s Huang at All-In Summit, calls data center opposition a ‘hoax’

President Donald Trump called Nvidia CEO Jensen Huang while the tech exec was on stage at the All-In Summit in Los Angeles, according to social media posts from attendees.
Trump's remarks focused on the backlash to artificial intelligence and data center construction, a topic that's increasingly roiling Washington.
U.S. President Donald Trump delivers remarks to U.S. Embassy personnel and business leaders at Deerfield Residence on September 12, 2026 in Dublin, Ireland.
After using his social media site to blast Anthropic CEO Dario Amodei's push for the AI industry to slow down development, President Donald Trump went a step further on Monday.
With Nvidia CEO Jensen Huang speaking on stage at the All-in Summit in Los Angeles, Trump called the tech exec, and was then put on speaker.
"I'm telling you, it's all a hoax," Trump said, according to a video posted on social media by an attendee. "The data centers are great, and they make people wealthy, and they make states wealthy."
President Trump has inserted himself into the raging debate about artificial intelligence and whether the model developers, principally Anthropic and OpenAI, are rapidly building technology that threatens to destroy humanity. Over the weekend, Amodei published an essay arguing for the intentional slowing of the pace of model development, garnering support from OpenAI CEO Sam Altman and SpaceX's Elon Musk .
Opposition to data center development and concerns about AI have been conflated into the same discussion as people increasingly worry that the technology is taking their jobs.
Trump published numerous posts on Truth Social, including one where he said those concerned about AI and data centers are "Revolutionaries for a Bad and Evil Cause." In another post, Trump said he didn't see any need for additional AI regulation , and called the recent AI concerns a "hoax" and "a scam." He wrote that calls to slow down building are only happening because the U.S. is leading other countries in its pace of construction.
After Huang put Trump on speakerphone on Monday, the president said data centers are the "oil of the next 20, 25 years."
He also joked that Huang, CEO of the world's most valuable company, "can develop the most complex computer chip that nobody can copy, but he can't figure out how to put me on speaker."
Trump praised the construction of AI data centers, which are being filled with Nvidia's graphics processing units. While Huang and Trump have appeared together in public several times during the president's second term, Monday's phone call further highlights their tightening bond and the centrality of AI to the U.S. economy, even as other policymakers urge regulation.
"I'm with you all the way," Trump told Huang.
Those opposing data center construction are "playing right into the hands of a lot of people that don't want to see it happen," Trump said, adding that it could be coming from China.
"We're not going to let that happen," Trump said.
"You're right," Huang replied. "We're not going to let that happen, sir."
Chamath Palihapitiya, one of the co-hosts of the summit, posted on X after the session in reference to one of the videos of it, "This was surreal."
An Nvidia representative didn't respond to a request for comment.

### Article 189 · 2026-09-14 · fxleaders.com
NVIDIA Stock Forecast: Can NVDA Reclaim $235 and Push Toward $300?

NVIDIA Stock Forecast: Can NVD...
NVIDIA Stock Forecast: Can NVDA Reclaim $235 and Push Tow...
NVIDIA Stock Forecast: Can NVDA Reclaim $235 and Push Toward $300?
NVIDIA (NASDAQ: NVDA) is trading near $218.29, holding fairly steady after falling about 5% from its early-September high of $235.74...
NVIDIA's stock is currently trading around $218.29, having fallen about 5% from its September high of $235.74 amid regulatory scrutiny and a tech selloff.
The company reported record fiscal Q2 results with revenue of $96.2 billion, and it projects $108 billion for fiscal Q3, despite potential margin pressures.
NVIDIA's acquisition of Hugging Face for $12.9 billion aims to enhance its AI capabilities, while it is also considering a significant investment in Anthropic's IPO.
Despite bullish analyst sentiment and raised price targets, regulatory risks and insider selling pose challenges for investors.
NVIDIA ( NASDAQ: NVDA ) is trading near $218.29, holding fairly steady after falling about 5% from its early-September high of $235.74. The world’s most valuable company by market cap is now consolidating as investors weigh its strong earnings and a string of strategic deals against growing regulatory scrutiny and a wider tech selloff driven by rising Treasury yields.
Record Fiscal Q2 Results Keep the Bull Case Intact
NVIDIA’s results from late August continue to support the stock. Revenue for fiscal Q2 stood at $96.2 billion, twice as much as the previous year, and adjusted EPS was almost 7% higher than expected. Data center revenue rose to $89 billion, supported by $49 billion from hyperscaler activity and a 138% increase in its ACIE segment. In fiscal Q3, the company is projecting revenue of $108 billion and anticipates 70% growth for fiscal 2028, but it also cautions there will be upward pressure on margins due to increased memory costs and supply challenges.
Hugging Face Deal Expands NVIDIA’s AI Reach
In early September, NVIDIA announced the purchase of open weight AI model hub Hugging Face in a bid to expand beyond chips to tools for AI developers , spending approximately $12.9 billion on the company. The agreement would bolster the customer relationship with NVIDIA’s hardware and provide a more robust stance in the software segment of the AI marketplace.
Anthropic IPO Talks Point to a Bigger AI Bet
NVIDIA is reportedly considering anchoring a $10 billion Anthropic IPO this week, according to Reuters. The offering could sell up to $100 billion worth of shares at a valuation around $2 trillion, making it potentially the largest public offering in history. The transaction would be an extension of NVIDIA’s computing partnership with Anthropic, which saw its annualised revenue run rate rise from approximately $9 billion at the end of 2025 to over $65 billion by mid-2026.
Regulatory and Insider-Selling Risks Remain
Another risk for investors is that the DOJ is reportedly scrutinizing NVIDIA’s chip-licensing deal with Groq to see if it was designed to steer clear of antitrust violation. Meanwhile, director Mark Stevens has recently sold over $235 million of shares, leading to speculation of insider gain-taking given the stock’s bull market run. Higher Treasury yields have also weighed on the overall performance of AI stocks, though the 53.3% year-over-year gain in revenue for TSMC in August indicated strong demand for advanced chips.
NVDA remains within a neutral-to-bullish channel, with the 50-day EMA zone around $214.00–$217.00 providing near-term support. Under that, the next significant demand area is the $206.00 region. The 14-day Relative Strength Index ( RSI ) reading of 56 indicates that the stock has further upside and downside potential, with MACD pointing to a consolidation phase.
If prices continue to trade above $223.50, then they may be on the verge of reaching the $235.00–$238.60 resistance zone and possibly lasting into new record highs. On the downside, a close below $206 could expose the stock to a move toward $196–$199. Additionally, some technical services have recently upgraded NVDA to Buy Candidate status due to a growing volume of support around the price of $217.55.
The general sentiment on Wall Street remains bullish on NVIDIA. Phillip Securities has raised its price target to $300 from $285, while the other analysts have a consensus of $324. Investors will be focused on further details on the Anthropic IPO, the ongoing investigation of the DOJ’s Groq and updates on the Vera Rubin platform, which is anticipated to account for about 20% of anticipated data center revenue.
Is NVIDIA stock still a buy?
NVIDIA’s strong AI demand, earnings growth and strategic investments continue to support the bullish case. However, investors should also consider valuation, regulatory risks and the possibility of further volatility.
What is the NVIDIA stock price target?
Phillip Securities recently raised its target to $300, while the broader analyst consensus is around $324. Technical resistance near $235-$238 remains an important level for the stock in the near term.
NVIDIA remains fundamentally strong, but the stock is entering a more important technical phase. A break above $223.50 could put $235-$238 back in focus, while losing $206 would weaken the setup and expose NVDA to a move toward $196-$199.
Arslan Ali Butt serves as the Lead Commodities and Indices Analyst, bringing a wealth of expertise to the field. With an MBA in Behavioral Finance and active progress towards a Ph.D., Arslan possesses a deep understanding of market dynamics.
His professional journey includes a significant role as a senior analyst at a leading brokerage firm, complementing his extensive experience as a market analyst and day trader. Adept in educating others, Arslan has a commendable track record as an instructor and public speaker.
His incisive analyses, particularly within the realms of cryptocurrency and forex markets, are showcased across esteemed financial publications such as ForexCrunch, InsideBitcoins, and EconomyWatch, solidifying his reputation in the financial community.

### Article 190 · 2026-09-14 · finance.yahoo.com
Nvidia’s Training Trade Hit a Speed Bump. Intel Could Win From What Comes Next

The September 14 selloff treated slower frontier AI development as bad news for chips. The more interesting question is whether it changes which chips get bought. Reuters Breakingviews argued that a moderation in giant model-training runs could redirect part of this year's roughly $1 trillion AI investment toward inference, where existing models answer queries and run agents.
That creates a different contest for Intel Corporation (NASDAQ: INTC ) and NVIDIA Corporation (NASDAQ: NVDA ).
Inference does not erase GPUs, but it broadens the bill of materials
Intel's opportunity is the server CPU. Production AI applications need orchestration, memory, networking and general-purpose compute around accelerators, while inference and agentic deployments can require substantially more general-purpose compute alongside accelerators. Intel Corporation (NASDAQ:INTC) also reported $6.3 billion of Data Center and AI revenue in its latest quarter, up 59% year over year. A shift toward deployed agents could therefore reinforce its core franchise before Intel proves that its foundry turnaround can earn attractive returns.
Execution is where the thesis can break. Intel is spending heavily to rebuild manufacturing leadership and still generated negative adjusted free cash flow in its latest quarter. Inference growth helps only if Intel keeps enough share and margin against AMD, Arm-based CPUs and specialized accelerators.
NVIDIA Corporation (NASDAQ:NVDA) remains the strongest counterargument to a simple rotation thesis. Its GPUs run both training and inference, and CUDA plus newer inference-focused systems give Nvidia a path to monetize deployed AI even if frontier training slows. For Nvidia, the downside is relative rather than existential: fewer giant training clusters could reduce demand for the most expensive accelerators or weaken pricing at the margin.
Hedge funds were adding both before the debate changed
Insider Monkey's database counted 138 hedge funds holding Intel in Q2 2026, up from 112 in Q1. AQR Capital Management owned 10,742,567 shares after trimming its position 7%. Nvidia rose to 285 funds from 275, while Fisher Asset Management increased its stake 3% to 90,935,947 shares. Those filings predate the September 14 safety-driven market reaction.
Intel had 152,248,752 shares sold short on August 31, equal to 3.02% of float, with 1.69 days to cover.
A frontier slowdown would not automatically make Intel a winner or Nvidia a loser. It could, however, change the mix of spending from maximum-scale training toward serving billions of useful requests. If that happens, the AI trade becomes less concentrated in one type of accelerator and more dependent on the entire data-center stack. Intel finally has a credible reason to care about that shift.
While we acknowledge the potential of INTC and NVDA as investments, we believe certain other AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 191 · 2026-09-14 · finance.yahoo.com
Nvidia and other chipmakers suffer as AI warnings raise spending concerns

Chipmakers Nvidia Corp (NASDAQ:NVDA, XETRA:NVD), Micron Technology Inc (NASDAQ:MU) and Broadcom Inc (NASDAQ:AVGO, XETRA:1YD) fell on Monday as calls to slow artificial intelligence (AI) development raised concerns about future hardware spending.
Dario Amodei, chief executive of AI developer Anthropic , and rival executives have called for a slower pace of development.
Nvidia Corp (NASDAQ:NVDA, XETRA:NVD) traded 3% lower at $210.86 in morning trading.
Jeffrey Favuzza, an equities trading analyst at investment bank Jefferies, found no clear sign that the safety debate would moderate spending .
He highlighted Amodei's clarification that the call did not mean halting model training, the process of teaching AI systems to identify patterns.
Federico Manicardi and Victoria Campos, of investment bank JPMorgan's international trading desk, argued that AI adoption remained intact and excessive slowing risked ceding leadership.
Micron Technology Inc (NASDAQ:MU) fell 6% to $914.30, recording the largest percentage decline among the three chipmakers.
Madison Rezaei, an analyst at investment research firm Bernstein, said she expects weaker demand for rural data centres built for training if that activity slows.
She questioned how quickly demand could shift to inference, the process through which trained AI models make predictions, given uncertainty over profitable uses.
Broadcom Inc (NASDAQ:AVGO, XETRA:1YD) declined 5% to $344.50 as AI concerns added to caution over its revenue outlook.
Its fourth-quarter revenue forecast of $34.8 billion fell slightly below expectations of $35.03 billion, adding to shareholder caution.
Long-term earnings projections exceeded forecasts, but the short-term guidance shortfall weighed on sentiment after its September 2 results.

### Article 192 · 2026-09-14 · quantumcomputingreport.com
UCLA, Caltech, and NVIDIA Develop Fourier Neural Operator for Quantum Control Sequence Synthesis

A multi-institution research collaboration led by UCLA (NarangLab) , Caltech , and NVIDIA has introduced a machine-learning framework to automate the inverse design of quantum control pulse sequences. Detailed in a preprint published on arXiv (arXiv:2608.03702) and presented at IEEE Quantum Week 2026 , the method utilizes a Fourier Neural Operator (FNO) to learn high-dimensional molecular quantum dynamics, replacing numerical differential equation solvers inside optimal control loops.
The FNO surrogate was trained on GPU-accelerated quantum state propagations generated by NVIDIA CUDA-Q Dynamics across an 888-dimensional Hilbert space modeling the trapped hydronium ion (H₃O⁺). Incorporating physics-informed frequency detuning embeddings and polarization symmetry constraints (σ⁺ and σ⁻ channels), the FNO surrogate predicts population trajectories across Raman sideband pulse windows up to ~10⁷× faster than accelerated GPU numerical propagation solvers. The surrogate is fully differentiable, enabling direct gradient-based optimization of continuous laser pulse parameters.
[ FNO-SPMP Control Performance vs. Reinforcement Learning Baseline ]
Fourier Neural Operator (FNO-SPMP)
Standard Reinforcement Learning (RL)
• Target Population Density: 0.98
• Preparation Success Rate: Up to 86.2%
Built on top of the differentiable FNO, the team implemented a stochastic pulse-measurement planner (FNO-SPMP) to navigate thermal population distributions at 20 K. On H₃O⁺, the framework generated pulse sequences that funneled thermal populations into single rotational/hyperfine states with an 86.2% success rate, reducing sequence synthesis latency from 10 hours down to 10–20 minutes. The methodology establishes an operator-learning paradigm within NVIDIA’s CUDA-Q platform to synthesize pulse-level control for molecular spectroscopy and complex QPU gate calibration.
Review the technical update via UCLA NarangLab here , examine the peer-reviewed preprint on arXiv here , and read our prior coverage of NVIDIA CUDA-Q Platform Integrations here .

### Article 193 · 2026-09-14 · investingnews.com
Nvidia Mulls $10B Role in Anthropic's Mega IPO

Anthropic aims to raise up to US$100 billion before the US midterm elections in November, setting up the largest IPO in history.
Anthropic is negotiating to secure NVIDIA (NASDAQ:NVDA) as an anchor investor for a record-breaking initial public offering (IPO) that could value the startup at roughly US$2 trillion.
According to a Reuters exclusive , the chipmaker is weighing a US$10 billion commitment to the offering, serving as an early backer that could signal strong institutional confidence to public markets preparing to absorb the astronomical valuations and capital demands of frontier artificial intelligence labs.
Anthropic’s push for public capital follows an explosive surge in sales. The company’s annualized revenue run rate eclipsed US$65 billion by late July, skyrocketing from approximately US$9 billion at the end of 2025.
Following a US$65 billion private funding round in May that valued the maker of Claude at US$965 billion post-money, the company is now projecting US$190 billion to US$200 billion in revenue by 2028 to support the US$2 trillion public price tag.
The IPO discussions expand existing operational ties between Anthropic and NVIDIA.
In November 2025, NVIDIA pledged up to US$10 billion to the startup, tied to an agreement requiring Anthropic to purchase US$30 billion in NVIDIA-powered Microsoft (NASDAQ:MSFT) Azure computing capacity.
More recently, NVIDIA has deployed its own balance sheet to directly broker physical infrastructure access for Anthropic. In late August, Anthropic signed a US$35 billion cloud-computing contract with Lambda, a cloud provider backed by NVIDIA.
In a highly structured arrangement, NVIDIA holds the actual lease on the 700 megawatt Nueces County, Texas, data center being developed by Hut 8 (TSX:HUT,NASDAQ:HUT) . This guarantees the space and allows Lambda to service Anthropic without procuring the real estate itself.
Earlier in August, Anthropic executed a similar US$45 billion agreement with another NVIDIA-backed cloud provider, Nscale, to lease capacity in West Virginia.
Despite its reliance on NVIDIA graphics processing units, Anthropic continues to diversify its supply chain.
The startup committed over US$100 billion in April to Amazon Web Services over the next decade, anchored by plans to use more than 1 million Amazon (NASDAQ:AMZN) Trainium2 chips.
It simultaneously secured multiple gigawatts of tensor processing unit (TPU) capacity from Google (NASDAQ:GOOGL) and Broadcom (NASDAQ:AVGO) in a separate deal . Google is actively providing financial guarantees to help Hut 8 raise debt for separate Anthropic data centers designed specifically to house TPUs.
Don't forget to follow us @INN_Technology for real-time news updates!
Securities Disclosure: I, Giann Liguid, hold no direct investment interest in any company mentioned in this article.
Giann Liguid is a graduate of Ateneo De Manila University with an AB in Interdisciplinary Studies. With a diverse writing background, Giann has written content for the security, food and business industries. He also has expertise in both the public and private sectors, having worked in the government specializing in local government units and administrative dynamics.
When he is not chasing the next market headline, Giann can most likely be found thrift shopping for his dogs.
Learn about our editorial policies.

### Article 194 · 2026-09-14 · qz.com
Nvidia, chip stocks fall as AI CEOs call for slowdown

Nvidia $NVDA stock fell 2% in premarket trading Monday as AI safety concerns rattled global tech markets. Shares of Broadcom $AVGO , Intel $INTC , and Marvell Technology dropped 3%, 5%, and 7%, respectively, after leaders of major artificial intelligence companies over the weekend called for a slowdown in AI development.
Anthropic CEO Dario Amodei published an essay Saturday contending that AI companies must pull back on advancing their most powerful models, citing the safety dangers such systems pose. Amodei told CBS News on Sunday that the thorniest obstacle to such a proposal is uncertainty over whether China would participate. Other prominent tech figures backed the proposal, according to CNBC .
OpenAI CEO Sam Altman said in a Saturday interview that an IPO this year would be "ill-advised," adding to uncertainty around the AI sector's near-term trajectory, according to CNBC.
Nasdaq $NDAQ -100 futures were down 1.5% ahead of the open, with S&P 500 futures off 0.6% and Dow Jones Industrial Average futures shedding 114 points, or 0.2%. Among Asian markets, the Kospi in South Korea retreated 3.26% and Tokyo's Nikkei 225 finished the session down 0.81%. Europe's pan-European Stoxx 600 index was down about 0.3%.
Markets are also contending with rising oil prices. WTI crude futures climbed 3% to trade above $103 a barrel, with Brent futures also rising past $108, following Saudi Arabia's decision to shut a pipeline that had been a critical conduit for crude exports through the Strait of Hormuz region. The closure followed drone strikes by Iran-aligned militants in Iraq, according to The Wall Street Journal .
Last week marked the first time since May that U.S. crude prices climbed past the $100-per-barrel threshold. The surge in crude last week pressed down on all three major indexes, with the Dow surrendering 1.6% for its worst weekly result since March; the S&P 500 and Nasdaq Composite each gave back roughly 0.8% and 0.7%.
Energy stocks were an exception to the broader decline. The U.K.'s FTSE 100 advanced 0.7%, with BP $BP and Shell $SHEL providing the primary boost.
The Federal Reserve opens its September policy meeting this week, with fed funds futures markets assigning about an 86% chance to a rate increase.

### Article 195 · 2026-09-14 · calcalistech.com
Anthropic’s $2 trillion IPO is taking shape as Nvidia considers a $10 billion investment

Anthropic’s $2 trillion IPO is taking shape as Nvidia considers a $10 billion investment
The Claude maker has selected Nasdaq for a potential listing and could seek to raise as much as $100 billion, while its annualized revenue has surged above $65 billion and adjusted operating income is expected to remain positive for a second consecutive quarter.
Anthropic is moving closer to a public offering that could rank among the largest IPOs ever, as the maker of Claude seeks to turn extraordinary growth in AI demand into an equally extraordinary public-market valuation.
The company has selected Nasdaq for a potential listing, according to Business Insider, and is in talks with Nvidia about becoming an anchor investor in the offering, according to people familiar with the discussions cited by Reuters. Nvidia could invest as much as $10 billion, while Anthropic is considering raising as much as $100 billion at a valuation of around $2 trillion.
Those numbers remain preliminary and could change. But even the possibility of an IPO on that scale points to a significant shift in how investors are being asked to value frontier AI companies. Anthropic has moved from a heavily funded private startup to a company with reported annualized revenue of more than $65 billion, while simultaneously committing to spend enormous sums on the computing infrastructure required to keep that growth going.
The company has also told shareholders that its adjusted operating income is expected to remain positive for a second consecutive quarter, according to the Financial Times. Its gross margins are above 80% before accounting for revenue shared with distribution partners such as Amazon and the cost of training its models, the newspaper reported.
That combination of rapidly rising revenue, positive adjusted operating income and very high gross margins could provide an important foundation for the valuation Anthropic is seeking. At the same time, the company’s spending commitments illustrate just how capital intensive the AI business has become.
Anthropic’s annualized revenue run rate surpassed $65 billion by the end of July, according to the company, up from approximately $9 billion at the end of 2025. In May, it raised $65 billion at a post-money valuation of $965 billion. The potential IPO valuation of around $2 trillion would therefore represent another dramatic increase in the company’s value in a matter of months.
The company’s projections for future growth are central to that calculation. Reuters has previously reported that Anthropic is projecting revenue of roughly $190 billion to $200 billion in 2028.
Nvidia’s possible participation would add another layer to the IPO. The chipmaker is already one of the most important companies in Anthropic’s infrastructure ecosystem, and an investment of up to $10 billion would make it an unusually significant financial backer of the public offering.
It would also deepen a relationship that increasingly illustrates the intertwined economics of the AI industry. Model developers need enormous quantities of computing power, while Nvidia benefits from the demand generated by those companies.
Anthropic relies heavily on Nvidia GPUs but is also trying to diversify its sources of computing capacity as demand for Claude has strained its available resources. The company is building relationships with several of the largest technology companies in the industry rather than relying on a single supplier.
In November 2025, Nvidia said it would invest up to $10 billion in Anthropic as part of a broader partnership under which Anthropic committed to purchase $30 billion of Microsoft Azure computing capacity powered by Nvidia chips.
Anthropic also counts Amazon and Google among its backers and major computing suppliers. In April, it said it would commit more than $100 billion over a decade to Amazon Web Services while using more than 1 million of Amazon’s Trainium2 chips. It has also agreed with Google and Broadcom to add multiple gigawatts of TPU capacity.

### Article 196 · 2026-09-14 · finance.yahoo.com
Jim Cramer Tries To Predict NVIDIA Corporation (NASDAQ:NVDA) Share Price Movement Following Anthropic CEO’s Remarks

Jim Cramer Tries To Predict NVIDIA Corporation (NASDAQ:NVDA) Share Price Movement Following Anthropic CEO’s Remarks
AI GPU giant NVIDIA Corporation (NASDAQ: NVDA ) is in fresh spotlight after interesting developments over the weekend saw major AI CEOs unite and call for a slowdown in development. The firm's products are the go-to items for AI data center computing, and Cramer discussed the developments in a tweet:
"Oh, and yes, Dario's comments send Nvidia's stock down four and then it works its way lower and then stabilizes. Yes, it's a buy. But let it come down. The buyback's not big enough. This stuff now happens in what seems like slow motion for me..."
The CNBC TV host's remarks fit into his broader take about NVIDIA Corporation (NASDAQ:NVDA) over the past couple of months. On multiple occasions, Cramer has bemoaned the weak share price and shared movements before markets open. His latest tweet about NVIDIA Corporation (NASDAQ:NVDA) discussed the impact of Anthropic's Dario Amodei's remarks about the need to slow down development on the broader sentiment about the firm.
This sentiment is about the demand for NVIDIA Corporation (NASDAQ:NVDA)'s AI GPUs. They are among the top performers and management continues to share metrics about future demand. For instance, CEO Jensen Huang outlined in March that the firm's estimate of 3.6 million units demanded for the Blackwell GPUs underrepresented the accurate situation. Not to mention, as part of its Q2 release, NVIDIA Corporation (NASDAQ:NVDA) outlined that its order backlog was more than $2 trillion.
Judging Cramer's remarks, it's clear that he's in the bullish camp for the firm and believes that even if the stock does waver following Amodei's remarks, the movement should be temporary. The AI boom continues to benefit NVIDIA Corporation (NASDAQ:NVDA) as the firm grew its revenue by 106% annually during the second quarter. The impact of AI was clear as well, with the data center business accounting for $83.7 billion out of the $96.22 billion of the total revenue.
However, the growth is coming at a time when the global memory market is in a historic shortage. The impact of this shortage was evident on NVIDIA Corporation (NASDAQ:NVDA) as well. While the firm's Q2 gross margins were 75%, the Q3 guide projected a dip to 74% with the Q4 figure estimated to sit between 71% and 72%. Not to mention, the firm's explosive revenue growth continues to reset the base to higher levels, and some, such as those from Seaport Global, have argued that as NVIDIA Corporation (NASDAQ:NVDA) is sold out of capacity, it might find it difficult to generate capacity for additional upside surprises.
Looking at hedge fund sentiment, 285 out of 1,006 funds covered by Insider Monkey had held a stake in NVIDIA Corporation (NASDAQ:NVDA) in Q2, while the figure was 275 out of 1,022 in Q1. A notable jump came in the form of GQG Partners , which increased its stake substantially to $590 million. Looking at the valuation, the stock trades at a forward P/E ratio of 24, which is lower than AMD's 33 and Intel's 55. Short interest as a percentage of float is lower than the other two.

### Article 197 · 2026-09-14 · newsroom.pinterest.com
Pinterest builds a new foundation for multimodal AI with NVIDIA

Pinterest builds a new foundation for multimodal AI with NVIDIA
Pinterest has built a new AI layer with NVIDIA to support a growing range of products that rely on both images and language, including visual search, content understanding and safety systems.
Built on the NVIDIA accelerated computing platform with NVIDIA Blackwell GPUs , NVIDIA Dynamo and Pinterest’s own visual embeddings, the new foundation gives Pinterest teams a shared way to build and launch multimodal AI products without creating custom infrastructure for each one.
With NVIDIA, Pinterest is turning 80 billion+ monthly searches into high-value signals for AI-powered discovery and shopping, enabling Pinterest Assistant to run 25x more visual context per request. In benchmark testing, Pinterest saw average improvements of about 85x faster response startup and 7.3x faster overall latency when using precomputed visual representations instead of repeatedly processing raw images.
“Building the next generation of AI-powered discovery means investing in infrastructure that can keep up with the scale and complexity of Pinterest,” said Kartik Paramasivam, Chief Architect at Pinterest. “Our collaboration with NVIDIA helps us deliver faster, smarter and more personalized experiences for the hundreds of millions of people who use Pinterest.”
Built for the Pinterest Intelligence and beyond
Pinterest’s foundational system was initially developed to support our intelligence layer, the technology woven throughout the user experience. For multimodal serving, Pinterest Intelligence combines NVIDIA Blackwell GPUs and NVIDIA Dynamo with open-source models and Pinterest-built technology, alongside NVIDIA’s broader AI software stack.
This foundation already supports a broader set of AI use cases across our platform, including ranking, safety, OCR, signal generation and future experiences. As we expand our use of vision-language models (VLMs) for features such as Pinterest Assistant, we need stronger infrastructure to make these experiences faster and more efficient at scale. Our expanded partnership with NVIDIA allows us to do exactly that.
“Pinterest is transforming visual discovery with AI, helping hundreds of millions of people find inspiration through more intelligent and personalized experiences,” said Ujval Kapasi, vice president, AI & HPC Frameworks and Libraries at NVIDIA. “By building its multimodal AI infrastructure on NVIDIA accelerated computing and software, Pinterest can bring the next generation of visual and conversational AI experiences to its users at scale.”
This work builds on nearly five years of collaboration between Pinterest and NVIDIA across over 14,000 NVIDIA GPUs. By standardizing the infrastructure behind multimodal AI, Pinterest is giving teams a shared foundation for building new experiences while improving performance and efficiency behind the scenes.
Instead of a single product launch, the end result is a long-term platform for the next generation of visual and conversational experiences across Pinterest.
For more information on Pinterest’s collaboration with NVIDIA, check out our engineering blog .

### Article 198 · 2026-09-14 · cnbc.com
Samsung backs Nvidia AI chip rival in $230 million funding round as GPU alternatives boom

Dutch startup Euclyd, which is a building a chip for AI inference that seeks to rival Nvidia, has raised $230 million funding round.
Samsung has backed a Dutch AI chipmaker in a $231 million funding round, amid a boom in investment in alternatives to Nvidia's graphic processing units.
Euclyd CEO Bernardo Kastrup told CNBC exclusively that the company's 200-million-euro Series A drew backing from Somerset Capital Partners, the Scaleup Europe Fund managed by EQT and Innovation Industries, which all co-led the round alongside Samsung.
The startup, founded in 2024, is designing an AI chip system, with different architecture to GPUs, for inference , including the processor and memory architecture.
Nvidia became the world's most valuable company after its GPUs, originally designed for gaming, were repurposed for training and using AI models, known as inference.
The company has developed a near monopoly over the market for the highest-end chips, but some hyperscalers, alongside startups, are looking to develop their own processors for AI workloads.
OpenAI announced in August that its first AI chip, the Jalapeño , had "industry-leading speed and efficiency." Google, AWS and Meta are all also developing their own AI chips.
"AI is becoming a foundation of economic growth, scientific discovery and national competitiveness, but its potential will remain constrained unless we fundamentally change the infrastructure beneath it," said Kastrup.
Euclyd's systems have yet to be proven at scale in commercial deployments.
But the company said its silicon systems for foundational models will reduce the energy needs and costs of AI data center infrastructure, which is seeing a funding boom.
The company is targeting two revenue streams: selling hardware and physical rack systems to enterprise customers who want secure self-hosted AI inference, and selling its intellectual property to companies that want to develop their own chips based on pre-existing tech.
"Samsung can help us in more ways than money," said Kastrup. "They are one of the biggest memory manufacturers in the world. They do a lot of engineering, they know a lot about systems, they know the supply chain, they have a huge network."
Euclyd aims to begin rolling out its physical chip systems in 2028, with thousands of enterprise customers being served by 2030, Kastrup told CNBC.

### Article 199 · 2026-09-14 · sdxcentral.com
Nvidia’s networking chief explains what the heck ‘scale-in’ actually means

By Ben Wodecki
Scale-up. Scale-out. Scale-across. Three unique networking domains with definitions largely accepted across the industry: interconnectivity inside the rack, across cabinets, and over distances ranging from campuses to vastly disparate facilities.
There are some exceptions to the rule of three, with some vendors coming up with their own additions to the trifecta. DriveNets, for example, previously talked up the idea of hybrid scaling , where each of the three blurs together. But such alternatives are, for the most part, few and far between.
Nvidia claims to have broken the rule of three twice already in 2026, with Inference Context Management Storage (ICMS) later renamed Context Memory Storage (CMX) . And the newest member of the menagerie is scale-in .
Five names. Five “pillars.” The self-proclaimed “ largest ” and “ fastest-growing ” networking company in the world has then gone beyond evangelizing the classic AI networking trifecta in a bid to pioneer distinct paradigms for its so-called AI factory stack.
It unveiled its latest iteration at Hot Chips, buried at the bottom of a list of announcements in a mess of vagueness and marketing spiel.
Upon first glance, scale-in seems to be pointed directly at north-south traffic: data flow between the compute and surrounding infrastructure services like storage, while the core trifecta is fundamentally about the east-west back-end fabric.
But putting the record straight, Nvidia networking chief Gilad Shainer explained in conversation with SDxCentral that the story isn’t so clear-cut.
“It was true that in previous generations like Hopper and Blackwell, there was a front-end network enabling users to access the servers and we placed BlueField-3 data processing units (DPUs) in every GPU (graphic processing unit) server, and that DPU connects to the access network. And that's it," Shainer said.
That separation collapses with the anticipated Vera Rubin generation, with the next-generation BlueField-4 DPU extending security and orchestration control directly into the scale-out and scale-across fabrics, north-south traffic, connections to central processing units (CPUs), and the fancy new LPX racks , and not simply guarding the access point.
“You cannot call it front-end anymore. … It's not just the access network or management network anymore. It needs to scale-in not just users, it needs to scale-in models. It needs to scale-in storage into the AI factory and run security across the entire AI factory, including supporting confidential computing, managing all the isolations between users across the entire AI factory and security around models and all the stuff around that,” Shainer added.
The initial blog that revealed scale-in networking to the world was accompanied by a more detailed technical post . Where vague marketing was in the former, the latter counters the shaky ground scale-in was framed on.
Nvidia suggests the concept provides up to 1.45-times more storage throughput than off-the-shelf Ethernet. Host CPU overhead is reduced as BlueField-4 accelerates data movement, while Spectrum-X Ethernet provides the AI-optimized Ethernet fabric across the storage path to reduce congestion.
In his sit-down with SDxCentral , Shainer went deeper into the details, contending that a BlueField-3 secured only its own 400 Gb/s access link. The addition of BlueField-4, though, secures traffic across every other network interface card (NIC) it orchestrates to 7.2 Tb/s, which he called an 18-times increase in secured traffic managed – a reach claim, not a raw bandwidth one; the blog does separately list BlueField-4's network bandwidth at two-times its predecessor.
Shainer noted that scale-in was built on a multitude of technologies that form the exact stack enabling this performance.
Shainer explained that Advanced Secure Trusted Resource Architecture ( ASTRA ) is the secret sauce bringing the “huge change” to Vera Rubin. ASTRA was detailed in January as a means to provide out‑of‑band management and policy enforcement across traffic.
For scale-in networking, Shainer said it allows BlueField-4 to orchestrate NICs, enforcing security domains across the entire stack, and ties directly into his view that traditional north–south (front-end) versus east–west (back-end) delineation no longer holds true.
“So we provide the BlueField-4, we provide the technology to connect to everything, we provide the design guidelines on how BlueField-4 connects to all the Connect-X 9s.
"There is all the software that runs on top of that, which is part of DOCA (the DPU software development kit). You have the Spectrum-X infrastructure. So all of those elements, all of that design, this is what we propose to our customers as we're moving to Vera Rubin installations.”
Coordinated roadmap or reactive marketing?
In a way, the emphasis on what’s in a name took place behind the scenes at Nvidia with regard to its fourth networking pillar.
The change from ICMS to CMX was, in Shainer’s opinion, because the original was unwieldy and not descriptive. In his view, CMX, which he routinely referred to as “context scale,“ better describes an infrastructure that scales context storage out of the GPU server for a whole pod.
“It wasn't a great name. It kind of described what it is, but you know, from a naming perspective, it wasn't that great,” Shainer said. “It's renamed to context scale. It's actually better representative of what it does.”
That renaming around the change of perspective as a product evolves, sums up Nvidia’s reactive approach to networking rather than some grandiose plan.
It's also indicative of scale-in networking. As the constant evolution of Nvidia’s networking stack might seem to some like a company churning out announcements to keep the money train rolling, the reality is that the emergence of this completely different beast is driven by the changing ways customers ultimately want to use that stack.
“Four, five years ago, when we introduced Spectrum-X on scale-out. We said, ‘hey, the most important thing for us is limiting jitter. We don't really care about the north-south network; put whatever you want there, buy any switches you want. Put it on the north side. We don't really care. The reason was [that] it was just focused on training. That's the only thing that happened five years ago," Shanier explained.
“Now the world is completely different. In the AI factory today, language processing unit (LPU) racks, CPU racks, storage racks, compute trays, all the security. It’s a dramatic change. … It's no more north-south," Shanier added. "The front-end is no more front-end. It's important what you build there and that's why Spectrum-X has evolved and actually provides what you need on that scale-in infrastructure.”

### Article 200 · 2026-09-14 · gurufocus.com
Elon Musk's 2027 SpaceX plan gives Nvidia a new frontier

Nvidia Corp. ( NVDA , Financials ), the semiconductor company whose GPUs dominate AI computing, could soon have customers running its hardware somewhere very different: space.
Elon Musk said he is highly confident SpaceX will begin launching Nvidia-powered AI computers into orbit in 2027.
The systems would use Nvidia's Vera Rubin NVL72 platform, which combines 72 Rubin GPUs with 36 Vera CPUs and advanced networking hardware.
SpaceX has already said it plans to use Nvidia chips exclusively for its computing infrastructure.
The company is targeting its first orbital-computing satellites next year, with significantly larger deployments expected during 2028.
The idea is to modify the same spacecraft platform used for SpaceX's V3 Starlink satellites.
Instead of communications equipment, those satellites would carry computing hardware and additional solar-generation capacity.
That matters because AI companies are increasingly constrained by power, land and data-center capacity on Earth. SpaceX is betting orbit could eventually provide another place to build compute.
For investors, 2027 will be the first meaningful test. If SpaceX can successfully launch and operate Nvidia-powered computing satellites, Nvidia could gain an entirely new infrastructure market while SpaceX moves closer to turning orbital AI from an engineering experiment into a commercial business.

### Article 201 · 2026-09-14 · gurufocus.com
Palantir and Nvidia rethink AI use over a growing data risk

Palantir Technologies Inc. ( PLTR , Financials ), the software company known for handling sensitive government and enterprise data, is reportedly putting tougher limits on how some advanced AI models can be used.
Palantir, Nvidia and Booz Allen Hamilton could restrict or stop using models from Anthropic and OpenAI unless the companies provide stronger guarantees around customer data and intellectual property, Reuters reported, citing The Information.
Palantir has pushed Anthropic for irrevocable zero-data-retention guarantees before making its models available through Palantir software.
Nvidia is taking a different approach. The chipmaker reportedly limits Anthropic models to less sensitive work and uses its own Nemotron models for some internal tasks.
Booz Allen has also barred employees from using Anthropic's commercial model for proprietary cybersecurity work. The concerns come as AI labs face more scrutiny over how usage logs and customer information are stored.
Microsoft may have an opening. The company is reportedly pitching isolated cloud environments and its own AI products to customers worried about data exposure.
For investors, this adds a new layer to the AI race. The winners may not simply have the strongest models. They may also be the companies customers trust with their most sensitive information.

### Article 202 · 2026-09-14 · qz.com
Hyundai delays in-house driver-assist software, partners with Nvidia

The South Korean automaker will deploy Nvidia-powered Level 2+ and Level 2++ systems in 2028 while its proprietary Atria platform is pushed back two years
Hyundai Motor Group has pushed its proprietary driver-assistance software debut to late 2029, a two-year delay from its previous schedule, according to Reuters . The automaker will rely on a partnership with Nvidia $NVDA in the interim, deploying the chipmaker's driver-assistance technology in 2028.
Hyundai will integrate Nvidia 's Hyperion 10 computing platform to roll out Level 2+ systems in the first half of 2028 and Level 2++ systems in the second half of that year, the company announced . Vehicles equipped with Hyundai's proprietary Atria AI software are targeted for the second half of 2029. The Nvidia -based systems will initially use cameras, ultrasonic sensors, and radar rather than lidar, according to Reuters.
Hyundai Motor Group president Minwoo Park, who previously worked at Nvidia before joining Hyundai in January, said the arrangement is not a full handover of the company's autonomous driving direction. "Our partnership with Nvidia is not about leaving our destiny entirely in their hands," Park Min-woo told Reuters. He said Hyundai will co-design the technology with Nvidia and use data generated by those systems to train its own Atria platform.
Park said Hyundai made a deliberate choice to deprioritize near-term in-house deployment in order to direct engineering effort toward more distant objectives, according to Reuters. That stance represents a departure from the philosophy of Song Chang-hyeon, the executive he replaced, who had made in-house software development the central priority before leaving the company in December.
Hyundai and affiliate Kia Corp together move more than 7 million vehicles a year, and the group is counting on that global footprint to generate the real-world driving data required to develop its autonomous technology. Hyundai anticipates overtaking rivals in total accumulated driving data by 2033.
The company outlined the strategy at its "HMG Autonomous Driving Media Day" event at the headquarters of 42dot, its autonomous driving subsidiary, in Gyeonggi Province, South Korea. At the event, Hyundai demonstrated footage of an Atria AI-equipped test vehicle navigating Seoul urban traffic without driver intervention at a Level 2++ capability.
The company also disclosed plans for a real-world Level 4 autonomous driving pilot in Gwangju, South Korea, by year-end, conducted in partnership with South Korea's Ministry of Land, Infrastructure and Transport. Hyundai said data collected during that deployment will feed back into its AI training system.
Hyundai's broader collaboration with Nvidia extends beyond vehicles to AI data centers and humanoid robots developed by Boston Dynamics, which Hyundai owns. Hyundai's South Korean union staged a full-day strike last month , with workers seeking written protections against job losses tied to the company's AI and robotics expansion, including plans to deploy Boston Dynamics' Atlas robot at its Georgia facility beginning in 2028.

### Article 203 · 2026-09-14 · fool.com
Broadcom vs. Nvidia: 3 Key Metrics Point to the Stronger AI Chipmaker to Buy After Earnings

Nvidia (NASDAQ: NVDA) and Broadcom , two of the largest chipmakers in the world, have now both reported earnings for their most recent quarters, which ended at the end of July for Nvidia, and in early August for Broadcom.
Both put up strong results as well. Nvidia's adjusted revenue grew 106% year over year, while diluted earnings per share (EPS) rocketed 120%. Meanwhile, Broadcom had adjusted net revenue growth of 86% and adjusted diluted EPS growth of 96%.
Both companies also topped Wall Street average estimates as well.
Although there is an investment case to be made for Nvidia and Broadcom, three key metrics point to the stronger AI chip stock following their respective earnings reports.
1. Nvidia and Broadcom both stunned with guidance
One of the first metrics in earnings reports that Wall Street analysts and investors look at is forward financial guidance , which both Nvidia and Broadcom provide to some extent. Specifically, they are looking to see how company forecasts compare to Wall Street estimates.
Broadcom projected revenue of $34.8 billion in its current quarter, slightly below analyst estimates of $35.03 billion.
However, on its earnings call, Chief Executive Officer Hock Tan said it believes its AI semiconductor revenue is set to double in 2027 to $115 billion and then double again in 2028 to $230 billion, with 2028 guidance coming in $50 billion ahead of analyst estimates.
While that's quite impressive, it will likely be difficult for analysts to get comfortable with the 2028 outlook just yet.
Nvidia, as it typically does, also knocked it out of the park with its guidance. The company forecast revenue of $108 billion in the current quarter, roughly $2.5 billion above estimates.
The company also projected 70% annual revenue growth in fiscal year 2028, with most of that occurring in calendar year 2027, while analysts had only estimated 44%. Not only did that beat forecasts, but it's also incredible growth given the company's $5 trillion-plus market cap.
2. Gross margins
Another metric investors closely watch for both Nvidia and Broadcom is gross margin , the percentage of revenue remaining after accounting for the cost of goods sold, which includes labor, materials, and overhead.
Gross margin shows how much a company makes from each sale before paying for other business costs, such as fixed costs, debt, or taxes. Gross margin is also representative of pricing power.
In its second quarter of fiscal 2027, Nvidia continued to boast gross margins of roughly 75%. However, this figure is expected to slip, with Nvidia predicting a 74% gross margin in the current quarter, followed by further contraction as the fiscal year progresses.
In fact, Nvidia expects its gross margins to narrow to the 71% to 72% range, the point at which management expects gross margins to inflect higher. Management attributed the margin contraction to higher memory costs.
In its most recent quarter, Broadcom had a consolidated gross margin of 75%. Management anticipates the current quarter gross margin will slip to 73%, as the company sells more of its custom chips, which are more memory-intensive.
However, Broadcom's management team has told analysts not to focus on gross margin, as it believes operating margin better reflects its business.
Ultimately, I still find Nvidia to be the more attractive play here. Sure, its growth may not be as fast, but it's still calling for 70% revenue growth at a market cap roughly three times Broadcom's. Nvidia generated $89 billion in AI chip revenue last quarter, compared with Broadcom's nearly $21 billion.
Investors have never seen growth like this at a company with Nvidia's scale. I also think Nvidia's fast-growing central processing unit (CPU) business is something for investors to be excited about.

### Article 204 · 2026-09-14 · thequantuminsider.com
NVIDIA Expands Open Source CUDA-Q Platform

NVIDIA Expands Open Source CUDA-Q Platform
NVIDIA introduced CUDA-Q Logical, an open-source orchestration layer for designing and testing applications for fault-tolerant quantum computers.
Iceberg Quantum used the platform to model 1,000 logical qubits with 150,000 physical qubits, about 10 times fewer than Diraq ’s previous estimate.
Fermilab cut the time needed to evaluate fault-tolerant system designs from about five months to three weeks, while Sandia made its QUOPS benchmarking tool available through CUDA-Q.
PRESS RELEASE — NVIDIA today announced an expansion of the NVIDIA CUDA-Q™ open source platform with CUDA-Q Logical, an orchestration layer that provides a programmable, verifiable approach to developing useful applications for fault-tolerant quantum computers.
Fault-tolerant quantum processors with logical qubits are essential for useful quantum computing, allowing systems to overcome the errors inherent in physical qubits so they can execute the larger computations needed for practical applications such as drug discovery, financial modeling and materials development.
However, developing applications for such systems is a tedious, time-consuming codesign challenge: A change to an algorithm, error-correction code, hardware architecture or other QPU component can significantly change the resources needed to run any given application.
With CUDA-Q Logical, researchers can now design and orchestrate the many components required for fault-tolerant quantum computing applications, easily switching between options to identify optimal system configurations for performance with logical qubits.
“Quantum computing is maturing into an era of logical qubits, and researchers need an open, customizable platform capable of representing all aspects of a fault-tolerant system,” said Timothy Costa, vice president and general manager of quantum at NVIDIA . “The addition of CUDA-Q Logical provides power and flexibility to explore fully integrated, co-optimized systems regardless of qubit type and architecture — drastically shortening the timeline to useful quantum-GPU supercomputing.”
CUDA-Q Logical is already being used by QPU makers and labs including Fermi National Accelerator Laboratory, Infleqtion, IQM Quantum Computers, QCDesign Quantum Motion and Sandia National Laboratories.
Using CUDA-Q Logical, Iceberg Quantum modeled its fault-tolerant architecture for Diraq ’s qubits, showing how 1,000 logical qubits can be created with just 150,000 physical qubits, roughly 10x fewer than Diraq’s previous estimates. CUDA-Q Logical gave an unprecedented way to rapidly assess potential implementations of Iceberg’s architecture, helping dramatically reduce the hardware needed for useful, fault-tolerant quantum computing.
Fermilab Uses CUDA-Q Logical to Explore Fault-Tolerant Applications
In early work, Fermilab researchers used CUDA-Q Logical to validate prior results and evaluate physical qubits, runtimes and other resource requirements across different error-correction approaches and quantum hardware.
Fermilab transformed complicated fault-tolerant system designs into a repeatable and verifiable computational workflow, accelerating fault-tolerant algorithm development from five months to three weeks, a 7x speedup.
“Fault-tolerant quantum computing is the path to unlocking new scientific discovery, but getting there will require researchers to codesign algorithm, error correction, architectures and hardware together,” said Anna Grassellino, chief technology officer at Fermilab and director of the Superconducting Quantum Materials and Systems Center. “Using CUDA-Q Logical, our team explored combinations of these resources in just three weeks, compared with what would have typically taken about five months of building specialized infrastructure.”
Sandia Creates Benchmark for Future of Quantum Computing
QUOPS is a new, independent cross-platform benchmark developed by Sandia National Laboratories that measures the progress quantum computing systems are making toward utility-scale applications.
With Sandia ’s QUOPS, the industry now has access to a hardware-agnostic, open method to benchmark progress toward shared goals for fault-tolerant quantum computers. Historically, progress in quantum computing has been measured primarily through advances in physical qubits — increasing qubit counts, improving fidelity and extending coherence.
“At Sandia , we can’t wait to see fault-tolerant quantum computers helping to solve problems of national importance for the Department of Energy and the United States,” said Timothy Proctor, co-director of Sandia National Laboratories’ Quantum Performance Laboratory. “Our mission right now is to bring that about sooner, by accelerating our industry partners’ progress. To do that, we, and other quantum computing stakeholders, have to be able to track and forecast the growth of quantum computer abilities. We created QUOPS to do exactly that, and we’re excited to see it used by quantum computing vendors and customers.”
Sandia shared early results in a preprint posted ahead of IEEE Quantum Week, reporting initial QUOPS benchmarks for QPUs from Google, IBM and Quantinuum. A QUOPS reference implementation is available in NVIDIA CUDA-Q.
Expanding the Quantum-GPU Supercomputing Platform
The ecosystem is also adopting NVIDIA ’s larger lineup of quantum computing technologies for turning qubits into useful quantum-GPU supercomputers.
Diraq used NVIDIA Ising, the world’s first family of open models for building and deploying AI for useful quantum computing, to calibrate its silicon-based qubit processor.
Companies are integrating their quantum processors with GPU supercomputing using NVIDIA NVQLink™, the open system architecture for tightly coupling quantum processors with GPU supercomputers. With NVQLink:
Anyon Computing developed a new quantum control system.
Quandela developed a QPU-GPU architecture.
Quantum Machines ran a demo of integrating state-of-the-art supercomputing resources with qubits at the Israeli Quantum Computing Center.
The NVIDIA CUDA-Q open development platform continues to be adopted across the quantum computing ecosystem:
BlueQubit launched the Quantum Flywheel grant program for researchers, to give them access to NVIDIA accelerated computing through CUDA-Q. ● Qedma Quantum Computing and QCentroid each integrated their technology with CUDA-Q to support quantum error correction and mitigation, as well as the deployment of quantum applications.
The quantum ecosystem is also working with NVIDIA to develop new and improved quantum applications:
IonQ announced progress on DQAOA-GPT, a quantum generative AI framework, using NVIDIA accelerated computing.
MITRE published work on building GPU-accelerated digital twins of quantum sensors.
Phasecraft is using NVIDIA cuQuantum to generate the largest-known variational quantum eigensolver emulated molecular database.
UCLA and Caltech are advancing the design of control sequences needed to run quantum applications.
CUDA-Q Logical is now available through GitHub. Explore the QUOPS repository. Learn more by reading these papers on CUDA-Q Logical and QUOPS .
Iceberg Quantum specializes in designing next-generation fault-tolerant quantum computing architectures, focusing on reducing the hardware overhead for quantum error correction. It develops innovative architectures based on quantum low-density parity-check (qLDPC) codes to address the scalability challenges of quantum error correction. It emphasizes dramatically lower qubit overhead compared to traditional surface-code approaches, working with leading quantum hardware companies to accelerate the transition to useful fault-tolerant quantum computing.
Diraq is a full stack quantum company which is building a quantum computer using silicon CMOS-based spin qubits.
Fermilab QI is focusing on: using technology developed for superconducting particle accelerators to vastly improve qubit systems, including those used for future quantum computers; Developing ways to convey information across large distances with entangled particles ; Improving quantum sensors for many applications and deploying them to potentially detect dark matter and give us new insights into the universe ; Writing algorithms that can simulate subatomic interactions on quantum computers, with many other uses outside of physics ; Developing methods to use quantum computing to improve data analysis and theoretical calculations.
The Sandia National Laboratories is one of three National Nuclear Security Administration research and development laboratories in the United States, managed and operated by the National Technology and Engineering Solutions of Sandia.
NSEC delivers research, engineering, and analytical solutions to the Department of Defense and the Intelligence Community. Since 1958, NSEC has contributed transformational innovations to essential systems such as the Semi-Automated Ground Environment (SAGE), the nation’s first air-defense system. These include Joint STARS, the Air Force/Army airborne ground surveillance, battle management, command and control aircraft, and Intelink, the first secure intranet used by the Intelligence Community.
A team of physicists led by MITRE’s Gerry Gilbert, a theoretical physicist and quantum expert, are working on a quantum moonshot: a mission to build a scalable universal quantum computer.
Atom Computing builds quantum computers using nuclear spin qubits formed from arrays of optically-trapped neutral atoms.
Quandela is a French startup that specializes in photonic quantum computing by providing modular, scalable, and energy-efficient photonic quantum computers, accessible both on the cloud and on premise. They provide prototyping services with their Perceval simulator alongside their general purpose chips optimized chips, and development of algorithms and protocols which provide photonic solutions for applications ranging from pharmaceutical and material design, to quantum machine learning, networking and optimization.
Quantum Machines develops operational and control systems (both hardware and software) for quantum computers.
BlueQubit specializes in quantum computing software, providing a cloud-based platform that enables enterprises, defense, and academic users to run advanced quantum algorithms on leading QPUs such as IBM Heron and Quantinuum H2. The company focuses on making quantum computing accessible for research and industry applications in finance, AI, and optimization. BlueQubit offers high-performance quantum simulators, SDK integration, and seamless migration from other quantum frameworks, supporting rapid prototyping and benchmarking. Its solutions address real-world challenges such as risk analysis, derivative pricing, and combinatorial optimization, emphasizing ease of use and practical value for early adopters.
IonQ is a developer in trapped ion quantum computing founded in 2015 that actively applies its technology to the aerospace and defense sectors. The company empowers satellite-based quantum networks and quantum enabled drones to improve positioning, navigation, and timing resilience in GPS denied environments, and collaborates with industry leaders like Airbus to optimize aircraft loading.
Phasecraft is developing the fundamental quantum theory and software that will enable quantum computers to be useful.
The University of California, Los Angeles, commonly referred to as UCLA, is a public research university located in Los Angeles, California. Its origins date back to 1881 when it started as a normal school called the southern branch of the California State Normal School. It later became part of the University of California system in 1919 and was officially established as UCLA, making it the second-oldest campus among the ten in the University of California system.
The California Institute of Technology, situated in Pasadena, California, is a private research university. It has played a crucial role in numerous contemporary scientific breakthroughs and stands alongside a select few technology institutes in the United States that prioritize teaching in pure and applied sciences.

### Article 205 · 2026-09-14 · businessinsider.com
Tech stocks are tumbling as AI apocalypse fears go mainstream

By Georgia Hennessy
AI-linked stocks sold off in premarket trading on Monday after tech leaders called for a slower approach to developing powerful artificial intelligence.
Tech stocks opened sharply lower Monday after a weekend of increasingly dire warnings about AI .
Nvidia extended its premarket slide at Monday's open, trading down 4% shortly after 9:30 a.m. ET, with SpaceX also down 1.9%. The wider Nasdaq was down over 1% at the open.
The weakness followed a weekend in which Anthropic CEO Dario Amodei urged AI companies to slow the "reckless" pace of development, warning that increasingly capable AI agents could eventually cause severe economic damage.
The call gained backing from some of the industry's biggest names . OpenAI CEO Sam Altman, Google DeepMind CEO Demis Hassabis, and SpaceX boss Elon Musk all supported Amodei's proposal to pace frontier AI development.
Altman said OpenAI would match Anthropic's commitment to embed outside evaluators in the company to assess its safety practices.
Read more about the AI apocalypse debate
Investor concerns were also sharpened by Jacob Coxon, a former researcher at OpenAI and Anthropic who resigned last week , saying the rival labs were "gambling with our lives" in their race to build self-improving AI.
The market reaction was particularly severe in Asia, where chipmakers and AI-infrastructure suppliers have been major beneficiaries of the AI boom.
SoftBank, one of OpenAI's largest backers, fell 14%. South Korea's volatile and tech-dominated Kospi index fell 3%, while Taiwan Semiconductor Manufacturing shares dropped 3.2%.
Memory-chip names were among the biggest losers at market open. SanDisk, Intel, and Micron all fell around 6%.
The downturn comes amid broader concern among investors and analysts that the AI rally has pushed some valuations ahead of the profits the technology has generated so far.
Those questions loom large for Anthropic as it prepares for a potential US listing this year . The company is reportedly on track to post adjusted operating profit for a second consecutive quarter.
Georgia is a Business News Fellow at Business Insider's London office. Before joining Business Insider, she worked at Japan's largest newspaper, The Yomiuri Shimbun, and interned at the Financial Times. She is an NCTJ-qualified journalist with a degree in Philosophy from the University of Birmingham.

### Article 206 · 2026-09-14 · ign.com
'It's Definitely at the Top of Our List' – SteamOS Is Getting Closer to Nvidia Driver Support

By Jacqueline Thomas
One of the biggest goal's of Valve's latest wave of hardware wasn't necessarily to move as many units as possible, but to expand the reach of SteamOS , and it does seem like it's succeeded. There are now two things that are really standing in Valve's way in its quest to dethrone Windows 11 as the de facto gaming OS: anti-cheat and Nvidia graphics drivers. And it looks like the latter is going to be solved soon.
Ahead of Steam Frame's launch, I got a chance to sit down with Valve software developers Pierre-Loup Griffais and Jeff Leinbaugh , and I asked how Nvidia support was coming along.
"Yeah, we're working on it hard," Griffais told me. "It's definitely at the top of our list. It's one of those things just like FEX and working on the Qualcomm driver, it just takes years." That doesn't sound like the driver support is right around the corner, but it does seem like the team has at least got Nvidia GPUs working on the Linux OS, albeit with limited performance.
"We've done a few things like we've enabled the driver now in the main tree of SteamOS," Griffais told me, "so you can get things to light up on certain generations, but in terms of the performance difference between that driver and where the state of the art is, there's definitely still a little bit of a rift that we're trying to work on, but it's getting better day-to-day."
There are certainly versions of Linux that already work with Nvidia drivers, but Team Green's GPUs are always a bit of a hassle on the open-source operating system. Instead, for most people, gaming on Linux works best with AMD graphics cards , as that company has supported drivers on the operating system for years.
But for Valve's goal of getting as many people on SteamOS as possible, getting Nvidia's cards working at full performance is incredibly important. According to the latest Steam Hardware Survey , Nvidia GPUs still make up for 72.88% of Steam's player base. Getting Nvidia graphics cards up and running reliably on SteamOS would be a huge win for Valve.
Hopefully Valve is able to get these graphics cards working as intended on SteamOS soon, and then, maybe, we can finally get anti-cheat support on the operating system. Because, after all, unlocking the operating system for another 72% of the playerbase could cause a huge spike in players migrating from Windows, and that'd be hard to ignore for the Call of Dutys of the world.

### Article 207 · 2026-09-14 · gurufocus.com
Nvidia Falls 3.5% While Quantum Software Claims a Sevenfold Research Speedup

Nvidia ( NASDAQ:NVDA ), the AI-chip and computing-platform giant, unveiled new quantum-development software Monday, but the announcement offered little shelter from the AI selloff. Shares traded around $210.87, down approximately 3.5%. Reuters reported that calls from industry leaders to slow AI development weighed on Nvidia and other chipmakers.
The headline number: five months of research work compressed into three weeks. Nvidia said Fermilab achieved that improvement in an architecture-development workflow, describing a sevenfold acceleration. Its new open-source CUDA-Q Logical layer supports the development of fault-tolerant quantum applications. The distinction matters: researchers completed a design workflow faster. That does not establish faster quantum hardware, commercial viability or additional sales.
For shareholders, the potential payoff comes from supplying the computing resources behind quantum research. Wider use of Nvidia's software could translate into more demand for its accelerated-computing infrastructure, although that commercial outcome remains unproven. The GuruFocus chart shows a GF Score of 95/100, with profitability and growth standing out while the weaker GF Value reading puts valuation under greater scrutiny. Strong fundamentals give investors something concrete to assess; quantum still needs to demonstrate sustained usage and paying demand.

### Article 208 · 2026-09-14 · nbcnews.com
Trump calls Nvidia CEO to talk AI — and gets put on speakerphone during industry summit

“Data centers are great, and they make people wealthy,” the president told CEO Jensen Huang, whose company makes AI chips and hardware.
By Raquel Coronell Uribe
President Donald Trump on Monday called Nvidia CEO Jensen Huang during an industry summit and gave another full-throated defense of artificial intelligence after Huang put the call on speakerphone.
Trump characterized concerns about AI safety as a “hoax,” while telling Huang in the middle of the All-In Summit that the U.S. had to beat China in AI innovation and development.
“The robots will not be taking over. The AI will not be taking over the rest of the world. The whole thing is a hoax,” Trump said, suggesting that critics are “just playing right into the hands of a lot of people that don’t want to see it happen. That could be political people, that could also be China.”
Trump also lauded politically unpopular data centers , calling them “great” and saying they make people and states “wealthy.”
“It’s the oil of the next 20, 25 years, it’s bigger than the internet and AI, you know, much more so,” he said, while adding that people “have to be a little careful” and do things “prudently.”
A video of Trump’s call, posted on X , was reposted by the Trump War Room account, which is associated with a Trump-aligned PAC. The call is also included in a podcast that Huang was recording at the time.
Nvidia said it had no comment on Huang’s exchange with Trump or whether they will be meeting soon to discuss these issues.
Trump’s comments to Nvidia, one of the world’s biggest manufacturers of AI chips and hardware, come as AI leaders have called for slowing down development of the technology.
Anthropic CEO Dario Amodei wrote in an essay over the weekend that AI development needed safeguards, which was quickly endorsed by Tesla CEO Elon Musk and OpenAI CEO Sam Altman, among others. It came after researchers at leading AI companies stepped down from their jobs last week and spoke out over safety concerns, some describing them as an existential threat to humanity.
Former President Barack Obama urged Democrats last week to prioritize the development of an AI agenda.
Trump, however, has firmly stood by his support for AI development. In a flurry of social media posts Monday , Trump described AI concerns as a “SICK conspiracy” and a “hoax.”
During the Nvidia phone call, Trump said he assumed Huang was on the same page as him regarding AI development; Huang said they were.
“We’re going to make sure that everybody wins in the AI race in America. Every industry, every company, every state, every people,” he told Trump during their call.
The Nvidia CEO, who helped persuade Trump last year to not send National Guard troops to San Francisco, sits on Trump’s council of science and technology advisers. He has lobbied lawmakers to allow sales of Nvidia around the world, which lawmakers have said could advantage China and undercut U.S. leadership in technology.
His conversation with Trump came as House Speaker Mike Johnson, R-La., who had been urged by House Democrats to end recess early so the lower chamber could take legislative action regarding AI safety, said this week that industry leaders should be the ones taking the lead on safety.
Johnson said Monday that Trump would call a meeting with AI leaders. A source familiar with the matter told NBC News that a meeting between Trump and the leaders was “in the works,” but no clear timing had been nailed down.
CORRECTION (Sept. 14, 2026, 10:39 p.m. ET): A previous version of this article and its headline misstated the event where Trump spoke by phone to Nvidia’s CEO. It was during the All-In Summit, not during an all-hands meeting at Nvidia.

### Article 209 · 2026-09-14 · quantumcomputingreport.com
Sandia, Quantinuum, and NVIDIA Introduce QUOPS Framework to Benchmark Physical and Logical Quantum Performance

A research collaboration led by Sandia National Laboratories , in partnership with Quantinuum and NVIDIA , has introduced the Quantum Universal Operations Performance System (QUOPS) . Detailed in a multi-institution paper published on arXiv (arXiv:2609.12146) and released across public software repositories, QUOPS is an architecture-agnostic benchmarking framework designed to measure integrated quantum computer performance across both physical- and logical-qubit platforms, addressing limits in traditional component-level metrics such as raw qubit count or isolated gate fidelities.
QUOPS evaluates full system execution—incorporating compilation, error correction, syndrome decoding, and error mitigation—by executing randomized layers of arbitrary-angle single-qubit rotations, RP(θ) , and CNOT gates across varying circuit widths ( w ) and depths. The benchmark yields two top-level system metrics: Q (QUOPS score), which defines the maximum circuit size s = 2 × w × depth successfully executed within a utility-motivated geometric volume ( w ² ≤ s ≤ w ³) at a minimum mean process polarization threshold of 1/√e ≈ 61%; and Ω (QUOPS rate), which measures the net operational throughput in executed operations per second while accounting for sampling overheads from error mitigation or postselection.
[ Experimental Cross-Platform QUOPS Performance Benchmarks ]
QUOPS Score ( Q ) & Throughput (Ω)
• Physical Transmon (105 Qubits, 2D Grid)
• Q = 216 | Ω = 2.0 × 10⁷ QUOPS/s (Width w =6)
• Physical Transmon (156 Qubits, Heavy-Hex)
• Q = 204 | Ω = 3.1 × 10⁵ QUOPS/s (Width w =6)
• Physical Trapped-Ion (56 Qubits, QCCD)
• Q = 1,320 (1,392 w/ PS) | Ω = 353 QUOPS/s (Width w =12)
• Physical Trapped-Ion (98 Qubits, QCCD)
• Q = 1,504 (1,824 w/ PS) | Ω = 303 QUOPS/s (Width w =16)
Quantinuum Helios-1 (FTQC)
• Logical Steane [[7,1,3]] Code (8 Logical Qubits)
The publication provides direct cross-platform baseline measurements across leading hardware: Quantinuum’s Helios-1 achieved a physical score of Q = 1,504 (1,824 under leakage postselection), Google’s Willow achieved Q = 216 at 2.0 × 10⁷ QUOPS/s, and IBM’s ibm_boston reached Q = 204 at 3.1 × 10⁵ QUOPS/s. Additionally, the team executed QUOPS on a fully fault-tolerant logical architecture using up to 8 Steane-encoded [[7,1,3]] logical qubits on Helios-1, demonstrating logical Clifford+ T circuit execution with active magic-state injection and syndrome extraction to achieve Q = 40 at Ω = 4.9 QUOPS/s.
Developed to align with federal procurement objectives—including the U.S. Department of Energy’s (DOE) Quantum Computer for Application Development and Discovery Science (QC ADDS) initiative—the framework has been integrated natively across open-source toolchains, including NVIDIA CUDA-Q, Quantinuum Guppy, TKET (pytket), and Sandia’s pyGSTi. By mapping resource requirements for canonical utility challenge problems into effective QUOPS circuit sizes—estimating targets of 270M to 370M QUOPS ( Q ≈ 2.5 × 10⁸ for factoring RSA-2048 and Q ≈ 3.4 × 10⁸ for FeMoco energy eigenvalue calculations)—the framework quantifies the 5-order-of-magnitude gap remaining between contemporary hardware and utility-scale application requirements, establishing a standardized metric for government procurement, hardware roadmaps, and fault-tolerant architectural verification.
Review the technical update via Sandia National Laboratories here , access the industry announcement on Quantinuum here , examine the peer-reviewed preprint on arXiv here , and inspect open-source benchmark implementations on GitHub here .

### Article 210 · 2026-09-14 · qz.com
Trump called Nvidia's Jensen Huang live onstage to call AI safety concerns 'a hoax'

The Nvidia CEO answered a call from the president while he was onstage at a summit. Put on speakerphone for the crowd, Trump called data centers "the oil of the next 20, 25 years"
President Donald Trump phoned Nvidia $NVDA CEO Jensen Huang while Huang was speaking onstage at the All-In Summit in Los Angeles on Monday, using the live call to dismiss concerns about artificial intelligence safety as "a hoax." The call, which lasted around five minutes with Trump on speakerphone, was captured on video by an attendee and circulated widely on social media.
"The robots are not going to be taking over the world. That's not going to happen," Trump said. "The data centers are great, and they make people wealthy, and they make states wealthy." Trump called data centers "the oil of the next 20, 25 years" and told Huang, "I'm with you all the way."
Trump also linked opposition to data centers and AI development to foreign adversaries. "They're just playing right into the hands of a lot of people that don't want to see it happen," he said. "That could be political people, and also China." Huang answered: "You're right. We're not going to let that happen, sir."
The call came after Anthropic CEO Dario Amodei published an essay Saturday calling on AI companies to slow the pace of AI development, warning that recursive self-improvement and a recent AI agent incident had made the risks too serious to ignore. OpenAI CEO Sam Altman and SpaceX's Elon Musk each signaled agreement with the call to slow AI development over the weekend.
Huang, who leads the world's most valuable company after years of surging demand for AI chips, challenged the empirical basis of the safety warnings. "Whistle-blowing is fine," he said, according to The New York Times . "The scientific prediction about the future is less fine because it's not grounded in science, obviously." He noted that companies like Anthropic and OpenAI were free to reduce their own pace whenever they decided to act on their concerns.
Earlier Monday, Trump had posted repeatedly on Truth Social attacking Amodei by name , calling AI safety concerns "a hoax" and "a scam" and writing that the only guardrails AI needed were "a STRONG AND SMART (High IQ!) PRESIDENT." He also described opposition to AI and data centers as "a SICK conspiracy" that benefits China. On the question of regulation, Trump said he saw no need for additional oversight. "We have to do things, and we have to do them prudently," he said during the call, according to the Times, "but that doesn't mean we're going to stop an industry."
After the session wrapped, All-In Summit co-host Chamath Palihapitiya took to X $TWTR with a one-sentence verdict: "This was surreal."

### Article 211 · 2026-09-15 · NVIDIA Corporation
Children’s Hospital Uses Open Source NVIDIA AI for Cardiac Care | NVIDIA Blog

Children’s Hospital of Philadelphia is using open source AI tools to model children’s hearts in seconds — with the goal of enabling safer, more precise care for kids with congenital heart disease.
A child born with a hole between the lower chambers of their heart, or a leaking valve in the single pumping chamber keeping them alive, needs care that fits their exact anatomy. Historically, the devices surgeons reach for were almost never designed with that specific child in mind.
“You’ve got a one-of-a-kind kid and an off-the-shelf device,” said Dr. Matthew Jolley, a cardiologist and researcher at Children’s Hospital of Philadelphia, or CHOP. “Our job is to find what fits — and modeling lets us do that before anyone goes into the cath lab or operating room.”
CHOP’s cardiac modeling service, built on MONAI — an open source medical imaging framework cofounded by NVIDIA — takes the images a child’s care team already has, such as CT scans, MRI and 3D ultrasound, and produces anatomically precise heart models in just seconds. A workflow that once required four hours of work by a skilled researcher now completes fast enough for routine clinical use.
More than 20 children’s hospitals across the U.S. now run cardiac modeling programs. At Boston Children’s Hospital, modeling supports more than half of all cardiac surgeries — roughly 500 cases a year. CHOP expects to reach about 200 modeled cases this year. Where this work began in cardiac care, CHOP is now aiming to apply the same tools across multiple disciplines through the IDEA Lab , part of the hospital’s Morgan Center for Research and Innovation.
When Jolley joined CHOP in 2015, 3D echocardiography was just coming online. There were tools for modeling adult valves, but almost nothing built for the complex, small anatomies he was treating.
His lab worked with the open source community to build SlicerHeart — an extension of 3D Slicer open source software for visualizing, segmenting and analyzing 3D medical images — and began developing workflows to model pediatric hearts and valves from multiple imaging modalities.
For years, producing a single model meant a skilled research assistant spending hours at a workstation. Machine learning changed that.
Using MONAI Label and NVIDIA’s Auto3DSeg implementation, Jolley’s team trained segmentation networks on pairs of prior images and models. The output meets the same quality standard a trained human would produce — in seconds rather than hours.
“Machine learning has become just bread and butter,” Jolley said. “As soon as we’ve made 10 or 20 image-model pairs, we train a model and start applying it.”
Using MONAI, CHOP can compare how two different artificial valves will fit in a patient’s heart to improve surgery planning. Coloring shows the stress on the cardiac walls created by the two different valves.
The clinical impact was seen quickly. For complex ventricular septal defects — holes between the heart’s lower chambers — CHOP now models routinely before surgery.
One early case made the value clear: A child had already undergone two failed repair attempts, with surgeons unable to locate the defect with traditional methods. The 3D model clarified the anatomy. The repair succeeded on the first try.
Visualization alone isn’t the end goal. Jolley’s team wants to know not just what a child’s heart looks like, but what will happen when a device is deployed inside it — before any procedure begins. That’s where Newton comes in.
Newton is an open source physics engine built on the NVIDIA Warp Python framework that runs physics simulations on GPUs. CHOP is working with NVIDIA and the open source community to build biomechanics-focused simulation frameworks with Warp that can be brought into Newton, originally intended for simulation-based AI robot training.
These frameworks, once integrated with 3D Slicer and SlicerHeart, can help doctors understand tissue material properties that determine how a device will deploy in a given patient. With GPU acceleration, they can reduce the time needed for cardiac device simulation from up to four hours — or a full overnight run for multiple configurations — to near real time.
CHOP has started implementing features built on NVIDIA Warp and Newton to understand how a device will work in a patient’s heart.
In practice, a clinician could compare how different devices fit a child’s specific anatomy and get results fast enough to inform a same-day decision.
CHOP has begun to implement features built on Warp and Newton for the closure devices used to seal holes in children’s hearts — and hopes to apply similar methods for simulations of transcatheter valves. The open source architecture of Warp and Newton is being connected with SlicerHeart, with the long-term goal of bringing real-time simulations into clinical workflows.
A coupler using SlicerHeart and NVIDIA Omniverse digital twins, powered by OpenUSD, is also in development. OpenUSD’s open source 3D interoperability allows diverse data and solvers to be integrated into simulations built from patient images. These simulations can then flow into virtual reality environments and harness embedded vision-language models (VLMs) , allowing clinicians to intuitively query and interact with a child’s cardiac anatomy in simulation before acting on it.
About 2.4 million people in the U.S. live with congenital heart disease. Historically, this has been a population too rare and too diverse to attract traditional device-company investment at the scale families need. No single company has built the tools Jolley’s team requires. No single institution could build them alone.
SlicerHeart’s tools are free to use and build on. Researchers at Stanford and Boston Children’s contribute additional tools alongside CHOP. A national consortium of children’s hospitals is now forming to build the next generation of shared modeling infrastructure, with open source as the connective tissue across institutions.
One of CHOP’s research collaborations simulates how heart valves interact with blood flow. Understanding these dynamics is critical for predicting disease progression, planning repairs, and evaluating new devices.
“It’s too small a population to support traditional commercial development by normal economics,” Jolley said. “But it’s such an important problem that between the research community and philanthropy, people are getting behind it. Open source defies traditional economics for small and heterogenous populations by allowing collaboration and progress without barriers.”
NVIDIA’s investment and active collaboration with others in developing open platforms — MONAI for medical imaging AI, Newton for physics simulation, OpenUSD for 3D interoperability and virtual reality — gives teams like Jolley’s access to infrastructure maintained at industrial scale. A lab at a children’s hospital can now quickly harness tools that would otherwise require a company-sized engineering team to build and sustain, while benefiting from the continued innovation of a broad open source community.
At GTC Berlin, banks, payment companies and financial data providers are showing what production-scale intelligence looks like — built on NVIDIA accelerated computing, powered by open weight models and running...
To help developers rapidly build world models, which help physical AI systems understand and simulate the real world, NVIDIA has expanded the Cosmos platform with new training tools, simulation checkpoints...
European retailers are using open models and physical intelligence across use cases — from a commerce platform cutting inference costs by 90% to to a fulfillment center where collaboration of...
Weather forecasts shape more than daily plans; timely weather information is crucial for energy producers, insurers and transport operators to plan around changing conditions. A global forecast can show a...

### Article 212 · 2026-09-15 · NVIDIA Corporation
‘Now We Can Know Everything and Do Anything,’ Jensen Huang Says at Dreamforce | NVIDIA Blog

At Dreamforce, Salesforce and NVIDIA announced Koa, a CRM reasoning model for Agentforce, post-trained from Nemotron on 27 years of Salesforce CRM intelligence — and running entirely within Salesforce’s own infrastructure.
That was the message NVIDIA founder and CEO Jensen Huang brought to Salesforce Dreamforce Tuesday, joining CEO Marc Benioff onstage in an appearance that coincided with the announcement of Koa — Salesforce’s first CRM reasoning model, built on NVIDIA Nemotron 3 Super.
Huang didn’t just take the stage. He walked into the crowd — threading through the audience at Moscone Center, mic in hand, with Benioff alongside. “We’re all following you, bro,” Benioff told Huang at one point, drawing applause.
“With electricity, we could power everything,” Huang said, tracing the arc of industrial revolutions. “With the internet, you can find anything. And now, with artificial intelligence as an infrastructure layer across the planet, we can know everything and do anything.”
That arc led directly to the announcement. Salesforce’s first reasoning model was built by post-training NVIDIA Nemotron 3 Super on a proprietary synthetic dataset drawn from nearly three decades of enterprise CRM deployments.
“Safety is paramount in a lot of ways. It’s job one,” Huang said. “However, safety is an engineering problem. We’re developing computing systems after all … If you build a product or a service and you’re not confident in its functionality, capability or safety, then don’t release it.”
He reiterated that innovation and leadership should coincide with safety and security . “Innovation, speed and safe products — it’s a false choice,” Huang said. “You could definitely have both at the same time. So run as fast as you can. But if you feel at any given point in time the company’s out of control, or the product’s not going to be safe, take a pause and make sure you get it right.”
Throughout his talk, Huang offered a positive vision for the future of AI. He noted he was among the first to push back on the notion that AI would end the software industry. He also pushed back on the idea that AI is a threat to jobs.
“As a result of our ambition, and with the productivity boost we get from AI, the sky’s the limit,” he added. “Engage AI. Don’t get left behind.”
“Every company, every enterprise, every country would become an AI company,” Huang said. “It’s going to be an agentic enterprise.”
“The sky is especially the limit for our Trailblazers,” Benioff said, referring to the company’s customer and developer community. “I think this technology, the way it empowers people … the technology can partner with them to do this in incredible new ways.”
Because NVIDIA Nemotron is open, Salesforce was able to fine-tune and run the model entirely within its own infrastructure. Salesforce controls the weights, the model runs on Salesforce’s systems and no customer data is used during training or inference.
“Not a single byte of customer data was used,” said Rohan Kumar, Salesforce’s president of platform and engineering, who introduced Koa before Huang took the stage.
“People are both adopting closed models at exponential rates, but also building their own custom AIs — because every single software company is an AI company, and every single enterprise is going to be an agentic and AI enterprise.”
NVIDIA is one of them — running on Salesforce across sales, service, marketing and operations, and currently piloting Agentforce for customer-support workflows.
The training corpus covers synthetic enterprise scenarios across 14+ industries — manufacturing, financial services, healthcare and travel.
In Salesforce’s CRM Bench, a model benchmark that includes a suite of real-world tasks like updating an opportunity, routing a case, or scheduling a follow-up, Koa already matches or exceeds leading model performance on CRM actions with 3x fewer errors.
Koa is already running inside Salesforce, powering an employee agent in Slack, and is moving into customer pilots in October as a customer-selectable model in Agentforce, starting with Formula 1, UChicago Medicine, Baxter Credit Union, 1-800Accountant, Engine and Xero. General availability is expected winter 2026 in U.S. regions.
