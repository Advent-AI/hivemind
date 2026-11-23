# Step 1 implementation council: proposed link correction

## Status

On 2026-11-06, Codex and Claude Code (`claude-fable-5-1`) reviewed the clean Step 1 contract, original source/output packets, existing implementation and prior experiments, and challenged each other's proposals over five rounds. A separate reader audited the final proposed wording against the assembled request and clean PRD without seeing the failure cases. Claude had access to previous experiment reports, so the council itself was not a blind evaluation. The exact handoffs, replies, and full candidate requests are in [the local council record](../poc/data/clean-step1-implementation-council-2026-11-06/). The candidate was subsequently sent in a six-article blind comparison; results are recorded in the PRD and run log. It was not adopted, and neither the canonical prompt nor production configuration has changed.

The council recommends **one small candidate for the first link-quality test**, not a claimed fix for all source-fidelity issues. The candidate clarifies an existing model decision; no extra model call is added to the product, no data structure changes, and code does not decide relevance. Source preparation, thesis links, summaries and citations remain separate issues under Alex's agreed order.

## The observed problem

Article 4's evidence about company-wide revenue is linked to a product-performance thesis even though the model's own explanation says that thesis is not informed. Article 27's cloud-gaming server expansion is linked to a TV-product thesis, while the explanation says it does not inform that thesis. These are stored model decisions, not links invented by the runner. Neither implies the fact should be discarded: the revenue trajectory can merit a new thesis under Alex's broad topic rule, and the cloud-gaming topic requires analyst judgment.

The current prompt already says to compare each idea, allows new theses, requires each evidence to inform its links and allows an empty result for an entire item. The cause of the contradictory model decisions is **not established**. Its item-level `NONE` instruction may be insufficiently explicit about individual ideas in a mixed article, but the two known cases could already have returned an empty item. The candidate is a falsifiable clarification, not a proven root-cause correction.

## Proposed model instruction

In an isolated copy of the request, replace this one existing system-prompt bullet:

```text
- NONE: If the item produces neither kind of pair, return both lists empty.
```

with the following bullet and separate unconditional sentence:

```text
- NONE: If an idea informs no open or proposed thesis and merits no new thesis, omit that idea. If no idea yields a pair, return both lists empty.

Do not link an idea to a thesis it does not inform.
```

The unconditional sentence is outside the `NONE` bullet: a useful idea might inform thesis A but not B, or merit a new thesis instead of a wrong existing link. The rest of the request remains unchanged, including source-backed context, contrary evidence, multiple valid thesis links, comparison of subject/scope and period, and meaningful new topics without a known financial impact. `inform` must retain the prompt's existing meaning: supports, challenges **or adds context**. There is no `links=[]` output and no new standalone evidence record.

| Decision for an idea | Output | State change in the current isolated runner |
| --- | --- | --- |
| Evidence informs one or more open or newly proposed theses | One evidence record with the valid links | Existing thesis unchanged; a new thesis is added only when its evidence link resolves. |
| No thesis covers it, but it merits tracking | Proposed new thesis and supporting evidence | The new thesis enters the isolated state with its linked evidence. |
| No thesis is informed and a new topic is not warranted | No pair for that idea | No thesis added for that idea; the article and raw answer remain available for review. |
| Other ideas are relevant | Their pairs are still returned | Their existing or new thesis handling is unchanged. |

The independent request reader found no material new conflict with the clean PRD, but flagged practical risks: Luna may interpret `inform` too narrowly, lose a defensible indirect link, skip a worthwhile new topic, or misapply the sentence. These are reasons to test, not reasons to use a hard-coded rule. The historical frozen opening standard and Alex's broader clean-design opening rule are not identical; no change to the historical standard is implied. The replacement is 199 characters versus 75 (+124); on the saved request the full system prompt is 2,727 versus 2,697 `o200k_base` tokens (+30). This growth makes the per-idea decision and unconditional link instruction visible for the experiment; the current request already implies much of it, so a model benefit remains uncertain.

## Concrete implementation and checks

