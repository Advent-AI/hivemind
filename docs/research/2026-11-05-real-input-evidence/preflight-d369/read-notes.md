# Stored-answer preflight, 2026-11-05 UTC

Scope: replay stored v116 draw 1 extraction answers against current frozen extraction checks and the original current items database; no model calls. This is a contract diagnostic, not a comparison of report-context arms or acceptance of v117. `historical-preflight.txt` contains the full output. The shell wrapper failed after the script printed `preflight done` because zsh reserves the variable name `status`, so the script's exit code was not captured on that invocation. A repeat using a Python subprocess captured exit 0 and the same counts in `historical-preflight-verified.txt`. It judged 243/243 extract rows, with 699 evidence + 11 candidates produced; 7 evidence quote checks refused, 4 duplicates merged, 1 empty candidate ladder refused. Matching judged 161 records, 3 skipped because their matching request was absent from this archive. Six archived judge answers had previously been marked refused; they are not six new extraction refusals. The structural check showed no missing enum values.

Read every one of the seven refused quotes against its stored article. These are raw model quotations, not the article text:

| Input | Quote difference visible in source | Initial interpretation |
|---|---|---|
| gnews:56085a9d3e88c464bcaed67b | The quote inserts `(vision-language-action (VLA))`; the nearest source sentence says `VLA` without this insertion. The expanded term occurs elsewhere on the page. | A stitched explanatory expansion, not a verbatim sentence. Check whether the quote-repair contract is meant to permit it before calling this a false refusal. |
| gnews:7620a6ac8ec29bf19328a734 | Model says `He said that Trainium2 ...`; source explicitly names Amazon CEO Andy Jassy in the sentence. | The model substitutes a pronoun for the named speaker. Same broad assertion, but not a verbatim quote. |
| gnews:7b39859113d4e2b8ebd8aa86 | Model writes `HON FAI`; source says `HON HAI`. | Changed named entity; refusal is warranted. |
| gnews:dadd84590540a466aea01b3c | Model starts `The company has started`; source starts `It has started`. | Attribution/wording substitution; same broad numerical claim, not verbatim. |
| gnews:24268bfaab6ef1d7876b188c | Model skips a middle clause about a third entity and AMD chips, while joining the beginning and end. | Non-contiguous quote. Read the complete sentence and the existing quote-repair rules before deciding if acceptable. |
| gnews:01a49ffd41f6abe24538da65 | Model writes `Part of that hold`; source says `The scale of Nvidia’s hold`. | Changed introductory phrase; the numeric claim is in the source but the quotation is not verbatim. |
| gnews:ca7564a0dc63b215f5d49402 | Model says `The FBI's RFI`; source sentence says `The RFI`. | An added owner from context, not the exact sentence. |

These are historical cases with a seeded library and do not measure new real-article gold. The system must preserve material evidence and a faithful source quotation; resemblance alone does not establish which refusals are wrong. Do not relax the quote check on the basis of this sample. A later paid send also needs a preflight on the actual experimental request construction: the existing `scripts/preflight.py` expects the article to be followed immediately by the normal closing block and will not accept the new report-background block without an experiment-specific check. The archive used here is not the new study's archive.

## Superseded request preflight

`experiment-preflight.json` reported six fake arms on the earlier draft. It is retained as a historical engineering check only: those requests used the original corpus ID and stale content metadata with a different archived body. They are invalid study inputs and do not accept the new variant design. Do not use these six results as the preflight for a real send. Build and independently check unique variant IDs, a local source database, mapped references and new request bytes, then run a fresh preflight.


## 2026-11-05: archive variant recheck and independent review

The builder now checks the capture, URL and HTML hash against the archive index and parses the publisher time from each saved HTML file. A fresh build reproduced all three variant IDs. The six A/B requests passed fake-transport preflight again, and one source-grounded fake answer traversed the real writer and reader. These are contract checks, not model quality results. The source URL in the reader points to the archive capture, but inherited title/publisher/classification have not all been independently verified, and the reader does not expose a separate capture-time or unverified-metadata badge. The reviewer also found that the A/B sender is not implemented/reviewed, and that a real article quote with a report-contaminated summary is not caught by the quote-only test. Read every actual answer and stored record against article and report when an approved experiment runs.

The independent review is retained at `independent-variant-implementation-review.md`. No real A/B requests were sent. The gold remains unsigned and several old/new boundaries remain unresolved. Do not score or call this an efficacy result. The test currently models an empty library, not the live historical 68-question library.
