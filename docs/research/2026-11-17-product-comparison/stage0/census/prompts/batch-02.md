# Blind reader, matter census batch 2 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 35 articles (numbers 36 to 70,
2026-09-08 to 2026-09-10, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 36 · 2026-09-08 · fool.com
3 Things Bears Have Wrong About Nvidia Right Now

There's no shortage of naysayers when it comes to Nvidia ( NVDA +2.55% ) . Just 1.18% of its outstanding shares are currently being shorted, but think about what that means for a company with a market cap just above $5.5 trillion.
There are nearly $57 billion in short positions out there, and that doesn't include put options, bearish ETFs, or other derivative activity. The actual number of shares sold short has actually increased 40% over the past year, and the value of those bearish wagers has risen another 35% on top of that.
The bears are everywhere, but I see that as more of an opportunity than a threat. Let's go over some of the knocks on Nvidia. I want to counter by pointing out what the worrywarts might be missing.
1. Nvidia is priced for perfection
There is nothing that I love more than when a bear argues that a stock is "priced for perfection." The assumption is that current expectations are too high and that the stock is bumping up against the ceiling, with so much air below it on the way down to the floor.
Last month's fiscal second quarter was a perfect example of Nvidia stock perpetually scaling the wall of worry. Bears were banking on analysts aiming too high by targeting 97% in top-line growth. It would be the fourth consecutive quarter of accelerating year-over-year growth.
How is that possible with a company as large as Nvidia? Expectations were high . Reality was kinder. Here's a look at the company's top-line growth:
The late-August financial update gets even better. Those same analysts tagged by bears as overly ambitious are serial lowballers. They projected revenue would decelerate sharply to just 45% for fiscal year 2028, which starts in February. Nvidia shattered those crystal balls two weeks ago by forecasting 70% growth for next year.
Perfection isn't the ceiling. Market winners thrive in the debunking process.
2. Rivals will gain market share at Nvidia's expense
It would be naive for a bull like me to assume that Nvidia will be the king of the hill forever. Competitive advantages can weaken over time, just as they have been strengthening for years. A disruptor can pioneer a better mousetrap for the AI revolution or whatever giant tech trend comes next.
The one thing that's fair to say is that it's not happening now . Let's have Advanced Micro Devices ( AMD +3.09% ) enter the chat. AMD has a colorful history of needling the market leader, and it's certainly cashing in on the AI boom Nvidia is championing.
AMD stock has outperformed Nvidia over the past year by more than tripling. However, in its latest quarter -- and I'll point out that their fiscal quarters ended about a month apart -- AMD's overall revenue rose just 50%, half of Nvidia's top-line growth.
I'll beat the bears to what they're thinking. Zoom in on AMD's data center business, which now accounts for more than half (58%) of its revenue, and that business skyrocketed 107% for the quarter. That's awesome, but Nvidia's data center revenue, which accounts for 93% of its results, soared 117%.
In the end, AMD's data center business delivered $3.5 billion in incremental revenue compared to a year earlier. Nvidia tacked on $48 billion in incremental data center revenue.
3. Margins will inevitably contract
Let's close on a margin of error. Nvidia's gross margin was 75% in its latest quarter. The adjusted net margin was a jaw-dropping 56%. It's easy to question the sustainability of those levels. Unlike the flawed "priced for perfection" argument, there is a clear ceiling here: Gross margin will never exceed 100%, and the after-tax adjusted bottom line will naturally be well below that.
The reasonable bear case is that growth may continue but decelerate. Margins will contract, so earnings will grow even slower than the slowing top line -- if not eventually turn into negative year-over-year earnings growth.
Set aside that high bandwidth memory (HBM) makers riding Nvidia's coattails are currently generating gross margins approaching 85%. With competition percolating, Nvidia will need to keep innovating and fortifying its moat. It probably has more pricing flexibility now than the bears think. With third-party HBM becoming a larger cost component in the AI build-out, won't it make it even riskier for a company to bank on non-Nvidia AI chips and accelerators?
In the meantime, you can buy the stock for less than 15 times next year's projected earnings. This is why the bears aren't arguing that Nvidia is too expensive, as it's trading at a discount to the overall market despite growing substantially faster. Nvidia will be volatile, but it's built to win.
By Rick Munarriz – Sep 8, 2026 at 11:52AM EST
Nvidia has its haters, an odd look for a stock with revenue more than doubling in its latest quarter and a forward earnings multiple in the teens.

### Article 37 · 2026-09-08 · uk.finance.yahoo.com
New ChatGPT is world’s first human-level AI, says Nvidia boss

Nvidia CEO Jensen Huang has claimed that the latest version of ChatGPT marks the first instance of artificial general intelligence (AGI), or human-level AI .
OpenAI's GPT-6 model, known as ChatGPT Astra, launched last week with impressive results in benchmark tests that appeared to set it apart from its rivals like Anthropic's Claude and Google's Gemini.
OpenAI said it was "state-of-the-art on computer use, browsing, software engineering, cyber security, science and professional work", capable of autonomously completing multiple tasks at once.
In a demonstration, the new AI model handled user requests while simultaneously performing complex tasks like creating a video game or preparing a legal document.
Following its unveiling, Mr Huang wrote in a post to X : "AGI has arrived. Congratulations OpenAI team."
The exact definition of AGI is contested among industry figures, though according to OpenAI's charter it involves "highly autonomous systems that outperforms humans at most economically valuable work".
In a press call to unveil the latest version of ChatGPT, OpenAI president Greg Brockman said "welcome to the AGI era", describing the new model as a "generational leap in capability".
He added: "If we fast forward a couple years, and we look back and say when was it really that AGI was created, I think it's going to be about this time, and I think it might be about this model."
His claims came just days after OpenAI CEO Sam Altman said that AGI was "at best... a very poorly defined term".
Speaking on the Sources podcast, he said: "I was going to say it's like an irrelevant marketing term."
In independent benchmark tests that aim to measure how close an AI model is to AGI, ChatGPT Astra set new high scores that closely matched human scores.
Greg Kamradt, from the ARC Prize Foundation that develops the tests, described it as a "meaningful step change in frontier-model performance".
Despite this, some industry figures remain sceptical of labeling any current AI models as human-level.
In response to Mr Huang's comments, tech consultant Marko Tasic disputed his claims, describing it as a marketing stunt ahead of a potential initial public offering (IPO).
"No, it's not AGI," he said. "This is just PR before IPO. Pump and dump, nothing more."

### Article 38 · 2026-09-08 · qz.com
Jim Cramer picks Nvidia and Broadcom as OpenAI GPT-6 Astra winners

Cramer pointed to Nvidia's role training the model and Broadcom's custom chip partnership with OpenAI as reasons to buy both stocks
CNBC's Jim Cramer identified Nvidia $NVDA and Broadcom $AVGO as the two stocks most likely to benefit from OpenAI's release of its GPT-6 Astra model, speaking Tuesday on CNBC's Morning Meeting.
Cramer said Nvidia deserves credit for making Astra possible. Training Astra required 100,000 Nvidia Blackwell GPUs, according to Jensen Huang, and the model — which rolled out in stages starting last week — has drawn notice for what OpenAI says are breakthroughs in cybersecurity and computer-use tasks. Huang's post on X $TWTR noted that a further 400,000 GPUs are being brought online for OpenAI, a figure that points to rapidly expanding demand for Nvidia 's hardware. Nvidia stock opened higher Tuesday before falling 2%.
"The stock that I think you should be buying is Nvidia ," Cramer said. "It didn't do anything wrong at all. If anything, it's doing the right thing — it's the reason why OpenAI is doing so well."
Broadcom benefits through a different channel. The company worked with OpenAI to develop a custom chip called Jalapeno, designed for inference — the day-to-day running of AI models rather than training. Because Astra's strong reception reinforces OpenAI's standing in the AI race, Cramer argued it also strengthens confidence in Broadcom 's custom silicon business. Broadcom stock was up 2.5% on Tuesday.
"If they accomplish that, Broadcom is their preferred partner, and we're going to see a stock that goes up much more," Cramer said, referring to OpenAI and Anthropic completing planned initial public offerings.
Broadcom counts both OpenAI and Anthropic as custom chip customers. According to Broadcom CEO Hock Tan, Anthropic will claim the top spot among Broadcom 's custom chip clients in fiscal 2027 and retain it through fiscal 2028, with OpenAI expected to move into second position that same year. Cramer's charitable trust holds positions in both Nvidia and Broadcom .
Cramer said investor sentiment around both chipmakers is tied to OpenAI's competitive position against rivals including Anthropic and open-source alternatives. Because OpenAI has pledged enormous sums to computing infrastructure, investors are closely watching whether it can keep pace at the leading edge of AI research, viewing that competitive position as central to the company's ability to sustain itself ahead of a possible 2027 IPO.
Cramer's portfolio also includes Intel $INTC and Micron $MU alongside Nvidia and Broadcom . Cramer argued that demand across the AI chip industry is broad enough that several companies can thrive simultaneously, with no single firm destined to take all the business.

### Article 39 · 2026-09-08 · tradingview.com
Why Nvidia stock is down over 1% today even as AI peers are surging

/ Why Nvidia stock is down over 1% today even as AI peers are surging
Why Nvidia stock is down over 1% today even as AI peers are surging
Nvidia stock fell about 1.5% on Tuesday to around $227, taking a breather after three consecutive sessions of gains as broader markets came under pressure from rising oil prices and renewed Middle East tensions.
The pullback was notable because several major semiconductor stocks moved higher.
Intel surged more than 8% after Northland Capital Markets analyst Gus Richard upgraded the stock to Outperform from Market Perform.
AMD gained about 5%, while Broadcom rose roughly 3%. The PHLX Semiconductor Sector index was also up around 2%.
The broader market moved in the opposite direction. The Dow Jones Industrial Average fell 574 points, or 1.1%, while the S&P 500 declined 0.4% and the Nasdaq Composite slipped 0.3%.
US markets were closed on Monday for the Labor Day holiday.
Oil prices remained a key source of pressure for equities on Tuesday as West Texas Intermediate crude futures rose for a sixth consecutive session, extending their longest winning streak since March.
Brent crude was trading around $98 a barrel as tensions between the US and Iran escalated over the weekend.
Against that backdrop, Nvidia’s decline comes after a strong run over recent months.
The stock is up about 24% over the past six months and remains just below its record high of $236.54.
However, Nvidia has significantly underperformed some semiconductor peers over the same period, with both AMD and Intel gaining more than 100%.
Cantor maintains $350 Nvidia target
Cantor Fitzgerald reiterated its Overweight rating on Nvidia and maintained a $350 price target.
The firm highlighted continued demand for AI infrastructure while acknowledging supply constraints across the semiconductor industry.
Analyst C.J. Muse said investors remain divided over the durability of the AI investment cycle as macroeconomic and debt concerns weigh on markets.
Cantor also emphasized Nvidia’s position as TSMC’s largest customer and argued that the stock trades at the cheapest valuation among compute companies based on calendar 2028 earnings estimates.
The firm also believes Nvidia remains under-owned by both hedge funds and long-only investors.
Muse addressed Nvidia’s high-bandwidth memory specifications, characterizing HBM de-specification as an economic decision aimed at optimizing gross margins and GPU sales around a finite number of bits.
Earlier this month, Morningstar raised its fair value estimate to $310 from $280, implying roughly 30% upside from the stock’s current level.
Nvidia reported $96 billion in fiscal second-quarter revenue, up 106% from a year earlier and above its $91 billion guidance.
The company expects October-quarter revenue of $108 billion, ahead of FactSet consensus of $105 billion.
Morningstar identified Nvidia’s fiscal 2028 outlook as the most significant part of the earnings report.
Nvidia expects revenue growth of 70% next year, implying nearly $700 billion in total revenue compared with Morningstar and FactSet estimates of roughly $570 billion.
The outlook reinforces the longer-term bullish case, even as Nvidia’s shares pause after their recent gains.

### Article 40 · 2026-09-08 · fool.com
Nvidia Earnings Blow Everyone Away

