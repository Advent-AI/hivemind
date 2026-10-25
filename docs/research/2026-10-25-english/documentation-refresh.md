# D163 documentation refresh

Status: reasoning refresh and read-only translation review completed; final mechanical results are recorded below. Runtime language migration remains separate and incomplete.

## D22 module pass

The pass follows PRD order 01→02→03→04→05→06→07→08→09→00. For each module: assess language-change impact, compare page and PRD, read its example, and preserve acceptance/open questions unless an existing decision says otherwise.

| Module | Reasoning result |
|---|---|
| Research universe | English subject kinds and theme names retain category IDs, versioning, unresolved-versus-outside-universe distinction and manual maintenance. The per-subject reference list remains separate from upstream scope. Examples still route company and tariff material through their original categories. Eleven list separators were changed to English punctuation in the owner. |
| Classification | All sixteen categories and lookup tables retain their IDs and decision order. Whole releases, source attribution, explicit replacements, New York/SEC publication-day rules, typed subject identifiers and the personal-memo exception remain. The phrase “views to track” was corrected to candidate theses in the category owner; its generated PRD follows it. Frozen simulation shortcomings stay recorded, not repaired here. |
| Config | Versioned human settings, checksum, per-category prompts and separate matching/rejudgement settings remain. No budgets or concurrency settings are introduced. Candidate translations do not overwrite old prompt versions or silently change runtime defaults. |
| Dispatch | Completeness→prior completion→classification order remains. No subject filter, wall-clock ordering or second classifier appears. Explicit updates retain new IDs; incomplete work resumes rather than becoming a completed skip. |
| Extraction | The shared five-block contract, read-only full-item analysis, quote/number checks, evidence links, memo exception and D149 association requirement remain. The default implementation gap is explicit. The category T8 “author's view” wording was changed to “author's opinions” so it cannot be mistaken for a stored thesis. |
| Thesis library | Question/ladder/due-date identity, five/binary ladders, asset sentiment versus theme outcomes, evidence tiers, source independence, dependencies, succession, matching order, append-only history and first/repeated judgements retain their meanings. D155 identity is bounded; D149 group membership is not a dependency or overarching thesis. Existing and proposed behavior remain separated. |
| Final verdict | Earlier triggers, premises and confirmation/falsification rules remain visibly obsolete. The decided due-date freeze is distinguished from the still-open question of a separate final-verdict step. Translation does not revive old acceptance rules. |
| Pull mode | It alone acts on supplied time. The decided schedule/freeze behavior remains; actual-outcome verification, pending-publication handling and daily duplicate consolidation remain open proposals. |
| Human review pool | Intake distinctions remain: invalid lookup data, unknown identifiers, proposed themes, repeated failures and incomplete input; resolvable out-of-universe assets do not enter. Output/ownership remains deferred. The reference list does not become a new approval queue. |
| System overview | Data flow and glossary use thesis, subject, focus, state, conclusion, source reference, research group and dependency consistently. The overview distinguishes D149 requirements from unimplemented default grouping. No new system state or source of evidence is introduced. |

## Current operational documents

- The pipeline and grouping plans now lead with the actual D162 failure and D163 task. Superseded “next run” instructions are retained in dated source snapshots, not active work orders. Step B's identity/atomicity contract, sample counts, costs and limitations remain available in English.
- The service document distinguishes the shared thesis ledger from user ideas/commitments. It no longer claims that a thesis database stores no theses. The read service and separate two-call Idea application are distinguished.
- The Idea document describes the adopted `idea-v7` full contract and real response shape, rather than leading with the retired one-call route. Per-part reasons, causes-or-consequences driver definition, three-driver cap, market-claim guard, graph source and known measurements remain. Original experiments are linked without promoting them.
- The UI design and package guide describe the existing component contract, dates, explicit edges and ownership in English. Runtime adapter changes remain pending.
- Experience pages are English editions of unapproved proposals. They do not override the system glossary, create a company-question quota, revive a five-rung-only assumption or authorise trading. The original drafts remain linked. Their outcome-verification proposal and inconsistent notification timing remain explicitly undecided.
- CURRENT_STATE now separates current work, adopted paths, open defects and the one next task. The previous large chronological log is preserved in a dated snapshot, with unresolved defects retained in the current page.

## Verification boundaries

`verify_english_docs.py` checks the 30 declared current files, missing/empty-file controls, exact historical exceptions and five scratch code mutants. These disable CJK detection, each of three restored terminology rules, or historical-anchor rendering. All fail their decisive assertion. This does not measure runtime English output.

The browser rejected the local-file URL under its protocol policy. No HTTP proxy, alternate browser surface or raw browser-control workaround was attempted. Generated HTML and renderer checks are available; visual browser verification is not complete.

Historical source documents, original articles, model archives, frozen prompt versions and old decision entries retain their original language. Their continued Chinese text is deliberate and outside the 30 current-file coverage measurement.

## Read-only review and measured results

The second read-only review (`translation-review.txt`) inspected PRDs 00–09, all five current page-data files against the original saved strings/HEAD, the corrected prompt candidates, and language/anchor checks. It found no further material prompt or page translation drift. It found one checker regression: three previously rejected concepts lacked English rules. Reading the original `HEAD:docs/check.py` confirmed this. The English checker now rejects premise, verification/confirmation/falsification conditions, and a thesis described as confirmed/falsified in current specification prose. Historical-draft exclusions remain. Evidence that an official confirmed an event still passes; the rule does not prohibit ordinary source attribution.

Twenty rejected/corrected terminology-control pairs pass. The three additional scratch mutants each remove one restored rule and fail their corresponding assertion. Sixty-four Markdown link targets exist. The full Python suite passed 227 tests in 16.16 seconds, run from a temporary working directory so legacy tests did not write into the repository. This suite result is a code regression result, not English-language model acceptance.

The judgement prompt uses the PRD's exact “historical only” label; the future English request builder must use the same label. Static prompt sizes after correction are recorded separately; complete-request sizes remain pending until builders are implemented.

The final mechanical output is retained in [docs-check-final.txt](docs-check-final.txt). It follows this reasoning refresh and regenerates the PRD bundle from the English source documents.
