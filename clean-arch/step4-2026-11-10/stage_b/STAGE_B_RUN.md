# Stage B, the run: what is sent, written before the send (D429)

Written 2026-11-11. Alex's words (D429): build the adapter's ladder mode, and once a review finds nothing serious, send Stage
B's three draws without asking again, capped at $2. **Stage A has not passed** (D426); Stage B measures what the frozen judge
does on the ladder step's own questions as they stand, with their known faults.

## What runs

- **Code:** `stage_b/ladder_adapter.py`, the Stage 2 adapter (`e2e-2026-11-09/adapter.py`, unchanged) in its ladder mode
  (design §5.4): no seed and no ruler view; each thesis Step 1 opened gets, at its opening article and before that article's
  records, the ladder step's answer from the **fourth Stage A's first send** (`run-4/send-1/outcomes.jsonl`, fixed before any
  Stage B result exists; design §8 "the candidate's first send of Stage A"). A written ladder becomes view `v<N>` and a row of
  `clean_ladders` naming the ladder configuration as its archive records it (`clean-ladder-stage-a d3b4a5f696c7cc82`); a
  thesis with no ladder gets the row alone, and links to it are counted, not written. No ladder call is made, so the design's
  cells for a ladder call, its retry and its transport do not apply to this replay. The frozen judge
  (`judging.round_of_judgements`) judges each day's changed views, with the Stage 2 adapter's leakage and selection checks; a
  due-day guard runs at the start of every day, again after the day's writes (so a view opened already due is never judged),
  and after the last day.
- **Draws:** the three unseeded draws u1, u2 and u3 (`poc/data/clean-unseeded-2026-11-10/draw-d1`, `-d2`, `-d3` with its
  second segment), as Stage A's cases name them. Identity checked by code: the stored cases are exactly the theses each trace
  opened, with the same description, outcome and period and the same opening day, and each has exactly one first-send outcome.
- **One process, one limit:** `run_stage_b.py` replays u1, u2 and u3 one after another under one spending limit of **$2 in
  all** (D429), whose ledger is `poc/data/clean-stage-b-2026-11-11/spend.jsonl`: every judge attempt's reserve and charge are
  written under the limit's lock as they happen, and a limit starts from what its ledger already records, so a later process
  (a redo launched after this one ends) cannot pass the cap either. Each draw writes its own folder (`draw-u1`, ...), created
  once; `run.json` records every attempt as it ends. Launched detached with a log and a pid file, after a machine and network
  check.
- **Estimate** from tokens at the published rates: the unseeded replays' frozen judge cost $0.0018 to $0.0019 a judgement;
  the dry runs make 79, 80 and 77 judgements: about $0.45 in all, before retries.

## Checked before the send ($0)

- **Dry runs** of the whole send with fake judges: 9, 8 and 9 views written from a ladder (26 of 26 laddered theses), every one
  judged; 79, 80 and 77 judgements; links to a thesis with no ladder 93, 66 and 41 (counted, not written). A fake judge that
  always chooses the **last** rung, and pushes every theme shown, passes the frozen judge's own checks on all 236 requests
  (114 with five rungs, 122 with three; 159 naming a theme push): the new shapes are accepted.
- **Tests** (`test_ladder_adapter.py`, 27): the views and only those; the stored ladder field by field; one ladder row a thesis,
  naming the configuration; links follow the ladder and reach the judge; the ledger sums to the spend; a limit starts from its
  ledger; the cap stops a replay and the whole send; the due-day guard stops, before a view opened already due is judged; a
  mismatched thesis is refused; a live run writes only under its folder; the launcher resends a refused draw once and not a
  stop code decides; a second launch while one runs sends nothing; a call in flight at a crash counts at its reserve; an
  unwritable reserve sends nothing; each draw reports its own spend; a later launch after the cap stop sends nothing; a draw
  with no judgement is incomplete; a folder left by a crash is recorded and never resumed, and a crashed redo leaves the draw
  incomplete; a cap refusal stops every later send at once; a stop in the ledger survives a crash; an incomplete draw is
  written to the ledger and ends later launches; a process that dies right after a terminal stop cannot lead to a redo (the stop
  reaches the ledger before the attempt reaches `run.json`). A test fails on any credential read.
- **Mutants** (`mutants.py`, output `mutants.output.txt`): the control passes; twenty mutants each fail the test written for
  that behaviour by an assertion (each mutant's whole output kept in the scratch folder the runner is given).
- **The preflight record** (`preflight.output.txt`, run on the stored replay of draw u1's judged library and archive):
  `scripts/preflight.py` replays extraction and matching answers and schema enums, not the judge's answers. It judged 0
  extraction answers, 0 extraction checks and 0 matching records (the archive holds only judge calls: nothing skipped, none
  refused), 43 schema enum values (none missing) and 23 open views (no duplicate keys), and exits 1, "UNEXERCISED: a check
  judged no case". The judge's answers are covered instead by `judge_answer_replay.py` (`judge-answer-replay.output.txt`):
  every stored judge answer of the three unseeded replays, 159, put through the frozen judge's own check with the request it
  answered: 159 accepted, none refused; and by the last-rung dry run above for the new shapes.

## What stops the send: one rule

After four reviews in which stop paths drew findings round after round, the stops follow one rule (AGENTS §1: "propose one
structural rule"): **the first stop of any kind ends the whole send and every later launch.** A stop is the cap refusing a
request, a draw ending incomplete, or a redo left unfinished by a crash. It is written to the ledger under the limit's lock
before it is raised, so no other judge thread sends after it, and a limit built later on the same ledger starts stopped: a
later launch sends nothing. A draw's terminal stop reaches the ledger before its attempt reaches `run.json`, so a process that
dies between the two leaves the stop, never a redo.

The only second chance is the design's one redo (line 1): a draw stopped by something a second send can change (a judgement
refused twice, an answer that does not fit the schema, a transport failure after the retry policy) is replayed once more in a
new folder (`draw-u1-redo`), from the start, under the same limit. A draw stopped by a check code decides the same way every
time (a leakage or selection refusal, the due-day guard, an identity check), a draw whose redo also stops, and a draw that
returns with no judgement (design §8) end incomplete. A process that dies mid-replay leaves a folder with no recorded outcome:
a later launch records it as a crash, never resumes it, and counts it as that folder's attempt. Any incomplete draw means
Stage B misses line 1, and the line stops and goes to Alex. The cap is never raised.

## After the send

The judgements are read as the baseline's were (`BASELINE.md`, `ladder/stage-b-reader-brief.md`): each alone, by the two reader
families, with planted controls and the count; the reading plan (`STAGE_B_READING.md`), including the control theses of the
design's line 3, is reviewed before any verdict is read. The lines are Alex's (D428).
