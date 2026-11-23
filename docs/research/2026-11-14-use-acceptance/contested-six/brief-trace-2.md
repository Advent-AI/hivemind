# Blind reader: why might each research answer be wrong? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/contested-six/packet-trace-2.json` and,
for the judging rules, `docs/research/2026-11-01-e2e-loop/judgement-gold/ruler-v1.md`. Open no other file. Do not edit files or
run model calls.

A research system follows one company (NVIDIA). Each item of the packet is one research question as its judge last saw it:
`request` is exactly what the judge was given (the question, its answer choices, every statement shown, with dates), `answer` is
the answer choice (`rung`) it chose with its reasons, `answered_on` its day. `candidates` are statements the system kept, dated on
or before that day, that the judge was NOT shown; each has its source `passage`. Several, or none, may matter.

For each question, read the whole request, the answer and every candidate, then give:
- `follows`: does the chosen answer choice follow from what the request shows? `yes` | `no` | `cannot_tell`.
- `form`: do the question's wording or its answer choices force or distort the answer (an undefined measure, a shape that cannot
  express the likely outcome, a choice that cannot be settled on its day)? `yes` | `no`.
- `insufficient`: is what the request shows too little to choose between neighbouring answer choices? `yes` | `no`.
- `candidates`: each candidate that bears on the question and is not already in the request in substance, with `effect` if it had
  been shown: `answer` (it would likely move the chosen answer choice), `confidence` (same choice, different strength), `neither`,
  or `cannot_tell`.
- `together`: the candidates you listed, taken together: `answer` | `confidence` | `neither` | `cannot_tell` | `none_listed`.
- `causes`: every cause of a wrong or weak answer you see, from `judge` (misreads what it was shown), `form`, `missing_fact`
  (a candidate it should have had), `insufficient_evidence`, `none`; several allowed.

Return, as your final message and nothing else, one JSON object per line, one line per question:
`{"question": "Q..", "follows": "...", "form": "...", "insufficient": "...", "candidates": [{"ref": "C..", "effect": "...", "why": "<= 25 words"}], "together": "...", "causes": ["..."], "why": "<= 40 words"}`
