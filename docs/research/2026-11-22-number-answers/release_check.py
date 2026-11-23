"""The $0 release check of RELEASE-BUILD.md §7 on four stored stores, read-only (a closing switch is added only to a copy).

    python3 docs/research/2026-11-22-number-answers/release_check.py <new output folder>

Builds each store's package with the real command, then: the decisive acceptance case on old-1; old-1/v8; the two known Yes/No leaks
at their own days; an unchanged event control; a closing switch on a copy; the diagnostic search of every forbidden stored string in
every decoded package field; the size and speed budgets against `bundle.library` on the same store. Writes results.json there."""
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import bundle, release, service  # noqa: E402
from hivemind.views import store  # noqa: E402

COMMAND = REPO / 'scripts' / 'release_build.py'
MARKER = 'Forecast unavailable'                     # D726's words, written here, not read from the module under test
FORMAT, ALLOW_LIST = 'hivemind-release/2', 'release-allow-list/1'   # RELEASE-PAGE.md's identifiers, written here, not read from the module
DATED = {'old-3/v36@2026-08-25': ('2026-08-25', 3239), 'old-1/v10@2026-08-28': ('2026-08-28', 5673)}   # each dated package's day and evidence
EXPECTED = {   # each store's default day, classes and evidence, fixed before this run from the reviewed first run (councils 75–75e reproduced them)
    'old-1': ('2026-09-20', {'number': 19, 'event': 28, 'yes_no': 0}, 8251),
    'old-2': ('2026-09-20', {'number': 17, 'event': 26, 'yes_no': 0}, 6306),
    'old-3': ('2026-09-20', {'number': 18, 'event': 31, 'yes_no': 0}, 6659),
    'served': ('2026-08-28', {'number': 13, 'event': 55, 'yes_no': 0}, 6461),
}
J1580_PREFIX = 'About $390 billion: $164 billion reported in the first half'   # the system's own forecast used as the forged value
CLOSING_REASON = 'due 2026-09-20, frozen on 2026-09-20 at rung 2 Bullish'
COMPARISON_ITEMS = REPO / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
STORES = {
    'old-1': (REPO / 'poc/data/comparison-2026-11-17/run/old-1/prod/views.sqlite', COMPARISON_ITEMS),
    'old-2': (REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod/views.sqlite', COMPARISON_ITEMS),
    'old-3': (REPO / 'poc/data/comparison-2026-11-17/run/old-3/prod/views.sqlite', COMPARISON_ITEMS),
    'served': (REPO / 'poc/data/served-2026-10-28-v34-nvda-3m-through-0828/views.sqlite', REPO / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'),
}


def build(ledger, items, out, as_of=None):
    args = [sys.executable, str(COMMAND), 'build', '--ledger', str(ledger), '--items', str(items), '--out', str(out)] + (['--as-of', as_of] if as_of else [])
    result = subprocess.run(args, capture_output=True, text=True, env={'PATH': '/usr/bin:/bin', 'PYTHONDONTWRITEBYTECODE': '1'})
    if result.returncode != 0:
        raise SystemExit(f'build {out} exited {result.returncode}: {result.stderr}')
    return json.loads(out.with_name(out.name + '.report.json').read_text()), release.read_data(out)


def check(ledger, items, package):
    views_db, items_db = service.open_ledger(str(ledger)), store.open_read_only(str(items))
    try:
        return release.check_package(package, views_db, items_db)[0]
    finally:
        views_db.close()
        items_db.close()


def fields(data, manifest=None):
    """(question id, field path, evidence id, text) for every decoded string of the package: every string value of the data at
    every level (ids, classes and the marker included) and of the manifest."""
    def walk(value, path, question_id, evidence_id):
        if isinstance(value, dict):
            question_id = value['id'] if 'class' in value else question_id
            evidence_id = value['id'] if 'one_line' in value else evidence_id
            for key, item in value.items():
                yield from walk(item, f'{path}.{key}' if path else key, question_id, evidence_id)
        elif isinstance(value, list):
            for n, item in enumerate(value):
                yield from walk(item, f'{path}[{n}]', question_id, evidence_id)
        elif isinstance(value, str):
            yield question_id, path, evidence_id, value
    yield from walk(data, '', None, None)
    if manifest is not None:
        yield from walk(manifest, 'manifest', None, None)


def forbidden(ledger, data):
    """Every stored string the package must not hold, by question and kind; judgement columns read only where the store has them."""
    conn = service.open_ledger(str(ledger))
    try:
        columns = {row[1] for row in conn.execute('pragma table_info(judgements)')}
        texts = [c for c in ('reasons', 'why_changed', 'implied_outcome', 'reference') if c in columns]
        out = []
        for question in data['questions']:
            view_id = question['id']
            for row in conn.execute('select label, condition from rungs where view_id=?', (view_id,)):
                if question['class'] == 'number':                # an event's or Yes/No question's labels are its shown answers
                    out.append((view_id, 'rung label', row['label']))
                out.append((view_id, 'rung condition', row['condition']))
            for row in conn.execute(f'select {", ".join(texts)} from judgements where view_id=?', (view_id,)):
                out += [(view_id, name, row[name]) for name in texts]
            out += [(view_id, 'switch reason', row['reason']) for row in conn.execute('select reason from view_switches where view_id=?', (view_id,))]
        return [entry for entry in out if entry[2]], [c for c in ('implied_outcome', 'reference') if c not in columns]
    finally:
        conn.close()


def diagnostics(ledger, data, package):
    stored, absent = forbidden(ledger, data)
    located = list(fields(data, json.loads((package / release.MANIFEST_FILE).read_text())))
    joined = '\x00'.join(text for *_, text in located)
    hits = []
    for view_id, kind, text in set(stored):
        if text in joined:
            for question_id, path, evidence_id, field in located:
                if text in field:
                    hits.append({'stored_in': view_id, 'kind': kind, 'text': text[:200], 'found_in': question_id, 'field': path, 'evidence': evidence_id})
    return {'stored_strings_judged': len(set(stored)), 'package_strings': len(located), 'judgement_columns_absent': absent, 'hits': hits}


def library_baseline(ledger, items):
    views_db, items_db = service.open_ledger(str(ledger)), store.open_read_only(str(items))
    try:
        started = time.monotonic()
        payload = bundle.library(views_db, items_db)
        return len(json.dumps(payload, ensure_ascii=False).encode()), time.monotonic() - started
    finally:
        views_db.close()
        items_db.close()


def by_id(data):
    return {q['id']: q for q in data['questions']}


def refresh(package, data=None, manifest_extra=None):
    """A forged copy made consistent everywhere but the store: its page made from the forged data again and both hashes refreshed, so
    the store comparison is what must refuse it."""
    if data is not None:
        payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
        (package / release.DATA_FILE).write_bytes(payload)
        (package / release.PAGE_FILE).write_bytes(release.render_page(payload))
    manifest = json.loads((package / release.MANIFEST_FILE).read_text())
    manifest['data_sha256'] = hashlib.sha256((package / release.DATA_FILE).read_bytes()).hexdigest()
    manifest['page_sha256'] = hashlib.sha256((package / release.PAGE_FILE).read_bytes()).hexdigest()
    manifest.update(manifest_extra or {})
    (package / release.MANIFEST_FILE).write_text(json.dumps(manifest))


def refused(ledger, items, package):
    try:
        check(ledger, items, package)
    except release.ReleaseRefused as error:
        return str(error)
    return None


def main(out):
    out = Path(out).absolute()
    out.mkdir()                                            # a new folder; refuses an existing one
    results = {'stores': {}}
    packages = {}
    for name, (ledger, items) in STORES.items():
        (out / name).mkdir()
        report, data = build(ledger, items, out / name / 'package')
        packages[name] = data
        library_bytes, library_seconds = library_baseline(ledger, items)
        seconds = report['export_seconds'] + report['check_seconds']
        results['stores'][name] = {
            'as_of': report['as_of'], 'counts': report['counts'], 'withheld_unresolved': len(report['withheld_unresolved']),
            'unresolved': report['withheld_unresolved'], 'data_bytes': report['data_bytes'], 'library_bytes': library_bytes,
            'seconds': round(seconds, 2), 'library_seconds': round(library_seconds, 2),
            'bytes_within_budget': report['data_bytes'] <= library_bytes,
            'seconds_within_budget': seconds <= 3 * library_seconds and seconds <= 120,
            'diagnostics': diagnostics(ledger, data, out / name / 'package')}
        print(name, json.dumps({k: v for k, v in results['stores'][name].items() if k not in ('unresolved', 'diagnostics')}), 'hits', len(results['stores'][name]['diagnostics']['hits']))

    ledger, items = STORES['old-1']
    data, package = packages['old-1'], out / 'old-1' / 'package'
    conn = service.open_ledger(str(ledger))
    stored = {row['evidence_id']: row for row in conn.execute("select * from evidence where evidence_id in ('e2295','e1865','e3597')")}
    implied = conn.execute('select implied_outcome from judgements where judgement_id=1580').fetchone()[0]
    in_force_v8 = [e['evidence_id'] for e in service.evidence(conn, 'v8', data['as_of'])]
    conn.close()
    required_text = {   # each example's full stored text, written down before the run (old-1, 2026-11-23); compared exactly
        'e2295': ('Morningstar cites NVIDIA Data Center revenue of $3 billion in FY2020 and $194 billion in FY2026, and estimates $361 billion in FY2027, up 86% year over year.',
                  'Nvidia’s DC business has achieved exponential growth already, rising from $3 billion in fiscal 2020 to $194 billion in fiscal 2026, and we estimate it will be $361 billion in fiscal 2027, representing 86% annual growth.'),
        'e1865': ('The author identifies firm SpaceX procurement commitments and NVIDIA Data Center growth above 60% into FY2028 as bullish confirmation conditions.',
                  'Bullish confirmation would require firm procurement commitments for the SpaceX buildout and continued NVIDIA Data Center growth above 60% into fiscal 2028.'),
        'e3597': ('The author says analysts estimate NVIDIA revenue of about $390 billion in calendar 2027 and over $550 billion in calendar 2028, with annual sales growth of roughly 24% to 25%.',
                  'Analysts see revenue reaching about $390 billion in 2027 and more than $550 billion in 2028, with annual sales growth of roughly 24% to 25%.')}
    kept = {}
    for evidence_id in ('e2295', 'e1865', 'e3597'):              # the fixed examples: a missing one is a failure, not a smaller list
        if evidence_id not in stored:
            kept[evidence_id] = {'questions': [], 'equal_to_store': False, 'present': False}
            continue
        holders = [(q['id'], e) for q in data['questions'] for e in q['evidence'] if e['id'] == evidence_id]
        kept[evidence_id] = {'questions': [h[0] for h in holders],
                             'equal_to_store': all(e['one_line'] == stored[evidence_id]['one_line'] and e['quote'] == stored[evidence_id]['quote'] for _, e in holders) and bool(holders),
                             'present': bool(holders),
                             'holds_its_wording': bool(holders) and all((e['one_line'], e['quote']) == required_text[evidence_id] for _, e in holders)}
    forged = out / 'old-1' / 'forged-summary'
    shutil.copytree(package, forged)
    changed = json.loads(json.dumps(data))
    next(e for e in by_id(changed)['v8']['evidence'] if e['id'] == 'e2295')['one_line'] = implied
    refresh(forged, changed)
    prose = out / 'old-1' / 'forged-manifest'
    shutil.copytree(package, prose)
    refresh(prose, manifest_extra={'note': implied})
    v8 = by_id(data)['v8']
    results['decisive'] = {'kept': kept, 'implied_outcome_j1580': implied[:120],
                           'substituted_into_e2295_refused': refused(ledger, items, forged),
                           'added_to_manifest_refused': refused(ledger, items, prose),
                           'unchanged_package_passes': check(ledger, items, package)['fields_compared']}
    results['decisive']['forged_value_is_j1580'] = implied.startswith(J1580_PREFIX)
    results['old-1/v8'] = {'class': v8['class'], 'forecast': v8['forecast'], 'evidence': len(v8['evidence']),
                           'same_ids_as_service_evidence': [e['id'] for e in v8['evidence']] == in_force_v8}

    leaks = {}
    for name, view_id, day, judgement_id in (('old-3', 'v36', '2026-08-25', 799), ('old-1', 'v10', '2026-08-28', 865)):
        ledger, items = STORES[name]
        report, dated = build(ledger, items, out / name / f'package-{day}', day)
        conn = service.open_ledger(str(ledger))
        row = conn.execute('select judgement_id, rung, why_changed, reasons from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (view_id, day)).fetchone()
        label = conn.execute('select label from rungs where view_id=? and position=?', (view_id, row['rung'])).fetchone()[0]
        conn.close()
        record = by_id(dated)[view_id]
        dated_manifest = json.loads((out / name / f'package-{day}' / release.MANIFEST_FILE).read_text())
        texts = [text for *_, text in fields(dated)]
        leaks[f'{name}/{view_id}@{day}'] = {
            'package_as_of': dated['as_of'], 'manifest_as_of': dated_manifest['as_of'], 'evidence': report['counts']['evidence'],
            'latest_judgement': row['judgement_id'], 'expected_judgement': judgement_id, 'label_kept': record['answer'] == label, 'answer': record['answer'],
            'why_changed_absent': not any(row['why_changed'] in t for t in texts), 'reasons_absent': not any((row['reasons'] or '\x01') in t for t in texts),
            'phrase_fields': {phrase: [(q, p, e, t[:160]) for q, p, e, t in fields(dated) if phrase in t]
                              for phrase in ('around $1 trillion', 'rung 4', 'at rung', 'capex at rung')}}
    results['leaks'] = leaks

    ledger, items = STORES['old-1']
    conn = service.open_ledger(str(ledger))
    control = next(q for q in data['questions'] if q['class'] == 'event' and q['id'] not in ('v10',) and q['answer'] is not None)
    stored_label = conn.execute('select r.label from judgements j join rungs r on r.view_id=j.view_id and r.position=j.rung where j.view_id=? and j.publication_day<=? order by j.judgement_id desc limit 1', (control['id'], data['as_of'])).fetchone()[0]
    control_ids = [e['evidence_id'] for e in service.evidence(conn, control['id'], data['as_of'])]
    conn.close()
    results['control'] = {'id': control['id'], 'answer': control['answer'], 'label_equals_store': control['answer'] == stored_label,
                          'evidence_equals_store': [e['id'] for e in control['evidence']] == control_ids}

    closing = out / 'old-1' / 'closing'
    closing.mkdir()
    copy = closing / 'views.sqlite'
    shutil.copyfile(ledger, copy)
    conn = sqlite3.connect(copy)
    rung = conn.execute("select rung from judgements where view_id='v8' order by judgement_id desc limit 1").fetchone()[0]
    rung_label = conn.execute("select label from rungs where view_id='v8' and position=?", (rung,)).fetchone()[0]
    reason = f'due {data["as_of"]}, frozen on {data["as_of"]} at rung {rung} {rung_label}'
    last_seq = conn.execute('select max(sequence_no) from processing_steps').fetchone()[0]
    conn.execute("insert into view_switches (view_id, open, reason, by_whom, after_seq) values ('v8', 0, ?, 'pull', ?)", (reason, last_seq))
    conn.commit()
    conn.close()
    views_db, items_db = service.open_ledger(str(copy)), store.open_read_only(str(items))
    exposed = bundle.view_bundle(views_db, bundle.item_lookup(items_db), 'v8')
    views_db.close()
    items_db.close()
    report, closed = build(copy, items, closing / 'package')
    texts = [text for *_, text in fields(closed)]
    results['closing'] = {'reason': reason, 'bundle_exposes_reason': any(s.get('reason') == reason for s in exposed['switches']),
                          'package_open': by_id(closed)['v8']['open'], 'reason_absent': not any(reason in t for t in texts),
                          'rung_label_inside_v8_fields': [(p, e, t[:120]) for q, p, e, t in fields(closed) if q == 'v8' and rung_label in t]}
    (out / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in results.items() if k != 'stores'}, ensure_ascii=False, indent=1))
    failures = [f'{name}: {key}' for name, s in results['stores'].items() for key in ('bytes_within_budget', 'seconds_within_budget') if not s[key]]
    for name in STORES:                                          # the delivered identifiers, data and manifest, against the literal ones
        delivered = json.loads((out / name / 'package' / release.MANIFEST_FILE).read_text())
        failures += [] if (packages[name]['format'], packages[name]['allow_list'], delivered['format'], delivered['allow_list']) == (FORMAT, ALLOW_LIST, FORMAT, ALLOW_LIST) else [f'{name}: format or allow-list']
    failures += [f'{name}: day, classes or evidence' for name, (day, classes, evidence) in EXPECTED.items()
                 if (results['stores'][name]['as_of'], results['stores'][name]['counts']['questions'], results['stores'][name]['counts']['evidence']) != (day, classes, evidence)]
    failures += [] if results['decisive']['forged_value_is_j1580'] else ['the forged value is not the system forecast j1580']
    decisive = results['decisive']
    failures += [f'kept {e}' for e in ('e2295', 'e1865', 'e3597')
                 if not (decisive['kept'].get(e, {}).get('present') and decisive['kept'][e]['equal_to_store'] and decisive['kept'][e]['holds_its_wording'])]
    expected_reasons = {'substituted_into_e2295_refused': 'question v8.evidence e2295.one_line: differs from the store',
                        'added_to_manifest_refused': "the manifest: keys off the allow-list ['note'], missing []"}   # exact, so another refusal (a stale hash) does not count
    failures += [k for k, reason in expected_reasons.items() if decisive[k] != reason]
    failures += [] if (results['old-1/v8']['same_ids_as_service_evidence'] and results['old-1/v8']['forecast'] == MARKER
                       and results['old-1/v8']['class'] == 'number' and results['old-1/v8']['evidence'] == 1284) else ['old-1/v8']
    for name, leak in results['leaks'].items():
        failures += [f'{name}: {k}' for k in ('label_kept', 'why_changed_absent', 'reasons_absent') if not leak[k]]
        failures += [] if leak['answer'] == 'Yes' else [f'{name}: answer']
        failures += [] if (leak['package_as_of'], leak['manifest_as_of'], leak['evidence']) == (DATED[name][0], DATED[name][0], DATED[name][1]) else [f'{name}: package day or evidence']
        failures += [] if leak['latest_judgement'] == leak['expected_judgement'] else [f'{name}: judgement']
        failures += [f'{name}: {phrase} found' for phrase, hits in leak['phrase_fields'].items() if hits]
    failures += [] if (results['control']['id'], results['control']['answer']) == ('v3', 'Yes') and results['control']['label_equals_store'] and results['control']['evidence_equals_store'] else ['control']
    closing = results['closing']
    failures += [] if closing['reason'] == CLOSING_REASON and closing['bundle_exposes_reason'] and closing['package_open'] is False and closing['reason_absent'] else ['closing']
    if failures:
        raise SystemExit(f'release check FAILED: {failures}')
    print('release check: every acceptance item and budget met; diagnostic hits to read by hand:',
          {name: len(s['diagnostics']['hits']) for name, s in results['stores'].items()})


if __name__ == '__main__':
    main(sys.argv[1])
