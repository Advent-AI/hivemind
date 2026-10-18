# Architecture alternatives for keeping an LLM-maintained views store current: full context vs retrieve-then-judge, incremental KG construction and dedup, cost, hybrids, concurrency

Scope note (for the report writer). Researched 2026-10-17/18. Labels used below:
- "Vendor claim": the number comes from the company selling the product.
- "Author-reported": the authors compare their own system with baselines they ran themselves.
- "Older": the result predates 2025.
- "Estimate": my own arithmetic, not a measurement.

I read the code directly from shallow clones at these commits:
- LightRAG `aaebfe1` (2026-10-14)
- microsoft/graphrag `5faaaf4` (2026-10-08)
- AuvaLab/itext2kg `840aba2` (2026-09-04, which contains ATOM)
- stair-lab/kg-gen `6259b4c` (2026-03-24)
- getzep/graphiti `d50741d` (2026-10-15)

Things the brief says are already established are not repeated here. They are:
- embeddings cannot separate direction, numbers or periods;
- choosing among ~4 candidates beats judging pairs one at a time;
- Mem0 moved to ADD-only;
- Graphiti never deletes.

Results already in the sibling notes `观点库 向量检索 去重匹配/agent_memory_crud.md` are referenced briefly, not re-derived. These include:
- the Mem0 LoCoMo table;
- Letta 74.0;
- the Zep LongMemEval numbers;
- Graphiti's node/edge dedup internals.

## 1. Long context vs retrieval for small, bounded sets: measured results, degradation with item count, and where retrieval becomes necessary

### Takeaway
When everything relevant fits comfortably in the prompt, the measured studies favour giving the model the whole set. This holds in long-context-vs-RAG QA studies and in memory benchmarks' update and conflict tasks. Degradation comes from three things:
- total length (it starts to bite at roughly 4K–16K tokens for 2024–25 models when the match is not literal);
- distractors that look similar (they shrink the effective length a lot);
- position.

Retrieval wins clearly only at large scale: hundreds of tools, contexts of 100K to 1M+ tokens, or chat histories far beyond the window. A per-object set of 5–30 compact view cards (≈1–5K tokens) sits inside the range where full context is measured to work. A universe-wide pool of shared macro/theme views (hundreds of cards) does not.

中文要点：小而有界的集合（单个标的 5–30 条观点 ≈ 1–5K token）属于"全量给模型"被测量证明有效的区间；真正必须检索的是几百条以上、或 >16–32K token 的场景（如全市场共享的宏观/主题观点池）。退化的主因是相似干扰项和位置，不只是长度。

### Cited Findings

**Long context (LC) vs RAG, head-to-head**

