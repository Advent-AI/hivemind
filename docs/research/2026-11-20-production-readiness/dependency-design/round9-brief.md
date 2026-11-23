# Council R, round 9: review of the built version and its $0 proof, before the July send (D694 (c))

You passed design version 5 in round 8 (READY TO BUILD). It is built (working tree, not committed). `PROOF.md` lists every file
changed and every $0 check with its record (`mutants.log`, `rebuild-control.log`, `prefix-v119.log`, `dry-run.log`, the frozen
`reading-rule.md`). The harness is `july_test.py`; its `send` subcommand is written and not run.

Review read-only, against `DESIGN.md` v5 and `TEST-PLAN.md`:
1. The code: `src/hivemind/views/links.py`, the link step in `views/round.py`, `writing._write_links` and `write(proposed_links=)`,
   the store changes, `judging._dependency_lines_full`, the launcher refusals, `research_context`. Any defect, any departure from the
   design, any reachable cell the tests miss (`tests/test_links.py`).
2. The proof: does each check prove what `PROOF.md` says? In particular the dry run's assertions (`july_test.py dry`) and the archive
   proof.
3. The send: `july_test.py send` and `run_sequence` with `BudgetTransport`, `SharedLedger`, `install_stop_gate` as they behave
   (`clean-arch/e2e-comparison-2026-11-13/budget_replay.py`): can it spend outside the allow-list or above $0.15, can a stopped
   sequence be resumed, is every outcome recorded?

End with READY TO SEND, or NOT READY with the exact changes; list nonblocking items separately.
