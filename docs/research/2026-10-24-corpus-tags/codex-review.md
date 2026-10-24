**标签确实有问题，主要是把抓取渠道当成作者、把公司所属主题传给所有附件，以及没有按同一份材料统一标签。**

例如，Amazon 的两份业绩附件明明被正文的 Item 2.02 点名，却因为程序先读到了目录，被标成 T6。另一边，Microsoft 的审计师同意函被贴上了“AI 资本开支”。

全程只读，未修改文件，未调用模型 API。

下文用 **N/F** 表示“整个指定数据库的行数／其中此次喂入窗口的行数”。实际数据库有 **2,205 行**，其中 `feed=1` 有 **1,718 行**；7 月 24 日至 8 月 15 日是 **740 行**，另有 2 月 25 日的 **12 行**。这些集合没有混算。各发现可能重叠，不能直接相加。

请求中的 `docs/prd/03-inputs.md` 当前不存在；字段要求依据 [分类 PRD 的字段表](/Users/lchingen/hivemind/docs/prd/02-classification.md:148)。没有审查或建议修改管线、提示词和设计。

**1. 每条标签规则及触发行数**

以下位置简称 `assemble.py`，完整文件是 [poc/corpus/scripts/assemble.py](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py)。同一规则的不同输出分别列出；零表示数据库中没有实际触发样本。

