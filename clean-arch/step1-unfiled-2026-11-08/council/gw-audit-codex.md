**这份请求还不能通过审计：两个事件例子有答案遗漏或重叠，六个例子带入了英伟达或测试材料，而且部分请求允许的答案会被代码拒绝。** 例如，出口限制例子中，“除豁免名单外全部国家”既可能符合“指定国家名单”，也符合“全部国家”。

以下按请求逐项列出。`S` 表示系统文本中的句子，按出现顺序编号；行号链接指向被审计的文件。判断依据中 `v` 表示冻结提示词的行号，`D` 表示决策编号。对长句中的不同规则分别判断。

### 1. 请求对照标准

| 句子或描述 | 来源 | 判断 |
|---|---|---|
| S1–3 角色、写一个问题、固定 | [系统 1]( /Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:1)；v1、D38 | 一致 |
| S4–5 一个数字或事件、到期可判断 | [系统 4](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:4)；v20–21 | 一致 |
| S6–8 按 outcome 选主要部分 | [系统 5](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:5)；D397 | **更窄**：D397 要列出措辞中*所有其他部分*，这里限定为其他数字或事件。 |
| S9 五种不写情形 | [系统 6](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:6)；D397、D38、v13、16–17 | **更窄**：D397 的“没有主要部分”不限于 outcome 同时列出多个数字或事件。 |
| S10–12 公司、其他公司、主题归属 | [系统 9](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:9)；v22、`build_prompt` | 一致 |
| S13–15 具体条件、不能依赖未来目标、不重叠无遗漏 | [系统 12](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:12)；v24–25、D38 | 一致 |
| S16–18 二选一、五个事件状态及标签 | [系统 13](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:13)；v25、D38 | **有缺口**：三个或四个自然结果如何分成五个互斥状态没有规则或例子；不能因此假定它们不存在。 |
| S19–22 数字单位、年份、五区间、边界与数值格式 | [系统 14](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:14)；v25–26、34–35、`CLOSING` | 一致 |
| S23 三种形状选一种 | [系统 15](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:15)；v25 | 一致 |
| S24–26 预期、居中、无预期时估计 | [系统 16](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:16)；D260、D398 | 一致 |
| S27–29 有利方向及原因 | [系统 17](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:17)；D186、D398 | 一致 |
| S30–31 到期及发布日期 | [系统 20](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:20)；D356、v26 | 一致 |
| S32–33 数字发布日期、财政年和自然年 | [系统 21](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:21)；v26、33 | 一致 |
| S34 事件日期 | [系统 22](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:22)；v16、26 | 一致 |
| S35 义务的 18 个月及核对日 | [系统 23](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:23)；D185、v13 | 一致 |
| S36–40 最后检查及修正 | [系统 25](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:25)；AGENTS §6 | **部分新增**：要求参考值“落在”中间区间，上文只说“接近”；D398 支持该规则，但它没有明确写在最后检查之前。 |

**Schema 描述**

| 描述 | 来源 | 判断 |
|---|---|---|
| `no_ladder` | [19](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:19)；D397、D38、v13、16–17 | **更窄**：同 S9。 |
| `question` | [44](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:44)；v20–21 | 一致 |
| `object` | [49](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:49)；v22、`build_prompt` | 一致 |
| `not_judged` | [53](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:53)；D397 | **更窄**：同 S6–8。 |
| `yes_no`、`yes`、`no` | [74、90、95](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:74)；v25 | 一致 |
| `states`、`label` | [102、122](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:102)；v25、D38 | 一致；但有上面 S16–18 的覆盖缺口。 |
| `figure`、`unit`、`year`、`lo`、`hi` | [134、162、167、190、201](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:134)；v26、34–35、`CLOSING` | 一致 |
| `favourable_end`、`favourable_why` | [213、217](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:213)；D186、D398 | 一致 |
| `reference.words`、`reference.value` | [239、250](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:239)；D260、D398 | 一致 |
| `due_day_basis` | [267](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:267)；v16、26 | 一致 |

