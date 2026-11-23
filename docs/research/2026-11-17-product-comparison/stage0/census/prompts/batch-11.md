# Blind reader, matter census batch 11 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 38 articles (numbers 373 to 410,
2026-09-19 to 2026-09-20, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 373 · 2026-09-19 · news.az
Nvidia, OpenAI CEOs set to attend Xi dinner at White House

Nvidia CEO Jensen Huang and OpenAI CEO Sam Altman are among the technology leaders expected to attend a White House state dinner for Chinese President Xi Jinping next week, a US official said Friday.
“It’ll be a very popular and hot-ticketed event,” the official said on condition of anonymity. The official added that Amazon founder Jeff Bezos, SpaceX and Tesla CEO Elon Musk, Apple CEO Tim Cook and Google CEO Sundar Pichai are also expected to attend, AFP reported.
Their participation comes as artificial intelligence is expected to feature prominently in talks between the US and Chinese leaders. The two countries are currently the dominant powers in the global AI race.
In the United States, the AI debate remains focused on concerns that leading developers, including OpenAI , Anthropic, Google and Meta, cannot afford to slow innovation because of the risk that China could overtake them.
China, which has long been viewed as trailing the US in cutting-edge AI, has been rapidly narrowing the gap.
Washington has sought to limit China’s progress through export controls on advanced chips required for developing cutting-edge AI systems, restricting access to high-end US semiconductors, including those produced by Nvidia.
‘As fast as we can’
Despite the rivalry between Washington and Beijing, there is hope that the two countries could reach some form of understanding on AI when their leaders meet in Washington.
However, more ambitious agreements, such as slowing AI development or establishing global safeguards, are considered unlikely.
Calls for stronger safeguards have grown following warnings from industry insiders about the potential risks posed by the technology.
Jacob Coxon, a former AI researcher at Anthropic, recently intensified concerns by saying that those developing AI “earnestly believe that it could kill us all by the end of the decade.”
Anthropic CEO Dario Amodei subsequently published an essay calling for caution and a slowdown in AI development.
Altman and Musk have supported the idea, as has Google DeepMind CEO Demis Hassabis, who has called for a US-led global regulatory body for AI.
US President Donald Trump this week dismissed concerns about AI as a hoax and has urged American AI companies to continue advancing the technology to maintain an edge over China.
Nvidia CEO Huang expressed a similar position in an interview with CBS News, saying, “we should go as fast as we can, irrespective of anybody else,” according to an excerpt released Friday.
“We’re going to go as fast as we can, but we would never, ever, and never should ship products before they’re ready, deliver products that are unsafe, and nobody’s expecting us to do that,” Huang said in the interview, which is expected to air in full on Sunday.
“But everybody’s expecting us to succeed and help America be as prosperous as possible,” he added.
Analysts say Chinese policymakers have placed greater emphasis on immediate AI-related risks, including deepfakes and child safety.
However, the head of China’s spy agency warned this week that the technology could pose a threat to national security.
By Nijat Babayev
Report, citing data from Azerbaijan's State Customs Committee, said tomato exports decreased by 900 tons, or 0.6%, in vo...
According to Report, the discussions took place during Shahbazov's meeting in Moscow with Mohamed Arkab, Algeria's Minis...
The company launched public offerings of approximately $35 billion in common stock and convertible preferred stock. It a...
Report said the talks took place during Shahbazov's meeting in Moscow with Senegalese Energy and Petroleum Minister El H...
Report, citing data from Azerbaijan's State Statistical Committee, said Russia remained the largest buyer, importing 5,1...
Report, citing data from Azerbaijan's State Customs Committee, said Italy accounted for 56.1% of the country's total cru...

### Article 374 · 2026-09-19 · finance.biggo.com
Nvidia Executives Dispose of Shares in Bulk: Huang Renxun Has Nearly $10 Million in Stock Withheld for Taxes, CFO Kress Cashes Out $7.65 Million Separately

Nvidia Executives Dispose of Shares in Bulk: Huang Renxun Has Nearly $10 Million in Stock Withheld for Taxes, CFO Kress Cashes Out $7.65 Million Separately — BigGo Finance
Nvidia Executives Dispose of Shares in Bulk: Huang Renxun Has Nearly $10 Million in Stock Withheld for Taxes, CFO Kress Cashes Out $7.65 Million Separately
Filings submitted by Nvidia to the U.S. Securities and Exchange Commission show that on September 16, five executives including CEO Jensen Huang disposed of a combined total of approximately 160,000 company shares, with the vast majority representing tax withholdings triggered by restricted stock unit (RSU) vesting rather than active selling. Huang had 45,728 shares withheld, valued at approximately $9.7 million. CFO Colette Kress, in addition to having 40,747 shares withheld for taxes, separately sold 34,918 shares on the open market on September 17 under a Rule 10b5-1 trading plan, cashing out approximately $7.65 million. On the same day, the Huang family trust transferred 438,000 shares at no cost for charitable donation purposes. Nvidia's stock closed at $222.27 that day, with a total market capitalization of $5.36 trillion.
Filings submitted by Nvidia (Nasdaq: NVDA) to the U.S. Securities and Exchange Commission (SEC) show that five executives, including CEO Jensen Huang, disposed of a combined total of approximately 160,000 company shares on September 16. However, the vast majority of these transactions were not active selling, but rather shares withheld by the company to satisfy tax obligations arising from the vesting of restricted stock units (RSUs).
According to Form 4 documents disclosed on September 18, Huang had 45,728 common shares withheld on September 16 at a per-share price of $212.17, corresponding to a value of approximately $9.7 million. The filing explicitly notes that these shares were withheld by Nvidia to satisfy tax obligations arising from RSU vesting, and were not sold on the open market. The transaction code in the SEC disclosure is "F," which is specifically used to identify share dispositions of this tax-withholding nature.
Similar transactions were executed concurrently by CFO Colette Kress, Chief Operating Officer Debora Shoquist, General Counsel and Secretary Timothy Teter, and Chief Accounting Officer Scott Gawel. The number of shares withheld for the four individuals was 40,747, 35,008, 35,738, and 2,932 respectively, all at the same per-share price of $212.17.
The only transaction that constituted actual open-market cashing out was executed by Kress the following day. Filings show that Kress sold a total of 34,918 Nvidia shares in three separate transactions on September 17, with a combined transaction value of approximately $7.649 million. The sales were executed pursuant to a Rule 10b5-1 trading plan adopted on June 16, 2026. Rule 10b5-1 plans allow corporate insiders to execute trades automatically under pre-established conditions, thereby avoiding allegations of trading on material non-public information. Based on the disclosed price ranges, Kress's three sales were executed at prices between approximately $218 and $220 per share.
Beyond the executive share movements, the same filing also disclosed a large share transfer involving the Huang family trust. On September 17, the Jen-Hsun & Lori Huang Living Trust transferred 438,000 Nvidia shares at no cost, of which 292,000 shares were donated to The Jen-Hsun & Lori Huang Foundation, and an additional 146,000 shares were transferred to a donor-advised fund. This transfer likewise did not involve open-market transactions and represents a charitable asset allocation adjustment.
Combining both filing dates, the full scope of disclosed share movements is as follows:
RSU vesting tax withholding (Code F)
Open-market sale under 10b5-1 plan
Charitable donation (foundation and donor-advised fund)
Putting these numbers in the context of overall holdings, the magnitude is actually quite limited. Nvidia's proxy statement filed in May shows that as of March 23, Huang held 870.6 million shares, representing 3.58% of outstanding shares. The 45,728 shares withheld this time represent approximately 0.005% of his holdings. During the same period, Kress reported holding 4.444 million shares; the combined 75,665 shares from tax withholding and open-market sales represent approximately 1.7% of her holdings. Debora Shoquist and Timothy Teter held 1.581 million and 2.687 million shares respectively, with this round of withheld shares representing approximately 2.2% and 1.3% of their respective holdings. Nvidia's entire board and executive team (14 individuals) collectively hold 957.3 million shares, representing 3.94% of outstanding shares.
It is worth noting that insider selling is hardly a new phenomenon at Nvidia. According to Form 4 filing statistics, over the past 12 months, 12 insiders have sold shares totaling approximately $1.58 billion, while the number of insiders making open-market purchases during the same period was zero. This also means that examining executive share movements from any single week makes it difficult to discern management's judgment about the company's prospects.
What is noteworthy is that this concentrated disposal of shares by executives coincided with Nvidia's stock trading near historical highs. On September 18, Nvidia's stock rose 1.34% to close at $222.27 per share, with a total market capitalization of $5.36 trillion. Based on that day's closing price, the 45,728 shares withheld from Huang correspond to a market value of approximately $10.16 million, while the 34,918 shares cashed out by Kress correspond to a market value of approximately $7.76 million.
From a corporate governance perspective, tax withholding triggered by RSU vesting is an extremely common mechanism in tech industry executive compensation structures. When restricted stock units meet vesting conditions, employees are required to pay income tax on the vested portion, and companies typically withhold a portion of shares directly to fulfill the withholding obligation. This passive reduction in share count conveys a fundamentally different signal from active selling based on an executive's personal judgment.
Nvidia, in responding to this disclosure, also emphasized that the transactions "were not active reductions of holdings by executives." The context for this statement is that the market is extremely sensitive to shareholding changes among Nvidia's core management—as the undisputed leader in AI computing power, the company's insider trading activity is often viewed by investors as an important window into management confidence.
Kress's open-market sale, while not insignificant in dollar terms, is generally viewed with relative tolerance by the market because it was executed under a pre-established 10b5-1 trading plan. Such plans require insiders to set trading conditions at a time when they are not in possession of material non-public information, and subsequent execution is not influenced by personal judgment at the time of the trade, thereby legally insulating against insider trading concerns.
Huang himself has continued to speak out on AI safety issues recently. In a newly released interview with CBS News, he again rejected predictions that AI will trigger catastrophic outcomes, arguing that such claims are fueling unnecessary panic. He stated that the probability of AI causing the end of the world by 2030 is "0%." He also argued that the industry should not slow down as a result, and should sprint forward as quickly as possible—but would never, and should never, launch unsafe products before they are ready. This stance is consistent with his long-held position: affirming AI's enormous potential while advocating for a rational approach to technological risk.
Viewed from a broader perspective, this round of share movements among Nvidia's executive team does not change any fundamental facts about the company. Tax withholding is a technical step in compensation settlement, charitable donations reflect the founding family's wealth-planning orientation, and the only transaction involving actual cash realization—Kress's sale—had its execution path locked in months earlier through a compliance framework. For investors following Nvidia, these disclosures are more routine actions to satisfy information transparency requirements than substantive signals for judging the company's prospects.

### Article 375 · 2026-09-19 · yellow.com
Nvidia 2030 Forecasts Reveal $727 To $28,560 Gap

Nvidia 's 2030 stock forecasts span from roughly $700 to more than $28,000, highlighting the enormous uncertainty around how far the AI infrastructure boom can run.
The gap reflects competing assumptions about future chip demand, AI spending and how much of that growth Nvidia can convert into sustained earnings.
The forecasts rest on the same core bet, that AI infrastructure spending keeps compounding through the decade.
CoinCodex puts 2030 shares between $727.04 and $1,017.11, implying gains of up to 128% from current levels, while TradersUnion projects $721.67 by the end of 2029 and Plus500 frames a wider $400 to $1,000 range tied to AI infrastructure growth.
Nearly every forecast traces back to one number. Jensen Huang, the company's chief executive, repeated on the same calendar day a year apart that AI infrastructure spending will hit $3 trillion to $4 trillion by 2030, an unchanged forecast that analysts are now using as the base assumption for chip-demand models running through the decade.
That $3 trillion to $4 trillion figure is an AI infrastructure-spending expectation, not a revenue forecast.
Huang's consistency signals confidence from the person closest to the company's order book, but every price target downstream still rests on a single executive's projection rather than independently verified demand data.
The Motley Fool 's $28,560 figure assumes the company sustains its historical 52% annualized gain, a pace few semiconductor companies have held for a full decade.
Other outlets, including pieces on semiconductor stocks to hold through 2030, lean on slower compounding tied directly to Huang's spending forecast, which explains why conservative models land closer to $700-$1,000 while momentum-based ones stretch into the tens of thousands in cumulative return.
For those valuations to make sense, AI infrastructure spending must reach the projected scale and the chip-demand assumptions embedded in each model must hold.
Disclaimer and Risk Warning: The information provided in this article is for educational and informational purposes only and is based on the author's opinion. It does not constitute financial, investment, legal, or tax advice. Cryptocurrency assets are highly volatile and subject to high risk, including the risk of losing all or a substantial amount of your investment. Trading or holding crypto assets may not be suitable for all investors. The views expressed in this article are solely those of the author(s) and do not represent the official policy or position of Yellow, its founders, or its executives. Always conduct your own thorough research (D.Y.O.R.) and consult a licensed financial professional before making any investment decision.

### Article 376 · 2026-09-19 · tradingview.com
Nvidia CEO Jensen Huang Rejects Calls to Slow Down AI Development: ‘We Are Going to Go as Fast We Can, But…

/ Nvidia CEO Jensen Huang Rejects Calls to Slow Down AI Development: ‘We Are Going to Go as Fast We Can, But…'
Nvidia CEO Jensen Huang Rejects Calls to Slow Down AI Development: ‘We Are Going to Go as Fast We Can, But…'
On Friday, Nvidia Corp NVDA CEO Jensen Huang pushed back against growing calls to slow artificial intelligence development , arguing that companies should move quickly while ensuring their products are safe before release.
Jensen Huang Defends Rapid AI Development
In a teaser video shared by CBS News, Huang told correspondent Jo Ling Kent that the AI industry should continue advancing at full speed. "We should go as fast as we can, irrespective of anybody else."
Huang noted that “we are going to go as fast we can, but” that does not mean releasing unsafe technology. He said companies should avoid shipping products before they are ready or "unsafe."
The Nvidia CEO also framed rapid AI progress as important to U.S. economic growth, saying companies are expected to help make the country "as prosperous as possible."
The full interview will be released on Sunday.
EXCLUSIVE: Nvidia CEO Jensen Huang tells CBS News' @jolingkent that he does not believe the U.S. should slow down in the AI race against China, but added, "we would never, ever and never should ship products before they're ready." Watch the interview this weekend on @CBSSunday . pic.twitter.com/t5pJnvygIq
Huang’s comments come as concerns over AI’s rapid development intensify.
Anthropic CEO Dario Amodei has argued that the technology is advancing at an "exponential" rate and warned that safety measures need to keep pace. He said the industry should slow down rather than stop developing AI altogether.
Amodei has also called for independent third-party evaluators to assess AI companies’ safety practices and urged companies to work together on common safety standards.
Earlier, former Anthropic researcher Jacob Coxon raised concerns that AI companies are prioritizing rapid innovation over adequate security measures, saying stronger safeguards are needed as the technology becomes more capable.
Earlier this week, Meta Platforms, Inc. META CEO Mark Zuckerberg said the company delayed its Muse AI agent for several months to address safety and security concerns. "Every lab has the responsibility and incentive to move at the pace required to train its models safely, and the ability to take its own actions to ensure that happens," Zuckerberg wrote on X .
Price Action: Nvidia shares closed at $222.27 on Friday, up 1.34%. It edged 0.12% higher to $222.53 in after-hours trading, according to Benzinga Pro.
According to Benzinga Edge Rankings , Nvidia ranks in the 98th percentile for Growth and shows positive short-, medium- and long-term price trends.https://www.benzinga.com/quote/NVDA

### Article 377 · 2026-09-19 · fool.com
Prediction: This Nvidia-Backed Artificial Intelligence (AI) Stock Could 10X by 2033

