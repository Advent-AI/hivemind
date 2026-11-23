# Council round 50: is the judging-v13 contract too heavy to repair? One recommendation for Alex

You are an independent read-only reviewer. Read the material, then challenge Claude's reflection.

**Context.**
- **D733:** the paid gate. All 72 answers were refused. The format's rules lived only in `calc_check.py`.
- **D734:** Alex chose "修一次再零成本盲测", one bounded repair of the request and checks, then a $0 blind conformance test.
- **Round 49:** a review of the repair design found serious issues (`codex-r49.md`): rules unstated across C1–C10, two unsound check
  changes, wrong test inputs, and a blind test that could pass with no usable answer.
- **Claude's reflection:** `claude-r49.md`, which argues the repair is not bounded and proposes three options for Alex.

All files are in `docs/research/2026-11-22-number-answers/`:
- `REPAIR-DESIGN.md`;
- `codex-r48.md`, `claude-r48.md`, `codex-r49.md`, `claude-r49.md`;
- `DESIGN.md` (the contract and its 30 rounds of history);
- `calc_check.py`;
- `PAID-GATE-RESULT.md`;
- `RESULT.md` (D725's diagnosis).

The decisions are in `docs/DECISIONS-log.md` (D725–D734). The working rules are in `AGENTS.md`: §1, "Then converge or stop"; §2,
"Code owns identity, never importance"; §6, "Never grow a prompt to fix quality"; §7.3, "A failed arm is diagnosed before the next
one" and "a measurement that removes the reason a mechanism exists retires the mechanism".

## Questions

1. Is Claude's claim right that D734's bounded repair is not bounded, so the line should stop and go back to Alex (D355)? Or can the
   repair be finished with a statable schema of reasonable size? Estimate the size and the number of further rounds.
2. Is the "core six checks" list in `claude-r49.md` the right minimum for D725's goal?
   - Which of today's checks are needed to stop a defect D725 named (double counting a total and its segment, two forecasts of one
     quarter, an own forecast passed off as the market's, a source number misread, wrong arithmetic)?
   - Which were added only for constructed cases?
   - Name any check in the six that is not needed, and any check outside them that is needed.
3. Does option (B) keep D725's design intact (labelled figures, checks of identity and arithmetic, unresolved allowed), or is it a
   different design Alex must open?
4. Which one recommendation and one test would you put to Alex now?
   - Choose among (A) finish the full repair, (B) shrink the format to a core set of checks with the rest shown to readers as recorded
     assumptions, and (C) close judging-v13. A better option is also welcome.
   - Give the test's stop condition. Keep in mind that the paid model is gpt-6-luna at medium effort, one pass, about 20 figures an
     answer.

Out of scope: the frozen ruler, `poc/config/poc-v118.json`, D725's pass lines. Be concrete and cite what you read.
