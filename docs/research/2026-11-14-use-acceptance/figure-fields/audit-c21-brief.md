# Blind audit of a candidate schema change (read-only)

Repository `/Users/lchingen/hivemind`. Compare `clean-arch/step1-unfiled-2026-11-08/arms/c21-schema.json` with `c8-schema.json` (parsed JSON;
the system text and closing check of c21 are c8's byte for byte: confirm with `cmp`). The change adds two required fields to each item of
`evidence[].figures`: `party` and `fiscal_period`. Read the whole request as the model reads it: `c8-system.txt` (section 2's CONDITION
bullet and every sentence about figures, parties, dates and periods), `c8-closing.txt`, and every description in the schema (the
statement's own `original_party`, `reporting_speaker`, `statement_date`, `evidence_period`, and the figure's `measure`, `period`, `value`,
`kind`, `basis`). The decision behind it is D495 in `docs/DECISIONS-log.md` (read it and D494), and the shape Alex approved is in
`clean-arch/step1-unfiled-2026-11-08/LOG.md` §17.

Report:
1. Each new description, sentence by sentence: clear / ambiguous / contradicts another sentence of the request or schema (quote it) /
   asks for what the item often cannot give. In particular: can `party` and the statement's `original_party` be read as the same thing
   or as conflicting; does "the company" tell the model what string to write; does `fiscal_period` tell it what to do with a company whose
   fiscal year differs from the calendar year, with "the quarter" in an article about the latest results, with a multi-year range, with
   "by 2029", and with a figure that has no period at all?
2. Could the two fields change what the model keeps, opens or links, or how it splits statements (for example by splitting a statement
   with several figures into several statements, or by dropping figures whose party it cannot name)? Name the words that would do it.
3. Do the examples inside the descriptions read the same for any industry and name no covered company, product or number?
4. The smallest wording changes that would remove a real ambiguity, without adding a rule about what to keep, open or link.
Out of scope: whether the fields should exist; other prompts.
