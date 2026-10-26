# Trace review of the v12 run: why it still misses the gold, and what a senior analyst's process says to change

Alex, 2026-10-26: "看所有的 trace 然后告诉我我们怎么持续做的更好接近 golden … We don't want to overfit … It needs to act exactly like a
very senior hedge fund analyst … a lot of the root causes … may need more thinking." Read: every thesis of the r3 ledger
(60), every gold failure (11) to its raw request and answer, the six duplicate aggregates to their matching decisions,
the 157 evidence rows dropped for lack of a target, and the first item of each company. Ledger
`poc/data/english-v25-admission-r3-2026-10-26/`; scores in `poc/reports/2026-10-26-admission-v12/`.

## What an analyst does that the pipeline does not

| Analyst step | Pipeline today | What the traces show |
|---|---|---|
| Carries a small model of each company: 2–4 live debates, each with the current number and the bogey | Block 5 shows open theses as question, focus and due date only (05-extraction: "no state, no evidence") | The model cannot apply the swing test (would this change the view?) because it never sees the view |
| On first contact with a company, builds that model from the first substantive document | v12 asks it to attach by default and open only for a stated reason | First items: AMD call 2 theses and 2 evidence rows (v23: 8 theses), MSFT call 0 theses, META call 1, CoreWeave 2, TSMC 1; A13 and A14 fail here |
| Holds one debate per decision; estimates, populations and sources are inputs to it | Thesis identity is the quantity (object, measure, scope, period); matching asks "the same quantity?" | Six 2026 aggregates: each later one had every earlier one in its matching list and Jev answered "new" six times, correctly for quantities; the extractor named none of them in `folds_into` |
| Treats a theme (policy, cycle) as worth tracking only through the companies it moves | Theme candidates carry no dependant; dependencies are chosen later in matching | 16 policy-stage candidates, 3 proceedings opened (prosecutors' charging decisions, an allocation order); 9 aggregate candidates |
| Weighs an obligation by its size against the company | `binding_obligation` has no size test | 19 candidates: an office lease, a $1bn stake, a preferred dividend beside Ohio and OpenAI |
| Keeps quarterly guidance as the update to the annual view | The role bans theses on quarterly figures; nothing says they are evidence | Q2 outlook ($91.0bn) and the inference ARR ($250m) not extracted in r2 and r3; v23 had both |
| Prunes the list periodically | Append-only; the daily duplicate check of 06-views is a proposal | Pairs opened on the same matter: AI Diffusion rule (10-K then 10-Q), SSI investment, Ohio guarantee, Compute & Networking beside Data Center |
| Reads twice before committing | One sample at temperature 0.2 | Run-to-run identity of items 50–65% (D181 census); the probe's three samples opened 3, 4 and 5 candidates on the same call |

## Root causes, by design layer

1. **Identity level (06-views).** The library's unit is a quantity; the analyst's is a question. For a company line the two
   coincide (Data Center revenue FY2027). For an aggregate they do not: "capex of the top five", "of the five named", "of the
   four largest", "big tech AI spending", "AI investment worldwide" are five quantities and one or two questions. Matching's
   criterion "the same quantity, another period" (D168) says nothing about "another population or estimate of the same question".
   This is the largest remaining class (6 of 60) and no prompt wording reaches it: the decision belongs to matching.
2. **Cold start (05-extraction).** "Attach by default, open for a reason" is the right rule once a model of the company exists;
   with no thesis for the subject it under-produces (1–2 theses) where v10's recipe over-produced (8–9). The analyst's first
   read of a company is a different act from the hundredth: it builds the 2–4 debates. The contract should say so, generally:
   when the library holds no thesis for a subject in the item, write the questions that carry its value now.
3. **Tests, not categories (05-extraction).** The four reasons are categories; the labeller's rules are tests (swing,
   independence, same result, minimal sufficiency). The model opens a proceeding as a `policy_stage` and a $1bn stake as a
   `binding_obligation` because each fits a category; it would fail the swing test. Conversely it folds China revenue into
   Data Center revenue because the category "main driver" is satisfied once; the independence test (different drivers, different
   evidence stream) would keep it apart. The ban list ("do not propose theses about quarterly figures…") is a category in reverse
   and it suppressed evidence. One principle should replace both lists.
