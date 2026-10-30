# Extraction quality beyond the ruler, role-v51 (2026-10-30)

Alex, after D246: "现在到底质量怎么样你深度的解析不要只是看尺子，我需要知道离产品上线还差多少".

## What was read

- Run P, role-v51 (`poc-v67`), 148 articles (development 118, test 30), three draws: a field census over all 444 answers
  (`census.py`, `date_census.py`, the number checks in `number-flags*.json`), at no cost.
- A seeded random sample of 24 articles (19 development, 5 test; seed 20261031, `sample.json`), draw 1 only, because
  production sends each article once. Four independent readers (Claude subagents that never saw the gold, the prompt or a
  score; `reader-prompt.md`) read each article whole as an analyst covering NVIDIA and judged every kept record (worth,
  summary line, original speaker, original day, source tier, duplicate), listed misses and questions (`verdicts/`). The
  readers' verdicts were then set beside the frozen gold (`aggregate.py`, `aggregate.json`). Six reader claims were
  checked against the article text by Claude (Groq quotation marks, the Palantir copy error, the Bleeding Edge dates,
  the Sharon/Firmus tiers, the Cramer page, the backstop dates): all held. Model readers are labelled as such (AGENTS §7.1).

## What the ruler measures, and holds

| Measure | role-v51 |
|---|---|
| Core kept per draw, development | 77, 77, 81 of 86 |
| Core matter in all three draws / supporting | 89% / 86% of their statements |
| Gold-rejected statements in all three draws | 53% (the noise is what changes between draws) |
| Numbers in a summary line absent from its quote | 55 of 2,065 flagged; all read: context from the next sentence, none invented |
| Statements per draw, development: v23 → v29 → v42 → v51 | 833 → ~620 → ~535 → ~534 |
| Gold-rejected kept per draw: v29 → v42 → v51 | ~135 → ~102 → ~100 |
| Cost and time per article | 4.7k input, 1.3k output tokens, about $0.0011 at $0.10/$0.50 per million; median 12.5 s, p90 22 s |

## What the ruler does not measure (readers, 24 articles, 102 records, one draw)

| Finding | Count |
|---|---|
| Grades: A usable as is / B minor defects / C a material defect / D misleading | 4 / 10 / 10 / 0 |
| Records worth keeping / marginal / noise | 27 / 33 / 42 (9 of the noise on one page, the Singapore mansion) |
| Original day wrong (the report day for an earlier or undated event) | 36, on 10 of 24 articles |
| Source tier wrong (officials' charges as third-party view, announced company plans as rumour) | 14 |
| Original speaker is the reporter (SemiAnalysis, TechRadar) instead of the company | 12 |
| Summary line loses a hedge or condition or says more than the quote ("acquisition" of Groq in quotes → acquired) | 12 |
| One event split into several records (one Reuters rumour as three) | 11 |
| Records with at least one field error | 52 of 102; 17 of the 27 worth keeping |
| Questions opened / judged sensible | 3 / 3 |
| Questions missed | 2: NVIDIA credit-support obligation (opened in 2 of 3 draws on that page), the $12.9B Hugging Face acquisition (0 of 3) |
| Reader misses against the gold | 8 medium or high; 5 of them gold entries; the gold misses 4 the readers want (backstop terms, revenue share, consensus too low) and keeps 2 the readers call noise |

The field errors are not cosmetic downstream: the writer and the judge read the original day to tell old news from new
(D203), and an outlet named as the original speaker makes one company announcement look like several independent
sources (the matching defect "another document's copy of the same figure judged new").

Question recall counted per question rather than per article, on stored data: of the 6 distinct must-open questions of
the development set, each draw opens 4 or 5 on at least one article (the DRAM contract-price question never; the OpenAI
Ohio lease in 2 of 3); of the 3 on the test set, 1 to 2 (total revenue opened where the gold asks data-centre revenue;
Hugging Face never). The test set holds 9 core entries and 3 must-open questions, too few to say more than "no sign of
overfitting".

## Standard doubts the readers raised (for Alex; nothing changed)

1. "Unknown, never the report day" loses the bound "said on or before the report day" (three readers). Not a loss: every
   record keeps its item's publication day separately, so the bound is already stored.
2. D240's unsized named actions keep every small press release and logo list (low weight, but each is a record).
3. D231 makes the Singapore case optional, so eleven records on a defendant's assets cost nothing.
4. The tier table has no row for an official's allegation, a company forecasting its own industry, or a research firm
   reporting a non-public action as fact.
5. D243 #6 keeps a repeated old figure at full weight each time, while AGENTS §8 says a repeat is not new evidence
   (matching stores it as `same_claims`).
