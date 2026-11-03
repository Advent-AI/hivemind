**我的结论：保留“抽取时看已有问题、决定证据给谁用”的架构；取消“必须挂题才能保存”和“按上下级关系自动删用途”。Claude 对我上一轮证明方法的批评成立，但他的替代规则仍保留了一个会继续误删的条件。**

博通就是最清楚的例子：23 条数字记录已经保存，却都没送进自研芯片题；其中只有 10 条去了总收入题。因此，独立保存解决不了这个例子，只取消总收入兜底也解决不了。

本轮只读文件和 SQLite，连接均使用 `mode=ro`；没有改文件，没有发送模型请求。下文 `v108 d1` 等简称，指 [research.md:145](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/research.md:145) 列出的六份账本。

**1. 新数字：哪些复现，哪些解释不成立**

我运行了两个 census 脚本，又独立比较了原始回答、处理后的记录和最终账本。

| 账本 | Claude 的“删过上级链接” | 排除先被引文检查拒绝的记录后 | 确认最终入库 |
|---|---:|---:|---:|
| v94 d1 | 180 | 178 | 178 |
| v94 d2 | 221 | 218 | 218 |
| v94 d3 | 189 | 185 | 185 |
| v108 d1 | 31 | 31 | 31 |
| v108 d2 | 27 | 27 | 27 |
| v108 d3 | 40 | 40 | 40 |

复核方法是：从 `model_calls` 取 `purpose='extract'` 的回答，按请求中的文章 ID 对应 `handovers.input_id`；用原始局部证据 ID 比较处理前后链接，再以文章 ID、处理后的引文和摘要对应最终 `evidence`。

**v108 数字成立；v94 的说法需要修正。** 原脚本只看原始回答和最终依赖关系，没有检查证据是否先被拒绝。[pruning_census.py:22](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/pruning_census.py:22)

例如，v94 d1 的 `call_id=368/e2` 已因 `quote not in item` 被拒，不能再算成删上级链接造成的损失。三个 v94 账本分别有 2、3、4 条这种情况。

但上述数字仍然只是**受删除操作影响的记录数，不是误删数**。v108 的 98 条占全部 1,667 条入库记录的 5.9%；不能由此推出“它解释的错误份额小”。是否误删，必须检查被删用途本身。

关于补上规则的追问，我核实了三件事：

- 存档 `call_id=818` 的请求，与导出的请求 JSON 相等。
- 其中的归属规则，与当前冻结的 `FILING_RULE_ROOT_FALLBACK` 相等。
- `--with-rule` 确实把这段规则原文放进追问，但依然移除了原来的结构化输出要求。[probe_filing.py:10](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/probe_filing.py:10)

结果也与 Claude 所述一致：第一次坚持“供应商收入不是客户支出”，第二次承认应该给 v16 使用。[追问结果:2](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/probe-broadcom-filing-with-rule.txt:2)、[追问结果:6](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/probe-broadcom-filing-with-rule.txt:6)

**我同意“部分成立”，不同意把它当成已经找到唯一原因。** 追问仍在强调“是不是本题自己的数字”，属于事后解释；没有重做原始抽取。第二次承认错误，也不等于下次生产请求会正确归属。

`missing_census.py` 的原口径数字同样完全复现：

| 三遍合计 | 未匹配到原始回答 | 匹配到、因无归属删除 | 匹配到、引文被拒 |
|---|---:|---:|---:|
| v94 | 130 | 28 | 4 |
| v108 | 113 | 16 | 2 |

**但不能把第二列直接解释成“这些事实从未写出”，也不能把第三列直接解释成“这些判断需要的事实被删了”。** 脚本按文章和词重合匹配，并只取金标两个位置的引用。[missing_census.py:26](/Users/lchingen/hivemind/docs/research/2026-11-03-filing/missing_census.py:26)

这里有比跨媒体漏匹配更严重的问题：

| 原报告的解释 | 金标实际上使用的内容 |
|---|---|
| q10 用“净利润 583 亿”推营业利润率 | 对 i084 的引用用的是**毛利率 74.9%** |
| q11 用“现金流 503 亿、486 亿”推 EPS | 对 i131 的引用用的是**回购 193 亿** |
| q11 用“数据中心收入 752.5 亿”推 EPS | 对 i129 的引用用的是**EPS 1.87 和总收入 816 亿** |

