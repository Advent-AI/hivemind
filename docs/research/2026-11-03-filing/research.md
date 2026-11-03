# 挂题专题（2026-11-03 起）：证据为什么挂错题、为什么都挤进收入大题

Alex（2026-11-03）："你这个单独开一个专题出来解决因为已经处理很久了下来我要focus解决，你把你的研究写好让codex subagent 独立review 你们两个battle
找到我们真正忽略的细节 - 是promot，是系统结构设计还是到底哪里有问题挂错一堆东西，机制是不是有问题（一定要挂吗？有没有可能是杂音"。

本页是 Claude 的研究底稿，给独立审查读。所有数字都有脚本在本文件夹（`$0`，只读存好的数据）。冻结的尺子（AGENTS §7.1）不动；第 1–4 步已冻结
（D274、D354），任何修法都是新版本，Alex 开。

## 1. 现在的机制（一个决定者，D264；冻结配置 `poc/config/poc-v108.json`）

1. 每篇文章一次抽取调用。请求里有当天开着的题，每道题一行"收件说明"（`placement.takes(view, paths_once=True)`，代码写的）。实际请求见
   `broadcom-request-v108-d1-call818.json`（用户块里 `[Open questions]`）。
2. 模型为每条证据填 `links`。`links` 的定义写在 schema 里（`placement.FILING_RULE_ROOT_FALLBACK`，全文）：

   > The questions this statement is filed under, decided after you have decided it is evidence: the id of the narrowest open question in
   > [Open questions] whose answer this statement makes more or less likely, as that question's own figure, step or estimate or through the
   > demand, supply, competition or pricing behind its answer; compare the specific questions before a company-wide revenue or margin question
   > and take that one only, never a broader question beside it; a shared company, industry, event or ecosystem is not a connection, and the
   > statement need not repeat the question's words (a variant, sibling or other name of the subject counts); whoever says it, and even when it
   > gives no period, basis or exact amount, because the weight is judged later; an estimate for another period or population of a question's
   > quantity is filed under it when no open question covers that period; when no specific question is connected, a statement that moves the
   > demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its period; plus the ids
   > of this answer's candidates the statement supports; empty when no question and no candidate is connected, however important it sounds.

3. 代码：一条证据挂在驱动题和它的上级题下时只留驱动题（`extraction.narrowest_links`，D207）；一个链接都没有的证据扔掉，原因记 `no home`（D209）。
   所以"留不留"和"挂哪"是同一个决定：挂不上就不留。
4. 判断只读挂在自己题下的证据，而且只读最近的：上 5 次判断之后到的，加上最近 10 次判断引用过的（`views/judging.evidence_in_view`，D198）。
5. 数字题的收件说明（paths_once）只写量、范围和期间，例如自研芯片题：
   `takes: spend_total figures, guidance, estimates and revisions for Spending on custom AI silicon (ASICs) at cloud providers in calendar 2026, this question's period 2026-01-01..2026-12-31`。

## 2. 数据

### 2.1 关键证据挂到对的题了吗（`gold_home_census.py` → `filing-census.txt`）

"该挂哪"没有现成的标准答案（D2 的事项 → 题映射没建）。代理：判断金标（读者 B，冻结）每道题列了推理用到的文章原话（packet 里的条目）。每条按
文章 + 原话重合度 ≥ 0.6 找到账本里的证据，看它挂在哪。19 道有题的金标题，153 条引用，三遍共 459 次。

| | 挂到这道题 | 挂到别的题 | 不在账本里（没写或被扔） |
|---|---|---|---|
| v94 三遍 | 157 | 140 | 162 |
| v108 三遍 | 177 | 151 | 131 |

挂错的去向：v94 数据中心收入（v2）65、毛利 17、总收入（v1）14……；v108 总收入 39、数据中心收入 31、Blackwell+Rubin 收入（v20）19、中国份额 15……
**两版都有约三分之一的关键证据挂在别的题下；收入大题是主要去处。** 代理的局限：读者 B 只引决定性的证据，"没被引"不等于没用。

### 2.2 收容题里装的是什么（`sink_census.py` → `sink-census.txt`）

每条挂在收容题下的证据，先对抽取金标（golden-v5）分类，核心/辅助的再看判断金标有没有引用它的条目、引给哪道题。

| | 链接 | 不是金标文章 | 核心 | 辅助 | 可选 | 不收 | 没列 | 核心+辅助里：引给本题 / 别的题 / 没有题引 |
|---|---|---|---|---|---|---|---|---|
| v108 总收入 d1 | 143 | 68 | 6 | 34 | 7 | 16 | 12 | 3 / 7 / 30 |
| v108 总收入 d2 | 135 | 84 | 10 | 18 | 2 | 14 | 7 | 4 / 7 / 17 |
| v108 总收入 d3 | 140 | 77 | 9 | 21 | 7 | 11 | 15 | 4 / 4 / 22 |
| v94 数据中心 d1 | 179 | 98 | 12 | 35 | 6 | 17 | 11 | 2 / 11 / 34 |
| v94 数据中心 d2 | 209 | 106 | 14 | 41 | 12 | 16 | 20 | 3 / 14 / 38 |
| v94 数据中心 d3 | 210 | 114 | 10 | 41 | 10 | 22 | 13 | 2 / 9 / 40 |

