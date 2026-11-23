# Stage B, the baseline reading: what is read, counted and decided, written before any reader's row (D426)

Written 2026-11-10; revised after each of six reviews (`council/kf-codex.md` to `kk-codex.md`: not ready), before any reader of the 159. Alex's
word (D426) opens the preparation of Stage B on the ladder step as it ran in the fourth Stage A, **which has not passed its
lines**. This page fixes the first test of that preparation: the $0 reading the design names (§8, "Baseline"). No model call
of the pipeline is sent; nothing here is a Stage B send, which needs his word again. The design's lines 4 and 5, which will
use these shares, are proposals he has not set.

**What it answers.** How often does the frozen judge, on ladders written by hand for the ruler's questions, give an answer
its own rules and the evidence it was shown do not support? One picture: on 2026-07-08 the judge moved "Will China authorise
H200 imports by January 31, 2027?" from No to Yes on a report that officials told three companies they would be permitted to
buy. A reader says whether that move follows the judge's rules on what it was shown.

## What is read

- **The judgements:** all 159 the frozen judge made in the three unseeded replays (54, 51 and 54; 16 questions: 10 yes/no,
  6 figures), unaltered (`stored_judgements.py`). Each is given with `request_as_sent`, which is the user message of the call
  whose answer was accepted (the system message is the judge's rules, which the form quotes in full; the schema is not
  shown); the stored answer; and `not_shown`: the evidence linked to the question at or before the judgement's sequence
  number, not replaced by then, that the request did not list (production's own `evidence_shown_in`), each with the piece it
  revises when it revises one.
- **The form:** `ladder/stage-b-reader-brief.md`, unchanged: the dry runs' fourth form.
- **Packets** (`build_baseline.py reading`): **every judgement is read alone.** A packet is a shuffled handful of
  judgements, no two of the same question: 40 packets of 4 or 5 judgements, 85 to 126 thousand characters each. Nothing in
  a packet's shape sets a control apart, and every judgement is read under the same conditions: from its own request, which
  carries the previous conclusion (the form already rules that the verdict comes from the request alone). The design
  describes Stage B's reading by thesis packet. **Whether Stage B is read in this shape is a design choice for Alex**, put
  to him with this result and Stage B's lines: read otherwise, the two readings differ in more than their ladders.
- **Controls, nine:**

  | control | stored judgement | what is changed | the form's test it falls under |
  |---|---|---|---|
  | planted 1 | 2027 capex, draw 3, 7th | the rung: 5 shown as 3, marked as a change; the text left as stored | 1: the rung is not where its own implied outcome falls |
  | planted 2 | Rubin ships in 2026, draw 3, 8th | the rung: Yes shown as No, marked as a change; the text left as stored | 1 |
  | planted 3 | 2026 capex, draw 2, 7th | a move to rung 5 by adding Google's $190 billion capital-expenditure guidance to the four companies' $650 billion plan | 2: a step the evidence does not allow (Alphabet is one of the four; the guidance is total capital expenditure) |
  | planted 4 | 2027 capex, draw 1, 6th | a move to rung 3 by a $150 billion deferral "Microsoft and Meta have said" | 2: a statement not in the evidence |
  | planted 5 | Rubin ships in 2026, draw 2, 9th | the answer stays at No because no shipment "is established"; the request's previous-conclusion line is rewritten to No to match | 3: the stated plan (in full production, shipping this fall, first shipments in the third quarter) makes Yes the most likely |
  | planted 6 | 2026 capex, draw 2, 9th | the answer stays at rung 1, the four companies' $650 billion plan "held about 20% lower" as unconfirmed; the previous-conclusion line rewritten to match | 3: a stated plan in the middle of rung 3, and nothing in the evidence that puts a number on a cut |
  | repeats 1 to 3 | H200, draw 1, 4th; custom silicon, draw 2, 6th; Kyber, draw 3, 3rd | nothing | read twice by each family, in two packets |

  The planted answers are written in `build_baseline.py`. Planted 1 and 2 are meant to be conspicuous: an answer whose rung
  contradicts its own text is what test 1 is. A planted answer is caught when the verdict is UNSUPPORTED; the count also
  prints whether the rung the reader names is the stored one.
- **The planted answers are tried before the reading** (`build_baseline.py validation`): the six, among six stored
  judgements of other questions, in two packets read once by a fresh session of each family. Two reviews found planted
  answers a careful reader could call INSUFFICIENT; a planted answer is used in the reading only if both families call it
  UNSUPPORTED here and name the stored rung (`plant_trial.py` writes `planted-in-use.json`, which the builder and the count
  both read). One that is not is dropped, and the result says how many were used and the packets as built. The design asks
  a planted case under each of the three tests: if the trial leaves a test without one, the reading does not start; a new
  planted answer for that test is written and tried. The trial is a minimum screen: it does not show that a planted answer
  is beyond dispute, that the reading's own sessions will catch it, that the readers catch subtle errors, or that they do
  not fail sound answers.
  **The trial's result (2026-11-11, `plant_trial.py`):** all six pass; each family calls each UNSUPPORTED and names the
  stored rung. On the six stored judgements beside them the two families also agree (five SUPPORTED, one INSUFFICIENT).
- **Readers:** two families (Codex, Claude), one fresh read-only session a packet, told to open only the form and the
  packet: 80 first readings. **The second family is Claude Opus 5.5 (`claude-opus-5-5`) for all 40 packets** (changed
  2026-11-11, before any verdict of the reading was looked at): the Fable sessions reached the account's usage limit after
  6 of 40 packets; those six files are kept in `fable-partial-not-counted/` and are not counted, so that one family is one
  model. The trial of the planted answers was read by Fable for this family; the trial establishes the controls, and the
  reading itself tests whether the Opus sessions catch them (the count's stop and void conditions). A session that has not returned after 60 minutes is stopped and run once more; a packet that
  fails twice is unread, and the reading is then incomplete. Every session started is logged with its time and whether it
  returned (`sessions.json`): the first family's by its runner script, the second's from the harness's completion notice.
  The log is the operator's record; the count checks it is whole, not that it is true.
- **Where the two verdicts on a judgement differ**, a control's included, so that the third readers' packets tell them
  nothing: two third readers, one of each family, with the form, the judgement and both verdicts and reasons under shuffled
  sides (`ladder/stage-b-third-reader-brief.md`). I read every stored judgement any reader, first or third, calls UNSUPPORTED, beside its
  request; that read is written down (`own-read.jsonl`) before the count will print a result, so it is made without the
  shares in view.
- **Mine, not the design's:** the design says "the third reader"; two, one a family, is Stage A's practice, since a reader
  rules with its own family more often than not. The three repeats, the three ways of counting an unresolved verdict, the
  trial of the planted answers, reading every judgement alone and the five-hour limit are also this plan's; none replaces a
  required reading.

## What is counted (`baseline_count.py`, written before any row; exercised on made-up rows)

A judgement's verdict is the one both first readers give; where they differ, the one both third readers give; else it is
unresolved. SUPPORTED and UNSUPPORTED are the decided verdicts; INSUFFICIENT is reported apart. Both shares are given three
ways: unresolved left out, counted SUPPORTED, counted UNSUPPORTED.

- by draw, by shape (yes/no, figure) and in all: judgements by verdict, and **the share of decided judgements that are
  UNSUPPORTED**;
- of the 16 questions, by the last judgement of each (2026-07-14 in all 16): **the share that is SUPPORTED among those
  decided**;
- with no line: a flaw that does not change the rung, the arithmetic, the two fields, and E (an item not shown that would
  change the rung);
- the controls: each family's catches of the six planted; each family's two verdicts on the three repeats.

## What stops it or voids it

The count prints a result only when the reading is complete and none of these holds; otherwise it names the condition and
prints no share. It takes nothing on trust that it can rebuild: it makes the whole reading again (every packet file and
the key) from the stored runs and the trial's result, and requires the files in the readers' folder to be those files, text
for text and no other, and the key to be that key. `check_count.py` runs it on twenty-five made-up readings built by the
real builder: three sound, the first's two shares checked against expected values, and twenty-two that must be refused,
each for its reason (`check_count.output.txt`).

**A correction made after the first readings were in (2026-11-11), before any count:** the count had required every
UNSUPPORTED to name another rung. Seven rows of 336 (five judgements, all figure questions, both families) name none, each
following the form's second test: the answer moved by a step the rules do not allow, and what remains leads to no rung.
The form asks for "the rung the rules and the evidence lead to", of which there is none. The check was stricter than the
form and refused rows that follow it; it now accepts no rung where the reader marks a flaw that changes the rung (the
second test), and refuses it otherwise. No verdict changes; the shares do not read this field.

- **Incomplete:** the record is not this reading's (a packet file differs from the one the builder makes, or is one the
  reading does not have; the key is not the builder's key; the planted answers in use leave one of the three tests without
  one); an answer file that does not hold exactly its packet's judgements; a judgement without a valid row from a family (a
  verdict; for UNSUPPORTED, a rung of the ladder other than the answer's, or none where the form's second test decides,
  marked by a flaw that changes the rung; a flaw that changes the rung only with
  UNSUPPORTED; E naming only items not shown; a reason, in words, wherever the form asks one); a differing verdict without
  both third readers' rulings, each with its reason; a packet whose logged sessions do not end in one that returned (a
  packet stopped twice is unread), a session logged as returned after more than 60 minutes, or no sound log; and my own
  read missing for any stored judgement a reader, first or third, calls UNSUPPORTED (`own-read.jsonl`, a verdict and its
  reason each).
