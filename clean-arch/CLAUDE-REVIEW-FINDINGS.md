# Claude review of the clean-architecture PRD and plan (2026-11-06)

Read-only review, requested by Alex through `CLAUDE-REVIEW-HANDOFF.md`. Nothing was edited and no model call was sent. Findings are leads,
not edits: check each against the cited source before acting, and send the product decisions (marked **Alex decides**) to Alex rather
than settling them in the PRD.

**Read:**
- `PRD.md`, in full;
- `reference-diagram.png`;
- Alex's 69 messages in Codex thread `01a1aeeb…`, quoted below as [n] in that thread's order;
- the code at the lines cited;
- read-only counts on the serving snapshot `poc/data/served-2026-10-28-v34-nvda-3m-through-0828/views.sqlite` and on `poc/data/e2e-v83-seed-d2/archive.sqlite`;
- `node clean-arch/render.mjs --check` passes.

**Not read:** `jev_matching.py` beyond what the PRD claims, the OpenAI pages the PRD cites, and the content of `architecture.html` (only its sync check was run).

## Most consequential

### 1. Step 3 keeps every repeat as a new record. Alex's words and his diagram say the opposite (**Alex decides**)

- **PRD §6** (the "Repeat" row) and **§9** save each repeat as a new evidence record, linked to the earlier one.
- **Alex [21]:** "if new evidence and evidence - great just add to db / if existing evidence and not dedup - add evidence to the thesis / else do nothing".
- **The diagram** labels this outcome "Dedup".
- **Codex's reply** (04:36) corrected this to "the current system keeps repeats". Alex's next message, "yeah that's a different thing" [22], does not agree to it: Codex's following line reads it as being about judgement. So the repeat row has no source in Alex's words (AGENTS, Authority).
- **What it costs:** in the serving snapshot, 2,023 of 4,298 evidence records (47%) are restatements (`same_claims`). That is the evidence growth Alex named as the problem in [10].
- **Options for Alex:**
  - (a) do nothing on a repeat;
  - (b) add the new source to the earlier record, and add a thesis link if the thesis differs;
  - (c) keep a new record linked as the same claim (the current behaviour).
- **Recommendation:** (b). The readers already count several sources per record: `service.evidence_record` returns `sources` and `outlets: len(sources)` (`src/hivemind/service.py:166-177`). Today each record has exactly one source (4,298 `evidence_sources` rows), so the store's shape already supports (b).

### 2. Pairs nested per thesis copy every multi-thesis statement, and the copies never meet

- **The shape** (PRD §12 schema): `pairs[].evidence[]` puts a statement under each thesis it informs, so a statement relevant to two theses is written twice.
- **How common that is:** in the snapshot, 1,918 of 4,298 records (45%) link to two or more theses. The split is 1,625 to two, 237 to three and 56 to four or five.
- **Why the copies never meet:**
  - §5 searches "the top-N related evidence attached to that thesis". Alex's words were "a search engine overlay on top of evidence db for a {thesis, evidence} to return the top-10 semantically relevant evidence" [18]; "attached to that thesis" is an addition.
  - §5 (line 135) and §9 also skip comparison for a new thesis.
  - So a statement already stored under thesis A, arriving again as evidence for a new thesis B, is never compared. It is saved as an independent fact.
- **Example:**
  - Article 1 files the CFO's "no H200 revenue in China" under "shipments and revenue".
  - Article 5 opens a new thesis "US licensing" and pairs a retelling of the same CFO line with it.
  - No search runs and no Jev call is made, so the ledger now holds two records for one statement.
- **Recommendations:**
  - **Representation (open in PRD §3; Codex can settle it).** Use a list-and-link shape:
    - `new_theses[]` with local ids `n1`, `n2` …;
    - `evidence[]`, each with `links[]` to supplied or local ids;
    - code refuses evidence with no link, a new thesis that no evidence cites, and a link that does not resolve.
    This keeps Alex's pairing rule [41] as a code contract instead of a nesting. It is also the shape the production writer already reads (`evidence.links`), which shrinks the §18 adapter.
  - **Search scope (Alex decides).** Search the entity's evidence with the thesis in the query, not as a filter. Run comparison for a new thesis's evidence too.

