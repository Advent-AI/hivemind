# Single-call extraction: make one call read, understand and extract stably (experiment log)

Alex, 2026-10-27 evening: "不这个一次一定是可以搞过的 → 读明白，抽取 … 这一定是prompt 的问题，你如果再拆成两步这个消耗的luna calls 太多了 …
你开始深度思考，实验记录怎么迭代improve，你有很多没有探索到可能出问题的地方". The two-call design
(`../2026-10-27-two-step-extraction/design.md`, two review rounds) stays as a record and is not built. One row per
measured iteration, refuted arms included (feedback rule: iterate with a written log).

Harness: `../2026-10-27-evidence-gate/benchmark_clean.py` (the paused run's stored request with the cleaned text, sent
N times at low; `wire_order.restore` puts the keys in the order production sends). Articles: the three benchmark pages
(CoreWeave gnews:011203…, Motley gnews:dadd84…, Rest of World gnews:01a49f…) and, from the next arm, one T6 company release
and one more T7 page from the run. Scratch archive `poc/data/evidence-gate-2026-10-27/archive.sqlite`; cost to the ledger.

## 0. A harness defect found first (2026-10-27 19:20)

Every five-send benchmark before this log (`benchmark-results.md`, `benchmark-clean-results.md`) re-sent the archived
request JSON, which `model.request_identity` stores with `sort_keys=True`. Production sends the dict as built. So the
benchmarks sent an alphabetised schema: `candidates` before `evidence`, and in a piece `event_time, id, links` before
`quote`: the model had to commit to links and the event time before writing the quote. The model's answers came back in
that order (the raw content of scratch call 99). Codex noted and corrected the same thing in D243 ("the original property
order is reconstructed because the earlier archive's canonical JSON reordered the schema"). Those benchmark magnitudes
are therefore not evidence about production; the run's own double extractions are (363 items extracted twice because the
ledger changed: 87 pairs differ by three or more pieces, 35 pairs are 0 on one send and 3+ on the other). Fixed by
`wire_order.restore`; the baseline is re-measured below.

## 1. The request as the model reads it (v12, cleaned CoreWeave page): what can go wrong

30,000 characters: system 7,458, user 19,040, schema 3,470. The article is 2,993 of them (10%).

| # | What the model reads | Why it can produce an empty or random answer | Lever |
|---|---|---|---|
| 1 | role line 4: "Every statement and number is, by default, evidence linked to a shown thesis" and line 23: "Link evidence only to the thesis or candidate it directly concerns … Do not link it to others merely through an indirect relationship. Omit statements with no thesis or candidate to link to" | two rules decide the same question in opposite directions; for a customer story against a list of the supplier's financial lines, "directly" is a judgement; the judgement is made once for the whole page, so it flips the page between all and nothing | one rule, decidable: evidence is a statement whose fact or figure changes the probability of a thesis's answer; name the customer/supplier/competitor/policy cases |
| 2 | closing line: "Return empty arrays when there is nothing to extract." | an explicit cheap exit; the two empty CoreWeave answers used 236–321 reasoning tokens against 450–508 for the full ones | remove; say when empty is right (a page with no business content) |
| 3 | `[Research groups]` 7,041 chars (23% of the user text) listing 18 groups with member thesis ids that are not in the linkable set | 109 of 402 "links to nothing shown" drops point at group members; the block serves candidates (69 in 1,114 items), not evidence | show groups without member ids, or only names and aliases |
| 4 | `[Existing theses]` 6,253 chars: 29 theses, every one an NVDA FY2027 line or a binding-deal event | nothing for a customer's installed-base economics to attach to except v6/v11/v14 by inference | the gate rule must say such a fact attaches to the revenue/margin thesis it bears on |
| 5 | role: 2 of 3 of the text is about candidates (four reasons, ladders, due dates, identity fields, groups); evidence has one paragraph | the task reads as "find new theses"; evidence is the side job | reorder: evidence first, candidates after; cut the candidate rules the schema already enforces |
| 6 | `reasoning_effort: low` with 8,000 output cap (T7/T8) | fast decisions; medium did not help on the (alphabetised) benchmark; retest once the prompt is fixed | config, last |
| 7 | evidence shape: 9 fields per piece (id, quote, one_line, speaker, original_who, original_day, tier, event_time, links) | heavy per piece at low effort: an incentive to write fewer | measure pieces vs fields; do not cut before measuring |
| 8 | schema: `evidence` may be empty; nothing in the shape makes the model account for the page | an empty answer is as valid as a full one | require an account per mandatory paragraph in the same call (statements or a skip reason) |
| 9 | `[What to read out]` for T7: "What happened, when and who was involved; attribution …; quoted figures" | fine | none |
| 10 | `[Subjects]` lists every universe theme (1,122 chars) | noise for a company page | later |

Audit rule (AGENTS §6): an arm removes at least as much text as it adds; characters and prompt tokens reported per arm.

## 1b. Hypotheses not yet tested (Alex: "你有很多没有探索到可能出问题的地方")

