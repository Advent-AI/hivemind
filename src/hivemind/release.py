"""The "Forecast unavailable" release: one allow-listed export of a views ledger, its package and its checks
(docs/research/2026-11-22-number-answers/RELEASE-BUILD.md; D726, D756, D758).

A number question carries its question, its evidence in force and the marker "Forecast unavailable". An event or Yes/No question
carries its question, its evidence and its answer labels. Nothing else is read into the package: no rung condition or bound, no
judgement reason or explanation, no switch reason, no history. Before a package is published, every field is compared with its
stored source at the package's day, and nothing published replaces an existing path.
"""
import base64
import ctypes
import ctypes.util
import errno
import hashlib
import json
import os
import stat
import sys
import tempfile
from datetime import date
from pathlib import Path

from . import bundle, service, vocabulary
from .views import identity, store

FORMAT = 'hivemind-release/2'           # 2: the package holds the reader's page (RELEASE-PAGE.md)
ALLOW_LIST = 'release-allow-list/1'
FORECAST_UNAVAILABLE = 'Forecast unavailable'
DATA_FILE = 'release-data.json'
MANIFEST_FILE = 'manifest.json'
PAGE_FILE = 'index.html'
PACKAGE_FILES = frozenset({DATA_FILE, MANIFEST_FILE, PAGE_FILE})
CLASSES = ('number', 'event', 'yes_no')
ALLOWED = {
    'envelope': frozenset({'format', 'allow_list', 'as_of', 'questions'}),
    'number': frozenset({'id', 'question', 'open', 'class', 'forecast', 'evidence'}),
    'answered': frozenset({'id', 'question', 'open', 'class', 'answers', 'answer', 'evidence'}),
    'evidence': frozenset({'id', 'one_line', 'quote', 'tier', 'speaker', 'original_who', 'original_day', 'sources'}),
    'source': frozenset({'title', 'publisher', 'day', 'uri'}),
    'manifest': frozenset({'format', 'allow_list', 'as_of', 'data_sha256', 'page_sha256'}),
}
EVIDENCE_TEXT = ('one_line', 'quote', 'tier', 'speaker', 'original_who', 'original_day')
SOURCE_TEXT = ('title', 'publisher', 'day', 'uri')
RENAME_EXCL = 0x4          # macOS <stdio.h>: renamex_np refuses an existing destination
RENAME_NOREPLACE = 0x1     # Linux <linux/fs.h>: renameat2 refuses an existing destination
AT_FDCWD = -100


class ReleaseRefused(ValueError):
    """The release refuses the input, the export or the package; the message names what and where."""


# ---------- the day

def canonical_day(text):
    """A day written YYYY-MM-DD, returned unchanged; anything else is refused. The stores compare days as text, so a day Python
    also reads (20260825) would select rows from later days."""
    try:
        day = date.fromisoformat(text)
    except (TypeError, ValueError):
        raise ReleaseRefused(f'not a day: {text!r}') from None
    if day.isoformat() != text:
        raise ReleaseRefused(f'a day must be written YYYY-MM-DD: {text!r}')
    return text


def resolve(views_db, as_of=None):
    """The bound of a build or a check, one rule for both: a given day must be canonical; `service.resolve_bound` then refuses an
    unfinished first day or a day after the last completed day; an omitted day with no default is refused."""
    if as_of is not None:
        canonical_day(as_of)
    bound = service.resolve_bound(views_db, as_of)
    if not bound:
        raise ReleaseRefused('the store has no default day; supply --as-of')
    return canonical_day(bound)


# ---------- identity

def _has_table(conn, name):
    return conn.execute("select 1 from sqlite_master where type='table' and name=?", (name,)).fetchone() is not None


def key_measure(conn, view_id, as_of):
    """The measure of the view's key as recorded on or before the day, or None: no key table, no key, or a key written after the
    day (a later key never reclassifies an earlier package)."""
    if not _has_table(conn, 'view_keys'):
        return None
    row = conn.execute('select measure, seq from view_keys where view_id=?', (view_id,)).fetchone()
    return row['measure'] if row is not None and service.visible(conn, row['seq'], as_of) else None


def ladder(conn, view_id):
    """(position, label) of every rung, by position: the only rung columns the package reads."""
    return [(row['position'], row['label']) for row in conn.execute('select position, label from rungs where view_id=? order by position', (view_id,))]


