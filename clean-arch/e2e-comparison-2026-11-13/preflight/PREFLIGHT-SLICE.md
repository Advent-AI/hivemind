# Preflight before the slice (AGENTS §5; council mo, 2026-11-13)

**Production (v118).** `scripts/preflight.py` over the three stored unseeded v118 draws (`preflight-v118-q1..q3.txt`; exit 0 each), the
current code:

| check | q1 | q2 | q3 |
|---|---|---|---|
| A. answers the schema refused | judged 0 | judged 0 | judged 1, refused 1 |
| B. extraction checks: judged / refused | 747 / 8 | 769 / 9 | 731 / 9 |
| refusal reasons | quote not in item 7, duplicate quote merged 1 | quote not in item 6, duplicate quote 2, a candidate ladder with no rungs 1 | quote not in item 7, a binding obligation due beyond 18 months 1, duplicate quote 1 |
| C. matching checks: judged / refused / skipped | 106 / 0 / 2 | 151 / 0 / 4 | 139 / 0 / 3 (skipped: "request not in this archive") |
| D. enum values named in the prompts | 43, missing 0 | 43, missing 0 | 43, missing 0 |
| E. keyed views, duplicates | 13, 0 | 12, 0 | 15, 0 |

The refusals are production's own checks on its own answers, the same kinds and rates as the v116 preflight (`preflight-v116-d*.txt`); none
comes from the wiring, which does not change a request (the byte-for-byte control in `proof_interception.py`). *Does not exercise:* the
budget transport (proved by `proof_interception.py` and `proof_end_to_end.py`), v118's behaviour on a fresh day (the slice shows it).

**The clean path.** Its checks on stored answers through the current code are the $0 proofs: `proof_wiring.py` (Stage B rebuilt row for
row), `proof_interception.py` (Step 1 one day as stored, Step 2 byte for byte, Stage A run 4 every outcome, the judge every table),
`proof_end_to_end.py` (one day through the orchestrator: Step 1, the cases and the ladder outcomes as stored). *Does not exercise:* the
coverage-start reading's check (an open defect of the preflight, `CURRENT_STATE.md`), new model answers (the slice shows them).

**Measurement capture added for the slice** (council mo, round 8): the ledger writes one line per settled or refused attempt (process id,
reserved, charged, time; `check_budget.py` check 17); the draw record keeps each attempt's process id and start and end times;
`spend_by_component.py` maps the lines to components. In the end-to-end proof: every line attributed, the lines sum to the ledger's spent,
every attempt timed (Step 1 13 attempts $0.1206, Step 2 19 $0.0089, the ladder 2 $0.0018, the judge 2 $0.0021, production 19 $0.0094; ledger
charges from stored usage).
