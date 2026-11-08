# Reflection after the c8 acceptance (Claude, written before the council; 2026-11-09)

## Results, regressions first

- **My dissent on theses.** By my reading the fresh run wrongly opened 3 theses, not the readers' 1:
  - clean-9, global semiconductor revenue;
  - clean-10, NAND demand from CMX.

  The readers called both allowed shared quantities. By my count the line is missed; by theirs it is met.
- **Links on the fresh set: 59 of 93 right (63%).** Of the 34 not judged right, I read about 25 as real errors, where an item is
  linked to the topically nearest open thesis. About 9 look like reader strictness: the founding announcement of the thesis, and
  memory-cost margin pressure linked to the DRAM price thesis.
- **Dev question measure** (one reader per draw; must_open covered / opened must_not):

  | | Covered | Must_not |
  |---|---|---|
  | Draw 1 | 25/28 | 0 |
  | Draw 2 | 24/28 | 1 (lidar again) |
  | Draw 3 | 27/28 | 0 |
  | c7 | 27/28 | 1 |

  - The Ohio-guarantee yes/no question is not covered in any draw; the broader credit-support amount thesis is opened instead.
  - "None" theses: 1, 3 and 5. Draw 3 opened a merchant inference-chip startups revenue thesis, which looks small.

## Lines met

| Line | Fresh set (50 unused news articles, 09-05 to 09-07) | Dev ×3 (frozen gold, a lead) |
|---|---|---|
| Helpful | 132/139 (95.0%); core 83/83 | 214 / 211 / 212 of 234 (line 190); core 85–86/86 |
| Wrongly opened theses | 1 (readers) | see the question measure above |
| Search | 141/143 pairs (98.6%) | 99.0 / 98.9 / 100.0% |
| Wrong merges | 1/57 (1.8%) | 1/100, 1/100, 1/106 (1.0 / 1.0 / 0.9%); every dispute judged by a third reader |
| Detail retention | 22 = 22 (structural) | not run |

Gold not-kept spans kept on dev: 27, 27 and 30, against c7's 30.

## What I learned (mechanism level)

1. **The loop's biggest single error this round was mine.** I widened a ruling of Alex's (on cash) into a blanket rule. A blind
   whole-request audit caught it. The audit is worth its cost every time.
2. **"No run has used" must count the old pipeline's whole-window runs.** My first July set would have been an exposed set dressed up
   as fresh. Council B caught it.
3. **Reader sessions over 50 articles silently stop after a few.** Batches of ten work, and every output must be checked for
   completeness: `status: incomplete`, and articles missing.
4. **c8's "link to every thesis it informs" did not raise over-linking.** Links per item fell from 0.61 to 0.50, and items linked to
   two or more theses went from 1.8% to 2.7%. Wrong links come from choosing the nearest topic, not from linking to many theses.
5. **One mechanism appears in three places:** Step 1's links, Step 2's later links (§41), and production's open defect 1 (D355). The
   model reads "informs" as "is about the same topic", not as "moves this question's answer".

## The next class I propose: link precision

- **Why it matters.** A thesis's evidence list is what the judging step reads. A third of the links being wrong pollutes the evidence
  each judgement weighs. It is the product's defect 1.
- **What I do not know yet:** the model's own account of a wrong link. Is it pairing pressure (the open-thesis list invites a link),
  the relevance field written after the choice, or the definition of "informs"?
- **Proposed next steps, cheapest first:**
  1. ($0) Census over the fresh set and the dev draws: wrong-link share by thesis kind and by item kind.
  2. (about a cent each) The model's own account on 6 wrong links and 3 right links: continue the stored conversation and ask
     which instruction led to the link and what it rejected.
  3. Only then a design, which goes through the council first.

  Any prompt change is measured against c8 on the same fresh set, plus a new fresh set, never on this set alone.
- **Falsifier.** If the account shows the readers' test, not the model's, is the outlier (the links a hedge-fund analyst would file),
  the class shrinks to reader calibration and no prompt change follows. That case goes to Alex with balanced examples.

## Weaker than it looks

- **The fresh set is 50 articles over a holiday weekend, one draw**, with no NVIDIA posts.
- **The thesis line depends on how wide "shared quantity" is read**, which is where my reading and the readers' differ.
- **Line 3 is structural**: no record's text is dropped, so grouping cannot lose a detail that Step 1 wrote.
- **The search line counts pairs inside reader-made groups.** Big groups, such as the 11 articles retelling the 70% guidance,
  dominate the pair count.
