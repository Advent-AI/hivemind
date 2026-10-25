# Blind review: gold labels and Jev matching

## 1. Ten-line summary

1. **The results do not yet establish that Jev is the better matching engine:** several gold labels and scoring rules change what the reported accuracy means. See sections 2–4.
2. **C v17/v22/v24 describe the same $250 billion guarantee; C v18/v21 describe the separate chip-financing arrangement.** The source explicitly distinguishes them. [C: `views` v17/v18/v21/v22/v24; `evidence` e148–e150/e182/e210/e223.]
3. **C v19 belongs with the Ohio project:** its source explicitly says Japan funds electricity “for the facility.” [C: `evidence` e151; `evidence_sources` id 194.]
4. **Company capex may join the capex group.** D165 prohibits company financial lines from founding groups by themselves, not from joining an appropriate existing group. [`docs/DECISIONS.md:2319`.]
5. **Vera CPU membership is now correctly optional; S v72/v89 still needs an uncertain label.** The latter source does not establish the claimed AI-only versus total-capex distinction. [GI:184–194,112; S: `evidence` e609/e766.]
6. **Four evidence labels clearly discard additional information; two more depend on whether the comparison unit includes the entire quoted table.** [EG:20,36–38,54,63.]
7. **Jev sees fewer possible targets than the existing matcher permits, and it loses information through short source excerpts.** [`src/hivemind/views/jev_matching.py:53,129,154`; `matching.py:295,410`.]
8. **A narrow abstention band around 0.5 would miss the recorded errors at 0.70 and 0.77.** [J2: `match_records` id 9; J1: `match_records` id 4.]
9. **The client has a reproducible cache-key defect:** changing option order changes the transmitted request but not its digest. [`src/hivemind/jev.py:29,72–75`.]
10. **The `tracks_a_matter` discrepancy is fixed in the current script, but its old omission survives in the stored results:** G v42 has no membership answers and is still excluded as “disputed.” [`scripts/jev_poc.py:87–93,316–322`; results:112,174.]

## Reading conventions and scope

File abbreviations:

| Abbreviation | File |
|---|---|
| GI | [grouping-identity-gold-2026-10-25.json](/Users/lchingen/hivemind/poc/eval/gold/grouping-identity-gold-2026-10-25.json) |
| EG | [evidence-decisions-seed-2026-10-25.json](/Users/lchingen/hivemind/poc/eval/gold/evidence-decisions-seed-2026-10-25.json) |
| IG | [idea-gold-2026-10-25.json](/Users/lchingen/hivemind/poc/eval/gold/idea-gold-2026-10-25.json) |
| Results | [Jev POC summary](/Users/lchingen/hivemind/poc/reports/2026-10-25-jev-poc/summary.md) |

Database abbreviations G/E/C/S use the four paths in the request. J1 and J2 mean `poc/data/english-jev-2026-10-25/` and `poc/data/english-jev2-2026-10-25/`. **I** means `poc/data/items-window-tags2-2026-10-24.sqlite`.

Below, **`G v13/e34`** identifies `G.views[view_id=v13]`, its `view_keys` row where present, and `G.evidence[evidence_id=e34]`. The provenance is the corresponding `evidence_links` row selected by those two IDs, then `evidence_sources` selected by evidence ID, then `I.items` selected by `input_id`. S has no `view_keys` table.

I read the 103 distinct theses relevant to the grouping request—G 32, E 45, C 20, S 6—and their initiating evidence and source passages. I also read all 65 incoming evidence decisions and their shown comparison pieces. The current grouping file contains 17 firm identity pairs, 46 required membership slots, 44 forbidden slots and six optional slots. These counts describe the **current file**, which differs from the labels embedded in the POC results. [GI:3–335; G/E/C/S: cited `views` and linked evidence below; G: `handovers` ids 3–7/10/12–14, `match_records` ids 2–6/9–12.]

## 2. Gold corrections

### 2.1 Grouping and identity corrections

These are changes I recommend to the **current** file, including its dispute descriptions.

