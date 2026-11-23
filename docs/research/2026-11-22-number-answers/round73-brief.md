# Council round 73 (decide the two open choices under D439 and Alex's delegation tonight), read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## Context
- **Alex's direction tonight** (quoted in D750, `docs/DECISIONS-log.md`): "这边的决策交给你，还有 Council … 不要 Scope Drift … 把剩下有问题的地方收敛起来，然后准备要往 Production 方向去走了 … 赶紧的往收敛方向去做测量和把它定下来". He is asleep.
- **AGENTS.md, "While Alex is not active, the council decides (D439)":** a choice or next step that would go to Alex goes to the
  council, is recorded citing D439, then executed and measured. The limits:
  - nothing pushed, deployed, published or committed;
  - credentials untouched;
  - paid spending within D439's ceiling (spent);
  - a disagreement the council cannot settle is recorded, and the cheaper, reversible course is taken.
- **D757 left two choices open:**
  1. open release work: build the "Forecast unavailable" release to `docs/research/2026-11-22-number-answers/FORECAST-UNAVAILABLE-DESIGN.md`
     (revision 4, ready per council 72d). It is one allow-listed exporter called directly by the release builder; the POC is unchanged;
  2. §4: non-number questions in the release show (a) answer and label without explanation text, recommended; or (b) partial prose.
- **D726** said the interim "is built with the release work, which is not started". Council 72 said opening release work is Alex's
  call. That was before this question was framed under D439 and his delegation.
- **The open checker defects** in `PAID-V13S-RESULT.md` §5 belong to the v13s line, which Alex closed (D756). No product reader uses
  `calc_small.py`, and the STOP bars tuning on those answers.

## Questions
1. **Under D439 and Alex's explicit delegation, may the council decide to open release work now,** building the exporter, its tests
   and the $0 release check, uncommitted, with the POC unchanged? Is that reversible and within the limits? Or is it still something
   only Alex can launch? Weigh Alex's own words tonight against D726's wording.
2. **Decide §4: (a) or (b).** Is (a) the cheaper, reversible course?
3. **The v13s checker defects:** close as won't-fix (line closed, no consumer), or fix? Fixing a closed line's checker would be scope
   drift unless something reads it.
4. **If release work opens: the smallest first slice that delivers a measured, reversible step toward production tonight,** and what
   must wait for Alex. For example:
   - the Python exporter and package check with tests and mutants, plus the $0 release check on `old-1/v8` and the two event leaks;
   - the UI's rendering of the release data as a second slice.

Return a numbered report with citations and a decision on each question.
