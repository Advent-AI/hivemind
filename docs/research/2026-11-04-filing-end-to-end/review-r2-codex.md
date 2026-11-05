Yes. I found serious problems with the scoring and success criteria that should change the proposed test before it is run. For example, the scorer credits Google’s capex statement as preserving Broadcom’s revenue, even when the answer contains no Broadcom statement.

Filenames below refer to docs/research/2026-11-04-filing-end-to-end/ unless stated otherwise.

Findings, most serious first:

1. The scorer can count a missing fact as present.

measure_filing.py, best(), accepts four shared words without checking that the statements describe the same fact.

Concrete case: answers.json → gnews:295fceb25273abae9bb6c995 → no_fallback → third send. Broadcom’s revenue and guidance are absent from the raw answer. Nevertheless, the scorer matches gold item i234 to e4, Google’s revenue, backlog and capex. The extraction-presence match consists of “billion”, “guided”, “revenue” and “with”.

score_refile.py has the same underlying problem. In refile-no_fallback-with-rule.json, gnews:25d0b1d2a9dfe0bb99432e1a, second send, e6 describes $80.6 billion of cash and securities. It is matched to i130, the passage about Q2 revenue guidance and gross margin.

Therefore, reproducing the reported totals does not establish that the corresponding facts survived or reached the right question. This needs correction or verified matches before those totals decide adoption.

2. The noise count contradicts the frozen gold’s explicit labels.

Of the selected articles’ 427 entries inside not_kept, 408 have weight “not_kept” and 19 have weight “optional”. measure_filing.py counts all 427 as rejected material. sink_by_standard.py and score_refile.py likewise classify by the containing list rather than the explicit weight.

Those optional entries contribute 5/9/8 to the stored control’s reported noise counts. For example, the gold explicitly labels the earlier Omniverse DSX announcement in gnews:8c9d215416b714064de3b095 optional.

Evidence: golden-v5-dev.json, the three scripts above, and the standard’s §5.3/§6 distinctions. This is a scorer correction against the existing gold, not a reason to change the gold.

3. The proposed success rule already passes the variant the packet rejects.

Using the current per-item calculation, definition_no_fallback produces:

- Total-revenue intake: 15/14/16, below the proposed ceiling of 28.23.
- Gold-used items reaching a listed question: 58/55/57, against control 53/53/58.
- Core present: 52/53/50, above the proposed floor of 49.
- Reported noise: 52/54/55, below control mean 68.

It passes even if each send must meet those thresholds.

Yet supporting presence falls from 67/72/74 to 62/62/70. More concretely, Morgan Stanley’s $7.8 million Rubin rack estimate reaches the Blackwell/Rubin revenue question in all three stored sends, but in none of the three definition_no_fallback sends: it is unlinked twice and sent to capex once.

Evidence: answers.json, article gnews:f66e1689ec2e27e7eab2a2dd, e1; frozen packet item i216; measure_filing.py; review-packet.md lines 59–62.

The rule does not protect supporting evidence generally or individual questions from losses hidden by gains elsewhere.

4. “Not cited by the gold reader” is being treated too much like “not useful.”

The frozen judgement ruler explicitly excludes judging whether evidence was filed correctly. Its citations identify evidence the reader used; they are not an exhaustive list of permissible destinations.

There is also an implementation omission: load_gold() reads the structured citation lists, but not citations inside their text or reasoning. For q01 it collects 12 items, while the answer also explicitly cites i105, i111, i202 and i208.

Evidence: judgement-gold/ruler-v1.md §3; gold-v1.json, q01; measure_filing.py, load_gold(); AGENTS.md §7.1. Consequently, “kept, used by no question” should mean “not found in the structured citation lists”, not “safe to remove”.

Answers to the five questions:

1. Is this the best-supported single change?

It is a reasonable single diagnostic after the scoring and decision criteria are repaired. The evidence supports testing whether a final review recovers missed connections. It does not establish that this will reliably solve filing.

