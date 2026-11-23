"""$0 mutation check of judging-v12 (D713, DESIGN.md §5 "Mutants"; AGENTS §4). Each mutant is applied to a scratch copy of the tree, run
without bytecode caches, and must make its named tests fail; the unmutated copy must pass them.

  python3 mutants.py <scratch folder>
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
COPY = ['src', 'scripts', 'tests', 'pytest.ini', 'poc/config', 'poc/universe.json', 'poc/seeds']
CITATIONS, FROZEN = 'tests/test_citation_lists.py', 'tests/test_frozen_questions_and_judgement.py'
JUDGING, MODEL, PREFLIGHT = 'src/hivemind/views/judging.py', 'src/hivemind/model.py', 'scripts/preflight.py'
MUTANTS = [
    ('push ids left open', JUDGING,
     "        properties['pushes'] = {'type': 'array', 'items': dict(push_item, properties=dict(push_item['properties'], evidence_id={'$ref': '#/$defs/evidence_id'}))}",
     "        properties['pushes'] = properties['pushes']", CITATIONS, 'test_every_id_field'),
    ('lists parsed from the text, not the rows', JUDGING,
     "    lists = {'evidence': sorted({p['evidence_id'] for p in pieces}),",
     "    lists = {'evidence': sorted(evidence_shown_in('\\n'.join(lines))),", CITATIONS, 'test_one_owner'),
    ('the v12 check reads the text, not the lists', JUDGING,
     "    if lists is not None:\n        allowed, deps = set(lists['evidence']), set(lists['dependencies'])",
     "    if False:\n        allowed, deps = set(lists['evidence']), set(lists['dependencies'])", CITATIONS, 'test_one_owner'),
    ('maxItems dropped for an empty list', JUDGING,
     "        properties['cites'] = dict(properties['cites'], maxItems=0)", "        properties['cites'] = dict(properties['cites'])",
     CITATIONS, 'test_every_id_field'),
    ('the validator ignores maxItems', MODEL,
     "        if 'maxItems' in schema and len(value) > schema['maxItems']:", "        if False:", CITATIONS, 'test_every_id_field'),
    ('strict dropped from the outgoing format', MODEL,
     "{'name': schema_name, 'strict': True, 'schema': schema}", "{'name': schema_name, 'strict': False, 'schema': schema}",
     CITATIONS, 'test_a_judging_v12_round'),
    ('the round sends the open format', JUDGING,
     "            schemas = {v: schema_for(version, lists[v]) for v in level}", "            schemas = {v: _open_format(version) for v in level}",
     CITATIONS, 'test_a_judging_v12_round or test_an_answer_outside_the_lists'),
    ('the retry sends the open format', JUDGING,
     "user + note, schemas[view_id], 'judgement', 'judge', transport=transport)",
     "user + note, schemas[view_id] if not note else _open_format(version), 'judgement', 'judge', transport=transport)",
     CITATIONS, 'test_a_judging_v12_round'),
    ('preflight checks judge rows against the fixed schema', PREFLIGHT,
     "        if purpose == 'judge':                     # a missing format is reported whatever the answer holds, a malformed one included\n"
     "            schema = saved_judge_format(request_json)",
     "        if False:\n            schema = saved_judge_format(request_json)", CITATIONS, 'test_preflight_fails'),
    ('preflight skips a malformed judge row before checking its format', PREFLIGHT,
     "        if purpose == 'judge':                     # a missing format is reported whatever the answer holds, a malformed one included",
     "        if ':malformed:' in sha or not answer_json:\n            reasons[f'{purpose}: not JSON'] += 1\n            continue\n"
     "        if purpose == 'judge':                     # a missing format is reported whatever the answer holds, a malformed one included",
     CITATIONS, 'test_preflight_fails'),
    ('preflight does not fail on a missing judge format', PREFLIGHT,
     "    if missing_formats:", "    if False:", CITATIONS, 'test_preflights_entry_point'),
    ('the closed format drifts', JUDGING,
     "        schema['$defs'] = {'evidence_id': {'type': 'string', 'enum': evidence}}",
     "        schema['$defs'] = {'evidence_id': {'type': 'string', 'enum': list(reversed(evidence))}}", FROZEN, 'test_the_citation_version'),
]


def tree(scratch, name):
    root = scratch / name
    if root.exists():
        shutil.rmtree(root)
    for part in COPY:
        source, target = REPO / part, root / part
        target.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if source.is_dir() else shutil.copyfile)(source, target, **({'ignore': shutil.ignore_patterns('__pycache__')} if source.is_dir() else {}))
    return root


def run(root, test_file, selection):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', test_file, '-k', selection],
                            cwd=root, capture_output=True, text=True, env=environment)
    return result.returncode, result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr[-200:]


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    control = tree(scratch, 'control')
    ok = True
    for name, path, old, new, test_file, selection in MUTANTS:
        code, summary = run(control, test_file, selection)
        print(f'control  [{name}]: exit {code} {summary}')
        ok = ok and code == 0
        root = tree(scratch, 'mutant')
        text = (root / path).read_text()
        if text.count(old) != 1:
            print(f'mutant   [{name}]: the mutated line is not found once: not applied')
            ok = False
            continue
        (root / path).write_text(text.replace(old, new))
        code, summary = run(root, test_file, selection)
        caught = code != 0
        ok = ok and caught
        print(f'mutant   [{name}]: exit {code} {"CAUGHT" if caught else "NOT CAUGHT"} {summary}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
