"""Combine the two blind label passes, build the adjudication packet for disagreements, and, once adjudicated, write reference.json and
score retrieval (no model calls).

Usage:
  adjudicate.py combine <folder>    agreement table; writes adjudication-packet.json for pairs whose labels differ
  adjudicate.py finalize <folder>   merges agreed labels with the third reader's verdicts into reference.json; scores recall at 10"""
import collections, json, sys
from pathlib import Path

POSITIVE = ('repeat', 'revision')


def passes(folder, reader):
    rows = {}
    for path in sorted(folder.glob(f'label-answer-{reader}-*.json')):
        for row in json.loads(path.read_text()):
            rows[row['id']] = row
    return rows


def combine(folder):
    key = json.loads((folder / 'label-key.json').read_text())
    a, b = passes(folder, 'A'), passes(folder, 'B')
    missing = [pid for pid in key if pid not in a or pid not in b]
    agree = collections.Counter()
    disputed = []
    for pid, pair in key.items():
        if pid in missing:
            continue
        la, lb = a[pid]['label'], b[pid]['label']
        agree[(la, lb)] += 1
        if la != lb:
            disputed.append(pid)
    total = len(key) - len(missing)
    same = sum(v for (x, y), v in agree.items() if x == y)
    print(f'pairs {len(key)}; labelled by both {total}; missing {len(missing)}; agreement {same}/{total} = {same / max(1, total):.1%}')
    print('agreed labels:', collections.Counter(x for (x, y), v in agree.items() for _ in range(v) if x == y))
    print('disagreements by label pair:', sorted(((x, y, v) for (x, y), v in agree.items() if x != y), key=lambda t: -t[2])[:10])
    source = {}
    for path in sorted(folder.glob('label-packet-*.json')):
        for row in json.loads(path.read_text()):
            source[row['id']] = row
    packet = [dict(source[pid], first_labels=[a[pid]['label'], b[pid]['label']]) for pid in disputed]
    (folder / 'adjudication-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print('adjudication packet:', len(packet))


def finalize(folder):
    key = json.loads((folder / 'label-key.json').read_text())
    a, b = passes(folder, 'A'), passes(folder, 'B')
    third = {}
    for path in sorted(folder.glob('adjudication-answer*.json')):
        for row in json.loads(path.read_text()):
            third[row['id']] = row
    reference = []
    for pid, pair in key.items():
        if pid not in a or pid not in b:
            continue
        if a[pid]['label'] == b[pid]['label']:
            label, richer = a[pid]['label'], a[pid].get('richer') or b[pid].get('richer')
        elif pid in third:
            label, richer = third[pid]['label'], third[pid].get('richer', False)
        else:
            continue
        drift = bool(a[pid].get('summary_drift') or b[pid].get('summary_drift'))
        reference.append({'id': pid, **pair, 'label': label, 'richer': bool(richer) and label == 'repeat', 'summary_drift': drift})
    (folder / 'reference.json').write_text(json.dumps(reference, indent=1))
    labels = collections.Counter(r['label'] for r in reference)
    print('reference pairs', len(reference), dict(labels), '| richer repeats', sum(r['richer'] for r in reference), '| summary drift flagged', sum(r['summary_drift'] for r in reference))
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    positives = collections.defaultdict(set)
    for r in reference:
        if r['label'] in POSITIVE:
            positives[r['later']].add(r['earlier'])
    retrieval = json.loads((folder / 'retrieval.json').read_text())
    by_item = collections.defaultdict(lambda: collections.defaultdict(set))
    for row in retrieval:
        for arm in ('R0', 'R0e', 'R1', 'R2'):
            by_item[row['key']][arm].update(row[arm])
    print(f'later items with at least one true repeat or revision: {len(positives)} of {len(items)}; true positive pairs {sum(len(v) for v in positives.values())}')
    for arm in ('R0', 'R0e', 'R1', 'R2'):
        found_any = sum(1 for k, earl in positives.items() if earl & by_item[k][arm])
        pairs_found = sum(len(earl & by_item[k][arm]) for k, earl in positives.items())
        cross = [(k, e) for k, earl in positives.items() for e in earl if not ({t['id'] for t in items[k]['theses']} & {t['id'] for t in items[e]['theses']})]
        cross_found = sum(1 for k, e in cross if e in by_item[k][arm])
        print(f'  {arm:4s} items with a counterpart in top 10: {found_any}/{len(positives)}; pairs {pairs_found}/{sum(len(v) for v in positives.values())}; cross-thesis pairs {cross_found}/{len(cross)}')
    sample = {s['key'] for s in json.loads((folder / 'exhaustive-sample.json').read_text())}
    candidates = {(p['earlier'], p['later']) for p in json.loads((folder / 'candidate-pairs.json').read_text())}
    sample_pos = [(e, k) for k, earl in positives.items() if k in sample for e in earl]
    missed = [p for p in sample_pos if p not in candidates]
    print(f'exhaustive sample: true positive pairs {len(sample_pos)}; not produced by the candidate routes {len(missed)}')


if __name__ == '__main__':
    {'combine': combine, 'finalize': finalize}[sys.argv[1]](Path(sys.argv[2]))
