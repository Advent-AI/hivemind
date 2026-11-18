# Blind audit of a candidate prompt change against its signed standard (read-only)

Repository `/Users/lchingen/hivemind`. Compare `clean-arch/step1-unfiled-2026-11-08/arms/c17-system.txt` and `c17-closing.txt` with the
current `c8-system.txt` and `c8-closing.txt` (run `diff`; this is version 2, written after a first audit found that "a span that is not one calendar year" could exclude a
2027-against-2026 comparison). The change rewrites one sentence of section 3 (shared_quantity's period). Read the whole changed request as the model reads it (system text, then the closing
check), and the signed standard `docs/prd/05-extraction-standard.html` §3 and §4 ("同一题、续期，还是另一题" in full).

Report, sentence by sentence of the change: consistent / contradicts / keeps wider / keeps narrower / no source, quoting the standard's
line. Then: (1) does the change contradict any other sentence of the request (for example "Another population or wording of the same
aggregate is evidence for it", "another estimate, source or wording of what an open thesis tracks", "If the two cannot move apart, link
the evidence", "Do not exclude evidence solely because it concerns a related period")? (2) Do the examples read the same for any industry,
name no covered company, product or number, and agree with the standard and the schema? (3) Could the new sentence make the model drop or reshape a comparison of next year against this year (for example a price in 2027 against
2026), drop a calendar-year figure it should open, or change how it treats statements it keeps as evidence? Name the words that would do it. Out of scope: other prompts; changing the standard.
