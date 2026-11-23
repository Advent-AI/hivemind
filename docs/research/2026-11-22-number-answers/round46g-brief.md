# Council round 46g: re-review the $0 gate after 46f (read-only, same thread)

Every 46f finding is answered:
- **per-unit:** the inverse is fixed and G3inv added;
- **C1:** T9 ("$800 billion" with approx_below), refused for an incomplete expression;
- **fixtures:** R1a's prior points to the 09-19 answer's reference (authenticated by the new C10); R2 and R3 keep the stored $70B and $1.08T references; the R2 talks amount is labelled as inferred;
- **new checks:** C9 same base (G4m) and C2 bound direction (R4m), with certainty by side;
- **priors:** comparison only (C10, P3c);
- **schema:** descriptions are operation-specific with examples from other industries;
- **render:** one stored family request rendered and a conforming answer checked (`render_v13.py`, `render-r1.*`).

Gate run 3 (`gate-run3.txt`, fixtures in `gate-run3.fixtures.json`): 34 of 34. Mutants (`mutants.py`, `mutants.log`): 10 of 10 caught, control passes. Design v7, `REQUEST-AUDIT.md` updated.

Output: a verdict line, GATE PASS STANDS or GATE FAIL; only findings that let a registered item pass for the wrong reason, refuse a gold control, or leave a conflict in the request.
