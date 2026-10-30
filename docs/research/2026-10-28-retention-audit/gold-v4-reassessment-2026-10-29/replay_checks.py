"""Replay the 48 stored extraction answers through current checks without a model call."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from hivemind import extraction, universe
from measure import measure, need, read


def replay(root, items_path, pages_path, universe_path):
    measure(root)
    records = read(root / 'assessments.json')['runs']
    expected = {x['run_id']: x for x in read(root / 'trace-checks.json')['source_and_sift_checks']}
    uni = universe.load(str(universe_path))
    sources = sqlite3.connect(items_path.resolve().as_uri() + '?mode=ro', uri=True)
    sources.row_factory = sqlite3.Row
    pages = sqlite3.connect(pages_path.resolve().as_uri() + '?mode=ro', uri=True)
    pairs = {}
    try:
        for r in records:
            item = dict(sources.execute('select * from items where input_id=?', (r['input_id'],)).fetchone())
            item['object_identifiers'] = json.loads(item['object_identifiers'])
            text = pages.execute('select text from items where input_id=?', (r['input_id'],)).fetchone()[0] if r['cohort'] == 'page' else item['text']
            need(hashlib.sha256(text.encode()).hexdigest() == expected[r['run_id']]['source_sha256'], 'source changed')
            q = read(root / r['request'])
            h = r['model'] == 'haiku'
            user = q['messages'][0 if h else 1]['content']
            system = q['system'] if h else q['messages'][0]['content']
            schema = q['output_config']['format']['schema'] if h else q['response_format']['json_schema']['schema']
            need(text in user, 'source not fully visible')
            pairs[r['request']] = (system, user, schema)
            answer = read(root / r['artifact'])
            e, c, d, g = extraction.sift_with_groups(answer['answer'], item, text, set(), uni, english=True, shown_group_ids=(), version='22', keep_unlinked=True)
            actual = json.loads(json.dumps(dict(evidence=e, candidates=c, dropped=d, new_groups=g)))
            need(actual == answer['sift'], 'sift changed: ' + r['run_id'])
        for name, triple in pairs.items():
            if '-haiku-' in name:
                need(triple == pairs[name.replace('-haiku-', '-gpt-')], 'explicit request mismatch')
    finally:
        sources.close()
        pages.close()
    return {'replayed': len(records), 'request_pairs': len(pairs) // 2, 'all_sources_visible': True, 'sift_matches': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--items', type=Path, required=True)
    p.add_argument('--pages', type=Path, required=True)
    p.add_argument('--universe', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(replay(Path(__file__).resolve().parent, args.items, args.pages, args.universe)))
