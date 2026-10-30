#!/bin/zsh
# Arm A1 (role-v35, poc-v51): one send per development article, compared with the v29 baseline (page §9.3 step 4).
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send a1-v35 /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v51.json && echo ARM-DONE
