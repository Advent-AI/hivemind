# Thesis admission v12: implementation plan

> For agentic workers: use superpowers:executing-plans to implement this plan task by task. Steps use checkbox syntax.

**Goal:** Change what the extraction step is asked to produce so that a new thesis opens only for one of four stated
reasons with a settling source and a stated loss if folded, and measure the change against a 20-case extraction gold on
the NVDA corpus (February 25 to August 15, 2026), serial baseline = the `poc-v23` Jev ledger.

**Architecture:** One owner changes: the extraction output contract (prompt `role-v12`, schema version 12, code checks in
`extraction.sift`). Matching, writing and judging do not change. A scoring script reads any ledger and the gold and
prints per-case full/partial/fail plus a census of theses opened. The run is the product's replay (`scripts/replay.py`,
parallel day by default, D183) under a new configuration `poc-v25`.

**Tech stack:** Python 3 standard library, sqlite3, the project's `hivemind` package; tiktoken only for the prompt-size
audit (already installed).

**Spec:** `reports/对冲基金论点粒度与金标.md` §1 (the eight rules), §3 (customer-project rule), §5 (gold examples), §6
(scoring), §8 (Alex's decisions, 2026-10-26: 1 = the assistant labels 20 cases this round, human review later;
2 = the clean version of option B, prompt + schema-enforced fields, no dedup key; 3 = B; 4 = C; 5 = C).

## Global constraints (AGENTS.md)

- Never grow a prompt to fix quality: report characters and o200k tokens of the role before and after; growth needs a
  written reason.
- Code over prose: the four admission reasons are a schema enum; the fields are required by the schema; code checks
  shape only, the model keeps the judgement of importance (D154/D155; log row 43 rejected a dedup key over free
  scopes, so no key rule is added).
- Stored requests of versions 1–11 stay byte-identical (schema and prompt gated on version 12).
- No hard-coded company, project or topic list anywhere.
- Explicit inputs: paths and configuration as arguments; the ledger of a run gets a new dated folder under
  `/Users/lchingen/hivemind/poc/data/` (not in Git); existing ledgers are read-only.
- Test small first: seed (NVDA only) → week → August, each read before the next.
- Commit only when Alex asks. Credentials never in args or files.

## Review focus (inputs no task's tests exercise directly)

