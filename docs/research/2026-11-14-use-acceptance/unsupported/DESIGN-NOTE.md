# The judge on questions that ask for an amount: what we found, the choice it raises, and why nothing is sent yet (D520, under D439), 2026-11-15, $0

## For Alex: the note

**What happens.** When a question asks for an amount ("how much credit support will NVIDIA have committed?") the judge always answers
with a band. Two things go wrong, in both systems, because they share the judge:

1. **Nothing in the news sizes the amount yet, and the judge names a band anyway.** The credit-support question opened on 2026-07-01
   with no dollar figure anywhere. For five days the judge answered "below $5 billion" in some runs and "$1 to 5 billion" in others.
   On 07-06 one partner disclosed a $4.88 billion backstop, and from that day the reviewers pass every answer.
2. **Part of the amount is sized, and the judge closes the gap with a number of its own that decides the band.** On the same question
   it scaled the $4.88 billion to the second partner at full size ($25.6 billion), then at half ($15.3 billion), then at full size
   again, then at one-fifth ($9 billion, a lower band), over eight days of one run. No statement gives any of the fractions.

**How often.** Reviewers have read 438 stored answers. 36 were settled as unsupported or as resting on too little; 31 of the 36 are
the first kind and 3 the second. These are readings of answers, many of them one question on successive days: the 31 sit on eight
question paths and three matters. At the end of the test windows, where an answer matters most: none of 16, 2 of 26 (with 3 more
left unresolved between the reviewers), 1 of 21 and 1 of 22 last answers.

**What the judge says when asked.** Given four of these answers back and asked what led to the band, it said each time that the
band rested on an assumption it had introduced and that the evidence did not give; in the two unsized cases it added that its own
instructions forbade the band it had chosen.

**The choice, which is yours.** Two cases, which need not get the same answer: (1) nothing sizes the amount; (2) an estimate uses a
step nothing supports.
- **A. Leave it.** Every question always shows a band. An unsupported answer can then stay on show; how much of that cost falls in
  a question's first days across the whole product is not measured.
