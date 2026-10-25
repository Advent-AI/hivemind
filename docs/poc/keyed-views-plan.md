# 观点有键：系统修正方案（2026-10-25，D153）

> 历史方案与 T1–T4c 记录。D155 已替代这里的清单门槛、别名自动身份与后续执行顺序；当前合同和量化结果以 [改进计划](grouping-improvement-plan.md) 为准。本文旧实验数字保留，不代表分组已经通过。

一句话：**观点带一把由代码持有的键；模型只填键、只从展示的名字里选、不再决定身份。** 这一条规则落在三处——量、主线、
要盯的量清单——分别对应今晚反复出现的三类问题：同一个量开多条、归组不稳、开错和漏开。复盘和数在
`docs/research/2026-10-25-structural-review.md`。每一步小范围测试、量化、记进 `pipeline-tuning-log.md`，然后才改默认管线。

范围：抽取合同、观点记录、比对的身份规则、写入、宇宙文件、服务和 idea 的查找方式。不动：只追加与按天截止、顺序号、
存档重放、四层证据、一天一判、UI 合同（thesis-ui/1）、英文迁移（单列；梯子数字化已把它最难的一块拿掉）。

## 1. 要解决什么（基线数）

| 问题 | 基线（第三遍封存 + 今晚一周小跑） | 目标 |
|---|---|---|
| 同一个量开多条 | 94 条里：ai-capex 9 条「支出」观点、税率两条、AMD 数据中心两条；一周小跑第一天就出现 Rubin 出货两条（自然年 vs 财年措辞） | 写入时键冲突 = 0（按构造）；迁移时把现有重复合并，数出几对 |
| 开错 | 58 条新开里 9 条产品琐事（16%）；关税/出口管制 8/8 条是反倾销、钨废料公告 | 琐事 0（清单门槛） |
| 漏开 | H200 对华许可 0 条（60 篇提到）；OpenAI 担保只开成金额 | 清单上的量每项有观点（覆盖率），漏的进复核池可见 |
| 归组 | 24 份原答 5 个错引用、1 处漏归 | 接线错 0（名字即选择）；语义错单独计数 |
| idea 选直接观点 | 金标 18/20 对、2 个陷阱；画布重合 0.65 | 键查找：20/20；重合度再量 |
| 梯子是句子 | 380 格里 270 格靠正则解析；解析器只认中文 | 格带数字上下界，解析器退场 |

## 2. 合同

### 2.1 观点的键

抽取在候选观点里填闭合字段；写入把它们存成列；比对先比键。`looks_at`、`question` 保留给人读。

| 字段 | 取值 | 谁填 | 谁查 | 例子 |
|---|---|---|---|---|
| `object` | 宇宙里的对象（已有） | 模型 | 代码：必须在宇宙里 | NVDA、ai-capex |
| `measure` | 闭合清单：公司 `total_revenue, segment_revenue, product_revenue, gross_margin, operating_margin, operating_expense_growth, total_expenses, operating_loss, tax_rate, capex, shipments_or_capacity, run_rate, design_wins, event`；主题 `spend_total, financing_amount, price, capacity, growth_rate, policy_event, other`（T1 后补齐六个） | 模型从枚举选 | schema 枚举；`other` 不开、进复核池 | gross_margin |
| `scope` | 量的限定名：分部、产品线、口径群（「Data Center」「五大云厂商」「Big Tech」）；从展示过的名字里选，或声明新的 | 模型（选择即枚举，见 2.6） | 代码归一化后绑定 | Data Center |
| `period` | `{start, end}` ISO 日期；财年由宇宙的财年月换算（FY2027 → 2026-02-01..2027-01-31） | 模型写财年或自然年，代码换算、校验 | 代码：end 不超过「明年」规则 | 2026-02-01..2027-01-31 |
| `basis` | `GAAP, non_GAAP, n/a` | 模型 | 枚举 | non_GAAP |
| `unit` | `USD, percent, count, GW, TWD, …`（闭合） | 模型 | 枚举 | USD |
| `event_type` | measure=event 时：`launch, shipment, licence, approval, deal_close, deployment, other` | 模型 | 枚举 | licence |
| `subjects` | 主线名字列表：展示过的名字或新声明（名字 + 范围） | 模型（2.6） | 代码绑定编号（D152 切片） | Vera Rubin platform rollout |

**键 = (object, measure, scope, period, basis, unit)**（unit 是 T0 打键后补的：同一个量的水平值和增速是两条）；事件观点的键 = (object, event, event_type, scope, period)。相同键 = 同一条观点
（新证据或接续/替代，按 06 已有规则），由代码判，模型不再问「是不是同一条」。键不同而文字相似的，才交给模型判（剩余）。

### 2.2 梯子的格