| File and key | Current label | My label | Deciding text or reason |
|---|---|---|---|
| GI:125–130, identity C v19/v17 | `different` | **`related_not_same`** | “The electricity **for the facility** … is being funded separately by Japan…” Separate financing, same campus project. [C v19/e151; I `items[input_id=gnews:04f9b244186ad52647b6931e]`.] |
| GI:272–279, Ohio membership C v19 | `forbidden` | **`required`** | The same sentence explicitly connects the power investment to the facility. The group includes the Ohio campus, not only NVIDIA’s guarantee. [C v19/e151; GI:260.] |
| GI:347–352, C v18/v21 dispute | Unscored; v21 supposedly has the wrong source | **`same`** | Immediately after the $250 billion guarantee sentence: “Nvidia is separately discussing financing the accelerators going inside, which could run to another $350 billion.” That supports v21’s chip-financing question. [C v18/e150, v21/e182; I `items[input_id=gnews:9e7560cfe0a707f9c14c7071]`.] |
| GI:107–112, S v72/v89 | `part_of` | **Uncertain: `same` versus `part_of`** | v72 says “capital expenditure **on AI alone**”; v89 says “**AI hyperscaler capital expenditures**.” The latter never establishes expenditure on all uses. A strict subset is therefore unproved. [S v72/e609, v89/e766.] |
| GI:355–360, G v1/v20 dispute | Unscored | **`related_not_same` for the stored questions; not `part_of`** | “Top 5 cloud providers and hyperscalers” capex versus spending “to fund AI infrastructure” by tech giants. The texts do not establish identical populations or strict containment. Equal approximate totals are insufficient. [G v1/e11, v20/e115.] |
| GI:363–368, E v11/v19 dispute | Unscored; described as the same pair as G | **`related_not_same`; correct the explanation** | E v11’s initiating source says “hyperscale CapEx to exceed $1 trillion **by 2027**,” despite its 2026 key. E v19 says AI-infrastructure spending exceeds $700 billion “this year.” This is not the G source pair. [E v11/e34, v19/e124.] |
| GI:371–376, C v1/v16 dispute | Unscored | **`related_not_same` for the stored questions; not `part_of`** | Same population/scope uncertainty as G v1/v20: top-five total capex versus tech-giant AI-infrastructure spending. [C v1/e6, v16/e102.] |
| GI:117–122, S v86/v89 | `different` | **`related_not_same`** | The SpaceX article explicitly connects its buildout to NVIDIA’s AI-factory financing and the same demand cycle: “If SpaceX funding tightens or hyperscalers slow orders…” This supports a shared investment process, not membership in an established hyperscaler total. [S v86/e693/e696; I `items[input_id=gnews:484913e67532d3a806abf6a1]`.] |
| GI:227–230, capex E v35 | `optional` | **`required`** | “We expect FY ’27 capital expenditures will grow year-over-year given demand signals across our portfolio.” Growth of Microsoft’s capex directly tracks the defined capex cycle. [E v35/e261.] |
| GI:388–392, E v18 | Uncertain | **Required Rubin-rollout membership; do not equate its value with capex** | Its source identifies the SK partnership and first factory opening next year; the corresponding first-factory source explicitly says it deploys Vera Rubin. The $500 billion includes NVIDIA memory purchases and SK supercomputer purchases, so it is not simply a capex total. [E v18/e115–e117, v15/e55; I `items[input_id=gnews:99a1ba68b933cb3eeb687120]`.] |
| GI:332–335, E v56/v57 | “Each is its own matter” | **Same Helios deployment process; optional narrower subgroups** | “Anthropic will deploy … MI450 series GPUs **in Helios**.” Keep two theses, but do not require separate unrelated matters. [E v56/e449, v57/e450.] |
| GI:340–341, capex dispute | D165 excludes company capex from every group | **Remove this alleged conflict** | D165 expressly says “the lines may join a group another thesis founded.” [`docs/DECISIONS.md:2319`; `src/hivemind/views/groups.py:86–93`.] |
| GI:344, forbidden-list explanation | Reality Labs is necessarily a judge case | **Correct the classification** | `operating_loss` is in `FINANCIAL_LINES`. This also illustrates why a code shortcut must not define semantic gold. [`src/hivemind/extraction.py:93`; G v36/e294/e295, E v41/e325.] |

For G v1/v20 and C v1/v16, my proposed relationship concerns the **defined questions currently stored**. I cannot certify that the articles’ underlying estimates use different company populations. That remaining source ambiguity must not be turned into a claimed successful or failed identity decision.

### 2.2 Every identity pair: disposition

The following covers the currently labelled pairs and the pairs moved into `_disputes`.

| Pair or set | Verdict | Source-grounded explanation |
|---|---|---|
| S v16/v48 | **Keep `same`** | The first source explicitly says “The $20 billion is for standalone CPU”; the second is also Vera standalone CPU revenue. [S v16/e75/e76/e81, v48/e471.] |
| C v17/v22/v24—all three pairwise comparisons | **Keep `same`** | Guarantee, financial backstop and financing all refer to the reported $250 billion Ohio arrangement. They do not include the separately described $350 billion chip financing. [C v17/e148/e149, v22/e210, v24/e223/e224.] |
| C v18/v21 | **`same`** | Both concern the separate accelerator financing; v21’s supporting sentence was omitted from its stored quotation. [C v18/e150, v21/e182; source cited above.] |
| G v1/v20; C v1/v16 | **`related_not_same`, with population uncertainty recorded** | Total capex and AI-infrastructure expenditure are not established as one quantity or strict subsets. [G v1/e11, v20/e115; C v1/e6, v16/e102.] |
| E v11/v19 | **`related_not_same`** | Different source periods as well as unclear spending scope; repair v11’s source/key mismatch separately. [E v11/e34, v19/e124.] |
| E v19/v20 | **Keep `related_not_same`** | Infrastructure spending versus accelerator addressable market; neither establishes actual spending as a strict component of the other. [E v19/e124, v20/e174.] |
| C v17/v18 | **Keep `related_not_same`** | Lease/debt guarantee versus additional chip financing. [C v17/e149, v18/e150.] |
| C v18/v20 | **Keep `related_not_same`** | Financing an acquisition and the project’s total cost are different measures, even though the cost includes chips. [C v18/e150, v20/e161.] |
| S v1/v89 | **Keep `related_not_same`; do not certify succession from these texts alone** | 2026 top-five capex versus 2027 “AI hyperscaler” capex. Same cycle, but a constant population has not been established. [S v1/e6, v89/e766.] |
| E v5/v8 | **Keep `related_not_same`** | Distinct tax bases in their stored keys; equal guidance does not make GAAP and non-GAAP rates identical quantities. [E `view_keys` v5/v8; `evidence` e6/e11/e12.] |
| E v34/v35 | **Keep `related_not_same`** | Capex level versus capex growth. v34 also has a calendar/fiscal key mismatch. [E v34/e260, v35/e261.] |
| E v52/v54 | **Keep `related_not_same`** | Data-center revenue level versus growth. [E v52/e445, v54/e447.] |
| E v51/v59 | **Keep `related_not_same` as stored; succession unverified** | The keys describe different fiscal years/bases, but v59’s initiating release discusses the second half of 2026, not a clear FY2027 forecast. [E `view_keys` v51/v59; `evidence` e444/e453.] |
| E v12/v1 | **Keep `part_of`** | NVIDIA standalone CPU revenue is a component of NVIDIA total revenue for the corresponding period. [E v12/e27/e33, v1/e1.] |
| E v47/v42 | **Keep `part_of`** | Amazon North America is a segment of Amazon consolidated revenue. [E v47/e367, v42/e326.] |
| S v72/v89 | **Uncertain** | The source does not resolve AI-only versus all-use expenditure. [S v72/e609, v89/e766.] |
| S v86/v89 | **`related_not_same`** | Explicitly connected AI-investment cycle; no demonstrated subset relationship. [S v86/e693/e696, v89/e766.] |
| C v19/v17 | **`related_not_same`** | Power infrastructure and financing for the same Ohio campus. [C v19/e151, v17/e148/e149.] |

