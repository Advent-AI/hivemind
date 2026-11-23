# Blind reader, matter census batch 8 of 11: which big questions do these articles raise? (read-only)

You are a senior hedge-fund analyst covering NVIDIA. Read ONLY the material below: 40 articles (numbers 253 to 292,
2026-09-16 to 2026-09-17, in publication order) and the signed standard's §3 (the opening reasons and "问题怎么写") and §4 (the opening
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

### Article 253 · 2026-09-16 · finance.yahoo.com
Nokia Jumps 6% as AI-RAN Trials Expand Across Eight Operators; NVIDIA and Ericsson Tread Water

Nokia stock surged 6% to $10.39 after its AI-RAN platform advanced to live field trials with eight global operators, delivering 20%+ spectral efficiency gains.
Ericsson's near-flat 0.7% move signals markets aren't pricing AI-RAN as a category-wide event, keeping today's rally a Nokia-specific story.
Nokia ( NYSE:NOK ) stock is rising in early Wednesday trading, up 6% to $10.39 after the company said its artificial intelligence-powered radio access network (AI-RAN) platform is moving from evaluation to live field trials at eight global operators. The list spans North America, Europe, Asia-Pacific and the Middle East, and it reframes AI-RAN as a shared industry priority rather than a single-vendor pilot. That geographic reach is what today's move is paying up for.
The move is Nokia-specific. The iShares U.S. Technology ETF ( NYSEARCA:IYW ) is unchanged at $250.08, and the SPDR S&P 500 ETF Trust ( NYSEARCA:SPY ) is up 0.4% to $760.33. Nokia stock is climbing while U.S. technology sits still and the broad benchmark is only marginally higher, which frames today as a name-specific catalyst.
Peer positioning tightens the read. Ericsson ( NASDAQ:ERIC ) stock is up 0.7% to $10.11, and NVIDIA ( NASDAQ:NVDA ) stock is up 0.9% to $214.04. Both are close to flat while Nokia leads, and that divergence gives the announcement its shape as a Nokia story.
Nokia announced growing global momentum for its AI-RAN business, with operators moving from early evaluation into lab and live field trials. The company named eight operators advancing proofs of concept and trials, including A1 Group, du, e&, Mobily, stc and TPG Telecom. Nokia is presenting AI-RAN as an adoption curve rather than a launch headline.
Learn 7 Secret Wealth Tips High Net Worth Investors Use
How do you continue to grow a seven-figure portfolio in retirement? The last thing you want is to run out of money, you want your money to generate lasting income while you enjoy your life.
Learn seven strategies high net worth investors use with new report: The Seven Secrets of High Net Worth Investors from Fisher Investments. Get your guide here (sponsor)
The platform pairs Nokia's AI-native anyRAN software with NVIDIA's Aerial RAN Computer, and Nokia says it's built for 5G networks with a software upgrade path toward future generations. Nokia says the platform has already delivered improvements in spectral efficiency of more than 20%, letting operators wring more capacity from spectrum they already hold rather than funding a hardware refresh. That software-led capacity story is Nokia's commercial pitch.
The commercial argument here is straightforward for Nokia. Operators can convert existing spectrum licenses into more capacity, a resonant offer in a period when radio access budgets are tight and greenfield buildout has slowed (the same non-chipmaker AI infrastructure angle we broke down in a free report on seven suppliers powering the buildout, here). Nokia's stack promises additional headroom without the capex event of a hardware refresh.
Emma Falck, President of Mobile Infrastructure at Nokia, stated the growing ecosystem of partners across regions demonstrates that AI-RAN "is becoming a shared industry priority, enabling more intelligent, efficient and software-driven networks." Ronnie Vasishta, Senior Vice President of Telecom at NVIDIA, declared AI-RAN "will transform the mobile network into one of the world's largest distributed AI infrastructures."
The gain at Nokia rests on an ecosystem announcement. Trials and proofs of concept carry no disclosed revenue, and Nokia has put no figure on what the AI-RAN pipeline is worth. What Nokia is selling here is software that pulls capacity from spectrum operators already own, a cheaper argument than the hardware cycle Nokia would otherwise be asking them to fund.
Ericsson is the peer that tests the read. Ericsson competes directly with Nokia in radio access, and a genuine industry rerating around AI-RAN would lift both names together rather than Nokia alone. Ericsson stock's 0.7% tick suggests today's news isn't yet being priced as a category-wide event.
NVIDIA sits on the supply side of the same announcement through its Aerial RAN Computer contribution. A nearly flat NVIDIA against a sharply higher Nokia signals today's news is more material to Nokia's positioning than to NVIDIA's scale. NVIDIA's market capitalization is measured in trillions, so AI-RAN attaches to a small slice of its revenue base.
The pattern here has logic. AI-RAN is a rerating catalyst for Nokia's software mix, and for NVIDIA it's another workload attached to a compute platform already priced for AI at scale. Ericsson's near-flat move would likely flip if a second RAN vendor announced a comparable pipeline of trials.
Separately, Nokia said Nokia Defense signed a memorandum of understanding with C3IA, a UK systems engineering and security services company, to support digital transformation across UK defense operations. The two plan to co-develop capabilities in tactical and operational communications, private mobile networks, command and control, sensing, autonomous systems and edge computing. Both companies participate in the UK Ministry of Defence's TacSys framework.
As background info rather than a same-day driver, Reuters reported earlier this month that Nokia is set to rejoin the Euro Stoxx 50 index, which brings index-tracking flows on a schedule of their own. Investors in Nokia stock can watch for whether today's operator list converts into disclosed commercial commitments in coming quarters, since that is the step that turns AI-RAN from a positioning story into a revenue line. The company's next earnings update will be the natural checkpoint for that translation, and investors should size their exposure to reflect that pipeline conversion still needs to happen.

### Article 254 · 2026-09-16 · finance.yahoo.com
Think Nvidia Is Overpriced? The Irony Keeps Me Buying Again and Again

NVDA's forward P/E of 24 and PEG ratio of 0.46 reveal a GARP stock hiding inside a $5 trillion market cap.
AMD and AVGO can't match NVDA's Networking segment, which alone generated $40 billion in one quarter, up 138% year over year.
Analyst EPS estimates for NVDA climbed from $12.67 to $15.57 in just 90 days, signaling earnings power is outrunning the valuation multiple.
I keep hitting the buy button on NVIDIA ( NASDAQ:NVDA ), and the louder the "it's overpriced" chorus gets, the more shares I add. That sounds reckless until you look at what the multiple is actually paying for.
Why the Expensive Label Misses the Point
At $212.17 and a $5.12 trillion market cap, NVIDIA looks like the definition of a stretched stock. The trailing P/E of 43 is the number every skeptic quotes. The one they skip is the forward P/E of 24 and a PEG ratio of 0.46. Growth at a reasonable price rarely arrives in mega-cap wrapping, and that mismatch is what keeps me buying. The multi-trillion dollar valuation looks intimidating at face value, yet under the hood NVIDIA behaves like a GARP stock.
Three Reasons the Numbers Keep Winning the Argument
Start with growth. Q2 FY2027 revenue landed at $96.22 billion, up 105.8% year over year, with Data Center alone at $89.02 billion, up 117%. Networking inside that segment printed $40.31 billion, up 138%. Management then guided Q3 to $108.0 billion, plus or minus 2%, and told analysts on the call to expect roughly 70% revenue growth in fiscal 2028. That is a company still accelerating at a scale most large caps stopped attempting a decade ago.
Quality of earnings is the second pull. Non-GAAP gross margin ran 75.0%, return on equity is 101.49%, and return on invested capital is 92.21%. Debt-to-equity sits at 0.073 with interest coverage of 503.4x. Fortress balance sheet, operator-level margins.
Third, capital return shows up. Q2 free cash flow was $21.34 billion, and NVIDIA returned roughly $26.0 billion to shareholders through buybacks and dividends, with about $99.0 billion remaining under the repurchase authorization. The dividend barely registers, and the buyback carries real weight.
Every time I check Advanced Micro Devices ( NASDAQ:AMD ) or Broadcom ( NASDAQ:AVGO ), I come back to the same wall. NVIDIA's Networking business by itself did $40.31 billion in a single quarter, up 138%. That is a networking company living inside an accelerator company, at a scale neither the pure GPU challenger nor the custom-silicon challenger has produced in a public quarterly earnings report. When I can own a platform earning a 75.0% non-GAAP gross margin and a 92.21% ROIC, I stop shopping for a proxy.
The scary line in the filings is $279 billion in supply commitments, most of it memory for Vera Rubin, alongside $108.5 billion in guarantee obligations tied to AI cloud partners. Add customer concentration among a handful of hyperscalers and DSO stretching from 45 to 60 days, and the shape of a demand shock becomes visible. Management calls the arrangement durable and fungible: "We recognize the scale of this support, and we know some will call this circular financing. We see it differently." I take the risk seriously. I also weigh it against top-five hyperscaler CapEx management pegged at nearly $800 billion in 2026 and $1.3 trillion in 2027. The demand pool is wider than any one customer.
Vera Rubin is shipping, and Huang says it delivers 30X higher throughput per megawatt and 35X lower token costs versus Grace Blackwell Ultra. Analyst EPS for the fiscal year ending January 2028 has climbed from 12.67 ninety days ago to 15.57 today. When earnings power keeps racing ahead of the multiple, the overpriced label starts to look like a mispricing I get to keep exploiting. That is why my next buy is already scheduled.

### Article 255 · 2026-09-16 · finance.yahoo.com
Why IREN (IREN) Is Down 6.1% After Nvidia Strikes US$5.5 Billion AI Cloud Deal With Miner

