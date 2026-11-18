"""The duplicate-question trace, step 1 ($0; D520): for each pair of questions of the old system's fresh-week run that both reviewing
teams called duplicates, one packet holding, for each question, its wording, its possible answers, the stored request of its latest
judgement exactly as the judge received it (the statements shown, the note of statements not shown, the previous answer) and the stored
answer. It also prints, from the stored matching record, why the second question was opened beside the first. Read-only on the run.

  python3 build_pair_packets.py
"""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week/p1/prod')
PAIRS = [('rtx', 'v14', 'v15'), ('rubin', 'v9', 'v11'), ('fy2028', 'v3', 'v5')]


def main():
    store = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    summary = []
    for name, first, second in PAIRS:
        out = [f'# Two questions on one subject (packet {name})', '',
               'Each question was answered by a judge that received only the request printed under it. Labels: question P and question Q.', '']
        shown_ids = {}
        for label, view_id in (('P', first), ('Q', second)):
            question, created_seq, due_day = store.execute('select question, created_seq, due_day from views where view_id = ?', (view_id,)).fetchone()
            rungs = store.execute('select position, label, condition from rungs where view_id = ? order by position', (view_id,)).fetchall()
            seq, day, rung, reference, implied, reasons, sha, call_id = store.execute(
                'select seq, publication_day, rung, reference, implied_outcome, reasons, request_sha256, call_id from judgements where view_id = ? '
                'order by seq desc, judgement_id desc limit 1', (view_id,)).fetchone()
            stored = archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchall()
            if len(stored) != 1:
                raise SystemExit(f'{view_id}: {len(stored)} archived calls with the request key of its latest judgement: refused')
            user = next(m['content'] for m in json.loads(stored[0][0])['messages'] if m['role'] == 'user')
            linked = [row[0] for row in store.execute('select evidence_id from evidence_links where view_id = ?', (view_id,))]
            shown_ids[label] = [evidence_id for evidence_id in linked if f'- {evidence_id} [' in user]
            out += [f'## Question {label}', '', f'**{question}**', '',
                    f'Opened at article {created_seq} of the week; due {due_day}; {len(linked)} statements linked, {len(shown_ids[label])} of them printed in this request. Possible answers:', '']
            out += [f'- {position} {rung_label}: {condition}' for position, rung_label, condition in rungs]
            out += ['', f'### The request of question {label}\'s latest judgement ({day}), as the judge received it', '', '```', user, '```', '',
                    f'### The stored answer of question {label} ({day})', '', f'- Answer: {rung}', f'- Reference: {reference}', f'- What it expects: {implied}', f'- Reasons: {reasons}', '']
            summary.append((name, label, view_id, day, call_id, len(linked), len(shown_ids[label]), len(user)))
        (HERE / f'pair-{name}.md').write_text('\n'.join(out) + '\n')
        source = store.execute('select created_from_input from views where view_id = ?', (second,)).fetchone()[0]
        for shown, decisions in store.execute('select shown_json, decisions_json from match_records where input_id = ? order by id', (source,)):
            for candidate in json.loads(decisions).get('candidates') or []:
                print(f"{name}: when {second} was opened, shown to the deciding call {json.loads(shown).get('candidates')}; recorded reason: {candidate.get('reason')}")
    for row in summary:
        print('packet %s question %s (%s): latest judgement %s, call %s; linked %d, printed in the request %d; request %d characters' % row)


if __name__ == '__main__':
    main()