In this episode of Motley Fool Hidden Gems Investing , Motley Fool contributors Tyler Crowe, Matt Frankel, and Jon Quast discuss:
Nvidia's earnings and guidance update.
The winners and losers from Nvidia's earnings.
CrowdStrike's earnings.
Is CrowdStrike's stock a buy?
Mailbag: Is local AI a hyperscaler problem?
To catch full episodes of all The Motley Fool's free podcasts, check out our podcast center . When you're ready to invest, check out this top 10 list of stocks to buy .
A full transcript is below.
This podcast was recorded on Aug. 27, 2026.
Tyler Crowe: Woah boy, did Nvidia 's earnings deliver. Motley Fool Hidden Gems Investing starts now. Welcome to Motley Fool Hidden Gems Investing . I'm your host, Tyler Crowe. Today, I'm joined by longtime Fool contributors Matt Frankel and Jon Quast. Guys, I think this has been the thing we've all been waiting for this week. It was Nvidia's earnings report. It came out after the close yesterday. Probably the most anticipated earnings report, even more so than the hyperscalers. I think it's fair to say that the report did not disappoint. Shares are up about 7% as we're taping this morning. Somehow, the company smashed earnings expectations and guidance expectations, which at this point, I'm starting to think Nvidia is arguably the most followed company on Wall Street. If the company can blast past expectations like this, I almost start to wonder, are Wall Street analysts not really good at their jobs, or was it just an incredible quarter here?
Jon Quast: Maybe both. Not all Wall Street analysts, but maybe some, but this is just an incredible quarter. It's every investor's birthday today with Nvidia. You look at the largest company in the world reporting 106% revenue growth at some scrappy start-up. It's utterly unbelievable, and then you look at the guidance for the coming year. It's guiding for 70% revenue growth on top of what it's reporting this year. We're talking tens of billions of dollars, and the thing with that guidance is that Wall Street was expecting good stuff. Wall Street is expecting 45% growth in the coming year, and VA is saying 70% growth. The thing with that is, it's indicating that it would even be higher if it could physically make the stuff, but saying that it is a supply-constrained outlook. In other words, if we could have more supply, then perhaps we could deliver more revenue growth in the coming year, we can't, so we're saying around 70%. Unbelievable, the top five hyperscalars spending roughly 800 billion in capex this year. Many investors believe that's been unsustainable that pace, but Nvidia saying they expect the hyperscalers to spend 1.3 trillion in the coming year, so 500 billion more than what they are going to spend this year. There's your headline numbers.
Matt Frankel: Companies that grow revenue at 106% year over year generally don't trade for 25 times forward earnings like Nvidia does. It's fair to say that the stock is pricing in an eventual deceleration. You mentioned the original estimate was for 45% revenue growth last year, which is a pretty big deceleration from 106%. Now that we're getting 70%, or they're saying 70%, which they have a good history of lowballing their estimates. That's the real reason the stock is rising. The company said itself that it can only satisfy about 70% of the demand it's seeing for its products. It's not the earnings themselves. Everyone expects Nvidia's earnings to be slightly better than the guidance and analyst expectations every quarter. In fact, Nvidia initially fell when the report came out before all those forward guidance numbers were revealed. There are margin compression concerns due to memory costs, but right now you're essentially trading about 300 basis points, or three percentage points, of your 75% gross margin in exchange for roughly doubling your revenue growth expectations going forward. The margins will be worth watching. Nvidia's margins have been expanding pretty much without fail for quarter after quarter, and that's no longer the case, but not much not to like about this report.
Tyler Crowe: It's strange. I'm a little bit at a loss for words for this, which makes for arguably the worst podcast media ever. But this guidance revision, this large, is obviously going to have a profound impact on the entire AI infrastructure ecosystem, not just Nvidia. We're seeing shares rise today and this idea that we're actually supply constrained versus, I don't know, maybe some of these new entrants like Google's, these custom-built chips that all the hyperscalers are building themselves. There was this concern that maybe demand might be there, but it is there. With that in mind, all of this supply coming to the market from Nvidia, from these other companies, and we're still supply constrained. We've covered the picks and shovels of the AI infrastructure build-out a couple of times here, but I want to challenge you guys a bit because this is the biggest story over the next couple of years. It's hard to avoid. What are some of the companies in this picks-and-shovels part of the industry that this revision signals to, that are going to be the winners and losers? Maybe let's focus on some of the ones that are a little lesser known here and really lean into our Hidden Gems theme here.
Jon Quast: Well, Tyler, I want to just point out what Matt said here regarding the gross margin concerns going forward for Nvidia, there's higher memory cost going into everything with AI, and that is going to impact some of Nvidia's margins. As you pointed out, maybe not a big deal with Nvidia, but let me just latch on to that higher memory cost thing. I think that that becomes a little bit problematic for a company such as HP . This is a loser here because of what's going on here. I'm not just saying that because HP stock is down today, but you look at consumer devices. Many of these memory companies, maybe not many, but some of them have pivoted away from the consumer market entirely because there's so much demand in the AI infrastructure trade. These memory companies pivoting exclusively to that.
Not only are memory prices going up generally, but now some of the companies supplying the consumer market have exited that. There's even a bigger shortage in the consumer part of the market. The memory costs are going to be a higher and higher percentage of the overall cost going into making a personal computer. The cost of a personal computer going up, that is really hard for a business like HP. You look at Dell , at least it has the tailwind from its AI server business that is supporting its growth. HP doesn't really have that. I would say it's a tough place to be if you're HP.
On the other side, let's talk about a hidden winner here. We're talking about potentially, I don't know how many extra GPUs that Nvidia is saying it's going to sell in the next 12 to 24 months. It's going to be a lot. Let's put it that way. GPU interconnectivity is a bigger and bigger trend. I look at a company such as Credo Technologies , ticker symbol CRDO. This is one of the several companies out there that can benefit from increased need in GPU interconnectivity. But when I look at Credo, one of the things that I do like about it is how small it is. Nvidia is saying 1.3 trillion potentially in spending in the next year from the top five hyperscalers. Credo Technologies only has 1.3 billion in revenue right now, and it's tripled in the last year, expecting 80% growth in the coming year. I believe this stock can be a good performer. Let's say if it reaches 5 billion in revenue within the next several years, that is just a drop of the gush of spending that Nvidia is projecting here. That is one that I think can be under the radar, maybe a hidden winner here.
Matt Frankel: I'll call out a few hidden winners and losers here, so a couple of winners. They're both roughly $15 billion market cap companies, and both are companies that most people haven't heard of. The first one's Onto Innovation , ONTO. They make the inspection tools used in making all these memory products that are fueling that supply challenge, and a between-the-lines takeaway is Nvidia's 70% expected growth rate next year. It implies that the company is going to need a lot more memory than expected, so that could be a positive tale in there. Another one's called IES Holdings , ticker symbol IESC. They design electric systems for data centers. We've talked about comfort systems. It's a similar story here, among other end markets they serve. If hyperscaler or capex goes from $800 billion to $1.3 trillion next year, power is a big constraint for data center development. Companies like this are going to have not only a lot to do, but a lot of pricing power. But on the losers' end,
Jon really hit the nail on the head when he said that any company that needs memory for any type of consumer electronics could be a loser. Although I love the company and its management team, I got to call out Garmin here, GRMN. They rely on third party memory for all their products and as much of a great job as they've done with companies like Nvidia scooping up more and more of the memory capacity, it could raise prices on Garmin devices or result in margin compression if they don't want to pass along price increases, it's likely to be a pretty temporary problem, but it's definitely one that's worth watching for companies like that.
Tyler Crowe: It'll be interesting to see if Nvidia is a chip company, but they outsource everything to Taiwan Semiconductor . I will be fascinated to see with the memory companies, as well as the chip manufacturers, the foundry companies, if we start talking about a significant expansion of production, because everywhere we look, we’re looking at these constrained bottlenecks, whether it be electricity, whether it be GPUs, CPUs, memory. Name your chip; we seem to be running short right now. I feel one of the stories we're going to be really following in the coming quarters is are we going to see significant expansion of capacity from these companies to actually meet this demand? Because otherwise, workers are just going to be stuck in this short-on-supplies thing, and a lot of these companies are going to have the winners and losers continue down this path unless there is some significant change. Coming up after the break, we got another earnings report coming up. We got CrowdStrike , who is also having an awesome day in the market.
Shares of CrowdStrike are up 18% as we're taping right now. After the company reported earnings, another great earnings report, similar to what we saw with Nvidia here. This pairs rather nicely with a lot of things that we've been talking about with AI because there was this story around AI and hacking and the idea of basically most of cybersecurity these days is going to be rendered obsolete by AI agents. But based on these earnings reports and Nvidia's guidance, it doesn't seem to be the actual issue here. It seems as though AI may be pushing customers to spend more instead of less. Guys, what did the report say?
Matt Frankel: Well, Nvidia's reaction was generally based on its forward guidance. CrowdStrike just reported a blowout quarter, period. Not because revenue grew 26% year over year, which was an acceleration. The real number is that net new growth in annual recurring revenue was up 51% year over year. That's a company record. That's something CrowdStrike has never been able to do, even in the much earlier phases of its growth ramping up. A net new AR that was about 17% higher than even management's own guidance. AI is clearly fueling demand for cybersecurity at a much stronger rate than experts thought. The remaining performance obligation, which is the technical word for the backlog, grew by 49% year over year to a little over $10 billion. Adjusted operating margin grew by 350 basis points. Management raised its full-year guidance significantly on both the top and bottom line. There were very high expectations going into this report. It's a highly valued stock, but CrowdStrike really delivered another great quarter.
Jon Quast: I love this not-so-subtle zinger from CrowdStrike CEO here from the conference call: AI is driving a clear divide between the cybersecurity companies that solve problems and those that compound problems. I'll let you decide which one CrowdStrike says it is itself, but what is so interesting here is, to Matt's point, this was a great new quarter for net new business during the quarter and the management team saying that this is as a result of the Mythos moment. If you remember Mythos coming out, this is one of those AI models out there supposedly broke containment and causing problems, and they had to pull it. Investors saw this initially as a threat to the cybersecurity space. CrowdStrike management saying this is actually going to be a benefit for us, and right now the numbers are backing that up. You see the timing of the Mythos being released and all that buzz, and then you see the uplift in CrowdStrike's business.
That said, I will put on my skeptical hat here because there are some recent changes in the last couple of years to CrowdStrike billing methods, and so all new customers are now coming in in this flex billing model. Whereas before, they signed contracts maybe for the year, and they picked which modules they wanted to adopt from CrowdStrike's roughly two dozen cybersecurity module options. Now you have a spending commitment. You can flex that into modules that you're experimenting with, flex away from the ones that aren't working for you. Then, within that time frame, you can re-flex. Otherwise, when you spend all the money that you had committed, you can just re-up at the same rates that you've negotiated with CrowdStrike. That really does allow for faster adoption. It allows for, rather than waiting for, let's say that you're a business and you see this Mythos moment, you're scared, you're wanting to try some things to protect yourself, whereas before you might need to wait til your contract was up or that whole thing.
Now you can just reflex, and you can experiment with things. Management pointing out that new customers are entering by the Flex business model, billing method. That's the one that they have to choose if they're a new customer. There's a significant uptake in the annualized recurring revenue right from the get-go. Maybe this is more of a billing thing that Mythos is showing us why this is such a good way to bill its customers, at least if you're CrowdStrike, but we'll see if that is actually great for both CrowdStrike and its customers long term.
Tyler Crowe: One of the more interesting things about AI, actually, is the way that it's changing the way a lot of software companies bill or charge how they're doing. We had this software as a subscription model, but now it's even starting to go almost on a usage basis, similar to what we're seeing with token usage with AI. Who knows, maybe one of the biggest innovations with AI is new billing processes here for these companies. CrowdStrike is another one of these darling companies. It's done incredible for investors. It's up 114% over the past year. There's plenty of Motley Fool members who've had recommendations on this around CrowdStrike who've done very well.
But I want to put the rubber to the road here for investors because another great quarter seems to continue. This is the crux of the challenge here is shares trade for 37 times sales. That means right now it would take 37 years for the company to generate its market cap in revenue. Now, granted that revenue stayed flat, the expectation is it would grow, but that's still huge. This was a discussion during the dotcom bubble with Sun Microsystems, where they're like, this isn't our earnings. This is our sales, before we have to actually deduct anything right now. This has been the story with CrowdStrike. It's a great business, it's growing a lot, but the valuation is crazy. With this valuation today, and everything you guys read from the earnings report and what you saw, is this stock an actual buy now, and if not, is there something within it doesn't have to be cybersecurity, but maybe the V-n diagram of what you could call CrowdStrike's tangential areas where investors should consider instead, if you think that this thing is just way too expensive?
Jon Quast: Well, Tyler, you're calling out valuation. I will say that I have sold stocks in the past based solely on valuation concerns. Every single time I have done that, I've lived to regret it in hindsight because, generally speaking, when the business is great, the market is great, everything is great, except for the valuation. Selling on that basis alone it's always been wrong for me. I tend to stay away from that more now. I really do try to sell businesses that are performing poorly or industries that I believe are under long-term threat. I'd let that be more of my deciding factor. If ever there was a company to not ignore the valuation entirely, but to push it way down your concerns list, I think CrowdStrike is one of them because it has demonstrated such an ability to compound its business over time, and I can't think of maybe a more important long-term industry than cybersecurity, one that's growing very nicely. CrowdStrike is one that, if your only concern is valuation, I'd hit pause on that because it really is a phenomenal business and industry.
I will say, though, if you are concerned about the valuation here but want to stay in the same general area, it's not a direct competitor, but I would just point out Rubrik, RBRK. This is a cybersecurity company, but not a direct competitor to CrowdStrike, it trades at only 14 times sales. That's about a third of the valuation, and yet it is growing faster than CrowdStrike. I think that is something to look at. It does generate free cash flow. It's got a pretty good balance sheet, so that would be one I'd look at.
Matt Frankel: I'm going to push back a little bit. If the pandemic era, SPAC bubble, and the Dublin high-growth tech stocks taught me anything, it's valuation always matters, at least a little bit. Contrary to what Jon just said, there are several stocks that I regret not selling on ridiculous valuations during that era. Just to put the numbers in perspective, CrowdStrike they've previously targeted 20% long-term revenue growth in perpetuity. At the current valuation, that tells us that the stock trades for about seven times the revenue it will generate in a decade from now. On one hand, growth is accelerating, which, you're right, is rare at this scale. The forward book of business is growing faster than current revenue. That implies acceleration in the near term.
That AI cybersecurity thesis is something that I completely believe in, but the math here is brutal. Even if, let's say, CrowdStrike's revenue were to triple over the next five years, which I think would be a stretch, the company would still be at about 12 times sales at the current price. There's a lot not to like here, and I know Tyler is going to be with me on this one. Their stock-based comp is massive enough to completely wipe out that operating income that we talked about. The company actually reports an operating loss on a GAAP basis. Their diluted share count grew by almost 5% over the past year. That's even after some buybacks to help offset it, and I would expect a similar rate going forward. Even though they're a leader, they're not without competition.
To modify a Warren Buffett quote that I love, CrowdStrike is a wonderful business at an uncomfortable price right now. I wouldn't start a new position here today. If you absolutely want to, it's definitely a great case for dollar-cost averaging into a position. But as an alternative, I recently bought Zscaler. They partner with CrowdStrike, a lot of the same tail ones, but a much more palatable valuation right now.
Tyler Crowe: The stock-based compensation, and this is not just a Crowd trick thing. It is something that I have always struggled with when it comes to evaluating businesses is when there is that much stock-based compensation that wipes out earnings or operating profits in that way, it's hard to assess the success of this business over the long term because so much bid is going to the employees rather than the shareholders. It will be a story worth following. With a valuation this high, I know that investors are going to be thinking about that over the long term. Coming up for the break, we're going to dip into the mailbag specifically related to AI.
ADVERTISEMENT: At McDonald's, feeding the little ones just got easier with a Happy Meal for just 299 on the app. That's long journey stop-offs and move-in fees sorted. Just a little spin for some big smiles. Some fun, some food. It's all inside this Happy Meal. Until 1st September from 11:00 A.M. Only on the app, not on delivery. One use per day, a maximum of four Happy Meals per redemption. Price may vary. Treacherous ring roads lie ahead on our mission to reach nanos. There is Mackey's for Black Pepper and Garlic McNuggets. Navigation, rerouting. The main mission can wait. Take a side mission to McDonald's. Available until 29th September from 11:00 A.M. Whilst stocks last, subject to availability. Participation varies.
Tyler Crowe: Everyone, quick reminder, if you want to get a question into us and have it read on air, email us at [email protected] . That's podcast with an S. I've also put the email in the show description, so you can get it there as well. Remember, keep it short, keep it Foolish, and we cannot give personal advice. Today's question comes from John from New Jersey, and the question is, we have had multiple discussions about whether the money invested in data centers will be worth it, and that's a very fair assessment of what we've done here. One of the threats to data centers is the idea that many of the new models can be run locally, not necessarily like cloud and OpenAI, but a lot of the Chinese models that we're seeing these days. One big advantage of these models is that all of your company's data will remain local and will not be sent to another company to possibly be sold on. The newly announced Apple computers, personal computers. I think it is the new Mac Mini, are actually designed to run AI locally. This gets to Jon's question, how much of a threat is local use of AI to the actual AI cloud companies?
Jon Quast: I can't tell you how much I love this question. I feel I have been a local AI crusader for months now, and I've been all by myself. Now John from New Jersey is standing with me. Johns got to stick together, so I'm really thankful to talk local AI. Just briefly, Apple, many products in particular, have already been used for local AI, and Apple leaning into that with its next generation, but let me answer this question directly. I don't think that local AI is a threat to the cloud AI industry. I think that there are different use cases. I think that more and more people, individuals, are going to want to run some local AI. Running a model that is personalized to me on my stuff in my home, I think that's going to be a growing trend. There's a lot to unpack with that. There's still a lot of learning how to structure it.
A lot of people out there are trying to solve for this, but beyond individuals, I think that hospitals, schools, government agencies, they're all going to want to run more and more local AI for obvious reasons. They're not going to want all that stuff in the cloud. Yet I do think that there's still a use case for cloud AI in the future, because that's where a lot of the innovation is going to be happening. A lot of running your own stuff on your own hardware, there are challenges to that. I think that SpaceX 's new Grok bot really is making it more usable, perhaps driving an adoption curve. Definitely watch that, but I still think there's going to be innovation happening and things that you're going to need a cloud AI for. I think it's going to be both in the future. I think that we already have so much money being spent going into the data centers, going into those. But I think there's going to be a layer on top of that, which is your own local AI at home, or in your place of work, place of business, your school, whatever. I think it's going to be both in the future, so I don't see this as either/or.
Matt Frankel: I generally agree with Jon. It's really a case of a rising tide lifts all ships here when it comes to AI. Data centers and on-device AI are two totally different things to solve, two totally different problems. Plus, data centers have a few key advantages that are going to help them continue to grow. We've already mentioned the memory problems several times in this episode. The AI boom has made memory for local AI much more expensive, just to name one thing. Data centers, their operators have a lot more room to win the memory price awards. They have more money. They pay more if you're investing hundreds of billions of dollars. You get priority. Local inference it's bound by memory capacity, not by raw compute power. That's not the constraint here. That is a big challenge, but while local AI is not much of a threat to cloud-based AI, to tie it into our earlier discussion, I do think it could be one of the best things that ever happened to cybersecurity. Think about it, if all of your employees' local devices are running their own AI models, there will be thousands of new AI endpoints that you need to secure inside enterprise networks. Definitely could help companies like CrowdStrike and Zscaler going forward, just to tie it into what we were saying earlier.
Tyler Crowe: There's a real irony here of the entire 2010s was the whole movement of migration to the cloud, and every single business wanted to migrate to the cloud. Now we're talking about everything going back onto local servers, local hardware, and keeping your own stuff in-house. Everything seems to come full circle. Well, guys, that's all the time we have for today.
As always, people in the program may have stocks they talk about, and The Motley Fool may have formal recommendations for or against, so don't buy or sell stocks based solely on what you hear. All personal finance content follows Motley Fool editorial standards, and it's not approved by advertisers. Advertisements or sponsored content are provided for informational purposes only. See our full advertising disclosure, please check out our show notes. Thanks for producer Dan Boyd and the rest of The Motley Fool team. For Jon, Matt, and myself, thanks for listening, and we'll chat again soon.
Nvidia's most recent earnings and guidance blew past expectations and set up another stellar year for anything AI-related.
By Motley Fool Staff – Sep 8, 2026 at 11:35PM EST

### Article 41 · 2026-09-08 · uk.finance.yahoo.com
Within 2% of its all-time high, can anything stop Nvidia stock?

Sometimes, a share comes along that stands out on almost any metric. Nvidia (NASDAQ: NVDA) is one. In five years, Nvidia stock has soared 924 %. The past decade has seen it move up an incredible 14,501 %.
Currently, the company commands a market capitalisation of $ 5.6trn – the biggest in the world.
The share has moved up 37% over the past year and is currently less than 2% away from its highest-ever level. Can nothing stop Nvidia stock?
A real story of business growth, not just stock price momentum
Looking at the price chart for Nvidia, it can be tempting to wonder whether the dramatic rise over recent years makes sense, or is an example of stock market exuberance.
It could be that there is an element of both things at once, in fairness. But it is important to realise that, unlike some much-hyped stocks, Nvidia has both a massive (and massively profitable) business that continues to grow at an unusually strong rate for a company of its size.
Its most recently quarterly numbers, published last month, demonstrate the point well. Revenue was $96bn. Remember – that is not an annual number, but a single quarter's worth of sales. Not only that, but the year-on-year revenue growth was an incredible 106%.
In the same quarter last year, the year-on-year revenue growth was close to half of that, at 56%.
So Nvidia is not only growing hugely – it is actually increasing its rate of growth. For a company with $1m in sales, that would be impressive. For one with $96bn in sales, it is simply phenomenal.
Operating income, meanwhile, grew even faster, at 124%. I see that as an example of economies of scale in practice. On top of that, operating cash flows grew even more strongly. They hit $24bn in the quarter, representing year-on-year growth of 157%.
Does the price make sense?
Can the chip giant keep growing at anything like this rate? Nvidia stock is close to an all-time high because the bulls think so. AI demand is huge and, for now at least, there is little sign of that slowing down.
Its proprietary technology gives Nvidia a significant competitive advantage. That is enhanced by its large installed user base.
But there are risks here, that could potentially see the Nvidia share price tumble at some point. One is the question of demand for AI overall. If it turns out to deliver less benefits than hoped, maybe companies will rein in spending.
Then there is a question about demand for Nvidia in particular. It is surging now but, as those numbers suggest, Nvidia chips do not come cheap.
That exposes a risk that lower-cost competitors will take market share from Nvidia, hurting its revenues and profits. Still, at 29 times earnings, the stock price does not look outrageous to me.
I think there are clear risks here but, for an investing willing to countenance them, I see Nvidia stock as worth considering even close to its all-time high price.

### Article 42 · 2026-09-08 · fool.com
Prediction: Sept. 10 Will Be a Big Day for Nvidia Shareholders. Here’s What to Watch.

