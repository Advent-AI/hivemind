# role-v29 对照签字标准（第 3 版，D243）

2026-10-29。逐句读 `src/hivemind/prompts/role-v29.txt` 和 `categories-v29.json`，对照 `docs/prd/05-extraction-standard.html`。没有发请求。这是开跑前的第三步（`docs/CURRENT_STATE.md` 的 next task），不是改动；改动按第 9.3 节一类一类做，每类先量基线。

## 和标准不一致，会改变答案的（要改）

| # | 标准（节） | role-v29 现在怎么写 | 差在哪 |
|---|---|---|---|
| 1 | 整体倾向谨慎、对增量敏感（§5.1，D243 方向） | 只有"一页有八条就是八条，不挑" | 没有"先问这是不是新信息、它让哪个答案变了"；会把常识和长期状况也当证据 |
| 2 | 主张和背景要带数字和具体的叙事，还要是新信息（§5.1，D243 第 5 条） | 第 (3) 类是"A named party's claim or estimate about the company or its industry"，没有条件；不留清单里只有"general risks or unargued verdicts""framing or background""view on politics or strategy without a figure" | 一条没写数字的具名主张（"能抢份额""仍然供不应求"）按现在的写法会被收 |
| 3 | 共同量 `shared_quantity`：任何一家公司之外、好几家都会受它影响的量或价格（§3 D 类，D243 第 2 条） | `industry_aggregate: one aggregate quantity for one calendar year` | 价格、利率没有开题理由。代码已有 `ADMISSION_REASONS_V13`（含 `shared_quantity`）和 `views/identity.SHARED_REASONS`，要做的是提示词这一句和版本切到 V13 |
| 4 | 收购算约束性义务（§3 C 类，D243 第 7 条） | "an equity stake whose size is stated and is not yet completed" | 没写收购 |
| 5 | 来源层：一句话符合两行取上面那行；混合的一条按主要说法定层（§5.5，D243 第 9 条） | 四层的定义有，次序和混合的规则没有 | "知情人士说公司将宣布"会被判成事实或传闻，两种都有 |

## 一致的（不用改）

四类陈述和例子（跨行业）；从第一段读到最后一段、八条就是八条；没有业务规模的产品细节；股价、仓位；和公司市场都无关的别家公司估值和交易（D238）；只有形容的引语（第 10 条）；一件事几句话是一条；来源层四层的定义；公司数用公司财年；约束性义务的两种问法和 18 个月；不开的清单；一个问题一个量一个期间。

## 怎么写都不扣分的（可选，不改）

在研公司的市值被提示词列为不留，按第 4 条是可选；T8 要求读目标价，按第 4 条也是可选；生态数字、重提的过去实际数都是可选。

## 顺序

先用 role-v29 在那一周和新的留出集上各发三次量基线（第 9.2 节），再按上表从影响最大的一类改起：先看基线里因为第 2 条多收了多少、因为第 3 条少开了多少，数大的先改。每改一类，全部文章各发一次和上一版比（第 9.3 节）。
