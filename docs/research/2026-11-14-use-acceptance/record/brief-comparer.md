# Blind comparer: two readers answered the same six questions; check each part against the articles (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record/compare-packet.json` (the two readers'
answers, part by part, under the labels P and Q; the labels are drawn anew for each question, so P of one question need not be P of
another) and `docs/research/2026-11-14-use-acceptance/week/packet-A1.json` (the 40 articles both answer sets rest on, numbered). Open no
other file in those folders or anywhere else. NVIDIA's fiscal year ends in late January: fiscal 2027 is the year to January 2027.

For each part, check both answers against the articles (use the cited article numbers, and look in the others if a figure is not where
cited) and mark:
- `P` and `Q`, each one of: `supported` (every figure, period and attribution it states is what an article says), `wrong` (it states a
  figure, period or attribution no article supports; say which), `incomplete` (what it states is supported but it leaves out something
  the question's part asks and the articles hold), `none` (it says the material does not hold this part, or gives no answer);
- `agree`: true when both state the same figures for the same periods from the same parties (wording aside), false otherwise; when one is
  `none`, false;
- `articles_hold`: true when at least one of the 40 articles states what this part asks, false when none does.

Write one JSON object per line: {"question": "Q1", "part": "a", "P": "...", "Q": "...", "agree": true, "articles_hold": true, "note": "<= 30
words; required unless both are supported and agree>"}