Nvidia (NASDAQ:NVDA) has been a key company -- and some may say the key company -- driving the artificial intelligence (AI) revolution. This is because the tech giant designs the most powerful graphics processing units (GPUs), the chips fueling AI, and has expanded this expertise into the creation of complete systems. Today, Nvidia is a full-stack AI company, offering customers a vast selection of products and services needed along the AI path.
All of this has translated into explosive growth and record levels of earnings. In the most recent quarter, Nvidia's revenue soared 106% to $96 billion. And profit followed, advancing 126% to $59 billion. Nvidia is benefiting from massive investments in AI infrastructure; capital expenditures by the company's top five customers are forecast to reach $1.3 trillion next year.
Nvidia shared this and other news just last month during its fiscal 2027 second-quarter earnings report. Now, Sept. 10 represents a fresh opportunity to hear more from this AI powerhouse. My prediction is that it will be a big day for shareholders. Here's what to watch.
So, first, a quick summary of Nvidia's recent and long-term performance. The company's earnings and stock price have soared over the past few years, as shown in the chart below, driven by its dominance in the AI chip market.
Nvidia entered this market about a decade ago, well before the AI boom started, and designed its GPUs specifically to serve AI. In the past, Nvidia focused its designs on the gaming space -- this remains a market for Nvidia, but the AI opportunity has become the tech giant's biggest business. For example, in the recent quarter, data center revenue came in at $89 billion on the total $96 billion in revenue.
Nvidia's stock price continues to climb, but with a gain of about 20% so far this year, it's underperforming certain AI peers such as chip rivals Advanced Micro Devices and Intel, and memory chip giant Micron Technology . Those three players have seen their stock prices soar in the triple digits. This is as investors shift into other AI players that didn't climb as much as Nvidia in the earlier stages of the AI boom.
Now, let's consider what's set to happen on Sept. 10. Nvidia is set to make a presentation at the Goldman Sachs Communacopia + Technology Conference at 8:50 a.m. Pacific Time, and this will be an opportunity for investors to hear the latest news at a crucial moment in time: as Nvidia rolls out its latest update, the Vera Rubin platform. The company said last month that it had begun production shipments of Rubin and that the system would likely account for 20% of data center revenue in the third quarter.
This launch also marks Nvidia's entry into the stand-alone central processing unit (CPU) market, one that so far has been dominated by AMD and Intel. Nvidia has set its sights on leadership here, so any CPU forecasts will be points to watch.
For the first time, Nvidia recently offered an annual growth forecast, predicting 70% year-over-year revenue growth for the 2028 fiscal year -- that's the fiscal year that begins in early 2027. Investors should look for additional comments, potentially concerning supply constraints and demand, that may offer further clues about what to expect.
Meanwhile, tight memory supply and higher prices have been and continue to be a headwind for Nvidia. The company might offer investors additional details about how it's handling this challenge. And while we're on the subject of headwinds, it will also be important to listen for any comments on potential sales in China. Restrictions by the U.S. blocked Nvidia's chip sales to China in April 2025, and though the U.S. has given the company the go-ahead, Nvidia still hasn't been able to reenter this high-potential market.
If Nvidia addresses some of these points, my prediction is that Sept. 10 could be a big day for shareholders, and the stock could take off in the days to follow. But even if I'm wrong and Nvidia shares don't react after the Goldman Sachs conference, that's OK. The company, thanks to its solid AI empire, is still well-positioned to deliver a win to investors over the long run.

### Article 43 · 2026-09-08 · wccftech.com
NVIDIA RTX 5070 Reportedly Gets GB205 Replaced By Bigger GB203 Die In A New Variant

NVIDIA might be preparing a new variant of the GeForce RTX 5070 by using the bigger GB203 die.
GeForce RTX 5070 Reportedly Gets a New Variant, Featuring a Cut-Down GB203 Die From RTX 5070 Ti
It's not new for NVIDIA to utilize different silicon for its existing GPUs, and we have seen that it has already started using bigger dies for some of its RTX 50 series cards. If you remember, various vendors like MSI have already launched a new variant of the RTX 5060 GPU. Unlike regular RTX 5060s, which utilize the GB206 die, some newer RTX 5060 cards have transitioned to the GB205 die.
The GB205 is bigger, but NVIDIA has nerfed it in order to achieve the same specifications. Now another report is suggesting that NVIDIA is transitioning to a newer die for some of the RTX 5070 GPUs. The leaker @hongxing2020 reports that a new variant of RTX 5070 is about to arrive, and it will utilize the GB203 GPU die instead of GB205.
The GB203 die is specifically used in the GeForce RTX 5070 Ti and the RTX 5080, and measures 378 mm2. So, this is nearly 43% bigger than the GB205 die that measures only 263 mm2. To ensure the GB205 can match the GB205 specifications on RTX 5070, NVIDIA will have to cut it down significantly. This will require NVIDIA to disable nearly 42.8% CUDA cores to achieve 6,144 shaders as the full GB203 features 10,752 CUDA cores.
Moreover, NVIDIA will have to disable 2 of 8 memory channels to achieve a 192-bit bus to accommodate a 12 GB GDDR7 memory configuration. The leaker didn't state the reason for such a transition, but we know that NVIDIA sometimes takes bigger dies that aren't good enough for the higher-end GPUs and deploys them in lower-end hardware. So, in this case, the GB203 dies that couldn't qualify for the RTX 5070 Ti and RTX 5080 will end up in some RTX 5070 cards.
The leaker also mentions that NVIDIA will release a new GPU driver tomorrow, which could mean early support for the new variant. However, this isn't explicitly mentioned in the tweet.

### Article 44 · 2026-09-08 · news.asu.edu
ASU launches course for digital creators with NVIDIA Omniverse Libraries, OpenUSD

ASU launches course for digital creators with NVIDIA Omniverse Libraries, OpenUSD
Designing Digital Worlds course gives students hands-on experience with agentic skills, with direct engagement from NVIDIA experts
Arizona State University is launching a new interdisciplinary course this fall that will give students hands-on experience with NVIDIA Omniverse Libraries and OpenUSD , bringing emerging technologies and direct engagement with NVIDIA experts into the classroom.
Designing Digital Worlds (DSC 553/494) introduces students to technologies and workflows used to connect and build 3D environments for architecture, industrial design, gaming, film and animation, immersive media, simulation and physical AI use cases.
The course is led by Ana Herruzo , associate professor in The Design School , director of the Master of Science in Immersive Experience Design and director of the MediatedX Research Lab at ASU’s Media and Immersive eXperience (MIX) Center .
The goal is to move beyond digital environments that are fully predetermined and toward worlds that can continue to function, react and change on their own.
“We’re asking students to move from designing a scene to designing a system,” Herruzo said. “Instead of controlling every moment through animation, they have to think about physics, rules and changing conditions. The world can keep running after they walk away from it, and that changes the design problem completely.”
As part of the course, students will engage with NVIDIA experts through guest lectures, office hours, reviews and specialized teaching resources, helping them apply OpenUSD and simulation concepts to their own projects.
The course takes an interdisciplinary approach to technologies that are increasingly connecting fields that have traditionally been taught separately. Students will explore applications including building information modeling (BIM) and digital twins in architecture; product design and simulation in industrial design; real-time world building for games; virtual production for film and animation; spatial computing for XR and immersive media; and 3D simulation and robotics for physical AI.
Rather than approaching these technologies solely from a computer science perspective, Designing Digital Worlds is designed to make emerging technical workflows accessible to students whose primary expertise may be in design, storytelling, architecture or other creative disciplines.
The course also introduces Python programming through AI-assisted workflows, helping students build technical skills while applying them directly to creative projects.
Jialong Xu, a doctoral student in design, and Janki Patel serve as teaching assistants for the course, supporting students as they navigate the intersection of creative practice and increasingly technical workflows.
Patel said working with NVIDIA Omniverse has influenced how she thinks about her own creative practice.
“NVIDIA Omniverse has helped me see my own work through a new lens. Learning these workflows while helping students explore them has inspired me to rethink my work and imagine new ways for immersive experiences to become more dynamic, connected and responsive to the world around us,” Patel said.
Preparing students for changing creative industries
The course responds to rapid changes across creative industries, where real-time 3D, simulation, virtual production, artificial intelligence and connected digital workflows are reshaping how creative work is produced.
That technical exploration is paired with critical examination of how emerging technologies are used and the consequences they may create. In ASU’s Master of Science in Immersive Experience Design , of which Designing Digital Worlds is a required core course, students also take "Ethics and Social Impact in Immersive Experiences," reflecting the program’s emphasis on understanding not only what technologies make possible, but how they may be applied, repurposed and affect people and communities.
That combination of technical fluency, creative experimentation and critical thinking is intended to prepare students not only to simply use emerging technologies, but to help shape how they are applied.
“Learning how to use the technology is only part of the education,” Herruzo said. “We also want students to think critically about what they create, how a technology might be used beyond its original purpose and what consequences those choices could have. Technical capability and critical thinking have to develop together.”
Students in Designing Digital Worlds will develop projects using OpenUSD pipelines and NVIDIA Omniverse Libraries workflows, with opportunities for feedback and design reviews throughout the semester. Drawing on NVIDIA’s free, open-source Learn OpenUSD curriculum and Simulation and Physical AI educator teaching kit , the course will help students develop foundational skills they can build on as they pursue the NVIDIA-Certified Professional: OpenUSD Development certification .
“Creators and designers need tools that expand their imagination while giving them the freedom and precision to realize their vision,” said Madison Huang, senior director of product and technical marketing for physical AI platforms at NVIDIA. “By providing hands-on experience with OpenUSD and simulation workflows using NVIDIA Omniverse Libraries, ASU is preparing the next generation to create virtual worlds that reflect the fidelity and behavior of the physical world — for applications spanning games, cinema, robotics and factory digital twins."
The course also creates opportunities for collaboration across the Herberger Institute for Design and the Arts, connecting areas that have traditionally been taught separately but are increasingly converging professionally.
Designing Digital Worlds is offered at ASU’s Media and Immersive eXperience (MIX) Center in Mesa beginning in fall 2026.

### Article 45 · 2026-09-09 · NVIDIA Corporation
NVIDIA Brings Real-Time AI to Broadcast, Sports and Global Streaming at IBC | NVIDIA Blog

At the IBC conference, running Sept. 11-14 in Amsterdam, the creative, technology and business communities are coming together to turn ideas into action and discuss innovations across the media and entertainment industries. More than 44,000 attendees from 170+ countries are gathering to explore 1,300+ exhibitions in 14+ halls and outdoor spaces, with over 600 speakers delivering insights.
Media companies are increasingly integrating AI into live production, sports, news and streaming workflows to unlock richer performance insights, verify video authenticity, and enhance and localize content — all without disrupting trusted broadcast environments.
At IBC 2026 in Amsterdam, NVIDIA announced a major expansion to NVIDIA AI for Media — a collection of GPU-accelerated software development kits (SDKs), NVIDIA NIM microservices, playbooks, and blueprints that enhance audio, video and augmented-reality effects for media and entertainment workflows — to unlock new ways to understand motion, verify and enhance video, localize programming and build AI-powered media applications.
The NVIDIA Synthetic Video Detector (SVD) NIM microservice, announced earlier this year at SIGGRAPH , helps organizations assess the probability of whether footage is authentic or AI-generated, giving editorial, content-authentication, digital-forensics and media-integrity teams another point of analysis in their review process.
Since its initial release, SVD’s accuracy has reached 99.3% for text-to-video content and 97.7% for image-to-video content, with especially large gains on difficult image-to-video cases.
Dalet is integrating SVD into a secure, cloud-hosted verification workflow for news organizations. This allows editorial teams to submit footage through SVD, inspect and review the resulting scores and metadata within a Dalet interface.
TwelveLabs announced the general availability of Compliance by TwelveLabs, its first application built on the company’s video intelligence platform, helping media and broadcast teams rapidly screen content against regional and custom compliance standards. The solution integrates SVD to add frame-level authenticity signals and confidence scores, enabling media teams to identify potentially synthetic media within the same compliance workflow.
Wowza , whose Wowza Streaming Engine media server technology powers more than 35,000 video deployments across over 170 countries, will distribute SVD through the Wowza Video Intelligence Framework . The solution, powered by NVIDIA-accelerated infrastructure, will enable broadcasters, streaming providers and other organizations to analyze live video feeds and extract data around detected objects, scenes and signs of AI generation in real time. It can be deployed and run on premises, at the edge, in the cloud, across hybrid deployments or fully air-gapped, giving organizations greater control over critical media workflows.
NVIDIA 3D Body Pose estimates 2D and 3D human joint locations and angles from video captured by a single camera, helping turn motion into structured data without marker-based capture systems.
For sports organizations, that data can support player and athlete movement tracking, biomechanics and performance analysis, replay enhancement, officiating and adjudication workflows, player-safety applications, and virtual interaction and immersive experiences.
The technology can also provide structured human-motion data for content-creation workflows. When mapped to a compatible character rig, joint and motion data can serve as input for animation blocking, digital doubles, character retargeting and virtual-production experiences.
Vizrt is using Body Pose technology in live virtual-studio environments, with tracked body movement driving real-time 3D lighting effects such as reflections, shadows and environmental rendering.
Video Frame Generation (VFG) makes video motion appear smoother by using generative AI to create new frames between the original frames of a video. It can increase frame rates by 2x or 4x while preserving visual quality and temporal consistency, enabling more fluid sports, slow-motion replays, live media and other high-motion video experiences. VFG also supports frame-rate conversion and frame boosting for generative AI video workflows.
Ross Video is integrating VFG into its Rio Replay platform to create AI-assisted slow-motion video for sports production.
The work supports 6x slow-motion generation for sports replay. Development is underway toward 8x interpolation, meaning generated intermediate frames can give replay teams smoother motion without requiring every frame to be captured by an ultrahigh-frame-rate source camera.
NVIDIA Video Super Resolution (VSR) uses AI to upscale video while reducing noise, blur and compression artifacts. New streaming modes let developers choose between real-time performance and higher image quality, while adjustable controls help achieve the desired level of enhancement. VSR also adds 10-bit video support and improves overall performance and quality. VSR is available through the NVIDIA Video Effects SDK and a NIM microservice for use in streaming, broadcast, conferencing, video playback and content-creation applications.
The technology can support video players, conferencing applications, creator tools, streaming services, transcoders and broadcast systems through a common interface.
NVIDIA TrueHDR converts standard-dynamic-range video into high-dynamic-range output in real time, reaching up to approximately 2,000 nits while preserving local contrast and adapting brightness to the content.
VSR, VFG and TrueHDR can be combined within a single video-effects pipeline — helping media companies enhance existing content libraries for streaming, transcoding, gaming and creator workflows.
The NVIDIA LipSync and Active Speaker Detection NIM microservices help developers build localization systems for interviews, news, sports, entertainment and other programming where multiple people may appear on screen.
LipSync transforms mouth movement in an input video to match a target audio track while preserving natural head pose, blinking and body movement. The new release improves facial occlusion handling and better preserves teeth, lip and facial textures.
The new Active Speaker Detection NIM microservice no longer requires speaker diarization for multiple audio tracks, adds voice activity detection and expands NIM microservice deployment support through a gRPC interface and broader GPU compatibility.
NDI is using NVIDIA AI for Media, including the NVIDIA LipSync NIM microservice, to enable real-time translation, lip-synced dubbing and regional language adaptation within existing broadcast workflows. By generating multiple language experiences from a common media stream, the approach can help broadcasters reach global audiences while reducing the bandwidth, infrastructure and production complexity traditionally required for multilingual distribution.
Studio Voice includes new Microphone Profiles built on NVIDIA Studio Voice NIM microservices, giving users more control over the tonal character of enhanced speech.
The capability is designed to suppress background noise, reduce room reverberation and improve speech clarity, then shape the enhanced output into a selected microphone profile for more polished live communications, streaming, podcasting and content creation.
As broadcasters, streaming services and sports organizations adopt software and AI, the infrastructure behind live content is becoming more flexible, more connected and increasingly built on shared accelerated computing.
The integration of Media Exchange Layer (MXL) with NVIDIA Holoscan for Media accelerates that transition — providing the common exchange layer that helps media applications connect and operate together.
Holoscan for Media is an open reference architecture and developer toolkit for building AI-powered media functions and applications for software-defined live production. MXL adds an open way for those software-based media functions to exchange live video, audio and data across a distributed environment.
As production functions move into software, developers can build applications that share accelerated infrastructure, connect dynamically and evolve independently. That can help media companies use infrastructure more efficiently, introduce new capabilities faster and reduce the amount of custom integration required between applications.
The integration also creates a stronger foundation for AI in live media. AI processing, video applications and traditional media functions can increasingly operate on the same accelerated infrastructure and in the same software-defined environment.
For technology vendors, this expands the opportunity to build applications that can work across broader, multi-vendor ecosystems. For media companies, it creates a path toward infrastructure that can adapt as formats, applications and AI capabilities change.
Sports is becoming a proving ground for a broader shift in AI: from general-purpose models toward fine-tuned open models built on proprietary data.
NVIDIA Sports Intelligence Playbooks are designed to accelerate that transition. They give leagues, media companies and technology providers structured frameworks to fine-tune NVIDIA open models on their own sports footage and annotations, creating multimodal AI that can understand the rules, players, scoring, strategy and context unique to a sport.
Sports organizations hold large volumes of proprietary video, metadata and performance information that are difficult for competitors to replicate. The playbooks provide a practical blueprint for converting those assets into AI capabilities that can underpin new analytics products, media experiences, automation tools and revenue streams.
The playbooks span the AI lifecycle, including data preparation, fine-tuning, inference, evaluation, optimization and deployment, and bring together NVIDIA technologies including Nemotron , NeMo AutoModel , Megatron Bridge , NIM microservices and NVIDIA accelerated computing .
By providing an integrated path from model customization to production, Sports Intelligence Playbooks can reduce the cost and complexity of building specialized sports AI while increasing demand across its compute, software and inference stack.
Early testing demonstrates the potential of domain specialization. When evaluated on previously unseen footage using question formats similar to those used in training, multiple-choice accuracy increased from approximately 53% to 94% and open-ended evaluation from approximately 5.7% to 66%.
Machina Sports is integrating Sports Intelligence Playbooks with its sports-native data, evaluation and agent infrastructure, enabling rights holders to turn proprietary media and expertise into private, deployable intelligence for live production, content and fan experiences.
The opportunity also expands as agentic AI becomes increasingly adopted. With the NVIDIA AI-Q Blueprint , organizations can use their domain-specific sports models as expert intelligence within agents that reason across video, enterprise data and software systems, extending the playbook from sports understanding into decision-making and automation.
Wowza is integrating vision language models, including NVIDIA Cosmos 3 and Nemotron, into the Wowza Video Intelligence Framework, fine-tuned through NVIDIA Sports Intelligence Playbooks to detect sports-specific moments in live streams and reduce time to action.
Reaching global audiences with live programming requires more than translating words. Language nuances, voice, timing, facial movement, captions and onscreen graphics must work together in real time, while preserving the editorial intent and production quality of the original program.
To help broadcasters, sports leagues, rights holders and streaming services bring these elements into a unified, software-defined, real-time localization workflow, NVIDIA is bringing its Content Localization technologies to the NVIDIA Holoscan for Media developer toolkit. Designed for broadcast and streaming developers, the reference workflow enables captions, translated audio, dubbing, synchronized video and localized graphics.
Content Localization with Holoscan for Media provides a reference for how localization technologies can work together in software-defined broadcast applications. Developers can select the capabilities needed for each program, market or distribution channel rather than deploying separate infrastructure for every localized version.
Content Localization with Holoscan for Media incorporates the latest advancements from NVIDIA AI for Media, including improved LipSync when faces are partially obscured and enhanced Active Speaker Detection to help applications identify who’s speaking in multi-person scenes.
Localization can transform the reach and economics of live programming. A shared, composable workflow can help media companies introduce regional coverage faster, serve more audiences and tailor experiences for individual markets — while preserving the timing, visual context and editorial control required for live production.
Technologies from AI-Media , CAMB.AI , Chyron and Panjaya each address a specific part of content localization with Holoscan for Media, from adapting voice and onscreen delivery to creating multilingual captions and translated audio, localizing graphics, and preserving expression and identity across live and on-demand content.
The Content Localization technologies also support file-based, streaming and post-production applications. Developers can use application programming interfaces for on-demand workflows and the Holoscan for Media reference workflow when localization must run as part of a live media environment. Together, they provide a consistent foundation for building multilingual media services across production and distribution.

