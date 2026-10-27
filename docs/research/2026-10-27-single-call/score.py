"""Score an arm's sends at sentence level: a piece is the sentence its quote covers (the cleaned text split as the
reading rule splits it), so two cuts of one sentence count as the same piece. Per article: pieces per send, empty sends,
distinct sentences, sentences in every send and in a majority of sends, mean pairwise Jaccard, links used.
Run: python3 score.py <scratch archive> <cleaned items db> <system file or v12> [min call_id]"""
import collections
import itertools
import json
import re
import sqlite3
import sys

W_ROLE = __file__.rsplit('/docs/', 1)[0] + '/src/hivemind/prompts/role-v12.txt'
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[“"A-Z])')
ABBREVIATION = re.compile(r'\b(U\.S|U\.K|Inc|Corp|Co|Ltd|Mr|Mrs|Ms|Dr|Jr|Sr|vs|e\.g|i\.e|No|St|Fig|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.$')


def sentences(text):
    out = []
    for line in text.split('\n'):
        merged = []
        for part in SPLIT.split(line):
            if merged and ABBREVIATION.search(merged[-1]):
                merged[-1] += ' ' + part
            else:
                merged.append(part)
        out.extend(merged)
    return out


def norm(text):
    return re.sub(r'\W+', ' ', text or '').strip().lower()


def sentence_of(quote, sents):
    q = norm(quote)
    for i, s in enumerate(sents):
        if q[:60] in s or s[:60] in q:
            return i
    return '?' + q[:30]


def main(scratch, items_db, system_file, min_call=0, purpose=None):
    conn = sqlite3.connect(f'file:{scratch}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    items = sqlite3.connect(f'file:{items_db}?mode=ro', uri=True)
    system = open(system_file if system_file != 'v12' else W_ROLE, encoding='utf-8').read()
    by_article = collections.defaultdict(list)
    for r in conn.execute("select call_id, purpose, request_json, answer_json, output_tokens, cost_usd from model_calls where call_id >= ? and purpose like 'benchmark:%' or purpose like 'arm:%' order by call_id", (min_call,)):
        if r['call_id'] < min_call:
            continue
        req = json.loads(r['request_json']); sent_system = req['messages'][0]['content']
        if sent_system != system or (purpose and r['purpose'] != purpose):
            continue
        iid = re.search(r'\[Item\] id (\S+),', req['messages'][1]['content']).group(1)
        data = json.loads(r['answer_json'])
        pieces = data.get('evidence') if 'evidence' in data else [p for e in (data.get('paragraphs') or {}).values() for p in e.get('statements', [])] + list(data.get('extra') or [])
        by_article[iid].append((pieces, r['cost_usd']))
    print('| article | pieces per send | empty | distinct sentences | in every send | in ≥3 of 5 | mean Jaccard | links used | USD |')
    print('|---|---|---|---|---|---|---|---|---|')
    for iid, sends in by_article.items():
        text, = items.execute('select text from items where input_id=?', (iid,)).fetchone()
        sents = [norm(s) for s in sentences(text)]
        sets = [{sentence_of(p['quote'], sents) for p in pieces} for pieces, _ in sends]
        union = set().union(*sets); common = set.intersection(*sets) if sets else set()
        counter = collections.Counter(x for s in sets for x in s)
        pairs = [len(a & b) / len(a | b) if a | b else 1.0 for a, b in itertools.combinations(sets, 2)]
        links = sorted({l for pieces, _ in sends for p in pieces for l in p['links']})
        print(f"| {iid[:24]} | {[len(p) for p, _ in sends]} | {sum(1 for p, _ in sends if not p)} | {len(union)} | {len(common)} | {sum(1 for v in counter.values() if v >= 3)} | {sum(pairs)/len(pairs) if pairs else 1:.2f} | {links} | {sum(c for _, c in sends):.4f} |")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 0, sys.argv[5] if len(sys.argv) > 5 else None)
