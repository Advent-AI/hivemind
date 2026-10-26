# Thesis admission v12 (D184/D185): measured against the extraction gold

Plan: `docs/research/2026-10-26-thesis-admission-v12/plan.md`; ledger of rulings: `ledger.md` beside it. Baseline: the
`poc-v23` Jev ledger (`poc/data/english-v23-jev-2026-10-25`). Treatment: `poc-v25` (extraction v12), run with the replay's
default parallel day on fresh ledgers under `poc/data/english-v25-admission-r3-2026-10-26/` (two earlier starts, r1 and
r2, are kept as found and explained below). Gold: `poc/eval/gold/extraction-admission-2026-10-26.json`, 20 cases
labelled by the assistant (D188). Scorer: `scripts/score_admission_gold.py`.

## What changed

- Extraction version 12: a candidate carries `opens_as` (one of `main_driver`, `industry_aggregate`, `policy_stage`,
  `binding_obligation`), `settled_by`, `folds_into` (a shown thesis or empty) and `lost_if_folded` (required when
  `folds_into` names a thesis). Code refuses blank `settled_by`, an unshown `folds_into`, a blank `lost_if_folded`
  beside a named thesis, and a binding obligation due beyond 18 months (`extraction.check_admission`). Versions ≤ 11
  unchanged: preflight over the v23 archive judges the same 1,952 stored answers with the same 451 refusals as the old
  code (`preflight-control.txt` vs `preflight-v12-code.txt`; part D names 170 enum values instead of 159, the new ones).
- Prompt size (`prompt-size.json`, o200k): role v11 6,567 chars / 1,312 tokens → v12 7,458 / 1,502; schema for 10 shown
  theses and 3 groups 2,740 / 741 → 3,050 / 845. Growth of 891 characters: the four reasons and three fields are defined
  once in the role; the user message is unchanged. The recipe lines were already removed in v11.

## Two false starts, both diagnosed on stored data before the next call

| run | calls, cost | what happened | class and mechanism | fix, proof |
|---|---|---|---|---|
| r1 | 9, $0.02 | day one wrote 0 theses | 5/5 schema-valid candidates refused `lost_if_folded is empty`; all had `folds_into` empty (an empty library has nothing to fold into) | the field is required only when `folds_into` names a thesis; $0 replay of the 5 stored candidates: all survive |
| r2 | 58, $0.06 | seed completed: 20 items, 30 evidence, 5 theses; gold A02 and A08 fail | every NVDA revenue thesis gone (0 of the baseline's 3); reason 1 was defined as the company's own annual guidance, and NVIDIA guides only quarterly, so its main driver could never open | reason 1 renamed `main_driver`: an annual quantity that carries the company's value, guided or not; 3 fresh samples of the Feb 25 call ($0.0083): data-center revenue 3/3, gross margin 3/3, five-provider aggregate 2/3, H200 China policy stage 1/3, Anthropic investment as a binding obligation 2/3; 3–5 candidates against the baseline's 10 that day |

## Seed (NVDA only, 2026-02-25..07-23; r3: 91 calls, $0.09)

| | v23 | v25 r3 |
|---|---|---|
| theses opened | 12 | 13 |
| by measure | total_revenue 1, segment_revenue 2 (Data Center, Compute & Networking), gross_margin 1, opex growth 1, tax_rate 2, event 2 (Rubin, H200 licence), capex 1, product_revenue 1 | segment_revenue 2 (Data Center, Compute & Networking), gross_margin 1, operating_margin 1, capex 1, product_revenue 1, event 2 (Rubin shipment; Anthropic investment as binding obligation), policy_event 4 (China import permission for H200; AI Diffusion replacement rule ×2; China antitrust decision), spend_total 1 |
| by admission reason | — | main_driver 7, policy_stage 4, industry_aggregate 1, binding_obligation 1 |
| named a thesis in `folds_into` and still opened | — | 2 (Compute & Networking beside Data Center; H200 import permission beside Data Center revenue) |
| same object, quantity and year held twice | NVDA segment_revenue FY2027 ×2 (v3, v9); tax_rate ×2 (v6, v12) | NVDA segment_revenue FY2027 ×2 (v2, v13) |
| evidence rows from seed items | 49 | 35 |

Gold cases in the seed window:

| case | v23 | v25 r3 | read |
|---|---|---|---|
| A01 gross margin paragraph | partial (opex and tax theses beside it) | **full** | the call opened data-center revenue, gross margin, the aggregate, Rubin and the Anthropic obligation; no opex, tax or total revenue |
| A02 Rubin samples vs production | full | **full** | opened from the call, due 2026-12-31 |
| A03 China: licence, permission, revenue | fail | **fail** | still no numeric China-revenue thesis; the policy question now names the right authority ("Will the Chinese authorities allow any H200 imports", v10), where v23's v8 asked about U.S. authorities |
| A08 quarterly press release | partial (a second tax-rate thesis) | **fail** | zero new theses (right); the gross-margin figure is linked as a repeat; the Q2 revenue outlook ("$91.0 billion, plus or minus 2%") was not extracted by either the release or the CFO commentary, in r2 and r3 alike, where v23 extracted it once |

The two `folds_into` cases are the signal the field was added for: in both, the model named the thesis it could have
attached to and opened anyway, and both are the seed's duplicates (Compute & Networking is the Data Center line under
another name; the H200 import question is a policy stage, which is the right call). The AI Diffusion rule opened twice
(v7 from the January 10-K, v12 from the April 10-Q): matching did not merge two policy theses on the same rule; that
is a matching case, not admission.

