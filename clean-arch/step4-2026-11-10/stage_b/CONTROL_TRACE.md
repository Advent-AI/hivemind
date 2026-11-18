# Where Stage B's controls were lost: a trace of 11 controls ($0, 2026-11-12)

Council B's next step (`council/la-codex.md`): trace the 8 controls excluded on the question and the 3 eligible controls with
part of reader B's material not shown, from the opening article to what the judge saw, and record where each difference first
appears. Sources: the Step 1 theses (`clean-arch/unseeded-2026-11-10/opened-u*.json`), the pairing records (`match-u*-*.jsonl`,
rule `MATCHING-v2.md`), the ladder question and due day and the control readers' rows
(`poc/data/clean-stage-b-reading-2026-11-12/controls-*`), and the draws' stored records and links
(`poc/data/clean-stage-b-2026-11-11/draw-u*/views.sqlite`, read-only). No model call. Checked by a second reviewer
(`council/lb-codex.md`: stands with corrections, applied here).

**Answer.** Several of the question differences are already in the Step 1 thesis: it asks the article's own angle on a matter (a
programme inside a total, the article's reported new date, a later milestone), and the ladder step keeps it. Two controls are
missing exact statements that Step 1 extracted and stored with no link to any thesis. The pairing's deliberate breadth and the
ladder step's wording also shape the comparison, and the third missing statement is not traced to a record. This is a lead for
the Step 1 diagnosis (D432), not an established attribution of every lost control to Step 1.

## The 8 excluded on the question

| control | ruler question | the Step 1 thesis asks | where the difference first appears |
|---|---|---|---|
| u1/clean-1, q09 | NVIDIA's total financing commitments and capacity backstops at FY2027 year-end | credit support to AI cloud partners under the new model | **in the Step 1 thesis** (one programme); the ladder keeps it. The pairing counts a programme inside a total as the same matter (D248 boundary 1), so whether this is a Step 1 fault or the comparison's breadth is a separate decision |
| u3/clean-1, q09 | as above | as above | as above |
| u2/clean-7, q16 | cloud providers' custom AI silicon spend in 2026 | the big four's custom accelerator spend in 2026 | **in the Step 1 thesis**: four named companies, one of them (Meta) outside "cloud providers", so not simply a part of the total |
| u3/clean-7, q18 | Rubin Ultra in Kyber racks ships by 2027-12-31 | Kyber "reach first shipments in 2028" (the article's reported date), and whether NVL576 ships in volume | **in the Step 1 thesis** (the article's date); the ladder asks "during calendar 2028", due 2028-12-31. The pairing readers disagreed (one held NVL576 volume a separate check) |
| u1/clean-6, q18 | as above | Kyber in 2027 "or slip to 2028"; period "2028" | **both**: Step 1's period (2028) became the ladder's due day 2028-12-31; the ladder's "during calendar 2027" adds a restriction "by the end of 2027" does not have (third readers split on it) |
| u2/clean-3, q08 | Chinese authorization for companies to import H200 by 2027-01-31 | Beijing allows NVIDIA to sell H200, settled by an announcement or by NVIDIA disclosing China sales or shipments | **in the Step 1 outcome** (NVIDIA's own disclosure can settle it without an authorization); the ladder keeps it. Both third readers: not comparable, for different stated reasons |
| u3/clean-5, q08 | as above | will NVIDIA "actually resume selling" H200 into China, "i.e." will Beijing permit buyers | **in the Step 1 outcome** (sales taking place); the pairing readers disagreed on which wording controls |
| u1/clean-11, q08 | as above | China approves H200 imports, and how many | **the ladder step's wording** for the company-scope difference the readers tested ("at least one Chinese AI firm" for "any Chinese company"); disputed, third readers split |

## The 3 eligible with material not shown

| control | reader B's missing item | the exact statement in the draw's records? | linked to any thesis? |
|---|---|---|---|
| u1/clean-4, q13 (2027 capex) | i090: analysts project NVIDIA revenue +82% this year, +41% next | **yes**: e86 (created with the capex thesis, same step 42), e131 (step 60) | **no** |
| | i143: about half of 2027 data-centre spend goes to memory | **yes**: e145 (step 63, after the thesis opened) | **no** |
| u3/clean-6, q13 (2027 capex) | i090 | **yes**: e88 (step 42, with the thesis), e135 (step 60) | **no** |
| | i143 | **yes**: e149 (step 63) | **no** |
| u2/clean-4, q04 (2026 capex) | i295: NVIDIA management, relayed by Morgan Stanley, describes "accelerating growth rates" as quarterly revenue approaches $100bn | **not found**: its source article (`gnews:ecde98f04e1a057b56113670`) left no record in the draw; whether it was read is not traced. Related statements from other articles are stored unlinked: e400 (Morgan Stanley after meeting management; revenue approaching $100bn, without "accelerating growth") and e392 (an $82bn quarter, a third quarter of accelerating growth) | (the related ones: no) |

The FY2027 consensus records (e265, e341; e266, e336) are related context and do not carry i090's 41% next-year forecast.

**Timing matters for which decision failed.** i090 was stored by the same Step 1 call that opened the capex thesis (step 42):
that call opened the thesis and kept the statement unlinked. i143 arrived later (step 63), when the thesis was already open:
that call filed it under no thesis. The design's later link (PRD, "The later link when a thesis opens") judges earlier unlinked
material when a thesis opens; it does not cover either case. A link-based request then leaves them out; the trace does not
separately prove every detail of request building.

## What this gives the Step 1 diagnosis (D432), as leads

1. **The thesis is written from the article's angle.** A programme inside a total, an article's reported new date, or a later
   milestone becomes the question. The frozen standard treats these as one bet with the total, the original deadline or the
   decision (D248; AGENTS §8), and the pairing pairs them for that reason; they still cannot be compared with reader B's answer.
   Whether Step 1 should write the bet in its standard form, or the comparison should allow the narrower question, is a choice
   for Alex once the diagnosis is in.
2. **Indirect evidence is not filed to an open thesis.** Two of the three missing items are a supplier's growth forecast and the
   memory share of spending, kept unlinked although the capex thesis was open, once by the call that opened it and once by a
   later call.

No change is proposed here; the diagnosis and one change go to Alex before any build.
