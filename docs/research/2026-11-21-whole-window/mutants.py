"""$0 mutation check of the linking version after the link question version was added (D705, WORDING-V2.md §5; AGENTS §4): the July
mutants (`../2026-11-20-production-readiness/dependency-design/mutants.py`, one anchor moved with the builders) and the version's own.
Each mutant is applied to a scratch copy of the tree, run without bytecode caches, and must make its named tests fail; the unmutated
copy must pass them.

  python3 mutants.py <scratch folder>
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
COPY = ['src', 'scripts', 'tests', 'pytest.ini', 'poc/config', 'poc/universe.json', 'poc/seeds']
LINKS, FROZEN = 'tests/test_links.py', 'tests/test_frozen_questions_and_judgement.py'
MUTANTS = [
    # the July mutants
    ('filing narrows a reads link', 'src/hivemind/views/store.py',
     """    reads = " and coalesce(kind, '') != 'reads'" if""", """    reads = "" if""", LINKS, 'test_a_reads_link_is_not_a_narrower_home'),
    ('links asked under the jev engine', 'src/hivemind/views/round.py',
     "    if cfg.matching.engine == links.ENGINE:", "    if cfg.matching.engine in ('jev', links.ENGINE):", LINKS,
     'test_under_the_jev_engine_no_link_question_is_asked'),
    ('an existing reader is not queued', 'src/hivemind/views/writing.py',
     "            written.changed_views.add(reader)", "            pass", LINKS,
     'test_an_existing_question_gains_a_reads_link or test_the_article_writes_the_link'),
    ('an ordinary replay writes a harness ledger', 'scripts/replay.py',
     "    if marked:\n        raise SystemExit('this ledger is marked harness-only; an ordinary replay does not write it')", "    pass", LINKS,
     'test_an_ordinary_replay_refuses_a_harness_only_ledger'),
    ('the sign is ignored in the label', 'src/hivemind/views/links.py',
     "    want_read_high = favourable_is_high if sign == TOGETHER else not favourable_is_high", "    want_read_high = favourable_is_high", LINKS,
     'test_the_label_follows_the_sign'),
    ('the circle check reads stored links only', 'src/hivemind/views/links.py',
     "    for link in proposed:\n        graph.setdefault(link['reader'], set()).add(link['read'])\n", "", LINKS,
     'test_a_circle_through_two_openings or test_a_circle_through_a_stored_link'),
    ('a correction keeps the offending direction', 'src/hivemind/views/links.py',
     "    criteria = {k: v for k, v in QUESTION_SETS[version][0].items() if k != excluded}", "    criteria = dict(QUESTION_SETS[version][0])", LINKS,
     'test_a_circle_through_a_stored_link'),
    # the question version (D705)
    ('READS ignores the configured version', 'src/hivemind/views/links.py',
     "reads_question(jev_matching.thesis_text(conn, v), version=cfg.matching.link_questions)", "reads_question(jev_matching.thesis_text(conn, v))",
     LINKS, 'test_version_two_asks_its_own_criteria'),
    ('SIGN ignores the configured version', 'src/hivemind/views/links.py',
     "directions[(c['id'], v)], version=cfg.matching.link_questions)", "directions[(c['id'], v)])", LINKS,
     'test_version_two_asks_its_own_criteria'),
    ('a correction ignores the configured version', 'src/hivemind/views/links.py',
     "excluded=excluded, note=note,\n                                                            version=cfg.matching.link_questions)",
     "excluded=excluded, note=note)", LINKS, 'test_version_two_asks_its_own_criteria'),
    ('config accepts an unknown or null question version', 'src/hivemind/config.py',
     "        if not isinstance(link_questions, str) or link_questions not in LINK_QUESTIONS:", "        if False:", LINKS,
     'test_the_question_version_is_read'),
    ('config accepts the field in another setting or engine', 'src/hivemind/config.py',
     "        if name != 'matching' or engine != 'jev-links':", "        if False:", LINKS, 'test_the_question_version_is_read'),
    ('config reads a null as the first version', 'src/hivemind/config.py',
     "        if not isinstance(link_questions, str) or link_questions not in LINK_QUESTIONS:",
     "        link_questions = link_questions or 'links-v1'\n        if link_questions not in LINK_QUESTIONS:", LINKS,
     'test_the_question_version_is_read'),
    ('a version-2 text drifts by one word', 'src/hivemind/views/links.py',
     "since a higher base lowers the growth)", "since a higher base reduces the growth)", FROZEN,
     'test_the_linking_version_pins_its_questions'),
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
