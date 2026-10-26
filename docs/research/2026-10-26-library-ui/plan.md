# Current-library frontend — October 26, 2026

Alex asked to rebuild the frontend against the current backend and collected database. Scope: read-only bundle/API/MCP projection, frontend contract, library navigation and existing detail components, build/launch documentation. Extraction, matching, prompts, scoring, group assignment, paid calls and the concurrent acceleration work are outside scope.

## Diagnosis and decisive proof

The adopted English Jev ledger contains 90 theses, 90 identity records, 227 judgements, 534 distinct evidence records, 716 evidence links, 784 source records, 15 replacements, 18 groups and 51 memberships. Fifty theses have no membership. Dependencies, resolutions and successions each contain zero records. All data is read at or before the last completed day, August 15, 2026.

The shell embeds an old 42-thesis translated snapshot, starts with no library navigation and obtains live records only after a paid Idea request. `bundle.view_bundle` omits identity, groups, successions and all but the first source. Its dependency projection omits resolutions; replacement display uses the statement date instead of when the replacement was recorded. These omissions affect all 90 identities, 18 groups/51 memberships and every multi-source record; they are read-layer omissions, not missing clustering in the collected ledger. The Vera Rubin group g1 is a known positive control.

Proof: serialize the actual complete English ledger read-only; adapt it through the same closed frontend contract used by agents; assert exact membership/source/evidence counts and select g1 without inventing a parent. Legacy ledgers with actual dependency records exercise those paths. A temporary real ledger supplies dated resolution/replacement cases absent from the current corpus. Mutate the historical selectors on a scratch copy and require failure.

## Prior decisions

D130: “Use one versioned, closed schema, one adapter for existing bundles, pure dated selectors”. D138: “neither list order nor the first chosen thesis creates a dependency”. D149/D165/D166: groups describe ongoing matters; membership is stored by ingestion. D163: English UI; preserve original quotations. The previous no-UI scope bounded those extraction experiments; this explicit request authorizes this read-layer slice. No generated overarching thesis or group score exists in this ledger, so none is displayed.

## State × event

| State/event | Transition and reads/writes |
|---|---|
| Initial page, valid bundled snapshot | Render library from last completed day; no network/model required; no database write |
| Refresh against configured API succeeds | Validate entire envelope then replace atomically; update library and Idea explorer together |
| Refresh fails, refused retry, malformed payload | Keep prior snapshot, display failure and explicit retry; never silently claim live data |
| Refreshes overlap / switch library to Idea / destroy | Abort superseded request, ignore late results; destroy listeners and drawer; no stale repaint |
| Filter/group/date changes | Derive from one immutable snapshot; group membership and every relation use their recorded day; ungrouped stays explicit |
| Day before creation / empty group / no judgements | Hide future records; show empty state, never invent assessment |
| Live ingestion / corrected source / new config during read | SQLite read transaction pins a single ledger snapshot; next explicit refresh obtains a new snapshot; no cache merge by local IDs |
| API interruption/crash/in-flight at browser close | No persistent frontend work or ledger writes; reopening uses bundled snapshot then optional refresh |
| Two components / two scopes | Instance-local state and event cleanup; a new envelope replaces all scoped IDs |
| Idea request | Existing explicit submit path and selected as-of day; no automatic paid request; return to library retains its data/filter |

## Value × reader

| Value/source | Writer | Readers |
|---|---|---|
| Thesis identity/year, bounds | Ledger writer → bundle projector | Adapter, detail metadata; no numeric inference from prose for current library |
| Group/name/scope/aliases; dated member IDs | Existing group tables → bundle projector | Contract, library sidebar/filter, detail group membership; peers, not dependencies |
| Sources and recorded arrival dates | evidence_sources/items → bundle projector | Evidence provenance, source counts; quotes unchanged |
| Replacement recorded day | replacements.seq → sequence date | Historical superseded state and active evidence counts |
| Dependencies and resolution timeline | dependencies/resolutions → bundle projector | Dated relationship selector/detail; waiting target can be null |
| Earlier/later period links | successions → bundle projector | Dated relationship selector/detail, separate from group membership |
| Envelope/as_of/days | Read-only snapshot builder | Shared contract, library filters, Idea explorer |
| Embedded snapshot | mock_build using explicit ledger/items | Browser initial state; labelled collected snapshot, not a live connection |

## New path × old checks