### Article 46 · 2026-09-09 · reuters.com
Nvidia plans major expansion of data centre capacity in Australia to meet AI demand

SYDNEY, Sept 10 (Reuters) - Nvidia said on Thursday it was planning an expansion of data ‌centre computing capacity in Australia that would ‌more than double the nation's current load through partnerships with ​local firms.
The chip company said it was working with Australian cloud and data centre firms including Firmus, CDC, NEXTDC and AirTrunk, targeting a buildout of up ‌to 2 gigawatts ⁠of AI-related capacity by 2027.
The announcement comes as Australia positions itself as a ⁠global hub for data centre investment, while facing calls for tougher regulation over concerns about their environmental ​impact and ​heavy energy and water ​consumption.
Australia's current computing capacity ‌is 1.6 GW, according to a report from lobby group Data Centres Australia, citing research from analysts DC Byte.
Nvidia said the capacity expansion would support Australia's demand for AI. Its partners' data centres ‌would be built using its "DSX ​platform".
"Growing AI adoption across industries ​is increasing demand ​for high-performance computing," Nvidia said in ‌a statement.
"Expanding capacity in Australia ​will enable ​local innovators to develop models, applications and agents while supporting additional power generation projects to support ​regional and ‌global demand for AI compute."
(Reporting by Ruchika Khanna ​in Bengaluru and Christine Chen in Sydney; ​Editing by Subhranshu Sahu)

### Article 47 · 2026-09-09 · fool.com
Can Micron Catch Up to Nvidia's $5.5 Trillion Market Cap?

Micron ( MU +4.20% ) caught many investors by surprise when it surged from a market cap of less than $100 billion at the start of 2025 to a more than $1 trillion behemoth this summer, but the memory-chip maker may have what it takes to become the world's most valuable company. To take that crown would require it to top Nvidia 's ( NVDA +2.55% ) market cap, which is currently $5.5 trillion.
That wouldn't be easy, but it's not out of the question, either. Micron has surged by 673% over the past 12 months alone, while Nvidia has only increased by 37% over the same stretch.
Investors shouldn't expect Micron to keep delivering 673% returns each year, but there are reasons to believe that Micron will outperform Nvidia for some time and potentially become the world's most valuable company.
Memory chips are just as important as GPUs
AI chips have held the spotlight on Wall Street for multiple years, but Micron and other memory players only started to gain real attention at the start of the year. Rumblings from tech leaders suggest that gaining access to enough memory hardware is now their top priority.
Elon Musk said that the global shortage of memory is "the limiting factor" to the AI build-out, and Amazon ( AMZN +0.56% ) specifically cited rising memory costs when raising its capital expenditure projections for this year.
Memory chips also happen to be critical components for GPUs. Every Nvidia processor includes multiple memory chips from companies like Micron. Advanced Micro Devices ( AMD +3.09% ) and Broadcom ( AVGO +2.83% ) also need memory chips for their AI accelerators.
However, it's not just AI parallel processors that require memory components. So do CPUs and solid-state drives, which are just as critical for AI infrastructure. Nvidia's GPUs are essential components for AI data centers, but Micron and its peers provide multiple foundational components for those vast server clusters. And with AI software demanding quick access to ever-larger volumes of data, Micron and other memory-chip makers have more opportunities than Nvidia to expand their products' footprints within data centers.
In the market cap race, Micron can only gain ground on Nvidia if its fundamentals grow faster than Nvidia's. It turns out that's what's happening.
Nvidia was no slouch in its fiscal 2027 second quarter -- it delivered 106% year-over-year revenue growth. That was a substantial increase. But it looks far less impressive next to Micron, which crushed guidance and delivered a 346% year-over-year top-line gain to $41.9 billion in its fiscal 2026 third-quarter. Both companies have net profit margins above 60%, but Micron's edged ahead of Nvidia's in their most recent quarters.
Recent acceleration has also favored Micron. While Nvidia has posted a respectable 18% sequential growth rate, Micron's revenue surged by more than 70% sequentially.
Nvidia still generates more revenue and profits per quarter than Micron, but the gap isn't that big when considering their growth rates. Nvidia's Q2 fiscal 2027 revenue and net income were $96.2 billion and $59.7 billion, respectively. In Micron's fiscal 2026 third quarter, its revenue and net income were $41.5 billion and $28.2 billion, respectively.
Micron may be one year away from reporting nearly the same revenue and net income as Nvidia just reported. The math supports that conclusion if Micron can double its revenue and profits year over year in fiscal 2027 -- and that's assuming that Micron doesn't quadruple its sales as it did in its most recent quarter.
There's been a lot of talk in the investing world about how Micron and Nvidia both have attractive valuations, especially if you compare them to the average valuations for tech stocks or the broad-market S&P 500 . However, a head-to-head comparison isn't even close.
Micron trades at a forward P/E ratio of 6 compared to Nvidia's 25. Micron's shares would have to roughly quadruple for the company to match Nvidia's forward P/E ratio. A similar gap exists between these two companies' price/earnings-to-growth (PEG) ratios . Micron's 0.14 PEG ratio is much lower than Nvidia's 0.58 PEG ratio. In general, any positive PEG ratio of less than 1 is viewed as signaling that the stock in question is undervalued. So Nvidia is still a bargain by that standard, but Micron is even more so.
Both forward P/E and the PEG ratio factor a company's expected future growth into the valuation calculation. When pricing in their upcoming opportunities, Micron looks like a better bargain, which could support the stock's continued outperformance over Nvidia. If these trends continue, Micron may be able to overtake Nvidia's market cap by the end of the decade.
By Marc Guberti – Sep 9, 2026 at 5:47AM EST

### Article 48 · 2026-09-09 · fool.com
Here's My Nvidia Stock Price Forecast for the End of September

Nvidia ( NVDA +2.55% ) stock has gained 1,600% since ChatGPT came out in 2022, catapulting it to the top of the stock market. It has retained its dominance over the past few years despite many challenges, and although it faltered earlier this year, it's back to beating the market, up 24% year to date.
Here's my prediction for where it's going to end the month .
Nvidia reported its latest earnings on Aug. 26, and the phenomenal report sent the stock higher. It's not showing any signs of slowing down; revenue increased 106% over last year in the fiscal 2027 second quarter (ended July 27), and management is guiding for it to rise about 90% in the third quarter.
It's also guiding for revenue to increase 70% in fiscal 2028, and according to CFO Colette Kress, it's a "supply constrained outlook." The top hyperscalers are expected to spend $800 billion this year and $1.3 billion next year. Nvidia gets a substantial piece of all of that.
However, Nvidia stock is still off its high from May. Without earnings news, Nvidia stock trades on potential announcements and external factors. It recently jumped on the news that it's acquiring AI development platform Hugging Face for $12.9 billion, and other significant news could lift it higher. There could be outside news, too, like interest rate movements and unexpected artificial intelligence (AI) updates.
Stocks sometimes move when they become too cheap to ignore or too expensive to support. Nvidia stock trades at 19 times trailing-12-month sales and 29 times trailing-12-month earnings. Those are near multiyear lows, implying that as Nvidia gets bigger and faces more competition, the market isn't willing to pay as much for the stock.
Another factor could simply be the time of the year. There's a phenomenon called the September effect , which is that September, on average, tends to be the worst month of the year for stocks. That doesn't mean it's terrible every year, but it's a trend. Even if the market does decline this month, that doesn't mean every stock will decline. Absent any particular news, though, the market could be weighed down by whatever it is that causes the September effect.
So where does that leave Nvidia stock by the end of the month? It just got a boost from the Hugging Face announcement, and it has surpassed the high it reached after the earnings report. Without further major announcements that could make the stock more valuable, I don't see it moving too much. The market isn't willing to value it much higher than it is today, and since it just jumped, it could even slightly decline in value.
By Jennifer Saibil – Sep 9, 2026 at 9:38AM EST
Nvidia stock jumped after the company's latest earnings report on Aug. 26, demonstrating high growth and a strong outlook.

### Article 49 · 2026-09-09 · fool.com
Nvidia CEO Jensen Huang Just Put a Nail in Michael Burry's Bear Case

Michael Burry is no stranger to controversial market calls. The hedge fund manager and founder of Scion Capital cemented his place in Wall Street history by predicting the subprime lending market crash in 2008. His high-stakes bet earned him $100 million, while his investors banked $725 million. The events were immortalized in the movie The Big Short , and Burry still turns heads with his headline-making calls.
The legendary investor's most recent target has been artificial intelligence (AI) and, more specifically, Nvidia ( NVDA +2.55% ) . Burry takes issue with the industry's estimates of the useful life of semiconductors used in AI, believing they are too long.
However, Nvidia CEO Jensen Huang just put a nail in Burry's bear case.
A little context helps illustrate Burry's concerns. Many technology companies estimate the useful life of Nvidia's graphics processing units (GPUs) at six years. For accounting purposes, that means the price of these processors is divided by six, and one-sixth of the cost is expensed as depreciation each year. By spreading the cost of these chips over their useful life, the annual expense decreases, resulting in higher annual profits.
Burry believes the lifespan of these chips should be shorter, saying they should be expensed over two to three years. By extending the useful life to six years, Burry argues companies are inflating their profits.
Nvidia launched its Ampere A100 Tensor Core GPU in mid-2020. The data center GPU soon became the workhorse of AI, providing 20 times the performance of the previous generation. Yet six years after their introduction, A100 chips are still being used. Just last month, neocloud CoreWeave inked a contract to rent these semiconductors for AI processing through 2029. Far from being obsolete, nine years after they were first released.
Perhaps more telling, the price to rent these older chips is actually increasing. Just this week, in a post on X, financial market platform Ornn Exchange shared details about the use of the slightly newer Hopper H100 chips, noting that the rental price for these processors is up 22% month over month.
Huang shared the post on Tuesday, adding his own .02 cents:
NVIDIA compute is fungible, durable and highly rentable. It is a productive, revenue-generating asset. https://t.co/cvmjaNoiK8
— Jensen Huang (@JensenHuang) September 8, 2026
The evidence clearly refutes Burry's contention that the useful life of Nvidia GPUs is being overstated. As these examples clearly show, these chips are lasting far longer than their estimated useful life.
The biggest takeaway for investors is undeniable. Even as demand for Nvidia's latest generation Vera Rubin and Blackwell processors remains strong, so too does demand for its older Ampere and Hopper chips.
Moreover, this puts a nail in Burry's contention that the useful life of these chips is overstated. If anything, the estimates being used may be too short, and we don't yet know how long these AI powerhouse chips will last.
It's also worth mentioning that at 28 times earnings, Nvidia stock is a steal.
By Danny Vena, CPA – Sep 9, 2026 at 2:20PM EST

### Article 50 · 2026-09-09 · nvidia.com
New GeForce Game Ready Driver Released For 007 First Light’s Path Tracing Update, Active Matter, Aniimo & WARDOGS

By Andrew Burnes
Our new GeForce Game Ready Driver optimizes your system for 007 First Light ’s path tracing upgrade, adds support for PUBG ’s forthcoming DLSS Super Resolution update, and gets you Game Ready for Active Matter , Aniimo , and WARDOGS , three new DLSS games launching in the near future.
BULKHEAD and Team 17’s WARDOGS is an All-Out Warfare FPS that combines tactical gunplay and combined arms combat with building and destruction mechanics in a large open map, where one hundred players split across three teams fight over the control zone. The team with the most players within the Control Zone earns points, and the first team to reach 100 points wins the match. The variables in zone location and individual player tactics mean no match ever plays out the same.
Each life, you purchase a custom loadout from a wide selection of weapons, gear, utility, and vehicles to help your team win the match. Every teamplay action you perform rewards cash. From reviving squadmates, transporting friendlies to the zone, or controlling the objective. Cash persists from match to match, so spending big on better gear, equipment, or a vehicle at the right time has the potential to turn the tide of battle and could yield massive returns.
WARDOGS has wracked up over 1.5 million Wishlists, over 500,000 gamers played the August closed beta, and BULKHEAD has announced that the eagerly-anticipated shooter will officially enter Early Access on September 10th.
GeForce RTX gamers entering WARDOGS ’ warzones will discover day-one support for DLSS 4.5 Super Resolution and Dynamic Multi Frame Generation, enhancing image quality and accelerating performance, for the best possible experience. And NVIDIA Reflex will optimize PC latency, ensuring your actions occur faster, potentially giving you a competitive advantage on the game’s massive battlefields.
PUBG: BATTLEGROUNDS is the high-stakes winner-take-all free-to-play shooter that started the Battle Royale craze. Drop into diverse maps, loot unique weapons and supplies, and survive in an ever-shrinking zone where every turn could be your last.
On September 10th, the perpetually-popular PUBG will add support for DLSS Super Resolution, which players can upgrade to our latest DLSS 4.5 models by using NVIDIA app’s DLSS overrides, accelerating performance and enhancing image quality in every match and mode.
In the critically-acclaimed, multi-million selling 007 First Light , follow James Bond as a young, resourceful and sometimes reckless recruit in MI6's training program, and discover a reimagined origin story of the world’s most famous spy. Incorporating IO Interactive’s signature stealth gameplay with world class James Bond action, you’ll embark on missions in breathtaking locations around the globe, drive iconic vehicles, and dive into a cinematic adventure in pursuit of a rogue agent who’s always one step ahead.
Since launch, 007 First Light has included DLSS 4.5 Super Resolution and Dynamic Multi Frame Generation, accelerating frame rates and enhancing image quality for GeForce RTX gamers. On September 15th, path tracing and DLSS 4.5 Ray Reconstruction will be added to 007 First Light , introducing extra-immersive, extra-detailed lighting, shadows and reflections, making its levels and set pieces even more cinematic.
If you’re away from home and your GeForce RTX PC or laptop, or simply don’t have a GeForce RTX system capable of playing 007: First Light with path tracing, you can still experience the game at its very best by streaming it from the cloud to nearly any device with an Ultimate GeForce NOW membership .
Gaijin Entertainment's Active Matter is a hardcore military online PvPvE, PvE and PvP shooter set in a multiverse shattered by a quantum catastrophe. Each player controls an operative stuck in a time loop, always brought back from the dead to the same point, and enters quantum unstable zones rich with active matter - a substance capable of warping and ripping the very fabric of space and time.
Rivals from other timelines, physics-breaking anomalies that change gravitational force, and ethereal beings stand in the way. Players harvest active matter, collect the loot and extract to a safe area before the whole zone ceases to exist with everything inside it.
Active Matter launches on Steam on September 15th, following the release of an Early Version via the game’s official website last year. The launch version adds new content, and includes support for DLSS 4.5 with Super Resolution, Ray Reconstruction, and Dynamic Multi Frame Generation, which accelerate and enhance image quality, and give you the performance headroom to activate the game’s ray-traced reflections, and ray-traced shadows settings.
Gamers can also dive into Active Matter even without the latest hardware by streaming it on GeForce NOW at launch on September 15th.
Pawprint Studios' Aniimo is a free-to-play, next-gen creature-catching open-world RPG. Players can explore the vast continent of Idyll, alive with beauty and the perfect setting to capture, to Twine, to find answers and for the Aniimo themselves to reach their full potential. Challenge, race, discover... immersive exploration ensures every step of the journey is engaging. Whether they're gliding, diving, burrowing... players can step foot anywhere, solo or with friends.
Aniimo officially launches on September 16th, featuring day-one support for DLSS 4.5 with Super Resolution and Dynamic Multi Frame Generation, giving GeForce RTX enhanced image quality and accelerated performance.
And in early 2027, Aniimo will introduce support for NVIDIA ACE , enabling players to interact with their creatures:
Instead of navigating traditional menus, players will interact with their Aniimo using natural language. Chat with them, teach them new skills, and dispatch them to gather resources via voice inputs. Each Aniimo will display dynamic emotions based on player responses, fostering a more authentic and meaningful connection with the creatures that live and work alongside them.
The NVIDIA ACE integration is powered by a locally-hosted, fine-tuned Nemotron Small Language Model (SLM) running on a player’s GPU. This powers each Aniimo's intelligence, allowing them to interpret player intent and trigger in-game behavior APIs for realistic actions and reactions.
Learn more about GeForce Game Ready Drivers here , and download the new GeForce Game Ready 616.92 WHQL driver through the NVIDIA app , or from GeForce.com .