**八个例子**

| 例子 | 来源与判断 |
|---|---|
| 发货 | [12–17](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:12)：**违反通用性**；而且“没有确认”不等于“没有发生”，无可靠信息时不能当作 No，见 D185。 |
| 担保 | [60–70](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:60)：**违反通用性**；同样把“没有确认”当作 No。 |
| 法国调查 | [111–140](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:111)：**违反通用性、有遗漏**；“接近结论”也未必是计划或期限。 |
| 出口限制 | [193–221](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:193)：**违反通用性、有重叠和遗漏**。 |
| 公司采购承诺 | [277–308](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:277)：**违反通用性**；数值区间本身连续。 |
| 行业资本开支 | [361–396](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:361)：**违反通用性**；数值区间本身连续，参考值在中间。 |
| 没有主要部分 | [439–447](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:439)：D397；一致，但原题未随例子给出，无法独立核实判断。 |
| 虚构零售商 | [454–502](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:454)：D398；区间一致，但占位 ticker 和未提供原文使对象、引用检查无法验证。 |

### 2. 标准对照请求

- **已覆盖：**固定问题和到期日、一个数字或事件、五档或事件二选一、区间格式、公司与主题归属、财政年、当前／下一年、18 个月义务、发布日期、参考预期、有利方向及无参考时估计。来源分别为 D38、D185、D186、D260、D356、D398 和 v13、16–17、20–26、32–35。
- **覆盖更窄：**D397 要显示所有未判部分及无主要部分时的理由；请求只列其他数字或事件，并把无主要部分写成特定的多项情形。见[系统 5–6](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:5)。
- **缺失：**D38 要写清数字由哪个来源回答，以及是期间总量还是时点值；请求提供 `settled_by`，但没有要求问题或答案明确保留这些信息。[D38](/Users/lchingen/hivemind/docs/DECISIONS-log.md:761)
- **缺失：**D185 的无可靠材料时“无法验证”没有体现在二选一例子中；例子把未确认视为 No。[D185](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2472)

### 3. 原则与检查

- 法国调查：无侵权且接受承诺但同时有罚款、或其他程序性决定，可能没有对应状态。五个条件之间未见必然重叠，但“宣布过程序性决定、最终仍待定”也可能落空。[例子 118–134](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:118)
- 出口限制：对一个有豁免名单的国家集合生效，可同时满足第 4、5 档；对部分国家实施禁令则可能两档都不满足。[例子 205–221](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:205)
- 两个二选一例子中，已确认发生与未确认发生形式上互补，但后者包含“实际发生、尚无证据”，会误判。见上表。
- 请求允许其他公司 ticker 或未列主题名称；[检查 2](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:228)会直接不写问题。请求没有告知这一结果。
- 请求允许主题状态使用简短名称，却未要求名称互不相同；[检查 3](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:240)会拒绝重复名称。请求也未说明数字边界必须有限且整数绝对值小于 2^53；[检查 7](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:274)会拒绝超出者。
- 参考值必须落在中间区间这一最后检查，应先在上文明确。仅抽查低、中、高三个数字也不能证明所有区间没有空隙或重叠。[系统 25](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:25)

### 4. 与作者表的分歧

作者表没有逐行写“判断”，以下是与其来源映射或表述的实质分歧：

- [第 202–203 行](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:202)：表称覆盖 D397；我认为“其他部分”和“没有主要部分”均被请求写窄。
- [第 208 行](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:208)：表承认三、四结果没有形状，但我将其列为需要处理的分类缺口。
- [第 217 行](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:217)：表称最后检查全部重复上文；我认为“参考值落在中间区间”此前没有明确写出。
- [第 222 行](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:222)：表认为相关身份字段不用；我认为 D38 要求的回答来源及期间／时点区分没有得到明确保留。