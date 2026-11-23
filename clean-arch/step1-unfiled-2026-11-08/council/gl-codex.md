**NOT READY.** For example, the design would judge only whether a guarantee was signed while leaving its amount unanswered. The existing decision says those can be two questions; the proposed handling needs Alex’s decision before an engineer can build it.

1. **The earlier blocking items are only partly answered.**

   - **Item 1 — request and writer mapping:** The draft now supplies a request and mappings, but the contract is incomplete. It requires a date-shaped `due_day` even when `no_ladder` says to leave other fields empty, and does not specify the exact schema or how article IDs reach `created_from_input`. Two engineers could produce incompatible answers or writes. A complete fix needs the exact accepted shapes for both success and no-ladder, plus every writer input. [Design lines 153–173](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:153>); [store line 81](</Users/lchingen/hivemind/src/hivemind/views/store.py:81>).
   - **Item 2 — tables and checks:** Still incomplete, as detailed below. In particular, the earlier request to cover “failures before and after the first judgement” remains unanswered.
   - **Item 3 — first test:** Improved: it now reads every judgement and defines categories. It still cannot apply all its pass lines as written and can pass with an inadequate control. See finding 5.

2. **The choices and request introduce rules that are not settled.**

   C1(a) drops separately meaningful answers, whereas D38 explicitly calls for two views when an event and amount, or independently moving parts, are involved. The recommendation should name **splitting as the option favoured by D38** and explain the cost of departing from it. [Design lines 123–129](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:123>); [D38 lines 761–766](</Users/lchingen/hivemind/docs/DECISIONS-log.md:761>).

   C2 describes only half of D186: that decision also calls for outcomes against guidance. D368 places both halves in the next extraction version, not automatically in this separate step. Present that distinction and ask Alex how it applies here. [D186](</Users/lchingen/hivemind/docs/DECISIONS-log.md:2476>); [D368](</Users/lchingen/hivemind/docs/DECISIONS-log.md:3965>).

   The draft also adds substantive rules: estimate ranges without a reference; use the latest reported figure as an expectation; choose the “main” part; and use period end or an estimated publication day. These are not established by the cited production sentences. The obligation instruction covers **unsigned** obligations, while the proposed code applies the limit to every `binding_obligation`. The “unclear” company labels depart from D38’s company labels. Cite authority or put each behavioural change to Alex; reconcile the request and checks. [Request lines 5–20](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:5>); [design lines 138–144 and 180–194](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:138>). The examples do not name NVIDIA, but the guarantee example closely matches the Ohio test case and should be replaced with an unrelated example.

3. **Recovery and concurrent work cannot be built reliably from the state table.**

   [Lines 240–259](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:240>) do not specify transitions and dates for: a crash before archiving, during view/rung/map writes, after the view but before the sidecar, or during/after judgement; work still in flight when the run ends; corrected input; another writer; and two theses processed together. A later run with changed settings gets a new folder but also supposedly never resends an existing thesis; the source of that existing state is unspecified. The table says every date is an article day, but does not specify the date for each read/write or the expected publication date. Define atomic writes, ownership, resume keys, configuration identity, and each reachable state/event cell, including terminal and closed states.

4. **The reader and old-check tables omit real consumers and failures.**

   `lo` and `hi` also determine ladder direction in matching, and the full-text view is read by matching search; neither reader appears in §5.4. [Matching lines 72–80 and 146](</Users/lchingen/hivemind/src/hivemind/views/matching.py:72>); [store lines 325–332](</Users/lchingen/hivemind/src/hivemind/views/store.py:325>). The old quarterly-number check is explicitly **not rechecked**, so the new path does not meet it merely because these 34 cases lack quarterly questions. `settled_by` being present in a schema also does not prove it is nonblank, which `check_admission` requires. [Design lines 269–277](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:269>); [extraction lines 523–527 and 625–627](</Users/lchingen/hivemind/src/hivemind/extraction.py:523>). Enumerate all readers and writers, and state how each old check is met or intentionally changed.

5. **Both test stages have decision-rule defects.**

   - Stage A sends each fresh thesis **once**, yet requires a sound ladder in **two of three sends** for eight of ten. The fresh-set line is impossible as written. Its control also receives different instructions and output checks; specify equivalent treatment and how refusals and no-ladder answers enter each comparison. The 27/34 and 30/34 thresholds have no demonstrated basis. [Lines 288–309](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:288>).
   - Stage B’s “wherever confirmed equal, less one” can pass with zero comparable questions. It also permits an unsupported-rate pass while many theses are never judged. Set a nonzero comparable-control minimum and explicit coverage requirements; count omitted evidence, refusals, unjudged theses and incomplete draws against fixed denominators. Explain the basis for 10% and 30 judgements. [Lines 311–324](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:311>).
   - The fresh acceptance articles were previously read and assessed in the Step 1 acceptance; being outside the 243-item window alone does **not** prove their ten questions tuned nothing in this design. Document exposure and selection before calling them held out. [Acceptance log lines 1572–1608](</Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1572>).

6. **Factual checks: several claims are supported, but three are overstated.**

   I checked eight claims: the census output supports **729 answers, 36 ladders, 14 two-rung, 22 five-rung, and one bounds refusal**; the judge prints labels and conditions, truncates quotes at 400 characters, and stops after two refusals. [Census output](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.txt:1>); [judge](</Users/lchingen/hivemind/src/hivemind/views/judging.py:121>).

   Corrections:

   - Equal request hashes establish equality of **sorted canonical JSON**, not byte-identical requests sent to the model. [Census line 54](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.py:54>); [model line 240](</Users/lchingen/hivemind/src/hivemind/model.py:240>).
   - Appending rendered bounds does **not** ensure the model-written `state` text agrees with them. The omitted `band_problem` check exists precisely for a stated band that disagrees. [Design line 195](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:195>); [split line 416](</Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/split.py:416>).
   - The promised port of `ordered_ladder` cannot directly implement “unclear”: that function refuses an unclear favourable end for a numeric company ladder. [Split lines 443–460](</Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/split.py:443>).

A complete sentence-by-sentence source audit remains necessary after C1 and C2; the findings above identify substantive issues visible now and do not substitute for that pending audit.

