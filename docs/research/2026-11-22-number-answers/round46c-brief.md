# Council round 46c: review design v3 (read-only, same thread)

Rounds 46 and 46b found one weakness five times: the checks trusted what the answer declares about itself. v3 adopts one
structural rule (see its header): code derives every relation it checks from the calculation graph and the passage text. Changes
are marked [46b.n] in `DESIGN.md`.

Check whether the rule closes the class. Do not answer finding by finding: name only a remaining serious defect that would let a
registered gate item pass for the wrong reason, or that would refuse a gold control. If one mechanism still draws findings, say so
and propose the one rule that removes it.

Output: a verdict line, READY FOR THE $0 GATE or NOT READY; serious findings, if any, with the fix you would accept; wording notes
in one list at the end.
