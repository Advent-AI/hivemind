# The six contested last answers of the fortnight, traced by Claude before any reader (2026-11-16, $0)

Run `poc/data/clean-carried-run-2026-11-16/c1/judge/draw-c1/`; each last request and answer saved as `last-<view>.txt`. Contest
reasons from `carried-run/codex|claude-answers.jsonl` and `control-confirmation.jsonl`. Causes may overlap.

| Question | Answer | Contest | What I read | Causes (overlapping) | Would the rung move? |
|---|---|---|---|---|---|
| v1 credit support and guarantees disclosed in the FY2027 10-K | rung 5, ≥ $50bn, from the $108.5bn guarantee cap | Codex: a cap is not a floor; Claude: supported | Every guarantee statement found is in the request; a 10-K discloses guarantees as the maximum potential payment, so the cap is what the filing would show; the question never says whether "amount" is the maximum or the expected payment | the question leaves its measure undefined; reader threshold | only under the other reading of "amount" |
| v5 big-five data-center capex 2026 | rung 3 ($750–850bn), "about $820bn" | Codex: a possible double count of Amazon's raise | $800bn and $820bn are both in rung 3, and so is $800bn with no raise | the judge's arithmetic in its implied outcome | no |
| v10 U.S. gigawatts added in 2026 | rung 2 (10–15 GW) | the separate reader: a range spanning two rungs placed by unquantified constraints | 11 kept gigawatt statements not shown are projects outside the U.S., for 2027, or credit support; one family named revenue per gigawatt as a confidence cross-check; nothing sizes U.S. 2026 additions | evidence insufficient to decide; reader threshold | not by anything found |
| v11 DRAM contract prices 2026 vs 2025 | rung 5 (≥ 30%) | Codex insufficient; separate reader: no price series | no sentence of the fortnight's 476 articles gives a contract price; the 8 memory-price statements not shown are qualitative ("rose more than expected") | the feed never carries the series the question names; the judge forecasts a band from qualitative evidence | not by anything found |
| v12 residual-value guarantee finalised by 2028-04-03 | rung 1, Yes | the separate reader: unsure | three statements on the matter were kept before the question opened (seq 332, 391; opened 398) and filed under v1: NVIDIA "may provide residual-value support for up to 25%", "no more than 25%", and "previously provided a residual-value guarantee" for the SB Energy project (S&P, Moody's); the later-linking step skips groups filed under another question (`clean-arch/step3/library.py`, the D508 correction) | a fact filed elsewhere never reconsidered; forecast uncertainty | no in my read (a precedent firms "Yes"); untested |
| v13 Nvidia CPO switches ≥ 100,000 in 2027 | rung 3, Still open | the separate reader: the only estimate reaches the threshold | the event shape makes "not reached, not abandoned" Still open; Nvidia publishes no unit counts (gate 1's W, split); the only figure is an analyst's "could reach" | the answer-choice shape (a threshold figure written as an event); data never published; reader threshold | the shape decides it, not evidence |

**What I take from it:** no one mechanism holds the six. One delivery fault (v12), of a mechanism already known and of
confidence-level effect in my read; two answers with nothing in the corpus that sizes them (v10, v11); two set by the question's
form (v1, v13); one contest with no effect on the rung (v5). The readers' contests mostly differ on how much evidence a forecast
needs, not on what the evidence says.
