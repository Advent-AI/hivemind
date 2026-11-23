# Council ir: last read of a request before a final counted probe (read-only)

`clean-arch/step4-2026-11-10/probe-2026-11-10/READING-claude.md` tells the whole story in one page: four sends of a new step's
request. The request as first sent declines the three topics that have no main thing 10 times of 10; every later request wrote
better and declined worse (0 of 4, 2 of 4, 5 of 9). Alex decided (D407 in `docs/DECISIONS-log.md`): one last send, of this arm, then
the build whichever way it comes out.

The arm, in `clean-arch/step4-2026-11-10/ladder/` (`candidate-system.txt`, `candidate-closing.txt`, `candidate-schema.json`), is the
request as first sent (`probe-2026-11-10/sent-system.txt`, `sent-closing.txt`, `sent-schema.json`) with exactly these changes:
1. the reference's words "are copied from the item exactly, as one unbroken passage …" (alone, it left the refusal at 3 of 3);
2. "The question is read later by a judge … it must stand on its own …" (alone, 3 of 3);
3. states in two shapes, `company_states` (the label an enum of the five) and `theme_states` (a name), with the two sentences on
   states naming the fields and otherwise as first sent;
4. the closing check exactly as first sent.
There are no `named` and `main` fields.

Do not edit files, run model calls or start runs. Diff the three files yourself. Answer in under 250 words:
1. First line: "send", or "hold" with the exact words or schema change you would make.
2. Is the arm exactly what D407 describes: nothing more in the system text, the closing check or the schema than the four points?
3. Is the request consistent with its schema (every field the text names exists; no text about a field that is gone)?
4. The line set with Alex: the three topics with no main thing declined in at least 8 of 9 sends; the five others answered with a
   ladder in 15 of 15. Anything in the arm that makes that line unreadable or unfair?
