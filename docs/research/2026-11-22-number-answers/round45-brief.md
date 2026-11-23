# Council round 45: why are the product's number answers unreliable? (independent investigation, read-only)

You are an independent investigator for a hedge-fund research pipeline. Work read-only and make no model calls. Read `AGENTS.md` in
full first; §1 (diagnose), §2 (design), §7.1 (the frozen ruler) and §8 (product thinking) govern. Report in English.

## The question from the owner, Alex

He wants this taken back to first principles, with an open mind. The product's number answers cannot be trusted:
- related number questions contradict each other;
- answers add overlapping amounts, use a figure of another scope, or step off a reference on unsupported arithmetic.

He wants to know which part of the pipeline's design produces this, from the code and the traces, not a patch. "The most important
thing is that we don't hallucinate with the numbers."

Treat every earlier diagnosis below as a lead, not as settled. Find the design choice or choices that produce the whole class.

## The product

`poc/config/poc-v118.json`.
- **Extraction:** one model call per article; it files quoted evidence under open questions and proposes new ones (`src/hivemind/extraction.py`).
- **Matching and writing:** `src/hivemind/views/jev_matching.py`, `writing.py`.
- **Judging:** once a day, one call per changed question, judging-v7 (`src/hivemind/views/judging.py`,
  `src/hivemind/prompts/judging-v7.txt`).
- **Pull mode:** closes questions at their due day.
- **Design documents:** `docs/prd/06-views.md` and `docs/prd/README.md`.

## The traces

Stores are finished runs; open them read-only with `?mode=ro`:
- `poc/data/comparison-2026-11-17/run/old-{1,2,3}/prod/` (`views.sqlite`, `archive.sqlite`): three draws of poc-v118 over 07-01..09-20,
  1,884 articles each.
- Tables: `judgements` (`rung`, `reference`, `implied_outcome`, `reasons`, `cited_evidence_json`, `call_id`), `views`, `rungs`,
  `evidence`, `evidence_links`, `dependencies`.
- The archive's `model_calls.request_json` holds each request exactly as sent.

## Earlier findings to test, not to trust

- **Cross-question contradiction** (`docs/research/2026-11-20-production-readiness/council-q/RESULT.md`): old-2 at 09-20 has Data Center
  (v9) Q4 at about $146B against total revenue (v14) Q4 at about $127B. It recurs in all three draws. No question has a dependency.
- **The 24 answers both blind readers rejected** (`docs/research/2026-11-20-hybrid/census/CENSUS.md`, `rejected-answers.md`), classed as:
  - O, overlap or double count;
  - S, a figure measuring something else;
  - E, an estimate with no basis;
  - W, talks taken as likely completion;
  - R, a rung misapplied;
  - M, too little material.

  About 16 of 24 leave the reference's rung on a weak step of their own.
- **The self-made reference** (`docs/research/2026-11-20-production-readiness/self-reference/RESULT.md`): 44 of 2,375 number
  judgements present the system's own earlier figure as the market reference.
- **The linking version** (D691–D711 in `docs/DECISIONS-log.md`; `docs/research/2026-11-21-whole-window/PILOT-RESULT.md`): a
  question reads a related question's conclusion. The pilot was inconclusive. Data Center stopped exceeding total revenue in the
  linked arm, but the total added a CPU forecast (D721 corrects that reading).
- **D720/D721** (`docs/research/2026-11-22-whole-and-part/`): before calling a choice a defect, read the frozen gold's reasoning
  (`docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json`).
- **Decided but not built:**
  - D186: rungs against guidance;
  - D191 point 4: `shared_quantity`;
  - D368 item 2: dependencies chosen at matching;
  - D368 item 4: the root reads its drivers.
- **Filing:** D207 and D265 file a statement under the narrowest question. Claude's quick count: old-2 v9 and v14 share 106 of about
  1,300 evidence items, and their 09-20 answers cite no item in common.

## What to do

1. **Trace at least three cases end to end** from the stored request to the answer, including old-2 v9 and v14 at 09-20 and at least
   one case from each of classes O, S and E. For each: what did the request show, where did each number in the derivation come from
   (a quoted figure, a previous conclusion, the model's own arithmetic), and which design choice let it through?
2. **Count, at $0,** whatever the trace suggests is the mechanism, over the three draws. For example:
   - how often the figures in `implied_outcome` appear in no evidence the request showed;
   - how often related questions use different base figures for the same period;
   - how often the reference is the system's own figure;
   - how often an annual figure is fixed first and a quarter is backed out as a residual.

   Check each instrument on a case you traced.
3. **Step back.** Name the design choices, by module, that produce the class; there may be several stacked. Is it the judge's prompt,
   the unit of judgement (one question judged alone), filing (narrowest-only), the evidence in view (D198), the ladder written at
   opening, the absence of shared typed facts, the absence of code checks on figures, or something else? Rank them by the share of the
   class each explains.
4. **Propose the structural fix you would choose,** and say:
   - what it changes, module by module;
   - how it keeps "code owns identity, never importance" (AGENTS §2);
   - what it leaves to the model;
   - how it agrees with the frozen gold's reasoning;
   - the cheapest test that would refute it, and what result stops it.

   Say also why the linking version did or did not address the root cause.

## Out of scope

Changing the frozen ruler or gold. Building anything. Paid calls.

## Output

- A one-paragraph answer.
- The traces.
- The counts, with their instruments and checks.
- The ranked design causes.
- The proposed fix and its refuting test.
- Your disagreements with the earlier findings.
