# Review of the comparison's reading tools before any output is read (read-only, $0; D672's condition)

**Rule and card:**
- the frozen rule: `stage0/verdict-rule.json`;
- the card: `stage0/card-spec.md` (amended by D673);
- the plan: `RUN-PLAN-v12.md` §1.4, §4.

D672 lets these tools be built during the run, provided a council review finds them faithful before any output is read. The full run is live
and no output has been read.

**Tools** (all in `stage0/`):
- `mapping.py` and `test_mapping.py`: the blind matter-to-question mapping, A2's form;
- `build_cards.py`: the library export and the cards;
- `mark_cards.py` and `test_mark_cards.py`: the deck, the controls, the marking, the debate rounds and `readings.json`;
- `score_comparison.py` and `test_score_comparison.py`, with `mutants-score-comparison.txt`: the verdict;
- `blinding-check-codex.md` and `-2.md`: the card form check.

**Check, citing file and line:**
1. Does each tool do exactly what `verdict-rule.json` and `card-spec.md` say? Look in particular at:
   - covers;
   - third readers;
   - splits and their resolution per counting;
   - duplicates and distinct bets;
   - the guardrail sample (seed, method, pooling);
   - decided denominators;
   - the 10-card minimum;
   - plants (a rung moved, 3 per system, each needing an explicit rejection);
   - supported controls (confirmed first);
   - repeats;
   - the verdict order.
2. Does anything leave a choice to be made after outputs are seen, or let a reader see the system's identity, the key, or another reader's
   mark before the debate?
3. Will the tools run on the real outputs? Both systems' stores are `views.sqlite`. The new system's are under
   `<draw>/judge/draw-<draw>/`, the old system's under `<draw>/prod/`. The judge request format is the same in both.

End with `READY TO READ` or `NOT READY: <the smallest changes>`. Under about 500 words. Do not open anything under `/private/tmp`,
`~/.codex/memories` or `~/.hivemind-keys`, and do not open the live run's folders under `poc/data/comparison-2026-11-17/run`.
