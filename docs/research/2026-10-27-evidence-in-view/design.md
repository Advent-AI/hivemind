# Evidence in view: what a judgement reads (2026-10-27)

Alex, 2026-10-27 06:00, on the finding that evidence in force grows without bound: "这是什么问题你深度思考之后改".

## 1. What the problem is

A quantity thesis such as v6 (NVIDIA FY2027 Data Center revenue) had 574 pieces of evidence in force by 2026-08-14 after six
weeks; v11 (total revenue) 341. Every judgement re-reads all of it: 40 of 316 judge requests were over 30k tokens (max 67k),
judging had become 38% of spend and rising, and the slips that stalled the run (a push on an id not shown) come from
enumerating 300+ ids. Two mechanisms, each at its own writer (census: `census.py`, this folder):

1. **Linking is wide at extraction.** `role-v14.txt` line 4 says "Every statement and number is, by default, evidence linked
   to a shown thesis" while line 23 says "link evidence only to the thesis it directly concerns … omit statements with no
   thesis to link to". The model resolves the contradiction by attaching every NVIDIA business mention to the broadest
   thesis in view: 415 of v6's 574 pieces were never cited by any of its 33 judgements (a Motley Fool note on liquid
   cooling, Bristol Myers buying a SuperPOD, LG's rack R&D, PYLER's DGX transition); 322 are linked to v6 alone; 2.5 pieces
   per item land on v6. That is the extraction prompt's rule, not the PRD's (05-extraction: "evidence may link to shown
   theses or current candidates"). Fixing it is a separate slice (prompt audit, extraction prompt version), reported to Alex
   with these numbers.
2. **The judge reads everything in force, every time.** Judging-v4's first rule: "Rejudge from all evidence currently in
   force". An analyst does not re-read every article each morning: he keeps the material his view rests on and reads what
   arrived. The ledger already holds both: each judgement's `cites` (what the conclusion rested on) and each link's `seq`
   (when a piece arrived). This slice builds that reading rule. Nothing leaves the ledger: "in force" is unchanged, and
   the PRD's repeat / replace / new rules and rejudgement triggers are untouched.

## 2. The rule (judging-v5, config poc-v30)

A judgement of thesis V at round `seq` is shown, of the evidence in force under V:

- **arrivals**: every piece linked to V (a replacement is linked at its own seq) after the READINGS-th most recent judgement
  of V, or everything when V has fewer than READINGS judgements: a piece is read in its first five judgements;
- **basis**: every piece cited by one of the last BASIS judgements of V: the material the standing conclusion rests on.

READINGS = 5, BASIS = 10. Everything else in force is not shown; the request states how many such pieces there are and that
the previous conclusion carries them. The answer may cite and push only shown ids (the closed set is what was sent, read back
from the request text as the theme block already is). Theme block, dependencies, previous conclusion: unchanged.

Measured on two stored ledgers (`census.py`; judgements after a thesis's first; "hidden cite" = a citation the judge actually
made that the rule would not have shown):

| ledger | judgements | in force, mean (≥50) | shown under the rule, mean / max (≥50) | judgements with a hidden cite | hidden cites |
|---|---|---|---|---|---|
| nvda-3m (to 08-14) | 325 | 224.6 | 95.0 / 193 | 22 (7%) | 57 of 3,853 (1.5%) |
| theme-r5 | 261 | 177.9 | 109.3 / 187 | 7 (3%) | 34 of 2,968 (1.1%) |

The hidden cites are third-party risk mentions the judge listed in a "pull the other way" sentence (e.g. a Motley Fool note
that inference favours custom silicon, cited for the first time seven judgements after it arrived). Tighter rules were measured
and rejected: "cited last time + new since" hides 16% of cites; "ever cited + last three readings" hides 2% but the set still
grows with everything ever cited (149 of 574 for v6). Bounded: the basis is at most ten judgements' cites, the arrivals at
most five judgements' links.

## 3. State × event (thesis V)

| state of V | event | shown | written |
|---|---|---|---|
| unjudged | first judgement | all in force (arrivals since the beginning); `hidden 0` | judgement with cites |
| < READINGS judgements | any judgement | all in force | judgement |
| ≥ READINGS judgements | new evidence linked / replacement written | arrivals (link seq after the READINGS-th last judgement) ∪ basis (cites of the last BASIS judgements) ∩ in force | judgement |
| ≥ READINGS | theme changed → propagation (no new evidence) | basis ∪ arrivals still inside the window | judgement (reads the theme block) |
| ≥ READINGS | a cited piece replaced | the old piece is not in force: not shown; the replacement is an arrival (with its predecessor as context) | — |
| ≥ READINGS | a basis cite older than BASIS judgements, never re-cited | leaves view; stays in force; counted in "not shown" | — |
| any | answer refused (cite / push outside the shown set) | retry with the note, same shown set | retired answer (D197 follow-up) |
| any | round resumed after a crash | same ledger → same shown set; the check reads the ids from the request that was sent | — |
| any | judging-v4 ledger continued under poc-v30 | the first v5 judgement computes basis from existing v4 judgements' cites | — |
| any | prompt version < 5 | in force, as before (gated like the theme block) | — |
| closed | — | not judged | — |

## 4. Value × reader

| value | writer | readers | effect |
|---|---|---|---|
| request evidence section (`[Evidence in view …]`, `[Not shown: N …]`) | `judging._lines_english` (v5) | the model; `check_answer` via `evidence_shown_in(request_text)` | smaller closed set |
| `judgements.cites / pushes` | `_record` (unchanged shape) | service, UI bundle, reports, trace, census | unchanged; cites are now within the shown set |
| `store.evidence_in_force` | unchanged | eligibility (`bool(evidence_in_force)`), v4 check, service | unchanged |
| `store.recent_judgements(view, n)` | new, read-only | `evidence_in_view` | — |
| config `poc-v30` (rejudging judging-v5) | new | replay (`--config`), manifests (environment key) | switch at a day boundary: a new day writes a new manifest |

## 5. New path × old checks

| check | old path (v4) | new path (v5) |
|---|---|---|
| cites within the thesis | in force | shown (request text; when the text is not given, computed from the ledger) |
| pushes within the thesis | in force | shown |
| cites_views, theme_pushes, rung, changed | unchanged | unchanged |
| retry note "citing only the listed ids" | holds | holds |
| preflight | does not rebuild judge requests (noted 2026-10-26) | same |
| `tests/test_theme_block.py` (v4) | pass | pass unchanged (v4 reads in force) |

## 6. Prior decisions

D191/D195 (theme block: one to all; themes are conclusions, never evidence) — untouched. D59 (memo theses without evidence
stay unjudged) — eligibility unchanged. 06-views step 7 "rejudge only open theses whose inputs changed" — triggers unchanged;
this rule changes what the judgement reads, not when it runs. No decision rejected a bounded reading; D198 records this one.
