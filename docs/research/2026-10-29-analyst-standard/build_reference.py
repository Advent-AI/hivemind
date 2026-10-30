"""Merge the hand-written reference parts into reference-week.json and reference-holdout.json, check every quoted span is a
verbatim substring of the item's text, count the statements by weight, and record sha256 of both files (the freeze)."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
WEEK_PARTS = ['reference-week-part0.json', 'reference-week-part1.json', 'reference-week-part1b.json', 'reference-week-part2a.json',
              'reference-week-part2b.json', 'reference-week-part3a.json', 'reference-week-part3b.json', 'reference-week-part3c.json']
HOLDOUT_PARTS = ['reference-holdout-partA.json', 'reference-holdout-partB.json']
WEIGHTS = ('core', 'supporting', 'optional')


def text_of(conn, input_id):
    row = conn.execute('select text from items where input_id=?', (input_id,)).fetchone()
    assert row, input_id
    return row[0]


def check(entries, conn, expected_ids):
    problems = []
    ids = [e['input_id'] for e in entries]
    assert len(ids) == len(set(ids)), 'duplicate input_id'
    missing = set(expected_ids) - set(ids)
    extra = set(ids) - set(expected_ids)
    assert not missing and not extra, (sorted(missing), sorted(extra))
    seen = set()
    for e in entries:
        text = text_of(conn, e['input_id'])
        for s in e.get('statements', []) + e.get('exclude', []):
            assert s['id'] not in seen, s['id']
            seen.add(s['id'])
            if 'weight' in s:
                assert s['weight'] in WEIGHTS, s['id']
            for span in [s['span']] + list(s.get('also', [])):
                if span not in text:
                    problems.append((e['input_id'], s['id'], span))
    return problems


def summarise(entries):
    counts = {w: 0 for w in WEIGHTS}
    counts.update({'exclude': 0, 'articles': len(entries), 'articles_with_statements': 0, 'must_propose': 0})
    for e in entries:
        for s in e.get('statements', []):
            counts[s['weight']] += 1
        counts['exclude'] += len(e.get('exclude', []))
        counts['articles_with_statements'] += bool(e.get('statements'))
        counts['must_propose'] += len(e.get('must_propose', []))
    return counts


def render(entries, title, path):
    lines = [f'# {title}', '', 'Rendered from the JSON (edit the JSON, never this file).', '']
    for e in entries:
        head = f"## {e['input_id']}" + (f" · call {e['call_id']}" if 'call_id' in e else '')
        lines.append(head)
        if e.get('statements'):
            lines.append('| id | weight | kind | tier | who | span | note |')
            lines.append('|---|---|---|---|---|---|---|')
            for s in e['statements']:
                span = s['span'] + (' ／ ' + ' ／ '.join(s['also']) if s.get('also') else '')
                lines.append(f"| {s['id']} | {s['weight']} | {s['kind']} | {s['tier']} | {s['who']} | {span} | {s['note']} |".replace('\n', ' '))
        else:
            lines.append('No statement to keep.')
        for x in e.get('exclude', []):
            lines.append(f"- exclude {x['id']}: {x['span']} — {x['note']}")
        for m in e.get('must_propose', []):
            lines.append(f"- must propose ({m['opens_as']}): {m['gist']}")
        for m in e.get('must_not_propose', []):
            lines.append(f"- must not propose: {m}")
        lines.append(f"- rejected: {e.get('rejected_note', '')}")
        lines.append('')
    path.write_text('\n'.join(lines) + '\n')


def main():
    conn = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    manifest = json.loads((HERE / 'haiku-week' / 'manifest.json').read_text())
    week_ids = [i['input_id'] for i in manifest['items'] if i.get('set', 'week') == 'week']
    holdout_ids = [h['input_id'] for h in json.loads((HERE / 'holdout-pick.json').read_text())]
    week = [e for p in WEEK_PARTS for e in json.loads((HERE / p).read_text())]
    holdout = [e for p in HOLDOUT_PARTS for e in json.loads((HERE / p).read_text())]
    week.sort(key=lambda e: e['call_id'])
    problems = check(week, conn, week_ids) + check(holdout, conn, holdout_ids)
    for p in problems:
        print('SPAN NOT IN TEXT', p)
    if problems:
        sys.exit(1)
    header = {'written': '2026-10-29 by Claude from the item texts under docs/research/2026-10-29-analyst-standard/standard.md (D229), '
                         'before any send; no model answer of this harness read. Week = development set (its v36b/v37/v38 answers were '
                         'read earlier); holdout = 20 unseen articles of 2026-07-08..14.',
              'unit': 'one research matter in one article; several spans may express it (span + also); a model record matches when its '
                      'quote covers span or any also',
              'weights': 'core / supporting / optional per standard.md §4; exclude = Alex-excluded (retention counts as false admission)',
              'restated_rule': 'a filed figure, guidance or deal older than the window, restated: optional (kept or omitted without '
                               'penalty; a changed period, basis or certainty is a distortion)'}
    (HERE / 'reference-week.json').write_text(json.dumps({'about': header, 'articles': week}, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'reference-holdout.json').write_text(json.dumps({'about': header, 'articles': holdout}, ensure_ascii=False, indent=1) + '\n')
    render(week, 'Reference: the v38 week (98 articles)', HERE / 'reference-week.md')
    render(holdout, 'Reference: the holdout (20 articles, 2026-07-08..14)', HERE / 'reference-holdout.md')
    digests = {}
    for name in ('reference-week.json', 'reference-holdout.json'):
        digests[name] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    (HERE / 'reference.sha256').write_text(''.join(f'{d}  {n}\n' for n, d in digests.items()))
    print('week', summarise(week))
    print('holdout', summarise(holdout))
    print(digests)


if __name__ == '__main__':
    main()
