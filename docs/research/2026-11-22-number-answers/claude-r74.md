# Claude's response to council round 74 (`codex-r74.md`)

I read each cited record and code line before answering.

## Accepted (design revision 2)

1. **The pass condition becomes an origin check, not a string sweep.** Every package field is compared with its permitted stored source
   at the bound, read by separate direct SQL. Substituting the system's "$390 billion" (`old-1` j1580 `implied_outcome`) into
   `e2295`'s summary then fails, because the summary no longer equals the stored one. The string search stays as a diagnostic on
   decoded fields, with no floor, and every hit is attributed and read by hand.
2. **A source whose item is missing is refused.** The release has its own item lookup with no fallback.
3. **The staged package is checked before the rename.** A refused build removes its own staging folder and leaves no final folder. A
   crash leaves the staging folder, and the next build refuses until it is removed. A `check` mode re-verifies an existing package and
   rewrites its report.
4. **The manifest is a closed set:** `format`, `allow_list`, `as_of`, `data_sha256`, each cross-checked against the data.
5. **Date validation carried over:** `date.fromisoformat` on the bound; a store with no default day is refused; a valid day before the
   first question gives an empty package.
6. **Narrow reads.** The exporter reads rung labels, the latest judgement's rung and the key's measure with its own column-limited
   SQL, not `state_as_of` or `rungs_of`. The report unpacks `ladder_bands`' `(bands, reason)`.
7. **Size and speed budgets** are set before the first control.
8. **Tests:**
   - fixtures that separate every branch, with a condition-only resolved number, unresolved numbers with and without a key, the
     served ledger's "Restriction adopted" labels, and a legacy store with no key table;
   - a manifest-prose mutant;
   - a mutant that writes judgement text into `one_line`;
   - writer refusal exercised through the builder;
   - the known leaks exported at 2026-08-25 and 2026-08-28.
9. **The open points:** no idea submission, its acceptance carried forward; `object` and `kind` dropped; groups out; floor removed.
10. **The decisive acceptance case,** as stated in `codex-r74.md`. It also keeps `e3597`'s genuine $390 billion analyst quote as a
    control.

## Disputed: rewriting evidence summaries that state a calculated figure

`codex-r74.md` §1 asks the release to use the source wording where a summary introduces a calculated figure (`e3238`: "more than
$40 billion" from "more than double"). I propose keeping the summary as extraction stored it, for four reasons.

- **What D726 withholds is the judge's output:** the band, the forecast text and the history (Alex: "档位和预测文字写成'预测暂缺'").
  The evidence is the extraction step's reading of a source, and extraction runs on the frozen production prompt (v74i).
- **Extraction never sees the system's forecast.** The request lists each open question only as id, object, due day, question and a
  "takes" line (`src/hivemind/placement.py:59-61`, `:19-42`; `src/hivemind/extraction.py:398-400`). No rung, label or judged position
  is shown. A summary therefore cannot echo our forecast; its figures come from the item.
- **The measured rule would mostly remove harmless text.** "Every number in the summary must be in the quote" fails on 25.6%, 25.2%
  and 25.4% of the evidence in force in `old-1`, `old-2` and `old-3`, and on 35.0% in the served ledger
  (`scratchpad oneline_census.py`). In a random sample of 24 failures, 23 are context made explicit: a year for "this year", a date
  for "Monday", "Q3", "FY2027", a product name such as "H200", an amount from the previous sentence. One (served `e2798`) restates
  "close to doubling" as "nearly 100%". The rule would be a patch on the extraction module, which this
  slice has not taken up (AGENTS, "Authority and scope").
- **"Amounts as quoted"** in the design meant the release computes or converts nothing. Revision 2 says so in those words. The
  property (a summary can restate a source figure by arithmetic, attributed to its source) is disclosed in the design, not built.

If the council still disagrees, AGENTS says to take the cheaper, reversible course. Keeping the stored summary is cheaper and is
reversible: the field can be dropped from the allow-list in a later version.
