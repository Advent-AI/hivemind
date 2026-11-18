# Blind reader, matter census batch 7 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 40 articles (numbers 213 to 252,
2026-09-15 to 2026-09-16, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 213 · 2026-09-15 · techcrunch.com
We don’t need AI regulation — leave safety to us, Nvidia’s Jensen Huang says

Nvidia founder and CEO Jensen Huang made his position on the dangers AI poses very clear while speaking at Salesforce’s Dreamforce conference on Tuesday. To him, AI isn’t some new form of “alien mind,” as at least one OpenAI safety researcher has described it. It’s just hardware and software, he says, built by humans. That means, in his view, it can be controlled by humans and existing laws.
“Safety is an engineering problem, not a legal one,” he said. “We’re developing software after all. We’re developing computing systems after all. It’s a complicated computing system, but it’s ultimately a computing system.”
Therefore, there’s no need for new laws or regulations to govern it, he argues. In fact, Huang sees little need for new laws at all. The free market, he argues, will be enough to pressure companies not to release unsafe products.
“If we’re not confident about the safety of the products, like all companies, like you and I, all the companies here, if you build a product or a service, and you’re not confident in its functionality, capability, or safety, then don’t release it. And so that’s a very obvious thing to do,” he said.
He continued: “You pace yourself until you are confident you’re releasing something that the market would appreciate. The market forces are already there. We don’t need any new laws. We don’t need new regulations. We just need companies to decide that when [to] run as fast as they can. I think innovation, speed, and safe products … it’s a false choice. You could definitely have both at the same time. So run as fast as you can. But if you feel at any given point in time the company’s out of control, or the product’s not going to be safe, you know, take a pause and make sure you get it right.”
In some ways, this is a comforting thought. If anyone in the world knows AI, it is Nvidia’s founder, who’s been building the hardware brains of AI since well before ChatGPT existed and now runs a company that also makes open source models, agents, harnesses, and sandboxes.
Then again, if we’re being cynical, his point of view is also unsurprising for someone who’s had his bread so well buttered by the AI boom . Why would he want regulation to come along and add in a layer of hinderance that could slow down Nvidia’s quest to sell ever more AI systems and software? As he also said in the interview: “I’m more ambitious than ever. As a result of our ambition, and with the product productivity boost that we get from AI, the sky’s the limit for us. The sky’s the limit for our company. The sky’s the limit for every industry, for every single country.”
Unfortunately, even companies with the best intentions ship faulty products with unintended consequences, even software. Remember the 2024 CrowdStrike bluescreen-of-death fiasco that grounded thousands of flights and caused other havoc for businesses? Then there are companies accused of deliberately acting with less-than-good intentions. Meta just paid $18 billion to settle a lawsuit over social media harms to children .
And AI has already caused harm, too, whatever the intentions or safety testing involved, from an OpenAI model hacking into Hugging Face to lawsuits against the AI lab over the suicides of young people who engaged in long conversations with its chatbot.
The “leave them alone” strategy, which would let these companies release products as they see fit, could be an unwise approach to AI safety as far as society is concerned. Though Huang is right that it’s possible existing product liability laws could cover AI — if AI doesn’t somehow kill us all before enough cases get through the courts to test that theory.
He didn’t discuss the other route, which seems close to taking shape: industry self-regulation. Huang’s approach has been more to champion open-weight models and companies’ use of them as a competitive counterweight to proprietary AI labs.
But right now, the industry has a short window to institute self-regulation and to encourage AI labs worldwide, even those in China, to see the wisdom in participating. As Microsoft CEO Satya Nadella said at the All-In Summit on Monday, “China should also deeply care about the same safety concerns if the United States cares about them, right? Why should it be different for them? It’s not like they won’t have the same hacking problem. It’s not as if they don’t want to make sure that their citizens are benefiting from AI, just like we would want our citizens to benefit from AI.”
For now, though, if Huang is a no on any new AI regulation, he may be influential enough to get his way. He also demonstrated this week that he, quite literally, has the ear of President Trump .

### Article 214 · 2026-09-15 · finance.yahoo.com
Nvidia (NVDA) Is Discussing Up To $10 Billion For An AI IPO

Nvidia (NasdaqGS: NVDA) is in advanced talks to invest up to US$10b in Anthropic's planned IPO, according to people familiar with the discussions.
The chipmaker is also exploring a potential acquisition of AI platform Hugging Face for up to US$14b, in a deal that would expand its software footprint.
Both moves would extend Nvidia's role beyond AI hardware into deeper capital partnerships and ownership stakes in key model and tooling providers.
These possible Anthropic and Hugging Face deals matter, but investors need to weigh them alongside Nvidia's broader risk profile. Take a look at 2 warning signs (1 major) we have identified for NVIDIA.
For readers looking for more ideas tied to the build-out behind generative AI, the next logical place to explore is 60 AI infrastructure stocks .
NVIDIA runs large scale AI infrastructure across data centers in the US and internationally, so deeper ties to Anthropic and Hugging Face would plug the hardware giant directly into the model and tooling layer that relies on its chips. The group already operates at a scale where software ecosystems can influence how effectively customers use its compute platforms.
Do Anthropic and Hugging Face pull Nvidia deeper into the AI stack, or just reinforce the existing story?
Nvidia's Narrative rests on the idea that it is building a full-stack AI infrastructure platform, not just selling chips, and that this breadth keeps customers tied into its ecosystem. The push to back Anthropic's IPO and potentially buy Hugging Face plugs straight into that thesis by tying capital to the software and model layers that run on its hardware.
"The company is capturing a growing share of the expanding value chain by deploying full-stack AI infrastructure, deepening customer lock-in, boosting recurring software revenues, and supporting high gross margins..."
See how the full story points towards a $303 fair value for NVIDIA .
The Anthropic talks align with that full-stack story. Funding a major model provider while already supplying compute extends Nvidia's role from supplier to financial partner, which fits the Narrative's focus on deeper customer reliance and recurring software-like economics. It also leans into the same AI infrastructure commitments that analysts see as supporting multi-year data center demand.
The Hugging Face discussions cut both ways for the thesis. Owning a widely used open-source hub could strengthen CUDA centric workflows and differentiate Nvidia further from AMD and Intel, yet it also sharpens existing risks around regulatory scrutiny, customer vertical integration and energy intensive AI factory buildouts that analysts already flag in the Narrative.
In the end, these Anthropic and Hugging Face moves only matter to you in the context of which Nvidia story you buy into, from long runway AI infrastructure platform to a hardware leader stretching its risk profile to stay ahead.

### Article 215 · 2026-09-15 · fool.com
Nvidia Bought Hugging Face for $12.9 Billion. This Software Acquisition Changes Everything.

Nvidia ( NVDA +2.55% ) spent about $12.9 billion recently to acquire Hugging Face. While the name tells you absolutely nothing about what Hugging Face does, I think it's a game-changing buy for Nvidia, as it marks the chipmaker's step into a different part of the artificial intelligence (AI) sector.
Nvidia investors should be thrilled with the direction this purchase will lead the company in.
Hugging Face dovetails well with Nvidia's existing businesses
Hugging Face is essentially a collaborative platform and repository for hosting pre-trained AI models, datasets, and open-source machine learning libraries. Its users can test out these models in its free cloud spaces and inference environments. While it does offer some paid tiers, it's mostly a free-to-use service as of now. So, why should Nvidia investors be excited about its purchase of a company that isn't generating a ton of revenue? In this instance, the chipmaker is OK with losing money on this service -- because it will steer developers toward the Nvidia ecosystem.
If a user develops an AI model or application using Hugging Face, and then wants to take it to the next level, redoing everything on different hardware won't make a lot of sense. So if everything developed in Hugging Face's programming environment runs on Nvidia's hardware already, it would be pretty easy to recreate it on a different Nvidia-powered platform where the program could be monetizable.
This will allow Nvidia to capture more of the business of AI developers utilizing open-source AI models (versus closed-source models like those from OpenAI or Anthropic), as they will be less likely to switch hardware platforms later on in their process.
This is a genius move, and it ensures that Nvidia will also be relevant in the next phase of AI when less hardware will need to be purchased.
However, the acquisition is not a measurable needle-mover. While Nvidia may benefit over the long term by having more developers steered in the direction of its hardware, that return on investment won't be easily discernible. That may be a problem for some investors, but I think most should be OK with it. After all, Nvidia had nearly $100 billion in cash, debt securities, and equity securities on its books as of the end of its most recent quarter. Nvidia made a smart move by acquiring Hugging Face, and while it may not be an obvious needle-mover, it will help secure the tech giant's place in the future.
By Keithen Drury – Sep 15, 2026 at 5:12PM EST

### Article 216 · 2026-09-15 · cnbc.com
Nvidia's Huang diverges with CEOs of Anthropic, OpenAI on AI safety at Dreamforce

Anthropic CEO Dario Amodei and Nvidia CEO Jensen Huang shared differing views on AI safety during the keynote of Salesforce's Dreamforce conference.
Their comments, followed later by an interview with OpenAI's Sam Altman, landed days after Amodei published an essay urging the AI industry to slow the pace of model development.
Dario Amodei, Anthropic Co-Founder and CEO, and Marc Benioff, Salesforce CEO and Co-Founder, attend Dreamforce 2026 summit in San Francisco, California, U.S., Sept.15, 2026.
Anthropic CEO Dario Amodei and OpenAI CEO Sam Altman presented views on artificial intelligence safety that differed from Nvidia CEO Jensen Huang in conversations at Salesforce's Dreamforce conference, days after the debate burst into the mainstream.
Amodei took the stage first with Salesforce CEO Marc Benioff, during his annual keynote, an appearance that followed an essay Amodei published over the weekend urging the industry to slow the pace of model development.
"I think that's the way to lead the industry forward, to set an example, to say that everyone can always be better," Amodei told Benioff on Tuesday, in front of about 12,000 people at San Francisco's Moscone Center.
Industry executives including OpenAI CEO Sam Altman , SpaceX CEO Elon Musk and Google DeepMind Chair Demis Hassabis, quickly voiced support for Amodei's proposal, which came after industry researchers last week raised the alarm on AI's potential to cause catastrophic harm. Amodei suggested a three-step plan to temper how quickly model capabilities improve without "sacrificing commercial advantage or the United States' lead in AI."
Huang, who appeared with Benioff shortly after Amodei, has a different perspective. The CEO of the world's most valuable company said market forces already exist, and that the industry doesn't need new laws or regulations. Huang added that speed and safety are not mutually exclusive, though companies should pace themselves until they are sure they are releasing something that the market will appreciate.
"It's a false choice," Huang told Benioff. "You could definitely have both at the same time."
Huang said it's up to the model developers to act responsibly with their products.
"Run as fast as you can," he said. "But if you feel at any given point in time the company's out of control or the product's not going to be safe, take a pause and make sure you get it right."
A day earlier, Huang was on stage in Los Angeles for the All-In Summit, where he took a call from President Donald Trump. The president, while on speaker, expressed concern about people who are trying to stand in the way of AI data center construction.
"We're not going to let that happen, sir," Huang said to Trump.
Dreamforce has been one of the premier events in the software industry for well over a decade, attracting about 50,000 people to downtown San Francisco and taking over a large swath of its hometown. Benioff's keynote always includes multiple high-profile guests, often people who are at the center of the tech universe at that particular time.
Benioff has had longstanding relationships with both Huang and Amodei.
On Tuesday, Salesforce and Nvidia announced a new reasoning model for the software company's Agentforce platform, which was built on one of Nvidia open-weight Nemotron models. Late last month, Salesforce and Anthropic expanded their strategic partnership and unveiled "Claudeforce," a new way for salespeople to access critical data directly from inside Anthropic's Claude chatbot.
In terms of how the model companies should proceed, Benioff told reporters on Tuesday, "If they feel like they should slow down, then they should slow down. If they feel they should speed up, they should they should speed up. And then they should be held accountable."
Altman's appearance with Benioff took place later in the day. During a fireside chat between the two CEOs, Altman said it's imperative for safety and monitoring to come before capabilities, given the power of existing models.
"You have companies saying things like, 'We will only be responsible if other companies are responsible,'" Altman said. People then ask what the company is going to do to be safe and responsible "no matter what," he said.
"There should be no qualifier on that," Altman said.

### Article 217 · 2026-09-15 · gurufocus.com
Nvidia Stock Gains as Fund Manager Warns AI Trade Could Unwind Fast

Nvidia ( NASDAQ:NVDA ) shares edged up 1% on Tuesday's session after plunging more than 3% on Monday, with investors assessing whether heavy spending on AI infrastructure can continue at its current pace.
Jordan Cvetanovski of Pella Funds said he does not view Nvidia as especially expensive when looking several years ahead. He is more concerned about how much capital has accumulated in AI-focused stocks.
A change in expectations around data-center construction could put pressure on Nvidia and other chipmakers, while weaker enthusiasm for advanced AI development could also prompt investors to reduce exposure to the sector.
The latest caution follows comments from Anthropic and OpenAI executives calling for a slower pace of AI development because of safety concerns. That added to questions already facing the industry after months of heavy infrastructure investment.

### Article 218 · 2026-09-15 · fool.com
This Unassuming Stock is Trouncing Nvidia in 2026. Here’s Why It’s a No-Brainer Buy.

Nvidia (NASDAQ:NVDA) has been a no-brainer buy for investors over the past few years. The company, as leader in the artificial intelligence (AI) chip market, delivered explosive revenue growth quarter after quarter -- and this translated into explosive growth in the stock price too. Investors viewed Nvidia as the key to benefiting from the AI revolution, given the company's central role in the space.
Nvidia continues to march on as the AI chip giant, generating enormous revenue gains -- for example, in the latest quarter, revenue soared in the triple digits to more than $96 billion. But the tech giant is no longer among the biggest winners in the S&P 500 when it comes to stock performance. The stock has advanced about 17% so far this year, which is good, but far from the gains we've seen in the past.
And at the same time, an unassuming consumer-related stock is trouncing Nvidia in 2026. Let's find out why this player is a no-brainer buy right now.
The company I'm talking about saw revenue soar in early pandemic days, as it offered consumers an easy way to shop from the comfort of their armchairs and easily pick up essentials or get them delivered. But in more recent years, this retaile r saw revenue stagnate. It maintained the $30 billion in annual revenue growth it gained in about three years earlier this decade, but it struggled to make further gains. The player I'm referring to is Target (NYSE:TGT), a stock that's climbed nearly 60% so far this year.
This retail giant faced various challenges, and these weighed on revenue growth and stock price performance. But over the past several months, a turnaround has been gaining momentum. Michael Fiddelke, a longtime executive at Target, took the reins as chief executive officer early in the year and put into place a plan that's already beginning to bear fruit. Fiddelke placed a focus on employee training, a revamp of displays and product assortment, and harnessing the power of AI to improve the shopping experience. To do this, Target announced it would invest $2 billion this year.
Target's development of such a plan is a reason to be optimistic, but what confirms my sentiment is the company's recent earnings report. The retailer still has a lot of terrain to cover, of course, but it's made impressive progress in these early turnaround stages. For example, traffic growth climbed 3.6% year over year, and food and beverage sales advanced in the high single digits after the company implemented layout changes in almost half of these assortments. Beauty was also an area of strength, with sales advancing in the high single digits.
And it's important to keep in mind that this recovery and growth plan was launched in March, so we're in the early stages of the process. That suggests a great deal of growth could lie ahead as the company redesigns layouts, improves product assortment, and benefits from its new stores, too -- 17 opened in the recent quarter.
All of this represents a solid reason to buy Target stock . It's a quality company that is well-positioned for success down the road as its turnaround plan advances. Now here's a second reason to get in on this stock right now: Target is a Dividend King, meaning it's increased its dividend for more than 50 consecutive years. This means you can count on this player for passive income and growth in this passive income over time. The company's dividend increases suggest a strong commitment to rewarding shareholders, and Target also has the free cash flow, at about $4.5 billion, to support dividend payments.
So, when you buy shares of Target, you're getting in on a fantastic turnaround story and benefiting from passive income at the same time. It's not surprising that this unassuming stock is trouncing Nvidia this year. And all of this makes it a no-brainer buy that you'll want to hold onto for the long term.

### Article 219 · 2026-09-15 · cnbc.com
Nvidia's Huang rips Anthropic's proposal for AI safety antitrust waiver: 'Completely unnecessary'

