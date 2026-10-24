# Research D: how the old system (`../tn-hivemind`) defined and cut a "thesis", and what went wrong with the cut

Read-only survey of `/Users/lchingen/tn-hivemind` on 2026-10-22. Every quote carries `file:line`. Nothing was edited.
The old universe is three companies (AAPL, AMZN, META); NVDA appears only as an OpenBit reference dossier and as a
desk comparison line, so the examples are AMZN, AAPL and META.

Vocabulary drift to keep in mind while reading: the same object was called, in order of time, *belief* (R1–R5),
*thesis/driver row* (DOSSIER_MODEL, Sept), *idea* (the cross-company ideas call), *debate* + *view* (the debate loop,
late Sept), and *factor* + *ladder* (FACTOR_PRD, Oct). `FACTOR_PRD.md:29` records the confusion itself: "The word
'thesis' meant two things. Today the persistent debate row (stored as a `driver` record) and its immutable argued
views (`thesis` records, one stance each) split one idea in two."

---

## 1. The schema of each concept in the latest prompts

Latest version of each family, with its size (`wc -c`):

| Family | Latest file | Chars | Role in the pipeline |
| --- | --- | ---: | --- |
| Debate map (debate loop) | `prompts/v4-debates-map-v14j.txt` | 20,678 | names the company's live debates (build 5–8; maintenance adds 0–3) |
| Debate view | `prompts/v4-debates-view-v14e-l4.txt` (`-v14e` 19,197) | 21,642 | one argued view per debate: stance, conviction, drivers, flip band |
| Factor map (factor configuration) | `prompts/v4-factor-map-v1.txt` | 6,530 | the map cut for factors: a debate is a *cause* |
| Factor ladder | `prompts/v4-factor-ladder-v20.txt` | 3,687 | 3–4 regime states, key metrics, loading, mixed split |
| Factor registry (maintain / build) | `prompts/v4-factor-registry-v12.txt` / `v4-factor-registry-build-v7.txt` | 3,099 / 3,041 | one global factor per shared world condition |
| Factor identity | `prompts/v4-factor-identity-v4.txt` | 1,688 | same / part_of / distinct against held factors |
| Cross-company ideas | `prompts/v4-ideas-shared-v12.txt` + `{{IDEA_RULES_V12}}` | 7,382 + 17,602 = 24,966 expanded | shared theses (5 families) |
| Ideas consolidation / merge / stance | `v4-ideas-consolidate-v6.txt` / `v4-ideas-merge-v1.txt` / `v4-ideas-stance-v4.txt` | 6,436 / 641 / 3,885 | dedup, fold legal matters, take sides |
| Claim extraction | `prompts/v4-extract-claims-v6.txt` | 6,198 | one fact per claim, ≤80 per window |
| Decide | `prompts/v4-decide-v12.txt` | 12,976 | what a development does to held theses' drivers |
| Due check | `prompts/v4-due-v7.txt` | 4,964 | settles one driver: met_supports / met_breaks / neither / not_reported / not_yet |
| Band check | `prompts/v4-factor-band-check-v5.txt` | 2,114 | may a factor step to the proposed state |

The schemas are strict JSON schemas built in Python, not pydantic models: `src/tn_hivemind/debates/view_schema.py`,
`map_call.py` (`BaseMapRequest`, `AnchoredMapRequest`, `MapRequest`, `FactorMapRequest` at `map_call.py:87,335,550,620`),
`ladder_call.py`, `registry_call.py`. The record shape is written in prose in `docs/FACTOR_PRD.md:125`:
"`states[]` | 3, at most 4, ordered from most bearish to most bullish, each written to §6.2.1:
`{id, name, band, regime, anchor, entry_signposts, implication}`". The thesis row's user-facing fields are in
`docs/DOSSIER_MODEL.md:112-121` (Title, Summary with the edge, Stance, Why/channel, Decision, Horizon, Drivers, Kind),
mapped key for key onto OpenBit's `drivers[]` row.

### 1.1 Debate (map v14j) — the granularity rules the model was given

Definition: "A debate is a question on which informed investors disagree, whose answer moves a value line (revenue
growth, margin, capital intensity and free cash flow, a segment's losses, a legal or regulatory cost, capital returns,
the multiple) by an amount that matters for a company of this size." (`v4-debates-map-v14j.txt:45`)

Identity: "A debate is identified by the decision its view makes: the scope …, the decision variable (what the view is
judged on: a value line, a segment's losses, a legal or regulatory cost, the multiple) and the horizon." (:16)
"The one-view test: two questions are the same debate when one view … answers both." (:17)
"A narrower mechanism or angle under the same decision variable and horizon is PART OF that debate" (:19)
"When unsure between folding two debates together and keeping them apart, keep them apart" (:21)

How big / what to merge (the decisive rule, and the one later named as the root defect):
"**One debate per value line family.** Investment intensity is ONE debate: the capex, its funding …, depreciation,
the margin effect and free cash flow are angles of the same investment-against-returns decision. A new monetization is
ONE debate: several new products, agents, subscriptions or commerce features that serve one strategy are its evidence.
Legal and regulatory cost is ONE debate across its matters (antitrust, privacy, youth safety, content rules, foreign
regulators). A product, a funding deal, a region or a single matter is evidence or PART OF the debate of its value
line, not a debate of its own, unless it alone could move the stock by several percent." (:22)

How many: "at the build, every live debate a PM would track for this company, one per value line family and one per
major profit pool, most important first: usually 5 to 8, fewer than 5 only for a company with a single engine. …
At a maintenance, 0 to 3 debates that nothing held covers; most maintenances add none." (:44)

What to carve out: "Products, launches, partners, vendors, suppliers, incidents, lawsuits and dockets are EVIDENCE
under a debate, never a debate of their own." (:46) "Cover the classic value lines of this kind of company before any
niche: the core revenue engine, investment intensity against returns, new monetization, long-dated bets and their
losses, legal and regulatory cost, capital allocation, and whether the multiple … is justified." (:47)
"The core revenue engine … and a new monetization … are separate debates whenever the new monetization is material to
the bull or the bear case" (:48). "The multiple is a value line. When the desk shows a re-rating or a de-rating … one
debate asks whether the multiple the stock now trades on is justified … Do not fold it into another debate." (:49)

