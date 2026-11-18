# The end-to-end comparison as an exploratory census (shape B'), design version 4, 2026-11-13

Version 1 was reviewed (`clean-arch/step1-unfiled-2026-11-08/council/ml-codex.md`: not ready; round 2, `ml-codex-2.md`: four changes;
round 3, `ml-codex-3.md`: three changes and a matching clarification; round 4, `ml-codex-4.md`: Jev's unanswered attempts, the
reservation bound, one wording); every point is answered here. This shape departs from D442's same-day condition, so it needs its own council consensus and decision
under D439; D442's same-day comparison (shape A, the ladder step wired end to end, fresh ladder draws) stays owed for D427's
acceptance.

**What it is for.** An exploratory census of observed final-answer losses on the frozen judgement ruler: the clean path's stored chain
and fresh production draws, each lost graded answer traced fact by fact to its cause. The cross-system ranking is provisional: the arms
run on different days. It is never an acceptance and never waives Step 4's failed lines. Why now: no stored run of production as it now
runs (`poc-v118`, D370, D374) was found in the searched records (every `manifest.json` under `poc/data/` and
`docs/research/2026-11-01-e2e-loop/arms/`, and the run logs there), so production's own unseeded result on the ruler is unknown.

**Dates, recorded beside every number.** Clean arm: Steps 1–3, the unseeded c8 draws u1–u3, 2026-11-10 (`poc/data/clean-unseeded-
2026-11-10/`); ladders, Stage A run 4 send 1, 2026-11-10/11 (`clean-arch/step4-2026-11-10/stage_a/`); judgements, Stage B, 2026-11-11
(`poc/data/clean-stage-b-2026-11-11/`). Production arm: each draw's launch and finish times from its manifest. A judgement selected
"on or before 2026-07-14" may have been made before that day.

## $0 verification, done before any send

| check | result |
|---|---|
| frozen-prompt, frozen-judgement and frozen-ruler tests | 8 passed |
| `config.load('poc/config/poc-v118.json')` | loads; no baseline block |
| `scripts/preflight.py` over the three stored seeded v116 runs (`preflight/preflight-v116-d1..d3.txt`) | A: judge answers the code refused 6, 4, 4 (all rung-and-reference refusals, mostly the China-share question, which an unseeded run does not open); B extraction checks judged 710, 687, 708, refused 12, 10, 11 (quote not in item, duplicate quotes, one candidate with no rungs); C matching checks judged 161, 166, 165, refused 0, skipped 3, 2, 2 ("request not in this archive"); D enum values 43, missing 0; E keyed views 25, 25, 24, duplicates 0 |
| the production record reader (`prod_records.py validate`) on the seed views of the same runs | 69 question outcomes compared with the frozen scorer's printed outcome: 0 mismatches; outcomes include "no judgement" (d2), "not in run" (d1, d3, q23), "no_view" (3 a draw) as explicit outcomes, not refusals. Mutant (the first judgement instead of the last): 23 mismatches, caught |
| the evidence-visibility reader (`prod_records.py validate-shown`) | the pattern: in 711 judgements every cited id is listed in that judgement's own request; 11,134 (judgement, evidence created after its request) pairs and duplicate-note ids, none counted as shown (mutant, any e-number anywhere: 276 failures, caught). **The function `shown_evidence` itself:** equal to an independently built set (line splitting, no pattern) for all 711 (view, day) pairs; 53 cutoff cases (ids listed only after an earlier day excluded for that day); 61 cross-view cases (different views' sets differ where their requests do); a judgement whose archive call is deleted (a scratch copy) is refused. Mutants: no date cutoff, 198 failures; every view's requests, 270 failures; both caught |

*Limits.* The preflight replays v116's stored answers; v118 differs from v116 only by the removed baseline block and the removed
temperature (D370, D374), which its checks do not read, so it cannot establish v118's unseeded behaviour; the one-day slice does.
*The clean arm sends nothing new:* its requests were sent on 2026-11-10/11; its verification is that every input it uses is rebuilt
from the stored run folders (the Stage B count already refuses a packet it cannot rebuild, `stage_b/control_theses.py`).

## Procedure

1. **The one-day slice** (2026-07-01, one draw, run cap $0.25): `zsh clean-arch/e2e-comparison-2026-11-13/run_budgeted_draw.sh <folder>
   <ledger> 2026-07-01 2026-07-01 0.25` (a manifest with the configuration's, the items database's and the code's sha256, a log, a pid
   file; the shared ledger made once with `budget_replay.py --init-ledger <ledger> --ceiling 5.00`). It completes, opens its own views,
   judges them, and the readers above read its views, rungs, judgements and requests. A failure stops and goes to the council.
2. **Three draws**, the same day, detached, one launcher each, NVDA, 2026-07-01..07-14, run cap $1.00 each, the same ledger. A draw that
   does not complete is re-run once from empty if the ledger leaves room; otherwise, or on a second failure, it is left out, reported.
3. **Opened questions:** every view each production draw created (none is seeded): question, rungs, due day.
4. **Matching** to the 23 ruler questions under `clean-arch/unseeded-2026-11-10/MATCHING-v2.md`, with the brief and procedure the clean
   readers used, written down before the readers start: two families blind (labels hidden, keys outside the repository), a third reader
   on each disagreement. The clean arm's matching (`mapping-runs.json`) stands as made. For one ruler question, the candidate views
   resolve as: any SAME confirmed: matched; none SAME and at least one unresolved: "unresolved"; every candidate NOT SAME, or no
   candidate at all: "not opened in the ruler's shape".
