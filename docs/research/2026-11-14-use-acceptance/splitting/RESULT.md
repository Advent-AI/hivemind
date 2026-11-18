# The split probe's result (D621), 2026-11-16

Data: `poc/data/clean-split-probe-2026-11-16/` (both arms, the reading, both families' answers). The key is outside the repository.
Spend: $0.0315 (frozen arm) and $0.0516 (split arm), $0.083 in all. No charge was above its reserve.

## The verdict under the registered rule: negative

On the global-AI-capex topic's 2027 question in pass 3 (item 21, `split|week-10-06:c1/clean-12@2027`), **both families mark Q
fails**:
- Codex: "The thesis asks for the 2027 global spending total, but the question asks for spending as a share of U.S. GDP …";
- Claude: "… a different measure that also moves with U.S. GDP".

Q is a hard line, and a hard-line fault on a yearly question that both families settle is a veto (DESIGN.md v4 §0b item 4). A mark
both first readers agree on is settled without third readers. The veto therefore holds under both countings, whatever the 14
disputed gate marks and the 1 disputed LQ point rule. The verdict is **negative**.

## What else was measured

**Counts (code):**
- both T topics split in 3 of 3 sends, with both years written each time;
- none of the 30 control sends named the case;
- no control changed kind.

**Plants:** both families caught both (BY on the base-year plant, LQ on the dropped limit), so the reading is valid.

**The hyperscalers' capex (c1/clean-4), 6 yearly questions:**
- no hard-line fault by either family;
- my own read found one due-day fault (pass 2's 2026 question is due 2028-03-15), which neither family marked. D is not a hard line.

**Global AI capex (c1/clean-12):**
- the 3 2026 questions are clean for both families;
- every 2027 question has a fault by at least one reader:
  - pass 1: XR (Codex), and G and XR (Claude);
  - pass 2: L and XR (Codex), G (Claude);
  - pass 3: Q (both, the veto), and L (Codex).

**C1:** the split arm's faults are mostly the frozen arm's own on the same topics: the CPO topic's FY2028 year and its checkpoints,
and the Kyber topic's missing references and debut. The disputed points are listed in `reading/` and are not ruled, since they cannot
change the verdict.

**Following the yearly line** (my own read): in 3 or 4 of 12 yearly questions the model still listed the other year's own value as
not judged.

## Diagnosis

**The mechanism of the veto.** The article gives global AI capital spending for 2026 as an amount (Goldman's $1 trillion), and for
2027 only as a share of U.S. GDP (2.5%). The topic as Steps 1 to 3 opened it asks the total for both years, "measured against" both
measures. The split's 2027 re-ask must write a question about the total for a year whose only stated figure is in another measure.
The three sends answer three ways:
- a total with no anchor;
- a total with a reference that has no number;
- a switch of measure, which is the veto.

The frozen step declined the whole topic ("no main") in every stored send, so this weakness was hidden behind the refusal.

**What it shows (narrowed by council round 166):** a measure mismatch in this one case. The source gives 2026 as an amount and 2027
only as a GDP share, while the topic asks totals for both. The split produced a share question in one of three sends. The other two
asked totals, and their faults are unsettled. That does not establish a general rule (for example, "a yearly question is sound only
where the article states that year's value in the topic's measure"). Nor does it prove the upstream topic alone caused the switch.
c1/clean-4's six clean yearly questions are a lead, not an acceptance.

**Limits:**
- M is not exercised;
- yearly items reveal their arm;
- one draw of three sends a topic.

## The council's decision (round 166, D622)

"CONSENSUS: record the negative result without third-reader calls; stop this candidate and record the measure mismatch as a case,
not a new rule."

- The 15 disputed points stay unruled.
- D397's splitting defect stays open.
- D612's reopening conditions govern paid work again.