def question_class(conn, view_id, labels, as_of):
    """'event' for an event measure in the key recorded by the day, 'yes_no' for exactly two labels that are Yes and No in the stored
    vocabulary, else 'number' (a view with no key and a ladder whose bands do not resolve included): the forecast of every number
    question is withheld."""
    if key_measure(conn, view_id, as_of) in identity.EVENT_MEASURES:
        return 'event'
    if len(labels) == 2 and {vocabulary.canonical('label', label) for label in labels} == {'Yes', 'No'}:
        return 'yes_no'
    return 'number'


def _answer(conn, view_id, as_of, positions):
    """The stored label of the latest judgement's rung on or before the day, or None when the question is not yet judged."""
    row = conn.execute('select rung from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (view_id, as_of)).fetchone()
    if row is None:
        return None
    if row['rung'] not in positions:
        raise ReleaseRefused(f'{view_id}: its latest judgement names rung {row["rung"]}, which its ladder does not hold')
    return positions[row['rung']]


# ---------- the export

def _item(items_db, cache, input_id, evidence_id):
    if input_id not in cache:
        row = items_db.execute('select title, publisher, source_uri from items where input_id=?', (input_id,)).fetchone()
        if row is None:
            raise ReleaseRefused(f'evidence {evidence_id}: source item {input_id} is not in the items database')
        cache[input_id] = row
    return cache[input_id]


def _visible_views(conn, as_of):
    return [row for row in conn.execute('select view_id, question, created_seq from views order by created_seq, rowid') if service.visible(conn, row['created_seq'], as_of)]


def release_export(views_db, items_db, as_of=None):
    """The release data as of the bound: every question visible on that day, closed ones included, built field by field from the
    allow-list. The result passes `check_export` or nothing is returned."""
    with bundle.read_snapshot(views_db, items_db):
        bound = resolve(views_db, as_of)
        items, questions = {}, []
        for view in _visible_views(views_db, bound):
            view_id = view['view_id']
            rungs = ladder(views_db, view_id)
            labels = [label for _, label in rungs]
            kind = question_class(views_db, view_id, labels, bound)
            record = {'id': view_id, 'question': view['question'], 'open': service.is_open_as_of(views_db, view_id, bound), 'class': kind}
            if kind == 'number':
                record['forecast'] = FORECAST_UNAVAILABLE
            else:
                record['answers'] = labels
                record['answer'] = _answer(views_db, view_id, bound, dict(rungs))
            evidence = []
            for piece in service.evidence(views_db, view_id, bound):
                sources = []
                for source in piece['sources']:
                    item = _item(items_db, items, source['input_id'], piece['evidence_id'])
                    sources.append({'title': item['title'], 'publisher': item['publisher'], 'day': source['publication_day'], 'uri': item['source_uri']})
                evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources})
            record['evidence'] = evidence
            questions.append(record)
        data = {'format': FORMAT, 'allow_list': ALLOW_LIST, 'as_of': bound, 'questions': questions}
    check_export(data)
    return data


# ---------- the closed set

def _keys(value, kind, where):
    if not isinstance(value, dict):
        raise ReleaseRefused(f'{where}: not an object')
    if set(value) != ALLOWED[kind]:
        extra, missing = sorted(set(value) - ALLOWED[kind]), sorted(ALLOWED[kind] - set(value))
        raise ReleaseRefused(f'{where}: keys off the allow-list {extra}, missing {missing}')


def _texts(value, names, where):
    for name in names:
        if not isinstance(value[name], str):
            raise ReleaseRefused(f'{where}: {name} is not text')


