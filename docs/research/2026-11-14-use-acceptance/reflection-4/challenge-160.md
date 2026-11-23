# Round 160: your four findings of round 159, fixed (D618; `splitting/BUILD-RESULT.md`, "Round 159's findings")

1. **Crash.**
   - `stage_b/test_split_writer.py::test_a_writer_process_killed_after_the_first_yearly_row_leaves_nothing_of_that_day` runs
     `ladder_adapter.replay('u1', …)` in its own process. The last u1 topic's outcome is replaced by a split outcome.
   - The process SIGKILLs itself right after the first yearly row's insert.
   - Preflight's locked copy then holds no ladder row, view or processing record of that day, and the completed days end before it.
   - A mutant that commits the parent's row on its own is caught.
   - **It found a real defect:** the writer could not import `ladder_split` outside the tests. Now fixed (`ladder_adapter.open_split`
     appends the ladder folder last; no module name collides).
2. **Not judged with both years written.**
   - I first wrote code that annotated the model's parts naming the sibling year. I withdrew it after a census: 746 of 3,335 stored
     parts name a year, and most are not the question's year ("the $3.20/hour peak in May 2026", "slipped from 2027 to 2028"). Whether a
     part is the other year's quantity is meaning (AGENTS §2: code owns identity).
   - The owner is now the yearly line: "Write the question for {year} only; {other} is asked as its own question, so do not list it as
     a part this question leaves out." It is 124 characters, up from 64.
   - Code passes the model's parts unchanged and adds only "{other}: no question written" when the sibling has no view.
   - Tests cover both written (parts unchanged, including one naming 2027 and a mixed one) and one written (the parts plus code's
     entry). The probe's reading measures obedience.
   - Recorded in DESIGN.md v4 §0b item 2.
3. **Readers.**
   - The detail page (`view_bundle`) and the Idea bundles (`thesis_bundles`) are tested in both the two-year and the one-year state.
   - Each Stage B reader's entry point is driven on a split store and refuses by name before writing anything: `control_theses.packets`,
     `stage_b_count.main` (now before reading its arguments), `control_census.main`, and `page_store.main` (before replaying).
   - On historical stores, through the same entry points:
     - `page_store.py` replays the stored c1 draw with the current writer: 95 of 95 judgements and every ladder row equal the stored
       draw's;
     - `control_census.py`'s output is byte-identical to `control-census.txt`;
     - `check_stage_b_count.py` gives 21 of 21 as expected.
   - All five readers of `clean_ladders` select named columns.
4. **Ids.** The writer refuses a topic number that is not digits or is ≥ 10,000, before writing. Ordinary ids have at most four digits;
   a yearly id is the number plus a four-digit year, so at least five. Within a topic the years differ and are written alike.

**Checks:** 35 split tests; the suite (346), the new system's folders (227) and the frozen checks pass; the frozen step's files are
unchanged. Mutants: 14 of 14 (`split-mutants.txt`).

**Asked:**

1. Accept the build, or name what is still wrong.
2. If accepted: the next step is the probe's $0 preparation. That means the 13 topics chosen by written rules from stored cases, a
   runner beside `stage_a.py` sharing its limit, the frozen control rebuilt byte for byte, the reading packets with the two plants, the
   full prompt audit, and the actual reservation sum against $0.40. It returns to you before any send.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
