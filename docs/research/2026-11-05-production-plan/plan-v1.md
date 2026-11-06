# From the split prototype to production: plan v1 (after round 1)

Round 1: five read-only Codex reviews (`r1/`) and Claude's own trace reading (`r1/claude-findings.md`); round 2 so far: a complete census of the
confirmation run by ten Codex readers, eight items each (`r2/codex-census-*.out`, 126 findings over 75 of 76 items, collected in
`r2/census-findings.json`), and Claude's verified responses (`r2/claude-responses.md`). This plan replaces v0. Nothing is re-run until Codex
and Claude agree on it and Alex has taken the decisions in §4.

## 1. The error classes the plan must answer (confirmation run, first 100 rows; census counts are one reader's, one draw)

| Class | Count | Example | Mechanism | Owner of the fix |
|---|---|---|---|---|
| One statement stored twice, once by A, once by B | 10 (+ contained quotes) | 1275 "2026 capex $60–$64B" as e4432 (TSMC capex) and e4436 (TSMC revenue) | the handover appends A and B; production `sift` merges identical quotes | code (handover) |
| B files under a broader question than an open narrower one | about 14 | 1211 hyperscale revenue → total revenue; 1246 CPU forecast → total revenue | production's `narrowest_links` is not applied; B's link description ranks the company-wide revenue question as the fallback | code (narrowing) + Alex (fallback, D361) |
| B parks weak links | about 14 | 1207 futures contracts → total revenue; 1240 TSMC revenue → ON Semiconductor revenue | the fallback sentence (D273) | Alex (D361) |
| A misses important new questions | 8 | 1234 Alphabet total revenue; 1228 Microsoft total revenue; 1266 Marvell revenue; 1209–1210 FY2028 revenue (opened at 1213) | to trace: A's opening sentence asks for "an important new question" (singular) while v74i asks for "the important questions this item raises" | prompt (A), proved on stored requests |
| Ladder direction or arithmetic wrong; a floor read as a point | 9 | 1273 "Strongly bullish: below $18 billion"; 1249 "> $200 billion" judged in the $200–250 billion rung | no favourable end; bounds and words written separately; references that are floors | record preparation (D186 favourable end; code-rendered intervals) |
| Part-period pace references | 7 of 15 ladders, 2 judged at the extreme rung | v79 TSMC revenue "NT$4.8T × 1.36" | my pace sentence | withdraw (record preparation) |
| Attribution wrong | 7 | 1254 company figures attributed to the article author with the article day | record preparation and B | prompt audit (record preparation, B) |
| Matching treats the publication day as the statement day | 7 | 1216 "officially announced DLSS 5 in March" compared as stated 2026-08-29 | `jev_matching.decide`: `said_day = original_day or publication_day` (production code, frozen matching D354) | Alex (a production finding) |
| Jev marks a passage a repeat on a partial overlap | 3 | 1266 a Q3 forecast inside a passage marked a repeat of Q2 | production matching | Alex (a production finding) |
| Unsupported or unverifiable new questions | 4 | 1251 share from financed customers; 1277 TSMC margin from a supplier rumour | no admission reason or settling material checked | record preparation (admission reason) |
| Every new question has an empty due day | 22 of 22 | — | exact day required; none known | code (analyst check date) + Alex confirms |
| B misses | 5 | 1246 Vera CPU in full production | to trace | B, after the prompt audit |

## 2. The production shape (agreed in substance with the production review, `r1/codex-production.out` §1–§5)

1. **One code path** in `src/hivemind` (module `split_extraction`): request builders, schemas, record preparation, `source_quote`, the handover;
   `round.run` calls it through the existing `extractor` hook, selected by a new configuration version (D359), never by an environment variable.
   Prompts as versioned files in `src/hivemind/prompts` (A, B, record preparation, collision). The research runner becomes a thin caller or retires.
