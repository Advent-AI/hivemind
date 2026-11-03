**The “one dial” conclusion is not supported. Some borderline cases remain difficult, but the design also contains separable defects: it confuses who speaks with what they say, lets neighboring claims supply a statement’s justification, and substitutes filing eligibility for evidence value.**

For example, Zuckerberg’s “slower-than-expected progress” is discarded because he represents a customer, while a journalist’s equally unquantified judgment avoids that check. That is a design error, not an unavoidable trade-off.

I read the complete stored v94 request, the governing sections, both gold files, the supplied probes, and raw answers beside their articles. No files changed and no paid calls ran. Proposed wording below is untested.

**1. The field design applies the wrong evidence rule to customer and competitor judgments. — Contradiction / design**

The design maps kind 3 to `analyst_or_outlet`, although the standard says **a named party’s claim or estimate**, not just an analyst’s. Its implementation rejects:

> `if e['party'] in RELATED_PARTIES and e.get('scale', 'none') == 'none'`

See [design-v78-fields.md:14](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/design-v78-fields.md:14) and [extraction.py:210](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/extraction.py:210).

**Stored example.** In [poc-v100-supporting-41.json](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/sends/poc-v100-supporting-41.json), article `gnews:c675…`, third answer, `e15`, Zuckerberg’s slower-than-expected agent progress is correctly recognized as `new/judgement`, but classified `customer/none`. The code therefore rejects it. The [gold keeps it as supporting](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:16023). Lisa Su’s customer forecasts exceeding expectations suffer the same problem.

The governing distinction is between **actions/operating figures** and **claims/estimates**, not between customer executives and professional analysts: [standard §5.1, lines 375–376](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:375).

**Alternative formulation:**

> “Identify what the statement asserts separately from the speaker’s relationship to the company. A customer or competitor can make a specific claim or estimate. Judge that claim under the named-party rule; do not reject it solely because it lacks an amount or date.”

**Predicted effect.** Recovers these named judgments without admitting partner lists. Simply removing the rejection would also admit noise: among nine raw records triggering this predicate across the two v100 files, Corning’s generic “world needs our glass optical fiber” also appears. Thus the correction must preserve the specific-claim test. No kept matter needs to be lost.

**2. The role’s procedure still contradicts the standard; changing exception precedence did not resolve it. — Contradiction**

The role says:

> “A material statement is one of four kinds.”

> “take it only when it has a kind and nothing on the list applies.”

The closing check says:

> “Fitting one of the four kinds does not keep an item.”

See [role-v74.txt:4](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v74.txt:4) and [review-v74.txt:1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/review-v74.txt:1).

The standard explicitly says the four kinds **describe** evidence; acceptance comes from the analyst’s judgment, including each rejection’s boundary: [§5.1, lines 370–372](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:370).

**Stored example.** The v94 Nations-blog answer, archive call `186`, keeps ThinkDeep, Sarvam and Widelabs as evidence. Each describes an existing service. The [gold rejects all three under D250’s arrangement rule](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:6949). Their names and reported benefits satisfy the role’s recognizable shapes without establishing a new step.

The author’s v77 experiment made “has a kind” the default reason to retain a statement and removed the closing warning. Its increased noise therefore does not exhaust sentence-level remedies.

**Alternative formulation:**

> “For each research matter, identify the new event, figure or specific judgment an analyst would record. Apply §5.3’s exclusions with their own boundaries. An exception removes only that exclusion; it does not establish that the statement should be kept. Retain every matter that passes.”

**Predicted effect.** Reduces existing-arrangement noise while preserving genuine adoptions without amounts. The “eight statements” sentence is not itself wrong; its antecedent must mean eight statements passing this test. A blanket “reject partner lists” substitute would lose the kept EY/Abridge/Amdocs/Box matter.

**3. The decision attaches to an entire quote rather than the particular assertion it justifies. — Design / missing**

The role says:

> “One evidence item records one statement. Copy its quote verbatim…”

The closing check exempts adoption:

> “also when a comparison shares its sentence”

See [role-v74.txt:16](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v74.txt:16) and [review-v74.txt:5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/review-v74.txt:5).

