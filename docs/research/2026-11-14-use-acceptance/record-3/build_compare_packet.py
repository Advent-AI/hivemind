"""The table test, the comparers' packet ($0; TABLE-TEST-DESIGN.md, check 2): the eight answer sets (four from the table, four from the
plain record of the last test), part by part, under labels S1..S8 drawn anew for each question with a fixed seed. Each answer comes with
the text of the lines it cites and the section and block (or heading) they sit under. Answers are read from the readers' files by
parsing. Written whole and, for readers that need shorter packets, in two halves by part. The key goes outside the repository.

  python3 build_compare_packet.py <key folder outside the repository> [--parts Q2a,Q6a --name settle]
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE.parent / 'record-2'
SETS = {'codex-table-1': 'table', 'codex-table-2': 'table', 'claude-table-1': 'table', 'claude-table-2': 'table',
        'codex-record-old': 'record', 'claude-record-old': 'record', 'codex-record-new': 'record', 'claude-record-new': 'record'}
FILES = {'codex-record-old': RECORD / 'codex-record-B.jsonl', 'claude-record-old': RECORD / 'claude-record-B.jsonl'}
PARTS = {'Q1': ['a', 'b'], 'Q2': ['a'], 'Q3': ['a', 'b'], 'Q4': ['a', 'b', 'c'], 'Q5': ['a', 'b'], 'Q6': ['a']}


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"question"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def lines_of(path, prefix):
    """line id -> its place (section and block, or heading) and its text."""
    found, section, block, last = {}, None, None, None
    for line in path.read_text().splitlines():
        if line.startswith('## '):
            section, block = line[3:], None
        elif line.startswith('### '):
            block = line[4:]
        elif line.startswith('    - ') and last:  # one article's own details under a joined line
            found[last]['line'] += ' || ' + line.strip()[2:]
        else:
            match = re.match(rf'- \[({prefix}-\d{{3}})\] (.*)', line)
            if match:
                last = match.group(1)
                found[last] = {'under': section if block is None else f'{section} > {block}', 'line': match.group(2)}
    return found


def main():
    key_folder = Path(sys.argv[1])
    only = sys.argv[sys.argv.index('--parts') + 1].split(',') if '--parts' in sys.argv else None
    name = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else 'whole'
    lines = {'table': lines_of(HERE / 'financial-table.md', 'T'), 'record': lines_of(RECORD / 'views-record-B.md', 'B')}
    answers = {}
    for set_name in SETS:
        by_part = collections.defaultdict(list)
        for row in objects(FILES.get(set_name, HERE / f'{set_name}.jsonl')):
            if row.get('question') in PARTS:
                by_part[(row['question'], str(row.get('part') or 'a'))].append(row)
        answers[set_name] = by_part
        missing = [f'{q}{p}' for q, parts in PARTS.items() for p in parts if not by_part.get((q, p))]
        if missing:
            print(f'{set_name}: no answer given for {missing}')
    rng = random.Random(20261126 if only is None else 20261127)
    packet, key = [], {}
    for question, parts in PARTS.items():
        names = list(SETS)
        rng.shuffle(names)
        key[question] = {f'S{index}': set_name for index, set_name in enumerate(names, 1)}
        for part in parts:
            if only and f'{question}{part}' not in only:
                continue
            entry = {'question': question, 'part': part, 'sets': {}}
            for index, set_name in enumerate(names, 1):
                shown = []
                for row in answers[set_name].get((question, part)) or []:
                    cited = [{'id': line_id, **lines[SETS[set_name]].get(line_id, {'under': None, 'line': '(no such line)'})} for line_id in row.get('lines') or []]
                    shown.append({'answer': row.get('answer'), 'cited_lines': cited})
                entry['sets'][f'S{index}'] = shown or [{'answer': '(no answer given for this part)', 'cited_lines': []}]
            packet.append(entry)
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / f'record-3-key-compare-{name}.json').write_text(json.dumps(key, indent=1))
    (HERE / f'compare-packet-{name}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    if only is None:
        half = (len(packet) + 1) // 2
        for number, chosen in enumerate((packet[:half], packet[half:]), 1):
            (HERE / f'compare-packet-half{number}.json').write_text(json.dumps(chosen, ensure_ascii=False, indent=1))
    print(f'{len(packet)} parts, eight sets each; labels drawn per question; key outside the repository; packet {len(json.dumps(packet))} characters')


if __name__ == '__main__':
    main()
