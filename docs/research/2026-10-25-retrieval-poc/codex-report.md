Embedding recall is worth a small, measured POC, but the stored data do not support replacing the current matching or grouping decisions yet. The strongest immediate result is encouraging: using existing cached vectors, the current hybrid search retrieves an accepted direct thesis in the top 10 for all 18 idea queries labelled as covered. However, finding a related thesis is easier than deciding it is the same question. Several duplicate candidates already saw the right earlier thesis and were still opened separately. The next experiment should therefore measure retrieval and identity decisions separately.

The smallest useful experiment can start at $0, then use cents of embeddings and an optional, separately authorised reranker comparison. Keep the current pipeline as the control. Use source-backed labels, preserve differences such as guarantee versus chip financing, and allow an uncertain result. For example, Rubin shipments, Vera CPU revenue and SK’s factory opening can belong to one research group while remaining three different theses. This review made no model calls, spent no money and changed no repository files.

**1. The census uses completed, sequence-bounded snapshots.** The grouped run finished during this review. The ungrouped database contains some August 6 work; I excluded it because August 5 is its last completed day.

| Label | Ledger | Completed through | Sequence cutoff | Theses | Evidence | Matching records |
|---|---|---:|---:|---:|---:|---:|
| G | [Grouped English](/Users/lchingen/hivemind/poc/data/english-groups4-2026-10-25/views.sqlite) | July 31 | 259 | 45 | 365 | 145 |
| E | [Ungrouped English](/Users/lchingen/hivemind/poc/data/english-2026-10-25/views.sqlite) | August 5 | 311 | 60 | 486 | 210 |
| C | [Chinese T4c](/Users/lchingen/hivemind/poc/data/views-2026-10-25-v15-T4c.sqlite) | July 31 | 259 | 40 | 358 | 155 |
| S | [Sealed Chinese](/Users/lchingen/hivemind/poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite) | August 15 | 584 | 94 | 827 | 315 |

Database connections used SQLite read-only URIs. Counts below filter each table by its own sequence field. IDs are ledger-specific: `G.v13` and `E.v13` are different records.

I read all 239 stored thesis questions, counted structural classes across these snapshots, and traced the named semantic cases into their evidence, matching decisions and source items. Structural counts are exhaustive for these snapshots. Semantic duplicate labels below are my source-backed review judgments, not owner-approved gold or a proven whole-library error rate.

The governing boundary is clear. [D154–D166](/Users/lchingen/hivemind/docs/DECISIONS.md:2218) preserve structured identity, remove the watch-list veto, require extraction-time grouping and prioritise stable product behaviour over cost optimisation. The historical sections of the keyed and grouping plans do not override those later decisions.

**The duplicate problem contains both genuine repetition and valid differences.**

| Class and counted population | Concrete records | Finding |
|---|---|---|
| Identical complete stored keys | G: 0 duplicate groups among 45 keys; E: 0/60; C: 0/40 | This does not establish semantic uniqueness. Free scope wording can keep the same quantity under different keys. |
| Source-backed duplicate: standalone CPU revenue | S.v16 and S.v48: 1 pair, 1 redundant thesis | S.v16’s initiating evidence explicitly clarifies that the roughly $20bn forecast is for standalone CPUs. S.v48 retells the Vera CPU forecast. They were created July 24 and August 3. |
| Source-backed duplicate family: the reported $250bn Ohio financing guarantee | C.v17, C.v22, C.v24: 3 pairwise comparisons, 2 redundant theses | “Guarantee,” “financial backstop” and the retold “financing” refer to the same reported arrangement in these sources. Different wording caused separate questions. These are proposed same-quantity labels for owner review. |
| Further likely duplicate requiring a source correction | C.v18 and C.v21: 1 pair | Both questions concern financing OpenAI’s chip purchases for the project. However, C.v21’s initiating stored evidence concerns the $250bn guarantee rather than adequately supporting its chip-financing question. Do not turn that record into clean positive gold without resolving this. |
| Overlapping 2026 spending scopes | G.v1/G.v20 and E.v11/E.v19: 1 pair in each English run | Top-five/hyperscaler capex and aggregate AI-infrastructure spending overlap. Their equality is not established by similar amounts or wording. |
| Sealed spending family | 9 theses: S.v1, v20, v23, v47, v71, v72, v86, v88, v89 | Four concern 2026 aggregates, three concern 2027 aggregates, one is cumulative 2024–2029 investment and one is SpaceX capex. Nine related theses are not nine duplicates. |
| Equal guidance, different accounting basis | E.v5/v8; S.v6/v8 | GAAP and non-GAAP tax remain different quantities even when management gives equal guidance. |
| Related AMD measures | S.v50/v52; E.v52/v54/v60 | Revenue level, revenue growth and different years must remain distinct. |

