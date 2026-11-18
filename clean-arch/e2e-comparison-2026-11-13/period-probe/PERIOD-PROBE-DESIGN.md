# The period-rule probe: c17 against c8 (D470; council round 12's conditions), 2026-11-13

**What it can decide:** whether making clean Step 1's shared-quantity period "one calendar year, this year or next" removes the misread the
model's accounts showed (the period read as a horizon; calendar 2027 called "beyond next year" from a July 2026 item), on the three cases that
showed it, without harming the memory question's 2027-against-2026 shape (D441) or the capex years. It is a case-specific diagnostic on seen
material; a pass leads only to a council decision on a test on fresh articles.

**Candidate:** `clean-arch/step1-unfiled-2026-11-08/arms/c17-system.txt` (closing and schema = c8's): §3 shared_quantity "for this or next
calendar year" → "for one calendar year, this year or next (a figure over a rolling twelve months, or an average or total over several years, is
not this reason's period, while a calendar year compared with the year before it is; whether a statement is kept is judged as evidence)" (version 2,
after the blind audit `audit-c17-blind.md` found "a span that is not one calendar year" could exclude a 2027-against-2026 comparison):
15,828 → 16,061 characters (+233; reason: a sourced clarification
of a misread line, §3 D "自然年的今年或明年"; nothing cut, cuts being levers). The added words say only that a comparison with the year before keeps its year as the period; unlike
c16's clause, they do not say a two-year statement is one thesis (that clause moved the capex year).

**Cases** (`cases-period.json`, stored states; `probe_identity.py` unchanged, three sends a case and arm; 96 jobs, about $1.4 estimated,
ceiling $2 under its tested ledger):
- targets: c1 step 76 and c3 step 112 (China's domestic-supplier share survey), c1 step 127 (memory prices; the same article opened the H100
  rental thesis);
- guards: D441's memory states d1–d3 step 56, listed three times (nine sends a state and arm); the capex article d1–d3 step 42; the federal
  spending article c1 step 241 (its two-figure thesis is not targeted: an unwanted change there is a regression).

**Lines, per case and frozen before the send (every answer read by Claude):**
- *Valid sends:* every target, capex and federal case needs at least two valid sends in each arm, or that case is inconclusive (listed).
- *Target, per case:* a new shared-quantity thesis on the article's matter with a period of one calendar year. A case is **fixed** when this holds
  in at least two of c17's valid sends and at most one of c8's; a send that opens no such thesis is never counted as fixed: it is listed with its
  reason and whether the article's statements on the matter were kept. **Met:** at least two of the three cases fixed and none made worse;
  **not met:** at most one fixed; **inconclusive:** fewer than two cases with enough valid sends.
- *Memory guard (54 sends):* valid sends at least 7 of 9 per state and arm, or the guard is inconclusive; counts are compared as shares of valid
  sends. Any shape: exercised when c8 has at least 5 memory-price theses of 27; regression when c17's are fewer by 5 or more. The 2027 or
  2027-against-2026 shape (the comparison D441 protects): exercised only when c8 has at least 4 such theses of 27, otherwise reported as not
  measured; regression when c17's are fewer by 3 or more. Each send's memory question, period and shape is listed.
- *Capex guard (18 sends):* the years opened per send listed; regression: c17 opens fewer capex years than c8 by 2 or more over its nine sends.
- *Federal guard:* the thesis each send opens listed; regression: c17's opening differs in kind from c8's in two or more sends (a dropped thesis, a
  merged one, another period).
- Any regression stops the line; inconclusive guards are reported as such, never as passed.

**Before the send:** a blind audit of version 1 (`audit-c17-blind.md`, one material point, answered) and of version 2 (`audit-c17v2-blind.md`);
the council's conditions of rounds 12 and 13 written into these lines.
