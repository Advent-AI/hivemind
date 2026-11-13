# Which end of the figure do the texts say is good for the company?

You are given eight items in `packet.json`, in this folder. Each item is a research topic about one company, NVIDIA (`topic`),
and the article the topic was opened from (`article`). Each topic tracks one figure. Open only this brief and the packet.

## The one question, for each item

From the topic's wording and the article alone: do they settle which end of the figure is good for the company's business, a
higher outcome or a lower one?

Answer with one value of `settled`:

- `higher`: the topic or the article says, or plainly implies, that a higher outcome is good for the company's business, and
  neither argues the opposite for the company;
- `lower`: likewise for a lower outcome;
- `both_argued`: the topic and the article give a reason for each end for the company (for example, a cost that also buys
  something the company needs);
- `nothing_said`: neither says anything on which end is good for the company.

Decide by what the texts say, not by what you believe is good for the company and not by what you know of it from elsewhere.
What the article says is good or bad for another company does not count for this one.

Also answer `one_year`: true when the figure the topic tracks is a figure for a whole year or an amount stated at a year-end
or an annual report; false when it is a figure for a quarter or a half-year.

## What to return

One JSON object per item, one per line, in the packet's order, as your final message: no prose before or after, no code fence.

`{"item": 1, "settled": "lower", "one_year": true, "words": ["...", "..."], "why": "one sentence"}`

`words`: the words of the topic or the article that decide it, quoted exactly, at most 30 words each; for `both_argued` quote
one passage for each end; for `nothing_said` leave the list empty.