def check_export(data):
    """Every object at every level holds exactly its record type's keys, with values of the allowed kinds. Returns the counts
    judged."""
    _keys(data, 'envelope', 'the package')
    if data['format'] != FORMAT or data['allow_list'] != ALLOW_LIST:
        raise ReleaseRefused(f'the package names format {data["format"]!r} and allow-list {data["allow_list"]!r}')
    canonical_day(data['as_of'])
    if not isinstance(data['questions'], list):
        raise ReleaseRefused('the package: questions is not a list')
    counts = {'questions': {kind: 0 for kind in CLASSES}, 'evidence': 0, 'sources': 0}
    for position, question in enumerate(data['questions']):
        where = f'question {position}'
        if not isinstance(question, dict) or question.get('class') not in CLASSES:
            raise ReleaseRefused(f'{where}: no allowed class')
        kind = question['class']
        _keys(question, 'number' if kind == 'number' else 'answered', where)
        _texts(question, ('id', 'question'), where)
        where = f'question {question["id"]}'
        if not isinstance(question['open'], bool):
            raise ReleaseRefused(f'{where}: open is not true or false')
        if kind == 'number':
            if question['forecast'] != FORECAST_UNAVAILABLE:
                raise ReleaseRefused(f'{where}: a number question carries only the marker')
        else:
            answers = question['answers']
            if not (isinstance(answers, list) and len(answers) == 2 and all(isinstance(a, str) for a in answers)):
                raise ReleaseRefused(f'{where}: answers are not two labels')
            if question['answer'] is not None and question['answer'] not in answers:
                raise ReleaseRefused(f'{where}: the answer is not one of its labels')
        if not isinstance(question['evidence'], list):
            raise ReleaseRefused(f'{where}: evidence is not a list')
        for piece in question['evidence']:
            _keys(piece, 'evidence', f'{where} evidence')
            _texts(piece, ('id',), f'{where} evidence')
            _texts(piece, EVIDENCE_TEXT, f'{where} evidence {piece["id"]}')
            if not isinstance(piece['sources'], list):
                raise ReleaseRefused(f'{where} evidence {piece["id"]}: sources is not a list')
            for source in piece['sources']:
                _keys(source, 'source', f'{where} evidence {piece["id"]} source')
                _texts(source, SOURCE_TEXT, f'{where} evidence {piece["id"]} source')
            counts['sources'] += len(piece['sources'])
        counts['evidence'] += len(question['evidence'])
        counts['questions'][kind] += 1
    return counts


# ---------- the origin check

def _open_at(conn, view_id, as_of):
    for row in conn.execute('select open, after_seq from view_switches where view_id=? order by id desc', (view_id,)):
        if service.visible(conn, row['after_seq'], as_of):
            return bool(row['open'])
    return True


def _expected_evidence(views_db, items_db, view_id, as_of):
    """The evidence in force at the day, by its own SQL: visible links in link order, minus those whose latest replacement is
    visible; each source row visible at the day, in row order, with its item required."""
    out = []
    for link in views_db.execute('select evidence_id, seq from evidence_links where view_id=? order by id', (view_id,)).fetchall():
        if not service.visible(views_db, link['seq'], as_of):
            continue
        latest = views_db.execute('select seq from replacements where old_evidence_id=? order by id desc limit 1', (link['evidence_id'],)).fetchone()
        if latest is not None and service.visible(views_db, latest['seq'], as_of):
            continue
        row = views_db.execute(f'select evidence_id, {", ".join(EVIDENCE_TEXT)} from evidence where evidence_id=?', (link['evidence_id'],)).fetchone()
        if row is None:
            raise ReleaseRefused(f'{view_id}: link to evidence {link["evidence_id"]}, which the store does not hold')
        sources = []
        for source in views_db.execute('select input_id, publication_day, seq from evidence_sources where evidence_id=? order by id', (link['evidence_id'],)).fetchall():
            if not service.visible(views_db, source['seq'], as_of):
                continue
            item = items_db.execute('select title, publisher, source_uri from items where input_id=?', (source['input_id'],)).fetchone()
            if item is None:
                raise ReleaseRefused(f'evidence {row["evidence_id"]}: source item {source["input_id"]} is not in the items database')
            sources.append({'title': item['title'], 'publisher': item['publisher'], 'day': source['publication_day'], 'uri': item['source_uri']})
        out.append({'id': row['evidence_id'], **{name: row[name] for name in EVIDENCE_TEXT}, 'sources': sources})
    return out


def _leaves(value):
    if isinstance(value, dict):
        return sum(_leaves(v) for v in value.values())
    if isinstance(value, list):
        return sum(_leaves(v) for v in value)
    return 1