There is also a **document inconsistency**: the PRD’s merge row still permits “the same focus or a part of it,” whereas the gold prohibits merging strict components and D154 prohibits merging different quantities. For the keyed implementation, D154 governs; the broad PRD sentence should not be used to mark a component merge correct. [`docs/prd/06-views.md:175,180`; `docs/DECISIONS.md:2225–2230`; GI:133.]

### 2.3 Every required and forbidden membership

Except for the changes above, these labels hold. Evidence IDs below identify the underlying readings rather than merely repeating the gold’s assertions.

| Matter | Required memberships that hold | Forbidden memberships that hold |
|---|---|---|
| **Blackwell/Rubin rollout — G** | v4/e3; v5/e5/e6/e13; v18/e60/e61; v19/e62/e63. The last source explicitly names both Vera Rubin and Blackwell in the NAVER factory. | v21/e158–e168, developer tooling; v22/e195, RTX product; v2/e1/e3/e4, total revenue; v3/e2/e4, DC revenue; v6/e7, margin; v7/e8, opex; v8/e9, tax; v14/e50/e53, company reporting line. [GI:139–177.] |
| **Blackwell/Rubin rollout — E** | v6/e7; v15/e55; v16/e56/e57 with its full NAVER source; v61/e490/e491. **v61 uses Blackwell GB300**, which fits this group’s stated Blackwell/Rubin scope. | v22/e202, RTX; v1/e1/e3, total revenue; v2/e2, DC revenue; v3/e4, margin; v4/e5, opex; v5/e6 and v8/e11/e12, tax; v9/e19, Compute & Networking revenue. [GI:138,146–177.] |
| **Blackwell/Rubin rollout — C** | v7/e7; v13/e54/e55; v15/e87. | v19/e151, Ohio power financing; v23/e220, export policy. [GI:152–181.] |
| **Capex cycle — G** | v1/e11; v12/e38; v20/e115; v24/e232, Meta; v30/e239/e242, Microsoft; v39/e301/e302, Amazon; v42/e311, Alphabet. | v2/e1/e3/e4; v3/e2/e4; v32/e243/e244/e246–e249; v33/e245–e249; v36/e294/e295; v25/e233/e235; v26/e234. These are revenue, segment or loss quantities, not capex. [GI:199–240.] |
| **Capex cycle — E** | v11/e34; v19/e124; v23/e230; v28/e251; v34/e260; v44/e329; v49/e413; v50/e434. | v1/e1/e3; v2/e2; v25/e248; v26/e249; v41/e325; v29/e254/e256; v30/e255/e262. Same distinction. [GI:209–249.] |
| **Capex cycle — C** | v1/e6; v16/e102; v39/e289. | v17/e148/e149 and v19/e151 are specific Ohio financing components; v7/e7 is shipment timing. Their broad AI connection does not make them the hyperscaler capex aggregate. [GI:219–254.] |
| **Ohio financing/campus — C** | v17/e148/e149; v18/e150; v20/e161; v21/e182/e183; v22/e210; v24/e223/e224; v36/e269/e270. **Add v19/e151.** | Keep v1/e6 and v39/e289 forbidden: their quantities are industry aggregates, not this project. [GI:259–279.] |
| **China chip controls — G/E/C** | G v9/e10, v35/e285; E v7/e8, v24/e240, v39/e313, v40/e316; C v23/e220, v8/e8, v9/e15, v25/e226. These concern licensing, restrictions, China access or associated conditions. | G v2/e1/e3/e4, v3/e2/e4; E v17/e60, sugar tariff quota, and v1/e1/e3; C v1/e6 and v17/e148/e149. [GI:282–316.] |

**Optional memberships:** keep standalone Vera CPU G v13, E v12 and C v11 optional. A CPU can be part of the platform while its standalone revenue opportunity remains separately defined. Keep accelerator TAM E v20 optional for the capex cycle. Promote E v35 as above. Keep C v14 optional because its question concerns restrictions on Chinese models, while the source discusses potentially restricting access to chips. [G v13/e33/e34; E v12/e27/e33, v20/e174, v35/e261; C v11/e28/e29, v14/e68/e69; GI:184–194,225–230,317–320.]

**Separate company matters:** retain G v17 Intel restructuring, G v45 and E v48 Globalstar acquisition, G v15 notes offering, and E v46 Leo launch. Keep them out of Rubin and the hyperscaler capex group. E v56/v57 belong to the Helios process described above. [G v17/e59, v45/e340/e341, v15/e54–e56; E v48/e369, v46/e332, v56/e449, v57/e450; GI:323–335.]

### 2.4 The eleven C theses singled out in the request

The current file has already added all eleven. My dispositions are:

