# Blind reader: choose and mark the fresh articles of a probe (read-only)

Repository: `/Users/lchingen/hivemind`. You are independent; no system answer exists yet for these articles and none is shown to you.

**Inputs.** The candidates, in a fixed order per category: `clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/candidates-v2.json`. The
article text: `poc/data/items-nvda-2026-07-01-10-27.sqlite`, table `items`, column `text`, by `input_id`. The research questions already
open when each article arrives (the same list for every article): `identity-probe/snapshot-c3-2026-07-14.json` (ids clean-1 … clean-15).
The signed standard (Chinese): `docs/prd/05-extraction-standard.html`, §3 (opening reasons A–E, "问题怎么写") and §4 (the opening tests and
"同一题、续期，还是另一题").

**Task.** For category T1 only (ignore the other categories), go down its `order` list and read each article in full, and mark **every** article in the list (up to twenty a
category; code applies the selection rule afterwards). An article fits only if it contains the category's situation in its own text:
- **T1:** it reports a shared quantity (a figure outside any one company that several depend on, e.g. several companies' combined spending
  or a market price) for a year other than one an open question already tracks, while an open question tracks the same quantity for
  another year. Expected: should a separate question for that other year be opened, by §3 and §4 and the opening tests (yes / no, and why)?
- **T2:** it reports a single deal NVIDIA is negotiating or considering and has not signed (a guarantee, backstop, financing or sized stake),
  beside the open programme-amount question clean-1. Expected: should a yes/no question on whether that deal is signed by a check date be
  opened (§4 "还没签的单笔交易…照旧可以开，不并进计划的金额题", subject to the size and opening tests)?
- **T3:** it compares one price or quantity between two years (next year against this year). Expected: should a new question about the
  change to the later year be opened (a shared price or quantity that passes the opening tests and no open question tracks), is it the same
  as an open question, or is there nothing to open? It must not become two questions only because two years appear.
- **T4:** it carries a statement that an open question already tracks (another estimate, source or report of the same thing, or a later
  date for an event whose earlier-deadline question is open). Expected: which open question it belongs to; no new question.

Mark also, for a fitting article, the **story**: a short key naming the underlying matter (e.g. "openai-ohio-financing",
"hyperscaler-capex-2027", "dram-contract-price-2027"), the same key for every article about the same matter, so that one matter is counted
once. Expected answers may be "nothing to open" when the figure lacks independent significance or cannot be settled: say so where it applies.

Return one JSON object per line, for every article you read (fits or not):
{"category": "T1"|"T2"|"T3"|"T4", "input_id": "...", "fits": true|false, "story": "<key or null>", "passage": "<= 50 words copied from the article, the decisive
sentence", "expected": "open a new question" | "link to clean-N" | "one question about the later year" | "nothing to open",
"question_if_new": "<the question an analyst would write, or null>", "why": "<= 40 words, citing the standard's line"}

Out of scope: judging any system; changing anything.