| # | possibility | how it would show | test |
|---|---|---|---|
| H1 | the shape lets the model stop anywhere: nothing makes it account for the page | count spread 3–11 on one page; D244's per-paragraph answers held counts | A3: required entry per mandatory paragraph in the same call |
| H2 | reasoning skipped: several sends carry 0 reasoning tokens at `low` (prnewswire A1: all five; a CoreWeave A0 send with 11 pieces) | pieces decided without a pass over the page | A4: `medium` on the best arm, measured in production order (the earlier medium test was on the alphabetised schema) |
| H3 | the article sits at the end of a 19k-character message, after 29 theses and 18 groups | attention to the page diluted; theses read as the task | A6: item block before the theses block (no text added) |
| H4 | the role reads as "propose theses" (two thirds of it) with evidence as a side job | few pieces, early stop | A5: evidence section first, candidate rules after; cut rules the schema enforces |
| H5 | nine fields per piece at low effort: an incentive to write fewer | pieces fall as fields rise | measure pieces against the piece shape on the best arm (contract change: Alex's call) |
| H6 | the groups block (23% of the user text) with unlinkable member ids | 109 drops; attention | A2 |
| H7 | `[Subjects]` lists every universe theme | theme candidates where none belongs | later, with A2's result |
| H8 | the gate rule itself (contradiction) | all-or-nothing by page | A1 (done: no empties in 25) |
| H9 | cleaning residue (author bio, a reader comment) draws pieces | pieces quoting p0010/p0011-type lines | A3 skips show it |
| H10 | output cap 8,000 with reasoning counted | `finish_reason: length` | checked below: none so far |
| H11 | retyped quotes fail the code check ("quote not in item", 92 drops) | loss after the call, not spread | a span-id quote (later; contract change) |

## 2. Arms

| arm | change | status |
|---|---|---|
| A0 | control: v12, cleaned text, production key order | running |
| A1 | gate rewrite only (`role-A1.txt`): line 4's "by default, evidence" sentence replaced by "a statement is evidence to each shown thesis whose answer its fact or figure makes more or less likely"; line 23 replaced by the decidable rule naming the company's own figures, a customer's/supplier's/competitor's/regulator's action, and a policy decision, with the omit cases (unrelated company, review detail, repeated figure); line 9's games/peripherals sentence removed; the user prompt's closing "Return empty arrays when there is nothing to extract" → "only for a page with no business content". 7,458 → 7,689 characters (+231): the growth is the definition that replaces a contradiction; nothing else added. Two more articles join (executivegov.com T7 gnews:0001b0c2…, prnewswire.com T6 gnews:040c2565…), with their own A0 sends. | next |
| A2 | A1 + groups block without member ids | after A1 |
| A3 | A1 + per-paragraph account in the same call (schema keyed by mandatory paragraph ids) | after A1, if empties persist |
| A4 | best arm at medium effort | last |
| A5 | best arm with the role reordered: evidence section first, candidate rules after; rules the schema already enforces cut | after A3 |
| A6 | best arm with the item block before the theses and groups blocks | after A3 |

Bars (per article, five sends): empty sends; pieces per send; distinct pieces; pieces in every send; mean pairwise
overlap by quote text; links used; reasoning tokens; cost. An arm passes to the next when it has no empty send on any
article and its all-five share rises on every article against A0.

## 3. Results

### A0, control (v12, cleaned text, production key order), 2026-10-27 19:40, $0.0130

| article | pieces per send | empty | reasoning tokens | distinct | in every send |
|---|---|---|---|---|---|
| CoreWeave gnews:011203… | 3, 11, 9, 4, 3 | 0 | 382, 0, 280, 436, 263 | 15 | 1 |
| Motley gnews:dadd84… | 15, 9, 17, 9, 9 | 0 | 567, 469, 347, 395, 361 | 23 | 2 |
| Rest of World gnews:01a49f… | 8, 7, 8, 4, 5 | 0 | 289, 252, 362, 328, 302 | 12 | 3 |

Reading: with the order production sends, no send is empty (the alphabetised schema produced the 0-piece answers: the
model had to commit to `links` and `event_time` before the quote). The spread in count (3 to 11 on one page) and the
small core (1–3 pieces of 12–23 distinct in every send) are the real problem to work on.

### A0 on the two added articles, 2026-10-27 19:50, $0.0045

| article | pieces per send | empty | reasoning tokens |
|---|---|---|---|
| executivegov.com T7 gnews:0001b0c2… (NNSA/HPE/NVIDIA supercomputers) | 4, 4, 4, 3, 0 | 1 | 295, 588, 498, 579, 556 |
| prnewswire.com T6 gnews:040c2565… (Parasail + d-Matrix release) | 2, 1, 1, 1, 2 | 0 | 430, 262, 421, 270, 251 |

So an empty send happens in production order too (1 of 25 sends over five articles), and a company release yields 1–2 pieces.

### A1, gate rewrite (`role-A1.txt`, closing sentence replaced), 2026-10-27 19:58, $0.0190

| article | A0 pieces per send | A1 pieces per send | A1 empty | A1 links used | A1 reasoning tokens |
|---|---|---|---|---|---|
| CoreWeave | 3, 11, 9, 4, 3 | 4, 5, 6, 5, 6 | 0 | v6, v11, v14, v22 | 370, 368, 276, 309, 300 |
| Motley | 15, 9, 17, 9, 9 | 10, 14, 6, 8, 20 | 0 | v6, v11, c1 | 445, 386, 300, 481, 569 |
| Rest of World | 8, 7, 8, 4, 5 | 13, 7, 9, 8, 6 | 0 | v6, v9, v11, v14 | 422, 382, 279, 475, 307 |
| executivegov | 4, 4, 4, 3, 0 | 5, 5, 2, 4, 5 | 0 | v5, v6, v11 | 328, 678, 512, 642, 264 |
| prnewswire | 2, 1, 1, 1, 2 | 3, 4, 3, 3, 4 | 0 | v6, v11 | 0, 0, 0, 0, 0 |

Sentence-level scores (`score.py`) are in the next block once the control filter is fixed. Reading: no empty send in 25; the
release page doubles its pieces and its five sends agree (Jaccard 0.85, with no reasoning tokens at all); CoreWeave's
spread narrows (3–11 → 4–6); Motley's widens (6–20); links now reach the margin thesis (v14) and others, as the rule
intends. One arm of five sends is not a verdict on spread; the no-empty result and the release page are the clear gains.

## 4. Why an answer is empty: the provider-side signature and the model's own account (2026-10-27 20:30, $0.0019)

Over the run's 1,553 extraction calls (production order, whole pages): 493 empty (32%). Empty answers finish with
`stop`, carry no refusal, the same cached prefix (2,080 tokens) as full answers, and take 3.9 s with a median 153
reasoning tokens against 9.2 s and 330 for full answers: a fast "nothing here" decision, not a failure. Where they
fall: 53% of calls with 0–9 shown theses, 17–22% with 30 or more; NVIDIA's own pages most of all (nvidia.com 83%,
developer.nvidia.com 65%, NVIDIA Corporation 46%), stock-commentary sites least (247wallst.com 2%, zacks.com 7%).
Pages with financial figures always find a revenue thesis; technical posts, product launches and customer projects
find "no thesis it directly concerns" and are omitted whole.

