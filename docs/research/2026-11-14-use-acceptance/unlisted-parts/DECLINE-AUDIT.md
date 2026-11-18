# The decline rules against the outcome's extra parts: the $0 audit D579 asked for (2026-11-16)

**Answer: one general rule, from D397, fits every case read; nothing in it names a field as an exemption.** The rule: identify the
main part first, from both fields, and apply the decline cases to it alone.

Against the stored refusals:
- it keeps all 20 refusals on cases 1 and 4 that both readers judged justified (8 topics);
- it removes the 2 refusals both readers judged unjustified (the probe's);
- it settles the 4 topics the families split on 2 and 2, so it does not take one family's threshold.

Sources:
- `decline_audit.py` → `decline-audit-refusals.txt`: every refusal in the three stored readings outside Alex's 44 (40 refusals,
  with reasons and both first readers' N marks).
- `refusal-accounts-output.txt`.
- The 66 stored topics' descriptions and outcomes, read by me. One reader; to be checked blind if the council relies on a count.

## 1. Line 6's seven decline cases, and which can be triggered by a part other than the main one

| Case | Reads | Triggered by an extra part the outcome names? | Seen |
|---|---|---|---|
| no main figure or event, or several with none the main one | the topic | yes: an outcome that adds figures | the probe's memory refusal; control refusals on July c2/clean-10 and week clean-13 (families split) |
| nothing can be checked on a date | the topic | no | — |
| a company's figure for a quarter or half-year | the figure | yes: an outcome's checkpoints ("15,000 in Q4 2026") | — |
| a period that is not one year, with no publication day | the figure | yes: an outcome's span ("from Q4 2026 through calendar 2027") | the probe's shipment refusal |
| a year already ended | the figure | yes: an outcome's comparison year ("versus 2025") | — |
| a year beyond next year | the figure | yes: an outcome's later year ("2.8% in 2028") | — |
| another company, or no theme covers it | the question | no | — |

Five of the seven read "the figure" or "the topic". None says how to find the main part when the outcome names more than one thing.

## 2. How often the outcome names more than the description's main part

By my reading, about 30 of the 66 stored topics have an outcome that adds a second figure, a period, an event or a consequence
beyond the main part the description asks about. Examples:

- the earlier checkpoints of a shipment forecast;
- amounts paid and the remaining term of a guarantee;
- the next year's projection;
- whether revenue resumes;
- a cap on an approval.

It is the usual shape, not an exception. Under the frozen request the step declined on two of these, both on case 1 (July c2/clean-10,
week clean-13): Codex judged each refusal justified, Claude did not. Under arm A it declined on two more (case 1 and case 4), both
judged unjustified by both.

## 3. The rule, and its source

D397, Alex's choice "只判主要那件":
- "a thesis gets at most one judged question: the part its `outcome` names. Every other part of its wording is listed and shown
  beside the answer as not judged";
- "A thesis with no main part gets no judged question, with the reason recorded".

The rule fills the case D397 leaves open, an outcome that names more than one part:

> The main part is the one the outcome names. When the outcome names more than one, it is the one the description also asks about.
> A topic has no main part only when neither field singles one out. The decline cases apply to the main part; every other part of
> the description and the outcome is listed in not_judged.

The rule takes no field as an exemption. A period or figure counts as main when the outcome names it alone, or when both fields
name it. A topic stays declined when the main figure itself breaks a case: the rolling twelve months of a survey still decline (D417).

## 4. The rule against every stored refusal on cases 1 and 4

| Topic | Both fields | The rule | First readers |
|---|---|---|---|
| July c1/clean-15 (federal AI obligations and contract awards) | both ask both | no main part: decline | both justified ✓ |
| July c2/clean-6 (memory contract prices and memory cost per rack) | both ask both | decline | both justified ✓ |
| July c3/clean-3 (approval status and the scale of sales) | both ask both | decline | both justified ✓ |
| week clean-12 (global AI capex 2026 and 2027) | both ask both years | decline | both justified ✓ |
| week clean-4 (hyperscaler capex 2026 and 2027) | both ask both years | decline (case 1) | passes 1 and 2 both justified ✓; pass 3 cited case 4 (not one year) and both judged that reason unjustified, while the topic still has no main part |
| July c1/clean-10, c1/clean-13, c3/clean-9 (twelve months from mid-2026) | the main figure is a rolling twelve months | decline (case 4, D417) | both justified ✓ |
| July c1/clean-11 (amount invested and equity stake) | both ask both | decline | split (Codex justified) |
| July c1/clean-2 (stake size, carrying amount, commitment) | both ask several | decline | split (Codex justified) |
| July c2/clean-10 (custom-ASIC purchases versus GPU purchases) | the description asks custom-accelerator spend; the GPU purchases are the outcome's comparison | ladder on custom-ASIC spend; the GPU comparison listed | split (Claude unjustified) |
| week clean-13 (equity-investment commitments: remaining balance, cash paid, changes) | the description asks how much "will be funded or remain outstanding"; the outcome's first figure is the remaining balance | ladder on the remaining balance; cash paid and changes listed | split (Claude unjustified) |
| probe: fortnight clean-13 (shipments, "from Q4 2026 through calendar 2027") | the description asks calendar 2027 | ladder on calendar-2027 volume; checkpoints listed | both unjustified ✓ |
| probe: July c3/clean-7 (commodity DRAM/graphics memory) | the description makes commodity DRAM main | ladder on commodity DRAM; graphics memory listed | both unjustified ✓ |

## 5. What stays open

- **Comparisons with the reference** (the disputed kind): arm A listed them more often. Under the strict counting, H (9 against 4)
  and XR (9 against 5) passed the harm limit, and the third readers split by family on H. The rule above does not settle whether a
  comparison the middle rung carries is a part to list. D436 keeps a second side of a bet as context, shown as not judged. The July
  third readers passed unlisted comparisons with the reference (PROMPT-AUDIT-LINE-2.md §7). The two families' H readers disagree on
  them. This stays reported, not scored, and is not written into any arm.
- **The count of about 30 is one reader's.**
- **Whether the rule, once written, changes the step's answers** can only be shown by sends.
