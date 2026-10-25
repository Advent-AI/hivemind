# English prompt review (D163)

Status: candidate text prepared; not configured or accepted. This review is a language and contract audit, not a new extraction experiment. The [migration plan](plan.md) holds compatibility prerequisites. The [system glossary](../../prd/00-system.md#glossary) owns definitions.

For example, a source author's opinion is a **third-party view**, but the question stored in Hivemind is a **thesis**. Translating both as “view” would erase a distinction the product uses.

## Baselines, not newest filenames

| Consumer | Adopted baseline | Review candidate | Configuration evidence |
|---|---|---|---|
| Extraction role | `role-v5.txt` | `role-v6.candidate.txt` | `poc/config/poc-v16.json` |
| Category blocks | `categories-v5.json` | `categories-v6.candidate.json` | Same extraction settings; all ten configured category entries inspected |
| Matching | `matching-v1.txt` | `matching-v2.candidate.txt` | `poc-v16` |
| Rejudgement | `judging-v2.txt` | `judging-v3.candidate.txt` | `poc-v16` |
| Idea decomposition and mapping | `idea-v7.txt` | `idea-v11.candidate.txt` | `poc/config/poc-v9.json`, the service's adopted full contract |

The files here are review artifacts, not runtime prompt versions. `idea-v10` is a different experimental contract requiring a causal clause; it is not the translation baseline. D160–D162 extraction roles and grouping paths are not adopted. Old configurations remain reproducible. An eventual new configuration must identify which adopted setting it replaces for each active entry point.

## Terminology correspondence

This table locates glossary concepts in the existing interface; it does not redefine them. Identifiers and field names remain stable even when their old spelling differs from current prose.

| PRD concept | Prompt wording | Existing fields/readers | Distinction to preserve |
|---|---|---|---|
| Thesis / candidate thesis | thesis / candidate thesis | `view_id`, `target_view_id`, `candidates`; extraction, matching, writing | A candidate is proposed, not already stored; `view` in an identifier is not a second product concept |
| Subject | subject; company or theme when specific | `object`, `object_id`, `object_kind`; universe and service | An asset thesis is not limited by definition to companies; this POC's implemented universe is narrower |
| Focus | focus, figure or event | `looks_at`; Idea part uses `looks_for` | Not an investment driver, research group or the numeric value itself |
| Asset / theme thesis | asset thesis / theme thesis | `kind`; ladder checks, writer, UI | Asset sentiment order versus theme outcome order; both permit binary ladders |
| Ladder / rung / state | ladder / rung / current rung judgement | `rungs`, `position`, `rung` | One-based rung position is not the displayed score and not automatically a truth claim |
| Conclusion | current rung and supporting reasons | judgement `rung`, `reasons`, `changed` | The reasons may change without changing rung |
| Evidence / source reference | evidence item / source | `evidence`, `quote`, `one_line`, `original_who`, `original_day`; source checks | A translated summary is separate from an exact original-language quote; a retelling is not independent corroboration |
| Evidence tier | fact, party statement, third-party view, rumour | canonical enum values in the migration plan | “Third-party view” names an opinion tier, not a stored thesis |
| Merge / succession | merge / succession, predecessor and successor | matching outcomes, `target_view_id`, successions | Same question versus next period; neither means research-group membership |
| Dependency | dependency | `dependencies`, `direction`, `wait_chain_view_id`, `wait_year` | A causal input to judgement; a group association is not a dependency |
| Research group | research group | D149 contract; absent from adopted extraction schema | Do not promise a field or capability absent from the running path |
| Research universe / reference list | universe / reference list | universe subjects versus per-subject `watch` entries | Universe controls supported subjects; the reference list does not veto new important topics |
| Open / closed | open / closed | view switches and matching checks | Lifecycle, not “active” versus “inactive” |
| Due date / period / publication day | each named explicitly | `due_day`, `year`, period bounds, item day | Different dates with different roles; do not substitute one for another |
| Repeat / replace / new evidence | schema outcome plus plain explanation | evidence matching and source/replacement records | A repeat adds a source; replacement keeps the old record; new evidence is a separate item |

## Complete-request audit

| Call | Read together | Information actually supplied | Checks and unresolved points |
|---|---|---|---|
| Extraction | Role, category `what`/`read`, `build_prompt`, `schema_for`, `sift`, fiscal note | Full item up to the existing length limit; metadata; subjects/themes; reference list; open theses and dependencies without scores/evidence | Generated English, immutable quotes/IDs, new enum schema and current checks must agree. Fiscal notes, retry text and dynamic headings also need translation. No grouping contract can be claimed while its fields/context are absent. |
| Matching, including second pass | Static prompt, `_user_text`, `build_lists`, `check`, identity and writer | Candidates and rungs; searched theses; existing context; evidence in force; no complete source | Preserve both passes. The old prompt permits near-date event merges that the key conflict check can override; this is the recorded D162 defect, not solved by translation. |
| Rejudgement | Static prompt, `build_prompt`, schema, `check_answer`, both retry paths | Evidence in force and replaced predecessors; dependency conclusions; previous conclusion for comparison | Only current evidence is citable; predecessor is context. The English text clarifies the baseline's contradictory phrase “replaced evidence” by describing what the builder actually supplies. Waiting/history labels must match builder output. |
| Idea decomposition | First prompt half, parts schema, dynamic subject catalogue and original idea | Covered subjects/counts and the user's idea | Preserve two-to-four parts and the existing dollar-claim interpretation. No causal-clause field from the unadopted experiment. |
| Idea mapping | Second prompt half, mapping schema, candidate briefs, code selecting/evaluating | Searched candidates with current judgements and selected context | Correct the false five-rung-only/bullish-first descriptions. Keep adopted direct/driver/context semantics, including causes **or consequences**, per-part reason and context limit. |

## Discrepancies and disposition

The census unit is the owning prompt clause or builder path, not occurrences of a word. All five baseline files and their builders above were read. Source-level findings below must not be called fixed merely because the candidate text is English.

| Finding | Instances in the adopted prompt set | Disposition |
|---|---|---|
| Idea describes every ladder as five-rung | One decomposition clause | Candidate now says five or two, as PRD 00/06 and current schema already require |
| Idea says rung 1 is universally most bullish | One mapping clause | Candidate distinguishes five-rung asset, theme and binary ladders |
| Idea calls the judged position “true” while later forbidding “true” | One opening clause conflicts with final mapping instruction | Candidate consistently says current judgement |
| Idea example equates NVDA FY2027 with calendar 2026 | One mapping example | Removed misleading equality; retain the existing fiscal-period coverage rule without inventing a new rule |
| Historical Chinese-only generation | One extraction clause; two Idea references to the library's language | New text requests English generated prose, keeping source quotations and IDs unchanged; removes an assumption about stored-language uniformity |
| Schema enums duplicated as prompt lists | Extraction measure/basis/unit/event lists and judgement push list | Allowed sets stay in schema; prose describes how to choose and interpret them. No enum is silently added or removed. |
| Replacement wording contradicts supplied data | One rejudgement clause | Describe the current item and the predecessor it replaced, matching `build_prompt`; no change to citation permissions |
| Missing personal-memo exception | Adopted role's mandatory initiating evidence and category T8's blanket opinion description | Pre-existing PRD D59 gap. Do not silently broaden scope while translating; record for the extraction work before claiming PRD-complete prompts. |
| Narrow opening policy and absent grouping | One adopted role policy; no group fields in adopted schema/context | Pre-existing D158/D149 implementation gaps. Candidate preserves adopted policy, not a claim that it fulfills the full PRD. |
| Event deadline identity promise differs from code | One matching clause versus keyed conflict path | Pre-existing D162 defect remains. No wording can establish that the writer accepts a merge it overrides. |

The last three rows block a claim that extraction is fully aligned with the PRD. They do not justify secretly changing its admission, identity or grouping behavior during language conversion. The current state must retain these defects.

## Size and review evidence

`prompt-size.json` records the static files before/after with local `o200k_base` counts. These are estimates, not billed usage or assembled-request counts. English spelling uses more characters than Chinese for four translated files, while each uses fewer estimated tokens. Explicitly removing repeated enum lists offsets some expansion. The already-English Idea prompt shrinks in both characters and tokens. No behavioral instruction was added simply to fill the larger character count.

| Pair | Characters before → after | Estimated tokens before → after |
|---|---:|---:|
| Role | 2,630 → 5,599 | 1,722 → 1,119 |
| Categories (whole JSON file) | 1,629 → 3,991 | 961 → 811 |
| Matching | 1,242 → 3,202 | 895 → 643 |
| Rejudgement | 622 → 1,678 | 471 → 322 |
| Idea | 2,844 → 2,632 | 633 → 558 |

These counts describe the first review candidates, before the corrections below. Recalculate after changes. Whole-request measurements and stored-answer compatibility replay remain required once the new builders and schema exist. A static text review cannot prove model behavior, and no fresh extraction/matching/judgement/Idea samples have been made for this language conversion.

## First read-only review disposition

`prompt-review.txt` found two material wording issues spanning three clauses. Each was verified against its cited source before editing:

1. The translated event paragraph omitted the explicit equality between the announced deadline and due date. `role-v5.txt` states it; extraction's date check does not enforce that equality. Restored “Use that date or deadline as the due date.” The undated-regulatory exception remains.
2. The role's fixed five-label order must qualify **five-rung** asset ladders, as both the baseline and `check_ladder` do. Added the qualifier. The Idea text must not assume all binary labels are Yes/No: PRD 06's kinds table also permits bullish/bearish labels, and `idea.judged` returns the actual label. Replaced the assumption with “binary ladders use their supplied labels.”

These were candidate-introduced defects caught before activation. They do not change the three pre-existing PRD gaps above. A follow-up read must inspect the corrected paragraphs and the full affected prompt, not count a green rerun as proof without reading it.

The follow-up review in `translation-review.txt` re-read both full affected candidates and found the corrections preserve the required meanings, with no additional material prompt drift. The judgement status label is aligned to the PRD's exact “historical only” wording; its new request builder must match. The follow-up's one finding concerned missing English glossary checks, now restored and tested as recorded in `documentation-refresh.md`. Candidate approval for wording is not runtime activation or semantic model acceptance.
