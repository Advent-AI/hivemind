"""The "Forecast unavailable" release package (docs/research/2026-11-22-number-answers/RELEASE-BUILD.md, revision 10; D726, D758).

Each test names the design row it proves (§1 the closed set and the checks, §2 state × event, §6 the numbered tests). The stores are
real SQLite files on a temporary path; the only edits of code are the mutation-procedure scratch copies of §6 tests 12, 14, 19, 20
and 21, which insert a pause or a fault into a copy of the module and the command."""
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import release, service  # noqa: E402
from hivemind.views import store  # noqa: E402

COMMAND = ROOT / 'scripts' / 'release_build.py'
DAYS = ['2026-08-24', '2026-08-25', '2026-08-26']
ASSET_LABELS = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']
V1_CONDITIONS = ['FY2027 revenue is at least $400 billion.', 'FY2027 revenue is at least $350 billion and less than $400 billion.',
                 'FY2027 revenue is at least $300 billion and less than $350 billion.', 'FY2027 revenue is at least $250 billion and less than $300 billion.',
                 'FY2027 revenue is less than $250 billion.']
V1_BOUNDS = [(400e9, None), (350e9, 400e9), (300e9, 350e9), (250e9, 300e9), (None, 250e9)]
V1_REASONS = 'The first-half figure and the third-quarter guide support an estimate of about $390 billion for the year.'
V1_WHY = 'Moved up to the $350 billion to under $400 billion rung on the raised guide.'
V5_WHY = 'Spending of around $1 trillion in 2027 makes acceleration likely.'
V6_WHY = 'The revenue question now sits in the $350 billion to under $400 billion rung, which the rule would cut.'
CLOSING = 'due 2026-08-25, frozen on 2026-08-25 at rung 2 Bullish'
E6_ONE_LINE = 'Bullish confirmation would need firm orders, the author said.'       # the fixture's one genuine source use of a label word
E6_QUOTE = 'Bullish confirmation would require firm procurement commitments.'
REPORT_KEYS = {'ledger', 'items', 'as_of', 'counts', 'withheld_unresolved', 'data_bytes', 'export_seconds', 'check_seconds'}
MARKER = 'Forecast unavailable'                                     # D726's words, written here, not read from the module under test
NUMBER_KEYS = {'id', 'question', 'open', 'class', 'forecast', 'evidence'}
ANSWERED_KEYS = {'id', 'question', 'open', 'class', 'answers', 'answer', 'evidence'}
FIXTURE_COUNTS = {'questions': {'number': 5, 'event': 1, 'yes_no': 1}, 'evidence': 5, 'sources': 6, 'fields_compared': 101}
FIXTURE_DATA_BYTES = 3313
UNREADABLE = 'conditions not read as amounts: positions [1, 2, 3, 4, 5]'
FIXTURE_UNRESOLVED = [{'id': 'v3', 'reason': UNREADABLE, 'has_key': True}, {'id': 'v4', 'reason': UNREADABLE, 'has_key': False}]


def refused_with(call, message, kind=release.ReleaseRefused):
    """The call is refused with exactly this message (a refusal for another reason does not count)."""
    with pytest.raises(kind) as caught:
        call()
    assert str(caught.value) == message, (str(caught.value), message)


def stderr_line(result, line):
    assert line in result.stderr.splitlines(), (result.stderr, line)


def make_items(path, ids=('item-1', 'item-2', 'item-3')):
    conn = sqlite3.connect(path)
    conn.execute('create table items (input_id text primary key, title text, publisher text, publisher_type text, category text, publication_day text, source_uri text)')
    for n, input_id in enumerate(ids, 1):
        conn.execute('insert into items values (?,?,?,?,?,?,?)', (input_id, f'Article {n} on data-center spending', f'Publisher {n}', 'news', 'T1',
                                                                 DAYS[min(n, 3) - 1], f'https://example.com/article-{n}'))
    conn.commit()
    conn.close()
    return path


def five_rungs(conditions, bounds=None):
    return [dict(label=label, condition=condition, **({'lo': lo, 'hi': hi} if bounds else {}))
            for label, condition, (lo, hi) in zip(ASSET_LABELS, conditions, bounds or [(None, None)] * 5)]


def key(conn, view_id, measure, event_type='n/a'):
    store.insert(conn, 'view_keys', view_id=view_id, measure=measure, scope='NVIDIA', scope_key='nvidia', period_start='2026-02-01',
                 period_end='2027-01-31', basis='n/a', unit='USD', event_type=event_type, seq=1, scope_source='model', key_version=1)


def judge(conn, view_id, seq, rung, why, reasons='', implied=None):
    store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=f'item-{seq}', rung=rung, reasons=reasons, cited_evidence_json='[]',
                 cited_views_json='[]', pushes_json='[]', changed=1, why_changed=why, publication_day=DAYS[seq - 1], theme_pushes_json='[]',
                 reference=None, implied_outcome=implied)


def evidence(conn, evidence_id, view_id, seq, one_line, quote, sources):
    store.insert(conn, 'evidence', evidence_id=evidence_id, quote=quote, one_line=one_line, speaker='Publisher', original_who='NVIDIA',
                 original_day=DAYS[seq - 1], tier='party_statement', event_time=None, created_seq=seq, created_from_input=f'item-{seq}')
    store.insert(conn, 'evidence_links', evidence_id=evidence_id, view_id=view_id, seq=seq)
    for input_id, source_seq in sources:
        store.insert(conn, 'evidence_sources', evidence_id=evidence_id, input_id=input_id, category='T1', publication_day=DAYS[source_seq - 1], seq=source_seq)


