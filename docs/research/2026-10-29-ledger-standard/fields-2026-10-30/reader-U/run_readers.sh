#!/bin/zsh
# Blind field readers: one Codex read-only session per packet (AGENTS §11), six at a time; a written verdict is never redone.
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/fields-2026-10-30/reader-U
ls packets | sed 's/\.json$//' | xargs -P 6 -n 1 zsh -c '
n=$1
[[ -s verdicts/$n.json ]] && exit 0
sed "s#PACKET_PATH#docs/research/2026-10-29-ledger-standard/fields-2026-10-30/reader-U/packets/$n.json#" reader-prompt.md > prompts/$n.md
codex exec -s read-only -C /Users/lchingen/hivemind-extraction-quality-2026-10-28 --skip-git-repo-check --ephemeral -o verdicts/$n.json - < prompts/$n.md > verdicts/$n.log 2>&1
echo "$n $?"' _
echo READERS-DONE