| 字段 | 实际规则 | 位置 | N/F |
|---|---|---|---:|
| `object_identifiers` | 未显式覆盖对象时，默认 NVDA，理由为上游为该对象提供的信息 | `assemble.py:35,116–120` | 460/27；另含全部 12 行开题材料 |
| 对象、`topic` | Google 记录没有话题时，设成 `nvda`，再查话题表 | `assemble.py:498,524` | 737/422 |
| 对象 | 合并同一 URL 的所有话题对象，按 `(kind,value)` 去重，保留第一次的理由 | `assemble.py:130–138,494–502` | 737/422 经此路径；实际多话题合并 **0/0** |
| 对象 | 未知话题退回 NVDA | `assemble.py:133` | 0/0 |
| 对象 | 同行文件和电话会写公司 ticker，理由均为 `filer` | `assemble.py:141–143,264,296` | 208/89 |
| 对象 | 同行公司表里的每个主题，附加到该公司的每份文件和电话会 | 同上；`companies.json:4–17` | 208/89；254/123 个主题标签 |
| 对象 | Fed 新闻稿、讲话、证词统一标“美联储政策利率” | `assemble.py:385–388` | 新闻稿 20/0；讲话 15/0；证词 0/0 |
| 对象 | BIS 全部标“芯片出口管制” | `assemble.py:389,409` | 16/4 |
| 对象 | USTR 全部标“中美关税” | `assemble.py:390,409` | 12/2 |
| 对象 | Commerce 标题命中第一组词，就标“芯片出口管制” | `assemble.py:402–405` | 15/3 |
| 对象 | 未命中第一组、命中关税／Section 232／China，就标“中美关税” | `assemble.py:406–407` | 90/29 |
| 对象 | Commerce 两组均未命中，写空对象 | `assemble.py:408` | 623/161 |
| 对象 | CPI、PPI 标美国通胀；就业报告标美国衰退风险 | `assemble.py:392–394` | 各 3/1 |
| `publisher`、`publisher_type` | 新闻用网址域名作为作者，再按域名后缀查作者表 | `assemble.py:62–71,312–324,465–471,512–521` | 查表命中 701/210 |
| 作者类型 | 作者表命中 company／media／analyst／individual | `author-table.json:4–17` | 71/49、534/96、94/64、2/1 |
| 作者类型 | 新闻作者表未命中，默认 media | `assemble.py:67–71` | 305/212 |
| 作者类型 | SEC、电话会、NVIDIA 自有发布直接写 company | `assemble.py:248,280,293,344,357` | 391/116；另含 12 行开题材料 |
| 作者、作者类型 | 官方材料直接写 official；FR 的作者写成 Federal Register | `assemble.py:426–431` | official 800/202；其中 FR 756/199 |
| 作者类型、类别 | 手工材料照 manifest 抄入 | `assemble.py:373–378` | 8/0 |
| `category` | 主文件的 form 以 `10-` 或 `20-` 开头，归 T2 | `assemble.py:203–205` | 15/6 |
| 类别 | 其余 SEC 主文件归 T6 | `assemble.py:206` | 55/15 |
| 类别 | 8-K 的首个 Item 2.02 区段点名某个 EX-99 附件，归 T1 | `assemble.py:209–213` | 18/6 |
| 类别 | 有 Item 2.02，但找不到对应正文区段，也把 EX-99 归 T1 | `assemble.py:214–215` | 0/0 |
| 类别 | 6-K EX-99 的说明为月度收入／销售，归 T6 | `assemble.py:216–218` | 0/0 |
| 类别 | 6-K EX-99 的说明命中财期／业绩等词，归 T1 | `assemble.py:219–220` | 0/0 |
| 类别 | EX-2、3、4、10 归 T3 | `assemble.py:221–222` | 43/18 |
| 类别 | EX-99 的说明命中演示材料，归 T5 | `assemble.py:223–224` | 0/0 |
| 类别 | 剩余 SEC 附件归 T6 | `assemble.py:225` | 105/38 |
| 类别 | 所有公司电话会归 T4 | `assemble.py:278,291` | 16/6 |
| 类别 | NVIDIA 新闻室标题含 `financial results` 就归 T1，否则 T6 | `assemble.py:341` | T1 2/1；T6 35/5 |
| 类别 | NVIDIA 博客全部归 T6 | `assemble.py:356` | 102/21 |
| 类别 | 新闻作者 company→T6，media→T7，analyst/individual→T8，official→T10 | `assemble.py:74–76` | 71/49、839/308、96/65、0/0 |
| 类别 | Fed 新闻稿 URL 含 `/monetary` 为 T11，否则 T10 | `assemble.py:412–417` | T11 4/0；T10 16/0 |
| 类别 | 其余官方材料沿用采集时类别：Fed 讲话、BLS→T11；FR→T10 | `assemble.py:417,430`；`harvest_official.py:20–28,154` | T11 24/3；T10 756/199 |
| 类别 | 手工材料沿用指定类别 | `assemble.py:375` | T1 1/0；T6 5/0；T7 2/0 |
| `klass` | 按来源写公司材料／官方材料／新闻；手工材料按作者类型分 | `assemble.py:246,278,323,343,356,373,430,470,520` | 397/116、800/202、1,008/422 |
| `copy_of` | 只检查 `klass='新闻'`；规范 URL 相同就指向前一条 | `assemble.py:539–547` | 写入 1/0；其余 1,197/318 行不参与检查 |
| `copy_of` | 同日规范标题相同，且同域名或一方属于转载站，标为转载 | `assemble.py:79–90,548–559`；`author-table.json:19–20` | 写入 8/8 |
| `coverage` | SEC 有 `.full.txt` 就算 full；公司电话会直接算 full | `assemble.py:243–251,281–295` | SEC 236/83；电话会 16/6 |
| `coverage` | 官方、新闻室、博客全文超过 200 字符就算 full | `assemble.py:346,359,433` | 939/229 |
| `coverage` | 手工材料有文件且至少 200 字符就算 full | `assemble.py:368–378` | 8/0 |
| `coverage` | 抓取页有文件时沿用覆盖标记；full/partial 只要有整页文本就变 full | `assemble.py:183–193` | 最终 full 519/422；stub 4/0 |
| `coverage` | 旧抓取记录缺日期或阻拦标记时，补读 HTML；阻拦优先，少于 500 字符为 stub | `assemble.py:164–179` | 331/325 经此路径；最终 328 full、3 stub |
| `coverage` | 没有抓取文件，默认 title；TrueNorth 改成 provider_summary | `assemble.py:185–186,318–320` | 最终 title 217/0；provider_summary 266/0 |
| `feed` | 只有 coverage=full 且文本至少 200 字符才为 1 | `assemble.py:125–126` | 1,718/740；其余 487 行为 0 |
| `publication_day` | SEC 使用 `filing_date` | `assemble.py:232,249` | 236/83 |
| 发布日 | 电话会取 `call_date` 的日期部分 | `assemble.py:276,289` | 16/6 |
| 发布日 | 新闻取列表日和页面日中较早的日期；RSS、时间戳先换纽约日期 | `assemble.py:104–113,309–325,458–472,506–522` | Google 737/422；TrueNorth 新闻 269/0；GDELT 0 |
| 发布日 | 新闻室、博客、手工材料沿用 manifest 日期 | `assemble.py:345,358,377` | 147/27 |
| 发布日 | 官方材料沿用采集的发布日期 | `assemble.py:432` | 800/202 |
| `tier` | 默认 core；同行 industry；官方按来源及是否有对象分 macro/geopolitics/noise | `assemble.py:119,264,295,428,517–524` | core 1,197/449；industry 208/89；macro 44/3；geopolitics 133/38；noise 623/161 |

