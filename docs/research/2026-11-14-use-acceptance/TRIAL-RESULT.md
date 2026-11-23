# The use-oriented acceptance's trial run on stored runs (D484, D485): result, 2026-11-14, $0

**Answer: the readings can be done at a modest workload and gave leads, but their reliability is weaker than a pass: A's calibration holds on
the gold's seven matters, the readers share only 7 of 12 matters; B's planted items could be spotted (each repeated a real item's request) and
one "known supported" control is itself disputed; B's statement check compared summaries with the passages the judge was shown, not with the
articles; C covered only the 62 facts the gold cites, the readers saw the judgement's reasons rather than its request, and with no known
"would change" case its unanimous "no" cannot be told from a reader that only says no.** As leads: both systems opened the seven matters both
readers listed except the Ohio question on the clean path; most judgements are supported; a few extrapolate amounts; four cited statements
carry date or summary errors (to be confirmed against the articles). Council round 6 (`council/mw-codex-6.md`) set these limits.

Material: clean draw c1 and production draw p1 of the full run (2026-07-01..07-14); 40 articles of the frozen gold (it calibrates readers only;
nothing is rescored). Readers: Codex (read-only) and Claude subagents, blind to the systems' names and to each other. Keys outside the
repository. Model cost $0.

## A. Big questions (reading A1: 40 articles; A2: against each system's questions)

| | Codex reader | Claude reader | line (design v3) |
|---|---|---|---|
| gold must_open matters recalled (7) | 6 (missed the DRAM 2027-vs-2026 price) | 7 | at least 3 in 4: both pass |
| articles listed with a gold must_not question | 1 of 27 (a US lidar-ban question) | 0 of 27 | at most 1 in 5: both pass |
| matters listed | 9 | 10 | 7 shared; 12 in the union |

A2 (both families; agree on 21 of 24 cells), each matter against each system's questions at 2026-07-14:

| matter | listed by | clean c1 | production p1 |
|---|---|---|---|
| credit-support / backstop obligations | both | opened | opened |
| Ohio lease guarantee, yes/no | both | **missed** (Codex) / folded into the credit-support total (Claude) | opened |
| hyperscaler capex 2026; 2027 | both | opened; opened | opened; opened |
| Kyber / Rubin Ultra shipping | both | opened | opened |
| China's H200 approval | both | opened | opened (Codex: narrower) |
| Rubin shipping in 2026 | both | opened | opened |
| NVIDIA stand-alone CPU revenue FY2027 | one | **missed** | opened |
| data-center revenue FY2027; FY2028 | one | **missed**; **missed** | in broader total-revenue questions |
| DRAM contract price 2027 vs 2026 | one | opened (Codex: narrower) | **missed** |
| US lidar restrictions (gold: must_not) | one | missed | missed |

The clean path's misses follow its own rule ("Do not open a thesis about … a financial measure's level, growth, margin or guidance for any
period, on its own") and its Ohio fold-in (D388); production's miss is the memory price (D481).

## B. Judgement support (25 items: 21 real last judgements, 4 planted)

| | Codex | Claude |
|---|---|---|
| planted wrong judgements caught | 4 of 4 | 4 of 4 |
| known-supported controls passed (confirmed first by a separate reader) | 3 of 4 | 4 of 4 |
| real judgements (21, the controls among them): SUPPORTED / UNSUPPORTED / INSUFFICIENT | 17 / 2 / 2 | 20 / 1 / 0 |
| families agree on real judgements | 18 of 21 | |

Supported by both families: c1 7 of 9, p1 10 of 12. Unsupported by both: p1's credit-support amount (an assumed one-fifth discount); by one: c1's
credit-support amount (an amount scaled from another deal). Field defects in the 201 statements the real judgements cite: both families flag the same 4 (each flags one more of its own): two statements
dated August 2026 in articles of July 12; a summary naming three firms that its quote calls "its top AI firms"; a summary of a charge filed on
July 6 in an article of July 2. **Flaw:** each planted judgement repeated a real item's request in the same packet; a reader can spot the pair.

## C. Facts that did not reach the judgement (62 reader-B facts in the 40 articles, per system)

| class, by code then read | c1 | p1 |
|---|---|---|
| delivered to a judgement of the matter's question | 31 | 22 |
| never delivered, though judged after it arrived | 8 | 19 |
| — of which linked to another question only | 4 | 19 |
| no judgement after it arrived | 4 | 15 |
| no question on the matter | 19 | 6 |

D456's known cases were found in their class (p1's $3.5bn guarantees linked to the credit-support total, never shown to the Ohio question; p1's
Kyber cancellation linked elsewhere, never shown to the Kyber question). The code's "not extracted" class was checked by hand on every row: most
are sentences the system did not keep while keeping others of the same article; a few need a sentence-by-sentence read.

Reading (37 items: the 27 never-delivered fact-and-system rows, 6 delivered and 4 unrelated controls): **neither family says any undelivered
fact would change its judgement** (Codex: 26 no, 1 cannot tell; Claude: 25 no, 2 cannot tell); both say "no" to every control. With no known
"yes" case among the controls, this reading's power to see a change is **not measured**.

## Workload (for pricing the acceptance's reading)

Per family for the whole trial: Codex about 1.5 million input tokens (mostly cached) and 12,000 output tokens; Claude subagents about 0.9
million tokens; wall time about 25 minutes of reading per family, plus the packet building and Claude's hand checks. Both families read every
item; no reading needed a third reader on more than three items.

## For the acceptance's design (what the trial changes)

- A and B gave usable leads, not a calibration that holds: B's planted items must not repeat a real item's request, and a disputed control is
  replaced; A's matters listed by one family only are reported, not dropped.
- C needs a known "yes" control before its "no" means anything: a fact shown to move a judgement (PRD 10's custom-chip case is one, 9 of 9).
- The clean path's rule against opening the company's own financial lines is a product choice the acceptance will show as misses; it is
  Alex's (D382–D385) to keep or change, not a reader's.
