You are an independent, read-only reviewer for the Hivemind repository (/Users/lchingen/hivemind). Read AGENTS.md first; it governs.
Out of scope: Step 2–4 code, the frozen ruler's files, Ohio (D388–D391), any module other than clean Step 1. Do not edit anything.

Alex approved gate 1 of a combined Step 1 plan (D435 in docs/DECISIONS-log.md; the plan is
clean-arch/step1-diagnosis-2026-11-12/COMBINED-PLAN.md, version 4, section "Gate 1"). Before any send, a council read is required.
Please check, citing the files you read:

1. **G1-c stop.** clean-arch/step1-diagnosis-2026-11-12/gate1/PREREAD-RESULT.md says G1-c cannot fix its lines (two blind source
   readers agree on no second matter) and stops before any send. Read the two readers' files it names and the brief. Is the stop right
   under D435 and AGENTS §7.3? Is the summary of the readers accurate?
2. **G1-a and G1-b ready to send?**
   - Arms: clean-arch/step1-unfiled-2026-11-08/arms/c15yc-* (changes 1 and 2) and c15c-* (change 2 alone); diff each against c8-*.
   - Audit: clean-arch/step1-diagnosis-2026-11-12/PROMPT-AUDIT-c15.md (round 2 answers a blind reader's findings,
     council/lt-codex.md). Are the revised sentences sourced, general across companies, and free of new contradictions with the
     standard (docs/prd/05-extraction-standard.html) or c8's other sentences?
   - States: clean-arch/step1-diagnosis-2026-11-12/cases-gate1.json (g1a: the capex article step 42 in three stored draws; g1b: the
     positive, negative, single-customer and Gulf states). Do the states test what the plan's lines say?
   - Harness: clean-arch/step1-diagnosis-2026-11-12/probe_c14.py (now takes each arm's schema file; production's adapter; a byte check
     against the stored sent request; the runner's retry rule; responses kept on arrival). Any defect that would make a result wrong?
   - Lines: the plan's G1-a and G1-b rows. Are they fixed tightly enough to decide before the result is read?
3. Anything serious missing before these 42 sends (about $0.6).

Answer in plain English: the answer in the first line, then one example, then the points in this order. End with one line:
"G1-a and G1-b ready to send: yes" or "no".
