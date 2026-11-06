# E1 diagnosis: helpful statements production writes and then drops as "no home" (2026-11-06)

PRD 11, E1, step 1 ($0 reading plus $0.02 of model-account probes). Alex chose E1 on 2026-11-06. Nothing in production changed.

## Question

PRD 11 asked: for every helpful gold matter that frozen production (poc-v108) wrote and then dropped, is it a **link miss** (an open question
takes it under the links rule as written, the company-wide revenue fallback included) or an **opening miss** (the question that would take it
does not exist)? The larger class picks the experiment.

## What was read

- Population: the benchmark readers' verdict "written, then dropped by a code check" on production's missed helpful matters, in the three
  same-day window draws and the three test-article draws (sealed worktree, `results/miss-*-control.out`): 96 dropped draws of 57 matters
  (38 window, 19 test; 7 core, 50 supporting). 92 draws were "no home"; 4 were quote refusals. The other no-home drops (the 441 counted in
  PRD 11 include statements the gold does not list as helpful) were not read here.
- For each: the gold entry, the source paragraph, the dropped statement as the model wrote it, the answer's own proposed questions, and the
  exact block of open questions with their "takes" lines from the stored request (`packet.json`, `build_packet.py`).
- Claude classified all 57 (`labels-claude.json`). A blind Codex reader classified the 54 that were not quote refusals from
  `reader-packet.json` (no labels, no gold weight), with the links rule as the model read it and the standard page
  (`reader-prompt.md`, `reader-answer.json`). A third class was needed: **none**, where no open question takes it and the standard would open
  none for it (its §6: no home, dropped).

## Result

Classes stand where both readers agree (44 of 54); the rest are disputed (`tally.py`, `final_labels.json`):

| Class | Matters | Core | Window draws | Test draws |
|---|---|---|---|---|
| Link miss: the question's own quantity in another period or quarter, or a variant or stopgap of a tracked product | 12 | 4 | 13 | 3 |
| Link miss: an indirect relation (a seller's revenue for buyers' spending, memory supply for memory prices, demand signals) | 5 | 0 | 6 | 0 |
| Disputed: all ten sit on the company-wide revenue fallback or the indirect clause | 10 | 0 | 8 | 7 |
| Opening miss: the question does not exist | 3 | 1 | 0 | 6 |
| None: a small matter no question takes and none should open | 24 | 0 | 29 | 20 |
| Quote refused by code (not a filing question) | 3 | 2 | 4 | 0 |
| Total | 57 | 7 | 60 | 36 |

- **Link misses outnumber opening misses** (17 agreed, up to 27 with the disputed, against 3). The one core opening miss is the Hugging Face
  acquisition (about $12.9 billion, a must_open binding obligation; the answer proposed no question). The two others are a may_open OPEC+
  output question; that answer proposed a must_not quota question instead.
- **The largest group is not a loss.** 24 matters are small (an undisclosed investment, a partner integrating NVIDIA software, a gaming card
  rumour, a share-price calculation, the capital-return policy): the standard's §6 drops them. In the draws where production kept one, it was
  filed under the total-revenue or Data Center question, the parking lot PRD 10 §2 describes.
- **Link misses are mostly coin flips.** Of the 17 agreed link misses, 12 were written and filed in another draw of the same day (the
  question each was filed under there is not checked here).

## What the product lost

The ruler counts one matter in one article (D250); the product needs the fact once. For each window draw that dropped a "fence" fact, the
same draw's ledger was searched for the fact filed under a question that takes it (`product_coverage.py`): 5 of the 13 dropped draws had it
from another article (the Q2 revenue guidance of $91 billion reached the total-revenue question from seven other articles in the draw that
dropped one copy; NVL72x2 and NVL576 reached the Rubin Ultra question). The 8 that were lost are estimates for a period the question does not
cover (FY2028 EPS consensus in four draws for the FY2027 EPS question, 2028 and 2024–2029 AI capex for the 2026 and 2027 capex questions, a
custom-ASIC growth rate through 2033 for the 2026 custom-silicon question) and one component slip (CPO-NVSwitch to Feynman, for Rubin Ultra).
The window judgement does not show a loss tied to them: those questions agree in every control draw, except custom silicon (v16) in draw 2,
where the ASIC growth rate and Broadcom's AI revenue were both dropped; that is a coincidence in one draw, not a shown cause.

## Mechanism

- The model's own account (`probe_empty_links.py`, `model-account.md`; 10 cases, 2 sends each, 181,784 input and 3,331 output tokens, at most
  $0.020 at the published rates): in all 20 answers it says no instruction justified the empty links and names the question the readers
  named. Its reason is the same each time: it read the question's own period ("FY2027"), population ("cloud providers") or named
  configuration ("Kyber NVL144") as a boundary. The rule says an estimate for another period is filed under the question, and the Rubin
  Ultra line lists "variants and stopgaps".
- **Caveat:** the probe named the question ids, which leads the answer (PRD 10 log row 7). It locates the reason; it does not show that
  asking again repairs the filing. A neutral re-filing in that row filed about half of the needed facts and also put noise back under the
  total-revenue question.
- Where the request carries it: each numeric question's line, written by code (`placement.takes`), names the question's period; the
  allowance for other periods is stated once, in the links field's description, by design ("stated once, in that rule, not repeated under
  every numeric question", D274, D268).

## Prior evidence on the same mechanism

- PRD 10 §3: a filing re-check at the end "recovers some, and misfiles about as many"; a general "the other party's figure counts" sentence
  moved facts to the wrong questions. §8 step 5: the closed-set links rule v74l (it covered "the question's own figure" and "variants and
  parts", and also deleted the fallback) failed its one test.
- PRD 11 §1 stated E1 as "production's largest recall loss in the benchmark". On the window that is not so: the readers put 116 of the 213
  missed draws down as "the model did not write it" and 60 as dropped by a check; on the test articles 36 of 68 were dropped, 29 not written.

## Measurement concern (recorded, the gold unchanged; D373)

24 statements the gold counts as helpful are statements the standard's own §6 drops when no question takes them. When production kept such
statements, they were parked under total revenue. The frozen gold and its scores stay as they are; this is disclosed with E1 results.

## Files

`extract_verdicts.py` → `dropped-verdicts.json` → `build_packet.py` → `packet.json`; `labels-claude.json`; `build_reader_packet.py` →
`reader-packet.json`; `reader-prompt.md` (it names the packet's scratch path at the time of the read) → `reader-answer.json`; `tally.py` →
`final_labels.json`; `product_coverage.py`; `probe_empty_links.py` → `model-account.md`. The scripts read the sealed worktree's runs, which
are on disk only (its `data-on-disk.md`).
