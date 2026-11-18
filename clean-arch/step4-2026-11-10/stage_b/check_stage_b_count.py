"""Exercise `stage_b_count.py` and `control_theses.py count` on made-up readings ($0). Each case is a full reading built by the real
builders from the completed Stage B run, with rows and session logs written by this script. A sound reading must print its lines;
every other case must refuse, naming the reason. The baseline count's refusals of rows, sessions and rulings, which Stage B's count
reuses, are exercised by `check_count.py`.

  python3 clean-arch/step4-2026-11-10/stage_b/check_stage_b_count.py <scratch folder>
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_baseline  # noqa: E402
import build_stage_b  # noqa: E402

FAMILIES = ('codex', 'claude')
JUDGEMENT_CASES = {                        # name: (planted in use, expected exit, words the output must hold)
    'clean': (6, 0, ['line 1, no draw incomplete: met', 'figure: SUPPORTED 113, UNSUPPORTED 1', 'unresolved left out: UNSUPPORTED 1/114 (0.9%) against at most 12.7%: met',
                     'yes/no: SUPPORTED 122, UNSUPPORTED 0', 'last judgements:']),
    'every yes/no judgement INSUFFICIENT': (6, 3, ['the yes/no line has no decided judgement']),
    'a test left without a planted answer': (6, 2, ["no planted answer under ['planted test 3'] passed the trial"]),
    'planted-in-use.json not the trial\'s result': (6, 2, ["planted-in-use.json is not the trial's result"]),
    'a trial row with a field missing': (6, 2, ['the trial: codex: trial judgement']),
    'a trial without its session record': (6, 2, ['no sound record of a fresh session']),
    'a reading row with a field missing': (6, 2, ["not the form's"]),
    'a rung that is text on a SUPPORTED row': (6, 2, ["rung_the_evidence_points_to is 'three'"]),
    'a planted answer missed by both': (6, 3, ['STOPPED']),
    'a key without one stored judgement': (6, 2, ['the key is not the key of this reading']),
    'a slow family': (6, 3, ['more than twice its estimate']),
    'figures over the line': (6, 0, ['MISSED']),
}
CONTROL_CASES = {
    'clean': (0, ['[Ohio, listed apart]', 'line 3, D430 reading (the line)', 'line 3, literal reading (beside)']),
    'an item left unmarked': (2, ['items must mark exactly']),
    'a disagreement with no ruling': (2, ['no ruling on']),
    'a ruling where the readers agree': (2, ['where the readers do not differ']),
    'a control packet changed': (2, ['is not the packet the builder makes']),
    'a disagreement ruled both ways': (0, ['same question unresolved']),
    'a missing answers file': (2, ['no answers for control-packet-4']),
    'a ruling with no reason': (2, ['a ruling is']),
    'a missing item beside a disputed one': (0, ['material not shown (items shown 2, not shown 1, unresolved 1, of 4)']),
}


def judgement_reading(scratch, name, planted_in_use):
    folder = scratch / ('judgements-' + name.replace(' ', '-'))
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    trial_key_path = scratch / f'{folder.name}-trial-key.json'
    subprocess.run([sys.executable, str(HERE / 'build_stage_b.py'), 'validation', str(folder), str(trial_key_path)], check=True, capture_output=True)
    trial_key = json.loads(trial_key_path.read_text())
    (folder / 'validation-answers').mkdir()
    for family in FAMILIES:
        for packet in (1, 2):
            lines = []
            for number, entry in trial_key.items():
                if entry['packet'] != packet:
                    continue
                planted_answer = entry['kind'].startswith('planted') and not (name == 'a test left without a planted answer' and family == 'codex' and entry['kind'] == 'planted test 3')
                row = {'judgement': int(number), 'verdict': 'UNSUPPORTED' if planted_answer else 'SUPPORTED', 'rung_the_evidence_points_to': entry['stored_rung'] if planted_answer else None,
                       'reasoning_flaw': 'none', 'arithmetic': 'none', 'reference': 'holds', 'implied_outcome': 'holds', 'E': 'none', 'why': 'e1 decides it' if planted_answer else ''}
                if name == 'a trial row with a field missing' and family == 'codex' and not planted_answer and not any('"SUPPORTED"' in line for line in lines):
                    row.pop('why')                 # a field the baseline's check does not read on a SUPPORTED row
                lines.append(json.dumps(row))
            (folder / 'validation-answers' / f'reader-{family}-packet-{packet}.jsonl').write_text('\n'.join(lines) + '\n')
    if name != 'a trial without its session record':
        (folder / 'sessions-trial.json').write_text(json.dumps({family: {'1': [{'seconds': 300, 'outcome': 'returned'}], '2': [{'seconds': 300, 'outcome': 'returned'}]} for family in FAMILIES}))
    trial = subprocess.run([sys.executable, str(HERE / 'stage_b_trial.py'), str(folder), str(trial_key_path)], capture_output=True, text=True)
    if trial.returncode != 0:                      # the trial refuses: the case writes the file the operator might, to reach the count's own check
        in_use = [[draw, view, number] for draw, view, number, test, *_ in build_stage_b.PLANTED if test != 3]
        (folder / 'planted-in-use.json').write_text(json.dumps(in_use) + '\n')
    if name == 'planted-in-use.json not the trial\'s result':
        (folder / 'planted-in-use.json').write_text(json.dumps(json.loads((folder / 'planted-in-use.json').read_text())[:5]) + '\n')
    key_path = scratch / f'{folder.name}-key.json'
    builder = subprocess.run([sys.executable, str(HERE / 'build_stage_b.py'), 'reading', str(folder), str(key_path), str(trial_key_path)], capture_output=True, text=True)
    if builder.returncode != 0:                    # the builder refuses before the trial passes: the case builds the packets by hand, as an operator might
        views = build_stage_b.all_views()
        texts, key = build_baseline.rendered(build_stage_b.stage_b_packets(views, {tuple(entry) for entry in json.loads((folder / 'planted-in-use.json').read_text())}), views)
        (folder / 'readers').mkdir()
        for number, text in enumerate(texts, start=1):
            (folder / 'readers' / f'packet-{number}.json').write_text(text)
        key_path.write_text(json.dumps(key, indent=1) + '\n')
    elif trial.returncode != 0 or name == 'planted-in-use.json not the trial\'s result':
        raise SystemExit(f'{name}: the builder built the reading packets although the trial did not pass')
    key = json.loads(key_path.read_text())
    (folder / 'readers-answers').mkdir()
    (folder / 'third-reader').mkdir()
    packets = sorted({entry['packet'] for entry in key.values()})
    figures = [number for number, entry in key.items() if entry['kind'] == 'stored' and entry['shape'] == 'figure']
    against = set(figures[:1] if name != 'figures over the line' else figures[:20])
    planted = [number for number, entry in key.items() if entry['kind'].startswith('planted')]
    own = []
    for family in FAMILIES:
        rows = {}
        for number, entry in key.items():
            verdict = 'UNSUPPORTED' if entry['kind'].startswith('planted') or number in against else 'SUPPORTED'
            if name == 'a planted answer missed by both' and number == planted[0]:
                verdict = 'SUPPORTED'
            if name == 'every yes/no judgement INSUFFICIENT' and entry['shape'] != 'figure' and entry['kind'] != 'planted test 1':
                verdict = 'INSUFFICIENT' if not entry['kind'].startswith('planted') else verdict
            other = 1 if entry['shown_rung'] != 1 else 2
            rung = (entry['stored_rung'] if entry['kind'].startswith('planted') else other) if verdict == 'UNSUPPORTED' else None
            rows[number] = {'judgement': int(number), 'verdict': verdict, 'rung_the_evidence_points_to': rung, 'reasoning_flaw': 'none', 'arithmetic': 'none',
                            'reference': 'holds', 'implied_outcome': 'holds', 'E': 'none', 'why': '' if verdict == 'SUPPORTED' else 'the figure in e1'}
            if name == 'a reading row with a field missing' and family == 'claude' and number == figures[3]:
                rows[number].pop('why')            # a SUPPORTED row: the baseline's check does not read its why
            if name == 'a rung that is text on a SUPPORTED row' and family == 'claude' and number == figures[4]:
                rows[number]['rung_the_evidence_points_to'] = 'three'
            if verdict == 'UNSUPPORTED' and entry['kind'] == 'stored' and family == 'codex':
                own.append(int(number))
        for packet in packets:
            (folder / 'readers-answers' / f'reader-{family}-packet-{packet}.jsonl').write_text(
                ''.join(json.dumps(rows[number]) + '\n' for number, entry in key.items() if entry['packet'] == packet))
    (folder / 'third-reader' / 'rulings-codex-1.jsonl').write_text('')
    (folder / 'third-reader' / 'rulings-claude-1.jsonl').write_text('')
    seconds = 700 if name == 'a slow family' else 200
    (folder / 'sessions.json').write_text(json.dumps({family: {str(packet): [{'seconds': seconds, 'outcome': 'returned'}] for packet in packets} for family in FAMILIES}))
    (folder / 'own-read.jsonl').write_text(''.join(json.dumps({'judgement': number, 'verdict': 'UNSUPPORTED', 'why': 'read beside its request'}) + '\n' for number in own))
    if name == 'a key without one stored judgement':
        key.pop(figures[5])
        key_path.write_text(json.dumps(key))
    return [sys.executable, str(HERE / 'stage_b_count.py'), str(folder), str(key_path), str(trial_key_path)]


def control_reading(scratch, name):
    folder = scratch / ('controls-' + name.replace(' ', '-'))
    shutil.rmtree(folder, ignore_errors=True)
    subprocess.run([sys.executable, str(HERE / 'control_theses.py'), 'packets', str(folder), str(scratch / f'{folder.name}-facts.json')], check=True, capture_output=True)
    (folder / 'controls-answers').mkdir()
    (folder / 'controls-third').mkdir()
    texts = sorted((folder / 'controls').glob('control-packet-*.json'))
    for family in FAMILIES:
        for path in texts:
            if name == 'a missing answers file' and family == 'claude' and path.stem == 'control-packet-4':
                continue
            rows = []
            for item in json.loads(path.read_text()):
                marks = {decisive['id']: 'shown' for decisive in item['reader_b_decisive_items']}
                if name == 'a missing item beside a disputed one' and item['control'] == 3:
                    first_id, second_id = list(marks)[:2]
                    marks[first_id] = 'not_shown'
                    marks[second_id] = 'not_shown' if family == 'claude' else 'shown'
                if name == 'an item left unmarked' and family == 'codex' and item['control'] == 2:
                    marks.popitem()
                differ = name in ('a disagreement with no ruling', 'a disagreement ruled both ways', 'a ruling with no reason') and family == 'claude' and item['control'] == 3
                rows.append({'control': item['control'], 'same_question': 'no' if differ else 'yes', 'same_due': 'yes', 'items': marks, 'why': 'the same total for the same year'})
            (folder / 'controls-answers' / f'reader-{family}-{path.stem}.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
    if name == 'a ruling where the readers agree':
        (folder / 'controls-third' / 'rulings-codex.jsonl').write_text(json.dumps({'control': 1, 'field': 'same_due', 'ruling': 'yes', 'why': 'x'}) + '\n')
    if name == 'a ruling with no reason':
        for family in FAMILIES:
            (folder / 'controls-third' / f'rulings-{family}.jsonl').write_text(json.dumps({'control': 3, 'field': 'same_question', 'ruling': 'yes', 'why': None}) + '\n')
    if name == 'a missing item beside a disputed one':
        second_id = [item for path in texts for item in json.loads(path.read_text()) if item['control'] == 3][0]['reader_b_decisive_items'][1]['id']
        for family, ruling in (('codex', 'shown'), ('claude', 'not_shown')):
            (folder / 'controls-third' / f'rulings-{family}.jsonl').write_text(json.dumps({'control': 3, 'field': f'item {second_id}', 'ruling': ruling, 'why': 'x'}) + '\n')
    if name == 'a disagreement ruled both ways':
        for family, ruling in (('codex', 'yes'), ('claude', 'no')):
            (folder / 'controls-third' / f'rulings-{family}.jsonl').write_text(json.dumps({'control': 3, 'field': 'same_question', 'ruling': ruling, 'why': 'x'}) + '\n')
    if name == 'a control packet changed':
        path = folder / 'controls' / 'control-packet-1.json'
        path.write_text(path.read_text().replace('"control": 1,', '"control": 1, "note": "x",'))
    return [sys.executable, str(HERE / 'control_theses.py'), 'count', str(folder)]


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    cases = [(f'count: {name}', judgement_reading(scratch, name, planted), code, words) for name, (planted, code, words) in JUDGEMENT_CASES.items()]
    cases += [(f'controls: {name}', control_reading(scratch, name), code, words) for name, (code, words) in CONTROL_CASES.items()]
    failed = 0
    for name, command, expected_exit, words in cases:
        run = subprocess.run(command, capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
        output = run.stdout + run.stderr
        holds = all(text in output for text in words)
        passed = run.returncode == expected_exit and holds and 'Traceback' not in output
        failed += not passed
        print(f"{'ok  ' if passed else 'FAIL'} {name}: exit {run.returncode} (expected {expected_exit}); holds what it must: {holds}")
        if not passed:
            print('      ' + '\n      '.join(output.strip().splitlines()[-8:]))
    print(f'{len(cases) - failed} of {len(cases)} cases as expected')
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
