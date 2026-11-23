**Not ready.** The main blocker is the $2 limit: the plan permits a stopped draw to start again with a fresh $0.66 allowance, while the other draws may already have spent their allowances. That can take the authorized total above $2. A second issue can let a newly opened, already-due question be judged before the date check catches it.

Stage A has **not passed**. D429 nevertheless authorizes Stage B after a review finds nothing serious, with all three draws capped at $2. [D426]( /Users/lchingen/hivemind/docs/DECISIONS-log.md:4727), [D429](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4771)

### 1. Design and implementation

The principal path matches the run plan: each stored first-send answer is placed at the opening article, before that article’s evidence; no seed or ruler views are created; links go to the corresponding new view; and the day’s writes are committed before judging. The use of **stored** answers is intentional in Stage B’s plan, although it differs from the live ladder calls described in the general state table. [Run plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:9), [replay](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:221), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:954)

Departures and qualifications:

- `config_checksum` contains a label and a truncated hash of the **outcomes file**, not the ladder configuration checksum required by the table. It identifies the source file but mislabels provenance. The Stage A runner separately calculates a configuration checksum. [Adapter](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:205), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:938), [Stage A](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/stage_a.py:142)
- `reference_status` can correctly contain `last reported figure`, which the writer produces, but the table lists only `reference figure` and `no reference figure`. The table needs to reflect the actual third value. [Writer](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:335), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:944)
- The inherited count `links through a matched clean thesis` describes links through the new one-to-one mapping as though they were ruler matches. The required count of views with no opening evidence is also absent. Both affect interpretation of the report. [Base link writer](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:193), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1037)
- `created_from_input` follows the specified first evidence input or `article:<sequence>` fallback; sequence and date are taken from the opening article. The other `clean_ladders` columns and the status, reason, checked-answer and outcome-record assignments follow the table, subject to the checksum and reference-status points above. [Adapter](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:128), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:950)
- Identity verification compares each stored case’s **description** to the trace and requires one outcome per case. It does not independently establish that the saved outcome was produced from the complete matching case, or verify the other thesis and article inputs. [Adapter](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:175)

### 2. Stops and dates

The day’s view and evidence writes are one transaction, and a stopped folder is not reused because creation requires a new directory. Later links, unchanged ladders, separate duplicate theses, judging only views with evidence, theme-triggered judging, and the frozen judge’s refusal and transport behavior follow the stated path. The stored-input approach makes the table’s ladder-call, ladder-retry and ladder-transport cells **inapplicable to this replay**, rather than tested live here. [Replay](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:196), [judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:284), [state table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:992)

The due guard checks existing views at the start of each day and once after the final day. A view created **during** the day is not checked before that day’s judgement; if already due, it can be judged before the next guard, or before the final guard stops the run. The current stored first-send ladders have no due day on or before July 14, so this does not appear to affect these inputs, but it violates the promised guard for an input the mode can receive. [Adapter](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:168), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1018)

A view with no opening evidence remains unjudged until it gets a link, as intended, because the judge requires evidence in force. Its required count is missing, as noted above. [Judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:300)

### 3. Spending

Within one live process, each attempt gets a reserve under the same lock before transport is called, and the charge is written under that lock after the attempt. The ledger total uses the charge when present and the reserve for an unfinished attempt. A crash with a call in flight therefore leaves a conservative recorded amount, assuming the synced reserve line is intact. [Ledger](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:60)

The $0.66 allocation is comfortably above the plan’s approximately $0.15-per-draw estimate, but that estimate comes from earlier judge costs and fake-judge request counts; it is not a guarantee of real usage or retries. Three initial processes, each actually launched at $0.66, have $1.98 of nominal allowances. [Run plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:20)

That does **not** enforce $2 across the whole Stage B:

- A redo starts in a new folder with a new in-memory budget. The plan allows a redo without deducting the stopped draw’s spend or outstanding reserve. [Run plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:36), [budget initialization](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:111)
- Each process accepts the caller’s `--cap`; there is no shared cross-process limit. [CLI](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:240)
- The hard-limit argument assumes the reserve is at least the eventual charge. The budget estimates this from serialized request size and the output cap; the code does not independently enforce that reported usage is within that reserve. [Budget](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:30)

A shared accounting rule must cover **all initial draws, unfinished attempts and any redo** before a send.

### 4. Frozen judge and readers

The mode calls the existing judge and inherits its evidence selection, 400-character quote cut, theme block and two-refusal behavior. It does not edit those rules. [Adapter](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:245), [judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:121), [refusals](/Users/lchingen/hivemind/src/hivemind/views/judging.py:317)

I found no reader of `clean_ladders` in production source. The view fields do reach the judge and the store’s other readers, as the design describes; `created_from_input` also reaches product-facing bundle and service code, though those paths are not run here. [Design’s reader table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:900), [bundle](/Users/lchingen/hivemind/src/hivemind/bundle.py:99), [service](/Users/lchingen/hivemind/src/hivemind/service.py:157)

The stored theme views use theme-specific numeric labels or event labels, rather than the company labels; the writer selects labels by object kind. The judge’s frozen general instructions still apply to themes, so the result should be read as the behavior of that existing judge on these new questions. [Writer](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:344), [judge prompt](/Users/lchingen/hivemind/src/hivemind/prompts/judging-v7.txt:1)

### 5. Tests and evidence limits

The nine tests state their intended requirements, use a fake judge and install credential refusals. They cover the u1 replay, stored view fields, row presence, basic links, a successful ledger, cap refusal, a due-date stop, description mismatch and output location. [Tests](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py:22)

The plan reports a passing control and seven caught mutants. I inspected the mutant script, but **did not run it**, because it creates and deletes a scratch tree. Its success check treats any nonzero test exit as a caught mutant and does not itself establish that the failure was the intended assertion; I therefore cannot independently confirm every reported catch or that every test fails without its particular code. [Mutant runner](/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/mutants-stage-b/run.py:29), [reported result](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:31)

Not demonstrated by these tests: the live entry point and all three draws under real caps; simultaneous in-flight attempts and process failure; transport retries and failed ledger writes; a twice-refused judgement and partial level commits; a due view **opened on its due day**; a view with no opening evidence; all `clean_ladders` fields and configuration provenance; and the combined cap including redo. The run plan reports three fake-judge dry runs, but does not document the required preflight result or its skipped cases. [Tests](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py:98), [preflight rule](/Users/lchingen/hivemind/AGENTS.md:174)

### 6. Result readability

The 34 u1–u3 stored cases comprise 26 ladders and eight no-ladder answers. I found no duplicate thesis IDs within a draw; `v<N>` is created in a separate database per draw, so the observed IDs do not collide. The stored theme labels and dates also do not show the suggested company-label or in-window-date problem. These checks do not replace verification of the complete case-to-outcome provenance or the missing counts. [Inputs](/Users/lchingen/hivemind/poc/data/clean-ladder-stage-a-2026-11-10/run-4/send-1/outcomes.jsonl), [adapter mapping](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:128)

**Not ready — first enforce the $2 total across concurrent draws and redos; then guard newly opened due views before judging, repair provenance and reporting counts, and verify the failure paths and required preflight at no model cost.**

