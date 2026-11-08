"""Build the Step 2 validation population from a stored Step 1 forward run (no model calls).

Writes items.json: every kept evidence item in forward order, with a stable key '<article seq>:<local id>', its resolved thesis ids
and descriptions, fields, and the source context around each passage. Writes candidate-pairs.json: ordered cross-article pairs from
discovery routes that do not use embeddings, with the route kept apart from the reader packets. Writes exhaustive-sample.json: 30
incoming items drawn uniformly within three article strata, with inclusion probabilities.

Usage: build_reference.py <trace.sqlite> <output folder>"""
import json, random, re, sqlite3, sys
from pathlib import Path

STOP = set('the a an of to in and for on its is as with by that it at from has have be will said says this than more its their they was were are but not or over into about after'.split())
NUM = re.compile(r'\$?\d[\d,]*(?:\.\d+)?\s*(?:billion|million|trillion|bn|tn|%|percent|gw|mw|x)?', re.I)
NAME = re.compile(r'\b[A-Z][A-Za-z0-9&\-]+(?:\s+[A-Z][A-Za-z0-9&\-]+)*')
COMMON_NAMES = {'NVIDIA', 'Nvidia', 'The', 'In', 'It', 'Its', 'A', 'An', 'This', 'According', 'AI', 'U.S', 'US'}


def figures(text):
    return {re.sub(r'\s+', '', f.lower()) for f in NUM.findall(text) if re.search(r'\d', f) and (len(f.strip()) > 2 or '%' in f)}


def names(text):
    return {n for n in NAME.findall(text) if n not in COMMON_NAMES and len(n) > 2}


def words(text):
    return {w for w in re.findall(r"[a-z0-9$%.']+", text.lower()) if w not in STOP and len(w) > 2}


def context(text, passage, width=500):
    at = text.find(passage)
    if at < 0:
        return None
    return text[max(0, at - width): at + len(passage) + width]


def main():
    trace, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    final = json.loads(conn.execute("select after_state from trace where status='complete' order by sequence desc limit 1").fetchone()[0])
    thesis_text = {t['id']: t['description'] for t in final}
    items = []
    for seq, request, result in conn.execute("select sequence, request, result from trace where status='complete' order by sequence"):
        payload = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]
        source = payload['source_item']
        r = json.loads(result)
        local = r.get('new_thesis_ids', {})
        for ev in r['evidence']:
            theses = sorted({local.get(l['target_id'], l['target_id']) for l in ev['links']})
            items.append({'key': f"{seq}:{ev['local_id']}", 'article': seq, 'input_id': source['id'], 'title': source['title'],
                          'publisher': source['publisher'], 'publication_date': source['publication_date'],
                          'summary': ev['summary'], 'passages': ev['source_passages'], 'original_party': ev['original_party'],
                          'reporting_speaker': ev['reporting_speaker'], 'tier': ev['tier'], 'statement_date': ev['statement_date'],
                          'statement_date_text': ev['statement_date_text'], 'evidence_period': ev['evidence_period'],
                          'theses': [{'id': t, 'question': thesis_text.get(t, '(not in final library)')} for t in theses],
                          'context': [context(source['text'], p) for p in ev['source_passages']]})
    for it in items:
        text = it['summary'] + ' ' + ' '.join(it['passages'])
        it['_figures'], it['_names'], it['_words'] = figures(text), names(text), words(it['summary'])
    pairs = []
    for j, later in enumerate(items):
        same_thesis = {}
        for earlier in items[:j]:
            if earlier['article'] == later['article']:
                continue
            routes = []
            if len(earlier['_figures'] & later['_figures']) >= 1 and len(earlier['_names'] & later['_names']) >= 1:
                routes.append('figure+name')
            if len(earlier['_names'] & later['_names']) >= 2:
                routes.append('names')
            union = earlier['_words'] | later['_words']
            if union and len(earlier['_words'] & later['_words']) / len(union) >= 0.25:
                routes.append('jaccard')
            if {t['id'] for t in earlier['theses']} & {t['id'] for t in later['theses']}:
                same_thesis[earlier['key']] = len(earlier['_words'] & later['_words'])
            if routes:
                pairs.append({'earlier': earlier['key'], 'later': later['key'], 'routes': routes})
        for key in sorted(same_thesis, key=lambda k: -same_thesis[k])[:5]:   # the exhaustive sample estimates what this narrower route misses
            hit = next((p for p in pairs if p['earlier'] == key and p['later'] == later['key']), None)
            if hit:
                hit['routes'].append('thesis-rank')
            elif same_thesis[key] >= 3:
                pairs.append({'earlier': key, 'later': later['key'], 'routes': ['thesis-rank']})
    for it in items:
        for field in ('_figures', '_names', '_words'):
            it.pop(field)
    chooser = random.Random(20261107)
    strata = [(1, 40), (41, 80), (81, 115)]
    sample = []
    for low, high in strata:
        pool = [it['key'] for it in items if low <= it['article'] <= high and it['article'] > 1]
        drawn = chooser.sample(pool, min(10, len(pool)))
        sample += [{'key': k, 'stratum': f'{low}-{high}', 'inclusion_probability': round(len(drawn) / len(pool), 4)} for k in drawn]
    (out / 'items.json').write_text(json.dumps(items, ensure_ascii=False, indent=1))
    (out / 'candidate-pairs.json').write_text(json.dumps(pairs, indent=1))
    (out / 'exhaustive-sample.json').write_text(json.dumps(sample, indent=1))
    routes = {}
    for p in pairs:
        for r in p['routes']:
            routes[r] = routes.get(r, 0) + 1
    print(f'items {len(items)}; candidate pairs {len(pairs)}; by route {routes}; later items with a candidate {len({p["later"] for p in pairs})}; '
          f'exhaustive sample {len(sample)}; items without source context {sum(1 for it in items if None in it["context"])}')


if __name__ == '__main__':
    main()