def make_store(path):
    """§6 fixture: three completed days; a number question with bounds (v1), one whose conditions resolve without a key (v2), unresolved
    ones with a key (v3) and without (v4), a Yes/No question with numeric bounds (v5), an event (v6) and a closed number question (v7)."""
    conn = store.open_db(str(path))
    for seq, day in enumerate(DAYS, 1):
        store.insert(conn, 'processing_steps', input_id=f'item-{seq}', sequence_no=seq, step='handed_over', result='ok', publication_day=day)
        store.insert(conn, 'days_completed', day=day, seq=seq)
    common = dict(object_id='NVDA', object_kind='company', kind='asset', due_day='2027-02-25', year='2027', seq=1, input_id='item-1', created_at='2026-08-24T12:00:00Z')
    store.create_view(conn, view_id='v1', looks_at='NVIDIA revenue in FY2027', question='How much revenue will NVIDIA report for FY2027?', rungs=five_rungs(V1_CONDITIONS, V1_BOUNDS), **common)
    key(conn, 'v1', 'revenue')
    store.create_view(conn, view_id='v2', looks_at='NVIDIA FY2027 capital spending', question='How much will NVIDIA spend on capital in FY2027?',
                      rungs=[{'label': '看多', 'condition': '不低于4000亿美元'}, {'label': '看空', 'condition': '低于4000亿美元'}], **common)
    unreadable = ['Revenue is clearly strong.', 'Revenue is strong.', 'Revenue is flat.', 'Revenue is weak.', 'Revenue is clearly weak.']
    store.create_view(conn, view_id='v3', looks_at='NVIDIA gaming revenue', question='How much gaming revenue will NVIDIA report for FY2027?', rungs=five_rungs(unreadable), **common)
    key(conn, 'v3', 'segment_revenue')
    store.create_view(conn, view_id='v4', looks_at='NVIDIA auto revenue', question='How much automotive revenue will NVIDIA report for FY2027?', rungs=five_rungs(unreadable), **common)
    store.create_view(conn, view_id='v5', looks_at='Hyperscaler capex growth', question='Will hyperscaler capital spending growth accelerate in 2027?',
                      rungs=[{'label': 'Yes', 'condition': 'Growth above zero', 'lo': 0.0, 'hi': None}, {'label': 'No', 'condition': 'Growth at or below zero', 'lo': None, 'hi': 0.0}], **common)
    key(conn, 'v5', 'growth_rate')
    store.create_view(conn, view_id='v6', looks_at='US export restriction', question='Will the US adopt the chip export restriction by 2027-01-31?',
                      rungs=[{'label': 'Restriction adopted', 'condition': 'The rule is adopted'}, {'label': 'No restriction adopted', 'condition': 'The rule is not adopted'}], **common)
    key(conn, 'v6', 'policy_event', 'regulation')
    store.create_view(conn, view_id='v7', looks_at='NVIDIA Q2 revenue', question='How much revenue will NVIDIA report for Q2 FY2027?', rungs=five_rungs(V1_CONDITIONS, V1_BOUNDS), **common)
    key(conn, 'v7', 'revenue')
    judge(conn, 'v1', 1, 2, V1_WHY, V1_REASONS, 'About $390 billion')
    judge(conn, 'v5', 1, 1, V5_WHY)
    judge(conn, 'v6', 1, 2, V6_WHY)
    judge(conn, 'v7', 1, 2, 'Held at the Bullish rung.')
    store.insert(conn, 'view_switches', view_id='v7', open=0, reason=CLOSING, by_whom='pull', after_seq=2)
    evidence(conn, 'e1', 'v1', 1, 'NVIDIA reported $164 billion of revenue in the first half.', 'The company generated $164 billion in the first six months.', [('item-1', 1), ('item-3', 3)])
    evidence(conn, 'e2', 'v1', 3, 'Morningstar estimates $361 billion of revenue for the year.', 'We estimate it will be $361 billion in fiscal 2027.', [('item-3', 3)])
    evidence(conn, 'e3', 'v1', 1, 'An early report put spending at $90 billion.', 'Spending was $90 billion, the report said.', [('item-1', 1)])
    evidence(conn, 'e4', 'v1', 2, 'A corrected report put spending at $95 billion.', 'Spending was $95 billion, the corrected report said.', [('item-2', 2)])
    store.insert(conn, 'replacements', old_evidence_id='e3', new_evidence_id='e4', said_day=DAYS[1], seq=2)
    evidence(conn, 'e5', 'v6', 1, 'Officials said the export rule is under review.', 'The rule is under review, officials said.', [('item-1', 1)])
    evidence(conn, 'e6', 'v5', 1, E6_ONE_LINE, E6_QUOTE, [('item-2', 1)])
    conn.commit()
    conn.close()
    return path


@pytest.fixture
def stores(tmp_path):
    return make_store(tmp_path / 'views.sqlite'), make_items(tmp_path / 'items.sqlite')


def export(stores, as_of=None):
    views_db, items_db = service.open_ledger(str(stores[0])), store.open_read_only(str(stores[1]))
    try:
        return release.release_export(views_db, items_db, as_of)
    finally:
        views_db.close()
        items_db.close()


def strings(value):
    """Every decoded string in the package (keys excluded)."""
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    return [value] if isinstance(value, str) else []


def by_id(data):
    return {q['id']: q for q in data['questions']}


def run(*args, cwd=None, timeout=120):
    return subprocess.run([sys.executable, str(COMMAND), *map(str, args)], capture_output=True, text=True, cwd=cwd,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, timeout=timeout)


def build_package(stores, out, as_of=None):
    views_db, items_db = service.open_ledger(str(stores[0])), store.open_read_only(str(stores[1]))
    try:
        data = release.release_export(views_db, items_db, as_of)
        staged = release.stage(out)
        release.write_package(data, staged)
        release.check_package(staged, views_db, items_db, expected_as_of=data['as_of'])
        release.publish(staged, out)
        return data
    finally:
        views_db.close()
        items_db.close()


def rewrite_data(package, data):
    """A copy of the package's data with its page and manifest made from it again, so every other check still passes."""
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    page = release.render_page(payload)
    (package / release.DATA_FILE).write_bytes(payload)
    (package / release.PAGE_FILE).write_bytes(page)
    manifest = json.loads((package / release.MANIFEST_FILE).read_text())
    manifest.update(as_of=data['as_of'], data_sha256=hashlib.sha256(payload).hexdigest(), page_sha256=hashlib.sha256(page).hexdigest())
    (package / release.MANIFEST_FILE).write_text(json.dumps(manifest))


def check(stores, package):
    """The counts of `check_package` with the stores."""
    views_db, items_db = service.open_ledger(str(stores[0])), store.open_read_only(str(stores[1]))
    try:
        return release.check_package(package, views_db, items_db)[0]
    finally:
        views_db.close()
        items_db.close()


# ---------- §6 tests 1–8: the export


def test_1_every_object_holds_exactly_its_record_types_keys(stores):
    """§1 ALLOWED, §6 test 1: the export passes the closed-set check; one added key fails it."""
    data = export(stores)
    counts = release.check_export(data)
    assert counts['questions'] == {'number': 5, 'event': 1, 'yes_no': 1} and counts['evidence'] == 5
    assert set(by_id(data)['v1']) == NUMBER_KEYS and set(by_id(data)['v6']) == ANSWERED_KEYS
    assert (data['format'], data['allow_list']) == ('hivemind-release/2', 'release-allow-list/1')     # RELEASE-PAGE.md's identifiers, literal
    by_id(data)['v1']['condition'] = V1_CONDITIONS[1]
    refused_with(lambda: release.check_export(data), "question 0: keys off the allow-list ['condition'], missing []")


