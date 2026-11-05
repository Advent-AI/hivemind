# Reflection brief: why the argument card lowered judgement accuracy, and how to solve it

You are a read-only reviewer. Do not edit any file. Repository: `/Users/lchingen/hivemind` (branch `main`, uncommitted work in progress).
Answer in English, plain words, each claim with the file, table row or stored request it rests on.

## What the card is for (read these first)

- `docs/DECISIONS.md` D201 (2026-10-27; Alex: each question carries a versioned research argument: what changed, sources for and
  against, whether sources are independent, limits; the judgement reads the argument and its sources, not just a list of evidence) and
  D358 (evidence bloat: a three-month run had one question with 1,768 linked pieces, a judgement reading 698 of them, 292 KB, and the run
  halted; Alex: "很严重，需要解决").
- `docs/research/2026-11-04-argument-record/design.md` (draft 8): the card is written in the same judging call (judging-v8), read back by
  the next judgement in place of the old evidence window; new evidence shown for 3 judgements; no periodic job (judging is event-driven,
  D63, D356). `simulation.md` sizes it.
- Code: `src/hivemind/views/judging.py` (`card_in_view`, `_lines_card`, `card_schema`, `check_card_answer`, `_record_card`), the prompt
  `src/hivemind/prompts/judging-v8.txt` against the frozen `judging-v7.txt`.

## What was measured (step 2 of the validation, `log.md` row 4)

One 14-day draw of judging-v8 (`poc/data/e2e-r10-card-v109-2026-11-04/d1`) paired with the frozen v7 draw
`poc/data/e2e-r9-frozen-v108-2026-11-03/d1`: identical evidence and questions (extraction, matching and collision answers replayed from the
same archive), only judging differs. Frozen judgement ruler (`docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py`):

- v8 agrees on 12 of 17 judged questions; v7 agrees on 15 of 17 in the paired draw and holds all three flipped questions in all three of
  its draws (d1, d2, d3). Flipped: q01 total revenue FY2027 (v1; gold rung 2, v8 rung 3), q02 Data Center revenue (v2, depends on v1),
  q09 financing commitments and backstops (v9; gold 25–60 B, v7 rung 4, v8 rung 3).
- v8 ends at the rung its own market reference names on 16 of 19 questions (v7: 9, 11, 8 of 19); over all judgements 71% (v7: 48%, 66%,
  51%).
- Other numbers: refusals 22 of 234 answers (9.4%), all fixed on one retry; requests 97% of v7's characters; judging cost $0.59 against
  $0.39; median visible output 1,280 tokens against 693; 204 of 1,267 card claims (16%) state a figure that none of their cited pieces
  contains (the model's own derived number), 20 of 135 claims on the final cards.

## Probes already run (cents; specs and results beside this brief, `probe-spec-*.json`, `probe-result-*.json`; script `probe_counterfactual.py` re-sends the stored request byte-identical, refusing if the rebuilt archive key differs)

1. q01 total revenue, v8's stored judgement on 07-13 and 07-14, each arm sent 3 times:
   - as stored: rung 3, 3, 3 (both days);
   - card claim k11's own calculation cut ("…imply about $387 billion if Q2's 11.5% sequential growth carries into Q3-Q4" → "…figures are
     reported"): rung 2, 3, 2 on 07-13 and 2, 2, 3 on 07-14; the rung-2 answers apply 95% year-over-year growth to FY2026's $215.9 B
     (about $421 B), as v7 did;
   - the "not quantified" caveats cut from eight claims: 3, 3, 3;
   - the raw pieces v7 cited but v8 was not shown added to the new-evidence block: 3, 3, 3 (07-13) and 2, 3, 3 (07-14).
2. q09 financing, the day v7 d1 moved to rung 4 (07-12):
   - v7's own stored requests re-sent 4 times: 07-11 rung 3, 3, 4, 3; 07-12 rung 3, 4, 4, 3. The three v7 draws moved to rung 4 on
     different days (07-06, 07-09, 07-12) and stayed: under v7 this is a coin flip that sticks once it lands.
   - v8's stored 07-12 request: 0 of 7 sends reach rung 4; with the card's Firmus caveats cut and the raw Firmus pieces added: 0 of 4; with
     the derived $20.7 B cut: 0 of 3.
   - v8's system prompt and schema on v7's 07-12 material (no card): 4 of 4 rung 4 (one answer double counts Sharon's $4.88 B); on 07-11
     material: 0 of 4. So v8's prompt alone does not suppress the move; the material v8 reads does. One visible difference: the dependency
     conclusion of v1 that v9 is shown is quantitative under v7 ("about $399.4 billion") and caveat-heavy under v8.
3. The model's own account (`probe-account-v8.md`): for q01 it names the run-rate sentence of the prompt ("reported figures and guidance give a
   run-rate that carries the guided growth forward, never the last quarter annualised flat") and picks sequential growth; for q09 it says
   its one-third discount of Firmus "relied on invented assumptions".

## The independent reader of ten final cards (`cards-step2.md`; the reader's report is quoted in `log.md` once written; key points)

0 sound, 7 minor issues, 3 material issues. 16 claims unsupported or overstated (10 clear; e.g. v1 k9 turns a Chinese memory shortage into
an NVIDIA demand constraint; v22 k7 says "flat" where the cited v5 conclusion says prices rise); 5 material omissions (v1 e106, the only
above-consensus estimate in force; v17 e155; v6 e136; v8 e489 and e249); 10 relay or independence errors (one release counted as two or
three sources; a separate later report marked as a relay); circular support (v2's own figure returns through v13 and is counted twice in
v19 and v20). It also flagged v1 k11 and v9 k7 as the card's own extrapolation presented as what sources imply.

## My diagnosis so far (attack it)

- M1 (shown on q01, 4 of 6 flips when cut): the card stores the model's own calculation and method choice as a claim backed by evidence ids
  and "independent sources". The next judgement reads it as part of the standing case and repeats the method instead of re-deriving. Under
  v7 the previous calculation appears only as "previous conclusion, for comparison only", and the model re-derives from the raw pieces.
- M2 (q09, not pinned to one sentence): v8's material makes a coin-flip move almost impossible (0 of 14 sends across arms); candidates are
  the card as a whole, the caveat-heavy dependency conclusions the cards produce upstream, and the narrower reading.
- M3 (reader): the card is a lossy, model-written summary: pieces it does not cite leave view after three judgements, and its relay and
  independence labels are often wrong. Whether this changed any rung in 14 days is not shown.

## What I need from you

1. Root cause. Is M1 the mechanism or a symptom? What design choice produces M1, M2 and M3 together? Check against the stored data and the
   code, not against my summary; say where my reading is wrong.
2. Options. Two to four structural ways to solve D201's and D358's problems without the loss, each consistent with the system: no periodic
   job, judging event-driven, code owns identity and never importance (AGENTS §2), the frozen rulers and the frozen v7 prompt untouched (a
   change is a new judging version), the prompt a general hedge-fund analyst's (no NVIDIA-fitted rule, AGENTS §6). Include "do not read the
   card back at all" and "keep v7's window and add the card only as a record" if you think they hold, and say what each loses.
3. For each option, the cheapest proof on stored data ($0 replay or a few cents of re-sent stored requests, three sends per arm) that would
   show it flips q01 and q09 back without harming the other 14 agreeing questions, and what risk that proof leaves uncovered (the long
   horizon of D358 is not in the 14-day window).
4. Your lean, in one paragraph.

Out of scope: extraction, matching, question opening (frozen, D274, D354); the frozen ruler files (AGENTS §7.1); any paid run longer than a
few re-sent requests.