def _compare(expected, actual, where):
    """The number of leaf values compared; the first difference is refused, naming where it is."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(expected) != set(actual):
            raise ReleaseRefused(f'{where}: fields differ from the store')
        return sum(_compare(expected[key], actual[key], f'{where}.{key}') for key in expected)
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise ReleaseRefused(f'{where}: {len(actual) if isinstance(actual, list) else "no"} entries where the store has {len(expected)}')
        return sum(_compare(e, a, f'{where}[{n}]') for n, (e, a) in enumerate(zip(expected, actual)))
    if type(expected) is not type(actual) or expected != actual:
        raise ReleaseRefused(f'{where}: differs from the store')
    return 1


def check_origins(views_db, items_db, data, expected_as_of):
    """Every package field against its permitted stored source at `expected_as_of`, derived from the store and never from the
    package: the day, each question's class, the questions, evidence and sources in order with their counts. Its reads are its own
    SQL, apart from the identity rule (`question_class`) and the day of a sequence number (`service.visible`). Returns the number of
    fields compared."""
    with bundle.read_snapshot(views_db, items_db):
        as_of = canonical_day(expected_as_of)
        if data['as_of'] != as_of:
            raise ReleaseRefused(f'the package is dated {data["as_of"]}, the store bound is {as_of}')
        views = [row for row in views_db.execute('select view_id, question, created_seq from views order by created_seq, rowid')
                 if service.visible(views_db, row['created_seq'], as_of)]
        packaged = data['questions']
        if [q['id'] for q in packaged] != [row['view_id'] for row in views]:
            raise ReleaseRefused(f'the questions differ from the store: {len(packaged)} entries where the store has {len(views)}'
                                 if len(packaged) != len(views) else 'the questions or their order differ from the store')
        compared = _compare(FORMAT, data['format'], 'package.format') + _compare(ALLOW_LIST, data['allow_list'], 'package.allow_list') + 1
        for view, question in zip(views, packaged):
            view_id = view['view_id']
            positions = {row['position']: row['label'] for row in views_db.execute('select position, label from rungs where view_id=? order by position', (view_id,))}
            labels = list(positions.values())
            kind = question_class(views_db, view_id, labels, as_of)
            record = {'id': view_id, 'question': view['question'], 'open': _open_at(views_db, view_id, as_of), 'class': kind}
            if kind == 'number':
                record['forecast'] = FORECAST_UNAVAILABLE
            else:
                latest = views_db.execute('select rung from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (view_id, as_of)).fetchone()
                if latest is not None and latest['rung'] not in positions:
                    raise ReleaseRefused(f'question {view_id}: its latest judgement names rung {latest["rung"]}, which its ladder does not hold')
                record['answers'] = labels
                record['answer'] = None if latest is None else positions[latest['rung']]
            expected_evidence = _expected_evidence(views_db, items_db, view_id, as_of)
            if not isinstance(question.get('evidence'), list) or len(question['evidence']) != len(expected_evidence):
                found = len(question['evidence']) if isinstance(question.get('evidence'), list) else 'no'
                raise ReleaseRefused(f'question {view_id}.evidence: {found} entries where the store has {len(expected_evidence)}')
            record['evidence'] = question['evidence']           # compared piece by piece below, named by the stored evidence id
            compared += _compare(record, question, f'question {view_id}') - _leaves(question['evidence'])
            for expected, actual in zip(expected_evidence, question['evidence']):
                compared += _compare(expected, actual, f'question {view_id}.evidence {expected["id"]}')
        return compared


# ---------- the package

def _dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def stage(out_dir):
    """A private staging folder, unique to this invocation, beside the destination."""
    out_dir = Path(out_dir)
    return Path(tempfile.mkdtemp(dir=out_dir.parent, prefix=f'.{out_dir.name}.staging-'))


def write_package(data, staged):
    """The data file, the reader's page made from it, and their manifest, written into the staging folder."""
    payload = _dump(data)
    page = render_page(payload)
    (Path(staged) / DATA_FILE).write_bytes(payload)
    (Path(staged) / PAGE_FILE).write_bytes(page)
    manifest = {'format': data['format'], 'allow_list': data['allow_list'], 'as_of': data['as_of'],
                'data_sha256': hashlib.sha256(payload).hexdigest(), 'page_sha256': hashlib.sha256(page).hexdigest()}
    (Path(staged) / MANIFEST_FILE).write_bytes(_dump(manifest))


def _no_replace_rename():
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    if sys.platform == 'darwin' and hasattr(libc, 'renamex_np'):
        call = libc.renamex_np
        call.argtypes, call.restype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
        return lambda source, target: call(source, target, RENAME_EXCL)
    if sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        call = libc.renameat2
        call.argtypes, call.restype = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
        return lambda source, target: call(AT_FDCWD, source, AT_FDCWD, target, RENAME_NOREPLACE)
    return None


