# G1-a read by hand (changes 1 and 2: c15yc against c8), 2026-11-13

**Result: G1-a does not pass.** On the judged run (`poc/data/clean-step1-gate1-2026-11-13/g1a-rerun/`, 18 sends, all answered, no
network loss), c15yc separates the two years in **5 of 9** sends against the line of 8 of 9; c8 separates in 0 of 9 (within its
≤2). Every c15yc send retains a capex thesis; none opens a third capex thesis or a later year. Under D435 the failed proof stops the
gate and goes to Alex.

| run | c15yc separates | c15yc misses | c8 separates | c8 misses |
|---|---|---|---|---|
| judged re-send | 5 of 9 (d1 s2; d2 s1, s3; d3 s1, s2) | 4, each one year only: 2027 with 2026 as its base (d1 s1, s3; d2 s2), 2026 only (d3 s3) | 0 of 9 | one year only 7, both years in one thesis 2 |
| first run (unexercised: two sends lost to the network; reported, not judged) | 8 of 8 answered | — | 0 of 8 answered | one year only 5, both years in one thesis 3 |
| c14 (D433, the year sentence's first wording, other states) | 7 of 9 | one year chosen as the bet 1; no capex thesis 1 | 0 of 9 | — |

The frozen ruler's seeds hold both years as separate questions (`poc/seeds/nvda-2026-07-01-v2.json`: v4, calendar 2026; v13, calendar
2027), so the misses are the model's errors against the ruler, not the line's.

**What changed and what did not.** The merge is gone: no c15yc send in either run holds both years in one thesis (c8: 5 of 17
answered). What remains is the choice of one year. **The mechanism, from the four misses' stored reasoning** (read by me): each quotes
the year sentence, recognises that it suggests two theses, then declines the second as too much: "Do we open both? That may be
excessive" (d1 s1); "I'll propose one for 2027? Or 2026? Actually maybe I should propose both? That seems excessive … over-generation
for a fool.com opinion piece" (d1 s3); "Would an analyst bet separately on 2026 combined capex? … 2026 is half over … I'll keep it to one
thesis (2027)" (d2 s2); "Proposing two shared_quantity theses feels like overkill … to avoid over-proposing, I'll have ONE thesis for
2026" (d3 s3). The reasons given: the current year's figure is "mostly already determined", the next year's is "just Nvidia's
projection, less firm", and the request's caution against opening too much. The sentence's own condition, "when an analyst would bet
on each", is where that caution enters: it leaves the second year to the model's judgement of importance, and the cautious rules win in
about one send in three.

**Across all sends of the year wording** (c14 and both c15yc runs, on the same article in three stored states): 20 of 26 answered
sends separate; c8, 0 of 26. One article: the mechanism and its rate on that article, not a rate across articles.
