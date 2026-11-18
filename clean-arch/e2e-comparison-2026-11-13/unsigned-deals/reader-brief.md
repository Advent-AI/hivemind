# Blind reader: choose and mark fresh articles about NVIDIA deals not yet signed (read-only)

Repository: `/Users/lchingen/hivemind`. You are independent; no system answer exists yet for these articles and none is shown to you.

**Inputs.** Candidates per story, in publication order: `clean-arch/e2e-comparison-2026-11-13/unsigned-deals/candidates.json`. Article text:
`poc/data/items-nvda-2026-07-01-10-27.sqlite`, table `items`, column `text`, by `input_id`. The research questions already open when every
article arrives (the same list for all): `unsigned-deals/snapshot-acceptance-2026-09-07.json` (clean-1 … clean-10; note clean-2, an
acquisition's completion; clean-3, a total of credit support; clean-7, a total of commitments for equity investments). The signed standard
(Chinese): `docs/prd/05-extraction-standard.html` §3 (opening reason binding obligation, "问题怎么写") and §4 ("同一题、续期，还是另一题"). Alex's
decisions on this boundary, in his words: `docs/DECISIONS-log.md`, D388 ("一笔重大的、还没签的承诺…单独开") and D389 (size: about 5% of the
company's most recent annual profit; an obligation whose amount is not stated is judged from what the article says; its known verdicts:
about $2bn, $2.5–3bn and $5bn small, $12.9bn large).

**Task.** For each story, read its articles in order and choose the **first** one whose own text states the matter (an article that only
mentions it in passing without the deal's substance does not fit); read it in full and mark it. Mark also every article you read before it.
For the chosen article, decide what a senior analyst's Step 1 should do with the library above:
- "open a signing question": a single deal NVIDIA itself would undertake (a stake, acquisition, guarantee, backstop, financing or purchase
  commitment), not yet signed, large enough on its own, with no open question already tracking that deal (even if a total of its kind is
  open: D388);
- "link to clean-N": an open question already tracks the deal, or the deal is small, or already signed under a plan tracked by its amount;
- "nothing to open": no obligation of NVIDIA's own, or nothing an analyst would track.

Return one JSON object per line, for every article you read:
{"story": "...", "input_id": "...", "chosen": true|false, "passage": "<= 50 words copied from the article, the decisive sentence",
"expected": "open a signing question" | "link to clean-N" | "nothing to open", "question_if_new": "<the yes/no question, or null>",
"size": "<the amount and how it compares with D389's line, or 'not stated: <qualitative reading>'>", "why": "<= 40 words, citing the standard or D388/D389>"}

Out of scope: judging any system; changing anything.
