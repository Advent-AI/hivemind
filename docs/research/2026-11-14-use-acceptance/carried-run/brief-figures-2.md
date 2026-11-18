# Blind reader: did each answer get the company figures that could change it? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY the packet your instructions name (`docs/research/2026-11-14-use-acceptance/
carried-run/packet-figures-2.json`) and, for the judging rules, `docs/research/2026-11-01-e2e-loop/judgement-gold/ruler-v1.md`.
Open no other file. Do not edit files or run model calls.

A research system follows one company (NVIDIA). `questions` are research questions: each `request` is exactly what the judge was
given when it last answered (the question, its answer choices and every statement shown, with dates), with the `answer` it gave.
`statements` are statements the system kept from news of the period, each with its day (most are the company's own figures).

For **each question**, list the statements that (a) bear on that question (they make some answer choice more or less likely),
(b) are **not** already in its request in substance, and (c) are dated on or before the question's last answer. For each, say
`effect` if it had been in the request: `answer` (it would likely move the chosen answer choice), `confidence` (same choice,
different strength), `neither`, or `cannot_tell`. Most statements bear on no question; a question may have none.

Return, as your final message and nothing else, one JSON object per line, one line per question:
`{"question": "Q..", "statements": [{"ref": "S..", "effect": "answer|confidence|neither|cannot_tell", "why": "<= 25 words"}], "why": "<= 30 words"}`
