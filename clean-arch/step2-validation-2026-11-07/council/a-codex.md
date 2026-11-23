**I would not use the proposed pass line yet.** It can miss the most costly error: treating a revised or richer statement as a repeat and hiding what changed. For example, two reports may both say “$5 billion,” but one may add a condition that matters to the investment decision.

The plan below is an **exploratory validation design**, not an accepted ruler or evidence that Step 2 works. The stored run and the proposed thresholds are described in [the validation frame](</Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/LOG.md>).

### 1. Build an independent reference

Reconstruct the 282 kept evidence items from `trace.result`, resolve local thesis IDs using `new_thesis_ids`, and use `after_state` for the thesis descriptions. Give each item a stable key based on article sequence and local evidence ID. Preserve all links: one item linked to two theses is still one evidence item.

Generate possible pairs **without using the embedding search under test**:

- Independently review every earlier item for a randomly selected, predeclared sample of incoming articles. This exhaustive sample is the control for what any candidate generator misses.
- For the rest, pool several independent discovery routes: reader-organized topic timelines, shared parties and quantities, lexical overlap, and source or event references. None is a condition for inclusion. Include cross-thesis pairs and hard negatives.
- Record the number of possible and reviewed pairs, the sampling probabilities, and the discovery route for every pair. Do not use model predictions to decide the reference label.

Two independent readers label pairs **repeat, revision, different-party forecast of the same quantity, or different**. The third label is an analysis subtype of *different*, not a fourth Jev outcome. Readers can mark insufficient information rather than guess. Resolve disagreements against the source and record both original labels and the reason. Readers must see both complete summaries, all source passages and enough surrounding article context, reporting source, original claimant, publication and stated dates, tier, period, figures and qualifications, plus associated thesis descriptions. Hide search ranks and Jev answers.

Estimate missed positive pairs by checking how many repeats and revisions in the exhaustive sampled articles were absent from the pooled generator. Report the sampling method, raw counts, uncertainty and an appropriately weighted estimate; also report misses by cross-thesis and relationship type. If the sample finds too few positives to estimate this usefully, expand it before claiming recall. An exhaustive sample estimates missed pairs; it does not prove the remaining reference is complete.

The older [65-decision reference](</Users/lchingen/hivemind/poc/eval/gold/evidence-decisions-seed-2026-10-25.json>) is useful for regression examples, but its existing thesis and target setup is not independent ground truth for this new search. Its [scorer](</Users/lchingen/hivemind/scripts/score_evidence_gold.py>) also sets uncertain cases aside and scores acceptable targets in that earlier setup.

### 2. Test retrieval

**Proposal:** embed each prior evidence record’s summary and verified source passages, with clearly labelled original party, stated time and evidence period when available. Query with the incoming thesis description, outcome and period plus the incoming evidence summary and passages. Compare alternative text representations only as separately named experiments; do not tune on the final review sample.

Search all earlier evidence for the same entity, including records linked to other theses. Query once for each `{thesis, evidence}` association, including a new thesis. Exclude the incoming article and later articles: article sequence defines availability, while a statement’s own date remains evidence for comparison and must not be silently replaced by publication date. Freeze the ordering rule before scoring.

Run the production reference as written: [word overlap within the linked thesis, top 10](</Users/lchingen/hivemind/src/hivemind/views/matching.py:108>). It has no prior same-thesis candidates for a newly created thesis. Report that limitation rather than giving it an entity-wide pool and calling it production. A separate entity-wide word-overlap arm would help distinguish the value of wider scope from embeddings.

The existing [search module](</Users/lchingen/hivemind/src/hivemind/search.py>) indexes theses, so its embedding transport and vector operations may be reusable; it is not already an evidence index.

### 3. Test comparison independently

The existing [Jev question](</Users/lchingen/hivemind/src/hivemind/views/jev_matching.py:90>) asserts that the stored piece is under the same thesis. Replace that premise for this experiment: compare the incoming and candidate statements **within the entity**, explicitly allowing different thesis links. Give the incoming thesis as context, not as proof that the two statements match.

