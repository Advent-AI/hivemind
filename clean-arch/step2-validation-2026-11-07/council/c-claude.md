# Council B: reference built, retrieval scored, and a problem in the reference (read-only)

Data is in `poc/data/step2-validation-2026-11-07/`: `reference.json`, `retrieval.json`, `label-answer-*`, `adjudication-answer.json`.

**Reference.**
- 573 pairs, from 488 triage-possible pairs, 66 scan-flagged pairs and a 60-pair unflagged audit.
- Two blind passes agree on 94.9%; 29 disputes were adjudicated by a third reader with the source.
- Labels: repeat 397, revision 27, different 136, same quantity other party 7, insufficient 6.
- 121 of 282 items have at least one true repeat or revision earlier (424 positive pairs). Only 3 positive pairs are cross-thesis.

**Retrieval** (recall at 10, strictly forward):

| | Items with a counterpart found (121) | Positive pairs (424) | Exhaustive-sample pairs (40; 6 missed by the candidate routes) |
|---|---|---|---|
| R0 production, within thesis | 118 | 362 | 38 |
| R0e word overlap, entity-wide | 114 | 328 | 35 |
| R1 embedding with thesis | 121 | 368 | 38 |
| R2 embedding, evidence only | 120 | **388** | **39** |

**Problem.** The readers marked 313 of 397 repeats "richer". I hand-checked 6 at random; 2 are not repeats at all:
- the Singapore police property order against the later charge of a CEO (two facts of one case);
- SharonAI's own backstop deal against NVIDIA's general model announcement.

Others are the same statement with different details, for example Q1 revenue with and without the data-centre figure. Both readers
are the same model family; agreement does not rule out a shared bias of reading "same story" as "repeat".

This decides Alex's rule (a repeat adds a source to the existing record): merging a "repeat" that carries new material facts loses
them.

**Proposal.**
1. Re-label every positive pair with the product question, by two fresh blind readers and the source, as one of:
   - **pure repeat:** nothing material in the later item that the earlier lacks; merging loses nothing;
   - **same statement plus new material detail:** a figure, condition, party or date the earlier lacks;
   - **revision;**
   - **different fact of the same matter;**
   - **different.**

   A third reader settles disagreements, and I hand-read a random 30.
2. Re-score retrieval on the corrected positives.
3. Jev J0 against J1 on the corrected labelled pairs (dry-run cost first), then on the retrieved R2 top 10.
4. Take to Alex the share of repeats that carry new material, and the options: add the source only; add the source and append the new
   detail to the existing record; keep a linked new record.

Challenge:
- (a) Is the re-label the right fix, or should the original labels stand, with "richer" read as a separate risk?
- (b) Is R2 beating R1 credible, given only 3 cross-thesis pairs?
- (c) What else would falsify the retrieval pass?

Under 400 words.
