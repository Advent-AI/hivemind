#!/bin/zsh
# Diagnostic reading of the five finished draws (plan section 1.4 item 10: new-1 stopped after its one redo, so no release verdict;
# "what finished goes to Alex as a diagnostic, with the cause"). Same tools and order as reading-chain.sh, with the export's
# --diagnostic mode, and a diagnostic count in place of the release scorer (which refuses anything but six eligible draws).
set -e
S=/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0
RUN=/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/run
OUT=/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/reading-diagnostic
cd /Users/lchingen/hivemind
export PYTHONDONTWRITEBYTECODE=1
step() { echo "$(date +%H:%M:%S) == $*"; }

[ -e "$OUT" ] && { echo "refused: $OUT exists"; exit 4; }
mkdir -p "$OUT"
step "1. eligibility (records the finished draws)"
python3 $S/eligibility.py $RUN $OUT/eligibility.json || true

step "2. mapping (diagnostic export of the finished draws)"
python3 $S/mapping.py export $RUN $OUT/mapping-out $OUT/eligibility.json --diagnostic
for n in 1 2 3; do python3 $S/mapping.py read $OUT/mapping-out; done
for n in 1 2 3; do python3 $S/mapping.py third $OUT/mapping-out; done
python3 $S/mapping.py result $OUT/mapping-out

step "3. cards"
python3 $S/mark_cards.py deck $OUT/mapping-out $OUT/deck
for n in 1 2 3; do [ -e $OUT/deck/round-0.done ] || python3 $S/mark_cards.py mark $OUT/deck; done
for r in 1 2; do
  for n in 1 2 3; do [ -e $OUT/deck/round-$r.done ] || python3 $S/mark_cards.py debate $OUT/deck $r; done
done
python3 $S/mark_cards.py readings $OUT/mapping-out $OUT/deck

step "4. diagnostic count"
python3 - "$OUT/deck/readings.json" > $OUT/diagnostic-count.json <<'PY'
import json, sys
sys.path.insert(0, '/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0')
import score_comparison as sc
r = json.load(open(sys.argv[1]))
out = {'note': 'DIAGNOSTIC, not a release verdict: five finished draws (new-1 stopped after its one redo); a matter is served by a '
               'system when it is served in at least 2 of that system\'s finished draws (both of new-2 and new-3; 2 of 3 old)',
       'draws': sorted(r['cards']), 'N': len(r['matters']),
       'margin_rule': max(3, -(-15 * len(r['matters']) // 100))}
for counting in ('1', '2'):
    served = sc.served_by(r, counting)
    a, b = len(served['new'] - served['old']), len(served['old'] - served['new'])
    out[f'counting {counting}'] = {'a (new only)': a, 'b (old only)': b, 'served by new': len(served['new']),
                                   'served by old': len(served['old']), 'both': len(served['new'] & served['old']),
                                   'served_new': sorted(served['new']), 'served_old': sorted(served['old'])}
c = r['controls']
out['controls'] = {'plants marked unsupported or insufficient': sum(m in ('unsupported', 'insufficient') for m in c['plants']),
                   'plants': len(c['plants']), 'supported controls marked supported': sum(m == 'supported' for m in c['supported']),
                   'supported controls': len(c['supported']), 'repeats the same': sum(c['repeats_same']), 'repeats': len(c['repeats_same'])}
out['distinct bets per draw'] = {d: v['ids'] - v['duplicates_both'] for d, v in r['distinct'].items()}
print(json.dumps(out, indent=1))
PY
echo "DIAGNOSTIC COUNT WRITTEN: $OUT/diagnostic-count.json"
step "done"
