You are reviewing, read-only, the benchmark design for the split extraction before any paid draw. Repository: this worktree. Report findings as a
numbered list, each with severity (blocker / serious / minor), the file and line, what is wrong, and the concrete fix. Say "No blocker" if none.

Read first:
- AGENTS.md §5, §7.1 (the frozen ruler; D372 counting; D373), §7.2, §7.3.
- docs/research/2026-11-05-production-plan/plan-final.md §2 C-8 (the acceptance agreed in six rounds) and review-log.md (rounds 0-6).
- docs/research/2026-11-06-architecture-benchmark/benchmark-design.md (the design under review).
- docs/research/2026-11-06-architecture-benchmark/bench_run.py (the harness), bench_measure.py (the measure), compare_ledgers.py (the gate check).
- src/hivemind/split.py, src/hivemind/views/round.py (the split branch), src/hivemind/replay.py, scripts/replay.py.
- The stored control draw the gate replayed: /Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d1 (manifest.json, replay.log),
  and the gate's output docs/research/2026-11-06-architecture-benchmark/runs/gate-v108-d1-offline-r2/replay.log.
- The r10 acceptance it mirrors: /Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/acceptance-design.md and acceptance_measure.py.
- The scorers it calls: /Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py,
  /Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/score_gold.py (same, same_matter), final-2026-10-30/final_scores.py (per_article).

Questions:
1. Does the design measure what C-8.1 agreed, on the frozen ruler, without changing any ruler file or adding a rule the ruler does not hold?
2. Is scoring both arms on the ledger (stored evidence records) instead of the raw extraction answers fair to both architectures? Does it hide a
   loss either arm has (for example, statements the extraction kept but matching or the writer dropped)? Compare with final_scores.per_article.
3. Are the two conditions' thresholds sound given the control's draw-to-draw spread (r10 control: helpful reached 161, 167, 169; judgement 15, 16, 14)?
   Is a criterion's null estimated?
4. Did the comparability gate prove what it must (the harness reproduces a stored draw), and is the one explained difference (revisions.said_day,
   D203) acceptable? Is the ReplayArchive (answering a stored refused judgement once, in recorded order) a faithful replay?
5. Anything in bench_run.py that makes the split arm or the control arm differ from the product's path other than the extraction (configuration,
   workers, matching workers, universe, seeds, items, judging)?
6. Anything missing that would make the result unreadable or force a rerun.

Out of scope: the prompts' wording, the judging and matching modules beyond how the harness calls them, modules Alex has not taken up, cost work.