Evidence volume fell 49 → 35 on the seed. Part of that is intended (no evidence to opex, tax and total-revenue theses).
The Q2 outlook miss is not: the outlook is quarterly guidance, which is evidence to the annual data-center thesis, and
the prompt's "do not propose theses about quarterly figures or guidance" may be read as "do not extract them". One case
in two runs; counted over the week below before anything is changed.

## Week (2026-07-24..31, every object; r3: 852 calls, $0.51)

| | v23 (week snapshot) | v25 r3 |
|---|---|---|
| theses after the week | 49 | 37 |
| by object | NVDA 17, MSFT 10, META 8, AMZN 6, ai-capex 6, INTC 2 | NVDA 18, chip-export-controls 8, INTC 4, ai-capex 3, AMZN 2, META 1, MSFT 1 |
| financial lines (total revenue, opex growth, tax rate, total expenses, operating loss, growth rate) | 17 | 0 |
| one object, quantity and year held by several theses | ai-capex 2026 ×5, MSFT growth_rate ×4, MSFT segment_revenue ×2, NVDA segment_revenue ×2, NVDA tax_rate ×2 | ai-capex 2026 ×2, NVDA segment_revenue ×2, INTC segment_revenue ×2 |
| evidence rows from week items | 264 | 341 |
| admission reasons of the week's candidates | — | main_driver 15, policy_stage 14, binding_obligation 11, industry_aggregate 3 |
| named a thesis in `folds_into` and still opened | — | 6 |

Gold cases in the week window (13), scored by the written rubric on both ledgers:

