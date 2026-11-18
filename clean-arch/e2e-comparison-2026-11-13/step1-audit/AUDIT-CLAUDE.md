# Prompt audit of clean Step 1 (c8), identity first (D460) — Claude's table, written before the blind reader's

The request as the model reads it: `request-system.txt` (15,828 characters), `request-user.txt` (the open theses, the item, the closing
check; 14,373), `request-schema.json` (5,835), dumped from `poc/data/clean-e2e-full-2026-11-13/c3/step1/trace.sqlite`, step 42. The standard:
`docs/prd/05-extraction-standard.html`, version 5 (frozen).

## The structural fact behind the identity rows

The standard gives library identity to matching: "同一题、续期，还是另一题：匹配这一步的事，抽取不判库里的", and its test 4 ("不是重复") is
judged at extraction "只对同一篇文章里提出的几个问题…和库里的比由匹配做" (D211). The clean architecture shows the open theses to Step 1 and has
no later thesis-matching step (`clean-arch/architecture.html`: Step 1 "identif[ies] existing research … without proposing already tracked
research as new"; Step 2 compares evidence, not theses). So Step 1's model now takes the decision §4 governs, but the request carries only
§4's general rule, not its boundaries, and nothing does D197's code identity for a shared quantity ("由代码按'主题＋量＋期间'判").

## The identity sentences of the request

| id | where | sentence |
|---|---|---|
| S1 | §2 | "Match by the underlying question or outcome, subject and scope, and time when relevant, not by word overlap. A different wording, source, forecast or direction alone does not make a new thesis. Related questions can be separate when their outcomes matter independently." |
| S2 | §2 | "do not assume different periods are automatically the same thesis or automatically unrelated." |
| S3 | §3 head | "A thesis asks one quantity for one period, or one event." / "no open thesis already asks it" |
| S4 | §3 binding_obligation | "One already undertaken is tracked by its amount at the next annual report; one not yet signed by whether it is signed by a check date within 18 months of the item" |
| S5 | §3 shared_quantity | "for this or next calendar year … Another population or wording of the same aggregate is evidence for it." |
| S6 | §3 do not open | "another estimate, source or wording of what an open thesis tracks; an annual quantity after next year" |
| S7 | §3 | "the closest open thesis with why an analyst would bet on the two separately because their answers can move apart … If the two cannot move apart, link the evidence to every open thesis it informs instead." |
| S8 | closing check | "A new thesis that asks the same underlying question, about the same subject and scope, as an open thesis or another new thesis is not proposed: link its evidence to that thesis." / "drop the thesis … if an open thesis exists and its answer cannot move apart from it" |
| S9 | §3 dates | "A shared quantity takes its release date and a product event the date its outcome can be checked, only when the item supports one. A question no date can settle is rewritten or not opened." |
| S10 | schema | `closest_open_thesis`, `why_a_separate_bet`: "how their answers can move apart"; `outcome`: "The outcome or event being tracked by this thesis." |

## The standard's identity lines (§4, §3) and whether the request carries them

| standard line | carried? |
|---|---|
| general: "同一个结果能判掉两题，就是同一题；答案能分开走、而且分析员会分别下注的，才是另一题" (D248) | yes (S1, S7, S8) |
| another estimate, source, wording, direction; another population or proxy of one aggregate → same question | yes (S1, S5, S6) |
| several forms of one plan → one question (D248 b1) | no |
| an unsigned single deal is a yes/no question, "照旧可以开，不并进计划的金额题" (D210; D248 unchanged) | **no** |
| different deadlines: the later is evidence while the earlier is open; renewal on expiry (b2) | no |
| milestones of one product generation: one question (b3) | yes (product_node line) |
| company quantities by fiscal year; calendar-year estimates are evidence (b4) | not applicable (the request has no main-driver reason; the company's own lines are seed questions) |
| the next period of the same quantity is a renewal, another question in time (Succession, D190) | no |
| "同一个量、同一年只有一个问题，由代码按'主题＋量＋期间'判" (D197) | **no** (S2 is abstract; no code does it) |
| a shared quantity's due day is its release date ("到期日：量是它的发布日") | narrowed (S9: "only when the item supports one") |

## Failure classes → sentences → standard → verdict

| class (count) | request sentences | the standard's line | verdict | the model's account |
|---|---|---|---|---|
| F1 / M1: the unsigned Ohio deal linked only to the programme's amount (u2, u3, c1, c2, c3) | S7, S8 decide; S4 lacks the keep-apart clause | §4: "还没签的单笔交易是'签不签'的是非题，照旧可以开，不并进计划的金额题" | **missing** | "signing it simply raises that total, so the two cannot move apart" (c3); "the scoping rule wins" (u3) |
| F2 / M4: next year's shared quantity folded into this year's question (u1, u3 q04; u2, c2, c3 q13; at the capex article, step 42, all three full-run draws opened one year; c1 opened 2027 later from another article, step 60) | S5 and S6 ("wording of the same aggregate", "another … wording of what an open thesis tracks") read as covering another year; S2 abstract | §3: "同一个量、同一年只有一个问题" with the period in the identity key (D197); renewal is the next period (D190); D class: "自然年的今年或明年" | **missing** (the year in a shared quantity's identity) and **abstract** (S2) | "the same hyperscaler-capex quantity one year out" (c3); u1–u3 alike |
| F3 / M5: a shared price over a non-calendar window or with two quantities (u1, c1, c2) | S3, S5 | §3: one quantity of one period; D class: a calendar year | **misread** | u1: "a slip" |
| F4 / M6: the programme's amount given the unsigned-deal date (u2, c1) | S4, S9 | §3 C: "已经承担（一笔或一个计划）…按下一份年报" | **abstract** ("undertaken" is not defined for an announced programme already under way) | none taken |
| F5: Step 1 shapes the ladder step refuses (two figures with none main 5; a rolling window 3; full run, first pass) | S3; the schema's `outcome` does not ask for the one tracked quantity or event | §3 "问题怎么写": one quantity of one period or one event; D436: a second side of the same bet stays as not-judged context; D417: a rolling window without a publication day is declined | **misread** (S3 is there); the `outcome` definition change was dropped by D436 | the fourth Stage A: the ladder's own wrong refusals "over-applied" |
| F6: the memory price not opened because the item gives no release date (u2, u3) | S9 ("only when the item supports one"; "A question no date can settle is … not opened") | §3: a quantity's due day is its release date; the standard does not ask the item to supply it | **contradiction** (S9 narrows the standard; its scope is ambiguous) | "no specific price/date" (u2); "doesn't give a specific contract price series with a release date" (u3) |

## What the table points to (hypotheses for the council, not fixes)

1. F1 and F2 have one structural shape: the clean path moved library identity into Step 1's model and carried only §4's general rule; the two
   specific boundaries that would have kept these questions apart (the unsigned deal; another year of one quantity) are not in the request.
   A fix written from the standard would carry §4's boundaries to the owner of the decision (a closed set with cross-domain examples,
   AGENTS §6), or return identity to code where the standard puts it (D197, shared quantities only); either is a design for the council.
2. c14 carried the year boundary into the merge sentences and moved the memory question from "2027 against 2026" to 2026 (D441). Any design
   must keep a comparison of two years of one price ("next year's price against this year's") one question: the standard's own class-D
   example ("2027 年 DRAM 合约价相对 2026 年的变化").
3. F6 is a contradiction in one sentence (S9), with two cases; F3, F4, F5 are misreads or abstract clauses with two to five cases each.

Lengths: no change proposed here.
