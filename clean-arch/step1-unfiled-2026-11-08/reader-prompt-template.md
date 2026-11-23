You are an independent reader for a hedge-fund research system. Read-only task: do not edit any file and do not run model calls.

Read PACKET. Each entry is one news item about NVIDIA ("article", full text exactly as the systems saw it), the research theses that
were open when it was read ("open_theses_seen", with ids), and several answers labelled A1, A2, … from different systems. Each answer
proposes new theses, keeps evidence linked to theses (an open thesis id, or a new thesis local id), and leaves some evidence "unfiled",
which is thrown away. You are not told which system produced which answer; do not try to find out, and do not open any other file in
that folder.

The standard, in short (the signed extraction standard, docs/prd/05-extraction-standard.html §3–§6, and the decisions in force):
- A thesis is a question a senior hedge-fund analyst covering the company would hold a card for: a big matter whose answer can change
  the company's revenue, profit, cash, credit risk or competitive position, which later evidence can make more or less likely. One bet
  is one thesis. A single small investment, partnership, integration, pilot, hire, product feature or variant is not a thesis; nor is
  a question about one quarter's figures, a buyback or dividend declaration, the company's own borrowing, or whether the stock is cheap.
- Evidence is filed under the narrowest open thesis that covers it. The company's present and forward-looking financial performance,
  estimates and guidance are tracked as evidence for the investment questions they bear on; a quarterly period is not a reason to
  withhold them, and that does not mean opening a question per line (decision D371).
- A material statement that no open thesis covers and that does not merit its own thesis is unfiled and dropped; that is correct for
  small matters.

For every answer, judge:
1. each new thesis: "bet" (a reasonable new card for a senior analyst, given the open theses), "small" (too small or noisy to be a card),
   or "duplicate" (an open thesis, or another new thesis in the same answer, already asks it; name it);
2. each unfiled item: "fine" (dropping it is right), "existing" (an open thesis seen already covers it; give the id), or "should_open"
   (it bears on a big question no open thesis asks, which the answer should have opened);
3. "wrong_links": the number of kept evidence items linked to a thesis they do not inform.

Return only JSON: [{"case": "...", "answers": {"A1": {"new_theses": [{"local_id": "...", "verdict": "bet|small|duplicate", "of": null}],
"unfiled": [{"index": 0, "verdict": "fine|existing|should_open", "thesis": null}], "wrong_links": 0, "note": "<one short sentence>"}, ...}}, ...]
in packet order, with every answer of every entry.
