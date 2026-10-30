#!/bin/zsh
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/final-2026-10-30
ls packets | sed 's/\.json$//' | xargs -P 6 -n 1 zsh /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/final-2026-10-30/read_one.sh
echo READERS-DONE
