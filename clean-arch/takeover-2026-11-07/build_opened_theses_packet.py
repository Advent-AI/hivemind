"""Source-backed thesis review packet (no model calls): every thesis a Step 1 run opened, with its outcome, the evidence filed under it
across the run, the theses open just before the article that opened it, and that article's full text. Readers use the same prompt as
the dev review (disputed-prompt.md): bet, small or duplicate.

Usage: build_opened_theses_packet.py <trace.sqlite> <packet.json> <key.json>"""
import collections, json, sqlite3, sys
from pathlib import Path


def main():
    trace, out, key_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    filed = collections.defaultdict(list)
    opened = []
    for seq, request, result, before in conn.execute("select sequence, request, result, before_state from trace where status='complete' order by sequence"):
        source = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']
        answer = json.loads(result)
        ids = answer.get('new_thesis_ids', {})
        for ev in answer['evidence']:
            for link in ev['links']:
                filed[ids.get(link['target_id'], link['target_id'])].append(ev['summary'])
        for proposed in answer['new_theses']:
            if proposed['local_id'] in ids:
                opened.append({'thesis_id': ids[proposed['local_id']], 'question': proposed['description'], 'outcome': proposed['outcome'],
                               'open_before': [t['description'] for t in json.loads(before)],
                               'article': {'title': source['title'], 'publisher': source['publisher'], 'date': source['publication_date'], 'text': source['text']}})
    packet, key = [], {}
    for n, case in enumerate(opened, 1):
        key[f'C{n}'] = case['thesis_id']
        packet.append({'id': f'C{n}', 'thesis': case['question'], 'outcome': case['outcome'], 'evidence_filed': filed[case['thesis_id']],
                       'theses_open_at_that_moment': case['open_before'], 'article': case['article']})
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    key_path.write_text(json.dumps(key, indent=1))
    print(f'theses opened {len(packet)}')


if __name__ == '__main__':
    main()
