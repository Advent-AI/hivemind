# The three-arm probe: what it reports and what it can decide, written before the send

Written 2026-11-10, before any answer exists, and rewritten after the council's read (`council/jh-codex.md`), still before any
answer exists. An exploration: first answers only, with no resend; three draws a cell; the three arms sent in one run, in
alternating order. 96 sends, about ten cents; cap $0.20. Nothing here is a registered test, and no result here passes or
fails a line of Stage A or shows a change to be safe.

## Why

The small send of the reference change (D411) filled the new field as written beforehand. Read by hand it also showed two
things it was not aimed at: three company figures all called "higher is good", and two of four events with a worse ruling out
than the same theses in the second run. One draw cannot tell chance from the change, and the stored sends are hours older.
The model's own account on six stored sends (`../stage_a/result-2/direction-accounts.json`) says in each that neither the
topic nor the item says which end is good for the company. The question told the model that another send chose the other end,
so the account locates a candidate cause and proves none.

## Arms

| arm | request |
|---|---|
| old | as the second Stage A sent it. Checked at no cost: its request has the stored request's identity for all 12 theses (`probe.py check`), and all 204 stored answers of the second run follow its schema's order of keys at every level, with a reversed schema told apart |
| reference | the working request, with the reference's kind and range (D411) |
| unclear | the working request with a third value for a company figure's favourable end: the test for higher and lower is left word for word; `unclear` is for a topic and an item that argue both ends or say nothing on it, and its sentence names the two readings or says there are none; one sentence in the closing check; the schema's enum and one description. The sentence "A result and its direction are separate: capital spending can build capacity or hurt returns" is cut, since `unclear` is its case. An option to show Alex, not a rule: it would amend D186 |

Theses for the direction (three arms): u3/clean-8, u1/clean-7, u2/clean-6, u1/clean-1, acc/clean-3, acc/clean-1, acc/clean-7,
acc/clean-5. Theses for the events (old and reference): u1/clean-3, u1/clean-12, u2/clean-3, u1/clean-11.

## What is reported, answer by answer

- Every one of the 96 cells is listed. An answer that is missing, cannot be read or does not fit its schema is "not
  complete" and is never left out of a count silently.
- Direction theses: for each thesis and arm, the three first answers as higher, lower, unclear, a theme's figure, an event,
  or declined with the reason.
- Every answer of the old and reference arms through the working code checks (an old answer's reference given the kind
  `expected` and no upper end, so that the same checks read both): the reasons listed, so that a change in quotations,
  references, ranges, due days or declines is seen.
- Events: the 24 answers shuffled and read by me without the arm's name, each against the event rules of the readers' form:
  no ruling out where one is possible; a wait written as a ruling out; a decision made before the article's day counted; the
  question's period differing from the answer's; the object. Faults listed answer by answer, then the arms' names restored.
- The direction's key: two readers, one of each family, judge from the topic and the article alone, before any answer exists,
  whether the texts settle the end (`direction-key/brief.md`). Where the two differ the thesis is "disputed" and is shown
  under both readings.

## What it can decide

| question | a signal | no signal at three draws (not "safe") |
|---|---|---|
| S1. Did the reference change move a direction? | a thesis where the old arm gives one end in 3 of 3 and the reference arm the other in 2 or 3 of 3 | no such thesis: the small send's u3/clean-8 is not reproduced |
| S2. Did the reference change move the events? | a thesis where the old arm's three answers are without a fault and the reference arm's have one in 2 or 3 of 3; or faults in the reference arm exceed the old arm's by 3 or more over the 12 | neither |
| S3. Does `unclear` do what the option claims? | shown to work at a high level only if, on every thesis the key calls not settled, the arm gives `unclear` in 3 of 3, and on every thesis the key calls settled, that end in 3 of 3; anything else is reported thesis by thesis as a wrongly removed direction, a wrongly given direction or a decline | |

A signal in S1 or S2 holds the reference change back from any measurement until a larger comparison of the same hour on the
thesis that showed it. No signal means the change is carried with the risk named. S3 is evidence for Alex's choice and
changes nothing in the build without his word.