The strongest proposed positive labels therefore comprise **four pairs across two families**, representing three redundant thesis records: S.v16/v48 and C.v17/v22/v24. The additional chip-financing pair remains provisional. The aggregate-spending families require explicit scope judgments.

The Chinese financing census also corrects an easy overstatement. C has **eight `financing_amount` theses**, but they are not eight copies of one quantity. Seven concern the Ohio/OpenAI arrangements; C.v19 concerns Japan’s separately funded power plant. Within the seven, the guarantee, chip financing, project cost and aggregate transactions are different measures.

The decisive matching traces show why recall alone is insufficient:

- **S match record 172:** S.v16 was already second in S.v48’s candidate list. The model opened a new thesis because it interpreted “CPU total revenue” and “Vera revenue” as different.
- **C records 78, 88 and 96:** the earlier financing theses were shown. The model distinguished their wording instead of recognising the underlying reported arrangement.
- **G record 43 and E record 44:** the earlier hyperscaler thesis was shown. Both models deliberately distinguished its scope from aggregate infrastructure spending.

The last two English decisions may be correct. They must not become “recall failures” merely because a later reviewer prefers fewer theses. E.v11 also starts from evidence forecasting capex **by 2027**, despite its stored 2026 question; that makes it particularly unsuitable as unquestioned identity gold.

Sources: each ledger’s `views`, `view_keys`, `evidence`, `evidence_links`, `processing_steps` and `match_records`; [source items](/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite); [build log, rows 11–13](/Users/lchingen/hivemind/docs/research/2026-10-25-english/build-log.md).

**Evidence repetition is common, and the existing pipeline already consolidates much of it.**

For each input and matching pass, I selected the last record without validation refusals. A matching “repeat” count below is an evidence–thesis decision count; one incoming statement can produce several such decisions.

| Ledger | Accepted repeat decisions | Evidence with sources from multiple input IDs | Evidence spanning multiple nonempty publisher values | Additional distinct input references beyond the first |
|---|---:|---:|---:|---:|
| G | 129 | 54 | 36 | 110 |
| E | 166 | 61 | 36 | 137 |
| C | 114 | 51 | 32 | 100 |
| S | 260 | 94 | 61 | 192 |

These are consolidation counts, not independent confirmation counts or verified repeat precision.

For example, E.e122 stores the reported $250bn guarantee with **eight source inputs from eight publisher values**. E.e36 has 20 source inputs. Retelling is therefore a substantial part of the workload, not an edge case.

An exhaustive whitespace-normalised exact-quote comparison across the 2,036 evidence rows found **two duplicate-quote groups, both in G**:

- **G.e133/e134:** the same July 27 NVIDIA statement about SSI increasing compute through Vera Rubin access. This is a missed consolidation.
- **G.e17/e47:** identical inventory/capacity language attributed to February and May company statements. Identical wording across different statement dates does not establish one evidence identity.

G.e133/e134 exposes a search-boundary problem. The first copy links to G.v5, the shipment thesis. The second links to G.v4, the product-revenue thesis. At sequence 87, match record 50 searches only G.v4’s evidence, so G.e133 is unavailable. The model reasonably reports no matching supplied evidence.

A better embedding within the same search boundary cannot recover that copy. The narrow structural question is whether an exact, provenance-aware lookup may find an already stored statement across thesis boundaries before normal within-thesis comparison. Broad global semantic evidence merging would be a much larger change.

Sources: `evidence`, `evidence_sources`, `evidence_links`; G `match_records.id=50`; [within-thesis ranking](/Users/lchingen/hivemind/src/hivemind/views/matching.py:120); [writer’s repeat handling](/Users/lchingen/hivemind/src/hivemind/views/writing.py:177).

**An out-of-list target is not automatically a recall miss.**

| Ledger | Raw merge/succession decisions | Target absent from that candidate’s own list | Raw repeat/replace decisions with nonempty targets | Evidence target absent from that pair’s own list |
|---|---:|---:|---:|---:|
| G | 14 | 2 | 154 | 4 |
| E | 17 | 3 | 192 | 9 |
| C | 21 | 1 | 115 | 0 |
| S | 34 | 4 | 280 | 3 |

These counts retain retries. Two C repeat decisions and one S repeat decision had empty targets and are excluded from the nonempty-target columns.

All **10 candidate-list exceptions** need classification before scoring:

- Four target another candidate, such as `c1`, rather than an existing thesis.
- Four attempt a wrong-quantity or wrong-object merge: standalone CPU into total revenue, North America revenue into total revenue, or Amazon capex into an industry aggregate.
- Two are extraneous candidate decisions in S record 40; that input’s stored handover contains no candidates.

