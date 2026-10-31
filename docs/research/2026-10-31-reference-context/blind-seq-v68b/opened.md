Read-only task; write your answer to stdout only.

You are a senior hedge-fund analyst. File: docs/research/2026-10-31-reference-context/blind-seq-v68b/opened.json. Each entry is a research
question an extraction run opened from a news article (question, looks_at, article title and day), with the article's gold labels
(gold_must_open: questions that must open from this article; gold_may_open: acceptable to open; gold_must_not: should not open), and
the questions the same run had already opened on earlier days (earlier_questions_in_this_run). For each entry answer:
- "duplicate" when an earlier question in this run is the same bet (the same outcome settles both: another wording, deadline, milestone,
  fiscal/calendar form, or one deal under a plan already asked by amount); give its id;
- else "must_open" / "may_open" when it matches one of the article's gold lists in meaning; "must_not" when it matches gold_must_not or
  is trivia an analyst would not bet on; "unlisted" when the gold says nothing about it (say in a phrase whether an analyst would hold it).
You are not told which set-up opened it; do not guess. Do not open any other file under docs/research.
Output exactly one JSON object: {"Q001": {"class": "duplicate|must_open|may_open|must_not|unlisted", "of": "q3 or empty", "note": "<short>"}, ...}
covering every entry, nothing else.
