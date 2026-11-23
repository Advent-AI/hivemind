"""Exposure census of the scored window (D667 item 2, D668; plan §1.2): which of the window's articles any past artifact holds, by id or by
text sha256. Every file under the roots is read (`.git` and this comparison's own folder excepted):
- SQLite files table by table, row by row (never as raw bytes, so an id split across overflow pages is still found);
- tar archives member by member (SQLite members are copied to a scratch file and read the same way);
- every other file as bytes.

A table holding `input_id` and `content_sha256` is exempt only when its (input_id, content_sha256) pair set equals a build listed in the
frozen `corpus-builds.json`. Its other tables are still read. The corpus-wide search index is exempt by path.

    python3 exposure_census.py <output folder> <scratch folder>

Writes census.json (population, hits per article, exclusions, kept articles per week, unscanned files, controls). Refuses to write when a
control fails.
"""
import datetime
import gzip
import hashlib
import json
import multiprocessing
import os
import re
import sqlite3
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWN = HERE.parent.resolve()
ROOT = Path('/Users/lchingen/hivemind')
SOURCE = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
WINDOW = ('2026-08-31', '2026-09-20')
BACKUPS = Path('/Users/lchingen/hivemind-backups')
SHA_TOKEN = re.compile(rb'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])')
CHUNK = 8 << 20
OVERLAP = 512
SQLITE_HEADER = b'SQLite format 3\x00'

BUILDS = json.loads((HERE / 'corpus-builds.json').read_text())
BUILD_HASHES = {b['pair_set_sha256'] for b in BUILDS['builds']}
SEARCH_INDEX = {str((ROOT / p).resolve()) for p in BUILDS['search_index']}


def population():
    """The scored window's articles by the clean selection rule: {input_id: content_sha256} and {id: day}."""
    conn = sqlite3.connect(f'file:{SOURCE}?mode=ro', uri=True)
    ids, days = {}, {}
    for iid, day, identifiers, text, feed, copy_of, supersedes, sha in conn.execute(
            'select input_id, publication_day, object_identifiers, text, feed, copy_of, supersedes, content_sha256 from items '
            'where publication_day between ? and ?', WINDOW):
        tickers = [x.get('value') for x in json.loads(identifiers or '[]') if x.get('kind') == 'ticker']
        if 'NVDA' in tickers and text and feed == 1 and not copy_of and not supersedes:
            ids[iid], days[iid] = sha, day
    return ids, days


def roots():
    listing = subprocess.run(['git', '-C', str(ROOT), 'worktree', 'list', '--porcelain'], capture_output=True, text=True, check=True).stdout
    trees = [Path(line.split(' ', 1)[1]) for line in listing.splitlines() if line.startswith('worktree ')]
    return trees + [BACKUPS]


def files_under(base):
    for directory, subdirs, names in os.walk(base):
        here = Path(directory)
        subdirs[:] = [d for d in subdirs if d != '.git' and (here / d).resolve() != OWN]
        for name in names:
            path = here / name
            if path.is_file() and not path.is_symlink():
                yield path


class Matcher:
    """Finds the window's ids and text sha256 values in bytes. An id is found wherever it starts with its prefix, whatever follows it, as
    long as the next byte cannot continue the id: a fixed-length id (gnews, extra: 24 hex) is cut at its length, then its next byte must not
    be hex; a slug id (nvblog, nvidianews, edgar) is compared whole, then its next byte must not be a slug character."""
    PREFIX = re.compile(rb'(?:gnews|extra|nvblog|nvidianews|edgar):')
    FIXED = {b'gnews:', b'extra:'}

    def __init__(self, ids, shas):
        self.fixed = {i.encode() for i in ids if i.split(':', 1)[0] + ':' in ('gnews:', 'extra:')}
        self.slugs = {}
        for i in ids:
            if i.split(':', 1)[0] + ':' not in ('gnews:', 'extra:'):
                self.slugs.setdefault(i.split(':', 1)[0].encode() + b':', []).append(i.encode())
        self.shas = {s.encode(): i for i, s in shas.items()}

    def find(self, data):
        found = set()
        for match in self.PREFIX.finditer(data):
            start, prefix = match.start(), match.group()
            if prefix in self.FIXED:
                candidate = data[start:start + len(prefix) + 24]
                after = data[start + len(prefix) + 24:start + len(prefix) + 25]
                if candidate in self.fixed and not re.match(rb'[0-9a-f]', after):
                    found.add(candidate.decode())
            else:
                for slug in self.slugs.get(prefix, ()):
                    if data.startswith(slug, start):
                        after = data[start + len(slug):start + len(slug) + 1]
                        if not re.match(rb'[A-Za-z0-9_\-]', after):
                            found.add(slug.decode())
        for token in SHA_TOKEN.findall(data):
            if token in self.shas:
                found.add(self.shas[token])
        return found


