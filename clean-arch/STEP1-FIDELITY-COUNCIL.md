# Step 1 source fidelity: Codex–Claude council

**Status: investigation and proposed next work; no tested fix has been found.** On 2026-11-07, Codex and Claude Code independently examined stored sources, raw answers, the clean request and existing downstream code, then challenged each other's conclusions over five rounds. The exact handoffs and replies are retained in the [council work area](../poc/data/clean-step1-fidelity-council-2026-11-07/). The Claude review was not blind to prior studies. No Luna extraction experiment, source-database write, prompt change or production change was made in this council.

## The problem in a concrete record

In one article about optical networking, the source quotes **Vishal Chandrasekar of Ayar Labs** making a 2028 forecast. The stored answer's source passage and `original_party` identify Chandrasekar, but its standalone summary says **Roy Kim of Lightmatter** made that forecast. The source passage was located successfully; the mistake was already in the model's raw answer. A reader relying on the summary can therefore learn a different speaker from the one in the quoted source. [Original answer and article](../poc/data/clean-step1-coverage-order-2026-11-06/review.html#article-41).

This is not the only kind of problem:

- **Meaning or direction can change.** A previous FEV answer correctly summarized a local system as backup for cloud models, while its thesis-link explanation reversed the direction. Additional citations cannot by themselves correct the reversed explanation.
- **A summary can be supported by the article but not by its attached passages.** The prior Firmus answer included a $2bn fundraising detail without citing the paragraph containing it; an FEV answer omitted the passage supporting a limited-connectivity condition.
- **Time has different roles.** A forecast's 2028 target is not automatically the day its author spoke. A contract's stated start, the reporting period for earnings and the publication date likewise need their source contexts preserved; their relationship to an original statement date can be uncertain.
- **The supplied article can itself be contaminated.** An earlier Firmus input included later unrelated recommendations. A quote can be an exact substring of that input and still belong to another story.

The issues can overlap in one record. A correct quote establishes that text appears in the supplied input; it does not establish that the summary, actor, time, conditions or thesis-link explanation are correct. The model's internal reasons remain unknown.

## What the saved comparisons actually show

The latest comparison contains **54 answers and 217 evidence records from nine selected articles**. Its answers are repeated draws, not 54 independent articles. In the six answers to the optical-networking article, one summary names the wrong executive, and two attribute the reporter's 72-to-576 processor plan to an executive whose adjacent quote discusses copper limits. In the six answers to another article, all put `since 2023` in a statement-date text field for a reported agreement that existed since 2023; whether that phrasing denotes an original action date or only an event period depends on the intended field and source context. These are specific trace observations, not a general error rate. The blind reviews contain other source-backed concerns and disagreements.

The older 49-article run produced 160 evidence items. Its articles and several important mistakes were reviewed, but the earlier proposed **complete, consistent record-by-record fidelity census is not finished**. Do not combine those 160 items with the 217 repeated-draw records as if they were independent observations or use either selected set as a population accuracy estimate.

## What has already been tried

| Prior attempt | Observed result | Boundary or regression |
|---|---|---|
| Locate and safely repair original quotations | The clean exploratory runner can preserve unmatched passages as unverified and continue the replay. | A located passage does not prove that the summary means the same thing or that the right person is named. |
| Move or clarify the final check | In the 84-call selected comparison, the Firmus missing citation improved in some arms. | FEV's connectivity condition and a named customer were lost in some answers; several answers assigned an unstated currency. No variant was adopted. |
| A second same-article citation review | It recovered the Firmus missing paragraph in three selected draws. | It missed the FEV condition and reversed relationship in all three; some evidence IDs were unaddressed. It is not an accepted runtime fix. |
| Source-first reading and a later linking step | On three previously used development articles, more of the selected facts were recovered. | Separate statements were merged because they shared a quote; source attribution, dates and routing still failed. The comparison changed multiple parts of the request. |
| Source mentions and time-role research | A research contract required original-text mentions for the claimant and time and could reject invented text in stored-data checks. A later small trial improved several selected attribution examples. | A real mention can still be assigned to the wrong claim or time role. The trial also lost cross-paragraph years and assumptions, and two of nine candidate answers failed quotation checks. The improvement cannot be attributed to any one change. |
| Evidence instructions moved earlier | One candidate answer recovered the known Kyber report and denial. | Other candidate answers still missed it and some introduced unsupported thesis links. The change was not adopted. |
| Quote before summary | The existing frozen production schema already places `quote` before `one_line`. | Older stored production answers still have attribution errors. Reordering clean fields is an untested hypothesis, not a demonstrated fix or established cause. |

The historical source-reading module described in the research notes is not present in the current checkout. Its documented contracts and results are useful references; they are not a verified drop-in implementation.

## Agreed design direction

The system needs to keep these relationships understandable for **each retained evidence matter**:

1. What the source actually states, with all passages needed for its actor, conditions and context.
2. Who made each material claim, distinguishing an unnamed report, a company's response and the article author's own wording when that distinction matters.
3. What the text says about time: when a statement was made, the period an outcome or forecast covers, or an unknown date.
4. What the model adds as its explanation of how that matter informs an existing or new thesis; that explanation must not reverse or invent the source claim.
5. How the saved record and the eventual dossier reader preserve those elements together.

This does **not** require mechanically splitting every paragraph or every mixed record. The existing standard allows one matter to include a main claim and a qualified secondary detail; separate records may be appropriate when one set of source and time fields would obscure distinct claims. Conversely, two distinct statements may cite the same source passage. Quote equality or overlap is not evidence identity.

A larger claim-level source representation could make some relationships more explicit, but it is a **design candidate**, not a verified fix. A field containing a name or timestamp copied from the source still cannot prove that the name made the claim or that the timestamp has the right role. Do not add code that decides investment relevance, automatically treats textual matches as semantic truth, or stops an exploratory run on an arbitrary rule. Preserve the user's final thesis–evidence pairing and the full article context.

## Concrete next work and how it chooses a change

1. **Finish the stored-record review.** For each of the original 49 articles and 160 evidence records, compare the entire article and pre-item thesis state with each raw summary, its cited passages, original party, reporting speaker, date and period fields, and every link explanation. Record each material claim with its supporting passage, any changed meaning or unlocatable support, and whether the source is contaminated or incomplete. Track an article-level omission separately from an error in a returned record. Read the 54-answer comparison as a separate repeated-sample set, not as extra unique articles.
2. **Test the review against both errors and controls.** Use the Ayar/Lightmatter mismatch, the FEV reversed relation and missing condition, Firmus's incomplete citation, and known source contamination; also include correctly attributed statements, genuine relative dates, valid indirect links, and legitimately combined matters. A second reader checks the observations and unresolved interpretations against the source. Record definite errors, concerns and disagreements separately.
3. **Trace the actual consumer before claiming an integration outcome.** The isolated clean trace retains multiple passages, source/time fields and link explanations. The existing production evidence table stores a single `quote` and `one_line`; Jev and judging read truncated quote text. The writer currently stores an unknown original day as empty, while Jev's incoming comparison and the revision-order path can fall back to the article's publication day. The clean Step 3 adapter is not implemented: mapping a clean multi-passage output and link explanation to these legacy fields remains an open contract, not a loss already observed in clean production.
4. **Choose one candidate from the traced evidence and test only that change.** For example, a single field-description clarification about a statement date versus the period a forecast covers can be tested independently if the review supports it. A different test could move `source_passages` before `summary` in the clean output schema, preserving the rest of the request and the paired output. These are separate hypotheses; neither is a solution for all fidelity problems. Do not bundle them with new fields, automatic flags and mandatory splitting into one experiment.
5. **Compare complete outputs, not just the targeted field.** Reconstruct the same saved article, before-state and actual request wire order for control and candidate, resend the unchanged control on the same day, and independently review the responses without arm labels. Examine missed useful evidence, wrong or duplicate theses, links, speaker, uncertainty, conditions, dates and quote support as well as the targeted error. Preserve every raw response and failure; do not merge or vote across sampled answers. Include previously unseen, different-domain sources when available and accurately describe any corpus limitations. A changed result in a small sample is evidence to investigate, not proof of mechanism or universal improvement.

There is **no invented minimum number of articles** or automatic semantic gate. Prioritization considers the impact on an analyst's decision, observed scope, confidence in the mechanism and the cost of a change. A serious single trace can matter. If a genuine code defect is traced within the taken-up clean slice, fix and verify that defect at its owner; a model-meaning mistake is not automatically a code defect.

## Council corrections and remaining uncertainty

Claude initially proposed moving several fields, adding an original-party mention, changing time descriptions, forcing some multi-source cases into separate records, and adding automatic source/date flags in one candidate. After challenge, it withdrew the bundled recommendation, the mandatory split and the proposed textual-match flags. It also corrected evidence IDs and withdrew an unsupported broad date-error count and an arbitrary minimum-article threshold. In the final round both reviewers agreed that an ineffective small test does not prove the model misread an instruction, and that a small-sample regression must be checked rather than automatically attributed to a candidate.

The unresolved question is **which change, if any, makes the full source-backed record more reliable without losing useful evidence or creating wrong links**. The saved results do not yet establish this. The review and controlled comparison above are designed to find that out; neither model's agreement is evidence that a solution has passed.