### 3. The Luna prompt has no "not evidence" rules, and its final check looks only for misses

- **Where:**
  - Lines 354–361 define evidence as anything that "supports, challenges or adds context", and add "Consider direct and indirect relevance".
  - The final check (lines 406–412) asks about evidence "missed or incorrectly linked" and about unsupported claims. Nothing asks what was kept that an analyst would not keep.
  - The only counterexamples are about theses.
- **The standard it drops** (Alex, D243, AGENTS §8): "这种典型的主张背景属于常识…除非带数字和具体的叙事不然都是属于不采纳" (typical background claims are common knowledge and are not kept unless they carry a number and a specific narrative); "不是什么事情都是惊弓之鸟需要抽取" (not everything needs to be extracted).
- **History:**
  - The evidence-bloat run was stopped and sealed for this reason (D206: "很严重", very serious).
  - The noise arms v53–v65 were all about this class.
  - With an empty library and "adds context", the first forward run will bloat.
- **Recommendation:**
  - Add the standard's not-kept classes as a closed list with two or three cross-industry examples each: background an analyst following the company already knew; product or marketing description; restated history; generic industry commentary without a number.
  - Have the final check read the kept list back against them in the same call (AGENTS §6).
  - Keep D240's line that a missing amount or date alone is no reason to drop.

### 4. The thesis has no answerable shape, and the prompt asks for an explanation the schema cannot hold (**Alex decides the contract**)

- **The explanation has nowhere to go.**
  - Lines 296–298 ask the model to "Explain how its answer could matter to revenue, profitability, cash or credit risk…".
  - The thesis object (lines 456–465) has only `state`, `id` and `description`.
  - So the explanation is either lost or pushed into the description (AGENTS §6: the request never asks for what the schema cannot express).
- **The example fails the prompt's own bar.**
  - The illustrative new thesis (line 518) is "How will acquiring the delivery-network operator affect the retailer's operations?".
  - No later evidence can settle it, so it fails the prompt's own counterexample at line 344 ("does not identify an outcome… later evidence can meaningfully inform").
  - An example is an instruction: this one teaches open-ended theses.
- **There is no scale bar.**
  - Alex's granularity rule (AGENTS §8): "a deal, product or project opens one only when its scale can change revenue, profit, cash or credit risk … 不要搜集一堆鸡毛蒜皮的事情" (don't collect a pile of trivia).
  - The E1 diagnosis (`docs/research/2026-11-06-e1-no-home-drops/`) found 24 small matters that production had to park: an undisclosed investment, a partner integrating NVIDIA software, a gaming-card rumour, a share-price calculation and a capital-return policy.
  - With an empty library and no scale rule, each becomes a thesis.
- **Decision for Alex:** the minimum a thesis carries, before the first run, because every thesis the run opens inherits it. The proposal is:
  - (a) the question;
  - (b) what outcome would answer it;
  - (c) its horizon or period;
  - (d) the entity tag, assigned by code (finding 6);
  - and, as a separate choice tied to Step 4, whether outcome ranges are needed.
- **Recommendation:**
  - Add a `why_it_matters` field for new theses.
  - Add two or three "not a thesis" counterexamples drawn from small matters.
  - Replace the example's new thesis with one that has an answerable outcome.

### 5. The prompt does not carry E1's lesson: a thesis's own period is read as a fence

- **What E1 found** (2026-11-06, two blind readers): 12 of 17 agreed link misses were the question's own quantity in another period or quarter, or a variant of a tracked product. In the model's own account, it treated the question's period, population or named configuration as a boundary.
- **What the draft says:** "time when relevant" (line 375) and "A different date alone does not automatically make a new thesis" (line 382). Neither tells the model what to do.
- **Why it is worse in the pair design:** the same miss becomes either a silent omission or a duplicate thesis ("2027 capex" beside "capex this year").
- **Recommendation:**
  - State the rule with one example: an estimate of the same quantity for another period, population or variant goes to the existing thesis, unless an analyst would bet on it separately (AGENTS §8: "wordings, deadlines, milestones and periods of one bet are one question").
  - Show each open thesis's period as a typed field in the payload; today the payload carries only `{id, description}`.

