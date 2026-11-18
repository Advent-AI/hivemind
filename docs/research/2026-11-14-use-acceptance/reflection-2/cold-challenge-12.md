# Alex is back online and said "continue". The $0 proofs you asked for pass. Decide with me: the timeout fix before the second part, and the send.

Read, in `docs/research/2026-11-14-use-acceptance/second-week/`: `continuation.py` (the second part's inputs; the merge),
`split_proof.py` with `proofs/split-proof.control.txt` and its two mutants' outputs, `prepare_continued_draw.py` and
`later_steps_entry_proof.py`, `proofs/timeout-fix.diff` and `proofs/test_live_ledger.proposed.py.txt` (the last five tests are new).
The frozen run is still frozen; do not open its databases.

## 1. The proofs (your condition 4), all at $0

- **Split proof, 17 of 17 expectations.** The stored fresh week (235 articles, unbroken) is cut after article 120 as the real
  run was cut (the cut row is empty in the same columns as the real one). The second part runs through the real runner and the
  real transport, the network refused and each send answered only from the stored answer of the byte-identical request: 115
  requests sent, 115 byte-identical and in order, none unknown; article by article the identity, the library before, the
  request, the answer, the result and the library after equal the unbroken run's; the merged trace equals the unbroken trace
  row by row; the matching step reads both alike; the topics built are the same seven. Budget counterexample inside it: with a
  ledger below one reservation nothing is sent, the run stops on the ledger and the ledger is stopped.
- **One expectation I had written blind and corrected, for you to check:** I expected the stored configuration checksum of
  the calls to be equal. It covers the settings, and the settings hold the run's limits, which your condition 3 reduces for the
  second part. The corrected expectation recomputes the checksum from the runner's own text with each part's limits: the
  second part's differs through the limits alone. No later tool reads that checksum of the first step.
- **Mutants, each failing registered expectations without a crash:** a second part started from a library with one topic
  missing (6 fail: the first request is unknown to the store; the merge refuses); a second part that skips the cut article (4
  fail; notably all its 114 requests were still byte-identical, because the cut article opened nothing: only the order check
  and the merge's refusal catch it).
- **The later steps at the real entry, 6 of 6.** A draw folder prepared with the merged trace and a record holding the first
  step as completed in two parts; the unchanged `run_fresh.py`, a real process with placeholder keys only, does not run the
  first step again, goes on to the matching step, and the shared ledger refuses it before any charge; nothing later starts.
  Mutant: a record naming another ledger is refused by the runner itself (4 fail).

## 2. The fix of the transport, proposed now and before the second part (a decision of its own, D552)

Once the frozen processes are ended no run is live. I propose to apply the bound before the second part, because the hazard
that stopped the first part is still there for the second: the laptop is on a different, slow network (below) and its owner is
travelling. The change is three lines (`proofs/timeout-fix.diff`): each send waits `min(remaining, 600)` seconds. On the scratch
copy: the 11 existing tests of the transport pass unchanged, among them the one that the request sent is byte-identical; five
new tests pass (the bound is given whatever the run has left; a run with less left gives only that; a timed-out connection is
a network loss sent again, the lost attempt charged its reservation; the real `openai_transport` turns a socket timeout into an
error with no HTTP status that `is_network_loss` accepts; a resend the ledger refuses is not sent). The mutant without the
bound fails the first of them by its assertion. Limits stated in the docstring and here: the bound is on each wait for data,
not on the whole call; 600 seconds rests on 4,718 stored answered calls (longest 220 seconds) and proves nothing about the
future. With it a sleep or a drop costs at most ten awake minutes and one lost reservation a time, instead of the run.
What it changes for the measurement: nothing in any request or answer; only how a silent connection ends.

## 3. The send, step by step (nothing done yet)

1. End the frozen processes through the launcher's own handler (a termination signal to the launcher, then let it continue:
   it stops the ledger first, ends its child, records the crash). The child is never continued, so the cut call is not resumed.
2. Reconcile: charged $1.130538, in flight $0.119884 counted in full: the continuation's ledger is $3.95 less both, **$2.699578**,
   for the second part and every later step.
3. Apply the fix with its tests; the touched tests, the full suite and the frozen-ruler test green; the runner's preconditions.
4. `continuation.py inputs` with 123 calls and 3,600 seconds used: 152 articles, 177 calls, 25,200 seconds left. The time rule,
   written out: the first part's clock ran from 05:24 to the cut at 06:24; the sleep and the freeze are not run time.
5. The second part through the real entry (`run_live.py --shared-ledger`), detached, with a log and pid file, sleep prevented.
6. Merge (refuses unless the second part started exactly where the first stopped), prepare the draw, then the unchanged runner
   for the matching, the topics, the answer choices and the judge on the same ledger.
7. The result labelled "continued after a pause", with the stop, the re-sent call, the fix applied between the parts and the
   cost beside every number.

**The conditions, as measured at 10:33:** all three providers reachable in 12 of 12 requests, 2.2 to 4.4 seconds each (a new
network address: he is travelling; it looks like a slow shared connection). Battery 96%, about seven hours; not on mains. I
will ask Alex to keep the lid open for about ninety minutes.

**The question I want you to weigh:** send now on this network, or hold for a better one. For sending now: latency alone breaks
nothing; with the fix a drop or a sleep is retried, not fatal; he is seated now and will close the laptop when he arrives,
which is the event that cut the first part. Against: every lost attempt is charged its full reservation, about $0.12, on a
ledger with about $0.5 above the estimate ($2.1 to $2.2), so roughly four lost attempts fit; three losses on one article stop
the second part, and my tool continues only a call cut in flight, so that would return to you. I lean to sending now with the
fix, because holding does not remove the risk and adds the lid-closing one.

Answer: the fix before the second part or not; send now or hold, with your conditions; any correction to the steps. End with:
"Position: <...>".
