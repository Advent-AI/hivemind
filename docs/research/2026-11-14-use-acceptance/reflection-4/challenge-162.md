# Round 162: the split probe's $0 preparation, for a send decision (`splitting/PROBE-PREP.md`, `splitting/PROMPT-AUDIT.md`)

You asked (round 161) for the fixed population, the request and reservation checks, the full prompt audit, and the blind reading and
scoring checks before any send. They are in the two files above. Briefly:

1. **The population** is 13 topics: T 2, M 1, C1 6, C2 2, C3 2. C1 is derived again by code from the census rule, and 4 of its 6
   have an open base year.
2. **The check:**
   - 13 of 13 frozen requests equal their stored first requests;
   - the split requests differ only in `no_ladder` and the system's decline list; the yearly re-asks differ only by the yearly line;
   - 7 stored ladders are accepted;
   - the synthetic split fits the schema and the checks, and three mutants are refused.
   - **Spend:** caps of $0.15 and $0.25 ($0.40), most calls 78 and 234, expected near $0.10, plus the breach guard.
3. **The prompt audit** (my own table first, then five fresh blind readers) found and changed:
   - "seven cases" in the system, while the schema had eight;
   - the yearly line's precedence over the closing check and `not_judged`;
   - mixed parts: "list that limit, condition or comparison";
   - the order against "no main figure";
   - the example's reference contradiction;
   - a clause that read as a condition;
   - "compared and both asked".

   Round 5's only finding is the unchanged closing check beside a decline. The frozen step declined both T topics under it 18 of 18
   times, so it is recorded, not answered. Growth: system +610, schema +1,192, yearly line 431 characters.
4. **The reading and scoring:**
   - two plants from stored ladders (a base year; a dropped limit);
   - `split-brief.md` (`BY`, `LQ`, how a yearly item is read) and a third-reader brief and packet;
   - `score_split.py` implementing §0b item 4 and §0c item 3, with both countings.
   - All of this is tested end to end with a fake transport through the real runners. Mutants: 33 of 33.
5. **A gap I found and closed:** my made-up yearly answers wrote `USD billion`, which the schema refuses. The fake model skipped
   `model.call`'s schema check, so a schema-fit test now covers every made-up answer.

**Asked:**

1. Can the probe be sent now: both arms, three sends each, same day, under the $0.40 caps, with about $10 left of D439's ceiling?
2. Or name what must change first.

After a send: two reader families, then third readers on disputes, then `score_split.py`, then a result round with you.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
