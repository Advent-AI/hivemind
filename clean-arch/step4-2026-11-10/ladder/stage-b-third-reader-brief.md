# Stage B: the third reader's rulings on a verdict

Two readers each read a set of judgements, independently, with the form in
`/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-b-reader-brief.md`. Read that form first: it says what a
judgement is, quotes the judge's own rules, and gives the tests for the verdict in a fixed order. You rule where the two
readers' verdicts differ. Do not edit files, run model calls or start runs.

## What you are given

A packet of judgements. Each is as the form describes it (`request_as_sent`, `answer`, `not_shown`), with one more field,
`to_rule`: `{"judgement": 17, "reader_a": {"verdict": "...", "rung_the_evidence_points_to": ..., "why": "..."},
"reader_b": {...}}`. "a" and "b" are not the same reader from one judgement to the next.

## How to rule

- Read the request as sent and the answer yourself before ruling. Apply the form's tests for the verdict in their order
  and stop at the first that decides. The verdict is about the rung only, from the request as sent alone; `not_shown` does
  not enter it.
- The readers' verdicts and reasons are leads: a reason may be right, wrong, or about something that does not change the
  rung.
- Do not rule UNSUPPORTED because you would have forecast differently where the rules and the evidence allow the answer's
  rung, and do not rule SUPPORTED because the fault is small: the form's tests decide.

## What to return

One JSON object per judgement, one per line, in packet order, as your final message: no prose before or after, no code
fence: `{"judgement": 17, "verdict": "SUPPORTED" | "UNSUPPORTED" | "INSUFFICIENT", "rung_the_evidence_points_to": a rung
number or null, "why": "one sentence naming the evidence id or the figure that decides it"}`.