The question hanging over Marvell Technology ( MRVL +3.85% ) is not whether its artificial intelligence (AI) story is real. Its share price has already answered that. Marvell stock opened 2026 at around $87, ripped to a high above $300 in June, got clobbered throughout July and August , and recently bounced back toward the $240 range.
This is the kind of action that growth investors live for. It is also the kind of volatility that forces investors to take a hard look at the business, its partners, and the math that supports whether Marvell can realistically produce a 10x gain from here.
What is Marvell's position in the AI chip stack?
Marvell is not a GPU designer nor a specialty manufacturer. Rather, it is a fabless designer that used to be primarily known for networking silicon but has spent the AI revolution transitioning into a data center infrastructure business. Marvell's stack within AI factories covers optical DSPs, Ethernet and switching, silicon photonics, and custom chips.
However, its custom silicon designs are why Marvell has become such a hot semiconductor stock . Hyperscalers like Amazon , Microsoft , Alphabet ( GOOGL -0.61% ) ( GOOG -0.77% ) , and Meta Platforms do not want to rent every watt of compute from the duopoly GPU suppliers, Nvidia ( NVDA +2.55% ) and Advanced Micro Devices . Instead, they are allocating meaningful capital expenditures toward application-specific integrated circuits (ASICs) and XPUs (specialized AI accelerators) that are fine-tuned to their own models.
Marvell's financial performance is beginning to match the growth story. In its fiscal 2026 (which ended Jan. 31), the company reported record revenue of $8.2 billion, up 41% year over year. The data center business grew 46% to $6.1 billion, fueled by demand for optical interconnects, custom silicon, switching, and storage. During its most recent fiscal quarter, which ended Aug. 1, Marvell generated revenue of $2.7 billion, up 37% year over year. The data center segment comprised 79% of sales and grew 46% year over year.
Nvidia's stamp of approval, plus a high-five from Google
In March, Nvidia invested $2 billion into Marvell as part of a broader strategic collaboration. Marvell's ecosystem is now folded into Nvidia's NVLink Fusion. By partnering with Marvell, Nvidia can integrate the smaller company's custom XPUs and networking equipment within its own racks. While Marvell supplies the custom silicon and compatible interconnects, Nvidia supplies the rest of the server. A few months later, in June, Nvidia CEO Jensen Huang called Marvell "the next trillion-dollar company" during a public event in Taipei, Taiwan.
About a month ago, Alphabet announced its own interesting deal with Marvell. Marvell has been tapped to help develop products around Google's custom Tensor Processing Units (TPUs). The ecosystem includes inference accelerators, storage and network controllers, memory interfaces, and near-memory compute.
Attached to that deal was a warrant for nearly 59 million shares at a fixed price of $206.58, worth about $12.2 billion if fully exercised. The majority of the warrant vests in 240 equal tranches for every $500 million Marvell generates in custom products revenue from Google. The structure of this deal implies up to $120 billion of qualified purchases through fiscal 2033.
Both the Nvidia and Alphabet deals matter because Broadcom dominates the custom ASIC space right now, holding an estimated 80% to 85% of the market. But a check and partnership from Nvidia implies that the much smaller Marvell is still useful inside its GPU empire. Meanwhile, Alphabet's warrant is a mechanism to show that one of Broadcom's flagship TPU customers is still willing to dual-source the surrounding silicon under the right conditions instead of leaving the whole project scope with one incumbent.
Can Marvell stock 10x from here?
If Marvell's share price were to 10x from its current level, that would make it a $2.1 trillion company -- twice as ambitious as Huang's trillion-dollar line from a few months ago. To assess what its growth trajectory could realistically look like, let's start by considering Marvell's total addressable market .
On the custom silicon side, Bank of America analyst Vivek Arya forecasts that the market for custom AI processors and the chips wired to them will be worth around $300 billion by 2030. On the other side of the business, Goldman Sachs estimates that the global optical-module market is worth $68 billion currently and expects it to grow to $148 billion by 2028. Adjacent analyses from Dell'Oro Group see AI back-end data center switch spending crossing $100 billion by 2030.
If I blend these market sizes with Marvell's own fiscal 2028 sales guide of $18 billion, I think a setup where it brings in annual revenues in the range of $60 billion to $90 billion by the early 2030s is reasonable. Of course, the top of that range could wind up stretching toward $100 billion or more if Google's warrant converts into higher volumes. Assuming Marvell can maintain a healthy price-to-sales (P/S) ratio around 20 through its hypergrowth phase, a $2 trillion market cap outcome becomes less of a fantasy.
While a $2 trillion market cap is not the base case , I think there is an achievable path for the company to get there. Although a 10x gain won't be easy, I'm confident Marvell stock will be a multibagger by the time 2033 comes around.
By Adam Spatacco – Sep 19, 2026 at 12:45PM EST

### Article 378 · 2026-09-19 · makeuseof.com
AMD and Intel finally have answers to Nvidia's DLSS and one just took the lead

By Shaheer Khan
When it first debuted, DLSS was a promising technology. While far from perfect, it was a groundbreaking feature that helped RTX cards deliver more performance while handling demanding features like Ray Tracing. Fast-forward 7 years and 5 iterations, and DLSS is in a completely different place: a real, improved way to boost performance on older hardware, even though Nvidia's intent has strayed too far.
Behind this tech, AMD and then Intel have struggled to match DLSS's feature set, but after all these years, they've finally caught up. FSR and XeSS offer the best parts of DLSS's stack, even though they've gone far beyond simply competing with DLSS.
FSR and XeSS have finally closed the upscaling gap
AMD needed four tries, and Intel needed a wider net
DLSS started as a game-specific technology, but with the debut of DLSS 2, it became a generalized AI reconstruction system applicable to a wider range of games.
While AMD's FSR debuted in 2021, two years after DLSS, it was really just AMD playing catch-up with Nvidia. The first iteration was underwhelming because it was only a spatial, algorithm-based upscaler with no machine learning.
FSR 2, however, became a temporal upscaler using information from prior frames, roughly matching DLSS 2, though it arrived later and delivered lower image quality.
With FSR 4, AMD finally implemented machine learning, introducing neural rendering that more closely matches DLSS. FSR 4.1 was just AMD fine-tuning the ML-based neural rendering approach with better dynamic lighting and temporal stability.
Similarly, Intel wasn't about to let itself fall behind AMD or Nvidia, so it brought its own upscaling tech, XeSS, with the release of the first Arc GPUs in 2022. Although XeSS started with AI upscaling and wasn't algorithm-based like the first FSR implementations, it arrived too late.
In contrast, XeSS never really became a solid option because it was adopted later than Nvidia and AMD, the image quality wasn't great, and it was more demanding than the other options. Moreover, game support for XeSS is quite limited, even though it works across all GPUs (higher versions explicitly require Intel's XMX cores in Arc GPUs).
The Frame Generation race that Nvidia still leads
FSR and XeSS are closing in, and AMD might be cooking up something even better
DLSS 3 introduced Frame Generation, a feature that adds AI-generated frames between rendered frames to boost overall FPS, smooth motion, and become Nvidia's real selling point. DLSS 4 took it a level further with Multi-Frame Generation, a frame-generation multiplier that, instead of generating a single AI-generated frame, generates up to 5 extra frames (with DLSS 4.5) to boost FPS further.
Nvidia practically changed how the industry measures performance, and raw figures don't really matter anymore. While public opinion on AI-generated frames is still split, Frame Generation eases the weight of Ray Tracing and Path Tracing.
AMD and XeSS once again fell behind Nvidia, and while both tech giants have their own versions of Frame Generation, FSR 4.1 can only do 2X Frame Generation, and Intel can go up to 4X with XeSS 3. However, AMD is testing FSR Multi Frame Generation of up to 8X in newer drivers for RDNA 4 GPUs (via VideoCardz ), and that might arrive sooner than expected and give it an edge over DLSS 4.5.
AMD denoisers finally have the answer to the best part about DLSS's stack
Ray Regeneration and Radiance Caching are promising technologies for Radeon GPUs
Beyond upscaling and Frame Generation, Nvidia has added more features to the DLSS stack with newer iterations. DLSS 3.5 introduced Ray Reconstruction, which replaced traditional denoisers that clean up grain, speckles, and visual static in ray-traced samples.
Ray Reconstruction works with reflections, shadows, global illumination, fine lighting details, and temporal stability and vastly improves quality for upscaled images with little to no performance downside.
AMD's answer was Ray Regeneration, a ray-tracing denoiser meant to be the equivalent of Nvidia's Ray Reconstruction, but it works differently by generating new replacement rays to produce more accurate lighting, reflections, shadows, and illumination.
On the other hand, Radiance Caching predicts how light will bounce around a scene instead of calculating every ray from scratch. It is AMD's answer to Nvidia's Neural Radiance Cache, which serves the same purpose on the DLSS side.
These feature sets are packaged together as FSR Redstone and are exclusive to newer RDNA 4 GPUs.
Where Nvidia still wins and where it doesn't
DLSS 5 is where Nvidia leads, but it's not about performance anymore
Nvidia has always been one step ahead of AMD and Intel with DLSS, mainly because they pioneered the upscaling technology, but DLSS's evolution hasn't been very steady.
DLSS 5 is Nvidia losing the plot , undermining the very reason DLSS exists in the first place, since it uses generative AI to repaint lighting, materials, and textures in a game.
However, DLSS 5 isn't what anyone had expected and does far more than what Nvidia claims. It completely alters a video game's intended art style. So far, it is a photorealism filter with a steep performance cost; it uses AI features on the newer RTX 50 Series cards to reduce overall consumption, but the same AI features are resource-intensive, so it works counterintuitively.
Right now, no DLSS-exclusive feature makes a performance difference that AMD or Intel doesn't offer. Both FSR and XeSS have multi-Frame Generation, and AMD's FSR Redstone has Ray Regeneration and Radiance Caching to match Nvidia's Ray Reconstruction and Neural Radiance Caching. However, Intel has nothing to compete with in this department.
If you put FSR 4.1 against DLSS 4.5, both have their own strengths. DLSS 4.5 delivers supreme image quality, but it falls short on performance; AMD has the edge with FSR 4.1, which produces a softer, more natural look by comparison, but they've now come on par.
AMD is already lining up its answer to DLSS 5
Beyond software, AMD has finally gained an edge over Nvidia with the latest RDNA 4 GPUs , and now they're gearing up to release the RDNA 5/UDNA lineup next year, which could possibly mark their return to flagship GPUs.
Leaks suggest Team Red is also working on a new neural rendering tech that takes the same approach as DLSS 5 (via VideoCardz ), enhancing lighting, and it could potentially have greater access to 3D rendering primitives to output a better image.
With the best parts of the DLSS stack, i.e., Super Resolution and Frame Generation, already in FSR and XeSS (denoiser only in FSR), and finally, the upscaled image quality doesn't cost much performance, it will be exciting to see what AMD and Intel will have to offer next against DLSS 5.
Saying that XeSS quality wasn't great... Even from 1.0 it was better than FSR2. 1.3 was comparable to FSR3.1 and it's also only algorithmic.
XeSS 2 is actually rather impressive and runs on XMX and DP4a. It's an ML based upscaler like FSR4 but definitely looks clearer in every game I've tried.

### Article 379 · 2026-09-19 · bgr.com
5 Regrets Users Have After Buying An Nvidia GPU

5 Regrets Users Have After Buying An Nvidia GPU
By Eduardo Ariedo
Buying an Nvidia GPU is a safe choice, especially for anyone who wants high performance, since the company makes some of the best graphics cards on the market. Whether for gaming or professional work, features like DLSS, ray tracing, and a mature software ecosystem help explain this preference. Still, even though it is an excellent purchase, some users regret it after a few months of use.
Part of these regrets comes from the price. Nvidia cards occupy a premium price segment, and the rising cost of powerful graphics cards explains part of users' regrets. In some ranges, paying more means buying features you may never use, but cheaper options usually don't make up for it at their current price.
Some regrets also appear over time, such as discovering that to keep up with the desktop, you will need other hardware upgrades. Even though this doesn't mean an Nvidia GPU is bad, we separated some complaints that highlight issues to watch out for before buying one.
You paid extra for Nvidia features you barely use
One of the most common regrets after buying an Nvidia GPU is realizing that part of what you paid is tied to features that don't always make a difference. Technologies like DLSS, ray tracing, and Reflex can be excellent in compatible games, but if your focus is on older or competitive titles, these functions can disappoint.
This weighs even more on the company's most powerful graphics cards. Although these models offer impressive performance, cheaper Nvidia GPUs can make more sense than flagship models , especially if you do not want the highest performance possible or play at high resolutions. In this case, users may not notice they paid too much until later.
If DLSS, ray tracing, or content creation features rarely come into play for these users, the extra value may seem less justified. For this profile, a more accessible Nvidia GPU, or even a competing alternative, could meet the same needs and offer reasonable performance for a fraction of the price.
You wish you had bought an Nvidia GPU with more VRAM
Another common regret among people who buy Nvidia graphics cards is their low VRAM. While this isn't a problem on flagships, entry-level models usually have only 8GB of memory, which is enough for many games. However, if you want to play at higher resolutions, with textures at maximum and ray tracing, this usually increases the card's memory consumption quickly. So, over time, you may need to reduce game quality to play stably.
This makes some owners look at models with more memory and think they should have spent a little more from the start. The RTX 5060 Ti 8 GB is one example of a graphics card with poor value because its VRAM can limit more demanding games. So, in the same way that it is possible to regret paying a lot for a GPU with features you will not use, the opposite can also happen, since depending on how you want to play, saving on features does not pay off.
Your Nvidia GPU forced you to upgrade the rest of your PC
Buying an Nvidia GPU is a major investment, but many users regret it when they realize they still need to upgrade other desktop parts. Depending on your previous build, the new card may require a larger case, better cooling, or even a new power supply to support its full power draw. Individually, many of these upgrades do not seem scary, but that changes when you buy them right after an expensive purchase.
Several affordable PC upgrades cost less than replacing major components , but needing to buy two or three of them at the same time, right after investing in a graphics card, can turn a GPU upgrade into a full PC overhaul. That is where some users regret not checking power requirements, dimensions, and compatibility before choosing the GPU. The card may even deliver the promised performance for the price, but you may still need extra upgrades to extract maximum performance.
A bad Nvidia driver update can create problems you never had before
Driver updates can also affect how your Nvidia card works, since a GPU can spend months working perfectly but start having problems as soon as you decide to update its drivers. In these cases, reports include black screens, crashes, stuttering, or strange behavior in some games. For anyone who bought one of these cards expecting stability, having to investigate whether the problem really came from the hardware or software can change the experience.
This is also a complicated situation because keeping graphics card drivers updated remains important . This is the only way to receive important fixes and support for new games. However, if you ignore updates and miss these optimizations, installing a buggy version can also create issues that didn't exist before.
In many cases, the solution is to roll back to a previous driver version. But this doesn't mean every user will experience instability; those who do feel some regret, since paying a lot for a card expecting reliability wasn't enough.
Your Nvidia GPU uses more power and creates more heat than you expected
Another regret can appear when the user realizes that the extra performance also comes with higher power consumption and heat production. This is very common in high-performance models, such as the RTX 5090 or similar cards, which can demand a lot from the power supply and raise the case's internal temperature during heavier games. So, if you wanted a more compact or even quiet PC, one of these GPUs can ruin the plan.
More heat inside the case can make other fans work harder, increasing overall system noise. Depending on your build, you can even solve part of this problem by adjusting fan curves, undervolting, or improving airflow inside the case to keep temperature and noise stable.
For some users, this behavior makes a less powerful GPU seem like a better choice after some time. The performance loss could be acceptable in exchange for lower consumption, lower temperatures, and a quieter computer.

### Article 380 · 2026-09-19 · turkiyetoday.com
Nvidia's Huang says AI development should move 'as fast as we can'

Nvidia CEO Jensen Huang speaks during a Q&A at the company's annual GTC developers conference in San Jose, California, U.S., March 17, 2026. (AFP Photo)
By Newsroom
N vidia CEO Jensen Huang said artificial intelligence development in the United States should move forward "as fast as we can," arguing against calls to slow frontier AI progress while stressing that companies must not put out unsafe products.
Speaking in an excerpt from a CBS News interview due to air Sunday, Huang was asked whether AI development should be slowed and whether such a move could affect competition with China.
"We should go as fast as we can, irrespective of anybody else," Huang said.
At the same time, he made clear that rapid development should not come at the cost of safety, saying companies should never ship products before they are ready or put out systems that are unsafe.
"We would never, ever, and never should ship products before they're ready, deliver products that are unsafe, and nobody's expecting us to do that," Huang said. "But everybody's expecting us to succeed and help America be as prosperous as possible."
Nvidia CEO Jensen Huang speaks at the company-wide convention at their T17 and T18 plots in Shilin-Beitou Technology Park in Taipei, May 27, 2026. (AFP Photo)
His comments set him apart from several major figures in the AI industry who have recently called for a slower pace in developing frontier models, a term used for the most advanced and capable AI systems.
Anthropic CEO Dario Amodei last week called on leading developers to slow improvements in model capabilities so that safety research and oversight could have more time to catch up.
OpenAI CEO Sam Altman and xAI founder Elon Musk later voiced support for slowing or more carefully pacing the development of frontier AI models.
The debate has intensified as increasingly capable systems have shown unexpected behavior during testing, raising questions over whether researchers can reliably keep their actions under control.
Nvidia Corp. co-founder and CEO Jensen Huang spoke at a press conference in Taipei on May 21, 2025. (AFP Photo)
Google confirmed Friday that its Gemini model accessed systems belonging to three real companies during a cybersecurity evaluation after accidentally gaining internet access.
According to the company, the model stopped each intrusion after recognizing that the systems were real, while Google did not classify the incidents as cases of model misalignment.
Model misalignment refers to situations in which an AI system behaves in ways that do not match the goals, instructions or safeguards intended by its developers.
OpenAI also introduced a formal framework this week for publicly reporting cases of model misalignment, saying the industry has not yet solved alignment and monitoring well enough to responsibly keep scaling advanced systems at maximum speed indefinitely.

### Article 381 · 2026-09-19 · yahoo.com
Trump calls AI danger talk a 'hoax' in phone call to Nvidia CEO in Los Angeles