1. An answer under v12 whose candidate names `folds_into` = a shown thesis AND still opens: it is kept (the model's call)
   but the census must count it, because this is the signal Alex wants to read. → Task 4 census column `folds_into`.
2. A v12 candidate with `opens_as = binding_obligation` and measure `event`: both the event path (no year rule) and the
   548-day bound apply; a due day 20 months out is refused. → Task 2 test.
3. A stored v10 answer replayed through the v12 sift must be judged exactly as before (no `opens_as` → old path).
   → Task 2 test + preflight positive control (mutant: guard removed → every stored candidate refused).
4. The scorer meets an item the run skipped (not in `handovers`): report "not processed", never "fail". → Task 4 test.
5. The parallel day re-prepares stale requests; the new schema's `folds_into` pattern depends on shown ids, so a
   re-prepared request must rebuild the schema from the current shown set. `request_for` already does this per call;
   Task 3's round test runs with shown views present.

---

## Design tables (AGENTS §2)

### State × event (one item through extraction under v12)

| State | Event | Transition / what is written |
|---|---|---|
| Request built (shown theses S, shown groups G) | Model answers | `sift_with_groups` → `sift`; new checks run only on candidates carrying `opens_as` |
| Candidate with `opens_as` | `lost_if_folded` or `settled_by` blank | dropped `(id, 'candidate admission: lost_if_folded is empty')` / `'settled_by is empty'`; its evidence keeps other links or is dropped as today |
| Candidate | `folds_into` not '' and not in S | dropped `'candidate admission: folds_into names a thesis not shown'` |
| Candidate `binding_obligation` | due_day > publication_day + 548 days | dropped `'candidate admission: binding obligation due beyond 18 months'` |
| Candidate `binding_obligation`, measure not event | year > publication year + 1 | kept (exempt from 06-views rule 5; D185) when within 548 days |
| Candidate other `opens_as`, measure not event | year > publication year + 1 | dropped as today |
| Candidate without `opens_as` (versions ≤ 11) | any | unchanged path |
| Kept candidate | matching / writing | unchanged: new fields travel in the handover JSON only; `_create_view` reads named fields, ignores the rest |
| Day complete | judging | unchanged |
| Run resumed after a crash | same item re-dispatched | unchanged (parallel day refuses a changed contract via its manifest; a serial resume needs `--workers 1`) |

### Value × reader

| Value | Writer | Readers (found by grep) | Effect |
|---|---|---|---|
| `opens_as`, `folds_into`, `lost_if_folded`, `settled_by` on a candidate | model (schema v12) → `sift` | `round.py` stores the handover JSON whole; `writing._create_view` reads named fields only; `jev_matching.candidate_state` formats named fields only; new: `scripts/score_admission_gold.py` reads them from `handovers` | no reader breaks; the census reads them |
| `extraction.ADMISSION_REASONS` | code | schema, prompt (named in prose, enum in schema), scorer, gold | one enum |
| `role-v12.txt`, `categories-v12.json` | this slice | `config._prompt_files` (existence), `build_prompt` | version-gated |
| `poc-v25.json` | this slice | `scripts/replay.py --config` | new run only |
| gold `poc/eval/gold/extraction-admission-2026-10-26.json` | this slice (assistant-labelled) | scorer; `SHA256SUMS` | sealed by checksum |

### New path × old checks

| Old check | v12 path |
|---|---|
| `check_ladder`, `check_bounds`, QUARTERLY, due_day after item, period dates | unchanged, run before the admission checks |
| year beyond next year (06-views rule 5) | unchanged except `binding_obligation` (D185) |
| `check_group_refs` | unchanged |
| quote in item, links to shown or kept candidates, same-quote merge | unchanged |
| preflight part B over stored answers | unchanged refusals (no stored answer carries `opens_as`) |
| `tests/test_event_horizon.py` (stored NAVER answer) | still passes: that answer has no `opens_as` |
| request identity of 3,595 archived calls | unchanged: versions ≤ 11 build the same schema and prompt |

### Prior decisions searched

D154/D155 (importance stays with the model; code owns only fully determined identity) — respected. Log row 43
(rejected key rule "theme + measure + period") — no key added. D159 (sequential visibility) — untouched. D165/D166
(groups) — untouched. D174/D176/D177 (NAVER horizon; v11 role tested on one source) — v12 starts from v11's text.
D181–D183 (parallel day default) — the run uses it. 06-views ladder rule 5 — amended for binding obligations only
(D185). 06-views open question "thesis granularity" — closed by D184.

---

## File structure

- Create `src/hivemind/prompts/role-v12.txt`, `src/hivemind/prompts/categories-v12.json`, `poc/config/poc-v25.json`
- Modify `src/hivemind/extraction.py` (constants, `admission_schema`, `schema_for`, `check_admission`, `sift`)
- Create `scripts/score_admission_gold.py`; `poc/eval/gold/extraction-admission-2026-10-26.json`; update
  `poc/eval/gold/SHA256SUMS`
- Create `tests/test_admission.py` (contract + sift + round + config), `tests/test_admission_gold.py` (scorer)
- Create `scripts/prompt_size.py` (audit; or inline in the results)
- Modify `docs/DECISIONS.md` (D184–D188), `docs/prd/05-extraction.md` (prose: admission reasons and fields),
  `docs/prd/00-system.md` glossary (+ `docs/check.py` ruled-out words), `docs/system-design/new-*.js` open-question
  text, `docs/CURRENT_STATE.md`, build log row 51
- Create `poc/reports/2026-10-26-admission-v12/` (baseline-v23.md, results.md, census, prompt sizes)

---

### Task 1: The gold (20 cases) and the decisions

**Files:** create `poc/eval/gold/extraction-admission-2026-10-26.json`; modify `poc/eval/gold/SHA256SUMS`;
modify `docs/DECISIONS.md` (append D184–D188).

**Interfaces, produces:** gold JSON `{"version": "extraction-admission-2026-10-26", "label": "assistant", "cases": [Case]}`
with

```
Case = {"id": "A01", "title": str, "items": [input_id, ...], "window": "seed"|"week"|"august",
        "passage": str (≤60 words), "source": str (report §5 例 n / ledger note Gn / Codex 例 n),
        "must_open": [Key], "must_not_open": [Key], "evidence_targets": [Link], "must_not_link": [Link],
        "system_v23": {"views": [...], "score": "full"|"partial"|"fail", "why": str}}
Key  = {"gist": str, "object": str, "measure": str, "year": str, "event_type": str (default "n/a"),
        "scope_regex": str (default ""), "opens_as": one of ADMISSION_REASONS or "", "alternatives": [Key]}
Link = {"quote_regex": str, "target": Key | "self:<must_open gist>"}
```

- [ ] Step 1: Write the 20 cases from report §5 (15) plus: A16 Codex 例 7 (CRWV managed-inference ARR, kept as an
  alternatives-only case), A17 the 247wallst four-company $745bn figure (`gnews:61ba718265df905f5dcc9dad`: must_not_open
  a new aggregate; evidence to the five-company 2026 aggregate), A18 the Bloomberg NAVER retelling (late statement:
  zero theses, a source reference only), A19 the Taiwan smuggling clause (`v23`'s item: evidence to the China licence
  thesis, no thesis), A20 the Goldman 2027 aggregate (`gnews:4a6db5f4d17bc985e47b0e49`: one 2027 aggregate allowed as
  next year; one thesis, not three). Every case names its items by `input_id` from the items db and its passage
  verbatim. Keys use the measure vocabulary of `extraction.MEASURES_V10`.
- [ ] Step 2: `python3 -c "import json; d=json.load(open(...)); assert len(d['cases'])==20"` and every `items[]` exists
  in `poc/data/items-window-tags2-2026-10-24.sqlite` (script in the results folder, output kept).
- [ ] Step 3: Append the SHA-256 to `poc/eval/gold/SHA256SUMS`; `shasum -a 256 -c` passes.
- [ ] Step 4: Append D184 (admission contract: the four reasons, the three fields, rule 8 as the default, Alex's words
  "可以"), D185 (binding-obligation horizon 18 months, "可以"), D186 (ladder labels: outcomes + favourable end; recorded,
  implemented in a later slice), D187 (objects: a company's own quantity under that company even when private;
  recorded, later slice), D188 (gold protocol: assistant-labelled 20 cases, "标20条", human review later).

### Task 2: The v12 contract in code

**Files:** modify `src/hivemind/extraction.py`; test `tests/test_admission.py`.

**Interfaces, produces:**
- `ADMISSION_FROM = 12`; `ADMISSION_REASONS = ['guidance_on_main_driver', 'industry_aggregate', 'policy_stage', 'binding_obligation']`;
  `BINDING_HORIZON_DAYS = 548`
- `admission_schema(shown_view_ids, shown_group_ids, measures) -> dict`: `grouped_schema(...)` plus required candidate
  fields `opens_as` (enum), `folds_into` (string, pattern `^(?:|<shown ids escaped, |-joined>)$`), `lost_if_folded`
  (string), `settled_by` (string)
- `schema_for(version, shown_group_ids=(), shown_view_ids=())` → for number ≥ 12 returns `admission_schema`
- `check_admission(c, shown_ids, publication_day) -> str | None`
- `sift(...)` calls `check_admission` after the period check when `'opens_as' in c`; `request_for` passes shown view ids

- [ ] Step 1: Write failing tests in `tests/test_admission.py` (fixtures from `test_keyed_views`: `ITEM`, `TEXT`,
  `UNIVERSE`, `EVIDENCE`, `candidate`):
  - `test_v12_schema_requires_the_admission_fields_and_v10_does_not`: v12 candidate `required` ⊇ the four names,
    `opens_as.enum == ADMISSION_REASONS`, `folds_into.pattern == '^(?:|v1|v7)$'` for shown `['v1','v7']`; v10 has none.
  - `test_sift_drops_blank_lost_if_folded_and_unshown_folds_into`: three candidates (valid; `lost_if_folded=''`;
    `folds_into='v9'` with shown `{'v1'}`) → kept `['c1']`, reasons contain `'lost_if_folded is empty'` and
    `"folds_into names a thesis not shown"`.
  - `test_binding_obligation_horizon`: `opens_as='binding_obligation'`, measure `financing_amount`, year `2028`, due
    `2027-06-30` (within 548 days of `ITEM['publication_day']`) kept; same with due `2028-06-30` dropped
    `'binding obligation due beyond 18 months'`; `opens_as='industry_aggregate'`, year 2028 → dropped by the year rule.
  - `test_candidates_without_opens_as_follow_the_old_path`: a v10-shaped candidate passes untouched (mutant: remove the
    `'opens_as' in c` guard → fails).
- [ ] Step 2: Run `python3 -m pytest tests/test_admission.py -q`; expected: 4 failures (names not defined / fields missing).
- [ ] Step 3: Implement the constants, `admission_schema`, `schema_for` extension, `check_admission`, the `sift` hook and
  the `request_for` change (`schema_for(version, group_ids, [v['view_id'] for v in shown_views])`).
- [ ] Step 4: `python3 -m pytest tests/test_admission.py tests/test_event_horizon.py tests/test_groups.py tests/test_keyed_views.py -q` → all pass.
- [ ] Step 5: Preflight positive control: `python3 scripts/preflight.py --archive /Users/lchingen/hivemind/poc/data/english-v23-jev-2026-10-25/archive.sqlite --items /Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite --views /Users/lchingen/hivemind/poc/data/english-v23-jev-2026-10-25/views.sqlite` → part B refusals equal the saved control (`poc/reports/2026-10-26-e2e-parallel/preflight.txt`); then with the guard removed on a scratch copy of `extraction.py` every stored candidate is refused (output kept in the results folder), restore.

### Task 3: Prompt v12, categories v12, configuration v25, prompt-size audit

**Files:** create `src/hivemind/prompts/role-v12.txt`, `src/hivemind/prompts/categories-v12.json`,
`poc/config/poc-v25.json`, `scripts/prompt_size.py`; test in `tests/test_admission.py`.

**Interfaces, consumes:** Task 2's schema. **Produces:** `poc-v25` with every category `T*-v12`, otherwise `poc-v23`.

- [ ] Step 1: `role-v12.txt` from `role-v11.txt`. Replace the five "Which questions to propose" bullets with: (a) the
  default is evidence to a shown thesis; (b) open a candidate only for one of the four reasons, named in `opens_as`:
  the company's own annual guidance on a main driver of its value; one industry aggregate per calendar year, a later
  estimate or another population of the same aggregate is evidence to it; a policy stage with its authority named; a
  binding obligation a universe company takes on (guarantee, financing, equity, purchase commitment), due when the
  signing can be checked, at most 18 months out; (c) `settled_by`: the public material that resolves it; (d)
  `folds_into`: the shown thesis the statement would otherwise attach to, or empty; `lost_if_folded`: what investment
  implication is lost if it only attached there, and a different population, source, estimate or wording is not a
  loss; (e) keep the ban list (quarterly figures, beyond next year except binding obligations, moats, appointments,
  votes, litigation procedure, buybacks) and the milestone/metric distinction. Remove nothing else. Target: fewer
  characters than v11 (6,567 system chars measured in D177); if more, write the reason in results.md.
- [ ] Step 2: `categories-v12.json` = `categories-v11.json` with the `_note` saying version 12 exists for the admission
  fields (D184); entries identical.
- [ ] Step 3: `poc-v25.json` = `poc-v23.json` with `T*-v12`, `version: poc-v25`, `_note` naming D184.
- [ ] Step 4: Tests: `test_config_v25_loads_and_builds_a_v12_request` (`config.load(poc-v25)`, `extraction.request_for`
  on `ITEM` with two shown views → system text starts with the v12 role's first line, schema has `opens_as`, pattern
  carries both ids); `test_round_writes_a_v12_candidate_end_to_end` (mirror `test_groups.test_round_runs_the_grouped_contract_end_to_end_with_a_scripted_model`
  with the four fields in the scripted answer; assert the view is written and `handovers.handover_json` carries
  `opens_as`). Run → pass.
- [ ] Step 5: `scripts/prompt_size.py`: prints chars and o200k tokens for `role-v10`, `role-v11`, `role-v12` and for one
  stored T4 request (the NVDA 2026-02-25 call, archive call of the v23 arm) rebuilt under v10 and v12 (system + user +
  schema). Save to `poc/reports/2026-10-26-admission-v12/prompt-size.json`.

### Task 4: The scorer

**Files:** create `scripts/score_admission_gold.py`; test `tests/test_admission_gold.py`.

**Interfaces:** `python3 scripts/score_admission_gold.py --gold <json> --views <ledger> --items <items db> --universe poc/universe.json [--out <md>]`.
Functions: `view_matches(view_row, key_row, key) -> bool`; `score_case(conn, case, universe) -> {"id", "score": "full"|"partial"|"fail"|"not processed", "missing_must_open": [...], "extra_opened": [...], "missing_links": [...], "forbidden_links": [...], "opened_by_items": [...]}`;
`census(conn) -> {"theses": n, "by_object": {...}, "by_measure": {...}, "by_opens_as": {...}, "folds_into_named": n}` (reads `handovers`).

Matching rule: object equal after `universe.resolve`; measure equal; year equal; `event_type` equal when the key's
measure is `event`/`policy_event`; `scope_regex` (when given) matches `scope` or `question`, case-insensitive. A
must_open is met when a view with that key (or any alternative) has an evidence link from one of the case's items.
A must_not_open fires when a view with that key was *created* by one of the case's items. An evidence target is met
when an evidence row whose quote matches `quote_regex` is linked to a view matching the target. Score: fail if any
must_open or evidence target missing; else partial if any must_not_open fired; else full. "not processed" when none
of the case's items appears in `handovers`.

- [ ] Step 1: Failing tests on a real ledger in `tmp_path` built with `store`: two views (NVDA gross_margin FY2027;
  NVDA tax_rate FY2027) both created by item X with links from X; gold case must_open gross_margin, must_not_open
  tax_rate, evidence target `mid-70s` → `partial`; remove the tax_rate view → `full`; remove the link → `fail`; a case
  whose item is not in handovers → `not processed`. Mutant: scorer ignoring must_not_open → test fails.
- [ ] Step 2: Run → fail (module missing). Implement. Run → pass.
- [ ] Step 3: Baseline: run the scorer on `/Users/lchingen/hivemind/poc/data/english-v23-jev-2026-10-25/views.sqlite` →
  `poc/reports/2026-10-26-admission-v12/baseline-v23.md`. Compare with report §5's hand scores (2 full / 7 partial /
  7 fail on 15); every disagreement is read and either the gold key or the scorer is corrected before any paid run.

