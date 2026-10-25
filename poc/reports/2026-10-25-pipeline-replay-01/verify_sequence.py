"""D159: exercise the sequential-read check with the removed day-start fan-out restored on a scratch copy."""
import ast
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def verify():
    current = (ROOT / 'src/hivemind/replay.py').read_text()
    old = subprocess.check_output(['git', 'show', '7033c87:src/hivemind/replay.py'], cwd=ROOT, text=True)
    function = next(n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == 'pre_extract')
    old_function = '\n'.join(old.splitlines()[function.lineno - 1:function.end_lineno])
    fanout = '''        fresh = [(item, route) for item, route in to_run if not route.resume_from]
        if len(fresh) > 1:
            extracted = pre_extract(conn, archive, cfg, universe, fresh, transport, log)
            to_run = [(item, dispatch.Route('extract', route.sequence_no, 'matched' if item['input_id'] in extracted else None, route.reason))
                      for item, route in to_run]
'''
    mutant = current.replace('import datetime', 'import concurrent.futures\nimport json\nfrom . import extraction\n\n'
                             'EXTRACTION_WORKERS = 8\n\n' + old_function + '\n\nimport datetime')
    mutant = mutant.replace('        for item, route in to_run:', fanout + '        for item, route in to_run:')
    assert mutant != current
    outcomes = {}
    with tempfile.TemporaryDirectory(prefix='hivemind-order-proof-') as directory:
        base = Path(directory)
        shutil.copytree(ROOT / 'src', base / 'src', ignore=shutil.ignore_patterns('__pycache__'))
        (base / 'tests/fixtures').mkdir(parents=True)
        shutil.copy(ROOT / 'tests/test_sequential_replay.py', base / 'tests')
        shutil.copy(ROOT / 'tests/fixtures/sequential-rubin.json', base / 'tests/fixtures')
        shutil.copytree(ROOT / 'poc/config', base / 'poc/config')
        shutil.copy(ROOT / 'poc/universe.json', base / 'poc/universe.json')
        environment = dict(os.environ, PYTHONPATH=str(base / 'src'), PYTHONDONTWRITEBYTECODE='1')
        for label, source in [('control', current), ('parallel', mutant)]:
            (base / 'src/hivemind/replay.py').write_text(source)
            result = subprocess.run([sys.executable, '-m', 'pytest', '-q', str(base / 'tests/test_sequential_replay.py')
                                     + '::test_next_extraction_reads_committed_prior_view'], cwd=base,
                                    env=environment, capture_output=True, text=True)
            output = result.stdout + result.stderr
            (OUT / f'verified-{label}.txt').write_text(output)
            outcomes[label] = result.returncode
            if label == 'parallel':
                assert 'test_next_extraction_reads_committed_prior_view' in output
                assert 'AssertionError' in output and 'NameError' not in output
    assert outcomes == {'control': 0, 'parallel': 1}, outcomes
    sys.path.insert(0, str(ROOT / 'src'))
    from hivemind import replay
    ledgers = []
    for path in sorted((ROOT / 'poc/data').glob('views-2026-10-25-v15-*.sqlite')):
        with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as db:
            db.row_factory = sqlite3.Row
            try:
                replay.refuse_unfinished_parallel(db)
                ledgers.append({'ledger': path.name, 'refused': False})
            except replay.StaleHandoverError as error:
                ledgers.append({'ledger': path.name, 'refused': True, 'reason': str(error)})
    assert len(ledgers) == 8 and sum(x['refused'] for x in ledgers) == 1
    result = {'mutation': outcomes, 'legacy_read_only': ledgers}
    (OUT / 'sequence-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    verify()