def scan_bytes(stream, matcher):
    found, tail = set(), b''
    while True:
        block = stream.read(CHUNK)
        if not block:
            break
        data = tail + block
        found |= matcher.find(data)
        tail = data[-OVERLAP:]
    return found


def pair_set_hash(conn, table):
    pairs = sorted(f'{i}\t{s}' for i, s in conn.execute(f'select input_id, content_sha256 from "{table}"'))
    return hashlib.sha256('\n'.join(pairs).encode()).hexdigest()


def scan_sqlite(path, matcher, label):
    """{id: [location]}, exempt tables, error or None."""
    hits, exempt = {}, []
    try:
        conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
        conn.text_factory = bytes
        tables = [r[0].decode() for r in conn.execute("select name from sqlite_master where type='table'")]
        for table in tables:
            try:
                columns = [r[1].decode() for r in conn.execute(f'pragma table_info("{table}")')]
                if {'input_id', 'content_sha256'} <= set(columns):
                    conn.text_factory = str
                    exempt_hash = pair_set_hash(conn, table) in BUILD_HASHES
                    conn.text_factory = bytes
                    if exempt_hash:
                        exempt.append(table)
                        continue
                for row in conn.execute(f'select * from "{table}"'):
                    for value in row:
                        if isinstance(value, (bytes, bytearray)):
                            data = bytes(value)
                        elif value is None or isinstance(value, (int, float)):
                            continue
                        else:
                            data = str(value).encode()
                        for article in matcher.find(data):
                            hits.setdefault(article, set()).add(f'{label}::{table}')
            except sqlite3.DatabaseError as error:
                hits.setdefault('__table_errors__', set()).add(f'{label}::{table}: {error}')
        conn.close()
        return hits, exempt, None
    except sqlite3.DatabaseError as error:
        return hits, exempt, f'{type(error).__name__}: {error}'


def scan_tar(path, matcher, scratch, label):
    hits, exempts, errors = {}, [], []
    with tarfile.open(path, mode='r|*') as archive:
        for member in archive:
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            head = stream.read(16)
            inner = f'{label}!{member.name}'
            if head == SQLITE_HEADER:
                copy = Path(scratch) / f'tar-{os.getpid()}.sqlite'
                with open(copy, 'wb') as out:
                    out.write(head)
                    while True:
                        block = stream.read(CHUNK)
                        if not block:
                            break
                        out.write(block)
                found, exempt, error = scan_sqlite(copy, matcher, inner)
                copy.unlink()
                for article, places in found.items():
                    hits.setdefault(article, set()).update(places)
                exempts += [f'{inner}::{t}' for t in exempt]
                if error:
                    errors.append(f'{inner}: {error}')
            else:
                class Joined:
                    def __init__(self):
                        self.first = head

                    def read(self, n):
                        if self.first:
                            data, self.first = self.first, b''
                            return data
                        return stream.read(n)
                for article in scan_bytes(Joined(), matcher):
                    hits.setdefault(article, set()).add(inner)
    return hits, exempts, errors


def scan_file(args):
    path, ids, shas, scratch = args
    matcher = Matcher(ids, shas)
    label = str(path)
    try:
        if str(Path(path).resolve()) in SEARCH_INDEX:
            return label, {}, ['(search index, exempt by path)'], []
        name = Path(path).name
        if name.endswith(('.tar', '.tar.gz', '.tgz')):
            hits, exempt, errors = scan_tar(path, matcher, scratch, label)
            return label, hits, exempt, errors
        with open(path, 'rb') as handle:
            head = handle.read(16)
        if head == SQLITE_HEADER:
            hits, exempt, error = scan_sqlite(path, matcher, label)
            return label, hits, exempt, [error] if error else []
        opener = gzip.open if name.endswith('.gz') else open
        with opener(path, 'rb') as handle:
            found = scan_bytes(handle, matcher)
        return label, {a: {label} for a in found}, [], []
    except Exception as error:                                    # recorded as unscanned, never silently passed
        return label, {}, [], [f'{type(error).__name__}: {error}']


