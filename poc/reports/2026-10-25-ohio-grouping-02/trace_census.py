"""Read-only census and counterfactual over the complete registered stored-answer population."""
import copy
import inspect
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe

OUT = Path(__file__).resolve().parent
OLD = ROOT / 'poc/reports/2026-10-25-ohio-grouping-01'
uni = universe.load(ROOT / 'poc/universe.json')
source = inspect.getsource(extraction.sift)
# Restore the measured baseline even after the one-line production fix is applied.
source = source.replace("if c.get('measure') not in ('event', 'policy_event') and year_match and", 'if year_match and')
baseline_ns = dict(vars(extraction))
exec(source, baseline_ns)
changed_ns = dict(vars(extraction))
exec(source.replace('if year_match and', "if c.get('measure') not in ('event', 'policy_event') and year_match and"), changed_ns)
items = sqlite3.connect(f'file:{ROOT}/poc/data/items-window-tags2-2026-10-24.sqlite?mode=ro', uri=True)
items.row_factory = sqlite3.Row
archive = sqlite3.connect(f'file:{ROOT}/poc/data/keyed-2026-10-25/archive-T2.sqlite?mode=ro', uri=True)
archive.row_factory = sqlite3.Row
cases = []
for row in archive.execute("select * from model_calls where purpose='extract' and request_sha256 not like '%:%'"):
    request = json.loads(row['request_json'])
    user = request['messages'][1]['content']
    input_id = re.search(r'【信息】编号 (\S+?)，类别 ', user).group(1)
    item = dict(items.execute('select * from items where input_id=?', (input_id,)).fetchone())
    cases.append((f'archive-T2/call-{row["call_id"]}', item, json.loads(row['answer_json']), set(re.findall(r'^\s+- (v\d+)（', user, re.M))))
for path in sorted(OLD.glob('*/item*/extraction.json')):
    index = int(path.parent.name[4:]) - 1
    item = json.loads((OLD / 'items.json').read_text())[index]
    context = json.loads((path.parent / 'context.json').read_text())
    cases.append((str(path.relative_to(ROOT)), item, json.loads(path.read_text()), {v['view_id'] for v in context['shown']}))

results, changes = [], []
for name, item, raw, shown in cases:
    before = baseline_ns['sift'](copy.deepcopy(raw), item, item['text'], shown, uni)
    after = changed_ns['sift'](copy.deepcopy(raw), item, item['text'], shown, uni)
    result = {'case': name, 'input_id': item['input_id'], 'raw_candidates': len(raw['candidates']),
              'raw_evidence': len(raw['evidence']), 'before_candidates': len(before[1]), 'after_candidates': len(after[1]),
              'before_evidence': len(before[0]), 'after_evidence': len(after[0]), 'dropped': before[2]}
    results.append(result)
    if before != after:
        changes.append(dict(result, before=before, after=after))
assert len(cases) == 326, len(cases)
assert len(changes) == 1, [(r['case'], r['input_id']) for r in changes]
assert changes[0]['input_id'] == 'nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout'
rescued = [c for c in changes[0]['after'][1] if c['id'] not in {x['id'] for x in changes[0]['before'][1]}]
assert len(rescued) == 1 and rescued[0]['measure'] == 'event'
totals = {key: sum(r[key] for r in results) for key in ('raw_candidates', 'raw_evidence', 'before_candidates', 'after_candidates', 'before_evidence', 'after_evidence')}
record = {'answers': len(cases), 'totals': totals, 'changes': changes, 'cases': results,
          'meaning': 'sift-only diagnostic, including raw answers refused by earlier group validation; not a model experiment'}
(OUT / 'trace-census.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
print(json.dumps({'answers': len(cases), 'totals': totals, 'changed': [(r['case'], r['input_id']) for r in changes]}, ensure_ascii=False, indent=2))
