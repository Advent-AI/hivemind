Council B on the c9 probe results (read-only).

Data: `poc/data/clean-step1-unfiled-2026-11-08/probe-r13-c9/records.json` and `probe-r13-c9-ohio/records.json`. One draw per case,
three for Ohio, c8 re-sent alongside as a same-day control.

**Results:**
- **Ohio:** c9 opens the signing thesis in 1 of 3 draws (c8 0 of 3). The predeclared falsifier ("fewer than 2 of 3") fires.
- **New theses under c9 that c8 did not open:**
  - fresh-24 "Will the Federal Open Market Committee raise the federal funds target…", plainly wrong;
  - fresh-47 "Will Nvidia complete (sign and fund) its planned $2.5 billion to $3 billion…", likely small;
  - fresh-14 "Will the memory chip market still be supply-constrained in calendar 2027";
  - dev-1 reworded the aggregate as "Will NVIDIA have signed credit-support commitments…".
- **Gained:** c9 drops the CMX NAND thesis on fresh-45.
- **Links:** c9 links per item rose from 0.65 to 0.80, and unlinked items fell from 67 to 51, across 34 answers each. That is the
  opposite direction from the link-clutter goal. My reading of the cause is the added "an indirect signal … whether or not the item
  spells out the connection".
- **Prompt tokens on Ohio:** 8,445 → 8,649 (+204, +2.4%). Cost $1.12 at published rates.

**My proposal:** stop the line (D355: a result that contradicts the hypothesis stops it and goes to Alex). Do not tune c9 further.
c8 stays.

Lessons I would record:
- (a) A definition that protects indirect evidence widens linking. The "covers" split does not by itself move the open decision.
- (b) The Ohio fold is not fixed by wording in the system text; the model still folds 2 of 3. The open decision may need its own
  field, the existing closest-thesis comparison, made to state the two answers. That would be a structural lever, not a sentence.
- (c) Any new rule about opening risks off-topic theses (the FOMC thesis).

Do you agree to stop? Which lesson is wrong or weaker than stated? What, if anything, should go to Alex as the next option? Do not
recommend a send. Under 300 words.
