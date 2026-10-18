# Agent memory systems: maintaining a store from a stream with add / update / delete / no-op (embedding candidates + LLM decision)

Scope note. Researched 2026-10-17. Code was read directly from shallow clones of the official repositories at these commits (file paths and line numbers below refer to them):
mem0 `0724291` (2026-10-14) and the last classic release tag `v1.0.11`; graphiti `d50741d` (2026-10-15); A-mem (agiresearch) `ceffb86` (2025-12-12); langmem `48e3c11` (2026-10-02); cognee `37f788b` (2026-10-16); MemoryOS `587ed77` (2026-07-07); letta `5bcdd17` (2026-09-10, landing page only).
"Vendor-reported" marks numbers published by the vendor of the system that scored them.

## 1. Mem0: the extraction → retrieval → ADD/UPDATE/DELETE/NOOP pipeline, Mem0g, LoCoMo results and the disputes

### Takeaway
The pipeline described in the Mem0 paper (two LLM calls: extract facts, then decide ADD/UPDATE/DELETE/NOOP for each against the top similar memories) is no longer what Mem0 ships. On 2026-04-14 Mem0 replaced it with a single LLM call that only adds memories ("nothing is overwritten or deleted"), plus hybrid retrieval. Its stated reason was that UPDATE/DELETE destroyed history and handled changes badly. Contradiction and duplicate handling moved to a closed "Dream" layer on the hosted Platform that supersedes or merges memories without deleting them. Mem0's LoCoMo numbers are vendor-reported and were disputed by both Zep and Letta.

### Cited Findings