| C thesis | Disposition | Deciding source content |
|---|---|---|
| v1 | **Required capex** | Top-five cloud-provider/hyperscaler capex. [C v1/e6.] |
| v7 | **Required Rubin** | Rubin production shipments. [C v7/e7.] |
| v8 | **Required China controls** | H200 authorization and uncertainty over China imports. [C v8/e8.] |
| v9 | **Required China-controls process** | Replacement of the AI Diffusion export framework; record that its scope is global rather than exclusively China. [C v9/e15.] |
| v11 | **Optional Rubin** | “The 20 billion is for standalone CPU.” [C v11/e28/e29.] |
| v13 | **Required Rubin** | SK factory using Vera Rubin. [C v13/e54/e55.] |
| v14 | **Optional China controls** | Model restrictions and possible restrictions on access to US chips are connected, but not the same policy question. [C v14/e68/e69.] |
| v15 | **Required Rubin** | Blackwell/Rubin revenue opportunity through calendar 2027. Its stored period is erroneous; that does not remove the membership. [C v15/e87; `view_keys` v15.] |
| v16 | **Required capex** | Aggregate AI-infrastructure spending. [C v16/e102.] |
| v25 | **Required China controls** | Taiwan restrictions on chip exports/performance. [C v25/e226.] |
| v39 | **Required capex** | Hyperscaler data-center expenditure exceeding $1 trillion in 2027. [C v39/e289.] |

These additions are explicitly marked post-run in the file. They are useful corrections, not a fresh held-out validation. [GI:409.]

### 2.5 Evidence-decision corrections

The governing distinction is **same statement**, not “same headline number” or “same topic.” A new period, new fact or unresolved difference is new evidence. [`docs/prd/06-views.md:190–198`.]

| File/key | Current | My label | Incoming text versus what was shown |
|---|---|---|---|
| EG:20, `nvda-20260125.htm\|e1\|v2` | Repeat | **New** | Incoming explicitly reports FY2026/FY2025/FY2024 revenue of **$215.938/$130.497/$60.922 billion**. The target says only “Fiscal year revenue … $215.9 billion, up 65%.” FY2024 is additional information. [G `handovers` id 5/e1; `match_records` id 4, key e1\|v2; `evidence` e14, also shown e1/e3/e4/e17.] |
| EG:38, `q1fy27cfocommentary.htm\|e3\|v3` | Repeat | **New** | Incoming adds “driven by the ramp of our **Blackwell 300 products**” and demand for **InfiniBand, Spectrum-X and NVLink**. The shown current-quarter statement gives $75 billion and growth rates without those drivers. [G `handovers` id 12/e3; `match_records` id 10; `evidence` e36, other shown e15/e21/e2/e16/e4/e17.] |
| EG:54, `q1fy27pr.htm\|e5\|v7` | Repeat | **New** | Incoming says operating expenses **$7.621 billion**. The shown piece says “up 52%” and gives causes, not the expense amount. A growth percentage is not the amount. [G `handovers` id 13/e5; `match_records` id 11; `evidence` e45/e8/e18.] |
| EG:63, `nvda-20260426.htm\|e6\|v9` | Repeat | **New** | Incoming adds: “The license requires that the H200s go through an **inspection process in the United States prior to any shipment**.” The target contains only the 25% tariff sentence. [G `handovers` id 14/e6; `match_records` id 12; `evidence` e28, other shown e27/e10/e20.] |
| EG:8, `q4fy26cfocommentary.htm\|e5\|v2` | Uncertain repeat | **Settle repeat** | “Secured inventory and capacity … beyond the next several quarters” retells the same company’s inventory/supply commitments covering future demand into 2027. [G `handovers` id 3/e5; `match_records` id 2; `evidence` e4.] |
| EG:9, same incoming piece under v3 | Uncertain repeat | **Settle repeat** | Same comparison and source occasion. [G `handovers` id 3/e5; `match_records` id 2, key e5\|v3; `evidence` e4.] |
| EG:11, `q4fy26cfocommentary.htm\|e9\|v8` | Uncertain replace | **New under the uncertainty rule** | Incoming says **17–19%**; stored transcript says **7–19%**. A transcription error is plausible, but the supplied records do not prove a later correction or revision. Preserve both rather than silently choosing which source is wrong. [G `handovers` id 3/e9; `match_records` id 2; `evidence` e9.] |
| EG:18, `q4fy26pr.htm\|e7\|v5` | Uncertain new | **Settle new** | Incoming identifies AWS, Google Cloud, Azure and Oracle as early deployers. Shown pieces describe six chips, shipment timing and Meta—not those deployers. [G `handovers` id 4/e7; `match_records` id 3; `evidence` e5/e6/e13.] |
| EG:32, `truenorth:transcript:NVDA:2026-05-20\|e5\|v5` | Uncertain replace | **Settle replace** | “In the second half … **starting in Q3**” is a later, narrower account of the previously announced shipment event. [G `handovers` id 10/e5; `match_records` id 9; `evidence` e6/e26.] |

**Two additional labels need an explicit unit-of-comparison decision before they are firm gold.**

- **EG:36, Q1 CFO e1→v2:** the summary repeats the current-quarter result, but its quoted table also contains the previously unshown $44.062 billion prior-year quarter. [G `handovers` id 12/e1; `match_records` id 10; `evidence` e35/e1/e14/e32/e31/e3/e4/e17/e30.]
- **EG:37, Q1 CFO e2→v3:** the same issue applies to the table’s $39.112 billion prior-year DC revenue. [G `handovers` id 12/e2; `match_records` id 10; `evidence` e36/e15/e2/e21/e16/e4/e17.]

If the whole incoming stored piece is the unit, I would keep these as **new**; if only its stated current-quarter claim is the unit, **repeat** is defensible. Mark them uncertain in the benchmark until that distinction is fixed. Operationally, the PRD already says uncertainty means new. [`docs/prd/06-views.md:192,198`.]

I retain the other 54 currently firm labels. In particular:

