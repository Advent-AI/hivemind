"""The self-report diagnostic's cases, at $0 (council round 13): from the Stage B reading (the frozen judge on the new system's own
questions, July window, three draws, every day's answer read by two reader families), the figure answers settled as resting on too
little or unsupported (the failed set), and, matched to them, figure answers both first readers passed on the same question path
(same draw and question), the passed set. Each case's stored request and answer are located by judgement id in its draw's store
and archive. A keyword rule, D520's, is run on exactly these cases as the baseline. Judges nothing.

  python3 prepare_cases.py <key folder holding stage-b-reading-key.json>
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'))
import baseline_count  # noqa: E402

READING = ROOT / 'poc/data/clean-stage-b-reading-2026-11-12'
RUN = ROOT / 'poc/data/clean-stage-b-2026-11-11'
FAMILIES = ('codex', 'claude')
KEYWORDS = re.compile(r'assum|discount|haircut|allowing|estimate|scaled|carry(ing)? forward|extrapolat', re.I)


def settled_verdicts(key):
    first, third = {f: {} for f in FAMILIES}, {f: {} for f in FAMILIES}
    for f in FAMILIES:
        for path in sorted((READING / 'readers-answers').glob(f'reader-{f}-packet-*.jsonl')):
            first[f].update(baseline_count.rows_in(path)[0])
        for path in sorted((READING / 'third-reader').glob(f'rulings-{f}-*.jsonl')):
            third[f].update(baseline_count.rows_in(path)[0])
    out = {}
    for number, entry in key.items():
        if entry['kind'] != 'stored':
            continue
        n = int(number)
        pair = [first[f][n]['verdict'] for f in FAMILIES]
        if pair[0] == pair[1]:
            out[n] = (pair[0], 'both first readers')
        else:
            rulings = [third[f].get(n, {}).get('verdict') for f in FAMILIES]
            out[n] = (rulings[0] if rulings[0] == rulings[1] else 'unresolved', 'third readers')
    return out


def stored_call(draw, judgement_id):
    store = sqlite3.connect(f"file:{RUN / f'draw-{draw}' / 'views.sqlite'}?mode=ro", uri=True)
    sha = store.execute('select request_sha256 from judgements where judgement_id=?', (judgement_id,)).fetchone()[0]
    archive = sqlite3.connect(f"file:{RUN / f'draw-{draw}' / 'archive.sqlite'}?mode=ro", uri=True)
    request_json, answer_json = archive.execute('select request_json, answer_json from model_calls where request_sha256=? and answer_json is not null order by call_id desc limit 1', (sha,)).fetchone()
    return sha, json.loads(request_json), json.loads(answer_json)


def main(key_folder):
    key = json.loads((Path(key_folder) / 'stage-b-reading-key.json').read_text())
    verdicts = settled_verdicts(key)
    figure = {int(n): e for n, e in key.items() if e['kind'] == 'stored' and e['shape'] == 'figure'}
    failed = [n for n in figure if verdicts[n][0] in ('INSUFFICIENT', 'UNSUPPORTED')]
    passed_pool = [n for n in figure if verdicts[n] == ('SUPPORTED', 'both first readers')]
    path_of = lambda n: (figure[n]['draw'], figure[n]['view'])
    passed = [n for n in passed_pool if path_of(n) in {path_of(f) for f in failed}]
    print(f'figure answers {len(figure)}; failed set {len(failed)} on {len({path_of(n) for n in failed})} question paths; '
          f'passed by both first readers {len(passed_pool)}, of them on the same paths {len(passed)}')
    cases = []
    for group, numbers in (('failed', failed), ('passed', passed)):
        for n in sorted(numbers, key=lambda n: (figure[n]['draw'], figure[n]['view'], figure[n]['day'])):
            entry = figure[n]
            sha, request, answer = stored_call(entry['draw'], entry['judgement_id'])
            text = f"{answer.get('implied_outcome', '')} {answer.get('reasons', '')}"
            cases.append({'case': f"{entry['draw']}-{entry['view']}-{entry['judgement_id']}", 'group': group, 'verdict': verdicts[n][0], 'draw': entry['draw'],
                          'view': entry['view'], 'day': entry['day'], 'judgement_id': entry['judgement_id'], 'request_sha256': sha,
                          'stored_rung': answer.get('rung'), 'keyword_warning': bool(KEYWORDS.search(text))})
    by_path = collections.defaultdict(lambda: collections.Counter())
    for c in cases:
        by_path[(c['draw'], c['view'])][c['group']] += 1
    for path, counts in sorted(by_path.items()):
        print('  ', path, dict(counts))
    for group in ('failed', 'passed'):
        rows = [c for c in cases if c['group'] == group]
        print(f"keyword rule on exactly these cases: {group} {len(rows)}, warned {sum(c['keyword_warning'] for c in rows)}")
    (HERE / 'cases.json').write_text(json.dumps(cases, indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1])
