# The D750 second writer test: result

Run folder: `poc/data/judging-v13s-blind6-2026-11-23/`. It was registered in `SMALL-DESIGN.md` §5 [D750], with council round 66's
changes, and scored by `blind6.py tally` (`TALLY.json`, `reasons.json`). The request is `judging-v13s.txt`, sha256 `54f5847d…`.

## 1. Verdict: FAIL on one settled line

| Packet | Answer | Shape, rung | First readers (Codex, Claude) | Adjudicators (Codex, Claude) | Settled | Line |
|---|---|---|---|---|---|---|
| X06 | fresh E Claude | forecast, rung 3 ($35B: 1.75x pace) | yes, no | no, no | **no** | **FAIL** |
| X07 | fresh E Codex | unresolved | yes, yes | (none) | yes | ok |
| X05 | fresh S Codex | forecast, rung 4 ($692.9–737.6B, central about $715B) | yes, yes | (none) | yes | ok |
| X08 | fresh S Claude | forecast, rung 4 ($708.1B: $715–745B × 97%) | yes, yes; Codex marked two defects | defects: uphold, reject | yes; two defect splits | inconclusive |
| X02 | fresh P-v8 Claude | forecast, rung 2 ($385.9B) | yes, yes | (none) | yes | ok |
| X04 | fresh P-v8 Codex | forecast, rung 2 ($377.7B) | yes, yes | (none) | yes | ok |
| X03 | control: invented 10% cut | forecast | no, no | (none) | no | ok |
| X01 | control: impossible floor | forecast | floor marked by both | (support only) | floor settled | ok |

- **The failure.** X06's writer took the market pace (about 1.48–1.5x) as a floor and management's "more than double" as a
  ceiling, and chose 1.75x, the midpoint.
  - Both adjudicators: the passages state "more than double" as a minimum; the midpoint has no source; the reasons for a miss
    (one customer evaluating, a competitor's own benchmarks, missing volume figures) size or bound no shortfall below $40B. The
    answer shows only that the outcome might fall short.
- **The defect splits on X08.**
  - F15 = 130 ÷ (125–145) gives a range whose top end is 104%. The Codex adjudicator calls that a part above its whole. The Claude
    adjudicator calls it the mechanical end of a range ratio that the format requires.
  - F5, the outside total-capex range, is marked as the market's reference for data-center spending. The Codex adjudicator says this
    implies a 100% share. The Claude adjudicator says F5 is a quoted outside figure, as the reference rule allows, and that the
    deduction is set out separately.
- **The reasons and premises** behind every settled S and E vote were read and recorded (`reasons.json`). X05 and X08's readers read
  the same four companies' AI-infrastructure plan as a plan that can slip, not as a floor, which fits each answer's own outcome.
- **A run incident, disclosed.** The background command running the eight Codex readers was terminated (exit 144) while three
  readers were still running. X04, X05 and X08 had empty outputs, kept in `reader-packets/interrupted/`. Fresh Codex readers were
  run for those three. No reading was discarded after it was seen.

## 2. The E record across the four runs (same case, same passages)

| Run | Codex writer | Claude writer |
|---|---|---|
| third run (D742 request) | 85% realisation, $34B; settled no | 1.85x bracket, $37B; yes in re-read 2, split under D747 |
| targeted test (D745) | 90% realisation, $36B; settled no | 1.8x × 90% share, $32.4B; split, then no under D747 |
| D749 | unresolved, specific gap; settled yes | 2.1x in full, $42B, asserting "already selling at volume"; split |
| D750 | unresolved, specific gap; settled yes | 1.75x bracket midpoint, $35B; settled no |

- **The Codex writer.** The repair (D749, D750) moved it from invented cuts to a justified unresolved, twice.
- **The Claude writer.** It forecasts every time, by a different route each time, and has never been settled supported under the
  current definitions.
- **S** improved but did not fully settle (corrected after council 67):
  - D750's two fresh forecasts earned settled support, with two defect marks on X08 still split.
  - D749's X08 support verdict was split after the correction: one reader accepted $710.4B while treating $730B as a floor.
  - D749's S Codex was settled supported.
- **P-v8** has been supported throughout.

## 3. Not done

Nothing was paid. Nothing was tuned on the 36 stored answers. The request was not changed after the registration.