每格 `{label, lo, hi}`，`lo/hi` 为数字或空（开区间），单位取观点的 `unit`；是/否两格 `{label: 是/否}`。`condition` 句子保留
给人读。代码检查：五格不重叠、不留空、单调；中间格含公司给的数（已有规则）。服务的 evaluate 直接比数字，`service.py` 的
正则解析器只留给迁移前的旧库读。

### 2.3 主线是对象

`poc/universe.json` 加 `subjects`：`{id, name, kind: product_line | program | customer_deployment | policy_process, of: 公司或主题,
aliases: [...]}`。例：`rubin`（Vera Rubin、Rubin、NVL72…，of NVDA）、`sk-ai-factory`（SK Telecom AI factory…，of NVDA，客户专属）、
`h20-china-licence`（H20、H200、对华许可…，of chip-export-controls）。成员关系由代码按命中写：候选观点的问题或其证据原句命
中主线别名 → 成员；模型在 `subjects` 里只确认或声明新主线（新主线进复核池，人看过后才进宇宙）。归组从「模型选对编号」变成
「别名命中 + 确认」。主线没有状态、不是依赖、不是上层论点（D149 原话）。

### 2.4 要盯的量清单（门槛）

`universe.json` 每个对象加 `watch`：这个对象分析师要盯的 (measure, scope) 对，附一句为什么。例：NVDA 盯 total_revenue、
segment_revenue[Data Center]、segment_revenue[Compute & Networking]、gross_margin、operating_expense_growth、tax_rate、capex、
product_revenue[Blackwell/Rubin]、event[shipment: Rubin]、event[licence: H20/H200 China]；ai-capex 盯 spend_total[五大云厂商]、
spend_total[Big Tech]、spend_total[全球 AI 基础设施]。规则：候选观点的 (measure, scope) 在清单上 → 开；不在 → 进复核池，
不开、不丢，带原句和它要开的键；复核池由人或代理看，进清单后下次自动开。清单是产品知识（像别名一样），初版由我以分析师
身份写、Alex 改（附录 A）。琐事（游戏、软件功能、工具更新）因为不在任何清单上而不会开。

### 2.5 身份规则

T1（封存 94 条打键）证明：键抓得到管线漏掉的重复，但「键相同即同一条」会误并（量的清单粗、scope 自由写）。所以键是身份的
必要条件，不是充分条件：
1. 代码：量不同（measure 或归一化 scope 不同）→ 绝不是同一条；模型若把候选归入这样的观点，比对检查拒绝，候选按新开处理。
2. 代码：键相同、或只差期间且期间重叠 → 「必须确认」的一对：比对调用只拿这一对问一个窄问题（同一个量吗）；是 → 归入 /
   接续 / 替代按 06 已有规则；否 → 新开。没有这样一对的候选不再问身份，直接新开。
3. 期间首尾相接、键相同 → 接续候选（06 已有）。
4. 比对的证据身份（重复 / 替代 / 新证据）不变。

### 2.6 选择即枚举（统一机制）

凡是模型要「指向」库里已有的东西（scope 名、主线名、分部名），schema 用枚举列出已展示的名字加一个 `new`；选 `new` 必须给
名字和范围；代码把名字归一化后绑定编号。模型不写编号。这是 D150 五个错引用（定义写对、编号填错）的构造性修复，
`poc/hierarchy_study/subject_names.py` 已实现这一机制并测过投影。

### 2.7 T2 之后补进合同的三条（都在代码里，都有测试）

- scope 的拼写归代码：没有范围的量（总收入、毛利率、利润率、费用增幅、总费用、亏损、税率、capex）scope 一律为空；清单上的范围按清单
  的拼写，由别名命中（`scope_hits`）；只有清单没写的范围才用模型的字。
- 公司年度数的期间由对象财年从 `year` 算出（`fiscal_period`），不用模型写的日期；事件保留模型的期间。
- 身份判定分两种键：代码持有的键（scope 来自清单或为空）——同键、同期、口径和单位不冲突的唯一开着的观点就是同一条，模型说「新」也
  并（记 note）；模型持有的键（自由范围）——同键列表交模型确认。归入另一个期间或另一个量，一律拒绝。

### 2.8 T4 之后补进合同的一条

- scope 分两种归属（`scope_source`，随键存进库）：代码持有（清单拼写或为空）和模型自写。只有双方都是代码持有时，scope 才参与「不同的量」
  的判定和自动合并；模型自写的 scope 只是措辞——这种候选和同量、同期的全部开着的观点并排给模型，由模型定归入还是新开，代码不按措辞
  拒绝（T4：一个融资故事因措辞不同开了 13 条，键拒了模型 5 次正确的合并）。清单里没有的量一旦出现一簇（俄亥俄园区的融资和容量、SK 工厂
  容量），正确的做法是给清单加一条带别名的范围，让它变成代码持有，而不是放宽规则。

