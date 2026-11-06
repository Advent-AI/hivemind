"""Blind packet for condition 4 of `benchmark-design.md`: every article-opened question of the given window draws, shuffled with a fixed seed, each
with its opening article (title, publisher, day), the passages written with it, and the questions open in its own ledger just before it (for the
duplicate test). Run and arm are replaced by a neutral id; the key goes to a separate file the reader is never given. Fields whose form shows which
architecture wrote the question (the focus line with its check method and date basis, the due day, a research-subject id) are left out; a research
subject is shown by its name.

    python3 blind_questions.py <packet.json> <key.json> <label>=<run> [<label>=<run> ...]"""
import json
import random
import sqlite3
import sys

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'


def questions(run):
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    rows = [dict(r) for r in conn.execute('select view_id, object_id, question, looks_at, due_day, created_seq, created_from_input from views order by created_seq')]
    has_subjects = conn.execute("select 1 from sqlite_master where name='research_subjects'").fetchone() is not None
    names = dict(conn.execute('select object_id, name from research_subjects').fetchall()) if has_subjects else {}
    out = []
    for v in rows:
        if (v['created_from_input'] or '').startswith('seed:'):
            continue
        item = items.execute('select title, publisher, publication_day from items where input_id=?', (v['created_from_input'],)).fetchone()
        passages = [r[0] for r in conn.execute('select e.quote from evidence e join evidence_links l using(evidence_id) where l.view_id=? and e.created_seq=?',
                                               (v['view_id'], v['created_seq']))]
        before = []
        for p in rows:
            if p['created_seq'] >= v['created_seq']:
                continue
            switch = conn.execute('select open from view_switches where view_id=? and after_seq<? order by after_seq desc, id desc limit 1', (p['view_id'], v['created_seq'])).fetchone()
            if switch and switch[0]:
                before.append(f'{names.get(p["object_id"], p["object_id"])}: {p["question"]}')
        out.append({'question': v['question'], 'subject': names.get(v['object_id'], v['object_id']),
                    'article': {'title': item[0], 'publisher': item[1], 'day': item[2]} if item else {'id': v['created_from_input']},
                    'opening_passages': passages, 'open_questions_before': before, '_view': v['view_id']})
    return out


def main():
    packet_path, key_path, *runs = sys.argv[1:]
    entries = []
    for argument in runs:
        label, run = argument.split('=', 1)
        entries += [dict(q, _source=label) for q in questions(run)]
    random.Random(20261106).shuffle(entries)
    packet, key = [], {}
    for index, entry in enumerate(entries, 1):
        qid = f'Q{index:03d}'
        key[qid] = {'source': entry.pop('_source'), 'view_id': entry.pop('_view')}
        packet.append(dict(entry, id=qid))
    json.dump(packet, open(packet_path, 'w'), ensure_ascii=False, indent=1)
    json.dump(key, open(key_path, 'w'), indent=1)
    print(f'{len(packet)} questions in the packet; key written apart')


if __name__ == '__main__':
    main()
