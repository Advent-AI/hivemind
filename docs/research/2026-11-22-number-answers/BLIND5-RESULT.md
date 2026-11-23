# The D749 writer test of the E writer repair: result

Run folder: `poc/data/judging-v13s-blind5-2026-11-23/`. It was registered in `SMALL-DESIGN.md` §5 [D749], with council round 64's
changes, and scored by `blind5.py tally` (`TALLY.json`, `reasons.json`). The request is `judging-v13s.txt`, sha256 `ac707fa9…`.

## 1. Verdict: INCONCLUSIVE (two support splits, X05 and X08); no line failed

**A correction, made after council round 65 (`codex-r65.md`).** I first recorded X08's two "yes" readings as compatible, although
my own note named the tension. The Claude reader read e1947 as a floor ("at least $730B") while accepting $710.4B. The Codex reader
read it as a guide. Under the registered procedure, matching votes with incompatible reasons go to adjudication.
- X08 was sent to adjudication. Both adjudicators said yes. The Claude adjudicator again read a floor above the outcome, and the
  Codex adjudicator did not reconcile the $730B figure.
- X08 is recorded as split (`reasons.json`). The row below is corrected, and the verdict stays INCONCLUSIVE.

| Packet | Answer | Shape, rung | First readers (Codex, Claude) | Adjudicators (Codex, Claude) | Settled | Line |
|---|---|---|---|---|---|---|
| X06 | fresh E Codex | unresolved | yes, yes | (none) | yes | ok |
| X05 | fresh E Claude | forecast, rung 2 ($42B: 2.1x, 100% Vera) | no, yes | no, yes | split | inconclusive |
| X02 | fresh S Codex | forecast, rung 4 ($730B estimate from the same four companies' AI-infrastructure plan) | yes, yes | (none) | yes | ok |
| X08 | fresh S Claude | forecast, rung 4 ($740B × 96% = $710.4B) | yes, yes (reasons incompatible: floor against guide) | yes, yes (reasons incompatible again) | split | inconclusive |
| X01 | fresh P-v8 Claude | forecast, rung 2 ($383.9B) | yes, yes | (none) | yes | ok |
| X04 | fresh P-v8 Codex | forecast, rung 2 ($380.8B) | yes, yes | (none) | yes | ok |
| X03 | control: invented 10% cut (blind4 U05) | forecast | no, no | (none) | no | ok |
| X07 | control: impossible floor (blind4 U02) | forecast | floor marked by Codex only | floor upheld by both | floor settled | ok |

- **The code** accepted all six fresh replies, and all six are publishable.
- **No defect** was marked on a fresh reply.
- **The reasons** behind the five settled fresh pairs and the two controls were read by Claude and recorded as compatible
  (`reasons.json`). X08 is corrected to incompatible, as above.

## 2. What changed against the targeted test (D745), same cases

- **E.** The Codex writer no longer invents a cut. It answers unresolved and names the gap: both the FY2027 base and the FY2028
  increase are projections, and no passage gives a shipment run-rate, an order with units and prices, or a deployment schedule. Both
  readers accept it. In the targeted test, the same writer type cut the reference by 10% and was settled not supported.
- **S.** Both fresh forecasts are supported by both families. In the targeted test both split.
- **P-v8.** Both fresh replies are supported forecasts, as before. The repair did not cause withholding on the supported case.
- **The controls.** Both read as expected.

## 3. The one split, read against its passages (Claude's own trace reading)

- **The answer.** E's Claude writer takes management's "more than double" in full, at 2.1x on $20B with Vera as 100%, giving $42B,
  rung 2. It argues the FY2027 base "is reaffirmed for the current year, so the CPU line is already selling at volume rather than a
  product with no shipments".
- **The passages it saw (15).** None shows Vera shipments, reported Vera revenue or orders:
  - e4689: "will be deployed";
  - e5044: Anthropic "is evaluating";
  - e4856: the $20B is a "potential";
  - e3660: management "still expects" $20B, which is an outlook;
  - the AMD benchmarks (e5399–e5404) show only that a Vera platform exists to be tested.
- **The request's own rule** (bullet 2) says a target for a product with no shipments yet "is taken in full only when the evidence
  shows the volume in hand".
- **On the passages, the premise that decides this answer is not shown.**
  - The Codex reader and the Codex adjudicator say so.
  - The Claude adjudicator accepted the reaffirmed outlook and the benchmarked platform as enough.
  - This is a question of fact against an existing rule, not a gap in Alex's D747 words. Where the families differ is whether a
    reaffirmed outlook counts as "volume in hand".

## 4. A trace note the readers did not mark (it became the X08 split after the correction)

- **What the answer says.** S's Claude reply (X08) says data-center capex "contains all AI capex plus non-AI cloud
  capacity". With e1947's more than $730B of AI infrastructure, that implies data-center capex above $730B, while its own outcome is
  $710.4B.
- **What it means.** The tension runs in the conservative direction and does not move the band (both figures are in rung 4).
  Neither reader marked it. It is disclosed, not scored.

## 5. Not done

Nothing was paid. Nothing was tuned on the 36 stored answers. The request was not changed after the registration.
