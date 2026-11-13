# Clean Step 4: judging the system's own questions (design v35; D396–D421)

**Alex, 2026-11-10:** "设计新系统自己的“判断”环节". **First test, by the same decision:** independent readers check, against
the sources, whether the system's answers to its own questions are well supported.

**Status.** Version 30 (2026-11-10). Twenty reviews, each by a reviewer new to the work, found serious points in every version
sent (councils `gg`, `gl` to `hg`; `hf` was given version 22 by my mistake and repeated `he`), narrower each round. The twenty-first (`hh`) found nothing and said it could not finish the whole design in one sitting, so a
round is now four reviewers, one angle each (AGENTS §11): the request audited blind, the contract, the three tables, Stage A
(`hi` to `hl` read version 25 and `hm` to `hp` version 26). The third round had six angles (`hq` to `hv`, on version 27): the two
parts no reviewer had reached, who reads each written value and the counts stated from the practice readings, became angles of
their own. The fourth round had seven (`hw`, `hx` to `hz`, `ia` to `ic`, on version 28); its contract reviewer found no new defect in
fixtures, checks and writes. The fifth round (`id` to `ij`, on version 29) again had seven; two of its angles found no new defect or one count to correct.
Seven blind audits have read the request (`gw`, `gy`, `hi`, `hm`, `hq`, `hw`, `id`). **The rounds do not reach zero:** 15, 9,
15, 11 and 11 findings, each real and each smaller than the last round's; none since the ninth single review has changed what
the step does. Version 30 answers the fifth round; whether to go on reviewing, or to build with the open corner cases as tests,
was put to Alex, who chose a small send first (D402): the request sent once on six stored theses, the answers read by hand,
before any further round or the build. Since
the ninth review none has found a wrong ladder outside the reader marks. Alex has decided every
choice the reviews put to him: D397, D398 (§4), and on what the fourteenth held open, D399 (the construction of five states), D400
(Stage A against his lines, with no paid control) and D401 (once a review finds nothing serious, build and send Stage A, capped at
$3, without asking again).