def test_2_number_question_carries_only_the_marker_and_its_evidence(stores):
    """§6 test 2 (D726): no rung label, condition, reason, explanation or implied outcome of v1 reaches any decoded field."""
    data = export(stores)
    v1 = by_id(data)['v1']
    assert v1['class'] == 'number' and v1['forecast'] == MARKER
    assert [e['id'] for e in v1['evidence']] == ['e1', 'e2', 'e4']
    texts, own = strings(data), strings(v1)
    for forbidden in [*V1_CONDITIONS, V1_REASONS, V1_WHY, 'About $390 billion']:
        assert not any(forbidden in text for text in texts), forbidden
    for label in ASSET_LABELS:                        # the selected label "Bullish" included; v1's own fields hold none
        assert not any(label in text for text in own), label
    allowed = {'Bullish': {('v5', 'e6', 'one_line'): E6_ONE_LINE, ('v5', 'e6', 'quote'): E6_QUOTE}}   # the fixture's genuine wording, by location
    for label in ASSET_LABELS:
        found = {(q['id'], e['id'], name): e[name] for q in data['questions'] for e in q['evidence'] for name in ('one_line', 'quote') if label in e[name]}
        found.update({(q['id'], None, key): text for q in data['questions'] for key, value in q.items() if key != 'evidence'
                      for text in strings(value) if label in text})
        assert found == allowed.get(label, {}), (label, found)


def test_3_identity_branches_and_the_unresolved_report(stores):
    """§1 question_class, §6 test 3: a condition-only ladder that resolves and unresolved ladders with and without a key are all
    number questions; only the unresolved two are listed."""
    data = export(stores)
    assert {q['id']: q['class'] for q in data['questions']} == {'v1': 'number', 'v2': 'number', 'v3': 'number', 'v4': 'number', 'v5': 'yes_no', 'v6': 'event', 'v7': 'number'}
    views_db = service.open_ledger(str(stores[0]))
    try:
        listed = {entry['id']: entry['has_key'] for entry in release.withheld_unresolved(views_db, data)}
    finally:
        views_db.close()
    assert listed == {'v3': True, 'v4': False}


def test_4_yes_no_with_numeric_bounds_keeps_its_label_not_its_explanation(stores):
    """§6 test 4 (§4 a): v5 is Yes/No with its answer; its explanation quoting $1 trillion is absent."""
    data = export(stores)
    v5 = by_id(data)['v5']
    assert (v5['class'], v5['answers'], v5['answer']) == ('yes_no', ['Yes', 'No'], 'Yes')
    assert not any('$1 trillion' in text for text in strings(data))


def test_5_event_keeps_its_labels_not_its_explanation(stores):
    """§6 test 5: an event with the served ledger's labels keeps them; its explanation quoting v1's rung is absent."""
    data = export(stores)
    v6 = by_id(data)['v6']
    assert (v6['class'], v6['answers'], v6['answer']) == ('event', ['Restriction adopted', 'No restriction adopted'], 'No restriction adopted')
    assert not any(V6_WHY in text for text in strings(data))


def test_6_legacy_ledger_without_a_key_table_reads_chinese_yes_no(tmp_path):
    """§6 test 6, §2 legacy row: no view_keys table; 是/否 labels are Yes/No."""
    path = tmp_path / 'legacy.sqlite'
    conn = store.open_db(str(path))
    conn.execute('drop table view_keys')
    store.insert(conn, 'processing_steps', input_id='item-1', sequence_no=1, step='handed_over', result='ok', publication_day=DAYS[0])
    store.insert(conn, 'days_completed', day=DAYS[0], seq=1)
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='Shipments', question='会开始量产出货吗？',
                      due_day='2026-12-31', year='2026', rungs=[{'label': '是', 'condition': '开始出货'}, {'label': '否', 'condition': '未开始出货'}],
                      seq=1, input_id='item-1', created_at='2026-08-24T12:00:00Z')
    judge(conn, 'v1', 1, 1, '已确认出货。')
    conn.commit()
    conn.close()
    data = export((path, make_items(tmp_path / 'items.sqlite')))
    assert (data['questions'][0]['class'], data['questions'][0]['answer']) == ('yes_no', '是')


def test_7_closed_question_shows_closed_without_its_reason(stores):
    """§6 test 7, §2 closing row: v7 is closed at 08-25; the closing reason naming its rung is absent."""
    assert by_id(export(stores, DAYS[0]))['v7']['open'] is True
    data = export(stores)
    assert by_id(data)['v7']['open'] is False
    assert not any(CLOSING in text or 'frozen on' in text for text in strings(data))


def test_8_replacements_and_sources_follow_the_day_and_missing_items_refuse(stores, tmp_path):
    """§6 test 8, §2 replacement and source rows: e3 is in force until its replacement on 08-25; e1's second source appears on 08-26;
    a visible source with no item is refused."""
    early, late = by_id(export(stores, DAYS[0]))['v1'], by_id(export(stores))['v1']
    assert [e['id'] for e in early['evidence']] == ['e1', 'e3']
    assert [e['id'] for e in late['evidence']] == ['e1', 'e2', 'e4']
    assert [s['day'] for s in early['evidence'][0]['sources']] == [DAYS[0]]
    assert [s['day'] for s in late['evidence'][0]['sources']] == [DAYS[0], DAYS[2]]
    short = make_items(tmp_path / 'short.sqlite', ids=('item-1', 'item-2'))
    refused_with(lambda: export((stores[0], short)), 'evidence e1: source item item-3 is not in the items database')


# ---------- §6 tests 9, 10, 13, 15, 16: the package and the origin check


def test_9_package_files_hash_and_manifest(stores, tmp_path):
    """§1 check_package, §6 test 9."""
    out = tmp_path / 'release'
    data = build_package(stores, out)
    assert check(stores, out)['fields_compared'] > 0
    files = "not exactly ['index.html', 'manifest.json', 'release-data.json']"
    variants = {
        'foreign file': (lambda p: (p / 'notes.txt').write_text('x'), lambda p: f"{p}: holds ['index.html', 'manifest.json', 'notes.txt', 'release-data.json'], {files}"),
        'subdirectory': (lambda p: (p / 'extra').mkdir(), lambda p: f"{p}: holds ['extra', 'index.html', 'manifest.json', 'release-data.json'], {files}"),
        'missing page': (lambda p: (p / 'index.html').unlink(), lambda p: f"{p}: holds ['manifest.json', 'release-data.json'], {files}"),
        'changed byte': (lambda p: (p / release.DATA_FILE).write_bytes((p / release.DATA_FILE).read_bytes().replace(b'Morningstar', b'Morningstan')),
                         lambda p: 'the manifest sha256 does not match the data file'),
        'manifest prose': (lambda p: (p / release.MANIFEST_FILE).write_text(json.dumps({**json.loads((p / release.MANIFEST_FILE).read_text()), 'note': 'About $390 billion'})),
                           lambda p: "the manifest: keys off the allow-list ['note'], missing []"),
        'manifest day': (lambda p: (p / release.MANIFEST_FILE).write_text(json.dumps({**json.loads((p / release.MANIFEST_FILE).read_text()), 'as_of': DAYS[0]})),
                         lambda p: f"the manifest as_of '{DAYS[0]}' differs from the data '{DAYS[2]}'"),
    }
    for name, (damage, message) in variants.items():
        copy = tmp_path / f'copy-{name.replace(" ", "-")}'
        shutil.copytree(out, copy)
        damage(copy)
        refused_with(lambda: check(stores, copy), message(copy))
    with pytest.raises(FileExistsError):
        staged = release.stage(out)
        release.write_package(data, staged)
        release.publish(staged, out)
    (tmp_path / '.other.staging-x').mkdir()            # another build's debris blocks nothing
    assert build_package(stores, tmp_path / 'other')


