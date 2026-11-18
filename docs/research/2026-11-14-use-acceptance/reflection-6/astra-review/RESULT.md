# Astra's 51 written questions, reviewed against their sources at $0 (D635)

**Method:**
- **First reviewer:** a fresh read-only Codex reviewer read every question against its topic and article (`reviewer-codex.jsonl`).
- **Second reviewer:** a Claude subagent read the 13 flagged questions and 8 sound ones, mixed and blind
  (`reviewer-claude-second.jsonl`, `compare.txt`).

**Confirmed by both reviewers: 11 material defects in 51 questions.** None is counted by gate 1's hard lines.

| Class | Questions | Mechanism (request line, decision) | Gate readers' marks |
|---|---|---|---|
| **A signed deal's completion due at the next annual filing**, cutting the topic's window | Hugging Face × 4 (fortnight c1/clean-6 × 3, week c1/clean-5 × 1) | Request line 23: "for an obligation already taken on, its next annual filing". D210 wrote that rule for the *amount* an obligation reaches ("a financing_amount question on the amount … at the company's next annual filing"), not for a completion event. | Both families fail D on all 4; D is not a hard line |
| **An event due at period end, before the material that settles it is published** | Vera Rubin × 3 (fortnight c1/clean-4) | Request line 22, "period_end when it is the last day of the period", against line 20, "on or after the day the material that settles the question is published". The topic says it is settled by the FY2027 10-K. | Both hold D: the brief allows period_end |
| **"This quarter" widened to the fiscal year-end** | Rubin × 3 (week c1/clean-7) | The model's choice. The topic gives the Q3 and Q4 reports as check dates and asks whether the ramp happens in the quarter named. | Codex fails D on 2 |
| **An invented measure** | Memory × 1 (week c1/clean-3) | The model's choice: "equal-weighted mean of … matched … quotations", defined by neither the topic nor the article. | Both hold |

- **Split between the reviewers** (not counted): two "Alibaba and ByteDance as examples" conditions. The second reviewer called one sound
  and the other immaterial.
- **Found by the second reviewer alone** (not counted, one reader): purchase commitments (fortnight c1/clean-2 d2) with a top band
  starting at $100 billion against the $279 billion last disclosed.
- The first reviewer missed it, so its 38 "sound" verdicts are an upper bound.

**Census of the same topics across every stored draw** ($0):
- **Hugging Face, fortnight** (stated check date 24 March 2028): luna used the stated date 3 of 3 times. Sol and astra used 2027-02-28
  6 of 6 each. The stronger models apply line 23 literally.
- **Vera Rubin:** every model used 2027-01-31 (period_end) in 11 of 12 sends.
- **Rubin:** mixed (Jan 31, Feb 28, Nov 30) across all models.

**What it changes:**
- "No agreed hard-line mark on 51 ladders" does not mean sound questions. About 1 in 5 of astra's written questions has a window or
  measure that would make the judge record the wrong thing.
- 7 of the 11 trace to two sentences of the frozen request:
  - line 23 is wider than D210's scope;
  - lines 20 and 22 contradict each other.
  These sentences act on every model, and the frozen step uses them in production.
- The gate's six lines do not count due days, so gate 1 cannot see this class.
