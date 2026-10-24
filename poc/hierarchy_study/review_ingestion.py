"""Read the article-level traces and count grouping outcomes; no model calls or source writes."""
import argparse
import json
from pathlib import Path
import sqlite3

import ingestion_groups as ingest
import study


def review(source, verified):
    items = json.loads((source / 'items.json').read_text())
    body = ingest.extraction.normalise(items[2]['text'])
    frozen = study.read_only(ingest.SEALED)
    target = ingest.extraction.normalise(frozen.execute("select quote from evidence where evidence_id='e724'").fetchone()[0])
    frozen.close()
    start = body.find(target)
    if start < 0:
        raise ValueError('Known delay source not located in the real input')
    streams, bridges = [], []
    totals = {'control': {'calls': 0, 'estimated_usd': 0}, 'grouped': {'calls': 0, 'estimated_usd': 0}}
    for folder in sorted(source.glob('sample-*')):
        arm = folder.name.split('-')[-1]
        events = [json.loads((folder / f'item{index}-result.json').read_text()) for index in [1, 2, 3]]
        conn = study.read_only(folder / 'views.sqlite')
        risk = []
        for row in conn.execute('select * from evidence where created_seq=3'):
            quote = ingest.extraction.normalise(row['quote'])
            offset = body.find(quote)
            if offset >= 0 and offset < start + len(target) and offset + len(quote) > start:
                risk.append({'evidence_id': row['evidence_id'], 'quote': row['quote'],
                             'view_ids': [r[0] for r in conn.execute('select view_id from evidence_links where evidence_id=?', (row['evidence_id'],))]})
        groups = events[-1]['groups']
        members = events[-1]['members']
        streams.append({'stream': folder.name, 'completed': 3, 'view_counts': [len(e['views']) for e in events],
                        'group_count': len(groups),
                        'singleton_groups': sum(sum(m['group_id'] == g['group_id'] for m in members) == 1 for g in groups),
                        'risk_links': risk, 'resend': json.loads((folder / 'resend.json').read_text())})
        if arm == 'grouped':
            hints = json.loads((folder / 'item2-extract.json').read_text())['answer']['relationship_hints']
            event = events[1]
            for hint in hints:
                child = event['new_views'].get(hint['candidate_id'])
                common = []
                for group in event['groups']:
                    ids = {m['view_id'] for m in event['members'] if m['group_id'] == group['group_id']}
                    if child in ids and ids.intersection(hint['related_view_ids']):
                        common.append(group['group_id'])
                bridges.append({'stream': folder.name, 'child': child, 'related': hint['related_view_ids'],
                                'question': hint['broader_question'], 'common_groups': common})
        for path in folder.glob('item*.json'):
            raw = json.loads(path.read_text())
            if 'request' in raw:
                totals[arm]['calls'] += 1
                totals[arm]['estimated_usd'] += raw['estimated_usd']
        conn.close()
    if len(streams) != 6 or len(bridges) != 3:
        raise ValueError('The fixed experiment population is incomplete')
    replayed = json.loads((verified / 'summary.json').read_text())
    result = {'streams': streams, 'bridges': bridges, 'totals': totals,
              'corrected_affected_events': replayed['corrected_affected_events'],
              'projected_associations': replayed['retained_extraction_relations']}
    study.write_json(source / 'measurements.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--verified', required=True, type=Path)
    args = parser.parse_args()
    review(args.source.resolve(), args.verified.resolve())
