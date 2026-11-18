"""Prepare a draw folder whose first step is a continued one (D551), so that the unchanged runner (`run_fresh.py`) runs the later
steps on it: the merged trace as `<root>/<label>/step1/trace.sqlite`, and a record that holds the first step as completed in two
parts. The record's identity is exactly what the runner writes at a first launch (kind, label, ledger, options), so a launch with
other options or another ledger is refused by the runner itself.

A later step can be held as not run (`not_run`, with the reason): the runner treats a component recorded as `skipped` as done,
the same way it records the answer choices and the judge of a draw that opened no topic. Only the matching and the judge can be
held so: the topics and the answer choices read the first step alone.

  python3 prepare_continued_draw.py <root> <label> <ledger> <manifest> <passes> <merged trace> <continuation record json> [<reason> step2 judge]
"""
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import continuation  # noqa: E402


def prepare(root, label, ledger, manifest_path, passes, merged_trace, continuation_record, not_run=(), reason=None):
    folder = Path(root) / label
    step1 = folder / 'step1'
    if folder.exists():
        raise SystemExit(f'{folder} exists')
    manifest = json.loads(Path(manifest_path).read_text())
    try:                                              # a stopped or unfinished first step is never recorded as completed
        articles = continuation.check_whole(merged_trace)
    except continuation.Refused as refusal:
        raise SystemExit(f'refused: the trace is not a finished first step: {refusal}')
    if continuation.read_part(merged_trace)['manifest']['item_ids'] != manifest['item_ids'] or articles != len(manifest['item_ids']):
        raise SystemExit("refused: the trace is not a first step of this manifest's articles")
    step1.mkdir(parents=True)
    shutil.copy(merged_trace, step1 / 'trace.sqlite')
    (step1 / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    (step1 / 'continuation.json').write_text(json.dumps(continuation_record, indent=1) + '\n')
    moment = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    record = {'identity': {'kind': 'clean', 'label': label, 'ledger': str(Path(ledger).resolve()),
                           'options': {'until_day': manifest['until_day'], 'passes': int(passes), 'from_day': manifest['from_day'],
                                       'manifest': str(Path(manifest_path).resolve())}},
              'state': 'running',
              'components': {'step1': {'attempts': [{'folder': 'step1', 'state': 'completed', 'started at': moment, 'ended at': moment,
                                                     'note': 'continued in two parts and merged (continuation.json); not run by this launcher'}],
                                       'state': 'completed', 'folder': 'step1',
                                       'note': 'continued in two parts after a call cut in flight (D551): see step1/continuation.json'}}}
    if set(not_run) - {'step2', 'judge'} or (not_run and set(not_run) != {'step2', 'judge'}):
        raise SystemExit('only the matching and the judge together can be held as not run: the judge reads the matching')
    if not_run and not (reason or '').strip():
        raise SystemExit('a step held as not run needs its reason')
    for component in not_run:
        record['components'][component] = {'attempts': [], 'state': 'skipped', 'note': f'not run: {reason}'}
    (folder / 'run.json').write_text(json.dumps(record, indent=1) + '\n')
    return record


def sha256_of(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_completion(root, label, ledger, manifest_path, passes, earlier_draw, note):
    """Prepare a draw that finishes an earlier one (D558): the earlier draw's first step, topics and answer choices are copied
    unchanged and recorded as completed, so the unchanged runner runs what is left, the matching and then the judge. The earlier
    draw is not touched. Refuses unless the earlier draw holds a finished first step and every attempt of the answer choices."""
    earlier, folder = Path(earlier_draw), Path(root) / label
    if folder.exists():
        raise SystemExit(f'{folder} exists')
    manifest = json.loads(Path(manifest_path).read_text())
    record = json.loads((earlier / 'run.json').read_text())
    for component in ('step1', 'cases', 'ladder'):
        if record['components'].get(component, {}).get('state') != 'completed':
            raise SystemExit(f'refused: the earlier draw did not complete {component}')
    folders = {component: earlier / record['components'][component]['folder'] for component in ('step1', 'cases', 'ladder')}
    try:
        articles = continuation.check_whole(folders['step1'] / 'trace.sqlite')
    except continuation.Refused as refusal:
        raise SystemExit(f'refused: the earlier first step is not finished: {refusal}')
    if continuation.read_part(folders['step1'] / 'trace.sqlite')['manifest']['item_ids'] != manifest['item_ids'] or articles != len(manifest['item_ids']):
        raise SystemExit("refused: the earlier first step is not this manifest's")
    cases = json.loads((folders['cases'] / 'cases.json').read_text())
    for number in range(1, int(passes) + 1):
        outcomes = [json.loads(line) for line in (folders['ladder'] / f'send-{number}' / 'outcomes.jsonl').read_text().splitlines()]
        if sorted(outcome['case'] for outcome in outcomes) != sorted(case['case'] for case in cases):
            raise SystemExit(f'refused: attempt {number} of the answer choices does not hold every topic once')
    folder.mkdir(parents=True)
    stamps = {}
    for component, source in folders.items():
        shutil.copytree(source, folder / component)
        for path in sorted(source.rglob('*')):
            if path.is_file() and path.suffix in ('.sqlite', '.json', '.jsonl'):
                relative = f'{component}/{path.relative_to(source)}'
                stamps[relative] = sha256_of(path)
                if sha256_of(folder / relative) != stamps[relative]:
                    raise SystemExit(f'refused: {relative} changed in the copy')
    moment = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    copied = f'copied unchanged from {earlier} ({note}); not run by this launcher'
    new_record = {'identity': {'kind': 'clean', 'label': label, 'ledger': str(Path(ledger).resolve()),
                               'options': {'until_day': manifest['until_day'], 'passes': int(passes), 'from_day': manifest['from_day'],
                                           'manifest': str(Path(manifest_path).resolve())}},
                  'state': 'running',
                  'components': {component: {'attempts': [{'folder': component, 'state': 'completed', 'started at': moment, 'ended at': moment, 'note': copied}],
                                             'state': 'completed', 'folder': component, 'note': copied} for component in ('step1', 'cases', 'ladder')}}
    (folder / 'run.json').write_text(json.dumps(new_record, indent=1) + '\n')
    (folder / 'completion.json').write_text(json.dumps({'finishes': str(earlier), 'note': note, 'copied_sha256': stamps}, indent=1) + '\n')
    return new_record, stamps


if __name__ == '__main__':
    root, label, ledger, manifest_path, passes, merged_trace, record_path = sys.argv[1:8]
    prepare(root, label, ledger, manifest_path, passes, merged_trace, json.loads(Path(record_path).read_text()),
            not_run=tuple(sys.argv[9:]), reason=sys.argv[8] if len(sys.argv) > 8 else None)
    print('prepared', Path(root) / label)
