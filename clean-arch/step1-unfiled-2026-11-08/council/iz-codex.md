**仍未关闭：新增句子把“是否被否决”交给后续判断，却没有保证它指的是整个问题。** 例如，撤回一个进口申请，不代表所有中国公司都不能获批。

1. **遗漏的否决方式、表格范围和 `Still open`（上轮 1、3、8、9）：部分关闭。** 请求不再要求模型列出“every way”；[读者表的 R](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:74) 也明确说不必全部列出，并在明显可以被否决却没有该档时判失败。两者的范围现在一致。

   但 [ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:255) 写入的是“the event of rung 1 has otherwise been decided against, or formally abandoned or withdrawn”。这是一句需要理解和判断的话，代码没有识别哪些申请属于整个事件，也没有判断所有可能的申请是否已经结束。因此 [DESIGN.md:430](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:430) 所说“代码接住其他方式”尚未得到证明。

   [u1/clean-11](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:88) 问任何中国公司是否获批。假设一家公司撤回申请，另一家公司仍在等待：第一档不成立；第二档新增句子可能被读成“申请已撤回”，也可能被读成“整个获批事件未被放弃”。正确结果应是仍在等待。八份手写结果都是作者指定档号，不能证明后续读者会选择正确解释。

2. **发生与仍然有效（上轮 2）：关闭了统一改写状态的问题；优先顺序仍是未确认的选择。** 请求恢复了“has happened by the due day”（[candidate-system.txt:13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)）；`u3/clean-12` 也改回问是否采取限制。对于“曾发生”问题，发生后撤销仍算发生，是连贯的读法。

   当两种条件同时成立时，代码仍让第一档优先。[设计](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:438) 如实标明这一解释已报告、尚未得到 Alex 确认。它不再冒充已确认的决定。

3. **可不判的内容（上轮 4）：部分关闭。** 设计现在明确承认：“three outcomes cannot carry everything a thesis may track”，并说其余内容列出（[DESIGN.md:447](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:447)）。法国案例也列出了调查认定。这比上轮准确。

   但 D397 的规则是判 `outcome` 指出的主要事项；若没有主要事项则不出题。它没有说当结果同时包含结论和处罚时，可以不说明依据地任意选择一个。[u1/clean-12](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:41) 只说“one question can track one of them”，没有说明为何处罚是该原题的主要事项。D409 中呈给 Alex 的几种结局选项及反对意见，不等于他确认了这个具体选择。

4. **新增第二档句子的效果。** 若把第一档、模型写的否决条件和新增句子都当作确定的真假命题，并把最后一句“only when rung 1 does not”应用于整个第二档，那么形式上没有重叠或空档。实际展示给判断程序的是自然语言，这个形式结论不保证它会正确理解事件范围。

   - **可能拉进别的事情：** 上述一家撤回、另一家等待的例子；撤回的是一个申请，问题问的是任何公司获批。
   - **可能把仍可发生的事判为落空：** [u3/clean-12](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:61) 把“所有现有提案撤回”放入第 2 档。但在到期日前判断时，政府仍可能提出另一项限制；撤回现有提案不必然是放弃采取任何限制。手写假设没有排除这种情况。
   - **不适用的动词：** “事件被正式撤回或放弃”对申请、交易容易理解，对首次发货、销售等事件则需要判断是谁放弃了什么。句子可读，但不能据此保证对每类事件都有明确含义。
   - **模型条件本身仍可过宽：** [u3/clean-5](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:71) 将到期前任何时候的购买禁令写成第 2 档。如果禁令后来解除、销售仍可能发生，它不一定是明确落空。新增通用句不能修正模型原句。

5. **请求全文。** 事件的发生、否决和可否为 null 在正文、schema 和末尾复核中各出现一次；这是三处重复，末尾用于复核。三处现在没有“every way”与“plain ways”的冲突。仍有一处实质张力：正文先说条件不得重叠，合并示例却允许先批准、后阻止都满足各自文字；代码靠第一档优先消除最终重叠，但模型看不到这条优先规则。

**尚不适合小规模发送：先用多个申请、撤回后仍可继续、以及禁令解除的完整事实例子，验证新增句子能否让独立读者一致区分“整个事件落空”和“仍在等待”，并为法国案例说明主要事项的选择依据。**