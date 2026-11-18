# Which system carries forward? A page for Alex's decision

Prepared on 2026-11-15 while Alex was away (D509), by Claude and the council (after three readings by an independent reviewer;
D515).

**Update, the same day (D544): the council has taken the decision this page was written for, as your instruction of 2026-11-13
asks of it while you are away. The work toward production goes on the new system; the old system stays what runs until the new
one passes its gates; both are kept and nothing was switched, deleted or deployed. Your word overrides this at any time.** It
is a decision about where the work goes, not a finding that the new system's answers are better: nothing below ranks the two.
The reasons: you had reopened work on the rebuild; it follows the rule on the company's financial figures you last confirmed
(D505); the fresh week gives no reason to abandon it and shows fewer trivial or duplicate questions in that one run. What stays
true against it: its step that writes answer choices has not met your lines, its judging test did not pass, it is not connected
to production storage, and it costs about five times as much to run. It is reconsidered if you change the product rule, if a
sound comparison on shared subjects favours the old system, or if the rebuild cannot meet its gates within a bound to be agreed;
a first checkpoint is $5 of further spending. The rest of this page is as written before that decision, and remains the
evidence for it.

## The decision

Two systems read the same news and produce the same kind of product: questions worth tracking, the statements that bear on them,
and an answer to each question.

- **The old system** is today's default configuration (`poc-v118`, kept unchanged for comparison). Its last full measurement was on
  the fixed test window of July; it has not passed any test of readiness on new news.
- **The new system** is the rebuild (`clean-arch/`): a new reading step, its own matching and grouping, an added step that writes
  each question's answer choices, and the same judge as the old system. Its fourth step (answer choices and judging) is still in
  progress, the step that writes answer choices has not passed its required tests (2026-11-12), and nothing of it is integrated
  with production storage (`clean-arch/README.md`).

**Which one does the work carry forward toward production?**

## The short answer

One fresh week does not pick a winner. By the rule written before the week was read, the result is "not clear" (D489), and nothing
since has changed that. The week does show what each system costs a reader, and it shows where Alex's choices of the past two days
bear on the comparison. Both are below. **The council's advice is to keep the old system as the default and keep both, and not to
choose from this evidence** (section 5).

## 1. One week, both systems

The week of 2026-09-22 to 09-28: 235 articles (232 never read by any earlier run; three had been read in earlier tests of the
reading step). Each system ran once, starting with no questions (`week/WEEK-RESULT.md`).