这里的 `tier` 是素材层次，不是模型给说话人的身份层级。

采集脚本确实预先提供了部分标签依据：同行采集器复制 `companies.json` 的主题，官方采集器写类别和日期，话题采集器写话题、对象和层次。但本数据库 **737 条 Google 记录的原始解析记录全部没有 `topic`，最终都走 NVDA 默认值**。`topics.json` 其余 **25 个话题均为 0 行**。其中“搜 SK Hynix／三星却固定标 MU”等配置有明显范围风险，但本次不能给它们算实际错误行数。

**2. 发现，按触及的喂入行数排序**

**① Federal Register 被写成作者：756/199。**

它是发布渠道。实际作者在公告的机构字段里。这违反[作者与渠道分开的规则](/Users/lchingen/hivemind/docs/prd/02-classification.md:122)。

例如：

- `official:fr-bis:fec28b710108438867ad` — **Streamlining Export Controls for Drone Exports**；作者是 BIS。
- `official:fr-ustr:49129a91dc865b5d3787` — **Fiscal Year 2027 Tariff-Rate Quota Allocations for Raw Cane Sugar, Refined Sugar, and Sugar-Containing Products**；作者是 USTR。

这些记录的 `publisher_type=official` 和 T10 本身没有因此变错。影响的是作者归属；199 条中，当前对象与类别组合能通过名单匹配的只有 38 条。不能把 199 算成模型身份层级已经判错的次数。

**② 公司所属主题被传给所有附件：208/89。**

这不是不合法的 JSON，也不是所有 208 条都错。规范允许“上游为这个主题提供”作为理由。但当前规则没有区分整份财报与附带的认证文件。

其中，仅认证、审计同意函、子公司表、内部治理文件这一可直接按附件类型核查的范围，就有 **57/29**：

- `edgar:0001193125-26-323660:msft-ex21.htm` — **MSFT 10-K EX-21**，实际是子公司名单，却标 AI 资本开支。
- `edgar:0001193125-26-323660:msft-ex23_1.htm` — **MSFT 10-K EX-23.1**，实际是审计师同意函，同样标 AI 资本开支。
- `edgar:0000002488-26-000123:exh311302certofceo-q210q26.htm` — **AMD 10-Q EX-31.1**，实际是 CEO 认证，却标半导体周期和自研芯片。

错误到达提示词的对象行。89 条中有 18 条 T3 已被名单类别挡住，其余 **71 条**有机会携带这些主题进入抽取。**这些附件归 T6 并不因此错误，也不应因“没投资价值”而删掉。**

**③ 用承载网页的域名决定作者和类别：已确认影响 91/69。**

这里有三个不同方向，不能只增加几个域名就算解决。

| 子类 | 已确认范围 N/F | 当前错误 |
|---|---:|---|
| 转载平台没有恢复原作者 | 65/49 | 64/48 条 Yahoo 转载，加 1/1 条 Morningstar 承载的 MarketWatch 新闻 |
| 公司自有发布走 media 默认值 | 15/11 | T7 应为 T6，同时缺少发稿公司对象 |
| 独立研究及明确分析栏目走新闻规则 | 11/9 | T7 应为 T8 |

