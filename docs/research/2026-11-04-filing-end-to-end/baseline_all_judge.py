"""The window-end judging requests of the all-seeds test (baseline-design.md, round 8), sending nothing. For each draw of the frozen v108 run and
each question of the frozen judgement ruler that kept a starting figure in any reading send:
  - a judged question: the control is its last stored judging request on or before the window end, rebuilt and refused unless its archive key
    matches (sent three times); arm n is the same request with reading send n's kept figures as evidence records at the head of its evidence
    block and the block's count raised, nothing else changed (sent once each; with no kept figure it is the control's request);
  - v10 and v12, never judged: arm n is step 2's constructed first judgement (`judging._lines_english` on the draw's ledger at the window end:
    question, ladder, the starting-figure records, dependencies, themes in force); a reading send that kept nothing is not judged.
The records are written as the frozen extraction writes a release's actual figures (tier fact, speaker and original source the company, original
day the report's day, source the item read); the quote as the model wrote it, the one-line as the model wrote it, followed by the unit it read when the value has no scale of its own.
v10 and v12 are always present: a reading send that kept nothing is recorded as not judged. Every request is checked by a synthetic answer citing a
starting-figure record (or, for a control, a stored one) through `judging.check_answer` against the text to be sent.

usage: python3 baseline_all_judge.py <reading.json> <out.json>     (then `shasum -a 256 <out.json> > <out.json>.sha256` after reading it)
"""
import hashlib
import json
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', HERE]
import oracle_build  # noqa: E402
from baseline_all import DRAWS, SENDS  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

COMPANY = 'NVIDIA Corporation'
FIRST_ID = 9101
WINDOW_END = '2026-07-14'
SCORED = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v16', 'v17', 'v18', 'v19', 'v20', 'v22']
NEVER_JUDGED = ('v10', 'v12')
HEADER = re.compile(r'\[Evidence in view under this thesis, (\d+) items\]\n')
HIDDEN = re.compile(r'\[Not shown: \d+ more pieces in force[^\n]*\]\n')


def kept(reading, view_id, n):
    """Reading send n's kept figures for a question, over the report's items in the order they were read, each with the item it came from."""
    return [dict(f, input_id=input_id) for input_id in reading['report'] for f in reading['results'][view_id][input_id][n]['figures'] if f['kept']]


SCALE = re.compile(r'%|\d\s*(?:k|m|b|t|bn|mn|mm|bln|mln|bil)\b|\b(?:thousand|million|billion|trillion)s?\b', re.I)


def one_line_of(f):
    """The model's one-line, followed by the unit it read when the value carries no scale or percent sign of its own (a table cell such as
    "(1,757)" or "$53,783": the row's quote carries no scale, and the one-line need not)."""
    return f['one_line'] if SCALE.search(f['value']) else f'{f["one_line"]} (unit: {f["unit"]})'


def pieces_of(figures, day):
    return [{'evidence_id': f'e{FIRST_ID + k}', 'tier': 'fact', 'speaker': COMPANY, 'original_who': COMPANY, 'original_day': day,
             'sources': [{'input_id': f['input_id'], 'publication_day': day}], 'one_line': one_line_of(f), 'quote': f['quote']}
            for k, f in enumerate(figures)]


def with_records(user, lines):
    """The stored request with the records' lines at the head of its evidence block (after the not-shown line, when there is one)."""
    header = HEADER.search(user)
    hidden = HIDDEN.match(user, header.end())
    at = hidden.end() if hidden else header.end()
    return (user[:header.start()] + f'[Evidence in view under this thesis, {int(header.group(1)) + len(lines)} items]\n' + user[header.end():at]
            + '\n'.join(lines) + '\n' + user[at:])


def block_ids(user):
    return re.findall(r'^- (e\d+) \[', user.split('[Evidence in view under this thesis', 1)[1].split('\n\n[', 1)[0], re.M)


