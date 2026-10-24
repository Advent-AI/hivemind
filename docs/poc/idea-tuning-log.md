# Idea route: tuning log

One entry per iteration, in order. Each names the hypothesis, what changed, how it was measured, the numbers, and
whether it stayed. Metrics come from `scripts/idea_probe.py` (49 probes, `poc/eval/idea-probes-2026-10-24.json`),
`scripts/idea_stability.py` (8 ideas × 3 fresh samples) and the archive `poc/data/service/idea-archive.sqlite`
(tokens, seconds, cost at list price). "Mapped" = views on the canvas per idea (direct + driver since v7).
The expected sets behind the probe's flags are my own reading, not gold; Alex's 20 gold ideas are still requested.
Alex, 2026-10-24: "你要 push 自己的思考，把每次做的都记录下来，持续迭代".

| # | Config / prompt | Hypothesis | Change | Mapped median / mean | Tokens in per idea | Cost per idea | Stability (first view, core overlap) | Kept? |
|---|---|---|---|---|---|---|---|---|
| 1 | poc-v3 / idea-v1 | One call over the idea's top-10 is enough to pick the views | first version | 1 / 1.73 | ≈ 2,400 | $0.004–0.010 | – | no: too few views, one error per class (price, invented claims) |
| 2 | poc-v4 / idea-v2, v3 | Decomposition in the prompt raises coverage | two-step prompt, top-20 candidates | 2 / 2.71 | ≈ 5,000 | $0.008–0.014 | – | no: parts were templated restatements |
| 3 | poc-v4 / idea-v4 | A fresh Luna with the MCP tools reads better | agent loop with search / view / evaluate / finish | 2 / 2.43 | 15,038 | $0.022 | 11 of 12 first views, 0.4–0.8 | no: same coverage, 3.6 turns, history re-sent |
| 4 | poc-v5 / idea-v5 | The agent fails because the interface is unclear | catalog in the message, tool descriptions, finish refuses unsearched parts | 2 / 2.39 | 27,048 | $0.037 | – | no: fixed blind finishes (11 → 1) and vague parts (7 → 0), +80% tokens, no more views |
| 5 | poc-v6 / idea-v6 | The service should do the looking up; the model only decomposes and maps | two calls, one search per part by the service, graph neighbours, service evaluates | 5 / 5.73 | 2,704 | $0.012 | 6 of 8, 0.44 | **yes** (D135) |
| 6 | poc-v7 / idea-v7 | Precision and stability come from tiers and code rules | direct / driver / context; service picks the first part's direct view; market-price parts refused; claim only against a direct view; Chinese fields re-asked | 6 / 5.84 (direct 2.3, driver 5.4; context 2.9 off canvas) | ≈ 2,800 | $0.0156 | 7 of 8, 0.53 | yes for the rules; the tiers cost +70% output tokens on call 2 |
| 6a | poc-v7, first cut | (defect found on 3 ideas) the direct rule matched object and year only; "this year" ≠ FY2027 demoted v3 to context and the claim went to v9 | fiscal year covers the calendar year; claim only against a direct view; service pick needs the model to list the view; at most 3 drivers per part | – | – | – | fixed before the run |
| 7 | poc-v8 / idea-v7 | Reasoning is most of the cost and time | reasoning_effort none on both calls | 5 / 5.08 (direct 2.8, driver 4.6) | ≈ 2,800 | $0.0089 | **8 of 8**, 0.58 | **yes**: call 1 3.2 s, call 2 4.4 s; the first view agrees in every sample; direct labels a little looser (a segment view as direct for a total); 2 Chinese slips, both caught by the re-ask |
| 8 | poc-v9 / idea-v7 (none) | The remaining instability is the model's free-text query per part | the service also searches a canonical query (object id, looks_for, period) and interleaves the two candidate lists; the direct pick follows the model's query | 4 / 5.1 (direct 2.9, driver 4.2) | ≈ 2,800 | $0.0085 | 7 of 8, 0.65 (full 0.62) | kept, effect within noise: the hypothesis was half wrong (below) |
| 9 | code only | Five of fourteen seconds are not the model | the parts' queries are embedded in one round trip (`search.warm_queries`) | – | – | – | – | **yes**: serial wall median 14.1 → 10.9 s on arm B, $0 |
| 10 | poc-v11 / idea-v8 | 71% of call 2's output is text nobody reads; 45% of its input repeats | no per-part reason (the page reads only `summary`), each candidate brief once, a two-sentence summary | 5 / 5.78 (direct 2.9, driver 4.6; context 5.1 off canvas) | call 2: 2,149 → 1,588 in, 352 → 247 out | $0.0070 (8 fresh, serial); call 2 $0.0062 → $0.0045 | 7 of 8, 0.55 (full 0.57) | serial wall median 8.6 s (from 10.9), call 2 4.7 → 3.6 s; canvas overlap with arm C on the same decompositions 0.67 (within sampling noise), no-view parts 16 → 13, but stability 0.65 → 0.55 and context labels doubled: arm E isolates which half of the diet did it |
| 13 | poc-v12 / idea-v9 | The id table of the lean payload, not the missing reason, costs the stability | no per-part reason, two-sentence summary, full per-part briefs as in idea-v7 | 5 / 5.35 (direct 2.7, driver 5.1; context 3.2) | call 2: 2,121 in, 232 out | call 2 $0.0050; $0.0080 per idea (measured beside the probe run, not serial) | 7 of 8, 0.50 (full 0.50) | **no**, and the hypothesis was wrong: with the full briefs and no reason the stability fell further (C 0.65 → D 0.55 → E 0.50), so it is the per-part reason that steadies the mapping (written after each part's views, before the next part's), not the payload shape; no-view parts 16 → 12, nothing mapped 1 → 0 |
| 12 | code only | Four of 31 service picks overrode a right model label (3 of 13 claims judged against the wrong view) | the pick is chosen among the model's direct views, search order, year check; no object test | picks 31 → 37 (C), 32 → 37 (D) | – | – | first view C 7 → 8 of 8, D 6 → 7 of 8 | **yes** ($0 replay): the four cases now take v2, v48, v94, v28; three claim verdicts changed (Rubin $50B: holds → not yet on the Vera view; TSMC capex: conditions → holds on the capex view; Meta capex: holds → not yet on the capex view); tie-break by the model's own order instead of the search's: the same picks on 44 of 48 samples, same agreement, kept the search |
| 14 | code only (poc-v9) | The candidate pool, not the labels, carries the variance: across 3 fresh samples the parts' objects agree 0.72, the pools 0.62, the canvas 0.65 | a part's candidates are its object's open views ranked by the idea's own text (deterministic given idea and object), then the searches' finds; the pick's tie-break is that order | 5 / 5.3 | – | $0.0095 | 7 of 8, 0.67 (fully fresh samples) | **no, reverted**: stability moved 0.65 → 0.67 only, and on the sealed gold the direct view was right in 15 of 19 against 17 of 19 before (the Rubin idea lost v48: the idea text's embedding does not reach the Vera view the model's query found), traps 3 against 2. The ranking by the idea text throws away the model's finds; the pool stays as the archives `stability-pool/` and the log `idea-probe-13` |
| 15 | poc-v13 / idea-v10 | The driver label is the noisiest decision (same object, same candidates: direct agrees 0.90, drivers 0.50); a written clause per driver should steady it, as the per-part reason did (E → C) | every listed view carries a clause; a driver is a view whose outcome moves the part's number and the clause says how, a view without one is not a driver; the NVIDIA example replaced by the rule; decompose section byte-identical (call 1 cached) | 49: as C | call 2: 2,173 in, 485 out (C 359), 5.5 s (C 4.7) | call 2 $0.0076 (C $0.0063) | design set 7 of 8, 0.51 (C 0.65); held-out 8 of 8, 0.62 (C 0.68) | **no, on both sets**: the clause made the model more selective and less consistent (drivers listed differ more between samples); gold direct 16 against 17, traps 3 against 2, driver recall 0.50 against 0.62, noise 17% against 23%. The neutral example sentence is kept for the next prompt arm |
| 11 | poc-v10 / idea-v7 + seed | The provider accepts `seed`; the same idea should then give the same card | `seed: 7` on both idea calls | – | – | $0.0094 | 1 idea × 3: three different decompositions, core overlap 0.32 | **no**: accepted but not deterministic on this model; the seed plumbing and the config were removed, the three archives stay as the record |

