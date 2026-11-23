# The lean path toward production: round log (Alex, 2026-11-14: "小步快跑")

## 0. Frame

- **Objective** (Alex chose the lean plan over the heavy acceptance; goal set 2026-11-14: "一步步tackle, 使用council skill 讨论复盘，执行，看数据
  然后推进，不要drift from PRD and scope"): decide which system carries forward toward production, with small steps that each answer one
  question the same day.
  - Step 1 ($0 model): a statement whose date is later than its own article's day is an impossible record; count it, find its mechanism, fix
    it where the record is written, in both systems, proved by deterministic replay.
  - Step 2 (about $4): one fresh week (2026-09-22..28, never sent by any run; the frozen list `fresh-articles-2026-09-22-10-05.json`), both
    systems one draw each from empty; readings A (big questions opened or missed, on a sample) and B (last judgements supported by what was
    shown) only, as calibrated in the trial (`TRIAL-RESULT.md`) with its fixes.
  - Step 3: from step 2's data, which system carries forward and what to fix next; a product choice goes to Alex with options.
- **Pass lines:** none fixed by Alex for step 2; it is a comparison, reported per system with every count; the proposed lines of
  `ACCEPTANCE-DESIGN.md` are reference only.
- **Reference systems:** production as it runs (poc-v118) and the clean path as frozen (c8, Step 2 D427, ladder step D426, frozen judge).
- **The ruler:** the frozen ruler stays (D261) and is not used to choose here; the trial's readings are leads, not a calibrated gate.
- **Constraints:** frozen prompts and pieces stay (D274, D354, D359, D426, D427); a code check that refuses an impossible value is identity, not
  judgement (AGENTS §2); no prompt change in this path without its own council round and Alex's word where it changes behaviour.
- **Budget:** step 2 about $4 (ceiling $8), priced from the full run's charged cost per article; Alex agreed the lean plan's size.

## 1. Step 1: statements dated after their article ($0) — the premise does not hold; nothing is built

- **Census** (`date-census.txt`): 31 statements in the six full-run draws (c1 6, c2 7, c3 6, p1 1, p2 4, p3 7) carry an original day later than
  their article's stored day. Every one read: almost all are **correct dates against a stored day that is one day early** (a Bloomberg
  Intelligence survey "released on Tuesday Jul 7" whose item is stored as 07-06 though its `published_at` is "Tue, 07 Jul 2026 07:00:00 GMT";
  Singapore's charges "(July 6)" in an item stored as 07-05; Nokia's 07-15 announcement in an item stored as 07-14); one is a page updated after
  publication (a 07-10 page holding SanDisk's results of August 5). The two "August 2026" statements both trial readers flagged quote the page
  itself ("Nvidia said in August 2026 …" in a 07-12 item): the page carries later text; the system copied it faithfully.
- **Source census** (`source-date-census.txt`, all 3,643 eligible items 2026-07-01..10-27): 165 items have a stored day earlier than the UTC
  date of their `published_at` (some by months: a `published_at` of 24 October on an item stored as 07-01, likely a feed's later date, not the
  article's); 13 items' texts report something as said or done more than a month after their day (a look-ahead lead: pages captured after
  updates; some are legitimate schedules, e.g. a dividend payable on October 1).
- **Decision (AGENTS §1: the cause is elsewhere; build nothing):** a check refusing such statements would throw away correct facts. The two
  real issues are in the source data (the day an item is stored under, and pages that carry later text), a measurement concern recorded for
  the readings: a reader judging "supported by what was available that day" may meet later text inside a page. No change to either system.

## 2. Step 2: one fresh week, one draw a system — frozen before any send

- **Inputs, proved at $0:** `fresh_week_inputs.py` builds the week through production's own replay loop (`testdb.feed`, NVDA, `dispatch.route`
  on an empty store) and checks it against the clean runner's selection rule: 235 items (232 never sent + 3 that earlier Step 1 test sets
  sent), the same set, order and text identity in both (`fresh-week-manifest.json`). The week's dates (`fresh-week-dates.txt`): one item stored a
  day before its `published_at`; no dated mention after an item's day phrased as already done. The comparison is still "on the stored page
  text", which may hold later edits we cannot see.
- **Driver:** `run_fresh.py` takes `--manifest` (Step 1 reads it; production replays from its first day); the default window is unchanged
  (proved: identical manifests for 07-01, 07-05, 07-14; recorded options unchanged; a day outside the window refused).
- **Run:** first a one-day slice (09-22, 27 items, both systems, its own root) to see every component complete on the new window; then the week,
  one draw a system, from an empty library, its own root and ledger; about $3.60, ledger ceiling $8 (slice and week together).
- **Readings** (two families, blind to the system and to each other, keys outside the repository): A on 40 articles sampled from the 232
  never-sent (seed 20261115, stratified by day): matters each family lists, covered = opened, or narrower carrying the matter's main outcome;
  each system's opened questions marked worth / trivia / duplicate; B on every last judgement by 09-28 against the request as sent, planted wrong
  judgements on requests not otherwise in the packet, four supported controls confirmed by a separate reader first. Disagreements listed.
- **Decision rule, written before reading:** a system **carries forward** when, on A, it covers at least two more of the matters both families
  list than the other system, and on B its share of last judgements both families call supported is not lower by more than one in ten.
  Otherwise the difference is **not clear**: the next small step targets the largest difference observed (named from the data), not a choice
  of system. Every count is reported per system, with missed matters, trivia, unsupported judgements and reader disagreements; one draw each.

- **Slice (2026-09-22, 27 items), read:** both draws complete in every component (clean: Step 1, Step 2, cases, ladder, judge; production);
  both read exactly the day's 27 manifest items; ledger $0.26, 146 attempts, no refusal. A lead for reading A: on day one the clean path opened
  one question (credit support and revenue guarantees), production seven, among them three overlapping guarantee or credit-support amounts and
  both "total revenue in FY2027" and "total revenue growth in FY2027". The week was launched as frozen (`poc/data/clean-lean-week-2026-11-14/week/`).
- **Week, first pass:** production complete (235 items extracted, 15 questions opened, 72 judgements, the same items as the manifest). The
  clean draw stopped at Step 1 step 87 of 235 on a transport failure after the transport's own retries ("Connection reset by peer"); under the
  run's redo rule (D449: one redo per component, for a transport failure) Step 1 was relaunched in `step1-redo`, from the start. Ledger $1.58
  before the redo.
- **Claude's own read of production's week library (a lead, before the blind readings):** 15 questions; likely duplicates: v14/v15 (the same
  RTX Pro 5500 approval), v3/v5 (FY2028 total revenue and its growth, settled by one outcome), v9/v11 (Rubin shipping by 2027-01-31 and by
  2027-12-31, one event with two deadlines); questionable: v12 (the Hugging Face acquisition as a purchase commitment), v8 (AI spending of "tech
  companies", no population); the FY2027 total-revenue question holds 126 linked statements (PRD 10's parking pattern).
- **The redo stopped too** (Step 1 step 61, "IncompleteRead(36144 bytes read)"), ending the draw by its rule. Diagnosed instead of rerun
  (AGENTS §1): 7 of 52 stored Step 1 traces had stopped on one network error, because the clean transport sent each attempt once while
  production's retries; fixed at the transport with every attempt on the ledger and recorded (D488, council `mw-codex-10.md`; tests and
  mutants). The clean week draw was relaunched from empty in `week-r2/` with a new $5.80 ledger (the first spent $2.17).
- *Lesson:* a failure the run rules call "redo once" was a recurring defect across five earlier runs; count a failure's class over stored
  runs before spending a redo on it.
- **The relaunched clean draw completed** (`week-r2/c1`, every component): 235 of 235 articles, no network loss, one format retry (step 4, an
  extra field, recorded), ledger $2.52 of $5.80 (both ledgers $4.69 of the $8 the step was sized at). 7 questions opened, 37 judgements.
- **What each system holds at the week's end (counted from the stored runs, $0):**

  | | clean c1 | production p1 |
  |---|---|---|
  | questions opened | 7 | 15 |
  | statements written | 569, from 182 articles | 673, from 186 articles |
  | thrown away for having no question | 0 | 278 ("no home") |
  | kept | 569 (314 after joining repeats) | 385 (after joining repeats) |
  | kept with no question (reach no judgement) | 389 | 0 |
  | links to questions | 196 | 449 (126 on FY2027 total revenue, 94 on data-center revenue) |
  | judgements | 37 | 72 |

  Among the clean draw's 389 statements with no question: the company's 70% growth outlook for fiscal 2028 (14 statements, 14 articles),
  gross-margin figures of 71% to 73% (11 statements), and the quarter's reported revenue; 145 of the 389 are the company's own figures. They are kept as D382 says ("财务类型不应该是thesis，而更多的是条件") and no judgement reads them.
- **Readings launched** (`week/`): `build_week_A2.py` (both question lists under the labels X and Y, each question with the article it was
  opened from, `opening-articles-A2.json`), `build_week_B.py` (22 real last judgements and 4 planted from earlier judgements, 26 items; the
  planted rung is the far end of the ladder from the answer's own, changed before any reading so no planted rung is a neighbour; all four
  checked against their originals: 5 to 1, 3 to 1, 3 to 1, yes to no), briefs `brief-A2.md`, `brief-B.md`, `brief-controls-B.md`; `tally_week.py`
  joins the answers to the keys and refuses on a missing cell, item or control. Part 2 of reading A (worth / trivia / duplicate) is read
  beside the opening article.

## 3. Step 2's result and step 3 (D489): not clear; no system chosen; one product choice goes to Alex

- **Result** (`week/WEEK-RESULT.md`, `week/tally.txt`): A, of five matters both families listed: production 4, clean 2 (families agree on all ten
  cells); questions worth holding: clean 6 of 7, production 8 or 9 of 15. B, supported by both families: clean 6 of 7, production 10 of 15;
  planted items caught 4 of 4 by both; supported controls passed 2 of 4 (Codex) and 4 of 4 (Claude).
- **The rule as written:** first half met by production, second not (19 points): not clear.
- **Council round 11** (`mw-codex-11.md`): the verdict stands; B cannot rank at this size and the two disputed controls are a disagreement with
  reasons, not errors to count back; the three-matter gap is by Alex's decisions, and "a company outlook against a market expectation is the
  reason he meant" is not his word; check the source at $0 before proposing a door.
- **Source check ($0):** the door covers 0 of 7 articles for FY2027 revenue; dropped (`WEEK-RESULT.md`, last section).
- **Council round 12** (`mw-codex-12.md`): no system chosen; three options to Alex, with the limits of one week and one draw stated.
- *Lessons:*
  - A candidate fix is read against the source articles at $0 before it is proposed: the door I drew from two quotes could not open the
    first of the three matters it was for.
  - A reader family can part from a "confirmed" control with a reason; a control settles a reader's attention (the planted items did), not
    a dispute about what counts as support. Seven judgements against fifteen rank nothing.
  - The readers were told to read by a standard that names the main driver as a question type; their listing shows the standard at work,
    not a user's preference. The gap is Alex's rule meeting that standard, so it is his to settle.
  - My own slip: a count written into this log before it was counted (production's "229 articles"; counted: 186). A number enters a log only
    from a query.

## 4. Step 3: Alex opens the test of revenue and margin questions on the new system (D490)

- **Alex:** "试开这类问题 (Recommended)" on the three options of D489.
- **Hypothesis:** the clean path lacks these questions only because its request forbids them; with the standard's row A carried for revenue
  and gross margin, it opens the three matters on the articles that carry them, files their figures there, and opens nothing else new.
  **What would refute it** (written before the send, `main-numbers/PROBE-DESIGN.md`): the matters not opened in most sends; a number card
  (EPS, a quarter, another company) or the same result asked twice in most sends of a case; the named figures not kept or not linked; the
  supply-commitments or Vera Rubin openings suppressed.
- **Change, one direction** (`clean-arch/step1-unfiled-2026-11-08/arms/c20-*`): a fifth reason `main_driver` in §3's closed set (the company's
  own annual revenue or gross margin, current or next fiscal year), its date in the date rule, the do-not-open row rewritten around it,
  "five reasons" in §3, the closing check and the schema. +746 characters; the standard's wording, narrowed to revenue and margin by D490's
  scope (the narrowing disclosed).
- **Reviews before the send:** two blind audits of the wording (`audit-c20-blind.md`, `audit-c20v2-blind.md`: first version wider than D490,
  no date rule, a growth example, measure and scope unasked, all fixed; the date stays an event, as the adopted request has it for
  obligations); council rounds 13 to 15 (`mw-codex-13.md` to `mw-codex-15.md`): both arms on every case, rates over valid sends, kept-and-linked
  as a line read by blind readers, number cards judged by what the question asks, a reader difference that could change the verdict left
  undecided, step two (the same matters met again, built case by case) written now and required before any fresh week. A synthetic answer
  passes the arm's schema and the runner's checks; the two controls fail as they must.
- **Step one sent** (`poc/data/clean-main-numbers-probe-2026-11-14/stage1`): ten stored states of the week, c8 and c20, three sends each, 60
  sends, ceiling $2.00.
- *Lessons so far:*
  - I told Alex "a few cents" before sizing the probe; with a same-day control on every case it is about one dollar. A cost goes to him
    from a dry run, not from a guess.
  - Three design rounds for a one-dollar probe: each found something that would have made the result unreadable (the request wider than
    the approved scope; a pass possible with the figures lost; the author as the only reader of a line). The rounds were worth it; the
    way to keep them short is to write the counting for "kept and linked" and for the readers at the first draft, where arm c1 had failed.
- **Step one's result (D491; `main-numbers/RESULT.md`, `tally-stage1.txt`):** 60 valid sends, $1.02. Against the control: the three questions
  open (fiscal 2027 revenue 9 of 9, the fiscal 2028 margin 6 of 6, fiscal 2028 revenue 13 of 15 with the growth shape disputed by the
  readers), figures kept and linked, no number card, none twice, none from a bare figure; statements with no question 118 → 45.
  **Fails on suppression:** the Vera Rubin question 0 of 3 against c8's 2 of 3. The hypothesis is refuted on a condition written beforehand;
  the line stops (D355).
- **Council round 16** (`mw-codex-16.md`): the verdict stands; my "the revenue question caused it" was a lead stated as a cause: the reasoning
  also gives the missing shipment date, as c8's non-opening send does. Not shown: that revenue must swallow product questions, or that
  statements without a figure never belong under revenue.
- **Where kept figures stand ($0):** 382 of 567 statements in the judge's store have no question; the 70% outlook is in none of 37 judgement
  requests; later linking judged 516 earlier statements and linked 2.
- *Lessons:*
  - The stop condition written before the send did its work: the arm passed every line it was built for and would have gone on to a paid
    week on those alone.
  - Read a reasoning trace for every reason it gives, not for the one that fits the story: I quoted the sentences that filed the news
    under revenue and passed over the date sentences beside them. The council read all three and found both.
  - Three sends a case can stop a line; they cannot name its cause. A cause needs either the control's spread or a case built to split
    the two reasons.

## 5. Reflection council mx (D492, D493): what the traces say, and the next step

