"""The table on the fresh week, the comparers' packet ($0; TABLE-WEEK-DESIGN.md version 2, step 4): for each matter the frozen key and the four
table readers' answers under labels S1..S4 drawn anew for each matter with a fixed seed. Every figure an answer gives comes with the
lines it cites: where each sits, its text, and for each article on the line the stored passages (so a figure found through another
article can be checked against that article's own passage). Answers are read from the readers' files by parsing. The label key goes
outside the repository.

  python3 build_week_compare.py <key folder outside the repository> [--name settle --matters M02]
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETS = ['codex-week-table-1', 'codex-week-table-2', 'claude-week-table-1', 'claude-week-table-2']
MATTERS = ['M01', 'M02', 'M03']


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"matter"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def table_lines():
    found, section, block, last = {}, None, None, None
    for line in (HERE / 'financial-table-week.md').read_text().splitlines():
        if line.startswith('## '):
            section, block = line[3:], None
        elif line.startswith('### '):
            block = line[4:]
        elif line.startswith('    - ') and last:
            found[last]['line'] += ' || ' + line.strip()[2:]
        else:
            match = re.match(r'- \[(T-\d{3})\] (.*)', line)
            if match:
                last = match.group(1)
                found[last] = {'under': f'{section} > {block}', 'line': match.group(2)}
    return found


def main():
    key_folder = Path(sys.argv[1])
    name = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else 'whole'
    only = sys.argv[sys.argv.index('--matters') + 1].split(',') if '--matters' in sys.argv else MATTERS
    key = json.loads((HERE / 'week-key.json').read_text())
    lines, trace = table_lines(), json.loads((HERE / 'table-rows-week.json').read_text())
    answers = {}
    for set_name in SETS:
        by_matter = collections.defaultdict(list)
        for row in objects(HERE / f'{set_name}.jsonl'):
            if row.get('matter') in MATTERS:
                by_matter[row['matter']].append(row)
        answers[set_name] = by_matter
    rng = random.Random(20261128 if name == 'whole' else 20261129)
    packet, labels = [], {}
    for matter in MATTERS:
        names = list(SETS)
        rng.shuffle(names)
        labels[matter] = {f'S{index}': set_name for index, set_name in enumerate(names, 1)}
        if matter not in only:
            continue
        entry = {'matter': matter, 'key': key['key'].get(matter) or [], 'sets': {}}
        for index, set_name in enumerate(names, 1):
            shown = []
            for row in answers[set_name].get(matter) or []:
                cited = []
                for line_id in row.get('lines') or []:
                    place = lines.get(line_id)
                    cited.append({'id': line_id, 'under': place['under'] if place else None, 'line': place['line'] if place else '(no such line)',
                                  'stored_passages': [{'article': member['article'], 'passages': member['passages']} for member in trace.get(line_id, [])]})
                shown.append({'group': row.get('group'), 'value': row.get('value'), 'period': row.get('period'), 'whose': row.get('whose'),
                              'note': row.get('note'), 'cited_lines': cited})
            entry['sets'][f'S{index}'] = shown or [{'value': None, 'note': '(no answer given for this matter)'}]
        packet.append(entry)
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / f'record-3-key-week-compare-{name}.json').write_text(json.dumps(labels, indent=1))
    (HERE / f'week-compare-packet-{name}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print(f'{len(packet)} matters, four answers each; key items {[len(entry["key"]) for entry in packet]}; packet {len(json.dumps(packet))} characters')


if __name__ == '__main__':
    main()
