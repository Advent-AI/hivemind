# c14 stage 1 result: the main case (D433), 2026-11-12

**Stage 1 does not pass its line.** c14 opened the two years of hyperscaler capital spending as two separate theses in **7 of 9**
sends; the predeclared line was at least 8 of 9 (with c8 at most 2 of 9). c8 did it in **0 of 9**. In one c14 send no capital-spending
thesis opened at all, which c8 never did (9 of 9 opened one). By the plan (DIAGNOSIS.md, "The first test"), a stage-1 fail stops the
line and goes to Alex; stage 2 is not sent.

Run: `poc/data/clean-step1-c14-probe-2026-11-12/` (`records.jsonl`, `responses.jsonl`); the 2026-07-04 article from each draw's stored
state (step 42), three sends per draw per arm, 18 sends, all valid on the first attempt; 145,392 tokens in, 161,818 out, **$0.24** at
the published rates. Before the send: `preflight-c14.output.txt` (production's adapter rebuilds every stored sent request byte for
byte; 24 of 24 stored answers pass; a synthetic two-year answer passes), `scripts-preflight.output.txt`. After the send: 9 of 9 c8
answers keep the production answers' top-level key order; one evidence item lists `links` before `figures` (the model's own order).

## Every send, read by hand

| draw | c8 (three sends) | c14 (three sends) |
|---|---|---|
| d1 | 2026 and 2027 in one thesis; 2026 only; 2026 only | 2026 and 2027 apart; apart; apart |
| d2 | both years in one thesis (2026 with 2027 folded in); 2027 only; 2026 only | apart; apart; apart |
| d3 | both years in one thesis (2026 with 2027 as a trend); both in one (2026–2027); both in one (2026 with 2027 folded in) | **2027 only** (2026 linked as its base); apart; **no capex thesis** (all three statements kept unlinked) |

- c14's separate-bet reasons for the second year read as an analyst's: "hyperscaler budgets could beat in 2026 while 2027 guidance
  disappoints (or vice versa)"; "Calendar 2027 capex is a distinct quantity from 2026 capex (each settles from a different year's
  filings)". No send opened a third capex thesis (the duplicate stop line holds).
- c8's sends show the two old shapes: both years inside one thesis (5 of 9), the shape the ladder step refuses ("not one
  calendar year", u1 clean-5), and one year only (4 of 9). (Corrected after council B, `council/lp-codex.md`: my first count had
  them reversed.)
- Both c14 failures are on the d3 state; the saved reasoning (`responses.jsonl`, read by me) shows why, at no cost:
  - **d3 send 3, no capex thesis:** the model met c8's counterexample "A customer expanding capacity informs demand; it is not a
    thesis of its own", read the hyperscalers' spending as customers' spending, and kept all three statements as evidence with no
    thesis ("There's tension … customer capex is not a thesis"). The collision between that sentence and shared_quantity ("several
    companies' combined output or spending") is in c8; c14 did not add it, but this send fell on it.
  - **d3 send 1, 2027 only:** it weighed opening both, worried about "over-generation", and read the $650bn 2026 plan as "a baseline
    fact" rather than a bet, so it opened 2027 and linked 2026 as context.

## Council B (`council/lp-codex.md`) and what follows

The hand read stands (with the c8 count corrected); no measuring-rule error turns a miss into a pass; the line was fixed before the
send. Recommendation: stop c14, keep c8, diagnose the misses before any next version. The saved reasoning gives that diagnosis
without a paid call: one miss is the model choosing one year as the bet, the other is a pre-existing c8 sentence on customers'
capacity colliding with shared_quantity. That is D391's pattern (the error moving to a neighbouring rule), so the line is not tuned
further on this set.

## What it shows and does not

The edit moves the behaviour strongly (0 of 9 to 7 of 9 on the same states) but not to the line, and one send lost the question it
targets. One article, three states, three sends each: a lead about this case, not a rate.
