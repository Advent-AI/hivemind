The draft still has serious conflicts with the signed standard. The main one is that its final check asks whether a statement is new and moves a question, but never explicitly asks whether the analyst would actually write it down.

For example, a new statement could have a plausible connection to demand and fall outside every reject row, yet still be too unimportant for the analyst’s notes. The three-question check has no explicit way to reject it on that basis.

1. **The analyst’s judgment is still missing from the final test.** [Lines 4 and 41](docs/research/2026-10-31-reference-context/role-v67-draft.txt:4) ask whether a statement is “new, or still in force,” which question it moves, and whether a reject row applies. [Line 8](docs/research/2026-10-31-reference-context/role-v67-draft.txt:8) says that eight statements passing the test yield eight items. But [§5.1](docs/prd/05-extraction-standard.html:369) asks whether the analyst **would record the statement**, because it changes how likely an answer is. Naming a question and a path does not by itself answer that judgment.

   Smallest fix: explicitly ask whether the analyst would record the statement under §5.1, both in the initial procedure and in the final check. Keep the row-by-row boundaries attached to their own rows.

2. **The first question still rules out an explicitly optional retelling.** [Lines 4–5](docs/research/2026-10-31-reference-context/role-v67-draft.txt:4) say a “retold past actual figure is optional,” but require every item to pass “Is it new, or still in force?” A retold past actual can be neither. [Line 41](docs/research/2026-10-31-reference-context/role-v67-draft.txt:41) repeats that requirement. This makes the stated option hard to exercise and contradicts [§5.3](docs/prd/05-extraction-standard.html:400), where it is optional.

   The same paragraph also calls “a figure the item itself presents as already known” **“Not new”**, without excepting retold guidance or a still-effective forecast or plan. That conflicts with the preceding sentence, which correctly says those count when retold.

   Smallest fix: make the first question accommodate the standard’s retelling boundaries, including the optional past actual, and qualify the “already known” sentence so it does not override guidance and forecasts or plans still in force.

3. **The opening sentence still narrows the questions evidence can move.** [Line 1](docs/research/2026-10-31-reference-context/role-v67-draft.txt:1) asks about “a question an analyst following the company **would bet on**,” then says the question may be “too small to open.” Those instructions pull in opposite directions: a question too small to open may be precisely one the analyst would not bet on separately. [§5.1](docs/prd/05-extraction-standard.html:369) asks whether the analyst would **note the statement** because it moves an answer; it does not require every such question to be separately worth a bet.

   Smallest fix: say “a question an analyst would note” or equivalent, and retain the explicit “open, worth opening, or too small to open” distinction. The later instruction to leave `links` empty when no supplied or proposed question fits is fine.

4. **The independent-meaning test is still incomplete.** [Line 17](docs/research/2026-10-31-reference-context/role-v67-draft.txt:17) asks whether “its answer can change while the other questions’ answers stay the same.” [§4](docs/prd/05-extraction-standard.html:305) also requires that those two situations lead to a **different judgment about the business**. A separately changing answer alone does not establish that. The draft also says the outcome “changes” the business, while the standard asks whether it **can** change it.

   Smallest fix: add the different-business-judgment part and use “can change” for the impact test. The separate size boundary for a deal, product or project is now correctly stated.

The local boundaries for policy steps, product comparisons, adoption, the news behind a price move, and a named analyst’s added fact or calculation now send the statement back for judgment rather than automatically keeping it. The examples are from varied industries and do not name a covered company. The conditional valuation’s explicit “is kept” matches its row in §5.3, but the final three-question check should not override that mandatory boundary.

This is a read-only text audit. It identifies instructions that conflict or leave a material gap; it does not measure how often the model would make a particular mistake.