# The D745 targeted test: result

Run folder: `poc/data/judging-v13s-blind4-2026-11-23/`. It was registered in `SMALL-DESIGN.md` §5 [D745] and scored by
`blind4.py tally` (`TALLY.json`).

## 1. Verdict: FAIL (registered line "every S and E reply has a settled yes")

| Packet | Case | Writer | Shape | First readers (Codex, Claude) | Adjudicators (Codex, Claude) | Settled | Line |
|---|---|---|---|---|---|---|---|
| U05 | E | codex | forecast, rung 3 | no, no | (none) | **no** | **MISS** |
| U02 | S | claude | forecast, rung 4 | no, yes | no, yes | split | MISS (inconclusive) |
| U08 | S | codex | forecast, rung 4 | no, yes | no, yes | split | MISS (inconclusive) |
| U06 | E | claude | forecast, rung 3 | no, yes | no, yes | split | MISS (inconclusive) |
| U04 | S | control: justified unresolved | unresolved | yes, no | yes, no | split | control not confirmed |
| U07 | P-v8 | codex | forecast, rung 2 | yes, yes | (none) | yes | ok |
| U09 | P-v8 | claude | forecast, rung 2 | yes, yes | (none) | yes | ok |
| U01 | P-v8 | control: unjustified unresolved | unresolved | no, no | (none) | no | ok |
| U03 | E | control: unsupported (15% cut) | forecast | no, no | (none) | no | ok |

- **Refusals and defects.** All 6 first replies passed the schema and the code checks and were publishable. No reader marked a defect,
  so no defect is settled or split.
- **Writers never withheld.** 0 of 6 replies answered unresolved, including on S and E, where the new sentence invites it.
- **One construction change, disclosed.** The registered row for K-unresolved-justified reads "S made unresolved with the specific
  gap". It was first built on the third run's S Claude reply, which the current code refuses (S1, F11 "estimated"). It was rebuilt on
  the third run's S Codex reply with the same reason text, and the code accepted it. The reason's five passage citations were checked
  against the request.

## 2. What split, and along which line

Every disagreement split by model family, and the four adjudications did not settle any of them: 8 of 8 adjudicator votes went with
their own family. On S and E, Codex read "supported" as "a passage states the size of the band-deciding assumption, or bounds the
same quantity". Claude read it as "the passages give a checkable bound that makes the rung most likely".

- **S (data-center spending of the four largest cloud companies in 2026; the rung 3/4 edge is $700B).** Both writers forecast rung 4.
  The Claude writer took $720B of total spending at a 98% data-center share. The Codex writer took $745B minus a $25B non-data-center
  deduction. Every reader on both sides read the same passage as decisive: e1947, "more than $730 billion combined on AI
  infrastructure", for the same four companies.
  - Claude: AI infrastructure sits inside data-center spending, so e1947 is a floor above $700B.
  - Codex: e1947 gives no data-center split, so it does not bound the share.
  - The answer's own stated lower bound gives $691B, in rung 3 (Codex adjudicator, U02).
