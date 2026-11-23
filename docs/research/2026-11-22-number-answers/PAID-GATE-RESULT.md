# judging-v13 paid gate: result (D733)

**STOP.** Every one of the 72 answers was refused by the code checks: 36 scored first attempts and 36 diagnostic retries. Nothing
was published, and the joint arm is usable in 0 of 9 pairs against the registered 8 of 9.

The result does not answer the question the gate was built for: does judging related number questions in one call give better
numbers than judging each alone? It shows that the answer format, as the request stated it, could not be filled. Most refusals are
rules the request never stated, or checks that refuse right answers. A few are the model's own errors.

- **Run:** `poc/data/judging-v13-paid-gate-2026-11-22/`, sent once (D732) with gpt-6-luna. The ledger records 72 attempts and
  $0.3677 of the $0.50 ceiling: $0.1554 for the first attempts and $0.2124 for the retries. Every attempt finished with status
  `answered`, so the result is complete, not INCOMPLETE.
- **The blind reading** was not run. The registered brief says "A card that has no answer cannot be usable", and every card has
  none, so the readers cannot change the verdict.
- **Council round 48:**
  - `round48-brief.md`;
  - `claude-r48.md`, Claude's reflection, written first;
  - `codex-r48.md`, an independent fresh read-only Codex session that reproduced every refusal from the journals and the requests.

## 1. Census (first attempt → retry; Codex's count, which corrects Claude's)

| Attempt | Arm | Answers | Structure (C7) messages / answers | Stopped at the structure check |
|---|---|---:|---:|---:|
| First | Joint | 9 | 39 / 9 | 9 |
| First | Separate | 18 | 47 / 18 | 17 |
| First | Single | 9 | 13 / 9 | 8 |
| Retry | Joint | 9 | 40 / 9 | 9 |
| Retry | Separate | 18 | 41 / 18 | 14 |
| Retry | Single | 9 | 12 / 9 | 6 |

`check()` returns early after any structure error, so most source, arithmetic and compatibility checks never ran on these answers.

**Prose where the check expects an id**, counted by occurrence:

| Field | First | Retry |
|---|---:|---:|
| `answers[].outcome` | 45 of 45 | 45 of 45 |
| `answers[].reference.figure` | 39 | 32 |
| `figures[].evidence` (139 of them on source figures, where C1 needs a passage id) | 175 | 133 (95) |
| `figures[].bridge` | 49 | 44 |
| `converts`, `disputed`, `inputs` | 3 | 3 |

**Not one of the 90 member answers named a figure as its outcome**, in either journal. This failure alone refuses every answer.
The retries did not repair it. They carried the first attempt's reasons, and the early return had hidden this reason on most
answers.

## 2. Mechanism

1. **The format's rules live in `calc_check.py`, not in the request.**
   - The sent schema carries 7 descriptions: `what`, `basis`, `kind`, `expression`, `relation`, `bridge` and `reference`.
   - These fields have none: `value`, `low`, `high`, `bound`, `unit`, `evidence`, `component`, `inputs`, `operation`, `signs`,
     `disputed`, `basis_text`, `rests_on`, `converts`, `scenario`, `outcome` and `rung`.
   - The check enforces closed conventions on them:
     - ids, not prose, in `evidence`, `outcome`, `reference.figure`, `bridge` and `disputed`;
     - the unit spellings `USD bn`, `%` and `x`;
     - a value or a range, never both (all 52 such refusals gave both);
     - the period label `H1`;
     - `share`, not `product`, for a percentage;
     - each operation's operand count;
     - `signs` only on `sum` and `roll_forward`.
   - The descriptions of `bridge` ("an estimate stating the conversion …") and `reference` ("An external figure, or a calculation …")
     read as asking for prose. The check reads both as ids.
   - REQUEST-AUDIT.md says "field definitions moved to the schema". Most did not reach the sent bytes.
2. **Some checks refuse right answers.** Each case was exposed by replaying a stored answer with the earlier refusal removed on a
   copy:
   - Q1 + Q2 Data Center revenue = "FY2027 first half" is refused, because the period parser reads only `H1`.
   - FY2026 Q4 × (1 + the source's stated 65% year-over-year growth) is refused for want of a bridge. The check excuses
     `apply_growth` only under a family `same_base` relation.
   - $411 billion × 92.5% is computed by `product` as 38,017.5.
   - "well over $300 billion" is refused because the parser starts one word later.
   - $1.05 trillion is compared with bands in billions.
3. **Model errors seen in the sample:**
   - a 15% growth rate supported by forecasts computed from that same rate, a cycle;
   - $25 billion and $18 billion of commitments added, although the source does not establish that the $18 billion comes on top of
     the $25 billion;
   - a full-year residual taken as a forecast. This is a judgement for a reader, not for code.
4. **Diagnostic on copies (Claude's script, labelled a probe, not a count of right answers).**
   - The script mechanically corrected the format classes.
   - Result: 25 of 36 first attempts passed the early structure check, 9 had no structure error at all, and 0 would publish. The
     retries gave the same counts.
   - It guesses links from matching amounts, so it does not show how many answers a repaired request would get right.

## 3. Process error

AGENTS §6 says: "Check before the send, at no cost. Write one answer that follows the prompt and run every code check on it."

- **What the $0 gate proved.** Its passing answer, like the rehearsal's clean fixture, was written by someone who knew the check's
  ids, units and period spellings. It proved that the harness accepts a conforming answer, not that the request teaches one.
- **The missed step.** A writer who sees only the outgoing request writes the answer, and that first output goes through the real
  checks. Each refusal must then point to the sentence of the request that states its rule.
- **What the eight council rounds covered.** Rounds 47 to 47h reviewed the harness. None read the request as the model reads it
  against the check.
- **A wrong field in the mid-run diagnosis.** Claude told Alex the prose sat in `rests_on`. It sat in `evidence`, `bridge`, `outcome`
  and `reference`.

## 4. Council consensus: one recommendation, one test (for Alex's choice)

**Recommendation.** Keep the STOP. Alex opens one bounded repair of judging-v13's request and checks:
- each field's rule goes in the schema beside the field;
- ids, units and choices become enums where the strict schema can hold them (the request already uses an id enum for `cites`);
- the demonstrated period, arithmetic, parser and unit failures are fixed;
- the checks for real scope changes, unstated assumptions and cycles are kept.

Claude first leaned toward having code send the model a catalogue of the passages' numeric expressions. The council set that aside.
The parser's known omissions would become missing evidence, and the catalogue leaves the outcome-link failure untouched.

**Test ($0, before any send).** One blind conformance test, registered before it runs:
1. **Correct examples and broken counterparts are fixed first.** The examples cover a joint pair, its two separate answers, and the
   three singleton shapes. The broken counterparts include a wrong number, a wrong period or scope, an unresolved overlap and a
   circular calculation.
2. **An independent writer sees only the new request** and writes the answers. The writer's first outputs go through the real
   harness without hand edits.
3. **Stop conditions.** The test stops if any correct form is refused, if any planted defect gets through its check, or if the
   writer needs a rule the request does not state.
4. **The 72 stored answers check individual fixes** where the intended figure and source can be identified. A guessed link earns no
   credit.

A clean result earns a request to Alex to send the same 36-request comparison again under a new decision, with D725's lines
unchanged. The alternative is to close judging-v13. poc-v118 is already the product (D690), and the number answers stay a known
defect.