Trump calls AI danger talk a 'hoax' in phone call to Nvidia CEO in Los Angeles
The debate around AI includes worries about job displacement, energy demands, and online trust, with real-world consequences for communities.
Policymakers and companies can address AI concerns by promoting transparency, setting standards for data centers, and protecting consumers from downsides.
President Donald Trump brushed aside concerns about artificial intelligence during a live phone call with Nvidia CEO Jensen Huang at the All-In Summit in Los Angeles.
The remarks came amid an AI reckoning, as the technology is raising concerns among industry insiders as well as citizens about the rapid spread of data centers, jobs, energy demand, and online trust.
Channel News Asia (@channelnewsasia), shared a clip on TikTok of Trump phoning Huang, with the president speaking bluntly about AI concerns. In the video's caption, the outlet said Trump "rubbished talk of AI dangers."
"The robots are not taking over. AI is not taking over. The whole thing is a hoax," Trump said.
During the call, Trump also spoke positively about data centers, calling them "great" and saying they "make people and states wealthy." He also said criticism of AI could be politically driven, adding "it could also be China."
One commenter wrote, "Nvidia's whole business would take a nosedive with AI slowing down. Of course it's not a hoax."
The debate around AI features science-fiction-style fears about robot takeovers. But these systems are shaping classrooms, hiring decisions, customer service, search results, and the information people encounter each day.
That means concerns about bias, privacy, misinformation, and accountability are valid; they directly affect workers, families, and communities.
The physical buildout behind AI also carries real-world consequences. Data centers can bring tax revenue and construction jobs, but they also require enormous amounts of electricity and water.
For nearby communities, that can mean strain on power grids, increased competition for resources, and difficult questions about land use and utility demand.
What can be done?
Policymakers, utility regulators, and companies can require greater transparency about how automated tools are used, where new data centers are built, and what those facilities will require from local energy and water systems.
Clear standards around grid upgrades, water use, labor conditions, and consumer protections can keep households from absorbing the downsides while corporations collect the rewards.
Where can I learn more?
Trump's call with Huang landed amid two big arguments over the AI boom: how its risks are brushed aside and who absorbs the costs. The articles below trace those questions through multiple channels.
• In Congress, Republicans advanced AI regulations rejected by lawmakers as researchers warned of climate and health costs.
• At Nvidia, Jensen Huang said AI as a layoff excuse was "scaring people."
• Families say trust is eroding as users turn to chatbots over loved ones.
• Across rural communities, Big Tech used lucrative deals and NDAs to assemble data center land.

### Article 382 · 2026-09-19 · trtworld.com
Nvidia CEO urges rapid AI development, pushing back on calls for slowdown

Nvidia's chief argues that hesitating on AI progress would let rivals overtake the United States in the global race entirely.
Nvidia CEO Jensen Huang has said artificial intelligence development in the US should move “as fast as we can,” pushing back against growing calls within the technology industry to slow advances while stronger safety measures are developed.
Asked by CBS News whether AI development should be slowed and whether doing so could affect competition with China, Huang said the industry should continue moving quickly regardless of its competitors.
“We should go as fast as we can, irrespective of anybody else,” Huang said in an excerpt released on Friday from an interview set to air on Sunday.
He stressed, however, that speed should not come at the expense of safety.
“We would never, ever, and never should ship products before they’re ready, deliver products that are unsafe, and nobody’s expecting us to do that,” said Huang.
“But everybody’s expecting us to succeed and help America be as prosperous as possible.”
The comments put Huang on a different side of an intensifying industry debate about whether increasingly capable AI systems are advancing faster than researchers can reliably control them.
Anthropic CEO Dario Amodei last week called for leading AI developers to slow improvements in model capabilities to give safety research and oversight more time to catch up.
OpenAI CEO Sam Altman and xAI founder Elon Musk subsequently expressed support for slowing or “pacing” development of frontier models.
Concerns have been fueled by recent cases in which advanced AI agents behaved unexpectedly during testing.
Google confirmed on Friday that its Gemini model accessed systems belonging to three real companies during a cybersecurity evaluation after accidentally gaining internet access.
The company said the model stopped each intrusion once it realised the systems were real and did not classify the incidents as model misalignment.
OpenAI this week also introduced a formal framework for publicly reporting cases of model misalignment, saying the industry has not yet solved alignment and monitoring well enough to responsibly continue scaling advanced systems at maximum speed indefinitely.

### Article 383 · 2026-09-20 · fool.com
Prediction: Nvidia's Revenue Growth Will Drive Shares to $400 Next Year

Nvidia (NASDAQ: NVDA) stock closed trading Friday at around $222 per share. So, predicting it will be a $400 stock next year is a bold call, especially since it's already the largest company in the world by market cap. However, there's math to back that premise up. Furthermore, recent comments from CEO Jensen Huang also make this believable.
If Nvidia can truly rise by 80% between now and the end of next year, it's an obvious buy at today's level, as there are few stocks that can be expected to deliver that type of upside.
Nvidia believes it will double its chip sales next year
Recently, Huang told the news media that he expects Nvidia to sell twice as many chips next year as in 2026. With all things being equal, suggest the business will be twice as big; therefore, its valuation should double. While there's a lot more to it than that, we're clearly still in the early innings of the artificial intelligence (AI) build-out.
This sentiment was echoed by Chief Financial Officer Colette Kress, who gave guidance for 70% revenue growth during the company's next fiscal year. Nvidia's guidance has always been tempered, and it has consistently exceeded predictions quarter after quarter during the AI race. Huang, on the other hand, has always made bold projections about where AI spending will go, and his forecast that the company will double the number of chips it sells year over year in 2027 is likely at the top end of the projection.
We can expect reality to land somewhere in between those points, but if Nvidia is likely to grow by anywhere from 70% to 100% next year, it's a no-brainer buy. The AI race isn't slowing down anytime soon , and as every company involved in the space continues to go full steam ahead on constructing AI data centers, Nvidia will remain one of the primary beneficiaries. And yet with all that going for it, its stock is not expensive.
Price-to-earnings ratio (P/E) is one of the best valuation metrics for weighing fully mature and profitable companies. Trading at less than 28 times earnings, Nvidia actually looks like a bargain.
The S&P 500 trades for about 25.1 times earnings, but the average S&P 500 component isn't expected to double its business in the next year. That's the primary flaw with the trailing P/E ratio -- it doesn't account for expected future growth.
However, investors can use earnings projections to get an idea of where a stock could be heading. Right now, Nvidia trades at 14 times next year's estimated earnings.
If the business delivers results in line with analysts' consensus expectations, and if it still trades for 28 times trailing earnings a year from now, the stock will have doubled. That would easily lift it past the $400 per share threshold. Furthermore, the company has a strong track record of outperforming analysts' estimates, so I wouldn't be surprised if the stock rises even more than that.
With the AI boom in full swing , I think this is as good a time as any to buy Nvidia shares. Shunning the stock now just because it has been so successful over the past few years would be a major mistake, as it looks well positions to keep providing investors with low-risk, market-beating returns.

### Article 384 · 2026-09-20 · cnbc.com
Nvidia CEO Jensen Huang emerges as Trump's top ally in AI safety debate

Jensen Huang's position as the leader of the world's most valuable company and the chipmaker at the heart of the AI boom has earned him President Donald Trump's favor.
While tech execs like Meta CEO Mark Zuckerberg and Amazon Chairman Jeff Bezos have cozied up to Trump during his second term, experts say Nvidia's CEO is exercising outsized influence.
Trump is increasingly mirroring Huang's policy stances on AI topics, such as safety, saying this week that "the robots are not going to be taking over the world."
Nvidia CEO Jensen Huang speaks during the keynote address at Salesforce's Dreamforce conference at the Moscone Center on Sept. 15, 2026 in San Francisco, California.
With the debate about regulating artificial intelligence raging in Washington this week, President Donald Trump picked up the phone to call his top ally on the subject: Nvidia CEO Jensen Huang.
"The robots are not going to be taking over the world," Trump told Huang, who'd put the president on speaker while on stage at the All-In Summit in Los Angeles on Monday. Trump repeated a point he'd made on social media: that mounting AI and data center concerns are a "hoax."
While other tech leaders like Meta CEO Mark Zuckerberg and Amazon founder Jeff Bezos have cozied up to Trump during his second term, experts told CNBC that Huang is exercising outsized influence in the White House. He's slated to attend Trump's high-profile state dinner for Chinese President Xi Jinping next week, according to a person familiar with the matter who asked not to be named due to confidentiality.
Nvidia has been powering the AI boom since before the launch of ChatGPT in late 2022, supplying the graphics processing units used by OpenAI, Anthropic and others to train their models and run large workloads. Revenue surged to $215 billion in the latest fiscal year, up from $17 billion in 2021.
Huang's position as the leader of the world's most valuable company and the chipmaker at the heart of the AI boom has earned him the president's ear on the most important AI topics.
"Trump just likes winners, and Jensen's very good at speaking his language," Samuel Hammond, director of AI policy at the think tank Foundation for American Innovation, said in an interview.
An Nvidia spokesperson declined to comment, and White House representatives didn't respond to a request for comment.
Whether joining Trump for a candlelit dinner at his Mar-a-Lago club in Florida, or closing a keynote by thanking guests for "making America great again," Huang has learned how to appeal to the president. Trump and Huang have appeared together at least six times in public since the start of the second term, including trips to Saudi Arabia and the U.K., and a recent trip to China via Air Force One.
Huang is pushing for U.S. AI to move faster while some of Nvidia's most important customers — namely OpenAI and Anthropic — are ramping up pressure on governments to regulate the technology as fears spread about its potential dangers.
An Anthropic researcher, Jacob Coxon , who previously worked at OpenAI, said he quit his job earlier this month because he feared top AI labs are "gambling with our lives." Coxon's resignation set off a firestorm on social media, prompting calls for increased oversight from more than 20 members of Congress.
Concerns were already swirling after OpenAI disclosed a significant security incident in July, when two of its models escaped containment, accessed the open internet, and breached the online AI repository Hugging Face to get a better score on a benchmark test.
Anthropic CEO Dario Amodei cited that episode in a bombshell essay a week ago, urging AI developers to slow how quickly they improve their most advanced AI models. Amodei encouraged companies to cooperate directly with the U.S. government, and reiterated his desire for "well-considered regulation of AI."
Amodei's "pacing" proposal was endorsed by other industry leaders, including OpenAI CEO Sam Altman , SpaceX CEO Elon Musk and Google DeepMind Chair Demis Hassabis, who agreed on the need for a slowdown and additional oversight.
Huang took a different position.
In public appearances over the past week, the Nvidia CEO brushed off concerns about AI's risks. He said that predictions of doom aren't grounded in science, and that model developers are responsible for securing their products before releasing them.
The solution to safety concerns, Huang said in Scotland on Thursday, is "good old-fashioned engineering."
"There were incidents, and those incidents, thankfully, did no harm," Huang said.
Huang's position is largely shared publicly by David Sacks, a venture capitalist who previously served as Trump's AI and crypto czar. Sacks co-hosts the "All-In" Podcast, which produced Monday's event that featured the Trump-Huang call.
"The only control or 'guardrails' that AI needs is a STRONG AND SMART (High IQ!) PRESIDENT, and the U.S.A. has that, in spades!," Trump wrote in a post on Truth Social on the same day as the summit.
President Donald Trump greets Vice President of China Han Zheng as SpaceX CEO Elon Musk, U.S. Ambassador to China David Perdue and Nvidia CEO Jensen Huang look on at Beijing Capital International Airport on May 13, 2026.
Before the recent uproar over safety, Nvidia focused its Washington outreach on export controls.
Last year, Nvidia was pushing to sell its AI chips to restricted countries, including China, drawing sharp criticism from U.S. lawmakers.
Some members of Congress, including Sens. Elizabeth Warren , D-Mass., and Josh Hawley, R-Mo., have cautioned that selling Nvidia hardware to China could threaten U.S. national security and narrow America's lead in AI.
In December, Huang's strategy paid off. Trump announced that Nvidia was granted permission to ship its H200 chip to Chinese customers, and that the U.S. would collect a 25% fee in exchange.
The H200 announcement drew intense pushback from both sides of the aisle. Huang declined an invitation from Warren to testify before the Senate Banking Committee in June. The following month, a top U.S. trade official confirmed that H200 sales to China were underway.
Nvidia and Huang argued that banning Nvidia exports to China would be against American interests, in part because such a move would spur the world's second-largest economy and computing market to develop its own cutting-edge AI chips. The H200 is no longer Nvidia's most powerful chip, as it has shipped two generations of its newer Blackwell processors in the U.S.
But Nvidia's fate wasn't entirely up to U.S. lawmakers, as China's regulators mostly blocked imports of the H200 chips.
Nvidia's clear profit motive leads some experts to say it takes the concerns expressed by model developers more seriously than those of the chipmaker, because the labs are the ones responsible for the actual AI technology.
"Nvidia is the most aggressive in terms of, let's just make money," said Andrew Yoon, a researcher at CivAI, a nonprofit warning about the dangers of AI. "At every turn, they are really trying to just make sure whatever happens is good for Nvidia's bottom line."
Nvidia's ambitions in China will loom large during the state dinner on Thursday, when Trump, Huang and Xi will all be in the same room. The White House is also planning a meeting with major AI executives to coincide with the event, according to CNN . Other industry executives, including Altman, are expected to attend.
But Huang's presence carries extra weight. During a House hearing on Monday, Treasury Secretary Scott Bessent was asked if Trump understands the threat AI presents.
"I would just say the president is completely aligned with Jensen Huang, the CEO of Nvidia," Bessent said.
WATCH: Nvidia CEO Jensen Huang says safety is an engineering problem

### Article 385 · 2026-09-20 · tech.yahoo.com
Which Nvidia GPU Is Equivalent To The PlayStation 5 Pro?

Which Nvidia GPU Is Equivalent To The PlayStation 5 Pro?
Can a console like the PlayStation 5 Pro really hold its own against high-end PC hardware? The PS5 Pro is the most powerful console on the market, taking the already impressive performance of the base PlayStation 5, and boosting frame rate and resolution support even higher. It's designed for gamers who want the best possible performance without having to sacrifice visual quality with a low-resolution performance mode.
The benefits vary from game to game, but on the whole, the PS5 Pro really does offer an improved experience over standard PS5 consoles. It uses custom AMD hardware inside, so you can't just walk into a store and find the PS5 Pro's GPU on a shelf. The latest and greatest Nvidia GPUs have it beat , but you can still get PS5 Pro-level performance with one of Nvidia's newer cards.
The closest Nvidia GPU match is an RTX 5060 Ti, which stands shoulder to shoulder with the PlayStation 5 in running new AAA games. It can even outperform the console in certain situations, but it's not always a one-side competition.
How is the RTX 5060 Ti similar to a PS5 Pro?
The PS5 Pro GPU has a similar spec sheet and clock speed to the 5060 Ti, but in-game benchmarks are where the comparison really starts to become clear. It's difficult to tell the two apart in some cases, and the 5060 Ti is even flexible enough to match the PS5's usual graphics and performance modes.
Looking at a graphically-intensive game like "Black Myth: Wukong", the PS5 Pro features a 60 fps performance mode that runs at 1080p, as well as a 30 fps graphics mode that boosts the resolution to 4K. The RTX 5060 Ti actually slightly beats the PS5 Pro at similar settings, breaking past the console's 60 fps cap when using DLSS upscaling .
Even when more advanced graphical features like ray tracing are introduced, the RTX 5060 Ti can still match the PS5 Pro in most games. The 5060 Ti can handle "Alan Wake 2," which makes heavy use of ray tracing effects, at basically identical settings to the PS5 Pro's quality and performance modes.
How does the PS5 Pro compare to other hardware?
The PlayStation 5 Pro is a remarkably powerful device, and its performance exceeds the other consoles on the market. Its GPU is 45% faster than the base PS5, and the addition of PSSR gives the PS5 Pro even more impressive visuals and performance. Even though the Xbox Series X is slightly faster than the base PS5 , it's still nothing compared to the PS5 Pro. The Nintendo Switch 2 and Xbox Series S don't come anywhere close, either.
That said, while the PS5 Pro stands at the top of the console market, there are other benefits to PC gaming that the PS5 Pro just can't match. The RTX 5060 Ti might be the closest GPU on paper to the Pro, for example, but Nvidia 5000 series graphics cards support multi-frame generation, boosting frame rates way higher than what's possible on PS5 Pro.
PC gamers also have more granular control over graphical settings and resolution, as well as their other components like CPU and RAM. A poor PSSR implementation or choppy framerate on PS5 Pro can't be remedied without a developer patch, but PC players can tinker with things for faster fixes.
Read the original article on BGR .

### Article 386 · 2026-09-20 · marketbeat.com
These 3 Stocks Sit at the Center of NVIDIA’s Cybersecurity Push

