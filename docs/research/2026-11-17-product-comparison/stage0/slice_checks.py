"""The slice's pass checks (plan §2; D672). Run after both slice draws have ended; reads finished outputs only.

    python3 slice_checks.py <slice root> <until day>

1. both draws complete;
2. the new system's Step 1: mean seconds and dollars per article within 1.5 times the measured 34 s and $0.0102;
3. every answer-choice pass ran gpt-6-astra under the astra configuration;
4. the old system wrote a day line for every day and no failed or unprocessed item;
5. each draw processed exactly the manifest's items up to the until day, in order;
6. a day's state (the views and each view's latest judgement on or before a given day) can be read back from each store, every
   judgement's day known.
Prints PASS or FAIL per check; exit status 1 on any FAIL.
"""
import datetime
import json
import sqlite3
import sys
from pathlib import Path

ITEMS = Path('/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/items-comparison.sqlite')
MANIFEST = Path('/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/manifest-2026-07-01-09-20.json')
ASTRA = 'clean-ladder-stage-a 14d0e269c8fe0335'


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main(root, until_day):
    root = Path(root)
    results = []
    record = lambda name, ok, detail: results.append((name, ok, detail))
    items = ro(ITEMS)
    day_of = lambda i: (items.execute('select publication_day from items where input_id=?', (i,)).fetchone() or [None])[0]
    expected = [i for i in json.loads(MANIFEST.read_text())['item_ids'] if day_of(i) <= until_day]
    runs = {label: json.loads((root / label / 'run.json').read_text()) for label in ('s-new', 's-old')}
    record('1 both draws complete', all(r['state'] == 'complete' for r in runs.values()), {k: r['state'] for k, r in runs.items()})

    step1 = runs['s-new']['components']['step1']
    attempt = step1['attempts'][-1]
    t0 = datetime.datetime.strptime(attempt['started at'], '%Y-%m-%dT%H:%M:%S%z')
    t1 = datetime.datetime.strptime(attempt['ended at'], '%Y-%m-%dT%H:%M:%S%z')
    trace = ro(root / 's-new' / step1['folder'] / 'trace.sqlite')
    reserved = trace.execute('select count(*) from trace').fetchone()[0]
    calls = trace.execute('select sum(coalesce(cost_usd, 0)), count(*), sum(seconds) from model_calls').fetchone()
    per_article_s = (t1 - t0).total_seconds() / max(1, reserved)
    per_article_usd = (calls[0] or 0) / max(1, reserved)
    record('2 Step 1 time and cost per article', per_article_s <= 51 and per_article_usd <= 0.0153,
           {'articles': reserved, 'seconds per article': round(per_article_s, 1), 'usd per article (archive cost)': round(per_article_usd, 4)})

    ladder = root / 's-new' / runs['s-new']['components']['ladder']['folder']
    passes = {}
    for archive in sorted(ladder.glob('send-*/archive.sqlite')):
        conn = ro(archive)
        configs = sorted(f'{v} {c}' for v, c in conn.execute('select distinct config_version, config_checksum from model_calls'))
        models = sorted({json.loads(r[0]).get('model') for r in conn.execute('select request_json from model_calls')})
        passes[archive.parent.name] = (configs, models)
    record('3 every ladder pass on astra', len(passes) == 3 and all(c == [ASTRA] and m == ['gpt-6-astra'] for c, m in passes.values()), passes)

    log = (root / 's-old' / runs['s-old']['components']['prod']['folder'] / 'replay.log').read_text().splitlines()
    days = sorted({line[:10] for line in log if line[:4] == '2026' and ' | ' in line})
    want = []
    d = datetime.date(2026, 7, 1)
    while d.isoformat() <= until_day:
        want.append(d.isoformat())
        d += datetime.timedelta(days=1)
    totals = [line for line in log if line.startswith('totals: ')]
    record('4 old system: every day and no failure', days == want and totals and "'failed': 0" in totals[-1] and "'not_processed': 0" in totals[-1],
           {'days': len(days), 'totals': totals[-1][:160] if totals else None})

    new_order = [r[0] for r in trace.execute('select input_id from trace order by sequence')]
    old_store = ro(root / 's-old' / runs['s-old']['components']['prod']['folder'] / 'views.sqlite')
    seen, old_order = set(), []
    for (input_id,) in old_store.execute('select input_id from processing_steps where sequence_no > 0 order by sequence_no, id'):
        if input_id not in seen:
            seen.add(input_id)
            old_order.append(input_id)
    record('5 processed items equal the manifest, in order', new_order == expected and old_order == expected,
           {'manifest': len(expected), 'new': len(new_order), 'old': len(old_order),
            'new differs at': next((k for k, (a, b) in enumerate(zip(new_order, expected)) if a != b), None),
            'old differs at': next((k for k, (a, b) in enumerate(zip(old_order, expected)) if a != b), None)})

    state_day = (datetime.date.fromisoformat(until_day) - datetime.timedelta(days=2)).isoformat()
    states = {}
    for label, store in (('new', ro(root / 's-new' / runs['s-new']['components']['judge']['folder'] / f'draw-s-new' / 'views.sqlite')),
                         ('old', old_store)):
        views = [v for v in store.execute('select view_id, created_from_input from views') if (day_of(v['created_from_input']) or '9999') <= state_day]
        unknown = 0
        latest = {}
        for j in store.execute('select view_id, seq, input_id from judgements order by seq'):
            day = day_of(j['input_id']) if j['input_id'] else None
            if day is None:
                unknown += 1
                continue
            if day <= state_day:
                latest[j['view_id']] = j['seq']
        states[label] = {'day': state_day, 'views': len(views), 'judged views': len(latest), 'judgements of unknown day': unknown}
    record('6 a day state reads back', all(s['judgements of unknown day'] == 0 for s in states.values()), states)

    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {json.dumps(detail, ensure_ascii=False)[:400]}")
    if not all(ok for _, ok, _ in results):
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
