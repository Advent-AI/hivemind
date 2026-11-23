Council A for a prompt change before its first send. Read-only, fresh reader, under 450 words. Repository /Users/lchingen/hivemind.

**Read:**
- `clean-arch/q12-capex-2026-11-09/DESIGN.md`, `probe-frozen.md` and `q12_probe.py`;
- `account.json` (the model's own account, three draws);
- the diff between `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt` and `c12-system.txt`, and between `c8-closing.txt` and
  `c12-closing.txt`;
- AGENTS.md §6 (writing prompts) and §8;
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` §11 (Alex's rulings of 2026-11-08, his exact replies).

**Context:** Alex chose to fix q12 (capital spending) after Stage 2 of D392. The option he picked said it changes the frozen c8.

**Check:**
1. **Does c12 trace to its sources?** Alex's ruling, the standard (AGENTS §8) and c8's own "every thesis it informs". Or does it add
   a rule, widen beyond the ruling, or fit the bench? Is the example (two reported balances give the change between them) general and
   harmless?
2. **Could c12 break Alex's ruling** (case B), or make company figures link to theses they do not inform? Name the likely regressions
   and whether the probe's lines and cases guard them.
3. **Is the probe sound?**
   - The c8 arm is the stored sent request; the stored request is checked to be c8.
   - c12 swaps only the system text and the closing check.
   - The lines are decidable and the cost is labelled as an estimate.
4. **Anything missing before the send?** The prompt audit rows, a synthetic answer (the schema is unchanged, so the code checks
   accept the same answers), size growth (+157 characters, with its reason).

**Out of scope:** the frozen ruler, the judge, the opening rules (D389, D390).

End with SEND or BLOCKER.
