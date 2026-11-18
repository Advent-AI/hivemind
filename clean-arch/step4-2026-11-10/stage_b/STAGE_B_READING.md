# Stage B, the reading: what is read, counted and decided (D428, D429, D430); written before the send

Written 2026-11-11, before Stage B is sent and before any of its verdicts exist. It carries the baseline's reading over
(`BASELINE.md`, reviewed seven times) and adds what Stage B needs: Alex's lines (D428) and the design's control theses (§8,
line 3). **Stage A has not passed** (D426), and every report of Stage B says so. Reviewed before any verdict is read.

## What is read, as in the baseline

- **The judgements:** every judgement the frozen judge makes in Stage B's three draws (about 236 in the dry runs), each with
  the request as sent, the stored answer and the evidence linked by then that the request did not list; read each alone in
  shuffled packets with no two judgements of one question, by the same form (`ladder/stage-b-reader-brief.md`).
- **Readers:** Codex and Claude Opus 5.5, one fresh read-only session a packet, as in the baseline (Opus is the baseline's
  second family as counted); two third readers on every differing verdict; my own read of every stored judgement any reader
  calls UNSUPPORTED, written before the count.
- **Controls:** six planted answers, two under each of the form's three tests, written on Stage B's own judgements (the review
  of 2026-11-12, `council/kv-codex.md`, found the baseline's six identifiable: two had two-rung events where every Stage B event
  has three, and all six had questions no Stage B judgement has). Each takes a stored judgement and changes its answer: test 1,
  the rung moved away from the answer's own implied outcome (u2 v2 #10, u1 v4 #6); test 2, the rung moved by a step the rules
  or the evidence do not allow (Google's total capital expenditure added to the four companies' data-centre plan, u2 v4 #7; a
  cancellation of commitments the evidence does not hold, u1 v7 #6); test 3, an answer that stays, its previous conclusion
  rewritten to match (rendered as the judge renders it: the previous reasons' first 800 characters), at a rung the rules do not
  lead to ("not established" used as a reason to stay, u3 v3 #9; the four companies' own 2026 plan cut 15% with no evidence for
  the cut, against the rules' "a consensus or guidance figure by itself keeps the judgement at the reference's rung", u2 v4 #3).
  The second review (`council/kw-codex.md`) found the first version's test-1 plants shared one generic `why_changed` sentence
  and judged the 2027 projection plant open to a good-faith INSUFFICIENT; both were rewritten. As in the baseline, a trial comes
  first: two packets (the six among six stored judgements) read by one reader of each family; only a planted answer both call
  UNSUPPORTED with the stored rung named is used, and the reading starts only when the answers in use cover all three tests
  (`stage_b_trial.py` writes `planted-in-use.json`; the count derives it again and refuses a file that differs). Three repeats
  of Stage B judgements, drawn with seed 20261112.
- **The trial decides which planted answers are clear (a rule, written after three reviews raised the same point).** Each
  review judged one or two planted answers open to another verdict in good faith (`council/kv-codex.md`, `kw-codex.md`,
  `kx-codex.md`). Whether readers agree that a planted answer is wrong, and on which rung, is what the trial measures: a
  planted answer both families call UNSUPPORTED with the stored rung named is used; one either family reads otherwise is not
  used and is reported. A review checks that each planted error is real and that its form does not give it away; it does not
  decide in advance how readers will read it. If a test is left with no planted answer, only that test's planted answers are
  rewritten and tried again, and the reading waits (the baseline's rule, `BASELINE.md`). The reading builder enforces the wait: it
  derives the trial's result itself and builds no reading packet until the trial passes. The trial is a minimum screen: two
  families agreeing selects a useful control; it does not show that every careful reader must agree or that the stored rung is
  the only defensible one (`council/ky-codex.md`; the baseline states the same limit).
- **One draw a packet.** The three draws word one matter differently (u1's, u2's and u3's Vera Rubin questions are three
  texts), so the baseline's rule "no two judgements of one question in a packet", read on exact text, would let two versions
  of one matter share a packet (`council/kx-codex.md`). Each reading packet holds one draw's judgements, at most one of each
  view; the trial's two packets are set by hand with no two of one matter (2026 and 2027 capital expenditure, two quantities,
  share the second). A planted answer missed by both families stops the reading (the design's
  instruction); a family missing more than one in five, more than a third of verdicts differing, fewer than 30 decided
  judgements, or a family's sessions over twice the estimate, read NOT MEASURED.
- **The count:** the baseline's `baseline_count.py`, generalised to Stage B's population and lines, with the same refusals of an
  incomplete record (every packet rebuilt and compared, every row's contract, session logs, third rulings, my own read).

## The lines (D428, in Alex's words: "数字题和是非题分开比")

Each line is computed on the same three readings as the baseline's shares (unresolved left out; counted SUPPORTED; counted
UNSUPPORTED) and compared reading for reading with the baseline.

| line | passes when | the baseline it compares with |
|---|---|---|
| 1 | no draw incomplete after one redo (design §8) | — |
| 2 | at least nine in ten laddered theses judged at least once (design §8); 26 laddered in the first send, so at least 24 | — |
| 3 | the control theses (below) | reader B's frozen answers |
| figure | decided figure-question judgements UNSUPPORTED at most 5 points above the baseline's | 4/52 (7.7%), 4/53 (7.5%), 5/53 (9.4%) |
| yes/no | decided yes/no judgements UNSUPPORTED at most 5% | 0/99 |
| last | of the judged theses whose last judgement in the window is decided, at most one in ten UNSUPPORTED (Alex's "3 in 30", scaled); INSUFFICIENT last judgements reported beside | 16 of 16 SUPPORTED |

What a judgement counts as a figure or a yes/no is its view's shape: a ladder with numeric bounds is a figure; an event (two or
three rungs, no bounds) is a yes/no. In the first send, 12 of the 26 laddered theses are figures and 14 are events
(11 event for a company, 3 event for a theme, 6 figure for a company, 6 figure for a theme); the share of judgements of each shape is reported
beside the lines.

## Line 3: the control theses

The 16 theses of the three draws that the frozen matching rule paired with a ruler question (`unseeded-2026-11-10/
mapping-runs.json`): q07 (three), q08 (three), q09 (two), q13 (two), q18 (three), q04, q16 and q23. All 16 have a ladder in the
first send.

1. **Eligible** when (a) a reader confirms the judged question asks what the ruler's question asks, for the same period;
   (b) for an event, the deadline is the ruler's; (c) reader B's frozen gold holds an answer for it; (d) the view has a
   judgement on or before 2026-07-14. Two readers (one of each family) on each, a third on a difference.
   **The due day of a figure (D430, Alex: "指同一份年报就算相同").** A figure's due day counts as the ruler's when both mark
   the publication of the same period's figure (the ladder step sets a year's figure's due day by code, D414, where the ruler
   gives another day for the same annual report: q09 2027-04-01 against 2027-02-28; q04 and q13 likewise). An event's
   deadline must be the ruler's. The literal reading (every due day equal) is counted beside. Three controls fail either way:
   the two Kyber theses written for "during calendar 2027" with a due day at the end of 2028, and the Ohio thesis due
   2027-12-31 against the ruler's 2027-06-30.
2. **The answer compared** is the view's last judgement on or before 2026-07-14 (the frozen scorer's rule), by outcome: for a
   figure, the chosen rung's band overlaps reader B's range; for an event, Yes against reader B's yes, and "Ruled out" or
   "Still open" against no (both mean the event has not happened by the deadline).
3. **Material shown:** for each eligible thesis, two readers mark each of reader B's decisive items (the gold's own
   `decisive_items`, read in the frozen packet) as shown or not shown to the judge by 2026-07-14, searching every evidence entry
   of every judge request for the view on or before that day (the design: "by searching the judge's requests for the figure").
   An item confirmed not shown decides that the material was not shown, whatever another item's mark; a set with no item
   confirmed missing and one unresolved (the third readers split) is unresolved. A disagreement with reader B where the
   material was not shown is reported apart as not shown to the judge by that day, without naming the step that lost it: the
   item is then traced (linked to the thesis and not shown, or never linked) before any step is named. "Shown by that day"
   searches every request through 2026-07-14, so an item shown on an earlier day may be absent from the last request whose
   answer is compared; the report says so beside line 3.
