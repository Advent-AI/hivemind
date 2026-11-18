# A fresh controlled comparison of A2 (D586): provenance check and design, version 4 (council rounds 95 to 98; round 98: go for the $0 proofs), nothing sent

## 1. Provenance: no stored topic set is held out

| Stored topics | Used in developing arms A to A3 |
|---|---|
| July (three runs, about 40 topics) | the probes' motivating, recovery, refusal and disputed topics; PROMPT-AUDIT-LINE-2 §7 recount; DECLINE-AUDIT read all 66 descriptions and outcomes |
| fortnight (13 topics) | the probes' motivating, regression and harm-control topics; CENSUS.md |
| week of 10-06 (13 topics) | the probes; CENSUS.md; d436-reading |
| week of 09-22 (7 questions) | PROMPT-AUDIT-LINE-2 (the line-2 failures that started the line) |
| carried library (10-06 articles) | the same week's matters as above |
| Alex's 44 (Stage A) | the ladder step's own design; D426: not tuned further |

**Conclusion:** fresh topics need the first step to open them from articles no new-system run has read.

**Exposure, rechecked today** (`fresh-exposure-2026-11-16/`; the census re-run into a new folder, searching `poc/data`, `clean-arch` and `docs/research` with its stated exclusions):
- **The week of 2026-10-13..19:** 383 eligible articles; 20 sent before by a run, probe or reading packet. The census list is
  `week-10-13-exposure.txt`.
- **The other 363:** they appear only in source-page work (page fetching and lineage diagnostics). The earlier census excluded that
  work by rule, and so does this one.
- **Per day:** 48, 66, 73, 52, 44, 46, 54.

## 2. Design (version 2)

- **The run:** clean Step 1 as frozen (c8, D427), on the whole week in source order, all 383 articles.
  - The 20 seen-before articles stay in the run, so the library meets what it would meet.
  - Topics they open are out of the population, as in the 10-06 week.
- **Why the whole week:** from a carried library fewer topics open than from empty. The carried-library test opened 4 against 16 on
  the same 11 articles. The 10-06 week opened 13 topics from 272 articles from empty, so three days would likely give fewer than 5.
- **Starting library:** the completed library of the week of 10-06 (`poc/data/clean-second-week-2026-11-15/week-continued/c1`).
  - It is real earlier material (D559). It is not a library accumulated over several weeks: that week began from empty and was
    finished after a stall (`second-week/COMPLETION-DESIGN.md`). This is stated with every number.
  - The entry point and starting state are proven at $0 first, as for the carried library.
- **An incomplete run:** if the ledger's reservations stop the run, the $0 proof shows what it reports. Only completed articles'
  topics enter the population; the run is marked incomplete; an incomplete run gives no verdict.
- **Cost and limits:**
  - The 10-06 week charged $3.55 for 272 articles, $1.11 of it on cut attempts. That is about $0.0094 an article clean and $0.013 with
    losses. The proof (`fresh-a2/fresh_a2_proof.py`, F7) gives $3.60 with no cut attempt and $6.06 at the 10-06 cut rate.
  - **A new shared ledger, ceiling $6.50**, used through `run_live.py --shared-ledger`.
    - **Proven at $0** (`fresh-a2/launcher_proof.py`, round 100): the ledger charges each answer at its usage, a network loss is
      resent and charged at its reservation, and a ceiling stops the run midway and reports it incomplete.
    - **Without the shared ledger** the cumulative reservations would stop the week after about 51 attempts.
    - **The largest reservation** among 25 requests with the unchanged 13-topic library is $0.157. The library grows during the week
      and real answers cost more than the recorded empty one, so the ledger may stop the run before it completes. That is an
      incomplete run: no verdict, back to the council.
    - **Limits file:** max_seconds 28,800; max_calls 700; the stored run's prices.
  - The answer-choice calls are about $0.10. Reader sessions sit outside the ledger and their dollar cost is not priced.
  - The D439 spend after the run would be about $31.6 of $40.
