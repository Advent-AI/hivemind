# The census of link decisions over the window: gate PASS by the registered rule; direction unsettled (D700, D701; 2026-11-21)

Run: `poc/data/link-census-2026-11-21/` (three draws, each counted: complete, both July seq-148 answers reused, equal to old-2 with no
link row; one ledger at Alex's $0.10: settled $0.0266 at the ledger's rule of three times each reported input, 52 attempts, nothing
refused or overrun). Scored by `read_census.py` against `expected-links.json` (written before any census answer; R 1, W 38, O 66):
`census-pairs.md` (every pair and draw).

## By the registered rule
- **Known positive (v9 Data Center FY2027 reads v14 total revenue FY2027, together):** right in 3 of 3 draws; margins 0.05, 0.09,
  0.03 (the July samples, fragile).
- **W pairs (38, the shown material names no connection):** no link in any draw. Wrong links: 0.
- **Gate: PASS.**

## The O pairs that were linked (reported, not scored)

| seq | pair | draw 1 | draw 2 | draw 3 | reading |
|---|---|---|---|---|---|
| 8 | v2 (all credit support, guarantees, backstops) – v1 (AI-cloud credit support) | v2 reads v1, 0.58 | v2 reads v1, 0.51 | no link (0.48) | a whole reads its part; 2 of 3 |
| 265 | v16 (total CPU FY2027) – v14 (total revenue FY2027) | v16 reads v14, 0.82 | 0.82 | 0.83 | a part reads its whole; stable |
| 321 | v17 (total revenue growth FY2028) – v16 (total CPU FY2027) | v17 reads v16, 0.50 | 0.50 | 0.55 | a company-wide figure reads a part of the year before; at the line |
| 534 | v21 (total revenue growth FY2027) – v16 (total CPU FY2027) | v21 reads v16, 0.73 | 0.72 | 0.76 | a whole reads its part; stable |
| 534 | v21 – v9 (Data Center FY2027) | v21 reads v9, 0.53 | **v9 reads v21**, 0.52 | v21 reads v9, 0.60 | the direction flips between draws |
| 1238 | v35 (total revenue FY2028) – v14 (total revenue FY2027) | v35 reads v14, 0.52 | 0.54 | no link (0.44) | another period of the same quantity; 2 of 3 |
| 1238 | v35 – v9 | no link | v35 reads v9, 0.50 | no link | 1 of 3 |

Every proposed link carried the sign together. Proposals per draw: 7, 8, 5 (proposals: the census writes no link).

## What it shows
- **No link between unrelated questions.** Across 3 × 38 W decisions, Jev never linked a financing amount to a revenue or margin
  question, or two financing amounts of different kinds.
- **The direction of a part against its whole is not settled by the criterion.** The same version reads part-to-whole (v9 → v14,
  v16 → v14) and whole-to-part (v2 → v1, v21 → v16, v21 → v9), and one pair flips between draws (v21–v9). This is the class §3 named
  ("abstract": the criterion's two clauses admit both directions), now counted on the whole window: of the 8 pairs linked in some draw,
  4 take the same direction in 3 of 3 draws (v9 → v14, v16 → v14, v17 → v16, v21 → v16), 3 are linked in only 1 or 2 draws, and 1
  flips direction.
- **Fragile decisions:** 6 of the linked or required decisions sit within 0.10 of the next class (v9 → v14 in all three; v17 → v16 in
  two; v21–v9 in one).

## What it means for the paid run
- A linked sequence of the paid run can take its link answers from its paired census draw: a link request depends on the candidate's
  state and the shown question's card, ladder and first two evidence pieces, none of which a written link changes, so the requests are
  the same (a circle correction, if any, would be new). The readers are then known before anything is bought: draw 1 and draw 2, v2,
  v9, v16, v17, v21, v35; draw 3, v9, v16, v17, v21. Each control can retire exactly its paired draw's readers from each reader's first
  link.
- Priced from old-2's stored judgements at published rates: the readers' judgements from their links on cost about $1.0 per sequence
  (v2 $0.26, v9 $0.30, v16 $0.15, v17 $0.15, v21 $0.13, v35 $0.05), plus the extra days a changed read question queues its reader
  (estimate +30%); three linked and three controls about $7. An estimate, not a ceiling.
- **The open question before buying judgements** (for the council, then Alex): measure the current wording as it is, with its
  whole-to-part links and one flipping pair disclosed, or first settle the direction of a part against its whole in the criterion,
  which changes what the system does (a new arm, probed on these 105 pairs at cents, then Alex).

## Council round 17 (`codex-r17.md`): PROBE A SHARPENED CRITERION FIRST, agreed
- The registered PASS holds (Codex re-derived every decision from the archived responses and the ledger).
- An analyst read of the 8 linked pairs (beside the registered score, not a re-score): **v17 reads v16, together, in 3 of 3 draws is
  the clearest risk.** FY2027 CPU revenue is part of FY2027's base; at a fixed FY2028 total, a higher base lowers FY2028 growth, and
  the request shows no next-year CPU mechanism for a positive effect. v16 reads v14 and v35 reads v9 are weak; v9 reads v14 useful;
  v2 reads v1, v21 reads v16, v21–v9 and v35 reads v14 defensible with care. The registration had marked these pairs O; growth against
  a prior-year part was not foreseen as a sign problem (recorded here, the gate stands as scored).
- My lean (measure the current wording) is withdrawn: the paid run would buy judgements for a reader with an unsupported sign in every
  draw, and a cents probe can first test a wording that keeps v9 reads v14 and the 38 negatives while removing unsupported links. No
  blanket ban on a whole reading its part (the credit-support pair shows a part can inform an aggregate).
- Reusing the census draws in a paid linked sequence holds for these graphs (Codex ran the production cycle check over each draw's
  proposals in article order: no correction); a $0 replay in the paid harness must confirm every matcher request hash before buying.