- **E (FY2028 Vera CPU revenue; management's "more than double" of $20B sits on the $40B edge between rungs 2 and 3).**
  - The Codex writer realised 90% of the $40B reference. Its basis was deployment plans, a customer evaluation and a competitor's
    benchmarks, and it said itself that "the passages give no order sizes or shipment pace". Both first readers, one per family,
    said not supported, so no adjudication was needed (corrected after council round 61, which caught "all four readers").
  - The Claude writer bracketed the pace between the server-CPU market pace (about 1.5x, e4687 and e4857) and the guidance (2x), then
    took a 90% Vera share.
    - The Codex adjudicator showed that the bracket fails under the answer's own share: 1.5 × $20B × 90% = $27B, in rung 4.
    - The Claude adjudicator rescued it by arguing a near-full Vera share from e4691 and e4856.
- **The justified-unresolved control.** Codex accepted the reason "no passage gives the share". Claude rejected it on the same e1947
  floor, so the control's expected reading is itself contested.

## 3. What the frozen gold does on the same kind of question

These are read for reasoning only. The gold questions differ from S and E in ladder and window.
- **q04 (the same four companies' 2026 data-center spending).** Reader B took the big four's total plans of about $650B as the
  reference, "the figure NVIDIA management also cites", with no deduction, and bet $650–720B.
- **q19 (FY2027 stand-alone Vera revenue).** Reader B discounted management's $20B to $8–18B. The reasoning was the launch timing
  (about two selling quarters) and the units the figure implies ($5,000 per CPU means four million units), against one counter-signal.
  No passage states the discount.

The frozen ruler's own answers are reasoned bets of the kind the Claude family accepts. D741 ruling 3 (Alex) is stricter for S: the
deduction must be stated.

## 4. What the paid re-send would meet

Under the paid gate's lines (`PAID-GATE.md` §4), a published singleton with a "deciding gap" stops the run. A deciding gap includes "an
unsized adjustment decides its band". Where the two readers disagree, the third reader is Codex. On blind4's evidence, a published E forecast built like
these replies risks being marked by Codex, and the run would stop.
- **Two corrections from council round 61, both checked:**
  - An unresolved singleton is published, shown as unresolved (`calc_small.publish_decision`: "held" only when a declared relation
    joins it to an answered member). The paid verdict inspects published singleton cards for defects (`paid_gate.py`, verdict), so it
    is not exempt.
  - The paid S singleton asks about CY2027 (`paid_gate.py` SINGLETONS: old-2 v6 8595). This test's S asks about CY2026 (`SMALL-DESIGN.md`
    §5: old-3 v6 9043).
- These votes are about support. They show a risk to the paid run, not a measured rate at which it would stop.

## 5. Not done

Nothing was paid. Nothing was tuned on the 36 stored answers. No request text changed after the registration.

## 6. The re-read under Alex's comparison ruling (D747): FAIL on a stop line

Registered in `SMALL-DESIGN.md` §5 [D747], reviewed by council round 62 (`codex-r62.md`), and scored by `blind4.py reread-tally`
(`REREAD-TALLY.json`, `reread-reasons.json`). Packets W01–W09 are in `reread-packets/`, adjudications in `reread-adjudication/`, and
the key is `reread-key.json`.

| Packet | Answer | First readers (Codex, Claude) | Adjudicators (Codex, Claude) | Settled | Registered line |
|---|---|---|---|---|---|
| W01 | U01 vague unresolved control | no, no | (none) | no | expects no: ok |
| W04 | U05 E Codex, unsized 10% cut | no, no | (none) | no | expects no: ok |
| W09 | U03 E, unsized 15% cut | no, no | (none) | no | expects no: ok |
| W02 | U06 E Claude, 1.8x × 90% Vera share | no, no | (none) | no | must settle: ok |
| W05 | U04 S justified unresolved | yes, yes | (none) | yes | must settle: ok |
| W08 | U08 S Codex, $25B deduction | yes, yes | (none) | yes | must settle: ok |
| W07 | U02 S Claude, 98% share | no, yes | no, yes | split | expects no: MISS |
| W06 | T15 E Claude, 85% growth bracket | yes, no | yes, no | split | expects yes: MISS |
| W03 | T10 S Claude, 95–100% share | no, yes | no, yes | split | must settle: MISS |

- **The stop.** On W07 (U02), both adjudicators upheld Codex's "part above or added into its whole" (F12, F11, F15). The answer
  calls F12's "more than $730 billion" of AI infrastructure "the supported floor" for data-center spending, while its own total
  spending (F11) is $720B and its data-center outcome (F15) $705.6B. The code did not catch it, because F12 is a source figure the
  answer uses as a floor only in its prose.
- **The reasons behind the six settled answers were read by Claude and recorded as compatible** (`reread-reasons.json`). Each pair
  applies the same reading. On W08, for example, both say the same four companies' AI-infrastructure figure and Meta's AI share explain
  why a deduction under $45B is more likely, and both note that this does not measure the deduction directly.
- **What the ruling changed.** Of the four answers that split in the targeted test, three now settle in both families, with
  compatible reasons: U04 yes, U06 no, U08 yes. All four controls and fixed cuts read as expected.
- **The remaining splits no longer follow model family.**
  - Codex is the stricter reader on S (T10, U02). Claude is the stricter reader on E (T15).
  - T15 was accepted by both families in the second re-read and now splits.
  - Read with the third-run S Codex reply's earlier no → yes → no, this shows single readers varying on boundary answers.
- **A process error, shared by Claude and the council.** The registration required five boundary answers to settle, or to settle as
  expected, but nobody estimated how often single readers split on boundary answers. AGENTS §7.1 says "a conjunction over many items
  fails by chance". That clause of the pass line could fail on reader variation alone. The stop on U02 does not depend on it.