来源：[gold-v1.json:501](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:501)、[gold-v1.json:553](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:553)。

这不是要求改金标。**问题是诊断脚本把“同一个材料编号”当成了“同一个事实”。**

真实的删除问题仍然存在。例如 v108 d1 `call_id=214`：

- e1：数据中心季度收入，空链接；
- e3：总收入及 EPS，空链接；
- e5：毛利率指引，空链接；
- e7：经营现金流及自由现金流，空链接。

这些都被记为 `no home`。其中 q12 确实用两种现金流之差估算资本开支。[gold-v1.json:592](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:592)

所以，“代理证据进不去”是真的问题；但“所有这些删除都是同一种字面误读”尚未证明。**连问题自己的季度数字都被丢掉了。**

**2. 直接回答 A：由谁决定，何时决定，看什么**

Claude 说得对：我上一轮没有把执行者说完整。现在明确如下，作为提案：

- **执行者：** 当前负责抽取的同一个模型。
- **时点：** 读完文章、确定要保留的陈述后，在同一次回答结束前决定用途。
- **输入：** 完整文章、这些陈述，以及文章当天开始时已经开放的问题；每题包括问题正文、对象、数量口径、期间和已有描述。
- **决定：** 分别判断每条陈述能帮助回答哪些问题，并说明它提供的是哪个判断依据。它可以有多个用途，也可以暂时没有用途。
- **代码职责：** 验证问题身份、出处和时间；不根据上下级关系推断某个用途无效。

这仍然可能误读。我不再声称“换个保存结构就修好了博通”。真正要验证的是：**把“题目自己的数字口径”与“可用于回答题目的材料”明确分开后，模型是否会改变归属。**

当前请求同时存在“按收件说明覆盖范围找题”和“通过影响关系找题”两种要求，分别见 [role-v74i.txt:1](/Users/lchingen/hivemind/src/hivemind/prompts/role-v74i.txt:1)、[placement.py:53](/Users/lchingen/hivemind/src/hivemind/placement.py:53)、[placement.py:72](/Users/lchingen/hivemind/src/hivemind/placement.py:72)。修订必须同时处理这些位置，不能只在最后追加一句“像分析师一样思考”。

**我不建议现在改成判断时检索。** 因而没有一个被我隐去的检索算法或新增检索调用。

D264 的原话是：

> “我们这个架构设计的核心就是透过适当的Prompt 和引入已经开的题，和题的叙述来决定抽取”

[D264:3076](/Users/lchingen/hivemind/docs/DECISIONS.md:3076)

上述提案**保留这个架构核心**。但 D264 的落地规则还包括“无链接就删除”；这一部分会被改变，不能说完全不动 D264。[D264:3077](/Users/lchingen/hivemind/docs/DECISIONS.md:3077)

**3. 直接回答 B：撤回原来未定义的零成本证明**

上一轮“重放即可证明博通送达”的说法不成立。原始回答没有 v16，重放不会凭空产生正确判断。

替代证明分开做：

| 要证明什么 | 明确定义的操作 | 能证明到哪里 |
|---|---|---|
| 自动删链接是否阻断用途 | 在内存中保留原始回答已有的链接，对比当前处理后链接 | 零成本；证明代码删除了什么 |
| 无归属删除是否丢失已有内容 | 比较原始回答、`handovers.dropped`、最终证据 | 零成本；证明哪些内容因无归属消失 |
| 新规则能否让模型选对问题 | 重发受影响的存档抽取请求 | **必须有新调用** |
| 送达后判断是否改善 | 仅替换受影响判断请求中的材料，再发判断 | **必须有新调用** |

第一个操作已有明确正反例：

- v108 d1 `818/e1` 原本有 v1、v2，取消自动删除会保留总收入用途；
- 同一回答的 `818/e2` 原本只有 v1，取消自动删除后仍然没有 v16。

这正好证明：**代码删除与模型漏选，是两种不同故障。** 当前删除位置见 [extraction.py:806](/Users/lchingen/hivemind/src/hivemind/extraction.py:806)。

获准以后，最小的抽取证明可以先取 v108 d1 四个原请求：

1. `818`：博通代理数字，以及同记录中的总收入／分部收入；
2. `214`：自己的季度数字和现金流被判无归属；
3. `929`：Marvell 同时影响自研芯片市场和竞争份额；
4. `429`：必须继续排除的背景材料。

