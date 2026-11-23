# Code review: the wiring for the diagnostic same-day run (D447, D448)

You are an independent, read-only code reviewer for the Hivemind repository at /Users/lchingen/hivemind. Read the code itself; do not
trust any summary. Report serious defects first, each with the file and line, the concrete failure scenario, and the smallest fix.

## The contract the code must meet

`clean-arch/e2e-comparison-2026-11-13/WIRING-DESIGN.md` (version 4; read it in full). In short: one shared spending ledger over every paid
call of a run (Step 1, Step 2's embeddings and Jev, the ladder step, the judge, production); each entry point reserves per actual attempt
and settles at usage; a refused reservation stops the whole run (persisted, in every process); a crash between a send and its charge leaves
the reservation counted; every input of the ladder step and the judge follows a fresh run instead of the stored Stage B constants, whose
defaults must still reproduce the stored runs; the run states and stop rules of §D.

Decisions that bind it: `docs/DECISIONS-log.md` D439 (council decides while Alex is away; limits: frozen ruler, no push/commit, credentials
and provider caps untouched, spending ceiling), D447 and D448 (search for "D447" and "D448"). AGENTS.md §2–§5 (design tables, one owner,
tests and mutants, verification).

## The code to review (all changes since commit 053c957 in these files, plus the new files)

- `clean-arch/e2e-comparison-2026-11-13/budget_replay.py` (`SharedLedger`: persisted stop, per-thread live-reservation mark;
  `BudgetTransport`), `check_budget.py`
- `clean-arch/step1/live.py` (`LiveTransport(..., ledger=None)`), `clean-arch/step1/run_live.py` (`--shared-ledger`),
  `clean-arch/step1/test_live_ledger.py`
- `clean-arch/step4-2026-11-10/stage_a/stage_a.py` (`StageALimit(shared=)`, `--cases-file`, `--shared-ledger`),
  `stage_a/build_cases.py` (`--fresh`), `stage_b/ladder_adapter.py` (`LedgerBudget(shared=)`, `replay(inputs=, shared=)`),
  `stage_b/run_stage_b.py` (arguments), `clean-arch/step4-2026-11-10/test_shared_ledger_hooks.py`
- new: `clean-arch/e2e-comparison-2026-11-13/budget_step2.py`, `run_fresh.py`, `test_run_fresh.py`, `proof_wiring.py` (output
  `proof_wiring.output.txt`), `proof_interception.py` (output `proof_interception.output.txt`)

Use `git diff 053c957 -- <file>` for the changed files. The proofs' recorded outputs are beside them; you cannot rerun them read-only.

## What to look for

1. Any paid call that can be sent without a reservation on the shared ledger, or charged twice, or never settled (including retries
   inside `model.openai_transport`, `jev.transport`, `search.openai_embeddings`, Stage A's resend, the judge's own retry loop, production's
   parallel threads).
2. Any path where a refused reservation, an overrun or a crash does not stop every later send in every process.
3. Any change that alters a request's bytes, or a default that no longer reproduces the stored Stage A, Stage B or cases.
4. `run_fresh.py`: walk its states against §D's table (success, a check's refusal, a transport failure, a budget refusal, a crash, a crash
   of the orchestrator itself, a second launch, a later launch, another draw's stop). Name any cell the code gets wrong or does not hold.
5. Whether the proofs actually prove what they claim (a check that cannot fail, a comparison over nothing, a mutant caught for the wrong
   reason).
6. Whether any frozen file changed: the ruler (AGENTS §7.1), `clean-arch/step2/*` and `clean-arch/step3/library.py` (D427),
   `clean-arch/unseeded-2026-11-10/unseeded-frozen.sha256`'s files, the production configuration and prompts.

## Out of scope

The readings (Stage A's and Stage B's reader procedures), the census method, the Step 1 prompt, the ruler and gold, whether the run is worth
doing (decided in D447), wording and style. Do not propose new mechanisms for cases nobody named.

End with one line: "Council position: <ready for the slice | not ready, because ...>".
