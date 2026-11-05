"""A few cents' look at judging-v9 before any run (targets.md T1, T3, T4): each case is a stored judging-v7 request of the frozen draw
(its reading and previous conclusion as sent), turned into the request judging-v9 would send by the code's own builder pieces: the previous
card inserted before the previous conclusion and the closing line extended (`judging._fresh_card_lines`, `_lines_fresh_card`). As the previous
card it shows the judging-v8 run's card for that thesis before that day with every claim the v9 figure check refuses removed, a harder case
than v9's own card would be (it still carries v8's watch items and caveats). Each case is sent `sends` times, eight at a time; every
answer goes through judging-v9's card checks against the request sent.

usage: python3 probe_v9.py <out.json> [sends=3]
"""
import concurrent.futures
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

V7_RUN = '/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
V8_RUN = '/Users/lchingen/hivemind/poc/data/e2e-r10-card-v109-2026-11-04/d1'


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def previous_card(v8_views, v8_archive, view_id, day):
    """The judging-v8 card of this thesis written before `day`, without the claims judging-v9's figure check refuses; None if none."""
    row = v8_views.execute('select a.card_json, j.request_sha256 from arguments a join judgements j using(judgement_id) '
                           'where a.view_id=? and j.publication_day<? order by a.id desc limit 1', (view_id, day)).fetchone()
    if not row:
        return None
    card = json.loads(row['card_json'])
    request = json.loads(v8_archive.execute('select request_json from model_calls where request_sha256=?', (row['request_sha256'],)).fetchone()[0])['messages'][1]['content']
    texts, question = judging.ref_texts(request), '\n'.join(request.split('\n')[:2])
    for side in ('for', 'against'):
        card[side] = [c for c in card[side] if not judging.figures_not_in_refs(c['text'], c['refs'], texts, question)]
    return {'card': card}


def v9_user(v7_user, argument=None):
    """The v7 request text with the v9 closing line, as `_lines_fresh_card` builds it (judging-v9 shows no previous card; `argument` is
    kept for the earlier probe that showed one, `probe-v9-result.json`)."""
    lines = v7_user.split('\n')
    lines[-1] = lines[-1][:-1] + "; a claim's refs may name only the evidence, dependency and theme ids listed above."
    return '\n'.join(lines)


def main():
    out = sys.argv[1]
    sends = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v108.json')
    v7_views, v7_archive, v8_views, v8_archive = ro(f'{V7_RUN}/views.sqlite'), ro(f'{V7_RUN}/archive.sqlite'), ro(f'{V8_RUN}/views.sqlite'), ro(f'{V8_RUN}/archive.sqlite')
    cases = [('v1', '2026-07-13'), ('v9', '2026-07-12')] + [(r['view_id'], '2026-07-14') for r in v7_views.execute(
        "select view_id from judgements where publication_day='2026-07-14' order by judgement_id")]
    system = open(config.prompt_path('judging-v9.txt'), encoding='utf-8').read()
    schema = judging.schema_for('judging-v9')
    requests = {}
    for view_id, day in cases:
        row = v7_views.execute('select request_sha256, rung from judgements where view_id=? and publication_day=?', (view_id, day)).fetchone()
        stored = json.loads(v7_archive.execute('select request_json from model_calls where request_sha256=?', (row['request_sha256'],)).fetchone()[0])
        user = v9_user(stored['messages'][1]['content'])
        requests[(view_id, day)] = (user, row['rung'])

    def send(case):
        user, _ = requests[case]
        response = model.openai_transport(cfg.provider, model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider))
        data = json.loads(response['choices'][0]['message']['content'])
        usage = response.get('usage') or {}
        return case, data, judging.check_fresh_card(data['card'], user), usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)

    jobs = [case for case in requests for _ in range(sends)]
    results = {f'{v}:{d}': {'v7_rung': requests[(v, d)][1], 'characters': len(requests[(v, d)][0]), 'answers': []} for v, d in requests}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for (view_id, day), data, errors, tokens_in, tokens_out in pool.map(send, jobs):
            results[f'{view_id}:{day}']['answers'].append({'rung': data['rung'], 'implied_outcome': data['implied_outcome'], 'card': data['card'],
                                                          'errors': errors, 'tokens_in': tokens_in, 'tokens_out': tokens_out})
    for key, r in results.items():
        rungs = [a['rung'] for a in r['answers']]
        refused = sum(1 for a in r['answers'] if a['errors'])
        print(f'{key:14} v7 rung {r["v7_rung"]} | v9 rungs {rungs} | card refused {refused}/{len(rungs)}')
    json.dump(results, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