def test_10_origin_check_derives_everything_from_the_store(stores, tmp_path):
    """§1 check_origins, §6 test 10: a forecast in a summary, a class swap, duplicates, another order and a future day are each
    refused."""
    out = tmp_path / 'release'
    data = build_package(stores, out)
    cases = {}
    forged = json.loads(json.dumps(data))
    by_id(forged)['v1']['evidence'][1]['one_line'] = 'About $390 billion'
    cases['forecast in a summary'] = (forged, 'question v1.evidence e2.one_line: differs from the store')
    swapped = json.loads(json.dumps(data))
    v5 = by_id(swapped)['v5']
    for name in ('answers', 'answer'):
        del v5[name]
    v5.update({'class': 'number', 'forecast': MARKER})
    cases['class swap'] = (swapped, 'question v5: fields differ from the store')
    doubled = json.loads(json.dumps(data))
    doubled['questions'].insert(1, doubled['questions'][0])
    cases['duplicate question'] = (doubled, 'the questions differ from the store: 8 entries where the store has 7')
    repeated = json.loads(json.dumps(data))
    by_id(repeated)['v1']['evidence'].append(by_id(repeated)['v1']['evidence'][0])
    cases['duplicate evidence'] = (repeated, 'question v1.evidence: 4 entries where the store has 3')
    future = json.loads(json.dumps(data))
    future['as_of'] = '2026-08-27'
    cases['future day'] = (future, 'day not completed: 2026-08-27 is after the last completed day 2026-08-26')
    reordered = json.loads(json.dumps(data))
    reordered['questions'][0], reordered['questions'][1] = reordered['questions'][1], reordered['questions'][0]
    cases['reordered questions'] = (reordered, 'the questions or their order differ from the store')
    swapped = json.loads(json.dumps(data))
    pieces = by_id(swapped)['v1']['evidence']
    pieces[0], pieces[1] = pieces[1], pieces[0]
    cases['reordered evidence'] = (swapped, 'question v1.evidence e1.id: differs from the store')
    for name, (changed, reason) in cases.items():
        copy = tmp_path / f'copy-{name.replace(" ", "-")}'
        shutil.copytree(out, copy)
        rewrite_data(copy, changed)
        refused_with(lambda: check(stores, copy), reason, ValueError)


def test_10_legacy_store_without_completed_days_passes_one_date_rule(tmp_path):
    """§2 legacy row, §6 test 10: no completed days and no processing steps; an explicit day after the last judgement builds and the
    same day passes a later check."""
    path = tmp_path / 'legacy.sqlite'
    conn = store.open_db(str(path))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='Shipments', question='Will shipments begin?',
                      due_day='2026-12-31', year='2026', rungs=[{'label': 'Yes', 'condition': 'Begin'}, {'label': 'No', 'condition': 'Do not begin'}],
                      seq=1, input_id='item-1', created_at='2026-08-24T12:00:00Z')
    judge(conn, 'v1', 1, 1, 'Shipments confirmed.')
    conn.commit()
    conn.close()
    pair = (path, make_items(tmp_path / 'items.sqlite'))
    build_package(pair, tmp_path / 'release', '2026-09-30')
    assert check(pair, tmp_path / 'release')['questions'] == {'number': 0, 'event': 0, 'yes_no': 0}


def test_13_check_refuses_a_missing_item_even_when_the_package_omits_its_source(stores, tmp_path):
    """§6 test 13: the items copy lacks item-3; the package copy drops every item-3 source, keeping e2 with none, its hash refreshed.
    A checker that silently skips a missing item accepts this pair; the release refuses it, naming the item."""
    out = tmp_path / 'release'
    data = build_package(stores, out)
    short = make_items(tmp_path / 'short.sqlite', ids=('item-1', 'item-2'))
    copy = tmp_path / 'copy'
    shutil.copytree(out, copy)
    for piece in by_id(data)['v1']['evidence']:      # e1 loses its item-3 source, e2 keeps its record with no source: what a checker
        piece['sources'] = [s for s in piece['sources'] if s['uri'] != 'https://example.com/article-3']   # that drops missing items expects
    rewrite_data(copy, data)
    refused_with(lambda: check((stores[0], short), copy), 'evidence e1: source item item-3 is not in the items database')


def test_15_symbolic_links_and_repeated_member_names_are_refused(stores, tmp_path):
    """§6 test 15: a symbolic link, a repeated member name and a named pipe are refused (the pipe without waiting)."""
    out = tmp_path / 'release'
    build_package(stores, out)
    linked = tmp_path / 'linked'
    shutil.copytree(out, linked)
    (tmp_path / 'outside.json').write_bytes((linked / release.DATA_FILE).read_bytes())
    (linked / release.DATA_FILE).unlink()
    (linked / release.DATA_FILE).symlink_to(tmp_path / 'outside.json')
    refused_with(lambda: check(stores, linked), f'{linked}/release-data.json: not a regular file')
    repeated = tmp_path / 'repeated'
    shutil.copytree(out, repeated)
    raw = (repeated / release.DATA_FILE).read_bytes()
    genuine = b'"one_line":"Morningstar estimates $361 billion of revenue for the year."'
    assert raw.count(genuine) == 1
    payload = raw.replace(genuine, b'"one_line":"About $390 billion",' + genuine)
    (repeated / release.DATA_FILE).write_bytes(payload)
    manifest = json.loads((repeated / release.MANIFEST_FILE).read_text())
    manifest['data_sha256'] = hashlib.sha256(payload).hexdigest()
    (repeated / release.MANIFEST_FILE).write_text(json.dumps(manifest))
    refused_with(lambda: check(stores, repeated), "a JSON member name repeats: ['one_line']")
    piped = tmp_path / 'piped'
    shutil.copytree(out, piped)
    (piped / release.DATA_FILE).unlink()
    os.mkfifo(piped / release.DATA_FILE)
    result = run('check', piped, '--ledger', stores[0], '--items', stores[1], timeout=30)      # a blocking open would hang here
    assert result.returncode == 1
    stderr_line(result, f'refused: ReleaseRefused: {piped}/release-data.json: not a regular file')


