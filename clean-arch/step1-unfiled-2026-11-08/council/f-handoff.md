# Reflection council: Step 1 unfiled fix round. Read the whole record cold (read-only)

You are a fresh, independent reviewer. Read-only: edit nothing, run no model calls.

**Read:**
- `AGENTS.md`;
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` (all of it);
- the council files in `clean-arch/step1-unfiled-2026-11-08/council/` except `f-claude.md`;
- the arms in `arms/`;
- the data in `poc/data/clean-step1-unfiled-2026-11-08/` (census, accounts, probe-r1, probe-r2, probe-r2-review);
- the earlier record: `clean-arch/takeover-2026-11-07/LOG.md` §§13–16, and `docs/DECISIONS-log.md` D209, D370, D371, D373.

**Out of scope:** the frozen gold, frozen production, Steps 2 to 4.

**Alex's constraints:** no hard-coding, no prompt overfitted to test cases, and every rule sourced; the test set is reserved for one final
check.

**Agree on:**
1. **Lessons at mechanism level:** what the probes really showed.
2. **Conclusions that are weaker than they look.**
3. **The remaining problems, ranked by product impact,** including whether the test-set miss is a product defect or mostly protocol and
   chance.
4. **One next angle**, with its source, its falsifier, its cost, and whether it is a prompt change, an evaluation change or a decision
   for Alex.

Consider at least:
- the salience of the unfiled rule, which is stated three times;
- improving the instrument first: a separately versioned D371 evaluation, or reader calibration;
- accepting the configuration with the defect recorded;
- a product question for Alex.

Under 600 words. Cite files.
