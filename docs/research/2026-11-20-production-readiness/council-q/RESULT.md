# Council Q: would an analyst use poc-v118's library? (2026-11-20; consensus in round 2; $0)

Alex, asked to read the served 09-20 library himself: "dont' you take a look for me let the council tak ea crack at it". Record:
`brief.md`, `library-pack.md` (the served library as text), Codex round 1 `codex-r1.md` (thread `01a1fba6-8066-7031-9a26-da22b7dcbd3d`,
read-only, memories off), Claude's read written before reading Codex's `claude-r1.md`, round 2 `round2-brief.md` and `codex-r2.md`.
Both readers are models; no person has read the output yet.

## Answer
**PARTLY.** An analyst would use it to find what happened, who said it and the source, and to check milestones. They would not use
its number answers, because linked number questions contradict each other.

## What both readers found
- **Most useful:** the evidence is faithful. Every claim checked against its article was right (Claude 10, Codex 10; one Codex "wrong"
  is the $12.9B Hugging Face total, which the 8-K splits as $11.9B plus up to $1.0B retention). Settled events are right on primary
  sources: v4 (Vera Rubin production shipments began in August, earnings call and 10-Q), v34 (8-K: agreement signed 2026-09-02), v3.
- **Most unsatisfying:** v9 (FY2027 Data Center revenue) carries Q4 Data Center at about $146B while v14 (FY2027 total revenue)
  carries all of Q4 at about $127B. v9's "market reference" of $414B is its own estimate of 09-12/13 relabelled from 09-15, and on
  09-20 it moved a band on a SemiAnalysis forecast dated 07-26. Also v8 against v16 (CPU), v35 against v14 (FY2028 base), and v21
  applying the FY2028 70% outlook to FY2027.
- **It recurs in all three draws** (read at $0 through `bundle.library` at 09-20): old-1 Data Center Q4 about $126B against a total
  Q4 of about $112B; old-3 a total of about $446B against Data Center of about $375B (an 84% mix, weaker evidence).
- **Mechanism:** no question has a dependency and no judgement cites another question (0 of 139 questions, 0 of 4,932 judgements
  across the three draws). Each number question is judged alone. The missing piece is decided and not built: D368 item 2 (Alex,
  2026-11-05: "2. 做"), D51 and D191 point 2; D368 item 4 sets the direction: the broader (root) question reads its narrower
  drivers' conclusions.
- **Also:** duplicates (v1/v2, v3/v22, v30/v31, v14/v21, v17/v35, v8/v16); small or non-NVIDIA bets (v11, v13, v19, v25, v26, v32,
  v36, v38, v41, v42); missing bets (the next quarter, Blackwell volumes through the Rubin transition, AMD and customers' own chips,
  China revenue); v6 overrides the $1.08T consensus with NVIDIA's own top-five $1.3T scaled to four; v5's figures are total capex
  for a data-center-capex question; v15's band rests on an unsupported $28B; v43's Yes rests on the target close date; 4 of 25
  sampled uncited evidence items worth keeping (Codex, one sample); the page opens on the newest questions.

## Recommendation (consensus) and one test
Do not build the daily wrapper yet: a daily refresh would deliver the same contradictions every day. First close the cross-question
contradiction with the decided dependencies. It changes frozen matching and judging, so it is a new version Alex opens.
1. **$0 first:** render the exact judging request in D368's direction (the total-revenue question reading the Data Center
   question's conclusion, `views/judging.py` `_lines_english`) and check that the decisive figures (Q4, the reference) survive the
   600-character cut.
2. **Then a few cents, only if they do:** re-judge the three draws' linked revenue questions at 09-20 with the dependency, three
   samples each beside fresh unchanged controls. Pass: source-backed quarterly figures that reconcile (Data Center never above total).
   Misleading if a forced mix or a later answer fed back manufactures agreement.
