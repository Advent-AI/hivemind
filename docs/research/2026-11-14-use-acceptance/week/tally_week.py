"""Lean step 2, the tally ($0): joins the two reader families' answers for readings A2 and B to the keys and prints every count the frozen
decision rule (LEAN-LOG §2) reads, per system. It judges nothing itself: coverage, worth and support are the readers' verdicts.

Reading B's supported controls are fixed by rule before any B answer is joined: the first four candidates, by candidate number, that the
separate reader marked SUPPORTED (`control-confirmation.jsonl`); the script refuses when fewer than four were confirmed.

  python3 tally_week.py <key folder outside the repository>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
SYSTEM_NAME = {'c1': 'clean', 'p1': 'production'}


def lines(name):
    return [json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')]


def reading_a(key):
    system_of = {label: system for system, label in key['labels'].items()}
    own_id = {row['system_id']: row['own_id'] for system in SYSTEM_NAME for row in key[system]}
    matters = json.loads((HERE / 'matters-A2.json').read_text())
    by_both = [m['matter'] for m in matters if m['listed_by'].startswith('both')]
    answers = {family: lines(f'{family}-A2.jsonl') for family in FAMILIES}
    cell, verdict = {}, {}
    for family, rows in answers.items():
        for row in rows:
            if row.get('part') == 1:
                cell[(family, row['matter'], system_of[row['system']])] = row
            elif row.get('part') == 2:
                verdict[(family, row['id'])] = row
    expected = len(matters) * 2
    for family in FAMILIES:
        judged = sum(1 for (reader, _, _) in cell if reader == family)
        if judged != expected:
            raise SystemExit(f'{family} judged {judged} of {expected} matter-and-system cells: refused')

    def covered(row):
        return row['status'] == 'opened' or (row['status'] == 'narrower' and row.get('main_outcome') is True)

    print('READING A, part 1: each matter against each system (status; ids in the system\'s own numbering)')
    for matter in matters:
        for system in SYSTEM_NAME:
            parts = []
            for family in FAMILIES:
                row = cell[(family, matter['matter'], system)]
                ids = ','.join(own_id.get(i, i) for i in row.get('ids') or [])
                extra = '' if row['status'] in ('opened', 'missed') else f" main_outcome={row.get('main_outcome')}"
                parts.append(f"{family}: {row['status']}{extra} [{ids}]")
            print(f"  {matter['matter']} ({matter['listed_by'][:4]}) {SYSTEM_NAME[system]:10} | " + ' | '.join(parts))
        print(f"      {matter['name']}")
    print('  covered = opened, or narrower with the matter\'s main outcome (the frozen wording):')
    for scope_name, scope in (('matters both families listed', by_both), ('all matters', [m['matter'] for m in matters])):
        for system in SYSTEM_NAME:
            per_family = {family: [m for m in scope if covered(cell[(family, m, system)])] for family in FAMILIES}
            agreed = [m for m in scope if all(covered(cell[(family, m, system)]) for family in FAMILIES)]
            print(f"    {scope_name} ({len(scope)}), {SYSTEM_NAME[system]:10}: " +
                  ', '.join(f'{family} {len(found)}' for family, found in per_family.items()) + f'; both families {len(agreed)} {agreed}')
    agree = sum(cell[('codex', m['matter'], s)]['status'] == cell[('claude', m['matter'], s)]['status'] for m in matters for s in SYSTEM_NAME)
    print(f'  the families give the same status on {agree} of {expected} cells')

    print('READING A, part 2: every opened question (worth / trivia / duplicate)')
    for system in SYSTEM_NAME:
        questions = key[system]
        for family in FAMILIES:
            counts = {}
            for question in questions:
                row = verdict.get((family, question['system_id']))
                if row is None:
                    raise SystemExit(f"{family} gave no verdict on {question['system_id']}: refused")
                counts[row['verdict']] = counts.get(row['verdict'], 0) + 1
            print(f"  {SYSTEM_NAME[system]:10} ({len(questions)} questions), {family}: {counts}")
        for question in questions:
            verdicts = [verdict[(family, question['system_id'])] for family in FAMILIES]
            if any(v['verdict'] != 'worth' for v in verdicts):
                shown = ' | '.join(f"{family}: {v['verdict']}" + (f" of {own_id.get(v.get('duplicate_of'), v.get('duplicate_of'))}" if v.get('duplicate_of') else '')
                                   + f" ({v.get('why')})" for family, v in zip(FAMILIES, verdicts))
                print(f"    {SYSTEM_NAME[system]} {question['own_id']}: {shown}")


def reading_b(key):
    confirmation = lines('control-confirmation.jsonl')
    confirmed = sorted(row['candidate'] for row in confirmation if row['verdict'] == 'SUPPORTED')
    if len(confirmed) < 4:
        raise SystemExit(f'only {len(confirmed)} supported controls were confirmed: refused')
    controls = confirmed[:4]
    answers = {family: {row['item']: row for row in lines(f'{family}-B.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        if sorted(answers[family]) != [row['item'] for row in key]:
            raise SystemExit(f'{family} judged {len(answers[family])} of {len(key)} items: refused')
    print(f'READING B: {len(key)} items; supported controls (confirmed first by a separate reader: {confirmed}): candidates {controls}')
    planted = [row for row in key if row['planted']]
    real = [row for row in key if not row['planted']]
    for family in FAMILIES:
        caught = [row['item'] for row in planted if answers[family][row['item']]['verdict'] != 'SUPPORTED']
        passed = [row['item'] for row in real if row['candidate'] in controls and answers[family][row['item']]['verdict'] == 'SUPPORTED']
        print(f'  {family}: planted wrong judgements caught {len(caught)} of {len(planted)}; supported controls passed {len(passed)} of {len(controls)}')
    for system in SYSTEM_NAME:
        rows = [row for row in real if row['draw'] == system]
        per_family = {family: {} for family in FAMILIES}
        for family in FAMILIES:
            for row in rows:
                found = answers[family][row['item']]['verdict']
                per_family[family][found] = per_family[family].get(found, 0) + 1
        both = [row for row in rows if all(answers[family][row['item']]['verdict'] == 'SUPPORTED' for family in FAMILIES)]
        print(f"  {SYSTEM_NAME[system]:10}: {len(rows)} last judgements; " + '; '.join(f'{family} {per_family[family]}' for family in FAMILIES) +
              f'; supported by both families {len(both)} of {len(rows)} ({len(both) / len(rows):.0%})')
        for row in rows:
            verdicts = {family: answers[family][row['item']] for family in FAMILIES}
            if any(v['verdict'] != 'SUPPORTED' for v in verdicts.values()):
                print(f"    {SYSTEM_NAME[system]} {row['view']} (item {row['item']}): " +
                      ' | '.join(f"{family}: {v['verdict']} ({v.get('why')})" for family, v in verdicts.items()))
        for family in FAMILIES:
            flagged = [(row['view'], bad.get('id'), bad.get('why')) for row in rows for bad in answers[family][row['item']].get('bad_citations') or []]
            print(f'    cited statements flagged by {family}: {len(flagged)} {flagged}')


def main():
    key_folder = Path(sys.argv[1])
    reading_a(json.loads((key_folder / 'week-key-A2.json').read_text()))
    reading_b(json.loads((key_folder / 'week-key-B.json').read_text()))


if __name__ == '__main__':
    main()
