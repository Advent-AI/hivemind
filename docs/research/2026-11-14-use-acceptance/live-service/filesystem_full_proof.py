"""The filesystem-full proof (OPERATING-CONTRACT.md, "Who writes, and copies: slice 4b"; row 6), run on its own, never in the suite.

Each variant gets its own new 2 MB disk image and mount point in a new temporary folder; the proof runs the writer on the stored
draw u1 with a fake judge (no model call) with its store on that disk, and always detaches and deletes the image. A full u1 replay writes about 2.5 MB there
(measured 2026-11-16), so the disk fills during the run.

  A. the free-space stop switched off (factor 0), so the disk fills inside a day: the writer must exit as a crash, its lock must be
     free once its process has ended, readers must serve the last completed day, and preflight must copy the store; whether the
     reason was recorded is reported, not required.
  B. the free-space stop as built (factor 20): the writer must stop before a day with its reason, before the disk is full.

If the image cannot be created or mounted, the proof reports UNEXERCISED and exits 2; it never reports a pass it did not run.

  python3 docs/research/2026-11-14-use-acceptance/live-service/filesystem_full_proof.py [temporary parent folder]
"""
import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STAGE_B = ROOT / 'clean-arch' / 'step4-2026-11-10' / 'stage_b'
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import live_lock, service  # noqa: E402

WRITER = '''
import sys
from pathlib import Path
here, out, locks, factor = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
sys.path[:0] = [str(here), str(here.parents[0] / 'e2e-2026-11-09'), str(here.parents[2] / 'src')]
import ladder_adapter
from hivemind import jev, live_lock, model
live_lock.LOCK_FOLDER = locks
def refuse(*arguments):
    raise SystemExit('a credential was read')
model._key = jev._key = refuse
ladder_adapter.FREE_SPACE_FACTOR = factor
from test_ladder_adapter import fake_judge
ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0)
print('the writer finished every day')
'''


def run(command):
    return subprocess.run(command, capture_output=True, text=True)


def variant(name, factor, mount, work, report):
    out, locks = mount / name, work / f'locks-{name}'
    locks.mkdir()
    (work / 'writer.py').write_text(WRITER)
    finished = run([sys.executable, str(work / 'writer.py'), str(STAGE_B), str(out), str(locks), str(factor)])
    last_error = (finished.stderr.strip().splitlines() or [''])[-1]
    store = out / 'views.sqlite'
    result = {'exit status': finished.returncode, 'last error line': last_error[:300],
              'free bytes on the disk after': shutil.disk_usage(mount).free}
    counts_file = out / 'adapter-counts.json'
    counts = json.loads(counts_file.read_text()) if counts_file.exists() and counts_file.stat().st_size else {}
    result['reason recorded beside the store'] = counts.get('stopped')
    if store.exists() and store.stat().st_size:
        with sqlite3.connect(f'file:{store}?mode=ro', uri=True) as conn:
            days = [r[0] for r in conn.execute('select day from days_completed order by id')]
        result['completed days in the store'] = len(days)
        with service.open_ledger(str(store)) as conn:
            result['readers serve'] = service.resolve_bound(conn, None) if days else 'nothing (no day completed)'
        live_lock.LOCK_FOLDER = str(locks)
        held = live_lock.acquire(store)
        live_lock.release(held)
        result['lock free after the process ended'] = True
        copies = None
        if days:
            preflight = importlib.util.module_from_spec(importlib.util.spec_from_file_location('preflight', ROOT / 'scripts' / 'preflight.py'))
            preflight.__spec__.loader.exec_module(preflight)
            [copy] = preflight.store_copies([str(store)])
            with service.open_ledger(copy) as conn:
                copies = service.resolve_bound(conn, None)
        result['preflight copy serves'] = copies
    report[name] = result
    return result


def on_its_own_disk(name, factor, work, report):
    """One variant on its own new 2 MB disk image, always detached afterwards; None when the image could not be made or mounted."""
    image, mount = work / f'{name}.dmg', work / f'mount-{name}'
    mount.mkdir()
    created = run(['hdiutil', 'create', '-size', '2m', '-fs', 'HFS+', '-volname', 'hmfull', str(image)])
    if created.returncode != 0:
        report['UNEXERCISED'] = f'{name}: the disk image could not be created: ' + created.stderr.strip()[-300:]
        return None
    mounted = run(['hdiutil', 'attach', str(image), '-nobrowse', '-mountpoint', str(mount)])
    if mounted.returncode != 0:
        report['UNEXERCISED'] = f'{name}: the disk image could not be mounted: ' + mounted.stderr.strip()[-300:]
        return None
    try:
        report[f'{name}: free bytes on the empty disk'] = shutil.disk_usage(mount).free
        return variant(name, factor, mount, work, report)
    finally:
        detached = run(['hdiutil', 'detach', str(mount)])
        if detached.returncode != 0:
            detached = run(['hdiutil', 'detach', str(mount), '-force'])
        report[f'{name}: detached'] = detached.returncode == 0


def main(arguments):
    parent = arguments[0] if arguments else None
    work = Path(tempfile.mkdtemp(prefix='hivemind-filesystem-full-', dir=parent))
    report = {'work folder': str(work)}
    try:
        a = on_its_own_disk('A-disk-fills-inside-a-day', 0, work, report)
        b = on_its_own_disk('B-free-space-stop', 20, work, report) if a is not None else None
        if a is None or b is None:
            return report, 2
        a_ok = (a['exit status'] != 0 and a.get('lock free after the process ended') and
                a.get('completed days in the store', 0) >= 1 and a['readers serve'] == a['preflight copy serves'])
        b_ok = b['exit status'] != 0 and 'WriterStopped' in b['last error line'] and bool(b['reason recorded beside the store'])
        report['A passes'], report['B passes'] = bool(a_ok), bool(b_ok)
        return report, 0 if a_ok and b_ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
        report['work folder removed'] = not work.exists()


if __name__ == '__main__':
    result, status = main(sys.argv[1:])
    print(json.dumps(result, indent=1))
    sys.exit(status)
