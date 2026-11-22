# Claude's read, round 1 (written before reading codex-r1.md)

Scope: the product poc-v118 (no seeds). New facts gathered at $0 for this round:
- `selection-census.md`: the matcher's "part_of" is undirected by its own criterion and noisy (old-2 seq 148: total revenue FY2027
  "part_of" Data Center 0.99; old-1 seq 1410: FY2028 growth "part_of" FY2027 Data Center 0.79; aggregates "part_of" single deals).
  It cannot choose an edge or its direction. The typed keys (`view_keys`: measure, scope, period) separate the pairs cleanly: in all
  three draws a `segment_revenue` / `product_revenue` question and a `total_revenue` question of the same company and fiscal year.
- Creation order differs: old-1 and old-3 open total revenue first (seq 22); **old-2 opens Data Center at seq 62 and total revenue at
  seq 148**. A rule that only acts when the reader is created misses one draw in three.
- **Filing:** in old-2, **106** evidence items are linked to both v9 (Data Center) and v14 (total). With D265 read literally on a
  chosen edge, all 106 would leave total revenue. The Wall Street estimate items (e4061, e4097, e4348) are linked to v14 only (e4348
  also to v17, v21, v35), so they stay either way.
- Matching describes a question by its text and ladder only (`views/matching.py` `describe_view`, lines 161–170): a changed
  judgement does not reach the matcher's requests. Not yet checked: whether the reading step's shown questions carry conclusions.
- The self-made reference (`../self-reference/RESULT.md`) shares a cause: the market figure for the whole sits under the whole only,
  and the part never reads it.

## Per item
1. **Who chooses and which way.** Recommend: code writes a component edge from the typed keys: same company, the same fiscal period,
   one question's measure a segment or product revenue and the other's total revenue; the part reads the whole. This is identity
   (an accounting fact on typed fields), not importance; the judge already holds "a component cannot exceed its whole"
   (judging-v7 line 4 and 9). The edge is written at whichever question's creation completes the pair (D191 point 2's "a dependency
   may be added to an existing thesis by a later item", Alex: "可以"). Direction: the part reads the whole, because the market's
   figures (consensus, guidance) are company-wide and filed under the whole (D207); PRD 06 lines 131–132 and D537 agree, the probe
   showed it works. D368 item 4 (root reads drivers) is about seed driver edges, a different relation (a driver is a judgement of
   cause, not an identity); it is not built here. Departing from D51's chooser (the matching call) for this identity case is Alex's
   choice. The direction label is computed from the two ladders (`matching.ladder_direction` and the bullish label of the part's
   ends), not guessed. Risk: keys are model-written (`scope_source: model`; old-2 v8 stand-alone CPU has measure `other` and would be
   missed; old-3 v14's question says "total CPU" while its scope says "Vera CPU"). A missed pair costs nothing new; a wrong pair
   shows a judge an irrelevant whole, which the judge can weigh.
   Not covered, said plainly: growth-rate against total of the same year (council Q's v21, v17: duplicates by D197's idea, a
   separate class); FY2028 against FY2027 (a successor reading its base: not an identity of one period).
2. **The line.** Print the dependency's stored `reference` and `implied_outcome` (D260 fields, written for every judgement) before
   the reasons, so the decisive figure is never cut; keep the reasons cut. Only requests that carry a dependency change; today's
   requests carry none, so every stored request stays byte-equal. Code, not the frozen prompt file; still a new judging version.
3. **Filing.** A component edge moves no statement: `narrowest_links` reads only edges whose kind states a hierarchy (seed edges).
   The 106 double-filed items stay as they are today. The edge needs a stored kind; old product stores have no rows, seeded stores
   keep their marks (SEPARATION-DESIGN 2.3).
4. **D542's five items in the product:** awaited circle: does not arise (code-written edges need no waiting; a circle would need a
   whole reading its part, which the rule never writes; the circle check stays). Closing: the reader prints "closed" today; a part and
   its whole share the fiscal year, so they close together or the part reads the closing conclusion; "historical only" is not needed.
   Theme twice: the rule names number questions of one company, never a theme. Historical readers: they read "depends on" correctly
   for a read edge; product stores hold no old rows. Label: `last_end` exists only on seeded stores; the product's label is computed.
5. **Order and cost:** the whole is judged first (`topological`), a changed whole queues its parts (`queued_by_change`). A few extra
   judge calls a day at about $0.006 each (the probe's measured cost): cents.
6. **Pieces and test.** Touched: the matcher's writer (an edge after matching), judging's line (code), filing's narrowest reader
   (code), the store (a kind). All frozen as poc-v118 runs them: a new version Alex opens. The test: because filing and matching are
   unchanged, only the parts' judgements change; replay each draw from its archive with every other answer reused byte-equal, and
   judge the linked parts forward day by day as their own sequence, beside a control sequence of the same parts unlinked (fresh,
   so the sampler is measured). About 2–3 parts a draw × about 75 days × 2 arms × 3 draws ≈ 1,000 calls ≈ $6 (estimate). Pass:
   reconciliation by the probe's reading rule on a fixed set of days, and no answer moved away from a source-backed figure.
   Unknown to check before: whether any other request reads a part's conclusion (reading step's shown questions, theme block).
