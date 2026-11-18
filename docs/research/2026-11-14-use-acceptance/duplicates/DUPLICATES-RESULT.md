# Do the old system's duplicate questions split the evidence? The trace of three pairs (D520, under D439), 2026-11-15, $0

Scripts: `build_pair_packets.py` (one packet a pair: each question's latest judging request exactly as its judge received it, and its
stored answer), `tally_pairs.py`. Readers: two families, one fresh session a pair each (Codex read-only: `codex-pair-*.jsonl`; Claude:
`claude-pair-*.jsonl`), given only `brief.md` and their packet. My own read of two pairs was written before any reader's file was
opened (`own-read-before-readers.md`). The run: the old system's fresh-week draw of D489. Nothing was sent to the pipeline's models and
nothing changed.

## The answer

**In each of the three pairs, both reader families listed facts that bear on one question and were shown only to the other question's
judge.** The two RTX answers and the two Rubin answers are "yes"; the two revenue answers each chose their own second band (the
bands are in different units, an amount and a growth rate). Whether any answer would change with the missing facts was not tested.
One association is on record: in the RTX pair, the answer without the shipment target is the one a separate reader had earlier
marked "unsure" about the deadline.

This is a reading of three pairs in one week of one run. The counts below are what the readers listed, not established losses and
not a rate.

## The three pairs

| Pair | Statements shown to each judge | Facts both families say are missing from one request **and** bear on its question | The two answers |
|---|---|---|---|
| **Beijing's approval of RTX Pro 5500 purchases** (`v14`, last judged 09-28; `v15`, judged once, 09-27) | 8 and 3; none in common | 3, all missing from `v15`: **Nvidia aims to start shipping to China in late December 2026, about 500,000 units a quarter (`e331`)**, the clearest; some industry executives expect the chip to escape U.S. export limits (`e284`), relevant by inference; "neither Beijing nor the companies confirmed the plan" (`e278`), which stands in the stored summary and not in the quoted passage printed beside it, and `v15`'s own answer already calls its reports unverified: a lead until the article is checked | Both "yes". `v14` cites the shipment aim; `v15` says the report "gives no approval date". |
| **Vera Rubin shipping** (`v9`, `v11`; both last judged 09-28) | 13 and 6; 5 in common | 4, all missing from `v11`: orders from every large customer, about 20% of data-center revenue in the third quarter, the fourth-quarter outlook, the inventory build. Each corroborates; the deciding fact (production shipments began in August 2026) is in both requests | Both "yes", on the same fact. |
| **Fiscal 2028 revenue, as an amount (`v3`) and as growth (`v5`)** (both last judged 09-28) | 47 and 39 of 43; 19 in common | 16: 4 missing from `v3` (a 66% market growth estimate; that the 70% outlook is the company's first year-ahead guidance; a view that growth will beat it; a projected 44% share of the largest cloud companies' spending) and 12 missing from `v5` (a rival's platform ramp and two large customers' plans to use it; a supplier's statement that memory stays tight until 2028; one buyer's plan to use only Nvidia chips and its capacity target; a cost per gigawatt; the chief executive's "double the chips sold in 2027") | Each its own second band, at the bottom edge ($700 billion against a floor of $692 billion; 70% against a floor of 70%). Four statements linked to `v5` were not printed in its request, so the readers could not assess them. |

How the families compare: on RTX they list 4 and 6 facts and agree on 3 that bear; on Rubin 8 and 8, agreeing on 4 (Codex says all
8 bear, Claude 4); on fiscal 2028, 34 and 29, agreeing on 16 that bear (Codex 31, Claude 16). Codex marks nearly everything as
bearing; the figures above are what both families say. My own read, written first, found the shipment-timing fact in the RTX pair
and called the Rubin facts not answer-bearing "once shipping has begun"; both families weigh them as corroboration, so that pair is
"corroborating facts missing, the deciding fact present", not "nothing missing".

**The recorded association (RTX), corrected after the council's round 12.** The shipment target was written at article 184 on
2026-09-27 and linked to `v14` only. Both questions were judged that same day, at article 186: `v14`'s answer cites the shipment
target, `v15`'s does not and says the report gives no approval date. (`v14` was judged again on 09-28; `v15` was not. My first
wording, that the report arrived on 09-28, was wrong.) Before the week's reading a separate reader had marked `v15`'s "yes"
**unsure** ("nothing ties approval to before 31 January 2027") and `v14`'s **supported**, citing the shipment aim
(`week/control-confirmation.jsonl`, candidates 5 and 1). This is an association: it does not prove that the target alone would
have changed that reader's mark or either answer; a shipment aim is indirect evidence about approval; and the two questions are
worded differently (Alibaba and ByteDance; domestic firms).

## Why each second question was opened (the stored matching records)

| Second question | What the record says |
|---|---|
| `v15` (RTX, "domestic firms") | Compared with thirteen open questions; **the first RTX question, opened twelve articles earlier the same day, is not among them**, though the new question was put in the research group the first had just created. Both are questions on a theme, not on the company. A lead, not a traced cause: the reading request of that article printed only the questions open at the day's start (section below), and the matching step also assembles its own candidates. |
| `v11` (Rubin by the end of 2027) | Compared with the first Rubin question and ruled "the same question for another period": a later deadline was treated as another period, which opens a question of its own. |
| `v5` (fiscal 2028 growth) | Compared with the amount question and ruled "a distinct question on the same matter". |

Three pairs, three different reasons. None is the case of D354's known defect (one request about H200 re-sent ten times), and no
rate follows from them.

