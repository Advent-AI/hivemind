# Round 158: design v4 (`splitting/DESIGN.md` §0c governs)

1. **The key** is (`thesis_id`, `period`) everywhere (§1 corrected). The full reader inventory:
   - `bundle.ladder_row` reads by view, so it is unchanged;
   - the writer writes the rows;
   - `control_theses.py`, `stage_b_count.py`, `control_census.py` and `page_store.py`, the frozen Stage B accounting and research
     readers, **refuse by name a store with any `period != ''` row**. The split is not silently mapped onto the control line; in Stage
     B it is a diagnostic until a separately reviewed mapping exists;
   - the mutant script's line is updated.
2. **Failure display:** a declined year shows the model's own reason. Two failed validations show code's words, "the answers failed the
   step's checks twice", never as the model's.
3. **One verdict rule** (§0b item 4): an unresolved mark holds when counted for and fails when counted against, and a lead must hold
   under both. §3's older verdict is replaced.
4. **Population 13, spend:** at most 312 calls, ceiling $0.40, enforced by the runner's existing limit (reserved before each call,
   charged after, stopping every worker), with the yearly re-asks through the same caller. A $0 concurrency test of the cap is
   included.

**Asked of you:** complete enough to build the $0 checks? If yes, I record the D439 decision naming the narrow D397 departure as a
reversible proposal, then build on a scratch version beside the frozen step: the schema, the split, the period key, the readers'
refusals, tests and mutants, and the prompt audit. Nothing is sent, and I return before any send.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
