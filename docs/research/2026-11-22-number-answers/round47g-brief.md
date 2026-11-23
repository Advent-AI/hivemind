# Council round 47g: after 47f (read-only, same thread)

Both 47f findings are answered (PAID-GATE.md §3g):
1. `Gate.run` sends all 36 first attempts before any retry; `score` judges completeness on first attempts only (each must end publish, held or refused); a retry that fails, is interrupted or never sent stays diagnostic. Rehearsed: interrupt during a retry → 36 scored attempts, verdict complete; retry transport failure → complete; interrupt during a scored attempt → INCOMPLETE; journal order checked.
2. The record keeps the whole provider response (no 20,000 cut); `returned_text` handles null content and refusals; `packets` renders both files before writing anything. Rehearsed: null-content refusal, a 25,000-character malformed answer naming a passage at its end, a failing render that leaves nothing and then succeeds.

Rehearsal 61 of 61 (three runs). Mutants 30 of 30, control passes. Plan unchanged (6f81dae5…).

This is the seventh review of the harness. State plainly whether anything left meets the bar; if nothing does, answer READY TO SEND. Out of scope: the frozen ruler, production code, D725's verdict lines, the $0 gate's checks, and controls that bind only the operator beyond making edits detectable.

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line.
