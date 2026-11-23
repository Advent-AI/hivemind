先说结论：我上一版的候选作废，也撤回上一版里说"字节差异 + council 就够了"的那几条。新候选只改措辞，每道题的 supersedes 句从 275 字符变成 272，净减 3，不增长。下面所有字符数都是手数，必须由脚本复核。

## 我上一版错在哪里

| 我之前说的 | 实际情况 |
|---|---|
| 候选 401 字符，净增约 126 | `audit-codex.md` 的"前缀版"每题已 +59。ten-candidate 的 `92:e2` 请求从 16,593 增到 17,183 字符（+590），违反 §6"增长要有等量删减或书面理由"。我的版本增长更大，撤回。 |
| 发送前字节差异断言加 council 就够了 | 不够。§6 要求整份请求的逐句审计，并由盲的第二读者读一遍；`audit-codex.md` 审的是当前请求和前缀版，并没有审我这一句。字节差异只能证明"只改了这一句"，替代不了语义审计。 |
| preflight 不阻塞 | 错。§5 要求任何付费前必须跑 preflight。它不覆盖 clean Step 2，但必须跑，且已经跑完。按 `harness-review.md` 的描述：v108 d1 重放 243 条抽取答案，726 条判过、12 条被拒（7 条引文不匹配、5 条重复引文），170 条匹配判断，2 条因请求缺失被跳过，另有 2 条历史 schema 拒绝。这些都要披露。我没有打开 log 文件本身。 |
| 成本约 $0.01 | 应以 `harness-review.md` 为准：七例不变字节的 42 次预留 $0.073964，只是预留不是账单。候选每题少 3 字符，差额可忽略，但必须按最终字节重算。我的 $0.01 是用旧探针用量粗估的，只能当参考。 |
| 发送器可以直接用 | 独立代码评审发现 4 个严重缺陷：发送口没有评审和 preflight 门、并发锁、网络在飞时日志写入失败、依赖未固定。修好并复审前不能假设就绪。 |
| 任何 supersedes→same 都算回归 | 过严。两位读者若都判旧句与新句相同，翻成 same 可能是对的。改为读原文判断。 |

## 唯一候选

当前（275 字符）：
> a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises it; another statement on the same topic is not this

候选（272 字符，手数）：
> Identify the statement addressed; a later change to the stored main statement: the same speaker revises that guidance, forecast or event progress, an official confirms or denies that claim, or the original source revises it; another statement on the same topic is not this

字符数：每题 −3；`92:e2` 十候选请求 16,593 → 约 16,563（−30）。提示 token 数未测，本地 `tiktoken` 不可用，不能拿字符数当 token 数。

## 每一处改动的溯源

只有一处新增：开头的 "Identify the statement addressed;"。其余四处都是删减：

1. **新增 "Identify the statement addressed;"**。
   - 来源：PRD §13 的 "what each statement refers to"，以及 `audit-codex.md` 指出的"没有告诉 Jev 先确认回应的是哪句"。这是假设，不是已签标准里缺的规则。
   - 没用 "target"：它可能被读成公司而不是命题。
   - 没用 "addresses the incoming piece's…"：太长。
   - 没写"必须点名"，所以不要求字面点名。
2. **"a later version of … , changed:" → "a later change to …:"（−10）**。
   - PRD §5 写的是"a later account changes the same statement"。"later" 仍在判据里，没有变成例子。
   - 没有新增日期要求，未知时间照旧无法检验。
   - 残余风险：把"一个更晚的版本"改成"一次更晚的变化"，可能被读窄。
3. **删 "piece's"（−8）**。同一请求的 `same_statement` 和 `different` 里已有 STORED PIECE 的叫法，指代清楚。`compression-review-codex.md` 要求对照真实来源报告复核，所以要纳入盲读。
4. **删 "statement"（−10），保留 "that"**。"that guidance, forecast or event progress" 仍然指向被改的那条主句。没有删 "that"，因为你指出的指代模糊正出在那里。
5. **删 "reported"（−9，"that" 保留）**。D168 的原文是 "confirms or denies that claim"，本来就没有 "reported"。

