"""$0 mutation check of tests/test_links.py (AGENTS §4): each mutant is applied to a scratch copy of the tree, run without bytecode
caches, and must make its named tests fail; the unmutated copy must pass them.

  python3 mutants.py <scratch folder>
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
COPY = ['src', 'scripts', 'tests', 'pytest.ini', 'poc/config', 'poc/universe.json', 'poc/seeds']
MUTANTS = [
    ('filing narrows a reads link', 'src/hivemind/views/store.py',
     """    reads = " and coalesce(kind, '') != 'reads'" if""", """    reads = "" if""",
     'test_a_reads_link_is_not_a_narrower_home'),
    ('links asked under the jev engine', 'src/hivemind/views/round.py',
     "    if cfg.matching.engine == links.ENGINE:", "    if cfg.matching.engine in ('jev', links.ENGINE):",
     'test_under_the_jev_engine_no_link_question_is_asked'),
    ('an existing reader is not queued', 'src/hivemind/views/writing.py',
     "            written.changed_views.add(reader)", "            pass",
     'test_an_existing_question_gains_a_reads_link or test_the_article_writes_the_link'),
    ('an ordinary replay writes a harness ledger', 'scripts/replay.py',
     "    if marked:\n        raise SystemExit('this ledger is marked harness-only; an ordinary replay does not write it')", "    pass",
     'test_an_ordinary_replay_refuses_a_harness_only_ledger'),
    ('the sign is ignored in the label', 'src/hivemind/views/links.py',
     "    want_read_high = favourable_is_high if sign == TOGETHER else not favourable_is_high", "    want_read_high = favourable_is_high",
     'test_the_label_follows_the_sign'),
    ('the circle check reads stored links only', 'src/hivemind/views/links.py',
     "    for link in proposed:\n        graph.setdefault(link['reader'], set()).add(link['read'])\n", "",
     'test_a_circle_through_two_openings or test_a_circle_through_a_stored_link'),
    ('a correction keeps the offending direction', 'src/hivemind/views/links.py',
     "    criteria = {k: v for k, v in READS.items() if k != excluded}", "    criteria = dict(READS)",
     'test_a_circle_through_a_stored_link'),
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


def run(root, selection):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests/test_links.py', '-k', selection],
                            cwd=root, capture_output=True, text=True, env=environment)
    return result.returncode, result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr[-200:]


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    control = tree(scratch, 'control')
    ok = True
    for name, path, old, new, selection in MUTANTS:
        code, summary = run(control, selection)
        print(f'control  [{name}]: exit {code} {summary}')
        ok = ok and code == 0
        root = tree(scratch, 'mutant')
        text = (root / path).read_text()
        if text.count(old) != 1:
            print(f'mutant   [{name}]: the mutated line is not found once: not applied')
            ok = False
            continue
        (root / path).write_text(text.replace(old, new))
        code, summary = run(root, selection)
        caught = code != 0
        ok = ok and caught
        print(f'mutant   [{name}]: exit {code} {"CAUGHT" if caught else "NOT CAUGHT"} {summary}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
