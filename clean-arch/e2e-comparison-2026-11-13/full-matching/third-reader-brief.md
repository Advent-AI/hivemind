# Third reader: disputed identities (read-only)

You decide, for each disputed pair below, whether the opened question is the SAME question as the named reference question.

Read, in this folder: `MATCHING-v2.md` (the rule; read §1 in full), `adjudication-earlier-rulings.md` (earlier rulings under the same
rule), `third-reader-packet.json` (the disputed pairs), and each reference question's full entry in
`docs/research/2026-11-01-e2e-loop/judgement-gold/questions-v1.json`. Do not open any other file.

For each pair, one JSON line: `{"dispute": 1, "same": true|false, "reason": "<one sentence naming the rule text that decides>"}`.
Judge from the texts and the rule alone. Output only the JSON lines.