Nvidia CEO Jensen Huang pushed back against calls to give AI companies antitrust exemptions to coordinate on slowing the development of advanced models.
Huang said AI safety is a real concern but argued it should be addressed through engineering and testing rather than new laws or regulations.
Nvidia CEO Jensen Huang on Tuesday slammed proposals of artificial intelligence companies antitrust exemptions that could coordinate a slowdown of developing increasingly powerful models.
Huang's comments — in an interview with CNBC's Jim Cramer — come during an intense debate over AI safety fueled by an essay Anthropic CEO Dario Amodei published Saturday. Amodei proposed that leading AI labs coordinate to " pace the frontier, " or deliberately slow the development of advanced models to give companies more time to test and safeguard. Amodei said that effort could require government mediation or waivers of antitrust restrictions.
Huang agreed that AI companies need to take safety seriously, but argued they should be able to solve those challenges themselves.
"The fact that we need new laws, new antitrust laws, or new regulations, so that these companies could do their fundamental engineering and do it properly before they release products, that is just completely unnecessary," Huang said on CNBC's " Mad Money ." "We have plenty of laws. We have plenty of regulations that govern the reliability and the functionality of products."
In his essay, Amodei laid out a three-step approach to moderate the pace of model development, beginning with embedding third-party safety evaluators at each lab. The second and third steps are democratic and global coordination on safety standards and "limits on the rate of unchecked AI progress," Amodei wrote. "Some forms of coordination that would be impactful for pacing are legally challenging, and will require government support."
The legal issues arise because leading AI labs are competitors and their models are competing products. The Sherman Antitrust Act generally prohibits agreements among rivals that unreasonably restrain competition, while certain forms of coordination — including agreements to restrict output — can be illegal. That creates potential legal risks if competing AI developers were to jointly agree on how quickly they would develop or release new models.
Huang said model developers have the power to ensure their products are safe before releasing them.
"Safety is an engineering problem. Testing is an engineering problem," said Huang, whose company counts Anthropic and rival lab OpenAI as important customers. Nvidia also develops its own Nemotron family of open-weight models. "We should create products and properly test them. And if they're not ready to be released, just hold on to it and keep testing it and keep engineering until it's ready."
The AI boom has turned Nvidia into the world's largest chipmaker and most valuable company. Efforts to slow the development of more capable models may pose a risk to Nvidia's future growth.
Anthropic did not respond to CNBC's request for comment on Huang's remarks.
"AI safety is a real thing," Huang told Cramer. "Engineering products so that they are safe for the world to use — that's a real thing. And companies should innovate as fast as possible, but they should never innovate so fast as to release unsafe products."
Huang also pushed back against warnings that increasingly powerful AI models will pose an existential threat to humanity.
"We're not going to die in 2030," he said. "There are so many people in the world who are going to build AI properly. We're going to have all kinds of guardrails, invent all kinds of technology for safety and security."

### Article 220 · 2026-09-15 · cnbc.com
Meta CEO Mark Zuckerberg sides with Nvidia's Huang on AI safety and slowdown debate

Meta CEO Mark Zuckerberg shared his view of artificial intelligence safety on Tuesday, taking a stance that's more akin to the perspective of Nvidia CEO Jensen Huang rather than Anthropic chief Dario Amodei.
Because AI labs risk "significant liability if their models cause harm," Zuckerberg believes that companies are incentivized to prevent potential problems, taking a more market-driven perspective of the topic that's in line with Huang's public comments on the same day.
"There is a lot of debate about slowing progress on capabilities until alignment catches up," Zuckerberg said. "My view is that trust and alignment are quickly becoming the most important capabilities that will differentiate agents and models."
Meta CEO Mark Zuckerberg attends the annual Allen and Co. Sun Valley Media and Technology Conference at the Sun Valley Resort in Sun Valley, Idaho, U.S., July 9, 2026.
Zuckerberg said in a post on X and other social media platforms that he believes AI labs that fail to "focus on alignment will fall behind," referring to the kind of work that developers conduct to ensure the technologies adhere to human values. This topic of AI safety has been blown into the spotlight over the past few days after Amodei published an essay over the weekend in which he called for the tech industry to "slow the pace at which we improve the capabilities of AI models," an option that Altman later endorsed and which President Donald Trump later criticized .
Because AI labs risk "significant liability if their models cause harm," Zuckerberg believes that companies are incentivized to prevent potential problems, taking a more market-driven perspective of the topic that's in line with Huang's public comments on the same day. Zuckerberg said that Meta "delayed shipping" its Muse AI technologies because of "safety and security" reasons on its own volition.
"We just did it as part of our day-to-day work because it was clearly the right thing for people and for us," Zuckerberg said.
Speaking at the annual Salesforce Dreamforce conference, Huang told Salesforce CEO Marc Benioff that AI model makers should take responsibility for their products instead of seeking government regulations from lawmakers intended to limit potential harms and risks, as Amodei previously said. Huang reiterated his perspective in an interview on CNBC's " Mad Money ," characterizing such AI- related laws and regulations as "just completely unnecessary."
"We have plenty of laws. We have plenty of regulations that govern the reliability and the functionality of products," Huang said.
Amodei also spoke at Dreamforce and reinforced his core belief that slowing down the pace of model development represents "the way to lead the industry forward, to set an example, to say that everyone can always be better."
Later in the day at Dreamforce, Altman joined Benioff for a fireside chat and discussed his belief that safety and monitoring should take precedent over features when it comes to AI development, and acknowledged the general sense of fear that companies may not do so because of competitive pressure.
"I think it's great for our industry to say we want to come together and we want to be able to coordinate and make sure we have enough time to do this safely," Altman said. "But when there's any implication that because of the commercial pressures and the race, some company or between countries, some countries might not do the right thing, I think that's when people get very scared."
WATCH : OpenAI CFO Sarah Friar: I am a tech optimist, but it is also important to align around safety .
OpenAI CFO Sarah Friar: I am a tech optimist, but it is also important to align around safety

### Article 221 · 2026-09-15 · jpost.com
Nvidia announces project with Palantir to develop AI supply chain management

The company explained that the time spent on projects improved, but there were still human interactions that the AI couldn't replicate with its algorithm.
By TOBIAS HOLCMAN
Nvidia and Palantir announced on Thursday that they will incorporate an artificial intelligence model into the control of their critical supply chains, giving the automated system decision-making power.
"Nvidia has arguably the most valuable, intricate, and complex supply chain in the world. Our sovereign stack, powered by Nemotron models and Ontology, is delivering capabilities that exceed the frontier while providing alpha protection qualities unavailable otherwise,” said Alex Karp, cofounder and CEO of Palantir Technologies.
The deployment, according to the companies, will allow for "unprecedented supply chain visibility, identify constraints, continuously codify operational expertise and guide decisions at machine speed."
The system will be first implemented in Nvidia's supply chain, which spans millions of parts, thousands of suppliers, and a global network of manufacturing partners, with the objective of unifying every team worldwide into one operating system that improves their efficiency.
"Supply chains are the operating system of the physical economy, and AI factories are among the most complex systems ever built,” said Jensen Huang, founder and CEO of Nvidia . “From wafers and components to manufacturing , systems and customer delivery, hundreds of companies and trillions of dollars of global economic activity come together to deliver AI infrastructure. NVIDIA and Palantir are transforming this vast operational graph into sovereign intelligence."
The human side is still key for the system
Even if Nvidia reported that planners improved their numbers when using the new model, it also said human employees still provided key insights that weren't possible to get using only an AI system.
According to the company, emails exchanged with partners that week, severe weather in the forecast for a key region, an ongoing geopolitical event, or understanding the transcript from the last supplier debrief call were factors the AI struggled to incorporate when working across the entire supply chain.
The company explained that those inputs were better implemented by human instinct created by years of work rather than by the mathematical algorithm that guided the system, while the AI had an important role in working around the repetitive and predictable tasks.
The company concluded that the best implementation would help workers spend less time reconstructing routine decisions so they could focus on unpredictable situations.
Additionally, the Nvidia explained that the model was only going to train according to insights provided by the workers, with no changes made during production while managing a supply chain.

### Article 222 · 2026-09-15 · fool.com
Nvidia Will Still Beat AMD Through 2028. Here's the Data Behind My Conviction.

Nvidia ( NVDA +2.55% ) and AMD ( AMD +3.09% ) hold a near-duopoly in discrete GPUs. Nvidia controlled 90% of the discrete GPU market in the second quarter of 2026, according to Jon Peddie Research, while AMD held an 8% share. Nvidia clearly dominates the market, but AMD's focus on cheaper chips has kept it in the race for the past two decades.
In the past, Nvidia and AMD mainly focused on the PC gaming market. But in recent years, both companies have turned their attention to the data center market, where more organizations are using high-end GPUs to train large language models (LLMs) and other AI algorithms.
Both companies are benefiting from the AI market's explosive growth, but Nvidia is the clear winner. Over the past five years, Nvidia's stock has surged 854% -- but AMD's stock has only risen 378%. Let's see why Nvidia will likely stay ahead of AMD through 2028.
Nvidia's GPUs are generally more expensive than AMD's GPUs. Still, they're more powerful, more efficient at training massive AI models (especially when linked with other GPUs via their proprietary NVLink interconnect technology), and more energy-efficient. AMD's GPUs are cheaper and often have higher memory bandwidth than Nvidia's GPUs, making them better suited for AI inference tasks (handling software requests) rather than AI training.
Nvidia also locks in its customers with CUDA (Compute Unified Device Architecture), its proprietary software ecosystem. Almost all major AI frameworks are natively optimized for CUDA rather than AMD's ROCm or other software stacks. That stickiness discourages Nvidia's customers from rewriting and optimizing their applications for other GPUs.
Another key difference is their product and revenue mix. Nvidia generates most of its revenue from its data center GPUs, but AMD sells both GPUs and x86 CPUs for PCs and servers. That makes Nvidia a more focused play on the AI-driven data center market than AMD.
In Nvidia's latest quarter, its data center revenue surged 117% year over year and accounted 92% of its top line. In AMD's latest quarter, its data center revenue -- which includes both its Instinct GPUs and Epyc CPUs -- rose 107% but only accounted for 58% of its top line.
The rest of AMD's revenue comes from CPUs and GPUs for PCs, as well as specialized embedded processors. Therefore, it's also competing against Intel ( INTC +5.74% ) , which leads the PC and server CPU markets, as it tries to keep up with Nvidia. Therefore, the slower growth of AMD's non-AI businesses could offset its stronger sales of AI chips.
How fast are Nvidia and AMD growing?
We should always take Wall Street's estimates with a grain of salt, but analysts expect Nvidia and AMD to both profit from the AI market's expansion over the next few years.
From fiscal 2026 (which ended this January) to fiscal 2029, analysts expect Nvidia's revenue and EPS to both grow at CAGRs of 60%. Those are incredible growth rates for a stock that trades at 21 times this year's earnings. From 2025 to 2028, analysts expect AMD's revenue and EPS to grow at CAGRs of 52% and 95%, respectively. However, its stock looks a bit pricier at 86 times this year's earnings.
AMD also arguably faces more near-term challenges than Nvidia. Whereas Nvidia merely needs to defend its technological lead, keep its customers locked into its software ecosystem, and gradually expand into the inference market with new chips, AMD needs its upcoming products -- including its Helios rack-scale systems and MI450 deployments -- to pull customers away from Nvidia. There could be enough room for Nvidia and AMD to grow without trampling each other, but AMD's higher multiple doesn't leave it much room for delays or other disappointments.
Nvidia and AMD could both generate big gains for their patient investors through 2028. However, Nvidia's stronger top-line growth, wider moat, and low valuation all suggest it will stay ahead of AMD -- which still has a lot more to prove -- over the next two years.
By Leo Sun – Sep 15, 2026 at 1:20PM EST

### Article 223 · 2026-09-15 · barchart.com
AI Extinction Fears Could Crush Nvidia’s $1.3 Trillion Growth Engine, but Don’t Panic Sell Just Yet

Nvidia (NVDA) has become almost synonymous with the artificial intelligence boom because its increasingly powerful GPUs have supplied the computing muscle needed to train and run increasingly capable models.
The numbers show how dependent the boom has become on that hardware. Nvidia generated $96.2 billion of revenue in its fiscal 2027 second quarter, up 106% year-over-year (YoY), while data center revenue reached $89 billion, up 117%. Nvidia's fiscal 2026 revenue was $215.9 billion, up 65%.
Goldman Sachs Expects Fed Chair Kevin Warsh to Raise Rates This Week — But Not Because of Oil Prices.
Morgan Stanley Doubles Down on Apple Stock as New Offerings Become 'More Exciting'
The EV Bubble Has Burst. How to Play Rivian Stock Now.
That growth reflects a feedback loop: Better GPUs allow AI developers to train larger models, which creates demand for still more computing power. Nvidia's latest Blackwell systems are now being joined by its Vera Rubin architecture, with the company expecting fiscal 2028 revenue to grow about 70%.
Yet last week, the conversation about AI changed almost overnight. While nothing about this safety debate changes those numbers overnight, it could challenge the assumption underneath them—that AI capabilities will keep advancing at today's pace.
AI Safety Concerns Are Getting Harder to Ignore
The concern became more tangible this week after former Anthropic researcher Jacob Coxon resigned and warned that AI developers were racing toward self-improving systems without adequate safeguards.
More strikingly, Anthropic's alignment-science lead Evan Hubinger publicly said he personally believes there is a greater than 10% chance AI could kill all humans within the next decade. Wired reported that current and former AI researchers echoed concerns that the industry is approaching a critical period for controlling increasingly autonomous systems.
That is not a forecast investors can plug into an earnings model. It is, however, evidence that concerns about AI safety are no longer confined to outside critics.
Anthropic CEO Dario Amodei responded by calling for the industry to "pace the frontier"—slowing the improvement of AI models until safety measures can catch up. His proposal includes independent evaluators with access inside AI companies, coordination among frontier developers, and international cooperation. Anthropic has committed to the evaluator approach.
OpenAI CEO Sam Altman backed the idea, saying OpenAI would also use independent evaluators and agreeing that the frontier needs to be paced.
This is where the issue becomes an Nvidia investment story. Nvidia does not need AI companies to stop spending for its growth to suffer. It only needs the rate of spending to slow.
The company's latest 10-Q shows just how concentrated the opportunity has become. Nvidia's Compute & Networking segment generated $88.3 billion of the $96.2 billion quarterly total, while the company said growth was driven by data center products for accelerated computing and AI.
Nvidia's own earnings call also highlighted the scale of the spending cycle. The company said the top five hyperscalers are expected to spend nearly $800 billion on capital expenditures in 2026 and $1.3 trillion in 2027.
A coordinated slowdown would not necessarily eliminate that spending. Data centers will still need GPUs, existing AI applications will still run, and companies will still compete for technological advantages.
But investors should recognize the asymmetry. Nvidia's current valuation and earnings trajectory require extraordinary AI infrastructure growth to continue. If safety concerns delay frontier models, reduce training intensity, or push developers toward more efficient systems, some of the industry's appetite for ever-larger GPU clusters could be deferred.
That would not destroy Nvidia's business. It could, however, puncture the growth expectations that have made the stock such a powerful AI proxy.
In short, fears that AI could become uncontrollable are a legitimate new risk for Nvidia—but they are not yet an investment thesis for selling the stock. The bigger threat is a prolonged shift from "build as fast as possible" to "prove it's safe before building more." Nvidia's $89 billion quarterly data center business shows how much money is riding on continued acceleration.
Smart investors should watch AI spending commitments, model-release schedules, and new safety requirements more closely than extinction forecasts—at least for now. If the AI race merely becomes more controlled, Nvidia can keep growing. If the race itself starts slowing or ends up derailing, the company's earnings trajectory could eventually feel the impact.

### Article 224 · 2026-09-15 · fool.com
Nvidia Spent $26 Billion on Buybacks and Dividends in a Single Quarter. Its Board Is Betting Today's Profits Last 3 More Years.