Thus this particular census finds **zero demonstrated correct candidate destinations lost from the own-list search**. It does not prove complete recall: a model can choose “new” precisely because the right thesis was never shown.

The evidence-list exceptions include real ranking misses:

- E records **83/84**, July 27: Huang’s qualification of the financing story chooses E.e122 or E.e123, shown elsewhere in the request but outside its own pair’s top 10. Record 85 reuses record 83’s request.
- G record **90** chooses the earlier Ohio guarantee report G.e148.
- G record **128** chooses the earlier agentic-AI statement G.e81.
- E record **203** chooses Musk’s earlier stored exclusivity statement E.e479.

Other exceptions name evidence not linked to the destination, malformed incoming IDs, or an unrelated old record. They must not be labelled retrieval successes.

E records 83 and 84 have archive cost estimates of **$0.038485 and $0.039924**. Record 85 is not another independent paid sample. This illustrates both the cost of the failure and the need to deduplicate costs by archived request identity.

The [build log, row 8](/Users/lchingen/hivemind/docs/research/2026-10-25-english/build-log.md) documents the earlier rule correction allowing a target shown elsewhere in the request when it belongs to the destination thesis. That historical correction is not a new finding of this review.

**The revenue concentration is real; its entire count is not a semantic error count.**

At E’s July 31 cutoff, sequence 259:

- E.v2, NVIDIA Data Center revenue: **185 evidence items**.
- E.v1, NVIDIA total revenue: **148**.
- Their intersection: **99**.
- Their union: **234 of 411 evidence items**, or **56.9%**.
- Across the whole snapshot, **140/411** evidence items link to multiple theses.

The current field-level multi-link count differs from the build log’s historical 133/411. I report the fresh count with its explicit cutoff rather than treating the two measurements as interchangeable.

In G, **138/365**, or **37.8%**, link to multiple theses. Grouping has therefore not by itself removed evidence fan-out.

A concrete case is E.e122/e123, the $250bn guarantee and separate $350bn chip-financing reports. Both eventually link to the two NVIDIA revenue theses. Neither English snapshot contains a `financing_amount` thesis. On the initiating Reuters input, G retains only the aggregate-spending statement; E also retains the two financing statements under revenue.

This separates three problems:

1. Missing a material question.
2. Choosing where its evidence belongs.
3. Finding earlier evidence after that destination is chosen.

Retrieval directly addresses the third. A reranker cannot repair the first without taking over extraction’s responsibility. Nor should all indirect revenue evidence be declared wrong: the PRD explicitly conditions direct evidence handling on the available dependency structure.

**The completed grouped snapshot has five groups and 13 memberships.**

| Group | Members | Assessment |
|---|---|---|
| G.g1: infrastructure investment and Blackwell/Rubin rollout | v1, v4, v5, v12, v18, v19, v20, v39, v42 | F1 persists: one group combines an investment cycle and a product rollout. |
| G.g2: H200 China authorisation | v9 | Single-member group; permitted by the contract. |
| G.g3: Intel restructuring | v17 | Separate company-specific process. |
| G.g4: Taiwan AI-chip export ban consideration | v35 | Separate policy process. |
| G.g5: Amazon–Globalstar acquisition | v45 | Separate transaction. |

There are **32 ungrouped theses**. Ungrouped does not mean missing membership: company financial lines normally need no group.

The named checks are:

- **F4:** G.v13, standalone Vera CPU revenue, remains ungrouped.
- **SK and NAVER:** G.v18 and G.v19 both belong to G.g1. Their current raw extraction answers explicitly select `g1`; these are two current successes, not current misses.
- Their failures in the earlier `groups2` run remain historical findings from build-log rows 17–19.
- **F1:** G.g1 contains four rollout/deployment questions, three aggregate-spending questions and two company-specific capex questions. Correctly organising those questions cannot be judged merely by reproducing G.g1.

All 13 stored membership bases are `model`. Replaying the current alias predicate with creation-sequence visibility reproduces **9/13** stored memberships and adds **zero** other memberships. It misses v1, v19, v39 and v42. It also fails to add the ungrouped Vera CPU thesis.

Because model-selected membership is added first, `basis=model` can conceal an additional alias hit. The measured statement is therefore “nine memberships are independently reproducible by aliases,” not “aliases never ran.”

Sources: G `thesis_groups`, `thesis_group_members`, `handovers`; extraction archive calls **76, 107 and 109**; [alias implementation](/Users/lchingen/hivemind/src/hivemind/views/groups.py); [grouping acceptance contract](/Users/lchingen/hivemind/docs/research/2026-10-25-grouping-acceptance.md).

