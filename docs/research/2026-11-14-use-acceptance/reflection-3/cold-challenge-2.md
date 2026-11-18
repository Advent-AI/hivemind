# Core-problem council, round 3: the blind review of the three July runs is done. Attack my reading; then one statement, one recommendation, one test.

You remain read-only. Everything below is a lead: verify it in the files before agreeing. Folder:
`docs/research/2026-11-14-use-acceptance/reflection-3/`.

## 1. What was run (your agreed step; $0 on the ledgers; reader sessions' cost unknown)

- `july-topics-packet.json`: the 40 topics of the three stored July runs (same 14 days, each from empty), runs shown as X, Y, Z,
  each topic with its three attempts at a judged question (question, whose, due day, answer choices, or the refusal).
- Task S (`brief-same-question.md`), two families apart (`codex-same-question.jsonl`, `claude-same-question.jsonl`): group by
  matter; for matters two or three runs opened, same / one apart / different, what differs, whether it changes the answer;
  per topic answerable and worth tracking.
- Task K (`brief-stated-or-chosen.md`), two families apart, who saw only the topics as first written, not the judged questions
  (`*-stated-or-chosen.jsonl`), and the same task on the 20 topics of the two later weeks (`*-stated-or-chosen-later-weeks.jsonl`).
- `own-read-before-the-readers.md` and `PREDICTIONS.md` were written before any answer was opened. Tallies:
  `tally_review.py` → `tally-output.txt`, and `tally-extra.txt`.

## 2. Results (regressions to my own claims first)

1. **My narrower cause is not shown.** I predicted the split "the news states the yardstick → same question; someone must choose
   it → different". Blind sorting does not reproduce it: both families call only 7 of 40 July topics "stated" (24 chosen, 9
   split) and 1 of 20 in the later weeks (15 chosen, 4 split). Only one shared matter is "stated" by both (P1 undecidable by my
   own rule: fewer than three). The French inquiry and the supply commitments, the same question in all three runs, were
   sorted "chosen" (a default deadline). P2: of the 9 twice-declined July topics 6 chosen, 3 split, 0 stated (I had said at
   least 8 chosen). P3: 2 chosen, 1 split, 0 stated. Nothing refuted, nothing established: with "chosen" this common the sort
   cannot discriminate. What the sort does say: in about 8 of 60 topics the news itself fixes what to measure and by when; in
   the rest the writer picks.
2. **A correction to my reflection:** the cloud companies' 2026 spending is the same judged question in all three runs (I had
   read the first step's three wordings as three questions).
3. **Task S, both families.** They grouped the 40 topics into the same 18 matters. 6 matters were opened by one run of three
   only. Of the 12 opened by two or three runs: the same question by both families 3 (2026 capital spending, the French
   inquiry, supply commitments); not the same by both 8 (federal AI spending, China's H200, the Intel stake, the China
   domestic-share survey, memory prices, credit support, the H100 rental price, Kyber); disputed 1 (Vera Rubin: one run's
   first attempt adds "revenue-generating"). On the 8, the difference changes the answer: Codex 8 of 8, Claude 7 of 8.
   What differs on the 8 (matters naming it, Codex / Claude): no judged question 5 / 5; what is measured 3 / 3; period or
   deadline 3 / 3; several parts 1 / 3; whose question 1 / 2; answer choices 1 / 1.
4. **Per topic, both families.** Worth tracking: yes 30 of 40, split 10, "no" by both 0. Answerable as written: of the 31 topics
   with a judged question, yes 12, unsure 10, no 2, split 7; the 9 twice-declined have none. Of the 9 declined, 6 are worth
   tracking by both.