4. **Themes without dependants (05/06).** The PRD has dependencies; the extractor is never asked which asset thesis a theme
   candidate feeds. A theme with no dependant is a number warehouse entry (D24/D28). D187 (Alex: "可以") already says a macro
   theme opens only with a dependant.
5. **Blind to the view (05-extraction block 5).** Without the current rung and the key evidence, the model cannot say
   whether a statement changes anything; it can only classify it. Showing the state is a design change with a cost (tokens,
   and the risk the model anchors on the current view when extracting).
6. **Sampling.** Not a design flaw to fix with a rule; a measurement fact to carry: every score has ±2 cases of noise.

## Checked and not a cause

- The 157 evidence rows dropped as "links to nothing shown": 77 had empty links (ETF moves, valuation multiples, an executive's
  departure, stock-price history: noise an analyst would also skip); 80 named a target not shown (a candidate that was itself
  refused, or a thesis outside the shown set). This is not lost analyst memory; no notes layer is needed.
- The code checks: 8 admission refusals in 480 items, none wrong on reading; the year rule refused four FY2028 quantities,
  all rightly.
- Matching: six "new" verdicts on aggregates are correct under the current criterion; Jev's two misses on the same matter
  (AI Diffusion rule twice, SSI twice) are the known free-scope class (log row 49), unchanged by this slice.

## How to keep moving toward the gold without overfitting

Each proposal is one general mechanism with the class it addresses and the count it would move; none names a company,
project or topic.

| # | Mechanism | Layer | Class it addresses (count on r3) | Risk | Measure by |
|---|---|---|---|---|---|
| 1 | Matching asks the analyst question for same-theme, same-measure, same-year candidates: "a separate decision, or another estimate/population/wording of the shown question?" (one more Jev relation option, like D168's period option); a merge records the population on the evidence | 06-views, `jev_matching` | 6 aggregate theses → 1–2; also Compute & Networking beside Data Center | Over-merging distinct quantities (the row-43 case: guarantee vs financing) is guarded by measure, not scope | Re-send the 9 aggregate candidates with the new option, 3 samples each, before any run |
| 2 | First-contact rule: when no thesis exists for a subject in the item, write the 2–4 questions that carry its value from this item (the same four reasons, applied to the company at once) | 05-extraction role | AMD 2 → 4, MSFT 0 → 2, META 1 → 2, CoreWeave 2 → 4; A13, A14 | Over-opening on thin first items (a press release) | Score first-contact items only, gold A12–A15 |
| 3 | Replace the four category definitions and the ban list by the three tests the labeller applies (would the answer change the judgement of the company; could it come out differently from the related question; what is lost if folded) and keep the four reasons as the closed `opens_as` enum; quarterly or run-rate statements named as evidence to the annual question | 05-extraction role (net shorter) | 7 small obligations, 3 proceedings, China revenue (A03), Q2 outlook and ARR (A08, A16) | The model may apply the tests loosely; measure, do not add examples | The 20 gold cases plus the census of reasons |
| 4 | A theme candidate names the asset thesis it feeds (`feeds`: a shown or candidate id, schema-enforced); matching records it as the dependency; a theme with none is refused | 05/06, schema + `sift` | 16 policy-stage and 9 aggregate candidates; implements D187 | None found: dependencies already exist in the design | Count theme theses with a dependant (today 0 rows in `dependencies`) |
| 5 | Show the current rung and the two most recent pieces for each shown thesis in block 5, so the swing test has something to swing | 05-extraction block 5, PRD change | Every judgement of "does this change anything"; cannot be counted before trying | Anchoring; tokens (+10–20% input) | A/B on one week: evidence links per item and gold links |
| 6 | Decide 06-views' pending proposal: a daily pairwise duplicate check among open theses of a subject, fed by the same-key census and `folds_into` | 08-pull-mode | Pairs opened days apart (AI Diffusion rule, Ohio, SSI) | Merging rewrites history; must be append-only | Pairs merged per day, read one by one |

Order I would take them in: 1 and 4 first (they are code and schema, they move the biggest counted classes, and neither
grows the prompt), then 3 and 2 together as role v13 (one audit, net shorter than v12), then 5 as its own A/B, and 6 as
pull-mode design. Each step: stored-data proof first, three fresh samples on the decisive cases, then one run over the
same window, scored by the same scorer against the same gold, with the census beside it.
