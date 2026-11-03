Ready within scope. No serious findings.

- Both prompts exactly match the saved inference-check control/treatment. The sole difference is the 290-character paragraph.
- All 20 requests preserve identical source text and schema order across models and conditions. Each within-model pair changes only the system prompt.
- The added paragraph applies to every added business link, including note, limitations and proposal content.
- The plan is five cases × two models × two prompts × three repeats: **60 calls**.
- Calibration distinguishes conditional inference from fact error and signed `proposal=null` from lost content. Repeated answers are not treated as independent source samples.
- Independently checked all 32 D218 answers: every matching request has empty catalog/history, and every answer has zero argument updates. The old paragraph-scoping concern is supported.

Budget and harness remain outside this review. No network access or edits.