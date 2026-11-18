# The ladder step wired end to end, and the diagnostic same-day run it enables (D447): design version 4, 2026-11-13

Version 1 was reviewed (`council/mn-codex.md`: five serious findings) and version 2 (`mn-codex-2.md`: six implementation and
decision-rule gaps); each is answered below. **Structural rule adopted for what remains** (AGENTS §1: one mechanism drawing findings round
after round; the council-loop skill's recorded trap of reviewing imagined behaviour): the contract (what the run decides, the limits, the
stop and redo rules, Stage B's conditions, the run states) is settled in this prose; integration details (where a check sits in a loop,
a type test, a patched attribute) are settled in code and its $0 tests, which the next review reads instead of prose. **Purpose:** run the clean path end to end on fresh articles (Step 1 c8 → frozen Steps 2–3 → the ladder step as it ran in the
fourth Stage A → the frozen judge) and, the same day, production v118, as a diagnostic under D442; never D427's acceptance while Step 4's
lines are unmet. Nothing frozen changes: the ruler, Steps 2–3 (D427), the ladder step's configuration (D426), the judge. "Same day" means
the model sends of both systems on one calendar day; the article window (v108's 243 items, 2026-07-01..07-14) is a fixed input.

## A. The wiring: every input and authorization that must follow a fresh run

| piece | change (defaults keep every stored run reproducible) |
|---|---|
| `unseeded-2026-11-10/run_unseeded_draw.sh` | an output root and a limits file as arguments; the Step 1 and Step 2 calls go through the budgeted runners of §B |
| `stage_a/build_cases.py` | a fresh-input path: given draw traces (a segmented trace as `a+b`), writes the opened theses as cases to a named file; checks every case is draw-qualified and unique, has its opening article, and that the set equals the theses the trace opened (count from the trace, not a constant); the default path still writes the 44 and still requires 44 |
| `stage_a/stage_a.py` | `--cases-file` (default `cases.json`) |
| `stage_b/ladder_adapter.py` | `replay(...)` takes the draw's trace and Step 2 folder, the ladder outcomes file, the ladder archive (the configuration checksum is read from its `model_calls`), the cases file, and the authorized output root; the module constants stay as defaults; the live-output check authorizes the given root |
| `stage_b/run_stage_b.py` | the draws, the root and the cap as arguments; its stop and redo rules unchanged |

## B. One enforced shared ceiling over every paid call

One `SharedLedger` (`budget_replay.py`: locked reads, atomic writes, settle at usage, overrun flag) for the slice, all six draws, every
retry and every paid reader call (reader sessions here are not API calls and cost nothing on this ledger). **Each entry point reserves
per actual attempt, keeping its component's own retry and stop behaviour:**

| entry point | how it is intercepted (no frozen file edited) | reservation per attempt | settles at |
|---|---|---|---|
| Step 1 (`clean-arch/step1/live.py`, `LiveTransport`) | an optional `ledger` argument on `LiveTransport` itself (the runner tests the exact type): with it, each attempt reserves on the ledger and settles at usage, the cumulative-dollar check skipped; the adaptation, model check, output-cap check, time and call limits and `max_attempts=1` unchanged; without it, as now | (2 × request bytes + 4,096) input tokens and the whole output cap at `model.PRICES` | the response's usage; no usage: the reservation |
| embeddings (`hivemind.search.openai_embeddings`, called by `step2/run_forward.py`) | the budgeted Step 2 runner replaces the module attribute before calling `run_forward.main`; the replacement reserves, then calls the original | three attempts (the helper retries inside) × (2 × request bytes + 4,096) tokens at the embedding rate | three times the reported total tokens; zero or missing: the reservation |
| Jev (Step 2 and production) | as `budget_replay.py` (`jev.transport` patched in Step 2's runner; the transport argument in production) | three attempts × the input bound | three times the reported input; zero or missing: the reservation |
| the ladder step (`stage_a.py`, `StageALimit.send_labelled`) | inside each attempt of its loop, in the locked step that reads the stop flag and takes the local reserve | (2 × bytes + 4,096) and the output cap | usage; else the reservation |
| the judge (`ladder_adapter.LedgerBudget.send`, which overrides `Budget.send`) | inside each attempt of `LedgerBudget.send`'s own loop, the same way | the same | the same |
| production (`budget_replay.py`) | as built | as built | as built |

**A refused reservation stops the whole run:** it raises a stop that each runner treats as its own first stop (Step 1 and Step 2 end the
draw; Stage A's limit stops every worker; Stage B's runner records the stop first; production's replay raises), and the launcher starts
nothing after it. A crash between a send and its charge leaves the reservation counted (conservative). The ceiling holds under the
stated input and output bounds; a charge above its reservation sets the overrun flag and stops every later send, but cannot undo the
charge. **Limits:** recorded spend under D439 so far $7.11, leaving $32.89; this run's total limit **$15.00**, the slice's sub-limit
**$1.50**; estimate about $9 (clean Step 1 about $2 a draw, Steps 2–3 about $0.15, ladder three passes about $0.12, judge about $0.15,
production about $0.45; embeddings to be measured on the slice).

### B2. Settled after version 2's review, against the code read

- **Step 1:** `clean-arch/step1/runner.py` tests `type(transport) is LiveTransport` (lines 221–370), so no subclass: `LiveTransport` gains
  an optional `ledger` argument; when it is given, the per-attempt dollar check reserves on the ledger and settles at usage, and the
  cumulative `reserved` check is skipped; without it, the transport behaves exactly as now (a test compares both).
- **The ladder step and the judge:** the reservation and settlement sit inside each attempt of the existing loops
  (`stage_a.py` `StageALimit.send_labelled`, lines 64–88; `ladder_adapter.py` `LedgerBudget.send`, which overrides `Budget.send`), in the same locked step that reads the stop flag and takes the local reserve, so each attempt is charged once
  on each ledger and the local limit keeps its own stop.
- **The shared stop and the slice's sub-limit:** the ledger persists `stopped` and its reason under its lock; a refused reservation sets it,
  and every later reservation in any process is refused. The slice runs on its own ledger (ceiling $1.50). **The handoff:** the full run's ledger is created only after
  every slice process has ended, with ceiling $15.00 minus the slice ledger's final spent and minus anything it still holds reserved
  (a reservation never settled stays counted), so the two together never pass $15.00; the full run's ledger is created only by a
  separate council decision after the slice is read, and a slice ledger found stopped authorizes nothing by itself.
- **Jev:** the budgeted Step 2 runner captures the original `jev.transport` before replacing it, and the wrapper calls the captured
  original (no recursion); production keeps passing the transport as an argument.
- **The interception trap:** the wrapper sets a per-thread token for the attempt it reserved; the trapped `urlopen` fails unless the
  calling thread holds a live token, so an unreserved call on another thread is caught.

### B3. Values and their readers; the new path and the old checks (AGENTS §2)

| value written | readers |
|---|---|
| ledger state (spent, reserved, stopped, reason) | every budgeted entry point (reserve, settle), the launcher (start nothing after a stop), the report |
| fresh cases file | `stage_a.py`, the adapter (cases must equal the opened theses) |
| ladder outcomes (pass 1–3) and archives | the adapter (pass 1, checksum from the archive), Stage A's readers (all passes) |
| Stage B views databases | the census reader (`prod_records`-style outcome by the scorer's rule), Stage B's readers |

| existing check on the old path | the fresh path |
|---|---|
| c8 pinned (`test_runner.py -k adopted_c8`), frozen unseeded files' sha256 | kept in the launcher |
| Step 1 runner's format and contract rules, archive identity | unchanged (same `LiveTransport` type) |
| Step 2's own refusals and later-link counts | run and reported per fresh draw |
| Stage A's per-pass archives, its stop rule | unchanged; the case file is the only new input |
| the adapter's due-day guard, leakage and selection checks, links to unjudged theses | unchanged; the inputs are arguments |
| Stage B's redo and stop rules | unchanged |

## C. The $0 proof (all before the slice)

1. **Requests, byte for byte:** for a sample of stored states, the budgeted Step 1 transport, the ladder limit and the judge limit send
   exactly the requests the existing path sends (key order and Step 1's adaptation included); a fake service records them.
2. **Outcomes by case and pass:** the parametrized adapter, with the defaults and with the stored inputs passed explicitly, fed the
   stored judge answers from the archive, rebuilds Stage B's three views databases (every view, rung, link, judgement row and count,
   ordered by key); `stage_a.py` with the stored archives rebuilds run 4's outcomes by case and pass; `build_cases.py` rebuilds
   `cases.json` byte for byte and, on a stored draw passed as fresh input, the same cases for that draw.
3. **Mutants:** a wrong trace, wrong cases, wrong ladder file, wrong ladder archive and a wrong output root are each detected; a mutant
   that bypasses the ledger is caught.
4. **Interception is complete:** with `urllib.request.urlopen` replaced by a function that fails the test when called without a live
   ledger reservation, a fake end-to-end run of one stored day through every component sends every attempt through the ledger.
5. **The ledger under stress:** concurrent sends, retries inside a component, missing usage, an overrun, a held reservation after a
   crash, and a refusal that stops every component.

## D. Run states (persisted in `<root>/run.json`, written before each action; a launcher that crashes resumes from it)

Each component attempt is `started`, `completed`, `stopped` (with its reason) or `crashed` (a signal exit, an interrupted launcher, a
launcher found dead, or an attempt found `started` at a later launch). **Changed by D449 (council mo):** the one redo of Step 1, Step 2 and
production is a relaunch with `--redo` and a required `--redo-reason`, made only when the component's output shows a stop a second send
can change (a model answer refused by its check twice, an answer that does not fit the schema, a transport failure after the component's
own retries); otherwise the run stops. The ladder step and the judge have no outer redo (the judge keeps its own inside `run_stage_b.py`).
**What stops the entire run:** a budget refusal (the ledger's persisted stop), a crash (D449), a stop after the one redo or of a component
with none, missing or mismatched cases, a due-day guard stop, a configuration that is not the frozen one, an overrun flag. A launcher that
finds the ledger stopped starts nothing. A launcher is alive while it holds its lock, registered on the ledger; the stop gate stops the
ledger before any send when a registered lock is free (`run_fresh.py`, `budget_replay.install_stop_gate`).

| component | success | a check refuses | transport failure | budget refusal | crash |
|---|---|---|---|---|---|
| Step 1 draw | stamped | the runner's rules per item | the runner's format rule, then the draw stops: one reasoned redo (D449) | the run stops | recorded; the run stops (D449) |
| Step 2 draw | stamped | reported | the helper's retries, then the draw stops: one reasoned redo (D449) | the run stops | recorded; the run stops (D449) |
| ladder pass | outcomes per case | `refused twice` (Stage A) | Stage A's rule: the run stops | the run stops | the pass recorded incomplete; the run stops (D449) |
| judge draw | judged | one new-folder redo inside `run_stage_b` (Stage B), then the run stops | the same | the run stops | recorded, never resumed; the run stops (D449) |
| production draw | totals | its own | the draw stops: one reasoned redo from empty (D449) | the run stops | recorded; the run stops (D449) |

## E. What the run can decide

- **The census, same day:** all 23 ruler questions per draw, the seven graded apart; matching by MATCHING-v2 (two blind families, a third
  reader), eligibility by Stage B's brief (both counts of unresolved), the loss trace. It describes the sample and locates failures; it
  cannot establish that either system is better, nor D427's acceptance.
- **Stage A's lines on fresh theses:** potentially measurable if the readings and denominators are complete, by Stage A's reading
  procedure (independent readers on every answer of the three passes, disputes to third readers); otherwise reported not measured.
- **Stage B's six conditions** (D428, `stage_b/STAGE_B_RESULT.md`): every draw completed; at least nine in ten laddered theses judged;
  at least eight eligible controls with the material shown, all but one agreeing; decided figure-question judgements UNSUPPORTED at most
  five points above the corresponding baseline reading; yes/no judgements UNSUPPORTED at most 5% (absolute); last judgements at most three
  UNSUPPORTED in 30, scaled to the number judged, INSUFFICIENT reported beside. Each under the three treatments of unresolved verdicts the
  recorded result used (left out; counted SUPPORTED; counted UNSUPPORTED). Stage B's reading rules apply, with D429's every-judgement requirement: every judgement read separately by both families (no
  sampling), at least 30 decided judgements, nonzero denominators, at most a third disputed, the planted controls screened by the trial; a condition whose rule fails is reported not measured.
- **Step 2's checks** run on each fresh draw and are reported (refusals, pending links, unresolved Step 1 links); those the fresh run does
  not exercise are named.

## F. Readings

The census readings as before; Stage A's (historically about 35 minutes a reader for 132 answers, plus disputes); Stage B's (historically
13–18 reader-hours for 210–360 judgements). They run as Codex and Claude sessions (not API calls). If a reading cannot be completed, the
lines it serves are reported not measured; three sends alone never count as Stage A covered.

## G. Order

The $0 proof (§C) and its review; then **the slice**: one fresh clean day (2026-07-01) through Step 1, Steps 2–3, the ladder step (one
pass) and the judge, and production's same day, under the $1.50 sub-limit: requests, outputs, links, timing, spending and failures read
before the full run is decided. The slice is a wiring check, not a draw and not evidence of quality.
