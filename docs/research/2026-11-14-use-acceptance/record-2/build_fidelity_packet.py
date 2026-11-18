"""The record test on unread articles, the fidelity sample ($0; RECORD-TEST-2-DESIGN.md, check 2): twenty seeded lines of each record
(seed 20261123) under shuffled labels F01..F40, each with the article it came from (title, publisher, text) and the statement's passages.
A merged line is checked against its first article. Written whole (for a Claude reader) and in parts of ten (for Codex readers). The key
goes outside the repository.

  python3 build_fidelity_packet.py <key folder outside the repository>
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def lines_of_view(label):
    found, heading = {}, None
    for line in (HERE / f'views-record-{label}.md').read_text().splitlines():
        if line.startswith('## '):
            heading = line[3:]
        match = re.match(r'- \[([AB]-\d{3})\] \*\*(.*?)\*\* \| (\w+) \| source: (.*?) \| basis: (.*?) \| said: (.*?) \| articles (.*)', line)
        if match:
            measure, _, period = heading.rpartition(' | ')
            found[match.group(1)] = {'measure': measure, 'period': period, 'value': match.group(2), 'kind': match.group(3),
                                     'source': match.group(4), 'basis': match.group(5), 'said': match.group(6)}
    return found


def main():
    key_folder = Path(sys.argv[1])
    articles = {article['article']: article for article in json.loads((HERE / 'articles-unread.json').read_text())}
    rng = random.Random(20261123)
    sampled = []
    for label in ('A', 'B'):
        lines, trace = lines_of_view(label), json.loads((HERE / f'views-rows-{label}.json').read_text())
        assert set(lines) == set(trace), 'every line of the view must be in its trace'
        for line_id in rng.sample(sorted(lines), 20):
            member = trace[line_id][0]
            sampled.append((line_id, lines[line_id], member))
    rng.shuffle(sampled)
    rows, key = [], {}
    for number, (line_id, line, member) in enumerate(sampled, 1):
        label = f'F{number:02d}'
        key[label] = line_id
        rows.append({'row': label, 'article': member['article'], 'passages': member['passages'], **line})
    for name, chosen in [('whole', rows)] + [(f'part{index + 1}', rows[index * 10:(index + 1) * 10]) for index in range(4)]:
        needed = sorted({row['article'] for row in chosen})
        (HERE / f'fidelity-packet-{name}.json').write_text(json.dumps({'articles': [articles[number] for number in needed], 'rows': chosen}, ensure_ascii=False, indent=1))
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'record-2-key-fidelity.json').write_text(json.dumps(key, indent=1))
    print(f'{len(rows)} rows (20 of each record) over {len({row["article"] for row in rows})} articles; whole and four parts of ten written; key outside the repository')


if __name__ == '__main__':
    main()