def publish(staged, out_dir):
    """One atomic move of the staged folder to the destination that refuses any existing destination, empty or not."""
    rename = _no_replace_rename()
    if rename is None:
        raise ReleaseRefused('this platform offers no atomic rename that refuses an existing destination')
    if rename(os.fsencode(str(staged)), os.fsencode(str(out_dir))) != 0:
        code = ctypes.get_errno()
        if code in (errno.ENOTSUP, errno.EINVAL, errno.ENOSYS):
            raise ReleaseRefused(f'the filesystem refuses an atomic no-replace rename ({os.strerror(code)})')
        raise OSError(code, os.strerror(code), str(out_dir))


def publish_report(report, path):
    """The report, written to a private temporary file and linked to its name; the link refuses any existing path, and its success
    is the moment the report is published. Returns None, or the temporary file it could not remove after publishing."""
    path = Path(path)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f'.{path.name}.')
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(json.dumps(report, ensure_ascii=False, indent=1).encode('utf-8'))
        os.link(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise
    try:
        os.unlink(temporary)
    except OSError:
        return temporary
    return None


def _unique_members(pairs):
    names = [name for name, _ in pairs]
    if len(names) != len(set(names)):
        raise ReleaseRefused(f'a JSON member name repeats: {sorted({n for n in names if names.count(n) > 1})}')
    return dict(pairs)


def read_data(package):
    """The package's data, read with the repeated-member check. `check_package` returns the data it checked, which is the copy to
    trust; this reader is for inspection only."""
    return _parse((Path(package) / DATA_FILE).read_bytes(), DATA_FILE)


URI_CHARACTERS = '%?#'


def store_path(path):
    """The resolved store path, the one the opener is then given (so the opener's own resolution has nothing left to follow): refused
    when it holds a character a SQLite URI decodes (`store.open_read_only` puts the path into a `file:` URI unescaped, so `%2D` would
    open a `-`)."""
    real = os.path.realpath(path)
    found = sorted({c for c in real if c in URI_CHARACTERS})
    if found:
        raise ReleaseRefused(f'{path}: a store path may not contain {found}, which the SQLite opener reads as URI syntax')
    return real


def _read_regular(folder, name, where):
    """The bytes of one regular file in an opened folder, read once through a descriptor that refuses a symbolic link and opens a pipe
    without waiting, so its type is refused instead."""
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)   # a pipe or device never blocks the check
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise ReleaseRefused(f'{where}/{name}: not a regular file') from None
        raise
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ReleaseRefused(f'{where}/{name}: not a regular file')
        chunks = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                return b''.join(chunks)
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _parse(raw, name):
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_members)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseRefused(f'{name}: not JSON ({error})') from None


def check_package(path, views_db=None, items_db=None, expected_as_of=None):
    """The package as a reader receives it: a real folder holding exactly the two regular files, each read once through one handle on
    the folder; JSON with no repeated member name; a closed manifest that agrees with the data and the sha256 of the very bytes
    parsed; data that passes `check_export` and, with the stores, `check_origins` at `expected_as_of` (or at the package's own day
    passed through `resolve`); and a page equal, byte for byte, to `render_page` of the very data bytes checked. Returns (counts, the data
    checked, its size in bytes)."""
    path = Path(path)
    try:
        folder = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise ReleaseRefused(f'{path}: not a folder') from None
        raise
    try:
        names = os.listdir(folder)
        if sorted(names) != sorted(PACKAGE_FILES):
            raise ReleaseRefused(f'{path}: holds {sorted(names)}, not exactly {sorted(PACKAGE_FILES)}')
        raw, manifest_raw, page = (_read_regular(folder, DATA_FILE, path), _read_regular(folder, MANIFEST_FILE, path),
                                   _read_regular(folder, PAGE_FILE, path))
    finally:
        os.close(folder)
    manifest, data = _parse(manifest_raw, MANIFEST_FILE), _parse(raw, DATA_FILE)
    counts = check_export(data)
    _keys(manifest, 'manifest', 'the manifest')
    if manifest['data_sha256'] != hashlib.sha256(raw).hexdigest():
        raise ReleaseRefused('the manifest sha256 does not match the data file')
    if page != render_page(raw):
        raise ReleaseRefused('the page is not the page made from its data')
    if manifest['page_sha256'] != hashlib.sha256(page).hexdigest():
        raise ReleaseRefused('the manifest page_sha256 does not match the page')
    for name in ('format', 'allow_list', 'as_of'):
        if manifest[name] != data[name]:
            raise ReleaseRefused(f'the manifest {name} {manifest[name]!r} differs from the data {data[name]!r}')
    if views_db is not None:
        bound = expected_as_of if expected_as_of is not None else resolve(views_db, data['as_of'])
        counts['fields_compared'] = check_origins(views_db, items_db, data, bound)
    return counts, data, len(raw)


