"""Choose the fresh acceptance articles (no model calls).

An item is eligible when it passes the runner's own selection rules. Eligible items are ordered by:
1. publication day;
2. `published_at` in UTC, when its date equals the publication day; otherwise 23:59:59Z of that day (news items store RFC 822
   text, and some carry a retrieval time);
3. input id.

The first `count` eligible items from `start` whose id no stored file mentions are taken. Mentions come from a hits file, written by
the census below: {path: [ids]}. A path listed in `--not-uses` is not counted, because the file only holds the source articles
themselves; no run sent them to a model.

The census matches whole ids, ids holding a second colon included, and checks itself: every dev and test id must be found.

Usage:
- `select_fresh.py census <hits.json>`
- `select_fresh.py choose <hits.json> <start day> <count> <output folder> [--not-uses <prefix> ...]`"""
import datetime, email.utils, hashlib, json, os, re, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import testdb  # noqa: E402

SOURCE = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SCANNED = ['poc/data', 'clean-arch', 'docs', 'reports', 'research_notes', '../tn-hivemind/docs']
TOKEN = re.compile(rb'(?:gnews|nvblog|nvidianews|official|truenorth|edgar|extra):[A-Za-z0-9._~%:/-]+')
DEV = ROOT / 'poc/data/clean-step1-unfiled-2026-11-08/gold-c7-flash/manifest.json'
TEST = ROOT / 'poc/data/clean-step1-unfiled-2026-11-08/test-c7-flash/manifest.json'


def connect():
    conn = sqlite3.connect(SOURCE.as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def census(hits_path):
    all_ids = {row[0] for row in connect().execute('select input_id from items')}
    hits = {}
    for root in SCANNED:
        for folder, _, files in os.walk(ROOT / root):
            for name in files:
                path = os.path.join(folder, name)
                try:
                    data = open(path, 'rb').read()
                except OSError:
                    continue
                found = set()
                for token in set(TOKEN.findall(data)):
                    text = token.decode('ascii', 'ignore')
                    for candidate in (text, text.rstrip('.:/-'), text.split('/')[0].rstrip('.:-')):
                        if candidate in all_ids:
                            found.add(candidate)
                if found:
                    hits[os.path.relpath(path, ROOT)] = sorted(found)
    mentioned = set().union(*map(set, hits.values()))
    for label, manifest in (('dev', DEV), ('test', TEST)):
        ids = json.loads(manifest.read_text())['item_ids']
        missing = [i for i in ids if i not in mentioned]
        if missing:
            raise SystemExit(f'census check failed: {len(missing)} {label} ids not found, e.g. {missing[:3]}')
    Path(hits_path).write_text(json.dumps(hits))
    print(f'{len(hits)} files mention an article id; every dev and test id found')


def when(item):
    raw = item['published_at'] or ''
    try:
        stamp = datetime.datetime.fromisoformat(raw.replace('Z', '+00:00'))
    except ValueError:
        try:
            stamp = email.utils.parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            stamp = None
    if stamp is not None:
        stamp = (stamp if stamp.tzinfo else stamp.replace(tzinfo=datetime.timezone.utc)).astimezone(datetime.timezone.utc)
        if stamp.date().isoformat() == item['publication_day']:
            return stamp.strftime('%Y-%m-%dT%H:%M:%SZ'), 'stated'
    return item['publication_day'] + 'T23:59:59Z', 'end of day'


def choose(hits_path, start, count, output, not_uses):
    hits = json.loads(Path(hits_path).read_text())
    used = {}
    for path, ids in hits.items():
        if any(path.startswith(prefix) for prefix in not_uses):
            continue
        for item_id in ids:
            used.setdefault(item_id, []).append(path)
    eligible = []
    for row in connect().execute('select * from items where publication_day >= ?', (start,)):
        item = testdb.item_of(row)
        tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
        if 'NVDA' not in tags or not item.get('text') or item.get('feed') != 1 or item.get('copy_of') or item.get('supersedes'):
            continue
        time, source = when(item)
        eligible.append((item['publication_day'], time, item['input_id'], source))
    eligible.sort()
    fresh = [e for e in eligible if e[2] not in used][:count]
    if len(fresh) < count:
        raise SystemExit(f'only {len(fresh)} unused eligible items from {start}')
    skipped = [e for e in eligible if e[2] in used and e <= fresh[-1]]
    out = Path(output)
    manifest = {'entity': 'NVDA', 'from_day': fresh[0][0], 'until_day': fresh[-1][0], 'item_limit': count,
                'item_ids': [e[2] for e in fresh]}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    (out / 'selection.json').write_text(json.dumps({
        'start': start, 'count': count, 'not_uses': not_uses, 'hits_files': len(hits),
        'order': [{'input_id': e[2], 'day': e[0], 'time': e[1], 'time_source': e[3]} for e in fresh],
        'skipped_used': {e[2]: used[e[2]] for e in skipped}}, indent=1))
    digest = hashlib.sha256((out / 'manifest.json').read_bytes()).hexdigest()
    print(f'{count} items {fresh[0][0]} -> {fresh[-1][0]}; {len(skipped)} used items skipped in the span; manifest sha256 {digest}')


if __name__ == '__main__':
    if sys.argv[1] == 'census':
        census(sys.argv[2])
    else:
        not_uses = sys.argv[sys.argv.index('--not-uses') + 1:] if '--not-uses' in sys.argv else []
        choose(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], not_uses)