转载的类别变动是 **36/30 条 T7→T8，另 1/1 条 T8→T7**。这是用页面的 `provider.url`、原文链接和现有作者表算出的，不是看到“预测”一词就改类别。

例子：

- `gnews:fddb23b609fb42502a9aabce` — **Prediction: Nvidia Stock Will Hit $800 Per Share by 2030**。页面明确为 Motley Fool 原稿，当前因 Yahoo 域名被标成 media/T7。
- `gnews:bb0d23846735c94b7c1722d2` — **Nvidia's potential new deal with OpenAI would revive a spooky tech-bubble habit, analyst warns**。页面明确是 MarketWatch／Dow Jones 新闻，当前因 Morningstar 域名被标成 analyst/T8。
- `gnews:b830d772d6e11e0ccaa0093b` — **IBM and Together AI Sign Multi-Year Agreement to Scale Open-Source AI Inference with NVIDIA AI Infrastructure on IBM Cloud**。IBM 自有新闻稿被标 media/T7，对象只有 NVDA。
- `gnews:db759b7fd9bedbcd0f632fe6` — **SK Group and NVIDIA Expand Strategic Partnership Across AI Factories and Next-Generation Memory**。同样漏掉发稿方对象。
- `gnews:fad9b5d27a8c0929b5daebc5` — **Is the NVIDIA DSX Reference Design the Real Collateral for $500B in Financing?**。原文明确写 `Analyst(s)`，当前为 T7。
- `gnews:4ce7b426f466da78af06cadc` — **Nvidia's potential $250B backstop for OpenAI is another strike against the AI trade**。来源栏目为 CNBC Investing Club，正文是该栏目的投资判断，当前为 T7。

影响类别对应的阅读块、作者身份，以及公司作者应进入的对象行。上述类别变动在当前名单下不会改变这些 NVDA 记录是否匹配名单。实际说话人层级是否判错，没有计入本次审查。

**④ 去重只处理新闻，而且只写指针：37/29 条需要补齐或统一标签。**

- **28/21** 条同 URL 的重复记录没有标记：24 组跨新闻／公司材料，另 4 组两边都是公司材料。
- 原文链接还能确定 **1/0** 条转载，现有同日标题规则漏掉它。
- 已标出的 8 条 Yahoo 转载，自身仍是 T7，指向的原稿却是 T8。

例如：

- `gnews:1308c676b64cc3b0290377ba` — **NVIDIA Sets Conference Call for Second-Quarter Financial Results**，与新闻室原件 URL 和全文相同，`copy_of` 为空。
- `gnews:973f2ef3c64c4c1895f73753` — **NVIDIA Expands NVIDIA Agent Toolkit With NVIDIA PhysicsNeMo and CUDA-X Libraries to Transform How the World Engineers, Designs and Builds**，也与新闻室原件重复。
- `gnews:8c610e8f4625edf599d90fba` — **Jensen Huang Just Revealed Nvidia’s Real Endgame — And the Risk It Creates for U.S. AI Leadership**，已指向原稿，但仍保留错误的 T7。

这违反[转载继承原类别、合并对象、使用最早发布日期的要求](/Users/lchingen/hivemind/docs/prd/02-classification.md:102)。当前已标转载的对象恰好都相同，日期也相同，所以这两项缺失本次没有额外错标数量。

这里统计的是标签漏合并，不宣称下游实际重复调用了多少次。

**⑤ “整页文本齐全”被当成“该材料全文齐全”：两种机制触及 107/26 条。**

第一种是 **10/9 条 CNBC 视频页**。页面只有视频介绍、导航和推荐视频，没有文字稿，仍被标 `full/feed=1`。我逐条检查了这 10 条的材料区段。

- `gnews:e953f5a61114c9b8933c5011` — **Cramer’s Stop Trading: Nvidia**。
- `gnews:6c94cb2a1a2a864e672d3f1d` — **Nvidia CEO Jensen Huang: Computing industry is going through a fundamental platform shift**。

第二种是官方文件的路径碰撞。`harvest_official.py:31–39` 把标题缩成最多 80 字符的文件名；同日同前缀的不同公告会共用文件。**41 组、97/17 条**涉及此问题，其中较早写入、正文被覆盖的是 **56/9 条**。