Nvidia ( NVDA +2.55% ) returned approximately $26.0 billion to shareholders through share repurchases and cash dividends in its fiscal second quarter of 2027 (the period ended July 26). That's more than the $21.3 billion of free cash flow the artificial intelligence (AI) chip giant generated in the quarter, and nearly 10 times its capital spending for the period.
With guidance, management says what it expects from the coming quarter. With buybacks and dividends of this size, I think it shows how long it expects profits like today's to last. After all, repurchasing stock only works out if the earnings behind the price hold up.
A year earlier, the fiscal second-quarter total was about $10 billion -- $9.7 billion of buybacks and $244 million in dividends. In the first quarter of fiscal 2027, the figure hit about $20 billion. And the most recent quarter brought the first half's total to more than $45 billion. Zoom out, and the step-up looks even steeper: the company returned $41.1 billion in all of fiscal 2026, and this year's first half alone topped that.
The pace is speeding up, and the board keeps making room for more. On May 18, Nvidia increased its quarterly dividend from $0.01 per share to $0.25 per share and approved an extra $80 billion of share repurchase authorization, without expiration.
On top of that, after the second quarter's record returns, about $99 billion still remained under the repurchase program.
Why isn't Nvidia reinvesting the money?
Because the business doesn't need it. Nvidia designs chips and systems, while manufacturing partners own the factories that produce them. Revenue grew 106% year over year to $96.2 billion in the quarter, and net income climbed 126% to $59.7 billion -- yet capital spending was just $2.7 billion.
That doesn't mean management is out of ideas. Nvidia spent more than $42 billion buying equity stakes in other companies in the first half of the fiscal year, up from about $1.2 billion a year earlier. And in early September, it agreed to buy Hugging Face, a platform for open-source AI models, in a deal valued at about $12.9 billion.
Between the returns and that investing, Nvidia used more cash in the first half than the business produced. Free cash flow was $21.3 billion for the quarter and $69.9 billion for the half, up from $39.6 billion a year earlier. The company even issued $25 billion of senior notes in June.
Chief financial officer Colette Kress said on the company's late-August earnings call that Nvidia's plan is to return 50% or more of its free cash flow. Year to date, she said, it has returned 60%.
A repurchase program can be slowed quietly anytime management turns cautious. A dividend, I'd argue, is a harder commitment to unwind. Reducing one tends to alarm investors like almost nothing else.
At $0.25 per share, Nvidia's payout runs about $6 billion a quarter. Increasing the dividend 25-fold in May was management saying it expects free cash flow to remain comfortably above that bill for years to come.
"[W]e intend to increase and return excess free cash flow net of strategic uses," Kress said on the call.
The repurchases point the same way. Nvidia paid average prices of about $202 to $214 per share for the stock it bought during the fiscal second quarter. That's close to the share price of about $211 as of this writing.
Boards can misjudge cycles, of course. The chip industry has a long history of booms that ended abruptly. If AI spending slows down a couple of years from now, the money spent on buybacks at these prices could end up looking expensive.
But a management team bracing for that outcome would probably hoard cash instead of multiplying its dividend by 25.
What, then, does the $26 billion tell us about the next three years? I think it shows us that management expects the earnings funding it to hold up at least that long.
The stock trades at about 28 times earnings , calculated over the past four quarters. Arguably, that's a modest price for a company whose profits more than doubled in the latest quarter -- so long as they prove durable.
Sure, Nvidia's board could be misreading its own cycle. But it has a clearer view of demand than anyone outside the company, and it isn't acting concerned.
Nvidia Spent $26 Billion on Buybacks and Dividends in a Single Quarter. Its Board Is Betting Today's Profits Last 3 More Years.
By Daniel Sparks – Sep 15, 2026 at 9:47PM EST
Nvidia returned approximately $26.0 billion to shareholders via share repurchases and dividends in its fiscal second quarter.

### Article 225 · 2026-09-15 · simplywall.st
NVIDIA (NVDA) Gets A Fresh Platform Test After Salesforce Deal Sparks Undervalued View

Salesforce's launch of Koa, a CRM reasoning model built on NVIDIA (NVDA) Nemotron, places the chipmaker's software stack directly inside front-line customer workflows, ranging from service agents to regulated government operations.
That Salesforce partnership lands at a moment when NVIDIA's share price has pulled back, with the 7 day share price return down 8.42% and the 30 day share price return down 6.31%. Even so, the year to date share price return is 11.71% and the 5 year total shareholder return is roughly 9x, so recent AI sector worries have cooled momentum in the short term while long term holders still sit on substantial gains.
Compare how other AI infrastructure players are reacting to the same sentiment shift by scanning the hand picked 60 AI infrastructure stocks that are building around platforms like NVIDIA today.
NVIDIA now trades well below recent highs, yet long term shareholders still sit on multi year gains. Do you lean into this reset, or wait patiently for a deeper markdown before putting fresh capital to work as the valuation math comes next?
Most Popular Narrative: 24.7% Undervalued
The most followed narrative on NVIDIA pegs fair value at $280 per share, well above the recent $210.96 close. This puts the current pullback in a very different light for anyone focused on long term cash flows.
NVIDIA is not just a chipmaker. It is the platform that powers modern AI.
Data Center Revenue: Now more than 70% of total revenue and growing rapidly.
GPUs (H100, A100, B100 coming): Widely viewed as a leading standard for training LLMs like GPT, Gemini, Claude, and more.
CUDA Ecosystem: Proprietary software stack that can help retain developers. It is often compared to Apple's App Store but for AI researchers.
NVLink, DGX Systems, and NVDA Networking (Mellanox): The company is not just selling chips. It is selling a broader AI infrastructure.
Many large AI models today are built with NVIDIA hardware. For some practitioners, switching away can feel like trying to cook without a kitchen.
See why 364 investors see NVIDIA as 25% undervalued .
According to oscargarcia, that fair value implies the stock trades at roughly a quarter discount to intrinsic worth, using a discount rate of 9.47% and a revenue growth rate assumption of 7.45% that is lower than earlier narrative updates.
The same storyline emphasizes NVIDIA's cash generation and profitability, including a profit margin assumption of 51.69%, and uses those projected earnings and cash flows to support the $280 figure instead of anchoring on analyst targets around $328.66.
That approach aligns with the platform view described in the narrative. In this framework, more than $302.97 billion in annual revenue and $192.88 billion in net income are tied back to an ecosystem that spans data center infrastructure, gaming graphics, and automotive compute rather than a single product cycle.
Still, NVIDIA's reliance on a few hyperscale buyers, along with ongoing export restrictions to China, could pressure that long term AI platform narrative if demand patterns shift.
Mixed sentiment around NVIDIA's pullback and long term platform story can be a useful signal only if you stress test the details yourself. To weigh both the potential upside and the open questions, go through the 4 key rewards and 2 important warning signs .
If NVIDIA is already on your radar, do not stop there. Cast the net wider now so you are not chasing the next wave after it moves.
Hunt for strong value by scanning the 35 high quality undervalued stocks that combine quality fundamentals with prices that some investors may consider attractive.
Stack potential income streams by reviewing the 6 dividend fortresses that focus on higher yielding companies with an emphasis on resilience.
Prioritize resilience first and return second by checking the 11 resilient stocks with low risk scores curated for lower risk profiles and sturdier business models.

### Article 226 · 2026-09-15 · xda-developers.com
Nvidia's latest driver update had me thinking my GPU was dead, but this one fix stopped my screen from flickering

By Abhinav Raj
When Nvidia's 616.56 driver landed on my Nvidia App at the end of August, I installed it the way I'd installed every single Game Ready driver, which was, without a second thought. That very same evening after work, I booted Microsoft Flight Simulator 2024 like I always do, but after a few minutes of flying, I started seeing strange artefacts across the screen . A few minutes later, the game dropped me on the desktop, ruining over 30-ish minutes of progress.
Like any other paranoid user, I assumed the worst. A little after two years of use, my RTX 4070 Ti Super was done for. A few minutes later, though, I found that it hadn't, and I only worked that out after a fellow XDA colleague reported similar problems on his own machine. That ruled out the dead GPU theory, and pointed straight at the update everyone had just installed. The fix, however, wasn't straightforward. Here's how I got my screen to behave fine again after the latest botched driver update.
A little about the botched Nvidia driver update in question
616.56 created problems that Nvidia refused to ship a hotfix for
The problematic driver, as widely reported by the community , is GeForce Game Ready 616.56, which Nvidia pushed out at the end of August. Within a few days, its own feedback thread and subreddits were filled with complaints that ranged from display flickering, artefacting, and in some severe cases, dropping to a black screen. This affected multiple GPUs, from GTX 16 series through RTX 30, 40, and 50-series cards. This was widely reported by a number of news outlets .
The pattern most users landed on pointed at color depth, and the panels set to 8-bit were most affected. In some cases, switching to 10-bit output or turning on Windows Automatic Color Management stopped it, but of course, Nvidia never confirmed this.
Nvidia was quick to take note of the problem, but frustratingly enough, their fix wasn't comprehensive. On September 5, the company shipped a hotfix through 616.86, but it only addressed intermittent browser flickering, broken virtual displays, and black screens in some Remote Desktop sessions. The same fixes were folded into the WQHL 616.92 driver on September 9, but the flickering went untouched in both. So, in some ways, it's still an ongoing issue, which is why it's worth knowing how to fix this.
By Jacob Roach
A driver rollback didn't fix the problem for me
If it were that simple, the article wouldn't exist
With the issue identified, the first, and the most obvious thing to do, was to roll the driver back. If 616.56 broke it, an older release should undo the damage. So, naturally, I reverted through the Nvidia App, rebooted, and waited for the flickering to stop.
To my absolute surprise (and sheer horror), it didn't. The problem persisted and the annoying flickering continued on the same apps as though nothing had changed at all. This had my mind going in different directions, such as residual states or perhaps an incomplete cleanup. I also tried switching up the DisplayPort wires to see if it would make a difference, which did not.
This result, however, carried a useful clue. If going back a driver branch did nothing, the fault isn't limited just to the driver. Part of the problem was in the Windows environment itself, in the Desktop Window Manager specifically, and how it hands display surfaces to the panel.
I now stopped tinkering with drivers altogether and started looking for the setting that governed this behavior directly, and it was a single registry value in Windows. This seemed to be the one setting that finally stopped the flickering for good.
By Adam Conway
One DWORD in Windows did what a rollback couldn't
The registry workaround to this problem that I was talking about governs something called the Multi-Plane Overlay, or MPO for short. MPO lets the Desktop Window Manager hand certain display surfaces straight to the panel instead of composing them first, and it was this handoff flicking on and off that was producing the flicker. Switching it off came down to a single registry edit, which was the solution that finally worked for me.
If the driver rollback didn't work, it's a solution that could fix your flickering as well. The value you are looking for is called OverlayTestMode . It's a DWORD, set to 5, and it can be found under:
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Dwm
The fix itself is simple, and can be done in a few minutes. Here is how I did it:
Open the Registry Editor by using the combination Windows + R, type regedit, and hit Enter. On the side of caution, it's best to create a System Restore point first.
Paste the HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Dwm into the address bar at the top and press Enter.
Right-click an empty area in the right pane, choose New, followed by DWORD (32-bit) Value, name it exactly OverlayTestMode.
Double-click the new OverlayTestMode file created, enter 5 in the "Value" field, leave the base as Hexadecimal, and click OK.
Restart Windows for the change to take effect.
This change, of course, is fully reversible, so deleting the value puts Windows back exactly as it was. Although it is always recommended to create a System Restore point to make sure there's a hassle-free way to roll back changes in case there are unintended consequences.
An astonishing number of users online were fully convinced that their GPU or the VRAM chip is dying as a result of this driver update, including myself, until I decided to check the root cause of this issue online. Unfortunately, drivers producing unintended consequences on hardware, even from companies like Nvidia, have become a rather common occurrence, and this one was a textbook case. This is primarily the reason why I'm an advocate for keeping frequent system restore points, and where possible, maintaining a log of important changes to your PC.

### Article 227 · 2026-09-15 · businessinsider.com
How Nvidia gutted a onetime rival and left behind a $3.5 billion AI cloud

By Geoff Weiss
After Nvidia carved up much of Groq, the AI chip startup is now eyeing its next act.
So what's left? A $3.5 billion AI cloud with real infrastructure — and a harder fight to stand out without the signature chips that once made it a viable Nvidia challenger .
Last December, Nvidia paid roughly $20 billion to license Groq's signature chip architecture and hire its leadership, stopping short of a full acquisition. It was one of Nvidia's biggest deals ever and strengthened its position in inference — the fast-growing market for running AI models, where rivals have gained more ground than in training.
Groq 2.0 has lost some of what once made it stand out. Some customers said technical support and AI model choice worsened after the deal. And as inference becomes commoditized, price and speed increasingly matter more than which company provides it.
The unusual structure has also drawn scrutiny, with the Justice Department investigating whether it was designed to skirt antitrust review, The New York Times reported. Nvidia said in a statement that the deal was "the American system working as designed."
The surviving entity is hardly an empty shell. Groq has 13 data centers, plans to quadruple capacity next year, and 6 million developers and thousands of companies using its cloud. It's also increasingly relying on Nvidia systems — a striking reversal for a startup that once pitched its chips as a faster alternative.
Groq is backed by $1 billion in fresh capital. It was valued at $3.5 billion in its latest funding round, versus $6.9 billion before the Nvidia deal, though shareholders received payouts in between. It's betting on the sheer demand for AI compute.
"We think that the needs for inference are great," a source close to the company said. "It's sort of like the restaurant business. People just need food."
Nvidia said Groq "continues to be a separate and independent business."
When the Nvidia deal broke last December, Groq was thrown into limbo, former employees said. Management played the acquisition talks "very close to the vest," one said.
The deal came together in eight days, followed by a "mad dash" as former Groq employees became Nvidians overnight, a source close to the company said.
Groq quickly cycled through two CEOs. Simon Edwards, who had recently joined as chief financial officer, initially took over. Adam Winter assumed the helm in March, after which the company unveiled its new cloud-focused strategy.
Rather than walking away from its data-center commitments, Groq's leadership quickly realized it could refit the sites with Nvidia hardware, a source close to the company said.
The deal reshaped Groq's workforce. Most of the hardware and software engineering teams — including the majority of the cloud engineering team that built GroqCloud — moved to Nvidia, while data center operations, legal, human resources, finance, and other business functions largely remained to keep the entity running. The company has since added cloud and infrastructure veterans to its C-suite.
The upheaval didn't mean employees walked away empty-handed. Those who held equity received payouts from the deal, according to two former employees.
Some Groq customers said it wasn't quite business as usual
Some customers also felt friction.
Before the deal, the company had been known for a "very, very hands-on" approach to customer support, a third former employee said.
Paul Richards, cofounder and CEO of the AI startup Recall, said uncertainty about Groq's future prompted it to rely less on the company and work with other providers — though roughly a quarter of its inference still runs on Groq.
"Every person I spoke to there left the company. So that obviously was alarming," he said.
Recall previously had a private Slack with Groq employees, Richards said, and after the deal, "it was crickets."
Richards also said that Groq discontinued many of the AI models Recall used and wasn't adding the newer models he requested.
Willow cofounder Lawrence Liu saw key support staff move to Nvidia, requiring a "re-initiation period" with their replacements, though the transition was quick and the service remained reliable.
ScreenApp CEO Andre Dean Smith said Groq fell behind on some model updates and never delivered a planned feature. That prompted his company to shift work elsewhere, though it has since expanded its use of Groq again, he said.
A source close to Groq said that while customers may have lost support contacts who moved to Nvidia, they were connected with replacements, and no complaints reached leadership.
Not everyone noticed the disruption. Eoin McMillan, founder of Sourcetable, said it was "business as usual" after the deal.
"From my end user experience, you would never know anything happened at all," he said.
Groq is fighting for customers as inference providers proliferate and become harder to distinguish. Its rivals span inference specialists like Fireworks and Together AI, neoclouds such as CoreWeave, and cloud giants like Amazon and Google.
Groq says it has unique experience running its AI chips, known as language processing units, at scale, and that it will be among the first to deploy Nvidia's latest inference systems that incorporate them.
"You've got a billion-dollar-financed inference-native cloud," said early Groq investor David Levy of Porch Capital. "Shouldn't this be a big deal? I think it is."
The harder question is what will make customers choose Groq. Speed gaps are narrowing. And companies like OpenRouter make it easier for developers to switch between AI providers.
"Economics is the best thing they can offer their customers," said Ashish Nadkarni, an IDC vice president focused on enterprise infrastructure.
Sourcetable's McMillan said that Groq's speed once made it an obvious choice for certain workloads. Since then, competing services have gotten fast enough to narrow the advantage.
Groq doesn't see that as a problem. Demand is high enough to mint multiple winners, a source close to the company said: "You don't necessarily need a moat."

### Article 228 · 2026-09-15 · theguardian.com
Anthropic CEO renews call for AI slowdown as Nvidia’s urges acceleration

