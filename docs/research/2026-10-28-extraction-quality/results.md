# 第一步的结果：主题论点展示给抽取（A），对照 / 实验各 3 次（2026-10-28 16:06–16:15）

一句话：A 翻转了它该翻转的那些陈述（三次里三次），没有让垃圾变多，没有碰坏公司论点那几条；它不治冷启动，也不治模型自己挂错的那几条。

## 怎么做的

- 尺：`gold-standard.md`；金标冻结在发送前（`gold-extraction.sha256`）：按规则抽的 20 篇 15 条 + 按事件选的 6 篇 11 条，共 26 条（core 11）。
- 对照：每篇文章当天的生产请求用生产构造器重建，26 篇的请求哈希都等于存档里的那次（`ab_gold.py check`）。中途修了 harness 一处：[Research groups] 块是按当时全文索引取前十名的，用现在的账本重建会变，改成从存档请求取当时的组清单。第一次的残留归档在 `results/aborted-first-attempt/`，不计。
- 实验：同一请求，只在 [Existing theses] 里加上当时开放的全部主题论点（schema 的 folds_into 随之扩大），别的一字不动。
- 各发 3 次，每次一个独立的草稿存档（同一请求会被存档直接复用，所以分开）。打分是代码（`ab_gold.py score`），每格后面有案例 id；`ab-results.md` 是完整的格子表。
- 费用：6 组 × 26 篇 = 156 次发送，$0.165；加上废掉的第一次约 $0.03。

## 总表（26 条金标，11 条 core）

| 组 | 次 | 留对 | 留了挂错 | 写了被丢 | 没写 | 拆分 | 多留 | 原始条数 | 留下 |
|---|---|---|---|---|---|---|---|---|---|
| 对照 | 1 | 9（core 6） | 3 | 13（core 3） | 1 | 9 | 53 | 239 | 69 |
| 对照 | 2 | 11（core 6） | 3 | 12（core 4） | 0 | 11 | 48 | 252 | 67 |
| 对照 | 3 | 7（core 5） | 3 | 13（core 5） | 3 | 8 | 32 | 225 | 46 |
| 存档答案（$0） | — | 13（core 7） | 4 | 9（core 2） | 0 | 9 | 51 | 246 | 74 |
| 实验 | 1 | 13（core 9） | 4 | 8（core 1） | 1 | 9 | 51 | 231 | 73 |
| 实验 | 2 | 15（core 8） | 3 | 7（core 2） | 1 | 8 | 51 | 227 | 76 |
| 实验 | 3 | 14（core 8） | 2 | 8（core 2） | 2 | 10 | 55 | 221 | 78 |

噪音底：对照自己四次（三次发送加存档那次）"留对"在 7–13 之间晃。所以看的是三次全体，不是单次。

## 读法

1. **该翻的翻了，三次里三次。** 管理层的超大规模资本开支数（a11-1，core）：对照三次要么没写、要么挂到没展示的 v4/v5 被丢；实验三次都留下挂到 v4。Kessler"极少量 H200 已出货"（a09-1，core，留出集）：对照 2/3，实验 3/3 并且挂到了 v3/v11/v14。Benzinga 同一消息（t01-1、t01-2）：对照各有一次挂到没展示的 v14 被丢，实验 3/3。Reuters ZTE 获批（t02-1 core、t02-2）：对照 3/3 被丢，实验 2/3 留对。
2. **没碰坏公司论点的那几条。** 俄亥俄 $1,050 亿（a07-1）、SB Energy（a07-3）、WSJ $6,000 亿（a14-1）、RTX 50 Super 搁置（a03-1）：两组六次全对。
3. **垃圾没变多。** "多留"对照 53/48/32，实验 51/51/55；实验里挂到主题 id 的多留只有 2/8/9 条，看了样本 1 的两条，一条是 a11-1 的拆分、一条是"Q2 指引假设对华 H20 为零"（金标按复述拒了，但挂到 v3 并不错）。
4. **留出集**（6 篇 4 条）：对照 2/4、2/4、1/4，实验 2/4、4/4、3/4。
5. **A 不治的两类，看得清楚。**
   - 冷启动：开源权重那封信（t03-1 core、t03-2、t03-3，07-24，v27 还没开）两组六次全部"写了被丢"。没有问题就没有证据，是设计（D42）。
   - 模型自己挂错：SK hynix 缺货到 2030（a03-2 core）七次全挂到 v19 或丢掉，没挂到毛利率 v6；KeyBanc 说 Vera Rubin 小延期（t01-3）七次全挂到收入 v2/v10。这是"挂得太宽 / 挂错"那一类，和展示什么无关。
