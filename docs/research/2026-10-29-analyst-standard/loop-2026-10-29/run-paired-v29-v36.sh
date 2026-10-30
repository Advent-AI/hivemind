#!/bin/zsh
# Re-establish the ruler (AGENTS section 7.3, a fresh control): v29 and v36 sent at the same time, interleaved, three draws each, all 118 development articles.
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send pair-v29-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v45.json &
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send pair-v36-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v52.json &
  wait
done
echo PAIR-DONE
