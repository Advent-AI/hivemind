"""Lean step 2, input check ($0): the items each system would read for 2026-09-22..28, through each system's own entry. Production: the
replay's own loop (`testdb.feed` per day, `--only NVDA`, `dispatch.route` on an empty store; only items routed to extraction are read). Clean:
the runner's own selection rule (`runner.selected_items` refuses any item outside it). The two lists must be the same items in the same order,
with the same text identity (sha256 of the stored text), or nothing is written. Writes the clean manifest from the production list.

  python3 fresh_week_inputs.py <manifest output path>
"""
import datetime
import hashlib
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
from hivemind import config, dispatch, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402
import runner  # noqa: E402

ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
FROM, UNTIL = '2026-09-22', '2026-09-28'


def production_list():
    items_db = testdb.open_db(str(ITEMS))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    out = []
    with tempfile.TemporaryDirectory() as folder:
        conn = store.open_db(str(Path(folder) / 'views.sqlite'))
        day = datetime.date.fromisoformat(FROM)
        while day.isoformat() <= UNTIL:
            for item in testdb.feed(items_db, day.isoformat(), day.isoformat()):
                if not any(o['value'] in ('NVDA',) for o in item['object_identifiers']):
                    continue
                if dispatch.route(conn, item, uni).kind == 'extract':
                    out.append(item['input_id'])
            day += datetime.timedelta(days=1)
    return out


def main():
    prod = production_list()
    manifest = {'entity': 'NVDA', 'from_day': FROM, 'until_day': UNTIL, 'item_limit': len(prod), 'item_ids': prod}
    clean_items = runner.selected_items(ITEMS, manifest)                    # refuses any item outside the clean selection rule
    conn = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    rule = [r[0] for r in conn.execute(
        "select input_id, object_identifiers, text, feed, copy_of, supersedes from items where publication_day between ? and ? order by publication_day",
        (FROM, UNTIL)) if 'NVDA' in [x.get('value') for x in json.loads(r[1] or '[]') if x.get('kind') == 'ticker']
        and r[2] and r[3] == 1 and not r[4] and not r[5]]
    if sorted(rule) != sorted(prod):
        raise SystemExit(f'the two entries differ: production {len(prod)}, the clean rule {len(rule)}; '
                         f'only production {sorted(set(prod) - set(rule))[:5]}; only clean {sorted(set(rule) - set(prod))[:5]}')
    identity = hashlib.sha256('\n'.join(f"{i['input_id']}:{hashlib.sha256((i['text'] or '').encode()).hexdigest()}" for i in clean_items).encode()).hexdigest()
    Path(sys.argv[1]).write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'{len(prod)} items, the same set and order through both entries; text identity {identity[:16]}; manifest written')


if __name__ == '__main__':
    main()
