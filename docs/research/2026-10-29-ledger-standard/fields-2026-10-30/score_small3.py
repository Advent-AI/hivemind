"""Small sample 3: per version and draw, the tier key's decisive records (kept, tier in the accepted set) and, on the 12 random
guard articles and on all articles sent, gold core and supporting entries kept and gold not_kept sentences kept. Keys' sha printed.

    python3 score_small3.py F3 v53 v54 v55
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

GOLD = HERE.parent / 'golden-v3/golden-v3-signed.json'


def squash(text):
    return re.sub(r'[^a-z0-9$]', '', (text or '').lower().replace('’', "'"))


def main(prefix, versions):
    tier_key = json.loads((HERE / 'key-tier.json').read_text())
    small = json.loads((HERE / 'key-small.json').read_text())
    print('key-tier sha256', hashlib.sha256((HERE / 'key-tier.json').read_bytes()).hexdigest()[:16], '| gold', hashlib.sha256(GOLD.read_bytes()).hexdigest()[:16])
    gold = {a['input_id']: a for a in json.loads(GOLD.read_text())['articles']}
    guard = tier_key['random_guard']
    sent = list(dict.fromkeys([r[1] for r in small['rows']] + small['tier_watch'] + small['company_guard'] + guard))
    print('version'.ljust(8) + 'tier ok / kept'.rjust(22) + 'guard core'.rjust(16) + 'guard supp'.rjust(16) + 'guard not_kept'.rjust(18) + 'all core'.rjust(16) + 'all supp'.rjust(16) + 'all not_kept'.rjust(18))
    for v in versions:
        tier, gcore, gsupp, gnk, acore, asupp, ank = [], [], [], [], [], [], []
        for d in (1, 2, 3):
            run = sg.answers(f'{prefix}-{v}-d{d}')
            sift = {i: sg.kept(run.get(i), i) for i in sent}
            ok = kept = 0
            for name, iid, span, accepted, _ in tier_key['rows']:
                if iid not in sift or not sift[iid]:
                    continue
                match = [e for e in sift[iid]['evidence'] if squash(span) in squash(e['quote'])]
                if match:
                    kept += 1
                    ok += match[0]['tier'] in accepted
            tier.append(f'{ok}/{kept}')

            def count(ids, weight):
                return sum(bool(sift[i]) and any(sg.same_matter(it, e) for e in sift[i]['evidence']) for i in ids for it in gold[i]['items'] if it['weight'] == weight)

            def nk(ids):
                return sum(bool(sift[i]) and any(sg.same(n['span'], e['quote']) for e in sift[i]['evidence']) for i in ids for n in gold[i]['not_kept'] if n['weight'] == 'not_kept')
            gcore.append(count(guard, 'core')); gsupp.append(count(guard, 'supporting')); gnk.append(nk(guard))
            acore.append(count(sent, 'core')); asupp.append(count(sent, 'supporting')); ank.append(nk(sent))
        print(v.ljust(8) + str(tier).rjust(22) + str(gcore).rjust(16) + str(gsupp).rjust(16) + str(gnk).rjust(18) + str(acore).rjust(16) + str(asupp).rjust(16) + str(ank).rjust(18))
    print('entries: guard core', sum(1 for i in guard for it in gold[i]['items'] if it['weight'] == 'core'), 'supp', sum(1 for i in guard for it in gold[i]['items'] if it['weight'] == 'supporting'),
          '| all core', sum(1 for i in sent for it in gold[i]['items'] if it['weight'] == 'core'), 'supp', sum(1 for i in sent for it in gold[i]['items'] if it['weight'] == 'supporting'),
          '| tier rows on sent articles', sum(1 for r in tier_key['rows'] if r[1] in sent))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
