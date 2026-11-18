# Challenge 20: the due-day audit and census (`reflection-6/due-day/AUDIT.md`, `due-day/census.txt`)

**Class (a): the request's line 23** ("for an obligation already taken on, its next annual filing") **is applied to completion
events.**
- **Where:** sol and astra date the fortnight Hugging Face completion at 2027-02-28 (9 of 9) and label it `stated`. The topic states
  24 March 2028; luna keeps the stated date (4 of 4).
- **The two decisions:**
  - D403, Alex: an event's day is the stated date or the period end, and "the model chooses no other day";
  - D210, Alex's go: the next-annual-filing rule is for "a financing_amount question on the amount the obligation reaches".
- **How the request reads:** line 23 is wider than D210 and contradicts D403 on events.
- **Counted:** 13 answers on 2 of 26 topics.
- **The other binding-obligation event** (the guarantee, 3 April 2028) is dated as stated by every model, 13 of 13.

**Class (b): events dated at period end before their settling report.** I classify these as D403's design, not a ladder defect.
They go on Alex's page as a consequence, with both readings (judge on the day, or wait for the report). The judging step owns that
choice.

**Proposed: one new request version, one clause.** Line 23 becomes "for an obligation already taken on asked as an amount, its next
annual filing".
1. **Prompt audit** of the whole changed request (lines 20 to 23, the schema's due_day descriptions, the closing check).
2. **$0 checks:**
   - no stored answer the current code accepts is refused by the code (the code does not test this clause; confirm by replay);
   - the change touches only binding-obligation events.
3. **Probe, about $0.75, astra only (the leading candidate):**
   - **the two Hugging Face topics, which must keep the topic's dates;**
   - **controls:**
     - the guarantee event (must keep 3 April 2028);
     - the three obligation-amount topics (fortnight c1/clean-2, week c1/clean-1 and -8), which must keep the next annual filing;
   - 3 draws each, 18 sends.
   - **Moves:** both Hugging Face topics take the topic's date in at least 5 of 6, every control keeps its day, and no new decline
     appears.
   - **Closes:** otherwise.

**Asked:**
1. Is (a)'s mechanism and source sound?
2. Is (b) correctly left to the judging step and Alex?
3. Send the plan?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
