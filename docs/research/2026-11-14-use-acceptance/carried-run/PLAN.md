# The product condition, end to end: two weeks with the library kept (D563), written and frozen before any answer is read

**What it is:** the new system as frozen (Step 1 c8, Step 2, topics, the answer-choice step, the frozen judge), unchanged.
Week 1 is the stored run of 2026-09-22..28 from empty (the cold start, 235 articles,
`poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1`). Week 2 is 2026-09-29..10-05, 241 articles never sent
(`manifest-2026-09-29-10-05.json`; text identities in `manifest-2026-09-29-10-05.text-sha256.json`), read by the first step from
week 1's last library (7 topics), first one day (2026-09-29), then the rest from that day's last library. The three parts are
joined (`extension.py`) into one first-step trace over 476 articles; the unchanged runner then runs the matching, topics, answer
choices (three attempts) and judge over the fortnight, regenerating week 1's later steps. A diagnostic: it passes no gate and
compares no systems.

**Proved at $0 before any send:** `proof-output.txt` (19 of 19: the extension reproduces a stored run split in two, by the real
launcher, byte for byte; five mutants refused; the later steps on the joined trace equal the stored draw's; no judge request
holds material first read after its day), `inputs-proof-output.txt` (11 of 11: order and text of the articles; the starting
library and the first request; the date check's own control). These replay every stored answer of the week through the
current code checks of every step (the clean path's preflight).

**Spend:** a new ledger, ceiling **$6.00, fixed**. Priced from tokens at the published rates on the stored week: Step 1 about
$0.0089 an article (week 2 about $2.15); over the fortnight the matching about $1.2, the judge about $0.3, the answer
choices about $0.06: about $3.7 in all; reservations at any moment about $0.3 at most. If the ledger stops, nothing is
raised: the run stops and the council is asked.

**The slice (2026-09-29) goes on to the rest only if:** every article complete (or the one failure the runner goes on after);
no ledger refusal; its cost per article at most 1.5 times the stored week's ($0.0134); its first request holds week 1's
library. Otherwise stop and return to the council.

## The reading (frozen now)

1. **Openings of week 2.** Every topic week 2 opens, read against the library held at that article (the row's starting
   library): `same_question` / `same_matter` / `none` / `cannot tell`, and worth holding (yes / no / cannot tell), by two
   reader families apart, my own marks first. Reported: how many of week 2's openings are on a held matter (with the
   examples), against week 1's openings per article as the reference. Controls: for the articles that opened a topic and
   for a sample of 20 other week-2 articles (seed 20261116), each family lists the matters that deserve a question and are
   neither held nor opened (lost questions), and the statements bearing on a held question left with no link (lost facts).
2. **Last answers.** For every question the library holds at 2026-10-05: its last judgement read against the request it was
   given, in the fresh week's reading B form (supported / unsupported / insufficient / cannot tell), two families apart, with
   planted wrong answers built on requests not otherwise in the packet and supported controls confirmed by a separate reader
   first. Reported apart, nothing leaving a denominator: questions with no answer choices (declined in all three attempts),
   questions never judged, judgements and their marks, unresolved disagreements.
3. **Source to answer, a sample.** For five questions drawn by seed 20261116, each family reads the fortnight's articles
   that the run linked to the question or that the census marked as bearing, and lists the facts that bear on the question;
   each is classed by code as delivered to the last judgement or not; undelivered facts are read against the full last
   request ("would it change the answer, its confidence, neither, cannot tell"). Controls: a known group-level positive (PRD
   10 §2's custom-chip group: 9 of 9 sends left the lowest rung when it was added) and a known negative (a fact already in the
   request). Reported as a sample, never as a rate.
4. **Deck 1** goes to Alex unchanged; nothing from this run replaces it.

No line decides anything here: no 90% line, no pass or fail on reader counts. What would change the next step: week 2
re-opening held matters often (it would mean the library does not hold in a running system), or last answers mostly
unsupported by what they were shown (the judge's material, not the questions, would be the next work).
