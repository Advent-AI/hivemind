NOT READY

例如，文章写预计收入为 2.5 quintillion 美元时，请求允许不填写这个无法表示的数字，但阅读表仍要求中间档覆盖它。一个符合请求的答案因此会被判错。

1. **超出数字范围的预期仍会被误判。** [请求](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:16)允许保留原文、将数值设为 null，并自行估计各档；[阅读表的 X](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:63)和[设计](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:867)却仍要求中间档覆盖文章中的数字。2.5 quintillion 超过档位边界允许的最大值，中间档无法覆盖它；即使 XR 正确地通过，X 仍会失败，结果被算作错误。完整修复应同步阅读表的规则、X 和设计，明确只有可表示且填写的预期数字才要求落在中间档，并用可表示和不可表示的正确、错误例子验证。

2. **已签约义务的到期日可以选错而通过。** [请求](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:23)要求已承担的义务使用下一次年度申报日；[设计的检查 5](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:389)只检查是否在 548 天内，[D](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:62)也未检查是否为下一次年度申报日。比如材料同时给出义务评估日和之后的下一次申报日，模型选了前者且不超过 548 天，D 和代码检查都可能通过。完整修复应明确由哪个判断核对已签约和未签约两种情况，并用各自正确、错误的日期验证。

3. **上一轮中性比较的修复尚无对应的表单验证。** 新表单将有预期和无预期时的比较对象都放进了 [F](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:64)，方向是对的。但设计引用的 [第十次阅读](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:934)使用的是修改前的表单：存档中两位读者对有预期的植入错误给的是 X 失败、F 通过，而不是按新表单给 F 失败。当前证据因此不能证明新 F 能抓住错误，尤其是文章没有预期时。完整修复需要用当前表单，对有、无预期两种情况各读正确和错误例子，并报告结果。

上一轮其余发现已有针对性修改：问题措辞、条件可核实、日期依据和方向理由都有了明确判断；不完整阅读的 G 和 B 计数也已定义。六条线的空样本和最低数量有规定；第六条只检查三次是否一致，一致本身不能证明答案正确。设计明确要求每份 Stage A 报告说明它不比较生产，符合 D400。

文字层面：[表单的包内容说明](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:18)列了方向，但漏写 F 需要读取的 `favourable_why`；设计的数据表包含它，表单应同步列出。

已逐条走完本角度的六条线、计数和分母、表单与请求的对应关系及 D400 限制；没有未读的本角度条目。