"""Blind packet for `benchmark-design.md` ("What the split was built for"): twenty stored evidence records of each arm, drawn with a fixed seed from
all of the arm's window draws, mixed and shuffled. Each record carries its fields as stored (quote, summary, speaker, original speaker, statement day,
tier, period), the questions it is linked to, and its article (title, publisher, day, the paragraph holding the quote). The arm and draw are replaced
by a neutral id; the key goes to a separate file the reader is never given.

    python3 blind_records.py <packet.json> <key.json> <arm>=<run>,<run>,<run> <arm>=<run>,<run>,<run>"""
import json
import random
import sqlite3
import sys

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
PER_ARM = 20


def records(run):
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    out = []
    for r in conn.execute('select e.*, s.input_id from evidence e join evidence_sources s using(evidence_id) where e.created_seq > 0 order by e.evidence_id'):
        links = [dict(q) for q in conn.execute('select v.view_id, v.object_id, v.question from evidence_links l join views v using(view_id) where l.evidence_id=?',
                                              (r['evidence_id'],))]
        out.append({'record': {k: r[k] for k in ('quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time')},
                    'linked_questions': [f'{q["object_id"]}: {q["question"]}' for q in links], 'input_id': r['input_id'], '_evidence': r['evidence_id']})
    return out


def paragraph(text, quote):
    position = text.find(quote[:60])
    if position < 0:
        return 'NOT FOUND in the stored text'
    start, end = text.rfind('\n', 0, position) + 1, text.find('\n', position + len(quote))
    return text[start:end if end > 0 else len(text)][:1500]


def main():
    packet_path, key_path, *arms = sys.argv[1:]
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    rng = random.Random(20261106)
    chosen = []
    for argument in arms:
        arm, runs = argument.split('=', 1)
        pool = [dict(r, _source=f'{arm} d{draw}') for draw, run in enumerate(runs.split(','), 1) for r in records(run)]
        chosen += rng.sample(pool, PER_ARM)
    rng.shuffle(chosen)
    packet, key = [], {}
    for index, entry in enumerate(chosen, 1):
        rid = f'R{index:03d}'
        title, publisher, day, text = items.execute('select title, publisher, publication_day, text from items where input_id=?', (entry['input_id'],)).fetchone()
        key[rid] = {'source': entry['_source'], 'evidence_id': entry['_evidence'], 'input_id': entry['input_id']}
        packet.append({'id': rid, **entry['record'], 'linked_questions': entry['linked_questions'],
                       'article': {'title': title, 'publisher': publisher, 'day': day, 'paragraph': paragraph(text, entry['record']['quote'])}})
    json.dump(packet, open(packet_path, 'w'), ensure_ascii=False, indent=1)
    json.dump(key, open(key_path, 'w'), indent=1)
    print(f'{len(packet)} records in the packet; key written apart')


if __name__ == '__main__':
    main()
