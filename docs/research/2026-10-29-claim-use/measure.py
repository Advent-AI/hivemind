"""Count reviewed answers and API usage; never infer semantic grades from text."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from statistics import mean, median
import sys

def measure(directory):
    plan = json.loads((directory / 'plan.json').read_text())
    readings = json.loads((directory / 'final-readings.json').read_text())['rows']
    expected = {f'{case}-{arm}-{draw}' for case in plan['cases']
                for arm in ('control', 'treatment') for draw in range(1, plan['samples'] + 1)}
    assert len(expected) == plan['planned_calls'] > 0
    assert len(readings) == len(expected) and {r['id'] for r in readings} == expected
    result = {}
    for arm in ('control', 'treatment'):
        answers = []
        grades = Counter()
        for row in readings:
            if row['arm'] != arm:
                continue
            path = directory / (row['id'] + '-answer.json')
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row['answer_sha256']
            answer = json.loads(path.read_text())
            assert answer['id'] == row['id']
            assert answer['completed'] and not answer['errors']
            assert row['grade'] in {'useful_reliable', 'useful_needs_review', 'misleading_or_missed', 'not_assessable'}
            grades[row['grade']] += 1
            answers.append(answer)
        usage = [a['response']['usage'] for a in answers]
        result[arm] = {
            'n': len(answers), 'grades': dict(grades),
            'mean_seconds': mean(a['seconds'] for a in answers),
            'median_seconds': median(a['seconds'] for a in answers),
            'mean_answer_chars': mean(len(json.dumps(a['answer'], ensure_ascii=False)) for a in answers),
            'input_tokens': sum(u['input_tokens'] for u in usage),
            'output_tokens': sum(u['output_tokens'] for u in usage),
            'non_null_proposals': sum(a['answer']['proposal'] is not None for a in answers),
        }
    result['estimated_usd'] = sum((r['input_tokens'] * .1 + r['output_tokens'] * .5) / 1e6 for r in result.values())
    return result

if __name__ == '__main__':
    directory = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    print(json.dumps(measure(directory), ensure_ascii=False, indent=2))
