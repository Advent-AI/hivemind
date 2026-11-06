"""Blind-reader packet: every new question both runs opened in their first 100 rows, shuffled, with the opening article's title and the
question's opening passages, and each run's question ledger (created sequence and question) under a neutral label. The reader judges each
question against the standard's sections 3–4 and D248 without knowing which run or prompt wrote it. Usage: blind_question_packet.py OUT RUN_A RUN_B"""
import json, random, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]

def ledger(run):
    status = json.loads((run / 'run-status.json').read_text()); start = status['starting_seq']
    conn = sqlite3.connect(f"file:{run / 'snapshot/views.sqlite'}?mode=ro", uri=True); conn.row_factory = sqlite3.Row
    manifest = json.loads((run / 'manifest.json').read_text()); first = {r['id'] for r in manifest['input_rows'][:100]}
    seqs = [r['sequence_no'] for r in conn.execute("select input_id, sequence_no from processing_steps where step='dispatched' and sequence_no>?", (start,)) if r['input_id'] in first]
    last = max(s for s in seqs if (run / 'items' / str(s) / 'result.json').exists() or not (run / 'items' / str(s)).exists())
    rows = [dict(r) for r in conn.execute('select view_id, created_seq, object_id, question from views where created_seq<=? order by created_seq', (last,))]
    new = []
    for v in rows:
        if v['created_seq'] <= start:
            continue
        folder = run / 'items' / str(v['created_seq'])
        user = json.loads((folder / 'b-request.json').read_text())['messages'][-1]['content']
        head = user[user.index('[Item]'):].split('\n')[0]
        a = json.loads((folder / 'a-answer.json').read_text())
        q = next((x for x in a['questions'] if x['question'].strip() == v['question'].strip()), None)
        passages = [e['quote'] for e in q['evidence']] if q else []
        new.append({'view_id': v['view_id'], 'created_seq': v['created_seq'], 'question': v['question'], 'article': head[:300],
                    'why_it_matters': q['why_it_matters'] if q else '', 'opening_passages': passages})
    return [{'id': r['view_id'], 'created_seq': r['created_seq'], 'subject': r['object_id'], 'question': r['question']} for r in rows], new

def main(out, run_a, run_b):
    rng = random.Random(20261105)
    labels = ['X', 'Y']; rng.shuffle(labels)
    packet = {'ledgers': {}, 'questions': []}; key = {}
    for label, run in zip(labels, (run_a, run_b)):
        rows, new = ledger(run)
        packet['ledgers'][label] = rows
        for q in new:
            packet['questions'].append(dict(q, ledger=label)); key[f"{label}:{q['view_id']}"] = str(run)
    rng.shuffle(packet['questions'])
    for i, q in enumerate(packet['questions'], 1):
        q['item'] = f'Q{i:02d}'
    out.mkdir(parents=True, exist_ok=False)
    (out / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (out / 'key.json').write_text(json.dumps({q['item']: {'ledger': q['ledger'], 'view_id': q['view_id'], 'run': key[f"{q['ledger']}:{q['view_id']}"]} for q in packet['questions']}, indent=1) + '\n')
    print(len(packet['questions']), 'questions;', {k: len(v) for k, v in packet['ledgers'].items()}, 'ledger rows')

if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