## The same-day candidates of four stored runs, against the stored records (D521, $0; `same_day_pairs.py`, `same-day-pairs.json`)

A decision already covers this ground, and I had missed it until the council's round 12: **D375 (Alex, 2026-11-05) replaced the
once-a-day list of open questions (D251) with "the questions committed before that item, including questions opened earlier the
same day"; its implementation and acceptance are pending, and the default system still reads the day-start list.**

Candidates are pairs of questions that share a research group and were opened the same day: ten in the four runs (a list of leads,
not a census of duplicates).
- **Six are two questions opened by one article** (two years of one measure, or two different measures): not one matter asked
  twice, and not a matter of what a later article could see.
- **Four are two questions opened by different articles of one day**, the earlier committed and open before the later article:

| Run, day | Earlier and later question | Did the later article's reading request print the earlier question? | Was the earlier question among those the new one was compared with? |
|---|---|---|---|
| fresh week, 09-24 | Vera Rubin shipping by 2027-01-31; Rubin GPUs shipping by 2027-12-31 | No (it printed all 8 questions open at the day's start) | Yes: ruled "the same question for another period", opened |
| fresh week, 09-27 | RTX Pro 5500 for Alibaba and ByteDance; for domestic firms | No (all 13 of the day's start) | **No**: compared with those 13 only; opened |
| July run 2, 07-09 | "Will China permit Alibaba, ByteDance and DeepSeek to buy H200 by 2026-12-31?"; "What stage will China's individual-approval process for H200 purchases reach by 2026-12-31?" | No (all 9 of the day's start) | Yes: ruled "different", opened |
| July run 3, 07-01 | "What amount of credit-support obligations will NVIDIA report under its AI-cloud program at its next annual filing?"; "How much financing and credit support will NVIDIA have committed to AI cloud providers by its next annual filing?" | No (the first day: no question at its start) | Yes: ruled "a distinct question on the same matter", opened |

What the records establish: in all four, the article that opened the second question was read without being shown the first,
which is the behaviour D375 decided to replace. That is not what let the second question open (next section). In three of four the later check did compare the two and kept them apart, each
with a different verdict; in one it did not compare them. Whether each pair is one matter asked twice: both reviewing teams said
so for the two fresh-week pairs; the two July pairs have not been read by reviewers (they read to me as one matter each).
Not established: that showing the earlier question to the reading step would have prevented the second question (not tried); a
rate.

## Where each second question was let through, traced in the code and the stored records (D523, $0)

Two facts I had not read when I designed a probe of the reading step (the council's round 14 found the first):
- **The reading step is told to propose a question even when it is already open:** "a question that is already open is folded into
  it by code afterwards, so propose it when the item raises it" (`prompts/role-v74i.txt`). So a second proposal is by design; whether
  a second question opens is decided by the comparison step that follows.
- **The comparison step compares a new candidate with** the questions that share its typed key or, only when none does, the hits of
  a text search, **plus the questions on the article's list**, which is the day-start list (`views/matching.py`, `build_lists`;
  `views/jev_matching.py`, `decide`).

| Second question | What happened, by the stored record and the code run on the stored run |
|---|---|
| RTX for "domestic firms" (`v15`) | **Never compared with `v14`.** Its candidate had a key match (the theme's Blackwell question, `v6`), so the text search was skipped; `v14` has another typed key (another kind of event, another wording of the scope) and, opened earlier the same day, was not on the day-start list. The same text search run on the stored run as it stands at the week's end returns `v14` first (that ranking is not proof of what it would have returned at article 175). With the per-article list D375 decides, `v14` would have been on the comparison list, and the code's own conflict check does not bar joining the two (`identity.conflicts` returns no conflict, the council's check); what the comparison would then have ruled is not known. |
| Rubin by the end of 2027 (`v11`) | Compared with `v9` through their shared key, and ruled "the same question for another period": the two deadlines are eleven months apart. |
| Fiscal 2028 growth (`v5`) | Compared with `v3` through their shared key, and ruled "a distinct question on the same matter". |
| The two July pairs (not read by reviewers: not confirmed duplicates) | Both compared, and ruled "different" and "a distinct question on the same matter". |

**A count of recorded openings, by code on the four stored runs** (`not-compared-census.json`; the counting was done in the session
and its script was not kept, so the figures are a lead until `d375` work below re-derives them): of 54 questions opened, 17 were
opened after another article of the same day had opened a question; in 3 of those an earlier same-day question on the same subject
was not among those compared; one of the three is a pair both reviewing teams called duplicates (`v15`), the other two are
different matters. This is not a rate of duplicates. One pair both teams called duplicates was opened without that comparison; what
the comparison would have ruled is unknown. The fresh week's other two pairs were compared and kept apart by the frozen comparison
step.

**The probe of the reading step is withdrawn** (`VISIBILITY-PROBE-DESIGN.md`, not sent): its pass condition, "no second question is
proposed", contradicted the frozen prompt, and the opening is not decided there.

## What this result may and may not be said to show

- Shown, for three pairs of one run: facts that both reader families list as bearing on a question were shown only to the judge of
  its duplicate; the two RTX answers and the two Rubin answers are "yes" and the two revenue answers each chose their own second
  band on different scales; in the RTX pair the answer without the reported shipment target is the one a separate reader had
  marked unsure about the deadline (an association).
- Not shown: that any answer would change with the missing facts (not tested); a rate of duplicates or of split evidence; that the
  day-start list is the cause of any pair (the reading requests confirm the earlier question was not shown; the effect of showing
  it is untried); anything about the new system beyond
  the week's count (both reviewing teams found no duplicate among its seven questions); which system carries forward.
