"""Does a first step continued in two parts give what an unbroken run gives? ($0; D551, condition 4.)

The stored fresh week (an unbroken run of 235 articles) is cut after article K as the real run was cut: K complete articles and
the next call in flight. The second part is then run through the real runner and the real transport, with only the network
replaced: a send is answered from the stored answer of the byte-identical request, anything else is refused, and any real
connection fails the proof. The two parts are merged and compared with the unbroken run, article by article, and as the later
steps read them. Registered expectations; the exit status is non-zero when one fails.

Mutants (each must fail an expectation, not crash): SPLIT_MUTANT=wrong-library (the second part starts from a library with one
topic missing), SPLIT_MUTANT=skipped-article (the second part skips the cut article), SPLIT_MUTANT=unchecked-second-part (the
merge takes any second part's trace: the three refusals of an unfinished second part must then fail).

  python3 split_proof.py <scratch folder> [<a file copy of the real cut trace>]
"""
import hashlib
import importlib.util
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1'), str(ROOT / 'clean-arch/step2'), str(HERE)]
import live  # noqa: E402
import runner  # noqa: E402
import run_forward  # noqa: E402
import continuation  # noqa: E402

UNBROKEN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1'
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SPLIT_AFTER = 120
MUTANT = os.environ.get('SPLIT_MUTANT')
EXPECTATIONS = []


def expect(name, holds, detail=''):
    EXPECTATIONS.append((name, bool(holds), detail))
    print(('  ok    ' if holds else '  FAIL  ') + name + (f' | {detail}' if detail else ''))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


budget_replay = load('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')


class UnknownRequest(Exception):
    """The second part sent a request the unbroken run never sent."""


class StoredAnswers:
    """The network of the proof: the stored answer of the byte-identical request, or a refusal."""

    def __init__(self, rows):
        self.by_request, self.sent, self.unknown = {}, [], 0
        for row in rows:
            response = json.loads(row['raw_response'])
            sent = response.pop('sent_request')
            self.by_request[hashlib.sha256(json.dumps(sent).encode()).hexdigest()] = (row['input_id'], response)

    def send(self, provider, request, timeout=None, max_attempts=None):
        key = hashlib.sha256(json.dumps(request).encode()).hexdigest()
        if key not in self.by_request:
            self.unknown += 1
            raise UnknownRequest('a request the unbroken run never sent')
        self.sent.append(self.by_request[key][0])
        return json.loads(json.dumps(self.by_request[key][1]))


def refuse_network(*arguments, **keywords):
    raise RuntimeError('the proof refuses every real connection')


def cut_copy(scratch):
    """The first part: the unbroken trace cut after SPLIT_AFTER articles, the next call left in flight as the runner leaves it."""
    folder = scratch / 'first/step1'
    folder.mkdir(parents=True)
    for name in ('manifest.json', 'initial.json', 'settings.json', 'limits.json'):
        shutil.copy(UNBROKEN / 'step1' / name, folder / name)
    shutil.copy(UNBROKEN / 'step1/trace.sqlite', folder / 'trace.sqlite')
    conn = sqlite3.connect(folder / 'trace.sqlite')
    with conn:
        format_retries = conn.execute("select count(*) from trace where sequence <= ? and retry_reason like '%SchemaError%'", (SPLIT_AFTER,)).fetchone()[0]
        conn.execute('delete from trace where sequence > ?', (SPLIT_AFTER + 1,))
        conn.execute("update trace set raw_response=null, result=null, after_state=null, status='in_flight', error=null, retry_reason=null where sequence = ?",
                     (SPLIT_AFTER + 1,))
        conn.execute('delete from model_calls where call_id > ?', (SPLIT_AFTER + format_retries,))
    conn.close()
    return folder, SPLIT_AFTER + format_retries + 1          # the calls the first part made, the cut one among them


