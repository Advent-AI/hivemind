# Check the "not a read" classification before it is frozen (read-only, $0)

**Alex chose** (D669, in `/Users/lchingen/hivemind/docs/DECISIONS-log.md`, search "## D669 "): "只排除真被读过的，比9/7–9/20".
- Only an article that a system processed or a reader read is excluded.
- Corpus storage and code-only batch checks are not reads.

**The rule** is in `classify_reads.py` in this folder (its docstring).
- Applied to the exposure census, it keeps 414 of the 502 articles of 2026-09-07 to 09-20.
- Every location it treats as **not a read** is in `not-reads-list.md`: 8 storage, 18 pool lists and 14 code-only.

**Your task:** check every listed not-read location against what it actually is.
- Open the folder and read its producing scripts and what the file holds.
- Do not open `census-out*` or `reads-out` article lists beyond what you need to check one location.
- For each, answer `agree`, or `disagree: it is a read because …`.

**Look in particular at these:**
- **Pool lists:** is any of them in fact a record of articles a run or a reader processed, not only a pool given to it?
- **Code-only:** does any of these scripts call a model, or was its output shown to a person or a reader as article content? For example,
  a review page built from it elsewhere.
- **Storage:** is any `items` table a probe's selection, rather than a corpus build or a run's own copy of its input?

Also name any kind of location the rule classes as a read that should not be, but only if it would change the count by 10 or more.

End with `AGREE` or `DISAGREE: <locations and why>`. Under about 500 words. Do not open anything under `/private/tmp` or `~/.codex/memories`.
