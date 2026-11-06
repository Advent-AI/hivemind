# Split POC: current library at each item

> **Scope update, 2026-11-05:** After the subject-filtered run omitted relevant questions, Alex chose the recommended all-open lookup. A and B now receive every question open immediately before the item. The earlier subject-and-theme restriction and pilot descriptions below are historical; the new scope is recorded in `all-open-context-design.md`. The stopped seven-day diagnostic has not been resumed and this change is not accepted production behavior.

Alex: “thesis needs to be clean to find what new perspectives not in the current system (with most recent 开题) fed to it”; later “if existing 题 then don't open; if not existing 题 open”; and “what are we testing ... connect ... real simulation”. The existing product's frozen v74i uses a day-start snapshot. This experiment tests a distinct, unaccepted configuration: both A and B receive the same latest committed open topics immediately before each item, in the corpus's owned dispatch sequence. It does not silently change production or compare day-start scores as if the input were identical. The articles' exact saved timestamps and historical starting-state limits remain visible; supplied corpus dispatch ordering is not proof of precise intraday event ordering.

Why: on Aug 29 A for seq 1211 could not see v72, opened by seq 1210, because A/B used the day-start library. The matching stage saw v72 but chose the same relation with confidence below its threshold and created v73. B also had no home for the $279bn statement because v72 was not shown to B. The user wants current research state. Rather than tuning thresholds on this example or assuming a `part_of` relation is directionally identical to `same`, use the latest committed library as model input. Whether the model correctly handles that input still requires direct testing; the context change does not guarantee correctness.

| State/event | Rule |
| --- | --- |
| Before first item | Real 08-28 snapshot; dispatch order, not a wall clock; no 08-29 data visible. |
| Before each later item | Read every currently open library question, including other companies and dynamically named subjects, at the last committed sequence. A and B receive the exact same immutable question list and article. |
| A and B | Two model calls in parallel for the same item. A carries its new viewpoint evidence; B links only existing IDs in that same snapshot. The metadata call only enriches optional fields. |
| Write succeeds | Actual matcher and writer commit before the following article's snapshot; no article-level speculative prefetch is valid across a changed library. |
| No new topic | A can pass while B writes evidence; the next item reads the resulting ledger. |
| Day boundary | Daily judgement uses written inputs; article after boundary sees all previous committed topics. Source publication day and input order are recorded. |
| Failure/crash | Save exact source, snapshot, original responses and archive. No fail is counted as pass, no silently fresh start. Recovery must verify identical input and code; in-flight requests are not assumed complete. |
| Other writer/config change | Isolated ledger, one writer, manifest pins runtime. A mismatch refuses reuse. |

| Value | Source and readers |
| --- | --- |
| Current question list | DB's last committed sequence; read by both model calls and matching. Includes dynamically named company topics even if upstream label uses a different identifier. |
| A/B requests and results | A/B prompts and actual source; exact request/response retained per item. No A/B answer is reused unless both source and full shown state match its original request. |
| Candidate and source evidence | A answer plus optional metadata; existing matcher/writer; full origin and proposed-check wording retained. |
| Evidence for existing topics | B output only names IDs in the shared snapshot; existing writer tracks actual destinations. |
| Optional date and ladder | Original article / A check text plus metadata model; absence does not gate opening. Date basis is retained. A known check day is not a confirmed resolution, and an unresolved newly opened question stays open. |

Actual product reader `extraction.shown_views` computes a day-start snapshot. The experiment must implement its own last-committed reader, reuse the actual historical row/state and grouping readers, and pass the exact same list into `round.run` for its matcher; production's default function remains unchanged. One writer means later extraction cannot begin until the preceding write completes. A/B still run in parallel; matching can use its existing parallel external calls. To resume without duplicates, dispatch's owned sequence and saved handover/write completion define where to restart; any uncertain in-flight call is preserved and visibly classified, not treated as empty.

Offline proof: begin with the 08-28 real ledger, write source-backed v72 via real matcher/writer with a fake Jev; immediately before the next same-day article, assert both A and B requests carry v72 and no future items; attach B evidence to v72 via actual matcher/writer. Repeat on the next day and on a dynamically named company question, and verify the actual read path, quote, links, and unresolved date/ladder. Mutant that reverts to day-start must fail. Then, on these two saved articles only, with preflight and unmodified A/B prompts, send the affected new requests and inspect all original articles, answers and matching decisions before a wider seven-day run. No equality between old and new inputs is claimed.

## Review corrections and bounded implementation