5. **Your falsifier** ("mostly substantively equivalent, answerable questions, with consequential differences confined to
   multi-part topics") is not met: 3 of 12 the same; the differences sit in deadline, what is measured and no-question as
   much as in several parts.

## 3. What I then found in the record (read `docs/DECISIONS.md` rows D458, D466, D468, D469, D473, D475, D479, D481 and the log's D466)

- D466 (2026-11-13, Alex's requested reflection) already ended here: "Two choices go to Alex: whether the product is measured
  with a research library that really existed before the window … or from an empty library; and, question by question,
  whether the three shapes the standard leaves open (programme against total; the deadline after a reported slip; whether
  memory must open) are product targets or recorded concerns". D468: "forward work waits on Alex's two D466 choices".
  D469: "Provisional (Alex not answering, D439): empty-start measurement; the three open shapes stay concerns".
  I find no later decision recording his answer. Everything since (the use-acceptance trial, the fresh week, the week of
  10-06, the four readings of the first gate) ran on that provisional choice.
- Three of today's eight not-the-same matters are exactly those three shapes: credit support (programme against total, and
  its date), Kyber (the deadline after a reported slip: 2027 in one run, 2028 in two), memory prices. Two more are D397's
  multi-part case ("no judged question … until splitting is built"): the Intel stake, federal spending. Two are refusals by
  written rule on matters both families call worth tracking: the H100 rental price (no listed theme; D477 "no H100 theme or
  ladder change") and the domestic-share survey (a rolling twelve months). The eighth is China's H200 (permission against
  recorded revenue).
- Every attempt since 11-13 to settle the shape by a rule edit failed and was not adopted: c17 (period sentence, D473), c18
  (unsigned deals, D475), c19 (outcomes written at opening, D479), production's price rule (D481). D458: of 71 lost
  question-draws, 27 are cases the standard does not settle, 14 breaches, 19 unresolved, 11 reasonable alternatives.
- PRD 10 (`docs/prd/10-filing-phase.md` line 67) lists "Opening questions" as "Another class of problem, not in this phase";
  with the key's questions given, the clean path agreed on 6.33 of 7, opening its own 4.0 (D466).

## 4. The statement I now put to you (attack each clause)

**The core problem:** the system is being measured on inventing its research questions from an empty notebook, and what such
a question must look like (what is measured, by when, which part, whose) is not settled for most matters in real news. The
choice of what to follow is mostly sound (30 of 40 worth tracking by both families, none agreed unworthy); the shape is not
(3 of 12 shared matters the same; 12 of 31 judged questions answerable by both). Each run fills the gap its own way, and the
later steps (answer choices, the first gate, the final judgement on self-opened questions) inherit it.

**Why the loop cannot close it:** the missing piece is a product rule (the standard's open shapes, D397's unbuilt splitting,
which matters outside the listed themes get a question, whether the test starts from empty at all). By AGENTS a rule about
what to keep or open needs Alex's words; the council chose provisionally (D469) and four wording fixes failed. Two more days
of step-level work under that provisional choice returned to the same two choices.

**What I am not claiming:** a rate; that a real prior library would fix it (untested); that variance between runs is itself
the product's harm (the product keeps one library; the harm is a question that cannot be settled or differs from what an
analyst would hold, shown by the answerable counts and by 4.0 against 6.33); that the readers' "answerable" is calibrated
(two model families, no source check).

## 5. What I ask of you

1. Is the statement in §4 supported by the files? Name every clause that is weaker than written, and the strongest reading
   of the record against it (for example: is it really one problem, or two: no-question refusals and differing shapes?).
2. Is "the loop cannot close it without Alex" true, or an evasion? Name anything the council may legitimately decide and
   test under D439 that would change the picture, with its falsifier; or say there is none.
3. One recommendation and one test for Alex (AGENTS §7.3), given he is reachable now. My candidate: ask him D466's two
   choices again, this time as concrete cards rather than as abstractions: the eight matters, each with the two or three
   questions the runs asked, and "which one would you hold, or none"; plus the one framing choice (the product's test starts
   from a real prior library of questions, with self-opened questions reported as proposals; or from empty, in which case his
   rulings on the cards become the shape rule in a new version he opens). No paid send before his answer. Attack it: is this
   one recommendation or a menu; what would you put instead; what is the one test after his answer.
4. The one sentence you would say to him first.

End with the line `CONSENSUS: yes` or `CONSENSUS: no, because …`.