# ---------- the reader's page (slice 2, RELEASE-PAGE.md)

PAGE_STYLE = (
    ':root{--paper:#f5f2eb;--wash:#ebe9e2;--rule:#dfddd6;--ink:#0f140d;--ink-2:#393d36;--ink-3:#6a6c65;color-scheme:light dark}'
    '@media (prefers-color-scheme: dark){:root{--paper:#0f140d;--wash:#1b2018;--rule:#393d36;--ink:#f5f2eb;--ink-2:#dfddd6;--ink-3:#9f9f98}}'
    '*{box-sizing:border-box}'
    'body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 "Helvetica Neue",Helvetica,Arial,sans-serif}'
    'main{max-width:860px;margin:0 auto;padding:24px 16px 64px}'
    '#fallback{max-width:860px;margin:24px auto;padding:0 16px;color:var(--ink-2)}'
    '.release-title{font-size:22px;font-weight:600;margin:0 0 4px}'
    '.release-day,.release-counts{margin:0;color:var(--ink-3);font-size:13px}'
    '.release-header{border-bottom:1px solid var(--rule);padding-bottom:16px;margin-bottom:8px}'
    '.question{border-bottom:1px solid var(--rule);padding:16px 0}'
    '.question-text{font-size:16px;font-weight:600;margin:0 0 6px;overflow-wrap:anywhere}'
    '.question-status{display:inline-block;margin:0 12px 0 0;font-size:12px;color:var(--ink-3);text-transform:none}'
    '.question-forecast,.question-answer{display:inline-block;margin:0;font-size:13px;padding:1px 8px;border:1px solid var(--rule);border-radius:999px;background:var(--wash)}'
    '.evidence{margin-top:10px}'
    '.evidence-count{cursor:pointer;font-size:13px;color:var(--ink-2)}'
    '.evidence-none{margin:10px 0 0;font-size:13px;color:var(--ink-3)}'
    '.evidence-list{margin:8px 0 0;padding-left:20px}'
    '.evidence-item{margin:0 0 14px}'
    '.evidence-label{margin:0 0 2px;font-size:11px;color:var(--ink-3)}'
    '.evidence-summary{margin:0 0 6px;overflow-wrap:anywhere}'
    '.evidence-quote{margin:0 0 4px;padding-left:10px;border-left:2px solid var(--rule);color:var(--ink-2);overflow-wrap:anywhere}'
    '.evidence-meta{margin:0 0 4px;font-size:12px;color:var(--ink-3);overflow-wrap:anywhere}'
    '.source-list{margin:0;padding-left:16px;font-size:12px;color:var(--ink-3)}'
    '.source>span{overflow-wrap:anywhere;margin-right:12px}'
)

