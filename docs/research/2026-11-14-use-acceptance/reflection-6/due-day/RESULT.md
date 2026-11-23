# The due-day probe (D636): result, 2026-11-16

**Run:** astra on the frozen request against astra on v2 (the binding-obligation clause narrowed to amounts). Interleaved, 2 draws,
9 topics, 36 sends (`poc/data/clean-dueday-probe-2026-11-16/`).
- **Spend:** $1.71. D439 is at about $36.4 of $40.
- No stop, no lost answer.

**Dates (stored days, `tally-output.txt`):**

| Topic | frozen | v2 |
|---|---|---|
| Hugging Face, fortnight (stated 24 March 2028) | 2027-02-28, 2027-02-28 | **2028-03-24, 2028-03-24** |
| Hugging Face, week (window: first half of 2027) | decline, 2027-02-28 | **2027-06-30, 2027-06-30** |
| Guarantee (stated 3 April 2028) | 2028-04-03 ×2 | 2028-04-03 ×2 |
| Three obligation amounts (code-set, D414) | 2027-04-01 ×6 | 2027-04-01 ×6 |
| Reflection AI, Vera Rubin, MIIT | the same in both arms | the same in both arms |

- **The mechanism:** the frozen arm stores the completion at the next annual filing. One frozen answer even lists "The proposed
  24 March 2028 check date" as not judged.
- **v2 fixes it** on both forms in both draws, and moves no control.

**Blind review:** two reviewers (Codex and Claude), 40 items with four controls. Every control was marked as expected, so the
reading is valid.
- **Agreed counting: moves.**
  - Both reviewers confirm the frozen completion dates as material period changes (3 sends), and that v2's completion questions are
    sound.
  - Defects present equally in both arms, unrelated to the clause:
    - the purchase-commitment choices (the top band starts at $100 billion against $279 billion disclosed);
    - Vera Rubin's year-end due day against its later 10-K (D403's design);
    - Reflection AI's decline (the main-part class);
    - the D414 code-set day, flagged by Codex alone in both arms alike.
- **Either counting: closes, on one item.** MIIT v2 d2 writes "Chinese firms, such as Alibaba and ByteDance" and does not list the
  named buyers' approval as not judged. Both frozen answers listed it.
  - Codex calls it material `condition_lost`; Claude calls it sound.
  - The event is not a binding obligation, so the changed clause does not govern it. It is the listing variation already seen on this
    topic in the astra review (split reviewers there too).

**Verdict under the rule fixed before: inconclusive** ("the reviewers disagree on a deciding item"). No third reader is added after
the result.

**What it shows:**
- The clause change does what it was built for. On one deal in two forms, the completion date follows the topic (4 of 4 against
  0 of 4), with every date control unchanged.
- The one blocking item is an unrelated listing variance that the registered rule counts.
