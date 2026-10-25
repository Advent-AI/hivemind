"""D156: verify checker tests reject deliberate defects on temporary copies."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'poc/hierarchy_study/review_subject_names.py'
TEST = ROOT / 'poc/hierarchy_study/test_review_subject_names.py'
MUTANTS = [
    ('existing_target', "ref != target['thread_id']", 'False', 'projection_itself'),
    ('new_target', "(target['name'], target['scope']) != (choice['new_name'], choice['new_scope'])", 'False', 'projection_itself'),
    ('final_binding', "if actual != expected or len(actual) != len(result['bindings']):", 'if False:', 'same_count'),
    ('empty_population', "'pending_semantic_review' if row['bindings_checked'] else 'unexercised'", "'pending_semantic_review'", 'empty_population'),
    ('failed_run', 'if failed is not None:', 'if False:', 'result_file_alone'),
    ('failed_checks', "if checks.get('history_unchanged') is not True or checks.get('resend') != 'skipped':", 'if False:', 'result_file_alone'),
    ('changing_snapshot', 'if current != data:', 'if False:', 'snapshot_rejects'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir()  # A rerun must use a new output directory.
    source = SOURCE.read_text()
    results = []
    with tempfile.TemporaryDirectory(prefix='hivemind-acceptance-mutants-') as temp:
        root = Path(temp)
        code = root / 'poc/hierarchy_study'
        code.mkdir(parents=True)
        (root / 'poc/reports').symlink_to(ROOT / 'poc/reports', target_is_directory=True)
        shutil.copyfile(TEST, code / TEST.name)
        cases = [('control', '', '', '')] + MUTANTS
        for name, old, new, selection in cases:
            if old and source.count(old) != 1:
                raise ValueError(f'Mutation is not uniquely located: {name}')
            (code / SOURCE.name).write_text(source.replace(old, new) if old else source)
            cache = code / '__pycache__'
            if cache.exists():
                shutil.rmtree(cache)
            cmd = [sys.executable, '-B', '-m', 'pytest', '-q', str(code / TEST.name)]
            if selection:
                cmd += ['-k', selection]
            run = subprocess.run(cmd, cwd=root, text=True, capture_output=True, timeout=60)
            output = run.stdout + run.stderr
            (out / f'{name}.txt').write_text(output)
            caught = run.returncode == (0 if name == 'control' else 1)
            if name != 'control':
                caught = caught and 'FAILED' in output and ('AssertionError' in output or 'DID NOT RAISE' in output)
            results.append({'case': name, 'returncode': run.returncode, 'expected_result': caught})
    print(json.dumps(results, indent=2))
    return 0 if all(r['expected_result'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