6. 还看到一条 harness 以外的事实：存档里那次生产答案比三次新发送平均都好（13 对 9/11/7）。同一字节的四次抽样"留对"7 到 13，抽取是采样器这件事在这把尺上量出来了。

## 定论

A 可以上：翻转在决定性案例上成立，三次一致，没有副作用。它的收益边界也写清了：主题相关的那部分（这 26 篇里约 8 条）；冷启动和挂错不是它的事。

## 下一步（按计划）

- A 的代码：`store.views_for_prompt` 加开放主题论点（或它的两个调用处），加一条检查：组成员列表里的 id 必须都可挂。一周整条路回放，数主题论点的证据数和再判断次数。谁来改、什么时候切默认配置，Alex 定（另一条线也提了同一条）。
- 第二步 B（碰撞裁决折入 + 事件期间归代码）$0 验；第三步 C；第四步挂错/拆分（a03-2、t01-3 这一类）用同一把尺一改一测。

## 文件

`ab_gold.py`（check / replay / send / report）、`results/send-control.json`、`results/send-themes.json`、`results/replay.json`、`results/archive-*.sqlite`（六个草稿存档）、`results/send-*.log`、`ab-results.md`（完整格子表和多留清单）。

## A 改好后的两周整条路回放（2026-10-28 16:24–16:58，`english-v35-nvda-2w-2026-10-28`）

改法：`store.views_for_prompt(themes=True)`（对象的开放论点加全部开放主题论点，按创建顺序一个清单）、`extraction.shown_views`（展示清单的唯一主人，串行和并行两个调用处都走它）、按提示词版本门控（`THEMES_SHOWN_FROM = 19`，v18 字节不变）、组成员列表只打印能挂的 id；`role-v19` / `categories-v19`（内容同 v18）、`poc/config/poc-v35.json`。测试 `tests/test_theme_shown.py` 三条先红后绿，全套 218；preflight exit 0；$0 复现 `resift_with_themes.py`：1,040 篇存档答案按"当时开放的主题也可挂"重筛，多留 49 条，挂的是 v14/v4/v5/v27/v16。

两周（07-01 到 07-14，243 篇，4 个 worker，$0.59）对照长跑自己的前两周（poc-v34，同一写入器，$0.62）：

| 量 | 对照 v34 | A v35 |
|---|---|---|
| 开的论点 | 17（主题 7） | 17（主题 5） |
| H200 许可论点 | 3 个（v3、v11、v14：证据 16/6/1，判断 1/2/1） | 1 个（v12：证据 14，判断 3） |
| 四大云厂资本开支论点 | v4 2 条证据 2 次判断，v5 2/2 | v5 7/4，v6 7/5 |
| 丢弃里"挂到没展示的 id" | 17 | 0 |
| 原始陈述 / 留下 | 1,694 / 612 | 1,745 / 571 |
| 没留证据的文章 | 115 | 120 |
| 费用 | $0.62 | $0.59 |

读法：
- 机制成立：挂到没展示 id 的丢弃归零；H200 一件事一个问题（对照开了三个），而且那一个活着（14 条证据、3 次判断，对照的 v3 只判断过 1 次）；资本开支两个主题论点各 7 条证据、4–5 次判断（对照各 2 条、2 次）。这正是 A 要治的"主题论点开了就死"和"同一件事反复开"里属于 A 的那一半。
- 留下的证据总数 612 → 571、没留证据的文章 115 → 120：一次抽样对一次抽样，差在采样器的噪音带里（同一字节三次发送"留下"在 46–78 之间晃），不能据此说 A 让证据变少，也不能说没有。金标实验（三次）量到的是留对上升、多留不变。
- 两边都开了小事件论点（对照：Firmus、法国反垄断；A：RTX 60、2026 年游戏架构、"内存占数据中心支出的份额"）——这是 C 的类，A 不碰。
- 费用相同。

