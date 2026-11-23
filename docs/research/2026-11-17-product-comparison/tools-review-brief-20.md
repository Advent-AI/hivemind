# Review round 20, confirmation only (read-only, $0)

Round 19 (`tools-review-codex-19.md`) asked for the chain to be rebuilt from primary data. Done (`git log -1`, D675's last entry):
- `stage0/rebuild.py` `differences` rebuilds every derived file in a temporary folder, with the code that wrote it:
  - eligibility;
  - libraries and mapping key;
  - `mapping.json`;
  - deck key and card texts.
- The deck's reader confirmations are replayed from their record. No reader is called.
- `score_comparison.score(run root, mapping out, marks folder)` refuses if any stored derived file differs, then scores the readings
  built by their one writer.
- `stage0/chain_dry_run.py` runs in process. Each edit is followed by a regenerated readings record, as you did, and the edited mapping,
  deck key and card text are all refused.

The primary data are:
- the run stores;
- the readers' own answer files (`map-*.txt`, `third/`, `control-confirmations.jsonl`, rounds 0–2);
- the frozen inputs.

Check, citing file and line:
1. Is there a change to anything other than the primary data that changes a verdict or a printed value through `score`? Give it.
2. Does the rebuild call any reader, write outside its temporary folder, or leave a module attribute changed?
3. Is any value or verdict changed for an unedited chain?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words. Report only a case of kind 1, 2 or 3.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