Anthropic’s CEO took the stage at a conference in San Francisco on Tuesday to reiterate his call for a slowdown of AI development, while Nvidia’s CEO argued against such deceleration.
Dario Amodei used an automotive analogy to make his point: when a competing car company has a safety incident like brake failures, it is a moment for all car companies to stop and review their own practices, he said at Salesforce’s Dreamforce convention on Tuesday.
“It’s very tempting to attack your competitor and say these guys are unsafe,” he said. “But I think the more responsible way to respond to it is to say, let’s look at our own record. We may not have had this big, high-profile incident, but I’m sure we’re not perfect.”
Nvidia’s Jensen Huang countered not long after: “Run as fast as you can.”
Amodei is calling for three courses of action: embedding third-party evaluators inside AI companies; coordinating safety standards among Democratic countries; and, eventually, larger global coordination. At Dreamforce, Amodei said Anthropic has committed to independent evaluators and was “going to have a dialogue with the rest of the industry” on the other two steps.
Amodei, xAI’s Elon Musk and OpenAI’s Sam Altman have recently called for a slowdown in the pace of AI development. The comments from the CEOs follow warnings from Jacob Coxon, a former Anthropic researcher, who resigned with a public declaration that AI could lead to the extinction of humanity within the decade. Coxon’s comments have stirred a larger debate within Silicon Valley, gained the attention of regulators and alarmed the public.
Huang, who also made an appearance at Dreamforce on Tuesday, said companies should not slow down AI development. He argued that new regulations were not necessary, advising AI companies to simply wait to release products until they know they are safe rather than begging the US government to intervene.
Huang said he envisioned a future where “every company, every enterprise … would become an AI company”. He said companies would become more ambitious when armed with AI and reiterated the idea that those who do not embrace the technology will get left behind.
He also pushed back on the idea that AI is going to destroy jobs, calling it “completely nonsense”.
One day prior at the All-In summit in Los Angeles, Donald Trump called Huang while the CEO was on stage. Huang put the president on speakerphone as Trump called the growing concern about AI a “hoax” and asserted again that a slowdown would only benefit China.
Huang responded: “We’re going to make sure that everybody wins in the AI race of America.”
Altman, who spoke later on Tuesday, called for a new level of rigor on security as AI advances.
Altman said AI models had advanced so quickly that monitoring and security need to be treated with a “new level of rigor”, calling an incident in which OpenAI agents hacked into another company a “wake-up call” for the industry. He also said the public was very “right to be afraid” of AI because of the potential loss of control, and the possibility of a small group of powerful AI companies exerting their views on the world.
People “feel the speed with which things are moving”, Altman said. “It doesn’t take as much imagination to imagine how this could go wrong.”
Previously, Altman agreed with Amodei’s push for a slowdown. But at Dreamforce on Tuesday, he said he was disappointed with how the argument had been framed.
“You have companies saying things like: ‘We will only slow down or we will only be responsible if other companies are responsible,’” he said, suggesting that this created fear for the public. “The world should trust that we are going to do the right thing because it’s the right thing.”
Altman said the hacking incidents showed that companies needed to prepare for an “impending wave of cyber-attacks”, saying: “We are not that far away from open-source models that can do serious damage.” Companies should use this “little period of advantage to defend yourselves”, he said.
The rising concern over AI comes as OpenAI and Anthropic head for initial public offerings, which could give investors and the public insight into the companies’ finances. Some analysts have predicted the IPOs will be among some of the largest in history. Amid the AI panic, Altman said he planned to delay OpenAI’s IPO until next year over safety concerns.
On Tuesday, Amodei said what surprised him most about AI was the speed of its proliferation.
“It’s been the pace of the progress – not just of the technology but of the economic side of it,” he said about the growing adoption of AI. “We had a prediction of just how capable these models would be. But I think what we didn’t appreciate is that it would lead to these companies growing so fast.”
Regardless of the rapid pace of development, Altman said he believed people would use AI as a tool to benefit other people and grow their businesses. He said this moment represented a time when the “sci-fi” scenario came to fruition, where people were talking to their AI assistants and transforming the way they work.
“I think we’re going to stay in an extremely human-centric world, no matter how good the technology gets,” he said.

### Article 229 · 2026-09-15 · aimagazine.com
NVIDIA & NDI: Advancing AI-Powered Multilingual Content

NVIDIA & NDI: Advancing AI-Powered Multilingual Content
By Adam Pond
NDI has announced NVIDIA AI-powered workflows that enable broadcasters to create and distribute multilingual content in real time.
Miguel Coutinho , Head of NDI, told AI Magazine: “Multilingual content has traditionally meant adding another layer of production for every language you want to support.
“That quickly becomes expensive and difficult to manage, particularly when you’re working in real time. What we’re demonstrating with NVIDIA is a different approach: keep the media workflow connected and use AI to create the language experiences from that shared source.
“It gives broadcasters a way to reach more audiences without having to build a separate production and distribution operation around every language.”
AI is quickly revolutionising a variety of industries and media is one of them . McKinsey has argued that gen AI’s impact on productivity could add trillions of dollars in value to the global economy.
NDI is a high-performance, royalty-free IP video standard created by NewTek (which is now part of Vizrt) – it is managed under an NDI business unit.
It is using NVIDIA AI for Media, including the NVIDIA LipSync NIM microservice, to enable real time translation, lip-synced dubbing and regional language adaptation within existing broadcast workflows.
“AI is transforming the way content is created, adapted and delivered,” says Lewis Smithingham , Principal Product Manager, Media and Entertainment at NVIDIA.
“The goal is to provide media organisations with the ability to increase viewer engagement by delivering content in their language and with advertising that makes sense for who and where they are. It’s a solution designed to create maximum value while reducing the cost and complexity of multilingual content delivery.”
The solution is aimed at eliminating separate language streams; the single-feed distribution is positioned to remove the infrastructure bottlenecks that have prevented real time global delivery.
The announcement was made at the IBC conference, which ran 11 - 14 September in Amsterdam, the Netherlands.
At the conference, NVIDIA announced a major expansion to NVIDIA AI for Media – which is a collection of GPU-accelerated software development kits (SDKs), NVIDIA NIM microservices, playbooks and blueprints that enhance audio, video and augmented-reality effects for media and entertainment workflows.
NVIDIA also announced Holoscan for Media with MXL, which is an open reference architecture and developer toolkit for building AI-powered media functions and applications for software-defined live production.
The company argues the integration creates a stronger foundation for AI in live media. AI processing, video applications and traditional media functions can increasingly operate on the same accelerated infrastructure and in the same software-defined environment.
It also announced NVIDIA Sports Intelligence Playbooks which are designed to give leagues, media companies and technology providers structured frameworks to fine-tune NVIDIA open models on their own sports footage and annotations, creating multimodal AI that can understand the rules, players, scoring, strategy and context unique to a sport.
NVIDIA 3D Body Pose: Estimates 2D and 3D human joint locations and angles from video captured by a single camera, helping turn motion into structured data without marker-based capture systems.
The NVIDIA Synthetic Video Detector (SVD): NIM microservice, announced earlier this year at SIGGRAPH, helps organisations assess the probability of whether footage is authentic or AI-generated, giving editorial, content-authentication, digital-forensics and media-integrity teams another point of analysis in their review process.
Video Frame Generation (VFG): Makes video motion appear smoother by using gen AI to create new frames between the original frames of a video.
NVIDIA Video Super Resolution (VSR) uses AI to upscale video while reducing noise, blur and compression artefacts.
NVIDIA TrueHDR: Converts standard-dynamic-range video into high-dynamic-range output in real time, reaching up to approximately 2,000 nits while preserving local contrast and adapting brightness to the content.
TSMC : The world's largest dedicated semiconductor foundry. Headquartered in Hsinchu, Taiwan, it manufactures advanced microchips for leading technology firms, pioneering sub-nanometre manufacturing processes essential for high-performance microprocessors and modern hardware infrastructure.
Microsoft : An American multinational technology corporation renowned for software development, consumer electronics and cloud computing. Its Azure platform provides scalable infrastructure, software services and enterprise solutions to millions of businesses and developers across the globe.
Dell Technologies : A global technology enterprise specialising in personal computers, data storage systems and server infrastructure. It supplies organisations worldwide with enterprise-grade hardware, cloud solutions and scalable data centre architecture required for demanding workloads.

### Article 230 · 2026-09-15 · zacks.com
NVIDIA vs. Broadcom: Which AI Stock Should You Buy After Earnings?

NVIDIA Corporation NVDA and Broadcom Inc AVGO both have capitalized on the robust artificial intelligence (AI) spending, with their latest quarterly results highlighting strong performance across key AI-related businesses. This raises an important question: which among the two is a better buy now for investors? Let's have a look –
NVDA's AI Growth Momentum Remains Strong as Demand Soars
According to NVIDIA's Aug. 26 press release, the company's fiscal second-quarter 2027 revenues reached $96.2 billion, up 106% year over year and 18% quarter over quarter. The Data Center business remained the key growth driver, generating $89 billion in revenues, up 117% year over year and 18% sequentially.
Alongside rapid top-line growth, NVIDIA delivered strong profitability. The company's non-GAAP gross margin came in at 75%, up from 72.5% a year ago. Notably, continued high operating income helped the company translate its revenue gains into faster earnings growth.
NVIDIA's growth momentum is expected to continue in the next quarter as well. The company expects revenues of around $108 billion, plus or minus 2%, in the fiscal third quarter of 2027, up 12% sequentially from the midpoint. NVIDIA, in reality, is well-positioned to gain from the next wave of AI investment as its cutting-edge Vera Rubin platform is already in full production
Solid Chip and Networking Demand Drives AVGO's AI Business
Broadcom reported $29.6 billion in revenues for the fiscal third quarter of 2026, up 86% year over year, according to the company's Sept. 2 press release. The key takeaway is that Broadcom's AI semiconductor revenues reached $16.7 billion, up 221% year over year and 54% sequentially.
Broadcom continues to benefit from the AI boom through custom chips and high-speed networking solutions. Ongoing AI spending is helping Broadcom's business gain momentum quarter over quarter. The company now expects AI semiconductor revenues to accelerate to $21.7 billion in the fiscal fourth quarter of 2026, increasing 236% year over year. Consolidated revenue guidance for the fiscal fourth quarter stands at $34.8 billion, up 93% year over year.
Along with rapid revenue growth, Broadcom's profitability remains a major strength. Broadcom's non-GAAP operating income rose 92% year over year to $20.1 billion in the fiscal third quarter, while free cash flow climbed 95% to $13.7 billion, giving the company strong financial flexibility to invest in research and development as well as growth.
NVIDIA or Broadcom: The Better AI Stock to Buy Post Earnings
The latest quarterly results show that NVIDIA is witnessing strong AI-driven growth led by Data Center demand. Broadcom, on the other hand, is benefiting from an increase in demand for its custom AI chips and networking solutions.
However, NVIDIA has a broader competitive moat that extends beyond its chips. While Broadcom's AI opportunity is mostly centered on custom accelerators and networking, NVIDIA has created a powerful ecosystem by combining graphics processing units, CUDA, networking and AI software.
NVIDIA also benefits from a more diversified customer base than Broadcom's handful of custom-accelerator businesses. Moreover, NVIDIA has demonstrated enormous scale while maintaining strong growth and profitability.
Lastly, NVIDIA's 63.7% net profit margin, compared with Broadcom's 42.9%, indicates NVIDIA's greater efficiency in converting revenues into bottom-line profits.
Therefore, NVIDIA appears to be the better buy than Broadcom, thanks to its stronger AI ecosystem, broader customer base, scale and stronger profitability. Additionally, NVIDIA appears more attractively valued than Broadcom. Per the price-to-earnings ratio, NVDA trades at 22.85 forward earnings compared with AVGO's 29.24 forward earnings multiple.
NVIDIA currently has a Zacks Rank #1 (Strong Buy), while Broadcom has a Zacks Rank #3 (Hold). You can see the complete list of today's Zacks Rank #1 stocks here.

### Article 231 · 2026-09-15 · cnbc.com
Nvidia CEO Huang attending Trump's state dinner for China's Xi: Source

Nvidia CEO Jensen Huang is expected to attend President Donald Trump's state dinner next week for Chinese President Xi Jinping.
Huang's planned attendance at the high-profile event is the latest sign of his alliance with Trump.
Huang appeared to side with Trump as the president pushed back on tech CEOs' warnings about the risks of rapid AI advancement.
Nvidia CEO Jensen Huang speaks during the keynote address at Salesforce's Dreamforce conference at the Moscone Center on Sept. 15, 2026 in San Francisco, California.
Nvidia CEO Jensen Huang is expected to attend a state dinner for Xi Jinping when the Chinese leader travels to Washington to meet with President Donald Trump next week, a person familiar with the matter told CNBC on Tuesday.
The person spoke on condition of anonymity to discuss the private guest list.
Huang's planned attendance at the high-profile event is the latest sign of his alliance with Trump. Those ties appeared stronger than ever this week, as the two men pushed back against other tech CEOs who have issued dire warnings about the risks posed by rapid AI advancement.
AI is expected to be a main topic of discussion when Xi meets with Trump. Huang was one of a select group of CEOs who traveled to China with Trump earlier this year.
It was not immediately clear who else has been invited to the state dinner.
A White House official told CNBC, "President Trump has invited several great American business leaders to his dinner with President Xi because he will always prioritize making good deals for our country."

### Article 232 · 2026-09-15 · fool.com
Prediction: Nvidia's $108 Billion Q3 Guide Will Look Conservative by December

Nvidia ( NVDA +2.55% ) expects third-quarter fiscal 2027 revenue of $108 billion, plus or minus 2%. Hence, the company is guiding for third-quarter revenue in the range of $105.8 billion to $110.2 billion.
However, I think Nvidia could report third-quarter revenue of around $113 billion to $114 billion. Here's why this seems like a plausible revenue target for the third quarter.
Why Nvidia could beat its third-quarter guidance
Nvidia has exceeded the high end of its revenue guidance in each of the past 12 quarters. Over the past four quarters, actual revenue has averaged 3.1% above the high end of guidance. If that trend continues in the third quarter, revenue could reach roughly $113.6 billion, compared with the current high end of about $110.2 billion.
Historical outperformance alone cannot help predict future revenue. But Nvidia's operating numbers also support similar revenue numbers. In the second quarter of its fiscal 2027 (ended July 26, 2026), Nvidia's hyperscaler revenue increased 13% sequentially to nearly $49 billion. AI Clouds, Industrial, and Enterprise (ACIE) revenue jumped 25% sequentially to $40 billion, while Edge Computing rose 13% sequentially to $7.2 billion.
If the three businesses simply repeat those sequential growth rates in the third quarter, total revenue can reach approximately $113.6 billion. Hence, Nvidia doesn't need growth to accelerate for its guidance to look conservative. The company needs the growth rates it just delivered to roughly continue for another quarter.
ACIE already accounts for about 45% of Nvidia's Data Center revenue. Management expects ACIE to drive most of the sequential revenue growth for Data Center in the third quarter, while hyperscaler demand could pick up more strongly in the fourth quarter and in fiscal 2028. Hence, Nvidia can rely on another large near-term growth driver beyond hyperscalers.
The ongoing ramp of Nvidia's next-generation computing system, Vera Rubin, is also expected to support revenue growth. Production shipments started in August 2026. Vera Rubin systems are expected to contribute about one-fifth of Nvidia's Data Center revenue in the third quarter. Nvidia estimates that its revenue opportunity per gigawatt of AI infrastructure will increase from about $25 billion with Blackwell systems to $40 billion with Vera Rubin systems, partly because the newer platform includes more CPUs, networking products, and other system components.
However, Vera Rubin is already included in Nvidia's third-quarter revenue guidance. Hence, a larger revenue beat will depend mainly on whether the company can ship more systems than expected.
However, certain risks cannot be ignored. Management expects supply to remain constrained through fiscal 2028, while higher memory prices are also adding pressure. Additionally, since hyperscaler revenue is expected to reaccelerate in the fourth quarter, it may provide less upside to third-quarter revenue results than ACIE or other growth drivers.
Nvidia is also preparing for higher demand. Inventory increased from about $21.4 billion in January 2026 to around $31.6 billion in July 2026. Supply and capacity commitments have also jumped from $119 billion in the previous quarter to $279 billion at the end of the second quarter. Nvidia's third-quarter revenue guidance also assumes no Data Center compute revenue from China.
Hence, I think there is a high probability that Nvidia will reach $113 billion to $114 billion in revenue in the third quarter.
Nvidia's third-quarter revenue guidance already looks aggressive, but its recent execution and changing revenue mix suggest there may still be room for upside.
By Manali Pradhan, CFA – Sep 15, 2026 at 3:00PM EST

### Article 233 · 2026-09-15 · insidermonkey.com
Nvidia’s Anthropic Investment: Securing AI Demand Amid Rising Competition

