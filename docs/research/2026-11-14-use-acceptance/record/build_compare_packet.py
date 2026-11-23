"""The company record test, the comparers' packet ($0; RECORD-TEST-DESIGN.md, check 2): the record reader's and the reference reader's
answers to the six questions, part by part, under the labels P and Q drawn anew for each question with a fixed seed, with only the article
numbers each cites (headings and quotes removed, since they would tell the two apart). The key goes outside the repository.

  python3 build_compare_packet.py <record answers.jsonl> <reference answers.jsonl> <key folder outside the repository>
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def answers(path):
    out = {}
    for line in Path(path).read_text().splitlines():
        if line.strip().startswith('{'):
            row = json.loads(line)
            if row.get('question') == 'use':
                continue
            cited = row.get('articles')
            if cited is None:
                cited = sorted({int(n) for text in row.get('lines') or [] for n in re.findall(r'article (\d+)', text)})
            out[(row['question'], str(row.get('part') or 'a'))] = {'answer': row.get('answer'), 'articles': cited}
    return out


def main():
    record, reference, key_folder = answers(sys.argv[1]), answers(sys.argv[2]), Path(sys.argv[3])
    rng = random.Random(20261120)
    packet, key = [], {}
    for question in sorted({q for q, _ in list(record) + list(reference)}):
        record_is_p = rng.random() < 0.5
        key[question] = {'P': 'record' if record_is_p else 'reference', 'Q': 'reference' if record_is_p else 'record'}
        for part in sorted({p for q, p in list(record) + list(reference) if q == question}):
            from_record = record.get((question, part), {'answer': '(no answer given for this part)', 'articles': []})
            from_reference = reference.get((question, part), {'answer': '(no answer given for this part)', 'articles': []})
            packet.append({'question': question, 'part': part, 'P': from_record if record_is_p else from_reference,
                           'Q': from_reference if record_is_p else from_record})
    (HERE / 'compare-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    (key_folder / 'record-key-compare.json').write_text(json.dumps(key, indent=1))
    print(f'{len(packet)} parts over {len(key)} questions; labels drawn per question; key outside the repository')


if __name__ == '__main__':
    main()