- **B. Show the band with a plain label** of what it rests on ("the judge's own assumption: a one-fifth timing discount"; "nothing
  sizes this yet"). The forecast stays visible. Not shown to work: a forecast legitimately uses calculations and assumptions, so a
  label could mislead or become routine, and whether the judge can mark its own answers reliably is untested.
- **C. Show no band.** In case (1), until something sizes the amount. Doing the same in case (2) is a further choice: it hides a
  forecast an analyst might still want.

The council has no recommendation among these. None is built or tested: any of B or C needs a new version of the judge (today's
is frozen) and a decision on what the product shows. Nothing has changed in either system.

## 1. Where the finding comes from

`UNSUPPORTED-CENSUS.md` (four stored readings joined, the counts, the instructions concerned, the earlier decisions on the ground)
and `ACCOUNT-RESULT.md` (the four accounts in full, $0.0041).

## 2. Two questions, day by day (stored answers; nothing sent)

**Data-center revenue for fiscal 2027, the old system, fresh week.**

| Day | Band | The figure and where it comes from |
|---|---|---|
| 09-22 | 3 | "A precise FY2027 figure cannot be derived from the supplied evidence"; the $350 to 400 billion band "without a defensible point estimate". |
| 09-23 to 09-26 | 3 | About $393 billion: the first quarter backed out from stated figures ($89 billion and 18% growth give about $75 billion: a derivation), then the 18% carried into the third and fourth quarters (an assumption the instructions ask for: "carries the guided growth forward"). |
| 09-27 | **2** | About $401 billion: the fourth quarter raised to about $131 billion "allowing for the stated acceleration", about 25% growth. No statement gives 25%. The figure crosses $400 billion by one billion. |
| 09-28 | 2 | The same, with the 25% now also standing in the previous answer shown back. Both teams fail this answer. |

**Credit support, the old system, July window.**

| Day | Band | The figure and where it comes from |
|---|---|---|
| 07-01 to 07-05 | 3 | "Low single-digit billions", with another $3.5 billion guarantee as "a scale anchor, not a confirmed programme total". Nothing sizes the programme. |
| 07-06 | 5 | $25.6 billion: one partner's disclosed $4.88 billion scaled to the other by GPU count (the like-deal sizing the instructions ask for; reviewers pass this step elsewhere). |
| 07-07 to 07-12 | 5 | $15.3 billion: the same with a 50% "execution discount", introduced on 07-07 and repeated for five days. |
| 07-13 | 5 | $25.6 billion again: the discount dropped when the second partner's sales were described as committed. |
| 07-14 | **4** | $9 billion: a one-fifth "timing discount" after a phased deployment schedule was reported. New in this answer; both teams fail it. |

What the two tables show: the direction of each change follows real news (a disclosed backstop, an acceleration outlook, a phased
schedule); the size of each estimate is the judge's. The band moved three times: on 07-06, from the third band to the fifth, when
the $4.88 billion comparable arrived, and on 09-27 and 07-14, the two movements the reviewers dispute, each on a day a new
estimate of the judge's own was introduced. On the days an estimate was carried (one day in the first table, five in the second)
the band did not move.

## 3. Can a list of the judge's own assumptions tell a bad answer from a good one? A check on stored answers

Counted by words in the stated figure and reasons ("assume", "discount", "haircut", "allowing", "estimate", "scaled", "carry
forward", "extrapolate"; a rough count by keyword, not a reading):

| | Answers on amount questions | With such a word |
|---|---|---|
| Baseline, passed by the reviewers | 48 | 42 (87%) |
| Baseline, settled unsupported or too little | 11 | 9 |
| Stage B, passed by the reviewers | 85 | 63 (74%) |
| Stage B, settled unsupported or too little | 22 | 18 |

**Most answers the reviewers pass also use such a word.** The count takes words like "estimate" and "scaled", not whether a step is
unsupported, so it is a warning against treating every calculation as an error, not proof that a list of the judge's own steps
could not help a reader. What the reviewers fail is narrower than "an assumption was made": an answer whose band is decided by a
step nothing supports, or one where nothing sizes the amount at all.

## 4. The design, examined against the council's three stop conditions (round 10)

**The idea examined:** the judge's answer gains one required field, written before the band, that says what the band rests on.

| What must be decided or built | Finding |
|---|---|
| What the field says | A plain list of own steps may be filled on most answers (section 3). To separate the failing ones it would have to be a judgement by the judge on its own answer: "the band rests on supplied figures and steps the rules give", "the band is decided by a step of my own" (which, and what the band would be without it), or "nothing shown sizes the amount". That is a three-way classification the model makes: by AGENTS §6 it needs a closed set with examples, which grows the frozen instructions. |
| Whether the judge writes it before choosing | The answer form puts the band first (`rung`), then the reference and the stated figure, then the reasons (`judging.schema_for`). A field's place in the form does not guarantee the model reasons through it first. |
| Every reader of the answer's fields | The store (`views/store.py`, the judgements table); the next day's request, which shows back only the band and the first 800 characters of the reasons (`views/judging.py`); the judgement reference's scorer, which reads the band; the closing record (`pull.py`); the service behind the pages, which reads the reasons (`service.py`, `bundle.py`); tests that pin the form (`tests/test_stance_fields.py`, `test_frozen_questions_and_judgement.py`). A new field needs a column, a place in the next request and a place on the page, or it reaches no reader. |
| Across days | The next request does not show the previous stated figure or any field but the band and 800 characters of reasons. A label would have to be carried by code into the next request, or judged afresh each day. Whether a carried number should count as "the judge's own" once its first evidence is no longer shown is undecided. |
| Against the frozen reference | The reference answers were written with the same habits (a discount for an unshipped product, sizing from a like deal; D263). A label does not change a band, so the judgement score cannot move by it; a rule that changed bands would be a different change and is not proposed. |
| What a test would have to show for a reader | That the label agrees with the reviewers on the 36 failing answers and on a sample of the passing ones, on single answers and along a question's days; that bands on passing answers do not move beyond their own run-to-run variation. A filled field alone would prove nothing. |

**The three stop conditions:**
1. *The field cannot distinguish unsupported steps from legitimate forecasts.* Not shown either way: section 3 is a warning for a
   plain list, and a three-way classification is untested.
2. *Its reader cannot keep the label's origin across days.* Holds as the code stands: the next request shows 800 characters of
   reasons and nothing else. This is a limit of this design, not proof that no design could carry it.
3. *The behaviour needs an unresolved product choice.* Holds: A, B or C above is a choice of what the product shows.

**So, by the council's own rule, nothing is sent now** (council round 11: the decision not to send is right). What exists is the
finding, the two traces, the check of section 3 and the choice for Alex.

## 5. If Alex chooses B or C: the one test that would come first

The stored requests of the failing answers and of an equal number of passing ones, each sent as stored and with the three-way
classification added, three times each; the classification read against the reviewers' verdicts, and the bands of the passing
answers compared with their own repeats. Its size is not worked out: all 36 failing answers with as many passing ones, two
conditions and three sends each, would be 432 judge calls; a selected set would be sized and priced before it is proposed. Before
it: the changed request read whole against the instructions and the reference by a reviewer who did not write it, and its cases
fixed in advance.