### Article 51 · 2026-09-09 · thenextweb.com
Nvidia-backed Zankore raises a $3.1bn loan to buy Nvidia GPUs for Indonesia

Zankore has secured a senior term loan facility of up to $3.1bn to buy and deploy Nvidia GPUs across Indonesia and Southeast Asia. Nvidia is one of the company’s backers and also the supplier of the hardware the financing will pay for.
Citi acted as exclusive debt adviser, while Citi, ING, Natixis CIB, Qatar National Bank and UOB served as senior mandated lead arrangers, underwriters and bookrunners.
Moreover, the deal also includes revenue-sharing and credit-support arrangements designed to link the pace of deployment to customer demand.
Zankore launched in August, just one month ago. It is backed by Indosat Ooredoo Hutchison, the Ooredoo Group, Nokia, and Nvidia.
The company sells GPU capacity for AI training, fine-tuning, inference and agentic workloads to enterprises and developers across the region.
Five international banks have now underwritten up to $3.1bn for a business with only about four weeks of operating history and a telecoms parent.
The telecoms connection helps explain how the financing came together. Indosat Ooredoo Hutchison is one of Indonesia’s largest mobile operators, with the land, power connections, regulatory position and balance sheet needed to support a large infrastructure project.
Zankore is new, but much of the infrastructure behind it is not. The credit-support arrangements appear to reflect that.
Zankore plans to start with 100MW of Nvidia infrastructure in Indonesia, reach around 200MW of capacity in the first half of 2027, and eventually build 1GW of what Nvidia calls DSX AI Factory capacity over three years.
The financing is particularly interesting because of Nvidia’s role, as the company has a stake in Zankore and supplies the GPUs that Zankore will buy with the financing. Nvidia has also spent the past year developing ways to bring outside capital into AI infrastructure projects.
TNW reported when six finance giants backed Nvidia’s $500bn plan to mobilise third-party capital for AI infrastructure, and when Nvidia began offering startups compute now and payment later.
Zankore is a straightforward example of that model. Nvidia backs the company, banks provide the financing, and Zankore uses that money to buy Nvidia’s hardware.
There is nothing improper about that structure, and the relationships are disclosed. But it does mean that some of Nvidia’s demand is now being financed through other companies’ balance sheets.
The risk of the AI infrastructure buildout is therefore shared with a growing group of lenders. If customers sign enough contracts, the model works for everyone. If demand falls short, the lenders are left with a large pool of GPUs whose value could decline as the market changes.
Indonesia is becoming an important test case for this approach. We already covered Firmus, another Nvidia-backed company building a 360MW site in Batam, based on expectations of $30bn in offtake deals.
Both companies are planning large Nvidia-powered facilities in Indonesia, with Nvidia as an investor in each. Across Southeast Asia, meanwhile, developers are planning roughly four times the data centre capacity currently in operation.
One important detail about Zankore’s loan remains unclear: what exactly secures it. Bloomberg reported last week that an Nvidia partner had found strong demand for a rare GPU-backed financing facility in Asia, which suggests the hardware itself could be part of the collateral.
A loan secured against GPUs, whose resale value depends partly on the same demand that is expected to repay the loan, carries a different risk from one secured against long-term customer contracts.

### Article 52 · 2026-09-09 · yahoo.com
Top Nvidia researcher’s family make bombshell intervention days before his cremation, claims he did not commit suicide

Top Nvidia researcher’s family make bombshell intervention days before his cremation, claims he did not commit suicide
Family of deceased Nvidia AI researcher disputes official ruling of suicide and demands halt to cremation.
Colleagues and friends of Irfan Al-Hussaini question suicide ruling, citing professional presentation hours before his death.
Family delivers formal complaint and petition to California Attorney General to stop scheduled cremation and seek re-examination of circumstances surrounding his death.
The family of a dead Nvidia AI researcher has been left baffled by an official ruling that he committed suicide — and demanded his cremation is halted.
Irfan Al-Hussaini, 32, was found unconscious in his Palo Alto home in July and died eight days later.
His family says the official ruling he killed himself does not make sense, pointing to him delivering a professional presentation hours before he was found.
"So he was fine. Everyone thought he did a good job. Everything seemed normal," his sister told NBC Bay Area. His friends also doubt he committed suicide, according to a petition calling for justice for him.
"The doctors reported that he suffered from irreversible brain damage due to lack of [blood] supply to his brain for half an hour to an hour.
"Irfan's colleagues' statements, the timeline of the 911 call, and what the doctor reported raises serious questions about what conspired that morning," they wrote.
Family members of Irfan Al-Hussaini march to hand-deliver a formal complaint and emergency petition to California Attorney General Rob Bonta's office in Sacramento.
They noted Al-Hussaini was "very successful" at work, but claimed his marriage was in "shocking disarray" and attacked his wife in a Change.org post.
His family wants his body to be preserved so physical evidence in the case can be preserved.
They went to Sacramento to deliver a formal complaint and emergency petition to California Attorney General Rob Bonta's office. The cremation is set for Thursday, which his family hopes to stop.
"We fear that important physical evidence will be lost because the body might be [cremated] anytime now, so we really want the Attorney General to step in and intervene and make sure that the body is properly investigated," his sister, Sarah Al-Hussaini, said.
The Nvidia researcher's loved ones hope a re-examination is in the works so the circumstances surrounding his death can be determined.
"Irfan's voice can no longer be heard – but we seek answers, accountability, and justice in his name. Anyone with evidence, firsthand information, or relevant experiences is urged to come forward and help bring the truth to light," his friends wrote.
California Post News : Facebook , Instagram , TikTok , X , YouTube , WhatsApp , LinkedIn
California Post Sports Facebook , Instagram , TikTok , YouTube , X
California Post App : Download here!
Home delivery : Sign up here! Page Six Hollywood : Sign up here!

### Article 53 · 2026-09-09 · fool.com
AMD and Nvidia Just Experienced an Unprecedented Valuation Split

When two companies competing in the same industry have similar operating profiles, they tend to be priced about the same in terms of valuation. The market is full of examples like this: PepsiCo and Coca-Cola , Home Depot and Lowe's , Nvidia ( NVDA +2.55% ) and AMD ( AMD +3.09% ) . However, the latter has experienced an unprecedented valuation split, and investors need to be aware of it.
Typically, there's one company that's more dominant than the other, and that company usually has a premium valuation. This is true for the stocks mentioned above, except for AMD and Nvidia. Despite Nvidia having a larger market share and growing faster than its peer, AMD is the more expensive stock. This is not a normal situation, and investors should be aware of it, as it should shape which of the stocks investors have higher exposure to.
Why is AMD stock so expensive?
Both AMD and Nvidia are growing at an impressive rate; as a result, using a trailing earnings metric like the price-to-earnings (P/E) ratio doesn't paint the full picture of where these two stocks should actually be valued. However, there is a huge gap when trailing earnings are used.
From this perspective, AMD has always been more expensive throughout the past few years as the AI arms race accelerated. However, AMD's earnings were heavily affected by profit margins that weren't optimal, thus the high valuation. AMD's margins are improving, but they're still nowhere close to Nvidia's, nor will they ever be.
Nvidia's profit margins -- which are after tax -- are actually higher than AMD's gross margins -- which are pretax. This is incredible considering these two are in a similar industry. However, when you look at the breakdown of these two businesses, it's clear that AMD will never match Nvidia's margins without a complete overhaul.
Nvidia is heavily focused on graphic processing units (GPUs) and the hardware that supports them, particularly in its data center division, which is benefiting significantly from the AI build-out. Nvidia products have been the industry standard from the beginning, and AMD hasn't been able to wrest away that leadership. In Q2, $89 billion of Nvidia's $96.2 billion total revenue came from its data center division. Because this segment is supply-constrained and Nvidia has the premium product, it can charge a higher price and make a ton of profit from these devices.
AMD has a different business. While it also has heavy exposure to data centers, that exposure is not nearly as high. In Q2, AMD's data center division generated $6.7 billion in revenue out of a total of $11.5 billion. That leaves its other divisions with a much higher share of total revenue, and these divisions don't have nearly as good an operating profile as Nvidia's data center business.
Because so much of AMD's business comes from lower-margin Client & Gaming division, it will never be able to catch Nvidia's margins in its current form.
This should secure Nvidia's place as having a higher valuation than AMD, but it doesn't. And that is a signal for investors to sell AMD and buy Nvidia instead.
If we use forward earnings, which include margin improvements and growth that AMD investors can expect, we see a stark contrast between the two that has only recently emerged.
When we utilize next fiscal year's projections, this difference is even more apparent.
Nvidia is much cheaper than AMD while also being a better business. I think investors need to take advantage of this price mismatch and scoop up shares of Nvidia , as this deal won't last forever.
By Keithen Drury – Sep 9, 2026 at 6:15AM EST

### Article 54 · 2026-09-09 · gurufocus.com
Cantor Has Strong Message for Nvidia Stock Investors

Cantor Fitzgerald has a strong message for Nvidia ( NASDAQ:NVDA ) investors after shares fell 2.1% Tuesday: market pressure has not broken its demand story.
Five-star analyst C.J. Muse reiterated a Buy rating and $350 price target, implying 55% upside from Tuesday's close. Oil prices and Middle East tensions pressured stocks, rather than company-specific deterioration.
Why Cantor Remains Bullish on Nvidia Stock
Muse expects AI infrastructure spending to keep driving Nvidia's growth, despite questions about macroeconomic pressure, debt, and supply constraints.
Valuation strengthens his argument. Based on 2028 earnings estimates, Muse considers Nvidia the cheapest stock among compute companies. That comparison suggests Nvidia's earnings could grow fast enough to make its valuation look less demanding over time, despite the stock's enormous advance.
Cantor also sees positioning as supportive. Muse said Nvidia remains under-owned by both hedge funds and long-only investment managers. If operating results continue exceeding expectations, those investors may be forced to rebuild exposure, creating an additional source of demand for the shares.
The analyst views Nvidia's reduction in certain high-bandwidth-memory specifications as a purely economic decision. He believes Nvidia is optimizing gross margin and GPU sales around a finite supply of memory bits.
Cantor is not alone. BMO Capital's Harsh Kumar recently reiterated Buy with a $340 target after Nvidia reaffirmed an estimated 70% revenue-growth outlook for fiscal 2028. Demand continues to exceed available supply.
Wall Street's broader view remains overwhelmingly bullish. Nvidia has 29 unanimous Buy ratings, while the average $325.23 target implies 44.1% upside. Shares have gained more than 21% in 2026.
The risk is that Cantor's valuation case depends on earnings nearly two years away. Competition, slower infrastructure spending, financing pressure among customers, or weaker margins could reduce those estimates.
Still, Muse's call treats Tuesday's decline as market noise. His message is that demand, valuation, and investor positioning continue strongly favoring Nvidia stock investors.

### Article 55 · 2026-09-09 · hitconsultant.net
Verily Secures Strategic Investment from NVIDIA to Accelerate Precision Health AI Platform

Verily Health Inc. has secured a strategic equity investment from NVIDIA , extending its fundraising momentum following its corporate restructuring and initial $300 million funding round in early 2026.
CU Healthcare Innovation Fund II, LP committed an additional follow-on investment, joining a capitalization syndicate that includes Alphabet (as a minority stakeholder), Series X Capital, and UCHealth.
Directly accelerates commercial deployment of the Verily Pre Platform, the enterprise data and artificial intelligence platform that harmonizes messy, fragmented clinical assets into FHIR-native, AI-ready datasets for life sciences and health systems.
Expands funding for Verily Me, the organization’s patient engagement offering designed to support individuals throughout longitudinal care journeys.
Expanding the Compute Foundation for Verily Pre and Verily Me
The capital infusion cements an operational collaboration first established between Verily and NVIDIA in October 2025.
The investment directly supports two core enterprise and consumer offerings:
Scaling the Verily Pre Platform: Serves as the central data and technical foundation across research and health system operations. By integrating NVIDIA’s full-stack accelerated computing—including NVIDIA B200 GPUs, the NeMo generative AI framework, Parabricks secondary genomic analysis, and RAPIDS accelerated data science libraries—researchers utilizing Pre Workbench can process multimodal biomedical datasets and train models at significantly higher computational efficiency and speed.
Advancing Multimodal Foundation Models (Forecast 1.0™): Leverages NVIDIA-accelerated infrastructure to scale Forecast 1.0, Verily’s proprietary foundation model that fuses genomic sequencing data directly with longitudinal EHR flowsheets to predict long-term chronic disease risk trajectories and organ decompensation.
Growing Verily Me & Agentic Patient Engagement: Funds the continued expansion of Verily Me, the company’s consumer-facing health navigation app, and its embedded conversational AI companion, Violet, to close gaps in preventive care and guide longitudinal chronic disease management.
Strategic Rationale: Cementing Independence and Accelerated Computing
The investment marks another critical milestone in Verily’s corporate evolution following its transition to an independent entity earlier this year. With Alphabet stepping back to a non-controlling minority stakeholder, Verily Health has aggressively secured strategic partners to establish vendor-neutral credibility across academic medical centers and life sciences sponsors.
By adding NVIDIA directly to its cap table, Verily secures prioritized access to high-demand next-generation AI hardware (such as Blackwell-architecture B200 accelerators), ensuring its biomedical data infrastructure remains optimized for the compute intensity of multi-omics foundation modeling.
“We are pleased to welcome NVIDIA as a new investor in Verily. These investments strengthen our ability to pursue the opportunity ahead,” said Stephen Gillett, Chairman and CEO of Verily. “Together, these investments and the continued support of our current investors accelerate our vision to build a trusted foundation for healthcare, bringing together the information and intelligence needed to power better decisions and unlock the full potential of AI across the healthcare ecosystem”.

### Article 56 · 2026-09-09 · fool.com
Prediction: $2,304 Invested in Nvidia Today Will Be Worth Triple That Amount in 5 Years

Ahead of Labor Day, you could buy 10 shares of Nvidia (NASDAQ: NVDA) for $2,304. I think those shares could be worth around $6,900 in five years, or about 3 times what the stock trades for today.
Making such a bold claim, of course, requires some proof for the skeptics. First, I'll get into what makes Nvidia special and why its momentum is likely to continue; then I'll get into the math showing how the stock could triple by 2030.
Nvidia has established itself as the biggest artificial intelligence (AI) winner since the technology started to go mainstream. That's because its graphics processing units (GPUs) are the primary chips powering AI workloads. While there is much more increased competition coming from custom AI chips and the occasional better offerings from Advanced Micro Devices and newer chip upstarts, Nvidia still finds itself in the catbird seat.
The company is the absolute dominant player in the AI training market, and this is unlikely to change. Nvidia has created a wide moat in this area with its CUDA software platform. It developed CUDA to easily program its chips and smartly seeded it among universities and research facilities doing early work on AI. The result is a generation of developers trained on its software, with most early AI code written on its platform and optimized for its chips.
Training is just part of the story, though, as inference is now growing faster and expected to eventually become the larger of the two AI computing markets. CUDA's moat is not as formidable in this area, but the company has made some good moves to remain a top player in this arena as well. Nvidia smartly "acquired" Groq and its language processing units (LPUs) earlier this year and incorporated them into its CUDA ecosystem. Inference tends to be more memory-bound than compute-bound, and LPUs have lightning-fast SRAM (static random-access memory) directly embedded in them. This reduces latency and makes them ideal for the decode phase of inference. Meanwhile, its GPUs can handle the more compute-heavy pre-fill phase.
This also speaks to Nvidia's greater strategy. The company is no longer just a GPU maker; it's become a complete AI infrastructure player. With a world-class networking portfolio, its own central processing units (CPUs), and other chips, the company can now deliver end-to-end complete rack solutions for specific AI tasks, such as training, inference, and agentic AI. At the same time, it's also acquired AI ecosystem players like SchedMD and Hugging Face (pending) to support open-source AI models and ensure that the broader developer ecosystem relies on open standards that run best on its hardware.
The market for AI infrastructure remains insatiable, and Nvidia recently projected that its revenue would grow by 70% in fiscal 2028 (ending January 2028), even though this growth is supply-constrained. To get to a $690 target in five years, I am still going to have to do a little math.
If it can produce a revenue compound annual growth rate (CAGR) of a little over 40% through 2031 (essentially its fiscal year 2032 ending in January 2031), its revenue would be around $2.3 trillion. This would mean 70% revenue growth next year and 25% revenue growth in fiscal 2032.
If the company's adjusted operating expenses rose at an average of 11% quarter over quarter through 2031 (fiscal 2032) and gross margin gradually stepped down to approximately 70%, and we apply a 15% tax rate on its operating income, Nvidia could generate over $1.1 trillion in adjusted earnings by 2031, or about $46 per share at its current share count of 24.4 billion. Place a 15 forward price-to-earnings ratio on fiscal 2032 projections for the stock, and its share price would be $690 in five years.

### Article 57 · 2026-09-09 · finance.yahoo.com
CoreWeave struggling to keep up with demand for Nvidia chips, CEO says

