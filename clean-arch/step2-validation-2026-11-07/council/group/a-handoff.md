# Council A, grouping round: an independent design, written before you see mine (read-only)

**Scope.** The clean architecture's Step 2/3, repeat handling only. Read `clean-arch/PRD.md` §5–§7 and
`clean-arch/step2-validation-2026-11-07/LOG.md` (all of it, including §9). Out of scope: Step 1 prompts, the frozen production
configuration, the frozen ruler (`golden-v5`, which no one edits), Step 4's design beyond what a reader of the dossier sees, and cost
work.

**Alex's decision (2026-11-08, his words: "A 继续；跑council loop 开始做").** When Jev calls an incoming record a repeat of a stored
one, the record is placed in the stored record's group: its source and any missing thesis link are added, and its own text and fields
are kept inside the group. The original is never rewritten.

The forward simulation (`forward_sim.py`, `forward-sim.json`) showed:
- under source-only merging, details are lost (Q2 guidance "assumes no China", Q1 net income and margin, the Taiwan raid on Supermicro);
- 3 clear wrong merges and 6 arguable out of 102;
- 14 missed repeats;
- the Kyber thesis grows to a group of 14 retellings.

Step 4 (judgement) is undefined in the clean PRD; there is no judge to run.

**Design the round.**
1. **The group contract.** What a group holds, and its identity: what keeps an id and what grows. Give a state × event table covering:
   - new;
   - a repeat of one group, or of several groups;
   - a revision;
   - a repeat of one group and a revision of another;
   - a failed comparison;
   - two items from one article matching the same group;
   - the same item replayed;
   - a missing thesis link;
   - a crash midway.

   Say what is written in each cell. Propose the rule for several matches and give your reasons.
2. **What search and Jev compare against:** the anchor's text only, or members too.
3. **What a reader of a thesis dossier sees for a group:** layout, order, how sources are counted, and the independence of repeats
   (PRD §6: several articles do not establish independent sources).
4. **The test.** Alex's open risk is that preserved text is not the same as noticed text, and that a group might be double-counted or
   mislead the reader when it is wrong. Design the cheapest test that would settle whether grouping serves the reader better than
   source-only merging, with no-merging as the full-information control.
   - Use the predeclared dossiers: clean-1 credit support; clean-18 and clean-24 competition; clean-11 and clean-17 roadmap, where the
     Kyber group of 14 is the size case.
   - Specify: who reads, what they are blind to, which questions are fixed beforehand and how, the answer key, the scoring, the size
     budget and the falsifiers.
   - No model judge is being built.
5. **What to build now** (Alex: "开始做"), and where: one owner, real tests, and nothing built that the test could still overturn.

Under 700 words. State what is uncertain.
