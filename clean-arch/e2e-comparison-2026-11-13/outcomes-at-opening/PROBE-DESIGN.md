# Does writing the outcomes at opening reshape Step 1's theses? Probe design (choice 2 of D477; council round 24, D439), 2026-11-13

**What it can decide.** Whether the first step, required to write each new thesis's one settling figure or event and its fixed outcomes
when it opens it, opens the matters the readers found reachable in a shape that can be laddered, stops opening matters that should not be
questions, and does not stop opening the questions it opens today. A pass sends choice 2 to a council decision on a forward Stage A-style
measurement; a failure (suppression, as c15yc and c17 did, or no reshaping) falsifies choice 2 on this evidence and leaves choices 1 and 3.
It changes no final answer by itself.

**Source.** The signed standard defines a thesis as "一个问题句、一组结果档、一个到期日，写下后不改" and its opening test asks "有一个日期和一份公开材料能把答案放进
事先固定的档吗？没有就重写问题"; §3 gives the outcomes per reason ("量，五档"; "还没签：是非两档"; "事件，五档或两档"); "结果档可核对、不重叠、不留缝，到期恰好一档成立；中间一档写明和什么比";
"标的问题的档描述业务结果；主题问题的档只写结局，不写好坏". D417 (Alex: "确认：这类题不出题") for the rolling window. The clean path moved the outcomes to a later
step (D396); this candidate gives the opening step the standard's own test back, as an output contract, not a sentence.

**The candidate c19** (`clean-arch/step1-unfiled-2026-11-08/arms/c19-*`, version 3): c8's system text and closing check unchanged; the schema
adds two required fields to each new thesis, after `period`: `settles_on` ("one quantity for one period, which may be its change against a stated
earlier period (a calendar year against the year before), or one event checked by a date (which of its states it has reached by then). If no
date and public material can place the answer in fixed outcomes, rewrite the thesis; if it cannot be rewritten, do not propose it (whether its
statements are kept is judged as evidence, section 4)") and `outcomes` (2 to 5 strings: "five ranges of that quantity or of its change, or the
event's states, five or two (two for a yes/no, such as whether an unsigned deal is signed by the check date); checkable, not overlapping and
leaving no gap …; a middle range says what it is compared with. A company thesis's outcomes describe the business result, even when a policy
drives it; a theme's … describe only the result"). Schema 7,646 → 8,970 characters; the growth is the output contract itself. Blind audits:
version 1 (`audit-c19-blind.md`: narrowed a change to one figure, an unsourced multi-figure rule, "its statements are evidence", every policy
treated as a theme), version 2 (`audit-c19v2-blind.md`: all resolved except "whether it has happened", which narrowed five-state events; fixed in
version 3). Preflight ($0, `preflight-outcomes.output.txt`): on all 18 stored states the stored c8 answer passes c8's checks, without the new fields
it is refused by c19's schema whenever it proposes a thesis, and with them it passes every runner check. The required `scripts/preflight.py` was run (`preflight-script.output.txt`, exit 0): it replays production's
extraction (v74i), matching and judging archives and does not cover the clean Step 1 request; the 18-state check above is this probe's preflight.

**Cases** (`cases-outcomes.json`; `probe_identity.py` unchanged; three sends a case and arm; 108 jobs, about $1.56 estimated before the longer
outputs, a $4 reservation ceiling):
- *Reachable targets* (the full run's opening states, c8 exactly): c1 step 127 (the memory price over the 12 months to mid-2027, and the H100
  rental price, one article), c2 step 56 (memory contract prices with the rack's memory cost).
- *Should not be questions* (both readers, `reachability/RESULT.md`): c1 step 2 (the Intel stake, completed), c1 step 101 (Firmus, about $500m),
  c3 step 19 (US approval, a background sentence), c2 step 226 (custom-chip spending, no dated outcome), c1 step 76 and c3 step 112 (the China
  survey's rolling twelve months, D417). *Split:* c1 step 241 (federal obligations).
- *Guards:* capex-open d1–d3 (step 42), the memory states d1–d3 (step 56), Ohio d1–d3 (step 8): questions c8 opens today, and a yes/no case.

**Counting** (frozen; every answer read by Claude send by send; no automatic count):
- *Valid sends:* targets and should-not-open cases need all three sends valid in each arm (format and network failures are resent by the
  probe); guards need at least eight of nine per arm, compared as shares of valid sends. A required case below its minimum makes the probe
  inconclusive.
- *Ladderable, judged alike for both arms:* every new thesis of both arms on the target and should-not-open cases goes, with its question,
  outcome and period only (c19's two new fields removed), shuffled and arm-blind, to a reader (Codex, read-only) who marks it ladderable (one
  quantity or its change for one fiscal or calendar year or stated date, or one event with a check date) or not, and names its matter.
- *Outcomes' quality (c19 only):* a second blind read of each c19 thesis, shown its question, outcome, period, `settles_on` and `outcomes`,
  against the standard's lines: the number of outcomes (five for a quantity or its change; five or two for an event, two for a yes/no);
  checkable, not overlapping, no gap, exactly one holding on the check date; a middle range says what it is compared with; company or theme
  wording; and `settles_on` and the outcomes answer the thesis's own question for its own period and check date (not another quantity, period or
  event). A c19 thesis whose outcomes fail any of these does not count as reshaped.
- *Targets:* three matters (memory at c1-127, H100 at c1-127, memory at c2-56). A matter is **reshaped** when a thesis on it that the reader
  marks ladderable, with outcomes that pass, holds in at least two of c19's three sends, and a ladderable thesis on it holds in at most one of
  c8's. **Met:** at least two matters reshaped and no target matter opened in fewer c19 sends than c8 sends in any shape.
- *Should-not-open:* on each of the six, a new thesis on the marked matter. **Regression:** c19 in at least two of three and c8 in at most one.
  Every reduction is reported.
- *Suppression:* capex-open, a capex thesis; memory states, a memory-price thesis: c19's share of valid sends lower than c8's by a third or
  more (three of nine). Ohio, a thesis on the guarantee: reported. Either suppression line fails the probe.
- *Reading:* Claude reads every answer and checks both readers' marks against it; a disagreement is listed with its case.

**Verdict:** pass = targets met, no regression, no suppression; fail = otherwise; inconclusive as above.
