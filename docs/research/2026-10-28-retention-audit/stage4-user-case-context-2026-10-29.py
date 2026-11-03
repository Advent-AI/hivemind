"""Reconstruct three user-adjudicated examples at their historical sequence; do not send a model request."""
import hashlib
import json
import sqlite3
from pathlib import Path

from hivemind import research_context, universe

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
DATA = Path('/Users/lchingen/hivemind/poc/data')
LEDGER = DATA / 'english-v38-nvda-1w-2026-10-28/views.sqlite'
ITEMS = DATA / 'items-nvda-2026-07-01-10-27.sqlite'
RESEARCH = ROOT / 'docs/research/2026-10-28-retention-audit'
TRACES = RESEARCH / 'user-week-traces-2026-10-29.json'
OUT = RESEARCH / 'stage4-user-case-context-2026-10-29.json'
CASES = [('sharon', 'gnews:3854aeddaa3f31de00cf2816', 'e6'),
         ('product_progress', 'gnews:795ea94e1100415a67fd1a96', 'e3'),
         ('singapore_case_overview', 'gnews:1eeceeb212a2c82c2e75e806', 'e8')]

traces = json.loads(TRACES.read_text())
uni = universe.load(str(ROOT / 'poc/universe.json'))
result = []
with sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True) as items:
    items.row_factory = sqlite3.Row
    for group, input_id, piece_id in CASES:
        selected = [r for r in traces['cases'][group] if r['input_id'] == input_id and r['extracted']['id'] == piece_id]
        if len(selected) != 1:
            raise ValueError('case missing or repeated: ' + input_id)
        original = selected[0]
        item = items.execute('select * from items where input_id=?', (input_id,)).fetchone()
        if item is None:
            raise ValueError('original item missing: ' + input_id)
        text = item['text'] or ''
        if hashlib.sha256(text.encode()).hexdigest() != original['source_sha256']:
            raise ValueError('source changed: ' + input_id)
        objects = [x['value'] for x in json.loads(item['object_identifiers']) if uni.has(x['value'])]
        with research_context.Reader(str(LEDGER), original['sequence'], objects, uni) as reader:
            catalog = reader.catalog()
            all_question_ids = [q['view_id'] for q in catalog['questions']]
            expansion = reader.expand(all_question_ids)
        if any(q['created_seq'] >= original['sequence'] for q in catalog['questions']):
            raise ValueError('future question included')
        if any(e['created_seq'] >= original['sequence'] for e in expansion['evidence']):
            raise ValueError('future evidence included')
        if original['extracted']['quote'] not in text:
            raise ValueError('target quote not in original article')
        result.append({'case': group, 'input_id': input_id, 'sequence': original['sequence'],
                       'source': text, 'source_sha256': original['source_sha256'],
                       'original_extraction': original['extracted'],
                       'original_placement_request': original['placement_request'],
                       'original_placement_answer': original['placement_answer'],
                       'historical_catalog': catalog, 'full_historical_expansion': expansion})
assert len(result[0]['historical_catalog']['questions']) == 3
assert any(q['view_id'] == 'v11' and 'Kyber' in q['question'] for q in result[1]['historical_catalog']['questions'])
assert all(r['original_extraction']['status'] == 'dropped' for r in result)
payload = {'note': 'Historical source data, not new gold; no model sent.', 'cases': result}
if OUT.exists():
    if json.loads(OUT.read_text()) != payload:
        raise ValueError('saved context differs; preserve it and investigate')
else:
    with OUT.open('x', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write('\n')
for r in result:
    print(r['case'], 'sequence', r['sequence'], 'questions', len(r['historical_catalog']['questions']),
          'distinct historical evidence', len(r['full_historical_expansion']['evidence']),
          'full context bytes', len(json.dumps(r['full_historical_expansion'], ensure_ascii=False).encode()))
