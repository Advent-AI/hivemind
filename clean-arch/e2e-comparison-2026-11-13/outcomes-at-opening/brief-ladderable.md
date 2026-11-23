# Blind reader: can each research question be given fixed outcomes? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `clean-arch/e2e-comparison-2026-11-13/outcomes-at-opening/packet-ladderable.json` (research
questions proposed by an analyst system, each with its question, tracked outcome and period) and the signed standard
`docs/prd/05-extraction-standard.html` §3 (the table of reasons with their outcomes, "问题怎么写") and §4 ("能核对"). Open no other file in that folder.

For each item decide **ladderable**: yes when it asks about one quantity, or its change against a stated earlier period, for one fiscal or
calendar year or a stated date, or about one event checked by a date, so that fixed outcomes (five ranges, or an event's five or two states)
could be written now and exactly one would hold on the check date; no when it asks about several quantities or outcomes none of which leads, a
rolling window with no publication day, a period the question leaves open, or nothing a date and public material can settle. Name the matter.

Return one JSON object per line: {"item": n, "ladderable": "yes|no", "why": "<= 25 words", "matter": "<short key, e.g. dram-price,
h100-rental-price, intel-stake, china-domestic-share, federal-ai-spending, hyperscaler-capex>"}
