# Gate 2 claims reading (read-only)

You are an independent reader. Read only this brief and `packet-claims.json`. Do not open other files or run commands or model calls.

Each entry is one answer of a research step to one article. It lists the **claims** the answer must keep, **stored reference items**
(how an earlier answer kept them), the **link rule**, the **open theses** the answer could link to, the answer's **new theses**, and its
**kept evidence** items with the thesis ids each links to.

For each claim, decide whether the answer keeps it: a kept evidence item states the same figure or event for the same measure as the
claim (the item may carry more, and the facts may sit in one item). A detail of the claim (a speaker, a count of companies, a
percentage) is required only where the stored reference items state it. Then decide whether it is linked as the link rule says.
Judge by meaning, not by matching words. If `answer_usable` is false, every claim is not kept.

Return one JSON object per entry, one per line, in packet order, and nothing else:
`{"n": 1, "claims": [{"claim_id": "C26", "kept": true|false, "linked_as_required": true|false, "item": "<evidence id or null>", "why": "one sentence"}]}`
