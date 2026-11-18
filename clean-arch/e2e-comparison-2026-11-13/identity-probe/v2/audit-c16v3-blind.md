**结论：这版不能算完全符合签署标准。** 分类例子大多有依据，但它把“和已开问题是不是同一题”的判断交给抽取步骤，而标准明确把这件事交给后面的匹配步骤。另一个风险是“另一个日历年”容易被读成拆题指令，尽管后文又说跨两年的比较只是一题。

例如，某原材料明年的均价与今年相比上涨多少，标准中的例子是一道关于明年的题；新文字先说“共同量的另一个日历年”可以是另一题，之后才给出这个例外。两句可以兼容，但模型需要先辨认出它是**一个变化**，不能仅凭出现了两个年份拆成两题。

我运行了两组 `diff`：系统提示词只增加了这组文字，结束检查只改了同题判断句。`c16` 和 `c8` 的 schema 相同。

### 逐句对照

| 改动 | 判定 | 标准依据与问题 |
|---|---|---|
| **“Same thesis or another, judged against the open theses and the other new theses”** | **contradicts** | 标准 §4 说：“抽取看不到库……这一条在抽取时只对同一篇文章里提出的几个问题判；和库里的比由匹配做。”同篇新问题之间的比较有依据；要求抽取判断已开问题则与步骤分工相反。 |
| **“The same thesis, when the same result settles both”**，包括其他措辞、来源、估计、方向、同一总量的其他人群或说法，以及同一计划按同一最终金额核对 | **consistent，限同篇候选之间的判断** | §4：“同一个结果能判掉两题，就是同一题”；“另一个估计、来源、措辞、方向”；“同一总量的另一种人群或代用口径”；“同一个计划的几种说法……最后核对的是同一个数，是一题。”拿它直接判库中问题，仍有上一行的步骤冲突。 |
| **“Evidence, not another thesis: a later deadline … while the thesis with the earlier deadline is open”** | **consistent，内容上；contradicts，步骤上** | §4：“早的那题开着时，晚的截止日是它的证据，不另开。”但同节标题和分工又说这是“匹配这一步的事，抽取不判库里的”。此句没有覆盖早题到期后仍追踪时的续期；那不是此句所述状态，不能据此说它否认续期。 |
| **“Another thesis … another calendar year of a shared quantity”** | **keeps wider** | §4 将“同一个量……的下一个期间”称为“续期”；§3 又说共同量“同一个量、同一年只有一个问题”。这些支持不同期间有不同身份，但不支持仅因换年就无条件另开。前置条件要求答案可分开、分别下注并通过其他测试，缩小了风险；但文字没有说明这是下一期间，也容易覆盖“同一题中用今年作比较基准”的情况。 |
| **“whether an unsigned single deal is signed, beside the amount of a programme it may join, when that deal alone could change the company’s cash or credit risk”** | **consistent**，但条件比标准举例更窄 | §4：“还没签的单笔交易是‘签不签’的是非题，照旧可以开，不并进计划的金额题。”§4 值得追测试要求规模能改变“收入、利润、现金或信用风险”；此句只举现金或信用风险，所以作为**例子**符合标准，但若被当作穷尽规则会 **keeps narrower**。它前面仍要求通过全部测试。 |
| **“One thesis although two years appear: a shared quantity’s change from this year to next is one thesis about next year”** | **consistent** | §3：“一个问题只问一个量的一个期间”，并直接举“2027 年 DRAM 合约价相对 2026 年的变化”。今年是比较基准，并不因此自动成为第二个问题。 |
| 结束检查改成 **“A new thesis that is the same thesis as an open thesis or another new thesis, by the rule in section 3, is not proposed: link its evidence to that thesis.”** | **contradicts** | 同篇候选去重符合 §4；但对于已开问题，标准说“和库里的比由匹配做”。新句在最终检查中再次要求抽取自行决定并不提出候选。它还把原先“同一基础问题、主体和范围”改成指向整组新规则，因此继承了上述换年歧义。 |

标准原文见 [§3 和 §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:271)；改动见 [系统提示词](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c16-system.txt:125)和[结束检查](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c16-closing.txt:14)。

### 1. 与请求中其他句子是否冲突

**没有发现这些例子之间必然的逻辑矛盾，但有会诱导误读的张力：**

- “同一总量的另一人群或说法是证据”和新句一致；“另一年”只有在确实问的是另一个期间的结果时才可能另算，不能把另一估计或另一口径误当成新问题。
- “另一个估计、来源或措辞不开题”和新句的同题段一致。风险来自模型将某个估计中的另一个年份当作独立预测，而忽略它只是同一问题的比较基准。
- “答案不能分开就关联证据”与新句的“答案能分开且分别下注”一致。但**能分开只是必要条件，不足以单独开题**；还要有独立投资意义、足够规模和可核对结果。
- “不要仅因相关期间排除证据”与另开下一期间的题不冲突：一条证据可以同时对两道不同期间的问题有用。风险是把“另一年是另一题”误读为“不同年份不得互相关联”。
- 结束检查说同题时把证据关联到该题；其他句子说关联到**每个**它能说明的问题。若将结束检查读成只关联那个同题，就会漏掉其他相关问题；结束检查同一段随后也要求关联每个相关问题，所以这是指令歧义。

### 2. 例子与行业、标准和 schema

例子跨银行、项目贷款、药品、工厂、航运、利率、零售、公用事业和原材料；**没有点名受覆盖公司、具体产品或数字**。其中月份和“今年／明年”是时间类别，并非具体公司数字。

例子作为原则可跨行业迁移，但并非每个例子都能直接套到任何行业：药品审批、项目担保等本身是行业场景。两个价格比较例子都属于商品价格，教学覆盖有重复。

从表达能力看，[c16 schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c16-schema.json)可以表示新问题、期间、开题理由、核对材料、与已开问题的差别，以及证据对已开或新问题的多重关联。它没有单独的“续期”字段，**所以不能仅凭 schema 证明后续会把下一期间正确处理为续期**。示例没有明确结果日期或核对材料时，也只是示意，实际开题仍须补齐标准要求；不能只靠示例判断已满足 schema 和开题条件。

### 3. 会不会误拆或误开

**会有风险，但仅凭文字审查不能断言模型实际会这样做。**

- **跨两年比较被拆开：**触发词是 **“Another thesis … another calendar year of a shared quantity”** 和例子里的 **“next year, beside this year’s”**。后面的 **“One thesis although two years appear”** 是纠偏，但它要求模型区分“两个分别追踪的年度结果”和“一个年度结果相对基准年的变化”。
- **小交易误开：**触发词是 **“whether an unsigned single deal is signed”**，尤其是 **“a programme it may join”**。文字已经加了 **“when that deal alone could change … cash or credit risk”** 和通过上方测试的条件，因此并非明文允许小交易开题；风险在于模型抓住“单笔未签交易可另开”，忽略规模和独立意义。
- **另一个估计误开：**最危险的词仍是 **“another calendar year”**。如果一个预测只是同一结果的另一估计，或只拿另一年作比较，标准要求作为证据；不能因为句中出现另一年就另开。新段自己的 **“another … estimate”** 同题规则和原请求的不开题规则都提供了相反约束。