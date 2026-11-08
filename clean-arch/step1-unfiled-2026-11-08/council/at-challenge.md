Council A on the next class, link clutter (read-only; same thread). Alex adopted c8 (D387) and chose "先花几分钱查原因" for link
clutter.

What I did:
1. Blind recheck (LOG §44): of 93 fresh links, about 72 useful, 19 weak, 2 wrong.
2. Model's own account (`poc/data/clean-acceptance-2026-11-09/judge/link-account.json`, $0.09): the 21 weak or wrong links plus 3
   useful controls, with the verdicts hidden from the model. In almost every weak case the model says, unprompted, that the statement
   "would not change an experienced analyst's view". Its reasons for having linked anyway:
   - "same subject and scope" coverage (Hugging Face facts filed to the deal-closing thesis);
   - word or theme overlap ("the only thesis naming Rubin"; "same month, same AI-infrastructure financing theme");
   - an inference chain ("backlog → GPU orders → Rubin revenue").

   The instructions it quotes:
   - "Link one statement to every thesis it informs";
   - §2 EXISTING "if an open thesis covers the statement, link it…";
   - "Do not exclude evidence solely because it concerns a related period, population or product variant";
   - the closing's customer/supplier "bears on demand / supply" clause;
   - the supply-chain example "Link the announcement as a potential supply signal".

   Even the 3 controls are described as restating the thesis's own premise.

**Mechanism (my reading).** The prompt asks for links by coverage of the subject. The closing check reads back only the items with
empty links ("Then read back each statement you return with empty links…"); it never reads back a link. Closing line 16 even pushes
toward linking: "an item an open thesis covers is linked there, not left without links." Asked afterwards, the model judges the links
correctly. This is the AGENTS §6 lesson: "in one pass the model keeps what looks like evidence…; asked afterwards it judges
correctly. So a closing check reads the list back."

**Proposed single change (arm c9 = c8 + this), in the closing check only:**
- line 16: "an item an open thesis covers is linked there" becomes "an item that informs an open thesis is linked there";
- one sentence added after the empty-links read-back: "Then read back each link: keep it only if the statement makes that thesis's
  answer more or less likely, or bears on a condition that decides it; a statement that shares the thesis's subject, company or
  product but would not change its answer goes without that link, and is kept without links if it is material."

Sources:
- standard §5.1 (evidence "makes some question's answer more or less likely");
- D383 (kept without links);
- the reader test used in acceptance.

Growth is about 330 characters. I would cut "including contrary facts"? No: contrary facts must still link.

**Proposed probe ($0 then cents).** Re-send the stored c8 requests of the fresh articles that carry links (the same before-states)
with c9's closing, 1 draw, then measure:
- (a) of the 21 weak or wrong links, how many disappear;
- (b) of the 72 useful links (59 right plus the 13 the recheck called useful), how many are kept;
- (c) helpful items and theses unchanged.

Falsifier: c9 loses more than 3 useful links, or fails to drop at least half the weak ones, or changes any theses. The fresh set
becomes exposed for this class, so a later acceptance of c9 needs another unused set.

Challenge, in under 450 words:
- Is the mechanism right?
- Is the change the smallest structural one, and is anything in it unsourced or wider than the standard?
- Counterexamples it would break: contrary facts, the founding evidence of a new thesis, a supplier's capacity under a supply thesis.
- Are the probe and the falsifier adequate?

End with AGREE (with changes) or DISAGREE.
