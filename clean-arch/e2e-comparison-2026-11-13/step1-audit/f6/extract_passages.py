"""F6's class, made auditable (D461, council round 8): every c8 send of D441's memory diagnostic that opened no memory-price thesis, with
each passage of its stored reasoning that mentions a date, a release, a series, a period or a price level near a memory or shared-quantity
word, for a reader to classify (the future settling date; a price series or level; the source's or article's date; another concern).
The pattern only finds passages; it decides nothing.

  python3 extract_passages.py > passages.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RECORDS = ROOT / 'poc/data/clean-step1-gate2-memory-completion-2026-11-13/combined-records.jsonl'
MEMORY = re.compile(r'(?i)DRAM|HBM|memory')
NEAR = re.compile(r'(?i)\b(date|release|series|settle|period|price level|specific (price|figure|number)|no (clear |specific )?figure)\b')
SHARED = re.compile(r'(?i)shared[_ ]quantity|contract pric|memory pric|DRAM pric|thesis')


def reasoning(record):
    texts = []
    for attempt in record['attempts']:
        message = attempt['response']['choices'][0]['message']
        texts.append(message.get('reasoning_content') or '')
    return '\n'.join(texts)


def main():
    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    declined = [r for r in rows if r['arm'] == 'c8' and not any(
        MEMORY.search(t.get('description', '') + t.get('outcome', '')) for t in r.get('new_theses', []))]
    out = []
    for record in declined:
        text = reasoning(record)
        sentences = re.split(r'(?<=[.?!])\s+', text)
        passages = []
        for index, sentence in enumerate(sentences):
            if NEAR.search(sentence) and SHARED.search(' '.join(sentences[max(0, index - 2):index + 3])):
                passages.append(' '.join(sentences[max(0, index - 1):index + 2])[:600])
        out.append({'id': f"{record['case']}/send-{record['send']}", 'reasoning_chars': len(text), 'passages': passages[:6]})
    print(json.dumps({'declined_sends': len(declined), 'total_c8_sends': sum(r['arm'] == 'c8' for r in rows), 'sends': out},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