## One-week acceptance of the pushed design (2026-10-28 evening)

Run `english-v36b-nvda-1w-2026-10-28` (poc-v36: themes shown, placement-narrow-v1 with the title line, unplaced kept), 07-01..07-07,
8 workers, archive cost $0.22 (extract 0.145, place 0.039, judge 0.024, match 0.011). One malformed extraction answer halted day 7;
the day was resumed from the archive and finished. Scorer: `accept_week.py` (table in `results/accept-week-table.md`); the ledgers
laid out for reading by `read_week.py` (`results/read-v34-week1.md`, `results/read-v36b-week1.md`).

Read by hand, not by the script:
- Placement is right by inspection. Total revenue holds 11 pieces, all NVIDIA's own figures and guidance (v34: 106, mixing DeepSeek
  chips, Greenpeace emissions, IREN contracts). Data Center revenue 4 (v34: 72). Kyber holds the whole delay story (46 pieces,
  including the Rubin Ultra rack claims, NVL576, "roadmap intact"), because the group's aliases carry "Rubin Ultra". The judge cites
  every piece it holds on the two revenue theses (11/11, 5/5; v34 33/106, 34/72) and reads a third of the tokens (median 1646 vs 4616).
- Admission is the open defect, unchanged by this round. This draw did not open the week's most important question (the AI Compute
  Partnership guarantees) nor H200 permission; it opened a Valar Atomics nuclear data-center deployment (23 pieces). The same
  moomoo article was sent four times across the three runs: two answers propose the ACP candidate, two propose none. Admission is a
  coin flip per send; E3 (fold duplicates, refuse small-event theses) must also make admission of the decisive question stable.
- 630 of 752 kept statements have no home, by design until the driver layer exists; 72 of 98 articles contribute to no thesis today.
- The week's one gold article (a11): v36b places the hyperscaler-spend statement right and leaves the 82%/41% growth line unplaced;
  v34 drops the spend statement and places the growth line; v35 places the spend statement and drops the growth line. Even.

## Admission arm: the binding-obligation sentence (2026-10-28 night, `admission_arm.py`, 78 sends, ~$0.09)

