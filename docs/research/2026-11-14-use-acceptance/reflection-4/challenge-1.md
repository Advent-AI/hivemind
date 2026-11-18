# Reflection council, round 2: five cold reads and my own are in. Attack the synthesis; then one answer to each of Alex's three questions, one recommendation, one test.

You wrote the measuring-method audit (`codex-measurement.md`). You may now open `docs/research/2026-11-14-use-acceptance/reflection-4/`.
Still read-only. Everything below is a lead: check it in the files before agreeing.

## 1. What is on the table (all in `reflection-4/`)

- `own-reflection.md`: mine, written before any report was opened.
- `codex-design.md`, `codex-history.md` (its author says it is incomplete), your `codex-measurement.md`.
- `claude-measurement.md` and `claude-history.md`: two cold reads by the other family, the same briefs as yours. The history one
  read every index row from D229 to D559 and the three round logs.

## 2. Where all six agree

1. **The goal:** a research record an analyst can rely on: a short list of big questions kept over time, each with a present
   answer supported by the facts that bear on it, and the reason visible. No single quantified production goal exists; four
   goals stand in the record at once (PRD 10 §1; "beats the old system", D427; the six lines for answer choices, D400; "an
   analyst can use it", D484, lines proposed).
2. **The measuring is a large part of why the work is stuck**, and real product defects exist whatever the stick.
3. **The conditions measured are not the product's** (preset questions, or an empty start; one company; one fortnight; no
   library carried).

## 3. What I verified first-hand from the two Claude reports, and add (attack each)

1. **The answer-choice gate has no control that clears it.** `clean-arch/step4-2026-11-10/stage_a/result/RESULT.md` l.55–60: one
   reader family holds every firm mark on 47 of 111 answer-choice lists, the other on 84; and "of the 36 ladders production
   wrote for other questions, two readers held every firm mark on 19 and on 25". `DESIGN.md` l.1056: "sound ladders given a
   failed mark | 3 of 7 | 0 of 7". Seven readings, no pass. And the record of D400 shows the six lines were my proposal
   ("通过线我提议：四条硬线一个都不能有 …"), which Alex accepted as the recommended option, with no chance estimate; I have since
   treated them as his fixed lines.
2. **The end-to-end stick cannot rank.** Seven gradable questions; new 2, 1, 0 against old 1, 1, 1, "the new system's own spread
   (0 to 2) is wider than the gap" (`comparison/COMPARISON-SIZING.md` l.23); the same first-step draws score 5, 3, 4 or 1, 2, 1
   by how the wording is matched; the judge was "written to the frozen gold's own reasoning" (D263) and the key is one model
   reader's answers.
3. **After the first step was accepted (c8, 2026-11-09): fifteen candidates, none adopted** (history report §2), seven gate
   readings, none passed, about twenty measuring instruments in eighteen days, most used once.
4. **What moved the judged result, every time, was what the judge is given, never wording** (history report §3): questions
   present at the start (6.33 of 7 against 4.0; 18, 18, 17 against 6, 5, 5); the company's starting figures (53 against 45 of
   57, three draws the same hours; adopted then removed by Alex, D370); delivered facts (18, 18, 17 against 17, 15, 16 with
   seeds; D361's 9 of 9). About a hundred wording versions left it at 15 to 17 of 17 to 19.
5. **Facts kept and not delivered are the oldest recurring defect** (eight times from 11-01 to 11-15, history report §4), and
   in the new system's fresh week "kept with no question: no judgement reads them: 389" of 569 statements
   (`week/WEEK-RESULT.md` l.20–24), while later linking "judged 516 earlier statements and linked 2" (LEAN-LOG l.155). Never
   tried: letting the step that answers a question look up the kept facts itself when it answers. I find no decision that
   refused it (D198 bounds what a judgement reads among linked evidence; D505 to D511 paused the delivery line on one
   inconclusive six-call test).
6. **Nobody, Alex included, has looked at the new system's library as the product shows it.** The stored July run's judged
   library is in the old system's storage format (`poc/data/clean-e2e-full-2026-11-13/c1/judge/draw-c1/views.sqlite`: 9 questions,
   69 judgements, 545 statements), which the existing page server takes as an argument (`scripts/hivemind_api.py --views`).
   The side-by-side left for him on 11-14 is a 98 KB page (`side-by-side/SIDE-BY-SIDE-WEEK.md`); he has not answered it.

## 4. The answers I propose to give Alex (attack the wording and the substance)

**The goal.** For a company, a short list of big questions kept over time, each with a present answer supported by the facts
that bear on it, in a library that already exists when the news arrives, so that an analyst opening a question sees why the
answer is what it is. "Ready" should mean: Alex opens the library after several weeks of news and finds most questions worth
holding and most answers following from what is shown, with nothing important missing, in numbers he sets after seeing it
once. The record instead carried four goals and I steered by the narrowest.

**Is it the measuring method?** For the last five days, largely yes; not only. The door I put first has no control that
clears it; the end-to-end stick cannot rank; the conditions were not the product's; the judges are two model families that
do not agree. Real whatever the stick: facts kept and not delivered; questions formed differently from run to run; answers
and ranges sized from nothing.

**Why stuck, and the way through.** Each next step was chosen from the last failure of a stick with no known error, by
changing sentences in one call. Three changes, in this order:
1. **The ruler becomes Alex's own marks on a short deck of cards** drawn from the product's output (question, answer choices,
   present answer, the three strongest cited passages; a "no question" card where a matter is missing). Repeats and
   same-system pairs give its error; the two model families mark the same deck first, so their agreement with him is
   measured; the deck accumulates. The gate ladder (D548) stops being what is steered by; the six lines stay on the record
   as not met and become a diagnostic until some control clears them (his decision).
2. **The condition becomes the product's:** a library kept across weeks (D559's small comparison, then a continuous run).
3. **Product work aims at what the answer step is given, not at wording:** first the delivery of kept facts (the answer step
   looks them up itself), sized on the deck before anything is built.

**One recommendation, one test.** Recommendation: change the ruler first (item 1); nothing else can be accepted or refused
soundly before it. The one test, at $0, before asking him anything further: Deck 1, about 24 cards from the stored July runs
(both systems, mixed and unlabelled; six repeats and same-system pairs among them; a few declined or missing matters),
marked first by the two model families apart, then by Alex in about half an hour: would I hold this question as worded; does
the answer follow from what is shown; is something important missing or wrong. It yields his usable share per system on
this deck, the readers' agreement with him, and the largest class of what he rejects. **It fails as a ruler** if his own
repeats disagree with each other as often as the model families do, or if he cannot mark a card without opening the
sources. It cannot show a rate for other news, nor which step caused a bad card.

## 5. Questions

(a) Is "largely the measuring, not only" supported, or does the record support a stronger or weaker statement? Name the
    strongest evidence against it.
(b) Item 3.4 ("what the judge is given, never wording"): a fair reading, or selection? Counterexamples from the record.
(c) Is demoting the gate ladder mine to recommend, given D400's lines are Alex's by his acceptance? What exactly should go to
    him as his decision, in one sentence?
(d) The owner-marked deck: the minimum design that makes it a sound instrument and still fits half an hour; what you would
    cut from mine; the main way it can mislead.
(e) Order: ruler first, then condition, then delivery. Would you put D559's small comparison (ready, about $0.5) before the
    deck, beside it, or after? Why?
(f) Anything in the five reports that contradicts this synthesis and that I have passed over.
End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
