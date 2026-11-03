#!/bin/zsh
# role-v63 (poc-v79) against role-v64 (poc-v80), sent together on the development gold (118) and the test gold (30), three draws
# (run_full.sh); key-v64.json frozen before this send (sha256 in key-v64.sha256). No edit to src/ or prompts while it runs.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
shasum -a 256 -c $ROOT/docs/research/2026-10-30-noise/key-v64.sha256 --status --ignore-missing 2>/dev/null || (cd $ROOT/docs/research/2026-10-30-noise && shasum -a 256 -c key-v64.sha256)
zsh $ROOT/docs/research/2026-10-29-ledger-standard/run_full.sh Y4 poc/config/poc-v79.json poc/config/poc-v80.json