Mechanism (two stored accounts, `results/ask_admission.json`): D184/D185's reason "binding_obligation … due when its signing can be
checked, at most 18 months out" is written for a deal not yet signed (Ohio). For a programme already announced and signed (the AI
Compute Partnership) the model either proposes nothing ("describes the arrangements without establishing a signed, named obligation
due within 18 months") or dates the question on the item day ("the relevant check was whether it had been signed by the item date"),
which the code refuses. Arm = one sentence replaced (`results/role-v21-draft.txt`, +345 characters, reason: the old sentence is the one
both accounts quote and no other sentence covers an obligation already in force): not yet signed → yes/no due after the item within 18
months; already taken on, one deal or a programme → a financing_amount question on the amount at the next annual filing, settled by
its commitments note. Control = the production bytes stored in the archives. Reference frozen before the send
(`results/gold-admission-acp.json`, sha `6647b3bb9dc6…`). Three draws, eight threads.

Read by eye first (Alex: "本来数据就没什么信息量来抽取?"): of the ten ACP articles sent, five carry the obligation in their text (moomoo:
guarantees, repurchase of unsold capacity at a pre-agreed price; datacenterdynamics: "rent back unused GPUs at a fixed rate";
mlq.ai: minimum utilisation guarantee; SemiAnalysis: the take-or-pay backstop economics; economictimes: "credit support"), NVIDIA's
own blog names "credit-support" once, and four (cnbc, qz, yahoo, mitrade) describe only the revenue share: there is no obligation to
extract from them, and "none" is the right answer on those four. Two of the three Ohio articles were sent on 07-27 with the Ohio
thesis already open (v31 in their shown list), so they are not admission cases; the Reuters article of 07-26 is.

| article (what its text carries) | control d1/d2/d3 | arm d1/d2/d3 |
|---|---|---|
| moomoo (guarantee, repurchase, revenue share) | none ×3 | opened ×3 (+ the Ohio signing event the article also reports, ×2) |
| datacenterdynamics (rent-back at a fixed rate) | none ×3 | opened ×3 |
| mlq.ai (utilisation guarantee) | none ×3 | proposed ×3; kept 1, refused 2 by the ladder-label check (ranges, not the five asset rungs) |
| SemiAnalysis (backstop economics) | none ×3 | opened ×3 |
| economictimes (credit support) | none ×3 | opened ×2, none ×1 |
| NVIDIA blog (credit-support model) | none ×3 | opened ×1, none ×1, plus one the scorer's pattern missed ("credit-support commitments", hyphen): opened ×2 by eye |
| cnbc, qz, yahoo, mitrade (revenue share only) | none | none |
| Reuters Ohio (talks to guarantee $250bn) | opened ×3 | opened ×2; refused ×1: due 2028-01-26, one day past the 548-day bound |

Totals over three draws: on the six articles that carry the obligation, control opened 0/18, the arm proposed 17/18 and the code kept
13/18 (refused: 2 ladder labels, 2 none). Extras fired by the arm: the Ohio signing event from the moomoo article (in its text; v35
opened the same) and nothing else. The Reuters Ohio case keeps opening (2/3; the one refusal is the 18-month boundary). Not changed:
the ladder-label rule (D186) refuses an obligation-amount question whose rungs are ranges; two of twelve proposals died there.

## D210 acceptance week (`english-v37-nvda-1w-2026-10-28`, $0.21, `results/accept-week-table.md`; the drops read one by one in `results/thrown-away-read.md`)

| | v36b | v37 |
|---|---|---|
| ACP question | not opened; 96 statements homeless | opened 07-01, 29 pieces, 5 judgements with an analyst's reasons; ~33 ACP statements still homeless (8 the opening article's own, ~25 size-less retellings) |
| Kyber delay story | opened, 46 pieces | not opened: the one proposal was in the item's first send and the re-send answered without it; ~56 statements homeless |
| theses that should not exist | Valar reactor (23 pieces) | Intel equity stake ($5bn, 2 pieces), Verkada equity stake (undisclosed, 1 piece): the amount form applied to "an equity stake" |
| placed / no home / other drops | 108 / 630 / 14 | 55 / 705 / 13 |
| junk among the drops, by reading | 393 (62%) | ~470 (67%) |
| material drops by mechanism | no standing question 205, same-item 5, placer 10, marginal 16 | re-send re-rolled admission ~60, no standing question ~100, ACP retellings ~25, same-item ~8, placer ~10, Valar 41 |

The sentence does what the arm measured: the programme opens and holds its evidence. The week's material loss did not fall, it moved: the
parallel day's re-send (34 of 98 items) re-samples admission and discards the first answer's candidates (9 this week, Kyber among them).
That mechanism was present in every earlier run too (v36b opened Kyber from an item that was not re-sent). Next, in order: keep the
first send's candidates across a re-send (code, D172–D183's recompute); the placer sees the item's candidates; "an equity stake" out of
the amount form.

## Ledger-blind arm (D211, `blind_arm.py`, 117 sends ≈ $0.15, `results/blind-arm-answers.json`)

The v22 request (poc-v38: no [Existing theses] block, no [Research groups] list, links only to the answer's own candidates, no
folds_into/lost_if_folded) on the 34 items the v37 week sampled twice plus 5 more Kyber articles, three draws; control = the two
stored v21 answers of each item. Read by item:
- Kyber (7 articles, 21 sends): the launch question proposed in 6 sends across 5 articles, at least one article in every draw; under
  v21 one proposal in ~10 sends, erased by the re-send. With one request per article and matching folding the duplicates, a story
  carried by seven articles opens when any one of them proposes it.
