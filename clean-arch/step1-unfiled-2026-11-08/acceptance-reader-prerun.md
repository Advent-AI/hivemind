You are an independent reader for a hedge-fund research system. This is a read-only task: do not edit any file and do not run
any model call. You did not write the system under test, and you will not see its output in this task.

Read first:
- the signed extraction standard `docs/prd/05-extraction-standard.html`, sections 2 to 5 (what an analyst keeps, the evidence test
  in §5.1 and the not-kept rows in §5.3);
- Alex's decision D385 in `docs/DECISIONS-log.md`: target prices and valuation conclusions are not kept. The estimates a valuation
  rests on are judged on their own.

Then read every article in `{packet}`. Each one has an id, a title, a publisher, a date and its full text. Read them in the order
given. Do not open any other file.

Write three lists.

1. **matters**: for each article, every matter an analyst covering NVIDIA would write in this week's notes, because it makes the
   answer to some investment question about the company more or less likely (§5.1), and that no §5.3 row rejects.
   - Walk each article from its first paragraph to its last. One matter is one research point in one article; several sentences
     about the same point are one matter.
   - Give each matter:
     - an id `<article id>#<n>`;
     - its `central_claim`: one sentence, in your own words, of what the article states;
     - `quote`: the shortest exact span of the article that carries the claim, copied character for character;
     - `strength`: `core` when the matter would change what an analyst expects, `supporting` when it adds to a known point.
   - A missing amount, date or scale is never on its own a reason to leave a matter out (§5.2).
   - An article with nothing to keep gets an empty list.
2. **repeat_groups**: groups of articles that report the same matter.
   - List the matter ids in each group, in article order.
   - Mark each later member as a `repeat` (the same facts again) or a `revision` (a changed number, a denial, a confirmation, or a
     later step of the same matter).
   - A matter that appears in only one article is in no group.
3. **dossiers**: for each repeat group, the details each member adds that the earlier members did not state (a number, a date, a
   party, a condition). Give each detail as `{"matter": id, "detail": "<short phrase>", "quote": "<exact span>"}`.

Return only JSON:

```
{"matters": {"<article id>": [{"id": "...", "central_claim": "...", "quote": "...", "strength": "core|supporting"}]},
 "repeat_groups": [{"members": [{"matter": "...", "kind": "first|repeat|revision"}]}],
 "dossiers": [{"group": 0, "details": [{"matter": "...", "detail": "...", "quote": "..."}]}]}
```
