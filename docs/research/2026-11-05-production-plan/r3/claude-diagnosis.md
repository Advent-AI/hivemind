# Round 3 input: Claude's $0 and cents checks on the round-2 points (confirmation run unless stated)

1. **Truncated input** (round 2 "missed", plan review 3). `extraction.MAX_TEXT_CHARS` = 400,000; 7 of 34,084 corpus items exceed it, 1 of
   the first 100 (1280, 749,299 characters, a 10-K). Production's single-call extraction truncates at the same limit, so this is a production
   contract gap that predates the split (PRD 05 requires reading the whole item).
2. **B's no-home passages that A's new question would take** (plan review 1). 6 B no-home drops in 76 items; 2 in items where A opened a
   question; 1 belongs to it (1240, Apple's 2 nm processors → TSMC FY2026 revenue); the other (1250, September stock seasonality) is noise.
   Small class, structural cause: B cannot see A's candidate of the same item (D375 snapshot). A also failed to bring that passage for its own
   question.
3. **Contained quotes** (plan review 5). 15 pairs, every one an A passage beside a B passage. The longer passage adds only connective words in
   5 (1253 "the bad news for AMD and Intel is that", 1271 "regarding inflation,", 1252, 1227, 1234) and a second statement in 10 (1254 ACIE and
   hyperscale revenue in one A passage; 1213 the 70% guide and the "more than 100% if not for supply constraints"; 1211 three margin sentences).
   Mechanism: A has no "one evidence item records one statement" rule; B (and role-v74i) have it. Not a text-containment identity rule.
4. **Ladder references** (round 2 C/A2). The 15 ladders of the confirmation run: guidance 6, part-period pace 6, prior-year reported figure 2,
   a floor ("more than double", 1) — by a keyword reading of the neutral condition, one reader.
5. **A floor read as a point** (plan review 6). Five judgements at rung 3 on references stated as floors (v80 "more than $200 billion", v83
   "more than double $20 billion", v87 "exceed $20 billion"). Each ladder puts the floor at the neutral rung's lower bound with a narrow band
   ($200–250 billion; $40–45 billion; $20–21 billion); the frozen judge stays at the reference's rung when nothing quantifies more (PRD 06,
   D260: "a consensus figure alone keeps the judgement at the reference's rung"). The mechanism is the ladder built around a floor, not the judge.
6. **B's broad-only filings** (plan review 4; responses A14). Model accounts, one each (`poc/data/b-filing-account-2026-11-05/`): 1211 quotes
   "select the narrowest applicable supplied question" and says on reflection the passage belongs under v10, not v2 — a misread, not an
   instruction conflict; 1246 says on reflection "no link", against the link rule ("an estimate for another period … is filed under it when no
   open question covers that period", which sends it to v7) — an inconsistent application of that rule; 1210 says the whole $279 billion does
   not answer the narrow memory-and-packaging question — the new question's scope was written narrower than its source figure by A.
7. **A's recall** (`r2/claude-responses.md` §D). The singular opening does not cause misses; opening is a draw per item; the same matter is
   carried by several articles, so recall is measured at the library level by day.