- ACP (moomoo): the obligation-amount question in 3/3 draws, but draw 3 split it four ways (capacity repurchase, CoreWeave
  capacity purchase, lease guarantees, the Ohio signing); the collision judge (D190) must hold them as one matter: to measure in the
  week run.
- Already-open questions re-proposed, as expected (total revenue, Data Center revenue, gross margin, the two capex aggregates, the
  memory share): about 10 of the 25 distinct questions; they fold at matching.
- Junk that the amount form still admits: the Verkada investment 3/3 (the "equity stake" word, open defect); NVIDIA's $119bn supply
  commitments as a financing_amount question (two articles; material, but it is a purchase obligation, not a guarantee).
- Per-sample stability is unchanged: 25 distinct questions, 3 in all three draws, 6 in two, 15 in one. The gain is at the story level,
  not the sample level. Statements per answer: median 8; no malformed answer; one ladder-label refusal.

## D211 acceptance week (`english-v38-nvda-1w-2026-10-28`, $0.23, `results/accept-week-table.md`; drops read in `results/thrown-away-read.md`)

| | v37 (D210) | v38 (D211) |
|---|---|---|
| extraction sends / items | 135 / 98 (34 re-sent) | **98 / 98** (none re-sent) |
| theses opened | 9 | 17, of which 4 duplicates by wording (ACP ×2, Kyber shipment, revenue growth) and 1 succession |
| match outcomes | new 10 | new 19, merge 12, succession 1 |
| stories with a page | ACP; not Kyber, Rubin, H200 | ACP, Kyber, Rubin shipping, H200, capex ×2, CPU, DC revenue, total revenue, supply commitments |
| placed / no home | 55 / 705 | 146 / 685 |
| items with no placed evidence | 78 | 57 |
| judge: ACP page | 5 judgements, cites 9 | v1 6 judgements, cites 32, reasons sum the $6.3bn + $3.5bn + $4.88bn and say what is not established |
| judge: Kyber page | none | v11 3 judgements, cites 19, "repeated coverage treated as one claim" |

Verdict: admission is no longer the loss. Every story of the week has a page, the request is one sample per article, the parallel day
re-sent nothing, cost unchanged. The loss moved to matching: the collision judge's `distinct_question_same_matter` opens a page per
wording (4 of 17), and the placer loses more statements when near-identical pages compete (~60 with the home shown, against ~10
before). Next mechanism, in D190's contract: a candidate on the same matter and the same quantity or event as an open page folds into
it whatever its wording; a new page needs a different quantity, period or decision (the same test D184 already states for lost_if_folded).

## D212 correction: count final retained content, not pages or handovers

The [retention audit](../2026-10-28-retention-audit/results.md) supersedes the paragraph above's claim that the remaining loss has moved
entirely to matching. Same 98 inputs, all 2,363 final extraction records across v36b/v37/v38 accounted for, $0 new calls. Actual written
records are 106/54/144, useful ones 67/47/127. Useful-output retention is 23.0%/17.4%/44.9%; v38 removes 254/255 clear junk records.
However, on the fixed 20-article source reference the complete final claims are only 12/33, 5/33 and 13/33; core claims are 12/25,
4/25 and 11/25. Cleaner output and more pages do not establish more complete core coverage. The semantic labels are Codex-authored.

V38's 156 useful losses have an exact trace classification: 94 lack a corresponding question throughout the week, 49 had a home
shown, 7 could use the item's own unshown candidate, 4 precede a later question, 1 fails the quote check and 1 is lost at matching.
The earlier approximate 60-home-shown count mixed these cases. The four duplicate-page examples also cross different boundaries:
ACP is in D190, revenue/growth bypasses its gate, and launch/shipment conflicts in code. No causal claim about duplicate pages causing
placement losses has been verified. The new audit and its fixed source reference govern the next bounded comparison; no default changed.