PAGE_SCRIPT = (
    "(function(){'use strict';"
    "var data=JSON.parse(document.getElementById('release-data').textContent);"
    "var root=document.getElementById('release');"
    "function el(tag,cls,text){var e=document.createElement(tag);if(cls){e.className=cls;}if(text!==undefined){e.textContent=text;}return e;}"
    "function piece(e){var item=el('li','evidence-item');"
    "item.appendChild(el('p','evidence-label','Hivemind summary'));item.appendChild(el('p','evidence-summary',e.one_line));"
    "item.appendChild(el('p','evidence-label','Source quote'));"
    "item.appendChild(el('blockquote','evidence-quote',e.quote));"
    "item.appendChild(el('p','evidence-meta',e.tier+' \\u00b7 '+e.speaker+' \\u00b7 original: '+e.original_who+(e.original_day?', '+e.original_day:'')));"
    "var sources=el('ul','source-list');"
    "e.sources.forEach(function(s){var row=el('li','source');"
    "row.appendChild(el('span','source-title',s.title));row.appendChild(el('span','source-publisher',s.publisher));"
    "row.appendChild(el('span','source-day',s.day));row.appendChild(el('span','source-address',s.uri));sources.appendChild(row);});"
    "item.appendChild(sources);return item;}"
    "var counts={number:0,event:0,yes_no:0};data.questions.forEach(function(q){counts[q['class']]+=1;});"
    "var header=el('header','release-header');header.appendChild(el('h1','release-title','Hivemind release'));"
    "header.appendChild(el('p','release-day','As of '+data.as_of));"
    "header.appendChild(el('p','release-counts',counts.number+' number questions \\u00b7 '+counts.event+' event questions \\u00b7 '+counts.yes_no+' Yes/No questions'));"
    "root.appendChild(header);"
    "if(!data.questions.length){root.appendChild(el('p','release-empty','No questions as of '+data.as_of));}"
    "data.questions.forEach(function(q){var card=el('article','question');card.dataset.id=q.id;"
    "card.appendChild(el('h2','question-text',q.question));card.appendChild(el('p','question-status',q.open?'Open':'Closed'));"
    "if(q['class']==='number'){card.appendChild(el('p','question-forecast',q.forecast));}"
    "else{card.appendChild(el('p','question-answer',q.answer===null?'Not yet answered':'Answer: '+q.answer));}"
    "var n=q.evidence.length;"
    "if(!n){card.appendChild(el('p','evidence-none','No evidence in force'));}"
    "else{var details=el('details','evidence');details.appendChild(el('summary','evidence-count',n+(n===1?' piece of evidence':' pieces of evidence')));"
    "var list=null;details.addEventListener('toggle',function(){if(details.open&&!list){list=el('ol','evidence-list');"
    "q.evidence.forEach(function(e){list.appendChild(piece(e));});details.appendChild(list);}});card.appendChild(details);}"
    "root.appendChild(card);});"
    "var fallback=document.getElementById('fallback');fallback.parentNode.removeChild(fallback);"
    "})();"
)

PAGE_CSP = ("default-src 'none'; script-src {script}; style-src {style}; img-src 'none'; font-src 'none'; connect-src 'none'; "
            "base-uri 'none'; form-action 'none'")
EMBED_ESCAPED = ('<', '>', '&', chr(0x2028), chr(0x2029))


def _source_hash(text):
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode('utf-8')).digest()).decode('ascii') + "'"


def embed(data_bytes):
    """The data file's text with `<`, `>`, `&`, U+2028 and U+2029 replaced by their six-character JSON escapes: still the same JSON,
    and unable to close or comment out the block it sits in."""
    text = data_bytes.decode('utf-8')
    for character in EMBED_ESCAPED:
        text = text.replace(character, chr(92) + f'u{ord(character):04x}')
    return text


DATA_PLACEHOLDER = '@@RELEASE_DATA@@'


def page_template():
    """The whole reader's page with its one data placeholder: charset and CSP first; the CSP admits only this template's own script and
    style and no connection, image, font, base or form target. Its sha256 is pinned in the tests."""
    csp = PAGE_CSP.format(script=_source_hash(PAGE_SCRIPT), style=_source_hash(PAGE_STYLE))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta http-equiv="Content-Security-Policy" content="{csp}">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Hivemind release</title>\n'
            f'<style>{PAGE_STYLE}</style>\n</head>\n<body>\n'
            '<p id="fallback">This release page needs JavaScript to show its questions.</p>\n<main id="release"></main>\n'
            f'<script type="application/json" id="release-data">{DATA_PLACEHOLDER}</script>\n'
            f'<script>{PAGE_SCRIPT}</script>\n</body>\n</html>\n')


def render_page(data_bytes):
    """The reader's page: the pinned template split once at its placeholder, with the escaped data inserted."""
    before, after = page_template().split(DATA_PLACEHOLDER)
    return (before + embed(data_bytes) + after).encode('utf-8')


# ---------- the report

def withheld_unresolved(views_db, data):
    """For the release report only: the number questions whose ladder does not resolve to bands, with the reason and whether the
    view has a key. Withheld like every number question; this list never enters the package."""
    out = []
    for question in data['questions']:
        if question['class'] != 'number':
            continue
        bands, reason = service.ladder_bands(store.rungs_of(views_db, question['id']))
        if bands is None:
            out.append({'id': question['id'], 'reason': reason, 'has_key': key_measure(views_db, question['id'], data['as_of']) is not None})
    return out