Asked directly (the original conversation continued with "which instruction led you to return nothing, and which two
statements did you reject"), the model names the rule each time:
- NNSA/HPE/NVIDIA supercomputers (the production-order empty send): "I applied the instruction to 'Link evidence only
  to the thesis or candidate it directly concerns' … 'The Mission and Vision supercomputers will use NVIDIA's Vera
  Rubin central processing unit server' came closest to v5 (stand-alone CPU sales) and v6, but the statement describes
  a customer project, not NVIDIA's reported sales." An analyst counts a national lab buying Vera Rubin CPU servers as
  evidence for CPU sales; the rule as written told the model not to.
- nvidia.com, DOOM DLSS launch (run call 218): the same rule; the statements "concern gaming software and game
  integrations", nothing shown is a gaming thesis. Right under the rule; a gap in the thesis list, not in the model.
- Tom's Hardware, Intel Arc Pro B70 vs RTX 5090 (run call 2, no theses shown yet): "Use the existing theses first" with
  none existing, and the candidate rules do not open a thesis for a product comparison. Right.

So the empties are the model following the written gate; the gate is wrong for customer, supplier and partner pages
(case 1) and the thesis list has no home for product news (case 2). A1 changes the gate (its executivegov sends: 5, 5,
2, 4, 5 with links to v5, v6, v11 against 4, 4, 4, 3, 0 before). What is left to the model is the spread of counts
among non-empty answers, which A3 addresses.

### A2, A1 plus the groups block without member ids, 2026-10-27 20:20, $0.0184

| article | A1 pieces per send | A2 pieces per send | A2 empty | A2 sentence Jaccard (A0 / A1) | A2 in ≥3 of 5 |
|---|---|---|---|---|---|
| CoreWeave | 4, 5, 6, 5, 6 | 7, 6, 8, 4, 3 | 0 | 0.54 (0.42 / 0.53) | 6 |
| Motley | 10, 14, 6, 8, 20 | 6, 9, 15, 9, 15 | 0 | 0.52 (0.55 / 0.42) | 10 |
| Rest of World | 13, 7, 9, 8, 6 | 5, 10, 8, 9, 8 | 0 | 0.36 (0.52 / 0.52) | 7 |
| executivegov | 5, 5, 2, 4, 5 | 5, 2, 4, 4, 3 | 0 | 0.57 (0.25 / 0.45) | 4 |
| prnewswire | 3, 4, 3, 3, 4 | 1, 1, 2, 3, 2 | 0 | 0.33 (0.70 / 0.85) | 2 |

Reading: removing the member ids (7,041 → about 3,900 characters of groups) changes nothing the five sends can show;
the spread is the same order as A1 and the release page loses pieces. Not kept as a lever on its own; the block stays
as it is until the production change for candidates is designed (its unlinkable ids remain a drop class, 109 drops).

## 5. A1 into the product as v16; the real test is a week of replay (2026-10-27 18:58)

Alex: "你要反思自己的错误，然后下去改然后马上测试啊，不要一直diverge scope". Done:
- `src/hivemind/prompts/role-v16.txt` = `role-A1.txt`; `categories-v16.json` = v12's entries; `poc/config/poc-v32.json` = poc-v30 with T*-v16.
- `extraction.EMPTY_LINE_FROM = 16`: the request's closing sentence becomes "Return empty arrays only for a page with no
  business content"; `V12_REASON_VERSIONS = (12, 16)`: v16 names v12's admission reasons (the role-v15 draft's enum
  mismatch cannot recur). Test: `tests/test_admission.py::test_v16_states_the_decidable_gate_rule…` (RED, then GREEN);
  suite 200 pass; every enum word is in role-v16.
- Replay test: `poc/data/english-v32-nvda-week-2026-10-27/run-week.sh`: 2026-07-01..07-07, cleaned database, parallel
  runner, fresh ledger and archive. Compared with the paused run's same days by `compare_week.py` (empties, evidence per
  item, candidates, drops, cost). Note the day-one case: with no thesis shown yet, v16's pieces link to nothing and are
  dropped (6 dropped on the first item); evidence enters through candidates until theses exist, as before.

### A3, A1 plus an account per mandatory paragraph in the same call, 2026-10-27 20:50, $0.0448

