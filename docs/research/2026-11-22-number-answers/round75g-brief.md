# Council round 75g: verify the two certification fixes of round 75f (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 75f (`docs/research/2026-11-22-number-answers/codex-r75f.md`) did not accept slice 1 on two certification gaps. It judged
everything else optional under AGENTS §5, and said it would stop after verifying those two against the saved packages.
1. The dated leak checks never compared the returned package's date with the requested day.
2. The delivered format and allow-list identifiers were checked only against the module's own constants.

Claude fixed both in `release_check.py` (the literal `FORMAT`, `ALLOW_LIST` and `DATED`, and the checks in the final decision) and in
test 1 of `tests/test_release.py`. The new run is `poc/data/release-check-2026-11-23g/results.json`, and `RELEASE-CHECK-RESULT.md`
was updated.

## Questions

1. Are both 75f gaps closed? Check against the saved packages and the script's final decision. For example, would a September package
   offered for an August check now fail? Would a `/2` identifier with matching constants now fail?
2. Is any claim on the result page unsupported by the run?
3. Verdict: slice 1 accepted, or not accepted with each serious finding. Optional tightenings are listed as optional (AGENTS §5).

**Out of scope:**
- the frozen pieces;
- the closed v13s line;
- the POC's own behaviour;
- slice 2 and the idea path;
- the recorded evidence-summary disagreement;
- style;
- the optional items 75f listed.
