# Plan v2: the clean system's first end-to-end measurement (revised for `el-codex.md`; 2026-11-09)

**What it is.** A seeded diagnostic. Given the ruler's 22 questions as an isolated fixture, does clean Steps 1–3 deliver to the frozen
judge the facts that change answers, compared with production re-sent the same day?

**What it is not:**
- a test of whether the clean system would open those questions (D370);
- a production acceptance;
- an unseen-data result: the window's articles are golden-v5 dev, which tuned c8.

Every result carries these labels.

## Stage 0 ($0): the adapter, checked at the request level

**Chronological replay, one day at a time, in the order production uses:**
1. **Seeds first.** For each draw, a fresh `views.sqlite` gets the 22 seeds via `seeding.seed_views` at seq 0, with production's rungs
   and dependencies.
2. **Articles in manifest order.** Each clean article k takes seq k:
   - its records are inserted at seq k;
   - links made by Step 1 for that article are inserted at seq k;
   - later links are inserted at the seq of the article whose processing made them (`library.later_log[*].article`);
   - repeat and revision relations are inserted at the seq of the article that created them.
3. **Judge once per day.** After a day's last article, the frozen `round_of_judgements` (judging-v7, gpt-6-luna) runs with seq equal to
   that article's seq and the day's changed views, as `round.judge_day` collects them.

Nothing from a later article is in the database when an earlier day is judged.

**Field mapping** (each choice listed and counted):
- `one_line` = the record's summary.
- `quote` = the first verified passage. The judge cuts quotes to 400 characters, as for production. Records with more than one passage
  are counted, and the loss is reported. A record with no verified passage is dropped, as production drops "quote not in item", and
  counted.
- `speaker` = reporting_speaker; `original_who` = original_party; `original_day` = statement_date (null allowed); tier as written.
- Sources: input_id and publication date.
- Links: Step 1 links go on the record that carried them. A later link goes on the group's original record.
- A repeat member becomes same_claims with its group's original. A revision becomes a revisions row, only where Step 3 recorded one.
- Clean-opened theses are not judged and are listed, with one exception. A thesis the clean system opened itself as an unsigned
  obligation signing question carries the standard's yes/no ladder (Yes/No; "还没签：是非两档"). It is scored for q23 only if the scorer's
  own rule maps it (a question containing "Ohio" and "guarantee"). Nothing is forced or hand-linked.

**Checks:**
1. **Leakage.** For every judge request on day d, every shown evidence item has a source publication day of d or earlier and a link seq
   of the day's seq or lower. This is checked from the request text and the database.
2. **Request shape.** One adapter request (v1 on 07-14) is compared field by field with a stored production v108 request for the same
   view and day: sections, ordering, dependencies, theme block.
3. **Answer path.** A synthetic answer passes `check_answer`, and `_record` writes it.
4. **Scorer.** The scorer accepts the database and prints every question.
5. **Mutants.** A mutant that inserts one future record must fail check 1.

## Stage 1 (cents): the delivery probe, as a gate for one hypothesis

**What it tests.** c8 has never run with 22 open theses. The hypothesis: with the seeds present, c8 links the facts the starved and
missed questions need.

**What is sent:**
- **Treatment:** c8, unchanged, with a seeded before-state: the 22 seeds plus the clean theses a seeded run would have opened by then,
  rebuilt from a seeded Step 1 replay of the earlier articles. If that is too costly, the treatment uses the 22 seeds only, with the
  limit stated.
- **Control:** the stored, unseeded c8 request, re-sent the same day.
- **Articles:** those carrying gold facts i163 (66% margin, q10), i131 (cash flow, q12), i234 and i139 (Broadcom, q16), the China-share
  fact (q17) and i005 (Ohio, q23), each located in golden-v5 dev and the trace before sending, plus 4 controls. Three draws each.
- **Before sending:** requests are rebuilt and verified byte for byte except the open-theses list, and predictions and stop conditions
  are frozen with sha256.

**What it decides.** If c8 with the seeds does not deliver q10 and q12's facts in at least 2 of 3 draws, Stage 2 cannot test the
starved-question hypothesis. That goes to Alex before Stage 2. It is not proof that Stage 2 cannot beat production elsewhere.

## Stage 2 (about $8, only on Alex's word): three paired draws

**Arms:**
- **Clean:** the seeded clean path above.
- **Control:** production v108 re-sent the same day. Current `scripts/replay.py` refuses seeded ledgers (lines 29–48), so the control
  runs from a separate worktree at the commit that produced the r10 control, with code unchanged and launched detached. That needs Alex's
  word, as does the fixture.

**Decision rule, frozen before sending:**
- The table of every question and draw for both arms, with judges' reasons read for every disagreement.
- The null is estimated from the two stored v108 control sets (r9 against r10: totals 46 and 46, with per-question swings on q02, q05,
  q16, q17, q20 and q23).
- **Better:** clean total minus control total is at least 3 over the three draws, and no question the control agrees in 3 of 3 is
  agreed by clean in 0 of 3.
- **Worse:** that difference is −3 or less, or such a regression.
- **Inconclusive:** anything else, and reported as such.
- **The starved-question test, separately:** q10 and q12 both agree in at least 2 of 3 clean draws (the prior acceptance's standard,
  `acceptance-measure.txt`).

## For Alex

1. The 22 seeds as an isolated fixture for this diagnostic (D370, D391).
2. The same-day control from a worktree at the r10 commit.
3. Stage 0 and Stage 1 now; Stage 2 only on his word after Stage 1.
