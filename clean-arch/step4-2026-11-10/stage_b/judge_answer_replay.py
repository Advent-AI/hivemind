"""The preflight for the frozen judge's answers ($0): every stored judge answer of the three unseeded replays, put through the
judge's own check (`judging.check_answer`) with the request text it answered, as `scripts/preflight.py` does for extraction and
matching answers (it does not cover the judge's). Prints, per draw, the answers judged, those the check refuses with their reasons,
and those it cannot judge (a call with no parsable answer, or naming no view).

  python3 clean-arch/step4-2026-11-10/stage_b/judge_answer_replay.py
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import judging  # noqa: E402

DRAWS = {draw: ROOT / f'poc/data/clean-unseeded-2026-11-10/draw-{draw}/judged' for draw in ('d1', 'd2', 'd3')}
JUDGED_VIEW = re.compile(r'^Thesis (\S+) \(', re.M)


def main():
    totals = collections.Counter()
    for draw, folder in DRAWS.items():
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        views = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        views.row_factory = sqlite3.Row
        recorded = {row[0] for row in views.execute('select call_id from judgements')}
        counts, refused = collections.Counter(), []
        for call_id, request_json, answer_json in archive.execute("select call_id, request_json, answer_json from model_calls where purpose like 'judg%'"):
            request = json.loads(request_json)
            text = request['messages'][-1]['content'] if 'messages' in request else request['input'][-1]['content']
            named = JUDGED_VIEW.search(text)
            try:
                data = json.loads(answer_json) if answer_json else None
            except ValueError:
                data = None
            if not named or not isinstance(data, dict):
                counts['not judged (no view named, or no parsable answer)'] += 1
                continue
            errors = judging.check_answer(views, named.group(1), data, text)
            counts['judged'] += 1
            kind = 'recorded' if call_id in recorded else 'not recorded'
            counts[f'{kind}, refused by the check' if errors else f'{kind}, accepted'] += 1
            if errors and call_id in recorded:
                refused.append((call_id, named.group(1), errors[:2]))
        print(f'{draw}: {dict(counts)}')
        for entry in refused[:5]:
            print(f'   a recorded judgement the check now refuses: {entry}')
        totals.update(counts)
    print(f'all: {dict(totals)}')
    if totals['judged'] == 0:
        raise SystemExit('UNEXERCISED: no answer judged')


if __name__ == '__main__':
    main()