### 6. Identity is half in the model's hands, and a new thesis gets no tag for the next lookup

- **The model echoes a description code already holds.** The schema requires an existing thesis's "Unchanged supplied description" (line 463). A paraphrase becomes a check failure, or silent drift.
- **`state` and `id` say the same thing twice and can disagree** (a "new" thesis with an id, or an "existing" one with null).
- **Nothing carries the entity.**
  - The diagram looks theses up by `{tags = company}`, but a new thesis carries no tag.
  - The INPUT bullet (line 284) "Company tags: identify the companies in scope" reads as a task.
  - The supplier example (lines 387–388) invites a thesis on a company that is not tagged.
- **Recommendation** (code owns identity, AGENTS §2):
  - An existing thesis returns its id only, and code fills in the description.
  - A new thesis gets a local id.
  - In the single-entity slice, code assigns the processed entity as the tag.
  - State what happens to another company's matter: evidence for a tagged thesis through a stated relation, or nothing.

### 7. Step 1 output fields that later steps need are untyped or missing (decide now, not in M3)

These fields are part of Luna's answer. Deciding them after the first run changes the request and makes that run's traces stale.

- **`statement_date` is a free string** (line 479). The writer's revision rule refuses any day that is not ISO (`writing.py:97`, `ISO_DAY`), and its late-statement check compares days as strings (`writing.py:244-245`).
  - **Example:** `"May"` makes every revision of that record "no stated day". It also passes the late check, because `"May" > "2026-…"` as text.
  - **Fix:** ISO `YYYY-MM-DD` or null, checked by code.
- **The tier is absent.** The writer's revision rule needs it: a view never revises a fact, and a third-party view revises only its own party (`writing.py:99-104`).
  - **Fix:** a closed set of four values with examples (AGENTS §6), which the draft's prose already half-describes.
- **There is no period field.** The writer stores `event_time`, and E1 (finding 5) needs the period to file statements correctly.

### 8. The plan blocks a cheap first run behind the production writer census

- **What the plan does:** M0 items 1 and 4 and the §18 map make a field-by-field census of the writer and readers a prerequisite of the first Step 1 run.
- **Why that is out of proportion:** the first run is cheap.
  - 243 stored extraction calls in `poc/data/e2e-v83-seed-d2/archive.sqlite` average 4,964 input and 1,207 output tokens, with a median of 12.5 s.
  - So 118 articles run one at a time take about 25 minutes and cost about $0.13 at gpt-6-luna's published rates ($0.10 / $0.50 per M tokens). This is an estimate from stored tokens.
- **Recommendations:**
  - Split M0.
    - **M0a, for the first run:** the request; the Luna fields from findings 4, 6 and 7; id assignment; failure handling (finding 10); and a fake-answer check through the runner.
    - **M0b, moved to M3:** the writer and reader census and the adapter.
  - **Test library:** use the existing store schema on a fresh empty SQLite instead of an ad-hoc library.
    - `views`, `evidence`, `evidence_links` and `evidence_sources` have no NOT NULL constraints (`store.py:15-22`), and `store.add_evidence`, `add_source` and `link` exist (`store.py:340-353`).
    - This exercises the M3 path from day one, as Alex asked: "I want the system to work" [65]; "the evidence and thesis db is just the one that we are using now" [33].
  - **Name the first run:**
    - NVDA;
    - an empty library, consistent with D370's no-seed default;
    - the 118 golden-v5 development articles (July 1–14), in replay order, all of which resolve locally.
    - The gold's entries can serve as a checklist of misses in the review, not as a gate [53].

### 9. The evaluation has no pass line or review sheet (**Alex decides the pass line**)

- **The gap:**
  - The diagram has "Eval pass criteria".
  - PRD §8 (line 187) and M1 (line 753) leave acceptance open.
  - The review question "Does Step 1 produce useful pairs?" is not a test (AGENTS §7.3).