- `official:fr-commerce:825bcd9db6a663122a09` — **…Ferry Berth Construction in Tongass Narrows in Ketchikan, Alaska**，读到的是另一份 Hoonah 项目公告。
- `official:fr-commerce:b054f200ac9748822884` — **…Comment Request; Steel Import License**，读到的是 NOAA Diving Program 文件。

后者不是正常转载，不能按相同正文合并。17 条窗口记录目前都没有对象，已经不匹配研究名单；9 条视频页则匹配 NVDA。两者都使 `coverage/full` 的含义不成立。

**⑥ 官方主题同时过宽、过窄：拟收紧触及 39/9 条。**

明确的过宽例子：

- `official:fr-bis:f80a665575eec5a5e2cc` — **Notice of Reduction of Tariffs on Patented Pharmaceuticals and Pharmaceutical Ingredients for Products of the United Kingdom…**，标成芯片出口管制。
- `official:fr-commerce:414407be5966432cc1ff` — **Foreign-Trade Zone (FTZ) 75, Notification of Proposed Production Activity; Intel Corporation; (Semiconductor Products); Chandler, Arizona**。这是生产活动公告，不是出口管制。
- 上面的 USTR 食糖配额公告被标成中美关税。

过窄则来自只检查被截成 200 字符的标题。两条中国反倾销／反补贴公告没有关税对象，其中一条在窗口内：

- `official:fr-commerce:b011a472789d6fe4a57f` — **Notice of Initiation of Changed Circumstances Reviews…Antidumping and Countervailing Duty Orders on Crystal…**
- `official:fr-commerce:ac588036fae1806640a2` — **Notice of Extension of the Deadline…Certain Linear Hydraulic Cylinders…**

它们的正式案号字段明确包含 `A-570-…`／`C-570-…`；第一条的公告摘要也明确写中国。这个案号范围共 **91/30** 条，漏标 **2/1** 条。

按“本公告正式处理的事项与国家”收紧，当前可移除 **37/8** 个宽泛主题标签，并补上上述 **2/1** 个关税标签。37 条是该收紧口径的改动范围，**不等于宣称它们与芯片或中国完全没有间接关系**。

相反，窗口内 29 条 Commerce 中国商品关税公告不能因商品是家具、轮胎、纸张就判成噪音。它们确实属于中美关税。

**⑦ 电话会对象的理由写成申报人：13/6。**

- `truenorth:transcript:AMD:2026-08-04` — **AMD Q2 FY2026 Earnings Call**。
- `truenorth:transcript:AMZN:2026-07-30` — **AMZN Q2 FY2026 Earnings Call**。

公司对象正确，但 `why='filer'` 不正确。应当表达公司发言方。它污染对象行的解释，不改变路由或 T4 类别。

**⑧ SEC 附件分类过窄：8/3。**

两种机制叠加：

- **2/2 条 Amazon 附件**：首个 Item 2.02 是目录。内存中改为检查实际正文区段后，两条都从 T6 变成 T1；其余当前已识别的 T1 不变。
- **6/1 条 6-K 附件**：说明字段只有 `EX-99.1` 等编号，代码不看附件封面，全部落入 T6。实际封面明确是财期业绩材料。

例子：

- `edgar:0001018724-26-000024:amzn-20260630xex991.htm` — **AMZN 8-K EX-99.1**。
- `edgar:0001018724-26-000024:amzn-20260630xex992.htm` — **AMZN 8-K EX-99.2**。
- `edgar:0001046179-26-000541:a2026q2consolidatedreport-.htm` — **TSM 6-K EX-99.1**，封面为截至 2026 年 6 月的半年财务报表。
- `edgar:0001628280-26-065813:pressreleasefinancialresul.htm` — **ASML 6-K EX-99.1**，封面明确为第三季度业绩；不在此次喂入窗口。

影响类别阅读块；公司对象和名单匹配不变。

**⑨ NVIDIA 新闻室的业绩关键词过宽：1/1。**

