# Council round 47d: after 47c (read-only, same thread)

Every 47c finding is answered (PAID-GATE.md §3d; paid_gate.py, paid_rehearsal.py, paid_mutants.py).
1. `merge(parts, shared_keys)`: unifies only forecasts of declared shared quantities, only across the two calls (`owner`), only when `_same_value`; within-call duplicates stay for C3/C4. Rehearsed both ways (member-key duplicate → C3 ambiguous; shared duplicate within one call → C4 two nodes), each refused as the joint arm would be.
2. The key is `{run_digest, packets_sha256, order}` only. `verdict` re-renders every packet from results.json + plan.json in the key's order (`render_packets`), takes decisions, cards and grounds from that, and requires the text to equal packets.md, the key's sha and the readings' sha; the key must map one packet to each unit. Rehearsed: swapped units → INCOMPLETE; decisions forged into the key → no change (STOP stays STOP).
3. Cards are K1.. and are grounds (an abstention reads with K1). Earlier attempts show their own answers (figures T<n>.F..); no-answer attempts show a neutral failure label. Check codes are removed from packets: a cross-member C3/C4 code exists only in joint answers and would reveal the arm.
4. `attempt_records` skips and lists an unparsable line as damaged; that attempt is unfinished; `recover` rebuilds results read-only (rehearsed with urlopen raising if called); the verdict is INCOMPLETE while any line is damaged.

Rehearsal 48 of 48 (three runs). Mutants 19 of 19, control passes. One parallel control failure was traced: the swap test sometimes swapped two draws of one unit, whose rehearsal text is identical (harmless to the verdict, which counts by unit); the test now swaps different units. Plan unchanged (6f81dae5…).

Out of scope: the frozen ruler, production code, D725's verdict lines, the $0 gate's checks.

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line.
