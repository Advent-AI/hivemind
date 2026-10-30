#!/bin/zsh
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send a3-v37-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v53.json || exit 1; done
echo ARM-DONE
