# Council round 5: the pass line is met; the remaining problem is noise (read-only)

**K6b on Luna medium, forward over 115 gold articles** (`poc/data/clean-step1-takeover-2026-11-07/gold-k6b-medium/`): 115 of 115,
0 failed.
- Gold (frozen matching): helpful 201 of 234, core **84 of 86** (best so far), not-kept 61 (K5 50; production 30–34).
- Final library: 21 theses. Three independent blind readers, same packet with K5's library as the other letter:
  - K6b medium: small 0 / 1 (the Intel stake) / 0; fragments 0 / 0 / 0; duplicates 0.
  - K5: small 9 / 10 / 9; fragments 3 / 3 / 2.
  - Pass line (at most 3 small, no fragments, helpful at least 190): met.
- My own read was stricter: I saw 4–5 small (Intel stake, physical AI in buildings, Taiwan and Korea power and water, microLED,
  DSX) and two possible fragments (China access / Huawei / domestic accelerators; credit-support model / neocloud demand
  channel). I report it as a disagreement; the independent readers decide.

**Luna JSON-mode check** (your round-4 test, 10 articles × 3): small theses 8 against 9 under strict schema; 3 of 30 JSON-mode
answers failed the schema (missing `links` on unfiled items). The request form does not explain Flash's lower small count; the
model does.

**Luna high effort** (27 × 3): 6 of 81 calls timed out at 180 s. The answered 75 look like medium: core 63 of 63, about 0.8
not-kept per answer. Not worth the latency.

**Flash K6b forward over 115** is at about 60 of 115.

**Noise.** The 61 not-kept in the Luna medium run, by the gold's reject row: reporter background or framing 15, common-knowledge
claim (D243 #5) 9, product detail without scale 7, not evidence under the keep rule 7, generic risk or unargued view 7,
adjective-only quote 5, arrangement in place 4, other 7. No class dominates. Wording changes to the closing check have repeatedly
failed (LOG §§2–7, your STEP1 files).

**Proposal K7 (structural, not tried before).** The closest-thesis fields worked for theses because they force the decision per
thesis in the answer itself. Do the same for the keep test. Each evidence item carries a required `keep_test` field: an enum
naming the one keep kind it satisfies (company figure, guidance or decision; counterparty action or figure; named party's new claim
or estimate; policy step) or the one not-kept row it falls under (background or framing, common knowledge, product detail without
scale, unargued view or adjective quote, arrangement in place, other company with no path, share price, repeated, boilerplate).
Code drops items labelled with a not-kept row, visibly, like unfiled items. The model still makes the call; code only acts on the
label (AGENTS §2).

Risks: the model labels everything as a keep kind (no effect), or it over-drops; the field adds output.

Test: the 27 articles × 3 at Luna medium against K6b medium. Measure not-kept kept, helpful, core, and read the dropped items to
count wrongly dropped helpful ones.

Questions:
- (a) Does K7 differ in substance from your "list sources first, then judge each" idea, and from the earlier failed placements?
- (b) Is it worth testing now, given the pass line is met?
- (c) What else would you try for noise?
- (d) Do you agree the pass line is met, and what caveats must go to Alex?

Under 600 words.
