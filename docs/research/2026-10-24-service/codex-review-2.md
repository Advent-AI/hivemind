The fixes are not fully closed: two money-query errors remain on the sealed ledger, and several new checks still accept incorrect states. For example, `evaluate('v84', '=', 26979000000)` returns `not_yet`, although that amount belongs inside the currently judged band.

No files changed. No model API was called.

**Remaining findings, ranked by caller impact**

1. **[P1] An exact shared boundary still gives the wrong answer for `v84`.**  
   [service.py:290](/Users/lchingen/hivemind/src/hivemind/service.py:290)

   Parsing `269.79亿美元` produces `26979000000.000004`, instead of exactly `26979000000`.

   Concrete input:

   ```python
   evaluate(ledger, 'v84', '=', 26979000000)
   ```

   Actual: `claim_position=4`, `judged_position=3`, `verdict='not_yet'`.  
   Correct: `claim_position=3`, `verdict='borderline'`.

   The error affects two adjacent conditions in this one ladder. At the same boundary, `verdict_for` also answers incorrectly for position 4 under all three comparators. The equality rule itself is sound; the amount conversion moves its boundary.

   **Rule needed:** convert written amounts without moving their boundaries.

2. **[P1] The parser misses the entire dollar ladder for `v70`.**  
   [service.py:303](/Users/lchingen/hivemind/src/hivemind/service.py:303)

   Each condition starts like this:

   ```text
   截至2026-12-31，筹集总额不低于5000亿美元且低于7500亿美元。
   ```

   The parser discards everything after the first Chinese comma, including the amount condition.

   Concrete input:

   ```python
   evaluate(ledger, 'v70', '>=', 500000000000)
   ```

   Actual: `evaluable=False`, with all five positions reported unreadable.  
   Correct: `claim_position=3`, `judged_position=3`, `verdict='holds'`.

   There are **43 dollar ladders**, not 42. The census test misses this one because it uses `band()` itself to decide whether a ladder contains money, then skips ladders where parsing fails completely. [test_service.py:93](/Users/lchingen/hivemind/tests/test_service.py:93)

   The same truncation can silently remove a restriction: the conditions `低于100亿美元` and `不低于100亿美元，且低于200亿美元` are accepted as covering everything, although neither covers amounts of 200 亿 or more.

   **Rule needed:** identify the operative condition before discarding explanatory text.

3. **[P2] `--lexical` does not enforce lexical or network-free searching with an existing index.**  
   [hivemind_api.py:111](/Users/lchingen/hivemind/scripts/hivemind_api.py:111), [hivemind_mcp.py:28](/Users/lchingen/hivemind/scripts/hivemind_mcp.py:28)

   The flag only skips the startup build. Neither front passes it into `search()`.

   With the supplied full index, the query:

   ```text
   Can NVIDIA's data center revenue top $300B this year?
   ```

   follows the normal semantic path and returns `mode='semantic'`. An uncached query invokes the embedding function. I confirmed that invocation with a local failure stub; no network request was made.

   The HTTP test uses a new empty index, so it cannot catch this existing-index case.

   **Rule needed:** make the selected search mode govern query handling too.

4. **[P2] An empty vector payload still qualifies as a fresh semantic vector.**  
   [search.py:115](/Users/lchingen/hivemind/src/hivemind/search.py:115)

   Using a read-only adapter, I presented `v3`’s existing row with its correct hash and model but `vector_json='[]'`.

   Actual: `mode='semantic'`, `missing_vectors=[]`; the example query’s first result changed from `v3` to `v9`. The empty vector receives a zero semantic score instead of triggering fallback.

   All **94 actual stored vectors have 1,536 components**. This is a reproduced payload-validation hole, not corruption found in the supplied index.

   **Rule needed:** a fresh vector must contain a usable vector, as well as matching text and model.

5. **[P2] The partition check explicitly accepts an uncovered boundary.**  
   [service.py:358](/Users/lchingen/hivemind/src/hivemind/service.py:358)

   Concrete synthetic ladder:

   ```text
   1: 低于100亿美元
   2: 高于100亿美元
   ```

   Actual: `ladder_bands()` returns the bands with `problem=None`.  
   Correct: refusal, because exactly 100 亿 belongs nowhere.

   The rewritten design also allows this through “at most one includes it,” while calling the result an unbroken partition. **None of the 42 accepted sealed-ledger ladders has this gap.**

   **Rule needed:** exactly one adjacent band owns each shared boundary.

