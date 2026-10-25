"""D160: actual entry points reject ignoring the third input or the registered request limit."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
source = (ROOT / 'poc/hierarchy_study/ohio_sequence.py').read_text()
source = source.replace("ROOT = Path(__file__).resolve().parents[2]", f"ROOT = Path({str(ROOT)!r})")
mutants = {
    'control': source,
    'drops-third': source.replace('for ident in item_ids:', 'for ident in item_ids[:2]:'),
    'ignores-limit': source.replace("self.max_requests = read(manifest)['max_requests'] if manifest.exists() else MAX_REQUESTS", 'self.max_requests = MAX_REQUESTS'),
}
with tempfile.TemporaryDirectory(prefix='hivemind-three-inputs-') as name:
    path = Path(name)
    (path / 'test_parameters.py').write_text((ROOT / 'poc/hierarchy_study/test_ohio_sequence.py').read_text())
    env = dict(os.environ, PYTHONPATH=f'{path}:{ROOT}/src:{ROOT}/poc/hierarchy_study', PYTHONDONTWRITEBYTECODE='1')
    for label, code in mutants.items():
        (path / 'ohio_sequence.py').write_text(code)
        result = subprocess.run([sys.executable, '-B', '-m', 'pytest', '-q', str(path/'test_parameters.py'), '-k', 'd160'], cwd=path, env=env, capture_output=True, text=True)
        text = result.stdout + result.stderr
        (OUT / f'parameters-{label}.txt').write_text(text)
        print(label, result.returncode)
        if label == 'control':
            assert result.returncode == 0, text
        else:
            assert result.returncode == 1 and ('AssertionError' in text or 'DID NOT RAISE' in text), text
