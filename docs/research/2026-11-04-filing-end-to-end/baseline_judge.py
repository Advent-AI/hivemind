"""Step 2 of the coverage-start baseline (baseline-design.md): the frozen judge's window-end requests for v10 and v12, one per step-1 send that
delivered the question's starting figure (v10 and v12; the controls are not judged), each carrying every figure that send kept for the question as evidence records (the system's own
records, never the gold's text). Records are written as the frozen extraction writes this release's actual figures (tier fact, speaker and original
source the company, original day the release's day); the quote is printed as the model wrote it. The requests are formatted by the production
judging code (`judging._lines_english`) on draw 1's ledger at the window end, as a first judgement, and labelled constructed: in production the
starting figures would be judged at coverage start and re-judged later with a previous conclusion. Sends nothing; `oracle_send.py <out>
<answers> --sends 1` sends and scores them on the frozen scorer's rule.

usage: python3 baseline_judge.py baseline-read.json <out.json>
"""
import hashlib
import json
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', HERE]
import baseline_read_measure as brm  # noqa: E402
import oracle_build  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

RELEASE = 'edgar:NVDA:0001045810-26-000051:q1fy27pr.htm'
RELEASE_DAY = '2026-05-20'
COMPANY = 'NVIDIA Corporation'
FIRST_ID = 9101


def pieces_of(figures):
    return [{'evidence_id': f'e{FIRST_ID + n}', 'tier': 'fact', 'speaker': COMPANY, 'original_who': COMPANY, 'original_day': RELEASE_DAY,
             'sources': [{'input_id': RELEASE, 'publication_day': RELEASE_DAY}], 'one_line': f['one_line'], 'quote': f['quote']}
            for n, f in enumerate(figures)]


def main():
    step1, out = json.load(open(sys.argv[1])), sys.argv[2]
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    conn = sqlite3.connect(f'file:{oracle_build.RUN}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    with open(config.prompt_path(cfg.rejudging.prompt_version + '.txt'), encoding='utf-8') as handle:
        judging_system = handle.read()
    requests = {}
    for view_id in brm.NEEDS:
        sends = step1['results'][view_id]
        if store.evidence_in_force(conn, view_id) or store.current_state(conn, view_id):
            raise SystemExit(f'{view_id} has evidence or a judgement in the draw; the design assumed neither')
        for n, r in enumerate(sends):
            if not brm.delivered(view_id, r['figures']):
                print(f'{view_id} from send {n}: the starting figure was not delivered; not judged (counts as a miss)')
                continue
            pieces = pieces_of([f for f in r['figures'] if f['kept']])
            lines = judging._lines_english(conn, view_id, store.view(conn, view_id), store.rungs_of(conn, view_id), pieces,
                                           store.dependencies_of(conn, view_id), None, judging.themes_in_force(conn, view_id))
            requests[f'{view_id} from send {n}'] = {'view_id': view_id, 'system': judging_system, 'user': '\n'.join(lines), 'constructed': True,
                                                    'pieces': pieces}
    for arm, r in requests.items():
        body = model.build_request(cfg.rejudging, r['system'], r['user'], schema, 'judgement', cfg.provider)
        r['request_sha256'] = model.request_identity(body)[1]
        r['characters'] = len(r['system']) + len(r['user'])
        r['synthetic_check'] = oracle_build.synthetic_check(conn, r['view_id'], r['user'], r['pieces'][0]['evidence_id'])
        r['system_is_judging_v7'] = r['system'] == judging_system
        print(f'\n{"=" * 30} {arm}: {r["characters"]} characters, {len(r["pieces"])} records, system is judging-v7: {r["system_is_judging_v7"]}, '
              f'synthetic answer check: {r["synthetic_check"] or "passes"}')
        print(r['user'])
    json.dump(requests, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'\nsaved {out}, sha256 {hashlib.sha256(open(out, "rb").read()).hexdigest()}')


if __name__ == '__main__':
    main()