SAN FRANCISCO, Calif. — What's good for Nvidia ( NVDA ) looks to be good for its key partner in the AI infrastructure boom, CoreWeave ( CRWV ).
"We are struggling to meet demand every day," CoreWeave CEO Michael Intrator told Yahoo Finance from the Goldman Sachs Communacopia & Tech Conference (video above). "Every GPU we have could be sold to multiple different clients. It is a unique moment, and it continues to be."
Nvidia serves as the backbone, primary supplier, and main financial guarantor for CoreWeave's ever-expansive neocloud operation.
Beyond supplying 100% of the advanced GPUs powering CoreWeave's specialized AI data centers, Nvidia acts as a major strategic shareholder, holding an 11.5% equity stake.
Nvidia said after reporting its fiscal second quarter earnings that it sees 70% revenue growth for fiscal year 2028, above analyst forecasts for 45% growth. The sales gain would be larger — think in excess of 100% — if not for memory chip shortages , Nvidia CEO Jensen Huang said.
That demand outlook should keep CoreWeave's business humming.
CoreWeave reported that second quarter sales surged 112% year over year. Adjusted operating profits more than doubled to $1.5 billion.
Driven by explosive enterprise demand for graphics processing unit (GPU) compute and a massive $104 billion total revenue backlog, management raised its full-year 2026 revenue guidance to a range of $12.4 billion to $13.2 billion.
CoreWeave stock responded accordingly, up about 40% year to date.
"The quarter demonstrated AI demand remains robust, strengthening pricing power (25% increases across SKUs), growing software/token business, and upside surprises on margins," Citi analyst Tyler Radke wrote. "Overall, this was one of the cleaner quarters we've seen from CoreWeave since the IPO and we think shares should move meaningfully higher on increased investor confidence in the execution and improving profitability."
Nvidia's torrid growth means "that we got a lot of work to do," Intrator said.

### Article 58 · 2026-09-09 · finance.yahoo.com
Marvell Or NVIDIA: Which One Costs Less Per Dollar Of Profit?

If you own Marvell Technology (MRVL) or NVIDIA, you own one idea: the world is building AI data centers as fast as the supply chain allows. NVIDIA sells the whole factory and rents its architecture to everybody. Marvell designs the custom parts hyperscalers use to build alternatives to NVIDIA's chips. Same trend, opposite ends, which is why these two belong side by side.
What Marvell And NVIDIA Guided For Fiscal 2028
Marvell raised its fiscal 2028 revenue outlook to approximately $18 billion, up $1.5 billion in a single quarter, against the roughly $12 billion of revenue it now expects for fiscal 2027. The driver is a data center business management expects to grow more than 60% in fiscal 2028.
NVIDIA guided a full year ahead for the first time, to approximately 70% growth in fiscal 2028, and called that number supply-constrained. Marvell is guiding to what it can sell. NVIDIA is guiding to what it can build.
Marvell Is Growing Into A Lower-Margin Mix
The growth arriving at Marvell is the kind that carries a lower gross margin. The company guided non-GAAP gross margin to a range of 57.5% to 58.5% for fiscal Q3 2027 and named the ramp in custom silicon as the cause: the XPU and XPU attach parts it designs one hyperscaler at a time. The CFO expects that range through fiscal 2028, while guiding operating margin toward a 38% to 40% target range exiting fiscal 2027, reaching the high end through fiscal 2028.
The revenue lands late. Management says the custom programs in execution step up most in fiscal 2029. Shares fell 8% to $223.1 in premarket trading the morning after the report, as worry over the timing of its AI chip deal overshadowed a beat on guidance.
NVIDIA Is Widening What It Captures - And What You Pay For It
NVIDIA pulls the other way on what it captures per data center. Its revenue opportunity per gigawatt has climbed from roughly $18 billion with Hopper to $40 billion with Vera Rubin, as its platform absorbed the CPU and the networking.
NVIDIA also keeps far more of each dollar of sales: its net margin runs 63.7% against Marvell's 27.9%. Marvell's net margin sits above its own operating margin, so part of that profit is earned below the operating line. Both current margins are well above Marvell's own three-year average of roughly 1.8% operating and 0.5% net — this year's numbers are a peak, not a run rate, unlike NVIDIA's, which sit close to its own multi-year average.
The premium sits on the smaller company. At $225.41 a share on September 8, Marvell is worth about $202 billion and trades at 57.8 times operating income — on net income, where Marvell's margin runs ahead of its operating margin, that gap narrows considerably. NVIDIA is worth about $5.4 trillion and trades at 23.7 times.
NVIDIA is ahead on six of six axes: valuation, revenue growth over one year, revenue growth over three years, operating margin, net margin, and leverage. That tally still undersells Marvell: its optical DSPs are a market-leading merchant franchise and its 1.6T products are ramping rapidly.
Marvell also has the year: it rose 242.3% over the past twelve months against 34.3% for NVIDIA. That year is the trap. The last three months already turned, Marvell down 15.5% while NVIDIA gained 8.4%. If you cannot settle whether either stock earns its price, our five-factor scorecard grades both on growth, profitability, stability, resilience, and valuation.
Two things help. First, judge the pair on the numbers rather than the headlines: put Marvell and NVIDIA side by side on a peer comparison. Second, stop deciding one pair at a time. That is what the Trefis High Quality Portfolio is for. That portfolio has a track record of outpacing the three major indices.

### Article 59 · 2026-09-09 · trefis.com
Did You Already Pay For NVIDIA’s Bigger Guide?

Did You Already Pay For NVIDIA’s Bigger Guide?
NVIDIA (NVDA) trades at $225.73, about 4% below its 52-week high after a 35% total return over the past twelve months. Management has just told the market to expect a much larger revenue quarter, and the easy read is that a step that size cannot already be in the price. But the stock’s reaction suggests investors have already absorbed much of the news. The question is how much of the revenue step translates into value for shareholders.
What NVIDIA Put On The Table, And What You Paid For It
For fiscal Q3 2027 the company guided revenue to $108.0 billion, plus or minus 2% . That is 18.7% above the $91.0 billion it had guided for fiscal Q2 2027, a $17.0 billion step for that one quarter against trailing twelve-month revenue of $302.97 billion. Nothing was revised here. It is a first outlook for a new quarter , set beside the guide for the quarter before.
Across the release, from the $213.05 close before it, to the close after, the stock gained 7.0%, about $14.93 a share. That move paid for the fiscal Q2 2027 results as well as the new guide, so it is not a clean price on the guidance alone.
The $17.0 billion revenue step equates to roughly $0.45 a share at a 63.7% net margin, versus the $14.93 per-share move in the stock. That does not prove the guidance is fully priced in, but it shows why the headline revenue increase alone is not enough to establish upside.
Why NVIDIA’s Own Boom Is Raising Its Costs
The squeeze comes from the buildout that fills the order book. Management says pricing conditions in memory are extreme, that the increases have run past what it expected, and that the scarcity is driven in large part by the AI build-out itself. The customers bidding for its systems are bidding up what it pays its memory suppliers.
So the gross margin for fiscal Q3 2027 was guided 0.9 percentage points below the guide given for fiscal Q2 2027. Management expects margin to bottom at 71% to 72% in fiscal Q4 2027 before settling at 72% to 73% in fiscal 2028, and it guided operating expenses higher in the same release. The volume is guided; the cost of it has just been reset.
What You Actually Own Going Into Fiscal 2028
Management also put a full year on the table for the first time, guiding revenue to grow approximately 70% in fiscal 2028 on what it calls a supply-constrained outlook. That is a far bigger statement than one quarter’s step.
Two things carry it. Vera Rubin is shipping in production and is expected to be about 20% of data center revenue in fiscal Q3 2027. ACIE, the sovereign, NeoCloud and enterprise side of the data center business, grew 138% year over year to $40 billion in fiscal Q2 2027. Neither points to a demand problem, and memory is the supply that now sets the margin.
So you own a volume number management says it can already supply; against a cost line it has told you gets worse before it improves. Before adding, it is worth seeing how other stocks have actually traded through their own earnings releases , because a step already in the price pays you nothing.
How Much Should You Bet On One Company’s Forecast?
A raised outlook is a genuine positive, and it is still one company’s forecast. Concentration tends to arrive by accident rather than by decision. What your largest position would do to your net worth is exactly what the Trefis Wealth team computes, with the same rules-based systematic discipline that runs our High Quality Portfolio. Request a free vulnerability audit of your biggest positions .

### Article 60 · 2026-09-09 · zacks.com
NVIDIA Bets Big on Hugging Face: ETFs to Win

NVIDIA NVDA has confirmed its plan to acquire Hugging Face, a New York-based startup known for its open-source artificial intelligence (AI) model repository. The deal, valued at $12.9 billion, represents NVIDIA's second-largest acquisition after its $20 billion purchase of chipmaker Groq's assets, as quoted on CNBC.
The acquisition price underscores the strategic value of Hugging Face as the AI industry continues to expand.
Hugging Face has emerged as a major platform for developing, sharing and running AI models, particularly open-weight models that developers can modify and host themselves.
According to Huang, roughly half of NVIDIA's business is driven by open models. NVIDIA is also a major developer of open AI models, making Hugging Face a natural fit with its broader AI strategy.
Beyond open-source AI, Hugging Face provides infrastructure and collaboration tools for organizations developing proprietary AI systems. The platform has more than 18 million users, hosts over 3 million models and 500,000 datasets, and is used by more than 200,000 companies, according to NVIDIA, as quoted on CNBC.
The acquisition could also give NVIDIA deeper insight into how AI developers and customers are using the technology.
Forrester analyst Naveen Chhabra said NVIDIA could gain visibility into which AI models are gaining popularity, what datasets developers are accessing and which architectures are attracting interest before broader market trends emerge, per the same CNBC article.
NVIDIA has lately positioned itself beyond its traditional role as a chipmaker by investing in companies across the AI value chain and helping fund GPU purchases through increasingly sophisticated arrangements.
Hugging Face CEO Clément Delangue told CNBC recently that China is winning the AI race with open-weight models. He expects Chinese tools to catch up to the U.S. frontier labs by the end of 2026 or in 2027.
Meanwhile, the accelerating U.S.-China AI race is drawing greater attention to America's dependence on China for certain components used in AI data centers.
Growing scrutiny of these supply chains could raise costs, creating further challenges for the massive infrastructure buildout needed to support AI growth. Hence, focusing on open-source AI models and their acquisition could prove to be a lucrative investment opportunity.
Are Open-Source Models Better for Cybersecurity?
Delangue, a strong advocate of open-source AI, sees open models playing a key role in the growing AI cybersecurity market, as quoted on CNBC. Their flexibility, transparency and ability to run within private environments make them useful for detecting evolving threats while keeping sensitive data under organizational control.
Against this backdrop, NVIDIA's recent investment in Hugging Face appears well aligned with the growing demand for open-source models.

### Article 61 · 2026-09-09 · gurufocus.com
Nvidia Just Found Another Way to Finance the AI Boom

Nvidia Corp. ( NVDA , Financials ), the semiconductor company behind the GPUs powering much of the AI boom , is getting another large infrastructure project off the ground in Southeast Asia.
AI platform Zankore secured a senior term loan facility of up to $3.1 billion to fund Nvidia-powered GPU and cloud infrastructure in Indonesia.
Citi served as exclusive debt adviser, with Citi, ING, Natixis, Qatar National Bank and United Overseas Bank among the lenders.
Zankore plans to begin with 100 megawatts of Nvidia infrastructure before expanding toward 1 gigawatt of AI factory capacity. The scale matters.
Most of Nvidia's largest AI customers have been U.S. hyperscalers and technology companies. Zankore gives the chipmaker another path into fast-growing markets where customers may need outside financing to fund expensive GPU deployments.
The structure also includes revenue-sharing and credit-support arrangements designed to tie deployment more closely to customer demand.
That can help projects get financed, but it also shifts more attention toward the quality of the demand behind Nvidia's hardware sales.
For investors, the next thing to watch is whether similar financing structures begin unlocking more multibillion-dollar GPU orders across Asia and other emerging AI markets.

### Article 62 · 2026-09-09 · fortune.com
AGI is here, Nvidia CEO Jensen Huang has declared. Here’s why the market doesn’t care

By Eva Roytburg
AGI, the technology once imagined to both destroy and enrich human civilization, has arrived, Nvidia chief Jensen Huang declared over the weekend.
OpenAI’s newest model, Astra (“stars” in Latin), has achieved the goal, Huang wrote on X on Sunday, after training on 100,000 Grace Blackwell chips (an earlier post said 300,000 before he deleted it). His post was received with a healthy mix of supporters and detractors: Jim Cramer said Nvidia was winning from the release, and crypto CEO Hunter Horsely said Huang was the “most credible referee.” But others had questions: Did Jensen not, asked AI critic Gary Marcus, have a financial incentive to declare AGI?
Markets got their first chance to weigh in Tuesday after the long Labor Day weekend. CoreWeave, battered by months of suspicion over its debt, exploded up 15%. SoftBank notched another 2%. But the hefty, lumbering Nvidia shed 2%. The last time Huang declared AGI (he’s done it twice before , by Fortune ‘s count), on Lex Fridman’s podcast in March, the stock fell 0.3%. So it follows that markets don’t believe Huang, or AGI has already been priced in.
“If you look in a slightly different place,” Gil Luria, head of technology research at D.A. Davidson, told Fortune , “you’ll see that the market is responding.” Indeed, the companies most leveraged to OpenAI—SoftBank, Oracle , CoreWeave—are the ones whose stocks are up. Astra, he added, “puts OpenAI as the state-of-the-art model, which they haven’t been in about a year.”
Nvidia, on the other hand, has been the dominant market player since 2024; it’s “too big to grow,” Luria said. Two weeks ago, Nvidia reported the most profitable quarter in capitalism’s history: $96 billion in quarterly revenue, up 106% from a year earlier, and guided to $108 billion for the current quarter. “They’re so good that nobody believes it can continue,” Luria said. For traders, the stock is more like a source of funds you pull from, rather than something you buy and sell based on individual news about the AI race— it’s what you sell to buy CoreWeave. That’s also why Luria shrugged off board member Mark Stevens’ filing last week to sell up to $1 billion of his shares. “Good for him.”
But what of AGI? Huang defined the word himself to Fridman in March as the ability to create a $1 billion company, but made no mention of that benchmark in his X post Sunday. Can Astra build such a company? Theoretically, Luria said—but until we see a billion-dollar business built by one person with an AI model, or an agent by an agent alone, “it’s a hypothetical.”
AI researchers have a stricter test. A widely cited definition describes AGI as an AI that can match or surpass the “cognitive versatility and proficiency of a well-educated adult.” Marcus and Miles Brundage, a researcher who quit OpenAI in 2024 over safety concerns, created a 10-point list to make that tangible: a well-educated adult can write an Oscar-caliber screenplay, laugh at the right moments in a movie, and master a new video game within hours.
By that standard, “we just absolutely have not achieved AGI, even though the models are astounding,” said Basil Halperin, an economist at the University of Virginia who co-wrote a widely circulated 2023 analysis arguing that financial markets don’t anticipate transformative AI for decades. He ran his own test last weekend, where he asked GPT-5.6 to move his old iTunes playlists to Spotify . “It got the job done. But I had to sit there babysitting it for three hours.”
Still, a spectacular new model release should beget more compute demand, which begets a higher stock price for Nvidia, or at least for the hyperscalers selling compute—right? Wrong, Halperin argues. Stocks, he said, “are a giant pain in the butt because they reflect many different things.” The two leading labs are private. Maybe existential risk, or cybersecurity risk, would could push equities down, rather than up, as investors flee to Treasuries and gold. And competition between OpenAI and Anthropic could leave the industry “kind of like Uber and Lyft—they earn money, but they’re not as profitable as Google or Apple .”
Where you would actually see AGI show up, Halperin argues, is in real interest rates. If AI raises growth, it raises interest rates, since rates are the expected discounted value of future earnings. And since a stock is the discounted value of its future earnings, higher rates shrink the present value of future profits, meaning a real AGI could, theoretically, make Nvidia’s stock fall.
The real interest rate—also known as the yield on inflation-protected Treasuries with inflation stripped out (TIPS)—is the cleaner signal of AGI. Halperin’s rule of thumb is that every percentage point of extra growth should add roughly a percentage point to real rates. So when Sam Altman and Dario Amodei talk tough about growth of 5% or 10% or more, they are describing a world where real rates sit near 10%. “Those will just swamp everything else, if those are actually going to come.”
But now, they’re not. They haven’t. Real interest rates have climbed an enormous three to four percentage points since 2021, and Halperin attributes some of that to hyperscalers’ capex, sitting at now running around 2% of GDP a year. But that’s nowhere near a singularity, and Astra didn’t add much to it at all. In fact, Halperin pointed to a paper by MIT economists Isaiah Andrews and Maryam Farboodi that found that long-term Treasury yields have on average fallen by more than a tenth of a percentage point around major model releases, and stayed down for weeks, a pattern that “would suggest that the market on average has been disappointed.”
The efficient market is thus aggregating the views of the general public, rather than those on X. A survey Halperin helped run tested the expectations of groups from normal people to AI researchers and found that most expect AI to add about half a percentage point to GDP growth. On one hand, that’s enormous. On the other, it’s nothing.
Halperin’s own forecast for the next five years is like “the dot-com boom, but twice as fast and twice as hard. Not the singularity. Not yet.” That seems to be what the markets are saying too.
Eva previously covered macroeconomics, market-moving news, and the forces shaping the global economy as a reporter at Fortune.

### Article 63 · 2026-09-10 · NVIDIA Corporation
d-Matrix Adopts NVIDIA NVLink Fusion for Rack-Scale XPU Deployment | NVIDIA Blog