2. **Handover contract:** one stored piece per normalised quote with the union of its links (as `sift`); `narrowest_links` applied to B's links;
   `candidates_with_evidence` re-run after merging; a candidate's own passages and B's links to an older-period question reconciled by the rule
   agreed in round 2 (C3); groups as agreed (C4).
3. **Record preparation contract:** subject from the listed ids or `new` (done); admission reason from the standard's five (D184), with each
   reason's checks in code as `check_admission` does (year limits with or without a ladder; obligations within 18 months); `favourable_end` and
   code-ordered, code-rendered numeric rungs (D186); the reference is guidance, consensus or a stated target, else the prior year's reported figure,
   else no ladder; an analyst check date when no exact day is supported (with Alex's confirmation).
4. **Per-item snapshot (D375) in the day runner:** sequential items with A and B in parallel as the reference implementation; speculative
   preparation only after a deterministic replay shows the same accepted requests and ledger and counts the discarded calls.
5. **Durable research subjects** in the ledger (id, name, kind, aliases), written in the same transaction as the question; restored on restart.
6. **State × event contract** as drafted in `r1/codex-production.out` §3, reviewed against the actual transactions; a limited run never marks a
   cut day complete (production `replay.py`'s `max_items_per_day` does today).
7. **Preflight** reconstructs and checks every split request, answer, snapshot and handover; reports skipped and unexercised checks.
8. **Frozen tests** for the accepted split version (prompt bytes, schemas, configuration checksum), beside the existing ones.

## 3. Corrections to my own changes (agreed, verified; `r2/claude-responses.md` §A)

Withdraw the pace reference (A2); em dash compared as a space only between word characters (A5); refuse run-on quotes (A6); the question's fiscal
year reinterprets only the same bare year (A7); year limits by admission reason, with or without a ladder (A8); the deal sentence narrowed to one
deal with D210's exception kept (C6).

## 4. Decisions for Alex (each with options and a recommendation, once Codex and Claude agree)

1. Acceptance on the frozen ruler given D370 (seeds as a labelled measurement fixture; an unseeded production-shaped run; or both).
2. The evidence call's fallback sentence (D273, D361).
3. All-open context at production scale: about 150 input tokens per open question per call (measured; 87 open questions ≈ 16,200 tokens).
4. The analyst check date for questions without an exact source date.
5. Production findings outside the split: the publication day used as a statement day in matching; Jev repeats on partial overlap; production's
   D266 run-on quote keeps a summary its passage does not support.
6. Promotion of the accepted split version (D359).

## 5. Order of work, each with its cheapest proof and the one test that accepts it

| # | Work | Cheapest proof ($0 unless said) | Accepting test |
|---|---|---|---|
| 1 | Handover contract (merge, narrowing, candidates re-checked) | replay every stored handover of the three runs; 1207, 1211, 1275 become one piece each | real writer on a temporary ledger: one piece with both links; a mutant without the merge fails |
| 2 | Record-preparation contract (admission reason and checks, favourable end, rendered intervals, reference rule, check date) and the A opening sentence | stored requests re-sent once on the cases that motivated each change (1273, 1239, 1240, 1249, 1253, 1251, 1234, 1228), cents | code checks on stored answers refuse an inverted ladder and a floor-as-point ladder; the recall cases propose their question |
| 3 | Move to `src/hivemind` with versioned prompts, configuration and durable subjects | replay stored answers through the moved code: byte-identical requests, same handovers | restart test: a research subject keeps its id and reaches the next item's A, B and matching |
| 4 | Day runner under D375 and the state × event contract | replay two stored ordered items with a crash between stages | the restarted ledger equals the uninterrupted one |
| 5 | Preflight and frozen tests | altered source, snapshot or answer refused; empty population reported unexercised | preflight green on the stored runs |
| 6 | Throughput and cost curve | replay schedule simulation; tokens by library size | a budget Alex accepts |
| 7 | Acceptance as Alex decides (§4.1), on held-out inputs with three draws and a same-day control | scorer dry-run on the stored ledgers | the registered measurement's prewritten criteria |
