# Council round 47c: after 47b (read-only, same thread)

Every 47b finding is answered (PAID-GATE.md §3c; code in paid_gate.py, cases in paid_rehearsal.py, mutants in paid_mutants.py).
1. Reconciliation: `_same_value` (bounds equal, each end within 1e-9 relative) replaces exact equality in `merge`; readers see each reconciled card's own original answer (`packets`: `per_card` from the separate finals, never the merged calc).
2. Completeness: `derive_finals` builds every unit's final status from answers.jsonl alone (not sent / interrupted / retry not sent / last decision; a second refusal is unresolved); `Gate.run` writes results.json in a finally through `summarise`; `verdict` is INCOMPLETE for any status other than publish, held or unresolved (transport included).
3. Packets: every attempt per card with check codes; `card_view` gives each card its own upstream figures renumbered F1.. and maps its recorded assumptions, leaving out any record that names a figure outside the card.
4. Binding: packets.md and packet-key.json are created exclusively; the key holds `run_digest` (answers.jsonl, results.json, plan.json) and the packets sha256; readings carry the packets sha256; the verdict is INCOMPLETE on any mismatch or on a ground that is not a non-empty string naming a passage or figure of that packet (`_grounded`).

Rehearsal: 41 of 41 (rehearsal.log). Mutants of these defences: 13 of 13 caught, control passes (paid-mutants.log). Plan unchanged (sha256 6f81dae5…); calc_check.py unchanged since gate run 27 (87 of 87).

Out of scope: the frozen ruler, production code, the D725 verdict lines and the $0 gate's checks.

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line for each.