`nvidianews:nvidia-sets-conference-call-for-second-quarter-financial-results-6927195` — **NVIDIA Sets Conference Call for Second-Quarter Financial Results | NVIDIA Newsroom**。

这是一份电话会预告，没有发布业绩，应为 T6。实际业绩稿是 8 月 26 日那条。该错误到达 T1 阅读块。只有这一例，不凑第二例。

**⑩ Fed 类别按整个频道或 URL 片段决定：9/0。**

8 篇非货币政策、非统计发布的讲话被标 T11；另有 1 篇统计发布被标 T10。

- `official:fed-speeches:9c2e70ef035e5c9105ce` — **Bowman, Supervisory Modernization After Silicon Valley Bank**，应按官方监管材料处理。
- `official:fed-speeches:edf8cf0d42b09ee485a9` — **Bowman, Opening Remarks**，实际是社区银行网络安全研讨会致辞。
- `official:fed-press:0d84bbab316fddb29a83` — **Federal Reserve Board releases results of the 2025 Survey of Consumer Finances…**，是统计发布。

这类错误会同时影响主题的类别匹配和阅读块，但此次窗口没有这些行。

其余没有确认实错的规则包括：SEC 法定申报日、BLS 三类映射、公司电话会 T4、手工材料类别，以及 `klass` 的三大分组。**公司通稿出现在“新闻”大组内本身不是错误**，素材计划允许这样存。

新闻有 **32/28** 条列表日与页面日不同，其中页面更早为 20/19，页面更晚为 12/9。这个差异不能直接判成日期错误。四条 DCD 记录的页面日期实际上抓到了推荐卡片；若改成一律优先页面日期，反而会把七月文章移到十月。

**3. 每条有问题规则的一条收紧建议**

以下都是标签写入侧的建议。数量是单项改动效果，存在重叠。

| 对应规则 | 单一结构规则 | 可计算效果，N/F | 会失去什么 |
|---|---|---|---|
| FR 作者 | 作者取正式签发机构，Federal Register 只作渠道 | `official/T10`：756/199 改作者；类别和 feed 不变 | 无正文损失；不能从已被覆盖的正文恢复可靠细分机构 |
| 公司主题继承 | 公司表只说明为何抓取该公司，不把公司所属主题自动传给每份材料 | 去掉 254/123 个主题标签；涉及 `edgar-peers` T1 12/6、T2 12/6、T3 40/18、T6 131/53，以及 `truenorth/T4` 13/6；当前名单匹配增减均为 0 | 财报、电话会中原本有用的主题提示也会暂时失去；公司对象和全文仍在 |
| 转载作者 | 先恢复本条原作者，再查作者类型；承载网站只作渠道 | `gnews`：36/30 条 T7→T8；1/1 条 T8→T7；共 65/49 条作者归属修正 | 无正文或路由损失；没有原作者证据的记录不能强行猜 |
| 公司自有发布 | 明确由公司自有渠道发出的材料，登记该公司身份，并把作者公司加入对象列表 | `gnews`：15/11 条 T7→T6；补公司作者对象；当前名单匹配不变 | 不应把这些公司自动加入研究名单 |
| 新闻类别 | 作者类型只给默认类别，来源明确标出的研究／分析栏目优先决定类别 | `gnews`：11/9 条 T7→T8 | 不能把普通新闻引用分析师的话也改成 T8 |
| 去重 | 同一原件只拥有一份规范标签，所有来源共同指向它，继承类别、对象并集和最早日期 | 新增 copy：`gnews/T6` 24/21、`nvblog/T6` 4/0、`gnews/T7` 1/0；另统一已有 8/8 条转载类别 | 不损失原文；会减少独立材料数，来源仍需保留 |
| 页面覆盖率 | `full` 必须证明取得的是本条材料的正文或文字稿，整页字符数不能代替此证明 | `gnews/T7`：10/9 条 full→非全文、feed 1→0 | 暂时失去视频介绍中的少量信息；当前文本没有视频内容 |
| 官方文件绑定 | 一条原始 URL 必须独占其原件路径，绑定有歧义的记录不能标 full | `official/T10`：97/17 条暂不算 full；其中确定被覆盖的为 56/9 | 若整组暂缓，会连同尚正确的 41/8 条一起暂缓；窗口内 17 条本来就不匹配名单 |
| 官方主题 | 主题来自本公告正式处理的事项及国家，机构名和孤立关键词不能代替它 | `official/T10`：BIS 移除 15/4、Commerce 移除 15/3、USTR 移除 7/1；Commerce 补入 2/1。窗口名单匹配 −8、+1 | 放弃宽泛的供应链、全球贸易间接联系；原文继续保留 |
| 对象理由 | 对象理由由当前材料中公司的实际角色决定 | `truenorth/T4`：13/6 条 `filer` 改为公司发言方 | 无 |
| 8-K 业绩附件 | 只有实际正文 Item 2.02 中的附件引用决定 T1，目录不是引用证据 | `edgar-peers`：2/2 条 T6→T1 | 无；已用存量正文验证只改变这两条 |
| 6-K 附件 | 附件类型由它自己的正式说明或封面确定，纯编号不充当内容说明 | `edgar-peers`：6/1 条 T6→T1 | 无；不能把所有 EX-99 都统一当业绩 |
| 新闻室 T1 | 只有实际发布某财期业绩的材料才为 T1，安排将来发布业绩仍为 T6 | `nvidianews`：1/1 条 T1→T6 | 无 |
| Fed 类别 | 按具体发布系列登记类别，整个讲话频道不能登记成货币政策系列 | `official`：8/0 条 T11→T10；1/0 条 T10→T11 | 无正文损失；同时应撤掉非利率材料的利率主题提示 |

