# The period split's $0 build (D616 → D617 → D618 → D619), 2026-11-16

Nothing is sent. The frozen answer-choice step's files are unchanged (`git diff` empty on `ladder_step.py` and the candidate request
files).

## Built

- **`clean-arch/step4-2026-11-10/ladder/ladder_split.py`** (scratch, beside the frozen step, which it imports):
  - the schema, with only `no_ladder` changed to a closed set: the seven frozen decline cases, transcribed verbatim (a test checks
    each phrase), plus `one_quantity_two_periods` with `periods`;
  - the period check (identity only: two different years written alike, exactly this year and next as of the item's day);
  - a yearly re-ask's check: its year's figure ladder, or another case, with no recursion;
  - the split flow, which re-asks once per year with the one added line;
  - truthful display: the model's reason for a decline, code's words for two failed validations.
- **The writer** (`stage_b/ladder_adapter.py`):
  - `clean_ladders` gains `period`, keyed (`thesis_id`, `period`): `''` for every unsplit row, as before;
  - `open_split` writes the parent's `split` row and one row per year;
  - one view per written year, its id digits only (`v42026`), because the frozen judge reads theme ids by `v\d+`;
  - the parent's statements go to every written year;
  - a written year lists an unwritten sibling as not judged.
  - A view-id collision would need a store with more than ten thousand topics, and the views table's key refuses it rather than
    overwriting.
- **The frozen Stage B readers** (`control_theses.py`, `stage_b_count.py`, `control_census.py`, `page_store.py`) call one refusal
  (`stored_judgements.refuse_split_store`) before any read of the table. A historical store without `period` passes unchanged.

## Proven

- `ladder/test_ladder_split.py` (17) on the real topic c1/clean-4 and its article, with the frozen step's own checks:
  - the schema's only change;
  - the period rule (9 cases);
  - the re-asks, whose requests are byte-equal to the frozen request plus the one line;
  - a declined year and a year failing twice;
  - no recursion;
  - an ended-year split refused with nothing split;
  - every other answer passing through unchanged;
  - malformed declines.
- `stage_b/test_split_writer.py` (13):
  - rows and views for both years, one year and no year;
  - statements reaching every written year;
  - not judged with the model's reason or code's words;
  - a crash after the first yearly row leaving no row or view of the article;
  - the library showing two ordinary yearly questions;
  - an unsplit replay (u1) with every `period` empty;
  - the readers refusing a split store and accepting a historical one;
  - a structural check that each reader refuses before its first read.
- `ladder/test_split_budget.py` (2):
  - with three sends held in flight, the others are refused and the spend stays within the cap;
  - **the bound's assumption exercised:** a provider reporting more tokens than the reserve assumed passes the cap by exactly the
    excess of the sends in flight. The $0.40 ceiling holds while every charge stays within its worst-cost reserve (request bytes and
    the output cap).
- The suite passes (346), the new system's folders (224), and the frozen checks. Mutants: 8 of 8 caught (`split-mutants.txt`).

## The request's growth (AGENTS §6)

- The schema grows from 6,116 to 7,223 characters (+1,107); the refusal description from 824 to 1,298.
- A yearly re-ask adds 124 characters to the closing text (64 before round 159; see below).
- **The reason:** the decline cases become the closed set AGENTS §6 asks for, in place of the prose list, and the one new case and its
  field are added. Nothing else in the request changes.

## Not yet done (the probe, separately reviewed)

- choosing its 13 topics from the stored cases (T 2, C1 6 with at least 2 open base years, C2 2, C3 2, M 1);
- a probe runner beside `stage_a.py`, sharing its limit;
- the frozen request rebuilt byte for byte as the control;
- the reading packets with the two plants;
- the full prompt audit of the changed request.

## Round 159's findings and what changed (D618)

The council did not accept the build. Three proofs claimed more than they showed, and one boundary was unstated. Each was checked
against the code and fixed.

1. **The crash proof called `rollback()` itself.**
   - It now runs the real replay loop in its own process. The last u1 topic's stored outcome is replaced by the split outcome (a
     stand-in: the transaction is tested, not the topic's wording).
   - The process kills itself with SIGKILL right after the first yearly row's insert. Preflight's locked copy of the crashed store
     holds no ladder row, view or processing record of that day, and every completed day ends before it.
   - **The defect it found:** the writer, run on its own, could not import the split module, because only the tests put the ladder
     folder on the path. The writer now appends that folder last. None of its modules shares a name with the writer's own folders.
2. **"Neither view lists the other year" (DESIGN.md v4 §0b item 2) had no owner.**
   - **Census:** 746 of the 3,335 stored left-out parts name a year, and most are not the question's year (a monthly peak, a slip to
     a later year, a projection). So whether a part *is* the other year's quantity is meaning, and code cannot decide it.
   - **The yearly line now tells the model:** "Write the question for {year} only; {other} is asked as its own question, so do not
     list it as a part this question leaves out." It adds 124 characters to a yearly re-ask (it was 64).
   - Code passes the model's parts unchanged and adds only what it knows: a year with no question. Tests cover both years written
     (the model's parts unchanged, including one naming the other year and a mixed one) and one written (the model's parts plus
     code's).
   - Whether the model obeys is measured by the probe's reading, not by code.
3. **The page and reader proofs were narrower than reported.**
   - The detail page (`bundle.view_bundle`) and the Idea bundles (`bundle.thesis_bundles`) now show each written year as an
     ordinary question with its year and its not-judged list, in both the two-year and the one-year state. An unwritten year has no
     detail page.
   - Each frozen Stage B reader is driven through its own entry point on a split store and refuses by name before any output:
     `control_theses.packets`, `stage_b_count.main` (now before reading its arguments), `control_census.main`, and
     `page_store.main` (before it replays).
   - **Historical stores, through the same entry points:**
     - `page_store.py` replays the stored c1 draw through the current writer: all 95 judge requests are answered from the archive,
       and every judgement and every ladder row equals the stored draw's;
     - `control_census.py`'s output is identical to its saved `control-census.txt` (49 lines);
     - `check_stage_b_count.py` drives `stage_b_count.py` and `control_theses.py count` on its made-up readings over the completed
       Stage B stores: 21 of 21 cases as expected.
   - Every reader of `clean_ladders` (`bundle.py` and the four Stage B readers) selects named columns. None reads by position.
4. **Yearly view ids could collide with ordinary ones** (`clean-4` in 2026 is `v42026`, as `clean-42026` would be).
   - The writer now refuses any topic number of 10,000 or more, or one that is not digits, before writing.
   - So an ordinary id has at most four digits, and a yearly id is the number followed by a four-digit year (at least five digits).
     Within one topic the two years differ and are written alike.

**Checks:** 35 split tests; the suite (346), the new system's folders (227) and the frozen checks pass; the frozen step's files are
unchanged (0 diff lines). Mutants: 14 of 14 caught (`split-mutants.txt`): the period rules, the yearly line, the sibling entry, the
statements, a commit of the parent row on its own (caught by the killed-process test), code dropping the model's parts, and each
reader's refusal. The yearly-line mutant first failed through the fake model's empty queue (traceback read). The fake now fails with a
named assertion, and the mutant is caught by it.

## Round 160's finding and what changed (D619)

The council refused the size bound. It refused topic numbers of 10,000 or more on the ordinary path too, which changes unsplit
behaviour. And `isdigit()` with `< 10,000` let a leading-zero number through, so "an ordinary id has at most four digits" did not
hold. Both were true when read against the code.

- **Yearly ids now begin with 0** (`v042026` for clean-4's 2026 view). An ordinary id is `v` and the topic number, and a topic number
  never begins with 0. So no yearly id can equal an ordinary one, whatever the size. Within yearly ids, 0, the number and a fixed
  four-digit year decode one way only. The frozen judge reads `v\d+`, which a leading 0 meets. The page's id pattern accepts it. No
  code converts a view id to a number for identity: `baseline.py` sorts the old system's seeded views by number, for order only.
- **The canonical topic-id contract, with its evidence.** Step 1 numbers topics with an integer counter
  (`clean-arch/step1/runner.py:350-352`). Every stored topic id has the form `clean-` and a number without a leading zero: 3,457 ids
  in 163 case and outcome files, 18 distinct, the largest 18. The writer now refuses any other form before writing anything; no stored
  input meets that refusal. The size bound is gone.
- **A split's two years are checked at the writer too:** two different years, written alike, each `2026` or `FY2027`. A malformed
  stored outcome is refused before anything is written.
- **The reader inventory missed a dimension:** code that maps a view to its topic by its id (`clean-<view number>`) without reading
  the ladder table. A search over all code found four such readers of the new system's stores:
  - `carried-run/build_sources.py`, `side-by-side/build_side_by_side.py` and `pilot-deck-1/build_deck.py` would silently map a
    yearly view to no topic. Each now calls the shared refusal right after opening a store, and each entry point is tested on a split
    store (`build_sources.main`, `build_side_by_side.load_entries`, `build_deck.main`).
  - `e2e-comparison-2026-11-13/opening-review/build_opening_cases.py` opens no store. It reads that study's fixed files, and a yearly
    id would stop it with an error (`next` finds no topic), never a wrong answer.
  - The other `v{k}` uses are the old system's 22 seeded views.
- **Historical stores:** the shared refusal passes every store the seven refusing readers read in their recorded runs (six stores,
  tested). The three new readers were not rerun end to end, because their recorded runs write into their study folders; the one added
  call is a read-only check shown to pass on their stores. The stored c1 draw replays through the current writer with 95 of 95
  judgements and every ladder row equal.
- **Tests:**
  - an ordinary `clean-42026` beside the split `clean-4`, through the real writer: views `v42026`, `v042026` and `v042027`;
  - four non-canonical topic ids refused with nothing written;
  - four malformed split years refused with nothing written.

**Checks:** 47 split tests; the suite (346), the new system's folders (239) and the frozen checks pass; the frozen step's files are
unchanged. Mutants: 20 of 20 caught (`split-mutants.txt`), including yearly ids without the leading 0, any topic id accepted, a
split's years not checked, and each of the seven readers' refusals dropped.
