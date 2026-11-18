# Claude's own read of the 22 answers, stored before any reader's answer (2026-11-16, about 22:20 PST)

Run: `poc/data/clean-carried-library-2026-11-16/reads/` (22 of 22 complete, one call each, ledger $0.427 of $1.00). Layout:
`read_probe.py` → `reads-layout.json`. Every answer read beside its article's kept statements and the topics it opened.

## The frozen reading (DESIGN.md), as written

| Labelled case (October topic) | Empty read | Carried read | Mark |
|---|---|---|---|
| Supply commitments (art. 9), same question | opened its own commitments question | no new question; the $279bn filed under September clean-2 | as intended |
| Hugging Face (art. 30), same question | opened its own closing question | no new question; filed under September clean-6 | as intended |
| Rubin's ramp (art. 76), same question | opened "ramp on schedule or slip into 2027" | no new question; both Rubin statements filed under September clean-4 | as intended |
| Capital spending 2026 and 2027 (art. 15), same question for 2026 | opened a 2026 question (five companies) and a Rubin question | no new question; the $800bn / $1.3tn sentence filed under clean-5, Rubin under clean-4 | as intended; 2027 opened in neither read |
| The lease guarantee (art. 9), related | opened "the SB Energy guarantee exposure" | filed under September clean-1 (the total) | no second question; a signed guarantee is part of the total (D390) |
| The loss-share support (art. 76), related | opened "credit support to customers' financing" | filed under clean-1 | no second question |
| The U.S. licence (art. 35), unresolved | opened nothing | two statements filed under clean-3 (Blackwell sales to China) | right home, I think |
| Global AI spending (art. 206), unresolved | opened "global AI spending = 2.5% of U.S. GDP in 2027" | no question; Goldman's figure filed under clean-5 (the big five's spending) | a neighbouring home, arguable |
| Memory prices (art. 12), absent | **opened nothing** | opened an HBM/DRAM 2027 price question | carried opened, empty did not |
| Groq's rack (art. 119), absent | opened the rack question and a DOJ/FTC action question | opened the rack question only; lawsuit and probe kept, filed nowhere | the DOJ/FTC question lost: worth it? unsure |
| B200 rental price (art. 173), absent | opened | opened | same |
| Reflection AI (art. 200), absent | opened (sign) | opened (sign and complete) | same matter |
| Equity-investment commitments (art. 235), absent | opened a guarantee-exposure and an equity-commitments question | **no question**; the $25bn commitments, the $99bn balance and the net purchases filed under clean-1 | clean-1's own outcome names "versus the equity investments it has made", so the filing follows the topic as written; a question the empty read opened is not opened |

**By the rule written before the run:** re-opened the same question in 0 of 4 same-question cases (fails at 2); the matter's
statements filed under the existing question in 4 of 4, as many as the empty read kept (1, 1, 2, 1 against 1, 1, 2, 1);
absent cases opened: empty 4 (Groq, B200, Reflection, equity commitments), carried 4 (memory, Groq, B200, Reflection), of the
empty read's four the carried read opens three (fails at two or fewer). **It supports going on.**

## Counts (one draw; not the rule)

| | empty | carried |
|---|---|---|
| topics opened | 16 | 4 |
| statements kept | 74 | 72 |
| statements filed under some question | 34 | 37 |
| statements filed nowhere | 40 | 35 |

## What I would flag for the readers

1. The equity-investment commitments: not opened with a library present, because the existing topic was written as "credit
   support versus equity investments". The September topic's two-thing shape carries over: a library passes its faults on.
2. The DOJ/FTC question on the Groq deal: opened only from empty; the stored October run did not open it either.
3. Homes I am unsure of: Goldman's global AI spending under the big five's spending (206 e6); customers' share of receivables
   under credit support (173 e3); the CFO's 70% growth under supply commitments (206 e3, which D508's readers counted as
   bearing on that question).
4. The empty reads themselves differ from the stored October run (article 12 opened nothing, 35 nothing, 15 a 2026-only
   question): the run-to-run variation D559 found, again.

**Not shown by this:** final answers; any rate; whether the carried library's own questions are good (they are one week of
the same system from empty); what happens over many weeks.

## Correction after the council (round 4, `../reflection-4/council-codex-4.md`)

"It supports going on" above is wrong by the rule as written: its positive condition needs the absent cases to open as in
the empty read, and the carried read opened three of the empty read's four. The result sits between the positive condition
and the failure line and is reported as it is (`RESULT.md`).
