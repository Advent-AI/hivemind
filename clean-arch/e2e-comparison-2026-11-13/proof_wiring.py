"""The $0 proof that the wiring changes nothing (WIRING-DESIGN.md §C, D448): the parametrized ladder adapter, fed Stage B's stored inputs
(by default, and passed explicitly), with a transport that answers each judge request from Stage B's stored archive, must rebuild Stage
B's views database row for row; a wrong input must be detected. No network: a request the stored archive does not hold fails the proof.

  python3 proof_wiring.py <scratch folder>
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STAGE_B = ROOT / 'clean-arch/step4-2026-11-10/stage_b'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09'), str(STAGE_B)]
import ladder_adapter  # noqa: E402
import stored_judgements  # noqa: E402
from hivemind import jev, model  # noqa: E402

VOLATILE = {'call_id', 'created_at', 'at'}          # assigned anew by each run's archive or clock


def tables_of(db_path):
    """Every table the views database holds, except SQLite's own counter and the full-text indexes derived from other tables."""
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    try:
        names = [r[0] for r in conn.execute("select name from sqlite_master where type='table' order by name")]
    finally:
        conn.close()
    return [name for name in names if name != 'sqlite_sequence' and '_fts' not in name]


def refuse_credentials(*arguments):
    raise SystemExit('the proof read a credential: a call escaped its recorded transport')


model._key = jev._key = refuse_credentials


def recorded_transport(archive_path):
    """Answers each request with the response Stage B received for the same bytes. A row whose answer a code check refused keeps its
    key with a ':refused:' suffix (model.Archive.refuse); its response is answered by the request's own sha256, in call order when
    the same request was sent more than once."""
    import collections
    conn = sqlite3.connect(f'file:{archive_path}?mode=ro', uri=True)
    stored = collections.defaultdict(collections.deque)
    for key, response in conn.execute('select request_sha256, response_json from model_calls order by call_id'):
        stored[key.split(':', 1)[0]].append(response)
    conn.close()
    misses = []

    def transport(provider, request):
        _, sha = model.request_identity(request)
        if not stored.get(sha):
            misses.append(sha)
            raise SystemExit(f'a judge request Stage B never sent ({sha[:12]}), or sent fewer times: the wiring changed a request')
        responses = stored[sha]
        return json.loads(responses.popleft() if len(responses) > 1 else responses[0])
    transport.misses = misses
    return transport


def rows(db_path, table):
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    try:
        columns = [r[1] for r in conn.execute(f'pragma table_info({table})')]
        if not columns:
            return None
        keep = [c for c in columns if c not in VOLATILE]
        return sorted(json.dumps(dict(zip(keep, row)), sort_keys=True, default=str) for row in conn.execute(f'select {", ".join(keep)} from {table}'))
    finally:
        conn.close()


def compare(rebuilt, stored):
    """{table: (rebuilt rows, stored rows)} for every table that differs; a comparison over no rows at all is a failure, not a pass."""
    differing, compared = {}, 0
    tables = sorted(set(tables_of(rebuilt)) | set(tables_of(stored)))
    for table in tables:
        a, b = rows(rebuilt, table), rows(stored, table)
        compared += len(b or [])
        if a != b:
            differing[table] = (None if a is None else len(a), None if b is None else len(b))
    if compared == 0:
        differing['no rows compared'] = (0, 0)
    print(f'    compared {compared} stored rows over {len(tables)} tables')
    return differing


def rebuild(draw, folder, inputs=None):
    stored_folder = stored_judgements.stage_b_folders()[draw]
    transport = recorded_transport(stored_folder / 'archive.sqlite')
    ladder_adapter.replay(draw, folder, transport=transport, cap_usd=5.0, inputs=inputs)
    return compare(folder / 'views.sqlite', stored_folder / 'views.sqlite')


def main(scratch):
    scratch = Path(scratch)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    results, judged = [], 0

    def record(label, ok, detail=''):
        nonlocal judged
        judged += 1
        results.append(ok)
        print(f"{'ok ' if ok else 'FAIL'} {label} {detail}")

    for draw in ('u1', 'u2', 'u3'):
        differing = rebuild(draw, scratch / f'{draw}-default')
        record(f'{draw}: the defaults rebuild Stage B row for row', not differing, differing or '')
    tampered = scratch / 'u1-tampered.sqlite'
    shutil.copy(scratch / 'u1-default' / 'views.sqlite', tampered)
    conn = sqlite3.connect(tampered)
    for (trigger,) in conn.execute("select name from sqlite_master where type='trigger'").fetchall():
        conn.execute(f'drop trigger {trigger}')          # the copy only: its append-only guards would refuse the change
    first_column = [r[1] for r in conn.execute('pragma table_info(same_claims)')][-1]
    conn.execute(f"update same_claims set {first_column} = coalesce({first_column}, '') || 'x' where rowid = (select min(rowid) from same_claims)")
    conn.commit()
    conn.close()
    differing = compare(tampered, stored_judgements.stage_b_folders()['u1'] / 'views.sqlite')
    record('positive control: one changed field in one row of same_claims is found', list(differing) == ['same_claims'], differing)
    trace, step2 = ladder_adapter.DRAWS['u3']
    explicit = {'trace': trace, 'step2': str(step2), 'ladders': str(ladder_adapter.LADDERS), 'ladder_archive': str(ladder_adapter.LADDER_ARCHIVE),
                'cases': str(ladder_adapter.CASES), 'output_root': str(ladder_adapter.OUTPUT_ROOT)}
    differing = rebuild('u3', scratch / 'u3-explicit', explicit)
    record('u3 (a segmented trace): the inputs passed explicitly rebuild Stage B row for row', not differing, differing or '')
    second_send = ladder_adapter.LADDERS.parent.parent / 'send-2' / 'outcomes.jsonl'
    mutants = {
        'the second send as the ladder file': dict(explicit, ladders=str(second_send)),
        'u1 trace for u3': dict(explicit, trace=ladder_adapter.DRAWS['u1'][0], step2=str(ladder_adapter.DRAWS['u1'][1])),
        'the third Stage A run\'s archive as the ladder archive': dict(
            explicit, ladder_archive=str(ladder_adapter.LADDER_ARCHIVE.parents[2] / 'run-3' / 'send-1' / 'archive.sqlite')),
        'cases with one thesis described otherwise': None,
    }
    broken_cases = scratch / 'cases-broken.json'
    cases = json.loads(ladder_adapter.CASES.read_text())
    for case in cases:
        if case['case'] == 'u3/clean-1':
            case['thesis']['description'] += ' (altered)'
    broken_cases.write_text(json.dumps(cases))
    mutants['cases with one thesis described otherwise'] = dict(explicit, cases=str(broken_cases))
    for label, inputs in mutants.items():
        try:
            differing = rebuild('u3', scratch / f"u3-mutant-{label.replace(' ', '-')}", inputs)
            caught = bool(differing)
        except SystemExit as stop:
            caught, differing = True, str(stop)[:90]
        record(f'mutant, {label}: detected', caught, differing if caught else '')
    try:
        ladder_adapter.replay('u3', scratch / 'outside', transport=None, cap_usd=5.0, inputs=explicit)
        record('a live replay outside its output root: refused', False)
    except SystemExit as stop:
        record('a live replay outside its output root: refused', 'writes only under' in str(stop))
    print(f'{judged} checks judged, {sum(results)} passed')
    return all(results) and judged > 0


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1]) else 1)
