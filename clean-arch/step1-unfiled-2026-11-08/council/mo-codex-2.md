The four rules address the main causes, but I would not yet say they close all eight findings. Two cases remain: an orchestrator killed while its child is alive, and a judge that crashes before recording its outcome.

**What I agree with**

- **R1:** Checking the shared stop before the helpers’ internal retries and recording local budget stops on the shared ledger address the two stop-propagation defects. The synthetic 403 must be handled as a non-retryable refusal in each actual transport. The check immediately before a send also needs a defined ordering with a concurrent stop: a send already admitted before the stop may finish; one admitted afterward must be refused.
- **R2:** Persisting the launch inputs, distinguishing signal exits from ordinary failures, and removing the outer ladder redo address the identified state errors. The judge should keep its **internal** one-redo rule for the eligible check and transport failures.
- **R3:** The agreed reservation bound and validation of token counts address the identified accounting defects. An invalid response must still reach settlement with the full reservation; validation itself must not raise and strand it.
- **R4:** Running real subprocesses through the launcher, with the named failure cases and byte comparisons, would close the main proof gaps if the checks also have controls that fail for the intended breach.

**What I dispute or would tighten**

1. **R2 does not yet close the orchestrator-crash finding.** After a SIGKILL of the launcher, the proposed rule says to refuse a relaunch while its child PID is alive. It does not say how another draw discovers the dead launcher, and the surviving child can continue sending before anyone relaunches that label. Waiting for the child to die before recording the crash also leaves that period open. The run needs a way for sends or launches to detect that the owning launcher is gone and stop the shared ledger; the surviving child must then cease sending. Also cover the gap between starting a child and recording its PID, and distinguish a reused PID from the original process.

2. **The judge’s crash cell still needs an explicit fix.** In [run_stage_b.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/run_stage_b.py:89), a first judge folder with no recorded outcome is marked as a crash, but execution continues to the redo folder. R2(c) catches a killed judge *process* when the outer launcher survives, but does not by itself fix this inner recovery path. A crashed judge attempt must stop without the internal redo; a completed, eligible refusal may use it.

3. **A reason recorded by `--redo-reason` is evidence of a decision, not a classification by itself.** I agree that a manual relaunch after reading can be the cheaper, reversible choice while an exit status is ambiguous. It is a change to the automatic behavior in the agreed design, so the council should record that choice explicitly. The reading must identify an eligible failure from the component’s output; an arbitrary reason must not authorize a deterministic failure or a crash. If classification cannot be established, stop rather than redo.

4. **Stopping the whole run on a crash is a reasonable conservative decision, but it is a change to §D.** The table requires recording the crash and no redo; it does not list every crash as a whole-run stop. I agree with the proposed broader stop to avoid spending on a draw that cannot complete, provided the decision is recorded rather than described as already required by §D.

For the proof, please include both a killed child **and a killed orchestrator with a still-live child**, plus a stopped ledger during each helper’s retry pause. The trap must be composed with the stop gate so it observes the actual send path. Keep the recorded default-case rebuild and the wrong-archive mutant as separate checks.

Council position: not yet consensus; agree with the four-rule direction and the conservative crash policy, subject to closing orphan-child and judge-crash recovery and recording the manual-redo and whole-run-crash decisions.