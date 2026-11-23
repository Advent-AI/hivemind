# "Forecast unavailable" release: build design for slice 1 (the exporter and the checked package)

**Note (slice 2).** The package format is now `hivemind-release/2`: it adds the reader's page `index.html` and `page_sha256`
(`RELEASE-PAGE.md`). Everything below still holds for the data and the checks.

**Status: revision 11. Built** (`src/hivemind/release.py`, `scripts/release_build.py`, `tests/test_release.py`; result in
`RELEASE-CHECK-RESULT.md`). Revision 10 was ready per council 74j; revision 11 records the changes council 75 required of the build.

**Revision 11 (council 75, `codex-r75.md`).** Each change is in the code and has a test and a mutant:
- **A view key counts only once it is visible at the bound** (its `seq`). A key written later never reclassifies an earlier package
  (test 22).
- **Text fields are strings, never null,** as §1 already specified (test 23). The four stores hold no null evidence or item fields.
- **`check_package` reads each file once,** through one handle on the folder (`O_DIRECTORY | O_NOFOLLOW`, then `O_NOFOLLOW` per file and
  `fstat`). It hashes and parses the same bytes and returns `(counts, data, bytes)`, so the command reports what was checked.
- **A store path whose resolved form holds `%`, `?` or `#` is refused** (`release.store_path`), because `store.open_read_only` puts
  the path into a SQLite `file:` URI unescaped (test 24). The opener itself is shared POC code and is not changed here.
- **The writer's own refusal** is proved by a scratch-copy pair (test 25).
- **Both commands print the whole report** before publishing it. Durations use `time.monotonic`. Refusals name the evidence id.
- **Council 75b** (`codex-r75b.md`):
  - `store_path` returns the resolved path, which the opener is given, so a link is not resolved twice (test 24);
  - package files are opened without waiting (`O_NONBLOCK`), so a named pipe is refused by type instead of blocking `check` (test 15);
  - reordered questions and evidence are tested (test 10).
- **Councils 75c and 75d, verification only.** The mutant runner judges each catch from the full failure message in pytest's XML
  report. One structural rule holds for every acceptance assertion: compare against fixed expected values written down before the run,
  never values taken from the output under test, and match each refusal's exact reason. Council 75e: applied to every assertion in
  `tests/test_release.py` and every check in `release_check.py`. Release work was opened by the council under D439 (D758). The behaviour is
fixed by D726, D756 and `FORECAST-UNAVAILABLE-DESIGN.md` (revision 4). This page holds the AGENTS §2 tables for the first slice.

**Revision 2 answers `codex-r74.md`** (see `claude-r74.md`):
- the pass condition is an origin check of every field against its stored source, not a string sweep;
- a missing source item is refused;
- the package is checked before it is moved into place;
- the manifest is a closed set;
- the bound is validated as a date;
- narrow reads;
- size and speed budgets;
- tests that separate every branch;
- `object`, `kind` and groups dropped;
- no idea submission.

The evidence summary stays as extraction stored it (§8, disputed in `claude-r74.md`).

**Revision 3 answers `codex-r74b.md`.**
- The checker derives everything it compares from the store, never from the package: the date, each question's class, the records and their counts.
- A missing source item refuses `check` too.
- The files must be two regular, non-symlink files, with no duplicate JSON member names.
- The staging folder has one owner.
- The builder's refusal is tested through the builder.
- The diagnostics read only the columns a store has.

**Revision 4 answers `codex-r74c.md`.**
- One date rule for build and `check`.
- Questions are ordered by `created_seq, rowid`.
- (Superseded in revision 5.) The build claimed its output folder before staging.
- Cleanup sits where the staging path is known.
- A report failure after publication has its own outcome.
- The builder's refusal is proved through the real command on a scratch copy.
- Tests 9, 13, 14 and 15 are sharpened.

**Revision 5 answers `codex-r74d.md` with one structural rule** (AGENTS §1: the publication mechanism drew findings in 74b, 74c and
74d). Staging is private, and the only public step is one atomic move that refuses any existing destination. There is no public
claim, so nothing public is created early or cleaned up. Staging is removed in a `finally` covering its whole life, so any error,
database errors included, leaves nothing at `--out`.

**Revision 6 answers `codex-r74e.md`.**
- The build's cleanup responsibility ends the moment `publish` succeeds: the staging path is cleared and the `finally` removes nothing
  after that, so a folder later created at the freed staging name is never touched.
