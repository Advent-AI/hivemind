> Historical source retained during D163. Current contract: docs/poc/idea-card.md.

# The idea card: a user's thesis read against the library (2026-10-24)

Alex, 2026-10-24: "你用 docker 起一个 mcp / api service，然后我们的 FE 就是一个调用 luna 然后去访问这个 endpoint 来做出我们
现在的 FE … 我们需要的返回其实是这些 thesis 的各种信息可以 overlay 在 FE 上面 … 还有 user thesis 要能够变成一个 idea card".

## What happens, in one picture

```
user types an idea ──▶ FE ──POST /ideas──▶ service: search (D76, D91) ──▶ luna reads the top-k and chooses (D76)
                                                   │                           │
                                                   │                           └─ a number in the idea → evaluate (code)
                                                   ▼
                        idea card ◀── {idea, reading: {summary, chosen[{view_id, why}], evaluation}, views: [bundles], days}
```

The model's key lives in the service (the credentials file mounted into the container), never in the browser, so the
"FE calls luna" step runs inside the service as one route. Hivemind still stores no idea and knows no user (D76): the
card is built per request and returned whole; the FE owns it from there.

## The one model call

Code decides everything it can (AGENTS §6): the search, the candidate set, the evaluation, the bundles. Luna decides
what only reading can decide: which of the top-k views bear on the idea, why (one line each, English), what the
library's current judgements say about the idea (three sentences, English), and, when the idea states a number
about a quantity one chosen ladder measures, which view, comparator and USD value to evaluate. Strict JSON schema;
an answer naming a view outside the candidates is dropped and the drop is reported in the card. No view found
(`search` null) → no model call: the card says there is no recorded view. Prompt: `prompts/idea-v1.txt`; setting
`idea` in `poc/config/poc-v9.json` (gpt-6-luna, reasoning none; the first version ran poc-v3). Every call is archived (`poc/data/service/idea-archive.sqlite`):
the same idea on the same day and library replays for $0.

## State × event (one request; nothing persists between requests)

| Event | What the card holds |
|---|---|
| search finds views, luna chooses some | `reading` with chosen ≥ 1, their bundles, `evaluation` when a claim was named |
| search finds views, luna chooses none | `reading.chosen = []`, `views = []`, summary says so; `no_recorded_view` false |
| search is null (D91) | `reading = null`, `no_recorded_view = true`, no model call, cost 0 |
| luna names a view outside the candidates | that id is dropped into `reading.dropped`; the rest stands |
| luna's claim names a view not chosen or an unknown comparator | `evaluation = null`, `reading.dropped` says why |
| the ladder of the claimed view is not money | `evaluation.evaluable = false` with the reason (service rule) |
| model refuses / schema error / transport error | HTTP 502 with the error class; nothing cached |
| `as_of` given | search, candidates, state, bundles and evaluation all as of that day; luna sees that day |
| same idea again | archive hit: identical card, `cost.cached = true` |
| two requests at once | each request opens its own connections (threaded server); the archive is SQLite with short writes |

## Value × reader

