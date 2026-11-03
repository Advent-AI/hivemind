The 19 answers contain substantive errors and evidence-use problems, but this stopped run cannot establish overall improvement. For example, both NVIDIA treatment answers acknowledge unknown signing status elsewhere, yet call the credit support “unsigned” in their admission reasons.

I read all 19 complete answers beside all eight complete control payloads, including G05’s 16 historical records and G09’s 34. Six payloads contain full articles; G05/G09 contain the supplied historical records, without full articles. The control and treatment user payloads are identical. I used the frozen [scoring.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/scoring.md) and [design.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/design.md), without changing their criteria.

1. **NVIDIA: unsupported credit-support claims remain, with different forms in the two arms.**

   In [nvidia-control-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nvidia-control-1-answer.json:42), `independent_judgement` says:

   > “it also puts NVIDIA's balance sheet and revenue quality at risk through credit support to capital-hungry AI clouds”

   This assigns the credit exposure to NVIDIA without establishing who provides it. The surrounding uncertainty concerns its size, not the provider. The question also assumes “financing it provides,” but the declarative judgement—not the question alone—is the decisive error.

   In [nvidia-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nvidia-treatment-1-answer.json:42), `reason` says:

   > “may create a guarantee or financing commitment whose terms are unspecified and unsigned”

   Yet `new_information` says no “signing status” is given, and `independent_judgement` says:

   > “Current evidence does not establish any amount, obligation or revenue effect”

   This is an unsupported **local characterization of signing status inside an otherwise conditional answer**. It is not an unqualified whole-answer assertion that NVIDIA has guaranteed the financing.

   In [nvidia-treatment-2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nvidia-treatment-2-answer.json:42), the admission reason is more definite:

   > “credit support extended to AI clouds, unsigned and unquantified”

   Elsewhere it explicitly says contract signing status is unstated and describes exposure conditionally. Again, the answer contradicts itself; the careful passages do not erase the unsupported admission premise.

   **Count:** definite provider attribution in control **1/2**; unsupported “unsigned” characterization in treatment **2/2**. These are different defects, not interchangeable scores.

2. **NVIDIA treatment 2 invents an unknown builder; both treatment proposals have admission problems.**

   Treatment 2 calls the Firmus project:

   > “a forward plan by an unspecified party”

   and later:

   > “a forward plan by an unnamed build party”

   The source explicitly says:

   > “Firmus is building a DSX AI factory campus in Batam, Indonesia.”

   The full article also quotes Firmus co-CEO Tim Rosenfield saying:

   > “Firmus AI cloud is building a NVIDIA DSX-aligned AI factory”

   Treatment 2 itself names Firmus earlier. This is a **definite internal and source contradiction**, not merely a cautious statement about unconfirmed financing or completion.

   Both treatments use the unsupported unsigned-obligation characterization to justify admission. Treatment 2 additionally invokes a “major business model milestone”; the frozen admission category is a **major product milestone**, not any business-model announcement. A possible exposure is a legitimate research lead, but these reasons do not establish the admission basis they claim.

   Treatment 1 also writes the nonexistent `arguments[0].question_id`:

   > `proposed_new_nvda_ai_cloud_credit_support_obligation`

   Its supplied catalog is empty. This is the recorded structural failure that stopped new sends. The announcement itself remains useful under N1; proposing a question does not add a separate evidence-use gain.

3. **G05: both answers falsely establish a shared WSJ origin for old evidence.**

   [history_repeat-control-1](/Users/lchingen/hivemind-extraction-quality-2026-10-29-prompt-restructure/history_repeat-control-1-answer.json:42) — corrected file link below — says independence is false because the incoming record:

   > “merely relays the WSJ report already in the record”

   [history_repeat-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/history_repeat-treatment-1-answer.json:37) is explicit:

   > “the same origin already captured in e717 and e719”

   The full input does not establish this:

   - `e717.original_who` is empty; its speaker is “Khac Phu Nguyen, GuruFocus.”
   - `e719.original_who` is empty; its speaker is “NVIDIA, as reported by Al Jazeera.”
   - Incoming explicitly attributes its report to WSJ.
   - `e761` explicitly attributes its **different, broader $600 billion** report to WSJ.

   Identifying the same substantive financing claim—especially `e717`—does not establish identical information origins. `independent_sources: false` is defensible because independence is unestablished; the asserted shared-origin explanation is not.

   **Count: 2/2 G05 answers.** The [control answer](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/history_repeat-control-1-answer.json:42) and treatment both preserve discussion rather than signed status, avoid a new question, and do not treat $350 billion and $600 billion as revisions.

   Two qualifications matter:

   - Treatment’s “incoming relay reinforces” is counterbalanced by “rather than strengthened.” I do **not** count definite confidence inflation.
   - Both carry forward the `e763` nonbinding-MOU caution. Its history concerns remarks following earlier reports, not an established description of the current $350 billion terms. That caution should not be read as a verified current-deal status; the old supplied judgement already contains this ambiguity.

