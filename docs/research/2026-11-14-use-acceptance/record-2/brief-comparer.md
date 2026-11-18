# Blind comparer: six readers answered the same questions; check every answer against the articles (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-2/compare-packet.json` (for each part of
each question, six answer sets under the labels S1 to S6; the labels are drawn anew for each question, so S1 of one question is not S1
of another) and `docs/research/2026-11-14-use-acceptance/record-2/articles-unread.json` (the forty articles, numbered, with title,
publisher and text). Open no other file in those folders or anywhere else. The articles concern NVIDIA (fiscal year ending late January:
fiscal 2027 is the year to January 2027, fiscal 2028 the year after).

The questions:
- Q1 Fiscal 2028 revenue growth: (a) the company's guide; (b) what analysts expected before the guide.
- Q2 Fiscal 2027 total revenue: (a) each market estimate with its source (list every one).
- Q3 Fiscal third-quarter 2027 revenue: (a) the company's guide; (b) the market's estimate.
- Q4 Gross margin: (a) the last reported quarter; (b) what is guided or estimated for the rest of fiscal 2027; (c) the outlook for fiscal
  2028.
- Q5 The last reported quarter: (a) total revenue with its growth; (b) data-center revenue with its growth.
- Q6 Revenue or gross margin only: the same measure and period given different values by different sources (not a revision over time):
  list every pair.

Some sets were answered from the articles (they cite article numbers and quotes); others from a record of stored figures (they cite
record lines, shown with their headings). Judge every set the same way, against the articles.

For each part:
1. **What the articles hold.** Read the articles (search all forty, not only those cited) and fix what they state for this part:
   `articles_hold` true or false, and `items`: the list of what a complete answer must give (for Q2 every market estimate of fiscal 2027
   total revenue with its source; for Q6 every pair of different values for one revenue or gross-margin measure and period from
   different sources; for the other parts usually one item, more when the articles give more than one figure the part asks for).
2. **Each set**, one mark:
   - `supported`: it gives every item, each with a figure, period and attribution the articles support; and, for a set answered from a
     record, the lines it cites do hold what it says (a figure the cited lines do not hold is not supported, even if an article has it);
   - `incomplete`: what it gives is supported, but an item the articles hold is missing (name the missing item);
   - `wrong`: it states a figure, a period or an attribution (whose figure it is) that no article supports, or that its cited lines do
     not hold (say which);
   - `none`: it says the material does not hold the part, or gives no answer.
   A set that gives an extra figure the articles support is still `supported`.

Write one JSON object per line and nothing else, with no code fence: {"question": "Q1", "part": "a", "articles_hold": true, "items":
["..."], "marks": {"S1": "supported", "S2": "incomplete", "S3": "wrong", "S4": "none", "S5": "supported", "S6": "supported"}, "notes":
{"S2": "<= 25 words: what is missing>", "S3": "<= 25 words: what is wrong>"}}
