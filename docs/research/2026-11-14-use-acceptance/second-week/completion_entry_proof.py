"""Can the unchanged runner finish a stored draw, running only the matching and the judge on unchanged inputs? ($0; D558.)

On the stored fresh week (an unbroken draw whose matching and judgements are stored): a new draw is prepared from its first
step, topics and answer choices alone, as the real completion will be prepared; the unchanged `run_fresh.py` then runs, every
child process under the trap of `proof_end_to_end.py` (a call with no live reservation on the shared ledger is refused; a call
with one is answered from the stored archives; an unknown request is a miss) and a HOME that holds placeholder keys only. What
it writes must equal what the stored draw holds. Registered expectations; non-zero exit when one fails. Mutant:
COMPLETION_MUTANT=other-choices (the first and second attempts of the answer choices exchanged in the prepared draw: the judge
then reads other choices, so its requests are unknown to the archive).

  python3 completion_entry_proof.py <scratch folder>
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
MUTANT = os.environ.get('COMPLETION_MUTANT')
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


def judgements_of(views):
    conn = sqlite3.connect(f'file:{views}?mode=ro', uri=True)
    rows = conn.execute('select view_id, seq, input_id, rung, reasons, cited_evidence_json, cited_views_json, pushes_json, changed, why_changed from judgements order by judgement_id').fetchall()
    conn.close()
    return rows


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
    (scratch / 'trap-config.json').write_text(json.dumps({
        'src': str(ROOT / 'src'), 'counts': str(counts), 'delay': 0.0, 'step1_trace': str(STORED / 'step1/trace.sqlite'), 'embeddings': str(STORED / 'step2/embeddings.json'),
        'archives': [str(STORED / 'step2/jev.sqlite'), str(STORED / 'judge/draw-c1/archive.sqlite')]}))
    home = scratch / 'home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    environment = dict(os.environ, PYTHONPATH=str(site), HIVEMIND_PROOF_TRAP=str(scratch / 'trap-config.json'), HOME=str(home))

    root = scratch / 'week'
    root.mkdir()
    ledger = root / 'ledger.json'
    budget_replay.SharedLedger.init(ledger, 5.0)
    _, stamps = prepare_continued_draw.prepare_completion(root, 'c1', ledger, MANIFEST, 3, STORED, 'the proof: the stored fresh week')
    draw = root / 'c1'
    if MUTANT == 'other-choices':
        (draw / 'ladder/send-1').rename(draw / 'ladder/send-x')
        (draw / 'ladder/send-2').rename(draw / 'ladder/send-1')
        (draw / 'ladder/send-x').rename(draw / 'ladder/send-2')
    launched = subprocess.run([sys.executable, str(WIRING / 'run_fresh.py'), 'clean', '--root', str(root), '--label', 'c1', '--ledger', str(ledger),
                               '--manifest', str(MANIFEST), '--passes', '3'], cwd=ROOT, capture_output=True, text=True, env=environment)
    record = json.loads((draw / 'run.json').read_text())
    state = json.loads(ledger.read_text())
    trapped = [json.loads(line) for line in counts.read_text().splitlines()] if counts.exists() else []
    components = record['components']
    print('runner exit', launched.returncode, '| draw', record['state'], '|', str(record.get('stopped'))[:160])
    expect('the draw ends complete, the matching and the judge each run once',
           record['state'] == 'complete' and all(components.get(name, {}).get('state') == 'completed' and len(components[name]['attempts']) == 1 for name in ('step2', 'judge')))
    expect('the first step, the topics and the answer choices were not run again',
           all(len(components[name]['attempts']) == 1 and 'copied unchanged' in components[name]['attempts'][0].get('note', '') for name in ('step1', 'cases', 'ladder'))
           and not any((draw / f'{name}-redo').exists() for name in ('step1', 'step2')))
    import hashlib
    unchanged = all(hashlib.sha256((draw / relative).read_bytes()).hexdigest() == digest for relative, digest in stamps.items())
    expect('the copied inputs are unchanged after the run (the trace, the topics, every attempt of the answer choices)', unchanged, f'{len(stamps)} files')
    same_library = all((draw / 'step2' / name).exists() and json.loads((draw / 'step2' / name).read_text()) == json.loads((STORED / 'step2' / name).read_text())
                       for name in ('library.json', 'decisions.json'))
    expect("the matching's library and decisions equal the stored draw's", same_library)
    new_views, stored_views = draw / 'judge/draw-c1/views.sqlite', STORED / 'judge/draw-c1/views.sqlite'
    def by_question_and_day(path):                    # within a day's round the judge sends its questions side by side: their order in the record is not the program's
        return sorted(json.dumps(request, sort_keys=True) for request in json.loads(Path(path).read_text()))
    same_requests = (draw / 'judge/draw-c1/judge-requests.json').exists() and by_question_and_day(draw / 'judge/draw-c1/judge-requests.json') == by_question_and_day(STORED / 'judge/draw-c1/judge-requests.json')
    expect("the judge's requests equal the stored draw's: the same request for every question on every day", same_requests)
    same_judgements = new_views.exists() and judgements_of(new_views) == judgements_of(stored_views)
    expect("every judgement equals the stored draw's (the choice, the reasons, what it cites)", same_judgements,
           f'{len(judgements_of(new_views)) if new_views.exists() else 0} judgements')
    expect('every call held a live reservation and was answered from the archives: none unreserved, none unknown',
           trapped and all(entry['live'] and 'miss' not in entry for entry in trapped), f'{len(trapped)} trapped calls')
    expect('the ledger counted every call, nothing is left in flight, and it is not stopped',
           state['attempts'] == len(trapped) and state['reserved'] < 1e-9 and not state['stopped'], f"{state['attempts']} attempts, charged ${state['spent']:.4f}")
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