## Iteration 8 read closely ($0, on stored samples)

- Call 1 was served from arm B's archive (same request), so the 49-probe comparison B → C changes only the candidate
  lists. Mapped fell 5 → 4 (median) mostly because call 2 re-labelled the same views: v2/v4 "driver" in B became
  "context" in C on the tariff idea (then nothing mapped, which is the honest answer: no gaming view exists), the four
  ai-capex views on the TPU idea went "direct" → "context". That is call 2's sampling noise on the driver/context
  line, not the candidates; a 49-idea arm without a fresh control cannot separate the two (§6), the 8 × 3 runs can.
- On the 8 × 3 samples: the first part's object agrees 8 of 8 in both arms, its wording 1–2 of 8, the number of parts
  5–6 of 8. The top search hit agrees 8 of 8 under the model's own query and only 6 of 8 under the canonical one, so
  the hypothesis was half wrong: the model's query is the steadier one for the top hit (the pick now follows it),
  the canonical query only adds the object's own views to the candidates. Core overlap: every listed view 0.58 →
  0.62, as built 0.58 → 0.65 (and 0.68 on arm B's decompositions with the merged candidates). The remaining
  variance is call 1 (how many parts, which secondary objects) and call 2's tier labels, not the search.
- Mistake, recorded: the replay of arm B's stability archives with the merged candidates changed call 2's request,
  so it was not a $0 replay: 24 fresh calls, ≈ $0.18, now stored in those archives beside the originals. A replay
  is free only when every request is byte-identical; check the archive's row count after any replay that follows a
  code change to a payload.

## Where the time goes (serial run, 2026-10-24 23:10, per idea)

| | calls (archive) | wall | gap |
|---|---|---|---|
| arm B, 7 fresh ideas | 7.8–10.7 s | 12.6–16.8 s | 4.7–6.2 s |

The gap is the embeddings: a never-seen query costs one round trip (0.6–1.9 s measured), an idea made seven in a row
(its own, then two per part). Iteration 9 embeds the parts' queries in one call. The two model calls themselves run
at 48–88 output tokens per second with a floor of several seconds each (an 11-token answer took 6–10 s at 23:30),
so two serial calls cannot meet the 6 s target on this network; ≈ 8 s is the design's floor here.

## What call 2 spends its tokens on (arm B, 49 ideas)

Output: 597 characters of per-part reasons, 343 of summary, 393 of view lists per idea; the page reads only the
summary (`poc/ui/src/idea/idea.js`), the reasons fed the probe log. Input: 28 candidate briefs per message, 15
distinct, 45% of the brief text a repeat. Iteration 10 cuts both.

## Serial timing, nothing else running (8 fresh ideas each, end to end in process with bundles)

| | control v6 | A v7 | B v8 |
|---|---|---|---|
| seconds per idea, median | 20.4 | 20.8 | 14.1 |
| cost per idea, mean | $0.0130 | $0.0146 | $0.0087 |
| arm B after iteration 9 (batched embeddings), 8 fresh ideas | | | 10.9 s, $0.0098 |
| iteration 10 (lean contract), 8 fresh ideas | | | 8.6 s, $0.0070 |

The earlier 12 s figure was the sum of median call times; the end-to-end median on fresh calls at this hour is
higher. Reasoning off saves 30% of the time and 33% of the cost; the tiers alone add time (longer call 2 answers).

## Measured baselines for the tuning plan (2026-10-24, night)

Per new idea on the two-call route (control, iteration 5): ≈ 12 s (call 1 5.8 s, call 2 5.0 s, service 1.5 s of
which five searches at 0.32 s, bundles 0.2 s, 2.7 MB answer); $0.012 (884 output tokens are 73% of it); the direct
view agrees in 11 of 12 fresh samples, the full mapped set overlaps 0.4–0.8.

Targets set before iterating: time ≤ 6 s, cost ≤ $0.005, first view 8 of 8, core overlap ≥ 0.8, zero price
claims, zero uncaught language slips, zero ideas with nothing mapped.

## Service-side changes measured without a model run

- The sequence-to-day map was never cached (sqlite3 connections cannot carry attributes): one view read 0.47 s →
  0.07 s; an idea 4–5 s → 0.4–0.7 s on replay.
- Search ranked full view records (92 × evidence counts): `service.summaries` ranks light records; one search 0.32 s
  → 0.057 s. The service's own share of a live idea (everything but the two model calls) is now 0.75 s for the card
  and 0.95 s with bundles, with seven searches per idea (the idea's own, two per part); the rest of the 14 s is the model.
- `POST /ideas` with `bundles: false` answers the card alone (9 KB, 0.53 s on replay) and the page fetches
  `/thesis-bundles` after drawing the idea card (2.06 MB, 0.22 s); the card with bundles was 0.72 s and 2.06 MB.

## What the deep reads found, by iteration

- Iteration 5: coverage doubled; "could reflect the outcome" views mapped to parts the library does not cover
  (TPU, Trainium, gaming, Apple); a share price read as revenue and evaluated.
- Iteration 6 (first cut, 3 ideas): the service's direct rule promoted the top hit on object and year alone (gross
  margin as the direct view of a market-share part); fixed by requiring the model to have listed the view.
- Iteration 6 (49): drivers remained generous (six per part on a one-line idea) → capped at three per part, the
  rest to context; the market guard refused the share-price part and its claim; the English re-ask caught one slip.
- Iteration 7: with reasoning off the first part's search sometimes ranks a segment view above the total (v9 above
  v2 for "NVIDIA total revenue"), and the service's pick follows the search; the rule inherits search noise.