def test_16_the_day_must_be_valid_and_canonical(stores):
    """§2 day rows, §6 test 16."""
    refused_with(lambda: export(stores, '2026-08-99'), "not a day: '2026-08-99'")
    with pytest.raises(release.ReleaseRefused) as caught:      # Python 3.10 refuses the spelling as a day; 3.11+ reads it, and the canonical rule refuses it
        export(stores, '20260825')
    assert str(caught.value) in ("not a day: '20260825'", "a day must be written YYYY-MM-DD: '20260825'")
    assert [e['id'] for e in by_id(export(stores, '2026-08-25'))['v1']['evidence']] == ['e1', 'e4']
    views_db = service.open_ledger(str(stores[0]))
    try:
        refused_with(lambda: release.resolve(views_db, '2026-08-27'), 'day not completed: 2026-08-27 is after the last completed day 2026-08-26', service.BoundNotCompleted)
    finally:
        views_db.close()


def test_16_a_day_before_the_first_question_gives_an_empty_package(stores):
    """§2 row "valid day before the first visible question", §6 test 16: the store's questions open on 08-24."""
    data = export(stores, '2026-08-23')
    assert data['as_of'] == '2026-08-23' and data['questions'] == []


# ---------- §6 tests 11, 17, 18: the command


def test_11_command_end_to_end_with_check_statuses(stores, tmp_path):
    """§1 the builder and check, §6 test 11."""
    out = tmp_path / 'release'
    built = run('build', '--ledger', stores[0], '--items', stores[1], '--out', out)
    assert built.returncode == 0, built.stderr
    report = out.with_name('release.report.json')
    written = json.loads(report.read_text())
    assert set(written) == REPORT_KEYS and (written['ledger'], written['items'], written['as_of']) == (str(stores[0]), str(stores[1]), DAYS[2])
    assert written['counts'] == FIXTURE_COUNTS and written['withheld_unresolved'] == FIXTURE_UNRESOLVED and written['data_bytes'] == FIXTURE_DATA_BYTES
    assert written['export_seconds'] >= 0 and written['check_seconds'] >= 0
    occupied = run('check', out, '--ledger', stores[0], '--items', stores[1])
    assert occupied.returncode == 2 and occupied.stdout.startswith(f'passes {out}: ')
    report.unlink()
    fresh = run('check', out, '--ledger', stores[0], '--items', stores[1])
    assert fresh.returncode == 0 and report.exists() and json.loads(report.read_text())['export_seconds'] is None


def test_17_database_error_leaves_nothing_and_a_retry_succeeds(stores, tmp_path):
    """§2 database-error row, §6 test 17."""
    broken = tmp_path / 'broken.sqlite'
    sqlite3.connect(broken).execute('create table other (x)').connection.commit()
    out = tmp_path / 'release'
    failed = run('build', '--ledger', stores[0], '--items', broken, '--out', out)
    assert failed.returncode == 1
    stderr_line(failed, 'refused: OperationalError: no such table: items')
    assert not out.exists() and not list(tmp_path.glob('.release.staging-*'))
    assert run('build', '--ledger', stores[0], '--items', stores[1], '--out', out).returncode == 0


def test_18_no_report_ever_replaces_an_input(stores, tmp_path):
    """§1 publish_report, §6 test 18: the report name is the items file itself, a symbolic link to it, and (on a case-insensitive
    volume) a case-variant name of it."""
    items_hash = hashlib.sha256(stores[1].read_bytes()).hexdigest()
    same = tmp_path / 'same.report.json'
    shutil.copyfile(stores[1], same)
    refused = run('build', '--ledger', stores[0], '--items', same, '--out', tmp_path / 'same')
    assert refused.returncode == 1 and hashlib.sha256(same.read_bytes()).hexdigest() == items_hash
    out = tmp_path / 'pkg'
    assert run('build', '--ledger', stores[0], '--items', stores[1], '--out', out).returncode == 0
    report = tmp_path / 'pkg.report.json'
    report.unlink()
    report.symlink_to(stores[1])
    linked = run('check', out, '--ledger', stores[0], '--items', stores[1])
    assert linked.returncode == 2 and hashlib.sha256(stores[1].read_bytes()).hexdigest() == items_hash
    report.unlink()
    variant = tmp_path / 'PKG.REPORT.JSON'
    shutil.copyfile(stores[1], variant)
    if report.exists():                                  # a case-insensitive volume: the variant is the report name
        checked = run('check', out, '--ledger', stores[0], '--items', variant)
        assert checked.returncode == 2 and hashlib.sha256(variant.read_bytes()).hexdigest() == items_hash


# ---------- §6 tests 12, 14, 19, 20, 21: scratch copies of the command (the AGENTS §4 mutation procedure)


def scratch(tmp_path, edits):
    """A copy of the package and the command with text edits applied; each edit must match once."""
    root = tmp_path / 'scratch'
    shutil.copytree(ROOT / 'src' / 'hivemind', root / 'src' / 'hivemind', ignore=shutil.ignore_patterns('__pycache__'))
    (root / 'scripts').mkdir()
    shutil.copy(COMMAND, root / 'scripts' / 'release_build.py')
    for relative, old, new in edits:
        path = root / relative
        text = path.read_text()
        assert text.count(old) == 1, ('scratch anchor', relative, old)
        path.write_text(text.replace(old, new))
    return root / 'scripts' / 'release_build.py'


def pause_code(signals, name, indent='        '):
    """Code that signals it has paused and waits for the test's resume file, ending at `indent` for the line it precedes."""
    return (f"__import__('pathlib').Path({str(signals / ('paused-' + name))!r}).touch()\n"
            f"{indent}while not __import__('pathlib').Path({str(signals / ('resume-' + name))!r}).exists(): __import__('time').sleep(0.02)\n{indent}")