- The late refusal at `publish`, and the end of cleanup after it, are proved through the real command on scratch copies with a
  pause.

**Revision 7 answers `codex-r74f.md`.**
- An explicit day is parsed first and used everywhere in its canonical `YYYY-MM-DD` form. Python reads `20260825` as the same day,
  but the stores compare days as text.
- Neither command writes a report over an input database.

**Revision 8 answers `codex-r74g.md` with one rule for every public write** (report writing drew findings in 74f and 74g). Nothing the
build or `check` writes ever replaces an existing path:
- the package is published by `publish` (`RENAME_EXCL`);
- the report is published by writing a private temporary file, then `os.link` to the report name, which fails with `EEXIST` when
  anything exists there.

Verified on this Mac: `os.link` refuses an existing file, a case-variant name of it (`ITEMS.SQLITE` for `items.sqlite`), and a
symbolic link, leaving each untouched. An input database always exists, so no report can replace one. The path comparison of
revision 7 is subsumed and dropped.

**Revision 9 answers `codex-r74h.md`.**
- A report is published the moment its link succeeds. A later failure to remove the temporary file is reported as published, naming
  the leftover file.
- `check`'s exit statuses are explicit, and the end-to-end tests assert them.

**Revision 10 answers `codex-r74i.md`:** `check` follows the build's rule. Any failure to publish the report before the link succeeds
(the name occupied, or the temporary file not created or written, such as `EACCES`) is exit 2 after the printed pass.

## 0. Scope

- **Slice 1 (this page), $0:**
  - the exporter `release_export` and its self-check;
  - the package writer, the package check and the origin check;
  - the release builder, which calls the exporter directly;
  - tests and mutants;
  - the $0 release check on stored stores.
- **Slice 2, next.** The release page reads only the package: no live service, no `/library` fetch, no translated JSON, no composite
  trials, no idea submission control or route. It gets a browser check of the `old-1/v8` screen, which completes D756's screen check.
- **No idea submission in the release** (council 74). The idea path (`idea.py`) reads the ledger at every step and calls a paid model
  per idea. The design's §5 idea acceptance (an idea card backed only by `v8`, and its composed request) is carried forward as pending
  for the first idea-enabled slice.
- **Not in scope:**
  - the POC, its API, MCP and page (unchanged);
  - colleagues' page;
  - frozen pieces, extraction included;
  - any model call;
  - commit, publish, deploy.

## 1. What is built

`src/hivemind/release.py` is the one owner, beside `service.py`.

- **Constants:**
  - `FORMAT = 'hivemind-release/1'`;
  - `ALLOW_LIST = 'release-allow-list/1'`;
  - `FORECAST_UNAVAILABLE = 'Forecast unavailable'`;
  - `PACKAGE_FILES = {'manifest.json', 'release-data.json'}`.
