"""The main-numbers probe, step one: the tally ($0). Joins the two blind reader families' marks to the key and prints every count the
frozen lines of PROBE-DESIGN.md read. It judges nothing itself: what a question asks, whether two questions are one result, and whether a
named fact is kept and linked are the readers' marks; a line is counted where the two families agree, and every difference is listed.
Suppression is counted from the records by the stored thesis's subject, each such thesis printed for reading.

  python3 tally_stage1.py <records.jsonl> <cases.json> <key folder outside the repository>
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
MATTERS = {'FY2027 revenue': ('revenue', 'FY2027'), 'FY2028 revenue': ('revenue', 'FY2028'), 'FY2028 gross margin': ('gross_margin', 'FY2028')}
MATTER_CASES = {'FY2027 revenue': ['t1-target', 't4-target', 't6-target'],
                'FY2028 revenue': ['t1-target', 't2-target', 't4-target', 't5-target', 't6-target'],
                'FY2028 gross margin': ['t4-target', 't5-target']}
KEEP = {'k1-keep': re.compile(r'supply commitment|purchase obligation|purchase commitment', re.I), 'k2-keep': re.compile(r'Rubin', re.I)}
MOST = 2 / 3 - 1e-9


def lines(name):
    return [json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')]


def rate(count, total):
    return f'{count}/{total}'


def main():
    records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
    cases = {case['case']: case for case in json.loads(Path(sys.argv[2]).read_text())}
    key = {row['answer']: row for row in json.loads((Path(sys.argv[3]) / 'main-numbers-key-reader-packet.json').read_text())}
    marks = {family: {row['answer']: row for row in lines(f'{family}-reader.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        missing = sorted(set(key) - set(marks[family]))
        if missing:
            raise SystemExit(f'{family} gave no line for {len(missing)} answers ({missing[:5]}): refused')
    answer_of = {(row['case'], row['arm'], row['send']): label for label, row in key.items()}
    valid = collections.defaultdict(list)
    for record in records:
        if record['attempts'][-1].get('outcome') == 'valid':
            valid[(record['case'], record['arm'])].append(record)
    print('valid sends per case and arm:', {f'{case} {arm}': len(rows) for (case, arm), rows in sorted(valid.items())})

    def question_marks(family, label):
        return {question['id']: question for question in marks[family][label].get('questions') or []}

    def opens(family, label, matter):
        asks, year = MATTERS[matter]
        return [q for q in question_marks(family, label).values()
                if q.get('asks') == asks and q.get('fiscal_year') == year and q.get('named') is True]

    print('\nOPENED (c20; a question the reader marks as that measure and year, named):')
    opened_ok = True
    for matter, case_names in MATTER_CASES.items():
        passing = {family: 0 for family in FAMILIES}
        room = 0
        for case_name in case_names:
            cells = []
            for arm in ('c8', 'c20'):
                sends = valid[(case_name, arm)]
                per_family = {family: sum(1 for record in sends if opens(family, answer_of[(case_name, arm, record['send'])], matter)) for family in FAMILIES}
                shapes = collections.Counter()
                for record in sends:
                    for q in opens('codex', answer_of[(case_name, arm, record['send'])], matter):
                        shapes[f"{q.get('shape')}, {q.get('scope')}"] += 1
                cells.append(f"{arm}: " + ', '.join(f'{family} {rate(per_family[family], len(sends))}' for family in FAMILIES) + (f' shapes {dict(shapes)}' if shapes else ''))
                if arm == 'c8' and all(per_family[family] / max(len(sends), 1) < MOST for family in FAMILIES):
                    room += 1
                if arm == 'c20':
                    for family in FAMILIES:
                        passing[family] += per_family[family] / max(len(sends), 1) >= MOST
            print(f'  {matter:20} {case_name}: ' + ' | '.join(cells))
        need = len(case_names) if matter == 'FY2028 gross margin' else (len(case_names) + 1) // 2
        verdict = all(passing[family] >= need for family in FAMILIES)
        opened_ok &= verdict and room >= (len(case_names) + 1) // 2
        print(f'    -> opened in most sends on {passing} of {len(case_names)} cases (needed {need}); cases with room {room}: {"met" if verdict else "NOT met"}')

    print('\nKEPT AND LINKED (named facts of the target cases):')
    kept_ok, exercised_by_matter = True, collections.Counter()
    for case_name, case in cases.items():
        for number, fact in enumerate(case.get('named_facts') or [], 1):
            row = {}
            for arm in ('c8', 'c20'):
                sends = valid[(case_name, arm)]
                kept = {family: 0 for family in FAMILIES}
                linked_same = {family: 0 for family in FAMILIES}
                linked_other = {family: collections.Counter() for family in FAMILIES}
                opened_sends = {family: 0 for family in FAMILIES}
                for record in sends:
                    label = answer_of[(case_name, arm, record['send'])]
                    for family in FAMILIES:
                        found = next((f for f in marks[family][label].get('facts') or [] if f.get('fact') == number), None)
                        if found and found.get('kept'):
                            kept[family] += 1
                        if opens(family, label, fact['matter']):
                            opened_sends[family] += 1
                            matches = (found or {}).get('link_match') or []
                            if 'same' in matches:
                                linked_same[family] += 1
                            else:
                                linked_other[family][', '.join(matches) or 'not linked'] += 1
                row[arm] = (len(sends), kept, linked_same, opened_sends, linked_other)
            total_c8, kept_c8 = row['c8'][0], row['c8'][1]
            total_c20, kept_c20, same_c20, opened_c20, other_c20 = row['c20']
            exercised = any(kept_c8[f] or kept_c20[f] for f in FAMILIES)
            keep_line = all(kept_c20[f] / max(total_c20, 1) >= kept_c8[f] / max(total_c8, 1) - 1 / 3 - 1e-9 for f in FAMILIES)
            link_line = all(opened_c20[f] == 0 or same_c20[f] / opened_c20[f] >= MOST for f in FAMILIES)
            if exercised:
                exercised_by_matter[fact['matter']] += 1
                kept_ok &= keep_line and link_line
            print(f"  {case_name} fact {number} ({fact['matter']}): kept c8 {dict(kept_c8)}/{total_c8}, c20 {dict(kept_c20)}/{total_c20}; "
                  f"linked to its own question in c20 {dict(same_c20)} of the sends that opened it {dict(opened_c20)}"
                  + (f"; otherwise {({f: dict(other_c20[f]) for f in FAMILIES})}" if any(other_c20[f] for f in FAMILIES) else '')
                  + ('' if exercised else '  [not exercised]') + ('' if (keep_line and link_line) or not exercised else '  <-- line not met'))
    kept_ok &= all(exercised_by_matter[matter] for matter in MATTERS)
    print(f'    -> exercised facts per matter {dict(exercised_by_matter)}: {"met" if kept_ok else "NOT met"}')

    print('\nNUMBER CARDS and TWICE IN ONE ANSWER (by what the question asks; all ten cases):')
    card = {arm: collections.defaultdict(lambda: {family: 0 for family in FAMILIES}) for arm in ('c8', 'c20')}
    twice = {arm: collections.defaultdict(lambda: {family: 0 for family in FAMILIES}) for arm in ('c8', 'c20')}
    differences = []
    for label, row in sorted(key.items()):
        per_family_cards, per_family_pairs = {}, {}
        for family in FAMILIES:
            questions = marks[family][label].get('questions') or []
            cards = sorted(q['id'] for q in questions if q.get('asks') in ('other_line', 'quarter', 'other_company')
                           or (q.get('asks') in ('revenue', 'gross_margin') and q.get('fiscal_year') == 'later'))
            pairs = sorted(tuple(sorted(pair.get('ids') or [])) for pair in marks[family][label].get('pairs') or [])
            per_family_cards[family], per_family_pairs[family] = cards, pairs
            if cards:
                card[row['arm']][row['case']][family] += 1
            if pairs:
                twice[row['arm']][row['case']][family] += 1
        if per_family_cards['codex'] != per_family_cards['claude'] or per_family_pairs['codex'] != per_family_pairs['claude']:
            differences.append((label, row['case'], row['arm'], row['send'], per_family_cards, per_family_pairs))
    for name, table in (('number card', card), ('twice in one answer', twice)):
        for arm in ('c8', 'c20'):
            total = sum(len(rows) for (case, a), rows in valid.items() if a == arm)
            print(f"  {name}, {arm}: by case {({case: dict(counts) for case, counts in table[arm].items()})}; "
                  f"sends with one, of {total}: " + ', '.join(f"{family} {sum(counts[family] for counts in table[arm].values())}" for family in FAMILIES))
    print(f'  reader differences on cards or pairs: {len(differences)}')
    for difference in differences:
        print('     ', difference)

    print('\nSUPPRESSION (the stored thesis, by subject; each such thesis is in the listing):')
    for case_name, pattern in KEEP.items():
        per_arm = {}
        for arm in ('c8', 'c20'):
            sends = valid[(case_name, arm)]
            opened = sum(1 for record in sends if any(thesis.get('opens_as') != 'main_driver' and pattern.search(thesis.get('description', ''))
                                                      for thesis in record.get('new_theses') or []))
            per_arm[arm] = (opened, len(sends))
        control = per_arm['c8'][0] / max(per_arm['c8'][1], 1)
        candidate = per_arm['c20'][0] / max(per_arm['c20'][1], 1)
        state = 'control absent, cannot judge' if control < MOST else ('SUPPRESSED' if control - candidate >= MOST else 'not suppressed')
        print(f"  {case_name}: c8 {rate(*per_arm['c8'])}, c20 {rate(*per_arm['c20'])}: {state}")

    print('\nREPORTED: g1 (the bare reported figure):')
    for arm in ('c8', 'c20'):
        sends = valid[('g1-guard', arm)]
        print(f"  {arm}: new questions in {sum(1 for record in sends if record.get('new_theses'))} of {len(sends)} sends")
    print(f'\nopened: {"met" if opened_ok else "NOT met"}; kept and linked: {"met" if kept_ok else "NOT met"}')


if __name__ == '__main__':
    main()