d-Matrix Adopts NVIDIA NVLink Fusion for Rack-Scale XPU Deployment | NVIDIA Blog
d-Matrix Adopts NVIDIA NVLink Fusion for Rack-Scale XPU Deployment
d-Matrix will connect its next-generation Raptor XPUs to NVIDIA’s AI infrastructure platform with NVLink Fusion, joining a growing ecosystem of partners using NVIDIA’s rack-scale architecture to accelerate time to market.
AI inference chipmaker d-Matrix today announced it will use NVLink Fusion to connect its next-generation Raptor XPUs to NVIDIA’s AI infrastructure platform — joining a growing roster of ecosystem partners.
By connecting Raptor to NVIDIA NVLink scale-up and Spectrum-X scale-out networking, the NVIDIA MGX rack architecture and the broader NVIDIA AI platform, NVLink Fusion gives d-Matrix an accelerated, lower-risk path from custom silicon to large-scale deployment.
“Demand for inference is soaring, but capital, time and energy remain finite,” said Sid Sheth, cofounder and CEO of d-Matrix during a press briefing yesterday. “With NVLink Fusion and MGX, we can integrate our Raptor XPUs into a broadly deployed, liquid-cooled architecture, giving customers a faster, lower-risk path to deploy and scale ultralow-latency inference.”
The NVIDIA AI platform is vertically integrated and horizontally open. NVLink Fusion extends this openness to XPUs and CPUs, allowing silicon companies to focus on their processor innovations while using NVIDIA infrastructure to deploy them at AI factory scale.
From Custom Silicon to Rack-Scale Deployment
Building an XPU is only the first step. Deploying it at AI factory scale requires a complete platform spanning networking, rack architecture, power, cooling, software and a proven supply chain. Each of the steps — sourcing chips, integrating high-speed interfaces, validating a scale-up networking solution, designing and certifying rack architecture — adds time, costs and risks.
NVLink Fusion lets silicon innovators connect directly into NVIDIA’s proven platform . It’s the high-bandwidth, low-latency technology that connects custom XPUs and CPUs to the NVIDIA stack.
By adopting NVLink Fusion, d-Matrix can tap into the NVIDIA MGX ecosystem’s mature, validated rack designs, supply chain, power and cooling infrastructure. By standardizing on a common rack, data centers can be built once and support GPUs, CPUs and XPUs — without requiring a separate rack architecture for each processor type.
NVLink Fusion Integrates d-Matrix XPUs Into AI Factories
Using NVIDIA NVLink, d-Matrix plans to connect its XPUs in a single high-bandwidth, low-latency scale-up domain. Its racks can also work alongside NVIDIA GPU-based systems like NVIDIA Vera Rubin NVL72 for disaggregated inference.
d-Matrix also plans to integrate NVIDIA Vera CPUs, NVIDIA ConnectX-9 SuperNICs, NVIDIA BlueField-4 DPUs and NVIDIA Spectrum-X Ethernet networking. Together with NVLink and MGX, these technologies give d-Matrix a proven foundation to deploy specialized inference alongside NVIDIA systems within flexible, unified AI factories.
NVLink Fusion Opens NVIDIA AI Factories to Specialized XPU Architectures
The NVIDIA full-stack AI factory platform includes NVIDIA Vera Rubin NVL72, Groq 3 LPX, the Vera CPU rack, Vera BlueField-4 STX storage and Spectrum-6 SPX Ethernet networking. It’s designed to be completely fungible — running every AI workload, model and model architecture — with the best performance per watt and lowest cost per token.
NVLink Fusion gives customers the flexibility to match the right compute to each workload within a common AI factory platform, opening access to NVIDIA networking, systems, software and global supply chain. Silicon innovators like d-Matrix can use NVLink Fusion to increase performance, accelerate time to market and reduce the risk of deploying semi-custom AI factories.
What is NVIDIA NVLink Fusion?
NVLink Fusion is the high-bandwidth, low-latency technology that connects third-party custom XPUs and CPUs to NVIDIA’s AI infrastructure. It provides NVLink scale-up networking, the NVIDIA MGX rack architecture, and access to the full AI factory platform spanning compute, networking, storage, security, power, cooling and software.
What problem does NVLink Fusion solve?
Building a custom XPU only the first step. Deploying one at scale requires rack architecture, cooling and power validation, system management software and a supply chain that can deliver at volume, which can cost billions of dollars and take years. NVLink Fusion lets silicon innovators skip that work and connect directly into NVIDIA’s proven, globally deployed AI factory platform.
Who are the NVLink Fusion partners?
Adopters include AWS, which is designing Trainium4 to integrate with NVLink Fusion, and d-Matrix, a custom inference accelerator provider. The technology ecosystem spans CPU, ASIC design, IP and optical interconnect partners including Alchip, Arm, Astera Labs, Ayar Labs, Cadence, Fujitsu, GUC, Intel, Lightmatter, Marvell, MediaTek, Samsung, SiFive and Synopsys.
What CPU architectures does NVLink Fusion support?
NVLink Fusion is CPU architecture-agnostic and supports Arm, x86 and RISC-V. Partners connect their CPUs using NVLink-C2C, which delivers up to 6x the energy efficiency of a PCIe interface.
What is the difference between NVLink and NVLink Fusion?
NVLink is NVIDIA’s scale-up interconnect between NVIDIA GPUs. NVLink Fusion extends that same interconnect, plus the surrounding rack architecture and ecosystem, to hyperscalers, AI-native companies, and custom silicon innovators who want to take advantage of NVLink scale-up, the NVIDIA AI infrastructure platform, and NVLink Fusion ecosystem.
Who is NVLink Fusion for?
Hyperscalers, AI-native companies and custom silicon innovators deploying their own XPUs or CPUs.

### Article 64 · 2026-09-10 · NVIDIA Corporation
How the World’s Robotaxi Leaders Are Building With NVIDIA Technologies | NVIDIA Blog

How the World’s Robotaxi Leaders Are Building With NVIDIA Technologies | NVIDIA Blog
Physical AI Takes the Wheel: How the World’s Robotaxi Leaders Are Building With NVIDIA Technologies
NVIDIA’s modular, full-stack robotaxi pipeline — a three-computer solution spanning AI training, simulation and in-vehicle computing — is being adopted across the robotaxi ecosystem.
The global robotaxi market — physical AI’s first commercial breakthrough — is projected to reach $400 billion by 2035 , with over 6 million commercial vehicles in operation as driverless fleets are already moving people through some of the world’s busiest and most complex streets.
Deploying a driverless vehicle is one challenge. Scaling a fleet is a next-level computing challenge; it means delivering the same safe, reliable performance across thousands of vehicles.
Meeting those demands requires enormous amounts of compute across the robotaxi development lifecycle, from preparing and training AI models to simulating and validating driving behavior, as well as real-time processing in the vehicle.
NVIDIA provides an open platform for AI training , simulation and safety validation , with libraries, software development kits, workflows and models that developers can use alongside their own technology stacks.
Every major robotaxi program operating at commercial scale today is running on NVIDIA’s modular stack, spanning AI training, simulation, in-vehicle computing — or a combination of the three — to develop and deploy fleets at scale.
What Is a Robotaxi Technology Stack?
A robotaxi technology stack is the end-to-end set of technologies used to develop, validate and deploy autonomous vehicles (AVs) — from data and AI model training to simulation, safety validation and real-time in-vehicle computing.
NVIDIA’s robotaxi and AV platform brings these capabilities together in a three-computer solution: the model training computer, simulation and validation computer, and in-vehicle computer.
1. Training Computer: NVIDIA DGX
Robotaxi intelligence advances as programs turn growing volumes of fleet data into increasingly capable models. Driving models can be trained on NVIDIA DGX systems.
The NVIDIA Alpamayo portfolio of open reasoning vision language action (VLA) models, simulation frameworks and physical AI datasets gives developers building blocks they can adapt to their own data, requirements and technology stacks. Its reasoning models help address long-tail AV challenges by breaking complex driving situations into smaller steps, reasoning through each one and selecting the safest trajectory.
NVIDIA also provides physical AI datasets, reinforcement learning blueprints and recipes for post-training and distillation, helping developers optimize models for their target vehicles.
On a challenging autonomous driving evaluation, adding meta-action and chain-of-thought reasoning data improved a VLA model’s trajectory prediction accuracy, reducing minimum average displacement error — the predicted path’s average deviation from the reference route — by 43%, from 2.08 to 1.18.
2. Simulation and Validation Computer: NVIDIA Omniverse and Cosmos on NVIDIA RTX PRO
Robotaxi programs can’t rely on physical miles alone to capture rare, long-tail driving scenarios. NVIDIA Omniverse NuRec models reconstruct real-world driving scenarios from sensor data, while NVIDIA Cosmos world foundation models generate physically based variations of them, enabling developers to turn thousands of real-world corner cases into millions of combinations of driving behavior, traffic, weather, lighting and sensor conditions.
From real-world corner cases to thousands of synthetic permutations spanning behavior and content, NVIDIA Cosmos variations expand AV training data and accelerate model deployment.
Running on NVIDIA RTX PRO Servers , NVIDIA Omniverse and Cosmos support closed-loop simulation and validation. The NVIDIA AlpaSim simulation framework extends the workflow for training and evaluating reasoning-based autonomous-driving models, helping developers identify weaknesses before deployment.
3. In-Vehicle Computer and Sensor Architecture: NVIDIA Hyperion With DRIVE AGX
NVIDIA Hyperion is NVIDIA’s modular in-vehicle compute and sensor reference architecture for level-4-ready robotaxis. Hyperion 10 pairs dual NVIDIA DRIVE AGX Thor systems-on-a-chip, built on the NVIDIA Blackwell platform , with 14 high-definition cameras, nine radars, three lidars and 12 ultrasonics for real-time, 360-degree sensor fusion. Its redundant compute and sensing design supports fail-operational driving if a sensor or compute component fails.
The dual DRIVE AGX Thor is designed to run modern AI workloads — including VLA models — for perception, reasoning, path planning and driving actions.
NVIDIA Halos provides a production-ready safety foundation through Halos OS, and a broader validation and certification framework spanning independent inspection, system validation, large-scale simulation and continuous testing from cloud to car.
Robotaxi Leaders Adopting NVIDIA’s Robotaxi Technology Stack
NVIDIA’s robotaxi ecosystem spans every region where commercial robotaxi services are emerging today: Asia, Europe, the Middle East and North America. Across these markets, mobility providers, AV developers and automakers are adopting NVIDIA’s three-computer architecture to train AI models, simulate and validate driving behavior, and deploy autonomous vehicles at scale.
Uber is scaling its fleet of NVIDIA Hyperion, with plans to reach 28 cities by 2028. Uber and NVIDIA are also building a robotaxi AI data factory on NVIDIA Cosmos to curate fleet driving data for rare scenarios. Together, Uber and NVIDIA are collaborating with Autobrains, Avride, Lucid, May Mobility, Mercedes-Benz, Momenta, Nissan, Nuro, Pony.ai, Stellantis, Waabi, Wayve, WeRide and Zoox to bring NVIDIA-powered robotaxi services to the Uber platform.
May Mobility is planning to operate autonomous ride-hailing services through Uber’s network, while developing its software stack on the NVIDIA DRIVE platform. May Mobility has also launched an autonomous ride-hailing pilot with Lyft in Atlanta, built on the NVIDIA DRIVE platform.
Bolt uses NVIDIA technologies to develop and scale AVs across Europe.
Lyft plans to use NVIDIA Hyperion as a reference architecture for future autonomous fleets.
Through its partnership with Grab , WeRide plans to bring its Hyperion- and DRIVE AGX Thor-based GXR to key markets across Southeast Asia.
Waymo partners with NVIDIA to help build its autonomous computing system.
Behind these services, AV developers are using NVIDIA accelerated computing, simulation and in-vehicle platforms to build the intelligence that operators and automakers deploy.
Wayve , Nissan a nd Uber are developing a global robotaxi program using a prototype vehicle that combines Nissan’s vehicle engineering, Wayve’s embodied AI and the NVIDIA Hyperion platform.
Autobrains is developing robotaxi programs with Uber in Munich and VinFast in Southeast Asia, built on NVIDIA Hyperion and enabled by Autobrains’ Agentic AI technology.
Zoox uses NVIDIA DRIVE for in-vehicle computing and cloud-based training and simulation.
Momenta is developing its software stack based on NVIDIA DRIVE AGX running on DriveOS.
Pony.ai developed its new-generation autonomous-driving domain controller with NVIDIA Hyperion and DRIVE AGX Thor.
Tensor is developing its level 4 Robocar with eight NVIDIA DRIVE AGX Thor systems-on-a-chip in its in-vehicle supercomputer.
Waabi expands into the robotaxi market through a deployment collaboration with Uber ; its Waabi Driver platform is built on NVIDIA DRIVE AGX Thor.
TIER IV and Isuzu are deploying level 4 autonomous buses built on NVIDIA Hyperion and DRIVE AGX Thor.
Lenovo is supplying its NVIDIA DRIVE AGX Thor-based AD1 level 4 domain controller for a next-generation robotaxi program with SWM .
DeepRoute.ai is developing a new generation of robotaxis built on the NVIDIA Hyperion platform with DRIVE AGX Thor.
As these systems move from development into production, automakers are integrating NVIDIA technology into autonomous and robotaxi-ready vehicle programs.
Tesla trains its autonomous-driving neural networks on NVIDIA supercomputers.
Mercedes-Benz and NVIDIA are collaborating with Uber to develop a robotaxi ecosystem based on the new S-Class, built on the NVIDIA Hyperion architecture, full-stack NVIDIA DRIVE AV L4 software, and NVIDIA Alpamayo open AI models, simulation tools and datasets to support reasoning-based, safety-first autonomy.
Stellantis, Wayve and Uber are collaborating to develop and deploy L4 driverless mobility services, leveraging NVIDIA Hyperion and AI computing technologies.
Lucid , Nuro and Uber are developing a global robotaxi service using NVIDIA DRIVE AGX Thor, part of the Hyperion platform.
Hyundai Motor and Kia are expanding their collaboration with NVIDIA to develop data-driven autonomous-driving systems built on NVIDIA Hyperion. NVIDIA will also explore expanded collaboration with Hyundai Motor Group’s joint venture, Motional , to advance level 4 robotaxi services.
Geely , alongside its ecosystem partners, plans to develop and commercialize robotaxis using Hyperion.
Zeekr , a Geely Auto Group brand, has adopted DRIVE AGX Thor for a centralized domain controller.
From cloud to car, nearly every layer of the robotaxi platform is being developed on NVIDIA accelerated computing.
Explore NVIDIA’s complete platform for robotaxi development .

### Article 65 · 2026-09-10 · NVIDIA Corporation
NVIDIA and Palantir Bring Sovereign Intelligence to Critical Supply Chains | NVIDIA Newsroom