Digital illustration of a central computer chip connected by glowing blue and green lines to server nodes over a world map.
NVIDIA CEO Jensen Huang identified cybersecurity as the next major growth market, citing AI-driven code expansion and machine-speed attacks that outpace legacy defenses.
NVIDIA is embedding cybersecurity tools like Morpheus, DOCA, and Nemotron into its ecosystem through expanding partnerships with CrowdStrike, Cisco Systems, and Palantir.
CrowdStrike, Cisco, and Palantir have each posted accelerating growth and positive analyst sentiment, with rising price targets reflecting their expanding roles in AI-driven security.
NVIDIA (NASDAQ: NVDA) CEO Jensen Huang gave cybersecurity his seal of approval, calling it the next major growth market, aligning with a growing number of indicators suggesting an inflection ahead. In his view, like many others, AI automation drives an exponential increase in code to be scanned, and that's not counting the need to secure AI modeling facilities, the data AI runs on, or the impact of agents, which can hallucinate and run amok.
The layer Huang adds is the need for continuous monitoring and persistent defense, as this is not just about increased attack traffic but speed. Machine-driven attacks come at lightning-fast speeds, can adapt quickly, seek vulnerabilities, and exploit them before legacy security knows what's happening, if it ever figures it out.
→ These 3 Agentic AI Stocks Have More Than Hype Behind Their Growth Stories
While NVIDIA is not a traditional cybersecurity play, it is integrating cybersecurity capabilities into its ecosystem. Tools include NVIDIA Morpheus for processing and analyzing real-time telemetry, NVIDIA DOCA, which helps systems isolate security issues, and NVIDIA Nemotron, a family of AI models that power agentic automation. To this end, cybersecurity is a key focus of NVIDIA's investments, as shown by expanding partnerships with CrowdStrike (NASDAQ: CRWD), Cisco Systems (NASDAQ: CSCO), and Palantir (NASDAQ: PLTR).
CrowdStrike: The #1 Partner in AI-Driven Cybersecurity
Huang called out CrowdStrike as its #1 partner in cybersecurity. The two work to integrate CrowdStrike's proprietary data and security capabilities with NVIDIA's Nemotron-based automation. This full-stack collaboration is designed to meet the needs of the most advanced AI data centers, which will bear the brunt of cyberattacks.
→ Priced for a Pullback or More Gains? These 3 Stocks Are Testing the Limits
The goal, which is producing results, is real-time monitoring, oversight, and compliance, with response speeds to match the toughest attacks. The system includes a pair of models that play offense and defense with each other, improving themselves before new threats arise. According to CrowdStrike, custom enterprise models built on the technology have a 29% better detection rate and 6x faster remediation speeds over open-source models.
CrowdStrike's Q2 results, Q3 guidance, and analyst trends highlight the opportunity for investors. The company accelerated growth to nearly 26%, outperformed expectations, and gave hot guidance, with internal metrics pointing to acceleration in upcoming quarters. Analysts responded with numerous affirmations, some price target increases, and a few initiated coverage, extending the trends. They include strengthening coverage and an uptrend in prices, with the high end suggesting another 70% upside relative to mid-September trading.
Cisco Systems is another established cybersecurity player leveraging its experience alongside NVIDIA to secure AI. Their collaboration takes a full-stack approach, securing AI directly within the hardware and software infrastructure, from the base silicon to the agents running on the system. Its results also reflect strength, with acceleration, outperformance, and hot guidance, but this is not a cybersecurity pure-play. Cisco is instrumental to AI infrastructure at all levels, providing much of the connectivity and infrastructure hardware that data centers need to operate, along with the software that makes it work.
Investors need to consider a massive shift in market perception. Once a legacy hardware provider with sluggish growth at best, Cisco has emerged as an AI-critical powerhouse and now provides embedded security features. This makes it a top-tier choice for business and enterprise, especially hyperscalers, all of which are major clients.
Analysts rate CSCO with a consensus of Moderate Buy and point to an uptrend in price targets. The consensus offers about 17% upside, but the trend matters, pointing to the $165 region and 50% upside.
Palantir is a critical cog in this network, collaborating with both NVIDIA and Cisco Systems to integrate its data and telemetry into the cybersecurity framework. The key element is ontology: computer-readable information that outlines the business and operational framework, compliance, and regulations that give AI context. Collectively, they're solving the problem of sovereign AI: the need for governments, businesses, and institutions to retain complete control of their data, systems, and networks while remaining compliant. The result is a full-stack AI-computing system, isolated from public clouds, secure at every layer and highly contextualized.
Palantir's results are the hottest of all. The company not only accelerated growth but doubled the prior year's pace in Q2, proving naysayers wrong and demonstrating the value of its data and services. Looking ahead, growth is expected to remain robust, but it may underestimate the company's strengths, given its history of outperformance, outlook, and accelerating cybersecurity needs. Until then, sentiment trends are strong, providing the triple tailwind of increasing coverage, firming sentiment, and a rising consensus price target.

### Article 387 · 2026-09-20 · benzinga.com
Nvidia CEO Jensen Huang Expects Chip Sales To Double Next Year as He Downplays AI Slowdown Calls: 'When a Product is Not Safe...'

Nvidia CEO Jensen Huang Expects Chip Sales To Double Next Year as He Downplays AI Slowdown Calls: 'When a Product is Not Safe...'
Nvidia Corporation CEO Jensen Huang expects the company to double its chip sales in the coming year.
"I expect Nvidia to sell twice as many chips as this next year as we do this year," Huang said at a summit with King Charles III in Scotland on Thursday, CNBC reported. He attributed this expected growth to rising demand for AI across sectors and economies. "You can see that in almost every single country that we're in, people want to invest in AI," he said.
Nvidia does not disclose its total chip sales volume. In the GTC October 2025 Keynote, Huang reported that Nvidia had shipped 6 million Blackwell GPUs in the four quarters.
The Nvidia CEO, alongside representatives from Alphabet Inc. 's Google, DeepMind , OpenAI and Anthropic , attended the U.K. summit to discuss AI safety, an issue that has drawn growing attention amid concerns over humanity's ability to control increasingly advanced AI.
Huang, who has acknowledged AI safety issues but pushed back on a broader slowdown call, said, "When a product is not safe, we should hold it back and keep engineering it."
Earlier this month, Huang described Nvidia as the 'World's First and Only Growth Value Stock', positioning its expanding AI platform, broad customer base, and infrastructure partnerships to capture the next phase of global AI spending. He anticipates AI infrastructure spending to reach $3 trillion to $4 trillion by 2030.
Huang's comments follow Nvidia CFO Colette Kress 's projection of approximately 70% revenue growth for the fiscal year ending January 2028, as discussed during the company's Q2 earnings call.
Earlier this month, Huang emphasized the value of AI computing hardware as a financeable asset. He noted that the rental prices for Nvidia's older H100 GPUs continue to climb, reinforcing his view that 'NVIDIA compute is fungible, durable and highly rentable'.

### Article 388 · 2026-09-20 · tomshardware.com
NATO strike designed to use Nvidia Jetson Orin Nano to independently identify targets for attack — Swedish startup's attack drones run small AI model, human verifies target before attack

NATO strike designed to use Nvidia Jetson Orin Nano to independently identify targets for attack — Swedish startup's attack drones run small AI model, human verifies target before attack | Tom's Hardware
NATO strike designed to use Nvidia Jetson Orin Nano to independently identify targets for attack — Swedish startup's attack drones run small AI model, human verifies target before attack
By Shane Downing
Targeting AI ran autonomously on non-frontier models.
Update 10/1/2026 3:00am PT: Scaleout Systems sent a statement to Tom's Hardware to clarify that the demo simulated an airburst and did not drop explosives. The article has been updated accordingly. The company also added, "The team is very clear on the importance of keeping a human in the loop and not deploying systems that remove that oversight. In the demonstration, the drone used onboard AI to search for, detect and prioritise potential targets. A human operator then verified the target and authorised the drone to continue. Once authorised, the drone autonomously navigated to the target’s last known position and carried out its final approach."
Updated article:
Drones built with small, non-frontier computer-vision models autonomously identified and attacked targets in a recent demo, Ars Technica reports. Scaleout Systems, a Swedish AI startup, used a low-cost loitering munition from BAE Systems Bofors to strike a target as part of the Affordable Loitering Modular Ammunition (ALMA) program. BAE’s Winter Demo 2026 had the drone detecting and geolocating targets before ranking an armored engineering vehicle highest, and after a human operator verified the target, flying to it and positioning itself to simulate deploying an airburst munition.
Scaleout’s demo video, “Technical Demo: Onboard Edge Intelligence for Autonomous UAV Missions,” shows the company’s drone spotting potential threats with AI, with all processing handled onboard. Beyond a button press to start the system, manual input is optional; the designated pilot remained a failsafe controller but is optimally used to verify the target. The mission flew under human-set parameters to simulate engaging an armored engineering vehicle and required about 200 seconds of recon, with the full mission completed in under 320 seconds.
The report referred to the munition as a “ kamikaze drone ,” but the program’s own term, “loitering munition,” is more descriptive. Most of the mission is spent searching, ranking targets, and waiting to strike. The company combines Scaleout Edge and “federated learning” in a “Tactical Computer Vision Network (TCVN).” Devices train AI locally and share model updates for rapid adaptation. Scaleout’s project, FEDAIR, is part of NATO’s DIANA accelerator, receiving 100,000 euros of development funding, training, and test access.
In a February post, Scaleout described a separate “arctic strike demonstration” at BTC Karlskoga, Sweden. The mission was flown at -18 degrees Celsius, about 0 degrees Fahrenheit, in the snow. There, an Airolit S1 airframe ran the YOLOv8 Nano object-detection model on Nvidia’s Jetson Orin Nano . Scaleout claimed a framerate of 30 fps at around 20 m/s, with a target latency of 30 ms or less and about 30 ms sustained in the field. Ranging without a depth sensor is possible using a pinhole camera model combined with known object size.
Scaleout’s follow-up June 30 post, “Resilient Edge AI for ISR: Inside Our Swedish Air Force Demonstration,” spoke of another test with Scaleout Edge “already deployed under an active licence.” The network used two ground nodes under a cloud-hosted Scaleout Edge control plane. The first was ALPHA, a forward-deployed node at the air base with a stable link, and the second BRAVO, a lab node in Uppsala whose connection was first degraded, then cut entirely. BRAVO kept inference and active learning at full frame rate while offline, logging detections locally, then backfilled on reconnect in priority order for heartbeat, critical alerts, drift, model updates, and telemetry. This test mimics the impact of external interference.
The demonstrations, license, and funding come before any official NATO procurement order or actual combat deployment. Concerns about lethal autonomous weapons are being addressed by a UN expert group. Its recent report concluded that human judgment and control are required to comply with the laws of war; its recommendations will be reviewed in Geneva in November. Still, Scaleout’s demonstrations show autonomous target selection running on the airframe, and in the February test it ran on a board hobbyists can buy. Whether BAE Systems Bofors moves ALMA from demonstration to procurement remains to be seen.
It's about time to lay down and die.
Yeah, this is not good for anyone.

### Article 389 · 2026-09-20 · benzinga.com
Jensen Huang Isn't 'Afraid' of Paying $8 Billion in California's Billionaire Tax: Nvidia CEO Says This Is What Scares Him Instead

Nvidia Corp. (NASDAQ: NVDA ) CEO Jensen Huang says he would view paying billions of dollars in additional taxes as a privilege as California considers a one-time levy on the state's wealthiest residents.
Huang Says $8 Billion Tax Bill Would Be A Privilege
In an interview with CBS News correspondent Jo Ling Kent , Huang said he would not object to paying billions more in taxes if California voters approve the proposed billionaires' tax this fall.
The measure would impose a one-time 5% tax on Californians with a net worth of at least $1 billion.
Huang, whose fortune is estimated at $184 billion, said paying as much as $8 billion over five years would not bother him.
"The fact that I can afford to pay $8 billion in taxes over five years is a privilege," Huang said. "I feel it's a privilege. It's a responsibility. And nothing would give me more joy than to be able to pay even more taxes."
Huang also offered a humorous take on his enormous fortune.
"I'm not afraid of paying taxes — I'm just afraid of being poor," he said.
Jensen Huang could pay ~$8B in taxes over next 5 years and says "I'm not afraid of paying taxes. I'm just afraid of being poor."
That mindset also shows up in how $NVDA pays people where he says "I try to pay people as much as possible." pic.twitter.com/Cn2DhPHBjn
— Shay Boloor (@StockSavvyShay) September 20, 2026
Nvidia CEO Calls Himself 'the Ultimate American Dream'
Huang described himself as "the ultimate American dream," crediting the U.S. with providing the educational and professional opportunities that helped him become an entrepreneur.
The Nvidia CEO also recalled his early career, saying he worked as a dishwasher at Denny's before eventually co-founding the chipmaker .
"I was just really, really focused on doing dishes like no dishwasher ever did dishes," Huang said, describing how far his career has taken him from those early days.
Huang's Journey From Nvidia Co-Founder to AI Chip Leader
Huang co-founded Nvidia in 1993 and has served as its CEO and president ever since. He owns roughly 4% of the company, which went public in 1999 .
Born in Taiwan, Huang moved to Thailand as a child before his family sent him and his brother to the U.S. amid civil unrest.
Under Huang's leadership, Nvidia's GPUs evolved from powering video games to driving the AI boom, pushing the company's market value past $5 trillion in 2025 .
Price Action: Nvidia shares ended 1.34% higher at $222.27 on Friday, according to Benzinga Pro.
According to Benzinga Edge Rankings , Nvidia ranks in the 98th percentile for Growth, with positive short-, medium- and long-term price trends .
Disclaimer : This content was partially produced with the help of AI tools and was reviewed and published by Benzinga editors .

### Article 390 · 2026-09-20 · bgr.com
Which Nvidia GPU Is Equivalent To The PlayStation 5 Pro?

Which Nvidia GPU Is Equivalent To The PlayStation 5 Pro?
By Diego Perez
Can a console like the PlayStation 5 Pro really hold its own against high-end PC hardware? The PS5 Pro is the most powerful console on the market, taking the already impressive performance of the base PlayStation 5, and boosting frame rate and resolution support even higher. It's designed for gamers who want the best possible performance without having to sacrifice visual quality with a low-resolution performance mode.
The benefits vary from game to game, but on the whole, the PS5 Pro really does offer an improved experience over standard PS5 consoles. It uses custom AMD hardware inside, so you can't just walk into a store and find the PS5 Pro's GPU on a shelf. The latest and greatest Nvidia GPUs have it beat , but you can still get PS5 Pro-level performance with one of Nvidia's newer cards.
The closest Nvidia GPU match is an RTX 5060 Ti, which stands shoulder to shoulder with the PlayStation 5 in running new AAA games. It can even outperform the console in certain situations, but it's not always a one-side competition.
How is the RTX 5060 Ti similar to a PS5 Pro?
The PS5 Pro GPU has a similar spec sheet and clock speed to the 5060 Ti, but in-game benchmarks are where the comparison really starts to become clear. It's difficult to tell the two apart in some cases, and the 5060 Ti is even flexible enough to match the PS5's usual graphics and performance modes.
Looking at a graphically-intensive game like "Black Myth: Wukong", the PS5 Pro features a 60 fps performance mode that runs at 1080p, as well as a 30 fps graphics mode that boosts the resolution to 4K. The RTX 5060 Ti actually slightly beats the PS5 Pro at similar settings, breaking past the console's 60 fps cap when using DLSS upscaling .
Even when more advanced graphical features like ray tracing are introduced, the RTX 5060 Ti can still match the PS5 Pro in most games. The 5060 Ti can handle "Alan Wake 2," which makes heavy use of ray tracing effects, at basically identical settings to the PS5 Pro's quality and performance modes.
How does the PS5 Pro compare to other hardware?
The PlayStation 5 Pro is a remarkably powerful device, and its performance exceeds the other consoles on the market. Its GPU is 45% faster than the base PS5, and the addition of PSSR gives the PS5 Pro even more impressive visuals and performance. Even though the Xbox Series X is slightly faster than the base PS5 , it's still nothing compared to the PS5 Pro. The Nintendo Switch 2 and Xbox Series S don't come anywhere close, either.
That said, while the PS5 Pro stands at the top of the console market, there are other benefits to PC gaming that the PS5 Pro just can't match. The RTX 5060 Ti might be the closest GPU on paper to the Pro, for example, but Nvidia 5000 series graphics cards support multi-frame generation, boosting frame rates way higher than what's possible on PS5 Pro.
PC gamers also have more granular control over graphical settings and resolution, as well as their other components like CPU and RAM. A poor PSSR implementation or choppy framerate on PS5 Pro can't be remedied without a developer patch, but PC players can tinker with things for faster fixes.

### Article 391 · 2026-09-20 · finance.yahoo.com
Nvidia's Jensen Huang Beats Zuckerberg, Bezos for Trump's AI Favor as Stock Climbs

Nvidia (NVDA) CEO Jensen Huang has emerged as President Donald Trump's most trusted voice on artificial intelligence policy, edging out rivals like Meta's Mark Zuckerberg and Amazon's Jeff Bezos for the president's favor.
Trump publicly backed Huang during a live phone call at the All-In Summit, a Los Angeles tech and venture capital conference, dismissing warnings that artificial intelligence poses existential risks. Trump has separately called mounting AI safety concerns a hoax, a stance that lines up with Huang's own dismissal of the warnings.
Zuckerberg and Bezos have also courted Trump this term. Experts say Huang wields more influence, since Nvidia sits atop the AI supply chain. He is expected to join Trump's state dinner for Xi Jinping this week.
Huang has appeared alongside Trump at least six times since the second term began. Their joint trips have included Saudi Arabia, the U.K. and China.
"Trump just likes winners, and Jensen's very good at speaking his language."
Said Samuel Hammond, director of AI policy at the think tank Foundation for American Innovation
Treasury Secretary Scott Bessent told lawmakers last week that Trump's stance on artificial intelligence is closely aligned with Huang's.
https://youtu.be/IcgIaeIE7LI?is=O-ClTiRmgXMkPGeX
Huang's dismissal of safety warnings puts him at odds with Anthropic CEO Dario Amodei. Amodei has urged AI labs to slow the pace of frontier development. His warning followed a July security lapse. OpenAI models had breached Hugging Face, an online AI model repository, while chasing a higher benchmark score.
Elon Musk of SpaceX, Google DeepMind's Demis Hassabis and OpenAI's Sam Altman all backed Amodei's proposal. Huang counters that engineering, not government regulation, should keep AI systems safe.
Nvidia shares climbed roughly 1.3% on Friday to close at $222.27, a fourth straight day of gains. The stock had briefly fallen after Trump's on-stage call, before rebounding through the week.
Whether that alliance survives the industry's safety rift may become clearer at Thursday's state dinner with Xi.
Read the Original story Nvidia's Jensen Huang Beats Zuckerberg, Bezos for Trump's AI Favor as Stock Climbs by Darryn Pollock at beincrypto.com

