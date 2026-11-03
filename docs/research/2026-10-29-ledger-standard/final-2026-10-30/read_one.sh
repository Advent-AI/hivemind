#!/bin/zsh
# One blind read: the packet named by $1 (its base name), Codex read-only.
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/final-2026-10-30
n=$1
[[ -s verdicts/$n.json ]] && exit 0
sed "s#PACKET_PATH#docs/research/2026-10-29-ledger-standard/final-2026-10-30/packets/$n.json#" reader-prompt.md > prompts/$n.md
codex exec -s read-only -C /Users/lchingen/hivemind-extraction-quality-2026-10-28 --skip-git-repo-check --ephemeral -o verdicts/$n.json - < prompts/$n.md > verdicts/$n.log 2>&1
echo "$n $?"
