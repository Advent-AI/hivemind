# Blind comparer: eight readers answered the same questions; mark every answer against the key and the articles (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-3/compare-packet-settle.json` (for each part of each
question, eight answer sets under the labels S1 to S8; the labels are drawn anew for each question, so S1 of one question is not S1 of
another; each answer comes with the lines it cites and where they sit) and
`docs/research/2026-11-14-use-acceptance/record-2/articles-unread.json` (the forty articles, numbered, with title, publisher and text).
Open no other file in those folders or anywhere else. The articles concern NVIDIA (fiscal year ending late January: fiscal 2027 is
the year to January 2027, fiscal 2028 the year after). The readers answered from stored material laid out in one of two ways; judge
every set the same way, whatever its lines look like.

The questions:
- Q1 Fiscal 2028 revenue growth: (a) the company's guide; (b) what analysts expected before the guide.
- Q2 Fiscal 2027 total revenue: (a) each market estimate with its source (list every one).
- Q3 Fiscal third-quarter 2027 revenue: (a) the company's guide; (b) the market's estimate.
- Q4 Gross margin: (a) the last reported quarter; (b) what is guided or estimated for the rest of fiscal 2027; (c) the outlook for fiscal
  2028.
- Q5 The last reported quarter: (a) total revenue with its growth; (b) data-center revenue with its growth.
- Q6 Revenue or gross margin only: the same measure and period given different values by different sources (not a revision over time):
  list every pair.

The answer key (what the articles hold; check it against the articles as you go and say so in a note if you find it wrong):
- Q1a: the company guides revenue growth of about 70% for fiscal 2028.
- Q1b: not in the articles. The right answer says the material does not hold it: mark that `none`; an answer that gives a figure here is
  `wrong` unless an article supports it as analysts' expectation before the guide.
- Q2a: the articles establish ONE estimate for the fiscal year: analysts predict more than $411 billion "in the current fiscal year"
  (article 36). Article 28's "$411 billion ... this year", in a passage about 2026, is NOT established as a fiscal-2027 estimate.
  `supported`: the article-36 estimate given as analysts', with its period as its line gives it ("current fiscal year"; the answer may
  add that it reads this as fiscal 2027); the answer may also add the article-28 figure when it gives that line's period as stored
  ("2026" or "this year") and does not state it as a fiscal-2027 estimate. `incomplete`: only the article-28 figure, given with its
  period as stored. `wrong`: the article-28 figure stated as a fiscal-2027 estimate as fact, or a figure or source no cited line or
  article supports.
- Q3a: the company guides $108 billion, plus or minus 2%, for the fiscal third quarter of 2027.
- Q3b: analysts expect $109 billion for the current quarter (article 25).
- Q4a: 75% gross margin in the fiscal second quarter of 2027, reported.
- Q4b: about 74% for the fiscal third quarter and 71% to 72% for the fiscal fourth quarter, the company's guidance (both are needed).
- Q4c: 72% to 73% for fiscal 2028, the company's.
- Q5a: total revenue $96.2 billion (also written $96.22 billion or $96 billion), up 106% year over year (both are needed).
- Q5b: data-center revenue $89.0 billion (also written $89.02 billion or $89 billion), up 117% year over year (both are needed).
- Q6, three key pairs, marked pair by pair:
  - K1: fiscal third-quarter 2027 revenue: the company's $108 billion guide against analysts' $109 billion.
  - K2: fiscal third-quarter 2027 revenue growth year over year: about 89% implied by the company's guide against the 90% analysts
    expect (MarketBeat's report).
  - K3 (a qualified pair): the last reported quarter's revenue growth: 106% year over year against "rising 100% to $96 billion in
    the recent quarter" (article 3, which states no comparison period). Found when the answer sets the two figures side by side.
  Other pairs are not required. `misstatement` is true when any pair the answer gives misstates a figure, a source or a period against
  its cited lines and the articles: e.g. stating as fact that article 3's 100% is a year-over-year figure, or that a line stored as
  "Q3 2026" or "2026" is fiscal, or presenting one source as two. Saying that a period is as stored, or that a reading is the
  answer's own inference, is not a misstatement.

For every part except Q6, give each set one mark:
- `supported`: it gives every item of the key for this part, each with the figure, the period and whose figure it is as the key and
  the articles give them, and the lines it cites hold what it says (a figure its cited lines do not hold is not supported);
- `incomplete`: what it gives is supported, but an item of the key is missing (name it);
- `wrong`: it states a figure, a period or an attribution that the key and the articles do not support, or that its cited lines do
  not hold (say which);
- `none`: it says the material does not hold the part, or gives no answer.
An extra figure the articles support does not lower a mark.

For Q6, give each set `pairs` (the key pairs it gives, among "K1", "K2", "K3"; an empty list if none) and `misstatement` (true or false).

Write one JSON object per line and nothing else, with no code fence, one line per part:
{"question": "Q1", "part": "a", "marks": {"S1": "supported", "S2": "incomplete", ...}, "notes": {"S2": "<= 25 words: what is missing or wrong>"}}
and for Q6: {"question": "Q6", "part": "a", "pairs": {"S1": ["K1", "K3"], "S2": [], ...}, "misstatement": {"S1": false, ...}, "notes": {"S1": "<= 25 words when a pair is missing or misstated>"}}
