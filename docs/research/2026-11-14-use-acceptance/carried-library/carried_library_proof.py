"""$0 proofs before the small comparison of D559: the first step reads the week of 10-06's opening articles once from the
week of 09-22's own library and once from empty. No model call: every request is rebuilt through the real run loop with a
recorded answer.

  python3 carried_library_proof.py <scratch folder> [--write-inputs <folder>]

What it proves, each with the count it judged:
  E1  the carried starting library is the September run's completed state (every article complete, started from empty, the
      state after the last article), equal to that run's seven topics, dated before the test week;
  E2  the articles are the distinct opening articles of the October week's thirteen topics, in the order they were read;
  E3  the real run loop, given an article's stored library, rebuilds the stored request byte for byte and the same library after;
  E4  an empty-start request equals a stored one as built (the October run's first article);
  E5  for each article the carried request differs from the empty one only in the open questions shown, and those are the
      September state's;
  E6  the first step's settings and system text are the same in both stored runs and now.
CARRIED_MUTANT=dropped-thesis | other-article must each fail.
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'clean-arch/step1'))
import runner  # noqa: E402

ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEPTEMBER = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1'
OCTOBER = ROOT / 'poc/data/clean-second-week-2026-11-15/week-continued'
OCTOBER_TRACE = OCTOBER / 'merged-step1.sqlite'
PRD = ROOT / 'clean-arch/PRD.md'
SHOWN = ('id', 'description', 'outcome', 'period')
MUTANT = os.environ.get('CARRIED_MUTANT', '')


class Failed(Exception):
    pass


def expect(condition, message):
    if not condition:
        raise Failed(message)


def read_trace(path):
    connection = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        run = connection.execute('select * from run').fetchone()
        rows = [dict(row) for row in connection.execute('select * from trace order by sequence')]
        return {name: json.loads(run[name]) for name in ('manifest', 'settings', 'source_items', 'initial_theses')}, rows
    finally:
        connection.close()


def september_state():
    run, rows = read_trace(SEPTEMBER / 'step1/trace.sqlite')
    expect(run['initial_theses'] == [], 'the September run did not start from empty')
    expect(len(rows) == len(run['manifest']['item_ids']) and all(row['status'] == 'complete' for row in rows), 'the September run is not complete')
    state = json.loads(rows[-1]['after_state'])
    if MUTANT == 'dropped-thesis':
        state = state[:-1]
    topics = [case['thesis'] for case in json.loads((SEPTEMBER / 'cases/cases.json').read_text())]
    expect([tuple(thesis[key] for key in SHOWN) for thesis in state] == [tuple(topic[key] for key in SHOWN) for topic in topics],
           'the carried state is not the September run\'s topics')
    expect(all(thesis['entity'] == 'NVDA' for thesis in state), 'a carried thesis is not the company\'s')
    expect(run['manifest']['until_day'] < '2026-10-06', 'the September window does not end before the test week')
    return run, rows, state


def october_articles():
    run, rows = read_trace(OCTOBER_TRACE)
    by_sequence = {row['sequence']: row for row in rows}
    cases = json.loads((OCTOBER / 'c1/cases/cases.json').read_text())
    items = {item['input_id']: item for item in run['source_items']}
    opened = {}
    for case in cases:
        thesis = case['thesis']['id']
        first = next(row for row in rows if any(t['id'] == thesis for t in json.loads(row['after_state'] or '[]'))
                     and not any(t['id'] == thesis for t in json.loads(row['before_state'])))
        item = items[first['input_id']]
        expect(item['title'] == case['item']['title'] and item['publication_day'] == case['item']['publication_date'] and item['text'] == case['item']['text'],
               f'the article of {thesis} is not the case\'s')
        opened.setdefault(first['sequence'], []).append(thesis)
    sequences = sorted(opened)
    if MUTANT == 'other-article':
        sequences[0] = next(sequence for sequence in by_sequence if sequence not in opened)
    expect(sum(len(opened.get(sequence, [])) for sequence in sequences) == len(cases) == 13, 'the articles do not open the week\'s thirteen topics')
    return run, rows, [{'sequence': sequence, 'input_id': by_sequence[sequence]['input_id'], 'title': items[by_sequence[sequence]['input_id']]['title'],
                        'publication_day': items[by_sequence[sequence]['input_id']]['publication_day'], 'opened': opened.get(sequence, [])} for sequence in sequences]


def rebuild(scratch, name, run, input_id, initial, raw_response):
    """One article through the real run loop with a recorded answer; returns the stored row (request as built, library after)."""
    output = Path(scratch) / f'{name}.sqlite'
    manifest = dict(run['manifest'], item_ids=[input_id], item_limit=1)
    settings = {key: value for key, value in run['settings'].items() if key != 'live_limits'}
    try:
        runner.run(ITEMS, output, manifest, initial, settings, runner.RecordedTransport([json.loads(raw_response)]), PRD)
    except Exception:                                   # the recorded answer may not fit another library: the request is stored before the answer is read
        pass
    _, rows = read_trace(output)
    expect(len(rows) == 1 and rows[0]['input_id'] == input_id, 'the rebuilt run did not read the one article')
    return rows[0]


def main(scratch, inputs=None):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=False)
    september_run, september_rows, carried = september_state()
    print(f'E1 ok: the carried library is the September run\'s completed state: {len(september_rows)} articles complete from empty, {len(carried)} topics, window to {september_run["manifest"]["until_day"]}')
    october_run, october_rows, articles = october_articles()
    print(f'E2 ok: {len(articles)} distinct opening articles for {sum(len(a["opened"]) for a in articles)} topics, sequences {[a["sequence"] for a in articles]}')
    by_sequence = {row['sequence']: row for row in october_rows}
    for article in articles:
        stored = by_sequence[article['sequence']]
        again = rebuild(scratch, f'as-stored-{article["sequence"]}', october_run, article['input_id'], json.loads(stored['before_state']), stored['raw_response'])
        expect(again['request'] == stored['request'], f'sequence {article["sequence"]}: the rebuilt request is not the stored one')
        expect(again['status'] == 'complete' and json.loads(again['after_state']) == json.loads(stored['after_state']), f'sequence {article["sequence"]}: the library after differs')
    print(f'E3 ok: {len(articles)} of {len(articles)} requests rebuilt byte for byte through the run loop from the stored library, same library after')
    first = october_rows[0]
    expect(json.loads(first['before_state']) == [], 'the October run\'s first article was not read from empty')
    again = rebuild(scratch, 'empty-as-stored', october_run, first['input_id'], [], first['raw_response'])
    expect(again['request'] == first['request'], 'the empty-start request is not the stored one')
    print('E4 ok: an empty-start request rebuilt through the run loop equals the stored request of the October run\'s first article (1 judged)')
    shown = [{key: thesis[key] for key in SHOWN} for thesis in carried]
    for article in articles:
        stored = by_sequence[article['sequence']]
        pair = {}
        for name, initial in (('empty', []), ('carried', carried)):
            row = rebuild(scratch, f'{name}-{article["sequence"]}', october_run, article['input_id'], initial, stored['raw_response'])
            pair[name] = json.loads(row['request'])
        payloads = {}
        for name, request in pair.items():
            payload, end = json.JSONDecoder().raw_decode(request['messages'][1]['content'])
            payloads[name] = (payload, request['messages'][1]['content'][end:])
        expect(payloads['empty'][0]['open_theses'] == [] and payloads['carried'][0]['open_theses'] == shown, f'sequence {article["sequence"]}: the open questions shown are not the intended ones')
        for name in pair:
            payloads[name][0]['open_theses'] = None
            pair[name]['messages'][1]['content'] = None
        expect(payloads['empty'] == payloads['carried'] and pair['empty'] == pair['carried'], f'sequence {article["sequence"]}: the two requests differ beyond the open questions')
    print(f'E5 ok: {len(articles)} of {len(articles)} request pairs differ only in the open questions shown ({len(shown)} carried, 0 empty)')
    strip = lambda settings: {key: value for key, value in settings.items() if key != 'live_limits'}
    expect(strip(september_run['settings']) == strip(october_run['settings']), 'the two stored runs used different settings')
    system = lambda rows: json.loads(rows[0]['request'])['messages'][0]['content']
    expect(system(september_rows) == system(october_rows), 'the two stored runs used different system texts')
    print(f'E6 ok: the same settings {strip(october_run["settings"])} and system text ({len(system(october_rows))} characters) in both stored runs; E3 shows today\'s build equals them')
    if inputs:
        inputs = Path(inputs)
        inputs.mkdir(parents=True, exist_ok=True)
        (inputs / 'initial-carried.json').write_text(json.dumps(carried, ensure_ascii=False, indent=1) + '\n')
        (inputs / 'initial-empty.json').write_text('[]\n')
        (inputs / 'articles.json').write_text(json.dumps(articles, ensure_ascii=False, indent=1) + '\n')
        (inputs / 'settings.json').write_text(json.dumps(strip(october_run['settings']), indent=1) + '\n')
        (inputs / 'manifest-base.json').write_text(json.dumps({key: value for key, value in october_run['manifest'].items() if key not in ('item_ids', 'item_limit')}, indent=1) + '\n')
        print('inputs written to', inputs)
    print('ALL OK')


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--write-inputs' else None)
    except Failed as failure:
        print('FAILED:', failure)
        sys.exit(1)