| Path | Checks |
|---|---|
| Full-library HTTP/MCP | Same read-only bundle writer, date validation, stable IDs, no future rows; no model/search needed |
| Current bundle → thesis-ui/2 | Closed schema, original unknown-field rejection, unique IDs, valid dates/states/citations; group membership references loaded theses |
| Legacy bundle or thesis-ui/1 | Explicit adapter/defaults; unavailable identity/group fields remain absent/null/empty, never reconstructed |
| Library navigation | Filter by actual subject/group/status, no guessed links; pre-creation and quiet-day selection use existing history rules |
| All sources / historical replacement | Source date and recorded day kept separate; original HTTP/HTTPS-only link safety and escaped text |
| Existing Idea canvas | All chosen roots and supplied via edges unchanged; cancelled requests cannot repaint library |
| Build/start | Default standalone build uses current English ledger/items, explicit --data retains legacy fixtures; API/MCP ledger defaults align with snapshot, explicit old paths still work |

Size budget remains 200 KiB of browser JS, using minified production output if necessary; validate full current snapshot within 200 ms. Measure full export and render, no extra framework/dependency. Verification: current/legacy corpus and temporal edge cases, HTTP/MCP paths, existing UI tests/mutants, real browser navigation/detail/history/error states, full Python suite once, reasoning refresh then docs/check.py last. Hash collected input databases before/after. No commit or push requested.

### Field and snapshot details

`thesis-ui/2` adds required dataset `groups` and required thesis `year`, nullable `identity`, `successions`; evidence adds `sources` and replacement `day` (nullable only for undated legacy exports); dependency adds nullable target, waiting-chain ID and dated/ordered resolutions. `fromBundles` upgrades old wire bundles with explicit empty/unknown fields. `parseDataset` accepts the old canonical v1 through a single compatibility conversion that retains unknown keys for rejection. No membership date, identity or replacement arrival is guessed. An undated legacy replacement is retained without asserting when it superseded the prior evidence.

Group objects expose only members included in the envelope and never claim those are the entire group's population. Full-library reads include all dated theses, open and closed. Empty history has an explicit as-of supplied by caller; an uninitialised database without completed days returns an error, not today's date. Read transactions wrap complete bundle assembly; source DB is also held in a read transaction. The shipped static snapshot and API/MCP defaults target the same English ledger and items DB. Switching datasets is whole replacement, never merging local IDs. Refresh discards any prior Idea response because its IDs belong to its original snapshot. Browser filters use the selected day; Idea submits that exact day. Library filters remain when returning from Idea. Default service Idea prompt stays explicitly configured; this work does not silently activate a different model or prompt.

### Review resolution before implementation

Read-only review found three missing dimensions; each was checked against the named functions.

| Additional state/reader | Required behavior |
|---|---|
| Historical judgement selected inside a later drawer | Evidence status and visible source list use the selected judgement's day, not drawer opening day. Current overview uses drawer day. Real-data audit will count earlier citations on later-replaced evidence. |
| Selected-thesis bundle, including Idea | Envelope declares `coverage: selection`; group members include only loaded thesis IDs. Full-library envelope declares `coverage: library`. Library coverage is required for a full-library claim. A legacy/agent selection is explicitly labelled Loaded theses, and details show only loaded related theses; no inferred whole-group count. |
| Valid replacement snapshot has a narrower date span | Compute retained graph/filter IDs and clamp selected day to the new span before changing any data or DOM. A bad dataset fails before any mutation. Reset an Idea graph on library refresh; library filters are retained only when their values still exist. |

The full table walk preserves original state, source, identity and ordering contracts under these additions. No core product choice changes. These resolve the three findings; the implementation follows these explicit rules.

Source attribution census: all 534 current evidence records supply a speaker, and 34 repeat that speaker in original_who. Display uses the recorded original source when present, otherwise the recorded speaker, with publisher kept separately. Preserve original statement date and event/period text. Stored evidence IDs in assessment text link to their evidence; source text and model answers are not rewritten.

The source writer defines `original_day` as free text, unlike ledger recording days: 4 current and 31 older records contain a month, range or an unspecified-date statement. The UI preserves it as textual `original_date`, formats only full ISO days and never uses it for historical visibility. This removes an overly strict frontend calendar assumption for the entire counted class.

Final documentation census found three additional current-status statements still saying grouping was not integrated: the extraction relations statement (page source plus generated PRD), extraction decision summary and library acceptance paragraph. D165 and the current ledger's 51 stored memberships contradict that status. Correct these three owners/four surfaces to D165 while preserving the semantic acceptance limits; regenerate the marked PRD block from its page source. This is a status correction, not a new extraction rule.

Public-entry check found one export omission introduced by this slice: the standalone page exposed `createLibrary`, but the package entry `src/index.js` did not. Put the export beside the other public components and make bootstrap consume that same entry. Verify import from the package path as well as the existing standalone browser lifecycle. No component behavior changes.

The standalone-host check also covers the styling boundary: like `createThesisExplorer`, `createLibrary` attaches the shared `hm-ui` scope to its host. The browser check uses a body without that class so the page shell cannot hide a missing component style scope.
