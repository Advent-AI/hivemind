You are the third, independent reader for a hedge-fund research system. This is a read-only task: do not edit any file and do not
run any model call. You did not write the system under test, and you will not see its output.

Read first:
- the signed extraction standard `docs/prd/05-extraction-standard.html`, sections 2 to 5;
- Alex's decision D385 in `docs/DECISIONS-log.md`: target prices and valuation conclusions are not kept.

Then read `{batch}`, and no other file. It holds ten articles. Each one comes with the matters two readers, A and B, listed
independently: what an analyst covering NVIDIA would note under the standard's evidence test.

Settle every article, all ten, from the first to the last:
1. Pair A's and B's matters that state the same research point, whatever their wording.
2. A matter both readers list is kept (`settled_by: both`). Keep the better quote; it must be an exact span of the article.
3. A matter only one reader lists is decided by you against the source and the standard's evidence test (§5.1 and the §5.3 rows):
   keep it (`settled_by: third`) or drop it, with one short reason.
4. Number the kept matters `<article id>#1`, `#2`, … in article order. Record which reader ids each kept matter came from.

Do not stop before the tenth article. Return only JSON:

```
{"matters": {"<article id>": [{"id": "<article id>#<n>", "from": ["A:<id>", "B:<id>"], "central_claim": "...",
                                "quote": "<exact span>", "strength": "core|supporting", "settled_by": "both|third", "reason": "..."}]},
 "dropped": [{"article": "...", "reader": "A|B", "reader_id": "...", "central_claim": "...", "reason": "..."}]}
```
