"""Cheapest paid proof of a configuration on a class of gold matters (AGENTS §1 step 4): the gold core or supporting matters a base arm wrote
in at most one of its three draws, or the matters of named articles; rebuild their articles' extraction requests under a configuration from
the base's draw-1 day-start snapshot, send each three times, and count per matter in how many sends it is written (score_gold.same_matter)
beside its count in the three stored base draws; the guard per article is the gold not-kept statements written per send against the stored
draws. About $0.004 a send.

    python3 resend_targets.py <config> <base d1,d2,d3> [--weight supporting|core|both] [--match TITLE...] [--max-articles 40]
"""
import argparse
import collections
import json
import shutil
import sqlite3
import sys
import tempfile
import types
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


def answer_of(archive, iid):
    r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
    return json.loads(r[0]).get('evidence', []) if r and r[0] else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config'); ap.add_argument('base')
    ap.add_argument('--weight', default='supporting'); ap.add_argument('--match', nargs='*', default=[]); ap.add_argument('--max-articles', type=int, default=40)
    ap.add_argument('--items', default=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    ap.add_argument('--save', default=None, help='a JSON file that keeps every new answer, so a recount costs nothing')
    ap.add_argument('--replay', default=None, help='count a saved JSON of answers again instead of sending ($0)')
    ap.add_argument('--timeout', type=int, default=180, help='seconds one call may take before the transport retries it (higher reasoning effort is slower)')
    args = ap.parse_args()
    cfg = config.load(args.config)
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    base_dirs = args.base.split(',')
    base = [states(p) for p in base_dirs]
    archives = [sqlite3.connect(f'file:{p}/archive.sqlite?mode=ro', uri=True) for p in base_dirs]
    weights = ('core', 'supporting') if args.weight == 'both' else (args.weight,)
    by_id = {a['input_id']: a for a in sr.articles}
    targets = collections.defaultdict(list)
    if args.match:
        wanted = [m.lower() for m in args.match]
        for a in sr.articles:
            if any(w in a['title'].lower() for w in wanted):
                targets[a['input_id']] = [n for n, it in enumerate(a['items']) if it['weight'] in weights]
    else:
        for key in base[0]:
            if base[0][key][1] in weights and sum(d[key][0] != 'not extracted' for d in base if key in d) <= 1:
                targets[key[0]].append(key[1])
    items = {it['input_id']: it for it in testdb.feed(testdb.open_db(args.items), '2026-07-01', '2026-07-14') if it['input_id'] in targets}
    skipped = [i for i in targets if i not in items]                  # a gold article the window's feed does not carry
    chosen = [i for i in targets if i in items][:args.max_articles]
    scratch = Path(tempfile.mkdtemp(prefix='targets-proof-'))
    shutil.copy(Path(base_dirs[0]) / 'views.sqlite', scratch / 'views.sqlite')
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    print(f'{len(chosen)} articles, {sum(len(targets[i]) for i in chosen)} {args.weight} matters; config {cfg.version}; 3 sends each'
          + (f'; {len(skipped)} target articles not in the feed, skipped' if skipped else ''), flush=True)

    def send(body):
        return json.loads(model.openai_transport(cfg.provider, body, timeout=args.timeout)['choices'][0]['message']['content'])

    def filed(data, item, shown, version):
        """What the pipeline files from an answer: the sift (quote check, the v78 field rule) and the filing (no home); each statement's fate."""
        shown_ids = [v['view_id'] for v in shown]
        evidence, candidates, dropped, new_groups = extraction.sift_with_groups(data, item, item['text'], shown_ids, uni, english=True, version=version, keep_unlinked=True)
        reading = extraction.Reading(evidence, candidates, dropped, new_groups, types.SimpleNamespace(cost_usd=0.0, cached=False, call_id=0, request_sha256=''), version)
        handover = extraction.file_reading(reading, None, cfg, item, shown)
        fate = {i: r for i, r in handover.dropped}
        fate.update({e['id']: 'reached' for e in handover.evidence})
        return handover.evidence, fate

    def stored_filed(base_dir, iid):
        h = ledgers[base_dir].execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        return json.loads(h[0]).get('evidence', []) if h else []

    def classes(e):
        return e.get('news') or ('/'.join(x for x in (e.get('new'), e.get('kind')) if x) or '-')

    def label(e, fate):
        return f"{e.get('party', '-')}/{classes(e)}/{e.get('scale', '-')}:{fate.get(e['id'], '?')[:24]}"

    def written(x, evs):
        return any(sr.sg.same(x['span'], e.get('quote') or '') for e in evs)

    ledgers = {p: sqlite3.connect(f'file:{p}/views.sqlite?mode=ro', uri=True) for p in base_dirs}
    recovered = collections.Counter(); noise_rows = collections.Counter(); noise_fates = collections.Counter(); matter_fates = collections.Counter()
    totals = collections.Counter(); saved = {}; used = collections.Counter(); written_total = 0
    replay = json.loads(Path(args.replay).read_text(encoding='utf-8'))['answers'] if args.replay else None
    with ThreadPoolExecutor(SENDERS) as pool:
        jobs = []
        for iid in chosen:
            item = items[iid]
            objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
            shown = extraction.shown_views(ledger, cfg, item, objects)
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
            body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
            if replay is not None and iid not in replay:
                continue
            jobs.append((iid, None if replay is not None else [pool.submit(send, body) for _ in range(3)], shown, setting.prompt_version.rpartition('-')[2]))
        for iid, futures, shown, version in jobs:
            a = by_id[iid]; item = items[iid]; answers = replay[iid] if futures is None else [f.result() for f in futures]; saved[iid] = answers
            for ans in answers:
                for e in ans.get('evidence', []):
                    written_total += 1; used[classes(e)] += 1
            sifted = [filed(ans, item, shown, version) for ans in answers]
            stored_raw = [answer_of(ar, iid) for ar in archives]
            stored = [stored_filed(p, iid) for p in base_dirs]
            print(f"\n## {a['publication_day']} | {a['title'][:80]} | new sends wrote {[len(ans.get('evidence', [])) for ans in answers]}, reached {[len(ev) for ev, _ in sifted]}; stored draws reached {[len(ev) for ev in stored]}")
            for n in targets[iid]:
                it = a['items'][n]
                base_raw = sum(d[(iid, n)][0] != 'not extracted' for d in base if (iid, n) in d)
                base_reached = sum(any(sr.sg.same_matter(it, e) for e in ev) for ev in stored)
                new_raw = sum(any(sr.sg.same_matter(it, e) for e in ans.get('evidence', [])) for ans in answers)
                new_reached = sum(any(sr.sg.same_matter(it, e) for e in ev) for ev, _ in sifted)
                hits = [(e, fate) for ans, (ev, fate) in zip(answers, sifted) for e in ans.get('evidence', []) if sr.sg.same_matter(it, e)]
                for e, fate in hits:
                    matter_fates[(classes(e), 'reached' if fate.get(e['id']) == 'reached' else 'dropped')] += 1
                recovered[(base_reached, new_reached)] += 1
                totals.update(matter_stored_raw=base_raw, matter_stored_reached=base_reached, matter_new_raw=new_raw, matter_new_reached=new_reached)
                print(f"   {it['weight'][:4]} stored raw {base_raw} reached {base_reached} -> new raw {new_raw} reached {new_reached} | {it.get('span', '')[:90]} | " + '; '.join(label(e, f) for e, f in hits))
            not_kept = [x for x in a['not_kept'] if x['weight'] == 'not_kept']
            stored_noise_raw = [sum(written(x, evs) for x in not_kept) for evs in stored_raw]
            stored_noise_reached = [sum(written(x, ev) for x in not_kept) for ev in stored]
            new_noise_raw = [sum(written(x, ans.get('evidence', [])) for x in not_kept) for ans in answers]
            new_noise_reached = [sum(written(x, ev) for x in not_kept) for ev, _ in sifted]
            totals.update(noise_stored_raw=sum(stored_noise_raw), noise_stored_reached=sum(stored_noise_reached), noise_new_raw=sum(new_noise_raw), noise_new_reached=sum(new_noise_reached))
            print(f"   guard: gold not-kept, stored raw {stored_noise_raw} reached {stored_noise_reached} -> new raw {new_noise_raw} reached {new_noise_reached} of {len(not_kept)} listed")
            def also_kept(e):                                 # the same statement also carries a gold kept matter: a long quote spanning both
                return any(sr.sg.same_matter(it, e) for it in a['items'])
            totals.update(noise_stored_reached_double=sum(1 for ev in stored for e in ev if any(written(x, [e]) for x in not_kept) and also_kept(e)),
                          noise_new_reached_double=sum(1 for ev, _ in sifted for e in ev if any(written(x, [e]) for x in not_kept) and also_kept(e)))
            for x in not_kept:
                hits = [(e, fate) for ans, (ev, fate) in zip(answers, sifted) for e in ans.get('evidence', []) if written(x, [e])]
                if hits:
                    n_reached = sum(fate.get(e['id']) == 'reached' for e, fate in hits)
                    if n_reached:
                        noise_rows[(x.get('row') or '?')[:60]] += n_reached
                    for e, fate in hits:
                        noise_fates[(classes(e), 'reached' if fate.get(e['id']) == 'reached' else 'dropped')] += 1
                    print(f"      noise written x{len(hits)} reached x{n_reached} [{(x.get('row') or '?')[:36]}] {x['span'][:80]} | " + '; '.join(label(e, f) for e, f in hits))
    t = totals
    print(f"\nmatters by (stored reached, new reached): {dict(sorted(recovered.items()))}")
    print(f"matter presences: stored raw {t['matter_stored_raw']} reached {t['matter_stored_reached']} -> new raw {t['matter_new_raw']} reached {t['matter_new_reached']}")
    print(f"gold not-kept statements over the articles: stored raw {t['noise_stored_raw']} reached {t['noise_stored_reached']} -> new raw {t['noise_new_raw']} reached {t['noise_new_reached']}")
    print(f"   of the reached noise statements, those whose quote also carries a gold kept matter (a long quote, counted on both lists): stored {t['noise_stored_reached_double']} -> new {t['noise_new_reached_double']}")
    print('noise reaching the ledger in the new sends, by row: ' + '; '.join(f'{n} {k}' for k, n in noise_rows.most_common(8)))
    print('noise written in the new sends, by its news class and fate: ' + '; '.join(f'{k[0]} {k[1]} {n}' for k, n in sorted(noise_fates.items(), key=lambda kv: -kv[1])))
    print('gold matters written in the new sends, by its news class and fate: ' + '; '.join(f'{k[0]} {k[1]} {n}' for k, n in sorted(matter_fates.items(), key=lambda kv: -kv[1])))
    print(f'every statement written ({written_total}), by class: ' + '; '.join(f'{k} {n}' for k, n in used.most_common()))
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        Path(args.save).write_text(json.dumps({'config': cfg.version, 'base': base_dirs, 'answers': saved}, ensure_ascii=False), encoding='utf-8')
        print(f'answers saved to {args.save}')


if __name__ == '__main__':
    main()