Profit-pool coverage duty: "c_coverage … one entry for every P alias … b_debate: the slot whose view decides this pool's
outlook … or undisputed" (:36). Horizon: "a debate is decided over the next 12 to 24 months" (:51).

Fields per new debate: `a_question` ("one question, answerable within about two years ('Does X hold above Y through
Z?', 'Will A earn back B?')", :52), `b_value_line` (a catalog line), `c_size_anchor` (example given to the model:
"the segment is 97% of revenue; each point of growth is about $2.5B of next year's revenue", :53), `d_bull_case`,
`e_bear_case`, `f_market_implies`/`g_market_items`, `h_evidence`, `i_deciding_kpis` (1 to 4), `j_next_catalyst`,
`k_catalyst_when`, `l_path_metric` (the anchored forecast row: revenue_growth_fy1 for the core engine, next-year EPS
for investment intensity, `eps_growth_5y` for the multiple, none for a new monetization; :59-65).

### 1.2 Factor map v1 — the same call, re-cut around causes (Oct 11)

"A debate is a cause: a driver of the business or the world (a demand cycle, an investment and its return, a
competitive shift, a new monetization, a long-dated bet, a regulatory or legal regime) whose outcome informed investors
dispute … Its states are regimes of that cause; financial lines and KPIs are the evidence that tells which regime
holds." (`v4-factor-map-v1.txt:12`)
"A segment or a financial line is never a debate by itself. When a segment's outlook is disputed, the debate is the
cause that decides it (for example the demand for and the return on the infrastructure a cloud business builds, not
the cloud segment's operating income)." (:14)
"Separate debates when investors disagree about them for different reasons and different evidence settles them (the
core revenue engine and a new monetization; two legal regimes with different decision makers). One legal or regulatory
regime is one debate across its matters." (:16)
Count unchanged: "usually 5 to 8 … at a maintenance, 0 to 3" (:31). Removed from v14j: the value line, the path row,
the profit-pool duty, "sharing a cause does not make them one debate" (`docs/design/THESIS_FORMATION.md`, D1).

### 1.3 View (debates-view v14e-l4)

"A thesis is an argued view, and it can be wrong. Its job is to be clear, testable and honestly tracked, not to be
certain." (`v4-debates-view-v14e-l4.txt:3`). One view per debate; the fields are filled in reasoning order a_ … y_:
both cases with ≥2 numbers each (:17), outside view (:18), the deciding row and its anchor (:20-22), expectation as a
move off the anchor (:23), scenarios (:24), variant (:25), next print (:26), `l_drivers` "2 to 4 signals that will
confirm or refute THIS VIEW over its horizon" each with `c_measure`, `d_observability`, `e_when`, `f_confirms_if`,
`g_refutes_if`, `h_role` validate/invalidate/both/kill (:27-32), premortem (:34), weighing (:35), stance, conviction
(:36-38), flip band (:39), decision triggers add/exit/kill (:40), `u_title` "about 12 words or fewer … Name this
debate's own subject (the core engine, the new monetization, the investment cycle, the multiple, the legal cost), so
the manager can tell the debates apart" (:41), `v_belief` template "R expects X [ID]; this view expects Y because Z;
the next print tests it at P; the answer comes by D when K." (:42), `x_horizon` short/medium/long (:44).
Rule 5 [checked]: "Knowable drivers only: every add, exit and kill trigger sits on a catalog line, a stated KPI, a kind
of company statement seen before, a desk observable, or a dated event." (:52). Share price is refused as a measure (:28).

### 1.4 Factor ladder v20

"A factor is the debate's cause, argued about the business and the world. Its states are regimes of that cause: what
is true of the business or the world in each, in a sentence or two, so anyone holding the evidence can tell which
holds. Financial lines and KPIs are evidence that tells the regimes apart, never the regimes themselves. Choose
key_metrics: the 1–3 shown lines or KPIs an analyst would watch for this cause, or none when events alone decide it."
(`v4-factor-ladder-v20.txt:6-10`)
Ladder: "One axis question about the cause, one named bullish_side and one horizon {kind: structural or tactical, end}.
Structural is 12–36 months; tactical is tied to a dated event." (:13-14) "3 states, at most 4, with stable ids, from
the most bearish up (lowest_state, second_state, third_state, and fourth_state or null), a state for each reachable
band. Give each a distinct regime noun, never a direction word such as Grows, Holds or Erodes. Neutral is a regime with
its own description, not silence or missing data." (:16-18) Each state: regime `{type: regime|event, what, by}` and an
optional anchor "{type: metric, line_id, binding, measure, range: [low, high), unit, periods}, on a like-for-like
basis: year-over-year growth or a trailing-twelve-months value for a seasonal line, never a quarterly level that the
calendar moves … A boundary sits where the world changes, outside a quarter's ordinary noise." (:19-25)
Entries: "A higher state's entries_from_below and entries_to_below: the dated developments (a ruling, a guide, a launch,
a disclosure) that move the factor into it from the state below and back down" (:26-28). Initial position argued from
facts with claim refs (:32-36). Loading: `{transmission, channel: revenue/margin/cash_flow/multiple/balance_sheet/
regulation/flows, materiality, better_state_slot}` (:39-41). Mixed debate: "When a held global factor (a G alias) sets
this debate's cause, load this company on it and keep only the company's residual as this ladder's axis" (:43-46).
Earlier v7 (8,908 chars) carried the axis-narrowing rule later blamed as mechanism F7: "One axis: if the debate bundles
several businesses or initiatives, ladder the one its deciding KPIs track and say so in the axis; the others are
separate factors, never extra states of this one." (`v4-factor-ladder-v7.txt:11-12`)

### 1.5 Factor registry v12 / build v7, identity v4

"Maintain one global factor per shared world condition." (`v4-factor-registry-v12.txt:1`) "A global factor describes a
world condition, not a company's success. At the same world condition, can its strategy, product or cost execution
produce different outcomes? That uncertainty belongs to the company." (:4-5) "Combine candidates only for their common
world condition at the level their evidence supports. Route others with part_of … When identity is a tie, choose new."
(:11-17) Build: "A theme is not one cause." (`v4-factor-registry-build-v7.txt:1`) "Fill F1–F3, null for unused slots."
(:9) Admission: "a stated axis, a bullish side, one horizon …, observable signposts and at least one material loading."
(:17-18)
Identity: "Decide whether a NEW factor is a factor of its own, given the factors already held on the same company: few
factors, no near-duplicates." (`v4-factor-identity-v4.txt:1-2`) same = "one view answers both … measured by another
line of the same cause (its revenue, its operating income, its cash flow)"; part_of = "a narrower mechanism, product,
region or input of one held factor's cause"; distinct = "another driver, or a separate docket of events"; "When torn
between distinct and the other two, answer distinct: absorbing a real factor hides it." (:9-16)

