Round 5 of the read-only review of the split benchmark design, before any paid draw. Your round-4 review: docs/research/2026-11-05-production-plan/r10/codex-review.out
(three serious findings and one packet gap). Revision 5: docs/research/2026-11-06-architecture-benchmark/benchmark-design.md, hashes in benchmark-design.sha256.
Changes: scripts/preflight_split.py runs model.check_schema on every replayed answer and refuses on any error or when none is judged (probe: 167
judged, 0 refused); bench_measure.py verify_pins refuses scoring when a run's first manifest pins other scoring files or golds, or when runs pinned
different shared files; bench_run.py refuses --archive-from without --offline; bench_traces.py marks each expected stage missing and carries the
written records in full with their links.
For each round-4 finding say resolved / partly / not, with the line you read; verify the hash file. Then say "No remaining blocker or serious finding"
or list what remains (file, line, problem, fix). Out of scope as before.
