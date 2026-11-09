"""Continue a clean Stage 2 draw whose Step 1 stopped (round log §30; stage2-frozen.md, addendum on stopped Step 1 runs).

The draw's segments are `stage2-clean-d<N>` and then `stage2-clean-d<N>-segment-<K>`, in order. The next segment runs the remaining
items of the first manifest, in its order, starting from the theses after the last completed article, with the first segment's
settings, the same pinned c8 request, and the draw's limits less what earlier segments reserved and called. Its launcher then runs Steps 2-3 over every segment joined with '+', stamps every
trace segment and the library, lists the q23 candidates, and writes 'steps 1-3 done' and 'stamped'. Refuses while any process of the
draw runs, when the last segment did not stop on a network cut (a refusal or a spent limit is not continued), or when the completed articles are not a prefix of the manifest.

Usage: continue_clean_draw.py <draw number>"""
import json, sqlite3, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'poc/data/clean-e2e-2026-11-09'
NETWORK_CUTS = ('IncompleteRead', 'URLError', 'timed out', 'TimeoutError', 'ConnectionResetError', 'RemoteDisconnected',
                'ConnectionError', 'ConnectionAbortedError')   # a reply cut or never received; anything else stops the draw

LAUNCHER = '''#!/bin/zsh
set -e
REPOSITORY_ROOT={root}
SEGMENT={segment}
cd "$REPOSITORY_ROOT"
PYTHONPATH="$REPOSITORY_ROOT/src" PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider clean-arch/step1/test_runner.py -k adopted_c8 >/dev/null || {{ echo "the PRD request is not c8" >&2; exit 2 }}
(cd "$SEGMENT" && shasum -a 256 manifest.json initial.json settings.json limits.json continuation.json "$REPOSITORY_ROOT"/clean-arch/PRD.md > SHA256SUMS)
echo $$ > "$SEGMENT/run.pid"
PYTHONDONTWRITEBYTECODE=1 python3 clean-arch/step1/run_live.py --source "$REPOSITORY_ROOT/poc/data/items-nvda-2026-07-01-10-27.sqlite" \\
  --output "$SEGMENT/trace.sqlite" --manifest "$SEGMENT/manifest.json" --initial "$SEGMENT/initial.json" \\
  --settings "$SEGMENT/settings.json" --limits "$SEGMENT/limits.json" > "$SEGMENT/run.log" 2>&1
PYTHONDONTWRITEBYTECODE=1 python3 clean-arch/step2/run_forward.py "{joined}" "$SEGMENT/step2" > "$SEGMENT/step2.log" 2>&1
echo "steps 1-3 done" >> "$SEGMENT/run.log"
shasum -a 256 {parts} "$SEGMENT/step2/library.json" > "$SEGMENT/step2/inputs.sha256"
PYTHONDONTWRITEBYTECODE=1 python3 clean-arch/e2e-2026-11-09/adapter.py candidates "{joined}" "$SEGMENT/step2" > "$SEGMENT/q23-candidates.json"
echo "stamped" >> "$SEGMENT/run.log"
'''


def segments(draw):
    first = DATA / f'stage2-clean-d{draw}'
    found = [first]
    k = 2
    while (DATA / f'stage2-clean-d{draw}-segment-{k}').exists():
        found.append(DATA / f'stage2-clean-d{draw}-segment-{k}')
        k += 1
    return found, DATA / f'stage2-clean-d{draw}-segment-{k}'


def main(draw):
    if subprocess.run(['pgrep', '-f', f'stage2-clean-d{draw}[/ -]'], capture_output=True).stdout.strip():
        raise SystemExit(f'a process of clean draw {draw} is still running')
    parts, target = segments(draw)
    statuses = [json.loads((part / 'run.log').read_text().splitlines()[0]) for part in parts]
    last_status = statuses[-1]
    error = str(last_status.get('error') or '')
    if last_status.get('status') != 'failed' or not error.startswith('TransportError:') or not any(cut in error for cut in NETWORK_CUTS):
        raise SystemExit(f'{parts[-1]} did not stop on a network cut ({last_status.get("status")}: {error[:120]}); it is not continued')
    manifest = json.loads((parts[0] / 'manifest.json').read_text())
    completed, last_state, last_id = [], None, None
    for part in parts:
        conn = sqlite3.connect(f"file:{part / 'trace.sqlite'}?mode=ro", uri=True)
        for input_id, status, after in conn.execute('select input_id, status, after_state from trace order by sequence'):
            if status == 'complete':
                completed.append(input_id)
                last_state, last_id = after, input_id
        conn.close()
    if completed != manifest['item_ids'][:len(completed)]:
        raise SystemExit('the completed articles are not a prefix of the manifest')
    remaining = manifest['item_ids'][len(completed):]
    target.mkdir()
    (target / 'manifest.json').write_text(json.dumps({**manifest, 'item_ids': remaining, 'item_limit': len(remaining)}, indent=1))
    (target / 'initial.json').write_text(json.dumps(json.loads(last_state), indent=1))
    (target / 'settings.json').write_text((parts[0] / 'settings.json').read_text())
    limits = json.loads((parts[0] / 'limits.json').read_text())   # the draw's limits bound every segment together
    limits['max_usd'] = round(limits['max_usd'] - sum(s.get('reserved_usd') or 0 for s in statuses), 6)
    limits['max_calls'] = limits['max_calls'] - sum(s.get('calls') or 0 for s in statuses)
    if limits['max_usd'] <= 0 or limits['max_calls'] <= 0:
        raise SystemExit('the draw has used its limits')
    (target / 'limits.json').write_text(json.dumps(limits, indent=1))
    (target / 'continuation.json').write_text(json.dumps({'continues': [str(p) for p in parts], 'after_completed': len(completed),
                                                          'from_state_of': last_id, 'reason': last_status.get('error')}, indent=1))
    trace_parts = [str(p / 'trace.sqlite') for p in parts + [target]]
    (target / 'continue.sh').write_text(LAUNCHER.format(root=ROOT, segment=target, joined='+'.join(trace_parts), parts=' '.join(trace_parts)))
    log = open(str(target) + '.launcher.log', 'w')
    process = subprocess.Popen(['/bin/zsh', str(target / 'continue.sh')], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    print(json.dumps({'segment': str(target), 'remaining': len(remaining), 'after_completed': len(completed), 'pid': process.pid}))


if __name__ == '__main__':
    main(int(sys.argv[1]))