### 1.6 Idea (ideas-shared v12 + IDEA_RULES, consolidate v6, merge v1)

"An idea is a belief-shaped question about a stock that, answered, would mean the stock is mispriced in one direction:
strategy, competitive position, a product or platform shift, management, capital allocation, regulation, industry
structure, sentiment and positioning. It often starts qualitative. Numbers are evidence and a way to check it, never
its starting point: 'segment X keeps growing at least 30%' restates a forecast; it is not an idea."
(`src/tn_hivemind/loop/idea_request.py`, `IDEA_RULES`, "WHAT AN IDEA IS")
Five tests: "1. A real question of belief … not a known status restated as a question … 2. Interesting: the market can
be wrong about it either way. A consensus truism is not an idea. 3. It moves the stock … 4. It forces a decision …
5. Decidable: … at least one driver can show the bull outcome and at least one the bear outcome" (same block).
"ONE FACTOR, ONE IDEA — Two ideas that rest on the same factor through the same channel for the same company are one
idea … Independent matters that resolve on their own timelines (separate lawsuits, separate regulators, separate
rulings) are separate ideas. Frame a product or a long-dated bet through the P&L line that carries it when one exists."
Parts: title ≤100 chars "Never a question, never a metric" (examples given: "Durability of the AI infrastructure
commitments", "Paid conversion of the new subscription tier", "Distribution versus model leadership in AI"); question
≤250 with both outcomes visible; edge ≤250; kind thesis|read; horizon short/medium/long; exposures with channel enum;
born_from; distinct_from; drivers 2–5 each with bull_if/bear_if that name "a named event … AND a quantity … or a date
or window"; a medium/long horizon "needs a sustained falsifier: a result over two consecutive quarters or a full fiscal
year".
Cross-company: five families (macro, geopolitics, industry_shift, supply_chain, regulation); 4–7 drivers, ≥2 theme
drivers with holds_if/ends_if; "typically 5 to 10 in an initial build; in a refresh usually none to two … never more
than 12" (`v4-ideas-shared-v12.txt:63-65`); a worked style example (Chinese EV share in Europe, :67-87).
Consolidation: "expect about 6 to 12 rows for a large company once the cross-company theses already covering it are
counted (a principle, not a quota)" (`v4-ideas-consolidate-v6.txt:4-5`); merge_into = "one factor, one view" (:9);
"A read … and a thesis about the business mechanism behind it are different ideas: never merge" (:12-13);
fold_into_regime: "A legal or regulatory matter gets its own row only if it is material on its own … about 20% of TTM
operating income or more (roughly 1% of market value at a typical multiple) … Every other live matter is folded into
ONE regime view for the company" (:30-36). Merge v1: group ideas that are "the same factor acting through the same
mechanism on the same companies … Keep apart ideas about different mechanisms of one topic, different matters
(separate lawsuits, separate regulators, separate products) or different companies." (`v4-ideas-merge-v1.txt:1-4`)

### 1.7 Claim, decide, due

Claim: "One fact per claim. Split sentences that carry distinct facts; never merge text from different places"
(`v4-extract-claims-v6.txt:13`); materiality "3 = thesis-moving (key KPIs, guidance, major new risk or regulatory
action, major strategic change)" (:31); ≤80 per window (:34). Decide: theses have "2 to 5 DRIVERS" (`v4-decide-v12.txt:8`);
"Most developments about a held debate are this [extends], not a new debate" (:105); `opens_thesis` only for a
significance-2/3 development that "raises a debate about the stock's value no thesis holds" (:97-99). Due: one driver
checked to met_supports/met_breaks/neither/not_reported/not_yet, "The stated condition must be fully satisfied"
(`v4-due-v7.txt:43`).

---

## 2. Real extracted examples (verbatim), with a class per item

