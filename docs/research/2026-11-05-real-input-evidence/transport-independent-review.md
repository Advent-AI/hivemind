沿用生产的 `model.call` 和 `openai_transport` 适合这次真实新闻 A/B；但在付费实验前，还有两处需要澄清。

例如，一次请求可能先超时、实际上已被服务商处理，随后重试成功。最终拿到的那份回答有 token 用量，**不代表前一次尝试没有产生费用**。

1. **费用记录还不完整。** [model.py](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/model.py:128) 在内部重试，但不会向调用方返回每次 HTTP 尝试的记录；即使最后成功，之前的费用仍可能未知。此外，回答格式无法解析时，归档把 token 和费用记为零，即使原始响应可能带有用量。方案应明确：成功回答的用量只是已知部分，未知重试费用单独标明；从可用的原始响应读取用量，按 §7.2 指定的费率计算，不能直接把归档里的零当作实际零成本。[design.md](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/design.md:88)

2. **串行安排与 §9 有矛盾。** 方案写实验串行运行，[AGENTS.md §9](/Users/lchingen/hivemind-no-preseed-evidence-review/AGENTS.md:396) 则要求实验调用并发。各组已有独立存档和独立研究库，可以按这条要求安排，同时保留同一篇文章、同一起始状态的配对比较。[design.md](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/design.md:72)

另外，最后一段的“重试最多三次”应改成**最多尝试三次，包括首次发送**；代码也会对部分 HTTP 错误重试。当前输入方案要求两组只差财报块、引文只对新闻验证，并检查财报事实是否被误写成新闻；在本次范围内，我没有发现另一个严重的输入矛盾。方案仍需按文中要求完成免费预检、输入核实和金标确认后，才能用于付费比较。

本次仅做只读审查；没有改文件，也没有发起付费调用。