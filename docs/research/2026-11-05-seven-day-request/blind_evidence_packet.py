"""Blind-reader packet for evidence: a fixed-seed sample of the passages each run wrote in its first 100 rows, from the new-question call
(passages under the question that article opened) and from the evidence call (passages under existing questions), each with the question
it was filed under and the article title. Shuffled; the reader judges helpful or not helpful under the standard's section 5 (D372).
Usage: blind_evidence_packet.py OUT PER_LANE RUN_A RUN_B"""
import json, random, sqlite3, sys
from pathlib import Path

def passages(run):
    status = json.loads((run / 'run-status.json').read_text()); start = status['starting_seq']
    conn = sqlite3.connect(f"file:{run / 'snapshot/views.sqlite'}?mode=ro", uri=True); conn.row_factory = sqlite3.Row
    manifest = json.loads((run / 'manifest.json').read_text()); first = {r['id'] for r in manifest['input_rows'][:100]}
    seqs = {r['sequence_no'] for r in conn.execute("select input_id, sequence_no from processing_steps where step='dispatched' and sequence_no>?", (start,)) if r['input_id'] in first}
    rows = conn.execute('''select e.evidence_id, e.quote, e.one_line, e.created_seq, l.view_id, v.question, v.created_seq as view_seq
                           from evidence e join evidence_links l using(evidence_id) join views v using(view_id) where e.created_seq>?''', (start,)).fetchall()
    out = {'opening': [], 'existing': []}
    for r in rows:
        if r['created_seq'] not in seqs:
            continue
        user = json.loads((run / 'items' / str(r['created_seq']) / 'b-request.json').read_text())['messages'][-1]['content']
        title = user[user.index('[Item]'):].split('\n')[0].split('title:')[-1].strip()[:200]
        lane = 'opening' if r['view_seq'] == r['created_seq'] else 'existing'
        out[lane].append({'evidence_id': r['evidence_id'], 'question': r['question'], 'quote': r['quote'], 'summary': r['one_line'], 'article_title': title})
    return out

def main(out, per_lane, run_a, run_b):
    rng = random.Random(20261105); items = []; key = {}
    for run in (run_a, run_b):
        found = passages(run)
        for lane, rows in found.items():
            rows = sorted(rows, key=lambda r: r['evidence_id'])
            for r in rng.sample(rows, min(per_lane, len(rows))):
                items.append(r); key[id(r)] = {'run': str(run), 'lane': lane, 'evidence_id': r['evidence_id'], 'population': len(rows)}
    rng.shuffle(items)
    packet = []; answer_key = {}
    for i, r in enumerate(items, 1):
        packet.append({'item': f'E{i:03d}', 'question': r['question'], 'article_title': r['article_title'], 'quote': r['quote'], 'summary': r['summary']})
        answer_key[f'E{i:03d}'] = key[id(r)]
    out.mkdir(parents=True, exist_ok=False)
    (out / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (out / 'key.json').write_text(json.dumps(answer_key, indent=1) + '\n')
    print(len(packet), 'passages')

if __name__ == '__main__':
    main(Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
