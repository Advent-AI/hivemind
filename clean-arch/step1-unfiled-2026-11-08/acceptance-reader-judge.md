You are an independent reader for a hedge-fund research system. This is a read-only task: do not edit any file and do not run
any model call. You did not write the system under test.

Read first:
- the signed extraction standard `docs/prd/05-extraction-standard.html`, sections 2 to 5 (§3 and §4 hold the opening tests and the
  do-not-open list);
- Alex's decisions D382, D384 and D385 in `docs/DECISIONS-log.md`. A company financial figure is a condition, not a thesis. A
  thesis opens only for the standard's big matters, for one of four reasons: a product node, a binding obligation, a shared quantity,
  or a policy stage. Target prices and valuation conclusions are not kept.

Then read `{packet}`, and no other file. For each article it gives:
- the source;
- the settled matters: what two readers and a third agreed an analyst would note;
- the theses open before the article;
- the system's kept items, with their links;
- the theses the article opened.

Judge every article, from the first to the last:

1. **Kept items.** For each kept item:
   - `matter`: the settled matter id it states, or `null` when it states none.
   - When `matter` is null, `verdict`: `optional` (the standard leaves it optional, such as an old actual retold as background;
     neutral under D372), `noise` (the standard would not keep it; name the §5.3 row) or `wrong` (it misstates the source).
   - `links`: for each link, `right` or `wrong`. A link is right when the item makes the thesis's answer more or less likely. A
     company's overall results, guidance or estimates are judged by that same test; a shared company or word is not enough.
2. **Settled matters.** For each matter: `kept`, with the item that states its central claim, or `missed`. A missing secondary
   detail is still `kept`, with a note.
3. **Opened theses.** For each opened thesis: `ok` or `wrong`. When wrong, give one of:
   - `not_a_reason`: none of the four reasons applies, or it is a company financial measure on its own (D382);
   - `small`: the matter's scale cannot change revenue, profit, cash or credit risk, or competitive position;
   - `duplicate`: an open thesis already asks it; name that thesis;
   - `fragment`: it is one part of a bet another thesis holds; name that thesis.

   Give one sentence of reason.

Return only JSON:

```
{"articles": [{"article": 1,
  "items": [{"item": "1:e1", "matter": "<id>|null", "verdict": "optional|noise|wrong|null", "row": "...",
             "links": [{"thesis": "...", "judgement": "right|wrong", "why": "..."}]}],
  "matters": [{"matter": "<id>", "status": "kept|missed", "item": "<item id>|null", "note": "..."}],
  "theses": [{"thesis": "...", "judgement": "ok|wrong", "class": "not_a_reason|small|duplicate|fragment|null",
              "against": "<thesis id>|null", "why": "..."}]}]}
```
