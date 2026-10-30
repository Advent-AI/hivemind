"""Find argument-text evidence IDs absent from that argument's structured source lists."""
import json
import re
from pathlib import Path

HERE = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD = Path('/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold')
NEW = HERE / 'stage4-haiku-luna-v3-2026-10-29'
OUTPUT = HERE / 'stage4-inline-citation-census-2026-10-29.json'
ID = re.compile(r'(?<![A-Za-z0-9:])e\d+\b')

def absent_from_lists(argument):
    mentioned = set(ID.findall(argument['statement']))
    structured = set(argument['support_ids'] + argument['opposing_ids'])
    return sorted(mentioned - structured, key=lambda value: int(value[1:]))

if absent_from_lists({'statement': 'e123, e12; item:e5', 'support_ids': ['e12'], 'opposing_ids': []}) != ['e123']:
    raise ValueError('positive and exact-ID controls failed')
if absent_from_lists({'statement': 'e123', 'support_ids': ['e123'], 'opposing_ids': []}):
    raise ValueError('negative control failed')

census = json.loads((HERE / 'stage4-citation-structure-census-2026-10-29.json').read_text())
rows = []
for row in census['arguments']:
    directory = NEW if row['group'] == 'five_case' else OLD / row['group']
    answer = json.loads((directory / row['file']).read_text())
    if row['group'] == 'five_case':
        answer = answer['answer']
    matches = [arg for arg in answer['arguments'] if arg['question_id'] == row['question_id']]
    if len(matches) != 1:
        raise ValueError('argument cannot be uniquely located: ' + row['file'])
    missing = absent_from_lists(matches[0])
    if missing:
        rows.append({'group': row['group'], 'file': row['file'], 'question_id': row['question_id'],
                     'incoming_reference': row['incoming_reference'], 'inline_ids_absent_from_lists': missing})
if len(census['arguments']) != 81 or len(rows) != 18 or sum(bool(r['incoming_reference']) for r in rows) != 15:
    raise ValueError('population differs from independently inspected data')
known = [r for r in rows if r['group'] == 'fresh2' and r['file'] == 'F09.analyst.answer.json' and r['question_id'] == 'v6']
if len(known) != 1 or known[0]['inline_ids_absent_from_lists'] != ['e200', 'e282']:
    raise ValueError('known case missing')
result = {'definition': 'Exact e-number references in an argument statement absent from both its structured support and opposition lists; not a semantic error count.',
          'argument_occurrences_judged': 81, 'occurrences_with_missing_inline_ids': len(rows),
          'of_these_current_source_listed': sum(bool(r['incoming_reference']) for r in rows), 'occurrences': rows}
if OUTPUT.exists():
    if json.loads(OUTPUT.read_text()) != result:
        raise ValueError('stored results differ; do not overwrite')
else:
    with OUTPUT.open('x', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write('\n')
print(f"Judged {result['argument_occurrences_judged']} arguments: {len(rows)} mention an ID not in their lists; {result['of_these_current_source_listed']} of those list the current record.")