- **Recommendation:**
  - Fix a per-article review sheet before the run. Its columns:
    - missed matter, with its quote;
    - kept noise;
    - wrong link;
    - duplicate thesis opened;
    - thesis not worth tracking;
    - attribution or date error.
  - Have it read by someone who did not write the prompt (AGENTS §7.1).
  - Ask Alex for the pass line, for example: no duplicate thesis, and at most N noise items per article.

### 10. What happens when a check fails is undefined

- **The gap:** §12 (line 495) lists the checks: the id is in the list, the passage comes from the item, a new thesis has a null id. It says their behaviour is "not implemented by this document".
- **Recommendation:** define it before the runner.
  - A pair that fails a check is dropped with its reason and kept in the trace, where the review reads it (D209).
  - An answer that fails the schema is recorded as a failed item, and the library stays unchanged.
  - No silent repair.

## Accuracy of the PRD's code claims

**Checked and correct:**
- production schema keys and evidence fields (`extraction.py:73-88`, `new_groups` added at `extraction.py:149-150`);
- the extractor refuses any other prompt version (`extraction.py:46`, `require_supported`);
- `shown_views` reads the theses open at the start of the item's day (`extraction.py:42-51`);
- evidence ranking is by word overlap within one thesis, top N (`views/matching.py:108-113`);
- `search.py` indexes theses only (`search.py:1-7, 86`);
- a repeat is stored as its own record plus a `same_claims` row (`writing.py:233-235`);
- the revision check reads tier and original day (`writing.py:89-104, 244-258`);
- snapshot counts: 68 theses, 4,298 evidence records, 6,578 links, 2,023 repeat relations, 121 revisions;
- source database: 34,084 records, 6,874 with `feed = 1`, dated 2026-02-25 to 2026-10-26;
- the replay default is `poc-v118` (`scripts/replay.py:59`, README line 83). AGENTS still says v116; that is stale, and out of this review's scope.

**Understated:** §14's reader finding.
- `bundle.py:70-73` and `service.py:173,187` read only `replacements`, which has 0 rows in the snapshot.
- The 2,023 same-claim relations and 121 revisions are read only by `store.evidence_in_force` (`store.py:412-425`), the record builder the judge uses (`judging.py:45`).
- So the API and the UI show none of these relations, not just the two inspected cases.
- The fix belongs in M3.

## Smaller points

- **Top N:** Alex said top-10 [18]. Record it as the starting N; §5 and §10 say N is not chosen.
- **The diagram's "relevant evidence" label:** the diagram's Step 1 input reads "open thesis and relevant evidence"; the PRD drops the evidence. Cite Alex [10] and [12] ("without the need to read the full evidence in pre-promt") as the clarification. The README says the PRD states such clarifications.
- **Two examples teach the wrong output:**
  - The example `relevance` "The forecast informs the sales-growth thesis" (line 514) is a tautology, and it teaches empty relevance.
  - The example's `reporting_speaker: "Example publisher"` contradicts lines 401–402 (the publisher comes from metadata).
- **Jev draft (§13):**
  - "Express uncertainty" has no output field.
  - The party and tier rule the writer enforces (`writing.py:89-104`) is not in the instruction, so Jev can answer REVISION and the writer then refuses it. Decide whether that rule lives in Jev's prompt or stays a code check.
- **Docs check coupling:** `docs/check.py` now also runs `clean-arch/render.mjs`, uncommitted on `clean-arch`. This ties the old repository's documents check to the new folder; keep it only if intended.

## Decisions for Alex, in one list

1. **Repeats:** do nothing, add the source to the earlier record, or keep a new linked record (finding 1). Recommendation: add the source.
2. **Minimum thesis contract:** question, answering outcome, horizon, entity tag; and whether outcome ranges are needed (finding 4).
3. **Luna's typed fields:** whether Luna returns the tier, an ISO statement date and a period (finding 7). Recommendation: yes.
4. **Search scope:** filtered by thesis, or the entity's evidence with the thesis in the query (finding 2). Recommendation: the entity's evidence.
5. **Pass line** for the Step 1 forward run (finding 9).

Codex can settle the rest:
- the list-and-link representation;
- check-failure handling;
- returning an id only for an existing thesis;
- the prompt's not-kept list, scale bar and period rule, written from the standard and audited.
