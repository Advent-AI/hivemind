"""The coverage-start reading over all 22 seed questions (baseline-design.md, round 8): each question reads each item of the company's latest
report once for its own starting figure, with the second version's request unchanged (baseline_read.SYSTEM, TASK, SCHEMA, the judging step's
model setting) and its code check (baseline_read.kept_figures). The report is chosen by code: the covered company's earnings-release items
(category T1, the company's ticker among the item's object identifiers) of the latest publication day before coverage start, read from their page
text with tables. Each question's lines are read from the frozen v108 ledgers at coverage start and refused unless the three draws agree. Three
sends per question and item; the send n of a question is its two items' sends n together.

The task text is the second version (baseline_read.TASK, the pilot's and round 8's) or the third (baseline_read.TASK_V3, round 14: only the sentence on
the lines to write when the report does not state the quantity differs, checked byte for byte against the second version's requests).

usage: python3 baseline_all.py check [--task 2|3|4] [--coverage-start 2026-07-01]                               (builds every request; sends nothing)
       python3 baseline_all.py send <out.json> [--task 2|3|4] [--questions v19,v20] [--coverage-start 2026-07-01] (three sends each; a transport
                                                                                                                   failure is re-sent with the same bytes)
"""
import concurrent.futures
import json
import sqlite3
import sys
import time

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts', HERE]
import baseline_read as br  # noqa: E402
import resend_filing as rf  # noqa: E402
from hivemind import config, extraction, model, placement  # noqa: E402