**4. 当前写入方式表达不全的要求**

- **多个对象可以表达。** JSON 列表已经支持，208 条也确实写了多个对象。问题是公司作者没有被补进去，不是需要另造多对象结构。
- **公司作者与报道对象可以不同，但当前新闻路径没有分别填好。** IBM、SK 的稿件可以同时保留 NVDA 和发稿公司。通稿平台也不能成为发稿公司。
- **栏目和发布系列没有进入判定。** 全部 2,205 行的 `channel_category` 都为空，schema 没有 `series`；`news_category()` 只接收作者类型，无法实现规范要求的优先顺序。
- **同一对象的多个来由没有合并。** `objects_for_topic()` 只保留第一次理由。当前多话题样本为零，不能声称已经造成多少漏标。
- **作者表没有有效期。** 当前没有按任期切换身份的已确认样本，因此是表达能力限制，不计本次错标。
- **版本字段存在，但从不写入。** `supersedes` 全为空；本库也没有 `/A` 申报，不能据此宣称丢了某个实际修订版。

**计数查询与核对方法**

数据库连接均为：

```python
sqlite3.connect(
    "file:/Users/lchingen/hivemind/poc/data/items-window.sqlite?mode=ro",
    uri=True,
)
# 随后执行 PRAGMA query_only=ON
```

基础总数及规则表使用以下字段查询：

```sql
SELECT count(*) AS total,
       sum(feed=1) AS all_feed,
       sum(feed=1 AND publication_day BETWEEN
           '2026-07-24' AND '2026-08-15') AS window_feed,
       sum(feed=1 AND publication_day='2026-02-25') AS seed
FROM items;
-- 2205, 1718, 740, 12

WITH b AS (
  SELECT *,
         feed=1 AND publication_day BETWEEN
           '2026-07-24' AND '2026-08-15' AS f
  FROM items
)
SELECT source, klass, category, publisher_type,
       coverage, day_source, topic, count(*) AS n, sum(f) AS f
FROM b
GROUP BY 1,2,3,4,5,6,7;
```

对象计数按 JSON 字段展开，没有在序列化 JSON 中搜字符串：

```sql
SELECT json_extract(j.value,'$.kind') AS kind,
       json_extract(j.value,'$.value') AS object,
       json_extract(j.value,'$.why') AS why,
       count(DISTINCT i.input_id) AS n,
       count(DISTINCT CASE
         WHEN i.feed=1 AND i.publication_day BETWEEN
              '2026-07-24' AND '2026-08-15'
         THEN i.input_id END) AS f
FROM items i, json_each(i.object_identifiers) j
GROUP BY 1,2,3;
```

