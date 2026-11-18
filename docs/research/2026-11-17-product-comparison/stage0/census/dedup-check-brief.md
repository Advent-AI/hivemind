# Council check of the matter list before it is frozen (read-only, $0)

**Context:** the blind matter census of the release comparison (plan `../../RUN-PLAN-v10.md` §1.3; D668, D670) read the 410 kept articles.
- Two families read them apart in 22 closed sessions. Each family merged its own lists, the two families were reconciled pair by pair, and
  third readers judged the one-family matters.
- That gave 38 entries (`matters-entries.json`). The pair-by-pair reconciliation left same-bet entries apart, for example three entries for
  NVIDIA's Anthropic IPO investment that differ only in their deadline.
- **A de-duplication step was added** (`census_merge.py dedup`), before any system output exists. Both families group the 38 entries by
  D248's one-bet rule, and entries grouped by either family become one matter, so no matter is counted twice. The count under agreed groups
  only is reported beside.
- **Result:** N = 30, or 33 under agreed groups only (`matters-final.json`, listed in `matters-final-list.md`), with 7 company-figure matters.

**Check, reading the files and the source articles where needed** (`batches/*.json` hold the article texts by number):
1. Is the de-duplication rule (merge on either family's grouping) faithful to D665's "the grouping of repeats, what counts as the same
   question" and to D248? Or should only agreed groups merge?
2. In `matters-final-list.md`, is any remaining pair still one bet, counted twice? Look in particular at the 2026 and 2027 hyperscaler capital
   expenditure entries (five companies, four companies, data-centre only, Alphabet alone).
3. Is any merged group in fact two bets (for example, the Hugging Face group)?
4. Anything that would let the list move after system outputs are seen.

End with `FREEZE` or `CHANGE: <the smallest changes>`. Under about 400 words. Do not open anything under `/private/tmp` or `~/.codex/memories`.