For both statements provide the full supplied passages and summary, original party, reporting speaker and source, tier, original date and partial date text, publication date, evidence period and relevant thesis context. Unknown values stay unknown. Preserve each candidate’s identity outside the model response. Jev accepts one state and multiple typed questions; its current evidence choices do not contain an uncertainty option ([transport](</Users/lchingen/hivemind/src/hivemind/jev.py>), [criteria](</Users/lchingen/hivemind/src/hivemind/views/jev_matching.py:37>)). An uncertainty representation and probability handling remain open; do not silently call an uncertain pair different.

Test Jev on independently labelled pairs regardless of whether search found them, then separately on actual top-10 results. This separates comparison errors from retrieval misses.

**Open for Alex:** if one incoming item is labelled repeat of one candidate and revision of another, or repeats of several candidates, what should be saved? Do not invent a winner or simulate a definitive dossier outcome until that is decided. The [PRD](</Users/lchingen/hivemind/clean-arch/PRD.md:143>) leaves conflicting and uncertain candidates open.

[D168](</Users/lchingen/hivemind/docs/DECISIONS-log.md:2338>) permits cross-thesis repeats but bounded replacement to the same thesis in the older path; its revision definition is useful prior evidence, not automatic approval of cross-thesis revision behavior. [D202](</Users/lchingen/hivemind/docs/DECISIONS-log.md:2594>) keeps both sides of a revision. [D204](</Users/lchingen/hivemind/docs/DECISIONS-log.md:2610>) preserved both repeat texts after 8 of 40 sampled prior repeats lost different or richer content. Alex’s later clean-design choice is to reuse a repeat record and add the source and missing link ([PRD §6](</Users/lchingen/hivemind/clean-arch/PRD.md:161>)); the earlier loss remains a risk to measure, not a reason to silently reverse that choice.

### 4. Metrics and proposed pass line

The 90% figures are reasonable **discussion targets**, but not sufficient acceptance criteria:

- **Retrieval:** recall at 10 for all labelled earlier repeat and revision pairs, separately by type and cross-thesis status. Also report the share of incoming associations for which at least one acceptable prior target is found. Show counts and uncertainty, including estimated generator misses.
- **Comparison:** confusion matrix on independently sampled pairs and on retrieved candidates; report repeat and revision recall separately, plus revision incorrectly labelled repeat.
- **Wrong merges:** count every false repeat by cause, including different parties, different periods or quantities, and richer or qualified statements. Report both false repeats / all true-different comparisons and false repeats / all predicted repeats. The proposed “2% of comparisons” alone can look good when most pairs are easy negatives. Show counts and uncertainty.
- **Combined path:** correct target and relationship after retrieval, including missed targets and uncertain cases. A correct label against the wrong target is not a success.
- **Three dossiers:** report records per thesis before and after deduplication, sources and links retained, revisions visible, and manually inspect whether meaningful qualifications disappear. Label this a simulation until conflict handling is decided.

A numerical pass requires Alex’s agreement, a sufficiently informative sample and no concealed loss in the inspected dossiers; small samples should produce an inconclusive result rather than a confident pass.

### 5. Cheapest decisive sequence

1. **$0:** reconstruct and audit item identities, links, entity and sequence; inspect representative articles and reference pairs; build and independently review the sampled reference. Stop if source context, IDs or forward availability cannot be reconstructed reliably.
2. **$0:** replay the word-overlap reference and verify the exhaustive-sample miss estimate. Stop if the reference misses too many positives or has unresolved reader disagreement large enough to change the conclusion.
3. **Cents, after counting calls and tokens:** embed the fixed corpus and queries; compare retrieval arms on the same reference. If the relevant earlier statements rarely enter the top 10, comparison quality cannot rescue the path.
4. **Cents:** send the fixed Jev requests on labelled pairs, including hard negatives and revisions, then on retrieved candidates. If it repeatedly turns changed or richer statements into repeats, the proposed saving behavior is unsafe at the measured rate.
5. **$0:** inspect the three simulated dossiers and present the unresolved multi-candidate choice to Alex. This does not validate the writer or Step 4.