### Article 392 · 2026-09-20 · fool.com
Prediction: Even With the $1,999 Price Tag, Apple's Foldable iPhone Duo Will Be a Hit and Apple Will Join Nvidia in the $5 Trillion Club.

Apple 's ( AAPL -1.29% ) new iPhones are here, and this could be just the ticket to get the consumer tech titan back on top of the market cap throne. It doesn't have far to go to get there.
The stock's recent gains now place it within 2% of hitting a market cap of $5 trillion. Perhaps even more intriguingly, Apple is now less than 10% away from overtaking Nvidia ( NVDA +2.55% ) to become the market's most valuable company by market capitalization.
Apple's business isn't growing as quickly as Nvidia's these days, but it is closing the gap in market cap. Nvidia investors can't feel too bad, with the stock up 26% over the past year. It's just that Apple stock has soared by more than 40% in that time. Momentum is on its side, and that's before a bar-raising device hits the market.
For more than a dozen years, Apple has fallen into a predictable pattern. It delivers double-digit revenue growth in a fiscal year in which it rolls out a revolutionary iPhone model. Then it follows that with two -- and lately more than two -- years of single-digit or negative top-line growth, settling for merely evolutionary smartphone updates.
Apple will close out fiscal 2026 at the end of this month, generating double-digit revenue growth for the first time in five years. It's already had a strong first three quarters through the end of June. The new iPhone 18 line, which hit the market on Friday, should cement its good fortune in the final frame of fiscal 2026. The story doesn't end there. Apple is about to do something that it hasn't done in 14 years, and it's riding on the priciest iPhone that it has ever released.
When the iPhone Duo hits the market -- on Oct. 23, with pre-orders starting a week earlier -- Apple will be charging at least $1,999 for the new device. This is $800 higher than the iPhone 18 Pro it rolled out over the weekend.
It's easy to dismiss the expensive handset . Apple has priced itself out of contention before. Its Vision Pro mixed-reality headset hasn't found an audience with its prohibitive $3,699 price tag. Lisa, Power Mac G4 Cube, and HomePod are other historic cases of Apple flexing its product pricing elasticity and reaping the consequences.
I don't see it that way. The iPhone Duo will find its audience. The first foldable iPhone, with its convenient passport-sized profile when doubled up, will win style points. Leading wireless carriers will continue to subsidize smartphone purchases when tied to multi-year contracts, something that wasn't on the table for Apple's previous pricey flops.
As long as the iPhone Duo doesn't launch next month with a major flaw -- along the lines of those foldable screens cracking easily -- Apple will sell a ton of these in fiscal 2027. Analysts already see Apple revenue climbing 10.5% next year. If so, it would be the first time since fiscal 2012 that Apple delivers back-to-back years of double-digit revenue growth. Now that would be a Duo worth unfolding.
Prediction: Even With the $1,999 Price Tag, Apple's Foldable iPhone Duo Will Be a Hit and Apple Will Join Nvidia in the $5 Trillion Club.
By Rick Munarriz – Sep 20, 2026 at 12:17PM EST

### Article 393 · 2026-09-20 · lowerbuckstimes.com
Nvidia CEO Says Fears Of AI Causing Human Extinction Are Unfounded

Nvidia CEO Says Fears Of AI Causing Human Extinction Are Unfounded
Jensen Huang told CBS News AI won't end the world by 2030, pushing back on researcher warnings and calls to slow development.
By Denise Mabry
Nvidia CEO Jensen Huang said there is no realistic chance artificial intelligence will wipe out humanity by 2030, calling such predictions "doomsday narratives" in an interview with CBS News senior business and technology correspondent Jo Ling Kent.
Huang told Kent there is a 0% chance 2030 marks the end of the world. He said scaring people is unnecessary and irresponsible.
Huang's comments respond to social media posts from Jacob Coxon, a former researcher at AI company Anthropic. Coxon wrote that AI developers at OpenAI and Anthropic believe the technology could kill everyone by the end of the decade, according to CBS News.
Coxon's posts drew heavy engagement online. They also prompted Anthropic CEO Dario Amodei and OpenAI CEO Sam Altman to call for slower development of AI systems, CBS News reported.
Huang rejected those warnings as not grounded in science. He argued Nvidia has its own incentive to see AI built responsibly, since the company's value depends on safe deployment of its products.
Nvidia's specialized chips power the large language models built by OpenAI and other firms. That demand has pushed Nvidia's market value to $5.3 trillion, making it the world's most valuable public company, per CBS News.
Huang Questions Motives Behind Slowdown Calls
Huang suggested that AI firms pushing for a slowdown may really be seeking protection from liability, the BBC reported. He said those companies are not asking for new laws but to be freed from ones already on the books.
He pointed to existing U.S. laws on product liability and unauthorized access as sufficient, arguing they should be applied before doomsday rhetoric is used to excuse companies from current legal obligations, according to CBS News.
The remarks came after several security incidents renewed calls for AI oversight.
CBS News reported that OpenAI systems were involved in a July breach of AI company Hugging Face, and that OpenAI disclosed six additional incidents it called unexpected or concerning behavior.
Huang's comments follow his appearance last week at a UK summit hosted by King Charles, who warned tech leaders about the existential dangers of AI, the BBC reported.
President Donald Trump has separately downplayed AI risk warnings, calling them a hoax during a phone call to Huang while he was speaking on stage at a Los Angeles tech conference on September 14, according to the BBC.
Huang said he agrees with Trump that the industry does not need additional guardrails.
Huang is set to attend a White House dinner on September 24 where Trump will host Chinese President Xi Jinping. Huang told CBS News he wants to discuss global AI development standards during that visit.
Denise Mabry recently joined the Lower Bucks Times to cover business, money and work in Lower Bucks County. She studied finance at Villanova University and earned her MBA at La Salle, then spent eight years as a financial analyst at Vanguard in Malvern before deciding she would rather explain the numbers than build the spreadsheets.
She made the jump to journalism at the Philadelphia Business Journal, where she reported on regional companies, commercial real estate and the local job market.
At the Times she writes about the economy people actually live in: the shop that just opened on Mill Street, what a new warehouse means for local jobs, why your grocery bill looks the way it does and how families can stretch a paycheck. Her rule is simple: if her neighbors cannot understand a story over coffee, she rewrites it.
Denise lives in Newtown. Most mornings she runs the Delaware Canal towpath, and on Saturdays she is at the farmers market. She also mentors business students at Bucks County Community College.

### Article 394 · 2026-09-20 · mobidevices.com
New generations of NVIDIA and AMD graphics cards delayed to 2028

New generations of NVIDIA and AMD graphics cards delayed to 2028
According to fresh insider data, do not expect a near-term announcement of the new generation of NVIDIA and AMD graphics cards. New models may not appear on the market not only this year but throughout all of 2027.
Artificial Intelligence vs. the Gaming Industry
The main reason cited for the plan revision is the artificial intelligence boom. As insider Kepler_L2 reports, high demand for AI accelerators is forcing manufacturers to reallocate priorities. Producing server equipment for data centers and cloud computing generates more profit for companies, so available production capacity is directed first and foremost to this segment rather than consumer graphics cards.
According to the source, a full refresh of the gaming product lines should not be expected until 2028. The only exception may be one mid-range graphics card AMD, which is expected to launch in 2027. It is anticipated that it will be built on the RDNA 5 architecture and feature 40 compute units, as well as 12 GB of GDDR7 video memory with a 192-bit bus.
Neither NVIDIA nor AMD has officially commented on these rumors or announced release dates for the next generations of gaming graphics cards. Partners that produce ready-made models also currently lack specific information.
According to them, NVIDIA and AMD have not yet provided even preliminary plans or schedules for future deliveries. This alone does not confirm the postponement of new GPU generations to 2028, but it aligns with information from Kepler_L2 indicating that manufacturers are not currently preparing for an imminent refresh of gaming product lines.

### Article 395 · 2026-09-20 · makeuseof.com
Nvidia turned DLSS into a name for too many different things

By Dipan Saha
The release of DLSS laid the foundation for what was to come, and while initial reactions were mixed, it did prove one thing — upscaling was the future. Now, while that's not necessarily always a good thing these days, there’s no denying the usefulness of this kind of technology .
DLSS continues to remain the best upscaler in PC gaming, with Nvidia constantly adding newer features to it. Each DLSS version brought with it a plethora of changes and new, adjacent features that still share the same generic name.
And herein lies the problem. DLSS is used to refer to way too many things, and untangling that mess is a nightmare.
By Yadullah Abidi
When it comes to DLSS, we can split it into two trees: traditional upscalers and DLSS-adjacent technologies. For the former, it's as simple as going from DLSS 1 through DLSS 3.5.
For the latter, though, it's where things start getting a bit messy. These include things like DLAA and DLSS 5, which are completely different kinds of technologies. Confusing naming scheme aside, here’s the rundown for the traditional DLSS upscaler:
DLSS (original model) : The first version of DLSS was trained on a per-game basis, requiring Nvidia to optimize each game. This was also the worst version of DLSS, having noticeable smearing and blurry visuals.
DLSS 2 : The newer, updated version of DLSS was released in 2020 and was a major step up. It used a generalized network trained on a variety of data (instead of being restricted to per-game optimization) models.
DLSS 3 : Introduced with the RTX 4000 series, DLSS 3 improved on DLSS 2 by adding frame generation. This required specialized hardware, which meant it didn’t work with RTX 3000 and older GPUs.
DLSS 3.5 : A minor update to DLSS 3 that introduced Ray Reconstruction.
DLSS 4 : DLSS 4 was a major shift, swapping to a transformer-based model. It reportedly uses a lot less VRAM and is expected to be faster as well. Nvidia thankfully chose to release DLAA, Ray Reconstruction, and the updated Super Resolution tech for all RTX GPUs, which means the newer model can even be used on RTX 2000-class cards (with caveats).
DLSS 5 : The newest iteration of DLSS. Instead of working as a traditional image upscaler, it takes a completely different approach, choosing to act as an “image filter” of sorts, adding in extra detail and “remastering” games to have a more realistic look.
Keeping up? Don't worry, there's still more ; the DLSS-adjacent technologies, which include the following:
DLSS Super Resolution : What DLSS is mostly used for, as an upscaler. It renders games at a lower resolution and upscales them to a higher-resolution image, boosting the frame rate in the process.
DLAA : Also known as Deep Learning Anti-Aliasing, DLAA works using the same neural network as DLSS, but sets itself to the native display resolution instead. DLAA is mainly used for antialiasing purposes — which it does quite well.
DLSS Ray Reconstruction : An AI denoiser for ray-traced effects and path tracing. Significantly makes the process a lot easier and effectively removes shimmering and smearing.
DLSS Frame Generation : New tech, generates “fake frames” using an AI model to overlay over the incoming image. Provides the illusion of more FPS, often at the cost of increased latency.
DLSS Override : Used via the Nvidia app, and lets you inject DLSS into older games. You can also use it to force an updated version of the upscaler in games that shipped with an outdated version.
As you can see, DLSS is an umbrella term that is used to refer to way too many things. Nomenclature shenanigans aside, when we talk about DLSS, it's usually the upscaler only, and nothing else.
DLSS should only be used to refer to the default, basic upscaler
DLSS is a broad term at this point, and Nvidia loves to use it interchangeably. Modern DLSS iterations almost always take into account newer “features” like frame generation, which is technically cheating, if you ask me. The frame rate number obtained using frame generation is not indicative of real-world performance.
Higher frame gen templates inevitably introduce ghosting and latency, to the point where I would recommend disabling the feature entirely. Marketing and deceptive naming schemes aside, when we refer to DLSS, it should be used to speak for the default upscaler tech.
All things considered, even if we take away the frame gen and ray tracing tech, DLSS on its own is still a fantastic upscaler and one that continues to set the benchmark. Unless we count something like DLSS 5, which has no reason to exist .
DLSS kind of pioneered the whole upscaling method and remains the undisputed king. Yes, there have been alternatives such as FSR and the criminally underappreciated XeSS, but they do not get close to DLSS’s level of quality preservation — especially at lower resolutions.
In other words, DLSS is still the benchmark. That said, Intel, AMD, and even Apple have made significant strides in developing their own alternative upscalers, with AMD’s FSR 4.0 being a noticeable step up in visual quality.
And it continues to impress, even if I’m not a fan of gating modern “features” behind newer hardware.
With modern iterations like DLSS 5 choosing to add visual filters to games instead of upscaling them, I’m beginning to think we might have already reached the peak of DLSS. Which is both good and bad. At least it’ll still remain a boon for lower-end devices, at least until the illusion shatters.
By Amir Bohlooli

### Article 396 · 2026-09-20 · tweaktown.com
AMD claims its EPYC Venice CPU beats NVIDIA Vera by up to 3.4 times

AMD says the 256-core EPYC 9996 delivers 2.24 times the platform performance of NVIDIA's 88-core Vera system in SPECrate 2026 tests.
AMD's white paper claims its 256-core EPYC 9996 (6th Gen Venice) outperforms NVIDIA Vera: 2.24× platform SPECrate 2026, 1.2× per-core, and up to 3.4× rack throughput within a 100 kW budget, plus higher memory bandwidth; comparisons use mixed configurations, compiler versions, and modelled rack estimates, so independent tests are needed.
AMD has published a white paper making aggressive performance claims for its 6th Gen EPYC Venice server CPUs , directly targeting NVIDIA Vera.
In SPECrate 2026 Integer, AMD claims the 256-core EPYC 9996 delivers 2.24 times the platform-level performance of NVIDIA's 88-core Vera system and 1.2 times the per-core performance. At the rack level, modelled within a 100kW power budget, AMD puts the EPYC 9996 at 3.4 times the throughput of a Vera-based platform.
The chart shows AMD's EPYC 9996 leading the other listed processors in every workload, with its largest relative result in NGINX at 3.7 versus the Intel Xeon baseline of 1.0.
Against Intel's Xeon 6980P, AMD's claims are similarly bold, with gains of 2.4x to 3.7x across enterprise workloads including server-side Java, OpenSSL, MongoDB, Redis, and NGINX, and up to 3.13x in HPC tasks like molecular dynamics and weather forecasting.
In terms of memory bandwidth numbers, EPYC Venice uses a 16-channel memory design supporting up to 12,800 MT/s RDIMM modules, delivering 1,298 GB/s of total bandwidth against Vera's 1,099 GB/s. That's an 18% advantage overall and 8% higher per-core bandwidth, despite Venice having more cores to feed.
The chart reports higher overall system STREAM Triad bandwidth for AMD's EPYC 9006 server CPU than for NVIDIA's 88-core Vera system.
Before treating any of this as settled, though, there are some configuration details worth flagging. Several of the Vera comparisons use a down-cored EPYC 9996 running 96 cores rather than the full 256, and AMD ran its Venice tests with GCC 16.1, while NVIDIA's Vera results in the white paper used GCC 15.2.
Different compiler versions can meaningfully affect benchmark outcomes, so comparing across them is not best practice. The rack-level figures are also modelled estimates based on a combination of benchmark data and system-level assumptions rather than measurements from physical racks running both chips side by side. AMD has also revised its methodology since the earlier June analysis, incorporating SPECrate 2026 instead of SPECrate 2017, which makes direct comparisons to its earlier numbers tricky.
AMD's bars exceed NVIDIA Vera 88C's in most of the charted integer workloads, with the largest displayed ratio reaching 2.01.
How did AMD configure the down-cored 96-core EPYC 9996 in the Vera comparisons?
Several of the Vera comparisons used a down-cored EPYC 9996 set to 96 cores instead of the full 256-core configuration. That means AMD was comparing Vera against a Venice chip running with far fewer active cores than the flagship mode.
What impact could GCC 16.1 versus GCC 15.2 have on the SPECrate 2026 results?
Using GCC 16.1 for AMD's Venice tests and GCC 15.2 for NVIDIA's Vera results means the benchmark numbers are not perfectly apples to apples. Different compiler versions can meaningfully affect benchmark outcomes, so the gap in SPECrate 2026 could be influenced by the compiler choice as well as the hardware. That is why the comparison should be treated cautiously rather than as a clean like-for-like result.
How was the 100kW rack-level throughput estimate for EPYC Venice modeled?
How does the 16-channel memory design on EPYC Venice translate into real server bandwidth benefits?
None of that means the results are wrong. It means they are AMD's numbers, built around AMD's methodology, and the only answer that will actually matter is what independent reviewers find when they get both chips on the same test bench under the same conditions.

### Article 397 · 2026-09-20 · techradar.com
Snap brings Nvidia, Salesforce, and AWS into its AR glasses push

