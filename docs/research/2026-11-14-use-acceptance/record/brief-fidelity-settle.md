# Blind reader: is each stored figure faithful to its article? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record/fidelity-settle-packet.json` (6 entries). Open no
other file in that folder or anywhere else: keys, designs and other readers' answers exist and you must not see them.

Each entry holds one `record_row` (a financial figure a system stored from an article: `measure`, `basis` (scope and qualifications),
`period`, `value`, `kind` (actual = reported; guidance = the company's own outlook; estimate = a named party's or consensus forecast),
`original_party` (whose figure it is), `statement_date` / `statement_date_text` (when it was said)) and the `article` it came from. The
company covered is NVIDIA (its fiscal year ends in late January: fiscal 2027 is the year to January 2027).

For each entry, find the figure in the article and mark every field against what the article says:
- `right`: the field says what the article says (another wording of the same thing is right);
- `wrong`: the field says something the article does not (a different measure, another period, another party, a wrong kind, a value the
  article gives for something else);
- `missing`: the field is empty (null) though the article states it;
- `unknown_ok`: the field is empty and the article does not state it.
For the date, judge `statement_date` and `statement_date_text` together as one field. Then two more marks:
- `own`: true when the figure is NVIDIA's own (its result, its guidance, or someone's estimate of NVIDIA's figure); false when it is
  another company's figure or a market or industry number;
- `revenue_or_margin`: true when the figure is NVIDIA's revenue (total or a segment) or its gross margin, whatever the row calls it.

Write one JSON object per line: {"entry": n, "measure": "...", "basis": "...", "period": "...", "kind": "...", "value": "...",
"original_party": "...", "date": "...", "own": true, "revenue_or_margin": true, "note": "<= 25 words, required when anything is wrong or
missing>"}
