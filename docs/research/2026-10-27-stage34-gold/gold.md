# Steps 3 and 4: the gold, written before any send (D201)

Twenty-four incoming records from the paused v29/v30 ledger, each at the library state before its own sequence number
(`cases.json` beside this file holds the record, the question catalog and the complete evidence of the linked question
at that moment, read through the step 2 reader). Drawn with seed 20261027 from the 3,216 evidence decisions and 69
candidate decisions of the run: 6 the product called repeat, 4 replace, 5 new with a near-threshold Jev score (same
statement or revision between 0.35 and 0.65), 3 clear new, 2 new-question candidates, 1 merged candidate; H01–H03 are
held out (drawn after the first 21, never used to tune a prompt). The reference answers below were written by the
assistant reading the record beside the question's existing evidence, before any model output of the new path
existed; they are assistant-authored, not independent human gold, and they are frozen for the comparison.

## The analyst's standard for this step (re-read of the gold, Alex 2026-10-27: "做一个 hedge fund analyst 的专业视角去看怎么做这一步的标准")

What a hedge-fund analyst does when one new record arrives on a name they cover, written as the rules the gold scores:

- **A. Primary-source test.** Who first said it, when? If the record's claim is already held from that original source, the record is a
  pickup: it adds an outlet, never a fact. 24/7 Wall St. restating the Q1 print, a bank note repeating the customer's own remark, an
  author repeating his own figure: pickups. They do not enter the weekly note.
- **B. Period and definition test.** A record bears on a question only if its period and definition match, or the mapping is stated.
  A Q1 print is not a full year (run-rate is a judgement, not a fact); FY2028 growth is not FY2027 growth; five companies' total AI
  outlays are not four hyperscalers' data-center capex. A mismatch is background with the mismatch named, never a rung-moving estimate.
- **C. Independence test.** Independent support needs a different original source with its own access to the fact: a customer's own
  disclosure, a filing, a third-party test. A vendor claim relayed by ten outlets is one source; ten analysts quoting management are one
  source. Support counts sources, not records.
- **D. Conflict rule.** A contradiction retires nothing. Both pieces stay; the argument says "contested", names what resolves it (the
  next print, a shipment confirmation, a filing), and confidence falls until then. A company's denial erasing an analyst's delay report
  is the worst single error this step can make: it hides the risk from the judgement.
- **E. Revision rule.** Only the owner of a claim revises it: management revises its guidance; the announced deal supersedes the rumour
  of that deal. The history stays, because the path is information (a guarantee that shrank from $250bn rumoured to $105bn announced
  says something about appetite).
- **F. Materiality filter.** The argument changes only when the record moves a number, a probability, a risk or a condition: "would it
  appear in this week's note on the thesis?" If not, the source is stored and the argument is left alone. A first delivery to a named
  customer with no size, a vendor efficiency claim, a consumer-GPU price note: store, mention at most as a condition.
- **G. New-question rule.** A question opens for a new investment judgement, a decision that could change the position, not for a new
  legal form, a new figure or a narrower scope of a judgement already tracked. The catalog's twenty yes/no questions on individual
  equity stakes are, to an analyst, one judgement: NVIDIA's investment exposure to its customers and its circularity. A candidate
  phrased as "did NVIDIA sign the xAI round" is that judgement's wrong form; the right form names the exposure.
- **H. The argument is the deliverable.** One defended statement per question: the current lean, the facts it rests on with their
  source quality, what opposes it, the conditions and limitations, and what would change it. Every update rewrites it in full, so the
  judgement and a human read one paragraph, not 591 pieces.

Three rows change on this re-read: G07 and G14 accept background_only as well as update_existing (rule F: a sizeless delivery and a
vendor efficiency claim need not touch the argument); G20 no longer accepts the candidate as written (rule G: the yes/no form is not an
investment judgement; propose_new is right only when `independent_judgement` names the exposure/circularity view, otherwise unresolved
or background_only). The control's score is unchanged by these edits (G07/G14/G20 were scored right or wrong on other fields).

