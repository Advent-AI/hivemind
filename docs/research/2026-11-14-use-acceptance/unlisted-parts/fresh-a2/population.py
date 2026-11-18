"""FRESH-A2-DESIGN.md v4's population ($0): the development matters, the blind classer's packet of the fresh topics, and the two
readers' classes joined (disagreement = uncertain).

  python3 population.py packet <fresh cases.json> <output packet>
  python3 population.py join <packet> <codex answers> <claude answers>

Development matters: the 66 stored topics read while developing arms A to A3 (`../topics-66.txt`, their description and outcome) and
Alex's 44 Stage A cases (`clean-arch/step4-2026-11-10/stage_a/cases.json`)."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CLASSES = ('development matter', 'different matter', 'uncertain')


def development_matters():
    matters, name = [], None
    for line in (HERE.parent / 'topics-66.txt').read_text().splitlines():
        if line and not line.startswith(' '):
            name = line.strip()
            matters.append({'id': f'stored {name}', 'description': '', 'outcome': ''})
        elif re.match(r'\s+D: ', line):
            matters[-1]['description'] = line.split('D: ', 1)[1]
        elif re.match(r'\s+O: ', line):
            matters[-1]['outcome'] = line.split('O: ', 1)[1]
    for case in json.loads((ROOT / 'clean-arch/step4-2026-11-10/stage_a/cases.json').read_text()):
        matters.append({'id': f'stage-a {case["case"]}', 'description': case['thesis']['description'], 'outcome': case['thesis']['outcome']})
    if len(matters) != 110 or any(not matter['description'] for matter in matters):
        raise SystemExit(f'development matters: {len(matters)} read, not 110 with descriptions')
    return matters


def packet(cases_path, output):
    cases = json.loads(Path(cases_path).read_text())
    topics = [{'id': case['case'], 'description': case['thesis']['description'], 'outcome': case['thesis']['outcome'],
               'opening_article': {'title': case['item']['title'], 'day': case['item']['publication_date']}} for case in cases]
    Path(output).write_text(json.dumps({'fresh_topics': topics, 'development_matters': development_matters()}, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(topics)} fresh topics against 110 development matters: {output}')


def join(packet_path, *answer_paths):
    topics = [topic['id'] for topic in json.loads(Path(packet_path).read_text())['fresh_topics']]
    given = []
    for path in answer_paths:
        rows = {row['id']: row['class'] for row in map(json.loads, (line for line in Path(path).read_text().splitlines() if line.strip().startswith('{')))}
        if sorted(rows) != sorted(topics) or any(value not in CLASSES for value in rows.values()):
            raise SystemExit(f'{path}: not one class from {CLASSES} for each fresh topic')
        given.append(rows)
    joined = {topic: given[0][topic] if all(rows[topic] == given[0][topic] for rows in given) else 'uncertain' for topic in topics}
    print(json.dumps(joined, indent=1))
    return joined


if __name__ == '__main__':
    command, arguments = sys.argv[1], sys.argv[2:]
    if command == 'packet':
        packet(*arguments)
    elif command == 'join':
        join(*arguments)
    else:
        print(__doc__)
