# The same week, both systems, side by side

Built by code on 2026-11-15 (D517; corrected after the council's review, round 8) from the stored runs of the week of 2026-09-22
to 09-28 (235 articles; each system run once, starting with no questions) and from the stored notes of two independent reviewing
teams (Team A: Codex; Team B: Claude), who read both systems' output without knowing which system wrote it.

- **Printed as stored:** every question, every possible answer with its full condition, each latest answer and its reasons, the
  reviewers' marks and reasons, and (on the second page) every statement an answer cites with its stored passage.
- **Written by hand, and marked so:** which questions of the two systems are on the same subject, and the note on how each such
  pair differs (`shared-subjects.json`; the notes are the council's words, `my-codex-8.md` and `my-codex-9.md`).
- **It ranks nothing and proves no winner.** One week, one run of each system. The reviewers marked an answer against the passages
  the judge was shown, not against the full articles.
- Second page: [`SIDE-BY-SIDE-WEEK-CITED.md`](SIDE-BY-SIDE-WEEK-CITED.md). Builder: `build_side_by_side.py`.

## Front page

The front page is about 3800 words; the entries and the second page are for checking it.

### 1. The five matters both reviewing teams listed, and where each system has them

Each team listed, from 40 sampled articles, the matters worth tracking on their own. "opened" means the system holds a question
on it. The three matters only one team listed are in the table before the entries.

| Matter | Listed by | Old system | New system |
|---|---|---|---|
| M01 NVIDIA fiscal 2027 revenue (total, or its data-center segment, about 92% of it) | both (Codex: total revenue; Claude: data-center revenue) | Team A (Codex): opened (`v2`, `v4`); Team B (Claude): opened (`v2`, `v4`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M02 NVIDIA fiscal 2028 revenue (total, or its data-center segment) | both (Codex: total revenue; Claude: data-center revenue) | Team A (Codex): opened (`v3`, `v5`); Team B (Claude): opened (`v3`, `v5`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M03 NVIDIA fiscal 2028 non-GAAP gross margin against the 72%-73% outlook | both | Team A (Codex): opened (`v10`); Team B (Claude): opened (`v10`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M04 NVIDIA supply and capacity purchase commitments at fiscal 2027 year-end ($279B at Q2) | both | Team A (Codex): missed (no question); Team B (Claude): missed (no question) | Team A (Codex): opened (`clean-2`); Team B (Claude): opened (`clean-2`) |
| M05 Whether Beijing formally approves Chinese firms buying NVIDIA RTX Pro 5500 GPUs by 2027-01-31 | both | Team A (Codex): opened (`v14`, `v15`); Team B (Claude): opened (`v14`, `v15`) | Team A (Codex): opened (`clean-7`); Team B (Claude): opened (`clean-7`) |

### 2. Subjects on which both systems hold a question

The pairing is by hand. Everything in the tables is stored text. Read the two questions before comparing the two answers: on
most subjects the systems ask different questions.

**Credit support and financing commitments to customers and partners**

| | Old system | New system |
|---|---|---|
| Question | [Old system 1 (`v1`)](#old-v1): At NVIDIA’s next annual report, what amount of financing commitments to customers and partners will NVIDIA report in its commitments note? | [New system 1 (`v1`)](#new-v1): What total amount in USD of NVIDIA’s credit-support commitments and minimum-revenue guarantees or backstops to AI labs and cloud partners, including the support for the additional lab’s nearly 2 gigawatts of computing capacity, will be disclosed in NVIDIA’s FY2027 Form 10-K and related quantified disclosures by the annual report’s publication? |
| Latest answer | 5 Strongly bearish: Reported commitments total at least $25 billion. (answered 2026-09-28) | 5 Strongly bearish: 100,000,000,000 USD or more (answered 2026-09-28) |
| Statements linked | 37 | 37 |
| Reviewers on the question | Team A (Codex): **worth**; Team B (Claude): **worth** | Team A (Codex): **worth**; Team B (Claude): **worth** |
| Reviewers on the answer | Team A (Codex): **INSUFFICIENT**; Team B (Claude): **SUPPORTED** | Team A (Codex): **UNSUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): Both credit-support answers choose their top band, but one means at least $25 billion and the other at least $100 billion. One reviewer disputes each answer's support.

**Approval of Blackwell chip sales to China**

| | Old system | New system |
|---|---|---|
| Question | [Old system 6 (`v6`)](#old-v6): Will the U.S. administration authorize Nvidia Blackwell chip exports to China by January 31, 2027? | [New system 3 (`v3`)](#new-v3): By January 31, 2027, will U.S. authorities authorize Nvidia to sell Blackwell-generation AI chips to China and will Chinese authorities permit those shipments? |
| Latest answer | 1 No: The U.S. administration has not authorized Nvidia Blackwell chip exports to China by January 31, 2027. (answered 2026-09-28) | 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31. (answered 2026-09-28) |
| Statements linked | 31 | 50 |
| Reviewers on the question | Team A (Codex): **worth**; Team B (Claude): **worth** | Team A (Codex): **worth**; Team B (Claude): **worth** |
| Reviewers on the answer | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): The old system forecasts no U.S. authorization; the new system forecasts "still open" on a different question requiring both U.S. and Chinese permission. Those answers are related, but they are not the same answer to the same question.

**The largest cloud companies' data-center spending in calendar 2026**

| | Old system | New system |
|---|---|---|
| Question | [Old system 7 (`v7`)](#old-v7): How much will the five largest AI hyperscalers spend on data centers in calendar 2026? | [New system 5 (`v5`)](#new-v5): How much will the five largest AI hyperscalers spend in total on data centers in calendar 2026, as shown by their Q4/full-year 2026 earnings and capex disclosures? |
| Latest answer | 3 $775 billion to below $825 billion: Combined spending is at least $775 billion and less than $825 billion; this is the neutral comparison range around the author's nearly $800 billion estimate. (answered 2026-09-26) | 3 from 775,000,000,000 USD to below 825,000,000,000 USD: from 775,000,000,000 USD to below 825,000,000,000 USD (the reference when the question opened: "the big five AI hyperscalers will spend nearly $800 billion on data centers this year") (answered 2026-09-28) |
| Statements linked | 11 | 20 |
| Reviewers on the question | Team A (Codex): **worth**; Team B (Claude): **worth** | Team A (Codex): **worth**; Team B (Claude): **worth** |
| Reviewers on the answer | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): The hyperscaler spending answers are in the same dollar band, but the old answer is from September 26 and the new one from September 28.

**Vera Rubin shipping**

| | Old system | New system |
|---|---|---|
| Question | [Old system 9 (`v9`)](#old-v9): Will NVIDIA's Vera Rubin platform begin shipping by January 31, 2027?<br><br>[Old system 11 (`v11`)](#old-v11): Will NVIDIA begin shipping Rubin GPUs by December 31, 2027? | [New system 4 (`v4`)](#new-v4): Will NVIDIA disclose in its quarterly results or FY2027 Form 10-K that Vera Rubin made volume customer shipments with first revenue recognition by the end of FY2027 (January 31, 2027)? |
| Latest answer | 1 Yes: NVIDIA begins shipping the Vera Rubin platform on or before January 31, 2027. (answered 2026-09-28)<br><br>1 Yes: NVIDIA has begun shipping Rubin GPUs by December 31, 2027. (answered 2026-09-28) | 1 Yes: NVIDIA's quarterly results or FY2027 Form 10-K show that Vera Rubin made volume customer shipments with first revenue recognition by January 31, 2027. (answered 2026-09-28) |
| Statements linked | 13<br><br>6 | 39 |
| Reviewers on the question | Team A (Codex): **worth**; Team B (Claude): **worth**<br><br>Team A (Codex): **duplicate** of `v9`; Team B (Claude): **duplicate** of `v9` | Team A (Codex): **worth**; Team B (Claude): **worth** |
| Reviewers on the answer | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**<br><br>Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): Both Rubin answers say yes, but the new question requires volume shipments and revenue recognition, while the old one asks whether shipping begins.

**Beijing's approval of RTX Pro 5500 purchases**

| | Old system | New system |
|---|---|---|
| Question | [Old system 14 (`v14`)](#old-v14): Will China's Ministry of Industry and Information Technology permit Alibaba and ByteDance to buy Nvidia RTX PRO 5500 cards by January 31, 2027?<br><br>[Old system 15 (`v15`)](#old-v15): Will China's Ministry of Industry and Information Technology approve domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027? | [New system 7 (`v7`)](#new-v7): Will China's Ministry of Industry and Information Technology (MIIT) formally approve purchases of Nvidia's RTX Pro 5500 by Alibaba, ByteDance, or other Chinese firms by January 31, 2027? |
| Latest answer | 1 Yes: MIIT permits Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027. (answered 2026-09-28)<br><br>1 Yes: China's Ministry of Industry and Information Technology approves domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027. (answered 2026-09-27) | 1 Yes: MIIT formally approves by January 31, 2027, a purchase of RTX Pro 5500 chips by Alibaba, ByteDance, or another Chinese firm. (answered 2026-09-28) |
| Statements linked | 8<br><br>3 | 22 |
| Reviewers on the question | Team A (Codex): **worth**; Team B (Claude): **worth**<br><br>Team A (Codex): **duplicate** of `v14`; Team B (Claude): **duplicate** of `v14` | Team A (Codex): **worth**; Team B (Claude): **worth** |
| Reviewers on the answer | Team A (Codex): **UNSUPPORTED**; Team B (Claude): **SUPPORTED**<br><br>Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): The old `v14` asks about Alibaba and ByteDance, while the new `v7` asks about at least one purchase by those firms or another Chinese firm. Both answers say yes, but their conditions differ.

**The Hugging Face purchase**

| | Old system | New system |
|---|---|---|
| Question | [Old system 12 (`v12`)](#old-v12): At NVIDIA’s FY2027 annual report, what amount of purchase commitments for the Hugging Face acquisition will NVIDIA report in its commitments note? | [New system 6 (`v6`)](#new-v6): Will NVIDIA complete (close) its agreed acquisition of Hugging Face, as disclosed in NVIDIA's filings, by March 24, 2028? |
| Latest answer | 3 Neutral: The reported amount is at least $10 billion and less than $15 billion. (answered 2026-09-28) | 1 Yes: NVIDIA completes the Hugging Face acquisition by March 24, 2028, as evidenced by NVIDIA's filings or a completion announcement. (answered 2026-09-28) |
| Statements linked | 3 | 11 |
| Reviewers on the question | Team A (Codex): **trivia**; Team B (Claude): **trivia** | Team A (Codex): **trivia**; Team B (Claude): **trivia** |
| Reviewers on the answer | Team A (Codex): **INSUFFICIENT**; Team B (Claude): **SUPPORTED** | Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED** |

How the pair differs (the council's words): The Hugging Face questions concern the amount reported as a purchase commitment and whether the acquisition closes. Both teams call both questions trivia; that does not make their answers comparable.

### 3. Questions only one system holds

**Old system: 7 of its 15**

- [Old system 2 (`v2`)](#old-v2): How much total revenue will Nvidia report for FY2027? Latest answer: 3 Neutral: Total revenue is at least 393868500000 USD and below 418231500000 USD. (answered 2026-09-28). On the question: Team A (Codex): **worth**; Team B (Claude): **worth**. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.
- [Old system 3 (`v3`)](#old-v3): How much total revenue will Nvidia report for FY2028? Latest answer: 2 Bullish: Total revenue is at least 692108500000 USD and below 739145000000 USD. (answered 2026-09-28). On the question: Team A (Codex): **worth**; Team B (Claude): **worth**. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.
- [Old system 4 (`v4`)](#old-v4): How much data-center segment revenue will Nvidia report for FY2027? Latest answer: 2 Bullish: FY2027 data-center segment revenue is at least $400 billion but below $450 billion. (answered 2026-09-28). On the question: Team A (Codex): **worth**; Team B (Claude): **duplicate** of `v2`. On the answer: Team A (Codex): **UNSUPPORTED**; Team B (Claude): **UNSUPPORTED**.
- [Old system 5 (`v5`)](#old-v5): How much will Nvidia's total revenue grow in FY2028? Latest answer: 2 Bullish: FY2028 total revenue growth is at least 70% and below 80%. (answered 2026-09-28). On the question: Team A (Codex): **duplicate** of `v3`; Team B (Claude): **duplicate** of `v3`. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.
- [Old system 8 (`v8`)](#old-v8): How much will tech companies spend on AI in calendar 2027? Latest answer: 3 Middle range: AI spending is at least $1.2 trillion and below $1.4 trillion. (answered 2026-09-28). On the question: Team A (Codex): **trivia**; Team B (Claude): **trivia**. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.
- [Old system 10 (`v10`)](#old-v10): What gross margin will NVIDIA report for FY2028? Latest answer: 3 Neutral: FY2028 gross margin is at least 71% but below 73%. (answered 2026-09-28). On the question: Team A (Codex): **worth**; Team B (Claude): **worth**. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.
- [Old system 13 (`v13`)](#old-v13): Will Nvidia agree to invest in Anthropic's IPO as an anchor investor by September 26, 2027? Latest answer: 1 Yes: Nvidia publicly agrees to invest as an anchor investor in Anthropic's IPO by September 26, 2027. (answered 2026-09-28). On the question: Team A (Codex): **trivia**; Team B (Claude): **trivia**. On the answer: Team A (Codex): **INSUFFICIENT**; Team B (Claude): **SUPPORTED**.

**New system: 1 of its 7**

- [New system 2 (`v2`)](#new-v2): How much in purchase obligations and supply commitments will NVIDIA disclose in its FY2027 Form 10-K, as reported in the purchase obligations and contractual commitments disclosures and related notes? Latest answer: 5 Strongly bearish: 200,000,000,000 USD or more (answered 2026-09-28). On the question: Team A (Codex): **worth**; Team B (Claude): **worth**. On the answer: Team A (Codex): **SUPPORTED**; Team B (Claude): **SUPPORTED**.

### 4. Answers the reviewers did not both pass

Of the 22 latest answers, both teams pass 16; both teams fail 1; one team alone fails 5 (Team A: 6 in all, Team B: 1). For eight answers a separate reader had been asked, before the reading, whether the answer is supported; that mark is shown where it exists.

**Both teams fail**

- [Old system 4 (`v4`)](#old-v4): How much data-center segment revenue will Nvidia report for FY2027? Latest answer: 2 Bullish: FY2027 data-center segment revenue is at least $400 billion but below $450 billion.
  - Team A (Codex): **UNSUPPORTED**. The $400 billion estimate depends on an assumed 25% Q4 increase. The shown statement forecasts faster sales to large cloud customers but does not quantify segment-wide growth.
  - Team B (Claude): **UNSUPPORTED**. Rung 2 is reached only by assuming about 25% Q4 growth, a rate no shown piece gives (e322 says acceleration, unquantified). Carrying the shown 18% gives about $393B, rung 3; the $400B estimate sits on the boundary.

**One team alone fails**

- [Old system 1 (`v1`)](#old-v1): At NVIDIA’s next annual report, what amount of financing commitments to customers and partners will NVIDIA report in its commitments note? Latest answer: 5 Strongly bearish: Reported commitments total at least $25 billion.
  - Team A (Codex): **INSUFFICIENT**. The guarantee ceilings indicate scale, but the request does not establish how much will appear in the commitments note. The cited $1 billion investment and guarantee do not bridge the gap to $25 billion.
  - Team B (Claude): **SUPPORTED**. Disclosed maximum guarantee exposure of $105B and a $108.5B cap (e10, e75), plus the Nscale items, put the scale far above the $25B floor of rung 5; the answer treats the caps as ceilings, not totals.
  - The separate reader, before the reading: **SUPPORTED**. Disclosed maximum guarantee exposure of $105 billion (cap $108.5 billion) plus further credit support and guarantees puts the reported total far above the $25 billion threshold; answer treats caps as ceilings; all figures are in the request.
- [Old system 12 (`v12`)](#old-v12): At NVIDIA’s FY2027 annual report, what amount of purchase commitments for the Hugging Face acquisition will NVIDIA report in its commitments note? Latest answer: 3 Neutral: The reported amount is at least $10 billion and less than $15 billion.
  - Team A (Codex): **INSUFFICIENT**. The $12.9 billion deal value does not establish the amount that will appear as a purchase commitment in the annual report’s note.
  - Team B (Claude): **SUPPORTED**. The only quantified evidence is the agreed acquisition price of about $12.9B to $13B (e188, e262, e359), which sits in rung 3's $10B-$15B band; nothing shown revises the amount or reports a closing.
- [Old system 13 (`v13`)](#old-v13): Will Nvidia agree to invest in Anthropic's IPO as an anchor investor by September 26, 2027? Latest answer: 1 Yes: Nvidia publicly agrees to invest as an anchor investor in Anthropic's IPO by September 26, 2027.
  - Team A (Codex): **INSUFFICIENT**. Reported talks establish a possible deal, but the request provides no basis for concluding a public agreement is more likely than not by the deadline.
  - Team B (Claude): **SUPPORTED**. Reported talks for the specific anchor role with up to $10B (e238) and a year of runway even if the IPO slips past November 2026 lean Yes on a two-rung ladder; the answer says no agreement exists today.
  - The separate reader, before the reading: **UNSURE**. Only a single-source report of talks plus a possible IPO delay. Nothing shown speaks to talks concluding in a public agreement; Yes within a year is a judgement the evidence neither establishes nor contradicts.
- [Old system 14 (`v14`)](#old-v14): Will China's Ministry of Industry and Information Technology permit Alibaba and ByteDance to buy Nvidia RTX PRO 5500 cards by January 31, 2027? Latest answer: 1 Yes: MIIT permits Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027.
  - Team A (Codex): **UNSUPPORTED**. The question requires permission for both Alibaba and ByteDance. The report says some firms were told approval was intended, without identifying both as approved or likely to be.
  - Team B (Claude): **SUPPORTED**. Reports say MIIT asked both firms for quantities and told companies it intends to approve (e284), and Nvidia aims to ship to China from late December (e331); together they lean Yes before January 31. Unverified status is stated.
  - The separate reader, before the reading: **SUPPORTED**. Shown reports: MIIT asked both firms for quantities, told firms it intends to approve, and Nvidia aims to ship in late December, before the deadline. Yes forecast follows; reasons hedge correctly; no outside fact.
- [New system 1 (`v1`)](#new-v1): What total amount in USD of NVIDIA’s credit-support commitments and minimum-revenue guarantees or backstops to AI labs and cloud partners, including the support for the additional lab’s nearly 2 gigawatts of computing capacity, will be disclosed in NVIDIA’s FY2027 Form 10-K and related quantified disclosures by the annual report’s publication? Latest answer: 5 Strongly bearish: 100,000,000,000 USD or more.
  - Team A (Codex): **UNSUPPORTED**. The answer treats a $108.5 billion cap as at least that much exposure and assumes the $105 billion guarantee is included. Neither step is established.
  - Team B (Claude): **SUPPORTED**. Shown evidence quantifies guarantee obligations capped at $108.5B (e114, e136) and the $105B OpenAI lease guarantee inside it; that clears the $100B boundary, so rung 5 follows. Unsized backstops rightly not added.

### 5. What each system is known to cost a reader

Copied unchanged from section 3 of the decision page (`../DECISION-PAGE-2026-11-15.md`), which an independent reviewer read three
times. Its counts of statements (569 written, 389 with no question) are the reading step's; the last part of this page explains the other count.

**The old system**
- One of its 15 latest answers rests on a number nobody gave it: its data-center revenue answer needs fourth-quarter growth of
  about 25%, an allowance the judge made itself (both teams).
- Six of its 15 questions are trivia or duplicates (both teams).
- 126 of its 449 links go to one question, fiscal 2027 revenue: news about other companies and the wider market is filed there
  (the "parking lot" of `docs/prd/10-filing-phase.md` §2).
- It missed one of the five big matters (supply commitments), though it had kept a statement about it under another question.
- It files a statement only at the moment it reads it and does not link an earlier record to a question opened later (none of
  3,225 links in six earlier runs points back; a later article repeating the fact can still deliver it; D456).
- It threw away 278 statements. This week did not establish how many of them a reader would miss.

**The new system**
- It gives no direct answer on the company's own revenue and margin, by the rule above; 145 kept statements of those figures had
  no question at the week's end.
- 389 of its 569 statements had no question at the week's end. A reading of all its stored statements against its seven questions
  confirmed five statements (three facts, three questions) that bear on a question and never reached its judge, with 23 more
  statement-and-question pairs undecided (D508). This is a minimum found by that reading, not a count of losses.
- Adding the strongest of those facts to its question's material: all six answers stayed "yes" (three without the fact, three
  with it), and all three given the fact marked it as counting against "yes". The test was inconclusive (D511).
- When a question opens, the system checks earlier groups of repeated statements if the group's first statement arrived without
  a question. If that first statement arrived under another question, the group is left out, even if the new question also needs
  it (D513, D514).
- Some stored labels are wrong: two market forecasts were filed as the company's own (D504).
- The step that writes answer choices has not passed its required tests. In the July comparison, on seven graded questions, the
  systems agreed with the reference about equally often. The recorded losses occurred before judging: a question was missing or
  did not match the reference closely enough. Some matches remained unresolved; this was not a test of readiness
  (`clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md`).
- In this setup it costs about five times as much to run (a baseline only; cost work comes after correctness).

### 6. Statements no question took

The new system keeps them (382 of 567 in the store its judge reads); the old system discards them when it reads them (278 in its log). Three examples of each, with their stored passages, are at the end of this page. They illustrate; they are not a matched test of what either system loses.


## All 22 entries

### The eight matters (five listed by both teams, three by one)

| Matter | Listed by | Old system | New system |
|---|---|---|---|
| M01 NVIDIA fiscal 2027 revenue (total, or its data-center segment, about 92% of it) | both (Codex: total revenue; Claude: data-center revenue) | Team A (Codex): opened (`v2`, `v4`); Team B (Claude): opened (`v2`, `v4`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M02 NVIDIA fiscal 2028 revenue (total, or its data-center segment) | both (Codex: total revenue; Claude: data-center revenue) | Team A (Codex): opened (`v3`, `v5`); Team B (Claude): opened (`v3`, `v5`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M03 NVIDIA fiscal 2028 non-GAAP gross margin against the 72%-73% outlook | both | Team A (Codex): opened (`v10`); Team B (Claude): opened (`v10`) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M04 NVIDIA supply and capacity purchase commitments at fiscal 2027 year-end ($279B at Q2) | both | Team A (Codex): missed (no question); Team B (Claude): missed (no question) | Team A (Codex): opened (`clean-2`); Team B (Claude): opened (`clean-2`) |
| M05 Whether Beijing formally approves Chinese firms buying NVIDIA RTX Pro 5500 GPUs by 2027-01-31 | both | Team A (Codex): opened (`v14`, `v15`); Team B (Claude): opened (`v14`, `v15`) | Team A (Codex): opened (`clean-7`); Team B (Claude): opened (`clean-7`) |
| M06 NVIDIA fiscal 2027 non-GAAP gross margin under memory-cost squeeze (Q4 trough 71%-72%) | one reader | Team A (Codex): missed (no question); Team B (Claude): missed (no question) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |
| M07 Whether Vera Rubin begins revenue-bearing production shipments in Q3 fiscal 2027 | one reader | Team A (Codex): broader (`v9`); Team B (Claude): opened (`v9`, `v11`) | Team A (Codex): broader (`clean-4`); Team B (Claude): opened (`clean-4`) |
| M08 Whether AMD's 2027 data-center revenue more than doubles as Helios/MI450 ramps | one reader | Team A (Codex): missed (no question); Team B (Claude): missed (no question) | Team A (Codex): missed (no question); Team B (Claude): missed (no question) |

### Old system: 15 questions

<a id="old-v1"></a>

#### Old system 1 (`v1`): At NVIDIA’s next annual report, what amount of financing commitments to customers and partners will NVIDIA report in its commitments note?

- About: NVDA (asset); opened at article 4 of the week; due 2027-02-28; 37 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: Reported commitments total less than $1 billion.
  - 2 Bullish: Reported commitments total at least $1 billion but less than $5 billion.
  - 3 Neutral: Reported commitments total at least $5 billion but less than $10 billion.
  - 4 Bearish: Reported commitments total at least $10 billion but less than $25 billion.
  - 5 Strongly bearish: Reported commitments total at least $25 billion.
- **Latest answer (2026-09-28, article 235): 5 Strongly bearish: Reported commitments total at least $25 billion.**
- Its reasons, as stored: There is no supplied market consensus, company guidance, stated commitments-note target, or prior reported note total, so the reference cannot be placed on the ladder. The strongest direct scale indicators remain maximum guarantee-exposure disclosures of $105 billion and $108.5 billion; they are ceilings, not amounts to add together or assume will be fully reported. New evidence adds a signed $1 billion Nscale financing commitment and a disclosed guarantee of up to $860.3 million, while the reported insurance discussions could eventually shift risk but are early-stage and have produced no stated deal or amount. Taken together with the existing guarantee scale, the evidence still makes a reported amount of at least $25 billion more likely than a lower rung; it does not establish that the full guarantee caps will appear as the reported total.
- What it expects to happen, as stored: At least $25 billion reported, making rung 5 most likely; the $105 billion and $108.5 billion maximum guarantee disclosures establish the scale but are ceilings, not the implied reportable total. The $1 billion Nscale financing and $860.3 million guarantee add specific support, while no amount is supplied for the larger backstop offer or the risk-transfer discussions.
- Team A (Codex) on the question: **worth**. The scale of customer financing and guarantees can change credit risk; the annual report supplies a dated check.
- Team B (Claude) on the question: **worth**. Credit support and guarantees to customers change NVIDIA's credit risk; the annual report's commitments note settles the amount on a fixed date.
- Team A (Codex) on the latest answer against what the judge was shown: **INSUFFICIENT**. The guarantee ceilings indicate scale, but the request does not establish how much will appear in the commitments note. The cited $1 billion investment and guarantee do not bridge the gap to $25 billion.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Disclosed maximum guarantee exposure of $105B and a $108.5B cap (e10, e75), plus the Nscale items, put the scale far above the $25B floor of rung 5; the answer treats the caps as ceilings, not totals.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Disclosed maximum guarantee exposure of $105 billion (cap $108.5 billion) plus further credit support and guarantees puts the reported total far above the $25 billion threshold; answer treats caps as ceilings; all figures are in the request.
- The 23 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v1); stored request: call 713.

<a id="old-v2"></a>

#### Old system 2 (`v2`): How much total revenue will Nvidia report for FY2027?

- About: NVDA (asset); opened at article 11 of the week; due 2027-02-28; 126 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: Total revenue is at least 446655000000 USD.
  - 2 Bullish: Total revenue is at least 418231500000 USD and below 446655000000 USD.
  - 3 Neutral: Total revenue is at least 393868500000 USD and below 418231500000 USD.
  - 4 Bearish: Total revenue is at least 365445000000 USD and below 393868500000 USD.
  - 5 Strongly bearish: Total revenue is below 365445000000 USD.
- **Latest answer (2026-09-28, article 235): 3 Neutral: Total revenue is at least 393868500000 USD and below 418231500000 USD.**
- Its reasons, as stored: The market reference is rung 3: Zacks estimates $406.05 billion and another analyst consensus is around $412 billion, both within $393.8685–$418.2315 billion. The strongest near-term forecast is Nvidia’s $108 billion Q3 guide; carrying its roughly 12% sequential growth forward from the $96.2 billion Q2 result implies about $407 billion for FY2027. The $111.3 billion Q3 consensus is above guidance and, if used instead with the same sequential-growth carry, implies about $418.0 billion—still just below rung 2’s $418.2315 billion floor. Nvidia’s approximately 70% FY2027 growth estimate would imply about $367 billion from FY2026 revenue of $215.9 billion, but that would require Q4 revenue to fall sharply from the guided Q3 level. The new SpaceX and China-related demand indications and the favorable China-permission themes add upside, but their FY2027 revenue contribution is not sized or sufficiently tied to shipments to move the central estimate across a boundary.
- What it expects to happen, as stored: About $407 billion: $178 billion reported in H1 plus the $108 billion Q3 midpoint guide plus about $121 billion for Q4 if the roughly 12% sequential growth from Q2 to guided Q3 carries forward. Using the $111.3 billion Q3 consensus instead implies about $418.0 billion under the same carry, still just below rung 2’s $418.2315 billion threshold.
- Team A (Codex) on the question: **worth**. FY2027 revenue is central to NVIDIA's valuation and can be checked in its annual results.
- Team B (Claude) on the question: **worth**. FY2027 total revenue is the annual number that carries the stock; the article gives the $406 billion consensus and the annual report settles it.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The stated $407 billion projection and the cited consensus estimates fall within rung 3. The answer identifies its extrapolation and competing growth estimate.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. H1 $178B plus $108B Q3 guide plus about $121B Q4 gives about $407B; consensus $406.05B and about $412B also sit in rung 3's band. Unsized SpaceX and China signals do not cross $418.2B.
- The 18 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v2); stored request: call 716.

<a id="old-v3"></a>

#### Old system 3 (`v3`): How much total revenue will Nvidia report for FY2028?

- About: NVDA (asset); opened at article 11 of the week; due 2028-02-29; 47 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: Total revenue is at least 739145000000 USD.
  - 2 Bullish: Total revenue is at least 692108500000 USD and below 739145000000 USD.
  - 3 Neutral: Total revenue is at least 651791500000 USD and below 692108500000 USD.
  - 4 Bearish: Total revenue is at least 604755000000 USD and below 651791500000 USD.
  - 5 Strongly bearish: Total revenue is below 604755000000 USD.
- **Latest answer (2026-09-28, article 235): 2 Bullish: Total revenue is at least 692108500000 USD and below 739145000000 USD.**
- Its reasons, as stored: The market reference is NVIDIA's FY2028 revenue estimate of $671.95 billion, which is rung 3. The stronger forecast input is management's roughly 70% FY2028 growth outlook: applying it to the $412 billion FY2027 consensus base gives about $700 billion, in rung 2. That estimate is close to rung 2's $692.1085 billion floor: using Zacks' lower $406.05 billion FY2027 estimate instead would imply about $690 billion, just below the boundary. The additional customer-demand announcements support the outlook but do not give a reliable FY2028 revenue conversion; the SpaceX target is a capacity ambition, not confirmed NVIDIA revenue, and management expects supply constraints through FY2028. The central forecast therefore remains rung 2, with limited margin over rung 3.
- What it expects to happen, as stored: About $700 billion: apply management's roughly 70% FY2028 growth outlook to the $412 billion FY2027 consensus base ($412 billion × 1.70), as calculated in e199. This is above rung 2's $692.1085 billion floor but below rung 1's $739.145 billion floor.
- Team A (Codex) on the question: **worth**. FY2028 revenue is central to the growth outlook and can be checked in annual results.
- Team B (Claude) on the question: **worth**. FY2028 total revenue is next fiscal year's main number; the article gives the $672 billion consensus and the annual report settles it.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Applying the shown approximately 70% growth outlook to the $412 billion consensus gives about $700 billion, in rung 2. The answer discloses sensitivity to a lower base.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Management's roughly 70% FY2028 growth guide applied to the $412B FY2027 consensus gives about $700B, a figure e199 itself states; that is above rung 2's $692.1B floor. The thin margin and Zacks' lower $671.95B are acknowledged. Cited statements flagged: [{'id': 'e271', 'why': 'Passage says Broadcom AI revenue more than doubles to $115 billion; summary says it will exceed $115 billion.'}].
- The 34 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v3); stored request: call 717.

<a id="old-v4"></a>

#### Old system 4 (`v4`): How much data-center segment revenue will Nvidia report for FY2027?

- About: NVDA (asset); opened at article 13 of the week; due 2027-02-28; 94 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: FY2027 data-center segment revenue is at least $450 billion.
  - 2 Bullish: FY2027 data-center segment revenue is at least $400 billion but below $450 billion.
  - 3 Neutral: FY2027 data-center segment revenue is at least $350 billion but below $400 billion.
  - 4 Bearish: FY2027 data-center segment revenue is at least $300 billion but below $350 billion.
  - 5 Strongly bearish: FY2027 data-center segment revenue is below $300 billion.
- **Latest answer (2026-09-28, article 235): 2 Bullish: FY2027 data-center segment revenue is at least $400 billion but below $450 billion.**
- Its reasons, as stored: The supplied evidence has no full-FY2027 Data Center consensus or annual company target. The operative reference is the near-term revenue trajectory: the prior-quarter run-rate framework puts the FY2027 reference at about $400 billion, at the lower edge of rung 2. Carrying forward roughly $75 billion in Q1 and $89 billion in Q2, applying about 18% sequential growth into Q3 gives roughly $105 billion; a further roughly 25% step-up in Q4, consistent with management's stated acceleration, gives about $131 billion. That totals approximately $400 billion. Rubin's expected 20% Q3 revenue mix and commercial shipments support the ramp, while the disclosed 2.5 GW Anthropic commitment implies about $100 billion of reference-design opportunity at $40 billion per GW through 2028—not $100 billion in FY2027. The supply bottleneck expected through FY2028 limits the upside, but does not quantify a reduction that would move the forecast below $400 billion. The implied outcome therefore remains at the bottom of rung 2 ($400 billion to below $450 billion), rather than crossing into rung 3.
- What it expects to happen, as stored: Approximately $400 billion: about $75 billion in Q1 plus $89 billion in Q2, roughly $105 billion in Q3 carrying forward about 18% sequential growth, and roughly $131 billion in Q4 allowing about 25% growth as large-cloud sales accelerate. The multi-year $100 billion reference-design opportunity from the 2.5 GW commitment is not counted in full for FY2027.
- Team A (Codex) on the question: **worth**. Data-center revenue is NVIDIA's dominant business and reflects a distinct cloud-versus-local demand question; annual results disclose it.
- Team B (Claude) on the question: **duplicate** of `v2`. Data center is about 92% of total revenue, so the same FY2027 result settles both and the answers cannot move apart; no separate bet.
- Team A (Codex) on the latest answer against what the judge was shown: **UNSUPPORTED**. The $400 billion estimate depends on an assumed 25% Q4 increase. The shown statement forecasts faster sales to large cloud customers but does not quantify segment-wide growth.
- Team B (Claude) on the latest answer against what the judge was shown: **UNSUPPORTED**. Rung 2 is reached only by assuming about 25% Q4 growth, a rate no shown piece gives (e322 says acceleration, unquantified). Carrying the shown 18% gives about $393B, rung 3; the $400B estimate sits on the boundary.
- The 9 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v4); stored request: call 715.

<a id="old-v5"></a>

#### Old system 5 (`v5`): How much will Nvidia's total revenue grow in FY2028?

- About: NVDA (asset); opened at article 22 of the week; due 2028-02-29; 43 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: FY2028 total revenue growth is at least 80%.
  - 2 Bullish: FY2028 total revenue growth is at least 70% and below 80%.
  - 3 Neutral: FY2028 total revenue growth is at least 45% and below 70%.
  - 4 Bearish: FY2028 total revenue growth is at least 25% and below 45%.
  - 5 Strongly bearish: FY2028 total revenue growth is below 25%.
- **Latest answer (2026-09-28, article 235): 2 Bullish: FY2028 total revenue growth is at least 70% and below 80%.**
- Its reasons, as stored: The market reference is roughly 65.5%–66% FY2028 growth, which is rung 3 (45% to below 70%). NVIDIA's approximately 70% FY2028 guidance is the stronger forecast input and sits exactly at rung 2's lower boundary. The supply bottleneck expected to last through FY2028 constrains the upside implied by customer demand; the AWS and federal GPU deployments support demand but span multiple years and do not provide enough FY2028 revenue or pricing detail to raise the implied outcome above the guide. Thus the implied outcome remains about 70%, rung 2.
- What it expects to happen, as stored: About 70% FY2028 growth: management's direct outlook is approximately 70%, and applying that growth to the cited $412 billion FY2027 consensus base implies roughly $700 billion of FY2028 revenue (e199). The supply constraint expected through FY2028 limits the case for exceeding that outlook.
- Team A (Codex) on the question: **duplicate** of `v3`. FY2028 revenue growth and the FY2028 revenue amount resolve the same annual outcome once the prior-year revenue is known.
- Team B (Claude) on the question: **duplicate** of `v3`. FY2028 revenue growth is the same reported FY2028 revenue stated as a rate; one result settles both.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Management’s approximately 70% growth outlook is at rung 2’s lower boundary, though the approximation makes the boundary sensitive.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Management guides about 70% FY2028 growth, called supply-constrained with demand higher; at least 70% is rung 2's floor, so the estimate sits there. Consensus of 65.5%-66% is acknowledged as the rung-3 reference. A boundary case.
- The 12 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v5); stored request: call 714.

<a id="old-v6"></a>

#### Old system 6 (`v6`): Will the U.S. administration authorize Nvidia Blackwell chip exports to China by January 31, 2027?

- About: chip-export-controls (theme); opened at article 33 of the week; due 2027-01-31; 31 statements linked; judged 5 times.
- Possible answers:
  - 1 No: The U.S. administration has not authorized Nvidia Blackwell chip exports to China by January 31, 2027.
  - 2 Yes: The U.S. administration has authorized Nvidia Blackwell chip exports to China by January 31, 2027.
- **Latest answer (2026-09-28, article 235): 1 No: The U.S. administration has not authorized Nvidia Blackwell chip exports to China by January 31, 2027.**
- Its reasons, as stored: The available reference is the existing U.S. restriction on Nvidia's most advanced chips, which places the expectation at rung 1; no Blackwell-specific consensus or guidance is supplied. The evidence implies that authorization of Blackwell by January 31, 2027 remains less likely than non-authorization: the H200 permission and reported easing concern older or different products, while the RTX Pro 5500 reports concern Chinese-side purchase intentions, not U.S. authorization of Blackwell. Those signals do not cross the binary rung boundary. This is a forecast, not a finding that non-authorization is already settled.
- What it expects to happen, as stored: The evidence implies no U.S. authorization of Nvidia Blackwell chip exports to China by January 31, 2027. Selective H200 permission and discussion of other products show some potential for easing, but provide no Blackwell-specific U.S. decision or sufficiently direct forecast to move to rung 2.
- Team A (Codex) on the question: **worth**. US permission for Blackwell exports could materially change access to China; a regulatory decision can be checked by the specified date.
- Team B (Claude) on the question: **worth**. A U.S. decision on current-generation chip exports would reopen billions of China sales; an official authorization settles it by the fiscal year-end check date.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Existing restrictions and the absence of a shown Blackwell-specific U.S. authorization support the forecast of no authorization by the deadline.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Shown evidence says Nvidia's most advanced chips remain barred, easing covered only older H200-class chips, and Greer said security export controls were off the table; no Blackwell authorization is shown, so No follows as a forecast.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Request shows a standing U.S. ban on Nvidia's most advanced chips, easing only for older H200, and no Blackwell authorization signal; RTX Pro 5500 items are China-side. No by deadline follows; reasons consistent, no added facts.
- The 17 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v6); stored request: call 707.

<a id="old-v7"></a>

#### Old system 7 (`v7`): How much will the five largest AI hyperscalers spend on data centers in calendar 2026?

- About: ai-capex (theme); opened at article 42 of the week; due 2027-04-30; 11 statements linked; judged 4 times.
- Possible answers:
  - 1 Below $700 billion: Combined spending is less than $700 billion.
  - 2 $700 billion to below $775 billion: Combined spending is at least $700 billion and less than $775 billion.
  - 3 $775 billion to below $825 billion: Combined spending is at least $775 billion and less than $825 billion; this is the neutral comparison range around the author's nearly $800 billion estimate.
  - 4 $825 billion to below $900 billion: Combined spending is at least $825 billion and less than $900 billion.
  - 5 $900 billion or more: Combined spending is at least $900 billion.
- **Latest answer (2026-09-26, article 160): 3 $775 billion to below $825 billion: Combined spending is at least $775 billion and less than $825 billion; this is the neutral comparison range around the author's nearly $800 billion estimate.**
- Its reasons, as stored: The reference is nearly $800 billion for calendar 2026, which sits in rung 3 ($775 billion to below $825 billion). The evidence still implies a total near $800 billion, so it does not cross either boundary. The energy comments and financing concerns identify possible constraints or risks but give no quantified change to the five hyperscalers’ 2026 spending; the global 2030 figure is not a 2026 estimate for these five companies.
- What it expects to happen, as stored: Nearly $800 billion in calendar 2026, based on the supplied estimates for the five hyperscalers, including NVIDIA's reported expectation in e270. That estimate falls within rung 3.
- Team A (Codex) on the question: **worth**. The five hyperscalers' combined data-center spending is a major demand driver, checkable against their public disclosures.
- Team B (Claude) on the question: **worth**. The five hyperscalers' combined 2026 data-center spending is the demand pool for NVIDIA; their annual reports settle it against the article's near-$800 billion.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The near-$800 billion estimate falls within rung 3, and the other cited evidence does not supply a revised 2026 total.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Every quantified piece on the five hyperscalers' 2026 data-center spending says nearly or around $800B (e43, e227, e270), inside rung 3's $775B-$825B band; energy and financing remarks give no amount.
- The 11 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v7); stored request: call 482.

<a id="old-v8"></a>

#### Old system 8 (`v8`): How much will tech companies spend on AI in calendar 2027?

- About: ai-capex (theme); opened at article 45 of the week; due 2028-12-31; 6 statements linked; judged 4 times.
- Possible answers:
  - 1 Lowest range: AI spending is below $1 trillion.
  - 2 Lower-middle range: AI spending is at least $1 trillion and below $1.2 trillion.
  - 3 Middle range: AI spending is at least $1.2 trillion and below $1.4 trillion.
  - 4 Upper-middle range: AI spending is at least $1.4 trillion and below $1.6 trillion.
  - 5 Highest range: AI spending is at least $1.6 trillion.
- **Latest answer (2026-09-28, article 235): 3 Middle range: AI spending is at least $1.2 trillion and below $1.4 trillion.**
- Its reasons, as stored: The reference is about $1.3 trillion for 2027, which sits in rung 3 ($1.2 trillion to below $1.4 trillion). The direct estimate for tech-company AI spending remains about $1.3 trillion; the hyperscaler capex figures support the scale but are not added to that broader estimate. S&P Global Ratings' projection that combined hyperscaler capex will exceed $1.3 trillion by 2027 adds upward pressure, but it does not quantify a level at or above $1.4 trillion for the question's scope, so the implied outcome does not cross a rung boundary.
- What it expects to happen, as stored: About $1.3 trillion in calendar 2027: the direct tech-company estimate is $1.3 trillion, with the global AI-infrastructure estimate and hyperscaler figures supporting that scale. The separate projection of hyperscaler capex exceeding $1.3 trillion is not a quantified estimate of the broader AI-spending total.
- Team A (Codex) on the question: **trivia**. The question leaves both the companies and AI spending undefined, so no identifiable public measure can settle its stated total.
- Team B (Claude) on the question: **trivia**. No dated public material can settle it: 'tech companies' and 'spend on AI' are undefined, and the source is one forecaster's estimate with no release to check.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The direct approximately $1.3 trillion estimate falls in rung 3; the answer distinguishes it from other spending measures.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. S&P Global's $1.3 trillion estimate for tech-company AI spending in 2027 (e48), matched by other $1.3 trillion figures, sits in rung 3's $1.2-$1.4 trillion band; nothing shown quantifies $1.4 trillion or more.
- The 6 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v8); stored request: call 706.

<a id="old-v9"></a>

#### Old system 9 (`v9`): Will NVIDIA's Vera Rubin platform begin shipping by January 31, 2027?

- About: NVDA (asset); opened at article 78 of the week; due 2027-01-31; 13 statements linked; judged 5 times.
- Possible answers:
  - 1 Yes: NVIDIA begins shipping the Vera Rubin platform on or before January 31, 2027.
  - 2 No: NVIDIA has not begun shipping the Vera Rubin platform by January 31, 2027.
- **Latest answer (2026-09-28, article 235): 1 Yes: NVIDIA begins shipping the Vera Rubin platform on or before January 31, 2027.**
- Its reasons, as stored: The reference is rung 2 as a deadline-based baseline: no separate market consensus or distinct shipment-date guidance is supplied, and the question's cutoff is January 31, 2027. The evidence moves the forecast to rung 1: NVIDIA-reported production shipments began in August 2026, before the cutoff. The Q3 FY2027 expectation that Vera Rubin accounts for about 20% of Data Center revenue supports commercial availability; the supply bottleneck through FY2028 limits scale, not whether shipments began.
- What it expects to happen, as stored: Vera Rubin production shipments began in August 2026, so the implied outcome is that shipping began before January 31, 2027 (rung 1). NVIDIA's expectation of about 20% of Data Center revenue from Vera Rubin in fiscal Q3 2027 is consistent with that timing.
- Team A (Codex) on the question: **worth**. The start of shipments for NVIDIA's next major platform can affect revenue and be checked through company announcements.
- Team B (Claude) on the question: **worth**. First shipments of the product generation that carries NVIDIA's value; company results settle it. The article gives no date, so the fiscal year-end is the researcher's.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Reported production shipments beginning in August 2026 support the selected yes outcome before January 2027.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. e311 and e190 report NVIDIA's Vera Rubin production shipments beginning in August 2026, before the January 31, 2027 cutoff; the Q3 revenue-share expectation is consistent. Yes follows by the ladder's own condition.
- The 5 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v9); stored request: call 711.

<a id="old-v10"></a>

#### Old system 10 (`v10`): What gross margin will NVIDIA report for FY2028?

- About: NVDA (asset); opened at article 98 of the week; due 2028-02-28; 18 statements linked; judged 5 times.
- Possible answers:
  - 1 Strongly bullish: FY2028 gross margin is at least 75%.
  - 2 Bullish: FY2028 gross margin is at least 73% but below 75%.
  - 3 Neutral: FY2028 gross margin is at least 71% but below 73%.
  - 4 Bearish: FY2028 gross margin is at least 69% but below 71%.
  - 5 Strongly bearish: FY2028 gross margin is below 69%.
- **Latest answer (2026-09-28, article 235): 3 Neutral: FY2028 gross margin is at least 71% but below 73%.**
- Its reasons, as stored: The reference is NVIDIA management’s FY2028 gross-margin guidance of 72%–73%, which sits in rung 3; Trefis also reports consensus expects roughly steady margins. The implied FY2028 outcome remains about 72.5% (the midpoint of guidance): Q4 FY2027 is expected to bottom at 71%–72%, and the FY2028 outlook includes price increases taking effect in Q1. The more detailed Q3 guide and memory-cost pressure reinforce near-term downside, but no evidence quantifies a further FY2028 reduction below the company’s 72%–73% range. Thus the forecast remains above 71% and below 73%, without crossing a rung boundary.
- What it expects to happen, as stored: About 72.5% for FY2028, using the midpoint of management’s 72%–73% guidance. Management expects a 71%–72% FY2027 Q4 bottom and says FY2028 margins settle at 72%–73%, including the effect of price increases taking effect in FY2028 Q1.
- Team A (Codex) on the question: **worth**. FY2028 gross margin affects the earnings behind NVIDIA's valuation and is checkable in annual results.
- Team B (Claude) on the question: **worth**. FY2028 gross margin against the 72%-73% guide decides whether earnings hold as memory costs rise; the annual report settles it.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Management’s 72%–73% outlook supports the 72.5% midpoint, which falls in rung 3; the cited cost pressures do not specify a different FY2028 estimate.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Management's FY2028 gross-margin guide of 72%-73% (e158, e200, e317), midpoint 72.5%, sits inside rung 3's 71%-73% band; no shown evidence quantifies a move beyond the guide.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Management guides FY2028 gross margin to 72%-73%, midpoint 72.5%, inside rung 3 (71% to below 73%). No shown evidence quantifies a move outside it. Reasons match the request; no added facts.
- The 18 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v10); stored request: call 712.

<a id="old-v11"></a>

#### Old system 11 (`v11`): Will NVIDIA begin shipping Rubin GPUs by December 31, 2027?

- About: NVDA (asset); opened at article 103 of the week; due 2027-12-31; 6 statements linked; judged 4 times.
- Possible answers:
  - 1 Yes: NVIDIA has begun shipping Rubin GPUs by December 31, 2027.
  - 2 No: NVIDIA has not begun shipping Rubin GPUs by December 31, 2027.
- **Latest answer (2026-09-28, article 235): 1 Yes: NVIDIA has begun shipping Rubin GPUs by December 31, 2027.**
- Its reasons, as stored: The reference is rung 1 (Yes): AWS’s stated deployment plan by the deadline places the reference at shipping by December 31, 2027. The reported August 2026 start of production shipments directly supports that outcome; the MLPerf item concerns a preview ahead of broader deployment, not whether initial shipments began. The planned late-2027 SpaceX deployment is consistent with shipments by the deadline. The supply bottleneck through fiscal 2028 is a downside constraint, but does not outweigh the reported start of shipments.
- What it expects to happen, as stored: NVIDIA reportedly began production shipments of Vera Rubin in August 2026, so shipments had begun before the deadline. The late-2027 SpaceX deployment plan is consistent with that timing; the supply bottleneck through fiscal 2028 is a constraint, not evidence that initial shipments had not begun.
- Team A (Codex) on the question: **duplicate** of `v9`. This asks again when the same Rubin generation begins shipping; the later deadline belongs with the earlier open question.
- Team B (Claude) on the question: **duplicate** of `v9`. Same event as Y-9, Rubin starting to ship, with a later deadline; a customer's deployment plan is evidence for that question.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The reported August 2026 production shipments support shipments beginning before the December 2027 deadline.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. e311 reports production shipments of Vera Rubin began in August 2026, with full-production reports consistent; shipping before December 31, 2027 follows. The supply bottleneck is a constraint, not evidence against a start.
- The 6 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v11); stored request: call 710.

<a id="old-v12"></a>

#### Old system 12 (`v12`): At NVIDIA’s FY2027 annual report, what amount of purchase commitments for the Hugging Face acquisition will NVIDIA report in its commitments note?

- About: NVDA (asset); opened at article 116 of the week; due 2027-02-28; 3 statements linked; judged 4 times.
- Possible answers:
  - 1 Strongly bullish: The reported amount is less than $5 billion.
  - 2 Bullish: The reported amount is at least $5 billion and less than $10 billion.
  - 3 Neutral: The reported amount is at least $10 billion and less than $15 billion.
  - 4 Bearish: The reported amount is at least $15 billion and less than $20 billion.
  - 5 Strongly bearish: The reported amount is at least $20 billion.
- **Latest answer (2026-09-28, article 235): 3 Neutral: The reported amount is at least $10 billion and less than $15 billion.**
- Its reasons, as stored: The reference is NVIDIA's announced acquisition value of approximately $12.9 billion, which sits in rung 3 ($10 billion to less than $15 billion). The evidence implies a reported commitment near that amount; there is no quantified change to the deal value that would move the forecast across a rung boundary.
- What it expects to happen, as stored: Approximately $12.9 billion: use the announced acquisition value as the best available proxy for the purchase commitment, with no evidence of a revised amount. That falls in rung 3.
- Team A (Codex) on the question: **trivia**. The article gives an acquisition price, not a purchase commitment disclosed separately in the commitments note; that specific amount may not be publicly reported.
- Team B (Claude) on the question: **trivia**. Would not change a position: the price is already agreed at about $12.9 billion, small beside NVIDIA's cash flow, and the note's amount carries no bet.
- Team A (Codex) on the latest answer against what the judge was shown: **INSUFFICIENT**. The $12.9 billion deal value does not establish the amount that will appear as a purchase commitment in the annual report’s note.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. The only quantified evidence is the agreed acquisition price of about $12.9B to $13B (e188, e262, e359), which sits in rung 3's $10B-$15B band; nothing shown revises the amount or reports a closing.
- The 3 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v12); stored request: call 709.

<a id="old-v13"></a>

#### Old system 13 (`v13`): Will Nvidia agree to invest in Anthropic's IPO as an anchor investor by September 26, 2027?

- About: NVDA (asset); opened at article 141 of the week; due 2027-09-26; 3 statements linked; judged 3 times.
- Possible answers:
  - 1 Yes: Nvidia publicly agrees to invest as an anchor investor in Anthropic's IPO by September 26, 2027.
  - 2 No: Nvidia has not publicly agreed to invest as an anchor investor in Anthropic's IPO by September 26, 2027.
- **Latest answer (2026-09-28, article 235): 1 Yes: Nvidia publicly agrees to invest as an anchor investor in Anthropic's IPO by September 26, 2027.**
- Its reasons, as stored: The reference is rung 2: no public agreement is reported, and no separate market consensus is supplied. The reported talks for the specific anchor-investor role, with a possible investment of up to $10 billion, make a public agreement by the deadline more likely than not. A possible delay until after the November 2026 elections still leaves time before September 26, 2027, so the evidence supports rung 1 rather than merely describing an unconfirmed agreement today.
- What it expects to happen, as stored: A public agreement by September 26, 2027 is more likely than not. Reuters reports talks and a possible investment of up to $10 billion; even if the IPO slips past the November 2026 U.S. midterm elections, the reported timing leaves several months before the deadline.
- Team A (Codex) on the question: **trivia**. The article describes the potential $10 billion investment as small relative to NVIDIA's profits and says it would not change much by itself.
- Team B (Claude) on the question: **trivia**. Small matter: the article itself calls $10 billion a small sum, about a sixth of one quarter's profit; the stake would not change a position.
- Team A (Codex) on the latest answer against what the judge was shown: **INSUFFICIENT**. Reported talks establish a possible deal, but the request provides no basis for concluding a public agreement is more likely than not by the deadline.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Reported talks for the specific anchor role with up to $10B (e238) and a year of runway even if the IPO slips past November 2026 lean Yes on a two-rung ladder; the answer says no agreement exists today.
- A separate reader, asked before the reading whether this answer is supported: **UNSURE**. Only a single-source report of talks plus a possible IPO delay. Nothing shown speaks to talks concluding in a public agreement; Yes within a year is a judgement the evidence neither establishes nor contradicts.
- The 3 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v13); stored request: call 708.

<a id="old-v14"></a>

#### Old system 14 (`v14`): Will China's Ministry of Industry and Information Technology permit Alibaba and ByteDance to buy Nvidia RTX PRO 5500 cards by January 31, 2027?

- About: chip-export-controls (theme); opened at article 163 of the week; due 2027-01-31; 8 statements linked; judged 2 times.
- Possible answers:
  - 1 Yes: MIIT permits Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027.
  - 2 No: MIIT has not permitted Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027.
- **Latest answer (2026-09-28, article 235): 1 Yes: MIIT permits Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027.**
- Its reasons, as stored: The reference is rung 2 (no permission by the deadline): no market consensus or confirmed permission is supplied, so the reference is the no-permission status. The forecast is rung 1 because the report that MIIT intends to approve purchases, together with its request for Alibaba's and ByteDance's planned quantities and uses, makes permission by January 31 more likely than not. Nvidia's reported late-December shipment aim is consistent with that timing, though none of these reports establishes that permission has already been granted. Repeated coverage of the same underlying reports adds no independent confirmation.
- What it expects to happen, as stored: Most likely, MIIT permits both companies to buy the cards by January 31, 2027. The reports give no exact approval date or purchase volume; the reported intention to approve and late-December shipment aim support approval within the deadline.
- Team A (Codex) on the question: **worth**. Chinese permission for these GPU purchases can affect NVIDIA's market access and competition; the decision can be checked by the stated date.
- Team B (Claude) on the question: **worth**. A pending Beijing decision that would reopen China to a new NVIDIA chip, with no China revenue in guidance; an official approval settles it by the check date.
- Team A (Codex) on the latest answer against what the judge was shown: **UNSUPPORTED**. The question requires permission for both Alibaba and ByteDance. The report says some firms were told approval was intended, without identifying both as approved or likely to be.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Reports say MIIT asked both firms for quantities and told companies it intends to approve (e284), and Nvidia aims to ship to China from late December (e331); together they lean Yes before January 31. Unverified status is stated.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Shown reports: MIIT asked both firms for quantities, told firms it intends to approve, and Nvidia aims to ship in late December, before the deadline. Yes forecast follows; reasons hedge correctly; no outside fact.
- The 8 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v14); stored request: call 705.

<a id="old-v15"></a>

#### Old system 15 (`v15`): Will China's Ministry of Industry and Information Technology approve domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027?

- About: chip-export-controls (theme); opened at article 175 of the week; due 2027-01-31; 3 statements linked; judged 1 times.
- Possible answers:
  - 1 Yes: China's Ministry of Industry and Information Technology approves domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027.
  - 2 No: China's Ministry of Industry and Information Technology has not approved domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027.
- **Latest answer (2026-09-27, article 186): 1 Yes: China's Ministry of Industry and Information Technology approves domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027.**
- Its reasons, as stored: The reference is rung 2 because no market consensus or formal approval timetable is supplied, so the no-approval-by-deadline outcome is the baseline rather than a reported expectation. The evidence shifts the forecast to rung 1: the reported request for purchase plans and stated intent to approve make approval by January 31, 2027 more likely than not, although the report gives no approval date and is unverified. The reports are overlapping accounts of one claim, not independent confirmation.
- What it expects to happen, as stored: Approval by January 31, 2027 is the more likely outcome. This follows from the reported request for planned purchase quantities and intended uses, plus the report that officials intend to approve purchases; the report supplies no specific approval date.
- Team A (Codex) on the question: **duplicate** of `v14`. Both ask whether MIIT approves domestic firms' RTX Pro 5500 purchases by January 31; the named companies are examples of those firms.
- Team B (Claude) on the question: **duplicate** of `v14`. Same MIIT approval of the same chip by the same date as Y-14; 'domestic firms' and 'Alibaba and ByteDance' are two wordings of one outcome.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The reported intention to approve purchases supports a forecast of approval by the deadline, with the unconfirmed nature of the report acknowledged.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. The only shown evidence, one unverified report in three outlets, says MIIT asked for purchase plans and intends to approve; on a two-rung ladder that leans Yes. The answer flags the missing date and single source.
- A separate reader, asked before the reading whether this answer is supported: **UNSURE**. Shown reports give intent to 'eventually' approve and no approval date; nothing ties approval to before 31 January 2027. Yes is plausible, but the ladder's deadline condition is not evidenced.
- The 3 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#old-v15); stored request: call 598.


### New system: 7 questions

<a id="new-v1"></a>

#### New system 1 (`v1`): What total amount in USD of NVIDIA’s credit-support commitments and minimum-revenue guarantees or backstops to AI labs and cloud partners, including the support for the additional lab’s nearly 2 gigawatts of computing capacity, will be disclosed in NVIDIA’s FY2027 Form 10-K and related quantified disclosures by the annual report’s publication?

- About: NVDA (asset); opened at article 4 of the week; due 2027-04-01; 37 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: below 10,000,000,000 USD
  - 2 Bullish: from 10,000,000,000 USD to below 25,000,000,000 USD
  - 3 Neutral: from 25,000,000,000 USD to below 50,000,000,000 USD (no reference figure when the question opened)
  - 4 Bearish: from 50,000,000,000 USD to below 100,000,000,000 USD
  - 5 Strongly bearish: 100,000,000,000 USD or more
- **Latest answer (2026-09-28, article 235): 5 Strongly bearish: 100,000,000,000 USD or more**
- Its reasons, as stored: The reference is the ladder’s no-reference baseline: rung 3 ($25bn to below $50bn). The forecast remains rung 5 because the strongest quantified disclosure is a maximum guarantee exposure of $108.5bn, already above the $100bn boundary; the separately reported $105bn OpenAI guarantee is treated as an example within that exposure, not added to it. NVIDIA’s reported offer to backstop part of financing intended to unlock $500bn adds a further in-scope commitment, but the evidence does not quantify NVIDIA’s share, so I do not count the $500bn as its guarantee exposure.
- What it expects to happen, as stored: At least $108.5bn of maximum guarantee exposure is already quantified; the $105bn OpenAI guarantee is treated as included in that cap. The FY2027 disclosure is therefore most likely to remain at or above $100bn, with any separately quantified share of the e500 backstop adding to the total but not derivable from the stated $500bn financing pool.
- Team A (Codex) on the question: **worth**. Large customer credit support and guarantees can change NVIDIA's credit risk; annual disclosures provide a dated check.
- Team B (Claude) on the question: **worth**. Credit support and revenue guarantees for customers behind about a quarter of FY2028 business change NVIDIA's credit risk; the annual report's commitments note settles the amount.
- Team A (Codex) on the latest answer against what the judge was shown: **UNSUPPORTED**. The answer treats a $108.5 billion cap as at least that much exposure and assumes the $105 billion guarantee is included. Neither step is established.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Shown evidence quantifies guarantee obligations capped at $108.5B (e114, e136) and the $105B OpenAI lease guarantee inside it; that clears the $100B boundary, so rung 5 follows. Unsized backstops rightly not added.
- The 10 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v1); stored request: call 35.

<a id="new-v2"></a>

#### New system 2 (`v2`): How much in purchase obligations and supply commitments will NVIDIA disclose in its FY2027 Form 10-K, as reported in the purchase obligations and contractual commitments disclosures and related notes?

- About: NVDA (asset); opened at article 14 of the week; due 2027-04-01; 17 statements linked; judged 7 times.
- Possible answers:
  - 1 Strongly bullish: below 50,000,000,000 USD
  - 2 Bullish: from 50,000,000,000 USD to below 100,000,000,000 USD
  - 3 Neutral: from 100,000,000,000 USD to below 150,000,000,000 USD (no reference figure when the question opened)
  - 4 Bearish: from 150,000,000,000 USD to below 200,000,000,000 USD
  - 5 Strongly bearish: 200,000,000,000 USD or more
- **Latest answer (2026-09-28, article 235): 5 Strongly bearish: 200,000,000,000 USD or more**
- Its reasons, as stored: There is no market consensus or company guidance for the FY2027 Form 10-K commitment total. The question's no-reference starting point is $100bn to below $150bn, rung 3. The latest quantified anchor is $279bn at FY2027 Q2, already above rung 5's $200bn boundary; the increase from $119bn in Q1, management's expectation that supply remains constrained through FY2028, and sustained growth guidance make a year-end disclosure at or above $200bn more likely than a fall below it. The evidence does not support adding the separately reported $500bn HBM figure: its period and overlap with the $279bn commitment total are unspecified. The newer TSMC-order report is a rumor involving several customers, so it reinforces direction but does not establish an additional Nvidia amount.
- What it expects to happen, as stored: Approximately $279bn or higher at the FY2027 10-K: $279bn was reported at FY2027 Q2, up from $119bn in Q1, and the supply-constraint and demand evidence supports commitments remaining elevated through year-end. This clears the $200bn rung-5 threshold; the separate $500bn HBM claim is not added because its timing and overlap are unspecified.
- Team A (Codex) on the question: **worth**. Growing supply obligations can materially affect cash and supply risk; the annual report can disclose their amount.
- Team B (Claude) on the question: **worth**. Purchase and supply commitments are a binding obligation large enough to change cash and credit risk; the Form 10-K states the amount, though the article gives no size.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The reported $279 billion in Q2 supply commitments supports a forecast above $200 billion, with overlapping and unsized figures excluded from the sum.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Supply commitments of $279B at the end of fiscal Q2, up from $119B in Q1 (e202, e113, e136), already clear rung 5's $200B floor, with supply constraints expected through FY2028; the unplaced $500B HBM figure is rightly not added.
- The 17 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v2); stored request: call 36.

<a id="new-v3"></a>

#### New system 3 (`v3`): By January 31, 2027, will U.S. authorities authorize Nvidia to sell Blackwell-generation AI chips to China and will Chinese authorities permit those shipments?

- About: chip-export-controls (theme); opened at article 33 of the week; due 2027-01-31; 50 statements linked; judged 6 times.
- Possible answers:
  - 1 Yes: By January 31, 2027, U.S. authorities have authorized sales of Nvidia Blackwell-generation AI chips to China and Chinese authorities permit those shipments.
  - 2 Ruled out: After September 23, 2026, U.S. export-control authorities formally prohibit Blackwell exports to China, or Chinese authorities formally prohibit Nvidia Blackwell shipments, with the prohibition remaining in force through January 31, 2027. This rung holds when that, or any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after 2026-09-23 and stands on 2027-01-31, and only when rung 1 does not.
  - 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31.
- **Latest answer (2026-09-28, article 235): 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31.**
- Its reasons, as stored: The reference is NVIDIA’s outlook: it excludes China data-center compute revenue, which is closest to rung 3, Still open; it is not a forecast of a formal prohibition. The evidence supports some route to Chinese purchases of the Blackwell-generation RTX PRO 5500, but the reported Chinese intent is unconfirmed and unsized, and that product is a workstation GPU outside the main data-center accelerator category. Meanwhile, reporting says current-generation/high-end accelerators remain barred by the U.S. and China has restricted even H200 shipments. Those facts make joint approval and permission by the due date less likely than continued openness without the required decision, but do not establish a qualifying post-September 23 formal prohibition or abandonment that remains in force. The new quantified H200 order, inventory, licence and Chinese-use restrictions strengthen the case against broad shipment resumption; they do not make the RTX PRO report a confirmed shipment or a data-center approval.
- What it expects to happen, as stored: By January 31, 2027, the most likely outcome is still no established joint U.S. authorization and Chinese permission for Blackwell data-center AI accelerators; the only specific Blackwell purchase path reported is the unsized, unconfirmed RTX PRO 5500 workstation proposal. That points to rung 3: the evidence does not show a qualifying post-September 23 formal prohibition or abandonment that remains in force through the due date.
- Team A (Codex) on the question: **worth**. Access to China's AI-chip market can materially affect sales; US and Chinese decisions can be checked by fiscal year-end.
- Team B (Claude) on the question: **worth**. Reopening China to current-generation chips would add billions in revenue; official decisions settle it by fiscal year-end. It joins two deciders, Washington and Beijing, in one question.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. Existing restrictions and unconfirmed purchase discussions support a forecast that joint authorization remains open; no qualifying later prohibition is shown.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Shown evidence has no U.S. Blackwell authorization with Chinese permission and no formal post-September 23 prohibition; high-end chips stay barred, H200 restricted, RTX PRO 5500 report unconfirmed. Still open follows by the ladder.
- The 13 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v3); stored request: call 33.

<a id="new-v4"></a>

#### New system 4 (`v4`): Will NVIDIA disclose in its quarterly results or FY2027 Form 10-K that Vera Rubin made volume customer shipments with first revenue recognition by the end of FY2027 (January 31, 2027)?

- About: NVDA (asset); opened at article 35 of the week; due 2027-01-31; 39 statements linked; judged 6 times.
- Possible answers:
  - 1 Yes: NVIDIA's quarterly results or FY2027 Form 10-K show that Vera Rubin made volume customer shipments with first revenue recognition by January 31, 2027.
  - 2 Ruled out: After September 23, 2026, NVIDIA formally cancels or abandons the Vera Rubin platform before it makes volume customer shipments. This rung holds when that, or any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after 2026-09-23 and stands on 2027-01-31, and only when rung 1 does not.
  - 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31.
- **Latest answer (2026-09-28, article 235): 1 Yes: NVIDIA's quarterly results or FY2027 Form 10-K show that Vera Rubin made volume customer shipments with first revenue recognition by January 31, 2027.**
- Its reasons, as stored: There is no explicit consensus for this exact event. The closest company reference is management's expectation that Vera Rubin contributes about 20% of fiscal Q3 2027 Data Center revenue, which sits at rung 1 because, if realized, it implies recognized revenue from material customer shipments before the deadline. The August production-shipment reports and management's expectation that sales to the largest cloud companies accelerate in Q4 as supply grows reinforce that forecast. Super Micro's reported commercial shipments add shipment support, although they do not establish NVIDIA's own reported revenue recognition. Supply constraints and the analyst view that some revenue may be delayed temper the outlook, but do not outweigh the specific Q3 revenue expectation and Q4 acceleration. No evidence indicates a qualifying cancellation or abandonment.
- What it expects to happen, as stored: The evidence implies Vera Rubin generates about 20% of fiscal Q3 2027 Data Center revenue, with sales to the largest cloud customers expected to accelerate again in fiscal Q4 as supply grows. This supports volume customer shipments and first revenue recognition by January 31, 2027, though it remains a forecast rather than an established result.
- Team A (Codex) on the question: **worth**. Revenue-bearing shipments of NVIDIA's next platform are a major product milestone, checkable through company disclosures.
- Team B (Claude) on the question: **worth**. First revenue shipments of the product generation that carries NVIDIA's value; quarterly results settle it. The article gives no date, so the fiscal year-end is the researcher's.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The projected Q3 revenue contribution and reported production and commercial shipments support a forecast of volume shipments and recognized revenue before the deadline.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Production shipments began in August and management expects Vera Rubin at about 20% of fiscal Q3 data-center revenue with Q4 acceleration; that implies volume shipments and recognized revenue before January 31, 2027. No cancellation shown. Cited statements flagged: [{'id': 'e279', 'why': "Summary labels Micron's November quarter 'fiscal Q1 2026'; passage gives no such label and the September 2026 date contradicts it."}].
- The 12 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v4); stored request: call 37.

<a id="new-v5"></a>

#### New system 5 (`v5`): How much will the five largest AI hyperscalers spend in total on data centers in calendar 2026, as shown by their Q4/full-year 2026 earnings and capex disclosures?

- About: ai-capex (theme); opened at article 42 of the week; due 2027-03-31; 20 statements linked; judged 5 times.
- Possible answers:
  - 1 below 700,000,000,000 USD: below 700,000,000,000 USD
  - 2 from 700,000,000,000 USD to below 775,000,000,000 USD: from 700,000,000,000 USD to below 775,000,000,000 USD
  - 3 from 775,000,000,000 USD to below 825,000,000,000 USD: from 775,000,000,000 USD to below 825,000,000,000 USD (the reference when the question opened: "the big five AI hyperscalers will spend nearly $800 billion on data centers this year")
  - 4 from 825,000,000,000 USD to below 900,000,000,000 USD: from 825,000,000,000 USD to below 900,000,000,000 USD
  - 5 900,000,000,000 USD or more: 900,000,000,000 USD or more
- **Latest answer (2026-09-28, article 235): 3 from 775,000,000,000 USD to below 825,000,000,000 USD: from 775,000,000,000 USD to below 825,000,000,000 USD (the reference when the question opened: "the big five AI hyperscalers will spend nearly $800 billion on data centers this year")**
- Its reasons, as stored: The reference is nearly $800 billion, which sits in rung 3. The direct forecast still implies about $800 billion for the five in calendar 2026, within rung 3's $775 billion–below-$825 billion range. Alphabet's $200 billion is a component of the aggregate, not an additional amount; the GPU and capacity commitments and supplier/customer demand indicators lean upward but do not quantify a 2026 total or revision that crosses a rung boundary. The global AI-infrastructure figure near $750 billion has a different scope, and the $1.3 trillion projections concern 2027.
- What it expects to happen, as stored: About $800 billion, based on NVIDIA's forecast for the big five's 2026 data-center capex as reported in e162 and e367, consistent with the near-$800-billion estimate in e103 and e119. This is within rung 3; Alphabet's $200 billion is part of the total, not an amount to add to it.
- Team A (Codex) on the question: **worth**. Combined hyperscaler infrastructure spending affects demand across suppliers and can be checked against annual disclosures.
- Team B (Claude) on the question: **worth**. The five hyperscalers' combined 2026 data-center spending is the demand pool for NVIDIA; their annual reports settle it against the article's near-$800 billion.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The direct estimate of nearly $800 billion falls in rung 3. The answer does not add a component or mix in differently scoped forecasts.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. NVIDIA's and other outlets' figure of nearly $800B for the big five's 2026 data-center spending (e162, e367, e103) sits in rung 3's $775B-$825B band; nothing shown quantifies a revision across a boundary.
- The 13 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v5); stored request: call 31.

<a id="new-v6"></a>

#### New system 6 (`v6`): Will NVIDIA complete (close) its agreed acquisition of Hugging Face, as disclosed in NVIDIA's filings, by March 24, 2028?

- About: NVDA (asset); opened at article 116 of the week; due 2028-03-24; 11 statements linked; judged 4 times.
- Possible answers:
  - 1 Yes: NVIDIA completes the Hugging Face acquisition by March 24, 2028, as evidenced by NVIDIA's filings or a completion announcement.
  - 2 Ruled out: After 2026-09-25, NVIDIA or Hugging Face formally terminates or withdraws the acquisition agreement before it is completed. This rung holds when that, or any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after 2026-09-25 and stands on 2028-03-24, and only when rung 1 does not.
  - 3 Still open: Neither rung 1 nor rung 2 holds on 2028-03-24.
- **Latest answer (2026-09-28, article 235): 1 Yes: NVIDIA completes the Hugging Face acquisition by March 24, 2028, as evidenced by NVIDIA's filings or a completion announcement.**
- Its reasons, as stored: The agreement and the newer reports describing Hugging Face as acquired make completion by the deadline the most likely outcome. However, the reports describing it as completed do not provide the NVIDIA filing or explicit completion announcement specified by rung 1, and the contemporaneous “pending” report is contrary evidence. That limits certainty but does not make an open or terminated deal more likely by the 2028 check date.
- What it expects to happen, as stored: The evidence implies the deal is likely to have closed already or to close well before March 24, 2028: multiple reports describe Hugging Face as acquired, while the agreement was announced roughly 18 months before the check date. No precise closing date can be derived from the evidence.
- Team A (Codex) on the question: **trivia**. The $12.9 billion deal is small relative to NVIDIA's scale and cash generation; the article does not establish a position-changing impact.
- Team B (Claude) on the question: **trivia**. Small matter: $12.9 billion against $96.7 billion of free cash flow in fiscal 2026; closing or not would not change revenue, profit, cash or credit risk.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. An agreed acquisition and reports describing it as acquired support a forecast of closing by 2028, while the answer acknowledges the pending report and absence of a completion filing.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. A deal agreed on Sept. 3, 2026, described by several outlets as acquired, with no termination, repricing or delay shown and 18 months to the deadline, makes Yes the likeliest rung; the pending caveat is acknowledged.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Agreement announced 3 September 2026, about 18 months before the check date; nothing shown reports termination, repricing or delay. Completion forecast follows; answer treats 'acquired' wording as unconfirmed and notes the 'pending' report.
- The 7 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v6); stored request: call 34.

<a id="new-v7"></a>

#### New system 7 (`v7`): Will China's Ministry of Industry and Information Technology (MIIT) formally approve purchases of Nvidia's RTX Pro 5500 by Alibaba, ByteDance, or other Chinese firms by January 31, 2027?

- About: chip-export-controls (theme); opened at article 169 of the week; due 2027-01-31; 22 statements linked; judged 2 times.
- Possible answers:
  - 1 Yes: MIIT formally approves by January 31, 2027, a purchase of RTX Pro 5500 chips by Alibaba, ByteDance, or another Chinese firm.
  - 2 Ruled out: After September 27, 2026, MIIT formally rejects all RTX Pro 5500 purchase plans from Alibaba, ByteDance, and other Chinese firms, or formally prohibits those firms from purchasing the chips. This rung holds when that, or any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after 2026-09-27 and stands on 2027-01-31, and only when rung 1 does not.
  - 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31.
- **Latest answer (2026-09-28, article 235): 1 Yes: MIIT formally approves by January 31, 2027, a purchase of RTX Pro 5500 chips by Alibaba, ByteDance, or another Chinese firm.**
- Its reasons, as stored: The available reference is no explicit consensus probability; the reported expectation that MIIT intends to approve some purchase plans, and that some firms were told approval is likely, places the reference at rung 1. I also forecast rung 1: those reports are specific to the firms and product in the question, and plans were collected months before the deadline. The contemplated ByteDance order and reported China supply plan indicate possible scale, not an approved quantity. Domestic-chip preferences, a proposed bundling rule, uncertainty over U.S. export treatment, and the H200 precedent temper the forecast; the late-December shipment target also leaves a relatively short window before the deadline. But none is evidence of a formal decision against all purchases, and the reported MIIT intent makes at least one approval by January 31 more likely than either an adverse formal decision or no decision.
- What it expects to happen, as stored: Most likely, MIIT formally approves at least one purchase by January 31, 2027; the evidence supplies no approval date or approved quantity. The reported roughly 1 million-unit ByteDance plan would equal about two quarters of the reported 500,000-unit-per-quarter China supply plan, but neither figure establishes how much MIIT would approve.
- Team A (Codex) on the question: **worth**. A Chinese approval could change NVIDIA's market access and competitive position; the pending decision has a fiscal year-end check date.
- Team B (Claude) on the question: **worth**. A pending Beijing decision that would reopen China to a new NVIDIA chip after curbs from both governments; an official approval settles it by the stated check date.
- Team A (Codex) on the latest answer against what the judge was shown: **SUPPORTED**. The reported intention to approve purchases supports forecasting at least one approval by the deadline; the answer recognizes that no approval has been confirmed.
- Team B (Claude) on the latest answer against what the judge was shown: **SUPPORTED**. Reports that MIIT told firms it intends to approve and that approval is likely (e400, e419), with a late-December shipment aim, lean Yes for at least one approval; H200 precedent and bundling risks are weighed, none a formal rejection.
- A separate reader, asked before the reading whether this answer is supported: **SUPPORTED**. Reported MIIT intent to approve, 'likely to receive approval' and a late-December shipment target support at least one approval by the deadline; rung needs only one purchase. Counter-evidence (H200 precedent, bundling) is weighed; none shows rejection.
- The 14 statements this answer cites, each with its stored passage: [SIDE-BY-SIDE-WEEK-CITED.md](SIDE-BY-SIDE-WEEK-CITED.md#new-v7); stored request: call 32.


## Statements no question took: three examples from each system

**These are illustrations, not a matched test.** The two lists are different populations: statements the new system still
holds with no question at the week's end, and statements the old system discarded at the moment it read them. Each list is a random draw of three with one fixed seed (20261202).
"Stored attribution" is the speaker the system recorded; nobody checked it. The passage is the system's stored quotation from the article.

**The new system keeps them.** In the store its judge reads, 382 of 567 statements have no question. The week's result page counts 389 of 569 at the reading step; 2 records were dropped on the way to the judge's store for want of a verified passage (`adapter-counts.json`), and the rest of the difference has not been traced.

- `e124` (article 49 of the week; stored attribution: NVIDIA): NVIDIA mentioned warm-water cooling technology during a keynote address, and investors read the remark as a threat to SPX Technologies' air-cooled cooling towers; the article ties that reading to the selloff that has dragged SPX shares from above $230 toward their 52-week low. The item gives no date, product name or technical detail for the NVIDIA remark.
  - Stored passage: "The selloff that has dragged the stock from above $230 down toward its 52-week low has a specific, nameable cause. … Nvidia mentioned warm-water cooling technology during a keynote, and investors immediately read that as a threat to SPX's air-cooled towers."
- `e477` (article 200 of the week; stored attribution: Consensus of analysts (estimates compiled by Bloomberg)): Analysts' estimates compiled by Bloomberg predict that Nvidia's earnings per share will almost double this fiscal year, according to the article, which cites this as happening even as the shares trade at a trailing P/E of around 30; the forecast was reported on 28 September 2026.
  - Stored passage: "That's even as analysts predict earnings per share will almost double this fiscal year, according to estimates compiled by Bloomberg."
- `e227` (article 95 of the week; stored attribution: NVIDIA): NVIDIA saw a jump in credit-default-swap trading after its $25B bond sale in June, which the item reads as increased hedging tied to NVIDIA's debt position.
  - Stored passage: "NVIDIA (NVDA) saw a jump in credit-default-swap trading after its $25B June bond sale, signaling increased hedging tied to NVDA’s debt position."

**The old system throws them away.** Its log records 278 statements dropped as "no home" (no question took them).

- `e6` of article 1 of the week (stored attribution: Flexiv): Flexiv is integrating NVIDIA Isaac ROS with its Rizon 4 adaptive robot, enabling a path from Isaac Sim testing to deployment on a physical robot.
  - Stored passage: "Flexiv is integrating Isaac ROS with its Rizon 4 adaptive robot, giving developers access to NVIDIA-accelerated robotics capabilities and a streamlined path from testing applications in NVIDIA Isaac Sim to deploying them on a physical robot."
- `e8` of article 25 of the week (stored attribution: iApp Technology): Thailand's iApp Technology is adapting Nvidia Nemotron 3 Nano for Thai-language legal work.
  - Stored passage: "Meanwhile, Thailand's iApp Technology is adapting Nemotron 3 Nano for Thai-language legal work."
- `e4` of article 227 of the week (stored attribution: Barchart.com): Barchart reported a consensus mean Nvidia price target of about $326, implying nearly 45% upside over the next 12 months.
  - Stored passage: "According to Barchart, the consensus rating on Nvidia sits at "Strong Buy," with the mean price target of about $326 indicating potential for a nearly 45% rally over the next 12 months."
