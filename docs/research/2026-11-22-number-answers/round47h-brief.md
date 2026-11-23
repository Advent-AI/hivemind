# Council round 47h: after 47g (read-only, same thread)

The 47g finding is answered (PAID-GATE.md §3h): scored first attempts are journalled in answers.jsonl and diagnostic retries in retries.jsonl (`Gate.record`); `attempt_records` reads both, splitting on '\n' only (the writer's delimiter), and labels each damaged line with its journal; `score` counts only answers.jsonl damage toward INCOMPLETE; `run_digest` covers both journals. Rehearsed: a torn retry record → reported, retry interrupted, verdict complete; the torn scored record control → INCOMPLETE; an answer holding U+2028, U+0085 and U+2029 stays one record; first-before-retry order checked on the provider's own call sequence.

Rehearsal 63 of 63 (three runs). Mutants 33 of 33, control passes. Plan unchanged (6f81dae5…).

This is the eighth review of the harness. State plainly whether anything left meets the bar; if nothing does, answer READY TO SEND. Out of scope: the frozen ruler, production code, D725's verdict lines, the $0 gate's checks, and controls that bind only the operator beyond making edits detectable.

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line.
