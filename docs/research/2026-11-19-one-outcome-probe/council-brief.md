# Council before send (read-only, $0). Under 200 words, ending `SEND` or `DO NOT SEND: <smallest change>`.

This arm acts on mechanism 2 of D676, the bundled questions that get no ladder, inside the rules: D382 is not touched.
- **The change:** one sentence added to the Step 1 closing check (`arm-closing.txt`; the base is the c8 closing). For each new thesis,
  "check that it asks one quantity for one period, or one event, as section 3 says: a thesis that names two periods, several figures or
  several outcomes is rewritten to the one the item bears on most directly, and the rest stays evidence."
- **Its source:** section 3 of the request already says "A thesis asks one quantity for one period, or one event." AGENTS §6 asks that a
  rule applied to each item be checked at the end of the same prompt. The closing check grows by 241 characters.

**The probe** (`probe.py`):
- **Cases:** the six refused theses on key matters (capex in both draws, Anthropic three times, Hugging Face), plus one guard that the
  ladder accepted (Vera Rubin, new-2 clean-2).
- **Step 1:** each opening item is re-sent twice under the arm, with that draw's stored open theses.
- **Ladder:** every returned thesis is laddered once by the frozen astra ladder.
- **Cost:** about $1 on its own ledger.

**Lines, written before the send:**
1. At least 4 of the 6 targets get a single-outcome thesis that the ladder accepts.
2. The guard still opens and is still accepted.
3. The arm returns no thesis on these items that c8 did not.

Check:
- that the sentence traces to the request and the standard;
- that it is general, not fitted to NVIDIA;
- that it contradicts no other sentence.

Out of scope: D382, the ruler, the judge.
