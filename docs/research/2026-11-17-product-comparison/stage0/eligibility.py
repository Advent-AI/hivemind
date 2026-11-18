"""Whether the six draws may give a release verdict (D667; plan §1.4 item 10; D675), and the fingerprints of the stores the reading uses.

    python3 eligibility.py <run root> <out json>

A draw is eligible when its record says complete under its own label, with the registered identity `launch_comparison.py` gives it
(kind, ledger, items database, manifest, 07-01 to 09-20, three passes; for the new system the comparison limits, astra-frozen and the judge
to 09-20). The six draws pass together when:
- they were launched within one hour of each other (a draw's launch: its first component's first attempt);
- every attempt the draw's ledger records (`<ledger>.attempts.jsonl`, failed sends included) and every model call stored anywhere in the
  draw falls within 72 hours of the first launch.
The output records, per draw, the launch, the last call, and the sha256 of the views and archive files the reading reads
(`mapping.store_paths`); `mapping.py export` refuses without a passing output and records the same fingerprints, and the scorer refuses
readings that do not carry them.
"""
import datetime
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapping  # noqa: E402

DATA = Path('/Users/lchingen/hivemind/poc/data/comparison-2026-11-17')
LAUNCH_WINDOW = datetime.timedelta(hours=1)
SEND_WINDOW = datetime.timedelta(hours=72)


def local(stamp):
    """A naive local time from either stored form: '2026-11-17T22:05:13-0800' (launcher) or '2026-11-17T22:06:16' (archives)."""
    try:
        return datetime.datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%S%z').astimezone().replace(tzinfo=None)
    except ValueError:
        return datetime.datetime.strptime(stamp[:19], '%Y-%m-%dT%H:%M:%S')


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def last_call(draw_folder):
    """The latest model call stored in any database under the draw's folder, and how many databases hold calls."""
    latest, databases = None, 0
    for path in sorted(Path(draw_folder).rglob('*.sqlite')):
        conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
        if not conn.execute("select 1 from sqlite_master where type='table' and name='model_calls'").fetchone():
            continue
        databases += 1
        stamp = conn.execute('select max(created_at) from model_calls').fetchone()[0]
        if stamp and (latest is None or local(stamp) > latest):
            latest = local(stamp)
    return latest, databases


def expected_identity(run_root, draw):
    """The identity launch_comparison.py registers for a counted draw (plan §2; D667)."""
    options = {'until_day': '2026-09-20', 'passes': 3, 'from_day': '2026-07-01', 'manifest': str(DATA / 'manifest-2026-07-01-09-20.json'),
               'items': str(DATA / 'items-comparison.sqlite')}
    if draw.startswith('new'):
        options.update(limits=str(DATA / 'comparison-limits.json'), ladder_variant='astra-frozen', judge_end_day='2026-09-20')
    return {'kind': 'clean' if draw.startswith('new') else 'prod', 'label': draw, 'ledger': str(Path(run_root) / 'ledgers' / f'{draw}.json'),
            'options': options}


def last_attempt(ledger_path):
    """The latest attempt the ledger's log records (failed sends and refusals included), how many lines it holds, and why the log cannot
    establish the timing, or None: the log must exist and reconcile with the ledger (one line per settled attempt and per refusal, the
    settled charges summing to the spend, nothing still reserved), since the ledger writes its log line after its own state."""
    path = Path(str(ledger_path).replace('.json', '.attempts.jsonl'))
    if not path.exists():
        return None, 0, f'{path.name} missing'
    lines = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    ledger = json.loads(Path(ledger_path).read_text())
    charged = sum(line.get('charged', 0) for line in lines)
    if len(lines) != ledger['attempts'] + ledger['refused'] or abs(charged - ledger['spent']) > 1e-6 or ledger['reserved'] > 1e-9:
        return None, len(lines), (f"{path.name} holds {len(lines)} lines and ${charged:.6f} against the ledger's {ledger['attempts']} attempts, "
                                  f"{ledger['refused']} refusals, ${ledger['spent']:.6f} spent and ${ledger['reserved']:.6f} reserved")
    return (max(local(line['at']) for line in lines) if lines else None), len(lines), None


