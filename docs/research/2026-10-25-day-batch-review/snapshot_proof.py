"""Build real historical SQLite snapshots and compare complete extraction requests.

Each snapshot retains original IDs, sequence order and FTS text, and excludes
later writes. No model request is sent and no source database is modified.
"""
import argparse
import collections
import json
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import ARMS, ROOT, ITEM, connect  # noqa: E402
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe  # noqa: E402
from hivemind.views import store  # noqa: E402


def snapshot(source, before_seq, *, exclude_unordered=False):
    """Records strictly before a sequence, including original FTS insertion order."""
    dest = sqlite3.connect(':memory:')
    dest.row_factory = sqlite3.Row
    kept_views = {r['view_id'] for r in source.execute('select view_id from views where created_seq<?', (before_seq,))}
    for table, schema in store.TABLES.items():
        dest.execute(f'create table {table} ({schema})')
        rows = source.execute(f'select * from {table} order by rowid')
        for row in rows:
            fields = list(row.keys())
            sequence = next((f for f in ('created_seq', 'after_seq', 'seq', 'sequence_no') if f in fields), None)
            if exclude_unordered and sequence and row[sequence] == 0:
                continue
            if sequence and row[sequence] >= before_seq:
                continue
            if table == 'rungs' and row['view_id'] not in kept_views:
                continue
            dest.execute(f'insert into {table} ({",".join(fields)}) values ({",".join("?" for _ in fields)})', tuple(row))
    for table, id_field, records in [('views_fts', 'view_id', 'views'), ('groups_fts', 'group_id', 'thesis_groups')]:
        dest.execute(f'create virtual table {table} using fts5({id_field} unindexed, text, tokenize="trigram")')
        kept = {r[0] for r in dest.execute(f'select {id_field} from {records}')}
        for row in source.execute(f'select {id_field},text from {table} order by rowid'):
            if row[0] in kept:
                dest.execute(f'insert into {table} ({id_field},text) values (?,?)', tuple(row))
    return dest


def audit(folder, config):
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    counts, examples, mismatches = collections.Counter(), [], []
    with connect(ROOT / 'poc/data' / folder / 'views.sqlite') as source, connect(ROOT / 'poc/data' / folder / 'archive.sqlite') as archive, connect(ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite') as inputs:
        meta = {r['input_id']: dict(r) for r in source.execute('select input_id,min(sequence_no) seq,min(publication_day) day from processing_steps where sequence_no>0 group by input_id')}
        day_start = {}
        for row in meta.values():
            day_start[row['day']] = min(day_start.get(row['day'], row['seq']), row['seq'])
        requests = list(archive.execute("select request_json from model_calls where config_version=? and purpose='extract' order by call_id", (config,)))
        for row in requests:
            original = json.loads(row[0])
            input_id, day = ITEM.search(original['messages'][1]['content']).groups()
            item = dict(inputs.execute('select * from items where input_id=?', (input_id,)).fetchone())
            item['object_identifiers'] = json.loads(item['object_identifiers'])
            objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
            built = []
            for seq in (meta[input_id]['seq'], day_start[day]):
                db = snapshot(source, seq)
                try:
                    shown = store.views_for_prompt(db, objects)
                    groups = store.groups_for_prompt(db, objects, item['title'] or '')
                    built.append(extraction.build_prompt(item, item['text'], shown, uni, 'v10', groups))
                finally:
                    db.close()
            saved = tuple(m['content'] for m in original['messages'])
            counts['requests'] += 1
            if built[0] != saved:
                mismatches.append(input_id)
                continue
            counts['reproduced_original_request'] += 1
            if built[0] != built[1]:
                counts['different_at_day_start'] += 1
                if len(examples) < 3:
                    examples.append({'input_id': input_id, 'day': day, 'sequence': meta[input_id]['seq'], 'day_start_sequence': day_start[day]})
        return {'counts': dict(counts), 'examples': examples, 'reconstruction_mismatches': mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    results = {name: audit(*spec) for name, spec in ARMS.items()}
    with args.out.open('x') as handle:
        json.dump(results, handle, indent=2)
    for name, result in results.items():
        print(name, result['counts'], 'reconstruction mismatches', len(result['reconstruction_mismatches']))
    if any(v['reconstruction_mismatches'] for v in results.values()):
        raise SystemExit('historical reconstruction not exact: inspect mismatches before using the measure')


if __name__ == '__main__':
    main()
