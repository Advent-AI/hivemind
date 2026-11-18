# Blind audit of a reworded schema change (read-only)

Repository `/Users/lchingen/hivemind`. Compare `clean-arch/step1-unfiled-2026-11-08/arms/c22-schema.json` with `c21-schema.json` and with
`c8-schema.json` (parsed JSON; c22's system text and closing check are c8's byte for byte: confirm with `cmp`). c22 rewords the
descriptions of two fields that c21 added to each item of `evidence[].figures`: `party` and `fiscal_period`. Read the request as the model
reads it: `c8-system.txt` (section 2's CONDITION bullet; every sentence on figures, parties, dates and periods), `c8-closing.txt`, and every
description in the c22 schema, the figure's `kind` among them. The earlier audit of c21's wording is
`docs/research/2026-11-14-use-acceptance/figure-fields/audit-c21-blind.md`; the reason for the rewording is in
`docs/research/2026-11-14-use-acceptance/figure-fields-2/PROBE-DESIGN.md` ("Diagnosis first" and "The candidate"), and D496, D497 in
`docs/DECISIONS-log.md`.

Report:
1. Each reworded description, sentence by sentence: clear / ambiguous / contradicts another sentence of the request or schema (quote it).
   In particular: does `party` now tell the model what to write for (a) a forecast the article states in its own voice, (b) a forecast the
   article gives as management's or the company's, (c) a reported result the article states with no spokesperson, (d) an analyst's
   estimate of the company's figure; and does the sentence "its kind is estimate, not guidance" agree with the `kind` field's own
   description? Does `fiscal_period` tell it what to write for a quarter whose fiscal year the article writes elsewhere, for a quarter in
   an article that writes only another fiscal year, for "the full year", for "next fiscal year", and for a calendar-year figure?
2. Could the rewording make the model leave a source empty that the article does state, or drop a figure, or split a statement, or
   change what it keeps, opens or links? Name the words that would do it.
3. The smallest wording changes that would remove a real ambiguity, adding no rule about what to keep, open or link.
Out of scope: whether the fields should exist; other prompts.
