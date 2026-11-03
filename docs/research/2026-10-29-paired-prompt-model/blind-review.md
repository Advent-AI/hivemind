已亲自读完 **60/60 份完整盲答**并对照五份来源。我的复核结果是：**5 份不应判为内容完整，2 份有漏记的来源忠实度问题；六个 NVIDIA 角色疑点仍应保留为不确定。**例如，四份回答保留了 Cloud 的全部数字，却没有保留这些数字属于“Q2”。

这是对模型评分的再次复核，不是人工金标，也不足以宣布哪个模型或提示词获胜。

**1. 冻结核心内容：43 份完整，5 份部分保留**

| 案例 | 完整阅读 | 完整 | 部分保留 |
|---|---:|---:|---:|
| NVIDIA 商业模式 | 12 | 12 | 0 |
| NN 扩产 | 12 | 11 | 1 |
| Google Cloud | 12 | 8 | 4 |
| 已签保证 | 12 | 12 | 0 |
| 新加坡排除案例 | 12 | 不适用 | 不适用 |

需要修正的具体判断：

- **R008、R037、R046、R060：`complete → partial`。**四份分别写了“Google Cloud revenue growth of 82% to $24.8 billion”“Google Cloud revenue growth of 82% to $24.8 billion”“Google Cloud revenue of $24.8 billion, up 82%”“Google Cloud revenue growth of 82% to $24.8 billion”，但完整回答均未交代 **Q2**。提到上一期“Q1”不能代替本期归属。[来源](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-paired-prompt-model/blind-sources.json>)明确写的是“In Q2 … 82% … $24.8 billion”。这是期间遗漏，不是数字编造。
- **[R035](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-paired-prompt-model/blind/R035.json>)：`complete → partial`。**限制项说目标的“**share attributable to this Wuxi expansion … [is] not disclosed**”。但来源正文将目标接在“This move … targeting US$80–US$90 million”之后，`item:e3` 更明确写“**from the expansion**”。回答保留了三个数字，却重新悬置了目标与这次扩产的联系，因此没有完整保留冻结的“一个相连供应事项”。

其余核心内容判断维持。没有发现把已签保证写成未签、把上限写成已付款，或把 Cloud 数字直接写成 NVIDIA 订单的遗漏错误。

**2. 漏记的事实问题与应保留的不确定性**

有 **2/60 份**存在可定位的来源忠实度问题；这里不是说现实事实已经被证伪：

| ID | 原答 | 来源证据与判断 |
|---|---|---|
| R035 | “share attributable to this Wuxi expansion … not disclosed” | 来源已把目标归于扩产。属于把已给的信息说成未披露；原评分只记录了其他措辞疑点，漏了这一处。 |
| [R014](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-paired-prompt-model/blind/R014.json>) | origin：“incident described as **occurring ‘last week’**” | 来源是“**Last week, Malaysian authorities said they had foiled** …”。“上周”限定当局发言，不能直接移成事发时间。这不影响它正确排除新加坡案。 |

六个 NVIDIA 角色疑点的校准判断可以维持：

| ID | 疑点原句 |
|---|---|
| R004 | “degree of NVDA's financial exposure through credit support are unknown” |
| R020 | “credit-support commitments NVIDIA would provide” |
| R022 | “with credit support extended to partners” |
| R031 | “how much credit NVIDIA would extend” |
| R041 | “NVDA's own credit support could add balance-sheet exposure” |
| R050 | “the scale of NVIDIA's financial exposure is unknown” |

来源只说采用信用支持模式，没有指明提供方。这些表述确实没有充分区分“谁提供”和“提供多少”，但结合完整回答，属于条件分析或未知敞口表述，**不应升级为“已确定 NVIDIA 提供担保”的事实编造**。

R032 的自研加速器推断、R035 的“tier-2”、R045 的客户关系措辞、R048 的“Q1 FY2027”、R059 的“NVIDIA link is an inference”，也没有足够依据升级为确定错误。尤其 R048 未经来源建立财年映射，但保留了原来的日历期间，不能据此断言期间实际错误。

**3. 七份非空提案：逐份按 D210 判断**

[D210](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md>)要求：已经承担的义务，问**下次年报时义务达到多少金额**，由承诺附注确定。是否付款、是否记负债，是不同的问题。

| ID | 提案关键原句 | 判断 |
|---|---|---|
| R009 | “Will NVIDIA report a material liability or payment exposure” | 不满足：问是否报告负债或敞口，没有问义务金额。 |
| R013 | “Will … disclose … maximum or recognized exposure … or … a recognized liability” | 不满足：仍是是否披露的问题，并混合不同金额口径。 |
| R024 | “Will NVIDIA disclose revenue … in fiscal 2027?” | 属于 `main_driver`，不是已承担义务；不能套 D210 判错。是否足以成为独立主要经营问题，维持不确定。 |
| R030 | “Will NVIDIA report any payment” | 不满足：问是否付款。 |
| R039 | “Will NVIDIA disclose a material recognized liability or loss contingency” | 不满足：问会计确认或披露状态。 |
| R043 | “What exposure …”；核验为“any payments or recognized liability and the status” | **应从不确定改为未满足 D210。**标题宽泛，但核验对象明确没有要求承诺附注中的义务金额。 |
| R056 | “What amount … paid or accrued” | 不满足：虽然问金额，问的是付款或计提金额。 |

所以，**六份已签保证提案均未满足 D210；另一份提案的适格性仍不确定**。这不推翻它们正文对已签保证的理解。

全部 **53 份 null** 不按理解失败扣分，其中已签保证的六份是 R011、R021、R025、R029、R038、R058。

**4. 新加坡负例：12/12 遵守排除要求**

R014 保留的是来源另述的马来西亚机场查扣：**72 台服务器、近 1300 万美元**。它明确排除了新加坡案，也没有断言查扣芯片属于 NVIDIA。

用户排除的是“**this Singapore server-transshipment case**”，并明确说不覆盖所有出口管制新闻。因此，正确判断单位是**指定案件是否被保留为研究证据**，不是整篇回答是否为空。原评分对此判断正确；R014 的时间归属问题应单列，不能改判为违反排除要求。

全程未编辑文件、未调用模型、未读取凭据、盲码映射、非盲回答或此前实验评分。