"""RELEASE-BUILD.md §6 mutants: each applied to a scratch copy (PYTHONDONTWRITEBYTECODE, no __pycache__) must fail
tests/test_release.py; the unmutated control must pass."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree

REPO = Path('/Users/lchingen/hivemind')
R, B = 'src/hivemind/release.py', 'scripts/release_build.py'
MUTANTS = {
    'condition emitted on number records': (R, "                record['forecast'] = FORECAST_UNAVAILABLE\n            else:\n                record['answers'] = labels\n                record['answer'] = _answer(",
                                            "                record['forecast'] = FORECAST_UNAVAILABLE\n                record['condition'] = 'FY2027 revenue is at least $350 billion'\n            else:\n                record['answers'] = labels\n                record['answer'] = _answer("),
    'one_line from the latest why_changed': (R, "evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources})",
                                             "evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources, 'one_line': (views_db.execute('select why_changed from judgements where view_id=? order by judgement_id desc limit 1', (view_id,)).fetchone() or {'why_changed': piece['one_line']})['why_changed']})"),
    'event test removed': (R, "    if key_measure(conn, view_id, as_of) in identity.EVENT_MEASURES:\n        return 'event'\n", ''),
    'Yes/No test removed': (R, "    if len(labels) == 2 and {vocabulary.canonical('label', label) for label in labels} == {'Yes', 'No'}:\n        return 'yes_no'\n", ''),
    'check_package without the file-set check': (R, "        if sorted(names) != sorted(PACKAGE_FILES):\n            raise", "        if False:\n            raise"),
    'manifest keys unchecked': (R, "    _keys(manifest, 'manifest', 'the manifest')\n", ''),
    'check_export without the closed-key check': (R, "    if set(value) != ALLOWED[kind]:", "    if not set(value) >= ALLOWED[kind]:"),
    'check_origins skipping evidence fields': (R, "            expected_evidence = _expected_evidence(views_db, items_db, view_id, as_of)\n",
                                               "            expected_evidence = question['evidence']\n"),
    'check_origins taking the class from the package': (R, "            kind = question_class(views_db, view_id, labels, as_of)\n            record = {'id': view_id, 'question': view['question'], 'open': _open_at(",
                                                        "            kind = question['class']\n            record = {'id': view_id, 'question': view['question'], 'open': _open_at("),
    'check_origins accepting duplicates': (R, "        packaged = data['questions']\n", "        packaged = list({q['id']: q for q in data['questions']}.values())\n"),
    'check_origins accepting another order': (R, "        packaged = data['questions']\n",
                                              "        packaged = sorted(data['questions'], key=lambda q: [r['view_id'] for r in views].index(q['id']) if q['id'] in [r['view_id'] for r in views] else -1)\n"),
    'pipe opened blocking': (R, "os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)", "os.O_RDONLY | os.O_NOFOLLOW, dir_fd=folder)"),
    'store path returned unresolved': (R, "        raise ReleaseRefused(f'{path}: a store path may not contain {found}, which the SQLite opener reads as URI syntax')\n    return real",
                                       "        raise ReleaseRefused(f'{path}: a store path may not contain {found}, which the SQLite opener reads as URI syntax')\n    return path"),
    'check_origins with an inner join': (R, "            if item is None:\n                raise ReleaseRefused(f'evidence {row[\"evidence_id\"]}", "            if item is None:\n                continue\n                raise ReleaseRefused(f'evidence {row[\"evidence_id\"]}"),
    'check without validating the day': (R, "        bound = expected_as_of if expected_as_of is not None else resolve(views_db, data['as_of'])",
                                         "        bound = expected_as_of if expected_as_of is not None else data['as_of']"),
    'builder skipping the staged check': (B, "counts, data, size = release.check_package(staged, views_db, items_db, expected_as_of=bound)", "counts, size = release.check_export(data), 0"),
    'symbolic-link check removed': (R, "os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)", "os.open(name, os.O_RDONLY | os.O_NONBLOCK, dir_fd=folder)"),
    'duplicate-key check removed': (R, "    if len(names) != len(set(names)):", "    if False:"),
    'switch reason emitted': (R, "            record = {'id': view_id, 'question': view['question'], 'open': service.is_open_as_of(views_db, view_id, bound), 'class': kind}",
                              "            record = {'id': view_id, 'question': view['question'], 'open': service.is_open_as_of(views_db, view_id, bound), 'class': kind, 'reason': (views_db.execute('select reason from view_switches where view_id=? order by id desc', (view_id,)).fetchone() or {'reason': ''})['reason']}"),
    'missing-item refusal replaced by the id fallback': (R, "        if row is None:\n            raise ReleaseRefused(f'evidence {evidence_id}: source item {input_id} is not in the items database')",
                                                         "        if row is None:\n            row = {'title': input_id, 'publisher': '', 'source_uri': ''}"),
    'publish replaced by os.rename': (R, "    rename = _no_replace_rename()\n    if rename is None:", "    rename = lambda source, target: os.rename(source, target) or 0\n    if rename is None:"),
    'the finally removed': (B, "        if staged is not None:\n            shutil.rmtree(staged)\n", ''),
    'staging path not dropped after publish': (B, "        staged = None                       # published", "        pass                                # published"),
    'canonical-day check removed': (R, "    if day.isoformat() != text:\n        raise ReleaseRefused", "    if False:\n        raise ReleaseRefused"),
    'key read without its day': (R, "    return row['measure'] if row is not None and service.visible(conn, row['seq'], as_of) else None",
                                 "    return row['measure'] if row is not None else None"),
    'null accepted as text': (R, "        if not isinstance(value[name], str):", "        if not (isinstance(value[name], str) or value[name] is None):"),
    'store-path refusal removed': (R, "    if found:\n        raise ReleaseRefused(f'{path}: a store path", "    if False:\n        raise ReleaseRefused(f'{path}: a store path"),
    'writer self-check removed': (R, "    check_export(data)\n    return data\n", "    return data\n"),
    "a number label written into another question's evidence": (R, "evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources})",
        "evidence.append({'id': piece['evidence_id'], **{name: piece[name] for name in EVIDENCE_TEXT}, 'sources': sources, **({'one_line': 'Bullish'} if view_id == 'v6' else {})})"),
    'report missing a field': (B, "    summary = {'ledger': str(args.ledger), 'items': str(args.items), 'as_of': data['as_of'],", "    summary = {'ledger': str(args.ledger), 'as_of': data['as_of'],"),
    'report not printed': (B, "    print(json.dumps(report, ensure_ascii=False, indent=1))\n", ""),
    'page embed not escaping <': (R, "EMBED_ESCAPED = ('<', '>', '&', chr(0x2028), chr(0x2029))", "EMBED_ESCAPED = ('>', '&', chr(0x2028), chr(0x2029))"),
    'quote written with innerHTML': (R, "item.appendChild(el('blockquote','evidence-quote',e.quote));", "var bq=el('blockquote','evidence-quote');bq.innerHTML=e.quote;item.appendChild(bq);"),
    'source address as a link': (R, "row.appendChild(el('span','source-address',s.uri));", "var ln=document.createElement('a');ln.className='source-address';ln.href=s.uri;ln.textContent=s.uri;row.appendChild(ln);"),
    'package page not compared with its data': (R, "    if page != render_page(raw):\n        raise", "    if False:\n        raise"),
    'page hash unchecked': (R, "    if manifest['page_sha256'] != hashlib.sha256(page).hexdigest():\n        raise", "    if False:\n        raise"),
    'CSP hash over another script': (R, "    csp = PAGE_CSP.format(script=_source_hash(PAGE_SCRIPT), style=_source_hash(PAGE_STYLE))",
                                     "    csp = PAGE_CSP.format(script=_source_hash(PAGE_SCRIPT + ' '), style=_source_hash(PAGE_STYLE))"),
    'publish_report replaced by os.replace': (R, "        os.link(temporary, path)\n", "        os.replace(temporary, path)\n        open(temporary, 'w').close()\n"),
}


def tree(where):
    root = Path(where)
    shutil.copytree(REPO / 'src', root / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(REPO / 'scripts', root / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
    (root / 'tests').mkdir()
    for name in ('test_release.py', 'conftest.py'):
        shutil.copy(REPO / 'tests' / name, root / 'tests' / name)
    return root


def run(root):
    return subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_release.py', '-q', '-p', 'no:cacheprovider', f'--junitxml={root}/junit.xml'], cwd=root, capture_output=True, text=True,
                          env={'PATH': '/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin', 'PYTHONPATH': f'{root}/src:{root}/poc', 'PYTHONDONTWRITEBYTECODE': '1', 'HOME': str(Path.home())}, timeout=900)


with tempfile.TemporaryDirectory() as base:
    control = run(tree(Path(base) / 'control'))
    print('control:', 'PASS' if control.returncode == 0 else 'FAIL', control.stdout.strip().splitlines()[-1])
    if control.returncode != 0:
        raise SystemExit('the unmutated control fails: no mutant is judged')
    caught = 0
    for n, (name, (relative, old, new)) in enumerate(MUTANTS.items()):
        root = tree(Path(base) / f'm{n}')
        path = root / relative
        text = path.read_text()
        assert text.count(old) == 1, (name, text.count(old))
        path.write_text(text.replace(old, new))
        result = run(root)
        cases = ElementTree.parse(root / 'junit.xml').getroot().iter('testcase')
        outcomes = [(case.get('name'), case.find('failure'), case.find('error')) for case in cases]
        failed = [name for name, failure, _ in outcomes if failure is not None   # a test that failed on its own scratch edit is not a catch
                  and 'scratch anchor' not in (failure.get('message') or '') + (failure.text or '')]
        errors = [name for name, _, error in outcomes if error is not None]
        verdict = 'CAUGHT' if failed and not errors else 'MISSED' if not errors else 'ERROR'   # a setup or collection error is not a catch
        caught += verdict == 'CAUGHT'
        print(f'{verdict}  {name}: {len(failed)} failing: {", ".join(failed[:6])}' + (f' | errors: {errors[:2]}' if errors else ''))
    print(f'{caught} of {len(MUTANTS)} mutants caught')