def controls(ids, shas, scratch):
    """Three checks the census must pass before it is believed."""
    results = {}
    window_id = sorted(ids)[0]
    # 1. an id inside an overflowed cell is found
    db = Path(scratch) / 'control-overflow.sqlite'
    db.unlink(missing_ok=True)
    conn = sqlite3.connect(db)
    conn.execute('create table t (x text)')
    conn.execute('insert into t values (?)', ('x' * 9000 + f' "{window_id}" ' + 'x' * 9000,))
    conn.commit()
    conn.close()
    hits, _, _ = scan_sqlite(db, Matcher(ids, shas), 'control')
    results['overflowed cell found'] = window_id in hits
    # the matcher: an id inside a file name is found; a longer id that merely starts with it is not
    matcher = Matcher(ids, shas)
    gnews = next(i for i in sorted(ids) if i.startswith('gnews:'))
    slug = next(i for i in sorted(ids) if i.startswith('nvblog:'))
    results['id before a file suffix found'] = matcher.find(f'/cases/{gnews}.json'.encode()) == {gnews}
    results['longer id not taken for a window id'] = matcher.find(f'"{slug}-part-2"'.encode()) == set() and matcher.find(f'"{gnews}ab"'.encode()) == set()
    results['text sha found'] = matcher.find(f'sha={shas[gnews]};'.encode()) == {gnews}
    # 2. a raw copy of a listed build is exempt; 3. another table in the same file is still read
    db2 = Path(scratch) / 'control-copy.sqlite'
    db2.unlink(missing_ok=True)
    conn = sqlite3.connect(db2)
    conn.execute('create table items (input_id text, content_sha256 text)')
    source = sqlite3.connect(f'file:{SOURCE}?mode=ro', uri=True)
    conn.executemany('insert into items values (?, ?)', source.execute('select input_id, content_sha256 from items'))
    conn.execute('create table trace (request text)')
    other_id = sorted(ids)[1]
    conn.execute('insert into trace values (?)', (f'... {other_id} ...',))
    conn.commit()
    conn.close()
    hits, exempt, _ = scan_sqlite(db2, Matcher(ids, shas), 'control')
    results['raw copy exempt'] = exempt == ['items'] and window_id not in hits
    results['other table in the same file read'] = other_id in hits and hits[other_id] == {'control::trace'}
    return results


def main(out_dir, scratch):
    started = time.time()
    out_dir, scratch = Path(out_dir), Path(scratch)
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    ids, days = population()
    check = controls(ids, ids, scratch)
    if not all(check.values()):
        raise SystemExit(f'a control failed: {check}')
    tree_roots = roots()
    paths = [p for base in tree_roots for p in files_under(base)]
    jobs = [(str(p), sorted(ids), ids, str(scratch)) for p in paths]
    hits, exempt, errors = {}, {}, {}
    with multiprocessing.Pool(8) as pool:
        for label, found, ex, errs in pool.imap_unordered(scan_file, jobs, chunksize=4):
            for article, places in found.items():
                hits.setdefault(article, set()).update(places)
            if ex:
                exempt[label] = ex
            if errs:
                errors[label] = errs
    table_errors = sorted(hits.pop('__table_errors__', set()))
    excluded = sorted(a for a in hits if a in ids)
    kept = sorted(set(ids) - set(excluded))
    week = lambda d: str(datetime.date.fromisoformat(d) - datetime.timedelta(days=datetime.date.fromisoformat(d).weekday()))
    by_week = {}
    for article in ids:
        w = by_week.setdefault(week(days[article]), {'population': 0, 'excluded': 0, 'kept': 0})
        w['population'] += 1
        w['excluded' if article in hits else 'kept'] += 1
    report = {
        'window': WINDOW, 'source': str(SOURCE), 'corpus_builds_sha256': hashlib.sha256((HERE / 'corpus-builds.json').read_bytes()).hexdigest(),
        'roots': [str(r) for r in tree_roots], 'files_scanned': len(paths), 'seconds': round(time.time() - started),
        'controls': check, 'population': len(ids), 'excluded': len(excluded), 'kept': len(kept), 'by_week': dict(sorted(by_week.items())),
        'hits': {a: sorted(hits[a]) for a in excluded},
        'hit_counts': {a: len(hits[a]) for a in excluded},
        'kept_ids': kept, 'exempt_tables': exempt, 'unscanned_or_errors': errors, 'table_errors': table_errors,
    }
    text = json.dumps(report, indent=1, ensure_ascii=False) + '\n'
    (out_dir / 'census.json').write_text(text)
    (out_dir / 'census.json.sha256').write_text(hashlib.sha256(text.encode()).hexdigest() + '  census.json\n')
    print(json.dumps({k: report[k] for k in ('files_scanned', 'seconds', 'controls', 'population', 'excluded', 'kept', 'by_week')}, indent=1))
    print('files with errors:', len(errors), ' table errors:', len(table_errors), ' files with exempt tables:', len(exempt))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
