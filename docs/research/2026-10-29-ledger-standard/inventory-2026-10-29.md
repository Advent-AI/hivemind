# Inventory of definitions in force (2026-10-29, read-only subagent; leads, verified where the standard relies on them)

Sources: worktree `hivemind-extraction-quality-2026-10-28`; `research_notes/对冲基金论点粒度与金标/codex-challenger.md` and `reports/对冲基金论点粒度与金标.md` from the main repo. DEC = docs/DECISIONS.md; STD = docs/research/2026-10-29-analyst-standard/standard.md; ROLE34 = src/hivemind/prompts/role-v34.txt.
Verified by Claude before use: B17 (`extraction.py:673-677` compares the candidate's year with the publication calendar year + 1), B15 (`check_ladder` requires the asset labels), D191 point 4 (DEC, D191), `check.py` rules out only "thesis driver".

## A. Classification schemes (33)
A1 ledger and question: 1 old views structure (D26, replaced); 2 thesis library structure (06-views:28-39); 3 actual ledger tables (store.py:12-37; views has no opens_as/settled_by; evidence has tier only); 4 thesis kind asset/theme (06-views:45-48; vocabulary.py:8); 5 thesis shape numeric/event, measures and event types (extraction.py:109-117); 6 ladder five or two (vocabulary.py:14-15; D186 not implemented); 7 admission reason opens_as main_driver/industry_aggregate/policy_stage/binding_obligation (D184; D191 renamed shared_quantity, code uses it only v13-v15); 8 lifecycle open/closed (D57); 9 research group (D149/D165/D166); 10 thesis tree, seven driver classes (D208, design, not built); 11 shared-quantity identity (D197; identity.py:9-15); 12 theme block one to all (D191/D195); 13 candidate destination merge/succession/new/skip; 14 evidence comparison repeat/replace/new (D202/D204 change the writer); 15 Jev labels; 16 collision verdicts (D190); 17 step 3/4 gold fields (D201, research only); 18 subject kinds.
A2 evidence: 19 evidence tier fact/party_statement/third_party_view/rumour (the only stored evidence class); 20 four keep kinds (D199/D229); 21 reject list; 22 old weight core/colour; 23 weight four levels core/supporting/optional/exclude (D219/D229; evaluation only); 24 D212 M/C/J; 25 research use usable/conditional/lead/reject (D221; evaluation only); 26 three judgements apart (D228); 27 six meaning cells (D220); 28 scoring dimensions (gold v4/v5); 29 old structural cells; 30 drop attribution (D209); 31 answer grade (D226); 32 step-4 rules A-H (D201); 33 idea mapping tiers (D145).
A3 opening: 34 admission fields (folds_into, lost_if_folded removed by D211); 35 report §1 eight rules (D184 names them the standard); 36 challenger §1 eight rules (AGENTS §8); 37 standard §6 four tests (D229; not in prompt or code); 38 role v13 three tests (not adopted); 39 challenger verdicts; 40 admission gold (D188); 41 reference v2 question cells; 42 independent investment judgement (D201).

## B. Overlaps and conflicts (20)
B1 aggregate reason has three names and two definitions (D191 shared_quantity "a quantity or price outside any one company that several move on" vs code/ROLE34 industry_aggregate "one aggregate quantity for one calendar year").
B2 main_driver: annual quantity only (D184) vs also the product generation's launch or ship date (D236).
B3 binding obligation: per deal or programme (D210/D236/D238) vs rule G "twenty yes/no questions on individual equity stakes are one judgement" (D201).
B4 three sets of opening tests; neither prompt nor code applies them (D235).
B5 PRD 05 still requires folds_into / lost_if_folded and block 5 (removed by D211).
B6 evidence with no home: dropped (D42, D209) vs "记问题覆盖缺口，不记垃圾" (STD:88) and AGENTS §8.
B7 linking rules: 05-extraction "directly discussed" vs D199 "makes more or less likely" vs D207 narrow one-home; placement-narrow-v1 names NVIDIA (D237).
B8 weight three or four levels; who owns exclude; 档位 means weight and rung.
B9 four "no" classes (reject list, exclude, research-use reject, D212 J) plus "unrelated statements".
B10 same item classed differently: share-price moves (prompt reject / ruler optional), bare price targets (STD reject / T8 asks for them / results optional), restated known facts (STD not kept / reference optional / D204 stores repeats), Singapore (gold v5 excluded / D231 optional).
B11 themes to companies: dependency edges (01-universe:80) vs one to all (D191/D195) vs declared channels (D208, design).
B12 groups vs driver layer vs "研究组不能替代粒度筛选"; glossary rules out "thesis driver".
B13 06-views repeat/replace text predates D202/D204.
B14 a component: merge (06-views:175) vs distinct with its own drivers (collision-v1) vs another population is the same question (ROLE34:16).
B15 code forces asset labels vs D186 business-outcome rungs (not implemented).
B16 a reported announcement: fact (ROLE34:10, D238) vs tier follows who confirmed it / company statements about the future are party statements.
B17 code year horizon uses publication calendar year + 1, the rule uses fiscal years: NVIDIA FY2028 refused in mid-2026 (verified).
B18 "lead" and "background" carry several meanings.
B19 who folds a candidate: "by code afterwards" (ROLE34:1) vs Jev and the collision judge (D190/D211).
B20 AGENTS §8 names two standards; D229 makes STD the one ruler.

## C. Opening rules in force
Reasons ROLE34:14 (D184, D185, D210, D236, D238); settled_by; STD:94 rule; STD:98-101 tests; D201 "a new product, a new figure or a narrower scope alone does not open one"; D191 point 3 macro-only items. Ruled out: ROLE34:15, 17, 18; STD:105; 06-views:178; D231. Horizon: 06-views:76-77; D185 548 days; ROLE34:17, 27, 34; D233; D158. Code checks (extraction.py 474-486, 498-500, 566-614, 660-744): ladder shape and asset labels, quarterly regex (asset, not event), year horizon, due after item, admission shape, bounds, real periods, candidate without surviving evidence. Matching (views/matching.py): universe, open targets, key conflicts, twins, one successor. Fold: shared quantity by code (jev_matching 104-118), Jev threshold 0.5, collision judge (D190, collision-v1), groups by names (D166).

## D. Evidence in force
Keep rule STD:3, 31; ROLE34:5 walk. Keep kinds ROLE34:4 (STD:33-38 differs: kind 2 "或有名字", kind 3 unqualified). STD:40 forecasts, rumours etc. are evidence; D240. Reject list ROLE34:6, STD:42-52; boundaries STD:54; quote acceptance D236. Writing ROLE34:9-11; meaning STD:58-69. Three judgements STD:84-90. Weight STD:75-82 (not stored). Tiers 06-views:95-106 (writer rank writing.py:84). Research use D221 (evaluation only). Filing D207/D209.

## E. Undefined or ambiguous
1 no single list of ledger record types; 2 opens_as/settled_by not stored; 3 no mapping between kind, shape, opens_as and measure/event type; 4 boundaries of "policy process" and "financing" (litigation); 5 driver layer has no admission reason or seeding rule; 6 weight levels, storage, ownership; 7 research use vs weight; 8 tier of a reported announcement or plan; 9 which opening tests govern; 10 event due-date horizon and the fiscal next-year defect; 11 whether a component is the same question; 12 theme thesis vs shared quantity vs research group vs universe theme; 13 "opening reason" is a ruled-out word (glossary: admission reason); 14 PRDs 05 and 06 predate D202-D211 and D229-D240.
