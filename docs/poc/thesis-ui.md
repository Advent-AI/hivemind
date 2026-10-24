# Thesis UI：数据与组件边界

本轮只整理 Thesis 和页面骨架。Idea 的判断、数字输入和匹配仍是演示代码，隔离在 `legacy` 模块，留到下一轮。
2026-10-24 晚：Idea 卡接到了服务（`poc/ui/src/idea/idea.js`，`docs/poc/idea-card.md`）：一句话 POST `/ideas`，回复经 `fromIdeaResponse` 进合同，`reading.chosen[0]` 做主卡、其余做支撑；本地匹配的演示代码 `legacy/idea.js` 已按 Alex 的要求删除。
例如：agent 取回 v3 的完整记录，交给一个转换函数，得到同一份已验证的 Thesis；卡片、历史图、证据列表和详情都读它，不各猜一套字段。

## 范围与依据

- D76、D112：服务负责取数和 agent 判断，UI 不调用模型、不保管密钥、不重写判断。
- D78、D81、D87、D97–D129：保留已确定的命名、颜色、图、交互、居中方式和字号。
- 新的入口接收 `thesis-ui/1` 数据；现有 `view_bundle` 经过唯一的适配器再进入 UI。schema 是允许字段的唯一清单。
- 不改抽取、比对、评分或 Idea 产品设计。不在本轮接通付费调用。新增一个只读取数入口 `thesis_bundles` / `GET /thesis-bundles`，复用已有 bundle writer，不重新组装源数据。

## 当前范围的清点

`data.en.json`：42 个 Thesis、375 次判断、1,089 个证据链接、44 条开关记录、32 条依赖。
中英文文件同构。现有一页同时负责展示、领域推导、交互和演示匹配；bundle 中评分为 position，UI 又根据标签猜 score。
开关和依赖只有 seq，证据的 publication day 被当成到达日期，因此历史重放没有足够字段稳定地还原状态。

## 所有权

| 模块 | 输入 | 输出/职责 | 不负责 |
|---|---|---|---|
| `model/thesis.schema.json` | agent 提供的规范数据 | 固定版本和封闭形状 | 渲染 |
| `adapters/bundle.js` | mock 或 API 的 bundle | 显式 score、日期、规范 Thesis | 网络与模型调用 |
| `model/contract.js` | 规范数据 | schema 与引用/时间关系校验；错误含字段路径 | 修补错误数据 |
| `model/thesis.js` | 已验证数据、指定日期 | 当前判断、状态、证据、关系、历史选择 | DOM |
| `components/thesis-card.js` | Thesis、日期范围 | 卡片 | Idea 匹配 |
| `components/thesis-chart.js` | Thesis、日期范围、回调 | 图与选择坐标 | 取数 |
| `components/thesis-detail.js` | 数据集、Thesis id、日期 | Overview/Evidence/History；拥有自己的交互状态和销毁函数 | 全局变量 |
| `components/canvas.js` | 已选择的卡片、回调 | 摆放、连线、平移、缩放 | 决定哪个 Thesis 匹配 Idea |
| `legacy/idea.js` + demo entry | 用户输入、旧演示数据 | 原来的 Idea 演示行为 | 正式 agent 接口 |

## 值 × 读者

| 值 | 写入方 | 读者/规则 |
|---|---|---|
| id | ledger/agent | 卡片、选择、依赖；数据集内唯一 |
| rung.position / score | bundle adapter 或 agent | 图、badge、表格；position 连续，score 显式，2 个 Yes/No 或 5 个数值状态 |
| judgement.id / day / seq / rung / cited | ledger/adapter | as-of 与历史；按 day、seq、稳定 id 排序，引用必须存在，不能引用未来证据 |
| evidence.day / arrival_day | 来源/ledger | date 显示读 day，历史过滤与柱子读 arrival_day |
| switches.day / dependencies.day | ledger seq 的日期 | 状态与关系只使用截至所选日期已存在的记录 |
| dataset.as_of / days | host | 默认日期和重放边界；不读机器时钟 |
| URI | 来源 | 只把 http/https 做成链接，文本与属性转义 |

## 状态 × 事件

| 状态/事件 | 结果 |
|---|---|
| 有效数据 + mount/update | 验证后一次性替换数据；所有组件共用同一快照 |
| 无效数据 + update | 抛带路径的 ContractError；现有画面不被半份数据替换 |
| 有/无判断、未创建、已关闭 | 显式空状态；不捏造 score；状态取对应日期的开关 |
| 悬空关系目标 | 保留引用；只画已载入的目标，不猜目标内容 |
| 切换 Thesis 或数据 | 清理旧事件/动画，重置详情局部状态 |
| 展开/折叠中重复点击 | 从当前高度反向；销毁取消动画 |
| History hover/click/quiet day | 保留 D122 的选点规则；不读未来判断 |
| destroy 后的事件 | 无监听器、无动画继续写 DOM |
| 两个实例同时存在 | 各自根节点、id 前缀、数据和生命周期；互不查全局 DOM |

## 旧检查与新入口

现有 mock 与 API 均经过相同 adapter。对 42 个中英文 mock、完整 ledger bundle 和已存 `/ideas` 样本做离线回放；不调用模型。
测试覆盖：缺字段/未知字段、重复 id、错误日期、非法状态、错误引用、乱序输入、源数据不被修改、关闭/关系时间、早于首次判断、日期间隙、替换证据和危险链接。
组件使用真实浏览器验证，覆盖两种梯子、空判断、筛选、历史选择、展开反向和销毁。Python 原套件跑一次；`docs/check.py` 最后跑。

构建保留单文件 mock，源代码改用 ES modules。只引入开发构建所需的 esbuild 和 schema 校验器 Ajv；schema 在构建时编译成独立校验函数，浏览器不运行编译器。JS 产物预算 200 KB（不含数据与字体）；验证全部示例数据预算 200ms。记录实际值，不把预算写成结果。

ESLint 检查模块边界中的未声明变量和无用代码；Prettier 固定格式。它们只用于开发，不进入页面。

## 本轮验证结果

- `npm --prefix poc/ui test`：10 项通过；两种语言的 42 条 mock 记录，以及全部 94 条 live bundle 都经过同一合同。
- `npm --prefix poc/ui run test:mutations`：把未来判断当成当前判断、把发布日期当到达日期、提前应用关闭状态，三个改坏版本都被真实数据检查拒绝。
- `python3 -m pytest tests -q`：31 项通过，包含通过实际 HTTP 和 MCP 传输读取 bundle。
- 浏览器：两个实例无重复 DOM id，拒绝非法更新后仍显示原数据；销毁一个实例不影响另一个；空历史、两个梯子类型、重放、筛选、展开与历史选点均可用。
- 本机最终构建：JS 约 174 KB，42 个 Thesis 的数据验证约 23ms，均在预算内。`npm run lint` 和 `npm run format:check` 通过。
- 冻结的上游 PRD 不变。此次读数层只补齐 id 和时间，不改变分类、抽取、比对、重判或到期规则。
