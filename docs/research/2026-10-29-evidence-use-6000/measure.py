"""Validate complete authored readings and aggregate them; no semantic inference."""
import collections
import hashlib
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
UNITS = {'nvidia': {'N1', 'N2'}, 'nn': {'NN'}, 'corning': {'C'}, 'amd': {'A'}, 'cloud': {'G'}, 'singapore': {'S'}}


def measure(data=None):
    if data is None:
        data = json.loads((HERE / 'assessments.json').read_text())
    rows = data['rows']
    expected = {(f'{case}-{arm}-{draw}', unit) for case, units in UNITS.items()
                for arm in ('control', 'treatment') for draw in (1, 2, 3) for unit in units}
    actual = {(r['answer_id'], r['unit']) for r in rows}
    if len(rows) != len(expected) or actual != expected:
        raise ValueError('Missing or repeated use observation')
    answers = {}
    for row in rows:
        path = HERE / (row['answer_id'] + '-answer.json')
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Raw answer changed')
        answer = json.loads(path.read_text())
        if not answer['completed'] or answer['errors']:
            raise ValueError('Incomplete answer must not disappear from scoring')
        if row['source_content'] not in {'preserved', 'excluded_as_requested', 'risk_question_not_a_separate_source_fact'}:
            raise ValueError('Unknown content classification')
        if row['bounded_claim'] not in {'overstated', 'limited_or_excluded'} or not row['read_reason']:
            raise ValueError('Missing reading or unknown label')
        if type(row['unsupported_credit_assertion']) is not bool:
            raise ValueError('Unknown credit assertion status')
        answers[row['answer_id']] = answer
    result = {'answers': len(answers), 'use_observations': len(rows), 'by_arm': {}}
    for arm in ('control', 'treatment'):
        rr = [r for r in rows if r['arm'] == arm]
        aa = [a for ident, a in answers.items() if ident.split('-')[1] == arm]
        facts = [r for r in rr if r['unit'] not in {'S', 'N2'}]
        result['by_arm'][arm] = {
            'source_fact_units_preserved': sum(r['source_content'] == 'preserved' for r in facts),
            'source_fact_units': len(facts),
            'excluded_as_requested': sum(r['source_content'] == 'excluded_as_requested' for r in rr),
            'unsupported_credit_assertions': sum(r['unsupported_credit_assertion'] for r in rr),
            'credit_risk_use_observations': sum(r['unit'] == 'N2' for r in rr),
            'actions': dict(collections.Counter(a['answer']['action'] for a in aa)),
            'input_tokens': sum(a['response']['usage']['input_tokens'] for a in aa),
            'output_tokens': sum(a['response']['usage']['output_tokens'] for a in aa),
            'median_seconds': statistics.median(a['seconds'] for a in aa)}
    return result


if __name__ == '__main__':
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