6. **[P2] Startup failure reporting loses already-completed indexing work.**  
   [search.py:102](/Users/lchingen/hivemind/src/hivemind/search.py:102)

   By inspection: with 94 missing vectors, if the first batch of 64 succeeds and the second fails, the first batch has already committed. Nevertheless, `ensure_index()` returns:

   ```text
   (0, 0, 0, error)
   ```

   That wrongly reports zero embedded views and zero tokens.

   Subsequent search answers still check the actual rows, so partial construction does **not** by itself produce a false semantic label. The incorrect part is the startup work/cost report.

**The original eight findings and their tests**

| Original finding | Status | Does the test catch the old behavior? |
|---|---|---|
| **1. HTTP thread failure** | Fixed by `HTTPServer`. | **Yes.** The `/days` assertion expects `(200, …)`. With the old server, its request helper instead reaches `raise AssertionError('the server did not answer')`. [test:130](/Users/lchingen/hivemind/tests/test_search.py:130) |
| **2. Future relationships** | The reported leak is fixed. | **Yes:** `assert 'v94' not in …['dependants']` for `2026-02-25`. The `late == 28` assertion only confirms the population; it does not prove filtering. The ledger contains **zero resolution records**, so that branch remains unexercised by this test. [test:56](/Users/lchingen/hivemind/tests/test_service.py:56) |
| **3. Future evidence sources in changes** | Fixed. | **Yes:** every returned source must have `publication_day <= '2026-02-25'`. Old `e3` sources violate that assertion. [test:85](/Users/lchingen/hivemind/tests/test_service.py:85) |
| **4. Amount parsing** | **Partly fixed.** Original examples now work; findings 1, 2 and 5 above remain. | **Yes for the named examples:** `v17` must return `borderline`; `v27` must return position 3 and `borderline`. The census assertion does not establish complete coverage. [test:120](/Users/lchingen/hivemind/tests/test_service.py:120) |
| **5. Equality inside a band** | Fixed at the verdict-rule level. | **Yes:** `evaluate(v3, '=', 325e9)['verdict'] == 'borderline'`; old behavior returned `holds`. [test:117](/Users/lchingen/hivemind/tests/test_service.py:117) |
| **6. Missing/stale vectors labelled semantic** | Fixed for absent rows, wrong models and stale text hashes. Empty payloads remain a hole. | **Yes:** stale `v3` must produce `mode='lexical'` and `missing_vectors=['v3']`; all semantic scores must be zero. The empty-index assertion covers absent rows. [test:81](/Users/lchingen/hivemind/tests/test_search.py:81) |
| **7. `none` and successful exit on failure** | Code fixed. | **No regression test exists** for either behavior in the two test files. The script now excludes literal `none` and calls `sys.exit(1)` when an example fails. [script:54](/Users/lchingen/hivemind/scripts/search_eval.py:54) |
| **8. Provider error body in exceptions** | The reported message-body leak is fixed. | **Yes:** the fake-401 assertion requires both `dummy` and `sk-` to be absent, while retaining `invalid_request_error`. Old behavior fails it. [test:107](/Users/lchingen/hivemind/tests/test_search.py:107) |

**Coverage and search cost**

I read all **380 stored conditions**, including the **215 conditions across 43 dollar ladders**. An independent boundary transcription found only the `v70` refusal and `v84` conversion errors. Across the 42 accepted ladders, **7,515 verdict probes** found four mismatches, all at `v84`’s same boundary.

The freshness check reads all 94 views, even for an earlier `as_of`. With this index it performs **96 SELECTs**, loads about **2.91 MB** of vector JSON, and performs 94 rung queries. Three measured calls took **13.03, 13.44 and 13.06 ms**. These numbers cover freshness checking alone.

All **12 service tests** passed when invoked without filesystem writes. The fake-401 test passed. The four cached search examples passed their current accepted sets. I did not run tests that create indexes, copy ledgers or launch the HTTP front.