- **Alex:** "跑council run review of the traces deeply then determine next step to try improving, don’t go in circles or make same mistake learn
  from it".
- **Read by Claude:** the clean draw's trace, library and judge store; production's store and archive; the probe's sends; three seeded samples
  of 36 read one by one (`council/mx-claude-reflection.md`). **Read cold by a fresh Codex:** `council/mx-codex-1.md`.
- **Found:** the loss is around the main numbers (the clean path holds no view; production's view is a pile and its drops include margin
  facts); the unread statements do not bear on the clean path's open questions, so better delivery to existing judgements recovers
  little; production's own week shows the Rubin statement filed under revenue at the same article, its question 43 articles late.
- **The circle named:** ten changes of words in the one call, each chosen from the last failure, each moving a neighbour. The week re-measured
  a gap the trial had shown.
- **Argued:** Codex's delivery audit withdrawn on Claude's samples; Claude's standing-question comparison kept as a candidate, not the
  step (presets, D370; four or five sends cannot show safety); both converge on the kept figures as a record.
- **Next step, $0** (`record/RECORD-TEST-DESIGN.md`, design changed twice by the council before any entry was read): the record built by code;
  fidelity by two blind families on 20 rows of each stratum; six fixed questions answered from the record alone against a reference
  written from the same 40 articles. Built: 341 figure rows from 179 statements of 74 articles (186 revenue or margin, 155 other);
  the 40 articles' view holds 44 revenue and margin rows under 42 headings: the stored measure and period are free text, so code alone
  merges none of them. Readers running.
- *Lessons:*
  - Before a paid run, write what an earlier, cheaper result already says about its outcome; if the main difference is known, the run is
    sized for what is not.
  - A reflection that only lists what failed picks the next failure. Ranking by what the reader ends without moved the next step from
    the question list to the figures the system already holds.
  - The stored runs of the other system are a second experiment already paid for: look there before designing a send.
- **The record test's result (D494; `record/RECORD-TEST-RESULT.md`, `tally-record.txt`):** measure and value right in 40 of 40 rows; five of six
  questions answered from the record as from the articles; the line missed on one wrong attribution (the reported 75% margin given as the
  CFO's). Cause traced to the stored record: who and when are kept once per statement (step 121, `ev-5`). Fidelity of the other rows and
  two questions' completeness left unsettled, as the council asked.
- **Council rounds 3 to 5** (`mx-codex-4.md`, `mx-codex-5.md`): my "not ready by one line, and close" settled too much; my view-level fix
  ("an actual is the company's report") could hide a mixed statement or make up a source; census first; then three choices to Alex.
- *Lessons:*
  - Check a rejection before reporting it: one "wrong" mark was my packet's fault (the readers were not shown the publisher the model saw).
  - A free test can still be over-read. "Five of six" was my tally of marks the comparers gave without the questions' wording in front of
    them; say what the instrument did not exercise.
  - When a field is stored once for a record that holds several things, every reader of that record inherits the ambiguity; the fix
    belongs where the record is written, and it is a field, not a rule.

## 6. Alex opens the new version of the record: a source and a fixed-form period on each figure (D495)

- **Alex:** "开新版：每个数字自带来源 (Recommended)" on the three choices of D494.
- **Hypothesis:** the record's attribution errors come from one party stored per statement; with a party and a fixed-form period on each
  figure the model gives the right party to each figure of a mixed statement and writes a fixed period only where the article
  establishes it, and nothing else the call decides moves, because no rule changes. **What would refute it** (written before the send,
  `figure-fields/PROBE-DESIGN.md`): the named figures' parties still wrong in most sends on two of the five target cases; fixed periods
  made up; fewer statements kept, linked or opened than the same-day control; figures' measure, value or kind degraded.
- **Change:** arm c21 = c8 with two required fields in `figures` items (`party`, `fiscal_period` with a pattern code checks); system text and
  closing check byte for byte c8's. Schema +1,086 characters.
- **Applied from the last probe's lessons, in the first draft:** both arms on every case; rates over valid sends; the control's room as a
  condition; every line read by two blind families with the publisher in their packet; not-exercised and undecided as outcomes; the cost
  from a dry run (about $1.00, ceiling $2.00).
- **Result (D496; `figure-fields/RESULT.md`, `tally-figure-fields.txt`):** 60 valid sends, $0.85. Party of the named figures right in four of four
  judged cases (c8 fails four); wrong parties 2.1% against 8.2%; fixed periods right in 176 of 177 by the readers; kept, linked, opened
  and the statements' own fields not seen to move. **Undecided, stopped:** the kind of figures an article states in its own voice (families
  split twice), and 15 fixed periods whose fiscal year the article never writes (both families passed them; the council and a code check
  did not).
