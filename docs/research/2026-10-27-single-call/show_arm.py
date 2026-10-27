"""Print an arm's pieces compactly for reading against the reference lists: per article, per send, each piece's tier,
links and one_line. Run: python3 show_arm.py <scratch archive> <purpose> [max pieces per send]"""
import json
import re
import sqlite3
import sys


def main(scratch, purpose, limit=20):
    conn = sqlite3.connect(f'file:{scratch}?mode=ro', uri=True)
    by_article = {}
    for request, answer in conn.execute("select request_json, answer_json from model_calls where purpose=? order by call_id", (purpose,)):
        iid = re.search(r'\[Item\] id (\S+),', json.loads(request)['messages'][1]['content']).group(1)
        by_article.setdefault(iid, []).append(json.loads(answer))
    for iid, sends in by_article.items():
        print(f'\n##### {iid}')
        for n, data in enumerate(sends, 1):
            pieces = data.get('evidence') if 'evidence' in data else [q for e in (data.get('paragraphs') or {}).values() for q in e.get('statements', [])] + list(data.get('extra') or [])
            print(f'  send {n}: {len(pieces)} pieces, {len(data.get("candidates") or [])} candidates')
            for p in pieces[:limit]:
                print(f"     [{p['tier'][:5]}] {','.join(p['links']) or '-':10} {p['one_line'][:125]}")
            for c in data.get('candidates') or []:
                print(f"     CAND {c.get('opens_as')}: {c.get('question', '')[:110]}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20)
