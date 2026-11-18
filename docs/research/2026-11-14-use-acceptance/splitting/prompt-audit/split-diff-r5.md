# What the split version changes in the frozen request (revision 5)

## System text

Before: Return no_ladder with the reason, and ladder null, in seven cases:

After: Return no_ladder with the reason, and ladder null, in eight cases:

## System text

Before: covers, in which case name that company or matter in the reason. Do not rewrite

After: covers, in which case name that company or matter in the reason; or the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (a comparison between the two does not make either a base when the value of each is asked), which is this case rather than the first, since each year has its main figure, and rather than judging only one of the two years as the one the outcome names: name the two years in periods, and each year is then asked as its own question. A retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on 2027. Do not rewrite

## Schema `no_ladder`

Before:

{
 "anyOf": [
  {
   "type": "string",
   "pattern": "\\S"
  },
  {
   "type": "null"
  }
 ],
 "description": "Why no judged question is written, or null: the topic has no main figure or event (none, or several with none the main one); nothing in it can be checked on a date (for an event: no date given and no period named, unless it is a pending regulatory decision, which is due at the company's current fiscal year-end); a company's figure for a quarter or a half-year; a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, with no publication day in the topic or the item; a figure for a year that has already ended on the item's day; a figure for a year beyond next year (unless the topic's opens_as is binding_obligation); or the question belongs to another company or to a matter no listed theme covers (name it). Exactly one of no_ladder and ladder is null (checked by code)."
}

After:

{
 "anyOf": [
  {
   "type": "null"
  },
  {
   "type": "object",
   "additionalProperties": false,
   "required": [
    "case",
    "reason",
    "periods"
   ],
   "properties": {
    "case": {
     "type": "string",
     "enum": [
      "no_main",
      "not_checkable_on_a_date",
      "quarter_or_half_year",
      "not_one_year_period",
      "year_ended",
      "beyond_next_year",
      "another_company_or_uncovered_matter",
      "one_quantity_two_periods"
     ]
    },
    "reason": {
     "type": "string",
     "pattern": "\\S",
     "description": "Why this case applies, naming the words that decide it."
    },
    "periods": {
     "anyOf": [
      {
       "type": "null"
      },
      {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     ],
     "description": "The two years, for one_quantity_two_periods only; null for every other case."
    }
   }
  }
 ],
 "description": "Why no judged question is written, as one case of this closed set, or null: no_main: the topic has no main figure or event (none, or several with none the main one); not_checkable_on_a_date: nothing in it can be checked on a date (for an event: no date given and no period named, unless it is a pending regulatory decision, which is due at the company's current fiscal year-end); quarter_or_half_year: a company's figure for a quarter or a half-year; not_one_year_period: a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, with no publication day in the topic or the item; year_ended: a figure for a year that has already ended on the item's day; beyond_next_year: a figure for a year beyond next year (unless the topic's opens_as is binding_obligation); another_company_or_uncovered_matter: the question belongs to another company or to a matter no listed theme covers (name it); one_quantity_two_periods: the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as a base or a comparison (a comparison between the two does not make either a base when the value of each is asked; this case, not no_main): name the two years in periods, written as a figure's year is written (2026, or FY2027); each year is then asked as its own question. Exactly one of no_ladder and ladder is null (checked by code)."
}

## The yearly re-ask's added line

Write the question for {year} only: this topic is split by year, and where the instructions above differ, this line prevails. The value for {other} is asked as its own question, so the two-year decline case does not apply here and that value alone is not listed in not_judged. List every other part as before; where a part joins the {other} value with another limit, a condition or a comparison, list that limit, condition or comparison.
