Round 3 of the read-only review of the split benchmark design, before any paid draw. Your earlier reviews: docs/research/2026-11-05-production-plan/r7/codex-review.out
and r8/codex-review.out. The design is now revision 3: docs/research/2026-11-06-architecture-benchmark/benchmark-design.md. Changed since round 2:
- scripts/preflight_split.py rewritten: population reconciliation, full handover comparison after research-subject registration, refusals instead of
  skips; run on poc/data/split-v3-prod-0829-0830-r2-2026-11-06 (finished) and on four tampered copies (see the design §Before launch 2).
- The gate re-run in a scratch copy with the stored draw's writer line: runs/gate-v108-d1-offline-stored-writer (compare.txt, replay.log, views.sqlite).
- The verdict: no "at least as good"; differences reported beside the same-configuration range; stop rules for the window and the test articles.
- bench_traces.py (new): a reading packet for every helpful matter missed in at least one draw; bench_measure.py writes test hits too.
- Resume safety in bench_run.py and bench_test_articles.py; every script of the folder pinned.
- compare_ledgers.py: dependency_resolutions and thesis_group_aliases added.
- A cents probe on record preparation's ladder (probes/probe_reference_sentence.py, reference-sentence-2026-11-06.json; probes/ladder-account-*.json):
  the stored request re-sent gave a ladder where the stored answer had none; the reworded sentence regressed two controls; no change was built.

For each of your round-2 findings (the nine carried from round 1 and the five new) say resolved / partly / not, with the line you read. Re-run the
preflight and compare_ledgers yourself if you can do so read-only. Then list any remaining blocker or serious finding with file, line, problem and fix,
or say "No remaining blocker or serious finding". Out of scope: prompt wording, the judging and matching modules beyond how the harness calls them,
cost work, and whether the ladder coin flip should be fixed (it is reported, not part of this benchmark's design).
