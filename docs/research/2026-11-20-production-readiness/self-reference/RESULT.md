# The self-made market reference: class, mechanism and share (D692; 2026-11-21; $0)

Asked by D692: "the self-made reference is traced apart on stored answers, at $0". Nothing was sent and nothing changed.
Census: `reference_census.py` → `reference-census.md` (the three finished poc-v118 draws, read-only; positive control old-2 v9 on
2026-09-15 is marked).

## The class
judging-v7 asks every judgement for a `reference`: "what the market expects for this question (consensus, the company's guidance, the
stated plan or deadline)". Over the number questions of the three draws (54 questions, 2,375 judgements that have a previous one):

| draw | the reference's first figure is in no part of the request outside the previous conclusion | of which the reference says it was carried from the previous judgement |
|---|---|---|
| old-1 | 28 (3%) | 15 (2%): v1 credit support 9, v8 Data Center 5, v2 1 |
| old-2 | 55 (7%) | 29 (4%): v9 Data Center 28, v15 1 |
| old-3 | 11 (2%) | 0 |

The second column is the defect: a figure the system computed itself, presented the next day as the market's ("The carried-forward
market-reference proxy is about $372.5 billion", old-1 v8; "Market consensus is approximately $372 billion, the reference supplied in
the previous conclusion", old-2 v9 on 09-12). The rest of the first column, read on a sample (old-1 v2, old-2 v1 and v2, old-3 v33),
is mostly a reference built from disclosed company figures and labelled as such ("No consensus ... is supplied. The closest disclosed
reference is the $8.38 billion subtotal of the $3.5 billion ... and Sharon AI's $4.88 billion"): not the defect. The strict class is
small (44 of 2,375, 1.9%) but it sits on the FY2027 Data Center question in two of three draws, the question council Q read first, and
it lasts: in old-2 from 08-16 to the end of the run.

## The mechanism, traced on old-2 v9 (every judgement 07-06 to 09-20 read)
1. **07-06 to 07-21:** "No market consensus or company FY2027 guidance is supplied"; from 07-10 it uses the closest company figure,
   the $91B Q2 total-revenue guide times the Data Center mix. Correct behaviour.
2. **07-22 to 08-15:** "No full-year FY2027 Data Center consensus or company guidance is supplied. The available annual run-rate
   reference is about $372B" (FY2026's $193.7B carried at Q1's 92% growth): its own calculation, still labelled as one.
3. **08-16 onward:** the request shows the previous conclusion as its rung and reasons only (`views/judging.py` line 157, cut at 800
   characters; the `reference` field is not shown). The reasons say "The reference is approximately $372 billion"; the next answer
   calls it "the market expectation stated in the previous conclusion" (08-18), then "Market consensus is approximately $372 billion"
   (08-28).
4. **09-14:** the reasons drop the $372B sentence and keep only "the approximately $414 billion forecast" (its own estimate since
   09-11, built on a SemiAnalysis H2 uplift). **09-15:** "Approximately $414 billion is the reference expectation". It stays to 09-20
   ("The market reference supplied by the previous conclusion is approximately $414 billion").

The request sentences: judging-v7 line 3 says "The previous conclusion is supplied only for comparison"; line 4 asks for "what the
market expects". No sentence says what to write when the material holds no market figure, and the previous conclusion carries no mark
of where its figures came from, so the judge's own figure re-enters as a given. Prompt-audit verdicts: **missing** (no case for "no
market figure supplied") and **misread** (the comparison-only previous conclusion used as a source); the model's own account was not
asked (a cent a case).

## Why the Data Center question had no market figure
The total-revenue question v14 cites a real one from 09-14: "The latest cited Wall Street estimate is $411 billion (e4061)", then
e4097 and e4348. Those statements are filed under total revenue only (one home, D207), and v9 does not read v14: the 09-20 request for
v9 holds no "411" (`../dependency-probe/run/control-request-user.txt`). In the probe the linked request delivered v14's conclusion,
and one of the three linked answers dropped the $414B and derived its reference from the $411B (changed 1, `claude-marks.md`); the
other two kept "$414B", which their previous conclusion still stated.

## What would remove it (candidates, not decided; the judge is frozen, so each is a new version Alex opens)
| Candidate | What it does | Share of the strict class (these draws) |
|---|---|---|
| linking related questions (under review, `../dependency-design/`) | delivers the whole's market figure to the part | the Data Center cases, 33 of 44; not credit support (old-1 v1, 9). A carried figure already in the previous conclusion can still win (2 of 3 in the probe) |
| a sourced reference: the answer names the evidence or dependency its reference comes from, or states that none was supplied; code checks that the named source was shown (identity, not importance) | stops an own figure being presented as the market's, wherever it arises | the whole class by construction; unproven until sent |
| show the previous reference with a mark "our own figure" | a label on one path | a patch: the reasons text carries the same figure unmarked |

Next: this goes to the council with the dependency design review, then to Alex with it; no send before that.
