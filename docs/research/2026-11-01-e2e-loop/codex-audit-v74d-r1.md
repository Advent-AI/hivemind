**The next improvement is to give each decision one owner: one evidence test, one filing rule, and field definitions beside the fields.** The request still lets a familiar number look like new information while rejecting a useful statement because it looks old, technical or difficult to file.

No files changed and no model calls ran. No `-o` destination was supplied, so the report follows here. Proposed wording is untested.

References below use **A**, **B**, and **C** for [proof-v103-a-mixed11.txt](docs/research/2026-11-01-e2e-loop/proof-v103-a-mixed11.txt), [proof-v103-b-supporting29.txt](docs/research/2026-11-01-e2e-loop/proof-v103-b-supporting29.txt), and [proof-v103-c-noise10.txt](docs/research/2026-11-01-e2e-loop/proof-v103-c-noise10.txt). **Standard** means the frozen `docs/prd/05-extraction-standard.html`, including D250.

1. **First priority: make filing depend on the statement’s connection to the particular question.**

   Exact wording:

   > “and what makes that figure more or less likely: the demand, supply, competition and pricing behind it”

   — `src/hivemind/placement.py:52`

   > “the id of the narrowest open question … whose takes line covers it”

   — `src/hivemind/placement.py:60`

   **Verdict: abstract; duplicate owner.** The identical tail appears under 17 numeric questions in the reconstructed request. “Narrowest” cannot reliably distinguish them when they all advertise the same broad coverage. The period exception is also repeated in every numeric line and again in the `links` description.

   Read-only replay of the three saved sets reproduced **89 reported noise occurrences; 59 were linked to Data Center revenue**. Across all retained records, **218/517** had that link. These are occurrences across the supplied sets, which contain **44 distinct article IDs**, not 50 distinct articles.

   Two concrete examples:

   - *Valar Atomics wants to power data center using minimal water*: “Their reactor … went critical on June 18 … generating 100 kilowatts.” Three noise occurrences reached the ledger, although the useful matter is the proposed NVIDIA partnership. **C:6**.
   - *Silent AI Colonialism*: “Yongin will ultimately demand about 15 GW of electricity.” Four occurrences across A/B reached the ledger. The number does not itself establish an effect on the company’s supply or economics. **A:11; B:41**.

   Standard **405** requires an identifiable connection; sharing an ecosystem is insufficient. Standard **370** also allows indirect evidence, so replacing the tail with “only this question’s own figures” would overcorrect.

   **Replacement in `links`:**

   > “After deciding that the statement is evidence, identify which question’s quantity or event it informs through a connection supported by the item. Compare relevant specific questions before a broader revenue question. Shared company, industry or ecosystem membership is insufficient. A question can take evidence about the demand, supply, competition or pricing behind its answer, not just direct measurements.”

   Keep the existing period allowance **once here**. Numeric takes lines should identify the quantity, scope and period; event lines should retain their specific coverage.

   **Expected effect:** less unrelated material filed under revenue; better retention of indirect evidence. **Risk:** demanding a quantified or explicitly stated financial impact would lose supplier results, customer backlog and named adoption. The replacement must not impose that requirement.

