"""Check complete accounting and aggregate authored readings, without grading text."""
import collections
import hashlib
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent


def measure(readings=None):
    plan = json.loads((HERE / 'case-plan.json').read_text())
    results = json.loads((HERE / 'run-summary.json').read_text())['results']
    expected = {f'{case}-{arm}-{draw}' for case in plan['cases']
                for arm in ('control', 'treatment') for draw in (1, 2, 3)}
    assert len(results) == len(expected) == 48
    assert {r['id'] for r in results} == expected
    sent = {r['id'] for r in results if not r.get('not_sent')}
    readings = readings if readings is not None else json.loads((HERE / 'readings.json').read_text())['rows']
    assert len(readings) == len(sent) and {r['answer_id'] for r in readings} == sent
    answers = {}
    for row in readings:
        path = HERE / (row['answer_id'] + '-answer.json')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        assert row['read_reason'] and row['content'] in {'preserved', 'excluded_as_requested'}
        answers[row['answer_id']] = json.loads(path.read_text())
    out = {'planned': 48, 'sent': len(sent), 'not_sent': len(expected - sent), 'arms': {}}
    for arm in ('control', 'treatment'):
        rr = [r for r in readings if r['arm'] == arm]
        aa = [answers[r['answer_id']] for r in rr]
        facts = [r for r in rr if r['case'] in {'nvidia', 'nn', 'corning', 'amd', 'cloud'}]
        first = [answers[r['answer_id']] for r in rr if r['draw'] == 1]
        out['arms'][arm] = {'sent': len(aa),
            'structure_pass': sum(not a['errors'] for a in aa),
            'target_facts_written': sum(r['content'] == 'preserved' for r in facts),
            'target_fact_observations': len(facts),
            'excluded_case_respected': sum(r['content'] == 'excluded_as_requested' for r in rr),
            'answers_with_explicit_semantic_error': sum(bool(r['errors']) for r in rr),
            'error_types': dict(collections.Counter(e['kind'] for r in rr for e in r['errors'])),
            'actions': dict(collections.Counter(a['answer']['action'] for a in aa)),
            'input_tokens': sum(a['response']['usage']['input_tokens'] for a in aa),
            'output_tokens': sum(a['response']['usage']['output_tokens'] for a in aa),
            'paired_first_draw_median_seconds': statistics.median(a['seconds'] for a in first),
            'paired_first_draw_output_tokens': sum(a['response']['usage']['output_tokens'] for a in first),
            'first_keys': dict(collections.Counter(next(iter(a['answer'])) for a in aa))}
    return out


if __name__ == '__main__':
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
