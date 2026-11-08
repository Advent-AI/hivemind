"""Reference v2: the two-question re-label (relation; material the later item adds and whether a source-only merge loses it).
v1 labels are kept as history in reference.json. No model calls.

Usage: reference_v2.py combine <folder>   agreement, adjudication packet for relation disputes
       reference_v2.py finalize <folder>  reference-v2.json and its summary"""
import collections, json, sys
from pathlib import Path


def passes(folder, reader):
    rows = {}
    for path in sorted(folder.glob(f'v2-answer-{reader}-*.json')):
        for row in json.loads(path.read_text()):
            rows[row['id']] = row
    return rows


def main():
    mode, folder = sys.argv[1], Path(sys.argv[2])
    key = json.loads((folder / 'v2-key.json').read_text())
    c, d = passes(folder, 'C'), passes(folder, 'D')
    if mode == 'combine':
        both = [vid for vid in key if vid in c and vid in d]
        agree = sum(1 for vid in both if c[vid]['relation'] == d[vid]['relation'])
        print(f'pairs {len(key)}; labelled by both {len(both)}; relation agreement {agree}/{len(both)} = {agree / max(1, len(both)):.1%}')
        print('disagreements:', collections.Counter((c[v]['relation'], d[v]['relation']) for v in both if c[v]['relation'] != d[v]['relation']).most_common(8))
        source = {}
        for path in sorted(folder.glob('v2-packet-*.json')):
            for row in json.loads(path.read_text()):
                source[row['id']] = row
        packet = [dict(source[v], first_relations=[c[v]['relation'], d[v]['relation']]) for v in both if c[v]['relation'] != d[v]['relation']]
        (folder / 'v2-adjudication-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        print('adjudication packet', len(packet))
        return
    third = {}
    for path in folder.glob('v2-adjudication-answer*.json'):
        for row in json.loads(path.read_text()):
            third[row['id']] = row
    reference = []
    for vid, pair in key.items():
        if vid not in c or vid not in d:
            continue
        if c[vid]['relation'] == d[vid]['relation']:
            relation = c[vid]['relation']
            loses = c[vid]['source_only_merge_loses'] or d[vid]['source_only_merge_loses']
            added = c[vid]['added_material'] if len(c[vid]['added_material']) >= len(d[vid]['added_material']) else d[vid]['added_material']
        elif vid in third:
            relation, loses, added = third[vid]['relation'], third[vid]['source_only_merge_loses'], third[vid]['added_material']
        else:
            continue
        reference.append({'id': vid, **pair, 'relation': relation, 'source_only_merge_loses': bool(loses), 'added_material': added})
    (folder / 'reference-v2.json').write_text(json.dumps(reference, indent=1))
    print('reference v2 pairs', len(reference), dict(collections.Counter(r['relation'] for r in reference)))
    same = [r for r in reference if r['relation'] == 'same_statement']
    print(f"same_statement pairs where a source-only merge loses material: {sum(r['source_only_merge_loses'] for r in same)}/{len(same)}")
    print('v1 → v2 relation:', collections.Counter((r['v1_label'], r['relation']) for r in reference).most_common(12))


if __name__ == '__main__':
    main()
