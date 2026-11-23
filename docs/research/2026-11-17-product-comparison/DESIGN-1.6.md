# The §1.6 tools: what D665 prints beside the verdict (design v7, before any output is read; D672)

Governing text:
- `RUN-PLAN-v12.md` §1.6;
- `stage0/verdict-rule.json`: `hard_checks` and `printed_beside`.

The ruler and the frozen instruments do not move (D674). Every reader is a closed session (`census/census_readers.run`), one per
family, with memories off (D661).

v2 answered round 4's Part B and v3 round 5's. v4 and v5 answer round 6: Codex in `tools-review-codex-6.md`, and a Claude reader. Every
round's Part B points are summarised in D675.

## 0. Inputs, release status and the report

- **Stores.**
  - Every tool reads a draw's components from its `run.json`: `components[c]['folder']`, so `step1-redo` or `step2-redo` after a D449
    redo, and the judge's completed attempt (`mapping.store_paths`).
  - `eligibility.py` fingerprints every file a tool reads: the judge or old store, `step1/trace.sqlite`, `step2/decisions.json` and
    `library.json`, `cases/cases.json`, and each pass's ladder `outcomes.jsonl`.
  - Each tool refuses a file whose sha256 differs.
- **Release status sits beside the verdict and does not replace it.**
  - `score_comparison` gives the verdict (invalid / too small / lead / loss / no winner).
  - The report prints "hard checks clear" when every hard check passed. It prints "release blocked: <check> failed" for a check that
    failed, and "release not cleared: <check> not measured" for a check that could not be measured (D665: "a release blocker reported
    with the verdict").
  - Release itself still needs a practical lead and Alex's word. Nothing is deployed.
- **A hard check that is not measured cannot clear release.**
  - The frozen rule says this of Step 2's lines. This design reads it the same way for D400's code parts, whose own accounting marks a
    line "not measured" below 3 company-figure theses or 20 laddered theses.
  - This is a reading to settle in the council and record before any output; it is the cautious, reversible course.
- **Printed beside, each from its tool:**

| Item | Tool | Source |
|---|---|---|
| D428's limits beside the guardrails | `score_comparison.beside` | Labelled as a comparison on the guardrail sample, not Stage B's measurement. Each system's figure share against 12.7% to 14.4%; its yes/no share against 5%; its decided latest answers (figure and yes/no) unsupported against 3 in 30, scaled; with denominators, and the insufficient latest answers beside |
| Sign test and interval (illustrative) | `score_comparison.beside` | Per counting, over the discordant matters (served by exactly one system): two-sided binomial p on a against b, and the Wilson 95% interval for the new system's share among them, labelled illustrative |
| Company-figure subgroup a, b, N | `score_comparison.beside` | Built |
| Days from first source to opening | `score_comparison.beside` | For each matter and draw with a confirmed covering question (split covers not counted): the earliest publication day among the matter's `articles` (the census numbering), to the earliest opening day of a covering question. A question opened before 09-07 is printed "opened in the warm-up"; one opened in the window before that day, "opened before the first listed article" |
| Floors | `score_comparison.beside` | §4 |
| D400 reader lines, D400 code parts | §1 | |
| Step 2's three lines | §2 | |
| D431's 07-14 reading | §3 | |
| 37 bulk-viewer articles excluded; 2 split matter pairs kept apart | report text | D669 and D671 records |

## 1. D400, all three passes

- **Code parts** (`d400_code_check.py`): Stage A's accounting, line 6, on each new draw's three ladder passes. The ladder folder comes
  from `run.json`, and every `outcomes.jsonl` is checked against its fingerprint in `eligibility.json`.
  - A skipped ladder component (no question opened) is "not measured".
  - Stored two-week runs (c1 to c3) could not measure the due-day line (7 to 11 theses with three ladders, 20 needed). The full window
    has about 8 times the articles.
  - "Figure ranges meet end to end" is enforced at the write (`ladder_step.check_answer`).
- **Reader lines 1–5:** Stage A's reading, unchanged, run per draw. Line 5's minimums scale as D452 scaled them
  (`clean-arch/e2e-comparison-2026-11-13/READING-PLAN.md`): ceil(35N/44) right and ceil(28N/44) right by a ladder. D400's 35 of 44 and the
  actual N are printed beside.
  - `d400_reader_lines.py` recomputes line 5 from `collect_readings.py report`'s counts (right, right by a ladder, of N) with the
    scaled minimums. `accounting.py` hard-codes 35 and 28, so its own line 5 is not read. N = 0 reads "not measured" (D452). `collect_readings.py` reads one ladder folder and its packet files:
  `build_reader_packets.py <key> --run <ladder folder>=<cases.json> --readers <draw's reader folder>`, then
  `collect_readings.py rows | disputes | report` on that folder.

## 2. Step 2's three lines on draw new-1 (hard)

Inputs: new-1's Step 1 trace, its `decisions.json` and its `library.json`. The seed is 20261117 plus the line's number.

**Line 1, search: recall over known labelled counterparts, not over every real repeat** (as the Step 2 log §12 labels it).
- **Sample:** records are drawn in rounds, one at random from each of three equal article strata (by forward position) per round, until
  100 have a labelled counterpart or the strata are exhausted. The first 100 labelled records in draw order are the sample.
- **Candidates:** earlier records only, in forward order, from two routes that do not use Step 2's embeddings:
  - entity-wide word overlap, top 10, scored by `views/matching._words` directly, as R0e scores it (no embedding fetch);
  - the same original party within 3 days.
- **Labels:** two readers, one per family, answer the neutral relation question of the Step 2 reference labelling
  (`poc/data/step2-validation-2026-11-07/v2-prompt-*.md`, question 1: the relation of the later record to the earlier, with no claim that
  the system filed it). Each disagreement goes to one more closed session, whose family is drawn per pair by seed, so that no family
  settles every dispute. A counterpart is a pair labelled `same_statement`, as `score_final.py` counts it.
- **Generator-miss audit:** the Step 2 log's whole-history scan (`build_reader_packets.py scan`), run on a fixed subset of 12 sampled
  records: the first 4 drawn in each stratum. Each record is shown in full beside every earlier record's summary, chunked.
  - Each record the scan flags is a candidate, not a label. It goes through the same full-context labelling and adjudication as the
    routes' candidates before it can count.
  - The audit's yield is reported: the counterparts the routes missed.
- **The labels are frozen** (file and sha256) before Step 2's candidates are read.
- **Pass:** a group holding a labelled counterpart is among the record's Step 2 candidates (`decisions.json` `candidates`) for at least 90
  of 100 labelled records. Fewer than 100: **not measured**.

**Line 2, clear wrong merges.**
- **Population:** every repeat in `decisions.json` that was not refused, each joined to its recorded `repeat_of` original.
- **Sample:** 200 at random.
- **Reading:** the frozen Step 2 merge reading (`poc/data/clean-step2-forward-2026-11-08/merge-prompt-1.md`, and `merge-third-prompt.md`
  from the same folder on every pair either reader rejected).
  The packet goes in the prompt in place of the file path.
- **Pass:** the third reader's `wrong` count is at most 4 of 200. Fewer than 200 repeats: **not measured**.

**Line 3, later details: the shipped renderer, as the Step 2 log §12 measured it.**
- **Population:** groups whose original has at least one later report.
- **Sample:** 30 at random.
- **The two renderings:**
  - "grouped": the frozen dossier, `step3/library.group_text(member_text=True)`;
  - "apart": each member as its own entry, `record_text`.
- **An independent detail key, of content only** (the council's round-8 consensus, D675):
  - **A detail** is what a later report's statement adds to its group's original: "a figure, condition, party, date or qualification an
    analyst would want to keep" (the Step 2 reference's question 2; PRD §6, "details a later report adds, such as a guidance
    condition"; the recorded test's "detail" category).
  - The record's own attribution fields (tier, stated day, period, reporting speaker) are not shown to the key readers. The publisher
    and publication date are shown as context only, and the prompts say they are never details (`CONTENT_ONLY`). A party or period
    that changes the claim still counts when the statement's own text says it.
  - Two closed key readers, one per family, each list the details. A third session settles every detail they do not share.
  - The key is frozen before either rendering is read.
- **Reading:**
  - Each rendering of a group goes to its own closed session in each family: four sessions per group. No session sees both renderings,
    as in the recorded test, where each reader read one view.
  - Both renderings carry the same surrounding dossier: the other groups under the same thesis, each as its original's record.
  - The session marks which key details its rendering states.
- **Pass:** over the 30 groups, the grouped rendering's detail total is no fewer than the apart rendering's, summed over both families,
  as the recorded test summed both readers. Each family's totals are printed beside.
  - The mean paired difference per group is printed with a 95% bootstrap interval over groups.
  - Fewer than 30 groups: **not measured**.
- **Printed beside:** the count of later reports whose tier, stated day, period or speaker differs from the original's (the fields
  `group_text` drops), counted by code.
- **Disclosed with the result:** both renderings carry the same content, so the line checks that grouping loses no content a later
  report adds, against the readers' own noise. It is weaker than the recorded test's unprompted questions.

Lines 1 and 2 are decided on their point estimates, with a Wilson 95% interval printed beside.

## 3. D431's frozen-reference reading at 07-14 (printed beside; both systems)

D442's procedure (`clean-arch/e2e-comparison-2026-11-13/DESIGN.md`, "Procedure", steps 3 to 6) is run as it was run then, on both
systems' draws as they stood at 07-14. It compares the answers the systems actually gave; MATCHING-v2 §4's adapter, which would re-ask
the ruler's question, is not built (D442's precedent).
- **The as-of state:** every view created on or before 2026-07-14 is listed first: by `created_seq` up to the last sequence of 07-14,
  closed views included. Then `service.state_as_of` at 2026-07-14 is read for each one. New-system units are joined by
  `clean_ladders.view_id`, split children included.
