# c8 whole-request audit: Claude's own pass, written before the blind reader (2026-11-08)

Scope: `arms/c8-system.txt`, `c8-closing.txt`, `c8-schema.json`. References: the signed standard (§§2–5), D380–D386, Alex's rulings.

| Clause (location) | Source | Verdict |
|---|---|---|
| Role: an unfiled statement is "kept in the company's record and linked when a thesis that covers it opens" | D383 | consistent |
| §1 the four kinds; example list without the valuation example | standard §5.1; D385 | consistent (example removed in c8) |
| §1 "Take a statement when an analyst … would write it in this week's notes" | standard §5.1 | consistent |
| §2 EXISTING / NEW / UNFILED | standard filing; D383 | consistent; "UNFILED" now means kept unlinked, not dropped; the wording "unfiled" survives |
| §2 CONDITION: figures listed; results inform a revenue/earnings thesis when they bear on it; a different period is not on its own a reason | D382; Alex's margin ruling; D371 | consistent |
| §2 usefulness test: revenue, profitability, funding or credit risk, competitive position; cash-balance example | standard's materiality frame (AGENTS §8); Alex's cash ruling | consistent; the example teaches context, as agreed in `z-codex` |
| §2 "The share price, a target price and other companies' figures are never conditions" | D385; standard row 8 | consistent |
| §2 linking: every thesis it informs; period-difference rule | standard §4 filing; K6b | consistent |
| §3 the opening test and four reasons | standard §§3–4; D384; D382 for class A | consistent; class A excluded by design |
| §3 dates set by the analyst for pending regulation and unsigned obligations | standard §3 E and C | consistent |
| §3 do-not-open list | standard §4 list | consistent; "own borrowing or leases as an obligation" matches the standard's wording |
| §3 counterexamples | K6b, consistent with §4 | consistent |
| §4 writing rules (one item, one statement; summary; passages) | standard §2 | consistent |
| Closing: evidence test, not-kept rows | standard §5.3 | consistent; **row 6 changed by D385** (disclosed conflict with the frozen gold) |
| Closing: "A report and another party's denial or confirmation of it are two items …; one party's statement keeps its own planned or rumoured details" | standard glossary 陈述; standard line 436; D385 | consistent |
| Closing: theses check (four reasons, settling material, separate bet when an open thesis exists, do-not-open) | standard §4; D384 | consistent |
| Closing: condition read-back (a balance or cash flow tied to nothing is not returned) | Alex's cash ruling; D383 ("what the closing check rejects is dropped") | consistent |
| Schema: `figures` (useful figures, one statement may list several); `opens_as` enum; `settled_by` non-blank; links description | D382; D384; standard §4 who checks what | consistent |

**Open points for the blind reader to test:**
- **The word "unfiled"** is still used in the role and in §2 although unfiled items are now kept. Is it read as "dropped"?
- **Growth:** system 13,476 (K6b) → 15,068 characters; closing 7,670 → 8,534; schema +about 2,400. Reason: Alex's four decisions,
  each needing its definition. Nothing redundant is known to remain.