On September 13, Reuters reported that Anthropic is in talks to bring NVIDIA Corporation (NASDAQ: NVDA ) in as an anchor investor in what could become one of the largest IPOs in history, potentially raising as much as $100 billion at a valuation of around $2 trillion. Nvidia is reportedly considering an investment of up to $10 billion. Anthropic's annualized revenue run rate has reportedly increased from about $9 billion in 2025 to more than $65 billion by mid-2026, with the company targeting as much as $200 billion of revenue by 2028.
The strategic significance for Nvidia is greater than the potential financial return from the investment: Anthropic is a major buyer and user of AI computing infrastructure, and Reuters reported that it has committed $30 billion to Microsoft Azure infrastructure powered by Nvidia chips. Anthropic is also pursuing major capacity agreements with other providers and developing custom chips, making its future hardware choices strategically important to Nvidia.
The move would also deepen an already established relationship. NVIDIA Corporation (NASDAQ:NVDA) has previously disclosed an investment and technology partnership with Anthropic, while its fiscal 2026 filing said it had entered into an agreement to invest up to $10 billion in Anthropic. Nvidia generated $215.9 billion of fiscal 2026 revenue, up 65%, with Data Center revenue up 68%, demonstrating the enormous economic leverage of continued AI infrastructure spending.
Anthropic's Rapid Growth Strengthens Nvidia's Long-Term Opportunity
The strongest bullish argument is that an equity investment could help NVIDIA Corporation (NASDAQ:NVDA) protect and expand one of the fastest-growing sources of demand for its GPUs. Anthropic's reported annualized revenue growth from $9 billion to more than $65 billion in roughly 18 months implies a rapidly expanding need for training and inference capacity. Its reported $30 billion commitment to Microsoft Azure powered by Nvidia systems provides a particularly direct link between Anthropic's growth and Nvidia's infrastructure demand. Anthropic is also reportedly committing $45 billion to rent AI computing capacity from Nscale, with that infrastructure expected to use Nvidia's Vera Rubin chips, indicating that the relationship can translate into future-generation hardware demand rather than being limited to Nvidia's existing products.
The investment could also strengthen Nvidia's position as AI workloads shift from model training toward large-scale inference and agentic AI. Nvidia recently said Anthropic is evaluating its Vera CPU for CPU-intensive agentic workloads, while Nvidia has positioned Blackwell Ultra and the Vera Rubin platform around the rapidly expanding inference market. Nvidia has disclosed visibility into more than $1 trillion of cumulative Blackwell and Rubin revenue from the beginning of 2025 through 2027, with Anthropic among the model developers contributing to that ecosystem. A successful Anthropic IPO would therefore potentially create a well-capitalized AI customer capable of financing much larger infrastructure deployments, while Nvidia could simultaneously benefit from the investment's financial upside.
There is also a strategic ecosystem benefit. Anthropic is working with Amazon, Google, Microsoft, Nvidia and other infrastructure providers, while NVIDIA Corporation (NASDAQ:NVDA)'s investment gives it a closer economic relationship with a leading model developer rather than relying solely on selling hardware. That matters as hyperscalers and AI companies increasingly explore custom silicon. Nvidia's ability to remain deeply embedded in Anthropic's infrastructure roadmap could help defend its software-and-systems ecosystem against competing accelerators and custom chips. The company's recent agreement with d-Matrix to integrate third-party inference processors through NVLink Fusion similarly shows Nvidia is attempting to make its architecture the broader platform around AI compute, rather than relying exclusively on selling GPUs.
The principal risk is that NVIDIA Corporation (NASDAQ:NVDA) could be investing billions of dollars to support a customer whose long-term infrastructure strategy may increasingly diversify away from Nvidia GPUs. Reuters reported that Anthropic has partnerships with Amazon, Google and Broadcom and is developing custom chips to optimize hardware costs. More recently, Anthropic agreed to purchase billions of dollars of AI servers from AMD, while Broadcom has been involved in efforts to develop custom AI chips for Anthropic. That creates a potential conflict for Nvidia: Anthropic's growth may be extremely positive for AI infrastructure demand overall while being less positive for Nvidia's share of that spending. If Anthropic becomes increasingly successful at using alternative accelerators or custom silicon, Nvidia's investment could effectively help finance the expansion of a customer that is simultaneously reducing its dependence on Nvidia hardware.
Valuation is another concern. A potential $10 billion investment at an implied Anthropic valuation approaching $2 trillion would require extraordinary future growth to generate attractive returns. Reuters reported that Anthropic's valuation had already reached $965 billion following its May 2026 financing, meaning the prospective IPO would represent a more than doubling of valuation in a relatively short period. Nvidia therefore faces the risk of committing substantial capital at an exceptionally high private-market valuation, where even strong operational growth may not translate into equivalent investment returns. Nvidia itself has warned in regulatory filings that strategic investments can result in impairment losses or the loss of some or all invested capital and that capital allocated to such partnerships may not produce the anticipated strategic benefits.
More importantly, the investment comes as the market is becoming increasingly sensitive to whether the enormous AI infrastructure buildout can continue at its current pace. On September 14, Anthropic CEO Dario Amodei joined other AI leaders in calling for a slowdown in AI development because of safety concerns, contributing to a sharp selloff in AI-related stocks; the Philadelphia Semiconductor Index fell 5.1% that day. Although this does not directly undermine Anthropic's demand, it highlights the valuation and spending risk surrounding the AI ecosystem. NVIDIA Corporation (NASDAQ:NVDA)'s fiscal 2026 gross margin was already 71.1%, down from the prior year, partly because of its transition toward full-scale Blackwell data-center systems and a $4.5 billion charge related to H20 inventory and purchase obligations. A large additional strategic investment could therefore expose Nvidia to both equity-valuation risk and the possibility that AI infrastructure spending normalizes faster than expected.
NVIDIA Corporation (NASDAQ:NVDA)'s potential Anthropic investment is strategically bullish but financially mixed. It could secure substantial future AI-chip demand and strengthen Nvidia's position in Anthropic's infrastructure roadmap, but Anthropic's growing use of AMD, custom chips, and other suppliers creates competitive risk. Overall, the deal supports Nvidia's long-term growth and ecosystem position, but its high valuation and diversification risks limit the immediate upside.

### Article 234 · 2026-09-15 · fool.com
Nvidia May Have Won the AI Training Race, but the Bigger Opportunity Is Likely Still Ahead

Nvidia ( NVDA +2.55% ) has already won one of the biggest races in the technology sector.
Its graphics processing units (GPUs) provide the key computing power for the majority of the servers used to train today's most advanced artificial intelligence models. But here's the part of the company's opportunity that investors may be underestimating: Training AI is only the beginning.
Once an AI model has been trained, it can be deployed so that people can actually use it. And every time an AI is tasked with answering a question, writing computer code, generating an image, searching for information, or completing a task, the computing infrastructure built around Nvidia's hardware gets called upon again.
That's inference, and it may become Nvidia's next enormous opportunity.
The easiest way to understand the difference is to think about a student. Training is like going to school. The student spends enormous amounts of time learning. Inference is what happens after graduation -- the now-educated individual actually using what they learned to do a job.
AI works similarly. Companies spend huge amounts of time and computing power training models to understand language, images, code, and other information. Nvidia's GPUs have been the workhorses providing the parallel processing power behind much of that training.
But once the model is ready, the need for large quantities of computing power doesn't end. In fact, it may just be getting started. Imagine a company spending billions to build an incredibly sophisticated AI model. It doesn't build that model just to sit unused in a data center. It wants paying customers to use it.
Every use creates another computing workload. And unlike training, those inference workloads can happen millions or billions of times.
Training creates the AI. Inference puts the AI to work.
If systems that use AI become a common part of everyday life and business, the volume of inference workloads they generate could become enormous. And the expected wide use of AI agents could make this opportunity even bigger.
Today's chatbot might answer a question it's asked -- a single response to a single query. Tomorrow's AI agents could do much more complicated things. Suppose you ask an AI agent to research a company. It could take that one request, and respond to it by searching through multiple financial databases, reading corporate filings, looking for recent news, comparing it to competitors, building a valuation model, checking its calculations, and then writing a report.
That's not one AI response. It's an agent undertaking a chain of reasoning and actions. The more steps an AI agent takes in its effort to fulfill a request, the more computing power it requires.
Nvidia is actively positioning itself to benefit from this trend. For instance, its newest Vera Rubin architecture, which combines the chipmakers GPUs with its new CPUs, is specifically designed for these long-running inference workloads.
Don't assume Nvidia wins this market automatically
While the opportunity for inference will likely be larger than the market for training, the competition among chipmakers in this space is likely to be intense as well.
On one hand, hyperscalers like Amazon and Alphabet are developing their own custom AI chips, partly to reduce their reliance on Nvidia. Besides, the inference market is particularly sensitive to cost, as customers will have both incentives to switch and opportunities to do so if a competitor can deliver similar results at a meaningfully lower cost.
So the investment thesis isn't simply that inference will grow, therefore Nvidia will win. The more important question is: How much market share in this growing segment of AI can Nvidia capture?
So far, the company is betting heavily that its combination of hardware, networking, software, and a robust developer ecosystem will keep it at the center of the AI infrastructure stack. That said, investors should pay close attention to how well the company sustains its market share in the coming years.
The first phase of the AI revolution was about building increasingly powerful AI models. Nvidia was by far the most important supplier of the computing power needed to build them.
The next phase is about putting those models to work. If AI agents become widespread, they will process billions of increasingly complex tasks on our behalf. That means Nvidia's opportunity will not end when an AI model finishes training. It will begin there.
That's why, despite the fact that Nvidia has already delivered massive returns to its shareholders since the start of the AI race, the bulls believe the stock still has more excellent performances ahead of it.
Lawrence Nga is a contributing Motley Fool stock market analyst covering technology, consumer goods, e-commerce, AI, fintech, and China stocks. Before joining The Motley Fool, Lawrence wrote for Motley Fool Singapore and held roles as a lecturer at Kaplan Financial China and Liverpool College of Management Science, a performance analyst at AB Sugar, a financial analyst at BSO China Limited, and manager of supply chain finance at British Sugar. He earned a Bachelor of Science in Applied Accounting from Oxford Brookes University and holds credentials from both the Association of Chartered Certified Accountants (ACCA) and the Chartered Institute of Management Accountants (CIMA).
By Lawrence Nga – Sep 15, 2026 at 5:39PM EST

### Article 235 · 2026-09-15 · fool.com
Nvidia vs. Micron: Which Is the Better Artificial Intelligence (AI) Semiconductor Stock to Own for the Next 5 Years?

Between 2023 and 2025, Nvidia ( NVDA +2.55% ) was the market's most obvious artificial intelligence (AI) trade. During this period, the stock went parabolic, surging by 1,180% and turning the chipmaker into the world's most valuable company by market cap. On a split-adjusted basis, that was a climb from about $14 per share to $186 by the end of 2025.
Currently, Nvidia stock sits around $218, up another 17% year to date. This is what it looks like when a company owns a scarce product that's in heavy demand -- in this case, graphics processing units (GPUs).
Micron Technology 's ( MU +4.20% ) rocket-like move came a bit later, but hit much harder. Memory chips were an afterthought during the initial GPU gold rush. But as training clusters got larger and inference workloads got hungrier, supplies of high bandwidth memory (HBM) started running short. Prices for HBM soared, and Micron stock responded epically -- rising 239% in 2025 and another 242% so far this year. This type of price action indicates the market has recognized that memory is no longer just another tech commodity -- its supply is one of the key bottlenecks dictating the pace at which data centers can be built.
Nvidia and Micron are not the same bet. While Nvidia sells engines, Micron is selling the tanks for the fuel these engines cannot operate without. This begs the question: At this point, which of these AI chip stocks would be the better one to buy and hold for the next five years?
AI development is no longer just about who can procure the most GPUs. Nvidia understands this shift, and has spent the last couple of years trying to own the whole AI factory -- from compute, networking, optics, and software to even some of the customers that rent capacity. This is what makes Nvidia's partner ecosystem so important.
Marvell Technology received a $2 billion investment from Nvidia and a seat inside NVLink Fusion. This integration allows Marvell's custom accelerators to plug directly into Nvidia's rack-scale stack, rather than competing with it. Meanwhile, Coherent and Lumentum each received $2 billion checks from Nvidia in addition to purchase commitments to scale their lasers and silicon photonics -- hardware that provides greater bandwidth and reduced latency, and keeps today's ever-larger server clusters from choking on the limitations of copper.
Nvidia also invested $1 billion in Nokia as part of a collaboration to develop AI-enabled radio access networks (RANs). The idea is to parlay the same accelerated compute stacks that go into hyperscale data centers and place them at the edge among telecom networks.
Lastly, Nvidia works closely with Nebius and CoreWeave , two of the largest neocloud providers. Those relationships achieve two things at once: They help customers finance their infrastructure build-outs while keeping more data centers running on Nvidia systems.
Of course, Nvidia does have competition. Advanced Micro Devices is scaling its GPU business, while custom ASICs (application-specific integrated circuits) being developed by the hyperscale cloud providers -- Microsoft Azure, Amazon Web Services, and Alphabet 's Google Cloud -- represent a longer-term threat. Even so, many of these new rival chips still sit inside the very networks, racks, and software stacks Nvidia is trying to profit from through its savvy partnerships. Hyperscalers may design their own AI chips that can be substituted (in some cases) for Nvidia's GPUs, but Nvidia can still provide the CPU s, DPUs, switches, optics, and the software layer that go around those custom chips.
Memory is the current bottleneck, but how long will it last?
Right now, memory might be the most critical component within AI chip stacks, because there's a global shortage, and it will be at least 2028 before new production coming online could make a dent in the strained supply-and-demand dynamic.
Nvidia has acknowledged this with its own wallet, as in its last reported quarter, it boosted its supplier commitments by $119 billion to a total of $279 billion through fiscal 2032, and management said that contracted spending was primarily related to securing memory.
That order book is a gift to Micron, SK Hynix , and Samsung , the three firms that dominate the advanced DRAM and HBM markets. When only three companies control a scarce input, prices and profits tend to go vertical.
I think Micron's boom will be narrower than Nvidia's because the most likely way that this up phase of the memory supercycle remains hot past 2030 would be if new applications -- autonomous vehicles, robotics , and agentic AI -- consume more memory than analysts are currently expecting. Even if those workloads explode, Nvidia will still benefit from incrementally greater GPU adoption in these markets, and it still benefits from a business that's exposed to the rest of the value chain.
Nvidia vs. Micron: Valuation is the tiebreaker
The matter of valuations is where the five-year outlook gets practical. Nvidia trades at a forward price-to-earnings (P/E) ratio of around 23, a sharp discount to the levels it changed hands at during prior chapters in the AI revolution. Micron looks much cheaper by comparison on a near-term forward earnings multiple because its profitability and earnings are exploding in tandem with HBM pricing.
An apparently cheap stock price can be a trap when assessing a historically cyclical business like Micron. If the memory shortage fades even a little bit, Micron's multiple could go from a period of expansion to snapping right back. Nvidia's earnings multiple, on the other hand, has more room to expand and hold if investors view the company as a durable, diversified architect of next-generation AI factories rather than as a single-product chip vendor.
While Micron appears to be the sharper trade amid the visible memory shortage, Nvidia is the better stock to buy and hold over the next five years because the company is no longer designing just one scarce component. Rather, Nvidia is positioned as a critical supplier across the entire AI supply chain.
By Adam Spatacco – Sep 15, 2026 at 1:53PM EST
While Micron's growth prospects may be sharper than Nvidia's for the time being, Nvidia looks better positioned for the entirety of the AI infrastructure build-out.

### Article 236 · 2026-09-15 · gurufocus.com
Nvidia Rebounds, but AI's $1.08 Trillion Boom Faces Its First Brake

Nvidia ( NASDAQ:NVDA ), the dominant artificial-intelligence accelerator supplier, rebounded about 1.1% to $213.24 Tuesday morning after sliding more than 3% in the previous session. The bounce shows investors are not abandoning the AI trade just yet. Calls for slower frontier-model development have injected a new layer of uncertainty, but there is still no disclosed evidence of major Nvidia customers cancelling chip orders or delaying their massive data-center buildouts.
The spending backdrop remains enormous. Reuters cited BofA Global Research estimates showing Microsoft, Alphabet ( NASDAQ:GOOG ), Amazon ( NASDAQ:AMZN ), Meta ( NASDAQ:META ) and Oracle ( NYSE:ORCL ) could collectively pour roughly $795 billion into capital expenditures in 2026 before pushing that figure to $1.08 trillion in 2027. That would represent an increase of about 36% in a single year, keeping powerful demand underneath AI accelerators, networking equipment and memory. Tighter AI-safety rules could change the pace of deployment, but investors would need to see actual project delays or budget cuts before the core Nvidia demand story materially weakens.
Nvidia's latest quarter makes the size of that exposure clear: data-center revenue reached $89 billion, representing about 92.5% of total quarterly sales, while management is targeting approximately $108 billion in third-quarter revenue. The GuruFocus graphic adds another strong signal, giving Nvidia a GF Score of 95 out of 100, with particularly high readings for profitability, growth and financial strength, alongside solid momentum; GF Value is the obvious weaker area. Tuesday's 1.1% recovery still claws back only about one-third of Monday's percentage decline, suggesting the market continues to believe in Nvidia's AI growth engine while demanding a larger cushion against any slowdown in hyperscaler spending.

### Article 237 · 2026-09-15 · fool.com
Nvidia's Latest Move Spells Trouble for AMD and Intel Investors

Nvidia ( NVDA +2.55% ) absolutely dominates the market for advanced graphics processing units (GPUs) used for artificial intelligence (AI) applications. When it comes to the ultra-computationally intensive processing required to train AI models, the company is often projected to command more than 90% of the market.
Even for less computationally intensive inference applications used to run AI software, estimates of the company's market share in the category often range between 60% and 75%. Notably, Nvidia hasn't had much to offer when it comes to central processing units ( CPUs ) used to run some AI inference applications, and it's only just starting to compete in the broader server CPU market that is currently dominated by Intel ( INTC +5.74% ) and Advanced Micro Devices ( AMD +3.09% ) . On the other hand, Nvidia looks poised to make big inroads in the server CPU market -- and it could pose significant challenges for the current category leaders.
Nvidia could be poised to upend the CPU market
Due to GPUs' greater role in AI and data-center processing, and stronger margins in the category, Nvidia has been largely content to ignore the CPU market over the last decade. That's changing rapidly, however. More AI processing is being shifted to CPUs, while growth in the total number of operational and trained applications has increased the company's incentives to become a top player in the category.
The AI hardware leader is making moves to become a more diversified provider of compute technologies and services, and it looks poised for a rapid expansion in the server CPU market. In its fiscal Q2 2027 report, Nvidia revealed that its Grace family of CPUs had already generated $5 billion in sales over the trailing 12-month period, and that's almost certainly just the beginning of the company's scaling in the category.
Nvidia projects that its data center CPU revenue will more than double from this fiscal year to the next fiscal year, with the rollout of its next-generation family of processors playing a huge role in the growth. Along with its top-of-the-line Vera Rubin GPUs, the company is rolling out its Vera family of CPUs.
Nvidia has entered full production of its Vera CPUs, and it stands to see strong growth in the processing category as it pairs the hardware with its Vera Rubin GPUs and sells the tech as a stand-alone product. With its control of the high-end GPU market, the company has the advantage of delivering CPUs that are optimized for integrated performance.
Along those lines, Nvidia says its Vera hardware delivers performance and efficiency that significantly exceed those of any other data center CPU in key areas. These strengths could allow it to quickly win market share from Intel and AMD.
By Keith Noonan – Sep 15, 2026 at 5:35AM EST

