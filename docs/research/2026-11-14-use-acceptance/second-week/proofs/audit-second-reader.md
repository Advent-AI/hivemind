The request leaves two boundaries unclear: what counts as an event expectation, and which topic fields count as its wording. The packet also shows inconsistent reader marks, so not every failed mark is evidence of a prompt failure.

### A. Event references

The request says: “reference is what this figure or event is measured against,” and its kind is `expected` when the item states “a consensus, the company's guidance, the stated plan or deadline.” For figures only, a recent reported amount can be used; “Otherwise reference is null.” The schema says `expected` is “what the market expects.”

The form’s `XR` says the reference quotes “what the article states the market expects” and an event’s is null whenever the article states no expectation. `X` says an event presents as expected only what the article states. They use similar words, but neither defines whether a progress report, an older plan, or an expectation about a related measure counts as the event’s expectation.

| Article expectation | Careful reading of request; attempts |
|---|---|
| China **plans to allow** purchases | Quote required; 2 of 3 quoted. |
| Rubin **could begin shipping later this year** | Quote required for first shipments; across three topics, quoted in 2/3, 1/3 and 0/3. |
| Groq **volume shipments expected later this quarter** | Quote required; 2 of 3 quoted. |
| Kyber **slated for release/debut in 2027**, versus reported delay to 2028 | The stated plan is to be quoted, but whether release or debut is the same as first shipments is open. All attempts quoted; one used the 2028 delay. |
| Investigation **nearing a conclusion** | Open: progress suggests timing, but is not plainly a stated plan or deadline. All 12 attempts were null. |
| Rubin **20% of revenue**, ramp **could slip** | The 20% is a different measure; the ramp forecast’s status as the reference is open. One attempt was null and two quoted 20%. |

**Marks were not consistent.** The same investigation sentence and null reference held in two attempts in Alex’s reading but failed across July topics. The same Kyber debut quotation held and was left open. Questions differ, so the packet does not prove every difference is a reader error.

The judge does **not** see an event’s reference: `write_view` builds event conditions without it and returns no reference passage.

Verdicts: **misread** for the clear plans or shipment expectations omitted; **abstract** for the boundary cases, because the request gives categories but no example resolving them. **Not the prompt** also applies to inconsistent marks and the judge’s missing reference.

### B. Unlisted parts

Counts below are attempts listing each part, out of three; “declined” means no list was produced. Placement is based on the topic text; whether a detail is independently left out can depend on the individual question.

| Topic | Description beyond the question | Outcome-only parts |
|---|---|---|
| 1 | — | Paid/accrued; remaining term: **1/3 each** |
| 2 | Unconditional status: **3/3**, as adjustable/cancellable | — |
| 3 | — | Average prices; margins: **2/3 each** |
| 4 | Both years: **all declined** | Forecast comparisons: **all declined** |
| 5 | Final cost; regulatory conditions: **3/3 each** | — |
| 6 | — | China revenue resumption: **3/3** |
| 7 | Shortage cause/slip: **3/3** | Revenue share; sales timing: **3/3 each** |
| 8 | 25% loss coverage: **1/3** | Paid/accrued; terms/duration: **3/3 each** |
| 9 | Commercial scale: **3/3** | Revenue contribution; later slip: **3/3 each** |
| 10 | Earlier price comparison: **2/2 answered** | — |
| 11 | Signing: **1/3**; consideration/terms: **3/3** | Regulatory conditions: explicit **2/3** |
| 12 | Both years: **all declined** | Forecast comparisons: **all declined** |
| 13 | Funding versus outstanding: funding **1/1 answered** | Changed commitments: **1/1 answered** |

The request says “List every other part of the topic’s wording that the question leaves out,” and the closing check repeats it. It never identifies which fields constitute that wording.

D547’s **undefined-field finding holds**. Its earlier count cannot be generalized from this packet: outcome-only parts range from **1/3 to 3/3**, and the new two agreed failures concern different topics. Verdict: **missing**, because the field boundary is unspecified. The inspected judge view omits the list; D397 requires it shown beside the answer, but this code alone does not establish whether a separate product view does so.

### C. Whether to design repairs

A reference repair is worth considering for consistent recording, but the judge gains nothing until it can see the reference. It could wrongly equate a revenue share with a shipment ramp or erase a valid plan. Preserve Groq’s quoted expectation and valid null cases; the packet does not supply their articles to independently recheck every null.

An unlisted-parts repair is worth designing because readers should see what the answer leaves out. It could clutter the answer with context or split one bet into fragments. Preserve the correctly listed acquisition cost and conditions, and the outcome-only parts already listed for topics 1 and 3.