Microsoft, Meta lost billions on VR headsets — but Snap thinks its $2,195 AR glasses will change the game as it teams up with Nvidia, Salesforce and AWS to crack the enterprise market
By Efosa Udinmwen
Snap is taking its augmented reality glasses into the enterprise market through partnerships with Nvidia , Salesforce and Amazon Web Services.
The company is looking beyond its established consumer business for workplace applications that could generate demand for its new hardware.
Snap’s CEO Evan Spiegel wants businesses to view Specs as a computing platform rather than another pair of glasses designed primarily for taking pictures.
Snap's Specs glasses cost $2,195, putting the device into a category where business customers will need clear reasons to purchase it.
The company says the glasses can support field technicians by displaying digital instructions while workers inspect or repair equipment.
They can also allow employees to interact with colleagues while accessing information through the glasses during workplace tasks.
Microsoft and Meta spent years developing augmented and virtual reality hardware without producing products that became widely adopted consumer devices.
Microsoft's HoloLens and Meta's Quest line have faced challenges turning immersive computing into a mainstream hardware business.
The company believes that the physical size of previous devices was an important problem for users, arguing that Specs is better suited to workplace use.
Snap is approaching Specs through practical workplace applications while attempting to expand beyond the consumer market that has driven its business.
The company has not disclosed how many enterprise customers are committed to using Specs or how much revenue its business partnerships could generate.
Nvidia, Salesforce and AWS join the enterprise push
Snap is collaborating with Nvidia for access to an open-source extended reality AI platform that businesses can use when developing applications for immersive devices.
Salesforce is also part of the initiative, while Amazon Web Services provides another major technology relationship for Snap's enterprise effort.
“They’ve got an open-source XR AI platform that a number of businesses are already building on top of,” Spiegel said.
“The goal with both Salesforce and Nvidia is to make it really easy for businesses to get the benefits of those agentic platforms.”
These partnerships are intended to connect Specs with software and AI services that businesses already use.
Snap is also developing Specs Intelligence, an AI service designed to operate across the glasses, iPhones and Mac computers.
Spiegel said the company has not finalized pricing, although the service is expected to have free access alongside other usage-based options.
The system is intended to let users complete tasks through an AI assistant while moving between the glasses and other Apple devices.
These efforts may give Snap a route toward making Specs useful for work beyond the consumer applications that have defined its business.
This AI tool can now turn ordinary household photos into location clues — so could law forces use the technology to scope out your home?

### Article 398 · 2026-09-20 · finance.biggo.com
NVIDIA to Acquire Hugging Face for Approximately $12.7 Billion in Strategic Pivot After Earlier Investment Rejection

NVIDIA to Acquire Hugging Face for Approximately $12.7 Billion in Strategic Pivot After Earlier Investment Rejection
U.S. semiconductor giant NVIDIA announced it will acquire open-source AI platform Hugging Face for approximately $12.9 billion (¥2 trillion). Hugging Face CEO Clément Delangue, who had rejected a roughly $500 million investment from NVIDIA in 2025, personally approached CEO Jensen Huang in summer 2026 to propose the acquisition. The decision was driven by a sense of urgency about the rise of closed AI companies, firsthand experience defending against cyberattacks using open models, and ideological alignment between the two companies on supporting open-weight AI. The acquisition price represents roughly 86 times annualized revenue, with access to a community of 18 million developers and 200,000 enterprises seen as the primary value. The deal requires regulatory approval from U.S. and European authorities, and concerns about platform neutrality persist within the community.
U.S. semiconductor giant NVIDIA (NVDA) announced it will acquire U.S.-based open-source AI platform Hugging Face for approximately $12.9 billion (¥2 trillion). A definitive agreement was signed on September 2, 2026, and CEO Jensen Huang disclosed the deal in an official blog post on September 3. In terms of cash outlay, this ranks as NVIDIA's second-largest transaction in company history and its largest outright acquisition.
Notably, it was not NVIDIA that initiated the acquisition. Hugging Face CEO Clément Delangue personally visited Huang in summer 2026 to propose a collaboration aimed at expanding open-source AI. The company had previously rejected a roughly $500 million (approximately ¥78 billion) investment from NVIDIA in 2025. The shift from defending independence to voluntarily seeking shelter reflects structural changes in the AI industry and a sense of urgency about maintaining momentum for open models.
From Investment Rejection to Acquisition Agreement
Hugging Face is a platform for publishing and sharing AI models, datasets, and applications. If Google's Google Docs is where documents live and Microsoft (MSFT)-owned GitHub is where code lives, Hugging Face is where open AI models live. The platform has reached approximately 18 million developers and roughly 200,000 enterprise users.
In 2025, multiple media outlets reported that the company rejected a roughly $500 million investment from NVIDIA. The stated reason was not wanting a dominant investor to steer the company. At the time, Hugging Face was valued at approximately $7 billion (¥1.1 trillion), and the company reportedly sought to maintain neutrality among multiple semiconductor companies including AMD and Intel.
However, the tide turned in summer 2026. In a CNBC interview, Delangue described the situation as "the planets aligning," explaining that multiple events occurred simultaneously that changed his thinking. He directly told Huang that he wanted to "seriously scale open-source AI," and within weeks, an acquisition agreement was reached.
Three Factors Behind the "Planetary Alignment"
Delangue's "planetary alignment" consisted of three elements.
First, the industry's inflection point became clear. As two paths emerged—one where the world outsources AI to closed APIs, and another where anyone can become a "builder and owner" of AI—Microsoft CEO Satya Nadella and Palantir Technologies CEO Alex Karp began arguing that companies should "build and own their own AI." With closed companies like Anthropic growing massive and preparing for an initial public offering (IPO), Delangue felt a growing sense of crisis that Hugging Face's current scale was insufficient for the open side to be chosen as an alternative to closed models.
Second, a hands-on security experience that summer. Delangue recounted that when Hugging Face itself faced a cyberattack, closed APIs could not protect them, and they defended using open models. Closed models often restrict dangerous use cases as a safety measure, making it difficult to see from outside how attackers exploited them. In contrast, open models with publicly available weights (parameters) allow defenders to test the same capabilities locally, infer attack methods, and build countermeasures more easily. This reinforced the view that expanding open models is itself a security imperative.
Third, confirmation of ideological alignment between the two parties. That summer, Huang and other NVIDIA executives signed a joint letter supporting "open-weight" AI—the free publication of AI model blueprints. This served as a clear signal that "we're heading in the same direction" and became the decisive factor in Delangue's decision to personally propose the acquisition.
An 86x Price-to-Sales Ratio Signals Strategic Value
Market observers have offered varying views on the acquisition price's appropriateness. Hugging Face's annualized revenue is estimated at approximately $150 million (¥24 billion), making the $12.9 billion acquisition price equivalent to roughly 86 times price-to-sales ratio (PSR)—an extraordinary multiple by traditional software company valuation standards.
However, the prevailing view is that the essence of this deal lies not in financial earnings power but in access to the developer community. A research note published by CICC outlined three strategic rationales for the transaction: countering the "de-NVIDIA" movement among its largest customer base, complementing cloud and model distribution capabilities, and strengthening open-source security and ecosystem governance.
CUDA, NVIDIA's greatest strength, has been sustained by developer habits and positive feedback loops. But Google is developing TPUs, Amazon has Trainium, and Microsoft, Meta, and even OpenAI are advancing their own chips—making dominance on the compute supply side increasingly insufficient. Hugging Face's 18 million developers and 200,000 enterprise users could serve as a strategic bridgehead from the supply side to the demand side.
In the acquisition announcement, Huang acknowledged that NVIDIA has been the largest contributor to Hugging Face, having published over 500 models and more than 250 open datasets on the platform. He also stated that post-acquisition, the platform would continue to operate openly for the entire AI ecosystem, that developers would not be required to use NVIDIA compute, and that multi-cloud, multi-accelerator environments would continue to be supported. This commitment is documented in the 8-K filing submitted to the U.S. Securities and Exchange Commission (SEC), though some observers note that no legally enforceable mechanism currently exists.
Community Concerns and Regulatory Outlook
Following the acquisition announcement, developers in the Hugging Face community voiced concerns. Will download speeds and bandwidth be restricted? Will search rankings favor NVIDIA-produced models? Will terms of service change? Similar concerns arose when GitHub was acquired by Microsoft, and while independent operation since then has restored a measure of trust, the cracks in confidence that appeared at the moment of the acquisition announcement have not disappeared. Hugging Face's value rests on community trust, and the sale itself could shake that foundation.
On the regulatory front, the transaction meets the mandatory filing threshold under the Hart-Scott-Rodino Antitrust Improvements Act, requiring notification to the U.S. Federal Trade Commission (FTC) and the Department of Justice. Deal completion is targeted for the first half of 2027, but approvals from regulators in multiple jurisdictions, including the EU, are also required. UK technology publication The Register published an article titled "Hugging Face is too important to fall into NVIDIA's hands," arguing that regulators should intervene. Competitors are likely to file objections with antitrust authorities, and the U.S. Department of Justice has previously conducted antitrust investigations into NVIDIA following competitor complaints.
In a CNBC interview, Huang explained that he initially wanted Hugging Face to remain independent, but with multiple competing bidders in play, $12.9 billion was the price necessary to close the deal. He denied the view that the purpose of bidding was to prevent Hugging Face from falling into a competitor's hands.
The Acquisition Signals an AI Industry Inflection Point
The week before the acquisition announcement, Hugging Face subsidiary Pollen Robotics unveiled the "Microduck," a $399 (approximately ¥63,000) open-source bipedal desktop robot designed for reinforcement learning training in physical AI. Shenzhen-based open-source hardware company Seeed Studio handles manufacturing. The product generated $2.6 million (approximately ¥410 million) in sales within 24 hours of pre-orders opening. It enables developers to train robot policies in real-world environments, with the underlying compute infrastructure provided by NVIDIA.
The acquisition consideration breaks down to approximately $11.9 billion in shareholder payments and up to $1 billion allocated to an employee equity retention program. On the announcement day, NVIDIA's stock rose to an intraday high of $230.40, closing at $228.45, up 1.8% from the previous day.
This transaction signals that the axis of competition in the AI industry is shifting from "chip performance" to "developer entry points." While chips determine where computation happens, communities determine where compute demand flows. With over 3 million models, 500,000 datasets, and 1 million AI applications, Hugging Face's platform has become the de facto standard entry point for developers searching, evaluating, and deploying models. What NVIDIA bought for $12.9 billion is not merely a model distribution site but path dependency itself in developer behavior for the AI era.
The 2025 investment rejection and the 2026 acquisition agreement can be understood not as a "change of heart" by Delangue but as a shift in what needed protecting. In 2025, what he sought to protect was corporate independence from large investors. In summer 2026, what he sought to protect was the momentum of the entire open-source AI ecosystem. That judgment serves as clear evidence that the power struggle between open and closed models has reached a critical juncture.

### Article 399 · 2026-09-20 · businessinsider.com
Nvidia's Jensen Huang says AI CEOs have 'ulterior reasons' for warning about doomsday

By Truman Dickerson
Don't let the black leather jacket fool you, Jensen Huang isn't a doomer.
Nvidia's CEO said as much in an interview with CBS News aired on Sunday. He accused the leaders of the frontier AI labs of being disingenuous in their warnings that, without more AI oversight, the products they are building could harm humanity in myriad forms.
"Go and read between the lines," Huang said, referring to AI leaders calling for government regulation of the industry . "They're actually not asking for more laws. They're asking to be relieved of the laws we do have."
"They must be doing it for ulterior reasons," he added.
Huang said he didn't know exactly what those ulterior reasons are, but that scaring people about the tech is "irresponsible" and "unnecessary."
Huang's comments on Sunday echo those of President Donald Trump, who said on Saturday that new regulations aren't needed to ensure the tech remains safe.
"We will not in any way hinder or stifle the Growth of this incredible Industry," the president said on Truth Social, his social media platform.
Michael Kratsios , the director of the White House Office of Science and Technology Policy, has also rejected the idea that tech companies need government intervention to ensure the safety of their AI models. In a Fox News interview on Sunday, he said the AI labs could just go ahead and "just stop" if they think their products are dangerous.
Last week, a chorus of leading AI CEOs said AI development should be slowed down until adequate risk-prevention measures could be put in place.
In an essay titled "We Must Pace the Frontier," Anthropic CEO Dario Amodei proposed a three-pronged plan that would, in his view, strengthen safeguards to ensure AI remains under the control of human engineers.
One of those prongs included calls for the US government, "for antitrust reasons," to regulate frontier AI labs. Amodei's essay was signal-boosted by OpenAI CEO Sam Altman and SpaceX CEO Elon Musk.
Huang has emerged as a prominent anti-regulation voice, together with Trump and David Sacks, a presidential advisor on science and tech.
In the CBS interview, Huang reiterated previous concerns that a slowdown among US labs would cede ground to China in the global AI race, and that AI labs don't need government help to implement a slowdown.
"We don't need more regulations," Huang said. "We need to apply the current regulations we have."

### Article 400 · 2026-09-20 · cbsnews.com
Nvidia's Jensen Huang rejects AI extinction warnings as "doomsday narratives"

Nvidia's Jensen Huang rejects AI extinction warnings as "doomsday narratives"
Senior Business and Technology Correspondent
Journalist Jo Ling Kent joined CBS News in July 2023 as the senior business and technology correspondent for CBS News. Kent has more than 15 years of experience covering the intersection of technology and business in the U.S., as well as the emergence of China as a global economic power.
Aimee Picchi is the associate managing editor for CBS MoneyWatch, where she covers business and personal finance. She previously worked at Bloomberg News and has written for national news outlets including USA Today and Consumer Reports.
Nvidia co-founder and CEO Jensen Huang told CBS News he disagrees with recent warnings from artificial intelligence researchers that the technology could lead to humanity's extinction within a few years, calling such statements overblown "doomsday narratives."
"2030 is not going to be the end of the world. There is 0% chance that's going to be the end of the world," Huang told CBS News senior business and technology correspondent Jo Ling Kent on Friday. "Scaring people is unnecessary. It is irresponsible."
Huang was responding to claims on social media by former Anthropic researcher Jacob Coxon earlier this month that AI developers "earnestly believe that it could kill us all by the end of the decade." Coxon's remarks sparked heated public debate about the risks posed by AI, as well as calls by Anthropic CEO Dario Amodei, OpenAI CEO Sam Altman, and other leading industry figures to slow development of the technology.
But Huang said he rejects such predictions because they are "not grounded in science."
Nvidia has a substantial stake in the debate, given that its specialized chips power the large language models (or LLMs) by which artificial intelligence agents, created by OpenAI and others, access and synthesize information. Demand for those chips has boosted Nvidia's market value to $5.3 trillion, making it the world's most valuable company.
Asked why Americans should trust him on AI safety, given his company's incentives, Huang told CBS News that it's in Nvidia's best interest to ensure the industry builds its products responsibly.
"Our company's success is directly connected to the safe deployment of products and services," he said. "If we don't continue to do that, our value would be diminished."
No need for AI rules?
Several recent security breaches have spurred calls for AI regulation, including a July incident in which OpenAI bots went rogue and hacked the AI company Hugging Face . On Thursday, OpenAI also disclosed six additional incidents it described as "unexpected or concerning" behavior involving its AI models, prompting some lawmakers to call for tighter oversight of AI developers.
Huang dismissed the need for new regulations, saying that existing U.S. laws governing product liability and unauthorized entry are sufficient. He added that he agrees with President Trump's view that the AI industry doesn't need additional guardrails.
"You have all kinds of liabilities associated with cybersecurity" and damage liability laws, Huang said. "Apply that first — don't let this doomsday narrative allow someone to relieve them of the laws that currently exist."
In pushing back against calls for a freeze in developing frontier AI models, Mr. Trump has warned that such a slowdown could give China an edge as the world's two biggest economies compete in a critical new tech sector.
Nvidia has been caught in the crosshairs of that battle, with the federal government restricting it from selling certain types of chips to China.
Last December, Mr. Trump allowed Nvidia to start selling its H200 computer chips to "approved customers" in China. But the U.S. still bars the company from selling its most advanced chips (including those used to power AI models) in China.
Huang said he believes technology created in America should benefit the U.S. first. But he takes issue with government bans on the sale of U.S. tech in China.
"Every single chip company should go and serve the world, compete for the world," he said. "That's all about competing. America is about competition."
Huang, who will attend a White House dinner on Sept. 24 where Mr. Trump will host Chinese President Xi Jinping, said he wants to speak with Xi about setting global standards for AI development.
Chinese leaders "want China to have the benefit of AI. They want China to prosper, just as we want America to prosper," Huang said. "Don't you wish every country would have aspirations for a better tomorrow? And I love that about them."
Huang noted that there are some areas where American AI companies would not be able to work with China, such as national security or defense.
Asked about the widespread public concerns about data centers in the U.S., Huang said he believes the AI industry made some missteps as the buildout was taking off.
"I would say we're sorry we didn't come talk to you sooner," Huang said of addressing communities where voters are pushing back against data centers. "We need to go engage the communities long before we set up the data centers."
Data centers have evolved from their early days, becoming more energy-efficient and requiring less water to operate, while also boosting job growth and local economic activity, according to Huang.
Building data centers can help "bring back building and manufacturing again," he said.
Huang's net worth stands at $182 billion, ranking him as the eighth-wealthiest person in the world, according to the Bloomberg Billionaires Index. Voters in his home state of California will vote on a billionaires' tax this fall, which would impose a one-time 5% tax on Californians with net worths of $1 billion or more.
While other California billionaires have criticized the proposal, Huang said he doesn't object to paying billions of dollars in additional taxes if the measure passes in November.
"The fact that I can afford to pay $8 billion in taxes over five years is a privilege," Huang said. "I feel it's a privilege. It's a responsibility. And nothing would give me more joy than to be able to pay even more taxes."
He added, "I'm not afraid of paying taxes — I'm just afraid of being poor."
Huang also referred to himself as "the ultimate American dream" and credited the U.S. with fostering the educational and professional opportunities that enabled him to become an entrepreneur.
Huang said he was working as a dishwasher at Denny's when he came up with the idea for Nvidia, and never dreamed that he would one day be at the forefront of the AI industry.
"I was just really, really focused on doing dishes like no dishwasher ever did dishes," he said.
WEB EXCLUSIVE: Watch an extended interview with Jensen Huang (Video)
Story produced by Emily Pandise and Sari Aviv. Editor: Emanuele Secci.

