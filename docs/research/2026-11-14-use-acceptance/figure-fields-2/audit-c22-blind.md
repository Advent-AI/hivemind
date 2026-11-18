**The rewording fixes several c21 ambiguities, but it leaves two material conflicts:** an unattributed forecast is told to use `estimate` even though `kind` defines an estimate as having a named or consensus source, and a forecast whose source is stated elsewhere in the article can be read as source-less.

For example, an article may say “management guided revenue to $100 billion” and later say “the guide implies 20% growth.” The second figure has a stated source in context, but “the item states in its own voice without saying whose it is” does not clearly say whether that context counts.

The parsed comparison confirms that c21 added the two required figure fields to c8, and **c22 changes only their descriptions** relative to c21. Both `cmp` checks succeeded: c22’s system text and closing check are byte-for-byte identical to c8’s. This is a reading audit; I did not send requests or measure model behavior. The wording is in [c22-schema.json](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c22-schema.json:192).

### 1. Sentence-by-sentence reading

**`party`**

1. **“The source of this figure, which may differ from the statement’s original_party.” — Clear.** It distinguishes the figure’s source from the statement-level field. The exact name format remains unspecified, but that does not prevent identifying the source.

2. **“For the company’s own reported result: the company.” — Clear for an identified company result.** A reported result needs no named spokesperson. The system defines “the company” as `current_entity`. It remains possible for the model to mistake an analyst’s estimate *about* the company for the company’s own result, but the wording itself separates a reported result from a forecast.

3. **“For a forecast or outlook: the company only where the item says the company, its management or a named executive gave it …; the named person or firm, or ‘consensus’ …; the item’s author or outlet for its own calculation or estimate.” — Mostly clear, with a context ambiguity.** Management’s or the company’s stated forecast takes the company; an executive’s name is added when the figure is given as that person’s statement. An analyst’s estimate takes the named analyst or firm, or `consensus` when the article gives it as the market’s or analysts’ expectation. An identifiable author’s own calculation takes the author or outlet.

   The unresolved point is **how attribution elsewhere in the article carries to a later figure**. “Where the item says … gave it” permits context, but does not say how clearly a later reference must connect to that earlier attribution. Also, “add the executive’s name” does not specify a string format; that is a formatting ambiguity, not an attribution conflict.

4. **“A forecast the item states in its own voice without saying whose it is … has no stated source: party is null, and its kind is estimate, not guidance.” — Ambiguous in context and conflicts with `kind`.** For an article-voice forecast with no source stated anywhere, the intended `party` is clearly `null`. But “states in its own voice” can also describe a paraphrase of management guidance attributed elsewhere; it does not say that the *whole article* lacks an attribution.

   The `kind` instruction conflicts with its own description: **“estimate: a named party’s or consensus forecast.”** An unattributed forecast is neither necessarily named nor consensus. The instruction also rules out `guidance` for it, while `kind` defines guidance as **“the company’s own outlook”** without saying that the company must be explicitly identified as its source. The result is an inconsistent classification instruction, even though the new sentence’s intended outcome is apparent.

5. **“Figures of one statement may share a source or have different ones; the statement stays one item.” — Clear.** It agrees with the figure-array description: **“A statement with several useful figures stays one item and lists them all.”**

**`fiscal_period`**

1. **“The same period in fixed form, only when the item itself writes the year of this figure’s period …” — Mostly clear, but incomplete about the quarter and fiscal/calendar marker.** It requires the relevant year to be written and gives examples of fiscal and calendar forms. For a quarter, it does not explicitly say that the quarter number must also be stated or explicitly connected to the figure. Nor does it say whether a bare year is enough to choose `FY` or `CY`. The requirement that it be the *same period* weighs against guessing, but does not fully spell out those boundaries.

2. **“The year may be written anywhere in the item for the same period …” — Clear in the illustrated case; ambiguous at the boundary.** If the article says “the second quarter of fiscal 2027” and later refers to **that quarter**, `FY2027-Q2` is supported. If a year appears elsewhere but its connection to the figure’s quarter is only inferred, “for the same period” leaves the strength of that connection open.

3. **“null when no period is given, when the item never writes that year … or when the period is not one year or one quarter …” — Clear for the listed cases.** A quarter or “the full year” with no written year takes `null`. Another fiscal year that would require calculating the figure’s year also takes `null`. A range or deadline takes `null`. The original stated wording can still be preserved in the separate `period` field.

4. **“Never work the year out from the publication date or from knowledge outside the item.” — Clear as to the year.** Unlike c21, it no longer expressly prohibits converting a calendar period into a fiscal period. “The same period” suggests preserving the original basis, but the prohibition now applies specifically to working out the **year**, leaving a possible conversion of quarter or FY/CY basis less explicit.

The requested examples therefore read as follows:

| Article wording | What c22 says |
|---|---|
| A quarter, with its fiscal year written elsewhere | Use the fixed form **if the article connects that written year to this same quarter**. A mere nearby year is not enough by the stated rule; borderline connections remain ambiguous. |
| A quarter, with only another fiscal year written | `null` if the quarter’s year must be worked out from that other year. |
| “The full year” | `null` if its year is not written; otherwise a fixed year only when that year is for this period. |
| “Next fiscal year” | `null` if its year is not written; use the fixed form if the article explicitly identifies that same year. |
| A calendar-year figure | `CY` form when the article states the year and establishes it as a calendar period. A bare year’s FY/CY interpretation is not explicit. |

### 2. Possible effects on the answer

These are **wording risks, not observed model failures**:

- **A stated source could be left empty.** “The item states in its own voice without saying whose it is” could be applied to a sentence that omits an attribution even though another part of the article explicitly connects the figure to management or an analyst.
- **A figure could be omitted.** The `party` field is required, but c22 removed c21’s general fallback, **“null when the item does not say whose figure it is.”** It supplies `null` explicitly only for unattributed forecasts. A reported or other figure with an unclear source has no equally explicit fallback, although the schema allows `null`. Omitting it would conflict with the instruction to list all useful figures.
- **Splitting is not instructed.** The new wording expressly says the statement stays one item, consistent with the existing array description and closing check. I see no changed words that direct a split; model variation remains possible.
- **Keeping, opening, and linking are not directly changed by either field description.** The classification conflict could nonetheless influence whether the model treats an unattributed forecast as a qualifying figure: section 2 describes figures as a reported result, guidance, or **“a named party’s or consensus estimate.”** Similarly, an incorrectly inferred or emptied period could influence a link, despite the instruction that **“a different period is not on its own a reason to leave them unlinked.”** There is no new instruction to open a question.

### 3. Smallest wording changes

These are proposed wording only; no file was changed.

- In `party`, qualify the unattributed-forecast sentence: **“A forecast for which the item does not state a source, including elsewhere in the item, has no stated source …”** This preserves `null` for a genuinely unattributed forecast while allowing an explicit cross-reference to an earlier source.
- Restore the general fallback: **“`null` when the item does not state the figure’s source.”**
- In `kind`, make its estimate definition agree with the existing new instruction: **“estimate: a forecast other than the company’s stated outlook, including a named party’s or consensus forecast and an unattributed forecast.”** This resolves the contradiction without adding a keep, open, or link rule.
- In `fiscal_period`, add: **“For a quarter, the item must also state its quarter number and identify it as part of that year; use the fiscal or calendar basis the item states.”** Restore c21’s **“do not convert a calendar period into a fiscal one.”** This makes the fixed form’s supporting information explicit without calculating a missing year.