4. **NN: all three preserve the quantities, but their reasons under-use the supplier evidence.**

   All retain **47 machine centers, 100% presold capacity, and the $80–90 million 2026 target**, without converting the target into realized NVIDIA revenue.

   The problem is their justification:

   - [nn-control-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nn-control-1-answer.json:42): “NN is outside the NVDA research scope.”
   - [nn-control-2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nn-control-2-answer.json:42): “no decision on the NVDA position is implicated by the text alone.”
   - [nn-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/nn-treatment-1-answer.json:42): the supply-chain signal is conditioned on “if NVIDIA is confirmed as a customer for the Wuxi capacity.”

   The source already describes production **for NVIDIA AI data-center racks**. It supports a reported supplier-capacity lead without proving NVIDIA is NN’s direct purchaser. Treatment recognizes a conditional signal, but unnecessarily makes that usefulness depend on a direct-customer confirmation.

   This is **under-use, not deletion**, and does not mean a new question was required.

   Separately, control 2 mentions `original_day` being blank but drops the source’s useful **“late June 2026”** timing. The other two preserve it. That is a definite time omission in **1/3** NN answers.

5. **Cloud and AMD: distinguish retained evidence from reasons that discount it.**

   [cloud-control-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/cloud-control-1-answer.json:42) retains all target figures but says:

   > “It does not bear on NVDA's revenue, guidance or AI-demand questions”

   The article explicitly identifies Alphabet as a NVIDIA customer and discusses AI demand. No purchase amount can be inferred, but dismissing even AI-demand relevance is unsupported under-use.

   [cloud-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/cloud-treatment-1-answer.json:42) preserves the figures and explains the limited customer-demand channel. It does not turn backlog into NVIDIA orders, claim to have read an Alphabet filing, or invent a table inconsistency. Its background treatment is acceptable. The changed independence Boolean alone is not evidence of improvement or independent corroboration.

   [amd-control-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/amd-control-1-answer.json:42) accurately retains both modeled comparisons but dismisses them as:

   > “a narrative contest with no investment decision attached”

   The full source explicitly connects competing performance measures to enterprise adoption and capital allocation. That competitive use is being discounted.

   [amd-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/amd-treatment-1-answer.json:42) explains a conditional competitive view, then says:

   > “that view needs independent benchmarks or NVDA-side data to be supported”

   **Uncertain under-use:** stronger performance conclusions need verification, but the supplied vendor claim already supports studying competitive positioning. The answer never claims actual AMD superiority.

   Both AMD answers omit useful full-article context about **x86 software incumbency** and NVIDIA’s **integrated-system/co-design counterargument**. These are contextual omissions, not failures to retain the frozen 2.4×/3.3× target unit.

6. **Corning: core content survives; treatment has qualified under-use and attribution concerns.**

   Both preserve “probably double” over “the coming years,” without changing *size* into revenue or inventing an endpoint. Both retain the partnership and capacity context.

   [corning-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/corning-treatment-1-answer.json:42) first calls the projects supply-chain leads, then says:

   > “These could become a supply-capacity lead … if NVIDIA or Corning later discloses binding terms, volumes or timing”

   **Uncertain under-use:** the first passage accepts their current limited usefulness; the second appears to withhold it.

   Its claim that the partnership/Wistron items lack a “primary NVIDIA or partner source in the text” also needs qualification. The article contains Weeks discussing partnering with Jensen Huang and quotes Wistron chairman Simon Lin. Those statements do not independently prove every reported project quantity, but named partner voices are present.

   I do not count background classification, missing binding terms, or the decision against a new question as errors.