1. **Reuse the existing isolated probe.** Adapt [the existing setting-comparison harness](../poc/data/clean-step1-review-consensus/link_setting_probe.py) and blind-packet builder in a new local experiment folder. Read the six archived requests and before-states for articles 4, 27, 10, 14, 41 and 34. Use the existing model transport and schema validator. The harness must replace the old bullet only when it occurs exactly once, preserve all other request bytes and key order, and record the full control and candidate requests and their hashes. It must not write thesis state or any production database.
2. **Use the real unchanged request as control.** On the same day, send the unchanged request and the candidate under the same model, reasoning setting, source text, open-thesis list and output schema. Three draws for each of six selected articles gives 36 calls. Keep the execution order, raw answers, failed calls and exact before-states; a failed call is not silently retried or omitted. These are known cases with source and chronology limitations, not a representative sample or a chronological forward replay.
3. **Review entire articles and answers blind.** Check whether a wrong link remains, and what happened to the underlying useful fact: linked correctly, used to open a worthy new thesis, or omitted. Preserve relevant indirect context, counterevidence, different periods, multiple links and multiple pieces of evidence for a newly proposed thesis. Article 10's financing/demand links and roadmap counterevidence, article 14's new topic, article 41's defensible roadmap context, and article 34's opposing views are controls. Read source contamination separately from model error. Report all draws and meaningful losses; three draws cannot establish a general error rate or prove perfect behavior.
4. **Use unseen material separately.** If the known-case comparison is informative, preselect additional previously unreviewed source items and freeze a realistic existing-thesis state before reading answers; compare against the same-day control. Do not count these as a new stateful forward run. After a promising result, a separate ordered replay must verify evolving thesis state, missing facts and source quality together.
5. **Update the actual PRD prompt only after evidence supports the change.** The canonical prompt and schema remain in `PRD.md`, from which `runner.draft()` reads them. If the candidate is adopted, edit that one bullet there, regenerate HTML, rerun the Step 1 tests and record results. No duplicate canonical prompt, new runtime contract version or frozen-production change is necessary.

As a no-model preflight, six control requests were compared byte-for-byte after JSON serialization with their completed original trace requests; all six saved provider answers passed the existing schema and `runner.validate()` checks. The candidate requests change only the one prompt span. Those checks show that the files and contract fit; they do **not** measure source fidelity or model judgment. The later 36-call comparison did not establish a reliable fix; see the PRD and run log.

## Other issues the link candidate does not resolve

- **Source preparation:** The original Firmus input included unrelated recommendations; the prepared-source path restores archived text and preserves source-selection provenance but currently uses previously recorded model role selections. It is not yet an integrated or proven live source service. Incomplete captured pages remain incomplete.
- **Summary and citation faithfulness:** Correct source passages can accompany a wrong summary, a reversed link explanation, or an uncited condition. Quote-first output order and a clearer summary definition are separate hypotheses, not validated solutions. Test either separately only after the first link comparison; keep coverage, attribution, uncertainty and useful indirect analysis as controls. The failed extra-review call is not adopted.
- **Storage compatibility:** Clean Step 1 returns multiple source passages. The existing production writer has one `quote` and one `one_line`, and production Jev reads truncated quote text. The multi-passage mapping and clean downstream readers remain to be designed and tested; do not silently concatenate, drop passages or claim compatibility.

## Council result and limits

The initial Claude proposal introduced unpaired evidence and a numeric semantic detector. Both were withdrawn because they conflict with Alex's decisions and would introduce brittle rules. A later proposal was also withdrawn because a universal causal-path requirement could lose legitimate context and delete the existing scope/time instruction. The final proposal is deliberately narrower. An independent audit caught a conditional-scope ambiguity; the unconditional sentence above addresses that ambiguity, but neither review establishes model efficacy.

The 49-item/160-record source-fidelity review agreed in the earlier council is still incomplete. The six-case link comparison is a small, targeted implementation diagnostic, not a substitute for reviewing the broader stored trace or for production acceptance. All subsequent recommendations depend on what the source-backed results actually show.
