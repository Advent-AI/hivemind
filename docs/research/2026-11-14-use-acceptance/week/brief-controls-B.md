# Independent reader: confirm supported controls for reading B (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/week/supported-candidates.json` (8 candidates; each
holds `request`, exactly what a judging model was sent that day: the question, its ladder of outcomes and every piece of evidence shown; and
`answer`, its rung, reasons and cited ids) and, for the judging rules, `docs/research/2026-11-01-e2e-loop/judgement-gold/ruler-v1.md`. Open no
other file in that folder or elsewhere.

For each candidate decide whether the answer's rung is SUPPORTED by what the request shows (it follows from the shown evidence by the
ladder's own conditions, does not contradict its own reasons, and adds no fact the request does not hold), NOT SUPPORTED, or UNSURE. Judge
only against what was shown that day; ignore later news. Be strict: mark SUPPORTED only when you are confident.

Write one JSON object per line: {"candidate": n, "verdict": "SUPPORTED|NOT SUPPORTED|UNSURE", "why": "<= 40 words"}