Sources: the formation bench's stored samples at 2026-09-26 (map v14d, view v14e): `evals/formation-v1/
vq6-s110-amzn-2026-09-26/dossier-AMZN.json`, `vq6-aapl-2026-09-26/dossier-AAPL.json`, `vq6-2026-09-26/dossier-META.json`;
factor ladders from the 2026-10-14 shadow build `evals/shadow-run-v1/build-2026-10-14/packet.json` (23 factors) and
`evals/thesis-formation-v1/ladder-anchor-resend-1/*.json`; the earlier idea-era dossier
`evals/meta-dossier-v5/dossier-META-stock-v2.json` (16 rows). Classes: (a) a financial-statement line restated as a
thesis; (b) a real debate; (c) a bundle; (d) too fine / trivial / not a business thesis.

| # | Co. | Object (source) | Question / axis as extracted | Ladder or test, due | Class and reason |
| --- | --- | --- | --- | --- | --- |
| 1 | AMZN | debate D1 → view "AWS AI demand can outgrow the consolidated build" (bullish, medium) | "Can AWS sustain strong revenue growth and convert AI demand into durable operating income over the next 12–24 months?" value line: AWS segment | first test: FY2026 Q3 **consolidated** revenue ≥208.5 / ≤200.3 vs 204.4 priced, by 2026-11-05; flip band FY2027 consolidated growth 16.9 / 14.9 | (b) real debate (R1's AMZN half), but tested on the company total, so the test does not read the debate |
| 2 | AMZN | D2 → "Capacity returns lag the FY2027 earnings burden" (bearish) | "Will Amazon's elevated infrastructure and capacity investment earn adequate returns without keeping free cash flow and earnings under pressure through FY2027?" value line FCF | FY2026 capex guide ≥230 / ≤210 vs 220, by 2026-11-05; FY2027 EPS 12.65 / 8.59 vs 10.62, early 2028 | (b) investment intensity vs returns |
| 3 | AMZN | D3 → "North America commerce growth has modest room to persist" (bullish) | "Can North American commerce sustain its recent growth while improving or protecting segment profitability over the next 12–24 months?" value line North America segment | consolidated revenue checkpoint; FY2026 growth 16.6 / 14.6 vs 15.6 | (a) a segment line restated as a thesis; the expected move is +0.2 pt on the company anchor |
| 4 | AMZN | D4 → "Amazon Ads growth adds modest upside to the FY2027 revenue path" (bullish) | "Will Amazon's advertising business sustain growth and monetization momentum over the next 12–24 months, including as shopping interfaces and ad-auction rules evolve?" value line Advertising services | consolidated revenue checkpoint; FY2027 growth 16.9 / 14.9 vs 15.9 | (a) "ads keep growing" (+0.3 pt); the cause (ad budgets shift to commerce media, R2) is in the subordinate clause |
| 5 | AMZN | D5 → "International growth is recovering and adds modest earnings upside" (bullish) | "Can International sustain growth and expand its modest operating contribution over the next 12–24 months?" value line International segment | International growth FY2026 Q3 ≥16 / ≤12 vs 14.8; FY2027 EPS band | (a) segment line restated |
| 6 | AMZN | D6, no view formed (open question) | "Will the combined legal and regulatory matters impose a material incremental cost or constraint on Amazon's earnings and business practices over the next 12–24 months?" | "no majority stance and no neutral sample with a valid flip band" | (c) every matter folded into one regime; no view could be argued on the bundle |
| 7 | AMZN | D7 → "Street EPS growth can support Amazon's central exit multiple" (bullish, long) | "Does the current valuation offer adequate return potential if Amazon delivers the Street's multi-year EPS path, or does the multiple still require stronger growth?" value line none | flip band is the **share price**: < $248.00 / > $268.89 | (d) valuation overlay whose only falsifier is a price move (QUALITY_STANDARD A1 failure) |
| 8 | AAPL | "iPhone upgrades sustain growth beyond the current launch cycle" (bullish) | "Will Apple sustain core device-led revenue growth through FY2027 as the recent iPhone cycle and new lineup translate into demand?" | FY2026 Q4 total revenue 116.3 / 111.7 vs 114; iPhone growth mid-teens / <10%, by 2026-11-07 | (b) the iPhone-cycle debate (R4), measured on the company total plus one iPhone test |
| 9 | AAPL | "Apple's valuation outruns sustainable multi-year EPS growth" (bearish, long) | "Can the current valuation be justified by a sustained acceleration in Apple's multi-year EPS growth, or has the rerating priced in more than the business can deliver?" | share price > $169.11 / < $154.37 at the FY2027 window | (d) price-only falsifier |
| 10 | AAPL | "Memory costs threaten Apple's FY2027 earnings power" (bearish) | "Can Apple preserve earnings power through FY2027 as memory and other component costs rise and the temporary tariff-refund benefit rolls off?" value line operating margin | FY2026 Q4 gross margin ≤47.0 / ≥48.0 vs 47.5 guide; opex > $19.4B | (b) margin structure vs component cost (one of Claude's reference theses) |
| 11 | AAPL | "Greater China recovery persists, but adds only modest FY2027 growth" (bullish) | "Will Greater China's recent recovery persist into FY2027, or will the region return to weak or declining growth?" value line Greater China segment | Greater China growth > 0% / < 0% at FY2026 Q4 | (a) a geography line; the reference left "segment, product and geographic lines" out as evidence |
| 12 | AAPL | "App Store legal changes leave FY2027 earnings largely intact" (bullish, long) | "Will the combined legal and regulatory changes materially reduce Apple's earnings power over FY2027?" value line EPS | FY2026 Q4 EPS ≥2.05 / ≤1.90 vs 1.99; Services revenue ≥ $32.0B | (c) Epic ruling + EU DMA + every other matter in one row, tested on company EPS |
| 13 | AAPL | "AI will support Apple's ecosystem before it monetizes materially" (bearish, long) | "Can Apple turn its AI capabilities into material incremental monetization by FY2027, rather than using AI only to support device demand and ecosystem engagement?" | total revenue 116.3 / 111.7; FY2027 growth 11.2 / 9.2 ("this does not by itself identify AI's contribution") | (b) a real question, with tests that cannot read it (not validatable in practice) |
| 14 | AAPL | open question | "Will Services sustain its growth and profit contribution into FY2027 as App Store economics and other service offerings evolve?" | — | (a) segment line restated |
| 15 | META | "Advertising growth is easing beneath Meta's high-twenties build" (bearish) | "Can Meta sustain high-twenties advertising growth over the next 12–24 months as impression growth and pricing evolve?" value line revenue | FY2026 Q3 revenue ≤63.6 / ≥66.2 vs 64.9; ad growth < 25% / > 28% | (a) the core line's growth rate; R2's cause ("do advertisers keep shifting budgets") is absent |
| 16 | META | "AI infrastructure costs outrun Meta's near-term EPS returns" (bearish) | "Will Meta's AI infrastructure investment earn adequate returns without pushing down earnings and cash generation over the next 12–24 months?" value line EPS | FY2026 capex outlook ≥ $150.0B / ≤ $137.6B; TTM FCF < $35B / > $50B at FY2027 Q1 | (b) R1's META half |
| 17 | META | "Muse distribution is ahead of its monetization" (bearish) | "Can Muse and Meta's other new AI, subscription and commerce offerings establish material monetization within the next 12–24 months?" value line revenue | FY2026 Q3 total revenue band; FY2027 growth 23.1 / 19.9 | (b) new monetization, but every test is the company total (the map's "new monetization: none" row rule came only in v14j) |
| 18 | META | "Wearables keep Reality Labs losses contained" (bullish) | "Will Reality Labs' operating losses remain contained while wearables and VR investment build a credible return, or will losses worsen over the next 12–24 months?" value line RL loss from operations | RL loss ≤ $4.3B / ≥ $5.2B vs 4.8 guide; RL revenue ≥ $0.50B / < $0.35B | (a) a segment loss line; R8's cause ("do wearables become a valuable interface or stay a subsidy") is the real debate |
| 19 | META | "Legal costs outlast Meta's proposed settlement" (bearish) | "Will the combined legal and regulatory matters impose material cash, earnings or operating costs on Meta over the next 12–24 months?" value line EPS | new fine ≥ $567M; FY2027 EPS ≤ $28.25 / ≥ $39.67 vs 33.96 | (c) youth-safety, FTC, EU and privacy matters in one row |
| 20 | META | "Muse excitement outruns Meta's five-year EPS growth" (bearish, long) | "Does Meta's current valuation, after the sharp rebound, fairly reflect the EPS growth investors can expect over the next five years?" | share price > $707.07 / < $647.69 by 2027-12-31 | (d) price-only falsifier |
| 21 | shared | global factor (shadow build 2026-10-14) | "Does demand for AI and cloud workloads absorb the capacity being built and support attractive returns on that investment?" | states capacity_strain / utilization_transition / productive_capacity; key_metrics []; structural to 2029-10-14; loadings AMZN, META | (b) R1 as a shared cause; note: no key metric reaches it (FORMATION_LOSSES §4) |
| 22 | AMZN | company factor (shadow build) | "After industry-wide AI and cloud demand is accounted for, does AWS turn its own capacity and customer commitments into sustained operating-return growth?" | key metric AWS operating income yoy; states named `lowest_state / second_state / third_state` (placeholder ids left in the admitted ladder) | (b) the company residual of #21; the state names are a defect |
| 23 | AMZN | company factor (shadow build) | "Can Amazon sustain North American commerce activity while keeping fulfillment and competitive investment from eroding the business's operating economics?" | states cost_heavy_competition / fulfillment_equilibrium / productive_commerce_flywheel; key metric NA operating income | (b) R6 finally formed as a cause |
| 24 | META | two factors in the same build | #13 "How do courts and authorities resolve youth-safety claims against social platforms, and do remedies materially constrain platform products or operations?" (global) and #15 "How far do youth-safety remedies specifically force lasting changes to Meta's product operation or use of user data, rather than bounded monetary resolution?" (company) | both: remedy_escalation / contested / bounded_resolution, identical `bullish_side` text | (d) a near-duplicate pair admitted side by side (the residual mechanism of S237 produced it) |
| 25 | AMZN | ladder re-send D2 (`ladder-anchor-resend-1/D2-0001018724.json`) | "After accounting for AI-compute demand, are Amazon's broader company-wide investments, including fulfillment infrastructure, converting into durable cash generation quickly enough to offset their cash cost?" | key_metrics L11, L14, L15 (capex, OCF, FCF); states Investment cash strain / Cash-conversion transition / Productive capacity; mixed split on G2 | (a)+(c): "broader company-wide investments" is a bundle whose states are FCF regimes (the "line tracker" class of S190) |
| 26 | META | idea-era dossier rows (meta-dossier-v5, 16 rows, 2026-09-26) | "Paid conversion of Meta One" · "Meta's share of Muse commerce economics" · "Consumer traction for Muse and Meta AI" · "Autonomy and operating costs of Muse tasks" · "Trust and safety in Meta's delegated AI" · "Production economics of Meta's AMD ROCm collaboration" · "Meta's data-center power sourcing strategy" | watch/thesis rows, 2–5 drivers each | (d) too fine: five Muse rows and two supplier/power rows where an analyst holds one or two (DOSSIER_MODEL §5a's "27 META rows" class) |

Counts over the 26 items (treating #25 as (a) and #26 as one item):
(a) line restated: 8 (#3, 4, 5, 11, 14, 15, 18, 25) · (b) real debate: 11 (#1, 2, 8, 10, 13, 16, 17, 21, 22, 23 — plus #1's
and #17's caveat that their tests read the company total) · (c) bundle: 3 (#6, 12, 19) · (d) too fine / not a business
thesis: 5 (#7, 9, 20 price-only valuation rows; #24 duplicate pair; #26 the fine idea-era rows).

Two structural observations from the table rather than from any document:
1. In the debate loop, 13 of the 18 formed views (all but the segment-specific ones) use the **same** first test: the
   next quarter's consolidated revenue against its anchor. The granularity of the debate list was 5–8, but the
   granularity of what was actually *tested* collapsed to one number per company.
2. Three of the 18 views per company set (1 per company) are the valuation row, whose falsifier is the share price.

---

## 3. Lessons and notes on granularity, duplication, drift and counts

Verbatim, with locations.

**How many, and the explosion**
- `docs/DOSSIER_MODEL.md:194-196`: "**How many:** enough to cover what moves the stock and no more. OpenBit's MAG7
  dossiers carry 16 to 50 rows, including shared ones. We expect about 6 to 15 company theses plus the shared
  exposures that matter. This is a principle, not a quota."
- `docs/DOSSIER_MODEL.md:244-247`: "A company's live theses are a **curated set of debates** … Run 3 showed why:
  forming a thesis for every new angle produced 27 META rows, including about 5 youth-litigation rows and about 5 Muse
  rows that an analyst would hold as 2."
- `docs/DOSSIER_MODEL.md:254-256`: "**The debate map owns the set.** The formation names the stock's live debates first
  (4 to 8) and forms one view per debate."
- `docs/research/openbit-dossier-2026-09-25/projection-v2.md:61-63`: "**Granularity.** OpenBit's 16–50 drivers per
  ticker are mostly *shared themes*. Only 13 of AAPL's 21, 4 of META's 16 and 3–5 of AMZN's 24 rows are about the
  company itself (§5). Our 5–8 company beliefs are therefore near OpenBit's own-company count. The visible gap is the
  *specific development-born debates* (Zoox, Muse, CEO transition, Qualcomm) and the shared themes."
- `docs/research/thesis-restructure-2026-10-02/07-identity-and-explosion.md:19-27` (summary): "In run 13, 111 decide
  dispositions named a debate angle: 77 went to a held row as context; 35 became flags …; the flags formed 28 clusters,
  and the map triaged 27 of them: 17 as evidence for a held debate, 6 as immaterial, 4 as new debates; … **5 new rows
  formed: 4.5% of the 111 readings**, over 9.3 weeks and 3 companies."
- same file :31-37: "86 rows in 4 ledgers (76 distinct ids) are 32 distinct debates: 9 company-specific, 6 pure factor
  readings, 14 mixed and 3 valuation. The 20 factor or mixed debates reduce to **8 factors**. … In each run, 10–17
  factor or mixed rows reduce to 6–8 factors: about 2 rows per factor."
- same file :48-53 (gaps): "a company map can add a row that duplicates a held shared theme (run 12: Amazon Leo is
  both); a debate that failed to form is not remembered (run 11 proposed App Store regulation 5 times); the designed
  cap of 10 debates is not built; retire never fired (0 of 143 map edits in run 13)."
- `docs/DECISIONS.md:375` (S77): "today's rows reduce to about 8 factors (one labeller; a blind second labelling before
  any cap is set)." `docs/FACTOR_PRD.md:61`: goal 5 "Few factors, governed: no explosion of near-duplicates."
- `docs/CURRENT_STATE.md:123`: the factor build on 2026-10-14 held "23 factors: 3 global, 7 Apple, 6 Amazon, 7 Meta".

**Factors become financial metrics (the central failure)**
- `docs/LESSONS.md:771-784` (lesson 47): "**When a thesis-quality row fails, look first at the unit of thought, not
  deeper into the numbers** (Alex, 2026-10-10: '财务指标真的只是一个维度而已，千万不要过度的解读。有数字拿好数字验证就好我们重点要搞thesis
  抽取和hedge fund analyst 一样'). A1's work spent a day on anchors … while the factor set itself was the problem: 14 of
  poc9's 23 factors are trackers of one financial line whose states are ranges of it, and the shared causes an analyst
  argues (AI infrastructure payback, the AI customer interface, advertising effectiveness) are split across line
  factors or missing. Formation produces them: the map makes one debate per value line family, the ladder narrows the
  axis to the supplied KPIs, and S89's identity absorbs or separates factors by key-metric overlap, never by cause."
- `docs/DECISIONS.md:83` (S190): "by whether a business claim or a financial range defines the states, 14 are trackers
  of one line … Mechanism: formation reuses the debate loop's map v14j (one debate per value line family, a value line
  and a forecast row per debate …), never revised after S85; the ladder request narrows the axis to the supplied KPIs;
  S89 absorbs or separates factors by key-metric coverage, not by cause."
- `docs/FACTOR_PRD.md:154-159`: "**Why direction words fail, and why buckets fail too.** Labels such as 'Grows / Holds /
  Erodes' state no regime … The opposite failure is a ladder of narrow ranges on one line (operating margin below 35 /
  35–38 / 38–41 / 41% and over): the state becomes whichever bucket the last print fell in, one quarter jumps two
  states, the factor restates a number instead of describing the world, and a reworded debate re-cuts it. The first
  factor window run wrote 102 of 127 states as metric ranges, many 1–5 points wide, and re-cut Apple's growth ladder
  four times in six weeks with the same buckets (S85)."
- `docs/DECISIONS.md:332` (S85) evidence column: "META margin 35 / 38 / 41%; AMZN International $1B / $2B / $3B;
  META's Q2 margin jumped two states; … every ladder request carried all 32 catalog lines and 90 stated KPIs (168 KB)
  while the map names each debate's 1–3 deciding KPIs".
- `docs/FACTOR_PRD.md:36-37` (why): "**The word 'thesis' meant two things.**"; `:39-40`: "**Stance moved only on
  results days.** In run 13, 9 of the 10 stance flips came on 07-29 to 07-31."; `:41`: "**Neutral never occurred** (0 of
  80 views)"; `:42`: "**Nothing ever left.** 0 rows closed in 17 map runs".
- `docs/QUALITY_STANDARD.md` row B1: "A factor is a business or world thesis … **fail**: 14 of poc9's 23 factors track
  one financial line whose ranges define their states (S190, Claude and Codex)".
- `docs/design/THESIS_FORMATION.md:20-23`: "**Reference** … The build-day formation … found 4 (all legal or event
  theses), partly 2, and missed 3 of high materiality: AI compute payback (AMZN, META), advertising budget capture
  (AMZN, META) and Amazon's delivery network." Mechanisms F1–F12 at `:28-44`, F1 being "The map organizes debates by
  value line: 'One debate per value line family'".
- `evals/thesis-reference-v1/REFERENCE.md` ("Left out by both"): "Valuation and the multiple (the priced overlay …);
  segment, product and geographic lines (evidence); capital returns; Apple's CEO transition; small legal and tax items."

**Merging, splitting, drift**
- `docs/LESSONS.md:160-163` (lesson 18): "Loop v4 met 'one open row per debate' while merging Reality Labs into the
  margin row and re-minting it later. — Pair every structural check with its semantic one (coverage, drift, id churn)
  … Never let a stopgap make an irreversible change (a merge) on a model's 'belongs under'."
- `docs/DOSSIER_MODEL.md:270-274`: "**No merges.** A map may propose that two rows are one debate; the proposal is
  recorded and never applied, because a merge is irreversible and a model's 'belongs under' is a judgment (a false
  merge of Reality Labs into the margin row in run 9d)."
- `docs/DECISIONS.md:372` (S74): "Company theses stay, as single-exposure factors; mixed debates are split. Evidence
  about the shared driver goes to the factor; the company thesis keeps only what is specific to the company, so one
  headline never moves a stock twice."
- `docs/DECISIONS.md:70` (S203): identity "absorbed 13 debates, every one a sibling of the same map answer (Apple's
  Epic ruling 5 of 8, EU DMA 3, its AI investment 3 …) while the duplicate census (S199) found one duplicate under the
  current configuration …: 13 real factors lost, 0 duplicates caught."
- `docs/DECISIONS.md:36` (S237): "the maps write every economic debate as a mixed one (the world cause and the
  company's mechanism with its key metrics in one debate), the registry rightly routes the shared cause whole …, and
  S194 removed the residual … without putting the company's half anywhere, so no company line of Meta or AWS reached
  any factor on the shadow build (5 of 20 debates)."
- `docs/design/FORMATION_LOSSES.md:134-144` (Mechanism B): "routed debates lose the company's own thesis and its numbers
  … None of those lines reaches any factor: the global ladders name no key metric (`key_metrics: []` on F1, F2, F3)".
- Drift rule in the prompt itself: `v4-debates-map-v14j.txt:23`: "when the wording has moved onto another debate's
  decision variable (for example a segment-loss debate now worded as the consolidated-margin debate), the debate has
  drifted: reframe it back … Never merge a drifted debate into the debate it drifted onto."
- `docs/FACTOR_PRD.md:174`: "One axis. Two causes make two factors, or a loading on a global factor (S74)."

**Consensus / non-consensus and stance**
- `docs/LESSONS.md:153-158` (lesson 17): "**Don't turn a thesis into a statistic** (Alex, 2026-09-27: 'a thesis doesn't
  always make you money, so I need to know what you are doing'). Five versions of stance rules produced all-neutral
  dossiers, then all-bearish ones from noise."
- `docs/LESSONS.md:148-151` (lesson 16): "A blind forecast ran about 4% low against actuals, beat consensus on 2 of 19
  dates, and its deviation had no skill. — Anchor numbers on consensus × (1 + the company's trailing beat)."
- `docs/DECISIONS.md:614` (S18): "**Alex, 2026-09-27: 'Directional like OpenBit'.** Every view takes a side from the
  model's lean against the anchored priced reference, however small … Measured before the choice: v11 all neutral".
- `docs/DOSSIER_MODEL.md:124-126` (five tests): "2. **Interesting.** The market can be wrong about it. A consensus
  truism is not a thesis."
- `docs/FACTOR_PRD.md:43-44`: "**What is priced is mostly words.** Only 31% of run-13 views state a priced number on
  their own variable. No replay ever saw published forward consensus."
- `docs/research/thesis-restructure-2026-10-02/05-what-a-thesis-is.md` §2-3: "bullish if we place the world in a state
  better for the trade than its price assumes, bearish if worse, neutral if the same … a thesis can be right and turn
  neutral because the price caught up. … That is a take-profit signal, and today's model has no way to express it."

**Process lessons that bear on granularity decisions**
- `docs/LESSONS.md:107-114` (lesson 12, Alex: "you're looking at the tree, you're not looking at the forest").
- `docs/LESSONS.md:185-191` (lesson 21): "The PM mean stayed flat for six runs while the label files named the causes".
- `docs/LESSONS.md:752-770` (lesson 46): the A1 row (a real falsifier) failed on "run 11's valuation and premium theses,
  whose only falsifier was a price move that would realize the thesis rather than refute it."

---

## 4. Evals and metrics that measured thesis quality, with results

| Instrument | Where | What it judges | Recorded results |
| --- | --- | --- | --- |
| Blind thesis review (G13 / A2) | `evals/stage23-gates-v1/thesis_review_brief.py:3-6, 66-73` | "Would a hedge-fund or equity analyst pitch or track this idea? Is the belief real and interesting, the transmission to the stock clear, the stance justified, and is it validatable through its drivers?" grade good/weak/bad, flags noise, truism, restated_fact, no_transmission, not_validatable; gate ≥60% good and 0 noise | `docs/BENCHMARK.md:383-399`: META runs 1–4: 56% / 46% / 58% / **92%** good; rows 9 / 13 / 26 / 13; "Rows an analyst keeps after merging (Claude labels)" 19/26 and 10/13; "OpenBit's 16 META rows judged good by the same reviewer 0/16" (OpenBit rows carry no drivers). `docs/QUALITY_STANDARD.md` A2 last measured: AAPL **50%**, AMZN 86%, META 75% |
| Blind PM judge (8 dimensions) | `evals/stage23-gates-v2/README.md:116-128`; rubric file removed in S187 | D1 materiality, D2 variant against a named consensus, D3 priced-in awareness, D4 transmission, D5 catalyst and timing, D6 falsifiability, D7 risk-reward and conviction, D8 stance justification and balance; "PM-actionable: a total of 16 of 24 or more, with no zero on D1, D2, D6 or D8"; noise = D1 0 | `docs/BENCHMARK.md:415-430`: META 09-26 totals 20.8–21.7 / 24, D2 2.3–2.7, D3 2.0–2.2; "OpenBit's rows score 4.2 and 3.3 under the same judge (the rubric rewards our fields, so this is not a research comparison)"; "The plan's target of +0.5 on D2 and D3 is not met" |
| Blind debate list (PM gate h2) | `evals/formation-v1/vq4-amzn-2026-09-26/pm-gate-h2/debates/list/packet/brief-1.md` | a blind analyst lists "the 3 to 6 debates that decide this stock's value"; compared with the map's list | labels at `…/labels-1.json`: B1 AWS AI payoff, B2 investment cycle vs FCF, B3 retail demand vs fulfillment profitability … (the reader's own cut, 3–6 debates) |
| A1: a real falsifier on every thesis | `docs/QUALITY_STANDARD.md` A1 | price is never the falsifier | met on the factor window (0 price conditions); failed on run 11's three valuation/premium theses |
| B1: a factor is a business or world thesis | `docs/QUALITY_STANDARD.md` B1; `evals/a1-factor-v1/REPORT.md` | states are regimes, not ranges of one line | **fail**: 14 of 23 line trackers; `a1-factor-v1 §6`: "**7 of 23 pass**" structural AND semantic; §3 "14 directed boundaries on 8 factors have no entry" |
| Reference-thesis match | `evals/thesis-reference-v1/REFERENCE.md`; RULES.md | nine theses two blind analysts both wrote (R1–R9) against the formed factor set | build day: "3 of 9 matched" under the calibrated reading; by 08-14 found 4, partly 2, missed 3 of high materiality |
| Duplicate census | `evals/thesis-formation-v1/dup-census/brief.md`; `docs/DECISIONS.md:74` (S199) | per pair: same_cause / face_of_same_cause (duplicate) vs overlapping_evidence / distinct_causes | 349 same-company pairs, two blind readers agreed on all 349, "found three duplicates … the only one under the current configuration (1 in 181 pairs)" (META operating leverage vs AI infrastructure payback) |
| Identity-call audit | `docs/DECISIONS.md:70` (S203) | what the identity call absorbed | "13 real factors lost, 0 duplicates caught" → identity now judges only against factors held before the run |
| Formation funnel | `docs/research/thesis-restructure-2026-10-02/07-identity-and-explosion.md:19-27` | how many debate angles become rows | 5 new rows of 111 readings (4.5%) over 9.3 weeks, 3 companies; ~3 clusters a week, ≤0.2 new-factor candidates a week |
| Stance behaviour | `docs/FACTOR_PRD.md:39-42`; `docs/QUALITY_STANDARD.md` D4 | neutral present, flips, closes | run 13: 9 of 10 flips on results days; neutral 0 of 80 views (debate loop) vs 15 of 25 open rows neutral (factor window); 0 rows closed in 17 map runs |
| Claim-level semantic dedup (evidence, not theses) | `docs/research/semantic-dedup-2026-09-25/empirical.md` §0 | repeats of the same fact | repeat recall ≈0.75 at 0.97 precision; "count evidence per development, not per claim" |

No instrument in the old repo measured "is this a real debate" on its own; the nearest are the thesis review's
`pitch_or_track` + flags (restated_fact, truism) and the reference-thesis match (a model-authored gold of 9 items).

---

## 5. The end-user side, and the value proposition

**User journey (binding anchor).** `docs/DOSSIER_MODEL.md:19-35` (Alex, 2026-09-25): "It is just me having a thesis or
me checking my thesis to what is evolving in the market. So I always have a record of what's changing. And then as a
user, I can basically say, hey, I want to follow the thesis … And that constitutes the trade that the agents can then
formulate a trade plan … don't make it complex." Four steps: **See views** (for a stock or a theme: what we believe,
direction, why) · **Check a thesis against the market** (which drivers moved, when, why, "with a permanent record of
every change to the view") · **Follow** ("at the version they adopted … The user's adopted version is never
rewritten") · **Act** (the followed thesis is the input to a trade plan under separate authority).

**The three questions the dossier answers** (`docs/DOSSIER_MODEL.md:89-92`): "1. What views should an investor hold on
this stock, and in which direction? … 2. What will prove or break each view? … 3. What just moved, and does it change
a decision?" and "Every piece of news either moves a driver of some view, or it is noise for this purpose."

**What a row carried for the user** (`docs/DOSSIER_MODEL.md:334-344`, OpenBit shape): rows (title, stance, lifecycle,
role, kind, horizon, channel, why; 改写 marks a stance or conviction change), a lifeline per row coloured by stance over
time, "What moved" (latest 20 moves with `sens` and `moved`), a narrative with the headline thesis, "**next catalyst**
(the soonest dated driver of the headline thesis: what is expected, when, what validates, what breaks), **breaks if**
(the headline's kill driver)", and the `x_hivemind` extension (belief, decision, drivers with their data state,
evidence items).

**The parked web UI** (`web/v4/app.js`, `web/v4/index.html`, title "Hivemind"): a company page with a price chart whose
rings mark the days views appeared (`app.js:395-600`), a views list filtered by stance with pills, title and the
debate question (`:629-640`), and a detail pane with "What would test it" (each driver with Supports if / Breaks if /
When, state pills Waiting / Due now / Answered / Not reported, and "Would end the view" on the kill driver;
`:706-735`), "Settled tests" (`:738-752`), the stance history, and the two cases beside the view (`:651-656`).

**Alex's product statements** (`context/discussion/USER_REQUESTS.md`): item 6 "「我们早就有这些金融和各种情绪面数据了……不是壁垒」。
要从未来用户旅程与价值创造找方向。"; item 15 "认可「我的投资，今天有什么值得重新决定？」和「接上 TrueNorth，让你关心的投资持续被研究，
让值得采取的决定被落实。」"; item 16 "两条明确用法：输入想法/叙事，匹配最适合的几个 stock，一键跟踪，或起 basket 来 trade；查看每个 stock
当前核心 bull/bear/neutral 叙事，以及何时、被什么 invalidate，形成历史流。"; item 13 the vision "agentic wealth manager … 在主流 AI
app 中想到接上 TN". `docs/FACTOR_PRD.md:63`: goal 7 "A path a user follows to go bull or bear on a stock, and a way to
check how original their own view is."

**Versus "just ask GPT".** No document in the old repository states the product's value against asking a chatbot in
those words. What it does state, and what functions as the differentiator throughout, is: (1) a persistent, dated,
append-only record of each view and of every test and stance change (`README.md:12-13`: "Records are append-only and
knowledge-time aware: nothing is backdated, and a view never reads information from after its date"; DECISIONS S42);
(2) tests settled by code against reported numbers, never by the model's recollection (`DOSSIER_MODEL.md:213-216`;
QUALITY_STANDARD "Numbers in the thesis come from code"); (3) a view argued against what the price already assumes
(view prompt rule 3 "No anchor, no 'the market'"); (4) follow/originality (FACTOR_PRD goal 7). Alex's own framing of
the gap is item 6 above: the data is not the moat; the journey and "what is worth re-deciding today" are.

---

## 6. Closing summary: what the old granularity was in practice, and the failure modes recorded

1. On paper, a company carried 5–8 debates (one per value-line family and one per major profit pool), each with one
   view of 2–4 drivers; shared themes were 5–10 at the build; later 6–15 rows per company was the stated expectation.
2. In practice (formation bench, 2026-09-26) each company held 6 views + 0–1 open question: core line growth, one
   investment-intensity row, one or two segment/geography lines, one bundled legal row, one valuation row.
3. The unit was the *decision variable* (a catalog line or forecast row), so 8 of 26 sampled items are a financial line
   restated as a question, and 14 of 23 factor ladders were ranges of one line (S190); the shared causes an analyst
   argues (AI compute payback, ad-budget shift, delivery network) were missed or split across lines.
4. Tests collapsed further than the list: 13 of 18 views used the same next-quarter consolidated-revenue checkpoint,
   so distinct debates were falsified by one number; 3 valuation rows had only the share price as falsifier.
5. Bundling was prescribed by prompt ("Legal and regulatory cost is ONE debate across its matters"), and the bundled
   rows then could not be argued (AMZN D6 formed no view) or carried every matter under one EPS test.
6. The opposite failure came earlier: forming a row per angle gave 27 META rows (about 5 youth-litigation and 5 Muse
   rows an analyst holds as 2); the cure was a map-owned set, "no merges", and a 4.5% admission rate (5 of 111 angles).
7. Duplicates were rare once the map owned the set (1 in 181 pairs), but the identity call absorbed 13 real factors
   while catching 0 duplicates; the fix was to never compare a run's own debates with each other outside the map.
8. Splitting a mixed debate into a shared factor plus a company residual lost the company half (5 of 20 debates had no
   company line reaching any factor) and then produced near-duplicate pairs when the residual was restored.
9. Drift and buckets: a ladder of 1–5-point ranges on one line re-cut Apple's growth ladder four times in six weeks and
   jumped META two states on one print; a segment-loss debate drifted into the margin debate and was falsely merged.
10. The old repo's own correction (S85, S190, S191) is the frame the new design inherits: a view is one *cause* about
    the business or the world, 3–4 regime states, 1–3 key metrics as evidence, segments and lines are evidence not
    debates, and valuation is an overlay not a thesis; its reference set is nine theses for three companies (3 shared,
    6 company), i.e. about 3–5 real debates per company plus 1–2 shared causes it loads on.
