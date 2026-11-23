# "Forecast unavailable" release, slice 1: built and checked at $0 (2026-11-23)

**Result: accepted by council 75g** (`codex-r75g.md`), after rounds 75 to 75f. Slice 1 is built to `RELEASE-BUILD.md`:
- revision 10 was ready per council 74j, after ten review rounds;
- revision 11 records what councils 75 to 75f required of the build.

It passes its tests, its mutants and the $0 release check on four stored stores. Nothing is committed, published or deployed. The POC
is unchanged; no POC code imports the release module.

- Code: `src/hivemind/release.py`, `scripts/release_build.py`, `tests/test_release.py`.
- Check: `release_check.py`; mutants: `release_mutants.py` (both in this folder).
- Output: `poc/data/release-check-2026-11-23g/`. The runs `release-check-2026-11-23/` to `-23f/` predate later fixes and are kept for
  the record. Their counts and bytes are the same; their seconds differ by run.
- The mutant counts below come from separate runs of `release_mutants.py`, not from `results.json`.

## 1. Council 75's findings, and what changed

Council 75 (`codex-r75.md`) reproduced the four packages' counts and both refusals of the substituted forecast. It did not accept the
slice. Its findings and the fixes:

| Finding | Fix | Proof |
|---|---|---|
| A key written after the bound could reclassify an earlier package (the key lookup ignored its `seq`) | the key counts only when visible at the bound | test 22; mutant "key read without its day" |
| Ten text fields accepted null, which revision 10 forbids | strings only | test 23; mutant "null accepted as text" |
| `check` read the data file three times: it could hash one version and certify another | one read through one folder handle; hash and parse the same bytes; the command reports that data | structural (`check_package`) |
| A path holding `%` could make SQLite open a different file from the one named | `release.store_path` refuses `%`, `?`, `#` | test 24; mutant "store-path refusal removed" |
| Test 14's marker case supplied the very line its mutant removes | the instrumentation no longer touches the line that drops the staging path | test 14; mutant caught |
| Test 13 damaged two things | the package copy keeps `e2` with no source, which is what a checker that drops missing items expects | test 13; mutant "inner join" caught |
| Tests 1, 2 and 9 lacked decisive assertions | test 25 proves the writer's own refusal; test 2 checks all five labels in `v1`'s own fields; test 9 names each refusal's reason | mutants caught |
| The mutant runner counted any non-zero exit | it stops on a failing control, and counts a catch only with a failing test and no setup or collection error | run below |
| My first result overstated the closing check, the diagnostic search and the dated check, and the script never failed | corrected below; the script now fails on any missed acceptance item or budget | this run |

**Council 75b** (`codex-r75b.md`) confirmed the fixes above and found four more gaps, now fixed:

| Finding | Fix | Proof |
|---|---|---|
| The store-path check returned the original path, which the opener resolved again | `store_path` returns the resolved path, and the opener is given that | test 24 (a symbolic link); mutant "store path returned unresolved" |
| A named pipe in a package would make `check` hang instead of refusing | files are opened without waiting (`O_NONBLOCK`), then refused by type | test 15, through the command with a 30 s bound; mutant "pipe opened blocking" |
| The check script could pass with a required example missing | the three examples are a fixed list; a missing one fails the script | this run |
| No test reordered records, and the runner credited a failure of a test's own scratch edit | test 10 reorders questions and evidence; scratch edits fail with "scratch anchor", which the runner does not count | mutant "check_origins accepting another order" |

It also asked that test 23 cover all ten text fields (now one case per field) and that test 2 check every question's own fields for
the labels (done).

**Council 75c** (`codex-r75c.md`) found no off-list field or mismatched value, and judged every code finding of 75 and 75b closed. It
found three verification gaps, now fixed:

| Finding | Fix | Proof |
|---|---|---|
| The runner read only pytest's short line, which can omit the "scratch anchor" message | each failure's full message is read from pytest's XML report | this run |
| Test 2 skipped evidence fields; test 21 did not check that the whole report is printed | test 2 allows a `v1` label only in the fixture's known genuine source text; test 21 parses the printed report | mutants "a number label written into another question's evidence", "report not printed" |
| The check script accepted an example id whose text had changed | superseded by council 75d's rule below | this run |

