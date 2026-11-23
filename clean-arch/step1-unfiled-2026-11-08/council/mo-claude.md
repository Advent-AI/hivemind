# Council mo: Claude's own read of the wiring code, written before Codex's review (2026-11-13)

What I think is weakest, so the review can confirm or refute it (not a conclusion to agree with):

1. **The redo is manual** (`run_fresh.py`): design §D gives one automatic redo for a stop a second send can change. I could not classify
   that from outside a subprocess (an uncaught Python error and an incomplete trace both exit 1), so the draw waits as `awaiting a redo
   decision` and a relaunch with `--redo` runs it once. Risk: a transient network failure costs a relaunch and my reading time; no money.
2. **Step 1's reservation rates** come from its limits file (input $0.50, output $1.20 per million) while the settlement uses
   `model.PRICES` (deepseek-flash $0.30/$1.20). Safe direction (reserve ≥ charge) as long as the limits file is the stored
   `stage2-limits.json`; a limits file with lower rates than `model.PRICES` would set the overrun flag on an ordinary answer.
3. **Settlement formulas differ by component:** Step 1 charges every input token at the full rate (no cached share); Stage A and the
   judge use `budget.cost` (cached share counted); Step 2's Jev and embeddings charge three times the reported tokens. All conservative
   against the bill, but the ledger's total will read above the recorded cost (it did for the census draws: $4.99 ledger vs $0.98 recorded).
4. **The run-wide stop is the ledger's persisted stop.** A stop of one draw (a crash, a redo that fails, mismatched cases, the judge's
   stop) stops every other draw at its next reservation, including a draw that is midway through Step 1 (its trace ends incomplete).
   That is design §D's "what stops the entire run", but it means one draw's crash leaves the others' partial outputs unusable.
5. **An orphaned child:** if `run_fresh.py` itself dies while a component process keeps running, the child keeps spending (inside the
   ledger) and writing; the next launch marks the attempt `crashed` and stops the run, so the child's next reservation is refused. The
   child's output is not used. Nothing kills the child.
6. **The interception proof's production component** compares requests by `model.request_identity` (sorted keys), not by the sent key
   order; Step 1's component compares the sent bytes. Production's transport passes the request dict unchanged to
   `model.openai_transport`, so the order is production's own, but the proof does not show it byte for byte.
7. **`proof_wiring.py`'s mutants** of the ladder file and the trace are caught by the adapter's own input checks (a refusal), not by the
   row comparison; the row comparison's power is shown by its positive control only.
