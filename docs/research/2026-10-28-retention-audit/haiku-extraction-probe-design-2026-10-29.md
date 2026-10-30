# Haiku 5.5 单篇抽取对照：试验前约定

2026-10-29。Alex 要求试用 Haiku 5.5。只测上次原始文章 `gnews:71df54965281684cc500960f` 的 v38 抽取步骤，不跑全流程，不改变默认模型。固定两项预先确定的事实、原文章和评判方式，沿用 [DeepSeek 抽取实验](deepseek-extraction-probe-design-2026-10-29.md)；2028 EPS 可以保留，权重待定，不计错。

三次全新现有 `gpt-6-luna` 对照和三次 `claude-haiku-5-5`，每次独立发送，不缓存重放。逐字相同的 system、user、原始 schema 和 8,000 输出上限；GPT 请求由生产构造并与 v38 历史摘要 `99dc1c7e9f97d09ba8f9480db32e267c0f57465051f50cccf2e7e190af507007` 验证一致，序列化顺序照生产；Haiku 采用 Anthropic Messages 的 `output_config.format` 表达相同 schema、`system` 对应系统消息、`messages` 对应用户消息、低思考力度。两家协议和思考力度不完全相同，不可将差异全归于模型；如 API 不接受 schema 就记录拒绝，不改变 schema、不重试。

每次先记完成、超额截断或接口错误。完整且通过生产 schema 的回答进入 v38 原生 sift；按逐条筛选后保留的内容人工核对两项事实为完整、部分或未写，不因为一条其他内容被剔除而排除整份回答；记录原始回答和每条剔除理由。核对：两年的云厂商支出预测是否完整；82%／41% 是否明确为收入、分别属于哪个期间以及谁的预测。拆成多条也可合计；引句要与原文一致，摘要不可引入原文没有的事实。保留全部原始答复和输出记录；无完整答复不计对错。只报告这一篇开发案例，不声称全周效果或改变产品。

先用 `scripts/preflight.py` 显式指定 `--archive /Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite --items /Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite --views /Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/views.sqlite`，核对 98 篇、841 条、筛后 831 条及拒绝理由；一个账本历史状态误报及 4 个未匹配请求单列，不把退出成功当成所有判断正确。检查本机和 Anthropic 模型列表，使用钥匙串读取密钥，不写代码、记录或命令行。网络不可用、无密钥或账户无模型权限则停止。独立只读审阅方案后才写试验代码。先发一个 Haiku 样本：schema 被拒绝则停止且不发其他样本，不改 schema；接口接受后，再并发其余 2 个 Haiku 和 3 个 GPT（最多 8）。第一个有效或截断样本均保留，不重试。如果之后有费用异常或接口拒绝，未发的请求停止，已在途的仍保留并核算；不重发截断或失败。运行独立会话，保留 pid 和 log。

费用：根据 [Anthropic Haiku 5.5 标准价格](https://platform.claude.com/docs/en/models/haiku-5-5/overview) 输入 $0.10/M、输出 $0.50/M，输入大于 100k 时 $0.50/M、输出 $2.50/M；GPT 用同上两个标准价。保守估计每次输入上限取请求的 UTF-8 字节数三倍加 16,384、输出按 8,064 计，每家 3 次；如输入超过 100k 则 Haiku 按高档计价。合计超过 $0.60 停止；未知 usage 按该次全额预留报告，超出预留则报告异常并停止后续重发。此预留不是平台保证的硬上限。

Anthropic 的结构化输出会自动增加系统说明，输入 token 也可能增加；虽然显式发送的 system、user、schema 一致，实际全部模型输入未必相同。见 [Anthropic 说明](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
