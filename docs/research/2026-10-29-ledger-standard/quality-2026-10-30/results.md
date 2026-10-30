# Extraction quality beyond the ruler, role-v51 (2026-10-30)

Alex, after D246: "现在到底质量怎么样你深度的解析不要只是看尺子，我需要知道离产品上线还差多少".

## What was read

- Run P, role-v51 (`poc-v67`), 148 articles (development 118, test 30), three draws: a field census over all 444 answers
  (`census.py`, `stability.py`, the number checks in `number-flags*.json`), at no cost.
- A seeded random sample of 24 articles (19 development, 5 test; seed 20261031, `sample.json`), draw 1 only, because
  production sends each article once. Four independent readers (Claude subagents that never saw the gold, the prompt or a
  score; `reader-prompt.md`) read each article whole as an analyst covering NVIDIA and judged every kept record (worth,
  summary line, original speaker, original day, source tier, duplicate), listed misses and questions (`verdicts/`). The
  readers' verdicts were then set beside the frozen gold (`aggregate.py`, `aggregate.json`). Model readers are labelled as
  such (AGENTS §7.1).
- **Verification (after Alex: "那你找到的这些问题验证是真的问题吗？").** Claude read every one of the 127 reader flags on the 81
  flagged records against the article text, and the 21 unflagged records, and gave each a verdict (`adjudication.py`,
  `adjudication.json`; the rule for the date and speaker fields is in its header: the request asks for "the original speaker
  and statement day" of a retelling; judging and matching read `original_who` and `original_day`; `event_time` is read by no
  step). The counts below are the verified ones; the readers' raw counts are kept beside them.

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

## What the ruler does not measure (24 articles, 102 records, one draw; verified by Claude)

| Finding | Readers flagged | Verified real | Not real or debatable |
|---|---|---|---|
| Original day wrong | 36 | 12 material (an announcement of June dated July 6, a September reveal dated October 17), 8 low (a company announcement dated the day a news story covered it) | 10 only `event_time` (read by no step), 4 misread (the outlet's own claim dated its report day; a month-only date left empty per D203), 2 debatable |
| Original speaker is the outlet instead of the company or official | 12 | 12 (and 1 more the readers missed) | 0 |
| Source tier wrong (an official's charges as a third-party view; an announced company plan as a rumour) | 14 | 9 | 5 debatable (a company forecasting its own industry; a TV host's paraphrase) |
| Summary line loses a condition or says more than the quote ("acquisition" of Groq in quotation marks written as an acquisition; "the item gives no date" where it says 2025) | 12 | 11 | 1 (a period label copied from the article) |
| One event split into several records | 11 | 9 | 2 debatable |
| Records worth keeping / marginal / noise | 27 / 33 / 42 | noise: 42 of 42 agreed | 0 |
| Records with at least one field error | 52 | 30 (35 with the low date cases) | — |
| Grades: A / B / C / D | 4 / 10 / 10 / 0 | not re-graded | — |

Questions, read from the candidates themselves (not the counting aid):
- Development set, distinct must-open questions: the credit-support obligation, the hyperscalers' 2026 and 2027 capex, the Kyber
  shipping date and the China H200 permit are opened in every draw; the OpenAI Ohio lease guarantee never as its own yes/no
  question, but covered in all three draws by the wider lease-guarantee amount question (the counting aid's "2 of 3" is a word
  match on that wider question); DRAM contract prices in no draw.
- Test set: supply commitments in every draw; data-centre revenue for FY2028 asked as total revenue growth in 2 of 3; the $12.9B
  Hugging Face acquisition in no draw (the statement itself is kept in every draw).
- The credit-support question on the Mitrade page opens in 2 of 3 draws (other pages carry it in every draw).
- Must-not: the lidar-legislation question in 1 of 3 draws under role-v51 (role-v42: 11 of 15); one Nigeria production question in
  draw 1.

Quotes code refused, all 28 in three draws, read one by one: 14 stitch parts of different sentences or paragraphs (the
Palantir–Nemotron statement, the China H200 permission, the Palantir classified-environments collaboration); 9 change a word or
two at an edge ("the company" written as "Nvidia", "As a result" as "So", "its" as "Nvidia's"; among them "Nvidia provides a
take-or-pay commitment", a core entry, and "Vera CPU expected to bring $20 billion"); 2 are titles that are not in the body; 1
skips words with an ellipsis; 1 writes "85 percent" as "85%"; 1 is a real misquote the check rightly caught ("Nvidia's" for
"Micron's").

The verified field errors are not cosmetic downstream: the judge and the matcher read the original day and speaker to tell old
news from new (D203), and an outlet named as the original speaker makes one company announcement look like several independent
sources (the matching defect "another document's copy of the same figure judged new"). They concentrate on pages that retell
earlier announcements (7 of the 12 material date errors are on the SemiAnalysis backstop page).

The test set holds 9 core entries and 3 must-open questions, too few to say more than "no sign of overfitting".

## Standard doubts the readers raised (for Alex; nothing changed)

Read by Claude; each points at a real gap or tension in the page and none is decided.


1. "Unknown, never the report day" loses the bound "said on or before the report day" (three readers). Not a loss: every
   record keeps its item's publication day separately, so the bound is already stored.
2. D240's unsized named actions keep every small press release and logo list (low weight, but each is a record).
3. D231 makes the Singapore case optional, so eleven records on a defendant's assets cost nothing.
4. The tier table has no row for an official's allegation, a company forecasting its own industry, or a research firm
   reporting a non-public action as fact.
5. D243 #6 keeps a repeated old figure at full weight each time, while AGENTS §8 says a repeat is not new evidence
   (matching stores it as `same_claims`).
