"""Exercise `baseline_count.py` on made-up readings ($0): each case is a full reading built by the real builder, with rows
and a session log written by this script. The count must print the expected shares for the sound ones and refuse, naming
the reason, for the others.

  python3 clean-arch/step4-2026-11-10/stage_b/check_count.py <scratch folder>
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_baseline  # noqa: E402

CASES = {                                  # name: (planted answers in use, expected exit, words the output must hold; None: the expected shares)
    'clean': (6, 0, None),
    'five planted in use': (5, 0, 'planted caught 5 of 5'),
    'a test left without a planted answer': (4, 2, 'not each of the form'),
    'a planted answer missed by both': (6, 3, 'STOPPED'),
    'one family misses two': (6, 3, 'more than one in five'),
    'a rung not on the ladder': (6, 2, 'rung_the_evidence_points_to'),
    'UNSUPPORTED naming no rung, with a flaw that changes the rung (the second test)': (6, 0, 'UNSUPPORTED among decided'),
    'UNSUPPORTED naming no rung, with no flaw': (6, 2, 'rung_the_evidence_points_to None'),
    'a row the key does not hold': (6, 2, 'does not hold exactly the judgements of packet'),
    'a row in another packet\'s file': (6, 2, 'does not hold exactly the judgements of packet'),
    'a third ruling missing': (6, 2, 'no valid ruling'),
    'no session log': (6, 2, 'no sound record of its sessions'),
    'a negative time': (6, 2, 'no sound record of its sessions'),
    'a packet stopped twice': (6, 2, 'was not read'),
    'a session that returned after more than an hour': (6, 2, 'returned after more than 60 minutes'),
    'a packet with a row given twice': (6, 2, 'is not the packet the builder makes'),
    'a file that is not a packet in the readers\' folder': (6, 2, 'is not a packet of this reading'),
    'no read of the author\'s own': (6, 2, "the author's own read"),
    'UNSUPPORTED only from the third readers, not read by the author': (6, 2, "the author's own read"),
    'a slow family': (6, 3, 'more than twice its estimate'),
    'a key without one stored judgement': (6, 2, 'the key is not the key of this reading'),
    'a packet whose content was changed': (6, 2, 'is not the packet the builder makes'),
    'E names an item that was shown': (6, 2, 'E is'),
    'SUPPORTED with a flaw that changes the rung': (6, 2, 'changes the rung'),
    'a reason that is a number': (6, 2, 'no reason given'),
}


def share(numerator, denominator):
    return f'{numerator}/{denominator} ({100 * numerator / denominator:.0f}%)'


def build(scratch, name, planted_in_use):
    """(folder, key path, the shares a sound reading must print)."""
    folder = scratch / name.replace(' ', '-').replace("'", '')
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    in_use = [[draw, view, number] for draw, view, number, *_ in build_baseline.PLANTED][:planted_in_use]
    (folder / 'planted-in-use.json').write_text(json.dumps(in_use))
    key_path = scratch / f'{folder.name}-key.json'
    subprocess.run([sys.executable, str(HERE / 'build_baseline.py'), 'reading', str(folder), str(key_path)], check=True, capture_output=True)
    key = json.loads(key_path.read_text())
    (folder / 'readers-answers').mkdir()
    (folder / 'third-reader').mkdir()
    stored = [number for number, entry in key.items() if entry['kind'] == 'stored']
    disputed = stored[:10]
    packets = sorted({entry['packet'] for entry in key.values()})
    sessions = {family: {str(packet): [{'seconds': 200, 'outcome': 'returned'}] for packet in packets} for family in ('codex', 'claude')}
    planted_numbers = [number for number, entry in key.items() if entry['kind'].startswith('planted')]
    verdicts, rows_of_family = {}, {}
    for family in ('codex', 'claude'):
        rows = {}
        for number, entry in key.items():
            planted = entry['kind'].startswith('planted')
            verdict = 'UNSUPPORTED' if planted or (number in disputed and family == 'claude') else 'SUPPORTED'
            if name == 'a planted answer missed by both' and number == planted_numbers[0]:
                verdict = 'SUPPORTED'
            if name == 'one family misses two' and family == 'codex' and number in planted_numbers[:2]:
                verdict = 'SUPPORTED'
            other = 1 if entry['shown_rung'] != 1 else 2
            rung = (entry['stored_rung'] if planted else other) if verdict == 'UNSUPPORTED' else None
            row = {'judgement': int(number), 'verdict': verdict, 'rung_the_evidence_points_to': rung, 'reasoning_flaw': 'none', 'arithmetic': 'none', 'reference': 'holds',
                   'implied_outcome': 'holds', 'E': 'none', 'why': '' if verdict == 'SUPPORTED' else 'the figure in e1'}
            one_stored = number == disputed[-1] and family == 'codex'
            if name == 'a rung not on the ladder' and family == 'codex' and number == planted_numbers[1]:
                row['rung_the_evidence_points_to'] = 9
            if name.startswith('UNSUPPORTED naming no rung') and family == 'codex' and number == planted_numbers[3]:
                row['rung_the_evidence_points_to'] = None
                row['reasoning_flaw'] = 'changes_the_rung' if 'second test' in name else 'none'
            if name == 'E names an item that was shown' and one_stored:
                row['E'] = ['e999999']
            if name == 'SUPPORTED with a flaw that changes the rung' and one_stored:
                row.update(reasoning_flaw='changes_the_rung', why='a step')
            if name == 'a reason that is a number' and family == 'codex' and number == planted_numbers[2]:
                row['why'] = 7
            if name == 'UNSUPPORTED only from the third readers, not read by the author' and number == stored[20] and family == 'claude':
                row.update(verdict='INSUFFICIENT', why='the evidence prefers no rung')
                verdict = 'INSUFFICIENT'
            rows[number] = row
            verdicts.setdefault(number, []).append(verdict)
        rows_of_family[family] = rows
        by_packet = {packet: [rows[number] for number, entry in key.items() if entry['packet'] == packet] for packet in packets}
        if name == 'a row the key does not hold' and family == 'codex':
            by_packet[packets[0]].append(dict(by_packet[packets[0]][0], judgement=999))
        if name == 'a row in another packet\'s file' and family == 'codex':
            by_packet[packets[1]].append(by_packet[packets[0]].pop())
        for packet, packet_rows in by_packet.items():
            (folder / 'readers-answers' / f'reader-{family}-packet-{packet}.jsonl').write_text('\n'.join(json.dumps(row) for row in packet_rows) + '\n')
    apart = [number for number, pair in verdicts.items() if pair[0] != pair[1]]          # the third readers rule every differing verdict, a control's included
    resolved = {}
    for family in ('codex', 'claude'):
        rulings = []
        for index, number in enumerate(apart):
            unsupported = (family == 'claude' and index >= 7) or (name == 'UNSUPPORTED only from the third readers, not read by the author' and number == stored[20])
            resolved.setdefault(number, []).append('UNSUPPORTED' if unsupported else 'SUPPORTED')
            rulings.append({'judgement': int(number), 'verdict': 'UNSUPPORTED' if unsupported else 'SUPPORTED',
                            'rung_the_evidence_points_to': (1 if key[number]['shown_rung'] != 1 else 2) if unsupported else None, 'why': 'e1 decides it'})
        if name == 'a third ruling missing' and family == 'claude':
            rulings = rulings[:-1]
        (folder / 'third-reader' / f'rulings-{family}-1.jsonl').write_text('\n'.join(json.dumps(row) for row in rulings) + '\n')
    if name == 'a slow family':
        sessions['claude'] = {packet: [{'seconds': 300, 'outcome': 'stopped'}, {'seconds': 300, 'outcome': 'returned'}] for packet in sessions['claude']}
    if name == 'a negative time':
        sessions['codex']['1'] = [{'seconds': -5, 'outcome': 'returned'}]
    if name == 'a session that returned after more than an hour':
        sessions['codex']['1'] = [{'seconds': 3700, 'outcome': 'returned'}]
    if name == 'a packet with a row given twice':
        packet_file = folder / 'readers' / 'packet-1.json'
        rows = json.loads(packet_file.read_text())
        packet_file.write_text(json.dumps([dict(rows[0], question='another question')] + rows, indent=1, ensure_ascii=False) + '\n')
    if name == 'a file that is not a packet in the readers\' folder':
        (folder / 'readers' / 'packet-99.json').write_text('[]\n')
    if name != 'no read of the author\'s own':
        called = sorted({int(number) for family in rows_of_family for number, row in rows_of_family[family].items() if row['verdict'] == 'UNSUPPORTED' and number in stored})
        (folder / 'own-read.jsonl').write_text(''.join(json.dumps({'judgement': number, 'verdict': 'SUPPORTED', 'why': 'read beside its request'}) + '\n' for number in called))
    if name == 'a packet stopped twice':
        sessions['codex']['1'] = [{'seconds': 3600, 'outcome': 'stopped'}, {'seconds': 3600, 'outcome': 'stopped'}]
    if name != 'no session log':
        (folder / 'sessions.json').write_text(json.dumps(sessions))
    if name == 'a key without one stored judgement':
        key.pop(disputed[0])
        key_path.write_text(json.dumps(key))
    if name == 'a packet whose content was changed':
        packet_file = folder / 'readers' / 'packet-1.json'
        rows = json.loads(packet_file.read_text())
        rows[0]['answer']['reasons'] += ' One more sentence.'
        packet_file.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    unresolved = [number for number in stored if number in resolved and resolved[number][0] != resolved[number][1]]
    last = [number for number in stored if number in key and key[number]['last_of_view']]
    last_unresolved = sum(1 for number in last if number in unresolved)
    expected = [f'UNSUPPORTED among decided (all): unresolved left out {share(0, len(stored) - len(unresolved))}; counted SUPPORTED {share(0, len(stored))}; '
                f'counted UNSUPPORTED {share(len(unresolved), len(stored))}',
                f'SUPPORTED among decided last judgements: unresolved left out {share(len(last) - last_unresolved, len(last) - last_unresolved)}; '
                f'counted SUPPORTED {share(len(last), len(last))}; counted UNSUPPORTED {share(len(last) - last_unresolved, len(last))}']
    return folder, key_path, expected


def main():
    scratch = Path(sys.argv[1])
    failed = 0
    for name, (planted_in_use, expected_exit, words) in CASES.items():
        folder, key_path, expected = build(scratch, name, planted_in_use)
        run = subprocess.run([sys.executable, str(HERE / 'baseline_count.py'), str(folder), str(key_path)], capture_output=True, text=True)
        output = run.stdout + run.stderr
        wanted = expected if words is None else [words]
        passed = run.returncode == expected_exit and all(text in output for text in wanted) and 'Traceback' not in output
        failed += not passed
        print(f"{'ok  ' if passed else 'FAIL'} {name}: exit {run.returncode} (expected {expected_exit}); holds what it must: {all(text in output for text in wanted)}")
        if words is None:
            for text in expected:
                print('        expected and printed:' if text in output else '        EXPECTED, NOT PRINTED:', text)
        if not passed:
            print('     ', output.strip().splitlines()[-3:])
    print(f'{len(CASES) - failed} of {len(CASES)} cases as expected')
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
