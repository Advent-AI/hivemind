# The period split, design v4 (D615; v1 to v3 refused in council rounds 155 to 157), 2026-11-16, $0

**What it repairs:** the open defect D397 names, for one kind only. A topic that tracks **one quantity in two years** (D38: "one view a
year") is refused today as having "several figures, none the main one". Two worthwhile bets are lost. Example: the five largest
hyperscalers' capex in calendar 2026 and in calendar 2027.

**What it does not claim:**
- it moves no gate: the official 44 hold no such topic;
- it does not touch D436's second sides, two-thing stakes or several products;
- it departs from D397's "at most one judged question per topic" for this one case only, as §1 names. That departure is recorded as a
  council decision under D439 before any build, reversed on Alex's word.

## 0. What changed from v1 (round 155)

- **The split now needs both years open,** this year and next (D38's "at most this year's and next year's"). A topic naming an ended
  year is never split, so v1's "an ended child equals an ordinary answer" is gone.
- **Steps 1 to 3 are untouched.** The parent stays the only topic; the split is two yearly views of it. That is a named, narrow
  departure from D397.
- **The page sees two ordinary views and no new state.**
- **Partial results, the measurement's denominators and the treatment of the 44 are specified.**

## 0b. What changed from v2 (round 156)

1. **Every yearly attempt has its own identity.** `clean_ladders` gains a non-null `period` column, and its key becomes (`thesis_id`,
   `period`):
   - an unsplit thesis keeps one row with `period = ''`, as today's rows are read;
   - a split parent has its `''` row with status `split` and the two years in its answer;
   - each yearly attempt has a row with `period = 'Y'`, whatever its outcome, and its view or none.
   - **Every reader is specified:**
     - `bundle.ladder_row` reads by `view_id`, unchanged, since a yearly view's row is unique;
     - `stage_b/control_theses.py`, which reads one row per thesis, reads the `''` row. On status `split`, it reads the yearly rows and
       treats each written yearly view as its own candidate for comparison with the ruler's question of that year, and an unwritten
       year as having no view;
     - the writer (`ladder_adapter.open_thesis`) writes the rows.
     - A search of `clean_ladders` over `src/`, `scripts/` and `clean-arch/` finds no other code reader.
2. **"Not judged" depends on the result:**
   - **both years written:** neither view lists the other year;
   - **one written (2026), the other refused:** the 2026 view lists "calendar 2027: no question written (<the refusal's reason>)" as
     not judged;
   - **neither written:** no view, and both refusals recorded on their rows.
   - The list is fixed when the views are written, in the same article, and the bundle and page tests cover all three states.
   - **Yearly view ids (D619):** `v`, 0, the topic's number and the four-digit year (`v042026`): digits only, as the frozen judge
     reads `v\d+`, and never equal to an ordinary id, because the writer refuses a topic id that is not `clean-` and a number without
     a leading zero (Step 1's counter; every stored id has that form). Readers that map a view to its topic by id refuse a split store
     (BUILD-RESULT.md, "Round 160").
   - **Who decides (D618):** whether a part is the other year's quantity is meaning, so the model is told in the yearly line ("{other}
     is asked as its own question, so do not list it as a part this question leaves out"). Code passes the model's parts unchanged
     and adds only the year that has no question. The probe's reading measures whether the model obeys.
3. **The transaction and recovery boundary, from the code:**
   - **The model calls** (the parent's, then each year's) run in the answer-choice step's runner. Each pass has its own archive, and
     the thesis's outcome line is written to `outcomes.jsonl` only after both yearly calls have returned.
   - The runner refuses an existing folder, and a stopped run is never started again (`stage_a.py` header). A crash after either call
     therefore leaves an incomplete run that is not resumed: no paid call is repeated and no outcome line is half-written.
   - **The writer** writes the parent's row, the yearly rows and their views in `open_thesis`, inside the article's commit, before
     judging. Its replay refuses an existing output folder, and an incomplete draw is never continued.
   - So a crash before the article's commit leaves none of these rows. A crash after it leaves the article's rows complete, in a run
     marked incomplete and not continued.
   - **The real-path proof** is a crash injected after the first yearly row's insert in `open_thesis`: the store then holds no row of
     that article. v2's "day atomicity" wording was wrong; it is article-level.
4. **The reading verdict is decisive.**
   - **Vetoes:** on any yearly ladder of T or M, a failing Q, O, R, L or N settled by both families (the gate's hard lines), a base-year
     question, or a lost qualification. On a C1 ladder, a hard-line fault that the frozen arm's ladders of that topic do not show.
   - **Both countings:** a lead must hold with unresolved points counted for the answer and counted against it. A lead under one only
     is inconclusive.
   - **Incomplete readings:** a missing third ruling, a missing first-reader row or a missed plant voids the reading (no verdict).
   - A refused yearly attempt counts in T's rule, not as a reading fault.
   - A control whose frozen sends disagree on kind is reported as **unexercised** for the kind rule; the case rule still applies to it.
5. **The spend bound:**
   - parent calls: 14 topics × 3 sends × 2 arms = 84;
   - yearly re-asks: up to 2 per new-version send that names the case, at most 84;
   - one retry per call.
   - That is at most about 336 calls at about $0.001 each, under a **ceiling of $0.40** on its own ledger, inside D439's remainder.

## 0c. What changed from v3 (round 157); this section governs where earlier sections differ

1. **The key is (`thesis_id`, `period`) everywhere,** with `period` non-null: `''` for an unsplit thesis and a split parent, `'Y'` for a
   yearly attempt. **Every code reader of `clean_ladders`** (searched in `src/`, `scripts/`, `clean-arch/`, `docs/research/`):
   - `src/hivemind/bundle.py` (`ladder_row`, by `view_id`): unchanged and applicable, since a yearly view's row is unique;
   - `stage_b/ladder_adapter.py`: the writer, which writes the rows;
   - `stage_b/control_theses.py` (one row by thesis), `stage_b/stage_b_count.py` (counts `status = 'ladder'`),
     `stage-b-controls/control_census.py` and `not-judged-display/page_store.py` (research scripts reading one row by thesis or every
     row): **these are the frozen Stage B accounting and research readers. Each refuses, by name, a store holding any row with
     `period != ''`.** The split is not silently mapped onto the control line. In Stage B it stays a diagnostic until a separately
     reviewed mapping (each yearly view to a frozen question, unmatched years, duplicates, denominators) exists.
   - `stage_b/mutants.py` names the writer's insert line, and its mutant is updated with the line.
   - The probe is of the answer-choice step only, and does not use these readers.
2. **Failure display, truthful:**
   - a yearly attempt the model declined shows "calendar Y: no question written (<the model's own reason>)";
   - one whose answers failed the step's checks twice shows "calendar Y: no question written (the answers failed the step's checks
     twice)", in code's words, never as the model's explanation.
3. **One verdict rule:** §0b item 4's is authoritative and §3's older verdict is replaced by it.
   - Counting **for:** an unresolved mark holds. Counting **against:** it fails.
   - A lead must hold under both.
4. **The population is 13 topics:** T 2, C1 6, C2 2, C3 2, M 1. **Spend:**
   - parent calls: 13 × 3 sends × 2 arms = 78;
   - yearly re-asks: at most 2 for each of the new version's 39 sends, so 78;
   - with one retry per call, at most 312 calls.
   - **The ceiling ($0.40)** is enforced by the answer-choice runner's existing spending limit: one limit for every request, reserved
     before each call and charged from the returned tokens or the reserve, stopping every worker at the first refusal (`stage_a.py`
     header; `budget`).
   - The yearly re-asks go through the same caller and limit.
   - **A $0 test** shows a cap below the parent and yearly total stopping before it is passed, with workers running concurrently.

## 1. The unit, ownership and the writer path

- **The topic:** the parent thesis stays the one topic Steps 1 to 3 know (its id, its links, Step 1's list of open theses, Step 3's
  library, revisions). No child topic exists upstream, so later matching, revisions and links find the parent as today. This avoids
  changing Step 3's frozen library (D427).
- **The views:**
  - the answer-choice step writes one view per year for the parent, `v12@2026` and `v12@2027`, each with its own year, question,
    ladder and due day by the existing rules (D414);
  - each yearly attempt has a ladder row keyed (`thesis_id`, `period`), as §0b item 1 and §0c item 1 specify;
  - the writer's mapping is `mapping['clean-12'] = ['v12@2026', 'v12@2027']`.
- **The departure from D397, named:** for this case only, one topic carries one judged question per open year.
  - D38 (Alex) makes one quantity in two years two views.
  - D397 (Alex) calls the present behaviour for such a topic "an open defect until splitting is built".
  - Every other multi-part topic keeps D397's one judged question.
  - Recorded as a council decision under D439 before any build, reversed on Alex's word.
- **Evidence:** every statement linked to the parent reaches both yearly views' judges, as it reaches the one view today. Each judge
  reasons for its own year. That a 2026 statement reaches the 2027 judge, and the reverse, is a property of this design. Its effect on
  judgements is **not tested by the ladder probe**; it is named as an open question for any later judging test.
- **Not judged:** as §0b item 2: it depends on which years were written.
- **Closing:** per view, as today. A statement arriving after one year's view has closed reaches it as a closed view (linked, not
  judged, counted: the existing behaviour and its test) and reaches the open sibling normally.
- **Presentation:** the page and `bundle` read ladder rows by view, so each yearly view is an ordinary question with its year. No new
  state reaches the page. The $0 checks show the library, the detail page and the Idea bundles on a store holding a split parent,
  unchanged for unsplit topics.

## 2. The boundary and every outcome

| Case | Who decides | What happens |
|---|---|---|
| One quantity, both years asked independently, both open | **the model:** typed case `one_quantity_two_periods` with `periods: [Y1, Y2]` | **code:** two distinct years, both this year or next by the step's existing year rules, so the case is accepted; the step is re-asked once per year with the one-line restriction |
| Either year ended, or beyond next year | — | **code:** the case is refused as malformed; re-asked once (the existing retry), then `refused twice`. Nothing is split |
| One open year as the question and another open year as its base or reference ("2027 against 2026") | **the model:** it must answer the asked year with the other as reference, as it does in the 20 stored one-year topics | **if the model names the case anyway, code cannot tell.** That is the misuse the probe's controls measure, and it is a stop condition |
| Two quantities, a second side (D436), a two-thing stake (Intel, Firmus) | the existing main-part rule | not this case; naming it without two open years is malformed (as above) |
| Several products over two open years | the model may name the case | each yearly re-ask meets the main-part rule for its year and may refuse |

**Every outcome of a split send:**
- both years write valid ladders, giving two views;
- one writes and the other refuses or fails validation twice, giving one view and the other year's refusal recorded on its row with its
  reason. This is not claimed equal to today's behaviour;
- both refuse or fail, giving no view and both refusals recorded;
- a re-ask naming the case again is malformed, and `refused twice` (no recursion).
- **Interrupted:** see §0b item 3. The boundary is article-level, with no resume.

**The schema change is a behaviour change, and it is measured as a new version.** `no_ladder` becomes `{case, reason, periods?}`, with
`case` a closed set: the existing prose decline cases, transcribed without a new rule, plus `one_quantity_two_periods`. The prompt
audit and a request diff come before any send.

## 3. The measurement (a product rule, apart from the official gate)

**The probe** (separately reviewed; about $0.10). Topics:
- T: the 2 development topics, one quantity over two open years;
- C1: 6 stored topics naming two years and tracking one, including at least 2 with an open base year ("2027 against 2026");
- C2: 2 second-side topics;
- C3: the 2 guards, Intel and Firmus;
- M: the several-products memory topic.

**Arms:** frozen step, 3 sends a topic; new version, 3 sends a topic, with children re-asked as the design says. Same day.

**Counts, fixed now:**
1. **T, per topic:** a send succeeds when it names the case and both yearly re-asks write valid ladders. A missing, refused or invalid
   re-ask fails the send. The topic passes with at least 2 of 3 sends succeeding. Both T topics must pass.
2. **C1, C2, C3, per topic:**
   - any send of the new version naming the case fails the topic;
   - an outcome change also fails it: the frozen step's 3 sends agree on their kind (ladder or refusal) and at least 2 of the new
     version's 3 sends have the other kind;
   - when the frozen step's sends themselves disagree on kind, only the case rule applies.
   - Every control topic must pass.
3. **Readers:** two blind families read every yearly ladder of T and M and the C1 ladders, mixed, with the gate form's marks plus two
   questions: does this question ask a year that was only a base or reference, and does it lose a qualification of the original
   topic?
   - Disagreements go to third readers of both families, as in the gate method.
   - Planted: one yearly ladder that asks a base year, and one that drops a qualification. A missed plant voids the reading.
   - A base-year question or a lost qualification settled by both families fails the probe.

**Verdict:** as §0b item 4 and §0c item 3: lead, negative, or no verdict when the reading is void.

**The 44:** the official gate's topics hold no one-quantity-two-open-years topic. Whether a no-change regression read of the 44 may be
sent under D426's stop is **a council decision before any adoption**, not assumed. If it may not, adoption is decided with that limit
stated.

## 4. The stop condition

Close the candidate if any of these happens:
- the model names the case on any control;
- a yearly question asks a base or reference year;
- a qualification is lost;
- the guards break;
- the $0 checks show any reader of `clean_ladders`, the page or the Idea path changing what it shows for an unsplit topic.