每个发送三次，共 **12 次抽取调用**。这是局部机制证明，不是验收，也不能据此报告全类修复率。

随后才考虑重发三个 v16 判断请求。v108 的 q10 从未判断过，**不存在可直接重发的 q10 判断请求**；若要测它，必须明确称为“按历史状态新构造的判断请求”。

**4. 直接回答 C：Claude 的规则哪里会继续错**

**最明显的问题，是它一边说“按用途”，一边又规定“不是上级自己的数字就删”。这两个条件相互冲突。**

四个反例：

- **竞争材料可以同时影响两个问题。** v108 d1 `call_id=929/e3`、最终 `e502`，写的是 Marvell 超过 50 个项目机会、潜在终身收入 750 亿。原始链接是 v6、v16，代码删了 v6。它不是 NVIDIA 份额这个数字本身，但可以是竞争依据。Claude 的上级例外仍会删掉这种用途。这里是否足以影响当年份额需要分析判断，不能由父子关系裁决。

- **总收入也需要产品收入和价格依据。** v94 d2 `call_id=645/e6` 的 Vera 收入目标同时给 v1、v19，最终删掉 v1。金标确实用这笔产品收入估计总收入。[gold-v1.json:72](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:72) “仅保护总收入自己的数字”救不了它。

- **“能作代理”不等于“是同一个量”。** 两份成功读到博通数字的旧判断，都明确折扣网络业务等不属于目标市场的部分。查询 `v94 d1/d2 judgements WHERE view_id='v16'` 的最后记录，`implied_outcome` 分别估计约 400—500 亿、750 亿。不能把“卖方收入量买方支出”写成自动等同关系。

- **多题使用不能替代保留标准。** v108 d1 `e246` 是“六个平台已经提供 Nemotron”；金标明确把它列为已有安排、背景、不收。[golden-v5-dev.json:16572](/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:16572) 如果模型给它编出需求、份额、收入三条理由，“每道会用的题都收”反而放大错误。

因此，Claude 当前版本是**一个正确方向，加上互相冲突的补丁**。尤其应去掉“只有上级自己的数字才保留”这个例外。

“没题用但保留”也确实改变 D209。原决定写得非常明确：

> “the placer's unfiled statements go to the handover's dropped list with the reason no home”

并明确不建设重新归属机制。[D209:2649](/Users/lchingen/hivemind/docs/DECISIONS.md:2649)

不能借“分析师应该留笔记”绕过这个决定。若 Alex 接受独立保存，暂时无用途的记录当时就**没有判断读者**；本提案不暗含自动检索或日后自动重新归属。这个局限必须公开。

**5. 直接回答 D：先定义事实，再量四个环节**

首先纠正我自己：上一轮的 **228 对仍不完整，应该是 230 对**。

漏掉的是：

- q01 的 `against.text` 中引用 i202；
- q18 的 `reference.text` 中引用 i231。

来源：[gold-v1.json:92](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:92)、[gold-v1.json:813](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:813)。

不过，230 只是“问题—材料编号”组合数，**还不是应送达事实数**。

我建议的零成本诊断定义是：

1. 从金标的 `reference`、`implied_outcome`、`against`、`decisive_items`、`reasoning` 中读取所有明确引用。
2. 对每个引用，读金标实际使用的那个事实。例如 q10／i084 取毛利率，不取净利润。
3. 为该事实记录主体、具体事项或数量、期间、实际／预测状态、条件及原始说话者。
4. 跨媒体匹配这些含义。金额相同、词相似、同一材料编号，都不足以确认相同事实。
5. 一条记录含多个事实时分别对应；一个事实拆成多条时允许合起来覆盖。无法确定的标“待核实”，不能强算有或没有。

**“应该送到 Q”在这里仅指：冻结金标明确用它帮助回答 Q。** 这是一个有明确正例的诊断集合，不覆盖所有有用证据；没有被金标引用，也不能判成不该送达。

四个环节这样数：

| 环节 | 可检查的定义 |
|---|---|
| 保存 | 截止检查时点，账本有记录完整表达这个事实 |
| 分配给问题 | 这些记录至少一条有通向 Q 的有效链接 |
| 展示 | Q 的真实存档请求实际包含所需内容；不能只检查证据 ID |
| 引用 | Q 的回答引用对应记录；复合记录还要核对理由用的是不是这个事实 |

