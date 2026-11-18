# Round 161: your round-160 finding, fixed (D619; `splitting/BUILD-RESULT.md`, "Round 160")

You were right on both points: the bound refused ordinary topics, and `isdigit()` let a leading zero through.

1. **Yearly ids are `v0<number><four-digit year>`** (`v042026`). An ordinary id is `v<topic number>`.
   - The writer now refuses any topic id that is not `clean-` plus a number without a leading zero, before writing
     (`ladder_adapter.CANONICAL_TOPIC`). That is Step 1's form: an integer counter at `clean-arch/step1/runner.py:350-352`.
   - All 3,457 stored topic ids (163 case and outcome files, 18 distinct, the largest 18) have it, so the refusal meets no stored input.
   - The size bound is removed. No ordinary id begins with 0, so no yearly id can equal one. Yearly ids decode one way only.
   - The frozen judge's `v\d+` and the page's id pattern accept the leading 0. The only numeric use of a view id
     (`baseline.py:190`) sorts the old system's seeded views.
   - **Through the real writer:**
     - an ordinary `clean-42026` beside the split `clean-4` gives `v42026`, `v042026` and `v042027`;
     - `clean-04`, `clean-0`, `clean-4a` and `other-4` are refused with nothing written;
     - a split whose stored years are malformed (`2026,2026`; `2026,FY2027`; `26,27`; one year) is refused with nothing written.
2. **A reader dimension I had missed: code that maps a view to its topic by id** (`f'clean-{view[1:]}'`), without reading
   `clean_ladders`. I searched all code for the pattern:
   - `carried-run/build_sources.py`, `side-by-side/build_side_by_side.py` and `pilot-deck-1/build_deck.py` would silently map a yearly
     view to no topic. Each now calls the shared refusal right after opening a store. Each is tested at its entry point on a split
     store.
   - `opening-review/build_opening_cases.py` opens no store and reads that study's fixed files. A yearly id would stop it with
     StopIteration, not a wrong answer.
   - The other `v{k}` uses are the old system's 22 seeded views.
3. **Historical stores:**
   - The shared refusal passes all six stores the seven refusing readers read in their recorded runs (tested).
   - The c1 replay is still 95 of 95 equal.
   - The three new readers were not rerun end to end, because their recorded runs write into their study folders. Their one added
     call is a read-only check.

**Checks:** 47 split tests; the suite (346), the new system's folders (239) and the frozen checks pass; the frozen files are unchanged.
Mutants: 20 of 20, including no leading 0, any topic id accepted, the years unchecked, and each reader's refusal dropped.

**On the model instruction:** agreed. Obedience and any lost mixed qualification are measured in the full prompt audit and the blind
reading, not by the fake model. The reservation total stays conditional on charges within their reserves.

**Asked:** accept the build, or name what is still wrong. If accepted, I prepare the probe at $0 and return before any send.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
