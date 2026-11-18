"""An isolated same-day visibility probe on stored articles (design: VISIBILITY-PROBE-DESIGN.md; D522). Dry by default.

For each case the production code builds two reading requests for one stored article of the old system's fresh-week run: the control,
from the questions open at the day's start (it must have the stored archive key), and the changed one, from the questions committed
before the article (the store read at the article's sequence minus one). Prompt, schema, model and settings are the frozen reading
step's; only the list of questions differs. Every answer goes through the production checks and filing (`sift_with_groups`,
`file_reading`) on its own arm's list. One HTTP attempt a call; every reply is saved before it is read; cost at the published rates.

  python3 visibility_probe.py <output folder>                      (dry: rebuilds, checks, sizes the cost; sends nothing)
  python3 visibility_probe.py <output folder> --send --max-usd <ceiling>
"""
import concurrent.futures
import copy
import json
import sqlite3
import sys
import time
import types
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
SENDS = 3
# scored cases: the article that opened the second question of a pair both reviewing teams called duplicates (earlier, later)
# separate controls: an article that opened a question on another matter than the questions committed earlier that day (its questions)
CASES = [{'case': 'rtx', 'role': 'scored', 'earlier': 'v14', 'opened': ['v15']},
         {'case': 'rubin', 'role': 'scored', 'earlier': 'v9', 'opened': ['v11']},
         {'case': 'fy2028', 'role': 'scored', 'earlier': 'v3', 'opened': ['v5']},
         {'case': 'control-revenue', 'role': 'separate', 'earlier': None, 'opened': ['v2', 'v3']},
         {'case': 'control-margin', 'role': 'separate', 'earlier': None, 'opened': ['v10']}]