2. **Second priority: reconcile newness and existing arrangements without pretending wording reveals missing history.**

   Exact wording:

   > “take it only when … it is new to an analyst following the company”

   — `role-v74d.txt:5`

   > “An action is a step the item reports as news: taken, decided or planned”

   — `role-v74d.txt:4`

   > “guidance, and a forecast or a plan still in force, keep their place even when retold”

   — `review-v74d.txt:1`

   **Verdict: contradiction between owners; abstract action boundary.**

   The proof lines contain **18 D250-arrangement noise occurrences**, including the combined D250-1/D250-3 line:

   - *Oldest manufacturers*: “Wistron … is establishing AI supercomputer manufacturing operations in Texas for NVIDIA.” **3/3**, **B:11**.
   - *Open Models*: “KiloCode integrated Nemotron into its code-routing architecture…” **2/3**, **A:34**.
   - Additional cases include NAVER, humanoid-company lists, available hosting platforms, an existing revenue-share facility, Hesai and Anthropic.

   Conversely, **two core matters are absent in all three A sends**:

   - *Kyber release*: “canceled the four-die Rubin Ultra design…” **A:28**.
   - *Authorized customers*: “Beijing refused to allow Chinese companies to buy…” **A:77**.

   The earlier probes explicitly attribute these omissions to “known” information: `probe-v79-newness.txt:3,8`. They support the mechanism, but are **not v74d explanations**.

   Standard **227,397,400** distinguishes an existing arrangement from an operative forecast or plan and says not to infer retelling when the text does not establish it.

   **Replacement, owned by the closing check:**

   > “Judge the particular action or information reported, not its verb tense. An arrangement merely described as already in place is background. An earlier announcement does not by itself make an operative forecast or plan obsolete. Do not infer that a reported action is old merely because its date is missing.”

   **Important limit:** Wistron’s supplied article does not date its original announcement. Its present-tense sentence resembles a permitted supplier expansion. This rewrite clarifies the distinction but cannot guarantee that case is solved. Requiring “newly announced” would lose legitimate undated actions.

   **Expected effect:** protect the two core omissions and reduce obvious existing-arrangement noise. **Risk:** SimReady integration, Samsung/SK Hynix expansion and LG discussions sit near the same boundary; they must remain explicit recall checks.

3. **Third priority: repair the common-knowledge example and remove the quantity-only definition of a judgment.**

   Exact wording:

   > “the leading soft-drink brand has held 40% of its market for years”, **“in an article about a bank”**

   > “nor a competitor’s current share, volume or price … stated with a figure”

   — `review-v74d.txt:4`

   **Verdict: misleading example; overly broad exception.** The rejected example teaches *unrelated industry*, while the accepted example teaches *current competitor + number*. It fails to teach the actual distinction in Standard **379–383**: a familiar competitive position can remain background despite its number.

   - *AMD Stock and Intel Crushed Nvidia*: “Intel has led here for years and holds more than 59%…” appears in all three answers. **B:56** prints five record matches, not five sends.
   - The same article’s “dominate the $200 billion CPU market” appears twice. **B:58**. A number is again being treated as sufficient substance.

   **Replacement:**

   > “A number alone does not turn a familiar competitive position into new information: ‘the rival grocer has led this market for years and still holds 40%.’ Distinguish that from a new specific market observation. Apply the analyst’s evidence test to both.”

   Separately:

   > “specific judgements (a level, direction or date for a quantity)”

   — `categories-v74d.json:33`

   **Verdict: narrower than the standard.** Standard **376,382** includes specific judgments about constraints and competitive consequences, not only quantities.

   Two missing examples:

   - *Next-gen AI rack system*: “no proven solution to expand the scale-up world size…” **B:62**.
   - *Kyber … Asian suppliers drop*: “The gap could give competitors … room to move in.” **B:93**.

   **Replacement T8 reading instruction:**

   > “Read the author’s forecasts, estimates, calculations and specific judgments, including their reasons and assumptions; preserve the original attribution of cited facts and figures.”

   The closing check remains responsible for rejecting unsupported commentary.

   **Expected effect:** reduce familiar-share noise and preserve specific qualitative judgments. **Risk:** “demand remains strong,” generic competitive optimism and interpretations adding no fact or calculation must still fail.

