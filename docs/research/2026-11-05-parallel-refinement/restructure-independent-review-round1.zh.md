**结论：两份草稿还不能算完成了重构，也不适合据此启动测量。** 它们加入了研究判断的说明，但保留了原有的大段规则；其中 A 对新问题的限制比签署标准更窄。比如，一个会独立影响药企价值的三期试验结果，标准允许与获批分别追踪，草稿却只写产品上市或开始出货。

以下是审查中发现的严重问题。两份草稿都只是 system 文字；对完整请求的判断，以下以草稿替换对应已存请求的 system、其余内容沿用为前提。

1. **审查文档把四类开题理由说成“实验暂行约束”，这不准确。** [审查文档]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructure-audit.zh.md:15)说“保留既有分类作实验暂行约束；四类是不是过窄单独标记”。但[签署标准第 3 节]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:271)明确说开题理由是封闭的：**四个开题理由展开成五种问题类型**。因此，不能说“四类限制是草稿额外加上的，也不能把是否需要封闭分类当作已解决的问题”。真正要查的是草稿对各类的描述是否完整、是否符合标准。

2. **A 把签署标准允许的问题排除在四类之外。** [A 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-new-thesis-draft.txt:26)规定主产品问题只能问该代产品“**launches or starts shipping**”。但[标准]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:345)明确举例：新药三期数据和获批，如果分析员会分别下注，可以分别开题。草稿没有给三期数据一个清楚的开题位置。

   同一段还把约束性义务中的投资写成“**an equity stake whose size is stated and is not yet completed**”。[标准第 3 节]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:278)包括“写明规模、尚未完成的入股**或收购**”。一笔规模足够大、尚未完成的收购，未必是股权入股；草稿没有明确覆盖它。

   另外，草稿把共同量写成“**one aggregate quantity for one calendar year**”。标准明确包括共同价格和利率，例如油价和利率上限。英文的 *aggregate quantity* 是否会被模型理解为包括这些价格和利率，不清楚；至少这比标准的描述更容易被读窄。旧请求本就有这些限制，草稿没有修复它们。对应来源见[A 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-new-thesis-draft.txt:26)和[标准第 3 节]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:279)。

3. **A、B 的分工可能让有价值的材料没有去处。** A 规定“**If there is no candidate, return no candidate-linked evidence**”；B 只找能回答已有问题的材料。于是，一条财务事实可能对投资研究有用，却既不足以单独开题，也无法清楚连接到当时已有问题：A 不返回它，B 也不要求收下它。[A 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-new-thesis-draft.txt:11)；[B 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-existing-evidence-draft.txt:1)。

   这与 [D371]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:4006)要求追踪相关的当期和未来财务信息之间有未解决的覆盖问题。D371 **并没有**要求每个财务数字都开题，也没有规定无关联已有问题的材料应如何保存。因此，这是从两份请求推导出的缺口，不能据此断言某条实际材料一定被丢失或已经找到修法。

4. **“解释关联”是新增要求，但完整请求没有明确的解释位置。** 两份草稿都新增“**Explain that connection from the supplied material and the question**”，并要求把原文与分析员推断分开。[A 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-new-thesis-draft.txt:4)；[B 草稿]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-existing-evidence-draft.txt:4)。

   可是，两份已存请求的输出格式都没有单独的关联解释字段：摘要要求独立复述原文，链接则是问题 ID。[A 格式]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-thesis-evidence-poc/frozen-requests.json:5467)；[B 格式]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/b-arm-frozen-v2.json:237)。如果这句话只要求模型在内部判断，就不必新增输出；如果要求写出来，放在哪里、如何避免把推断写成来源事实，都没说清。[D369]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3994)允许逻辑清楚的间接关联，但不授权新设强制输出字段。

5. **A 的最后一句仍可能让人以为只能返回证据。** 已存 A 请求先说“**Return candidates, their article evidence, and any new groups**”，最后又说“**Return only the evidence items you keep**”；格式则要求三个顶层部分。[已存 A 请求]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-thesis-evidence-poc/frozen-requests.json:5395)。

   前后文可以把最后一句理解为只筛选证据，所以我不能断言它必然互相矛盾或已经导致漏题。但[审查文档]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructure-audit.zh.md:18)说 A 的末句已明确“只筛证据但仍返回候选及组”，而交付的草稿只包含 system 文字，没有展示修改后的 user 末句。如果沿用已存请求，这个歧义仍在。

**关于是否真正重构：有少量重排，但主体是增补。** 对照已存 system 文字，A 从 12,309 增至 13,210 字符，增加 **901**；B 从 5,814 增至 6,321 字符，增加 **507**。两者都保留了原有的证据类别、例子和写法说明；A 也保留了整段原开题限制。新增的研究判断、独立问题测试和标题让顺序更清楚，但没有看到相应的大段合并或删减，也没有在审查文档中看到字符数、提示词 token 数和增长理由。[AGENTS §6]( /Users/lchingen/hivemind-no-preseed-evidence-review/AGENTS.md:210)要求这些信息。这里的字符数仅比较 system 文字，**不是完整请求的 token 数**。

逐项对照新增文字后，以下内容有依据，不能一概当作新规则：区分原文和推断、保留来源与条件、不得编造未给出的市场预期、间接关联不能只因没有量化而丢弃、相关季度事实可以支持年度问题，以及支持和反对材料都要考虑；这些分别有[标准 §4–5]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:308)、[D369 和 D371]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3990)支撑。A 新增的四个问题测试总体上也对应标准，但它们**不能覆盖或抵消**后面更窄的硬限制。

本次没有改文件、发产品模型请求或评分。以上是对文字和请求格式的审查，不是模型效果结论。**现有三处开题金标争议仍未解决**；D372 对证据计数的决定没有解决它们，也没有改变冻结文件或历史分数。[D372]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:4012)

