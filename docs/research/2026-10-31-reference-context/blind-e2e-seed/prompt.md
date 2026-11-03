Read-only task; do not edit any file except writing your answer to stdout.

You judge whether an extraction kept a given statement's matter. File: docs/research/2026-10-31-reference-context/blind-e2e-seed/packet.json. Each entry has a
gold statement (gold_statement, with gold_meaning) from a news article, and six draws, A1–A3 and B1–B3: in each draw, the list of
statements (quotes) an extraction kept from that article. A and B are two extraction set-ups; you are not told which is which, and the
labels are assigned at random per entry. Do not try to guess them.

For every entry and every draw, answer kept = true when at least one quote in that draw states the same matter as the gold statement
(the same fact, figure, action or claim, possibly in other words or a longer or shorter sentence), otherwise false. A different fact about
the same company does not count; a quote that contains the gold statement's matter among other things counts. If unsure, say unsure.

Output exactly one JSON object: {"E01": {"A1": true, "A2": ..., "B3": ..., "note": "<one short reason when any draw is false or unsure>"}, ...}
covering every entry. No other text.
