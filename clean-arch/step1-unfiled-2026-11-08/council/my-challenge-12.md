# Reflection council "my", round 13: the same-day candidates traced against D375; review, and decide on one stored-data proof

D521 recorded round 12. Corrected as you found, each checked in the stored run: the shipment target was written on 09-27 (article
184) and both RTX questions were judged that day; the association is told as an association; `e278` is a lead; the fiscal-2028
facts are "what the readers listed"; the decision page's sentence is rewritten; D375, which I had missed, is named as the decision
in force (my search for "same day" in the index did not reach a row titled "Read the latest committed research library before each
item").

## The same-day trace (`duplicates/same_day_pairs.py`, `same-day-pairs.json`; the section of that name in `DUPLICATES-RESULT.md`), $0

Ten candidate pairs in four stored runs (questions sharing a research group, opened the same day; leads, not a census).
- Six are two questions opened by one article (two years of one measure, or two measures): not the matter.
- Four are different articles of one day opening questions on one matter, the earlier committed and open first:

| Case | The later article's stored reading request | The later comparison |
|---|---|---|
| fresh week 09-24, Rubin shipping (`v9`, `v11`) | printed all 8 questions open at the day's start, not `v9` | compared with `v9`: "the same question for another period"; opened |
| fresh week 09-27, RTX (`v14`, `v15`) | printed all 13, not `v14` | **not compared with `v14`**; opened |
| July run 2, 07-09, H200 (`v10`: "Will China permit Alibaba, ByteDance, and DeepSeek to buy H200 by 2026-12-31?"; `v11`: "What stage will China's individual-approval process for H200 purchases reach by 2026-12-31?") | printed all 9, not `v10` | compared: "different"; opened |
| July run 3, 07-01, credit support (`v1`: "What amount of credit-support obligations will NVIDIA report under its AI-cloud program at its next annual filing?"; `v2`: "How much financing and credit support will NVIDIA have committed to AI cloud providers by its next annual filing?") | the first day: no question to print | compared: "a distinct question on the same matter"; opened |

So the visibility gap at reading is confirmed in four of four (the behaviour D375 replaced on paper), and the later comparison kept
the pair apart in three and never made it in one. Both reviewing teams called the two fresh-week pairs duplicates; the two July
pairs are unread by reviewers. Rule on those two if you will: one matter asked twice, or not.

## The proposal: one D375-aligned proof on stored requests (a new arm; this round is its review before any send)

**The question it answers:** when the article that opened the second question is read with the first question on its list, as D375
decides, does the reading step file its statements under the first question and propose no second one?

- **Cases:** the later article of each of the four pairs. Feasibility checked at $0: each stored reading request (frozen reading
  prompt v74i, gpt-6-luna, low effort; about 17,500 characters) prints open questions as two lines each ("  - v14
  (chip-export-controls, due 2027-01-31): <question>" and its "takes:" line), and the system itself printed the earlier question's
  two lines verbatim in a later request of the same run. The July run 3 case has an empty list in the stored request; it is
  included only if the list's own empty form can be replaced by the form the next request uses, else it is left out and said so.
- **Arms:** control, the stored request rebuilt and matched to its archived key, sent as stored; changed, the same request with the
  earlier question's two lines, exactly as the system printed them later, added at the end of the open-question list. Nothing else
  differs: prompt, schema, model and settings are the frozen reading step's. Three sends an arm a case: 24 calls (18 without the
  July run 3 case).
- **Read by code, then by me, raw answers beside the article:** in each answer, (a) is a new question proposed on the pair's matter;
  (b) which statements are linked to the earlier question. The answers are not put through the store's later checks (the store is
  at its end state); that is a limit.
- **Written before the send:** the control proposes the second question in at least two of three sends in each case, or that case
  does not reproduce and is set aside. **Prediction:** with the earlier question listed, no second question on the matter in at
  least two of three sends, and at least one statement linked to the earlier question, in at least three of the four cases (two of
  three if a case is set aside). **It fails** if the second question is still proposed in most sends of two or more cases: then
  listing the earlier question is not enough, and the comparison step is where the pair is kept apart.
- **Cost:** about 5,000 tokens in and a few thousand out a call at $0.10 and $0.50 a million: about $0.10 in all; ceiling $0.50;
  one HTTP attempt a call; every reply saved before it is read.
- **What it cannot show:** that the questions' answers would differ; how the whole day would run with per-item lists (later
  articles, the comparison step, re-sent requests); anything about adopting D375, whose "implementation and acceptance" Alex
  left pending and which stays his.

Attack the design (is adding two lines a faithful stand-in for D375's list; is the prediction fair; what must be fixed before
a send), or say that the trace should be recorded and the path closed here instead.

End with: "Council position: <...>".
