"""Audit stored pipeline transitions; no model calls or writes to source ledgers."""
import collections
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def open_read(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def audit():
    ledgers = []
    for path in sorted((ROOT / 'poc/data').glob('views-2026-10-25-v15-*.sqlite')):
        conn = open_read(path)
        counts = collections.Counter()
        counts['views'] = conn.execute('select count(*) from views').fetchone()[0]
        counts['handovers'] = conn.execute('select count(*) from handovers').fetchone()[0]
        stale, pending = [], []
        for rec in conn.execute("select * from processing_steps where step='extracted' and result='ok'"):
            if not rec['reason'].endswith(' (parallel)'):
                continue
            counts['parallel_extractions'] += 1
            earlier = [r[0] for r in conn.execute('''select v.view_id from views v join processing_steps p
                on p.input_id=v.created_from_input and p.step='written' and p.result='ok'
                where p.publication_day=? and v.created_seq<?''', (rec['publication_day'], rec['sequence_no']))]
            if earlier:
                stale.append({'seq': rec['sequence_no'], 'input_id': rec['input_id'], 'earlier_same_day_views': earlier})
            if not conn.execute("select 1 from processing_steps where input_id=? and step='handed_over' and result='ok'", (rec['input_id'],)).fetchone():
                pending.append(rec['input_id'])
        mixed = []
        for h in conn.execute('select * from handovers'):
            handover = json.loads(h['handover_json'])
            cids = {c['id'] for c in handover['candidates']}
            decisions = {}
            for rec in conn.execute('select * from match_records where seq=? order by id', (h['seq'],)):
                answer = json.loads(rec['decisions_json'])
                listed = json.loads(rec['shown_json'])
                counts['match_calls'] += 1
                for d in answer['candidates']:
                    decisions[d['id']] = d
                    counts['candidate_decisions'] += 1
                    counts['new_with_candidates'] += int(d['outcome'] == '新观点' and bool(listed['candidates'].get(d['id'])))
                for d in answer['evidence']:
                    counts['unrequested_evidence_decisions'] += int(d['id'] + '|' + d['view_id'] not in listed['evidence'])
            for e in handover['evidence']:
                direct = [v for v in e['links'] if v not in cids]
                merged = [v for v in e['links'] if decisions.get(v, {}).get('outcome') == '归入已有的']
                if direct and merged:
                    mixed.append([h['seq'], e['id'], direct, merged])
        ledgers.append({'ledger': path.name, 'counts': dict(counts), 'stale_exposure': stale,
                        'unfinished_parallel': pending, 'split_evidence_comparisons': mixed})
        conn.close()
    conn = open_read(ROOT / 'poc/data/views-2026-10-25-v15-T4c.sqlite')
    archive = open_read(ROOT / 'poc/data/keyed-2026-10-25/archive-T2.sqlite')
    cases = []
    # Initial source-based hypotheses, NOT scoring labels. Review later revoked 165:
    # its annual actual funding is not the old guarantee amount (see design-review.txt).
    expectations = {116: {'c1': 'v17', 'c3': 'new', 'c4': 'v18'},
                    126: {'c1': 'v17', 'c2': 'v18'}, 147: {'c1': 'v17'}, 165: {'c1': 'v17'}}
    for seq, expected in expectations.items():
        rec = dict(conn.execute('select * from match_records where seq=? and call_no=1', (seq,)).fetchone())
        h = dict(conn.execute('select * from handovers where seq=?', (seq,)).fetchone())
        call = dict(archive.execute('select * from model_calls where request_sha256=?', (rec['request_sha256'],)).fetchone())
        handover = json.loads(h['handover_json'])
        shown = json.loads(rec['shown_json'])
        answer = json.loads(rec['decisions_json'])
        for cid, target in expected.items():
            if target != 'new':
                assert target in shown['candidates'][cid], (seq, cid, target)
        cases.append({'seq': seq, 'input_id': h['input_id'], 'expected': expected,
                      'listed': shown, 'answer': answer, 'handover': handover,
                      'request': json.loads(call['request_json']), 'call_id': call['call_id'],
                      'historical_cost_usd': call['cost_usd']})
    control = next(x for x in ledgers if x['ledger'].endswith('T4c.sqlite'))
    assert control['counts']['parallel_extractions'] == 255
    assert len(control['stale_exposure']) == 195
    assert sum(x['counts'].get('match_calls', 0) for x in ledgers) == 518
    return {'ledgers': ledgers, 'identity_cases': cases,
            'limits': 'Independent storage runs share input answers; exposures are not semantic errors. Case expectations are assistant source review.'}


if __name__ == '__main__':
    result = audit()
    (OUT / 'census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'ledgers': [{**x['counts'], 'name': x['ledger'], 'stale_exposure': len(x['stale_exposure']),
                                  'unfinished_parallel': len(x['unfinished_parallel']), 'mixed': len(x['split_evidence_comparisons'])} for x in result['ledgers']],
                      'identity_cases': [{'seq': x['seq'], 'expected': x['expected'], 'listed': x['listed']['candidates']} for x in result['identity_cases']]}, ensure_ascii=False, indent=2))