**Stored examples.**

- V94 archive call `223`, `e1`, quotes “Nvidia remains the king” alongside revenue-growth figures. Its summary asserts the figures, not leadership.
- In v100’s Nemotron-blog third answer, the quote contains both LangChain’s integration and its benchmark comparison. The whole record becomes `product_comparison_or_detail` and is rejected, losing the kept integration.
- The [common-knowledge probe:3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/probe-v80-common-knowledge.txt:3) explicitly justifies the “king” passage using the neighboring financial figures.

The standard already distinguishes the adoption from its accompanying comparison, and records **one matter**, not necessarily one grammatical sentence: [D250 items 3 and 5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:229).

**Alternative formulation:**

> “Decide which research matter this record preserves. Apply the evidence test to that assertion. Retain the quoted context needed to understand it, but do not let an adjacent number, date or comparison justify another assertion. A comparison accompanying a qualifying adoption does not erase the adoption.”

**Predicted effect.** Preserves integrations while reducing independently summarized characterizations. It need not lose any kept matter. A shortest-quote rule would risk losing conditions and attribution; I do not recommend one.

The reported **13 of 33** mixed-quote cases are consequently not proof of 13 independent bad decisions. D250’s existing counting rule already requires examining what each record preserves. No ruler change is needed.

**4. “Known” conflates a statement’s age, its disclosure date and its continuing relevance. — Contradiction / abstract**

The closing check asks:

> “whether it is new”

The v80 definition goes further:

> “reported as recent (days or weeks, not an earlier month or year)”

See [review-v74.txt:1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/review-v74.txt:1) and [extraction.py:162](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/extraction.py:162).

**Stored examples.** The [v79 probes](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/probe-v79-newness.txt:1) reject Beijing’s refusal as an existing position and the design cancellation because another report appeared the previous week. V80 rejects Omniverse’s licensing change as `known`, although the article distinguishes the May effective date from the July announcement.

The standard supplies an operational rule despite unavailable company memory: judge retelling from **text and dates**, do not presume it when unclear, and preserve still-effective guidance, forecasts and plans: [§5.3:400](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:400).

**Alternative formulation:**

> “Distinguish when the underlying event occurred from when this item reports it. Do not infer that a statement was already known merely because the project began earlier or the item cites another report. Apply the separate rules for an existing arrangement, a retold actual figure, and guidance or plans still in force.”

**Predicted effect.** Recovers recent disclosures and continuing guidance without reopening clearly retrospective arrangements. A compulsory recent-date test would lose the kept DeepSeek project, underway for a year, and LG’s discussions “last month.” The wording cannot perfectly resolve every undated arrangement.

**5. Filing is being used as the evidence test, and “relationship” is being substituted for a causal path. — Abstract / design**

The role calls each `takes` line:

> “the one rule for what belongs in that question’s file”

The schema permits an empty link:

> “however important it sounds.”

See [role-v74.txt:1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v74.txt:1) and [placement.py:60–64](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/placement.py:60).

**Stored example.** The [debt-raising probe:18](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/probe-v75-residue.txt:18) first recognizes NVIDIA’s financing plan as evidence, then says it should be omitted because it does not concern demand, supply, competition or pricing. That is the filing vocabulary replacing the evidence rule.

Conversely, the author’s proposed “the path is the relation itself” is too broad. D250 requires a path from **this matter** to a question; being a supplier does not make everything the supplier does relevant. [Standard §5.3:405](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:405).

**Alternative formulation:**

> “First establish why this statement is evidence under §5.1–5.3. Then file it under the narrowest covered question, considering that question’s actual quantity or event. Explain the connection through what the statement changes; a shared company, industry or ecosystem is insufficient. An unfiled statement is dropped under D209, not reclassified as background.”

**Predicted effect.** Reduces generic ecosystem filing and preserves relevant indirect evidence. It cannot recover genuinely homeless statements without another authorized change. Requiring an explicit revenue amount would wrongly lose supplier figures and named customer actions.

Identical tails do **not** make all questions identical—the quantities still differ—but they provide insufficient guidance when treated as topic keywords. The stored period conflict is real; D268’s current `takes()` wording already addresses it.