- **Stopped:** a planted answer both families call other than UNSUPPORTED. The design's instruction is that the reading
  stops until the form is mended, and that is what is done: the reading stops and its rows are not used. I read the miss
  beside its request and the council reads it too. If we find the form at fault, it is mended and the reading starts again
  from the beginning. If we find the planted answer at fault and not the form, the design gives no instruction for that: it
  goes to Alex with the miss, and nothing starts again on my word.
- **Not measured:** a family that misses more than one in five of the planted answers in use (two or more of six); more
  than a third of the 159 verdicts differing between the two families; fewer than 30 decided judgements; no question with a
  decided last judgement; a family whose first readings took in all more than five hours of session time. Five hours is
  this plan's reading of the design's "more than twice its estimate": the design gives 51 seconds a judgement and about 2.3
  hours a reader for the 159; with the nine controls that is 2.4 hours, taken as 2.5.

**How often the controls would void a sound reading** (a calculation, the readers taken as independent): if a reader catches
a planted answer nine times in ten, a family misses two or more of six in 11% of readings and some planted answer is missed
by both in 6%; at nineteen in twenty, 3% and 1.5%. So a void or a stop is diagnosed before it is taken as the readers'
failure.

## What it cannot show

- Anything about the ladder step's ladders: they are not in this reading, and Stage A has not passed.
- The 159 judgements are of 16 questions, about ten days each: a question's daily answers repeat one another, so the first
  share is closer to 16 cases than to 159. The second share has 16 at most. Another mix of questions moves either share
  without the judge being better or worse.
- The planted answers are plain errors; catching them does not show the readers catch subtle ones, or that they do not fail
  sound forecasts: there is no control known to be sound, since a stored answer's soundness is what is being read. Three repeats are a small check. Both families can share a mistake, and the third readers see the first
  readers' reasons.

## Cost

No model call of the pipeline. Reader sessions only; the design's estimate of about 2.3 hours a reader for the 159 comes
from 51 seconds a judgement in a dry run and is not a measured budget for these packets.
