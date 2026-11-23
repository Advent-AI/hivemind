# Council round 41, third challenge: your 41c findings taken (read-only)

1. `entries()` now cuts an entry from its own start line (`- eN [` or `- vN (`) to the next entry start or the next known block header,
   whatever its lines look like. The rehearsal checks every packet quote against the stores themselves (the stored quote's first 400
   characters as the request printed it): 300 checked, all whole; old-2:6955's e4070 (a multiline quote) kept whole.
2. `ambiguous` is allowed only for a target frozen as ambiguous, always with `valid_support: false`; 8807 marked ambiguous is refused
   (rehearsed).

`rehearsal.log`: 60 checks, REHEARSAL PASS. Answer READY TO SEND or NOT READY with blocking items only.
