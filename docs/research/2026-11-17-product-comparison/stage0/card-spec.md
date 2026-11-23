# The comparison card (frozen with verdict-rule.json; plan §1.4, §1.5 F; D667)

One card per question to be marked. The same form serves both systems; nothing on it names or hints at the system.

1. **The question:** the system's question text, its due day, and its answer ladder (the rungs or outcomes as the system wrote them),
   normalised to plain text: "Question", "Due", "Possible answers" (one per line).
2. **The latest answer at the cutoff:** the chosen rung or outcome, and the system's own stated reason, as plain text.
3. **The material that answer was given:** each evidence item the answering request contained, as its request shows it (the passage or
   summary, the source's publisher and day). The order is by day, then as the request listed them. System-specific field names are removed.
   No evidence the request did not contain is shown.
4. **The library's other questions:** their question texts in opening order, each with its opening day, so that `duplicate` can be judged.
   Only the later question of a same-bet pair is a duplicate.
5. **The marks asked:** worth (worth / trivia / duplicate); answer (supported / unsupported / insufficient); a reason of at most 40 words.
   A question with no answer by the cutoff is carded with "no answer" and only the worth mark is asked.

**Blinding (amended before any output, D673):** the builder removes every system-specific field, label and formatting:
- the request header's focus string;
- rung stance labels (only each rung's condition is kept);
- matcher and grouping notes;
- evidence ids, which are renumbered per card.

What the system wrote as its question and its rung conditions is its output and is shown as written. A closed reader shown 10 cards of each
stored system (clean-e2e-full c1 and the old system's q1) lists every element of the form, not of the wording, that tells the systems
apart. Each one named is removed and the test repeated until none is named. Differences of wording are disclosed with the result.

**Order and keys:** the cards are shuffled per batch by seed 20261117; the key from card to system and draw is kept outside the repository.