## Iteration 12: the service's direct pick overrode the model's right answer (found 2026-10-24 23:50)

Census on arm B's 49 ideas: the service picked the first part's direct view in 31; in 10 of those the model had
called more than one view direct. Reading the ten pairs: in four the pick was wrong and the model was right in
every arm (v7, v8, v9, v11): TSMC capex → the service took TSMC revenue (v69, object TSM) over TSMC capex (v94,
object supply-chain-shift, labelled direct by the model); Meta capex → total expenses (v27) over capex (v28);
NVIDIA total revenue → the Compute & Networking segment (v9) over total revenue (v2); Rubin revenue → total revenue
(v2) over Vera product revenue (v48). Three of the four carried a dollar claim, so 3 of 13 claim verdicts were
evaluated against the wrong view. Mechanism: the rule took the top hit of the part's search when object and year
matched and the model had listed the view anywhere, so a view the model called "context" or "driver" became the
direct view and the claim's target. Fix: the pick is made among the views the model called direct, in the search's
order, the first whose text carries the part's year; no object test (v94's object is a theme). Replayed at $0.

## Iteration 10 read closely

The three claims the pick fix moved now read right on the lean contract (Rubin $50B against the Vera product view:
not yet; TSMC capex against the capex view: holds; Meta capex against the capex view, not total expenses: not yet),
and the two-sentence summaries name what no view covers. Two costs of the id table showed: ids assigned to a part
they were not offered for rose from 0–2 per 49 ideas (arms B, C) to 6 (the model sees one table and spreads it
across parts), and context labels doubled (3.0 → 5.1 per idea); both are the kind of noise the stability number
measures. The summary stayed ≈ 360 characters: the sentences got longer, the output saving came from the reasons.