读：金标文章里挂进收容题的，约一半是标准说不收、可选或没列的；标准要收的里面，判断金标拿来推这道题的每遍只有 2–4 条，没有任何题引用的 17–40 条。
抽读 v108 总收入 d1 的 143 条（一条一条的分类是关键词粗分，要人读确认）：约 57 条讲英伟达收入或业绩（"一季度营收 816 亿"被多家重复报），约 60 条
是英伟达的小新闻（Uber 自动驾驶、Omniverse 免费、Palantir 用 Nemotron、Valar 核微堆、Cramer 说英伟达太贵），约 26 条是别的公司或行业（博通、美银）。

### 2.3 对判断的影响（`judgement-gold/score-r9-frozen-v108-d*.txt` 对 `score-r7-combined-v94-d*.txt`）

- 自研芯片题（q16，金标 600–850 亿美元，依据是博通 AI 芯片营收：二季度 108 亿、三季度指引 160 亿）：v94 博通的话三遍里两遍挂到这道题，那两遍判
  400–600 亿和 600–800 亿（一对一近）；没挂上那遍判低于 400 亿。v108 博通的话 7–10 条，挂到总收入、数据中心收入、加速器份额，从没挂到这道题；三遍都判
  低于 400 亿，理由里一次没提博通。
- 营业利润率题（q10）：v94 每遍 1–2 条（一条是"美光营业利润率 80.4% 对英伟达约 66%"），v108 一条没有，三遍都没判。
- 总收入、数据中心收入、Blackwell+Rubin 收入三题 v94 三遍对两遍，v108 三遍全对。

### 2.4 请求会不会爆（判断请求的输入 token，按天；`e2e-funnel-r9-frozen-v108.txt`）

v108 总收入从 2k 涨到第 10 天 13k 后停在 12–14k；v94 数据中心从 3k 涨到 13–17k 后停住。判断只看最近到的和最近引用的（2.1 第 4 条），所以随天数
有上限，上限跟每天进来的条数走。语料里点名英伟达的文章：7 月 1,008、8 月 1,159、9 月 1,776、10 月 2,076，按比例估 9–10 月约 25k（估计，不是测量）。
三个月封存那次停下时最大的判断请求是 9.3 万 token（当时一条证据平均挂 3.3 道题、每天 40–60 条进一道题）。**结论：v108 不太会在大小上爆；问题在内容。**

### 2.5 模型本人的说法（`probe-broadcom-filing.txt`，存档对话续问两次）

博通那篇 v108 写了 4 条，3 条讲博通（e2 营收 108 亿、e3 CEO"增长来自定制 AI 加速器需求"、e4 160 亿），全挂总收入。问它为什么不挂自研芯片题：
- 第 1 次："No instruction supports filing either item under v1; that link was an error ... the $10.80 billion figure is Broadcom's quarterly
  sales—not cloud providers' calendar-2026 spending on custom AI silicon ... neither belongs under v16."
- 第 2 次："I treated Broadcom's AI sales and Tan's demand comment as competitor information bearing on NVIDIA's revenue prospects; v16 is
  specifically for estimates of cloud providers' custom-AI-silicon spending ... I gave too much weight to the rule that a competitor's reported
  revenue can bear on the company's markets, and too little to the distinction between a relevant signal and the specific quantity a question takes."

两次都把收件说明读成"只收这道题自己那个数"；把"供应商卖了多少"和"买方花了多少"当成两件事；落到总收入走的是兜底那句（竞争 → 公司收入题）。

### 2.6 第一轮审查期间补的两项（Claude，2026-11-03）

**标准要收、没有题引用的那 30 条（v108 总收入 d1，逐条读过）：** 三类。(a) 生态小动作：Palantir 用 Nemotron（4 条，同一件事不同媒体）、
LangChain 调优 Nemotron（5 条）、Hugging Face、Anthropic BioNeMo、RTX 3060 重新上架、SpaceX 轨道数据中心、Valar 核电、Firmus / Sharon AI 园区（3 条）；
抽取标准按 D240 收它们，题的标准下没有题要它们，兜底把它们送进总收入。(b) 其实属于窄题：彭博"定制 ASIC 市场年增 27%"（自研芯片）、
Cerebras"比英伟达快 15 倍"、SambaNova 融资和摩根大通部署（份额 / 竞争）、"一季度 75 个数据中心项目延期或取消"（资本开支）。(c) 真属于总收入：
"二季度营收指引 910 亿 ±2%"——代理没认出它是金标用的（读者 B 引的是同一事实的另一条原话），**所以 2.1 的"挂到这道题"是低估。**

**金标引用了、却不在账本里的（`missing_census.py` → `missing-census.txt`）：**

| | 没写 | 写了、没家被扔 | 写了、引文被拒 |
|---|---|---|---|
| v94 三遍 | 130 | 28 | 4 |
| v108 三遍 | 113 | 16 | 2 |