def null_pattern(trace_path):
    conn = sqlite3.connect(f'file:{trace_path}?mode=ro', uri=True)
    row = conn.execute(f"select {', '.join(continuation.TRACE_COLUMNS)} from trace where status='in_flight'").fetchone()
    conn.close()
    return None if row is None else [column for column, value in zip(continuation.TRACE_COLUMNS, row) if value is None]


def run_second_part(folder, network, ledger_ceiling):
    """The real runner and the real transport on the second part's inputs; returns (outcome or the error, the ledger's state)."""
    ledger_path = folder / 'ledger.json'
    budget_replay.SharedLedger.init(ledger_path, ledger_ceiling)
    ledger = budget_replay.SharedLedger(ledger_path)
    limits = json.loads((folder / 'limits.json').read_text())
    settings = json.loads((folder / 'settings.json').read_text())
    settings['live_limits'] = limits                                      # as run_live.py does
    transport = live.LiveTransport(limits, send=network.send, ledger=ledger, wait=lambda seconds: None)
    try:
        outcome = runner.run(str(ITEMS), str(folder / 'trace.sqlite'), json.loads((folder / 'manifest.json').read_text()),
                             json.loads((folder / 'initial.json').read_text()), settings, transport, ROOT / 'clean-arch/PRD.md')
    except Exception as error:                                            # a mutant must fail an expectation, not crash
        outcome = {'status': 'raised', 'error': f'{type(error).__name__}: {error}'}
    return outcome, json.loads(ledger_path.read_text())


