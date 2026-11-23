# A $0 deterministic proof of D375's per-article list of open questions: design, version 3 (D524 to D526, under D439), 2026-11-15

D375 (Alex, 2026-11-05): before each item the reading step reads the questions committed before that item's dispatch sequence,
including questions opened earlier the same day; implementation and acceptance pending; the default still reads the day-start
list. This proof asks what building it would change on the stored fresh-week run of the old system, with no model call, no external
comparison call and no change to any package or frozen file.

**What a pass may be said to show, and nothing more:** given the stated fake service answers, the per-article list passes the
existing checks and the writer writes the expected records, on the serial path. It does not show what the real reading step or
the real comparison would answer, that a reader benefits, or that D375 is ready for acceptance. The parallel runner is not
exercised: D375's recovery acceptance on it stays open.

Version 1 was reviewed by the council (round 16) and not built; each of its six points is answered in the section named. Version 2 was reviewed (round 17): five points answered, the recovery comparison corrected in section 4 of this version.

## 1. Done at $0 so far

- **The state before the tested article is rebuilt by the production replay** from stored answers alone, network refused
  (`rebuild_state.py`): to article 174 of 2026-09-27, no failed item, no new archive row; questions, statements, links, judgements
  and switches identical to the stored run up to that sequence. Not yet shown, and required before any case runs (point 5):
  the same for question keys, groups, their other names, group members, dependencies, handovers, match records and processing
  steps, table by table and column by column; and the records the refused part-day judgement leaves in the scratch store listed
  and shown not to be read by the entry point under test.
- **Lists over every article of four stored runs** (`d375_lists.py`, 964 article reads): the list the production code builds at the
  article's sequence minus one equals an independently selected set of question ids (created before the article, open at that
  sequence, of the article's subjects or a theme) in every case, and never holds a question created at or after the article. To be
  corrected (point 4): the invariant "contains the day-start list" is dropped (a question may close during the day; none did in
  these runs, so a synthetic closure is added below); the independent derivation is extended from ids to each question's groups,
  other names and parents as of that sequence.
- **What the list would touch, by count:** it is longer than the day-start list for 150 of the fresh week's 235 articles, and for
  63, 84 and 72 of 243 in the three July runs. Five stored openings were not compared with a question the list would have added
  (fresh week: articles 42, 45, 103, 175; July run 3: article 115). A lead, not read: of the week's 278 statements dropped for
  want of a question, 134 came from the 150 articles whose list would be longer.

## 2. What is real, what is changed, what is synthetic (points 1 and 3)

- **Real:** dispatch, the replay loop (serial), the item's entry point (`round.run`), the list builder, the comparison list, the
  comparison engine's handling of answers with its typed-key and conflict checks, the collision judge's result handling, the
  checks and the writer; on copies of the rebuilt store.
- **Changed in the harness only:** the sequence the list is read at (`store.day_start_seq` answered with the article's sequence
  minus one for the tested item).
- **Synthetic, and labelled as such in every output:**
  1. *The reading answer on a changed list.* Two stand-ins, run as separate arms: (a) the stored answer of the article, through
     the real checks and filing on the new list; (b) a labelled synthetic answer in which the statements are linked directly to
     the earlier question and no candidate is proposed. Neither exercises the real changed reading request or its archive key.
     The control arm (day-start list) stays on the normal reading path and the archive, so a broken entry point is caught.
  2. *The external comparison.* Adding a question changes the whole comparison request, so its stored response is not a cache hit
     and no changed request is described as stored. The fake transport assembles a response for the changed request from the
     individually stored answers to the unchanged relation questions (each verified against its stored request) plus a labelled
     value for each new relation. The collision judge's request, when its peer list changes, gets its own explicit fake; so does
     every second-pass comparison of statements a changed outcome newly requires. Any request not planned in the case's table
     is refused, and a refusal fails the case.

## 3. Cases, predictions and allowed differences (points 1, 3, 6)

