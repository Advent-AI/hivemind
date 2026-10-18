# "链接到已有条目，或声明为新条目"：实体链接 NIL、关键论点匹配、生产级声明匹配与受控词表（截至 2026-10）

说明：本笔记不重复上一轮已确立的结论（嵌入分不开方向、数字和期间；在约 4 个候选里做选择优于逐对判断）。标"较早"的是 2023 年以前的结果。数字都注明数据集和指标。厂商自述标为"厂商声称"。

## 问题 1：带 NIL 判定的实体链接（BLINK、ReFinED、GENRE、ChatEL、OneNet）：NIL 怎么判、准确率多少、知识库怎么随时间增长

### Takeaway
各家的结构都一样：先召回出一小组候选，再由交叉编码器或 LLM 选出其中一个，或者判为 NIL。系统能做到很准的是"在库内选对"那一半。"判定为新"这一半，在真实的大型知识库上依然很弱：在 Wikidata 版本差构造的 NILK 上，最好的 out-of-KB F1 只有 47.8，精确率不到 40%。而且只有显式训练、显式度量 NIL，这个数字才看得见。LLM 链接器虽然给出了"都不是"这个选项，却没人报告它的 NIL 精度；另有研究显示，正确答案是"以上都不是"时，LLM 的准确率会掉 30–50%。