4. **Fourth priority: stop the product-detail exclusion from swallowing product progress.**

   Exact wording:

   > “a product feature, performance, compatibility, retail price or content detail that gives no business scale”

   — `role-v74d.txt:7`

   Its exception is elsewhere:

   > “the launch, shipment, delay or cancellation of the product that carries the company’s value…”

   — `review-v74d.txt:5`

   **Verdict: contradiction in scope; split owner.** The exception sounds restricted to the principal product, while the frozen gold also keeps supporting evidence about smaller product lines.

   - *RTX 5080 SUPER*: “signals that NVIDIA is going ahead with the lineup instead of canceling it.” **B:109**, absent 3/3.
   - *Unannounced RTX 50 Super*: Seasonic’s listing as evidence that the refresh may happen. **B:119**, absent 3/3.

   Standard **387,394,444** separates technical specifications from evidence about actions and progress; uncertainty and smaller business importance do not automatically disqualify evidence.

   **Replacement, in the closing check only:**

   > “Reject specifications and performance details without business substance. Separately judge a reported launch, shipment, delay, cancellation or change to a product plan or configuration; uncertainty or a smaller product line does not by itself make that statement a specification.”

   **Expected effect:** recover the two progress matters without collecting wattages. **Risk:** treating every compatibility listing as progress would reintroduce product-detail noise. The statement must actually support a product-plan inference.

5. **Fifth priority: define the recorded matter beside `quote` and `one_line`; do not optimize quote length as a noise fix.**

   Exact wording:

   > “One evidence item records one statement … Copy its quote verbatim…”

   — `role-v74d.txt:16`

   But `quote` and `one_line` have **no descriptions** in the v74d schema. Their definitions remain in the system role.

   **Verdict: misplaced definition; some reported failures are not separate noise matters.**

   - *GPU Debt Backstop*: all six A/B answers quote “Nvidia revenue is skyrocketing” alongside the useful second-half estimate disagreement. Their summaries describe the estimate disagreement, not a separate “skyrocketing” finding. **A:57; B:74**.
   - *Silent AI Colonialism*: the emissions sentence also contains the retained **26% shipment-growth forecast**. **A:9; B:40**.

   Standard **231** explicitly handles incidental rejected text inside the same retained matter. Standard **408–420** requires enough context to preserve meaning.

   The reported **33 mixed records** and **89 noise occurrences** are different counting units. Accordingly, **56 is an approximation**, not an exact count of independent remaining noise matters.

   **Replacement `quote` description:**

   > “Copy the source verbatim. Include the attribution, terms and conditions needed to support this matter; neighbouring text does not justify a separate claim.”

   **Replacement `one_line` description:**

   > “Write a standalone summary of this matter, preserving its speaker, action or measure, period, conditions and uncertainty. Do not promote neighbouring commentary into an additional finding.”

   **Expected effect:** cleaner stored meaning, not a claimed removal of every mixed-quote flag. **Risk:** aggressive clipping already lost partner amounts and context in v74b; preserve Sharon’s amount, Firmus’s forecast and conditional calculations.

6. **The complete duplicate-rule audit shows why consolidation is needed.**

   All role/review references here are under `src/hivemind/prompts/`.

   | Role wording | Closing-check wording | Difference |
   |---|---|---|
   | `role-v74d.txt:7`: feature/performance/compatibility/retail detail without scale | `review-v74d.txt:5`: product/benchmark detail, plus published comparisons | Closing check adds comparisons and all exceptions. One rule requires two locations. |
   | `role:8`: positions, trades, price moves **and market value** | `review:8`: positions and price moves | Market value disappears from the second list; Standard 395 makes it optional. |
   | `role:8`: news behind a move **“is kept”** | `review:8`: exclusion **“does not cover”** that news | Automatic retention versus returning to the evidence test. |
   | `role:9`: unrelated companies’ valuations, prices and deals | `review:9`: **any** other-company matter without a connection | Different coverage; the latter carries D250’s broader test. |
   | `role:10`: common knowledge “unless” a figure and specific account | `review:4`: number alone insufficient; current-share exception | Different emphasis encourages numbered background. |
   | `role:10`: background/history | `review:3`: existing use, arrangements and earlier deals | The closing check adds substantial conditions absent from the first list. |
   | `role:10`: general risks/unargued verdicts | `review:6`: adds interpretations of recorded events, calculations and conditional valuations | Important boundaries exist only at the end. |
   | `role:10`: political/strategic views | `review:7`: views **without a figure and decision** | The role’s exclusion is broader. |
   | `role:11`: same fact/arrangement; detailed transaction-versus-programme distinction | `review:10`: “same fact (keep the fuller one)” | “Fuller” can mean a broad programme description and suppress a distinct transaction. |
   | `role:12`: characterizing quotation | `review:6`: same rejection combined with unargued views | Duplicate owner. |
   | `role:13`: boilerplate/bylines/templates | No corresponding final row | Missing from the purported final list. |

   Two further precedence conflicts:

   - `role:5` says an exception **never keeps** an item; `review:2,6` recognizes explicitly retained cases. Standard **451** distinguishes “return to judgment” from “keep.”
   - `role:4–6` makes membership in four kinds compulsory; Standard **372** says these are usual forms, not an exhaustive admission gate.

   **Replacement procedure:**

   > “Read every paragraph and apply the closing evidence test to each research matter. The four forms describe common evidence; membership does not decide retention. Apply each exclusion with its own boundary. Preserve cases the boundary explicitly retains.”

   Delete the role’s rejection list. Merge its necessary content into the closing check or the relevant field definition.

