"""Score a probe round on golden-v5 and build the blind thesis-and-unfiled packets.

Gold (frozen scorer's matching, kept evidence only; unfiled items do not count as kept): helpful matters kept, core kept, items
matching a not-kept span, per arm, summed over draws. Thesis packets: for each article, every answer's proposed new theses and its
unfiled items, shuffled and labelled, beside the open theses the answer saw, for a blind reader.

Usage: score_round.py <probe folder> <gold manifest> <stored trace> <key output path>"""
import collections, json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-29-ledger-standard'))
import score_gold  # noqa: E402

GOLD = ROOT / 'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json'


def statement(ev):
    return {'quote': ' '.join(ev['source_passages']), 'one_line': ev['summary']}


def main():
    probe, manifest_path, stored, key_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    results = json.loads((probe / 'results.json').read_text())
    manifest = json.loads(manifest_path.read_text())['item_ids']
    gold = {a['input_id']: a for a in json.loads(GOLD.read_text())['articles']}
    conn = sqlite3.connect(f'file:{stored}?mode=ro', uri=True)
    before = {seq: json.loads(b) for seq, b in conn.execute('select sequence, before_state from trace')}
    texts = {}
    for seq, request in conn.execute('select sequence, request from trace'):
        payload = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]
        texts[seq] = {'title': payload['source_item']['title'], 'text': payload['source_item']['text']}
    counts = collections.defaultdict(collections.Counter)
    for r in results:
        arm = r['arm']
        if 'kept_evidence' not in r:
            counts[arm]['failed answers'] += 1
            continue
        a = gold[manifest[r['article'] - 1]]
        kept = r['kept_evidence']
        counts[arm]['answers'] += 1
        counts[arm]['kept items'] += len(kept)
        counts[arm]['unfiled items'] += len(r.get('unfiled', []))
        counts[arm]['new theses'] += len(r['answer']['new_theses'])
        for entry in a['items']:
            if entry['weight'] in ('core', 'supporting'):
                hit = any(score_gold.same_matter(entry, statement(ev)) for ev in kept)
                counts[arm]['helpful total'] += 1
                counts[arm]['helpful kept'] += hit
                if entry['weight'] == 'core':
                    counts[arm]['core total'] += 1
                    counts[arm]['core kept'] += hit
                unfiled_hit = not hit and any(score_gold.same_matter(entry, {'quote': ' '.join(u['passages']), 'one_line': u['summary']}) for u in r.get('unfiled', []))
                counts[arm]['helpful only in unfiled'] += unfiled_hit
        for ev in kept:
            if any(any(score_gold.same(e['span'], q) for q in ev['source_passages']) for e in a['items']):
                continue
            rejected = [nk for nk in a['not_kept'] if any(score_gold.same(nk['span'], q) for q in ev['source_passages'])]
            if rejected and all(nk['weight'] == 'not_kept' for nk in rejected):
                counts[arm]['not-kept kept'] += 1
    for arm, c in counts.items():
        print(f"{arm:12s} answers {c['answers']} failed {c['failed answers']} | helpful {c['helpful kept']}/{c['helpful total']} core {c['core kept']}/{c['core total']} "
              f"| kept items {c['kept items']} unfiled {c['unfiled items']} (helpful only in unfiled {c['helpful only in unfiled']}) | not-kept kept {c['not-kept kept']} | new theses {c['new theses']}")
    chooser = random.Random(5)
    packets, key = [], {}
    for number in sorted({r['article'] for r in results}):
        answers = [r for r in results if r['article'] == number and 'kept_evidence' in r]
        chooser.shuffle(answers)
        labelled = {}
        for index, r in enumerate(answers, 1):
            key[f'{number}:A{index}'] = f"{r['arm']}:d{r['draw']}"
            labelled[f'A{index}'] = {'new_theses': [{'question': t['description'], 'outcome': t['outcome']} for t in r['answer']['new_theses']],
                                     'unfiled_items': [u['summary'] for u in r.get('unfiled', [])]}
        packets.append({'article': number, **texts[number], 'open_theses': [{'id': t['id'], 'question': t['description']} for t in before[number]], 'answers': labelled})
    (probe / 'thesis-packet.json').write_text(json.dumps(packets, ensure_ascii=False, indent=1))
    key_path.write_text(json.dumps(key, indent=1))
    print('thesis packet: articles', len(packets), 'answers', len(key))


if __name__ == '__main__':
    main()
