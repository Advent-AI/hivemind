The c12 probe was sent: `poc/data/clean-q12-2026-11-09/probe-c12/records.json`, 84 calls, $0.94, 0 errors.

**Lines** (probe-frozen.md):
1. **FAIL.** On A, c12 writes the cash-flow sentence 0 of 3, the same as c8.
2. **Pass.** On B, c12 keeps neither cash sentence in any draw. c8 kept both, unlinked, in 1 of 3.
3. **FAIL, by one item.** i307 went from 2 of 3 in c8 to 1 of 3 in c12 on the q17 China case, while i304 went from 1 of 3 to 2 of 3 on the
   same case.
4. Not run, since line 1 failed.

Prompt tokens averaged 9,656 for c8 and 9,693 for c12.

**Traced** (`clean-arch/q12-capex-2026-11-09/account-c12.json` and `capability-c12.json`):
- **The fixed account question, asked of each c12 answer on A.** In 3 of 3 the model cites the changed clause, "when it informs no open
  thesis", and says "No open thesis takes it".
- **A direct question on the same answer:** does any open thesis ask about a figure that follows from these two figures by a standard
  definition? 3 of 3 say yes, name v12 and derive Q1 capex of about $1.7bn.
- v12 is in the payload in every draw.

**My reading:**
- The wording hypothesis is refuted.
- The model has the derivation, but does not apply it in the one reading pass. Asked afterwards, it applies it. This is AGENTS §6's
  pattern: "In one pass the model keeps what looks like evidence and cites a rule afterwards; asked afterwards it judges correctly. So a
  closing check reads the list back…".
- Under D355 the line stops and goes to Alex.

**My proposed recommendation to him:**
- **The arm.** Move the derivation test into the closing check: before leaving out a statement of the company's own figures, check
  whether an open thesis asks about a figure that follows from it by a standard definition; if so, return it linked there. The c12
  CONDITION edits are reverted except the scope fix, "informs no open thesis".
- **The test.** The same 14 cases and lines, about $0.9.

**Challenge it** (read-only, under 250 words):
- Is the reading right, or is there another mechanism? For example, the closing check reads back only statements returned with empty
  links, so a sentence never returned is never read back.
- Is the proposed closing-check sentence a fit to the bench?
- Should line 3's one-item swing count as a regression or as sampling?
