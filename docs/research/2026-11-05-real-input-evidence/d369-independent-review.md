审阅结论：**两项决定的方向基本记对了，但有两处把你的话写得比原话更确定；新评价方式与冻结规则之间的关系也还没有说清。** 目前草稿明确标了未签字、不能打分；我没有发现指定文件声称这两项决定已经通过实际验收。

例如，你决定不必纠结“核心还是辅助”，并不等于你已经决定 Hugging Face 那条一定要留下。草稿现在把后者也写成了“已决定”。

1. **“已经开启新版评价”超出了原话能直接证明的范围。** [D369 原文记录](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3992)引用的是“往后……捕捉到就好，不用真的严格区分”，但同一条记录随后写成“明确开启新版评价”。你确实决定了今后的方向；原话没有直接提到开启哪个新版标准或金标。与此同时，[AGENTS.md](/Users/lchingen/hivemind-no-preseed-evidence-review/AGENTS.md:246)要求冻结材料不变，新版须由你决定、从头建立金标，并在审阅、签字前不能打分。应把“新版已开启”标为对你决定的解释，而不是逐字决定；在关系澄清并完成规定审阅前，不应拿草稿评分。

2. **Hugging Face 的“必须捕捉、已经决定”归因不足。** [预览](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/gold-preview.zh.md:22)以核心、辅助不再严格区分为理由，宣布该条必须保留；[草稿](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/draft-gold-reconciled-three.json:124)也写成“capture decided”。但 D369 没有点名这条，也没有决定它是否跨过“应留还是可选”的边界。它可以作为读者基于原文和标准提出的判断，但不能写成你已决定的具体案例。

3. **合并查看捕捉情况可以作为方案，但具体验收规则还没定。** 冻结标准原文分别报告核心和辅助，并列出不同的达标提案。[冻结标准](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:550) [设计](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/design.md:91)把它们写成一个“必须捕捉组”，这符合你不纠结两者边界的方向，但**单凭原话还不能推导出新的具体达标次数或通过条件**。设计目前也没有声称这些条件已经确定；这一点应继续保持。

4. **MXC 的案例结论记对了，通用表述要保留条件。** [D369](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3994)、[草稿](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/draft-gold-reconciled-three.json:306)和[主工作区审阅页](/Users/lchingen/hivemind/reports/2026-11-05-system-design-reader.html:2372)都写明保留 MXC 为辅助，并把可能带动 NVIDIA 需求标为推断。你说的是模型判断“相关且逻辑清晰”；因此，“间接联系也有价值”应始终带着这两个条件，不能读成任何看似连得上的间接联系都自动值得保留。

还有一个状态文字问题：[预览](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/gold-preview.zh.md:33)在“尚未决定”标题下第一项写“已决定”，容易让人误以为 MXC 仍待决定；实际草稿已正确标为保留。

本次只依据 D369 中保存的用户原话核对；指定材料中我没有找到这两句的独立原始对话记录。未修改文件、未发起付费调用，也未验证冻结文件的哈希。