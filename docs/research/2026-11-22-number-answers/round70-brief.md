# Council round 70 (before the paid send Alex authorized): independent review, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## Context
- **Alex's decision D753** (`docs/DECISIONS-log.md`, last entry): "破例一次，付费重发". This is a one-time exception to D749's
  clean-pass condition: the 36 requests rebuilt in v13s with the D751 request, under D725's lines and `PAID-GATE.md` §4, with a total
  cap of $0.50 including retries. It also sets "can't tell yet" as the E-type default, with no request change.
- **What is ready.** Nothing has been sent.
  - The plan: `docs/research/2026-11-22-number-answers/paid-plan-v13s.json`, pinned in `paid-plan-v13s.sha256` (`0dc7c310…`). It
    holds 12 requests × 3 draws, built by `paid_gate.py plan-v13s`. Its system text is the registered D751 request (`080a0012…`).
  - **The code change**, in `paid_gate.py`:
    - the constants `PINNED_PLAN_V13S` and `AUTH_V13S` (a fresh one-time key path `~/.hivemind-keys/v13s-paid-gate/`);
    - `send()` now picks the pin and the authorization by the plan's format and refuses a mixed plan;
    - the v13 pin and the spent v13 authorization are unchanged.
  - **$0 checks**, with a stub gate and scratch key paths:
    - an altered plan is refused, and a wrong ceiling is refused;
    - the pinned plan passes;
    - a second use of the authorization is refused, and the old v13 plan is refused because its authorization is spent.
    - The rehearsal passes 19 of 19, and the paid mutants are 33 of 33 caught with the control passing.
- **The intended launch.**
  - `python3 paid_gate.py send poc/data/judging-v13s-paid-2026-11-23 0.5 docs/research/2026-11-22-number-answers/paid-plan-v13s.json`,
    detached, with a log and a pid file.
  - After it: `packets`, two blind readers per packet (Codex and Claude), a third Codex reader on disagreements, then `verdict` as
    `PAID-GATE.md` §4 registers it.
- **The reading rule** was fixed before any answer existed (`PAID-GATE.md` §4; D731). Since then:
  - Alex ruled D747: an explained related figure counts as support;
  - D753 makes "can't tell yet" the E-type default;
  - the free tests' reader definitions are in `blind_rules.py`.

## Questions
1. **Is the send ready?** Check:
   - the plan's contents against the registered cases (`PAID-GATE.md`, `paid_gate.py` PAIRS and SINGLETONS);
   - the pin, the cap and the authorization logic in `send()`;
   - the retry policy (first attempt scored, retries diagnostic, inside the cap);
   - that nothing else changed in the gate.
2. **The reading rule.** Should the paid readers' brief (the `packets` text in `paid_gate.py`) carry Alex's D747 definition of
   support, and the D753 default, before any answer exists? Or must the registered §4 rule stay exactly as fixed? What is the smallest
   correct course that neither changes the verdict lines nor ignores Alex's later rulings?
3. **Anything that could waste the send.** Examples: an INCOMPLETE risk, a known refusal class, a guard that would stop it for a
   reason unrelated to luna. What does the cheaper check leave uncovered?
4. **Verdict:** send as is, send with listed changes, or do not send.

Return a numbered report: findings marked serious / minor / wording, with citations, then the verdict.
