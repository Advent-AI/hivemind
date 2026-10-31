Read-only task; write your answer to stdout only.

File: docs/research/2026-10-31-reference-context/blind/candidates.json. Each entry is a candidate research question an extraction proposed
from a news article (candidate_question, looks_at, article title and day) beside the questions already open that day (open_questions,
each "id: text"). Judge, for each entry, whether the candidate is the same question as one already open: the same outcome would settle
both (another wording, deadline, milestone, fiscal/calendar form, or a single deal under a plan already asked by amount counts as the
same); answer the id of that open question, or "none" when it is a different bet an analyst would hold separately. You are not told
which set-up proposed each candidate; do not guess. Do not open any other file under docs/research.
Output exactly one JSON object: {"C001": {"same_as": "v3|none", "note": "<short>"}, ...} covering every entry, nothing else.