**6. The examples disproportionately teach quantified evidence and leave specific, unquantified judgments underdefined. — Missing**

All five kind-2 examples in [role-v74.txt:4](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v74.txt:4) contain a quantity or duration. T8 says:

> “The author’s forecasts and price targets with their figures”

T6 separately directs attention to:

> “partnerships, investments”

See [categories-v74.json:25](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/categories-v74.json:25) and [:33](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/categories-v74.json:33).

**Stored example.** V94 archive call `200` extracts nine backstop records but omits the analyst’s claim that second-half shipment/revenue consensus is materially below its supply-chain estimate. That claim specifies a quantity, direction, comparison and period without giving the amount of disagreement.

The standard keeps new specific judgments and named actions without amounts: [§5.1:375–382](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:375).

**Alternative formulation:**

> “Read forecasts and specific judgments, carrying figures when supplied. ‘The analyst expects next year’s loan losses above consensus’ specifies an estimate without an amount; ‘the bank faces challenges’ does not. Read partnerships for the reported action, not merely the existence of a relationship.”

**Predicted effect.** Improves unquantified-judgment recall while retaining the exclusion of general commentary. No kept matter inherently needs to be lost. These examples should replace existing examples, not lengthen the request indefinitely.

**Blind spots in the author’s conclusion**

- **The fields discard distinctions before the filters examine them.** “Effectively zero” is labeled `scale=none`; a specific technical impossibility and general optimism both become `judgement/none`. Failed filters over these labels cannot establish inseparability in the source text.
- **The author notices mixed quotes but does not carry that distinction into the impossibility claim.** TD Cowen’s generic shortage assertion is rejected by the gold; climbing rental prices are kept. The preserved evidence is the latter, even when one quote contains both.
- **The 70% agreement figure predates the boundary decisions.** The [standard’s D250 history:223](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:223) describes disagreements that prompted those decisions. It is not a measured ceiling under the frozen definitions.
- **The many jobs in one call remain an untested contributor.** Extraction, filing, candidate creation and identity construction interact, but their presence alone does not prove the cause. No second call is necessary to correct the contradictions above.

**Verdicts on the four claims**

| Claim | Verdict |
|---|---|
| 1. One dial | **Wrong as a universal conclusion.** Coarse filters fail; identifiable prompt and code defects remain. |
| 2. `takes` becomes the keep gate | **Substantially right, but incomplete.** The probes demonstrate substitution. Identical tails do not eliminate the questions’ different subjects. |
| 3. Exceptions become universal permission | **Right as observed behavior; incomplete diagnosis.** Several exceptions accurately reproduce the standard. The missing distinction is “not rejected by this row” versus “accepted overall.” |
| 4. No memory makes newness unanswerable | **Incomplete.** Some cases lack decisive context, but the standard explicitly supports text-based judgment. The historical reader result does not establish present impossibility. |

**“One dial”: separable in part, not a demonstrated perfect separator**

The useful signal is **a reported change or specific research assertion**, rather than **an existing service or general characterization**. It belongs to the assertion, not to its surrounding paragraph.

| Frozen gold keeps | Signal | Frozen gold rejects | Signal |
|---|---|---|---|
| Perplexity chooses the CPUs | A selection decision | ThinkDeep’s service | Existing use and benefits |
| EY expands implementation capabilities | An expansion action | Sarvam’s service | Existing availability and reach |
| Sharon plans deployment of 40,000 GPUs | A prospective deployment plan | Widelabs’ service | Existing use and beneficiaries |

The kept cases are documented at [Perplexity](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:16005), [EY](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:16485), and [Sharon](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:1715); the three rejected cases appear together in the [Nations-blog gold](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json:6949).

**Known failures of a simple version of that signal:** “is establishing” would wrongly admit Wistron; requiring explicit change wording would lose SimReady integration; requiring a recently begun activity would lose DeepSeek’s year-old project. These remain system gaps. They do not justify treating the entire residual population as inseparable—or choosing a global permissiveness setting before correcting the concrete defects.

