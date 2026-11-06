# Split extraction, version 2: what the first 100 items got wrong, why, and what changed (2026-11-05)

Alex, 2026-11-05: "好，从重复开题开始做;你自己解决当前的所有问题，我要你看prompt, trace, 然后好好看问题为什么错，确认尺子和你量测方法没有本质问题，然后开始解决这些问题；我们这次抽取分开成证据和新题目应该要有更好的效果，这个是目标，你要在前100个sample run 里面吧我们的现在的问题解决，然后不要drift from current proto".
Mid-work, on the review prompt: "what is the review prompt tell me make sure you are not makeing mistake".

Scope: the experimental split path in this worktree (A finds new questions, B files evidence under existing ones, record preparation, Jev
matching with the analyst review, the real writer and daily judging). The prototype's shape is unchanged; the production replay default,
the frozen ruler (AGENTS §7.1) and the stopped run's data are untouched. Predictions written before the run: `split-v2-predictions.md`.

## 1. The ruler and the measurement

- **The ruler is sound for this.** The signed standard (`docs/prd/05-extraction-standard.html`, version 5) already says which questions
  open (§3: five reasons; §4: three tests, granularity, the not-to-open list) and when two questions are one (§4 "同一题、续期，还是另一题",
  D248's seven boundaries). D372 sets evidence scoring to helpful / not helpful. Nothing in it needed changing; every failure below is a gap
  between the prompts or code and that text.
- **The measurement had a gap.** The first-100 review counted duplicates and dropped records but never asked whether each new question should
  exist at all under §3–§4. Read against the standard, about 15 of the 35 new questions should not have opened (a DLSS feature, a game
  benchmark, one county's moratorium, a layoff, a war's escalation, a customer's GPU plan, a share for 2028, a small tax incentive). That is
  the largest class and is now measured: each new question of both runs is read by a blind reader against §3–§4 and D248.
- golden-v5 covers July articles; these 100 items (08-29 to 08-31) have no gold. Here the measurement is the class census by code plus a
  blind reader; it shows mechanisms on one draw, not a score.

## 2. Classes found on the first 100 (stopped run `split-fresh-seven-day-matching-v4`, 76 article items, 35 new questions)

| # | Class (count) | Example | Mechanism (traced) |
|---|---|---|---|
| 1 | New questions the standard does not open (about 15) | v74 DLSS 5 on RTX 40, v77 Effingham County, v80 US–Iran, v93 AWS's GPU plan, v87 share in 2028 | A's prompt paraphrased the standard loosely: "is not automatically a new question" (an abstract clause) instead of the closed five reasons and the not-to-open list the production prompt v74i carries; the code checks the standard gives code (year limit) were not run on A's questions |
| 2 | Subject filed wrong (about 12 of 21 unlisted) | three Fed questions under three invented subjects; HF acquisition as a "theme"; TSMC capex under a new company | record preparation was asked for the subject but never shown the subject list (A was); free text such as "Federal Reserve benchmark interest rate" did not resolve and became a new research subject |
| 3 | Numeric questions without a ladder (16 of 16), so never judged | v73 FY2028 revenue growth, v85 CPU revenue, v101 Broadcom AI revenue | record preparation: "use five intervals only when a meaningful reference and boundaries are supported; never invent an article claim" read as "always skip"; the production ladder rules were absent |
| 4 | A's evidence without the evidence standard (mean 6.2 passages, max 30) | v80: every paragraph of a war op-ed; v70: NVIDIA's revenue "illustrating why a policy risk could matter" | A's prompt said "include every helpful passage", with no closing check; B had the standard's full not-kept list. Two rulers in one pipeline |
| 5 | Duplicates (3 confirmed, 2 likely) | v90 = v85 (FY2028 CPU revenue, same CFO figure); v100 = v82 (Fed September decision); v88 = v5 (hyperscaler 2027 capex) | Jev's 0.5 cut kept the old question from the review (v85 at 0.49, v64 at 0.45, v109 as "other period" 0.69); the review split coarse/fine readings and named-scope variants; for v90 A had v85 in view and wrote "server and stand-alone scopes differ" |
| 6 | Quote refusals (5) | 1246 "Nvidia's" for "The company's" lost the cancellable-commitments condition; Xiaomi "year‑over‑year" | the split quote check passed no subject names (production's sift does, D266); hyphen glyphs U+2010/U+2011 were not compared as "-" (187 of 34,084 corpus articles carry U+2011) |

Not changed: B's prompt (only the all-open context reaches it); B's misses are a separate class to read after this run. MediaTek (1285) is
outside the first 100; its re-proposal came from the hidden context (fixed by all-open) and B's omission is a retold announcement.

## 3. Changes, each with its source and its proof before the run

| Class | Change | Source | Proof on stored data |
|---|---|---|---|
| 6 | `source_quote` passes the item's subject names to the existing repair and compares U+2010/U+2011 as "-", returning the exact source text | production `extraction.sift` (D236, D266) | all 1,251 stored A/B quotes: refusals 12 → 9, the 3 recovered are the cases above, 0 accepted passages changed, every result is source text |
| 2 | record preparation is shown the subject list; `object` is an enum of listed ids or `new` (with a name); the kind follows the subject | AGENTS §2 code owns identity; v74i's asset/theme sentence | 36 stored questions re-sent once: 34 on the right subject (was about 15); left: US–Iran as new, robot-chip export controls under NVDA |
| 3 | record preparation carries v74i's ladder and numeric-bound sentences; empty only when there is no reference | role-v74i "How to write a candidate thesis", "numeric bounds" | same send: numeric ladders 0/17 → 10/17, all accepted by `check_ladder`/`check_bounds` |
| 2/5 | a theme quantity summed over a calendar year (spend, capacity, market size) gets the D197 key; code decides its identity | standard §3 D, D197 | five-hyperscaler capex → `ai-capex` spend_total 2027 → code merges into v5 ($0, real ledger copy) |
| 1 | A's prompt carries the five reasons with cross-industry examples and the not-to-open list; a numeric question for the year after next is dropped by code | standard §3–§4; v74i "Which questions to propose"; 06-views ladder rule 5 | 21 items once: 10 of 13 junk-opening items open nothing; of the legitimate 8, AWS and CPI not opened because the articles hold no AWS or CPI figure (model account), FY2028 server CPU missed once (the model says it should have opened it) |
| 4 | A's evidence passes the same closing check as B (the frozen review rows appended to A's request); background goes in why_it_matters | standard §5; AGENTS §7.1 one ruler | same send: v80's 30 passages → no question; passages per question now 1–8 |
| 5 | A names its closest existing question and the result that separates its question (D248's test); that question always reaches the review | D248 general rule | 1253 no longer proposes the CPU duplicate |
| 5 | the review sees every open question Jev calls the same, a part or the same quantity for another period, at any probability | D190 (Jev reads wording), D258 | stored Jev answers: reviews 32 → 39, pairs 42 → 66; the added peers include v64, v85, v109 |
| 5 | collision-v4: a coarse or fine reading of one outcome is one question; a scope is separate only when the texts show its own figure; a later deadline of a one-off event is the same question, another period of a recurring quantity a succession; relation definitions in the schema (v4 only) | D248 items 1–2, standard §4 "另一种口径" | 13 pairs × 3 sends (`poc/data/collision-v4-probe-2026-11-05-r2`): CPU 3/3, RTX 3/3, Fed 2/3, HF 2/3 merged (v3: 0/3–3/3); all 8 must-stay-apart pairs 3/3 apart. A first draft with a rate example merged Fed year-end into the September meeting once; replaced by a cross-industry example |

Regression found and removed before the run: a field description on A's quote ("copied character for character") made the model write
article text into the question field in 4 of 6 sends; without it 0 of 6 (`poc/data/a-v2-variants-2026-11-05`). Quote fidelity is held by code.

Prompt sizes: A system 3,273 → 4,834 characters (the standard's five reasons and not-to-open list replace one abstract sentence; the
closing check, about 6,600 characters, is appended to A's request so both calls use one evidence ruler); collision 1,235 → 1,862.

Tests: `tests/test_unkeyed_collision_matching.py` (+6: a 0.49 part, another-period and low same proposals reach the review; the named closest
question reaches it; a different proposal does not; v4 alone carries relation definitions, older requests unchanged), mutant restoring the
0.5 rule fails 4 of them; `test_split_v2.py` (9), mutant without subject names and glyphs fails the quote tests. Spec changes recorded here:
an unsourced candidate is dropped with its reason instead of stopping the run (production parity, D209); A's answer names the closest question
instead of a free reason. Suite: 247 passed, 61 skipped; frozen rulers unchanged.

## 4. First run on the first 100 (`poc/data/split-v2-first100-2026-11-05/`, about $0.6) and the blind reading

Census by code (`census_first100.py`), stopped run → this run: new questions 35 → 22; filed under an invented subject 21 → 0; passages per
new question from the opening article 6.2 (max 30) → 2.0 (max 6); dropped records 13 → 4 (quote refusals 5 → 1, no home 8 → 3); numeric
questions with an accepted ladder 0 of 16 → 9 of 20; questions judged in the two days 16 → 9 (fewer questions; the numeric ones with a
ladder are now among them).

Blind reading (Codex read-only, both runs' questions shuffled under neutral ledger labels; keys held outside the readers' folders; the
first launch was stopped within seconds when the keys were found beside the packets, and relaunched clean): questions the standard does not
open, duplicates included: 24 of 35 → 3 of 22 (duplicates 3 → 1: core against headline PCE, which I read as two separately watched figures).
The reader also rejected the stopped run's TSMC 2 nm and robot-chip export-control questions (no production start or pending decision in the
source), so neither is a loss. Sampled opening passages helpful: 9 of 30 → 18 of 30 (the rest: context filed under the wrong new question,
such as a revenue guide under a gross-margin question); passages under existing questions 21 of 30 → 21 of 30 (that call did not change).
Broadcom: 15 passages → 1; the old 15 held 2 helpful statements and 13 risk lists; the new one kept the full-year guidance and missed the
third-quarter guidance.

Not caught by the reader, found in the trace: the Hugging Face acquisition opened again with a later closing date (1256); the review merged
the same pair at 1248 and kept it apart at 1256, a coin flip measured as 2 of 3 in the pair probe.

Traced against the prediction it missed (ladders, predicted at least 60%): of 11 empty ladders, 5 had no reference in their evidence and 6
had only a quarter's or part-year figure, which the sentence "the reference the source or evidence gives" did not cover.

## 5. Changes for the final configuration

| Class | Change | Source | Proof |
|---|---|---|---|
| duplicate deal | A: "One deal or one programme is one question: its agreement, approval and closing are steps of it"; review example "(the agreement, approval and closing of one deal)" | standard §4 "约束性义务：'一笔或一个计划'一题" (D210) | A on 1248 and 1256, twice each: 0 proposals (before: proposed at 1256); review pairs: 8 of 8 must-stay-apart pairs 3/3 apart |
| ladders | the reference may be the full-year pace a quarter's or part-year figure implies, said so in the condition | PRD 06 ladder rule (state the neutral comparison); D-unnumbered "conditional on available information" | 6 of 6 part-period questions get an accepted ladder with the pace named; 3 of 3 without a reference stay empty |
| quotes | a quote whose words equal the source passage's is that passage at any length; an em dash closed up to a word compares as a space | D236 (punctuation is not a change) | stored quotes 12 → 8 refusals, 0 accepted passages changed; test with a changed number refused |

One reading choice to report to Alex: the part-period pace as a ladder reference is a derived figure, stated as such in the rung, not a
sourced figure.

## 6. Final and confirmation runs

| Measure (first 100 rows) | Stopped run | First v2 run | Final run | Confirmation run |
|---|---|---|---|---|
| New questions | 35 | 22 | 13 | 22 |
| Blind reader: should not open (duplicates) | 24 (3) / 22 (3) / 21 (2) in the three passes | 3 (1) | 1 (0) | 3 (0) |
| Filed under an invented subject where a listed one fits | about 12 of 21 unlisted | 0 | 0 | 1 (Hormuz oil under a new subject, not middle-east-conflict) |
| Numeric questions with an accepted ladder | 0 of 16 | 9 of 20 | 9 of 12 | 15 of 21 |
| Passages per new question, mean (max) | 6.2 (30) | 2.0 (6) | 3.5 (11) | 2.8 (10) |
| Sampled opening passages helpful (blind, of 30) | 9 / 10 / 8 | 18 | 18 | 18 |
| Sampled existing-question passages helpful (blind, of 30) | 21 / 23 / 21 | 21 | 22 | 16 |
| Quote refusals | 5 | 1 | 5 | 1 |
| Second Hugging Face question | — | opened | not opened | not opened |

The final run's two misses were traced before the confirmation run (§5 of the predictions): the quarterly sentence read as "a quarterly
figure forbids an annual question" (model's own account, two items), and two quote gaps. The confirmation run met its predictions except one
invented subject. It also showed one defect of my own: the year limit read a fiscal year that record preparation wrote as a bare "2028" as a
calendar year and dropped "FY2028 total revenue growth" (1207). Fixed afterwards: the fiscal year the question names sets the limit
(`question_year`); replaying every stored handover of the three v2 runs changes only that question.

Existing-question passages: B did not change across the v2 runs; its sampled helpfulness moved 21–22 → 16. The 14 unhelpful ones are
statements filed under a company's total-revenue question with no specific link (NVIDIA FY2027 four times, and the new TSMC and ON
Semiconductor revenue questions): the evidence call's fallback sentence (D273, kept by D361) sends a demand, supply or competition statement
with no specific question to the company-wide revenue question of its period, so every new total-revenue question becomes another place to
park. This is PRD 10's core blocker, not a change made here.

Residuals, each one a run: a derived share that no public material reports ("share of revenue from customers it financed") opens in every
run; one market-share question without source support; one shared quantity filed under a new subject. The seven-day run stays stopped;
production defaults and the frozen ruler are unchanged.