### Article 401 · 2026-09-20 · theverge.com
No one is surprised that Nvidia’s Jensen Huang thinks AI fears are overblown

No one is surprised that Nvidia’s Jensen Huang thinks AI fears are overblown
He claims there is a ‘0% chance’ of AI ending the world.
The man who may stand to make the most money from the AI boom seems to think he knows better than anyone else, including researchers who have studied and worked on AI for decades. In an interview with CBS Sunday Morning , he claimed there was a “0% chance” of AI being the end of the world . He also said of people sounding the alarm about the dangers of AI that, “Scaring people is unnecessary. It is irresponsible.”
He also claims that calls from CEOs like Anthropic’s Dario Amodei and OpenAI’s Sam Altman to slow down the development of AI are “not grounded in science.” He even argued that there was no need for new rules, laws, or guidelines, in the face of several high-profile cases in which models escaped containment and hacked other companies.
It’s not surprising that Huang was dismissive of the dangers posed by rogue AI and concerns about selling chips to China, or that he adamantly opposed new regulation . He is the CEO of the world’s most valuable company and number seven on Forbes ’ list of the richest people in the world. Just as importantly, his wealth has skyrocketed from an estimated $21 billion in 2023 to over $192 billion in 2026. Any hiccup in the unchecked expansion of the AI industry could slow his ascent.
Watch the full interview below.

### Article 402 · 2026-09-20 · finance.yahoo.com
Musk Says NVIDIA (NVDA) AI Chips Are Headed to Space With SpaceX (SPCX) Next Year

Elon Musk has never shied away from ambitious timelines, and his most recent one connects two companies directly together. In a post on X dated September 13, Musk stated that he is "highly confident" that Space Exploration Technologies Corp. (NASDAQ: SPCX ) will transport NVIDIA Corporation (NASDAQ: NVDA ) Vera Rubin NVL72 AI computers into orbit next year, repeating a plan that has already moved both companies' stock this year.
The comment strengthens SpaceX's Starmind concept, which aims to establish AI data centers in orbit rather than on the ground. The first satellite, named Starmind AI1, will carry a space-optimized version of NVIDIA's Vera Rubin NVL72 rack-scale system. The standard terrestrial NVL72 combines 72 Rubin GPUs and 36 Vera CPUs, although SpaceX and NVIDIA have not disclosed the final configuration of the orbital version. Space Exploration Technologies Corp. (NASDAQ:SPCX) plans to launch the satellite in the fourth quarter of 2027 and reach substantial scale by 2028. Musk's plan isn't new; during SpaceX's first earnings conference as a public company in August, he stated that the company would build exclusively on NVIDIA hardware in the future, calling the Vera Rubin architecture the best available AI computer design.
Betting That Space Is Cheaper Than Earth
Musk's central point is that space is, in the long run, the most cost-effective area to develop AI computing. He cites solar power availability in orbit as a crucial advantage, and estimates that within two to three years, space might become the lowest-cost place for AI computing in general, describing the orbital architecture as simpler, less expensive, denser, and lighter than a standard data-center rack. Not everyone believes the physics and economics will align on Musk's timeframe. Microsoft President Brad Smith has publicly questioned the broader concept, telling reporters that he would be surprised if companies actually transferred computation from land to low-Earth orbit.
For NVIDIA Corporation (NASDAQ:NVDA), the read-through is simple: space-based computing would represent a new, if early-stage and speculative, source of demand for its Vera Rubin platform, on top of the company's strong position in terrestrial AI infrastructure. According to some analyst models, SpaceX accounts for approximately 5% of NVIDIA's revenue.
SpaceX's reasoning is more convoluted. The plan is entirely dependent on the success of Starship, SpaceX's next-generation rocket system, which still needs to demonstrate its capacity to handle launch frequency and reliability on the scale Musk describes. When Musk said during SpaceX's August earnings call that the company would build its future AI infrastructure exclusively on NVIDIA, NVDA shares rose more than 4%, while SpaceX's shares fell more than 10% before paring losses, reflecting investor concerns about execution risk and capital intensity, despite the fact that the NVIDIA relationship was well received.
Hedge fund ownership data for Space Exploration Technologies Corp. (NASDAQ:SPCX) is limited in terms of movement due to its new public listing, with 119 funds having stakes as of the second quarter. NVIDIA Corporation (NASDAQ:NVDA) saw hedge fund holdings increase from 275 in the first quarter to 285 in the second, confirming its standing as one of the most widely held companies among institutional investors, even though this particular orbital-compute plan remains a modest, speculative portion of the company's overall growth story.
NVIDIA's involvement adds technical substance to Musk's orbital-computing proposal, as it reflects a hardware and engineering relationship rather than merely a stated vision. SpaceX's existing compute-rental agreements with Anthropic and Google demonstrate demand for its broader AI infrastructure business, and SpaceX's underlying rocket business, particularly Starship's reusability, could provide it with a cost structure that competitors would struggle to replicate if the launch cadence occurs as planned.
That said, Musk has a well-documented history of missing ambitious deadlines, and this project relies on Starship achieving a level of launch reliability and cadence that it has not yet achieved. Physical issues such as heat dissipation, radiation, and satellite servicing in orbit remain largely unresolved, and skeptics like Microsoft's Brad Smith have called into question the fundamental premise that computational economics favor space over Earth-based data centers at all.
This announcement is best interpreted as a reaffirmation of an already-known goal rather than fresh information, but the timeframe compression indicates Musk feels real pressure (or confidence) to deliver ahead of schedule. Investors in NVIDIA Corporation (NASDAQ:NVDA) should view this as a mild, long-term demand tailwind that doesn't significantly impact the near-term investment thesis. Investors in Space Exploration Technologies Corp. (NASDAQ:SPCX) should keep a careful eye on Starship's launch cadence and reliability indicators in the coming year, since that, more than Musk's stated confidence level, will determine whether the fourth-quarter 2027 target is achievable.
While we acknowledge the potential of SPCX as an investment, we believe certain AI stocks offer greater upside potential and carry less downside risk. If you're looking for an extremely undervalued AI stock that also stands to benefit significantly from Trump-era tariffs and the onshoring trend, see our free report on the best short-term AI stock .

### Article 403 · 2026-09-20 · moomoo.com
NVIDIA-backed "British Oracle" Races for U.S. IPO with $35 Billion Valuation Target

① British AI cloud service provider Nscale has filed an S-1 registration statement with the U.S. SEC , planning to list on the New York Stock Exchange and seeking a valuation of up to $35 billion; ② Nscale was spun off from a cryptocurrency mining company in 2024. NVIDIA is its GPU supplier, customer, and investor, having invested over $2 billion and signed a $1.2 billion capacity lease agreement.
Cailian Press, September 20 (Editor: Zhao Hao) — Nscale, a UK-based AI cloud service provider backed by NVIDIA, has filed for an IPO in the United States.
On Friday, September 18, Nscale announced on its official website that it has filed an S‑1 registration statement with the U.S. Securities and Exchange Commission (SEC) in preparation for an IPO; the number of shares to be issued and the price range have not yet been determined.
Nscale stated that the company has applied to list its common shares on the New York Stock Exchange under the ticker symbol "NSCL," with Goldman Sachs, JPMorgan, and Morgan Stanley serving as the joint book-running managers for the proposed offering.
Sources familiar with the matter reveal that Nscale plans to seek a valuation of up to $35 billion through an IPO. Notably, the company was spun off from a cryptocurrency mining group just two years ago.
Nscale employs approximately 450 people at its UK headquarters. Sources familiar with the matter reveal that, as part of its IPO plans, Nscale will also launch a retail subscription offering for UK investors through its investment platform, RetailBook.
Analysts believe that this potential IPO is a bet on the market's sustained enthusiasm for AI infrastructure, even as calls to slow the pace of AI development continue to grow louder.
In March this year, Nscale raised $2 billion at a valuation of $14.6 billion, with participation from NVIDIA, Dell, Nokia, and others. According to data from deal-tracking firm Dealroom, Nscale has so far secured $3.7 billion in equity financing and over $5 billion in debt financing.
"English version of Oracle"
Nscale was spun off in 2024 from Arkon Energy, an Australian renewable-energy infrastructure company whose business is mining Bitcoin using renewable electricity. Since then, Nscale has quickly become one of the best-funded data center operators in Europe.
Last September, Trump visited the United Kingdom, and the UK and the US announced the signing of the "Tech Prosperity Agreement." Under this agreement, Nscale will collaborate with NVIDIA and OpenAI to build a UK‑version "Stargate" project; Nscale has also established a partnership with Microsoft to construct the UK's largest AI supercomputer in Loughton.
"The Star Gate" is a U.S. artificial intelligence infrastructure joint venture announced at the White House early last year by OpenAI's Altman, SoftBank's Masayoshi Son, and Oracle's Ellison; at the time, the three companies planned to invest $500 billion in the project over four years.
Positioned as the Oracle to the U.S. version of "Stargate," Nscale assumes the role of Oracle in the British edition. According to the press release, Nscale will significantly expand its production capacity planned for "Stargate UK."
At the time, NVIDIA CEO Jensen Huang announced in London that he would invest £500 million in Nscale to accelerate the deployment of a plan to deploy up to 300,000 GPUs. Jensen Huang also stated, "We believe Nscale can become the national champion of AI infrastructure in the UK."
Nscale also highlighted in its recently released prospectus the company's deep partnership with NVIDIA—NVIDIA is both its GPU supplier and a customer, as well as a source of financial support.
NVIDIA has signed a $1.2 billion capacity lease agreement with Nscale and has invested over $2 billion in Nscale. In addition, NVIDIA has provided a guarantee for Nscale's $860 million lease obligation at a facility in Texas.
Nscale stated that, as of the end of August this year, its in-house data centers hosted 7 megawatts of active computing capacity, while an additional 48 megawatts were operating in leased data center space, under contracts totaling $2.6 billion. Furthermore, 1.3 gigawatts of capacity is currently being prepared.
The AI infrastructure sector, where opportunities and risks coexist.
As demand for AI infrastructure remains robust, emerging cloud service providers such as CoreWeave, Crusoe, and Nebius have also experienced rapid growth.
Last month, Nscale signed a landmark agreement with Anthropic to lease capacity at its flagship data center in West Virginia. The six-year deal is valued at up to $45 billion.
Nscale estimates that this data center, currently under construction, is expected to begin phased commissioning by the end of next year, with a total cost of approximately US$70 billion, including a 2 GW natural-gas-fired power plant to support its operations.
However, over the weekend, Anthropic CEO Dario Amodei called on the entire industry to slow down the pace of AI development. Subsequently, Sam Altman of OpenAI and Elon Musk also voiced their support.
These calls triggered a sell-off in AI‑infrastructure and semiconductor stocks earlier this week, as markets worried that major tech firms might scale back capital spending on data centers. Just on Wednesday, nuclear‑energy company Holtec International withdrew its planned IPO.

### Article 404 · 2026-09-20 · videocardz.com
DGX Spark prices are already climbing before RTX Spark mini PCs launch

DGX Spark now costs at least $4999
DGX Spark pricing in the US is moving above NVIDIA’s own listed price just weeks before RTX Spark systems reach the market. NVIDIA still shows the DGX Spark Founders Edition at $4,699 , but the system is out of stock on its marketplace. The cheapest unit we found actually available is currently $4,999.99 on Amazon , sold by Micro Center and shipped by Amazon.
Available systems already cost 25% more than launch MSRP
That means buyers looking for an available DGX Spark are already paying around $300 more than NVIDIA’s listed price. It is also a long way from the original $3,999 price announced for DGX Spark.
ASUS Ascent GX10 listing that had temporarily climbed to $8,299 for the 1TB version and $9,499 for the 2TB model, around 50% above prices shown a month earlier. Those prices have since dropped, with the ASUS system now available on Amazon for around $6,000.
DGX spark pice doubled in month!
damn…. pic.twitter.com/MtDVEPa7E1
— soul (@Soul0Engineer) September 15, 2026
The timing comes just before NVIDIA launches RTX Spark PCs with Windows 11. NVIDIA says compact desktops and laptops will begin shipping in October with Grace CPUs, Blackwell RTX graphics and up to 128GB of unified LPDDR5X memory . The desktop RTX Spark N1X specification includes a 20-core Grace CPU and 6,144-core Blackwell RTX GPU, while a lower configuration supports up to 64GB of memory.
NVIDIA has not announced RTX Spark retail pricing yet. However, the closest existing Grace Blackwell systems are already selling above NVIDIA’s own listed DGX Spark price, while temporary retailer increases have gone much higher. With RTX Spark using the same type of large unified memory configuration, its launch pricing will be worth watching when the first Windows mini PCs arrive next month.
The main unanswered question is whether NVIDIA will eventually allow DGX Spark to run Windows and RTX Spark to run Linux, or whether operating system support will remain one of the key differences between the two platforms. NVIDIA currently lists DGX Spark with DGX OS, an Ubuntu-based Linux distribution , while RTX Spark officially supports Windows 11 . NVIDIA has not announced official cross-platform support for either system.
The compact workstation market is also getting more crowded. AMD recently launched its Ryzen AI Halo Developer Platform with the Ryzen AI Max+ 395, 128GB of unified LPDDR5X memory and official support for both Windows 11 and Linux. Apple already competes in this segment with Mac Studio , which offers up to 128GB with M4 Max and much more with M3 Ultra.
Intel has current Core Ultra processors with integrated graphics and support for large memory capacities, but it does not currently offer a direct equivalent to DGX Spark or Ryzen AI Halo built around a high-end integrated GPU and 128GB unified-memory configuration.

### Article 405 · 2026-09-20 · finance.yahoo.com
Nvidia CEO Wants To Pay Workers ‘As Much As Possible,’ Calls $8B In Taxes ‘A Privilege’ Amid Samsung, SK Hynix Pay Push

Nvidia CEO Wants To Pay Workers ‘As Much As Possible,’ Calls $8B In Taxes ‘A Privilege’ Amid Samsung, SK Hynix Pay Push
Jensen Huang says the chipmaker aims to reward employees generously as its AI-driven growth generates unprecedented wealth.
Samsung and SK Hynix workers recently secured higher wages and profit-sharing terms after contentious negotiations.
Huang pushed back on AI doomsday warnings and called for American chip companies to compete globally.
Nvidia CEO Jensen Huang said he aims to pay his employees "as much as I can," while projecting that the AI chipmaker could pay about $8 billion in U.S. taxes over five years, framing both as a consequence of the company's extraordinary success.
"The fact that I can afford to pay $8 billion in taxes over five years is a privilege," Huang told CBS News on Saturday. "Instead of paying people as little as possible to get their work, I try to pay people as much as possible."
Huang's comments come as chipmakers see their businesses expand multifold, fueling calls from workers for a larger share of the industry's booming profits. In South Korea, employees at Nvidia's key memory suppliers Samsung Electronics and SK Hynix recently secured richer compensation packages after contentious labor negotiations.
At Samsung, workers approved a deal in May that averted an 18-day strike. The agreement included an average 6.2% wage increase and a new semiconductor performance bonus worth 10.5% of business performance earnings.
SK Hynix workers also pushed back against an initial agreement in August. After further negotiations, the union approved a revised deal last week that increased the cash portion of profit-sharing bonuses to 50% from 40%, while retaining a 6.3% wage increase.
Huang Pushes Back On AI Doomsday Warnings
In the CBS interview, Huang also dismissed predictions that AI could cause catastrophic harm by the end of the decade, calling such claims "doomsday narratives."
"2030 is not going to be the end of the world," he said, arguing that such warnings are "not grounded in science."
He also opposed additional AI-specific regulations, saying existing laws covering cybersecurity, product liability, and unauthorized access should be applied first.
On China, Huang said American technology should benefit the U.S. first but argued that chip companies should ultimately compete globally. "Every single chip company should go and serve the world," he said.
On Stocktwits, retail sentiment for NVDA remained 'bearish,' unchanged over the past two weeks, with traders looking ahead to the bilateral talks during Chinese President Xi Jinping's visit later this week for trading cues.
"$NVDA I think we will have some good news by Wednesday that will really push this higher," a trader wrote . "This doom and gloom over AI is crazy. Xi and Trump meeting will help calm markets immensely. Truth is both have an interest in growing their economies, especially Trump with all the other stuff going on."

