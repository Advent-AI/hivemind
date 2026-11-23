Independent deep review, read-only: you are a council member reading cold. Do not edit any file. Repository: /Users/lchingen/hivemind,
branch clean-arch.

**Scope.** The D388 line in clean Step 1, the extraction step that opens research questions ("theses") and links evidence.

**Out of scope:**
- link clutter;
- other modules;
- any change to the frozen gold or ruler (AGENTS.md §7.1);
- the production configuration.

**Read first:**
- `AGENTS.md` §§1, 2, 6 and 7;
- the D388 record in `docs/DECISIONS-log.md` (search "## D388");
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§48–52.

**Then the primary material:**
- the arms `clean-arch/step1-unfiled-2026-11-08/arms/{c8,c10a,c10b,c11}-{system.txt,closing.txt,schema.json}`;
- the probe records `poc/data/clean-step1-unfiled-2026-11-08/probe-r13-c9*/records.json` (the c8 control and c9),
  `probe-r14-c10*/records.json` and `probe-r15-c11*/records.json`;
- the model's own accounts `probe-r14-c10/thesis-account.json` and `probe-r15-c11/thesis-account.json`;
- the blind verdicts `clean-arch/step1-unfiled-2026-11-08/council/bq-codex-{A,B}.md` and `cg-codex-C.md`;
- the cases and their expectations `clean-arch/step1-unfiled-2026-11-08/cases-c9.json`.

Read raw answers yourself (fields `new_theses`, `kept`, `company_impact`, `why_a_separate_bet`). Do not rely on the log's summaries.

**Answer, under 700 words:**
1. What is established, and what is not? Say which evidence carries each claim and where the log overstates.
2. Do the unrelated changes in arms that add a closing paragraph look like real side effects or noise, from the raw answers? These are
   dev-1 recast, the fresh-12 EU programme, and fresh-22's lost HBM-shipments thesis.
3. What is the right next lever, and why? Consider at least:
   - restoring the standard's words in c11;
   - moving the rule into §3 or the field;
   - a separate, focused call for this one judgment;
   - stopping.

   Weigh each against AGENTS §6 and §7.3: one pass versus a closing read-back; "when a fix keeps moving another class, the call is
   doing several jobs"; no case-fitted rules; a general hedge-fund prompt.
4. What is the single cheapest decisive next test, with its falsifiers and cost? Price from `hivemind.model.PRICES`; one c8-sized send
   is about $0.015.
5. Which process errors repeat across c9–c11, and what one rule would prevent each?

Hold no preferred conclusion. Stopping is a legitimate answer.
