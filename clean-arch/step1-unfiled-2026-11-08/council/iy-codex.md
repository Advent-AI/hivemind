1. **未关闭。** 请求现在要求 `ruled_out` “cover every way the event can be decided against, or formally abandoned or withdrawn”（[candidate-system.txt:13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)），但读者表只要求覆盖“the plain ways”（[stage-a-reader-brief.md:71](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:71)）。两者判法不同。手写例子也还把落空放进等待：**u1/clean-11** 的条件只写了禁止或拒绝申请，没有写全部申请被撤回；其标为第 2 档的例子又说“some withdrawn”，不能确定剩下的申请是否全部被拒。需要用明确的事实描述重验，而不是只看人工填写的档号。

2. **未关闭。** “each read as the position on the due day”和“stands cleared on the due day”（[candidate-system.txt:13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)）选择了到期时仍有效的含义，但原题也可能问**到期前是否曾发生**。批准后撤销，对后一种问题仍是“发生过”。旧示例的措辞可以解释新措辞的来源，不能证明 D409 授权把所有事件都改成到期日状态。代码的优先顺序仍会决定两个条件同时成立时的结果；称它为“tie-break”没有消除这个影响。

3. **部分关闭。** 我上次把“事实未知”直接等同于“不能使用该档”说得过宽：冻结的判断提示明确说“The rung is your forecast”，并说没有确认不等于事件没有发生。手写文件现在也说明是假定事实已知后人工放档。但 `Still open` 仍然是“前两档都不成立”的标签，并不总等于事件仍在等待；条件漏掉一种否决方式时尤其如此。改名没有修复这一点。

4. **部分关闭。** “a finer difference inside an outcome **that the topic’s wording names**”（[candidate-system.txt:13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)）解决了要求列出题目从未提及的细节的问题。设计也明确说不能丢掉追踪的结果。但请求仍把题目中任何“结果内的细分”一概列为不判；法国调查例子显示，“结论是什么”可能是原结果本身，不一定只是处罚结果的细节。需按原题判断，不能只按“细分”二字处理。

5. **已关闭原来的报告问题。** [脚本说明](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:1) 明确说“does not compute a rung from facts”，只打印作者的放档供质疑。它证明八份手写答案通过现有格式和代码检查；它本身不证明放档正确。

6. **已关闭。** 上轮举出的销售与披露混淆可以由 Q、R 或兜底的 W 抓到，不能称为表格所有项目都抓不到的错误；无需为该结论改文件。

7. **对第 1–5 条已关闭。** [collect_readings.py:266](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/collect_readings.py:266) 同时打印两种算法，并在结果不同时显示“depends on the unresolved points”。第 6 条仍分别打印两次，没有组合行；它由代码计算、并不依赖这些第三读者裁决。组合结论只打印，保存的报告仍是两份结果和未解决点。

8. **基本关闭，但与请求的范围仍不一致。** R 现在明确说：可以明显被否决却没有 `Ruled out` 档时，“the mark fails”；已有该档时要覆盖“the plain ways”（[stage-a-reader-brief.md:71](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:71)）。这抓到了明显遗漏，但不等于请求所写的“every way”，见第 1 条。

9. **部分关闭。** `Yes`、`No` 跟在完整问题后比原标签易读。但 `Still open` 仍可能给出错误印象：例如到期日前申请已经全部撤回，而否决条件漏写撤回时，代码仍会输出 `Still open`。下游只看到标签和理由时，这与真实状态冲突。

10. **已关闭。** “You write these two conditions and no other: what is left … needs no condition”（[candidate-system.txt:13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)）与 [schema](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:91) 的“No condition is written for what is left”一致，不再要求模型写第三个字段。

**请求全文仍有的问题：**

- “the event … has happened”与“each read as the position on the due day”没有区分历史发生与当日有效。例子“stands cleared”会教模型选择后者，甚至在原题只问是否曾获批时也是如此。这一统一选择在 D409 中没有明确来源。
- “every way”出现在正文、schema 描述和末尾检查中，共三次；读者表却使用较窄的“plain ways”。末尾复核有其用途，但三个位置需要表达同一范围。
- 正文要求模型写两个条件，同时允许 `ruled_out` 为 null；schema 接受 null，整体可理解，但“two conditions”宜写清第二个可以为空。
- 没发现请求仍要求模型输出退役的 `yes_no` 或五状态字段，也没发现合并例子要求 schema 或代码拒绝的字段。

**改写后的手写答案：**

- **acc/clean-2：** 原题问是否在期限前完成收购；“has completed”可以表达历史完成。第 2 档只列宣布终止、放弃或监管阻止，未覆盖例如交易协议到期而双方正式确认不再交易。原文没有给出完成日；这里不据此认定未来一定能在当天的指定文件中查到。
- **u1/clean-12：** 仍把“调查的结论及任何处罚”缩成“是否罚款或补救”（[脚本:40](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:40)）。现在把无处罚时的结论列入不判，比上轮透明，但原结果明确追踪结论；不能仅说它是无处罚内部的细节。
- **u2/clean-3：** 原题追踪允许或继续禁止；例子“the block goes on as before”被放入 `Still open`。若既有正式禁令仍有效，它符合第 2 档的“prohibition … stands”，所以人工放档至少缺少决定性事实。若只是没有新公告，也不能单凭沉默证明禁令仍有效。
- **u3/clean-12：** 原题问是否采取超出既有指引的新限制；手写题要求到期日限制“in force”（[脚本:59](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py:59)）。若新限制已实施、到期前又撤销，原题的“是否采取”与手写题会得到不同答案。这是到期状态替换发生事件的具体例子。
- **u3/clean-5：** 改回追踪实际销售，解决了上轮“只追踪披露”的改写。但“有禁令且仍在复核”被放第 2 档，例子没有给出第 2 档要求的“no such sale has been made”；此前已有销售时第 1 档成立。“no sale shown”也不等于没有销售，不能仅由此断定第 3 档。
- **u1/clean-3：** 首次发货是发生事件；“has taken place”保持了这一含义。宣布延迟且没有发货可落第 2 档；“no shipment shown”本身不证明没有发货，也不能单凭它断定第 3 档。
- **u1/clean-11：** 问题改成到期日是否**持有**批准，而原结果问是否**获得**批准；批准后撤销时两者不同。第 1 档却只说“have officially approved”，没有说批准仍有效，和问题本身也不一致。撤回申请的遗漏见第 1 条。
- **u3/clean-9：** 原结果包括结论、日期、认定和处罚；手写题只问罚款或补救。即使没有处罚，认定违法与未认定违法仍可能是原题的重要结果，不能直接当作同一处罚结果内无须判断的细节。

**尚不适合发送：先统一“曾发生”与“到期仍有效”的处理，统一请求和读者表的否决覆盖范围，再纠正上述手写案例并重新免费检查。**