**2. Recall should be measured as a historical retrieval experiment, with separate labels for agreement and correctness.**

The current baseline has four different retrieval paths:

| Task | Current mechanism |
|---|---|
| Candidate thesis identity | Key-based candidates first; otherwise trigram search plus eligible extraction-context theses, truncated to configured top N |
| Evidence repeat/replacement | Word-overlap ranking within the destination thesis |
| Available research groups | Groups attached to the input’s objects, plus global lexical group search |
| Idea lookup | Embeddings plus lexical and object boosts; two subsequent model calls decompose and map the idea |

This follows [matching.py](/Users/lchingen/hivemind/src/hivemind/views/matching.py:134), [store.py](/Users/lchingen/hivemind/src/hivemind/views/store.py:276), [search.py](/Users/lchingen/hivemind/src/hivemind/search.py:221) and the [idea contract](/Users/lchingen/hivemind/docs/poc/idea-card.md). “Replace trigram search” alone would not describe the actual intervention.

Each retrieval query should have an identity such as:

`(ledger, input_id, sequence, matching pass, candidate_id)`

For evidence, add the incoming evidence ID and destination thesis ID. Keep attempts separately, while also reporting a deduplicated decision-level result.

Reconstruct the library **immediately before the decision**, including open/closed state and replacements. Do not embed a final-library view of group members or include future theses. For second-pass evidence matching, follow that pass’s actual eligibility rules.

The measurement should retain three label sets:

| Label set | Use | Limitation |
|---|---|---|
| Stored model choice | Measures agreement with the existing pipeline | Can preserve its mistakes |
| Trusted code identity | Measures whether complete, compatible identities remain findable | Requires version and provenance checks |
| Source-reviewed semantic judgment | Measures the desired product result | Must be checked with Alex before it becomes gold |

Only **20/45 G theses and 18/60 E theses** currently qualify for `automatic_key` under the implemented version-2 rule. C’s keys lack that version and cannot acquire automatic authority retroactively. Their information is still useful for comparison.

Critically, **all 825 inspected `match_records.written_json` values are null**. The POC cannot treat that column as the final outcome. Recover new-thesis mappings from `processing_steps` with `step='written'`, then inspect actual thesis, succession, evidence and membership rows. Apply recorded code overrides; raw `outcome='merge'` does not prove a merge happened.

For each query, output:

- Eligible target count and any missing prerequisite.
- Original own list and other context visible in the request.
- New ranks at k = 1, 3, 5, 10 and 20.
- Gold target set, or `new`, `uncertain`, `unsupported` or `not_exercised`.
- Whether the target was absent from recall, present but misranked, or present but wrongly classified.
- Representation version, source hashes, tokens, elapsed time and score components.

Use **any-correct-target recall** where alternatives are acceptable. Use **all-required-target recall** for multi-part questions. Report both; finding one spending thesis does not prove both 2026 and 2027 were retrieved.

“No existing match” needs its own precision measurement. Always returning a neighbour must not count as successful lookup.

**There is already a useful, limited $0 embedding result.**

The sealed index contains:

- **94 current vectors**, all matching the existing thesis-text hashes.
- **1,536 dimensions** per vector.
- **16,118 recorded thesis-token allocations**.
- **2,096 cached query vectors**, including all 20 gold idea texts.

The roughly 1,900-token figure in the task belongs to the English seed measurement: build-log row 5 records 15 views and 1,893 tokens. It is not the sealed 94-thesis index. Index token allocations are rounded per batch, so 16,118 is an approximate aggregate rather than a billing receipt.

I ran two read-only rankings against the cached vectors. The current search function received an embedder that raises if called; no embedding call occurred.

| Ranking | Hit@1 | Hit@3 | Hit@5 | Hit@10 |
|---|---:|---:|---:|---:|
| Pure cosine | 15/18 | 16/18 | 17/18 | 17/18 |
| Current hybrid search | 13/18 | 16/18 | 16/18 | 18/18 |

These are hits against the **model-authored** [idea gold](/Users/lchingen/hivemind/poc/eval/gold/idea-gold-2026-10-25.json), not end-to-end idea correctness.

Important individual results:

- Gold #5’s designated Vera-revenue thesis ranks **21st by cosine and sixth by hybrid**.
- Gold #15’s designated thesis ranks second; a deployment event ranks first.
- Hybrid search moves the gross-margin target from first to third and TSMC capex from first to second.
- Both queries labelled uncovered return candidate lists. Search coverage and direct-answer suitability remain different judgments.

