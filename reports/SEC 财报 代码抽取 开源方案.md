# 让 XBRL 接管数字，代码只啃无标签表

旧系统的五类失败（NVIDIA 的缩写月份、Apple 的复数 "Years ended"、Microsoft 的无标题表、新的分部版式、同名不同行被并成一个指标）都来自同一个做法：从压平的表格文字里重新猜每个数字的期间、指标和分部。可这些信息，申报人早已用 inline XBRL 写在 10-K/10-Q 的每个数字上了。财务报表和附注里的数字全部带标签，每个都带 ISO 起止日期、单位、概念名（如 `RevenueFromContractWithCustomerExcludingAssessedTax`）和 axis/member 维度，分部、产品、地区表也在内。成熟的开源路线是直接读每份申报自带的 XBRL 实例和链接库：Arelle 是 SEC 自己运行的引擎，edgartools 是最活跃的 Python 封装。SEC 的 companyfacts API 当不了主路径，因为它按设计丢掉了全部分部和公司自定义数据，Apple FY2025 的 iPhone 收入在里面出现 0 次。代码还得自己解析的只剩两块：10-Q/10-K 的 MD&A 表（约占一份申报数字的四分之一，实测其中带标签的数字为 0）和 8-K 业绩新闻稿（完全无标签）。这一块没有好用的开源工具：唯一专门的解析器 edgartools，在 NVIDIA、Apple、Microsoft 最新的新闻稿上几乎重现了旧系统的全部失败类别。第三个难点是时间：companyfacts 的 `fy`/`fp` 描述的是申报，不是数字所属的期间；frames 永远取最后一次申报的值；SEC submissions JSON 的受理时间戳在 7 家公司里有 6 家偏了 4–5 小时。对新系统的含义有三条。第一，10-K/10-Q 走逐份 XBRL 事实路径，数字身份由（concept、全部维度、起止日期、单位）决定，不看行标签。第二，无标签表只按封闭语法解析，能和同一份申报的 XBRL 对上才采信，其余要么拒绝，要么交给只能回答单元格 id 的模型。第三，每个数字按"身份 × 申报"存成一条观测，版本关系由代码判定。文中标"实测"的数字来自研究团队 2026-10-16 对 SEC 公开数据的零成本测量，多数只覆盖一份或几份申报，是个例，不是普查。

## 10-K/10-Q 约四分之三的数字已带标签，旧系统读错了层

