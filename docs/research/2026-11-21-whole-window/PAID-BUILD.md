# The paid harness, built (PAID-DESIGN.md version 6, D707; for council review before any send)

Files: `paid_run.py` (plan, dry, dry-refused-upstream, send; one sequence per process), `paid_mutants.py` (five mutants of the
harness's own checks), `worksheet.py` (the pinned reading worksheet), `verdict.py` (§4's verdict from the read worksheet and the harm
findings, with its checks), `contradictions.py` (the lead parser).

## $0 evidence
- `plan.json`: the three draws' links (from the probe draws, candidate ids resolved to v14, v16, v21), readers v9, v14 (07-10), v16
  (07-15), v21 (07-26) in every draw; the controls retire 247 rows (v14 71, v9 70, v16 56, v21 50), each reader's archive judge rows from
  its first retired call on checked equal to its accepted judgements from its link day (no refused first attempt among readers).
- `paid-dry-{linked,control}-{1,2,3}.log` (a marker judge for every bought judgement, every answer "changed", so propagation is at its
  largest): all six complete; links committed exactly the probe draw's (none in controls); every probe link job met; every post-link
  reader judgement fresh (call id above the copied archive's top) and every pre-link one from the archive; the upstream snapshot check
  run on every linked reader request (267 in linked-1) with no problem; the fixed trajectory (H2) holds (non-reader judgements and every
  other table equal to old-2's). Bought: 266 per linked sequence (19 days added by propagation), 247 per control.
- `paid-dry-refused-upstream.log`: v14's first attempt on its third judgement refused (an evidence id it was not shown), its retry
  accepted; no request shows the refused answer; 267 bought (the retry); snapshot checks clean.
- `paid-mutant-{1..5}.log`, each caught: the control not retired (freshness fails); a stale upstream recorded by the harness only
  (snapshot problems); v21 missing from the allow-list (the sequence stops on 07-26); a probe link answer missing (stops on 08-06 at the
  link job); a non-reader admitted and bought (H2 fails).
- `verdict-checks.log`: 14 checks, every one as specified, including round 25's (both gains withdrawn: not improved; one withdrawn alone:
  improved; a shared error on a clear date cannot be adjusted) and round 26's (two unquantifiable CPU gains: undecided), round 24's
  (5 control definite, 13 linked unresolved: undecided) and the precedence.
- `worksheet-dry.log`: the worksheet on the dry stores: 72 distinct pairs per sequence covering the 73 dates (432 rows).
- `price.log`: from the dry counts and old-2's archived usage at published rates (cache writes 1.25x): linked about $1.06 each (+10%
  prompt growth, +5% retries), controls about $0.91 each; about $5.89 in all; the largest single reservation $0.043, six live at once
  about $0.26.

## The send (after this review and Alex's ceiling)
One ledger at the ceiling Alex names (`budget_replay.py --init-ledger`), then six processes at once:
`paid_run.py send <out> <kind> <draw> <ledger> <ceiling>` for linked-1..3 and control-1..3. Each refuses a ceiling not equal to the
ledger's, registers its launcher (the stop gate stops all when one dies), holds July's latch, and writes `summary.json`. Then the
worksheet, the hand reading (Claude, a blind reader, third reads), the findings file and `verdict.py`.

Recommended ceiling to ask Alex: $7 (the estimate plus the live reservations and about 15% margin).

## Round 28 findings and the rebuild (`codex-r28.md`, NOT READY: four)
1. **One acceptance gate** (`paid_run.acceptance`) for the dry runs and the send: the window completed with terminal `complete`; the
   committed graph equal to `pinned-plan.json`'s, labels included (none in a control); the probe jobs consumed exactly the pinned set;
   freshness; the snapshot; H2. `send` exits non-zero when it fails. The judging day is bound inside `round.judge_day` and cleared when
   it returns; a request is admitted only when its schema is `judgement` (unit check: a request titled "Thesis v14" without it, sent
   while a day is set, is not admitted).