def main():
    reading, out = json.load(open(sys.argv[1])), sys.argv[2]
    day = reading['report_day']
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    with open(config.prompt_path(cfg.rejudging.prompt_version + '.txt'), encoding='utf-8') as handle:
        judging_system = handle.read()
    with_figures = [v for v in SCORED if v in NEVER_JUDGED or any(kept(reading, v, n) for n in range(SENDS))]
    requests = {}
    for draw, run in DRAWS.items():
        conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
        draw_ids = {r[0] for r in conn.execute('select evidence_id from evidence')}
        for view_id in with_figures:
            base = {'draw': draw, 'run': run, 'view_id': view_id}
            if view_id in NEVER_JUDGED:
                if store.evidence_in_force(conn, view_id) or store.current_state(conn, view_id):
                    raise SystemExit(f'{draw} {view_id} has evidence or a judgement; the design assumed neither')
                for n in range(SENDS):
                    figures = kept(reading, view_id, n)
                    if not figures:
                        requests[f'{draw} {view_id} arm {n}'] = dict(base, arm='arm', reading_send=n, not_judged='the reading kept no figure', sends=0)
                        continue
                    pieces = pieces_of(figures, day)
                    lines = judging._lines_english(conn, view_id, store.view(conn, view_id), store.rungs_of(conn, view_id), pieces,
                                                   store.dependencies_of(conn, view_id), None, judging.themes_in_force(conn, view_id))
                    requests[f'{draw} {view_id} arm {n}'] = dict(base, arm='arm', reading_send=n, system=judging_system, user='\n'.join(lines),
                                                                 constructed=True, pieces=pieces, sends=1)
                continue
            row = conn.execute('select request_sha256, rung, publication_day from judgements where view_id=? and publication_day<=? '
                               'order by judgement_id desc limit 1', (view_id, WINDOW_END)).fetchone()
            stored = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (row['request_sha256'],)).fetchone()[0])
            system = next(m['content'] for m in stored['messages'] if m['role'] == 'system')
            user = next(m['content'] for m in stored['messages'] if m['role'] == 'user')
            if model.request_identity(model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider))[1] != row['request_sha256']:
                raise SystemExit(f'{draw} {view_id}: the rebuilt request is not the stored one; refusing')
            requests[f'{draw} {view_id} control'] = dict(base, arm='control', system=system, user=user, constructed=False, pieces=[], sends=SENDS,
                                                         stored_rung=row['rung'], stored_day=row['publication_day'])
            for n in range(SENDS):
                pieces = pieces_of(kept(reading, view_id, n), day)
                if draw_ids & {p['evidence_id'] for p in pieces}:
                    raise SystemExit(f'{draw} {view_id}: a record id collides with the draw\'s evidence ids')
                arm_user = with_records(user, oracle_build.evidence_lines(conn, view_id, pieces)) if pieces else user
                if block_ids(arm_user) != [p['evidence_id'] for p in pieces] + block_ids(user):
                    raise SystemExit(f'{draw} {view_id} arm {n}: the evidence block does not hold the records then the stored pieces')
                if int(HEADER.search(arm_user).group(1)) != int(HEADER.search(user).group(1)) + len(pieces):
                    raise SystemExit(f'{draw} {view_id} arm {n}: the block count is wrong')
                requests[f'{draw} {view_id} arm {n}'] = dict(base, arm='arm', reading_send=n, system=system, user=arm_user, constructed=bool(pieces),
                                                             pieces=pieces, sends=1)
        for key, r in requests.items():
            if r['draw'] != draw or not r['sends']:
                continue
            body = model.build_request(cfg.rejudging, r['system'], r['user'], schema, 'judgement', cfg.provider)
            r['request_sha256'] = model.request_identity(body)[1]
            r['system_is_judging_v7'] = r['system'] == judging_system
            cite = r['pieces'][0]['evidence_id'] if r['pieces'] else block_ids(r['user'])[0]
            r['synthetic_check'] = oracle_build.synthetic_check(conn, view_id=r['view_id'], user=r['user'], cite=cite)
    sent = {k: r for k, r in requests.items() if r['sends']}
    print(f'questions with a kept figure in some reading send: {with_figures}')
    print(f'{len(sent)} requests to send, {sum(r["sends"] for r in sent.values())} sends; not judged: '
          f'{[k for k, r in requests.items() if not r["sends"]]}')
    problems = [k for k, r in sent.items() if r['synthetic_check'] or not r['system_is_judging_v7']]
    print(f'synthetic answer check passes on {len(sent) - len(problems)} of {len(sent)}; system is judging-v7 on all: {not problems}; problems: {problems}')
    for key, r in sent.items():
        print(f'  {key}: {len(r["system"]) + len(r["user"]):,} characters, {len(r["pieces"])} records, key {r["request_sha256"][:12]}')
    json.dump(requests, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'saved {out}, sha256 {hashlib.sha256(open(out, "rb").read()).hexdigest()}')


if __name__ == '__main__':
    main()
