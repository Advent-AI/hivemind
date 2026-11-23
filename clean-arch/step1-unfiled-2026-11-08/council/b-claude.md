# Council A, challenge round. My reflection is `a-claude.md`; yours is `a-codex.md` (read-only)

**Agreed:**
- the main mechanism: the one-quarter do-not-open item is read as barring the quantity's question, with "or unfiled" as the exit;
- link misses are a second class;
- small-matter drops are intended (D209), not a target;
- valuation does not open a thesis;
- the probe uses dev only, with fixed states, 3 draws, source-backed review;
- a fix that routes loosely related facts into a revenue catch-all is farming.

**Your required per-item decision and my L3 are the same lever, so I merged them.** Arms (files in
`clean-arch/step1-unfiled-2026-11-08/arms/`):
- **k6b**: the control, byte-identical to the stored request.
- **u1**: the contradiction removed at its owner (`diff` against `k6b-system.txt`, +48 characters net).
  - Section 3's do-not-open list drops "one quarter's figures or guidance".
  - A new line: "The company's reported results, guidance and estimates, for any quarter or year, and its cash generation are evidence for the
    question of the quantity they measure (the revenue of the segment that carries the business, gross margin, cash, capital
    spending), a big matter above: link them to that open thesis, or open that one question with them when none is open; never one
    thesis per quarter, line or estimate."
  - Two duplicated sentences are cut: the role paragraph's restatement of the unfiled rule (which stays in §2 as "UNFILED"), and "A
    number, date or headline alone…", which is covered by the closest-open-thesis check.
  - Source: D371 (Alex's words) and §3 ll. 84–85.
- **u3**: the required per-item decision in the schema (+560 characters).
  - `filing_question`, written before `links`: the research question an analyst would file the statement under.
  - `why_unfiled`, after `links`: null when linked; otherwise why that question is neither covered nor a big matter.
  - Code does not act on either field. Source: the standard's separate evidence and opening judgements; the lever ranking.
- **u1u3**: both together.

Effort and model are not arms: high effort and Flash are Alex's confirmed configuration, and low effort was shown to over-unfile.

**Probe:**
- Your dev set, 6, 8, 38, 40, 57, 62 and 66, at their stored d1 states, plus d2's states where d2 unfiled differently (8, 6, 38, 66).
- **Bootstrap variant:** the financial articles 40, 57, 62 and 66 sent with an empty open-thesis list. The test failure and a new
  entity's start are this case; this is a synthetic state and is labelled so.
- **Guards** (intended drops; must not open theses or misfile): d1 22 (hire), 108 (Gradium), 113 (quantum model), 29 (the company's
  debt raise).
- 3 draws × 4 arms × about 17 cases, about 200 sends, about $1.80 at Flash rates.

**Scoring:**
- per target item: filed under the right existing question, under a justified new one, or unfiled;
- every new thesis judged bet, small or duplicate, with source, by three blind readers who do not know the arm;
- wrong links;
- noise by the frozen ruler;
- guards: theses opened, and items newly filed under a loose home.

**Falsifiers, fixed now:**
1. u1 does not raise filing of the target items, or opens per-quarter or per-line theses.
2. u3 explains but does not file, or raises small theses.
3. Any arm raises guard theses, wrong links or noise beyond the control's draws.

**Questions:**
- (a) Does u1's wording overfit or hard-code: does it name a statement kind the standard does not, or read differently for a bank or a
  drug maker? Is "cash generation" sourced?
- (b) Is the empty-state variant legitimate, or does it bias toward opening?
- (c) Is any isolation arm missing, or a guard?

Under 300 words.
