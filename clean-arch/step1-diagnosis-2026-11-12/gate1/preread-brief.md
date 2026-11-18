# Gate 1 pre-read: which matters in a thesis meet the opening tests (read-only)

You are an independent reader. Read only this brief and `preread-packet.json`. Do not open other files, run commands or model calls.

Each item is a thesis a research step opened from the article shown. Its outcome may name one matter or several. For each item:
1. List every **matter** the thesis (question, outcome, period) tracks or names as something that could be tracked: the main one,
   and any second quantity, period or event. Do not list a reference figure it is compared with, the main event's own other outcome
   (a slip to a later date, an abandonment, a bar) or context (a fine, a consequence): those belong to the main matter.
2. For each matter, decide whether it **meets the opening tests on its own**: a senior hedge-fund analyst would hold a separate card
   for it, because its answer could change the company's revenue, profit, cash, credit risk or competitive position; public material
   will settle it on a date; and it is not the same question as another matter listed.

Return one JSON object per item, one per line, in packet order, and nothing else:
`{"n": 1, "matters": [{"matter": "…", "main": true|false, "meets_tests": true|false, "why": "one sentence"}]}`.
