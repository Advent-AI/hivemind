Round 3 of the focused call (read-only). Alex set the scale line as D389: read "## D389" in `docs/DECISIONS-log.md`. The diff against
round 2 is in `council/dg-diff.txt`:
- **System text:** D389's decided sentences, and "Use only this item's information, and the company's most recent annual profit given in
  the request as fixed input".
- **Closing check:**
  - company_impact puts the stated amount beside 5% of that profit;
  - large_enough is true at about 5% or more of the profit with a stated amount, and the qualitative conclusion with no stated amount;
  - "Write no figure that neither the item nor the request gives".
- **Payload:** a `company` object (`focused/focused_probe.py`, COMPANY), giving FY2026 net income of $120.067bn. Its source is a corpus
  article, gnews:595a83074fb8af0237f822ce; the company's own 10-K is not in the corpus window.

The plan and falsifiers are those of r16 and r17. Under 150 words: is D389 carried word for word, with nothing wider or narrower? Does
anything risk Ohio, whose amount is unstated? Is the fixed input sourced acceptably for a probe? End with SEND / READY, or the blocker.
