# Independent investigation: why does the clean Step 1 leave helpful evidence unfiled, and what general fix is there? (read-only)

You are an independent investigator; no conclusion is preferred. Read-only: edit nothing, run no model calls.

**Read:**
- `AGENTS.md` (§1, §2, §6, §7, §8 especially);
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` §0 only (the frame). Do not read §1–§2 until you have formed your own view;
- the request: `clean-arch/takeover-2026-11-07/k6b-system.txt`, `k6b-closing.txt`, `k6b-schema.json`;
- the stored runs: dev `poc/data/clean-step1-takeover-2026-11-07/gold-k6b-flash/trace.sqlite` and `gold-k6b-flash-d2/trace.sqlite`;
  test `poc/data/clean-step1-takeover-2026-11-07/test-k6b-flash/trace.sqlite`. Table `trace`: `result` JSON holds `evidence` and
  `unfiled_evidence`; `before_state` holds the open theses;
- the model's own accounts: `poc/data/clean-step1-unfiled-2026-11-08/account-test.json` and `account-d1.json`;
- the census: `poc/data/clean-step1-unfiled-2026-11-08/census-dev.json` and `census-test.json`;
- decisions: `docs/DECISIONS-log.md` D208, D209, D370, D371, D373; the earlier no-home diagnosis
  `docs/research/2026-11-06-e1-no-home-drops/README.md`; the signed standard `docs/prd/05-extraction-standard.html` (§3, §6).

**Out of scope:** the frozen gold (never edited), frozen production, Steps 2 to 4, cost.

**Alex's constraint:** no hard-coded fix and no prompt overfitted to the test cases. Every rule must trace to the standard or a decision,
name no company, product or test case, and read the same for a bank, a drug maker or a retailer.

**Answer:**
1. The mechanism(s) behind helpful evidence being left unfiled, by class, with counts and the request sentences responsible.
2. Which classes are real losses under the standard and D371, and which are drops the standard intends.
3. The structural levers you would test, preferring the output contract, a required per-item field, check placement, effort or model
   over sentence wording. Give each lever's source and its falsifier, and the isolation arms.
4. A probe design: which dev articles (not test), fixed before-states, controls that must not regress (noise, small theses), 3 draws.
5. What could make this a benchmark-farming fix, and how to guard against it.

Under 700 words. Cite files and lines.