7. **G09 and Singapore do not show the major failures the review was guarding against.**

   Both G09 answers preserve NVIDIA’s assurance alongside the reported delays. Neither deletes the historical reports, declares the technical dispute settled, or fabricates a FY2027 revenue effect.

   [history_denial-treatment-1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-prompt-restructure/history_denial-treatment-1-answer.json:42) expressly says:

   > “it cannot confirm or deny the SemiAnalysis delay report in specific terms”

   Its `opposes` links include `e50`, the PCB-manufacturing mechanism, as well as `e49`, `e51`, and `e53`. A roadmap can remain intact despite manufacturing problems. **The `e50` relation is therefore uncertain/overbroad**, but the surrounding prose prevents treating this as a definite assertion that NVIDIA disproved those problems. Not updating `v6` is acceptable.

   Both Singapore answers honor the explicit exclusion and preserve uncertainty about chips and destination. Treatment’s timing sentence—

   > “The statement dated to the article day … not confirmed as the statement day”

   —is confused and misses the article’s repeated **“yesterday”** cue. Because it expressly disclaims the statement date, I mark this **uncertain wording plus lost relative timing**, not a definite invented July 2 statement date.

For completeness, this is the disposition of **every received answer**. “Retained” assesses content, not its action label; absent follow-up is kept separate from factual error.

| Answer ID | Useful content | Bounded claims | Source/time | Follow-up |
|---|---|---|---|---|
| `nvidia-control-1` | N1 retained; N2 overclaimed | Unsupported NVIDIA exposure | Provider unestablished | Terms questioned; provider assumed |
| `nvidia-control-2` | N1 retained; N2 only briefly retained | Bounded | No material error found | No concrete N2 check |
| `nvidia-treatment-1` | N1 retained; N2 conditional lead | Unsupported unsigned label; admission/ID defects | Signing-status contradiction | Filings/contracts identified |
| `nvidia-treatment-2` | N1 retained; N2 conditional lead | Unsupported unsigned label; admission defect | False unnamed builder | Filings/contracts identified |
| `nn-control-1` | Figures retained; under-used | Target remains target | No material time error | No concrete ramp check |
| `nn-control-2` | Figures retained; under-used | Target remains target | Late-June timing omitted | None |
| `nn-treatment-1` | Figures retained; overly narrow use | No NVIDIA-revenue inflation | Timing retained | Customer check, too narrowly framed |
| `corning-control-1` | Core outlook/context retained | Size and uncertainty preserved | No new date error established | None explicit |
| `corning-treatment-1` | Retained; under-use uncertain | Forecasts remain forecasts | Attribution concern above | Terms/volumes/timing |
| `singapore-control-1` | Correctly excluded | Allegations remain uncertain | No material error found | Not required |
| `singapore-treatment-1` | Correctly excluded | Allegations remain uncertain | Relative timing lost; wording uncertain | Not required |
| `amd-control-1` | Comparisons retained; use discounted | Modeled/projected preserved | AMD→BofA attribution retained | None |
| `amd-treatment-1` | Retained; under-use uncertain | No actual-win claim | Relay chain retained | Materials/independent benchmarks |
| `cloud-control-1` | Figures retained; demand relevance wrongly denied | No NVIDIA-order conversion | Media attribution retained | Not required |
| `cloud-treatment-1` | Useful customer context retained | Properly bounded | No primary-filing claim | Not required |
| `history_repeat-control-1` | Repetition and preliminary status retained | No signed-status inflation | Unsupported shared WSJ origin | Existing limitations retained |
| `history_repeat-treatment-1` | Same claim retained | No definite confidence increase | Unsupported shared WSJ origin | Binding agreement/Ohio coverage |
| `history_denial-control-1` | Both accounts retained | No technical or revenue settlement | Broad opposition qualified | None explicit |
| `history_denial-treatment-1` | Both accounts retained | Specific uncertainty explicit | `e50` opposition uncertain | None explicit |

The frozen inherited-date caveat still applies to Manning, Weeks, and Capek; copied metadata is not a newly invented date or a verified event date.

The inventory is **48 planned, 19 received, 29 not sent**. No case has three samples per arm, so the registered stable-improvement comparison cannot be evaluated. These findings are source-relative model review, not human gold. No files were edited, no new model calls were made, and no outside modules were reviewed.