Gold #5 itself needs correction or confirmation: it asks about **Rubin revenue**, while its designated S.v48 is supported by a **Vera CPU** forecast. The [probe file](/Users/lchingen/hivemind/poc/eval/idea-probes-2026-10-24.json) is also explicitly an analyst reading, not gold.

Existing vectors additionally show why a universal similarity threshold is unsafe:

- S.v16/S.v48, the CPU duplicate candidate: cosine **0.879**.
- S.v1/S.v89, different years: **0.894**.
- S.v72/S.v89, potentially different spending scopes: **0.958**.

A higher score does not imply stronger identity.

For the stored matching decisions, the answer is still **unmeasured**: none of the 325 handover candidates has its exact baseline query text in the query cache. The sealed vectors use object, kind, focus, question and rung conditions; they do not supply embeddings for the proposed question–focus–key representation. Using a newly created thesis vector as its earlier candidate query would silently change the experiment.

**3. Deduplication needs a permissive search representation and a strict identity decision.**

Use two explicitly versioned representations:

```text
Recall text
  object name and identifier
  question
  focus
  measure and scope
  explicit period start/end
  basis, unit and event type

Comparison record
  all of the above
  key version and scope provenance
  ladder and due date
  relevant initiating quotation and source identity
```

Run a text-only arm and a key-enriched arm. Adding labels to an embedding does not make the model enforce them. Compare their measured retrieval quality rather than assuming the richer string wins.

Keep these decisions in code where the current contract already determines them:

| Comparison | Decision |
|---|---|
| Different explicit accounting bases | Not identical |
| Level versus growth; USD versus percent | Not identical |
| Different periods | Not a merge; test succession separately |
| Launch versus shipment versus deployment | Not identical |
| Different code-owned scopes | Not identical |
| Complete, trusted version-2 automatic keys agree | Preserve the current deterministic identity rule |
| Free scope wording differs, or a field is ambiguous | Retrieve for comparison; do not infer equality or inequality from spelling alone |

This is the practical meaning of D154’s “necessary, not sufficient” boundary. Literal equality of free-text scopes is not a prerequisite for finding a semantic duplicate. Conversely, compatible fields do not establish that two loosely defined questions are identical.

The semantic comparator should distinguish:

`same quantity/event`, `narrower or broader`, `related`, `different`, `insufficient information`.

Those labels feed the existing merge/new/succession rules. A general relevance score cannot stand in for them. In particular, treating “part of” as “same” recreates the Amazon-capex and segment-revenue mistakes.

The initiating quotation matters in S.v16/S.v48: the thesis wording alone suggests broad versus narrow revenue, while the evidence explains that both refer to standalone CPU sales. This can be tested by adding already stored source material to the comparison record; it requires no extraction-contract change.

For evidence, represent **who asserted what, about which event or quantity, for which period, and when**. Preserve the original source separately from the publisher retelling it. A repeated estimate, a revised estimate and an official denial may be very close embeddings but require three different actions.

A cross-encoder can rank these pairs. It cannot be assumed to classify them reliably without labels. Its sigmoid score is not a calibrated probability of identity.

**4. Grouping should be tested as source-supported membership, with clustering used to diagnose broad groups.**

The current alias rule is a valuable baseline because it is cheap and inspectable. Its limits are now measurable:

- It reproduces 9/13 current memberships.
- It misses NAVER despite explicit Rubin/Blackwell language in the source.
- It misses Vera CPU because neither the thesis text nor the stored aliases supplies the necessary connection.
- It cannot split G.g1’s two matters.

Test membership using:

```text
thesis question + focus + key
    against
group name + scope + aliases + historically available member questions
```

Then run a separately labelled, source-assisted arm adding the relevant original passage. Do not claim that a thesis-text-only model recovered a relationship that was supplied in the passage.

The source evidence is explicit:

- SK’s press release says the factory will deploy Vera Rubin.
- NAVER’s press release says the infrastructure will include Vera Rubin and Blackwell.
- The NVIDIA transcript identifies Vera CPU as a Rubin-platform component.

A source-assisted local reranker may recover all three without a generative call. That is a testable hypothesis. A model that answers from remembered product knowledge alone has not established a source-supported membership.

Grouping must allow **zero, one or several memberships**. Nearest-centroid assignment to exactly one cluster would violate the contract. NVIDIA affiliation alone must not pull RTX Spark or an unrelated product into Rubin.

For F1, use the nine G.g1 members as a small diagnostic:

- Rollout/deployment candidates: v4, v5, v18, v19.
- Aggregate investment candidates: v1, v12, v20.
- Company capex cases needing an explicit membership judgment: v39, v42.
- Missing candidate to evaluate: v13.

