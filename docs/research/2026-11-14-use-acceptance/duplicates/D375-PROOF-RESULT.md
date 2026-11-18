# The $0 proof of D375's per-article list: result so far (D526, D527, under D439), 2026-11-15; a passed, bounded serial proof by the condition the council set in round 19 (its limits are at the end of the last section)

Design: `D375-PROOF-DESIGN.md`, version 3 (accepted by the council for building, round 17). Scripts: `rebuild_state.py`,
`d375_lists.py`, `d375_proof.py`. No model call, no external comparison call, no package or frozen file changed; cost $0.
Nothing below says anything about what a real reading step or a real comparison would answer: every answer to a question the
stored run never asked is a labelled fake supplied by the harness.

## Stage 1: the state before the tested article is the stored run's (`rebuild_state.py`; `d375_proof.py state`)

- The production replay (serial), on a scratch copy of the stored archive with every network call refused, rebuilt the old
  system's fresh-week run from 2026-09-22 to article 174 of 2026-09-27: no failed item and no new archive row.
- Compared with the stored run on all 24 tables, every column except wall-clock times: 21 identical (among them questions and
  their keys, possible answers, statements and their sources, links, judgements, handovers, match records, groups, group members
  and other names, switches, same-claim records, the question search rows). Three differ, each checked:
  - the group search rows: the stored run's two extra rows are other names added at articles 175 and 184, after the rebuilt
    history;
  - the processing log: identical by content for articles 1 to 174; row numbers differ on the last day because the stored run
    also recorded that day's later copies; one row exists only in the rebuilt store, the refused part-day judgement;
  - the review pool: one entry only in the rebuilt store, the same refused judgement.
- So the refused part-day judgement left two records. The item's entry point reads the processing steps of its own article only.

## Lists over every article (`d375_lists.py`; cases D and E of the design, list-only parts)

- 964 article reads in four stored runs: the list the production code builds at the article's sequence minus one equals an
  independently selected set of question ids in every case and never holds a question created at or after the article. The
  independent check of groups and other names and the synthetic same-day closure were added later (below).
- The list is longer than the day-start list for 150 of the fresh week's 235 articles and for 63, 84 and 72 of 243 in the July
  runs. Five stored openings were not compared with a question the list would have added (fresh week: articles 42, 45, 103, 175;
  July run 3: article 115).

## Stage 2: case A, control arm (`d375_proof.py control`)

Article 175 through dispatch and the real entry point (`round.run`) on a copy of the rebuilt store, with the day-start list and
stored answers only (network refused; no new archive row): dispatched at sequence 175; every table identical to the stored run up
to article 175 (the three tables above accounted for the same way); the article's own processing steps identical; the second RTX
question (`v15`) opened with the stored reason, compared with the thirteen day-start questions and not with `v14`. **The harness
reproduces the stored behaviour of the default system for this article at $0.**

## Stage 3a: what the per-article list asks that the stored run never asked (`d375_proof.py discover`)

Article 175 on the per-article list, with the stored reading answer as a stand-in (through the real checks and filing: 2
statements, 1 candidate, nothing dropped) and a transport that answers nothing. The run made exactly one request that is not in
the stored archive and stopped there, recorded as a failed comparison step: the comparison request for the candidate, with the
same candidate state as the stored request, **21 questions unchanged (8 on group membership, 13 relations) and one new: the
relation to `v14`.** So the response to assemble holds 21 individually stored answers and one labelled value. What the run asks
after that answer (the collision judge, a second pass on statements) is not yet mapped.

## Stage 3b: case A on the per-article list, with labelled fake service answers (`d375_proof.py arm <name>`)

Every arm runs article 175 through dispatch and the real entry point on a copy of the rebuilt store, with the list read at the
article's sequence minus one and the stored reading answer as a stand-in (the arm "direct" uses a labelled synthetic answer). The
fake transport answered only what was planned: the changed comparison request from **21 individually stored answers plus one
labelled value** for the relation to `v14`; the second comparison (the judge of two questions on one matter) from the stored
verdict on `v6` plus one labelled verdict on `v14`; and, where the candidate is joined, labelled values for the comparisons of
its statements with the four statements already under `v14`. No unplanned request was made in any arm.

