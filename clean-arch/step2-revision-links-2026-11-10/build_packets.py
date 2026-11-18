#!/usr/bin/env python3
"""Blind reader packets over the census of relation-carried links (census.py's output). No model call.

Packet A, filing: would an analyst file this statement under this question? Every carried link, mixed with controls a reader cannot
tell apart: a record under a question Step 1 itself filed it under (expected: filed), and a record under a question no record of its
article was filed under (expected: not filed).
Packet B, relation: is the incoming statement a later version of the stored one? Every relation that carried a link, mixed with
relations of draw 1 that two source readers labelled on 2026-11-09 (reports/step2-revision-census-2026-11-09), as calibration.

The key (which case is which) is written outside the repository, to the folder given as the third argument.

Usage: build_packets.py <census json> <packet folder> <key folder>"""
import contextlib, glob, json, random, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import adapter as e2e_adapter  # noqa: E402

DRAWS = ROOT / 'poc/data/clean-e2e-2026-11-09'
EARLIER_LABELS = ROOT / 'reports/step2-revision-census-2026-11-09/comparison-after-challenge.json'
SEED = 20261110
RECORD_FIELDS = ('summary', 'passages', 'tier', 'original_party', 'reporting_speaker', 'statement_date')


def draw_inputs(draw):
    trace = f"{DRAWS}/stage2-clean-d{draw}/trace.sqlite+{DRAWS}/stage2-clean-d{draw}-segment-2/trace.sqlite"
    by_article, library = e2e_adapter.load_draw(trace, DRAWS / f'stage2-clean-d{draw}-segment-2/step2')
    records = {record['id']: record for article in by_article.values() for record in article}
    sources = {}
    for part in trace.split('+'):
        with contextlib.closing(sqlite3.connect(f'file:{part}?mode=ro', uri=True)) as conn:
            for source in json.loads(conn.execute('select source_items from run').fetchone()[0]):
                sources[source['input_id']] = source
    judged = sorted(glob.glob(str(DRAWS / f'stage2-clean-d{draw}/judged*')))[-1]
    with contextlib.closing(sqlite3.connect(f'file:{judged}/views.sqlite?mode=ro', uri=True)) as conn:
        questions = {view_id: {'question': question, 'due_day': due_day} for view_id, question, due_day in conn.execute('select view_id, question, due_day from views')}
        for view_id, label, condition in conn.execute('select view_id, label, condition from rungs order by view_id, position'):
            questions[view_id].setdefault('answers', []).append(f'{label}: {condition}')
    return records, library, sources, questions


