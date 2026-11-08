"""Score an unfiled-round probe (no model calls).

Ruler (frozen golden-v5 dev, the frozen scorer's matching via score_gold_runs; kept evidence only, unfiled items not counted): helpful
matters kept, core kept, items matching a not-kept span, per case and arm, summed over draws. Filing: unfiled items, new theses and
their descriptions per answer. `--packets` writes blind reader packets: per case, every answer's new theses, kept evidence with links and
unfiled items, shuffled under labels, beside the article and the theses the answer saw; the key stays outside the packet.

Usage: score_probe.py <probe folder> <cases.json> [--packets <key.json>]"""
import collections, importlib.util, json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('score_gold_runs', ROOT / 'clean-arch/takeover-2026-11-07/score_gold_runs.py')
sgr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sgr)


def main():
    folder, cases = Path(sys.argv[1]), {c['case']: c for c in json.loads(Path(sys.argv[2]).read_text())}
    records = json.loads((folder / 'records.json').read_text())
    gold = {a['input_id']: a for a in json.loads(sgr.GOLD.read_text())['articles']}
    payloads = {}
    for name, case in cases.items():
        conn = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
        request = json.loads(conn.execute('select request from trace where sequence=?', (case['sequence'],)).fetchone()[0])
        payload = json.JSONDecoder().raw_decode(request['messages'][1]['content'])[0]
        payloads[name] = dict(payload, open_theses=[] if case['state'] == 'empty' else payload['open_theses'])
    table = collections.defaultdict(collections.Counter)
    order = ['k6b', 'u1', 'u3', 'u1u3', 'u1k', 'u1ku3', 'u1c', 'c1', 'c2']
    arms = sorted({r['arm'] for r in records}, key=order.index)
    for r in records:
        t = table[(r['case'], r['arm'])]
        t['answers'] += 1
        if 'kept' not in r:
            t['failed'] += 1
            continue
        input_id = payloads[r['case']]['source_item']['id']
        statements = {input_id: [{'quote': ' '.join(ev['source_passages']), 'quotes': ev['source_passages'], 'one_line': ev['summary']} for ev in r['kept']]}
        if input_id in gold:
            counts, _ = sgr.score([gold[input_id]], statements)
            t['helpful'] += counts['core matter kept'] + counts['supporting matter kept']
            t['helpful total'] += counts['core total'] + counts['supporting total']
            t['not-kept'] += counts['items matching a not-kept span']
        t['kept'] += len(r['kept'])
        t['unfiled'] += len(r['unfiled'])
        t['new theses'] += len(r['new_theses'])
    print(f"{'case':10s} " + ''.join(f'{a:>30s}' for a in arms))
    print(f"{'':10s} " + ''.join(f"{'helpful/kept/unfiled/new/nk':>30s}" for a in arms))
    totals = collections.defaultdict(collections.Counter)
    for name in cases:
        cells = []
        for arm in arms:
            t = table[(name, arm)]
            totals[arm].update(t)
            cells.append(f"{t['helpful']}/{t['helpful total']} {t['kept']}/{t['unfiled']}/{t['new theses']}/{t['not-kept']}" + (f" f{t['failed']}" if t['failed'] else ''))
        print(f'{name:10s} ' + ''.join(f'{c:>30s}' for c in cells))
    print(f"{'TOTAL':10s} " + ''.join(f"{totals[a]['helpful']}/{totals[a]['helpful total']} {totals[a]['kept']}/{totals[a]['unfiled']}/{totals[a]['new theses']}/{totals[a]['not-kept']}".rjust(30) for a in arms))
    if '--packets' in sys.argv:
        key_path = Path(sys.argv[sys.argv.index('--packets') + 1])
        chooser = random.Random(1108)
        packet, key = [], {}
        for name, case in cases.items():
            answers = [r for r in records if r['case'] == name and 'kept' in r]
            chooser.shuffle(answers)
            entry = {'case': name, 'article': {k: payloads[name]['source_item'][k] for k in ('title', 'publisher', 'publication_date', 'text')},
                     'open_theses_seen': [{'id': t['id'], 'question': t['description']} for t in payloads[name]['open_theses']], 'answers': {}}
            for n, r in enumerate(answers, 1):
                label = f'{name}/A{n}'
                key[label] = {'arm': r['arm'], 'draw': r['draw']}
                entry['answers'][f'A{n}'] = {
                    'new_theses': [{'local_id': t['local_id'], 'question': t['description'], 'outcome': t['outcome']} for t in r['new_theses']],
                    'evidence': [{'summary': ev['summary'], 'links': [l['target_id'] for l in ev['links']]} for ev in r['kept']],
                    'unfiled': [ev['summary'] for ev in r['unfiled']]}
            packet.append(entry)
        (folder / 'reader-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        key_path.write_text(json.dumps(key, indent=1))
        print(f'reader packet: {len(packet)} cases, {len(key)} answers')


if __name__ == '__main__':
    main()
