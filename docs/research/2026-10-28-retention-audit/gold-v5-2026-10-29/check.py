"""Check the frozen development reference; never judge investment meaning."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

VALUES = {'core', 'supporting', 'optional', 'exclude'}
MEANINGS = {'correct', 'partial', 'wrong', 'absent'}
TRACES = {'sufficient', 'needs_context', 'unsupported', 'absent'}
ISSUES = {'original_date', 'period_conflict', 'attribution', 'certainty',
          'wrong_source', 'duplicate', 'missing_context', 'unsupported_inference', 'other'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def unique(rows, key):
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows) and bool(rows), 'empty or duplicate ' + key)
    return result


def validate(root, check_manifest=True):
    if check_manifest:
        manifest = read(root / 'manifest.json')
        require(set(manifest['files']) == {
            'README.md', 'reference.md', 'reference.json', 'sources.json',
            'calibration.json', 'design.md', 'check.py'}, 'incomplete freeze manifest')
        for name, expected in manifest['files'].items():
            require(hashlib.sha256((root / name).read_bytes()).hexdigest() == expected,
                    'frozen file changed: ' + name)
    reference = read(root / 'reference.json')
    require(reference['status'] == 'bounded_development_reference', 'invalid scope')
    sources = unique(read(root / 'sources.json'), 'input_id')
    items = unique(reference['items'], 'id')
    for source in sources.values():
        require(bool(source['text']) and bool(source['source_uri']), 'missing source text or URI')
        require(hashlib.sha256(source['text'].encode()).hexdigest() == source['sha256'],
                'source digest mismatch: ' + source['input_id'])
    for item in items.values():
        require(item['value'] in VALUES, 'unknown value: ' + item['id'])
        require(item['input_id'] in sources, 'missing source: ' + item['id'])
        require(bool(item['source_parts']), 'missing source parts: ' + item['id'])
        for part in item['source_parts']:
            require(bool(part) and part in sources[item['input_id']]['text'],
                    'quote absent from source: ' + item['id'])
        for field in ('meaning', 'why', 'research_family', 'authority'):
            require(bool(item[field]), 'missing ' + field + ': ' + item['id'])
        require(isinstance(item['required'], list), 'required must be a list')
        require(item['value'] == 'exclude' or bool(item['required']), 'empty required meaning')
        require(set(item['authority']) == {'selection', 'value', 'grouping', 'note'}, 'authority dimensions')
        require(all(item['authority'].values()), 'empty authority')
    require({x['user_question'] for x in items.values()} - {None} == set(range(1, 12)),
            'user decisions not fully mapped')
    calibration = unique(read(root / 'calibration.json')['cases'], 'id')
    for case in calibration.values():
        require(case['reference_id'] in items, 'unknown calibration reference')
        expected = case['expected']
        require(expected['selection'] in {'kept', 'omitted'}, 'unknown selection')
        require(expected['meaning'] in MEANINGS, 'unknown meaning')
        require(expected['traceability'] in TRACES, 'unknown traceability')
        require(bool(expected['reason']), 'missing judgement reason')
        absent = expected['selection'] == 'omitted'
        require(absent == (not case['records']), 'selection/records disagree')
        require(absent == (expected['meaning'] == 'absent'), 'selection/meaning disagree')
        require(absent == (expected['traceability'] == 'absent'), 'selection/trace disagree')
        if case['records']:
            unique(case['records'], 'id')
        for issue in expected['issues']:
            require(issue['kind'] in ISSUES, 'unknown issue')
            require(issue['severity'] in {'material', 'record_only'}, 'unknown severity')
            require(bool(issue['reason']) and bool(issue['field']), 'missing issue evidence')
        origin = case['origin']
        if origin['kind'] == 'stored_answer':
            path = root / origin['path']
            require(hashlib.sha256(path.read_bytes()).hexdigest() == origin['sha256'],
                    'saved answer changed')
            answer = read(path)['answer']['evidence']
            matches = [row for row in answer if row['id'] == origin['evidence_id']]
            require(matches == case['records'], 'calibration changed the actual answer')
        else:
            require(origin['kind'] == 'constructed_calibration' and bool(origin['note']),
                    'unlabelled constructed case')
    return {'reference_items': len(items), 'source_articles': len(sources),
            'value_counts': dict(Counter(x['value'] for x in items.values())),
            'calibration_cases': len(calibration),
            'stored_answer_cases': sum(x['origin']['kind'] == 'stored_answer' for x in calibration.values()),
            'semantic_accuracy': 'not_measured_by_this_script'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(1, 'REFUSED: ' + str(exc) + '\n')