Compare pairwise similarities and a hierarchical sub-clustering with an owner-reviewed division into matters. Do not require two clusters merely because two were requested in the hypothesis. Record whether the split is stable when one member is removed and whether a bridge thesis legitimately belongs to both matters.

A reranker evaluated against the present broad G.g1 may reproduce F1 perfectly. That is why stored-membership agreement and desired membership quality need separate columns.

**No split should be written by this POC.** D149 assigns association during extraction; the existing design has no settled post-creation group-split operation. Any later operation needs a decision about group identity, historical membership and future reads. An offline proposed split is useful evidence for that decision, not permission to perform it.

For scalability, reuse member-thesis vectors. Embed the group description separately and retrieve a few relevant member examples for comparison. Re-embedding a growing concatenation of every member would make both cost and group meaning drift on every addition.

**5. One evening can answer whether this direction is promising, not whether it is production-ready.**

The smallest implementation is an offline evaluator with exact vector scans. At 45–94 theses per ledger, an approximate-nearest-neighbour service would add an unnecessary variable.

| Stage | Inputs and work | Outputs | Estimated time and new API cost |
|---|---|---|---|
| A. Freeze and reconstruct | Completed snapshots; all 825 matching records; handovers, write records and archives | Manifest, decision table, original recall lists, exception classes | 30–45 min; $0 |
| B. Fix the measuring stick | All 52 G candidate cards; 45 G thesis/group cards; 40 stratified evidence decisions; named C/S regressions; existing idea labels | Source-backed labels with required/optional/forbidden relations and unresolved cases | 60–120 min; $0 |
| C. Offline controls | Original lists, exact keys, current aliases, cached idea embeddings | Baseline recall, identity and membership tables; positive controls | 30–45 min; $0 |
| D. New recall | Text-only and key-enriched representations; G/E first; Chinese strata separately | Exact top-k results and per-case rank changes | 20–40 min; embedding estimate below |
| E. Reranking | One local cross-encoder; optionally 24 paired generative comparisons | Error reasons, abstention coverage, paired cost and stability | 30–60 min locally; optional paid arm separately bounded |
| F. Decision report | Frozen test configuration, all failures and unstarted cases | Six-layer acceptance report and a go/no-go recommendation | 30 min |

The timing is an estimate. If label review consumes the evening, stop with a valid baseline. Do not replace missing labels with model agreement to finish on schedule.

The 40 evidence cards should include 20 repeats, all four accepted G replacement decisions, and 16 new decisions, with hard negatives selected from the same story. Retellings of one story stay in one split.

Use known Ohio/Rubin failures for development. Hold out entire other story families and later inputs for the frozen test. Parallel Chinese and English versions of the same source must stay together. These are holdouts for implementation choices, not an untouched external benchmark.

The retrieval arms should be small:

1. Current candidate lists.
2. Exact-key candidates alone.
3. Dense text recall.
4. Dense key-enriched recall.
5. A union of required key candidates, lexical candidates and dense candidates, ranked with a fixed fusion rule.

Keep known exact identities outside a lossy top-k competition. Preserve broad retrieval for free scopes. Select one representation and fusion configuration on development data, then score the held-out set once.

