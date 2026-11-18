# Round 90: DESIGN-A3 v11, to your round-89 points. Go or no-go for building it.

Reading B's contract, complete: every entry the blind classer finds a named way in goes to the two third readers whatever the first
readers marked; they rule each part of the entry (as the classer split it) with the H brief's four values. A part: both `part` holds;
both `already_judged` fails; both `settlement` fails; any disagreement or any `cannot_tell` is unresolved (for in one counting, against in
the other). The entry holds only when every part holds, fails when any part fails, else unresolved. An entry with no named way keeps
Reading A's settled mark. The send fails H when any entry fails, as Reading A counts it. Tests: matching `settlement` fails; a
disagreement is unresolved both ways; an agreed first-reader `already_judged` overturned to `part`; a mixed entry whose named-way part
holds and whose other part fails, fails. Reading A's verdict printed first in every case, a diagnostic lead included.
End with `CONSENSUS: yes` (build A3, both readings, the classer's brief and their $0 checks and tests, then return for the send) or
`CONSENSUS: no, because …`.
