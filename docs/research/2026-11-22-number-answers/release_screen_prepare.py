"""Prepare the $0 screen check of RELEASE-PAGE.md §6: build the format-2 pages with the real command, and freeze screen-expected.json
from the accepted slice-1 packages before the first screen run.

    python3 docs/research/2026-11-22-number-answers/release_screen_prepare.py <new run folder>

The expected file is written from the data of `poc/data/release-check-2026-11-23g/` (the packages council 75g accepted), not from the
pages under test, and its sha256 is printed for the result."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(REPO / 'tests'))
from hivemind import release, service  # noqa: E402
from hivemind.views import store  # noqa: E402

ACCEPTED = REPO / 'poc/data/release-check-2026-11-23g'
COMPARISON_ITEMS = REPO / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
OLD = {name: REPO / f'poc/data/comparison-2026-11-17/run/{name}/prod/views.sqlite' for name in ('old-1', 'old-3')}
DOT = f' {chr(0xb7)} '
ESCAPE_QUOTE = '</script><img src=x onerror=alert(1)> & a line' + chr(0x2028) + 'break'


def counts_line(questions):
    n = {kind: sum(q['class'] == kind for q in questions) for kind in ('number', 'event', 'yes_no')}
    return f"{n['number']} number questions{DOT}{n['event']} event questions{DOT}{n['yes_no']} Yes/No questions"


def kept(texts):
    """The page's reading rule: each text trimmed, empty texts dropped."""
    return [t.strip() for t in texts if t and t.strip()]


def card_top(q):
    n = len(q['evidence'])
    status = 'Open' if q['open'] else 'Closed'
    shown = q['forecast'] if q['class'] == 'number' else ('Not yet answered' if q['answer'] is None else f"Answer: {q['answer']}")
    count = 'No evidence in force' if n == 0 else f"{n} {'piece' if n == 1 else 'pieces'} of evidence"
    return kept([q['question'], status, shown, count])


def group(e):
    day = f", {e['original_day']}" if e['original_day'] else ''           # the page adds the day only when there is one
    texts = ['Hivemind summary', e['one_line'], 'Source quote', e['quote'], f"{e['tier']}{DOT}{e['speaker']}{DOT}original: {e['original_who']}{day}"]
    for s in e['sources']:
        texts += [s['title'], s['publisher'], s['day'], s['uri']]
    return kept(texts)


def frozen_page(data, checked):
    header = kept(['Hivemind release', f"As of {data['as_of']}", counts_line(data['questions'])])
    cards = [{'id': q['id'], 'top': card_top(q), 'groups': []} for q in data['questions']]
    collapsed = {'header': header, 'cards': cards, 'other': [], 'clipped': [], 'unreadable': []}
    expanded = json.loads(json.dumps(collapsed))
    target = next(c for c in expanded['cards'] if c['id'] == checked)
    target['groups'] = [group(e) for e in next(q for q in data['questions'] if q['id'] == checked)['evidence']]
    return {'count': len(data['questions']), 'collapsed': collapsed, 'expanded': expanded}


def build(ledger, items, out, as_of=None):
    args = [sys.executable, str(REPO / 'scripts/release_build.py'), 'build', '--ledger', str(ledger), '--items', str(items), '--out', str(out)]
    result = subprocess.run(args + (['--as-of', as_of] if as_of else []), capture_output=True, text=True, env={'PATH': '/usr/bin:/bin', 'PYTHONDONTWRITEBYTECODE': '1'})
    if result.returncode:
        raise SystemExit(f'build {out}: {result.stderr}')


def main(run):
    run = Path(run).absolute()
    run.mkdir()
    build(OLD['old-1'], COMPARISON_ITEMS, run / 'old-1')
    build(OLD['old-3'], COMPARISON_ITEMS, run / 'old-3-0825', '2026-08-25')
    build(OLD['old-1'], COMPARISON_ITEMS, run / 'old-1-0828', '2026-08-28')
    import test_release as fixture                                  # the test suite's fixture store, plus one hostile quote
    scratch = run / '.escape-stores'
    scratch.mkdir()
    views, items = fixture.make_store(scratch / 'views.sqlite'), fixture.make_items(scratch / 'items.sqlite')
    conn = store.open_db(str(views))
    fixture.evidence(conn, 'e9', 'v6', 1, 'A hostile quote, shown as text.', ESCAPE_QUOTE, [('item-1', 1)])
    conn.commit()
    conn.close()
    build(views, items, run / 'escape')
    data = lambda folder: json.loads((ACCEPTED / folder / 'release-data.json').read_text())
    expected = {
        'accepted': str(ACCEPTED),
        'pages': {'old-1/v8': frozen_page(data('old-1/package'), 'v8'),
                  'old-3/v36@2026-08-25': frozen_page(data('old-3/package-2026-08-25'), 'v36'),
                  'old-1/v10@2026-08-28': frozen_page(data('old-1/package-2026-08-28'), 'v10')},
        'morningstar_quote': next(e['quote'] for q in data('old-1/package')['questions'] for e in q['evidence'] if e['id'] == 'e2295'),
        'escape': {'question': 'v6', 'quote': ESCAPE_QUOTE.strip(), 'count': 7},
    }
    path = run / 'screen-expected.json'
    path.write_text(json.dumps(expected, ensure_ascii=False, indent=1))
    print('screen-expected.json sha256', hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    main(sys.argv[1])