**Council 75d** (`codex-r75d.md`) again found no off-list field or mismatched value. Its three findings had one mechanism:
- test 2 took its "genuine" text from the export under test;
- test 21 accepted a partial report;
- the acceptance script's "$390 billion" also matches the system's own forecast, and a stale-hash refusal satisfied a check meant
  for another reason.

**One structural rule now holds** (AGENTS §1): every acceptance assertion compares against fixed expected values written down before
the run, never values taken from the output under test, and every refusal check matches its exact reason:
- test 2 allows a label only in the fixture's own two constant texts;
- tests 11 and 21 require the report's exact key set and fixed values;
- the script compares each example's full summary and quote with the stored text written into it (old-1, 2026-11-23), and each
  refusal with its exact message;
- mutant "report missing a field" proves the key-set check.

**Council 75e** (`codex-r75e.md`) found no path for a forbidden or mismatched value. It showed the rule was applied only partly, and it
is now applied to the release tests' value and refusal assertions and to every check in the script:
- the tests compare with literal key sets and the literal marker text, never the module's own constants;
- test 2 checks each label occurrence by its location (question, evidence, field);
- tests 11 and 21 check the report's full contents: counts `{number 5, event 1, Yes/No 1}`, 5 evidence, 6 sources, 101 fields
  compared, 3,313 bytes, and the two unresolved questions with their reason;
- every refusal of a value in the tests is matched by its exact message (some occupied-path tests check only the error type or exit
  status; see the optional items below);