### Article 238 · 2026-09-15 · techcrunch.com
Salesforce and Nvidia’s new reasoning model is everything the AI labs should fear

A new AI model called Koa is one of the biggest announcements from Salesforce this week at its giant Dreamforce tech conference. Koa is the company’s first reasoning model, built on Nvidia’s open-weight Nemotron model. The two companies worked together to post-train Koa to excel at sales, marketing, and customer-support-related tasks.
Koa is a shining example of how the enterprise world’s needs for AI are diverging from what the frontier labs are offering. Proprietary AI labs would rather have enterprises uploading files, code, prompts, and feedback directly into their models and agents, and spending millions to do so.
But with the model, Salesforce is offering its enterprise customers:
an open-weight alternative to closed frontier models
a model trained to do specific work tasks (rather than to solve impossible math problems )
Koa will be provided as an alternative to the other models Salesforce offers in its Agentforce platform, where its customers build agents to handle rote tasks like answering customer service questions or scheduling appointments.
“We’ve built many small task-specific language models, which are part of Agentforce’s portfolio,” Jayesh Govindarajan, EVP of Salesforce AI, told TechCrunch. “But reasoning has always been something that we’ve relied on the frontier model providers for. Until now.”
Before Koa, if an agent needed to reason through a long-running or multi-step task, those prompts would be routed to a frontier model like Claude or ChatGPT through Agentforce’s AI gateway (the system that decides which model handles which request).
“One of the reasons we hadn’t done this before, train our own enterprise-grade frontier model — we always wanted to — but the challenge has always been the lack of a pre-trained base model to start with. Until Nemotron came along, there was no sovereign American pre-trained model that was available, one, and two, that was state of the art, and, three, that had clear data provenance. We have no idea what Qwen trains on,” Govindarajan said, referring to the popular Chinese open-weight model produced by Alibaba.
Post-training a model like this means taking it from a general-purpose system to one well-versed in sales and customer support knowledge, and to do that, Salesforce and Nvidia did not use any actual data from Salesforce’s customers. Instead, they crafted synthetic data that mimicked customers’ patterns.
“We actually simulated a customer service environment with a persona customer service professional, including irate customers that call into the customer service center, all the way to a sales professional who’s trying to close a deal,” Govindarajan described.
Koa is meant to be better at the work tasks Salesforce customers want an agent to do — and cheaper, in terms of tokens burned — than sending those same tasks to Claude or ChatGPT.
With Nemotron, “we have a unique architecture for inference to be token efficient,” Kari Ann Briski, Nvidia’s VP of Generative AI Software for Enterprise, told TechCrunch. “It’s kind of the trifecta of things that you need to have: sovereign AI, time to first token, efficient reasoning, for the tokenomics of it all.”
However, Salesforce isn’t exactly abandoning Anthropic or OpenAI. It just announced a partnership with Anthropic called Claudeforce that allows companies to use Claude as their AI interface, while their data remains in Salesforce’s system of records, secured by its infrastructure.

### Article 239 · 2026-09-15 · finance.yahoo.com
NVIDIA, AMD and Intel Forecast: AI Stocks Eye a Rebound

Intel is a little higher in pre-market trading, but recently we've seen some noise as broad semiconductor de-risking continues to be one of the stories here. Intel itself has been a fairly successful story over the last year as the turnaround continues for the company.
AI industry leaders got crushed. Perhaps the prospect of slowing frontier model development, as thrown out there by multiple leaders in the industry, has spooked the markets. Investors immediately figured that slower data-center CapEx and semiconductor demand would be part of that. It is a little overdone. It's just a few words, but it looks like the market is trying to turn things around.
Furthermore, you have to keep in mind that interest rates being higher than anticipated has been a bit of a drag.
NVIDIA looks slightly positive in early market trading, with the market trying to reach toward the 50-day EMA. Again, this is about anxiety, with AI capital expenditures being the immediate problem. After all, if fewer data centers were to be built, NVIDIA is directly hit.
The market is looking at this in more fear-than-fact-based terms because NVIDIA's actual business numbers remain extraordinarily strong. So really, rates and the fear of a slowdown are fighting the reality of growth and economic numbers in this company that remain truly envy-worthy of most others.
AMD looks slightly positive as well. The same situation applies as with NVIDIA. The question is, will there be less demand for chips? AMD's company-specific AI story remains exceptionally strong, like NVIDIA's, and they are expecting the addressable market to be approximately $2 trillion by 2030, so demand should still be out there.
It is increasingly landing major infrastructure deployments rather than simply presenting an alternative to NVIDIA. It is becoming a true competitor. The valuation is a bit high at the moment, but it looks like we are still very much in consolidation, with $450 offering a bit of a floor.
Nasdaq, Dow and S&P 500 Forecast: Markets Await the Fed
Bitcoin Price Analysis: BTC Risks Drop to $71K if This Rounded Top Confirms
XRP Eyes Recovery to $1.55 as RLUSD Market Cap Grows by 50%
Ethereum Price Prediction: ETH Breakout Puts $3K in Focus

### Article 240 · 2026-09-15 · quantumcomputingreport.com
NVIDIA Unveils CUDA-Q Logical to Accelerate Fault-Tolerant System Orchestration Across Hardware Modalities

At IEEE Quantum Week 2026 in Toronto , NVIDIA announced a major extension to its open-source accelerated quantum computing platform with the release of CUDA-Q Logical . Sitting directly above the physical execution layer, CUDA-Q Logical introduces an extensible, retargetable compilation and orchestration framework designed to address the central bottleneck of fault-tolerant quantum computing (FTQC): co-designing high-level logical algorithms, quantum error correction (QEC) codes, real-time decoders, and physical QPU micro-architectures within a single unified pipeline.
Detailed in a research publication by NVIDIA’s quantum engineering team, CUDA-Q Logical lowers target-independent quantum programs through a virtual logical machine architecture, generating QEC microcode, physical pulse schedules, and real-time control plans while preserving semantic provenance. The platform enables direct derivation of full-stack resource estimates from actual compiler artifacts rather than abstract analytical formulas. Early deployment across national laboratories and hardware developers demonstrated dramatic design accelerations: Fermi National Accelerator Laboratory (Fermilab) reported accelerating fault-tolerant system resource modeling from five months down to three weeks—a 7× operational speedup. Simultaneously, the U.S. Department of Energy’s Sandia National Laboratories integrated its newly introduced Quantum Universal Operations Performance System (QUOPS) cross-platform utility benchmark natively within CUDA-Q.
[ NVIDIA CUDA-Q & NVQLink Q3 2026 Ecosystem Integration Matrix ]
• 1,000 Logical Qubits from 150,000 Physical Qubits
• ~10× Reduction in Physical Qubit Overhead
• Hypergraph-Product Simplex [[98,18,4]] qLDPC
• 18 Logical Qubits in 98 Data Qubits (~5.4 Physical/Logical)
• 18.4% Code Rate | 5× Savings vs. Distance-3 Surface Code
• 150-Qubit Halocene Superconducting QPU
• 3D Stacked Virtual- z Surface Code Topology
• 0.2% Two-Qubit Gate Leakage Modeled in Lattice Surgery
• Identified 60% Reduction in Logical Noise Threshold
• Unified RDMA-over-Ethernet Memory Space (CPU/GPU/QPU)
• Sub-4-Microsecond GPU-QSC Interconnect Latency
• QUOPS Metrics Baseline (arXiv:2609.12146)
• Quantinuum Helios-1 (Physical Q =1,504 | 8-Logical Q =40)
• Quantified 5-Order-of-Magnitude Gap to Utility Targets
• $150,000 Compute Grant Program
• Unified Cloud Pipeline (AWS, IBM, NVIDIA)
• Boundary Engineering in Qmio 32-Qubit Superconducting QPU
• Trapped-Ion QPUs (Forte, Tempo Series)
• IEEE QCE26 Award-Winning Research Portfolio
• 14.6% Acceleration in Synopsys FEA (35M Elements)
• 24% AI Error Reduction | Energy-to-Solution Break-Even at ~34 Qubits
• Differentiable Fourier Neural Operator (FNO)
• ~10⁷× Speedup vs. GPU Numerical Propagation Solvers
• FNO-SPMP Achieved 86.2% State Preparation Success on H₃O⁺
• Decoupled NV-Center Error Limits (Dephasing/Thermal/Leakage)
• OPM Array Medical Target: 5 mm Localization Error
The CUDA-Q Logical release coincides with rapid adoption of NVIDIA’s NVQLink low-latency interconnect protocol and GPU-accelerated quantum simulation libraries (cuQuantum, cuTensorNet, and Ising models) across the international ecosystem. By standardizing retargetable compilation layers, hardware developers can plug proprietary QPU architectures into open resource estimation toolchains without exposing trade secrets, establishing an auditable foundation for utility-scale quantum-GPU supercomputers.
Review the official announcement via NVIDIA Newsroom here , access the technical paper on NVIDIA Research here , and explore our full series of detailed architectural analyses on Quantum Computing Report by GQI :

### Article 241 · 2026-09-15 · bgr.com
Which Nvidia GPU Is Equivalent To The Meta Quest 3?

Which Nvidia GPU Is Equivalent To The Meta Quest 3?
By Aaron Greenbaum
VR gaming is a tricky proposition. On one hand, VR headsets provide an immersive experience you can't get with the best gaming monitors . On the other hand, unless you buy a standalone VR headset like the Meta Quest 3 , you might get tangled in wires while playing a game. But how much power can manufacturers fit in a device meant to slip over your eyes without weighing down your neck after several hours of use? More than you think.
The Meta Quest 3 headset is outfitted with a Snapdragon XR2 Gen 2 processor, which rivals a "Rift min-spec machine," according to Meta . As the minimum requirements to use the Oculus Rift include an Nvidia GTX 960 at 4GB, one would assume the Meta Quest 3's processor matches that GPU, but the Snapdragon XR2 Gen 2 is so unlike the Nvidia GPUs that direct comparisons are difficult.
Ask five people which Nvidia GPU they think is equivalent to the Meta Quest 3, and you'll get five different answers. Factors such as memory bandwidth, pure computational processing, and cooling all play a part in overall performance and affect the final result in different ways. Some say a GTX 1650 is a closer comparison, while others think a GTX 1060 is a more apt analogue. Some might argue that the Meta Quest 3 is only as powerful as an Nvidia GTX 750 Ti.
Normally, when you want to compare the GPUs of two different platforms, it's a prelude to comparing how games perform on the disparate devices. For instance, people might ask which Nvidia graphics card is equivalent to a Steam Machine because they want to know if "Baldur's Gate 3" will run better on a Steam Machine or their PC. This logic can provide a more accurate comparison for the Meta Quest 3's processor. If you scour the Meta Quest game catalog, a good chunk of them are Meta exclusives, but some are available on Steam, giving you a good starting point.
Titles like " VRChat ," and " Bonelab " require a minimum of a GeForce GTX 960 and 1070, respectively, but they also run on the Meta Quest 2, which is half as powerful as the Quest 3. So does that mean the Meta Quest 3 is much stronger than a GTX 960 or 1070? Yes and no. At the end of the day, a game's performance relies less on a powerful GPU and more on the optimization of its own code. Since one Meta Quest 3 has the same specs as every other Meta Quest 3 (the Meta Quest 3S notwithstanding), it's somewhat easy to ensure games run smoothly on a Quest 3.
Meanwhile, other headsets plug into PCs, which can run off a potentially infinite combination of CPUs, GPUs, RAM sticks, SSDs, and operating systems, and coding has to account for as many as possible. As such, even though a Meta Quest 3 might not have the same raw processing power as some dedicated Nvidia GTX cards, it can run games more efficiently.

### Article 242 · 2026-09-15 · finance.yahoo.com
Palantir and Nvidia Are Restricting Anthropic’s AI. Microsoft Could Win the Enterprise Trust War

Palantir and Nvidia have reportedly tightened restrictions around Anthropic's advanced AI models over data-retention concerns. Palantir has demanded irrevocable zero-data-retention guarantees before making the models available through its software, while Nvidia limits Claude to less-sensitive internal work. At Palantir Technologies Inc. (NASDAQ: PLTR ), that lands inside its sovereign-AI pitch. At Microsoft Corporation (NASDAQ: MSFT ), it creates an opening to sell customer-controlled enterprise AI.
Palantir Can Turn Distrust Into a Feature
Palantir Technologies Inc. (NASDAQ:PLTR) told investors in August that customers should retain control over their operations, data and decisions, and that proprietary information should never become training data for future models. Its September 10 sovereign-AI push with Nvidia uses Nvidia Nemotron open models and customer-controlled infrastructure. If enterprises grow wary of sending sensitive prompts to frontier labs, Palantir can sell orchestration and local control around alternative models.
There's a catch -- capability. Restricting a leading frontier model can leave customers with fewer choices or weaker performance on some tasks, while Anthropic is already addressing the concern. On September 1 it announced Enterprise Frontier Safeguards, which will store data in customer-controlled cloud infrastructure while combining that setup with zero-data-retention protections. Anthropic says the system will begin rolling out later this fall.Palantir's Q2 results were spectacular, with U.S. commercial revenue up 149%, but the trust premium still has to justify an expensive software stock. Insider Monkey tracked 86 hedge funds long PLTR in Q2 2026, down from 96 in Q1. Arrowstreet Capital increased its position 97%.
Microsoft Already Sells the Escape Hatch
Microsoft Corporation (NASDAQ:MSFT) has a cleaner monetization path. Its Sovereign Private Cloud can run large AI models in fully disconnected, customer-controlled environments, and Microsoft expanded that proposition with Mistral on July 21. Anxiety about sensitive enterprise data can push regulated customers toward Microsoft's local and sovereign stack without abandoning frontier AI.
Microsoft is not insulated from the same issue. It also offers Anthropic models across Copilot and Foundry, saying Anthropic models used in its online services, including Copilot, are excluded from some in-country processing commitments and are unavailable in certain sovereign-cloud environments, while Foundry offers Azure-hosted Claude deployments with separate data-residency controls. That makes model choice a strength, but also means Microsoft must manage the same third-party trust boundary it can sell customers an escape from.
Insider Monkey's database showed 273 hedge funds with reportable MSFT longs in Q2, down from 282 in Q1. Among large common-shareholders, Arrowstreet increased its stake 14%. Short positioning is more pointed in Palantir: 65.13 million shares were sold short as of August 31, 3.00% of float, with 2.2 days to cover.
The enterprise winner may be the company that makes model choice boring. Palantir has the sharper sovereignty narrative. Microsoft has the broader infrastructure and distribution. On this specific trust trade, MSFT is the better add and PLTR is a hold.
While we acknowledge the potential of PLTR and MSFT as investments, we believe certain other AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 243 · 2026-09-16 · NVIDIA Corporation
Emerald AI, Google and NVIDIA Launch Alliance to Advance Flexible AI Data Centers | NVIDIA Blog

The AI Energy Management Alliance brings together the full AI and power value chain to accelerate the interconnection of flexible, grid-enhancing data centers, strengthen reliability and protect affordability.
AI factories are the infrastructure of the intelligence era. Scaling them responsibly will depend as much on innovation across the grid as inside the data center.
Today, Emerald AI, Google and NVIDIA announced the launch of the AI Energy Management Alliance (AEMA), a first-of-its-kind coalition advancing data centers that can dynamically manage their electricity use in response to grid conditions.
This power flexibility can help unlock faster, larger connections for AI infrastructure while supporting the energy systems and communities that make its growth possible. Getting more watts out of existing infrastructure reduces environmental impacts per watt and supports energy affordability.
Traditional interconnection processes were designed around facilities with flat, static electricity demand. They weren’t built for computing infrastructure capable of responding intelligently when the power system is constrained.
A flexible data center can adjust its electricity drawn from the grid in several ways — shifting computing workloads, discharging storage, using paired generation or responding to system contingencies. These capabilities allow a large electricity customer to serve as a controllable resource rather than an inflexible load.
Used effectively, flexibility can make more efficient use of existing grid capacity, reduce demand during periods of system stress, and avoid or defer costly infrastructure upgrades. It can also give utilities and grid operators greater confidence to connect AI facilities on shorter timelines.
AEMA is technology-neutral and performance-based. Its focus is on the measurable service a facility can deliver — including response speed, duration, predictability and behavior during an emergency — rather than the specific hardware or software used.
Defining ride-through, curtailment and contingency-response obligations before a facility connects — meaning the alliance is setting clear rules for facilities regarding staying connected during brief grid disturbances, reducing power use when needed and responding to emergencies.
Allocating interconnection costs in a way that reflects actual system impacts and benefits, such as avoided upgrades and improved ramping capability.
These measures can reduce uncertainty for developers while giving system operators the information and control needed to preserve reliability.
AEMA convenes the full value chain across computing and power — including AI platforms, infrastructure providers, data center operators, technology companies, power producers, utilities and regional grid operators.
The founding members will be joined by launch partners from across the ecosystem. Together, AEMA will develop technical and operational approaches, collaborate with utilities on interconnection solutions and advocate for policies that recognize grid-responsive demand.
AI factories transform energy and data into intelligence. Power-flexible design gives them the potential to support the grid as they do it.
NVIDIA and Emerald AI are already working with energy and infrastructure leaders on AI factories that can respond to grid conditions in real time. AEMA will broaden that work by bringing the technology, energy and policy communities together around models that can be deployed across the U.S.
The rules governing power for AI are being written now. By creating a common framework for performance, reliability and collaboration, AEMA aims to help the U.S. build the infrastructure of intelligence at the speed and sustainability the moment demands.

