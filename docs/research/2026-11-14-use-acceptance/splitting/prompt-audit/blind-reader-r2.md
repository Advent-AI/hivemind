1. **The yearly instruction conflicts with the request’s own rule for omitted parts.**  
   > “The value for 2027 is asked as its own question, so the two-year decline case does not apply here, and that value is not a part this question leaves out; list every other part as before, including a condition or comparison that names 2027.”

   **Verdict: contradicts** the closing check and the `not_judged` schema description quoted in findings 2 and 3. They say to list *every* omitted part, while this sentence excludes the other year’s value. The design explicitly calls for that exclusion when both yearly questions are written, and for code to add the refused year when only one is written. But the model receives conflicting instructions.

   The final clause helps protect a comparison or condition that mentions 2027. It does **not clearly say to separate an omitted value from another limit contained in the same part**. For example, if a topic asks for “2027 revenue from stores open for at least two years,” the model could treat the whole phrase as the other year’s value and omit the store-age limit. A mixed part can therefore be lost.

2. **The closing check repeats the conflicting instruction.**  
   > “Read the question back: does it ask one thing, the one the topic's outcome names, and is every other part of the topic's wording listed in not_judged?”

   **Verdict: contradicts** the yearly instruction above. It is consistent with D397 for the ordinary one-question path, but it does not acknowledge the design’s exception for the other year.

3. **The schema gives the same conflicting instruction.**  
   > “Every other part of the topic's wording that the question leaves out (a second figure or event, a condition, a comparison); empty only when the question leaves nothing of the wording out.”

   **Verdict: contradicts** the yearly instruction. The other year is a second figure left out of an individual yearly question, yet the yearly instruction says not to list it when it is asked separately. The design’s treatment of a refused year is performed by code, so the unconditional schema text does not describe the yearly model response clearly.

4. **The main instruction also makes the yearly exception unclear.**  
   > “List every other part of the topic's wording that the question leaves out, a second figure or event, a condition or a comparison, in not_judged, each with one sentence on why it is not the one tracked.”

   **Verdict: contradicts** the yearly instruction for the other year’s figure. It is consistent with D397 outside the specified split. The yearly instruction appears later, but the request never explicitly says it overrides this sentence and the schema for that one part.

5. **The split case itself can be read as competing with the main-part rule.**  
   > “A topic's wording may ask about more than one thing.”

   **Verdict: consistent** with D397 and D38.

   > “Judge the one the topic's outcome names as what is tracked.”

   **Verdict: contradicts** the new case when the outcome names both years independently: it tells the model to judge the tracked thing, while the new case tells it to decline and name both years. The new case says it is “rather than the first,” but does not explicitly resolve this competition with the main-part instruction.

   > “Never fold two things into one ladder: ‘Will the regulator approve the drug for a second use, and how many patients will take it in the first year?’ is judged on the approval when that is what its outcome names, and the patient count is listed; ‘How much will the carrier's fuel bill be next year, and will its pilots strike?’ is judged on the fuel bill when that is what its outcome names, and the strike is listed.”

   **Verdict: consistent** with D38 and D397 for the examples given. It does not itself distinguish two independent years of the same quantity from two different things.

6. **The new decline case expresses the intended boundary, but its example is not enough to remove ambiguity for mixed wording.**  
   > “Return no_ladder with the reason, and ladder null, in eight cases: the topic has no main figure or event, naming none, or naming several with none of them the main one; nothing in the topic can be checked on a date, which for an event means that neither the topic nor the item gives a date and the topic names no period, unless it is a pending regulatory decision, for which use the company's current fiscal year-end; the figure is a company's figure for a quarter or a half-year, which is evidence to a yearly question; the figure covers a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, and neither the topic nor the item gives the day it is published; the figure is for a year that has already ended on the item's day; the figure is for a year beyond next year, unless the topic's opens_as is binding_obligation; or the question belongs to another company or to a matter that no theme in the request's themes covers, in which case name that company or matter in the reason; or the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison, which is this case rather than the first, since each year has its main figure: name the two years in periods, and each year is then asked as its own question.”

   **Verdict: consistent** for the new case with the design’s two-independent-open-years boundary and its named departure from D397. D38 supports one question per year. The “no main” part is consistent with D397; the ended-year and beyond-next-year parts are supported by D38’s stated year boundary, subject to D38’s own recorded qualification. The other inherited refusal cases are **not established by the specified sources**.

   > “A retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on 2027.”

   **Verdict: consistent** with the design’s boundary. It clearly illustrates independent values versus a base-year comparison. It does not show a case in which the other year is both a comparison and part of an additional condition, so that boundary remains less clear for mixed wording.

   > “Do not rewrite a figure for a year beyond next year as an event to keep it; a numeric completion target may define the state of an event that is itself the topic.”

   **Verdict: has no source** among the specified sources for this rewrite rule. D38 supports the open-year limit, but does not state this instruction.

