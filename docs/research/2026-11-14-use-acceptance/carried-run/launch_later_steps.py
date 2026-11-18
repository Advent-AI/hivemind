"""After the second week's first step: join the three parts, prepare the draw, and launch the unchanged runner on the later
steps over the fortnight (PLAN.md, D563). Refuses if the rest is unfinished or a part does not join.

  python3 launch_later_steps.py <run root>
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(HERE.parent / 'second-week')]
import extension  # noqa: E402
import prepare_continued_draw  # noqa: E402


def main(run_root):
    run_root = Path(run_root)
    pid = int((run_root / 'rest/run.pid').read_text())
    if subprocess.run(['ps', '-p', str(pid)], capture_output=True).returncode == 0:
        raise SystemExit('the rest is still running: refused')
    (run_root / 'joined-2').mkdir()
    joined = run_root / 'joined-2/trace.sqlite'
    result = extension.join(run_root / 'joined-1/trace.sqlite', run_root / 'rest/trace.sqlite', joined)
    manifest_path = run_root / 'manifest-2026-09-22-10-05.json'
    manifest_path.write_text(json.dumps(result['manifest'], indent=1) + '\n')
    print(f"joined: {result['first_articles']} + {result['second_articles']} = {len(result['manifest']['item_ids'])} articles")
    record = {'kind': 'extension over two weeks (D563)', 'parts': [
        {'trace': str(ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite'), 'articles': 235, 'from': 'empty', 'note': 'the stored week of 2026-09-22 (D487-D489)'},
        {'trace': str(run_root / 'slice/trace.sqlite'), 'articles': 33, 'from': "week 1's last library", 'note': 'the slice, 2026-09-29'},
        {'trace': str(run_root / 'rest/trace.sqlite'), 'articles': result['second_articles'], 'from': "the slice's last library", 'note': '2026-09-30..10-05'}]}
    prepare_continued_draw.prepare(run_root, 'c1', run_root / 'ledger.json', manifest_path, 3, joined, record)
    run_json = run_root / 'c1/run.json'
    state = json.loads(run_json.read_text())
    note = 'extended over two weeks and joined (step1/continuation.json, D563); not run by this launcher'
    state['components']['step1']['note'] = note
    state['components']['step1']['attempts'][0]['note'] = note
    run_json.write_text(json.dumps(state, indent=1) + '\n')
    with open(run_root / 'later-steps.log', 'w') as log:
        process = subprocess.Popen(['caffeinate', '-i', sys.executable, str(ROOT / 'clean-arch/e2e-comparison-2026-11-13/run_fresh.py'), 'clean',
                                    '--root', str(run_root), '--label', 'c1', '--ledger', str(run_root / 'ledger.json'),
                                    '--manifest', str(manifest_path), '--passes', '3'],
                                   cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    (run_root / 'later-steps.pid').write_text(f'{process.pid}\n')
    print('later steps launched, pid', process.pid)


if __name__ == '__main__':
    main(sys.argv[1])
