"""Eligible cases for a measurement of D375, step 2 ($0; D528): reader packets. For each question the old system opened before the last
article of its day (fresh-week run), the statements that later articles of that day produced, as the reading step wrote them: those
kept under other questions, those dropped for want of a question, and (unmarked, as known cases) those the system did file under the
question that day. One packet holds at most 60 statements of one question, in shuffled order; the key (which statement is which) goes
to a folder outside the repository.

  python3 build_same_day_packets.py <key folder outside the repository>
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

RUN = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week/p1/prod')
HERE = Path(__file__).resolve().parent
SEED, MOST = 20261115, 60


def main():
    key_folder = Path(sys.argv[1])
    key_folder.mkdir(parents=True, exist_ok=True)
    store = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    days = [(row[1], row[2]) for row in store.execute('select * from days_completed order by 1')]
    handovers = {seq: (input_id, json.loads(text)) for input_id, seq, text in store.execute('select input_id, seq, handover_json from handovers')}
    rng, key, packets = random.Random(SEED), [], []
    for view_id, opened, question, due_day in store.execute('select view_id, created_seq, question, due_day from views where created_seq > 0 order by created_seq'):
        day, day_end = next((d, end) for d, end in days if opened <= end)
        later = sorted(seq for seq in handovers if opened < seq <= day_end)
        if not later:
            continue
        rungs = store.execute('select position, label, condition from rungs where view_id = ? order by position', (view_id,)).fetchall()
        statements = []
        for evidence_id, one_line, quote, who, seq in store.execute('select evidence_id, one_line, quote, original_who, created_seq from evidence where created_seq > ? and created_seq <= ?', (opened, day_end)):
            reached = store.execute('select 1 from evidence_links where evidence_id = ? and view_id = ? and seq <= ?', (evidence_id, view_id, day_end)).fetchone()
            statements.append({'status': 'filed under this question that day' if reached else 'kept under other questions', 'stored_id': evidence_id, 'article': seq,
                               'summary': one_line, 'passage': quote, 'attribution': who})
        for seq in later:
            input_id, handover = handovers[seq]
            dropped = [d[0] for d in handover.get('dropped') or [] if d[1] == 'no home']
            if not dropped:
                continue
            row = archive.execute("select answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{input_id}%',)).fetchone()
            answer = json.loads(row[0]) if row and row[0] else {'evidence': []}
            for local_id in dropped:
                statement = next((e for e in answer['evidence'] if e.get('id') == local_id), None)
                if statement is None:
                    raise SystemExit(f'article {seq}: dropped statement {local_id} is not in the stored answer: refused')
                statements.append({'status': 'dropped for want of a question', 'stored_id': f'{seq}:{local_id}', 'article': seq, 'summary': statement.get('one_line'),
                                   'passage': statement.get('quote'), 'attribution': statement.get('original_who') or statement.get('speaker')})
        rng.shuffle(statements)
        for part, start in enumerate(range(0, len(statements), MOST), 1):
            chunk = statements[start:start + MOST]
            name = f'{view_id}-{part}'
            lines = [f'# Packet {name}', '', f'**The question:** {question}', '', f'Due {due_day}. Possible answers:'] + [f'- {p} {label}: {condition}' for p, label, condition in rungs]
            lines += ['', f'**{len(chunk)} statements read on {day}:**', '']
            for number, statement in enumerate(chunk, 1):
                item = f'{name}-{number}'
                key.append({'item': item, 'question': view_id, 'packet': name, **{k: statement[k] for k in ('status', 'stored_id', 'article')}})
                lines += [f"- **{item}** (stored attribution: {statement['attribution']}): {statement['summary']}", f"  - Passage: \"{statement['passage']}\""]
            (HERE / f'packet-{name}.md').write_text('\n'.join(lines) + '\n')
            packets.append((name, len(chunk)))
    (key_folder / 'same-day-key.json').write_text(json.dumps(key, indent=1, ensure_ascii=False) + '\n')
    (HERE / 'packets.json').write_text(json.dumps(packets) + '\n')
    counts = {}
    for row in key:
        counts[row['status']] = counts.get(row['status'], 0) + 1
    print(f'{len(packets)} packets, {len(key)} statement-and-question items: {counts}')
    print('packets:', packets)


if __name__ == '__main__':
    main()
