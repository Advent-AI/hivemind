> **Stale in part (2026-11-17, D653):** Alex has since chosen astra (D648) and its gate-1 run on the 44 was sent and read (D649); "ready for your word" below is historical. The current state and next step are in `reflection-8/LOG.md`.

# What waits on Alex: one page for one sitting (2026-11-16, D575)

**In one line:** the new system is not ready to replace the running one.

- The step that writes each question's answer choices still misses your quality gate.
- The test of its final answers has not passed either.
- Making it fit into the product has moved a long way.

Six choices are yours, and nothing below decides them for you. Until you choose, the running system stays the default (D544).

The two systems:

- **The running system** is the pipeline that serves the product today.
- **The new system** is the rebuilt pipeline (clean Steps 1 to 4). It reads news, opens questions, writes their answer choices and
  judges them.

## Your choices, in the order they were put to you

### 1. Mark the pilot cards (Deck 1), about half an hour

**What it is:** 19 cards from one stored week, with output from both systems; no card says which system wrote it.

- 12 real answers and 2 planted wrong answers.
- 2 matters no question took up.
- 3 sheets of facts that never reached an answer.
- 3 hidden repeats of earlier cards.

**What you mark:**

- On each answer card: is the question worth tracking (yes / no / cannot tell)? Is the answer supported by what is shown (yes / no /
  cannot tell)?
- On the two cards for matters no question took up: only whether the matter is worth tracking (there is no answer to mark).
- On each fact sheet, for every fact, two marks: does it bear on the question (yes / no / cannot tell)? Would it change the answer,
  only its confidence, neither, or cannot tell? The sheets include controls.
- The deck's last box gives your marks as text to paste back; the counting needs the key held outside the repository.

**Why it comes first:** since 2026-11-10 every judgement of quality has come from model readers, and their two families disagree. The
deck tests whether your own reading can check them. It ranks neither system and passes no gate.

**Where:** [`pilot-deck-1/deck-1.html`](pilot-deck-1/deck-1.html), opened in a browser.

### 2. What role should your six lines play for the answer-choice step?

**Your six lines (D400):**

1. No set of answer choices asks a different question from its topic.
2. None leaves a part of its topic unlisted.
3. None has an outcome with no matching answer, or with two.
4. No refusal without a justified reason.
5. At least 35 of the 44 topics right in at least two of three attempts, at least 28 of them with written answer choices.
6. The same favourable direction in all three attempts for every company figure, and the same due day for at least nine in ten topics.

(The later readings had fewer topics than 44; the council scaled line 5 to them as a diagnostic, not as your line.)

**The record:** the gate has been missed in all nine readings. Not every line failed each time: in the latest reading line 4 was met,
and line 6 could not be measured there (too few topics of the kinds it covers).

**New (D568, D569):** we read the same 39 answer choices again with fresh readers of the same two model families.

- Every line came out the same as before.
- The same seven attempts failed line 2.

That is repeatability under one method. It is not proof that each mark is right.

**Also new:**

- **Line 2's field had no reader.** The parts a question leaves unjudged were shown nowhere until today; they now appear beside each
  answer.
- **One reading mark checks a field still unread.** It is not one of your six lines but a mark the readers give (an event's stated plan,
  part of the reference); that field is read nowhere in the product.
- **A paper recount:** with both of those marks set aside (the unjudged-parts mark and the event-reference mark), 9 or 7 of 13 topics
  come out right, against 11 needed. The recount was not done with only the reference mark set aside.

**Options:**

- Keep all six lines, read with every mark, as the gate.
- Decide separately what role each disputed mark should play (the unjudged-parts mark, now shown on the page; the event-reference
  mark, read nowhere).
- Set new lines after your Deck 1 reading.

**Tried since (D577 to D580):** the step was told plainly that the topic's wording means both the description and the outcome.

- In a small test it listed more of the omitted parts.
- It also declined twice where both readers said it should not.

