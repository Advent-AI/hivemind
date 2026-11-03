Read-only audit; do not edit any file. Repository: /Users/lchingen/hivemind-extraction-quality-2026-10-28.

THE STANDARD (the only ruler): docs/prd/05-extraction-standard.html, version 4 (Chinese), especially §5.1 (the keep rule and four kinds),
§5.2 (incomplete evidence is evidence), §5.3 (the not-kept table and its "boundary" column, plus the D238 row), §6 (what core and
supporting cover), the glossary's 七类驱动, and the decided items (D240, D243 items 4, 5, 6, 10).

THE TEXT UNDER AUDIT: docs/research/2026-10-30-noise/review-core-t2.txt. It is appended at the very end of the extraction request
(after the article), telling the model to check its evidence list once and return only what it keeps. It must carry the standard and
add no rule the standard does not hold.

TASK: go clause by clause (every clause and every example). For each: quote it; quote the standard line(s) it traces to (section);
classify as CONSISTENT, CONTRADICTS, WIDER-DROP (would drop something the standard keeps, including supporting or optional-to-keep items),
NARROWER-DROP (keeps something the standard rejects), NO-SOURCE, or EXAMPLE-DISAGREES; one sentence of reason. Then list any standard
rule about what to keep that the keep list omits and that the drop list could therefore remove (e.g. other companies' operating figures,
which §6 counts as supporting). Then list internal contradictions. End with the three findings most likely to make the model drop real
evidence. Quote exactly; if unsure say so. Out of scope: questions/opening, fields, matching.