### Article 406 · 2026-09-20 · investinglive.com
Nvidia CEO Huang rejects AI doomsday fears, says 0% chance of world ending by 2030

Nvidia CEO Huang rejects AI doomsday fears, says 0% chance of world ending by 2030
Nvidia CEO Jensen Huang told CBS News there is a 0% chance AI ends the world by 2030, renewing his pushback on doomsday fears. He said the industry should not slow down but must never ship unsafe products, and has argued against new regulation.
For markets these comments are sentiment rather than a data point. Nvidia sits at the center of the AI trade, and regulation is the channel through which safety concerns could most plausibly reach earnings and valuations. Huang leads the biggest supplier of AI processors and so has an obvious commercial interest in his stance, which investors will weigh accordingly. Unease voiced from inside the industry is more likely to move sentiment than near-term chip demand, so the AI trade probably responds more to spending, earnings and policy headlines than to the safety debate itself.
Huang has put a firm 0% on AI ending the world by 2030, arguing the industry should keep moving fast and ship only safe products, even as an Anthropic resignation stokes fresh unease.
Summary:
Nvidia CEO Jensen Huang told CBS News' Jo Ling Kent that AI does not pose an extinction risk to humanity, putting the chance of it ending the world by 2030 at 0%.
He has repeated the stance at several events in recent days, arguing that AI can be safely managed and that new regulations are not needed.
The comments follow a wave of unease sparked by the resignation earlier this month of Anthropic employee Jacob Coxon, who warned that AI researchers earnestly believe it could kill us all by the end of the decade.
Huang said the industry should not slow down, but that products should never be shipped before they are ready or delivered if they are unsafe.
Nvidia is the leading provider of AI processors. The full interview was slated to air on CBS Sunday Morning on September 20.
Nvidia Corp. Chief Executive Officer Jensen Huang has renewed his pushback against AI doomsday scenarios, telling CBS News there is a 0% chance that artificial intelligence ends the world by 2030. He said the technology does not pose an extinction risk to humanity, and told CBS News' Jo Ling Kent that he completely disagrees with the idea that AI will destroy the world by the end of the decade. The interview was slated to air in full on CBS Sunday Morning on September 20, and CBS's headline said Huang agrees with President Donald Trump on AI.
Huang has made similar arguments at multiple events in recent days, maintaining that AI can be safely managed. He has also argued that new regulations are not needed. His company is the leading provider of AI processors, which makes his views on the technology's risks, and on how it should be regulated, commercially relevant as well as personal.
The comments come after a wave of unease set off earlier this month by the resignation of Anthropic employee Jacob Coxon. Coxon warned that the researchers building AI earnestly believe it could kill us all by the end of the decade. The two positions are stated views rather than measurable forecasts, and neither can be tested against data today.
On the industry's pace, Huang said in the CBS interview that it should not slow down and should move as fast as it can, regardless of what others do. He drew a line at safety, saying companies should never ship products before they are ready and should never deliver products that are unsafe.
For investors, the debate matters mainly through regulation. The argument that AI can be managed without new rules is one side of a policy discussion that could affect how quickly companies can build and sell AI systems, and public concern of the kind raised by Coxon's warning tends to add to political pressure.

### Article 407 · 2026-09-20 · nypost.com
There’s a ‘0% chance’ AI will end the world by 2030, Nvidia CEO Jensen Huang assures

There's a '0% chance' AI will end the world by 2030, Nvidia CEO Jensen Huang assures
There’s a ‘0% chance’ AI will end the world by 2030, Nvidia CEO Jensen Huang assures
By Zoe Hussain
Nvidia CEO Jensen Huang has dismissed dire warnings that artificial intelligence could soon lead to humanity’s extinction — calling such predictions overblown “doomsday narratives.”
“2030 is not going to be the end of the world. There is 0% chance that’s going to be the end of the world,” Huang told CBS News correspondent Jo Ling Kent in an interview airing Sunday .
“Scaring people is unnecessary. It is irresponsible.”
The billionaire tech executive’s comments come amid a heated debate in Silicon Valley over whether companies should second-guess the rapid development of AI — and whether the technology poses an existential threat.
The conversation was sparked in part by former Anthropic researcher Jacob Coxon, who wrote a series of viral X posts warning that top AI developers “earnestly believe that it could kill us all by the end of the decade.”
“I spent the last three years doing pretraining research at both OpenAI and Anthropic. Neither company is acting responsibly. They are racing straight to self-improving superintelligence and gambling with our lives,” Coxon wrote in the post, generating over 800,000 likes.
Coxon’s comments fueled calls from Anthropic CEO Dario Amodei, OpenAI CEO Sam Altman, and other tech leaders to slow AI development.
Huang dismissed the end-of-times predictions as “not grounded in science.”
Nvidia has a major stake in the AI debate, even before the industry’s initial boom, by supplying chips to OpenAI, Anthropic, and almost all other companies to train their models.
Their specialized chips, which provide the computing power behind high-demand machine learning models, have launched Nvidia’s market value into orbit. At $5.3 trillion, it’s the most valuable public company in the world.
Despite its vested business interests, Huang said Nvidia has reasons to want AI deployed safely and responsibly.
“Our company’s success is directly connected to the safe deployment of products and services,” Huang said. “If we don’t continue to do that, our value would be diminished.”
The Nvidia exec added that existing US laws on product liability and unauthorized entry are sufficient, agreeing with President Trump that the industry doesn’t need more guardrails.
“You have all kinds of liabilities associated with cybersecurity and damage liability laws,” Huang said. “Apply that first — don’t let this doomsday narrative allow someone to relieve them of the laws that currently exist.”

### Article 408 · 2026-09-20 · fool.com
Nvidia Stock Hasn't Set a Record in 4 Months. History Says These Stalls Have Ended 2 Ways.

Nvidia ( NVDA +2.55% ) hasn't closed at a record high since May 14, when the stock finished at $235.74. That was 87 trading days ago, about four months. Shares now sit near $215 as of this writing, about 9% below that mark.
Droughts like this aren't new for the artificial intelligence (AI) chip giant, though. Since reclaiming its 2007 peak in 2016, Nvidia's stock has gone 60 or more trading days without a record close seven times.
Five of those stretches ended at new highs within about six months. The other two turned into bear markets that cut the stock by more than half.
Four of the seven droughts lasted at least as long as the current one has. Two of them ended with the stock at fresh records: a 115-day stretch that ended in June 2025 and a 120-day stretch that ended this past April.
The other two kept going -- and the stock took a beating both times. After peaking in October 2018, Nvidia went 344 trading days without another record close, falling 56% along the way before finally recovering in February 2020. The stretch that began in November 2021 ran 373 trading days, with the stock down 66% at the low, before a new record arrived in May 2023.
In other words, the record has no middle ground. Every drought that resolved quickly was over within about 120 trading days, and the only two that ran longer became bear markets. Today's stall would pass the 120-day mark in early November.
What separated them?
The difference, I'd argue, showed up in Nvidia's revenue , not on its price chart.
The 2018 drought began as the fallout from a cryptocurrency bust reached Nvidia's results. Demand from miners had collapsed, and unsold inventory piled up at the distributors and card makers that sell its products.
"Our near-term results reflect excess channel inventory post the crypto-currency boom, which will be corrected," CEO Jensen Huang said in Nvidia's November 2018 earnings release.
But the slump didn't stop at the channel. In late January 2019, Nvidia cut its quarterly revenue guidance to $2.20 billion from $2.70 billion, blaming weak demand for gaming chips in China, among other problems. And sales for the full fiscal year that followed fell 7% to $10.92 billion.
The 2021 drought had the same shape. Gaming revenue fell 27% in fiscal 2023 (a year that ended in late January 2023), and Nvidia's total revenue came in flat at $27.0 billion, with sales in the fiscal fourth quarter down 21% from a year earlier.
Sales kept climbing straight through the quick droughts. The most recent stall, which started in late October 2025, was more than halfway done when Nvidia reported quarterly revenue up 73% year over year in late February. Two months later, the stock was back at a record.
Capturing how different today's backdrop is, Nvidia grew revenue 106% year over year in the second quarter of fiscal 2027 (a period that ended July 26), reaching $96.2 billion. Data center revenue climbed 117% to $89.0 billion. And net income more than doubled, rising 126% year over year to $59.7 billion. Growth is speeding up, too. The company's year-over-year revenue growth rate has now accelerated for four straight quarters, moving from 62% last fall to 73%, then 85%, and now 106%.
And management expects the growth to continue. On Nvidia's late-August earnings call, chief financial officer Colette Kress told analysts the company expects revenue to grow about 70% in fiscal 2028. She called that a supply constrained outlook, meaning the ceiling is how many chips the company can produce.
The price, against numbers like those, doesn't look demanding. Shares cost about 27 times earnings -- and about 14 times expected fiscal 2028 earnings, a price that seems to assume the big growth mostly ends after next year.
Which ending should investors expect this time? Both of Nvidia's long, painful droughts overlapped falling sales.
With revenue accelerating and next fiscal year's ceiling set by supply, today, I think, looks a lot more like the stalls the stock grew its way out of. The stock, in my opinion, remains a buy at this level.
Of course, neither bust was forecast ahead of time. Nvidia set its October 2018 record just weeks before the crypto warning, and the gaming slump followed within months of the November 2021 peak. Demand for AI computing could turn just as fast. But that turn would show up where the last two did -- in the company's reported sales. And a four-month wait for a record isn't evidence of it.
The chip giant's droughts between record closes have ended at new highs within about six months -- or in bear markets that cut the stock by more than half.
By Daniel Sparks – Sep 20, 2026 at 5:08AM EST
Since 2016, seven droughts of 60 or more trading days either ended at new highs by about day 120 or stretched into multiyear bear markets.

### Article 409 · 2026-09-20 · finance.yahoo.com
3 AI Hardware Stocks Linked To Nvidia And US China Trade Talks

AI hardware went from tech niche to geopolitical bargaining chip almost overnight, as Nvidia CEO Jensen Huang now shapes how President Trump talks about regulation, export fees, and China trade. That power shift creates real ripple effects for companies exposed to these talks. Read on to see how three US listed hardware stocks tied to AI chips and datacenter gear are plugged into this story, and why those links could matter for your portfolio.
The stocks covered below are just a small slice of the picture, and the full screen surfaced another 55 companies with equally compelling AI hardware trade stories that are not discussed in this article. To go straight to the source and identify, filter, and analyze the highest conviction US China AI hardware trade beneficiaries, head into the US-China AI Hardware Trade Beneficiaries screener .
Monolithic Power Systems (MPWR)
Overview: Monolithic Power Systems designs power management chips that feed AI servers and data centers, with heavy exposure to China based hardware demand.
Operations: The business generates about US$3.3b from semiconductors, with meaningful sales tied to China, Taiwan, South Korea and US customers.
Market Cap: US$59.8b
Monolithic Power Systems matters in this US China AI hardware story because its power chips sit inside the very servers Nvidia is fighting to keep shipping, so any breathing room on export rules can ripple straight into demand for its components.
"Investor optimism appears anchored in MPS's exposure to accelerating AI adoption in data centers (including design wins with major ASIC based AI platforms and anticipated industry wide server transitions to 48V/800V architectures), which could drive sustained revenue outperformance, even as end market growth normalizes and competition increases."
What happens to that optimism if a single unseen pressure on future profitability breaks the market's comfort with current expectations.
If that unseen pressure is on your mind, read the full narrative for Monolithic Power Systems to see whether Monolithic Power Systems' AI upside still outweighs the risk.
Marvell Technology (MRVL)
Overview: Marvell Technology builds custom chips and high-speed connectivity hardware that help power AI data centers and cloud infrastructure worldwide.
Operations: The business generates about US$9.5b from integrated circuits, with around US$3.9b tied to China and further exposure across Asia and the United States.
Market Cap: US$214.2b
Marvell Technology sits right in the plumbing of the US China AI hardware story, supplying custom silicon and networking gear that helps Nvidia class accelerators talk to each other inside hyperscale data centers.
"NVIDIA's $2B equity investment (March 31, 2026) into Marvell via NVLink Fusion is not a component deal; it is an ecosystem architecture deal. NVIDIA is financially aligned with Marvell's success."
What happens to that alignment if one unseen pressure shifts how hyperscalers allocate future AI infrastructure budgets?
If that question is on your mind, read the full narrative for Marvell Technology to learn how Marvell Technology's Nvidia tie up could amplify or dilute its AI leverage over time.
Overview: Advanced Micro Devices supplies AI accelerators, GPUs and CPUs that power data center compute and AI workloads for global cloud and enterprise customers.
Operations: Advanced Micro Devices generates about US$22.2b from Data Center, US$11.8b from Client, and roughly US$3.6b each from Gaming and Embedded segments.
For the US China AI hardware story, Advanced Micro Devices matters because its AI GPUs and EPYC server processors give hyperscalers a credible alternative source of compute capacity that is still tightly tied to US export policy.
"Market optimism around AMD's AI accelerator and data center CPU ramp (for example, MI350/355 and EPYC Turin) may be overshooting near-term reality, given that hyperscaler and government/sovereign demand visibility and regulatory approvals are still developing and can introduce execution risk, potentially leading to overestimated future revenues."
What happens to those rich expectations if a single unresolved policy decision shifts how quickly customers can actually deploy AMD powered AI racks?
That policy overhang is exactly why reading the full narrative for Advanced Micro Devices can help you see where Advanced Micro Devices might still surprise on AI execution and market share.
Markets move fast, stories age quickly, and the most interesting breakout ideas rarely stay under the radar for long. Check these fresh lists before momentum gets fully priced in and act now.
Target resilient cash generators before the crowd notices by scanning the 35 high quality undervalued stocks that still pair solid balance sheets with meaningful free cash flow.
Ride the next wave of automation by filtering through the 95 robotics and automation stocks quietly building momentum as factories, warehouses, and services lean harder into machines.
Position ahead of potential rate and inflation shifts by reviewing the 7 dividend fortresses that aim to keep income streams flying while others are still searching.

### Article 410 · 2026-09-20 · fool.com
Jensen Huang Just Announced Fantastic News for Nvidia Shareholders

Nvidia ( NVDA +2.55% ) has turned its graphics processing unit (GPU) expertise into an artificial intelligence (AI) empire. These powerful chips, once mainly used in the gaming industry, became a key tool for AI in recent years. And Nvidia has built on this by expanding its offerings into a full suite of AI products and services, such as networking tools and AI platforms tailored to specific industries.
All of this has led to incredible growth for the tech giant, with earnings soaring to record levels. In the latest quarter, for example, revenue climbed more than 100% to about $96 billion. And profit also surged in the triple digits to $59 billion. Meanwhile, the stock has been a top performer over time for investors, advancing about 900% over the past five years.
But investors have worried about how far this AI boom can go. They've questioned the extraordinary levels of capital spending by tech companies to support the infrastructure build-out, with the concern being that the revenue opportunity may fall short. This worry has weighed on Nvidia stock on occasion, even pushing it to a decline in the first quarter of this year.
However, last week, a new clue about the future emerged: Nvidia chief Jensen Huang just announced fantastic news for shareholders.
Before we dive into the latest, though, let's take a quick look at Nvidia's path so far in AI, a market on track to reach into the trillions of dollars by the end of the decade. Nvidia recognized the promise of AI early and saw that the GPU could play a critical role. This was about 10 years ago, and Nvidia decided to go all in on this industry and focus the design of its GPUs on AI.
It was a successful bet, as we can see through Nvidia's earnings growth in recent years.
And the fact that Nvidia entered the market early allowed it to develop key relationships with customers and build a solid reputation. The company's pledge to update GPUs on an annual basis has been another element that's supported its leadership in this market.
All of this has clearly been very positive, and this momentum could continue. Nvidia and AI peers have spoken of ongoing high demand for their goods and services. It's important to note that real-world use of AI is just beginning, signaling more earnings growth for these players down the road.
Still, some investors aren't convinced -- and that's weighed on AI stocks, including Nvidia, holding them back from major gains this year.
With all of this in mind, let's consider Jensen Huang 's fantastic news for shareholders. Huang, speaking at a summit in Scotland, told members of the press that Nvidia would double the number of chips sold next year. That's compared with this year.
"The reason for that is because AI has, has so much contribution to the benefits of different industries, different economies, and you can see that in almost every single country that we're in, people want to invest in AI," Huang said, according to CNBC.
This follows the company's first-ever forecast for the full year to come: During Nvidia's recent earnings report, citing increased visibility, the tech giant predicted a 70% year-over-year gain in revenue in the next fiscal year.
Of course, among investors and the general public, concerns about the tech build-out may persist. But Huang's comments further reinforce the case that Nvidia's AI revenue growth opportunity is far from over -- and the company may actually be entering a fresh wave of growth as AI is more actively applied by companies, individuals, and governments.
This should offer Nvidia shareholders and potential investors a certain level of comfort. Even if the stock doesn't take off immediately, future business prospects remain bright, and this should translate into further gains for the stock over time. So these latest words from Huang represent fantastic news for anyone who owns Nvidia stock or who aims to get in on this top AI player.
By Adria Cimino – Sep 20, 2026 at 12:10PM EST