7. **The schema names the cases and years consistently with the design, but inherits the same unresolved competition.**  
   > “The two years, for one_quantity_two_periods only; null for every other case.”

   **Verdict: consistent** with the design’s typed case and two-year output.

   > “Why no judged question is written, as one case of this closed set, or null: no_main: the topic has no main figure or event (none, or several with none the main one); not_checkable_on_a_date: nothing in it can be checked on a date (for an event: no date given and no period named, unless it is a pending regulatory decision, which is due at the company's current fiscal year-end); quarter_or_half_year: a company's figure for a quarter or a half-year; not_one_year_period: a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, with no publication day in the topic or the item; year_ended: a figure for a year that has already ended on the item's day; beyond_next_year: a figure for a year beyond next year (unless the topic's opens_as is binding_obligation); another_company_or_uncovered_matter: the question belongs to another company or to a matter no listed theme covers (name it); one_quantity_two_periods: the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (this case, not no_main): name the two years in periods, written as a figure's year is written (2026, or FY2027); each year is then asked as its own question.”

   **Verdict: consistent** for `one_quantity_two_periods` and its distinction from `no_main` with the design. As in finding 6, the specified sources do not establish every inherited refusal case. The sentence does not settle a possible overlap with another refusal, such as an uncovered matter.

   > “Exactly one of no_ladder and ladder is null (checked by code).”

   **Verdict: consistent** with the design’s choice between a refusal and a written question.

   > “Why this case applies, naming the words that decide it.”

   **Verdict: consistent** with the design’s requirement to record the refusal reason; the specified sources do not prescribe this exact explanation format.

8. **The yearly instruction selects the requested year, but the broader request still asks for the whole outcome.**  
   > “Write the question for 2026 only: this topic is split by year.”

   **Verdict: consistent** with the design’s yearly re-ask. It conflicts in practice with the unqualified instruction to judge what the outcome names when that outcome names both years; the request should make the yearly instruction’s precedence explicit.

   > “A figure is answered in figure: its unit (USD, percent, count, GW, MW, TWD or multiple; other when it is none of these, the question then naming the unit), the one year it covers (written FY2027 for a company's figure, which uses its fiscal year; written 2026 for a theme's figure, which uses the calendar year) and exactly five ranges of that one figure.”

   **Verdict: consistent** with D38’s one figure and one year per question. The precise unit list is not established by the specified sources.

   > “The one year the figure covers: FY2027 for a company's figure (its fiscal year); 2026 for a theme's figure (a calendar year).”

   **Verdict: consistent** with D38’s stated fiscal/calendar distinction, subject to D38’s recorded qualification.

   > “Code refuses the other form.”

   **Verdict: has no source** in the specified decisions or design boundary; it is a claim about implementation enforcement.

   > “For a figure, use its publication date, which falls after the end of the period the figure covers: stated when the topic or the item gives it, expected_publication when you set the day you expect it to be published.”

   **Verdict: consistent** with D38’s stated publication-date rule, subject to D38’s recorded qualification.

   > “Company figures use the company's fiscal year: ‘this year’ contains the item's publication day, and ‘next year’ follows it; convert fiscal years using the fiscal-year note.”

   **Verdict: has no source** for this exact conversion procedure in the specified sources. D38 expressly marks the details of how years are counted as a proposal.

   > “Other figures use calendar years.”

   **Verdict: consistent** with D38’s stated distinction, subject to its recorded qualification.

9. **Other refusal and omitted-detail instructions apply outside the split.**  
   > “A question about another company's own figure, or about a matter no listed theme covers, has no object here: return no_ladder.”

   **Verdict: has no source** among the specified sources for this refusal boundary.

   > “Nothing else: a question with another object is returned as no_ladder.”

   **Verdict: has no source** among the specified sources for that refusal.

   > “A difference inside an outcome, such as an approval with conditions against one without, is not an outcome of its own; when the topic's wording names it, list it in not_judged.”

   **Verdict: consistent** with D397’s treatment of omitted wording and D436’s treatment of a second side as context rather than another question.

10. **The remaining question-shape instructions support one question per answer.**  
    > “Write the one question the topic is judged on: what it asks, its answer ladder and its due day.”

    **Verdict: consistent** with D38 for each yearly answer; read as a rule for the whole topic, it is narrower than the design’s split exception.

    > “A judged question concerns one figure for a named period or one event.”

    **Verdict: consistent** with D38.

    > “For a figure, the question names the period it covers or the day it is measured at, and the material that settles it.”

    **Verdict: consistent** with D38.

    > “The one judged question: one figure for a named period, or one event.”

    **Verdict: consistent** with D38 for each answer; the singular wording does not explain that the split topic can have two yearly answers.

    > “For a figure it names the period covered or the day measured at, and the material that settles it.”

    **Verdict: consistent** with D38.

11. **The examples in the instructions are general; the supplied article and topic necessarily name the covered company and its numbers.**  
    > “A retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on 2027.”

    **Verdict: consistent** as a general example: it names no covered company or product. The request payload does name NVDA, its products, other companies and their amounts because it supplies the actual topic and article. Those are source material, not a company-specific instruction. The fiscal-year note also names NVDA and its actual years; it is company-specific input used to interpret the date, rather than a general rule.

**Summary:** The split boundary is stated and illustrated, but the yearly omission rule conflicts with three existing instructions and does not fully protect mixed parts containing another year and an additional limit.