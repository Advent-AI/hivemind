"""Question check packets for a Step 1 run against the frozen question gold (golden-v5 must_open / may_open / must_not; no model calls).

Per gold article the run completed: the theses it opened (question and outcome), the theses open after it, and the gold's question lists.
Readers mark each opened thesis as matching a must_open, a may_open or a must_not entry, or none, and each must_open entry as covered or
not by a thesis open after the article (the same underlying question; a fold of the same programme or quantity counts). The packet holds
no run label.

Usage: build_question_packets.py <trace.sqlite[+segment...]> <dev|test> <packet.json>"""
import json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    trace, which, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    gold = {a['input_id']: a for a in json.loads((ROOT / f'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-{which}.json').read_text())['articles']}
    packet = []
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        for iid, result, after in conn.execute("select input_id, result, after_state from trace where status='complete' order by sequence"):
            g = gold.get(iid)
            if not g:
                continue
            q = g['questions']
            r = json.loads(result)
            opened = [{'question': t['description'], 'outcome': t['outcome']} for t in r['new_theses'] if t['local_id'] in r.get('new_thesis_ids', {})]
            if not (opened or q['must_open'] or q['must_not']):
                continue
            packet.append({'article': g.get('title') or iid, 'opened': opened,
                           'open_after': [t['description'] for t in json.loads(after)],
                           'must_open': [x['gist'] for x in q['must_open']], 'may_open': [x['gist'] for x in q['may_open']],
                           'must_not': [x['gist'] for x in q['must_not']]})
    for n, case in enumerate(packet, 1):
        case['id'] = f'A{n}'
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print(f'articles {len(packet)}; opened {sum(len(c["opened"]) for c in packet)}; must_open entries {sum(len(c["must_open"]) for c in packet)}')


if __name__ == '__main__':
    main()
