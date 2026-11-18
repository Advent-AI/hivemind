# F6: the shared quantity's due day — the $0 source audit and a design for the council (D461), 2026-11-13

**Answer: the date sentence is a recurring reason the clean Step 1 declines a shared price, a real settling date exists for the declined
cases, and a later step already sets that date by code; one sentence can be corrected without inventing dates.** Nothing is changed or
sent before the council's review.

## The sentence (c8 system prompt, `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt` lines 112–115)

"Give the date the item supports. When it gives none, use the date the reason fixes and say how it was set: an obligation already
undertaken, its next annual report; an unsigned obligation, a check date within 18 months of the item; a pending regulatory decision, the
current fiscal year-end. **A shared quantity takes its release date and a product event the date its outcome can be checked, only when the
item supports one.** A question no date can settle is rewritten or not opened."

## The standard and the decisions

- §3: "到期日：量是它的发布日；事件是能判出结果的那天"; class D's settling material: "几家公司年报、统计发布、官方决定".
- §4 "能核对": "有一个日期和一份公开材料能把答案放进事先固定的档吗？没有就重写问题". §4 "原文支持": the subject, the quantity or event and the
  time basis are found in the source; the researcher's check date applies to undated regulatory decisions and unsigned obligations. Neither
  line asks the item to give a quantity's publication day.
- D414 (Alex: "由程序统一定"): in the clean path's ladder step, code sets a theme figure's due day at the calendar year-end plus 90 days unless
  the topic or item states one. D417 (Alex: "确认：这类题不出题"): a figure that is not one year's and has no stated publication day is declined
  there.
So the sentence asks Step 1 for a day the standard does not ask the item for and that the ladder step sets by code.

## The class, counted on stored data ($0)

| where | sends that opened no memory-price question | of them, the reasoning weighs the item's missing date or series | hand read |
|---|---|---|---|
| u2 (d2, steps 56 and 90) | 1 draw | yes: "the item gives no specific price/period. Too vague"; "no specific price/date; tangential for NVDA; the article is Micron-centric" | read |
| u3 (d3, steps 47 and 90) | 1 draw | yes: "Could be 'DRAM contract prices in 2026' via TrendForce. But the item doesn't support a specific date/series" | read |
| D441's memory diagnostic, c8 (`poc/data/clean-step1-gate2-memory-completion-2026-11-13/combined-records.jsonl`) | 26 of 54 | 22 by a pattern over the stored reasoning; 16 of them also call it not material | 5 of 6 random sends weigh it ("the rule says shared_quantity takes its release date. The item doesn't give a clear release date"), always beside other reasons |

The settling date exists for every declined case: a calendar year's contract-price figure is published by the statistics releases the
model itself names (TrendForce/DRAMeXchange), and D414 fixes the ladder's day for it. The sentence is weighed in most declines but never
shown as the only reason (materiality and the item's lack of a price level appear beside it).

## The change (one sentence, at its place)

Before: "A shared quantity takes its release date and a product event the date its outcome can be checked, only when the item supports one."

After: "A product event takes the date its outcome can be checked, only when the item supports one; a shared quantity takes its year's
release date, which the item need not give."

Characters: 130 before, 170 after (+40); the growth's reason: the two date rules are separated so that the product event keeps its
condition. Nothing else changes. The period itself still needs the item's support ("for this or next calendar year"; §4 "原文支持"), so a
rolling window still has no year and stays declined (D417).

## Expected effect, and on the final judgement (D391)

More sends open the memory-price question on the memory articles, with the period the item supports; the ruler's q05 ("How will server DRAM
and HBM contract prices in calendar 2027 compare with calendar 2026?") becomes matchable in more clean draws (none of six so far). More
questions alone are not success: the test counts questions in a shape the ladder step can build and the judge can answer.

## Falsifiers (any one stops it)

1. The candidate opens no more memory-price questions than c8 on the memory articles (the effect is not there).
2. The share of opened memory questions in the 2027 or 2026-to-2027 shape falls (D441's regression: c8 13 of 28).
3. It invents days: a stated due day the item does not support and the reason does not fix, or a rolling window opened as a year.
4. It opens shared quantities the ladder step must refuse, or small ones, on the neighbouring articles (the H100 rental price, the China
   domestic-share survey) more often than c8.
5. It moves the capex or Ohio outcomes on their articles (it must not: the sentence does not touch them).

## Test (proposed, for the council)

On stored before-states, c8 against c8 with the one sentence (arm c16), deepseek-flash as stored: the memory article in the three D441
states (18 sends a side a state, as D441), and three sends a side a state on the neighbours (H100 rental, the China survey, the capex
article, the Ohio article). Before any send: the candidate request rebuilt byte for byte except the sentence, a synthetic answer through
every check, preflight, a whole-request audit of the changed sentence with a blind reader, the lines above written and frozen with their
sha256. About 180 sends, about $3.6 at the published rates (D441's sends cost about $0.02 each); ceiling $5; spend under D439 then about $22
of $40. The memory article is F6's own motivating case and also D441's regression case: the council decides whether it may carry the test
or only guard it, with fresh articles for acceptance.
