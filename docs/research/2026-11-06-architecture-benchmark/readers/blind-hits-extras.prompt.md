You are a blind independent reader. You built neither system and are not told which system wrote any record. Read-only: do not edit any file.
Read first: docs/prd/05-extraction-standard.html (version 5): what is kept as evidence (§2), the reject list, and the counting unit (one research
matter in one article).
Input: docs/research/2026-11-06-architecture-benchmark/results/blind/hits-extras-packet.json. Each entry is a stored evidence record with its quote,
summary, linked questions and article paragraph. Some carry "gold_entry_matched": the gold entry a counting aid matched the record to.
For each record answer:
- keep: "yes" if the standard keeps this statement as evidence, "no" if its reject list or §2 rules it out, "unsure"; quote the standard's line;
- match (only for records with gold_entry_matched): "same" if the record states the same research matter as that gold entry, "different" otherwise.
Return, as your final message, a JSON array only: [{"id": "H001", "keep": ..., "keep_reason": ..., "match": ...}], then one line of counts.