还要另记通过依赖问题结论传来的内容。否则，会把“没有直接链接但已间接读到”算成损失。真实请求会截短引文和依赖结论，所以检查最终文本是必要的。[judging.py:182](/Users/lchingen/hivemind/src/hivemind/views/judging.py:182)、[judging.py:200](/Users/lchingen/hivemind/src/hivemind/views/judging.py:200)

时间上，用 `created_seq`、链接 `seq` 和判断 `seq`；不能用文章宣称的原始日期，把后来才收到的报道提前提供给判断。最终状态与“整个期间是否曾读到”分开统计。

**我已按事实而非媒体，对博通两笔数字跑完六份账本：**

| 账本 | 保存的事实 | 分配给 v16 | 最终请求展示 | 最终回答引用 |
|---|---:|---:|---:|---:|
| v94 d1 | 2 | 2 | 2 | 2 |
| v94 d2 | 2 | 2 | 2 | 2 |
| v94 d3 | 2 | 0 | 0 | 0 |
| v108 d1 | 2 | 0 | 0 | 0 |
| v108 d2 | 2 | 0 | 0 | 0 |
| v108 d3 | 2 | 0 | 0 | 0 |

两笔事实分别是季度 AI 收入 108 亿、下一季度指引 160 亿。逐条核对来源后，跨媒体对应的记录如下；这里的枚举是**诊断身份对应表，不是生产归属规则**。

下面的代码可直接在仓库根目录运行，只读六份账本，复算上表：

```python
import json, re, sqlite3
from pathlib import Path

root = Path.cwd()
bases = {
    "v94": root.parent / (
        "hivemind-extraction-quality-2026-10-28/"
        "docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94"
    ),
    "v108": root / "poc/data/e2e-r9-frozen-v108-2026-11-03",
}
# 人工读过引文和上下文的同事实记录：Q2 实际值；Q3 指引。
aliases = {
    ("v94", 1): ("213 374 403 415", "130 213 375 406"),
    ("v94", 2): ("228 426 438 500", "137 228 431 496"),
    ("v94", 3): ("226 437 448 511", "138 226 441 512"),
    ("v108", 1): ("219 410 444 454 523", "136 220 411 446"),
    ("v108", 2): ("236 431 460", "156 237 432 463"),
    ("v108", 3): ("242 442 470 483", "157 242 443 473"),
}
def ro(path):
    c = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c

for (version, draw), facts in aliases.items():
    folder = bases[version] / f"d{draw}"
    c, a = ro(folder / "views.sqlite"), ro(folder / "archive.sqlite")
    j = c.execute("""
        SELECT * FROM judgements WHERE view_id='v16'
        ORDER BY judgement_id DESC LIMIT 1
    """).fetchone()
    request = json.loads(a.execute(
        "SELECT request_json FROM model_calls WHERE call_id=?",
        (j["call_id"],)
    ).fetchone()[0])
    user = "\n".join(m["content"] for m in request["messages"]
                     if m["role"] == "user")
    shown = set(re.findall(r"^- (e\d+) \[", user, re.M))
    cited = set(json.loads(j["cited_evidence_json"]))
    stored = {r[0] for r in c.execute(
        "SELECT evidence_id FROM evidence WHERE created_seq<=?", (j["seq"],)
    )}
    filed = {r[0] for r in c.execute("""
        SELECT evidence_id FROM evidence_links
        WHERE view_id='v16' AND seq<=?
    """, (j["seq"],))}
    totals = [0, 0, 0, 0]
    for fact in facts:
        ids = {"e" + n for n in fact.split()}
        assert ids <= stored
        for k, population in enumerate((stored, filed, shown, cited)):
            totals[k] += bool(ids & population)
    print(version, draw, totals)
```

这段代码中的展示与引用身份，已经逐条核对过博通数字在请求摘要及回答理由中的含义。扩展到全部 230 对时，仍需先做上述事实拆分；**不能把这张两事实表冒充完整归属验收。**

**6. 收敛：目前能 defend 的排序，以及唯一建议**

先给能量化的边界：