We have no reviewed repair. The records do not give a general rule for which part is judged when a topic's outcome names several
things (for example, whether a product's volume shipments or its first revenue is the thing tracked). Some of the strict counts
also got worse (`unlisted-parts/RESULT.md`).

**Since then (D582 to D588; you were away, so the council decided):**
- **Your rule added:** a second side of the same bet stays in the question as context (D436). With it (arm A2), the step left no
  part unlisted on the test topics, and it stopped declining wrongly.
- **What went wrong instead:** it now also lists things the answer already decides. For example, it lists "the deal is terminated"
  beside a question whose answer choices include exactly that.
- **One more fix tried (A3):** it removed some of those entries. It added a neighbouring kind. The model readers disagree among
  themselves on every one of these kinds, and none of them is one of your six lines. So we stopped adjusting this edge.
- **The test on unread news (D589, D590), the week of 10-13:** the system opened only 5 new questions, too few independent ones
  for a verdict, so the comparison closed without one. On those 5 questions:
  - the current step still leaves a part unlisted on one question (your line 2);
  - on another, it lets "Ruled out" catch a mere postponement (your line 3);
  - its refusals were all justified (your line 4).
  - A2 did no worse anywhere, and A2 is still not accepted.
- **The two model reader families disagree on the due day of company figures in annual reports.** Your rule (D414) sets that day
  in code. Read alone, both families now apply your rule, so the reader instructions were left unchanged.
- **A new question for you (D591): when a company announces that something will happen later than a question's date, is the
  question "ruled out" or "still open"?**
  - **The example:** "Will Vera Rubin start shipping by 31 December 2026?" Nvidia announces that first shipments move to 2027.
  - **The current step writes this as "ruled out"** on 37 stored answers, and the model readers mostly accept it.
  - **For a deal's closing or a government's rules moved past the date, the readers lean to "still open".** No rule of yours
    covers the difference.
  - **Option 1, "ruled out" (recommended, not your existing rule):** a deadline bet counts as lost when the one who decides
    announces a slip past the date. Cost: on the card, a delay and a cancellation look the same.
  - **Option 2, "still open":** the card shows no decision, and the question closes without the event having happened. Cost: about
    37 stored answers become failures of your line 3, and the step needs a repair.
  - **Until you choose:** nothing changes, and the 38 affected answers are listed beside every gate count
    (`unlisted-parts/fresh-a2/postponement/BOUNDARY-CASES.md`).
- **The final-answer test (D592):** it can compare only 4 questions with your reference where 8 are needed. No single repair the
  council can make reaches 8: delivering three missed facts reaches 7, and the eighth needs changes to two steps at once. A new
  reference set would be your choice.
- **Running the new system live (D593; your choice 6):** the rules a live database must follow were written and agreed after nine
  rounds of review: how readers see one consistent day, what happens on a crash or a full disk, and who may copy it. Next they are
  proven at no cost on test databases. Nothing runs live, and the one exception to the working rule "never open a live run's
  databases" is only proposed, for you.

**Later the same day (D623 to D632; the council decided):**
- **The readers are not too harsh** (D625). A careful writer wrote answers for 26 topics outside your 44, and the readers found no
  fault in any of them.
- **On those topics, the current step breaks one of your lines 1 to 4 in about 1 attempt in 6.**
- **More thinking time did not help** (D626).
- **A stronger model from the same provider** ("sol"; its published price is 20 times the current model's, and per answer it cost about 9 times more) broke a line in 5 attempts of 78, against
  the current step's 13 (D630).
  - It declines more often: 24 times against 15.
  - Most of its extra declines are on topics whose outcome names several things.
  - The readers disagree on those declines.
- **A new question for you (D631): when a topic's outcome names several things, which one is the question about?**
  - An independent check found that no rule of yours decides it. Five stored topics show it, each with two readings:
    - **Optical-switch shipments:** the full year 2027 is the question, or the whole span from late 2026 through 2027 is.
    - **Chip sales into China:** U.S. approval is the question and China's acceptance a condition, or the two governments' decisions
      are two separate things.
    - **An acquisition:** signing is the question and closing follows, or signing and closing are two separate things.
    - **Investment commitments:** the remaining balance is the question and the cash paid is context, or each is its own figure.
    - **Memory prices:** the contract-price change is the question and the makers' margins are context, or these compete. Separately:
      is "HBM/DRAM" one usable price, or must one series be chosen?
    - **A chip export licence (added later):** lifting the U.S. licence requirement is the question and resumed China revenue its
      consequence, or the two are separate things.
  - **Until you choose:** nothing changes, and the stronger model stays a candidate, not adopted
    (`reflection-6/model/rule-audit.md`).
- **The strongest model tried (D632 to D634):** "astra", whose published price is 100 times the current model's. It ran against
  "sol" on all 26 topics in two halves, three attempts each, $3.72 in all. These are measurements of today's unchanged instructions.
  - **Against your lines 1 to 4:** astra failed 4 attempts of 78 and sol failed 9. Every one of astra's 4 is a decline on a topic whose
    outcome names several things.
  - **Checked against the articles by two reviewers (D636):** 11 of astra's 51 written questions would make the judge record the wrong
    thing, and your six lines do not count them:
    - 4 date a signed deal's completion at the next annual report instead of the topic's date;
    - 3 date an event at its period end while the report that proves it comes later;
    - 3 widen "this quarter" to the year-end;
    - 1 invents a way of averaging two prices.
- **A one-sentence fix for the first of those (D636, D637):**
  - **The cause:** our instructions told the step that an obligation "already taken on" is checked at the next annual report. Your
    D210 meant that for amounts, such as how much is owed. The stronger models applied it to "will the deal close", against your D403
    rule for events: the topic's date or its period end.
  - **The fix:** narrowing the sentence to amounts. In a small test on one deal written two ways, the date followed the topic 4 times
    out of 4, against 0 of 4 before, and nothing else moved.
  - **The verdict was "no conclusion",** because the two reviewers split on one unrelated question.
  - **Its status:** kept beside the frozen instructions as a proposed fix, not adopted. You can undo it with a word.
- **Ready for your word: the gate-1 measurement on your 44 topics (D643).** It is prepared and not sent.
  - **Pick one of two configurations:** astra on today's instructions, or astra with the two sentences below.
  - **Cost and spending limit:** about $5 to $7 to run, and set the limit at about $9.
  - **How to launch:** write one small authorization file, then run one command.
  - **What is known and what is not:** in `reflection-6/gate1-candidate/README.md`.
- **One more candidate tried (D639 to D641):** astra with your D436 sentence ("another side of the same bet stays as context, and is
  not by itself a reason to decline").
  - It wrote the export-licence question (H20) both times, where the unchanged instructions declined both times. No reviewer found
    a fault in those questions.
  - On memory prices it also wrote questions, but the reviewers disagree.
  - Both readings were voided by their own checks: one reader family failed planted test cases on whether a listed item is "already
    decided by the answer choices", so that side effect is unmeasured.
  - It stays an untested-enough candidate, not adopted.
- **For you, with both readings:**
  - **An event dated at its period end whose proof arrives later** (for example, "first Vera Rubin revenue in fiscal 2027", proven by
    the 10-K in March). Should the judge decide on the day, or wait for the report? Your D403 sets the day. When to read the proof
    is the judging step's choice.
  - **The readers' instructions** still state the wide "annual report" rule for every obligation. In practice both reader families
    already preferred the topic's date.

**Until you choose:** the gate stays as written and stays unmet.

### 3. What should the next product test start from? (D559)

**The choice:**

- **Option A:** confirm that the next product-oriented test starts from a real library of questions already held, built by an earlier
  run. Tests that start from empty can stay as diagnostics.
- **Option B:** choose another starting condition.

**Evidence, with its limits (D561 to D564):**

- **Small comparison, 11 articles:** read once from a held library and once from empty. The held library opened 4 new questions where
  the empty start opened 16. It did not open a separate equity-commitments question that the empty start opened; those facts went under
  a held question, and both reader families accepted that home. By the rule written before the run, the result fell between its two
  outcomes.
- **The fortnight run, one draw:** week 2's six new questions repeated none of the held ones. This cannot show the problem is solved in
  general.

**Until you choose:** each test states its own starting condition.

### 4. Answers placed with nothing behind them (D520)

**The problem has two cases, which need not get the same answer:**

- **Case one:** nothing shown to the judge sizes the amount, yet it names a band.
- **Case two:** the estimate rests on an unsupported step the judge supplied itself (a discount, a growth rate), and that step decides
  the band. (A step the judge supplies is not wrong in itself; the case is the unsupported one.)

**Options for each case:**

- Show the band as today.
- Show it with a plain label of what it rests on.
- Show no band.

No recommendation is recorded among these.

**What was tried (D565, D566):**

- **Asking the judge:** asked after the fact which band its own evidence sized, the judge did not separate the answers readers had
  failed from those they had passed.
- **Two reader families:** they mostly agreed on the narrower mark that no amount was the answer's starting point, and split on
  whether a scaled comparable is a basis. That narrower observation came after the fact, and the check's own verdict was "unclear".

Neither a label nor a "no band" rule has been built or tested.

**Until you choose:** the band is shown, as today.

### 5. Two directions the running product invents (D571); two separate choices

**5a. Yes/No questions:** "Yes" is coloured as good news and "No" as bad. A "Yes" can be bad for the company. Change it, or keep it.

**5b. Theme ranges:** the highest range is scored +2 by inference. For a theme such as memory prices, higher may be bad. Change it,
or keep it.

**What the new system does instead:**

- Its events, and its theme ranges with no registered favourable direction, are shown in neutral colours, with no score.
- An Idea's combined score is not computed when one of these is among its drivers, and the Idea card says which one.

### 6. Running the new system live

**Where it stands now (D594 to D603):** the design was resumed under D439, agreed, built and tested on test copies at no cost. Nothing
is running live and nothing has been restarted.

**What the tests show:**

- While the new system writes a day, the website and the agent tools only ever show whole finished days.
- On a brand-new database's first day, they say "not ready yet" instead of showing a half-done day (open defect 10 is fixed).
- Only one writer can work on a database at a time.
- A copy for checking is taken safely, and a crash or a full disk loses nothing that was already finished.

**Example:** the test re-ran six months of one draw while asking the website for the library about 170 times. Every answer was a
whole finished day, never part of one.

**Three choices are yours:**

1. **How live data is read.** Today's working rule never opens a running database directly, only a copy (AGENTS §9). The product's
   own readers would need an exception (P1). This is proposed, not decided.
2. **Restarting the running service.** It picks up the new behaviour only on a restart. Example: a date after the last finished day
   would then be refused instead of answered from a half-done day.
3. **When to adopt.** Adopting the new system at all still comes after the quality gates.

**One small gap remains your choice:** if the page cannot reach the service, it quietly keeps the copy built into the page, as
specified. A "collected snapshot" note is a possible change.

## What the council decided in the meantime, reversibly (D606, D607; each reversed on your word)

- **The next product test** starts from a library built from real earlier material. Tests from empty stay as separate diagnostics.
- **Your six lines** stay the gate, with their accounting unchanged.
- **A company's formal decision that a dated event will not happen by its date** rules the event out. Example: "NVIDIA will not ship
  Vera Rubin in 2026" answers "will it ship by 2026-12-31?" as ruled out. An authority's proceeding that goes on is still waiting.
  This is the readers' majority view and my earlier lean; your ruling replaces it.
- **The two product directions (D520, D571)** stay as the running product has them.
- **Reading a live database directly (P1)** is not taken. The copy rule stays.

## What is in force meanwhile

- **The product:** the running system serves it, unchanged.
- **The council:** works under D439, deciding reversibly and recording each decision. Any paid send needs its own decision, within the
  $40 ceiling; about $26.18 is used.
- **The new system's integration, checked on stored replays and serving tests:**
  - the page shows its questions, including the parts each question does not judge, with no invented direction;
  - due questions close on their due day, as in the running system;
  - a freshly opened page shows the latest completed day.
  - Still open: the first-day defect, the live-service design and the Idea planner on a new-system database.
- **The final-answer test (D576):** it could compare only four questions with the reference, because the other questions, or the
  facts shown to the judge, did not meet its control conditions; eight were required. This says nothing either way about the judge on
  the excluded questions. Re-running the judge cannot change it.
- **Next, at no cost (D576):** a count of the answer choices that leave a part of the question unlisted (your line 2), now that the
  page shows that list; any change is brought to the council before it is tried.

## Where the evidence is

- **The record of this stretch:** decisions D559 to D575 (`docs/DECISIONS-log.md`).
- **The round log:** §§53 to 57 (`LEAN-LOG.md`).
- **The page and serving checks:** `page-contract/` (`RESULT.md`, `SERVE-RESULT.md`, `SERVING-WHILE-WRITING-RESULT.md`).
- **The repeated reading:** `gate1-stick/RESULT.md`.
- **The fortnight run:** `carried-run/RESULT.md`.
- **The earlier page:** `DECISION-PAGE-2026-11-15.md`.