- **Council round 8** (`mx-codex-8.md`): undecided and stop; my "everything else met" outran the tally (the statement-level and link guards
  were computed by me beside it, not printed by it; a period the readers passed still needed checking against the rule's own words).
- *Lessons:*
  - A hypothesis can hold on its target and still fail to be adoptable: the same model that separates the sources also completes them.
    Guard the behaviour next to the target (what it does when the article is silent), not only the old behaviour.
  - Two reader families agreeing is not the rule being applied: both passed fiscal years the article never wrote. A line whose rule is
    mechanical ("the year is written in the item") gets a code check beside the readers.
  - Settle both arms' disputed marks, not only the candidate's, before comparing rates; and split a long packet before a reader stops
    at ten answers.
  - The tally script must print every line the design names, or the result will claim more than it shows.

## 7. The figure fields, second version (D497): empty unless the article says it

- **Alex:** "做第二版再测 (Recommended)" (about $0.90).
- **Diagnosed first, from the first arm's stored reasoning ($0):** it calls an outlet's "margins are expected to …" "gross margin guidance" at
  once, never asking whose; and it works a quarter's fiscal year out from "the next year (fiscal 2028)" or, once, from the publication
  date. The first definitions named neither case.
- **Change (arm c22):** the two field definitions reworded (a forecast is the company's only where the item says the company gave it; null
  when the item states no source anywhere; a fixed period only where the item writes that year, tied to the figure's quarter), and, from
  the blind audit, the `kind` definition clarified at its own field (an unattributed forecast is an estimate): three descriptions, the
  third disclosed. System text and closing check still c8's.
- **Design** (`figure-fields-2/PROBE-DESIGN.md`): ten stored states the first probe did not use (two unattributed forecasts, three market-
  beside-company statements, one control whose source is stated and must not be emptied, two articles that write no fiscal year, two
  openings). Council round 9 and the blind audit changed it before the send: a figure the control keeps and the arm drops now counts
  against the arm; the period's code check is presence only and the readers tie the year to the figure; the year-unknown cases need a
  minimum of kept figures; the tally prints every line with a verdict, smoke-tested on the first probe's marks before the send.
- **Sent:** `poc/data/clean-figure-fields-probe2-2026-11-15/stage1`, c8 and c22, three sends, 60 sends, ceiling $2.00.
- **Result (D498; `figure-fields-2/RESULT.md`, `tally-probe2.txt`, `guards-recomputed.txt`):** 60 valid sends, $0.69. Sixteen of eighteen lines met
  on the tally; both faults of the first version gone (no year the article does not write, 0 of 185; no unattributed forecast given to
  the company); the gain kept on new articles; the control not emptied. Not a pass: the all-figure source line at 10 of 185 by the strict
  reading (one over), 4 by the cases as written.
- **Council rounds 10 and 11** (`mx-codex-10.md`, `mx-codex-11.md`): two guards I called met were counted by the tally at a coarser grain than
  the design words them (recomputed: met, with their working printed); a figure I read as the company's was the writer's arithmetic
  (108 on 96.2 is 12%, the article says 17%); the two EPS figures are accepted by the cases as written, not by the standard.
- *Lessons:*
  - Diagnosing from the stored reasoning before rewording paid: both named behaviours were removed in one version, on new articles.
  - A tally that prints "met" must compute the line at the grain the design states; "by case" is not "by statement". Check a guard's
    grain when writing the tally, with an example where the two differ.
  - Check a figure's arithmetic before deciding whose it is: a number the company could not have given is not the company's.
  - A line set at one in twenty on about 185 figures turns on one figure. Either the sample is sized for the line or the line is read
    with its interval; I set a knife-edge and then stood on it.
  - Joining readers' files with `cat` joined two answers on one line; join by parsing.

## 8. The record test on unread articles (D499): c8's record against c22's

- **Alex:** "直接做记录测试 (Recommended)": the one-figure miss of D498 waived for this step; the council's "a pass comes first" stays recorded.
- **Question:** on articles no arm has read, does a record built by code from each request's kept figures let a reader answer six fixed
  questions without a wrong statement, and does c22's record do it where c8's led its reader to a wrong attribution (D494)?
- **Material:** forty articles drawn by seed from the 81 unread articles of 2026-09-29..10-05 that carry a revenue or margin figure (a text
  screen fixed before any answer); each read once by c8 and once by c22 against the week-end library (a constructed state; requests by
  the reviewed builder, a stored request rebuilt byte for byte first). 80 sends, all valid, $1.07 (ceiling $2.00); spend on the path $8.32.
- **Design** (`record-2/RECORD-TEST-2-DESIGN.md`; council round 12 before the send): the record builder written and checked on stored
  answers first (every line id traces to its statements and passages); matched articles only; a reader of each family on each record
  (four answer sets) and on the articles (two reference sets); comparers who first fix what the articles hold, item by item for the
  questions that ask for every estimate and every pair, then mark each answer supported, incomplete, wrong or none; fewer than five
  questions exercised is inconclusive, not a failure.
- **Result (D500; `record-2/RECORD-TEST-2-RESULT.md`):** eight of ten exercised parts supported for all four record readers by both
  comparers (the guide, the market's quarter estimate, the reported quarter, the margin path). By the line: c8's record met; c22's
  undecided on the two list questions. Read: not separated. Two disputed readings are in both records (an estimate dated "this year",
  a growth figure dated "Q3 2026"); one is c22's (a CFO's remark on customers' forecasts kept as a second growth figure). Sampled
  lines: sources 19 of 20 and 20 of 20 right; one wrong kind each. c8's wrong attribution of D494 did not recur.
- **Council (mx round 13), consensus:** the formal outcomes are kept and are not a ranking; c22 is not adopted; no further arm; the
  kept figures are shown usable on these articles, not complete, and a table is not shown to replace a tracked question; a grouping
  step may join only what the evidence establishes and never derives a quarter from the article's day.
- **Verdict:** the figure-fields line stops (c20, c21, c22: $2.56 of sends, then this $1.07 test). One choice goes to Alex: test a
  financial record as something the product shows ($0 first test), or return to the choice of system with D489 unresolved.
- **Lessons:** (1) a field built for a fault found on chosen cases is tested first where a reader would meet the fault; (2) a disputed
  part is settled for every answer set, or a stricter fresh reader weighs on one record only; (3) a question asking for "every" item
  needs its answer key fixed before the readers; (4) the reader's burden was the same fact under many names: identity, for code on what
  the evidence establishes.

## 9. A financial table built by code from what the adopted request keeps (D501): a $0 reader test

- **Alex:** "试做财务数字表 (Recommended)": no change to the system, nothing sent; the same figure on one line, the article's wording and
  source kept, an uncertain period not guessed; fresh readers answer the same questions.
- **Question:** does a code-only layout of c8's stored figures let a reader answer the same questions with no new error, and with less
  work than the plain record of D500?
- **Design** (`record-3/TABLE-TEST-DESIGN.md`, version 2): three code decisions, each a full match over a closed set (the source is the
  company; the stored period writes "fiscal", a year and at most a quarter; rows are one line when whose figure, kind, period key,
  measure and value are equal); measures are never joined across wordings nor values across precision. The builder carries its own
  must-stay and must-pass controls. 114 rows in 99 lines, 5 sections, 39 period blocks; 63 rows under a fixed period key; 10 joined
  lines.
- **Council (mx round 14) before any reader, five changes made:** the Q2 key credited a "this year" estimate as a fiscal-year one;
  the third Q6 pair needed its qualification; a joined line showed one article's qualification as if all gave it; a join the families
  mark differently must be undecided; pairs found are coverage, not effort. Also: the table shows the system's stored labels, not
  the article's words, and now says so (one stored period carries a fiscal year its article only implies).
- **Result (D502; `record-3/TABLE-TEST-RESULT.md`), $0:** no wrong join found in the ten joined lines (both families); all four table
  readers meet the answer line (eight parts supported, none wrong after the fresh pair on the one disputed part); key pairs found 1,
  1, 2, 3 on the table against 1, 2, 0, 2 on the plain record; tokens and seconds do not separate the layouts: no reliable saving
  shown. The table readers no longer complain of one fact under many headings; relative periods on market estimates and the same
  figure at different rounding remain.
- **Council (mx round 15), consensus:** report the written lines with their size, not "no error"; the table goes to Alex as a tested
  mock, not as the accepted handling of revenue and margin; a reading of the fresh week's three missed matters from such a table is
  fair as a separate question, D489's 2 against 4 unchanged.
- **Verdict:** one choice goes to Alex: review the mock and test it on the fresh week's three matters ($0); or tracked revenue and
  margin questions (D382, D384 reopened); or stop the table line.
- **Lessons:** (1) an answer key fixed before the readers brought the comparers to the same mark on ten of eleven parts; (2) a council
  read of the joined lines before any reader caught a display fault and a key fault; (3) do not promise Alex a measure ("saves work")
  the test cannot take; (4) a table inherits the stored labels' limits and must say what it shows.

## 10. The table on the fresh week (D503): can a reader find the figures of the three matters the new system had no question for? $0

- **Alex:** "看样表，并在最初那一周再验一次 (Recommended)": the same table from that week's stored answers, read blind for the three matters;
  a separate question, D489's 2 against 4 unchanged.
- **Design** (`record-3/TABLE-WEEK-DESIGN.md`, version 2; council round 16 before any reader, four rules added): a key of the company's
  outlook and market estimates from the seven articles D489's families tied to the matters, built from two reference readers and
  frozen first (twelve figures; three single-reader figures settled as belonging to the other matter); a code search of the table for
  each; two table readers a family; comparers marking each key figure found in the key article's line, found elsewhere, misstated or
  not found, and misleading extras; the joined lines relied on read by both families before the verdict.
- **Result (D504; `record-3/TABLE-WEEK-RESULT.md`):** M01 undecided (five of five found by all four; the extras split), M02 not
  findable (an article's own $700 billion never kept; the CEO's "double chip sales" found by two of four, its own article's
  statement kept with no figure), M03 not findable (the Bloomberg-compiled "under 72%", a line of its own, found by two of four).
  Eleven of twelve key figures are in the table. Nine of nine relied-on joins one claim. Stored-label faults on show: two market
  consensus figures filed under the company; three unattributed expectations stored as an outlet's forecast; one article's own
  wrong year.
- **Council (mx round 17), consensus, with three of Claude's points withdrawn:** the outcomes as the line gives them; D489 unchanged
  and "not clear", nothing ranks the systems; the table is a place to look figures up, not reliably read in one pass and no
  substitute for a judgement; tracked financial questions are Alex's option, not an established remedy; c20's cause cannot be read
  out of its stored reasoning.
- **Verdict:** one product question goes to Alex: for the company's major financial numbers, should a reader see the kept figures,
  get a tracked question with a judgement, have kept figures reach related judgements, or several.
- **Lessons:** (1) a conclusion stays what its pre-written rule gave (Claude proposed "the new system is ahead" on a "not clear"
  comparison); (2) comparers told to judge by a short stored passage cannot settle what the article says elsewhere; (3) with four
  readers the count that found a figure is the result; (4) a stored reason is not a cause.

## 11. Do the kept financial figures reach the judgements of related questions? (D505) $0

- **Alex:** "进入相关问题的判断 (Recommended)", the only option he chose: figures are evidence for related judgements, not a table and not
  questions of their own; first a $0 check; "有就报给你，没有就停".
- **Design** (`delivery/DELIVERY-CHECK-DESIGN.md`, version 2; council round 18 before any reader, four changes): the standard is PRD
  10 §1 ("the facts that can change its answer", with onward reasoning), not a new one; a census by code of what each judgement
  request was shown; both families list, one question a packet with a completion line, the table lines that bear on each of the
  seven questions; each candidate read in the stored request and by a fresh pair shown everything the judge had; three outcomes
  (finding, none, undecided).
- **Result (D506; `delivery/DELIVERY-CHECK-RESULT.md`):** a judge is shown exactly the linked statements (196 links). One finding: the
  credit-support question held "nearly 2 gigawatts" as a volume and never received the company's revenue opportunity per gigawatt
  ($25 and $40 billion), kept from two articles (one linked to the Vera Rubin question only, one to none); all four readers say it
  bears. Six open leads. No missing figure established for five questions. All seven judgements of that question were in its top
  band; the effect of the figure was not measured.
- **Council (mx round 19), consensus with corrections:** the finding stands as two figures, one question; a conditional indication
  of scale, not a guarantee; no counterfactual, no rate; no census of the 389 unreceived statements (beyond his scope, blind to
  statements linked elsewhere).
- **Verdict:** reported to Alex as found; nothing built on one instance; an open defect of the new system.
- **Lessons:** (1) delivery is read in the request, never inferred from a same-claim group; (2) a first reader's list is a lead,
  what the judge already had decides (29 one-family candidates became five leads); (3) apply every condition of the frozen rule when
  sorting by hand (one line was filed as delivered against the period rule); (4) write what was observed, not the counterfactual.

## 12. How large is the gap? A census over everything the new system kept in the fresh week (D507) $0

- **Alex:** "先查清这类缺口有多大 (Recommended)": all kept statements, those linked to another question included, against the seven questions;
  the scope widened by his word beyond the financial figures; then decide whether to change anything.
- **Design** (`delivery-class/CLASS-CENSUS-DESIGN.md`, version 2; council round 20 before any reader, three changes): the standard is
  PRD 10 §1 again; 567 statements in six parts, each read by both families against the seven questions with all seven keys written
  for every statement; candidates by code (listed, not linked); a fresh pair shown everything the judge had and the whole article of
  each candidate, marking the one fact judged, in the article, already shown and bearing apart; confirmed only when both say in the
  article, not shown and bearing; repeats merged into facts by hand with the reason recorded; the confirmed count is a minimum found
  by this reading, not a complete census.
- **Result (D508; `delivery-class/CLASS-CENSUS-RESULT.md`):** 63 candidates; confirmed five statements, three fact-and-question pairs
  in three questions (the CEO's doubling of chips sold under supply commitments; Washington's silence on the RTX Pro 5500 under the
  Blackwell-approval question; Beijing's 2025 stop order on the RTX Pro 6000D under the RTX Pro 5500 question, read before that
  question opened and bearing against its answer "yes"); 23 unresolved pairs; 35 dropped. The fresh families' bars differ (53 against
  34 of 63 marked bearing). D506's finding is open under this rule. The system's own links: 64% and 55% also listed by the readers.
- **Council (mx round 21), consensus with corrections:** three pairs and 23 unresolved pairs, a minimum; no "small", no rate, no
  ruler for Alex to set from the split; the one test to offer is the effect on the judgement, on the strongest case only (six calls).
- **Verdict:** reported to Alex with that one test for his word; nothing built.
- **Lessons:** (1) count in one unit; (2) a finding is the output of its rule and its readers: the same fact was confirmed by four
  and split by two; (3) check a reader's reason against the written test; (4) after a census, test the effect where the product is
  judged, on the strongest case first.

## 13. Does one missing fact change one stored judgement? Six calls (D510, D511; under D439 after Alex went inactive, D509)

- **Authority:** Alex inactive (D509); the council and Claude had agreed on the test (round 21); design to the council before the
  send (round 22, four changes: attempts saved before parsing; the judge's own answer check; retries counted; a complete separation
  required for "confidence fell").
- **Hypothesis:** the missing precedent (Beijing's 2025 stop order on the RTX Pro 6000D) would move the RTX Pro 5500 question's
  answer off "yes" or lower its confidence. **Change:** the stored request as stored against the same with the one stored statement
  inserted, three sends each. $0.0093.
- **Result:** inconclusive by the rule written first. Six of six "yes"; the two blind rankings overlap and the controls span the
  range; the judge marks the statement against "yes" in three of three and names it in none; the request already held a like
  precedent (blocked H200 imports).
- **Council (mx round 23), consensus:** pause the delivery line, defer the change, keep the defect open; a cold reflection council
  next, one product-ranked step from the whole record.
- **Lessons:** (1) read the control for facts of the same kind before writing the measure; (2) a reader's "bears" is not a judge's
  changed answer; (3) the judge's structured marks are a more sensitive observable than its reasons: pre-register them; (4) stepping
  back is a decision, taken from the goal.

## 14. Reflection council "my" (D512, under D439): step back from the corner; a decision page for Alex

- **Why:** D511 paused the delivery line after several steps in a row separated nothing; the council loop's own rule and D466 call for
  a cold reflection.
- **The cold reviewer's reading (`council/my-codex.md`):** neither system has earned the choice; the sequence promoted the most recently
  exposed defect into the next priority; the council corrected overclaims and not the direction; the losses ranked by what they cost
  a reader: an answer unsupported by its evidence, a big matter with no judgement, a relevant fact that does not reach a judgement,
  clutter and wrong labels.
- **Claude's reflection (`council/my-claude.md`, written first):** the same reading of the record; candidate next steps: a second
  fresh week, a decision page, the structural cause of the delivery gap, the Step 4 faults.
- **The disagreement and its end:** the reviewer proposed re-reading the 22 last judgements; Claude asked what it adds over reading
  B and how its result would bear on the choice; the reviewer withdrew it. **Consensus:** the decision page first, with the week's
  evidence, Alex's choices since, each system's cost to a reader, one recommendation and one test; a $0 trace only if it can change
  a named line on the page.
- **Lessons:** (1) each next step is tested against the path's own question before it is designed ("could this change the choice of
  system?"), by the council as well as by Claude; (2) the largest named difference is not the next priority by itself: re-rank from
  the goal after every result that separates nothing; (3) a proposal is challenged on what it adds over what the record already
  holds; the reviewer's own proposal fell to that question.
- **The page's first draft, reviewed (round 3):** not ready: a dozen sentences wrong or stronger than their records ("235 unseen";
  links counted as statements; "nobody has read" the dropped statements; "changed nothing visible"; "never placed later"; "same
  matching"; "not run since"), and a recommendation to select the new system that the evidence does not support. Rewritten as
  version 2 with every correction checked against its record: the council's advice is to keep the default and both systems and not
  to choose from this evidence; one registered comparison is named as the test that could decide it.
- **A correction to the record itself (D513):** the reviewer's citation of the later-linking count showed that D506 and D508 had
  mis-stated the cause: the new system does look back when a question opens, at statements with no link (516 judged, 2 linked);
  one already linked elsewhere is not reconsidered. Five pages carry a dated correction; no count changes. The class had been
  traced on 2026-11-13 (D456) and was not cited.
- **Lessons:** (4) a mechanism sentence ("nothing does X") is checked in the code and the stored run before it is written; (5) the
  decisions and earlier traces are searched for the mechanism by name before a census is designed, and again after a context
  compaction; (6) a page for Alex is drafted from the records with each number's unit and date beside it, and reviewed cold before
  he sees it: the first draft's errors were all of one kind, a summary written from memory of the record instead of from it.
- **Rounds 4 and 5:** the page ready after named edits (the look-back rule worded on groups and on how the first statement arrived,
  D514; the six answers; the July comparison in its own words; the cost figure removed). **Consensus (D515):** the page is the
  reflection's outcome and is left for Alex; nothing further is sent or run on the lean path until he answers; no step outranks
  waiting.
- **Where the path stands:** spend $8.33; D489 "not clear"; the delivery defect open and paused; one decision with Alex.

## 15. Could an affordable comparison choose between the systems? The sizing (D516, D517; under D439) $0

- **Why:** the stop at D515 was a wait on Alex, not a finished step; the reflection council (round 6) superseded the wait with a $0
  sizing of the comparison the decision page named.
- **Done:** `comparison/draw_counts.py` (what each stored draw holds), `comparison/sizing.py` (the smallest difference a comparison of
  a given shape detects; checked by simulation), `comparison/COMPARISON-SIZING.md`.
- **Found:** the three reader-based lines a choice would rest on have one draw of each system on each of two windows and no repeat.
  A week ends with 7 questions on the new system and 15 on the old; under simple assumptions the shapes the money allows detect
  differences of roughly 22 to 38 points or more. On "answers supported" the sign of the difference flips between the two windows.
- **Council (round 7):** ran the script, reproduced the figures and corrected the first wording ("30 points or nothing"; "nothing
  seen suggests"; one 40% figure; a row claiming a check against full articles; unread weeks and costs stated as facts).
  **Decided (D517):** this comparison is not sent. The decision page's last section says so in plain words.
- **Lessons:** (1) size a test before proposing it as "the one test that could decide": the page had offered a comparison nobody
  had sized; (2) a power calculation is an illustration under its assumptions, and is written that way; (3) reading the earlier
  away-period first (D477 to D482) showed that "the answer-choice step's owed tests" were a line stopped for cause, not waiting work.

## 16. The same week, both systems, side by side (D517, D518; under D439) $0

- **Why:** if measurement cannot choose, a reader has to see the product, not counts about it.
- **Done:** `side-by-side/build_side_by_side.py` writes `SIDE-BY-SIDE-WEEK.md` (a front page of about 3,800 words, then all 22
  questions with every possible answer, the latest answer, its reasons and both reviewing teams' marks) and
  `SIDE-BY-SIDE-WEEK-CITED.md` (every statement each latest answer cites, with its stored passage and the stored request's
  identity). Everything is stored text except the pairing of questions by subject and the notes on how each pair differs
  (`shared-subjects.json`, the council's words).
- **Council (rounds 8 and 9):** the first build was not ready (it cut every answer condition of 70 characters or more, showed no
  cited statement, compared two different populations in its examples without saying so) and my reading "where they overlap they
  say the same thing" was wrong: on four of six shared subjects the two systems ask different questions or use different scales.
  Rebuilt; left for Alex beside the decision page. **Decided (D518):** production stays the default and both systems stay; what
  would change it is named.
- **Lessons:** (1) two answers are compared only after their two questions are read side by side; "both say yes" hid different
  conditions; (2) a builder that shortens stored text silently is a defect: print in full or mark the cut; (3) a page for judging
  needs the sources behind each answer, not only the reviewers' verdicts.

## 17. When does the judge give an answer its evidence does not support? Census and four accounts (D518, D519; under D439) $0.0041

- **Why:** the council's product-ranked next investigation: an answer its evidence does not support is the loss a reader pays most
  for, and the judge is shared by both systems.
- **Searched first:** both earlier readings of the judge (D426's baseline, Stage B) had recorded their failing answers with my own
  read of each. The census joins four stored readings instead of reading again (`unsupported/inventory_earlier_readings.py`,
  `class-by-judgement.json`, `tally_unsupported.py`, `UNSUPPORTED-CENSUS.md`).
- **Found:** 438 readings of answers; 36 settled as unsupported (10) or as too little to prefer a band (26). 31 of the 36 are one
  situation: an amount is asked, nothing shown is enough to size it, and a band is named anyway (three matters, eight question
  paths). On the credit-support total, in four runs, every answer of the first five days fails and the readers pass all 31 answers
  from the day a sized amount is in view. Three more rest on a step of the judge's own (a one-fifth discount, a 25% growth, a
  scaling ratio).
- **The judge's own account (four calls, $0.0041; `unsupported/ACCOUNT-RESULT.md`):** in all four the judge, asked plainly, says the
  band rests on an assumption it introduced that the evidence does not give; in the two unsized cases it adds that its own
  instructions forbade the band. Checked against the stored requests: each figure it calls its own is absent from the evidence.
  Found on the way: the 25% and the one-fifth come back to the judge inside its own previous answer, which the request shows and
  the instructions tell it to carry.
- **Council (round 9):** reproduced the counts, read six hand classes (all stand), and corrected the page (readings are not
  independent cases; two situations of the evidence, not two proven mechanisms; "missing" and "abstract" are narrow readings; D59
  does not cover the case; timing is not cause).
- **Lessons:** (1) the search of the earlier record came first this time and replaced most of a planned reading; (2) a count over
  daily answers is a count of readings: say how many questions carry it; (3) the judge's own words in the stored answer already
  said nothing sized the amount: read the stored answer's fields before asking the model anything.

## 18. The judge line stops at a choice for Alex; the old system's duplicate questions traced (D520; under D439) $0

- **The judge line:** the council (round 10) found one of my readings of the accounts wrong (the one-fifth discount was new in its
  answer, not carried from the previous one) and asked for a $0 design. The design note (`unsupported/DESIGN-NOTE.md`) traces two
  questions day by day, shows by a keyword count that most answers the reviewers pass also state an assumption or an estimate, and
  finds that a label has no path to the next day's request as the code stands and that what the product shows is an open choice.
  By the council's stop rule nothing is sent. Round 11 struck my sentence "the council's lean is B": it had named a possible
  choice, not a recommendation.
- **The duplicates:** `duplicates/DUPLICATES-RESULT.md`. In each of the three pairs both reader families found facts that bear on one
  question and were shown only to the other's judge; no pair's answers differ in band; in the RTX pair the less-informed answer is
  the one a separate reader had marked unsure for the missing fact. The stored matching records give three different reasons for the
  three second questions.
- **Lessons:** (1) I put words in the council's mouth ("lean is B"); a consensus is quoted, not paraphrased upward; (2) link counts
  were a lead, the judge's actual request was the measurement: the council asked for the dated requests before any claim, and the
  reading by claim (not by record number) is what separated repeats from missing facts; (3) my own read, written first, was
  narrower than both families' on one pair (I counted only facts that could decide; they also counted facts that corroborate):
  the brief's "bears" has to say which is meant; (4) a cause on record for one case (D354) is not the cause of the next three:
  the stored matching record of each was one query away.

## 19. The same-day candidates against the decision in force (D521; under D439) $0

- **What the council corrected (round 12):** the shipment-target statement was written on 09-27, not 09-28 (I had inferred the day
  from which answer was judged last instead of reading the statement's own record); "no pair's answers differ in band" set an
  amount beside a growth rate; sixteen "facts that bear" were what readers listed, not losses; and **D375 had already superseded
  D251**: my search of the decision index for "same day" did not reach a row titled "Read the latest committed research library
  before each item".
- **Done (`duplicates/same_day_pairs.py`):** ten same-day candidate pairs in four stored runs; six are two questions of one
  article; in the four where different articles of one day opened questions on one matter, the later article's stored reading
  request printed exactly the questions open at the day's start and not the earlier question. The later comparison kept the pair
  apart in three (three different verdicts) and did not compare them in one.
- **Lessons:** (1) search the decisions for the mechanism by what it does ("list of open questions", "snapshot", "each item
  reads"), not only by the name I gave it, and read the status column: a superseded decision was the one I cited; (2) date a
  statement from its own record, never from the answers around it; (3) a count of what readers listed is labelled as that until
  each item is checked.

## 20. A probe designed twice on a wrong premise, withdrawn; the duplicates traced to the comparison step (D522, D523; under D439) $0

- **What happened:** I proposed a paid probe of the reading step (show the earlier same-day question; expect no second question).
  The council refused it twice. Round 13: one inserted line is not the list D375 means; the answers must pass the real checks on
  the state of that moment. Round 14: the pass condition contradicts the frozen prompt, which tells the reader to propose a
  question even when it is open.
- **What the $0 work established on the way:** the production code rebuilds every stored reading request from the run's store read
  at the day's start (stored keys match), builds the per-article list by the same code, and its checks and filing reproduce the
  stored handovers in isolation. Then the trace: the comparison step's list is "same typed key, else text search, plus the
  day-start list"; one second question (RTX) was never compared; the others were compared and kept apart.
- **Lessons:** (1) read the whole frozen request before designing anything on a step: one sentence of the prompt voided two
  designs and three council rounds; (2) trace to the step that takes the decision before testing the step that precedes it: the
  stored matching record named the deciding step from the start; (3) count the class before proposing a probe: "never compared"
  is one duplicate in 54 opened questions; (4) the $0 machinery built for a withdrawn probe (historical rebuild, checks in
  isolation) is the reusable part.

## 21. The $0 proof of D375's per-article list: design reviewed three times, stages 1 and 2 built (D524 to D526; under D439) $0

- **Why:** the council refused to close the path (round 15): D375 is already Alex's decision, and a $0 proof can show what building
  it changes before any send.
- **The design** took three versions (`duplicates/D375-PROOF-DESIGN.md`). The council's points that changed it: a changed comparison
  request is a new request and no stored answer is its answer; a stand-in for the reading answer must be called one; recovery is
  shown by interrupting and resuming, not by rebuilding a list; a resumed run legitimately leaves audit records, so equality is
  the wrong test; "contains the day-start list" is not an invariant.
- **Built and run so far:** the production replay with the network refused rebuilds the stored run to article 174 (24 tables
  compared, three differences accounted for); article 175 through the real entry point reproduces the stored run exactly;
  the per-article list checked over 964 article reads; it is longer than the day-start list for 150 of 235 fresh-week articles.
- **Lessons:** (1) a stored run with its archive is a free, exact test bench when the replay is deterministic: prove that first
  (every request found, every table equal) and the rest of a proof costs nothing; (2) compare whole stores by a generic
  table-by-table reader and then explain each difference by a query, never by a guess; (3) the count that mattered appeared on
  the way: D375 changes the reading of most articles, so its effect is on filing far more than on duplicates.

## 22. The D375 proof: stages 3 and 4 run; not yet passed (D527; under D439) $0

- **Run:** the per-article list makes exactly one request the stored run never made (the relation to the question opened earlier
  the same day); with labelled fake answers the real checks and writer join the candidate ("same") or change only the
  comparison's record ("different"); cases B and C unchanged; four interruptions through the bounded replay resume to the same
  product state (`duplicates/D375-PROOF-RESULT.md`).
- **Council (round 18):** case-specific wiring findings, three overstatements corrected, and the registered proof not passed until
  its missing checks are built. It also refused my position that measuring D375 must wait for Alex: under D439 that decision is
  the council's, after the proof and a priced design.
- **Lessons:** (1) a proof passes when the script fails on a violation, not when I read its printed tables and find them as
  expected; (2) a fake that accepts requests "by kind" is wider than the plan it stands for: name each planned request;
  (3) a difference seen in a run and then called "allowed" was not declared: register it, then rerun; (4) I read "frozen, his to
  open" as a reason to stop twice in this stretch (closing the path; deferring the measurement), and the council read D439 as
  written both times.

## 23. The D375 proof: every registered check built and holding (D527; under D439) $0

- **Built after the council's round 18:** `duplicates/d375_shown.py` (9,149 listed questions over 964 articles carry the groups and
  other names of their sequence; a synthetic same-day closure); `d375_proof.py later` (a later article behind an interrupted
  one: eight requirements); the arms' allowed differences and end states and the interruptions' expected records as checks that
  fail the script; the fake restricted to the named planned requests; three mutants that fail.
- **Result:** every check exits 0; the mutants exit 1.
- **Lessons:** (1) writing the expectation into the script before the run is what separates "it did what I predicted" from "I
  explained what it did": one arm's difference had been explained after the fact and had to be registered and rerun; (2) a
  check needs its own failing case: three one-line mutants took minutes and are the only evidence the checks judge anything;
  (3) the whole proof cost nothing because the first hour went to proving the replay deterministic.

## 24. The D375 proof passes as a bounded serial proof; the measurement is to be designed small (D528; under D439) $0

- **Council (round 19):** the checks allowed whole tables to differ, wider than the design's "any other difference fails"; the
  recovery checks allowed failure records without requiring them. Both fixed, with a fourth mutant (an unrelated row inside an
  allowed table). By the council's stated condition the proof is a passed, bounded serial proof.
- **The measurement's direction (round 19):** the request must say truthfully what its list is, so the list and its wording are
  one change; the first test is the smallest end-to-end one, on complete days with same-day openings, against a default control
  re-sent the same day; the prediction is about facts received by the final judgement, with a harm control.
- **Priced at $0 from stored token counts:** a 14-day draw of the default is $0.49 to $0.58 at published rates, a 7-day draw $0.47.
- **Lessons:** (1) "allowed tables" is not "allowed rows": a check as wide as a table passes anything in it; (2) allow and require
  are different checks: an expected record that may be absent proves nothing; (3) I proposed three full draws on archived
  controls; the PRD's own section 6 forbids an archived control, and I had not reread it before proposing.

## 25. Eligible cases for measuring D375, read on the stored week (D528; under D439) $0

- **Done:** 728 statement-and-question items in 20 packets, two reader families (`d375-measure/SAME-DAY-CASES-RESULT.md`): 37 pairs
  both mark as bearing and not reaching the question on the day it opened; 14 dropped for want of a question (9 distinct
  statements, all read by me); 17 of the 23 kept elsewhere are the duplicate RTX pair.
- **Found:** on its first day the fiscal 2027 revenue question was judged on one statement while the quarter's revenue and the next
  quarter's guidance, read the same day, were dropped; the same for the report that Vera Rubin shipments had begun. By keyword,
  each such fact reached its question one or two days later.
- **Lessons:** (1) find the eligible cases before designing the measurement: the prediction the council asked for (facts reaching
  the final judgement) would have been unexercised in this week; (2) "dropped" is not "lost": check what arrives later before
  counting a loss; (3) a keyword check of arrival is a lead and is labelled so.

## 26. The trace into the final requests finds one question that never received its guidance (D529; under D439) $0

- **Why:** the council (round 20) would not stop the line on a keyword lead: "dropped, then arrived later" had to be read in the
  actual final requests.
- **Found:** for 13 of the 15 traced pairs a statement of the same fact was in the final request. For the data-center revenue
  question it was not: the next quarter's guidance and the year's market estimate were filed under the total-revenue question
  all week and never shown to it. Its final answer is the one both reviewing teams called unsupported: it carried 18% and
  "allowed" 25% of its own.
- **What it joins:** the judge census asked whether a missing input explains unsupported answers (round 8); here, for the week's one
  agreed unsupported answer, a missing input exists. And it is PRD 10 §2's relation, on the default system.
- **Lessons:** (1) my keyword check had said "a like statement reached the question" for the guidance, because I searched the two
  revenue questions together; reading each question's own request separated them; (2) the stop I recommended (round 20, option a)
  would have closed the line one query short of its most concrete finding; (3) trace a fact to the request of the question it
  bears on, not to "the system".

## 27. The missing-input case is recorded; its mechanism is sized before any test (D530; under D439) $0

- **Council (round 21):** a confirmed missing-input case, cause unresolved; my six-call test refused for now (two added facts cannot
  be told apart; the judge's 25% already stands in its previous answer; facts shown as new do not reproduce when it would get them).
- **Next:** the ten settled unsupported answers of the census, each checked for a relevant figure that existed in the run and was
  absent from the request.
- **Lessons:** (1) one case is a lead: count the class on the records already paid for before designing its test (AGENTS §1, which I
  skipped by proposing the test first); (2) "it bears by one step" was my inference: the figure's relevance has to be shown from
  the source and the request; (3) naming the PRD's relation is not naming the rule that produced the filing.

## 28. A missing figure explains three of the ten settled unsupported answers (D530; under D439) $0

- **Done:** each settled unsupported answer searched for a sizing figure present in its run's store and absent from its request,
  then read (`missing-input/MISSING-INPUT-RESULT.md`).
- **Found:** three of ten (two of six distinct matters): the fresh week's data-center revenue answer (guidance and consensus under
  the total-revenue question) and the custom-chip answers of two readings (Broadcom's guided AI revenue kept with no question;
  delivered the next day, and the answer then passed). The other seven had no figure to deliver.
- **Lessons:** (1) the judge line and the delivery line are one line for these answers: an answer the reviewers fail can be the
  judge's own number or a number the system held and did not deliver, and only the request tells which; (2) the stored runs
  already hold natural before-and-after pairs: look for them before proposing a send.

## 29. The two filings traced: each a written rule working as written (D531; under D439) $0

- **Council (round 22):** corrected my clean-path case (the statement arrived before the question opened: a later-linking decision)
  and my sizing words ("coincided with", "none found").
- **Traced (`missing-input/FILING-TRACE-RESULT.md`):** the old system's reading step filed the guidance under the total only, as its
  prompt asks; the new system's later-linking check refused Broadcom's guidance (0.12) under wording that excludes a supplier's
  overall guidance. In both, "about the question's own matter" is the test, and "bears on it through a related quantity" is
  outside it.
- **Lessons:** (1) I called it "kept with no question while the question was open" from the hand-written stand-in question of the
  baseline; the system's own question opened later: check which question the system itself held, and when; (2) reading the raw
  answers before the checks showed at once that no check was involved; (3) before blaming a filing, read the rule it followed:
  both followed theirs.

## 30. No common mechanism from two cases; the dependency lead goes under D368 (D532; under D439) $0

- **Council (round 23):** the two traces hold as observed; "a rule working as written" overstated them (the old system's link
  instruction names indirect evidence, which I had not quoted); and D368 already decides the dependency selection I presented as
  a lead.
- **Lessons:** (1) twice in this stretch a decision in force covered what I presented as new (D375, D368): search the decisions by
  what the mechanism does, in the log's text and not only the index's titles, before writing "a lead"; (2) quote the whole rule:
  I cited the prompt's sentence and missed the answer form's own instruction for the same field; (3) two cases that look alike
  are two cases.

## 31. The dependency lead stops: the facts would have to travel the other way (D532; under D439) $0

- **Done:** the 22 reference facts the old system linked to another question only, each against the stored relation of the two
  questions, D368's direction and the conclusion a judge would receive (`missing-input/DEPENDENCY-TRACE-RESULT.md`).
- **Found:** one of 22 in the direction a dependency serves, with no figure. Sixteen sit under a broader question (company-wide
  revenue; a total) and bear on a narrower one. The stop rule applies.
- **Lessons:** (1) a channel has a direction: check it before counting what it could carry; an hour's trace removed a lead I had
  been ready to propose as a step; (2) the lean path's investigations of the old system keep arriving at the same place, the
  company-wide revenue question as a home for indirect evidence, which PRD 10 already names: say so, and stop re-deriving it.

## 32. This stretch closed and consolidated; the next slice is D368's channel on its own terms (D533; under D439) $0

- **Council (round 24):** close and consolidate; keep the default and both systems; do not make waiting the next task; assess D368's
  dependency channel separately on a stored, correctly directed case.
- **Done:** the decision page's section 7 (open choices; decisions awaiting implementation and acceptance; defects with evidence).
- **Lessons of the stretch, in one place:** (1) every reviewer correction that mattered came from reading a stored record I had
  summarised instead of read (the prompt's own sentence; the library's later-linking log; a statement's own date; D375; D368);
  (2) the cheap, decisive work was always the trace to the request a judge actually received; (3) I proposed to stop four times
  and the council found a cheaper true next step each time: a stop is a claim to be tested like any other.

## 33. D368's dependency channel on stored, correctly directed cases (D533; under D439) $0

- **Done:** `dependency-channel/CHANNEL-ASSESSMENT.md`: on a frozen seeded draw, the line each supported question would receive under
  D368's direction, built in the production format from the stored conclusions.
- **Found:** 8 of 14 lines would have carried a figure the receiving request did not hold; some are the supporting judge's own
  derived numbers. No judgement re-run.
- **Lessons:** (1) a decided, unbuilt slice can be assessed on stored runs of an older configuration that still held the edges:
  look for the configuration that exercised the mechanism before calling it unexercised; (2) a channel that carries conclusions
  carries the assumptions inside them: this meets the judge's own-number finding, and a design has to tell the two apart.

## 34. The channel assessment corrected: its lines came from the future (D534; under D439) $0

- **Council (round 25):** I picked each supporting conclusion by "sequence not later than the receiver's"; in a day-end round all
  judgements share one sequence, and the supporters were judged after the receiver and had read its conclusion. The eight lines
  are a lead, into two questions.
- **Lessons:** (1) inside one round, order is the judgement's own number, not the day's sequence: I broke the rule this repository
  states for itself (order comes from a sequence the program owns) by using the coarser of two sequences; (2) before counting what
  a channel would carry, write down when each piece of it existed; (3) "eight lines" was "two receivers": name the unit a test
  would actually send.

## 35. The stored chronology: no supporting conclusion exists that had not read its receiver (D534, part 1; under D439) $0

- **Done:** for the two receiving questions of the seeded draw, every call ordered by judgement number: from the second day on each
  supporting conclusion that existed before a call had been produced with the receiver's earlier conclusion in view.
- **Means:** D368's direction cannot be tested by rearranging stored conclusions; the supporters have to be judged afresh without
  the receiver's conclusion. The $0 part that remains is the ordering-and-propagation proof with labelled fake outputs.

## 36. D368's ordering and propagation exercised with fake outputs (D534, part 2; under D439) $0

- **Done:** `dependency-channel/ordering_proof.py`: one extra round through the production judging round on a scratch copy of the
  seeded draw, the edges read in D368's direction for judging only; seven registered expectations hold; a mutant keeping the
  stored direction fails six.
- **Seen on the way:** in the stored direction one changed supporter fans out to nineteen judgements (it changes a theme, and a
  changed theme queues every open company question); in D368's direction the same change queues three.
- **Lesson:** the two uses of one stored edge (who reads whose conclusion; which question is the narrower home) live in two
  functions, so the direction of one could be exercised without touching the other: find the seam before assuming a frozen file
  must change.

## 37. The ordering proof accepted as a wiring result; two $0 checks before a measurement design (D535; under D439)

- **Council (round 26):** accepted with limits; corrected my description of the frozen reference (it does use other questions'
  evidence and its total-revenue view); a measurement must start from a verified state of 2026-07-14 before that day's judging,
  never from an extra round after the window; a two-sided question needs registered harm, benefit and inconclusive.
- **Lesson:** I described the reference's reasoning from the first lines of one entry; the entry's later lines said the opposite.
  Read the whole record before characterising it (the same error as the prompt's sentence, the library's log and the statement's
  date earlier in this stretch).

## 38. A source-backed case and a verified rebuilt state for D368's direction (D535; under D439) $0

- **Done:** (a) each figure of the eight supporting lines looked up in the passages the supporting judgement cites: one clear case,
  the Vera CPU target reaching the data-center question, which holds no Vera CPU statement of its own; (b) the seeded run rebuilt
  to 2026-07-14 before its judging round from stored answers, verified table by table, and the stored-direction round re-run from
  it identical to the stored one.
- **Found on the way:** a cached replay stops at the first answer the code's own check once refused, because the archive keeps such
  answers under a separate key on purpose; handing the stored refused reply back reproduces the history exactly.
- **Lessons:** (1) a failed rebuild is a question: the first differing line named the cause in two queries; (2) the state a
  measurement needs can be rebuilt and proved identical before a cent is spent, and the control re-run from it is the proof that
  the harness adds nothing of its own.

## 39. The reversal is not measured now; the next census is on the unseeded week (D536; under D439) $0

- **Done:** the whole round dry in D368's direction (14 to 18 calls, seven expectations, mutant fails); the reference's ten facts
  for data-center revenue traced by statement id and then through the whole request; the stored seeded draws scored on the frozen
  reference (15, 15, 16 of 17); judgements shown not to feed back into reading or matching (the 14 days replay with every
  judgement a fake and the same 589 links).
- **Council (round 27):** send neither shape; my table counted statements only (the consensus, the guidance and the H200
  permission already arrive through the total-revenue line or the theme block); stored conclusions are leads; a gain on the frozen
  reference is not impossible; D368 item 4 stays recorded and is not replaced here. Next: a $0 design census of dependency
  selection on the stored unseeded week, with a stop rule.
- **Lessons:** (1) search the earlier results by what the mechanism does before a task starts, and read a decision's item whole
  with who settled it: the arrows were traced and reviewed on 2026-11-03 and 04, and item 4 was a delegated settlement (second
  time, after D513); (2) "was the question shown this fact" is asked of the whole request (statements, the lines of other
  questions, the theme block, the previous conclusion), not of the statement list; (3) a lookup by wording matched statement ids
  ("e392"): match by id, then read; (4) score the stored runs on the frozen reference before designing a test of a change: the
  room it leaves decides what a send can show; (5) a mutant that stops on an error has caught nothing until the error is read.

## 40. Where a dependency could have been chosen, and what one edge would do (D537, D538; under D439) $0

- **Done:** the census of the unseeded fresh week (`dependency-selection/DEPENDENCY-SELECTION-CENSUS.md`: 97 pairs, own read first,
  two blind readers); the edge proof (`EDGE-PROOF-RESULT.md`: judging on the last day through the real checks, thirteen
  expectations, two mutants; every stored reading filed again with and without the edge).
- **Found:** one clear case (data-center revenue reading total revenue: the consensus and the guidance it never received); the
  driver relations an analyst wants most run from a later question to an earlier one; the same edge that shows the conclusion to
  the judge removes seven filing links through the narrowest rule, one of them a statement the broader question cites.
- **Council (rounds 28, 29):** corrected two figures of mine (the $96.2 billion quarter was already in every request; one of the
  three statements says $96 billion); the judging proof is conditional; a lost filing is not a changed answer; the six-call test
  is deferred; the slice's design is opened at $0, the separation of the edge's two uses first.
- **Lessons:** (1) before testing whether a new input helps a judge, trace every other reader of the record that would carry it:
  the edge had a second reader in filing; (2) a control that reproduces the stored run (all 235 filings; the last round) is what
  lets a seven-statement difference be believed; (3) a comparison that fails everywhere at once is the harness (row objects
  against tuples; a store read from a worker thread): read the first failure before the result; (4) the matching step already
  stores a closed relation for every compared pair: look at what is recorded before designing what to ask.

## 41. The separation design, two proofs, and the council's first review (D538, D539; under D439) $0

- **Done:** `dependency-selection/SEPARATION-DESIGN.md` (the rule, the four tables, what stays open); `separation_proof.py` (35
  expectations; mutants fail 13 and 12); after the council's round 30, the inventory of every stored ledger's dependency rows
  (`edge_inventory.py`: 1,138 and 395, none other) and `separation_proof_2.py` (19 expectations; mutants fail 1, 2 and 4): the
  production writers store the kind and a whole week replays with the chosen dependency in place.
- **Council (round 30):** a candidate, not a contract. My "the rule adds nothing" was wrong (it reads D265 more narrowly); my
  "only one edge between two questions" had a counterexample (a same-direction duplicate is not a circle); "kind is never
  inferred" contradicted my own table for old rows; the pages and the idea route are readers of the meaning, not of a label.
- **Lessons:** (1) when a design says "this adds nothing to the decisions", list the one sentence it reads differently: there
  was one; (2) state a rule over pairs as a table of every combination before calling it a rule: the counterexample was the
  second row; (3) a contract and its migration must be read against each other in the same sitting; (4) with filing proved
  unchanged, the whole week could be replayed at $0 with the edge in place: the conditional proof of the day before was a limit
  of the unseparated edge, not of the method; (5) a crash with no traceback was one archive connection read by several threads,
  after I rebuilt stored history under the seam: rebuild history as stored, apply the change after.

## 42. The filing and label contracts of the separation, finished (D540; under D439) $0

- **Done:** `dependency-selection/filing_contract.py` (ten cases through the code's own rule: what the reading step linked, what the
  rule leaves with and without a stated hierarchy, what the decisions call for); the label outcomes in the seam and the second
  proof (20 expectations); the inventory widened to snapshot folders and bounded to what it read.
- **Found:** in every real case the reading step wrote one item linked to both questions; each code state gets five of the ten
  right, a different five; no reading of an edge yields the expected homes. The label the seeding module writes on every seed
  edge (`last_end`) is defined nowhere.
- **Council (round 31):** the candidate is provisional; a two-figure sentence under both questions is D360's intent, not an
  error; the second proof forces stored answers back and is not a live judge's sequence; a different label is a conflict, not a
  duplicate.
- **Lessons:** (1) before calling a double link an error, read the decision that makes one on purpose; (2) a count of records
  with a property is not a count of breaches; (3) a test of a judge over several days is a sequence, each arm from its own
  earlier answers: saved requests sent in isolation answer another question; (4) when a stored value's meaning is written
  nowhere, say so and return it; the proof reports it instead of choosing.

## 43. The dependency stretch closed as provisional; the status consolidated (D541, D542; under D439) $0

- **Done:** the package's suite under the separated reading (285 of 287 as they are); old rows through the service (399 of 399
  in the matching-era ledgers); the state-by-event table for the unseeded path; three mismatches between decisions and code
  recorded; `docs/CURRENT_STATE.md`'s lean block rewritten from ten stacked next-task paragraphs to one statement.
- **Council (rounds 32, 33):** the seed-label stop fired and no meaning was invented; the filing finding is a hand reading; my
  "nothing reads a question being created" missed the awaited question, and "no pair names a theme" missed three theme pairs in
  my own census; the stretch is closed as provisional; my general stopping rule is refused (some contracts of unbuilt pieces
  decide whether the pieces can coexist).
- **What ten rounds on this slice taught:** (1) the stretch started from a task whose mechanism was on record two weeks earlier:
  search the earlier results first (D536); (2) the one finding with weight came from asking who else reads the record a new
  input would travel on (the edge's second reader), not from the input itself; (3) "is it reachable" must be asked of every
  writer, the waiting one included, before a row of a state table says "cannot occur"; (4) when a slice cannot move the path's
  question, say so with the evidence and ask for the closure with a rule; the council took the closure and refused the rule,
  and both were right; (5) none of it changed which system carries forward: the next step is ranked from the goal, cold.

## 44. The cold reflection: nothing ranks the systems; the next step is Alex's; no investigation is opened (D543; under D439) $0

- **Done:** my own reflection first; a fresh independent reading of the whole record; one challenge round; consensus. The status
  page now has one next task and says no investigation is open; the decision page says why the old system stays the default
  (continuity and readiness, not quality).
- **What the cold reader saw that I had not written:** the fresh week's 4 against 2 mixed Alex's product rule with system
  quality, so the path's one measurement could not have ranked the systems as it was framed; and four places on the two pages
  that would have misled him reading cold.
- **Lessons for the next path:** (1) before a comparison, remove what a product rule decides from what is being compared;
  (2) before each step, write what result would move the path's question, and stop the step if none would; (3) a path with no
  step left that can move its question is closed by saying so, with the evidence, not by finding another corner; (4) a page
  for the owner is read cold by someone who did not write it before it is called done.

## 45. The choice is made: the work goes on the new system; its answer choices in the fresh week read and traced (D544 to D546; under D439) $0

- **Why the path's own question was decided after all (D544):** the first consensus of the cold reflection left it to Alex; his
  words in D439 give it to the council. Decided reversibly: the work toward production goes on the new system, the old system
  stays the running default until the new one passes its gates, both remain; reasons, qualifications, what reverses it and a $5
  checkpoint are in the decision.
- **Done:** the 21 stored attempts at answer choices of the fresh week read by two readers apart with the Stage A form
  (`fresh-ladders/FRESH-LADDERS-RESULT.md`); each question traced into the judge; a census of all 49 amount questions of the
  stored runs of both systems (`range_census.py`).
- **Found:** one fault of Alex's lines in both readings (line 2, six of 21 attempts on three questions); ranges written with no
  figure that the first filed amount overran (two of seven questions; the old system's twin); in the census, 9 of the 12
  questions opened without a comparable amount sat on an end range against 4 of 37 with one, but on five matters, one of them in
  every run: under the trigger agreed beforehand, no general design.
- **Lessons:** (1) while Alex is away, "the next step is his" is not an outcome for what the council may decide: decide
  reversibly and write what reverses it; (2) trace a passing answer into what the judge then did with it: the lines passed two
  questions that sat on their top range all week; (3) agree the trigger before the census, then keep to it: a strong association
  on five matters is recorded, not designed for; (4) "the least consequential line" was the wrong measure once that line was the
  only thing between a sample and the gate.

## 46. The prompt audit of line 2: an undefined term (D546; under D439) $0.0022

- **Done:** the whole request of the answer-choice step read against D397, D400 and the reading form; every left-out clause of
  the seven questions tabulated by the field it sits in; the model's own account on four stored attempts
  (`fresh-ladders/PROMPT-AUDIT-LINE-2.md`).
- **Found:** "the topic's wording" is never tied to a field. A clause in the `description` was listed 6 of 6 times; a clause only
  in the `outcome` 11 of 18. The model names the same sentence each time and mostly reads the wording as the description alone.
  The decision and the reading form do not settle an outcome-only clause; both readers had marked those as failures.
- **Lessons:** (1) before counting a mark as the step's fault, check that the standard decides the case: here the readers and the
  model were guessing at the same undefined term; (2) tabulate failures by where the text sits in the request, not by what kind
  of clause it is: three "kinds" were one case; (3) four cents' worth of the model's own account settled what three rounds of
  marks could not.

## 47. The gates listed; no candidate for the declined questions; a one-week diagnostic designed in three versions (D548 to D550; under D439) $0

- **Done:** the gates the new system must pass, listed from the record with where it stands (`NEW-SYSTEM-FRAME.md`); the
  bounded question the council set, answered from the July refusal review: no general, permitted change recovers a worthwhile
  declined question (memory prices: the first step's shape of the topic, its candidates failed and its sentence changes are
  stopped; rental prices: theme coverage judged from a name, a shared product definition stopped for that boundary, at most 2
  of the 4 needed). Then the design of one more week through the new system, read for its answer choices
  (`second-week/DESIGN.md`), with an exposure census of the four later weeks (`exposure_census.py`, `exposure_bounds.py`).
- **Found:** no later week is wholly unseen (seen-before articles: 50 of 244, 22 of 272, 19 of 383, 28 of 475); in the chosen
  week 19 more articles sit on review pages of the offline source-page work and 2 carry a recurring headline an old run read;
  the first step's charge per article in July was about a sixth above the fresh week's; the unchanged runner stops the first
  step at 300 calls.
- **The council refused two versions** before agreeing to the third: a pooled rule that could not be met; outcome rules that
  named causes; a reading plan that could not cover eleven topics; a ceiling changed without a decision.
- **Lessons:** (1) before fixing a rule, run it on what is already known: mine pooled a week that already failed it; (2)
  "unseen" is a search result with stated bounds, never an assumption: say what the search can and cannot show; (3) an outcome
  rule says what a result is evidence of and what is read next, not what caused it; (4) price a run from every stored basis
  and add the reservations in flight: a guard below the plausible charge wastes the whole run; (5) a gate table is read from
  the decision that opened each gate: my draft made the newest acceptance the only gate, and D483 says it changes none.

## 48. The week's run stalled on a sleeping machine and is frozen; continued as a second part at Alex's return (D550, D551; under D439) $1.13 so far

- **Done:** the run of D550 launched after the runner's preconditions, the suite and a network check. At 120 of 272 articles
  the laptop slept with a call in flight; on waking the call made no progress. Alex asked for a pause (offline, flying): the
  processes were suspended, nothing killed. The stall was diagnosed at $0 (`second-week/RUN-STALL-2026-11-15.md`) and the
  choice at resume argued with the council.
- **Found:** the new system's first step sends each call with the run's whole remaining time as its timeout; a silent
  connection never errors, so the retry of D488 never starts. On 4,718 stored answered calls the longest took 220 seconds.
- **The council corrected:** the cut call may have been answered and charged, so its full reservation counts against the
  ceiling; the old continuation rule covered recorded network errors, so this stop is a new case with its own proof; the limits
  count across both parts; the continued result is not claimed equal to an unbroken run.
- **Lessons:** (1) a launch on a laptop needs the row "the machine sleeps" in its table: sized against money and calls, the
  run was stopped by a closed lid; (2) a retry rule covers only the failures that announce themselves: ask of every wait in a
  paid path what bounds it; (3) an earlier design that fixed one failure (D488) is a place to look for the neighbouring one:
  its table had no silent connection; (4) when the owner says pause, the first act is a reversible freeze, then the diagnosis.

## 49. The week continued, the answer choices read: not clean (D552 to D554; under D439) $3.67 on the ledgers

- **Done:** the stalled run continued as a second part after three $0 proofs (the split of a stored unbroken week replayed
  from stored answers, 20 of 20 with three mutants; the later steps at the runner's real entry; the answer choices alone, with
  a full positive control on stored answers); the transport's wait bounded at 600 seconds (D552); the topics and the answer
  choices run, the matching and the judge not (D553); 39 attempts read by Claude first, then two reader families and a third
  reader of each (`second-week/RESULT.md`).
- **Found:** 9 of 39 attempts declined on 4 of 13 topics; three zero-fault lines missed on agreed faults; 6 of 12 topics right
  by written choices against 8 needed. Over all 60 stored topics the largest reason for declining is a topic that asks two
  things (22 of 37 refusals): declined three times of three when the topic's own question asks two things, by chance when
  only its `outcome` lists several. The third readers left 41 of 48 points open, 23 on the due day.
- **The council corrected, on the way:** the merge had to refuse an unfinished second part before any send; a refusal-only
  proof does not show a step completes, so a full control was added; the lost attempts' real bill is unknown, not "a cent".
- **Lessons:** (1) a week that looks different from the last is a reason to read how the first step shaped its topics before
  reading the step under test: the same matter opened for one year got its question, opened for two years got none; (2) a
  mutant must change what the path under test reads: one that altered an unread field passed; (3) an expectation about a
  refusal must name which guard refuses: the step's own cap answered where the ledger was expected; (4) a conservative charge
  for failures is a budget line of its own on a poor network: eight lost attempts cost more on the ledger than 87 answered
  calls; (5) when two reader families split on most points put to them, the form is unclear at that point: 23 of 41 were one
  sentence of a note against a decided rule.

## 50. After the diagnostic: no candidate, a map of the first gate, an audit of the step's own two classes (D555 to D558; under D439) $0

- **Done:** a study of the topics declined for "no main part" against the earlier boundary check and this week's rulings
  (`second-week/NO-MAIN-BOUNDARY-STUDY.md`); one map of all 104 stored topics over the four readings, reconciled to each
  report (`FIRST-GATE-MAP.md`, `first_gate_map.py`); a prompt audit of the event-reference and unlisted-part classes with an
  independent second read (`PROMPT-AUDIT-TWO-CLASSES.md`); the design and the $0 proof of finishing the week as a diagnostic
  (`COMPLETION-DESIGN.md`, `completion_entry_proof.py`).
- **Found:** on agreed no-main topics the step declines every time (27 of 27) and on agreed one-main topics one attempt in
  five (9 of 48); every candidate for this class breaks a guard. Every reading carries 6 to 8 agreed marks against the
  zero-fault lines, of changing kinds. July's count is short mostly through refusals by rule and through one field: an
  event's reference, nine of whose fourteen marks are one sentence another reading held, and which the judge is never shown.
  The request never says which fields are "the topic's wording".
- **The council corrected:** the first-named rule (refused: D397, D469, D470, none of which Claude had reread); "the step
  draws the line where the readers do" (only on the no-main side); Alex's 44 topics were not "about half" right by written
  choices (31 or 25 of 44); the event marks make five topics short on two matters, not six on three; the second reader had not
  agreed that the unlisted-parts repair was not worth designing; "everything else is his rules working" (no: the accurate
  statement is that no bounded, product-relevant repair is ready).
- **Lessons:** (1) before any candidate, grep the decision index for the class in several wordings and list the stretch's
  working folders: a candidate refused two days earlier was proposed again; (2) a census by the reason the step gives counts
  attempts; a direction needs topics, and topics need matters: six short topics were two matters; (3) ask of every mark
  who reads the field downstream before calling its fault a product problem; (4) the same words marked differently in two
  readings are a finding about the form, and belong beside the result, not inside the count; (5) when the owner is reachable
  again, the decision that is his goes to him with one recommendation, and the cheap proof of the next step is done first.

## 51. The core-problem council Alex asked for: forming answerable questions, measured from an empty start against his 11-05 record (D559) $0

- **Asked** (Alex, on the week's result): "没过。然后你需要run council 到底核心问题是什么".
- **Done** (`reflection-3/`): my own reflection first; a fresh cold read; five challenge rounds to consensus; a blind review of
  the three July runs' 40 topics by two reader families (did the runs ask the same question; answerable; worth following) and
  a second blind task on where each topic's yardstick comes from; a coverage trace of the two later weeks' 20 topics, with
  their whole opening articles, against two earlier-dated libraries (the sealed library of news to 08-28; the week of
  09-22's own topics). Predictions were stored before any answer was opened (`PREDICTIONS.md`, `PREDICTIONS-coverage.md`).
- **Found:**
  - July: 18 matters by both families; the same judged question in every run that opened it on 3 (a fourth disputed),
    delivered but different on 3, a question in one run and a refusal in another on 4, refused in both on 1, opened by one run
    of three on 6.
  - Later weeks: 18 of 20 topics are standing matters, 16 of 20 were opened from an article that mentions the matter in
    passing, 2 are new events; 10 of 20 were on a matter an earlier-dated library already held a question on (both families;
    same question or same matter).
  - July's opening articles, read the same way afterwards: 35 of 40 topics on standing matters, 23 of 40 opened from a
    passing mention. A passing mention does not mark the unstable questions: the three matters with the same question in
    every run came from passing mentions; credit support and Kyber, opened from news about them, came out differently.
  - In the record: `CURRENT_STATE.md` has held since 2026-11-05 that Alex requires a library established from real material
    available before the test start, and that an empty-library diagnostic cannot represent that case. It had no decision
    number; D466 and D469 treated the start state as open and chose empty provisionally.
- **The council refused or the readers did not bear out, of my own claims:** the yardstick split as the cause (not shown; my
  second failed narrower cause in this council, after "the multi-part matter"); "what to follow is mostly sound" (against
  D477); "3 of 12 the same" as one number (missing and differing kept apart); "the loop cannot close it without Alex"; "the
  weakest act in its hardest condition"; the 2026 cloud-spending matter read off the first step's wording instead of the
  judged question.
- **Consensus (D559):** the product problem is forming answerable questions (a worthwhile matter left without one; a delivered
  question that asks a materially different or potentially unresolvable thing), no single cause proven; the clean
  measurements examined start from empty; the next product-oriented test returns to a real starting library; the empty-start
  results and the gate record stay; D558's completion run is superseded as the next step. To Alex: one confirmation and one
  small same-article comparison, after five $0 proofs. Not established: that a carried library prevents the failures.
- **Prepared, not sent** (`carried-library/DESIGN.md`): the small comparison's inputs, cases, reading and stopping rule fixed;
  six expectations on the starting library, the articles and the requests (11 of 11 rebuilt byte for byte; two mutants
  caught); the driver and launcher run under the trap (22 reads, the ledger's refusal stops it; one mutant caught).
- **Lessons:** (1) a requirement of Alex's recorded outside the numbered decisions is invisible to a search of the decision
  index: before framing a choice for him, read the status page's dated corrections and the worktrees of that stretch too,
  and give any such record a number; (2) before asking why a step fails, look at what the test feeds it: here 16 of 20
  topics came from passing mentions in general pieces, which no step-level reading had shown; (3) a narrower cause I propose
  is a prediction to register and test blind before it is said to anyone: two were wrong in one evening; (4) a blind reader
  without the source can say whether two questions differ, not whether a matter deserves a question: the source-backed
  review on record outranks it; (5) report missing questions and differing questions apart.
- **Spend:** $0 on every ledger; about $22.10 of the $40 limit (Claude's setting) as before. Reader sessions (seven Codex,
  six Claude) and the council thread are outside every ledger; their dollar cost is unknown.

## 52. The reflection council Alex asked for: the goal, the measuring, the way through (D560) $0

- **Asked** (Alex): the council reads the system design and every past attempt end to end; what is the goal; is it the
  measuring method; stuck for a long time, re-examine and break through.
- **Done** (`reflection-4/`): my own reflection first; five cold reads with no position given (the design, the history twice,
  the measuring method twice); the claims I meant to use checked in their files; two challenge rounds to consensus.
- **Found:** the record carries four goals and no single number for "ready"; the first gate has never been cleared by
  anything on record and its lines were my proposal, accepted without a chance estimate; the July end-to-end reference
  could not rank the systems at that size; every clean measurement examined ran in a condition that is not the product's;
  after the first step was accepted on 11-09, no candidate was adopted and no gate passed. Real under any stick: kept facts
  that reach no answer, questions formed differently between runs, answers and ranges sized from nothing.
- **The council refused, of my own claims:** "largely the measuring"; "what the judge is given, never wording"; the old
  system's 36 lists as a proof; the deck as an instrument; fact lookup by the answer step as a direction.
- **Consensus (D560):** the three answers; a $0 pilot of Alex's own review on the stored fresh week, beside the frozen
  reference and the gates; then D559's comparison; the six lines' role put to him after the pilot.
- **Lessons:** (1) a line I propose and Alex accepts as "recommended" is still mine to have sized first: before proposing
  any pass line, put a reference and a second draw through it and state the chance of failing; (2) when verdicts pile up as
  "missed by one", "undecided", "not separated", the stick is the first suspect, not the next candidate; (3) the premise in
  a question to Alex is itself a decision: "the real product starts from zero" was mine; (4) a cold reader given the whole
  index finds in an hour the circles the loop does not see from inside: seven recurring conclusions, five requirements not
  followed; (5) owner judgement has been absent since 11-10: an instrument he reads himself comes before another gate.
- **Built** (`pilot-deck-1/`, $0): the design with its selection rule and seed written before the draw (two rules changed
  before any card was seen, each recorded); 19 cards from the stored fresh week (12 real answers, 2 wrong answers, 2 matters
  with no question, 3 hidden repeats; 3 completeness sheets, each with a negative control both first census readers left
  empty); every card's answer choices checked against the request it was answered from (17 of 17), the repeats identical to
  their originals, the page rendered and its script parsed; the tally run on made-up marks. Known blinding limits: the
  two systems' requests differ a little in wording, and the wrong answers are of 2026-09-22 while most real ones are of
  09-28.
- **Spend:** $0 on every ledger; about $22.10 of the $40 limit as before. Five cold-read sessions and the council thread are
  outside every ledger; their dollar cost is unknown.

## 53. The small comparison on Alex's "go": the same articles from last week's library and from empty (D561, D562) $0.43

- **Run:** 11 opening articles of the week of 10-06, each read twice by the unchanged first step (from the week of 09-22's
  seven topics; from empty); 22 of 22 complete, one call each; ledger $0.427 of $1.00.
- **Found:** with the library, 4 questions opened against 16, none on a held matter; the four held questions not re-opened
  and their facts filed under them; 17 of 27 homes right and 2 wrong by both readers; the equity-commitments question not
  opened (its facts under a held question whose scope names equity investments) and a DOJ/FTC question on the Groq deal
  lost; memory prices opened only with the library. Both conditions miss questions on the company's own numbers (D382, D384,
  D505).
- **Verdict by the rule written before:** between "supports going on" and "fails" (three of the four missing matters).
- **The council corrected:** my "supports going on" (I read the positive line as a count, not the same cases); "every
  labelled case"; the 25 against 18 as distinct matters; the company-number gap attributed to both readers; "a fault" in a
  held question's shape.
- **Lessons:** (1) write a pass line in the unit it will be counted in ("the same cases", not "as often"), or it gets read
  in the author's favour; (2) a held question's scope decides where later facts go: a library passes on its shapes, good
  or bad; (3) the next unknown is not the first step but whether the questions carried are worth carrying: that is what
  Alex's deck reads.

## 54. Two weeks in the product's condition (D563, D564) $3.48

- **Run:** the stored week of 09-22 carried into 09-29..10-05 by the unchanged first step (a slice of 33 articles first, four
  conditions checked, then the rest), joined, then the unchanged later steps over the fortnight; ledger $3.476 of $6.00.
- **Found (corrected by council rounds 8 to 11):** week 2 opened 6 topics in 241 articles, none on a held question; answer
  choices written for 12 of 13 topics in all three attempts, but **gate 1 not met** (Alex's six lines, scaled: 7 or 5 of 13
  right against 11; line 4 met); of 12 last answers none unsupported by both reader families, 6 contested by at least one of
  three readers for several reasons; both families name the company's own figures as the largest missing matter; two
  statements over-read their passages (`e590`, `e279`).
- **The page:** it showed the new system's library as empty: the new writer recorded neither processing steps nor completed
  days. Fixed at the writer (`ladder_adapter.py`), every reader of the two records audited, test and mutants, the extension
  proof 19 of 19 unchanged; accepted for completed replays (a store whose first day did not finish is an untested exception).
- **The due-date class:** one matter across every stored reading (Rubin's FY2027 revenue); no new version for it.
- **My errors the council caught:** "the condition was not the reason" (other articles and draws do not isolate it); "written"
  read as "right"; a contested answer counted as one reason; the page fix first put in a frozen file (the runner's freeze
  check refused it) and first diagnosed as days only; "handed over" first written before the article's statements; a
  saved proof that predated the change cited as evidence; a pattern screen reported as a census without its limit.
- **Lessons:** (1) evidence for a code change is the output saved after the final edit, never an earlier file of the same
  name; (2) a writer's record has readers beyond the one that motivated it: list them by searching the field before calling
  a fix neutral; (3) a census of "filed nowhere" misses the facts filed under another question (D508 already showed it):
  name the whole population of a gap before counting it; (4) the next unknown is no longer whether answers can be written
  but whether they get the material that sizes them: the company's own figures (D505) are sized next, $0.

## 55. What the contested answers rest on, the judge's own account, and closing in the new system (D564 to D567) $0.035

- **Readings, $0:** the company's own figures not delivered to the fortnight's questions would move none of the 12 answers by
  either family (controls: Claude caught the positive, Codex missed it on my mis-dated packet and rated it confidence on a fixed
  one); the six contested last answers are not explained by the candidates read, but by too little evidence to choose a band and
  by question forms (both families, controls caught).
- **The judge's self-report ($0.0346, D565):** asked what sized its band, it says its own assumption did in 41 of 45 answers,
  passed and failed alike: does not separate by the frozen rule. Its sentences suggest a split ("nothing states the total" against
  "a step applied to stated amounts"); two reader families on 22 other answers: unclear by the rule (one control missed); they agree
  when no amount is the starting point and split on scaled comparables. The D520 line closed for Alex (D566).
- **Integration (D566, D567):** production's replay completed a day before its own closing on days without items (fixed; 0 of 5
  stored closings affected); the new loop now walks calendar days, closes due questions as production does and owns its sequence;
  tests, ten mutants, the unchanged extension proof, a replay to 2027-04-02.
- **My errors the council caught:** C option wording that merged D520's two cases (I accepted a revision without walking it against
  them); a control dated "2026-07" and one with no date; a control whose period did not match the brief's `direct`; counts stated
  beyond what the sentences say; a new "drop links to closed questions" rule that production does not have; a sequence collision
  my first design missed; gaps in trace numbers; a count of attempts labelled as writes; a replay checker that printed BAD without
  failing; three tests first written against the wrong data or table.
- **Lessons:** (1) when a council revises a closed question's options, walk the revision against the distinction the test exists
  to measure before freezing; (2) a control must be checked against the brief's own definitions, not only against the case; (3) a
  change that touches sequences needs the reader table of every sequence and the cases of gaps and collisions before code; (4) a
  checker that does not fail is not a check; (5) the integration gates move with deterministic $0 work, while answer quality has
  not moved in nine readings: the next step tests the measuring method itself.


## 56. The measuring stick repeated, and the product page made to read the new system (D568 to D573) $0

- **Gate 1 repeated (D568, D569):** identical packets, fresh readers and third readers of both families: every line's verdict the same,
  line 2's seven failing sends identical, 2 (or 5) of 108 Q/L/R values changed. Read as reproduced by the method, not proved right.
- **Found by asking who reads a mark:** the parts not judged (L) and an event's reference (XR) had no reader in the product, against
  D397's "shown beside the answer". Built: the bundle, the closed schema, the drawer (D570).
- **The page refused the new system's three-choice events** (6 of 12 questions; one refusal failed the whole page). Built a contract
  that reads events, theme ranges and unrecorded shapes by their names or positions, neutral, without an Idea composite (D571, D572);
  the API serves a new-system store and the page renders it (D573).
- **Council rounds 27 to 44, my errors caught:** a "sound" reference that was not independent, a fault count unlike the gate's, an
  unsupported probability, an undefined recurrence line, a one-reader fallback, comparing incomplete readings; a page proof on a store
  the page could not read; `None` hiding a broken row; no before-creation rule on direct paths; a missing-row case treated as
  production; "Still open = 0" in a composite and the planner's real ends; inferred theme scores left on the axis; the trial composite
  unguarded; a design file sent to review before my edit had written it (the edit had failed at an assertion).
- **Lessons:** (1) before measuring a gate, ask who reads each mark: a mark nothing reads cannot move the product; (2) a contract that
  refuses one item and fails the whole dataset hides a whole class until someone builds the page; (3) after an edit, check it landed
  before sending it anywhere; (4) "no table" or "no row" says nothing about provenance; say what is unknown instead of defaulting.

## 57. Serving while writing, and the page's first live read (D574) $0

- **Checked:** the API read a store while the accepted loop wrote it, at seven pauses: no partial day leaked into the completed-day
  view; completion and closing dated right.
- **Found and fixed:** a freshly opened page kept its embedded snapshot's day when the live library arrived, so a page built on one
  day and opened later showed the old day; now the startup read shows the served day (later replacements keep the verified clamp).
- **Found and recorded, not built:** before any day completes, the service serves the day in progress; a race-free guard needs one
  snapshot for check and read without holding the writer (open defect 10).
- **My errors the council caught:** a page check that counted cards (a different day with the same count would pass) and then compared
  identities that two days shared; a startup-only guard (a store empty at start reaches the state later); a per-read guard racing the
  writer; a design still describing a rejected guard as enforced; a lint error and unformatted edits found only when the UI's own checks
  ran; a library check that failed at load because it embeds the committed demo's old script (the coordinated upgrade I had written
  down myself).
- **Lessons:** (1) a page check must assert what distinguishes the cases (status on a closing day), not what they share; (2) run a
  component's own checks (lint, format, browser fixtures) before calling it proved, not only its unit tests; (3) a guard against a race
  needs the check and the read in one state, or it is not a guard.

## 58. Alex's page, Stage B's controls, and a probe of the unlisted parts (D575 to D577), $0 then about $0.15

- **Alex's page** (`DECISION-PAGE-2026-11-16.md`): six choices in order. It took four council rounds to stand. The early drafts
  misdescribed the deck, merged D520's two cases, called a pattern settled, and then disclosed a control's expected answer.
- **Stage B's control line** (`stage-b-controls/CENSUS.md`): a judge-only re-send cannot exercise it (4 of the 8 controls needed; every
  blocker sits upstream of the judge).
  - It repeated a trace made on 2026-11-12 (`CONTROL_TRACE.md`) that I had not read first: the fifth miss of the search-earlier-traces
    rule.
- **The unlisted parts** (`unlisted-parts/`): 12 failing attempts on 7 matters across four readings; 10 of the 12 are clauses only in
  the topic's outcome.
  - The request never ties "the topic's wording" to a field: four places, one of them the events sentence that asks for a cap on an
    approval to be listed. Its two examples both put the second part in the topic's question.
  - Arm A defines the wording in all four places. The probe: 18 stored requests, unchanged and changed ×3, read blind with planted
    controls.
- **My errors the council caught** before the send, rounds 59 to 64:
  - an overstated cause ("one mechanism explains every case") and settled counts that were not settled;
  - a blanket exclusion that would have dropped the cap the arm exists to keep;
  - three of the four places changed, leaving the term two meanings;
  - a regression rule that scored the disputed kinds;
  - an answer check that ignored the returned reasons;
  - a "byte for byte" claim resting on a sorted-key hash;
  - a send not bound to what was checked;
  - a scorer that accepted one third-reader family, unvalidated rulings and a missing send;
  - a breach found only after the arm;
  - a plant miss that returned "inconclusive";
  - a breach test whose charge also passed the cap, so the guard's mutant survived it.
- **Lessons:**
  1. Before a census, open the folder of the step under study (`stage_b/` held the trace).
  2. A harness's check must compare against the exact expected object (the control plus the arm), not a property of the difference.
     Also replay answers from the model's own text, not from re-serialized JSON (that made 11 good answers look refused).
  3. A test of a guard must set a case only that guard can catch.
  4. Size the pre-send work to the decision, but a scorer that decides a paid line is held to the same standard as the run.

## 59. The unlisted-parts probe, its decline side effect, and the planner (D578 to D581), $0.11

- **The probe** (`unlisted-parts/RESULT.md`): negative under the rule fixed before the send.
  - The changed written answers left no part unlisted, against 4 or 5 control topics.
  - The change declined twice where both readers said it should not.
  - Read by both families with three planted controls (6 of 6 as expected) and third readers.
- **Mechanism, as a lead:** the two accounts ($0.0012) apply line 6's decline rules to the outcome's words.
- **No sourced repair:**
  - The tie-breaker I proposed (the main part is the one both fields ask) was refused, because D397 does not hold it.
  - An independent reader found that the decisions settle the main part of a multi-part topic in 34 of 63 cases, with no general
    procedure.
- **The planner:** a three-choice event is shown to it as Yes and Still open. Two designs were refused: Ruled out is not Yes's
  complement, and a contract and model test would be needed. Parked.
- **Hold (D581):** no bounded gate-moving candidate on the record.
- **My errors the council caught:**
  - "removed" and "made" stated as causes from three sends a side;
  - an exemption rule written from two answers;
  - a paper application of a rule presented as results;
  - a count of mine treated as a measurement;
  - "Ruled out is the opposite of Yes";
  - claims about API and MCP the trace never observed;
  - a miscount of the store's questions (11 for 12);
  - a reason I transcribed wrongly (fixed to the reader's words before scoring).
- **Lessons:**
  1. A definition changes every rule that reads the defined term. Before a definition arm, list every sentence that reads the term,
     and every rule that reads its neighbours ("the topic", "the figure"), and put those in the harm controls.
  2. A rule fitted to the cases in view needs its source first; a table of my own applications is a prediction, not evidence.
  3. State what a trace ran, not what the code path implies.
  4. When three angles in a row end without a gate-moving candidate, say so and hold, rather than open a fourth (D543).

## 60. The hold lifted by Alex's instruction; D436 as the source; arm A2 (D582), $0 until the send

- **Why I resumed:** Alex's standing instruction (keep going until the challenges to production are solved) outranks a council hold.
- **What turned the line:** I went back to Alex's own rulings on the shape in question. D436 ("算一个题，第三处不改") says a second side of
  the same bet stays in one question as context, shown as not judged. It also forbade the Step 1 outcome split I first considered.
  Two blind readers then applied D436 to twelve topics, with full articles, and agreed that:
  - the two topics arm A declined are one bet;
  - the four stored refusals the first readers had split on are one bet;
  - four refusals stand.
- **The council shaped the clause in four rounds:**
  - D436's own examples only, given as examples;
  - "not by itself a reason to decline";
  - no "two bets mean no main part".
  It shaped the scorer too:
  - a kept refusal is a justified model refusal, never a code refusal;
  - a correct recovery has no failed gate-accounted mark, with G reported beside it as gate 1 reports it;
  - unjustified and code refusals still count as harm.
- **My errors caught:**
  - I said D436 was never cited (it was, in rounds 67 to 69);
  - a clause sentence that turned separate bets into no main part;
  - a scorer that counted code refusals as kept and three marks as correct;
  - a test whose mutant survived because another rule decided first;
  - a mutant that was too broad;
  - a mutant copy missing a module (an import error, not a catch).
- **Lessons:**
  1. When a line stalls on "no source", read Alex's rulings on that very shape before inventing a rule.
  2. A test of a rule must assert that rule's own output (the lost-topic list), not the final decision another rule can also reach.
  3. A mutant must change only the rule under test.

## 61. A2's result, the over-listing audit, and arm A3 built through sixteen council rounds (D583, D584), $0.15 then about $0.23

- **A2's result (D583): negative under the fixed rule.**
  - It removed the unlisted parts on the motivating topics (control 6 topics, A2 0) with no refusal, and it kept every refusal
    control.
  - Recoveries met the bar only when unresolved points count for the answer.
  - The one harm traced to the change is over-listing: 9 of 137 entries are not parts, against 1 of 71 in the control. They are an
    event's own outcomes (a delay, a termination) and the material the answer is read from.
  - Y, XR and W recur in the control.
- **Rule 2 measured against itself:** the unchanged request run twice on the same 18 topics differs by more than one on 5 marks (9
  counting against), including the marks A2 failed. The "+1" bar cannot tell an arm from variation (`control-vs-control.txt`).
- **The model's account:** it lists termination while saying "Formal termination is covered by 'ruled_out'". Nothing asks it to check
  an entry against its outcomes.
- **The council took sixteen rounds (78 to 93) to make A3 sendable.** Each round found a real gap:
  - an example that was wrong (a delay is not always Still open);
  - a test that could pass at zero;
  - a removal that could take away a second side D436 keeps;
  - the rendered Ruled out ("or any other decision against the event"), which makes a termination a finer case;
  - a reader-mark disagreement that would make A3 negative by construction, answered with a pre-registered Reading B;
  - uncertainty in both arms;
  - per-part rulings combined into per-entry and per-send marks;
  - a "diagnostic lead" too wide;
  - named ways counted by topic rather than by identity;
  - unmatched "other" named ways;
  - a Reading B that could pass by raising the control.
- **Three blind readers audited the request:**
  - the not-judged sentences;
  - the whole request, by failure class;
  - the whole request, clause by clause.
  The last called the removal unsourced. Alex's own D409 choice ("更细的区别列为'不判'") is the source, stated as an interpretation.
- **My errors caught:**
  - an edit that failed its assertion and was sent to the council unapplied (round 90; the council saw version 10);
  - a mutant list broken by escaping;
  - a send chained on a log folder that does not exist (nothing was sent);
  - a classer brief example taken from a test topic, replaced before use.
- **Lessons:**
  1. Confirm the file changed before sending a review: a failed assertion in a write script leaves the old text in place.
  2. Before writing a removal rule, read the answer as the judge is shown it. Code's appended wording changed what counts as a
     restatement.
  3. When a pre-registered reading would make a result negative by construction, say so before the send. Either add a pre-registered
     adjudication, or do not send.

## 62. A3's result, the edge tuning stopped, and a fresh comparison of A2 on the week of 10-13 (D585 to D588), $0.22 then up to $6.50

- **A3's result (D585): negative under both readings.** Checked send by send:
  - **"Named ways kept" failed on the classer:** it put the identical text "The acquisition being terminated" in two different
    kinds.
  - **"Parts kept" failed on the check itself.** It counted the intended removal of a restated delay as a loss, and it missed content
    A3 still lists under other matter labels.
  - **The real effect consistent with the sentence:** on another event, A3 lists the Ruled-out rung's own named decision ("Nvidia
    withdrawing the proposal") as not judged.
  - **Line 2 stayed fixed.** On the motivating topics: control 8 sends, A2 0, A3 0.
- **Three probes, one pattern.** Each fix of the side list's edge moved the error to a neighbouring kind (outcome words, then restated
  outcomes and sources, then named ways). The reader families split on every one of those kinds, and none is one of Alex's lines.
  The council stopped the edge tuning (D586, D391's rule) and kept A2 as an unaccepted candidate.
- **No stored topic set is held out.** All 66 stored topics and Alex's 44 were read during development, so a fresh comparison needs
  the first step to open topics from an unread week (D587).
- **The council's catch (round 99):** without `--shared-ledger`, the first step's transport adds every full reservation to a running
  total, so a $6.50 limit would stop the week after about 51 attempts. The exact launcher was then proven at $0 (`launcher_proof.py`:
  settlement, a resent loss, a stop midway).
- **Sent (D588):** the first step on the week of 10-13 (383 articles) from the 10-06 library. Then come the cases, the population
  classed blind, and the control-against-A2 send after the council's word.
- **My errors caught:**
  - I proposed a launcher command without the shared ledger;
  - I wrote the design's $5.00 ceiling and proposed $6.50 without updating the file, and the council saw the mismatch;
  - a stop test whose ceiling was below one reservation (0 articles completed), then one that never stopped;
  - a pipeline test that put an omission on a stand-in topic whose stored answer was a refusal.
- **Lessons:**
  1. Read the transport's spending code before naming a ceiling: a reservation that is never released is a limit on attempts, not
     on dollars.
  2. A stop test must be shown to stop partway, not at zero and not never.
  3. Before a send, the reviewed design and the command must say the same numbers; change the file first.

## 63. The fresh A2 comparison closes without a verdict; a fresh gate-1 reading of the frozen step; the D mark's split traced to its reasons (D589, D590), $3.48

- **The first step** on the unread week of 10-13 completed: 383 articles, $3.4485, 5 topics opened from a carried library.
- **Population (b)** was classed blind (a Codex classer, then me) and has 3 topics, under the minimum of 5. The council chose to send
  and read as registered, then close (round 102). It refused my proposal to pool the corpus's last week: that would change the
  registered sample after it missed its minimum.
- **The fresh gate-1 reading of the frozen step** (5 topics, 30 sends, $0.0282; `unlisted-parts/RESULT-FRESH-A2.md`):
  - line 2 missed (the custom-silicon topic);
  - line 3 missed (a Ruled-out rung that catches a postponement);
  - line 4 met;
  - line 5: 2 or 1 of 5 right.
- **A2:** better or equal everywhere, with no new agreed fault, but no verdict. The comparison is STOPPED: a Codex first reader
  missed plant 1, the control fails L on 1 topic, and the countings disagree. A2 stays unaccepted.
- **The two families' third readers split on 21 of 29 points.** The largest share is the due-day mark (D).
  - **Census over 14 stored readings:** 225 company figures show a code-set day that differs from the fiscal-year note's month.
    Codex first readers fail D on 133, Claude on 0.
  - **Read reason by reason:** 128 are obligation figures where Codex dates "the next annual filing" by the note's "around
    February". Alex's D414 dates it by code (60 days after year-end), and he accepted the month's lateness in his own words.
  - **The other 5** are a real error (a calendar-2027 question labelled FY2028) that the Claude family passed.
- **My errors caught:**
  - A line-6 lead read from the model's raw due day instead of the stored view that code sets.
  - A first brief sentence for D that could have overridden stated days and the obligation clause. The council refused it
    (round 103), and the cause was then read from the reasons, not inferred from the census's association.
- **Lessons:**
  1. Read the stored field the product uses before calling a send inconsistent.
  2. A census selector shows association. The cause is read from the reasons, and a fix is written to the rule the reasons cite.
  3. Before proposing a rule, search the decisions for Alex's own answer: D414 already settled the question the readers split on.
- **The D diagnostic (council rounds 103 to 106; `unlisted-parts/fresh-a2/d-diagnostic/`):**
  - The council refused it three times before any reader:
    - my first sentence could override stated days and the obligation clause;
    - the sample repeated topics across groups;
    - it had no stated-day control for an obligation.
  - Built as frozen, it held 24 distinct topics, 2 of them constructed controls, with expectations checked by a fresh checker.
  - Read D-only, fresh readers of both families hold all 12 class items under both briefs. The sentence changes nothing and is not
    adopted.
  - Recorded as a reader discrepancy (round 107). The brief is unchanged.
- **Next (D590):** a $0 census of Ruled-out rungs that catch a postponement (line 3), screen validated, answers and topics counted.
- **Lesson 4:** a reader split that a single-mark reading does not reproduce is not fixed by rewording the rule. Test the rule with
  frozen controls in both directions before writing it into the form.

## 64. Ruled-out rungs that catch a postponement: one authority miss, 37 company delays, and a boundary no decision settles (D591), $0.0007

- **The census** (`unlisted-parts/fresh-a2/postponement/`):
  - The keyword screen was too wide (104 of its 135 picks passed by both families) and missed "during" forms, so counts came from
    the stored marks.
  - In 296 frozen-step event answers, the Ruled-out first sentence is a timing statement in 37 company delays (both families pass
    R on 29) and in 1 authority case (Taiwan p3, failed by both third readers).
  - The day-passing kind D416 fixed is gone from the frozen step.
- **The model's own account of Taiwan p3:** it had no named proposal to call withdrawn, so it carried the question's deadline into
  the decision.
- **Worked cases:** five, a positive and two counterexamples among them, with each card's wording under each reading. The readers
  split by decider, with no rule behind the split.
- **Decided (rounds 108, 109):** no change. Both readings are recorded, the 38 answers are listed as candidates affected, and the
  question goes on Alex's page with a labelled lean. Next is the final-answer test's control shortfall, as a $0 design.
- **My error caught:** I first leaned to writing reading 1 into the brief. That would have turned the step's one fresh line-3
  failure into a pass by changing the form: relaxing the ruler on reader judgment. I withdrew it before the council saw it.
- **Lesson:** when the cheapest fix of a failure is a change to the measuring form, ask first whether the change would pass the very
  answer it was found on. If so, it goes to Alex as a question, not into the form.

## 65. The final-answer test's shortfall stated; the live store's operating contract agreed in nine versions (D592, D593), $0

- **The shortfall:** an unchanged re-send stays at 4 of 8 comparable controls; delivering three facts gives at most 7; the eighth
  needs an unproven two-step change. The 7-control course is not started for the line's sake.
- **The operating contract:** resumed under D439 after D575's pause, and refused eight times before it was agreed (rounds 111 to 119).
  Each round found real gaps:
  - `to_day` bounds;
  - WAL size and busy reads;
  - committed partial-day writes;
  - start-up indexing sending unfinished views outside;
  - full-text ranking statistics;
  - the copy's authority;
  - MCP's shared connection;
  - index retries;
  - store identity on replacement;
  - lock aliases, start races and the lock folder's lifecycle;
  - a path swapped around an open;
  - hard links and WAL side files.
- **Version 9 is agreed for a $0 proof build on test stores.** Live operation is not authorized, and P1 stays proposed.
- **Lessons:**
  1. A live-data contract has to name every reader, copier and date bound from the code, not from the route list.
  2. Each guarantee needs either a mechanism or an honest limit; claims of "never" fell to counterexamples four times.
  3. Narrowing a contract to a stated precondition is a legitimate answer when a binding cannot be built.

## 66. The live store's contract built and proven in slices at $0 (D594 to D603)

- **Built** (uncommitted; nothing restarted):
  - one owner for every date bound;
  - one pinned read per request, through `service.open_pinned`, which names the store on failure;
  - search over visible views only;
  - the writer's WAL store, its stops, lock and end;
  - preflight's locked copy and the snapshot route;
  - every reader opening a store by its own path.
- **Proven:** serving while the built writer runs (proof 10, 23 of 23); the page's day reaching the Idea call (2f); and the crash,
  disk and busy proofs (5a, 5b, 6a, 6b, 7′, 8′). The suite passes (346), and so do the new system's folders (192). Mutants: 24 for
  4b, 6 for slice 5, and every one caught.
- **Real findings fixed on the way:**
  - a WAL store without side files cannot be opened read-only, so the writer leaves WAL on every exit;
  - preflight read each store a second time unlocked;
  - the API and MCP opened hard-linked stores;
  - a busy result and other SQLite failures were reported alike.
- **Not understood, and stated as such:** SQLite's disk I/O error on a renamed store appears only after another test has run in the
  same process. A renamed store breaks the contract's precondition anyway.
- **My errors:**
  - tests written before reading the functions they drive (`acquire` calls `verify`, a nonexistent `view_switches.day`, the
    library's 24-card page, `rowid`);
  - one disk image shared by two variants;
  - the wrong store chosen for a stored card;
  - a loose "both sides" count that I first reported as evidence.
- **Lessons:**
  1. Read the schema and the function before the assertion. Every wasted round here was a check written blind.
  2. A combined-run-only failure is traced through the recorded traceback before any change. It was a real ordering issue in the
     writer's own reporting.
  3. When a stand-in is used (the exclusive lock for WAL busy reads), first prove that it exercises the condition, then call it a
     stand-in in the record.

## 67. Re-ranked from the goal; line 5's fresh misses traced and the route closed (D604, D605), $0

- **The re-rank (round 145):** with the live store proven, Step 4's Gate 1 is the largest blocker. The council chose a $0 trace of
  the fresh line-5 misses before any candidate. Stage B's eighth control was not chosen first.
- **The trace:** it reproduces 2 of 5 and 1 of 5. Each topic's blocking marks:
  - clean-14: XR;
  - clean-15: L and XR;
  - clean-17: R and XR;
  - clean-18: D, counted against only.
- **The source-backed reading:** in every XR failure, a rule-following answer gives the same answer choices, because a figure shows
  a reference only with a number in its unit and an event's reference reaches no rung.
- **Closed, no candidate:** the gate stays unmet, and paid work is held until new evidence or Alex's rulings.
- **My errors:**
  - I claimed the reference reaches no reader, from an older finding and a word search, without following the writer. The council
    caught it.
  - I attributed the development recount to XR alone, when it was counted without both L and XR.
- **Lesson:** "who reads this field" is answered by following the writer into what it renders (rung text), not by searching the
  readers for the field's name.

## 68. A reflection council, three closed routes and a hold (D606 to D612), $0

- **The stop hook rejected D605's wait, so the council decided Alex's page reversibly (D606).** It later reversed its own postponement
  reading after the full-rung audit (D607). Rung 1 always carries the date, and code's sentence makes a decision against the dated
  event a ruling out.
- **The fiscal note (D608):** no product effect shown. The clause is not inert, because check 5 refuses a pre-year-end day.
- **The reflection council** (a fresh Codex session, cold, after my own reflection) ranked figure delivery (D505) above my retrace of
  the gate-4 misses. The trace (D609, D610) found 5 bearing statements undelivered on 3 questions, from two mechanisms, and none was
  predicted to move an answer by a blind second reader with working controls. 49 groups are homeless by D382 and D384.
- **The comparison (D611):** the power arithmetic is unchanged, the old library ends at 08-28, and no unread week is left.
- **The hold (D612):** "The standing instruction to make progress does not make an uninformative send productive." Four reopen
  conditions.
- **My errors:**
  - an unexplained flip of my postponement lean;
  - a census script written before reading the item fields;
  - a first figure grouping that did not add up.
- **Lessons:**
  1. Before proposing a candidate, check its feasibility against the design that would decide it. A2 failed at once on the fresh-A2
     design's own definition of a development matter.
  2. A cold reader with no stake re-ranks better than my own reflection did: it found that my proposed trace repeated what the record
     already held.

## 69. The period split: built, prepared, probed, negative (D614 to D622), $0.083

- **Hypothesis.** D397 calls a topic that asks one quantity for two open years "an open defect until splitting is built". Splitting it
  into one question a year (D38) would recover two topics the frozen step declined in every send. It would not touch other topics.
- **Built** beside the frozen step: a typed decline case, yearly re-asks, the writer's `period` key with yearly view ids beginning
  with 0, and every reader of the new system's stores refusing a split store. Five council rounds caught real defects:
  - a crash proof that rolled back by hand;
  - the writer not importing the split module outside the tests;
  - a size bound that changed unsplit topics;
  - a missed reader dimension (code mapping a view to its topic by id).
- **Prepared** over council rounds 162 to 165:
  - the population first used 7 topics of the 44 (D426), and now uses 12 outside them;
  - retries were added to the spend;
  - the reading is bound to its sends by content;
  - five blind prompt-audit rounds found "seven cases" against eight, the yearly line's precedence, mixed parts, and a contradicting
    example;
  - my made-up answers had written units the schema refuses, and a schema-fit test now covers them;
  - mutants 40 of 40, four only after a test was added.
- **Result.** The counts passed:
  - T split in 6 of 6 sends with both years written;
  - no control misuse;
  - both plants were caught.

  It is **negative** by the registered rule: both families failed Q on c1/clean-12's 2027 question that switched to a share of U.S.
  GDP, where the article gives 2027 only in that measure. c1/clean-4's six yearly questions are clean.
- **Kept or not.** Not adopted. The candidate stops, and the mismatch is recorded as a case, not a rule (council round 166).
- **Lessons:**
  - a fake model skips the schema check `model.call` makes, so every made-up answer is checked against the schema;
  - a population drawn by "stored cases" must be checked against D426's 44 by code;
  - a check that can no longer change the verdict (third readers after an agreed veto) is not run.

## 70. Reflection 6: the reading checked, three levers closed, a stronger model measured, an Astra screen sent (D623 to D632), $1.00 so far

- **Hypothesis.** Gate 1's zero-fault lines might be out of reach because of the readers, not the writer. If the readers are sound, a
  lever on the writer (reasoning effort, a required field, the model) might bring its faults near zero.
- **The reading is checked** (D625). Four reference writers wrote answer choices for the 26 stored topics outside the 44. The Claude
  writer had 0 agreed faults. Planted controls and sound controls behaved, so the readers are not harsh.
- **Closed:**
  - higher reasoning effort (D626: no fewer failures);
  - a required field (closed by construction);
  - a paired gate-3 comparison (D628: underpowered at any affordable size).
- **The model** (D629, D630, $0.72):
  - sol halves the frozen step's agreed failed sends, 13 to 5 of 78;
  - but it refuses 24 times against 15, so the comparison is inconclusive by its rule;
  - clean ladders were 41 for luna and 50 for sol.
- **Sol's refusals traced** (D631, D632, $0):
  - the unjustified and disputed ones fall on topics whose outcome names several parts;
  - the description-priority sentence I proposed was refused as an unconfirmed rule (D397 makes the outcome's part the judged one);
  - an independent audit found the sources silent on five boundary topics, which go to Alex's page with both readings.
- **The Astra screen** (D632): fresh astra against fresh sol on 12 seeded topics, three draws each, under $6.70.
  - The council refused two earlier versions: the stored sol draws as control, and a "moves" line that claimed more than 78 sends show.
- **Lessons:**
  - Before a paid comparison, size the caps from the measured tokens of the stored runs, with the attempts in flight. My first cap of
    $1.00 for sol could not hold its own reserves.
  - Write a screen's verdict as a screen ("promising", or "closes this candidate under this test"), never as a gate claim.
  - When the budget pushes toward reusing a stored control, shrink the sample instead. The fresh control is the rule (AGENTS §7.3).
  - A rule the sources do not state is not written into a prompt, even when it is the readers' common reading. It goes to Alex as a
    boundary list with both readings.

## 71. Astra screened on all 26 topics, its questions reviewed against sources, one due-day clause corrected (D633 to D637), $5.59

- **Hypothesis.** The top model removes the step's faults. If it does not, the remaining ones trace to sentences of the request.
- **Astra against a fresh sol arm** (two halves of the 26 topics, $3.72):
  - failed sends 4 of 78 against 9;
  - every astra failure is a main-part decline;
  - no agreed hard-line mark on its 51 written questions.
- **The narrower main-part rule closed at $0** (D635): it turned Hugging Face's sourced wrong decline into "none". The readers' verdicts
  follow judgement about which part is the bet, not a text rule.
- **A source-backed review** (two reviewers) found 11 material defects in the 51 questions that gate 1 does not count. 4 trace to
  request line 23, which is wider than D210 and contradicts D403.
- **The one-clause correction:**
  - its probe ($1.71) fixes the completion date 4 of 4 against 0 of 4, with every control unchanged;
  - inconclusive by its rule on one request-independent listing split;
  - kept beside the frozen request.
- **Lessons:**
  - "No hard-line mark" is not "sound": read the written questions against their sources before claiming a candidate's quality.
  - A complement drawn by re-using the first draw's function silently reads the overridden size. Fix a draw's own seed and size, and
    check it against what was sent.
  - A rule masked by another rule survives its mutant. Write a test where only that rule decides.
  - Review packets must carry everything the reviewer needs (opens_as, the step's own decline rule, the rendered view), with known
    controls. One reviewer still cited a figure from outside its packet.

## 72. Astra with A2, under D612(4): two readings voided by their planted controls (D639 to D641), $1.31

- **Hypothesis.** D436's second-side sentences stop astra's main-part declines without A2's listing harm.
- **Prepared over council rounds 29 to 32:**
  - a fresh frozen arm;
  - harm in the verdict;
  - three blind audits, one of which aligned the closing check;
  - a planted listing control;
  - transport bytes compared;
  - tests 15 of 15 and 12 mutants caught.
- **Result.** A2 wrote H20 2 of 2 where the frozen arm declined (unflagged), and memory 2 of 2 (disputed). Both the gate reading and a
  separate H-only reading are VOID: Codex readers marked planted already-decided outcomes as `part`.
- **Kept or not.** Provisional, unadopted. The route stops.
- **Lessons:**
  - A planted control on a category one reader family does not apply will void every reading. Check a category's control on stored
    readings of that family before building a verdict on it.
  - A planted item must be exactly what the category names. "Never becoming final" was not identical to the question's combined
    condition.
