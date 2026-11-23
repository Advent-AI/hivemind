# Blind reader, reading B: is each judgement supported by what the judge was shown? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/packet-B.json` (25 items) and, for the judging rules,
`docs/research/2026-11-01-e2e-loop/judgement-gold/ruler-v1.md`. Open no other file in that folder or elsewhere: keys and other readers' answers
exist and you must not see them.

Each item is one judgement: `request` is exactly what the judge was sent that day (the question, its ladder of outcomes, and every piece of
evidence it was shown, with passages, speaker and date; pieces "not shown" were not seen); `answer` is its rung, reasons and cited ids. Judge
only against what the request shows; do not use later news or your own knowledge of outcomes.

For each item:
- **verdict**: SUPPORTED (the rung follows from what was shown, by the ladder's own conditions, including where it says the estimate sits),
  UNSUPPORTED (the rung contradicts the answer's own reasons, rests on a fact or step the request does not hold, or ignores shown evidence that
  places it elsewhere), or INSUFFICIENT (what was shown cannot place it, and the answer says so or should have);
- **cited items**: for each id the answer cites, whether that piece's summary matches its own passage, speaker and date as shown (list the ids
  that do not, with why);
- a short reason.

Write one JSON object per line: {"item": n, "verdict": "SUPPORTED|UNSUPPORTED|INSUFFICIENT", "bad_citations": [{"id": "...", "why": "<= 20
words"}], "why": "<= 40 words"}
