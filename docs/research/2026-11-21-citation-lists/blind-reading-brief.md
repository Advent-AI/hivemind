# Blind second reading of the paid acceptance probe (read-only)

You are the blind second reader required by `docs/research/2026-11-21-citation-lists/PROBE-DESIGN.md` v5 §3. Read only:
- `PROBE-DESIGN.md` §3 (the reading rule and classes), `probe-targets.json` (the frozen targets: required claim, sources, partial,
  near misses, optional details, ambiguous flags), `stored-v7-support.json`;
- `poc/data/citation-probe-2026-11-22/packet-B.json` (51 Part B target readings: each answer with the quotes of every id it uses and of
  the target's lists) and `packet-C.json` (12 comparisons, 3 judging-v12 and 3 judging-v7 answers each, with every cited entry's text).
Do NOT open any file named `readings-*` in that folder: another reader's classes are there and you must not see them.

Part B: for each packet-B entry id, give the class and valid_support by the frozen rule: evidence targets → intended | unsupported |
misattributed | omitted (valid_support true only when the required claim is stated and an entry in `sources` is used for it); a target
frozen as ambiguous → ambiguous with valid_support false; placement targets → correct | absent | misattributed with valid_support false.
Judge misattribution by the claim each used entry is used for. Part C: for each comparison, read all six answers in full and list any
material harm of kinds (a)–(d) with status confirmed or unresolved (repeated in at least 2 of 3 v12 and at most 1 of 3 v7, counted by
claim); an empty list if none.

Answer with ONE JSON object only, no prose before or after:
{"reader": "Codex", "B": {"<entry id>": {"class": "...", "valid_support": true|false, "note": "<short reason when not intended/correct/ambiguous, or when unsure>"}, ...},
 "C": {"<comparison key>": {"read": true, "harms": [{"kind": "a|b|c|d", "status": "confirmed|unresolved", "note": "..."}], "note": "<one line>"}, ...}}
Include all 51 Part B ids and all 12 comparison keys.
