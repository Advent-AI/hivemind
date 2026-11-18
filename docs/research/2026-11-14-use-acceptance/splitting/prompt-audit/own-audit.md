# The split version's prompt audit: my own table, written before reading the blind reader

The request: the frozen system text (9,545 characters, now 9,950), the user message (payload, then the frozen closing check), and the
strict schema (6,116 characters, now 7,193). A yearly re-ask adds one line of 161 characters after the closing check. Sources: D38
(one view a year), D397 (one judged question per topic; "an open defect until splitting is built"), D436 (a second side is one
question), DESIGN.md v4 §2 (the boundary table) and §0b item 2 (who decides "not judged").

| # | Sentence (where) | Source | Verdict |
|---|---|---|---|
| 1 | "A topic's wording may ask about more than one thing. Judge the one the topic's outcome names … List every other part … in not_judged" (system, line 5) | D397, D436 | **Consistent, but it pulls against the new case for a T topic.** Its outcome names both years, so "the one the outcome names" has no single answer. The frozen step resolved that by declining with "no main figure" in every send. The new case is the more specific rule for exactly this case (D38), so the two do not contradict. But the model must read line 5's "one thing" as yielding to the eighth case. Measured by T's count. |
| 2 | "Return no_ladder with the reason … in seven cases:" (system, line 6, frozen) | the frozen list | **Contradiction, fixed.** The schema offered eight cases while the system named seven. The system line now says "eight cases" and adds the case, with one example on each side of the boundary, from another industry (a retailer's store openings, and its revenue against the year before). |
| 3 | The new case in the system text and in the schema's closed set ("one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison") | D38; DESIGN §2 rows 1 and 3 | **Consistent.** It is the boundary the design draws. The base-or-comparison clause is the misuse guard. Before the example it was abstract; the example makes the boundary concrete. |
| 4 | The seven old cases in the schema's closed set | the frozen description, verbatim (a test checks each phrase) | **Consistent.** |
| 5 | "Exactly one of no_ladder and ladder is null (checked by code)" (schema) | the frozen description | **Consistent.** |
| 6 | The closing check: "does it ask one thing, the one the topic's outcome names, and is every other part of the topic's wording listed in not_judged?" | frozen | **In a yearly re-ask, it pulls against the yearly line.** The other year is part of the wording. The yearly line comes after the closing check and names the exception, so it is a scoped exception, not a contradiction. Whether the model obeys is measured by the reading (L, BY, LQ). |
| 7 | The schema's `not_judged`: "Every other part of the topic's wording that the question leaves out … empty only when the question leaves nothing of the wording out" | frozen | **The same scoped exception as row 6.** In a yearly re-ask a T topic's list can be empty while the other year is left out. That is the design's §0b item 2 (D618). |
| 8 | The yearly line: "Write the question for {year} only; {other} is asked as its own question, so do not list it as a part this question leaves out, and list every other part as before." | D38; §0b item 2 (D618) | **Consistent.** The added "list every other part as before" answers round 161's mixed-qualification caveat. Whether a mixed part keeps its other limit is measured by the reading (LQ). |
| 9 | The decline cases for an ended year and a year beyond next year | frozen | **Consistent with the new case.** The new case needs both years open; code refuses another pair. |
| 10 | Industry wording | AGENTS §6 | **Consistent.** The example names a retailer, no covered company, product or number. The years 2026 and 2027 illustrate the rule and are not taken from a test article. |

**Growth:** the system text grows by 405 characters, the schema by 1,077, and a yearly re-ask by 161. The reasons:
- the closed set replaces the prose decline list in the schema (AGENTS §6: a classification as a closed set);
- the eighth case is written where the seven are (row 2);
- one example on each side of its boundary replaces an abstract clause.

**Not measured by this audit, measured by the probe:**
- whether line 5 and the closing check (rows 1 and 6) keep the model from naming the case on a T topic (T's count);
- whether the base-or-comparison clause holds on the four C1 topics with an open base year (the control count and BY).
