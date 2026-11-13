# Council iq: independent read of a change to an answer's shape, before a counted probe (read-only)

Context, in `clean-arch/step4-2026-11-10/probe-2026-11-10/` (`READING-claude.md` tells the whole story in one page): a request was
sent three times on six stored topics. Sentences fixed two classes of fault. Two rules kept slipping: a theme's states took the
company's bullish and bearish labels in two sends of three; and a topic that names two things with neither the main one, declined
4 times of 4 by the first request, was declined 0 of 4 and then 2 of 4 after sentences were added. Alex decided (D406 in
`docs/DECISIONS-log.md`): move those two rules from sentences into the answer's shape, then send eight topics three times each and
read the counts.

The change, to read in `clean-arch/step4-2026-11-10/ladder/` against the third send's request (`probe-2026-11-10/round3-system.txt`,
`round3-closing.txt`, `round3-schema.json`):
- `candidate-schema.json`: two new first fields, `named` (every figure or event the topic's outcome names) and `main` (the main
  one, or null); `states` split into `company_states` (the label is an enum of the five labels) and `theme_states` (a name).
- `candidate-system.txt`: a new first bullet under the question rules ("Begin with named and main …"); the first refusal case now
  reads "main is null"; the states sentences name the two shapes.
- `candidate-closing.txt`: the first test reads `named` and `main` back; the test on a theme's labels is gone (the shape holds it).

The standard: D38 (a view looks at one thing; a theme's outcomes are named, with no bull or bear), D397 (one judged question per
topic, the part its outcome names; a topic with no main part gets none), D399, D403, D404, D405, D406; `AGENTS.md` §2 ("Code owns
identity, never importance"), §3 ("Code over prose"), §6 (the prompt principles).

Do not edit files, run model calls or start runs. Answer in under 450 words:
1. First line: "send", or "hold" with the exact words or the exact schema change you would make.
2. Does the shape carry D397 and D38 rightly? Is `main` a judgement left to the model (which it must be), with code checking only
   that it is one of `named` and that a null `main` means no ladder?
3. Is anything in the request now inconsistent with the schema (a field named in one and not the other; an instruction that the
   schema cannot hold)?
4. Could the new first fields push the model to decline a topic it should answer, such as a yes/no event, or a topic that asks
   several things of which one is the main one (the Ohio guarantee: the signing is judged, the amount and the credit-risk
   condition are listed)? Say which words, and the guard.
5. My proposed reading of "steady" for the counted probe: the three topics with no main thing declined in at least 8 of 9 sends;
   the five others answered with a ladder in 15 of 15; every states ladder in the shape of its object's kind. Is that a fair
   line for six cents of evidence, or does it claim too much or too little?
