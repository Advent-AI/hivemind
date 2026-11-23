# Prompt audit of clean Step 1 (c8), identity first (D460): the agreed table, 2026-11-13, $0

Two readers, read apart: Claude (`AUDIT-CLAUDE.md`, written first) and a blind Codex reader given only the standard, the request and the
failure cases (`AUDIT-BLIND.md`). The request: `request-system.txt`, `request-user.txt`, `request-schema.json` (c3, step 42). The standard:
`docs/prd/05-extraction-standard.html`, version 5, frozen.

**Answer: the request decides whether a new question is the same as an open one with the standard's general rule only; the standard's
boundaries for that decision are not in it, and one date sentence narrows the standard.** In the clean architecture Step 1 sees the open
theses and no later step compares theses, so the decision §4 gives to matching ("同一题、续期，还是另一题：匹配这一步的事") is the Step 1
model's, made with "the same underlying question … cannot move apart" and without §4's specific lines.

## The failure classes (both readers)

| class | request sentence(s) | the standard's line | Claude | blind reader | agreed |
|---|---|---|---|---|---|
| F1: the unsigned Ohio deal linked only to the programme's amount (u2, u3, c1, c2, c3) | closing check: "A new thesis that asks the same underlying question, about the same subject and scope … is not proposed"; "drop the thesis … if an open thesis exists and its answer cannot move apart from it"; §3 S7 | §4: "还没签的单笔交易是'签不签'的是非题，照旧可以开，不并进计划的金额题"; §3 C's size test | missing | missing | **missing** (materiality of the guarantee still needs judgement: the $500bn is the facility's build-out cost) |
| F2: next year's shared quantity folded into this year's question (u1, u3 q04; u2, c2, c3 q13) | "Another population or wording of the same aggregate is evidence for it"; the closing check's "same underlying question, about the same subject and scope"; S2 "do not assume different periods are automatically the same thesis or automatically unrelated" | §3 D: "自然年的今年或明年。同一个量、同一年只有一个问题，由代码按'主题＋量＋期间'判"; §4: the next period is a successor | missing + abstract | missing | **missing** (linking 2027 evidence to the 2026 question is not itself an error; the missing 2027 question is, given its own significance) |
| F3: a shared price over a non-calendar window or with two quantities (u1, c1, c2) | "A thesis asks one quantity for one period, or one event"; "for this or next calendar year" | §3: "一个问题只问一个量的一个期间，或一件事"; D: a calendar year | misread | misread | **misread** |
| F4: an announced programme dated as an unsigned obligation (u2, c1) | "One already undertaken is tracked by its amount at the next annual report; one not yet signed by …" | §3 C: "已经承担（一笔或一个计划）…按下一份年报" | abstract | misread | **disputed** (two cases) |
| F5: Step 1 shapes the ladder step refuses (two figures with none main; rolling windows) | "one quantity for one period"; "for this or next calendar year" | §3 as above; D417 | misread | misread (disputed refusals read case by case) | **misread** |
| F6: the memory price not opened for want of an item-supplied release date (u2, u3) | "A shared quantity takes its release date … only when the item supports one. A question no date can settle is rewritten or not opened." | §3: "量是它的发布日"; §4 "能核对": a date and public material, not an article-supplied day | contradiction | contradiction (with an evidence limit: the q05 row it was pointed to does not quote the reason; TRACE.md does: "no specific price/date", "doesn't give a specific contract price series with a release date") | **contradiction** |

## The standard's identity lines the request does not carry (both readers)

The unsigned single deal beside the plan's amount (D210, D248 unchanged); the shared quantity's year in its identity (D197); several forms
of one plan as one question, and a deal joining the plan already tracked by amount (D248 b1); different deadlines of one event, and the
successor on an unresolved expiry (b2); the next period as a successor (D190); the event's period start not blocking a merge (b5). Carried:
the general rule, another estimate/source/wording/direction/population, the milestones of one product generation (b3).

## Other findings of the blind reader (outside the failure classes; recorded, not acted on)

The request has no main-driver opening reason (the company's own annual lines, §3 A); in this pipeline those are seed questions, and the
seven graded questions do not include them. Some do-not-open items (dividend declarations, organisational changes, every product variant)
and the required closest open thesis and kept-evidence prerequisite have no explicit line in §3–§4.

## What it points to (hypotheses for the council)

- **One structural mismatch, not one sentence:** the owner of the identity decision moved to Step 1 in the clean architecture, but the
  standard's boundaries for it stayed with matching. Both readers: F1 and F2 share this weakness; the traces do not prove one causal
  sentence.
- **One contradiction:** F6's sentence narrows the standard's shared-quantity due day to one the item supplies.
- **Misreads** (F3, F5, and F4 by one reader) are sentences the model has and does not apply; AGENTS §6 says a misread needs the model's
  account before any change, and F3's and F5's shapes are refused downstream by the ladder step.