SECTION_INPUTS = {'step1': ['trace.sqlite'], 'step2': ['decisions.json', 'library.json'], 'cases': ['cases.json'], 'ladder': ['send-1/outcomes.jsonl',
                  'send-2/outcomes.jsonl', 'send-3/outcomes.jsonl']}


def section_inputs(run_root, draw, record):
    """The files the §1.6 tools read from a new draw (DESIGN-1.6.md §0), each in the folder its run record names (a redo's folder after a
    redo), by path relative to the draw."""
    out = []
    if not draw.startswith('new'):
        return out
    for component, names in SECTION_INPUTS.items():
        entry = record['components'].get(component, {})
        if entry.get('state') == 'completed':
            out += [f"{entry['folder']}/{name}" for name in names if (Path(run_root) / draw / entry['folder'] / name).exists()]
    return out


def verified(eligibility, run_root, draw, relative):
    """A file a §1.6 tool reads, refused unless the eligibility output fingerprinted it and it is unchanged."""
    digest = eligibility['draws'][draw].get('inputs', {}).get(relative)
    path = Path(run_root) / draw / relative
    if digest is None or sha256(path) != digest:
        raise SystemExit(f'refused: {draw}/{relative} is not fingerprinted by the eligibility check, or changed since')
    return path


def check(run_root):
    run_root = Path(run_root).resolve()
    draws, problems = {}, []
    for draw in mapping.DRAWS:
        record = json.loads((run_root / draw / 'run.json').read_text())
        if record.get('identity') != expected_identity(run_root, draw):
            problems.append(f"{draw}: registered identity {record.get('identity')} is not the counted draw's {expected_identity(run_root, draw)}")
        starts = [local(a['started at']) for c in record['components'].values() for a in c.get('attempts', []) if a.get('started at')]
        try:
            paths = mapping.store_paths(run_root, draw)                # refuses an incomplete draw
        except SystemExit as refusal:                                 # recorded; the finished draws are still fingerprinted (diagnostic)
            problems.append(str(refusal))
            paths = None
        latest, databases = last_call(run_root / draw)
        attempt, attempts, unreconciled = last_attempt(run_root / 'ledgers' / f'{draw}.json')
        if unreconciled:
            problems.append(f'{draw}: the timing cannot be established: {unreconciled}')
        if attempt and (latest is None or attempt > latest):
            latest = attempt
        draws[draw] = {'launch': min(starts).isoformat() if starts else None, 'last call': latest.isoformat() if latest else None,
                       'databases with calls': databases, 'ledger attempts': attempts,
                       'stores': {Path(p).name: {'path': str(p), 'sha256': sha256(p)} for p in paths} if paths else {},
                       'inputs': {rel: sha256(run_root / draw / rel) for rel in section_inputs(run_root, draw, record)}}
        if not starts:
            problems.append(f'{draw}: no launch recorded')
    launches = [datetime.datetime.fromisoformat(d['launch']) for d in draws.values() if d['launch']]
    if launches and max(launches) - min(launches) > LAUNCH_WINDOW:
        problems.append(f'launches span {max(launches) - min(launches)}, more than one hour')
    first = min(launches) if launches else None
    for draw, d in draws.items():
        if first and d['last call'] and datetime.datetime.fromisoformat(d['last call']) > first + SEND_WINDOW:
            problems.append(f"{draw}: a call at {d['last call']}, more than 72 h after the first launch {first.isoformat()}")
    return {'eligible': not problems, 'problems': problems, 'first launch': first.isoformat() if first else None, 'draws': draws}


def write(result, path):
    """The eligibility file's one writer: the mapping records this file's sha256, so its bytes are part of the chain."""
    Path(path).write_text(json.dumps(result, indent=1) + '\n')


if __name__ == '__main__':
    result = check(sys.argv[1])
    write(result, sys.argv[2])
    print('ELIGIBLE' if result['eligible'] else 'NOT ELIGIBLE: ' + '; '.join(result['problems']))
