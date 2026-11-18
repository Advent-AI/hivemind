# Review round 21, confirmation only (read-only, $0)

Round 20 (`tools-review-codex-20.md`) is fixed (`git log -1`, D675's last entry):
- `stage0/rebuild.py` `scored` computes the verdict on the readings built from the rebuilt snapshot, inside the temporary folder;
- a stored derived file that differs from the rebuild is refused, and that includes `readings.json`;
- rebuild progress goes to stderr;
- the import path is restored.

The dry run (`stage0/chain_dry_run.py`, `stage0/chain-dry-run.txt`) shows:
- each derived file edited twice, once with the readings record rewritten from the edit and once without, and both refused;
- the verdict reads only the snapshot;
- stdout carries no progress;
- the import path is unchanged.

Check, citing file and line:
1. Is there still a change to anything other than the primary data that changes a verdict or a printed value through `score`? Give it.
2. Does the rebuild call a reader, write outside its temporary folder, or leave a module attribute or the import path changed?
3. Is any value or verdict changed for an unedited chain?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words. Report only a case of kind 1, 2 or 3.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
