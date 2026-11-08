"""Blind packets for whole forward runs: per article, the answers on identical text of the original clean run, each named candidate run
and frozen production draw 1, each item shown with the descriptions of the theses it links to. Plus one packet with each clean run's
final thesis library for a duplicate and noise read.

Usage: build_forward_packets.py <output folder> <arm key output path> <label>=<candidate trace.sqlite> ..."""
import json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / 'poc/data/clean-step1-takeover-2026-11-07'
ORIGINAL = [ROOT / 'poc/data/clean-step1-2026-07-08-09-continuing/trace.sqlite', ROOT / 'poc/data/clean-step1-2026-07-08-09-segment-2/trace.sqlite']
PRODUCTION = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/runs/control-v108-d1/views.sqlite')


def clean_trace(paths):
    """input_id -> (items with linked thesis descriptions, final state after that item)."""
    rows = {}
    for path in paths:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        for input_id, before, result, after in conn.execute("select input_id, before_state, result, after_state from trace where status='complete' order by sequence"):
            result, before, after = json.loads(result), json.loads(before), json.loads(after)
            names = {t['id']: t['description'] for t in before}
            names.update({local: next(t['description'] for t in after if t['id'] == stored) for local, stored in result.get('new_thesis_ids', {}).items()})
            items = [{'summary': ev['summary'], 'quotes': ev['source_passages'],
                      'linked_theses': [names.get(link['target_id'], '(undeclared thesis)') for link in ev['links']]} for ev in result['evidence']]
            rows[input_id] = (items, after)
    return rows


def production_rows():
    conn = sqlite3.connect(f'file:{PRODUCTION}?mode=ro', uri=True)
    questions = {view_id: question for view_id, question in conn.execute('select view_id, question from views')}
    rows = {}
    for input_id, handover_json in conn.execute('select input_id, handover_json from handovers'):
        handover = json.loads(handover_json)
        candidates = {c['id']: c['question'] for c in handover.get('candidates', [])}
        rows[input_id] = [{'summary': ev['one_line'], 'quotes': [ev['quote']],
                           'linked_theses': [questions.get(link) or candidates.get(link) or '(no thesis)' for link in ev.get('links', [])]}
                          for ev in handover['evidence']]
    return rows


def main():
    out, key_path = Path(sys.argv[1]), Path(sys.argv[2])
    candidate_paths = dict(spec.split('=', 1) for spec in sys.argv[3:])
    out.mkdir(parents=True, exist_ok=False)
    ids = json.loads((ROOT / 'poc/data/clean-step1-2026-07-08-09/manifest.json').read_text())['item_ids']
    original, production = clean_trace(ORIGINAL), production_rows()
    candidates = {label: clean_trace([Path(p)]) for label, p in candidate_paths.items()}
    census = {a['article']: a for part in range(1, 5) for a in json.loads((CENSUS / f'census-answer-{part}.json').read_text())}
    texts = {p['article']: p for part in range(1, 5) for p in json.loads((CENSUS / f'census-packet-{part}.json').read_text())}
    for label, candidate in candidates.items():
        missing = [n for n, input_id in enumerate(ids, 1) if input_id not in candidate]
        if missing:
            raise SystemExit(f'{label} run lacks articles {missing}')
    chooser = random.Random(11)
    packets, key = [], {}
    for number, input_id in enumerate(ids, 1):
        arms = [('original', original[input_id][0]), ('production', production[input_id])] + [(label, c[input_id][0]) for label, c in candidates.items()]
        chooser.shuffle(arms)
        answers = {}
        for index, (arm, items) in enumerate(arms, 1):
            key[f'{number}:R{index}'] = arm
            answers[f'R{index}'] = items
        matters = [{'id': f'M{i}', 'matter': m['matter'], 'weight': m['weight']} for i, m in enumerate(census[number]['matters'], 1)]
        packets.append({'article': number, 'title': texts[number]['title'], 'text': texts[number]['text'], 'matters': matters, 'answers': answers})
    for part in range(4):
        (out / f'score-packet-{part + 1}.json').write_text(json.dumps(packets[part::4], ensure_ascii=False, indent=1))
    libraries = [('original', original[ids[-1]][1])] + [(label, c[ids[-1]][1]) for label, c in candidates.items()]
    chooser.shuffle(libraries)
    library_packet = {}
    for letter, (arm, state) in zip('XYZW', libraries):
        key[f'library:{letter}'] = arm
        library_packet[letter] = [{'id': t['id'], 'question': t['description'], 'outcome': t['outcome'], 'period': t['period']} for t in state]
    (out / 'library-packet.json').write_text(json.dumps(library_packet, ensure_ascii=False, indent=1))
    key_path.write_text(json.dumps(key, indent=1))
    print('articles', len(packets), 'library sizes', {letter: len(v) for letter, v in library_packet.items()})


if __name__ == '__main__':
    main()
