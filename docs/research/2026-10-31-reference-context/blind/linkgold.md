Read-only task; write your answer to stdout only.

You are a hedge-fund analyst following NVIDIA. File: docs/research/2026-10-31-reference-context/blind/linkgold.json. Each entry is a
statement from a news article (statement, meaning, article title and day) beside the research questions that were open that day
(open_questions, each "id: text"). For each entry, name the id of the open question whose answer this statement makes more or less likely
(directly, or through the company's demand, supply, inputs, competition, pricing, product progress, policy or obligations). If it moves
several, name the one it bears on most and list the others after a comma. If it moves none of the listed questions (it belongs to a
matter no listed question asks), answer "none". Do not open any other file under docs/research.
Output exactly one JSON object: {"H001": {"question": "v9" or "v9, v2" or "none", "note": "<short>"}, ...} covering every entry, nothing else.
