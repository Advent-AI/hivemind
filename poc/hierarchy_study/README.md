# Main-thesis experiment

Independent research harness. It reads the existing ledger and cached vectors, writes only into a new report
directory, and does not change extraction, production grouping, or the UI.

As of D149 (2026-10-25), associating theses with business subjects during extraction is a **required target behavior**.
That requirement does not adopt these experiments as the default pipeline. The current implementation gaps are
listed in [the pipeline plan](../../docs/poc/pipeline-plan.md#抽取时归组目标与当前实现); the single contract owner is
[the views PRD](../../docs/prd/06-views.md#研究主线抽取时归组). D147 is still an isolated prototype with known membership
errors, and D148's added-context variant remains rejected. The commands below describe historical experiments,
not a required post-extraction clustering job.

Run from the repository root, using its existing Python environment:

```sh
python3 poc/hierarchy_study/study.py prepare --out /absolute/new/report-directory
python3 -m pytest poc/hierarchy_study/test_study.py -q
python3 poc/hierarchy_study/study.py run --out /absolute/new/report-directory
python3 poc/hierarchy_study/argument_first.py --out /absolute/new/report-directory
python3 poc/hierarchy_study/render_report.py --out /absolute/new/report-directory
```

`prepare` refuses an existing directory. `run` uses 31 fixed records and four historical cutoffs. A–D are the
frozen comparison; E is a separately declared argument-first exploratory baseline. All use the same model and
the same final evidence snapshot for synthesis. Each of three independent samples has its own model archive.

The model-call wrapper makes one HTTP attempt, records a started reservation before sending, and refuses to
resend a failed or uncertain step on resume. The 48-attempt and $8 repository-price-estimate limits are hard stops.
These are experiment limits, not a claim about provider billing. No prompt repair or automatic sample replacement.

Outputs include exact requests/answers and usage, the frozen input, manifests, deterministic grouping metrics,
agent-reading probes, and a self-contained review page. ARI is a repeatability diagnostic for exclusive groups,
not a truth score. No semantic accuracy claim is made without a user-accepted reference.

Plan and product proposal: `docs/research/2026-10-24-hierarchy-poc/`.

## Fixed-scope follow-up experiments

`replay.py` compares fresh synthesis with old-summary updates on the two frozen Rubin and cloud-capex scopes.
Its results are in `poc/reports/2026-10-24-main-thesis-replay-01/`.

`basis_replay.py` uses the same snapshots, gives each source an immutable reference with code-owned provenance,
classifies every current source, and only then renders the final summary. A fresh direct-synthesis control uses
the same source references. The final readers see either all non-irrelevant basis rows or the direct summary's
chosen sources. It does not modify production storage, extraction, search, or UI.

```sh
python3 poc/hierarchy_study/basis_replay.py prepare --out /absolute/new/dated-directory
python3 poc/hierarchy_study/basis_replay.py run --out /absolute/new/dated-directory
python3 poc/hierarchy_study/review_basis.py --out /absolute/new/dated-directory
```

The follow-up is bounded to 42 single-attempt model requests and an $8 repository-price estimate. Do not rerun
model experiments to reproduce the report: `review_basis.py` reads saved answers without model calls.
Its governing plan is `docs/research/2026-10-24-main-thesis-basis/plan.md`.

## Ingestion-time organization

`ingestion_groups.py` starts with empty experimental databases and reads three original articles through
the existing dispatch, extraction checks, thesis search, matching checks and writer. The grouped arm adds
relationship hints and group decisions inside the existing calls, without a separate clustering call.
English protocol enums are adapted in memory for legacy checks; generated prose and newly stored data stay English.

```sh
python3 poc/hierarchy_study/ingestion_groups.py prepare --out /absolute/new/dated-directory
python3 poc/hierarchy_study/ingestion_groups.py run --out /absolute/new/dated-directory
```

The recorded run is `poc/reports/2026-10-24-ingestion-groups-01/`. `replay_ingestion.py` verifies identical
requests against those stored answers without network access, applies the affected-group bookkeeping fix,
and projects the existing extraction hints to resolved IDs. That projection is diagnostic, not an adopted
production grouping rule. Run `review_ingestion.py --source ... --verified ...` for the measured census.
Plan and findings: `docs/research/2026-10-24-ingestion-groups/`.

## D143 relation handoff experiment

`relation_handoff.py` keeps extraction-owned associations through the existing identity checks and writer. `test_relation_handoff.py` uses the original three article answers and real temporary databases; `review_handoff.py` follows fixed source passages through evidence links and memberships.

The new live experiment failed acceptance: 1/3 automatic shared groups, equal to the fresh D142 control. The code-only replay passed 3/3. Do not treat this module as an adopted production grouping strategy. Results and next contract question: `docs/research/2026-10-24-relation-handoff/findings.md`.

## D144 continuing business subjects

`ingestion_threads.py` requires local business-subject references during extraction and resolves subject identity separately from thesis identity in the existing matching call. `review_threads.py` traces actual source passages, and `diagnose_threads.py` replays the first article with explicitly edited self-targets without making model calls.

The live experiment is not validated: both returned new-arm matching answers failed on self-targets, and the third extraction timed out. No new stream reached the later grouping test. The zero-call format diagnostic is not an acceptance pass. Recorded results: `poc/reports/2026-10-25-ingestion-threads-01/`; explanation and proposed next contract change: `docs/research/2026-10-25-ingestion-threads/findings.md`.

## D147 extraction-owned membership

The active isolated prototype is `retained_membership.py`. Extraction reads the full article and the globally searched business subjects, then assigns each candidate thesis to a displayed existing subject or a declared new one. Ordinary matching resolves only thesis and evidence identity. The original writer preserves membership; unreferenced proposed subjects are never written and no longer abort the article.

`direct_subjects.py`, `extraction_membership.py`, and `flat_membership.py` preserve earlier variants and their failed raw outputs. They are research records, not production defaults. The final prototype retains all reference checks, uses the single-pattern reference schema, and replays unchanged requests before calling missing steps. All variants share the same 48-call/$8 experiment budget.

Inspect the recorded result without model calls:

```sh
python3 poc/hierarchy_study/review_threads.py --out /Users/lchingen/hivemind/poc/reports/2026-10-25-direct-subjects-01 --retained
```

Plan, diagnosis, per-variant outcomes and limitations: `docs/research/2026-10-25-direct-subjects/findings.md`. The prototype has not been adopted in production, MCP or the UI.


## D148 grouping consistency diagnostic

`grouping_consistency.py` runs three fresh controls and three membership-context samples from the same two-article prefix. The context variant is **not adopted**: OpenAI reaches Rubin, but one sample also admits an unrelated PC thesis and another omits risk evidence. The control also has a wrong SK membership. D147's three fixed core connections remain valid; complete grouping consistency is not established.

`review_consistency.py --out /Users/lchingen/hivemind/poc/reports/2026-10-25-grouping-consistency-01` inspects all six recorded outputs without model calls. The independent run used 12 requests/$0.202629 estimated under its 18-request/$2 cap. Results and the proposed joint review with the Idea work: `docs/research/2026-10-25-grouping-consistency/findings.md`.

## D150 membership explanations (not adopted)

`membership_basis.py` replaces each bare membership ID with a short source-to-scope explanation followed by
its ID in the same extraction call. It validates the full answer, then projects only the IDs into the original
pipeline; explanations are archived, not treated as evidence. The 12-call comparison did not solve consistency:
one basis sample linked OpenAI correctly, one omitted it, and one misassigned PC to Rubin. The conditional Google
case was not run. Findings and the next handoff: `docs/research/2026-10-25-grouping-basis/`.
