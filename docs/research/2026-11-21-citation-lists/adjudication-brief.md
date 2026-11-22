# Source-backed adjudication (read-only)

Read only `poc/data/citation-probe-2026-11-22/adjudication-case.json`. It holds a frozen reading rule, the answers and source quotes
for disputed items, and two readers' positions (unnamed). Decide each item strictly by the rule text as written, from the answers and
quotes in the file; do not open other files. Answer with ONE JSON object only:
{"Part C": {"linked-1:8776": {"decision": "confirmed (b) | unresolved | not a harm", "reasons": "..."}},
 "Part B": {"<item id>": {"class": "intended | omitted | unsupported", "valid_support": true|false, "reasons": "..."}, ...}}
