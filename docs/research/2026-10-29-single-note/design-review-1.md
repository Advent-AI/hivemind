当前版本有两处严重缺口，建议先补齐再实现实验脚本。例如，新案例只有 `incoming`，却允许引用不存在的 `item:e4`。

1. **新 8-K 案例的编号范围错误。** [signed-treatment-request.json:82](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-single-note/signed-treatment-request.json:82) 仍允许 `item:e2/e3/e4`。我用现有 `model.check_schema` 验证，虚构引用确实通过。应从该请求实际记录生成枚举；此例只能引用 `incoming`。九份处理请求中，仅这一份发现编号范围不符。

2. **取消 G10 后，没有必须更新完整旧论点的正例。** [design.md:21](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-single-note/design.md:21) 换成空目录案例，只能检验新提案；剩余两个历史案例都允许不更新。因此始终输出空 `updates`，也可能通过，无法证明保住 D201。应保留 G10，或配置同样必须更新旧论点的固定正例。

已读原 G10 完整请求及 71 条历史；原参考有据：e1205/e1206 支持已签约和初始付款上限，不支持已经付款。NVIDIA、NN 续问及 D222 原始失败也已核对。指定两份请求的完整 schema 与现有校验器兼容；空域省略、编号枚举及逐比较 `unknown` 未发现严重问题。

审查期间文件被并发修改；以上针对修改后的版本。我未编辑文件，未调用网络或模型。