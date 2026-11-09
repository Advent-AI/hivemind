# Plan v3: the clean system's first end-to-end measurement (revised for `el-codex.md` and the Claude reader's review; 2026-11-09)

**What it is.** A seeded diagnostic. Given the ruler's 22 questions as an isolated fixture, does clean Steps 1–3 deliver to the frozen
judge the facts that change answers, compared with production re-sent the same day on the same articles?

**What it is not:**
- whether the clean system would open those questions (D370);
- a production acceptance;
- an unseen-data result: dev articles tuned c8.

**A conflict Alex should see.** D382 makes financial figures conditions, not theses, yet seeds v1–v3, v10–v12, v20 and v22 are exactly
such theses. The fixture asks c8 to link figures to figure-questions it would never open itself.

## Same articles for both arms

v108 read 243 items over 07-01 to 07-14; the clean dev list has 115. The first week shares 98, and the second week is 145 against 17.
v108 also read gnews:f4eb52, which carries gold i301 and i302 (q10, q12). **Both arms therefore run on v108's 243-item list.** The items
database hash matches (57bc2544).

## Stage 0 ($0, new code reviewed by the council before any send): the adapter and the control harness

**Adapter: a chronological replay that mirrors production's dispatch.**
1. **Seeds.** For each draw, a fresh `views.sqlite`: the 22 seeds via `seeding.seed_views` at seq 0, with production's rungs,
   dependencies and ids.
2. **Insert in dispatch order.** Article k gets seq k:
   - its records become evidence `e<N>`, inserted in record order;
   - its Step 1 links go on the record that carried them;
   - Step 3's links a repeat brought, and later links, are inserted at the seq of the article whose processing made them
     (`library.later_log`);
   - a revision inherits the revised piece's links, as `writing.py:256–261` does;
   - links are inserted in dispatch order, because judging shows evidence in link-insert order (`store.py:415`).
3. **Judge once per day.** After a day's last article, the frozen `round_of_judgements` (judging-v7, gpt-6-luna) runs for only the
   views that got a new link that day, as `round.py:64–83` collects them, with seq equal to that article's seq.

**Field mapping** (each choice counted and reported):
- `one_line` = summary, unchanged.
- `quote` = the verified passages. The judge's 400-character cut applies, and what it cuts is counted.
- `speaker` = reporting_speaker; `original_who` = original_party; `original_day` = statement_date (null allowed); tier as written.
- A record with no verified passage is dropped and counted, as production drops "quote not in item".
- Clean-opened theses are listed and not judged, except an unsigned-obligation signing thesis the system opened itself. That one gets
  the standard's yes/no ladder and is scored for q23 only through the scorer's own rule.

**Control harness.** Current `scripts/replay.py` refuses seeded ledgers (lines 29–48 and 80; `tests/test_no_seed_replay.py`).
- The control is a separate harness that calls `hivemind.replay.run` with poc-v108 (which has no baseline) on a seeded ledger. It leaves
  replay.py unedited.
- extraction.py and judging.py changed after v108's commit a907eba. So the control's requests are first rebuilt and byte-checked
  against the 11-03 archive with `scripts/preflight.py`. A mismatch stops the control.

**Checks:**
1. **Leakage, both bounds.** For each judge request on day d, every shown item's link seq is above the previous day's judging seq and
   at or below this day's, and its source day is d or earlier. Checked from the request text and the database. A mutant inserting one
   future record must fail.
2. **Request shape.** An adapter request is compared field by field with the stored v108 request for the same view and day.
3. **Answer path.** A synthetic answer passes `check_answer` given the request text (`judging.py:207`), and `_record` writes it.
4. **Scorer.** The scorer accepts both arms' databases.

Stage 0's checks run on Stage 1's seeded output, since the unseeded trace links nothing to a seed.

## Stage 1 (cents, after Alex's word on the fixture): the delivery probe

**Treatment.**
- c8, unchanged, with a seeded before-state: the 22 seeds, plus only those clean theses that duplicate no seed. For example, clean-3
  (China H200) is dropped as v8, and clean-1 is dropped as v9.
- The rule for showing a seed as a c8 thesis is frozen before sending: description = the seed question, outcome = its ladder's labels,
  period = its due date.

**Control.** The stored unseeded c8 request, re-sent the same day.

**Articles:**
- The stored c8 trace already wrote the 66% margin (seq 63), the cash flow (seq 57) and both Broadcom figures (seqs 59, 80), all
  unlinked. Those articles go in, plus the China-share and Ohio articles.
- Controls are articles carrying company-figure facts production gets right: v1, v3, v11 and v22. c8's CONDITION rule could stop
  linking those, and that loss is the larger risk.
- Three draws each. Requests are rebuilt and verified, and predictions and stop conditions are frozen with sha256 before the send.

