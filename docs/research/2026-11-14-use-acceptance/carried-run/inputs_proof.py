"""The two-week run's inputs, proved at $0 (D563, step 3). Registered expectations; a non-zero exit when one fails.

  1. The second week's manifest is the production entry's articles for 2026-09-29..10-05 in its order, less the three the Step 1
     tuning runs sent, every one in the frozen never-sent list; the clean runner's own selection accepts it; the text of every
     article is identified by its sha256 (written beside the manifest).
  2. The inputs `extension.py` writes from the stored week of 09-22: the starting library is that run's last library, the
     settings are its own; the request the run loop builds for the second week's first article from them holds exactly that
     library as its open questions and the article's own fields, and differs from the request built from an empty library
     only in the open questions.
  3. The date check of `extension_proof.py` judges something: on a request holding a statement first read after its day it
     reports the statement; on the stored requests it reports none.

  python3 inputs_proof.py <scratch folder>
"""
import hashlib
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
USE = HERE.parent
STORED = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1'
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
MANIFEST = HERE / 'manifest-2026-09-29-10-05.json'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1'), str(HERE)]
import extension  # noqa: E402
import runner  # noqa: E402

EXPECTATIONS = []


def expect(name, holds, detail=''):
    EXPECTATIONS.append((name, bool(holds)))
    print(('  ok    ' if holds else '  FAIL  ') + name + (f' | {detail}' if detail else ''))


def request_for(folder, initial, scratch, name):
    manifest = json.loads((folder / 'manifest.json').read_text())
    settings = json.loads((folder / 'settings.json').read_text())
    output = scratch / f'{name}.sqlite'
    try:
        runner.run(ITEMS, output, dict(manifest, item_ids=manifest['item_ids'][:1], item_limit=1), initial, settings,
                   runner.RecordedTransport([{'choices': [{'message': {'content': '{}'}, 'finish_reason': 'stop'}]}]), ROOT / 'clean-arch/PRD.md')
    except Exception:                                   # the made-up answer fails the checks; the request is stored before it is read
        pass
    conn = sqlite3.connect(f'file:{output}?mode=ro', uri=True)
    request = json.loads(conn.execute('select request from trace where sequence = 1').fetchone()[0])
    conn.close()
    return request


def main(scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=False)
    print('1. the second week\'s articles')
    spec = importlib.util.spec_from_file_location('fresh_week_inputs', USE / 'fresh_week_inputs.py')
    week_inputs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(week_inputs)
    week_inputs.FROM, week_inputs.UNTIL = '2026-09-29', '2026-10-05'
    production = week_inputs.production_list()
    note = json.loads((HERE / 'manifest-note.json').read_text())
    manifest = json.loads(MANIFEST.read_text())
    fresh = {row['input_id'] for row in json.loads((USE / 'fresh-articles-2026-09-22-10-05.json').read_text())['fresh']}
    expect("the manifest is the production entry's articles in its order, less the three sent before",
           manifest['item_ids'] == [i for i in production if i not in note['dropped_as_sent_before']] and len(note['dropped_as_sent_before']) == 3,
           f"{len(manifest['item_ids'])} of {len(production)}")
    expect('every article is in the frozen never-sent list', all(i in fresh for i in manifest['item_ids']))
    items = runner.selected_items(ITEMS, manifest)
    expect("the clean runner's selection accepts it, in the same order", [item['input_id'] for item in items] == manifest['item_ids'])
    days = [item['publication_day'] for item in items]
    expect('the days run from 2026-09-29 to 2026-10-05 without going back', days == sorted(days) and days[0] >= '2026-09-29' and days[-1] <= '2026-10-05',
           f'{days[0]} .. {days[-1]}')
    identities = {item['input_id']: hashlib.sha256((item['text'] or '').encode()).hexdigest() for item in items}
    (HERE / 'manifest-2026-09-29-10-05.text-sha256.json').write_text(json.dumps(identities, indent=1) + '\n')
    print('   text identities written:', len(identities))

    print('2. the inputs from the stored week of 09-22')
    folder = scratch / 'second'
    extension.write_inputs(STORED / 'step1', MANIFEST, folder, json.loads((STORED / 'step1/limits.json').read_text()))
    stored = extension.read_part(STORED / 'step1/trace.sqlite')
    library = json.loads((folder / 'initial.json').read_text())
    expect("the starting library is the stored week's last library", library == json.loads(stored['rows'][-1]['after_state']),
           f"{len(library)} topics: {[t['id'] for t in library]}")
    expect("the settings are the stored week's own", json.loads((folder / 'settings.json').read_text())
           == {k: v for k, v in stored['settings'].items() if k != 'live_limits'})
    carried = request_for(folder, library, scratch, 'carried')
    empty = request_for(folder, [], scratch, 'empty')
    payload, end = json.JSONDecoder().raw_decode(carried['messages'][1]['content'])
    shown = [{key: topic[key] for key in ('id', 'description', 'outcome', 'period')} for topic in library]
    item = items[0]
    expect("the first article's request holds the starting library as its open questions", payload['open_theses'] == shown)
    expect("…and the article's own fields", payload['source_item']['id'] == item['input_id'] and payload['source_item']['text'] == item['text']
           and payload['source_item']['publication_date'] == item['publication_day'])
    empty_payload, empty_end = json.JSONDecoder().raw_decode(empty['messages'][1]['content'])
    same_rest = (dict(payload, open_theses=None) == dict(empty_payload, open_theses=None)
                 and carried['messages'][1]['content'][end:] == empty['messages'][1]['content'][empty_end:]
                 and carried['messages'][0] == empty['messages'][0] and {k: v for k, v in carried.items() if k != 'messages'} == {k: v for k, v in empty.items() if k != 'messages'})
    expect('it differs from the request built from an empty library only in the open questions', same_rest and empty_payload['open_theses'] == [])

    print('3. the date check judges something')
    store = sqlite3.connect(f"file:{STORED / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    first_seen = dict(store.execute('select evidence_id, min(publication_day) from evidence_sources group by evidence_id'))
    requests = json.loads((STORED / 'judge/draw-c1/judge-requests.json').read_text())
    check = lambda request: [e for e in request['shown'] if e not in first_seen or first_seen[e] > request['day']]
    latest = max(first_seen, key=lambda e: first_seen[e])
    planted = dict(requests[0], shown=requests[0]['shown'] + [latest])
    expect('on a request holding a statement first read after its day, the check reports it', check(planted) == [latest],
           f"day {requests[0]['day']}, statement {latest} first read {first_seen[latest]}")
    expect('on the stored requests it reports none', all(not check(r) for r in requests), f'{len(requests)} requests')
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
