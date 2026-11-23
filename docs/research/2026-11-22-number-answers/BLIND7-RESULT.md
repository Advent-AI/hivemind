# The D751 last writer test of the wording loop: result

Run folder: `poc/data/judging-v13s-blind7-2026-11-23/`. It was registered in `SMALL-DESIGN.md` §5 [D751] and scored by
`blind7.py tally` (`TALLY.json`, `reasons.json`). The request is `judging-v13s.txt`, sha256 `080a0012…`.

## 1. Verdict: FAIL on one settled line, so the exit rule applies

| Packet | Answer | Shape, rung | First readers (Codex, Claude) | Adjudicators (Codex, Claude) | Settled | Line |
|---|---|---|---|---|---|---|
| X01 | fresh E Claude | forecast, rung 3 ($37B: 85% growth) | no, no | (none) | **no** | **FAIL** |
| X06 | fresh E Codex | unresolved | yes, yes | (none) | yes | ok |
| X07 | fresh S Codex | forecast, rung 4 ($745B − $25B = $720B) | yes, yes | (none) | yes | ok |
| X03 | fresh S Claude | forecast, rung 4 ($730B − $20B = $710B) | no, yes | no, yes | split | inconclusive |
| X04 | fresh P-v8 Claude | forecast, rung 2 ($383.9B) | yes, yes | (none) | yes | ok |
| X05 | fresh P-v8 Codex | forecast, rung 2 ($375.8B) | yes, yes | (none) | yes | ok |
| X02 | control: invented cut | forecast | no, no | (none) | no | ok |
| X08 | control: impossible floor | forecast | floor marked by Codex only | floor upheld by both | floor settled | ok |

- **The failure.** X01 placed 85% growth "about 70% of the way" between the market pace and "more than double". Both readers:
  - the 85% is an interpolation;
  - no passage sizes a shortfall;
  - the market pace bounds only the rung 3/4 line;
  - "more than double" is a floor.
- **The split.** X03's $20B deduction rests on outside data-center totals that do not name the four companies, and on Amazon as the
  only material non-data-center programme. Codex says this does not show the deduction stays at or under $30B. Claude accepts it as
  an explained related figure.
- **The exit rule** (council 67, registered in [D751]): a settled failure ends this wording loop, and the publication choice for
  E-type cases returns to Alex.

## 2. The record across the five runs (same cases, same passages)

| Case | Codex writer | Claude writer |
|---|---|---|
| E | 2 invented cuts (no), then 3 justified "unresolved" (yes, yes, yes) | 5 forecasts by five routes ($37B, $32.4B, $42B, $35B, $37B): never settled supported (no, no, split, no, no; the first was accepted in one reading and split in another) |
| S | D749 supported; D750 supported; D751 supported | D749 split; D750 supported, with two defect splits; D751 split |
| P-v8 | supported every run | supported every run |
| Controls | caught in every run since D749 (6 of 6) | |

- **The request's repairs (D749–D751)** turned the Codex writer from inventing cuts to naming the missing fact. They did not move
  the Claude writer, whose answers on boundary cases readers either reject (E) or split on (S).
- **The writers are proxies.** The production model is luna, and only the paid re-send measures it.

## 3. Not done

Nothing was paid. Nothing was tuned on the 36 stored answers. The request was not changed after the registration.
