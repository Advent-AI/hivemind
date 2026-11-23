我没能把方案写进计划文件，因为这次会话里 Write 工具被禁用了，所以完整方案都放在下面。没有发送任何请求，也没有改任何源文件。

# 结论

**候选**：只改 `clean-arch/step2/compare.py` 里 `PIECES['supersedes']` 这一句，让新材料自己必须在回应旧记录的主句。

**测试**：7 条完整归档请求 × 原句和新句两个版本 × 3 次，共 42 次调用，约 $0.01，不需要再向 Alex 确认。

先说明一点：我没有打开 `06-views` 第 191、197、306 行。标准溯源只经由 D168 的引文，审计时要补读。

## 候选措辞

当前原句（275 字符，`compare.py:61-63`）：
> a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises it; another statement on the same topic is not this

候选（我手数约 401 字符，净增约 126，脚本要重算）：
> a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that **very** claim, or the original source revises it; **the incoming piece must itself address that main statement, outright or by plain implication, and a reply to or news about another claim of the same story is not this**

和原句的差别只有三处：
1. "that reported claim" 改成 "that very claim"，把确认或否认钉在同一条主句上。
2. 尾句原来是话题层的排除（"同话题的另一句不算"），现在改成对新材料一侧的要求：它必须自己在回应那条主句。
3. 明写 "outright or by plain implication"。这样不要求逐字点名，间接更新（C073）和官方确认（D168）都保留。

没动的部分：
- "a later version" 的时间条件原样保留。
- 官方的确认和否认都还在。
- 不加"不确定"这个输出，不加分数门槛，句子里没有任何公司或产品名。
- `same_statement` 和 `different` 两句不改。

**风险**：Jev 只返回类型化标签，不给理由，所以这句话可能只是旧句的同义改写。C036 的输入摘要里已经写明 Kyber NVL144，而旧句早有"同话题不算"，Jev 还是判错了。因此对照臂自己的波动要算进判据。结果只能是"否决"或"值得做留出集"，不能说修好了。

## 标准溯源

| 候选里的句子 | 来源 |
|---|---|
| later version … changed | PRD §5 Revision 行；D168 原文 |
| that very claim | D168 "confirms or denies **that claim**"；PRD §13 "what each statement refers to" |
| must itself address that main statement | PRD §5 "A later statement about the same subject is not necessarily a revision" |
| outright or by plain implication | D168 明确包含确认；draft-review.md 要求不得强制逐字点名 |
| another claim of the same story is not this | D168 "another statement on the same topic is not this" 的具体化，不是新规则 |

D381 的"只放进最像的那组"只读标签，不受影响。

## 测试设计

**构造**：每例是该新记录的完整归档请求，包含所有候选问题 q0…qN，答案也保留全部候选的标签。对照臂用归档原字节。候选臂是同一字节，只把每个问题里的 supersedes 句替换掉。发送前做 $0 断言：差异只出现在这一句，替换次数等于该批问题数。每个回答再过未改动的 `compare.outcome`，得到 kind、repeat_of、revises，也就是同一条 label→group→link 链。

**7 例**：
- 正常重复：B01（Broadcom 的有效重复）。
- 真更新或对照：
  - C035：明确回应 NVL576 时程。
  - C073：来源报道的政策放松，不等于已完成采购。
  - C021：官方否认 Kyber 延迟。旧文已含这条否认，所以不是干净的时间先后对照，它就是先前的 P01。
- 假更新线索：C036、C057。
- 争议：C059（即 R05）。两位读者和第三位意见不一致，只报告，不计分。

**预先写好的判据**：
- **护栏，任一破则停**：
  - C035、C073、C021：对照臂 ≥2/3 次给 supersedes 的，候选臂也要 ≥2/3，且重放后的 revises 目标边不能丢。
  - B01：候选臂 same_statement ≥2/3。
  - 任何 supersedes→same_statement 的翻转都算回归，因为那会把更新变成合并，比现状更糟。
  - 其余候选问题的标签变化，以及额外的 revises 边（如 P01 在 45:e3 上的争议边），逐条列出。
