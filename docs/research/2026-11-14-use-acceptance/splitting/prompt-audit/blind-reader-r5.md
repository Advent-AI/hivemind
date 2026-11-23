1. **Contradicts another sentence of the request:** “or the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (a comparison between the two does not make either a base when the value of each is asked), which is this case rather than the first, since each year has its main figure, and rather than judging only one of the two years as the one the outcome names: name the two years in periods, and each year is then asked as its own question.”

   The unchanged instruction says: “Judge the one the topic's outcome names as what is tracked.” The new sentence explicitly overrides that instruction for two independently asked years, but it does not say it overrides the unchanged closing check: “Read the question back: does it ask one thing, the one the topic's outcome names, and is every other part of the topic's wording listed in not_judged?” On the **initial** request, the model can follow the new decline rule, but the closing check still asks it to check a question and list omitted parts. The yearly line resolves the conflict for re-asks; it is absent from the initial request. The splitting itself is consistent with the design boundary and D38.

2. **Consistent, with a procedural dependency:** “The value for 2027 is asked as its own question, so the two-year decline case does not apply here and that value alone is not listed in not_judged.”

   Design §0b item 2 says neither written question lists the other year when both are written. If the other year is refused, code adds that year and the refusal reason afterwards. Thus the sentence is consistent with the complete procedure, although the model cannot yet know whether the other question will actually be written.

3. **Consistent:** “List every other part as before; where a part joins the 2027 value with another limit, a condition or a comparison, list that limit, condition or comparison.”

   This addresses the mixed-part risk: the other year’s value alone is omitted, but a condition or comparison attached to it must still be listed. The instruction is clear in principle; whether the model preserves such a part requires reading its answer.

4. **Consistent:** “A retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on 2027.”

   Together with the preceding rule—especially “a comparison between the two does not make either a base when the value of each is asked”—this distinguishes asking for both values from asking for one value against a base. It matches the design’s boundary. The examples use a generic retailer and do not name a covered company, its products, or its numbers.

5. **Consistent:** “Write the question for 2026 only: this topic is split by year, and where the instructions above differ, this line prevails.”

   This gives each re-ask one year and expressly resolves conflicts with earlier instructions, as required by the design’s two separate yearly attempts.

6. **Consistent:** “The two years, for one_quantity_two_periods only; null for every other case.”

   This matches the design’s typed case and two-year handoff. The schema’s changed decline-case description repeats the same boundary: “one_quantity_two_periods: the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (a comparison between the two does not make either a base when the value of each is asked; this case, not no_main): name the two years in periods, written as a figure's year is written (2026, or FY2027); each year is then asked as its own question.” **Verdict: consistent.**

7. **Consistent:** “Why this case applies, naming the words that decide it.”

   This asks the model to explain which topic wording supports its selected decline case. It does not add a new reason to decline.

8. **Consistent:** “Return no_ladder with the reason, and ladder null, in eight cases.” The change from seven to eight reflects the additional typed case; the other seven cases are outside this audit.

**Summary:** The yearly instruction preserves mixed conditions and makes the base-year boundary understandable; the remaining request-level conflict is the unchanged closing check on the initial two-year decline.