## 3. 状态 × 事件（候选观点从抽取到写入）

| 状态 / 事件 | 转移、写入、日期 |
|---|---|
| 候选到达，键完整 | 查清单：在 → 继续；不在 → 写复核池（`review_pool_entries`，带键、原句、来源顺序号），不开，不报错 |
| 候选键缺字段或 measure=other | 复核池，理由「键不完整」；不进写入 |
| 键与库中某开着的观点相同 | 不新开；候选的证据连到那条；梯子不同 → 按 06 接续/替代；记 `merged` 步骤 |
| 键与库中某关闭/到期的观点相同 | 新 period 相接 → 接续；否则新开并记前驱 |
| 键相同的两条候选在同一份交接里 | 合为一条（先到的键持有） |
| 事件候选，键相同文字不同 | 代码先判同键；仍交模型确认（2.5 第 3 条）；模型说不同 → 两条都进复核池，不开 |
| scope / subject 选了 `new` | 名字归一化：等于已展示名 → 绑旧编号并计数；否则新编号；新主线名进复核池（不建对象），成员先按别名 |
| 写入失败 / 崩溃 | 候选、复核池、成员同一事务；重跑从处理记录接续（已有） |
| 重送同一信息 | 路由 skipped（已有）；复核池不重复写（唯一索引：键 + 来源） |
| 清单更新后的下一次运行 | 复核池里命中新清单项的条目由人点「开」或代理在下一轮开；不回溯重跑 |
| 迁移（旧库打键） | 新副本；每条旧观点一次键填写（模型）+ 代码校验；键冲突对单独报告，不自动合并封存库 |
| 跨期：FY 与自然年 | period 一律存起止日；展示给模型时同时给财年注（已有 fiscal_note） |

## 4. 值 × 读者

| 值 | 写者 | 读者 |
|---|---|---|
| `measure, scope, period, basis, unit, event_type` | 抽取（模型填）→ 写入（列） | 比对身份（代码）、清单门槛、服务 evaluate、idea 的直接观点查找、报告、迁移脚本 |
| 格的 `lo/hi` | 抽取 → 写入 | evaluate（claim 判定）、UI 的梯子显示（经 bundle，不改 thesis-ui/1 的字段名：`condition` 仍给，数字另加字段） |
| `subjects` 成员 | 代码按别名 + 模型确认 → 写入 | idea 的相关观点（替代今天稀疏的依赖图）、服务 `/views` 过滤、报告 |
| `watch` 清单、`subjects` 别名 | 分析师（universe.json） | 抽取提示词第 5 块（展示）、门槛、成员命中 |
| 复核池条目 | 写入 | 人 / 代理的复核页、下一轮开题、漏开率的分母 |

## 5. 新路径 × 旧检查

| 旧检查 | 新路径上 |
|---|---|
| 梯子五格 / 两格、标签顺序（`check_ladder`） | 保留；加数字检查（不重叠、不留空、单调） |
| 年份不超过明年 | 改为 period.end 不超过明年末（同义，按日期） |
| 出处检查（原句在原文里） | 不变 |
| 比对检查（候选只能归入展示过的观点、证据目标在列表里） | 身份改为键优先后，模型只对事件剩余作答；检查范围缩小、不放松 |
| 依赖检查、重判顺序、一天一判 | 不变 |
| preflight 的四段 | 加第五段：键完整率、复核池分布、键冲突数（0 元重放） |
| 服务 evaluate 的梯子解析 | 新库走数字；旧库仍走解析器直到迁移 |

## 6. 先前决定

D33（抽取定归属、比对定身份、写入保存）：保留边界，身份的大部分从模型移到代码。D37 / D58–D60（冻结）：本方案是
D153 授权的偏离，细则成为新决定。D63（一天一判）不变。D91（没有观点返回 null）不变。D133（英文原生）：梯子数字化
是其前提。D135 / D145 / D146（idea 两次调用、完整合同、金标）：idea 的直接观点改为键查找，金标不变。D142–D150（归组）：
2.3 替代「模型选编号」，2.6 是 D150 诊断的构造性修复。

## 7. 迁移

封存库不动。新副本：94 条封存观点 + 一周小跑的观点各做一次「打键」调用（模型按 2.1 的 schema 从 `looks_at`、问题、梯子
填键；代码校验），写入副本的新列；键冲突对输出报告，由我以分析师身份逐对读，合并与否记录，不自动合并。约 125 次调用，
估算 $0.6。

## 8. 小范围测试与量化（每项一行进 `pipeline-tuning-log.md`）

