"""Validate the bounded, manually read comparison and count its labels; no semantic scoring."""
from collections import Counter
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure(root, data=None):
    data = read(root / 'assessments.json') if data is None else data
    gold = root / data['gold']
    need(digest(gold) == data['gold_sha256'], 'gold manifest changed')
    for name, sha in read(gold)['files'].items():
        need(digest(gold.parent / name) == sha, 'frozen gold changed: ' + name)
    refs = {x['id']: x for x in read(gold.parent / 'reference.json')['items']}
    runs = data['runs']
    planned = {f'{t}-{m}-{n}' for t in ('memory', 'amd', 'policy', 'singapore')
               for m in ('haiku', 'gpt') for n in (1, 2, 3)}
    planned |= {f'{t}-{c}-{m}-{n}' for t in ('revenue', 'holdout')
                for c in ('clean', 'page') for m in ('haiku', 'gpt') for n in (1, 2, 3)}
    need(len(runs) == len(planned) and {r['run_id'] for r in runs} == planned,
         'missing or duplicate planned answer')
    for r in runs:
        name = r['run_id']
        need(r['model'] == ('haiku' if '-haiku-' in name else 'luna'), 'wrong model')
        need(r['draw'] == int(name[-1]), 'wrong draw')
        need(r['cohort'] == (name.split('-')[1] if name.startswith(('revenue-', 'holdout-')) else 'multi'), 'wrong cohort')
        for file_key, sha_key in [('artifact', 'sha256'), ('request', 'request_sha256')]:
            need(digest(root / r[file_key]) == r[sha_key], 'changed input: ' + name)
        answer = read(root / r['artifact'])
        need(answer['completed'] and not answer['schema_errors'], 'incomplete answer: ' + name)
        kept_list = answer['sift']['evidence']
        kept = {x['id'] for x in kept_list}
        need(len(kept) == len(kept_list), 'duplicate evidence id')
        need(r['raw_evidence'] == len(answer['answer']['evidence']) and r['kept_evidence'] == len(kept), 'wrong evidence count')
        expected = {x['id'] for x in refs.values() if x['input_id'] == r['input_id']}
        rows = r['assessments']
        need(expected and len(rows) == len(expected) and {a['reference_id'] for a in rows} == expected, 'missing or duplicate reference item: ' + name)
        assigned = set()
        for a in rows:
            need(a['value'] == refs[a['reference_id']]['value'], 'changed reference weight')
            ids = a['record_ids']
            need(len(ids) == len(set(ids)) and set(ids) <= kept, 'unknown or duplicate record id')
            assigned.update(ids)
            need(a['selection'] in {'kept', 'omitted'}, 'unknown selection')
            need(a['meaning'] in {'correct', 'partial', 'wrong', 'absent'}, 'unknown meaning')
            need(a['traceability'] in {'sufficient', 'needs_context', 'unsupported', 'absent'}, 'unknown citation label')
            absent = not ids
            need(absent == (a['selection'] == 'omitted') == (a['meaning'] == 'absent') == (a['traceability'] == 'absent'), 'inconsistent omitted item')
            need(bool(a['reason']), 'missing reason')
            for issue in a['issues']:
                need(issue['kind'] in {'original_date', 'period_conflict', 'attribution', 'certainty', 'wrong_source', 'duplicate', 'missing_context', 'unsupported_inference', 'other'}, 'unknown issue')
                need(issue['severity'] in {'material', 'record_only'}, 'unknown severity')
                need(issue['record_ids'] and set(issue['record_ids']) <= set(ids), 'issue outside matched records')
                need(issue['field'] and issue['reason'], 'missing issue evidence')
        unreviewed = r['unreviewed_output_ids']
        need(len(unreviewed) == len(set(unreviewed)) and set(unreviewed) == kept - assigned, 'unaccounted or double-counted output')
    stats = {}
    for model in ('haiku', 'luna'):
        rr = [r for r in runs if r['model'] == model]
        groups = {}
        for cohort in ('all', 'multi', 'clean', 'page'):
            aa = [a for r in rr if cohort == 'all' or r['cohort'] == cohort for a in r['assessments']]
            groups[cohort] = {}
            for value in ('core', 'supporting', 'exclude', 'optional'):
                cases = [a for a in aa if a['value'] == value]
                groups[cohort][value] = {
                    'n': len(cases), 'meaning': dict(Counter(a['meaning'] for a in cases)),
                    'selection': dict(Counter(a['selection'] for a in cases)),
                    'traceability': dict(Counter(a['traceability'] for a in cases)),
                    'material_issue_cases': sum(any(i['severity'] == 'material' for i in a['issues']) for a in cases),
                    'original_day_error_cases': sum(any(i['kind'] == 'original_date' and i['field'] == 'original_day' for i in a['issues']) for a in cases),
                    'status': 'measured' if cases else 'not_exercised'}
        stats[model] = {'groups': groups, 'raw_records': sum(r['raw_evidence'] for r in rr),
                        'kept_records': sum(r['kept_evidence'] for r in rr),
                        'unreviewed_records': sum(len(r['unreviewed_output_ids']) for r in rr)}
    return {'runs': len(runs), 'reference_observations': sum(len(r['assessments']) for r in runs),
            'by_model': stats, 'warning': 'Counts of manual labels on repeated development cases, not population performance.'}


if __name__ == '__main__':
    print(json.dumps(measure(Path(__file__).resolve().parent), ensure_ascii=False, indent=2))
