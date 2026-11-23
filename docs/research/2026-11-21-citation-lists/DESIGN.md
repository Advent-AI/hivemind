# Citation-only judge version: closed id lists in the answer format (design v3, D712)

**Alex's decision (D712, 2026-11-21):** "开引用格式新版本 (推荐)". The question offered: every id field of the judge's answer takes
a closed list built from the request; a $0 check on stored data that accepted answers still pass and the bad ids are excluded; any
paid test asks him again.

**Scope:** the answer format's four id fields, and the checks needed to enforce them:
- the local validator's `maxItems`;
- preflight reading each call's saved format.

**Not changed:**
- the prompt text;
- the request text;
- the rung field;
- `check_answer` and its retry;
- any retry policy;
- what evidence is shown;
- the link direction (a separate design, D711).

v2 answers council round 38 (`codex-r38.md`): the format-error path, the batch and resume cells, duplicate theme pushes, preflight,
the D358 sizes, lists from the rendered rows, an unused version name, and the T1 proof.

v3 answers round 38b (`codex-r38b.md`):
- one owner of membership: under v12, `check_answer` uses the same row-built lists;
- preflight reads the saved format of judge rows only;
- the v7/v8 path keeps calling `build_prompt`;
- a format error on the retry;
- `maxItems: 0` keeps the item types;
- T1's exact assertions;
- T2 described as evidence from archived text, with a footnote control.

## 1. Census (stored data, $0)

