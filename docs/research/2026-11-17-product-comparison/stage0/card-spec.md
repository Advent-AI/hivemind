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

**Blinding:** a reader who sees one card of each system must not be able to tell them apart by the form alone. The builder is tested on
stored draws of both systems (clean-e2e-full c1, the old system's q1) by a closed reader asked to guess the system from the form; a guess
rate above chance on 20 cards fails the builder.

**Order and keys:** the cards are shuffled per batch by seed 20261117; the key from card to system and draw is kept outside the repository.
