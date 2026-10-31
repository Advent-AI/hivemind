#!/bin/zsh
# role-v64 (poc-v80) against role-v65 (poc-v81), sent together on the development gold (118) and the test gold (30), three draws
# (run_full.sh); key-v65.json frozen before this send. No edit to src/ or prompts while it runs.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
(cd $ROOT/docs/research/2026-10-30-noise && shasum -a 256 -c key-v65.sha256)
zsh $ROOT/docs/research/2026-10-29-ledger-standard/run_full.sh Y5 poc/config/poc-v80.json poc/config/poc-v81.json
