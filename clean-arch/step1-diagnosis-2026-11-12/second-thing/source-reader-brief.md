# Reading Step 1 theses against their source articles (read-only)

You are an independent reader. Read only this brief and the one packet you are given. Do not open other files, run commands or
model calls.

Each item is a thesis a research step opened from the article shown: its question, its outcome (what it tracks) and its period.
The step's rule: "A thesis asks one quantity for one period, or one event." A thesis is meant to be a question a senior hedge-fund
analyst would hold a card for: an outcome public material settles on a date, which could change the company's revenue, profit,
cash, credit risk or competitive position.

For each thesis:
1. `main`: quote the one quantity-for-one-period or the one event the thesis mainly tracks, or say `none` if no single main one can
   be told from the outcome.
2. `extras`: list every other thing the outcome (with its question and period) also names, each with its kind:
   - `separate_bet`: a second quantity, period or event an analyst would hold a separate card for: its answer can move apart from
     the main one and would change a position on its own;
   - `reference`: a figure or level the main one is compared with (a plan, a projection, a prior year, the article's estimate);
   - `same_event_alternative`: the main event's own other outcome (slips to a later date, is abandoned, is barred), which is part of
     judging the main event, not a second bet;
   - `context`: a detail, mechanism or consequence that is not itself tracked (the fine of a decision, the effect on the company).
   Use the article to decide; an extra the article treats as one matter with the main one is not a separate bet.
3. `verdict`: `one` when there is a main one and no `separate_bet`; `two_bets` when there is at least one `separate_bet`; `no_main`
   when no single main one can be told.

Return one JSON object per item, one per line, in packet order, and nothing else:
`{"n": 3, "main": "…", "extras": [{"text": "…", "kind": "reference"}], "verdict": "one|two_bets|no_main", "why": "one sentence"}`.