- The 10-K shipment statement is not demonstrated to revise the earlier launch guidance, so **repeat** remains preferable to supersedes. [EG:22; G `handovers` id 5/e5; `evidence` e6.]
- Q1 gross margins **74.9%/75.0%** are **new**. The shown margin explanation does not contain those figures. [EG:53; G `handovers` id 13/e4; `evidence` e44/e22/e29/e7.]
- Q1 customer mix is **new**, not a replacement of Q4 customer mix. [EG:40; G `handovers` id 12/e4; `evidence` e16.]

### 2.6 Third gold file: idea gold

The title asks for three gold files; the numbered instructions name two. I therefore also reviewed the idea file’s 20 cases and the 59 referenced S theses. These are the clear corrections and unresolved bindings.

| File/key | Current | My disposition | Deciding text |
|---|---|---|---|
| IG:34–37, idea 5 | Rubin revenue binds directly to S v48 | **Remove direct binding; no verified exact direct thesis** | v48 is standalone Vera **CPU** revenue. “The closest quantity” is not the idea’s quantity under IG’s own direct definition. [IG:9,35; S v48/e471, v16/e76.] |
| IG:50–53, idea 9 | Falling H100 prices bind directly to S v46 | **Context, not direct** | v46 concerns the **maximum price reached at any point in 2026**, supported by a prediction of hitting $2.75/hour. That does not answer whether prices keep falling through the year. [S v46/e448.] |
| IG:74–77, idea 15 | AMD taking share binds directly to S v52 | **Context, not an exact share answer** | “More than double” AMD DC revenue is company growth. It does not establish market share or displacement of NVIDIA; the cited NVIDIA fiscal period is also not aligned automatically. [S v52/e480; S `views` v3/v52.] |
| IG:78–81, idea 16 | IC growth deceleration binds directly to S v30 | **Require an aligned growth comparison; current binding insufficient** | A FY2027 revenue level is not itself a comparison of FY2027 and FY2026 growth rates. [S v30/e288/e293/e294; IG:9.] |
| IG:42–45, idea 7 | Any listed capex view can answer a 2026→2027 decline | **Do not score decline until populations and spending scopes align** | Top-five total capex, AI-only capex and “AI hyperscaler” capex are mixed. [S v1/e6, v23/e255, v72/e609, v89/e766.] |
| IG:48, idea 8, trap v20 | Always a wrong direct quantity | **Uncertain, not a firm trap** | v20’s source describes industry giants funding AI infrastructure at $700 billion; v71 describes Big Tech AI expenditure at $730 billion. The file does not establish a different population or spending boundary. [S v20/e179, v71/e598.] |
| IG:21,25,37,49,61,65,69 | `>=` for “top/exceed/more than/over” | **Strict `>`; remove the incorrect v48 binding separately** | The wording in ideas 1/2/5/8/11/12/13 is strictly above the amount. Equality is a different boundary case. [IG:18,22,34,46,58,62,66.] |
| IG:29,33,73 | No claim for 73%, doubling or 1 GW | **Represent the stated numeric/relative claim, or explicitly exclude it from claim scoring** | These ideas contain measurable claims despite `claim: null`. [IG:14,26,30,70.] |

The missing Section 232 semiconductor and China-chip direct matches remain defensible: the tempting S policy theses concern metal derivatives or scrap allocation. [S v61/e524, v62/e525, v63/e526–e528; IG:86–93.]

## 3. Jev usage: defects and ranked improvements

### 3.1 What is sound

The typed API is a reasonable fit for bounded relationship questions. The engine returns the existing matching schema, and the normal checker and atomic writer still run. This is a useful integration boundary. [`src/hivemind/views/jev_matching.py:110–165`; `round.py:48,152`; `writing.py:87–100`.]

Appending a **stored group ID** to `group_refs` is accepted: `groups.plan` explicitly recognizes IDs in the existing group collection. It is not necessary to invent a local declaration for that group. [`src/hivemind/views/groups.py:86–89`.]

Using the piece’s **original statement day**, falling back to publication day, is the correct basic ordering source. The engine does this at `jev_matching.py:156`; the writer checks for older statements at `writing.py:215–218`.

### 3.2 Defects and material limitations

