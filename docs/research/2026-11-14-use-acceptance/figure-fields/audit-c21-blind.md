**The two new fields fit the approved shape, but their descriptions leave real ambiguity about whose name to write and when a period can be converted.** For example, an analyst’s estimate of the company’s revenue can have the analyst as the figure’s source while the company is the subject of the number. The request does not clearly distinguish those roles.

I compared the parsed JSON: c21 differs from c8 only by the two required figure fields. `cmp` confirmed that both the system text and closing check are byte-for-byte identical. D495 authorizes this test version without changing what is kept, opened or linked; c8 remains the adopted request. The earlier approved shape calls for a useful figure to carry who said it and its period. [D494 and D495](/Users/lchingen/hivemind/docs/DECISIONS-log.md:5641), [approved shape](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:472)

The findings below concern wording risks; I did not run the model, so they are not observed changes in its answers.

### 1. Each new description

**`party`**

1. **“Whose figure this one is, as the item states it: the company for its own reported result or its own guidance; the named person, firm or ‘consensus’ for an estimate; the item’s author or outlet for its own calculation or estimate.”**  
   **Ambiguous.** “Whose figure” can mean the subject of the figure or the person who produced it. For an analyst’s estimate of company revenue, those are different. The sentence intends the source, but the statement-level `original_party` says **“Party whose action, figure or claim is reported”**: a model could reasonably copy that field or regard the two fields as conflicting. They can agree for a company’s result and differ for a mixed statement; the request does not explain that relationship.

   “The company” is defined in the system text as `current_entity`, so the referent is clear, but **the string to return is not**: the model could write the literal “the company,” the entity identifier, or a company name from the article. “As the item states it” also leaves the result unclear when the company is identified by a pronoun or context. The executive-outlook example below adds uncertainty: should guidance voiced by an executive carry the company or the executive?

2. **“In a statement with several figures each takes its own (a reported result beside an executive’s outlook; the company’s figure beside the market’s estimate).”**  
   **Ambiguous.** “Each takes its own” means an individual value is needed, but does not explain whether an executive’s outlook is the executive’s or the company’s guidance, or what exact name to use for “the market.” It can also be misread as requiring different parties, even where several figures have the same source. The examples are compatible with the existing instruction that several figures stay in one item, but do not explicitly reinforce it.

3. **“null when the item does not say whose it is.”**  
   **Ambiguous, but provides a necessary fallback.** It is unclear whether a source established by context counts as the item saying whose figure it is. Read literally, it may produce `null` for an implicitly attributed company result; read broadly, it may encourage inference. It does not require dropping the figure.

**`fiscal_period`**

1. **“The same period in fixed form, only when the item establishes it: FY2027 for the company’s fiscal year 2027, FY2027-Q3 for its third fiscal quarter, CY2027 or CY2027-Q2 for a calendar year or quarter.”**  
   **Ambiguous and sometimes asks for a form the figure cannot supply.** The pattern accepts one fiscal or calendar year, optionally one quarter. It cannot express a multi-year range or a deadline such as “by 2029.” The sentence does not explicitly say to use `null` when the source gives a period that this pattern cannot represent.

   For a company whose fiscal year differs from the calendar year, the examples distinguish `FY` from `CY`, but do not say whether a date range or calendar quarter may be converted into a fiscal quarter using knowledge outside the item. “Only when the item establishes it” points against outside inference, but does not fully settle what counts as establishing it. The example “its third fiscal quarter” also omits the year needed for `FY2027-Q3`.

2. **“A relative period (‘last quarter’, ‘next fiscal year’) takes a fixed form only when the item itself names that quarter or year; null when it does not.”**  
   **Mostly clear, with a boundary ambiguity.** It gives a null fallback for relative periods, but “names” could mean an explicit label or a period identifiable from the article’s surrounding results context. An article saying “the quarter” while discussing the latest results may therefore get a fixed value if the article names that quarter, but the instruction does not settle cases where the context merely implies it.

3. **“Never work one out from the publication date.”**  
   **Clear.** It rules out using publication date to calculate a period. It does not resolve whether other article context is enough. This is distinct from `statement_date`, which is the date the original statement was made, and `evidence_period`, which is the period the statement describes.

For a figure with **no period**, the existing `period` description clearly says `null`; the new description implies but does not explicitly say that `fiscal_period` is also `null`. For a **multi-year range** or **“by 2029,”** selecting a single year would misrepresent the source; the accepted pattern cannot preserve the range or deadline, but the description should state the null outcome.

### 2. Possible effects on what is kept, opened, linked or split

Neither field explicitly changes those decisions. The existing schema says **“A statement with several useful figures stays one item and lists them all,”** and the closing check likewise keeps a repeated measure with its figures as one item. The new “each takes its own” sentence does not override that. Still, it could be misread as requiring one statement per source, particularly for a result alongside an estimate.

The main risk to figure completeness is the combination of **“Whose figure … as the item states it”** with a required field: a model might omit a figure whose source it cannot name, even though the field permits `null`. That would conflict with the instruction to list all useful figures and the closing check’s direction that a missing amount, date or scale does not by itself drop an item.

A guessed fixed period could also make a later reader or the model treat a figure as belonging to the wrong period. Section 2 explicitly says **“a different period is not on its own a reason to leave them unlinked”** and asks the model to preserve period differences. The new wording does not instruct a linking change, but a wrongly inferred period could influence one. I see no sentence in the additions that directly tells the model to open a new thesis.

### 3. Examples

The `party` examples are generic and do not name a covered company, product or number. They apply across industries, although “executive’s outlook” leaves the attribution ambiguity above.

The `fiscal_period` examples are also industry-neutral and name no company or product, but **they do contain numbers**: `FY2027`, `FY2027-Q3`, `CY2027` and `CY2027-Q2`. They therefore do not satisfy a literal “no number” requirement. They are format examples rather than company-specific financial figures.

### 4. Smallest wording changes

These changes clarify the fields without adding a keep, opening or linking rule:

- For `party`, replace “Whose figure this one is” with **“The source of this figure, which may differ from the statement’s `original_party`”**; specify **“use the company name supplied in `current_entity`”** if that input is a name, or otherwise specify the intended company-name source. State that multiple figures may have the same source, and that an executive’s company guidance uses the company if that is the intended attribution. Keep the `null` fallback.
- For `fiscal_period`, add: **“Use null when no period is given or when the period cannot be represented by one year or quarter in this format, including a range or deadline.”** State that a fixed label must be supported by the item itself, including for relative periods, and that the model must not convert between calendar and fiscal periods using outside knowledge. Retain the prohibition on deriving it from publication date.
- If examples must contain no numbers at all, describe the accepted format in words rather than using concrete year and quarter examples; the existing schema pattern already defines the permitted characters.

No files were changed.