For local models, **BAAI/bge-m3** is a reasonable multilingual embedding comparison; its model card specifies 1,024-dimensional vectors and up to 8,192 tokens. **BAAI/bge-reranker-v2-m3** supplies a multilingual query–passage relevance score. Neither model card establishes financial identity accuracy. Pin the revision and inference settings, and measure local latency rather than borrowing benchmark claims. [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3), [reranker model card](https://huggingface.co/BAAI/bge-reranker-v2-m3).

For the first API embedding arm, use **`text-embedding-3-small`**, matching the existing index. Reserve `text-embedding-3-large` for a predeclared comparison if the smaller model’s specific failures justify it. Current published standard prices are **$0.02 and $0.13 per million input tokens** respectively. [Small model pricing](https://developers.openai.com/api/docs/models/text-embedding-3-small), [large model pricing](https://developers.openai.com/api/docs/models/text-embedding-3-large).

The stored-text volume is small:

| Representation population | Approximate tokens |
|---|---:|
| G: 45 theses + 52 candidates, key-enriched | 6,810 |
| E: 60 theses + 75 candidates, key-enriched | 9,661 |
| C: 40 theses + 61 candidates, key-enriched | 10,423 |
| S: 94 theses + 137 candidates, key-enriched | 23,651 |
| All four, one representation | 50,545 |
| All stored and incoming evidence, with summaries, quotes and provenance | 537,896 |

These are estimates from measured character volumes: ASCII characters divided by four, plus 1.5 tokens per non-ASCII character. They are not tokenizer measurements or billed usage. They deliberately precede cross-ledger text deduplication.

Allowing **one million tokens** covers the proposed representations, evidence and reasonable overhead:

- Small embeddings: about **$0.02**.
- Large embeddings: about **$0.13**.
- Proposed first-stage small-embedding cap: **$0.05**.

Local inference has no API fee, but consumes setup time, memory and compute. It should not run alongside an active paid ingestion run.

**The matching cost baseline needs two price columns.**

Joining matching records to archives by request hash gives:

| Snapshot | Unique archived matching requests | Input/output tokens | Archive cost estimate | Mean estimate/request | Median / p95 seconds |
|---|---:|---:|---:|---:|---:|
| G | 144 | 1,131,213 / 127,417 | $2.6882 | $0.01867 | 7.75 / 23.8 |
| E | 208 | 1,595,147 / 187,554 | $3.8695 | $0.01860 | 7.3 / 21.7 |
| C | 155 | 1,002,103 / 146,262 | $2.7152 | $0.01752 | 9.1 / 26.8 |

These archive amounts use [model.py’s](/Users/lchingen/hivemind/src/hivemind/model.py:26) fixed rates of $1.25/M input and $10/M output for `gpt-6-luna`; they are estimates, not invoices.

The current official page instead lists **$0.10/M input and $0.50/M output**. At those standard rates, without cache discounts, G’s same token volume would be about **$0.1768 total**, or **$0.00123 per request**. Do not mix that repricing with the historical estimate and call the difference an algorithmic saving. [Current GPT-6 Luna pricing](https://developers.openai.com/api/docs/models/gpt-6-luna).

An illustrative listwise reranker decision using **1,500 input and 200 total output tokens** costs:

- **$0.003875** under the repository’s accounting rates.
- **$0.00025** under the current published standard rates.

Actual reasoning tokens must be included. Calling an LLM separately for ten pairs can erase the saving. Also, a current matching request often decides several evidence pairs and dependencies; a one-decision reranker is not a like-for-like replacement.

If authorised, compare **24 inputs × three fresh samples × two arms = 144 requests**: unchanged current control versus the selected reranking intervention. Allocate 12 development and 12 held-out inputs, retaining every refusal. Expected cost under the conservative historical accounting is roughly $1.6; propose a **$3 total cap**, checked against the actual selected requests and output ceilings before launch. If that cap cannot cover the registered workload, return to Alex rather than shrink or raise it silently.

Use separate archives per fresh replicate so stored-answer caching cannot masquerade as repeated sampling. Do not change the provider or model as part of the comparison.

**The following are proposed acceptance numbers for Alex to approve, not adopted product gates.**

| Layer from the governing acceptance contract | Proposed evening criterion |
|---|---|
| Content coverage | No loss of labelled important content in the tested path. Missing candidate creation remains visible and is not credited to retrieval. |
| Membership meaning | All registered required relations recovered; zero forbidden relations. Report unreviewed and optional relations separately. |
| Thesis identity | Zero false merges on explicit basis/unit/period/event negatives; recover every registered duplicate regression. Report automatic-decision coverage and abstentions. |
| Evidence fidelity | Zero false repeat/replacement decisions on reviewed hard negatives; preserve every source reference. The disjoint-thesis SSI case is reported separately if the allowed search boundary cannot reach it. |
| Sequential behaviour | Zero future-target leakage; exact reconstruction of tested candidate and membership visibility; missing prerequisites fail the evaluator. |
| Stability and cost | Recall@10 at least 95%, Recall@20 at least 99% on reviewed eligible targets, with exact counts; no loss of a critical target versus control. Three fresh model samples must satisfy critical cases individually. Proposed warm retrieval p95 ≤100 ms and local top-20 reranking p95 ≤2 s on the actual machine. |

For small positive denominators, the recall percentages effectively require every target. If a stratum has no positives, report **unexercised**. Do not average a wrong merge away with many easy “new” decisions.

A stringent combined gate can fail a noisy control by chance. For illustration, 36 independent decisions each correct with probability 0.95 all pass only about 16% of the time. Measure fresh control against fresh control before interpreting a combined pass/fail. Repeated calls and related articles are correlated, so they do not create 36 independent business cases.

A negative result is still useful:

- Dense recall fails to recover source-reviewed targets already found by the baseline.
- A reranker ranks related but wrong quantities above the correct one.
- Improvements depend on manually inserting “Vera” or other test-specific aliases.
- Grouping only reproduces the broad G.g1.
- The system achieves zero errors only by abstaining on nearly everything.
- Savings disappear once all matching responsibilities and fallbacks are included.
- Gold disagreements remain unresolved.

Any failed registered acceptance stops that line. Read and classify the reasons before proposing another configuration, as required by [AGENTS §§6–7](/Users/lchingen/hivemind/AGENTS.md).

**The evaluator needs a small contract before implementation.**

| State/event | Required behaviour |
|---|---|
| Input database is still receiving writes | Use the frozen sequence cutoff; verify selected-row digests before and after |
| Missing archive, source or write mapping | Mark incomplete and exclude from success claims; do not infer an answer |
| No eligible earlier destination | Label a new-item case, not a recall success |
| Embedding or reranking fails | Retain the failure and denominator; do not silently substitute another method |
| Configuration or representation changes | Create a new named result set; never overwrite the control |
| Run is interrupted and resumed | Resume pending work by manifest/query identity; preserve completed results |
| Test stage completes or fails | Seal its configuration and result; no automatic next arm |

The manifest feeds every stage. Query representations feed only retrieval. Gold labels feed only scoring, never query construction. Rankings feed the comparator. Proposed decisions feed an offline comparison report, never the product ledger.

Before paid work, run the required stored-answer preflight. Before any future integration, preserve existing source, allowed-target, identity, succession, dependency-cycle, replacement-date and historical-read checks. A changed shortlist changes the request; a cached old answer can test the evaluator but cannot establish the new model behaviour.

**6. The principal limits concern information and authority, not vector storage.**

- **Historical leakage:** filter by arrival sequence, not the model’s calendar knowledge or the final database. Member examples, evidence and aliases must also be historically available. Model knowledge may suggest a relationship, but only supplied contemporary sources can justify it.
- **Small and dependent samples:** one week, one dominant company and repeated outlets do not establish market-wide reliability. Report results by story, task, language and key provenance. Zero errors in 30 independent cases still permits roughly a 10% error rate under the usual “rule of three” approximation.
- **Mixed languages:** test English→English, Chinese→Chinese and cross-language retrieval separately. Never use a shared local `v1` as identity across ledgers. Do not translate stored source text or treat cross-language similarity as identity proof.
- **Re-embedding cost:** immutable thesis text needs embedding once per model and representation version. Evidence arrivals should not re-embed its thesis. The existing hash-based design already supports this. Group descriptions and changing member context need separate versioning.
- **Lost distinctions:** averaging vectors can blur period, scope and accounting basis. Exact fields remain outside the similarity score.
- **Remaining LLM work:** deciding which uncovered matters warrant theses; understanding unresolved scope differences; assessing materiality; interpreting ambiguous revisions and source authority; choosing dependencies; and judging evidence against a ladder remain semantic work until separately validated.
- **Retrieval cannot supply missing facts:** if extraction omitted financing content or stored an incorrect period, a better rank cannot make the record correct.

**Only the following choices need Alex’s decision.** File placement, report fields and evaluator organisation are implementation choices.

| Choice | Options and recommendation |
|---|---|
| What constitutes the semantic gold? | Approve or revise the CPU and financing duplicate labels, spending-scope distinctions and idea #5. **Recommend resolving these before scoring a new arm.** |
| What may the first POC change? | Shadow retrieval only, or automatic decisions. **Recommend shadow retrieval and offline decision proposals; keep the current pipeline authoritative.** |
| May evidence recall cross thesis boundaries? | Preserve within-thesis search, or test a narrow provenance-aware lookup for already stored statements. **Recommend testing the narrow lookup offline against SSI, without authorising broad semantic merging.** |
| What should happen to a group containing two matters? | Leave it as stored, or design a historically versioned split operation. **Recommend an offline proposed split first; no ledger mutation.** |
| Which next-stage budget is authorised? | $0 controls only; add small embeddings capped at $0.05; optionally add the paired reranker arm capped at $3. **Recommend embeddings after label approval, with generative reranking conditional on the measured remaining error class.** |

For reproducibility, the main counts come from `SELECT … WHERE <table sequence> <= cutoff`, JSON parsing of exact candidate/evidence IDs, and joins through actual input IDs. No substring match was used to decide whether a target belonged to a shown list.

Selected-row SHA-256 prefixes, computed from `ORDER BY rowid` rows serialised with sorted JSON keys, UTF-8 and compact separators, identify the reviewed matching snapshots:

| Snapshot | `views` digest prefix | `match_records` digest prefix |
|---|---|---|
| G | `2cc9e162785a961d` | `79440ee787e7772d` |
| E | `adb37b150d59394f` | `6ff3df515b5cc301` |
| C | `3965d28a671e42a4` | `ee74e3774afdcd3f` |
| S | `4efd776bfeaef5bd` | `65884e29bbbc8294` |

The historical experiment results cited here remain attributed to their documents. The new measurements are the bounded database census, exact-list comparisons, alias replay, cached-vector rankings and token-volume estimates described above.