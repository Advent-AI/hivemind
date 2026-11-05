"""Step 1, second version, of the coverage-start baseline (baseline-design.md): each open question reads the company's latest report once for its
own starting figure, one question in focus. Code keeps a figure only when its quote is the report's own text (the extraction's comparison form, with
a currency or percent sign joined to its number, since a flattened table prints each cell on its own line), at least the extraction's eight
characters, carries a label, and prints the figure written as the value. v10 and v12 are the questions under test; v4 (another party's figure)
and v7 (a yes-or-no question) are controls that should return no figure. The model setting is the judging step's (gpt-6-luna, medium reasoning).

usage: python3 baseline_read.py check                 (builds the requests and prints them; sends nothing)
       python3 baseline_read.py send <out.json>       (three sends per question)
"""
import concurrent.futures
import json
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts', HERE]
import resend_filing as rf  # noqa: E402
from hivemind import config, extraction, model, placement  # noqa: E402

RELEASE = 'edgar:NVDA:0001045810-26-000051:q1fy27pr.htm'
PAGES = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.page.sqlite'
QUESTIONS = ('v10', 'v12', 'v4', 'v7')
SYSTEM = ('You are a research analyst starting coverage of a company. You read its latest financial report once, to record where one open question '
          'starts: the latest figure the report gives for the question\'s quantity. You write only what the report states.')
TASK = ('Write the figure this question\'s quantity stands at in the report\'s most recent reported period. When the report does not state the '
        'quantity under the question\'s name, write the lines it does state that the quantity is made of or reported as, under the report\'s own '
        'names. For each figure: quote is the report\'s own text, copied exactly; for a table row, the row from its label to the figure you report, '
        'as printed. value is that figure as printed, and unit its unit. period is the period the figure covers, as the report names it. basis is '
        'the accounting basis the report gives the figure (for example GAAP or non-GAAP), or "as stated". one_line states the figure, its period and '
        'its basis in one sentence. Return an empty list when the report gives no figure for this question\'s quantity.')
LINES_V2 = ('When the report does not state the quantity under the question\'s name, write the lines it does state that the quantity is made of or '
            'reported as, under the report\'s own names.')
LINES_V3 = ('When the report does not state the quantity under the question\'s name, write only the lines it is computed from, or the line that is this '
            'same quantity under another name, under the report\'s own names; never a broader line that also holds other things, or a line next to it.')
TASK_V3 = TASK.replace(LINES_V2, LINES_V3)     # the third version (baseline-design.md, round 14): only this sentence differs
LINES_V4 = ('When the report does not state the quantity under the question\'s name, write the lines it is computed from, or the line the report uses '
            'for this same quantity, under the report\'s own names.')
CHECK_V4 = (' Last, read each figure back against the question and keep it only if an analyst reads this question\'s quantity directly off it, or '
            'computes the quantity from it, in the report\'s most recent reported period; drop a line that would first have to be split to give the '
            'quantity, a line next to it, and a figure of any other period.')
TASK_V4 = TASK.replace(LINES_V2, LINES_V4) + CHECK_V4     # the fourth version (round 18): the identity test read back at the end
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['figures'], 'properties': {'figures': {'type': 'array', 'items': {
    'type': 'object', 'additionalProperties': False, 'required': ['quote', 'value', 'unit', 'period', 'basis', 'one_line'],
    'properties': {k: {'type': 'string'} for k in ('quote', 'value', 'unit', 'period', 'basis', 'one_line')}}}}}


def build():
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    items = sqlite3.connect(f'file:{rf.ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    row = items.execute('select input_id, publication_day, publisher, title from items where input_id=?', (RELEASE,)).fetchone()
    text = sqlite3.connect(f'file:{PAGES}?mode=ro', uri=True).execute('select text from items where input_id=?', (RELEASE,)).fetchone()[0]
    views = sqlite3.connect(f'file:{rf.DRAW}/views.sqlite?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    item = {'publication_day': row['publication_day'], 'category': 'T1', 'object_identifiers': [{'value': 'NVDA'}]}
    shown = {v['view_id']: v for v in extraction.shown_views(views, cfg, item, ['NVDA'])}
    requests = {}
    for view_id in QUESTIONS:
        lines = placement.question_lines([shown[view_id]])
        user = (f'[Question]\n' + '\n'.join(lines) + f'\n\n[Report] id {row["input_id"]}, published {row["publication_day"]} by {row["publisher"]}: '
                f'{row["title"]}\n{text}\n\n{TASK}')
        requests[view_id] = model.build_request(cfg.rejudging, SYSTEM, user, SCHEMA, 'extraction', cfg.provider)
    return cfg, text, requests


from hivemind.baseline import comparable, numbers, check_figures  # noqa: E402  (one owner: the product's check, D364)


def kept_figures(data, text):
    """Each figure with the code's identity checks (hivemind.baseline.check_figures)."""
    return check_figures(data.get('figures', []), text)


def main():
    cfg, text, requests = build()
    if sys.argv[1] == 'check':
        for view_id, body in requests.items():
            print(f'{view_id}: request {len(json.dumps(body))} characters, key {model.request_identity(body)[1][:16]}')
        for view_id, body in requests.items():
            user = body['messages'][1]['content']
            print(f'\n----- {view_id}\n' + user[:user.index('[Report]')] + '[…report…]\n' + user[-1000:])
        print('\n----- system\n' + requests['v10']['messages'][0]['content'])
        return
    out = sys.argv[2]
    jobs = [(view_id, n) for view_id in requests for n in range(3)]

    def one(job):
        view_id, n = job
        reply = model.openai_transport(cfg.provider, requests[view_id], timeout=300)
        data = json.loads(reply['choices'][0]['message']['content'])
        usage = reply.get('usage') or {}
        return view_id, n, {'figures': kept_figures(data, text), 'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]}

    results = {view_id: [None] * 3 for view_id in requests}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for view_id, n, r in pool.map(one, jobs):
            results[view_id][n] = r
    json.dump({'requests': {v: model.request_identity(b)[1] for v, b in requests.items()}, 'results': results}, open(out, 'w'), indent=1, ensure_ascii=False)
    for view_id in results:
        for n, r in enumerate(results[view_id]):
            print(f'\n{view_id} send {n} (tokens {r["tokens"]}):')
            for f in r['figures']:
                print(f'   kept {f["kept"]} (in report {f["in_report"]}, labelled {f["labelled"]}, value in quote {f["value_in_quote"]}) | {f["value"]} {f["unit"]} | {f["period"]} | {f["basis"]}\n'
                      f'      quote: {f["quote"][:140]!r}\n      one-line: {f["one_line"][:160]}')


if __name__ == '__main__':
    main()
