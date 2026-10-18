# 投资观点（thesis）的存储、关联与更新：买方实践、研究管理系统、驱动因子分类法、LLM 投资智能体与事件数据产品（截至 2026-10-17）

写给报告撰写者的说明：
- 标〔厂商〕的数字或机制来自卖产品的公司本身，未经独立验证；标〔作者自报〕的是论文作者在自己系统上的回测；标〔二手〕的是转述而非原始文档；标〔旧〕的是 2023 年以前的材料。
- 标"已读代码"的条目是我用 `gh api` 直接读了 GitHub 源码（给出 commit），不是摘要。
- 本目录的姊妹笔记（`../观点库 向量检索 去重匹配/`）已覆盖 Mem0/Graphiti 等通用记忆系统的增删改流程、声明匹配文献和向量相似度的局限；这里不重复，只覆盖投资领域的做法。

## 问题 1：买方实践与研究管理系统（RMS）——如何记录 thesis、驱动因素/KPI、催化剂、止损/证伪条件，以及新信息如何挂到已有 thesis 上

### Takeaway
公开可读的买方做法把 thesis 挂在"一个持仓/一家公司"上，每个 thesis 下有 3–5 条支柱（pillar）和 3–5 条会推翻它的风险；新数据点先按公司归档，再由分析师判断它"加强、削弱还是不影响哪一条支柱"——匹配单位是"公司内的某条支柱"，而不是文本相似度。商用 RMS（Bipsync、FactSet RMS）公开文档里只写到"按公司/自定义主题打标签、AI 推荐标签"，没有公开 thesis 版本化或"thesis 漂移"检测的机制细节。

### Cited Findings
**一份公开的 thesis 跟踪规范（Anthropic 发布的金融服务插件技能，2026-05 最后修改，已读原文）**
- 新建 thesis 的字段：公司与代码、多/空、1–2 句核心 thesis（例："Long ACME — margin expansion from pricing power + operating leverage as mix shifts to software"）、"Key pillars: 3-5 supporting arguments"、"Key risks: 3-5 risks that would invalidate the thesis"、催化剂（财报、产品发布、监管决定）、目标价/估值、"Stop-loss trigger: What would make you exit" — [anthropics/financial-services thesis-tracker SKILL.md](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)（commit ef165e4，2026-05-21）
- 每个新数据点写一条更新日志：日期、数据点、"Thesis impact: Does this strengthen, weaken, or neutralize a specific pillar?"、动作（不变/加仓/减仓/退出）、更新后的信心（高/中/低）。即新信息要落到**某一条具体支柱**上 — [同上](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)
- 维护"thesis 记分卡"：每条支柱一行，列为"原始预期 / 当前状态 / 趋势"（例：Revenue growth >20% | On track | Q3 was 22% | Stable）；另有催化剂日历（日期、事件、预期影响） — [同上](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)
- 规则原文："A thesis should be falsifiable — if nothing could disprove it, it's not a thesis"；"Track disconfirming evidence as rigorously as confirming evidence"；"Review theses at least quarterly, even when nothing dramatic has happened"；"Store thesis data in a structured format so it can be referenced across sessions" — [同上](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)
- 注意：这是一份提示词规范（给 LLM 的工作流），没有存储、检索或去重的代码，也没有效果测量。