## The unit and the fields

One case = one incoming record (an evidence piece or a candidate question) against the library at `before_seq`.

Step 3, the relation opinion (Jev's job, an opinion with a score):
- `question`: how the record bears on each linked question: direct (a reported, guided or estimated value of the
  measured quantity, or the event the question asks about) / lead (a driver, a customer, a product, a denial: bears on
  the answer without stating it) / background (context, an argument, a later period) / unrelated / uncertain.
- `evidence`: for the closest old record(s): same (the same claim from the same original source, however reworded or
  by whichever outlet) / revision (the same claim's later value or status) / different.

Step 4, the research update (the analysis model's job, read with the complete old and new content):
- `action`: update_existing(question ids) / propose_new / background_only / unresolved.
- `replaces`: old record ids that this record supersedes, or none. "None" is an assertion scored as such.
- `new_information`: what the question's argument learns, or none.
- `independent`: whether the record is independent support (a different original source), with the original source.
- `limitations` and `opposing`: qualifications the argument must keep; old records this one contradicts.

The product's stored decision (Jev + writer, D167–D169) is the control; its verdict against the gold is the last column.

## Cases

| case | record (short) | S3 question | S3 evidence | S4 action | replaces | new information | independent | limitations / opposing | product decision → verdict |
|---|---|---|---|---|---|---|---|---|---|
| G01 | SiliconANGLE relays NVIDIA: Cadence/Synopsys 1.5x on Vera (07-26) | v5 lead | same as e688 | update v5 | none | none (second outlet, same day, same claim) | no: NVIDIA's own benchmark | vendor benchmark; no sales | repeat→e688 **right** |
| G02 | 24/7 WS restates Q1 FY27: $81.615bn rev, $75.246bn DC, 75% GM, $48.554bn FCF | v6 direct; v11 direct; v14 direct | same as e150/e28 (DC), e124 (total), e204 (GM) | update v6, v11, v14 | none | none; four quantities in one sentence, each already held | no: NVIDIA's Q1 report | one source record carries four claims; split when stored | repeat→e150 **right** |
| G03 | 24/7 WS: Q2 guidance $91bn ±2%, GM 75%, excludes China DC compute; author: China weakness priced in | v6 direct (guidance); v11 direct; v14 direct | same as e33 (guidance) and e200/e37 (China exclusion) | update v6, v11, v14 | none | the ±2% range only (immaterial); the author's "priced in" is background | no: NVIDIA guidance relayed | keep e200's exclusion as a qualification of the guidance | repeat→e33 **right** |
| G04 | Joel South: Q1 FY27 revenue $81.62bn +85.2%, NI $58.32bn +210.6% | v11 direct; v22 direct | same as e124 | update v11, v22 | none | none | no: NVIDIA's Q1 report | — | repeat→e124 **right** |
| G05 | James Royal relays WSJ: $350bn deal to finance OpenAI's chip purchases | v27 direct | same as e717 (and e719's $350bn) | update v27 | none | none; e717's "preliminary, could collapse" stays on the argument | no: the same WSJ report | the record drops e717's qualifier; the argument keeps it | repeat→e717 **right** |
| G06 | Drury: analysts expect NVIDIA to grow 43% next year (metric unstated) | v22 background (FY2028, a later period) | same as e1145 (same author, same figure, five days later) | update v22 (as background) | none | none | no: the author repeats his own relay of analysts | metric and period unstated here; e1145 states FY2028 revenue | repeat→e1145 **right** |
| G07 | NVIDIA blog: Nebius received its first Vera Rubin NVL72 in Finland | v6 lead; v11 lead | different from e336 (Tom's Hardware on the Noetra facility); related to e293 | update v6, v11 or background_only (rule F) | **none** | a first delivery to a named customer (Nebius); no size | no: NVIDIA's own statement | no size, no revenue; e336's "no deployment timeline" stays | replace→e336 **wrong**: a different statement about a different facility was retired |
| G08 | Cimino: first stand-alone CPU this fall; on track for $20bn CPU sales this year | v5 direct (management's $20bn) | same as e404/e549 ($20bn) and e22 (the author's own fall launch line) | update v5 | **none** | none | no: NVIDIA's figure via the same author | the "$20bn" is visibility/target, not revenue (e549) | replace→e505 **wrong**: WIRED's China-timing rumour is a different statement and was retired |
| G09 | NVIDIA rep to Tom's Hardware, 07-06: "Our roadmap is intact" | v6 lead (a denial of the delay reports) | different from e49–e55 (it contradicts them) | update v6 | **none** | NVIDIA's denial; no detail | yes: NVIDIA against SemiAnalysis | opposing: e49, e50, e51, e53; the denial addresses none of the specifics | replace→e53 **wrong**: a party's denial erased the contrary report |
| G10 | NY Post: NVIDIA and OpenAI announced up to $105bn financing toward the Ohio data center (08-17) | v25 direct (the announcement); v27 uncertain (financing "toward" the center, chips or lease not stated) | revision of e1165 (<$120bn rumour) and of e690's $250bn; different from e712 | update v25 (and v27 as uncertain) | e1165 (status: rumour → announced) | the announced amount and party statement; whether it is the lease/debt guarantee v25 asks about is not stated | yes: the companies' announcement | the record does not say which instrument; keep e690/e1165 as history | replace→e1165 **right** (a revision), with the instrument left open |
| G11 | StockStory relays JPMorgan: SpaceX to absorb a "very significant percentage" of 2027 GPU shipments | v22 lead; v6 lead; v11 lead | same claim as e956 (Musk's remark), new claimant (JPMorgan) | update v22, v6, v11 | none | a bank repeats the customer's own remark; no quantity | no: rests on Musk's statement | not corroboration | new **wrong as support**: stored as a second independent piece |
| G12 | AI Magazine: OpenAI committed to ~8 GW-IT at PORTS-Pike, NVIDIA exclusive provider (08-18) | v6 lead; v11 lead | same as e1195 (NVIDIA's 08-17 release); related to e1194 | update v6, v11 | none | none | no: restates NVIDIA's release | — | new **wrong**: a duplicate of e1195 stored as new |
| G13 | Frenette: Huang confirmed Vera Rubin faces no production delays, massive volumes | v6 lead; v11 lead | same as e293 | update v6, v11 | none | none | no: Huang's 07-15 remark relayed | the author's "confirmed" adds nothing | new **wrong**: a duplicate of e293 stored as new |
| G14 | NVIDIA blog: Vera Rubin trains the largest models with one-fourth the GPUs of Blackwell | v6 lead (efficiency claim; direction for revenue ambiguous) | different (e308 is Drury's cost-advantage summary, not this claim) | update v6 or background_only (rule F) | none | a 4x GPU-efficiency claim: fewer GPUs per model against a higher price per rack (e294) | no: vendor claim | direction ambiguous; vendor figure | new **right** |
| G15 | Quartz relays Bloomberg: early-2027 price rises on some Vera Rubin/Grace Blackwell systems, rate varies by generation and memory | v14 direct (pricing); v11 lead | same as e1365 + e1369 (one Bloomberg report, two halves) | update v14, v11 | none | none | no: the same Bloomberg report | unnamed sources (rumour) | new **wrong**: a duplicate of e1365/e1369 stored as new |
| G16 | Saxo's Dalfovo: demand may grow enough for NVIDIA and alternatives to expand together; revenue can rise as share falls | v11 background; v22 background | different | update v11, v22 (a qualification of the competition argument) | none | share loss need not mean revenue decline if the market grows faster | yes: an independent strategist | opposing: e376, e1032 (share-loss bearish views); no figures | new **right** |
| G17 | Royal: OpenAI 2025 operating loss $20.9bn, est. $7bn loss in Q1 2026 | v27 background; v25 background (customer credit risk) | different from e724 (same theme, no figures) | update v25, v27 | none | the loss figures | yes: independent of NVIDIA and of e724 | the figures' source is not named; bears on risk, not on whether the agreement is signed | new **right** |
| G18 | Rasgon (Bernstein): the financing program has headlines and big numbers, few operational details | v38 background | same observation as e1081 (CTech: terms, commitments, timetable undisclosed), new claimant | update v38 | none | a named analyst's endorsement of e1081's observation; no new fact | partly: a different claimant of the same observation | not new support for "few details" | new **acceptable as a source, wrong as support** |
| G19 | candidate: binding non-exclusive license for Poolside's Model Factory (~$6bn), folds_into v44 | v44 lead | — | update v44 | none | the deal's structure: equity stake plus a $6bn license, from one announcement | no: one Poolside deal | not an independent investment judgement: one deal, two legal forms, settled by the same announcement | candidate new **wrong**: a part of v44's deal opened as its own question |
| G20 | candidate: NVIDIA's reported investment in xAI's January 2026 round (portfolio's No. 2 holding) | no existing question | — | propose_new only with an `independent_judgement` naming NVIDIA's investment exposure/circularity; else unresolved or background_only (rule G) | — | a material stake in a customer with no question in the catalog | yes | the candidate's yes/no wording is not an investment judgement | candidate new **wrong as phrased**: the stake matters, the question form does not carry the judgement |
| G21 | candidate theme: combined Big Tech AI outlays 2026 (>$730bn est.), merged by key into v3 (four hyperscalers' DC capex) | v3 direct (another estimate of the theme's quantity) | different population (all Big Tech, all AI outlays) | update v3 (merge) | none | a broader-population estimate | yes: Reuters | the population and measure differ; the argument must keep the label "Big Tech total AI outlays", not read $730bn as the four-company DC figure | merge→v3 **right**, the population label must survive |
| H01 | Duprey relays leaked Liang Wenfeng: DeepSeek expects large batches of NVIDIA systems in coming months; Huawei capacity limited | v6 lead (China demand resuming); v11 lead; v22 lead | different from e623/e625 (other remarks of the same leak); same leak as e613/e614 | update v6, v11, v22 | none | expected China shipments to DeepSeek; Huawei capacity limit | no: the same leaked transcript as e613/e614 | leaked, unverified, relayed; upside against e200/e37 (guidance excludes China) | new **right** |
| H02 | Eurogamer: May's price rise hit only 5090-class GPUs; July's affects a wider range | v14 lead (small); v11 background | the May part same as e606; the wider July scope different | update v14 | none | the July rise's wider scope | no: relays the BenchLife/VideoCardz chain | consumer GPUs are a small share of revenue | new **right** |
| H03 | BNN/Reuters: BMS said it will be the first life-sciences company to buy a Vera Rubin DGX SuperPOD | v6 lead | same as e420/e401 | update v6 | none | the "first in life sciences" claim only | no: BMS's announcement relayed | no size | repeat→e420 **right** |

Control (the product's stored decisions) against this gold: right on 14 of 24 (G01–G06, G10, G14, G16, G17, G20, G21,
H01–H03 minus the two "wrong as support" rows counted as half: G11 and G18), wrong on 7: three replacements that retired
a different statement (G07, G08, G09: one of them a party's denial erasing the contrary report), three duplicates
stored as new (G12, G13, G15), one part of an existing deal opened as a new question (G19). The three replacement errors
are the costliest class: they delete a qualification or a contrary report from what the judgement reads.

## What the gold does not establish

- It is one reader's judgement on 24 cases; a second reader's agreement is not measured. The three held-out cases say
  whether a prompt tuned on G01–G21 generalises, not whether the gold is right.
- Text fields (`new_information`, `limitations`) are scored by reading against the gold's wording, not by string
  match; `action`, `replaces`, `independent` and the two step-3 relations are scored exactly.
- The 24 cases are weighted by stake, not count: a wrong `replaces` on a contrary report (G09) costs more than a
  duplicate stored as new (G12), because it changes what the judgement can see.
