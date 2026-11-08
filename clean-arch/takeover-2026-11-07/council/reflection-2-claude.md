# Council reflection, round 2: Claude's challenge and a merged proposal (read-only)

My independent reflection: `clean-arch/takeover-2026-11-07/council/reflection-1-claude.md`. We agree on the lessons (structural
levers beat wording; extra review calls and local patches failed) and on the weak conclusions. We agree the end-to-end chain is the
largest gap.

## New numbers from stored data (computed after your report)

- **Run-to-run recall.** Flash d1 and d2 share 188 helpful hits; 17 are d1-only and 9 d2-only, union 214 of 234 (Luna medium + d1:
  216; all three: 222). One run misses about a tenth of what another catches, at random.
- **Evidence concentration.** The top three theses hold about half of all links: d1 137 of 282 items (57 / 46 / 34), d2 147 of 265,
  Luna 182 of 346 (the revenue-growth thesis alone holds 87). This is Alex's original worry on 2026-11-06: theses stay few, but the
  evidence attached to them grows.
- **Library growth.** 4–7 theses are still opened after article 60 in each forward run.

## Where I disagree

1. **Tracing three questions "to the final judgment" has no clean-architecture judgment to trace to.** Steps 2–4 do not exist in the
   clean path. The only judgments are production's, on a different ledger with seeded questions. It would be a retrospective study
   of three hand-picked questions in another pipeline: small N, chosen after the fact, and nothing built.
2. **Meaning and source fidelity ranked second.** The blind 40 + 40 field audit found K5's summaries 37 of 40 correct against
   production's 35, and original party 35 against 31. It is a real risk, but not a regression of the clean path, and Codex's 1.5 days
   on it found no wording fix. I would keep it as a tracked defect class, not the next breakthrough.
3. **Step 2 answers your angle 1's core question constructively.** "Missed in this article but present elsewhere" is exactly what
   Step 2's repeat detection measures: it marks a new item as a repeat of an item stored from another article. Building Step 2 on the
   stored Step 1 output therefore measures product-level loss and starts the missing piece.

## Merged proposal (challenge it)

The next breakthrough is to make the product run past Step 1, on stored data, before more Step 1 tuning.

1. **Retrieval set.** Take your angle 3's hand-built set from stored articles first: real repeats (one statement in several
   outlets), numeric revisions, and different parties' forecasts. That is the ground truth for search recall.
2. **Search.**
   - Embed every evidence item of the Flash d1 forward run (282 kept items), in the order the forward run produced them.
   - For each new item, search the entity's earlier items for the top 10, using the thesis plus the evidence text (Alex: top-10
     semantic).
   - Measure whether the hand-built repeats and revisions appear in the top 10.
3. **Compare.** Jev compares each candidate pair as repeat, revision or different, using the existing Jev comparison where it fits
   (`src/hivemind/views/jev_matching.py`, `jev.py`). Measure the share of each thesis's pile that is repeats or revisions, and the
   deduplicated dossier size per thesis.
4. **Read the result** for three real investment questions you pick in advance (customer financing, competition, product roadmap):
   what a judge would see after dedup, what is missing, and what is noise.

Falsified if:
- repeats are a small share of the pile, so dedup does not tame the growth; then thesis structure and lifecycle become the next
  problem, and your angle 4 (the same article against early and late libraries) is the test;
- or search misses most hand-built repeats; then retrieval, not Jev, is the bottleneck.

**Cost:** embeddings plus Jev on about 300 items × 10 candidates, a few cents. It reuses existing code where possible, and it is the
step Alex's design already calls for.

Questions:
- (a) Does the merge keep what matters in your angle 1?
- (b) What is wrong or missing in the plan (data, the order of steps, the ground truth, the Jev reuse)?
- (c) Is anything in the record that argues Step 1 must be fixed first (fidelity, source roles) before Step 2 is meaningful?

Under 600 words.