7. **The residual omissions require different explanations; they are not one prompt defect.**

   The proofs flag **29 raw-zero rows: 2 core and 27 supporting**, representing **22 distinct article–matter pairs**. Direct reading rules out one claimed complete omission: **Omniverse’s free-production decision is present in all three A answers under alternative quotations**. Its details vary, but it is not “never written.” **A:16**.

   The remaining inventory:

   | Matters absent in the indicated set | References | Diagnosis |
   |---|---|---|
   | Rubin Ultra cancellation; Beijing refusal | A:28,77 | Newness/retelling conflict; earlier probes identify it. Relevant questions already exist: v18 and v8. |
   | SimReady integration; Jetson Thor/Reachy integration | A:17; B:45,105 | Existing-arrangement versus integration boundary. v74d does explicitly permit integration; precise current cause remains unconfirmed. |
   | Samsung/SK Hynix expansion | B:38 | Same boundary; present in one A send. Earlier probe names the mistaken background reading. |
   | Micron actual results; Micron guidance; Microsoft backlog; Apple’s memory-cost-driven price increases | A:60,62,68; B:23,87,88,113 | Relevant operating evidence omitted despite `role:4`. Earlier probes support over-rejection of indirect evidence for Micron/Apple. Do not broaden to all other-company figures. |
   | Higher backstops; no intention to invoke them; accelerating programme negotiations; conditional rental IRR | A:45–47,55; B:69,70,72 | Specific estimates, programme information and conditional analysis. T8’s narrow definition and programme-level merging are plausible contributors; no v74d probe establishes which. Higher backstops appears in one B answer. |
   | “No proven solution”; competitive opening; rising older-GPU rental prices | B:62,93,144 | Specific qualitative findings versus general commentary. Existing examples do not explain the distinction well enough. |
   | Utah executive order | B:97 | A policy action explicitly allowed by `role:4`; no demonstrated wording defect beyond the possible background reading. |
   | Two RTX refresh-progress matters | B:109,119 | Product-detail/progress scope conflict described above. |
   | McKinsey’s 2035 market estimate | B:124 | Already allowed by `role:4` and `review:1`; omission mechanism unconfirmed. No basis for adding another “keep distant forecasts” instruction. |
   | LG discussions about rack cooperation | B:136 | Strategic-view/action boundary; earlier probe explicitly describes this error. |

   For the unconfirmed cases, **“misread, cause unconfirmed” is more defensible than inventing a causal sentence**. Existing probes concern earlier configurations.

