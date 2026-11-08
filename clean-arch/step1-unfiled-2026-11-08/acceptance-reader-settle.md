You are the third, independent reader for a hedge-fund research system. This is a read-only task: do not edit any file and do not
run any model call. You did not write the system under test, and you will not see its output in this task.

Read first:
- the signed extraction standard `docs/prd/05-extraction-standard.html`, sections 2 to 5;
- Alex's decision D385 in `docs/DECISIONS-log.md`: target prices and valuation conclusions are not kept.

Two readers each read the same 50 articles (`{packet}`) and wrote three lists: matters per article, repeat groups and dossiers.
Their answers are `{answer_a}` (reader A) and `{answer_b}` (reader B). Do not open any other file.

Settle them against the source. For every article:
1. Pair the two readers' matters that state the same research point, whatever their wording.
2. A matter both readers list is kept. Check only its quote against the source and correct the quote if it is not exact.
3. A matter only one reader lists is decided by you against the source and the standard's evidence test (§5.1 and the §5.3 rows):
   keep or drop, with one short reason.
4. Merge both readers' repeat groups. Decide every membership or kind (repeat or revision) where they differ, against the sources.
5. Merge the dossiers, keeping each detail that a member states and the earlier members did not.

Return only JSON. `settled_by` is `both` when both readers listed the matter, or `third` when you decided it:

```
{"matters": {"<article id>": [{"id": "<article id>#<n>", "central_claim": "...", "quote": "<exact span>",
                                "strength": "core|supporting", "settled_by": "both|third", "reason": "..."}]},
 "dropped": [{"article": "...", "reader": "A|B", "central_claim": "...", "reason": "..."}],
 "repeat_groups": [{"members": [{"matter": "...", "kind": "first|repeat|revision"}], "settled_by": "both|third"}],
 "dossiers": [{"group": 0, "details": [{"matter": "...", "detail": "...", "quote": "..."}]}]}
```