5. **Eligibility** (question, period and quantity the ruler's; due day the ruler's, D430) by two blind readers with a third on
   disagreement, the same brief for both arms; the literal reading (the same due day) beside.
6. **Outcomes, per ruler question, per draw, per arm, the first that applies:** (i) reader B's gold open or no gold view: "not
   graded"; (ii) no candidate view confirmed SAME and at least one unresolved after the third reader (point 4's rule): "unresolved", excluded
   from opening counts;
   (iii) no view matched SAME: "not opened in the ruler's shape"; (iv) several views matched SAME: the one created first is judged, the
   others listed (an unresolved candidate beside a confirmed one is listed and does not change the outcome); (v) eligibility unresolved:
   "unresolved"; (vi) not eligible: "opened, not eligible", with the reason; (vii) no judgement on or before 2026-07-14: "no judgement";
   (viii) a figure rung with no bound: "no comparison"; (ix) agrees or disagrees, by the frozen scorer's rule (`prod_records.outcome`
   for production; the same rule for the clean arm's ladders, as Stage B counted them).
7. **Each lost graded answer traced fact by fact** (outcomes iii and vi–ix-disagree). For each of reader B's decisive items for that
   question: *extracted* (a kept evidence item of the run states it), *linked in time* (linked to the matched view before the last
   judgement on or before the window end), *shown* (listed in a judge request for that view on or before that day:
   `prod_records.shown_evidence`, and Stage B's request search for the clean arm). Two readers mark extracted and linked against the
   item text; code reads shown. **Cause, the first that applies:** (a) opening (outcome iii or vi); (b) not judged (outcome vii): the
   facts' marks are listed as observations, never as the cause of a judgement that does not exist, and never as a judgement error;
   (c) some decisive item never extracted; (d) some extracted item never linked in time; (e) some linked item never shown; (f) every
   decisive item shown and the view's rungs cannot express reader B's range (no rung band overlaps it, or a different measure);
   (g) every item shown and the rungs could express it: judgement; (h) the readers cannot settle a fact: "ambiguous". A loss with
   several causes takes the first in this order and lists the rest; each decisive item's three marks are reported.
8. **Report:** per arm and draw, each graded question's outcome and cause; every other ruler question's outcome; the clean arm's
   numbers read from its stored chain under the same rules. No pass line.

## Spending: an enforced shared ceiling

Every production run (the slice, three draws, at most one re-run) runs through `budget_replay.py`: production's own replay
(`hivemind.replay.run`, the arguments `scripts/replay.py` passes, its seeded-ledger refusal imported from it) with one change, the
transport the production code already accepts, `BudgetTransport`. Before each attempt it reserves that attempt's worst cost on one
ledger shared by every run under a lock: a language-model request (2 × its JSON bytes + 4,096) input tokens and its whole output cap at
`model.PRICES`; a Jev request the same input bound times Jev's three internal attempts, and every Jev call settles at that whole
reservation (`jev.transport` may have sent unanswered attempts that were billed). A language-model attempt goes out once and is
sent again (up to three, production's pauses) only when the service gave no answer (no HTTP status, 429 or 5xx). Every response
settles at its usage, every failed attempt and every usage-less response at its reservation; a response above its reservation stops
all later attempts. An attempt that would pass the ceiling is not sent: production records that item or judgement as failed, and the
draw counts as incomplete. **Why the reservation bounds a call's cost.** Input: a token covers at least one byte of the text it encodes, so a request's input tokens
cannot exceed its message bytes plus the few formatting tokens per message, which 4,096 covers; the reservation takes twice the whole
JSON's bytes. Measured on all 1,609 stored `gpt-6-luna` calls of the seeded v116 runs, the largest ratio of input tokens to request bytes
is 0.255 (a judging call, 10,694 tokens for 41,968 bytes), so the reservation is at least 7.8 times the largest observed input. Output:
the provider stops a completion at `max_completion_tokens`, and no stored call's output exceeded it (0 of 1,609). The $5.00 holds under
these two bounds; if a response ever exceeds its reservation, the overrun flag refuses every later attempt and the excess is reported.
**Ceiling: $5.00 for all production runs** (expected about $0.5–0.7 a draw; the reservations of the calls in
flight need about $0.5 of room), with the run caps beside (`--cap` 0.25 for the slice, 1.00 for each draw). Total under D439 at most
$4.77 + $5.00 = $9.77 of $40.

Checks (`check_budget.py`, fake services, no network): 16 threads × 20 calls under a ceiling of 5.5 reservations: spent plus reserved
never passed the ceiling, some calls refused, nothing left reserved; Jev's one-argument call reserves three attempts and settles at that
whole reservation, and after one such call a second that would pass a ceiling of 1.5 reservations is refused (mutant: settle Jev at its
reported usage, caught); two network failures then an answer: three attempts, the failures at their reservation; HTTP 400 sent once; an overrun refuses
later attempts; a request without an output cap refused; a usage-less response settled at its reservation: 10 of 10, three runs after the last change. Mutants:
no ceiling check (caught), every status retried (caught), failed attempts settled at zero (caught). The first control run caught a real
defect: ledger reads outside the lock could see a half-written file, crash a thread and leave its reservation held; reads are now
locked and writes atomic. (The numeric bound of version 2, $12.25, is replaced: it was an estimate.)

**What it will not show.** Same-day differences; fresh ladder draws; whether the clean path should go to production (D427); the daily
path of a judgement.