def main():
    output = Path(sys.argv[1])
    max_usd = float(sys.argv[sys.argv.index('--max-usd') + 1]) if '--max-usd' in sys.argv else 0.0
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    items_db = testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    conn = store.open_read_only(str(RUN / 'views.sqlite'))
    archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    prepared, worst = [], 0.0
    for case in CASES:
        rows = [conn.execute('select created_from_input, created_seq, question from views where view_id = ?', (view,)).fetchone() for view in case['opened']]
        if len({row['created_from_input'] for row in rows}) != 1:
            raise SystemExit(f"{case['case']}: its questions were not opened by one article: refused")
        input_id, item_seq = rows[0]['created_from_input'], rows[0]['created_seq']
        day = conn.execute('select publication_day from processing_steps where input_id = ? limit 1', (input_id,)).fetchone()[0]
        item = next((i for i in testdb.feed(items_db, day, day) if i['input_id'] == input_id), None)
        if item is None:
            raise SystemExit(f"{case['case']}: the article is not in the article database: refused")
        objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
        stored_sha, stored_answer = archive.execute("select request_sha256, answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{input_id}%',)).fetchone()
        lists, requests = {}, {}
        lists['control'] = extraction.shown_views(conn, cfg, item, objects)
        original = store.day_start_seq
        store.day_start_seq = lambda connection, publication_day: item_seq - 1
        try:
            lists['changed'] = extraction.shown_views(conn, cfg, item, objects)
        finally:
            store.day_start_seq = original
        for arm in ('control', 'changed'):
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], lists[arm], uni)
            requests[arm] = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
        if model.request_identity(requests['control'])[1] != stored_sha:
            raise SystemExit(f"{case['case']}: the control built by the production code is not the stored request: refused")
        added = [v['view_id'] for v in lists['changed'] if v['view_id'] not in {w['view_id'] for w in lists['control']}]
        if case['earlier'] and case['earlier'] not in added:
            raise SystemExit(f"{case['case']}: the earlier question {case['earlier']} is not among the questions committed before the article: refused")
        if not added:
            raise SystemExit(f"{case['case']}: no question was committed earlier that day: nothing to test")
        stored = json.loads(stored_answer)
        wording = [row['question'] for row in rows]
        targets = [c['id'] for c in stored.get('candidates') or [] if c.get('question') in wording]
        # the statements the stored answer filed under the question(s) it opened: the source-backed statements of this case, fixed before any send
        marked = [{'stored_id': s['id'], 'quote': s['quote']} for s in stored['evidence'] if set(targets) & (set(s.get('links') or []))]
        marked += [{'stored_id': s['id'], 'quote': s['quote']} for s in stored['evidence'] if s['id'] in {i for c in stored.get('candidates') or [] if c['id'] in targets for i in c.get('evidence_ids') or []}
                   and s['id'] not in {m['stored_id'] for m in marked}]
        price_in, price_out = model.PRICES[setting.model]
        for arm in ('control', 'changed'):
            characters = sum(len(m['content']) for m in requests[arm]['messages']) + len(json.dumps(schema))
            worst += SENDS * (characters / 2.5 / 1e6 * price_in + setting.max_output_tokens / 1e6 * price_out)
        prepared.append({'case': case['case'], 'role': case['role'], 'earlier': case['earlier'], 'opened': case['opened'], 'opened_wording': wording, 'article': input_id,
                         'article_seq': item_seq, 'day': day, 'added_to_the_list': added, 'statements': marked, 'requests': requests, 'lists': lists, 'item': item,
                         'setting': setting, 'schema': schema})
        print(f"{case['case']} ({case['role']}): article {item_seq} of {day}; control has the stored key; questions listed {len(lists['control'])} -> {len(lists['changed'])} (added {added}); "
              f"request {len(requests['control']['messages'][1]['content'])} -> {len(requests['changed']['messages'][1]['content'])} characters; stored answer opened {case['opened']} with {len(marked)} statements under them")
    setting = prepared[0]['setting']
    print(f"\nmodel {setting.model}, effort {setting.reasoning_effort}, output allowance {setting.max_output_tokens}; {len(prepared) * 2 * SENDS} calls, one HTTP attempt each; "
          f"cost if every call used its whole output allowance: ${worst:.3f}")
    if '--send' not in sys.argv:
        (Path(__file__).resolve().parent / 'changed-request-rtx.txt').write_text(next(p for p in prepared if p['case'] == 'rtx')['requests']['changed']['messages'][1]['content'])
        print('dry: nothing sent (the changed request of the rtx case is written beside this script for review)')
        return
    if worst > max_usd:
        raise SystemExit(f'the worst case ${worst:.3f} is above the ceiling ${max_usd}: refused')
    if output.exists():
        raise SystemExit(f'{output} exists: refusing to write over it')
    output.mkdir(parents=True)
    price_in, price_out = model.PRICES[setting.model]

    def send(job):
        entry, arm, number = job
        started = time.time()
        record = {'case': entry['case'], 'role': entry['role'], 'arm': arm, 'send': number}
        try:
            reply = model.openai_transport(cfg.provider, entry['requests'][arm], max_attempts=1)
        except Exception as error:  # a transport failure is a recorded attempt, not a lost one
            record.update(error=repr(error)[:400], usd_at_published_rates=0.0)
            (output / f"reply-{entry['case']}-{arm}-{number}.json").write_text(json.dumps(record, indent=1))
            return record
        (output / f"reply-{entry['case']}-{arm}-{number}.json").write_text(json.dumps(reply, ensure_ascii=False, indent=1))
        usage = reply.get('usage') or {}
        tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
        cached = min(tokens_in, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
        record.update(input_tokens=tokens_in, cached_tokens=cached, output_tokens=tokens_out, seconds=round(time.time() - started, 1),
                      usd_at_published_rates=round((tokens_in - cached) / 1e6 * price_in + cached / 1e6 * price_in * model.CACHED_INPUT_SHARE + tokens_out / 1e6 * price_out, 6))
        try:
            data = json.loads(reply['choices'][0]['message']['content'])
            errors = model.check_schema(data, entry['schema'])
            if errors:
                raise ValueError('; '.join(errors)[:300])
            shown = entry['lists'][arm]
            evidence, candidates, dropped, new_groups = extraction.sift_with_groups(copy.deepcopy(data), entry['item'], entry['item']['text'], {v['view_id'] for v in shown}, uni)
            handle = types.SimpleNamespace(data=data, call_id=0, request_sha256='', cached=False, cost_usd=0.0)
            handover = extraction.file_reading(extraction.Reading(evidence, candidates, dropped, new_groups, handle, 'x'), entry['item'], shown)
            record.update(answer=data, kept=[{'id': e['id'], 'links': e['links'], 'quote': e['quote'], 'one_line': e.get('one_line')} for e in handover.evidence],
                          candidates=[{'id': c['id'], 'question': c.get('question'), 'evidence_ids': c.get('evidence_ids')} for c in handover.candidates],
                          dropped=[list(d) for d in handover.dropped])
        except Exception as error:  # an answer that cannot be read or checked is recorded as such
            record['error'] = f'{type(error).__name__}: {error}'[:400]
        return record

    jobs = [(entry, arm, number) for entry in prepared for arm in ('control', 'changed') for number in range(1, SENDS + 1)]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        records = [future.result() for future in [pool.submit(send, job) for job in jobs]]
    cases = [{key: entry[key] for key in ('case', 'role', 'earlier', 'opened', 'opened_wording', 'article', 'article_seq', 'day', 'added_to_the_list', 'statements')} for entry in prepared]
    (output / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=1))
    (output / 'requests.json').write_text(json.dumps({entry['case']: entry['requests'] for entry in prepared}, ensure_ascii=False, indent=1))
    (output / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    spent = sum(record.get('usd_at_published_rates') or 0 for record in records)
    (output / 'spend.json').write_text(json.dumps({'calls': len(records), 'usd_at_published_rates': round(spent, 6), 'ceiling_usd': max_usd}, indent=1))
    print(f"sent {len(records)} calls; answers read and checked {sum(1 for r in records if 'kept' in r)}; ${spent:.4f} at the published rates")


if __name__ == '__main__':
    main()
