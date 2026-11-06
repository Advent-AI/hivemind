Round 4 of the read-only review of the split benchmark design, before any paid draw. Your round-3 review: docs/research/2026-11-05-production-plan/r9/codex-review.out.
The design is now revision 4: docs/research/2026-11-06-architecture-benchmark/benchmark-design.md, hashed in benchmark-design.sha256 (verify the hashes).

Changes for your round-3 findings:
- (2) pins: bench_run.pinned_files now covers universe.json, the seed file, the fixture, the items database, the scoring code and gold files, the
  standard page; a resumed draw with any differing pin is refused; bench_test_articles checks the items database hash; bench_measure prints the scoring
  files' hashes.
- (3) a new draw is refused when its folder holds a ledger or an archive without a manifest; only --archive-from may import one.
- (4) bench_traces.py now carries every archived extraction-stage answer in full (call id, request hash), the split's record preparation, the full
  handover, the processing steps, and marks NOT FOUND / unread explicitly. Try it read-only if you can (it needs a hits file; bench_measure writes one).
- (5) the design labels the current-code gate "identical except four dates" and states how the exception is handled.

Two points where I disagree with your round-3 fix, for you to judge:
- (1) wire bytes: the archive stores only the sorted-key request, so the send order of a stored request is not recorded anywhere and cannot be
  proven after the fact. You offered "state the limitation" as the fix if the order is not retained; the design and preflight docstring now state it.
  The benchmark re-sends no stored request (both arms send through production model.call). The preflight now also prints archived split answers that
  cannot be replayed (none on the probe; the split has no retry). Is anything still blocking here?
- (6) stop lines: the design has no acceptance threshold any more; nothing in it accepts or promotes the split (D359, Alex's). The stop lines apply
  D355, Alex's own words quoted in the design ("如果有什么不符合hypothesis 的地方你需要终止然后和我说我们重新评估"). plan-final §4.1 put "the criteria's
  thresholds" to Alex for an acceptance; Alex adopted the plan's recommendations (docs/DECISIONS-log.md, the 2026-11-05 record at the end). Does a
  stop rule under D355, with no acceptance claim, still need a separate decision from him? If yes, say exactly which sentence of the design needs it.

For each round-3 finding say resolved / partly / not, with the line you read. Then list any remaining blocker or serious finding (file, line, problem,
fix), or say "No remaining blocker or serious finding". Out of scope: prompt wording, the judging and matching modules beyond how the harness calls
them, cost work, the ladder coin flip.