| Finding | Location | Consequence |
|---|---|---|
| **Candidate target universe is narrower than the checker’s universe.** | `jev_matching.py:129–130`; `matching.py:145–157,295` | Jev asks only about `candidate_lists`. The checker also accepts shown views. The early same-key branch and final truncation can omit otherwise legal targets. |
| **Evidence target universe is also narrower.** | `jev_matching.py:151–160`; `matching.py:400–410` | The generative matcher may use a target shown elsewhere in the request when it belongs to the destination thesis. Jev never asks those extra comparisons. |
| **The semantic context omits decisive material.** | `jev_matching.py:45–56,64–65`; `matching.py:184–188` | Candidate evidence is reduced to summaries; target keys are omitted; only the first in-force target quote is included, truncated to 300 characters. Incoming quotes are truncated to 600 characters. NAVER and the Ohio chip-financing example show why the omitted sentence matters. [G v19/e62/e63; C v21/e182.] |
| **Succession is simultaneously too strict and too permissive.** | `jev_matching.py:83–99`; PRD:176 | Exact normalized scope wording is required even for model-written scopes. Conversely, any later start date is accepted: the function does not establish the next annual period, non-overlap, or a closed-event continuation. It returns the first eligible candidate. |
| **No semantic succession or skip decision exists.** | `jev_matching.py:143–148`; PRD:176–178 | The engine can only derive succession from that key heuristic or open a new thesis. It cannot deliberately skip a broad/mixed or closed-same-period candidate. |
| **Dependency output is always empty.** | `jev_matching.py:148` | This removes a capability, not merely a prose explanation. |
| **Founder eligibility is reused as membership eligibility.** | `jev_matching.py:131`; `extraction.py:96–99`; D165:2319 | Company capex lines that may join existing groups never receive Jev membership questions. |
| **Membership provenance is wrong, and merged candidates lose added memberships.** | `groups.py:83–89`; `writing.py:116–117,133–147` | Appended Jev IDs are stored as `basis='model'`, despite the plan’s `basis=jev`. Only newly created/succeeding theses enter the group plan; a merged candidate adds nothing. [`rerank-grouping-plan.md:107`; PRD:397.] |
| **The second pass does not reunite every destination of a mixed-linked piece.** | `matching.py:159–164`; `round.py:132–145`; `writing.py:180–211` | Direct links are compared first; merged-candidate links later. A repeat chosen in either set can govern the entire piece, although the comparisons were separated. The PRD requires waiting and comparing all destinations together. [PRD:195.] |
| **Repeat wins mechanically over replacement and all new information.** | `jev_matching.py:159–161`; `writing.py:203–211` | One repeat above threshold can defeat a stronger replacement, and the writer then stores no incoming text. This magnifies a single mistaken “same” decision across every linked thesis. |
| **Option-order changes collide in the cache.** | `jev.py:29,72–78` | The request digest sorts object keys; transmission preserves insertion order. Two option permutations can reuse one answer despite different transmitted ordering. |
| **Choice probabilities are not validated as probabilities.** | `jev.py:62–65` | I passed `{same: 2, new: -1}` to `validate`; it returned no problems. Numeric types, finite values, bounds and any required distribution consistency need checking. No malformed vendor response was observed; this is a client-validation defect. |
| **A multi-call decision is not fully linked to its archive records.** | `jev_matching.py:123–125,164`; `round.py:49–52` | `call_id` identifies only the last call; the stored digest is a digest of digests, not an archived request. Individual calls exist, but there is no explicit ordered call-ID list for the match. |

**The “lost succession” is not automatically an error.** G actually stores v12→v1, but its predecessor is top-five 2026 capex and its successor is broader 2027 hyperscale capex. The source must establish continuity of the population before that edge becomes gold. Do not fix this by allowing arbitrary scope changes. [G `successions` id 1; G v1/e11, v12/e38.]

**The dependency baseline is one written edge, not two.** G has `dependencies` id 1, v18→v5. A second proposal appears in `match_records` id 8, but that attempt was refused; id 15 contains the accepted dependency. The build log’s “wrote 2 dependencies” conflates proposals with stored edges. [G `dependencies` id 1; `match_records` ids 8/15; `docs/research/2026-10-25-english/build-log.md:97`.]

### 3.3 Ranked improvements and the measurements needed

The ranking below prioritizes preserved information and valid week-level results before latency.

| Rank | Improvement | Expected effect and decisive measurement |
|---|---|---|
| **1** | **Compare complete eligible evidence sets using shared state per `(item, thesis)`.** Put stored pieces in state once; ask a target `choice` per incoming piece with stored IDs plus `none`, then classify/confirm the selected relation. | In the latest first-pass record per input, G has **556 comparison lists; 387 omit at least one in-force piece**. The listed sets total 4,668 entries versus 25,950 in full historical sets; the largest set is 138. Measure target recall, false repeats, false replacements, retained novel facts, tokens and elapsed time. These are exposure counts, not 387 proven mistakes. [G `match_records` ids 1–145, latest `call_no` 1/2 per input; `evidence_links` and `replacements` filtered to `seq < match.seq`.] |
| **2** | **Require whole-statement equivalence for destructive repeat decisions, with calibrated abstention/fallback.** Supply the distinguishing facts and resolved dates rather than only a headline. | Directly addresses the gross-margin error and the four firm gold corrections above. Measure how many genuinely new facts survive in `evidence`, not only agreement with match labels. [G `handovers` ids 5/12/13/14; J2 `match_records` ids 4/9.] |
| **3** | **Use the same legal target universe as the checker, and apply key exclusions before selection.** | Four G first-pass decisions choose targets outside their own evidence shortlist: id 90 e3→v4 targets e148; id 107 e3→v3 targets e81; id 128 e6→v3 targets e81; id 140 e4→v2 targets e216. Measure recovery of valid targets and false-target rate. These demonstrate an opportunity unavailable to the current Jev questions; they do not prove all four decisions are semantically correct. [G `match_records` ids 90/107/128/140.] |
| **4** | **Separate group founding from joining; give membership questions adequate source context.** | Restores evaluation of the seven company-capex slots G v24/v30/v39/v42 and E v28/v34/v44, and tests the missed NAVER connection. Measure every required/forbidden membership independently, including multiple memberships—not just the best group. [GI:199–217; G v19/e63; E v16 source.] |
| **5** | **Ask semantic succession and dependency questions only after legal candidates are identified.** | The control contains three written succession edges and one dependency edge. Measure those edge types separately from new/merge counts, including invalid added edges. [G `successions` ids 1–3; `dependencies` id 1.] |
| **6** | **Fix cache identity, archive linkage and response validation.** | Prevents invalid reuse and makes permutation/fallback experiments auditable. Measure cache hits by exact request representation, trace completeness, and rejection of malformed replies. No week-level accuracy gain is established yet. [`jev.py:29,62–78`; `jev_matching.py:123–125,164`.] |

The batching opportunity is concrete but is not a measured speedup: those same 134 selected G input records contain **398 distinct incoming-piece calls versus 272 distinct item/thesis groups**—126 fewer outer requests, about 31.7%, before confirmation calls and chunking. A naïve all-pairs scan would substantially increase comparison volume, so elapsed time and billed tokens must be measured rather than inferred from request count. [Same G `match_records` selection as rank 1.]