### Article 244 · 2026-09-16 · NVIDIA Corporation
University of Manchester Uses NVIDIA Earth-2 to Forecast Air Pollution Across the UK | NVIDIA Blog

Manchester physicists David Topping and Hao Zhang applied NVIDIA Earth-2 generative models to air quality forecasting — unlocking predictions fast enough to inform public health.
Air pollution is a serious public health risk, contributing to an estimated 30,000 deaths in the U.K. alone last year. Data-driven insights can help — but computing air quality with traditional chemistry-based models is expensive, which limits how detailed they can be and how regularly they can be run.
David Topping, a professor in the University of Manchester’s department of Earth and environmental science, saw that the NVIDIA Earth-2 family of open AI models and tools had cracked a related problem for weather forecasting — and asked whether the same generative frameworks could work for pollution fields.
“The biggest challenge is the compute required to forecast air quality,” said Topping. “Once you put chemistry into weather models, they get really, really slow. So I said, why don’t we try using the generative frameworks that NVIDIA develops for climate and weather for pollution fields?”
Working with the NVIDIA Earth-2 team, Topping and colleagues generated training data from existing chemistry-climate simulations, then trained Earth-2 CorrDiff — a generative downscaling model — on Isambard-AI, the U.K.’s national AI supercomputer in Bristol.
The team has since added Earth-2 StormCast, a model that enables time-dependent forecasts that directly use air quality observations, and showed the test-training and inference workflows running on the NVIDIA DGX Spark personal AI supercomputer.
“To improve human health, it’s essential that we understand the impact of environmental stressors in the air we breathe,” said Topping. “Our U.K.-wide pollution model allows us to model potential future scenarios, such as predicting what would happen if different pollution-related government policy changes went into effect.
Another potential application is proactive air quality insights for healthcare organizations. Topping envisions a scenario where regional and national healthcare services could reach out to patients with conditions like asthma to let them know that air pollution is going to be high in their area tomorrow, or next week.
The team is also exploring how the air pollution model could pair with data from edge AI devices to ingest real-time air quality data and drive real-time decision making, such as in the event of a wildfire.
“The fact that this model trained in two days on Isambard-AI — and can now run on a DGX Spark sitting on a desk — changes who can do this science and how quickly,” said Niall Robinson, developer relations manager for weather and climate at NVIDIA. “We’re just at the beginning of what these open workflows can do globally.”
“The ability to switch from one NVIDIA framework to another was really impressive,” said Hao Zhang, a doctoral student at the University of Manchester who trained StormCast on Isambard-AI. “We’re only just starting to explore how to use these frameworks in different ways to model complex pollution fields.”
To retrain the Earth-2 model for air pollution, Topping and the team used a year’s worth of U.K. pollution data simulated at hourly intervals to generate a detailed, U.K.-wide pollution model at a resolution of 2-3 square kilometers.
Running on a single, eight-GPU node on Isambard-AI — the U.K.’s most powerful AI supercomputer, packed with 5,448 NVIDIA GH200 Grace Hopper Superchips delivering 21 exaflops of AI performance — the process took just two days.
“Earth-2 CorrDiff has shown an incredibly efficient use of the world-class NVIDIA hardware inside Isambard-AI,” said Simon McIntosh-Smith, director of the Bristol Centre for Supercomputing at University of Bristol and cofounder of Isambard-AI. “It’s fitting that, for a climate-based project, the GPU hours used were relatively low, requiring less power from the supercomputer to run the workloads.”
In addition to providing a look back at air pollution over the past year, the model can help predict future air pollution scenarios for the U.K. The team plans to further increase the resolution of its model by incorporating additional open data, enabling researchers to understand air pollution at street scale.
The same generative pollution workflow also runs on the NVIDIA GB10 Grace Blackwell superchip-powered DGX Spark desktop AI system for inference and smaller training runs. Topping now has an DGX Spark system in his office retraining models.
The team plans to release open source training data and workflows for the pollution models will be released so that similar models can be trained for other countries and regions.
“Our aim is to offer this workflow to the entire world,” he said. “We hope that every global country and every major city with a small burst of supercomputer AI time will be able to produce their own detailed pollution models with their own local data.”
Looking five years out, Topping sees the endpoint as something simpler still: an agentic interface where a clinician or government agency asks the question and the chain of models handles everything else.
“With better open access to air quality observations, someone could ask our pollution model running on DGX Spark: what’s the pollution going to be like in this neighborhood tomorrow?” he said. “And a whole chain of interactions will deliver an answer, grounded on the science these frameworks represent.”

### Article 245 · 2026-09-16 · NVIDIA Corporation
NVIDIA Vera Rubin NVL72 Delivers Leading Performance in MLPerf Inference v6.1 Debut | NVIDIA Blog

First preview submission using NVIDIA Vera Rubin NVL72 systems delivers up to 3.7x better throughput than NVIDIA GB300 NVL72.
System performance, efficient infrastructure scaling and continuous software optimization are key levers that determine AI inference economics. Higher system performance means more tokens generated, resulting in higher revenue. Efficient scaling means throughput grows proportionally as hardware gets added, requiring fewer resources to serve users at scale. Continuous optimization means generating more value from infrastructure investments.
Underlying all three is platform fungibility: the same infrastructure runs any model, any workload, from training to inference, recommender to reasoning, language to video, keeping utilization high.
The NVIDIA platform is purpose-built to optimize across all these, as highlighted by MLPerf Inference v6.1 results released today:
NVIDIA Vera Rubin NVL72 system debuts with leading performance : In its first MLPerf Inference preview submission, NVIDIA Vera Rubin NVL72 delivers up to 3.7x better throughput than GB300 NVL72.
NVIDIA GB300 NVL72 scales with leading efficiency : A 288-GPU submission across four GB300 NVL72 racks achieved 99% scaling efficiency, with throughput growing nearly linearly from a single-rack baseline.
Continuous software optimizations drive performance gains : Software optimizations in NVIDIA’s MLPerf Inference v6.1 submissions delivered up to 1.6x higher performance over v6.0. Optimizations continued post-v6.1 submission, delivering further performance gains.
For organizations making AI infrastructure decisions, performance, scaling efficiency and software velocity are important considerations that determine long-term inference economics.
NVIDIA submitted Vera Rubin NVL72 preview results on two of the most demanding benchmarks in the MLPerf Inference v6.1 suite: DeepSeek-R1 and Qwen3-VL.
Vera Rubin NVL72 delivers up to 3.7x higher throughput than GB300 NVL72 on Qwen3-VL across offline, server and interactive scenarios, using vLLM with the NVIDIA Dynamo open source inference framework. On DeepSeek-R1, using the NVIDIA TensorRT-LLM library, throughput is up to 2.5x higher than GB300 NVL72. These early results showcase NVIDIA’s accelerated pace of innovation and how performance will improve with continuous software optimizations.
MLPerf Inference v6.1, Closed Division. Results retrieved from www.mlcommons.org on Sep 16, 2026. NVIDIA platform results from the following entries: 6.1-0106 and 6.1-0074. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use is strictly prohibited. See www.mlcommons.org for more information.
This performance means each Vera Rubin NVL72 rack delivers significantly more tokens, serves more users and generates more revenue than a GB300 NVL72 rack, while lowering cost per token.
The results reflect full-stack codesign across hardware and software. Vera Rubin’s enhanced Tensor Cores and Transformer Engine accelerate both the prefill and decode stages of inference, while NVFP4 precision reduces memory footprint across model weights, attention and KV cache — increasing throughput with minimal loss of output quality.
Vera Rubin submissions heavily used disaggregated serving, separating prefill and decode along with large-scale expert parallelism for maximum efficiency across the mixture-of-experts layers that power models like DeepSeek-R1 and Qwen3-VL.
The NVL72 scale-up domain — powered by sixth-generation NVIDIA NVLink and NVLink Switch to deliver 10x higher packet rates and 3x lower latency than off-the-shelf Ethernet — provides the interconnect foundation that makes these techniques effective at rack scale.
This codesign extends to NVIDIA’s partner ecosystem: Nebius also submitted Vera Rubin NVL72 preview results and demonstrated excellent performance.
AI agents, which reason, plan and act across multiple steps, are reshaping how inference performance is measured. In benchmarks designed to capture this shift, such as SemiAnalysis AgentX, Vera Rubin NVL72 delivered 30 x better performance than GB300 NVL72 in preview testing. In addition, the upcoming MLPerf Endpoints benchmark will bring standardized measurement to agentic inference workloads, beyond what traditional throughput benchmarks capture.
Scaling efficiency — how effectively additional GPUs translate to throughput gains — is a key measure of AI infrastructure productivity. NVIDIA delivers this with high-bandwidth, low-latency scale-up interconnects within each rack, high-bandwidth networking between racks and efficient request orchestration across nodes.
NVIDIA’s DeepSeek-R1 (DSR1) submission scaled from a single GB300 NVL72 rack (72 GPUs) to four racks (288 GPUs), achieving 99% scaling efficiency in the offline scenario. Throughput grew nearly in proportion to the hardware added.
MLPerf Inference v6.1, Closed Division. Results retrieved from www.mlcommons.org on Sep 16, 2026. NVIDIA platform results from the following entries: 6.1-0073 and 6.1-0074. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use is strictly prohibited. See www.mlcommons.org for more information.
Scaling efficiency is key because more GPUs don’t automatically mean proportionally more throughput. If adding nearly double the GPU count delivered only a single-digit percentage improvement in throughput, the infrastructure cost would far outpace the performance return. The architecture, interconnect and software must all scale together.
GB300 NVL72 also demonstrated rack-scale efficiency on the WAN 2.2 text-to-video benchmark, reaching 0.65 720p videos per second at 5.7 seconds per video — 9x higher throughput and 7.5x lower latency than a single node.
In v6.1, GB300 NVL72 performance on Qwen3-VL improved up to 1.6x over v6.0 results. The gains came through lower KV cache precision, additional kernel fusion, better kernels and disaggregated serving with vLLM and NVIDIA Dynamo.
Software optimization continued past the v6.1 submission deadline as well. Post-submission results, not yet verified by MLCommons, on GPT-OSS-120B and DLRMv3 show further performance gains.
Beyond the NVIDIA Grace Blackwell and Vera Rubin NVL72 platform results, NVIDIA submitted Jetson AGX Thor results using NVIDIA TensorRT Edge-LLM on the newly introduced Edge-Agentic benchmark with Qwen3.6-27B .
The NVIDIA partner ecosystem participated broadly, with 19 partners — eight of them on multi-node Blackwell NVL72 systems — demonstrating excellent performance. This includes ASUS, Azure, Cisco, CoreWeave, Crusoe, Dell Technologies, Fujitsu, Giga Computing, HPE, Inventec, Lambda, MiTAC Computing, Nebius, Oracle Cloud Infrastructure, Quanta Cloud Technology, Red Hat, ScitiX, Supermicro and Wiwynn .
From compact edge devices to the largest AI factories, NVIDIA continues to advance performance across the full technology stack with an annual cadence of platform architectures, continuously improving software and an ecosystem built to deliver it at scale.

### Article 246 · 2026-09-16 · scmp.com
Huawei unveils latest tech to boost AI power, curb China’s Nvidia reliance

Huawei unveils latest tech to boost AI power in push to break China’s Nvidia reliance
Its SuperPoD will face off against offerings by US rivals in the global computing power arena, including Nvidia’s NVL system
Huawei Technologies on Thursday unveiled its latest Atlas 960 SuperPoD computing cluster and an upgraded version of its UnifiedBus interconnect technology, key components of the Chinese tech giant’s strategy to build advanced artificial intelligence systems despite US semiconductor-related restrictions.
At the Huawei Connect 2026 conference in Shanghai, the Shenzhen-based firm introduced near-packaged optics (NPOs) – a placement structure enabling higher speeds and lower energy use – to the company’s SuperPoD architecture for the first time.
Huawei said the combination of its UnifiedBus interconnect technology and Hi-ONE optical system would allow a SuperPoD to connect as many as 4,000 processors, extending high-speed optical connections deeper into the computing system.

### Article 247 · 2026-09-16 · trefis.com
How Far Can NVIDIA Stock Fall In A Demand Scare?

How Far Can NVIDIA Stock Fall In A Demand Scare?
NVIDIA (NVDA) stock trades near $212, about 10% below its 52-week high, and it has gone nowhere over the past three months. The company itself has not been standing still. So it is worth asking the uncomfortable question: how far does a stock like this fall when a real shock arrives, and how long would you wait to get it back?
Why Is NVIDIA Stock Flat While Revenue Climbs?
Two things changed in late August. The first is cost. Memory prices have risen by more than NVIDIA expected, and management calls the pricing conditions extreme. Gross margin was 75% in fiscal Q2 2027, and management now guides it to a bottom at 71% to 72% in fiscal Q4 2027 before settling at 72% to 73% in fiscal 2028.
The second is who funds the demand. NVIDIA has put nearly $50 billion into the Frontier AI labs and lined up six infrastructure capital firms to raise over $500 billion of outside money. On some NeoCloud capacity, it now guarantees a floor of revenue and takes a share of the rent above it. Management knows some people call that circular financing .
Is NVIDIA A Worse Business At A Thinner Margin?
On the numbers, no. Revenue over the trailing twelve months is $302.97 billion, up 83.4% from a year earlier. That is slower than the 116.5% the company averaged over the past three years, and the trailing figure is the one that counts here, because it covers the most recent year rather than a three-year stretch. Management ties the margin reset to component costs, not to demand.
Vera Rubin shipments started in August 2026, and management expects that platform to be about 20% of data center revenue in fiscal Q3 2027. So the business is not weakening. It is getting more expensive to run, and NVIDIA now helps fund more of the demand behind it.
How Far Does NVIDIA Fall When A Shock Arrives?
NVIDIA fell an average of 28% peak to trough across the 15 market shocks it has traded through since 2007, while the S&P 500 fell 16%. The deepest was the 2008-2009 financial crisis, an 84% fall against 53% for the index.
Growth and demand scares have cost NVIDIA 36% on average, worse than the 28% it averages across all shocks. Those scares are the shape of the risk in front of it now. In the financial crisis, that 84% fall on a position worth a tenth of your portfolio would have taken about 8% off everything you own and about 17% at a fifth.
The recovery record is kinder. Of the shocks NVIDIA has recovered from, the median wait from the low back to the pre-shock high was about a month. The 2008-2009 crisis is the exception: about 88 months from the low. So the profile is a stock that falls hard and usually repairs fast, with one precedent where the repair took years.
Is Your NVIDIA Position Sized For Its Own History?
That question is easy to answer in a calm week. The honest version depends on what else you own and on whether you would need the money before it came back. Would you be adding at the low or selling into it?
Almost nobody settles position size one holding at a time. Our rule-based Trefis High Quality Portfolio does that weighing for you, holding by holding.
Or if you would rather compare how far names like this fall, start with our Drawdown Defenders screen . A stock that repairs quickly still has to be held while it falls. That portfolio has a track record of outpacing the three major indices.

### Article 248 · 2026-09-16 · fool.com
More Than a Quarter of Nvidia's Revenue Now Comes From Customers Based in Taiwan. Should Investors Be Worried?

