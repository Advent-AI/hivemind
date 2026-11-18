I agree with the $1.50 ceiling, one-day scope, parallel launches, stop rules and proposed reading. I would change two things before the send so the results support what the slice claims to measure.

- **Run or verify the required $0 preflight immediately before the paid run.** [AGENTS.md §5](/Users/lchingen/hivemind/AGENTS.md:182) requires it before any paid run. The [existing preflight record](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/DESIGN.md:26) covers stored v116 runs and names its limits for v118; check its refusals and skipped cases against the current code, and record what it does and does not exercise.
- **Adjust the spending and timing claims to the records available.** The shared ledger holds aggregate spend and reservations, not a breakdown by component. The Step 2 runner discards reported embedding token counts ([run_forward.py](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:109)), and the draw record has no component timestamps. With parallel runs, exact component charges and times cannot all be recovered from those records. Either capture those observations without changing the frozen path, or report the total ledger charge and only the component costs and times that the archives and logs substantiate, marking the rest unavailable.

Keep the same-day claim only if both systems’ actual sends occur on the same calendar day. A send admitted before a stop may finish, as D449 specifies. If the fresh day opens no thesis, the launcher skips the ladder and judge; report those parts as unexercised rather than a successful end-to-end check.

I have reviewed the proposal; I have not launched the slice.

Council position: change the pre-send preflight and the spending/timing measurement claims first.