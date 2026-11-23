"""The comparison's input check (plan §1.2 item 5, code change B; $0): the items each system would read over a date range from the given
items database, through each system's own entry. Production: the replay's own loop (`testdb.feed` per day, `--only NVDA`,
`dispatch.route` on an empty store; only items routed to extraction are read). Clean: the runner's own selection rule
(`runner.selected_items` refuses any item outside it). The two must be the same items, and the clean manifest is written in production's
order, with the text identity of every item as the clean entry reads it. Controls: an excluded article is in neither list; a kept article is
in both. `fresh_week_inputs.py` (2026-11-14) with the dates and the database as arguments; nothing else changed.

    python3 comparison_inputs.py <items db> <from day> <until day> <manifest output> <excluded id> <kept id>
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
from hivemind import dispatch, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402
import runner  # noqa: E402


def production_list(items, first, last):
    items_db = testdb.open_db(str(items))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    out = []
    with tempfile.TemporaryDirectory() as folder:
        conn = store.open_db(str(Path(folder) / 'views.sqlite'))
        day = datetime.date.fromisoformat(first)
        while day.isoformat() <= last:
            for item in testdb.feed(items_db, day.isoformat(), day.isoformat()):
                if not any(o['value'] in ('NVDA',) for o in item['object_identifiers']):
                    continue
                if dispatch.route(conn, item, uni).kind == 'extract':
                    out.append(item['input_id'])
            day += datetime.timedelta(days=1)
    return out


def main(items, first, last, manifest_path, excluded_id, kept_id):
    prod = production_list(items, first, last)
    manifest = {'entity': 'NVDA', 'from_day': first, 'until_day': last, 'item_limit': len(prod), 'item_ids': prod}
    clean_items = runner.selected_items(items, manifest)                    # refuses any item outside the clean selection rule
    conn = sqlite3.connect(f'file:{items}?mode=ro', uri=True)
    rule = [r[0] for r in conn.execute(
        'select input_id, object_identifiers, text, feed, copy_of, supersedes from items where publication_day between ? and ? '
        'order by publication_day', (first, last))
        if 'NVDA' in [x.get('value') for x in json.loads(r[1] or '[]') if x.get('kind') == 'ticker']
        and r[2] and r[3] == 1 and not r[4] and not r[5]]
    if sorted(rule) != sorted(prod):
        raise SystemExit(f'the two entries differ: production {len(prod)}, the clean rule {len(rule)}; '
                         f'only production {sorted(set(prod) - set(rule))[:5]}; only clean {sorted(set(rule) - set(prod))[:5]}')
    if [i['input_id'] for i in clean_items] != prod:
        raise SystemExit('the clean entry does not read the items in production order')
    if excluded_id in prod or excluded_id in rule:
        raise SystemExit(f'control failed: the excluded {excluded_id} is still read')
    if kept_id not in prod or kept_id not in rule:
        raise SystemExit(f'control failed: the kept {kept_id} is not read')
    identity = hashlib.sha256('\n'.join(f"{i['input_id']}:{hashlib.sha256((i['text'] or '').encode()).hexdigest()}" for i in clean_items).encode()).hexdigest()
    Path(manifest_path).write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'{len(prod)} items {first}..{last}, the same set and order through both entries; excluded control absent, kept control present; '
          f'text identity {identity}; manifest written')


if __name__ == '__main__':
    main(*sys.argv[1:7])
