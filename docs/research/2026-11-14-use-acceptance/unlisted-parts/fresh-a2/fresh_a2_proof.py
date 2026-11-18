"""$0 proofs before FRESH-A2-DESIGN.md v4's paid run (D587). No model call: requests are rebuilt through the real run loop with a
recorded answer.

  python3 fresh_a2_proof.py <new scratch folder> [--write-inputs]

  F1  the week of 2026-10-13..19 through both systems' entries: the same items in the same order, equal to today's exposure census;
  F2  the starting library is the week of 10-06's completed state: every article complete, the first read from empty, the window
      ending before the test week; its topics listed;
  F3  today's run loop rebuilds stored 10-06 requests byte for byte from their stored libraries (the entry is unchanged);
  F4  for the test week's first articles, the request from the carried library differs from an empty-start one only in the open
      questions shown, and those are the library's;
  F5  the settings and system text are the stored run's;
  F6  an incomplete run is reported as incomplete, with only completed articles' topics (a truncated copy of the stored trace);
  F7  the cost estimate from the 10-06 week's ledger, and the reader workload by population size.
FRESH_MUTANT=dropped-thesis | truncated-not-flagged must each fail.
"""
import json
import os
import shutil
import sqlite3
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(ROOT / 'src'), str(ROOT / 'clean-arch/step1'), str(ROOT / 'docs/research/2026-11-14-use-acceptance')]
import fresh_a2  # noqa: E402
import runner  # noqa: E402

ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
PRD = ROOT / 'clean-arch/PRD.md'
OCTOBER = ROOT / 'poc/data/clean-second-week-2026-11-15/week-continued'
CENSUS = HERE.parent / 'fresh-exposure-2026-11-16/exposure-census.json'
SHOWN = ('id', 'description', 'outcome', 'period')
MUTANT = os.environ.get('FRESH_MUTANT', '')


class Failed(Exception):
    pass


def expect(condition, message):
    if not condition:
        raise Failed(message)


def rebuild(scratch, name, run, input_id, initial, raw_response, manifest_base=None):
    output = Path(scratch) / f'{name}.sqlite'
    manifest = dict(manifest_base or run['manifest'], item_ids=[input_id], item_limit=1)
    settings = {key: value for key, value in run['settings'].items() if key != 'live_limits'}
    try:
        runner.run(ITEMS, output, manifest, initial, settings, runner.RecordedTransport([json.loads(raw_response)]), PRD)
    except Exception:                                   # a recorded answer may not fit: the request is stored before it is read
        pass
    _, rows = fresh_a2.read_trace(output)
    expect(len(rows) == 1 and rows[0]['input_id'] == input_id, 'the rebuilt run did not read the one article')
    return rows[0]