Under the supplied API shape, `choice` supports 255 options: **254 stored pieces plus `none`**. The largest reconstructed G set, 138, fits that option limit. A combined `repeat:<id>`/`replace:<id>` option scheme fits only 127 stored pieces and would already need chunking here. A two-stage find-and-confirm design avoids that restriction and separates retrieval from the decision to discard or supersede information. This is API-shape reasoning; I did not fetch or verify the vendor recipe.

Do not let IDs carry the meaning: each option must be associated with the actual stored text. Test reordered options because first-option bias is documented in the repository’s account of Jev 1.13; that is a hypothesis to test for 1.14, not proof that 1.14 has the same bias. [`docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:22,28`.]

### 3.4 Thresholds and fallback

A band such as **0.40–0.60** would route the earlier near-threshold cases, but **would not route either 0.70 or 0.77**. The corrected-criteria run still gives the shipment supersedes decision 0.73. [J1 `match_records` id 4; J2 `match_records` ids 4/9.]

The earlier “0.51 just under threshold” explanation is inaccurate: in the archived comparison, **0.51 is the probability of `different`**, while `same_statement` is 0.48. Lowering a threshold does not turn a different argmax into same under the current rule. [J1 `model_calls` call_id 590; `jev_matching.py:159`; build-log:98.]

The old cascade’s stated **confidence ≥0.95** is not probability ≥0.95. With three choices, the documented formula corresponds to approximately **p≥0.9667**. That would route all these examples, but it does not prove the generative fallback would correct them. The control itself disagrees with some labels. Measure paired fallback accuracy, retained information and fallback rate on a source-corrected held-out set. [`rerank-grouping-plan.md:27–30`; G `match_records` ids 4/11.]

### 3.5 Dependencies, dates, cache and failures

- **Dependencies are expressible without generated prose.** A `noul` per candidate/shown-thesis pair can ask whether the required dependency exists; a direction `choice` can use the existing four allowed directions. Preserve the checker’s self-edge, candidate-resolution and cycle checks. Waiting for a future period also needs the existing chain/year fields; a direction question alone cannot supply that state. [`matching.py:45–48,353–395`; `vocabulary.py:13`.]
- **Statement date is correctly sourced but incompletely presented.** `said_day` uses the original day or publication day, yet `piece_state` shows only the unfilled original day. Several seed pieces therefore ask Jev a temporal question with a blank date while code later supplies a date. Resolve that value before asking. Do not substitute the event’s date or fiscal period for the statement date. [`jev_matching.py:64–65,156`; G `handovers` ids 3/5/10/13.]
- **Same-day replacement is currently permitted.** The writer rejects only strictly older dates. This may be necessary for a genuine same-day correction, but date equality cannot establish that a correction happened. The February shipment example has no such revision evidence. [`writing.py:215–223`; G `handovers` id 5/e5; J1/J2 `match_records` id 4.]
- **Archive reuse is appropriate for deterministic replay and crash recovery.** It is wrong when a caller intends a fresh statistical replicate, an option-order experiment, or a fresh response from a changed unpinned model alias. Cached answers also bypass current response validation. [`jev.py:71–83`; `model.py:72–85`.]
- **Failure behavior matches the stated transport policy:** one retry after two seconds for HTTP 429/529; other HTTP/network errors fail the item. The outer matching step catches exceptions. Jev gets one semantic attempt, although its failure is misleadingly labelled “refused twice.” [`jev.py:17,27–46`; `round.py:39–56`.]
- **Partial multi-call costs can disappear from the item result:** if a later internal Jev request fails, `_match` exits before adding the returned aggregate cost. Earlier successful calls remain in the archive, so account from archive records as well. [`jev_matching.py:116–125`; `round.py:42–46`.]

## 4. Scoring fairness

### 4.1 Evidence scorer

I reproduced the current script’s reported scores: **G 53/60, J1 50/60, J2 58/60**, each with zero missing decisions and zero wrong-target classifications. G’s seven failures are classified by this script as wrong **kind**, not a wrong-target category. [EG:4–68; G/J1/J2 `match_records` first-pass decisions; `scripts/score_evidence_gold.py:50–69`.]

Those numbers are reproducible, but the following prevent treating them as final comparative quality:

1. **It scores proposals rather than verified writes.** It reads `decisions_json` without checking refusals or successful `processing_steps`. A failed proposal can count. [`score_evidence_gold.py:18–31`.]
2. **Missing decisions leave the denominator.** That can reward an arm that fails or omits difficult cases. Report coverage and a fixed-denominator result alongside accuracy on completed cases. [`score_evidence_gold.py:50–53,65`.]
3. **Targets are accepted by substring.** A string such as `68%` or `25%` does not establish the same quantity, period, speaker or in-force status. [`score_evidence_gold.py:59`; EG:21,63.]
4. **Second-pass decisions are omitted.** Only call numbers 1 and 2 are considered. G has second-pass records 62, 84, 109, 120 and 139, each call number 3. [`score_evidence_gold.py:22–23`; G `match_records` cited IDs.]
5. **The key assumes stable view IDs across arms.** It is `(short input name, incoming evidence ID, view ID)`. That is workable for the aligned seed, but diverging new/merge/succession histories can make the same view ID mean different things later. [`score_evidence_gold.py:24–31`.]
6. **Gold is conditional on G’s historical evidence state.** A different arm can legitimately have a different set of statements in force after an earlier decision. Score both a frozen common-state classification task and the resulting sequential ledger; do not silently mix them. [EG:2; G `match_records.shown_json`; `writing.py:203–229`.]
7. **One false repeat can erase information across several links, while the scorer counts each label independently.** The writer’s actual effect needs its own fidelity measure. [`writing.py:200–211`.]

