"""Blind field audit: random items from the K5 gold run and from frozen production draw 1 on the same gold articles, put in one shape
(summary, passages, original party, reporting speaker, tier, statement date, period, linked questions) and shuffled, so a reader judges
every field without knowing the system. Usage: build_field_audit.py <output folder> <key path> <items per system>"""
import json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / 'poc/data/clean-step1-takeover-2026-11-07'
PRODUCTION = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/runs/control-v108-d1/views.sqlite')

def main():
    out, key_path, per_system = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    out.mkdir(parents=True, exist_ok=False)
    chooser = random.Random(20261107)
    items, texts = [], {}
    conn = sqlite3.connect(f'file:{B / "gold-k5/trace.sqlite"}?mode=ro', uri=True)
    k5 = []
    for input_id, request, before, result, after in conn.execute("select input_id, request, before_state, result, after_state from trace where status='complete'"):
        payload = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]
        texts[input_id] = {'title': payload['source_item']['title'], 'publisher': payload['source_item']['publisher'],
                           'publication_date': payload['source_item']['publication_date'], 'text': payload['source_item']['text']}
        names = {t['id']: t['description'] for t in json.loads(before) + json.loads(after)}
        result = json.loads(result)
        local = {loc: next((t['description'] for t in result['new_theses'] if t['local_id'] == loc), '(undeclared)') for loc in result.get('new_thesis_ids', {})}
        for ev in result['evidence']:
            k5.append({'input_id': input_id, 'summary': ev['summary'], 'passages': ev['source_passages'], 'original_party': ev['original_party'],
                       'reporting_speaker': ev['reporting_speaker'], 'tier': ev['tier'], 'statement_date': ev['statement_date'] or ev['statement_date_text'],
                       'period': ev['evidence_period'], 'linked_questions': [names.get(l['target_id']) or local.get(l['target_id'], '(unknown)') for l in ev['links']]})
    pconn = sqlite3.connect(f'file:{PRODUCTION}?mode=ro', uri=True)
    questions = dict(pconn.execute('select view_id, question from views'))
    production = []
    for input_id, handover_json in pconn.execute('select input_id, handover_json from handovers'):
        if input_id not in texts:
            continue
        handover = json.loads(handover_json)
        candidates = {c['id']: c['question'] for c in handover.get('candidates', [])}
        for ev in handover['evidence']:
            production.append({'input_id': input_id, 'summary': ev['one_line'], 'passages': [ev['quote']], 'original_party': ev['original_who'] or None,
                               'reporting_speaker': ev['speaker'] or None, 'tier': ev['tier'], 'statement_date': ev['original_day'] or None,
                               'period': ev['event_time'] or None, 'linked_questions': [questions.get(l) or candidates.get(l) or '(none)' for l in ev.get('links', [])]})
    sample = [('k5', x) for x in chooser.sample(k5, per_system)] + [('production', x) for x in chooser.sample(production, per_system)]
    chooser.shuffle(sample)
    key, packets = {}, []
    for index, (system, item) in enumerate(sample, 1):
        key[f'I{index}'] = system
        packets.append({'id': f'I{index}', 'article': texts[item['input_id']], **{k: v for k, v in item.items() if k != 'input_id'}})
    size = len(packets) // 4 + (len(packets) % 4 > 0)
    for part in range(4):
        (out / f'audit-packet-{part + 1}.json').write_text(json.dumps(packets[part * size:(part + 1) * size], ensure_ascii=False, indent=1))
    Path(key_path).write_text(json.dumps(key, indent=1))
    print('items', len(packets), 'from k5', len(k5), 'production', len(production))

if __name__ == '__main__':
    main()
