# Reading plan for the full run (D451, D452; WIRING-DESIGN.md §E, §F) — version 3, agreed in council mq (D452)

Written while the run is live (2026-11-13), from the stored procedures; the volumes are filled in when the run lands. Every procedure
below is carried over unchanged from its reviewed source; anything that is not is listed under "Open points" for the council.

## 1. The census, same day (diagnostic; D442's shape)

- **Inputs:** the opened theses of the clean draws c1–c3 (Step 1's traces) and the views of the production draws p1–p3; the frozen ruler's
  23 questions (seeds v2 plus q23).
- **Matching:** MATCHING-v2 (`clean-arch/unseeded-2026-11-10/MATCHING-v2.md`, sha in `MATCHING.sha256`): two blind families, a third
  reader on every difference, as for q1–q3 (`clean-arch/e2e-comparison-2026-11-13/matching/`).
- **Selection, eligibility and outcome: the census design's points 4–6 as written** (`DESIGN.md` lines 45–61), for both arms: a ruler
  question's candidates resolve as matched, unresolved or not opened in the ruler's shape; several views matched SAME: the one created
  first is judged and the others listed (p3's two credit-support views, if both match, fall under this rule); eligibility by two blind
  readers with a third, D430's due-day reading with **the literal reading (the same due day) printed beside**; outcomes in the design's
  order (i)–(ix), by the frozen scorer's rule (`prod_records.outcome`; the clean draws' views databases have the same tables). The Ohio
  question stays in the census.
- **The loss trace: the census design's point 7 as written** (`DESIGN.md` lines 63–71): every lost graded answer traced fact by fact for
  each of reader B's decisive items — extracted, linked in time, shown — with the cause the first that applies of (a) opening, (b) not
  judged, (c) never extracted, (d) never linked in time, (e) never shown, (f) rungs cannot express reader B's range, (g) judgement,
  (h) ambiguous; several causes: the first, the rest listed; each item's three marks reported.
- **Reports:** point 8 as written; the seven graded questions apart; no pass line. It describes; it decides no acceptance.

## 2. Stage A on fresh theses (the ladder step's lines, D400)

- **Population:** every opened thesis of c1–c3, three passes each (`<draw>/ladder/send-1..3/outcomes.jsonl`).
- **Form and accounting:** `ladder/stage-a-reader-brief.md` and the third-reader brief, unchanged; both families on every written ladder
  and every refusal, in shuffled packets with the key outside any reader's folder; a third reader on every differing firm mark and every
  W; my own read of every disputed mark behind a line; the NOT MEASURED rules of the design (a missing row or ruling; more than a third
  of mark pairs differing). A send refused twice (by a check, the schema or as not JSON) has no reader packet and counts in line 5 as
  not right, reported by reason.
- **Lines 1–4 and 6** as written (no ladder fails Q, L or R; no refusal fails N; direction and due-day agreement with their minimum
  denominators, 3 and 20, and NOT MEASURED below them).
- **Line 5, a council-set diagnostic line (decision before any count, citing D439):** right ≥ ceil(35·N/44) and right by a ladder ≥
  ceil(28·N/44) for the N fresh theses. Alex's D400 wording (35 and 28 of 44) is printed beside it with the actual N and the result; it is
  not reported as Alex's line. N = 0 reads NOT MEASURED (zero thresholds would pass vacuously).
- **D400's limit in every report:** Stage A measures the step against the lines and its own three sends; it does not establish that the
  step writes better ladders than production, nor any comparison with production.

## 3. Stage B on the fresh path (the judge's six conditions, D428; D429's reading)

- **Population:** every judgement of c1–c3's judge folders.
- **Procedure:** `stage_b/STAGE_B_READING.md` as written: one draw a packet, at most one judgement of a view a packet, both families on
  every judgement, two third readers on every differing verdict, my read of every UNSUPPORTED, the trial of planted answers before the
  reading, the count by `baseline_count.py` generalised as for Stage B.
- **Conditions:** every draw completed; at least nine in ten laddered theses judged; at least eight eligible controls with reader B's
  material shown, all but one agreeing; figure judgements UNSUPPORTED at most five points above the baseline; yes/no at most 5%; last
  judgements at most three UNSUPPORTED in 30, scaled; each under the three treatments of unresolved verdicts.
- **Line 3's special rules, as written** (`STAGE_B_READING.md` lines 75–99): the Ohio question is listed apart and is in neither count
  (it stays in the census); the literal due-day reading's eligible, shown and agreeing counts and its line printed beside; how many
  compared answers were made on 2026-07-14 and how many earlier.
- **Planted answers:** two new ones per test, written on the full run's own judgements by the procedure of `STAGE_B_READING.md`,
  reviewed by the council for a real fault and no give-away; then the trial and its rule unchanged; the trial, planted-control,
  disagreement and session-time stop rules all kept.

## 4. The fresh inputs, verified in two gates (council mq)

The stored tools read u1–u3's folders and mapping (`stage_b/control_theses.py`, `stage_b_trial.py`, `baseline_count.py`, the census
builders). After the run has ended (no code edit while it is live), they take the fresh folders (and, for Stage B, the reviewed mapping) as
inputs, as the adapter now does, each with a $0 check: the packets and counts rebuild from the fresh folders; a missing or mismatched input
is refused; the stored u1–u3 build is reproduced byte for byte with the defaults.

- **Gate 1, after the run ends:** the census-matching packets and Stage A's reading packets: every opened thesis of each arm once in the
  matching packets; every written ladder and refusal of the three passes once in Stage A's packets. Then those two readings start, side
  by side.
- **Gate 2, after the census mapping is reviewed:** Stage B's control theses and packets from that mapping and the fresh folders: every
  original judgement exactly once, the repeats and the planted answers counted apart as `STAGE_B_READING.md` requires; the new planted
  answers reviewed; the trial completed. Then Stage B's main reading starts.

## Points settled in council mq (round 1), to record as a decision before the readings

Line 5 as a council-set diagnostic line (above); two new planted answers per test, reviewed, then the trial; census matching and Stage A's
reading side by side, Stage B after the census's mapping. The earlier open points, kept for the record:

1. **Stage A line 5 on another population size.** Alex's line is counted on 44 theses (at least 35 right, at least 28 right by a ladder).
   The full run's population is whatever c1–c3 open. Carrying the same proportions (35/44, 28/44, rounded up) is a change of the line's
   form, not of its standard; it needs a recorded decision (D439) before any count.
2. **Stage B's planted answers.** The six planted answers were written on Stage B's own judgements because readers could identify
   planted answers built on other runs (`council/kv-codex.md`). The full run's judgements are new; new planted answers on them, with
   their trial, are needed, or the reuse of the six must be argued.
3. **Control theses (Stage B line 3)** come from the mapping of the fresh theses to the ruler (the census's matching); the census reading
   therefore runs first.
4. **Order and size:** census matching → Stage A reading → Stage B trial and reading; packet sizes as before; sessions fresh and
   read-only; an incomplete reading reported not measured.
