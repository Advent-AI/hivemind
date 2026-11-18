**NOT READY:** the reader can still stop on a valid judge answer if the response’s usage metadata has an unexpected shape.

For example, an answer with valid JSON content and `"usage": "unavailable"` is saved by the sender, but the reader calls `.get()` on that string and stops before reporting any verdict.

**A. The three earlier findings**

- **Not serious — schema-refused answer: closed for the reported cases.** The reader now reports a schema refusal and immediately continues without reading fields from the invalid answer. The separate usage-metadata defect below occurs before that check. [judge_probe.py](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/judge_probe.py:177)
- **Not serious — retry cost: closed.** The protocol now includes three attempts per send. The no-send check returned **$0.1994** for all three attempts, below the $0.25 cap; the protocol’s **$0.1995** is a slightly higher, conservative figure. The budget reserves each attempt under a lock. [PROTOCOL.md](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md:55), [budget.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:63)
- **Not serious — preflight record: closed with the stated limits.** The log records the 10 refused rows, 43 enum values checked, and the unexercised extraction and matching checks. The protocol discloses those limits. [preflight.log](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/preflight.log:3), [PROTOCOL.md](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md:58)

**B. Sender and reader**

1. **Serious — unexpected usage metadata can stop the reader.** The spending code explicitly treats a non-dictionary `usage` as unavailable and can return and save the response. The reader then assumes any truthy `usage` has `.get()`. A string or nonempty list therefore raises before the answer is checked, recorded in `reading.json`, or included in a verdict. The raw response remains in the per-draw file, but the promised reading is not produced. [budget.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:41), [judge_probe.py](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/judge_probe.py:143), [judge_probe.py](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/judge_probe.py:177)

- **Not serious — verdict rule.** For rows the reader successfully processes, the code requires three accepted answers in each arm, prints a difference only for two distinct unanimous rungs, and treats mixed answers as undecided. [judge_probe.py](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/judge_probe.py:52), [PROTOCOL.md](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md:66)
- **Not serious — request identity.** The no-send check passed. It compares the whole request after replacing only the user text, then checks the four-line removal and count change. Historical wire bytes remain unavailable, and the protocol says the current ordering is *consistent with* them rather than proven identical. [judge_probe.py](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/judge_probe.py:77), [PROTOCOL.md](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md:46)

**C. Protocol claims**

- **Not serious — rounding discrepancy.** The protocol says $0.1995 while the current check prints $0.1994. The protocol does not understate the check’s estimate. [PROTOCOL.md](/Users/lchingen/hivemind/clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md:55)
- **Not serious — replay evidence.** The saved reports support the 239-request control and the first differing round, including the 14 identical requests and the unbuilt remainder. I found no other sentence in the scoped protocol that claims more than the inspected evidence supports. [control-report.json](/Users/lchingen/hivemind/poc/data/clean-step2-edge-effect-2026-11-10/control/control-report.json:1), [counterfactual-report.json](/Users/lchingen/hivemind/poc/data/clean-step2-edge-effect-2026-11-10/remove-relation/counterfactual-report.json:14)

No file was edited and no network request was sent.

**NOT READY — serious finding 1.**