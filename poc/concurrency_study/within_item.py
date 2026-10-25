"""Live serial/parallel Jev comparison on one unchanged real matching phase."""
import copy
import json
from pathlib import Path
import statistics
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot
from hivemind import config, extraction, model, universe
from hivemind.views import jev_matching, matching, store
from concurrency_study.budget import GuardedTransport, single_attempt_http, envelope
from concurrency_study.full_day import readonly
from concurrency_study.ingestion import StudyTransport

BASE = ROOT / 'poc/reports/2026-10-25-full-day-canonical'
OUT = ROOT / 'poc/reports/2026-10-25-within-item-parallel'
ORDER = ('serial-1', 'parallel-1', 'parallel-2', 'serial-2', 'serial-3', 'parallel-3')


def inputs():
    cfg, uni = config.load(ROOT / 'poc/config/poc-v23.json'), universe.load(ROOT / 'poc/universe.json')
    with readonly(BASE / 'views.sqlite') as source:
        # Largest actual first matching phase fitting six samples within the
        # original remaining 34-request allowance. No candidate is fabricated.
        possible = [(len(json.loads(r['shown_json']).get('requests', [])), dict(r))
                    for r in source.execute('select * from match_records where seq>=85 and call_no=1')]
        size, row = max(((n, r) for n, r in possible if 2 <= n <= 5), key=lambda entry: entry[0])
        conn = snapshot(source, row['seq'], exclude_unordered=True)
        conn.commit()
        hand = json.loads(source.execute('select handover_json from handovers where input_id=?', (row['input_id'],)).fetchone()[0])
    with readonly(BASE / 'items.sqlite') as source:
        item = dict(source.execute('select * from items where input_id=?', (row['input_id'],)).fetchone())
        item['object_identifiers'] = json.loads(item['object_identifiers'])
    expected = {r['request_sha256'] for r in json.loads(row['shown_json'])['requests']}
    assert size == len(expected) == 5
    return cfg, uni, conn, item, hand, expected


def decide(conn, archive, cfg, uni, item, hand, workers, transport):
    hand = copy.deepcopy(hand)
    packet = extraction.Handover(hand['evidence'], hand['candidates'], hand['dropped'], 0, '', True, 0,
                                 hand.get('new_groups', []))
    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
    shown = store.views_for_prompt(conn, objects)
    lists = matching.build_lists(conn, packet, shown, cfg.search_top_n)
    answer = jev_matching.decide(archive, cfg, conn, item, packet.candidates, packet.evidence, lists, shown,
                                workers=workers, transport=transport)
    checked = matching.check(conn, uni, answer.data, packet.candidates, packet.evidence, lists, shown)
    outcome = {'candidates': [{k: r.get(k) for k in ('id', 'outcome', 'target_view_id', 'dependencies')}
                              for r in answer.data['candidates']],
               'evidence': [{k: r.get(k) for k in ('id', 'view_id', 'outcome', 'target_evidence_id')}
                            for r in answer.data['evidence']],
               'groups': {r['id']: sorted(r.get('jev_group_refs', [])) for r in packet.candidates}}
    return answer, checked, outcome


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'manifest.json').exists():
        raise ValueError('study already attempted')
    cfg, uni, conn, item, hand, expected = inputs()
    with readonly(BASE / 'archive.sqlite') as db:
        known = {r['request_sha256']: dict(r) for r in db.execute('select * from model_calls')}
    requests = []
    def recorded(request):
        sha = model.request_identity(request)[1]
        assert sha in expected and sha in known
        requests.append(request)
        return json.loads(known[sha]['response_json'])
    offline = model.Archive(OUT / 'offline.sqlite')
    answer, checked, _ = decide(conn, offline, cfg, uni, item, hand, 1, recorded)
    assert not checked.refusals and len(requests) == 5
    offline.conn.close()
    allocation = json.loads((BASE / 'allocation.json').read_text())
    with readonly(BASE / 'budget.sqlite') as db:
        current_count = db.execute('select count(*) from attempts').fetchone()[0]
        held = db.execute('select sum(coalesce(charged,reserved)) from attempts').fetchone()[0]
        assert db.execute("select count(*) from attempts where state!='complete'").fetchone()[0] == 0
    assert current_count + 30 <= allocation['max_calls']
    assert held + sum(envelope('jev', r)[0] for r in requests) <= allocation['remaining_cap_microdollars']
    (OUT / 'manifest.json').write_text(json.dumps({'source': item['input_id'], 'day': item['publication_day'],
        'requests': sorted(expected), 'samples': list(ORDER), 'workers': [1, 8], 'physical_request_limit': 30,
        'budget_journal': str(BASE / 'budget.sqlite'), 'note': 'Same five requests; same snapshot; no product writes.'}, indent=2))
    active = peak = 0
    lock = threading.Lock()
    prepare = single_attempt_http()
    def measured(provider, request):
        send = prepare(provider, request)
        def call():
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            try:
                return send()
            finally:
                with lock:
                    active -= 1
        return call
    guard = GuardedTransport(BASE / 'budget.sqlite', measured,
        cap_microdollars=allocation['remaining_cap_microdollars'], max_calls=allocation['max_calls'])
    transport = StudyTransport(guard, workers=8)
    results = []
    for name in ORDER:
        peak = 0
        folder = OUT / name
        folder.mkdir()
        archive = model.Archive(folder / 'archive.sqlite')
        start = time.perf_counter()
        answer, checked, outcome = decide(conn, archive, cfg, uni, item, hand,
            8 if name.startswith('parallel') else 1, transport)
        seconds = time.perf_counter() - start
        assert not checked.refusals
        assert {r['request_sha256'] for r in answer.request_records} == expected
        assert archive.totals()[0] == 5
        result = {'name': name, 'seconds': seconds, 'peak_inflight': peak, 'outcomes': outcome,
                  'calls': answer.request_records, 'cost_usd': answer.cost_usd}
        (folder / 'result.json').write_text(json.dumps(result, indent=2))
        results.append(result)
        archive.conn.close()
        print(json.dumps({k: result[k] for k in ('name', 'seconds', 'peak_inflight', 'cost_usd')}), flush=True)
    serial = [r['seconds'] for r in results if r['name'].startswith('serial')]
    parallel = [r['seconds'] for r in results if r['name'].startswith('parallel')]
    summary = {'results': results, 'serial_median_seconds': statistics.median(serial),
               'parallel_median_seconds': statistics.median(parallel),
               'ratio_of_medians': statistics.median(serial)/statistics.median(parallel),
               'outcome_sets_equal': all(r['outcomes'] == results[0]['outcomes'] for r in results),
               'scope': 'One live matching phase; not whole-pipeline speed.', 'budget': guard.summary()}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: summary[k] for k in ('serial_median_seconds', 'parallel_median_seconds', 'ratio_of_medians', 'outcome_sets_equal')}), flush=True)


if __name__ == '__main__':
    run()
