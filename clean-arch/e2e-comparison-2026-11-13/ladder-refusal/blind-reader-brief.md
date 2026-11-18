# Blind reader: main figure or event, a candidate rule, and its consistency (read-only)

Repository `/Users/lchingen/hivemind`. You see only questions and their tracked outcomes, no system answers: `clean-arch/e2e-comparison-2026-11-13/ladder-refusal/blind-cases.json` (12, ids q01–q12).
Rules to read: `clean-arch/step4-2026-11-10/ladder/candidate-system.txt` (the whole file; lines 5 and 6 decide this), and the owner's ruling
D436 in `docs/DECISIONS-log.md` (search "## D436"): a second side of the same bet is one question, kept as context and shown as not judged.

**A.** For each case, from its outcome text: "one main" (one figure or event is what is tracked; the rest explains, compares, is a component
of it, or is another side of that same bet) or "none main" (several things an analyst would track separately, none primary). Name the main one.

**B.** A candidate clause would be added inside line 6's first refusal case: "… or naming several that an analyst would track separately, none
of them the main one; a component of the tracked total, a comparison with it, or another side of the same bet beside the tracked figure or event
is not a second main one: judge the tracked one and list the other in not_judged." Apply the current line 6 and then the candidate, as a careful
model would, to each case: does the candidate change the decision (refuse → ladder or ladder → refuse)? Flag every case where the candidate
could make a model treat two independently tracked things as one ("same deal, both important"), or keep refusing a case that has a main one.

**C.** Read the whole request with the candidate in place: does the clause contradict, widen or narrow line 5, the rest of line 6 or D436?
Quote the words at issue.

Return A and B as one JSON object per line: {"id": "q01", "verdict": "...", "main": "...", "current": "ladder|refuse", "candidate": "ladder|refuse",
"risk": "<null or the words that could mislead>"}; then C in at most 150 words. Out of scope: changing files.