| Arm (the labelled fake values) | What the real checks and writer did | Against the control arm, tables that differ by content |
|---|---|---|
| **same** (first comparison: the same quantity or event; second: the same question; statements: different) | the candidate joined to `v14` ("merge v14"); no question created; the article's two statements linked to `v14` and `v6` | the links (to `v14` in place of `v15`), the match record, the step's note, and every row that exists only because `v15` was opened (its question, key, possible answers, switch, search row, group membership) |
| **same-repeat** (as above; statements: the same statement) | the same end state as "same" | the same |
| **veto** (first comparison: the same; second: different) | the second comparison keeps them apart: `v15` opened | the match record only (compared in full in the checked run) |
| **different** (both: different) | `v15` opened, statements filed as stored | **the match record only** (its list and reason now name `v14`) |
| **direct** (a synthetic reading answer: no candidate, the statements linked straight to `v14`) | the statements kept under `v14` by the real checks and filing; no comparison of a candidate; written | the links, the handover (another reading answer), the match record, the step's notes, `v15`'s rows, and the group's other names the candidate would have declared |

Each arm's differences are the ones the design declared before the run, with one addition found on the way and now declared: in
the arm "direct" the group's other names are absent, because only a candidate declares them.

**What this shows, and only this:** with the earlier same-day question on the list, the comparison step does compare the new
candidate with it; given answers that say "the same", the existing checks and writer join the candidate to the earlier question
and file its statements there; given answers that say "different", nothing changes but the record of the comparison. The answers
were supplied by the harness. What the real comparison would answer about these two questions is not known.

## Stage 3b: cases B and C (`rebuild_state.py` to articles 97 and 10; `d375_proof.py control|arm ... B|C`)

The states just before articles 98 and 11 were rebuilt the same way (no failed item, no new archive row; questions, statements,
links, judgements and group members identical to the stored run). For each case the control (day-start list, stored answers
only) reproduces the stored run for that article, and the per-article arm was run with labelled "different" values ready for any
question the stored run had not asked.

| Case | The per-article list gains | Requests beyond the stored archive | Result | Against its control |
|---|---|---|---|---|
| **B.** Article 98 opened the gross-margin question (`v10`); the Rubin shipping question (`v9`) had opened earlier the same day | `v9` | **none**: the stored comparison had already compared the candidate with `v9` ("different") | `v10` still opens; statements filed as stored | no table differs |
| **C.** Article 11 opened two questions at once (`v2`, `v3`); the financing question (`v1`) had opened earlier the same day | `v1` | **none**: both candidates had already been compared with `v1` | both questions still open | no table differs |

So cases B and C did not change with their stored reading answers held fixed. The five stored openings not compared with a
gained question (one of them the second RTX question) are leads from the stored runs, not a demonstration of every effect a
longer list could have. (One artefact of the control's
check, to fix in the script: its test of the group search rows flags groups created after the tested article; they are later
groups, not a difference.)

## Stage 4: four interruptions through dispatch and the bounded replay (`d375_proof.py recover`)

Article 175 on the per-article list with the fakes of arm "same", through `replay.run` bounded to the day's first fifteen items
(the first fourteen are already written and skipped by dispatch). Every run ends at the same point: the article's own steps
done, then the part-day's closing judgement refused (it is never planned). The uninterrupted run made one reading call, wrote
the article's two statements and joined the candidate to `v14`.

| Interruption | After the first run | After running again | Against the uninterrupted run, by content |
|---|---|---|---|
| 1. The reading fails before any handover is saved | the day stops ("item failed; day remains resumable"); step "extracted: failed"; no statement written | same sequence 175; one reading call; matched, written, handed over | product tables identical, no duplicate link; extra: the failed reading step and its review-pool entry |
| 2. The handover is saved and the comparison fails | step "matched: failed"; no statement written | **no reading call** (the saved handover is used); matched, written, handed over | product tables identical; extra: the failed comparison step and its review-pool entry |
| 3. An error inside the writer after its first write | one statement had been written inside the writer's savepoint; after the error **none is in the store** (rolled back); step "written: failed" | no reading call; the comparison runs again from its recorded answers; written, handed over | product tables identical; extra: the failed writing step, its review-pool entry, a second "matched" step and a second copy of the two match records |
| 4. The completed item is run again | (completed) | nothing is read, compared or written for the article | product tables identical; extra: one more refused closing judgement and its review-pool entry |

In every interrupted case the processing log also holds one more "merged" row for each of the day's two copied articles: the
replay marks a day's copies each time it routes the day. No article after 175 was routed or processed in any run (the bound).
That a failed item stops the day's later items is read from the replay loop (it raises on a failed item before taking the next)
and was not exercised with a later article in the run.

## What the proof shows, and what it does not

