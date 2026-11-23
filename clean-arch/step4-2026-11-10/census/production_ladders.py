"""$0 census of the ladders production's frozen extraction (v74i, low reasoning) wrote in the three same-day control draws of
2026-11-09 (D392), read from the stored answers. It runs production's own ladder checks and the sealed split's two checks (PRD 11, E3:
`empty_rung`, `band_problem`, loaded as source text from the sealed worktree) over every candidate ladder, and prints, for every
five-rung numeric asset ladder, which end of the number its Strongly bullish rung holds, by question and by request (a request sent in
several draws is the same bytes, so a difference there is the model's sampling alone). Nothing is written.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 production_ladders.py"""
import collections, json, re, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPLIT = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/split.py')
DRAWS = [ROOT / f'poc/data/clean-e2e-2026-11-09/stage2-control-{d}/archive.sqlite' for d in ('d1', 'd3', 'd4')]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction  # noqa: E402


def split_checks():
    source = SPLIT.read_text()
    namespace = {'re': re}
    exec(source[source.index('SCALE = {'):source.index('def _number(value)')], namespace)
    return namespace['empty_rung'], namespace['band_problem']


def main():
    empty_rung, band_problem = split_checks()
    counts, refused, directions, same_request = collections.Counter(), [], collections.defaultdict(list), collections.defaultdict(list)
    for path in DRAWS:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        try:
            rows = conn.execute("select call_id, answer_json, request_sha256 from model_calls where purpose = 'extract'").fetchall()
        finally:
            conn.close()
        counts['extraction answers read'] += len(rows)
        for call_id, answer, request_sha in rows:
            for candidate in (json.loads(answer) or {}).get('candidates') or []:
                rungs, kind = candidate['rungs'], candidate['kind']
                counts['candidate ladders'] += 1
                counts[f'{len(rungs)} rungs'] += 1
                problems = {'check_ladder': extraction.check_ladder(rungs, kind), 'check_bounds': extraction.check_bounds(rungs),
                            'empty_rung': empty_rung(rungs), 'band_problem': band_problem(rungs)}
                for check, problem in problems.items():
                    if problem:
                        counts[f'refused by {check}'] += 1
                        refused.append((path.parent.name, call_id, check, problem, candidate['question']))
                if kind == 'asset' and len(rungs) == 5 and not problems['check_ladder'] and not problems['check_bounds']:
                    first = extraction.normalise_ladder(rungs, kind)[0]
                    end = 'the highest band' if first.get('hi') is None and first.get('lo') is not None else \
                          'the lowest band' if first.get('lo') is None and first.get('hi') is not None else 'no open band'
                    counts[f'asset number ladder: Strongly bullish holds {end}'] += 1
                    neutral = extraction.normalise_ladder(rungs, kind)[2]
                    directions[re.sub(r'\W+', ' ', candidate['question'].lower())[:60]].append((path.parent.name, call_id, end, neutral.get('lo'), neutral.get('hi')))
                    same_request[request_sha[:8]].append((path.parent.name, call_id, end, neutral.get('lo'), neutral.get('hi')))
    if not counts['candidate ladders']:
        raise SystemExit('no candidate ladder was read: the census judged nothing')
    for key, value in sorted(counts.items()):
        print(f'{value:5}  {key}')
    for row in refused:
        print('refused:', row)
    print('\nfive-rung asset number ladders, grouped by the first 60 characters of the question (draw, call, bullish end, Neutral band):')
    for question, writes in sorted(directions.items()):
        print(f'- {question}')
        for write in writes:
            print('    ', write)
    print('\nthe same request (byte-identical, by its sha256) laddered in more than one draw (draw, call, bullish end, Neutral band):')
    for sha, writes in sorted(same_request.items()):
        if len(writes) > 1:
            print(f'- request {sha}: ' + ('SAME ladder position' if len({w[2:] for w in writes}) == 1 else 'DIFFERENT'))
            for write in writes:
                print('    ', write)


if __name__ == '__main__':
    main()