When investors think about who buys Nvidia's (NASDAQ:NVDA) chips, the names that come to mind tend to be American: the giant cloud platforms and the labs building artificial intelligence (AI) models. The company's latest quarterly filing offers a different answer.
During the fiscal second quarter of 2027 (the period ended July 26), $27.0 billion of Nvidia's revenue was billed to customers headquartered in Taiwan. That's 28% of the quarter's $96.2 billion total.
The line is climbing fast, too. A year earlier, it was $8.9 billion, or about 19% of revenue. Three months before the latest quarter, it was about $12 billion, or roughly 15%. So the dollar figure tripled in a year and more than doubled in a quarter -- far faster than the business as a whole grew.
An investor could see that and worry the growth story has quietly moved somewhere unexpected. The stock sits near $212 as of this writing, down about 10% from its 52-week high.
But I think the disclosure is more useful than alarming. It shows who Nvidia bills -- and why that group isn't the same thing as demand.
A $27 billion line item
Nvidia sorts revenue by geography using the headquarters location of the direct customers it bills. On that basis, the United States led the fiscal second quarter at $60.1 billion, or about 62% of revenue. Taiwan came second at $27.0 billion. China, including Hong Kong, contributed $7.9 billion, and the rest of the world combined for just $1.3 billion. Altogether, customers headquartered outside the U.S. accounted for 38% of the quarter's revenue, against 30% a year earlier.
The quarter those numbers sit inside was itself enormous. Companywide revenue totaled $96.2 billion, up 106% year over year, and about 92% of it came from the data center business.
In other words, Taiwan wasn't just growing with the company. It was gaining share of a total that itself doubled.
Who is actually buying?
Nvidia's direct customers (the buyers it invoices) include distributors, companies that build graphics cards and servers, cloud service providers, AI model makers, and system integrators. And the company notes that the end customer and the shipping location may be different from the direct customer's headquarters.
Taiwan happens to be the home base of much of the industry that turns Nvidia's chips into finished AI servers. Nvidia's own annual filing names Taiwan-based Hon Hai Precision Industry , better known as Foxconn, among the contract manufacturers that assemble, test, and package its final products.
Much of the revenue billed to Taiwan, then, is likely hardware passing through intermediaries on its way to data centers somewhere else.
In other words, the Taiwan line doesn't say Taiwanese demand for AI chips tripled. It more likely says that as Nvidia's newest products (full server racks, not just chips) ramped up, more orders routed through the island's system builders before reaching the cloud providers, AI model makers, and other end users Nvidia calls its indirect customers.
Read the table that way, and it becomes a measure of how much of Nvidia's revenue lands with just a few direct customers. One direct customer accounted for 16% of Nvidia's total revenue in the quarter -- about $15 billion billed to a single buyer.
That shape isn't new, either. In the same quarter a year earlier, two direct customers represented 23% and 16% of revenue. Of course, the names behind the percentages can shift as orders route differently. But a few enormous buyers of record have carried the company for a while.
Further, the same island shows up on the other side of the business. Nvidia's annual filing names Taiwan Semiconductor Manufacturing among the foundries that produce its semiconductor wafers.
So Taiwan sits on both sides of Nvidia's business. Much of the manufacturing happens there, and more than a quarter of revenue is billed there. Any disruption to the island's role (geopolitical or otherwise) would touch both sides at once.
Demand itself is better judged elsewhere. Management's forecast for the fiscal third quarter, now underway, is $108.0 billion of revenue -- and growth like that is ultimately a claim about what customers keep spending.
The geography table can't tell you whether they will. Paired with the concentration disclosure, it tells you how few names of substantial size are on the invoices. That concentration, I'd argue, is the finding worth taking from the filing.

### Article 249 · 2026-09-16 · tomshardware.com
Developer vibe codes a tool to let Nvidia RTX 50-series laptop owners crank up their power limits — can juice RTX 5090 mobile GPU to 225W

Developer vibe codes a tool to let Nvidia RTX 50-series laptop owners crank up their power limits — can juice RTX 5090 mobile GPU to 225W
By Zak Killian
The tool appears to be fully vibe-coded and highly experimental, but it does seem to work on at least some laptops.
Folks with Nvidia-based gaming laptops can now use a new tool called NvpwrControl to unlock additional performance from their assuredly power-limited mobile GPU, as long as they're willing to accept the risks of cranking their GPU power limit by as much as 40 watts. The tool, spotted by VideoCardz , is available for download on GitHub , and it is labeled as 'experimental', so you'll want to be very sure you're willing to damage the reliability, if not the lifespan, of your fancy discrete GPU gaming laptop before using it.
If you've ever had a gaming laptop, you will know that the GPU model name can be deeply misleading. Whether it's NVIDIA using wildly different GPU configurations , AMD using confusing suffixes that don't exist in desktop GPUs , or Intel naming integrated graphics like a discrete GPU , all three vendors do things to keep the user guessing why their new gaming laptop isn't as fast as expected based on the name alone.
NVIDIA GeForce RTX 50 Series Laptop GPU Power Limits
GPU Power (varies per laptop)
GeForce RTX 5050 Laptop
GeForce RTX 5060 Laptop
GeForce RTX 5070 Laptop
GeForce RTX 5070 Ti Laptop
GeForce RTX 5080 Laptop
GeForce RTX 5090 Laptop
In Nvidia's case, the GPU models ( aside from the RTX 30 Series ) don't match at all between laptop and desktop, but even with the smaller size of the laptop GPUs, the chips are still sharply limited in performance by their stringent power limits. These limits top out at 150W, with an extra jolt, usually 25W, available from Dynamic Boost if the CPU isn't heavily loaded. This is, frankly put, not enough power for even the mobile GeForce RTX 5070 Ti to stretch its legs, to say nothing of the GeForce RTX 5080 Laptop or GeForce RTX 5090 Laptop. In high-intensity gaming situations, these GPUs can score pretty similarly due to having the same power limit.
That's what makes this tool attractive. By cranking the power limit, you can give these power-limited GPUs a performance boost. The developer doesn't provide any benchmarks , but I can say from experience that testing power limit adjustments on a power-limited GPU can give nearly linear performance gains, meaning that increasing the power limit from a stock 140W all the way up to 180W could potentially give a GPU performance uplift in the neighborhood of 25% or more, although it is impossible to verify this without testing.
There are quite a few caveats to this utility, though. For one thing, even the author describes it as 'experimental ', and for another thing, it's clearly AI-generated in the largest part. The developer is called "LevinAI", after all, and there are the hallmarks of generative AI all over the GitHub repository. Still, there are a few reports on both GitHub and Reddit suggesting that users have been testing it, and the developer claims that it works on his GeForce RTX 5070 Ti laptop, posting the proof below.
Other notable qualifiers include that it only supports Blackwell GPUs for now, and it only enables power controls when it can recognize the power policy layout and OEM baseline. If your GPU already ships with a wacky power configuration, this tool may not work for you. It's also not verified to work on every brand of laptop nor every model of GeForce RTX 50-series GPU, so we absolutely wouldn't try this unless you're willing to replace your Blackwell-based laptop.
The partially AI-generated project description (likely chosen as the author's native language appears to be Russian) explains that the developer investigated numerous layers of the software stack on top of the GPU to see where the power limit could be modified. The controls that NVIDIA exposes generally won't let the user raise the power limit above the value set by the OEM for fear of potentially damaging the hardware, since the power delivery and cooling mechanisms were likely not designed with the higher power draw and thermal output in mind.
The solution he found was apparently to modify a low-level NVIDIA power policy that isn't normally exposed to end-users. He says, "One of the important findings was that the power-management chain contains internal policy values that are not exposed through the normal consumer power-limit controls. This is the path that eventually led to a working experimental implementation." However, due to the method employed, the tool does require the user to disable Windows driver signature verification, which is yet another 'gotcha' of the mod.
As amusing as it is to see that the developer left his AI assistant's instructions for constructing his GitHub repository (which he didn't follow), it's a reminder both of the reliability concerns around "vibe"-coded software in production as well as of the incredible potential of AI software development. Since we spotted the story on this utility, the developer has already bumped the version from 1.5.0 to 1.8.0 with a new release on GitHub, suggesting that the pace of improvements is extremely rapid.
A few users on Reddit, where the author posted the above screenshot, lambasted the developer for taking ownership of what they claim is "100% AI generated work" and also for not structuring his code repository correctly (since all of the source is packed in a ZIP file, not properly viewable on GitHub). However, the majority of other users seem enthusiastic about his work, and several have already posted proof that it seems to work, with huge gains in 3DMark and other benchmarks.
Zak is a freelance contributor to Tom's Hardware with decades of PC benchmarking experience who has also written for HotHardware and The Tech Report. A modern-day Renaissance man, he may not be an expert on anything, but he knows just a little about nearly everything.
This is quite cool because if you look at some of the Power->Performance graphs for the RTX 5000 series GPUs they show that the GPUs are limited by their power envelope
Many laptop modders have made serious gains by increasing their laptops power limits by shunt modding them. This might be a safer option to soldering resistors onto your PCB
GPUs they show that the GPUs are limited by their power envelope
Well, therin lies the problem. In an already insufficient thermal space like a laptop, and which often have limited cooling, this will not turn out nice. No amount of cooling pads, or thermal paste will be able to offload the heat. The fans in a low to midrange gaming laptop will be very loud. Maybe on the most expensive laptops, with extreme cooling, this could be of benefit, but even then those systems will run very hot.
In an already insufficient thermal space like a laptop, and which often have limited cooling, this will not turn out nice. No amount of cooling pads, or thermal paste will be able to offload the heat.
https://i.kym-cdn.com/photos/images/newsfeed/000/966/457/29e.jpgJust destroy my laptop, fam
30 minute battery time, and melted case.
Boy developed “toasted skin” condition from using a laptop every day
Nuts! Okay, to the discerning tech enthusiast, it kinda looks obvious. He must have been resting the underneath of the laptop on his belly. The marks resemble the underneath of a gaming laptop grill/intake. I have a very similar pattern on my HP Omen 15. The rare occasions I do have the laptop in a similar position, I use a padded tray. DOH!
So what I am hearing is we take a whole bunch of laptop 5090 motherboards out of their chassis, unlock the power limits, and put them in racks. Something something AI. Profit?
Saying "Developer vibe codes a tool" is like saying "Musician AI generates a song".
Except the recursive self-improving vibe coder bots will inherit the Earth.

### Article 250 · 2026-09-16 · cnbc.com
Snap tries to bring AR glasses to enterprise market, partnering with Nvidia, AWS and Salesforce

Snap is partnering with Nvidia, Amazon Web Services and Salesforce as part of an enterprise sales push centered on its $2,000 Specs augmented reality glasses.
"With Nvidia, they've got an open-source XR AI platform that a number of businesses are already building on top of," Snap CEO Evan Spiegel said.
Snap is partnering with Nvidia , Amazon Web Services and Salesforce as part of an effort to bring its $2,000 Specs augmented reality glasses to the enterprise market.
Evan Spiegel, Snap's CEO, characterized the initiative as tied to the company's broader effort to help people "understand that Specs is a computer, not a pair of smart glasses for taking photos."
When Snap revealed the Specs AR glasses in June, with a $2,195 price tag and $200 refundable deposit, the company pitched the device as catering to the public instead of developers. Although AR and related virtual reality technologies have improved over the years, devices like Microsoft's HoloLens and Meta's Quest-branded VR headsets have failed to become breakout hits .
Spiegel said the bulkiness of those older devices were a major hindrance, and said his company's Specs AR glasses will be better suited for tasks like helping field technicians troubleshoot equipment problems by viewing digital instructions, and interacting with workers.
To date, Snap's success has been in the consumer market. The company is hoping that a partnership with the likes of Nvidia can change that.
"They've got an open-source XR AI platform that a number of businesses are already building on top of," Spiegel said. "The goal with both Salesforce and Nvidia is to make it really easy for businesses to get the benefits of those agentic platforms."
Snap is also debuting a consumer-oriented AI service dubbed Specs Intelligence that's like a digital assistant that can do tasks across the AR glasses as well as iPhones and Mac computers. Spiegel said the company hasn't determined specific pricing details yet, but it will include a free tier and "different price points" depending on usage.
The company's latest AI-related foray comes as debate heats up in the broader technology market about safety , and whether foundation model leaders like Anthropic and OpenAI should slow the pace of development.
Spiegel said, "these are concerns that have been raised for a long time."
"It's really important that we coordinate an international and thoughtful response," Spiegel said. "It's really important that regulators and policymakers consider actual potential harms rather than imagined harms, and so that's why I think it's going to be really important for a thoughtful and international group to really get together on this."

### Article 251 · 2026-09-16 · macrumors.com
Apple May Return to Server Market With Nvidia Technology

Apple is considering offering an AI server built around "M8" series chips and has discussed incorporating Nvidia networking hardware, The Information reports.
The system would be sold to outside customers, potentially bringing Apple back into a business it left behind when it discontinued Xserve in 2011. Apple is reportedly targeting companies that want to run AI models on their own equipment, with a particular focus on inference and generating responses from trained models.
One option under consideration is Nvidia's NVLink Fusion, which provides hardware and software for exchanging data between chips. Apple could use the platform to link its M8 processors, although neither the Nvidia arrangement nor the server itself is finalized. The report places a potential release date in 2029, but it could be canceled before then.
Apple CEO John Ternus reportedly supported the initiative when work on it began approximately a year ago, during his tenure as the company's hardware engineering chief. The project follows growing interest in Apple hardware among AI businesses , which have been buying Mac mini and Mac Studio systems in large quantities.
Apple already produces server hardware for Private Cloud Compute, the infrastructure that handles Apple Intelligence tasks requiring processing beyond a user's device. According to the report, scaling Apple's existing connections between chips would present cost and speed problems, which is why it is considering Nvidia's technology. Apple has also declined partners' requests to use those Private Cloud Compute servers.
An agreement would give Nvidia a role in an Apple product that could compete with its own AI systems. NVLink Fusion allows Nvidia to supply networking technology to companies building alternative processors, expanding its business beyond customers using Nvidia chips.
The discussions also suggest a closer working relationship between Apple and Nvidia following their longstanding disputes. Apple has already announced plans to extend Private Cloud Compute to Google Cloud using Nvidia GPUs . The companies have reportedly explored additional ways to work together on AI, including the use of Nvidia's open-source models.
The project still faces challenges beyond developing the hardware. There is still said to be a need for stronger support for business customers and more software resources for AI developers, including further investment in its MLX framework.
Developers are questioning whether a settlement of the U.S. government's antitrust case against Apple would meaningfully loosen the company's control over the iPhone, according to The Information.
The report highlights PayPal and Epic Games among the companies that have raised concerns with the Department of Justice (DOJ). Officials have reportedly indicated that they favor a negotiated...
Some iPhone Duos are already experiencing hinge issues that cause display cracks, based on photos shared on Reddit and the MacRumors forums. Almost all of the display faults are right along the hinge, and most result in a line of bright pixels across one side of the screen.
Apple Music has a 404 page easter egg on the web: a functional iPod that appears when you load a page that does not exist, such as music.apple.com/macrumors.
Apple is clever with this. If you navigate to music.apple.com/ipod instead, the page says "Looking for something?" instead of "Page Not Found."
Apple silicon is cost, energy and space efficient for inference. They are already filling a prosumers gap that's no contested by nvidia.
That's where all the rage and money is, these days. I still think they're at their best when they innovate in the consumer/prosumer space though.
xserve was great, super reliable and the OS was a breath of fresh air compared to linux. Especially now where local AI is critically important for businesses (not trying to have your corporate secrets leak out), it only makes sense that Apple's chips with their amazing efficiency AND power should be a big player in the space.
Right now Apple has zero server rackable computers so even if we wanted to use Studios it costs $500 (yes you read that right) for a garbage plastic rack mount for the studios.
Our comprehensive guide highlighting every major new addition in iOS 27, plus how-tos that walk you through using the new features.
Whether you're upgrading from an older iPhone or completely new to Apple, this guide will help you get the most out your new device.
MacRumors attracts a broad audience of both consumers and professionals interested in the latest technologies and products. We also boast an active community focused on purchasing decisions and technical aspects of the iPhone, iPad, Mac, and other Apple platforms.

### Article 252 · 2026-09-16 · greenpeace.org
NVIDIA’s AI climate hoax report

Dive deep into research, investigations, and reports from our campaigns to protect people and the environment.
NVIDIA claims AI will solve the climate crisis, but its hidden emissions surged 725% since 2020. Uncover the greenwashing tactics behind AI’s massive emission growth.
Greenpeace report on the unprecedented territory grab in the Deep sea mining industry.
We are here to dismantle the machinery of destruction and build something beautiful in its place.
New report from Greenpeace and ocean communities: Global Ocean Justice Now Making the case for a human rights-based approach to marine conservation
Testing commissioned by Greenpeace International in 2025 found plastic particles in the baby food products of two global consumer goods companies – Danone and Nestlé.
This global research – the first of its kind – shows that we can power an ambitious energy transition without sacrificing crucial ecosystems – whether on land or at sea.
Equity, Benefit-Sharing and Financial Architecture in the International Seabed Area
A new independent study commissioned by Greenpeace International, reveals that current International Seabed Authority proposals would return virtually nothing to developing countries
Greenpeace International’s analysis of 24 research papers in peer-reviewed scientific journals found that the plastics we use to package our food are exposing us to health risks – and none more so than heated ready meals and takeaways.
Economic Potential of Seabed Nodules in the Cook Islands
The economic potential of seabed polymetallic nodules in the South Pacific’s Cook Islands has been overstated, according to a new independent study commissioned by Greenpeace International.
