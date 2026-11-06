Round 6 of the read-only review of the split benchmark design, before any paid draw. Your round-5 review: docs/research/2026-11-05-production-plan/r11/codex-review.out.
Revision 6: docs/research/2026-11-06-architecture-benchmark/benchmark-design.md (hashes in benchmark-design.sha256).

Your last three rounds drew findings from one mechanism, the provenance of a scored draw. Following AGENTS.md §1 ("When one mechanism draws findings
round after round, stop answering findings: propose one structural rule"), the design now states one rule (section "What runs", "One rule for
provenance"): a scored draw is a paid draw made by this harness in a folder that held no ledger and no archive, keeping one mode and one set of pins
for its whole life; bench_run.py refuses a cross-mode or changed-pin resume; bench_measure.py refuses runs without this harness's manifest, with any
offline entry, with other scoring files, or where two runs pinned different versions of a file both use (only files one run alone pins may differ);
--reference labels stored runs. bench_traces.py marks an item UNREAD per section and stage, including archived calls with no answer.

Check the rule and its code against your round-5 findings (resolved / partly / not, with lines). Then report only a blocker or serious finding that
could change the benchmark's numbers or how they are read; say "No remaining blocker or serious finding" if there is none.