4. **Line 3 passes** when at least 8 eligible theses have reader B's material shown, and all but one of those agree with
   reader B. Fewer than 8: the control is unexercised and Stage B cannot pass (the design's words). The Ohio question (q23,
   u1/clean-2) is listed apart, as the design says, and is in neither count. The literal reading's eligible, shown and agreeing
   counts and its line are printed beside, as are how many compared answers were made on 2026-07-14 and how many earlier.

## What it cannot show

That the ladder step's ladders are sound (Stage A has not passed; their known faults are in them); that the readers catch
subtle errors (no control is known to be sound); anything about the system's other steps. Three draws of 26 laddered theses:
the lines' chance behaviour is in `result/line-chance.txt`.

## The tools (written after the run ended, before any of its verdicts was read; revised after the review of 2026-11-12)

- `build_stage_b.py validation|reading`: `validation` writes the two trial packets (`validation/`) and their key outside the
  readers' folder; `reading`, after the trial, writes the packets (`readers/`): every Stage B judgement alone, no two of one
  question in a packet, the planted answers in use, the three repeats, reusing `build_baseline.py`. The number of packets is the
  larger of the most judgements one question has and the total length over 110,000 characters, per draw (the first build, on the
  question rule alone and across draws, gave 14 packets of 17 or 18 judgements, 345 to 405 thousand characters, set aside
  unread).
