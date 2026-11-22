"""The readers' packet for the July test (reading-rule.md): the six sequences' v9 and v14 answers under shuffled labels (the key kept
outside the repository), each sequence's first-attempt refusals, and the material both arms were shown, once per question and day
(control-1's requests without their previous-conclusion section, which differs per sequence).

  python3 build_packet.py <send folder> <key folder>
"""
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

SEQUENCES = ['control-1', 'linked-1', 'control-2', 'linked-2', 'control-3', 'linked-3']
TARGETS = ('v9', 'v14')


def answers(folder):
    summary = json.loads((folder / 'summary.json').read_text())
    conn = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
    rows = conn.execute('select view_id, publication_day, rung, reference, implied_outcome, reasons, cited_evidence_json, cited_views_json, changed, why_changed '
                        'from judgements where seq > 147 and view_id in (?, ?) order by judgement_id', TARGETS).fetchall()
    archive = sqlite3.connect(f'file:{folder / "archive.sqlite"}?mode=ro', uri=True)
    refusals = [json.loads(r[0])['messages'][-1]['content'].split(' ', 2)[1] for r in archive.execute(
        "select request_json from model_calls where purpose='judge' and call_id > ? and request_sha256 like '%:refused:%'", (summary.get('archive_top', 0),))]
    return summary, rows, refusals


def without_previous(text):
    return re.sub(r'\n\[Previous conclusion[^\n]*(?:\n(?!\[)[^\n]*)*', '\n', text)


def main():
    send, key_dir = Path(sys.argv[1]), Path(sys.argv[2])
    labels = [f'sequence-{letter}' for letter in 'KLMNPQ']
    random.SystemRandom().shuffle(labels)
    key, lines = {}, ['# Readers\' packet: six sequences of two questions, NVIDIA, 2026-07-10 to 2026-07-12', '',
                      'v9: "How much Data Center segment revenue will NVIDIA report for FY2027?"; v14: "How much total revenue will NVIDIA report',
                      'for FY2027?". Each sequence judged both questions each day it was due, from the same starting state. Apply `reading-rule.md`',
                      '(A to D and the pass line) to each sequence. The material both questions were shown each day is at the end.', '']
    for label, name in sorted(zip(labels, SEQUENCES)):
        summary, rows, refusals = answers(send / name)
        key[label] = {'sequence': name, 'linked': summary.get('linked'), 'stopped': summary.get('stopped'), 'links': summary.get('links')}
        lines += [f'## {label}', f'- first-attempt refusals: {refusals or "none"}']
        for view_id, day, rung, reference, implied, reasons, cites, cites_views, changed, why in rows:
            lines += [f'### {view_id} on {day}: rung {rung}, changed {bool(changed)}', f'- reference: {reference}', f'- implied outcome: {implied}',
                      f'- reasons: {reasons}', f'- cites: {cites}; cites_views: {cites_views}', f'- why changed: {why}', '']
    lines += ['## The material shown (control-1\'s requests, previous conclusion removed)', '']
    archive = sqlite3.connect(f'file:{send / "control-1" / "archive.sqlite"}?mode=ro', uri=True)
    ledger = sqlite3.connect(f'file:{send / "control-1" / "views.sqlite"}?mode=ro', uri=True)
    for view_id, day, call_id in ledger.execute('select view_id, publication_day, call_id from judgements where seq > 147 and view_id in (?, ?) order by judgement_id', TARGETS):
        request_json = archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0]
        text = json.loads(request_json)['messages'][-1]['content']
        lines += [f'### request for {view_id} on {day}', '```', without_previous(text), '```', '']
    (send / 'reader-packet.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    key_dir.mkdir(parents=True, exist_ok=True)
    (key_dir / 'key.json').write_text(json.dumps(key, indent=1))
    print('packet', send / 'reader-packet.md', 'key', key_dir / 'key.json')


if __name__ == '__main__':
    main()
