# Independent review of a two-system comparison (read-only, $0). Read the primary material cold; no conclusion is offered to you.

Alex spent two days and about $145 on a release comparison of two pipelines that read the same NVIDIA news, 2026-07-01 to 09-20:
- the **old** system: production `poc/config/poc-v118.json`;
- the **new** clean system: `clean-arch/PRD.md`, Step 1 c8, then Step 2, cases, ladder and judge.

The result is that the new system loses badly on the frozen rule. Alex asks: **did we measure wrong, or is the result real, and why did
we spend two days to get it?** Answer from the files, citing file and line.

**Material**
- The plan: `docs/research/2026-11-17-product-comparison/RUN-PLAN.md` and `DESIGN-1.6.md`.
- The rule: `stage0/verdict-rule.json`.
- The matter list: `stage0/census/matters.json`; how it was built: `stage0/census/`, `stage0/exposure_census.py`, `stage0/classify_reads.py`.
- The run log, last entries: `RUN-LOG.md`.
- The decisions: `docs/DECISIONS.md` D382, D384, D489–D491, D505, and D665–D675.
- The diagnostic reading of the five finished runs: `poc/data/comparison-2026-11-17/reading-diagnostic/`.
  - `mapping-out/library-L*.json` are each run's questions at the cutoff, with the labels in the mapping key.
  - `mapping-out/map-*`, `mapping-out/third/` and `mapping.json` are the readers' mapping.
  - `deck/C*.txt` and `deck/round-*` are the cards and the marks.
  - `deck/readings.json` and `diagnostic-count.json` are the readings and the count.
- The per-matter trace: `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/full-trace.txt`.
- The runs, finished and not live: `poc/data/comparison-2026-11-17/run/{old-*,new-*}`.

**Questions**
1. **The ruler.** Is the matter list fair to both systems?
   - How were the 32 matters chosen?
   - Does the way they were chosen favour one system's design?
   - How many are things the new system's own rules forbid it to open, and was that known before the run?
2. **The reading.** Are the mapping and the card marks right?
   - Check a sample of the old system's served cards and of the new system's non-served matters against the libraries.
   - Is there any matter where the new system holds a question that should cover it but was mapped out?
3. **The runs.** What do the new system's questions spend its question budget on, compared with the old system's?
   - Are they big matters by its own rule (D384)?
4. **Predictability.**
   - Given D382, D489 and D505, could the outcome have been computed before the run?
   - What did the plan say about the company-figure matters?
   - What was the highest score the new system could reach under its own rules?
5. **The one thing** that should be done next, with the evidence for it.

Reply in under 500 words. Separate what you checked from what you infer. Do not open anything under `~/.hivemind-keys`. You may read the
mapping keys' draw labels only to name the runs.
