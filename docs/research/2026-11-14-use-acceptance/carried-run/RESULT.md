# The product condition, end to end over two weeks with the library kept: the reading (D563), 2026-11-16

**Answer: in this one draw, with the library of week 1 held, the six questions week 2 opened duplicated none it held (both
families), and the step that writes answer choices wrote them for 12 of 13 topics in all three attempts, but the choices do not meet Alex's six lines (gate 1: 7 or 5 of 13
topics right against a scaled 11). Of the 12 last answers, none is unsupported by both families and 6 are contested
by at least one of three readers, for several different reasons. The company's own numbers have no home by product rule, and
neither reader family predicted that any not delivered would change one of the 12 answers; two statements over-read their
passages; the product's page could not show the new system's library (fixed at the writer, D564). One draw, one company,
one fortnight; week 2's later steps were regenerated with week 1's, not a live two-week history.**

Run: `poc/data/clean-carried-run-2026-11-16/` (week 1 the stored run of 2026-09-22..28 from empty; week 2 2026-09-29..10-05, 241
never-sent articles, read from week 1's library; the later steps regenerated over the fortnight; ledger $3.476 of $6.00, no
refusal). Plan frozen before any answer was read (`PLAN.md`, sha256 in `PLAN.sha256`); my own read stored first (`OWN-READ.md`).

## What the run did

| | Week 1 (from empty) | Week 2 (library kept) |
|---|---|---|
| Articles | 235 | 241 |
| Topics opened | 7 | 6 |
| Kept statements with no link | 389 of 569 (68%) | 339 of 626 (54%) |

Answer choices over the fortnight: **12 of 13 topics written in all three attempts**; the one declined in all three is
"venture funding for physical AI companies" (no listed theme covers it; the two opening readers split on its worth, my own read says not worth holding). Written is not right: read against
Alex's six lines (reading A below), they do not meet them. For comparison, from an empty start: the week of 10-06, 4 of 13
topics declined at least once, 2 every time, and agreed faults beyond refusals; July, 21 of 104 declined in two or three attempts.
Different weeks and articles: an observation, not a measured difference.

## Reading A: Alex's six lines on the fortnight's answer choices (`poc/data/clean-carried-run-2026-11-16/stage-a/report.txt`)

The October tooling unchanged: two families apart (39 valid rows each), 24 sends disputed, a third reader of each family on 34
points; every unresolved point counted both ways. **Gate 1 is not met:** line 1 missed (3 or 5 sends), line 2 missed (7), line 3
missed (4 or 7), line 4 met (the only refusals, robotics funding ×3, justified), line 5 missed (right 7 or 5 of 13 against a scaled
11; by written choices 6 or 4 against 9), line 6 not measured. Fault kinds: a stated plan left out of an event's reference (not
shown to the judge; its effect untraced); a due day before the report that settles the event (the Rubin revenue question, upheld
by both third readers; the CPO case split); "and" in the question against "or" in the Yes rung (MIIT, disputed among third
readers); parts left unlisted; a question leaning on an unnamed lab. The October and July readings used other articles and draws:
this does not isolate the effect of the library.

**The due-date class, sized** (`due_day_census.py` → `due-day-census.txt`; a pattern screen, flagged cases read by hand): across
every stored written event answer, the only answers naming a periodic report as the sole settling material with the due day at
the period's end are six attempts of one matter (Rubin's FY2027 revenue, the same week-1 topic in two readings). Not a reason to
open a new version of the step.

## Reading 1: week 2's openings (two families; `tally-openings.txt`)

- **Re-opened a held question: 0 of 6** by both families. Same matter, another shape: capital spending for 2027 beside 2026 (both;
  a year of its own, D38), the residual-value guarantee beside the credit-support total (one family; a signing question, D388).
- Worth holding: 2 yes by both (capital spending 2027; the residual-value guarantee); 4 split yes/no (robotics funding, U.S.
  gigawatts added in 2026, DRAM contract prices 2026, co-packaged-optics switch volumes).
- Controls on 26 articles (the 6 openers and 20 drawn by seed): lost facts named by both families 0; wrong homes named by both 2
  (an investment return under credit support; Micron's customer commitments under NVIDIA's supply commitments).
- Lost questions both families name again and again: **the company's own numbers** (the quarter's revenue against the $108bn
  guide, fiscal 2028 growth against 70%, margins, earnings) and **the $150bn buyback**. The first is the product rule (D382,
  D384; D505: such figures should reach the judgements of related questions, not be questions of their own; not built).

## Reading 2: every last answer (two families, planted and confirmed controls; `tally-answers.txt`)

- **12 questions: supported by both 9; unsupported by both 0; split 3** (memory prices 2026: insufficient/supported; the credit
  support total: the $108.5bn cap read as the amount, unsupported/supported; 2026 capital spending: $820bn by adding Amazon's
  raise to the $800bn reference, unsupported/supported).
