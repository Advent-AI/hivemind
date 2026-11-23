# Council round 78: settle the recorded evidence-summary disagreement (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## The open disagreement

`docs/research/2026-11-22-number-answers/RELEASE-BUILD.md` §8 records a disagreement from councils 74–74c:
- An evidence summary (`one_line`, written by extraction) can restate a source figure by arithmetic and attribute it to the source.
  Example: `old-1/e3238`'s "NVIDIA projected … more than $40 billion in FY2028", for a quote that says "more than double that next
  year".
- **Codex:** revision 4's "amounts as quoted" requires source wording for such an amount.
- **Claude:** the release computes nothing and shows the stored summary beside its quote.
- **Both agree:** no digit filter, no change to extraction (frozen).
- The course taken was the cheaper reversible one: keep the summary.

The reader's page is now built (`RELEASE-PAGE.md` revision 7, D760; `src/hivemind/release.py` `PAGE_SCRIPT`). Each evidence entry
shows the summary, then the quote, then a detail line, then its sources.

## Claude's proposal for consensus

Label the two texts on the page, so a reader can tell whose words each is:
- before the summary, the visible label "Hivemind summary";
- before the quote, "Source quote".

The summary's figures are then attributed to Hivemind's restatement, and only the quote is presented as the source's words, which
is what "amounts as quoted" protects. Nothing is filtered or rewritten. Extraction is untouched.

This changes the pinned template, so it needs:
- the screen check re-run with a newly frozen expectation;
- a new pin;
- `hivemind-release/3`, per revision 7's rule, since format 2 has been certified.

## Questions

1. Does labelling resolve your position in §8, so the disagreement can be recorded as settled by consensus? If not, what exactly
   would?
2. Is the format bump to `/3` right, or is a pre-release change under `/2` acceptable, given that nothing has been released?
3. Anything the change could break: the screen check's frozen lists, contrast, the not-clipped rule, tests?
4. Verdict: adopt, adopt with changes, or keep the recorded disagreement.

**Out of scope:** everything else.