**止损/证伪条件（kill criteria）**
- 〔二手〕Annie Duke 在《Quit》（2022）中提出的 kill criteria 由"一个状态（可测量的条件）+ 一个日期（截止时间）"组成，例："If I can't get an executive in the room (the state) by the next meeting (the date), then I'll kill the deal" — [Elliot Robia, Kill Criteria (Substack)](https://elliotrobia.substack.com/p/kill-criteria)；[Penguin Random House 书目页](https://penguinrandomhouse.ca/books/692752/quit-by-annie-duke)
- 〔二手，质量一般〕投资术语页的说法：一个强的 thesis 要回答"what would change your mind?"，预先定义 kill criteria 是为了避免无限期持有亏损仓位 — [money365 术语页](https://www.money365.market/glossary/investment-thesis)

**商用 RMS 公开文档能读到的机制**
- 〔厂商〕Bipsync：Smart Tagging "recommends relevant labels for notes and files"；Toro 助手可检索整个研究库（笔记、备忘录、文档、附件）并给出综合回答、起草投委会备忘录。页面上**没有**说明笔记如何关联到 thesis/主题、没有 thesis 模板、版本化或"新旧研究对比/thesis 变化检测"的描述 — [Bipsync AI 页面](https://bipsync.com/bipsync-ai/)
- 〔厂商，仅见于搜索摘要；FactSet 宣传册 PDF 抓取时返回 404〕FactSet RMS 用于存储、分享笔记和尽调材料；"Tag Assistant auto-tags notes with custom topics"（按客户自定义主题自动打标签）；FactSet Internal Research Notes (IRN) 用于汇总、存储、检索、跟踪和分享研究 — [FactSet RMS 宣传册（链接 404）](https://insight.factset.com/hubfs/Resources%20Section/Brochures/research-management-solutions-brochure.pdf)；[airframe.ai 对 FactSet RMS 的分析页](https://www.airframe.ai/product/factset-com-products-research-management/analysis)；[SoftwareOne IRN 产品页](https://platform.softwareone.com/product/factset-internal-research-notes-irn/PCP-5812-1278)
- 〔厂商〕AlphaSense 的财报电话会 Smart Summaries：每场电话会在数小时内自动生成摘要；先用语义搜索和情绪分析识别、组织内容，再由在金融内容上微调的 LLM 合并成文字；要点按重要性排序，每条带可点击的原文引用；每份摘要含 Key Takeaways、Q&A、Guidance and Outlook，以及列出主要主题（产品发布、供应链、招聘、并购等）的 Topics — [AlphaSense 博客](https://www.alpha-sense.com/blog/product/smart-summaries-earnings-analysis/)；[AlphaSense 帮助文档：Transcript Summaries](https://help.alpha-sense.com/hc/en-us/articles/41712766038675-Transcript-Summaries)

**卖方/买方"变体认知"（variant perception）的写法**
- 〔二手，面试准备类网站，质量低〕pitch 的核心是"与共识不同、且若被广泛认识会导致价格显著不同"的洞见，加上让市场意识到的催化剂（"what will make the market realize you're right, and when"） — [dataford 面试题页](https://dataford.io/questions/pitch-me-a-stock-that-you-currently-find-highly-compelling-what-is-the-variant-perception-that-the-market-is-missing)

### Inferences
- 实践中 thesis 的"身份"由（公司/持仓，多空方向）决定，支柱是它下面的少量固定条目；新证据是"按公司路由 → 判断落在哪条支柱 → 记加强/削弱/无关"。这与我们"按受影响对象过滤 → 让 LLM 选同一驱动的候选"在结构上相同，但实践中候选集合是**某公司 thesis 的 3–5 条支柱**（很小、人工维护），而不是向量检索的 top-k。
- 实践中的证伪条件与我们设计里的"confirm/falsify conditions with deadlines"同构（状态 + 日期），这一点我们的设计与公开做法一致。
- "Track disconfirming evidence as rigorously as confirming evidence" 对应我们"方向相反 → 作为削弱证据挂上"的处理；实践中削弱证据挂在**同一条支柱**下，不另建反向 thesis。
- 实践中的单个 thesis 绑定一个持仓（单对象），而我们的"观点"像因子（一个驱动影响多个对象）；多对象的那一面在实践中由"主题/篮子"承担（见问题 2），不在单个公司 thesis 里。

### Gaps
- 没有找到任何 RMS（Bipsync、FactSet RMS、Sentieo/AlphaSense Notebook、Tegus 工作区、Bloomberg BQuant/Notes）关于 thesis 版本化、thesis 漂移检测或"新笔记自动对比已有 thesis"的公开技术文档；只有标签推荐与检索问答层面的厂商描述。
- 没有找到关于专业分析师"每家公司同时跟踪多少条活跃 thesis/支柱"的调查数据；"3–5 条支柱"只来自一份提示词规范，不是统计。
- Notion/Excel 等自建做法没有找到可引用的一手描述。

## 问题 2：实践中使用的驱动因子/主题分类法——因子与主题篮子、每家公司的 KPI 驱动树、是否维护固定的驱动清单

### Takeaway
业界有三类"驱动清单"，都是**事先固定、由人或厂商维护**的：(1) 风险因子模型（Barra USE4：60 个行业因子 + 12 个风格因子）；(2) 厂商的事件/主题分类（RavenPack 7,000+ 事件类型；Bigdata 7,000+ 主题类别；高盛 Marquee 主题篮子）；(3) 每家公司的 KPI 驱动模型（Visible Alpha 平均每家 156 个一致预期条目；Canalyst 4,000+ 家公司的驱动模型）。KPI 是"数百个条目"量级，而 thesis 支柱是"个位数"量级；把 KPI 当匹配单位会太细，把行业因子当单位会太粗。

### Cited Findings
- 〔旧，2011〕Barra US Equity Model (USE4)：60 个基于 GICS 的行业因子 + 12 个风格因子（另有国家因子），用于刻画市场与行业之外的风险来源 — [MSCI USE4 文档](https://www.msci.com/documents/10199/242721/Barra_US_Equity_Model_USE4.pdf)；[USE4 Methodology Notes (Aug 2011)](https://www.top1000funds.com/wp-content/uploads/2011/09/USE4_Methodology_Notes_August_2011.pdf)
- 〔厂商〕高盛 Marquee Flagship Baskets 是"thematic baskets designed to capture exposure to macro drivers not captured by traditional indices"，篮子主题包括通胀、ESG、碳、利率预期，以及定价权、劳动力成本、资产负债表、并购活动等"自上而下驱动"；自定义篮子按风格分为 Thematic、Factors、Momentum、Value、Sectors/Industries 等类别。总数未公开 — [Marquee Flagship Baskets](https://marquee.gs.com/welcome/products/index-solutions/flagship-baskets)；[Marquee Custom Baskets](https://marquee.gs.com/welcome/products/index-solutions/custom-baskets)
- 〔厂商〕RavenPack 追踪 1,200 万以上实体、检测 7,000 种以上事件类型、13 种语言 — [WRDS RavenPack 介绍页](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/ravenpack/)；[WRDS RavenPack one-sheet](https://wrds-www.wharton.upenn.edu/documents/1164/RavenPack-one-sheet.pdf)
- 〔厂商〕Bigdata.com 知识图谱：1,200 万以上实体（公司、组织、产品、地点等），每个实体有"unique, point-in-time-aware identifier"；7,000 以上"business, macroeconomic, and geopolitical topics"类别 — [Bigdata 文档：Knowledge Graph 介绍](https://docs.bigdata.com/getting-started/knowledge_graph/introduction)
- 〔厂商，2025-03-25 新闻稿〕Visible Alpha（2024 年被 S&P Global 收购）提供 7,300 多家公司、200 多家贡献机构、100 万以上条目的一致预期，**平均每家公司 156 个条目**（部分公司可达约 1,000 个）。这些条目包含"Company-Specific KPIs" — [S&P Global 新闻稿](https://press.spglobal.com/2025-03-25-S-P-Global-Market-Intelligence-Launches-Visible-Alpha-on-S-P-Capital-IQ-Pro-Platform)；[S&P Visible Alpha Estimates 页面](https://www.spglobal.com/market-intelligence/en/solutions/visible-alpha-estimates)
- 〔厂商，搜索摘要〕Canalyst（被 Tegus 收购，Tegus 后被 AlphaSense 收购）：4,000 多家上市公司的分析师自建可驱动模型，含"company-specific drivers, recurring KPIs and forecasts"；另有 80 多张行业比较表，带行业特有 KPI（航空的 Load Factor、Passenger Mile Yield；酒店的 Occupancy、RevPAR；企业 SaaS 的 CAC、留存率） — [AlphaSense 帮助：Canalyst Models](https://help.alpha-sense.com/en/articles/10384037-canalyst-models)；[Tegus 收购 Canalyst 公告](https://marketing.tegus.com/blog/tegus-acquires-canalyst-to-create-the-new-industry-standard-for-investment-research)
- 〔二手〕Mauboussin 与 Rappaport《Expectations Investing》的"expectations infrastructure"从影响公司表现的"triggers"追溯到"value drivers"，核心是反推股价中已计入的预期，再判断预期会如何变化 — [Shortform 书摘](https://www.shortform.com/pdf/expectations-investing-pdf-michael-j-mauboussin-and-alfred-rappaport)

### Inferences
- 三类清单的粒度差异很大：因子模型约 72 个（全市场共用）；主题/事件分类约 7,000 个（全市场共用，厂商维护）；单公司 KPI 约 156 个（一致预期条目，大多是财务行项）。thesis 的支柱是 3–5 个。我们的"驱动（driver）"若要作为匹配键，粒度应接近"支柱/主题篮子"，而不是 KPI 行项或事件类型。
- 高盛主题篮子在结构上正是"一个驱动 → 一组受影响标的（带权重/方向）"，与我们"观点像因子、影响多个对象并各自标正负"的设计最接近；业界的做法是**先有驱动（篮子）再挂标的**，篮子由人定义和维护。
- KPI 驱动树（Canalyst/Visible Alpha）适合作为证据的"数字落点"（证据引用哪个 KPI），而不是观点身份本身——这与 AGENTS.md 第 8 节"财务报表行项是证据，不是定义"一致。
- 实践中没有"每家公司固定驱动清单"由机器生成的公开先例：行业 KPI 清单由厂商分析师按行业维护；公司特有 KPI 由建模分析师维护。

### Gaps
- 摩根士丹利主题篮子、Bloomberg 主题、AlphaSense Themes 的分类数量和维护方式没有找到公开文档。
- 没有读到《Expectations Investing》原文中 value triggers / value factors / value drivers 的具体清单（如"turbo trigger"概念）；上面只引用了书摘层面的描述。
- 没有找到买方机构"每家公司维护固定驱动清单"的调查或一手描述。

## 问题 3：带记忆的 LLM 投资智能体（2023–2026）——如何存储洞见/信念、如何为新信息检索、如何更新或去重，记忆的实测效果

### Takeaway
学术界的金融智能体（FinMem、FinAgent、FinCon、HedgeAgents、MarketSenseAI 2.0）都把记忆当作"可检索的历史条目库"：用向量相似度（多加近因、重要性加权）取 top-K（K=3–10），**没有一个做去重或合并**，也没有一个评估"新信息是否被挂到正确的旧条目"。它们报告的记忆效果来自单只股票、几个月窗口、作者自报的回测，且不单调（FinMem 的 K=3 比 K=1 差）。维护最久的开源项目 TradingAgents 的演化值得注意：从向量检索（2025-06）→ BM25（2026 年初）→ 2026-04 完全放弃相似度检索，改为按"代码 + 时间"取最近记录的只追加日志，并以（代码，日期）做幂等去重。

### Cited Findings
**FinMem（arXiv 2311.13743，2023-11；ICLR 2024 相关活动）〔旧〕**
- 记忆条目 = 摘要文本 + 时间戳 + 向量（text-embedding-ada-002）+ 层级与重要性元数据。长期记忆分三层：浅层（每日新闻，Q=14 天）、中层（10-Q，Q=90 天）、深层（10-K，Q=365 天） — [FinMem 论文](https://arxiv.org/html/2311.13743)
- 检索打分 γ = 近因 + 相关性 + 重要性；近因 = e^(−δ/Q_l)；相关性 = 事件向量与查询向量的余弦；重要性 = v × α_l^δ，α 分别为 0.9 / 0.967 / 0.988。每层取 top-K，工作记忆容量 3K。被频繁访问的条目升层（升层时近因重置为 1.0）；近因 < 0.05 或重要性 < 5 时清除。没有去重或合并机制 — [FinMem 论文](https://arxiv.org/html/2311.13743)
- 〔作者自报〕K 的消融（仅 TSLA，2022-06-16 至 2022-12-28）：K=1 累计收益 52.09%、Sharpe 1.86；K=3 29.44%、1.12；K=5 54.70%、2.50；K=10 79.44%、2.75。作者称 K=5 最优（波动和回撤最低） — [FinMem 论文](https://arxiv.org/html/2311.13743)

**FinAgent（arXiv 2402.18485，2024；会议归属 KDD 2024 未核实）**
- 市场情报模块分"最新"和"过往"两部分；最新情报除了给交易用的摘要，还额外生成一个**专门用于检索的查询文本**；"多样化检索"按 M 种检索类型（短/中/长期影响、价格走势、趋势等）各取 top-K，共 M×K 条；另有低层反思记忆（价格走势分析）和高层反思记忆（交易决策分析），都按向量相似度匹配 — [FinAgent 论文](https://arxiv.org/html/2402.18485)
- 〔作者自报〕TSLA 消融（年化收益 ARR）：仅市场情报 39.01% → 加低层反思 57.16% → 加高层反思 89.25% → 全系统 92.27%；AAPL 上有/无多样化检索的对比只给了"更好"的定性结论 — [FinAgent 论文](https://arxiv.org/html/2402.18485)

**FinCon（arXiv 2407.06567，2024；会议归属 NeurIPS 2024 未核实）**
- "投资信念"是从交易轨迹中提炼出的概念化洞见（历史动量、新闻洞见、批评观点等方面）。跨回合更新：比较两个回合中持续盈利和持续亏损的交易，分别生成概念化洞见，以两回合交易决策序列的**重合百分比**作为"学习率"τ，用 meta-prompt 对提示文本做"文本梯度"更新（θ ← M_r(θ, τ, meta_prompt)）。分析师的程序性记忆按数据源时效设不同衰减率，检索按近因/相关性/重要性（FinMem 的简化版） — [FinCon 论文](https://arxiv.org/html/2407.06567)
- 〔作者自报〕有/无跨回合信念更新：GOOG 累计收益 −11.944% → 25.077%（Sharpe −0.496 → 1.052）；NIO 8.197% → 17.461%；组合（TSLA/MSFT/PFE）28.432% → 113.836%（Sharpe 1.181 → 3.269）；作者称约 4 个训练回合即收敛 — [FinCon 论文](https://arxiv.org/html/2407.06567)
- 注意：FinCon 的"信念"是一段被反复改写的提示文本，不是可寻址的观点记录；没有"一条信念一个 id"的概念。

**HedgeAgents（arXiv 2502.13165，WWW 2025）**
- 三种记忆：市场信息记忆（每日市场信息与汇总查询 Q_t）、投资反思记忆（决策时的反思和动作）、通用经验记忆（"经验分享会"上由 LLM 合成的典型案例与同伴洞见）。检索：从当日数据构造汇总查询 Q_t，用 text-embedding-3-large 在**全部记忆**中取 K=5 条相似案例。没有描述去重/合并/遗忘 — [HedgeAgents 论文](https://arxiv.org/html/2502.13165v1)
- 〔作者自报〕附录 B：开启记忆检索使年化收益提高 57.71%、Sharpe 提高 39.3%（相对值）；〔二手摘要〕系统声称 3 年总收益 400%、年化 70% — [HedgeAgents 论文](https://arxiv.org/html/2502.13165v1)；[alphaXiv 概览](https://www.alphaxiv.org/overview/2502.13165)

**MarketSenseAI 2.0（arXiv 2502.00415，2025）**
- 新闻智能体做"渐进式摘要"："Each day's raw text is first distilled into a concise summary, which is then integrated with previous summaries to form a progressive narrative"，使"older but still-relevant news (e.g., open legal cases)"留在上下文中。SEC 文件和电话会经三步 LLM 处理（文件摘要、电话会摘要、基本面合并）；宏观报告语义分块存向量库，用 HyDE 对一组固定查询检索 — [MarketSenseAI 2.0 论文](https://arxiv.org/html/2502.00415v2)
- 〔作者自报〕HyDE 取 top-7 块：召回 0.91、精确 1.00、相关度 0.66、忠实度 0.98；加入 SEC 文件和电话会后约 5% 的信号从买/卖变为持有；S&P 100（2023–2024）累计收益 125.9% vs 指数 73.5%。论文没有描述按股票保存的历史观点或其更新/去重 — [MarketSenseAI 2.0 论文](https://arxiv.org/html/2502.00415v2)；[arXiv 摘要页](https://arxiv.org/abs/2502.00415v1)

**TradingAgents（arXiv 2412.20138 v7，2025-06-03；代码已读）**
- 论文：智能体之间通过结构化报告（分析师报告、交易员决策报告、辩论记录）存入"全局状态"而非长对话；论文未描述跨交易日的长期记忆或检索方法 — [TradingAgents 论文 v7](https://arxiv.org/html/2412.20138)
- 已读代码，v0.1.0（commit cc97cb6，2025-06-05）：`FinancialSituationMemory` 用内存版 ChromaDB + text-embedding-ada-002，存（市场情形，建议）对，查询默认 `n_matches=1` — [memory.py @ cc97cb6](https://github.com/TauricResearch/TradingAgents/blob/cc97cb6/tradingagents/agents/utils/memory.py)
- 已读代码，2026-02（commit d4dadb8）：改为 `rank_bm25` 的 BM25 词法匹配（"no API calls"） — [memory.py @ d4dadb8](https://github.com/TauricResearch/TradingAgents/blob/d4dadb8/tradingagents/agents/utils/memory.py)
- Issue #563 指出：BM25 记忆只存在内存里，进程重启即丢失；按请求新建实例的服务用法下记忆"zero benefit"；示例和 CLI 从不调用 `reflect_and_remember()` — [Issue #563](https://github.com/TauricResearch/TradingAgents/issues/563)
- 已读代码，2026-04-25（v0.2.4，commit 6abc768/ebd2e12 "replace per-agent BM25 memory with persistent append-only decision log"）及其后修复：现行 `tradingagents/memory/log.py` 是只追加的 markdown 日志，每条以 `[日期 | 代码 | 评级 | pending]` 开头；**幂等去重**："Any entry for this ticker and date blocks another, pending or settled"（2026-09-16 修复"已结算决策被记录两次"）；检索 `get_past_context(ticker, n_same=5, n_cross=3, as_of)` 只按"同代码最近 5 条 + 其他代码最近 3 条反思"取，**不做任何相似度检索**；`as_of` 过滤只注入在该日期前已出结果的教训（防止回测前视，issue #1251，2026-08-30） — [log.py](https://github.com/TauricResearch/TradingAgents/blob/main/tradingagents/memory/log.py)；[提交历史](https://github.com/TauricResearch/TradingAgents/commits/main/tradingagents/agents/utils/memory.py)
- 已读代码：结算（`settlement.py`）在持有窗口（默认 5 个交易日）走完后才计算原始收益与相对基准（默认 SPY）的超额，窗口未走完就保持 pending；反思（`reflection.py`）提示词要求 2–4 句，并明说"a thesis written for months is not disproved by a week"，要模型在窗口太短时直说无法判断 — [settlement.py](https://github.com/TauricResearch/TradingAgents/blob/main/tradingagents/memory/settlement.py)；[reflection.py](https://github.com/TauricResearch/TradingAgents/blob/main/tradingagents/memory/reflection.py)

**AlphaAgent（arXiv 2502.16789，2025；会议归属 KDD 2025 未核实）——"因子"去重的结构化做法**
- 原创性约束：新因子与已有因子库（Alpha101）比较抽象语法树（AST），相似度 = 最大同构子树的节点数，原创性分 = 与库中任一因子的最大相似度；与"假设–因子一致性"（LLM 打 0–1 分：描述是否实现了假设、公式是否符合描述）和复杂度约束一起作为正则项。论文未给出拒绝阈值 — [AlphaAgent 论文](https://arxiv.org/html/2502.16789v1)
- 〔作者自报〕去掉原创性约束后命中率 0.16，有约束时 0.29（CSI 500 与 S&P 500，2021-01 至 2024-12）；论文说成功和失败的因子会写入知识库，但没有说明新假设如何与旧假设比较 — [AlphaAgent 论文](https://arxiv.org/html/2502.16789v1)

### Inferences
- 学术金融智能体的"记忆"解决的是"给当前决策找相似的历史情形"，不是"维护一个不重复、可更新的观点库"；它们没有观点身份（id）、没有合并、没有失效状态，因此对我们"同一观点挂证据 / 反向削弱 / 新建 / 可逆合并"的核心问题**没有可借鉴的已测机制**。
- 它们报告的记忆增益（FinMem、FinAgent、FinCon、HedgeAgents）都是作者在少数标的、短窗口上的回测，且有不单调现象（FinMem K=3 < K=1），按 AGENTS.md 第 6 节"模型调用是采样器"的标准，这些数字不能当作"记忆有效"的证据。
- TradingAgents 的演化是一个反向信号：在实际使用中，相似度检索（向量→BM25）被换成了"按键（代码）+ 时间"的确定性检索，去重也落在键（代码，日期）上，由代码而非模型判断。这支持我们备选方案中的"按对象取全部活跃观点"或"驱动注册表"，而不是更深的向量检索。
- AlphaAgent 的做法说明：当对象有结构（公式/AST）时，去重用结构比较而不是文本向量。对应到我们：观点的结构化字段（驱动 id、受影响对象集合及正负、方向、期限）可以由代码比较，文本相似度只用于召回候选。
- TradingAgents 的结算与反思设计（窗口走完才结算、窗口短于 thesis 期限时不判死）与我们"关闭前由 LLM 复核全部证据的最终裁决"一致，也提示裁决要带"观察窗口是否够长"的判断。

### Gaps
- FinRobot、AlphaAgents（BlackRock，2025）、以及 2026 年新出的金融研究智能体的记忆/观点库机制未在本次查到；不确定它们是否有观点去重。
- 所有论文都没有"新信息挂到旧条目的准确率"一类的评测；无法给出可比的匹配精度数字。
- FinMem 的会议归属（ICLR 2024 主会还是 workshop）未核实。

## 问题 4：事件驱动信息产品（RavenPack、Bigdata.com、Kensho、AlphaSense）——如何把新闻映射到实体和事件类型、如何对重复报道去重（新颖度），有何准确率记录

### Takeaway
RavenPack 的去重不是文本相似度，而是**按键 + 时间窗**：同一实体 + 同一事件类别构成"相似事件"，24 小时窗口内的首条报道新颖度 ENS=100，后续相关报道打折；更长的"相似事件间隔天数"（2014 年文档为 100 天，2017 年文档为最长 365 天）用于筛出"很久没发生过"的事件。实体映射靠固定知识库 id（RavenPack/Bigdata 1,200 万实体、时点感知 id；Kensho 链接到 Capital IQ 2,500 万公司）。各厂商都没有公开新颖度或去重的准确率；Kensho 只公开了置信度阈值建议，并说明分数不是概率。

### Cited Findings
- 〔厂商〕RavenPack 把数据组织为五个维度：实体、事件、相关度（实体在事件中的参与深度）、新颖度（"whether a detected event is new, a repeat, or a continuation of a pre-existing event or theme"，跨所有数据源）、情绪 — [Celent 对 RavenPack 的介绍](https://www.celent.com/solutions/676764665)；[Finextra：RavenPack 升级 RPNA](https://www.finextra.com/pressarticle/56610/ravenpack-upgrades-rpna)
- 〔二手：学术论文转述 RavenPack 使用指南，2023〕REL（相关度）0–100，表示新闻与某公司关联多强，0 = 顺带提及，100 = 相反；75 被视为显著相关（指南建议的过滤阈值）。ENS（事件新颖度）0–100，"indicates the novelty of a news story within a 24-hour time window. A score of 100 means that a news story was not already covered by earlier announced news, while subsequently published news story score on a related event is discounted" — [Panel Data Nowcasting（arXiv 2307.02673）在线附录](https://arxiv.org/pdf/2307.02673)
- 〔厂商研究，旧，2014-10-01〕"Event Similarity Gap"= 自上次检测到相似事件以来的天数，把新颖度窗口从 24 小时延长到 100 天；文中"相似事件"指同一实体、同一事件类别。只保留间隔 > 90 天的事件后，Russell 2000 多空策略 Sharpe 从 1.03 升到 1.43（2007-01 至 2014-08） — [RavenPack 研究：Systematically Trading Infrequent News](https://www.ravenpack.com/research/systematically-trading-infrequent-news)
- 〔厂商博客，旧，2017-04-25〕新版 RavenPack Analytics：检测事件数量增加 4.7 倍；Event Relevance 0–100 表示事件在文档中的显著程度；Event Similarity Days 记录"days required since a similar event was detected in the past (up to 365 days)"；称信息比率最多提高 50%。计算细节需索取白皮书 — [RavenPack 博客](https://www.ravenpack.com/blog/new-ravenpack-analytics-event-detection)
- 两份 RavenPack 材料对相似间隔窗口的说法不同（2014 年 100 天 vs 2017 年最长 365 天），应是产品版本差异；均未公开算法或准确率。
- 〔厂商〕Bigdata.com：实体有时点感知的唯一 id，可跨服务按实体检索以"higher precision and reduces noise"；7,000+ 主题类别；来源可按名称、来源等级、国家过滤；文档未描述去重/新颖度算法或准确率 — [Bigdata 文档](https://docs.bigdata.com/getting-started/knowledge_graph/introduction)
- 〔厂商〕Kensho NERD：识别文本中的实体并链接到 S&P Capital IQ（"25 million public and private companies"）和 Wikimedia（"more than 92 million data items"）；靠上下文消歧（例：微软电话会里的 "Apple" 是 Apple Inc. 而非 Apple Bank）。建议阈值：Capital IQ 链接 ned_score > 0.9（偏召回）/ > 0.95（平衡）/ > 0.98（偏精确）；Wikimedia > 0.0 / > 0.15 / > 0.25。分数"not probabilities, percentages, or linearly related"；NED 分数在重训练之间较稳定，NER 分数"fluctuate substantially"；在 HTML 表格、句子片段、列表上效果下降。只声称"approaches human labeling accuracy"，没有公开 P/R — [Kensho NERD FAQ](https://docs.kensho.com/nerd/faq)
- 〔厂商〕AlphaSense Smart Summaries 的主题列表和引用机制见问题 1；没有公开主题如何跨文档归并或去重 — [AlphaSense 帮助文档](https://help.alpha-sense.com/hc/en-us/articles/41712766038675-Transcript-Summaries)

### Inferences
- RavenPack 的新颖度设计与我们的"证据去重"问题直接对应：判断"是否重复"的单位是（实体，事件类别）这样的键，再加时间窗；首条记满分，后续转载打折。这符合 AGENTS.md"重复不是新证据"的原则，且由代码决定，不需要模型判断。对我们而言，证据层可用（对象，驱动，来源事件）+ 时间窗做新颖度；观点层的"同一观点"判断仍需要模型。
- 厂商普遍把"实体 id + 固定分类 id"作为一切下游匹配的骨架；文本向量只用于检索（Bigdata 把每个段落嵌入用于搜索），不用于判断身份。
- 实体链接的置信度阈值要按用途分开设定（Kensho 给出三档），且模型重训练后分数会漂移——如果我们用 LLM 或向量分数作门槛，阈值需要随模型版本重新校准。

### Gaps
- RavenPack 原始使用指南（字段 ENS_KEY、ENS_SIMILARITY_GAP 等的正式定义、事件分类的层级结构 topic/group/type/sub-type/property/category）未能读到原文；层级名称只见于搜索摘要，未核实。
- 没有任何厂商公开新颖度/去重/事件分类的准确率；Kensho 也无 P/R 数字。
- Bigdata.com 与 RavenPack 的公司关系（两者数字"1,200 万实体、7,000+ 类别"相同）未在本次读到的页面中核实。

## 问题 5：实践对我们匹配设计的启示——匹配单位（thesis、驱动、KPI）、每个对象的规模、由谁维护清单

### Takeaway
所有可读到的实践和产品都把"身份判断"放在**固定、可寻址的键**上（公司 + 支柱；实体 + 事件类别；代码 + 日期；因子库 + 结构比较），文本相似度最多用于召回；清单由人（分析师、厂商）维护，机器只推荐标签。规模上，每个公司 thesis 只有 3–5 条支柱，远小于我们设计中的"向量 top-20 → top-4"所假设的候选规模。因此"驱动注册表 + 按对象取全部活跃观点给 LLM"更接近业界做法；纯向量召回链路在业界没有已测的先例。

### Cited Findings
- 匹配单位为"公司内的支柱"：新数据点判定"strengthen, weaken, or neutralize a specific pillar"，每家公司 3–5 条支柱、3–5 条推翻风险 — [thesis-tracker SKILL.md](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)
- 匹配单位为"实体 + 事件类别 + 时间窗"：RavenPack ENS（24 小时）与相似事件间隔（100 天 / 最长 365 天） — [RavenPack 2014 研究](https://www.ravenpack.com/research/systematically-trading-infrequent-news)；[RavenPack 2017 博客](https://www.ravenpack.com/blog/new-ravenpack-analytics-event-detection)
- 匹配单位为"代码 + 日期"，检索按代码 + 近因、不用相似度：TradingAgents 现行日志 — [log.py](https://github.com/TauricResearch/TradingAgents/blob/main/tradingagents/memory/log.py)
- 匹配单位为"结构"：AlphaAgent 以 AST 最大公共子树比较新旧因子 — [AlphaAgent 论文](https://arxiv.org/html/2502.16789v1)
- 驱动清单由人或厂商维护：高盛主题篮子（人定义的驱动 → 标的组）；Canalyst 行业 KPI 由"sector-focused analysts"建；RMS 自动打标签用的是客户自定义主题（FactSet Tag Assistant）或推荐标签（Bipsync） — [Marquee Flagship Baskets](https://marquee.gs.com/welcome/products/index-solutions/flagship-baskets)；[AlphaSense 帮助：Canalyst Models](https://help.alpha-sense.com/en/articles/10384037-canalyst-models)；[Bipsync AI](https://bipsync.com/bipsync-ai/)
- 规模参照：单公司 KPI 一致预期平均 156 条〔厂商〕；全市场风险因子 72 个〔旧〕；厂商事件/主题类别 7,000+〔厂商〕 — [S&P 新闻稿](https://press.spglobal.com/2025-03-25-S-P-Global-Market-Intelligence-Launches-Visible-Alpha-on-S-P-Capital-IQ-Pro-Platform)；[MSCI USE4](https://www.msci.com/documents/10199/242721/Barra_US_Equity_Model_USE4.pdf)；[WRDS RavenPack](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/ravenpack/)
- 定期复核是实践要求（"at least quarterly"），结算要等观察窗口走完（TradingAgents 默认 5 个交易日，且提醒窗口短于 thesis 期限时不能判死） — [thesis-tracker](https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md)；[reflection.py](https://github.com/TauricResearch/TradingAgents/blob/main/tradingagents/memory/reflection.py)

### Inferences
- **匹配单位**：业界的身份单位相当于我们的"驱动（driver）"，而不是"一句话 claim"或 KPI。建议把"同一观点"拆成两步：(1) 驱动身份——新候选是否属于某对象已登记的某个驱动（按对象路由后在一个小集合里由 LLM 选，或新建驱动）；(2) 观点身份——同一驱动下，方向与期限由代码比较（同向同期限 → 挂证据；反向 → 削弱证据；不同期限 → 另一观点）。这与我们现稿最后一步"代码比较方向和期限"一致，差别在第一步用注册表代替向量 top-20。
- **规模估算（估计，需用我们自己的数据计数）**：若每个对象活跃驱动在个位数到十几个（参照 3–5 条支柱），一篇文档涉及 1–4 个对象，则"把相关对象的全部活跃观点一次给 LLM"约为几十条观点；按每条约 200–400 token 估算为约 1 万 token 量级。这只是估计，必须先在我们存量数据上统计"每对象活跃观点数"的分布（尤其是宏观/行业对象，可能挂着大量观点，是长尾）。
- **因子型观点的特殊性**：我们一个观点影响多个对象，实践中对应"主题篮子"。按对象取全部活跃观点时，一个宏观驱动会出现在很多对象的列表里；注册表应以驱动为主键、对象列表为属性（像篮子），而不是在每个对象下各存一份，否则会制造重复。
- **谁维护清单**：业界没有让机器自由新建驱动的先例；人或厂商维护清单，机器推荐。对我们而言，"新建驱动"应是比"挂证据"更严格的路径（例如要求新驱动与该对象现有驱动逐一比较后才允许建立，并可被后续合并）；可逆合并正是为这一步的错误兜底。
- **证据去重与观点去重分层**：RavenPack 的做法说明证据层的"重复报道"可由键 + 时间窗在代码里处理，不必进入 LLM 匹配；进入 LLM 的只剩"观点身份"判断，候选集合更小。
- **不应借鉴的部分**：学术智能体的"向量 top-K 相似情形检索"解决的是另一个问题（找类比），且没有去重；不能用它们的记忆增益数字支持我们的检索设计。

### Gaps
- 没有找到任何公开系统同时满足"多对象因子型观点 + 自动新建/合并 + 有匹配准确率测量"；我们的设计在这一点上没有可直接对照的先例。
- 专业分析师每个名字跟踪的活跃 thesis/驱动数量、以及跨公司主题由谁维护，没有调查数据；上面的规模只能用我们自己的存量数据来定。
- "全部活跃观点一次给 LLM"在长列表下的选择准确率（例如列表 50+ 条时是否下降）没有在投资领域找到测量；需参考姊妹笔记中关于长上下文/列表选择的研究，或用我们的数据实测。