def main(scratch, real_cut_trace=None):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    scratch.mkdir(parents=True)
    socket.socket.connect = refuse_network
    unbroken = continuation.read_part(UNBROKEN / 'step1/trace.sqlite')
    rows = unbroken['rows']
    print(f"the unbroken run: {len(rows)} articles; cut after article {SPLIT_AFTER}; mutant: {MUTANT or 'none'}")

    first_folder, calls_used = cut_copy(scratch)
    if real_cut_trace:
        expect("the proof's cut row is empty in the same columns as the real run's cut row",
               null_pattern(first_folder / 'trace.sqlite') == null_pattern(real_cut_trace), str(null_pattern(real_cut_trace)))

    second_folder = scratch / 'second'
    record = continuation.write_inputs(first_folder, second_folder, calls_used, 3600)
    if MUTANT == 'wrong-library':
        library = json.loads((second_folder / 'initial.json').read_text())
        (second_folder / 'initial.json').write_text(json.dumps(library[:-1], ensure_ascii=False))
    if MUTANT == 'skipped-article':
        manifest = json.loads((second_folder / 'manifest.json').read_text())
        (second_folder / 'manifest.json').write_text(json.dumps(dict(manifest, item_ids=manifest['item_ids'][1:], item_limit=manifest['item_limit'] - 1)))
    manifest = json.loads((second_folder / 'manifest.json').read_text())
    limits = json.loads((second_folder / 'limits.json').read_text())
    expect('the second part holds the remaining articles in order, the cut one first',
           manifest['item_ids'] == unbroken['manifest']['item_ids'][SPLIT_AFTER:] and record['cut_call'] == manifest['item_ids'][0],
           f"{len(manifest['item_ids'])} articles")
    expect('it starts from the library as it stood after the last complete article',
           json.loads((second_folder / 'initial.json').read_text()) == json.loads(rows[SPLIT_AFTER - 1]['after_state']),
           f"{len(json.loads(rows[SPLIT_AFTER - 1]['after_state']))} topics")
    expect("its limits are the run's less what the first part used", limits['max_calls'] == 300 - calls_used and limits['max_seconds'] == 28800 - 3600,
           f"{limits['max_calls']} calls, {limits['max_seconds']} seconds")

    network = StoredAnswers(rows[SPLIT_AFTER:])
    outcome, ledger = run_second_part(second_folder, network, 100.0)
    expect('the second part completes', outcome.get('status') == 'complete', json.dumps(outcome)[:200])
    expect('every request it sent is byte-identical to the stored request of the same article, in order, and none is unknown',
           network.unknown == 0 and network.sent == unbroken['manifest']['item_ids'][SPLIT_AFTER:], f'{len(network.sent)} sent, {network.unknown} unknown')
    expect('every send was reserved and settled on the shared ledger', ledger['attempts'] == len(network.sent) and ledger['reserved'] < 1e-9 and ledger['spent'] > 0,
           f"{ledger['attempts']} attempts, spent {ledger['spent']:.4f}")

    second = continuation.read_part(second_folder / 'trace.sqlite') if (second_folder / 'trace.sqlite').exists() else {'rows': []}
    compared = ['input_id', 'before_state', 'request', 'raw_response', 'result', 'after_state', 'status', 'error', 'retry_reason']
    differing = [(row['sequence'], column) for row, stored in zip(second['rows'], rows[SPLIT_AFTER:]) for column in compared if row[column] != stored[column]]
    expect('article by article, the second part equals the unbroken run: identity, library before, request, answer, result, library after',
           len(second['rows']) == len(rows) - SPLIT_AFTER and not differing, f"{len(second['rows'])} articles, first differences {differing[:3]}")

    if MUTANT == 'unchecked-second-part':
        continuation.check_second_part = lambda rows, remaining_ids, state: None
    damaged = {'truncated (its last ten articles missing)': "delete from trace where sequence > (select max(sequence) - 10 from trace)",
               'stopped on a failure at its last article': "update trace set status='failed', error='TransportError: timed out', after_state=before_state, "
                                                          "result=null where sequence = (select max(sequence) from trace)",
               'out of order (two articles exchanged)': "update trace set input_id = case sequence when 5 then (select input_id from trace where sequence = 6) "
                                                        "when 6 then (select input_id from trace where sequence = 5) end where sequence in (5, 6)"}
    for number, (description, statement) in enumerate(damaged.items(), start=1):
        damaged_trace = scratch / f'damaged-second-{number}.sqlite'
        if (second_folder / 'trace.sqlite').exists():
            shutil.copy(second_folder / 'trace.sqlite', damaged_trace)
            conn = sqlite3.connect(damaged_trace)
            with conn:
                conn.execute(statement)
            conn.close()
        try:
            continuation.merge(first_folder / 'trace.sqlite', damaged_trace, scratch / f'merged-damaged-{number}.sqlite')
            refusal = None
        except (continuation.Refused, sqlite3.Error) as error:
            refusal = str(error) if isinstance(error, continuation.Refused) else None
        expect(f'the merge refuses a second part that is {description}', refusal is not None and not (scratch / f'merged-damaged-{number}.sqlite').exists(),
               (refusal or 'merged')[:110])

    merged_folder = scratch / 'merged/step1'
    merged_folder.mkdir(parents=True)
    try:
        continuation.merge(first_folder / 'trace.sqlite', second_folder / 'trace.sqlite', merged_folder / 'trace.sqlite')
        merge_refusal = None
    except continuation.Refused as refusal:
        merge_refusal = str(refusal)
    expect('the two parts merge', merge_refusal is None, merge_refusal or '')
    if merge_refusal is None:
        merged = continuation.read_part(merged_folder / 'trace.sqlite')
        expect("the merged run row is the unbroken run's (manifest, settings, article records, starting library)",
               all(merged[key] == unbroken[key] for key in ('manifest', 'settings', 'source_items', 'initial')))
        columns = [column for column in continuation.TRACE_COLUMNS if column != 'reserved_usd']
        differing = [(row['sequence'], column) for row, stored in zip(merged['rows'], rows) for column in columns if row[column] != stored[column]]
        expect('every row of the merged trace equals the unbroken trace (all columns but the running reservation)',
               len(merged['rows']) == len(rows) and not differing, f"{len(merged['rows'])} rows, first differences {differing[:3]}")
        cut_reservation = rows[SPLIT_AFTER]['reserved_usd'] - rows[SPLIT_AFTER - 1]['reserved_usd']
        offsets = {round(row['reserved_usd'] - stored['reserved_usd'], 9) for row, stored in zip(merged['rows'][SPLIT_AFTER:], rows[SPLIT_AFTER:])}
        expect("the running reservation goes on from the first part's, the cut call counted once more",
               offsets == {round(cut_reservation, 9)} and all(row['reserved_usd'] == stored['reserved_usd'] for row, stored in zip(merged['rows'][:SPLIT_AFTER], rows)),
               f'offset {offsets}')
        call_columns = 'purpose, config_version, model, request_sha256, request_json, response_json, answer_json, prompt_chars, input_tokens, output_tokens, config_checksum'
        calls = {}
        for name, path in (('merged', merged_folder / 'trace.sqlite'), ('unbroken', UNBROKEN / 'step1/trace.sqlite')):
            conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
            calls[name] = conn.execute(f'select {call_columns} from model_calls order by call_id').fetchall()
            conn.close()
        expect("the stored calls of the merged trace equal the unbroken run's, in order (request, answer, sizes; the configuration checksum apart)",
               [call[:-1] for call in calls['merged']] == [call[:-1] for call in calls['unbroken']], f"{len(calls['merged'])} calls")
        # The checksum the runner stores with a call covers the settings, and the settings hold the run's limits: the second part has
        # less of them, so its checksum differs. Recomputed here from the runner's own text, once with each part's limits.
        prompt, schema = runner.draft(ROOT / 'clean-arch/PRD.md')
        closing = runner.closing_check(ROOT / 'clean-arch/PRD.md')

        def checksum(settings):
            return hashlib.sha256(json.dumps({'settings': settings, 'prompt': prompt, 'closing': closing, 'schema': schema}, ensure_ascii=False).encode()).hexdigest()
        second_settings = dict(json.loads((second_folder / 'settings.json').read_text()), live_limits=json.loads((second_folder / 'limits.json').read_text()))
        first_calls = SPLIT_AFTER + (calls_used - SPLIT_AFTER - 1)
        expect("the checksum stored with the second part's calls differs from the first part's through the limits alone",
               {call[-1] for call in calls['unbroken']} == {checksum(unbroken['settings'])}
               and {call[-1] for call in calls['merged'][:first_calls]} == {checksum(unbroken['settings'])}
               and {call[-1] for call in calls['merged'][first_calls:]} == {checksum(second_settings)},
               f"{len(calls['merged'][first_calls:])} calls of the second part")
        expect('the matching step reads the merged trace as it reads the unbroken one',
               run_forward.step1_records(str(merged_folder / 'trace.sqlite')) == run_forward.step1_records(str(UNBROKEN / 'step1/trace.sqlite')))
        built = subprocess.run([sys.executable, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a/build_cases.py'), '--fresh', 'c1', '--draws', str(merged_folder),
                                '--parts', 'trace.sqlite', '--output', str(scratch / 'cases.json')], capture_output=True, text=True, cwd=ROOT)
        expect('the topics built from the merged trace are the unbroken run\'s topics',
               built.returncode == 0 and json.loads((scratch / 'cases.json').read_text()) == json.loads((UNBROKEN / 'cases/cases.json').read_text()),
               (built.stderr or built.stdout)[-160:] if built.returncode else f"{len(json.loads((UNBROKEN / 'cases/cases.json').read_text()))} topics")

    refused_folder = scratch / 'second-with-no-budget'
    continuation.write_inputs(first_folder, refused_folder, calls_used, 3600)
    starved = StoredAnswers(rows[SPLIT_AFTER:])
    outcome, ledger = run_second_part(refused_folder, starved, 0.01)
    expect('with a ledger below one reservation nothing is sent, the run stops on the ledger and the ledger is stopped',
           not starved.sent and outcome.get('status') == 'failed' and 'the shared ledger refused' in str(outcome.get('error')) and ledger['stopped'],
           json.dumps(outcome)[:160])

    failed = [name for name, holds, _ in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))
