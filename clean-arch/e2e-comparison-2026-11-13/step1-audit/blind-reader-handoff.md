# Blind second reader: a whole-request prompt audit of one extraction request against its signed standard (read-only)

You are an independent reader. Nobody's conclusions are given to you. Read, in this order:
1. The signed standard (frozen, Chinese): `docs/prd/05-extraction-standard.html`, especially §3 (the table of opening reasons A–E with their
   periods and due days; "问题怎么写") and §4 (the opening tests, "不开的", and "同一题、续期，还是另一题" in full).
2. The request exactly as the model reads it: `clean-arch/e2e-comparison-2026-11-13/step1-audit/request-system.txt`,
   `request-user.txt` (the open theses, the item, and the closing check at its end), `request-schema.json` (every field description).
   Note: in this pipeline the extraction model is shown the open theses and no later step compares new theses with the library.
3. The failures, each with stored cases (raw answers in the traces; the model's later accounts are leads, not proof):
   - F1: a report that the company is negotiating an unsigned guarantee of one large lease is linked only to the open thesis on the amount
     of its credit-support programme; no yes/no signing thesis is opened. Cases: `poc/data/clean-e2e-full-2026-11-13/c1/step1/trace.sqlite`,
     `c2/step1-redo/trace.sqlite`, `c3/step1/trace.sqlite`, table `trace`, sequence 8 (`result` column); accounts in
     `clean-arch/e2e-comparison-2026-11-13/opening-review/accounts-2026-11-13.json` and `clean-arch/step1-diagnosis-2026-11-12/model-account.json`.
   - F2: next calendar year's combined hyperscaler capex is used as the reference of a this-year question instead of its own thesis. Cases:
     sequence 42 in the same three traces; the same accounts files.
   - F3: a shared price opened over a non-calendar window ("12 months to mid-2027", c1 sequence 127) or with two quantities (memory prices
     and per-rack memory cost, c2 sequence 56).
   - F4: a programme already announced and under way tracked by "signed by" a check date 18 months out rather than at the next annual report
     (c1 sequence 1).
   - F5: theses a later step had to refuse because they track two figures with none main, or a rolling twelve-month window (see the refusal
     reasons in `poc/data/clean-e2e-full-2026-11-13/stage-a/report.txt`).
   - F6: a shared price (memory contract prices) not opened, the model saying the item gives no release date (`clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md`, the q05 row).

Write two tables:
- **A.** Every instruction in the request that decides whether a new thesis is proposed, whether it is the same as an open thesis, or its
  period and due day (quote it, give its place), against the standard: consistent / contradicts / keeps wider / keeps narrower / no source.
  Then every identity rule of the standard's §4 "同一题、续期，还是另一题" and §3's period and identity lines: carried by the request / not carried.
- **B.** For F1–F6: the request sentence(s) that produce it (quoted), the standard's line on the case (quoted), and one verdict:
  contradiction / missing / abstract / misread / not the prompt.

Then say, in at most 120 words, whether F1 and F2 share one structural cause, with the evidence.

Out of scope: any other request or pipeline; changing the standard or its gold; proposing prompt text.
