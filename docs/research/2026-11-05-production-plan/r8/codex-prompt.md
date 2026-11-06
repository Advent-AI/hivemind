Round 2 of the read-only review of the split benchmark design, before any paid draw. Your round-1 review is
docs/research/2026-11-05-production-plan/r7/codex-review.out. The design is now revision 2:
docs/research/2026-11-06-architecture-benchmark/benchmark-design.md. Changed since round 1:
- bench_run.py: every window draw copies one fixture ledger (fixture/views.sqlite) and records file hashes per draw; the ReplayArchive claim narrowed.
- bench_test_articles.py (new): golden-v5 test's 30 articles through each arm's extraction stage against the same fixture, three draws each.
- bench_measure.py: scores the checked handovers (the ledger's handovers table) and the ledger records, reports where each helpful matter ends,
  writes per-matter hits, uses score_ref.same_question unchanged (labelled a counting aid), prints the standard version and page hash and the D373
  concern; --test mode for the test draws.
- compare_ledgers.py: also processing_steps, research_subjects, match_records.
- The thresholds were re-derived from six stored control draws (r9: /Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03/d1..d3; r10:
  /Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d1..d3); check the arithmetic yourself.

For each of your round-1 findings 1-9 say resolved / partly / not, with the line you read. Then list any new blocker or serious finding with file,
line, the problem and the fix, or say "No remaining blocker or serious finding". Verify claims against the files; do not accept the design's own
summary. The split preflight (§Before launch 2) runs when the probe run in poc/data/split-v3-prod-0829-0830-r2-2026-11-06 finishes; judge whether the
design's use of it is sound. Out of scope: prompt wording, the judging and matching modules beyond how the harness calls them, cost work.
