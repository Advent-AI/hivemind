# Current state

As of 2026-10-22. The design lives in `docs/system-design.html` (New tab); decisions D1–D61 in `docs/DECISIONS.md`.
The work is an architecture POC: the design page, a PRD per module and DECISIONS; no product code.

## Status

- Freeze (D58–D60, 2026-10-22): every module except pull mode and the final verdict is frozen in its current text,
  after two deep reviews in rounds (the second one's last round found nothing); a change needs a new decision. What each
  PRD lists under "还没定的" stays open: the themes in the theme library, upstream supply, each category's prompt
  wording, the granularity of views, how search ranks, the labelling details, the review pool's output.
- Where the design is: the system overview and glossary in `docs/prd/00-system.md`; the views database, its rules
  and its open items in `docs/prd/06-views.md`; extraction in `docs/prd/05-extraction.md`; the input side in
  `01`–`04` and `09`. The views rebuild discussion is in `docs/views-rebuild-log.md`.
- Pull mode and the final verdict: old drafts to be redone together. Decided so far (D54, D57): pull mode runs at the
  end of the day or on a cron interval and freezes the state of views due that day; a view has one switch, open or
  closed, and a person can close or reopen it by hand. Whether the final verdict stays a step of its own is open, and
  two of Claude's proposals wait for pull mode.
- Sealed copies (D43, D50, D61): v1 `docs/archive/2026-10-16-v1/` (the earlier design) and v15
  `docs/archive/2026-10-22-v15/` (the frozen design), each with `SHA256SUMS`, never edited. The superseded copies
  are in Git: v2–v7 `94622a5`, v8 `7830a18`, v9 `267c89d`, v10 `8d617c7`, v11 `35bb392`, v12–v14
  `3da83a9`.
- After any change, Claude refreshes everything by reasoning, module by module (D22, procedure in
  `docs/prd/README.md`); `python3 docs/check.py` is only the last, mechanical step.

## Open defects

- `simulate_classification.py` resolves a ticker on the UTC date of `published_at`; the page says the New York
  publication day (D9). It does not model the SEC filing day (D34), and has no cases for the macro rules (D15) or for
  crypto, commodity and theme objects (D11). It merges a copy without looking at `supersedes`, so an update that names
  the version it replaces is merged instead of classified as a new version; it does not check fields required only
  in some cases (`has_readable_text` for text, `period` for reports and data, a text's genre); one sample is a single
  XBRL fact, which is not pushed in (D32); one branch treats a same-issuer, same-day item as a copy without comparing
  content; a 13F sample checks the related company of one split holding row, though a whole 13F is one item (D53). It
  counts a 6-K exhibit as fiscal results only when its description says "results" (one sample); it returns two text-version
  ownership filings (Form 4, SC 13G) as T13, though T13 takes the structured version; it reports the one data
  interface that returns text and a listing as "not an input" instead of splitting it (D58). It reads related objects
  from an old field name, `company_identifiers`, while the contract's field is `object_identifiers`, so its pass does
  not test the current field (read under the current name, 392 of 411 stored items lose their related objects; D60).
  The script is not changed at the POC stage.

## Next task

Research, as Alex asked: what a thesis looks like from a hedge fund's side, so that the granularity of views is
neither too big nor too small (what to combine, what to carve out; how many questions per object; a key part such as
NVDA's China revenue stays its own view; views must not all be financial-statement lines). Then pull mode and the final
verdict are designed on the new views database, as Alex takes them up. How search ranks and the labelling details are
settled when the build starts. Deferred by Alex: upstream supply; the review pool's output.
