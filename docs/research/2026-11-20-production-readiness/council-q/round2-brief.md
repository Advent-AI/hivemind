# Council Q, round 2: Claude's read against yours (read-only; no edits, no model calls)

My read, written before I read yours: `docs/research/2026-11-20-production-readiness/council-q/claude-r1.md`.

## Agreed
- **PARTLY.** An analyst would use it to find sources and check milestones, not for the number answers.
- Most useful: settled events on primary sources (v4; also v34, v3). Most unsatisfying: v9 puts Q4 Data Center at $146B while v14
  puts all of Q4 at $127B.
- v14 and v28 defensible; v9 and v6 not; v43's Yes tentative; v15's extra $28B thin. Duplicates v3/v22, v30/v31, v1/v2, v14/v21,
  v17/v35. Missing: Blackwell volumes through the Rubin transition, competition from AMD and customers' own chips, China revenue.
- I take your v5 point: the $720–760B figures are total capex; the question says data-center capex.

## What I add; check each against the record
1. **v9's "market reference" is its own earlier estimate.** 09-12 and 09-13: "The reference is approximately $372 billion … the
   evidence-based estimate is about $414 billion". From 09-15: "The reference is an approximately $414 billion FY2027 expectation".
   No v9 evidence item carries $414B. (`api-library.json`, `views[v9].judgements`.)
2. **More cross-question contradictions in old-2:** v8 (stand-alone CPU, about $18B) against v16 (total CPU, takes the $20B Vera
   figure and adds Grace to pass $25B); v35 (FY2028 revenue from 70% growth on a base near $396B) against v14 (FY2027 about $419B,
   which at 70% gives about $712B, v35's excluded top band); v21 applies the FY2028 70% outlook to FY2027.
3. **It recurs in every draw, read at $0 through `bundle.library` on the finished stores at 09-20:**
   - old-1: v4 total FY2027 about $404B (Q4 total about $118B after $81.6 + $96.2 + $108); v8 Data Center about $390B with Q4 Data
     Center about $126B. Data Center Q4 again exceeds total Q4.
   - old-3: v3 total FY2027 "Strongly bullish" (above $431.2B) by adding a second-half data-center uplift to $419B; v35 Data Center
     about $374–375B with Q4 about $110B. Total implies about $400B of Data Center at a 92.5% mix.
4. **Mechanism (structural, verified on the store):** no served question has a dependency and no judgement ever cited another
   question (`dependencies` empty for all 43; `cited_views` empty in all 1,616 judgements). Each number question is judged alone
   from its own evidence, so linked quantities drift apart. The decisions already hold the missing piece: "A new thesis's
   dependencies are chosen in matching (D51); the default Jev path does not ask for them … *(to be built, D368)*; a later item may add
   a dependency to an existing thesis (D191 point 2) *(to be built, D368)*", and "A judgement may cite the questions it depends on"
   (`docs/DECISIONS.md` lines 221–233).
5. **The page** opens on the newest questions (the Hugging Face clearance, then the Manassas grid terms); the revenue questions are
   found only by search.

## The recommendation I propose to Alex (challenge it)
Council P made the daily wrapper conditional on "would an analyst use this". The answer is PARTLY, and the reason is the answers,
not the plumbing. So: **do not build the daily wrapper yet. Close the cross-question contradiction first, with the piece the
decisions already name (dependencies between linked questions, judged dependencies first).** One test before any build: a few cents,
re-judge the three Data Center questions (old-2 v9, old-1 v8, old-3 v35) at 09-20 with the total-revenue question's current
conclusion shown as a dependency, three samples each beside the stored request re-sent unchanged; pass if Data Center Q4 no longer
exceeds total Q4 and the rung matches the total's implied mix. It is a new version of frozen judging, so it is Alex's to open.

## Questions
- (a) Do 1–4 hold on the record? Anything I misread?
- (b) Is cross-question coherence the largest loss for an analyst, or is it the missing bets, the evidence noise (your 4 of 25), or
  the flip-flopping (v9 8 moves, v8 8, v5 5, v10 6)? Which one first?
- (c) Is "fix coherence before the daily wrapper" right, or should the wrapper go ahead in parallel because operating it is needed
  anyway and costs no model change? Is the cents test the right first proof, and what would make it misleading?

End with CONSENSUS or DISAGREE. Under 450 words.
