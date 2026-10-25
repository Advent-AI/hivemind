# Current state

As of October 25, 2026; decisions through D170, plus isolated experiment D177. Governing design: `docs/system-design.html` and `docs/prd/`. The POC build began October 23. The foundation is frozen except pull mode and the final verdict; changes to frozen modules need a recorded decision. One row per measured step is in the [build log](research/2026-10-25-english/build-log.md). Earlier states are in [the previous snapshot](research/2026-10-25-english/current-state.before-refresh.md) and, for this phase before the close-out, in commit `f4ff787`; they are not work orders.

## Status

An isolated prompt candidate is published for review: `role-v11` and `poc-v24-admission-test` change only T6 extraction instructions. The [NAVER comparison](../poc/reports/2026-10-25-naver-admission/results.md) retained the planned 200 MW / 2028 project in 3/3 fresh treatments versus 2/3 controls. The default remains v23/T6-v10; no schema or horizon-policy change is adopted. The candidate needs wider source validation before adoption. The paid harness and database traces remain in the original experimental worktree; this branch includes the outputs and versioned prompt only.

Sequential request construction was centralized without changing requests, schemas, cache identity or processing order. [Validation](research/2026-10-25-sequential-cleanup/README.md): all 3,595 preserved request identities match and all 123 product/corpus tests pass. This maintenance does not enable concurrency or change extraction eligibility.

The English pipeline runs end to end. Extraction v10 (`role-v10`, `categories-v10`, `gpt-6-luna`) reads each item whole and declares groups for ongoing matters (D163–D166); matching runs on TypeSafe's Jev `jev-1.14.0` by default (D169, `poc/config/poc-v23.json`), with the generative matcher kept as the configured alternative (`poc-v23-llm`); the writer owns the replacement and succession rules (D167, D168); judging runs once a day before pull mode (D63).

Measured on two arms with the same extraction over the seed (NVDA, February 25 to July 23), the week of July 24–31 and August 1–15, scored per state against golds read from the texts (log rows 41–49, `poc/reports/2026-10-25-benchmark-v23/`): Jev matching equals the generative call on evidence and candidates (merge 7/9 vs 7/7, new 82/82 vs 70/71, evidence repeat and new within a point or two), groups far better (required members 35/38 vs 18/28), and matches at 45% lower cost and 4.8 times the speed. Its two weak states were root-caused and corrected in D168, measured by re-sending the stored requests: wrong replacements 17 to 1, successions 0/3 to 3/3. Evidence retrieval is measured apart: recall@10 36/36 and 46/49. The whole run cost about $1 per arm at published rates.

The phase was closed out with a code review (D170, log row 50). The ledgers, archives and traces are kept on disk and in two backups, listed in the [data manifest](research/2026-10-25-english/data-manifest.md); `poc/data/` is not in Git. Commit `f4ff787` holds the measured state whole, including the research code removed at the close-out.

## Adopted implementation

- D155: reference lists no longer veto candidates; full-match period handling, exact scopes, event identity, same-answer coalescing, old-key trust and atomic write and resume.
- D159: each item finishes writing before the next extracts.
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
- Not yet done: the service and UI switch to the English ledger (a new search index), `matching-v4` for dependencies in the generative matcher.

Pull mode and the final verdict remain earlier drafts to redesign together. The decided rule freezes the current state and reasons at the due date and closes the thesis. Upstream supply and human-review handling remain deferred.

## Next task: validate admission beyond the NAVER case

Validate the unchanged candidate instruction on additional stored-source contexts before default adoption. One-source success does not establish general extraction quality. Broader concurrency investigations and their experimental runtime are outside this branch; no batching or regrouping change is included. No further paid run is launched by this status update.

## Previous experiments

D157–D162 (grouping and extraction experiments, including the two-step source-first comparison) failed semantic acceptance; their reports are in `poc/reports/2026-10-25-*` and their code in commit `f4ff787`. The first Jev benchmark (log rows 33–41, `poc/reports/2026-10-25-benchmark/`) measured the earlier engine on extraction v9 and found the replacement and succession issues that D168 corrected.