| Value | Written by | Read by |
|---|---|---|
| `POST /ideas` body `{text, as_of?, k?}` | FE | the service |
| `idea {text, as_of}` | service | FE card header |
| `reading {summary, chosen[{view_id, why}], claim, dropped[]}` | luna, checked by code | FE: the lines under the idea card |
| `evaluation` (the service's `evaluate` answer) | code | FE: holds / not_yet / borderline on the card |
| `views[]` bundles (the shape `poc/mock/data.json` already uses: view_id, object, kind, looks_at, question, due_day, year, created_seq, created_day, created_from, rungs, open, switches, judgements, evidence, dependencies, dependants) | `hivemind.bundle` (one shaping for the mock file and the live route) | the FE's existing adapter, unchanged |
| `days[]` | service | FE time axis |
| `cost {usd, input_tokens, output_tokens, seconds, cached}` | `model.call` | FE footer, the measurement |
| archive rows | `model.Archive` | replays; `scripts/preflight.py` style audits |

## New path × old checks

- `search` null and lexical mode (D91, Codex pass 2): the route inherits them; null → no model call (tested).
- `evaluate` partition rule: a claim on a non-money ladder is `evaluable: false`, never guessed (service tests).
- Credentials: read by `model._key` from the mounted file; never in the image, compose file, logs or answers.
- The threaded server: every request opens its own SQLite connections (Codex pass 1 finding 1 stays fixed).
- The prompt is read as the model reads it: idea, day, candidates with ladder and current state; nothing the answer
  does not need (no evidence text: the FE fetches evidence by code).

## Prior decisions

D76 (the caller chooses; Hivemind stores no theses), D78 (the FE says Idea for the input and Thesis for a stored
question), D91 (null = no recorded view), D24/D28 (data paths from what a thesis needs), D12/D13 (no clock: `as_of`).

## Fronts in Docker

`Dockerfile` + `docker-compose.yml`: two services from one image, `api` (HTTP, host port 127.0.0.1:8788) and `mcp`
(streamable HTTP, host port 127.0.0.1:8789). Mounted: the sealed ledger read-only, `poc/data/service/` (index,
idea archive) read-write, the items database read-only (for source titles), the credentials file read-only.

## Measured before the FE is wired (2026-10-24, `scripts/idea_eval.py`, archive `poc/data/service/idea-archive.sqlite`)

Twenty ideas (the four examples, the sixteen day-0 sentences) through the route once, gpt-6-luna at reasoning effort
low, prompt 5,177 characters for ten candidates:

| | |
|---|---|
| model calls | 19 (one idea, "黄仁勋是个天才", was null: no view names anything in it, no call) |
| cost | $0.099 in all; $0.0035–0.0102 per idea, median $0.0053 |
| time | 63 s of model time; 1.5–6.7 s per idea, median 3.4 s |
| the $300B example | chose v3 alone, claim v3 ≥ 300e9, verdict holds (claim and judged position both 2); the summary notes "this year" is not FY2027 |
| the capex bubble | eight capex views, led by v20 (judged below $600B) against v1 (judged ≥ $750B): "mixed" |
| Rubin slipping | v7 (judged position 1, mass production in H2 2026, contrary to the idea) and v48 |
| the 75% margin | v4, judged position 3 (73–75%), with the note that no view covers sustaining it |
| nonsense that names NVDA (logo, a dream, a split) | chosen = [] with a one-sentence "no view covers this" |
| day-0 lead among the chosen | 4 of 10; the six misses are sentences the day-0 mapper had put on v3 when only ten views existed (CUDA moat, TPU share, CoWoS, a 2027 capex slowdown, Blackwell orders, chip exports), where luna chose v9, v7, v2 or the 2027 capex views instead; a lead, not gold |

Nothing was changed after this run (one run, no fix-run loop); the archive replays every card for $0.

## Docker, as it stands

Images build (`hivemind-api` 203 MB, standard library only; `hivemind-mcp` 290 MB from local wheels) and both
containers run: GET routes answer, an archived idea replays through the container for $0, MCP over HTTP lists the
eight tools and searches. A fresh idea from inside a container does not return: the machine's VPN (Clash Mi, TUN mode,
default route `utun4`) resolves `api.openai.com` to a tunnel address the Docker VM cannot route to (`No route to
host` even with `--network host`, so Docker Desktop's host networking is off). The service therefore runs on the host
until Alex enables host networking in Docker Desktop or opens a Clash HTTP port with LAN access; the compose file
needs one line either way. An idea request now waits at most 60 s per attempt for the model (three attempts), then
answers 502.

## UI integration

The UI lives in `poc/ui` (D130, D138). `fromIdeaResponse` validates this route's view bundles against
the versioned `thesis-ui/1` contract; `graphOf` preserves the direct mappings and each related entry's `via`.
The card header is shared with Thesis; the removed decomposition rows remain available only in the response.
The same bundles can be fetched without a model call through `thesis_bundles` in MCP or `GET /thesis-bundles`
in HTTP. The earlier local matcher has been removed. Details: `poc/ui/README.md` and D138.

## Not in this slice

The sealed ledger's original text remains as stored. D133 governs new English output; this UI change does not
translate or rebuild data. The live Idea flow is wired as described below.

## FE wiring

The FE is wired (2026-10-24 evening, after Codex's Thesis UI, D130): `poc/ui/src/idea/idea.js` posts the
sentence to `/ideas`, the answer goes through Codex's `fromIdeaResponse` into the `thesis-ui/1` contract, the
chosen theses are now peer roots (D138), with related cards attached through `related[].via`; the Idea card shows the sentence, the verdict on the
number (claim and judged position in the cards' own scores) and the reading; null → "No recorded view on anything
in this idea"; an empty choice → the reading alone; a failed call → the status and message. One request in flight
at a time. Verified in a real browser against the running service: the $300B example (Holds, v3 leads, v9
supports), the house idea (null), no console errors; 14 node tests, lint and format clean, page 166 KB JS.

Deep test of the whole path in the browser against the running service (2026-10-24, late evening), each case read
from the page, not only from the API: the $300B example (Holds, v3 leads, v9 supports; claim and judged position in
the cards' scores); the Chinese "3500 亿美元" idea (Not yet, claim at +2, judged +1, three theses); the capex bubble
(eight theses fanned out and fitted to the viewport); "NVDA 的 logo 比 AMD 好看" (No thesis, the reading shown whole);
"asdfgh qwerty" (No thesis, no recorded view); Vera Rubin (one yes/no thesis, Yes); the service stopped (Error:
cannot reach the service at the address); the detail panel on a live thesis (Overview, Evidence with sources and
tiers, History with the score chart); the time axis (Full, Last 30 days) and the replay over the loaded days. Found
and fixed on the way: ladder scores printed "++1" (the shared score renderer is used now); the reading was cut to one
line in three states (it wraps, up to five lines); and the service took 4–5 s per idea because the sequence-to-day
map was never cached (a sqlite3 connection cannot carry attributes): cached per connection and refreshed when the
ledger grows, one view read went from 0.47 s to 0.07 s and an idea from 4–5 s to 0.4–0.7 s. Not tested: two
submissions within the same second (the abort path is code-read only).

## The agent reads the idea (2026-10-24, late evening, D134)

Alex: a fresh Luna loaded with the Hivemind MCP should be able to take a user's question, break it down, call
Hivemind to retrieve what it needs and decide the final theses. `POST /ideas` now runs exactly that inside the
service, with the same tools the MCP front offers.

```
idea ──▶ search(idea) by code (D91 null → no model call)
      ──▶ luna, system prompt idea-v4, tools search / view / evaluate / finish
             turn 1..n: break into 2–4 parts → search each part → view what matters → evaluate a dollar number → finish
      ──▶ code: a finish may name only views the agent has seen; the claim is evaluated again by code; bundles; cost over all turns
```

The turn goes to OpenAI's Responses API with reasoning (the chat endpoint refuses function tools with
reasoning_effort for gpt-6-luna) and no server-side state: the model's encrypted reasoning items are sent back with
every turn, so a turn is a pure function of the conversation and the archive replays a whole card for $0.

### State × event (one request)

| Event | What happens |
|---|---|
| search(idea) null (D91) | card with `no_recorded_view`, no model call |
| the model calls search / view / evaluate | code runs it against the ledger as of the day, appends the result as a tool message, records it in `reading.trace`; a search returns at most 10 views; every view shown is remembered |
| the model calls finish | the loop ends; the arguments are checked against the finish schema (a bad shape → 502) |
| the model answers in prose without a tool call | one nudge ("Call finish with your reading."); a second prose answer → 502 "did not finish" |
| 8 turns without finish | 502 "did not finish within 8 turns" |
| a finish names a view the agent never saw | the id is dropped into `reading.dropped`; the rest stands |
| the claim names a view no part mapped | `evaluation` null, the drop is recorded |
| the same idea again, same day, same ledger | every turn replays from the archive; `cost.cached` true, `cost.usd` 0 |
| the provider refuses or times out (60 s per attempt) | 502 with the error class |

### Value × reader (additions to the card)

| Value | Written by | Read by |
|---|---|---|
| `reading.parts[] {question, view_ids, why}` | the agent's finish, ids filtered by code | the Idea card (one line per part: question and the theses, or "no thesis") |
| `reading.chosen[] {view_id, why, part}` | code, from the parts in order, de-duplicated | `graphOf` and the bundles; UI ownership is D138 |
| `reading.trace[]` | code, one entry per tool call | `scripts/idea_probe.py`; a later FE line "how it searched" if Alex wants it |
| `cost.turns` | code | the measurement |
| MCP `instructions` | `scripts/hivemind_mcp.py` | an external agent (Claude, Luna) reading the same recipe |

### Checks (tests/test_idea.py, the model scripted)

The scripted agent searches, reads two views, evaluates, finishes with three parts (one naming an unseen id): the
request carries the recipe, the first search's views and every tool result in Responses shape with the reasoning
items; parts and chosen come out in order; the unseen id is dropped; the claim is evaluated by code; the trace lists
the calls; the second run replays every turn. An agent that only talks is nudged once and then refused. The null
idea and the config without an idea setting are refused before any call. The HTTP route starts as a user starts it.

### Measured (49 probes, `scripts/idea_probe.py`, 2026-10-24 late evening; the same ideas as the retrieval probes)

| | one call over the top 10 (idea-v1) | one call, two steps, top 20 (idea-v3) | the agent (idea-v4) |
|---|---|---|---|
| views mapped per idea, median / mean | 1 / 1.73 | 2 / 2.71 | 2 / 2.43 |
| ideas with no view mapped | 3 | 1 | 0 |
| parts per idea | – | 2.9 | 2.7, of which 36 named as covered by no view |
| searches the model ran per idea | – | – | 1.6 (the idea's own search is given) |
| model turns per idea | 1 | 1 | 3.7 |
| cost per idea | $0.004–0.010 | $0.008–0.014 | $0.011–0.041, $1.11 for the 49 |
| ids named that the model never saw | 0 | 0 | 0 |

What the agent does better: it reads the ladders it maps (view calls), its parts name drivers and constraints (for
"total revenue above $400B": data-center and segment revenue, Rubin timing, Vera revenue as drivers; margin, opex and
capex as constraints), and every idea gets at least one view. What it does worse: it evaluated thresholds the idea
never stated (9 of 49: "capex will double", "Networking is under-appreciated", "Is the AI trade over?"); code now
drops a claim when the idea states no amount (a year is not one), which removed 8 of them; the ninth, "NVIDIA stock
will hit $300" read against total revenue, is a mapping error the model made and code cannot see. It also maps
further afield than before (Apple's data centers → the capex views; a tariff on gaming → the margin view), which is
the inclusiveness Alex asked for and the reader judges. The one-call two-step prompt maps as many views for a third
of the cost; the agent is kept because it is the flow Alex specified (D134): the same recipe a fresh Luna with the
MCP would follow, with every search and read on the record.

Choices for Alex: a verdict of "off the ladder's scale" when the claimed amount is a thousand times outside every
band (the $300 share price against a revenue ladder); and whether the FE shows the trace ("how it searched").

## Two calls, the service in between (2026-10-24, night, D135)

Measured on the agent version: 27,000 input tokens per idea, 27% of them a 94-line catalog re-sent on every turn,
24% the idea's first search results re-sent, the agent's own new reads under 20%; the mapped count no higher than
one call. Alex: "不是本来就应该这样做吗？". The route is now:

```
idea ──▶ search(idea) by the service (D91 null → no model call)
     ──▶ call 1 (luna): parts [{object, looks_for, period, query}] ×2–4 + claim {part, comparator, value_usd} | null
           input: the idea, the day, the object list (object, kind, number of views; objects with none) ≈ 250 chars
     ──▶ the service: one search per part (8 candidates: id, what it looks at, judged position);
                      the idea's own top 5; the claim's amount checked against the idea's text
     ──▶ call 2 (luna): per part the candidate ids that answer or move it, one sentence why; the summary
     ──▶ the service: admits only candidate ids; follows the dependency graph from the first part's views
                      (upstream = what they depend on, downstream = what depends on them); evaluates the claim;
                      bundles for mapped and related views
```

### Value × reader (what changed)

| Value | Written by | Read by |
|---|---|---|
| `reading.parts[] {index, object, looks_for, period, query, candidates, view_ids, why}` | call 1 types the part and writes the query; the service runs it; call 2 picks ids; the service filters | the Idea card (object · looks_for · period → theses), the probe |
| `related[] {view_id, via, relation, direction, judged}` | the service, from `dependencies` and `dependants` as of the day | `graphOf`, preserving the supplied `via` (D138) |
| `reading.claim {part, comparator, value_usd, view_id}` | call 1 names the part; the service names the view (the part's first mapped) and refuses a claim the idea states no amount for | `evaluation` |
| `reading.trace[] {tool: search, part, query, returned}` | the service | the probe; a later FE line |
| `cost.turns` = 2 | | the measurement |

### State × event (additions)

| Event | Result |
|---|---|
| call 1 writes a part about an object outside the library | the part is kept, its search returns what it returns (usually other objects), call 2 maps nothing to it, the card says so |
| call 2 names an id the part was not offered | dropped with the part named; the rest stands |
| call 2 skips a part | the part reads "the mapping call did not answer this part" |
| the claimed part maps to no view | `evaluation` null, "the claimed part maps to no view" |
| the first part maps to views with no edges | `related` empty |
| the same idea again | both calls replay from the archive, `cost.cached` true |

### Measured (the same 49 probes, one run each; `scripts/idea_probe.py`, archive `poc/data/service/idea-archive.sqlite`)

| | one call, top 10 (idea-v1) | agent, 4 tools (idea-v4) | agent + catalog (idea-v5) | two calls, service between (idea-v6) |
|---|---|---|---|---|
| views mapped per idea, median / mean | 1 / 1.73 | 2 / 2.43 | 2 / 2.39 | **5 / 5.73** |
| related views from the graph per idea | – | – | – | 2.27 |
| parts per idea / vague parts | – | 2.7 / 7 | 2.4 / 0 | 2.7 / 0 |
| parts with no view | – | 36 | 16 | 18 (every part searched) |
| ideas with nothing mapped | 3 | 0 | 0 | 1 |
| input tokens per idea, median | ≈ 2,400 | 15,038 | 27,048 | **2,704** |
| model calls per idea | 1 | 3.6 | 3.9 | 2 |
| cost for the 49 (list price, no cache discount) | $0.25 | $1.11 | $1.86 | $0.56 |
| seconds per new idea (median call × calls) | 3 | 9 | 11 | 11 |
| claims kept / dropped by the amount rule | 13 / – | 13 / 8 | 12 / 4 | 13 / 0 |

The two-call route maps twice as many views as the agent with a tenth of the tokens, and every part is searched
because the service searches it. What it still gets wrong is the model's own reading: "NVIDIA stock will hit $300"
is read as a part about NVDA revenue and evaluated against the total-revenue ladder (holds), the same error in every
arm; call 1 still writes parts about objects the library has no view for (Micron twice, Google, custom silicon),
which is the right behaviour (the part says so and maps to nothing). The expected sets the probe flags against are
my own reading of 49 ideas, not gold; with five views per idea most mappings fall outside them, so the flag counts
UNEXPECTED, not errors.

## Settled, and what the tuning measured (2026-10-24, night)

Alex confirmed the two-call route as the design (D135) and asked for speed, cost and stability to be tuned with
numbers ("你要充分的量化测试指标以及是不是真的能达到你的目标"). Every iteration, its hypothesis, its change and its numbers
are in `idea-tuning-log.md` (13 iterations, 5 kept, 2 refuted, 2 mistakes recorded). The measurements: 49 probes
(`scripts/idea_probe.py`), 8 ideas × 3 fresh samples (`scripts/idea_stability.py`), serial timing with nothing else
running, the archive for tokens and list-price cost. The expected sets behind the probe's flags are my reading, not
gold; Alex's 20 gold ideas are still requested.

### Targets against results

| Target (set before tuning) | Baseline (D135, idea-v6) | Result | Met? |
|---|---|---|---|
| Time per new idea ≤ 6 s | 20.4 s serial (12 s was a sum of medians) | 8.6 s with the lean contract (10.9 s with the full one) | no: two serial model calls at reasoning none take 3–4 s each on this network (an 11-token answer took 6–10 s at 23:30); ≈ 8 s is the design's floor here |
| Cost per idea ≤ $0.005 | $0.012–0.013 | $0.0070 (lean) / $0.0098 (full); call 1 $0.0024, call 2 $0.0045 / $0.0062 | no: $0.0045 of it is call 2's 1,588 input tokens and 247 output tokens; the next cut is fewer candidates, measured |
| First part's direct view agrees in every fresh sample | 6 of 8 | 8 of 8 (full contract), 7 of 8 (lean) | yes / nearly |
| Canvas set overlaps ≥ 0.8 between samples (Jaccard, median) | 0.44 | 0.65 on the design set, 0.68 on a held-out set of eight other ideas | no: three sources of equal size (which secondary objects call 1 names 0.75, the candidates 0.78, which candidates call 2 calls a driver 0.78); four further arms were measured and refuted (seed, idea-text pools, a clause per driver, graph-bound drivers); the levers left trade recall for stability (two drivers per part: 0.67 / 0.76 at recall 0.65 → 0.56) or a second call (0.73 simulated); the same sentence on the same day replays identically from the archive |
| Zero claims on share prices | 1 of 49 | 0: a market-price part is refused by code and carries no claim | yes |
| Zero claims judged against the wrong view | 3 of 13 (found during tuning) | 0 of 13: the pick follows the model's direct label | yes |
| Zero Chinese fields in the card | 1 slip per 24 samples | 2 slips per 49 ideas, both caught and re-asked | yes |
| Zero ideas with nothing mapped (when a view exists) | 1 of 49 | 1 of 49: the tariff-on-gaming idea, where no gaming view exists (the honest answer, D91) | yes |
| Views on the canvas per idea | 5 / 5.73 (median / mean) | 5 / 5.78 (lean), 4 / 5.0 (full), now split direct 2.8 + driver 4.3–4.6; 3 more from the graph | kept |

### Against the sealed gold (D146, 2026-10-25)

Twenty ideas judged as an analyst would (`poc/eval/gold/idea-gold-2026-10-25.json`, sealed; `scripts/idea_gold.py`):
the kept configuration shows the right direct view for 18 of 20, a trap (a view that looks like the answer and is
not) for 2, reaches 65% of the drivers an analyst wants (median), carries 22% noise on the canvas, and judges every
stated amount against the gold's view (20 of 20). Model-authored gold: my analyst reading, not Alex's hand.

### What is now code (the rules the measurements settled)

- Tiers: call 2 labels every mapped view direct / driver / context; the canvas draws direct and driver, the card
  keeps context; at most three drivers per part, the rest become context (six-driver parts measured on one-line ideas).
- The first part's direct view: among the views the model called direct, in the part's own search order, the first
  whose text carries the part's year (FY2027 covers calendar 2026); no object test. The earlier rule (top search hit
  on object and year) overrode the model's right label in 4 of 31 picks and judged 3 claims against the wrong view
  (TSMC capex against TSMC revenue, Meta capex against total expenses, Rubin revenue against total revenue).
- A part about a share price, market cap or valuation maps to nothing and carries no claim; a claim needs an amount
  written in the idea and a direct view on its part; the service evaluates.
- A field that comes back in Chinese is asked once more in English (D133); the slip is counted.
- The service searches each part twice, with the model's query and with its own (object id, what the part looks for,
  period), and interleaves the two lists; the pick's tie-break stays the model's query order (8 of 8 against 6 of 8).
- The parts' queries are embedded in one round trip: five of fourteen seconds were seven serial embedding calls.
- Reasoning effort none on both calls (−30% time, −33% cost, first view 8 of 8; 'minimal' is not accepted by gpt-6-luna).
- The mapping contract is paired with the prompt version in code (`CONTRACTS`): idea-v8 asks no per-part reason
  and writes each candidate once; idea-v9 asks no reason with the full briefs; idea-v7 is the full contract.

### Choices for Alex

- The card's contract: the full one (per-part reason; 10.9 s, $0.0098, first view 8 of 8, canvas overlap 0.65) or
  the lean one (no reason, every candidate written once; 8.6 s, $0.0070, 7 of 8, 0.55). Arm E (no reason, full
  briefs: 7 of 8, 0.50) showed that the reason itself, written after each part's views, is what steadies the
  mapping, though the page never shows it. Alex chose the full contract (D145, "用完整版吧"), the default of the API and the scripts: the full contract (`poc/config/poc-v9.json`: idea-v7, reasoning none); the next arm is a reason
  capped at twelve words, then six candidates per part.
- The gold: written and sealed by Claude in the analyst's role at Alex's request (D146); a disagreement with Alex's own reading becomes a new dated file.