COVERAGE_START = '2026-07-01'
TICKER = 'NVDA'
SEEDS = [f'v{k}' for k in range(1, 23)]
SENDS = 3
DRAWS = {f'd{n}': f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d{n}' for n in (1, 2, 3)}
PILOT = f'{HERE}/baseline-read.json'          # the second version's requests as sent: the release requests of v10 and v12 must be the same bytes
TASKS = {2: br.TASK, 3: br.TASK_V3, 4: br.TASK_V4}


def latest_report(items, coverage_start=COVERAGE_START):
    """The covered company's earnings-release items of the latest publication day before coverage start: the filed ones (channel EDGAR) when that day
    has any, since the company's newsroom and investor-site copies of the same documents are not marked as copies; else all of them."""
    rows = [r for r in items.execute("select input_id, publication_day, publisher, title, object_identifiers, channel from items where category='T1' "
                                     "and publication_day < ? order by publication_day, input_id", (coverage_start,))
            if any(o.get('kind') == 'ticker' and o.get('value') == TICKER for o in json.loads(r['object_identifiers'] or '[]'))]
    if not rows:
        raise SystemExit(f'no earnings-release item of {TICKER} before {coverage_start}')
    day = max(r['publication_day'] for r in rows)
    of_day = [r for r in rows if r['publication_day'] == day]
    return [r for r in of_day if r['channel'] == 'EDGAR'] or of_day


def question_lines(cfg, report_day):
    """Each seed question's lines as the reading shows them, from each draw's ledger at coverage start (the second version read draw 1)."""
    item = {'publication_day': report_day, 'category': 'T1', 'object_identifiers': [{'value': TICKER}]}
    per_draw = {}
    for draw, run in DRAWS.items():
        views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
        views.row_factory = sqlite3.Row
        shown = {v['view_id']: v for v in extraction.shown_views(views, cfg, item, [TICKER])}
        per_draw[draw] = {view_id: placement.question_lines([shown[view_id]]) for view_id in SEEDS}
    if any(lines != per_draw['d1'] for lines in per_draw.values()):
        raise SystemExit('a seed question reads differently in the three draws; refusing')
    return per_draw['d1']


def build(version=2, questions=SEEDS, coverage_start=COVERAGE_START):
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    items = sqlite3.connect(f'file:{rf.ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    pages = sqlite3.connect(f'file:{br.PAGES}?mode=ro', uri=True)
    report = latest_report(items, coverage_start)
    texts = {r['input_id']: pages.execute('select text from items where input_id=?', (r['input_id'],)).fetchone()[0] for r in report}
    lines = question_lines(cfg, report[0]['publication_day'])
    requests, second = {}, {}
    for view_id in questions:
        for r in report:
            head = (f'[Question]\n' + '\n'.join(lines[view_id]) + f'\n\n[Report] id {r["input_id"]}, published {r["publication_day"]} by '
                    f'{r["publisher"]}: {r["title"]}\n{texts[r["input_id"]]}\n\n')
            requests[(view_id, r['input_id'])] = model.build_request(cfg.rejudging, br.SYSTEM, head + TASKS[version], br.SCHEMA, 'extraction', cfg.provider)
            second[(view_id, r['input_id'])] = model.build_request(cfg.rejudging, br.SYSTEM, head + br.TASK, br.SCHEMA, 'extraction', cfg.provider)
    pilot = json.load(open(PILOT))['requests']
    for view_id in ('v10', 'v12'):
        if coverage_start == COVERAGE_START and (view_id, br.RELEASE) in second and model.request_identity(second[(view_id, br.RELEASE)])[1] != pilot[view_id]:
            raise SystemExit(f'{view_id}: the release request is not the second version as sent; refusing')
    for key, body in requests.items():           # the version's only difference from the second version is its task text
        swapped = json.loads(json.dumps(body).replace(json.dumps(TASKS[version])[1:-1], json.dumps(br.TASK)[1:-1]) if version != 2 else json.dumps(body))
        if swapped != second[key]:
            raise SystemExit(f'{key}: the request differs from the second version beyond the task text; refusing')
    return cfg, report, texts, requests


def main():
    version = int(sys.argv[sys.argv.index('--task') + 1]) if '--task' in sys.argv else 2
    questions = sys.argv[sys.argv.index('--questions') + 1].split(',') if '--questions' in sys.argv else SEEDS
    coverage_start = sys.argv[sys.argv.index('--coverage-start') + 1] if '--coverage-start' in sys.argv else COVERAGE_START
    cfg, report, texts, requests = build(version, questions, coverage_start)
    if sys.argv[1] == 'check':
        print(f'report chosen: {len(report)} items of {report[0]["publication_day"]}: ' + '; '.join(
            f'{r["input_id"]} ({r["title"]}, page text {len(texts[r["input_id"]]):,} characters)' for r in report))
        print(f'task version {version}; {len(requests)} requests ({len(questions)} questions x {len(report)} items), {len(requests) * SENDS} sends; seed '
              f'lines equal in the three draws; v10 and v12 second-version release requests are the pilot\'s as sent; every request differs from the second '
              f'version only in its task text')
        for key in [k for k in (('v9', report[0]['input_id']), ('v20', report[-1]['input_id'])) if k in requests]:
            body = requests[key]
            user = body['messages'][1]['content']
            print(f'\n----- {key[0]} on {key[1]}: {len(json.dumps(body)):,} characters, key {model.request_identity(body)[1][:16]}')
            print(user[:user.index('[Report]')] + user[user.index('[Report]'):user.index('\n', user.index('[Report]'))] + '\n[…page text…]\n' + user[-900:])
        return
    out = sys.argv[2]
    jobs = [(view_id, input_id, n) for (view_id, input_id) in requests for n in range(SENDS)]

    def one(job):
        """One reply. Only a transport failure is re-sent (the same bytes); a reply that is not JSON is kept and counts as no figure."""
        view_id, input_id, n = job
        for attempt in range(4):
            try:
                reply = model.openai_transport(cfg.provider, requests[(view_id, input_id)], timeout=300)
                break
            except Exception as error:
                if attempt == 3:
                    return job, {'figures': [], 'failure': f'transport: {type(error).__name__}: {str(error)[:200]}', 'tokens': [0, 0]}
                print(f'  {view_id} {input_id} send {n}: {type(error).__name__}; re-sent in {30 * (attempt + 1)} s', flush=True)
                time.sleep(30 * (attempt + 1))
        usage = reply.get('usage') or {}
        tokens = [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]
        content = reply['choices'][0]['message']['content']
        try:
            data = json.loads(content)
        except ValueError:
            return job, {'figures': [], 'failure': 'reply is not JSON', 'raw': content, 'tokens': tokens}
        return job, {'figures': br.kept_figures(data, texts[input_id]), 'tokens': tokens}

    results = {view_id: {r['input_id']: [None] * SENDS for r in report} for view_id in questions}
    record = lambda: {'task_version': version, 'coverage_start': coverage_start, 'report': [r['input_id'] for r in report], 'report_day': report[0]['publication_day'],
                      'requests': {f'{v}|{i}': model.request_identity(b)[1] for (v, i), b in requests.items()}, 'results': results}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for (view_id, input_id, n), r in pool.map(one, jobs):
            results[view_id][input_id][n] = r
            json.dump(record(), open(out + '.partial.json', 'w'), indent=1, ensure_ascii=False)
    json.dump(record(), open(out, 'w'), indent=1, ensure_ascii=False)
    price_in, price_out = model.PRICES[cfg.rejudging.model]
    sends = [r for by_item in results.values() for rs in by_item.values() for r in rs]
    cost = sum(r['tokens'][0] / 1e6 * price_in + r['tokens'][1] / 1e6 * price_out for r in sends)
    for view_id in questions:
        for n in range(SENDS):
            kept = [f for input_id in results[view_id] for f in results[view_id][input_id][n]['figures'] if f['kept']]
            refused = [f for input_id in results[view_id] for f in results[view_id][input_id][n]['figures'] if not f['kept']]
            print(f'{view_id} send {n}: kept {len(kept)} ' + ' | '.join(f'{f["value"]} ({f["period"][:30]})' for f in kept)
                  + (f'; refused {len(refused)}' if refused else ''))
    failures = [r['failure'] for r in sends if r.get('failure')]
    print(f'\n{len(sends)} sends, {len(failures)} failures {failures[:3]}; cost ${cost:.4f} at the published rates ({price_in}/{price_out} per '
          f'million tokens, input uncached); saved {out}')


if __name__ == '__main__':
    main()
