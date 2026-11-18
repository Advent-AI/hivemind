"""The record test on unread articles, the comparers' packet ($0; RECORD-TEST-2-DESIGN.md): the six answer sets (two reference sets from the
articles, four record sets: a reader of each family on each record), part by part, under labels S1..S6 drawn anew for each question with
a fixed seed. Each record answer comes with the text of the record lines it cites, so the comparer can check the answer rests on them;
reference answers keep their article numbers and quotes. Answers are read from the readers' files by parsing (several objects may share
a part: Q2 and Q6 list one object per estimate or pair). The key goes outside the repository.

  python3 build_compare_packet.py <key folder outside the repository>
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETS = {'codex-reference': 'reference', 'claude-reference': 'reference', 'codex-record-A': 'record', 'codex-record-B': 'record',
        'claude-record-A': 'record', 'claude-record-B': 'record'}
PARTS = {'Q1': ['a', 'b'], 'Q2': ['a'], 'Q3': ['a', 'b'], 'Q4': ['a', 'b', 'c'], 'Q5': ['a', 'b'], 'Q6': ['a']}


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"question"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def lines_of_view(label):
    found = {}
    for line in (HERE / f'views-record-{label}.md').read_text().splitlines():
        match = re.match(r'- \[([AB]-\d{3})\] (.*)', line)
        if match:
            found[match.group(1)] = match.group(2)
    return found


def main():
    key_folder = Path(sys.argv[1])
    view_lines = {label: lines_of_view(label) for label in ('A', 'B')}
    headings = {}
    for label in ('A', 'B'):
        heading = None
        for line in (HERE / f'views-record-{label}.md').read_text().splitlines():
            if line.startswith('## '):
                heading = line[3:]
            match = re.match(r'- \[([AB]-\d{3})\]', line)
            if match:
                headings[match.group(1)] = heading
    answers = {}
    for name in SETS:
        by_part = collections.defaultdict(list)
        for row in objects(HERE / f'{name}.jsonl'):
            if row.get('question') in PARTS:
                by_part[(row['question'], str(row.get('part') or 'a'))].append(row)
        answers[name] = by_part
        missing = [f'{q}{p}' for q, parts in PARTS.items() for p in parts if not by_part.get((q, p))]
        if missing:
            print(f'{name}: no answer given for {missing}')
    rng = random.Random(20261125)
    packet, key = [], {}
    for question, parts in PARTS.items():
        names = list(SETS)
        rng.shuffle(names)
        key[question] = {f'S{index}': name for index, name in enumerate(names, 1)}
        for part in parts:
            entry = {'question': question, 'part': part, 'sets': {}}
            for index, name in enumerate(names, 1):
                rows = answers[name].get((question, part)) or []
                shown = []
                for row in rows:
                    item = {'answer': row.get('answer')}
                    if SETS[name] == 'record':
                        label = name[-1]
                        item['cited_lines'] = [{'heading': headings.get(line_id), 'line': view_lines[label].get(line_id, '(no such line)')}
                                               for line_id in row.get('lines') or []]
                    else:
                        item['articles'] = row.get('articles')
                        item['quotes'] = row.get('quotes')
                    shown.append(item)
                entry['sets'][f'S{index}'] = {'kind': 'answered from a record' if SETS[name] == 'record' else 'answered from the articles',
                                              'answers': shown or [{'answer': '(no answer given for this part)'}]}
            packet.append(entry)
    (HERE / 'compare-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'record-2-key-compare.json').write_text(json.dumps(key, indent=1))
    print(f'{len(packet)} parts over {len(PARTS)} questions, six sets each; labels drawn per question; key outside the repository; '
          f'packet {len(json.dumps(packet))} characters')


if __name__ == '__main__':
    main()
