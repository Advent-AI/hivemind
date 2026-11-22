"""Blind reader packet for the dependency probe: the six final answers under shuffled labels (key kept outside the repo), v14's
09-20 conclusion, and the control request's text (the evidence both arms listed).

  python3 build_reader_packet.py <run folder> <scratch> <key folder>
"""
import json, random, sqlite3, sys
from pathlib import Path

run, scratch, key_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rows = [json.loads(line) for line in open(run / 'answers.jsonl', encoding='utf-8')]
randomizer = random.SystemRandom()
labels = [f'answer-{letter}' for letter in 'PQRSTU'][:len(rows)]
randomizer.shuffle(labels)
key = {}
lines = ['# Blind reading packet: six answers to one judging request (FY2027 Data Center revenue, NVIDIA, 2026-09-20)', '',
         'Each answer below was written for the same question on the same day. Some requests also showed the total-revenue question\'s',
         'conclusion (quoted below); you are not told which. Apply `reading-rule.md` (A to E) to each answer.', '']
conn = sqlite3.connect(scratch / 'old-2-changed.sqlite')
total = conn.execute("select reasons, rung from judgements where view_id='v14' order by judgement_id desc limit 1").fetchone()
lines += ['## v14 (FY2027 total revenue), its 09-20 conclusion', f'rung {total[1]}; reasons: {total[0]}', '']
for label, row in sorted(zip(labels, rows)):
    final = row['attempts'][-1]['answer'] or {}
    key[label] = {'arm': row['arm'], 'sample': row['sample'], 'attempts': len(row['attempts']),
                  'first_attempt_errors': row['attempts'][0]['errors']}
    lines += [f'## {label}', f'- rung {final.get("rung")}; reference: {final.get("reference")}; implied outcome: {final.get("implied_outcome")}',
              f'- cites_views: {final.get("cites_views")}; cites: {final.get("cites")}', f'- reasons: {final.get("reasons")}',
              f'- why changed: {final.get("why_changed")}', '']
(run / 'reader-packet.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'src'))
from hivemind.views import judging                     # noqa: E402
control = sqlite3.connect(scratch / 'old-2-control.sqlite')
control.row_factory = sqlite3.Row
(run / 'control-request-user.txt').write_text(judging.build_prompt(control, 'v9', 'judging-v7')[1], encoding='utf-8')
key_dir.mkdir(parents=True, exist_ok=True)
(key_dir / 'key.json').write_text(json.dumps(key, indent=1), encoding='utf-8')
print('packet', run / 'reader-packet.md', 'key', key_dir / 'key.json')
