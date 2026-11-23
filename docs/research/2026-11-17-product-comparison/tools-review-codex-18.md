1. A file can pass both checks and flip the verdict. Start with `base(new_served=5, old_served=1, guard_cards=4)`. Mark `new-1-g-figure-0` and `new-1-g-figure-1` unsupported, with both cards answered in the key. Apply this JSON Patch to the resulting `readings.json`: [Fixture](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/test_score_comparison.py:18)

   ```json
   [{"op":"replace","path":"/cards/new-1/new-1-g-figure-0/answer","value":"no answer"}]
   ```

   I reproduced `practical loss` becoming `practical lead`. Verification also accepts changed opening dates and first-article dates, which changed the reported delay. [Guardrails](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:97) · [Verification](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:304)
2. The recorded dry run passed. A valid writer fixture with one completed draw that opened zero questions was refused because the writer omitted that draw’s card map. The rule calls for `too small`. [Dry run](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/chain-dry-run.txt:1) · [Writer](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/mark_cards.py:309) · [Rule](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/verdict-rule.json:72)
3. Well-formed writer fixtures matched the parent byte for byte across all five verdicts. [Scorer](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:464)

NOT READY: Verify answer presence and opening dates against the deck key, verify first-article dates against the census, and preserve empty draw maps through writing and verification.