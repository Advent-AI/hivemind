"""Launch one draw of the release comparison (plan §2–§3; D667): checks the versions manifest, creates the draw's own ledger with its guard,
and starts run_fresh.py detached under caffeinate (the Mac must not sleep, D205), with its log and pid beside it.

    python3 launch_comparison.py <root> <label> new|old <until day> <guard usd> [--redo <component> --redo-reason <text>]

`new` runs the clean pipeline (astra-frozen, the comparison limits, the judge to <until day>, three passes); `old` runs poc-v118. Both read
the shared items database and the frozen manifest. A launch is refused when the code either system runs has uncommitted changes (src,
scripts, clean-arch, poc/config and this folder's Python: no modified or untracked file), when any file of the versions manifest differs,
or when an existing ledger's ceiling is not the given guard. A redo (D449) goes through here too.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
DATA = ROOT / 'poc/data/comparison-2026-11-17'
RUN_FRESH = ROOT / 'clean-arch/e2e-comparison-2026-11-13/run_fresh.py'
BUDGET_REPLAY = ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py'


def manifest_changed():
    manifest = json.loads((HERE / 'versions-manifest.json').read_text())
    changed = []
    for name, digest in manifest.items():
        if name == 'git_commit':
            continue
        path = ROOT / name if not name.startswith('/') else Path(name)
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            changed.append(name)
    return changed


CODE_PATHS = ['src', 'scripts', 'clean-arch', 'poc/config', 'docs/research/2026-11-17-product-comparison/stage0']


def code_not_committed():
    """Modified, staged or untracked files under the code paths (stage0: Python only)."""
    out = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all', '--', *CODE_PATHS], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout
    dirty = []
    for line in out.splitlines():
        path = line[3:]
        if path.startswith('docs/research/') and not path.endswith('.py'):
            continue
        dirty.append(line)
    return dirty


def main(root, label, kind, until_day, guard, *redo):
    dirty = code_not_committed()
    if dirty:
        raise SystemExit(f'refused: code with uncommitted changes: {dirty[:10]}')
    changed = manifest_changed()
    if changed:
        raise SystemExit(f'refused: files differ from the versions manifest: {changed}')
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    ledger = root / 'ledgers' / f'{label}.json'
    ledger.parent.mkdir(exist_ok=True)
    if not ledger.exists():
        subprocess.run([sys.executable, BUDGET_REPLAY, '--init-ledger', ledger, '--ceiling', str(float(guard))], check=True, cwd=ROOT)
    elif float(json.loads(ledger.read_text())['ceiling']) != float(guard):
        raise SystemExit(f'refused: the existing ledger {ledger} has ceiling {json.loads(ledger.read_text())["ceiling"]}, not {guard}')
    argv = ['caffeinate', '-i', '-s', sys.executable, str(RUN_FRESH), 'clean' if kind == 'new' else 'prod', '--root', str(root), '--label', label,
            '--ledger', str(ledger), '--manifest', str(DATA / 'manifest-2026-07-01-09-20.json'), '--until-day', until_day,
            '--items', str(DATA / 'items-comparison.sqlite')]
    if kind == 'new':
        argv += ['--limits', str(DATA / 'comparison-limits.json'), '--ladder-variant', 'astra-frozen', '--judge-end-day', until_day,
                 '--passes', '3']
    if redo:
        if len(redo) != 4 or redo[0] != '--redo' or redo[2] != '--redo-reason' or not redo[3].strip():
            raise SystemExit('a redo is: --redo <component> --redo-reason <text>')
        argv += list(redo)
    log = open(root / f'{label}.launcher.log', 'a')
    process = subprocess.Popen(argv, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    (root / f'{label}.pid').write_text(f'{process.pid}\n')
    print(f'{label} ({kind}) launched: pid {process.pid}, ledger {ledger} (guard ${guard}), until {until_day}')


if __name__ == '__main__':
    main(*sys.argv[1:])
