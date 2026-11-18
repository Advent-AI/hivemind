**Do not send yet.** The matched comparison is worth preparing, but its scorer can call a result favourable when the high-effort arm has lost answers, and it can close the candidate when neither arm provides a meaningful test.

The changes needed are:

1. **Account for every send in the decision.** `reading()` skips answers refused twice by code, while `score()` counts hard-line faults only among answers shown to readers. A high-effort arm could therefore appear to have fewer faults because its answers disappeared. Report all 78 outcomes per arm, distinguish model refusals, code refusals and unreadable attempts, and make missing answers unable to improve the verdict. Test a case where high loses answers and the old scorer would have called that an improvement. [Probe](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/effort/effort_probe.py)

2. **Make an uninformative tie inconclusive.** The current rule closes the candidate even when both arms have zero faults; the test explicitly asserts that result. Zero versus zero shows no improvement, but it does not establish that high effort failed to fix the observed problem. Predeclare the minimum medium-arm signal needed to distinguish a close from an inconclusive result. [Tests](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/effort/test_effort_probe.py)

3. **Check the sound controls as well as the planted errors.** The scorer explicitly skips their `all: holds` expectation. Predefine how a false failure on a sound control affects validity, and test it. The four planted faults alone cannot detect an overly harsh reader.

4. **Verify actual request order, not just canonical hashes.** The check is useful, but the stored-request comparison uses the archive’s sorted-key identity, and dictionary equality does not establish nested key order. Compare the production-serialized requests, including nested order, with effort as the only difference.

Keep the spending caps and stopped-draw rule. After these $0 corrections and decisive checks, the council can make the send decision; the existing **$1 ceiling** need not change. The outcome remains a small, previously exposed-topic diagnostic, not acceptance on the 44.

**CONSENSUS: no, because the decision and control checks need the four corrections above before a paid send.**