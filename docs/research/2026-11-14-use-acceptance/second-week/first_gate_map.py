"""The map of the distance to the first gate over every stored topic (D556; $0). It restates the four stored readings topic by
topic with the collector's own rules (the marks two readers agree on; where they differ, the two third readers' ruling when they
rule alike, else the point is open) and reconciles each to its report before anything is listed. It judges nothing: classes
come from the marks, the rulings and the reason the step gave.

  python3 first_gate_map.py <key of the week of 10-06> <output json>
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
DATA = ROOT / 'poc/data'
FRESH = ROOT / 'docs/research/2026-11-14-use-acceptance/fresh-ladders'
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'))
import accounting  # noqa: E402
import collect_readings  # noqa: E402

REASONS = [('no main part (D397)', r'main (one|figure|event)|neither .* main|without (naming|making|identifying)|two (separate |yearly |annual )?figures|several (tracked )?(figures|things)|both calendar|no single'),
           ('no listed theme', r'none of the listed themes|no listed theme|not covered by any listed theme|listed themes? cover|rental price'),
           ('a period that is not one year (D417)', r'not (a figure for )?one (fiscal or )?calendar year|rolling|twelve months|12 months|publication day'),
           ("a quarter's or half-year's figure", r'quarter|half-year'),
           ('a year already ended', r'already ended|had ended'),
           ('a year beyond next year', r'beyond next year'),
           ('nothing checkable on a date', r'no date|cannot be checked|no check|names no period'),
           ('another company', r'another company|belongs to')]


def reason_class(reason):
    return next((name for name, pattern in REASONS if re.search(pattern, reason or '', re.I)), 'other: ' + (reason or '')[:60])


def sends_of(outcomes, readers, of_family, families):
    """Per send: its kind, the marks that fail by agreement, the marks left open, and whether it is right and a sound written
    answer under each counting ('for': open points hold; 'against': open points fail)."""
    out = {}
    for send, outcome in outcomes.items():
        kind = accounting.kind_of(outcome)
        rows = [readers['reader 1'].get(send), readers['reader 2'].get(send)]
        entry = {'kind': kind, 'agreed_fails': [], 'open': [], 'named_upheld': [], 'named_open': [],
                 'reason': reason_class(outcome.get('reason')) if kind == 'refusal' else None}
        if kind == 'refused twice' or any(row is None or accounting.row_problem(row, outcome) for row in rows):
            entry.update(read=False, right={'for': False, 'against': False}, written={'for': False, 'against': False})
            out[send] = entry
            continue
        rulings = [of_family[family].get(send, {}) for family in families]
        for mark in accounting.marks_that_apply(kind):
            if rows[0][mark] == rows[1][mark]:
                value = rows[0][mark]
            else:
                ruled = {ruling.get('marks', {}).get(mark) for ruling in rulings}
                value = ruled.pop() if len(ruled) == 1 and len(rulings) >= 1 and None not in ruled else 'open'
            if value == 'fails':
                entry['agreed_fails'].append(mark)
            elif value == 'open':
                entry['open'].append(mark)
        for reader_name, row in zip(('reader 1', 'reader 2'), rows):
            if row['W'].strip():
                upheld = {ruling.get('W', {}).get(reader_name) for ruling in rulings}
                if upheld == {True}:
                    entry['named_upheld'].append(row['W'].strip()[:110])
                elif upheld != {False}:
                    entry['named_open'].append(row['W'].strip()[:110])
        clean_for = not entry['agreed_fails'] and not entry['named_upheld']
        clean_against = clean_for and not entry['open'] and not entry['named_open']
        entry.update(read=True, right={'for': clean_for, 'against': clean_against},
                     written={'for': clean_for and kind != 'refusal', 'against': clean_against and kind != 'refusal'})
        out[send] = entry
    return out


def population(name, folder, key_path, cases):
    _, item_of, outcomes, readers, _ = collect_readings.read_rows(folder, key_path)
    families = [family for family in collect_readings.third_reader_families(folder) if family] if (Path(folder) / 'third-reader').exists() else []
    of_family = {family: collect_readings.read_rulings(folder, item_of, outcomes, readers, family)[0] for family in families}
    sends = sends_of(outcomes, readers, of_family, families)
    topics = {}
    for case in sorted({send[0] for send in sends}, key=lambda c: (c.split('/')[0], int(c.split('-')[-1]))):
        attempts = [sends[(case, attempt)] for attempt in (1, 2, 3) if (case, attempt) in sends]
        topics[case] = {'thesis': cases[case], 'attempts': attempts,
                        'right': {how: sum(a['right'][how] for a in attempts) for how in ('for', 'against')},
                        'written': {how: sum(a['written'][how] for a in attempts) for how in ('for', 'against')}}
    totals = {how: {'right': sum(1 for t in topics.values() if t['right'][how] >= 2), 'right by a ladder': sum(1 for t in topics.values() if t['written'][how] >= 2)}
              for how in ('for', 'against')}
    return {'name': name, 'topics': topics, 'totals': totals, 'third_readers': families}


def main(week_key, output):
    cases44 = {case['case']: case['thesis'] for case in json.loads((ROOT / 'clean-arch/step4-2026-11-10/stage_a/cases.json').read_text())}
    july = {case['case']: case['thesis'] for draw in ('c1', 'c2', 'c3') for case in json.loads((DATA / f'clean-e2e-full-2026-11-13/{draw}/cases/cases.json').read_text())}
    week2 = {case['case']: case['thesis'] for case in json.loads((DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json').read_text())}
    fresh = {case['case']: case['thesis'] for case in json.loads((DATA / 'clean-lean-week-2026-11-14/week-r2/c1/cases/cases.json').read_text())}
    scratch = Path(output).parent / 'fresh-week-as-a-reading'
    if not scratch.exists():                                     # the fresh week in the collector's layout: one Codex reader and Claude's own marks, no third reader
        for number in (1, 2, 3):
            (scratch / f'send-{number}').mkdir(parents=True)
            (scratch / f'send-{number}/outcomes.jsonl').write_text((DATA / f'clean-lean-week-2026-11-14/week-r2/c1/ladder/send-{number}/outcomes.jsonl').read_text())
        (scratch / 'readers-answers').mkdir()
        (scratch / 'readers-answers/reader-codex-packet-1.jsonl').write_text((FRESH / 'codex-reader.jsonl').read_text())
        own = json.loads((FRESH / 'own-marks-before-the-reader.json').read_text())
        codex_b = {json.loads(line)['item']: json.loads(line)['B'] for line in (FRESH / 'codex-reader.jsonl').read_text().splitlines() if line.strip().startswith('{')}
        for row in own:                                          # Claude's fresh-week marks carried no B list; B enters no line, so the Codex reader's is copied
            row.setdefault('B', codex_b[row['item']])
            if any(row.get(mark) == 'fails' for mark in accounting.ALL_MARKS) and not row.get('why', '').strip():
                row['why'] = 'see FRESH-LADDERS-RESULT.md'
        (scratch / 'readers-answers/reader-claude-packet-1.jsonl').write_text('\n'.join(json.dumps(row) for row in own) + '\n')
    populations = [population("Alex's 44 topics, fourth reading", DATA / 'clean-ladder-stage-a-2026-11-10/run-4', DATA / 'clean-ladder-stage-a-2026-11-10/run-4/key-item-to-send.json', cases44),
                   population('July, 40 topics', DATA / 'clean-e2e-full-2026-11-13/stage-a', DATA / 'clean-e2e-full-2026-11-13/stage-a-key.json', july),
                   population('the fresh week, 7 topics (one Codex reader and Claude\'s own marks; no third reader)', scratch, FRESH / 'key.json', fresh),
                   population('the week of 10-06, 13 topics', DATA / 'clean-second-week-2026-11-15/week-continued/stage-a', week_key, week2)]
    reports = {populations[0]['name']: DATA / 'clean-ladder-stage-a-2026-11-10/run-4/stage-a-report.json', populations[1]['name']: DATA / 'clean-e2e-full-2026-11-13/stage-a/stage-a-report.json',
               populations[3]['name']: DATA / 'clean-second-week-2026-11-15/week-continued/stage-a/stage-a-report.json'}
    for entry in populations:
        line = f"{entry['name']}: {len(entry['topics'])} topics | open points for the answer: {entry['totals']['for']} | against: {entry['totals']['against']}"
        if entry['name'] in reports:
            report = json.loads(reports[entry['name']].read_text())
            stored = {'for': report['every unresolved point counted for the answer']['lines']['5'][1], 'against': report['every unresolved point counted against it']['lines']['5'][1]}
            same = all(entry['totals'][how][field] == stored[how][field] for how in ('for', 'against') for field in ('right', 'right by a ladder'))
            line += f" | the report: {dict((how, {k: v for k, v in stored[how].items() if k != 'of'}) for how in stored)} | reconciled: {same}"
            entry['reconciled'] = same
        print(line)
    Path(output).write_text(json.dumps(populations, indent=1, ensure_ascii=False, default=list) + '\n')
    return 0 if all(entry.get('reconciled', True) for entry in populations) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
