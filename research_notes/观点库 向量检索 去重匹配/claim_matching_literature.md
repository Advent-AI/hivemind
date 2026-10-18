# 声明匹配、语义去重与事件共指：判断"新观点/新证据是否已存在"的文献与评测（截至 2026-10）

说明（写给报告撰写者）：
- 数字均注明数据集与指标。凡标"已核对原文"的数字，是我从论文 PDF/HTML 原文表格中逐字读出的；WebFetch 的小模型摘要曾对 Shaar 2020 给出与原文不符的数字（已弃用），因此关键数字都以原文为准。
- 2020–2022 的结果属于"较旧"结果（BERT 时代），标注〔旧〕。基准结果与生产报告分开标注：除 RavenPack/Bigdata 两条外，下面全部是基准（benchmark）结果。
- 我方内部研究（Apple/Amazon/Meta 声明级）作为对照：同一句子跨季度 cosine 0.988；cosine≥0.95 的对里仅 34% 是真重复；text-embedding-3-large top-4 召回 99% 的已知重述；LLM 在候选中选择 P=0.975 / R=0.76；逐对 LLM 判官 P=0.99 / R=0.32。

## 问题 1：声明检索 / "检测已核查过的声明"（CheckThat! 2020–2025、Shaar 2020、MultiClaim/SemEval-2025 Task 7）

### Takeaway
最强流水线一律是"检索（BM25 + 稠密向量，微调时加 BM25 难负例）取 top-20~100 → 交叉编码器或 LLM 重排"，在自含式短文本（推文 vs Snopes）上 MAP@5 达 0.88–0.96、多语言 success@10 达 0.96；但当输入是口语化、依赖上下文的发言（政治辩论/演讲——与财报电话会最像）时，最好成绩只有 MAP@5 0.35–0.46，2021 年甚至没有队伍打败 BM25 基线。难点不是向量模型，而是输入需要"去语境化/规范化"、以及话题相同≠可被同一核查覆盖。

