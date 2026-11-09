Fixed. Re-read `adapter.py` (judge, worst_cost, load_draw), `test_adapter.py` and `run_clean_draw.sh` (read-only, under 150 words).

1. **The cap's release and its cost are now one locked step.**
   - The actual cost is recorded, not capped at the reserve.
   - A failed call is charged its full reserve.
   - Each reserve covers `TRANSPORT_ATTEMPTS = 3`, model.openai_transport's default attempts.
2. **Provenance.** The launcher writes `step2/trace.sha256` right after Step 2 builds the library from that trace. The adapter refuses a
   Step 2 folder whose stamp does not match the trace's bytes, and a test covers that refusal. With the ten-field copy check, this ties
   placements, revisions and later links to the launcher's own Step 2 run on this trace.

SEND (clean arm, pending the control harness) or BLOCKER?