| case | v23 | v25 r3 | read |
|---|---|---|---|
| A04 five, four, three companies of capex | partial | **full** | one 2026 aggregate from the call (v1); FactSet's five-company figure opened a second one (v32) with another scope, the census shows the pair; the $1tn-a-year clause did not become a thesis |
| A05 NAVER | partial | **full** | zero project theses; the $1bn investment opened as a binding obligation (allowed by the gold); the 200 MW statement is evidence to data-center revenue and Rubin |
| A06 SK | fail | **fail** | evidence to data-center revenue and Rubin, none to gross margin (the gold's HBM4 cost reading); no project thesis |
| A07 Ohio | fail | **fail** (one link short) | the guarantee thesis opened on July 27 from the first report that named it (v22, binding obligation, check day 2027-07-27); a second one (v23) opened the same day after the model named v22 in `folds_into`; the Tom's Hardware, Quartz and Al Jazeera reports all link to it; Reuters' closing clause (">$700 billion") was not extracted, so one of three links is missing; on July 26 the first attempt was refused: due beyond 18 months |
| A08 press release (seed) | partial | **fail** | see the seed table: the Q2 outlook was not extracted |
| A09 analyst opinion | fail | **fail** | Morningstar: 12 evidence rows, 6 to the Ohio guarantee thesis and 8 to data-center revenue (v23 wrote six near-duplicates to total and data-center revenue); the MarketWatch opposing view: 9 rows to the guarantee thesis (v23 dropped the whole item); the gold's "Sharon AI / Firmus" backstop sentence is not among the quotes |
| A13 MSFT call | fail | **fail** | the $175bn calendar-2026 capex statement is evidence to the five-company aggregate, no MSFT thesis; the model's one candidate was FY2026 total revenue with the item's own day as due day, refused; Intelligent Cloud FY2027 opened from the 8-K exhibit, not the call |
| A15 META call | fail (by the rubric; the hand score was partial) | **full** | one thesis: FY2026 capital expenditures; the Q2 capex line links to it |
| A18 Bloomberg NAVER retelling | full | **full** | late statement, nothing written |
| A19 Taiwan clause | fail | **fail** | the clause opened a policy stage on Taiwan's performance-threshold controls (v25) instead of linking to the China licence thesis; the gold calls it evidence |
| A01, A02, A03 (seed) | partial, full, fail | full, full, fail | unchanged from the seed table |

Over the 13 cases the run has met: v23 full 2, partial 4, fail 7 → v25 full 6, partial 0, fail 7. Every v25 failure is a missing link or a
missing thesis (A03 China revenue, A13 MSFT capex), never a thesis opened beside the gold's.

What the week's 24 new theses are, read one by one against the eight rules (assistant reading):

- Kept by any analyst (11): the five-company 2026 aggregate (two scopes, one question), Intel Products and Foundry revenue, Intel gross margin and capex (a 10-Q with no theses before it), Meta FY2026 capex, Microsoft Intelligent Cloud FY2027, AWS FY2026, Amazon capex FY2026, the Ohio guarantee, the OpenAI chip-purchase financing (v33), the SK Hynix purchase commitment, the AI Diffusion replacement rule.
- Binding obligations an analyst would weigh before opening (5 of 11 candidates): NVIDIA's $1bn in NAVER, $2bn in Marvell, $5bn in Safe Superintelligence (opened twice: v21, v27), a lease for Hut 8's Texas site, a lease for an office building in San Jose (v31). The reason's definition names no size; rule 2 (would the answer move the judgement of NVIDIA?) fails the office lease outright.
- Policy stages an analyst would not track (3 of 14 candidates): two Taiwan prosecutors' charging decisions in the smuggling probe (v24, v28, one matter twice), and the Commerce investigation (v34) is a borderline. The reason's definition says "a stage of a policy process with its authority named"; a prosecutor's charging decision has an authority and is not a policy.
- Duplicates (4 pairs): AI Diffusion rule (v7, v12: January 10-K and April 10-Q; matching did not merge two policy theses on one rule), Safe Superintelligence (v21, v27), Ohio guarantee (v22, v23), the five-company aggregate (v1, v32: the call's "top five cloud providers and hyperscalers" and FactSet's five names). In three of the four the model named the earlier thesis in `folds_into` and opened anyway; its stated loss was the amount or the wording, which the prompt says is not a loss. The field does what it was added for: it marks the decision to read.

Evidence rose 264 → 341 on the week. The opposing MarketWatch view (dropped whole by v23) is linked; the Ohio reports link to the guarantee thesis instead of to revenue.

## August (2026-08-01..15; r3: 887 calls, $0.62) and the whole window

| | v23 | v25 r3 |
|---|---|---|
| theses after August 15 | 90 | 60 |
| by object | NVDA 22, ai-capex 17, AMD 10, MSFT 10, META 8, CRWV 7, AMZN 6, TSM 4, INTC 2, SMCI 2, two macro themes | NVDA 23, chip-export-controls 9, ai-capex 7, INTC 5, TSM 4, AMD 3, SMCI 3, AMZN 2, CRWV 2, META 1, MSFT 1 |
| financial lines that are not a main driver (total revenue, opex growth, tax rate, total expenses, operating loss) | 29 | 3 (total revenue of TSMC, CoreWeave, SMCI, each the company's one revenue line) |
| one object, quantity and year held by several theses | ai-capex 2026 ×11, ai-capex 2027 ×3, MSFT growth ×4, MSFT segment ×2, NVDA segment ×2, NVDA tax ×2, CRWV run_rate ×2 | ai-capex 2026 ×6, NVDA segment ×2, INTC segment ×2, AMD growth ×2 |
| admission reasons of all candidates | — | main_driver 25, binding_obligation 19, policy_stage 16, industry_aggregate 9 |
| named a thesis in `folds_into` and still opened | — | 8 |
| evidence rows / links / judgements | 534 / 716 / 227 | 710 / 834 / 185 |

Gold, all 20 cases, both ledgers scored by the same scorer (`baseline-v23.md`, `final-v25-r3.md`):

| | full | partial | fail |
|---|---|---|---|
| v23 | 3 | 7 | 10 |
| v25 | **9** | 0 | 11 |

Every v25 failure is a miss, never an extra: a thesis the gold wants and the run did not open (A03 China revenue, A07's third link,
A13 MSFT capex, A14 AMD data-center FY2026 and Helios), or a statement not extracted or not linked (A06 HBM4 → gross margin,
A08 Q2 outlook, A09 the backstop sentence, A10 SpaceX capex, A16 inference ARR, A17 the four-company figure, A19 the Taiwan
clause). v23's seven partials were extras beside a right answer; v25 has none.

Cost at published rates (`model.PRICES`, from the archive's tokens), seed + week + August:

| stage | v23 | v25 r3 |
|---|---|---|
| extraction (gpt-6-luna) | 480 calls, $0.57 | 689 calls (the parallel day re-prepares stale requests), $0.85; output tokens carry the three new fields |
| judging | $0.29 | $0.28 |
| matching (Jev) | $0.14 | $0.17 |
| total | $1.01 | $1.31 |

August's 23 new theses, read against the eight rules (assistant reading): kept by any analyst 11 (AMD data-center growth and
gross margin, TSMC revenue, gross margin and HPC platform, CoreWeave revenue and capex, SMCI revenue and gross margin, the
OpenAI $30bn equity investment, the chip-value loss coverage in the financing platforms); binding obligations an analyst would
weigh first 6 (Firebird, SpaceX and Intel equity stakes, TSMC's Sony joint venture, Intel's $15bn offering, SMCI's preferred
dividend, which is not an obligation NVIDIA or SMCI's investors debate); a policy stage that is not one 1 (BIS's critical-minerals
allocation order); duplicates of the 2026 aggregate 4 (big-tech AI spending, AI investment worldwide, four companies, five
companies again); one AMD duplicate (server-CPU growth beside data-center growth).

## What the run shows

1. The clutter class is gone: 29 financial-line theses → 3, 90 theses → 60, with more evidence (534 → 710) and the gold's
   "exactly right" count tripled (3 → 9). The failure count did not move (10 → 11) because v12's failures are misses, not extras.
2. Three classes remain, counted on the 60: duplicates of one aggregate (6 theses for one question; the prompt's own rule
   says another population is evidence, and the model names the earlier thesis in `folds_into` in 3 of the 5 extra cases, then
   opens anyway with a loss that is only wording or amount); small binding obligations (about 7 of 19 fail rule 2: an office
   lease, a $1bn stake, a preferred dividend); policy stages that are proceedings, not policy (3 of 16: prosecutors' charging
   decisions, an allocation order). Together about 16 of 60 theses, against about 60 of 90 before.
3. Evidence misses appeared that the baseline did not have: the Q2 revenue outlook (A08) and the inference ARR (A16) were not
   extracted; both are quarterly or run-rate statements, and the prompt's ban on *theses* about quarterly figures may be read
   as a ban on extracting them. Two cases; a class to count over the whole window before any wording changes.
4. The `folds_into` field is the right lead: 8 candidates named a thesis and opened anyway, 6 of them duplicates.

Proposed next arm (not built; Alex's call, AGENTS §6: an audit of the whole request before any wording grows): a role v13 with
(a) `main_driver` covering a dated milestone on the main product as well as an annual quantity (review finding 1);
(b) the D185 exception stated beside the year limit (finding 5); (c) rule 2 written into `binding_obligation` and
`policy_stage` ("would the answer change the judgement of the company?"); (d) a line that a quarterly or run-rate statement is
evidence to the annual thesis. Each of (c) and (d) must remove at least as much text elsewhere. A code step is also open for
the duplicate class: when `folds_into` names a thesis with the same object, measure and year, matching could compare the
candidate with that thesis first; that is a matching change (06-views) and needs its own decision.

## Data

`poc/data/english-v25-admission-r3-2026-10-26/` (views.sqlite, archive.sqlite, run-seed/week/aug.out and .pid); the aborted
starts `english-v25-admission-2026-10-26/` (9 calls) and `english-v25-admission-r2-2026-10-26/` (58 calls) kept as found.
Scores: `baseline-v23.md`, `seed-v25-r3.md`, `week-v25-r3.md`, `final-v25-r3.md`; prompt sizes `prompt-size.json`; preflight
control and v12-code runs `preflight-control.txt`, `preflight-v12-code.txt`.

## v26: the collision judge (D190), one run over the same window (r4, $1.33)

| | v23 | v25 r3 | v26 r4 |
|---|---|---|---|
| theses | 90 | 60 | 45 |
| 2026 aggregate theses under `ai-capex` | 11 | 6 | 2 (the call's "top five" and "Big Tech combined AI outlays"; seven later aggregate candidates merged into them, one 2027 candidate became a succession) |
| one object, quantity and year held twice | 7 classes | 4 | 3 (aggregate ×2, NVDA segment ×2, AMD growth ×2) |
| collision verdicts asked / merged or succeeded | — | — | 26 / 9 |
| evidence rows | 534 | 710 | 656 |
| gold full / partial / fail | 3 / 7 / 10 | 9 / 0 / 11 | 4 / 0 / 16 |

The judge did what it was built for: the 26 verdicts read one by one are right or defensible (the merges are all aggregate
variants into one of two aggregate theses; "Compute & Networking" was kept apart as the generative probe also judged; the
Ohio guarantee's second report was judged "other period" of the first and stayed new, a miss). No merge removed a thesis the
gold wants: the aggregate the gold wants (A04, A17, A20) is v1, and A17 is now full because the four-company figure links to it.

The gold score fell from 9 to 4 full, and every lost case is an extraction difference between two fresh runs of the same prompt,
not a matching decision: the Feb 25 call did not open the Rubin milestone this time (A02; it opened from the April 10-Q), the
NAVER 55→200 MW sentence and META's $31.1bn capex line were not extracted (A05, A15), CoreWeave's revenue thesis and the
inference ARR were not proposed (A12, A16). This run also opened six total-revenue theses where r3 opened three.

**What this measures about the measurement.** Two runs of one extraction prompt differ by about five cases in twenty on this
gold; D181's drift census (50–65% of items identical between runs) said as much. A single-run gold score cannot separate a
one-step change from the sampler. The rule for the next arms: a matching change is measured on stored candidates (the probe:
11/18 against 8/18) and by the census of duplicates (6 → 2); an extraction change is measured over three fresh runs, or with
the extraction answers pinned and only the changed step re-run. The 9 → 4 swing is therefore not evidence against the judge,
and the earlier 3 → 9 gain is a one-sample estimate with the same width.

## The judge measured with extraction pinned (D190 confirmation)

Both arms replay the same window with every extraction request answered by r3's recorded answer for that item (recorded view
ids translated to the arm's own ids by item and question; group references and fold targets stripped), Jev live, judging
synthetic; the arm adds the collision judge. Only the matcher differs (`docs/research/2026-10-26-thesis-admission-v12/pinned_matching_study.py`,
ledgers `poc/data/pinned-matching-2026-10-26/`).

| | control (poc-v25) | arm (poc-v26, judge) |
|---|---|---|
| theses | 60 (reproduces r3 exactly) | 56 |
| 2026 aggregate theses | 6 | 3 |
| evidence rows / links | 707 / 830 | 711 / 806 |
| collision verdicts / merges | — | 31 / 6, $0.011 |
| gold full / fail | 9 / 11 | 8 / 12 |

The one gold case that differs (A04) differs because the judge merged FactSet's five-company candidate into the call's
aggregate and the $690bn sentence was then stored as a repeat of the CFO's "$700bn" statement (a source reference on the
existing piece), which the scorer's quote pattern cannot see; nothing was lost. No merge removed a thesis the gold wants. The
judge missed two aggregate duplicates it should have merged ("AI spending by big tech companies"; the five companies named
in the Goldman article, which the earlier 3-sample probe merged in 2 of 3), so it takes the class from six to three, not to one.

A first version of this comparison without the id translation lost 4 gold cases to shifted view ids in the recorded links;
that reading is kept in `pinned-arm-v26-par.md` as the record of why the translation exists.

## Role v13 and v14 probes (D192): wording is exhausted

Probe: the gold's 20 items re-sent with the stored v12 user message and the candidate role's system prompt and schema, three
samples, sifted, scored at the candidate level against the gold's must-open and must-not-open keys; the stored v12 answers of
two runs are the controls (`role-probe/role-probe-v13.json`, `role-probe-v14.json`; $0.17 together).

| per sample | v12 (r3) | v12 (r4) | v13: three tests, first contact, quarterly as evidence | v14: v12 + milestone clause |
|---|---|---|---|---|
| must-open keys proposed (of 15) | 9 | 8 | 8.7 | 4.7 |
| must-not-open keys proposed | 0 | 1 | 3.7 | 0.7 |
| candidates on these items | 30 | 30 | 33 | 17 |
| Helios milestone (A14) | 1/1 | 0/1 | 3/3 | 2/3 |
| Ohio guarantee (A07) | 0/1 | 0/1 | 2/3 | 1/3 |
| data-center revenue and gross margin from the Feb 25 call (A01) | 2/2 | 2/2 | 2/2, 2/2, 2/2 | 0/2, 0/2, 0/2 |

v13 raised two milestones and opened clutter (a tax-rate thesis from the press release in two samples, a Taiwan proceeding
in two); v14 raised the same two milestones and dropped the two first-day theses every other version opens. Neither is
adopted. The China revenue thesis (A03) was proposed by no version in any sample; Microsoft's capex (A13) by one sample in
eleven. These are the model's settled judgements on these texts, not readings of a list.

## Two structural arms probed the same way (D193): reasoning effort and the current view

| per sample, on the gold's 20 items | must-open keys proposed (of 15) | must-not-open keys proposed | candidates | note |
|---|---|---|---|---|
| v12, run r3 | 9 | 0 | 30 | stored |
| v12, run r4 | 8 | 1 | 30 | stored |
| v12 + reasoning_effort medium (config only) | 8.3 | 0.7 | 25 | calls 1.8× slower; $0.14 for the probe against $0.08 |
| v12 + each shown thesis's current rung and last reasons in block 5 | 8.3 | 1.7 | 29 | the China numeric thesis proposed once in 11 samples across all arms, here |
| v13 | 8.7 | 3.7 | 33 | D192 |
| v14 | 4.7 | 0.7 | 17 | D192 |

Five arms, one window, same scorer: coverage of the gold's must-open theses sits at 8–9 of 15 per sample for every arm but one,
whatever the wording, the reasoning effort or the context shown. The misses are the same six judgements each time (a numeric
China-revenue thesis, Microsoft's calendar capex and Intelligent Cloud from the call, AMD's data-center FY2026 line and the
Helios milestone, CoreWeave's revenue beside its capex), each proposed in 0–2 of 3 samples by every arm. Three of the six are
readings the gold could accept as alternatives (China as a policy stage; Microsoft's capex as evidence to the aggregate;
CoreWeave's capex as the one thesis); three are misses by any reading (Helios, AMD data-center FY2026, Microsoft's cloud line).

## The six misses read against the texts (D194): one gold key removed, scores unchanged

Each persistent miss was read in its transcript beside every candidate the four v12 runs wrote for that item (archives of r1–r4,
$0). One is the gold's: the call gives no full-year 2026 data-center figure for AMD, only the Q3 guide, second-half server growth
and "more than double in 2027", and every run opens the 2027 line; the FY2026 key (v23's `v53`) is removed from A14 and the
gold resealed (14 must-open keys). Five are the model's: the China policy candidates name the U.S. as the authority the text
leaves open (r1, r4) or nothing is opened on China (r2, r3); Microsoft's $175bn goes to the aggregate as evidence (r3) or
opens as FY2027 capex (r4) while the Microsoft page has no capex question of its own; Helios ("initial shipments on track to
begin later this quarter"), Intelligent Cloud ($40.95–41.25bn guided, Azure +45%) and CoreWeave's raised revenue guidance
($12.4–13.2bn) are stated figures the model never opened, each on the first call of its company in the window, where it opened
one or two theses and stopped.

Rescored against the corrected gold, no ledger moves (A14 still fails on Helios):

| ledger | full | partial | fail |
|---|---|---|---|
| v23 baseline (`english-v23-jev-2026-10-25`) | 3 | 7 | 10 |
| v25 r3 | 9 | 0 | 11 |
| v26 r4 | 4 | 0 | 16 |
| pinned control v25 | 9 | 0 | 11 |
| pinned arm v26 (remap) | 8 | 0 | 12 |

The per-sample tables above count must-open keys of 15; the removed key was proposed by no stored run, so read them as of 14.