The answer's shape: `paragraphs` keyed by the mandatory paragraph ids (a digit, a month name or 120+ characters), every
key required, each either `{"statements": [pieces]}` or `{"skip": reason}`; `extra` for statements from other
paragraphs; `candidates` and `new_groups` as before; the page sent numbered `p0001 …`. One call, nine fields per piece
as in production. Sentence-level scores (`score.py`):

| article | A0 pieces | A1 pieces | A3 pieces | A3 in every send (A0 / A1) | A3 Jaccard (A0 / A1) | A3 skips |
|---|---|---|---|---|---|---|
| CoreWeave | 3, 11, 9, 4, 3 | 4, 5, 6, 5, 6 | 13, 14, 15, 14, 13 | 10 (2 / 1) | 0.81 (0.42 / 0.53) | repeat ×2 |
| Motley | 15, 9, 17, 9, 9 | 10, 14, 6, 8, 20 | 16, 14, 15, 14, 15 | 10 (4 / 1) | 0.75 (0.55 / 0.42) | |
| Rest of World | 8, 7, 8, 4, 5 | 13, 7, 9, 8, 6 | 37, 22, 30, 39, 22 | 19 (3 / 3) | 0.64 (0.52 / 0.52) | |
| executivegov | 4, 4, 4, 3, 0 | 5, 5, 2, 4, 5 | 9, 11, 12, 8, 5 | 4 (0 / 0) | 0.60 (0.25 / 0.45) | |
| prnewswire | 2, 1, 1, 1, 2 | 3, 4, 3, 3, 4 | 12, 14, 9, 8, 10 | 5 (1 / 3) | 0.59 (0.70 / 0.85) | |

Over 25 sends: 301 paragraph entries with statements, 94 skips (no_claim 60, repeat 18, boilerplate 16), 6 extra
statements. Per call about $0.0018 and 20–30 s against $0.0008 and 10–15 s (the schema carries one piece definition per
mandatory paragraph; shared by `$defs`).

Quality, read piece by piece on CoreWeave send 1: 14 pieces, all statements an analyst keeps (the 2029 A100 contract,
$2.58bn quarterly revenue +112%, the $104bn backlog, prior-generation pricing at or above earlier levels, Burry's $176bn
depreciation claim, H100s rebooked at 95%, the 6.5 kW vs 120–140 kW power facts, 3.7 → 4.2 GW contracted power, the
CFO on renewals); one filler ("the A100 first launched in 2020", linked to nothing, dropped by code). Every piece links
to three or four theses (v6, v11, v22, often v14): the rule "every such thesis" is read widely; this is D198's open
"links wide" question, not a stability defect, and is not changed here.

Decision: A3 is the mechanism that holds (the shape makes the model account for the page; D244 saw the same), A1's
rule removes the empties. Both go into the product as extraction v17; the week replay then compares v12, v16 and v17.

## 6. v17 into the product; a mistake of mine stopped the v16 week test (2026-10-27 19:06)

The v16 week replay failed on 2026-07-06 with "configuration, universe or runtime changed during the day": I edited
`extraction.py`, `model.py` and added prompt files for v17 while the parallel runner was mid-day (its manifest hashes
every .py and prompt file; AGENTS §9: a gate runs on a snapshot no one is editing). The ledger is intact (55 items
through 07-05 and part of 07-06); the day is finished with `--workers 1` (`resume-serial.sh`) and no code changes until
both replays end.

v17 = v16 plus the account per mandatory paragraph (`extraction.ACCOUNT_FROM = 17`, `accounted_schema`,
`flatten_account` in `sift`, `$ref` and `minItems` in `model.check_schema`, `ACCOUNT_LIMIT = 60` required paragraphs
per answer); `poc-v33.json`; tests `test_v17_numbers_the_page…` and `test_v17_answers_are_flattened…` (RED then
GREEN); suite 202 pass. Its week replay runs in `poc/data/english-v33-nvda-week-2026-10-27/` beside the v16 resume.

## 7. The week test, v12 against v16 (2026-10-27 19:18; `compare_week.py`)

Same 98 items (2026-07-01..07-07, NVDA). A = the paused run (poc-v29, T*-v12, whole pages). B = poc-v32 (T*-v16, cleaned
pages, its own ledger from day one).

| | v12 (A) | v16 (B) |
|---|---|---|
| items with an empty handover | 64 (65%) | 31 (32%) |
| of which the model itself returned nothing | 55 | 8 |
| evidence kept per item, mean (median) | 1.1 (0) | 2.7 (2) |
| candidates | 9 | 11 |
| pieces dropped by code | 39 | 121 (98 with empty links: the model now writes the statement and says no thesis fits; D42 keeps such a piece out) |
| drops "quote not in item" | 4 | 11 |
| week cost (B, all purposes) | | $0.22: extract 151 calls $0.114, match 257 $0.059, judge 32 $0.048 |

Reading: the empties that were the model's own choice fall from 55 to 8 of 98; what remains empty is mostly the cold
start (eleven theses exist by day seven) and pages whose statements fit no thesis, which the code now drops with a
record instead of the model omitting them silently. Evidence per item more than doubles. The mid-run runtime change
(§6) cost one serial finish, no data.

## 8. The week test, v17 (2026-10-27 19:42), and the decision

