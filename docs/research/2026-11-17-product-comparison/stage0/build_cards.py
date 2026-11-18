"""Library export and cards for the comparison's reading (card-spec.md; plan §1.5 F; D672, D673). Both systems write the same store
(views, rungs, judgements, evidence) and send the same judge request, so one reader of both serves every draw.

    python3 build_cards.py <views.sqlite> <archive.sqlite> <items db> <output.json>

Writes, per question the library holds at the end of its run (the cutoff), the card text of card-spec.md: the question, its due day and its
possible answers (each rung's condition, stance labels removed); the latest answer and its reasons; the material the answering request
contained (evidence renumbered per card; matcher notes, ids and the header's focus string removed); the library's other questions in opening
order with their opening days. A question never judged is carded "no answer".
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

RUNG = re.compile(r'rung (\d+) ([^:]*): ')
ITEM = re.compile(r'^- e\d+ \[([^;\]]*); ([^;\]]*);.*?from \S+ (\d{4}-\d{2}-\d{2})\] (.*)$')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def conditions(view_id, conn):
    """{position: condition} with stance labels removed: the store's own conditions, as the system wrote them."""
    return {r['position']: (r['condition'] or r['label'] or '').strip() for r in
            conn.execute('select position, label, condition from rungs where view_id=? order by position', (view_id,))}


def material(request_json):
    """The evidence lines of a judge request, renumbered: [(kind, publisher, day, summary, quote)]. Every other line is dropped."""
    request = json.loads(request_json)
    text = request['messages'][-1]['content']
    items, current = [], None
    for line in text.splitlines():
        m = ITEM.match(line)
        if m:
            current = [m.group(1).strip(), m.group(2).strip(), m.group(3), m.group(4).strip(), '']
            items.append(current)
        elif current is not None and line.startswith('    Quote: '):
            current[4] = line[len('    Quote: '):].strip()
        elif not line.startswith('    '):
            current = None
    return items


def library(views_path, archive_path, items_path):
    conn, archive, items = ro(views_path), ro(archive_path), ro(items_path)
    day_of = lambda input_id: (items.execute('select publication_day from items where input_id=?', (input_id,)).fetchone() or [None])[0]
    views = list(conn.execute('select view_id, question, due_day, created_seq, created_from_input from views order by created_seq'))
    out = []
    for v in views:
        latest = conn.execute('select rung, reasons, request_sha256, seq from judgements where view_id=? order by seq desc limit 1',
                              (v['view_id'],)).fetchone()
        rungs = conditions(v['view_id'], conn)
        entry = {'question_id': v['view_id'], 'question': v['question'], 'due': v['due_day'], 'opened': day_of(v['created_from_input']),
                 'possible_answers': [rungs[p] for p in sorted(rungs)], 'answer': None, 'reasons': None, 'material': []}
        if latest is not None:
            entry['answer'] = rungs.get(latest['rung'])
            entry['reasons'] = latest['reasons']
            row = archive.execute('select request_json from model_calls where request_sha256=? limit 1', (latest['request_sha256'],)).fetchone()
            if row is None:
                raise SystemExit(f"{v['view_id']}: the latest judgement's request is not in the archive")
            entry['material'] = material(row['request_json'])
        out.append(entry)
    return out


def card_text(entry, lib):
    lines = [f"Question: {entry['question']}", f"Due: {entry['due']}", 'Possible answers:']
    lines += [f'- {c}' for c in entry['possible_answers']]
    if entry['answer'] is None:
        lines += ['', 'Latest answer at the cutoff: no answer']
    else:
        lines += ['', f"Latest answer at the cutoff: {entry['answer']}", f"Reason given: {entry['reasons']}", '',
                  f"Material that answer was given ({len(entry['material'])} items, by day):"]
        for k, (kind, publisher, day, summary, quote) in enumerate(sorted(entry['material'], key=lambda m: m[2]), 1):
            lines.append(f'{k}. ({kind}; {publisher}; {day}) {summary}')
            if quote:
                lines.append(f'   Quote: {quote}')
    others = [e for e in lib if e['question_id'] != entry['question_id']]
    lines += ['', 'Other questions in the same library, in opening order:']
    lines += [f"- opened {e['opened']}: {e['question']}" for e in others]
    return '\n'.join(lines)


def main(views_path, archive_path, items_path, out_path):
    lib = library(views_path, archive_path, items_path)
    cards = [{'question_id': e['question_id'], 'answered': e['answer'] is not None, 'text': card_text(e, lib)} for e in lib]
    Path(out_path).write_text(json.dumps({'library': lib, 'cards': cards}, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(lib)} questions, {sum(c["answered"] for c in cards)} answered; material items {sum(len(e["material"]) for e in lib)}')


if __name__ == '__main__':
    main(*sys.argv[1:5])
