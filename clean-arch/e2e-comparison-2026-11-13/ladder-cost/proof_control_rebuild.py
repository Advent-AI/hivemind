"""D467's proof 3 ($0): the seeded Stage 2 control, replayed through the same wiring with every judge answer served from its stored archive
by request identity, rebuilds the stored judgements: the same requests (each found in the archive), the same views, days and shown
evidence (the list's order is the concurrent judges' completion order, so the records are compared sorted). A request the archive does not hold stops the proof (the wiring or the judge's inputs differ).

  python3 proof_control_rebuild.py d1          # writes nothing outside a temporary folder
"""
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
from hivemind import model  # noqa: E402
import adapter  # noqa: E402

DATA = ROOT / 'poc/data/clean-e2e-2026-11-09'
JUDGED = {'d1': 'judged', 'd2': 'judged', 'd3': 'judged-2'}
Q23 = {'d2': 'clean-1'}


class Missing(Exception):
    pass


def stored_answers(archive_path):
    conn = sqlite3.connect(f'file:{archive_path}?mode=ro', uri=True)
    answers = {}
    for sha, response in conn.execute("select request_sha256, response_json from model_calls order by rowid"):
        answers.setdefault(sha.split(':')[0], []).append(json.loads(response))   # a refused row's key carries ':refused:<n>'; served in order
    conn.close()
    return answers


def main():
    draw = sys.argv[1]
    judged = DATA / f'stage2-clean-{draw}' / JUDGED[draw]
    answers = stored_answers(judged / 'archive.sqlite')
    served = {'found': 0}

    def recorded(provider, request, *args, **kwargs):
        sha = model.request_identity(request)[1]
        if sha not in answers or not answers[sha]:
            raise Missing(f'request {sha[:12]} is not in the stored archive')
        served['found'] += 1
        return answers[sha].pop(0)

    trace = f"{DATA / f'stage2-clean-{draw}' / 'trace.sqlite'}+{DATA / f'stage2-clean-{draw}-segment-2' / 'trace.sqlite'}"
    step2 = DATA / f'stage2-clean-{draw}-segment-2' / 'step2'
    with tempfile.TemporaryDirectory() as folder:
        try:
            run = adapter.replay(trace, step2, Path(folder) / 'out', transport=recorded, cap_usd=10.0, q23=Q23.get(draw))
        except Missing as error:
            raise SystemExit(f'{draw}: the wiring does not rebuild the control: {error} (after {served["found"]} found)')
        rebuilt = json.loads((Path(folder) / 'out' / 'judge-requests.json').read_text())
    stored = json.loads((judged / 'judge-requests.json').read_text())
    key = lambda r: (r['day'], r['seq'], r['view'], tuple(r['shown']))
    same = sorted(rebuilt, key=key) == sorted(stored, key=key)       # judging runs concurrently: the list order is completion order
    print(f'{draw}: {served["found"]} judge requests served from the archive; rebuilt {len(rebuilt)} judgement records, stored {len(stored)}; '
          f'identical as a set of (day, seq, view, shown evidence): {same}')
    if not same:
        first = next((i for i, (a, b) in enumerate(zip(rebuilt, stored)) if a != b), min(len(rebuilt), len(stored)))
        print(f'   first difference at record {first}: rebuilt {rebuilt[first] if first < len(rebuilt) else None} | stored {stored[first] if first < len(stored) else None}')


if __name__ == '__main__':
    main()
