# Round 155: the period split, design v1 (`splitting/DESIGN.md`)

It covers your four requirements:

1. **Unit and writer path:**
   - two child topics with new identities (`clean-12@2026`, `clean-12@2027`), each with one judged question, so D397 is kept;
   - the parent gets a `split` row;
   - the writer's existing list mapping sends every statement linked to the parent to both children. A statement about one year
     reaching the other year's judge is stated as a property to read;
   - per-view closing and updates.
2. **Boundary:**
   - the model names a typed case `one_quantity_two_periods` with its two years;
   - code checks two distinct allowed years, each through the existing year checks, and re-asks once per year with a one-line
     restriction;
   - a base year that has ended is refused by the existing check, so the result is the same as answering the open year;
   - non-year topics (D436, Intel, Firmus) fail the shape check and are refused as today;
   - several products: the children may refuse, which is no worse than today;
   - no recursion.
3. **Test:**
   - $0 checks first: byte-for-byte rebuild, a request diff, synthetic answers, the writer and page on a split store, tests, mutants,
     the prompt audit;
   - then a probe, reviewed apart, of about $0.10: the 2 two-year topics, 6 one-year-with-base controls, 2 second-side, 2 guards and the
     memory topic, 3 frozen and 3 new sends each;
   - **a product decision rule written now:** the case used on both two-year topics and valid child ladders; no case use and no outcome
     change on controls beyond the same-day control's own variation; blind readers find no base-year question and no lost
     qualification;
   - limits: development cases only, and adoption needs a regression read of the 44.
4. **Stop:** misuse on controls, a base-year child, a lost qualification, broken guards, or a writer or page change for unsplit topics.

**Asked of you:** is the design complete enough for its $0 checks to be built (code and tests on a scratch version beside the frozen
step, nothing sent)? Or what is still missing? Is the schema change (a typed case over the existing prose decline cases) a hidden rule
change?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
