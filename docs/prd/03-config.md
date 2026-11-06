# Config

> Status: first version frozen, October 18, 2026. English edition: October 25, 2026 (D163); corrected to D169, D190 and D364 on 2026-11-05 (D367).
> Design page: `docs/system-design.html` → New → Config. Recorded decisions take precedence over this PRD.

## Purpose

Config contains settings a person must choose (D2): extraction model settings per category; separate settings for matching, the collision judge (the generative model that decides whether a candidate and a thesis of its own subject and measure are one question, D190) and rejudgement; and the thesis search result count. A final-verdict setting stays in the frozen configurations and is read by no step (D356). Extraction owns category content and prompt assembly.

The old system had five overriding configuration layers and several presets. Multiple switches could control one feature, so a file did not reveal actual behaviour. Here the universe owns research scope, classification supplies item metadata, and code owns ordering and failure handling. Config retains only deliberate human choices.

## Recorded settings

<!-- generated: schema -->
| Item | Meaning | Source |
|---|---|---|
| Version | Every settings change creates a new version. | Created when settings change |
| Checksum | Calculated from the complete configuration and recorded with every model call, including extraction, matching, the collision judge and rejudgement, so the exact version can be traced. | Calculated by code |
| Model settings and search result count | Extraction has settings per category: model, prompt version and reasoning effort. The thesis library has separate matching (the Jev engine, D169) and rejudgement settings, and an optional collision-judge setting: the generative model asked whether a candidate and a listed thesis of its own subject and measure are one question (D190); a version without it leaves matching to Jev alone. Config also sets the search result count, initially 10. Prompt content belongs to the extraction and thesis library modules. A settings version is immutable; a change creates a new one. | Chosen by a person |
<!-- /generated: schema -->

## Rules

<!-- generated: rules -->
1. Config owns human-selected model settings and the thesis search result count. Upstream classification supplies category, publication day and subjects. Code owns processing order and failure handling. The research universe owns subjects and tracked categories.
2. Config does not set spending or concurrency limits.
3. Any change creates a new version. Preserve old versions without modifying them.
4. Missing required values or references to nonexistent model settings invalidate the entire version. It cannot process any item.
<!-- /generated: rules -->

## Example

Changing the news prompt creates a new configuration version. Subsequent news extraction uses it; other categories retain their settings. Earlier processing records still identify their original version.

## Acceptance

- Every extraction, matching, collision-judge and rejudgement call records Config version and checksum.
- Missing required values or nonexistent model settings invalidate the entire version.
- Any change creates a new version without changing the old one.
- Config does not select processed categories or contain spending/concurrency settings.

## Open questions

<!-- generated: open -->
- None currently.
<!-- /generated: open -->

## Related decisions

- D2: human choices only. D3: no spending/concurrency limits in Config. D18: category selection belongs to the universe.
- D19/D37: first-version freeze; changes need a decision.
- D25: extraction settings per category; reading content belongs to extraction.
- D27/D33: separate matching settings. D29: final-verdict settings, read by no step since D356.
- D41: separate model-call settings; D374 removes the unused sampling setting. D45: proposed duplicate checks are not approved and receive no settings yet.
- D46: search result count N, initially 10. D47: Config is not limited to model settings.
- D51: dependency selection occurs within matching, so the library has matching and rejudgement settings, not a separate dependency call.
- D169: the matching setting names the Jev engine. D190: an optional collision-judge setting beside matching; a version without it leaves matching to Jev alone.
- D370: the separate coverage-start reading is retired; the replay refuses historical settings that enable it.
