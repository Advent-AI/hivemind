# Prompt audit of the gate-1 candidates (c15yc, c15c, c15o; all three edits together in c15), 2026-11-13

Arms (`clean-arch/step1-unfiled-2026-11-08/arms/`): **c15yc** = c8 + change 1 (years) + change 2 (customers), +311 characters;
**c15c** = c8 + change 2, +105; **c15o** = c8 + change 3 (the `outcome` description in the schema), +292; **c15** = all three, +603
(about 137 tokens, an estimate at 4.4 characters a token; production states the schema at the end of the system text, so change 3 is
read by the model as part of the system text). Change 1 is c14's wording, audited in `PROMPT-AUDIT-c14.md` and read blind twice
(`council/ll-codex.md`, `ln-codex.md`). This audit covers changes 2 and 3 and their interactions.

| request sentence | the standard's line, or the decision | verdict |
|---|---|---|
| c8 line 110: "A customer's deployment plan is evidence for the company's demand and product theses, unless it changes the company's own cash or credit risk, which is judged as an obligation." → "A single customer's …" | standard §5 (evidence): a customer's spending, orders or backlog bears on demand; §3 row D: "几家公司的合计（云厂商资本开支）" is a shared quantity | **c8 keeps wider** where the sentence reaches an aggregate of several customers (the model applied it so in c14 d3 send 3 and draw-d2 step 237); **c15 consistent**: a single customer's plan stays evidence, an aggregate is left to shared_quantity's own tests |
| c8 line 130: "A customer expanding capacity informs demand; it is not a thesis of its own, and not a claim that the supplier has received orders." → "A single customer expanding capacity …; several companies' combined spending is a shared quantity, opened only by the tests above." | as above; §4 opening standard | **consistent**: the tail keeps the supplier-orders point; "opened only by the tests above" keeps an aggregate subject to the opening tests (an analyst's card, a settling date), so it does not open every aggregate |
| schema `outcome`: "The outcome or event being tracked by this thesis." → "The one quantity for one period, or the one event, this thesis tracks. It may name the reference it is measured against, the event's own other outcomes (a later date, an abandonment) and context. A second quantity or event an analyst would bet on separately is not part of it: it is its own thesis when it is a big matter, otherwise evidence." | c8 section 3: "A thesis asks one quantity for one period, or one event"; D38: "a question that needs a number and an event is two views"; standard §4: "另一题：同一件事里答案能分开走、分析员会分别下注的"; D397: extra parts allowed beside the main one | **c8 keeps narrower at the field** (no unit beside it); **c15 consistent**: it states the unit where the model writes the outcome, keeps references, an event's own alternatives and context (D397), and sends a second bet to its own thesis or to evidence (the standard's opening and evidence rules), adding no new rule |
| interacting, unchanged: "Open only matters an analyst would bet on separately; small matters open no thesis" | §4 granularity | consistent: a second matter becomes its own thesis only when it is a big matter |
| interacting, unchanged: the closing check "A new thesis needs at least one kept evidence item" and "Each kept evidence item links to every thesis it informs" | §5 | consistent: a second bet kept as evidence still links to the main thesis it informs |
| interacting, unchanged: schema `description` ("The research question") | — | watch point: the second matter could move into `description`; gate 1's G1-c reads `description` and `outcome` together |

**Principles.** General across companies: the three sentences name no company or industry. Growth: +603 characters for c15, each
edit placed at the sentence or field the model cites or writes; no duplicate removed (c8's four merge passages differ in scope; the
customer sentences each carry their own point). No example added.

**What the audit cannot show.** How the model applies the sentences: gate 1's sends measure that.

## Round 2: the blind second read (`clean-arch/step1-unfiled-2026-11-08/council/lt-codex.md`) and what changed

The second reader read the whole c15 request against the standard. Its findings on the changed sentences, each checked against the
standard's text, and the answer:

| finding | checked against | answer |
|---|---|---|
| "Its figure for another year is a separate quantity" calls a period a different quantity and, read alone, reaches the year after next | standard row D (line 279): "量…自然年的今年或明年。同一个量、同一年只有一个问题" | reworded: "The same aggregate for this year and for next year is two theses when an analyst would bet on each: another period is not another wording." |
| the closing check's "same subject and scope" can make another population a different scope | row D: "同一总量的另一种人群、另一种说法是这个量的证据" | reworded: "(for a shared quantity, the same aggregate, in any population or wording, and the same calendar year)" |
| the `outcome` description lets a later date read as permission to open a second deadline question | line 348 (an open earlier deadline) | reworded: the event's own other outcomes are "judged as part of that event" |
| the `outcome` description's "big matter" is not the whole opening test | lines 297, 308–318 (the opening tests) | reworded: "its own thesis when section 3 says to propose one, otherwise evidence" (c8's own term and pointer) |
| "single" narrows the standard's customer example without a source | line 336 (a customer's deployment plan is evidence); row D (line 279: "几家公司的合计（云厂商资本开支）" is a shared quantity) | kept: the scoping is row D's own distinction between one company and several companies' total; sourced here |

Findings on c8 text the candidates do not change, recorded and not addressed by this gate (one class at a time): a single customer's own
quantity can be a question under D187 (line 295; matching now skips companies off the coverage list, so no product effect today); c8
asks extraction to compare with open theses, which the standard assigns to matching (line 318); no opening reason for a company's major
annual business driver; the fiscal-year and event-deadline rules are not stated.

Sizes after round 2 (characters, against c8): c15yc +346, c15c +105, c15o +342, c15 +688 (about 156 tokens, an estimate at 4.4 characters a token).

## Round 3: the council read (`council/lu-codex.md`) and what changed

| finding | answer |
|---|---|
| "single" in the deployment-plan sentence is not in the standard (line 336), and the standard's allowance of a combined-spending question does not show that every multi-customer plan escapes the evidence rule | the deployment-plan sentence is restored exactly as c8 and the standard have it; the collision came from the capacity counterexample ("not a thesis of its own": every census hit and c14 d3 send 3 cite it), so only that sentence changes, by adding row D's own distinction: "several companies' combined spending is a shared quantity, opened only by the tests above" |
| the counterexample rules out a single customer's own capacity question more broadly than D187 (line 295) | recorded as a c8 finding outside this gate; matching skips companies off the coverage list today, so no product effect |

Sizes after round 3 (characters, against c8): c15yc +332, c15c +91. Change 3 (c15o) is stopped before any send.
