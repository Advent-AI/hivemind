# Plan: the clean system's first end-to-end measurement (Claude, before the council; 2026-11-09)

Alex (D391): "收尾，你先完整的和council 讨论下你要怎么做下一步的收尾测量等，需要你完整的读完trace 和所有历史的learning 和我们的状态再决定下一步".

## Inputs read (four cold digests, verified at the cited lines)

- **Scorer.** `score_judgement.py` refuses a run whose v1–v22 are not the seed texts (lines 38–43). It takes the last judgement on or
  before 07-14 by judgement_id, and needs rungs with lo/hi bands.
- **Replay.** `scripts/replay.py` refuses seeded ledgers (29–48) and configs with a baseline (78–79). Nothing in src/ calls
  `seed_views`.
- **Production misses** (v108, three draws: 15, 15, 16 agreements):
  - **q10 and q12 never judged:** 0 evidence links. The 66% operating margin was never written. The cash-flow sentence was written
    and dropped as "no home". The judge given the gold facts gets q10 3/3 and q12 2/3.
  - **q16** follows whether Broadcom's figures are linked to it. Even with gold facts it agrees only 1/3: interpretation.
  - **q17** swings on the gold's own boundary.
  - **q23 (Ohio)** is folded into v9 in 7 of 9 draws.
- **Clean data versus the judge:**
  - no rungs or bands and no due date (outcome and period are free text);
  - links have no sequence number, and 40–53% of evidence is unlinked;
  - statement_date is null for most records;
  - several passages per record against production's one quote;
  - repeat groups instead of same_claims and revisions;
  - the library is in memory, keyed by article index.
- **History:**
  - judging drifts across days, so the rules require a same-day control, not the archive (P10:68, 128);
  - the window's articles are golden-v5 dev, which tuned c8, so a score is optimistic;
  - no end-to-end pass line is registered;
  - readers A and B differ on 3 of 23;
  - substitute paths have misled before (an adapter changed record order).

## What the measurement answers

**The question.** Given the ruler's 22 questions as an isolated fixture, does clean Steps 1–3 deliver to the frozen judge the facts that
change answers, at least as well as production?

**What it does not answer:** whether the clean system would open those questions itself (D370), or the daily path. The label says so.

## Stages

**Stage 0 ($0): the adapter contract and checks.** The adapter writes a fresh `views.sqlite` per draw:
- the 22 seeds via `seeding.seed_views`, at seq 0, with rungs and dependencies as production wrote them;
- each clean record as one evidence row:
  - quote = the first verified passage, the others joined into one_line;
  - tier, speaker, original_who = party, original_day = statement_date;
  - sources from input_id and publication date;
- links from the record's thesis_ids to view ids, with one seq per publication day;
- repeat groups as same_claims, and revisions as revisions;
- then judging day by day with the frozen `round_of_judgements` (judging-v7, gpt-6-luna), one seq per day.

Clean-opened theses are not judged, except a yes/no Ohio thesis mapped to q23 with Yes/No rungs. They are listed.

Checks:
- stored clean records through the adapter, with counts compared;
- a synthetic judge answer through `check_answer`;
- the scorer accepting the database;
- a read-back that every link's seq is at or below its day's judging seq.

**Stage 1 (cents): the delivery probe.**
- **Why first.** c8 has never run with 22 open theses. The decisive question is whether it links the facts the missed questions need.
- **What is sent.** c8, unchanged, with the 22 seeds as open theses and the stored before-state otherwise, on the gold articles carrying:
  - q10: i163, the 66% margin;
  - q12: i131, cash flow;
  - q16: i234 and i139, Broadcom;
  - q17: China share effectively zero;
  - q23: i005, Ohio;

  plus 4 or 5 control articles. Three draws each.
- **What is read.**
  - Is each fact written and linked to its question?
  - How much does linking clutter move with 22 open theses?
  - Does any seed get duplicated by a new thesis?
- **Stop condition.** If c8 does not deliver q10 and q12's facts with the seeds present, the full run cannot beat production, and the
  next work is delivery, not the run.

**Stage 2 (about $8, on Alex's word): the end-to-end run, three draws.**
- **Arms.** The clean arm runs c8 forward over 07-01 to 07-14 from the seeded start, then Steps 2–3, the adapter, daily judging and the
  scorer. The same-day control is production v108 re-sent the same day, which needs the same fixture exception.
- **Predictions and stop conditions,** frozen with sha256 before the send:
  - **Pass:** the clean arm's agreements are at least the control's in 2 of 3 paired draws, and q10 or q12 is judged in at least 2 of 3.
  - **Fail:** fewer agreements in 2 of 3, or more never-judged questions.

  Every disagreement is traced to the step that lost the fact.

## For Alex to decide

1. The 22 seeds as an isolated fixture for both arms, against D370's retirement of them as a starting library.
2. A same-day v108 control, about $2 more, or the archived v108 with that limit disclosed.
3. Stage 1 now, and Stage 2 only on his word after it.