The 08-28 snapshot is only a historical diagnostic starting point: its source versions and pre-08-29 availability have not been fully established. It is not proof of a clean historical population. The corpus order is `publication_day`, source class (company, official, other), stored `published_at`, then rowid. It is reproducible, not verified real-world arrival chronology; 16 known later-version/time/comment cases remain excluded. The run manifest names these facts. Raw quotes at the top of this design are from Alex's actual current conversation and are also recorded in the user-visible thread; this experiment does not supersede the frozen default.

Both actual requests use the heading `[Open questions immediately before this item]`; B's system instruction uses `immediately before the item`, not day-start. A and B must carry the identical question IDs, with exact snapshot bytes persisted. Matching can additionally search the currently committed ledger; that wider search is recorded and is not falsely called the A/B snapshot.

| Interruption point | Recovery |
| --- | --- |
| Before route | No write; start the next unprocessed input. |
| After dispatch, before either model | Reuse the stored dispatch sequence and snapshot. If a request was not sent, send that request; do not invent an empty answer. |
| A or B returns | Preserve complete original provider response, request and archive. On resume independently reuse only a successful exact request plus response; any missing/in-flight call remains unfinished. |
| Metadata returns / before handover | Verify the metadata request and raw response bind to the exact same article and A output; reuse if identical. |
| Handover saved, match failed | `round.run` reads the saved handover and retries its recorded matching stage, never re-extracts silently. |
| Matching saved, before write | Use saved matching identities only when inputs and ledger state are unchanged; otherwise repeat the affected match as the existing `round` contract requires. |
| Writer committed, before progress status | Actual `dispatch.is_processed`/handover markers and the sequence, not the progress file, establish completion; do not repeat the write. |
| Daily judging partially committed | Reuse the original day sequence and actual judge's per-view completed markers; do not judge a view twice. Complete-day marker is authoritative. |
| Date/config/source/prompt or shown snapshot differs | Never reuse an old answer. Preserve the old run and label the new one separately. |

Dynamic research-subject identities and their names must be stored in the isolated ledger, reconstructed after restart, and not inferred from a title. For the POC's library context, show every open question in the configured scope to A and B, not only questions whose generated identity matches the upstream article tag. The input article's original object labels are not rewritten. Persisted subjects and replayed requests are independently checked.

Opening behavior needs both present and absent source-backed tests: if the meaningful topic was absent, A can open it; if already present, the next article should retain its relevant evidence without opening it again. An offline fixture can prove wiring only; the actual model's two behaviors need source-and-output reading and the real matcher/writer. Gold counts apply only to frozen-gold entries against the exact list actually shown; no all-new-topic precision follows from two gold articles.

## Source-backed pilot before the seven-day run

The user explicitly requested the seven-day test. First send A and B on the stored 2026-08-29 source `gnews:dbbde813240d4096829a72a9`, with the real pre-start ledger and the per-item subject-and-theme snapshot. If A opens a question, send only its metadata preparation request. This send determines whether the changed request and current output contracts work with the actual provider, whether the returned quotations and speaker/dates match the article, and whether the optional metadata is supported. The $0 replay cannot answer those questions. Save every wire request, provider response, answer, shown library and refusal. Review all returned material against the source before allowing the real matching/writing continuation. This one source is not a seven-day score or an acceptance of the model's semantics. Preserve the source-history and arrival-order caveats in the manifest; neither the frozen gold nor the earlier run is changed.

## Seven-day diagnostic launch

The user explicitly requested a seven-day run. Run the seven-day A/B, actual matching/writing and daily judging diagnostic after the source-backed pilot and offline recovery checks. It starts from the 68-question 2026-08-28 ledger, orders the 470 selected feed records by the documented corpus ordering and excludes the 16 known problematic records. Each item uses the preceding committed library, with its configured subject questions and all themes. The prior ledger's true source availability and precise intraday feed ordering remain incompletely verified, and the frozen extraction gold covers only two articles in this window. Do not report a complete frozen-gold accuracy for all seven days.

The pilot opened v70 and wrote 20 pieces. Three existing questions were judged; v70 had no rung and was not judged. A combined one evidence passage with both management's outlook and the author's interpretation under one tier; B combined actual segment revenue and a future company guide under a fact tier. The judgement cited other existing records rather than those particular new records, so no effect from them is established. These are recorded semantic defects, not a passed quality claim. The pilot's final `research_context.Reader` expansion refused the four target questions because the complete payload was 1,931,225 bytes against a 1,000,000-byte limit. Two of 69 open questions individually exceed that limit (v2: 1,376,425 bytes, v10: 1,405,331 bytes); v6 and v70 individually fit. The seven-day runner does not exercise that reader. Its execution is therefore a diagnostic, not full product-path acceptance; the reader defect remains open. Same-source overlap remains visible for direct trace review, with no assumption that identical passages always contain the same claim.
