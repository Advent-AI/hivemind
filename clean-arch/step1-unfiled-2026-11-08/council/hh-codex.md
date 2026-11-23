**NOT READY — I could not complete the independent review needed to declare version 25 ready.**

For example, I verified that the original dry run caught all 11 planted faults under their intended marks for both readers, but that does not establish that Stage A will catch every misleading ladder. I did not complete the requested fixture-by-fixture and sentence-by-sentence walks.

What I did verify:

- **hg’s three findings are addressed in the written design.** [Check 1](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:284) explicitly refuses four or six ranges and six states, with entry-point tests specified. [Check 8](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:369) specifies full response capture and spending-limit accounting independently of the truncated archive. [The state table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:477) removes the duplicate-count claim. These are design specifications; the new implementation has not yet been built or tested.

- **The first two Stage A dry-run summaries match their stored results.** Running their existing read-only score scripts reproduced 11/11 planted faults for each reader in the first dry run and 9/9 for each in the second. The first also reproduced the reported three versus zero failed marks on the seven supposedly sound examples. The saved Codex answers give the reasons for those three marks. See [the first score script](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/dryrun/score_dryrun.py:1) and [the second](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/dryrun2/score_dryrun2.py:1).

- **The distinction between a sound answer and a valid code fixture is explicit.** [The design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:245) says the examples test shapes and written rows, while the readers assess substance. I did not find a reason in the material I checked to reopen that settled stance.

The remaining review work is material: walk all eight fixtures through every check and written row; audit every request and schema sentence against its cited source; check the three design tables against their actual readers and old checks; and trace the claims from `dryrun3` through `dryrun8` and `reference` to the saved answers. Until those are done, I cannot answer whether a wrong answer escapes all reader marks, whether two engineers could implement different behavior, or whether all six Stage A lines can fail and cannot pass for a wrong reason.

No files were edited, and no model calls or runs were started.