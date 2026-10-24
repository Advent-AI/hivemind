# Probing the idea route: where retrieval and reading fall short (2026-10-24)

Alex: "do more matching of how an idea could use the endpoints to go about finding the right theses … go through the
logic multiple times and see where, for example, the search engine retrieval may be lacking". Method: 49 realistic
ideas (`poc/eval/idea-probes-2026-10-24.json`; English and Chinese, with and without numbers, about NVIDIA, its
supply chain, China, competitors, peers, capex, nonsense, and two pinned to earlier days), each with the views that
bear on it by my own reading of the 94 views (a reading, not gold). `scripts/idea_probe.py` runs search and the model
and flags each probe; `--search-only` is free. Logs: the session scratchpad; archive `poc/data/service/idea-archive.sqlite`.

## Census, first run → after the fixes

| Flag | Meaning | Run 1 | Run 2 |
|---|---|---|---|
| MISS | an expected view is not among the ten candidates | 6 | 6 (different ones; see below) |
| NULL | search said "no recorded view" | 3 (2 wrong) | 0 |
| OBJECT_WITHOUT_VIEWS | the idea "names" a universe object that has no view | 5 (3 false: `rate`, `risk`) | 2 (GOOGL, MU: real) |
| EMPTY | the model chose no view | 4 (all right) | 3 (all right) |
| UNEXPECTED | the model chose a view outside my expected set | 13 | 17 |
| cost | | $0.25 | $0.13 (changed candidates re-read; the rest replayed) |

## Four retrieval mechanisms, each counted, fixed and tested

1. **The text leg was blind to Chinese without spaces.** `store.search_views` splits a query on whitespace, so
   "数据中心需求见顶了吗？" was one phrase the trigram index never matched → null (probe 49), though v3, v1 and v20
   bear on it. Fix: `search.lexical_terms` asks the index for Latin words of three characters or more and every
   three-character window of each Chinese run. Test: the windows and a non-null answer.
2. **Names were split into words.** `fed-policy-rate` gave the alias `rate`, `us-recession-risk` gave `risk`,
   `Micron Technology` gave `technology`, `us-china-tariffs` gave `china`: three probes got a false object, and
   for "H20 sales to China…" and "Section 232 tariffs…" the object boost lifted the eight noise views of the tariff
   and export-control themes (anti-dumping notices, tungsten allocations; D104) above everything. Fix: an alias is
   the id, the full name or an entry in the universe's new `aliases` list; a Latin alias must stand as a word
   (`meta` is not in `metadata`). Test: `rate` is not the Fed, `metadata platforms` names nothing.
3. **Product names did not stand for their company.** "Rubin will contribute more than $50B" and "Blackwell demand
   is softening" named no company, so no view got the object boost; the first lost v48 (Vera product revenue) to
   SMCI, MSFT and META revenue views, the second ranked CoreWeave views first. Fix: `poc/universe.json` now lists
   aliases per company and theme (NVDA: Blackwell, Rubin, Vera, Hopper, H100, H20, GB300, DGX, GeForce, CUDA, 黄仁勋 …;
   AMD: MI450, Helios, Venice …; TSM: CoWoS; GOOGL: TPU; AMZN: Trainium, AWS; themes: AI trade, 出口管制, 关税, 美联储 …).
   The pipeline reads only id and name, so nothing else changes. Run 2: v48 is a candidate for probe 7.
4. **The null rule had no similarity leg.** "Is the AI trade over?" names nothing the old aliases knew and matches
   no Chinese text → null, though v20, v1 and v88 bear on it. Measured on 74 sentences: every idea with a view has a
   top similarity of 0.33 or more; a house purchase 0.19, "黄仁勋是个天才" 0.22; off-subject ideas about Apple, Tesla
   or Bitcoin score 0.33–0.48. Amendment to D91's detection (the decision itself stands: null means no recorded
   view): null only when no object is named, no view text matches, and the top similarity is below 0.30. The ideas
   above the floor go to the model, which answers "none" ($0.004 each); Apple and Tesla now cost a call.

## What still misses, and why (run 2)

- Probe 18, "H20 sales to China will resume": v9 is my expectation only because its question lists China
  restrictions as a factor; the library has no view on H20 or licences. Probe 20: v9 is the fifth of five expected.
- Probes 22 and 40 ("TPU and Trainium cap NVIDIA's share", "Blackwell demand is softening"): v3's text says data
  center revenue, not Blackwell or share; v2 and v9 are found and chosen. A broad idea against 23 NVDA views and
  k = 10 cannot hold every bearing view.
- Probes 47 and 49 (the AI trade, 数据中心需求见顶): v1 and v20 rank 11th or lower among 19 capex views; the
  model still chose v88/v71 and v23/v1/v3. Same k limit.

## The model's reading (not changed: §6, no prompt grows without an audit)

- Claims: right in all eleven money cases, including Chinese "3500 亿美元" → 350e9 and "be a $10B line" → "=";
  verdicts match the bands (holds / not_yet / borderline). One prose slip: probe 39's summary wrote "$3,000 billion"
  for 3000 亿; the claim number was right.
- Inclusive choice: the model adds v2 / v9 as "context" next to the direct view (probes 8, 9, 23, 38, 45, 46) and
  chose six views for 数据中心需求见顶; the summary always says what no view covers. For the FE, `chosen[0]` is the
  direct view; a `role` (direct / context) is a choice, not a defect.
- Sampling: probe 1 chose v3 alone in run 1 and v3 + v9 in run 2 once its candidate list changed; the model is a
  sampler, and the archive makes any given card reproducible.
- Numbers the ladders cannot evaluate: percent (73%, 20%), gigawatts (1 GW), counts (100,000 vehicles): six probes
  stated such a number; the model correctly set no USD claim, and `evaluate` has no unit model beyond dollars.

## Choices for Alex (each changes what the system does)

1. **k.** Ten candidates lose the fourth or fifth bearing view on broad ideas (probes 20, 22, 40, 47, 49). Options:
   k = 15 or 20 (more tokens per call, ~+40%), or a per-object cap (at most n views per object so one company's 23
   views cannot fill the list). Lean: k = 15 and measure.
2. **Evaluate beyond dollars.** Extend the band parser to unit-tagged ladders (%, GW, 辆, 小时价格) so "below 73%" or
   "below 1 GW" gets a verdict. Lean: yes, after the FE shows where numbers are typed.
3. **Say which named object has no view.** The card could carry `search.objects: [{object, views_as_of}]` so the FE
   can print "no view on Micron as of 08-15" instead of the model's sentence. Lean: yes, one field.
4. **A role per chosen view** (direct / context), one word in the schema, for the FE's layout. Lean: wait for the
   FE contract.
5. **The eight noise views** (five anti-dumping, three tungsten / 232) stay in this sealed ledger until the next run
   with the tightened tags; the alias fix stops them from crowding candidates, the model already rejects them.
