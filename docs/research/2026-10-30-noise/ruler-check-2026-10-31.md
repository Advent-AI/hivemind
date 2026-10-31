# Ruler check on the not-kept statements role-v63 keeps (2026-10-31)

Alex, 2026-10-31, after the v63 report: "但是还是有70多篇被留下；你再次重新检查尺子，看看是不是这些留下的还有歧义；然后再思考怎么降低noise".

## Population

Run Y3, role-v63, development gold (golden-v3-signed.json, sha256 78844bc3…), three draws. A not-kept gold entry counts as kept in a
draw when a kept statement's quote matches its span (`score_gold.same`, the scorer's own match; `final_scores.py`). 117 distinct
entries are kept in at least one draw, 232 draws in all (77.3 per draw): 45 in all three draws, 25 in two, 47 in one
(`kept_rejected.py` → `kept-rejected-Y3-v63.json`).

## Method

A blind reader (Codex, read-only) judged each of the 117 against the signed standard, version 4, mixed with two controls it could not
tell apart: 40 core or supporting gold entries v63 keeps in at least two draws, and 30 not-kept gold entries v63 never keeps
(`blind_ruler.py`, seed 20261031; packets in `blind4/`). The key and the kept list were moved outside the repository while it read.
For each statement it gave a weight (core, supporting, optional, not kept), whether the standard settles it, the lines it used and,
when not settled, the sentence the standard would need.

## Results

| Group | Statements | Reader agrees with the gold | Reader disagrees |
|---|---|---|---|
| Control: gold keeps, v63 keeps | 40 | 38 kept | 2 not kept |
| Control: gold rejects, v63 drops | 30 | 28 not kept | 2 supporting |
| Gold rejects, v63 keeps | 117 | 82 not kept (157 draws) | 35 kept: 31 supporting, 4 optional (75 draws) |

The reader agrees with the gold on 93–95% of the controls but on 70% of the entries v63 keeps: the model keeps exactly where the
ruler is least settled. The reader called 8 of the 35 "ambiguous" itself; the other 27 it read as settled the other way.

Per draw, v63's 77.3 split three ways (`partition_rejected.py`, in this order):

| Part | Per draw | What it is |
|---|---|---|
| Carried | 16.0 | Every statement matching the not-kept span also matches a kept gold entry: the not-kept words ride inside the quote of a matter the gold keeps (a deployment quoted with the partner's listing history, a valuation quoted with its derivation and its target). One record of a kept matter, not a separate noise record. |
| Disputed | 21.0 | The blind reader would keep the entry. |
| Noise | 40.3 | The gold and the blind reader both say not kept. |

## What the disputed entries show about the ruler

Each disagreement was read against the article and the standard's text (`blind4/verdicts-*.jsonl`, `blind4/key.json`).

1. **The counting unit.** The 16 carried draws are counted because the scorer matches sentences, while the signed unit is one matter,
   "一件事用几句话说仍是一条" (standard §2). Counting a not-kept entry only when its statement matches no kept gold entry changes the
   measuring stick: Alex's call.
2. **Gold rows that the standard's text contradicts.** The D238 row is cited for another company's operating facts (Hesai's lidar cost
   and market share, the Nebius–LangChain integration), while the standard's D238 paragraph says "别家公司的动作和经营数字不能用这一行删掉，
   它们留不留按 5.1 的规则判". The Singapore defendants' denial and defence statement are marked not kept, while 5.3 makes the case
   optional. "Broadcom is more than 50% more expensive than Nvidia's" is marked "without a number". Corrections to a frozen gold are a
   separate dated record (AGENTS §7.1), not made here.
3. **Two lines that point opposite ways** (the standard needs a sentence; Alex decides each):
   - A. **An arrangement retold without a date** (14 draws: Nokia AI-RAN, Mercedes CLA on DRIVE, labs using NVL72, Marvell,
     Coherent and Lumentum, NemoClaw available). D243 proposal 5 rejects background the analyst already knew; the 5.3 retelling row
     (D243 proposal 6) says "抽取看不到库，只能从文字和日期看……看不出是旧事的不算重提". The gold used the analyst's knowledge; the reader
     used the text.
   - B. **How close another company's matter must be** (24 draws: Hesai ×2, a partner reactor going critical, NRC review times, a
     Korean cluster's 15 GW, a Microsoft–MediaTek interconnect plan, Nebius–LangChain, operators' target customers, Intel's card price,
     Huawei Ascend demand). 5.1 counts customers, suppliers, competitors, regulators and the economy and the D238 paragraph sends
     their actions and figures to 5.1; the gold judged them as touching none of the seven drivers ("金标里把这类判断标出来供复核").
   - C. **A comparison the company, a partner or a third party publishes** (14 draws: 10x lower cost than closed models, 40% more GPUs
     in a power budget, cooling water to near zero, a workstation test, an open model's release). The product row's boundary names
     only a competitor's comparison against the company's product.
   - D. **A named analyst's view of a new event with a short reason** (12 draws: a Kyber delay widening a competitive window, Seaport's
     circular-financing concern, a memory shortage capping Chinese AI firms, a DRAM crisis that "won't end soon" because contracts are
     locked). 5.3 rejects "没有推导的看法"; the standard does not say what counts as a derivation.
   - E. Financing analysis and valuation pieces (5 draws: an IRR scenario for a backstopped rental book, a 1.3x debt-service floor, a
     relative valuation, a target stated after its derivation) and the Singapore case statements (6 draws, optional by 5.3).

## What the agreed noise shows about the prompt

32 of the agreed-noise entries kept on their own in at least two draws were put back to the model in its stored conversation
(`probe_keep.py`, replies in `probes/v63-keep-*.txt`): which sentence of the request kept it through the closing check. 14 quote
review-v63's closing list whole ("Keep these whenever they move such a question; none is dropped for the reasons above: …"), 11 quote
one of its items (a partner's action or figure, a named party's action without an amount, a change to the product's plan or
configuration, adoption or integration, a price decision), 4 quote the role text's kind (3) ("a named party's new claim or estimate
about the company or its industry"), 3 quote no instruction. The closing list overrides every "usually fail" row, which contradicts the
standard's structure: 5.3's exceptions sit on their own row and say "不能用这一行删掉，按 5.1 判", never "keep". The list is review-v63's
own sentence, written in this session; six Codex rounds read it sentence by sentence and none flagged its scope.

## The fix being measured

review-v64 (`poc-v80`): the rows are not kept (5.3 不留); each exception sits on the row it limits and says what that row does not
cover, which the check judges; the closing list is cut; 5.1's "fitting one of the four kinds does not keep an item" and D240's "a
missing amount, date or scale never drops one" are said once. Read-only Codex rounds 7–9. Measured against role-v63 in run Y4 with
key-v64.json (frozen before the send); the disputed entries are reported apart and decide nothing until Alex settles them.
