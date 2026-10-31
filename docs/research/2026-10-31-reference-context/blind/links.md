Read-only task; write your answer to stdout only.

You are a hedge-fund analyst. File: docs/research/2026-10-31-reference-context/blind/links.json. Each entry has a statement an extraction
kept from a news article (quote and one_line, with the article's title and day) and the open research question it was linked to
(question). Judge, for each entry, whether the statement makes that question's answer more or less likely:
- "right": it does (directly, or through the company's demand, supply, inputs, competition, pricing, product progress, policy or
  obligations);
- "wrong": it does not bear on that question; it belongs to another listed matter or to none;
- "new": it is material but belongs to a question not in the list (say in one phrase what question).
Do not open any other file under docs/research. Output exactly one JSON object: {"L01": {"verdict": "right|wrong|new", "note": "<short>"}, ...}
covering every entry, nothing else.
