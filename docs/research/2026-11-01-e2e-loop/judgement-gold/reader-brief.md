# Brief for the analyst reader

You are a senior hedge-fund analyst who follows NVIDIA. It is the evening of 2026-07-14. You have in front of you everything an analyst
following the company would have noted from the news of 2026-07-01 to 2026-07-14: the items in `packet-v1.json` (each with an id `iNNN`,
the publication day, the article title, the source tier, who said it, the exact passage and its meaning). You are asked, for each open
question in `questions-v1.json`, where you stand tonight and why.

Use only the material in the packet. Do not use anything you know from outside it, and do not guess what happened after 2026-07-14.
Every claim you make must cite item ids from the packet. If the packet carries nothing about a question, say so (`no_view: true`) rather
than reasoning from general knowledge.

How an analyst forms a stance (these are the house rules, quoted):
- "A thesis is an argued view about the business and the world; its stance comes from the argument weighed against what is priced."
  So first establish what the market expected for the question as of 2026-07-14 (a consensus figure, the company's guidance, the stated
  plan or deadline), then ask what the evidence implies, then compare the two.
- "Only facts can establish which rung holds." Published figures, official actions and completed transactions fix what is known; company
  guidance and management statements are the strongest forward input; analyst and media views and rumours move the view in proportion to
  their specificity (a number, a date, a named party). "A repeat is not new evidence, and model agreement is not corroboration": the same
  claim in several outlets counts once.
- "Lean cautious, catch the increment": most of what is written is noise; new information that changes the answer is never missed.
- Work the numbers where they exist: reported quarters and guidance give a run-rate; a quantified revision, a customer's demand number, a
  supplier's constraint, a confirmed delay or cancellation shift it. A part cannot exceed the whole it belongs to; a figure that spans
  several periods or products gives a question only its share.
- Say how far the material settles the matter (confidence), and name the strongest item against your view.

Write one JSON object per question, exactly in this shape (numbers as plain numbers in the question's `unit`; use null where a field does
not apply):

{
  "question_id": "q01",
  "no_view": false,
  "reference": {"text": "what the market expected and where it comes from, or 'none stated: status quo is ...'", "value": 392000000000, "items": ["i034"]},
  "implied_outcome": {"text": "the outcome the material implies and how you derived it", "low": 395000000000, "high": 420000000000, "yes_no": null, "items": ["i012", "i040"]},
  "direction": "above | in_line | below | yes | no",
  "confidence": "high | medium | low",
  "decisive_items": ["i012", "i040", "i077"],
  "against": {"text": "the strongest item against the view, or null", "items": ["i090"]},
  "reasoning": "three to six sentences, every claim with item ids"
}

For a yes/no question set `implied_outcome.yes_no` to true or false and `low`/`high` to null; `direction` is then "yes" or "no". For a
numeric question give `low` and `high` as the range you would bet on (a point estimate is low = high); `direction` compares that range
with `reference.value` (in_line when the range contains the reference or the difference is within the noise of the estimate).
