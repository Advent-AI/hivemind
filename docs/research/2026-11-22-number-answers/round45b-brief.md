# Council round 45b: challenge (same thread, read-only)

Thank you. Claude wrote its own reflection before reading yours: `docs/research/2026-11-22-number-answers/claude-r45.md`. We agree on
the root:
- no shared, checked calculation behind related numbers;
- prose answers whose figures code cannot tell from assumptions;
- filing and evidence selection splitting the inputs;
- linking that passed conclusions, not assumptions.

Now settle the disagreements so we can give Alex one recommendation and one test. Answer each, citing files or call ids.

## Questions

1. **The unit of the shared calculation.**
   - Claude proposes one judging call per related family (same company and fiscal year, overlapping quantities). It writes one
     quarterly path, and each question's answer is read from it, consistent by construction.
   - You propose shared dated inputs, with per-question answers and code reconciliation that marks a failure as unresolved.
   - Which removes the 17-of-18 different-Q3-base cases and the $146B/$127B kind? Under yours, two per-question judges can each use
     legitimate but different assumptions on the same shared inputs (midpoint against beat-adjusted Q3). What does the product publish
     then, and how often would that be "unresolved" on the stored data?
   - What does a joint call cost in request size? Use the stored old-2 v9 and v14 requests at 09-20.
2. **Where a figure's identity is labelled.**
   - You put typing at extraction: source, population, measure, period, units, kind.
   - Claude puts it in the judge's structured derivation: each term names its evidence id, and code checks the figure appears in that
     quote.
   - Extraction v74i is frozen (D274), and Alex closed extraction work. Which is necessary for the class, which is sufficient, and
     which is cheaper? Can the judge-side version catch class S (another scope's figure) without typed scope at extraction?
3. **Code owns identity, never importance (AGENTS §2).**
   - List exactly what code would check: figure-in-quote, arithmetic, part ≤ whole for a declared relation, the same input value for
     the same key across a family, a reference that names a shown source.
   - Say what stays the model's: which drivers, how much, discounts, overlap guesses labelled as assumptions.
   - Is any check a disguised importance rule?
4. **D24 and D28 ("no number warehouse"; design from what a thesis needs).** Does either design drift toward a warehouse? What bounds
   it?
5. **Who declares which questions are related.** Is it the link question (presence only, since direction no longer matters under a
   joint calculation), typed keys, or the judge? D711 notes that the keys label stand-alone CPU `other`.
6. **The frozen pieces.**
   - Which versions must Alex open: the judge only, or also extraction or matching?
   - Does the design keep the frozen gold's reasoning? Name the gold questions that test it (q01, q02, q19, q22).
7. **The minimum safe interim for a first release** while this is built. Claude's candidate: publish evidence and events, and show
   number questions without a forecast rung, or as "experimental". Is that right, or is there a cheaper honest interim?
8. **The one test.**
   - Your $0 representation test: reconstruct published calculations under the proposed rules, with the gold as controls.
   - What exactly is the first paid test after it, and what result stops the line? Re-judging stored families at fixed states, joint
     against alone, three draws?
   - Write its pass and stop lines in numbers.

## Output

- One converged design, in five to eight lines.
- The answers to 1–8.
- The one recommendation and the one test for Alex.
- Any remaining disagreement with Claude, stated plainly.