| At the end of the week | Old system | New system |
|---|---|---|
| Questions opened | 15 | 7 |
| of which worth holding, by two independent reviewing teams | 8 or 9 | 6 |
| trivia | 3 | 1 |
| duplicates of its own questions | 3 | 0 |
| Statements written | 673 | 569 |
| thrown away because no question took them | 278 | 0 |
| kept, with no question at the week's end | 0 | 389 |
| Links between statements and questions | 449 (126 of them to one question, fiscal 2027 revenue) | 196 |
| Of five big matters both teams named, covered by a question | 4 | 2 |
| Latest answer to each question: supported by what the judge was shown, by both teams | 10 of 15 | 6 of 7 |
| Estimated model cost of the week (stored token counts at today's listed rates, before cache discounts) | about $0.47 | about $2.31 |

- The rows count different things and cannot be added up.
- Seven answers against fifteen cannot rank the systems: one answer is 14 points for the new system, and the two teams disagreed
  on two of the old system's.
- The cost row is an estimate, not a bill: the new system's run was charged $2.52; the old system's shares a $2.17 ledger with a
  one-day trial and two stopped attempts. The new system's figure includes three passes of the step that writes answer choices, as
  it was set up for this measurement. Nearly all of its cost is the reading step.

## 2. Where Alex's choices bear on the comparison

- The new system does not open a question on the company's own revenue or margin (D382). On 2026-11-15 Alex chose that these
  figures serve as evidence for related questions, with no table and no questions of their own (D505).
- The old system's lead in the week (4 of 5 big matters against 2) is made of exactly those three: fiscal 2027 revenue, fiscal 2028
  revenue, fiscal 2028 gross margin. On the other two (supply commitments; Beijing's approval of a chip's purchases) the new system
  has both and the old system has one.
- Both sides of this are real. The old system's lead comes from questions Alex has chosen the new system should not hold, so it is
  not a point the old system wins by default. And under that choice the new system gave no separate answer on those figures in
  this week. Two matters are too few to call the rest either way, and D489's result stays "not clear".

## 3. What each system costs a reader today

**The old system**
- One of its 15 latest answers rests on a number nobody gave it: its data-center revenue answer needs fourth-quarter growth of
  about 25%, an allowance the judge made itself (both teams).
- Six of its 15 questions are trivia or duplicates (both teams). In each of the three duplicate pairs, two reader families listed
  facts that bear on one question and were shown only to the judge of the other (`duplicates/DUPLICATES-RESULT.md`). The two RTX
  answers and the two Rubin answers are "yes" and the two revenue answers each chose their own second band; whether supplying the
  missing facts would change an answer was not tested. In the RTX pair the answer without the reported shipment target is the one
  a separate reader had marked unsure. Of the three pairs, one second question was opened without ever being compared with the
  first (opened earlier the same day, it was not on the day's list; D375 decided a per-article list, not yet built); the other
  two were compared and kept apart by the comparison step.
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

## 4. What is not known

- Which system answers better. The week cannot say.
- How much either system loses in what it throws away or leaves without a question.
- Whether the new system's delivery gaps change answers.
- How either behaves on a second week: everything in section 1 is one week and one run each.

## 5. The council's advice, and a comparison that was sized and not run

**Advice for now: keep the old system as the default, keep both systems, and do not choose from this evidence.** The reasons are
continuity and readiness: the old system is what runs today, and the new one's step that writes answer choices has not passed
its tests and nothing of it is integrated with production storage. It is **not** a finding that the old system's answers are
better: the quality of the two systems' answers is not ranked by anything on this page. Since the week, ten small steps taught us about the company's financial
figures and about delivery, but did not decide which system to carry forward. The council advises against more small tests of
corners.

**Choosing by measurement was sized, and not run (D517).** A comparison whose questions, pass conditions and budget are written
down before it runs could choose by measurement. The council worked out what the one it had in mind would take; other designs
are not ruled out
(`comparison/COMPARISON-SIZING.md`): a week ends with 7 questions on the new system and 15 on the old, so at any size the money and
the unread news allow, the comparison may miss differences that matter, and its reliability cannot yet be calculated from our
stored readings. We did not run it. If Alex wants it anyway, what it needs is in that page: news neither system has been tested
on, the same number of runs for each, lines he sets as counts, and many more weeks than we have.

**If he prefers to choose by judgement**, this page is what the evidence can give him, and section 3 is what he would be choosing
between.

## 6. Two more pages, prepared after this one (2026-11-15)

- **The same week, both systems, side by side** (`side-by-side/SIDE-BY-SIDE-WEEK.md`): every question each system held at the week's
  end, its possible answers, its latest answer with its reasons, and both reviewing teams' marks; a second page holds every
  statement each answer cites. It ranks nothing. Read the two questions of a pair before comparing their answers: on most shared
  subjects the two systems ask different questions.
- **The judge on questions that ask for an amount** (`unsupported/DESIGN-NOTE.md`): the judge, which both systems share, names a band
  when nothing in the news sizes the amount, or closes the last gap with a number of its own. The note gives the counts, two
  questions traced day by day, and one choice that is Alex's (leave it; show the band with a plain label; or show no band until
  something sizes the amount). Nothing was changed.

## 7. What the council did while Alex was away, in one list (2026-11-15, D516 to D542)

Sent in this period: $0.0134 (ten judge calls). Nothing was pushed, committed or changed in either system. Every item has its own
page with its limits.

**Decided by the council while Alex was away; his to overturn**
1. Which system carries forward: the work goes on the new system; the old system stays the running default until the new one
   passes its gates (D544; the update at the top of this page). A cold reading of the whole record by a fresh reviewer found
   that nothing ranks the two systems' answers and that no affordable test on the record is likely to change that (D543); the
   choice was made on direction and on his product rule, reversibly.

**Still open, Alex's to choose** The comparison that could choose by measurement was sized and not run: at the proposed size it may miss
   differences that matter (D517; `comparison/COMPARISON-SIZING.md`).
2. What the product shows when nothing sizes an amount, or when an estimate rests on a step of the judge's own
   (`unsupported/DESIGN-NOTE.md`). The council has no recommendation among the options.
3. Whether the old system should hold judged questions on the company's own financial lines (D382 and D505 are his rule for the
   new system).

**Already decided by Alex, awaiting implementation and acceptance (not asked again)**
4. D375, each article sees the questions committed before it, the same day included. Proved at no cost as a bounded serial proof
   with labelled fake answers: the wiring works, and an interrupted article resumes cleanly (`duplicates/D375-PROOF-RESULT.md`).
   In the fresh week the same-day facts that missed a new question mostly reached it one to four days later; no case of a fact
   missing from a final request was shown to be one D375 recovers (`d375-measure/SAME-DAY-CASES-RESULT.md`). A real measurement
   needs a new version of the reading prompt's wording and a paid run; the council has not opened it.
