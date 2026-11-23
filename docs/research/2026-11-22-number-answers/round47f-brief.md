# Council round 47f: after 47e (read-only, same thread)

Every 47e finding is answered (PAID-GATE.md §3f):
1. The first attempt is scored on both arms (`first_attempt`; `summarise` reconciles the separate arm's first answers; `packet_units` scores first attempts). D725 registered the arms "under the same format and checks" and says nothing about retries; its lines stay as written, applied to first attempts. Retries are sent and read in attempts.md only. Rehearsed: a joint pair repaired by its retry is still scored on its refused first attempt (both arms 6).
2. `merge` unifies only when units are equal too (`units[a] == units[b]`). Rehearsed: 110 USD bn vs 110 USD → C4 refusal.
3. A format failure's returned text (`raw` kept in the record; `returned_text`) and the passages it names go to attempts.md under a blind label, first or final attempt alike; the scoring packet keeps the neutral label.
4. `verdict` seals the readings into the run once (readings.json, exclusive), scores, and writes verdict.json once (readings sha, key commitment, packets sha, run digest, result); a second verdict is refused; `replay` must reproduce it. Rehearsed all three.

Rehearsal 55 of 55 (three runs). Mutants 25 of 25, control passes. Plan unchanged (6f81dae5…).

This is the sixth review of the harness. Please state plainly whether anything left meets the bar below; if nothing does, answer READY TO SEND. Out of scope: the frozen ruler, production code, D725's verdict lines, the $0 gate's checks, and process controls that bind only the operator (the operator can always edit files they own; what matters is that any such edit is detectable by the records).

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line.