**It decides one hypothesis.** It holds if c8 with the seeds links q10's and q12's facts in at least 2 of 3 draws, without losing the
control seeds' links. If it fails, that goes to Alex before Stage 2. It is not proof about other questions.

## Stage 2 (on Alex's word): three draws per arm, same day, same 243 items

**Decision rule, frozen before sending:**
- Report every question and draw for both arms, with and without the reader-noise questions (q09, q12, q23; `gold-v1.json`
  stick_noise). Read the judge's reasons for every disagreement.
- **Better:** clean total minus control total is at least 3 over the three draws, both with and without the noise questions; q10 and q12
  both agree in at least 2 of 3 clean draws; and no question the control agrees in at least 2 of 3 drops to 0 of 3 in the clean arm.
- **Worse:** a difference of −3 or less, or such a drop.
- **Inconclusive:** anything else, including ties. It is reported as inconclusive, never as a pass.
- The null is the two stored v108 control sets (46 and 46).
- The oracle's q16 result is recorded as grounded in 0 of 3, not 1 of 3.

**Cost (estimate):**
- clean c8 on 243 items is about $2.5 a draw, and Steps 2–3 with Jev are small;
- judging is about $0.36 a draw;
- the v108 control is about $0.75 a draw.

About $11 for three paired draws, priced from earlier tokens at published rates.

## For Alex

1. The 22 seeds as an isolated fixture for this diagnostic, given D370 and D382.
2. The same-day v108 control through a separate harness, without editing replay.py.
3. Stage 0 now ($0). Stage 1 (cents) after item 1. Stage 2 (about $11) only on his word after Stage 1.

## v4 revisions (for `ep-codex.md`)

- **Leakage, defined two ways:**
  - **No future in the database:** at each judging seq, no evidence, source, link, same_claims or revisions row exists whose article
    seq is above the day's seq, or whose source day is after d.
  - **Selection is production's:** the shown set equals the frozen `evidence_in_view` output (arrivals since the fifth-latest
    judgement, plus the basis of the last ten), checked by recomputation.

  The "since yesterday" bound is removed. A mutant that inserts one future row must fail the first check.
- **Stage 0 runs before any send,** on constructed seeded cases: stored clean records with hand-made links to seeds, covering a later
  link, a repeat, a revision and a multi-day judge sequence. The same checks rerun on Stage 1's output afterwards.
- **Proving the control harness:**
  - **Inputs:** the harness takes an explicit ordered item list, the 243 items with their order read from
    `poc/data/e2e-r9-frozen-v108-2026-11-03/d1/replay.log`. It refuses any other list.
  - **Bytes:** before any send, it rebuilds v108's extraction and judging requests for the archived 11-03 run and compares each
    `model.request_identity` sha256 with the 11-03 archive. Any mismatch stops the control. This is a dedicated check, not preflight.
- **Calibrating the decision rule:**
  - Its false-call rate is estimated, before any send, by resampling the six stored v108 draws (r9 and r10 control) as
    control-against-control. The threshold is the smallest total difference whose false-call rate is at most 10%, frozen with its
    sha256.
  - **Precedence:** a per-question collapse (a question the control agrees in at least 2 of 3 that falls to 0 of 3) makes the result
    "worse" whatever the total. "Better" needs the total threshold, both q10 and q12 agreeing in at least 2 of 3, and no collapse.
    Anything else is inconclusive.
- **Stage 1 comparison, observable in both arms:**
  - For each target fact: is it written, and is it linked to any thesis?
  - For the treatment: is it linked to the seed asking its quantity?
  - For the control-figure articles: are the company-figure facts written in both arms, and, in the treatment, linked to v1, v3, v11
    and v22?
  - Duplicate questions: a new thesis a blind reader judges to ask the same as a seed.
- **Explicit adapter mappings:**
  - A group member Step 2 judged a repeat becomes `same_claims(original, member)`.
  - A `revises` entry becomes `revisions(old, new)`, and the revised piece's links are inherited.
  - quote = verified passages only; unverified passages are dropped.
  - A record with no verified passage is dropped.

  Every drop and truncation is reported as an adapter loss, per draw.

## Qualifications carried into Stage 0 (`er-codex.md`, READY WITH CHANGES)

- **The control's byte proof checks the outgoing request as sent,** dict and key order as built (AGENTS §5). `model.request_identity`
  sorts keys, so it is not enough on its own.
- **The calibrated threshold is exploratory.** Six historical draws cannot establish today's false-call rate or rule out drift, and the
  report says so beside the threshold.
- **Stage 0 settles two mappings:**
  - how several revisions and a repeat group's links map into the judge's single-predecessor fields;
  - the check that a clean-opened Ohio question is equivalent to q23 before it is scored.
- **The adapter, the control harness and their checks get a council read before any send.**
