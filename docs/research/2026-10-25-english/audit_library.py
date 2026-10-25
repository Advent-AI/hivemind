"""D163: inventory the selected English-library inputs without generating theses.

Read source databases and historical ledgers only. Exercise the real feed and
dispatch on temporary storage. The output pins source identity; it does not
certify the meaning of source text or the quality of future extraction.
"""
import argparse
import collections
import contextlib
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import dispatch, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

SOURCES = ('poc/data/items-window.sqlite',
           'poc/data/items-window-tags2-2026-10-24.sqlite',
           'poc/corpus/items.sqlite')
SELECTED = SOURCES[1]
LEDGERS = ('poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite',
           'poc/data/views-2026-10-25-v15-T4c.sqlite')
STAGES = (('seed', '2026-02-25', '2026-07-23'),
          ('first_week', '2026-07-24', '2026-07-31'),
          ('extension', '2026-08-01', '2026-08-15'))
KNOWN_INPUT = 'edgar:NVDA:0001045810-26-000021:nvda-20260125.htm'


def read_only(path):
    if not path.is_file():
        raise ValueError(f'missing database: {path}')
    conn = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return contextlib.closing(conn)


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def source_problems(item):
    problems = []
    try:
        day = item['publication_day']
        if datetime.date.fromisoformat(day).isoformat() != day:
            problems.append('noncanonical publication day')
    except (KeyError, TypeError, ValueError):
        problems.append('invalid publication day')
    if item['feed'] == 1:
        if item['coverage'] != 'full' or not item['text']:
            problems.append('feed item has no full body')
        if hashlib.sha256((item['text'] or '').encode()).hexdigest() != item['content_sha256']:
            problems.append('body does not match stored hash')
    return problems


def verify_controls(record):
    """The real filing passes; body/date defects must fail this same check."""
    assert record['input_id'] == KNOWN_INPUT
    assert not source_problems(record), 'known filing failed'
    altered = dict(record, text=record['text'] + '\nchanged body')
    assert 'body does not match stored hash' in source_problems(altered), 'hash control was not caught'
    altered = dict(record, publication_day='not-a-date')
    assert 'invalid publication day' in source_problems(altered), 'date control was not caught'


def inventory():
    report = {'decision': 'D163', 'generated_for': '2026-10-25',
              'status': 'input preparation only; no English model run',
              'source_databases': [], 'historical_ledgers': [], 'stages': []}
    before = {rel: digest(ROOT / rel) for rel in (*SOURCES, *LEDGERS)}
    for rel in SOURCES:
        with read_only(ROOT / rel) as conn:
            counts = dict(conn.execute('select count(*) rows, sum(feed=1) feed, '
                                       'min(publication_day) first_day, max(publication_day) last_day from items').fetchone())
            counts['seed_feed'] = conn.execute('select count(*) from items where bootstrap=1 and feed=1').fetchone()[0]
            report['source_databases'].append({'path': rel, 'sha256': before[rel], **counts})
    with read_only(ROOT / SOURCES[0]) as original, read_only(ROOT / SELECTED) as corrected:
        old = {r['input_id']: dict(r) for r in original.execute('select * from items')}
        new = {r['input_id']: dict(r) for r in corrected.execute('select * from items')}
        if old.keys() != new.keys():
            raise ValueError('corrected source population differs from original input IDs')
        immutable = ('text', 'source_uri', 'publication_day', 'content_sha256')
        changes = collections.Counter(key for ident in old for key in old[ident]
                                      if old[ident][key] != new[ident][key])
        report['source_label_changes'] = {'compared': len(old), 'changed_fields': dict(changes),
                                          'source_fields_unchanged': all(not changes[key] for key in immutable)}
        if not report['source_label_changes']['source_fields_unchanged']:
            raise ValueError('corrected labels also changed original source content or identity')
    for rel in LEDGERS:
        with read_only(ROOT / rel) as conn:
            counts = {table: conn.execute(f'select count(*) from {table}').fetchone()[0]
                      for table in ('views', 'evidence', 'judgements')}
            counts['question_with_chinese'] = sum(any('\u4e00' <= c <= '\u9fff' for c in row[0])
                                                  for row in conn.execute('select question from views'))
            counts['judgement_cadence'] = [dict(row) for row in conn.execute(
                "select case when publication_day < '2026-07-29' then 'before_2026-07-29' "
                "else 'from_2026-07-29' end period, "
                "case when input_id like 'day:%' then 'day' else 'item' end owner, count(*) count "
                "from judgements group by 1,2")]
            report['historical_ledgers'].append({'path': rel, 'sha256': before[rel], **counts})
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    report['universe'] = {'path': 'poc/universe.json', 'sha256': digest(ROOT / 'poc/universe.json'), 'version': uni.version}
    report['source_problems'] = []
    with read_only(ROOT / SELECTED) as conn, tempfile.TemporaryDirectory(prefix='hivemind-input-audit-') as temporary:
        known = dict(conn.execute('select * from items where input_id=?', (KNOWN_INPUT,)).fetchone())
        verify_controls(known)
        report['positive_controls'] = ['known original filing', 'altered body refused', 'invalid date refused']
        with contextlib.closing(store.open_db(str(Path(temporary) / 'dispatch.sqlite'))) as routed:
            for name, first, last in STAGES:
                entries, routes = [], collections.Counter()
                for item in testdb.feed(conn, first, last):
                    problems = source_problems(item)
                    if problems:
                        report['source_problems'].append({'input_id': item['input_id'], 'problems': problems})
                    route = dispatch.route(routed, item, uni)
                    routes[route.kind] += 1
                    entries.append({key: item[key] for key in ('input_id', 'publication_day', 'category', 'title',
                                                              'content_sha256', 'source_uri', 'language', 'text_chars')} |
                                   {'route': route.kind, 'reason': route.reason,
                                    'sequence_no': route.sequence_no or None})
                if not entries or not routes['extract']:
                    raise ValueError(f'empty or unexercised stage: {name}')
                report['stages'].append({'name': name, 'from': first, 'until': last, 'items': len(entries),
                                         'routes': dict(routes), 'inputs': entries})
    changed = [rel for rel, sha in before.items() if digest(ROOT / rel) != sha]
    if changed:
        raise ValueError(f'input databases changed during read-only inventory: {changed}')
    report['all_input_databases_unchanged'] = True
    report['checks'] = {'judged_feed_records': sum(s['items'] for s in report['stages']),
                        'source_failures': len(report['source_problems']),
                        'limit': 'hash/date/full-body consistency and real dispatch only; source meaning not certified'}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='new JSON report; existing files are never overwritten')
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output already exists; choose a new dated report name')
    report = inventory()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    for stage in report['stages']:
        print(f'{stage["name"]}: {stage["items"]} input records; {stage["routes"]}')
    print(json.dumps(report['checks']))
    print(f'report: {args.out}')
    if report['source_problems']:
        sys.exit(1)


if __name__ == '__main__':
    main()