def run_paused(command, args, signals, name, action):
    process = subprocess.Popen([sys.executable, str(command), *map(str, args)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    deadline = time.time() + 60
    while not (signals / f'paused-{name}').exists():
        assert process.poll() is None and time.time() < deadline, process.communicate()
        time.sleep(0.02)
    action()
    (signals / f'resume-{name}').touch()
    out, err = process.communicate(timeout=120)
    return process.returncode, out, err


FAULT = ("evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources})",
         "evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources, "
         "'one_line': views_db.execute('select why_changed from judgements where view_id=? order by judgement_id desc limit 1', (view_id,)).fetchone()['why_changed'] if view_id == 'v1' else piece['one_line']})")
STAGED_CHECK = ("counts, data, size = release.check_package(staged, views_db, items_db, expected_as_of=bound)", "counts, size = release.check_export(data), 0")


def test_12_the_staged_check_is_what_stops_a_writer_fault(stores, tmp_path):
    """§6 test 12: with a writer fault the command refuses and leaves nothing; with the fault and no staged check the bad package is
    published, so the staged check is what prevents it."""
    faulty = scratch(tmp_path / 'a', [('src/hivemind/release.py', *FAULT)])
    out = tmp_path / 'release'
    refused = subprocess.run([sys.executable, str(faulty), 'build', '--ledger', stores[0], '--items', stores[1], '--out', out], capture_output=True, text=True)
    assert refused.returncode == 1
    stderr_line(refused, 'refused: ReleaseRefused: question v1.evidence e1.one_line: differs from the store')
    assert not out.exists() and not list(tmp_path.glob('.release.staging-*'))
    unguarded = scratch(tmp_path / 'b', [('src/hivemind/release.py', *FAULT), ('scripts/release_build.py', *STAGED_CHECK)])
    published = subprocess.run([sys.executable, str(unguarded), 'build', '--ledger', stores[0], '--items', stores[1], '--out', out], capture_output=True, text=True)
    assert published.returncode == 0, published.stderr
    assert V1_WHY in (out / release.DATA_FILE).read_text()


def test_14_publication_never_replaces_or_removes_another_folder(stores, tmp_path):
    """§1 publish, §2 rows on an occupied --out and two builds, §6 test 14."""
    data = export(stores)
    out = tmp_path / 'release'
    first, second = release.stage(out), release.stage(out)
    release.write_package(data, first)
    release.write_package(data, second)
    release.publish(first, out)
    with pytest.raises(FileExistsError):
        release.publish(second, out)
    assert second.exists() and check(stores, out)['fields_compared'] > 0
    other = tmp_path / 'other'
    staged = release.stage(other)
    release.write_package(data, staged)
    other.mkdir()
    with pytest.raises(FileExistsError):
        release.publish(staged, other)
    assert other.is_dir() and not any(other.iterdir())
    early = tmp_path / 'early'
    early.mkdir()
    assert run('build', '--ledger', stores[0], '--items', stores[1], '--out', early).returncode == 1 and early.is_dir()

    signals = tmp_path / 'signals'
    signals.mkdir()
    paused = scratch(tmp_path / 'late', [('scripts/release_build.py', 'release.publish(staged, out)', pause_code(signals, 'publish') + 'release.publish(staged, out)')])
    late = tmp_path / 'late-out'
    holder = {}

    def occupy():
        late.mkdir()
        holder['identity'] = (late.stat().st_dev, late.stat().st_ino)
    code, _, err = run_paused(paused, ['build', '--ledger', stores[0], '--items', stores[1], '--out', late], signals, 'publish', occupy)
    assert code == 1 and f"refused: FileExistsError: [Errno 17] File exists: '{late}'" in err.splitlines()
    assert (late.stat().st_dev, late.stat().st_ino) == holder['identity'] and not any(late.iterdir())
    assert not list(tmp_path.glob('.late-out.staging-*'))

    after = scratch(tmp_path / 'after', [('scripts/release_build.py', '        release.publish(staged, out)\n',
                                          f"        release.publish(staged, out)\n        {pause_code(signals, 'freed')}staged.mkdir(); (staged / 'marker').write_text('mine')\n")])
    done = tmp_path / 'after-out'
    code, _, err = run_paused(after, ['build', '--ledger', stores[0], '--items', stores[1], '--out', done], signals, 'freed', lambda: None)
    assert code == 0, err
    markers = list(tmp_path.glob('.after-out.staging-*/marker'))
    assert len(markers) == 1 and markers[0].read_text() == 'mine'


def test_19_a_report_name_taken_during_the_build_survives(stores, tmp_path):
    """§2 report rows, §6 test 19."""
    signals = tmp_path / 'signals'
    signals.mkdir()
    paused = scratch(tmp_path, [('scripts/release_build.py', '    return write_report(summary, report)\n\n\ndef check',
                                 f"    {pause_code(signals, 'report', indent='    ')}return write_report(summary, report)\n\n\ndef check")])
    out = tmp_path / 'release'
    marker = tmp_path / 'release.report.json'
    code, _, err = run_paused(paused, ['build', '--ledger', stores[0], '--items', stores[1], '--out', out], signals, 'report', lambda: marker.write_text('occupied'))
    assert code == 2 and marker.read_text() == 'occupied'
    assert any(line.startswith('report not written ([Errno 17] File exists: ') and line.endswith(f"-> '{marker}'); run check to write it") for line in err.splitlines()), err
    checked = run('check', out, '--ledger', stores[0], '--items', stores[1])
    assert checked.returncode == 2 and checked.stdout.startswith(f'passes {out}: ') and marker.read_text() == 'occupied'


def test_20_a_temporary_file_left_after_the_link_still_counts_as_published(stores, tmp_path):
    """§1 publish_report, §6 test 20."""
    command = scratch(tmp_path, [('src/hivemind/release.py', '    try:\n        os.unlink(temporary)\n    except OSError:',
                                  "    try:\n        raise PermissionError('test: cannot remove')\n    except OSError:")])
    out = tmp_path / 'release'
    result = subprocess.run([sys.executable, str(command), 'build', '--ledger', stores[0], '--items', stores[1], '--out', out], capture_output=True, text=True)
    leftovers = list(tmp_path.glob('.release.report.json.*'))
    assert result.returncode == 0 and len(leftovers) == 1
    stderr_line(result, f'report published; its temporary file {leftovers[0]} could not be removed')
    assert json.loads(out.with_name('release.report.json').read_text())['as_of'] == DAYS[2]
    assert list(tmp_path.glob('.release.report.json.*'))


def test_21_check_that_cannot_write_its_report_exits_2(stores, tmp_path):
    """§1 check's statuses, §6 test 21."""
    out = tmp_path / 'release'
    build_package(stores, out)
    command = scratch(tmp_path, [('src/hivemind/release.py', "    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f'.{path.name}.')",
                                  "    raise PermissionError('test: cannot create')")])
    result = subprocess.run([sys.executable, str(command), 'check', out, '--ledger', stores[0], '--items', stores[1]], capture_output=True, text=True)
    assert result.returncode == 2 and result.stdout.startswith(f'passes {out}: ')
    stderr_line(result, 'report not written (test: cannot create); run check to write it')
    printed = json.loads(result.stdout[result.stdout.index('\n{') + 1:])    # the whole report, printed on its own lines, though not written
    assert set(printed) == REPORT_KEYS and (printed['ledger'], printed['items'], printed['as_of']) == (str(stores[0]), str(stores[1]), DAYS[2])
    assert printed['counts'] == FIXTURE_COUNTS and printed['withheld_unresolved'] == FIXTURE_UNRESOLVED and printed['data_bytes'] == FIXTURE_DATA_BYTES
    assert printed['export_seconds'] is None and printed['check_seconds'] >= 0


# ---------- council 75: key visibility, text fields, store paths, the writer's own refusal


def test_22_a_key_written_after_the_day_does_not_reclassify_it(stores, tmp_path):
    """§1 question_class (council 75): a question with no key on 08-24 that gains an event key on 08-25 stays a number question in
    the 08-24 package."""
    conn = store.open_db(str(stores[0]))
    store.create_view(conn, view_id='v8', looks_at='NVIDIA buyback', question='How large a buyback will NVIDIA announce by 2027?',
                      rungs=[{'label': 'Above the estimate', 'condition': 'At least $60 billion'}, {'label': 'Below the estimate', 'condition': 'Less than $60 billion'}],
                      object_id='NVDA', object_kind='company', kind='asset', due_day='2027-01-31', year='2027', seq=1, input_id='item-1', created_at='2026-08-24T12:00:00Z')
    judge(conn, 'v8', 1, 1, 'The estimate is about $70 billion.')
    store.insert(conn, 'view_keys', view_id='v8', measure='event', scope='NVIDIA', scope_key='nvidia', period_start='2026-02-01', period_end='2027-01-31',
                 basis='n/a', unit='n/a', event_type='other', seq=2, scope_source='model', key_version=1)
    conn.commit()
    conn.close()
    early, late = by_id(export(stores, DAYS[0]))['v8'], by_id(export(stores, DAYS[1]))['v8']
    assert (early['class'], early.get('forecast')) == ('number', MARKER)
    assert (late['class'], late['answer']) == ('event', 'Above the estimate')
    out = tmp_path / 'early'
    build_package(stores, out, DAYS[0])
    assert by_id(release.read_data(out))['v8']['class'] == 'number'


EVIDENCE_COLUMNS = {'one_line': 'one_line', 'quote': 'quote', 'tier': 'tier', 'speaker': 'speaker', 'original_who': 'original_who', 'original_day': 'original_day'}
SOURCE_COLUMNS = {'title': ('items', 'title'), 'publisher': ('items', 'publisher'), 'uri': ('items', 'source_uri'), 'day': ('sources', 'publication_day')}


@pytest.mark.parametrize('field', [*EVIDENCE_COLUMNS, *SOURCE_COLUMNS])
def test_23_every_evidence_and_source_text_field_must_be_text(tmp_path, field):
    """§1 check_export (council 75): a null in any of the ten text fields the closed set requires is refused, at the writer."""
    views, items = make_store(tmp_path / 'views.sqlite'), make_items(tmp_path / 'items.sqlite', ids=('item-1', 'item-2', 'item-3', 'item-9'))
    conn = store.open_db(str(views))
    values = dict(evidence_id='e7', quote='Officials said the rule would be published.', one_line='Officials expect the rule.', speaker='Publisher',
                  original_who='Officials', original_day=DAYS[0], tier='party_statement', event_time=None, created_seq=1, created_from_input='item-9')
    if field in EVIDENCE_COLUMNS:
        values[EVIDENCE_COLUMNS[field]] = None
    store.insert(conn, 'evidence', **values)
    store.insert(conn, 'evidence_links', evidence_id='e7', view_id='v6', seq=1)
    store.insert(conn, 'evidence_sources', evidence_id='e7', input_id='item-9', category='T1',
                 publication_day=None if field == 'day' else DAYS[0], seq=1)
    conn.commit()
    conn.close()
    if field in SOURCE_COLUMNS and SOURCE_COLUMNS[field][0] == 'items':
        items_conn = sqlite3.connect(items)
        items_conn.execute(f"update items set {SOURCE_COLUMNS[field][1]} = null where input_id = 'item-9'")
        items_conn.commit()
        items_conn.close()
    where = 'question v6 evidence e7' + ('' if field in EVIDENCE_COLUMNS else ' source')
    refused_with(lambda: export((views, items)), f'{where}: {field} is not text')


def test_24_a_store_path_with_uri_syntax_is_refused(stores, tmp_path):
    """§1 store_path (councils 75, 75b): a path holding a character the SQLite URI opener decodes is refused before anything is opened;
    an accepted path is returned resolved, so the opener does not resolve a link a second time."""
    odd = tmp_path / 'a%2Db'
    odd.mkdir()
    shutil.copyfile(stores[0], odd / 'views.sqlite')
    message = f"{odd / 'views.sqlite'}: a store path may not contain ['%'], which the SQLite opener reads as URI syntax"
    refused_with(lambda: release.store_path(odd / 'views.sqlite'), message)
    result = run('build', '--ledger', odd / 'views.sqlite', '--items', stores[1], '--out', tmp_path / 'release')
    assert result.returncode == 1 and not (tmp_path / 'release').exists()
    stderr_line(result, f'refused: ReleaseRefused: {message}')
    assert release.store_path(stores[0]) == os.path.realpath(stores[0])
    link = tmp_path / 'link.sqlite'
    link.symlink_to(stores[0])
    assert release.store_path(link) == os.path.realpath(stores[0])          # the opener is given the target, with nothing left to follow


DRIVER = """import sys
sys.path.insert(0, sys.argv[1])
from hivemind import release, service
from hivemind.views import store
views, items = service.open_ledger(sys.argv[2]), store.open_read_only(sys.argv[3])
try:
    data = release.release_export(views, items)
    print('returned', sorted(data['questions'][0]))
except release.ReleaseRefused as error:
    print('refused', error)
"""
WRITER_FAULT = ("                record['forecast'] = FORECAST_UNAVAILABLE\n            else:\n                record['answers'] = labels\n                record['answer'] = _answer(",
                "                record['forecast'] = FORECAST_UNAVAILABLE\n                record['condition'] = 'FY2027 revenue is at least $350 billion'\n            else:\n"
                "                record['answers'] = labels\n                record['answer'] = _answer(")
SELF_CHECK = ("    check_export(data)\n    return data\n", "    return data\n")


def test_25_the_writer_refuses_its_own_off_list_field(stores, tmp_path):
    """§1 release_export (AGENTS §3, council 75), the mutation pair: a writer fault adding `condition` is refused inside
    `release_export`; with the writer's own check removed, the off-list field is returned."""
    driver = tmp_path / 'driver.py'
    driver.write_text(DRIVER)
    for name, edits, expected in (('fault', [WRITER_FAULT], 'refused'), ('unchecked', [WRITER_FAULT, SELF_CHECK], 'returned')):
        command = scratch(tmp_path / name, [('src/hivemind/release.py', *edit) for edit in edits])
        result = subprocess.run([sys.executable, str(driver), str(command.parents[1] / 'src'), str(stores[0]), str(stores[1])], capture_output=True, text=True,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        assert result.stdout.startswith(expected), (name, result.stdout, result.stderr)
        if name == 'unchecked':
            assert result.stdout.strip() == "returned ['class', 'condition', 'evidence', 'forecast', 'id', 'open', 'question']", result.stdout
        else:
            assert result.stdout.strip() == "refused question 0: keys off the allow-list ['condition'], missing []", result.stdout


# ---------- slice 2: the reader's page (RELEASE-PAGE.md revision 7)

import base64  # noqa: E402
import re  # noqa: E402

NETWORK_APIS = ('fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource', 'sendBeacon', 'import(', 'Worker', 'innerHTML', 'outerHTML',
                'insertAdjacentHTML', 'document.write', 'eval(', 'Function(', "createElement('a')", 'href', 'src')
CLIPPING_PROPERTIES = ('content', 'overflow', 'overflow-x', 'overflow-y', 'clip', 'clip-path', 'contain', 'text-overflow', 'line-clamp',
                       '-webkit-line-clamp', 'max-height', 'opacity', 'visibility')


def test_26_the_page_is_a_pure_function_of_the_data_with_literal_escapes():
    """RELEASE-PAGE.md §5 tests 1 and 2: the same data gives the same page; <, >, &, U+2028 and U+2029 become their six-character
    JSON escapes, so the data block cannot close or comment out, and it parses back to the same data."""
    hostile = '</script><img src=x onerror=alert(1)> & a line' + chr(0x2028) + 'break' + chr(0x2029) + '<!--'
    payload = json.dumps({'quote': hostile}, ensure_ascii=False).encode()
    page = release.render_page(payload)
    assert page == release.render_page(payload)
    block = page.decode().split('<script type="application/json" id="release-data">')[1].split('</script>')[0]
    backslash = chr(92)
    assert block == payload.decode().replace('<', backslash + 'u003c').replace('>', backslash + 'u003e').replace('&', backslash + 'u0026') \
        .replace(chr(0x2028), backslash + 'u2028').replace(chr(0x2029), backslash + 'u2029')
    assert '</script' not in block and '<!--' not in block and json.loads(block) == {'quote': hostile}
    assert page.decode().count('<script') == 2


def test_27_the_template_has_no_network_code_drawn_text_or_clipping():
    """RELEASE-PAGE.md §5 test 3: the script uses no network or markup-writing API and makes no link; the stylesheet draws no text and
    clips nothing; the CSP is exactly the designed policy with the hashes of the template's own script and style; charset and CSP
    come first."""
    for api in NETWORK_APIS:
        assert api not in release.PAGE_SCRIPT, api
    for name in CLIPPING_PROPERTIES:
        assert not re.search(r'(?<![-\w])' + re.escape(name) + r'\s*:', release.PAGE_STYLE), name
    assert 'nowrap' not in release.PAGE_STYLE
    digest = lambda text: "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"
    csp = (f"default-src 'none'; script-src {digest(release.PAGE_SCRIPT)}; style-src {digest(release.PAGE_STYLE)}; img-src 'none'; "
           "font-src 'none'; connect-src 'none'; base-uri 'none'; form-action 'none'")
    template = release.page_template()
    assert template.startswith('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                               f'<meta http-equiv="Content-Security-Policy" content="{csp}">\n')
    assert template.count(release.DATA_PLACEHOLDER) == 1


def test_28_the_package_page_must_be_the_page_of_its_data(stores, tmp_path):
    """RELEASE-PAGE.md §5 test 4: a page changed by one byte, or with a fetch added and its CSP and hashes updated, is refused because
    it is not render_page(data); a correct page with only its manifest hash wrong is refused for that reason; a fourth file is
    refused."""
    out = tmp_path / 'release'
    build_package(stores, out)
    assert check(stores, out)['fields_compared'] == FIXTURE_COUNTS['fields_compared']

    def copy_with(name, page=None, page_hash=None):
        target = tmp_path / name
        shutil.copytree(out, target)
        if page is not None:
            (target / release.PAGE_FILE).write_bytes(page)
        manifest = json.loads((target / release.MANIFEST_FILE).read_text())
        manifest['page_sha256'] = page_hash or hashlib.sha256((target / release.PAGE_FILE).read_bytes()).hexdigest()
        (target / release.MANIFEST_FILE).write_text(json.dumps(manifest))
        return target

    original = (out / release.PAGE_FILE).read_bytes()
    one_byte = copy_with('one-byte', original.replace(b'needs JavaScript', b'needs Javascript'))
    refused_with(lambda: check(stores, one_byte), 'the page is not the page made from its data')
    script = release.PAGE_SCRIPT
    added = script.replace("(function(){'use strict';", "(function(){'use strict';fetch('http://127.0.0.1:59999/library').catch(function(){});")
    digest = lambda text: "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"
    fetching = original.decode().replace(script, added).replace(digest(script), digest(added)).encode()
    assert fetching != original
    refused_with(lambda: check(stores, copy_with('fetching', fetching)), 'the page is not the page made from its data')
    wrong_hash = copy_with('wrong-hash', page_hash='0' * 64)
    refused_with(lambda: check(stores, wrong_hash), 'the manifest page_sha256 does not match the page')
    fourth = tmp_path / 'fourth'
    shutil.copytree(out, fourth)
    (fourth / 'extra.html').write_text('<p>x</p>')
    refused_with(lambda: check(stores, fourth), f"{fourth}: holds ['extra.html', 'index.html', 'manifest.json', 'release-data.json'], "
                                                "not exactly ['index.html', 'manifest.json', 'release-data.json']")


CERTIFIED_TEMPLATE_SHA256 = '33fd58c6a49ecdca7cfb87825b725937356b887553c1f2c9cc4cbebaf0866964'   # certified by poc/data/release-screen-2026-11-23c


def test_29_the_page_template_is_the_one_the_screen_run_certified():
    """RELEASE-PAGE.md revision 7, test 3: the whole page template, with its data placeholder, is the one the $0 screen run certified
    (poc/data/release-screen-2026-11-23c); any change to any part of it fails here until a new screen run certifies it."""
    assert hashlib.sha256(release.page_template().encode('utf-8')).hexdigest() == CERTIFIED_TEMPLATE_SHA256
