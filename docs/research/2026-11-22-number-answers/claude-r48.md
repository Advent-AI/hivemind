# Round 48, Claude's own reflection (written before reading Codex's report)

## The result as registered

- 36 scored first attempts, 36 diagnostic retries, $0.3677 spent of $0.50 (ledger: 72 attempts, no refusal by the ledger, not stopped).
- All 72 answers were refused by `calc_check.py`; nothing was published. Every attempt finished (status `answered`), so the result is
  complete, not INCOMPLETE.
- By D725's lines: the joint arm is usable in 0 of 9 pairs. **STOP.**
- The blind reading cannot change this. The registered reader brief says a card with no answer cannot be usable, and every card is
  "no answer". The readers are not run; the packets can still be rendered and sealed at no cost if the record needs them.

## What the result measures

It does not measure the question the gate was built for (does judging a family in one call give better numbers than judging each
member alone?). It measures whether the model can fill v13's answer format as the request states it. It cannot.

## The mechanism (traced on stored answers, both journals)

1. **The format's rules live in the check, not in the request.** The sent schema has 7 descriptions (`what`, `basis`, `kind`,
   `expression`, `relation`, `bridge`, `reference`). These fields have none: `value`, `low`, `high`, `bound`, `unit`, `evidence`,
   `component`, `inputs`, `operation`, `signs`, `disputed`, `basis_text`, `rests_on`, `converts`, `scenario`, and `outcome` and `rung` on
   the answers. The check enforces closed conventions on them that the request never states:
   - `evidence` is a passage id, while the model wrote the sentence (175 figures in the first attempts);
   - `outcome` and `reference.figure` are figure ids, while the model wrote "$398.1 billion" and sentences (45 and 39);
   - `bridge` is a figure id, while its own description reads as prose ("an estimate stating the conversion …"), and the model
     wrote prose (49);
   - `unit` must be exactly `USD bn`, `%`, `x` or `USD`; the model wrote `USD billions`, `$ billion`, `percent` and `fraction`;
   - a figure has a value or a range, never both; a guidance "$108.0 billion, plus or minus 2%" was read as value, low, high,
     bound `approx` and component `midpoint`;
   - a period is labelled `FY2027 H1`, not "FY2027 first half" or "first six months";
   - a percentage is applied with `share` (which divides by 100), not `product`;
   - `range_from_relative` takes the midpoint and the relative figure as two operands;
   - `signs` exists only on `sum` and `roll_forward`, and a four-term difference is a `sum` with signs.
2. **Even with these corrected mechanically on copies, nothing publishes.** 9 of 36 first attempts get past the structural layer, and
   0 publish. The next layer includes:
   - the expression copied with its words ("65% growth in Q4", where the extractor yields "65%");
   - the period vocabulary;
   - `apply_growth` of last year's quarter by a year-over-year growth. The check accepts this without a bridge only when the family
     has a `same_base` relation, and the bridge description's list of identities does not include growth;
   - some arithmetic that follows from the conventions above.
3. **One wrong answer anywhere refuses the whole answer.** An answer carries about 20 figures, and each figure must pass several
   rules. A long conjunction fails by chance even when each part is usually right (AGENTS §7.1, "a conjunction over many items fails
   by chance"). The retries carried every reason, and they fixed nothing: 36 of 36 were refused again, mostly on the same classes (prose where an id
   is expected in 20, value and range in 22).

## My process error

- AGENTS §6: "Check before the send, at no cost. Write one answer that follows the prompt and run every code check on it."
  - I wrote the $0 gate's answer knowing the check's conventions. It proved that the check accepts a conforming answer, not that
    the request teaches one.
  - The step that would have caught this at no cost: an answer written by a reader who sees only the request, run through the
    checks.
- REQUEST-AUDIT.md says "field definitions moved to the schema". Only 7 descriptions reached the sent schema, and I did not check the
  sent bytes against that sentence.
- The eight council rounds (47 to 47h) reviewed the harness: the journals, the keys, the packets and the verdict. None reviewed the
  request as the model reads it against the check.
- The "rests_on prose" diagnosis I gave Alex mid-run was wrong in its field. The prose sat in `bridge`, `evidence`, `outcome` and
  `reference`, not in `rests_on`. I correct it in the report.

## The way forward (my lean, to be challenged)

- The gate as registered says STOP. It is recorded as written (D680).
- What the result can still decide: whether a v13-style calculation can be filled at all. That decides whether the number-answer
  work continues on this path.
- Lean:
  - **(ii) first:** move every decision code can make out of the model.
    - Code extracts each numeric expression from the shown passages and lists it as a numbered source figure, with value, unit,
      bound and period parsed by code. The model only references these by id. This removes the expression, evidence, unit and
      value-or-range classes at their owner.
    - `outcome`, `reference.figure`, `bridge`, `inputs` and `evidence` become enums of the ids the request holds where the strict
      schema allows it.
  - **(i):** every remaining field gets its rule in the schema beside it, including the operation and period vocabulary, and the
    check's too-narrow rules are written down as decisions before any change.
  - **The test, all at $0 before any send:**
    - every stored answer is re-read under the changed contract, and no right answer may be refused;
    - a blind reader who sees only the new request writes answers for three families, and they must pass;
    - then the same 36-request gate, about $0.40, on Alex's word.
  - **Stop condition:** if a blind reader's answers still fail on rules the request states, the format is too heavy for one call.
    In that case close judging-v13 and keep poc-v118 (D690).
- Not certain:
  - (ii) is a new design piece (code builds the source figures), not a wording fix. It needs its own design tables (AGENTS §2)
    before code.
  - Whether Alex wants to spend more on this path is his call.
