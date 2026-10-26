# The theme block (D195): r5 (`poc-v29`) beside r4 (`poc-v26`), one replay of the same window

Ledgers: `poc/data/english-v26-collision-r4-2026-10-26/` (control) and `poc/data/english-v29-theme-r5-2026-10-26/` (arm);
window 2026-02-25..07-23 NVDA only, then 07-24..08-15 every object. Script: `docs/research/2026-10-26-theme-dependencies/theme_block_compare.py`
(full table and the five pairs of reasons in `r5-vs-r4.md`); the three one-off re-sends before the run in `resend-three.txt`.

| | r4 control | r5 arm |
|---|---|---|
| theses (theme theses) | 45 (6) | 44 (8) |
| judgements, asset / theme | 175 / 11 | 287 / 18 |
| asset requests carrying a theme block | 0 | 245 |
| judgements that named at least one theme push | 0 | 194 |
| propagation-only judgements (an asset thesis judged in a round where none of its own inputs changed that day) | 0 | 123 |
| of them, conclusions that said changed | — | 13 (10%) |
| rung moves over the window | 9 | 13 |
| judging cost at `model.PRICES` | $0.32 (186 calls) | $0.52 (307 calls) |
| whole run, every input token at the input rate | $1.33 | $1.59 |
| whole run, cached input at its published rate (10% of the input rate; a quarter of extraction's input is cached, judging's 0–2%) | $1.21 | $1.46 |
| judge calls that ran out of output (`finish_reason: length`) | 0 | 1 |
| extraction gold (D194), full / fail | 4 / 16 | 5 / 15 |

**What it shows.** The block is read and answered: 194 of 245 block-carrying judgements name a theme push (147 toward the
first end, 42 toward the last on the week stage; the two AI-capex theses carry three quarters of them). The signs follow
each thesis's own ladder: Meta's capex thesis (rung 1 = below $120bn) takes the capex themes toward the last end, Intel's
gross margin and AMD's data-center line toward the first; the Taiwan proceedings and a tariff-quota theme are ignored by
most asset theses. Propagation costs what the census said (+121 judgements against the estimate of 141; +$0.20 of judging
against $0.24) and yields a changed conclusion one time in ten, mostly "same rung, new supporting figures". Reasons read
the same or better than r4's on the five asset theses with the same question in both ledgers; where the rung differs
(Intel margin 3 → 2, AWS 3 → 1) the arm's last judgement is two weeks later with more evidence, so the difference is not
the block's alone. The gold difference (4 → 5 full) is extraction sampling (D193), not judging.

**The one failure.** On 2026-08-01 the first judgement of the day, NVDA data-center revenue FY2027 (the largest request,
122k characters, 30.9k input tokens), came back with empty content: the model spent the whole 8,000-token output budget
on reasoning (`finish_reason: length`). The day failed as designed (resumable); re-sent on resume, the same request
answered normally. One call in 307 against none in 186; the per-call request size is unchanged by the block (6.3k against
6.2k input tokens per judge call), so this is the sampler on an oversized thesis, recorded, not handled. The resumed
round had nothing to recover (the failure preceded the first commit of that round), so the ledger-derived queue was
exercised by its unit test only.

**Decision.** `poc-v29` is the replay default (D196). Open: the UI does not show the block or the pushes (its own slice);
the aggregate theme theses still open in near-duplicates (two to three per window after the collision judge) and each
one appears as its own line in every block.