- **The answer-choice step:** each topic in the population gets the frozen request (control) and A2, three sends each, the same day.
- **The population, classed before any answer is read:**
  - **Who:** a fresh blind Codex reader and I, separately. Each gets every opened topic and the development matters (the 66 stored
    topics' descriptions and outcomes, and Alex's 44).
  - **What:** each topic is marked as on a development matter, on a different matter, or uncertain. Where the two of us disagree, the
    topic is uncertain.
  - **The decision runs on two populations and must agree on both:** (a) every topic outside the seen-before articles; (b) its
    different-matter topics. When they disagree, the result is inconclusive.
  - **Each population needs its own minimum:** at least 5 topics, and the control failing L on at least 2 of them.
    - A population below either is reported in full, with no verdict.
    - A verdict needs both populations exercised.
    - When only (a) is exercised, its numbers are reported as "not shown to be independent of the development matters", with no
      verdict.
    - The risk is stated now: (b) may be small, so the run may end with a fresh gate reading and no comparative verdict.
  - Whatever the comparison gives, the control arm is reported as a fresh gate-1 reading of the frozen step.
- **The reading:** the unchanged gate-1 form (Alex's six lines; `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`), with H
  added and reported, never a veto. Two families, third readers of both, and three planted controls.
- **The expected effect on the reader (D391):** the product shows "Not judged" parts beside an answer (D570). A part left unlisted
  means the card hides what the answer ignored. A2 should make the card honest about its scope. It is not expected to change the
  judged answer.

## 3. What is reported, and the decision written now

**The unchanged gate report, for each arm:**
- all six lines under their unchanged accounting, with every failing send listed;
- unresolved points counted for the answer, then against it;
- no claim that a zero-fault line passed unless it has no failing send;
- line 5 as raw counts (topics right in 2 of 3 sends, and those by written answer choices) over n. Its 35 of 44 and 28 of 44 are
  marked not applicable to this population. Nothing here is called Alex's gate verdict.

**The comparison (a diagnostic, beside the gate report):**
- **Lead** needs all of these, in both populations and both countings:
  1. A2 fails L (a part left unlisted) on fewer topics than the control, and on at most 1.
  2. A2's sends failing N (an unjustified refusal) are no more than the control's.
  3. **No regression traced to the change.** For every other line and mark (H included), each send where A2 fails a mark the
     control does not fail on the same topic is read and classed, before the verdict, in `trace-review.json`, as for A3:
     - **consistent with the change:** the failing content is what A2's added definition asks the step to list or decline;
     - **pre-existing:** the same fault appears in the control's sends of that topic;
     - **uncertain.**
     Any failure consistent with the change is negative, except on H. H is reported and is never a veto: an extra listed item is not
     one of Alex's six lines. Any uncertain failure other than on H makes a lead "lead, uncertain harms". H's uncertain points are
     reported apart and never change the verdict. The control-against-itself differences
     (`control-vs-control.txt`) are printed beside the counts as context only, and no bar is computed from them.
- **Inconclusive:** the control fails L on fewer than 2 topics, or the populations or countings disagree.
- **Otherwise negative.**

H is printed per topic. A lead is evidence on one fresh week. It is not a pass of Alex's gate.

## 4. After the first step: the steps in order (each at $0 unless said)

1. **Check the run:** `run_live.py` exit 0, and the trace reads complete (`fresh_a2.opened_topics`). An incomplete run gives no
   verdict and goes back to the council.
2. **Cases:**
   `clean-arch/step4-2026-11-10/stage_a/build_cases.py --fresh f1 --draws poc/data/clean-fresh-a2-2026-11-16 --parts step1/trace.sqlite --output poc/data/clean-fresh-a2-2026-11-16/cases/cases.json`.
   Its fresh path counts only topics new beyond the starting library. It was checked on the 10-06 continuation, where it gave 4
   cases, equal to `fresh_a2.opened_topics`.
3. **Population (a):** every case whose opening article is not in `fresh-a2/seen-before-10-13.json` (20 articles).
4. **Population (b), classed before any answer is read:**
   - `population.py packet` builds the packet. A fresh blind Codex reader (`population-brief.md`) and I class it separately, and
     `population.py join` joins the two; a disagreement counts as uncertain.
   - (b) is the topics both of us class `different matter`.
   - `population.json` is written and its sha256 recorded.
5. **The check:** `fresh_probe.py check`. Then the council, before the answer-choice send.
6. **After the council's word:** `fresh_probe.py send`, then the reading as for the probes (`../reading_prep.py`, packets, two
   families, third readers, H), then `fresh_score.py`, the trace review, the result, and the council.

**Built and tested at $0:**
- `fresh_probe.py`, checked on a stand-in of the 10-06 week's 13 cases;
- `fresh_score.py`;
- `test_fresh.py`: 4 tests through the whole stand-in pipeline;
- `fresh-mutants.txt`: 4 mutants, each caught.
