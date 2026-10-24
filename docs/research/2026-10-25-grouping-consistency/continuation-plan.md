# 归组一致性：允许细节不同，检查研究内容有没有跑偏

Alex 本轮要求继续检查归组一致性，不要求每次完全相同；Claude Code 正在处理 Idea 侧的一致性。本轮只研究 D147 的组归属。生产、Idea、UI、上层论点生成均不修改。

## 已有数据与原因

完整范围为 D147 retained 的 3 条流、每流 4 篇，共 12 份抽取原答，11 条最终观点、8 个组、14 条成员关系。Rubin 的出货、SK 工厂、SpaceX 卫星三个研究问题，每份都在同一组。原文证据位置和实际 evidence_links 已在 D147 复查。最终 1、4、3 组的差别是：三条额外的小组关系（SK 两条、卫星一条），和只在第二份抽到的两个其他问题（PC 芯片、OpenAI 部署）。不能把抽取覆盖差异当成拆组，也不能把多一个小组直接当成严重错误。

形成机制：抽取允许一条观点属于多个研究主题，现有写入保存该选择。三个小组各自只有一条成员，且这条成员仍在 Rubin 主组中。它们没有使核心连接丢失。因此不加“删小组”或“强制同一组数”的规则。后续要检验它们会不会吸走后来相关观点。

## 固定的两篇原文与判断

从 corpus 读取完整 text，不裁剪，不改文章标签和日期。两篇均未参与 D147 调试。

1. gnews:7ce0b7c3361fc5060098941f，2026-08-05，AMD 的 Lisa Su 访谈及业绩报道。提到 SpaceX/NVIDIA，但 AMD 自己的服务器收入增长观点不属于 Rubin 推出和采用。若未抽到这种观点，记“没有可判断的负例”，不能记作正确隔离。该文作为晚到材料在 seq 5 进入。
2. nvblog:google-cloud-vera-rubin-infrastructure，2026-10-21，Google Cloud A5X/Vera Rubin 公告。原文说 next month 将一般可用，该新部署问题应与原出货、SK、SpaceX 同属 Rubin；它仍是独立问题，不等于 NVIDIA 开始出货。作为 seq 6 进入。

这两个判断是 assistant 根据原文作出的语义检查，非人工金标。它们沿用已确认的“同产品不同客户应能同组；不能只因同公司/同产业就混入”含义。本轮是描述性边界探测，不引入一个自行设置的总体及格百分比，也不以它替换 Claude 的封存金标。

检查每份：原三个问题之间的连接是否保留；新增 Google 部署有没有到该组；AMD 自己的收入问题有没有混入；拒绝/漏抽/错合观点/错分组分别计数；全部额外组及其成员逐条列出。用证据原文、candidate id → binding → view id 和真实成员关系核对，不按跨样本 g1/v1 编号相等或标题关键词打分。名字、编号和额外细组数量本身不扣分。每份都报告，不能只报告平均数。

## 运行与预算

不改 D147 prompt/schema/process。复制三个 completed retained views.sqlite，使用 SQLite backup 读出一致副本，不复制模型缓存。每份只顺序处理这两篇；这是三个既有不同状态的 fresh continuation，不是三份全新从空库的重复。没有对照臂或改善效果的声称；它测量当前方法，不比较方法。每篇最多抽取、匹配、必要时二次证据比对三个调用：总上限 18 次，费用估算上限 $2。新目录单独记本次请求；D147 的 47 次/$0.641424 原预算和记录不动、不再续跑。模型与 provider、设置沿用 D147。

准备后封存两篇、三份起点、运行代码/依赖/config/universe 的校验和；每次启动和每篇前核对。每个流遇到拒绝或未知调用结果即停止该流，保存原因，不补样本、不偷偷重试、不自动改变提示词。超预算全停。失败的下一方案需先报告，不在本轮自行加臂。付费前跑 preflight 并与 D147 分布比对，另外从空临时库重放三条原始流，逐字核对请求，确保当前代码仍重现起点。调用串行；检查机器和提供方 DNS；detach 并记录 pid/log。

## 状态 × 事件

| 状态/事件 | 行为、写入、日期 |
|---|---|
| 准备前 | 验证源文件和两篇完整原文；只读来源；新建独立输出目录，记录 hashes。 |
| 准备后/正常调用 | seq 由 dispatch 延续到 5/6；publication_day 保留原文；原 process 原子提交。 |
| 拒绝、再遇失败、服务失败/未知结果 | 回滚该篇，保存 failed；该流不再发请求，其余流保留自己的结果；未知结果仍占预算。 |
| 写入中断/重启 | 已提交篇按 dispatch 跳过；未提交篇允许同一 request 原答重放，未知 HTTP 不重送；请求不同拒绝。 |
| 提交后、结果文件写入前中断 | ingestion_events 已同事务保存结果；从其 result_json 恢复该篇报告。 |
| 运行结束仍在等待 | 不宣布完成，不启动另一份相同流；最多180秒请求超时由既有 transport 管理。 |
| 日后续跑/配置变化/原文修正 | 日期不取系统时间；核对 hashes，不符拒绝，需新独立实验。 |
| 同时另一写入者/两范围 | 单输出目录 flock；三份私有库；源只读；不改正式库。 |
| 完成/重送 | 两篇重送应 skipped；as-of 4 的组与证据必须逐字段相同。 |

## 值 × 来源、写者、读者

| 值 | 来源/写者 | 所有读者 |
|---|---|---|
| 起点副本 | 只读 retained SQLite backup | 原 dispatch/extraction/matching/writing/threads；记录起点组和历史检查 |
| 两篇 items | 原 corpus 全文、JSON object_identifiers | 原 process；检查证据位置 |
| 模型原答 | 原 Calls，fresh 本次缓存 | 原 validate/sift/matching/write；人工逐条分析 |
| 组/成员/观点/证据 | D147 原 process 唯一写入者 | 原 thread_detail；本轮只读报告；Idea/UI 不读这些实验文件 |
| manifest/budget/failed/events | 本轮准备与驱动、原 Calls | 重启核对、预算拒绝、结果复查 |
| 报告 | 核对真实引用路径的脚本与人工语义读审 | Alex；交接给 Claude 的边界说明 |

## 新路径 × 旧检查

没有新生产数据形状。调用 D147 原 extraction_schema、validate_extraction、sift、matching.check（含二次比对）、writing、write_threads、dispatch。实验驱动只负责隔离、预算上限更小、哈希、停止/恢复。先在三份旧原答上逐请求重放；源文件不变；破坏一条核心成员的临时副本必须被测量发现。没有相关观点时结果是未测到，不能通过。历史比较使用 seq 4 的完整 thread_detail，不比较文件字节。

## 先前决定

D142: “no separate full-library clustering pass”。D143: “Matching resolves thesis identity without rewriting group membership”。D144: “A subject can start with one thesis”。D147: “no production adoption”; “overall group counts (1, 4, 3), large-library recall, cross-company boundaries ... remain unvalidated”。全部保留。没有新聚类模型、隐藏的去重、额外总结调用或组数目标。

## 与 Claude 的合并边界

Claude 负责同一 Idea 如何拆解、搜索、选 direct/driver/context（D145/146）。本轮负责入库时哪些独立观点共属一个研究主题。两边未来通过真实 view_id 对接：先看该 Idea 必须看到的观点是否存在，再看搜索是否找到，再看选择和归组。不能把缺失观点算成分组错误，也不能把同组自动当成支持/因果，更不能把组当成数值判断的替代。先各自给出原始证据路径与误差分类，合并时再跑同一 Idea 的端到端用例。