Self-Route study (Li et al., EMNLP 2024 industry track; older, July 2024):
- Setup: Gemini-1.5-Pro, GPT-4o and GPT-3.5-Turbo on 9 LongBench/∞Bench datasets. RAG used top-k = 5 chunks of 300 words.
- Averages, LC vs RAG: Gemini-1.5-Pro 49.70 vs 37.33; GPT-4o 48.67 vs 32.60; GPT-3.5-Turbo 32.07 vs 30.33.
- "For 63% queries, the model predictions are exactly identical" between RAG and LC, and 70% of queries differ by under 10 points.
- Source: [Li et al. 2024, arXiv 2407.16833](https://arxiv.org/html/2407.16833)

"Long Context vs. RAG for LLMs: An Evaluation and Revisits" (Jan 2025):
- 13,628 questions that need external context. LC answered 56.3% correctly (7,676) vs RAG 49.0% (6,683). LC-only correct: 2,287; RAG-only correct: 1,294.
- RAG did comparably or better on dialogue-based and fragmented sources and on open "how/why" questions.
- The best retriever was RAPTOR (38.5% on the sample set) vs BM25 20.4% and text-embedding-3-small 21.6%.
- Source: [arXiv 2501.01880](https://arxiv.org/html/2501.01880)

LaRA (2025, 2,326 test cases, 11 LLMs):
- "No Silver Bullet": the better choice depends on model size, long-text ability, context length, task type and chunk characteristics.
- Source: [LaRA, arXiv 2502.09977](https://arxiv.org/abs/2502.09977)

"Long-Context LLMs Meet RAG" (ICLR 2025):
- Adding more retrieved passages first helps, then hurts.
- "Using stronger retrievers is also not a mitigation… the performance degradation can even be more severe with them." The mechanism is hard negatives: passages that look relevant but are not.
- Source: [ICLR 2025 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/5df5b1f121c915d8bdd00db6aac20827-Paper-Conference.pdf). I took this from the search summary, not a full read.

**Memory benchmarks: full-context baselines on update/conflict tasks**

MemoryAgentBench (arXiv 2507.05257, 2025), Table 3. Scores are AR / TTL / LRU / SF, where SF is selective forgetting (the conflict-resolution / fact-consolidation competency).

| Group | System | AR | TTL | LRU | SF |
|---|---|---|---|---|---|
| Long-context agent | GPT-4o (128K) | 58.1 | 50.0 | 54.9 | 32.5 |
| Long-context agent | Claude-3.7-Sonnet | 59.7 | 53.9 | 62.2 | 22.5 |
| Long-context agent | GPT-4.1-mini | 71.8 | 46.2 | 49.1 | 20.5 |
| Simple RAG | BM25 | 60.5 | 44.5 | 35.6 | 25.5 |
| Structure-augmented RAG | GraphRAG | 40.9 | 24.8 | 19.9 | 8.0 |
| Structure-augmented RAG | HippoRAG-v2 | 65.1 | 35.8 | 36.2 | 29.5 |
| Structure-augmented RAG | RAPTOR | 36.8 | 35.9 | 27.9 | 7.5 |
| Memory system | Mem0 | 32.6 | 21.2 | 20.7 | 10.0 |
| Agentic memory | MemGPT | 34.3 | 40.8 | 22.4 | 15.5 |

- The paper says: "All methods fail on the multi-hop situation (with achieving at most 28% accuracy). Only long context agents can achieve fairly reasonable results on single-hop scenarios."
- Retrieval used 512-token chunks for document QA, 4,096-token chunks otherwise, and top-10 retrieved chunks.
- Source: [MemoryAgentBench](https://arxiv.org/html/2507.05257)
- The sibling notes record FactConsolidation single-hop as GPT-4o long context 60.0 vs Mem0 18.0 vs Zep 7.0.

LongMemEval (ICLR 2025):
- On LongMemEval_S (~115K tokens per problem), oracle evidence vs full history: GPT-4o 0.870 vs 0.606 (−30.3%); Llama 3.1 70B 0.744 vs 0.334 (−55.1%); Llama 3.1 8B 0.710 vs 0.454.
- Memory-design fixes that worked:
  - fact-augmented key expansion: +9.4% recall@k and +5.4% accuracy;
  - time-aware query expansion: +6.8–11.3% on temporal retrieval.
- Source: [LongMemEval, arXiv 2410.10813](https://arxiv.org/html/2410.10813)
- At this scale (115K tokens) retrieval wins. That is not our per-object scale.

BEAM (arXiv 2510.27246, Oct 2025), dialogues of 100K–10M tokens:
- Knowledge update at 1M tokens, vanilla LC vs RAG vs LIGHT (episodic retrieval + working memory + scratchpad):

| Model | Vanilla LC | RAG | LIGHT |
|---|---|---|---|
| Llama-4-Maverick | 0.164 | 0.342 | 0.414 |
| GPT-4.1-nano | 0.150 | 0.342 | 0.392 |
| Qwen2.5-32B | 0.064 | 0.378 | 0.357 |

- Contradiction resolution is ≈0.01–0.05 for every method: "a challenging open problem".
- Source: [BEAM](https://arxiv.org/html/2510.27246v1)

LoCoMo:
- Conversations are 16K–26K tokens, so they fit in context. Full context scored 72.90, above every memory system in Mem0's own table.
- A Letta agent with plain file tools scored 74.0 (GPT-4o-mini), vs Mem0's best graph result of 68.5.
- Sources: sibling notes, citing [Mem0 paper](https://arxiv.org/html/2504.19413) and [Letta blog](https://www.letta.com/blog/benchmarking-ai-agent-memory) (vendor claims).

**How accuracy degrades with length, distractors and position**

NoLiMa (ICML 2025; "needle" questions with no literal overlap with the answer):

| Model | Base | 1K | 2K | 4K | 8K | 16K | 32K | Effective length |
|---|---|---|---|---|---|---|---|---|
| GPT-4o | 99.3% | 98.1% | 98.0% | 95.7% | 89.2% | 81.6% | 69.7% | 8K |
| Claude 3.5 Sonnet | 87.5% | 85.4% | 84.0% | 77.6% | 61.7% | 45.7% | 29.8% | 4K |
| Gemini 1.5 Pro | 92.6% | 86.4% | 82.7% | 75.4% | 63.9% | 55.5% | 48.2% | 2K |
| Llama 3.3 70B | 97.3% | 94.2% | 87.4% | 81.5% | 72.1% | 59.5% | 42.7% | 2K |
| GPT-4o mini | 84.8% | 67.7% | 58.2% | 44.2% | 32.6% | 20.6% | 13.7% | <<1K |

- Distractors with irrelevant literal matches cut GPT-4o's effective length from 8K to about 1K.
- Literal cues restore accuracy: multiple-choice with literal cues scored 93.1% vs 56.2% for one-hop without a literal match (Llama 3.3 70B, 32K).
- "At 32K… 11 models drop below 50% of their strong short-length baselines."
- Sources: [NoLiMa HTML](https://arxiv.org/html/2502.05167); [abstract](https://arxiv.org/abs/2502.05167)

Context Rot (Chroma, 2025-07-14; vendor research report, 18 models including Claude Opus 4, GPT-4.1, Gemini 2.5 Pro, Qwen3):
- Performance falls as input grows, even on simple tasks.
- Lower needle–question similarity gives steeper decline.
- Distractors hurt more as length grows.
- On LongMemEval, the focused prompt (~300 tokens) scored "significantly higher" than the full prompt (~113K tokens) for every family. Exact numbers are shown only in charts.
- Source: [Chroma research](https://www.trychroma.com/research/context-rot)

Lost in the Middle (TACL; older, 2023), multi-document QA with 10/20/30 documents:
- The curve is U-shaped (primacy and recency bias).
- GPT-3.5-Turbo can drop "by more than 20%". In the worst case, with 20 and 30 documents, accuracy falls below closed-book (56.1%) while oracle is 88.3%.
- Claude-1.3: closed-book 48.3%, oracle 76.1%.
- Source: [Liu et al., arXiv 2307.03172](https://arxiv.org/abs/2307.03172), Table 1 read from the PDF.

Position bias when selecting from a list ("Match, Compare, or Select?", COLING 2025):
- "Selection accuracy varies significantly as the position of the matching record increases in the candidate list."
- Varying the number k of candidates kept: "GPT-3.5 Turbo is highly variable, while that of GPT-4o Mini is relatively stable".
- Their compound pipeline keeps the top 4 from a cheap ranker (Flan-T5-XL) and lets the large model select.
- Source: [arXiv 2405.16884v3](https://arxiv.org/html/2405.16884v3)

**Where retrieval becomes necessary: large catalogues**

RAG-MCP (May 2025; qwen-max-0125, DeepSeek-v3 judge):
- In the stress test, tool positions below ~30 mostly succeed at over 90%. Beyond ~100, precision collapses.
- All tools in the prompt: 13.62% accuracy at 2,133.84 average prompt tokens. Retrieval first: 43.13% at 1,084 tokens.
- Source: [arXiv 2505.03275](https://arxiv.org/html/2505.03275v1)

Anthropic Tool Search Tool (2025-11-24; vendor claim):
- 58 tools take about 55K tokens of definitions.
- MCP-eval accuracy rose from 49% to 74% (Opus 4) and from 79.5% to 88.1% (Opus 4.5) when tools are retrieved on demand.
- Token use for definitions fell 85%.
- "The most common failures are wrong tool selection… especially when tools have similar names."
- Source: [Anthropic engineering](https://www.anthropic.com/engineering/advanced-tool-use)

### Inferences
- **Our size.** A compact view card (claim, driver, direction, horizon, signed objects, deadlines, id) is about 120–200 tokens (estimate). At that size:
  - 5–30 active views per object is about 0.6–6K tokens;
  - two related objects together are about 1–12K tokens.
  For strong 2024–25 models, NoLiMa shows only mild loss at 1–4K and noticeable loss from 8–16K. On this evidence, Option A (all active views of the document's related objects) sits in the "full context works" zone for one or two company objects.
- **Macro/theme views.** A theme that touches many objects can bring a list of 100+ cards (15K+ tokens). That is where measured degradation (NoLiMa ≥16K, RAG-MCP beyond ~100 items) and the cost penalty start. Shared macro/theme views are therefore the part that needs retrieval or a separate, smaller list (see Section 4).
- **Distractors are our main risk.** The danger in a per-object list is less its length than its similarity. Every view on NVDA mentions NVDA, data centre, margins and so on. These are exactly NoLiMa's "irrelevant literal matches" and the ICLR 2025 "hard negatives". So full-context accuracy must be measured on our own lists, not taken from generic benchmarks. Order effects should be tested by permuting the list (position bias, COLING 2025).
- **Update/conflict decisions specifically.** The measured evidence (MemoryAgentBench SF/FactConsolidation, LoCoMo full context ≥ memory systems) says that when the relevant set fits, long context beats retrieval-based and graph-based memory on keeping state consistent. Graph/structure-augmented RAG did worst on selective forgetting: GraphRAG 8.0, RAPTOR 7.5.
- **Even under full context, code still decides direction and horizon.** NoLiMa shows literal cues help a great deal, and earlier work showed embeddings cannot separate direction. So the LLM should pick the same-driver view from the full list, and code should compare the structured direction/horizon fields, as in the current draft.

### Gaps
- I found no published measurement of LLM accuracy at choosing "the same driver/claim" from N in-context items as N varies from 4 to 30+ with frontier 2026 models. The COLING 2025 paper gives curves only for GPT-3.5/4o-mini, with no table values in the HTML. This must be measured on our own stored cases: the same cases under the top-4 arm and under the full-list arm, with permuted orders.
- I found no NoLiMa or Context Rot numbers for 2026 models (Claude 5.x, GPT-5.6+). Effective-length thresholds above are from 2024–25 models and probably understate current models.
- I could not get exact per-model LongMemEval focused-vs-full numbers from the Chroma report (charts only).

## 2. Incremental knowledge-graph construction with LLMs: how each builder deduplicates entities and relations when new documents arrive

### Takeaway
None of the KG builders judge "same claim" semantically on insert. Entity identity is either:
- an exact normalized name (LightRAG, GraphRAG incremental);
- exact name+label, then an embedding threshold (ATOM/iText2KG);
- a semantic hash, then an optional offline LLM pass inside clusters (KGGen);
- a cascade of exact name, then MinHash, then LLM-chooses-one-of-~15 (Graphiti).

Relation dedup is either by endpoint pair (LightRAG, GraphRAG) or by relation-name embedding regardless of endpoints (ATOM). "Merging" means concatenating descriptions and having an LLM re-summarize them. The only measured duplicate numbers are author-reported:
- KGGen: −22.4% entities, −23% edges after its clustering pass;
- ATOM: entity/relation resolution F1 0.994/1.0 vs Graphiti 0.959/0.902 and iText2KG 0.977/0.989.

These are entity-level mechanisms. They do not address our problem, which is claim/driver-level sameness with direction.

中文要点：主流 KG 构建工具在写入时都不做"是否同一观点"的语义判断——实体靠精确名（LightRAG、GraphRAG 增量）、名称+类型精确匹配后余弦阈值（ATOM 0.8）、语义哈希 + 离线聚类内 LLM 去重（KGGen）、或精确名→MinHash→LLM 从约 15 个候选里选一个（Graphiti）。"合并"就是拼接描述再让 LLM 重写摘要。公开的重复率数字只有作者自报。

### Cited Findings

**LightRAG (HKUDS; code `aaebfe1`, Oct 2026)**
- **Entity identity = normalized name.** `_merge_nodes_then_upsert` calls `knowledge_graph_inst.get_node(entity_name)`. If the node exists, it merges; otherwise it creates. `normalize_entity_name` only cleans text: HTML, Chinese/English punctuation and quotes, spacing.
  - Sources: [operate.py L2429-L2640](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/operate.py#L2429-L2640); [utils.py L5833-L5860](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/utils.py#L5833-L5860)
- **Merge = union plus LLM summary.**
  - Entity type is the most frequent type.
  - Descriptions are deduplicated by exact string, sorted by timestamp, and combined.
  - An LLM map-reduce summary runs only when there are ≥ `DEFAULT_FORCE_LLM_SUMMARY_ON_MERGE = 8` fragments or the token limits are exceeded (`SUMMARY_MAX_TOKENS = 1200`, `SUMMARY_CONTEXT_SIZE = 12000`).
  - Sources: [operate.py L372-L420](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/operate.py#L372-L420); [constants.py L30-L36](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/constants.py#L30-L36)
- **Relations** are keyed by the sorted (src, tgt) pair, so they are effectively undirected per pair.
  - Source: [operate.py L3819-L3840](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/operate.py#L3819-L3840)
- **No semantic entity resolution on insert.** Merging "Apple" with "Apple Inc." is a manual API, `amerge_entities(source_entities, target_entity)`.
  - Source: [utils_graph.py L3440](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/utils_graph.py#L3440)
- **Paper (Oct 2024; older).** Incremental update takes "the union of the node sets and edge sets", with no community rebuild. The authors estimate GraphRAG needs about 1,399 communities × 2 × 5,000 tokens ≈ 13,995,000 tokens to regenerate community reports on update. Datasets were UltraDomain Agriculture/CS/Legal/Mix (0.6–5.1M tokens). This is author-reported.
  - Source: [LightRAG, arXiv 2410.05779](https://arxiv.org/html/2410.05779)

**Microsoft GraphRAG incremental indexing (code `5faaaf4`, Oct 2026)**
- **Entities** in a delta are matched to old entities on exact `title` (a pandas merge on the title column), then grouped by title.
  - Descriptions are kept as a list and re-summarized by the `summarize_descriptions` LLM step.
  - `degree` keeps the first value, with the code comment "todo: we could probably re-compute this".
  - Sources: [update/entities.py](https://github.com/microsoft/graphrag/blob/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/update/entities.py); [workflows/update_entities_relationships.py L61-L109](https://github.com/microsoft/graphrag/blob/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/workflows/update_entities_relationships.py#L61-L109)
- **Relationships** are grouped by exact (source, target). Descriptions are listed, weight is averaged, and degrees are recomputed.
  - Source: [update/relationships.py](https://github.com/microsoft/graphrag/blob/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/update/relationships.py)
- **Communities** of the delta get ids offset past the old maximum ("Increment all community ids by the max of the old communities"). They are merged in, not re-clustered.
  - Source: [update/communities.py](https://github.com/microsoft/graphrag/blob/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/update/communities.py)

**iText2KG / ATOM (Lairgi et al.; ATOM accepted to EACL 2026 Findings; code `840aba2`)**
- **Entity match.** First an exact name+label match. Otherwise cosine similarity (text-embedding-3-large) with argmax over the unmatched existing entities, merged if ≥ θE = 0.8. No LLM is used in the merge.
  - Sources: [matcher.py L19-L100](https://github.com/AuvaLab/itext2kg/blob/840aba2c89d2f00c84c6b1da4c1c0b6637fa8d5d/itext2kg/atom/graph_matching/matcher.py); [ATOM paper](https://arxiv.org/html/2510.22590v2)
- **Relation match.** Relation names are renamed to the best match at cosine ≥ θR (default 0.7 in `build_graph`, 0.8 in `merge_two_kgs`) "regardless of endpoints and timestamps". The t_obs, t_start and t_end timestamp lists are unioned.
  - Sources: [matcher.py L105-L175](https://github.com/AuvaLab/itext2kg/blob/840aba2c89d2f00c84c6b1da4c1c0b6637fa8d5d/itext2kg/atom/graph_matching/matcher.py); [atom.py L219-L225](https://github.com/AuvaLab/itext2kg/blob/840aba2c89d2f00c84c6b1da4c1c0b6637fa8d5d/itext2kg/atom/atom.py#L219-L225)
- **Measured on 2020-COVID-NYT (author-reported).** 1,076 articles; ground truth 4,223 atomic facts and 7,210 5-tuples. Fact decomposition used Claude Sonnet 4; extraction used GPT-4.1.
  - Resolution F1: ATOM 0.994 entity / 1.0 relation; Graphiti 0.959 / 0.902; iText2KG 0.977 / 0.989.
  - Latency −93.8% vs Graphiti and −95.3% vs iText2KG.
  - Run-to-run stability (Jaccard) 0.552 vs 0.212 for direct extraction.
  - Stated limitation: threshold merging "can occasionally merge semantically distinct named entities… (e.g., gpt-5:model and gpt-3.5:model)".
  - Source: [ATOM, arXiv 2510.22590](https://arxiv.org/html/2510.22590v2)

**KGGen (Mo et al., Stanford, 2025; code `6259b4c`)**
- **Default dedup = `SEMHASH`.** Items are normalized and singularized (inflect), then run through SemHash `self_deduplicate` at threshold 0.95.
  - Sources: [steps/_3_deduplicate.py](https://github.com/stair-lab/kg-gen/blob/6259b4c71523ceae75dafb4acec2eb833bef8f8e/src/kg_gen/steps/_3_deduplicate.py); [utils/deduplicate.py](https://github.com/stair-lab/kg-gen/blob/6259b4c71523ceae75dafb4acec2eb833bef8f8e/src/kg_gen/utils/deduplicate.py)
- **Optional `LM_BASED` / `FULL` pass**, which runs over the whole graph:
  1. KMeans on S-BERT embeddings into clusters of about 128 items.
  2. For each item, retrieve the top-16 by 0.5·BM25 + 0.5·embedding.
  3. A DSPy `Deduplicate` signature returns `duplicates` (exact items from the set) and a canonical `alias`. Duplicates are only "variation in tense, plural form, stem form, case, abbreviation, shorthand".
  - Source: [utils/llm_deduplicate.py L57-L230](https://github.com/stair-lab/kg-gen/blob/6259b4c71523ceae75dafb4acec2eb833bef8f8e/src/kg_gen/utils/llm_deduplicate.py)
- **Measured (author-reported).**
  - MINE-1 knowledge retention (100 articles × 15 facts): KGGen 66.07% vs GraphRAG 47.80% vs OpenIE 29.84%.
  - On a 1M-character novel, dedup cut entities 22.4% (4,602 → 3,573) and edges 23%.
  - The authors acknowledge "over or under de-duplication".
  - Source: [KGGen, arXiv 2502.09956](https://arxiv.org/html/2502.09956)

**Graphiti (non-invalidation parts; details in sibling notes)**
- **Node candidates** come from identity properties, exact name, and cosine on name (limit 15, min 0.6).
  - Low-entropy names go to the LLM. Otherwise MinHash/LSH resolves at Jaccard ≥ 0.9 deterministically.
  - The rest go to an LLM that must return one id or −1 per entity.
- **Edge dedup** is limited to edges between the same entity pair.
- **No published precision/recall** for Graphiti's dedup step in isolation.
- Source: sibling notes, citing [node_operations.py](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/maintenance/node_operations.py)

**Schema canonicalization (closest analogue to a per-object driver registry): EDC, "Extract, Define, Canonicalize" (Zhang & Soh, 2024; older)**
- Steps: extract open triples, have the LLM write a definition for each relation, retrieve the relevant schema elements, and let the LLM verify the canonical one. If no schema exists, it does "self-canonicalization".
- It was built because prior methods required "the KG schema… included in the LLM prompt".
- Datasets: WebNLG, REBEL, Wiki-NRE. The abstract has no numbers.
- Source: [arXiv 2404.03868](https://arxiv.org/abs/2404.03868)

### Inferences
- **Option C (incremental KG) brings no dedup mechanism stronger than what the current draft already has.**
  - Exact-name keys (LightRAG, GraphRAG) are the equivalent of "same driver string".
  - Cosine-threshold merges (ATOM 0.8, KGGen SemHash 0.95) are exactly the embedding-sameness test the earlier research rejected for direction, numbers and periods. ATOM's own failure example (gpt-5 vs gpt-3.5) is the "same sentence, different period" problem.
  - The more careful pattern (Graphiti, KGGen LM pass) is again "retrieve ~15–16 candidates, then the LLM picks", which is the current draft.
- **KG builders separate two things we also need**:
  - an online, cheap identity decision (exact key or retrieval-then-LLM-pick);
  - an offline consolidation pass over clusters (KGGen) or a manual merge API (LightRAG `amerge_entities`).
  Both fit our "reversible merge" status.
- **Option B (per-object driver registry) is the EDC pattern** applied per object. Linking to a small closed set is a classification over a list that fits easily in context. Creating a new driver, however, moves the dedup problem up one level, to deciding whether a new driver duplicates an existing one. So the registry needs the same offline consolidation pass.
- **Graph-structured memories performed worst** on the measured update/forgetting tasks (MemoryAgentBench SF: GraphRAG 8.0, RAPTOR 7.5, Mem0 10.0). Graph structure is evidence against Option C for the update decision itself. It may still help for browsing and explaining views, which is not measured here.

### Gaps
- AutoKG and other 2024–2026 incremental builders (Graphusion, KARMA, Docs2KG) were not researched within the tool budget. I found no measured duplicate rates for them.
- LightRAG and GraphRAG publish no duplicate-rate or entity-resolution accuracy for incremental insertion.
- The ATOM/iText2KG and KGGen numbers are author-reported. I found no independent replication.
- EDC's numeric results were not extracted (abstract only).

## 3. Cost and latency at ~3,000 documents/day: tokens per decision, prompt caching, published comparisons

### Takeaway
At our per-object sizes, full context (Option A) costs roughly 2–3.5× the input tokens of retrieve-top-4 (estimate). In dollars the gap is small: about $20–50/day on a Sonnet-class model. It is the same order of magnitude as simply reading the documents.

Published cost gaps are large (10–100×) only because they compare 100K-token histories with a 1–2K-token retrieval. Caching pays back after one reuse within the 5-minute TTL, but our arrivals per object are sparse. Hits therefore need per-object batching and an append-only ordering of each object's view list.

中文要点：在单标的规模下，全量方案的输入 token 约为检索 top-4 方案的 2–3.5 倍（估算），在 Sonnet 级模型上每天只多约 20–50 美元，与"读文档本身"的成本同量级。文献中 10–100 倍的成本差来自 10 万 token 级历史，不适用于我们。缓存只需一次复用就回本，但前提是同一标的的文档被成批处理、观点列表按创建顺序只追加。

### Cited Findings

**Published tokens per decision and latency**
- LoCoMo (Mem0 paper, vendor; in sibling notes): full context ~26K tokens per conversation vs Mem0 ~7K. p95 latency 17.12 s full context vs 1.44 s Mem0. — [Mem0 paper](https://arxiv.org/html/2504.19413)
- LongMemEval (Zep paper, vendor): average context 1.6K vs 115K tokens, "about 90% lower latency". — [Zep paper](https://arxiv.org/html/2501.13956)
- Self-Route: same accuracy as LC for GPT-4o (48.89 vs 48.67) at 61.40% of LC's tokens. 38.39% of tokens for Gemini-1.5-Pro (46.41 vs 49.70), i.e. "65% cost reduction for Gemini-1.5-Pro and 39% for GPT-4O". — [arXiv 2407.16833](https://arxiv.org/html/2407.16833)
- RAG-MCP: 1,084 vs 2,133.84 prompt tokens. Tool Search: −85% definition tokens (vendor). — [RAG-MCP](https://arxiv.org/html/2505.03275v1); [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- COLING 2025 entity matching, cost per 4,000 test pairs (GPT-3.5): select-among-candidates $1.71; pairwise matching $4.52; filter-then-select (ComEM) $0.92. — [arXiv 2405.16884v3](https://arxiv.org/html/2405.16884v3)

**Anthropic prompt caching and prices (read 2026-10-17)**
- Multipliers:
  - cache write 1.25× base (5-minute TTL) or 2× (1-hour TTL);
  - cache read 0.1× base, but 0.05× on Opus 5.5 / Sonnet 5.5 and 0.025× on Fable/Mythos 5.1;
  - the TTL is refreshed free on each hit and counts from the start of the request.
- Up to 4 breakpoints; 20-block lookback.
- Prefix order is tools → system → messages, and any change invalidates everything after it.
- Minimum cacheable length: 512 tokens on 5.x models; 1,024–4,096 on older ones. Below the minimum, requests are silently not cached.
- Source: [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

Prices per MTok (input / 5m write / 1h write / hit / output):

| Model | Input | 5m write | 1h write | Hit | Output |
|---|---|---|---|---|---|
| Opus 5.5 | $4 | $5 | $8 | $0.20 | $20 |
| Sonnet 5.5 | $2 | $2.50 | $4 | $0.10 | $10 |
| Haiku 5.5 (≤100K-token prompts) | $0.10 | $0.125 | $0.20 | $0.01 | $0.50 |

- The Batch API gives −50% on input and output and stacks with caching.
- Source: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**OpenAI prompt caching (read 2026-10-17)**
- GPT-5.6 and later: 1,024-token minimum; cached input 0.1× (0.05× on GPT-6.1 Sol); cache write 1.25×; 30-minute retention.
- Earlier models: no write charge; in-memory retention of 5–10 minutes (up to 1 h) or 24-hour retention.
- `prompt_cache_key`: "aim for about 15 requests per minute in total across all prefixes using each key".
- Put stable instructions and shared reference material first.
- Source: [OpenAI prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching)

### Inferences

**Arithmetic (all inputs are estimates).**

Assumptions:
- D = 3,000 documents/day.
- One matching call per document. Each call carries:
  - static instructions/schema S ≈ 1,500 tokens;
  - the document's extracted candidate views ≈ 2 × 200 = 400 tokens.
- View card ≈ 150 tokens.
- On average 2 related objects per document.
- Output ≈ 300 tokens per call.

Tokens per call and per day:

| Arm | Input tokens per call | Input tokens per day |
|---|---|---|
| A, typical (15 views/object) | 1,900 + 2×15×150 = 6,400 | 19.2M |
| A, high (30 views/object) | 1,900 + 9,000 = 10,900 | 32.7M |
| Current draft (top-4 per candidate, ≤8 cards) | 1,900 + 8×150 = 3,100 | 9.3M |

Output is 0.9M tokens/day for every arm.

Uncached list price per day:

| Model | A typical | A high | Draft | Output |
|---|---|---|---|---|
| Sonnet 5.5 | $38 | $65 | $19 | +$9 |
| Haiku 5.5 | $1.9 | $3.3 | $0.9 | +$0.45 |
| Opus 5.5 | $77 | $131 | $37 | +$18 |

So the difference between A and the draft is about $20–50/day (~$600–1,400/month) on Sonnet 5.5, before caching or the Batch discount.

For comparison, reading the documents themselves at an assumed ~6K tokens per document is about 18M tokens/day, the same order of magnitude. The matching step is therefore not the dominant cost under either arm.

**When caching pays.**
- With a 5-minute write (1.25×) plus hits at 0.05×, a prefix pays back after one reuse within the TTL: 1.30 vs 2.00 units for two calls.
- A 1-hour write (2×) needs ≥2 reuses per hour.

**Our arrival rate per object.**
- 3,000 × 2 / 500 ≈ 12 document–object touches per object per day. Spread evenly, that is 0.5 per hour, so caching would rarely hit.
- Arrivals actually cluster: an earnings day brings the release, transcript, notes and news within hours.
- The design to get cache hits:
  1. a per-object queue that processes that object's documents back to back (this is also what correctness needs; see Section 5);
  2. the view list rendered in a fixed append-only order (by a program-owned creation sequence) before any document-specific content.
- A status change to an earlier view (closed, merged) invalidates the cached suffix from that view onward.
- Multi-object prompts share a prefix only up to the first object, so the primary object should come first.

**The static prefix.** S ≈ 1,500 tokens hits almost always. It saves ~4.3M token-equivalents per day, about $8/day on Sonnet 5.5.

**Latency.** At 3–11K-token prompts, prefill is not the bottleneck. The 17 s vs 1.4 s gaps in the literature come from 26K–115K-token prompts. Throughput is set by per-object serialization, not by prompt size.

**Merged calls.** Option A can be folded into the extraction call: the document plus the related objects' active views go in, and evidence-for-id, new views and merges come out. That removes a whole call. But it is "a call doing several jobs" (AGENTS.md §6), and it makes extraction quality depend on list length. It should be measured as its own arm, not assumed.

### Gaps
- I found no published cost comparison at our scale (5–30 items, thousands of decisions per day). All published comparisons are at 26K–115K-token histories or tool catalogues.
- There are no measured cache hit rates for document-stream workloads. Our hit rate must come from a census of stored publication times per object (inter-arrival times under 5 minutes and under 1 hour).
- All token sizes above (card size, candidate views per document, objects per document) are estimates. They should be replaced by a census of stored documents and views.

## 4. Hybrid designs: per-entity full context plus retrieval for cross-entity candidates; periodic offline consolidation

### Takeaway
The measured hybrids all follow one of two shapes:
- **cheap path first, expensive path only when needed:** Self-Route; ComEM's cheap-filter-then-select; tool search with deferred loading;
- **cheap online writes, consolidation moved offline:** LightMem's sleep-time update; Letta's sleep-time compute; KGGen's cluster pass.

Both report large cost savings at equal or better accuracy. For us this maps to:
- the full active list for each company object (small, bounded);
- retrieval only over the universe-wide pool of shared macro/theme views;
- a periodic offline pass that proposes reversible merges among near-duplicate views.

中文要点：被测量过的混合方案分两类——"先走便宜路径，必要时再走贵路径"（Self-Route、先粗筛再选择、按需加载工具）和"在线只做便宜写入，合并放到离线"（LightMem 睡眠期更新、Letta 睡眠期计算、KGGen 聚类）。对应到我们：单标的全量 + 跨标的宏观/主题观点检索 + 定期离线合并建议。

### Cited Findings
- **Self-Route.** The model first answers from RAG, or declares the question unanswerable, and falls back to LC only then. GPT-4o: 48.89 vs LC 48.67 at 61.40% of the tokens, answering 57.36% of queries on the RAG path. — [arXiv 2407.16833](https://arxiv.org/html/2407.16833)
- **ComEM.** A medium model ranks and filters to the top 4, then a strong LLM selects. F1 85.61 (GPT-3.5) / 86.42 (GPT-4o-mini) vs selecting alone 81.60 / 82.26, at $0.92 vs $1.71 per 4,000 pairs. — [arXiv 2405.16884v3](https://arxiv.org/html/2405.16884v3)
- **LightMem (ICLR 2026).**
  - Pipeline: sensory filter → topic-grouped short-term memory → long-term memory with an offline "sleep-time update" that "decouples consolidation from online inference".
  - LongMemEval: +2.09–6.40% accuracy over the strongest baseline with GPT, up to +7.67% with Qwen.
  - Cost: total tokens cut up to 38× (GPT) and API calls up to 30×; online-only tokens cut up to 105.9×.
  - Author-reported.
  - Source: [ICLR 2026 abstract](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a05b72653ec5b473732129829ae04195-Abstract-Conference.html); [arXiv 2510.18866](https://arxiv.org/pdf/2510.18866v4)
- **Sleep-time compute (Lin et al., Apr 2025; the technique Letta ships as sleep-time agents).**
  - About 5× less test-time compute for the same accuracy on Stateful GSM-Symbolic and Stateful AIME.
  - Up to +13% / +18% accuracy when sleep-time compute is scaled.
  - 2.5× lower average cost per query when amortized over related queries on the same context.
  - Benefit correlates with how predictable the queries are.
  - Source: [arXiv 2504.13171](https://arxiv.org/abs/2504.13171)
- **KGGen.** The offline cluster pass (k-means into 128-item clusters, then LLM dedup with top-16 BM25+embedding candidates) merged 22.4% of entities and 23% of edges on a 1M-character corpus. — [arXiv 2502.09956](https://arxiv.org/html/2502.09956)
- **LongMemEval design findings.** Two indexing changes help the retrieval half of any hybrid: fact-augmented keys (+9.4% recall@k) and time-aware query expansion (+6.8–11.3%). — [arXiv 2410.10813](https://arxiv.org/html/2410.10813)
- **Anthropic Tool Search (vendor).** A deferred-loading catalogue (retrieval) replaces "everything in context" once there are ~50+ items (58 tools ≈ 55K tokens). Accuracy: 49% → 74% (Opus 4) and 79.5% → 88.1% (Opus 4.5). — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- **LightRAG** offers `amerge_entities` as an explicit after-the-fact merge rather than resolving on insert. **GraphRAG** appends delta communities rather than re-clustering. — [utils_graph.py L3440](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/utils_graph.py#L3440); [update/communities.py](https://github.com/microsoft/graphrag/blob/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/update/communities.py)

### Inferences
- **Recommended shape (inference).**
  - **Per company object:** the full list of active views as cards (Option A), within a token budget (e.g. ≤8–12K; an estimate based on the NoLiMa effective lengths).
  - **Shared macro/theme views:** treat each theme as its own object with its own list. Documents classed as macro releases or official actions get the theme list in full when it is small. When a document mentions themes not in its class, retrieve top-k from the theme pool.
  - **Code** compares direction and horizon on the chosen view.
  - **Offline pass:** a daily or weekly per-object pass over active views (KGGen-style clusters, LLM chooses among candidates) proposes reversible merges.
  - This keeps the online decision in the measured full-context zone, and puts retrieval only where the item count is large.
- **Fallback.** A Self-Route-like fallback is cheap insurance: if an object's list exceeds the budget, drop to retrieve-top-k for that object only.
- **What the hybrid fixes.** The hybrid removes the retrieval-miss failure for company-level views, the class where top-20 retrieval misses the true match. It does not fix the LLM mis-choosing among similar cards. That class must be counted separately on stored cases.

### Gaps
- I found no published measurement of "per-entity full context plus cross-entity retrieval" as a combined design. Each half is measured separately.
- LightMem's and sleep-time compute's gains are on conversation-memory QA and math. Their transfer to claim dedup is unmeasured.
- I found no measured benefit of periodic consolidation passes on duplicate rates in a streaming store, other than KGGen's one-shot −22%.

## 5. Concurrency and ordering: two documents updating the same entries, and out-of-order arrivals

### Takeaway
The streaming builders serialize writes to the same key rather than merging concurrent LLM decisions:
- Graphiti requires episodes to be added "sequentially" and its MCP server queues per `group_id`;
- LightRAG takes a keyed lock per entity name and per sorted (src, tgt) pair while documents are processed in parallel;
- ATOM avoids the problem by making the merge an order-insensitive binary operation (exact match, cosine threshold, timestamp-list union), with no LLM in the merge.

Out-of-order arrival is handled by separating observation time from validity time (ATOM t_obs vs t_start/t_end; Graphiti valid_at vs created_at in the sibling notes), not by processing order.

中文要点：流式构建系统对同一键的写入一律串行化（Graphiti 按 group_id 排队、LightRAG 按实体名和排序后的边端点对加锁），而不是并发后再合并 LLM 判断；ATOM 把合并做成与顺序无关、不调用 LLM 的二元操作。乱序到达靠区分"观察时间"和"有效时间"处理，而不是靠处理顺序。

### Cited Findings
- **Graphiti, `add_episode` docstring:** "It's important that each episode is added sequentially and awaited before adding the next one… consider using FastAPI's background tasks or a dedicated task queue like Celery." — [graphiti.py L1404-L1418](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/graphiti.py#L1404-L1418)
- **Graphiti MCP server:** "Episodes for the same group_id are processed sequentially to avoid race conditions" (via a `QueueService`). — [graphiti_mcp_server.py L421](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/mcp_server/src/graphiti_mcp_server.py#L421)
- **Graphiti concurrency bug (issue #1676).** Concurrent `add_episode` calls for different group_ids could reassign the shared driver mid-execution and "silently persist episodes under the wrong graph". It was fixed by a request-scoped driver bundle. — [graphiti.py L1305-L1316, L1424-L1427](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/graphiti.py#L1305-L1316)
- **Graphiti in-call concurrency** is bounded by `SEMAPHORE_LIMIT` (default 20) per gather call. — [helpers.py L39-L47](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/helpers.py#L39-L47)
- **Graphiti bulk ingestion skips edge invalidation** ("For now we won't track edge invalidation"), so the contradiction logic depends on sequential ingestion. The edge-resolution code handles a contradicting fact that "starts later" (out-of-order arrival) by setting the new edge's `invalid_at`. — sibling notes, [bulk_utils.py](https://github.com/getzep/graphiti/blob/d50741d1bf463cbe3859eb73914cbff1b66839e6/graphiti_core/utils/bulk_utils.py)
- **LightRAG parallelism.**
  - Up to `MAX_PARALLEL_INSERT = 3` files in parallel. Merge phases run up to 2 × `MAX_ASYNC_LLM` tasks.
  - Each entity merge runs under `get_storage_keyed_lock([entity_name])`. Each relation merge runs under a lock on the sorted (src, tgt) pair, which gives a canonical lock key.
  - Sources: [README.md L318-L320](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/README.md); [operate.py L3714-L3840](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/operate.py#L3714-L3840); [constants.py L96-L97](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/constants.py#L96-L97)
- **LightRAG write ordering.**
  - The file-backed vector stores order redo-log replays by a `__write_seq__` token: a nanosecond wall-clock reading "bumped past the last value this process handed out".
  - It was added because `int(time.time())` ties "let a stale redo record overwrite a genuinely newer durable row".
  - The file lists its own limits: stamp order is not commit order, rows written before the token carry none, and two processes on one tick tie.
  - Merged entity descriptions are sorted by extraction timestamp.
  - Sources: [kg/write_seq.py](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/kg/write_seq.py); [operate.py L2596-L2600](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/operate.py#L2596-L2600)
- **ATOM.**
  - `parallel_atomic_merge` reduces a list of per-fact KGs pairwise in a thread pool until one remains, then merges that into the existing KG.
  - Relation matches union the t_obs, t_start and t_end timestamp lists (dual-time model).
  - The merge module is "13% of its total latency".
  - Sources: [atom.py L115-L147](https://github.com/AuvaLab/itext2kg/blob/840aba2c89d2f00c84c6b1da4c1c0b6637fa8d5d/itext2kg/atom/atom.py#L115-L147); [matcher.py L155-L162](https://github.com/AuvaLab/itext2kg/blob/840aba2c89d2f00c84c6b1da4c1c0b6637fa8d5d/itext2kg/atom/graph_matching/matcher.py); [ATOM paper](https://arxiv.org/html/2510.22590v2)
- **GraphRAG incremental update** is a batch workflow (`load_update_documents` → `update_entities_relationships` → `update_communities`…) over a delta. It has no concurrent writers. — [index/workflows](https://github.com/microsoft/graphrag/tree/5faaaf4f5685fa2056fa8c3bf9342cb089f2942f/packages/graphrag/graphrag/index/workflows)

### Inferences
- **Serialize per object.** One queue or actor per object, processing documents in publication-time order, is the industry norm (Graphiti per group_id, LightRAG per key). It also maximizes prompt-cache hits (Section 3).
- **Multi-object documents.** Two designs fit:
  - acquire the locks of all affected objects in sorted key order (LightRAG's sorted pair key avoids lock-order deadlock);
  - or split the document into per-object decisions, each run in its object's queue. Evidence attachment then commutes, and only "create new view" needs the cross-object check.
- **Shared macro/theme views** are the hot spot: many documents per day touch them. A theme queue of its own keeps those decisions serialized without blocking company queues.
- **Use a program-owned sequence for order, not the wall clock.** ATOM's order-insensitive merge only works because its merge has no LLM decision. Our decisions are LLM choices whose outcome depends on which views already exist, so they are order-dependent. The safe rule is: process in a program-owned sequence per object.
  - LightRAG's `__write_seq__` is a wall-clock workaround whose file states its own limits. AGENTS.md §3 says to order by a sequence the program owns.
- **Late documents.** A document that arrives late (publication time earlier than already-processed ones) should be judged against the views as of its publication time, or at least have its evidence dated by publication time. Status transitions (confirm, falsify, expire) should then be recomputed from dated evidence, not from processing order, as in Graphiti's valid_at/created_at split.

### Gaps
- I found no published measurement of duplicate-creation rates caused by concurrency (two documents creating the same new view at once) in any system. The mechanism is only addressed by serialization.
- Mem0, Letta and Cognee concurrency handling was not re-read in this pass. The sibling notes cover Letta's git-worktree memory edits qualitatively.
- I did not find how any system re-judges earlier decisions when a late document arrives (re-running the dedup decision vs only re-dating). Graphiti only adjusts invalidation dates.
