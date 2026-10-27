"""Step 1 at scale, extraction only: every item of a day range that has a stored request in the paused run's archive is
sent once with a system prompt file (the cleaned text, production key order, the B-arm closing line and T8 block), and
the answer is sifted by the current code checks. Reports per category: items, empty answers (model), pieces kept per
item, pieces dropped and why, links per piece, cost; and lists ten random items with their kept pieces for reading.
Run: python3 scale.py <arm> <system file> <run folder> <cleaned items db> <scratch archive> <from-day> <until-day>"""
import collections
import concurrent.futures
import json
import os
import random
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '2026-10-27-evidence-gate'))
from hivemind import extraction, model, universe as universe_module  # noqa: E402
from benchmark import send  # noqa: E402
from benchmark_clean import with_clean_text  # noqa: E402
from wire_order import restore  # noqa: E402
from arm import OLD_CLOSING, NEW_CLOSING, T8_READ_OLD, T8_READ_NEW  # noqa: E402


def main(arm, system_file, run, items_db, scratch, from_day, until_day):
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{items_db}?mode=ro', uri=True); items.row_factory = sqlite3.Row
    uni = universe_module.load(os.path.join(ROOT, 'poc', 'universe.json'))
    archive = model.Archive(scratch)
    system = open(system_file, encoding='utf-8').read()
    requests = {}
    for (req,) in stored.execute("select request_json from model_calls where purpose='extract' and request_sha256 not like '%:%' order by call_id"):
        user = json.loads(req)['messages'][1]['content']
        iid = re.search(r'\[Item\] id (\S+),', user).group(1); day = re.search(r'published (\d{4}-\d{2}-\d{2})', user).group(1)
        if from_day <= day <= until_day:
            requests[iid] = req                                   # the last stored request per item: the one accepted at its turn
    stats = collections.defaultdict(lambda: collections.Counter()); dropped_reasons = collections.Counter(); samples = []; total = 0.0
    def prepare(iid, req):
        row = items.execute('select * from items where input_id=?', (iid,)).fetchone()
        if row is None or not row['text']:
            return None
        request = with_clean_text(restore(json.loads(req)), iid, row['text'])
        request['messages'][0]['content'] = system
        request['messages'][1]['content'] = request['messages'][1]['content'].replace(OLD_CLOSING, NEW_CLOSING).replace(T8_READ_OLD, T8_READ_NEW)
        return dict(row), request
    prepared = {iid: prepare(iid, req) for iid, req in requests.items()}
    prepared = {iid: v for iid, v in prepared.items() if v}
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('ARM_WORKERS', '8'))) as pool:
        futures = {iid: pool.submit(send, archive, request, 'low', purpose=f'scale:{arm}') for iid, (row, request) in prepared.items()}
        answers = {iid: f.result() for iid, f in futures.items()}
    for iid, (row, request) in prepared.items():
        user = request['messages'][1]['content']
        shown = set(re.findall(r'\n  - (v\d+) \(', user.split('[Research groups]')[0]))
        pieces, reasoning, cost, seconds = answers[iid]
        total += cost
        data = {'evidence': pieces, 'candidates': [], 'new_groups': []}
        evidence, candidates, dropped = extraction.sift(data, row, row['text'], shown, uni, english=True)
        cat = row['category']; st = stats[cat]
        st['items'] += 1; st['empty'] += not pieces; st['pieces'] += len(pieces); st['kept'] += len(evidence); st['dropped'] += len(dropped)
        st['linked'] += sum(1 for p in pieces if p['links']); st['cost'] += cost
        for d in dropped: dropped_reasons[(d[1] if isinstance(d, list) else str(d)).split(':')[0][:40]] += 1
        samples.append((iid, cat, row['publisher'], (row['title'] or '')[:70], [(e['tier'], e['links'], e['one_line'][:110]) for e in evidence], len(pieces)))
    print(f'arm {arm}: {sum(s["items"] for s in stats.values())} items, USD {total:.4f}')
    print('| category | items | empty (model) | pieces per item | kept per item | linked share of pieces | dropped |')
    print('|---|---|---|---|---|---|---|')
    for cat, s in sorted(stats.items(), key=lambda kv: -kv[1]['items']):
        n = s['items']; print(f"| {cat} | {n} | {s['empty']} ({s['empty']/n:.0%}) | {s['pieces']/n:.1f} | {s['kept']/n:.1f} | {s['linked']/max(1,s['pieces']):.0%} | {s['dropped']} |")
    print('dropped by reason:', dict(dropped_reasons.most_common(6)))
    random.seed(1)
    for iid, cat, pub, title, kept, n in random.sample(samples, min(10, len(samples))):
        print(f'\n-- {iid} {cat} {pub} | {title} | {n} pieces, {len(kept)} kept')
        for tier, links, line in kept[:10]: print(f"     [{tier[:5]}] {','.join(links) or '-':10} {line}")


if __name__ == '__main__':
    main(*sys.argv[1:8])