def main(census_path, packet_folder, key_folder):
    census = json.loads(Path(census_path).read_text())
    rng = random.Random(SEED)
    inputs = {draw: draw_inputs(draw) for draw in (1, 2, 3)}
    articles, article_alias = {}, {}

    def article_of(draw, input_id):
        if input_id not in article_alias:
            source = inputs[draw][2][input_id]
            article_alias[input_id] = f'A{len(article_alias) + 1:02}'
            articles[article_alias[input_id]] = {name: source.get(name) for name in ('title', 'publisher', 'publication_day', 'text')}
        return article_alias[input_id]

    def statement(draw, record_id):
        record = inputs[draw][0][record_id]
        return {**{name: record.get(name) for name in RECORD_FIELDS}, 'article': article_of(draw, record['input_id'])}

    # ---- packet A: filing
    filing, filing_key = [], []
    seen_controls = set()
    for link in census['carried']:
        draw, record_id, view_id = link['draw'], link['new']['record'], link['question']
        records, library, sources, questions = inputs[draw]
        filing_key.append({'kind': 'carried', 'draw': draw, 'record': record_id, 'question': view_id})
        filing.append({'statement': statement(draw, record_id), 'question': questions[view_id]})
        if (draw, record_id) in seen_controls:
            continue
        seen_controls.add((draw, record_id))
        article_records = [r for r in records.values() if r['input_id'] == records[record_id]['input_id']]
        own = [(r['id'], v) for r in article_records for v in r['thesis_ids'] if v in questions]
        own_of_record = [pair for pair in own if pair[0] == record_id]
        positive = rng.choice(own_of_record or own) if own else None
        if positive:
            filing_key.append({'kind': 'control: filed by Step 1', 'draw': draw, 'record': positive[0], 'question': positive[1]})
            filing.append({'statement': statement(draw, positive[0]), 'question': questions[positive[1]]})
        linked_from_article = {v for r in article_records for v in r['thesis_ids']} | {l['question'] for l in census['carried']
                                                                                      if l['draw'] == draw and l['new']['article'] == records[record_id]['input_id']}
        elsewhere = sorted(v for v in questions if v not in linked_from_article)
        negative = rng.choice(elsewhere)
        filing_key.append({'kind': 'control: no record of the article filed there', 'draw': draw, 'record': record_id, 'question': negative})
        filing.append({'statement': statement(draw, record_id), 'question': questions[negative]})
    order = list(range(len(filing)))
    rng.shuffle(order)
    filing_cases = [{'id': f'F{n + 1:02}', **filing[i]} for n, i in enumerate(order)]
    filing_key = [{'id': f'F{n + 1:02}', **filing_key[i]} for n, i in enumerate(order)]

    # ---- packet B: relation
    pairs, pair_key, seen_pairs = [], [], set()
    for link in census['carried']:
        for old in link['carried_by']:
            identity = (link['draw'], link['new']['record'], old['record'])
            if identity in seen_pairs:
                continue
            seen_pairs.add(identity)
            pair_key.append({'kind': 'carried', 'draw': link['draw'], 'incoming': link['new']['record'], 'stored': old['record']})
            pairs.append({'stored': statement(link['draw'], old['record']), 'incoming': statement(link['draw'], link['new']['record'])})
    earlier = json.loads(EARLIER_LABELS.read_text())['saved_edges']
    in_census = {(k['incoming'], k['stored']) for k in pair_key if k['draw'] == 1}
    for label, count in (('revision', 4), ('repeat', 2), ('different', 2)):
        pool = [edge for edge in earlier if edge['after_challenge'] == label and (edge['incoming'], edge['stored']) not in in_census]
        for edge in rng.sample(pool, min(count, len(pool))):
            pair_key.append({'kind': f'calibration: labelled {label} on 2026-11-09', 'draw': 1, 'incoming': edge['incoming'], 'stored': edge['stored']})
            pairs.append({'stored': statement(1, edge['stored']), 'incoming': statement(1, edge['incoming'])})
    for entry in pair_key:
        if entry['kind'] == 'carried' and entry['draw'] == 1:
            entry['labelled on 2026-11-09'] = next((edge['after_challenge'] for edge in earlier
                                                   if (edge['incoming'], edge['stored']) == (entry['incoming'], entry['stored'])), None)
    order = list(range(len(pairs)))
    rng.shuffle(order)
    relation_cases = [{'id': f'R{n + 1:02}', **pairs[i]} for n, i in enumerate(order)]
    pair_key = [{'id': f'R{n + 1:02}', **pair_key[i]} for n, i in enumerate(order)]

    packet_folder, key_folder = Path(packet_folder), Path(key_folder)
    packet_folder.mkdir(parents=True, exist_ok=True)
    key_folder.mkdir(parents=True, exist_ok=True)
    (packet_folder / 'packet-filing.json').write_text(json.dumps({'articles': articles, 'cases': filing_cases}, ensure_ascii=False, indent=1))
    (packet_folder / 'packet-relation.json').write_text(json.dumps({'articles': articles, 'cases': relation_cases}, ensure_ascii=False, indent=1))
    (key_folder / 'key-filing.json').write_text(json.dumps(filing_key, indent=1))
    (key_folder / 'key-relation.json').write_text(json.dumps(pair_key, indent=1))
    import collections
    print('filing cases', len(filing_cases), dict(collections.Counter(k['kind'] for k in filing_key)))
    print('relation cases', len(relation_cases), dict(collections.Counter(k['kind'] for k in pair_key)))
    print('articles', len(articles), 'characters of article text', sum(len(a['text'] or '') for a in articles.values()))
    print('bytes', {p.name: p.stat().st_size for p in packet_folder.glob('packet-*.json')})


if __name__ == '__main__':
    main(*sys.argv[1:4])
