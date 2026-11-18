# Council mo, challenge round 2: closing the orphan child and the judge's crash cell

**1. A dead orchestrator, found by every send, without PIDs.** Each orchestrator already holds an exclusive `flock` on
`<root>/<label>/launch.lock` for its whole life; the kernel releases it the moment the process dies, and its children do not inherit the
descriptor (`subprocess` closes inherited descriptors by default), so a surviving child does not keep it held. The rule:
- the orchestrator takes its lock, then registers `{label: lock path}` in the shared ledger's state (under the ledger's lock), and removes
  its entry under the same lock before it releases its lock on a normal end (complete, awaiting a redo decision, stopped);
- the stop gate (R1), before every actual network attempt in every process (each child and every other draw), reads the ledger and
  tries a shared non-blocking `flock` on every registered lock path: one it can take belongs to an orchestrator that died without
  removing its entry; the gate then stops the ledger ("the launcher of <label> is gone") and refuses the attempt. The orphan's next send
  is refused, and so is every other draw's;
- a relaunch of that label takes the free lock, finds its own stale entry and its `started` attempt: the crash is recorded and the run is
  already stopped.
This needs no PID, so PID reuse does not arise, and there is no gap between starting a child and recording its PID: liveness is the
lock, held from before the first child starts until after the last ends. Ordering (your R1 point): the gate reads under the ledger's
lock; an attempt admitted before a stop is written may finish, one that reads after it is refused. SIGTERM or SIGINT to the orchestrator
terminates the child, records the crash, stops the ledger, then removes the entry.

**2. The judge's crash cell.** `run_stage_b.py`'s inner path (a first folder with no recorded outcome → counted as a crash → continue to
the redo folder) runs only when `run_stage_b` is launched again over the same root. `run_fresh.py` never launches the judge a second time:
the judge has no outer redo (R2(e)), and a crash of the judge's process (a signal exit, or an orchestrator found dead) stops the run before
anything is relaunched. The inner path is therefore unreachable through the orchestrator, and I would leave Stage B's runner as reviewed.
A test will hold it: a judge attempt found `started` with its folder present → the run stops and `run_stage_b` is not called again.
Exceptions inside the judge's own replay (refused twice, schema, transport) keep the internal redo, as you said.

**3 and 4.** Agreed: both are recorded as a new decision citing D439, as changes to §D, not as readings of it: the redo of Step 1, Step 2
and production is a relaunch with `--redo` and a required `--redo-reason` written to the record, allowed only when the component's output
shows an eligible failure (a transport failure after its retries, an answer refused or not fitting its schema), otherwise the run stops;
a crash stops the whole run.

**Proof additions agreed:** a killed child and a killed orchestrator with a live child (the child's next send refused, another draw's next
send refused); a stop written during each helper's retry pause (Jev, embeddings), the retry sending nothing; the trap composed under the
gate, so it sees only actual sends; the default-case rebuild and the wrong-archive mutant as separate checks; byte comparisons with
controls.

Does this close the eight findings? If yes, I build it, prove it at $0, and bring the code and the proof outputs back for a last read.
