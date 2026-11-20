# Merge test: execution plan (written before any send, 2026-11-19)

**Alex, 2026-11-19 (the goal):** "write the plan, execute the plan, and don't do full blown runs, validate it works based on metrics we
meassure for quality". This plan carries out D678's test. D677 stopped paid sends; this goal lifts that stop for this test only (D679).

## What is tested
This is the merge's one new piece of wiring.
- Clean Step 1 (c8, unchanged) reads each article with the **old system's open questions** as its open theses.
- The evidence it files under an old question reaches the **frozen production judge** with that question's old answer choices.
- The judge then answers.

| | Old draw (as stored) | Hybrid (this test) |
|---|---|---|
| Questions and choices | Old opening and ladder | **The same rows**, unchanged |
| History to 09-06 | Old evidence and judgements | **The same rows** |
| Window evidence, 09-07..09-20 | Old extraction and filing | **c8's filing** under the old questions |
| Judge | Frozen judging (poc-v118) | **The same code and configuration**, on the target questions only |

## The article set (revised after council round c, `council-c-codex.md`)
**My first count was wrong.** I read the census article numbers as positions in `kept-articles.json`. They are numbers in
`census/numbering.json`.
- With the right numbering, 8 of the 11 census articles reached the old target questions in at least one old draw.
- Control 223 is `gnews:5adb2372…`, which old filed under v5 and v6.

The plan's first set (126 articles) also drew in the new draws' custom-chip and DRAM theses: adjacent matters, not these two.

**The set is now 70 articles** (65 for capex and 8 for Anthropic, with some overlap), in `articles.json` with each article's source:
- the census articles and the control: 12;
- the window sources of the five old target questions: 32 for capex and 5 for Anthropic;
- the window links of the new draws' directly corresponding theses:
  - new-2: clean-5 (big-four capex 2026–27) and clean-43 (Anthropic);
  - new-3: clean-4 (capex), clean-34 and clean-58 (Anthropic).

## The questions (stored rows)
| Draw | Matter | Question | Old answer at 09-20 |
|---|---|---|---|
| old-2 | M04 | v5: four largest hyperscalers' data-center capex, calendar 2026 (5 rungs) | rung 4, $700–800B |
| old-2 | M17 | v40: NVIDIA invests $10B to anchor Anthropic's IPO by 2026-09-20 (yes/no) | rung 2, No |
| old-3 | M04 | v6: the same as v5 | rung 4 |
| old-3 | M17 | v47 (by 2026-09-20) and v48 (by 2027-03-14) | v47 rung 2; v48 rung 1 |

## Steps
1. **$0. The open list per article.**
   - For each draw and article, take the old views open at that article's old sequence number: created at or before it and not
     switched off before it.
   - Each becomes a Step 1 thesis (code-owned conversion):
     - `id` is the view id;
     - `description` is the question;
     - `outcome` is the view's observable focus (`looks_at`);
     - `period` gives the reporting period and the deadline as two labelled parts.
   - The answer choices stay with the judge.
   - c8's own new theses are recorded but **not opened**, because opening is the old system's job.
2. **$0. Preflight.**
   - One request is built per draw with the stored c8 settings. Its system text and closing check must equal new-2's stored request,
     byte for byte.
   - A synthetic answer linking to `v5` must pass Step 1's checks.
3. **Paid, about $1.4.** 140 c8 sends: 70 articles × 2 draws.
   - Each article is its own one-item Step 1 run, 8 at a time.
   - They go on a new ledger with a $5 ceiling.
4. **$0. Filing census.**
   - For each target question: the c8 evidence linked to it, by article.
   - c8's proposed new theses, checked for NVIDIA's own figures.
5. **Paid, about $0.3. Judging, in two arms on the same 09-06 copy of each old store.**
   - **The copy.** Every row written after 09-06 is cut: answers, links, sources, switches, repeat and revision relations. The other
     views keep their 09-06 state. The target questions created later are put back on the day the old system created them.
   - **The judge.** The frozen judge's own round judges the target questions only; its queue is restricted explicitly.
   - **Hybrid arm:** c8's evidence for the target questions, written day by day.
   - **Control arm:** the old system's own window evidence for the target questions (with its sources and its repeat and revision
     relations), written day by day the same way. It isolates the evidence source from the reconstruction. The archived old answers
     saw other questions updated through 09-20; the control did not.
6. **Readers.**
   - Each answer is turned into a card in the deck's format: question, choices, final answer, reasons and the material it was given.
   - The hybrid cards are mixed with the five old cards for the same questions and with deck controls, under shuffled labels.
   - Two blind readers read them, Claude and Codex, with the comparison's reader brief.
7. **Score** against the lines below. Claude reads every trace behind a failed line.

## Quality lines (written before any send)
| # | Line | Pass when |
|---|---|---|
| P1 | Delivery, checked in the judge requests themselves | In both draws, a request of each primary question shows c8 evidence carrying the matter's decisive statement. For capex, that is the four companies' 2026 capex figures or an aggregate of them, such as article 181's $720–745B. For Anthropic, it is the reported $10B anchor-investment talks |
| P2 | No meaning drift | No five-company or 2027 figure is presented as the answer to the four-company 2026 question. A total-capex figure used for "data-center" capex is named as a proxy. This is a higher bar than old met: old's capex answers did not label the proxy, and that is disclosed |
| P3 | Talks stay talks | No Anthropic answer treats reported talks as a signed or completed investment |
| P4 | Opening rule (diagnostic only) | The c8 theses proposed on NVIDIA's own figures are counted. Not a pass line: the open lists already hold old revenue and margin questions |
| P5 | Supported answer | Both readers mark the four primary hybrid answers supported: old-2 v5, old-2 v40, old-3 v6, old-3 v47. old-3 v48, which the deck read as duplicate and unsupported, is a negative control |
| V | Validity, before P5 is read | The readers pass the deck controls and mark the control arm's reconstructed old-evidence answers supported. Otherwise the reconstruction, not the merge, is in question |

- **Pass** means V holds, and P1, P2, P3 and P5 hold in both draws.
- **Also reported:**
  - whether the hybrid's answer matches old's;
  - the material's size;
  - the share of material about the question, read by Claude: one draw each and descriptive. The PRD's old-system problem was 24–44%
    of citations about other companies or the whole market.
- **What this cannot show:** automatic opening, repeat grouping (Steps 2–3 are not run), the other 30 matters, or release readiness.
