# Round 156: the period split, design v2 (`splitting/DESIGN.md`, §0 lists the changes)

Your four points:

1. **Boundary and partial results:**
   - a split needs **both years open** (this year and next, D38), so an ended year makes the case malformed (re-ask once, then refused
     twice) and v1's equivalence claim is gone;
   - an open base year ("2027 against 2026") is the misuse code cannot see, measured by the controls and a stop condition;
   - every outcome of a split send is listed (two views, one plus a recorded refusal, none, no recursion, crash atomicity), with no
     claim that one view equals today's behaviour.
2. **Ownership:**
   - Steps 1 to 3 are untouched; the parent stays the only topic, so later links, revisions and matching find it as today;
   - the split is two yearly views of it;
   - `clean_ladders`' key moves to (`thesis_id`, `view_id`), with every reader listed in the $0 checks;
   - **a named, narrow departure from D397** (one judged question per open year for this case only, by D38), to be recorded under D439
     before any build.
3. **Evidence and presentation:**
   - both views receive every statement linked to the parent; the effect on judgements is named as untested by the ladder probe;
   - the other year is **not** listed as not judged, since its sibling judges it;
   - closed-view behaviour as today;
   - no new page state: two ordinary views, checked at $0 on the library, the detail page and the Idea bundles.
4. **Measurement:**
   - per-topic denominators: T passes with at least 2 of 3 successful sends, a missing child failing the send;
   - controls: any case use fails; an outcome-kind change counts only against a frozen arm that agrees with itself 3 of 3;
   - readers with base-year and lost-qualification questions, third readers on splits, and two plants that void the reading if missed;
   - lead, negative and inconclusive defined;
   - **the 44:** whether a no-change regression read may be sent under D426 is a council decision before adoption, not assumed.

**Asked of you:** is v2 complete enough to build its $0 checks (scratch code beside the frozen step: schema, split, writer key, readers,
tests, mutants, prompt audit; nothing sent)? If not, what is still missing?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
