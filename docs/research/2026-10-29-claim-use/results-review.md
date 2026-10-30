本组样本中，treatment 没有呈现整体改善；最明确的退步是三次都丢掉 Google Cloud 的客户需求线索，另一次丢掉可用的估值情景。比如，客户收入增长不能直接算成 NVIDIA 订单，但仍能帮助判断需求环境。

已审读 **source files＝7，graded＝42**。42 份均完成、无 errors。仅使用指定回答字段；未改文件、未调用模型。以下按整份回答的投资用途评分，不因标签或可选细节单独加减分。

| 评级 | Control | Treatment | 合计 |
|---|---:|---:|---:|
| useful_reliable（R） | 17 | 14 | 31 |
| useful_needs_review（N） | 4 | 3 | 7 |
| misleading_or_missed（M） | 0 | 4 | 4 |
| not_assessable（A） | 0 | 0 | 0 |

这是七个来源各重复三次的分布，不是 42 篇独立文章的成功率，也不据此设通过线。

| 来源 | Control：全部 ID 与评级 | Treatment：全部 ID 与评级 |
|---|---|---|
| nvidia | nvidia-control-1：R<br>nvidia-control-2：R<br>nvidia-control-3：N | nvidia-treatment-1：R<br>nvidia-treatment-2：R<br>nvidia-treatment-3：R |
| nn | nn-control-1：R<br>nn-control-2：R<br>nn-control-3：R | nn-treatment-1：R<br>nn-treatment-2：R<br>nn-treatment-3：R |
| signed | signed-control-1：R<br>signed-control-2：R<br>signed-control-3：R | signed-treatment-1：R<br>signed-treatment-2：R<br>signed-treatment-3：R |
| amd | amd-control-1：R<br>amd-control-2：R<br>amd-control-3：R | amd-treatment-1：R<br>amd-treatment-2：R<br>amd-treatment-3：R |
| cloud | cloud-control-1：R<br>cloud-control-2：R<br>cloud-control-3：R | cloud-treatment-1：M<br>cloud-treatment-2：M<br>cloud-treatment-3：M |
| valuation | valuation-control-1：N<br>valuation-control-2：N<br>valuation-control-3：N | valuation-treatment-1：M<br>valuation-treatment-2：N<br>valuation-treatment-3：N |
| singapore | singapore-control-1：R<br>singapore-control-2：R<br>singapore-control-3：R | singapore-treatment-1：N<br>singapore-treatment-2：R<br>singapore-treatment-3：R |

**估值和增长指标的实质问题：**

- **收入指标被错误说成不明：5/6 份 valuation 回答。** 原文先说 “further revenue growth ahead”，再给 82% 和 41%。control-1/2、treatment-1/2/3 却否认或悬置收入口径。尤其 [treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-claim-use/valuation-treatment-1-answer.json) 先承认 “it frames this as revenue growth”，随后又说 “does not state whether the growth refers to revenue”。财年、基期和预测日期确实值得查，但不能因此抹去已经明确的收入指标。control-3 认出了收入，却把期间明确写成 calendar 2026，超过原文确定程度。
- **估值情景被直接拒绝：valuation-treatment-1。** 它写道：“Reject for business research: this is a valuation and price-target call”。这是用途判断错误：**12.76 美元 EPS × 25 倍＝319 美元**，可以作为 FY2028 年末的条件情景，不需要成为公司承诺才有研究价值。treatment-2/3 保留了这条推导；treatment-3 进一步提出比较多种 EPS 路径和倍数，核查方向最好。control 三次也保留了推导，但没有明确交代 319 美元对应 FY2028 年末，使用时需要补回投资期限。没有发现乘法算错或把 319 美元保证为当前价值。
- **客户增长线索被稳定丢弃：cloud-treatment 三次。** [treatment-2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-claim-use/cloud-treatment-2-answer.json) 的理由是：“these are figures for Alphabet’s cloud division, not Nvidia revenue, orders, or demand”。前两项区别正确，最后因此否定研究用途不成立。248 亿美元收入、82% 同比增长、超过 5000 亿美元积压，提供客户经营增长和在手需求的不同信息。control 三次都保留了这些用途，同时没有转成 NVIDIA 订单。
- **收入增加被混成增速持续加快。** [cloud-treatment-3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-claim-use/cloud-treatment-3-answer.json) 写 “revenue momentum has been consistently accelerating”；treatment-1 也沿用了原文 “continuing the acceleration”。按所列数值计算，季度增速并不单调上升；最近一期约 **19.8%**，81.6→91 的下一季预测约 **11.5%**。这里支持继续增长，不支持持续加速。这是来源本身也有的问题，回答未识别；两份回答的主要降级理由仍是丢弃客户需求线索。

**其余案例的判断：**

- **NVIDIA 商业模式：treatment 有明确改善。** 三次都保留产品收入加云收入分成，并把信用风险写成待验证的条件推断。[control-3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-claim-use/nvidia-control-3-answer.json) 则从 “capacity it helps finance” 推到 “exposure to partners’ utilization and credit”，没有明确区分谁提供信用支持。利用率影响分成合理；NVIDIA 自身承担信用义务仍需查，所以评 N，而非整份编造。
- **NN、AMD：两组均稳定有用。** NN 六份都保留扩产、预售和业务目标，没有要求直接买方具名才允许使用，也没有转成 NVIDIA 订单。AMD 六份都保留厂商模拟、100kW 机柜口径和未来型号预测，没有升级成独立实测或普遍性能胜负。后续核查主要针对投产、合同约束、模型假设和客户实际采购标准。
- **已签担保：两组均可靠。** 六份都理解为已存在的有条件风险，正确区分 1050 亿美元初始上限、预期 2028 年服务条件和实际付款。control-3、treatment-2/3 尤其清楚地指出：OpenAI 的补偿承诺能否收回，仍取决于 OpenAI 自身信用。
- **新加坡：六份都遵守了本案排除要求。** [treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-claim-use/singapore-treatment-1-answer.json) 保留 DeepSeek 调查作为另一条监管线索是合理的；但把马来西亚机场查获案称为 “part of the same transshipment story”，并据此一并排除，缺少案件关联依据，评 N。其余回答没有展开其他案件，不因这一可选遗漏扣分。

提案问题单列：**42 份 proposal 均为 null，没有可评的提案错误**。来源自带的发表日与陈述日冲突未计入回答缺陷。