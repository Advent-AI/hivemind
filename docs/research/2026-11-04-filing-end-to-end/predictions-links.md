# Predictions for the one test of v74l (frozen 2026-11-04 before the first send; sha256 in `predictions-links.md.sha256`)

## The test

- Arms: `stored` (frozen v74i, re-sent the same day) and `v74l` (`links-v74l.json`: the links rule and three role edits), three sends each.
- Articles: 69 = development 54 (`selection-test.json`, set `dev`) + held-out 15 (`heldout.json`, sha256 `f35dcd0e…`, frozen before any v74l send).
- Requests: rebuilt byte for byte through production code; `resend_filing.py check selection-test.json --arms stored,v74l` passed on 2026-11-04
  (69 identical to the stored ones, 138 built, each role edit found once in each).
- Command: `python3 resend_filing.py send selection-test.json answers-links.json --sends 3 --arms stored,v74l`.
- Size: 414 sends; $0.60 at gpt-6-luna's published rates (`model.PRICES`: $0.10 input, $0.50 output per million tokens; input priced uncached;
  measured 8,151 prompt and 1,204 completion tokens a send on the stored arm, v74l about 440 more prompt tokens); about 15–30 minutes at 8 at a time.
- Decision: `python3 decide.py selection-test.json answers-links.json stored v74l --draws 4000`, by PRD 10 §6 as amended on Alex's "go" (D360). The
  cases it lists are read by a reader who did not write the change, for the report.

## What is predicted (estimates; the control is re-sent the same day, so its numbers move)

Per send unless said. Basis: the stored arm and the draft-0 arm (definition, no fallback) measured on 2026-11-04 (`calibrate-decide-dnf.txt`), and
the round-2 reader's reading of draft 2 (`log.md` row 11).

| Set | Measure | Control | v74l | Basis |
|---|---|---|---|---|
| development | facts the gold uses reaching a question it uses them for | 60–68 | 66–78 | stored 62 / 63 / 66; draft 0 68 / 68 / 64 (passage rule); reader: +11 right on 57 read cases |
| development | statements under v1 or v22 | 40–50 | 12–25 | stored 41 / 49 / 49; draft 0 17 / 15 / 21 |
| development | the standard's not-kept spans present | 29–37 | 20–33 | stored 37 / 36 / 29; draft 0 24 / 25 / 27 |
| development | core matters present | 48–52 | 46–53 | stored 150, draft 0 148 over three sends |
| held-out | facts the gold uses reaching a question it uses them for (22 facts) | 14–16 | 14–17 | reader: 15 reach in the stored answers, 5 never written or refused |
| both | statements with no home (dropped) | 22–32 | 35–55 | stored 81, draft 0 154 over three sends |
| development | supporting matters present | 62–70 | 55–68 | stored 197, draft 0 176 over three sends (homeless supporting matters no question uses) |
| both | single-home moves (not counted) | | the share question (v6) loses i138, i139, i155, i234, i300 to custom silicon (v16) in most sends; the v13 / v4 facts lean to v4 | the tie sentence; PRD §3 (v6 does not read v16) |
| all | prompt tokens | about 8,150 | about 8,590 | `resend_filing.py check` |

Expected verdict: pass. The least certain line is the development reach increase: it needs about +13 facts over three sends (+4.3 a send) to clear
p < 5% (draft 0 gave +9, p = 11.8%; the reassignments put one standard deviation of the summed difference near 7.6).

Per question (limits 3 drops, 2 full drops, 5 new noise, 3 full new noise; an identical variant fails in about 8–10% of reassignments): no question
fails. Listed for reading, predicted: the share question's single-home moves to custom silicon; some company-wide revenue facts filed under a
narrower driver.

## Stop and next

- Any line of the decision fails: stop, report to Alex with the census and the mechanisms read (D355: "如果有什么不符合hypothesis 的地方你需要终止然后和我说我们重新评估").
- Pass: v74l becomes a candidate; the 14-day end-to-end run, three draws, scored on the frozen judgement ruler, starts only on Alex's word (PRD §6).

## What this test cannot decide

Whether the judgements improve (the 14-day end-to-end run decides that); the wiring by which v6 does not read v16 (PRD §3); per-question changes
below the limits (two facts, two to four noise statements), which are listed, read and reported but decide nothing.
