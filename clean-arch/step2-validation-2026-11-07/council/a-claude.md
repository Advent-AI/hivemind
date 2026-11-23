# Claude's independent design (written before reading Codex's)

## A $0 census of the stored Flash d1 output (282 kept items, forward order)

A cheap heuristic is used here only to size the work, never as ground truth. It counts cross-article pairs as repeat-like when they
share at least 2 figures, or when their summaries' word sets overlap at Jaccard 0.35 or more.
- 253 candidate pairs. 71 of 282 items (25%) have at least one earlier candidate.
- 192 pairs share a thesis; **61 are on different theses only**. A thesis-scoped search would miss them, which supports Alex's
  entity-wide choice.
- Expectation, not a finding: true repeats are a minority of the pile (perhaps 15–25% of items). If so, dedup alone will not tame
  evidence growth.

## Ground truth

- **Population:** every ordered pair (earlier item, later item) of the same entity in forward order, from different articles.
  Same-article pairs are Step 1's within-item rule.
- **Candidate generation, independent of the search under test,** as the union of:
  1. the figure and entity overlap rule above;
  2. the summary-word Jaccard rule;
  3. a different embedding (a different model or text field from the tested one), top 30.
- **Labels by blind readers who see both items' summaries, passages, parties, dates and the two source articles' text around the
  passage:**
  - same statement (repeat);
  - revision (the same party's later version of the same figure or plan, or an official's confirmation or denial of a report);
  - same quantity, another party's view;
  - same matter, different fact;
  - different.

  Two readers per pair; disagreements go to a third with the sources.
- **Misses of the generator:** take a random sample of about 200 non-candidate pairs within the same thesis or month and have readers
  label them, to estimate the repeats the generator missed.
- **Fidelity cases:** flag pairs where one summary drifts from its passage (for example, "may adopt" written as "adopted"), so wrong
  merges caused by Step 1 are counted apart.

## Retrieval arms (all strictly forward: an item searches only items saved before it)

- **R0, production reference:** word overlap within each linked thesis, top 10 (`views/matching.rank_evidence`).
- **R1:** embedding of summary plus passages; the query is the thesis description plus the item summary; the entity's evidence;
  top 10.
- **R2:** R1 without the thesis in the query (evidence text only), to test whether the thesis helps or hurts cross-thesis repeats.
- **Metric:** recall at 10 of true repeats and revisions. A pair counts when the earliest true counterpart, or any true counterpart,
  appears (both are reported).

## Comparison arms (on the candidates R1 returns)

- **J0:** the existing Jev piece question as is ("already under the same thesis").
- **J1:** the same criteria with the cross-thesis wording ("stored evidence of the same company"), and a state carrying tier,
  original party, statement date and period on both sides.
- **Metrics:**
  - accuracy on true pairs;
  - wrong merges by type (a different party merged; a different period merged; a different fact merged);
  - a revision taken as a repeat;
  - candidates labelled repeat when the truth is different.

## Conflicts among several candidates (for Alex)

Proposed rule: if any candidate is a repeat, apply the repeat (add the source, add missing links). Else if any is a revision, link
the revision. Record every candidate's label for audit. This follows Alex's repeat decision; the precedence is his call.

## Order and cost

1. **$0:** build R0, R1 and R2 candidate lists. Embeddings cost about $0.02 per M tokens; 282 items is about 60k tokens.
2. **$0:** the ground-truth packets, then the readers.
3. **Retrieval recall at 10, $0** once embeddings exist.
4. **Cents:** Jev J0 and J1, one request per item, with up to 10 questions.
5. **Dossier read** for customer financing, competition and the product roadmap.

**Falsifiers:**
- recall at 10 below 90% stops at retrieval;
- comparison accuracy below 90%, or wrong merges above 2%, stops at Jev;
- a repeat share under about 15% means growth needs thesis structure.
