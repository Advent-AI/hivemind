# Blind audit of a candidate request change against its signed standard (read-only)

Repository `/Users/lchingen/hivemind`. Compare `clean-arch/step1-unfiled-2026-11-08/arms/c19-schema.json` with `c8-schema.json` (run `diff`; this is version 2, written after a first blind audit, `audit-c19-blind.md`: read it and check whether each
material point is resolved and whether anything new is wrong; the
system text and closing check of c19 are identical to c8's: check with `diff`). The change adds two required fields to each proposed new thesis,
`settles_on` and `outcomes`. Read the whole request as the model reads it (`c19-system.txt`, then the closing check `c19-closing.txt`, then the
schema), and the signed standard `docs/prd/05-extraction-standard.html` §3 (the table of reasons with their outcomes, "问题怎么写") and §4 (the
opening tests), and D417 in `docs/DECISIONS-log.md`.

Report, sentence by sentence of the two new descriptions: consistent / contradicts / keeps wider / keeps narrower / no source, quoting the
standard's line. Then: (1) does any new sentence contradict a sentence of the system text or closing check (for example on when to open, on
the date rule per reason, on evidence for statements with no thesis, on "Open only matters an analyst would bet on separately")? (2) Do the
descriptions read the same for any industry and name no covered company, product or number? (3) Could the new fields make the model stop
proposing theses the standard keeps (for example a quantity for next calendar year compared with this year, an unsigned deal's yes/no, a
product's shipment by a date), or make it rewrite a thesis into a narrower one that loses what an analyst tracks? Name the words that would do
it. Out of scope: other prompts; changing the standard.
