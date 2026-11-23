#!/bin/zsh
# The reading chain of the release comparison (CURRENT_STATE "When all six draws end", steps 1-5), run once when new-1 completes.
# Each step stops the chain on failure (set -e). A reader round that left void answers is run again, at most three times in all;
# a round still incomplete stops the chain at the next step's own refusal. Outputs go to poc/data/comparison-2026-11-17/reading.
set -e
S=/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0
RUN=/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/run
OUT=/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/reading
cd /Users/lchingen/hivemind
export PYTHONDONTWRITEBYTECODE=1
step() { echo "$(date +%H:%M:%S) == $*"; }

step "waiting for new-1 to end"
while true; do
  state=$(python3 -c "import json; print(json.load(open('$RUN/new-1/run.json'))['state'])")
  [ "$state" = complete ] && break
  if [ "$state" != running ]; then echo "new-1 ended as '$state': no release verdict (plan section 1.4 item 10)"; exit 2; fi
  sleep 60
done

[ -e "$OUT" ] && { echo "refused: $OUT exists"; exit 4; }
mkdir -p "$OUT"
step "1. eligibility"
python3 $S/eligibility.py $RUN $OUT/eligibility.json
python3 -c "import json, sys; sys.exit(0 if json.load(open('$OUT/eligibility.json'))['eligible'] else 3)"

step "2. mapping"
python3 $S/mapping.py export $RUN $OUT/mapping-out $OUT/eligibility.json
for n in 1 2 3; do python3 $S/mapping.py read $OUT/mapping-out; done
for n in 1 2 3; do python3 $S/mapping.py third $OUT/mapping-out; done
python3 $S/mapping.py result $OUT/mapping-out

step "3. cards"
# the diagnostic reading of the five finished draws (diagnostic-chain.sh) wrote its own deck key; it is set aside, with its control
# confirmations, once that reading has ended, so this deck writes the release key (a deck never overwrites a key)
DIAG_PID=$(cat /Users/lchingen/hivemind/poc/data/comparison-2026-11-17/diagnostic-chain.pid 2>/dev/null || echo 0)
while kill -0 $DIAG_PID 2>/dev/null; do sleep 60; done
KEYS=$HOME/.hivemind-keys/comparison-2026-11-17
if [ -e $KEYS/deck-key.json ]; then
  [ -e $KEYS/deck-key-diagnostic.json ] && { echo "refused: $KEYS/deck-key-diagnostic.json exists"; exit 5; }
  mv $KEYS/deck-key.json $KEYS/deck-key-diagnostic.json
  [ -e $KEYS/control-confirmations.jsonl ] && mv $KEYS/control-confirmations.jsonl $KEYS/control-confirmations-diagnostic.jsonl
fi
python3 $S/mark_cards.py deck $OUT/mapping-out $OUT/deck
for n in 1 2 3; do [ -e $OUT/deck/round-0.done ] || python3 $S/mark_cards.py mark $OUT/deck; done
for r in 1 2; do
  for n in 1 2 3; do [ -e $OUT/deck/round-$r.done ] || python3 $S/mark_cards.py debate $OUT/deck $r; done
done
python3 $S/mark_cards.py readings $OUT/mapping-out $OUT/deck

step "4. verdict"
python3 $S/score_comparison.py $RUN $OUT/mapping-out $OUT/deck > $OUT/verdict.json
echo "VERDICT WRITTEN: $OUT/verdict.json"

step "5. release checks"
python3 $S/d400_code_check.py $RUN $OUT/eligibility.json > $OUT/d400-code-check.txt
for line in line1 line2 line3; do python3 $S/step2_lines.py $line $RUN $OUT/eligibility.json $OUT/step2-lines; done
python3 $S/step2_lines.py report $OUT/step2-lines > $OUT/step2-lines.txt
echo "RELEASE CHECKS WRITTEN"
step "done"