## Where it stands (2026-10-25, 00:05)

| | full contract (C: idea-v7, reasoning none) | lean (D: idea-v8) | no reason, full briefs (E: idea-v9) |
|---|---|---|---|
| seconds per idea, serial median | 10.9 | 8.6 | ≈ 9–10 (not timed alone) |
| cost per idea | $0.0098 | $0.0070 | $0.0080 |
| first view agrees (8 ideas × 3) | 8 of 8 | 7 of 8 | 7 of 8 |
| canvas overlap, median | 0.65 | 0.55 | 0.50 |
| views on the canvas per idea (49) | 4 / 5.0 | 5 / 5.8 | 5 / 5.4 |
| claims judged against a wrong view | 0 | 0 | 0 |

The three contracts share every code rule; they differ only in what call 2 writes. The per-part reason costs
≈ 2 s and ≈ $0.003 per idea and buys ≈ 0.1 of canvas stability on this instrument (16 ideas × 3 samples with it:
0.58 and 0.65; 16 without: 0.55 and 0.50). My lean: run the full contract (poc-v9) until a measured arm beats it;
the API and the two scripts now default to it. The next arm, not run tonight: a reason capped at twelve words
(keeps the per-part attention, cuts most of the 597 characters), then six candidates per part instead of eight.
Against the targets: time 20.4 → 10.9 s (target 6: below the floor of two serial calls on this network), cost
$0.013 → $0.0098 (target $0.005: the next two arms are the way there), first view 6 → 8 of 8 (met), canvas overlap
0.44 → 0.65 (target 0.8: the variance left is call 1's decomposition), price claims 1 → 0 (met), claims against a
wrong view 3 → 0 (met), Chinese fields 0 uncaught (met), nothing mapped only where no view exists (met).

## Generality check (Alex, 2026-10-25: the prompt must serve other companies and macro events, not NVIDIA)

Tonight's prompt changes touched only the two idea-reading prompts (decompose, map), not extraction (frozen, D37).
The two prompts name one company in one example sentence ("a fiscal year that covers the period counts: NVIDIA's
FY2027 is calendar 2026"); the code's rules name none (object list and aliases come from `poc/universe.json`; the
fiscal rule is "a calendar year matches its own fiscal year and the next", which holds for January, June and
September year ends). Of the 49 probes, 21 are not about NVIDIA (TSMC, Meta, Microsoft, AMD, Intel, Micron, Apple,
CoreWeave, SpaceX, Anthropic, SK Group, and the themes ai-capex, semiconductor-cycle, tariffs, export controls): all
21 mapped at least one view, 16 got a direct pick. Limit: the sealed library is NVIDIA-heavy (one company's documents
plus six themes), so macro-only ideas are tested thinly. The example sentence becomes neutral in the next prompt arm
(with the twelve-word reason), measured once.

## The sealed gold (2026-10-25, D146)

Alex: "3.的标准就是hedge fund analyst /investor 会看的观点，你来进入角色做golden 然后封存". Twenty ideas in
`poc/eval/gold/idea-gold-2026-10-25.json` (digest in `SHA256SUMS`, never edited), each with the views an analyst
accepts as direct, the one a stated amount is judged against, the drivers wanted beside it, acceptable neighbours
and traps; two ideas the library does not cover. `scripts/idea_gold.py` scores a configuration and refuses an
unsealed file. Model-authored gold (§7): it is my analyst reading, not Alex's hand.

| gold score | C (kept: idea-v7, none) | D lean | E no reason | F object pools |
|---|---|---|---|---|
| direct view right (19 gold ideas among the 49 probes) | 17 | 16 | 16 | 15 |
| a trap shown as direct | 2 | 2 | 3 | 3 |
| driver recall, median | 0.62 | 0.67 | 0.67 | 0.67 |
| canvas noise (views outside direct, drivers, acceptable) | 23% | 25% | 24% | 28% |
| claims judged against the gold's view | 19/19 | 19/19 | 19/19 | 18/19 |

The kept configuration on all twenty (one new idea, $0.008): direct right 18 of 20, traps 2 of 20, driver recall
median 0.65, canvas noise 22% (26 of 118 views), claims 20 of 20. The two misses are the next quality leads, each
with a census of one: (15) "AMD's MI450 will take data center share": the model called the Anthropic 1GW deployment
event direct and left AMD's FY2027 data-center growth (v52) out, an event standing in for a quantity; (18) "Section
232 tariffs on semiconductors": call 1 made the first part an ai-capex part, so a capex view became "direct" for a
thesis the library does not cover. Driver recall at 0.65 and noise at 22% say the driver tier is the loose part:
the canvas carries views an analyst would not ask for (NVIDIA segment views on a CoreWeave idea) and misses some it
would (Meta revenue beside Meta capex).

## Where the instability enters, measured before iteration 15 ($0, 16 idea-sets × 3 fresh samples)

| step | overlap across samples |
|---|---|
| the set of objects call 1 chooses | 0.75 |
| the candidates for the same object (canonical + model query, top 8) | 0.78 (model query alone 0.60, canonical alone 0.78, unions of 12–16 no better) |
| call 2's choice with object and candidates held fixed: direct set | 0.90 |
| … driver set | 0.50 |
| … direct + driver | 0.78 (the canvas moves 25% per part on call 2 alone) |
| the canvas | 0.65 |

Three sources of about equal size: which secondary objects call 1 names, which candidates they get, and which of
them call 2 calls a driver. A fourth part exists in 3 of 49 ideas (not a source). Rules applied after call 2 do not
help: "driver only if the ledger's graph links it to the direct view" lifts the canvas overlap to 0.71 but halves the
gold's driver recall (0.65 → 0.33); "same object" changes nothing. Asking call 2 twice and keeping the drivers both
name (simulated on the samples) gives 0.65 → 0.73 at recall 0.62 → 0.55 and a second call's price; kept in reserve.
The product already answers the same sentence the same way on the same day: the archive replays it (checked:
identical card, cached). The 0.65 is what a re-ask with the cache off, a paraphrase, or a changed library would show.

Against overfitting: the levers were designed on the 8 stability ideas and the 20 gold; a held-out set of 8 ideas
on other objects (`poc/eval/idea-heldout-2026-10-25.json`: AWS, Microsoft margin, Super Micro, AMD revenue, Intel
revenue, Reality Labs, CoreWeave ARR, 亚马逊电力) is measured once for the kept configuration and once for the arm;
an arm is accepted only when it moves both sets.

## Stability: where it stands after iterations 8, 11, 14 and 15 (2026-10-25, 01:00)

| | design set (8 × 3) | held-out set (8 × 3) | gold driver recall | gold noise |
|---|---|---|---|---|
| kept configuration (C) | 0.65, first view 8 of 8 | 0.68, first view 8 of 8 | 0.65 | 22% |
| drivers per part ≤ 2 instead of 3 (a structural cap, $0, replayed) | 0.67 | 0.76 | 0.56 | 18% |
| drivers per part ≤ 1 | 0.61 | 0.74 | 0.45 | 14% |
| direct views only | 0.62 | 0.85 | 0.00 | 11% |
| two mapping calls, drivers both name (simulated) | 0.73 | – | 0.55 | 11% |

What moved it: the canonical second query (0.58 → 0.65), the pick that follows the model's direct label (first
view 7 → 8 of 8). What did not: a provider seed, candidates ranked by the idea text, a clause per driver, graph- or
object-bound drivers after the fact. The three sources are of equal size and two of them are the model's own
sampling (which secondary objects it names, which of the same candidates it calls a driver); with no temperature
control on this model the remaining levers all trade recall for stability (the cap) or a second call for it (the
intersection). The held-out ideas, single-company questions, sit at 0.68 against the design set's 0.65, so nothing
tonight was fitted to the design set. The same sentence on the same day is answered identically by the archive;
the 0.65–0.68 is what a paraphrase, a re-ask with the cache off or a changed library shows.

My lean: leave the canvas rule as it is (recall is what the analyst's gold measures); offer the cap of two drivers
as a switch only if Alex prefers a steadier canvas to a fuller one; keep the two-call intersection in reserve for a
"stable mode" that costs a second call. The next stability gain is upstream of this module: a library with one
view per quantity (the eight noise views leave with the next run) and dependency links between the company views
and the theme views, so that the drivers can come from the graph instead of the model.

## Open levers (not yet tried)

- 26 of 49 ideas have two or more parts on the same object (35 of 143 parts repeat one): the service could merge
  them before searching, which steadies the number of parts and shortens call 2; it changes the card's rows.
- Six candidates per part and three idea rows instead of eight and five: −25% of call 2's input.
- Prompt-prefix caching on the provider's side (the two system prompts never change): discount unverified.