### Task 5: Documents

**Files:** modify `docs/prd/05-extraction.md` (prose under "Two outputs" and "Acceptance"), `docs/prd/00-system.md`
glossary (row "admission reason"), `docs/check.py` (`AVOIDED_WORDS` + control: "opening reason" → "admission reason"),
`docs/system-design/new-*.js` (the granularity open question → decided, D184), `docs/CURRENT_STATE.md` (status + next task).

- [ ] Step 1: Edit; `python3 docs/check.py` passes (it rebuilds the PRD bundle).
- [ ] Step 2: Reasoning refresh: re-read 05, 06, 00 for the admission wording; list each inconsistency fixed in results.md.

### Task 6: Measure

**Files:** `poc/reports/2026-10-26-admission-v12/results.md`, `census-*.json`, run logs under
`/Users/lchingen/hivemind/poc/data/english-v25-admission-2026-10-26/`.

- [ ] Step 1: Preflight ($0) as in Task 2 Step 5; unchanged refusals.
- [ ] Step 2: Seed, detached with log and pid, cap $3 (the cap the v23 arm ran under):
  `python3 scripts/replay.py --from 2026-02-25 --until 2026-07-23 --only NVDA --config poc/config/poc-v25.json --views /Users/lchingen/hivemind/poc/data/english-v25-admission-2026-10-26/views.sqlite --archive .../archive.sqlite --testdb /Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite --cap 3`.
  Read the day table; score the seed cases (A01–A03, A08); census vs v23 seed (NVDA theses). Read every miss to its raw
  answer. Stop and report if a seed case the baseline passed now fails for a reason in the new fields.
- [ ] Step 3: Week 2026-07-24..31 (no `--only`), same ledger; score week cases; census.
- [ ] Step 4: August 1–15; score all 20; census; cost from tokens at `model.PRICES`.
- [ ] Step 5: results.md: per-case table v23 vs v25, census table (theses by object / measure / opens_as; 90 baseline),
  prompt sizes, cost, the misses read, what the fields show (how often `folds_into` named a thesis and the model still
  opened), and the open defects. Build-log row 51; CURRENT_STATE; D184 result line.

### Task 7: Review

- [ ] Codex read-only review of the diff (scope: extraction contract, scorer, gold keys; out of scope: matching, writing,
  parallel day); each lead checked against the code before acting; fixes with tests. Full suite once.
