# Current state

As of October 26, 2026; decisions through D182. Governing design: `docs/system-design.html` and `docs/prd/`. The POC build began October 23. The foundation is frozen except pull mode and the final verdict; changes to frozen modules need a recorded decision. One row per measured step is in the [build log](research/2026-10-25-english/build-log.md). Earlier states are in [the previous snapshot](research/2026-10-25-english/current-state.before-refresh.md) and, for this phase before the close-out, in commit `f4ff787`; they are not work orders.

## Status

Branch `feat/parallel-day` holds the parallel day (D172–D182) on top of the two earlier pushed branches: the sequential request-construction cleanup [`07aaff0`](https://github.com/Advent-AI/hivemind/commit/07aaff0db561803fe19f0ccb5ba80e7e4a8fa205) (all 3,595 archived request identities preserved) and the NAVER prompt candidate [`8848660`](https://github.com/Advent-AI/hivemind/commit/884866055cc265455bb72d25cd22e71db10e6558) (inactive by default). None of the three is merged into `main`.

The English pipeline runs end to end. Extraction v10 (`role-v10`, `categories-v10`, `gpt-6-luna`) reads each item whole and declares groups for ongoing matters (D163–D166); matching runs on TypeSafe's Jev `jev-1.14.0` by default (D169, `poc/config/poc-v23.json`), with the generative matcher kept as the configured alternative (`poc-v23-llm`); the writer owns the replacement and succession rules (D167, D168); judging runs once a day before pull mode (D63).

Measured on two arms with the same extraction over the seed (NVDA, February 25 to July 23), the week of July 24–31 and August 1–15, scored per state against golds read from the texts (log rows 41–49, `poc/reports/2026-10-25-benchmark-v23/`): Jev matching equals the generative call on evidence and candidates (merge 7/9 vs 7/7, new 82/82 vs 70/71, evidence repeat and new within a point or two), groups far better (required members 35/38 vs 18/28), and matches at 45% lower cost and 4.8 times the speed. Its two weak states were root-caused and corrected in D168, measured by re-sending the stored requests: wrong replacements 17 to 1, successions 0/3 to 3/3. Evidence retrieval is measured apart: recall@10 36/36 and 46/49. The whole run cost about $1 per arm at published rates.

The phase was closed out with a code review (D170, log row 50). The ledgers, archives and traces are kept on disk and in two backups, listed in the [data manifest](research/2026-10-25-english/data-manifest.md); `poc/data/` is not in Git. Commit `f4ff787` holds the measured state whole, including the research code removed at the close-out.

## Adopted implementation

- D155: reference lists no longer veto candidates; full-match period handling, exact scopes, event identity, same-answer coalescing, old-key trust and atomic write and resume.
- D159: an item's accepted extraction answers the request built after every earlier item finished writing.
- D172, D181: the parallel day (`hivemind.parallel_day`), opt-in with `scripts/replay.py --workers N`: later items' extraction requests are prepared early and prepared again right after any commit that changes them; each item accepts only a byte-identical request at its turn; matching questions within an item run concurrently and apply in order; one writer. The serial path stays the default.
- D163–D166: the English runtime (`vocabulary.py`, canonical values with legacy conversion on read), the fresh English library, research groups declared during extraction with aliases and decided by names in code (`views/groups.py`).
- D167–D169: no hard-coded identity; the measure vocabulary gains `market_size` and `project_cost`; the Jev engine (`views/jev_matching.py`, client `jev.py`) with the PRD's replacement definition, the shared succession rule and an answer for "the same quantity, another period"; a repeat may name the piece shown for the same evidence under another thesis.
- Idea service: the adopted two-call contract `poc-v9` / `idea-v7`, reasoning `none` (D135/D145); limits in the [Idea specification](poc/idea-card.md). The service still reads the sealed Chinese ledger with its search index.
- UI and service: shared thesis schema and adapter, cards, history chart, evidence, drawer and graph routing; historical reads, search, numeric claim evaluation and thesis bundles over HTTP and MCP ([service specification](poc/service.md)).

The [pipeline overview](poc/pipeline-plan.md) separates the implementation from the design requirements.

## Open defects and limits

- Shared by both matching engines (log row 49): the same figure stated in another document is often judged new (2–3 of 30 sampled new decisions); one matter can end up in several groups (the capex matter holds two groups in the Jev arm, three in the control); a decision naming a candidate of the same answer breaks a chain or duplicates a thesis (7 decisions over all ledgers, all generative); an empty `original_who` on both sides reads as the same party in the writer's rule; two names for the same population are sometimes kept apart (2 merge misses of 9 with Jev).
- Aggregate theses multiply under the `ai-capex` theme: the Jev arm holds nine 2026 aggregate-spending theses, each a different population under the gold's rule. Whether such variants deserve separate theses is the analyst's judgement, not an identity defect; it is recorded for a product decision.
- Extraction: the adopted instructions are narrower than the PRD's important-question rule and omit the personal-memo exception (the English prompt audit records it); extraction can change the quantity before identity matching (a guarantee amount versus the financing provided). D162's recorded failures in an experiment arm were not re-checked on v10.
- The classification simulation keeps the limits in [the preserved defect list](research/2026-10-25-english/classification-existing-defects.txt); a passing simulation is not classification acceptance.
- Corpus: 97 official notices with 56 body and filename collisions need the recorded re-fetch before a rebuilt corpus is relied on.
- The older intermittent search-test failure is untraced; the Docker external-connectivity restriction needs a current check before a container model run.
- Parallel day: the spend cap is checked per committed item, so in-flight early requests can pass it by at most the worker count's calls; the cap counts archived calls, not a retried attempt whose reply was lost (as for the OpenAI client). Re-prepared requests cost about 24% more per day.
- Not yet done: the service and UI switch to the English ledger (a new search index), `matching-v4` for dependencies in the generative matcher.

Pull mode and the final verdict remain earlier drafts to redesign together. The decided rule freezes the current state and reasons at the due date and closes the thesis. Upstream supply and human-review handling remain deferred.

## Parallel day (D172–D182)

Measured live on the complete July 27 day (53 items), three serial against three parallel trials interleaved ([result](../poc/reports/2026-10-26-e2e-parallel/results.md)): median 501.8 s → 112.5 s, **4.46× end to end**, 5.91× for item work; daily judging (~37–40 s) is the same code in both modes. Every trial's audit is clean; each parallel trial's runner accepted exactly the rebuilt exact-prefix request for all 53 items; each trial's answers replayed through the other mode give an identical ledger. Drift from the recorded sequential golden is inside the serial trials' own spread. The product entry point (`--workers 16`) ran the same day live in 135.5 s with the same checks clean. On recorded answers the parallel day equals the golden in all ten tables (D180, and again on the promoted module).

Fifteen consecutive days (August 1–15, 221 items) with every call answered by one deterministic oracle of the request bytes, at no cost (D182, [result](../poc/reports/2026-10-26-multi-day-oracle/results.md)): the parallel ledger equals the serial one in all 12 compared tables, its turns accepted exactly the serial run's 221 extraction requests, and a broken runner was caught. At recorded call durations the fifteen days take an estimated 2.79× less time (2,512 s → 900 s); a busy day gains 3.6–4.5×, a day of a few items 1.5–2×.

What remains of the time is not scheduling: items that depend on the item just before them (~45–60 s), daily judging (D63), and each item's two matching phases in order (~17 s). Ten times end to end on this day would need those to shrink.

## Next task

Alex's choice whether the parallel day becomes the replay default (lean: yes at 16 workers: same ledger for the same answers, 4.46× faster, about 24% more cost). No paid run is open.

## Previous experiments

D157–D162 (grouping and extraction experiments, including the two-step source-first comparison) failed semantic acceptance; their reports are in `poc/reports/2026-10-25-*` and their code in commit `f4ff787`. The first Jev benchmark (log rows 33–41, `poc/reports/2026-10-25-benchmark/`) measured the earlier engine on extraction v9 and found the replacement and succession issues that D168 corrected.
