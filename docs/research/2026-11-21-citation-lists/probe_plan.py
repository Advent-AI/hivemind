"""$0: the paid acceptance probe's request plan (PROBE-DESIGN.md; D715). Writes probe-plan.json:

- acceptance: the largest stored request of the five archives (most evidence ids), and the sealed D358 run's largest (647 ids; its
  shared evidence enum is under the documented 1,000 values only if a referenced enum counts once);
- refused: the 17 distinct stored refused judge requests (old-1, old-2, old-3, control-1 and linked-1 fresh rows), each with its bad ids;
- matched: for each refused request, the same question's accepted first-attempt request in the same archive whose evidence count is
  closest (ties: the nearest earlier call), never a request of the refused set.

Each entry carries the stored system and user texts, the closed lists read from the text, and a cost estimate from the stored tokens at
the published gpt-6-luna rates.

  python3 probe_plan.py
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(HERE))
from hivemind import model                                              # noqa: E402
from hivemind.views import judging                                     # noqa: E402
import t2_offline                                                       # noqa: E402

PRICE_IN, PRICE_OUT = model.PRICES['gpt-6-luna']


def view_of(user):
    match = re.match(r'Thesis (v\d+) \(', user)
    return match.group(1) if match else None


def cost(tokens_in, tokens_out):
    return round((tokens_in or 0) / 1e6 * PRICE_IN + (tokens_out or 0) / 1e6 * PRICE_OUT, 6)


def entry(label, call_id, request, tokens_in, tokens_out, answer_json=None):
    user = request['messages'][1]['content'].split(t2_offline.RETRY_MARK, 1)[0]
    lists = t2_offline.lists_from_text(user)
    return {'source': label, 'call_id': call_id, 'view': view_of(user), 'system': request['messages'][0]['content'], 'user': user,
            'lists': lists, 'evidence count': len(lists['evidence']), 'stored answer': answer_json,
            'estimated cost': cost(tokens_in, tokens_out), 'stored tokens': [tokens_in, tokens_out]}


def main():
    refused, accepted_by_source, largest = [], {}, None
    seen = set()
    for label, folder, top in t2_offline.SOURCES:
        archive = sqlite3.connect(f'file:{folder / "archive.sqlite"}?mode=ro', uri=True)
        views = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
        committed = {r[0] for r in views.execute('select call_id from judgements')}
        for call_id, sha, request_json, answer_json, tokens_in, tokens_out in archive.execute(
                "select call_id, request_sha256, request_json, answer_json, input_tokens, output_tokens from model_calls "
                "where purpose='judge' and call_id>? order by call_id", (top,)):
            request = json.loads(request_json)
            pair = (sha.split(':')[0], answer_json)
            if pair in seen:
                continue
            seen.add(pair)
            item = entry(label, call_id, request, tokens_in, tokens_out, answer_json)
            if largest is None or item['evidence count'] > largest['evidence count']:
                largest = item
            if ':refused:' in sha:
                schema = judging.schema_for('judging-v12', item['lists'])
                item['bad ids'] = sorted({re.search(r"'([^']+)' not in", e).group(1) for e in model.check_schema(json.loads(answer_json), schema)
                                          if "' not in" in e})
                refused.append(item)
            elif call_id in committed and t2_offline.RETRY_MARK not in request['messages'][1]['content']:
                accepted_by_source.setdefault(label, []).append(item)
    distinct = {}
    for item in refused:                           # a retry carries its first request's text: one request, the bad ids of both attempts
        key = (item['source'], item['user'])
        if key in distinct:
            distinct[key]['bad ids'] = sorted(set(distinct[key]['bad ids']) | set(item['bad ids']))
            distinct[key]['refused calls'].append(item['call_id'])
        else:
            distinct[key] = dict(item, **{'refused calls': [item['call_id']]})
    refused = list(distinct.values())
    refused_users = set(distinct)
    matched = []
    for item in refused:
        pool = [a for a in accepted_by_source.get(item['source'], []) if a['view'] == item['view'] and (a['source'], a['user']) not in refused_users]
        if not pool:
            raise SystemExit(f'{item["source"]} {item["call_id"]}: no accepted request of {item["view"]} to match')
        best = min(pool, key=lambda a: (abs(a['evidence count'] - item['evidence count']), abs(a['call_id'] - item['call_id'])))
        if any((m['source'], m['view']) == (item['source'], item['view']) for m in matched):
            continue                               # one comparison per (source, question): PROBE-DESIGN v2 §2, to fit the ceiling
        matched.append(dict(best, matches=f'{item["source"]}:{item["call_id"]}'))
    matched.sort(key=lambda m: m['estimated cost'])                      # cheapest first
    sealed = sqlite3.connect(f'file:{t2_offline.SEALED}?mode=ro', uri=True)
    sealed_largest = None
    for call_id, request_json, tokens_in, tokens_out in sealed.execute("select call_id, request_json, input_tokens, output_tokens from model_calls where purpose='judge'"):
        item = entry('sealed-D358', call_id, json.loads(request_json), tokens_in, tokens_out)
        if sealed_largest is None or item['evidence count'] > sealed_largest['evidence count']:
            sealed_largest = item
    old3 = sqlite3.connect(f'file:{dict((l, f) for l, f, _ in t2_offline.SOURCES)["old-3"] / "archive.sqlite"}?mode=ro', uri=True)
    request_json, tokens_in, tokens_out = old3.execute('select request_json, input_tokens, output_tokens from model_calls where call_id=69').fetchone()
    empty_themes = entry('old-3', 69, json.loads(request_json), tokens_in, tokens_out)
    if empty_themes['lists']['themes']:
        raise SystemExit('old-3 call 69 is expected to carry no theme')
    plan = {'acceptance': [largest, empty_themes, sealed_largest], 'acceptance names': ['A1', 'A0', 'A2'], 'refused': refused, 'matched': matched}
    sends = {'acceptance': 1, 'refused': 3, 'matched under v12': 3, 'matched under v7 (control)': 3}
    estimate = (sum(a['estimated cost'] for a in plan['acceptance']) + 3 * sum(r['estimated cost'] for r in refused)
                + 6 * sum(m['estimated cost'] for m in matched))
    plan['sends'], plan['estimate'] = sends, round(estimate, 4)
    (HERE / 'probe-plan.json').write_text(json.dumps(plan, ensure_ascii=False))
    print(json.dumps({'acceptance': [(a['source'], a['call_id'], a['evidence count'], a['estimated cost']) for a in plan['acceptance']],
                      'refused': [(r['source'], r['call_id'], r['view'], r['evidence count'], r['bad ids']) for r in refused],
                      'matched': [(m['source'], m['call_id'], m['view'], m['evidence count'], m['matches']) for m in matched],
                      'sends': sends, 'estimate (stored tokens, published rates)': plan['estimate']}, indent=1))


if __name__ == '__main__':
    main()