- **Refusals.** Every refused judge answer on the stored runs is an id-membership error: an id outside the list its field allows.
  - Population (Codex r37b and r38, reproduced by Claude's `id_typo_census.py`): 5,415 archive rows, 5,408 distinct request-answer
    pairs, 5,389 committed, 17 refused, 2 valid answers of the stopped control batch never committed. Sources: old-1, old-2, old-3,
    and the pilots' fresh rows.
  - The classes:
    - a one-character copy of a listed evidence id (e3620 → e362);
    - a garbled evidence id (`e393`);
    - a theme id in `cites_views` or in an evidence field;
    - a dependency id used as an evidence id.
- **The same class halted a run before (D358, 2026-10-28).** The sealed three-month run's Data Center request showed 698 evidence
  ids; "the model mislabels one id among dozens of pushes about every other attempt, the code refuses the answer, two refusals halt
  the day".
- **List sizes per request**, counting evidence twice (cites and push ids) plus themes, dependencies and the two 3-value push enums:
  - the five archives: max 915 (old-1 call 5652: 451 evidence ids);
  - the sealed D358 archive: 10 of 949 requests over 1,000; call 6918 has 647 evidence ids, which is 1,323 values as plain enums and
    676 if one shared evidence enum counts once.
- **Provider limits** (OpenAI structured outputs guide, read 2026-11-21):
  - "up to 1000 enum values across all enum properties";
  - above 250 values, at most 15,000 characters per string enum;
  - 120,000 characters in all;
  - `minItems`/`maxItems` and `$defs`/`$ref` are supported;
  - the guide is silent on empty enums and on how a referenced enum counts.

## 2. Mechanism

Every request's closing line already forbids the wrong ids (`judging.py` lines 180–182). The answer format accepts any string there
(`schema_for`, lines 55–75), so the model breaks the prose rule: about 0.3% of answers, 2.6% of linked readers', and every other
attempt on a 698-id request (D358).

The code already decides membership after the answer (`check_answer`). Moving the same set into the format makes a wrong id
unwritable: code owns identity (AGENTS §2). The judge still decides which evidence matters and how it pushes.

## 3. The change

- **One new version, `judging-v12`** (unused name; `judging-v9` named an earlier experiment):
  - It has judging-v7's text and request, with closed lists. Its prompt file is a byte copy pinned to v7's sha.
  - `SUPPORTED_VERSIONS` gains it. `schema_for('judging-v7')` and `schema_for('judging-v8')` keep `JUDGING_SCHEMA_SHA`.
  - Config: `poc-v121` = poc-v118 with `rejudging.prompt_version` = judging-v12.
  - No v8-based version is built. The shared list builder is proven on linked-1's saved v8 requests offline (T2).
- **The lists come from the rows that render the request**, not from parsing its text:
  - one function returns the system text, the user text and the three id lists from the same objects at the same store state:
    - evidence: the `pieces` it prints;
    - dependencies: the resolved dependencies that get an entry (a waiting dependency has no citable target);
    - themes: the themes it prints;
  - `build_prompt` keeps its signature and returns the first two;
  - for v7 and v8, `round_of_judgements` still calls `build_prompt`, so the harness hooks that wrap it keep working;
  - for v12 it calls the new function, which `build_prompt` also delegates to, so the text is rendered in one place;
  - each v12 view's schema is built from its lists, and `ask` sends it, the retry included;
  - the lists are not fooled by an id inside a multiline quote or reasons (Codex r38 counterexamples).
- **One owner of membership under v12.** `check_answer` takes the same lists for v12 and checks evidence, theme and dependency
  membership against them, not against the parsed text.
  - Why: the text parser can narrow as well as widen. A quote holding a blank line followed by "[" ends the evidence block early, so
    a real later id would be refused (Codex r38b).
  - v7 and v8 keep the text parser unchanged (frozen). That latent narrowing is recorded as a finding, not fixed there.
  - Under v12, a citation the format accepts can still take `check_answer`'s retry for a non-membership reason.
- **The format.**
  - One `$defs` string enum of the evidence ids, sorted, referenced by `cites.items` and `pushes.items.evidence_id`.
  - A plain enum of the dependency ids for `cites_views.items`.
  - A plain enum of the theme ids for `theme_pushes.items.view_id`.
  - An empty list gives its array `maxItems: 0` and keeps its item type: a string for `cites` and `cites_views`; the full object for
    `pushes` and `theme_pushes`, with its id field an open string. No empty enum is written.
  - The schema name stays `judgement`.
- **The local validator** (`model.check_schema`) gains `maxItems`, the mirror of `minItems`. No existing schema uses it (grep), so
  no current answer changes status.
- **Preflight part A**, judge rows only, checks each stored refused row against the format saved in that row's request
  (`request_json.response_format.json_schema.schema`).
  - A judge row without a saved format is reported as such, not skipped.
  - Extraction and matching rows keep their current paths. A Jev row's request has no `response_format` (Codex r38b).
- **Size.**
  - No pre-send counting rule: the provider's counting of a referenced enum is unverified, and a guessed rule could refuse a
    request the provider accepts.
  - A request the provider refuses comes back as HTTP 400, which the transport raises at once without retrying (`openai_transport`).
    It goes through `judge_day`'s generic path to `judging_failed`, and the day is resumable. A resume sends the same oversized
    request and hits the same limit; that visible stop is the behaviour until a design change.
  - No rule drops evidence to fit.

## 4. Tables

### 4.1 State × event

| State / event | What happens | What is written; which date |
|---|---|---|
| First judgement | the lists are built as for any request | as now |
| No dependency (all of poc-v121) | `cites_views` has `maxItems: 0` | — |
| No theme | `theme_pushes` has `maxItems: 0` | — |
| No evidence printed | `cites` and `pushes` have `maxItems: 0` (eligible views have evidence in force, but the printed set can be empty) | — |
| A membership error from the provider (should not occur under strict mode) | `model.check_schema` refuses it: the row is saved with `:schema:`, `SchemaError` is raised, and the error reaches `judge_day`'s generic `judging_failed` path (not `judgement_refused_twice`, and no retry) | the refused row, suffixed; the day is resumable; a resume re-samples |
| A `check_answer` refusal not about membership (rung range, a rung move without changed, an empty stance, a duplicate theme push) | the retry carries the same schema; a second refusal → `judgement_refused_twice` | as now |
| A format error on the retry | `SchemaError` → `judging_failed`; judgements of earlier views in the same level may already be committed | those judgements stay; a resume skips them |
| Several workers in a level, one fails | other workers' answers may already be saved, while the level records no judgement; on resume, committed judgements are skipped and saved answers are reused when the rebuilt request is byte-equal | as now |
| Resume after a config or input change | a different request means a new key and a fresh answer; the default parallel runner may refuse the changed config or input before judging resumes (`parallel_day._manifest`) | as now |
| A theme closes, or a dependency resolves, after the request is built | the lists are frozen in the sent format, and under v12 `check_answer` uses the same lists | — |
| The provider refuses the format (HTTP 400: size or keyword) | not retried by the transport → `judging_failed` → resumable; a resume hits the same limit | no answer row |
| A valid id that names the wrong source | not detectable by code | measured separately (§6) |

### 4.2 Value × reader

| Value | Reader | Effect |
|---|---|---|
| The per-request schema | `model.build_request`, then `request_identity` (archive key) | every v12 judge request has a new key: no stored answer is reused; any paired run needs its own replay proof |
| The schema name `judgement` | `paid_run.is_judgement_request`, `july_test` | unchanged |
| The saved format | preflight part A | read per judge row (changed, above) |
| `build_prompt` | the paid_run and july_test prompt hooks | still called for v7/v8; a v12 harness hooks the new function |
| The answer | `vocabulary.judgement_answer`, `_record` | the same shape |
| The input size | cost | about 450 characters at the median, up to about 3,700 at the five archives' max with the shared enum; priced at $0.10 per million input tokens; measured in the $0 test |

### 4.3 New path × old checks

| Old check | Under v12 |
|---|---|
| `check_answer` membership | under v12, checked against the same lists as the format, so it cannot fire on an answer that passed; v7/v8 unchanged |
| Rung range, first-judgement changed, rung move needs changed, stance non-empty, duplicate theme push | unchanged |
| Frozen tests | v7/v8 unchanged; v12's prompt sha = v7's; a pinned schema on a fixed list |
| D359 (only named versions are built) | `SUPPORTED_VERSIONS` gains `judging-v12` only |
| Launchers | poc-v121 is a product config like poc-v118 |

### 4.4 Prior decisions

- D354 and D712: the frozen judge, now opened by Alex.
- D359: the code builds only named versions.
- D694: a new name for a request change.
- D198: the closed set is what the request showed.
- D358: the evidence-bloat halts, the same class.
- D711: the census and the recommendation.
- The pre-v74i extraction admission schema constrained `folds_into` to the shown ids. It was removed with the frozen prompt (commit
  248ef1b4); no decision rejected it.

## 5. The $0 test (registered before it runs)

### T1: the product path
old-2 is replayed under poc-v121 through `replay.run`, serial path.
- **The archive.** A scratch archive seeded with old-2's non-judge calls only, so every judge request misses it and reaches the
  transport and the real validator.
- **The transport.**
  - It finds each judge request's stored old-2 call by its (system, user) bytes; the 1,620 pairs are unique (Codex r38).
  - It asserts that the outgoing request equals the stored one in every key except the format.
  - It asserts that the format has `strict: true` and the name `judgement`, and differs from v7's only in the four citation
    constraints and the `$defs` they use.
  - It asserts that each of the outgoing lists (evidence, dependencies, themes) equals the ids the request shows, read from its text
    (evidence and theme entries; dependency entries).
    - A mismatch is listed with its call and read by hand: a parser case is told from a builder bug before T1 can pass.
    - An extra or missing id in any list fails T1. Codex r38c added an unlisted theme to 1,471 formats and every stored answer still
      validated, so validation alone cannot catch it.
  - It returns the stored answer, which goes through the real `model.call` and `model.check_schema`.
  - Any other request (a non-judge miss, an unknown pair) stops the replay.
- **The four refused first calls** (e88, e3955, e3998, theme ids). Each gets the saved accepted retry answer, labelled as a
  substitution: under strict mode the provider could not have returned the refused one. All four retry answers fit their first
  requests (Codex r38b). The four retry-note requests are not reached and are tested apart (T1b).
- **Pass.**
  - Exactly 1,616 judge responses through the transport, 4 of them labelled substitutions.
  - The replay completes.
  - The store equals old-2's on every table, listed explicitly from `sqlite_master`, with the expected differences named:
    timestamps, archive call ids, request hashes, config checksum and version, and new empty tables.
    - Judgements are compared on every substantive field: view, sequence, input, rung, reasons, reference, implied outcome, cites,
      `cites_views`, pushes, theme pushes, changed, `why_changed`, publication day.
    - Every other table is compared on all its columns but the named ones (handovers, match records, days completed and the rest).
  - New request hashes and the config are checked apart.

T1 does not touch provider acceptance (§6).

### T1b: the four originals
Each refused original goes through the real `model.call` under its v12 request and raises `SchemaError` on the id `check_answer`
refused.

### T1c: a real v12 retry
- A store fixture with a theme in force; a fake provider answers the first v12 request with a duplicate theme push, which
  `check_answer` refuses, then answers the retry correctly.
- Assert that the retry request carries exactly the first request's format, citation lists included, and the retry note.
- Mutant: the retry sent with the open v7 format must fail this test.

### T5: preflight on a judge row without a saved format
A refused judge row whose request has no `response_format` makes `scripts/preflight.py` exit non-zero, with the row named.
Today `main` ignores part A's result, so it also needs a failing exit for this case. Extraction and matching rows keep their
paths.

### T2: every stored shape, offline (evidence from archived text)
- For every stored judge request of old-1, old-2, old-3, control-1 and linked-1, the lists are taken from the saved text. These are
  archived calls whose store state is gone.
- The parser can widen or narrow a list (the footnote case), so T2 is evidence from the archived text. T1 covers the built path.
- Each answer is validated through the real `check_schema` with the v12 format.
- Pass:
  - all 5,389 committed answers and the 2 uncommitted valid ones validate;
  - all 17 refused answers fail on their bad id;
  - the population is printed as in §1.

### T3: the real validator's controls
For all four fields, through `model.check_schema`:
- an allowed id passes;
- an unlisted id fails.

An empty list with `maxItems: 0` passes `[]`, and fails one otherwise valid item of the right type with an array-length error,
not a type error.

T3 fails on today's validator, which ignores `maxItems`.

### T3b: one owner of membership
- A rendered request whose evidence quote holds a blank line followed by "[1]", with a real evidence entry after it. The v12 lists
  include the later id, and `check_answer` under v12 accepts a citation of it.
- The same answer under v7's text parser is refused. This control shows the parser case is real.

### T4: sizes
The largest format over the five archives and over the sealed D358 archive is printed: evidence count, enum values with the
reference counted once and counted twice, and characters.

### Mutants
Each is caught by a test that passes on the unmutated code:
- push ids left open;
- lists parsed from the text instead of taken from the rows (the multiline-quote case);
- `check_answer` under v12 reading the text instead of the lists (T3b);
- `maxItems` dropped for an empty list;
- `maxItems` removed from the validator;
- `strict` dropped from the outgoing format (T1);
- preflight reading the fixed schema for judge rows.

### Also
- Prompt size: the format's characters and tokens before and after, median and max.
- The suite, the frozen tests and `docs/check.py`.

## 6. What the $0 test cannot show

- **Provider acceptance of the exact format:** the shared reference, `maxItems: 0`, and a largest request (D358 call 6918's size).
- **Whether the judge picks the intended source when constrained:** e3111 could become e3110 or e3112.
- **Whether the forecasts move.**

A paid step, Alex's to open, settles these. It would first send the largest stored request and an empty-list request to check
acceptance, then re-send the stored refused requests and a matched set of accepted ones, and read the cited sources beside the
forecasts.