- `stage_b_trial.py`: the trial's result. It rebuilds the trial packets and key and requires them equal, requires each answer
  file to hold each judgement of its packet once, every row with every field of the form, a rung that is null or a rung of the
  ladder, a reason that is text, and the form's contract; a session record (`sessions-trial.json`) of one returned fresh
  session a packet and family; and the answers in use to cover all three tests; only then does it write
  `planted-in-use.json`. The reading builder runs the same derivation and refuses to build before it passes.
- `stage_b_count.py`: the count. It derives the trial's result again and refuses a `planted-in-use.json` that differs; rebuilds
  the packets and key from the run folders and requires them equal, every stored judgement once, the three repeats and all
  three tests; then the baseline count's refusals (every row's contract, now with every field of the form present; session
  logs; third rulings; my own read of every UNSUPPORTED) and its reports (each planted answer's two verdicts and whether the
  stored rung was named; each repeat's verdicts as a stored judgement and as a control; hours; families' differences; verdicts
  by draw and shape; each question's last judgement). It reads NOT MEASURED, printing no share, when a family misses more than
  one in five planted answers, a family's sessions exceed twice 51 seconds a judgement, the families differ on more than a
  third, fewer than 30 judgements are decided, or any line's denominator is zero (figure, yes/no, last judgements, laddered
  theses); STOPPED when both families miss a planted answer. Then D428's lines on the three readings.
- `control_theses.py packets|count` and `control-reader-brief.md`: line 3. `packets` writes four packets of four controls (the
  ruler question, the judged question and its rungs, reader B's decisive items from the frozen packet, and every evidence entry
  the judge was shown for the view in its requests on or before 2026-07-14; no rung chosen and no reader B answer; 140 to 195
  thousand characters) and the code's facts outside the readers' folder; it refuses a decisive item the frozen packet lacks.
  Two readers, one of each family, answer `same_question`, `same_due` (D430) and a mark for each decisive item by id; a third
  reader of each family answers each disputed point afresh, without the first readers' answers. `count` rebuilds the facts and
  packets and requires them equal, requires every answer file to hold each control of its packet once with every field in its
  closed set, and a ruling with a written reason from both third readers on every disagreement and none elsewhere; a point the
  third readers split on is unresolved, and a control with an unresolved point is not counted as shown or eligible.
- `check_stage_b_count.py` (21 made-up readings: twelve of the count, trial and builder, nine of the controls) and
  `count_mutants.py` (thirteen mutants, each caught, two by a crash whose traceback was read; `count_mutants.output.txt`). In an earlier mutant printout I saw the code's comparison with
  reader B for three controls (u3/clean-3, u3/clean-5, u3/clean-6); no reader's verdict exists yet.

## What the review of 2026-11-12 said a pass cannot show (added)

The judgements of one question repeat it day after day, so 236 judgements are not 236 independent tests; the planted answers are
plain errors and do not show that the readers catch subtle ones or accept sound ones; 0 of 16 last judgements UNSUPPORTED in
the baseline does not show a zero rate.
