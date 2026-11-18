"""Proof of the extension and of the path the two-week run will take ($0; D563, steps 1 to 3). Registered expectations; a
non-zero exit when one fails. Every process runs under the trap of `proof_end_to_end.py` (a call with no live reservation on
the ledger is refused; a call with one is answered from stored archives; a request the archives do not hold is a miss and
fails the call) and a HOME holding placeholder keys only.

On the stored fresh week (2026-09-22..28, 235 articles, an unbroken run from empty):
  1. the first run: its first 120 articles, exactly as an unbroken run of those 120 writes them (the stored rows and calls);
  2. the second run: the real launcher (`clean-arch/step1/run_live.py`) reads articles 121 to 235 from the inputs `extension.py`
     writes (the first run's last library as its starting library), answered by the trap from the stored answers: it must
     send the stored requests byte for byte (the handoff the live run will use);
  3. the join of the two must be the stored trace (every column of every row; the run row's manifest, articles and starting
     library; every call record but its timing);
  4. five mutants of the second run must each be refused by the join;
  5. a draw prepared from the joined trace, run by the unchanged runner through the matching, topics, answer choices and judge,
     answered from the stored week's archives, must write what the stored draw holds; no judge request may hold material dated
     after its day.

  python3 extension_proof.py <scratch folder>
"""
import collections
import importlib.util
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WIRING = ROOT / 'clean-arch/e2e-comparison-2026-11-13'
STORED = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1'
MANIFEST = ROOT / 'docs/research/2026-11-14-use-acceptance/fresh-week-manifest.json'
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
CUT = 120
sys.path[:0] = [str(HERE), str(HERE.parent / 'second-week')]
import extension  # noqa: E402
import prepare_continued_draw  # noqa: E402

EXPECTATIONS = []
TIMING = ('call_id', 'seconds', 'created_at')


def expect(name, holds, detail=''):
    EXPECTATIONS.append((name, bool(holds)))
    print(('  ok    ' if holds else '  FAIL  ') + name + (f' | {detail}' if detail else ''))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def article_of(request_json):
    request = json.loads(request_json)
    return json.JSONDecoder().raw_decode(request['messages'][1]['content'])[0]['source_item']['id']