- **`ALLOWED`:** the closed key set per record type.

  | Record | Keys |
  |---|---|
  | envelope | `format`, `allow_list`, `as_of`, `questions` |
  | number question | `id`, `question`, `open`, `class` (= `number`), `forecast` (= the marker), `evidence` |
  | event or Yes/No question | `id`, `question`, `open`, `class` (`event` or `yes_no`), `answers` (the two stored rung labels, in position order), `answer` (the stored label of the latest judgement's rung on or before the bound, or null), `evidence` |
  | evidence in force at the bound | `id`, `one_line`, `quote`, `tier`, `speaker`, `original_who`, `original_day`, `sources` |
  | source recorded on or before the bound | `title`, `publisher`, `day`, `uri` |
  | manifest | `format`, `allow_list`, `as_of`, `data_sha256` |

- **`question_class(views_db, view_id, labels)`** (design §3):
  - `event` when the view key's measure is in `identity.EVENT_MEASURES`. The key is read as `select measure from view_keys`, and
    only when the table exists;
  - `yes_no` when there are exactly two labels which, through `vocabulary.canonical('label', …)`, are `Yes` and `No` in either order;
  - `number` otherwise: a view with no key, or one whose bands cannot be resolved.
- **`release_export(views_db, items_db, as_of=None)`:**
  - pins both connections (`bundle.read_snapshot`);
  - takes an explicit day only in canonical form: `date.fromisoformat(day).isoformat()` must equal the text given, otherwise
    `ReleaseRefused` (so `20260825` is refused, not read as `2026-08-25`). It then resolves the bound with `service.resolve_bound`,
    refuses a store with no default day, and uses that canonical text in every query;
  - exports every view that exists at the bound (`service.view_exists`), closed ones included, in `created_seq, rowid` order;
  - builds each record field by field from the table above, with column-limited SQL:
    - `select view_id, question, created_seq from views order by created_seq, rowid`;
    - `select position, label from rungs`;
    - `select rung from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1`;
    - `service.is_open_as_of`, which reads only `open` and `after_seq`;
  - takes evidence in force from `service.evidence` and its fields from that record;
  - looks up each source's `title`, `publisher` and `source_uri` in the items database by `input_id`. A visible source whose item is
    missing raises `ReleaseRefused` (there is no fallback to the id);
  - calls `check_export` on its own result before returning (AGENTS §3: the writer refuses).
- **`check_export(data)`:** the closed-set check.
  - Every dict at every level has exactly its record type's keys.
  - Value checks:
    - `format` and `allow_list` equal the constants, and `as_of` is a canonical `YYYY-MM-DD` day (`date.fromisoformat(as_of).isoformat() == as_of`);
    - `class` is in its set;
    - a number record's `forecast` is the marker;
    - `answers` is two strings, and `answer` is one of them or null;
    - `open` is a bool and every text field is a string.
  - It returns the counts it judged: questions per class, evidence, sources.
- **`check_origins(views_db, items_db, data, expected_as_of)`:** the pass condition. It is independent of the exporter's code path.
  It derives everything it compares from the store, never from the package.
  - **The bound: one rule for both commands.** `expected_as_of` is given by the caller.
    - The builder passes the bound it resolved: `service.resolve_bound` on the requested day, or the default when none is given; an
      omitted day with no default is refused.
    - `check` passes the package's `as_of` through the same `service.resolve_bound`, which refuses a day after a store's last
      completed day. A legacy ledger with no completed days accepts any valid date in both commands alike.
    - The package's `as_of` must equal `expected_as_of`.
  - **The class** of each question is derived from the stored measure and labels (`question_class`). The permitted keys and values
    are then chosen from that class, never from the package's `class` field.
  - **Order and counts.** The questions are compared as an ordered list in `created_seq, rowid` order, as `bundle.library` orders
    them (`old-2/v2` and `v3` share sequence 8). Each question's evidence is compared in link order (`evidence_links.id`), and its
    sources in row order (`evidence_sources.id`). A duplicate question, evidence record or source therefore fails.

  It compares every field with its permitted stored source at the bound, by direct SQL:
  - the question set equals the views visible at the bound, with `question` equal to `views.question`;
  - `open` equals the latest visible switch's `open`;
  - for `event` and `yes_no`: `answers` equal the rung labels in position order, and `answer` equals the label of the latest judgement
    rung on or before the bound, or null;
  - for `number`: only the marker;
  - the evidence id set equals the links visible at the bound, minus those whose latest replacement is visible, computed in its own
    SQL. Each evidence field equals the `evidence` row's column;
  - each source list starts from every visible `evidence_sources` row, in row order, with `day` taken from
    `evidence_sources.publication_day`. Each row needs a matching `items` row for `title`, `publisher` and `source_uri`; a row with no
    item raises `ReleaseRefused` (a left join, so a missing item is never silently dropped).

  Any difference raises `ReleaseRefused`, naming the question, the field and the evidence id. It returns the number of fields
  compared.
- **`stage(out_dir)`:** creates a private staging folder with a name unique to this invocation, `tempfile.mkdtemp(dir=out_dir.parent,
  prefix='.<name>.staging-')`. Creation is exclusive, so only this invocation owns it. It returns the path.
- **`write_package(data, staged)`:** writes `release-data.json` and `manifest.json` into the staging folder. It creates nothing
  else.
- **`publish(staged, out_dir)`:** one atomic move that refuses any existing destination, empty or not:
  - on macOS, `renamex_np(staged, out_dir, RENAME_EXCL)` through `ctypes`. Verified on this Mac: onto a free path it succeeds; onto
    an existing empty or non-empty folder it fails with `EEXIST`, and both folders stay as they were;
  - on Linux, `renameat2(AT_FDCWD, staged, AT_FDCWD, out_dir, RENAME_NOREPLACE)`;
  - where neither call exists, or the filesystem lacks support (`ENOTSUP`, `EINVAL`), it raises `ReleaseRefused`.

  It never replaces, creates or removes anything at `out_dir` except by that one move.
- **`check_package(path, views_db=None, items_db=None, expected_as_of=None)`:**
  - the directory holds exactly `PACKAGE_FILES`, each a regular file and not a symbolic link (`os.lstat`), with no subdirectories;
  - both files parse as JSON with no duplicate member name at any level (an `object_pairs_hook` that refuses a repeated key);
  - the manifest has exactly its four keys, and its `format`, `allow_list` and `as_of` equal the data's;
  - its sha256 equals the data file's;
  - the data passes `check_export`, and, when the stores are given, `check_origins` with the expected bound;
  - it returns the counts.
- **`withheld_unresolved(views_db, data)`** is for the report only. It lists the number questions whose `service.ladder_bands(rungs)`
  returns `(None, reason)`, with the reason and whether the view has a key. Its output never enters the package.

`scripts/release_build.py`:
- **`build --ledger --items [--as-of] --out`:**
  1. refuse an existing `--out` or `<out>.report.json` early, as a convenience. The no-replace publication of each holds the
     guarantee;
  2. resolve the bound once: a given `--as-of` must be canonical `YYYY-MM-DD` (as above), then `service.resolve_bound`;
  3. `stage(--out)`. From here a `finally` removes this staging folder while the build still owns it;
  4. `release_export` at that bound;
  5. `write_package` into the staging folder;
  6. `check_package` on the staged folder, with the stores and the resolved bound;
  7. `publish` to `--out`. The moment it succeeds, the build drops its staging path (`staged = None`); the `finally` then removes
     nothing;
  8. `publish_report`: write the report to a private temporary file in the same folder (`tempfile.mkstemp`), then `os.link` it to
     `<out>.report.json`. The link fails with `EEXIST` if anything exists at that name. **A successful link is the moment the report
     is published.** The temporary file is then removed. If that removal fails, the command still reports the report as published,
     names the leftover temporary file, and exits 0.

  The failure outcomes:
  - **Before publication** (steps 2–7): any exception, whether `ReleaseRefused`, `OSError`, `sqlite3.Error` or another, prints the
    reason and exits 1. The `finally` removes this build's staging folder; nothing exists at `--out` from this build. A corrected
    retry at the same `--out` succeeds.
  - **After publication, before the link** (step 8 fails before the link succeeds, including `EEXIST`): the package is final and
    checked, and whatever is at the report name is untouched. Exit 2 with "package published and checked; report not written; run
    `check` to write it".

  It has no input path for prepared or translated JSON, and it takes no clock reading; the folder name is the caller's (D12, D13).
- **`check <out> --ledger --items`:** re-runs `check_package` on an existing package, with the stores, the package's canonical
  `as_of` validated against the store (above), and the regular-file and duplicate-key checks. It leaves the package in place, prints
  the report, and writes `<out>.report.json` only through `publish_report`, so it never replaces anything. Its exit statuses:
  - 0: the package passes, and the report was published;
  - 2: the package passes, and the report is not published: its name is occupied (an earlier report, or anything else, which stays
    untouched), or writing the temporary file or the link fails for any other reason, which is printed;
  - 1: the package is refused, with the reason. This is also the retry after a report write failed. Its report gives `check_seconds` and marks
  `export_seconds` as not measured.
- **The report:**
  - the store path and the bound;
  - counts per class;
  - the unresolved list;
  - the fields compared;
  - bytes;
  - `export_seconds` (build only) and `check_seconds`.

## 2. State × event (one export, read-only)

| State / event | What happens | What is written | Day used |
|---|---|---|---|
| Store's first day still in progress | `FirstDayNotCompleted`; the build stops | nothing | none |
| Store with no completed day and no judgement, `--as-of` omitted | refused: "no default day; supply --as-of" | nothing | none |
| `--as-of` not a valid date (`2026-08-99`) | refused by `date.fromisoformat` | nothing | none |
| `--as-of` valid but not canonical (`20260825`) | refused: the stores compare days as text, so a non-canonical day would read rows from later days | nothing | none |
| The report name is occupied, by a file, a case-variant name of an input, or a symbolic link (build or `check`) | the build refuses at the start; a name occupied later makes `publish_report` fail with `EEXIST` and exit 2; `check` exits 2 after printing; whatever is there is untouched | the package only (build) | — |
| `--as-of` after the last completed day | `BoundNotCompleted`; the build stops | nothing | requested day |
| `--as-of` valid, before the first visible question | empty `questions`; the report says 0 | package | bound |
| `--as-of` omitted | last completed day (a legacy ledger: its last judgement day) | package | resolved bound |
| View created after the bound | not exported | — | bound |
| View closed on or before the bound | `open: false`, with no reason and no day | — | bound |
| Closed, then reopened, before the bound | the last visible switch wins | — | bound |
| Event or Yes/No not yet judged at the bound | `answer: null` | — | bound |
| Evidence replaced on or before the bound | excluded; the replacement is in force | — | bound |
| Evidence replaced after the bound | kept | — | bound |
| Source recorded after the bound | excluded | — | bound |
| Visible source with no row in the items database | `ReleaseRefused`, naming the evidence and input id | nothing final | bound |
| Store written by a live run | not supported. The builder is given a snapshot (AGENTS §9), and both connections are pinned | — | — |
| `--out` exists, empty or not, at the start | refused early; `publish` would also refuse | nothing | — |
| `check_export`, `check_package` or `check_origins` refuses | this build's staging folder is removed, exit non-zero | nothing final | — |
| A write, check or move fails, or a database error (`sqlite3.Error`, such as an items database with no `items` table) | exit 1; the `finally` removes this build's staging; a corrected retry at the same `--out` succeeds | nothing | — |
| A folder, empty or not, appears at `--out` after staging | `publish` refuses with `EEXIST`; that folder is untouched; staging removed; exit 1 | nothing of this build | — |
| The filesystem has no atomic no-replace move | `publish` refuses; staging removed; exit 1 | nothing | — |
| Crash while staging | a uniquely named staging folder is left as debris. Nothing is at `--out`, and no later build is blocked | staging only | — |
| Crash after the rename, before the report | the package is final and checked; `check` rewrites the report | package | — |
| The report write fails after publication | exit 2: the package is final and checked; `check` regenerates the report | package | — |
| Two builds aimed at one `--out` | each stages privately; the first `publish` wins; the second's `publish` refuses with `EEXIST`, and its `finally` removes only its own staging | the winner's package | — |
| Package `as_of` later than the store's last completed day (`check`) | refused by `resolve_bound` | nothing | package `as_of` |
| A legacy ledger with no completed days, explicit day | the build and `check` both accept any valid date (one rule) | package | requested day |
| A package file is a symbolic link, or a JSON member name repeats | `check_package` refuses | nothing | — |
| The package's `class` disagrees with the store's (a Yes/No answer replaced by the marker) | `check_origins` refuses: class is derived from the store | nothing final | bound |
| Store or configuration changed between builds | each package records its bound and data sha256; the report names the store path | — | — |
| Legacy ledger: no `view_keys` table, `是`/`否` labels | no key, so no event; the labels canonicalise to Yes/No | — | — |

## 3. Value × reader

Readers of the package:
- `check_package` and `check_origins`;
- the release page (slice 2);
- the tests.

The report's reader is the person building. No POC code imports `release`.

| Value | Permitted source at the bound | Checked by |
|---|---|---|
| `id`, `question` | `views.view_id`, `views.question` | `check_origins` |
| `open` | the latest visible `view_switches.open` | `check_origins` |
| `class` | `view_keys.measure`, `rungs.label` | `check_origins` derives it from the store; tests and mutants check the identity rule |
| `answers`, `answer` | `rungs.label` by position; the latest `judgements.rung` on or before the bound | `check_origins` |
| `forecast` | the constant marker | `check_export` |
| evidence fields | the `evidence` row; visible `evidence_links` minus visible replacements | `check_origins` |
| source fields | every visible `evidence_sources` row (`publication_day` as `day`); its `items` row's `title`, `publisher`, `source_uri`, required | `check_origins` (left join; a missing item refuses) |
| manifest | the data's `format`, `allow_list`, `as_of`; the data sha256 | `check_package` |
| report (outside the package) | `ladder_bands` per number question; counts | read by the builder's user |

**Never read by `release_export`:**
- `rungs.condition`, `lo`, `hi`;
- `judgements.reasons`, `why_changed`, `implied_outcome`, `reference`, `pushes_json`, `theme_pushes_json`, `cited_*`;
- `view_switches.reason`;
- `clean_ladders`;
- `thesis_groups`;
- `dependencies`, `successions`.

## 4. New path × old checks

| Check on the old path (`bundle.library`, `view_bundle`, `service`) | New path |
|---|---|
| `resolve_bound`: unfinished first day, future bound | same call |
| `bundle.library`: no default day refused; `date.fromisoformat` | same two checks |
| A view not visible at the bound is not served | same `view_exists` |
| Sources visible at the bound; replacements applied | same `service.evidence`, verified independently by `check_origins` |
| Pinned read transaction | same `bundle.read_snapshot` |
| `item_lookup` falls back to the id for a missing item | refused instead |
| A malformed `clean_ladders` row is refused | not read |
| Corrupt judgement JSON is refused | no JSON column read |
| The UI contract rejects unknown fields | the release's own `check_export`; the page's reading of it is slice 2 |

## 5. Prior decisions

- D726: number questions show sources and "Forecast unavailable", with band, forecast text and history withheld together.
- D756: Alex's choice.
- D757: the design, revision 4.
- D758: the release is opened; §4 (a); order.
- D12/D13: no clock.
- D163: English product text.
- D690: poc-v118 stays the product.
- D261: the ruler is untouched.
- D274: the extraction prompt is frozen.

## 6. Tests (`tests/test_release.py`) and mutants

The fixtures use a real store on a temporary path (`store.create_view`, `store.insert`), with a real items database. Each test names
its row above:
1. **Closed set (§1).**
   - Every dict in a fixture export has exactly its type's keys.
   - Positive control: an export with one added key fails `check_export`.
2. **Number with `lo`/`hi`.** The record carries the marker. No rung label, condition, `reasons`, `why_changed` or `implied_outcome` of
   that view appears in any decoded package field.
3. **Branch fixtures for identity and the report:**
   - a condition-only number that resolves: `number`, and absent from `withheld_unresolved`;
   - an unresolved number with a key: `number`, and present;
   - an unresolved number without a key: `number`, and present.
4. **Yes/No with numeric bounds** (`growth_rate` key, labels Yes/No): `yes_no`, with its answer label. A `why_changed` quoting
   "$1 trillion" is absent.
5. **Event with the served ledger's `v49` labels,** "Restriction adopted" / "No restriction adopted": `event`, with its label kept. A
   `why_changed` quoting another question's band is absent.
6. **Legacy store** with no `view_keys` table and `是`/`否` labels: `yes_no`.
7. **Closing switch** whose reason names the band label: `open: false`, and the reason is absent.
8. **Replacement and source visibility** at two bounds. A visible source with a missing item is refused.
9. **Package:**
   - staged, then checked, passes;
   - a foreign file fails, and so does a subdirectory;
   - a changed data byte fails;
   - an extra manifest key with an unchanged data hash fails;
   - a manifest `as_of` differing from the data's fails;
   - an existing `--out`, empty or not, is refused, and a leftover staging folder from another build does not block a build.
10. **Origin check, each from the store:**
    - in a staged copy, the system's forecast text placed in an evidence `one_line` fails, naming the field;
    - a Yes/No record turned into a number record, keeping the closed set, fails;
    - a duplicated question, and a duplicated evidence record, each fails;
    - a package whose `as_of` is a day later than the store's last completed day fails `check`;
    - a legacy fixture with no completed days, built at an explicit day later than its last judgement, passes a later `check`.
11. **Builder end to end,** run as the user calls it (subprocess, `--as-of` omitted):
    - the build exits 0, and the package and its report exist;
    - `check` with the build's report still in place prints a passing result and exits 2;
    - after the test removes that report, `check` exits 0 and publishes a fresh one.
12. **Builder refusal, through the real command, on a scratch copy** (the AGENTS §4 mutation procedure; no fake in the suite):
    - the unchanged command succeeds on the fixture store (test 11);
    - on a scratch copy, the writer fault "one evidence `one_line` taken from the latest judgement's `why_changed`" is introduced.
      The same command exits 1 with the origin-mismatch reason, no `--out` and no staging folder left;
    - on a second scratch copy, the same writer fault plus the builder's staged check removed: the bad package reaches `--out`. That
      shows the staged check is what prevents publication.
13. **`check` with a missing item.** A finished package. Then a copy of the items database with one referenced item deleted, and a
    copy of the package with that same source removed and its manifest hash refreshed. `check` refuses, naming the missing item. (An
    inner-join mutant accepts this pair, so this case catches it.)
14. **The publication rule.**
    - Module steps: builds A and B both stage, then A publishes. B's `publish` refuses with `EEXIST`. A's package passes `check`, and
      B's staging is still there for its owner to remove.
    - Module steps: after staging, a foreign *empty* folder is put at `--out`. `publish` refuses, and the foreign folder still exists
      afterwards, empty.
    - The command, early: an existing empty `--out` gives exit 1, and the folder survives.
    - The command, late (a scratch copy with a pause before `publish`, released by the test): the test creates an empty folder at
      `--out` during the pause. The command exits 1, its staging folder is removed, and the same empty folder survives (same device
      and inode).
    - The command, after the move (a scratch copy with a pause just after `publish`): the test recreates the freed staging name as a
      folder holding a marker file. After the command exits 0, the marker is still there.
18. **Report over an input.** `--out` is chosen so that `<out>.report.json` is the items database, three ways: the same path, a
    case-variant name on this case-insensitive volume, and a symbolic link to it. `build` refuses, and `check` on an existing package
    exits 2. The items file's sha256 is unchanged.
19. **Report name taken during the build** (a scratch copy with a pause just before `publish_report`): the test writes a marker file
    at the report name. The command exits 2 and the marker is unchanged. `check` then prints a passing result, exits 2, and leaves the
    marker unchanged.
21. **`check` cannot write its report** (a scratch copy in which creating the report's temporary file raises `PermissionError`): `check`
    prints the passing result and the write error, and exits 2.
20. **Temporary file left after the link** (a scratch copy in which removing the report's temporary file raises): the build exits 0
    and says the report is published, naming the leftover temporary file. The report exists and equals the build's report.
17. **A database error through the command.** A valid ledger with an items database that has no `items` table: exit 1, the database
    error printed, nothing at `--out`, no staging folder left. A retry at the same `--out` with the correct items database succeeds.
15. **Files:**
    - a symbolic link in place of `release-data.json` fails;
    - a data file whose repeated `one_line` member has the genuine value last, with the manifest hash refreshed so every other
      check passes, fails on the repeated name.
16. **Bound validation:**
    - `2026-08-99` is refused;
    - `20260825` is refused, while `2026-08-25` builds. On a fixture with evidence on both sides of that day, the package holds only
      the earlier evidence;
    - a valid day before the first question gives an empty package.

**Mutants,** on a scratch copy with `PYTHONDONTWRITEBYTECODE=1`; each must fail a test:
- `condition` emitted on number records;
- `one_line` taken from the latest judgement's `why_changed`;
- the event test removed;
- the Yes/No test removed;
- `check_package` without the file-set check;
- manifest keys unchecked;
- `check_export` without the closed-key check;
- `check_origins` skipping evidence fields;
- `check_origins` taking the class from the package;
- `check_origins` comparing sets instead of ordered lists;
- `check_origins` with an inner join to `items`;
- `check` without validating the package's `as_of` against the store;
- the builder skipping the staged `check_package` (the scratch-copy pair in test 12);
- `publish` replaced by `os.rename` (test 14's foreign empty folder is then replaced);
- the `finally` removed (test 17 then leaves staging);
- the staging path not dropped after `publish` (test 14's marker is then removed);
- the canonical-day check removed (test 16's `20260825` then builds with later evidence);
- `publish_report` replaced by `os.replace` (tests 18 and 19 then overwrite the items file and the marker);
- the symbolic-link check removed;
- the duplicate-key check removed;
- the switch reason emitted;
- the missing-item refusal replaced by the id fallback.

## 7. The $0 release check (stored stores, read-only)

Stores: `old-1`, `old-2`, `old-3` (`comparison-2026-11-17/run/old-N/prod/views.sqlite`, items `items-comparison.sqlite`) and the
served ledger with its items database.

**Budgets,** set before the first control (AGENTS §2):
- the package's data bytes at most `bundle.library`'s JSON bytes on the same store and bound;
- export plus all checks at most three times `bundle.library`'s seconds on the same store, and at most 120 s per store.

The steps:
1. **Build each store's package at its default bound.** The build passes `check_package` with `check_origins`. Report the fields
   compared, the counts per class and the unresolved list.
2. **The decisive acceptance case** (council 74), on the `old-1` package:
   - Morningstar's `$361 billion` estimate (`e2295`) is kept, its summary and quote equal to the stored ones;
   - the genuine "Bullish confirmation" quote (`e1865`) is kept;
   - the genuine analyst "$390 billion" quote (`e3597`) is kept, as the control;
   - in a copy of the staged package, the system's `old-1` j1580 `implied_outcome` ("About $390 billion…") substituted into
     `e2295`'s summary fails `check_origins`;
   - the same text added to the manifest fails `check_package`.
3. **`old-1/v8`:** `class` is `number`, with the marker and the same evidence ids as `service.evidence` at the bound.
4. **The known event leaks at their own dates.** Export `old-3` at 2026-08-25 (`v36` j799 is the latest judgement) and `old-1` at
   2026-08-28 (`v10` j865). Each keeps its original answer label, and j799's "around $1 trillion" text and j865's band text are absent.
5. **Control:** one unchanged event question keeps its label and evidence.
6. **Closing.** On a temporary copy of `old-1`, add a closing switch for `v8` in the store's own format ("due …, frozen on … at
   rung N <label>"). First confirm that `bundle.view_bundle` exposes the reason with the band label. Then confirm the package shows
   `open: false` and not the reason.
7. **Diagnostics** (not the gate). For every question, take each string the package must not hold:
   - rung labels and conditions;
   - judgement `reasons` and `why_changed`, and `implied_outcome` and `reference` where the store has those columns (the served
     ledger has neither; the report says so);
   - switch reasons.

   Search every decoded string field of the package for each, with no floor. List every hit with its question, field, evidence id
   and the stored string it matched, and read each by hand. A genuine source quote, such as `e1865`'s "Bullish", is recorded as such.
8. **Budgets:** bytes and seconds against the budgets above.

## 8. Evidence summaries keep extraction's wording (settled by consensus, councils 78 and 78b)

**Settled (D761).** On the reader's page, each entry is labelled: "Hivemind summary" before the summary, "Source quote" before the
quote.
- "Amounts as quoted" applies to the text labelled Source quote, which reproduces the passage verbatim. The origin check makes it
  equal to the stored quote, and extraction checks the quote against the item.
- The adjacent Hivemind summary may state a dollar amount that follows directly from that passage and keeps its qualifiers: "more
  than $40 billion" for "more than double" $20 billion. An exact "$40 billion" would change the claim.
- Rewriting summaries to show the arithmetic would need a new extraction version, which only Alex opens.

The record of the disagreement before it was settled:

The release shows each evidence summary as extraction stored it; the release computes or converts nothing. A summary can make
context explicit or restate a source figure by arithmetic, attributed to its source: `old-1/e3238` gives "more than $40 billion in
FY2028" for a quote's "more than double that next year".
- **Measured:** 25.6%, 25.2% and 25.4% of evidence in force in `old-1`, `old-2` and `old-3`, and 35.0% in the served ledger, carry a
  number not in their quote. In a sample of 24, 23 are context: a year, a date, a quarter, a product name, an amount from the previous
  sentence. One restates "close to doubling" as "nearly 100%".
- **Why this is not the forecast D726 withholds.** Extraction never sees the system's forecast. Its request lists each open question
  only as id, object, due day, question and a "takes" line (`placement.py:19-61`, `extraction.py:398-400`); no rung, label or
  judged position.
- **Council 74b** (`codex-r74b.md` §2) verified that extraction sends no rung, label or judged position, and that the census
  reproduces.
- **The disagreement that remains is narrow.**
  - Codex reads revision 4's "amounts as quoted" as requiring source wording for a calculated amount attributed to a source, such
    as `e3238`'s "more than $40 billion".
  - Claude reads it as "the release computes or converts nothing".
  - Both agree: no digit filter, no change to extraction.
- **The course taken.** By AGENTS' rule for an unsettled disagreement, the cheaper, reversible course is to keep the stored summary.
  The quote is shown beside it, so the source wording is on the reader's screen. A later version can drop the field from the
  allow-list or change it.