**Shown, at $0, on the serial path, as case-specific wiring findings for the stored fresh-week run:** the production replay rebuilds
the stored state up to the article before the tested one from stored answers, matching the stored run on every compared table
apart from the three listed differences; for the RTX article, with the list of open questions read at the article's own
sequence, the comparison step compares the new candidate with the question opened earlier the same day; **given labelled fake answers that say "the same"**, the existing checks and writer
join the candidate to that question and file its statements there, and given "different" they change nothing but the record of
the comparison; in cases B and C nothing changes; the interrupted item (with no later article in the exercised part of the day)
resumes on its own sequence, reuses its saved handover, loses a half-made write, and ends in the same product state with no
duplicate.

**Not shown:** what the real comparison or the real reading step would answer on a longer list; any benefit to a reader; the
parallel runner (an explicit limit of this proof; D375's wider acceptance still needs it).

**Built since the council's round 18 (`d375_shown.py`; it exits with an error on any breach; no breach):**
- *What is shown, not only which questions.* Over the 964 articles of the four stored runs, 9,149 listed questions (6,489 of them
  in a group): each carries exactly the groups and the groups' other names it had at the article's sequence minus one, derived
  independently from the tables with the script's own queries. Parents: no stored run holds a dependency between questions, so
  the parent list was checked only as empty; a run with dependencies is not covered.
- *Case D1, a same-day closure (synthetic).* On a copy of the rebuilt store one question (`v13`) is closed at sequence 165, after
  the day's start (160) and before the tested article (175): it stays on the day-start list, leaves the per-article list, and
  the rest of that list is unchanged.

- *A later article behind an interrupted one* (`d375_proof.py later`; exits with an error if a requirement is broken; all eight
  hold). The bounded replay takes the day's first sixteen items, so article 176 follows the tested article, whose comparison is
  made to fail once. After the failure the day stops on the failed item and article 176 is routed but not processed. Run again:
  the tested article resumes without a second reading, on the list of its first attempt, and finishes before article 176 starts;
  article 176 then completes on a list that holds the earlier RTX question and no second one, and its three statements are
  filed as in the stored run.

- *The expectations as checks that fail the script* (`d375_proof.py`; council round 18, point 2). Registered in the script before
  the checked runs: for each arm, the tables allowed to differ from its control and the end state it must reach (questions
  created, links of the article's statements, the decision on the candidate); for each interruption, the only extra records
  allowed (the failed step, its review-pool entry, the repeated comparison's two records in the mid-write case, the copies'
  marks, the refused closing judgement), exactly one write before the injected error and none after, no missing record, no
  duplicate link, and the number of reading calls on the second run. The fake answers only the named planned requests (the
  relation to `v14`, the second comparison's verdict on `v14`, the four statement comparisons under `v14`); any other new
  request fails the arm. The control's group check now looks only at groups that exist by the tested article. Rerun with the
  checks on: the three controls, the five arms of case A (the "veto" arm now compared in full: the match record only), cases B
  and C, the four interruptions and the later-article check all end with exit status 0. The "direct" arm's missing other names
  were inspected (the two names and one search row that only a candidate's declaration adds) and registered before its checked
  run; they were not declared before its first, unchecked run.
- *The checks themselves can fail.* Three mutants, each breaking one registered expectation, make the script exit with an error
  while the unmutated arm passes: the new relation removed from the plan (an unplanned request); the match record no longer
  allowed to differ; a second question wrongly expected at the end.

- *Row by row, and required* (council round 19). The arms' checks no longer allow a whole table to differ: every differing row
  must be one the tested article explains (its own sequence; or a row of the second question, or of the names its declaration
  adds, present only in the control), and the arms "different" and "veto" and cases B and C allow the article's match record
  and nothing else. A fourth mutant adds one unrelated link to a table that is allowed to differ and the arm fails ("an
  unexplained differing row"). The recovery checks now require what they had only allowed: that the interruption happened, that
  the first run stopped on the failed item, exactly one failed record of the right step and exactly one review-pool entry of
  the right kind; a completed item run again must add no step for the article. (Found on the way: the store refuses an update
  to a link; it is append-only.)

**Every check registered in the design is built, enforced by exit status, and holds; four mutants fail. By the condition the
council set in round 19 this is a passed, bounded serial proof.** Its limits stay as stated: every answer to a question the
stored run never asked is a labelled fake; the cases are those tested, on one stored run; parents between questions were
unexercised (none exists in the four runs: a synthetic parent case belongs to a real build's verification); the serial path only.

## For a build of D375, found on the way

- The frozen reading prompt and the request heading say the list is "at the start of the item's day": a build needs a new
  version of that prompt.
- The list is longer for 150 of the fresh week's 235 articles, so their stored reading answers do not apply: measuring D375 is
  a paid run.
- The comparison list is "same typed key, else text search, plus the shown list": the shown list is what brings a same-day
  question with another typed key into the comparison.
