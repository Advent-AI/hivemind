"""Tally the acceptance readers' Step 1 verdicts (no model calls; the readers judge, this only counts and lists disagreements).

Inputs: the judging packet, and each reader's batch answers (`<folder>/judge-<reader>-<n>.json`, reader A and B). With `--third
<file>`, the third reader's rulings on the disputed cases are applied. A case still split after the third reader counts against the
system (protocol §5).

Counts:
- settled matters kept, by both readers, after the third reader;
- opened theses judged wrong;
- links judged wrong;
- kept items by verdict.

`--disputes <file>` writes every case where A and B differ, for the third reader.

Usage: tally_acceptance.py <packet.json> <answers folder> [--disputes out.json] [--third third.json]"""
import collections, json, sys
from pathlib import Path


def load(path):
    text = Path(path).read_text()
    return json.loads(text[text.find('{'):text.rfind('}') + 1])


def main():
    packet = json.loads(Path(sys.argv[1]).read_text())
    folder = Path(sys.argv[2])
    verdicts = {}
    for reader in 'AB':
        articles = {}
        for path in sorted(folder.glob(f'judge-{reader}-*.json')):
            for entry in load(path)['articles']:
                articles[entry['article']] = entry
        verdicts[reader] = articles
    expected = {e['article'] for e in packet}
    for reader in 'AB':
        missing = expected - set(verdicts[reader])
        if missing:
            raise SystemExit(f'reader {reader} did not judge articles {sorted(missing)}')
    third = load(sys.argv[sys.argv.index('--third') + 1]) if '--third' in sys.argv else {'rulings': []}
    ruling = {(r['kind'], r['article'], r['key']): r['judgement'] for r in third['rulings']}
    disputes, counts = [], collections.Counter()
    for entry in packet:
        number = entry['article']
        a, b = verdicts['A'][number], verdicts['B'][number]
        cases = []
        status = {r: {m['matter']: m['status'] for m in v[number]['matters']} for r, v in verdicts.items()}
        for matter in entry['settled_matters']:
            cases.append(('matter', matter['id'], status['A'].get(matter['id']), status['B'].get(matter['id']), 'kept'))
        thesis = {r: {t['thesis']: t['judgement'] for t in v[number]['theses']} for r, v in verdicts.items()}
        for opened in entry['opened_theses']:
            cases.append(('thesis', opened['thesis'], thesis['A'].get(opened['thesis']), thesis['B'].get(opened['thesis']), 'ok'))
        links = {r: {(i['item'], l['thesis']): l['judgement'] for i in v[number]['items'] for l in i.get('links', [])}
                 for r, v in verdicts.items()}
        for item in entry['kept_items']:
            for link in item['links']:
                key = (item['item'], link['thesis'])
                cases.append(('link', f'{key[0]}->{key[1]}', links['A'].get(key), links['B'].get(key), 'right'))
        items = {r: {i['item']: (i.get('verdict') if i.get('matter') in (None, 'null') else 'helpful') for i in v[number]['items']}
                 for r, v in verdicts.items()}
        for item in entry['kept_items']:
            counts[f"item {items['A'].get(item['item'])}/{items['B'].get(item['item'])}"] += 1
        for kind, key, va, vb, good in cases:
            counts[f'{kind} total'] += 1
            if va == vb:
                verdict = va
            elif (kind, number, key) in ruling:
                verdict = ruling[(kind, number, key)]
                counts[f'{kind} settled by third'] += 1
            else:
                verdict = None
                disputes.append({'kind': kind, 'article': number, 'key': key, 'A': va, 'B': vb})
            counts[f'{kind} pass'] += verdict == good
            counts[f'{kind} disputed'] += verdict is None
    for kind in ('matter', 'thesis', 'link'):
        total, passed, open_ = counts[f'{kind} total'], counts[f'{kind} pass'], counts[f'{kind} disputed']
        print(f'{kind}: {passed}/{total} pass ({open_} still disputed, counted against the system; '
              f'{counts[kind + " settled by third"]} settled by the third reader)')
    print('kept items by verdict (A/B):', dict(sorted((k[5:], v) for k, v in counts.items() if k.startswith('item '))))
    if '--disputes' in sys.argv:
        Path(sys.argv[sys.argv.index('--disputes') + 1]).write_text(json.dumps(disputes, ensure_ascii=False, indent=1))
        print(f'{len(disputes)} disputes written')


if __name__ == '__main__':
    main()