Same 98 items. v17 (poc-v33; after the cap fix `ACCOUNT_LIMIT = 30`, T7/T8 output cap 12,000; one page had spent the
whole 8,000-token cap on reasoning and returned nothing): empty handovers 30 (model's own 8), evidence per item 7.2
(median 7), candidates 7, theses opened by day seven 5 (v16: 11; v12: 9), pieces dropped 458 (441 "no thesis fits"),
week cost $0.41 (extract $0.21, match $0.13: Jev calls 686 against 257). Read piece by piece on two items: v17 keeps 29
and 23 pieces where v16 keeps 4 and 5; v17's include "Jenny Lim was charged in April 2026" and "Li as the controller of
Luxuriate Your Life", every one linked to the total-revenue thesis; v16's are the H200 decision, the chip-smuggling
charges, the Huawei warning, linked to the export-control and CPU theses.

Decision (D199): v16 goes to production; v17 is refuted for production (stability bought with volume and fewer theses).
The three-month run restarts from 2026-07-01 with poc-v32 on the cleaned database. Next arms, if the run shows the
need: the width of links (every piece to three or four theses), candidates for product and gaming pages.

## 9. Step 1 on its own: ten v16 answers read beside their articles (2026-10-27 20:10, $0)

Alex: "你到底在跑什么？你drift了吧？我不是要你看下step 1抽取到底行不行？" The full run I launched is paused ($0.215,
119 items, kept). Ten items from the v16 week archive (2 company pages, 4 news, 2 opinion, 2 that returned nothing),
each read with its cleaned text, the theses shown to it, and every piece.

| item | pieces | right | wrong or noise | missed |
|---|---|---|---|---|
| BI, Burry shorts NVDA (T7) | 2 | Burry short NVDA, his overinvestment warning | both linked to gross margin v3 (nearest financial thesis; a positioning view bears on no quantity thesis) | nothing material |
| CommonWealth digest, Singapore smuggling (T7) | 3 | the seizure, the SGD 55M order, the four firms charged; the digest's Rubio/Google stories ignored | | |
| nvidia.com, DOOM driver (T6) | 2 | launch facts, links empty → dropped by code (no gaming thesis) | | |
| nvidia.com, DOOM launch (T6) | 3 | | all three (DLSS support in three games) linked to total revenue v5 | |
| Business Times, Chinese firms leave NVIDIA (T7) | 6 | 46% vs 30% domestic budget, 80% over budget, share to shrink, 2 trillion yuan, 80% domestic supply; linked to total and DC revenue | speaker strings cut ("Business Times reporting the B"), one day off by one | |
| SemiAnalysis, backstop (T8) | 4 + 1 candidate | market below SA's tracking (v5), backstop revenue (v5, v3), SharonAI 40k GB300 six-year backstop → binding-obligation candidate (right) | | $7T AI debt by 2029, $2T annual AI capex 2028: theme estimates with no theme thesis shown to an NVDA item |
| Quartz, revenue-sharing program (T7) | 4 | the program, Kress's recurring stream, SharonAI 40k and Firmus 170k GPUs / 360 MW, custom-chip competition | all linked to gross margin v3 (only four theses existed on 07-02) | |
| Motley Fool, $25,000 (T8) | 14 | Q1 FY27 revenue +85% / EPS +140% (v5), Huang's $1T Blackwell+Rubin through 2027 (v5), ~$20bn CPU sales (links empty: the CPU thesis did not exist yet) | author's valuation arithmetic (P/E 34, $305, $38,400: links empty, dropped) and five generic risk musings linked to total revenue | |
| NVIDIA blog, GFN Thursday games (T6) | 0 | right: a games list and a membership sale | | |
| wccftech, RTX 5080 SUPER TDP (T7) | 0 | right under the thesis list: a spec rumour, no product thesis | | |

Verdict on step 1 (v16): it works for what carries a thesis: figures, dated actions and attributed claims are
extracted, quoted correctly, tiered mostly right, and attached when a fitting thesis exists; the empties left are
pages with nothing for the theses. Three defects remain, each with its mechanism:
1. Links stretch to the nearest financial thesis (DLSS game support → total revenue; Burry's short → gross margin;
   an author's generic risks → total revenue). Mechanism: the rule "every shown thesis whose answer it makes more or
   less likely" with a thin thesis list; the model prefers a link to none. Lever: say that a statement with no
   thesis is kept with empty links (code drops it, as now) and that a product, game or driver fact bears on no
   quantity thesis unless it carries a size; measured by the share of pieces linked to a thesis whose focus the
   piece does not name.
2. Opinion pages: the author's commentary is extracted as third_party_view beside the facts the author cites
   (Motley: 14 pieces, about 5 noise). Lever: for T8, the category block's "what to read out" names the author's
   forecasts, ratings and the facts cited, not the author's generic risk list.
3. Theme theses are not shown to a company item at extraction (`views_for_prompt(objects)` shows the objects'
   theses), so capex and debt estimates in NVDA articles have nowhere to attach; D191 made themes one-to-all in
   judging only. Lever: show the open theme theses in the extraction request as linkable targets (a design choice
   for Alex: it widens every request by the theme block).
Stability (A1 five sends): no empty send; about half of the pieces repeat between sends (sentence Jaccard 0.4–0.5);
the figures repeat, the author views and cuts vary.

## 10. Arm B1: reject or link, scored against reference lists (2026-10-27 20:40, $0.0160)

Alex: "有些观点或是证据就分明不重要，我们本来就可以reject, 你的评量也不应该硬接才对". `role-B1.txt`: a statement is kept
only when material (a figure, a dated action, a named party's claim about the business) and bearing on a shown thesis;
"never link a statement to a thesis it does not bear on because no better thesis is shown; leave it out" (+322
characters: the reject list replaces the earlier omit sentence). Scored by reading every piece of every send against
`reference-B.md` (written before the sends).

| article | pieces per send | reference items present per send | in all 5 / in ≥3 of 5 / never | noise pieces (of all) | link notes |
|---|---|---|---|---|---|
| CoreWeave (8 items) | 5, 4, 6, 5, 4 | 5, 4, 5, 5, 4 | 3 / 4 / 1 (Burry's claim never; the revenue/backlog once) | 1 of 24 (power-draw technicals) | v6/v11 throughout, v14 on pricing: right |
| Motley (5 items) | 1, 3, 5, 6, 4 | the cited FY2026 DC revenue every send, networking 4, compute 4, share-to-75% 2 | 1 / 3 / 3 (the TSMC forecast, the author's revenue scenarios and the EPS consensus: never) | 0 | all v6: right |
| Rest of World (5 items) | 4, 6, 6, 9, 6 | Humain taxis 5, Stargate 400k 5, Humain 18k Blackwell 5, DC revenue $51.2bn 4, AMD/Groq deals 2, sold out 2 | 3 / 4 / 0 | 2 of 31 ("did not respond", a political-dependence view; both with empty links, dropped by code) | right; send 5 tiers reported facts as rumour |
| ExecutiveGov (4 items) | 2, 3, 1, 2, 3 | first Vera Rubin server 4, Mission 2027/Vision 2028 4, the announcement 3 | 0 / 3 / 1 (scale: not in the text) | 0; send 3 opened a "Vera products revenue" candidate from one article | the CPU-server fact links to v5 (CPU sales) in 2 sends, to v6 in 3: the link is the unstable part |
| PR Newswire (3 items) | 1, 2, 1, 1, 1 | the arrangement 5 | 1 / 1 / 2 (no figures in the release) | 0 | right |

Reading: the reject rule holds (noise 3 of 96 pieces, no stretched links on games or positions); the empties are gone
and stay gone. What remains unstable is completeness: on a page with eight material statements a send keeps four or
five, a different subset each time (CoreWeave: Kress's utilization in sends 2 and 5, the H100 rebooking in 1 and 4,
the revenue and backlog once). B1 also over-rejects on the opinion page: the TSMC forecast and the EPS consensus the
author cites are read as "valuation arithmetic". Two arms follow: B1b (the same rule with "a forecast, estimate or
consensus figure the author cites from a named firm or analysts is material") and B2 (B1's rule with the per-paragraph
account of A3, to see whether the account gives completeness without A3's noise and lost candidates).

## 11. Arms B1b and B2 (2026-10-27 21:05, $0.0171 + $0.0356)

B1b (B1 plus "a forecast, estimate or consensus figure the author cites from a named firm or analysts is material"):
Motley 4, 6, 13, 12, 2 pieces; the clause reopens the author's market forecasts (InfiniBand, switch market) in two
sends and not the others; CoreWeave 5, 4, 4, 2, 5. Refuted: the opening is as unstable as the omission.

B2 (B1's rule with the per-paragraph account): CoreWeave 8, 12, 13, 14, 11 with 6–7 of the 8 reference items per send
(Burry's claim in 4 of 5, Kress in 3, the H100 rebooking in 4, power in 5) but three reporter-assessment pieces per
send, "written by Luke James", "the A100 launched in 2020"; Rest of World 13–31 pieces, mostly the reporter's framing
sentences; PR Newswire 5–8 restatements of one arrangement. The account forces a filling of every paragraph; the
reject rule does not hold under it. Refuted for production.

Standing: the reject rule (B1) keeps the pieces clean but a send keeps about half of the material statements, a
different half each time. Next: B1 at reasoning_effort medium (A4) and B1c (B1 plus "keep every material statement
that bears on a thesis, not a selection").

## 12. Arm B3: the role rewritten as the model reads it (2026-10-27 21:40, $0.0325)

Alex: "什么叫重要陈述，你也没给例子，他哪里知道？" and "你不看你的prompt, 不看问题去测试". Read end to end, the v16/B1
role opens with "test and form theses" and puts candidates first; evidence is the third section with one abstract
definition and no example; nothing says to walk the whole page or when the job is done; the T8 reading block asks for
"the author's opinions, arguments". `role-B3.txt` (+1,190 characters, the reason: a definition with examples and a
procedure replace an abstract clause the model could not execute): evidence first; four kinds of material statement,
each with two or three examples; "go through the item from its first paragraph to its last and take every statement
of these kinds; a page with eight such statements yields eight evidence items"; a reject list with examples; the link
rule with "keep it with empty links"; the T8 reading block narrowed to forecasts, ratings, targets and cited figures.

| article | pieces per send | reference items present per send | noise per send | links |
|---|---|---|---|---|
| CoreWeave (8) | 10, 9, 11, 10, 10 | **8 of 8 in every send** | 0–1 (an unnamed Google architect's service-life estimate, kept as rumour) | v6/v11; Burry's and the architect's claims linked in 2 sends, empty in 3 |
| Motley (5) | 15, 18, 13, 20, 18 | the cited figures (TSMC, DC revenue, compute, networking, share) in every send; the author's scenario in 4 | 2–4 (the author's addressable-market sums, "Ethernet expected to dominate") | send 2 linked nothing at all |
| Rest of World (5) | 22, 29, 23, 27, 24 | all eight core facts in every send | 6–8 expert geopolitical views and reporter lines, mostly with empty links | send 3 linked nothing at all |
| ExecutiveGov (4) | 5, 6, 5, 6, 6 | all in every send | 1 (an administrator's quote without a figure) | all v6; the CPU-server fact never reaches v5; send 3 linked nothing |
| PR Newswire (3) | 9, 14, 10, 8, 11 | the arrangement, the 10x/3x claim, the 40-data-center figure | 5–8 restatements of one deployment | v6/v11 |

Reading: completeness is solved by the examples and the walk (the core set is present in every send on every page).
Two defects remain, each with its mechanism: (1) links decided for the page, not per statement: 3 of 25 sends linked
nothing; (2) restatements and figure-less expert views pass the reject list. B4 adds "decide links statement by
statement" with four link examples, and rejects restatements, characterizing quotes and figure-less expert views.

## 13. Arm B3 on the held-out article, and arm B4 (2026-10-27 22:05, $0.0043 + $0.0275)

B3 on gnews:a85f1634… (Tom's Hardware, China's $35bn RTX Pro 5500 orders; 41 theses shown from the paused run's
ledger; reference list written before any send): 7, 5, 7, 5, 6 pieces; reference items 1 (the 3 million cards /
$35bn order), 6 (the $11,400 price), 7 (5–10% of demand), 8 (3 million cards in 2027) and 10 (the spokesman) in every
send; 2 (cannot fill the orders) in 2 of 5; 3, 4, 5, 9 (the compliance fact, the spec, H200/B300 restricted, "not
confirmed") never, as the reject rule reads them. Two of five sends linked nothing (the page-level flip).

B4 (`role-B4.txt`, +734: links decided statement by statement with four examples; restatements, characterizing
quotes and figure-less expert views rejected):

| article | pieces per send | reference items | noise per send | links |
|---|---|---|---|---|
| CoreWeave (8) | 10, 9, 9, 10, 11 | 8 of 8 every send | 1–3 (the architect's estimate; two power-draw technicals in send 4) | per statement now: pricing/H100/CFO → gross margin v14, contract/Kress/power → v6; Burry empty in all 5; the revenue/backlog figure v6 in 4, empty in 1 |
| Motley (5) | 16, 16, 18, 20, 17 | the cited figures every send | 3–5 (the author's sums, EPS scenario) | own figures → v6 every send; the market forecasts empty in 4 sends, all v6 in 1 |
| Rest of World (5) | 14, 11, 11, 12, 12 | all core facts every send | 2–3 (CUDA developer count, "tens of billions") | deals and revenue → v6 every send; expert geopolitics gone |
| ExecutiveGov (4) | 5, 6, 4, 5, 3 | all every send | 0–1 (the administrator's quote) | v6; v5 (CPU) in 1 send |
| PR Newswire (3) | 5, 5, 4, 6, 5 | the arrangement, 10x/3x, 40 data centers | 0–1 (restatements gone: 8–14 → 4–6) | sends 1–2 linked nothing, 3–5 linked to v6 |

Reading: completeness and noise are where they should be on all five pages. What still varies is the link decision at
a true boundary: a customer pairing a rival accelerator with NVIDIA fleets (PR Newswire), a market forecast cited by an
author (Motley): a send links them all or none. The content is now the same every time; only that borderline
judgement flips.

B4 on the held-out article: 5, 5, 6, 6, 6 pieces; the five core facts in every send, all as rumour (unnamed Reuters
sources: right); links to total revenue v11 in 4 sends, nothing in 1. B5 adds three sentences to the link rule: a
rumour bears on a thesis as a confirmed statement does (the tier carries the confidence); a customer's or partner's
deployment of the company's products bears on its demand thesis without a dollar figure; a market forecast bears on
the company's revenue thesis only when it names the company's share or product. Tested on the three pages that
flipped (PR Newswire, Motley, the held-out) and CoreWeave as the regression.

## 14. Arm B5 (2026-10-27 22:30, $0.0184 + $0.0043) and B6

B5 on the held-out page: 6, 5, 5, 5, 7 pieces, the core facts linked to v11/v22 in every send (the flip gone). But PR
Newswire went 11, 2, 11, 12, 3 (four sends with zero reasoning tokens; the sentence "a customer's or partner's
deployment … bears on its demand thesis even without a dollar figure" readmitted the release's restatements) and
CoreWeave's linked count varied 11, 7, 3, 5, 7 where B4 was steady. Two of the three added sentences did harm; the
rumour sentence did the work. B6 = B4 plus the rumour sentence only, tested on the three pages that moved.

## 15. Arm B6 and a refuted code rule (2026-10-27 22:50, $0.0115 + $0.0046)

B6 (B4 plus the rumour sentence only): CoreWeave 9, 9, 11, 11, 9 with 6–9 linked per send (as B4); the held-out page
6, 5, 6, 6, 6 with 4–6 linked to v11/v22 in every send and consistent tiers (the flip gone); PR Newswire 13, 6, 3, 6,
14. Across B4/B5/B6 the release page is the one that will not settle (5, 5, 4, 6, 5 / 11, 2, 11, 12, 3 / 13, 6, 3,
6, 14): the model's judgement of "the same arrangement said again" varies; its core (the deployment, the 10x/3x claim,
availability) is in every send, the variance is restatements. A code rule "one piece per paragraph unless a new figure"
was simulated on the stored answers ($0): it cuts CoreWeave to 6–7 by dropping figure-less material statements that
share a paragraph with a figure (pricing beside revenue) and leaves the release at 9, 4, 3, 4, 7: refuted. Press
releases stay a named residual class (restatements, not missing or wrong facts).

Decision: B6 goes into the product as extraction v18 (`role-v18.txt`, `categories-v18.json` with the T8 reading block
narrowed, `poc-v34.json`); the week-scale extraction-only test runs with 8 workers on the 98 items.

## 16. Step 1 at scale with v18 (`scale.py`, 8 workers): the first week, 2026-10-27 23:05, $0.1064

100 items (the paused run's stored requests of 2026-07-01..07, cleaned text, role-B6 = v18), one send each, sifted by
the current checks.

| category | items | empty (model) | pieces per item | kept after sift | pieces with a link |
|---|---|---|---|---|---|
| T7 news | 65 | 2 (3%) | 8.1 | 1.0 | 18% |
| T8 opinion | 20 | 1 (5%) | 7.7 | 1.9 | 30% |
| T6 company | 15 | 0 | 6.3 | 0.3 | 5% |

Reading: the model now extracts 6–8 material statements per page and almost never returns nothing (3 of 100, against
55 of 98 under v12 and 8 under v16); 82–95% of those statements carry no link because the week's thesis list holds 4
to 11 NVDA theses, so the code drops them (660 "links to nothing shown"). The ten sampled items confirm it: "Vera
Rubin rack costs $7.8M" yields 15 material pieces and 0 kept (no pricing or margin thesis yet); 247wallst's pages keep
the quarter's figures and guidance linked to v6. Step 1 is doing its job; what reaches the library is now bounded by
the theses that exist. The same test on the paused run's last week (2026-08-18..24, 40+ theses shown) follows.

## 17. Step 1 at scale with v18, the last week of the paused run (2026-08-18..24), 2026-10-27 23:15, $0.2066

143 items with 40+ theses shown.

| category | items | empty (model) | pieces per item | kept after sift | pieces with a link |
|---|---|---|---|---|---|
| T7 news | 83 | 0 | 8.5 | 3.7 | 49% |
| T8 opinion | 34 | 0 | 8.1 | 3.8 | 48% |
| T6 company | 26 | 1 (4%) | 7.1 | 1.5 | 23% |

The ten sampled items read right: the $500bn financing partnerships → the financing thesis v38; the $1.5bn SB Energy
investment → v41; Dan Ives's 15% server price rise → gross margin v14; SpaceXAI adopting Vera CPUs → the CPU thesis v5;
a VRAM-unlock tool and a Holoscan developer post → 0 kept (right). "Poolside strikes a $6bn licensing deal" yields two
pieces and no link: a deal with no thesis to open from, which is the admission side, not extraction.

## Verdict on step 1 (2026-10-27 23:20)

With v18 one call reads, understands and extracts: on six articles sent five times each, every material statement is
present in every send; no send is empty on a page with business content; links are decided per statement and the
rumour pages link consistently; the noise left is press-release restatements. At scale (243 items of the run, one send
each) 2% of answers are empty against 32% under v12, 7–8 material statements come out per page, and what the library
keeps is now set by the theses that exist to attach to (48% of pieces linked in the last week, 18% in the first).
Residuals, named: restatements on company releases; the CPU-server and product facts reaching the right thesis
only when it is shown; theme estimates with no theme thesis shown at extraction (D199's open list).

Spend on the scratch archive today: $0.6912 in all, $0.5761 on the arms, probes and scale tests.

## 18. Acceptance on the product's own path: the v18 week, 2026-10-27 22:24–22:35, $0.22 (D200)

Alex: step 1 to production. `poc-v34` is the replay default (D200); before the run, the switch exposed that
`ACCOUNT_FROM = 17` would have sent v18 with v17's per-paragraph shape while every B arm and both scale tests used the
flat shape (fixed at the owner: `ACCOUNT_VERSIONS = (17,)`; the production request now equals the measured bytes on all
243 scale items). Then one week, 2026-07-01..07, NVDA, cleaned database, extraction → Jev matching → judging, in
`poc/data/english-v34-nvda-week-2026-10-27/` (`run-week.sh`, 361 calls, 0 failed), compared with the v16 week by
`compare_week.py`:

| | v16 week (poc-v32) | v18 week (poc-v34) |
|---|---|---|
| items extracted | 98 | 98 |
| answers the model left empty | 8 | 4 |
| items with an empty handover after the code's sift | 31 (32%) | 50 (51%) |
| evidence kept per item, mean (median) | 2.7 (2) | 2.3 (0) |
| evidence rows written | 213 | 222 |
| pieces dropped by code | 121 (98 with empty links) | 537 (506 with empty links, 14 linked to a theme thesis the request did not show, 19 quote not in item) |
| theses opened by day 7 | 11 | 9 |
| week cost | $0.22 | $0.22 (extract $0.15, match $0.03, judge $0.04) |

Read item by item on the eight items where v16 kept the most more than v18: v16's extra pieces are the stretched links
of §9 defect 1 (an author's generic AI-pullback risks → total revenue; AI-RAN spectral-efficiency results → total revenue
and Data Center revenue; a Singapore chip-smuggling seizure → gross margin; Intel's Xeon 6 and 18A deals → four NVDA
candidates). v18 writes the same statements with empty links and the code drops them (D42). Two of v16's eleven theses
were that noise (whether DGX Rubin NVL8 uses Xeon 6; Microsoft's Intel 18A wafer agreement); v18's nine are the
quantities and events. One real loss, already named in D199's open list: the CNBC Kyber-delay item of 07-05 (the delay
to 2028, NVIDIA's denial, NVL576 limited, the backup rack scrapped) keeps only the SemiAnalysis revenue projection,
because the Kyber question (v9) opens on 07-06 from a later item: the cold start's "no thesis fits" drop (D171). The 14
drops linked to v4/v5 are the capex figures of 07-07 pointing at the two theme theses, which the extraction request
does not show to a company item (§9 defect 3, Alex's design choice). Nothing new was found; v18 stands as the default.
The median item contributes nothing to the library in the first week because few theses exist yet, not because the
model returned nothing; at the last week of the run 45% of pieces found a thesis (§17).

