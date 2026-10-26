# Documentation refresh — October 27, 2026

The README and maintained guides now describe the current POC and its actual entry points. For example, a fresh clone can browse the bundled library, while running the API requires local databases that are excluded from Git.

This is documentation maintenance. No product behaviour, provider, prompt, budget or acceptance criterion changes. Existing product code, extraction and concurrency work remains outside the documentation commit. Linked prose reports and screenshots accompany the documentation; links to other unpublished artifacts are labelled local. No paid calls are needed.

## Findings and scope

The cause is accumulated documentation drift after D165–D241: summaries kept earlier defaults, while detailed decisions and implementation moved forward. The audit covered the root and frontend READMEs, current state, pipeline/service/Idea guides, all ten PRDs and their design-page data. Historical experiments were read as history, not used as current instructions.

| Description counted before editing | Locations | Correction and evidence |
|---|---|---|
| Grouping described as unavailable or an isolated implementation | One README claim; one page-data sentence mirrored in the library PRD and generated bundle | Grouping is integrated under D165/D169. Retain D147 as history; point to the current pipeline guide. Regenerate the PRD block from page data. |
| Idea API described with an old default | One `poc-v9` reference in the pipeline guide | `scripts/hivemind_api.py` selects `poc-v32-idea.json`; the config names `idea-v7` and `idea-summary-v7`. |
| Current and historical Idea contracts mixed | Service introduction; Idea flow diagram, composite response row, confidence paragraph and historical latency paragraph | The default has two discovery calls and a final positive-weight adoption call. Old exclusions/two-call results remain labelled historical under D196. |
| Status cutoff older than the decisions it describes | One header says D234 while the page reaches D241 | Replace the status chronology with current behaviour, measured evidence, open defects and one next task. Preserve the prior text in the linked snapshot. |
| Service paths and startup assumptions | Two root README references to `poc/data/service/`; one MCP description implying HTTP by default | Read defaults from both CLI parsers and Compose. Document `service-english`, local data requirements, MCP stdio default and fresh run directories with their own PID. |
| New UI features missing from the entry guide | Root README lacked the current workspace, confidence, Trigger and Action overview | Summarize D196/D197/D225/D234/D235–D241 and link to their owning specifications. Keep Action's preview boundary explicit. |

The grouping claim's three copies are one source sentence plus its generated readers, not three independent rules. The page data remains the source. No hand-edited generated block or new contract is introduced.

## Reasoning refresh

Read in the order specified by the [PRD index](../../prd/README.md). Each row checks whether this update affects the module, whether page and PRD still agree, whether the example remains valid and whether acceptance/open questions change.

| Module | Result |
|---|---|
| Research universe | No scope or version rule changes. Existing company/theme examples, acceptance and open reference-data questions remain valid. |
| Classification | No category, subject or time-rule changes. Existing examples and recorded simulation limits remain as written. |
| Config | Documentation now distinguishes replay v23 from Idea v32. No settings or version rules change. |
| Dispatch | No routing or sequence change. Redelivery and incomplete-input examples remain valid. |
| Extraction | Current grouping integration is consistently described. No output, prompt, source check or acceptance change. |
| Thesis library | The old grouping-prototype sentence becomes explicitly historical. Its page source and generated PRD agree; membership, identity, evidence and ordering rules do not change. |
| Final verdict | Still an earlier draft; due-date state freezing remains decided. No proposal is promoted. |
| Pull mode | Scheduling detail remains deferred; the due-date example and externally supplied time remain unchanged. |
| Human review pool | Intake stays frozen and output deferred. No new review condition. |
| System overview | Existing glossary entries for Idea confidence, Trigger and Action match the new entry guide. No new concept or system boundary. |

The README now owns runnable startup instructions; service and UI guides link to it. The service guide owns read semantics, the Idea guide owns adoption/confidence, and the UI specification owns presentation. The shorter current-state page points to those owners instead of accumulating past layouts.

## Verification

- Python suite: 165 passed in 20.91 seconds. The first attempt stopped before collection because the sandbox blocked a pytest plugin's local socket; the authorized host run completed. No test or product code was changed.
- Frontend suite: 56 passed. All 20 existing mutation checks rejected their intended changes; lint and formatting passed.
- HTTP and replay CLI help matched the documented options. No service was launched and no model call was made by this refresh.
- All 99 links in the initial maintained-guide check resolved on disk. The complete documentation publication has 200 local links, all backed by tracked or included files. Other artifact references are explicitly local; raw outputs and study scripts remain uncommitted.
- `docs/check.py` passes: 53 generated blocks, 20 wording controls, 71 listed constants, 68 wording locations, 30 English surfaces, classification simulation, ten design nodes and seven detail pages. The bundle contains 11 PRDs.
- Publication inspection covers only documentation and its screenshots. Credential-pattern inspection found one false positive in a source-item identifier, verified in context; no credential was found. Product source, database files and raw research outputs are outside the selected paths.

The [previous status page](current-state.before-refresh.md) preserves the pre-refresh chronology. Relative links were adjusted for its new directory; original claims remain historical.
