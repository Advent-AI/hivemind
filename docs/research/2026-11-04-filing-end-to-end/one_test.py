"""The one test (predictions-one-test.md): the custom-silicon question's last stored judging request in each frozen v108 draw, sent as stored
three times and three times with the draw's own ledger statements of the gold's q16 facts inserted in its evidence block, formatted by the
production code (`judging._lines_english` on `store.evidence_in_force` pieces). The request is rebuilt by `model.build_request` with the
judging-v7 schema and refused unless the as-stored rebuild has the stored archive key. Answers are saved beside this script.

usage: python3 one_test.py <out.json>
"""
import concurrent.futures
import json
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import measure_filing as mf  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

RUNS = f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03'
GOLD_ITEMS = ['i234', 'i139', 'i300', 'i155', 'i138']     # gold-v1 q16's decisive and implied items that the articles carry


def pieces_for(conn, items):
    """The ledger pieces stating each gold item (the corrected fact match over every piece in force under any question), deduplicated."""
    in_force = {}
    for (view_id,) in conn.execute('select view_id from views'):
        for p in store.evidence_in_force(conn, view_id):
            in_force.setdefault(p['evidence_id'], p)
    chosen = []
    for item_id in GOLD_ITEMS:
        item = items[item_id]
        candidates = [p for p in in_force.values() if any(s['input_id'] == item['input_id'] for s in p['sources'])]
        hit = mf.best([dict(p, one_line=p['one_line'], quote=p['quote']) for p in candidates], mf.item_text(item))
        if hit and hit['evidence_id'] not in [c['evidence_id'] for c in chosen]:
            chosen.append(hit)
    return chosen


def main():
    out = sys.argv[1]
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    items = {i['id']: i for i in json.load(open(f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json'))['items']}
    schema = judging.schema_for('judging-v7')
    jobs, meta = [], {}
    for draw in ('d1', 'd2', 'd3'):
        conn = sqlite3.connect(f'file:{RUNS}/{draw}/views.sqlite?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        archive = sqlite3.connect(f'file:{RUNS}/{draw}/archive.sqlite?mode=ro', uri=True)
        sha, rung = conn.execute("select request_sha256, rung from judgements where view_id='v16' order by seq desc limit 1").fetchone()
        stored = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])
        system = next(m['content'] for m in stored['messages'] if m['role'] == 'system')
        user = next(m['content'] for m in stored['messages'] if m['role'] == 'user')
        if model.request_identity(model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider))[1] != sha:
            raise SystemExit(f'{draw}: the rebuilt request is not the stored one; refusing to send')
        shown = set(re.findall(r'^- (e\d+) \[', user, re.M))
        added = [p for p in pieces_for(conn, items) if p['evidence_id'] not in shown]
        view = store.view(conn, 'v16')
        built = judging._lines_english(conn, 'v16', view, store.rungs_of(conn, 'v16'), added, [], None)   # the production formatting of these pieces
        start = next(i for i, line in enumerate(built) if line.startswith('[Evidence in view under this thesis')) + 1
        lines = []
        for line in built[start:]:
            if line.startswith('\n['):
                break
            lines.append(line)
        header = re.search(r'\[Evidence in view under this thesis, (\d+) items\]', user)
        with_facts = user.replace(header.group(0), f'[Evidence in view under this thesis, {int(header.group(1)) + len(added)} items]' + '\n' + '\n'.join(lines), 1)
        meta[draw] = {'stored_rung': rung, 'added': [(p['evidence_id'], p['one_line']) for p in added]}
        for arm, text in (('as_stored', user), ('with_facts', with_facts)):
            for n in range(3):
                jobs.append((draw, arm, n, system, text))

    def send(job):
        draw, arm, n, system, text = job
        reply = model.openai_transport(cfg.provider, model.build_request(cfg.rejudging, system, text, schema, 'judgement', cfg.provider))
        data = json.loads(reply['choices'][0]['message']['content'])
        return draw, arm, n, data['rung'], data['implied_outcome'], data['reasons']

    results = {d: {'as_stored': [], 'with_facts': [], **meta[d]} for d in meta}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for draw, arm, n, rung, implied, reasons in pool.map(send, jobs):
            results[draw][arm].append({'rung': rung, 'implied_outcome': implied, 'reasons': reasons})
    for draw, r in results.items():
        print(f'{draw}: added {[a[0] for a in r["added"]]} | as stored rungs {[x["rung"] for x in r["as_stored"]]} | with facts rungs {[x["rung"] for x in r["with_facts"]]}')
    json.dump(results, open(out, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
