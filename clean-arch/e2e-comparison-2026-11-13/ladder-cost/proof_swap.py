"""D467's proofs 1 and 2 ($0): (a) swapping the ten measured seed views to their own seed ladders rebuilds the stored control exactly —
every judge request served from the archive and the same judgement records — so the swap changes nothing else (facts, links, revisions,
dependencies, judging days); (b) a positive control: swapping one view (v4) to a ladder with reworded rung conditions makes its first judge request
differ (missing from the archive) while every request before it is found.

  python3 proof_swap.py d1
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import proof_control_rebuild as rebuild  # noqa: E402
import swap_adapter  # noqa: E402

MEASURED = ['v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v13', 'v16', 'v17', 'v18']


def seed_ladders():
    seeds = {q['view_id']: q for q in json.loads(swap_adapter.adapter.SEEDS.read_text())['questions']}
    return {view_id: {'question': seeds[view_id]['question'], 'due_day': seeds[view_id]['due_day'], 'year': seeds[view_id]['year'],
                      'rungs': seeds[view_id]['rungs']} for view_id in MEASURED}


def run(draw, swaps):
    judged = rebuild.DATA / f'stage2-clean-{draw}' / rebuild.JUDGED[draw]
    answers = rebuild.stored_answers(judged / 'archive.sqlite')
    served = {'found': 0, 'missing': None}

    def recorded(provider, request, *args, **kwargs):
        sha = rebuild.model.request_identity(request)[1]
        if sha not in answers or not answers[sha]:
            served['missing'] = request['messages'][-1]['content'].split('\n')[0][:80]
            raise rebuild.Missing(sha[:12])
        served['found'] += 1
        return answers[sha].pop(0)

    trace = f"{rebuild.DATA / f'stage2-clean-{draw}' / 'trace.sqlite'}+{rebuild.DATA / f'stage2-clean-{draw}-segment-2' / 'trace.sqlite'}"
    step2 = rebuild.DATA / f'stage2-clean-{draw}-segment-2' / 'step2'
    with tempfile.TemporaryDirectory() as folder:
        try:
            swap_adapter.replay_swapped(trace, step2, Path(folder) / 'out', transport=recorded, swaps=swaps, q23=rebuild.Q23.get(draw))
        except rebuild.Missing:
            return served, None
        rebuilt = json.loads((Path(folder) / 'out' / 'judge-requests.json').read_text())
    stored = json.loads((judged / 'judge-requests.json').read_text())
    key = lambda r: (r['day'], r['seq'], r['view'], tuple(r['shown']))
    return served, sorted(rebuilt, key=key) == sorted(stored, key=key)


def main():
    draw = sys.argv[1]
    served, same = run(draw, seed_ladders())
    print(f'{draw} (a) ten views swapped to their own seed ladders: {served["found"]} requests served; missing: {served["missing"]}; '
          f'records identical: {same}')
    shifted = seed_ladders()['v4']
    shifted = dict(shifted, rungs=[dict(r, condition=r['condition'] + ' (as reported in full-year results)') for r in shifted['rungs']])
    served, same = run(draw, {'v4': shifted})
    print(f'{draw} (b) v4 swapped to rungs with reworded conditions: {served["found"]} requests served before the first miss; first missing '
          f'request: {served["missing"]}  (the judge reads rung labels and conditions, not the stored lo/hi: shifting lo/hi alone changed no request)')


if __name__ == '__main__':
    main()