2. **Decisive checks:** freshness is now "the accepted judgement's call was made during its own day's judging" (the archive's top before
   and after each `judge_day`; unit check: a call in another day's window fails); the snapshot compares each dependency entry, found by
   its own target id, line for line with that target's recorded judgement day, comparison point, forecast and reasons excerpt, and the
   snapshots are written to `snapshots.jsonl`; H2 uses the pinned reader set, never the admission table, and compares typed keys and every
   substantive judgement field (pushes, theme pushes, why changed).
3. **Stop paths, typed:** each sequence records every judge attempt at the transport (reader, day, request hash, retry, admitted) and
   every judge row written with its day, and a terminal outcome (`complete`, `double refusal` with the reader and day, or `infrastructure
   stop` with its reason). Exercised: `paid-double-refusal-linked.log` and `-control.log` (v9 refused twice on its second judgement:
   terminal "double refusal", gate refused), `paid-refused-reservation.log` (the paid entry point on a $0.000001 ledger: the first reader
   reservation refused, terminal "infrastructure stop", exit 1, nothing sent), the latch race (`paid-units.log`). Preflight on the inputs:
   `preflight-window.log` (old-2's archive and ledger) and `v120-replay-{1,2,3}.log` (the probe archives' link answers).
4. **The worksheet and the verdict:** `worksheet.py build` writes P rows under shuffled labels (key outside the repository) and H rows
   with the exact requests, the read judgement ids shown and the paired control's conclusion in force (H4), the seven fixed dates (H5),
   and reference changes or market-figure keywords (H3); `worksheet.py gains` writes the gain review rows after P is read (both linked
   answers per gain, deduplicated). `verdict.py` refuses: off-window dates, a date read twice or missing, a class outside the four, a
   missing or non-boolean flag, a missing or invalid gain review for a provisionally improved pair, and a run-decided flag that disagrees
   with the six summaries (`worksheet-verdict-dry.log`: a synthetic reading of the dry stores gives "pass"; each of six bad inputs is
   refused).

## Rerun evidence ($0)
- `paid-dry-{linked,control}-{1,2,3}.log`: all six accepted by the gate; 266 / 247 bought; 266 snapshot checks per linked sequence.
- `paid-dry-refused-upstream.log`: accepted, 267 bought, the refused answer shown to no request.
- `paid-mutant-{1..6}.log`, each refused by the gate on its named check: control not retired (freshness), stale upstream recorded and
  swapped upstreams (snapshot), a reader missing from the allow-list and a probe answer missing (window not completed), a non-reader
  bought (H2, now in the summary itself).
- `verdict-checks.log` (14), `paid-units.log` (3), `worksheet-verdict-dry.log`.

## Reading load, measured on the dry worksheet
P 432 rows; H4 213; H5 84; H3 1,521 in the dry run, an upper bound (every marker answer changes its reference); a real run's H3 count
is known only after the run. Gain rows 18 in the synthetic reading.

## Round 29 findings and the changes (`codex-r29.md`, NOT READY: three, and the H3 load)
1. **Acceptance carried to the verdict:** the gate adds a clean final ledger (not stopped, no overrun); `verdict.py` requires all six
   summaries accepted and evaluates terminal outcomes first (a linked double refusal fails with no packet required; an infrastructure
   stop, a control double refusal, an H2 difference or a rejected summary is inconclusive).
2. **Reviews required, conclusions derived:** the verdict regenerates the expected H rows from the stores and refuses any missing,
   unexpected or unread row; H1 from the summaries' dated judge rows on matched reader-days; H3 (a linked grounding error unmatched by
   the paired control's conclusion in force), H4 (a double count), H5 (2 or more extra material failures) from the read rows; each gain's
   credit from its two supplying answers' reviews (`gain_credit`).
3. **Packets:** the P packet alone is blind (no arm name, no H rows); the H packet carries, per row, the exact request, the read
   judgements shown with their own requests (the trace), and the paired arm's conclusion in force; H3 now includes every reader's
   conclusion in force on the seven fixed dates (v21 on 07-26 among them).
4. **H3 load:** the selection is now the structural rule (PAID-DESIGN.md §4 H3): 90 of 247 on old-2's reader answers, about 700 rows
   across six sequences with the fixed dates, against about 1,464 under the earlier trigger.

`e2e-checks.log` ($0, the dry stores, packets built and a synthetic reading): a complete reading passes; refused or failing as
specified: P rows only, an unread H row, an incomplete gain review, every gain withdrawn (not improved: fail), an H4 double count, a
linked grounding error the control lacks, two more H5 failures, a rejected summary (inconclusive), a linked double refusal with no P
rows (fail), four extra refusals on matched reader-days (H1 fail) and three (tolerated: pass). Two of my own check fixtures were wrong on
their first run (the H1 days not matched, then packet files overwritten by an earlier case) and were corrected; the code under test did
not change. `h3-load.log`: the structural rule on old-2's 247 reader answers.

## Rounds 30–31 and the pilot path
- Round 30 (NOT READY): H3's selector misses cases; review records not validated (a material failure without its reliance finding;
  duplicate rows; a quantified CPU correction stored once per company judgement); completion inferred from replay returning; reading
  estimate 18–30 reviewer-hours. Round 31 (reflection, consensus, D708): pilot first, under the rule written in PAID-DESIGN.md §8.
- Fixed for the pilot: the gate checks the completed calendar against the pinned one (`planned_days`, fixed apart from the replay's
  window; mutant `window cut short` caught, `paid-mutant-7.log`); `verdict.bind_p` refuses a P reading that is not exactly the stores'
  pairs (a substituted judgement, a shifted span, a missing or duplicated row); `gain_credit` refuses a material failure without its
  reliance finding and a duplicated review, and applies a quantified CPU correction as a corrected range compared on each gain date with
  that date's segment range as read; `verdict.pilot_decision` reads pair 1 alone and cannot give the comparison's pass.
