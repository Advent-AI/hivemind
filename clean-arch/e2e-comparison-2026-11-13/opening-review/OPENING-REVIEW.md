# The opening losses against the signed standard (D457), 2026-11-13, $0

**Answer: few opening losses are shown breaches of the signed standard, and those few are spread over small mechanisms; the largest
classes are choices the standard leaves open.** Fixing any one mechanism would open at most one to three more question-draws to comparison
on the frozen ruler in these twelve draws, an opportunity none of which is measured as a right final answer. No opening mechanism is shown
to be large enough to carry a phase on this evidence (D458).

Sources: the full run's 36 not-agreeing graded question-draws (`cases-full.txt`, built by `build_opening_cases.py` from the matching and
eligibility readings), the earlier production draws q1–q3 (RESULT.md and `poc/data/clean-e2e-comparison-2026-11-13/draw-q*/`), and the
earlier clean draws u1–u3 (TRACE.md, 17 cases, with the model's own accounts). The standard is the frozen extraction standard, version 5
(`docs/prd/05-extraction-standard.html`): §3's table (classes C, D, E and their due days), §3 "how a question is written" ("一个问题只问
一个量的一个期间，或一件事"), §4's "same question, renewal or another question" (D248's boundaries). Each verdict (`VERDICTS.md`) was read
by Claude against the stored question, its source article or raw answer, and the standard's line, then challenged by the council
(`council/mt-codex-4.md`), which moved the Ohio and "launch" cases from breach to unresolved.

## The four outcomes, per run and system (question-draws)

| | breach shown | reasonable alternative | the standard does not settle it | unresolved (readers split, ambiguous, or no account) | total |
|---|---|---|---|---|---|
| clean, full run c1–c3 | 3 | 2 | 4 | 9 | 18 |
| production, full run p1–p3 | 1 | 3 | 7 | 7 | 18 |
| production, earlier q1–q3 | 3 | 3 | 10 | 2 | 18 |
| clean, earlier u1–u3 (TRACE.md) | 7 | 3 | 6 | 1 | 17 |

A question-draw with a breach and an allowed difference is counted under "breach".

## The mechanisms, with their evidence status

| mechanism (the standard's line) | shown | not shown (unresolved) | systems | what fixing it alone could open to comparison |
|---|---|---|---|---|
| M1. An unsigned single deal (the Ohio lease guarantee) filed only into the plan's amount question, no yes/no question opened. §4: "还没签的单笔交易是'签不签'的是非题，照旧可以开，不并进计划的金额题" (D210; D248 unchanged) | 2: u2, u3 (the model's accounts: "a component of that amount", "the scoping rule wins") | 5: c1, c2, c3 (link reasons only), p2, p3 (no candidate, no reason): the line says the deal *may* be opened, and opening needs the model's judgement that it is a separate bet | both | none shown: the five draws that opened it (p1, q1, q2, q3, u1) chose check dates the standard allows and none is eligible against 2027-06-30 |
| M2. An undated pending regulatory decision given 2026-12-31. §3 E: "文章没写日期的待决监管事项，用本财年末" (the two source articles give no date for China's approval; read) | 4: p2, q1, q2, q3 | — | production (the clean draws and p1, p3 use 2027-01-31) | unmeasured: each also names a narrower population, which the matching readers call narrower, though an approval for named firms can answer "any firm" |
| M3. The product-node question says "launch" without defining it. D248 boundary 3: "一题，问能带来收入的那一步（通常是开始出货）；送样、发布作证据" | — | 3: p1, q2, q3 (p2's is a matching split): "launch" is ambiguous, not shown to name the wrong milestone | production | p1 at most (its deadline is the ruler's; its answer is reader B's, but on a launch question, not a shipment question) |
| M4. Two capex years in one question, the later year as the base. §3: one quantity of one period; parts that move apart and are bet separately are split | 3: u1 q04, u3 q04, u2 q13 (the model's accounts) | 2: c2, c3 q13 (no account) | clean | up to 3 |
| M5. A shared memory price over a non-calendar window or with two quantities. §3 D: "自然年的今年或明年"; one quantity | 3: u1, c1 ("12 months to mid-2027"), c2 (prices and rack memory cost, NAND added) | — | clean (production opened no memory question) | unmeasured: the clean draws also chose 2026 alone, which the standard allows |
| M6. An undertaken plan's amount given the unsigned-deal check date. §3 C: "已承担的按下一份年报" | 2: u2, c1 | — | clean | none: also a part of the total (not settled) |

## The classes the standard does not settle (largest first)

1. **The programme against the total (q09), every one of the 12 draws, both systems** (10 counted here; c1 and u2 also carry M6). Each
   system asks the amount committed under the AI-cloud programme (or a programme and a lease-guarantee part, q1, p3); the ruler asks the
   10-K's total of all financing commitments and backstops. D248 boundary 1 joins the forms of one plan; the standard's own example for
   class C is a programme-level amount ("NVIDIA 为云客户产能兜底的义务在 FY2027 年报达到多少"). The standard's tests (same result, answers
   that move apart, a separate bet) were not applied case by case here; recorded as a concern beside D373, not as proof that both shapes
   are equally good.
2. **A later deadline or due day for Kyber (q18): the only difference in 6 question-draws** (c1, c3, p3, q1, u1, u3), beside M3 or a
   matching split in 3 more (q2, q3, p2): the systems ask "by 2028" after the report of a slip to 2028 (u1: shipments in 2027, due a year
   later). D248 boundary 2 governs a later deadline only while an earlier question is open; none was.
3. **The memory price not opened (q05), 8 question-draws** (p1–p3, q1–q3, u2, u3): opening a shared quantity is a judgement ("都可以开题");
   the standard's own class-D example is this quantity and the gold marks it must-open, but no line requires it. In production the memory
   facts went to the total-revenue questions (D273's fallback); in q3 the big four's 2026 capex did too, and no capex-2026 question opened.

## What it means

- **No single mechanism carries the losses.** The shown breaches are small (M2 4, M4 3, M5 3, M6 2, M1 2), and each is bounded by a second,
  allowed difference or by an eligibility opportunity no one has measured as a right answer.
- **The largest classes are choices the standard leaves open** (programme against total, the deadline after a slip, whether to open
  memory). A product change aimed at them would aim at the ruler's shapes, which D237 forbids; they are recorded as concerns. This does
  not show that the measurable gap is closed: the standard's own tests were not run on them case by case.
- **Production and the clean path break different rules where a breach is shown**: production's M2 (event dates), the clean path's M4, M5,
  M6 (periods and quantities).

## Limits

Twelve draws of one window; c2 and c3's capex-2027 cases and the five Ohio cases have no model account (a cent each would settle them; not
sent); the matching and eligibility readers split along family lines on ten question-draws; what fixing a mechanism could open is read case
by case against the other differences the eligibility readers recorded, not re-read by readers and not measured.
