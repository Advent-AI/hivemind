# Embedding models, vector stores, model versioning and cost for a financial "views database" (research notes, seen 2026-10-17)

All prices and model states below were read on 2026-10-17 unless stated otherwise. Embedding prices and model names change every few months; treat every price as "as seen on that date" and re-check before committing. "Vendor-reported" marks numbers published by the company that sells the model.

## Q1. Embedding models in 2025–2026 and their fit for financial text

### Takeaway
On the only independent finance embedding benchmark found (FinMTEB, EMNLP 2025), general LLM-based API models are at the top for English: voyage-3-large and the research model Fin-E5 tie overall, and voyage-3-large leads on retrieval. Voyage's own finance model (voyage-finance-2, 2024) is now "Legacy", and its recommended replacement is voyage-4. For Chinese, Qwen/BGE open models lead FinMTEB. One FinMTEB result matters directly for view de-duplication: on financial semantic-similarity tasks a bag-of-words baseline beats every dense model. So dense vectors alone are a weak judge of "same claim", and lexical matching plus an LLM decision belongs in the design.

### Cited Findings

**Independent benchmark: FinMTEB**
- FinMTEB (Tang & Yang; arXiv 2502.10990, submitted 2025-02-16, accepted to EMNLP 2025): 64 finance datasets, 7 task types, English and Chinese. Text types include financial news, annual reports, ESG documents, regulatory filings and earnings transcripts. 15 models evaluated. — [arXiv abstract](https://arxiv.org/abs/2502.10990)
- Key findings: (1) scores on general benchmarks have little correlation with finance scores ("The ranking correlation is not statistically significant (p-values all greater than 0.05)"); (2) finance-adapted models consistently beat general ones; (3) "The simple BOW model (achieving a score of 0.4845) outperforms all evaluated dense embedding architectures on STS", which the authors attribute to the standardized language of financial text. — [arXiv abstract](https://arxiv.org/abs/2502.10990); [arXiv HTML](https://arxiv.org/html/2502.10990)
- English averages (paper Table 1): Fin-E5 (7B) 0.6767, voyage-3-large 0.6765, text-embedding-3-large 0.6613, e5-mistral-7b-instruct 0.6475, gte-Qwen1.5-7B-instruct 0.6427, NV-Embed v2 0.6322, bge-large-en-v1.5 0.6301. — [arXiv HTML](https://arxiv.org/html/2502.10990)
- FinMTEB leaderboard, English retrieval: voyage-3-large 0.746, Fin-E5 0.711, text-embedding-3-large 0.711. Chinese retrieval: gte-Qwen1.5-7B-instruct 0.642, bge-m3 0.624, bge-large-zh-v1.5 0.607. Chinese overall: gte-Qwen1.5-7B-instruct 0.648, bge-large-zh-v1.5 0.634. No date is shown on the page. — [FinMTEB leaderboard (HF Space)](https://financemteb-finmteb.hf.space)
  - Data-quality flag: the same leaderboard lists "Qwen3-Reranker-8B" at 0.998 overall for Chinese. That is a reranker, not an embedding model, and the score is implausible; treat it as a leaderboard error. The leaderboard text says 63 datasets while the paper says 64.
  - The paper does not evaluate the 2025–2026 models (Voyage 4, Qwen3-Embedding, Gemini Embedding 2, Cohere Embed 4/5). No independent finance-domain comparison of them was found.
- Fin-E5 was trained with persona-based synthetic data. — [arXiv abstract](https://arxiv.org/abs/2502.10990)

**Voyage AI (MongoDB) — the provider Anthropic points to**
- Current generation (Voyage 4, released 2026-01-15): voyage-4-large, voyage-4 and voyage-4-lite (API), plus voyage-4-nano (open weights, Apache 2.0, on Hugging Face). All have 32,000-token context and dimensions of 256/512/1024/2048 (1024 is the default for the API models, 2048 for nano). Output dtypes are float, int8, uint8, binary and ubinary. — [Voyage docs: embeddings](https://docs.voyageai.com/docs/embeddings); [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- voyage-4-large uses a mixture-of-experts architecture; Voyage says serving cost is "40% lower than comparable dense models". (Vendor-reported.) — [Voyage 4 blog](https://blog.voyageai.com/2026/01/15/voyage-4/)
- Voyage 4 shared embedding space: all four models produce compatible embeddings, which allows "asymmetric retrieval" (for example, index with voyage-4-large and query with voyage-4-lite). Voyage's words: "Upgrade to voyage-4 or voyage-4-large for query embeddings as your accuracy requirements evolve, without re-vectorizing documents." — [Voyage 4 blog](https://blog.voyageai.com/2026/01/15/voyage-4/); [MongoDB product update](https://www.mongodb.com/products/updates/the-voyage-4-series-now-available)
- Vendor-reported margins for voyage-4-large: +1.87% over voyage-4, +4.80% over voyage-4-lite, +8.20% over Gemini Embedding 001, +8.20% over Cohere Embed v4, +14.05% over OpenAI v3 large. No Qwen3-Embedding comparison. The blog says finance is among the evaluated domains but gives no separate finance number. (Extraction flag: the two identical 8.20% margins may be an extraction error; re-check the blog's table.) — [Voyage 4 blog](https://blog.voyageai.com/2026/01/15/voyage-4/)
- voyage-finance-2 (released 2024-06-03): 32K context, 1024 dimensions, float output only. Vendor-reported average NDCG@10 over 11 finance retrieval datasets (including FinanceBench, TAT-QA, ConvFinQA, FinQA, FiQA): 0.831, against OpenAI v3-large at 0.762 and Cohere English v3 at 0.713. — [voyage-finance-2 blog](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/); [Voyage docs](https://docs.voyageai.com/docs/embeddings)
- Voyage itself reports (vendor-reported) that voyage-3-large beats its domain-specific models, voyage-finance-2 included; only voyage-code-3 kept an edge in its own domain. Evaluation: 100 datasets across 8 domains. — [voyage-3-large blog](https://blog.voyageai.com/2025/01/07/voyage-3-large/)
- Lifecycle: voyage-finance-2, voyage-3.5 and voyage-3-large became "Legacy" on 2026-01-15. The recommended replacement for voyage-finance-2 and voyage-3.5 is voyage-4; for voyage-3-large it is voyage-4-large. — [MongoDB Voyage model lifecycle](https://www.mongodb.com/docs/voyageai/models/lifecycle/)
- Quantization and dimension trade-off (vendor-reported, voyage-3-large): int8 at 1024 dimensions scores "only 0.31% below" float at 2048 dimensions with 8x less storage. Binary at 512 dimensions beats OpenAI-v3-large float at 3072 dimensions by 1.16% at "1/200 the storage cost". — [voyage-3-large blog](https://blog.voyageai.com/2025/01/07/voyage-3-large/)
- Other current Voyage models: voyage-context-4 (contextualized chunk embeddings; 120K tokens with auto-chunking), voyage-multimodal-3.5, rerank-3 and rerank-3-lite (32K context; rerank-3 announced 2026-09-30). — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)

**OpenAI**
- text-embedding-3-small: 1536 dimensions, 8192 input tokens, MTEB 62.3%. text-embedding-3-large: 3072 dimensions, 8192 tokens, MTEB 64.6%. Both can be shortened with the `dimensions` parameter. Vectors are normalized to length 1. Tokenizer is cl100k_base. Training knowledge stops at September 2021. No newer OpenAI embedding model is listed. — [OpenAI embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)

**Google Gemini**
- gemini-embedding-2: stable, updated April 2026. Inputs are text, image, video, audio and PDF. 8,192-token input limit. Dimensions 128–3072 (default 3072; recommended 768/1536/3072), auto-normalized when truncated. Task instructions go in the prompt; there is no `task_type` parameter. — [Gemini embeddings docs](https://ai.google.dev/gemini-api/docs/embeddings)
- gemini-embedding-001: text only, 2,048-token limit, 128–3072 dimensions (manual normalization below 3072), uses the `task_type` parameter. — [Gemini embeddings docs](https://ai.google.dev/gemini-api/docs/embeddings)

**Cohere**
- Cohere docs list embed-v5.0-pro and embed-v5.0-fast (128k context, 256–2048 dimensions; text, images and mixed PDFs), embed-v4.0 (128k, 256–1536), and the v3 English and multilingual models (512 context, 1024 or 384 dimensions). — [Cohere embed docs](https://docs.cohere.com/docs/cohere-embed)
- Embed 5 launched on 2026-09-30, per third-party coverage. Pro is for indexing and Fast for queries, and the two share one vector space (Cohere's tests: −1.6 points when querying with Fast). 100+ languages. Cohere claims gains over Embed 4 on financial filings. Third-party pages quote vendor-reported FinanceBench retrieval scores of 80.1 (Pro) and 80 (Fast). These details come from secondary sources, not a Cohere primary page. — [The New Stack](https://thenewstack.io/cohere-embed-pro-fast/); [gradually.ai](https://www.gradually.ai/en/ai-models/cohere-embed-v5-pro/); [digitalapplied](https://www.digitalapplied.com/blog/cohere-embed-5-pro-fast-embedding-models)

**Open-weight models (self-hostable)**
- Qwen3-Embedding: 0.6B, 4B and 8B; 32K context; Matryoshka dimensions 32–4096 (8B); instruction-aware; 100+ languages; Apache 2.0. Self-reported scores for the 8B model: MTEB multilingual 70.58 ("No.1" as of 2025-05-24), MTEB English v2 75.22, C-MTEB (Chinese) 73.84. Not evaluated on FinMTEB in the sources found. — [Qwen3-Embedding-8B model card](https://huggingface.co/Qwen/Qwen3-Embedding-8B)
- BGE-M3: 1024 dimensions, 8192 tokens. It produces dense, sparse (lexical weights) and ColBERT-style multi-vector outputs from one model. 100+ languages, MIT license; the card recommends a "hybrid retrieval + re-ranking" pipeline. It is #2 on FinMTEB Chinese retrieval (0.624). — [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3); [FinMTEB leaderboard](https://financemteb-finmteb.hf.space)
- NV-Embed-v2: 8B, 4096 dimensions, 32K tokens, MTEB 72.31 (#1 as of 2024-08-30), but CC-BY-NC-4.0, so no commercial use. On FinMTEB English it scores 0.6322, below e5-mistral and gte-Qwen. — [NV-Embed-v2 card](https://huggingface.co/nvidia/NV-Embed-v2); [arXiv HTML](https://arxiv.org/html/2502.10990)
- Jina: jina-embeddings-v4 (32K, 2048 dimensions with Matryoshka down to 128) is under the Qwen Research License. jina-embeddings-v5-text-small (32K, 1024 dimensions) and v5-text-nano (8K, 768 dimensions) are CC BY-NC 4.0. This comes from search snippets of jina.ai pages and was not fetched in full. — [jina-embeddings-v4](https://jina.ai/en-US/models/jina-embeddings-v4/); [jina-embeddings-v5-text-small](https://jina.ai/models/jina-embeddings-v5-text-small/)
- voyage-4-nano: open weights under Apache 2.0, 32K context, 2048 default dimensions, in the same embedding space as the Voyage 4 API models. — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings); [HF voyage-4-nano](https://huggingface.co/voyageai/voyage-4-nano)
- Finance-tuned open models also exist, e.g. FinModernBERT-embed-large; not evaluated here. — [HF FinModernBERT-embed-large-v1](https://huggingface.co/BatuhanECB/FinModernBERT-embed-large-v1)

**Prices (USD per 1M input tokens, seen 2026-10-17)**

| Model | Price | Batch | Free allowance | Source |
|---|---|---|---|---|
| voyage-4-large | $0.12 | −33% | 200M tokens | [Voyage pricing](https://docs.voyageai.com/docs/pricing) |
| voyage-4 | $0.06 | −33% | 200M | same |
| voyage-4-lite | $0.02 | −33% | 200M | same |
| voyage-context-4 | $0.12 | −33% | 200M | same |
| voyage-finance-2 (Legacy) | $0.12 | −33% | 50M | same |
| voyage-multilingual-2 | $0.12 | −33% | 50M | same |
| voyage-3.5 / 3.5-lite (Legacy) | $0.06 / $0.02 | −33% | none | same |
| voyage-3-large (Legacy) | $0.18 | −33% | none | same |
| rerank-3 / rerank-3-lite | $0.05 / $0.02 | −33% | 200M | same |
| OpenAI text-embedding-3-small | $0.02 | not shown on official page; third parties say $0.01 | — | [OpenAI pricing](https://developers.openai.com/api/docs/pricing); batch per [costgoat](https://costgoat.com/pricing/openai-embeddings) (unverified) |
| OpenAI text-embedding-3-large | $0.13 | (third parties: 50% off) | — | [OpenAI pricing](https://developers.openai.com/api/docs/pricing) |
| Gemini Embedding 2 (text) | $0.20 | $0.10 | free tier exists | [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Cohere embed-v4.0 | $0.12 (aggregator) | — | — | [getmaxim](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/cohere/model/embed-v4.0) (not a Cohere page) |
| Cohere Embed 5 Pro / Fast | $0.12 / $0.08 (third-party) | — | — | [The New Stack](https://thenewstack.io/cohere-embed-pro-fast/) (Cohere's pricing page shows only per-instance prices for Embed 5: $3–5/hour, [Cohere pricing](https://cohere.com/pricing)) |

- Voyage: "Free token credits do not apply to Batch API usage." Batch limits: 1,000 texts per request, with a token cap per request of 1M for the lite models, 320K for standard and 120K for large. — [Voyage pricing](https://docs.voyageai.com/docs/pricing); [Voyage docs](https://docs.voyageai.com/docs/embeddings)

### Inferences
- For a new build in October 2026, voyage-finance-2 is a poor choice even though it is "the finance model". It is Legacy, offers float at 1024 dimensions only (no Matryoshka, no int8/binary), Voyage's own numbers show its general models surpassing it, and it sits outside the Voyage 4 shared space (the shared-space claim names only the four Voyage 4 models).
- The strongest evidence-backed API choice is the Voyage 4 family. Its predecessor tops independent FinMTEB English retrieval; it is the provider Anthropic documents; it offers int8/binary and Matryoshka output; and its shared space lets the expensive model be used for stored views while cheaper models (or the open-weight voyage-4-nano) handle queries. Voyage-4's lead over its predecessor on finance text is vendor-reported only.
- Chinese/English: the documents are English and the team works in Chinese. If views are written or stored in Chinese and matched against English documents, the model must handle cross-lingual retrieval. Voyage 4, Cohere Embed 5, Qwen3-Embedding and BGE-M3 all claim multilingual support, but the only Chinese finance evidence (FinMTEB-ZH) covers older open models. The cheapest way around this is to store one canonical embedding text per view in English (the documents' language), keep the Chinese text for display, and test cross-lingual matching on a labeled sample.
- The FinMTEB STS finding (bag-of-words beats dense) is a direct warning for de-duplication, which is an STS-like task. Similarity between two short financial claims ("AAPL services margin will expand" vs "AAPL services margin will contract") is likely to be high under dense vectors even when the direction flips. Structured fields (affected object, direction) should be hard filters or code-checked fields, not left to the vector; vectors should only gather candidates, and the LLM (or code) decides.
- Self-host fallback: Qwen3-Embedding-0.6B or 4B (Apache 2.0, strong Chinese) or BGE-M3 (MIT, built-in sparse output) are the licensable open options. NV-Embed-v2 and Jina v5 are non-commercial; Jina v4 is under a research licence.

### Gaps
- No independent benchmark of Voyage 4, Qwen3-Embedding, Gemini Embedding 2 or Cohere Embed 5 on finance text (FinMTEB or FinanceBench retrieval) was found. All of their finance claims are vendor-reported.
- No benchmark was found for English↔Chinese cross-lingual retrieval on financial text.
- voyage-4-nano's parameter count and quality relative to voyage-4-lite were not found.
- Gemini embedding-001's current price is not on the current pricing page.
- Cohere Embed 5 price, FinanceBench numbers and shared-space claim were not confirmed from a Cohere primary page.
- The FinMTEB per-task breakdown (for example STS and retrieval for each model) was not reliably extracted; only averages and leaderboard retrieval scores are cited above.

## Q2. What Anthropic recommends for embeddings, and integration notes

### Takeaway
Anthropic sells no embedding model. Its docs name Voyage AI (now part of MongoDB) and list the Voyage 4 family as the recommended general models and voyage-finance-2 as the finance model. Keys now come from MongoDB Atlas. Anthropic's own retrieval research shows that combining embeddings with BM25 and a reranker clearly beats embeddings alone.

### Cited Findings
- "Anthropic does not offer its own embedding model. One embeddings provider with a wide variety of models and capabilities is Voyage AI by MongoDB." The page adds that "you should assess a variety of embeddings vendors". — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- Recommended general models: voyage-4-large (best quality), voyage-4 (balanced), voyage-4-lite (lowest latency and cost). Finance tasks: voyage-finance-2. Chunk and document-level retrieval: voyage-context-4. — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- Integration notes from the same page:
  - API keys are created in MongoDB Atlas ("AI Model APIs"). The endpoint is `https://ai.mongodb.com/v1/embeddings`. The `voyageai` Python package must be ≥0.3.7 to use Atlas keys, and the TypeScript client needs `environment` set to `https://ai.mongodb.com/v1`. Voyage is also on AWS Marketplace.
  - Always set `input_type` to "query" or "document" for retrieval ("Do not omit `input_type` or set `input_type=None`"). It prepends "Represent the query for retrieving supporting documents: " or "Represent the document for retrieval: ".
  - Vectors are normalized to length 1, so dot product equals cosine similarity.
  - Matryoshka: stored vectors can be shortened by keeping the leading dimensions and then re-normalizing.
  - `output_dtype` controls quantization (int8 cuts size 4x, binary 32x).
  - Token counts can be checked with `count_tokens`.
  — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings); [MongoDB tokenization](https://www.mongodb.com/docs/voyageai/tutorials/tokenization/)
- Note: legacy MongoDB model states say voyage-finance-2 is "Available only via ai.mongodb.com". — [MongoDB lifecycle](https://www.mongodb.com/docs/voyageai/models/lifecycle/)
- Anthropic "Contextual Retrieval" (2024-09-19). Retrieval failure is measured as 1 − recall@20. Contextual embeddings cut failures by 35% (5.7%→3.7%); adding contextual BM25 cut them by 49% (→2.9%); adding a reranker cut them by 67% (→1.9%). Gemini and Voyage embeddings were "particularly effective". Top-20 chunks beat top-10 and top-5. Generating the context costs about $1.02 per million document tokens with prompt caching. Knowledge bases under 200,000 tokens can go straight into the prompt with no RAG. — [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

### Inferences
- There is a mismatch inside Anthropic's page: the FAQ still recommends voyage-finance-2 for finance, while MongoDB's lifecycle page marks it Legacy with voyage-4 as its replacement. Follow the lifecycle page for a new build.
- For the views use case, the Contextual Retrieval result supports a hybrid design (BM25 + dense + optional rerank) over dense-only candidate retrieval. It matches the FinMTEB STS finding in Q1.
- In a credential-sensitive project (AGENTS.md §9), the Voyage key is a MongoDB Atlas key and should be handled like the Anthropic key: an environment or secret store, never logs or arguments.

### Gaps
- No Anthropic-specific integration (for example a Claude tool that calls Voyage directly) was found beyond the docs page and the cookbook pointer to a Pinecone RAG recipe.

## Q3. Vector stores at 10^3–10^6 vectors

### Takeaway
At this scale no separate vector service is needed. 20,000 views fit in about 80 MB at 1024 dimensions in float32 and can be searched exactly (brute force). pgvector, if the system already runs Postgres, or an embedded store (sqlite-vec with FTS5, or LanceDB) covers vectors, metadata filters and BM25-style hybrid search in one process or database. Qdrant, Elasticsearch/OpenSearch and Chroma Cloud add a service without a need at this size.

### Cited Findings
- **pgvector** (latest 0.8.7):
  - Types and dimension limits: `vector` up to 16,000 dimensions, but HNSW and IVFFlat indexes only up to 2,000; `halfvec` indexes up to 4,000; `bit` up to 64,000; `sparsevec` (HNSW, ≤1,000 non-zero elements).
  - Distances: L2, inner product, cosine, L1, Hamming, Jaccard.
  - Exact search gives "perfect recall"; HNSW and IVFFlat are approximate.
  - Filtering: with approximate indexes the filter is applied *after* the index scan. Iterative index scans (since 0.8.0; `strict_order` or `relaxed_order`) fix filtered queries that return too few rows.
  - Hybrid search: combine with Postgres full-text search through Reciprocal Rank Fusion or a cross-encoder.
  — [pgvector README](https://github.com/pgvector/pgvector)
- **sqlite-vec**: "pre-v1, so expect breaking changes!" Supports float, int8 and binary vectors, and metadata, auxiliary and partition-key columns for filtering. The README mentions brute force plus IVF and DiskANN indexes. Pure C with no dependencies; runs on Linux, macOS, Windows and WASM. Backed by Mozilla Builders and others. — [sqlite-vec README](https://github.com/asg017/sqlite-vec)
- sqlite-vec plus FTS5 hybrid: the author (Alex Garcia) published SQL that fuses FTS5 and sqlite-vec results with RRF. — [Simon Willison, 2024-10-04](https://simonwillison.net/2024/Oct/4/hybrid-full-text-search-and-vector-search-with-sqlite/)
- **LanceDB**: OSS runs in-process against a local directory (no server). Hybrid search combines vector search and a full-text index, with RRF as the default reranker (Cohere, CrossEncoder and others are pluggable). Prefiltering is the default; postfiltering is available. — [LanceDB hybrid search docs](https://docs.lancedb.com/search/hybrid-search)
- **Qdrant**: hybrid queries via `prefetch` (dense + sparse) fused with RRF or DBSF. Supports multiple named vectors per point (useful for model migration) and payload filtering. — [Qdrant hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- **Chroma**: supports dense, sparse (BM25, SPLADE) and hybrid search with RRF, but the Search() and Schema() APIs that carry hybrid search are shown with `CloudClient()` and described as Chroma Cloud features. Local/OSS availability is not stated. — [Chroma sparse vector search](https://www.trychroma.com/project/sparse-vector-search); [Chroma docs](https://docs.trychroma.com/docs/overview/introduction)
- **Elasticsearch / OpenSearch**: per a third-party write-up, Elasticsearch's RRF retriever has been Enterprise-tier only, from its 8.8 preview through 8.16 GA and into 9.x; on Basic it returns a 403 license error. OpenSearch ships RRF and score normalization under Apache 2.0. (Not confirmed on an Elastic primary page; the Elastic RRF docs fetch failed.) — [dev.to (u11d)](https://dev.to/u11d/reciprocal-rank-fusion-on-free-elasticsearch-licensing-workarounds-and-the-opensearch-alternative-56jk); [Elastic subscriptions PDF 2026-03-03](https://www.elastic.co/pdf/subscriptions-2026-03-03.pdf)
- Storage reduction from quantization: int8 is 4x smaller and binary 32x smaller than float32. — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)

### Inferences
- Sizing (arithmetic, estimate):
  - 1 vector of 1024 float32 dimensions = 4 KB. 20,000 views ≈ 82 MB (164 MB at 2048 dimensions).
  - 1M evidence items at 1024 dimensions ≈ 4.1 GB float32, 2.0 GB halfvec, 1.0 GB int8, 128 MB binary (plus index overhead).
  - Exact search over 20k × 1024 is about 20M multiply-adds per query, milliseconds on one CPU. An ANN index is unnecessary for views and only becomes useful for evidence or chunks beyond roughly 10^5–10^6 rows.
- Dimension compatibility with pgvector indexes:
  - voyage-4 at 1024 dimensions fits a `vector` HNSW index.
  - 2048-dimension Voyage, 3072-dimension Gemini or OpenAI large, or 4096-dimension Qwen3-8B vectors need `halfvec` (≤4,000) or Matryoshka truncation.
  - Qwen3-8B at 4096 must be truncated to index at all.
  - Exact search has no such limit.
- Filtering matters more than the ANN algorithm. Candidate views should be restricted first by structured fields (affected object id, asset class, status). With pgvector exact search or LanceDB's default prefilter this is correct by construction. With pgvector HNSW the post-filter can drop results unless iterative scans are on.
- Ranking by "need a separate service": none (sqlite-vec, LanceDB) < existing database (pgvector) < service (Qdrant, OpenSearch, Elasticsearch, Chroma server or Cloud). For a single-machine research system the first two are adequate. sqlite-vec's pre-v1 status means pinning its version.
- Hybrid BM25 + vector in one place: Postgres (tsvector + pgvector + RRF in SQL), SQLite (FTS5 + sqlite-vec + RRF in SQL) and LanceDB (built in) all cover it without extra infrastructure. On Elasticsearch, native RRF needs a paid tier.

### Gaps
- No independent latency or recall benchmark at 10^4–10^6 scale comparing pgvector, sqlite-vec and LanceDB was fetched. Choices above rest on documented features plus arithmetic.
- Qdrant's local/embedded Python mode (without a server) was not confirmed in the fetched pages.
- Whether Chroma's hybrid Search API now works in local/OSS mode was not confirmed (the page is undated).
- sqlite-vec's ANN index types (IVF, DiskANN) were listed in the README, but their maturity (experimental vs stable) was not checked.

## Q4. Changing embedding models later

### Takeaway
Vectors from different models (or incompatible generations of one vendor) cannot be compared, so a model change means re-embedding everything the new queries must search. The cheap insurance is to store the model id, dimension, dtype, input_type and a hash of the exact embedded text with every vector, and to run new and old vectors side by side (a second column or named vector, dual-write, backfill, validate, switch). At this scale the re-embed bill is small; the real cost is validation. Shared-space families (Voyage 4; Cohere Embed 5 Pro/Fast as reported) reduce churn within a family, not across families.

### Cited Findings
- Gemini: embeddings from gemini-embedding-001 and gemini-embedding-2 are incompatible; upgrading "requires re-embedding all existing data". — [Gemini embeddings docs](https://ai.google.dev/gemini-api/docs/embeddings)
- Voyage 4: all four Voyage 4 models share one space, so query embeddings can be upgraded "without re-vectorizing documents". This covers the Voyage 4 generation only. — [Voyage 4 blog](https://blog.voyageai.com/2026/01/15/voyage-4/)
- Cohere Embed 5 Pro and Fast share a vector space (third-party report). — [The New Stack](https://thenewstack.io/cohere-embed-pro-fast/)
- Voyage lifecycle policy: Legacy → Deprecated needs 12 months' notice for embedding models, and Deprecated → Retired another 6 months, so at least 18 months from Legacy to retirement. voyage-finance-2, voyage-3.5 and voyage-3-large went Legacy on 2026-01-15. No retirement dates are published yet. — [MongoDB lifecycle](https://www.mongodb.com/docs/voyageai/models/lifecycle/)
- General principle: "A vector from model v1 and a vector from model v2 — even for the identical document — sit in different spaces, so cosine similarity between them is meaningless … there is no in-place transform that makes the old vectors valid." The recommended pattern is blue-green: add a new column or collection, backfill, dual-write new ingests, validate on held-out queries, then switch. (From search snippets of these pages.) — [tianpan.co, 2026-07-05](https://tianpan.co/blog/2026-07-05-retiring-an-embedding-model-reindex-without-downtime); [Zilliz FAQ](https://zilliz.com/ai-faq/change-embedding-model-without-reindexing)
- Qdrant migration guide. Option 1 is blue-green with a new collection: dual writes, then backfill by scroll and re-embed, then switch an alias. It works as-is only for upserts; deletes and partial updates must pause or get extra logic. Option 2, preferred for v1.18+, adds a second named vector to the same collection: dual-write, `update_vectors` to backfill while keeping payloads and IDs, switch the query vector name, delete the old vector. Validate with labeled queries (Recall@10, MRR, nDCG@10) before switching. — [Qdrant embedding-model migration](https://qdrant.tech/documentation/tutorials-operations/embedding-model-migration/)
- Drift-Adapter (Vejendla, EMNLP 2025, arXiv 2509.23471) learns a small mapping from new-model query vectors into the old space (orthogonal Procrustes, low-rank affine or residual MLP), trained on a small sample of paired embeddings. It recovers 95–99% of full re-embedding Recall@10 and MRR, adds under 10 µs per query, and costs over 100x less than re-indexing, tested on MTEB corpora and a CLIP upgrade (~1M items). — [arXiv 2509.23471](https://arxiv.org/abs/2509.23471)
- Embedding text depends on `input_type` (Voyage prepends different prompts), so the same text embedded as "query" and as "document" gives different vectors. — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- Matryoshka truncation of stored vectors (keep the leading dimensions, then re-normalize) changes dimension without re-embedding, within the same model. — [Anthropic embeddings page](https://platform.claude.com/docs/en/build-with-claude/embeddings)

### Inferences
- Per-vector record (minimum) so that vectors from two models are never compared by accident: `embedding_model` (exact id, e.g. `voyage-4-large`), `embedding_space` (e.g. `voyage-4`, so nano, lite, standard and large count as one space while 3.x and finance-2 each count as their own), `dimension`, `dtype` (float, int8, binary), `input_type` and prompt template, `normalized`, `text_sha256` (hash of the exact string sent, including any template or field concatenation), and `embedded_at` (for audit only, never ordering). A query must refuse to compare vectors whose `embedding_space`, `dimension` or `dtype` differ. This is enforced in code, not left to convention (AGENTS.md §3 "Code over prose", "Identity").
- Changing the embedding template (which fields of a view are concatenated) is a model change for this purpose. Hashing the exact text sent detects it.
- For a views database, re-embedding the views is trivial (see Q5: under $1 for 20k views). The question is whether historical evidence and document chunks must also move. Keep the source text for everything embedded so re-embedding is always possible; never keep only vectors.
- Drift-Adapter-style mapping is a stopgap for large corpora. At 10^4–10^6 vectors a full re-embed costs dollars, so a learned adapter adds risk without a matching saving.
- Validation is the real cost of a switch. A labeled set of (document, correct view or "new") pairs from production is the measuring stick, and must exist before the first model change (AGENTS.md §7).

### Gaps
- No vendor guarantee was found that a future Voyage 5 will share the Voyage 4 space. The shared-space property should be assumed to hold only within a named generation.
- tianpan.co and Zilliz were cited from search snippets, not full fetches.

## Q5. Cost estimate inputs and a worked example (3,000 documents/day, 20,000 views)

### Takeaway
Embedding is cheap at this scale (estimate). Embedding every chunk of 3,000 mixed financial documents a day costs about $0.15–$1.50 a day ($4–$45 a month) at October 2026 list prices, depending on model. Embedding all 20,000 views costs under $1 one-time, and re-embedding everything on a model change is a two- or three-figure dollar amount per year of stored chunks. The LLM duplicate/merge/new decisions, not the embeddings, will dominate the bill.

### Cited Findings
- Voyage tokenizer: about 1.2–1.5 tokens per English word and about 5 characters per token. Voyage produces 1.1–1.2x as many tokens as `tiktoken` for the same text. No guidance is given for Chinese. — [MongoDB Voyage tokenization](https://www.mongodb.com/docs/voyageai/tutorials/tokenization/)
- 10-K length: the average word count rose from 30,000 (2000) to 42,000 (2013), per the WSJ CFO Journal via NYSSCPA, 2015-06-02. Possibly outdated. — [NYSSCPA](https://nysscpa.org/news/1046127-10-ks-reaching-novel-length-2015-06-02)
- Earnings call transcripts: in a dataset of 33,362 S&P 500 transcripts (2005–2025) the median length is 53,734 characters (max 244,695). — [HF kurry/sp500_earnings_transcripts README](https://huggingface.co/datasets/kurry/sp500_earnings_transcripts/blob/f3ded372da8d18dc6ad98955c4558e34b5fe6d45/README.md)
- Prices per 1M tokens (seen 2026-10-17): voyage-4-lite $0.02, voyage-4 $0.06, voyage-4-large $0.12 (Batch −33%; 200M free tokens for the Voyage 4 family); OpenAI 3-small $0.02 and 3-large $0.13; Gemini Embedding 2 $0.20 ($0.10 batch); Voyage rerank-3 $0.05. — [Voyage pricing](https://docs.voyageai.com/docs/pricing); [OpenAI pricing](https://developers.openai.com/api/docs/pricing); [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Voyage per-request caps: 1,000 texts; 320K tokens for voyage-4 and 120K for voyage-4-large. — [Voyage docs](https://docs.voyageai.com/docs/embeddings)
- Anthropic's Contextual Retrieval uses chunks of "several hundred tokens" and top-20 retrieval. Prompt-cached context generation costs about $1.02 per 1M document tokens. — [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

### Inferences
All figures in this section are estimates built on the cited prices and lengths plus assumptions labeled as such.

**Input assumptions (estimates)**
- Document mix per day (assumed; no source for the stream's actual mix): 2,400 short items (news, official actions, macro releases) at about 1,000 tokens each; 450 medium items (earnings releases, 8-Ks, sell-side notes) at about 4,000; 120 transcripts at about 11,000 (53,734 characters ÷ 5); 30 long filings (10-K/10-Q) at about 55,000 (42,000 words × 1.3, likely low given the 2013 data).
  - Total ≈ 2.4M + 1.8M + 1.3M + 1.65M ≈ **7.2M tokens/day** ≈ 215M/month ≈ 2.6B/year.
- View embedding text (claim + affected objects + direction + short rationale): about 250 tokens. 20,000 views ≈ 5M tokens.
- Evidence item text: about 150 tokens.
- Extracted claims per document, if only claims are embedded as queries: about 8 claims × 80 tokens. 3,000 docs ≈ 1.9M tokens/day.

**Path A — embed every chunk of every document** (7.2M tokens/day)

| Model (price/1M) | Per day | Per month (30 d) | Per year |
|---|---|---|---|
| voyage-4-lite ($0.02) / OpenAI 3-small ($0.02) | $0.14 | $4.3 | $53 |
| voyage-4 ($0.06) | $0.43 | $13 | $158 |
| voyage-4-large ($0.12) / voyage-finance-2 ($0.12) / Cohere Embed 5 Pro ($0.12, unverified) | $0.86 | $26 | $315 |
| OpenAI 3-large ($0.13) | $0.94 | $28 | $342 |
| Gemini Embedding 2 ($0.20; batch $0.10) | $1.44 ($0.72) | $43 ($22) | $526 ($263) |

- The Voyage 4 family's 200M free tokens cover about 28 days of Path A. Whether the allowance is one-time per account was not stated, so treat it as one-time.

**Path B — embed only the claims extracted from each document** (1.9M tokens/day): about $0.11/day ≈ $3.5/month on voyage-4, or $0.23/day on voyage-4-large.

**Views**: 20,000 × 250 tokens = 5M tokens, which is $0.30 on voyage-4 or $0.60 on voyage-4-large one-time. New views at a few hundred a day cost cents per month.

**Re-embedding on a model change (estimate)**

| What is re-embedded | voyage-4 | voyage-4-large | with −33% batch |
|---|---|---|---|
| 20k views | $0.30 | $0.60 | $0.20 / $0.40 |
| 1M evidence items (150M tokens) | $9 | $18 | $6 / $12 |
| 1 year of raw chunks (2.6B tokens) | $158 | $315 | $105 / $211 |

**Storage (estimate)**
- 20k views at 1024 dimensions in float32 ≈ 82 MB.
- 1 year of raw chunks at about 500 tokens each ≈ 14,400 chunks/day ≈ 5.3M vectors ≈ 21.6 GB float32, 10.8 GB halfvec, 5.4 GB int8 or about 0.7 GB binary at 1024 dimensions.
- Storing raw chunks pushes the store into the 10^6–10^7 range; storing only views and evidence keeps it at 10^4–10^6.

**Throughput**: 7.2M tokens/day ÷ 320K tokens per request ≈ 23 voyage-4 requests per day as a minimum. Rate limits are not a constraint at this volume.

**What dominates**: duplicate/merge/new decisions mean one LLM call per document (or per extracted claim) that reads the document plus around 10–20 candidate views. That will cost far more than embedding. The design should spend effort on keeping that candidate set small and well filtered, not on embedding price. (Claude prices were not fetched here.)

### Gaps
- The actual document mix and lengths in the stream are not known; the mix above is an assumption. A token count over one stored day of documents (with `count_tokens`) would replace it at no cost.
- No current (2024–2026) source was found for average 10-K or news article length; the 10-K figure is from 2013.
- Chinese token ratios for Voyage were not documented.
- Whether Voyage's 200M free tokens are one-time or recurring was not stated on the pricing page.
- OpenAI's batch price for embeddings and Cohere Embed 4/5 prices were not confirmed from primary pages.