**Version 31 (2026-11-10): the design as built (D402 to D407).** Four small sends followed version 30
(`probe-2026-11-10/READING-claude.md`). Changes to the request's sentences corrected the faults of writing and lowered the
declining of topics that have no main thing: in the last send, in the order the request is sent, the three such topics were
declined in 6 of 9 sends, against 8 of 9 for the request as first sent, and the line put to Alex was 8 of 9. By D407 the build
therefore uses the request as first sent, and the three faults of writing are refused by code and sent back once: a reference
that is not the article's words (check 6), a theme's state named with a company label (check 3), and a question or a condition
that points at the item (check 6a). The step is built (`ladder/ladder_step.py`, `ladder/model_calls.py`, their tests) and so is
Stage A (`stage_a/`: the runner, the accounting, the readers' packets, the collection of readings); Stage A has been sent.
This version also puts back the block on the three outcomes of a send, the lines and the accounting (§8), which an edit of
version 29 removed by mistake (round log §69): `stage_a/accounting.py` and its tests are that block's code.

**Version 32 (2026-11-10): after Stage A, an event is answered in three outcomes (D408 to D411).** Stage A missed every one
of the six lines as ruled, three of them whoever reads (`stage_a/result/RESULT.md`). Alex decided: the work stays at this step
and the event answers are changed first, checked at no cost and reviewed, before the same Stage A is run once more (D408); an
event has at most three outcomes, it happened, it is ruled out, or neither, the last written by code (D409, which supersedes
D399's five states); a group named and not listed is not a fault of a question (D410); an amount already reported may be a
figure's baseline when labelled as that, built after the event answers (D411, not yet built). **§5.2.1 states the event answer
in full and is its owner; where §5.2 to §5.4 and §7 still speak of `yes_no`, of five states or of check 3 in their accounts of
earlier versions, §5.2.1 is what the code does.** The first Stage A's code and request are kept with its result
(`poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked-2/code-as-read/`).

**Scope of the build.** The ladder step (§5 to §7) and Stage A. Stage B (§8) is an outline of what the dry runs established; its
forms, lines and coverage rule get their own review, and Alex's word, before any Stage B send.

**Where it stands (2026-11-10, D425, D426).** Four Stage A runs; the fourth is the step as it stands. Lines 2 and 6 are met,
line 5 on two of three readings; lines 1, 3 and 4 are missed by 1, 2 and 3 answers of 131 (`stage_a/result-4/RESULT.md`).
**Stage A has not passed.** A second look by the model at its own answer was tested and is not adopted (D425). By Alex's word
the step is not tuned further on the 44 theses and the preparation of Stage B opens on it, as an exception to "only when
Stage A meets its lines" below: the review of Stage B's forms and lines and the $0 baseline reading (§8). No paid Stage B
send without his word again (D426).

**It is not READY until a fresh reviewer finds nothing serious. Nothing is built, nothing paid was sent.**

## 1. In one page

- **What Step 4 is.** Two parts:
  1. a new **ladder step**: when a thesis opens, one call writes the question it is judged on, its answer ladder and its due day;
  2. production's **frozen judge**, unchanged, run daily over the laddered questions.
- **What the review found.** The judge is measured. The ladder is not, and it is the weak part:
  - Production's own ladder sentences give a different ladder on each send. One request, the same in three draws, put the bullish
    end at the low amount twice and at the high amount once, with the middle band at $5–10bn, $2–3bn and $1–5bn (§2.2). The code checks
    passed all three.
  - The 34 theses the three unseeded draws opened are not in a shape a ladder can take as they are: 12 to 16 ask more than one
    thing, 7 to 9 of the 18 number questions have no reference figure in their opening article, and 30 state no calendar due day (§2.1).
- **The next implementation step.** Build the ladder step alone and test it alone (Stage A, §8). The frozen judge runs over its
  ladders only when Stage A meets its lines (Stage B).
- **Example.** Draw 1 opened: "Will NVIDIA sign a financial guarantee/backstop for OpenAI's lease of a
  large data center in Ohio — and at what amount — large enough to change NVIDIA's credit risk?", period "Check date of 31 December
  2027 …". The ladder step writes the judged question "Will NVIDIA sign a guarantee or backstop for OpenAI's Ohio data-center lease by
  2027-12-31?", two rungs (Yes, No), due day 2027-12-31 (stated), and lists as not judged "the amount of the guarantee" and "whether it is large enough to
  change NVIDIA's credit risk". The judge
  then answers that question daily from the evidence linked to the thesis. A reader sees the topic, the judged question, the answer,
  and the part that is not judged.

## 2. What the stored data shows ($0)

### 2.1 The 34 opened theses, read blind

Packet: `census/packet.json` (builder `census/build_packet.py`): each thesis with the fields Step 1 wrote, its opening article's full
text and the 79 statements that article linked to it. Two blind readers of different families fill a fixed form
(`census/reader-brief.md`); `census/tally.py` counts. Counted by code on all 34: opening reason binding_obligation 7, product_node 6,
shared_quantity 13, policy_stage 8; period null 0. Every period is a sentence; 5 of the 34 contain an ISO date, which in 3 is a date to check on and in 2 only
the article's own publication day.

| question (source rule) | reader 1 (Codex family) | reader 2 (Claude family) | same answer on |
|---|---|---|---|
| asks one thing / several (D38) | 18 / 16 | 22 / 12 | 30 of 34 |
| one ladder keeps the question: yes / drops a part / no | 18 / 13 / 3 | 23 / 8 / 3 | 29 of 34; the three "no" are the same (u1 clean-5, u2 clean-10, u3 clean-10: memory and HBM) |
| ladder type: number / yes-no / several states | 18 / 11 / 5 | 18 / 13 / 3 | 30 of 34 |
| the thesis states a calendar due day | 4 | 4 | the same 4. For the other 30, reader 1 found a period or an expected publication for 21 and no basis for 9 (mostly "late January 2027"); reader 2 found one for all 30 |
| company question / world question (v74i line 22) | 19 / 15 | 17 / 17 | 32 of 34 |
| number questions with no reference figure in the article | 9 of 18 | 7 of 18 | — |
| company number questions whose favourable end is unclear | 6 of 6 | 6 of 6 | 6 of 6 |

The two readers split on how to class a derived due day (13 of 34 the same): the form's classes "a period end" and "an expected
publication" overlap for a figure published after its period, a defect of my form, so only "stated or not" is reported. The other
disagreements were not sent to a third reader: both readers' counts lead to the same two choices of §4, and no line depends on them.

Reader 1's answers agree with my own trace on the four cases traced before its reading (u1 clean-2, clean-4, clean-7; u2 clean-10).
The council's independent cold read (`gi-codex.md`) did not classify all 34. It counts at least 7 compound theses on a conservative
test, finds every period to be a sentence and not a date, and gives no count for theme or company, direction or a missing
reference. Earlier versions of this page attributed four counts to it that its file does not hold; they are withdrawn.
Step 1's own rule is "A thesis asks one quantity for one period, or one event" (`arms/c8-system.txt`): the bundling is
in `description`; `outcome` usually names one thing.

The same matter also takes different shapes between draws: Kyber is "shipping by end-2027" in draw 2 (clean-5) and "first shipments
by end of calendar 2028" in draw 3 (clean-7), so "yes" means on time in one and delayed in the other.

### 2.2 The ladders production's frozen request writes

`census/production_ladders.py` (output `production_ladders.txt`) reads every candidate ladder v74i wrote in the three same-day control
draws of 2026-11-09 (729 stored extraction answers).

| | count |
|---|---|
| candidate ladders | 36 (14 yes/no, 22 five-rung) |
| refused by `check_ladder` | 0 |
| refused by `check_bounds` | 1 |
| refused by the sealed split's `empty_rung` / `band_problem` (PRD 11, E3) | 0 / 0 |

- **One request, three ladders.** The request for the article that announced the credit-support model has the same canonical
  sha256 (`cad0dc63…`, `model.request_identity`) in draws 1, 3 and 4, built by the same frozen code. Its ladder for "What total amount
  of financing commitments and capacity backstops … at its FY2027 year-end?" came out as: bullish at the low end, Neutral $5–10bn;
  bullish at the low end, Neutral $2–3bn; bullish at the high end, Neutral $1–5bn.
- **Across the window** production wrote a ladder for that question 13 times (two wordings, from different articles). One was
  refused by the bounds check (draw 4, call 58). Of the 12 accepted: bullish at the low end 10 times and at the high end
  twice; six different Neutral bands.
- In production most of these candidates folded into a seeded question with a reviewed ladder. On the clean path the first write is
  the ladder for the life of the thesis (D38).
- What this does not show: that the ladder is the largest risk of Step 4, or which sentence causes the spread.

### 2.3 The frozen judge's refusals

Counted in the stored archives: the three seeded clean draws of Stage 2 retried 10, 16 and 18 judgements of 239, 269 and 251 calls.
38 of the 51 stated reasons are "v… is not a dependency of v…": a theme shown under D191 written into `cites_views` (PRD 11, E4).
The three unseeded draws retried 0 of 159; the China-share question, where the class lives, was never judged there. Two refusals of one
judgement stop the day (`judging.py` lines 322–328).

### 2.4 Facts the mapping rests on (each read in the code or the data)

- A thesis's library state holds `description`, `entity`, `id`, `outcome`, `period`. `opens_as` and `settled_by` are only in the Step 1
  answer of the opening article (`trace.result`, keyed by a local id).
- The judge finds theme ids with `^- (v\d+) \(` and evidence ids with `^- (e\d+) \[` (`judging.py` lines 182–191): a view id must be
  `v<N>` and an evidence id `e<N>`.
- The judge is shown each rung's label and condition, never `lo` and `hi` (`judging.py` line 124).
- The judge shows the first 400 characters of a quote (`judging.py` line 130); 138, 150 and 140 of the 548, 589 and 536 evidence records of
  the three unseeded draws are longer.
- The theme block and the re-queue rule key on the view's `object_kind` (`judging.py` lines 79, 83, 270), which production takes from
  the research list (`poc/universe.json`, twelve themes). A candidate whose object is not on the list is not opened, and a theme's
  name goes to the review pool (`matching.py` lines 332–338).
- In the unseeded draws 144, 119 and 86 links went to theses that matched no ruler question and were dropped unjudged: the system's own
  questions have never met a judge.

## 3. Decisions this design follows (searched by name: ladder, rung, due, theme, dependency, obligation)

| decision | what it fixes for Step 4 |
|---|---|
| D38 | A view is one question, a fixed ladder and a due date, never rewritten. "A view looks at one thing: a question that needs a number and an event is two views … a question whose parts can move in opposite directions is two views." Company views run strongly bullish to strongly bearish; theme views are named by outcome. Five rungs; an event that happens or not has two. A number's due date is the day it is published. |
| D397 | On the clean path a thesis gets at most one judged question, the part its `outcome` names; every other part is shown as not judged; a thesis with no main part gets none. A recorded departure from D38 for a topic with two real bets. |
| D248 | Two questions stay apart only when their answers can move apart and an analyst would bet on each separately; a small matter opens no question. |
| D46, D248 boundary 4; `extraction.sift` | At most this year's and next year's number questions open; a quarterly figure is evidence, not a view. |
| D185 (`check_admission`) | A binding-obligation question is due within 18 months of the item. |
| D186 with D368 item 1; D398 | "Rungs of an asset thesis state the business outcome (above, near or below guidance), and each thesis registers which end is favourable." D368 puts both halves in the next extraction version. D398: the clean ladder step builds both now, with D260's list as the reference. |
| D191, D195 | A theme question is context for every company question; a changed theme queues every open company question; a theme opens only when it is on the research list. |
| D51, D368 item 2 | Dependencies are chosen at matching; the default path gives an article-opened thesis none (to be built). This design stores none. |
| D198, D63, D260 | What a judgement reads; one round a day; a forecast against a reference ("consensus, the company's guidance, the stated plan or deadline"), with the reference and the implied outcome stated. |
| D354, D359 | The judge (judging-v7 on gpt-6-luna, medium effort) and its checks are frozen; no other version is built. |
| D356 | Closing at the due day is pull mode's; a due day falls on or after the day the result is published. |
| D370; Alex 2026-11-08 | No preset questions; figures are evidence. Step 4 judges only what Step 1 opens. |
| D378; PRD 11, E3 and E4 | The sealed split ran a separate call that wrote questions with ladders: a ladder present in 21 of 44 on one request, inverted ladders, a band that missed its bounds, a rung holding no value. "Checks, not wording, are the part to port." E4 records the judge's refusal class with a judging version only Alex opens. |
| D391 | c8 is frozen; a change is a new version Alex opens; every change names its effect on a reader or the judgement first. |
| D396 | This design; readers check the answers against the sources; build and paid sends on Alex's word. |

**Expected effect on a reader (D391).** Today 0 of 34 of the system's own questions has an answer. After this step each has a
judged question a reader can check against the sources, or a stated reason why it has none.

## 4. What Alex decided, and what this design takes from production

**D397. A topic that asks more than one thing gets one judged question** (Alex, 2026-11-10: "只判主要那件"; 12 to 16 of 34 by the
two readers).
- The judged question is the part the thesis's `outcome` names. The topic and every part left out are shown beside the answer as not
  judged.
- A thesis with no main part gets no judged question, with the reason recorded (3 of the 34 by both readers: the memory topics).
- Known costs, stated to him: the parts left out have no answer (a part dropped in 8 to 13 topics); for a topic with two real bets
  this departs from D38, an open defect; the part `outcome` names is not proven to be the bet an analyst would pick. Stage A's
  readers mark each left-out part as a bet an analyst would hold or not, which sizes what splitting would add.

**D398. The ladder step carries D186, both halves** (Alex, 2026-11-10: "两半都带上").
- The model states the reference the article gives and, for a company's figure, the favourable end with one sentence why. Code
  checks that a reference value sits in the middle range, orders and labels the rungs, and writes each range's text.
- The reference is D260's list: a consensus, the company's guidance, the stated plan or deadline. That is wider than D186's word
  "guidance"; the question put to him said "市场预期或公司指引".
- Known costs, stated to him: 7 to 9 of 18 number questions have no such figure in their opening article, so their ranges are the
  model's own estimate, shown as "no reference", and can differ from one write to the next as production's do; the two readers found
  the favourable end unclear for 6 of 6 company number questions, so a registered direction can still be wrong. Stage A measures
  whether it is stable and defensible.

**D399. The request teaches how to build an event's five states** (Alex, 2026-11-10: "把这个做法写进提示词"). Outcomes that exclude
one another, one or two of them divided by a property that holds or does not, with a merger review as the example. Three
hand-written five-state ladders had failed without it; three built by it passed two readers.

**D400. Stage A is read against Alex's lines, with no paid control arm** (Alex, 2026-11-10: "同意：不设对照，线按提议"). An exception
to AGENTS §7.3 for this first measurement. Stage A does not show the step is better than production, and every report says so.

**D401. After a review that finds nothing serious, the ladder step is built and Stage A sent without asking again,** capped at $3
(Alex, 2026-11-10: "可以，评审放行后直接做"). A line missed stops and goes to him. Stage B needs his word again.

**Behaviour this design takes from production; each is his to change.** All four were reported to him on 2026-11-10:
- **A world question whose theme is not on the research list is not judged**, and the theme's name is reported as a suggestion. This
  is what production's code does for any candidate (`matching.py` lines 332–338). D191 point 3 decides it only for a macro-only item
  ("an unlisted theme waits for a company item"); for a company item no decision says it. Its cost is counted in Stage A.
- **No dependencies are stored** (production's default path today; D368 item 2 is its own slice).
- **A number question whose opening article states no expectation still gets a ladder**, as production writes one today (D398
  records it).
- **A thesis whose due day cannot be set gets no ladder** and is counted (D38: a view has a due date). It is the request's
  refusal case "nothing in the topic can be checked on a date": the model returns `no_ladder` with that reason, and a reader
  judges it by mark N like any other refusal. None of the 34 has a null period.

**A restriction narrower than production's sentence, decided by Alex (D403, 2026-11-10: "保持更严").** An
event's due day is the date the thesis or the article gives, or the last day of the period the thesis names (the fiscal year-end
for a pending regulatory decision with no date); the model does not choose another day. v74i line 26 says only "name the date at
which its outcome is assessed". The reason is one owner: Step 1 writes a thesis's period, and this step turns it into a day. Three
blind audits mark the sentence narrower; it is narrower by his decision. An event that gives no date and whose thesis names
no period is declined as "nothing in the topic can be checked on a date".

## 5. The ladder step

### 5.1 When it runs and what it reads

Once per thesis Step 1 newly opened, after Step 3 saved that article and before that day's judging.

| input | source |
|---|---|
| `thesis.id` | the library state after the opening article (`clean-<N>`) |
| `thesis.description`, `outcome`, `period`, `opens_as`, `settled_by` | the opening article's Step 1 answer (`trace.result.new_theses`), joined to the state by description (the join `census/build_packet.py` makes: exactly one match, or the run refuses) |
| `item.publication_date`, `publisher`, `title`, `text` | the opening article's Step 1 request (`source_item`) |
| `company`, `fiscal_year_note` | the run's entity; `universe.fiscal_note(entity, publication_date, english=True)` |
| `themes` | `universe.theme_list()`, as `[{id, name}]` |

Nothing later than the opening article is read: no evidence linked afterwards, no other thesis, no judgement.

### 5.2 The request

- **System text:** `ladder/candidate-system.txt`, the request as first sent (D407; 7,123 characters, the closing check 662). Its
  examples are a drug approval, an air carrier and capital spending; none names the covered company, its products or a test article.
- **User text:** one JSON object, serialized with `json.dumps(payload, ensure_ascii=False)` as the Step 1 runner does
  (`runner.py` line 264), with exactly these keys in this order:
  `{"company": "NVDA", "fiscal_year_note": "…", "themes": [{"id": "…", "name": "…"}, …], "thesis": {"id": "clean-3", "description":
  "…", "outcome": "…", "period": "…", "opens_as": "…", "settled_by": "…"}, "item": {"publication_date": "2026-07-02", "publisher":
  "…", "title": "…", "text": "…"}}`,
  then a blank line, then the closing check, `ladder/candidate-closing.txt`. The check reads the answer back and stands at the
  very end of the request, after the payload (AGENTS §6), where production puts its own closing sentences (`extraction.py`
  line 403).
- **Schema (strict):** `ladder/candidate-schema.json` (draft). Either `no_ladder` is a reason and `ladder` is null, or `ladder` is
  complete and `no_ladder` is null. Inside `ladder` exactly one of two answer shapes is filled: `event` (the condition under which the event has happened and,
  or null, the condition under which it is ruled out; §5.2.1, D409; before version 32, `yes_no` and five `states`); `figure` (a
  unit, exactly five ranges, the favourable end). The schema cannot express "exactly one"; check 1 does.
  The schema uses only keywords production's requests already send to this provider (`type`, `anyOf`, `required`,
  `additionalProperties`, `items`, `enum`, `pattern`) and `description`. It carries no list length: no stored request has sent
  `maxItems` to this provider, and production's validator (`model.check_schema`) enforces a list's minimum and not its maximum,
  so a six-range and a six-state answer both passed it on the fixtures. Check 1 counts the five.
- **Model:** gpt-6-luna at medium effort with an output cap of 16,000 tokens, the judge's setting (`cfg.rejudging`), with the
  strict schema; one configuration. Priced from tokens at
  `hivemind.model.PRICES` before the send.

Each rule sentence of the request, with its source (the whole-request audit, with a blind second reader, comes before any send):

| sentence of the request | source |
|---|---|
| one figure for a named period or one event; a question, not an assertion; a figure or event must determine the outcome on the due date | v74i lines 20–21 |
| the question stands on its own for a later judge, who has only the question, the ladder and new evidence (D38: the view is written once and judged later, from evidence; the probe, D404) | D38; D404 |
| a figure's question names the period it covers or the day it is measured at, and what settles it | D38: a view looks at one number, "which year, whether a period amount or a point-in-time value, and the source it is answered from" |
| judge the one the topic's `outcome` names; list every other part of the wording, a second figure or event, a condition or a comparison | D397; D38 "a view looks at one thing". `settled_by` is passed as context and decides nothing: when it and `outcome` point to different things, `outcome` decides |
| `no_ladder`: no main figure or event (none, or several with none the main one); nothing checkable on a date (for an event: no date given and no period named, unless it is a pending regulatory decision, due at the fiscal year-end) | D397; D38 (a view has a ladder and a due date); D403; v74i line 16 |
| `no_ladder`: a company's figure for a quarter or a half-year; a figure for a year beyond next year, unless the topic's `opens_as` is binding_obligation | v74i lines 16–17; D46; `extraction.sift` lines 625–632, which make the same two exceptions |
| `no_ladder`: a figure for a year that has already ended on the item's day | D38: "a year whose period has ended gets no new view". D38 counts the year from the latest day processed and v74i line 26 from the item's day; on this path they are one day, since the replay refuses a trace that is not in day order (`adapter.py` line 305) |
| a figure beyond next year is not rewritten as an event; a numeric completion target may define an event's state | v74i line 16 |
| the company or a listed theme; a question of another company or of an unlisted matter is returned as `no_ladder` with its name | v74i line 22; production's [Subjects] sentence asks for the matter's name and its matching then does not open it (`matching.py` lines 332–338); here the model is told the result, so the request asks for nothing a check refuses |
| concrete conditions now; no future target; no overlap or gap; exactly one holds | v74i lines 24–25; D38 |
| a yes/no event has two rungs, anything else five; a company's states carry the five labels strongly bullish to strongly bearish, and the Neutral state's condition says what it is neutral against, the expected outcome when the item states one and otherwise the baseline the model compares with; a theme's are named by outcome | v74i line 25 ("State the neutral comparison in its condition"), carried as it stands; D38 |
| how to build five states: outcomes that exclude one another, one or two of them divided by a property that holds or does not; the merger example | D399. It is the construction for D38's "rungs do not overlap, cover every outcome", added because the second audit found no worked event ladder and three hand-written ones had failed. It also gives an event with three natural outcomes its five states |
| a figure: its unit from production's list (`extraction.UNITS`), with "other" where production writes "n/a"; one year, written `FY2027` or `2026`; five ranges; inclusive `lo`, exclusive `hi`, amounts in full, open ends | v74i lines 26, 34 and 35; production's closing sentence on `year` |
| the reference is a consensus, guidance, or the stated plan or deadline, for a figure or an event; its words are copied from the item exactly, as one unbroken passage (D398: "the reference the opening article gives"; D405) | D260; judging-v7. Only a figure's reference value is checked against ranges (D398); an event's is recorded and read by readers. The value is a number the item states and never one it does not; an expectation in words alone is kept as words, with no value (D398: code "checks that a stated reference value lies in the middle range") |
| when the reference has a value, a figure's middle range holds it, the ranges on either side the outcomes above and below it; the favourable end with a reason | D186, D398 |
| no stated expectation, or one stated in words alone: the ranges are the model's estimate | D398; production's behaviour |
| the due day falls after the item's day, on or after the day the settling material is published | `extraction.sift`; D356 |
| a figure's due day is its publication date, after the end of the period it covers; fiscal and calendar years | v74i line 26; D38; D356 |
| an event's due day is the date its outcome is assessed: stated, or a period end, which is the last day of the period the topic names or, for a pending regulatory decision with no date, the company's current fiscal year-end | v74i lines 16 and 26. Narrower than line 26 on purpose: Step 1 writes a thesis's period (c8 §3), and this step turns that period into a day and does not choose another (one owner, AGENTS §3). Decided by Alex (D403). A topic and item that give no date and no period fall under "nothing can be checked on a date" |
| a topic whose `opens_as` is binding_obligation is due within 548 days (18 months): an obligation taken on at its next annual filing, one not yet signed on its check date | v74i line 13; D185; `check_admission`, which tests the same field. The request and the check share that one scope: the `opens_as` Step 1 wrote, which the call is shown |
| the answer is written in English | v74i line 23; D163 |
| the closing check: one thing and every other part listed; a figure's ranges meet end to end; an event's states taken two at a time, then an outcome that fits none; the reference's value; the bounds; the due day | AGENTS §6; each clause repeats a rule stated in the system text; it is the last text of the request, after the payload |

An event's `year` is not asked of the model: code writes the year of the due day, as the seeds do (v8: due 2027-01-31, year 2027)
and as the adapter already does for the Ohio question.

`ladder/examples.json` is not part of the request and is never sent to the model. It holds **check fixtures**: answers that pass
the schema and checks 1 to 8, with a projection of what the step writes for them (the view's fields and each rung's label,
condition and bounds; the complete rows are §5.4's), on stored theses on purpose. They test the code, which
needs valid shapes and not sound content; none is offered as a sound ladder, and where one has a note it records what readers found in it. The request's own examples are the three in the system text.

**The blind whole-request audit** (AGENTS §6) was run on version 13's request by a second reader who had not seen the source
table (`council/gw-audit-handoff.md` → `gw-audit-codex.md`). What it found and what changed:

| finding | change |
|---|---|
| `not_judged` asked for other figures or events; D397 says every other part of the wording | the request and the schema now say every other part: a second figure or event, a condition, a comparison |
| "no main part" was written as one special case | now "the topic has no main figure or event" |
| D38's "which year, a period amount or a point-in-time value, and the source" was not carried | the question names the period or the day measured at, and what settles it |
| the closing check asked that a reference value fall in the middle range; the text above said only "near" | the text above now says the middle range holds the reference's value |
| theme state names were not required to differ, while check 3 refuses equal names | the request says each name is different |
| the yes/no examples in `examples.json` said "confirmed"; an event not confirmed is not an event that did not happen (judging-v7) | the examples state the event and its complement |
| the two five-state examples had gaps or overlaps | they are now marked as showing the shape only; see §9 |
| an event with three or four natural outcomes has no rule or example | unchanged, as in production; a known gap (§9), measured in Stage A |
| the request does not tell the model that another company or an unlisted theme gets no view | deliberate (check 2) |
| six examples name the covered company | they are not sent to the model |

**The second blind audit** (`council/gy-audit-handoff.md` → `gy-audit-codex.md`), on the request and schema as changed, without the
worked examples: every sentence and every schema description consistent with its source except these, each now answered:

| finding | change |
|---|---|
| v74i line 16's rule against rewriting a distant annual figure as an event was not carried | carried |
| v74i line 25's neutral comparison was not asked for a company's event states | the Neutral state's condition says what it is neutral against (v74i's sentence, carried as it stands) |
| no worked event ladder teaches a complete, non-overlapping set of states | the construction and the merger example (above) |
| an event's due-day choices are narrower than v74i line 26 | kept, with its reason (above) |
| the closing check sampled three outcomes | it now checks ranges end to end and states two at a time |
| a figure's due day after its period ends was a reader's mark and not in the request | in the request |
| the request allowed another company, an unlisted theme and any size of bound, which code ended or refused | the request now returns `no_ladder` for the first two and names the one set of numbers the check accepts (check 4) |

**Third blind audit (`hi-audit-codex.md`), on version 25's request.** It found no sentence or example fitted to the covered
company, a closing check that repeats only rules above it, and a merger example whose five states neither overlap nor leave a gap.
Its findings and what changed:

| finding | change |
|---|---|
| "a year that has already ended on the item's day" is wider than D38's "latest day processed" | the two are one day on this path; recorded in the source table and in check 5 |
| a company's Neutral state as "the expected outcome, otherwise the middle of the five" has no source | removed; v74i's own sentence is carried |
| the size and digit limits on a number come from the check, not from the standard | recorded as a format rule, not a rule of what to keep |
| a figure's reference had to carry a value, so an expectation given in words alone had to be dropped or given an invented number | first answered by excluding such words, which the fourth audit found narrower than D260 and D398; now the words are kept with a null value (below) |
| an event's due day is narrower than v74i line 26 | kept with its reason; reported to Alex, who has since decided it (D403, §4) |
| v74i line 23, "Write generated descriptions in English", was not carried | carried |

**Fourth blind audit (`hm-audit-codex.md`), on version 26's request.** Every sentence consistent with its source but three, and
no request that a check must refuse. The three: the number limits are the check's, a format and not a rule of what to keep
(agreed, and recorded so); the event due day, narrower and reported to Alex (§4); and one finding to act on:

| finding | change |
|---|---|
| a figure's reference limited to a stated number drops an expectation the article gives in words; D260 and D398 decide no such exclusion | the reference keeps the item's words; its value is the number the item states, or null when it states none. Code checks the middle range only when a value is given, which is D398's own wording ("a stated reference value"), and writes the reference into the middle rung only then |

**Fifth blind audit (`hq-audit-codex.md`), on version 27's request.** Every sentence consistent with its source but the number
limits (the check's format, recorded so) and the event due day (reported to Alex, §4). Two findings to act on:

| finding | change |
|---|---|
| the request asks for the number the item states and also for a number within the limits; an item that states a number outside them leaves no answer the check accepts | the request says to leave the value null in that case; the words are kept |
| the closing check stood at the end of the system text, and the payload came after it, so it was not the end of the request | moved to the end of the user text, after the payload, as production does |

**Sixth blind audit (`hw-audit-codex.md`), on version 28's request.** Every sentence consistent with its source but the number
limits and the event due day, as before; the closing check is now the last text. Two findings to act on:

| finding | change |
|---|---|
| the check refused some spellings of numbers the request allows (`1e+0000`; thirty-one trailing zeros) | the check decides by the number's value, whatever its spelling (check 4) |
| the merger example did not say whether "the filing withdrawn" is the state on the due day or something that once happened | the example's two undecided states now read "no decision yet, the filing still pending" and "no decision, the filing withdrawn and none pending" |

**Seventh blind audit (`id-audit-codex.md`), on version 29's request.** Three findings to act on:

| finding | change |
|---|---|
| the merger example left out a review that is closed or lapses, and "blocked" could be read as something that once happened | the five states are read as the position on the due day: cleared with no conditions; cleared with conditions; blocked; not decided, a filing still pending; not decided, no filing pending (withdrawn, lapsed or closed) |
| a figure with no reference figure states no neutral comparison (v74i line 25) | code writes "(no reference figure when the question opened)" into its middle rung (check 7) |
| "fifteen significant digits" could be read with or without trailing zeros; five audits had marked the number limits as having no source in the standard | the limits are retired (check 4) |

**Eighth blind audit (`ik-audit-codex.md`), on version 30's request, the last read before the six-request send of D402.** It asked
that the send wait for two points:

| finding | change |
|---|---|
| "no main figure or event" does not plainly cover several things with none the main one (D397), and "nothing can be checked on a date" does not plainly cover an event with no date and no period (D403) | both said plainly, in the request, the schema's description and the form. My first wording declined every event with no date and no period; the auditor's challenge round (`il-codex.md`) caught that it dropped the pending regulatory decision, which is due at the fiscal year-end, and its own words are now used |
| the request asks for "a number" and the check refuses one beyond a float's range or of more than 4,300 digits; check 7's test list still named numbers the new rule accepts | the test list is corrected; the difference is recorded in check 4 and kept, with its reason. The six-request send applies no check of the step, so it does not bear on it |

**The six-request probe (D402) and what it changed (D404, D405).** The request of version 30, sent once on six stored theses:
`probe-2026-11-10/` holds the requests as sent, the answers, the model's own accounts and the reading (`READING-claude.md`, with a
cold reader's). Three classes, each located by the model's own account, each answered by one change:

| what the answers showed | the model's account | change |
|---|---|---|
| two of three quoted references were not the article's words (one reordered, one taken from the topic) | "I read 'in the item's own words' as allowing a faithful paraphrase" | "Its words are copied from the item exactly, as one unbroken passage: not reworded, not reordered, and not taken from the topic"; check 6 stays strict (D405) |
| a question that says "this item" | "I implicitly wrote for a reader with the item" | the request says who reads the question later and that it must stand on its own |
| a theme's five states labelled Strongly bearish to Strongly bullish | "None. I used the company-state labels in error" (the rule sat at the end of a long sentence) | the theme's rule is said first and on its own; check 3 refuses a theme state named with a company label |

The closing check then read these three back. System text 7,123 to 7,517 characters, closing 662 to 855: growth, for three
classes a send showed and no review had. **These changes to the request were not kept (D406, D407).** The sends that followed
showed them lowering the declining of topics with no main thing, and a required field naming the main thing lowering it further
(`probe-2026-11-10/READING-claude.md`, with my error of re-sending requests taken from the archive, whose keys are sorted). The
build uses the request as first sent; the three classes are held by code, which refuses the answer and sends it back once
(checks 3, 6 and 6a). Not changed, and left to the readers' marks: a present amount recorded as an
expectation (XR), a yes/no wording over five states (Q, R), `stated` against `period_end` for a day that is both.

The audit is repeated after any change to the request or the schema, before a send.

v74i's lines 32–34 (measure, scope, period_start, basis) are not used: the clean path has no typed key (D382).

### 5.2.1 An event in three outcomes (version 32; D409, which supersedes D399)

**The decision.** Alex, 2026-11-10, on "事件类的题…答案要分几种结局？": "分三种": "发生了 / 明确落空（被否决、被放弃）/ 到期还没结果。第三种由程序写成“前两种都不是”，所以
不会有遗漏。保住了“否决”和“还在等”的区别；更细的区别（如“附条件批准”）列为“不判”。"

**Why.** Stage A (`stage_a/result/RESULT.md`): five states written by the model for a company's event were faulted by both
reader families in 10 of 17 ladders, yes/no in 2 of 24. Of the seven gaps or overlaps both families found, six sit in the
division of an event beyond three outcomes (pending against not pending, broad against narrow, a licence against another
restriction, refused against withdrawn, a remedy without a finding) and one in a Yes that needs a confirmation its No does
not. The council's reading of the five theses the run wrote both ways (`council/iv-codex.md`): yes/no is the cleaner send in
each, and loses "ruled out" against "still open" in two.

**What the model writes, and what code writes.**

| part | who | what |
|---|---|---|
| `event.happened` | the model | the condition under which the event the question asks about has happened by the due day |
| `event.ruled_out` | the model | the condition under which the event as a whole stands ruled out on the due day although it has not happened: decided against, or formally abandoned or withdrawn, after the item's day; null only when nothing can rule it out before the due day |
| rung 1, `Yes` | code | the first condition as given |
| rung 2, `Ruled out` (only when a condition is given) | code | that condition, then "This rung holds when that, or any other decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after <the article's day> and stands on <due day>, and only when rung 1 does not." The scope governs the model's own sentence too (changed after the second Stage A, below) |
| the last rung: `Still open` (three rungs) or `No` (two) | code | "Neither rung 1 nor rung 2 holds on <due day>." or "Rung 1 does not hold on <due day>." |

So, whatever the two conditions say, the rungs are H; not H and R; not H and not R: exactly one holds for every outcome, by
construction. This is identity, which code owns (AGENTS §2): it decides nothing about which event matters or what rules it
out. What stays the model's, and the readers' mark R: that `happened` is the event the question asks about, that `ruled_out`
is that event decided against or abandoned and not its merely being awaited, and that each can be checked on the due day. A
difference inside an outcome that the thesis's wording names goes to `not_judged` (D397), as any part left out does; a
difference the wording does not name is not listed.

**What two rounds of the council's read settled before any send (`council/iw-codex.md`, `iy-codex.md`).**
- *A rejection the model did not name must not land in "still open".* If the `Ruled out` rung held only the way the model
  names, every other way of being decided against would fall in the last rung beside the waiting, and the difference D409
  keeps would be lost. Asking the model for "every way" was tried and withdrawn: listing ways is the mechanism that left the
  gaps in five states, and a reader can always name one more. So code closes the rung: after the model's condition it adds
  that the rung holds when that, or any other decision against the event as a whole, or a formal abandonment or withdrawal of
  it as a whole, stands on the due day: the request's own words for D409's "明确落空（被否决、被放弃）", with a scope. "As a
  whole" keeps one applicant's withdrawal from ruling out an approval others still await; "stands on the due day" keeps a
  prohibition that was lifted from counting (the third round's two cases, `iz-codex.md`); "taken after the article's day"
  keeps a bar already in place when the question opened from counting as its answer (the second-family reader's point,
  `ix-claude.md`: "No condition has a start date"). So a ruling out is new, whole and standing. The model's condition names
  the way an analyst expects; code's sentence takes the others; `Still open` is then what is left. The request tells the
  model the same scope, once, and that where both conditions would hold the event counts as happened.
- *Read by two families before any send (`dryrun13/`).* Four by-hand ladders as the judge sees them, and facts stated in full
  for the due day (several applicants of whom one withdraws; a prohibition lifted; a block under appeal; an approval
  revoked), each to be placed in a rung by a reader who sees nothing else; the key written first and held outside the
  folder. First reading, on the sentence before "taken after": both readers placed all 20 as the key. The second reading, on
  the final sentence with three scenarios of a bar already in place, is recorded in the round log (§69). Mark R fails an answer with no `Ruled out` rung where the event can plainly be
  ruled out, and a `Ruled out` condition that is only a waiting.
- *An event undone.* When both conditions hold as written (approved, then revoked), rung 1 is the answer: D409's first outcome
  is "发生了", it has happened by the due day. Asking for every condition as the position on the due day was tried and
  withdrawn: it turns a thesis that tracks an occurrence into one that tracks a standing status. A thesis that does track a
  status ("in force on the day") says so in its own `happened` condition. **Reported to Alex, not confirmed:** an event that
  happened and was undone before the due day counts as happened.
- *A fact nobody can know on the day.* The rungs are complete for what is true; whether it is known is not the ladder's to
  settle. The frozen judge forecasts the rung from its evidence (judging-v7: "The rung is your forecast"; "Only fact can
  establish that a rung's outcome already holds"). The labels answer the question printed beside them: `Yes` and `No`, or
  `Yes`, `Ruled out` and `Still open`. A condition that cannot be checked on the due day is mark R's.
- *What may be left unjudged.* D409 allows a difference inside an outcome to be listed; it does not allow the outcome the
  thesis tracks to be dropped. Which part of a thesis's wording is the one tracked is D397's rule and marks Q and L. Three
  outcomes cannot carry everything a thesis may track: an investigation's conclusion, its finding and what it imposes are one
  question only by choosing one of them, and the rest is listed. That cost was put to Alex with D409 (the council's dissent).

**After the second Stage A: the scope governs the model's own sentence (`stage_a/result-2/RESULT.md`; `dryrun14/`).**
- *The class, counted on the second run's 43 event ladders.* A ruled-out sentence that says "after" (31 ladders): R held by both
  readers on 27, failed by both on 1 (a question and an answer with different periods), disputed on 3. A ruled-out sentence
  with no "after" (11): failed by both on 3, held by both on 2, disputed on 6. One ladder has no ruled-out rung where one is
  plainly possible. So the sentence without "after" lies behind 3 of the 4 ladders both readers fail and 9 of the 14 failed
  under the strictest counting.
- *The mechanism.* The request asks for a ruling out "after the item's day" and the model writes it in about three answers of
  four. Code's sentence carried "taken after <day>" for "any other decision" only, so where the model's sentence left it out a
  decision already made before the article could be the ruling out.
- *The change.* One clause moved in code's sentence, so that "was made after <the article's day> and stands on <due day>" is
  said of the model's sentence and of every other decision alike. No rule Alex decided changes; the request is not touched.
- *The proof at no cost (fourteenth reading).* Six answers of the second run with no "after", each shown with the sentence as
  it was and as it is, with three sets of stated facts; the criterion fixed before any reader answered. Its result is in the
  round log (§69).
- *What this does not fix, counted:* a question and an answer with different periods (3 ladders of 2 theses); a missing
  ruled-out rung (1); a regulator's decision filed under the company (4 event ladders failed by both readers, all of theses
  that Step 1 opened as a policy stage; over both runs, 10 of the 33 policy-stage ladders filed under the company are failed
  on the object by both readers, and none of the 101 ladders of product nodes and binding obligations).

**The request** (`ladder/candidate-system.txt`, 7,123 to 6,872 characters; `candidate-closing.txt`, 661 to 812; the schema's
`yes_no` and `states` replaced by `event`). One sentence group changed in each, and nothing else:
- the system text's rule for an event, with the merger example in three outcomes, in place of the yes/no rule, the five-state
  construction and the label rules; "Fill exactly one of event and figure";
- the closing check's sentence for an event: that `happened` is the event asked about; that `ruled_out` is that event decided
  against or abandoned, not its merely being still awaited, and is null only when nothing can rule it out; and that each can
  be checked on the due day.
Every sentence's source is D409 in Alex's words above; the example is the request's own merger, a general one (AGENTS §6).

**New path against old checks (AGENTS §2, table 3).**

| what held for the old event shapes | under three outcomes |
|---|---|
| check 1: exactly one shape | kept: exactly one of `event` and `figure` |
| check 1: exactly five states | retired with the states |
| check 3: a company's five labels; a theme's five names, none a company label (D404) | retired: code writes every label |
| check 5: an event's due day basis is stated or period_end (D403) | kept, unchanged |
| check 6: the reference's words; an event's reference has no value in a range | kept, unchanged |
| check 6a: nothing points at the item | kept; reads the question and both conditions |
| check 7: an event's year is its due day's year | kept |
| mark R: exactly one rung for every outcome | by construction; R reads the two conditions the model wrote |
| mark F: a company's state labels and the Neutral baseline | retired for events: an event's rungs carry no bullish or bearish label, as a yes/no never did |
| production's `check_ladder`, two or five rungs | not on this path (§7.3) |

**Who reads the new values (AGENTS §2, table 2).** The rung labels `Yes`, `No`, `Ruled out`, `Still open` and
the three code-written sentences: the judge's prompt, which prints each rung as "rung N label: condition" (`judging.py` line
124), so "rung 1" in a condition names what the judge sees; the theme lines of other views, which print a theme's current rung
label after the theme's question (`judging.py` lines 147–154: "…question: now rung 3 Still open"), which is why a label
answers the question and is not a bare "Neither"; the readers' packet. Nothing on this path reads a label as a direction: `matching.
ladder_direction` and the frozen scorer read `lo` and `hi`, which an event's rungs do not carry.

**Prior decisions on the mechanism.** D399 allowed the request to teach five states; it is superseded. D404 named how a
theme's five states are labelled; nothing is left for it to apply to. D397 (one judged question, the rest listed) is what
carries a finer difference. D403 (an event's due day) is unchanged. D186 and D398 concern a figure's ranges and are unchanged.

**Tests** (`ladder/test_ladder_step.py`): two rungs when nothing can rule the event out, the second code's; three rungs with
code's two sentences, a condition with no full stop given one; the schema takes an `event` and refuses `yes_no` and `states`;
a condition of either kind that points at the item is refused. A mutant for each (41 of 41 caught).

**Not changed by this version:** a figure's ranges, reference, direction and due day (the classes that follow, D408; D411).

### 5.2.2 The reference: a reported amount named as that, a range carried as a range (D411; built and probed, not yet measured)

**The decision.** Alex, 2026-11-10, on whether an amount already reported may be the baseline of a ladder: "能用，但要标明": "可以拿来
当基准，但明确标成“最近一次已公布的数字”，不再叫“市场预期”；文章给的是区间（如 50%–60%）时也允许填区间。"

**Why.** In both Stage A runs the reference is the mark both readers fail most on figures (10 ladders in the second): an
amount already reported carried as what the market expects (the $119 billion of supply commitments, three theses), and an
expectation stated as a range ("approximately 50%-60%") that a field of one number could not hold, so that the judge was told
there was no reference figure. A typed field was missing (AGENTS §2); no sentence could have fixed either.

| part | before | now |
|---|---|---|
| `reference.kind` | none | `expected` (what the market expects: a consensus, guidance, the stated plan or deadline) or `last_reported` (for a figure only: the amount most recently reported for the same quantity, where the article states no expectation) |
| `reference.value`, `value_to` | one number or null | the number; for a stated range its lower end, with `value_to` its upper end; `value_to` null otherwise |
| check 6 | a figure's value lies in the middle range | the value lies in the middle range; for a stated range, the middle range runs from at or below its lower end to at or above its upper end; `value_to` is null or greater than `value`; `last_reported` on an event is refused |
| the middle rung, shown to the judge | `(the reference when the question opened: "<passage>")` | the same for `expected`; `(the amount last reported when the question opened: "<passage>")` for `last_reported` |

**The request** grew: the system text 6,872 to 7,316 characters and the closing check 812 to 1,037 (the first request: 7,123
and 661). The reason for the growth (AGENTS §6): the paragraph now defines two kinds and a range where it defined one kind and
one number; nothing else in it was a candidate for a cut that an audit has found. Every sentence's source is D411 in Alex's
words above and the paragraph it replaces.

**Shown at no cost** (`stage_a/reference_by_hand.py`, `stage_a/result-2/reference-by-hand.txt`): the second run's own answers
for two of the reported-amount theses, the range thesis and a control, with only the reference rewritten by hand into the new
shape: all pass the schema and the checks, and the judge's middle rung reads "the amount last reported" for the $119 billion
and carries the 50 to 60 percent passage where it said "no reference figure". This shows the field can now hold what the
article says; it does not show that the model fills it rightly. The file carries a counter-case on purpose: a ceiling of "up to
$105 billion" for one project entered as the amount last reported for a total passes every check, because code reads the words,
the kind's form and the range, never the meaning. "The same quantity" is defined in the request against a part, a ceiling and
another quantity, and mark XR owns it.

**What the council's read settled before any send (`council/je-codex.md`).**
- *The middle range spans a stated range from end to end.* My first rule placed a range by its middle; a range that ended
  beyond the middle range then passed. D411 keeps the range and does not say where it goes; D398's sentence does ("the middle
  range holds that value, the outcome near what is expected"): what is expected is the stated range, so the middle range
  starts at or below its lower end and ends at or above its upper end. The request, the closing check, the form and check 6
  now say exactly that, in those words (round two of the council found "the whole range" said in the request and something
  else checked). With "50%-60%" the natural ladder has a middle range of 50 to below 60: an outcome of exactly 60 falls in the
  next range, as any upper bound does in ranges that are closed below and open above. **Reported to Alex, not confirmed.**
- *"Otherwise reference is null"* now covers an event whose article gives a reported number and no expectation.
- *The wording was trimmed* where the paragraph, the schema and the closing check said the same thing three times: the schema
  keeps the fields, the paragraph how to choose, the closing check the reading back.
- *Not changed, and known:* a reference in words alone, and every reference of an event, is stored and is not shown to the
  judge; only a figure's reference with a number appears, in the middle rung. That was so before D411 and is outside it.

**Tests** (`ladder/test_ladder_step.py`): a reported amount is named as that and never as the reference; none on an event; a
range carried by its two ends and spanned end to end by the middle range (four cases); the
upper end greater and never alone; the schema asks for the kind. 121 tests; 48 of 48 mutants caught. The readers' form marks XR and X on the same rule.

**Sent twice, small** (round log §69). (1) The changed request once on 18 stored theses, with what was expected of each
written beforehand: the field was filled as written in all seven reference cases (the reported 119 billion as last reported
in three theses; "50%-60%" as a range under a middle range of 50 to below 65; the one-project ceiling of 105 billion no
longer a reference; 279 billion and 25 billion as last reported), and the two declines for no main thing were kept. (2) A
three-arm probe registered before its send (`probe-direction-2026-11-10/REGISTERED.md`, `RESULT.md`), the request as the
second run sent it against this one in the same run, three draws on twelve theses: the registered signals that the change
moved the favourable end or the events did not fire; a first answer a check would send back fell from 15 of 36 (all for
the quotation) to 6 of 36. Three draws show no rate and do not show the change safe.

### 5.2.3 The two halves of line 6, counted (2026-11-10; nothing built)

**The favourable end** (`stage_a/direction_census.py`; `stage_a/result-2/direction-by-thesis.txt`;
`probe-direction-2026-11-10/RESULT.md`). Eleven of the 44 theses draw a company's figure; nine are amounts the company
owes, guarantees or has committed. In both full runs the same two give both ends among their three sends. The model's own
account, on six stored sends, is that neither the topic nor the item says which end is good for the company. Two readers of
the texts alone, one of each family, find "lower" settled in none of seven such theses, where the working request answers
"lower" in 19 of 21 first answers. Letting the model answer `unclear` gave the two wobbling theses one answer and set two
steady ones wobbling: not shown to work by the test registered before the send, and not tuned further. "Position 1 is
Strongly bullish" for a company ladder is read in six places of production (the table in the probe's RESULT.md), so a
company figure shown with no direction is a change of the thesis library (D38, D186), not of this step. What the product
registers for such a figure is Alex's choice.

**The due day** (`stage_a/due_day_rule_replay.py`; `stage_a/result-2/due-day-rule-60-90.txt`). 68 of 71 figures of the second
run have a day the model estimated, and it differs between the sends of 15 of 21 figure theses by 1 to 45 days (median 4).
Set by code from the year (the fiscal year-end plus 60 days, a calendar year-end plus 90) the day is the same in 32 of 34
theses against 18. The replay also shows what the rule does to a figure that is not a year's: a survey's "next 12 months"
the ladder calls "2027" lands about eight months late, and a quarter that should have been declined about four. Sixty days
is a large US filer's deadline for its annual report and no promise that the figure asked for is in it; 90 days is a
convention. Whether code sets the day is Alex's choice.

### 5.2.4 Alex's two choices on line 6, as built (D413, D414; 2026-11-10; proved at no cost, not yet sent)

**D413, the favourable end of an amount the company owes.** Alex: "没表态时记越低越好". One sentence joins the request's
line on `favourable_end`, after the sentence that a result and its direction are separate: for an amount the company owes,
guarantees or has committed to pay, when neither the topic nor the item settles which end is good for the business, because
they argue both ends or say nothing on it, it is lower; when the topic's own words say that more of it is good, it is higher;
with one example of each from other trades (a retailer's lease guarantees; an airline's aircraft purchase commitments that
the topic tracks as the fleet growth its plan needs). One sentence joins the closing check. Nothing is cut: a cut beside a
change is a lever of its own. The decision stays the model's; code checks nothing new; mark F of the readers' form carries
the rule. Source of every word: D413. The cost Alex was shown and the council's reservation are in the decision's record.

**D414, the due day of a year's figure.** Alex: "由程序统一定".

| part | before | now |
|---|---|---|
| the due day of a figure whose basis is `expected_publication` | the day the model expects | set by code: the end of the year the figure covers plus 60 days for a company's figure (its fiscal year-end, from the research list's fiscal calendar), plus 90 days for a theme's figure (31 December); `ladder_step.due_day_of`, the one owner; the view carries it |
| the day the model writes for such a figure | the due day | kept in the answer's record, and read once: a day before the year's end means the figure the model has in mind is not that year's figure |
| check 5 | the day is after the item's day; a binding obligation within 548 days | the same two rules, read on the day the question is due; and a figure expected before its year ends is refused, the reason naming the two ways out (a quarter or half-year is declined; another period takes the day the item states, with basis `stated`) |
| a stated day; an event's day | the answer's | unchanged |
| line 6's count of the due day | the answer's `due_day` | the view's, the day the question is due (`stage_a/accounting.py`) |

**The request is not changed for D414.** A first build added a sentence to the due-day line telling the model that code sets
the day and by how much. The small send (`probe-d413-d414-2026-11-10/RESULT.md`) showed what it did: in about four sends in
ten the model wrote code's day as its own estimate, so the refusal below could no longer tell a rolling twelve months from a
year, and a made-up day labelled `stated` appeared in 7 of 80 figure ladders (none in 91 before). The sentence is out; the
line is the second run's, word for word; the model estimates as it did, and code replaces the estimate.

*State × event for the day.* The day is computed where the view is written, from the answer alone; nothing is stored between
runs, and a later run of the same answer gives the same day. A year the fiscal calendar does not hold leaves the answer's day
(the year's own check then refuses the answer). *Value × reader:* the view's `due_day` is read by the readers' packet, by
line 6's count and, in Stage B, by the judge's page; each reads the view. The answer's `due_day` is read by check 5 alone.
*New path × old checks:* the two old rules of check 5 now read code's day; replayed on the second run's 114 stored ladders
they refuse none. One reachable input they do now refuse, which no stored answer holds: a binding obligation's figure for
the fiscal year after next with an estimated day (opened in July 2026 for fiscal 2028, code's day is 2028-03-31, beyond the
548 days). The request's own rule for an obligation already taken on is its next annual filing, so the answer is sent back
toward that; a day the topic states is kept as before. *Why a day before the year's end is read as "not that year's
figure":* the request says a figure's publication date falls after the end of the period it covers; a year's figure cannot
be out before its year ends, and a forecast of it is not the figure. The reason sent back names the request's own ways out
and no new one: a company's quarter or half-year is declined; another period takes the publication day the topic or the
item gives; when neither gives one, nothing can be checked on a date and the answer is declined.

**Proved at no cost** (`stage_a/due_day_by_code_replay.py`, `stage_a/result-2/due-day-by-code-run-2.txt`): on the second
run's stored ladders the new refusal sends back 7 answers, all of the three theses known not to be a year's figure (the
quarter acc/clean-5; the surveys u1/clean-9 and u2/clean-8), and nothing else is refused; of the 33 theses whose three
answers the checks still accept, 31 have one due day (as sent: 18 of 34); the two that differ are an event with two period
ends and a figure filed under the company in one send and a theme in two. What a replay cannot show: what the model does
when the refusal is sent back to it. Tests: five on D414 in `ladder/test_ladder_step.py`, one changed with the spec (a
far-year binding obligation now needs a stated day); 126 tests; 55 of 55 mutants caught.

**The request** is now 7,815 characters of system text and 1,245 of closing check (the second run's: 6,872 and 812). The
growth is two decided rules (D411, D413), each a rule the audit showed missing; nothing was cut beside them.

### 5.2.5 After the third Stage A: four rules of Alex's, each tested alone (D416 to D421; built; measured in the fourth Stage A)

The third Stage A met line 6 and missed lines 1 to 3 (`stage_a/result-3/RESULT.md`). Alex kept the lines and ruled four
things; each went into the request only after a small send of its own beside the working request, with what does not pass
written before the send and the council's read after it (round log §69).

| decision | Alex's words | what changed | its own small send |
|---|---|---|---|
| D417 | "确认：这类题不出题" | a seventh case of no ladder, in the request's list and in the schema's own: a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, with no publication day in the topic or the item | `probe-d416-d418-2026-11-10/RESULT.md`: the two survey theses declined in 6 of 6 sends at the first answer (the control: 5, four only after code's refusal); no year's figure pulled into a decline |
| D420 | "② 算“明确落空”" | the event paragraph: an authority's investigation or examination that the question asks to end in a published decision or conclusion always has a ruling out, the authority formally abandoning or withdrawing it without that decision or conclusion; its still going on is neither, and a decision to go on with it is no ruling out; one example from another trade | `probe-d420-d421-2026-11-10/RESULT.md`: the nine French answers all so (the control: 4 so, 2 with no ruling out, 2 wrong though not empty, 1 declined) |
| D418 | "归行业主题“芯片出口管制”" | the paragraph on the object: a question whose tracked outcome is a government's or regulator's decision to permit, restrict or ban a class of products or trade is the theme's, also for the company's own product; the company's own sales, shipments or revenue under such a decision, and a proceeding against the company, are the company's; one example from another trade | the first wording pulled the company's own sales to the theme in 2 of 3 sends and was held (the model's account: "applied that exception too broadly"); narrowed, same folder as D420: permissions 9 of 9 under the theme, the company's own sales 3 of 3 under the company |
| D416 | "先小额验证这个改法" | an event's `ruled_out` is `by_whom` (the company, authority, court or party whose decision it would be) and `decision` (one full sentence naming them and what they decide against the event as a whole, or that they abandon or withdraw it); null only when no one's decision can rule the event out; the event paragraph, its three examples, the closing check's event sentence, the schema. Code shows the judge the decision as the second rung's first sentence, as before, and checks that neither part is empty (`ladder_step.ruling_out_of`); it reads the earlier one-sentence shape too, for stored runs | the first trial failed its registered stop on the French kind, before D420 existed (`probe-d416-d418-2026-11-10/RESULT.md`); the second, after D420, alone: no stop fired (`probe-d421c-2026-11-10/RESULT.md`). On the six product-deadline theses, the two trials together: no wait written as the ruling out in 36 typed answers against 9 in 36 answers of the one-sentence shape sent in the same minutes |

**Why a typed ruling out** (D416's diagnosis, `stage_a/result-3/wait-as-ruling-out-hand-read.md`): of 140 stored event answers
read in full, 7 wrote the wait as the ruling out, six of them on product-deadline theses; by the model's own account the rule
was understood and slipped in one pass. A free sentence has a place for "the day passes"; who decides and what they decide
has none. What the shape does not exclude, and D420's rule does: a decision to go on with a proceeding.

**Value × reader for the typed parts.** `decision` is read by `ruling_out_of`, and through it by the rungs' writer and by
the check for a condition that points at the item; `by_whom` is read by its emptiness check and by the readers' packet
(`other_fields.ruled_out_by`); the judge is shown `decision` alone, inside the second rung. Scripts that print stored runs
read either shape.

**The request** is now 9,545 characters of system text and 1,325 of closing check (the second run's: 6,872
and 812). The growth is six decided rules (D411, D413, D416, D417, D418, D420), each a rule a measurement showed missing and
each with its examples; nothing was cut beside them, and D414's sentence was added and removed.

**The readers' form** carries D417 (the seventh allowed refusal), D418 (the object rule; mark O), D420 and D416 (the event
rule; mark R; `ruled_out_by`). The third readers' hand-off now carries the list of themes the first readers' always did
(`ladder/stage-a-third-reader-handoff-template.md`).

### 5.3 What code does with the answer (each check with its source)

1. **Shape.** Exactly one of `no_ladder` and `ladder` is null, and inside `ladder` exactly one of `event` and `figure` is not
   null (§5.2.1). A figure's `ranges` are exactly five: four or six is a refusal, counted here and nowhere else (§5.2).
   `no_ladder`: record the reason; no view. The tests send a four- and a six-range answer through the step's entry point with
   a fake transport: each is refused and resent; an answer with both shapes, or neither, is refused.
2. **Object.** `universe.resolve(object)` must be the run's company (`object_kind` company, `kind` asset) or a listed theme
   (`object_kind` theme, `kind` theme). Anything else is refused, and resent like any refusal: the request tells the model to
   return `no_ladder` for a question that belongs to another company or to a matter no listed theme covers, naming it (the clean
   path holds one company, D187 not being built; an unlisted theme is not opened, as in production's `matching.py`, §4). The name
   in such a `no_ladder` is reported as a suggestion. Whether the object is the right one for the question is not something code can
   establish (mark O).
3. **States: retired (D409).** Until version 31 this check held a company's five state labels and a theme's five state names
   (D404). An event now has no state the model names or labels: its rungs are written by code (§5.2.1), so there is nothing for
   the check to hold, and its tests left with it.
4. **A figure.**
   - **The numbers are read as written.** Production's `model.py` parses an answer with `json.loads`, which turns numbers into
     floats before any check could see what was written (`1e-400` becomes zero). The step therefore keeps the answer's own text
     (the string in `choices[0].message.content`, taken by a wrapper round the transport it is given; one wrapper a call, since
     calls run at once) and parses it a second time, reading each number token with Python's exact decimal type, which holds
     any length of digits, so the rule below decides by the number's value and not by how it is spelt (`1e+0000` and
     `1.0000000000000000000000000000000` are the number 1). The decimal type refuses only an exponent beyond about 10^18
     (`1e999999999999999999999999` raised; reproduced); no mantissa an answer can carry brings such a value back into the set,
     so that token, like `NaN` and `Infinity`, which Python's parser lets through, is read as "outside the set", and the parse
     never raises on a number. Checks 1 to 7 read this second parse and no other, so every bound,
     and a reference's value, is the exact decimal the model wrote, or "outside the set". An answer the model archive returns
     from its cache has no such text: the step refuses it and stops the replay (§7.1).
   - **Any finite number.** A bound, and a reference's value, is accepted when it is a finite number: the decimal type holds
     it, and its nearest float is finite too. `NaN`, `Infinity`, `1e400` and a token the decimal type cannot hold are a refusal,
     resent like any other (check 8). The request asks only for "a number"; there is no limit on size or digits. One difference from the request is known and
     kept: a number beyond a float's range (about 1.8e308), or an integer of more than 4,300 digits (check 8), is refused though
     the request does not say so. No item states such a number, and a sentence about it would be a rule for a case nobody has. Versions 20 to
     29 had one (zero, or 1e-9 to 1e18, fifteen significant digits), so that the float kept in production's `rungs` table would
     equal the number written. Eleven reviews in a row found a new corner in it, and no reader on this path reads that float
     (§5.4). The limit served nothing here and is retired.
   - **What is kept, and what is a copy.** The exact decimal the model wrote is what the checks compare, what the rung's text is
     written from (check 7) and what `checked_answer` keeps. `rungs.lo` and `rungs.hi` hold `float(decimal)`, Python's nearest
     float, which can differ from the decimal past the fifteenth significant digit: a copy for production's readers of that
     table, none of which runs on this path. `ladder/number_rule_check.py`: 400,000 random numbers of up to thirty digits, none
     changed by its written text; fourteen spellings and sizes accepted and six refused, as this rule says.
   - **The ranges.** Code sorts the five ranges by `lo`, the open-below range first, so the order the answer lists them in does
     not matter. The sorted bounds, compared as exact decimals, form one unbroken partition, open above (`check_bounds`), open
     below (D38: the rungs cover every outcome; a test `check_bounds` lacks), with no range holding no value (`empty_rung`).
   - **Direction.** For a company's figure `favourable_end` is higher or lower and `favourable_why` is not empty; for a theme's
     figure `favourable_end` is n/a and `favourable_why` is empty. Any other combination is refused (D186; D38), so check 7
     always has an end to order a company figure from.
   - **Year and unit.** The year has one of two forms: `FY` and four digits, or four digits alone; a span of years or any other
     text is refused. Code tests the whole string (the validator's pattern search lets a trailing line break through). A company's figure carries the `FY` form and a theme's the bare
     calendar year, and the other form is refused (v74i line 26: "Company figures use the company's fiscal year … Other figures
     use calendar years"). The schema's units are production's list with the literal
     `other` where production writes `n/a`; a figure in any other unit is written with `other`, its ranges are rendered as bare
     numbers, the question must name the unit, and mark Y reads that it does.
5. **Dates.** The article's day is the day every date test uses; the replay refuses a trace that is not in day order
   (`adapter.py` line 305), so it is also the latest day processed, which is how D38 counts the year. `due_day` is a real date
   after the article's day (`extraction.sift`). For `opens_as` binding_obligation, at most 548
   days after the article's day: production's number for 18 months (`extraction.BINDING_HORIZON_DAYS`, in `check_admission`),
   which the request states in days too, since eighteen calendar months can be 549. The tests take day 548 (accepted) and day
   549 (refused). A figure of a year beyond next year is refused, a
   binding obligation excepted (`beyond_next_year`; D46). A figure of a year whose period ended before the article's day is refused,
   with no exception (D38); the period is `universe.fiscal_period` for the company's `FY` year and the calendar year for a theme's. Production's quarterly pattern (`extraction.QUARTERLY`) is **not ported**. Production
   drops a company candidate that is not an event when the pattern matches its `looks_at` or its question (`sift` lines
   625–627). The pattern matches Q1 to Q4, the word "quarter" wherever it is not the start of "quarterly report", and wordings of a
   half-year's revenue or sales. On this path the question must name the material that settles it
   (D38), and that material is quarterly reports for 14 of the 34 stored theses (the pattern matches their `settled_by`, and
   none of their `outcome` or `description`). So a sound annual question that names "the fourth-quarter release" would be
   refused. That is a risk and not a count: the seven fixture questions, written by hand for this path, match the pattern in none. One
   constructed case shows it: the ninth reading's first item, an annual figure whose question names "its fourth-quarter
   earnings release", holds every mark for both readers and is matched by the old pattern.
   Stage A measures it: code reports every written company figure whose `outcome` or question the old pattern matches, beside
   its Y mark. A company's quarterly or half-year figure is the request's refusal case, read by mark N; a ladder written for one
   fails mark Y, which says so in the form (ninth reading, §8). `due_day_basis` fits the shape: stated or
   expected_publication for a figure; stated or period_end for an event (the request's own rule; v74i lines 16 and 26).
6. **Reference.** `reference.words` must be the article's own words in one unbroken passage (D405). The words are accepted when
   they occur in the article exactly. Otherwise both of these must hold: production's `extraction.repair_quote` returns a
   passage of the article that holds the quote's words and no others, in the quote's order, as production's quote tokeniser
   reads words (`extraction._quote_tokens`); and the quote occurs whole in the article once the article's footnote markers
   (`[5]`) are taken out and spacing, letter case and the forms of quote marks and dashes are set aside (`extraction.normalise`).
   A quote that leaves out, adds, moves or changes a word, a number, a sign or a punctuation mark of the article is therefore
   refused, never repaired (Alex's choice between this and production's repair rule, D405): "does expect" is not accepted for
   the article's "does not expect", nor a full stop written where the article goes on with a comma. Production's repair looks
   at no quote of fewer than eight characters, so one that short is accepted only when exact.

   **Corrected after Stage A's send.** As first built, the check asked that the quote's normalised text occur whole inside the
   repaired passage (the Step 1 runner's `preserves_quote`). Stage A showed it refusing the article's own words: where the
   article reads "… up from roughly 30% today [5] ." the repaired passage stops at "today", and a quote ending "today." was
   refused: 6 of the 141 references of the run, all of one thesis, whose three sends ended refused twice for it. The rule above
   is D405's record with one more thing set aside, the footnote marker, which is the page's and not the article's words; the
   first clause, on the passage's words, also refuses a passage that holds words the quote does not. A wider first correction
   (words only, punctuation set aside) was withdrawn after council `it` showed it accepting a dropped "≥". The stored run was
   replayed through the rule at no cost (`stage_a/recheck_stored_run.py`): 3 sends change and 129 stand. The marker set aside
   goes to Alex with the result. Two weaknesses the first rule also had are left as they are, having no instance in the run: a
   quote joined across a paragraph break (0 of 85 accepted passages span a line break) and an exact match cut out of a word or
   a number (0 of 68 exact matches).

   **Check 6a. Nothing in the question or a condition points at the item (D407).** The judge reads the question later, without
   the article. The judged question and both conditions of an event are read for "this item", "in the item", "the item's",
   and the same with "article"; a match is a refusal, sent back with the instruction to put the specific information in its
   place. The pattern is the closed set of wordings the sends showed: two instances in the 27 ladders stored before the build;
   nine answers in Stage A, each read and each a true instance. "The Article 232 tariffs" is not matched. One wording it does not
   catch was seen once in Stage A ("at the item date"): mark Q owns the rule, and the check is not widened on one instance.

   For the reference, the runner's further path, a lookup index, is not
   used: a refused reference is resent. What is written is the article's own passage: it is stored in `clean_ladders`, given to
   readers and, when a figure's reference has a value, shown to the judge in the middle rung (check 7); the model's own words stay in the outcome record. The tests: exact words;
   words that differ in letter case or a curly quote mark only (the article's passage is written); a footnote marker before the
   full stop, as Stage A met it, and one between two words (accepted, the article's passage written); a left-out "not", a moved
   word, an added word, a quote that runs on past the article's text, a dropped comma, a full stop where the article has a
   comma, a dropped sign, and a repaired passage holding words the quote does not (each refused); a quote of fewer than eight
   characters (accepted only when exact). A reference's `value` is a number the item
   states, under the number rule of check 4, or null. When a figure's reference has a value, it must lie in the middle range
   (`lo` ≤ value < `hi`, compared as exact decimals): D186, "near guidance"; D398, "a stated reference value". When a figure's
   reference is null or has no value, the ladder is recorded as "no reference figure" and its ranges are the model's estimate.
   An event's reference is recorded and not shown to the judge, who states a reference of its own from the evidence (D260).
   Code establishes only these things; that the value is the number the words state, that no stated number was left out, and
   that the words are what the market expects, are readers' marks (X and XR). The tests add: a figure whose reference has words
   and no value (accepted, "no reference figure", no reference in the middle rung); a value outside the middle range (refused).
7. **Labels and conditions:**
   - an event: `Yes` with the condition given; `Ruled out`, when a condition is given for it, with that condition and
     code's sentence (it holds when that, or any other decision against the event as a whole, or its abandonment or
     withdrawal as a whole, was made after the article's day and stands on the due day, and only when rung 1 does not); and
     a last rung written by code, `Still open` ("Neither rung 1
     nor rung 2 holds on <due day>.") or, with two rungs, `No` ("Rung 1 does not hold on <due day>."): §5.2.1;
   - a company figure: position 1 is always Strongly bullish, as production stores a company ladder. With the higher end
     favourable, position 1 holds the highest range and the ranges run down to the lowest at position 5, Strongly bearish; with
     the lower end favourable, position 1 holds the lowest range and they run up (the split's `ordered_ladder`, ported with its
     tests; `ladder/examples.json` shows both). Each condition is its interval;
   - a theme figure: positions run from the lowest range to the highest; the label and the condition are the interval.

   An interval's wording is the split's `render`: `below <hi> <unit>` for the lowest range, `<lo> <unit> or more` for the highest,
   `from <lo> <unit> to below <hi> <unit>` otherwise; the unit is omitted when it is "other". A bound's number is written from the
   decimal the model wrote: `0` for zero; a whole number as its digits, with thousands separators once it is 1,000 or more in
   size (`119,000,000,000`; `73`; `-250`); any other number in plain notation, with no exponent and no trailing zeros (`0.5`;
   `3.5`; `1234.5`). This replaces the split's six significant digits. The text, read back as a decimal with the separators
   removed, equals the number the model wrote, which code asserts; so the text the judge reads, the stored bound and the number
   the model wrote are one number. The tests give the number rule JSON text: a positive, a negative, a decimal and zero;
   `73.50`, `9007199254740993`, `2.5e18`, `17234567891234567.89`, `1e+0000` and `1e-400` (each accepted, with the text check 4's
   script prints for it); `1e400`, `NaN`, `Infinity` and `1e999999999999999999999999` (each refused and resent, through the
   step's entry point); a reference value at the lower
   bound of the middle range (inside) and at its upper bound (outside); an answer returned from the cache (the run stops). For
   direction: a company figure with n/a or an empty reason, and a theme figure with higher (each refused).
   When a figure's reference has no value, or is null, its middle rung's condition is its interval followed by
   ` (no reference figure when the question opened)`: v74i line 25 asks that the neutral comparison be stated, and D398 that such
   a ladder be marked. When a figure's reference has a value, its middle rung's condition is its interval followed by
   ` (the reference when the question opened: "<the article's passage, check 6>")`, so the judge reads the neutral comparison in the condition, as v74i line
   25 asks; a label never carries it. A figure's rung carries no other text, so what the judge reads cannot differ from the bounds;
   `band_problem` is not ported for that reason. `ladder/examples.json` gives one answer of each shape with the rows written for it.
8. **A refusal** by check 1 to 6a is sent once more: the same request, followed by the refused answer in full and the reasons. An answer that is not JSON, or does not fit the
   schema, is a refusal too: production's `model.call` archives it and raises `SchemaError`, which the step catches and treats as
   a refusal with that reason. Three answers make `model.call` raise something else: an integer of more
   than 4,300 digits (`ValueError`, Python's limit) and brackets nested too deep (`RecursionError`), in its own parse, before it
   archives anything; and a string that is not valid Unicode, such as a lone surrogate, when the archive tries to store the
   answer (`UnicodeEncodeError`, a kind of `ValueError`). All three were reproduced. The step catches `ValueError`, with every
   kind of it, and `RecursionError` when its wrapper holds a response for the call, and treats the answer as not readable: the same refusal, resent once. Its text and tokens are in the wrapper, so the outcome record and the spending
   limit hold them though the archive has no row. Any other exception is not an answer's fault and stops the run. The outcome record is written as JSON with every
   non-ASCII character escaped, so that it can hold any text an answer carried; such an answer never reaches checks 1 to 7,
   so no view is ever written from it. The second answer is taken as it comes: a ladder
   that passes is written; a `no_ladder` is recorded with the model's reason and the first refusal's reasons; a second refusal
   records "no ladder: refused" with both sets of reasons. A response with no text (cut at the output cap, or declined by the
   provider) is an answer that is not JSON.

   **What is kept of each of the two requests, and what it cost.**
   - *Cost.* Every request of the step goes through the measurement's spending limit, `e2e-2026-11-09/budget.py`, the wrapper the
     adapter already sends the judge through. Before a send it reserves the request's worst case (every byte of the request as an
     input token, plus the output cap) and refuses a send that would pass the cap. As each response arrives, before anything
     parses the answer, it charges the response's own token counts at the published rates, or the whole reserve when the
     response carries none. The cap and every cost reported come from this limit, never from the model archive: production
     writes zero tokens and zero cost for an answer that is not JSON (`model.py` line 265).
   - *Text.* The step's own wrapper sits inside the limit and keeps the answer's text in full. The model archive is not its
     source: it cuts a stored response at 200,000 characters.
   - *The outcome record* of a thesis holds its requests, one or two, and for each: the request's sha256, the answer's own text
     in full, its token counts, and its result (a ladder, a `no_ladder`, or refused with the reasons). Stage A writes the record
     to its pass's folder; the replay writes it to `clean_ladders` (§5.4).
   - *Tests*, through the real `model.Archive` and `model.call` with a fake transport: an answer that is not JSON and carries
     token counts, then a sound one; an answer longer than 200,000 characters. In each the record holds both answers in full and
     the limit's spend counts both, while the archive's own row shows zero cost or a cut response. And an answer holding a
     4,301-digit integer, then one nested 100,000 deep: each refused and resent, each in the record with its tokens.

**What code establishes and what readers judge.** The checks establish the answer's shape and the few facts above; they say nothing
about whether a ladder is right. Every property of substance is a reader's mark in Stage A, and the marks are a closed set: Q (the
question is the thesis's), O (the object), R (exactly one rung holds; Yes is the event and No its complement; states neither overlap
nor leave an outcome out), D (the due day is supported), X (the stated expectation is placed rightly), F (the direction), Y (the
year and unit), G (the ranges), L (every other part is listed), XR (the reference field is right and is not left out), N (a refusal
is justified), and W, any other fault that would mislead a reader, named by the reader. A fault no check sees is expected; it is a
defect of this design only when no mark would catch it. The dry run of §8 plants one fault under each mark and reads whether the
readers catch it.

**One table for the cases where no question is written,** so the request, the schema and the code cannot drift apart:

| case | the request says | the schema | code |
|---|---|---|---|
| the outcome names several things, none the main one | return `no_ladder` | `no_ladder` a reason, `ladder` null | records it; readers judge it (N) |
| nothing can be checked on a date | return `no_ladder` | the same | records it; N |
| a company's quarterly or half-year figure | return `no_ladder` | the same | records it; a ladder written anyway is not refused by code and fails mark Y, whatever the thesis asks |
| a figure for a year already ended | return `no_ladder` | the same | records it; a ladder written anyway is refused (check 5) |
| a figure beyond next year, unless `opens_as` is binding_obligation | return `no_ladder` | the same | records it; a ladder written anyway is refused (check 5), unless `opens_as` is binding_obligation, when it is accepted; the tests take both |
| the question belongs to another company or to a matter no listed theme covers | return `no_ladder`, naming it | the same | records it and reports the name; a ladder written with such an object is refused (check 2) |
| an answer refused twice | — | — | "no ladder: refused", with both sets of reasons |

The unit list is production's (`extraction.UNITS`), with "other" where production writes "n/a" (check 4).

### 5.4 What is written, and who reads it

Everything a replay day writes before its judging (the views, rungs and ladder records of the theses its articles opened, then
the evidence, links, repeats and revisions of those articles) is **one commit** of the run's `views.sqlite`, made once, before that
day's round, as the adapter commits today: all of the day or none of it. A run folder holds one draw, in which a thesis id is
unique; Stage A, which reads theses of several draws, writes no `clean_ladders` and keys its files by case (§8). The ladder record is a row
of a table this path adds, `clean_ladders`, keyed by the thesis id; its columns are in the field-by-field table below. It keeps
each answer's own text in full, so the checks can be run again on it at no cost.

| value | written to | readers on this path | readers elsewhere, not run on this path |
|---|---|---|---|
| view id `v<N>` for `clean-<N>` (the thesis's own number) | `views.view_id`; `clean_ladders` holds the pair both ways | the judge's first line; `themes_shown_in`; `judgements`; the reader packet | — |
| `object_id`, `object_kind` | `views` | `themes_in_force`, `queued_by_change`, `open_asset_views`; the judge prompt | matching |
| `kind` | `views.kind` | the judge prompt | — |
| `question`; `looks_at` := the thesis's `outcome` (with `object_id`, the three texts of `views_fts`) | `views`, `views_fts` | the judge prompt: `question` after the header, and `looks_at` inside it as `focus "…"` (`judging.py` line 123), which Stage A's packet shows as `focus`; other views' theme lines | production's matching search (`views_fts`); production's extraction request (`store.views_open_at_day_start`; `views_for_prompt` has no caller). The clean Step 1 reads its own library state, never these |
| `due_day`; `year` (a figure's from the answer, an event's the due day's year) | `views` | the judge prompt, which shows both and prints a theme's due day in other views' prompts (`judging.py` lines 123 and 154); the replay's due-day guard reads `due_day` (§7.1) | pull mode reads `due_day` (`pull.py` line 31) |
| the open switch, written with the view by `store.create_view`: open, reason "created", by "matching" (the function's fixed values), after the opening article's sequence number | `view_switches` | `store.is_open`, which decides whether a view is judged; nothing on this path closes a view | pull mode; a person's switch |
| rung `position` | `rungs` | `store.rungs_of` orders the rungs by it; the judge prompt prints it and a judgement names its rung by it (`judging.py` line 123) | — |
| rung label and condition | `rungs` | the judge prompt (label and condition); theme lines of other views (the current rung's label only, `judging.py` line 149) | — |
| rung `lo`, `hi` (the nearest floats, check 4) | `rungs` | none on this path: Stage A's counts and the report read the exact decimals of `checked_answer`, and readers see a figure's ranges as the conditions' text | `matching.ladder_direction`; the frozen scorer; the product's pages (`bundle.py` line 45) |
| `created_seq` | `views` | the adapter's leakage check: no view, evidence or link numbered after the day's last article (`adapter.py` lines 235–241) | — |
| `created_from_input` | `views` | no reader on this path; written as production writes it | the product's pages (`bundle.py` line 99, `service.py` line 157) |
| `created_at` | `views` | no reader on this path; written as production writes it | none found in `src/hivemind/` |
| `thesis_id`, `view_id` | `clean_ladders` | the adapter's link writer, which sends a link to `clean-<N>` to `v<N>` when the row has a view; the packet's builder | — |
| `config_checksum`, `article_seq`, `article_day` | `clean_ladders` | the report: which configuration wrote the row, from which article | — |
| `not_judged`, the favourable end and why, the reference and `due_day_basis` (inside `checked_answer`); `reference_status`; `status` and a "no ladder" `reason`; the `outcome_record` | `clean_ladders` | the reader packet's builder and the report; shown to a user beside the answer. The thesis's own wording is not copied here: the packet's builder reads it from the Step 1 trace, its one owner | — |

**The complete writes, field by field.** A written ladder is one call of `store.create_view` and one row of `clean_ladders`; a
thesis with no ladder is the row alone. `ladder/examples.json` shows a projection of these for eight answers; the build's tests
read back every field below for each of them, for a `no_ladder` and for an answer refused twice.

| argument of `store.create_view` | value |
|---|---|
| `view_id` | `v<N>` for thesis `clean-<N>` |
| `object_id`, `object_kind` | what `universe.resolve` returns for the answer's `object`: the ticker and `company`, or the theme's id and `theme` |
| `kind` | `asset` for the company, `theme` for a theme |
| `looks_at` | the thesis's `outcome` |
| `question` | the answer's `question` |
| `due_day` | the answer's `due_day` |
| `year` | a figure: the answer's `year`; an event: the four digits of the due day's year |
| `rungs` | check 7's rows in position order: `label`, `condition`, and for a figure `lo` and `hi` as floats, null at the open end; an event's rungs carry no `lo` or `hi` |
| `seq` | the opening article's sequence number |
| `input_id` | the `input_id` of the opening article's evidence, or `article:<sequence>` (below) |
| `created_at` | the article's day at 00:00:00Z |

The function itself writes the open switch (open, "created", by "matching", after that sequence number) and the search text.

| column of `clean_ladders` | a ladder | the model's `no_ladder` | refused twice |
|---|---|---|---|
| `thesis_id` | the thesis id | the same | the same |
| `view_id` | `v<N>` | null | null |
| `status` | `ladder` | `no ladder` | `no ladder: refused` |
| `reason` | null | the model's reason | null; the reasons are in the outcome record |
| `reference_status` | a figure: `reference figure`, `last reported figure` (D411) or `no reference figure` (check 6); otherwise null | null | null |
| `checked_answer` | the accepted answer as JSON, numbers as the model wrote them, `reference.words` replaced by the article's passage | the answer as given: the reason, and `ladder` null | null |
| `outcome_record` | check 8's record: one or two requests, each with its sha256, the answer's text in full, token counts and result | the same | the same, two requests |
| `config_checksum` | the ladder configuration's checksum | the same | the same |
| `article_seq`, `article_day` | the opening article's | the same | the same |

- `created_seq` is the opening article's position in the Step 1 manifest. `created_from_input` is the `input_id` the adapter writes
  for that article's evidence sources, so a view and its opening evidence name the same item; when the article kept no record,
  `article:<sequence>`, the adapter's existing fallback. `created_at` is the article's
  publication day at 00:00:00Z, never the wall clock.
- **Order at an article** (sequence number k, its publication day): first the ladder calls of the theses that article opened,
  and their rows, written and not yet committed, so each new view exists at k; then the article's records as evidence with their links; then the later
  links Step 3 made while processing it. This is the order the adapter already uses for the Ohio view.
- **Links, and how the adapter learns of a new view.** The adapter keeps a set of the views it may link to and judge and a map
  from a clean thesis to its views (`self.views`, `self.mapping`; `adapter.py` lines 144–145); its link writer drops a link to
  anything outside them (lines 193–204) and its send check refuses a judge request for a view outside the set (lines 255–261).
  In the new mode both start empty. When a ladder is accepted for `clean-<N>`, the adapter adds `v<N>` to the set and
  `clean-<N>` → `v<N>` to the map as it writes the view, before that article's links are written. A thesis with no ladder gets
  neither entry: a link to it is not written and is counted "link to an unjudged thesis". The test follows one new view from
  its ladder through a link to the judge's request, and one refused thesis whose link is counted and not written. Evidence, repeats and revisions are written as the Stage 2 adapter writes them
  (`e2e-2026-11-09/adapter.py`).
- The only writer of a view on this path is the ladder step; the only writer of evidence and links is the adapter; one process owns a
  run folder, which it creates and refuses to reuse.

## 6. The judge: production's, unchanged

`judging.round_of_judgements` once a day over the views that got a new link that day, as `round.judge_day` and the adapter run it.
"Unchanged" includes: the evidence in view (D198); the theme block, and a changed theme queueing every open company question with
evidence (D195); the first 400 characters of a quote; and two refusals of one judgement stopping the day. The adapter's leakage,
selection and budget checks carry over; it gains a mode that builds no seed and no ruler view.

## 7. The three tables (AGENTS §2)

### 7.1 State × event

**States of a thesis:** opened (no row in `clean_ladders`); laddered (a row and a view, no judgement yet); judged (a view with at
least one judgement); no ladder (a row, no view; terminal); due (the judging day has reached the due day).

**Dates and sequence numbers.** The ladder call reads the opening article's publication day from the trace. A view is written with
that day and that article's sequence number. A judging round uses the day's last article's sequence number and that day as its
publication day, as the adapter does. The due day comes from the answer. Nothing reads the wall clock.

**Stop rule of this replay.** A run folder is created once and never reused; its model archive lives in it. A replay that crashes
or stops, at any point and for any reason, ends there with a non-zero exit: the program starts nothing again, and nothing of a
stopped folder is ever resumed or read by a later run. A new replay is a new folder, launched by whoever launched the first, and
sends every ladder call and every judgement again. There is no count of tries in the program. Resuming a stopped run is
production's rule (`has_judgement`, `queued_by_ledger`) and is not designed here (§9). Below, "the stop rule applies" means this.

| state | event | what happens | what is written |
|---|---|---|---|
| opened | the answer passes the checks | the view is created | in the day's one commit: view, rungs, ladder row |
| opened | the answer is refused by a check, does not fit the schema or is not JSON | sent once more with the refused answer and the reasons; the second answer is taken as it comes: a passing ladder, a `no_ladder`, or a second refusal, which ends as "no ladder: refused" | the outcome record holds both answers in full, each with its token counts and its reasons (check 8); the ladder row carries it |
| opened | the model returns `no_ladder` | ends as "no ladder" with its reason | the ladder row |
| opened | a ladder names another company or an unlisted theme | refused by check 2 and resent, as any refusal (the row above the last) | as for a refusal |
| opened | the model archive answers a ladder request from its cache | it cannot in a folder used once, where each thesis has one request and a resend differs by its appended reasons; if it does, the step has no text of the answer to read the numbers from: the replay stops with a non-zero exit, and the stop rule applies | nothing for this article's theses |
| opened | a send would pass the spending cap | the limit refuses it before it is sent (`OverBudget`); the run stops with a non-zero exit and nothing is skipped. The cap is never raised (AGENTS §9); in Stage A the result reads NOT MEASURED and goes to Alex | nothing for this article's theses |
| opened | the transport fails after its retry policy | the replay stops at that article with a non-zero exit; nothing is skipped; the stop rule applies | nothing for this article's theses |
| opened, laddered or judged | a crash or an error at any point before the day's commit: during a ladder call, or while views, evidence or links are being written, at any article of that day | the day's commit is all or nothing, so nothing of that day is in `views.sqlite`; the model archive, which commits each call, keeps the answers that completed, and the spending limit has charged them; the replay stops with a non-zero exit; the stop rule applies | nothing of that day |
| opened | one article opens several theses | each gets its own call; the calls read nothing of each other and may run at once; all of the article's calls return before its rows are written, in thesis-id order, by the one writer, inside the day's commit. If one call fails in transport, the others are awaited and the answers that complete stay in the folder's model archive, nothing of that day is committed, and the replay stops; the stop rule applies | nothing of that day |
| laddered, judged or no ladder | a later article links to the thesis | links only; a thesis with a ladder row is never sent again | links (none for "no ladder", counted) |
| laddered or judged | a later article restates the date or the amount | it is evidence; the ladder stays (D38; D248: "a later deadline is evidence while the earlier is open") | evidence and a link |
| any | Step 1 opens a second thesis for the same bet (its identity miss) | the second thesis gets its own ladder and is judged apart; no merge here. Stage A does not count duplicates: its form judges each item on its own, and a duplicate is Step 1's identity miss, outside this step | a second row and view |
| any | a corrected article | the Step 1 trace of a draw is never edited; a corrected article is a new Step 1 run and a new draw | — |
| any | another writer, or another configuration | none: one process creates and owns the run folder, with one ladder configuration, whose checksum every ladder row carries | — |
| laddered or judged | a new link that day | judged in that day's round if it has evidence in force; once per sequence number | a judgement, committed alone (production) |
| laddered or judged | a theme's conclusion changed that day | queued by `queued_by_change` if it is a company question with evidence | a judgement |
| laddered or judged | no new link and no changed theme that day | not judged that day; its last conclusion stands | nothing |
| judging | one answer refused | retired and sent once more with the reasons (production) | the retry |
| judging | refused twice, on a first or a later judgement of the view | the day stops with `JudgementRefused` (production); the view's earlier judgements and the day's committed ones stay in the folder; the stop rule applies | — |
| judging | the transport fails, or the spending cap refuses a send, on one judgement of a level | the round raises. The judge sends one level of views at once from a thread pool and records nothing of the level before every call has returned (`judging.py` lines 317–329). The pool waits for the level's other calls: those that complete are archived and charged, and none of the level is recorded as a judgement. Judgements of earlier levels that day stay committed. The stop rule applies | — |
| judging | the transport fails, or the cap refuses, on the resend of one refused judgement | this happens later, while the level's answers are checked and recorded one by one (`judging.py` lines 319–329): the views of that level recorded before it stay committed (`_record` commits each), the refused view and those after it in the level have no judgement, and their first answers stay in the archive, the refused one retired. The round raises; the stop rule applies | — |
| judging | the process dies with calls of a level in flight | a call in flight may have been sent and billed and leaves nothing in the archive; answers that had returned are archived; judgements already recorded are committed. The adapter's spending count is in memory and is lost with the process: a limit of the adapter as it stands, for Stage B's design to settle before any Stage B send. The stop rule applies | — |
| judging | the day or the run ends | a round is synchronous inside its day; nothing is in flight | — |
| no ladder | any later day | never judged; its links are counted | counts |
| laddered or judged | a replay day reaches the view's due day | closing is pull mode's (D356), which this replay does not run. The replay's days are the days that have an article, as the adapter builds them; a calendar day with no article has no step. The guard runs at the start of every replay day, before any view is created, any record written or any view judged or queued that day, one with no new link included, and once more after the last replay day, against that day; it reads the day and writes nothing: if an open view's due day is on or before the day, the replay stops with a non-zero exit and reports the view. A view that falls due on a day with no article is caught at the next article day, or by the end check when its due day is on or before the last replay day. A view due after the last replay day is still open when the replay ends, as it should be. No due day of the 34 falls inside the 14-day window | — |

### 7.2 Value × reader

§5.4.

### 7.3 New path × old checks

| check production applies to a candidate (`extraction.sift`) | this path |
|---|---|
| `check_ladder`: 2 or 5 rungs, non-empty text, company labels in order or reversed | non-empty text kept by the schema's patterns, which the validator enforces; the count of five ranges by check 1. Changed: an event has two or three rungs, written by code (§5.2.1, D409), where `check_ladder` allows two or five; `check_ladder` is called only by production's `extraction.sift`, which this path does not run, `store.create_view` takes any number of rungs, and the judge checks only that the rung it returns lies within the view's rungs (`judging.py` lines 212–213), so three rungs are written and judged with no change to frozen code. A company figure's labels are written by code |
| `normalise_ladder` | replaced: code orders the rungs from the favourable end |
| a quarterly company figure is not a view (a pattern over `looks_at` and question) | production applies it to a company candidate that is not an event (`sift` lines 625–627). Not ported as code: the pattern matches Q1 to Q4, "quarter" wherever it is not the start of "quarterly report", and half-year revenue wordings, and a question on this path names its settling material, quarterly reports for 14 of 34 theses; a risk, measured in Stage A (check 5). The rule is the request's refusal case, read by mark N, and a ladder written for a quarter or a half-year fails mark Y |
| not beyond next year (`beyond_next_year` reads any text and passes a string with no four-digit year) | kept for a figure (check 5), on a closed year format: `FY2027` or `2026`; any other text is refused by the schema, where production would let it pass |
| `due_day` a date after the item | kept (check 5) |
| `check_admission`: `settled_by` non-blank; 18 months | `settled_by` is non-blank by c8's schema (`pattern \S`), which the Step 1 runner checks on every answer (`runner.validate`); the horizon kept as production computes it, 548 days after the article's day (check 5) |
| `check_bounds`, which production applies only to a candidate carrying a typed key (`sift` line 644) | applied to every figure, plus the open bottom range |
| typed period dates valid (`period_start` ≤ `period_end`) and the typed key | a deliberate departure: the clean path has no typed period or key (D382), so this check has no counterpart; the due-day and year checks are what remains |
| the evidence checks | Step 1's; unchanged |
| `candidates_with_evidence`: a candidate opens only with at least one of its evidence ids kept, an owner's memo excepted (`extraction.py` lines 595 and 693) | not applied by this step: whether a thesis opens is Step 1's decision, made before this call. A thesis whose opening article kept no record still gets its ladder and its view; the view is not judged until a later link brings evidence (§7.1), and the run counts such views as "a view with no opening evidence" |
| what no check proves, here or in production | that an event's states cover every outcome, that the question is the thesis's, that the direction and the ranges are sensible: Stage A's readers judge these |

## 8. The test

### Stage 0 ($0): done in this review

§2. Two blind readers; their counts are reported side by side as a range.

### Dry run of the Stage A reading ($0): done in this review

`dryrun/` holds 18 hand-written ladders as the judge would be shown them: 7 written to be sound, one of each answer shape and a
justified refusal, and 11 each carrying one planted fault: one under each of ten marks, two under R and none under XR (`build_dryrun.py`; the key stayed outside the
repository until both readers had answered). Two readers of different families marked them blind with the Stage A form
(`reader-brief.md`; `score_dryrun.py`).

| | reader 1 (Codex family) | reader 2 (Claude family) |
|---|---|---|
| planted faults caught under their own mark | 11 of 11 | 11 of 11 |
| sound ladders given a failed mark | 3 of 7 | 0 of 7 |
| time for the 18 ladders | 25 seconds | 293 seconds |

- **Every planted fault was caught under its own mark by both readers.** That is ten of the eleven marks: XR had no planted
  fault, here or in any later reading. Readers have failed XR four times on answers I had written as sound (this reading's
  item 1, the sixth's item 1, the eighth's item 2, the eleventh's item 12), which shows that they use the mark and not how often they would catch a
  planted fault under it.
- **A planted fault often breaks more than one mark.** Readers failed further marks on some planted answers of the first two
  readings (a wrong due day also fails Q; a misplaced reference also fails G); the record below lists each.
- **The record of every reading is `readings_summary.md`,** generated by `readings_summary.py` from the stored answers: every
  failed mark and every fault named under `W`, by reader and item, and for the first two readings the planted mark beside it.
  The accounts below interpret that record and must agree with it.
- **The three marks reader 1 failed on my "sound" ladders were right:** two five-state ladders did not cover every outcome or let
  two states hold at once, and one reference quoted talks, which are not an expectation. The fixtures in
  `ladder/examples.json` were rewritten later (fifth and sixth dry runs).
  Five states that cover every outcome are hard to write even by hand, so mark R on five-state ladders is a risk for Stage A that these
  few hand-written examples illustrate; they say nothing of how often the model will fail it. The families again differ in strictness (round log §67); disputes go to the third reader with the article.
- **Reading time, an estimate from 18 hand-written ladders with short packets:** at the slower reader's 16 seconds a ladder,
  Stage A's 132 answers would be about 35 minutes read one after another. Real answers with their full articles may take longer;
  the time is reported and stops nothing.

### Second dry run ($0): the readings as the test will run them

`dryrun2/` (`build_dryrun2.py`, `score_dryrun2.py`; keys outside the repository until the readers had answered).

**A. Comparison packets** (`packet-a.json`, form `reader-brief-a.md`): three theses, six ladders each as the judge is shown them,
three written as the candidate would and three as a v74i-style answer would, the source hidden; 9 carry a planted fault. (The
test then had two arms; the packets still show that the form reads mixed ladders of one thesis side by side.)

| | reader 1 (Codex family) | reader 2 (Claude family) |
|---|---|---|
| planted faults caught under their own mark | 9 of 9 | 9 of 9 |
| unplanted ladders given a failed mark | 0 of 9 | 0 of 9 |
| time for the three packets | 15 seconds | 271 seconds |

(The test then had two arms and six ladders a packet.)

**B. Judgements** (`packet-b.json`): the 20 stored judgements of two ruler questions in unseeded draw 1 (v9, a company's amount; v13,
a theme's figure), whose window-end answers agree with the gold; 4 were given a rung at the other end of the ladder.

| | first form (`reader-brief-b.md`): reader 1 / reader 2 | second form (`reader-brief-b2.md`): reader 1 / reader 2 |
|---|---|---|
| planted wrong rungs marked UNSUPPORTED | 4 of 4 / 4 of 4 | 4 of 4 / 4 of 4 |
| the 16 stored judgements: SUPPORTED | 8 / 11 | 11 / 11 |
| INSUFFICIENT | 3 / 3 | 5 / 5 |
| UNSUPPORTED | 5 / 2 | 0 / 0 |
| the two readers give the same verdict | 17 of 20 | 20 of 20 |
| time for the 20 | 30 s / 618 s | 28 s / 1,025 s |

**The forms as they now stand were read again on the same packets.** The judgement form's third version (`reader-brief-b3.md`)
adds the rule for a move made on a step the rules do not allow. Reader 1: the 4 planted wrong rungs UNSUPPORTED; of the 16 stored
judgements, 11 SUPPORTED, 4 INSUFFICIENT and 1 UNSUPPORTED, the judgement of 2026-07-05, which is the real case the rule was added
for. Reader 2: the same on every one of the 20 (20 of 20 verdicts equal). The ladder form with its longer list of refusal cases (`reader-brief-a.md`), reader 1 again: 9 of
9 planted faults caught, no mark failed on the 9 unplanted. It named one other fault under `W` on an unplanted ladder (`u1
clean-3-2`: the Yes condition asks for NVIDIA's own confirmation, while the thesis's `settled_by` also names shipping
confirmations from others); reader 2 named none. I read it against the thesis: the fault stands, on a ladder I had written as
sound. Under Stage A's rule it would go to the third reader. 

**Third dry run ($0;** `dryrun3/`**): refusals, and the judgement form's fourth version.**
- Eight refusals on made-up theses of other companies, read with the one Stage A form (`ladder/stage-a-reader-brief.md`): one
  for each of the five refusal cases the request then had (a sixth was added after), and three that are not justified (a dated approval refused as
  uncheckable; an executive appointment, a reason outside the five; "beyond next year" claimed for a binding obligation). Both
  readers marked all eight as the key.
- The judgement form with its tests in a fixed order (`dryrun2/reader-brief-b4.md`), on the 20 stored judgements again: both
  readers marked the 4 planted wrong rungs UNSUPPORTED, and of the 16 stored judgements 11 SUPPORTED, 4 INSUFFICIENT and 1
  UNSUPPORTED, the judgement of 2026-07-05, which is a real case of the form's second test; the two readers gave the same verdict
  on all 20. The packet is one the readers' families had read under earlier forms, so this shows the final wording keeps the
  result; the baseline reading, with fresh planted cases, is its independent test.

**Fourth and fifth dry runs ($0;** `dryrun4/`, `dryrun5/`**): the form's mark L, and five-state ladders.**
- Mark L on a condition. One thesis three ways (`dryrun4/`): the Ohio wording asks for the signing, "at what amount" and "large
  enough to change NVIDIA's credit risk". With only the amount listed, both readers fail L and name the condition; with both
  listed, both hold L; with nothing listed, both fail it. Field B came back from both; they differ on whether the condition is a
  bet of its own, which is why B decides no line.
- Five-state ladders built by the request's construction (`dryrun5/`): the two fixtures and the request's merger example as it
  then stood, and two carrying a planted overlap or gap (items 2 and 4). On mark R both readers held the three built by the
  construction and failed the two planted. The other marks and named faults, as the stored answers give them:
  - reader 1 failed F on items 1 and 4 (a fine of any size is ranked above a remedy that could cost the company more), failed
    L on items 2 and 5 and named under W that their states do not tell an escalated restriction that is not a licensing rule
    from no escalation, and named on item 3 that a withdrawn filing is an outcome of its own;
  - reader 2 named on item 3 that dividing a block by whether an appeal had been lodged brings in a second event.

  What was done with them: the request's merger example now divides only by what the decision itself settles, withdrawal
  included (cleared with or without conditions; no decision with the filing withdrawn or not; blocked); the theme's states were
  widened twice and still fail (seventh and eighth readings); the ranking of fines in the company fixture was not chased
  further. These are reasons the fixtures are check fixtures and not answers claimed sound.
- **Sixth to eighth readings (`dryrun6/` to `dryrun8/`): the fixtures on every mark.** These readings chased faults in my own
  fixtures. As the stored answers give them:
  - *sixth* (one reader, nine answers): three marks failed, a reference that was a hope (XR, item 1), a condition not listed (L,
    item 2) and a comparison not listed (L, item 5), and one fault named under W (item 4: a restriction other than a licensing
    rule would sit in the same state as unchanged guidance). The four fixtures were changed;
  - *seventh* (both readers, nine answers): eight held every mark for both; the ninth, the theme's state ladder, failed L for
    one reader and Q and L for the other (narrower than its thesis's "or other escalated restriction");
  - *eighth* (both readers, two answers): the widened theme ladder failed again, on Q for one reader and on R for the other,
    who also named a fault under W (a restriction already in force could be counted as the new one); the merger example held R
    for both, and one reader failed its object and its reference field, which belong to my packet and not to the request.

  What they showed, on these examples: the form's readers find such faults, and the two
  families mostly agree on them. Three attempts did not give the thesis worded "how far will X escalate" a ladder both would pass. The fixtures are
  therefore check fixtures for the code and are not claimed sound (§5.2); the merger example inside the request, which is an
  instruction, held mark R for both readers in its current wording (eighth reading). The readers differed there on two other
  marks of my packet (the object and the reference field), which the request's example does not carry: reader 1 gave O differently
  from its own earlier reading, the mark the reference reading already showed it does not always give twice alike.
- **Ninth reading (`dryrun9/`): a quarter, a half-year and a year.** Four answers on a made-up grocer, read by both families
  with the form as it now stands: an annual figure whose question names the fourth-quarter release; a ladder for a quarter's
  figure and one for a half-year's, each asking exactly what its thesis names and sound on every other mark; and a refusal of the
  quarter's figure. Each reader held every mark on the annual figure, failed Y and nothing else on the two ladders, and held N
  on the refusal: 4 of 4 as planted, for each. On these four made-up cases the form's Y mark separates a quarterly figure from
  an annual one that names a quarter; it says nothing of how often the model writes one.
- **Eleventh reading (`dryrun11/`): the instructions the form newly names.** Thirteen answers on the made-up grocer: seven
  with one planted breach (an assertion in place of a question, Q; conditions resting on a target not yet set, R; a due-day
  basis that is not true, D; a reason that does not support the favourable end, F; a Neutral state that does not say what it is
  neutral against, once where the article states the expected outcome and once where it states none, F; a percentage on the
  wrong scale, Y) and six sound twins. As the stored answers give them (`readings_summary.md`):
  - both readers failed the planted mark on all seven;
  - reader 2 failed nothing else and held every mark on the six twins;
  - reader 1 also failed X, G and XR on the wrong-scale answer, which follow from the same error (the value 0.31, and a
    middle range that leaves out the 31% guided); it failed XR on both loyalty-scheme answers, and it was right: my packet
    left the reference's value empty though the article states "5 million sign-ups", a fault I did not plant and reader 2 did
    not see; and it failed R on the scheme's sound twin, holding that "has not reported 5,000,000" does not establish that
    the goal was missed, which reader 2 did not.

  So: seven of seven planted breaches caught by each reader, on thirteen made-up answers. Two things it also shows. A reader
  can miss a fault (reader 2, the empty value), which is why two families read and a third rules where they differ. And my
  "sound" answers are not reliably sound: readers found faults I had not planted in the first, second, fifth, sixth, seventh,
  eighth and eleventh readings.
- **Twelfth reading (`dryrun12/`): the due day of a binding obligation.** Four answers: an obligation already taken on, due at
  its next annual filing (sound) and on the day of a lenders' review that the article also states (planted); an obligation not
  yet signed, due on the day by which the signing can be checked (sound) and at the annual filing (planted). Both readers
  failed D on the two planted and nothing else, and held every mark on the two sound: 4 of 4 for each. On the second planted
  answer both also named under `W` that the year shown is 2027 while the signing is due in 2026, which follows from the planted
  day, since an event's year is taken from its due day.

### Stage A: the ladder step alone (D401: sent after a review that finds nothing serious; capped at $3; priced from tokens before the send)

- **What is sent.** The candidate of §5 only: the 34 stored theses and the 10 theses of the fresh acceptance run
  (`poc/data/clean-acceptance-2026-11-09/`), three sends each: 132 calls before resends.
- **A case, and where its files go.** A thesis id is local to its draw (`clean-1` exists in each), so a case is the pair of
  draw and thesis id, written `u1/clean-3` (the draws `u1`, `u2`, `u3`; the acceptance run `acc`): 44 cases. A send is one case in
  one of the three passes. Each pass writes `stage-a/send-<n>/outcomes.jsonl`, one row a case, keyed by the case. Readers get
  items numbered in a shuffled order; the key from item number to case and pass is kept outside any folder a reader can list.
  Every join (the three passes of a case, the two readers' rows, the third reader's rulings) is on case and pass. The test
  builds two cases with one thesis id from two draws and reads back two results.
- **The cap.** One spending limit of $3 covers all three passes and every resend (check 8). If a send would pass it the runner
  stops, the 132 are not complete, and the result reads NOT MEASURED and goes to Alex.
- **A stop is not restarted.** The Stage A folder is created once and refused if it exists, as a replay's run folder is. If the
  runner stops for any reason (a crash, the cap, a transport failure after its retries), the 132 are not complete: the result
  reads NOT MEASURED and goes to Alex with what was spent. Nothing is resumed, so no send is made twice and no balance passes
  from one process to another. A new Stage A is a new folder, on his word, under a cap he sets. Three reviews in a row found a
  new gap in the rules for resuming; this rule replaces them.
- **One stop for all workers.** Sends run from a pool. Stage A's limit is the adapter's (`budget.Budget`: the same reserve, the
  same charge, the same retries) with one addition inside the step it already takes under its lock before every send, a
  transport retry included: in that one locked step it reads the stop flag; if the flag is set it refuses the send; otherwise
  it accepts the reserve and writes the ledger's reserve line. The flag is set under the same lock, by the first refusal of the
  limit or the first error that is not an answer's own. So a send either took its reserve before the flag was set, and then it
  runs, finishes and is charged, or it never begins: no worker can read "go on" and send after the flag. The runner waits for
  every worker to return and only then reads the spend. Tests: a worker held inside its send while another is refused, then
  released (no further send begins); a worker held just before the locked step while the flag is set (it does not send); the
  same on a transport retry.
- **The spend on disk.** The limit counts in memory, and a stopped run must still report its cost. So the runner appends to
  `stage-a/spend.jsonl`, under one lock, each line one whole JSON object, written, flushed and synced: before each send of the
  transport `{"attempt": id, "reserve": dollars}`, and after it `{"attempt": id, "charge": dollars, "known": true}` from the
  response's token counts, or the reserve again with `"known": false` when the response carried none or the send failed. An
  attempt's id is the case, the pass, the request (1, or 2 for the resend) and the transport's try (1 to 3): `u1/clean-3|2|1|1`.
  With no restart, no id occurs twice. The spend reported is, over the ids, the charge where there is one and the reserve where
  there is none, in two parts: known charges, and reserves counted in full. A last line that is not whole is dropped and
  reported. Tests: two attempts writing at once (four whole lines); a reserve with no charge (counted in full, reported apart);
  a cut last line; a second start on an existing folder (refused).
- **Three sends are three samples.** Each of the three passes has its own model archive (`send-1/`, `send-2/`, `send-3/`), so an
  identical request is sent again and not answered from a stored answer; a resend after a refusal is a new request (the reasons
  are appended) in the same archive. The runner refuses to count an answer that came from the cache (`Answer.cached`), and its
  test plants one.
- **No paid control arm (D400), and what Stage A cannot say.** Versions 2 to 12 sent v74i's sentences beside the candidate. Each review
  found a new way in which two differently built answers could not be judged alike (what the control may refuse, how its words
  relate to its bounds, how its answer is checked). Without it, Stage A measures the candidate against the lines below and its own
  three sends. **It does not show that the step writes better ladders than production does, and it measures no regression against
  production:** the reference reading is of other questions and other articles and is a lead. D398 decides that the step carries
  D186; it does not decide that the result is better. AGENTS §7.3 asks that an acceptance stand beside a fresh control; Alex made
  the exception for this measurement (D400), and every report of Stage A carries this limit.
- **Exposure of the 10:** their articles accepted c8 once (D386); readers judged whether each thesis should have opened, and later
  sessions investigated them (round log §§43–46). This review read none of them: the census packet is built from the three unseeded
  draws only (`census/build_packet.py`). They are a second set, not a blind hold-out.
- **Before the send:** the whole-request audit with a blind second reader; hand-written answers through every check: the
  check fixtures of `ladder/examples.json`, one of each answer shape and a refusal, each with the input it runs on; an answer that
  each check refuses; and the dry runs' planted faults, which pass the checks. Each check's mutant; the call count and cost.
- **By code, every answer:** its outcome; for a figure, whether it has a reference figure; for a company figure, whether the old
  quarterly pattern matches its `outcome` or question (check 5); and per thesis whether its three sends agree on the object, the
  answer shape, the due day and the direction, and whether their middle ranges overlap. A thesis counts as agreeing on a point only when all three sends wrote
  a ladder and the three are the same on it.
- **By readers** (two families, each reader in its own folder, with the thesis, its article, the fiscal-year note the step was
  given and the focus line the judge is shown; a third on disputes; I read every
  disputed mark behind a fixed line myself), in one pass with one form, `ladder/stage-a-reader-brief.md`: the form of the first dry run with the due-day mark as
  corrected by the reference reading, the request's own six refusal cases and no more, mark L on every other part of the wording,
  and a field for B. The form on disk is the one used; a change to it is read again on the dry runs' packets before a send. The
  marks, copied from the form, which is their one owner (a difference between the two is a defect of this page):
  - Q: the judged question is worded as a question, not as an assertion, and asks the thing the thesis's `outcome` names.
    For a figure it also names the period the figure covers, or the day it is measured at, and the material that settles it.
    And it does not ask something other than its `focus` line (a focus that also names parts listed in `not_judged` is
    expected and is not a conflict). `n/a` for a `no_ladder`
  - O: the object is the question's own company or the right theme
  - R: exactly one rung holds for every outcome; for a yes/no, the Yes condition is the event happening and the No condition
    its complement. Every condition is concrete and can be checked on the due day: none rests on a target or a threshold
    that is not yet set
  - D: the due day follows the rule for its kind. A figure: a day by which the figure can be expected to have been
    published, after its period ends (the day the thesis or the article states, or, where neither states one, a plausible
    reporting date). An event: the date the thesis or the article gives for assessing it, or the last day of the period it
    names, or the company's fiscal year-end for a pending regulatory decision with no date. It fails when the day
    contradicts a date the thesis or the article gives, falls before the figure's period ends, or, for an event, is a date
    none of these gives And `due_day_basis` says truly where the day comes from: `stated` only when the thesis or the
    article gives that day; `period_end` only when it is the last day of the period the thesis names, or the fiscal year-end
    for a pending regulatory decision; `expected_publication` when the step set the day it expects the figure to be
    published. For a thesis whose `opens_as` is binding_obligation: an obligation already taken on is due at its next annual
    filing, and one not yet signed on the day by which the signing can be checked; another day fails
  - X: a figure: a number the `reference` carries lies in the middle rung, as the judge will read it; a reference with no
    number, or none, has nothing to place and holds, unless the ladder presents as expected something the article does not
    state. An event: the ladder presents as expected only what the article states
  - F: for a five-rung ladder about the company only: the direction is defensible (which end is bullish, or the labels of
    the states). For a figure, the reason given in `favourable_why` supports the favourable end. For five states, the
    Neutral state's condition says what it is neutral against: the expected outcome when the article states one, otherwise a
    baseline it names. `n/a` for a yes/no ladder and for a theme
  - Y: for a figure only: the year, the unit and the scale of the numbers are the question's (an amount in full; a
    percentage as 31, not 0.31), and the figure is a whole year's. A company's figure for a quarter or a half-year fails,
    whatever the thesis asks
  - G: for a figure, always one of the first three: where the article gives any figure for this quantity, `holds` when an
    analyst would accept the ranges as a fair division of the outcomes around it and `fails` when not; `not_assessable` when
    the article gives none. `n/a` only for an event's ladder and for a `no_ladder`
  - L: every other part of the thesis's wording that the question leaves out (a second figure or event, a condition, a
    comparison) is listed in `not_judged`, each with a reason that says why it is left out; a wording that asks nothing else
    holds with an empty list
  - B: exactly one entry for each part listed in `not_judged`, in its order: `"bet"` when an analyst would hold a separate
    view on it, `"not_a_bet"` when it is a detail of the judged question; `[]` when nothing is listed and for a `no_ladder`
  - XR: the `reference` field quotes what the article states the market expects. It carries the number when the article
    states one, and no number the article does not state. It is null only when the article states no expectation
  - N: for a `no_ladder` only: the refusal is justified by one of the allowed cases, and that case truly applies. A refusal
    because the question belongs to another company or to a matter no listed theme covers names that company or matter.
    Which year is this year and which next year is read from the `fiscal_year_note`
  - W: any other fault that would mislead a reader of this judged question, in a short sentence; the empty string `""` when
    there is none. The field is always present

  **G decides no line** and enters no count of sound ladders (the lines are D400's). Its share is printed as the figures on
  which it holds over the figures on which it was assessed, with the number not assessable beside it, or as "no figure
  assessable". What the reference reading shows (`readings_summary.md`, generated): each reader read the 36 production ladders
  twice, and gave the same value both times on ONE 36, O 34, R 36, X 35, F 36, Y 36 and G 30 for reader 1, and on O 36, X 35, G 33
  and 36 on the rest for reader 2. Among the marks worded alike in the two forms, G moved most for both readers. D is not
  comparable: the second form changed the due-day rule, and the values agree on 9 for reader 1 and 29 for reader 2. The
  consequence stays: a figure whose ranges a reader finds unfair can still count as right, and each reader's G is printed beside
  every count.

  **A refusal by the model is marked on N alone;** a refusal for any reason outside the six cases fails it, so an answer that
  disobeys the request cannot be counted right.

- **Three outcomes of a send** (a send is one thesis in one of the three passes), all in the denominators (44 theses × 3 sends):
  1. a ladder written: *sound and complete on the firm marks* when Q, O, R, D, X, L and XR hold and F and Y hold where they
     apply; otherwise unsound, by mark. Every fault a reader names under W, by one reader or both, goes to the third reader
     with the thesis and the article; a fault the third reader upholds makes the ladder unsound, and every W is printed in the
     report with its ruling. The name says what it leaves out: a figure can be sound and complete on the firm marks and still have ranges a
     reader finds unfair (mark G), so G's share is printed beside every count of this measure;
  2. a refusal by the model: justified (N holds, and no other fault upheld under W) or not;
  3. refused twice, by a check, by the schema or as not JSON, with the reason of each attempt.

  A send is **right** when it is a ladder sound and complete on the firm marks, or a justified refusal: declining a topic that has no main question is
  the behaviour D397 asks for, and it is not counted as a bad ladder. Outcome 3 is reported apart, by check; it is not right, and it is
  not marked by readers. A refusal because the question belongs to another company or an unlisted matter is judged by N like any
  other. Every refusal is printed in the report with its case, the reason the model gave and N's value; no share by kind of
  refusal is computed, since the reason is free text. Those naming another company or an unlisted matter are the cost of holding
  one company and a fixed list of themes.
- **Lines (Alex's, D400).** All six are fixed. They are read on each mark's value after the third reader's rulings (the
  accounting, below).
  1. No ladder fails Q.
  2. No ladder fails L.
  3. No ladder fails R.
  4. No refusal fails N.
  5. A thesis is *right* when at least two of its three sends are right, and *right by a ladder* when at least two of its three
     sends are ladders sound and complete on the firm marks. At least 35 of the 44 theses are right, and at least 28 of the 44
     are right by a ladder, so that refusals alone cannot meet the line. (Two sound ladders and one unjustified refusal: right, and
     right by a ladder. One sound ladder and two justified refusals: right, not by a ladder. One sound ladder, one unsound and one
     justified refusal: right, not by a ladder.)
  6. Two counts, each on its own population. **Direction:** among the theses whose three sends are all company figures, the
     favourable end is the same in all three for every one; the count needs at least 3 such theses. **Due day:** among the theses
     whose three sends are all written ladders, of any shape, the due day is the same in all three for at least nine in ten; the
     count needs at least 20 such theses. A count below its minimum reads NOT MEASURED. A thesis whose three ladders differ in
     shape is in the due-day count, is outside the direction count, and is reported as "shape differs across sends". This is
     where the direction problem of the reference is measured.

  A line missed stops and goes to Alex with the classes (D401).
- **The accounting, in one table.**

  | outcome of a send | who reads it | a valid row gives | where it counts |
  |---|---|---|---|
  | a ladder written | both readers | `holds` or `fails` for Q, O, R, D, X, L and XR; the same for F on a five-rung company ladder and for Y on a figure, `n/a` elsewhere; G `holds`, `fails` or `not_assessable` on a figure, `n/a` elsewhere; N `n/a`; `B` one of `bet` or `not_a_bet` for each part listed in `not_judged`; `W` a string, empty for no other fault; `why` not empty when a mark fails or `W` is not empty | lines 1 to 3; line 5; line 6, by code; the shares |
  | a refusal by the model | both readers | N `holds` or `fails`; every other mark `n/a`; `B` empty; `W` and `why` as above | line 4; line 5 |
  | refused twice (by a check, by the schema, or not JSON) | nobody: there is nothing to mark | no row | line 5, as not right; reported by reason |

  - **A mark's value** is the two readers' value where they agree. Where they differ, on any of Q, O, R, D, X, F, Y, L, XR and N,
    the third reader rules with the thesis and the article, and the ruling is the value. Every non-empty `W`, from one reader or
    both, goes to the third reader, who upholds it or not; an upheld `W` makes the send not right. G and B are not ruled on: each
    reader's value is printed.
  - **Asking again.** A reader, the third included, is asked again, up to twice, for a row or a ruling that is missing or not
    valid.
  - **NOT MEASURED, never passed.** When, after that, a written ladder or a refusal lacks a valid row from either reader, or a
    differing mark or a `W` lacks a valid ruling, lines 1 to 5 all read NOT MEASURED: a fault could sit in the answer nobody
    marked. The same when the two readers differ too often, counted once over the whole reading and not answer by answer:
    the pairs of an answer and a mark, among Q, O, R, D, X, F, Y, L, XR and N, on which the two valid rows differ, over all
    such pairs that apply, on every written ladder and every refusal. More than a third reads NOT MEASURED; four differing
    marks on one answer, among answers that otherwise agree, do not. When no answer has a reader's row at all, every send
    having been refused twice, there is nothing to divide: the share is printed as "no reading", lines 1 to 3 and 6 read NOT
    MEASURED, line 4 reads "no refusal occurred", and line 5 is read as it stands, none of the 44 being right.
  - **A line is measured only on something.** Lines 1 to 3 read NOT MEASURED when no ladder was written. Line 4 reads "no refusal
    occurred" when the model refused nothing, reported as that and not as a pass of judged refusals.
  - **My own read** of every mark the third reader ruled on behind lines 1 to 4 decides nothing (AGENTS §7.1: meaning is judged
    by a reader who did not write the change). Where I differ from a ruling, the difference is printed beside the line and goes
    to Alex with the result.
  - **The calculation is code, tested before the send on made-up rows:** a missing row for a bad answer; an `n/a` on an applicable
    mark; a row with no `W`; a `B` of the wrong length; a figure with G `n/a`; a differing mark with no ruling; a `W` upheld on
    an otherwise sound ladder; no ladder at all; no refusal at all; a twice-refused answer among sound ones; a thesis whose three
    sends are two company figures and an event; an answer returned from the cache; four differing marks on one answer among
    agreeing ones; two cases with one thesis id; every send refused twice.

  **Every instruction of the request, and what fails when the model does not follow it.** A code check refuses and resends; a
  mark is a reader's.

  | the request tells the model | a breach is caught by |
  |---|---|
  | write a question, not an assertion, that asks one figure or event, the one the topic's outcome names | Q |
  | a figure's question names its period or day and the material that settles it | Q |
  | list every other part of the wording, each with a reason | L (a blank reason: the schema) |
  | decline only in the six cases | N |
  | decline a company's quarterly or half-year figure | Y, on a ladder written for one |
  | decline a figure for a year ended, or beyond next year unless a binding obligation | check 5, on a ladder written for one |
  | decline another company's question or an unlisted matter, and name it | check 2, on a ladder written for one; N, on a refusal that does not name it |
  | do not rewrite a figure beyond next year as an event | Q: the question no longer asks what the outcome names |
  | the object is the company or a listed theme | check 2; O |
  | conditions concrete and checkable on the due day, none resting on a target not yet set; no overlap, no gap | R |
  | a yes/no event: Yes is the event, No its complement | R |
  | any other event: exactly five states, built by the construction; a company's carry the five labels once each | checks 1 and 3; R; F |
  | a company's Neutral state says what it is neutral against: the expected outcome, or the baseline compared with | F |
  | a figure: its unit, one year in the company's or the calendar form, five ranges, numbers within the limits, amounts in full and percentages as 31 not 0.31 | checks 1 and 4; Y |
  | exactly one answer shape | check 1 |
  | the reference in the item's own words; a value only when the item states the number; the middle range holds a value | check 6; XR; X |
  | the favourable end of a company's figure, with a reason that supports it | check 4 (a reason is given); F (it supports the end) |
  | the due day, and a basis that says truly where the day comes from | check 5 (the basis fits the shape); D (the day follows the rule, and the basis is true) |
  | a binding obligation is due within 548 days: one already taken on at its next annual filing, one not yet signed on the day the signing can be checked | check 5 (the 548 days); D (which day) |
  | write in English | no mark of its own: an answer in another language is named under W |

  Each row a reader's mark owns has been read with a planted breach beside a sound twin, under the form as it stood at the
  time (`readings_summary.md`): the settling material (Q), a reason that is not one (L), an unnamed company and the fiscal
  year (N) in the tenth reading; an assertion (Q), an unset target (R), a false basis (D), a reason that does not support the
  end (F), the Neutral comparison with and without a stated expectation (F) and the scale (Y) in the eleventh; the due day of a
  binding obligation (D) in the twelfth. The tenth also planted the Neutral comparison, read then under mark X; it is F's
  now, and the eleventh reads it there. These are made-up cases on one grocer: they show how both readers read the form's
  wording on these breaches and their twins, and nothing of how often the model commits them.
- **Reported beside the lines, deciding none.** One share a mark, each on its own population; an empty population is printed
  as such, never as a share. When the result reads NOT MEASURED for want of a row or a ruling, no share is printed at all.
  Each field then shows, for each reader, a count of every value the form allows for it and of the answers that reader did not
  give a valid row for: Q, O, R, D, X, F, Y, L, XR and N as `holds`, `fails`, `n/a`, not read; G as `holds`, `fails`,
  `not_assessable`, `n/a`, not read; B, over the parts listed in `not_judged` of the answers read, as `bet`, `not_a_bet`, with
  the parts of unread answers counted as not read. Example: two figures, reader 2 missing the second. G for reader 1: `holds` 1,
  `not_assessable` 1; for reader 2: `holds` 1, not read 1.

  | mark | counted on | the share |
  |---|---|---|
  | Q, O, R, D, X, L, XR | written ladders | those on which the mark's value (the accounting, above) is `holds` |
  | F | five-rung company ladders | the same; "no such ladder" when there is none |
  | Y | figures | the same; "no figure" when there is none |
  | N | refusals by the model | the same; "no refusal occurred" when there is none |
  | G | figures, for each reader apart, with no single value | `holds` over `holds` plus `fails`, with the count of `not_assessable` beside it; "no figure assessable" when that reader assessed none |
  | B | the parts listed in `not_judged`, for each reader apart | `bet` over the parts listed; "nothing listed" when there is none |

  Beside O, R, X, F and Y, which the two forms define alike, the reference reading's share for each of its two readers
  separately: the ladders on which that reader holds the mark, over the 36 less those the reader gave `n/a`. The reference's
  ladders are other questions from other articles and were not adjudicated, and the column says so. D is printed with a caveat:
  the reference's readers had the article only. Q has no counterpart, and L, XR and N do not exist for the reference; these are
  printed as "no reference".
- **Readers' budget** (estimates from the slower reader's measured 16 seconds a ladder; the faster took a twentieth): 132 answers,
  about 35 minutes a reader; the third reader, at most a third of the marks, 30 minutes; my own read of the disputed marks behind
  lines 1 to 4. The time taken is reported and stops nothing; a reader that returns no valid rows falls under the rule on
  asking again.

### Stage B: the frozen judge on the system's own ladders (after Stage A; about $0.3 a draw, an estimate)

**Stage B is an outline.** What follows records what the dry runs established and the shape the test will take. Its forms, its
lines and the rule for how many judgements must be decided before a pass means anything are reviewed, and put to Alex, before
any Stage B send; they are not part of what is asked now.

- **Run:** the candidate's first send of Stage A for each of the 34 theses, fixed before any result is read; the adapter's new
  mode; the frozen judge.
- **Readers:** every judgement (or the sample fixed below, when the total passes 400), with the request as sent, the evidence in
  force it did not show, and the sources, on the form `ladder/stage-b-reader-brief.md` (the dry run's fourth form made general: any number of judgements, and the
  evidence not shown given apart for mark E). **The standard is the judge's own rules:** the
  form quotes judging-v7 in full, so the reader and the judge use one ruler (a judgement is a forecast; an amount nobody states
  may be sized from the same programme's disclosed comparable; a reference by itself keeps the judgement at its rung). The verdict is
  about the rung only, and the form gives its tests in a fixed order, the first that decides ending the reading:
  1. the rung is not the one the answer's own implied outcome falls in: UNSUPPORTED;
  2. the answer moves rung, or is a first judgement, by a step the rules or the evidence do not allow: the reader sets the step
     aside; if what remains would not lead to this rung, UNSUPPORTED;
  3. setting such a step aside, the rules and the evidence make another rung the most likely: UNSUPPORTED;
  4. they make the chosen rung the most likely: SUPPORTED;
  5. otherwise INSUFFICIENT: reported apart, counting neither for nor against.

  The third form of the dry run held these rules without the order; the fourth states it and was read again on the dry run's
  packet (below), which holds a real case of rule 2. The baseline reading plants a case under each of rules 1 to 3 among stored
  judgements the readers have not seen.

  The verdict is read from the request as sent, which is all the judge saw. The evidence in force that the request did not show
  is given for one separate mark, E: an item not shown that would change the rung. E tests what the judge was shown (D198), not
  the judge; it is reported and enters no line.

  SUPPORTED and UNSUPPORTED judgements are the *decided* ones. Marked apart, with no line: a flaw in the reasoning that does not
  change the rung (a comparable from another programme, a figure counted twice), the arithmetic, and the two D260 fields. Planted
  wrong judgements, which the readers cannot tell apart, test the readers; a reader who misses more than one in five of them is
  replaced.
- **Readers' workload, estimated from stored runs:** the three unseeded replays made 54, 51 and 54 judgements for 6, 5 and 5 views,
  about ten a view over the 14 days. With 7 to 12 laddered theses a draw that is 70 to 120 judgements a draw, 210 to 360 in all, each
  read twice. If the total passes 400, the readers read every judgement of each thesis's first day, last day and every day its rung
  changed, and a random half of the rest drawn with a seed fixed before the run; the report then says which judgements were not read.
- **Control with a known answer:** the 16 theses, over the three draws together, that were matched to a ruler question
  (`clean-arch/unseeded-2026-11-10/mapping-runs.json`: 6, 5 and 5). A control thesis is *eligible* when a reader confirms its judged
  question, period and due day equal the ruler's, reader B's frozen gold holds an answer for that question, and the thesis has a
  judgement on or before 2026-07-14, the window end reader B's answers are for. For an eligible thesis the answer compared is its
  standing answer on that day: its last judgement on or before it, which is the frozen scorer's own rule (`score_judgement.py`: "the
  run's last judgement on or before the window end"); evidence linked after that judgement would have caused a later one. The
  frozen rule is used unchanged. It is
  compared by outcome, not by rung position: for a figure, the chosen rung's
  range overlaps reader B's range (the frozen scorer's own rule); for a yes/no, the answers match. The Ohio question's date differs,
  so it is listed apart. For each eligible thesis a reader also lists the items reader B's answer rests on (the gold's own reasons) and
  marks each as shown to the judge by that day or not, by searching the judge's requests for the figure, as the Stage 2 delivery
  audit did. A disagreement where that material was not shown is a miss of Steps 1 to 3, reported apart; line 3 counts the eligible
  theses whose material was shown. The report also says how many compared answers were made on 2026-07-14 itself and how many
  earlier.
- **Denominators, all reported, per draw and in total:** theses opened; laddered; no ladder by reason; judged at least once; never
  judged; judgements; refused judgements; judgements by reader verdict; judgements not read; control theses matched, eligible and agreeing;
  stopped or incomplete draws. A draw with
  no judgement is incomplete.
- **Baseline, read at $0 before Stage B is sent:** the same two readers and the same form (`ladder/stage-b-reader-brief.md`) read all
  159 stored judgements of the three unseeded replays, which the frozen judge made on the ruler's ladders, with planted cases under
  each UNSUPPORTED rule mixed in. A planted case missed by both readers stops the reading until the form is mended. Its shares are what the frozen judge does on ladders
  written by hand; Stage B asks whether the ladder step's ladders do worse.
- **Lines** (the margins are proposals; Alex sets them):
  1. no draw incomplete after one redo;
  2. at least nine in ten laddered theses judged at least once;
  3. of the 16 control theses in total, at least 8 eligible with reader B's material shown, else the control is unexercised and
     Stage B cannot pass; of those, all but one agree with reader B;
  4. the share of decided judgements that are UNSUPPORTED is not more than five points above the baseline's, after the third
     reader and my own read of each;
  5. among the judged theses whose last judgement in the window is decided, the share that is SUPPORTED is not more than ten
     points below the same share among the baseline's views. Theses and views whose last judgement is INSUFFICIENT are left out of
     both the numerator and the denominator and are counted beside them.

  **Budget** (estimates at the slower reader's measured 51 seconds a judgement): the baseline, 159 judgements, about 2.3 hours a
  reader; Stage B, 210 to 360 judgements, 3 to 5 hours a reader, with planted ones adding a tenth; the third reader on disputes,
  at most a third of the verdicts, up to 2 hours; my own read of every UNSUPPORTED. In all an estimate of 13 to 18 reader-hours,
  read by thesis packet in parallel. A pass that takes more than twice its estimate stops, and the result reads NOT MEASURED.

  Fewer than 30 decided judgements, a judged thesis whose last judgement has no verdict from both readers, or a line whose
  denominator is zero, reads NOT MEASURED.

  **What the comparison with the baseline can say.** The baseline's questions are the ruler's and the candidate's are the system's
  own, with another mix of yes/no, state and figure questions; the shares are reported for each shape beside the totals. A share
  no worse than the baseline's does not prove the new ladders sound: Stage A's marks, the control of line 3 and my own read of the
  UNSUPPORTED judgements are what speak to that.

  Lines 4 and 5 are computed over the judgements read; a thesis's last
  judgement is always read, whatever the sampling, so line 5 covers every judged thesis. More than a third of verdicts disputed
  between the two readers reads NOT MEASURED.

## 9. Known gaps this design does not close

- **The judge's focus line.** The judge is shown the thesis's `outcome` as its focus (§5.4). For a topic that asks more than one
  thing, that line still names the parts the question leaves out. Stage A's readers see it and judge the question against it;
  whether it pulls a judgement off the question is for Stage B's reading.
- The opening misses of the unseeded measurement (the second year of an annual quantity, the memory question, Ohio) and q12.
- The judge's refusal class (E4): counted here, fixed only by a judging version Alex opens.
- A question's shape differing between draws (Kyber, §2.1): the ladder step makes each draw's question checkable; it does not make
  draws agree.
- The second bet of a topic that holds two (D397's recorded departure from D38).
- **Five-state event ladders.** D38 and v74i give an event two rungs or five. Three hand-written five-state ladders in this review
  each had a gap or an overlap. The request now carries a construction for them, and ladders built by it passed the readers' mark R
  in the fifth dry run; whether the model applies it is what Stage A measures, with mark R on this shape reported apart. If it
  fails there, whether an event may have three or four states, or only yes/no, is a choice for Alex.
- Resuming a stopped replay; closing at the due day.

## 10. Before the build, and before the send

- **Before the build:** a fresh reviewer, each round a new one, until a round finds nothing serious (D401).
- **Build:** the ladder step with its checks, each with a test and a mutant; the fixtures of `ladder/examples.json` through the
  checks; the adapter's write of a view from a ladder record.
- **Before the send:** the whole-request audit repeated on the request and the schema as they then stand (§5.2 records two); a
  price from tokens under the $3 cap; the readers' folders and the form in place. No further word from Alex is needed for Stage A
  (D401); Stage B needs it.