8. **Most written-but-unfiled examples do not require a new seed question.**

   There are **10 zero-reached rows with nonzero raw counts**, covering **9 distinct matters**:

   | Written matter | References | Available coverage / limitation |
   |---|---|---|
   | Annual 2028 AI capex | A:41 | Existing capex questions plus the explicit other-period/population allowance. Leaving it empty conflicts with that allowance. |
   | Cumulative 2024–2029 capex | A:53 | Can inform the capex outlook without becoming a one-year total. One B send does retain it. |
   | AI debt-market forecast | A:42; B:67 | Evidence about funding the buildout; assess the connection to spending/demand. It is not NVIDIA’s own commitment amount. |
   | Firmus energy agreement | A:52 | Customer deployment/demand connection, already explained by the article; not automatically NVIDIA’s own obligation. |
   | Changing CPU:GPU ratio | B:4 | Relevant existing CPU revenue/accelerator-share questions. |
   | PC superchip launch | B:54 | No dedicated PC question, but a possible connection to total revenue; it must not be forced into Data Center or standalone Vera revenue. |
   | NVL576 delay | B:61 | v18 already explicitly takes variants, delays and configuration changes. This is a misapplication, not a missing takes category. |
   | DSX Flex pilot | B:82 | Potential deployment/demand evidence; assess its actual connection rather than requiring its own question. |
   | NVIDIA raising its own debt | B:14 | No direct own-borrowing question is shown. v9 concerns commitments **to others**. Do not solve this by reversing v9’s meaning. |

   Partial losses also remain: **A:27,50; B:71,145; C:51,52,55**. These include intermittent filing failures and a Firmus quote refusal. The latter is **not an evidence-selection defect**.

   **Additional replacement in `links`:**

   > “Resolve references and variant names from the surrounding item before comparing questions. A statement need not match the question’s words. If no question or permitted candidate covers it, leave links empty.”

   No seed-content changes are proposed.

9. **Proposed structure and measured size.**

   Keep one call and the existing output shape.

   | Location | Sole responsibility |
   |---|---|
   | System role | Analyst task, complete article walk, evidence before filing, four illustrative forms, distinction between evidence and proposing questions. |
   | Category block | What kind of source this is and where to look. Remove competing rejection rules and repeated tier assignments. T6’s customer-list exclusion belongs in the final check; T8 gets the replacement above. |
   | Subjects/reference | Company context, fiscal conventions and reusable identity names. Preserve the supplied questions. |
   | Open-question takes lines | Question-specific quantity/event, scope and period. Preserve event coverage; remove repeated numeric tails and period exceptions. |
   | Article | Unchanged. |
   | Closing check | The standard’s retention test and one complete rejection list, with each boundary attached to its own row. Final review remains in the same call. |
   | Schema descriptions | `quote`, `one_line`, attribution, tier, links, candidate opening reasons, dates, scope, groups and bounds. Move existing definitions here rather than copying them. |

   In particular, move tier precedence to `tier`: the existing ordered definition in `extraction.py:82–86` is more precise than repeating simplified tier statements in the role and category blocks. This is an ownership improvement; the supplied proofs do not establish a separate tier-failure count.

   I constructed and counted an **in-memory structural draft** against the requested debt-backstop article and the same 22 questions:

   | Component | Current characters | Draft characters |
   |---|---:|---:|
   | System role | 12,729 | 2,521 |
   | User message, including article and closing check | 44,404 | 39,251 |
   | JSON schema | 4,510 | 11,507 |
   | **Total** | **61,643** | **53,279** |

   **Reduction: 8,364 characters, 13.6%.** The article’s 26,588 characters are unchanged. Counts use the same `json.dumps(..., ensure_ascii=False)` schema serialization and exclude transport wrappers. Moving definitions enlarges the schema; removing duplicate instructions makes the complete request smaller.

   The ranking above is by expected practical effect, **not measured improvement**. Start with question-specific filing and the contradictory evidence owners; protect the two core omissions while doing so. Treat product progress and specific judgments separately. Quote cleanup comes last because many of its apparent wins would merely shorten records that already contain valid evidence.