Recently, JPMorgan analyst Richard Choe issued a rare double-upgrade on IREN after the company signed a roughly US$5.50 billion, five-year partnership with Nvidia tied to its fast-growing AI cloud services platform.
This shift, alongside IREN's decision to wind down Bitcoin mining and expand vertically integrated AI infrastructure, marks a material redefinition of its core business model.
Next, we'll examine how the Nvidia partnership and AI cloud transition reshape IREN's investment narrative and future growth assumptions.
AI is about to change healthcare. These 39 stocks are working on everything from early diagnostics to drug discovery . The best part - they are all under $10b in market cap - there's still time to get in early.
To own IREN today, you have to believe it can successfully complete its shift from Bitcoin mining to an AI-first, vertically integrated cloud platform while managing heavy upfront spending and ongoing losses. The Nvidia partnership and JPMorgan's double-upgrade sharpen that story by reinforcing the AI thesis, but they do not remove the near term pressure from sizeable capex, financing needs, and execution risk around large contracted projects.
Among recent announcements, the US$3.65 billion GPU financing facility stands out alongside the Nvidia deal. It underpins IREN's goal of scaling to 480MW of AI Cloud capacity by the end of 2026, and ties directly into the same theme as the Nvidia partnership: aggressive, contract-backed expansion. Together, they frame both the key upside catalyst in AI infrastructure growth and the core risk that capital commitments could outrun cash generation if conditions turn less supportive.
Yet behind the AI growth story, investors should also be aware that IREN's large, fixed capital commitments could become a real problem if demand or financing conditions...
Read the full narrative on IREN (it's free!)
IREN's narrative projects $8.7 billion revenue and $504.8 million earnings by 2029.
Uncover how IREN's forecasts yield a $80.93 fair value , a 90% upside to its current price.
Before this news, the most optimistic analysts were already assuming IREN could reach about US$14.7 billion in revenue by 2029, which is a far more bullish view than the baseline catalyst of simply scaling AI cloud contracts. Those same analysts were counting on around US$1.3 billion in earnings, so this kind of scenario reflects a much more optimistic narrative that may shift again as the Nvidia-linked developments are fully reflected.
A great starting point for your IREN research is our analysis highlighting 1 key reward and 4 important warning signs that could impact your investment decision.
Our free IREN research report provides a comprehensive fundamental analysis summarized in a single visual - the Snowflake - making it easy to evaluate IREN's overall financial health at a glance.
The future of work is here. Discover the 38 top robotics and automation stocks leading the charge in AI-driven automation and industrial transformation.

### Article 256 · 2026-09-16 · fool.com
What Nvidia and SK Hynix Are Signaling About Micron's Outlook

Micron Technology ( MU +4.20% ) is poised to release its fiscal 2026 fourth-quarter results on Sept. 30, and the market will be eagerly awaiting its report to understand the health of the memory industry.
After all, the strong demand and tight memory supply have been driving stunning growth in Micron's revenue and earnings in recent quarters. The rapid increase in memory prices has led to a big jump in Micron stock over the past year, and the sustainability of that rally will be put to the test when the company releases results.
However, the good news for Micron investors is that the comments from Nvidia ( NVDA +2.55% ) and SK Hynix , two key players in the artificial intelligence (AI) ecosystem, suggest that Micron's impressive growth is here to stay. Let's see why.
Nvidia and SK Hynix point toward further hikes in memory prices
When Nvidia released its fiscal 2027 second-quarter results last month, the company remarked that memory price hikes are here to stay. The semiconductor bellwether expects margin pressure due to higher component costs, especially memory. According to Nvidia CFO Colette Kress:
As you are already aware, we are experiencing extreme pricing conditions in memory. The magnitude of the price increase has exceeded our prior expectations and are headed even higher into next year.
Nvidia expects its gross margin to drop over the next couple of quarters. It expects a slight improvement in the next fiscal year, driven by higher chip prices. So, Nvidia management's comments indicate that Micron's primary catalyst -- strong memory pricing -- isn't going anywhere.
Similarly, South Korean memory giant SK Hynix expects the memory shortage to worsen next year. The company estimates that memory demand could outstrip supply beyond 2030, even as it brings more capacity online. In fact, Korean investment firm KB Securities estimates that SK Hynix is sitting on memory inventory of just 10 days.
Additionally, the aggressive jump in hyperscalers' capital spending on AI infrastructure suggests that memory demand will remain robust. Nvidia, for instance, estimates that the capex of the top five hyperscalers could increase to $1.3 trillion in 2027, up from $800 billion this year.
So, there is a strong chance Micron's quarterly numbers will exceed expectations, as the severe memory shortage is likely to send prices even higher. Moreover, the tight demand-supply environment bodes well for Micron's fiscal 2027 guidance.
Micron's valuation makes it a no-brainer buy
Micron's revenue in fiscal 2027, which has just begun, is poised to increase by 88% to $244.5 billion, according to consensus estimates. Its earnings per share, meanwhile, could jump by 112% to $156.07. However, don't be surprised to see Micron's fiscal Q1 guidance suggesting stronger growth rates due to the reasons discussed above.
Moreover, Micron is trading at just 6.6 times forward earnings. Ideally, it shouldn't be trading at such a steep discount given its phenomenal earnings growth. The S&P 500 index, for comparison, has a forward earnings multiple of 21. So, I won't be surprised to see this AI stock taking off after Sept. 30 on account of stronger-than-expected numbers and guidance, as Micron's ability to clock consistently strong growth could inflate its valuation.
By Harsh Chauhan – Sep 16, 2026 at 9:05AM EST

### Article 257 · 2026-09-16 · thenationalnews.com
Nvidia's GTC will return to Washington and a very different political climate

Nvidia announced that one of its flagship AI conferences, GTC will be returning to Washington later this year. Unlike the last time it took place in the US capital, public perception of AI has drastically soured.
Polls show increased concern in the US about the potential impact AI will have on the labour market as well as the proliferation of noisy and electricity-hogging data centres that have a negative environmental impact.
"The leather jacket returns to Washington, DC," a social media post from Nvidia read, referring to its chief executive Jensen Huang . He has described the forthcoming GTC (GPU Technology Conference) as the Super Bowl and Woodstock of AI.
Though the company’s GTC events have occasionally been held in Washington since 2016, this will be the second time such an event in the US capital will have a keynote speech delivered by Mr Huang, who delivered a keynote during GTC for the first time back in 2025.
Mr Huang, one of the world's most high-profile AI executives, has insisted that the technology's benefits will far outweigh the negatives. He has even accused other technology executives who have expressed concerns about AI as having a "God complex".
Nvidia's GTC will take place from November 30 to December 3, weeks after the US midterm elections that will decide which party controls Congress.
Amid the souring public mood, Mr Huang has made several visits to the White House over the past year to discuss AI issues and chip export controls with President Donald Trump.
This week, Mr Huang told a business and technology conference that too many people were expressing what he described as irresponsible fears about AI.
"We have to take account for all the stupid predictions made," he said, to a round of applause.
The discussion was interrupted by a phone call from Mr Trump, whom Mr Huang put on speakerphone.
Nvidia's chief executive told Mr Trump that he "wouldn't let" irrational fears cause the US to lose what the White House has often called an AI race with China.
Critics of that stance have pointed out that Mr Huang has consistently lobbied for the US to relax chip export restrictions to China, which some say could give Beijing a helping hand in the AI race.
"Sorry, but asking Jensen Huang about AI risk is like asking [Colombian drug lord] Pablo Escobar about drug policy," said X user Jay Shooster.
Meanwhile, independent Senator Bernie Sanders said on Tuesday that he would introduce legislation calling for a pause on the pursuit of AI super-intelligence until more regulatory guardrails were established. The outspoken politician has also expressed fears about the potential for AI to wipe out jobs.
Nvidia, whose incredibly powerful GPUs, CPUs and logic board designs have largely been the backbone of rapid AI development in recent years, employs about 42,000 workers. Some people have pointed out that AI have created jobs that did not previously exist.
Others have also said that the proliferation of data centres has bolstered the need for electricians, construction workers and water experts.
For all the public pushback against AI, Nvidia's revenue has skyrocketed.
"Connect with policymakers, developers, researchers and industry partners to learn how AI is helping drive the US economy" says a description on Nvidia's GTC website, which also teases Mr Huang's keynote speech on December 1.
According to Nvidia, the multi-day event will take place at the Ronald Reagan Building and International Trade Centre and venues across Washington.

### Article 258 · 2026-09-16 · ionq.com
Generative AI Accelerates Quantum Optimization | IonQ & NVIDIA

Our benchmark framework evaluates the full technical stack and provides meaningful comparisons to the people and businesses that rely on it.
IonQ, ORNL, NVIDIA, and the University of Tennessee, Knoxville Show AI Method Reduces Quantum Optimization Trade Off
An AI model directly generated quantum circuits, making accurate large-scale optimization faster and more affordable with constant runtime as problems grow
TORONTO and COLLEGE PARK, Md. — Sept. 16, 2026 — IonQ (NYSE: IONQ), the world's leading full-stack quantum platform and foundry, today detailed joint research with Oak Ridge National Laboratory (ORNL), NVIDIA, and the University of Tennessee, Knoxville (UT) showing that a trained generative model can write quantum optimization circuits directly, eliminating the trial-and-error parameter-tuning loop that has made the most accurate approach too costly to run. The paper is being presented this week at IEEE Quantum Week in Toronto.
Hybrid quantum optimization breaks a large problem into smaller pieces, solves each one, and recombines the results. Each piece needs a tailored quantum circuit, which traditionally required trial- and-error parameter tuning: run, measure, adjust, and repeat, often hundreds of times. Larger pieces can improve answers, but they also raise tuning costs, limiting the size of problems researchers could solve.
“Better answers in hybrid quantum optimization have traditionally come with a steep tuning tax. In this benchmark, generative AI replaced the iterative tuning loop, and as the quantum subproblems grew the solution quality improved,” said Dr. Martin Roetteler, IonQ’s Vice President of Quantum Applications R&D and a co-author of the paper. “Take that cost away and you can work at the size where the answer is meaningful. The result provides a potential path toward scaling hybrid quantum optimization, unlocking completely new capabilities and scales that align with IonQ’s existing and future quantum computing hardware generations.”
To teach the generative model how to tune circuit instructions, the team first showed it what strong results looked like. They ran the conventional trial-and-error method across many sampled problems, kept only the near-optimal circuits, and used those examples to train a transformer, the same class of model behind large language models but trained on circuits instead of text.
The trained model generates candidate quantum circuits directly, without the repetitive parameter-tuning loop used by conventional methods. In the reported experiments, the model sampled ten candidate circuits for each subproblem; all ten were simulated and scored, and the best-scoring candidate was used to update the global solution.
On a dense, higher-order benchmark problem with 100 decision variables, model-generated answer quality roughly doubled as subproblems grew. Under the prior state-of-the-art method, circuit-finding time rose sharply from about 34 seconds on 4 qubits to more than 11 minutes on 12 qubits. The generative approach held nearly 28 seconds for every size previously tested. Both approaches are quantum methods; the study compares circuit-generation approaches, not quantum against classical solvers.
ORNL led the study. Co-authors span ORNL's National Center for Computational Sciences and its Materials Science and Technology Division, IonQ, NVIDIA, and UT. Abhinav Rijal, a graduate researcher in the Department of Physics and Astronomy at UT is a co-author of the study.
“This work brings generative AI, quantum computing, and high-performance computing together to tackle large-scale, complex optimization problems. AI can become a new computational layer for quantum circuit synthesis, enabling the automatic design and optimization of quantum circuits for increasingly complex problems. We are now extending the framework to real-world scientific and engineering applications and scaling it across larger HPC systems to address problems of even greater scale and complexity,” said Dr. In-Saeng Suh and Dr. Seongmin Kim, National Center for Computational Sciences, ORNL.
“Drawing on accelerated computing and AI to make breakthroughs in quantum algorithms is one of the most promising ways to reach useful quantum applications as quickly as possible,” said Sam Stanwyck, Director, Quantum Product at NVIDIA. “By enabling developers to build quantum algorithms architected around AI from the outset, tools like CUDA-Q are laying the foundation for the next generation of advances in quantum computing and its useful application.”
The paper describes its results as benchmark-scale validation.
Every circuit in the study was simulated rather than executed on quantum hardware, using the NVIDIA cuQuantum SDK through the NVIDIA CUDA-Q open platform for quantum-GPU supercomputing on a single NVIDIA H200 GPU in the Oak Ridge Leadership Computing Facility’s Defiant2 system. That environment is what makes the comparison meaningful: both the trial-and-error method and the generative one ran on identical GPU-accelerated infrastructure, providing a controlled comparison of the two end-to-end workflows. The measured difference principally reflects the distributed quantum approximate optimization algorithm (DQAOA)-GPT’s replacement of iterative variational parameter optimization with generative circuit synthesis and a fixed number of candidate evaluations.
The paper is available at arXiv:2607.20225 . It is one of nine IonQ papers accepted at IEEE Quantum Week 2026, held Sept. 13–18 at the Metro Toronto Convention Centre, and the winner of a best paper award.
IonQ, Inc . [NYSE: IONQ] is the world’s leading quantum platform and foundry - delivering integrated quantum solutions across computing, networking, sensing, and security. IonQ’s newest generation of quantum computers, the Superion, is the latest in a line of cutting-edge systems. Earlier systems have helped customers and partners including Amazon Web Services, AstraZeneca, and NVIDIA achieve a 20x performance increase over previous quantum solutions and accelerate innovation in drug discovery, materials science, financial modeling, logistics, cybersecurity, and defense. In 2025, the company achieved 99.99% two-qubit gate fidelity, setting a world record in quantum computing performance .
Headquartered in College Park, Maryland, IonQ has operations across North America, Latin America, EMEA, and APAC. Our quantum computing services have been available through all major cloud providers since 2021, while we also meet the needs of networking and sensing customers across land, sea, air, and space. IonQ is making quantum platforms more accessible and impactful than ever before. Learn more at IonQ.com .
UT-Battelle manages ORNL for DOE’s Office of Science, the single largest supporter of basic research in the physical sciences in the United States. DOE’s Office of Science is working to address some of the most pressing challenges of our time. For more information, visit energy.gov/science .
The University of Tennessee, Knoxville, is Tennessee's flagship land-grant university and is home to more than 40,000 students across 14 degree-granting colleges and schools. UT holds the highest Carnegie classification for research activity and maintains deep partnerships with industry and the U.S. Department of Energy's Oak Ridge National Laboratory. The university is expanding research and education in quantum science and technology through collaborations spanning quantum computing, networking, sensing and materials.
Note to Investors Regarding Forward-Looking Statements
IonQ Media contacts:
IonQ Investor Contact:
ORNL Media Contact:
UT Media Contact:

### Article 259 · 2026-09-16 · barchart.com
Why It’s Time to Load Up on Nvidia Stock

Nvidia (NVDA) has been powering the ongoing artificial intelligence (AI) boom. Its graphics processing units (GPUs), central processing units (CPUs), networking products, and increasingly integrated AI systems continue to benefit from enormous investments in data center infrastructure. As a result, NVDA has continued to deliver impressive financial results.
Notably, concerns about a potential slowdown in AI development have weighed on semiconductor stocks, raising fears that the enormous spending on AI infrastructure could eventually moderate. However, demand for Nvidia's products is unlikely to slow, and the company could continue delivering extraordinary growth.
Billionaire Charlie Munger, Who Died at 99, Skipped Insurance on His Mansion Since He Could Just Write a Check to Rebuild — 'All Intelligent People Do It My Way'
Dear Tesla Stock Fans, Mark Your Calendars for October 1
However, Nvidia's operational strength hasn't fully trickled into its stock performance. NVDA stock has underperformed relative to rivals like AMD (AMD) and Intel (INTC). Its valuation also remains compelling relative to peers and its growth trajectory, supporting the bull case.
Nvidia's growth trajectory remains compelling, with expectations for substantial increases in both revenue and earnings over the coming years. The continued expansion of AI infrastructure and its expanding portfolio of computing platforms gives it a solid base for future growth.
Nvidia's top-line growth has been accelerating. In the first quarter of fiscal 2027, The company's revenue climbed 85% year-over-year (YoY). Further, in the second quarter, its top line hit $96.2 billion. That was a 106% increase YoY.
Nvidia expects third-quarter revenue to reach $108 billion. Even at that level, the company would grow revenue by more than 89% compared with the same period a year earlier. Given solid demand from diversified end markets, Nvidia could outperform its forecast, and its growth could accelerate again.
The demand is coming not only from major cloud providers but also from AI-focused companies, traditional enterprises, and governments investing in sovereign AI capabilities. Based on the company's outlook, revenue could increase by 70% in fiscal 2028.
Nvidia's data center operations are positioned to remain a major contributor, particularly as customers continue adopting the Blackwell architecture. At the same time, Nvidia's full-stack approach to AI computing allows it to participate across the infrastructure ecosystem. Nvidia has also started shipping systems based on its next-generation Vera Rubin architecture, providing another potential source of growth.
Another solid opportunity is the CPU market, particularly as agentic AI applications require more computing resources. Nvidia's Grace CPU business has already surpassed $5 billion in trailing twelve-month revenue, while Nvidia estimates that the total annual server CPU market is worth approximately $20 billion. The company expects its CPU revenue to more than double in fiscal 2028.
Nvidia's rapid revenue expansion should translate into significant earnings growth. Current analyst estimates call for Nvidia's earnings to double in fiscal 2027, followed by earnings growth exceeding 68% in fiscal 2028. With solid demand, Nvidia could also exceed analysts' expectations.
Nvidia's business continues to show solid momentum, with both revenue and profits expected to grow strongly. Despite that, NVDA stock appears undervalued. Nvidia currently trades at about 23.9 times forward earnings, which is low given its strong earnings growth potential.
Nvidia's valuation looks even more compelling when compared with peers. AMD, for example, trades at 80.3 times forward earnings, while Intel's forward P/E ratio is around 99 times. That puts Nvidia at a significant discount to both companies, despite its leadership in the AI infrastructure space.
Nvidia's accelerating revenue, exceptional earnings growth potential, expanding AI infrastructure demand, and a growing presence across GPUs, CPUs, networking, and full-stack AI systems make it a compelling investment.
While concerns over an AI spending slowdown persist, Nvidia's fundamentals still point to solid growth ahead. In addition, NVDA stock trades at a substantially lower forward earnings multiple than AMD and Intel, despite delivering stronger growth and maintaining a dominant position in AI computing.
Wall Street remains optimistic as well. Analysts currently give NVDA stock a consensus rating of "Strong Buy." With an average price target of $326.09, analysts project about 54% upside from the stock's current price.

### Article 260 · 2026-09-16 · techcrunch.com
Nvidia’s Les Karpas joins the agenda lineup at Disrupt 2026

The world hasn’t been the same since ChatGPT made its debut in November 2022, when seemingly out of nowhere, a means of engaging with large language models propelled AI beyond hype and into day-to-day reality.
Robotics, like AI, has been discussed, built upon, and in some ways adopted for a long time now, but it’s yet to have that big breakthrough moment. And at TechCrunch Disrupt 2026 , Nvidia Inception’s Global Head of Physical AI, Les Karpas , will dive into why that is and what could change that in his session on the Real World AI Stage, Robots Are Waiting for Their ChatGPT Moment. Here Is What Is Standing in the Way .
After all, anyone who’s seen Nvidia CEO Jensen Huang’s keynotes the past few years knows the company is bullish about the robotics field. And you can get the opportunity to listen as Karpas details the limitations and opportunities in the AI and robotics spaces firsthand at Disrupt. From October 13-15 at San Francisco’s Moscone West , you and 10,000+ tech leaders, founders, and investors can catch Karpas and the rest of our extensive AI-focused lineup, which ranges from building companies to building in the real world.
Act now and get your ticket to save up to $200 before September 25, after which our prices increase . Save up to 30% when you bring a group, since the Disrupt experience is meant to be shared.
The all-too-real problem facing robotics
Karpas’ POV on the core limitation facing general-purpose robots is simple to understand but wildly complicated to resolve. Nobody has an internet-wide dataset for physical AI in the way OpenAI, Anthropic, and others had for language. Even self-driving fleets from Waymo and its competitors were able to build datasets through years of accumulated road miles, datasets that are still expanding market by market.
A growing ecosystem of startups is now trying to manufacture that scale artificially through simulation, synthetic data, and foundation models trained across many robot forms simultaneously. And that challenge of bridging the digital and physical is why we created the Real World AI Stage . Karpas will be joined by founders from Shield AI, Colossal Biosciences, FieldAI, and Foxglove, as they walk through the unique challenges and opportunities they face.
Nvidia’s unique perspective comes to Disrupt
Karpas is one of the best-positioned people in the world to answer the question his session presents. As Nvidia Inception’s Global Head of Physical AI, he coordinates the company’s relationship with the wide-ranging startup ecosystem stretching across robotics, automotive, manufacturing, mobility, smart cities, and much more. The same companies trying to solve that data gap are the ones he regularly interfaces with.
And his path to getting there is one that speaks to the cross-disciplinary skills the robotics industry demands. Across roles at Stanley Black & Decker, Intellectual Ventures, Herman Miller, iRobot, Cirque du Soleil, and more, he’s been an architect, manufacturing engineer, startup CEO, venture studio executive, and corporate venture capitalist.
Create your own breakthroughs at Disrupt
This is your chance to hear firsthand how Nvidia is thinking about the single biggest bottleneck in physical AI, and what it’ll take to clear it. That kind of insight could give you a leg up on your competition or spark an idea that could fuel your next startup venture. That kind of inspiration is what Disrupt is all about, and you can get it only by being in the room and making connections during the event.
Act swiftly to get the ticket that gives you the kind of access you need, whether it’s new sources of fundraising or new startups to invest in. Lock in your trip before prices increase on September 25 . Bring a group and save up to 30% on bundle passes.

### Article 261 · 2026-09-16 · gurufocus.com
CoreWeave Stock Jumps After Major Nvidia AI System Goes Live

CoreWeave ( CRWV ) shares climbed about 3% on Wednesday trading after the AI cloud company said it had brought Nvidia's ( NVDA ) multi-rack Vera Rubin NVL72 platform online.
The new deployment connects hundreds of Rubin GPUs into a unified computing cluster designed to support large-scale artificial intelligence workloads. The rollout builds on CoreWeave's June launch of a single Vera Rubin NVL72 rack.
CoreWeave said the expanded system combines multiple Vera Rubin racks into one scalable environment using Nvidia's Spectrum-X networking technology. A single Vera Rubin NVL72 rack includes 72 Rubin GPUs and 36 Vera CPUs, along with networking and data-processing hardware intended for AI applications.
The company also introduced new capabilities for its AI Object Storage platform, including cross-region write acceleration and an archive storage tier. CoreWeave said the additions are designed to keep data closer to AI workloads and may reduce latency through managed caching across its Kubernetes-based infrastructure.

### Article 262 · 2026-09-16 · benzinga.com
Jensen Huang Says Hyperscalers Get This ‘Almost Always Wrong’ — Nvidia Has a Workaround

The biggest AI infrastructure players may have a planning problem. NVIDIA Corp 's CEO Jensen Huang says hyperscalers are "always almost wrong" because they plan capacity once a year while AI demand is changing too quickly to fit an annual calendar.
His workaround? Build a much larger network of nimble regional clouds.
The unusual admission came during the All-In Summit, when the hosts pressed Huang on Nvidia's support for neocloud companies and the need for more competition at the hyperscale layer.
Huang said Nvidia would be happy with five hyperscalers, but argued the industry ultimately needs 50, 100 or even 1,000 neoclouds. The reason is speed: hyperscalers typically plan their infrastructure once a year, while AI market dynamics are moving so rapidly that those forecasts can quickly become obsolete.
That creates an opening for regional cloud providers that can react faster to local demand and infrastructure constraints.
Huang said regional clouds know their markets and can move quickly to secure land, power and existing facilities, something that is harder for companies operating from Silicon Valley or Seattle to coordinate globally. Nvidia is consequently building what Huang described as a large-scale distributed network of companies securing those critical resources.
The strategy is already moving beyond the U.S. Huang pointed to activity in Australia and Southeast Asia, saying Nvidia is helping bring additional gigawatts of capacity online through regional cloud partners.
That could matter enormously for Nvidia. The company does not necessarily need every AI workload to run through a handful of hyperscalers if it can help create hundreds of smaller customers that collectively consume massive amounts of Nvidia hardware.
It also reinforces a broader shift in the AI infrastructure trade. The bottleneck is increasingly not simply who has the best chips, but who can secure the electricity, land and data center capacity needed to deploy them.
For investors, Huang's neocloud strategy offers a different way to think about Nvidia's next growth phase: instead of betting on fewer giant AI customers, Nvidia is helping build an army of smaller ones.

### Article 263 · 2026-09-16 · techtarget.com
With Nvidia GPUs, CoreWeave hits architectural milestone

With Nvidia GPUs, CoreWeave hits architectural milestone | TechTarget
With Nvidia GPUs, CoreWeave hits architectural milestone
TechTarget has learned that CoreWeave has put powerful multi-rack capabilities into production around Nvidia's latest AI platform.
CoreWeave has brought seven Nvidia Vera Rubin NVL72 racks into production across two regions, totaling 504 GPUs, as the AI cloud provider begins scaling Nvidia's newest systems beyond a single rack.
The company will unveil Wednesday that it has brought up multi-rack Vera Rubin systems on CoreWeave Cloud, alongside new storage capabilities designed to keep data moving as AI workloads scale.
For data center operators and IT buyers, multi-rack Rubin changes the infrastructure planning problem. A deployment must account for network capacity, power delivery, liquid cooling, storage performance and failure handling across the same workload. Those pieces can determine how much of the advertised GPU capacity a customer can actually use.
CoreWeave's Corey Sanders, senior vice president of product, said the hardest parts of moving from a single NVL72 rack to multiple racks were networking and operations.
The networking must provide enough throughput to keep AI workloads from waiting on data moving between racks. The operational challenge grows as workloads span racks that need to function together.
"The operational complexity grows more than multiplicatively," Sanders said in an interview.
Each NVL72 rack combines 72 Rubin GPUs with 36 Vera CPUs, Nvidia NVLink 6, ConnectX-9 SuperNICs, BlueField-4 DPUs, high-speed storage and liquid cooling.
"The single rack is Nvidia's product. The multi-rack domain is the operator's product," said Stephen Sopko, practice lead for semiconductors and deep tech at HyperFrame Research.
Inside an NVL72, Nvidia NVLink provides the high bandwidth scale-up fabric. Connecting multiple racks introduces a scale-out network to handle large amounts of synchronized traffic.
CoreWeave says its architecture uses two-tier, non-blocking connectivity with multiple rails and planes. Each Rubin GPU has two ConnectX-9 SuperNICs, providing up to 1.6 Tbps of scale-out network connectivity per GPU.
"The network is no longer simply connecting servers, it is becoming part of the computer itself," said Sameh Boujelbene, vice president and analyst at Dell'Oro Group.
Once GPUs span multiple racks, Boujelbene said, the scale-out network needs to keep traffic predictable under massive, synchronized workloads. Congestion, load balancing, latency and fault isolation become more important.
She called the 1.6 Tbps per GPU figure a meaningful architectural milestone because it reflects the bandwidth requirements of next-generation AI systems.
CoreWeave says its architecture can scale to roughly 128,000 GPUs per rail. That figure is an architectural-scale target, rather than a claim that CoreWeave has deployed a 128,000 GPU Rubin cluster. The company has disclosed 504 Rubin GPUs across its seven production racks.
CoreWeave also deliberately disables faster GPU-to-GPU links during testing and forces traffic through the backend network.
Sanders said the exercise lets CoreWeave see how traffic moves across the multi-plane fabric and exposes problems involving switches, cabling, software and other network components.
The company validates systems from individual GPUs and nodes through complete racks and multi-rack workloads. It runs GPU diagnostics, interconnect checks, compute and thermal workloads, rack-level 72 GPU jobs and distributed workloads before systems enter production.
Sanders said failures can originate in GPUs, networking, switches, cabling or software. CoreWeave can hold systems from production when failures or additional validation requirements emerge.
Large-scale training is particularly sensitive to the network, Sanders said. Mixture of experts inference also creates substantial inter-rack communication as models become more complex and workloads use multiple components or agents.
Networking is only part of the infrastructure CoreWeave must coordinate. Power, cooling and hardware health also need to track workloads across racks.
CoreWeave has extended its Mission Control product with Racky, its unified rack manager, and Valvey, its programmable per-rack liquid cooling valve assembly. The Rack LifeCycle Controller handles rack-level lifecycle operations.
Sanders said that CoreWeave manages power and cooling through a combination of hardware and software. Racky and Valvey can monitor infrastructure conditions, adjust cooling flow and manage usage patterns at the rack level.
"The single rack is the operational unit," Sanders said.
The approach allows CoreWeave to manage multiple racks as a larger operating environment while keeping the physical boundaries out of the customer workload.
Sopko said the operational layer is critical as AI systems become more distributed.
"The cabinet is an API object, not a custom build," he said.
A GPU can slow down. A network connection can become unreliable. A switch can fail. A cooling problem can throttle an entire rack. Any of those events can affect a distributed workload even when most of its GPUs are operating normally.
"The job has to finish," Sopko said. A slow GPU, hot rack or congested network path can stall a long-running workload and increase the cost of producing each token.
“At hundreds or thousands of GPUs, hardware failures become constant background noise," said Dave McCarthy, research vice president of cloud and edge infrastructure services at IDC. "Checkpointing overhead and automated failure recovery become critical software challenges to prevent wasted cluster hours.”
CoreWeave is also adding storage capabilities aimed at reducing data movement as distributed AI workloads scale.
Its CoreWeave AI Object Storage service includes the Local Object Transport Accelerator, or LOTA, which provides a compute local NVMe endpoint for cached object data.
CoreWeave claims LOTA can reduce latency by eight times compared with reading directly from traditional object storage. Sanders said the comparison is between direct reads from an object storage system and access through the local cache.
The company also says LOTA can provide up to 7 GBps per GPU. The throughput can be sustained under the right workload and cache conditions, Sanders said.
The technology is aimed primarily at large-scale training, where model weights, datasets and checkpoints can generate heavy storage traffic. It can also support some inference workloads and frequently accessed data.
CoreWeave is adding cross-region write acceleration for workloads such as checkpointing. Data is written durably in the local region and acknowledged locally, while the object data moves to a second region in the background.
CoreWeave says the migration typically completes within 72 hours.
Sanders said the model works for many checkpoint scenarios because the remote copy does not have to be immediately available. The workload can continue while CoreWeave handles the second copy in the background.
CoreWeave is also introducing an Archive tier for data that can move out of the active working set. Archived objects can be read without a separate restore operation, although reads have higher latency and lower throughput than data in the standard tiers.

### Article 264 · 2026-09-16 · benzinga.com
Nvidia CEO Jensen Huang Says Elon Musk’s Terafab May Look Audacious, But ‘If Anybody Could Do It, He Can’

Nvidia Corp. 's CEO Jensen Huang said Elon Musk may be uniquely positioned to pull off Terafab, the semiconductor-manufacturing project planned by Tesla Inc. and Space Exploration Technologies Corp. , while acknowledging the technical depth required to fabricate leading-edge chips.
Huang Backs Musk's Audacious Terafab Ambition
"If anybody could do it, he can," Huang said Monday at the All-In Summit. Huang said the two of them were on a flight together to a country, adding that "Elon likes to talk about these things and so we spent a lot of time talking about it."
BREAKING: Jensen Huang on Elon Musk's Terafab:
"If anybody could do it, he can. We were on a flight together and we spent a lot of time talking about it. Once he decides to do something, it's hard to stop him. You can't discourage Elon, which is one of his superpowers." https://t.co/O5vMJDgHQz pic.twitter.com/HlEeYcMjxq
— DogeDesigner (@cb_doge) September 14, 2026
Huang stopped short of saying whether Nvidia would eventually fabricate its chips at Terafab. "We know a lot about process technology because we're pushing the limits of everything," he said, pointing to Nvidia's scale and systems expertise.
Reverting to discuss Musk, the Nvidia chief said, "You can't discourage Elon from doing it," adding that it was Musk's "superpower" and that "Once he decides to do something, it's hard to stop him."
Terafab Targets Unprecedented Scale In Chipmaking
Musk unveiled Terafab in March, and SpaceX's SEC filings state that it is developing the initiative with Tesla, while Intel Corp. joined in April. The long-term goal is one terawatt of compute hardware annually, with lithography-mask design, logic and memory fabrication, and advanced packaging vertically integrated under one program.
SpaceX says it is developing Terafab to ease potential chip shortages and produce hardware optimized for Tesla vehicles and Optimus robots, alongside chips designed for orbital AI infrastructure. Musk has said the facility could span roughly 100 million square feet, about 10 times the size of Tesla's gigafactory in Texas.
The company cautions, however, that specific timelines, milestones, and capital expenditures remain undetermined and that neither Tesla nor Intel is obligated to remain involved. SpaceX in its SEC filing also warns Terafab may ultimately fail to meet its chip needs.
Huang's confidence follows earlier praise for Musk's execution. Nvidia said xAI and Nvidia built the 100,000-GPU Colossus supercomputer in Memphis in 122 days, including just 19 days from the first rack arriving to the start of training. Huang earlier on a podcast aired in October 2024, called the accomplishment "superhuman" and described Musk as "singular in his understanding of engineering."
The admiration runs both ways. Musk said in March he was a "huge admirer" of Nvidia and Huang, called Nvidia's market capitalization "well-deserved," and said Tesla and SpaceX expected to keep ordering its chips at scale.
Their relationship deepened in August when Musk said SpaceX would build "exclusively" on Nvidia, calling Vera Rubin "the best AI computer."

### Article 265 · 2026-09-16 · finance.yahoo.com
Q2 Earnings Roundup: Nvidia (NASDAQ:NVDA) And The Rest Of The Processors and Graphics Chips Segment

Let's dig into the relative performance of Nvidia (NASDAQ:NVDA) and its peers as we unravel the now-completed Q2 processors and graphics chips earnings season.
The biggest demand drivers for processors (CPUs) and graphics chips at the moment are secular trends related to 5G and Internet of Things, autonomous driving, and high performance computing in the data center space, specifically around AI and machine learning. Like all semiconductor companies, digital chip makers exhibit a degree of cyclicality, driven by supply and demand imbalances and exposure to PC and Smartphone product cycles.
The 9 processors and graphics chips stocks we track reported a very strong Q2. As a group, revenues beat analysts' consensus estimates by 6.3% while next quarter's revenue guidance was 6.8% above.
While some processors and graphics chips stocks have fared somewhat better than others, they have collectively declined. On average, share prices are down 3.6% since the latest earnings results.
Nvidia (NASDAQ:NVDA)
Founded in 1993 by Jensen Huang and two former Sun Microsystems engineers, Nvidia (NASDAQ:NVDA) is a leading fabless designer of chips used in gaming, PCs, data centers, automotive, and a variety of end markets.
Nvidia reported revenues of $96.22 billion, up 106% year on year. This print exceeded analysts' expectations by 4.2%. Overall, it was a very strong quarter for the company with a beat of analysts' EPS estimates and an impressive beat of analysts' operating income estimates.
"AI has reached its inflection point. It's doing useful work. Its tokens are productive and profitable. Now, compute is revenue," said Jensen Huang, founder and CEO of NVIDIA. "And demand is accelerating. This time last year, one lab alone was driving the buildout; today, we have a golden age of new AI labs and startups, multiple frontier labs scaling in parallel, a thriving open-model ecosystem and physical AI coming online — with strong momentum across the U.S. and around the world. The AI infrastructure buildout is at full steam. Vera Rubin, now in full production, was built to power exactly this moment."
Nvidia achieved the fastest revenue growth in the group. Unsurprisingly, the stock is up 1.3% since reporting and currently trades at $212.38.
Best Q2: Intel (NASDAQ:INTC)
Inventor of the x86 processor that powered decades of technological innovation in PCs, data centers, and numerous other markets, Intel (NASDAQ:INTC) is a leading manufacturer of computer processors and graphics chips.
Intel reported revenues of $16.13 billion, up 25.4% year on year, outperforming analysts' expectations by 11.7%. The business had an incredible quarter with a significant improvement in its inventory levels and a beat of analysts' EPS estimates.
Although it had a fine quarter compared to its peers, the market seems unhappy with the results as the stock is down 3.2% since reporting. It currently trades at $97.06.
Having been at the forefront of developing the standards for cellular connectivity for over four decades, Qualcomm (NASDAQ:QCOM) is a leading innovator and a fabless manufacturer of wireless technology chips used in smartphones, autos and internet of things appliances.
Qualcomm reported revenues of $9.95 billion, down 4% year on year, exceeding analysts' expectations by 3%. Still, it was a mixed quarter as it posted an increase in its inventory levels.
A global leader in its category, Lattice Semiconductor (NASDAQ:LSCC) is a semiconductor designer specializing in customer-programmable chips that enhance CPU performance for intensive tasks such as machine learning.
Lattice Semiconductor reported revenues of $201.1 million, up 62.2% year on year. This number surpassed analysts' expectations by 8.6%. Overall, it was a stunning quarter as it also produced a beat of analysts' EPS estimates and an impressive beat of analysts' operating income estimates.
Lattice Semiconductor achieved the highest guidance raise among its peers. The stock is down 23.5% since reporting and currently trades at $105.51.
Based in the US, Penguin Solutions (NASDAQ:PENG) is a diversified semiconductor company offering memory, digital, and LED products.
Penguin Solutions reported revenues of $478.7 million, up 47.6% year on year. This print beat analysts' expectations by 17.5%. It was an exceptional quarter as it also recorded a beat of analysts' EPS estimates and an impressive beat of analysts' operating income estimates.
Penguin Solutions pulled off the biggest analyst estimate beat of the whole group. The stock is down 24.4% since reporting and currently trades at $47.41.
Over the past year, investors have been forced to repeatedly answer the same question: what is the market's biggest risk? The answer has changed several times, and each shift has reshaped market leadership.
Late in 2025 and early 2026, artificial intelligence became the market's primary uncertainty. Investors questioned whether AI would erode software pricing power and weaken competitive moats as AI made it easier to replicate once-differentiated products.
By the spring, technology took a back seat to geopolitics. The U.S. conflict with Iran briefly became the market's dominant narrative, raising concerns about oil prices, inflation, and global growth. But as energy markets remained orderly and fears of a prolonged supply disruption faded, investors quickly turned their focus back to fundamentals.
Want to invest in winners with rock-solid fundamentals? Check out our Top 5 Quality Compounder Stocks and add them to your watchlist. These companies are poised for growth regardless of the political or macroeconomic climate.

### Article 266 · 2026-09-16 · wccftech.com
Valve Enables NVIDIA Drivers Inside SteamOS, But Admits A Performance Rift Still Separates It From Windows

Valve highlights the importance of NVIDIA GPU support for SteamOS as certain GPU generations now become compatible, but performance optimizations are still going on.
Valve Enables NVIDIA's Driver in the Main SteamOS Tree, but Performance Remains Behind the Current Linux Driver Stack
Valve is making some significant progress in bringing NVIDIA GPU support to SteamOS, which has been one of the biggest hardware compatibility barriers. Speaking to IGN ahead of the Steam Frame launch, Valve software developer Pierre-Loup Griffais said that the company is working heavily on NVIDIA support and described it as a top priority.
It's definitely at the top of our list. It's one of those things just like FEX and working on the Qualcomm driver, it just takes years.
Griffais reports that Valve has now enabled the NVIDIA driver in the main SteamOS development tree, and this makes certain NVIDIA GPU generations initialize and display an image under SteamOS. However, it's one of the first steps to getting the hardware to work as it's intended to. Griffais acknowledged that there is a noticeable performance gap between Valve's current implementation and the state-of-the-art NVIDIA driver stack.
We've done a few things like we've enabled the driver now in the main tree of SteamOS,
so you can get things to light up on certain generations, but in terms of the performance difference between that driver and where the state of the art is, there's definitely still a little bit of a rift that we're trying to work on, but it's getting better day-to-day.
He says that the team is continuously working on this gap and that the situation is improving on a daily basis. This seems particularly important as Valve continues to expand SteamOS beyond its Steam Deck console. The operating system is now being developed for a wide range of hardware that includes desktops and even third-party handhelds. Valve has previously confirmed that it has been working closely with NVIDIA to improve compatibility with GeForce hardware.
As you might know, NVIDIA has a dominant position among Steam users when it comes to the most popular GPUs. This makes proper GeForce hardware support relevant to Valve's efforts. However, the company hasn't provided a specific release date for full NVIDIA GPU support.

### Article 267 · 2026-09-16 · fool.com
Nvidia Stock Forecast: Where Investors Could Stand in 5 Years

The artificial intelligence (AI)-fueled surge in shares of Nvidia (NASDAQ: NVDA) has made it the largest company in the world with a market cap of over $5 trillion.
It has reached this position following a stunning jump of almost 10x in the stock price over the past five years. Investors may now be wondering whether Nvidia can achieve another 10x jump over the next five years, especially given its enormous market cap.
We will take a closer look at Nvidia's prospects and see how much upside investors can expect from this AI stock over the next five years.
Can Nvidia really jump another 10x?
A 10x jump in Nvidia stock over the next five years will take its market share to $50 trillion. The global gross domestic product (GDP) is anticipated to hit $150 trillion in 2030, according to data from Visual Capitalist, up from $125 trillion last year.
A 10x jump in Nvidia stock means that it will account for a third of the global GDP after five years, as compared to just 4% right now. That seems quite unlikely. However, Nvidia still has significant room for growth over the next five years, and it trades at an attractive valuation. As a result, there is a good chance the company will deliver solid gains.
For instance, AI infrastructure spending isn't slowing down. Nvidia points out that the annual capital spending by the top five hyperscalers is on track to reach $800 billion this year. The figure is expected to increase to $1.3 trillion in 2027. Importantly, annual data center spending could cross $3 trillion in 2030, according to market research firm Dell'Oro.
The firm points out that a third of this spending, or $1 trillion, will go toward AI accelerators. The networking components to connect those accelerators will add to this addressable market. Nvidia is the biggest player in AI accelerators with an 80% market share. The company is bolstering its presence in this market by entering into lucrative areas, such as server processors .
As such, I won't be surprised to see Nvidia maintaining its dominance in the AI accelerator market after five years. Assuming it can sustain its impressive share of this space, its AI accelerator revenue alone could hit $800 billion (based on the $1 trillion estimate noted in the previous paragraph). That would be a big jump over Nvidia's 2026 data center revenue of $194 billion. It is worth noting that the company also includes sales of networking components in the data center segment, so Nvidia's addressable opportunity could be much larger.
What's worth noting is that this estimate has increased substantially this year. Let's assume Nvidia indeed manages to clock 52% annual earnings growth over the next five years; its earnings per share could reach $75.54 (using fiscal 2027's projected earnings per share of $9.31 as the base).
If this AI stock trades at 21 times earnings after five years, in line with the S&P 500 index's forward earnings multiple, its price could jump to $1,586. That's 7.5x Nvidia's current stock price.
Of course, this may seem like a very ambitious estimate. Still, it is evident that Nvidia has the potential to jump significantly over the next five years, even if the stock doesn't multiply by 7x. This makes Nvidia stock an attractive buy right now as it trades at just 24 times forward earnings.

### Article 268 · 2026-09-16 · reuters.com
Snap targets enterprises with Salesforce, Nvidia AI tools for augmented-reality glasses

Sept 16 (Reuters) - Snap on Wednesday announced partnerships with companies including Salesforce, Nvidia and Amazon Web Services to integrate workplace tools into ‌its Specs augmented-reality glasses, courting enterprise demand to carve a foothold ‌in the heavily contested market.
Unveiled in June with a hefty price tag of $2,195, Specs is a ​major bet by the Evan Spiegel-led social media company in a category drawing increasing investments and consumer interest and dominated by Big Tech rival Meta.
Apple , however, has seen mixed results in making its Vision Pro headset a mainstream success, ‌underlining the challenges facing the ⁠AI-powered gadgets segment.
To drive sales in a tough market, Snap is positioning its AR glasses as a workplace device for businesses ⁠seeking hands-free computing solutions in environments traditionally disconnected from desktops, such as factory floors, retail outlets and field service operations.
Snap said enterprise software maker Salesforce would add ​its AI ​agent platform Agentforce into Specs, allowing workers ​to access company data and ‌automate tasks through the glasses.
Nvidia will power the AI, enabling Specs to interpret a worker's visual environment and retrieve relevant company data, while Amazon Web Services will offer its AI assistant, allowing employees to use voice commands for tasks such as checking product availability.
Snap did not disclose the financial terms of the ‌partnerships, which include those with software company ​Trifork and augmented-reality software firm Hololight.
Specs' charging case, ​sold separately, will have cellular ​connectivity through its telecom partners, including Verizon in the U.S., ‌Orange in France and BT Group's ​EE in the ​UK.
Snap, which also announced Specs Intelligence AI service on Wednesday, has previously said shipping for the glasses is expected to begin later this fall ​in the U.S., UK and ‌France.
Starting in October, consumers can try Specs at the Westfield Century ​City shopping mall in Los Angeles, Snap said.
(Reporting by Jaspreet Singh ​in Bengaluru; Editing by Jonathan Ananda)

### Article 269 · 2026-09-16 · benzinga.com
Chamath Called Nvidia the ‘Bank of AI’—and Jensen Huang Just Proved It

Nvidia Corp is no longer just selling the picks and shovels of the AI boom. It is increasingly helping figure out who gets the money, infrastructure and computing power needed to build the next phase of it—which may explain why Chamath Palihapitiya called the company the "bank of AI" at the All-In Summit.
The comment came as the All-In hosts pressed Jensen Huang on Nvidia's growing role across the AI ecosystem. The company has been working across suppliers, infrastructure providers and financing partners to address bottlenecks before they constrain AI deployment.
Huang's explanation was revealing. He described AI as a "new industrial revolution" requiring far more than GPUs: manufacturing, electricity, internet infrastructure and physical data-center capacity all have to scale together.
That creates an unusual strategic opportunity for Nvidia. If the company can identify where the ecosystem is about to hit a wall—and help remove that wall—it can expand the addressable market for its own computing platform at the same time.
The scale of that challenge is already becoming enormous. Huang said roughly $400 billion in venture financing flowed into AI companies over six months, creating jobs and massive demand for compute, which is subsequently driving demand for data centers.
The financing question becomes particularly important as AI infrastructure requirements move into the hundreds of billions of dollars. Nvidia has increasingly worked with financial institutions and other ecosystem players to help make AI compute an investable, financeable asset.
That is what makes the "Bank of AI" analogy more than a clever sound bite. Nvidia does not need to own every company building AI infrastructure. It needs those companies to have enough capital to keep buying Nvidia-powered systems.
The strategy effectively turns Nvidia into an ecosystem enabler: Help customers secure capital, power and infrastructure, and Nvidia can keep supplying the computing engine underneath them.
For investors, that could make Nvidia's AI opportunity considerably broader than its semiconductor market share. The biggest constraint on AI spending may eventually be capital and infrastructure—not demand for GPUs.
And if Huang can help solve that constraint, Chamath's "Bank of AI" label may prove less metaphor than business strategy.

### Article 270 · 2026-09-16 · investing.com
Apple building M8 AI servers, talks with Nvidia, reports The Information

Apple building M8 AI servers, talks with Nvidia, reports The Information
Investing.com -- Apple is developing an enterprise AI server built around its own M8 Ultra chips, with a target launch of 2029, and has held talks with Nvidia about using the chipmaker's NVLink Fusion interconnect platform to link those chips together, The Information reported Wednesday.
Nvidia (NASDAQ: NVDA), which dominates the AI server market and earns roughly a fifth of its data-centre revenue from networking gear, is the most direct equity expression of that development: any Apple deal to adopt NVLink Fusion would add a new, large-volume customer while simultaneously confirming Nvidia's strategy of monetising interconnect technology even as rival chips challenge its GPU franchise.
The planned server would come in two configurations — one pairing two M8 Ultra chips and one pairing four — and would target AI developers, businesses and governments, according to The Information. Some Apple engineers working on the project believe Nvidia's NVLink Fusion, which bundles switches, chiplets and software to allow chips from different vendors to communicate at high speed, represents the best available connectivity solution. The product could still be cancelled, The Information noted, and neither Apple nor Nvidia has publicly confirmed the talks.
New Apple (NASDAQ: AAPL) CEO John Ternus, who took the helm earlier this month, was a backer of the server project at its inception roughly a year ago while leading Apple's hardware engineering division, people familiar with the matter told The Information. His continued support is seen as a key reason the project has momentum.
The project reflects a genuine commercial imperative. Mac was Apple's fastest-growing product segment in its most recently reported quarter, with revenue surging nearly 29% to $10.4 billion, fuelled by unexpected demand from AI developers snapping up Mac mini and Mac Studio units, per The Information. That surge has created acute supply shortages and exposed the limits of consumer-grade hardware for enterprise AI workloads.

### Article 271 · 2026-09-16 · gurufocus.com
CoreWeave Doubles Down on Nvidia at Critical Moment

CoreWeave ( NASDAQ:CRWV ) shares rose about 3% Wednesday after the AI cloud provider brought Nvidia's ( NASDAQ:NVDA ) multi-rack Vera Rubin NVL72 system online, connecting hundreds of next-generation Rubin GPUs into a single scale-out cluster. The milestone strengthens CoreWeave's pitch as one of the earliest cloud platforms able to commercialize Nvidia's newest AI hardware, an important differentiator as competition intensifies across AI infrastructure.
Warning! GuruFocus has detected 4 Warning Signs with CRWV.
Is CRWV fairly valued? Test your thesis with our free DCF calculator.
CoreWeave operates specialized cloud infrastructure designed for artificial-intelligence workloads, leasing high-performance computing capacity to customers training and running large AI models. Its business depends heavily on access to Nvidia GPUs, rapid infrastructure deployment and keeping expensive computing assets highly utilized.
The announcement builds on CoreWeave's June disclosure that it was the first AI cloud provider to bring a Vera Rubin NVL72 system online.
"CoreWeave was the first AI cloud provider to validate and bring up a Vera Rubin NVL72, demonstrating that this advanced rack-scale architecture could operate as a reliable, high-performance cloud service," said Chen Goldberg, executive vice president of product & engineering at CoreWeave.
A single NVL72 rack combines 72 Rubin GPUs with 36 Vera CPUs. CoreWeave's multi-rack configuration links hundreds of accelerators using Nvidia's Spectrum-X Ethernet networking, allowing customers to treat a much larger pool of compute as one cluster.
"For customers building agentic AI, that means greater scale, faster iteration, and higher productivity as models and agents continuously learn and improve," Goldberg said.
CoreWeave also introduced upgrades to its AI Object Storage platform, including cross-region write acceleration and a new Archive tier. Its Local Object Transport Accelerator can reduce latency by as much as eight times through managed caching.
The launch strengthens CoreWeave's technology credentials, but the key question is whether early access translates into profitable utilization.
Investors should watch customer demand for Rubin capacity, contract wins, utilization rates and whether new clusters generate enough revenue to justify CoreWeave's heavy infrastructure spending.
Faster-than-expected Rubin adoption would strengthen the growth case. The risk is that capacity expands faster than customer demand, leaving CoreWeave with expensive assets that take longer to monetize.

### Article 272 · 2026-09-16 · gurufocus.com
Apple may build AI servers with its own chips and Nvidia networking

Apple Inc. ( AAPL , Financials ), the consumer technology company behind the iPhone and Mac , may be preparing to take its in-house chips somewhere new.
Warning! GuruFocus has detected 6 Warning Sign with BAC.
The company is considering building enterprise servers powered by its M-series Ultra processors, according to The Information. There is another interesting piece. Apple could pair those chips with networking equipment from Nvidia.
That would put two very different chip strategies inside the same server. Apple has spent years designing processors to reduce its dependence on outside suppliers, while Nvidia has become the backbone of much of the AI data-center market.
Apple would reportedly sell the servers to businesses rather than simply use them inside its own data centers.
That could matter.
Apple silicon has largely been associated with Macs, iPhones and the company's own computing ecosystem. Selling servers would give Apple a way to push those chips into the much larger enterprise infrastructure market.
It could also put Apple closer to companies such as Dell, Hewlett Packard Enterprise and Supermicro, which already sell servers into data centers.
The project is still under consideration, so there is no guarantee Apple moves forward.
But if it does, investors may have to start looking at Apple's chip strategy differently not simply as something that powers its devices, but as a business that could eventually reach well beyond them.

### Article 273 · 2026-09-16 · fool.com
Michael Burry Just Said 7 Words Dismissing AI After Slowdown Fears: "There Is Nothing AI to Slow Down." Should Investors Trust His Nvidia and Palantir Shorts?

Michael Burry earned his fame by correctly anticipating the 2008 mortgage crisis and shorting the mortgage bond market to make a windfall, as chronicled in the best-selling Michael Lewis book The Big Short and the movie of the same name. He recently closed down his money management fund, but he still provides market commentary for his fans.
This week, he took a shot at artificial intelligence (AI) companies as concerns arise about the idea that the pace of AI development needs to be slowed, saying, "There is nothing AI to slow down."
Burry has asserted that the AI sector is in a bubble many times, and he put his money where his mouth is with literal puts on Nvidia ( NVDA +2.55% ) and Palantir Technologies ( PLTR +1.32% ) . He recently sold his Nvidia position and part of his Palantir position to free up cash, but he retains several short positions in the tech sector. Meanwhile, Wall Street is broadly bullish on both. Should investors trust Burry's negative views?
Should AI slow down?
Recently, there has been a surge in the level of worried talk about the damage that AI could do to human society. The volume has picked up since it was revealed that some AI agents have gone rogue and autonomously hacked external companies' systems in pursuit of their own ends.
Such events have led several high-profile AI developers to warn that the consequences of unchecked AI development could be disastrous, and to call for a slowdown.
Anthropic CEO Dario Amodei, for example, published a note urging a slowdown, "pacing the rate of capabilities advancement so that risk prevention has time to keep up." OpenAI CEO Sam Altman and SpaceX CEO Elon Musk both chimed in with notes of caution as well.
AI companies like Nvidia and Palantir have benefited from breathtaking advances in AI, and if those technologies were to be exposed as not quite as revolutionary as the world thinks, their stocks could plummet. Nvidia's share price growth has already started to slow down from its previous torrid pace. It's up 13% this year, roughly the same as the S&P 500 . It has also become much cheaper, trading at 27 times earnings. Palantir stock is roughly flat year to date, but it's still quite expensive, trading at a P/E ratio of 148.
Burry asserts that the call for a development slowdown is a planned move to cover for companies that are slowing down anyway:
Let's all take a moment to understand how self-serving it is for OpenAI, Anthropic and other execs of big hyperscalers to talk of slowing things down.
1. LLMs are not AI and won't be AGI. There is nothing AI to slow down.
2. Competition is coming up fast, slowing benefits...
-- Cassandra Unchained (@michaeljburry) Sept. 14, 2026
This isn't surprising given his previous views on AI, but so far, AI is demonstrating value for users, which is why investors are tolerating all of the AI-related capital expenditures, which Nvidia expects to reach $3 trillion to $4 trillion by 2030.
Burry's been right before, and he made a fortune off his analysis. But he isn't necessarily always right. Should investors trust his analysis here?
Investors should certainly be prepared for any outcome in AI. Whether Burry's right or not, investors should maintain a diversified portfolio and avoid being overly concentrated in AI or any other industry. You don't have to short the AI sector, but you shouldn't bet only on it, either.
Michael Burry Just Said 7 Words Dismissing AI After Slowdown Fears: "There Is Nothing AI to Slow Down." Should Investors Trust His Nvidia and Palantir Shorts?
By Jennifer Saibil – Sep 16, 2026 at 1:35AM EST
Several high-profile AI leaders have recently agreed that AI developers should slow down due to the dangers the technology poses.

### Article 274 · 2026-09-16 · wccftech.com
NVIDIA Reportedly Sends RTX 5070 Replacement Without Informing The User; GPU Gets Stolen As FedEx Delivers It In The Bin

The report shows the negligence on NVIDIA and FedEx' part, resulting in the theft of an RTX 5070 GPU.
User Claims Both NVIDIA and FedEX Didn't Inform Him About the GPU Replacement Being Delivered Until the User Found Someone Stole His GPU
Welcome to another RMA horror story, where the user neither got his GPU repaired or replaced, nor did he get his original GPU back. The Redditor u/Ill_Worker3155 says he was having an issue with his GeForce RTX 5070 and decided to send the card to NVIDIA for an RMA. NVIDIA accepted the RMA request and also agreed to replace the GPU.
The FedEx tracking showed that the GPU was received by NVIDIA on August 29, but NVIDIA didn't confirm receipt of the GPU. Nearly two weeks later, the user was still clueless as to why NVIDIA didn't update him regarding the RMA process. NVIDIA reportedly didn't send him any notification about sending the replacement either, forcing the user to contact the company regarding the same.
NVIDIA informed the user that the package was already delivered by the courier service, which was surprising, as the user didn't get the notification from FedEx either. After checking the tracking number, the user discovered his GPU was already delivered on September 9, and the delivery guy left it in the outdoor recycling bin. The surprising part of the story is that FedEx marked his package as "Signature release on file", which means the delivery didn't require the customer's signature.
It's unclear as to who authorized that release. It could have been a delivery preference or an instruction associated with the shipment. In any case, by the time the user checked his bin, the RTX 5070 package was gone. Here, we see clear negligence by both NVIDIA's RMA service and FedEx, which handled the delivery. Neither of them contacted the user via any means, leaving the user without a GPU that now costs over $800.

### Article 275 · 2026-09-16 · marketbeat.com
AI Panic Hit Tech Stocks—But NVIDIA’s Growth Engine Is Intact

Despite calls to slow AI model advancement, infrastructure demand remains strong, with backlogs and capital expenditure plans expanding significantly across hyperscalers in Q2.
NVIDIA maintains a nearly 97% Buy-side analyst consensus with no Sell ratings, and its consensus price target implies more than 50% upside from current levels.
Inference workloads, led by companies like Advanced Micro Devices, are poised to accelerate data center buildout as AI infrastructure shifts from training toward profitable monetization.
AI leaders shocked the world by calling for a slowdown in AI's advancement and for regulation. The news triggered a sector-wide drawdown, raising the risk of a deeper correction, but short sellers shouldn't get their hopes up.
As scary as it may seem to AI investors, the slowdown in AI's advancement isn't likely to affect the infrastructure buildout. For the market, more advanced AI models don't matter, since labs such as OpenAI and Anthropic already have highly capable (and potentially dangerous) versions; what matters is the infrastructure to deploy utilitarian AI across the enterprise landscape.
→ IonQ and NVIDIA Just Cracked a Major Quantum Computing Bottleneck
The market gets this wrong: safety and capacity aren't the same thing. AI demand is not collapsing. Q2 results from NVIDIA (NASDAQ: NVDA) to Salesforce (NYSE: CRM), and nearly every AI-capable company in between, point to accelerating infrastructure demand. In this scenario, September price weakness is a good time to buy these stocks, as catalysts for their price action lie ahead.
The AI Boom Hasn't Really Boomed (Yet)
Key details for investors to watch include backlogs, utilization rates, persistent pricing power, and the potential for capital expenditure (CapEx) relief. Q2 backlogs expanded at a historic pace, increasing by triple digits at Alphabet (NASDAQ: GOOGL), Dell (NYSE: DELL), and Super Micro Computer (NASDAQ: SMCI).
→ 3 Luxury Consumer Brands to Watch in a Beaten-Down Sector
Critical players like Oracle (NASDAQ: ORCL), now ubiquitous across cloud instances regardless of hyperscaler, saw backlogs grow to more than $650 billion, while neoclouds like Nebius (NASDAQ: NBIS) reported far larger increases, with Nebius's backlog up 4x. CapEx plans among the leading hyperscalers total over $700 billion, underscoring the spend.
Utilization rates matter because they run near 100%, even for older legacy technology. The takeaway is that technology transitions from model training and advanced computing to inference as it ages out, providing a long runway for cash flow and capitalization. This is the foundational factor in NVIDIA's ability to securitize its GPUs, enabling institutional investors such as retirement funds to invest in the cash flow.
The trigger for stock price gains will be the monetization of existing assets, which, coincidentally, aligns with profitability. Hyperscalers dialing back ultra-expensive frontier modeling will suddenly free up cash flow, removing the primary hurdle for stock prices today. The upfront cost of AI infrastructure is debilitating, impairing cash flow and profitability for most AI-related companies.
However, analysts were skeptical of CapEx plans and a rapidly differentiating market, causing stocks to move in different directions. As it stands, AI infrastructure names, including NVIDIA, remain the big winners, as they are the focus of current spending.
Wedbush pointed out that the buildout is moving slightly faster than adoption, which is a root cause of concern. The takeaway for investors is that slowing AI model spend not only improves profitability but also frees up cash to meet existing CapEx plans.
NVIDIA is the most important stock for AI today, providing the core infrastructure and software that enable it, and its analyst trends are as strong as they could be.
MarketBeat shows coverage increasing month over month and a firm Buy consensus rating with nearly 97% Buy-side bias. Currently, the company carries no Sell ratings, and the consensus price target implies more than 50% upside.
Valuation metrics suggest NVIDIA is 50% undervalued today simply based on its price-to-earnings (P/E) multiple, trading in the low 20s versus the historical mid-30s.
Stock price chart for NVDA with moving averages, MACD, and stochastic indicators, displaying the stock pulling back on AI modeling fears.
Longer-term, this stock is trading at pennies on the dollar, approximately 5x the five-year outlook, suggesting it can rise by 400% to 600% over the coming years.
Its Helios racks provide hyperscalers with numerous benefits, including inference speed, cost, and profitability. Investors need to remember that model training is the "upfront" cost of AI, while inference is the back-end monetization. With this in mind, we can expect the data center buildout to continue at full steam, if not accelerate, over the coming quarters as AI inference ramps to critical mass.
The biggest risks for AI are bottlenecks in GPU and memory supply, as well as in energy and water. These factors are slowing the build, but also provide opportunities. Companies such as Vertiv (NYSE: VRT), Bloom Energy (NASDAQ: BE), and AirJoule (NASDAQ: AIRJ) provide hurdle-jumping technologies that enable data centers to exist and operate with minimal impact on locals.
Among the risks are the upcoming elections, which are likely to be a referendum on AI. The outcome will have far-reaching ramifications but is unlikely to end the buildout. Potentially, established AI companies could benefit from increased regulatory oversight, as it could widen their competitive moats—making it harder for new AI labs to start, limiting the risk of disruption. If increased regulations don't come about, these companies will have free rein to continue building their city-sized supercomputers.

### Article 276 · 2026-09-16 · zacks.com
SoundHound vs. NVIDIA After Earnings: Which AI Stock to Buy Now?

SoundHound AI, Inc . SOUN emphasizes voice and agentic artificial intelligence (AI), while NVIDIA Corporation NVDA remains a major player in AI infrastructure. Both companies have benefited from strong AI demand, as reflected in their latest quarterly results. Let's compare their latest results and growth prospects to determine which stock offers the stronger investment opportunity right away.
SOUN's Growth Accelerates as Margins Improve and Losses Narrow
SoundHound reported exceptional second-quarter 2026 results, as highlighted in the company's Aug. 5 press release. Revenues reached $61.9 million in the second quarter, up 45% year over year. Revenue growth remains a key positive, as second-quarter revenues were 10 times higher than the second-quarter 2022 levels when it debuted as a public company.
Management expects the revenue growth momentum to continue through the remainder of 2026, and raised its full-year revenue outlook to $230 million-$260 million. Revenue growth is expected to improve as demand for high-ROI voice and agentic AI solutions accelerates, supported by SoundHound's OASYS platform and in-house AI models.
The company's GAAP gross profit jumped 68% year over year in the second quarter, outpacing its 45% revenue growth and signaling improving profitability as the business scales. While SoundHound remains unprofitable, its losses are narrowing, with its GAAP net loss declining to $42.8 million from $74.7 million in the year-ago quarter.
NVDA's AI Growth Accelerates on Strong Data Center Demand
NVIDIA's Data Center business remains the primary growth driver, generating $89 billion in the fiscal second quarter of 2027, up 117% from a year ago and 18% sequentially, according to the company's Aug. 26 press release. The company's consolidated revenues reached $96.2 billion, up 106% year over year and 18% quarter over quarter.
Revenue growth momentum is expected to remain strong next quarter. Management projects revenues of around $108 billion, plus or minus 2%, for the fiscal third quarter of 2027, up 12% sequentially at the midpoint.
NVIDIA also delivered robust profitability alongside strong top-line growth. The company's non-GAAP gross margin was 75% compared to 72.5% a year earlier, while high operating income indicated that NVIDIA was able to convert its revenue growth into higher earnings.
Meanwhile, the advanced Vera Rubin platform is in full production, positioning NVIDIA to benefit from the next wave of AI investment.
SoundHound or NVIDIA—Which AI Stock to Buy Post Earnings?
The latest earnings results have highlighted that both SoundHound and NVIDIA have benefited from strong AI-driven growth. SoundHound has demonstrated rapid revenue growth and improving financial performance, while NVIDIA delivered robust revenue growth and strong profitability.
However, SoundHound's growth remains concentrated in the voice and agentic AI market, which is still smaller in scale, while its ongoing losses make it a high-risk investment. In contrast, NVIDIA has built a dominant position in the AI infrastructure market, supported by a deep-rooted ecosystem, varied revenue streams, and strong profitability.
All these factors make NVIDIA a more mature business, with a stronger financial foundation than SoundHound. Thus, NVIDIA is a more compelling buy right now. NVIDIA currently carries a Zacks Rank #1 (Strong Buy). You can see the complete list of today's Zacks Rank #1 stocks here.
SoundHound AI, Inc. (SOUN) : Free Stock Analysis Report

### Article 277 · 2026-09-16 · bgr.com
What Is Hugging Face, Nvidia's Latest Acquisition?

What Is Hugging Face, Nvidia's Latest Acquisition?
By Marcus Mears III
We may receive a commission on purchases made from links.
While some of the best GPUs may spring to mind first when you think of Nvidia, the company's recent contributions in AI go well beyond selling processors, and those contributions may be intensifying following the recent announcement that Nvidia agreed to acquire the company Hugging Face . The agreement was made public on September 2, 2026, and the $12.9 billion deal, set to finalize in the first half of 2027, brings one of the most prominent figureheads in open AI development under Team Green's purview.
Hugging Face is a community for over 18 million developers and power users to come together, collaborate, and share AI models (among other resources like tutorials) built for various solutions in data science and machine learning. Visit the Hugging Face website , and you'll see that one of its most prominent features is the Hugging Face Hub , a massive repository where creators can find and share apps, models, and datasets. It's similar to GitHub, but with a much heavier focus on machine learning and AI development.
But it's not just for individuals. According to Nvidia , "more than 200,000 companies use the platform to discover, evaluate, customize and deploy AI," so acquiring Hugging Face is a two-pronged attack strategy. acquire a major AI player ingrained into a significant portion of corporate tech, and gain a direct access line to a passionate community of creators and their projects.
Why would Nvidia buy Hugging Face?
Over the years, Nvidia engineered a comprehensive software ecosystem to complement its hardware, including CUDA (Compute Unified Device Architecture), which is a major perk of switching to Nvidia GPUs according to owners , and a growing slate of tools, libraries, and AI models. Acquiring Hugging Face gives Nvidia ownership of a platform millions of developers use to discover, customize, and deploy those models, furthering the company's reach beyond the hardware and software infrastructure that powers those applications.
Hugging Face's emphasis on open models is particularly important to Nvidia here — unlike proprietary services that keep architecture and weights behind closed doors, open-source and open-weight models give developers considerably more freedom to access, modify, and distribute AI models on their own infrastructure. Hugging Face has quickly become a bustling distribution point for those models.
Nvidia CEO Jensen Huang has also been a vocal supporter of open models , and Nvidia itself has already contributed hundreds of models and datasets to Hugging Face, including GR00T training data which rose to the top 10 most-downloaded datasets on the entire platform. Aside from expanding Nvidia's grip on the AI sector, there is also a defensive aspect to the acquisition. Major Nvidia customers are developing their own AI processors, including Microsoft ( Maia 200 ), Google ( Tensor Processing Units ), and Amazon ( Trainium 3 ), potentially reducing their reliance on Nvidia's products over time. Owning a platform used by millions of AI developers could give Nvidia another avenue for maintaining its influence over the broader AI ecosystem.
What this means for Hugging Face developers
For now, developers shouldn't expect Hugging Face to become an Nvidia-only ecosystem. Huang has explicitly stated that "Hugging Face will remain an open platform for the entire AI ecosystem. Developers will choose the models they want, the frameworks they want, the clouds and inference service providers they want and the computing platforms they want." In other words, you will not have to jump through Nvidia-shaped hoops to build on or deploy to the Hugging Face community.
Nvidia's many resources could also allow for significant expansion. Huang says Nvidia plans to leverage its infrastructure, engineering and global reach to improve platform reliability, safety, model evaluation, inference and deployment capabilities across Hugging Face. This is particularly beneficial when open-source and open-weight projects are involved — there is strength in numbers.
Still, Nvidia's ownership is not likely to be looked upon positively by all. Outside of Hugging Face's recent security controversy as a result of an OpenAI hack , Nvidia is planting its green flag into a tight knit community that previously wasn't bound by an overarching corporation's commitment to shareholders, interests in business expansion, and possible future rules and restrictions. Huang's commitment to maintaining Hugging Face's open-source nature is reassuring for the time being, but developers will ultimately have to wait and see if that promise is kept.

### Article 278 · 2026-09-16 · gurufocus.com
Apple Talks to Nvidia About NVLink for Its Own AI Server

Apple Inc. ( NASDAQ:AAPL ) is developing an enterprise AI server built around its own M8 Ultra chips for a 2029 launch, and has held talks with Nvidia Corp. ( NASDAQ:NVDA ) about using its NVLink Fusion interconnect to link those chips, The Information reported . Apple shares were up 0.49% and Nvidia shares 2.12% intraday.
Warning! GuruFocus has detected 6 Warning Sign with BAC.
The server would come in two configurations, one pairing two M8 Ultra chips and one pairing four, aimed at AI developers, businesses and governments. Some Apple engineers consider NVLink Fusion the best available connectivity option. The platform bundles switches, chiplets and software so chips from different vendors can communicate at high speed, and Nvidia earns roughly a fifth of its data center revenue from networking gear.
Mac was Apple's fastest-growing segment last quarter, with revenue up nearly 29% to $10.4 billion on unexpected demand from AI developers buying Mac mini and Mac Studio units, creating supply shortages. New chief executive John Ternus backed the server project when it started about a year ago, while running hardware engineering.

### Article 279 · 2026-09-16 · gurufocus.com
Nvidia Gains 1.4% as Flexible Power Targets AI's Grid Bottleneck

Nvidia ( NASDAQ:NVDA ), the AI-accelerator and data-center platform leader, launched the AI Energy Management Alliance with Google and Emerald AI on Wednesday, putting one of AI's biggest physical bottleneckselectricitysquarely in its sights. Nvidia shares gained approximately 0.9% to $214.08 . The initiative is not about selling another GPU today. It is about making sure the power grid can handle the mountains of GPUs customers want to deploy tomorrow.
The alliance wants data centers to behave more like flexible grid assets, shifting computing workloads, tapping stored energy or cutting electricity demand when the grid comes under pressure. Its framework is designed to measure how quickly facilities can respond, how long that flexibility lasts, how predictable it is and how operators behave during emergencies. If utilities and grid operators can trust those commitments, hyperscale projects could face fewer interconnection roadblocks and potentially require less incremental infrastructure before coming online.
That matters enormously for Nvidia because power availability is increasingly becoming a constraint on AI infrastructure deployment. Data-center revenue reached $89 billion , roughly 92.5% of Nvidia's latest quarterly sales, so delays in energizing new facilities can eventually become delays in installing Nvidia systems. GuruFocus gives Nvidia a GF Score of 95 out of 100, with especially strong readings for profitability, growth and financial strength, while GF Value remains the weakest component. That picture captures the investment setup neatly: Nvidia's operating engine remains exceptionally strong, but valuation still leaves investors demanding continued execution.

### Article 280 · 2026-09-16 · crusoe.ai
Crusoe's MLPerf Inference v6.1 results on NVIDIA GB200 NVL72

Crusoe's MLPerf Inference v6.1 results on NVIDIA GB200 NVL72
Crusoe's debut MLPerf Inference v6.1 submission benchmarked gpt-oss-120b and Qwen3-235B on NVIDIA GB200 NVL72 on Crusoe Cloud. They run on the same Managed Kubernetes and Slurm infrastructure customers use.
Today, MLCommons published the MLPerf® Inference v6.1 results, and with them Crusoe's first-ever MLPerf submission. We submitted results for gpt-oss-120b and Qwen3-VL-235B-A22B running on NVIDIA GB200 NVL72 on Crusoe Cloud, validating that the NVIDIA Accelerated Computing Platform, from NVIDIA CUDA® and NVIDIA TensorRT-LLM through NVIDIA Dynamo, NVIDIA NVLink™, and NVIDIA Quantum InfiniBand , runs exactly as our customers consume it.
Three results matter more than the raw numbers:
We exceeded NVIDIA's published single-node reference for Qwen3-VL-235B-A22B. NVIDIA's guidance for a 4x GB200 NVL72 node was roughly 56 samples/s Offline and 46 queries/s Server. Our submission measured 58.40 and 49.70. Our gpt-oss-120b submission is likewise the highest per-GPU GB200 NVL72 result in the closed division, at roughly 12,700 tokens per second per GPU.
Scaling from one node to four was effectively linear. Qwen3-VL Server throughput at 16 GPUs came in at 4.00x the 4-GPU result, and Offline landed within a fraction of a percent of the linear extrapolation. Rack-scale NVLink and NVIDIA Quantum InfiniBand make the fabric a non-factor for this workload shape. ‍
A topology tuning pass produced a ~2.5x Interactive throughput gain on identical hardware. By rebalancing the prefill:decode GPU split in a disaggregated NVIDIA Dynamo deployment from 75:25 to 50:50, Qwen3-VL Interactive throughput on 16 GPUs went from 15.85 to 39.85 queries/s. Same GPUs, same fabric, dramatically more serving capacity.
This post covers the results, the methodology behind them, and the engineering it took to get a multi-node prefill/decode-disaggregated serving topology through MLPerf's closed-division rules. A companion post covers our AMD MI355X submission.
MLPerf Inference v6.1 results on NVIDIA GB200 NVL72
All results are MLPerf Inference v6.1, closed division, on NVIDIA GB200 NVL72 on Crusoe Cloud (gb200-186gb-nvl-ib.4x instances, 4x GB200 per node, 1200W TGP per GPU).
gpt-oss-120b works out to roughly 12,700 tokens per second per GPU in both scenarios. MLPerf measures latency-bounded throughput in the Server scenario, so the interesting number is the ratio: our Server result lands within 0.6% of Offline. The latency SLA costs almost nothing on this platform. The same node that maxes batch throughput also holds p99 time-to-first-token and time-per-output-token under the v6.1 limits, which is the property that matters when sizing a production deployment.
All runs cleared closed-division accuracy: gpt-oss-120b at 83.69% exact-match (Offline) and 83.64% (Server) against an 82.30% floor, and Qwen3-VL between 78.56% and 78.82% hierarchical F1 against a 78.24% floor. gpt-oss-120b passed compliance audits TEST07 and TEST09.
Published results are available in the MLCommons MLPerf Inference v6.1 closed-division results.
Prefill/decode disaggregation: a 2.5x gain from topology alone
The 16-GPU Qwen3-VL deployment is the most architecturally interesting system we submitted. Rather than running 4 independent node-sized replicas, we deployed NVIDIA Dynamo in a prefill/decode-disaggregated topology: prefill workers (TP2) handle prompt processing, decode workers (TP1) handle token generation, and KV cache moves between them over NVIDIA Inference Xfer Library (NIXL).
Disaggregation matters because prefill and decode have opposite hardware appetites. Prefill is compute-bound and parallelizes across long prompts; decode is memory-bandwidth-bound and wants maximum batch residency. Serving both phases on the same GPUs forces a compromise; splitting them lets each pool run at its natural operating point. This is the same architecture behind large-scale production inference systems, and MLPerf's Interactive scenario, with its tight p99 latency limits, is precisely where it pays off.
Our first Interactive run used a 75:25 prefill:decode GPU split and measured 15.85 queries/s. Profiling showed decode was the bottleneck: prefill GPUs finished prompts faster than decode GPUs could stream tokens under the p99 limit. Rebalancing to 50:50 and binary-searching the sustainable query rate brought the submission to 39.85 queries/s, a roughly 2.5x improvement with zero hardware changes. The final topology was 6 prefill workers across 3 nodes and 4 decode workers on the fourth. To date, that result is the highest Qwen3-VL Interactive score in the round on the GB200 NVL72 system.
Two takeaways for anyone deploying disaggregated serving:
The prefill:decode ratio is workload-dependent and worth sweeping. The optimal split for a latency-bound Interactive workload was very different from the throughput-oriented defaults.
Scaling was linear. Offline throughput at 4 nodes (230.09 samples/s) matched the linear extrapolation from the 3-node run (172.35 predicted 229.8). Server hit 198.94 against a target of 200 on the first attempt after setup fixes, 99.5% of the configured rate.
We deliberately ran these benchmarks on the orchestration services that power our customers’ workloads today.
The single-node gpt-oss-120b runs executed on Crusoe Managed Kubernetes , the same platform as our other MLPerf work, with the same observability through Crusoe Managed Metrics. The multi-node Qwen3-VL runs executed on a Crusoe Managed Slurm cluster using NVIDIA's sflow launcher, with the model repository on VAST-backed shared NFS and staged to per-node NVMe so the storage hot path never crossed the network during timed runs.
This submission demonstrates the NVIDIA Accelerated Computing Platform on Crusoe at two scales: a single GB200 node exceeding published reference throughput, and a multi-node disaggregated topology scaling linearly across NVLink and NVIDIA Quantum InfiniBand. Every Crusoe cluster is validated end to end during bring-up before a customer touches it, and MLPerf is one instrument in that process.
We are continuing to work with NVIDIA on performance and software co-design across GB200 NVL72, GB300 NVL72, and beyond, and we will keep publishing results for both Inference and Training workloads.
Ready to serve at this scale? Talk to our team about running inference on NVIDIA GB200 NVL72 on Crusoe Cloud .

### Article 281 · 2026-09-16 · gurufocus.com
Nvidia Stock Rises as Meta CEO Rejects AI Slowdown Calls

Nvidia ( NASDAQ:NVDA ) shares climbed 1.5% on Wednesday as Meta CEO Mark Zuckerberg pushed back against proposals for a broad slowdown in artificial intelligence development, easing some concerns about potential restrictions on the technology sector.
Zuckerberg said existing market incentives and legal exposure can encourage AI companies to address safety concerns without requiring a mandated reduction in development, according to a Wednesday report.
His comments put Meta alongside Nvidia CEO Jensen Huang, who has also opposed measures that could restrict the pace of AI progress. The debate follows calls from executives at OpenAI and Anthropic for greater caution as AI capabilities advance.
For Nvidia, the discussion matters because tighter rules could affect demand for advanced chips and the infrastructure needed to train and operate AI models. Investors have been monitoring whether technology companies will maintain large-scale spending on data centers and computing capacity.
The latest market reaction suggests Zuckerberg's position may have reduced some near-term concern over regulatory constraints, although the broader debate around AI safety and development remains unresolved.

### Article 282 · 2026-09-16 · finance.yahoo.com
AI will not wipe out humanity, Nvidia-backed tech CEO declares

It's somewhat reassuring to see prominent tech figures pushing back against the notion that AI will wipe out the human race.
"There is NO realistic scenario where AI wipes out all of humanity," Recursive CEO and well-respected tech entrepreneur Richard Socher said in an X post on Wednesday.
Socher is also the co-founder of AI-powered search engine You.com , which has raised capital from prominent names including Nvidia ( NVDA ), Salesforce ( CRM ) Ventures, and DuckDuckGo. You.com currently has an estimated valuation of more than $1.5 billion.
Socher added, "I've talked to many AI safety experts about existential risks. Some of the 'experts' are just phenomenal sci-fi authors. There are also real researchers working on realistic risks. They point out real and likely harms, and I'm explicitly not arguing that there could be no such harm. We need to take these seriously. However, whenever I ask for an actual detailed scenario that would kill every single human, i.e. extinction, it usually starts and ends with 'just look at current progress and use your imagination'. No science, no scenario planning, just handwaving probabilities without data, based on gut feelings, often little expertise, sometimes real expertise combined with a huge amount of technological optimism turned into fear and then trying to quantify it post hoc."
Within the course of three days, Anthropic ( ANTH.PVT ) CEO Dario Amodei and OpenAI ( OPAI.PVT ) CEO Sam Altman have managed to scare the hell out of the human race with the powerful technology they created and pushed their teams of pioneering supercoders to supercharge.
"Over the last few months, I have become convinced that fully addressing the risks requires even more prudence — not just investing in risk prevention, but pacing the rate of capabilities advancement so that risk prevention has time to keep up," Amodei stated in a 3,800-word essay on Saturday. "We must slow the pace at which we improve the capabilities of A.I. models. Progress will still seem fast, and we must make wise use of the time we gain."
Amodei doubled down on his comments at Salesforce's annual Dreamforce event on Tuesday afternoon.
Altman said right after Amodei's weekend post that he agreed with his rival.
He then followed that up on Monday with a dark X post of his own.
"There are two ways AI progress could go very badly, and that we must avoid. First, we could lose control of the future to AI. This is unacceptable; we are unapologetically on Team Humanity, and AI must always serve people. To ensure that, we need ways to ensure that alignment and safety techniques stay ahead of progress in model capabilities," Altman wrote.
"Second, we could end up in a world with too much concentration of power," he continued. "If an extraordinarily powerful AI is used by one person or company to impress their worldview onto everyone else, the results could be extremely dystopian. Avoiding these two threats requires walking a narrow middle path; for example, one country could gain too much power. Another example is one lab ending up with too much power."
Okta ( OKTA ) co-founder and CEO Todd McKinnon said dire predictions on AI make sense but are on the extreme side of the equation.
"If there's going to be a betting market on how the human race would be extinct, I'm not sure AI would be in the top 50, but it does get headlines, and people are very excited about it," he said on Yahoo Finance's Opening Bid (video above). "But the reality is that, like every new technology, there's a lot of peril and there's a lot of great things that could go right about it. And we have to make sure we balance them out together and make progress going forward."

### Article 283 · 2026-09-16 · fool.com
Is It Too Late to Buy Nvidia Stock?

Although it briefly lost its crown to Apple ( AAPL -1.19% ) in July, chipmaker Nvidia ( NVDA +2.55% ) is once again reigning supreme as the largest company in the world by market capitalization.
It's also the only company in the world currently worth over $5 trillion.
But Nvidia has had a bit of a rocky year . It's only barely keeping pace with the S&P 500 in terms of growth. Both are up 17.6% over the past year. Is that a sign that Nvidia's high-growth days are behind it?
In other words, is it too late to buy Nvidia stock? Here's what investors need to know.
Massive companies can still grow further
Just because a company is the biggest of the big doesn't necessarily mean it's done growing , or even done growing quickly.
Apple, the only current challenger for Nvidia's largest-company crown, is a great example of this. In 2018, it became the first U.S. company to reach a $1 trillion valuation, and investors questioned how much higher its price could possibly go.
As it turns out, quite a bit higher. It took just two years for Apple to double in size and reach a $2 trillion valuation in 2020. Since then, it's more than doubled again, with a $4.9 trillion valuation today.
Imagine if you'd sold your Apple shares just eight years ago because you thought it couldn't go much higher. You'd have missed out on massive, market-crushing gains.
Of course, for every Apple and Nvidia that have kept growing, even at a massive size, there's a company that's seen its growth stall. And the larger a company gets, the harder it can be for it to maintain strong growth . Eventually, it can simply run out of addressable market.
The good news is that this doesn't seem to be happening to Nvidia. Over the last five years, Nvidia's revenue has grown 1,150%, and its net income has soared 2,250%. Meanwhile, its stock is up "just" 821%.
That means that from a valuation perspective, Nvidia's shares are much cheaper than they were five years ago. Its current trailing price-to-earnings (P/E) ratio of 26.7 is at a five-year low. It's also much lower than Apple's trailing P/E of 38.2 (lower is better).
Of course, if Apple were expected to grow faster than Nvidia, it's not surprising that investors would be willing to pay more of a premium for Apple shares. But Apple's revenue is only up 27.4% over the past five years, and its net income has only gone up 36.2%.
That probably means investors are worried about Nvidia's current revenue and profit streams, which are reliant on sustained AI infrastructure spending .
There are no signs that the current AI spending boom is fizzling, but even if it did, Nvidia's top-of-the-line GPUs would likely find a market powering the next big technological advance .
All things considered, Nvidia still looks very much like a company worth buying for the long term.
By John Bromels – Sep 16, 2026 at 6:15AM EST

### Article 284 · 2026-09-16 · finance.yahoo.com
If You'd Put $1,000 Into Nvidia Stock 20 Years Ago, Here's What You'd Have Today

Nvidia ( NVDA ) cemented its place as the market's favorite bet on artificial intelligence (AI) three years ago and it shows no signs of letting up.
Indeed, the company has become so important to investors that Nvidia's earnings report helps set the tone for trading for the broader market.
To recap: OpenAI's ChatGPT kicked off the AI frenzy at the end of 2022. Seemingly insatiable demand from AI hyperscalers for Nvidia's graphics processing units (GPUs) propelled NVDA stock past $1 trillion in market capitalization midway through 2023.
It took only about eight months for yet another blowout quarterly earnings report to push Nvidia stock past the $2 trillion mark.
Cut to early 2024, when Nvidia's over-the-top first-quarter earnings — plus a NVDA stock split and a dividend hike — pushed its market cap past $3 trillion.
As of this writing, Nvidia, which replaced Intel ( INTC ) in the Dow Jones Industrial Average in late 2024, is the world's largest publicly traded company. Indeed, it became the first company to top $4 trillion in market cap in mid-2025. Today, it's the only member of the $5 trillion market-cap club.
But then, long-time shareholders should be used to such outsized rewards and risks by now.
That's because volatility has always been the price of admission to this long-time market beater. True, Nvidia, a highly cyclical semiconductor stock , has vastly outperformed the broader market since going public at the end of the last century.
Quite naturally, it has done so with several vertiginous ups and downs along the way.
During the tech bear market of 2021-2022, shares lost two-thirds of their value in just 11 months. NVDA rebounded by more than tripling in 2023, versus a 24% gain for the S&P 500.
And as for 2024? Nvidia stock gained more than 170% compared to a 25% rise in the broader market. The stock once again led the broader market in 2025, albeit by "only" 21 percentage points.
Nvidia's market-beating ways go much farther back than most folks might know, however. In fact, few stocks have done more for investors over the past few decades than Nvidia.
From its initial public offering at $12 a share in January 1999 through December 2020, NVDA stock created $309.4 billion in shareholder wealth, according to an analysis by Hendrik Bessembinder, a finance professor at the W.P. Carey School of Business at Arizona State University.
Indeed, per Bessembinder's findings, which account for a stock's increase in market value adjusted for cash flows in and out of the business and other factors, Nvidia was one of the 30 best stocks over that 30-year time frame.
Looked at another way, over its life as a publicly traded company, Nvidia stock generated an annualized total return of 37%. The S&P 500, with dividends reinvested, returned an annualized 10.8% over the same period.
Importantly, most of the shareholder wealth generated by Nvidia came over just the past few years. That's because back in the day, the primary market for Nvidia's chips consisted of PC and console video game enthusiasts.
Happily for Nvidia, it just so happens that the company's powerful GPUs and related intellectual property are indispensable to the fields of artificial intelligence , professional visualization, cryptocurrency mining and more.
As noted above, NVDA processors are in demand for use in data centers — and especially data centers that power generative AI. Indeed, the company is struggling to keep up with orders from hyperscalers such as Microsoft ( MSFT ), Meta Platforms ( META ), Amazon.com ( AMZN ) and Alphabet ( GOOGL ).
Few blue chip stocks offer so much exposure to so many emerging endeavors, which helps explain NVDA stock's amazing returns over the longer haul. AI has been NVDA's afterburner.
But as remarkable as the company's business may be, it doesn't quite get to the heart of what NVDA stock has meant to long-term shareholders and their brokerage statements. For that, consider the following facts about Nvidia stock.
Over the past two decades, Nvidia stock generated an annualized total return (price change plus reinvested dividends) of 36%. The S&P 500, by comparison, generated an annualized total return of 11.3% over the same span.
What does that mean in dollar terms? Have a look at the above chart and you'll see that if you invested $1,000 in Nvidia stock 20 years ago, it would today be worth more than $475,000. The same amount invested in an S&P 500 index fund would theoretically be worth not quite $8,500 today.
As for adding to NVDA at current levels, the Street remains bullish even after the stock's incredible run. Indeed, NVDA rates as a top Dow Jones stock to buy.
Of the 61 analysts issuing opinions on Nvidia stock surveyed by S&P Global Market Intelligence , 48 rate it at Strong Buy, 10 say Buy, two call it a Hold and one has it at Strong Sell.
That works out to a rare consensus recommendation of Strong Buy. Indeed, Nvidia ranks among analysts' top S&P 500 stocks to buy now .
"NVDA now provides full rack AI systems," notes the analyst, who rates NVDA at Outperform (the equivalent of Buy.) "We see several structural tailwinds driving sustained outsized top-line growth in high-performance gaming, datacenter/AI and autonomous driving vehicles."
Just remember that NVDA is ultimately a chip company, and the semiconductor industry is cyclical. As exciting as the AI build-out may be, Nvidia's growth prospects could one day change.

### Article 285 · 2026-09-16 · zacks.com
Zacks Industry Outlook NVIDIA, Texas, STMicroelectronics and Intel

Chicago, IL – September 16, 2026 – Today, Zacks Equity as NVIDIA Corporation NVDA, Texas Instruments TXN, Intel INTC and STMicroelectronics STM.
commentary/2989797/buy-ti-and-
Companies in the Semiconductor – General industry are at the forefront of the ongoing technological revolution based on HPC, AI, electrified and automated driving, IoT and other technologies. The semiconductors they produce enable the cloud to function and help analyze data into actionable insights that can be used by companies to operate more efficiently. AI and data-center infrastructure are currently the industry's biggest growth drivers, while automotive and industrial applications provide important additional opportunities. Therefore, the long-term outlook can only be considered bright.
In the immediate future, however, there could be some challenges. While geopolitical instability and the arms race among nations may sound like positive drivers for some, actual wars disrupt supply chains, delay deliveries and drive up prices. U.S. tariffs could exacerbate inflation in end products using semiconductors and potentially disrupt trade, resulting in more of the same challenges. Supply-chain adjustments, export restrictions and elevated memory prices could also create near-term pressures.
NVIDIA Corporation is at the center of the AI infrastructure buildout, with its GPUs, networking products and accelerated-computing platforms benefiting from rapidly expanding AI workloads. Texas Instruments offers exposure to the broader semiconductor cycle through its analog and embedded-processing products, with industrial, automotive and data-center demand providing important growth opportunities. TXN also benefits from long product lifecycles, sticky customer relationships and its ongoing capacity investment cycle. Our bets are therefore on these two stocks.
WSTS expects global semiconductor sales to grow 89.9% in 2026 to $1.51 trillion, highlighting the extraordinary strength of the current cycle. The increase is being driven primarily by memory and AI infrastructure, but strong growth in logic, microprocessors and analog also points to broader semiconductor demand. The regional outlook is similarly strong, with the Americas expected to lead growth in 2026. The broad-based expansion is also supportive of semiconductor demand across the industry's major end markets, including AI and data centers, automotive and industrial applications.
IDC also expects exceptional growth in 2026, with semiconductor revenue rising 52.8%, driven overwhelmingly by AI infrastructure investment. Memory, particularly DRAM and HBM, is the primary driver. IDC estimates that by 2030, data-center semiconductors will account for nearly half of the total semiconductor market, highlighting the scale and longevity of AI infrastructure demand. At the same time, IDC notes margin pressure, supply-allocation challenges and macroeconomic headwinds in several non-memory end markets.
Gartner expects semiconductor revenue to grow 92% in 2026 to $1.56 trillion. Memory is again the biggest contributor, with DRAM and NAND benefiting from severe supply tightness and price increases. The AI-driven diversion of memory capacity, along with sharply higher memory prices, is creating supply constraints and component mismatches in non-AI markets.
Gartner expects memory supply to remain tight in 2027 as AI infrastructure continues to increase memory consumption, potentially limiting the pace of growth in automotive, industrial and other non-AI applications. The underlying strength of automotive and industrial semiconductor demand remains, however, as it is driven by several secular trends, including electrification, vehicle automation, factory automation, robotics, machine vision and rising semiconductor content.
The U.S. government's target of reducing dependence on China, and onshoring projects with national security implications are also shaping the progress of this industry.
The companies grouped under the Semiconductor – General industry develop and supply a broad range of integrated and discrete semiconductor products, including microprocessors, graphics processors, embedded processors, chipsets, connectivity solutions, digital light processing (DLP) products and analog semiconductors. These products serve diverse end markets, including data centers, automotive, industrial, consumer electronics and communications. The industry includes companies such as NVIDIA, Texas Instruments, Intel and STMicroelectronics .
< > Artificial intelligence is the single biggest driver of the semiconductor industry, given the transformation it is bringing in efficiency, cost-effectiveness, automation, safety, environmental benefits and other areas. AI has become an imperative for effective competition across industries, creating enormous demand for the infrastructure needed to develop and deploy AI. This infrastructure requires thousands of semiconductors across GPUs, CPUs, networking, memory, power management and other components. Technology companies are building their own AI capabilities where possible and buying from specialized providers where it makes sense. Moreover, as AI adoption expands, its infrastructure requirements increase further. In this backdrop, data-intensive applications, advances in machine learning and growing AI adoption across data centers, automotive, industrial automation, healthcare, financial services and other markets are major drivers. The resulting semiconductor demand is likely to remain strong for years to come. There is significant opportunity in the automotive and industrial markets . In fact, these two end markets are shaping up to be its strongest growth drivers after AI. The automotive opportunity is driven largely by electrification (which consumes a large number of chips in things like power management, battery management systems, power conversion systems, charging infrastructure and motor control electronics). Strong growth is also coming from vehicle automation, including autonomous driving and increasingly sophisticated automotive computing. The industrial opportunity is mainly in factory automation, where robots, machine vision systems, production lines and real time monitoring systems are consuming a growing number of embedded processors, analog chips, connectivity chips, sensors and power semiconductors. Current geopolitics has mixed implications for growth . Geopolitical tensions are adding a dimension to semiconductor demand, as countries increasingly adopt the latest technology in defense, infrastructure and other critical applications. As defense spending accelerates the world over, particularly on fighter planes and unmanned aerial vehicles currently being used in military operations, demand for sophisticated underlying electronics is likely to increase. Tachnavio estimates that semiconductors used in the military and aerospace market will grow at a 6% CAGR through 2029. However, war is not conducive to trade overall because of the disruptions in trade routes, uncertainty in demand and price escalation in key commodities. There may also be export restrictions on products being sold to an enemy country. Therefore, ongoing tensions around the world could dampen demand, raise prices or cause other disruptions in the larger computing, consumer, data center, auto and industrial markets. U.S.-China tensions remain elevated, while there is considerable concern that many of the world's most important leading-edge chips are currently made in Taiwan, considering the heightened cross-strait tensions. Since this has national security implications, there is an ongoing drive to onshore or nearshore manufacturing. The CHIPS Act is facilitating the process. Macro concerns remain significant . Elevated inflation, tariffs and geopolitical tensions are adding to costs and weighing on consumer confidence. U.S. consumer spending has also moderated, while industrial and other cyclical semiconductor markets remain sensitive to any broader economic slowdown. These factors could temper demand for semiconductors used in consumer electronics, automotive and industrial applications, although AI and data-center demand remains a strong industry growth driver. Semiconductor supply chains are adjusting . Efficient semiconductor supply chains based on the just-in-time model are no longer prioritized, as the cost advantages they enable are increasingly balanced against the need for resilience in times of huge demand and unforeseen disruptions. Players continue to adjust for external disruptions, such as COVID, wars and tariffs. This, along with other factors, such as the U.S.-imposed restraints on dealing with China, has led semiconductor companies to diversify their supply chains and in some cases, reduce their dependence on the country. This is an ongoing process that will take several years. Some companies are also building inventory so disruptions from geopolitical and other issues may be limited.Semiconductor-General Industry is a stock group within the broader Zacks Computer and Technology Sector. It carries a Zacks Industry Rank of #23, which places it in the top 9% of nearly 250 Zacks-classified industries.
The group's Zacks Industry Rank, which is the average of the Zacks Rank of all the member stocks, indicates that near-term prospects are improving. Our research shows that the top 50% of the Zacks-ranked industries outperforms the bottom 50% by a factor of 2 to 1.
An industry's positioning in the top 50% of Zacks-ranked industries is normally because the earnings outlook for the constituent companies in aggregate is relatively strong. The opposite is true for stocks in the bottom 50% of industries. In this case, the aggregate earnings estimate for 2026 has increased steadily over the past year and is up 51.4% from the year-ago level while the aggregate earnings estimate for 2027 is up 108.8%.
Before we present a few stocks that you may want to consider for your portfolio, let's take a look at the industry's recent stock-market performance and valuation picture.
Tracking the performance of the Zacks Semiconductor – General Industry over the past year shows that the industry has traded at a premium to both the broader Zacks Computer and Technology Sector and the S&P 500 index through most of 2026 and more consistently so since March 2026.
The industry has gained 30% over the past year. The broader technology sector gained 23% while the S&P 500 index gained 17%.
On the basis of forward 12-month price-to-earnings (P/E) ratio, we see that the industry is currently trading at a 18.32X multiple, which is its lowest point over the past year. It is also trading at a 7.7% discount to the S&P 500's 19.84X and an 11% discount to the broader sector's 20.59X. The industry has traded between a low of 18.32X, a high of 37.34X and a median level of 25.04X over the past year. The industry looks somewhat undervalued at these levels.
Macro and geopolitics notwithstanding, the industry stands to benefit from stable or declining interest rates, which can improve the attractiveness of risky assets and support investment. Several of the technology heavyweights in this industry are the core suppliers to the AI mega cycle we are seeing now, so we remain optimistic over the long run. Considering the attractive valuation, we think this is a good time to get into play. We are picking NVIDIA Corporation and Texas Instruments:
NVIDIA Corporation : Headquartered in Santa Clara, California, NVIDIA is a key provider of computing infrastructure, including GPUs, AI accelerators and networking technologies for artificial intelligence and accelerated computing in data centers, as well as gaming, professional visualization and automotive applications.
The industry backdrop remains highly favorable for NVIDIA as demand for AI-processing semiconductors continues to expand rapidly. Gartner expects revenue from AI-processing semiconductors to grow at a 26.8% compound annual growth rate (CAGR) through 2030, driven by continued spending on AI infrastructure and expanding workloads. This provides NVIDIA with a large and growing addressable market for its GPUs and accelerated-computing platforms, extending the company's current growth trajectory.
NVIDIA's second-quarter fiscal 2027 revenue surged 106% year over year and 18% sequentially, while Data Center revenue jumped 117% year over year and 18% sequentially to $89 billion. Management said AI demand is accelerating, with the buildout expanding beyond the major hyperscalers to multiple frontier AI labs, startups, the open-model ecosystem, enterprises, sovereign AI initiatives and physical AI. Its expanded AWS partnership, which calls for 2 million additional NVIDIA GPUs to be deployed in 2027-28, further underscores the scale and longevity of AI infrastructure investment.
NVIDIA is expanding its ability to meet surging AI demand by securing additional wafer, advanced packaging and high-bandwidth memory capacity through key manufacturing partners. It works closely with TSMC and other foundries to increase production of its latest GPUs and CPUs, while partnerships with memory suppliers such as SK hynix support HBM availability. It has more than 150 supply chain ecosystem partners in Taiwan.
NVIDIA is also securing key components well ahead of anticipated demand, helping support the ramp of its Blackwell and Rubin platforms. Wistron is an important partner expanding U.S. production. Management has said that more than 350 factories across 30 countries are ramping NVIDIA's Vera Rubin platform. This broad manufacturing network and long-term component commitments enable NVIDIA to scale Blackwell and Rubin systems as demand continues to exceed available supply.
On the downside, rising memory prices are expected to weigh on NVIDIA's profitability, with gross margin projected to decline from 75% in the second quarter of fiscal 2027 to 71%-72% in the fourth quarter before recovering to 72%-73% in fiscal 2028 as price increases take effect. Supply constraints across wafers, advanced packaging, HBM and other components remain a near-term constraint on NVIDIA's ability to fully meet strong customer demand. Competition from AMD and other chipmakers, along with hyperscalers developing custom AI accelerators, could pressure NVIDIA's share of AI workloads, although the company is also positioning itself in the custom silicon market through its partnership with MediaTek.
In the last 30 days, the Zacks Consensus Estimate for 2027 (ending January) increased by 33 cents (3.7%) while the estimate for 2028 increased $2.76 (22%). Analysts currently expect revenue and earnings to grow a respective 88% and 93.5% this year followed by a respective 65.5% and 66% in the next.
Texas Instruments, Inc. : Dallas, Texas-based Texas Instruments is an original equipment manufacturer of analog and embedded processing chips for industrial, automotive, communications, consumer, data center and other applications.
While the US is its largest market, followed by Europe, it's worth noting that China still accounts for roughly a fifth of its revenues, which could be at increasing risk given the current geopolitics.
As the pandemic and geopolitics impacted the chip supply chain, and the government incentivized American companies to reshore manufacturing, TI changed its manufacturing strategy from one that opportunistically used external capacity to one on the path to source more than 95% of its wafers internally, with more than 80% on 300mm, by 2030.
To this end, it expanded its internal manufacturing capacity in 2024, with tool installations completed and production currently ramping at two 300mm wafer fabs in Richardson, Texas, one in Sherman, Texas, and one in Lehi, Utah. Another Sherman fab and a second Lehi fab are under construction.
The company is a beneficiary of an investment tax credit of up to 35% related to some of its investments in U.S. semiconductor manufacturing (expected to continue on qualified investments up to 2034). It also has an agreement with the Department of Commerce to receive direct funding of up to $1.6 billion for the two large-scale 300mm wafer fabs in Sherman, Texas, as well as the under-construction Lehi fab in Utah.
As of the end of the second quarter, TI had received $630 million of the CHIPS Act funding. The company agreed to spend more than $18 billion in U.S. manufacturing, particularly on 300mm wafer capacity by the end of 2029. With its major capacity expansion nearing completion, TI expects 2026 capital expenditures of $2-3 billion, below the elevated spending levels of recent years.
As may be expected, capacity expansion initially has a negative impact on margins, as capacity can only be filled over time. Therefore, underutilization can weigh on margins during the ramp period . If there are in addition any end market issues, such as supply chain glitches in the automotive market or cyclicality in the industrial market, the impact is compounded.
It is encouraging to note that TI has also gradually increased the share of direct sales to customers, which improves insight into their projects and timelines, thus driving sales, customer penetration and market share gains. Customer relationships also tend to be sticky because TI primarily supplies analog and embedded products, which often have long product lives and remain designed into applications for years.
In 2025, more than 80% of business came from direct customers. Since TI has a huge portfolio of thousands of products and builds capacity years in advance to ensure stable supplies even when there is uncertainty in the market, it is positioned to attract and retain customers, grow its share of content in each design and gradually capture a growing share of the fragmented automotive and industrial markets.
Industrial and automotive each accounted for around 33% of revenue in 2025, underscoring the importance of these markets and the opportunity from growing electronic content. Data center accounted for around 9%. Strength is currently broad-based, with second-quarter growth led by industrial, data center and automotive: industrial revenue increased around 30% year over year, automotive grew in the mid-teens and data center revenue doubled.
In the last 60 days, the Zacks Consensus Estimate for 2026 increased by 79 cents (10.3%) while the estimate for 2027 increased 99 cents (11.1%). Analysts currently expect revenue and earnings to grow a respective 22.7% and 55.1% in 2026 followed by a respective 12% and 16.8% in 2027.

### Article 286 · 2026-09-17 · NVIDIA Corporation
GFN Thursday: ‘Aniimo’ on GeForce NOW | NVIDIA Blog

A new creature-catching adventure is ready to stream from the cloud this week. Pawprint Studio’s Aniimo arrives on GeForce NOW at launch, inviting gamers to explore the vibrant continent of Idyll across supported devices.
Also this week, 007 First Light receives a path-tracing update on GeForce NOW, alongside a smashing limited-time Deluxe Edition sale on Steam and Epic Games Store .
Gaijin Network’s fractured-multiverse action game Active Matter and Annapurna Interactive’s acclaimed space mystery Outer Wilds are also among 11 new titles joining the cloud this week.
The path to Idyll begins now. Aniimo is a free-to-play, open-world creature-catching role-playing game where every creature encountered can become a companion. Catch Aniimo with Aniipods, then Twine with them to take on their form and use unique skills to solve puzzles, win battles and overcome challenges.
Glide, dive and burrow across Idyll, then return to a personal RV to build a warm, interactive Homeland alongside Aniimo companions. Stream Aniimo on a Steam Deck , in the newly supported Firefox browser and across any other supported devices — without waiting through its 45GB download or making room in local storage. There’s always room in the Homeland for one more Aniimo.
In the critically acclaimed, multimillion-selling 007 First Light , follow James Bond as a young, resourceful and sometimes reckless recruit in MI6’s training program, and discover a reimagined origin story of the world’s most famous spy. Incorporating IO Interactive’s signature stealth gameplay with world-class Bond action, players can embark on missions in breathtaking locations around the globe, drive iconic vehicles and dive into a cinematic adventure in pursuit of a rogue agent who’s always one step ahead.
Path tracing has now been added to 007 First Light , introducing extra-detailed lighting, shadows and reflections, making its levels and set pieces even more cinematic, immersive and realistic. And NVIDIA DLSS 4.5 Ray Reconstruction ensures the fidelity, clarity and accuracy of these additions are at their absolute best.
Ultimate members can stream with GeForce RTX 5080-class performance, with up to 5K high dynamic range and cinematic-quality streaming. DLSS 4.5 Super Resolution and Dynamic Frame Generation accelerate frame rates and enhance image quality.
A limited-time opportunity awaits: the 007 First Light Deluxe Edition is on sale on Steam from Sept. 15-29 and on Epic Games Store from Sept. 3-18. The mission is on sale. The getaway car is in the cloud.
Gaijin’s Active Matter , a realistic military shooter set in a fractured multiverse, has launched on GeForce NOW. As an operative stuck in a time loop, join dangerous raids for loot or intense player vs. player battles.
Fight against rivals from other timelines, survive physics-breaking anomalies and try to stay alive. Harvest active matter, gather loot and extract to a safe place before the whole zone ceases to exist.
Ultimate members can take on each raid with GeForce RTX 5080-class performance in the cloud, delivering high frame rates, advanced graphics features and low latency across supported devices. The zone won’t wait — and neither does the next loop.
Outer Wilds joins the GeForce NOW library this week. As the newest recruit of Outer Wilds Ventures, search for answers across a strange, ever-changing solar system trapped in an endless time loop. Gamers can trace mysterious signals, decipher alien writing and discover hidden locations before an underground city is swallowed by sand or a planet crumbles beneath their feet.
Ready to take this week’s new games for a spin? Start with a day pass to try premium cloud gaming before committing to a membership. Even better, the cost of the day pass can be applied toward a first monthly membership — making it easy to level up with GeForce RTX-powered cloud gaming.

### Article 287 · 2026-09-17 · kron4.com
After AI scientist’s mysterious death in Palo Alto, family demands answers

(KRON) — Following a Nvidia artificial intelligence data scientist and researcher’s mysterious death in Palo Alto, his family is urging state and local authorities to dig for more clues to answer unsolved questions.
Irfan Al-Hussaini’s family are questioning cause of death findings from the Santa Clara County Medical Examiner’s Office, which ruled his death as a suicide. Family members and their attorney said circumstances surrounding his passing are suspicious.
Al-Hussaini worked for Nvidia, headquartered in Santa Clara. He was found unconscious in his Palo Alto apartment on July 22, someone called 911 at 10:22 a.m., and he was transported to a hospital, according to the petition. The AI senior data scientist died eight days later, on July 30. He was 32 years old.
His parents, sister, and the family’s attorney will gather outside Palo Alto City Hall Thursday to release new information about the case. The family is seeking an independent medical examiner to review forensic evidence. More than 14,000 supporters have signed a Change.org petition seeking a thorough investigation.
On July 22, Al-Hussaini gave a work presentation around 9 a.m., sent a Slack message to his manager at 10:02 a.m., someone called 911 at 10:22 a.m., and police responded to his home, a family spokesperson said.
The petition states, “According to his work colleagues … he had a presentation that morning ending around 9 am. Not too long after, he sent a text to the team group chat on Slack at 10:02 am saying that ‘Athi’ is not feeling well and he would take the rest of the day off. His colleagues mentioned they had no prior idea who ‘Athi’ was. Palo Alto police records show that a 911 call was made from Irfan’s address around 10:22 am.”
Palo Alto police officials allegedly told the family they treated the scene inside his Palo Alto home as a medical emergency, not a suspicious death scene.
The family’s attorney, former homicide prosecutor Tony Brass, said, “This is a family in agony, and they deserve answers. Right now, no one is taking responsibility. Not the police, not the Medical Examiner. Irfan died under serious, unresolved circumstances, and this family won’t stop asking the questions until someone finally conducts a full investigation as the law requires.”
A Palo Alto Police Department lieutenant told KRON4 that officers and firefighters responded to a report of a possible suicide.
The lieutenant wrote, “The adult male was treated by PAFD on scene and transported to a local hospital where he was later pronounced deceased. At this time the case is still under investigation pending the report from the medical examiner. We have received materials from the family and others, and our review and investigation is on-going. At this time neither the police department nor the medical examiner have identified any evidence that the death was the result of foul play.”
The Santa Clara County Medical Examiner’s Office did not respond to KRON4’s request for comment.
Al-Hussaini had recently been promoted at work and had many plans for the future, his family said.
Sarah Al-Hussaini wrote in a statement, “My brother Irfan was my best friend. It’s impossible to imagine that he took his own life when he was so full of plans for the future. We’ve been left with unanswered questions while the police department and Medical Examiner point fingers at each other.”
She added, “The circumstances are highly suspicious and raise serious questions about what happened.”
Al-Hussaini’s family hand-delivered a formal complaint to California Attorney General Rob Bonta’s office in Sacramento on September 8, asking for state investigators to look into the case.
Nexstar Media, Inc. is a leading, diversified media company that produces and distributes engaging local and national news, sports, and entertainment content across its television and digital platforms. The My Nexstar sign-in works across the Nexstar network—including The CW, NewsNation, The Hill, and more. Learn more at nexstar.tv/privacy-policy.

### Article 288 · 2026-09-17 · semafor.com
Nvidia’s case for taming AI agents

In this article:
The scaffolding that’s built around an AI model is just as important — if not more important — for AI safety than the model itself, Nvidia’s VP of agentic AI told Semafor.
“Rather than creating fear and FUD, let’s just secure it. We know how. We’ve done these things before,” Adel El Hallak said, referencing the acronym for fear, uncertainty and doubt.
El Hallak’s argument provides insight into the more technical case — as opposed to the geopolitical or ideological ones — for why AI doomerism may be overblown.
Nvidia CEO Jensen Huang has emerged as the most prominent tech figure voicing skepticism about recent claims by leaders like Anthropic CEO Dario Amodei that AI labs should slow down model development because the tech is quickly advancing beyond companies’ abilities to safeguard it. AI agents are central to that fear because they can take actions on their own, though regulation of agentic AI specifically is not discussed as much as is broad oversight of the models.
Huang this week rejected the notion that the industry has to choose between safety and speed, saying “you could definitely have both at the same time .”
El Hallak said advances in AI models make “harness engineering” more critical — a harness is the layer of instructions and code that governs how an AI agent operates in practice.
“If you’re training a capable agent, it is important that you don’t put a lion in and expect to be able to control it in a horse’s pen.”
He couldn’t comment on whether government regulation of the agentic layer is needed, but pointed to industry initiatives like the Open Secure AI Alliance as a venue for that kind of work, to figure out “at which part of the layer do we need to add more strengths and more guardrails and more safeguards.”
“The world’s not going to slow down.”
Some in Washington argue tech companies can’t be trusted to take up these issues on their own.
“ This is not an industry that can regulate itself ,” Democratic Rep. Pete Aguilar said this week, arguing for the need for federal industry-wide rules on AI safety.

### Article 289 · 2026-09-17 · gurufocus.com
Nvidia Stock Rises. Jensen Huang Sees Chip Sales Doubling in 2027

Nvidia ( NVDA ) shares climbed more than 2% Thursday as investors reacted to fresh comments from CEO Jensen Huang that chip sales could double in 2027, while new performance data for the company's next-generation Vera Rubin platform added to the AI trade.
The latest sales outlook came from Huang at an event in Scotland. He said Nvidia expects chip sales next year to be about twice this year's level, pointing to continued demand as businesses expand their use of artificial intelligence.
Nvidia also released preliminary MLPerf results on Sept. 16 showing Vera Rubin NVL72 delivering up to 3.7 times the inference throughput of the previous GB300 system on the Qwen3-VL test. Vera Rubin has entered full production, with shipments expected to begin this fall.
The broader market provided another lift. U.S. stocks rebounded Thursday as oil prices fell more than 2% and the 10-year Treasury yield eased, helping technology shares recover from recent pressure.

### Article 290 · 2026-09-17 · marketbeat.com
IonQ and NVIDIA Just Cracked a Major Quantum Computing Bottleneck

IonQ and NVIDIA Just Cracked a Major Quantum Computing Bottleneck
Interested in IonQ, Inc.? Here are five stocks we like better.
Researchers from Oak Ridge National Laboratory, IonQ, and NVIDIA used generative AI to design quantum circuits, cutting compilation runtime from 11 minutes to about 28 seconds.
IonQ shows triple-digit revenue growth and a debt-free balance sheet, but continues posting large net losses while trading well below its 52-week high.
NVIDIA's CUDA-Q platform and H200 GPU powered the benchmark, positioning the company as a profitable infrastructure bridge between classical and quantum computing.
For years, quantum computing hit a stubborn software wall. While quantum hardware promised to resolve complex computational bottlenecks, the time and cost of calibrating quantum circuits created a commercial barrier. When setting up a calculation takes longer than the calculation itself, the technology becomes much less practical.
A joint milestone achieved by Oak Ridge National Laboratory, IonQ, Inc. (NYSE: IONQ), and NVIDIA Corporation (NASDAQ: NVDA) tackles this operational dilemma. By training generative artificial intelligence models to design quantum circuits directly, researchers showed compilation runtimes can drop from minutes to seconds.
→ IonQ and NVIDIA Just Cracked a Major Quantum Computing Bottleneck
This engineering leap pulls quantum computing out of isolated academic testing and steps it closer to regular commercial use, offering technology investors two distinct ways to position for the growth of advanced computing.
Cracking the Code: A Quantum Compilation Breakthrough
On Sept. 16, 2026, researchers presented a study at IEEE Quantum Week in Toronto detailing how a generative AI model can write quantum optimization circuits directly.
→ 3 Luxury Consumer Brands to Watch in a Beaten-Down Sector
Hybrid quantum optimization breaks an intricate problem down into smaller pieces, solves each on quantum processors, and reassembles the results.
Historically, finding the correct circuit instructions for each segment required a repetitive trial-and-error method known as variational parameter tuning. Researchers had to run, measure, adjust, and rerun circuits dozens or hundreds of times. As quantum subproblems grew larger to yield higher-quality answers, the tuning tax escalated rapidly, driving up cloud computing costs and lengthening execution times.
→ 2 Stocks Breaking Out Post-FOMC With One Thing in Common
To eliminate this roadblock, the research team trained a transformer model on near-optimal circuit configurations. Rather than relying on repetitive guess-and-check loops, the AI model generated candidate circuits directly. Running on a single NVIDIA H200 graphics processing unit within the Oak Ridge Leadership Computing Facility's Defiant2 supercomputer, the framework evaluated a fixed set of candidate circuits, sidestepping the iterative bottleneck entirely.
The results show how much this approach could improve quantum computing at larger scales. When tested against a dense benchmark problem involving 100 decision variables, the traditional compilation method suffered severe latency. The circuit-finding runtime jumped from approximately 34 seconds on four qubits to more than 11 minutes on 12 qubits.
The generative AI model, by comparison, maintained an almost flat runtime of roughly 28 seconds across every qubit scale tested. At the same time, the quality of the generated answers roughly doubled as the number of quantum subproblems increased.
For enterprise clients, computational efficiency can directly translate to lower costs. Classical high-performance computing clusters consume substantial electricity and capital during endless compilation cycles.
Reducing the runtime to 28 seconds could make it easier for companies in logistics, financial modeling, and materials science to run optimization routines within more predictable budgets. This improvement could also support broader adoption across commercial cloud platforms, improving the economics of quantum-as-a-service (QCaaS).
This milestone arrives at an opportune moment for IonQ, Inc. IonQ continues expanding commercial access to its trapped-ion systems through major cloud partners, including Amazon's (NASDAQ: AMZN) AWS, Microsoft's (NASDAQ: MSFT) Azure, and Alphabet's (NASDAQ: GOOGL) Google Cloud.
Financial results highlight growing commercial traction. IonQ reported second-quarter revenue growth of roughly 286.7% year-over-year (YOY), with annual revenue reaching about $130.02 million. For the quarter ending in June, IonQ posted an earnings per share (EPS) loss of 33 cents, beating consensus expectations by 23 cents.
Operating in deep technology requires careful capital management. IonQ generated an annual net loss of approximately $510.38 million, reflecting ongoing research investments. Additionally, the federal government recently awarded $100 million grants under the CHIPS and Science Act to competitors D-Wave Quantum (NASDAQ: QBTS), Rigetti Computing (NASDAQ: RGTI), and Quantinuum (NASDAQ: QNT), while bypassing IonQ.
IonQ carries zero long-term debt and holds a current ratio of roughly 10.66, providing a multi-year cash cushion. While peer D-Wave posted second-quarter revenue of just $3.1 million, IonQ continues to scale its top line. IonQ currently trades near $40 and sits well below its 52-week peak of $84.64, while Wall Street maintains an average price target just over $67.
While pure-play quantum developers navigate long-term hardware roadmaps, NVIDIA is establishing itself as the infrastructure bridge connecting classical data centers to quantum processing units.
The Oak Ridge benchmark relied on NVIDIA's CUDA-Q open platform and cuQuantum software development kit running on an H200 accelerator. NVIDIA also introduced its CUDA-Q Logical software, designed to assist developers with multi-qubit error correction. By embedding its software layer across both trapped-ion and superconducting systems, NVIDIA captures enterprise compute demand regardless of which hardware architecture leads the market.
NVIDIA pairs this strategic positioning with reliable profitability. The company generates annual revenue of around $215.94 billion, with second-quarter sales climbing approximately 105.9% YOY. With net margins hovering near 63.66% and annual net income of about $120.07 billion, NVIDIA trades at a forward price-to-earnings (P/E) ratio of roughly 24. A board-authorized $80 billion share repurchase program provides additional support for long-term NVIDIA shareholders.
Commercial quantum computing is moving from theoretical ambition to engineered reality. Resolving the compilation bottleneck proves that combining accelerated classical computing with quantum algorithms can unlock productivity gains for complex logistics and industrial challenges.
Investors assessing the space face two distinct asset profiles. IonQ represents a high-beta opportunity with operational upside, supported by triple-digit top-line growth and a debt-free balance sheet. Potential risks remain centered on elevated net losses and the reality that these recent benchmarks were conducted via classical GPU simulation rather than live physical hardware.
NVIDIA offers a lower-volatility infrastructure vehicle that monetizes the hybrid quantum shift while generating free cash flow from its core artificial intelligence hardware footprint.
Growth-focused investors seeking early-stage disruption might consider tracking IonQ for stabilization after its recent consolidation, while conservative investors may prefer NVIDIA as a diversified anchor to capture the ongoing expansion of advanced computing.
The article " IonQ and NVIDIA Just Cracked a Major Quantum Computing Bottleneck " was originally published by MarketBeat.

### Article 291 · 2026-09-17 · finance.yahoo.com
Nvidia’s CUDA-Q Logical Extends Its Quantum Software Moat, But the Hardware Timeline Remains Uncertain

Nvidia Corporation (NASDAQ: NVDA ) has expanded CUDA-Q with a new orchestration layer designed for fault-tolerant quantum computing. National Laboratories and leading QPU makers were already using the technology when Nvidia announced the release. The launch also highlights the contrast between Jensen Huang's cautious view of the timeline for useful quantum computing and Nvidia's increasingly active role in developing the infrastructure needed to get there. However, as recently as January 2025, Jensen Huang said that useful quantum computers could still be 15 to 30 years away. The fundamental hardware challenges behind that view have not disappeared simply because the company has developed better software for orchestrating quantum systems.
A New Tool for Fault-Tolerant Quantum Computing
On September 14, Nvidia launched CUDA-Q Logical, an open-source orchestration layer built into its CUDA-Q platform. It is designed to help researchers develop applications for fault-tolerant quantum computers using logical qubits. The tool is available on GitHub and is already in use at Fermi National Accelerator Laboratory, IQM Quantum Computers, Sandia National Laboratories, Infleqtion, QCDesign, and Quantum Motion. NVIDIA's Timothy Costa highlighted:
Quantum computing is maturing into an era of logical qubits, and researchers need an open, customizable platform capable of representing all aspects of a fault-tolerant system. The addition of CUDA-Q Logical provides power and flexibility to explore fully integrated, co-optimized systems regardless of qubit type and architecture — drastically shortening the timeline to useful quantum-GPU supercomputing.
Fault-tolerant systems based on logical qubits are viewed as necessary for practical quantum applications such as materials development and drug discovery because they can address the errors that happen in individual physical qubits. The launch also supports the company's broader strategy of making its GPUs the key classical computing layer for hybrid quantum-classical systems.
A Physics Problem Software Alone Can't Solve
In January 2025, Jensen Huang argued that useful quantum computers were still 15 to 30 years away, then acknowledged in March that his comments had come out wrong. That shift was followed by NVentures making significant investments in PsiQuantum, QuEra, and Quantinuum. However, Huang's original concerns were tied to the difficult task of scaling quantum systems, including the enormous increase in qubit scale needed to build very useful quantum computers. That challenge remains unresolved, regardless of the software the company develops to support and orchestrate quantum systems.
The adoption of CUDA-Q Logical by national laboratories provides a meaningful short-term signal for Nvidia's quantum strategy. But the launch does more to reinforce the company's long-term platform opportunity than to materially shorten the runway toward useful, fault-tolerant quantum computing.
Institutional interest in Nvidia continued to build, with hedge fund ownership rising from 275 funds at the end of Q1 2026 to 285 funds at the end of Q2 2026. Short interest remained very low at 1.29% of float as of August 31, 2026. Together, the figures suggest that institutional confidence in the stock remains strong.

### Article 292 · 2026-09-17 · finance.yahoo.com
Tesla, NVIDIA and Microsoft Forecast: Big Tech Buyers Return

Tesla looks like it's going to jump at the open here based on pre-market trading on Thursday. After the Federal Reserve raised interest rates, it appears that, in general, we're seeing more risk appetite flow back into the stock market. It looks like the U.S. economy is being paid attention to. As the Federal Reserve stated, the strength of the U.S. economy was a bit surprising.
In this environment, that does seem to lift all boats, and Tesla is currently trying to take advantage of that. The 200-day EMA sits at $379.11, so keep that in mind as a potential barrier.
NVIDIA looks like it's going to jump right away. It's up about $5 in pre-market trading, and it is crossing out of the oversold condition on the stochastic oscillator, jumping above that crucial $215 level. Now, it looks like it's going to open, filling the gap from a couple of sessions ago.
Ultimately, NVIDIA is all about the AI play. The AI play seems to be doing fairly well in pre-market trading, so it looks pretty healthy.
Microsoft looks like it's going to jump as well, opening about $5 higher than it closed. Microsoft's been on fire for a while. It seems like it has a massive amount of support near the $477.31 level. We are well above there, but we are below that $515 barrier.
Ultimately, though, it does look like the buyers are returning, at least for a day or two, as we continue to see consolidation with more of a bullish tilt than anything else. This is a market that looks like it is trying to build momentum for another bullish move at the moment.
XRP Price Forecast: Breakdown Puts $1.10 Support in Focus
Nasdaq, Dow and S&P 500 Rise Ahead of Fed Rate Decision
Pump.fun Price Prediction: Can PUMP Deliver 3.5x Upside?
Franco-Nevada Nears All-Time Highs After Record Revenue Growth
US Dollar Price Forecast: Dollar Strengthens as Fed-BoE Policy Divergence Widens; Key Levels for EUR/USD and GBP/USD