For each arm the product state after the item is compared with its reference table by table; the differences allowed are listed
before the run, and any other difference fails the arm.

| Case | Arm | Reference | Must show | Allowed differences |
|---|---|---|---|---|
| A. RTX, article 175 | control: day-start list, stored answers only | the stored run after article 175 | identical state: `v15` opened, compared with the thirteen day-start questions | none |
| | per-article list, stored reading answer, fake "same" for `v14` | the control | `v14` on the comparison list; the candidate joined to `v14` by the real checks and writer | no `v15` and nothing keyed to it; the candidate's statements linked to `v14`; the match record (list, decision, reason); group membership of `v15` absent |
| | per-article list, stored reading answer, fake "different" for `v14` | the control | `v15` opened | the match record's list and reason (now naming `v14`); nothing else |
| | per-article list, synthetic direct-link answer | the control | the statements kept under `v14` by the real checks and filing; no candidate; no comparison request for a candidate | no `v15`; the links; the handover; the match record |
| B. A truly distinct earlier same-day question: article 98 (`v10` opened; `v9` earlier the same day) | per-article list, stored answer, fake "different" for each new relation | a control run of article 98 from stored answers | `v10` opens; statements filed as stored | the match record's list and reason |
| C. A same-article pair: article 11 (`v2`, `v3`) | per-article list, stored answer | its control | both questions open | the match record's list and reason, if the list gains `v1` for a candidate |
| D1. An earlier same-day closure (synthetic: a question closed in the scratch store between the day's start and the article) | lists only | independent derivation | the closed question is absent from the per-article list though present at the day's start | not applicable |

## 4. Interruption and resume, through dispatch and the replay loop (point 2; revised after the council's round 17)

On copies of the rebuilt store, article 175 is processed through `replay.run` with the per-article list and the fake services of
arm "same". **The comparison point is the same for every run:** the replay is bounded to the first fifteen items of 2026-09-27
(articles 161 to 175; the first fourteen are already written and are skipped by dispatch), and the state is read when article
175's own steps have ended, before the part-day's closing judgement (which is refused, as in the rebuild, and whose records are
set aside on both sides). The uninterrupted run is taken at that same point.

Four interruptions, each followed by a second bounded run to completion:
1. the reading fails before any handover is saved (the stand-in reader raises);
2. the handover is committed and the comparison fails (the fake comparison raises once);
3. **a real mid-write failure:** an error raised inside `writing.write` after at least one of its writes, within its savepoint; the
   check first shows that the write made before the error is gone (the savepoint rolled back), then resumes;
4. the item completed; the bounded replay is run again.

**What must match the uninterrupted run:** the questions, statements, links, the handover used and the decisions, with no product
record written twice; the item keeps its sequence number; where a handover was saved it is the one used (no second reading); in
interruptions 1 to 3 no later article was processed before the item finished; the list the resumed call builds is the list of the
first attempt.

**What is expected to differ, and is checked by content and order rather than for equality:** the failed step's processing record
and its review-pool entry (`round._fail`), a repeated matching attempt's records where the comparison ran twice, generated row
numbers, and wall-clock times. Each interruption's expected records are listed in the harness before it runs; a record outside
that list fails the case.

## 5. Findings a real build would need, noted on the way (not part of the proof)

- The frozen reading prompt and the request's heading say the list is "at the start of the item's day": a build changes that
  wording, which is a new version of a frozen prompt.
- A longer list changes the reading request of most articles after the day's first opening (150 of 235 in the fresh week), so
  stored reading answers do not apply: measuring D375 is a paid run, decided separately.

## 6. Stop

The proof stops and reports if: the rebuilt store is not shown identical on every table the entry point reads; the control arm
does not reproduce the stored state; an arm shows a difference outside its allowed list; a resume case leaves a duplicate or a
different final state; an unplanned request is made; or any step needs a package or frozen file changed.

## 7. Outputs

`d375_proof.py` with its per-arm tables of differences, the scratch stores outside the repository, a result page. Cost $0.
