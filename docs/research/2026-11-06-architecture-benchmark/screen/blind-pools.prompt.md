You are a blind independent reader. You built neither system and are not told which system or version wrote any entry. Read-only: do not edit
any file.
Read first: docs/prd/05-extraction-standard.html (version 5): what is kept as evidence (§5.1), the not-kept list (§5.3) with its boundaries, and
filing under the narrowest open question (D207).
Input: docs/research/2026-11-06-architecture-benchmark/screen/blind-pools-packet.json. Each entry is a statement written from an article (quote,
summary, article title and paragraph). An entry of kind "addition" is a statement the gold of its article does not list. An entry of kind "link"
also names one open question the statement was filed under.
For each entry answer:
- addition: keep = "yes" if the standard keeps this statement as evidence, "no" if its not-kept list or §5.1 rules it out, "unsure"; quote the line;
- link: link = "right" if the statement makes that question's answer more or less likely, "wrong" otherwise; say why in one sentence.
Return, as your final message, a JSON array only: [{"id": "S001", "keep": ..., "link": ..., "reason": ...}] (keep only for additions, link only for
links), then one line of counts.