def main(scratch, write_inputs=False):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=False)
    import fresh_week_inputs as week
    week.FROM, week.UNTIL = '2026-10-13', '2026-10-19'
    production = week.production_list()
    manifest = {'entity': 'NVDA', 'from_day': week.FROM, 'until_day': week.UNTIL, 'item_limit': len(production), 'item_ids': production}
    clean = [item['input_id'] for item in runner.selected_items(ITEMS, manifest)]
    census = json.loads(CENSUS.read_text())['weeks']['2026-10-13..2026-10-19']['articles_in_order']
    expect(clean == production == census, f'the entries or the census differ: production {len(production)}, clean {len(clean)}, census {len(census)}')
    print(f'F1 ok: {len(production)} items, the same set and order through both entries and today\'s census')

    run, rows = fresh_a2.read_trace(OCTOBER / 'merged-step1.sqlite')
    expect(len(rows) == len(run['manifest']['item_ids']) == 272 and all(row['status'] == 'complete' for row in rows), 'the 10-06 run is not complete')
    expect(json.loads(rows[0]['before_state']) == [] and run['initial_theses'] == [], 'the 10-06 run did not start from empty')
    expect(run['manifest']['until_day'] < '2026-10-13', 'the 10-06 window does not end before the test week')
    library = json.loads(rows[-1]['after_state'])
    if MUTANT == 'dropped-thesis':
        library = library[:-1]
    cases = [case['thesis'] for case in json.loads((OCTOBER / 'c1/cases/cases.json').read_text())]
    topics, complete, done, total = fresh_a2.opened_topics(OCTOBER / 'merged-step1.sqlite')
    expect([thesis['id'] for thesis in library] == [topic['thesis']['id'] for topic in topics], 'the library is not the run\'s opened topics in order')
    expect(sorted(thesis['id'] for thesis in library) == sorted(case['id'] for case in cases), 'the library is not the week\'s cases')
    print(f'F2 ok: the 10-06 week\'s completed state: {len(rows)} articles complete from empty, window to {run["manifest"]["until_day"]}, '
          f'{len(library)} topics, equal to its {len(cases)} cases')

    for row in (rows[0], rows[len(rows) // 2], rows[-1]):
        again = rebuild(scratch, f'as-stored-{row["sequence"]}', run, row['input_id'], json.loads(row['before_state']), row['raw_response'])
        expect(again['request'] == row['request'], f'sequence {row["sequence"]}: the rebuilt request is not the stored one')
    print('F3 ok: 3 of 3 stored 10-06 requests (first, middle, last) rebuilt byte for byte from their stored libraries')

    base = {key: value for key, value in run['manifest'].items() if key not in ('item_ids', 'item_limit')}
    base.update(from_day=week.FROM, until_day=week.UNTIL)
    shown = [{key: thesis[key] for key in SHOWN} for thesis in library]
    for input_id in production[:3]:
        pair = {name: json.loads(rebuild(scratch, f'{name}-{input_id.replace(":", "_")}', run, input_id, initial, rows[0]['raw_response'], base)['request'])
                for name, initial in (('empty', []), ('carried', library))}
        payloads = {}
        for name, request in pair.items():
            payload, end = json.JSONDecoder().raw_decode(request['messages'][1]['content'])
            payloads[name] = (payload, request['messages'][1]['content'][end:])
        expect(payloads['empty'][0]['open_theses'] == [] and payloads['carried'][0]['open_theses'] == shown, f'{input_id}: the open questions shown are not the library\'s')
        for name in pair:
            payloads[name][0]['open_theses'] = None
            pair[name]['messages'][1]['content'] = None
        expect(payloads['empty'] == payloads['carried'] and pair['empty'] == pair['carried'], f'{input_id}: the two requests differ beyond the open questions')
    print(f'F4 ok: 3 of 3 test-week request pairs differ only in the open questions shown ({len(shown)} carried, 0 empty)')

    system = json.loads(rows[0]['request'])['messages'][0]['content']
    expect(all(json.loads(row['request'])['messages'][0]['content'] == system for row in rows), 'the stored run used more than one system text')
    print(f'F5 ok: one system text ({len(system)} characters) across the 272 stored requests; F3 shows today\'s build equals it; settings '
          f'{ {key: value for key, value in run["settings"].items() if key != "live_limits"} }')

    truncated = scratch / 'truncated.sqlite'
    shutil.copy(OCTOBER / 'merged-step1.sqlite', truncated)
    connection = sqlite3.connect(truncated)
    connection.execute('delete from trace where sequence > (select min(sequence) + 99 from trace)')
    connection.commit()
    connection.close()
    cut_topics, cut_complete, cut_done, cut_total = fresh_a2.opened_topics(truncated)
    if MUTANT == 'truncated-not-flagged':
        cut_complete = True
    expect(not cut_complete and cut_done == 100 and cut_total == 272 and all(topic['sequence'] <= rows[99]['sequence'] for topic in cut_topics),
           'a truncated run is not reported as incomplete with only its completed articles\' topics')
    print(f'F6 ok: a run cut after 100 of 272 articles reads as incomplete, with {len(cut_topics)} topics from its completed articles (no verdict)')

    attempts = [json.loads(line) for line in (OCTOBER / 'ledger.attempts.jsonl').read_text().splitlines()]
    lost = [a for a in attempts if a['charged'] >= 0.9 * a['reserved']]
    normal = [a['charged'] for a in attempts if a not in lost]
    per_article = sum(normal) / 152
    print(f'F7: the 10-06 continuation (152 articles, from the library left at article 121): {len(attempts)} attempts, ${sum(a["charged"] for a in attempts):.4f}; '
          f'{len(lost)} charged at their reservation (cut), ${sum(a["charged"] for a in lost):.4f}; the rest ${per_article:.4f} an article; '
          f'reservation median ${statistics.median(a["reserved"] for a in attempts):.4f}')
    print(f'    383 articles: ${383 * per_article:.2f} with no cut attempt; ${383 * per_article + len(lost) / 152 * 383 * statistics.median(a["charged"] for a in lost):.2f} '
          f'at the 10-06 cut rate; the ceiling must also hold the reservations in flight')
    for n in (5, 10, 15):
        print(f'    readers for n = {n} topics: {n * 6 + 3} items to read a family ({-(-(n * 6 + 3) // 22)} packets of 22), as A2\'s probe needed '
              f'third readers on about 2 in 3 sends')
    if write_inputs:
        inputs = HERE / 'inputs'
        inputs.mkdir(exist_ok=False)
        (inputs / 'manifest-2026-10-13-10-19.json').write_text(json.dumps(manifest, indent=1) + '\n')
        (inputs / 'initial-10-06-library.json').write_text(json.dumps(library, ensure_ascii=False, indent=1) + '\n')
        (inputs / 'settings.json').write_text(json.dumps({key: value for key, value in run['settings'].items() if key != 'live_limits'}, indent=1) + '\n')
        print('inputs written to', inputs)
    print('ALL OK')


if __name__ == '__main__':
    try:
        main(sys.argv[1], '--write-inputs' in sys.argv[2:])
    except Failed as failure:
        print('FAILED:', failure)
        sys.exit(1)