- **改善线索，仅为线索**：C036 或 C057 在候选臂 ≥2/3 次离开 supersedes，且对照臂 ≤1/3 次离开。
- **停止**：护栏被破，或两条假线索都不比对照臂好。后者判为同义改写，终止这条线，不再改措辞。

**报告顺序**：先报回归，再报失败和用量，然后给每例 3×2 的原始标签和重放结果，再由我亲自读 C036、C057、C035、C073、C021 的原文轨迹（AGENTS §7.2）。不写新评分器。

## 限制（报告里必须带上）

- 样本是 Jev 自己选出的 supersedes。双读者都判"不同"的 14 条里 13 条是同一个 Kyber 故事，它们不独立，不能当 56 个独立错误，也不是误差率。
- C057 是同一个融资项目里的另一句话，机制未必和 Kyber 类相同。
- C007 类的输入摘要缺目标，不在本测试内。C036 和 C059 的摘要里目标其实已在，所以缺上下文不是唯一原因。
- **时间**：候选没动 "later"，所以测试不能检验先后。
  - C021 旧文已含否认。
  - C073 只知道发布日。
  - C047 和 C052 的元数据冲突，没有纳入。
  - 未知时间不能被补成事实。
- C035、C073 的"应为更新"是读者解读，不是冻结金标。C059 因分歧不计分。B01 只是一个重复。
- 7 例 × 3 次不能估计总体，只能否决，或支持做留出集。不能推出准确率、召回、下游投资判断改善，也不能说 Step 2 已修好。

## 成本与停止

以下是估算：
- 先前 Jev 完整请求 18 次共 78,795 输入 token，约 4.4k 每次。
- 42 次约 0.2M token × $0.042/M ≈ $0.01。
- 候选臂每题多约 30 token。
- 保守预留公式可能显示数分钱。

建议设硬预留 ≤ $0.10、共 42 次、每个请求只发一次、不重试、不续跑，首个失败后不再发下一批。费用按 `model.PRICES` 按 token 计算并披露费率。

## 发送前条件：哪些真的阻塞

**不阻塞**：
- 费用和授权：AGENTS §7.3 "Own the loop" 允许几分钱、已同意方向、无 stop 的探针直接做，用户也已明确指示。CONCLUSIONS.md 末段同样如此。
- `scripts/preflight.py`：它只重放 v108，不覆盖 clean Step 2（HARNESS-DESIGN.md 实施备注）。替代做法是归档身份重放（`check_archived_requests.py` 已 76/76 匹配），再把存档答案过 `compare.outcome`，都是 $0。
- "整请求审计未做"：这次的改动只有一句，用 $0 字节差异断言证明即可。AGENTS §7.3 的"发送前 council"由这次 Codex–Claude council 加家长的独立复核满足，不需要新增确认。

**真正要处理的工程项**（不是确认要求）：
1. **绕过缓存**：对照臂字节和归档一致，走常规 `jev.ask` 会命中存档而不是新采样。必须用逐字节单次 HTTP 的发送器。可参考另一工作树的 `diagnostic.py`（`send_one`、`validate`、`execute`），它的设计评审过，但要换新 manifest 和 14 个正文哈希，不能假设旧发送器直接适用。
2. 发送前即时确认没有其他付费作业在跑（AGENTS §9）。
3. 用新目录，`mkdir(exist_ok=False)`，响应严格校验，不保存密钥。
4. 发送前不再改运行用的代码。

## 家长执行顺序

1. $0：核对 14 个正文哈希，跑差异断言，把存档答案重放 `compare.outcome`，与 `comparison-after-challenge.json` 的标签对一遍。
2. 假传输测试：每个请求恰好发一次，失败后不续批，缓存不命中。
3. 发送 42 次，按上面的判据读原始标签。
4. 只在 Step 2 记录里追加一行，不改产品配置和冻结尺子。