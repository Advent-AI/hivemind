"""The positive control of the answer-choices-only path ($0; council, 2026-11-15): on the stored fresh week, the unchanged runner
with the matching and the judge held as not run writes the topics and runs all three attempts of the answer choices to the end,
and what it sends and writes equals the stored run.

Every child process loads the trap of `proof_end_to_end.py` (a call holding no live reservation on the shared ledger is refused
and counted; a call holding one is answered from the stored answer-choice archives of the fresh week; a request no archive
holds is a miss). HOME holds placeholder keys only. Also here: a first step that is not finished cannot be prepared as
completed. Registered expectations; non-zero exit when one fails. Mutant: CONTROL_MUTANT=another-article (the text of one topic's
opening article is altered where the topic builder reads it: that topic's requests are then unknown to the archives, so the
control must fail). A first version of this mutant altered the article records of the run row, which nothing later reads, and
passed: a mutant must change what the path under test reads.

  python3 choices_full_control.py <scratch folder> <merged trace of the split proof>
"""
import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
WIRING = ROOT / 'clean-arch/e2e-comparison-2026-11-13'
STORED = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1'
MANIFEST = ROOT / 'docs/research/2026-11-14-use-acceptance/fresh-week-manifest.json'
MUTANT = os.environ.get('CONTROL_MUTANT')
sys.path.insert(0, str(HERE))
import prepare_continued_draw  # noqa: E402

EXPECTATIONS = []


def expect(name, holds, detail=''):
    EXPECTATIONS.append((name, bool(holds)))
    print(('  ok    ' if holds else '  FAIL  ') + name + (f' | {detail}' if detail else ''))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def calls_of(archive):
    conn = sqlite3.connect(f'file:{archive}?mode=ro', uri=True)
    rows = conn.execute('select request_sha256, request_json, answer_json from model_calls order by call_id').fetchall()
    conn.close()
    return rows


