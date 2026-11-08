"""Step 2 retrieval arms over stored Step 1 items, strictly forward: an item searches only items from earlier articles.

One query per {thesis, evidence} association. Arms:
  R0  production as written: word overlap (views/matching._words, the same scoring as rank_evidence) within the linked thesis, top 10;
      a thesis with no earlier items has no candidates.
  R0e the same word overlap over the entity's earlier items, any thesis.
  R1  embedding of each stored item (summary, passages, party, time, period); query = thesis question + incoming summary and passages;
      cosine over the entity's earlier items, top 10.
  R2  R1 without the thesis in the query.
Embeddings are fetched once per text with the repository's embedding helper and cached in the output folder; `--dry-run` counts texts
and tokens (estimated as characters / 4) without sending.

Usage: retrieve.py <folder with items.json> [--dry-run]"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import search  # noqa: E402
from hivemind.views import matching  # noqa: E402

TOP = 10


def item_text(it):
    parts = [it['summary'], ' '.join(it['passages']), f"party: {it['original_party'] or 'unknown'}",
             f"stated: {it['statement_date'] or it['statement_date_text'] or 'unknown'}", f"period: {it['evidence_period'] or 'unknown'}"]
    return '\n'.join(parts)


def query_text(it, thesis):
    body = it['summary'] + '\n' + ' '.join(it['passages'])
    return (f"thesis: {thesis['question']}\n" + body) if thesis else body


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


def main():
    folder = Path(sys.argv[1])
    dry = '--dry-run' in sys.argv
    items = json.loads((folder / 'items.json').read_text())
    texts = {}
    for it in items:
        texts[f"doc:{it['key']}"] = item_text(it)
        texts[f"q2:{it['key']}"] = query_text(it, None)
        for thesis in it['theses']:
            texts[f"q1:{it['key']}:{thesis['id']}"] = query_text(it, thesis)
    cache_path = folder / 'embeddings.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    missing = [k for k in texts if k not in cache]
    est_tokens = sum(len(texts[k]) for k in missing) // 4
    print(f'texts {len(texts)}, to embed {len(missing)}, about {est_tokens} tokens, about ${est_tokens / 1e6 * 0.02:.4f} at $0.02/M ({search.EMBEDDING_MODEL})')
    if dry:
        return
    used = 0
    for start in range(0, len(missing), 64):
        chunk = missing[start:start + 64]
        vectors, tokens = search.openai_embeddings([texts[k] for k in chunk])
        used += tokens
        cache.update({k: v for k, v in zip(chunk, vectors)})
    cache_path.write_text(json.dumps(cache))
    print(f'embedded {len(missing)} texts, {used} tokens reported')
    words = {it['key']: matching._words(it['summary'] + ' ' + ' '.join(it['passages'])) for it in items}
    results = []
    for j, it in enumerate(items):
        earlier = [e for e in items[:j] if e['article'] < it['article']]
        target = matching._words(it['summary'])
        r2 = sorted(earlier, key=lambda e: -cosine(cache[f"q2:{it['key']}"], cache[f"doc:{e['key']}"]))[:TOP]
        r0e = sorted(earlier, key=lambda e: -len(target & words[e['key']]))[:TOP]
        for thesis in it['theses']:
            same = [e for e in earlier if thesis['id'] in {t['id'] for t in e['theses']}]
            r0 = sorted(same, key=lambda e: -len(target & words[e['key']]))[:TOP]
            r1 = sorted(earlier, key=lambda e: -cosine(cache[f"q1:{it['key']}:{thesis['id']}"], cache[f"doc:{e['key']}"]))[:TOP]
            results.append({'key': it['key'], 'thesis': thesis['id'], 'R0': [e['key'] for e in r0], 'R0e': [e['key'] for e in r0e],
                            'R1': [e['key'] for e in r1], 'R2': [e['key'] for e in r2]})
    (folder / 'retrieval.json').write_text(json.dumps(results, indent=1))
    print(f'associations {len(results)}; with no earlier same-thesis item (R0 empty) {sum(1 for r in results if not r["R0"])}')


if __name__ == '__main__':
    main()
