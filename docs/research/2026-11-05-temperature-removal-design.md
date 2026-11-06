# Remove the misleading model sampling setting

Alex, 2026-11-05: “干掉所有的tempaerature 参数这个confusing了”. Scope: runtime model configuration and requests, the current replay default, and current design statements. Historical frozen configuration files, request archives, gold and historical reports are evidence, not editable live settings.

## Census and contract

There are 15 tracked configuration files plus the current untracked v117, all carrying the old field. `Setting`, `_setting`, `build_request`, and `scripts/mock_translate.py` are the live Python owners. Current system-design data and PRDs describe it as effective. The OpenAI request builder already omits it. The non-OpenAI branch sends it, so removing it changes that branch to the provider default; no performance equivalence is claimed. The configured replay default uses OpenAI. A sampled request in the v2 experiment confirms the OpenAI wire request contains no such field.

The `poc-v108` bytes are hash-pinned and `poc-v116`'s checksum is in acceptance records. Preflight loads the named historical configuration, verifies its canonical checksum, and checks selected parts of saved requests before replaying the saved answers; it does not rebuild a full request. Rewriting old configs would invalidate evidence, so leave historical bytes untouched and ignore the legacy field at runtime. New config `poc-v118`, copied from v117 without the field, has its own version and checksum; the replay default moves to it. The Idea API has its own current default `poc-v33-idea`: create a field-free `poc-v118-idea` with otherwise identical settings and move that default too. Six utility entry points default to v1, v2, v7 or v9; each is changed to a new field-free copy of its previous configuration, retaining its own model and prompt choices. The field is removed from the live Setting and never sent by either provider path. Explicitly compare production-built OpenAI request bytes before and after; do not infer equality from preflight. This is not an endorsement of the alternate-provider default.

## Values and readers

| Value | Writers / readers | Outcome |
|---|---|---|
| Config bytes, version, checksum | old configs, new v118 and v118-idea; `config.load`, preflight, archive, run identity | old bytes/checksums unchanged; each new config has a distinct identity; cache hits may reuse a row recorded under the earlier config |
| Setting fields | `_setting`, test and translate callers, `build_request` | old unused field ignored, no attribute or required key; all other fields retained |
| Model request | `build_request`, archive identity, transport | OpenAI unchanged; other provider no longer receives the field and uses its default |
| Model/prompt/effort | both configs; extraction, matching, judgment | v118 equals v117 for all active fields |

## State and old checks

| Situation | Handling |
|---|---|
| Before first run or fresh later run | default v118, no old field |
| Historical archived call / existing ledger | old config file and checksum still resolve; saved request is preserved |
| Interrupted parallel day | environment identity includes the setting shape; the existing manifest may refuse even with a historical config. Do not resume an interrupted run across this change without a fresh run; no live runs were found |
| Interrupted serial item | the entry point does not generally guard configuration changes. No assertion of refusal; do not resume across this change |
| Later run on a completed non-seeded library | read with the selected new configuration as before; do not claim new historical acceptance |
| Missing other required settings or prompt | existing config checks refuse |
| Alternate provider | parameter omitted; provider default behavior is not equivalent to prior explicit value |
| Historical alternate-provider request with this field | new requests have a different identity and cannot be assumed to hit the old cache; inspect the saved request and answer directly, not a resend. No such request was found in the 82 local archives examined by the reviewer; the conclusion does not cover other archives |

Tests must prove both new defaults load without the field and match their respective predecessor apart from version/field, old configs retain their checksums, request bytes are equal for predecessor vs new OpenAI settings, and neither provider request contains the field. The frozen-default assertion must be updated for v118 while retaining the v108 file hash and v116 acceptance checksum. Test real CLI defaults and cache reuse; mutate the request builder to reintroduce the field and show the test fails. Run frozen-ruler and frozen-config tests, relevant tests, full suite and documentation check. The prompt experiment is a separate experimental worktree and must not change these runtime files while a run is live.

An independent read-only review found the four gaps above; each correction was checked against `dispatch.py`, `parallel_day.py`, `preflight.py`, the frozen test and API entry before amending this design. A second review found the conditional historical alternate-provider cache miss described above; its limitation is recorded explicitly rather than treating a new request as a replay.

The implementation review found four utility defaults still pointing to old files; a complete entry-point search found two additional ones. All six now select separate field-free copies of the same historical configurations. This does not change their other configured choices. It also verified seven stored Idea requests against actual archived request hashes; a separate local check rebuilt all ten stored v2 extraction wire requests. Historical alternate-provider caches with the removed field remain a documented limitation; no such requests were observed in the local archives surveyed.
