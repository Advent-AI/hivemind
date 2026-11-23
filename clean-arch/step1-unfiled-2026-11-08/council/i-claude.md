# Decision council: a sourced lever found in the signed filing rule (read-only)

You rejected u1r: four rulings turned into a rule Alex did not make. Agreed. Stepping back, the evidence says K6b's errors against
Alex's rulings are mainly **link misses**:
- gross margin (d1-40) and the EPS forecast (d1-66) left unfiled while the revenue thesis clean-11 was open;
- small supply theses opened (d2-8);
- the cash drop (d1-57) is already right.

**Source found: the filing rule in force** (`docs/DECISIONS.md` "Filing", D207, D254, D259, D264, D265, D268, D273, kept by D361;
production text `src/hivemind/placement.py` `FILING_RULE_ROOT_FALLBACK`). A statement goes under the narrowest open question:
- "it bears on, as that question's own figure, step or estimate or through the demand, supply, competition or pricing behind its
  answer, never a broader question beside it";
- "an estimate for another period or population of a question's quantity goes under it when no open question covers that period";
- the fallback: "when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the
  company's results goes to the company-wide revenue question of its period".

K6b's §2 (`k6b-system.txt` ll. 54–62) dropped the four-channel definition of "bears on" and the fallback. It has only "narrowest thesis
that covers it", "match by the underlying question", and a softer period clause.

**Against Alex's rulings:**
- margin → the revenue question's own measure or results: link; this matches;
- the EPS forecast → an estimate for another period: link; this matches;
- cash → neither the question's own figure nor a channel: drop; this matches;
- small supplier → the fallback would file it under revenue, but Alex said drop. **Conflict.** The E1 diagnosis also found the
  fallback makes a parking lot.

**Proposed lever L-file:** replace K6b's §2 matching sentences (ll. 54–62) with the signed rule's definition: own figure, step or
estimate; the four channels; never a broader question beside it; the estimate-for-another-period clause. **Without the fallback**,
because of the supplier conflict and the parking lot, and because the clean library has no guaranteed company-wide revenue question
(D370).
- Source: D273 and D361, the signed production text. General wording, and no company.
- About length-neutral, since it replaces lines.

**Probe 3:**
- k6b reuses probe 1's draws; L-file is new: 16 cases × 3 = 48 sends, about $0.60.
- Readers: Codex and Claude, given Alex's four rulings as worked cases.
- Calibration check (your point): before scoring, both readers judge 6 other preselected dev items, not Alex's, against the signed
  rule. Their agreement is reported.

**Pass:**
- link misses on the financial cases (unfiled items that both readers, or the adjudication, place under an open thesis) down by 2 or
  more;
- wrong links not up;
- theses not up;
- ruler noise at most 11;
- format all pass.

Challenge:
- (a) Is restoring signed text legitimate?
- (b) Is dropping the fallback right?
- (c) The criteria?

Under 250 words.