没动的部分：
- 官方确认和否认（D168）。
- 同一发言人和原始来源两种情形。
- "main"。
- 尾句"同话题的另一句不算"（`compression-review-codex.md` 明确要求保留，并拒绝了 271 字符版）。
- `same_statement` 和 `different` 两句。

## 对这个候选的自我质疑

- **和你给的 274 字符版的区别**：我用 "statement" 不用 "target"，保留 "that guidance" 和 "that claim"，并保留 "the original source"。"its original source" 的 "its" 指代不清，所以没用。
- **"addressed" 可能太窄**。事件进展被来源直接更新时，并没有一个被"回应"的句子，C073 就是这种情形。我靠判据里 "original source revises it" 那一支兜底，但这是否奏效只有 C073 能检验。
- **"Identify" 没有输出位置**，Jev 只返回标签。所以它可能被忽略，也可能与原句等效。这个事实只能靠对照臂的自身波动来判断。
- **身份不是靠句法证明的**。"statement addressed" 是否等于 "stored main statement" 由模型和读者按原文判断。措辞不能证明身份成立，我也不会这么声称。
- 本候选还没有被独立读者看过。`compression-review-codex.md` 评审的是你的 274 版，不是这一句。

## 测试与预先写好的判据

**测试**：七例都用完整归档请求，每个请求包含它的全部候选问题，对照臂是同日原字节，各发 3 次，共 42 次。

**要保留的输出**：
- 每个候选的标签和概率。
- 经未改动的 `compare.outcome` 重放后的 kind、repeat_of、revises，并和默认原结果比较。
- 额外的 revises 边单独列出。

**七例各自的角色**：
- **C036（`92:e2`，十个候选）**：同一请求里同时有
  - q0：正确目标，对 Kyber 延迟的直接否认；
  - q1：重复；
  - q3、q7、q9：被判错的相关链接。q3 需要单独检查。

  它一份请求就能同时测目标、重复和错链。
- **C035**：对 NVL576 时程的明确回应。
- **C073**：来源报道的政策放松。
- **C021**：只是目标识别对照。旧文已含否认，不证明新的时间先后。
- **C057**：同一项目里的另一句话。
- **B01**：正常重复。
- **C059**：争议，只观察、不计分。

**判据（比我上一版温和）**：
- **线索**：`92:e2` 的 q9（或 q7），C057 也一样，在候选臂离开 supersedes 的次数比对照臂多 ≥2 次（共 3 次），同时 q0 仍是 supersedes、q1 仍是 same_statement（各 ≥2/3）。
- **否决**，满足任一条：
  - C035、C073 或 q0，对照臂 ≥2/3 保持 supersedes，候选臂 ≥2/3 丢掉；
  - B01 或 q1 的重复，候选臂 ≥2/3 丢掉；
  - 错链没有一条比对照臂的自身波动更好（等同于原句，没有采纳理由）。
- **变成 same_statement 或其他标签**：对着两篇原文逐条读，判是错还是对，不自动算回归。读者判新旧相同的，可能是对的。

**限制**：
- 样本由 Jev 自己选出，Kyber 一个故事占大头，不能当 56 个独立错误，也不是误差率。
- 缺上下文类（如 C007）不在其中。
- 时间无法检验。
- 7 例 × 3 次只能否决，或支持做留出集。
- 不能证明下游投资判断改善，也不能说 Step 2 已修好。

## 发送前真正阻塞的条件

1. **§6 整请求逐句审计，加盲的独立第二读者读这一句**。没有做，也不能用字节差异代替（`audit-codex.md`）。
2. **§7.3 发送前 council**：对这句话做一次独立 Codex 读和一轮挑战。
3. **发送器的四个严重缺陷修好并复审**（`harness-review.md` 及你的转述）。
4. **发送前再跑一次 preflight 并确认没有别的付费作业在跑**。preflight 已完成，若代码或配置变了就要重跑，且它不覆盖 clean Step 2。
5. 已满足的：原始传输字节同一性（已被 `harness-review.md` 独立验证）、成本预留 $0.073964（候选字节更短，需按最终字节重算）、不需要再向 Alex 确认。

没有发起任何网络调用，也没有改动生产代码。