The four firm corrections above are enough to invalidate “58/60 proves better” as presently stated. I have not presented a revised headline score because the comparison-unit ambiguity and different arm histories must first be resolved.

### 4.2 Grouping/identity scorer

| Issue | Evidence and effect |
|---|---|
| **The current `tracks_a_matter` function is fixed, but the recorded answers are not replenished.** | It now admits `kind == 'theme'`. Replaying the old measure-only predicate against G/E/C identifies **G v42 only** as the discrepancy: it is a theme thesis with measure `capex`. The results still show no membership answer for it. [`scripts/jev_poc.py:87–93`; G `views`/`view_keys` v42; Results:112,174.] |
| **`disputed` repeats the incorrect D165 interpretation.** | Every required financial-line thesis is excluded; the test does not exempt theme theses. Thus even the repaired v42 predicate cannot make v42 count. [`jev_poc.py:316–322`; D165:2319.] |
| **An identity dispute suppresses unrelated membership scoring.** | `_disputes` is matched only by ledger and view ID. C v18/v21’s disputed identity therefore removes their clear Ohio membership; G v1/v20 and E v11/v19 suffer the same leakage. [`jev_poc.py:319–320`; Results:20–24,59–61,104–108.] |
| **`gold_states` makes the measuring stick depend on the implementation shortcut.** | A required company-capex member is assigned `new` if `tracks_a_matter` is false. Semantic gold must not be rewritten to agree with which questions code asks. [`jev_poc.py:185–208`.] |
| **`unlabelled` depends on the arm’s prediction.** | The same C v19 is counted as wrong when Jev chooses the forbidden group but can be excluded when the control chooses new. Current results still have different denominators, 33/34 versus 20/33. [`jev_poc.py:325–334`; Results:18,23.] |
| **Founder exclusion is asymmetric.** | `judge` excludes founders under stored cards; `judge_control` does not make the corresponding exclusion. Current G stored results compare 31/31 against 35/35. [`jev_poc.py:347–348,378–399`; Results:129.] |
| **Explicit uncertain cases are not generally honored.** | G and E are declared fully labelled even though GI retains G v10/v31 and E v18/v21 under `uncertain`. These can become default-new gold. [`jev_poc.py:313,329`; GI:379–406.] |
| **A fused group can receive credit as either correct group.** | Stored g1 maps to both Rubin and capex; g2 and g4 both map to China controls. Required intersection is accepted before any forbidden intersection. This hides fused membership and fragmentation. [`jev_poc.py:337–340,356–364,388–395`.] |
| **The offline POC selects only one membership; the engine appends all above threshold.** | The SK example scores 0.96 Rubin and 0.58 capex. The POC selects Rubin; the engine would append both eligible groups. A best-group score is not evidence for the multi-membership engine. [`jev_poc.py:228–232`; `jev_matching.py:138–141`; Results:170.] |
| **Own-matter treatment differs between arms.** | Jev putting an own matter into another group can be wrong, while the control branch can set it aside as `own_matter`. Use one rule for both. [`jev_poc.py:365–372,392–398`.] |
| **Current and historical gold are mixed in one report.** | Membership scoring reads the current gold, but identity scoring uses the `gold` labels saved inside old results. Current GI has 17 firm pairs and S v72/v89 under `part_of`; Results still reports 20 pairs and calls that pair `related_not_same`. [`jev_poc.py:415,485–497`; GI:107–112; Results:184,191.] |
| **Repeatability checks only the three-state label.** | Changing the target group, target thesis or raw relation can remain “identical” if both runs say grouped/dedup/new. [`jev_poc.py:429,463–466`; Results:145.] |
| **Snapshot scope is not enforced by the scorer.** | `Ledger` loads every current view; the scorer reloads current databases. GI’s E v61 cutoff note does not itself enforce a cutoff. [`jev_poc.py:72,419`; GI:134.] |

The current summary also differs from build-log row 33: for example, C now reports **33/34 versus 20/33**, while the log retains **27/29 versus 20/28**. That is consistent with post-run relabelling, but a reader needs an explicit result version and gold digest rather than two apparently comparable “final” figures. [Results:18; build-log:96; GI:409.]

**Fair comparison rule:** select the same source-labelled cases before seeing either arm’s prediction; score every required and forbidden membership separately; distinguish raw answer, checked decision and committed result; and bind each result to its gold version, database cutoff and request representation. This is also the structure proposed in the repository’s snapshot plan. [`rerank-grouping-plan.md:72–77`.]

## 5. What I could not verify

- **Vendor behavior and live API limits:** I made no web requests or model calls. The semantic-find proposal is reasoning from the supplied API shape. Current calibration, first-option bias in 1.14, retry recovery and actual latency improvements remain unmeasured.
- **A complete Jev week comparison:** J1 ends at handover sequence 20. J2 advanced during this review and was at sequence 146 on the final read. I therefore do not claim a frozen, completed week result. [J1/J2 `handovers`, maximum `seq` 20/146.]
- **The original tax-rate utterance:** the stored transcript and filing disagree. Without an authoritative correction or audio, “transcription error” remains an inference. [G `evidence` e9; `handovers` id 3/e9.]
- **The population behind ambiguous capex estimates:** the stored articles do not establish identical company sets or the inclusion of non-AI spending for G v1/v20 and S v72/v89.
- **External truth of stored articles:** this review checks labels against the supplied source text, not whether the articles’ claims are true in the world.
- **A saved output file:** this session permits filesystem reads only, and no output path was supplied. I could not write the report to disk. No repository files or databases were changed.