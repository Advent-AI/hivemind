**这批结果不能证明 Luna 整体更好，也不能回答“Haiku 是否同样响应提示修改”。最明确的差异是 Cloud：Haiku 三答完整保留，Luna 只有第三答完整保留。**

已逐一核对全部 **57 份返回及对应输入、参考**：56 份完整，1 份截断，另有3次计划未发送。以下不使用关键词评分。

1. **NVIDIA：pilot 的“两个确定错误”判得过重。**  
   [D218](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2746)允许分析师推断，但不能冒充来源已确立的事实。

   | 回答 | 原句与判断 |
   |---|---|
   | Haiku control-1 | “Conditional reading… **could include** … financing exposure”：属于假设性分析，不能当成已发生的担保事实。[原答](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/nvidia-control-1-answer.json:44) |
   | Haiku control-2／3 | 均明确写“**Conditional interpretation**”，随后说“would also carry credit-support exposure”／“would make NVDA partly exposed”。提供方这个前提没有讲清，措辞偏强；应记**推断边界不清／uncertain**，不能直接记成确定的来源事实错误。[2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/nvidia-control-2-answer.json:44)、[3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/nvidia-control-3-answer.json:44) |
   | 旧 inference-check treatment-2 | 在条件分析之前直接写“**it is also taking on a credit-support role**”，limitations 又预设“credit support NVIDIA would provide”。这是把未确立的提供方写成既定角色，属于明确的来源事实越界。[原答](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-inference-check/nvidia-treatment-2-answer.json:44) |

   因此，[pilot-reading 的 definite 2→0](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/pilot-reading.json:26)不能支撑“稳定消除事实错误”。能成立的是：Luna 三答都没有把信用支持提供方指定为 NVIDIA。

2. **Cloud：遗漏和期间错误都成立，而且要分开记。**  
   输入的 `source_record` 已完整提供 **Q2收入248亿美元、增长82%、积压超5000亿美元**；全文明确写“**$81.6 billion (period ended April 2026)**”。[输入](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/cloud-reference.json:14)  
   Luna 第一答完全转向 NVIDIA 财务，并写成“**period ended July 2026**”，属于明确期间错误；第二答只泛称 Cloud 收入与积压增长，没有保留三个必要数值。它们都没有完整保留用户指定的**一个客户财务证据事项**，不是三个独立漏项。[第一答](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/cloud-treatment-1-answer.json:42)、[第二答](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/cloud-treatment-2-answer.json:42)

3. **谨慎表达不能自动算丢失研究价值。**  
   NN 六答都保留47台、全部预售、2026年8000万—9000万美元目标，也实际保留供应链用途。强调买方未知、目标未兑现，不能据此判无用。AMD 六答保留模拟比较及预测性质；Corning 六答保留规模展望与供应联系；Singapore 六答遵守排除要求。历史否认六答都保留公司回应与延期报道，没有把争议当成已经查清。这些目标上没有足够依据拉开模型优劣。

4. **“已签就必须新开金额题”不是完整的决策规则。**  
   [D201](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2587)仍要求独立投资判断及完整准入；[D210](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2670)规定已承担义务采用下次年报的金额题，不能替代前面的准入判断。[本轮设计](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/design.md:9)把 signed 必须开题写成了更强的案例预期。  
   Haiku 三答都读懂已签、1050亿美元上限及支付条件；`proposal=null`只能单列为未满足该动作预期，不能算事实理解失败。Luna 第一答问“是否有付款或确认负债”，也不是D210的义务金额题；第二答才问义务金额。[第一答提案](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/signed-treatment-1-answer.json:54)

5. **正文正确不代表关系标签正确，也不代表输出完整。**  
   例如 history_repeat 中，Haiku 前两答把与 e763 的关系写成 `revises`，但没有原主体后来修订同一主张的依据；Luna 前两答把 e719 写成 `different_origin`，输入也没有证明它与 WSJ 报道拥有独立取证。这些应单列关系错误。[Haiku例](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/history_repeat-control-1-answer.json:69)、[Luna例](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/history_repeat-treatment-1-answer.json:57)  
   existing_signed 三份完整回答均更新 v25。Haiku 第二次则在6000 token耗尽时没有正文，属于未完成，不能猜测其语义对错。[截断记录](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-model-capability/existing_signed-control-2-answer.json:17)

6. **这次测的是固定提示下的模型差异，不是修改提示后的响应能力。**  
   已核实10对请求的提示文本、来源输入与 schema 相同。但缺少“两模型各自修改前、修改后”的配对结果，所以无法据此说 Haiku 不听修改、Luna 更听修改，也不能把换模型的差异算成提示修改收益。