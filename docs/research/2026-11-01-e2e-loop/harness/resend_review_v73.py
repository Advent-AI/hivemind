"""Cheapest paid proof of a text change on the v72 base (D265; AGENTS §1 step 4): for the gold supporting matters a control arm extracted in
at least two draws of three and the v92 draws in at most one, rebuild their articles' extraction requests under a changed configuration from
the v92 draw-1 ledger's day-start snapshot, send each three times, and count per matter in how many of the three sends it is written
(score_gold.same_matter, the funnel's test), beside its count in the three stored v92 draws; and, as the guard, the gold not-kept
statements of the same articles written in the new sends against the stored draws. About $0.004 a send.

    python3 resend_review_v73.py <changed config> <control arm d1,d2,d3> <v92 arm d1,d2,d3> [--items ITEMS_DB] [--weight supporting]
"""
import argparse
import collections
import json
import shutil
import sqlite3
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402
from matter_states import states  # noqa: E402

SENDERS = 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config'); ap.add_argument('control'); ap.add_argument('base')
    ap.add_argument('--items', default=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    ap.add_argument('--weight', default='supporting')
    args = ap.parse_args()
    cfg = config.load(args.config)
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    control = [states(p) for p in args.control.split(',')]
    base = [states(p) for p in args.base.split(',')]
    targets = collections.defaultdict(list)             # input_id -> [(matter index, span)]
    for key in base[0]:
        if base[0][key][1] != args.weight:
            continue
        ext_c = sum(d[key][0] != 'not extracted' for d in control if key in d)
        ext_b = sum(d[key][0] != 'not extracted' for d in base if key in d)
        if ext_c >= 2 and ext_b <= 1:
            targets[key[0]].append(key[1])
    base_dir = args.base.split(',')[0]
    scratch = Path(tempfile.mkdtemp(prefix='v73-proof-'))
    shutil.copy(Path(base_dir) / 'views.sqlite', scratch / 'views.sqlite')
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    items_db = testdb.open_db(args.items)
    by_id = {a['input_id']: a for a in sr.articles}
    days = sorted({by_id[i]['publication_day'] for i in targets} | {by_id[i].get('day', '') for i in targets if by_id[i].get('day')})
    items = {it['input_id']: it for it in testdb.feed(items_db, '2026-07-01', '2026-07-14') if it['input_id'] in targets}
    print(f'{len(targets)} articles, {sum(len(v) for v in targets.values())} {args.weight} matters extracted by the control in >=2 draws and by the base in <=1; '
          f'config {cfg.version}; 3 sends each', flush=True)

    def send(body):
        return json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])

    jobs = []
    with ThreadPoolExecutor(SENDERS) as pool:
        for iid, matters in targets.items():
            item = items[iid]
            objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
            shown = extraction.shown_views(ledger, cfg, item, objects)
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
            body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
            jobs.append((iid, matters, [pool.submit(send, body) for _ in range(3)]))
        recovered = collections.Counter(); guard_new = []; guard_base = []
        for iid, matters, futures in jobs:
            a = by_id[iid]
            answers = [f.result() for f in futures]
            print(f"\n## {a['publication_day']} | {a['title'][:80]}")
            for n in matters:
                it = a['items'][n]
                new_count = sum(any(sr.sg.same_matter(it, e) for e in ans.get('evidence', [])) for ans in answers)
                base_count = sum(d[(iid, n)][0] != 'not extracted' for d in base if (iid, n) in d)
                recovered[(base_count, new_count)] += 1
                print(f"   matter: stored v92 {base_count}/3 -> {cfg.version} {new_count}/3 | {it.get('span', '')[:110]}")
            not_kept = [x for x in a['not_kept'] if x['weight'] == 'not_kept']
            new_noise = [sum(any(sr.sg.same(x['span'], e.get('quote') or '') for e in ans.get('evidence', [])) for x in not_kept) for ans in answers]
            guard_new.append(sum(new_noise) / 3)
            print(f"   guard: gold not-kept statements written per send {new_noise} of {len(not_kept)} listed")
    print(f'\nmatters by (stored v92 count, new count): {dict(sorted(recovered.items()))}')
    print(f'guard: gold not-kept statements written in the new sends, mean per article per send {sum(guard_new) / max(1, len(guard_new)):.2f}')
    shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    main()