5. D368, the matching step chooses a new question's dependencies (a link that lets one question read another's conclusion).
   The stored runs hold none. What the council's checks found, all at no cost (`dependency-selection/`, `dependency-channel/`):
   - **One real case in the fresh week.** When the data-center revenue question opened, the system had just compared it with
     the total-revenue question and recorded "part of". Total revenue's conclusion held the year's consensus (about $406 to
     $412 billion) and the next quarter's guidance ($108 billion). The data-center question never received them and its last
     answer filled the gap with a growth step of its own (section 3, first point). In a conditional check on the last day,
     with the link added, that conclusion was shown to the data-center judge through the system's real checks. That is not the
     same as showing the figures would have been delivered in a real run, or that the answer would change.
   - **The same link also moves statements.** As the code stands, a link makes the linked question "the narrower home", so
     seven statements would have lost their place under total revenue, one of them the company's outlook excluding China, which
     a total-revenue answer cites. A design that keeps the two uses of a link apart is written and checked on stored data
     (`dependency-selection/SEPARATION-DESIGN.md`): with it, a whole week replays with the link in place and nothing else
     moves. It is recorded as **provisional, not ready to build**: a list of points a builder must settle first is in its
     section 7, and no model was asked what it would do with the extra line.
   - **Where a statement belongs is not something a link can decide.** In ten cases read one by one, the reading step had put
     each statement under both questions; whichever way a link is read, half come out as your rules call for and half do not.
     That is the filing problem of PRD 10, unchanged.
   - **Four places where the design pages and the code part, or no decision says what should happen** (a link that would close
     a circle is dropped with a note instead of being refused; a branch for a closed question that nothing ever sets; a label
     on the old preset links that is defined nowhere; what to do when a later article proposes the opposite direction for a
     link that exists). These are part of why the design is not ready to build. Recorded with their evidence; nothing was
     changed.
   - **The relations an analyst wants most could not be chosen.** The Rubin shipping questions opened after the revenue
     questions they bear on, and a link is chosen only when a question opens. Adding one later is decided (D191) and unbuilt.
   - **The direction for the old preset questions (D368 item 4) was settled by Claude on Alex's delegation, not in his words,
     and is not measured.** On those stored runs the answers already agree with the frozen reference on 15, 15 and 16 of 17
     questions; neither test shape was sent (D536). The earlier trace (`missing-input/DEPENDENCY-TRACE-RESULT.md`) read every
     link in that one direction and found no case; it stands as written for that direction.

**Defects found or sized, with their evidence**
6. The judge, shared by both systems: of 438 stored readings of answers, 36 settled as unsupported or resting on too little; 31
   are one situation, an amount asked while nothing shown sizes it (`unsupported/UNSUPPORTED-CENSUS.md`). These are readings
   from several studies, many of them the same question on successive days (the 31 cover eight question paths on three
   matters): a failure pattern, not a rate of wrong answers. Three of the ten
   settled unsupported answers coincided with a figure the system held and had not delivered to that question
   (`missing-input/MISSING-INPUT-RESULT.md`).
7. The old system's duplicate questions: three pairs in the fresh week; one second question was opened without being compared
   with the first, the other two were compared and kept apart (`duplicates/DUPLICATES-RESULT.md`).
