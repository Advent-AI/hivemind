# Blind reader: what sizes each research answer's amount? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/self-report/packet-source-check-<n>.json`.
Open no other file. Do not edit files or run model calls.

A research system follows one company (NVIDIA). Each case is one judgement of a question that asks for an amount: `request` is
what the judge was shown (the question, its answer choices as bands, and every statement shown, with its source and quote);
`answer` is the band (`rung`) it chose, its reference, reasons and implied outcome. Judge only against what the request shows.

For each case give:
- `start_amount`: the evidence id(s) and amount the answer's estimate starts from, or `none`.
- `bears`: how that amount bears on the quantity and period asked: `direct` (a stated figure or stated forecast of the same measure and period), `comparable`
  (another party, measure or period that you accept as a basis for this one), `weak` (the answer treats it as comparable but you
  do not accept it as a basis), `none_shown` (no amount is the start), `cannot_tell`.
- `supports_band`: do that starting point and any calculation from shown figures support this band? `yes` | `no` | `cannot_tell`.
- `step_decides`: does a step the evidence does not state (a scaling, a discount, a growth rate, a share) decide which band is
  chosen? `yes` | `no` | `cannot_tell`.
- `step`: if `step_decides` is `yes`, the step and its effect on the band, at most 20 words; else empty.
- `accept`: would you accept the chosen band as supported by what is shown? `yes` | `no` | `too_little`.
- `why`: at most 30 words, naming the evidence ids.

Return, as your final message and nothing else, one JSON object per line, one line per case:
`{"case": "K..", "start_amount": "...", "bears": "...", "supports_band": "...", "step_decides": "...", "step": "...", "accept": "...", "why": "..."}`