| # | 测什么 | 输入与上限 | 指标 | 通过线 |
|---|---|---|---|---|
| T0 | 基线 | 一周小跑（poc-v14）的 trace，$0 | 重复对、琐事数、清单覆盖、复核池（无）、每天成本 | 记录 |
| T1 | 键能不能抓重复 | 迁移打键（7.），≤ $1 | 键冲突对数；逐对读：真重复 / 真不同 | 真重复全部被抓到（v8/v10、税率对、支出家族）；误并 0 |
| T2 | 带键 + 门槛的抽取 | 开题 20 篇，≤ $2 | 琐事 0；清单覆盖；复核池条目逐条读；键完整率 | 琐事 0、H200 许可开出、复核池里没有清单内的量 |
| T3 | 归组 | 已备好的 subject-names 实验（开发 3+1、留出 Google / AMD 各 3），≤ $1.5；再加别名命中臂 | 接线错、重复声明、语义错、漏归分开 | 接线 0；Google ≥ 2/3 进 Rubin；AMD 0/3 |
| T4 | 整周 | 7 月 24–31，≤ $10 | T0 的全部指标对比 | 重复 0、琐事 0、覆盖 ≥ 基线、成本不升 > 20% |
| T5 | idea 在带键的库上 | 20 句金标 + 8×3 稳定性，≤ $1 | 直接观点对、陷阱、claim、重合度 | 20/20、0 陷阱、重合度 ≥ 0.65。**推迟到整段重跑之后**：金标引用的是封存库的编号，要按键映射到新库；一周的库只到 7 月 31 日，金标里 8 月才开的观点（CoreWeave、AMD、Meta）没有 |

反过拟合：清单和主线别名在 T2 之前写定并封存校验和；留出文章（Google、AMD）不参与设计；指标定义不随结果改。

## 8a. 结果（2026-10-25 夜，详见 `pipeline-tuning-log.md`）

T1 打键抓到了重复也暴露了误并 → 键是必要条件；T2–T2d 在开题 20 篇上把重复从 4 对收到 0；T4–T4c 在整周上：琐事 1 → 0、同键重复 0、
一周费用 −19%、复核池让清单外的量可见（23 条，其中 17 条该进清单）。未收敛：模型自写 scope 的一簇（融资）8 条——补清单而不是改规
则，随整段重跑做。T3（归组）开发集 4/4 没提出候选，无结论；T5（idea）推迟到整段重跑后。

## 9. 不做的事

不生成主线总结或上层论点；不改 UI 合同；不回填历史评审；不在本方案里做英文迁移（但 2.2 使梯子不再依赖语言）；不做全库
聚类；复核池初版只是一张表和一页列表，不做工作流。

## 10. 顺序

T0（一周跑完，读 trace）→ 写定附录 A 的清单和主线别名 → T1 → 方案细则记决定 → 改抽取合同、写入、比对、evaluate、preflight
（带测试）→ T2 → T3 → T4 → T5 → 结果表进本文件，再决定整晚重跑。

## 附录 A：要盯的量清单与主线别名（分析师草稿，Alex 改）

| 对象 | 要盯的量 (measure[scope]) | 主线（别名） |
|---|---|---|
| NVDA | total_revenue；segment_revenue[Data Center]；segment_revenue[Compute & Networking]；gross_margin；operating_expense_growth；tax_rate；capex；product_revenue[Blackwell+Rubin]；shipments_or_capacity[Rubin]；event[shipment: Rubin]；event[licence: H20/H200 China] | rubin（Vera Rubin、Rubin、NVL72、Vera）；blackwell（Blackwell、GB200、GB300、B300）；china-licence（H20、H200、对华许可、export licence） |
| AMD | total_revenue；segment_revenue[Data Center]；event[shipment: MI450 / Helios] | mi450（MI450、Helios、MI500） |
| TSM | capex；total_revenue；shipments_or_capacity[CoWoS] | cowos（CoWoS、advanced packaging） |
| META / MSFT / AMZN / GOOGL | total_revenue；segment_revenue[最大分部]；capex | — |
| CRWV | total_revenue；capex；shipments_or_capacity[active power] | — |
| ai-capex | spend_total[五大云厂商]；spend_total[Big Tech]；spend_total[全球 AI 基础设施]；price[H100 rental] | hyperscaler-capex（capex、资本开支、AI infrastructure spend） |
| chip-export-controls | policy_event[licence: AI chips to China] | china-licence（同上） |
| us-china-tariffs | policy_event[tariff: semiconductors / servers]（232） | — |
| semiconductor-cycle | growth_rate[industry revenue] | — |
| supply-chain-shift | capex[TSMC]；capacity[CoWoS] | cowos |

清单外出现的量（SpaceX 算力、Uber L4 车辆、Zankore 200MW、GeForce NOW 游戏数）进复核池；Alex 认为该盯的，加进清单。
