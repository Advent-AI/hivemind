Challenge round (read-only). A second independent reviewer, a Claude reader, also recommends closing Step 1 on c8 and measuring end to
end on the frozen judgement ruler. I verified its key facts:
- `judgement-gold/score_judgement.py` reads `<run>/views.sqlite` and refuses a run whose v1–v22 are not the seed questions (lines
  36–44).
- The clean dev runs started empty (`poc/data/clean-step1-c8-dev-d1-2026-11-09/initial.json` is `[]`).
- Production v108's scores (`judgement-gold/score-r9-frozen-v108-d{1,2,3}.txt`): it reports 15, 15 and 16 agreements. q10 (operating
  margin) and q12 (capex) are never judged, q16 is wrong, q17 swings, and q23 is absent.
- D370 (Alex): "He also previously directed removal of the 22 artificial preset questions … Historical seeds, gold, results and
  records remain historical, not a new active starting library."

**Its path:**
1. Start a measurement library with the 22 seeds. It flags this as against D370's spirit and needing Alex's word.
2. Run c8 Steps 1–3 over 07-01 to 07-14.
3. Write an adapter from the clean library to the production view store (`seeding.py:seed_views`, `views/store.py`).
4. Judge daily with the frozen `views/judging.py` as a measuring harness, not as the clean Step 4 design.
5. Score unchanged.

It proposes this rule: "no arm on Steps 1–3 opens unless it names a judgement-ruler question that a trace shows it would flip".

**My concern.** c8's §3 does not open a thesis on "a financial measure's level, growth, margin or guidance … on its own", while most
ruler questions (q01–q12) are such measures. With the seeds, the 22 questions exist as a harness. Without them, the clean system cannot
open most ruler questions by design, so no score is comparable.

Under 300 words:
1. Is seeding the 22 questions as a measuring harness the right first test, or does it measure something other than the clean product?
2. Is the alternative — score only the questions the clean system opens itself, through a reviewed mapping — better or premature?
3. What exactly should Alex decide?
4. Do you adopt the proposed rule?

End with a one-line recommendation.
