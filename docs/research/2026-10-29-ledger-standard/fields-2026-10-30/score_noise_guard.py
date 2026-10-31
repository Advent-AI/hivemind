"""Noise guard of small sample 2: on the 12 development articles where role-v52 kept gold-rejected statements role-v51 did
not (run S), count per draw the gold not_kept sentences kept, all of them and the 21 named ones (the spans v52 kept in at least
two more draws than v51, listed in run S); and, on all 29 articles, core and supporting entries kept per draw. Gold sha printed.

    python3 score_noise_guard.py F2 v51 v52 v53
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

GOLD = HERE.parent / 'golden-v3/golden-v3-signed.json'


def named_spans(gold, ids):
    """The run-S spans: gold not_kept sentences on these articles that v52 kept in >= 2 more draws than v51."""
    runs = {(v, d): sg.answers(f'S-{v}-d{d}') for v in ('v51', 'v52') for d in (1, 2, 3)}
    out = []
    for iid in ids:
        sifted = {k: sg.kept(r.get(iid), iid) for k, r in runs.items()}
        for n in gold[iid]['not_kept']:
            if n['weight'] != 'not_kept':
                continue
            h = {v: sum(bool(sifted[(v, d)]) and any(sg.same(n['span'], e['quote']) for e in sifted[(v, d)]['evidence']) for d in (1, 2, 3)) for v in ('v51', 'v52')}
            if h['v52'] - h['v51'] >= 2:
                out.append((iid, n['span']))
    return out


def main(prefix, versions):
    print('gold sha256', hashlib.sha256(GOLD.read_bytes()).hexdigest()[:16])
    gold = {a['input_id']: a for a in json.loads(GOLD.read_text())['articles']}
    noise_ids = json.loads((HERE / 'noise-guard-ids.json').read_text())
    key = json.loads((HERE / 'key-small.json').read_text())
    all_ids = list(dict.fromkeys([r[1] for r in key['rows']] + key['tier_watch'] + key['company_guard'] + noise_ids))
    spans = named_spans(gold, noise_ids)
    print('articles', len(all_ids), '| noise articles', len(noise_ids), '| named spans', len(spans))
    print('version'.ljust(8) + 'named kept/draw'.rjust(20) + 'all not_kept kept/draw (12)'.rjust(30) + 'core/draw (29)'.rjust(20) + 'supp/draw (29)'.rjust(20))
    for v in versions:
        named, allnk, core, supp = [], [], [], []
        for d in (1, 2, 3):
            run = sg.answers(f'{prefix}-{v}-d{d}')
            sift = {i: sg.kept(run.get(i), i) for i in all_ids}
            named.append(sum(bool(sift[i]) and any(sg.same(sp, e['quote']) for e in sift[i]['evidence']) for i, sp in spans))
            allnk.append(sum(bool(sift[i]) and any(sg.same(n['span'], e['quote']) for e in sift[i]['evidence'])
                             for i in noise_ids for n in gold[i]['not_kept'] if n['weight'] == 'not_kept'))
            core.append(sum(bool(sift[i]) and any(sg.same_matter(it, e) for e in sift[i]['evidence']) for i in all_ids for it in gold[i]['items'] if it['weight'] == 'core'))
            supp.append(sum(bool(sift[i]) and any(sg.same_matter(it, e) for e in sift[i]['evidence']) for i in all_ids for it in gold[i]['items'] if it['weight'] == 'supporting'))
        print(v.ljust(8) + str(named).rjust(20) + str(allnk).rjust(30) + str(core).rjust(20) + str(supp).rjust(20))
    tot_core = sum(1 for i in all_ids for it in gold[i]['items'] if it['weight'] == 'core')
    tot_supp = sum(1 for i in all_ids for it in gold[i]['items'] if it['weight'] == 'supporting')
    print('core entries', tot_core, '| supporting entries', tot_supp)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