| 顺位 | 机制 | 目前能确认的份额 | 不能据此声称什么 |
|---|---|---|---|
| 1 | 模型在抽取回答中没有选到用途 | 博通 **23/23** 条数字记录原始链接均无 v16；完整 230 对沿用旧词匹配时，262 次“在别题”中 **260 次**原回答就没有目标链接 | 不能把 260 次全部判成真实错挂，更不能全部归因于收件说明 |
| 2 | 总收入兜底接走材料 | 博通 23 条中 **10 条到 v1**；其余 13 条到 v2／v6 | 兜底解释去向的一部分，不是漏选 v16 的充分原因 |
| 3 | 无归属即删除 | v108 原始回答共 2,109 条，**416 条因 no home 删除**；已确认其中有问题自己的数字及现金流依据 | 416 条并非全都应该保留 |
| 4 | 自动删上级用途 | v108 **98 条记录**受影响；旧词匹配的 262 次“在别题”中 **2 次**原回答已有目标链接 | 不能用总删除数当误删数，也不能仅保护“上级自己的数字” |
| 5 | 重复报道重新进入阅读窗口 | v108 最终总收入请求共展示 320 条记录，其中 **108 条有 `same_claims` 的重复关系**；36 对关系满足旧链接已过窗口、新链接刚进入窗口 | 这是放大和重复展示机制，尚未证明它造成了错误归属或错误预测 |

查询依据分别是：

- `model_calls.answer_json` 对照 `evidence_links`；
- `handovers.handover_json → dropped`；
- `same_claims` 对照最终判断请求，以及该次判断之前第五次判断的 `seq`。

最后一项只是系统记录的“相同陈述”关系，不是我确认的 108 条纯冗余。真实例子是 v108 d1 `e266 → e334`：同一份 Bloomberg 的 3,930 亿收入预测，以后来报道重新进入窗口；后一条还含利润信息，不能整条当废话删除。

**这个排序有两层确定性：模型漏选是博通类的首要故障；全体错挂中，各种提示词误读各占多少，目前没有可靠数字。** 把“收件说明误读”“兜底”“必须挂题”分别算成互斥百分比，会重复计算同一条错误链。

我最终只推荐这一条结构规则：

> **每条证据与每道问题之间的用途，都是独立的分析判断；保存与否不由是否存在用途决定，用途也不由问题的上下级关系决定。**

它保留 D264 的抽取时决策方式。它不要求所有证据都进总收入，不要求另建检索，也不承诺把所有问题一次修完。对于银行、药厂、零售商和芯片公司，含义相同。

Alex 需要决定的是：**是否接受这条规则所包含的“可暂时无用途保存”和“多个真实用途并存”，并据此打开新版本。** 涉及的旧决定不能略过：

| 决定 | 原文要点 | 提案如何处理 |
|---|---|---|
| D207 | “one home, the narrowest question” | 改为逐个用途判断，取消自动排斥上级用途。[2633](/Users/lchingen/hivemind/docs/DECISIONS.md:2633) |
| D208 | “Root judgements read driver and theme conclusions, not their evidence” | 保留通过下级结论传递；但不再据此禁止同一事实另有总题用途。这是放宽原设计。[2640](/Users/lchingen/hivemind/docs/DECISIONS.md:2640) |
| D209 | 无归属进 `dropped`，不建重新归属机制 | 独立保存明确改变前半句；不暗中建设后半句。[2649](/Users/lchingen/hivemind/docs/DECISIONS.md:2649) |
| D264 | 开题库参与抽取，由抽取决定归属 | 保留决策者和时点；改变其继承的无归属删除条件。[3076](/Users/lchingen/hivemind/docs/DECISIONS.md:3076) |
| D274 | 冻结提示词、归属规则、收件说明和 schema | 必须另开版本，不能修改冻结文件。[3155](/Users/lchingen/hivemind/docs/DECISIONS.md:3155) |
| D354 | “A change is a new version only Alex opens” | 写入与匹配输入会受影响，需要明确授权边界；不自动改判断提示词。[3694](/Users/lchingen/hivemind/docs/DECISIONS.md:3694) |

最便宜的证明顺序是：**先按实际事实修正诊断对应关系；再零成本隔离代码删除；获准后审查完整新请求并做 12 次局部抽取；只有归属真的改变，才重发受影响判断。**

在这之前，不应启动整条流水线，也不应把“双方同意一条规则”当成它已经有效的证据。