v108 没家被扔的例子：金标拿"上季度净利润 583 亿"推营业利润率（q10），拿"经营现金流 503 亿、自由现金流 486 亿"推每股收益和资本开支（q11、q12），
拿"一季度数据中心收入 752.5 亿"推数据中心收入（q02）。窄题的收件说明只认自己那个数，推它用的数没处挂；又不是"需求、供给、竞争、定价"，兜底也不收，
于是扔掉。这和博通进不了自研芯片题是同一个读法。459 次里：挂对 177、挂别处 151、没写 113、没家被扔 16、引文被拒 2。

## 3. 这几条规则是怎么来的（DECISIONS）

- 一条证据只挂最窄的一道（D207）：三个月封存那次证据膨胀（D198 之前一条平均挂 3.3 道），挂题一家制后第 1 周每条 3.3 → 1.82、最大题 106 → 52。
- 没家就扔（D209）："if it doesn't matter, just fucking throw it away"。
- 一个决定者（D264）：抽取直接挂题，不再单独放题；挂不上就扔。
- 数字题收件说明的共同结尾"…以及背后的需求、供给、竞争、定价"：让间接证据进窄题，也让数据中心收入题成了收容所（Codex 第二轮：三组 89 次杂音 59 次挂
  在数据中心收入题）。v74f 去掉结尾、不兜底：杂音 53，但 82 条要收的写了没题挂、辅助 95 → 70。v74h 去掉结尾、加公司收入题兜底：辅助回来，杂音 100，
  收容所搬到总收入。v74i 冻结（D274）。
- 抽取标准（第 1 块尺子）收没写金额的具名动作（D240："不一定什么条件数据时间都要满足，你应该把它记录下来，只是可能档位低一点"）；题的标准说小事
  不开题（D248）。

## 4. 假设（等审查来打）

- **H1 提示词：** 收件说明按字面读，代理证据（供应商营收代表买方花费）进不了窄题；`links` 定义里"或通过背后的需求、供给、竞争、定价"被收件说明压过。
- **H2 结构：** "留不留"和"挂哪"绑在同一个决定里（D209 + D264）。抽取标准要收的小动作（D240）在题的标准下没有题（D248），为了不丢只能兜底，
  兜底就成收容所。两块标准之间没有出口。
- **H3 机制：** 一条只挂一道（D207）和"一条事实几个用途"冲突（博通同时是自研芯片花费的依据、英伟达份额的竞争信号）。
- **H4 杂音：** 收容题里约一半是标准不收或没列的；标准要收的里大多数没有任何判断题用。挂进去不帮判断，反而稀释。也许不是所有被留下的证据都该有家。
- **H5 架构：** 挂题发生在抽取时（每篇文章推给题）。另一种是判断时由每道题自己去库里取（拉），或两级（先入库不挂，再由题挑）。现在判断只读挂在
  自己下面的。
- **H6 度量：** 我们没有"该挂哪"的标准答案，一直在用代理；不知道一个修法到底修了多少。

## 5. 要审查回答的

1. 我们忽略了什么细节（提示词、schema、代码、数据流、标准之间、度量）？每条给出处（文件 + 行，或数据 + 查询）。
2. H1–H6 逐条：成立、不成立、部分成立，数据怎么说。可以自己写只读查询验证（数据库路径见下）。
3. 根上是提示词、系统结构设计，还是机制本身？"一定要挂吗？"、"是不是本来就是杂音？"给明确回答。
4. 只提一条结构性的规则（AGENTS §1："When one mechanism draws findings round after round, stop answering findings: propose one structural rule"），
   写清它会动哪些读者、会丢什么、怎么在存好的数据上零成本或几美分先证明。

## 6. 范围和护栏

- 冻结的尺子一个字不动（AGENTS §7.1）；不改任何提示词或代码（只读审查）；不发付费调用。
- 提示词是通用对冲基金分析师（AGENTS §6）：任何修法对银行、药厂、零售、芯片都成立，不点名英伟达或测试文章，不按 bench 拟合。
- 代码只管身份，不管重要性（AGENTS §2）。

## 7. 数据位置

- v108 三遍：`poc/data/e2e-r9-frozen-v108-2026-11-03/d{1,2,3}/`（`views.sqlite`：`evidence`、`evidence_links`、`judgements`、`views`、`rungs`；
  `archive.sqlite`：`model_calls` 含每次请求和答案）。
- v94 三遍：`../hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94/d{1,2,3}/`。
- 金标：`docs/research/2026-10-29-ledger-standard/golden-v5/`（抽取）、`docs/research/2026-11-01-e2e-loop/judgement-gold/`（判断）。
- 标准：`docs/prd/05-extraction-standard.html`；决定：`docs/DECISIONS.md`（D198、D207–D209、D240、D248、D250、D264、D273、D274、D354）。
- 代码：`src/hivemind/placement.py`（takes、FILING_RULE_ROOT_FALLBACK、question_lines）、`src/hivemind/extraction.py`（narrowest_links、sift、
  file_reading、no home）、`src/hivemind/views/judging.py`（evidence_in_view）。