### Cited Findings
**双编码器召回 + 交叉编码器重排（BLINK，较早，2020）**
- BLINK 的双编码器在 5.9M 个候选实体里检索只要约 2 ms，然后交叉编码器对 top-64 重排。在 Zero-shot EL 测试集上，Recall@64 为 BM25 69.13%、双编码器 82.06%；端到端 unnormalized accuracy 从 Logeswaran et al. 的 55.08 提到 63.03（large）。论文只度量库内准确率 P@1，不处理 NIL — [Wu et al. 2020, BLINK](https://arxiv.org/abs/1911.03814)

**把 NIL 作为一个候选（ReFinED，较早，2022）**
- ReFinED 在候选里"加一个 NIL 特殊候选，其未归一化分数为 0，表示所有候选都不对"。推理时取综合得分最高的那个，可能是库内实体，也可能是 NIL。它靠实体类型和描述打分，所以能链接训练时没见过的实体，覆盖 Wikidata 约 90M 实体。论文报告比同类方法快 60 倍以上，平均 F1 高 3.7 — [Ayoola et al. 2022, ReFinED](https://arxiv.org/abs/2207.04108)

**闭集生成（GENRE，较早，2021）**
- GENRE 逐 token 生成实体名，并用"知识库名称前缀树上的约束束搜索"保证输出必然是一个合法实体，即结构上的闭集。它在 20 多个数据集上达到或接近 SOTA。参数规模随词表增长，不随实体数增长。"新实体只需写明名字即可加入"。摘要不讨论 NIL — [De Cao et al. 2021, GENRE](https://arxiv.org/abs/2010.00904)

**专门度量 NIL 的研究**
- 《Learn to Not Link》（2023）构建了 NEL 数据集：9,924 条，其中 NIL 占 33.57%；NIL 里 17% 是"库里缺这个实体"（Missing Entity），83% 是"根本不是实体的短语"（Non-Entity Phrase）。NIL 用阈值判：最高分 ≥ ε=0.5 就链接到最高分实体，否则判 NIL — [Learn to Not Link, arXiv 2305.15725](https://ar5iv.labs.arxiv.org/html/2305.15725)
- 同一论文在 NEL 上的结果：交叉编码器 CLINK-cross 非 NIL 准确率 86.97%、NIL 89.19%、总体 87.71%；双编码器 BLINK-bi 分别为 72.27% / 88.59% / 77.74% — [同上](https://ar5iv.labs.arxiv.org/html/2305.15725)
- 同一论文在 AIDA 上的对比：把 NIL 计入评测时 CLINK-cross 的 NIL 准确率只有 58.53%，总体 82.03%；不计 NIL 时总体 85.49%。作者据此指出，忽略 NIL 会让准确率虚高 — [同上](https://ar5iv.labs.arxiv.org/html/2305.15725)
- 训练集里不放 NIL 样例时，"所有模型的 NIL 准确率都大幅下降"；只用 25% 的 Non-Entity Phrase 样例就能恢复到可用水平。加一个实体类型（typing）辅助任务，交叉编码器总体准确率从 83.67% 升到 87.41% — [同上](https://ar5iv.labs.arxiv.org/html/2305.15725)
- BLINKout（Dong et al. 2023，《Reveal the Unknown》）把 NIL 做成带表示的特殊实体，再加 NIL 分类和同义词增强，与规则法、阈值法、特征法对比。测试集有三种构造方式：人工标注 NIL、剪掉部分知识库（pruning）、用旧版本知识库（versioning）— [Dong et al. 2023](https://arxiv.org/abs/2302.07189)
- BLINKout 的 out-of-KB F1：在人工标注 NIL 的 ShARe/CLEF 2013 上，阈值版 BLINK 为 66.5，BLINKout 最好达 90.5–90.9。在 NILK-sample（用 Wikidata 2017 与 2021 两个版本的差构造）上，阈值版 BLINK 为 26.2（P 17.8 / R 49.4），BLINKout 最好为 47.8（P 37.1 / R 67.1）；规则法 P 只有 6.6。在 NILK 上总体准确率仍有约 88–90，因为绝大多数提及在库内 — [Dong et al. 2023, Table 2](https://arxiv.org/pdf/2302.07189)
- 同一论文的个案分析："当一个错误但相似的库内实体拿到接近 100% 的分数时，阈值法很可能把 out-of-KB 提及漏判"。对于与库内实体非常相似的新实体（剪库数据集）和细粒度实体（NILK），所有模型都判错，不过 NIL 常排在第 2、第 3 位 — [同上](https://arxiv.org/pdf/2302.07189)

**NIL 的聚类与知识库增长**
- TAC KBP 从 2011 年起要求系统要么返回知识库 ID，要么返回 "NILxxxx" ID，并把指向同一个库外实体的查询聚成一类，用 B-cubed+ 计分（较早）— [TAC KBP 2011 overview](https://tac.nist.gov/publications/2011/presentations/KBP2011_overview.presentation.pdf)；[LDC EDL 数据说明](https://catalog.ldc.upenn.edu/LDC2019T02)
- NASTyLinker（Heist & Paulheim 2023）把提及和实体一起聚类，自上而下切分；冲突时按"传递亲和度"把提及分给最近的实体。在 NILK 上，库内实体的基线 F1 为 79.5%，各种聚类法对 NIL 实体的 F1 在 40%–50% — [Heist & Paulheim 2023](https://arxiv.org/abs/2303.04426)
- 同一系统用于 Wikipedia 列表页：13.4M 个提及（70%）被判为 NIL，对应 7.6M 个新实体，相当于让 CaLiGraph 的实体数增加 130%。人工抽检发现"库内实体的聚类正确率明显低于 NIL 实体"。双编码器 recall@4 = 97%；全量运行 62 小时 — [同上](https://arxiv.org/pdf/2303.04426)
- Hoffart、Altun、Weikum（WWW 2014）显式为"知识库外实体"建模，用来发现新出现的实体，前提是"知识库永远不完整，每天都有新公司"（较早；本轮没取到数字）— [WWW 2014 条目](https://ir.webis.de/anthology/2014.wwwconf_conference-2014.37/)
- TempEL（NeurIPS 2022 D&B）使用 2013–2022 年的 Wikipedia 快照：持续存在的实体，准确率最多下降 3.1%；新出现的实体最多下降 17.9% — [TempEL](https://arxiv.org/abs/2302.02500)

**LLM 链接器（2024）**
- ChatEL（LREC-COLING 2024）分三步：先用先验加 BLINK 召回 10 个候选，再让 LLM 生成辅助描述，最后做多选题，其中有"都不匹配"选项。用 GPT-4 时 10 个基准的平均 micro-F1 为 0.795，对比 ReFinED 0.773、GENRE 0.725、Prior 0.754。作者还发现 CoNLL03 至少 5% 的金标是错的。论文没有单独报告 NIL 指标 — [ChatEL](https://arxiv.org/html/2402.14858v1)
- OneNet（EMNLP 2024）有三个模块：LLM 逐个淘汰无关候选；"上下文 CoT"与"先验"两个视角各自链接；两者一致就采纳，不一致时交给辅助 LLM 裁决。大数据集上最多给 10 个候选，允许回答 "-1.None"，但没有 NIL 评测。Zephyr-7b 版的 micro-F1 为 0.681–0.796 — [OneNet](https://arxiv.org/html/2410.07549v1)

**LLM 拒绝所有选项的能力**
- 《None of the Above, Less of the Right》（Tam et al.，ACL Findings 2025）在 MMLU 上测了 28 个 LLM：正确答案换成"以上都不是"后，准确率一致下降 30–50%；数学类降 14.6%，商业伦理降 48.1%。作者结论是 LLM "缺乏系统评估并拒绝所有给定选项的元认知能力" — [arXiv 2503.01550](https://arxiv.org/abs/2503.01550)
- 同一论文的分模型数字（来自检索摘要，本轮没有逐项核对原文）：GPT-4o −36.8pp、Claude 3.5 −26.5、DeepSeek-R1 −8.8、o3-mini −16.2，推理模型跌得较少 — [arXiv 2503.01550](https://arxiv.org/html/2503.01550v1)

### Inferences
- "选中哪个已有条目"和"判定为新"是两个难度不同的问题。只看总体准确率，NIL 会被掩盖：NILK 上总体约 90，但 out-of-KB F1 不到 50。我们的度量必须把"判为新"单独拆出 P/R，用真实的"后来才出现的 driver/观点"来测，做法类似 KB versioning：用 T 时刻的库判 T+Δ 的文档。
- 阈值法的典型失败，正对应我们"同一 driver、方向相反"或"相近但不同 driver"的情形：一个相似但错误的已有条目拿到极高分，于是新条目被吞掉。把 NIL 显式表示成一个候选（ReFinED、BLINKout），再用 NIL 样例训练和校准，是文献里比单纯调阈值更好的做法。
- LLM 多选时有一个"偏向选已有项"的结构性弱点（"以上都不是"时跌 30–50%）。这对 (a) 和 (b) 两种方案同样成立：只要让 LLM 在闭集里选"哪一个，或新建"，"新建"一侧就会系统性偏少。所以"新建"率需要单独监控和抽检。
- 实体类型辅助任务把准确率提高了约 3.7pp。这提示：让候选在结构字段上先对齐（对象、driver 类别），能降低选错的概率。

### Gaps
- 没找到 2024–2026 年 LLM 链接器（ChatEL、OneNet 及后续）在 NIL 上的 P/R 报告：它们给了"None"选项，但没度量。
- TAC KBP NIL 聚类历年的具体 B-cubed+/CEAF 分数没有取到。
- Hoffart 2014 和 NILK 原论文的数字没有取到。

## 问题 2：IBM Project Debater 的关键论点分析（KPA）：把论点匹配到少量关键论点；阈值与"最佳匹配"策略；关键论点怎么生成、怎么去重

### Takeaway
KPA 就是"把新条目链接到一个小的受控集合"的完整实验场。最佳匹配加阈值（BM+TH）在"0 或 1 个匹配"的常见情形下最好，双阈值能处理少量多匹配。即便由专家事先写好关键论点，也有约 27% 的论点匹配不到任何一条，而且专家集合会漏掉数据里实际存在的论点。去重的做法是：用同一个匹配模型给候选关键论点两两打分，与更靠前的候选匹配分超过阈值的就删掉。按 aspect 加情感组织关键论点（类似"驱动因子 + 方向"）时，匹配精度最高。

### Cited Findings
**ArgKP 与匹配策略（Bar-Haim et al. ACL 2020，较早）**
- 数据：28 个辩题。专家为每个"辩题 × 立场"事先写 7 条关键论点（KP），写的时候没看过论点。至少 60% 的标注者认为匹配，才算正例 — [Bar-Haim et al. 2020a](https://arxiv.org/abs/2005.01619)
- 论点的分布：无 KP 4.7%；有歧义（票分散在几条 KP 上，都不到 60%）22.8%；单一 KP 67.5%；多个 KP 5.0%。合计"27.5% 的论点没有匹配到任何 KP" — [同上](https://arxiv.org/pdf/2005.01619)
- 匹配打分（Threshold 策略下正类 F1）：TF-IDF 0.352，GloVe 0.330，BERT 嵌入 0.403，MNLI 迁移 0.526，在 ArgKP 上微调的 BERT-base 0.657，BERT-large 0.684 — [同上 Table 4](https://arxiv.org/pdf/2005.01619)
- 选择策略（都用 BERT-large），全体论点 F1 / 无 KP 论点准确率 / 多 KP 论点 F1：
  - Threshold：0.684 / 0.933 / 0.782
  - Best Match：0.703 / 0.839 / 0.606
  - BM+Threshold：0.713（P 0.772，R 0.665）/ 0.915 / 0.580
  - Dual Threshold：0.730 / 0.908 / 0.773
  - Best Match 是唯一不需要标注数据来学阈值的策略 — [同上 Table 5](https://arxiv.org/pdf/2005.01619)
- 误报主要有两类：两句共享大段文字但主旨不同；两句部分相关，但存在一条更合适的 KP。对后一类，Best Match 有帮助 — [同上](https://arxiv.org/pdf/2005.01619)

**自动生成 KP 与去重（Bar-Haim et al. EMNLP 2020，较早）**
- 匹配模型（BM+TH）：ALBERT F1 0.809，RoBERTa 0.773（快 6 倍），BERT 0.721 — [Bar-Haim et al. 2020b](https://arxiv.org/abs/2010.05369)
- KP 抽取算法共四步 — [同上](https://arxiv.org/pdf/2010.05369)
  1. 先选短而质量高的评论作为候选 KP。
  2. 用 BM+TH 把评论匹配到候选，按覆盖数排序。
  3. 依次删除"与排名更高的候选匹配分超过阈值"的候选（匹配分不对称，取双向平均）。
  4. 把被删候选及其评论重新匹配到剩下的候选。
- 结果：辩论数据上，把全部评论匹配到 5 条和 10 条 KP 时，精度分别为 0.752 和 0.792；只匹配 60% 的评论时精度超过 90%。与专家手写 KP 相比，100% 覆盖时 0.696 vs 0.708，80% 覆盖时 0.8 vs 0.808；覆盖率更低时专家 KP 精度更高。跨域：问卷数据 20 条 KP、60% 覆盖时精度 0.763；评论数据 60% / 100% 覆盖时为 0.731 / 0.568，都优于基于金标摘要的 KP（0.642 / 0.454）— [同上](https://arxiv.org/pdf/2010.05369)

**KPA-2021 共享任务（ArgMining 2021，较早）**
- 数据规模：训练 24 题、5,583 个论点、207 条 KP；验证 4 题、932 / 36；测试 3 题、723 / 33。正例比例 0.14–0.18，"未定"比例 0.13–0.18。严格覆盖率（至少有一条正例 KP 的论点占比）0.69–0.72，宽松覆盖率 0.91–0.95 — [Friedman et al. 2021](https://arxiv.org/pdf/2110.10577)
- 评测设计：因为"只有 5% 的论点对应多条 KP"，每个论点只取置信度最高的那条 KP。主办方承认"相当一部分论点不对应任何 KP，模型必须给出阈值"，但为了简化，改为在全部 (论点, KP) 对里按置信度取前 50% 来评。"未定"对在 strict mAP 中算错，在 relaxed mAP 中算对 — [同上](https://arxiv.org/pdf/2110.10577)
- 匹配赛道：第一名 SMatchToPR strict mAP 0.789、relaxed 0.927。很多模型 relaxed mAP 都很高，差距主要体现在 strict 上。共 22 份提交、17 支队伍 — [同上](https://arxiv.org/pdf/2110.10577)
- 生成赛道：BarH 的 mAP 0.885，KP 集合排名第一。主办方指出：只评匹配不够，因为生成冗余或空泛的 KP 也能拿到高 mAP，所以必须单独评估 KP 集合的质量；匹配赛道做得好"不保证"完整 KPA 做得好 — [同上](https://arxiv.org/pdf/2110.10577)
- 主办方的复盘：专家事先写的 KP 集合漏掉了数据中实际出现的论点（例如"校园安全""防止疫情传播"）。同一条 KP，不同系统匹配到的论点比例差异很大（一个系统 35%，另一个高得多）。建议今后由每个模型自己设定"无匹配"的最低置信阈值 — [同上](https://arxiv.org/pdf/2110.10577)

**LLM 时代**
- PAKPA（Tang et al. ACL 2024）分三步：
  1. 用 LLM 的上下文学习从评论中抽取 (aspect, 情感)。
  2. 按 aspect 加情感贪心聚类（aspect 词余弦阈值 0.55）。
  3. 每个簇生成一条只含一个 aspect 的 KP，簇大小即该 KP 的流行度。

  在 Yelp 上，量化精度 PAKPA 0.95，ABKPA 0.83，SKPM 0.76，RKPA-Base 0.66。论文指出，以句子为单位的生成式 KP 会"观点重叠、幻觉、量化不准" — [PAKPA](https://arxiv.org/html/2407.14049v1)
- TU Delft 本科毕业论文（Eijkenboom 2025，样本小，权重低）用美国国会委员会听证记录（143 个论点、480 条 KP）测试：GPT-3.5-turbo 和 o4-mini 零样本做论点到 KP 映射，macro-F1 最高 0.880，优于未微调和已微调的 RoBERTa；两样本提示没有增益；批量 32 不损失准确率 — [Eijkenboom 2025](https://repository.tudelft.nl/file/File_b180a9f8-d055-4d4e-a524-13c8ea1ce70d)

### Inferences
- ArgKP 的分布（约 27% 无匹配、5% 多匹配、其余单匹配）和我们"候选观点对已有观点"的情形同构，因此 BM+TH（必要时 Dual Threshold）是有实测支撑的默认策略：先取最佳，再用阈值决定是否判为"新"。
- 一个受控集合即使由专家精心编写，也会漏掉、也会变旧（专家 KP 漏项，自动 KP 在高覆盖时与专家打平）。所以注册表必须能从数据里长出新条目，而且新条目要用和匹配相同的模型去重（Bar-Haim 2020b 的第 3 步）。
- PAKPA 是与方案 (b) 最接近的实证：先把每条意见落到一个受控的 facet（aspect）加极性上，再在 facet 内聚合，匹配精度从 0.66–0.83 升到 0.95。不过它的 aspect 词表本身也是自底向上聚类出来的（阈值 0.55），并非人工预设。
- "空泛的 KP 也能拿高分"是注册表粒度风险的直接证据：driver 定义得越宽，匹配率越高，信息量越低。

### Gaps
- 没找到 LLM 在大规模 KP 集合上带"无匹配"选项的系统评测（只有一篇本科论文）。
- 没找到 KP 集合随时间增量更新（流式 KPA）的研究。

## 问题 3：生产级声明匹配（Full Fact、Meedan Check、Google Fact Check 工具）：实际流水线、"同一声明 / 新声明"怎么判、人工复核、实测质量

### Takeaway
三家都是"向量召回 + 一个二值匹配判定 + 人在环"。Meedan 公开了明确的三档策略：相似度高于 0.95 自动归组，较低的作为建议交给核查员确认或拒绝，其余视为新。Full Fact 发现纯向量"常常混淆不同的人和地点"，于是加入实体、数字分析，再训一个匹配分类器。三家都没公开生产环境的准确率。Google 不做语义匹配，靠发布方提供 ClaimReview 结构化标注加关键词或图片检索。

### Cited Findings
**Meedan / Kazemi et al.（ACL 2021，较早）**
- 声明匹配的定义："能由同一篇核查文章回应的消息对"。数据：WhatsApp tipline 消息和公开群消息，加上约 15 万篇核查文章（含 Google Fact Check Explorer 的聚合）；2,343 个标注对；4 级标签（Very Similar / Somewhat Similar / Somewhat Dissimilar / Very Dissimilar）— [Kazemi et al. 2021](https://arxiv.org/pdf/2106.00853)
- 余弦阈值分类器（正类为 "Very Similar"）的最大 F1，I-XLM-R 模型：
  - 全语言 0.73（阈值 0.90）
  - 英语 0.88（0.78）
  - 印地语 0.82（0.87）
  - 泰米尔语 0.57（0.96）
  - 最优阈值随语言在 0.78–0.96 之间变化
  - 对比：英语 SBERT 0.90（0.71）
  - [同上 Table 5](https://arxiv.org/pdf/2106.00853)
- AdaBoost 分类器（特征：长度、长度差、嵌入、余弦），只用 522 个数据点：准确率 0.883，正类 F1 0.885，明显高于纯阈值法 — [同上 Table 6](https://arxiv.org/pdf/2106.00853)
- 阈值法的误差：误报 24/89、漏报 65/89。24 个误报里有 16 个被标为 "Somewhat Similar"，人工查看发现它们都是"部分重叠的声明"，即共享一部分主张、不共享另一部分 — [同上](https://arxiv.org/pdf/2106.00853)
- 部署方式：37,823 条印度大选 tipline 消息，用单链接层次聚类（阈值 0.90）得到 1,305 个至少 2 条的簇，最大簇 213 条。上线系统"相似度超过 0.95 自动归组，从相似度较低的候选里推荐可能的匹配，由核查机构确认或拒绝；匹配也可手动添加"，服务 12 家以上核查机构 — [同上](https://arxiv.org/pdf/2106.00853)
- Check 的早期实现（2020）：Multilingual Universal Sentence Encoder 加 Elasticsearch 向量检索。用户自己设"最低相似度阈值（0–100%），达到即自动关联"；"用户每次删除自动匹配或手动添加匹配"都作为反馈，算法给建议，再从用户的操作中学习 — [Meedan Tech & Check 2020](https://meedan.org/post/tech-and-check-2020)
- Meedan 的博客：有近似匹配时，tipline 用户能立即收到回复；核查方能把"同一声明的重复和变体"归到一组，用来衡量流行度。没有公开阈值和准确率 — [Meedan 博客](https://meedan.org/post/claim-matching-global-fact-checks-at-meedan)

**Full Fact**
- 2020 年的设计：训练一个 BERT 类的 match/no-match 句子分类器，再加实体分析（数一数两句是否包含相同的数字、人物、组织）。统计类声明另走一条路：抽取主题、趋势、数值、日期、地点，对照英国 ONS API，系统识别 15 个主题、约 60 个表示趋势的动词（rising、falling 等）。规模：2020 年仅英国媒体中就检出 50 万条以上与疫情相关的声明；在阿根廷，每周发布的核查有一半针对 AI 工具发现的声明 — [Full Fact 2020](https://fullfact.org/blog/2020/jul/afc-global/)
- 2025 年的描述：先用预训练模型把声明和媒体句子转成向量比较。团队发现这样"常常混淆不同的人或地点"，于是加入实体识别和词性标注，再训练一个常规神经网络来预测匹配概率，"准确得多"。之后引入生成式模型，需要的样例少得多，便于扩展到其他语言。服务 30 个国家、3 种语言的 40 多家机构，一个普通工作日处理约 33 万句；坚持"专家在环"，以规避全自动系统的偏差和幻觉。没有给出准确率 — [Full Fact 2025](https://fullfact.org/blog/2025/feb/how-ai-can-help-fact-checkers/)；[Full Fact AI](https://fullfact.org/ai/about)
- Full Fact 的定义（Corney 2021）：两条声明匹配，当且仅当它们"真值条件相同"，即不存在一个世界让其中一条为真、另一条为假；现实中接受"近似相等"。定义里还有两点 — [Corney 2021](https://fullfact.org/blog/2021/oct/towards-common-definition-claim-matching/)
  - 真值依赖时间：例如"通胀是 2.5%"在 10 年里只有 5 个月为真。
  - 允许非对称匹配：当 t(v) ⊃ t(u) 时，例如"约 3%"与"恰好 2.9%"，精确的那条蕴含粗略的那条，反之不成立。作者明确把声明匹配和语义相似、复述检测、蕴含区分开。

**Google Fact Check 工具**
- Fact Check Explorer 的检索方式："输入关键词查看带该词的最新核查"、上传图片查是否核查过、按发布方过滤。数据来自发布方在核查文章上加的 schema.org ClaimReview 标注（声明、声明人、结论）— [Google News Initiative](https://newsinitiative.withgoogle.com/resources/lessons/google-fact-check-tools/)
- 通过 Markup Tool 提交的标注存放在 datacommons.org，以数据 feed 公开 — [检索摘要，Google Fact Check 页面](https://toolbox.google.com/factcheck/about?hl=pl)
- 本轮没有找到 Google 公开描述过语义声明匹配或去重 — [同上](https://newsinitiative.withgoogle.com/resources/lessons/google-fact-check-tools/)

**金融新闻厂商（受控事件分类，厂商声称）**
- RavenPack 的事件类别数：RPNA 4.0 为 2,064 个，RPA 1.0 为 6,895 个；"事件相似度分析"窗口从 100 天扩到 365 天；覆盖 35 万以上实体 — [RavenPack WRDS 宣传册](https://wrds-www.wharton.upenn.edu/documents/1395/RavenPack.pdf)

### Inferences
- 生产系统都没让模型独自决定"新还是旧"。Meedan 的三档（自动 / 建议 / 新）正是 Bar-Haim 的 Dual Threshold 在运营上的版本。中间档交给人或第二道判定，是成熟做法；人对建议的确认和拒绝反过来成为标注。
- Full Fact 的教训和我们上一轮的结论一致：向量匹配之后必须有结构字段比较（人、地、数字）。对我们来说，对应的字段是对象、driver、方向、期限。
- Kazemi 的误报以"部分重叠声明"为主，Corney 提出的非对称匹配，正好对应我们"新证据只覆盖已有观点一部分"或"更具体版本"的情形。这类关系应该落到"附为证据"或"新观点"，而不是"同一观点"。
- 生产级声明匹配面对的是"同一真值条件"的声明，粒度比我们的"driver"细。我们的 driver 更接近 KPA 里的 KP 或 PAKPA 里的 aspect。所以声明匹配的经验更适合用在"证据 ↔ 观点"这一层，而不是"观点 ↔ driver"这一层。

### Gaps
- Full Fact、Meedan、Google 都没有公开生产环境的匹配 P/R，也没有公开"新声明"判定的误差率。
- Meedan 现行阈值、是否已改用 LLM 判定，没有找到 2023 年以后的一手说明。
- RavenPack 的 Event Novelty Score、事件相似度的定义与判定方法，本轮没有从一手文档核实。

## 问题 4：受控词表 / 注册表的打标与自由文本相似度聚类：实证对比、词表如何生长和去重、风险

### Takeaway
在能直接对比的研究里，"先有（或先归纳出）一个受控 schema，再做闭集归类，同时用 LLM 校验能否归并"，在精度、简洁度、冗余度上都优于纯嵌入聚类。具体包括：EDC 对比 CESI 和开放 KG，TnT-LLM 对比嵌入聚类，PAKPA 对比按句子生成的 KP。起作用的有两点：一是 LLM 逐条核对"能否替换"，二是在词表增长时去重，而不只是因为有了一个列表。风险也有实测：自由生长的 schema 依然会膨胀到数百项；聚类会过度合并；LLM 扩展词表会出现冗余和幻觉；新条目的准确率掉得最多；合并必须可逆。

### Cited Findings
**EDC：同一流程里对比"对齐目标 schema"和"自我规范化"（EMNLP 2024）**
- EDC 的流程：
  1. 开放式抽取三元组。
  2. LLM 为每个关系写定义。
  3. 用训练过的 schema 检索器，按定义召回最相似的已有关系。
  4. 让 LLM 判断"在当前语境下，X 能否被 Y 替换？"。能就映射过去；不能时，目标对齐模式下丢弃，自我规范化模式下把它作为新关系加入 schema。

  作者称，让 LLM 验证（而非只看嵌入相似度）"缓解了以往方法的过度泛化" — [Zhang & Soh 2024, EDC](https://arxiv.org/pdf/2404.03868)
- 自我规范化的人工评测（精度↑ / 关系数↓ / 冗余度↓，冗余度为每个关系与其最近邻的平均余弦）：

  | 数据集 | EDC | CESI | 开放 KG |
  |---|---|---|---|
  | WebNLG | 0.956 / 200 / 0.833 | 0.724 / 280 / 0.893 | 0.982 / 529 / 0.927 |
  | REBEL | 0.867 / 225 / 0.831 | 0.504 / 307 / 0.854 | 0.903 / 667 / 0.895 |
  | Wiki-NRE | 0.898 / 106 / 0.833 | 0.753 / 114 / 0.849 | 0.909 / 204 / 0.881 |

  标注者间一致性 0.94。作者观察到 CESI 会"不恰当地把不同关系聚到一起" — [同上 Table 2](https://arxiv.org/pdf/2404.03868)
- 消融：去掉 schema 检索器后性能下降 — [同上](https://arxiv.org/pdf/2404.03868)

**TnT-LLM：LLM 归纳分类体系后闭集打标，对比嵌入聚类（Microsoft，KDD 2024）**
- 方法：LLM 对样本做多轮"生成 → 修订"，得到标签体系；再让 LLM 打标；最后蒸馏成轻量分类器。在 Bing Copilot 数据上，生成的体系覆盖率超过 99.5%（意图和领域两套）— [Wan et al. 2024, TnT-LLM](https://arxiv.org/pdf/2403.12173)
- 人工评测：GPT-4 版 TnT-LLM 的标签准确率和用例相关性，优于"ada2 / instructor-xl 嵌入 + k-means 聚类，再由 GPT-4 / GPT-3.5 命名"的基线。作者称聚类类方法"更易受簇粒度、以及用例与输入是否对齐等建模选择的影响"— [同上](https://arxiv.org/pdf/2403.12173)
- 标注本身就有歧义：意图、领域准确率的评审者间 κ 为中等（>0.4），领域相关性只有 0.379。在中等一致性的任务上，GPT-4 与人类多数意见的一致度高于人类彼此之间。蒸馏出的轻量分类器（如嵌入上的逻辑回归）与 GPT-4 打标质量相当 — [同上](https://arxiv.org/pdf/2403.12173)

**Clio：自底向上聚类加层级归类（Anthropic，2024-12）**
- 流程是先摘要、聚类，再把底层簇归到高层类别。在合成数据上恢复已知分布：20 个高层类别时准确率 94%，敏感话题数据 18 个类别时 84% — [Clio, arXiv 2412.13678](https://arxiv.org/abs/2412.13678)

**词表增长的可靠性**
- ReLTEx（2026-08）指出：直接用 LLM 做分类体系扩展，会产生"嘈杂且冗余的概念、层级不一致的结构和幻觉"。它的做法是 LLM 生成候选、按结构校验、再控制递归扩展（本轮没取到数字）— [ReLTEx, arXiv 2608.10970](https://arxiv.org/abs/2608.10970)
- 分类体系扩展任务的标准定义是：为新概念找到最合适的父节点（CodeTaxo、ATTEMPT 等）— [CodeTaxo, ACL Findings 2025](https://preview.aclanthology.org/credits/2025.findings-acl.214)

**合并与可逆**
- Wikidata 合并重复条目时，把数据并入接收条目，旧条目变成重定向。合并前必须确认两者是同一概念（"树"和"橡树"不能合并）。撤销合并要按顺序恢复两个条目的历史版本；如果已有机器人把重定向替换成目标条目，撤销还要通知机器人维护者 — [Wikidata Help:Merge](https://www.wikidata.org/wiki/Help:Merge)

**过期与覆盖风险**
- 新实体的链接准确率最多下降 17.9%，持续存在的实体最多下降 3.1% — [TempEL](https://arxiv.org/abs/2302.02500)
- 专家事先写的 KP 集合漏掉了数据里的论点 — [KPA-2021](https://arxiv.org/pdf/2110.10577)
- RavenPack 的受控事件类别从 2,064 个增长到 6,895 个（厂商声称）— [RavenPack WRDS](https://wrds-www.wharton.upenn.edu/documents/1395/RavenPack.pdf)

### Inferences
- 注册表比自由聚类好，主要原因是"逐条用 LLM 核对能否归并"（EDC 第 4 步）和"新条目用同一模型去重"（Bar-Haim 2020b），而不是"有了列表"这件事本身。CESI 那种纯嵌入聚类恰恰过度合并，这和我们已知的"嵌入分不开方向、数字"是同一个机制。
- 自我生长的 schema 仍然有几百项（EDC 有 106–225 个关系，开放 KG 有 204–667 个）。按"每个对象一张 driver 表"、500 多个对象计算，总 driver 数会很大，且有跨对象重复（例如"利率下行"影响多个对象）。这和"观点像因子、可影响多个对象"的定义有冲突，需要决定 driver 是挂在对象上，还是全局一张表、再关联对象。
- 粒度没有客观标准（TnT-LLM 的 κ 只有 0.38–0.55）。driver 粒度一旦确定，就需要写进定义和示例里，并且用同一套判定去管新增和合并，否则会漂移。
- 可逆合并有现成范式：Wikidata 的重定向加按序恢复。注册表里 driver 的合并和观点的合并可以用同一套机制。

### Gaps
- 没找到同一数据、同一 LLM 下"闭集注册表链接"与"自由文本检索 + LLM 选择"的正面对比。EDC 的两种模式最接近，但它比较的是"有无目标 schema"，不是"注册表与自由文本"。
- 没找到金融领域 driver / 因子注册表在 LLM 打标下的准确率研究。RavenPack 只有类别规模的厂商数字。
- 注册表长期运行中的漂移，如定义变宽、同义条目累积的度量研究，本轮没找到（ReLTEx 只给了定性描述）。

## 问题 5：这些研究对 (a) 自由文本观点检索 + LLM 选择与 (b) 每对象 driver 注册表 + 闭集链接 的启示

### Takeaway
文献不支持"二选一"，支持的是分层。(b) 在"同一驱动因子"这一层更稳：闭集选择、LLM 核对能否归并、新增条目用同一判定去重，都有实证收益。(a) 的检索加挑选，仍是任何 NIL 判定前必需的召回步骤。两种方案的共同短板都是"判为新"：要显式表示 NIL、用真实的后出现条目度量、设中间档，不能指望 LLM 自觉不选已有项。

### Cited Findings
- 闭集结构能保证输出合法：GENRE 用前缀树约束，ReFinED 在候选里放 NIL — [GENRE](https://arxiv.org/abs/2010.00904)；[ReFinED](https://arxiv.org/abs/2207.04108)
- NIL 必须单独度量：AIDA 上不计 NIL 时总体 85.49，计入后 82.03，NIL 准确率只有 58.53 — [Learn to Not Link](https://ar5iv.labs.arxiv.org/html/2305.15725)
- 真实的新实体最难：NILK 上 out-of-KB F1 为 26.2–47.8 — [BLINKout](https://arxiv.org/pdf/2302.07189)
- LLM 拒绝所有选项的能力弱：降幅 30–50% — [Tam et al. 2025](https://arxiv.org/abs/2503.01550)
- BM+TH 和 Dual Threshold 在"0 或 1 个匹配为主"的分布上最好 — [Bar-Haim 2020a](https://arxiv.org/pdf/2005.01619)
- 生产系统用三档并有人在环 — [Kazemi et al. 2021](https://arxiv.org/pdf/2106.00853)；[Meedan 2020](https://meedan.org/post/tech-and-check-2020)
- 向量之后加实体、数字比较 — [Full Fact 2025](https://fullfact.org/blog/2025/feb/how-ai-can-help-fact-checkers/)
- 按 facet 加极性组织后，匹配精度为 0.95，基线为 0.66–0.83 — [PAKPA](https://arxiv.org/html/2407.14049v1)
- LLM 核对能否归并，优于纯嵌入聚类（精度 0.867–0.956 vs 0.504–0.753）— [EDC](https://arxiv.org/pdf/2404.03868)

### Inferences
**(b) 的优势（有证据支撑）**
- 把"是不是同一观点"拆成两个子问题：一是"是否同一 driver"，即闭集选 id 或 NIL；二是"方向、期限、对象"，由代码比较。这与 Full Fact"向量后加结构字段"、PAKPA"aspect 加情感"、EDC"定义后核对"的思路一致，也符合本项目"能由代码决定的不交给模型"的规则。
- driver 有了稳定 id 以后，"同 driver、方向相反 = 削弱证据"就成为一条代码规则，不再依赖嵌入去区分方向。
- 注册表天然支持可逆合并（重定向），也支持统计每个 driver 下的观点数。

**(b) 的风险（有证据支撑）**
- 粒度：driver 太宽，匹配率高、信息量低（KPA"空泛 KP 也能高分"）；太细，就退化成自由文本。
- 增长：新 driver 的提案如果不经去重，表会膨胀（EDC 的开放 KG 有 529–667 项）。
- 偏向已有项：LLM 会少报"新 driver"（NA 降幅 30–50%）。
- 过期：新条目的准确率掉得最多（TempEL 为 17.9%）。
- 专家预设覆盖不全：KPA 的专家 KP 漏项。

**(a) 的必要性**
- 无论是哪种方案，判定前都要召回一小组候选（BLINK、ChatEL、OneNet、EDC 的 schema 检索器）。(a) 的"共享对象过滤、嵌入 top-20、混合排序到 top-4"就是这一步。在 (b) 下，它变成"在 driver 表里召回 top-k 个 driver"，加上"在同一 driver 下召回已有观点"。

**两者共同的设计点（文献给出的具体做法）**
- 把 NIL / 新建作为一个有描述的显式候选；判定用 BM+TH，必要时 Dual Threshold。
- 设中间档，让第二道判定或人工复核处理，复核结果回流为标注（Meedan 的做法）。
- 用"旧库 + 后来的文档"构造测试集，单独报告"判为新"的 P/R（BLINKout 的 versioning 做法）。训练和提示里要有足够的 NIL 样例（Learn to Not Link）。
- 新 driver 入表前，先用同一判定与已有 driver 两两核对（Bar-Haim 2020b 的第 3 步、EDC 的第 4 步）；合并做成重定向（Wikidata）。
- 观点对证据这一层用声明匹配的非对称关系：更具体或部分重叠的作为证据附上，而不是认作同一观点（Corney 2021，Kazemi 的误报分析）。

**未解决的设计问题（文献给不出答案）**
- driver 该挂在对象上，还是全局一张表再关联对象？观点被定义为"一个驱动因子影响多个对象"，按对象建表会导致跨对象重复。

### Gaps
- 没有任何研究在同一任务上测量"闭集注册表链接"与"自由文本检索 + LLM 选择"的准确率差。上面的判断来自相邻任务（EDC、PAKPA、TnT-LLM、KPA），属于推断，不是测量。
- 没找到流式场景下（每天上千篇文档、注册表持续增长）注册表质量随时间变化的实测。
- 没找到 LLM 在"新 driver 提案"上的召回与精度数据，即它多常该提而没提、不该提却提了。