8. The old system's filing: the data-center revenue question never received the next quarter's guidance or a consensus for the
   year, which were filed under total revenue; in the trial, sixteen of 22 reference facts filed elsewhere sat under a broader
   question (PRD 10's subject).
9. The new system's delivery gap (D506, D508, D511): three confirmed pairs in the fresh week, effect on an answer not shown;
   paused. One more instance traced: a later-linking check that refused a supplier's guidance (`missing-input/FILING-TRACE-RESULT.md`).

## 8. Since the choice (D544 to D547, 2026-11-15): the first steps on the new system, all at no cost but 0.2 cents

- **Its answer choices in the fresh week were read by two readers apart and traced** (`fresh-ladders/FRESH-LADDERS-RESULT.md`):
  21 stored attempts on seven questions. No refusal, no question other than the topic's, the same due day and direction across
  attempts. One fault of your lines in both readings: a clause the question leaves out is listed in one attempt and missing in
  another (six of 21).
- **That fault was audited and recounted** (`fresh-ladders/PROMPT-AUDIT-LINE-2.md`): the instructions never say which text "the
  topic's wording" is; and in the July reading, which third readers had ruled on, the same omission of a comparison with the
  reference figure was passed. Two of the six are that case, two are disputed, two stand on one question. No change to the
  instructions is designed.
- **A second fault, which your six lines do not see:** two of the seven questions ask for an amount and opened from an article
  that states none; the step wrote ranges of its own, the first disclosed amount overran them, and the answer sat on the top
  range all week. A count over all stored runs of both systems: 12 of 49 amount questions opened this way, 9 of them sat on an
  end range; nearly all are one matter (the total of credit support), in every run of both systems. Recorded as a defect; no
  general design is opened on five matters.

## 9. Since then (D548 to D554, 2026-11-15): what the new system must pass, and one more week of news run through it

- **What it must pass, in order, as the record has it** (`NEW-SYSTEM-FRAME.md`): your lines for the step that writes a
  question's answer choices (not passed); the lines for the judge on the system's own questions (not passed); the comparison
  with the old system (still owed); use on unseen news (lines proposed, not yours); integration (not written).
- **One more week was run to see the first of these on news the step was not tuned on** (2026-10-06 to 10-12, 272 articles;
  `second-week/RESULT.md`). It is a diagnostic: it passes nothing and reverses nothing.
- **It did not come out clean.** Of the week's 13 topics, the step declined to write answer choices for 4 at least once, and
  for 2 every time: the five cloud companies' spending and total AI spending, each opened as one topic for 2026 and 2027
  together. Declining a topic that asks two things with neither marked as the main one is the rule you chose on 2026-11-10
  ("只判主要那件"), with its cost stated then. The week shows the size of that cost: the two demand questions of the week have no
  answer. The week before, where the same matter was opened for one year, got its question.
- **Three smaller faults both sets of readers agree on:** a question that drops the name of the guarantee it asks about; parts
  of a topic left out of the question and not listed; one refusal where the main figure was plain.
- **What it cost and what went wrong on the way:** $3.67 on the run's ledger against a limit of $3.95. The laptop slept during
  the run and the run could not recover by itself, because one call was allowed to wait for hours. That is fixed (a call now
  waits at most ten minutes and is sent again), and the run was continued from where it stopped after proofs that a continued
  run equals an unbroken one. About $1.1 of the $3.67 is the ledger's worst-case charge for calls lost on the aircraft's
  network; the real bill for those is lower. The two steps after the answer choices (matching the statements, judging) were
  not run for lack of room on the ledger; they can be run later from what is stored.
- **A measuring problem to know about:** the two sets of readers disagree on most of the points put to a third reader, and
  more than half of those are one thing: the day a yearly figure falls due. The program sets it 60 days after the fiscal
  year-end (your decision of 2026-11-10); a note the readers are given says "around February; use that day".
- **Where it stands:** the council is deciding what follows; nothing is changed meanwhile. Spending on paid calls while you
  were away: about $22.10 of the $40 limit Claude set itself.

## 10. The core problem, as the council you asked for sees it (D559, 2026-11-15)

- **The answer:** the system is poor at turning a matter into a question that can be answered and followed, and our tests
  have made it do that from a blank page every time.
- **A picture:** on 2026-10-06 a general "which stock to buy" piece carried one sentence on the cloud companies' spending
  plans for 2026 and 2027. Starting from a blank page, the system opened one question for both years; the next step refused
  it three times; that week had no question on cloud spending. In July the same system had formed the 2026 question cleanly
  three times out of three. A library that is kept would already hold it.
- **What the readers found:** July's same two weeks of news, read three times, gave 18 matters; only 3 came out as the same
  question each time. In the two later weeks, 18 of the 20 questions opened were about matters that had existed for months,
  16 were opened from a passing mention in a general piece, and 10 were on matters an earlier library already held a
  question on. July's 40 read the same way: 35 on matters that already existed, 23 opened from a passing mention. A passing
  mention is not what makes a question come out differently: July's three steady questions came from passing mentions.
- **What the record already said:** on 2026-11-05 you required a test to start from a library built from real material
  available before the test, and the status page has said so since. The measurements from 2026-11-10 on went back to an
  empty start: one with your approval as a test of the system opening its own questions, the others on the council's
  provisional choice while you were away. That requirement was not carried into those choices.
- **Not shown yet:** that keeping the library removes the failures. The system may still open a second, worse question beside
  the one it holds. And the first days of covering a company are a blank page in any case.
- **Asked of you:** to confirm the return to a kept library for the next test, and a go for one small test (22 reads, a
  ledger limit of $1.00, about $0.5 expected): the 11 articles from which the week of 10-06's questions were opened, each read
  twice, once with the library the system built in the week of 09-22 and once from a blank page. Its path, its inputs and its
  stopping rule are proved without any paid call ([design](carried-library/DESIGN.md)).
