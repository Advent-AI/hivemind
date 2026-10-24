"""Measure D143's fixed source passages and show actual destinations for human review."""
import argparse
import json
from pathlib import Path

import ingestion_groups as base
import study


def review(out):
    items = json.loads((out / 'items.json').read_text())
    sealed = study.read_only(base.SEALED)
    anchors = []
    for item_index, evidence_id in [(0, 'e7'), (1, 'e55'), (2, 'e724')]:
        body = base.extraction.normalise(items[item_index]['text'])
        quote = base.extraction.normalise(sealed.execute('select quote from evidence where evidence_id=?', (evidence_id,)).fetchone()[0])
        start = body.find(quote)
        if start < 0:
            raise ValueError(f'Known source passage absent: {evidence_id}')
        anchors.append((body, start, start + len(quote)))
    sealed.close()
    results, totals = [], {}
    for folder in sorted(out.glob('sample-*')):
        arm = folder.name.rsplit('-', 1)[-1]
        total = totals.setdefault(arm, {'calls': 0, 'estimated_usd': 0, 'input_tokens': 0, 'output_tokens': 0})
        for path in folder.glob('item*.json'):
            call = json.loads(path.read_text())
            if 'request' not in call:
                continue
            total['calls'] += 1
            for key in ['estimated_usd', 'input_tokens', 'output_tokens']:
                total[key] += call.get(key, 0)
        events = [json.loads(path.read_text()) for path in sorted(folder.glob('item*-result.json'))]
        conn = study.read_only(folder / 'views.sqlite')
        passages = []
        for seq, (body, left, right) in enumerate(anchors, 1):
            hits = []
            for row in conn.execute('select * from evidence where created_seq=?', (seq,)):
                quote = base.extraction.normalise(row['quote'])
                start = body.find(quote)
                if start >= 0 and start < right and start + len(quote) > left:
                    destinations = [dict(r) for r in conn.execute('select v.view_id,v.question from views v join evidence_links l on l.view_id=v.view_id where l.evidence_id=?', (row['evidence_id'],))]
                    hits.append({'evidence_id': row['evidence_id'], 'quote': row['quote'], 'destinations': destinations})
            passages.append(hits)
        shipments = {v['view_id'] for e in passages[0] for v in e['destinations']}
        deployments = {v['view_id'] for e in passages[1] for v in e['destinations']}
        common = []
        if len(events) >= 2:
            for group in events[1]['groups']:
                members = {m['view_id'] for m in events[1]['members'] if m['group_id'] == group['group_id']}
                if any(s != d and s in members and d in members for s in shipments for d in deployments):
                    common.append(group)
        risk_ids = {v['view_id'] for e in passages[2] for v in e['destinations']}
        affected = set(events[2]['affected_groups']) if len(events) == 3 else set()
        shared_ids = {g['group_id'] for g in common}
        later_ids = {g['group_id'] for g in events[-1]['groups']} if events else set()
        result = {'stream': folder.name, 'completed_articles': len(events), 'passages': passages,
                  'shared_groups': common, 'risk_reaches_shipments': bool(risk_ids & shipments),
                  'shared_group_affected': bool(shared_ids & affected),
                  'risk_marks_shared_group': bool(risk_ids & shipments) and bool(shared_ids & affected),
                  'shared_group_identity_retained': bool(shared_ids) and shared_ids <= later_ids,
                  'events': events,
                  'resend': json.loads((folder / 'resend.json').read_text()) if (folder / 'resend.json').exists() else None,
                  'failure': json.loads((folder / 'failed.json').read_text()) if (folder / 'failed.json').exists() else None}
        results.append(result)
        conn.close()
    report = {'streams': results, 'totals': totals, 'source_anchors': ['e7', 'e55', 'e724'],
              'note': 'Quote-span matches expose destinations for manual review; no title-substring scoring.'}
    study.write_json(out / 'measurements.json', report)
    for r in results:
        print(r['stream'], 'completed', r['completed_articles'], 'shared', len(r['shared_groups']),
              'risk', r['risk_reaches_shipments'], 'affected', r['risk_marks_shared_group'], 'failure', r['failure'])
    print(json.dumps(totals, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    review(parser.parse_args().out.resolve())