公司主题改动按来源、类别计数：

```sql
SELECT i.source, i.category, count(*) AS n,
       sum(i.feed=1 AND i.publication_day BETWEEN
           '2026-07-24' AND '2026-08-15') AS f
FROM items i
WHERE EXISTS (
  SELECT 1 FROM json_each(i.object_identifiers) j
  WHERE json_extract(j.value,'$.kind')='theme'
    AND json_extract(j.value,'$.why')='upstream feed: company in theme'
)
GROUP BY 1,2;
```

转载标签不一致：

```sql
SELECT a.source, a.category, b.category, count(*) AS n,
       sum(a.feed=1 AND a.publication_day BETWEEN
           '2026-07-24' AND '2026-08-15') AS f
FROM items a JOIN items b ON b.input_id=a.copy_of
GROUP BY 1,2,3;
-- gnews T7 T7: 1/0
-- gnews T7 T8: 8/8
```

官方文件碰撞使用 manifest 的**完整文件路径**分组，再以 URL 连接数据库：

```sql
WITH p AS (
  SELECT CAST(key AS INTEGER) AS seq,
         json_extract(value,'$.file') AS file,
         json_extract(value,'$.url') AS url
  FROM json_each(:official_manifest, '$.pages')
),
g AS (
  SELECT file, count(DISTINCT url) AS urls, max(seq) AS last_seq
  FROM p GROUP BY file
  HAVING count(DISTINCT url)>1
)
SELECT count(*) AS ambiguous,
       sum(i.feed=1 AND i.publication_day BETWEEN
           '2026-07-24' AND '2026-08-15') AS ambiguous_f,
       sum(p.seq<g.last_seq) AS overwritten,
       sum(p.seq<g.last_seq AND i.feed=1
           AND i.publication_day BETWEEN
           '2026-07-24' AND '2026-08-15') AS overwritten_f
FROM p JOIN g USING(file)
JOIN items i ON i.source_uri=p.url;
-- 97, 17, 56, 9
```

其余需要原始元数据的计数，使用以下明确路径：

| 计数 | 查询或判定路径 |
|---|---|
| SEC 各分支 | 以 accession＋document name 连接 manifest 与 `input_id`；只在内存执行 `exhibit_category()`，按返回语句行号汇总 |
| Yahoo 原作者 | `pages/index.jsonl[url].file` → 对应 HTML 的 `NewsArticle.provider.url`；再查现有作者表 |
| Morningstar 转载 | URL 路径段精确为 `news/marketwatch`，并核对页面的 MarketWatch／Dow Jones 来源栏 |
| CNBC 视频 | `publisher='cnbc.com'`，URL 路径段精确含 `video`；逐条核对材料区段 |
| 未标同 URL 转载 | 使用现有 `canonical_url()` 分组；排除组内已有 `copy_of` 的组，保留一个原件，其余计新增转载 |
| 漏掉的中国关税公告 | 只取正式 `AGENCY` 段之前的方括号案号字段；逗号拆分后完整匹配 `[AC]-570-\d{3}`，再检查主题对象是否缺失 |
| 公司默认类型错误 | 精确域名集合：`news.skhynix.com`、`navercorp.com`、`ey.com`、`quantinuum.com`、`nokia.com`、`tier4.co.jp`、`apollo.com`、`lw.com`、`paulweiss.com`、`newsroom.ibm.com`、`coreweave.com`、`aws.amazon.com`、`openai.com` |
| 研究／分析遗漏 | 精确域名集合：`tikr.com`、`marketwise.com`、`futuriom.com`、`equiti.com`、`trefis.com`、`newsletter.semianalysis.com`、`futurumgroup.com`、`uncoveralpha.com`；另加来源栏目精确为 `CNBC Investing Club` 的两条 |

每个主要计数都回查了上文的具体记录。额外使用 NVDA 2 月业绩附件和 BLS CPI 作为正确对照；Amazon 的内存验证只翻转两条错误附件，没有翻转正确对照。