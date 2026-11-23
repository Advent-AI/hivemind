# Claude's merge proposal, written before reading Codex's

**The split.** The old system decides which questions exist; the new system handles the evidence.

| Piece | From | Why (measured) |
|---|---|---|
| Opening questions | Old (poc-v118 extraction, matcher, collision judge) | It serves 10 of 32 frozen matters, against the new system's 2–3, and holds the core figures |
| Extra questions the old system misses | New Step 1's own openings, only after fix 1 (a refused thesis is not open) | The census found the new system raises capex across five hyperscalers, DRAM, neocloud commitments and the Groq review, then loses them to the refusal cascade |
| Answer choices | Old's rungs on old questions; the new ladder for new questions | Old questions are single-figure and already carry rungs; the new ladder drops bundled theses |
| Reading articles and extracting evidence | New Step 1 (c8), with the old system's open questions shown as its open theses | It holds more of what matters (helpful 211–214 against 162–171 of 234) and keeps unlinked facts (D383) |
| Earlier versions and repeats | New Steps 2 and 3 (Jev, grouping) | 141 of 143 earlier versions found; repeats grouped |
| Judging | The frozen judge (the same in both systems) | Differences come only from what reaches it |

**The wiring.** Each day, the old system's views opened up to that day are converted into Step 1's open-thesis shape (id, description, outcome,
period) and given to Step 1 as `initial_theses` or added to its open list. Step 1 files the day's evidence under them. Steps 2 and 3 run as
now. The judge judges the old questions with their old rungs, on the new evidence.

**A small test** ($0 sources where possible)
- **Questions:** taken from the stored old-1 run (`poc/data/comparison-2026-11-17/run/old-1/prod/views.sqlite`), each with its opening day
  and rungs. The old system is not re-run.
- **Window:** a slice, for example 09-07..09-20 (410 kept articles), with old-1's questions open as of 09-06.
- **Evidence before 09-07:** the open problem is that the judge needs it.
  - One option is to start the slice earlier.
  - Another is to replay new Step 1 over July–August with old-1's open lists (about $21, too much for "small").
- **Compare:** the hybrid's judgements against old-1's own, on the same questions, read by the same card readers. Is each judgement
  supported, and is its material cleaner? Also count how many new-only questions the new system adds.

**Questions for the council**
1. Is the split right, or should the new system open everything with the old system's question rules added?
2. The smallest honest test, and what it can decide.
3. Its attainable outcome, computed before any send.