def trace_rows(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        return [list(row) for row in conn.execute(f"select {', '.join(extension.TRACE_COLUMNS)} from trace order by sequence")]
    finally:
        conn.close()


def call_rows(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        columns = [row[1] for row in conn.execute('pragma table_info(model_calls)') if row[1] not in TIMING]
        return [list(row) for row in conn.execute(f"select {', '.join(columns)} from model_calls order by call_id")]
    finally:
        conn.close()


def run_row(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        return [json.loads(value) for value in conn.execute('select manifest, settings, source_items, initial_theses from run').fetchone()]
    finally:
        conn.close()


def first_run(stored_trace, output):
    """The first 120 articles as an unbroken run of them writes: the stored rows and calls, its manifest and articles cut to them."""
    shutil.copy(stored_trace, output)
    manifest, _, items, _ = run_row(stored_trace)
    ids = manifest['item_ids'][:CUT]
    conn = sqlite3.connect(output)
    with conn:
        conn.execute('update run set manifest = ?, source_items = ?',
                     (json.dumps(dict(manifest, item_ids=ids, item_limit=CUT, until_day=items[CUT - 1]['publication_day']), ensure_ascii=False),
                      json.dumps(items[:CUT], ensure_ascii=False)))
        conn.execute('delete from trace where sequence > ?', (CUT,))
        later = [call_id for call_id, request in conn.execute('select call_id, request_json from model_calls') if article_of(request) not in ids]
        conn.executemany('delete from model_calls where call_id = ?', [(call_id,) for call_id in later])
    conn.close()
    return ids


def mutate(second_trace, kind, scratch):
    """A copy of the second run's trace, broken one way."""
    copy = scratch / f'second-{kind}.sqlite'
    shutil.copy(second_trace, copy)
    conn = sqlite3.connect(copy)
    with conn:
        manifest, _, items, initial = run_row(second_trace)
        if kind == 'dropped-article':
            conn.execute('delete from trace where sequence = 5')
            conn.execute('update trace set sequence = sequence - 1 where sequence > 5')
        elif kind == 'wrong-start':
            conn.execute('update run set initial_theses = ?', (json.dumps(initial[:-1], ensure_ascii=False),))
        elif kind == 'duplicated-article':
            first_id = run_row(STORED / 'step1/trace.sqlite')[0]['item_ids'][0]
            conn.execute('update run set manifest = ?', (json.dumps(dict(manifest, item_ids=[first_id] + manifest['item_ids'][1:]), ensure_ascii=False),))
            conn.execute('update trace set input_id = ? where sequence = 1', (first_id,))
        elif kind == 'broken-transition':
            before = json.loads(conn.execute('select before_state from trace where sequence = 10').fetchone()[0])
            conn.execute('update trace set before_state = ? where sequence = 10', (json.dumps(before[:-1], ensure_ascii=False),))
        elif kind == 'day-back':
            early = dict(items[-1], publication_day='2026-09-21')
            conn.execute('update run set source_items = ?', (json.dumps(items[:-1] + [early], ensure_ascii=False),))
    conn.close()
    return copy


def main(scratch):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    scratch.mkdir(parents=True)
    proof = load('proof_end_to_end', WIRING / 'proof_end_to_end.py')
    budget_replay = load('budget_replay', WIRING / 'budget_replay.py')
    site = scratch / 'trap-site'
    site.mkdir()
    (site / 'sitecustomize.py').write_text(proof.SITECUSTOMIZE)
    counts = scratch / 'trap-counts.jsonl'
    archives = [str(STORED / 'step2/jev.sqlite')] + [str(STORED / f'ladder/send-{n}/archive.sqlite') for n in (1, 2, 3)] + [str(STORED / 'judge/draw-c1/archive.sqlite')]
    (scratch / 'trap-config.json').write_text(json.dumps({'src': str(ROOT / 'src'), 'counts': str(counts), 'delay': 0.0,
                                                          'step1_trace': str(STORED / 'step1/trace.sqlite'), 'embeddings': str(STORED / 'step2/embeddings.json'),
                                                          'archives': archives}))
    home = scratch / 'home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    environment = dict(os.environ, PYTHONPATH=str(site), HIVEMIND_PROOF_TRAP=str(scratch / 'trap-config.json'), HOME=str(home))
    stored_trace = STORED / 'step1/trace.sqlite'

    print('1. the first run')
    first_folder = scratch / 'first'
    first_folder.mkdir()
    first_ids = first_run(stored_trace, first_folder / 'trace.sqlite')
    stored_rows = trace_rows(stored_trace)
    expect('the first run holds the stored first 120 rows unchanged', trace_rows(first_folder / 'trace.sqlite') == stored_rows[:CUT], f'{CUT} rows')

    print('2. the second run, by the real launcher from the inputs extension.py writes')
    manifest, settings, items, _ = run_row(stored_trace)
    rest = {'entity': manifest['entity'], 'from_day': items[CUT]['publication_day'], 'until_day': manifest['until_day'],
            'item_limit': len(manifest['item_ids']) - CUT, 'item_ids': manifest['item_ids'][CUT:]}
    (scratch / 'rest-manifest.json').write_text(json.dumps(rest, indent=1))
    second_folder = scratch / 'second'
    record = extension.write_inputs(first_folder, scratch / 'rest-manifest.json', second_folder, json.loads((STORED / 'step1/limits.json').read_text()))
    expect("the second run's starting library is the first run's last library",
           json.loads((second_folder / 'initial.json').read_text()) == json.loads(stored_rows[CUT - 1][6]), f"{len(record['library_topics'])} topics")
    ledger = scratch / 'ledger.json'
    budget_replay.SharedLedger.init(ledger, 100.0)
    launched = subprocess.run([sys.executable, str(ROOT / 'clean-arch/step1/run_live.py'), '--source', str(ITEMS), '--output', str(second_folder / 'trace.sqlite'),
                               '--manifest', str(second_folder / 'manifest.json'), '--initial', str(second_folder / 'initial.json'),
                               '--settings', str(second_folder / 'settings.json'), '--limits', str(second_folder / 'limits.json'), '--shared-ledger', str(ledger)],
                              cwd=ROOT, capture_output=True, text=True, env=environment)
    print('   launcher exit', launched.returncode, '|', launched.stdout.strip()[-160:], launched.stderr.strip()[-200:])
    second_rows = trace_rows(second_folder / 'trace.sqlite')
    same_requests = [row[3] for row in second_rows] == [row[3] for row in stored_rows[CUT:]]
    expect('the launcher sent the stored requests byte for byte, starting from the first run\'s library', same_requests, f'{len(second_rows)} requests')

    print('3. the join')
    joined = scratch / 'joined.sqlite'
    extension.join(first_folder / 'trace.sqlite', second_folder / 'trace.sqlite', joined)
    joined_rows = trace_rows(joined)
    differing = [(a[0], [extension.TRACE_COLUMNS[i] for i in range(len(a)) if a[i] != b[i] and not (extension.TRACE_COLUMNS[i] == 'reserved_usd' and abs((a[i] or 0) - (b[i] or 0)) < 1e-6)])
                 for a, b in zip(joined_rows, stored_rows) if a != b]
    differing = [entry for entry in differing if entry[1]]
    expect('the joined trace is the stored trace: every column of every row (reservations to a millionth)', len(joined_rows) == len(stored_rows) and not differing,
           f'{len(joined_rows)} rows; differing {differing[:3]}')
    stored_run, joined_run = run_row(stored_trace), run_row(joined)
    expect("the run row's manifest, articles and starting library are the stored run's",
           joined_run[0] == stored_run[0] and joined_run[2] == stored_run[2] and joined_run[3] == stored_run[3])
    expect('every call record is the stored one but its timing', call_rows(joined) == call_rows(stored_trace), f'{len(call_rows(joined))} calls')

    print('4. mutants of the second run')
    for kind in ('dropped-article', 'wrong-start', 'duplicated-article', 'broken-transition', 'day-back'):
        broken = mutate(second_folder / 'trace.sqlite', kind, scratch)
        try:
            extension.join(first_folder / 'trace.sqlite', broken, scratch / f'joined-{kind}.sqlite')
            refused = None
        except extension.Refused as refusal:
            refused = str(refusal)
        expect(f'the join refuses the mutant "{kind}"', refused is not None, refused or 'joined')

    print('5. the later steps on the joined trace, by the unchanged runner')
    root = scratch / 'week'
    root.mkdir()
    ledger = root / 'ledger.json'
    budget_replay.SharedLedger.init(ledger, 100.0)
    prepare_continued_draw.prepare(root, 'c1', ledger, MANIFEST, 3, joined, {'note': 'the extension proof: the stored fresh week split after article 120'})
    launched = subprocess.run([sys.executable, str(WIRING / 'run_fresh.py'), 'clean', '--root', str(root), '--label', 'c1', '--ledger', str(ledger),
                               '--manifest', str(MANIFEST), '--passes', '3'], cwd=ROOT, capture_output=True, text=True, env=environment)
    draw = root / 'c1'
    record = json.loads((draw / 'run.json').read_text())
    print('   runner exit', launched.returncode, '| draw', record['state'], '|', str(record.get('stopped'))[:160])
    expect('the draw ends complete; the first step is not run again; the later steps each run once',
           record['state'] == 'complete' and len(record['components']['step1']['attempts']) == 1
           and all(record['components'].get(name, {}).get('state') == 'completed' and len(record['components'][name]['attempts']) == 1 for name in ('step2', 'cases', 'ladder', 'judge')))
    expect("the matching's library and decisions equal the stored draw's",
           all(json.loads((draw / 'step2' / name).read_text()) == json.loads((STORED / 'step2' / name).read_text()) for name in ('library.json', 'decisions.json')))
    expect("the topics equal the stored draw's", json.loads((draw / 'cases/cases.json').read_text()) == json.loads((STORED / 'cases/cases.json').read_text()))
    outcomes = lambda folder: collections.Counter(json.dumps({k: v for k, v in json.loads(line).items() if k not in ('requests', 'seconds')}, sort_keys=True)
                                                  for n in (1, 2, 3) for line in (folder / f'ladder/send-{n}/outcomes.jsonl').read_text().splitlines())
    expect("the answer choices of the three attempts equal the stored draw's", outcomes(draw) == outcomes(STORED), f'{sum(outcomes(draw).values())} outcomes')
    requests = lambda folder: sorted(json.dumps(request, sort_keys=True) for request in json.loads((folder / 'judge/draw-c1/judge-requests.json').read_text()))
    expect("the judge's requests equal the stored draw's", requests(draw) == requests(STORED), f'{len(requests(draw))} requests')
    judgements = lambda folder: sqlite3.connect(f"file:{folder / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True).execute(
        'select view_id, seq, input_id, rung, reasons, cited_evidence_json from judgements order by judgement_id').fetchall()
    expect("every judgement equals the stored draw's", judgements(draw) == judgements(STORED), f'{len(judgements(draw))} judgements')
    late = []
    store = sqlite3.connect(f"file:{draw / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    first_seen = dict(store.execute('select evidence_id, min(publication_day) from evidence_sources group by evidence_id'))
    for request in json.loads((draw / 'judge/draw-c1/judge-requests.json').read_text()):
        unknown = [e for e in request['shown'] if e not in first_seen]
        late += [(request['day'], e, first_seen.get(e)) for e in request['shown'] if e in unknown or first_seen[e] > request['day']]
    judged = len(json.loads((draw / 'judge/draw-c1/judge-requests.json').read_text()))
    expect('no judge request holds material dated after its day', judged and not late, f'{judged} requests checked; later material: {late[:3]}')
    trapped = [json.loads(line) for line in counts.read_text().splitlines()] if counts.exists() else []
    expect('every call held a live reservation and was answered from the stored answers: none unreserved, none unknown',
           trapped and all(entry['live'] and 'miss' not in entry for entry in trapped), f'{len(trapped)} trapped calls')
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