- **Step 4, matching:** MATCHING-v2's SAME rule, two blind families, and two third readers, one per family, on each disagreement, as the
  full run did (`READING-COMMITMENT.md`). A split stays unresolved. D442's rule for a ruler question's candidates applies.
- **Step 5, eligibility:** question, period and quantity the ruler's, and due day the ruler's (D430). Decided by two blind readers, with
  two third readers, one per family, on a disagreement; a split stays unresolved. The literal reading (the same due day) is printed beside.
- **Step 6, outcomes:** the first that applies, (i) to (ix).
  - Several SAME views: the first created is judged and the others listed.
  - A figure rung with no bound: "no comparison". A unit that differs from the ruler question's, or that cannot be established:
    "no comparison (unit)". No conversion is made.
  - Agreement by the frozen scorer's rule (`prod_records.outcome` for the old system; for the new system the same rule, as Stage B counted
    it: "Ruled out" and "Still open" answer no, `stage_b/control_theses.py`).
- **Printed:** per ruler question and draw, its outcome; and per draw and system, the agreements on the seven graded questions.

## 4. The floors (printed beside; proposed, not gates)

As their source states them (`docs/research/2026-11-14-use-acceptance/reflection-10/codex-1.md`; `RUN-PLAN-v2.md` §1.6). Each floor is
computed per draw and under both countings, and holds when it is met in at least 2 of the system's 3 draws:
- **Covered:** at least 80% of important matters have a covering question.
- **Trivial or duplicate:** at most 20% of the questions, counted as decided worth marks on every random-sample card, covering cards
  included. The frozen rule keeps covering cards out of the guardrail shares only.
- **Supported:** at least 90% of latest answers, counted on every answered random-sample card. An insufficient or unresolved answer is
  counted and gets no credit.

Wrong citations and answer-changing omissions: **not measured**.

## Tables

**Value × reader:**

| Value | Written by | Read by |
|---|---|---|
| `eligibility.json` (all fingerprints) | eligibility | every §1.6 tool, export, scorer |
| d400 code check | `d400_code_check` | report: release status |
| d400 reader lines 1–5 | `d400_reader_lines.py` (Stage A's tools on verified copies) | report: printed beside only |
| step2-lines.json | `step2_lines.py` | report: release status |
| d431-0714.json | `d431_reading.py` | report |
| beside quantities | `score_comparison.beside` | report |

**State × event:**

| Event | Handling |
|---|---|
| A reader session voids | Retried once, then reported missing. A line with a missing mark is not measured |
| A draw stopped or ineligible | No release verdict. `eligibility.py` still records every finished draw's fingerprints and names the draws that stop the aggregate. The tools run on what finished, as a diagnostic (plan §1.4 item 10) |
| A file changed after eligibility | The tool refuses |
| A component was redone | Its counted folder is the one `run.json` names |
