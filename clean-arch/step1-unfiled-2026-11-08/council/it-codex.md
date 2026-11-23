**Serious — the corrected check accepts quotations that change meaning or join separate passages.** [ladder_step.py:97](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:97) and [extraction.py:216](/Users/lchingen/hivemind/src/hivemind/extraction.py:216):

- Quote `Growth was 10%.` against article `Growth was ≥10%.` is accepted. The quote drops `≥`; the same happens with `>` and `~`.
- Quote `Revenue rose. Profit fell.` against article `Revenue rose.\n\nProfit fell.` is accepted, joining two paragraphs.
- Quote `10` against article `Sales were 100 million.` is accepted as an exact substring. Likewise, `million` is accepted inside `millionaires`. This last weakness also existed in the old exact-match path.

These examples challenge the author’s assertion that no changed or omitted part is taken as the article’s own. The stored passage restores the sign or paragraph break, but the model built its answer from the quote it wrote.

**Serious — D405 does not establish that this broader rule was Alex’s choice.** [D405](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4441) says the strict option required “an unbroken passage” and that “no quote with a word left out” would be accepted. The corrected rule preserves the word-order part for tokens the tokenizer recognizes, but the examples above show it does not consistently preserve an unbroken passage or the article’s meaning.

It also departs from the **Decided** sentence, which permits differences in spacing, letter case, and forms of quote marks and dashes—not arbitrary punctuation and footnote markers. Fixing the footnote example is consistent with the apparent purpose of Alex’s strict choice; treating every ignored sign and boundary as acceptable is a broader interpretation that D405 does not settle. Reporting both counts is appropriate, but does not itself establish approval for that broader behavior.

**Minor — the replay is sound for these stored answers, with a limit on what it proves.** [recheck_stored_run.py:54](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/recheck_stored_run.py:54):

- All seven changed first answers pass the corrected check. The step would therefore take each first answer without sending its stored retry.
- For all 61 first answers still refused for the same reasons, I rechecked the stored second answer: its reasons and, where accepted, its passage are unchanged. The stored second answers can stand as the recorded responses to those same retry requests.
- I found **no send requiring a new call** to determine its outcome under this corrected check. The replay establishes what the recorded answers do under the check; it cannot predict whether a fresh model call would produce the same answer.

**Minor — the tests do not catch every accidental loosening.** [test_ladder_step.py:314](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/test_ladder_step.py:314) covers an omitted word, moved words, an added word and text appended beyond the article. It does not cover the omitted comparison signs, joined paragraphs, or matches inside a word or number shown above. The current implementation accepts those counterexamples, so the existing tests cannot detect those weaknesses.

**Wording — no further clearly wrong refusal identified in the stored answers I inspected.** The remaining refused quotes I found either changed or omitted article words, or could not be located as the article’s own unbroken words. This is an inspection finding, not proof that every possible punctuation or short-quote case works.

**Measurement:** The rechecked outcomes can be used to measure **the corrected check as implemented**, with the original and rechecked counts shown separately. They cannot yet be presented as measuring compliance with D405’s strict quotation choice because of the accepted counterexamples above.

This was a single independent review. The [council skill](/Users/lchingen/.codex/skills/codex-claude-council/SKILL.md) calls for a Claude review and challenge rounds, but your no-model-call instruction precluded those rounds.