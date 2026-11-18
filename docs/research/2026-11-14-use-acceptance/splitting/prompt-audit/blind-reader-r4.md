1. **The rule for a topic that has both independent yearly values and a comparison between them is not fully clear. — Keeps narrower than the design boundary, or is ambiguous.**

   > “Return no_ladder with the reason, and ladder null, in eight cases: the topic has no main figure or event, naming none, or naming several with none of them the main one; nothing in the topic can be checked on a date, which for an event means that neither the topic nor the item gives a date and the topic names no period, unless it is a pending regulatory decision, for which use the company's current fiscal year-end; the figure is a company's figure for a quarter or a half-year, which is evidence to a yearly question; the figure covers a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, and neither the topic nor the item gives the day it is published; the figure is for a year that has already ended on the item's day; the figure is for a year beyond next year, unless the topic's opens_as is binding_obligation; or the question belongs to another company or to a matter that no theme in the request's themes covers, in which case name that company or matter in the reason; or the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison, which is this case rather than the first, since each year has its main figure, and rather than judging only one of the two years as the one the outcome names: name the two years in periods, and each year is then asked as its own question.”

   Design §2 distinguishes two independently asked values from a question that asks one year **against** the other. The sentence excludes a year named *only* as a comparison, but does not say what happens when both values are independently asked **and** the topic also compares them. The model could read the comparison as making one year a base even though both values are requested.

   > “A retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on 2027.”

   **Consistent.** The examples make the two simple ends of the boundary clear, but do not resolve the mixed situation above.

2. **The yearly instruction preserves a mixed part, but the model must correctly identify the extra limitation. — Consistent.**

   > “List every other part as before; where a part joins the 2027 value with another limit, a condition or a comparison, list that limit, condition or comparison.”

   This directly addresses a part that names the other year *and* something else. It does not instruct the model to discard the whole part, so the extra limitation should remain visible. The request itself cannot guarantee that the model identifies every such limitation.

3. **The yearly instruction can override the earlier requirement to list the other year. — Consistent.**

   > “Write the question for 2026 only: this topic is split by year, and where the instructions above differ, this line prevails.”

   > “The value for 2027 is asked as its own question, so the two-year decline case does not apply here and that value alone is not listed in not_judged.”

   These sentences resolve the conflict with the unchanged instruction to select the outcome’s main part and list everything left out. They also prevent the same split decline from being applied again on the yearly re-ask. Design §0b item 2 provides for code to add the other year if its question ultimately fails; the yearly sentence alone does not represent that eventual result.

4. **The typed decline and its explanation follow the design. — Consistent.**

   > “Why this case applies, naming the words that decide it.”

   > “The two years, for one_quantity_two_periods only; null for every other case.”

   > “Why no judged question is written, as one case of this closed set, or null: no_main: the topic has no main figure or event (none, or several with none the main one); not_checkable_on_a_date: nothing in it can be checked on a date (for an event: no date given and no period named, unless it is a pending regulatory decision, which is due at the company's current fiscal year-end); quarter_or_half_year: a company's figure for a quarter or a half-year; not_one_year_period: a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, with no publication day in the topic or the item; year_ended: a figure for a year that has already ended on the item's day; beyond_next_year: a figure for a year beyond next year (unless the topic's opens_as is binding_obligation); another_company_or_uncovered_matter: the question belongs to another company or to a matter no listed theme covers (name it); one_quantity_two_periods: the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (this case, not no_main): name the two years in periods, written as a figure's year is written (2026, or FY2027); each year is then asked as its own question.”

   > “Exactly one of no_ladder and ladder is null (checked by code).”

   The new case, two periods, and separate yearly questions match design §2. The first long sentence has the same mixed-comparison ambiguity described in finding 1. The other named decline cases reproduce the existing request; their underlying rules are outside this audit.

5. **The changed examples do not name a covered company or its products. — Consistent.**

   The retailer example is generic. The supplied payload names real companies and figures, but it is the article and topic being evaluated, not a new general instruction fitted to those companies.

**Summary:** The new case and yearly re-ask can be applied consistently, and the mixed-part instruction preserves extra limits; the remaining ambiguity is a topic that independently asks both yearly values while also comparing them.