SEC 要求经营公司在 10-K、10-Q 中用 Inline XBRL 标记"封面和财务报表信息（包括附注、附表，以及年报中的审计师信息）"([SEC Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl))。按 Rule 405 的细节标记要求，附注表格和正文里的每个数字都要逐个打标签，自 2012 年 6 月起对所有申报人生效。这一条出自二手资料，研究团队没有读到规则原文([Colonial Stock Transfer](https://colonialstock.com/xbrl-tagging.htm))。MD&A 从未被要求：2020 年 SEC 修订 MD&A 规则时"没有建议 MD&A 采用 XBRL 格式"([XBRL US 意见](https://xbrl.us/news/xbrlus-comment-sec-mda/))。实测结果一致。NVIDIA 截至 2026-07-26 的 10-Q 有 **1,002 个 `ix:nonFraction` 数字和约 313 个未标记的数字，约 76% 带标签**；MD&A 一节里带标签的数字是 **0**，未标记的有 236 个([nvda-20260726.htm](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm))。Apple FY2025 10-K 约 75% 带标签，MD&A 里同样是 0 个对 88 个([aapl-20250927.htm](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm))。这两个比例都是对单份申报的正则估算。业绩 8-K 几乎全空：NVIDIA 2026-08-26 业绩 8-K 的封面文件有 22 个标签，新闻稿 `q2fy27pr.htm` 和 CFO 评论 `q2fy27cfocommentary.htm` 都是 0 个，整份申报只渲染出一个封面 `R1.htm`([NVIDIA 8-K index](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/index.json))。

SEC 从同一份申报人 XBRL 生成四层数据，区别在时效和完整度。下表综合自 [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)、[FSDS 2026q3 readme](https://www.sec.gov/files/dera/data/financial-statement-data-sets/2026q3.zip)、[FSNDS 页面](https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets) 和 [FSNDS readme](https://www.sec.gov/files/aqfsn_1.pdf)，时效和大小是 2026-10-16 的实测。

| 数据层 | 时效 | 分部 / 维度 | 公司自定义标签 | 期间日期 | 规模 | 合适用途 |
|---|---|---|---|---|---|---|
| data.sec.gov API（companyfacts、companyconcept、frames） | 通常 1 分钟内 | 无 | 无 | 精确 `start`/`end` | Apple 一家 3.79 MB | 合并口径历史、交叉核对 |
| Financial Statement Data Sets（FSDS，季度） | 季末后约 5 天 | 有 `segments` 列（2024 年 12 月起；只含报表正面出现的概念） | 有 | `ddate` 取整到月末 | 2026q3 解压后 986 MB | 批量回填报表正面 |
| Financial Statement and Notes Data Sets（FSNDS，月度） | 月末后约 3 天 | 有（`dim` 表） | 有 | 取整到月末 | 2026 年 8 月解压后 2.46 GB | 批量回填附注和分部 |
| 单份申报原始文件（`.htm`、`_htm.xml`、`_pre/_cal/_def/_lab.xml`、`FilingSummary.xml`） | 受理后即可取 | 有 | 有 | 精确 | Apple 10-K 实例 1.42 MB | 逐份抽取的主路径 |

companyfacts 缺分部是写明的规则，不是推测。SEC 说明 XBRL API 只收"使用非自定义 taxonomy"并且"适用于整个申报主体"的事实([SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces))。实测 Apple 的 companyfacts，每条记录只有 `start, end, val, accn, fy, fp, form, filed, frame` 九个字段，没有任何 axis 或 member 字段。按精确数值搜索，FY2025 总净销售额 416,161,000,000 出现 1 次，而 **iPhone 的 209,586M、Services 的 109,158M、美洲分部销售额 178,353M、美洲分部营业利润 72,480M 全都出现 0 次**([companyfacts CIK0000320193](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json))。同一份 10-K 的实例文件里这些数字都在：iPhone 是 `RevenueFromContractWithCustomerExcludingAssessedTax` 挂在 `srt:ProductOrServiceAxis=aapl:IPhoneMember` 上；美洲分部是同一个概念挂在 `srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember` × `us-gaap:StatementBusinessSegmentsAxis` 上；未分摊的公司层面营业利润 -42,627M 挂在 `CorporateNonSegmentMember` 上([aapl-20250927_htm.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927_htm.xml))。这份实例共有 1,131 个事实，其中 452 个带维度（Arelle 计为 460 个）。

拿 XBRL 对照旧系统的失败，可以推出几点。表头写 "Jul 26, 2026" 还是 "Years ended" 都不重要，因为每个事实的期间来自它 context 里的 ISO `startDate`/`endDate`/`instant`。HTML 里没有标题的表，在 XBRL 里仍是一个 presentation role，带 `definition`（FSNDS 里叫 `longname`）和 `menucat`。Apple 按 ASU 2023-07 改了分部版式，但在 XBRL 里仍是同一个概念挂在同样两个 axis 上。旧系统并成一行的同名行，在 XBRL 里分属不同概念或不同 member。这些结论是从数据形状推出来的：研究团队没有在旧系统出错的那几份申报上逐一验证，也没有打开 Microsoft FY2026 10-K 的 role 列表，确认那些无标题表在里面长什么样。几个实践细节：SEC 限速每秒 10 次请求，并要求在 `User-Agent` 里写明联系邮箱([Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data))。FSNDS readme 仍写着"按季度更新"、维度键名叫 `dimh`，可实际文件按月发布，列名是 `dimhash`([FSNDS readme](https://www.sec.gov/files/aqfsn_1.pdf)、[2026_08_notes.zip](https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip))。两个批量数据集都把期末日取整到月末，所以 NVIDIA 2026-07-26 这类 52/53 周财年的日期，只能从实例文件或 companyfacts 拿到。

## Arelle 与 edgartools 解析可靠，认出"哪张是收入表"仍靠猜

2026 年值得用的开源库只有两个，其余的要么停更了，要么只是下载器。下表的版本、日期和许可证取自 2026-10-16 的 PyPI 与 GitHub 元数据([Arelle](https://github.com/Arelle/Arelle)、[Arelle/EDGAR](https://github.com/Arelle/EDGAR)、[edgartools](https://github.com/dgunning/edgartools)、[py-xbrl](https://github.com/manusimidt/py-xbrl)、[secfsdstools](https://github.com/HansjoergW/sec-fincancial-statement-data-set)、[python-xbrl](https://pypi.org/project/python-xbrl/)、[OpenEDGAR](https://github.com/LexPredict/openedgar))，性能数字是对 Apple FY2025 10-K 的单次实测。

| 库 | 最新版本 | 许可证 | 能做什么 | 要注意的 |
|---|---|---|---|---|
| Arelle（`arelle-release`） | 2.46.1，2026-10-08 | Apache-2.0 | 完整的 XBRL 处理器：XBRL 2.1、Dimensions、Formula、Inline XBRL 1.1、xBRL-JSON/CSV；SEC 目前用的是 2.44.2 | 冷启动 55.0 s（主要花在下载 taxonomy），热缓存 0.7 s，约 210 MB 内存 |
| edgartools | 5.62.0，2026-10-11 | MIT | 解析全部链接库、识别报表、给维度分类、95 个标准概念、解析 8-K 新闻稿表格 | 默认视图隐藏分部；大约每周发一版，输出会变；冷跑 23.0 s、213 MB |
| py-xbrl | 3.0.3，2026-03-08 | GPL-3.0 | 底层 XBRL/iXBRL 解析 | 有"旧申报抽不出事实"等未关闭的 issue；GPL 会约束分发的代码 |
| secfsdstools | 2.4.3，2025-09-20 | Apache-2.0 | 把 FSDS 转成 parquet、标准化 BS/IS/CF、支持 `segments` | 只覆盖 FSDS（报表正面），时效是季度 |
| python-xbrl、OpenEDGAR | 分别在 2016、2022 年后无更新 | — | — | 已停更 |
| sec-edgar-downloader、secedgar | 仍在维护 | MIT / Apache-2.0 | 只下载申报 | 不解析 |

实测中，edgartools 从 Apple FY2025 10-K 生成的损益表与公司公布的合计一致：净销售额 416,161、产品 307,003、服务 109,158、营业利润 133,050、净利润 112,010（百万美元）([Apple 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm))。不过它的事实表只有 1,044 行，实例里却有 1,131 个事实，差额的原因没查。它有三条数据路线，只有逐份申报的 `filing.xbrl()` 支持维度和自定义概念；Company Facts 路线建在 SEC companyfacts 上，文档明写 "Segment/dimension data: No"([choosing-the-right-api.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/getting-started/choosing-the-right-api.md))。即使走 `filing.xbrl()`，默认的报表视图也会"隐藏属于附注披露的明细（地区、分部等）"，要用 `view="detailed"` 才看得到([dimension-handling.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/concepts/dimension-handling.md))。2026 年它修的几处缺陷正好落在分部数据上：#1188（命名空间尾段相同时，不同的 QName 被合并成一个）、#1331（detailed 视图漏掉部分分部收入，9 月关闭）；#1449（ASU 2023-07 的分部行按 member 映射）仍未关闭([edgartools issues](https://github.com/dgunning/edgartools/issues))。版本迭代这么快，用它就要锁定版本，并把版本号记进每次抽取的结果。

Arelle 的取舍正好相反：它不替你判断哪张是损益表，但对 XBRL 标准的覆盖最完整，SEC 的 EDGAR 渲染器和验证插件就跑在它上面([Arelle/EDGAR](https://github.com/Arelle/EDGAR))。55 秒冷启动只是第一次缓存 taxonomy 的成本，缓存之后单份 10-K 只要 0.7 秒。还有第三条路：SEC 为每份 iXBRL 申报抽出的 `_htm.xml` 是普通的 XBRL 2.1 XML，研究团队就是用 Python 标准库直接读它，得到上面 Apple 的事实计数。代价是标准 taxonomy 里的标签、计算权重和废弃关系得另外加载。XBRL US 的 API 不适合当产品的数据源：免费账号每次查询最多返回 100 条，只许非商业用途，并且禁止转存到其他数据库([XBRL US API](https://xbrl.us/xbrl-api/))。

各家重建一张表的方法都一样：每张表对应 presentation linkbase 里的一个 extended-link role，role 的树给出行的顺序和首选标签。SEC 渲染器把每个 role 变成一个 R 文件并归类（封面、报表、附注、政策、表格、明细），FSNDS 再把结果发布成 `ren` 和 `pre` 两张表([FSNDS readme](https://www.sec.gov/files/aqfsn_1.pdf))。Apple FY2025 10-K 有 71 个报告，收入分解在 R38，分部明细在 R68([Apple FilingSummary.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/FilingSummary.xml))。同一个概念会出现在多张表里，例如 NVIDIA 的 `OperatingIncomeLoss` 既在损益表（report 2）里，也在两张分部明细表（report 63、64）里([2026_08_notes.zip](https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip))。数值和位置都是按申报原样给出的，这部分可靠；不可靠的是"认出哪个 role 是损益表"。edgartools 的 `statement_resolver.py` 靠关键抽象概念、关键概念和 role URI 正则来打分，代码注释里记着修过的漏洞，例如 **"Issue #581: Match both singular and plural (Statement/Statements)"**；还有 Vale 的 20-F，经营现金流合计用的是公司扩展概念，结果报表找不到([statement_resolver.py](https://github.com/dgunning/edgartools/blob/main/edgar/xbrl/statement_resolver.py))。这和旧系统的单复数问题一模一样，只是从表头挪到了 role 名上。另一个坑是，有些公司只用维度来报告报表正面的行。比如 Workday 的 COGS 只挂在 `ProductOrServiceAxis` 上，不处理维度就会得到空值([dimension-handling.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/concepts/dimension-handling.md))。没有哪个工具发布过按 role 重建报表的普查级准确率。所以风险最低的做法是按概念加 axis/member 去选事实，role 只用来说明这个数字在哪张表上。

## 收入一项就有十几种标准标签：归一化靠映射表和申报人的链接库

### 公司自定义标签不是主要麻烦，标准标签的漂移才是

SEC 对 10-K 的统计显示，2014–2020 年自定义行项目标签约占一份申报行项目标签的 16–22%，之后大型加速申报人（LAF）大致持平或略降([SEC custom tags](https://www.sec.gov/data-research/gaap-xbrl-custom-tags))；XBRL US 的说法是每年约有 19% 的概念属于扩展([XBRL US](https://xbrl.us/why-normalize-data/))。研究团队用 2026q3 FSDS（5,607 份 10-K/10-Q）实测了报表正面：大型加速申报人平均有 **8.1%** 的不同标签是自定义的（中位数 6.7%），按事实算是 6.2%。自定义标签集中在现金流量表（12.2%）和权益变动表（11.7%），资产负债表只有 3.9%；几家巨头从 Apple 的 0.4% 到 Amazon 的 8.5% 不等([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets))。两组数字的口径不同（一组是 10-K 的全部行项目，一组主要是 10-Q 的报表正面），不能直接比较，但都说明研究系统要用的数字大多带标准标签。

更大的问题是，同一件事有好几个标准标签可选。在 1,845 份大型加速申报人的申报里，损益表第一行收入用 `RevenueFromContractWithCustomerExcludingAssessedTax` 的占 59.8%，用 `Revenues` 的占 21.7%，用 `RevenueFromContractWithCustomerIncludingAssessedTax` 的占 8.1%，用自定义标签的占 3.7%，其余是 `OperatingLeaseLeaseIncome` 这类行业标签([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets))。同一家公司也会换标签：Apple 的总收入在 FY2009–2017 用 `SalesRevenueNet`，FY2018 用 `Revenues`，FY2019–2025 用 `RevenueFromContractWithCustomerExcludingAssessedTax`；NVIDIA 在 FY2019–2022 用后者，之后又换回 `Revenues`([companyfacts](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json))。SEC 在 2022 年 12 月专门提醒过，有申报人"在不同期间用不同元素标记损益表的同一行"；2023 年 11 月又提醒了同一行换标签文字的问题([SEC 提醒](https://www.sec.gov/structureddata/announcement/2212-dqreminder-different-tags-same-labels))。所以概念名和标签文字，单拿哪一个都当不了身份。

还有一种形状，直接对应旧系统"同名行被并成一个"的毛病：一个概念在同一期里装着好几个只差维度的数字。Apple 截至 2026-06-27 季度的 10-Q 里，`RevenueFromContractWithCustomerExcludingAssessedTax` 同时装着这些数：合并数 109.417bn；五个地区分部（美洲 45.781、欧洲 29.395、大中华 18.816、日本 6.554、其他亚太 8.871，加起来正好 109.417）；五个产品/服务（iPhone 54.252、Mac 10.352、iPad 6.191、可穿戴 7.883、服务 30.739）；以及产品小计 78.678([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets))。如果用"表标题 + 行标签"当键，这十几个数要么被并掉，要么被拆乱；如果用（概念 QName、完整的 axis=member 集合、起止日期或时点、单位、主体/共同申报人）当键，每个数都是唯一的。

### 现有的归一化做法：手工映射表打底，代码规则补位

开源工具都以一张手工整理的"标签 → 标准行"映射为主。edgartools 有 95 个标准概念和 2,900 多个标签映射（stable 版文档写的是 2,067 个），约 206 个有歧义的标签按计算父项、报表类型等上下文来判定，约 270 个被明确排除。文档自称覆盖"约 95% 的常见报表标签"、测过 390 多家公司，但没有独立的准确率数据([edgartools standardization](https://edgartools.readthedocs.io/en/latest/xbrl/concepts/standardization/))。secfsdstools 用改名、求和、相减等分阶段规则做标准化，并做了自查：在 346,570 行标准化后的资产负债表里，**Assets = Liabilities + Equity 精确成立的占 93.70%**，Assets = 流动资产 + 非流动资产成立的占 98.47%([secfsdstools notebook](https://raw.githubusercontent.com/HansjoergW/sec-fincancial-statement-data-set/main/notebooks/07_01_BS_standardizer.ipynb))。学术界的确定性做法来自 Du、Huddart 和 Jiang：每个 Compustat 项目对应 FASB taxonomy 里最高一层的标签，这个标签缺失时，按标准计算链接库从子项推算出来；公司自定义标签则按申报人自己的 presentation 和 calculation linkbase 放到对应的标准父项下([Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf))。欧盟 ESEF 强制要求扩展标签"锚定"到基础 taxonomy，美国只是"不禁止"，所以处理 SEC 申报时指望不上它([XBRL International](https://www.xbrl.org/enhancing-comparability-with-anchoring/)、[DQC 会议纪要](https://xbrl.us/wp-content/uploads/2020/02/DQCMeetingNotes040120.pdf))。跨年拼接有现成的数据可用：FASB 每年随 taxonomy 发布废弃关系（`dep-concept-deprecatedConcept` 等），指向替代它的元素。2026 版共废弃了 337 + 130 + 97 个元素，被废弃的元素保留两个年度版本后删除([FASB 2026 Release Notes](https://xbrl.fasb.org/resources/annualrelease/2026/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf))。综合来看，一张约一百个标准行、两三千个标签的映射表，就能覆盖大多数公司的报表正面，可以从 edgartools 公开的 JSON 起步；剩下 4–12% 的自定义标签交给申报人自己的链接库来定位，不需要逐家公司手工映射。要是退回到按标签文字匹配，就会重演旧系统的碰撞。

### 分部数据：两种标记模型并存，"按地区的营业利润"大多不存在

分部事实就是普通概念（`Revenues`、`OperatingIncomeLoss`、`CostOfRevenue` 等）加上 `us-gaap:StatementBusinessSegmentsAxis`；有调节项时再加 `srt:ConsolidationItemsAxis`（`OperatingSegmentsMember`、`CorporateNonSegmentMember`、`IntersegmentEliminationMember` 等）。FASB 2025 年的分部 taxonomy 实施指南写明了以下几点([FASB segment TIG](https://xbrl.fasb.org/impguidance/SG1_TIG/segmentreporting.pdf))。两种模型都合规：没有调节项时只用 Segments 轴，有调节项时用两个轴。分部 member 几乎都是公司扩展。ASU 2023-07 新增了 `SegmentReportingOtherItemAmount`、`SegmentExpenditureAdditionToLongLivedAssets` 和 CODM 职务元素。而且在 FASB 自己的示例里，几项重要的分部费用用的就是扩展行项目。实测巨头 2026 年最新申报里的分部营业利润：Apple、Alphabet、NVIDIA 用两个轴，Amazon、Meta、Microsoft 只用 Segments 轴；Apple 的重要分部费用 `CostOfGoodsAndServicesSold` 也按两轴分部标记([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets))。在 1,966 份大型加速申报人的申报中，75.3% 用了 BusinessSegments 轴，64.9% 用了 ProductOrService 轴，54.2% 用了 ConsolidationItems 轴，42.5% 用了 Geographical 轴；不同的 axis 名一共有 647 个（来源同上）。

所以分部抽取器的键应是（概念、Segments member、ConsolidationItems member 或缺省），并且把"只有 Segments 轴"和"Segments 轴 + `OperatingSegmentsMember`"当作同一个分部数。它还能自查：同一概念、同一期的各分部数，加上公司层面未分摊项、分部间抵销和调节项，应当等于不带维度的合并数，Apple 的收入正好成立。分部 member 是公司扩展，身份用 member 的 QName，显示时用标签链接库里的名字；member 改了名就是一个新 member，跨期要显式连起来。要特别说明的是，"按地区的分部营业利润"在大多数公司的申报里根本不存在：ASC 280 只要求按地区披露对外收入和长期资产([Deloitte Roadmap 5.5](https://dart.deloitte.com/USDART/home/codification/presentation/asc280-10/roadmap-segment-reporting/chapter-5-entity-wide-disclosures/5-5-information-about-geographic-areas))。只有像 Apple 这样本身按地区划分分部的公司才有这个数；其他公司的地区利润，只能是系统自己估出来的数。

### 数据质量：大错已经很少，剩下的是口径漂移

XBRL 早期错误很多：2009 年首批 400 家大公司的申报里，有四分之一存在计算不一致，主要原因是借贷方向（正负号）处理错了([Debreceny et al. 2010](https://ideas.repec.org/a/eee/jappol/v29y2010i3p296-306.html))。XBRL US 数据质量委员会（DQC）的规则推出第一年，全体申报人的错误下降了 64%([DQC results](https://xbrl.us/home/priorities/data-quality/filing-results/dqc-results/dqc-results-2/))。到 2026 年 9 月的 v30.0.5，规则集共有 196 条，覆盖正负号（DQC_0015）、期间（DQC_0006、DQC_0146）、axis/member（DQC_0001）、计算（DQC_0004，即 A = L + E）、数量级（DQC_0091）和元素选择（DQC_0018，废弃元素）([XBRL US rules](https://xbrl.us/home/priorities/data-quality/rules-guidance/))。其中 90 条已随 FASB taxonomy 发布([FASB 2026 Release Notes](https://xbrl.fasb.org/resources/annualrelease/2026/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf))，规则本身以 Arelle 插件的形式开源([dqc_us_rules](https://github.com/DataQualityCommittee/dqc_us_rules))。2026q3 的实测是：**5,424 份申报里，`Assets` 与 `LiabilitiesAndStockholdersEquity` 相差超过 0.05% 的有 0 份**；7,159 个期末收入事实中有 8 个是负数（0.11%），还没逐个追查([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets))。SEC 2022–2026 年的数据质量提醒集中在这些问题上：换标签、换标签文字、EPS、信用损失、`ConsolidatedEntitiesAxis` 误用（2026 年 3 月）和 Schedule III（2026 年 9 月）([SEC OSD](https://www.sec.gov/page/osdstaffobsandguide))。2023 年的样板意见函还点名了封面股数因数量级（整数还是千）标错的问题([Cooley PubCo](https://cooleypubco.com/2023/09/08/sample-comment-letter-xbrl/))。也就是说，对大公司来说，剩下的风险主要不是数字本身错，而是跨期、跨公司的口径选择不一致，以及银行、REIT 等行业里的错标。

衡量标尺也要选对。Boritz 和 No 发现，XBRL 金额与 10-K 原文不一致的只有 0.01%，而聚合商数据有 6.5–7.7% 不一致([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2253638))。Chychyla 和 Kogan 发现，30 个会计项目里有 17 个的 Compustat 值与 10-K 有显著差异([ResearchGate](https://www.researchgate.net/publication/272304077_Using_XBRL_to_Conduct_a_Large-Scale_Study_of_Discrepancies_between_the_Accounting_Numbers_in_Compustat_and_SEC_10-K_Filings))。Du 等人发现，约 32% 的股票年度在两种数据源下落进不同的应计利润五分位([Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf))。Compustat 是有意做重分类的，拿它当标尺，测的是"和 S&P 的标准化一不一致"，而不是"对不对"。一个要复现公司申报内容的系统，标尺应该是申报本身，其次是代码能做的自洽检查（计算链接库、A = L + E、分部求和）。

## MD&A 与新闻稿：维护最勤的开源解析器也重现了旧失败

哪些部分没有标签很清楚：10-K/10-Q 里 MD&A 等叙述章节的表格，以及 8-K 里全部的 EX-99.x 附件（业绩新闻稿、CFO 评论、投资者演示）。研究团队在三份最新的 10-Q 里数了一下：Apple 有 9 张不含任何 `ix:nonFraction` 的数字表（带标签的有 19 张），NVIDIA 是 14 对 32，Microsoft 是 13 对 38([AAPL 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm)、[NVDA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)、[MSFT 10-Q](https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm))。SEC 在 2018 年 12 月的征求意见里问过给业绩新闻稿加 XBRL 要花多少成本。XBRL US 在 2019 年回复说，新闻稿条目约 30% 是非 GAAP 指标，不在 US GAAP taxonomy 里；约 70% 是之后会在 10-Q 里再出现的 GAAP 数([XBRL US 意见函](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf))。此后没有任何规则要求新闻稿带标签。2026 年 5 月，SEC 反而提议允许公司改交半年报 Form 10-S，让 10-Q 变成可选。如果通过，选了半年报的公司在一、三季度就只剩新闻稿可读([Debevoise](https://www.debevoise.com/insights/publications/2026/05/breaking-the-quarterly-cycle-sec-proposes-optional))。

edgartools 是唯一还在维护、并带专门的业绩新闻稿表格解析器的开源库。它的网格层做得不错：能展开 colspan/rowspan，去掉空的间隔单元格，把拆开的 `$ | 13674` 合成 `$13,674`，把 NVIDIA 分两行写的 "October 26," 和 "2025" 接成一个日期，还会从标题、表头、前几行和表前段落里找数量级([edgartools earnings.py](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py))。文档里的"95%"指的是 8-K 章节识别的准确率；"表格抽取准确率 > 95%"在它的目标文件里还是一个没勾上的目标（来源同上）。研究团队用 5.26.1 和最新的 5.62.0 跑了 NVIDIA、Apple、Microsoft 最新的业绩 8-K，两个版本输出相同，**旧系统的失败类别几乎全部重现**([NVDA EX-99.1](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm)、[AAPL EX-99.1](https://www.sec.gov/Archives/edgar/data/320193/000032019326000018/a8-kex991q3202606272026.htm)、[MSFT EX-99.1](https://www.sec.gov/Archives/edgar/data/789019/000119312526323632/msft-ex99_1.htm))：

| 失败类别 | edgartools 的表现 |
|---|---|
| 期间写法 | 复数 "Years Ended September 27, 2025"、裸缩写 "Jul 27, 2025"、"13 Weeks Ended"、"Q2 FY26" 都解析不出期间 |
| 两行拼成的表头 | Microsoft 的 "Three Months Ended June 30, - 2026" 解析不出，导致这份新闻稿里每个事实的期间和年份都是 None |
| 财季编号 | 按日历月推算：NVIDIA 的七月季度被叫成 Q3（公司叫 FY2026 Q2）；Apple 截至 2026-06-27 的季度被叫成 Q2，起始日写成 2026-04-01 |
| 同名不同行 | Apple 销售额下和成本下的 "Products"、"Services" 被映射成同一个概念；NVIDIA 成本下和费用下两行 "Acquisition-related and other costs (A)" 也被并成一个 |
| 认错表 | NVIDIA 的 `income_statement` 取到的是非 GAAP 调节表；Microsoft 一张按三个月和十二个月分列的表被判成 BALANCE_SHEET |

更危险的是两种不报错却给出错数的情况：`1,234(1)`（数值后面跟着脚注标记）被解析成 **-12341.0**；Apple 和 Microsoft 以美元计的 "Gross margin"，因为标签里含 "margin" 被当成百分比，单位标成 `pure`，也没有乘数量级（来源同上）。这些问题都来自文档本身，不是某个工具的偶发 bug。换用这个库，只是把同样的失败搬进了依赖里。

其他工具帮不上忙。sec-parser 把整张表只当成一个元素（"Table with 24 rows, 80 numbers"），最后一版停在 2024 年 6 月([sec-parser docs](https://sec-parser.readthedocs.io/en/stable/))。sec-api 的 Extractor 是商用的章节抽取服务，不拆单元格([sec-api](https://sec-api.io/docs/sec-filings-item-extraction-api))。EDGAR-CORPUS 干脆删掉了所有表格([EDGAR-CORPUS](https://ar5iv.labs.arxiv.org/html/2109.14394))。`pandas.read_html` 能处理合并单元格，但文档直说"做好清理的准备"([pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html))。camelot 和 tabula 只处理 PDF，而 EDGAR 的正式文件是 HTML。公开的基准也测不到这件事。FinTabNet 测的是图片里的表格结构（TableFormer 的 TEDS 为 93.6%）([TableFormer](https://arxiv.org/pdf/2203.01017))。TAT-QA、FinQA、FinanceBench 测的是在已经抽好的表上回答问题，其中 FinanceBench 里带检索的 GPT-4-Turbo 有 81% 的题答错或拒答([FinanceBench](https://arxiv.org/abs/2311.11944v1))。最接近的是 2025 年的 FinTagging（30 份 2024 年的 10-K）：大模型找出数字的最佳 F1 是 0.72，但把数字对应到 US-GAAP 概念的最佳准确率只有**约 17%**([FinTagging](https://arxiv.org/html/2505.20650v1))。也就是说，模型会找数，但不会给数起对名字。

代码有一条捷径：把无标签的单元格和同一份 10-Q 的 iXBRL 事实按显示值配对。三份 10-Q 里，三位数以上的单元格能配上的比例分别是：Apple 78%（无歧义）、NVIDIA 60%（8% 有歧义）、Microsoft 78%（4% 有歧义）。而 "3"、"4"、"6" 这样的小整数，会同时等于好几个毫不相干的事实([NVDA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm))。这次配对没有看期间和数量级，也只测了三份申报，只能说明配对对 MD&A 里重复报表内容的 GAAP 大数有效。只出现在 MD&A 里的分部 KPI、百分比变化、固定汇率行配不上，它们占三位数以上单元格的 22–40%。而且数值相等不能证明是同一个数，正式采信前还要求期间和数量级也一致。新闻稿的数和后来的 10-Q/10-K 也可能对不上：AmerisourceBergen 2017 财年的净利润，10-K 里比业绩 8-K 里少了 5,000 万美元（12%）([XBRL US 意见函](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf))。至于"代码出结构、模型做标注"的混合方案：dottxt 用受约束生成输出 CSV，但没给准确率([dottxt](https://blog.dottxt.ai/extracting-financial-data.html))；Reducto 建议加一层带引用的核验([Reducto](https://reducto.ai/blog/10k-document))；ICAIF 2025 的一篇论文用表格自身的合计层级来校验模型抽取的结果([arXiv 2511.10659](https://arxiv.org/abs/2511.10659v1))。但没有一项在 EDGAR HTML 上测过逐个事实的准确率。

不读新闻稿，损失的主要是内容，不是时间。20 家大公司 2024–2026 年从业绩 8-K 到下一份 10-Q 的间隔，中位数是 **1 天**（n=165），到 10-K 是 9.5 天（n=58）。Microsoft 在发稿后 3–6 分钟就提交 10-Q；NVIDIA 自 2023 年 11 月起在 11–44 分钟后提交（2024 年 5 月有一次隔了 7 天）；Apple、Amazon、Alphabet、Meta 在当晚 17:30 以后或次日清晨提交，所以申报日落在下一个工作日。拖得久的是 Walmart（8–22 天）、UnitedHealth（13–25 天）和 JPMorgan（17–23 天）([submissions AAPL](https://data.sec.gov/submissions/CIK0000320193.json)、[submissions NVDA](https://data.sec.gov/submissions/CIK0001045810.json))。对跟踪大型科技股的产品来说，XBRL 通常一天之内就到；但新闻稿里的非 GAAP 指标、业绩指引和 KPI，永远不会出现在 XBRL 里。

## 数字身份、申报观测、发布时间必须分开记

companyfacts 的一行，意思是"某个事实在某份申报里出现了一次"：`start`/`end`/`val` 描述数字，`accn`/`form`/`filed`/`fy`/`fp` 描述申报。NVIDIA 2010-02-01 至 2010-05-02 的收入 1,001,813,000 出现了 4 次，来自四份不同的申报，只有最后一份带 `frame: CY2010Q1`([companyconcept NVDA Revenues](https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json))。7 家巨头里，约一半的期间出现在两份以上的申报中，全部期间里有 2.2–8.1% 出现过不同的值([companyfacts NVDA](https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json))。`fy`/`fp` 是申报的 DEI 字段，不是数字所属的期间。例如 Apple 2022-09-25 至 2022-12-31 这个 14 周的季度（Apple FY2023 Q1）带的是 `fy 2024, fp Q1`，因为这条记录来自 FY2024 Q1 10-Q 里的上年比较列([companyfacts AAPL](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json))。申报人的 DEI 本身也会写错：NVIDIA 2010 年的一份 10-Q 把 FY2011 Q1 标成了 `fy 2010, fp Q2`（见上面的 NVDA 链接）。期末相同、起点不同，就是两个不同的数：同一份 10-Q 里，NVIDIA 截至 2023-07-30 的收入既有 3 个月的 13,507M，也有 6 个月的 20,699M。身份键只要丢掉 `start`、单位或维度中的任何一个，不同的数就会共用一个 id，差异就会被误读成重述。旧系统就是这样出错的。

frames 总是取最后一次申报的值：7 家公司 74,939 个带 frame 的组里，frame 无一例外落在最晚申报的那一行上。结果晚到的标错也会被传下去。Amazon 2011 年二季度的净利润，原始 10-Q 报的是 191M；但 Amazon 的 FY2012 10-K 把 2012 年和 2011 年的季度日期标反了，而它又是最后一份报这个期间的申报，于是 **frames 接口至今返回 7,000,000**([frames NetIncomeLoss CY2011Q2](https://data.sec.gov/api/xbrl/frames/us-gaap/NetIncomeLoss/USD/CY2011Q2.json))。

数字后来的变化大多不是通过修正申报（10-K/A、10-Q/A）来的，而是出现在之后普通 10-Q/10-K 的比较列里。在 7 家公司里，数值第一次出现变化的地方几乎都是 10-Q 和 10-K；修正申报最多贡献了 62 处，就是 Apple 2010 年那份 10-K/A，它把 2009-09-26 的总资产从 53,851M 改成了 47,501M。Tesla 历年的 10-K/A 大多只带 2 个事实([companyfacts AAPL](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)、[companyfacts TSLA](https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json))。很多"变化"只是精度不同：按取整近似判断，NVIDIA 的 1,056 处变化里有 508 处、Tesla 的 1,058 处里有 522 处只是取整差异。真正的追溯调整例如：Alphabet 2018 年一季度营业利润从 7,001M 变成 7,633M，Microsoft 2017-06-30 的总资产从 241,086M 变成 250,312M([companyfacts GOOGL](https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json)、[companyfacts MSFT](https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json))。还有带完整财务 XBRL 的 8-K，比如 Microsoft 2024-12-03 那份 8-K 带了 572 个事实([submissions MSFT](https://data.sec.gov/submissions/CIK0000789019.json))。归纳起来，"后来出现了不同的值"至少分五类：精度变化；追溯调整（会计变更、终止经营、重新划分分部）；差错重述（常伴随 8-K Item 4.02）；后一份申报标错；身份碰撞（3 个月和 YTD 混淆、单位不同、维度不同）。只有第二、三类才是这个经济数字的新版本。companyfacts 不提供 `decimals`，要精确判定精度变化，只能借助 FSDS 的 `dcml` 或实例文件。

工具方面，edgartools 的 `pit_mode=True` 保留全部版本，`as_of(d)` 只取 `filing_date <= d` 的事实；但它的代码注释假定真正的重述"以修正申报的形式提交"，这和上面的普查结果相反([edgartools](https://pypi.org/project/edgartools/))。XBRL US 的指引是：原报数用 `ScenarioPreviouslyReportedMember` 标出，不带维度的缺省值视为重述后的数([XBRL US guidance](https://xbrl.us/guidance/reporting-restated-values-in-the-face-of-the-financials/))。一篇 2026 年的厂商教程建议用 0.5% 的容差，免得"取整噪声冒充重述"，还承认自己在审计时就在这一步发现过 bug([Tradevo](https://dev.to/tradevodata/how-to-build-a-point-in-time-fundamentals-database-from-sec-edgar-and-when-not-to-2gn6))。没有开源工具能自动标出变化的原因；能做到"原报值 + 后续版本"的，是 Compustat Point-in-Time 这类商业产品([Global Custodian](https://www.globalcustodian.com/?p=26067))。

时间戳本身也要小心。按 Regulation S-T Rule 13，美东时间 17:30 以后提交的申报算作下一个工作日提交([17 CFR 232.13](https://www.law.cornell.edu/cfr/text/17/232.13))，并且要到下一个工作日早上约 6:00 才对外发布([SEC filing status](https://www.sec.gov/page/edgar-how-do-i-determine-status-my-filing))。归档文件的 Last-Modified 也印证了这一点：例如 Alphabet 一份 10-Q 在美东 21:15:54 受理，文件到第二天美东约 06:04 才出现。NVIDIA 有一份 10-Q 在周五 19:36 受理，申报日就成了下周一([EDGAR index header](https://www.sec.gov/Archives/edgar/data/1045810/000104581023000175/0001045810-23-000175-index-headers.html))。受理时间应取自 index header 里的 `ACCEPTANCE-DATETIME`（美东本地时间，不带时区），或者带明确时区的 Atom 订阅。**2026-10-16 实测 submissions JSON 里的 `acceptanceDateTime`，7 家公司里有 6 家的 "Z" 值比真实 UTC 晚了 4–5 小时**。例如 Apple 一份在美东夏令时 16:30:28 受理的 8-K，被写成 `2026-07-31T00:30:28Z`，正确值应是 20:30:28Z；只有 Tesla 是对的。edgartools 把这个字段当成真正的 UTC 来解析，所以会继承这个偏差([submissions AAPL](https://data.sec.gov/submissions/CIK0000320193.json)、[index header AAPL](https://www.sec.gov/Archives/edgar/data/320193/000032019326000018/0000320193-26-000018-index-headers.html))。用 17:30 规则核对一下受理时间和申报日，就能发现这种偏差。

最后是财年。52/53 周财年会产生 364 或 371 天的年度、91 或 98 天的季度。frames 用 ±30 天的容差按日期把它们映射到日历标签上，用的不是公司自己的财季名([companyfacts AAPL](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json))。submissions 只给一个 `fiscalYearEnd`（Apple 是 "0926"），可 Apple 实际的年末在 9 月 24 日到 30 日之间浮动。第四季度常常没有单独的 3 个月数据：Apple 2021–2025 年、NVIDIA 2024–2026 年的 10-K 都没有，只能用全年数减去前九个月的 YTD 推出来([companyfacts GOOGL](https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json))。edgartools 只对可以相加的期间流量做这种推算，对时点数、股数、比率和每股收益则拒绝推算。它的注释里记着一次错误：把四个季度的加权平均股数直接相加，算出 Alphabet 有 485 亿股，实际约 121 亿股([edgartools](https://pypi.org/project/edgartools/))。推算出的 Q4 还必须用同一个版本的两个输入：如果 10-K 里的全年数已经重述过，而九个月数还是原 10-Q 里的值，两者相减就混用了不同版本。

## 新系统：XBRL 事实为主路径，无标签表按封闭语法拒绝其余

上游一份一份地送来已分类的申报，正好适合"逐份读 XBRL"。旧系统的五个失败分属三类：期间解析、选表、行身份。这三件事 XBRL 都已经在源头编码好了。

| 旧系统的失败 | 类别 | 10-K/10-Q 改走 XBRL 之后 | 无标签表仍需代码做的事 | 开源工具现状 |
|---|---|---|---|---|
| NVIDIA 缩写月份 | 期间解析 | 期间取自 context 的 ISO 日期，不读表头 | 封闭的表头语法要收进缩写月份和分两行写的日期 | edgartools 不认 "Jul 27, 2025" |
| Apple 复数 "Years ended" | 期间解析 | 同上 | 语法要收进 Year/Years、N Weeks Ended | edgartools 不认 "Years Ended …" |
| Microsoft 无标题表 | 选表 | 按概念 + axis/member 选事实，role 只标位置 | 按内容（期间列、行路径）认表，不靠标题 | edgartools 把 MSFT 一张表判成 BALANCE_SHEET |
| 新的分部版式 | 版式 | 同一个概念挂同样的 axis，与 HTML 版式无关 | 把跨列的表头下推到每一列 | edgartools #1449 未关闭 |
| 同名不同行被合并 | 行身份 | 不同的行是不同的概念或 member | 行身份 = 父标题路径 + 标签 | edgartools 合并了 Apple 两处 "Products" |

按上面的证据，一份申报进来后的处理路径大致如下：

```
一份已分类申报
├─ 10-K / 10-Q，以及带完整财务 XBRL 的 8-K（看 XBRL 内容判断，不看表单类型）
│  ├─ 读 _htm.xml 实例 + _pre/_cal/_def/_lab.xml + FilingSummary.xml
│  ├─ 事实身份 = (CIK, concept QName, 完整 axis=member 集合, start/end 或 instant, unit)
│  ├─ 观测 = 事实身份 × accession，附申报日和 index header 里的受理时间
│  ├─ 检查：A = L + E、分部求和 = 合并数、申报人计算链接库、正负号与数量级、同一身份出现不同值
│  └─ 归一化：标准行映射表 → 申报人 cal/pre 父项 → FASB 废弃关系
├─ 同一份 10-K / 10-Q 里的 MD&A 表
│  ├─ 网格：展开合并单元格，保留原文，每格一个 (表, 行, 列) id
│  ├─ 封闭的表头语法 + 行路径 + 封闭的数字格式，其余一律拒绝
│  └─ 与同一份申报的 XBRL 事实绑定（值、期间、数量级都一致才算）
└─ 8-K Item 2.02 的 EX-99.1 / EX-99.2
   ├─ 同样的网格和封闭语法，结果标为"初值"
   ├─ 10-Q/10-K 到来后与 XBRL 事实对账
   └─ 剩下的非 GAAP 和 KPI 行交给模型，模型只能回答单元格 id，再由代码核验
```

数字身份和观测要分开存。第一次观测到的就是"首次报告值"；之后再出现相同的值只算确认，不生成新版本；值不同时，先用 `decimals` 排除精度变化，再按上面五类之一记下取代关系。公司的财季要用 `start`/`end` 加上公司自己的财年日历推出来，不能用 `fy`/`fp`。推算出的 Q4 要记下它用到的两条输入观测，以 10-K 的申报日作为发布日；任何一条输入被取代时，它也一并失效。发布时间根据受理时间按 17:30 规则推出，受理时间取自 index header，不取 submissions JSON。8-K 走哪条路，要看 XBRL 的内容：Microsoft 2024-12-03 那份重新划分分部的 8-K 有 572 个财务事实，应该走 XBRL 路径；NVIDIA 的业绩 8-K 只有一个封面 R 文件，应该走新闻稿路径。

解析库有两种选法，证据都支持。一是 Arelle：标准覆盖最完整，是 SEC 自己用的引擎，Apache-2.0 许可，缓存好之后单份 10-K 0.7 秒。二是用标准库读 `_htm.xml` 和申报自带的链接库，只为标签、计算权重和废弃关系另外加载标准 taxonomy。edgartools 适合当映射 JSON 的来源和交叉核对的工具，不适合放在主路径上：它每周发版，输出会变，默认隐藏分部，新闻稿解析器还重现了旧的失败；真要用，就锁定版本并记下版本号。companyfacts 和 FSNDS 都不当主路径：前者用来回填合并口径的历史、核对比较列；后者用来批量回填分部和附注的历史。

无标签表这条路径，设计重点在于规定拒绝什么。表头只认一个封闭的写法集合：Three/Six/Nine/Twelve Months、Quarter、Year/Years、N Weeks Ended，月份可以是全称也可以是缩写，分两行写的要先接起来。数字单元格也只认一个封闭的格式集合，像 `1,234(1)` 这种直接拒绝，不去猜。单位按行的类型（金额、每股、股数、百分比）来定，不按标签里有没有 "margin" 这类字眼。能和同一份申报的 XBRL 绑定上的 GAAP 重复数，一次就同时完成了标注和核对。剩下的 KPI 和非 GAAP 行交给模型，模型只能用单元格 id 作答，由代码核对三件事：这个单元格存在、解析出的值就是被使用的值、各分项加总等于合计。用子串去原文里搜，能抓到模型编出来的数，却抓不到"数是对的、期间或行错了"，而这正是 edgartools 实测里最常见的失败。所以核验必须按单元格定位。

还有几件事不知道，在动手构建前应先量清楚。没有任何库发布过普查级的准确率；配对率只来自三份申报，标签覆盖率只来自两份。无标签路径最便宜的金标准是：把一份 10-Q 的 iXBRL 标签藏起来，只用 HTML 跑表格解析，再拿结果和藏起来的事实比对。这不花钱，用的是真实申报，也能把旧系统那五类失败的案例都放进去。XBRL 路径的自洽检查（A = L + E、分部求和）也可以先在存好的 FSNDS 上跑一遍，看它们实际会拦下多少数据。

## 结论

旧系统的失败不是因为正则写得不够细。同样的五类失败出现在维护最勤快的开源解析器上，说明它们是"从渲染后的文字里重建数字身份"这件事本身带来的。10-K/10-Q 改用 XBRL 事实之后，问题就从"怎么猜对"变成了"怎么选对、怎么对齐"：选对概念和维度，对齐跨期、跨公司的口径。后者可以由代码加映射表来承担，还能用会计恒等式和分部求和来自查。反过来看，衡量这条路径对不对，标尺应该是申报本身，而不是 Compustat 这类有意重分类过的数据。

需要代码抽取的范围缩到 MD&A 和新闻稿之后，设计重点就从"尽量多解析"变成了"明确拒绝什么"：封闭语法之外的一律拒绝，能和 XBRL 对上的才采信，模型只负责给剩下的单元格起名。时间是另一条独立的线：数字身份、申报观测和发布时间要分三处记。大部分"重述"其实只是比较列或取整差异，SEC 自己的 JSON 时间戳也会错几个小时，所以这些都该由代码按规则判定，不能直接信上游给的字段。