- the script pins each store's day, classes and evidence count, the marker text, `v8`'s 1,284 pieces of evidence, the identity of the
  forged value (the system's `j1580` forecast), both leak answers ("Yes"), the control (`v3`, "Yes") and the closing reason.

**Council 75f** (`codex-r75f.md`) found two certification gaps and judged everything else optional under AGENTS §5. Both are fixed:
- **Each dated package's own day is checked.** Before, a September package passed as the August one because both answers were "Yes".
  Now the package and its manifest must carry the requested day, with the evidence count of that day: 2026-08-25, 3,239 pieces; 
  2026-08-28, 5,673 pieces.
- **The delivered format and allow-list identifiers** (`hivemind-release/1`, `release-allow-list/1`) are compared with literal strings
  in the script, for the data and manifest of every store, and in test 1. Before, they were compared only with the module's own
  constants.

**Left as optional (council 75f, AGENTS §5),** none of which lets a wrong package through:
- a test helper takes its expected day from the export;
- some occupied-path tests check only the error type or the exit status;
- test 2's scan of other questions' evidence covers summaries and quotes; the origin check compares every field.

**No regression.**
- The release tests: 36 pass. The full suite passes: 425 tests, the frozen-ruler guards included.
- Mutants: 31 of 32 are caught by failing tests, each judged from its full failure message (a failure of the test's own scratch edit
  does not count), with no setup errors.
- **The 32nd, the canonical-day check removed, is equivalent on this repository's Python 3.10.10,** whose `date.fromisoformat` already
  refuses `20260825`. Under Python 3.13, on a temporary copy of `old-1` with one later completed day:
  - the real code refuses `20260825`;
  - the mutant exports `v8` with 1,284 pieces of evidence through 2026-09-20 into a package dated 2026-08-25, where the right package
    holds 621.

## 2. The $0 release check (design §7)

| Store | Bound | Number / event / Yes-No | Evidence | Fields compared | Data bytes (library) | Seconds (library) |
|---|---|---|---|---|---|---|
| old-1 | 2026-09-20 | 19 / 28 / 0 | 8,251 | 91,055 | 5,788,634 (14,478,536) | 8.05 (6.36) |
| old-2 | 2026-09-20 | 17 / 26 / 0 | 6,306 | 69,636 | 4,427,609 (11,893,701) | 6.19 (4.91) |
| old-3 | 2026-09-20 | 18 / 31 / 0 | 6,659 | 73,559 | 4,685,247 (12,375,915) | 6.54 (5.25) |
| served | 2026-08-28 | 13 / 55 / 0 | 6,461 | 71,524 | 4,612,321 (12,145,774) | 4.29 (3.36) |

- **Every package passed its origin check:** every field compared with its stored source at the bound.
- **No number question is unresolved** in these stores.
- **Budgets met:**
  - the bytes are 0.37–0.40 of the existing library's;
  - the seconds are 1.25–1.28 times the library's, against a budget of 3 times and 120 s.
- **How the evidence is counted.** The count includes each piece once per question that holds it. Every piece has exactly one source
  row (`old-1`: 5,390 rows for 5,390 pieces).
- **The script exits non-zero when any check it names fails:** each store's day, classes and evidence; the budgets; each example; each
  exact refusal; the forged value's identity; `v8`; each leak; the control; the closing. This run ended "every acceptance item and
  budget met".

**The decisive acceptance case** (council 74, `old-1`):
- **Kept, each equal to the store and to its full text written into the script before the run:**
  - Morningstar's $361 billion (`e2295`, under `v8`);
  - the genuine "Bullish confirmation" quote (`e1865`, under `v4`, `v5`, `v8`);
  - the analysts' "$390 billion" (`e3597`, under `v4`, `v5`).
- **The system's own forecast** (`j1580` implied outcome, "About $390 billion: …"):
  - substituted into `e2295`'s summary, it is refused with exactly "question v8.evidence e2295.one_line: differs from the store";
  - added to the manifest, it is refused with exactly "the manifest: keys off the allow-list ['note'], missing []".

**The other checks:**
- **`old-1/v8`:** class `number`, marked "Forecast unavailable". Its 1,284 pieces of evidence are the same ids as `service.evidence` at
  the bound.
- **The known Yes/No leaks at their own days.**
  - `old-3/v36` at 2026-08-25 (judgement 799) and `old-1/v10` at 2026-08-28 (judgement 865) are the latest judgements there, and
    each package carries its own day (3,239 and 5,673 pieces of evidence).
  - Both keep "Yes".
  - The full explanation and reason texts are absent.
  - So are the judgements' own phrases: "around $1 trillion", "rung 4", "at rung" and "capex at rung" occur in no field.
- **Control:** event `old-1/v3` keeps "Yes" and its evidence, equal to the store.
- **Closing,** on a copy of `old-1` with a closing switch for `v8`, "due 2026-09-20, frozen on 2026-09-20 at rung 2 Bullish":
  - `bundle.view_bundle` exposes it;
  - the package shows `open: false`;
  - the reason appears nowhere.
  - The word "Bullish" does occur inside six `v8` fields: five source titles and the genuine `e1865` quote. That is source wording,
    which the design keeps.

## 3. The diagnostic search, every hit read

The search covered every decoded string of each package, ids, classes, the marker and the manifest included. For each question it
took every stored string the package must not hold:
- rung labels of number questions;
- the rung conditions of every question;
- judgement reasons, explanations, implied outcomes and references, where the store has those columns (the served ledger lacks the
  last two);
- every switch reason, "created" included.

| Store | Stored strings judged | Package strings | Hits |
|---|---|---|---|
| old-1 | 6,670 | 91,012 | 1,378: "created" 987, "Bullish" 391 |
| old-2 | 6,677 | 69,597 | 771: "created" 516, "Bullish" 255 |
| old-3 | 7,045 | 73,514 | 1,613: "created" 1,176, labels 437 ("Bullish", "High", "Low", "Bearish", "Middle") |
| served | 2,149 | 71,460 | 1,794: "created" 1,632, "Bullish" 162 |

- **No condition, reason, explanation, implied outcome, reference or closing reason is found anywhere.**
- **The label hits are 257 package fields holding 32 distinct texts, all read.** Every one is source wording:
  - headlines: "Jensen Huang's Bullish Call …", "Stock Traded Lower", "Earnings Call Highlights", "Lows Not Seen Since 2019",
    "Sky-High P/E", "That Bearish Bet";
  - the memory term "High Bandwidth Memory";
  - the analyst quote "Bullish confirmation would require …".
- **The "created" hits fall in 33 distinct texts, all containing the ordinary word.** It is every question's creation reason and
  carries no forecast.

## 4. Not shown, and still open

- **The reader's screen** (slice 2, D756's screen check) is not built. The release page must read only this package, with no live
  fetch and no idea submission, and needs a browser check of the `old-1/v8` screen.
- **The idea path in the release:** deferred (council 74); its acceptance is pending.
- **The recorded disagreement on evidence summaries** (`RELEASE-BUILD.md` §8) stands.
- **`store.open_read_only` puts a path into a SQLite URI unescaped.** That is shared POC code; the release refuses such paths
  rather than changing it.