NVIDIA and Palantir Bring Sovereign Intelligence to Critical Supply Chains | NVIDIA Newsroom
NVIDIA and Palantir Bring Sovereign Intelligence to Critical Supply Chains
September 10, 2026
Collaboration establishes an AI stack combining Palantir sovereign AI and custom NVIDIA Nemotron open models for complex supply chain operations.
The AI stack is first being deployed within NVIDIA’s supply chain to codify operational intelligence and accelerate the path from wafer to first token.
Organizations can optimize their own supply chains through the Palantir Sovereign AI Operating System Reference Architecture running on cloud or on-premises infrastructure.
Palantir Technologies Inc. (NASDAQ: PLTR) and NVIDIA (NASDAQ: NVDA) today announced a collaboration to bring sovereign AI to critical supply chains, starting with NVIDIA’s own operations .
The deployment creates an AI stack that brings NVIDIA Nemotron ™ open models into Palantir Foundry and Artificial Intelligence Platform (AIP), grounded in the Palantir Ontology, which aims to create unprecedented supply chain visibility, identify constraints, continuously codify operational expertise and guide decisions at machine speed — maintaining the reliability and efficiency of NVIDIA’s AI infrastructure supply chain while retaining control and ownership of proprietary data.
The AI stack powering this work and its applications across industries will be showcased in depth at Palantir’s AIPCon 11 conference . Organizations across complex industries — including agriculture, manufacturing, pharmaceutical, retail, technology and governments — can use the AI stack to optimize their own unique supply chain operations.
NVIDIA operates one of the most complex supply chains, spanning millions of parts, thousands of suppliers and a global network of manufacturing partners. Bringing a rack-scale AI system to production requires the coordinated availability of compute, memory, networking, power, cooling and mechanical components. As demand for AI infrastructure accelerates, NVIDIA works closely with its ecosystem to secure supply for the 1.3 million parts in each NVIDIA Vera Rubin rack and scale AI infrastructure faster.
“NVIDIA has arguably the most valuable, intricate and complex supply chain in the world. Our sovereign stack, powered by Nemotron models and Ontology, is delivering capabilities that exceed the frontier while providing alpha protection qualities unavailable otherwise,” said Alex Karp, cofounder and CEO of Palantir Technologies. "We are very proud of our partnership and its cornerstone role in the sovereign AI revolution.”
“Supply chains are the operating system of the physical economy, and AI factories are among the most complex systems ever built,” said Jensen Huang, founder and CEO of NVIDIA. “From wafers and components to manufacturing, systems and customer delivery, hundreds of companies and trillions of dollars of global economic activity come together to deliver AI infrastructure. NVIDIA and Palantir are transforming this vast operational graph into sovereign intelligence — combining NVIDIA Nemotron models with Palantir’s Ontology to reason, plan and orchestrate the journey from wafer to token.”
Open Models, Customized for Organization-Specific Decisions
Palantir customers can create their own supply chain AI stack by post-training NVIDIA Nemotron with their own data using Palantir Foundry and AIP. Within Palantir AIP, NVIDIA cuOpt ™ software unlocks optimizations and scenario planning, enabling teams to model supply constraints, assess tradeoffs and understand the operational impact of allocation decisions. Post-trained NVIDIA Nemotron open models recommend actions, explain tradeoffs and flag emerging risks, while supply chain experts retain control of final decisions.
The new AI stack gives NVIDIA supply chain teams a shared command center to reduce time of ownership, beginning with materials allocation decisions that affect how quickly parts move through the supply chain. The system helps teams identify potential constraints earlier, evaluate alternatives more quickly and allocate materials based on end-to-end production impact.
Open models are central to this approach. Every organization’s value chain, supplier network, operating constraints and decision criteria are different; a general-purpose model cannot capture that unique context on its own. By customizing Nemotron open models with proprietary operational data, prepared and augmented using NVIDIA NeMo™ Data Libraries, enterprises can build AI that reflects how their business operates while retaining control over their models, data and deployment environment.
Each recommendation, planner action and production outcome strengthens the system. Integrated with the NVIDIA NeMo AutoModel and NeMo RL libraries, Palantir Autopilot operationalizes that feedback to support continued model improvement. This creates a governed learning loop that preserves operational knowledge, measures decisions against real-world results and improves the specialized AI models supporting the workflow.
Built for Sovereign, Enterprise-Scale Deployment
The companies plan to extend the learnings from NVIDIA’s deployment to help enterprises build more resilient, responsive and intelligent supply chains. Across manufacturing, energy, healthcare, automotive and aerospace, the approach can help turn fragmented operational data into faster, more resilient decisions while retaining control and ownership of proprietary data.
Given the sensitivity and criticality of NVIDIA’s supply chain, the deployment runs on NVIDIA reference architectures and the jointly developed Palantir Sovereign AI Operating System Reference Architecture (SAIOS), which is supported by Dell Technologies and Cisco .
Every supply chain is different. This AI stack can be deployed on premises with leading system manufacturers including Cisco, and Dell, or in the co-lo and cloud with Rackspace and Nebius — enabling organizations to run AI where their data, systems and operational requirements demand it.
About Palantir Technologies Inc.
Foundational software of tomorrow. Delivered today. Additional information is available at https://www.palantir.com .
Certain statements in this press release including, but not limited to, statements as to: NVIDIA and Palantir transforming operational graph into sovereign intelligence—combining NVIDIA Nemotron models with Palantir’s Ontology to reason, plan and orchestrate the journey from wafer to token; expectations with respect to supply chain; expectations with respect to growth, performance, availability, and benefits of NVIDIA’s products, services and technologies, and related trends and drivers; expectations with respect to NVIDIA’s third party arrangements, including with its collaborators and partners; expectations with respect to technology developments, and related trends and drivers; projected market growth and trends; expectations with respect to AI and related industries; and other statements that are not historical facts are forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended, which are subject to the “safe harbor” created by those sections based on management’s beliefs and assumptions and on information currently available to management and are subject to risks and uncertainties that could cause results to be materially different than expectations. Important factors that could cause actual results to differ materially include: global economic and political conditions; NVIDIA’s reliance on third parties to manufacture, assemble, package and test NVIDIA’s products; the impact of technological development and competition; development of new products and technologies or enhancements to NVIDIA’s existing products and technologies; market acceptance of NVIDIA’s products or NVIDIA’s partners’ products; design, manufacturing or software defects; changes in consumer preferences or demands; changes in industry standards and interfaces; unexpected loss of performance of NVIDIA’s products or technologies when integrated into systems; NVIDIA’s ability to realize the potential benefits of business investments or acquisitions; and changes in applicable laws and regulations, as well as other factors detailed from time to time in the most recent reports NVIDIA files with the Securities and Exchange Commission, or SEC, including, but not limited to, its Annual Report on Form 10-K and Quarterly Reports on Form 10-Q. Copies of reports filed with the SEC are posted on NVIDIA’s website and are available from NVIDIA without charge. These forward-looking statements are not guarantees of future performance and speak only as of the date hereof, and, except as required by law, NVIDIA disclaims any obligation to update these forward-looking statements to reflect future events or circumstances.
Palantir Forward-Looking Statements
This press release contains forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended. These statements may relate to, but are not limited to, Palantir's expectations regarding the amount and the terms of the contract and the expected benefits of Palantir's software platforms. Forward-looking statements are inherently subject to risks and uncertainties, some of which cannot be predicted or quantified. Forward-looking statements are based on information available at the time those statements are made and were based on current expectations as well as the beliefs and assumptions of management as of that time with respect to future events. These statements are subject to risks and uncertainties, many of which involve factors or circumstances that are beyond Palantir's control. These risks and uncertainties include the ability to meet the unique needs of customers; the failure of Palantir's platforms to satisfy customers or perform as desired; the frequency or severity of any software and implementation errors; Palantir's platforms' reliability; and customers' ability to modify or terminate the contract. Additional information regarding these and other risks and uncertainties is included in the filings Palantir makes with the Securities and Exchange Commission from time to time. Except as required by law, Palantir does not undertake any obligation to publicly update or revise any forward-looking statement, whether as a result of new information, future developments, or otherwise.
Lisa Gordon
Palantir
media@palantir.com
Palantir and NVIDIA
About Palantir Technologies Inc.
Foundational software of tomorrow. Delivered today. Additional information is available at https://www.palantir.com .
Certain statements in this press release including, but not limited to, statements as to: NVIDIA and Palantir transforming operational graph into sovereign intelligence—combining NVIDIA Nemotron models with Palantir’s Ontology to reason, plan and orchestrate the journey from wafer to token; expectations with respect to supply chain; expectations with respect to growth, performance, availability, and benefits of NVIDIA’s products, services and technologies, and related trends and drivers; expectations with respect to NVIDIA’s third party arrangements, including with its collaborators and partners; expectations with respect to technology developments, and related trends and drivers; projected market growth and trends; expectations with respect to AI and related industries; and other statements that are not historical facts are forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended, which are subject to the “safe harbor” created by those sections based on management’s beliefs and assumptions and on information currently available to management and are subject to risks and uncertainties that could cause results to be materially different than expectations. Important factors that could cause actual results to differ materially include: global economic and political conditions; NVIDIA’s reliance on third parties to manufacture, assemble, package and test NVIDIA’s products; the impact of technological development and competition; development of new products and technologies or enhancements to NVIDIA’s existing products and technologies; market acceptance of NVIDIA’s products or NVIDIA’s partners’ products; design, manufacturing or software defects; changes in consumer preferences or demands; changes in industry standards and interfaces; unexpected loss of performance of NVIDIA’s products or technologies when integrated into systems; NVIDIA’s ability to realize the potential benefits of business investments or acquisitions; and changes in applicable laws and regulations, as well as other factors detailed from time to time in the most recent reports NVIDIA files with the Securities and Exchange Commission, or SEC, including, but not limited to, its Annual Report on Form 10-K and Quarterly Reports on Form 10-Q. Copies of reports filed with the SEC are posted on NVIDIA’s website and are available from NVIDIA without charge. These forward-looking statements are not guarantees of future performance and speak only as of the date hereof, and, except as required by law, NVIDIA disclaims any obligation to update these forward-looking statements to reflect future events or circumstances.
Palantir Forward-Looking Statements
This press release contains forward-looking statements within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended. These statements may relate to, but are not limited to, Palantir's expectations regarding the amount and the terms of the contract and the expected benefits of Palantir's software platforms. Forward-looking statements are inherently subject to risks and uncertainties, some of which cannot be predicted or quantified. Forward-looking statements are based on information available at the time those statements are made and were based on current expectations as well as the beliefs and assumptions of management as of that time with respect to future events. These statements are subject to risks and uncertainties, many of which involve factors or circumstances that are beyond Palantir's control. These risks and uncertainties include the ability to meet the unique needs of customers; the failure of Palantir's platforms to satisfy customers or perform as desired; the frequency or severity of any software and implementation errors; Palantir's platforms' reliability; and customers' ability to modify or terminate the contract. Additional information regarding these and other risks and uncertainties is included in the filings Palantir makes with the Securities and Exchange Commission from time to time. Except as required by law, Palantir does not undertake any obligation to publicly update or revise any forward-looking statement, whether as a result of new information, future developments, or otherwise.

### Article 66 · 2026-09-10 · es.tradingview.com
Nvidia CEO Reportedly Dismisses Anthropic Exec's AI Doomsday Warning As ‘Outlandish’ And ‘Deeply Untrue’

/ Nvidia CEO Reportedly Dismisses Anthropic Exec's AI Doomsday Warning As ‘Outlandish’ And ‘Deeply Untrue’
Nvidia CEO Reportedly Dismisses Anthropic Exec's AI Doomsday Warning As ‘Outlandish’ And ‘Deeply Untrue’
Huang defended the industry’s safety efforts at a Goldman Sachs conference, while dismissing Coxon’s warnings about runaway AI risks.
The Nvidia CEO sees cybersecurity emerging as a major AI opportunity, with CRWD, CSCO and PLTR positioned to benefit.
Huang remains confident in Nvidia’s growth and reiterated the company’s 70% revenue growth target.
Nvidia Corp. CEO Jensen Huang has reportedly pushed back against former Anthropic researcher Jacob Coxon’s warnings about the dangers of rapidly advancing AI, calling the researcher’s comments “deeply untrue” and criticizing them as wrong, arrogant and dismissive of the safety work being done across the industry.
Huang made the remarks at Goldman Sachs’ Communacopia + Technology Conference on Thursday, according to Brad Gerstner, the founder of Altimeter, who attended the event.
Coxon resigned from Anthropic earlier this week and publicly accused leading AI companies of racing toward self-improving superintelligence without adequate safeguards.
Coxon, who spent about three years doing AI pretraining research at OpenAI and Anthropic, said neither company was “acting responsibly” and that they were “racing straight to self-improving superintelligence and gambling with our lives.” He warned that increasingly capable systems could eventually “hack anything, revolutionize any field overnight, and acquire real power and resources.”
The researcher also said AI developers “earnestly believe that it could kill us all by the end of the decade,” arguing that the risk was not merely theoretical.
Coxon’s comments have also received support from within Anthropic. Alignment Science lead Evan Hubinger said he believed there was more than a 10% chance AI could cause human extinction within the next decade and that Anthropic did not yet have a solution for aligning superintelligent systems.
Huang doubled down on his enormous AI infrastructure spending forecast, arguing that demand is being driven by a fundamental shift from retrieving information to generating it. He defended his vision of $3 trillion to $4 trillion of AI infrastructure spending by 2030, comparing the transformation with previous infrastructure revolutions such as electricity and the internet.
“The last 60 years, everything was prerecorded,” Huang said. But as users increasingly want to “know anything” rather than simply find information, he argued, computing demand will explode because answers must be generated in real time.
Huang also reiterated Nvidia’s revenue outlook for next year, saying “I think we could grow 70% year over year. We’re confident about that.”
Huang Highlights Nvidia’s Autonomous Car Tech
Huang said he sees autonomous driving as the breakout application for physical AI, predicting that self-driving vehicles will shift the industry away from brute-force data collection toward real-time onboard reasoning.
Pointing to Nvidia’s recent developments in this space, Huang highlighted the company's autonomous driving architecture, Alpamayo, as a key driver enabling vehicles to analyze and navigate unfamiliar environments in real time.
"The first killer app for physical AI is just self-driving cars... And (now) what you're really looking for is a thinking car, a car that can reason. And we made some groundbreaking work in this area. It's called Alpamayo. It's the world's first reasoning and thinking car."
On Stocktwits, retail sentiment for NVDA dipped over the past week and was ‘bearish’ on Thursday, with some traders expressing concern about the stock’s recent weakness even after Huang’s appearance at the Goldman Sachs event.
“$NVDA when Jensen can’t pump while talking at (a) financial conference you know we’re cooked,” said a trader. Another wrote : “$NVDA pumps getting weaker guess Jensen should make a folding phone.”
NVDA stock dipped for three consecutive sessions through Thursday, losing about 5.5% cumulatively. Shares were flat in the overnight session late Thursday.

### Article 67 · 2026-09-10 · businessinsider.com
Nvidia CEO Jensen Huang says cybersecurity is AI's next blockbuster app

By Geoff Weiss
If coding was one of AI's first big blockbuster apps, Nvidia CEO Jensen Huang predicts cybersecurity will be the next.
Speaking at a Goldman Sachs conference on Thursday, Huang said that companies will increasingly use AI to find software vulnerabilities and defend against cyberattacks.
Huang's prediction comes as AI safety has become a hot debate in Silicon Valley. Researchers at companies like Anthropic have warned that increasingly powerful AI could pose existential threats if left unchecked — including by enabling more sophisticated cyberattacks.
Huang wasn't asked about the debate or weighing in on it. Instead, he said that increasingly capable AI will make cybersecurity one of the biggest business opportunities for the technology industry.
Huang said that cybersecurity is a natural extension of coding.
"A derivative of coding is, of course, bug finding," he said. "And a derivative of that, which is a very large market, is called cybersecurity."
Unlike coding assistants that respond to prompts, Huang said AI-powered cybersecurity systems run continuously — meaning companies will pay to keep them going around the clock.
The comments come as Nvidia has been pushing deeper into cybersecurity. The company has recently announced partnerships with CrowdStrike, Cisco, and Palantir to build AI-powered cybersecurity tools.
Other AI giants are also betting on cybersecurity. OpenAI chief financial officer Sarah Friar said Tuesday at the conference that the company sees cybersecurity as a major "commercial opportunity."

### Article 68 · 2026-09-10 · gurufocus.com
Nvidia Drops Over 2% as Australia Targets a 125% AI-Capacity Jump

Nvidia ( NASDAQ:NVDA ), the artificial-intelligence chip powerhouse, targeted up to two gigawatts of Australian AI infrastructure by 2027a staggering expansion equal to 125% of the country's current data-center capacity. Yet Nvidia shares dropped approximately 2.5% to $218.14 Thursday morning as investors looked beyond the enormous headline.
Firmus, CDC, NEXTDC and AirTrunk would construct the facilities around Nvidia's DSX platform, potentially embedding its technology deep inside Australia's emerging AI economy. The opportunity lands as Nvidia's latest quarterly results delivered $96.2 billion in revenue, with data centers contributing $89 billion, or roughly 92.5% of the total. Nvidia is no longer simply selling chips. It is helping countries design entire AI ecosystems around its architecture.
The GuruFocus image reinforces that quality story: Nvidia carries an exceptional GF Score of 96 out of 100, powered by outstanding growth, profitability, momentum and financial strength, although its GF Value rating remains the clear weak spot. Still, two gigawatts represents a target, not booked Nvidia revenue. No GPU volumes, partner purchase commitments or detailed deployment schedules were disclosed. The ambition is huge, but Australia must still deliver the electricity, approvals and paying workloads needed to turn that capacity into Nvidia sales.

### Article 69 · 2026-09-10 · gurufocus.com
Nvidia and Palantir Land Historic AI Partnership

Palantir Technologies ( NASDAQ:PLTR ) and Nvidia ( NASDAQ:NVDA ) are applying a new artificial-intelligence system to supply-chain operations, with Nvidia serving as the first deployment site.
The initiative combines Nvidia's Nemotron open models with Palantir's Foundry and Artificial Intelligence Platform. The system uses Palantir's Ontology to connect AI models with operational data and processes, creating a framework for managing supply-chain information.
Nvidia plans to use the technology across its own supply chain to organize operational knowledge and shorten the process involved in moving from semiconductor production to deployed AI workloads.
The companies said the framework is also intended for other organizations seeking to apply AI within their supply networks. Palantir's Sovereign AI Operating System Reference Architecture can run through cloud services or directly on a company's own infrastructure.
The collaboration targets supply chains that require greater control over data and AI systems. The initial Nvidia deployment could also provide a practical setting for the technology before broader use by other organizations.

### Article 70 · 2026-09-10 · rdworldonline.com
Verily secures new investment from Nvidia

By Julia Rock-Torcivia | September 10, 2026
Verily Health, a company focusing on AI for precision health that emerged from Google X and eventually became Google Life Sciences in 2015, has received funding from its partner Nvidia.
The company’s flagship product, the Verily Pre Platform, is a precision health platform that turns clinical, genomic and device data into AI-ready datasets. Verily’s current investors include Alphabet, Series X Capital and UCHealth.
In a statement, Verily CEO Stephen Gillett said the funding would help the company bring “together the information and intelligence needed to power better decisions and unlock the full potential of AI across the healthcare ecosystem,” Stephen Gillett, Chairman and CEO of Verily, said in a press release.
The investment will help support scaling of the Pre Platform, the company said.
Verily and Nvidia announced a collaboration in October 2025, allowing researchers using the Verily Pre Platform to use Nvidia AI libraries and frameworks, including NeMo, Parabricks and RAPIDS, Nvidia’s software tools for AI-accelerated science, and Nvidia B200 GPUs, the hardware beneath them. The companies also collaborated to create Forecast 1.0, a foundation model that integrates genomics and EHR data to improve the accuracy of predicting long-term health risks.
NVIDIA and Alphabet are among R&D World’s 100 most innovative companies of 2026 . The list examines what each company built, who is using it and the results it has reported. R&D World will publish the full comparison in the 2026 Global R&D Funding Forecast.
Verily has announced and killed off a number of projects since its creation and moved its headquarters from San Francisco to the Dallas-Fort Worth area in 2024. In 2014, Verily announced glucose-sensing smart contact lenses, only to put the project on hold in 2018 , saying that tear glucose did not correlate reliably enough with blood glucose. In 2023, it discontinued Verily Value Suite as well as some early-stage products, including work in remote patient monitoring for heart failure. In 2025, Verily killed off its entire medical devices program .
Many of the discontinued projects were hardware or early-stage R&D with long regulatory paths and no near-term revenue in sight. Value Suite and Granular were software, but Verily was attempting to compete against well-established businesses, including Epic and Oracle Health.
There are some signals that the Verily Pre Platform could be different. Other institutions are already using the infrastructure, for one. Vanderbilt , UCHealth, CU Anschutz and RefinedScience are using the workflows.
