"""The small comparison's reads, laid out per article for reading by hand ($0; DESIGN.md, "The reading").

  python3 read_probe.py <the run's reads folder> [--json <output>]

For each article, both reads: the topics it opened (as written), every statement it kept with where it filed it (an existing
topic, a topic it opened, or nowhere), and the read's status. It judges nothing.
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE / 'inputs'


def read(folder):
    trace = folder / 'trace.sqlite'
    if not trace.exists():
        return {'status': 'not run'}
    connection = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    try:
        row = connection.execute('select status, error, result, raw_response, before_state, after_state from trace').fetchone()
    finally:
        connection.close()
    if row is None or row[0] != 'complete':
        return {'status': row[0] if row else 'empty', 'error': row[1] if row else None}
    result, raw = json.loads(row[2]), json.loads(row[3])
    answer = json.loads(raw['choices'][0]['message']['content'])
    shown = {t['id'] for t in json.loads(row[4])}
    allocated = result.get('new_thesis_ids') or {}
    opened = [{'local_id': t['local_id'], 'id': allocated.get(t['local_id']), 'description': t['description'], 'outcome': t['outcome'],
               'period': t['period'], 'kept': t['local_id'] in allocated} for t in answer.get('new_theses', [])]
    statements = []
    for item in result.get('evidence', []):
        homes = []
        for link in item.get('links') or []:
            target = link.get('target_id')
            kind = 'existing' if target in shown else 'opened here' if target in allocated or link.get('target_type') == 'new' else link.get('target_type')
            homes.append({'to': allocated.get(target, target), 'kind': kind, 'why': link.get('relevance')})
        statements.append({'id': item['local_id'], 'summary': item['summary'], 'party': item.get('original_party'),
                           'passages': item.get('verified_source_passages') or item.get('source_passages'), 'homes': homes})
    return {'status': 'complete', 'opened': opened, 'statements': statements,
            'unfiled': result.get('unfiled_evidence'), 'unresolved_links': result.get('unresolved_links')}


def main(reads, output=None):
    reads = Path(reads)
    articles = json.loads((INPUTS / 'articles.json').read_text())
    carried = {t['id']: t['description'] for t in json.loads((INPUTS / 'initial-carried.json').read_text())}
    layout = []
    for article in articles:
        entry = {'sequence': article['sequence'], 'title': article['title'], 'day': article['publication_day'], 'stored_run_opened': article['opened']}
        for condition in ('empty', 'carried'):
            entry[condition] = read(reads / f"{article['sequence']:03d}-{condition}")
        layout.append(entry)
        print(f"\n##### {article['sequence']} ({article['publication_day']}) {article['title'][:90]}  [the stored October run opened {article['opened']}]")
        for condition in ('empty', 'carried'):
            r = entry[condition]
            if r['status'] != 'complete':
                print(f"  {condition}: {r['status']} {r.get('error') or ''}")
                continue
            filed = {}
            for statement in r['statements']:
                for home in statement['homes'] or [{'to': 'nowhere', 'kind': 'nowhere'}]:
                    filed.setdefault((home['kind'], home['to']), []).append(statement['id'])
            print(f"  {condition}: {len(r['statements'])} statements kept; opened {len(r['opened'])}")
            for topic in r['opened']:
                print(f"     OPENED {topic['id'] or '(dropped by code)'}: {topic['description'][:200]}")
            for (kind, target), ids in sorted(filed.items(), key=lambda pair: (pair[0][0], str(pair[0][1]))):
                name = carried.get(target, '') if kind == 'existing' else ''
                print(f"     {kind:<12} {str(target):<10} {len(ids):>2} statements {ids}  {name[:90]}")
    if output:
        Path(output).write_text(json.dumps(layout, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--json' else None)