- Evidence: the six dry sequences rerun with the current harness, all accepted with the calendar check (`paid-dry-*.log`);
  `e2e-checks.log`: the full path's 14 checks and the pilot's 7 (a complete reading continues; never a pass; a substituted P judgement and
  a missing H4 reading refused; an H4 double count stops; a quantified correction turning the gains definite stops as not improved; every
  unquantifiable CPU gain unresolved together stops as undecided).
- Still open for the full reading (not the pilot): H3's selector (round 30's cases), H5's duplicate counting.

## Round 32 findings and the changes (`codex-r32.md`, NOT READY: three)
1. **Readings bound to the regenerated rows:** `bind_p` compares each P row's dates and both answers' full forecast and reasons with the
   stores' row; `bind_rows` compares each H4 row (request, read judgements shown and their trace, the CPU judgement, control-1's answer
   in force) and each gain row (request, forecast, gain dates) with rows regenerated from the stores; every reading carries its record
   (first and second readers, a third when they differ, the final value theirs or the third's) and its excerpt. The official pilot
   decision refuses dry summaries (`allow_dry` for the $0 checks only).
2. **Numbers validated:** a resolved P class needs finite, ordered ranges for both answers and their excerpts, and must be the class the
   ranges give; a quantified CPU correction needs a finite, ordered corrected range; a corrected company answer carried across two gain
   dates gives a class per date.
3. **Order:** linked double refusal; validity; coverage; harm; control floor; credited P.
Evidence: `e2e-checks.log`, 30 checks, exit 0 (the new: dry summaries refused for the official decision; a P row with its forecast text
removed, a class the ranges contradict, a P row without its second reading, an H4 row with another request, an H4 row without the control
answer, and a NaN corrected range refused; coverage short before an H4 double count gives inconclusive; the carried correction gives
clear on one date and definite on the other). One fixture of mine set only the final H4 finding, which the new record rule refused; the
fixture was completed.

## Round 33 findings and the changes (`codex-r33.md`, NOT READY: two)
1. **Reading records checked, not only present:** each reader's value must be one of the allowed values; when the first and second
   differ, the third must be allowed and carry its quoted source (`third source`); every excerpt (P ranges, H findings) must be a piece of
   the answer or request it was read from; every gain review quotes its rule-B trace from the answer. The same record rule now applies to
   the full reading's H rows.
2. **The CPU correction only on the total-revenue answer:** a CPU increment reviewed on any other answer is refused; a quantified one
   needs the increment removed (positive) and a corrected range equal to the company's read range minus it (within $0.05B), and the same
   company answer must be read with one range wherever it appears.
Evidence: `e2e-checks.log`, 35 checks, exit 0 (new: readings outside the allowed values, an excerpt not from its answer, a gain review
without its trace, a CPU correction on the Data Center answer, and a correction that raises the total are each refused). Two of my
fixtures set only a final H finding, which the record rule refused; they were completed.

## Round 34 findings and the changes (`codex-r34.md`, NOT READY: three)
1. **A disputed reading needs a quoted source:** `third source` must be a quote of at least 12 characters from the regenerated
   evidence (the P row's stored answers; the H rows regenerated from the stores in both the pilot and the full verdict, never the text
   carried in the submitted row); a gain review needs its quoted inputs (`rule B inputs`) and the reasoning from them to its finding.
2. **The corrected range is computed:** the endpoints used for credit are the company's read range minus the increment removed; the
   reader's transcription is only cross-checked.
3. **One range per answer:** every supplying judgement, of both questions in both arms, must be read with one range wherever it appears,
   checked before any date is counted.
While making these, I found my round-33 edit had left a duplicated block in `verdict.py` (the H tables and an old `gain_credit` defined
twice, the later definition in force); it was removed and the changes applied once.
Evidence: `e2e-checks.log`, 40 checks, exit 0 (new: a disputed P reading settled with `true` or spaces, a disputed H4 finding without a
quoted source, one control answer read with two ranges, each refused; the 380.02 segment against a computed 380.00 corrected total stops
whatever the transcription says).

## Round 35 findings and the changes (`codex-r35.md`, NOT READY: two)
1. **Decimal arithmetic:** the corrected range's endpoints are computed and compared in decimal (`$400.2B` less `$20.1B` equals the
   `$380.1B` segment, so the date is not definite).
2. **Reliance per gain date:** a material rule-B failure is reviewed once per answer, and its review must give, for every gain date that
   answer supplies, whether that date's reconciliation rests on it (`reliance by date`); only those dates lose credit.
The one-range test now uses a same-class pair (the carried control answer read at $400B and $390B, both clear), so only the one-range
rule can refuse it. Evidence: `e2e-checks.log`, 43 checks, exit 0 (new: the decimal equality continues; reliance on one of two dates
withdraws only that date; a material failure missing a date's reliance is refused; the same-class two-range case is refused).