**Paper mechanism (arXiv 2504.19413, April 2025)**
- Extraction prompt P = (conversation summary S, last m messages, new message pair). The paper uses m = 10 previous messages and s = 10 similar memories. All LLM operations used GPT-4o-mini with function calling. — [Mem0 paper](https://arxiv.org/html/2504.19413)
- Update phase: for each candidate fact, retrieve the "top s semantically similar memories using vector embeddings" and present them to the LLM through function calling. The four operations are "ADD for creation of new memories when no semantically equivalent memory exists; UPDATE for augmentation of existing memories with complementary information; DELETE for removal of memories contradicted by new information; and NOOP when the candidate fact requires no modification". The LLM chooses the operation directly; there is no separate classifier. — [Mem0 paper](https://arxiv.org/html/2504.19413)
- Mem0g (graph variant): an entity extractor plus a relationship generator produce triplets. Nodes are matched by embedding similarity above a threshold t. A "conflict detection mechanism identifies potentially conflicting existing relationships", and "an LLM-based update resolver determines if certain relationships should be obsolete, marking them as invalid rather than physically removing them". — [Mem0 paper](https://arxiv.org/html/2504.19413)

**Classic open-source code (tag v1.0.11, the last 1.x before the rewrite)**
- After fact extraction, each new fact is embedded and searched with `limit=5` (not s = 10 as in the paper), scoped by user_id / agent_id / run_id. Results are deduplicated by id. UUIDs are then mapped to "0", "1", … "for handling UUID hallucinations" before one update call (`get_update_memory_messages`) with `response_format=json_object`. — [mem0 v1.0.11 main.py L555-L592](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/main.py#L555-L592)
- Event handling: ADD creates a new uuid. UPDATE overwrites text and embedding under the same id (`_update_memory`). DELETE calls `vector_store.delete(vector_id)`, a hard delete from the searchable store, and writes a SQLite history row (old value, `event="DELETE"`, `is_deleted=1`). NONE only refreshes agent_id / run_id. — [mem0 v1.0.11 main.py L620-L690, L1340-L1364](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/main.py#L1340-L1364)
- The update prompt (`DEFAULT_UPDATE_MEMORY_PROMPT`) defines four cases by example:
  - UPDATE if the information "is already present in the memory but the information is totally different". If two items convey the same thing, "keep the fact which has the most information".
  - Example: "Likes cheese pizza" vs "Loves cheese pizza" → no update.
  - Example: "I really like cheese pizza" + "Loves chicken pizza" → UPDATE to "Loves cheese and chicken pizza".
  - DELETE if a retrieved fact "contradicts the information present in the memory". Example: "Loves cheese pizza" + "Dislikes cheese pizza" → DELETE.
  - Source: [mem0 prompts.py L176-L325](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/configs/prompts.py#L176-L325). The prompt is still in the file but is no longer called from the add path.
- Mem0g code (v1.0.11):
  - Graph search keeps nodes whose cosine similarity is ≥ `threshold` (default 0.7) and walks their valid relations.
  - The LLM gets `DELETE_RELATIONS_SYSTEM_PROMPT`. It deletes a relation only if it is "Outdated or Inaccurate" or "Contradictory", with the rule "DO NOT DELETE if their is a possibility of same type of relationship but different destination nodes" (example: alice loves_to_eat pizza + "also loves burger" → keep both).
  - Source/destination node matching uses a 0.9 default threshold.
  - Delete was turned into a soft delete, `SET r.valid = false, r.invalidated_at = datetime()`, "enabling temporal reasoning over historical graph state" (issue #4187).
  - Sources: [graph_memory.py L73-L95, L294-L335, L420-L432](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/graph_memory.py#L420-L432); [graphs/utils.py L57-L97](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/graphs/utils.py#L57-L97)

**The 2026 rewrite (current code and docs)**
- Changelog, 2026-04-14 (SDK v2.0.0 / v3.0.0), "New Memory Algorithm":
  - "ADD-only extraction: Memories accumulate; nothing is overwritten or deleted."
  - "Hybrid retrieval: Semantic search, BM25 keyword search, and entity boost"
  - External graph stores were removed from the open-source SDK.
  - Vendor-reported scores: LoCoMo 71.4 → 91.6, LongMemEval 67.8 → 93.4, BEAM (1M) 64.1.
  - Source: [mem0 docs/changelog/highlights.mdx L222-L240](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/changelog/highlights.mdx)
- Stated rationale: "The previous algorithm could UPDATE or DELETE existing memories during extraction. The new algorithm only adds new facts. When information changes (e.g., a user moves from New York to San Francisco), both facts are preserved with temporal context." The listed effects are "More memories over time … Better temporal reasoning … No information loss: facts that seemed contradictory but were actually complementary are preserved". Keeping memory counts low is now handled "at retrieval time instead". The old pipeline is described as "Two LLM passes (extract + merge)"; the new one as "Single-pass ADD-only (one LLM call)". — [mem0 docs/migration/platform-v2-to-v3.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/migration/platform-v2-to-v3.mdx); [oss-v2-to-v3.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/migration/oss-v2-to-v3.mdx)
- Current open-source add path ("V3 PHASED BATCH PIPELINE"):
  1. Embed the whole new message batch and fetch `top_k=10` existing memories in scope.
  2. Map them to integer ids.
  3. Make one LLM call with `ADDITIVE_EXTRACTION_PROMPT`, given the summary, up to 20 recently extracted memories, the existing memories, the last-k messages, the observation date and the current date.
  4. Drop any extracted text whose MD5 hash equals the hash of a retrieved memory or of another item in the batch. This is exact-text deduplication only.
  5. Insert the rest as new records with `event: ADD`.
  - Entity linking: spaCy entities are matched to an entity store by exact normalized text or by vector score ≥ 0.95, with `linked_memory_ids` kept on the entity.
  - Source: [main.py L918-L1220](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/main.py#L918-L1220)
- In the additive prompt, semantic deduplication is delegated to the LLM. Existing memories are "ONLY for deduplication and linking … If new information … is semantically equivalent to an Existing Memory with no meaningful new context, skip it". It also tells the model "When in doubt, extract. A slightly redundant memory is far less costly than a missing one. The deduplication system downstream will handle true duplicates". The model is asked to output `linked_memory_ids` for related memories, including the case "Contradiction: New information that conflicts with an existing memory". — [prompts.py L468-L946 (L511, L578, L692-L700)](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/configs/prompts.py#L468-L946)
- Code observation: in the Python open-source add path at this commit, the per-memory `linked_memory_ids` returned by the LLM is never persisted. Only `text` and `attributed_to` are copied into the payload. Every `linked_memory_ids` write in main.py is on entity-store records. So the LLM's contradiction links are discarded. — [main.py L1007-L1040, L1100-L1200](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/main.py#L1007-L1200)
- Current retrieval: semantic search over-fetches `max(top_k*4, 60)`. Then BM25 (normalized by a sigmoid) and an entity boost (entity similarity ≥ 0.5, weight 0.5, damped by how many memories the entity links to) are added. The combined score is `(semantic + bm25 + entity)/max_possible`. The semantic score must pass `threshold` (default 0.1) before combining. — [main.py L1646-L1700](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/main.py#L1646-L1700); [utils/scoring.py L57-L130](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/utils/scoring.py#L57-L130)
- Platform "Dream" (closed source, documented only):
  - Supersede, always on and evaluated at add time: "Marks an older fact as outdated when a newer one contradicts it" and links it to the newer fact. Superseded memories "are not deleted and not hidden by default".
  - Merge, always on: "Folds a duplicate into a single canonical memory". The merged record is "hidden from reads by default … retained rather than deleted".
  - Synthesis, opt-in: writes pattern memories that link back to their source memories.
  - Read modes: default returns active + superseded; `latest_only=true`; `include_merged=true`.
  - "Nothing Dream does is destructive … Every change is recorded and reviewable."
  - Source: [mem0 docs/platform/features/dream.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/platform/features/dream.mdx)
- Memory Decay (Platform, 2026-05-08): a search-time recency/usage bias clamped to 0.3×–1.5×, described as "Soft bias, never a filter". — [mem0 changelog L209-L220](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/changelog/highlights.mdx)

**LoCoMo results (paper, vendor-reported, GPT-4o-mini, adversarial category excluded "because ground truth answers were unavailable")**

| System | LLM-judge J (overall) |
|---|---|
| Mem0 | 66.88 ± 0.15 |
| Mem0g | 68.44 ± 0.17 |
| Zep | 65.99 ± 0.16 |
| LangMem | 58.10 |
| OpenAI memory | 52.90 |
| A-Mem | 48.38 |
| Best RAG | 60.97 |
| Full context | 72.90 |

- Per category:
  - Mem0: single-hop 67.13, multi-hop 51.15, open-domain 72.93, temporal 55.51
  - Mem0g: temporal 58.13
- Latency, p95 total: Mem0 1.44 s; Mem0g 2.59 s; Zep 2.93 s; LangMem 60.40 s; full context 17.12 s.
- Memory footprint per conversation: Mem0 ~7k tokens; Mem0g ~14k; Zep 600k+; full conversation 26k.
- Source: [Mem0 paper](https://arxiv.org/html/2504.19413)
- Note that full context (72.90) beats every memory system in Mem0's own table.

**Criticisms and rebuttals**
- Zep, 2025-05-06: says Mem0 misconfigured Zep in three ways.
  1. It assigned the user role to both speakers, "treating it as a single user whose identity changed with each message".
  2. It appended timestamps to messages instead of using `created_at`.
  3. It ran searches sequentially instead of in parallel, inflating latency.
  - Zep's corrected result (vendor-reported): J = 75.14 ± 0.17, p95 search latency 0.632 s.
  - Zep's critique of LoCoMo itself: 16k–26k-token conversations fit in context; category 5 lacks ground truth; it contains multimodal and speaker-attribution errors; and full context beats Mem0. Zep recommends LongMemEval instead (about 115k tokens, with explicit knowledge-update questions).
  - Source: [Zep blog](https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/)
- Letta, 2025-08-12: says it could not reproduce how Mem0 backfilled LoCoMo into MemGPT/Letta and that Mem0 "did not respond". A Letta agent with plain file tools (grep / search_files / open / close) on GPT-4o-mini scored 74.0% on LoCoMo, against Mem0's best graph result of 68.5%. Letta's conclusion: memory quality depends more on "whether an agent will be able to effectively use a retrieval tool" than on the retrieval mechanism. — [Letta blog](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- Practitioner report (secondary): Mem0's resolver "runs on text similarity, not on your application's notion of scope". It "cannot tell the difference between 'the user changed their mind' and 'the user has two preferences that both hold, just in different contexts'", and when wrong it "quietly issues a DELETE". The same report notes that UPDATE and retraction are not the same operation. — [DEV Community post (search summary; page fetch failed on TLS)](https://dev.to/mukesh_13/mem0-auto-resolves-memory-conflicts-for-you-until-it-silently-deletes-one-you-still-need-4f4m)
- Memory-R1 gives the canonical false-contradiction example. "The user mentions adopting two dogs across sessions" and "the vanilla Memory Manager misinterprets this as a contradiction and issues DELETE+ADD, fragmenting memory"; an RL-trained manager issues one UPDATE instead. — [Memory-R1](https://arxiv.org/html/2508.19828v4)

### Inferences
- Mem0's own path is the strongest evidence that letting the LLM DELETE or UPDATE in place on a similarity-retrieved neighbourhood is fragile. It moved to append plus non-destructive supersede/merge flags. This matches our rule that closed views are kept and never deleted.
- In Mem0's old design, UPDATE meant "merge more detail into the same id and rewrite the text". In our design that would break the rule that a claim is never reworded. The analogue for us: UPDATE = attach evidence or change status, never rewrite the claim; a reworded claim = a new view plus a `superseded_by` link.
- The current open-source code sees only top-10 existing memories retrieved by embedding the whole input batch, and its only mechanical dedup is exact MD5. Semantic duplicates rely on the LLM noticing them among those 10. For a views store fed by a stream of long documents, recall of the correct existing view would be poor without structured candidate keys (object × driver).
- The UUID → integer remapping (old and new code) is a cheap guard worth copying. So is Graphiti's validation of returned idx ranges.

### Gaps
- How Dream's add-time Supersede/Merge works (prompt, candidate count, thresholds) is not public. No precision/recall is published for it.
- The vendor-reported v3 scores (LoCoMo 91.6, LongMemEval 93.4) have no independent reproduction that I found. One search summary claimed "not one number in agent memory has been independently reproduced" and mentioned a 25.56-point arithmetic error in a headline score. I could not locate the primary source (FutureAGI's page does not contain it), so treat it as unverified.
- The Mem0 paper says s = 10 similar memories but the v1.0.11 code uses limit = 5 per fact (deduplicated across facts). I did not find which configuration produced the paper's numbers.

## 2. Graphiti / Zep: entity resolution, fact (edge) deduplication, bi-temporal invalidation, reported accuracy and latency

### Takeaway
Graphiti is the most complete public reference for "never delete, invalidate":
- Candidates are found by structure first (same entity pair for duplicates), then by hybrid BM25 + cosine search.
- One small-model LLM call returns both `duplicate_facts` and `contradicted_facts` as index lists.
- Deterministic date code then decides which edge expires, using `valid_at` / `invalid_at` (when the fact held in the world) and `created_at` / `expired_at` (when the system learned and retired it). This includes the case where facts arrive out of order.
- Bulk ingestion skips invalidation, so correctness depends on sequential ingestion.

### Cited Findings

**Paper (arXiv 2501.13956, January 2025)**
- Two timelines. T is the chronological order of events; T′ is the order in which Zep ingested data. Edges carry t′_created / t′_expired (system) and t_valid / t_invalid (world). — [Zep paper](https://arxiv.org/html/2501.13956)
- Entity resolution in the paper:
  - Embed names (1024-dim) and run cosine search, plus "separate full-text search on existing entity names and summaries".
  - The LLM sees the current message plus the last n = 4 messages.
  - Edge deduplication is "constrained to edges existing between the same entity pairs".
  - Contradiction: an LLM compares new edges with "semantically related existing edges". "When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge."
  - Source: [Zep paper](https://arxiv.org/html/2501.13956)
- Results (vendor-reported):
  - DMR: Zep 94.8% vs MemGPT 93.4% with gpt-4-turbo; Zep 98.2% with gpt-4o-mini.
  - LongMemEval: gpt-4o-mini 63.8% vs 55.4% full context; gpt-4o 71.2% vs 60.2%. Average context 1.6k tokens vs 115k, with about 90% lower latency.
  - Per type (gpt-4o): knowledge-update 83.3 vs 78.2; temporal-reasoning 62.4 vs 45.1; single-session-assistant 80.4 vs 94.6 (−17.7%, acknowledged as a limitation).
  - Source: [Zep paper](https://arxiv.org/html/2501.13956)

**Current code (graphiti `d50741d`, October 2026)**
- Edge model fields: `fact`, `fact_embedding`, `episodes` (the list of source episode uuids, i.e. provenance), `valid_at`, `invalid_at`, `expired_at`, `reference_time`, `attributes`. — [graphiti_core/edges.py ~L264-L290](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/edges.py)
- Edge resolution (`resolve_extracted_edges`):
  1. Fast path: collapse edges in the same batch that share (source, target, normalized fact), including same-type reverse direction.
  2. Duplicate candidates: hybrid search `EDGE_HYBRID_SEARCH_RRF` (BM25 + cosine, RRF rerank) filtered to edges whose endpoints are both in {a, b}, then post-filtered to the exact pair.
  3. Invalidation candidates: a second hybrid search over the whole group with no endpoint filter, minus the duplicate candidates.
  4. Default search limit is 10; default cosine min score is 0.6.
  - Sources: [edge_operations.py L399-L646](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L399-L646); [search_config.py L29](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/search/search_config.py); [search_utils.py L64-L65](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/search/search_utils.py)
- If the new fact text and endpoints already exist verbatim, the existing edge is reused and the episode uuid is appended to `episodes`. No LLM call is made. — [edge_operations.py L940-L950](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L864-L1087)
- The single LLM prompt `dedupe_edges.resolve_edge` (run on `ModelSize.small`) shows EXISTING FACTS (same pair) and FACT INVALIDATION CANDIDATES with continuous idx numbering, and returns a Pydantic `EdgeDuplicate{duplicate_facts, contradicted_facts}`. Key rules:
  - System prompt: "NEVER mark facts as contradicted unless the new fact explicitly makes the old fact false."
  - "NEVER mark facts as duplicates if they have key differences, particularly around numeric values, dates, or key qualifiers."
  - "A contradiction requires explicit evidence that the old fact stopped being true or was replaced … Do NOT infer contradiction from recency alone, episode dates, meeting dates, weekly snapshots … or a new event involving the same entities."
  - Example: "works … as a software engineer" → "as a senior engineer" counts as a contradiction, not a duplicate; "ran 5 miles Tuesday" vs "ran 3 miles Wednesday" is neither.
  - Code then drops out-of-range idx values with a warning.
  - Sources: [prompts/dedupe_edges.py L25-L110](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/prompts/dedupe_edges.py); [edge_operations.py L864-L1087](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L864-L1087)
- Deterministic temporal resolution (`_apply_temporal_invalidation`, `resolve_edge_contradictions`), applied only to edges the LLM flagged as contradicted:
  - If the new edge already has `invalid_at`, it is historical, so `expired_at = now`.
  - If a contradicted candidate has a later `valid_at` than the new edge, the new edge is the stale one: its `invalid_at` is set to the candidate's `valid_at`. This handles out-of-order arrival.
  - Otherwise, a candidate whose `valid_at` is earlier than the new edge's gets `invalid_at = new.valid_at` and `expired_at = now`.
  - Edges whose validity intervals do not overlap are left untouched.
  - Nothing is deleted.
  - Source: [edge_operations.py L715-L783](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L715-L783)
- Future-tense guard (`normalize_future_temporal_bounds`):
  - For facts matching "plans to / expects to / scheduled to / aims to / committed to / …'ll", `valid_at` is clamped to the statement's reference time. The future date stays in the text.
  - A deadline ("by / before / due by") is not treated as `invalid_at` unless the fact has ongoing-end language ("until / expires / no longer").
  - Source: [temporal_edge_utils.py L17-L80](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/temporal_edge_utils.py)
- Node (entity) resolution today:
  - Candidates come from three sources: configured identity properties (exact match), durable exact-name lookup, and cosine search on the name (`NODE_DEDUP_CANDIDATE_LIMIT = 15`, `NODE_DEDUP_COSINE_MIN_SCORE = 0.6`, "without reranking").
  - Deterministic resolution comes first:
    - An exact normalized name with exactly one match resolves; more than one match goes to the LLM.
    - Names with low character entropy (< 1.5) go to the LLM.
    - Otherwise MinHash/LSH (32 permutations, band size 4) with Jaccard ≥ 0.9 resolves.
  - Only unresolved names go to the LLM prompt `dedupe_nodes.nodes`. It shows each candidate's name, types and the first 120 characters of its summary, requires exactly one resolution per extracted entity, and returns `duplicate_candidate_id` or −1.
  - The prompt's rule is "duplicates only if they refer to the same real-world object or concept". Examples: NYC = New York City; Java the language ≠ Java the island.
  - Sources: [node_operations.py L67-L68, L456-L634, L649-L816](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/node_operations.py); [dedup_helpers.py L31-L36, L321-L400](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/dedup_helpers.py); [prompts/dedupe_nodes.py L118-L180](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/prompts/dedupe_nodes.py)
- Mechanism change since the paper: node candidate search in current code is cosine plus exact name, not "full-text on names and summaries". Edge search remains BM25 + cosine. The separate `invalidate_edges` prompt is gone; dedup and contradiction share one call. The context window constant is now `EPISODE_WINDOW_LEN = 3` (the paper says n = 4). — [graph_data_operations.py L29](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/graph_data_operations.py)
- Order dependence: `add_episode_bulk` resolves duplicates but has the comment "For now we won't track edge invalidation". Contradiction handling therefore needs sequential `add_episode`. — [bulk_utils.py L578](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/bulk_utils.py)
- Independent measurements of Zep's update step:
  - MemoryAgentBench FactConsolidation single-hop: Zep scored 7.0, against 60.0 for GPT-4o long context and 18.0 for Mem0. — [MemoryAgentBench](https://arxiv.org/html/2507.05257)
  - HaluMem memory updating, correct rate: Zep 47.28% (Medium) and 37.35% (Long), the second best after MemOS. — [HaluMem](https://arxiv.org/html/2511.03506v3)

### Inferences
Patterns to copy for the views database:
- Candidate generation by structure. Duplicates are looked up only among items with the same key (for us: the same affected object(s) and driver). A wider semantic search is used only for "might this weaken or falsify something".
- One LLM call that returns index lists for both duplicates and contradictions, validated in code.
- Validity dates owned by code, not by the LLM.
- The future-tense guard, which maps directly onto guidance and estimate evidence: a forecast is valid from its statement date, and its target date is not an expiry.

Graphiti's weaknesses also apply to us:
- On MemoryAgentBench FC-SH it scored worse than plain BM25. Conservative "explicit contradiction only" rules miss implicit supersession.
- It has no notion of "opposite direction = evidence against". A contradicted edge simply expires. Our design needs a three-way outcome (supports / weakens / falsifies) instead of a binary contradicted flag.

### Gaps
- No published precision/recall for Graphiti's duplicate or contradiction decisions in isolation. The paper reports only end-to-end QA.
- No published per-episode cost. The LLM call count per episode (extraction + node dedup + edge resolve + timestamps + attributes) is not stated in tokens or dollars.

## 3. Letta (MemGPT), LangMem, A-MEM, Cognee, MemoryOS and other 2025–2026 systems: duplicates, conflicts, history

### Takeaway
Most of these systems either let an agent rewrite memory text freely (Letta, LangMem, A-MEM), or deduplicate by deterministic identity (Cognee's uuid5 of the normalized name). Only a few treat conflict as a first-class record:
- Cognee's `FactConflict` with `time_varying` vs `fixed`.
- Hindsight's opinion network with a confidence that moves on reinforce / weaken / contradict.
- TEPA / MOSAIC-style keyed state machines.

On history: Letta now keeps git history of memory files. LangMem and A-MEM overwrite in place. MemoryOS evicts by capacity.

### Cited Findings

**Letta**
- The MemGPT-era edit tools were core_memory_replace / memory_replace / memory_insert / memory_rethink, plus sleep-time agents that rewrite blocks in the background. — [search summary of Letta docs/forum](https://docs-v1.letta.com/guides/agents/architectures/memgpt)
- The `letta-ai/letta` repository's main branch is now only a landing page. "The current source code lives in letta-ai/letta-code"; the V1 server is archived and "does not represent current Letta". — [letta README / AGENTS.md at 5bcdd17](https://github.com/letta-ai/letta)
- Context Repositories (2026-02-12): memory is markdown files in a git repository, and "every change to memory is automatically versioned with informative commit messages". A "memory defragmentation" skill "merges duplicates". Reflection and subagents work in git worktrees and merge back, with conflicts handled by git. This replaces the "MemGPT-style memory tools". No measurements were given. — [Letta blog](https://www.letta.com/blog/context-repositories)

**LangMem (LangChain)**
- `create_memory_manager` defaults to `enable_inserts=True, enable_updates=True, enable_deletes=False`. The instructions ask the model to "Consolidate and compress redundant memories … Remove incorrect or redundant memories while maintaining internal consistency".
- `create_memory_store_manager` retrieves context in one of two ways: LLM-generated parallel search queries, or dilated-window queries over the conversation. It keeps `query_limit=5` memories. Updates are `store.put` under the same key, which overwrites in place with no version history; RemoveDoc entries are deleted.
- Source: [langmem knowledge/extraction.py L185-L226, L846-L876, L1010-L1130](https://github.com/langchain-ai/langmem/blob/48e3c11f5bb527282c7d5339c6a87a0b35abccfc/src/langmem/knowledge/extraction.py)
- Measured: LoCoMo J 58.10 with p95 latency 60.40 s in Mem0's (vendor) table. — [Mem0 paper](https://arxiv.org/html/2504.19413)

**A-MEM (arXiv 2502.12110; code agiresearch/A-mem)**
- Each note gets keywords, tags and context from the LLM. On add, k = 5 nearest neighbours are retrieved from ChromaDB. An "evolution" prompt returns `should_evolve`, actions `strengthen` (add links, retag the new note) and/or `update_neighbor` (rewrite neighbours' context and tags). Every `evo_threshold=100` evolutions the store is re-indexed.
- There is no duplicate detection and no contradiction operation. `evolution_history` exists on the note but is never appended to.
- Source: [memory_system.py L93-L158, L233-L287, L590-L718](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)
- Code defect (my reading of the code):
  - `find_related_memories` returns `indices` as rank positions 0..k−1 in the search result.
  - `update_neighbor` then applies them to `list(self.memories.values())`, the store in insertion order. Whenever the store holds more than k notes, it rewrites the wrong notes.
  - `suggested_connections` stores those rank numbers as "links" rather than memory ids.
  - Source: [memory_system.py L288-L314, L684-L716](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)
- Measured: LoCoMo J 48.38 in Mem0's (vendor) table. — [Mem0 paper](https://arxiv.org/html/2504.19413)

**Cognee**
- Node identity is deterministic: `uuid5(NAMESPACE_OID, node_id.lower().replace(" ", "_").replace("'", ""))`. Same normalized name means the same node, whatever it refers to. — [cognee/infrastructure/engine/utils/generate_node_id.py](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/infrastructure/engine/utils/generate_node_id.py)
- Memify task `review_conflicts`: "Review source-backed facts and persist disputes without changing the facts."
  - Candidate groups are built in code: "Facts sharing a relationship name and one endpoint".
  - The LLM labels each conflict `kind: time_varying` ("a later source may correctly state a different value") or `fixed` ("only one value was ever true, so a difference means one source is wrong"). It assigns facts to `current` / `superseded` / `conflicting`.
  - Exclusions: a conflict is not reported when the attribute naturally holds several values, when the values are synonyms, when they are different scopes of one whole, or "when a value is only planned or proposed".
  - "Omitting a conflict is the safe outcome."
  - Stored as a `FactConflict` DataPoint with identity fields (dataset_id, about_id, attribute), status resolved/unresolved, values and sources.
  - Sources: [review_conflicts.txt](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/infrastructure/llm/prompts/review_conflicts.txt); [FactConflict.py](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/modules/engine/models/FactConflict.py); [review_conflicts/facts.py L42-L54](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/tasks/memify/review_conflicts/facts.py)
- Measured: MemoryAgentBench FactConsolidation SH 28.0 / MH 3.0. — [MemoryAgentBench](https://arxiv.org/html/2507.05257)

**MemoryOS (BAI-LAB, arXiv 2506.06326)**
- Short-, mid- and long-term tiers.
  - A mid-term page is merged into an existing session when `semantic_sim + α·Jaccard(keywords) ≥ 0.6`; otherwise a new session is created.
  - Mid-term sessions are evicted by LFU.
  - Long-term knowledge is a `deque(maxlen=100)`, so the oldest knowledge is silently dropped.
  - Content moves up tiers on a "heat" threshold.
  - Source: [mid_term.py L71-L77, L191-L278](https://github.com/BAI-LAB/MemoryOS/blob/587ed7755c7aed179965792830ff1b5ad9a6fa92/memoryos-pypi/mid_term.py); [long_term.py L12-L19](https://github.com/BAI-LAB/MemoryOS/blob/587ed7755c7aed179965792830ff1b5ad9a6fa92/memoryos-pypi/long_term.py)
- Vendor-reported: "average improvements of 49.11% and 46.18% in F1 and BLEU-1" on LoCoMo. — [MemoryOS README](https://github.com/BAI-LAB/MemoryOS)

**Hindsight (Vectorize.io, arXiv 2512.12818, December 2025)**
- Four networks: world facts, experiences, entity summaries, and opinions.
  - An opinion is o = (text with rationale, confidence c ∈ [0,1], timestamp τ, bank, entities).
  - New facts are matched to opinions by entity overlap or similarity above θ, and classified {reinforce, weaken, contradict, neutral}.
  - Update rule: c′ = min(c+α, 1) on reinforce; max(c−α, 0) on weaken; max(c−2α, 0) on contradict. On contradiction the text "may also update".
  - Entity resolution scores string, co-occurrence and temporal similarity; no thresholds are published.
  - Facts are retained.
  - Source: [Hindsight](https://arxiv.org/html/2512.12818v1)
- Vendor-reported: LongMemEval 83.6% (OSS-20B), 89.0% (OSS-120B), 91.4% (Gemini-3); LoCoMo 83.18 / 85.67 / 89.61. — [Hindsight](https://arxiv.org/html/2512.12818v1)

**MOSAIC (arXiv 2607.16211, May 2026)**
- Argues that LLM-classification memory "silently accumulate[s] contradictions". It uses entity-typed graph storage, hash-accelerated dual-path retrieval instead of LLM classification, and "active conflict detection at save time".
- Self-reported: conflict detection 66% vs a 14% baseline; LoCoMo 89.35%; HaluMem extraction F1 86.77 (Medium) and 85.84 (Long).
- Source: [MOSAIC abstract page](https://arxiv.org/abs/2607.16211)

### Inferences
- For an investment views database, the closest conceptual matches are:
  - Hindsight's opinion network: a belief whose confidence moves with supporting or contradicting evidence. This is close to our view + evidence(supports/weakens).
  - Cognee's `time_varying` vs `fixed` split, which maps onto whether a newer source can legitimately change the answer (guidance revision, estimate) or a difference means one source is wrong (a reported actual vs a rumour).
  - Cognee's "planned or proposed is not a conflict" rule, which matches Graphiti's future-tense guard.
- Hindsight's opinions have no evidence list. Our design should keep explicit evidence rows (quote, speaker, date, kind, supports/weakens) rather than only a confidence scalar. A scalar with a fixed α is not auditable and double-counts repeated news, which our rule "a repeat is not new evidence" forbids.
- Cognee's uuid5(normalized name) identity is "equal values establish identity", which our AGENTS.md forbids. It is cheap but merges homonyms.

### Gaps
- I did not inspect letta-code's TypeScript source for its dedup logic. The defragmentation skill's mechanism and any measurements are not documented beyond the blog.
- The A-MEM paper repository (WujiangXu/AgenticMemory) was not checked for the same index bug. The finding applies to agiresearch/A-mem at `ceffb86`.
- I found no published dedup precision/recall for LangMem, Cognee or MemoryOS.

## 4. Evaluations of the update / dedup / conflict step itself, and known failure modes

### Takeaway
Three benchmarks isolate the update step:
- HaluMem: update correct / hallucination / omission rates.
- MemoryAgentBench FactConsolidation: newest-fact-wins conflict resolution.
- LongMemEval's knowledge-update category.

All three show that commercial memory systems mostly fail by omission. They keep stale facts or never record the update; wrong updates are rare. Multi-hop conflict resolution is essentially unsolved: ≤ ~7% for every system. Where a fact has an explicit key and order, deterministic last-write-wins matches or beats LLM-decided updates.

### Cited Findings

**HaluMem (MemTensor, arXiv 2511.03506, v3 January 2026)**
- Update ground truth is pairs {m_old → m_new}. Metrics are correct rate C, hallucination rate H and omission rate O. — [HaluMem](https://arxiv.org/html/2511.03506v3)
- Memory updating (C / H / O, %):

| System | HaluMem-Medium | HaluMem-Long |
|---|---|---|
| Mem0 | 25.50 / 0.45 / 74.02 | 1.45 / 0.03 / 98.51 |
| Mem0-Graph | 24.50 / 0.26 / 75.24 | 1.47 / 0.04 / 98.40 |
| Memobase | 5.20 / 0.55 / 94.25 | 4.10 / 0.36 / 95.38 |
| MemOS | 62.11 / 0.42 / 37.48 | 65.25 / 0.29 / 34.47 |
| Supermemory | 16.37 / 1.15 / 82.47 | 17.01 / 0.58 / 82.42 |
| Zep | 47.28 / 0.42 / 52.31 | 37.35 / 0.48 / 62.14 |

  Source: [HaluMem](https://arxiv.org/html/2511.03506v3)
- Extraction recall:
  - Medium: Mem0 42.91, MemOS 74.07, Supermemory 41.53.
  - Long: Mem0 3.23, Mem0-Graph 2.24, MemOS 81.90.
  - Time cost (minutes, Medium): Mem0 2,809.8; Mem0-Graph 2,894.72; MemOS 1,049.37; Supermemory 368.74; Memobase 433.25.
  - Source: [HaluMem](https://arxiv.org/html/2511.03506v3)
- Conflict of interest: HaluMem is authored by MemTensor (contact @memtensor.cn), which builds MemOS, the system that tops every HaluMem table. These are not independent numbers for MemOS. — [HaluMem](https://arxiv.org/pdf/2511.03506)
- The Mem0 results are for the pre-April-2026 algorithm (paper dated November 2025 / January 2026).

**MemoryAgentBench (arXiv 2507.05257)**
- FactConsolidation is built from MQUAKE counterfactual edit pairs. Facts carry serial numbers, and the agent is told that "newer facts have larger serial numbers". — [MemoryAgentBench](https://arxiv.org/html/2507.05257)
- Scores (single-hop / multi-hop):
  - Long context: GPT-4o 60.0 / 5.0; GPT-4o-mini 45.0 / 5.0
  - RAG: BM25 48.0 / 3.0; HippoRAG-v2 54.0 / 5.0
  - Memory systems: Mem0 18.0 / 2.0; Cognee 28.0 / 3.0; Zep 7.0 / 3.0; MemGPT 28.0 / 3.0; MIRIX 14.0 / 2.0
  - Source: [MemoryAgentBench](https://arxiv.org/html/2507.05257)
- A later paper summarises: "54% single-hop and all 22 reported systems score at most 7% multi-hop". — [Reliable Post-Retrieval Assembly / "Don't Ask the LLM to Track Freshness" (2606.01435)](https://www.alphaxiv.org/abs/2606.01435)
- Stream sizes: 455 / 4,580 / 18,332 facts (6k / 64k / 262k tokens), with 55–63% of keys overwritten at least once. — [search summary of MemoryAgentBench-derived work](https://huggingface.co/papers/2507.05257)

**Deterministic freshness beats LLM-decided updates where keys exist**
- 2606.01435 (IIT Kharagpur, 2026) separates LLM evidence extraction from a code policy that picks the newest serial number.
  - Results: 82% / 93% single-hop and 27% / 41% multi-hop with gpt-4o-mini / gpt-4o.
  - "Most of the gain therefore comes from separating evidence identification from final policy execution rather than from the freshness operator itself."
  - On LongMemEval there was no significant gain: 26/45 vs 29/45, McNemar p = 0.45.
  - Source: [alphaxiv 2606.01435](https://www.alphaxiv.org/abs/2606.01435)
- TEPA (arXiv 2608.07429): items are (key, value, support count, conflict count, state ∈ {Hypothesis, Active, Revoked}, time).
  - A precedent is revoked when its posterior mean falls below 0.3 after ≥ 5 observations, or when its recent success rate falls below 0.34 after ≥ 3 same-key outcomes. "Revoked memory remains in the archive for audit while leaving the active retrieval set."
  - MemoryAgentBench SH-6k: TEPA-Rev 0.890 = last-write-wins 0.890, vs append-only 0.583. MH-6k: all methods 0.01–0.08.
  - Under a hidden full reversal, append-only scored 0.210, worse than no memory at 0.309; TEPA scored 0.950.
  - Diagnosis: "stale evidence can remain highly relevant to the current query, giving similarity, recency, and larger context a weak signal for supersession", and "append-only memory keeps stale and fresh evidence active under the same key".
  - Source: [TEPA](https://arxiv.org/html/2608.07429v2)

**LongMemEval knowledge-update category**
- Zep 83.3 vs full context 78.2 with gpt-4o, vendor-reported. — [Zep paper](https://arxiv.org/html/2501.13956)

**Learned managers**
- Memory-R1 trains the ADD/UPDATE/DELETE/NOOP manager with PPO/GRPO on QA correctness, using only 152 training QA pairs.
  - LoCoMo with LLaMA-3.1-8B: F1 35.73 vs Mem0 27.29; J 59.83 vs 43.93.
  - Qwen-2.5-7B: F1 43.14 vs 30.61; J 61.51 vs 53.30.
  - No per-operation error analysis is published.
  - Source: [Memory-R1](https://arxiv.org/html/2508.19828v4)

**Failure modes with evidence**
- Omission / stale facts dominate. See the HaluMem O-rates above: 52–98% for Mem0, Supermemory and Zep.
- False contradiction → wrong DELETE: the two-dogs case in [Memory-R1](https://arxiv.org/html/2508.19828v4). Scope blindness in [DEV post](https://dev.to/mukesh_13/mem0-auto-resolves-memory-conflicts-for-you-until-it-silently-deletes-one-you-still-need-4f4m). Graphiti hard-codes guards against this in its prompt ("Do NOT infer contradiction from recency alone…"). — [dedupe_edges.py](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/prompts/dedupe_edges.py)
- False merge: Cognee's name-hash identity, and Mem0's v1 UPDATE that merges "cheese pizza" + "chicken pizza" into one rewritten string. — [generate_node_id.py](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/infrastructure/engine/utils/generate_node_id.py); [mem0 prompts.py L176-L325](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/configs/prompts.py#L176-L325)
- Bloat: Mem0's ADD-only change says "your memory count will grow rather than plateau". Zep's footprint was 600k+ tokens per LoCoMo conversation in Mem0's measurement. — [platform-v2-to-v3.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/migration/platform-v2-to-v3.mdx); [Mem0 paper](https://arxiv.org/html/2504.19413)
- Order dependence: Graphiti bulk ingestion skips invalidation. Graphiti's code also has to detect a contradicting candidate that "starts later" when facts arrive out of order. — [bulk_utils.py L578](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/bulk_utils.py); [edge_operations.py L715-L745](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L715-L783)
- Index / identity hallucination: Mem0 remaps UUIDs to small integers; Graphiti drops out-of-range idx values; A-MEM's rank-vs-store index bug is a real instance. — [mem0 v1.0.11 main.py L584-L588](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/main.py#L555-L592); [A-mem memory_system.py](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)
- Cost: HaluMem measured memory construction for Mem0 at about 2,810 minutes on the Medium set, with LLM calls on every add. The current Mem0 cut extraction to one call ("cutting extraction latency roughly in half", vendor-reported). — [HaluMem](https://arxiv.org/html/2511.03506v3); [oss-v2-to-v3.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/migration/oss-v2-to-v3.mdx)

### Inferences
- The measurements argue for:
  - Doing supersession in code from structured keys and dates where possible: last-write-wins on a key, Graphiti's date logic.
  - Keeping the LLM to evidence extraction and classification (supports / weakens / duplicate / new), validated against a closed set of ids.
- Omission, not hallucination, is the dominant measured failure. A views store should measure "evidence that should have attached to view V but didn't" (recall) as its primary update metric. Precision of attachments comes second.
- No benchmark tests factor-like items (one view → many objects, with direction). We will need our own gold for "same view / merge / new / evidence-against", built from stored documents and kept stable before iterating (AGENTS.md §7).

### Gaps
- I found no published precision/recall of duplicate detection specifically (pairwise "same item?" accuracy) for any of the commercial systems. Benchmarks score updates or QA, not dedup pairs.
- I did not verify BEAM's "contradiction resolution" sub-score (vendor Mem0 reports BEAM 64.1 overall only).
- MemoryAgentBench numbers for newer systems (Mem0 v3, Zep 2026) were not found.

## 5. History: which designs keep superseded items (soft invalidation) and which overwrite, and why

### Takeaway
The field converged on soft invalidation during 2025–2026:
- Graphiti never deletes; it sets `invalid_at` / `expired_at`.
- Mem0g moved from hard to soft delete.
- Mem0 itself abandoned UPDATE/DELETE for ADD-only plus non-destructive supersede/merge flags.
- Letta versions memory in git.
- Cognee records disputes "without changing the facts".
- TEPA archives revoked items.

LangMem, A-MEM and Mem0 v1's vector store still overwrite or hard-delete, and MemoryOS evicts by capacity. The stated reasons for keeping history: temporal questions ("where did I live before"), complementary facts that only looked contradictory, and audit.

### Cited Findings
- Graphiti: bi-temporal edges. A contradicted edge gets `invalid_at = new.valid_at` and `expired_at = now`; nothing is removed. — [edge_operations.py L715-L783](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/edge_operations.py#L715-L783); [Zep paper](https://arxiv.org/html/2501.13956)
- Mem0 v1 vector store: UPDATE overwrites in place, DELETE removes the vector. Only an SQLite `history` table keeps the old text (`is_deleted=1`), and search never reads it. — [mem0 v1.0.11 main.py L1340-L1364](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/main.py#L1340-L1364)
- Mem0g: "Soft-delete: mark relationship as invalid instead of removing it, enabling temporal reasoning over historical graph state" (`r.valid=false, r.invalidated_at`). — [graph_memory.py L420-L432](https://github.com/mem0ai/mem0/blob/v1.0.11/mem0/memory/graph_memory.py#L420-L432)
- Mem0 2026: ADD-only, "both facts are preserved with temporal context … No information loss". Dream supersede / merge are flags, "retained, never erased". — [platform-v2-to-v3.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/migration/platform-v2-to-v3.mdx); [dream.mdx](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/docs/platform/features/dream.mdx)
- Letta Context Repositories: "every change to memory is automatically versioned". — [Letta blog](https://www.letta.com/blog/context-repositories)
- Cognee review_conflicts: "persist disputes without changing the facts". — [review_conflicts/__init__.py](https://github.com/topoteretes/cognee/blob/37f788bd287750e10d7610173e5332b3843f6ebd/cognee/tasks/memify/review_conflicts/__init__.py)
- TEPA: revoked items stay in the archive for audit and leave the active retrieval set. — [TEPA](https://arxiv.org/html/2608.07429v2)
- Hindsight: facts retained; opinions keep a confidence trajectory. — [Hindsight](https://arxiv.org/html/2512.12818v1)
- Overwrite designs:
  - LangMem: `store.put` same key; deletes are allowed when enabled. — [extraction.py](https://github.com/langchain-ai/langmem/blob/48e3c11f5bb527282c7d5339c6a87a0b35abccfc/src/langmem/knowledge/extraction.py)
  - A-MEM: `update_neighbor` rewrites neighbours' context and tags; `evolution_history` is never written. — [memory_system.py](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py)
  - MemoryOS: `deque(maxlen=100)` and LFU eviction. — [long_term.py](https://github.com/BAI-LAB/MemoryOS/blob/587ed7755c7aed179965792830ff1b5ad9a6fa92/memoryos-pypi/long_term.py)
- Cost of keeping history: append-only without a supersession state leaves stale and fresh items active together. TEPA measured append-only at 0.583 vs last-write-wins at 0.890 on FC-SH-6k, and at 0.210 vs 0.309 for no memory under a reversal. Keeping history therefore needs an explicit active / superseded state that retrieval honours, not just more rows. — [TEPA](https://arxiv.org/html/2608.07429v2)

### Inferences
- Our rule (closed views kept; status ∈ active / confirmed / falsified / expired / merged; a reworded claim is a new view that supersedes) matches the converged design. It is stricter than Mem0's Dream because the claim text is immutable.
- What to copy:
  - Graphiti's split between "world-valid" dates (when the view was formed and when its deadline falls) and "system" dates (when ingested, when status changed).
  - A `superseded_by` / `merged_into` pointer, as in Mem0's Dream links.
  - Retrieval filters on status by default, as in `latest_only`, with history available on request.
- What to avoid:
  - In-place text rewrite (Mem0 v1 UPDATE, A-MEM neighbour rewrite, LangMem put).
  - Capacity eviction.
  - Append-only with no state field, which TEPA shows is worse than no memory under reversals.

### Gaps
- No system publishes a study of how much history retention costs in retrieval precision at scale (for example, superseded items crowding the top-k). Mem0 claims ranking "handles this at retrieval time" but publishes no separate measurement of it.
