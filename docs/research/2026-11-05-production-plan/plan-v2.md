# From the split prototype to production: plan v2 (after round 2)

Replaces v1. Inputs: round 1 (`r1/`), round 2 (`r2/codex-disagreements.out`, `r2/codex-plan.out`, the census `r2/census-findings.json`, Claude's
responses `r2/claude-responses.md`), Claude's checks `r3/claude-diagnosis.md`. Principle from round 2 (plan review 15, AGENTS §1, §6): diagnose
each class on stored data and agree its mechanism before any prompt change or paid send; build the contracts before moving code.

## 1. Contracts to settle first (in this order), each with its $0 proof and accepting test

**C-1. The handover: one statement, one stored piece, every home that takes it.**
- Exact normalised duplicates merge into one piece with the union of links, as `sift` does (`extraction.py` "the same sentence read out
  twice is one piece with both links"); `candidates_with_evidence` re-runs after merging.
- A carries the same unit rule as B and role-v74i ("One evidence item records one statement … a figure, date or comparison in the neighbouring
  words does not make another claim in the same quote new"): 10 of the 15 contained pairs are an A passage holding two statements (diagnosis 3).
  No text-containment identity rule.
- B's no-home passages and A's new questions of the same item: the record-preparation call (which already reads the article and A's questions)
  is given B's no-home passages and may link each to an A question it bears on; code keeps a passage only when linked. Relevance stays the
  model's (diagnosis 2: 1 of 6 in the confirmation run; 1240).
- A merged passage linked to an A question and, by B, to an older-period question of the same quantity: kept as both until matching decides
  the candidate's fate; settled by replaying 1207 with the candidate surviving, merged and dropped (disagreement C3).
- Proof: replay every stored handover of the three runs through the real writer on temporary ledgers. Test: one piece with both links for
  1207, 1211, 1275; a mutant without the merge fails; 1240's Apple passage reaches the TSMC question when preparation links it.

**C-2. Groups as PRD 05 already assigns them** (disagreement C4: decided, not open). A declares new research groups and group references where
the grouping contract calls for them (a deal, a rollout, a policy process; not a company's own financial line), in the same schema shape role-v74i
uses; matching and the writer resolve and preserve them as today. Proof: replay a stored deal and a plain financial line; the first creates or
joins its group, the second carries none.

**C-3. Complete input** (diagnosis 1). Production truncates at 400,000 characters for both paths; 7 corpus items exceed it. The contract: no
silent truncation; a long item is read in sections that each reach A and B with the same snapshot, or is refused with its reason. Proof: 1280's
purchase-commitment note reaches A and B. The choice between sectioning and refusing goes to Alex with the 7-item census.

**C-4. Record preparation** (subject from the listed ids or `new` — built).
- Admission reason from the standard's five (D184); each reason's checks in code with or without a ladder: an annual quantity this or next year;
  an obligation not yet signed checked within 18 months, one already assumed at the next annual filing (D210); events by their dates. Missing
  material or dates never reject (the unnumbered 2026-11-05 record); a claimed settling material is stored, and a known mismatch flagged, not
  rejected (C5).
- `favourable_end` (D186, D368) with code-ordered rungs and monotonic bounds; each numeric rung's interval rendered from its bounds; the bounds
  checked against a stated percentage band where one is stated (A4: the 1280 arithmetic).
- The reference: the pace sentence withdrawn; "the reference the source or evidence gives, such as guidance, a consensus or analyst estimate, the
  last reported figure for the same quantity or a stated target" stays an open list (not exclusive; round 2 A2/14). A floor or a range as the
  reference is the neutral rung's span, not its lower bound (diagnosis 5) — to prove on 1249, 1253, 1273 before adopting.
- Proof: stored record-preparation requests re-sent only after the audit of that request (AGENTS §6) and its replay checks; accepting test:
  code refuses an inverted or non-monotonic ladder on the stored 1239 and 1273 answers.

**C-5. The day runner under D375 and the state × event contract** (round-1 production §3, plan review 12). Sequential items with A and B in
parallel as the reference; the table reviewed against the actual transactions (archive, savepoint, round commit, subject registry). Tests: item
2's A and B both see item 1's committed question; crash and restart between each stage reproduce the uninterrupted ledger; a refused retry, a
configuration change, a corrected input, a competing writer and a limit-cut day each behave as the table says (a cut day is never complete).

## 2. Then diagnose the remaining quality classes (no prompt change before its row is filled)

| Class | Status | Next check |
|---|---|---|
| B files under a broad question when a narrower one is open (about 14) | misread on the accounts (1211 admits v10); the other-period rule applied inconsistently (1246) | prompt audit of B's request (AGENTS §6); candidate: the links test as a closing check in the same request (AGENTS §6 "a test the model must apply to each statement is a check at the very end"); proof on the census cases |
| B parks weak links via the fallback (about 14) | D273, kept by D361 | Alex (§3.2) |
| A writes a question narrower than its source figure (1210) | one case traced | count across runs |
| Attribution, number meaning and uncertainty (about 10) | census | count by field; prompt audit of B and preparation |
| Unverifiable questions (1251) | census | independent reader on the claimed settling materials: unknown / known not reported / supported |
| Coarse and fine readings (C1) | D248 permits the merge; the merged question must carry the finer outcome | replay stored coarse/fine pairs through the writer; check the surviving ladder |
| D197 for spending of another scope (C2) | the five-company total and four-company data-center pair is unproven | independently labelled same-theme pairs (D190 A17 as the merge control) |
| Deal stages (C6) | wording to narrow; "a guarantee beside a financing" example to check against D248 item 1 | stored signing-versus-programme pair |
| Matching's publication day as statement day; Jev repeats on partial overlap | production matching (D354) | Alex (§3.5) |

## 3. For Alex (each with options and a recommendation once Codex and Claude agree)

1. How the split is accepted (D370 retired the seeds the frozen judgement scorer requires): the seeds as a labelled measurement fixture for the
   historical comparison; and an unseeded production-shaped run whose counts (library-level question recall by day, evidence delivered to the
   right question, judgements present and correct) are designed and reviewed before it runs.
2. The fallback sentence (D273, D361).
3. All-open context stays as decided; what he gets is the measured capacity and cost (about 150 input tokens per open question per call) and the
   failure mode when a library exceeds one request, before any change is proposed.
4. A check-date policy for questions without an exact source date, after the state table (estimated date, material arrived or not, no ladder,
   end-of-day closure, later research) shows how pull mode would treat it.
5. Production findings outside the split: matching's said_day; Jev's partial-overlap repeats; D266's run-on summary gap; the 400,000-character
   truncation.
6. The long-item contract (sections or refusal) and the promotion of the accepted split version (D359).

## 4. Corrections to my own changes (round 2 refined)

Withdraw the pace reference; em dash compared as a space only when closed up after a letter ("report—$96.2"), otherwise "-" (with positive and
negative controls); run-on quotes: keep the copied passage only when its summary is re-derived from that passage, otherwise refuse (to prove on the
three stored cases); the fiscal reinterpretation of a bare year only when the question names that same year; year limits by admission reason.
