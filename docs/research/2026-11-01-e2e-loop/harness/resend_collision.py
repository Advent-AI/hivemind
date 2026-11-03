"""Cheapest proof of a collision-judge prompt change (AGENTS §1 step 4, §6): re-send every stored collision request of one run n times
with the stored system prompt and n times with a replacement, and print each peer's verdict side by side with the candidate and peer
questions, then the count of verdicts that moved each way. The bytes are production's, with only the system prompt replaced; about
$0.002 a send.

    python3 resend_collision.py <run folder> <config json> <new system prompt file> <n>
"""
import collections
import json
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402

SENDERS = 8


def main():
    run, cfg_path, new_file, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    cfg = config.load(cfg_path)
    new_system = Path(new_file).read_text(encoding='utf-8').strip()
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    titles = {r[0]: r[1] for r in views.execute('select view_id, question from views')}
    rows = archive.execute("""select call_id, request_json, answer_json from model_calls where purpose='match'
                              and request_json like '%"name": "collision"%' order by call_id""").fetchall()
    print(f'{len(rows)} stored collision requests; {n} sends as stored + {n} with the new prompt ({len(new_system)} chars vs '
          f'{len(json.loads(rows[0][1])["messages"][0]["content"])} stored)', flush=True)

    def send(body):
        content = model.openai_transport(cfg.provider, body)['choices'][0]['message']['content']
        return {r['thesis_id']: r['relation'] for r in json.loads(content).get('relations', [])}

    moved = collections.Counter()
    with ThreadPoolExecutor(SENDERS) as pool:
        jobs = []
        for call_id, request_json, answer_json in rows:
            body = json.loads(request_json)
            edited = json.loads(json.dumps(body)); edited['messages'][0]['content'] = new_system
            jobs.append((call_id, body, json.loads(answer_json or '{}'),
                         [pool.submit(send, json.loads(json.dumps(body))) for _ in range(n)],
                         [pool.submit(send, json.loads(json.dumps(edited))) for _ in range(n)]))
        for call_id, body, stored, control_f, edited_f in jobs:
            control = [f.result() for f in control_f]; edited = [f.result() for f in edited_f]
            user = body['messages'][-1]['content']
            candidate = user.split('\n', 1)[0][:160]
            stored_v = {r['thesis_id']: r['relation'] for r in stored.get('relations', [])}
            print(f'\n## call {call_id} | {candidate}', flush=True)
            for peer in stored_v:
                c = [a.get(peer, '-') for a in control]; e = [a.get(peer, '-') for a in edited]
                print(f'  {peer} {titles.get(peer, "?")[:70]!r}\n     stored {stored_v[peer]} | control {c} | new {e}', flush=True)
                for a, b in zip(c, e):
                    moved[(a, b)] += 1
    print('\n# verdict pairs (control -> new), counted over every peer and send:')
    for (a, b), k in sorted(moved.items(), key=lambda kv: -kv[1]):
        print(f'  {k:3d}  {a} -> {b}')


if __name__ == '__main__':
    main()