- Controls: 4 planted wrong answers caught by both families (4 of 4; the plants are conspicuous contradictions between a choice
  and its own reasons); 4 confirmed supported controls accepted by both (4 of 4; these are 4 of the 12 real answers, not
  additional ones).
- Statement fidelity, verified against the stored passages: `e590` says the Hugging Face CEO "said he had just sold his company"
  and that the acquisition "had been completed"; the passage is TechCrunch's parenthetical, and completion is an inference (both
  families flag it). `e279` labels Micron's November quarter "fiscal Q1 2026", copied from the article's title, not its passage
  (one family). The first step's summary added what the passage does not hold.
- The separate control reader (8 candidates) marked 3 not supported (U.S. gigawatts, memory prices, CPO volumes) and 1 unsure (the
  residual-value guarantee). Across all three readers, **6 of 12 answers are uncontested** (supply commitments, China's Blackwell
  approval, Rubin's revenue, the Hugging Face closing, MIIT's approval, 2027 capital spending) and 6 contested, for several
  reasons: a cap read as the amount, a possible double count, qualitative evidence used to choose a numeric band, an event
  forecast, and an answer-choice interpretation. Cases to trace one by one; not one proven mechanism.

## Reading 3: did the answers get the facts that could change them? (a reader lead, not a test; `claude-sources.jsonl`, `codex-sources.jsonl`)

Five questions drawn by seed (supply commitments, China's Blackwell approval, 2026 and 2027 capital spending, the residual-value
guarantee), each read with its last request and up to six of the fortnight's articles on it. No family named an undelivered fact
that would move an answer; a few that would change its confidence. **The reading fell short of its frozen plan:** the packet
showed the request but not the last answer itself; it had no separate negative control; the readers listed absent facts
themselves instead of a code classification of every listed fact. The positive control (PRD 10's custom-chip group) was caught by
the Claude-family reader and missed by the Codex-family reader. A lead from one family on five questions, not a result.

## Reading 4: did the company's own figures reach the questions they bear on? (D564; `figures_census.py`, `tally-figures.txt`)

By the statements' own fields (party NVIDIA, a typed financial figure): 270 kept statements in 61 groups of repeats. Against each of
the 12 judged questions' last request, the groups not shown and dated by its day: 46 to 61 a question. Two families apart read
every question with its whole last request and answer, the custom-chip question of July with its five facts mixed in as a positive
control and one statement already shown to the Rubin question as a negative.

- **No pair that would move an answer, by either family.** Pairs named as changing only the confidence: NVIDIA's sales to the
  largest cloud companies for the two capital-spending questions (both families on the 2027 one); revenue per gigawatt and
  data-center revenue as a cross-check of U.S. gigawatts (Claude family only); cash-flow figures for the Hugging Face and
  residual-value questions (Codex family only, the Claude family "neither").
- **Controls.** Negative: neither family named the statement already shown. Positive: the Claude family named the two Broadcom
  revenue figures as moving the answer (as they did, 9 of 9 sends, in PRD 10's test). The Codex family named nothing in the main
  reading because the packet dated the control facts "2026-07" and left the negative's day empty: **my packet's fault**; on a
  control packet with the real days it named four as confidence and the fifth "cannot tell", none as moving the answer. So a Codex-family "no effect" is weak evidence, as
  in reading 3; the Claude family caught the control both times.
- **What it shows:** among the selected figures and questions, neither family predicted an answer-choice change; the control and
  selection limits leave a delivery gap unresolved. Limits (council round 12): the selector takes only statements whose party is
  NVIDIA and whose typed measure matches a fixed list, not every financial fact; it drops a repeat group when any member was
  shown, so a repeat's own details in an unshown member are not read (partly shown groups exist); readers saw summaries and
  figures, not the source passages; a reader's "would move" is a prediction until a send tests it. Reading 1's largest missing
  matter (the company's own figures) is first a matter of which questions exist (D382, D384: figures are evidence, not questions).
- **Gate 1, per topic** (`faults_by_topic.py`, `faults-by-topic.txt`): the most frequent failing mark is a stated plan left out of an
  event's reference (7 attempts, 3 topics), which is not shown to the judge; fixing it alone would make 2 more topics right
  (9 or 7 of 13 against 11, a paper upper bound if that mark alone changed). No one kind of fault holds the gap.

## Found on the way

**Integration** (`INTEGRATION-CHECK.md`): the product's page server shows the new system's stored library as empty: the read side
places questions in time by completed days, which the new system's writer never records. Gate 5's first concrete defect.

## Limits

One draw; one company; one fortnight; week 2's later steps were regenerated with week 1's (not a live system's history); the
readers are two model families and one separate model reader; reading 3 is five questions. Nothing here compares the two systems
or passes a gate.
