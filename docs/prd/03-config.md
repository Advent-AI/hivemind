# Config

> Status: first version frozen, October 18, 2026. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Config. Recorded decisions take precedence over this PRD.

## Purpose

Config contains settings a person must choose: extraction model settings per category, separate matching and rejudgement settings, final-verdict settings, and the thesis search result count. Extraction owns category content and prompt assembly.

The old system had five overriding configuration layers and several presets. Multiple switches could control one feature, so a file did not reveal actual behaviour. Here the universe owns research scope, classification supplies item metadata, and code owns ordering and failure handling. Config retains only deliberate human choices.

## Recorded settings

<!-- generated: schema -->
| Item | Meaning | Source |
|---|---|---|
| Version | Every settings change creates a new version. | Created when settings change |
| Checksum | Calculated from the complete configuration and recorded with every model call, including extraction, matching, rejudgement and final verdicts, so the exact version can be traced. | Calculated by code |
| Model settings and search result count | Extraction has settings per category: model, prompt version, reasoning effort and temperature (lower temperature makes answers more stable). The thesis library has separate matching and rejudgement settings; final verdicts have their own. Config also sets the search result count, initially 10. Prompt content belongs to the extraction, thesis library and final-verdict modules. A settings version is immutable; a change creates a new one. | Chosen by a person |
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

- Every extraction, matching, rejudgement and final-verdict call records Config version and checksum.
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
- D27/D33: separate matching settings. D29: final-verdict settings.
- D41: separate model-call settings and temperature. D45: proposed duplicate checks are not approved and receive no settings yet.
- D46: search result count N, initially 10. D47: Config is not limited to model settings.
- D51: dependency selection occurs within matching, so the library has matching and rejudgement settings, not a separate dependency call.
