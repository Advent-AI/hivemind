# The postponed-event class, audited (D606's step), 2026-11-16, $0

`audit_collect.py` → `audit-answers.jsonl`: every event answer the frozen answer-choice step wrote in the stored gate-1 readings.
- Probe readings contribute their control sends only, by their sealed keys; changed arms, plants, and runs 2 and 3 before the frozen
  step are left out.
- That gives 246 answers shown, 195 distinct, over 43 topics.
- The census's "296" counted more readings' answers; this audit uses only the frozen step's own, which is the narrower base.

`audit-screen.txt` and `audit-class.txt` hold the timing ruling-outs, picked by a narrow screen: "will not … by/during", postpone,
defer, delay, "moved … to after". A sample of 12 unpicked decisions found one missed form ("moved … to after"), now added. The
result is 34 distinct answers (45 shown) over 7 matters, each read whole, with its rungs and every first and third reader's R and
reason.

## The matters

Counts are from one grouping, by the question's words (`audit-counts.txt`). An earlier table here was from a coarser grouping and
did not add up (council round 149).

| Matter (decider) | Distinct answers | Shown | First readers' R on the answers shown | Readers' reasons for a fail |
|---|---|---|---|---|
| Vera Rubin first shipments by 2026-12-31 (NVIDIA) | 10 | 15 | 12 both hold; 3 split (third readers: 2 both hold, 1 split) | "a delay rather than a decision against first shipments as a whole" |
| Vera Rubin volume shipments and revenue in FY2027 (NVIDIA) | 9 | 11 | 9 both hold, 1 split, 1 both fail | "can be a forecast of delay rather than a decision against the event", plus a W about the 10-K's day |
| Kyber NVL144 / Rubin Ultra first shipments (NVIDIA) | 8 | 11 | 9 both hold, 2 split | **another class:** the question asks "during 2027" but Yes says "by 2027-12-31" |
| Rubin volume ramp by fiscal Q4 FY2027 (NVIDIA) | 3 | 3 | all both hold | |
| Groq 3 LPX volume shipments in fiscal Q3 FY2027 (NVIDIA) | 2 | 2 | all both hold | |
| Hugging Face acquisition closing by 2028-03-24 (NVIDIA or Hugging Face) | 1 | 2 | both fail, twice (settled, no third reader) | "will not close by the date … a forecast of delay … the deal still pending" |
| Taiwan's export controls by 2027-01-31 (an authority) | 1 | 1 | split; both third readers fail | the wait (D420) |
| **Total** | **34** (company: 33 over 6 matters) | **45** (company: 44) | | |

## The whole rung, read as the judge and the page see it

In every answer, rung 1 states the event **with its date**. Examples:
- "NVIDIA begins shipping Vera Rubin by December 31, 2026 …";
- "NVIDIA reports Vera Rubin volume customer shipments with first revenue recognition on or before the end of FY2027";
- "NVIDIA completes the Hugging Face acquisition by March 24, 2028".

The Ruled-out rung is the model's decision followed by code's sentence: "This rung holds when that, or any other decision against the
event of rung 1 as a whole, … was made after <article day> and stands on <due day>, and only when rung 1 does not."

- **A company's formal announcement that the event will not happen by the due day** is a decision against rung 1's event as written:
  the dated event, as a whole. The reader brief's R row says the same: "the `Yes` condition is the event the question asks about; the
  first sentence of the `Ruled out` condition … is a decision against that event as a whole … and not the event's merely being still
  awaited".
  - **Qualified in round 149:** an announcement is not necessarily a decision. "It will not happen by the date" can be a forecast of
    delay rather than the company deciding against the dated event. Some dissenting reasons draw exactly that line ("can be a
    forecast of delay"), so it is too strong to say they all ignored the date. Any future reading keeps a forecast-versus-decision
    guard. The frozen step's sentences mostly name a decision ("formally announces", "formally decides to defer", "postponed"); some
    say only "announces that … will not …", which is where that guard bites.
- **A delay inside the deadline** cannot rule out: code's "only when rung 1 does not" and "stands on the due day" leave rung 1 to
  hold if the event happens by the due day.
- **A changed decision** that no longer stands on the due day does not rule out, by code's sentence.
- **A cancellation** rules out in every answer read.
- **An authority's proceeding** follows D420 and the brief's own clause: its formal abandonment or withdrawal rules it out, and its
  going on is the wait.
  - Taiwan p3's "will not adopt … by January 31, 2027" names a timetable while the proceeding goes on. That is the wait, so it is a
    misapplication.
  - It is one send of three; the topic's other two name abandonment or withdrawal.
  - The model's own account is on record (`taiwan-account-output.txt`): it carried the deadline into the decision.

## What it gives

- **No general model error is shown in the company-delay class.** Across 6 company matters (33 distinct answers), the frozen step's
  ruling outs read as decisions agree with rung 1's dated event, code's sentence, D409, D416 and the reader brief. The open edge is
  forecast against decision, not a missing rule.
- **D606's provisional reading misstates these questions.** That reading was "a formal postponement where the event remains possible
  reads Still open". Read against the undated event, it would leave a dated question "Still open" after its date while the company
  has already announced it will not happen by then. **By D606's own reversal condition** ("if worked cases show it misstates the
  question an analyst holds"), the reading is reversed:
  - for an event with a due day, the event is rung 1's, with its date;
  - a decision that it will not happen by the due day, standing on the due day, rules it out;
  - an authority's proceeding follows D420.
- **The authority kind is one isolated misapplication** (Taiwan p3, one send of three).
- **By D606's criterion the route closes,** since it found only isolated misapplications and no general rule is missing. Line 3 stays
  unmet on the fresh week by that one send.
- **Found on the way, another class, not pursued here:** two Kyber answers whose Yes ("by 2027-12-31") is wider than their question
  ("during 2027"). That is a question-to-rung window mismatch (the Q and R marks), 2 answers on 1 matter.
- **My error:** in round 148 I proposed "Still open" as my lean. My recorded lean on Alex's page (D591) was the opposite, "rules out",
  and I did not say I had changed it. The audit supports the D591 lean.