Removing the fallback alone demonstrably loses useful material. The definition variant demonstrably moves some material to undesirable destinations. I do not find another tested prompt change clearly superior. My recommendation is to retain the frozen production version while making this one proposed test capable of distinguishing improvement from loss.

2. What evidence is weaker or misread?

E1, E5 and E8 reproduce as script outputs, subject to the matching and optional-label defects above.

E3’s central claim holds: the archived q16 judgements lack Broadcom’s figures and finish below $40 billion in all three draws. Both independent readers use Broadcom. That establishes missing input; it does not prove that supplying it alone will change the judgement.

E2’s examples are genuine: d2 cites Intel’s retail price and Broadcom revenue; d3 cites Taiwan gas plants. The stated percentage needs its counting unit and classification recorded. Repeated citation occurrences and distinct cited statements are different populations.

E4’s 17% figure does not reproduce for the named 54 articles. Archived raw statements total 242; fresh stored sends contain 210/219/213, an average decline of 11.6%. Kept statements are 206 versus 174/188/190, a 10.7% decline. All 54 rebuilt request identities matched. That identity check alone does not prove wire-byte ordering.

E6’s mechanism is supported by the rack-price example. The supplied scripts do not specify the pairing calculation behind 63/51/14/10 sufficiently to establish that exact ratio.

E7 overstates uniformity: i234 reaches q16 in one stored send and two combined sends, a gain of one send, not two.

E8 measures statement instances across repeated sends, not 42 independent facts. Its second turn also supplies an existing answer, selects statements for attention and changes the response schema. It supports the hypothesis behind an in-call review, but is not a measurement of that review.

E9 is useful explanatory evidence, not proof of causation. The earlier questions name candidate destinations, and the accounts sometimes reinstate the “own figure only” restriction that D259 removed.

3. Does the proposed wording follow the standard, and can it restore noise?

Its main instructions have support:

- Review at the end: AGENTS.md §6.
- Choose the narrowest connected question: D207/D265 and the standard’s filing rule.
- Include indirect evidence and variants: D259/D273 and §5.1/§5.3.
- Leave genuinely unconnected material unlinked: D209.

The wording is general across industries. It also leaves D259’s broad relevance allowance intact, so it can restore noise. The saved re-file answers demonstrate this with Lisa Su’s general customer-engagement claim and existing hosted-model availability lists.

The review should remain explicitly subordinate to the preceding keep/reject decision. “A question can take it” must not become a reason to restore a rejected statement. It also cannot recover a fact that was never written, and its specific corrective branches do not address a fact already linked to the wrong narrow question.

4. Can the metric pass harm, fail improvement, or reward many links?

Yes to all three.

The rejected variant passing is a concrete false-acceptance example. The cash/guidance mismatch and optional material counted as noise demonstrate ways to penalize acceptable output.

Per-item counting prevents multiple credits for one fact, but linking that fact to many questions increases its chance of receiving its single credit. extraction.narrowest_links() removes ancestor links; it does not enforce one destination among unrelated questions. Reporting total links through M7 does not prevent this unless the decision actually considers inappropriate links.

Keep the per-item count as a summary, but require verified fact matches, explicit optional handling, and examination of losses by question and supporting/core status. Specify whether each threshold applies to the mean or every send. None of this requires editing the frozen gold.

5. What do I predict?

Lower total-revenue intake, partial recovery of useful facts, and some restored noise. I would not predict reliable recovery of every important loss.

As a limited check, I overlaid the saved second-turn links onto the no_fallback answers in memory. The existing scorer then reports revenue intake 13/18/24, gold-used coverage 56/56/52, and core presence 53/55/47. This is not the proposed in-call experiment, and it inherits the scorer defects. It nevertheless shows why the current evidence does not justify confidence that the re-check clears the worst-send core floor of 49.

I made no file edits and sent no model calls. The six frozen-file hashes pinned by test_frozen_rulers.py matched.