### Cited Findings
- 〔旧，已核对原文〕Shaar et al. 2020（ACL）首次定义任务：PolitiFact 数据集 768 对"输入–已核查声明"（输入是 2016 美国总统辩论句子），检索库 16,636 条已核查声明；Snopes 数据集 1,000 对（输入是推文），检索库 10,396 条 — [Shaar et al. 2020](https://arxiv.org/abs/2005.06058)
- 〔旧，已核对原文〕难度分析：人工标注 100 对 PolitiFact 样本，48% 属于"Type-2"（无法靠近似字符串匹配找到）；TF-IDF cosine > 0.25 的真匹配对，PolitiFact 只有 27%，Snopes 有 50% — [Shaar et al. 2020](https://arxiv.org/abs/2005.06058)
- 〔旧，已核对原文〕PolitiFact 测试集：BM25 匹配核查文章正文（IR:Body）MRR 0.565 / MAP@5 0.546 / HasPositive@5 0.653；sentence-BERT-large 只匹配声明 MRR 0.395；把 BM25 与 SBERT（声明+标题+正文前 4 句）分数作为特征，用 rankSVM 重排 BM25 top-100：MRR 0.608 / MAP@5 0.588 / HasPositive@5 0.685 / HasPositive@20 0.787 — [Shaar et al. 2020](https://arxiv.org/abs/2005.06058)
- 〔旧，已核对原文〕Snopes 测试集：BM25（声明+标题）MRR 0.664 / MAP@5 0.600；SBERT-large 0.543；rankSVM 重排 top-50 达 MRR 0.788 / MAP@5 0.782 / HasPositive@5 0.894。重排深度：PolitiFact 在 top-100 最好、超过后下降；Snopes 在 top-50 最好（初检越强，需要重排的深度越浅）。作者还发现未微调的 BERT/RoBERTa 句向量"完全无关的声明之间 cosine 也常常很高"，故改用 SBERT — [Shaar et al. 2020](https://arxiv.org/abs/2005.06058)
- 〔旧〕CheckThat! 2020 Task 2（推文 vs Snopes）：冠军 Buster.AI MAP@5 0.929，前两名远超其余队伍 — [CheckThat! 2020 overview](https://arxiv.org/abs/2007.07997)
- 〔旧，已核对原文〕CheckThat! 2021 Task 2A（英文推文，1,401 条输入，检索库 13,835 条 Snopes 声明）：冠军 Aschern（TF-IDF + 微调 SBERT + LambdaMART 重排）MAP@5 0.883 / MRR 0.884，比 Elastic Search 基线（0.749）高 13.4 点；阿拉伯语 bigIR（BM25 取 top-20 → 微调 AraBERT 重排，负例取自 BM25 高位非正例）MAP@5 0.908 vs 基线 0.794 — [CheckThat! 2021 overview](https://arxiv.org/abs/2109.12987)
- 〔旧，已核对原文〕CheckThat! 2021 Task 2B（政治辩论/演讲，669 条输入，检索库 19,250 条 PolitiFact）：**没有任何队伍打败 BM25 基线**（基线 MAP@5 0.346；DIPS 0.328；BeaSku 用三元组损失微调 SBERT + BM25 特征 rankSVM，0.327）— [CheckThat! 2021 overview](https://arxiv.org/abs/2109.12987)
- 〔旧，已核对原文〕CheckThat! 2022 Task 2A（英文推文，检索库 13,835）：冠军 RIET Lab（sentence-T5 召回，用 MNR 损失 + BM25 难负例微调；GPT-Neo 生成式重排）MAP@5 0.956 / MRR 0.957；第二 AI Rational（SBERT + ElasticSearch + SVM）0.922，并指出对 MAP@k/P@k 而言"重排等价于分类"；Task 2B（辩论，检索库 20,771）最好 SimBa MAP@5 0.459（四种句向量各取 top-50 的并集做 blocking，再用线性 SVC 判别）— [CheckThat! 2022 Task 2 overview](https://ceur-ws.org/Vol-3180/paper-29.pdf)
- SemEval-2025 Task 7（MultiClaim：205,751 条已核查声明、28,092 条社媒帖、27 种语言、31,305 对）：指标 success@10；单语轨冠军 PINGAN AI 0.9601，跨语轨冠军 0.85875；基线 E5-Large 0.8589、BM25 0.8123、GTR-T5-Large 0.7299（单语）。跨语比单语低 10+ 个百分点；未见语言（土耳其语、波兰语）明显更差 — [SemEval-2025 Task 7 overview](https://arxiv.org/abs/2505.10740)
- SemEval-2025 Task 7 的主流有效做法：用 in-batch negatives 做对比学习微调嵌入模型，加难负例进一步提升；多阶段流水线（召回 top-50 → 重排 → 加权投票）。例如 TIFIN India：Stella 400M 嵌入取 top-50 → Qwen2.5-72B-Instruct 提示式重排 → 与嵌入 top-10 做 Reciprocal Rank Fusion；重排与投票带来的提升在跨语设置中更大 — [SemEval-2025 Task 7 overview](https://arxiv.org/abs/2505.10740)
- CheckThat! 2025 Subtask 4b（社媒帖 → 科学论文来源检索，MRR@5）：BM25 基线约 0.43；第 3 名混合检索+重排 MRR@5 0.6643；DS@GT 0.58（30 队中第 16）— [Deep Retrieval at CheckThat! 2025](https://arxiv.org/abs/2505.23250)；[DS@GT at CheckThat! 2025](https://arxiv.org/abs/2507.06563)
- 声明匹配的定义（Kazemi et al. 2021）："识别包含可由同一篇核查文章服务的声明的消息对"；数据来自 WhatsApp tipline，5 种语言；自训蒸馏嵌入模型在所有设置下超过 LASER 与 LaBSE — [Kazemi et al. 2021](https://aclanthology.org/2021.acl-long.347/)
- LLM 直接判对（Pisarevskaya & Zubiaga，COLING 2025，已核对原文）：ClaimMatch 测试集 1,000 对（500 正/500 负，源自 CheckThat 2022 英文），二分类"两条声明能否用同一证据核查"。基线：微调 XLM-R F1 96.2；All-MiniLM 余弦 76.6；OpenAI text-embedding-3-small 余弦 77.2。零样本最佳单模板约 88–91 F1（GPT-3.5 89.2、Gemini 90.7）；系统+用户提示组合 NLI-5+PD-6 模板，零样本 GPT-3.5 96.1、Gemini 97.1，few-shot Gemini 97.2，但 few-shot 下 GPT-3.5 掉到 59.5、Llama 掉到 48.0 — [Pisarevskaya & Zubiaga 2025](https://arxiv.org/abs/2501.10860)
- 同上的错误分析：模型会因"非实质性细节差异"拒绝本应匹配的对（如 70 mph vs 72 mph 限速的同一执法行动）；NLI 式"真/假"措辞会诱使模型去核查事实而不是做匹配；"含义相同"类模板会因一方多出子声明而拒绝匹配；Llama few-shot 时会拿测试声明去比示例 — [Pisarevskaya & Zubiaga 2025](https://arxiv.org/abs/2501.10860)
- LLM 判"相关"（Vykopal et al. 2025，已核对原文）：AMC-16K（MultiClaim 子集，8K 单语 + 8K 跨语对，20 种语言，仅 16% 为相关），7 个 LLM；最好的单语 Macro-F1 超过 80%，70B+ 模型稳定优于小模型；跨语平均降约 4.5%；翻译成英文对多数模型有利（Llama3.1 few-shot 提升 16% Macro-F1），但多语模型 Command R+ 用原文更好。**假阳性中约 65% 是"仅因话题相同而判为相关"** — [Vykopal et al. 2025](https://arxiv.org/abs/2503.02737)

### Inferences
- "推文 vs 已核查声明"（2A）与"辩论句 vs 已核查声明"（2B）之间 0.88–0.96 对 0.35–0.46 的差距，是对我们最重要的一条信号：财报电话会、卖方研报、新闻里的观点句更像 2B（口语、指代、省略主语和时间），直接嵌入检索会显著变差。推论：入库前先把声明规范化（补全主体、时间/财期、方向、指标），再嵌入与匹配。
- 判官提示的措辞决定误差方向：问"是否表达相同含义"→ 过严（因数字/细节差异拒绝，与我们逐对判官 R=0.32 的现象一致）；问"是否相关"→ 过松（65% 假阳性来自话题相同）。我们的身份规则（同驱动、同方向、相近期限）应写成封闭的字段比较，而不是自由语义判断。
- 平衡测试集（1:1）上的 96–97 F1 不能直接外推到我们的场景：我们的候选来自 top-k 近邻，是高度相似的难负例（同句不同季度），这种分布下的精度会低得多。
- 重排深度：文献最佳在 top-50~100（BM25 初检较弱时）；稠密检索强时可浅。我们 top-4 召回 99% 是声明级重述；观点级（改写更大）应在开发集上重新测召回曲线再定 k。

### Gaps
- Kazemi 2021 的具体 F1/准确率数字未取到（只拿到摘要）。
- CheckThat! 2023、2024 是否设有"已核查声明检索"任务未核实；2025 年只核实到 4b（科学来源检索）。
- 未找到在"高相似难负例"（同句跨期）分布上评测 LLM 判官的公开基准；现有 LLM 判对研究都用平衡或随机负例。

## 问题 2：跨文档事件共指（ECB+ 及 LLM 方法）与新闻故事聚类/去重（Miranda 2018、SemEval-2022 Task 8）

### Takeaway
"是否同一事件"的判断依赖触发词/实体之外的论元——时间、地点、参与者；只靠表面词汇的模型（包括零样本逐对 LLM）在同类事件密集的语料上会大面积误合并（GVC 上零样本 GPT-3.5 的 B³ 精度仅 35%）。新闻流聚类里，加入时间戳特征是最大单项增益（排序准确率 86.5%→96.9%）。微调交叉编码器/蒸馏模型在 ECB+ 上 CoNLL F1 约 85–89，零样本 LLM 约 77–79。

### Cited Findings
- ECB+ 测试集 CoNLL F1（已核对原文表 2，ACCI 2025 汇总）：Caciularu2021（CDLM）85.6；Cattan2021 81.0；Held2021 85.7；Ahmed2023 81.7；Ding2024 86.0；Chen2023 86.4；Nath2024（LLM 生成理由 + 知识蒸馏到小模型）86.4；**零样本逐对提示 Llama 76.6、GPT-3.5-Turbo 79.2**；ACCI（论元中心因果干预去偏）88.4，RoBERTa-large 版 89.7 — [Yao et al. 2025, ACCI](https://arxiv.org/abs/2506.01488)
- GVC（Gun Violence Corpus，全是枪击事件，事件类型高度同质）测试集（已核对原文表 4）：Held2021 CoNLL 83.7；Nath2024 83.0；ACCI 85.2；**零样本 Llama CoNLL 60.0（B³ P 38.1 / R 89.5），GPT-3.5-Turbo CoNLL 55.8（B³ P 35.4 / R 82.6）**——即 LLM 逐对判官在同类事件上严重过度合并 — [Yao et al. 2025, ACCI](https://arxiv.org/abs/2506.01488)
- ACCI 的诊断：现有 CD-ECR 系统过度依赖触发词表面匹配，学到"触发词相同 ⇒ 共指"的伪相关，忽略时间、地点、参与者等论元一致性；ACCI 用反事实模块估计并扣除触发词偏置 — [Yao et al. 2025, ACCI](https://arxiv.org/abs/2506.01488)
- 〔已核对原文〕Ahmed et al. 2023（ACL Findings）"2*n 优于 n²"：任一数据集里只有 5–10% 的提及对共指；先用词元启发式（触发词词元相等/包含、训练集共指同义词元对、句子词元重叠阈值，阈值在开发集上按召回调）过滤掉大量非共指对，再在平衡的对上训练交叉编码器判别器。ECB+ CoNLL：启发式 LH 单独 76.4，LH+Dlong 81.7；用全数据同义对的 LHOra+Dlong 87.4；GVC 上启发式单独仅 51.8、加判别器 75.0（落后 SOTA 8–9 点），但预测期复杂度对提及数线性 — [Ahmed et al. 2023](https://arxiv.org/abs/2305.05672)
- 同上错误分析：错误类别包括同句代词、**弱时间推理**（不同日期发布的文章里"周六""元旦"指同一天，需利用发布日期等元数据）、共指实体歧义、**误导性的词汇相似**、漏掉集合成员共指 — [Ahmed et al. 2023](https://arxiv.org/abs/2305.05672)
- 〔旧，已核对原文〕Miranda et al. 2018（EMNLP）流式多语新闻聚类：新文档与各簇质心算加权余弦（标题/正文/二者的词、词元、命名实体 TF-IDF 子向量 + 时间戳特征），最高相似度超过阈值 τ 则并入，否则新建簇；权重用 SVM-Rank 学（每篇文档取 20 个最相似错误簇为负例）。时间特征建模为高斯分布，开发集调得 σ = 72 小时 — [Miranda et al. 2018](https://aclanthology.org/D18-1483/)
- 〔旧，已核对原文〕同上结果（成对 P/R/F1）：英文 CluStream 基线 F1 79.0（P 98.6 / R 65.9）；词+词元+实体 F1 92.7；再加时间戳 F1 94.1（P 98.2 / R 90.3）；德文加时间戳 97.1、西文 94.2。SVM 排序器在英文训练集上的准确率：仅词 85.5 → +词元 85.9 → +实体 86.5 → **+时间戳 96.9**；只用时间特征 F1 61.1（P 44.5 / R 97.6）。学习得到的权重比网格搜索 τ 更会判断"何时新建簇" — [Miranda et al. 2018](https://aclanthology.org/D18-1483/)
- 〔旧〕SemEval-2022 Task 8（多语新闻相似度）：近 10,000 对新闻、18 种语言组合，按 7 个相似维度标注，关注"真实世界发生的事"而非文风/立场；组织者强调"两篇文章可能有大量文本重叠，但描述的是相隔数年的相似事件"；最佳系统与金标相关系数 0.818，人类标注者可更高 — [SemEval-2022 Task 8 overview](https://aclanthology.org/2022.semeval-1.155/)；冠军 YNU-HPCC 为多 Transformer 集成 — [YNU-HPCC](https://paperswithcode.com/paper/ynu-hpcc-at-semeval-2022-task-8-transformer)
- StreamBench（2026）：2016 与 2025 年重大新闻构成，605 个事件、15,354 篇文档，任务含话题聚类、时间问答、摘要；多个并发事件混在同一文档流时 LLM 难以区分；加入结构化线索（如元数据）话题聚类最多 +4.37%、时间问答最多 +9.63%，作者认为时间推理仍是当前 LLM 的开放难题 — [StreamBench](https://arxiv.org/abs/2603.19250)
- LLM 增强的 GDELT 新闻事件聚类：LLM 用于事件检测前（关键词抽取、文本嵌入）与后（事件摘要、主题标注）—— [Large Language Model Enhanced Clustering for News Event Detection](https://arxiv.org/abs/2406.10552)
- 〔生产〕RavenPack 新闻分析提供"新颖度"维度：可判断检测到的事件是新事件、重复还是既有事件/主题的延续；Event Novelty Score 取值 0–100，基于 24 小时窗口（以上为二手描述，未读到 RavenPack 官方文档）— [RavenPack 升级新闻稿 (Finextra)](https://www.finextra.com/pressarticle/56610/ravenpack-upgrades-rpna)；[使用 RavenPack 数据的论文](https://arxiv.org/pdf/2307.02673)

### Inferences
- GVC 的结果几乎就是我们内部"同一句话不同季度 cosine 0.988"问题的学术版本：同类事件（每季度"Apple 超预期"）在语义上几乎相同，区分它们的只有时间/财期与论元。零样本 LLM 逐对判官在这种分布上精度可跌到 35%（过度合并）；而我们的逐对判官表现为过严——两者都说明"逐对自由语义判断"不稳，应把财期、主体、指标、方向作为代码比较的硬字段。
- 证据级去重（"20 家媒体报道同一事件只算一次"）应建成事件簇：簇键 = 主体实体 + 事件类型/指标 + 事件日期（或财期），时间衰减窗口按 Miranda 的思路在开发集上调（新闻约 3 天量级；但财报类事件的自然窗口是财期，不是小时）；向量相似度只做候选。
- Ahmed 的做法对我们可直接迁移：先用廉价、可解释、按召回调阈值的规则（同 ticker、同财期、同指标词元）把候选对从 n² 压到线性，再把有限的判官预算花在难对上。

### Gaps
- 未找到金融新闻（同一公司事件多源转载）的公开事件共指/去重基准及其 P/R。
- 未取到 GPT-4/GPT-4o/Claude 级模型在 ECB+/GVC 上的零样本数字（ACCI 只报了 GPT-3.5 与未注明版本的 Llama）。
- 近重复新闻检测（MinHash/SimHash 等）的系统性评测本轮未检索到可引用数字。

## 问题 3：检索-再判定架构（双编码器召回 + 交叉编码器/LLM 判定；列表式 vs 逐对；top-k；阈值校准；误合并与漏重复的权衡）

### Takeaway
各领域证据一致：让 LLM 在一个上下文里看到全部候选并"选择"（listwise/select），比独立逐对判"是否匹配"F1 高约 15–18 点且更便宜；但选择式有位置偏差，需要一个廉价排序器先把候选排好、只留 top-4 左右。召回阶段用 BM25 + 稠密混合、取 top-20~100；阈值应在开发集上学习/调参，并区分"并入"与"新建"两种决策。

### Cited Findings
- 〔已核对原文〕ComEM（"Match, Compare, or Select?"，COLING 2025）：8 个实体匹配数据集，GPT-3.5-Turbo 平均 F1：逐对 Matching 64.02（成本 $4.52）、6-shot Matching 69.99（$32.75）、Comparing 66.86（$11.75）、**Selecting 81.60（$1.71）**、ComEM 85.61（$0.92）；GPT-4o-mini：Matching 67.80、Comparing 84.36、Selecting 82.26、ComEM 86.42 — [Wang et al. 2024/2025, ComEM](https://arxiv.org/abs/2405.16884)
- 同上：ComEM 先用小模型（Flan-T5-XL）以逐对匹配给候选排序，**只保留 top-4 候选交给选择策略**；选择与比较策略存在位置偏差——真匹配在候选列表中越靠后，准确率越低；把所有候选放进同一上下文能让 LLM 利用记录间的相互关系（全局一致性）— [ComEM](https://arxiv.org/abs/2405.16884)
- 〔已核对原文〕LLM-CER（SIGMOD'26）：让 LLM 对"记录集合"做上下文聚类而不是逐对判；最优集合大小 9、每集合约 4 个不同实体、集合内簇大小越均衡越好、同实体记录相邻排列更好；与逐对（集合大小 2）相比准确率相当或更好，API 调用少 12–108×、token 少 3–28×、成本低 3–22×；误聚类检测护栏耗时 +10%，FP-measure 最多 +75%；对比 BQ/CrowdER+LLM 等基线最多高 150% 准确率 — [LLM-CER](https://arxiv.org/abs/2506.02509)
- BatchER（2023/2024）：实体解析的批量提示框架，用覆盖式示例选择在准确率与成本间取平衡 — [BatchER](https://arxiv.org/abs/2312.03987)
- Pairwise Ranking Prompting（2023，排序任务而非等价判断）：20B 的 Flan-UL2 用逐对比较提示，在 TREC-DL2020 上 NDCG@1 比 GPT-4 高 5% 以上；作者认为现成 LLM 不擅长 pointwise/listwise 排序表述，中等规模 LLM 的 listwise 输出常冲突或无用 — [Qin et al. 2023, PRP](https://arxiv.org/abs/2306.17563)
- 〔旧〕Shaar 2020：重排 BM25 的 top-N，PolitiFact 在 N=100 最好、N=200 开始下降；Snopes 在 N=50 最好 — [Shaar et al. 2020](https://arxiv.org/abs/2005.06058)
- SemEval-2025 Task 7 头部系统：召回 top-50 → 重排 → 输出 top-10 — [SemEval-2025 Task 7 overview](https://arxiv.org/abs/2505.10740)
- 〔旧〕CheckThat! 2022：AI Rational 证明对 MAP@k/P@k，重排可退化为一个分类器（SVM）；SimBa 用多种嵌入各 top-50 的并集做 blocking，只在难例上训练分类器 — [CheckThat! 2022 Task 2 overview](https://ceur-ws.org/Vol-3180/paper-29.pdf)
- 〔旧〕阈值校准：Miranda 2018 在开发集上调 τ，并用 SVM-Rank 学特征权重，后者比网格搜索 τ"显著更会决定何时新建簇" — [Miranda et al. 2018](https://aclanthology.org/D18-1483/)；Ahmed 2023 的启发式阈值在开发集上按"保留共指对、最少漏掉 P+"来调 — [Ahmed et al. 2023](https://arxiv.org/abs/2305.05672)
- 判官措辞决定误差方向：Pisarevskaya 2025 中"含义相同"模板因细节/数字差异漏判 — [Pisarevskaya & Zubiaga 2025](https://arxiv.org/abs/2501.10860)；Vykopal 2025 中"相关"框架约 65% 假阳性来自话题相同 — [Vykopal et al. 2025](https://arxiv.org/abs/2503.02737)；GVC 上零样本逐对共指判官 B³ 精度 35–38%（过度合并）— [ACCI](https://arxiv.org/abs/2506.01488)

### Inferences
- 我们内部结果（选择式 P 0.975 / R 0.76 vs 逐对 P 0.99 / R 0.32）与 ComEM（Selecting 81.60 vs Matching 64.02，同模型）方向完全一致：应采用"选择式"判官，候选数约 4（ComEM 与我们的 top-4 召回 99% 都支持这个量级），并按相似度排好序以减轻位置偏差。
- 建议的流水线（推断，供决策）：
  1. 规范化：新观点/证据先抽成字段（对象/ticker、方向、驱动/指标、财期或事件日期、期限、来源、发言人）。
  2. 代码阻断（blocking）：同对象 + 时间窗/财期兼容才进入候选；方向相反直接由代码判为"反向证据"而非新观点（字段比较，不交给模型）。
  3. 混合召回：BM25 + 稠密向量各取 top-N 合并（文献 N=20–100；我们的声明级数据 top-4 已达 99%，观点级需重测）。
  4. 选择式 LLM 判官：一次看全部候选，输出"选中哪一个/都不是"，并引用决定性字段；输出受枚举约束。
  5. 离线合并：定期对已存观点做集合级聚类（LLM-CER 式，集合约 9 条）+ 误聚类护栏，回收在线阶段漏掉的重复。
- 误合并 vs 漏重复的代价不对称（推断）：观点级误合并会把两个不同论点的证据与状态搅在一起，难以撤销；漏重复只产生一条重复观点，可由离线合并修复。因此在线阶段应偏精度（我们的选择式 P 0.975 合适），召回缺口交给离线合并。证据级相反：漏重复会把 20 家转载算成 20 条独立证据（虚高置信），误合并会把两个不同季度的同类事件当成一次（漏掉真实重复信号）；事件键里的日期/财期字段是两者的分界线。
- 预期精度（推断，按文献区间）：召回阶段 top-10 成功率在自含文本上 0.85–0.96，在口语/转录类输入上可能只有 0.4–0.7（CheckThat 2B）；选择式判官 F1 在 0.80–0.86 量级（ComEM），我们自测 P 0.975 / R 0.76 落在此区间内；纯逐对零样本判官在同类事件密集的数据上不可用。

### Gaps
- 未找到在"等价/去重判断"（而非相关性排序）上直接比较 listwise 与 pairwise LLM 判官的 2025–2026 论文；PRP 结论来自相关性排序，不能直接迁移。
- 未找到 LLM 判官输出置信度用于阈值校准（calibration curve、ECE）的去重类评测数字。

## 问题 4：用 LLM 做实体解析（blocking + LLM 匹配）作为带文本字段的结构化记录去重类比

### Takeaway
GPT-4 级模型零样本做实体匹配已与用数千样本微调的 PLM（Ditto 等）相当，且对未见实体类型稳健得多；但逐对调用昂贵，主流做法是"blocking/排序器缩小候选 → 选择式或集合聚类式 LLM 判定"，可把成本降一到两个数量级。手写匹配规则对强模型反而有害，对弱模型有益。

### Cited Findings
- 〔已核对原文〕Peeters et al.（arXiv 2310.11244 v4；ComEM 引为 Peeters et al. 2025）：GPT-4 零样本 F1——WDC Products 89.61（Ditto 微调 84.90）、Abt-Buy 95.78（Ditto 91.31）、Walmart-Amazon 89.67、Amazon-Google 76.38（Ditto 80.07）、DBLP-Scholar 89.82（Ditto 94.31）、DBLP-ACM 98.41 — [Peeters et al.](https://arxiv.org/abs/2310.11244)
- 同上：在未见实体上，微调 PLM 迁移后 F1 下降 36–56 点，而 LLM 保持稳定，GPT-4 比最好 PLM 高 40–68 点；in-context 示例对 GPT-4 只 +0.85（平均），对 GPT-4o +3.10，Mixtral 反而 −11.42；手写匹配规则使 GPT-4 下降 1–3 点、使 Mixtral 提升 3–17 点；成本（WDC Products 每条提示）：零样本 GPT-mini 0.006 美分、GPT-4 0.474 美分、微调 GPT-mini 推理 0.003 美分；微调 GPT-mini 在 WDC Products 达 88.89 F1 — [Peeters et al.](https://arxiv.org/abs/2310.11244)
- ComEM：选择式 81.60 vs 逐对 64.02（GPT-3.5，8 数据集平均），组合方案 85.61 且成本 $0.92 vs 逐对 $4.52；候选 top-4 — [ComEM](https://arxiv.org/abs/2405.16884)
- LLM-CER：集合聚类（集合大小 9）相对逐对 API 调用少 12–108×、成本低 3–22×，误聚类护栏 FP-measure 最多 +75% — [LLM-CER](https://arxiv.org/abs/2506.02509)
- BatchER：批量提示 + 覆盖式示例选择以降成本 — [BatchER](https://arxiv.org/abs/2312.03987)
- 事件共指里的 blocking 类比：Ahmed 2023 的词元启发式把 n² 对降为线性，只在过滤后的平衡对上判别 — [Ahmed et al. 2023](https://arxiv.org/abs/2305.05672)；CheckThat 2022 SimBa 用多嵌入 top-50 并集做 blocking — [CheckThat! 2022 Task 2 overview](https://ceur-ws.org/Vol-3180/paper-29.pdf)

### Inferences
- 我们的观点记录（声明句 + 对象/方向 + 期限 + 证据）就是"带文本字段的结构化记录"：结构字段（对象、方向、期限桶）适合做 blocking 键，文本字段（驱动、理由）交给选择式判官。
- "手写规则让强模型变差"提示：身份规则不要以长篇说明写进提示，而应由代码执行字段比较后，只把通过阻断的候选交给模型。
- 观点库规模（约 500 个标的 × 每标的少量活跃观点）很小：按对象 blocking 后每个新观点的候选通常只有个位数，逐条选择式调用的成本可忽略；集合聚类更适合定期离线合并。

### Gaps
- 实体解析基准（商品、论文引用）的文本短且字段规整，与"论点"这种抽象命题的匹配难度差异未知；未找到在论点/论证级记录上的 ER 评测。

## 问题 5：金融/投资领域的声明、观点与叙事追踪研究

### Takeaway
金融 NLP 已有"前瞻性声明 vs 已发生事实"的句级识别（F1 0.92–0.96）和针对财报的声明核验基准（FinDVer，最好的 GPT-4o 仍明显落后人类专家），也有"跨期追踪披露中指标/叙事变化"的研究和厂商产品；但**没有找到任何公开基准评测"投资观点/论点是否与已存观点相同"或"卖方观点随时间追踪"的匹配精度**，这部分只能靠我们自己的数据测。

### Cited Findings
- 〔已核对原文〕Shah et al. 2024（FEVER 研讨会）金融数值声明检测：原始数据 87,536 份分析师报告 + 1,085 份财报电话会记录；"in-claim"= 推测性的财务预测，"out-of-claim"= 关于过去事件的数值陈述（已确认事实）；人工标注约 2,681 句（研报）+ 498 句（电话会），标注一致率 99.21% / 95.78%。F1：ChatGPT-3.5 零样本 研报 0.919 / 电话会 0.757；Llama-2-70B 6-shot 0.917 / 0.797；SME 规则弱监督 0.927 / 0.938；微调 RoBERTa-large 研报 0.964、RoBERTa-base 电话会 0.956；作者据此构造"乐观度"指标并观察到其与盈利意外和收益相关 — [Shah et al. 2024](https://aclanthology.org/2024.fever-1.21/)
- FinDVer（EMNLP 2024）：4,000 条专家标注、针对长篇混合内容财务文档的可解释声明核验；评测 25 个 LLM（长上下文与 RAG 两种设置），最好的 GPT-4o 仍显著落后人类专家 — [FinDVer](https://arxiv.org/abs/2411.05764)
- Fin-Fact：带专业核查员标注与理由的多模态金融事实核查数据集（具体规模与基线数字本轮未取到）— [Fin-Fact](https://arxiv.org/abs/2309.08793)；MiniCheck-FISCAL 在 Fin-Fact、FISCAL、FinDVer 上评测轻量金融核验器 — [MiniCheck-FISCAL](https://arxiv.org/abs/2511.19671)
- "From Text to Alpha"（2025）："LLM 当抽取器、嵌入当尺子"：抽取以指标为中心的文本片段，用嵌入相似度量化相邻披露期之间的语义变化（"移动靶"/指标漂移）；该信号的风险调整 alpha 是命名实体识别基线的两倍以上 — [From Text to Alpha](https://arxiv.org/abs/2510.03195)
- 财报电话会话题追踪：LLM 智能体动态追踪大量电话会中的金融相关话题与叙事随时间的演变 — [Agentic Retrieval of Topics and Insights from Earnings Calls](https://arxiv.org/abs/2507.07906)
- 〔生产/厂商，未经独立验证〕Bigdata.com 的 NarrativeMiner 跨新闻、电话会、SEC 文件追踪叙事演变，并声称可量化来源间时滞（如 SEC 文件比新闻覆盖峰值晚约 443 天）— [Bigdata 叙事追踪用例](https://bigdata.com/use-cases/tracking-the-ai-bubble-across-media-earnings-calls-and-sec-filings)
- 〔生产〕RavenPack 新颖度维度区分新事件/重复/延续，ENS 基于 24 小时窗口（二手描述）— [Finextra](https://www.finextra.com/pressarticle/56610/ravenpack-upgrades-rpna)

### Inferences
- Shah 2024 的 in-claim/out-of-claim 二分正好对应我们的"观点 vs 证据"：前瞻性声明是观点候选，已发生的数值陈述是证据候选；该分类在研报上零样本即可达 ~0.92 F1，但在电话会上零样本掉到 0.76——再次说明口语转录是难输入。
- "From Text to Alpha"的做法（同一指标跨期比较语义变化）与我们"同一句话不同季度 cosine 0.988"的发现互补：跨期高相似本身是信号（管理层重复同一说法），不应被去重吞掉；去重键必须含财期，"重复"要记为同一观点的新一期证据，而非丢弃。
- 由于没有可借用的观点去重金标，我们需要自建：从已存的 Apple/Amazon/Meta 声明级金标扩展到观点级，单独留出测试集，按 AGENTS.md 规则只在测试集上评一次。

### Gaps
- 未找到"卖方观点追踪""投资论点去重/合并"的学术基准或带 P/R 的生产报告。
- 未取到 Fin-Fact 的规模与基线数字、FinDVer 的具体准确率数字。
- 金融新闻多源转载的事件去重（"20 家媒体算一次"）没有找到带 P/R 的公开评测；RavenPack ENS 的算法与准确率未公开（仅有定义级描述）。
