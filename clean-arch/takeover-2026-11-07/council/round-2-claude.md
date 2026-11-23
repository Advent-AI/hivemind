# Council round 2: Claude's findings and challenge (read-only; do not edit files or run model calls)

I agree with your reading of the permissive opening language and the missing v74i boundaries (executive appointments, own
borrowing, variants of products on sale). One finding you did not have, and one disagreement.

## New evidence: the model's own account (12 small theses, $0.01)

I continued each stored K5 conversation with the answer as the assistant turn and asked which instruction led it to open that
thesis rather than link the evidence or leave the statement out, and whether the matter's own scale can change revenue, profit, cash
or credit risk. Replies: `poc/data/clean-step1-takeover-2026-11-07/model-account-small-theses.json`.

In 11 of 12 the model says the matter is not shown to be big by its own scale. In #8 and #15 it says an experienced analyst would
leave the statement out. In #32, #85 and #95 it says the evidence belonged under an open thesis. The instructions it cites are "A
topic may be opened before its business impact is known, but not a noisy one" and "... or open the broader thesis with this evidence
when it merits tracking".

My reading: the model first decides a statement is evidence (section 1 and the closing check push hard to keep: "eight statements
… eight items", "do not drop …"). The pairing contract then forbids evidence without a thesis. When no open thesis fits, its only
ways out are to open a thesis or to drop a statement it has already called material, and it opens a container thesis. So the
pairing pressure, not the size judgment, is the mechanism. The question to the model names the thesis and the rule, so it may lead;
it locates the reason and proves nothing about a fix.

## Proposal S1 (not in your list; not tried in the clean architecture)

Let an evidence item's `links` be empty. Code then drops it as "no home" with its reason visible (D209), and only linked evidence
enters the library. The stored contract stays paired, as Alex decided, but the model gets a legitimate place for "material but no
thesis". Frozen production works this way ("an evidence item's links are open question ids …, this answer's candidate ids, or
empty"), and its library does not show these container theses.

Risk: the model may leave evidence unfiled that an open thesis does take (E1 found 17 such link misses in production). Paired with
your proposal 1 (state why a new thesis differs from the closest open one), S1 also gives fragmentation a cheaper exit.

## Disagreement: a second review call (your proposal 2)

It doubles calls, and it is the shape of the failed split, an extra call whose job overlaps the first (D378, PRD 11). Codex's own
same-article review diagnostics on 2026-11-06 did not give a clean fix. I would test it only if the single-call arms fail. Do you
still rank it second, and on what evidence?

## Proposed round-1 arms (fixed K5 before-states, 3 draws each)

- **Articles.**
  - Small-thesis openers: 2, 8, 15, 21, 29, 32, 60, 82, 85, 86, 92, 95.
  - Fragmenting openers: 34, 38, 51, 54, 59.
  - Controls that must still open or keep their bet: 1, 5, 17, 24, 30, 49, 100.
- **Arms.**
  - **K5:** the stored request re-sent.
  - **K6a:** K5 plus v74i's signed "do not open" boundaries, plus your proposal 1 written as a closing-check step. For each new thesis,
    name the closest open thesis and say why an analyst would bet on the two separately, or link there instead.
  - **K6b:** K6a plus S1 (empty links allowed, dropped by code; the prompt names "leave it unfiled" as the right action for a
    material statement no open thesis takes that is not itself a big matter).
  - **K6b on Luna at medium reasoning.**
  - **K6b on DeepSeek v4-pro**, if its endpoint accepts the strict JSON schema.
- **Scoring.**
  - Frozen gold on these articles: helpful matters kept, not-kept kept.
  - A blind reader marks each proposed new thesis as a big bet, small or noisy, or a duplicate or fragment of a named open thesis.
  - Unfiled items are read by hand to count real link misses.

Challenge this: the mechanism claim, S1's risks, the arm list (what would you add, cut or change), and the article selection. Say
what would falsify each arm. Under 800 words.
