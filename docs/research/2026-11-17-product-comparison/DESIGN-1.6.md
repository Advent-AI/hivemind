# The §1.6 tools: what D665 prints beside the verdict (design v2, before any output is read; D672)

Governing text:
- `RUN-PLAN-v12.md` §1.6;
- `stage0/verdict-rule.json`: `hard_checks` and `printed_beside`.

The ruler and the frozen instruments do not move (D674). Every reader is a closed session (`census/census_readers.run`), one per
family, with memories off (D661).

v2 answers round 4's Part B: Codex in `tools-review-codex-4.md`, and the Claude reader summarised in D675.

## 0. Inputs, release status and the report

- **Stores.**
  - Every tool reads a draw's components from its `run.json`: `components[c]['folder']`, so `step1-redo` or `step2-redo` after a D449
    redo, and the judge's completed attempt (`mapping.store_paths`).
  - `eligibility.py` fingerprints every file a tool reads: the judge or old store, `step1/trace.sqlite`, `step2/decisions.json` and
    `library.json`, and each pass's ladder `outcomes.jsonl`.
  - Each tool refuses a file whose sha256 differs.
- **Release status sits beside the verdict and does not replace it.**
  - `score_comparison` gives the verdict (invalid / too small / lead / loss / no winner).
  - The report adds "release: clear", or "release blocked: <check>" for any hard check that failed or was not measured (D665: "a release
    blocker reported with the verdict").
- **A hard check that is not measured cannot clear release.**
  - The frozen rule says this of Step 2's lines. This design reads it the same way for D400's code parts, whose own accounting marks a
    line "not measured" below 3 company-figure theses or 20 laddered theses.
  - This is a reading to settle in the council and record before any output; it is the cautious, reversible course.
- **Printed beside, each from its tool:**

| Item | Tool | Source |
|---|---|---|
| D428's limits beside the guardrails | `score_comparison.beside` | The new system's figure share against 12.7% to 14.4%, its yes/no share against 5%, as D428 states them |
| Sign test and interval (illustrative) | `score_comparison.beside` | Matters served by exactly one system: two-sided binomial p on a against b, and the Wilson 95% interval for a/(a+b), labelled illustrative |
| Company-figure subgroup a, b, N | `score_comparison.beside` | Built |
| Days from first source to opening | `score_comparison.beside` | For each matter a system serves: the matter's `first_day` (`matters.json`) to the earliest opening day of a covering question, per draw |
| Floors | `score_comparison.beside` | §4 |
| D400 reader lines, D400 code parts | §1 | |
| Step 2's three lines | §2 | |
| D431's 07-14 reading | §3 | |
| 37 bulk-viewer articles excluded; 2 split matter pairs kept apart | report text | D669 and D671 records |

## 1. D400, all three passes

- **Code parts** (`d400_code_check.py`): Stage A's accounting, line 6, on each new draw's three ladder passes. The ladder folder comes
  from `run.json`.
  - A skipped ladder component (no question opened) is "not measured".
  - "Figure ranges meet end to end" is enforced at the write (`ladder_step.check_answer`).
- **Reader lines 1–5:** Stage A's reading, unchanged, run per draw. `collect_readings.py` reads one ladder folder and its packet files:
  `build_reader_packets.py <key> --run <ladder folder>=<cases.json> --readers <draw's reader folder>`, then
  `collect_readings.py rows | disputes | report` on that folder.

## 2. Step 2's three lines on draw new-1 (hard)

Inputs: new-1's Step 1 trace, its `decisions.json` and its `library.json`. The seed is 20261117 plus the line's number.

**Line 1, search.**
- **Sample:** records drawn at random in three equal article strata (by forward position).
- **Candidates:** earlier records only, in forward order, from two routes that do not use Step 2's embeddings:
  - entity-wide word overlap, top 10 (`retrieve.py` R0e);
  - the same original party within 3 days.
- **Labels:** two readers, one per family, answer the neutral relation question of the Step 2 reference labelling
  (`poc/data/step2-validation-2026-11-07/v2-prompt-*.md`, question 1: the relation of the later record to the earlier, with no claim that
  the system filed it). A third reader settles disagreements.
- **Generator-miss audit (Step 2 log §1):** for each sampled record, 5 random earlier records of the same entity that neither route
  returned are labelled the same way. A same-statement pair found here is a labelled counterpart too, and the audit's yield is
  reported.
- **The labels are frozen** (file and sha256) before Step 2's candidates are read.
- **Pass:** a group holding a labelled counterpart is among the record's Step 2 candidates (`decisions.json` `candidates`) for at least 90
  of 100 labelled records. Sampling stops at 100 labelled records. Fewer: **not measured**.

**Line 2, clear wrong merges.**
- **Population:** every repeat in `decisions.json` that was not refused, each joined to its recorded `repeat_of` original.
- **Sample:** 200 at random.
- **Reading:** the frozen Step 2 merge reading (`merge-prompt-1.md`, and `merge-third-prompt.md` on every pair either reader rejected).
  The packet goes in the prompt in place of the file path.
- **Pass:** the third reader's `wrong` count is at most 4 of 200. Fewer than 200 repeats: **not measured**.

**Line 3, later details.**
- **Population:** groups whose original has at least one later report.
- **Sample:** 30 at random.
- **The two renderings vary the grouping alone:**
  - "apart": each member as its own entry;
  - "grouped": the original, then each later report under it.
  - Both use the same per-record fields (`step3/library.record_text`'s head line for every member).
- **An independent detail key:** a third-family reader lists, from the members' own records, every material detail that only a later
  report adds. This is the key, and it is frozen before either rendering is read.
- **Reading:** two readers, one per family, each read both renderings under random labels and mark which key details each rendering
  states.
- **Pass:** over the 30 groups, the grouped rendering's paired detail total is no fewer than the apart rendering's, under both readers
  (the recorded "no fewer" test). Fewer than 30 groups: **not measured**.

The point estimate decides each line. A Wilson 95% interval is printed beside.

## 3. D431's frozen-reference reading at 07-14 (printed beside; both systems)

- **The as-of state:** each store's own readers at a day (`service.py`'s as-of path): questions opened from inputs published on or before
  07-14, and the latest judgement with an input id of `day:2026-07-14` or earlier.
- **The mapping:** two blind readers map each question to the 23 ruler questions under MATCHING-v2's SAME rule, and a third reader settles
  disagreements.
- **A substitution, recorded here before any output:**
  - MATCHING-v2 §4's adapter, which re-asks the ruler question on the mapped evidence, is not built. It would change what the system
    answered.
  - This reading compares the answers actually given. It is therefore a different measurement from D395's seven-question score, and it
    is labelled as such.
- **Comparable only when the questions are the same:**
  - a yes/no question with the same due day as the ruler question;
  - a figure question with the same period, measure and unit. The unit comes from the old system's `view_keys.unit` and the new system's
    checked ladder answer (`figure.unit`).
  - Every other SAME match is "not comparable", for example another deadline or a part of a total.
- **Agreement** uses `score_judgement.py`'s own rules.
- **Printed:** per question and draw: agree, disagree, not comparable, not opened, or opened but not judged. Also the count of comparable
  agreements on the seven graded questions, per draw and system.

## 4. The floors (printed beside; proposed, not gates)

From the cards, per system, under both countings:
- **Coverage:** matters served / N.
- **Trivia:** trivia marks among the guardrail sample's decided worth marks. Duplicates are reported apart.
- **Supported:** supported answers among the guardrail sample's decided answers.

Wrong citations and answer-changing omissions: **not measured**.

## Tables

**Value × reader:**

| Value | Written by | Read by |
|---|---|---|
| `eligibility.json` (all fingerprints) | eligibility | every §1.6 tool, export, scorer |
| d400 code check and reader lines | `d400_code_check`, Stage A tools | report: release status |
| step2-lines.json | `step2_lines.py` | report: release status |
| d431-0714.json | `d431_reading.py` | report |
| beside quantities | `score_comparison.beside` | report |

**State × event:**

| Event | Handling |
|---|---|
| A reader session voids | Retried once, then reported missing. A line with a missing mark is not measured |
| A draw stopped or ineligible | No release verdict. The tools run on what finished, as a diagnostic (plan §1.4 item 10) |
| A file changed after eligibility | The tool refuses |
| A component was redone | Its counted folder is the one `run.json` names |
