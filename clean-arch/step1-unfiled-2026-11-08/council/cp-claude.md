# Focused call for D388: design (Claude, before the council; 2026-11-09)

**Alex's word.** "试一个单独小步骤 (Recommended)" (LOG §53). He chose it knowing it departs from his "写在同一个提示词里面", and it
authorizes a test, not adoption.

**Why a separate call** (§53). Every same-call arm (c9–c11) moved 4–5 untargeted cases, while c8 agrees with itself on 31 of 32. c8's
request stays byte-identical here, so the main call cannot move.

**The step** (`focused/focused_probe.py`, `system.txt`, `closing.txt`, `schema.json`):
1. **Routing, code, identity only.** Each statement c8 kept and linked to a binding_obligation thesis, open before the article or
   opened in the same answer, is routed. Opening reasons of earlier theses are read from the run's own history.
2. **One call per article.**
   - Inputs: the article (title, date, text); every open thesis plus the theses c8 opened in this answer, flagged as new; the routed
     statements (summary, passages, linked thesis IDs).
   - It is the same model and transport as Step 1: DeepSeek Flash, high effort, JSON mode with the schema in the system text.
3. **System text.** A one-job instruction, then quotations. Code checked each quoted block word for word against c8's system text and
   the D388 record:
   - §3's thesis test;
   - the binding_obligation paragraph;
   - "Open only matters an analyst would bet on separately …";
   - D388's two operative sentences;
   - "Use only this item's information."
4. **Closing check, at the very end (AGENTS §6).** For each statement it writes, in order:
   - `signed_status` (not_yet_signed / undertaken / not_an_obligation);
   - `company_impact`;
   - `large_enough`;
   - `separate_bet`;
   - `already_asked_by`;
   - `opens`.

   Statements about one obligation share one new signing thesis.
5. **Code contract** (refuses, never repairs):
   - one decision per routed statement, and no others;
   - `opens` only when not_yet_signed, large_enough, separate_bet and already_asked_by null all hold;
   - `already_asked_by` is a shown thesis ID;
   - the statements under new theses are exactly the opened ones.

**Each closing-check clause beside its source:**

| Closing clause | Source, word for word |
|---|---|
| "undertaken … (already signed, including a deal already signed under a plan tracked by amount)" | §3 "One already undertaken is tracked by its amount"; D388 "a deal already signed under a plan tracked by amount" |
| not_an_obligation: "another company's matter, the company's own borrowing or leases, a completed or unsized investment, a forecast or a market figure" | §3 "an obligation the company takes on in its own name … Its own borrowing or leases and a completed or unsized investment are not obligations"; the forecast and market-figure words name non-obligations by kind |
| company_impact text | c11's reviewed field description, unchanged |
| "large_enough: true only when the obligation is large enough to change the company's revenue, profit, cash or credit risk" | §3 "large enough to change its revenue, profit, cash or credit risk" (D248 boundary 6) |
| "separate_bet: … an analyst would bet on its signing separately from the total" | §3 "Open only matters an analyst would bet on separately"; D388 "merits a separate investment judgment" |
| "already_asked_by … already asks whether this obligation is signed" | §3 "no open thesis already asks it" |

**Plan** (`focused/plan-r16.json`): the stored c8 answers of the 32 cases, plus Ohio from the dev-d2 and dev-d3 runs.
- 24 articles carry routed statements.
- 3 draws on the decisive cases: Ohio in d1, d2 and d3; fresh-47, fresh-50, fresh-9, fresh-22, fresh-7, dev-1 and fresh-8.
- 1 draw on the other routed articles.
- 44 requests, about $0.21 at published rates (an estimate with 3k output tokens each).

**$0 checks.** A synthetic Ohio answer passes the schema and the contract. An opening without every condition and a missing decision
are both refused. The Ohio request routes e1, e4 and e5; e4 is the Ohio statement.

**Falsifiers** (any one stops the line):
- Ohio's signing thesis in fewer than 8 of 9 draws, or a `company_impact` that presents the $500bn asset cost as the guarantee amount;
- a signing thesis on fresh-47 or fresh-50 (small);
- one on fresh-9 (agreed);
- one on fresh-22's $25bn or fresh-7's supplier commitments (undertaken);
- one on dev-1's announced programme;
- a duplicate of fresh-8's completion thesis (already asked);
- any other opened signing thesis that a blind reader judges wrong. The reader brief states the yardstick (the company's revenue,
  profit, cash or credit risk), and a verdict on another yardstick is unjudged;
- a contract refusal rate above 1 in 10.

**Known limits:**
- It reaches only statements c8 kept and linked to an obligation thesis. The miss read in §53 found no material obligation outside it
  in two runs.
- The stored NVDA set holds no material unsigned obligation from another industry.
- Cost in production is one more small call on about 18% of articles.

## Revision after `cq-codex.md` and `cr-codex.md`

- **Statements about one deal:** "Return one new signing thesis per obligation whose statements open, and list every opening statement
  about that obligation under it." `already_asked_by` now names only a shown thesis, never one proposed in this call.
- **Signing status:** a fourth value, "unclear" (the item does not say which). It never opens.
- **Forecasts:** "a forecast or a market figure" is removed from not_an_obligation. That list is now only §3's own words: not taken in
  its own name; its own borrowing or leases; a completed or unsized investment.
- **Date:** "The date the item supports; when it gives none, a check date within 18 months of the item, with how it was set" (§3).
- **company_impact:** the added "whom it backs, for what and for how long" procedure is removed.
- **separate_bet:** "the obligation merits a separate investment judgment" (D388's words).
- **opens:** true exactly when all conditions hold, false otherwise. Code enforces it both ways.
- **Code contract:**
  - opens equal to the conditions;
  - no empty or repeated new thesis;
  - the raw answer is kept on every failure;
  - articles with no routed statement are printed as skipped.

  Whether two statements are the same obligation, and whether a cited thesis asks about that obligation, are read from the answers.
  Code cannot decide either.
- **$0 checks** (bytecode cleared): a right answer passes; opens false with all conditions met is refused; "unclear" passes the schema.
- **Counting, set before the send:**
  - a transport error is re-sent once and recorded;
  - a contract refusal counts as a miss on Ohio's 8-of-9 line and toward the 1-in-10 refusal line.

  The run prints its 10 skipped cases.
- **Not changed:** "already asks whether this obligation is signed" stays. The thesis D388 keeps is the signing question, so a
  different question about the same obligation does not ask it.
- **Second revision** (`cs-codex.md`, `ct-codex.md`):
  - **The check date is always within 18 months:** "the date the item supports when it gives one within that time, otherwise the date
    18 months out at most".
  - **A transport error is re-sent once,** and both attempts are recorded.
  - **"not_yet_signed"** now reads "when the item describes the obligation as not yet signed (for example proposed, planned, expected or
    under negotiation)". The standard says not to write 拟议/预计 as 已签. "unclear" now applies only when the item gives no indication
    either way.
  - **A fifth condition, `settleable`:** "public material (a filing, an announcement) will settle on a date whether it is signed" (§3's
    thesis test). It enters `opens`, and code enforces it.