def main(scratch, merged_trace):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    scratch.mkdir(parents=True)
    proof = load('proof_end_to_end', WIRING / 'proof_end_to_end.py')
    budget_replay = load('budget_replay', WIRING / 'budget_replay.py')

    truncated = scratch / 'unfinished-first-step.sqlite'
    shutil.copy(merged_trace, truncated)
    conn = sqlite3.connect(truncated)
    with conn:
        conn.execute('delete from trace where sequence > (select max(sequence) - 3 from trace)')
    conn.close()
    try:
        prepare_continued_draw.prepare(scratch / 'refused', 'c1', scratch / 'no-ledger.json', MANIFEST, 3, truncated, {}, ('step2', 'judge'), 'proof')
        refusal = None
    except SystemExit as stop:
        refusal = str(stop)
    expect('a first step that is not finished cannot be prepared as completed', refusal is not None and not (scratch / 'refused').exists(), (refusal or '')[:140])

    trace = Path(merged_trace)
    if MUTANT == 'another-article':
        trace = scratch / 'altered.sqlite'
        shutil.copy(merged_trace, trace)
        conn = sqlite3.connect(trace)
        with conn:                                    # the topic builder takes the article from the request of the row that opened the topic
            for sequence, request, before, after in conn.execute("select sequence, request, before_state, after_state from trace order by sequence").fetchall():
                if len(json.loads(after)) > len(json.loads(before)):
                    built = json.loads(request)
                    payload, end = json.JSONDecoder().raw_decode(built['messages'][1]['content'])
                    payload['source_item']['text'] += ' An added sentence.'
                    built['messages'][1]['content'] = json.dumps(payload, ensure_ascii=False) + built['messages'][1]['content'][end:]
                    conn.execute('update trace set request = ? where sequence = ?', (json.dumps(built), sequence))
                    break
        conn.close()

    site = scratch / 'trap-site'
    site.mkdir()
    (site / 'sitecustomize.py').write_text(proof.SITECUSTOMIZE)
    (scratch / 'no-vectors.json').write_text('{}')
    counts = scratch / 'trap-counts.jsonl'
    (scratch / 'trap-config.json').write_text(json.dumps({
        'src': str(ROOT / 'src'), 'counts': str(counts), 'delay': 0.0, 'step1_trace': str(merged_trace), 'embeddings': str(scratch / 'no-vectors.json'),
        'archives': [str(STORED / f'ladder/send-{number}/archive.sqlite') for number in (1, 2, 3)]}))
    home = scratch / 'home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    environment = dict(os.environ, PYTHONPATH=str(site), HIVEMIND_PROOF_TRAP=str(scratch / 'trap-config.json'), HOME=str(home))

    root = scratch / 'week'
    root.mkdir()
    ledger = root / 'ledger.json'
    budget_replay.SharedLedger.init(ledger, 1.0)
    prepare_continued_draw.prepare(root, 'c1', ledger, MANIFEST, 3, trace, {'note': 'the split proof: the stored fresh week cut after article 120'},
                                   ('step2', 'judge'), 'the positive control of the answer choices alone')
    launched = subprocess.run([sys.executable, str(WIRING / 'run_fresh.py'), 'clean', '--root', str(root), '--label', 'c1', '--ledger', str(ledger),
                               '--manifest', str(MANIFEST), '--passes', '3'], cwd=ROOT, capture_output=True, text=True, env=environment)
    record = json.loads((root / 'c1/run.json').read_text())
    state = json.loads(ledger.read_text())
    trapped = [json.loads(line) for line in counts.read_text().splitlines()] if counts.exists() else []
    print('runner exit', launched.returncode, '| draw', record['state'], '|', str(record.get('stopped'))[:150])
    components = record['components']
    expect('the draw ends complete: the topics and the answer choices run, the matching and the judge held as not run',
           record['state'] == 'complete' and components.get('cases', {}).get('state') == 'completed' and components.get('ladder', {}).get('state') == 'completed'
           and components['step2']['state'] == 'skipped' and components['judge']['state'] == 'skipped' and not (root / 'c1/step2').exists())
    expect("the topics equal the stored run's",
           (root / 'c1/cases/cases.json').exists() and json.loads((root / 'c1/cases/cases.json').read_text()) == json.loads((STORED / 'cases/cases.json').read_text()))
    same_requests, same_outcomes, sends = True, True, 0
    for number in (1, 2, 3):
        new_folder, stored_folder = root / f'c1/ladder/send-{number}', STORED / f'ladder/send-{number}'
        if not (new_folder / 'outcomes.jsonl').exists():
            same_requests = same_outcomes = False
            continue
        new_calls, stored_calls = calls_of(new_folder / 'archive.sqlite'), calls_of(stored_folder / 'archive.sqlite')
        sends += len(new_calls)
        same_requests = same_requests and sorted(new_calls) == sorted(stored_calls)
        outcomes = [sorted((json.dumps(json.loads(line), sort_keys=True) for line in (folder / 'outcomes.jsonl').read_text().splitlines()))
                    for folder in (new_folder, stored_folder)]
        same_outcomes = same_outcomes and outcomes[0] == outcomes[1]
    expect('in each of the three attempts, the requests sent and the answers stored equal the stored run\'s', same_requests, f'{sends} calls')
    expect("in each of the three attempts, the outcomes written equal the stored run's (ladders, refusals, due days, every field)", same_outcomes)
    expect('every call held a live reservation and was answered from the archives: none unreserved, none unknown',
           trapped and all(entry['live'] and 'miss' not in entry for entry in trapped), f'{len(trapped)} trapped calls')
    expect('the ledger counted exactly the calls sent, and nothing is left in flight',
           state['attempts'] == len(trapped) == sends and state['reserved'] < 1e-9 and not state['stopped'], f"{state['attempts']} attempts, charged ${state['spent']:.4f}")
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
