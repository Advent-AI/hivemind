# Council in: cold read of six answers of a new step (read-only: do not edit files, run model calls or start runs)

A new step turns a research topic ("thesis"), opened from one news article, into one judged question with an answer ladder and a
due day. Its request was sent once on six stored theses, as a probe (Alex's decision D402 in `docs/DECISIONS-log.md`). Read the six
answers cold and say what is right and wrong in each. Do not open `clean-arch/step4-2026-11-10/probe-2026-11-10/READING-claude.md`
or `clean-arch/step4-2026-11-10/DESIGN.md` before your own verdicts are written; they hold the author's views.

## What to read

- The request the model was given: `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, then the payload, then
  `clean-arch/step4-2026-11-10/ladder/candidate-closing.txt`; the answer schema `candidate-schema.json` in the same folder.
- The six requests as sent: `clean-arch/step4-2026-11-10/probe-2026-11-10/requests.json` (each `messages[1].content` holds the
  payload: the thesis and the article in full).
- The six answers: `clean-arch/step4-2026-11-10/probe-2026-11-10/answers.jsonl` (`answer` is the parsed answer).
- The decisions the request must carry, in `docs/DECISIONS-log.md`: D38 (a view: one question, a fixed ladder of five rungs or two
  for a yes/no event, a due date; a company's rungs run strongly bullish to strongly bearish; a theme's are named by outcome, with
  no bull or bear), D397 (one judged question per topic, the other parts listed as not judged), D398 (the reference the article
  gives, in its own words; a figure's middle range holds a stated reference value; the favourable end of a company's figure),
  D399 (how to build five states), D403 (an event's due day).

## Deliver, per answer, in a table

1. Does the judged question ask the one thing the thesis's `outcome` names, and is every other part of the wording listed in
   `not_judged`? Or, for a refusal: is it one of the six cases the request allows, and does it truly apply?
2. Does exactly one rung hold for every outcome? Walk the states or ranges and name any overlap or gap.
3. Is the object right (the company, or the right listed theme), and do the labels fit D38 for that kind of object?
4. The reference: are its words in the article, word for word (search the article text in the request)? Is it what the market
   expects (a consensus, guidance, a stated plan or deadline), and is its value the number those words state?
5. The due day and its basis: do they follow the request's rules?
6. Anything else that would mislead a later judge who sees only the question, the ladder and later evidence, never this article.

Then: the three most important things this probe shows about the request, most important first. Then open the author's reading
(`READING-claude.md`) and list where you differ. Under 900 words.
