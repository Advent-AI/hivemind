# Are the eleven first-pass refusals reachable? Two blind readers, $0 (D476), 2026-11-13

**Answer: of the eleven theses the judge's first pass refused on the full run, both readers agree on ten. Six should be declined: no
question worth asking in any shape the ladder step can take (five distinct matters). Four runs, two distinct matters, have a question
worth asking that the article supports in a shape that can be laddered: the H100 rental price (twice, from one article) and the memory
price (two articles). They split on one: federal AI obligations.** On this population Stage A counts 32 right, 22 by a written ladder,
of 40 (line scaled to 32 and 26). So the written line is reachable on paper only if all four agreed conversions land and nothing else is
lost: +4 gives 26.

Readers: Codex (`codex-phase1.jsonl`, `codex-phase2.jsonl`) and a Claude subagent (`claude-phase1.jsonl`, `claude-phase2.jsonl`). Each read
the article and the library at that step first, without the thesis, and wrote the questions the source supports (Codex 13, Claude 18:
12 distinct matters), then compared them with the thesis (`packet-phase2.json`); the key (`key.json`) was not shown.

| case | thesis | Codex | Claude | the mechanism behind the refusal |
|---|---|---|---|---|
| 1, 5 | c1/clean-12, c3/clean-10: the H100 GPU-hour rental price in 2026 | reachable (as written for c1) | reachable (year-end price) | the ladder step's rule "a matter no listed theme covers" (`poc/universe.json` holds 12 themes, among them "AI capital spending" and "Semiconductor cycle"; the model judged that none covers a GPU rental price, and the Stage A readers split): not the thesis's shape |
| 7 | c1/clean-13: HBM/DRAM prices over the 12 months to mid-2027 | reachable (DRAM price, calendar 2026) | reachable (DRAM price, calendar 2026) | Step 1's rolling window (the period rule read as a horizon) |
| 8 | c2/clean-6: memory contract prices in 2026 and the rack's memory cost | reachable (DDR5 contract price, 2026) | reachable (DRAM contract price, 2026) | Step 1's second figure (a bank's rack estimate no public material settles) |
| 10 | c1/clean-15: federal AI obligations and potential awards | reachable (obligations, calendar 2026) | declining right (about $7bn cannot move NVIDIA's revenue: §4 test 1) | split |
| 2, 6 | c1/clean-10, c3/clean-9: the China domestic-share survey | declining right | declining right | D417 (Alex: "这类题不出题") |
| 3 | c2/clean-10: custom-ASIC spending against NVIDIA GPU purchases | declining right | declining right | no dated outcome the article supports (both); the Stage A readers had called this refusal wrong |
| 4 | c1/clean-2: the Intel stake's size and carrying amount | declining right | declining right | a completed, sized investment is not an obligation (§3 C) |
| 9 | c3/clean-3: US approval of China sales and their scale | declining right | declining right | one background sentence; no pending decision named |
| 11 | c1/clean-11: the Firmus investment and stake | declining right | declining right | about $500m cannot change NVIDIA's revenue, profit, cash or credit risk |

**What it shows.**
1. Most refusals are right, and for a reason upstream of the ladder: four of the six right refusals are theses Step 1 should not have
   opened at all (a completed stake, a small stake, a background sentence, an outcome with no settling material). The refusal is the
   pipeline catching Step 1's over-opening.
2. The reachable four come from two different places: two from a Step 4 rule (the H100 price refused because no theme in the fixed list
   covers it; Claude's reader called declining "wrong here"), two from Step 1's memory shapes (the same class c15yc and c17 failed on).
3. A restructure in which the opening step writes the ladder could touch at most the memory pair and the over-openings; it would not touch
   the theme-list refusals unless the opening step also stopped needing a listed theme.
4. Limits: one run's population; the readers judged worth and shape, not a written ladder's quality; the Stage A readers earlier ruled the
   H100 refusals right on the theme list as it stands (council round 5).

## Addendum: every theme-coverage decline in the stored final-configuration answers (council round 20's step 1, $0; `theme-census.txt`)

Read: the fourth Stage A run (132 answers) and the full run's three draws (120), every send. **Six theses were declined for "no listed theme
covers it" (12 sends), and the same model laddered three of them under an existing theme in other sends.** The H100 rental price: declined
in five of nine sends over the three draws and laddered in four: three under "Semiconductor cycle" (an annual average or a year-end price)
and one under "Custom silicon at cloud providers" as a yes/no on staying below the peak (c2 send 3; council round 21 caught the miscount). The other three:
a US lidar ban (two declines, once laddered under "Chip export controls", a wrong fit), the CPU-to-GPU ratio in inference (declined 3 of 3),
Huawei's chip output (two declines). 31 theses were laddered under a theme in 80 sends; memory prices go to "Semiconductor cycle" every time,
although that theme's definition (`poc/universe.json`) watches only industry revenue growth.

So the H100 refusal is not a missing theme or a new-theme path: it is the model's coin flip on whether a thinly defined existing theme
"covers" a market price, the same theme it stretches to memory prices without hesitation. A new-theme design (storage, deduplication,
cross-company reading, D191) is not needed to explain it; whether a theme's definition should name the prices it carries is a product
question about `poc/universe.json`, which production shares.

## Addendum 2: does the H100 thesis reach any judgement that matters? (council round 21's check, $0; corrected in round 22)

Only draw c2's first pass laddered it (c1 and c3 declined), so c2 is the one place to look. Its theme judgement (v8, "What is Ornn's
published H100 GPU-hour spot rental price … on December 31, 2026?", rung 3, $2 to below $3) was shown as theme context in 31 company-question
judge requests (`poc/data/clean-e2e-full-2026-11-13/c2/judge/draw-c2/archive.sqlite`). A first count searched the answers' text and found
none; the council found that **20 of the 31 answers cite it by id** in their structured theme pushes (a text search misses an id): five
questions, v1 credit support (5), v2 Vera Rubin shipments (5), v3 China's H200 authorization (1), v5 the Kyber rack (4), v7 supply commitments
(5); 18 push one way, 2 the other. Read in the last judgement of each: the reasons of v1, v2, v3 and v5 never mention the rental price; v7's
says "The updated lower-rental-price theme is a counterweight, but not enough to pull the estimate below the $125 billion boundary." By subject,
v3 and v5 are the questions behind graded q08 and q18; their reasons do not rest on it. No same-input control was run, so this shows no
decisive use in this window, not that the theme had no effect.
