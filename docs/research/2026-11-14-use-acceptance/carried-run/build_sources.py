"""Reading 3 of PLAN.md, a sample ($0): for five questions drawn by seed 20261116, the question's last judgement request and the
fortnight's articles the run linked to it or that a reading-1 reader flagged as holding a fact for it (at most six articles a
question, flagged first, then the latest linked). A positive control is mixed in as a sixth question: the custom-chip question's
stored July request (draw d1 of the frozen v108 run, as in PRD 10's one test) with the articles that carry the facts whose
addition moved its answer off the lowest rung in 9 of 9 sends. Blinded and shuffled; the key outside the repository.

  python3 build_sources.py <run root> <key folder>
"""
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'clean-arch/step4-2026-11-10/stage_b'))
import stored_judgements  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEED = 20261116
JULY = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
GOLD_ITEMS = ['i234', 'i139', 'i300', 'i155', 'i138']


def flagged_by_readers():
    """Articles a reading-1 reader flagged with a fact for a held question: {question: [input ids]}."""
    key = json.loads((Path(sys.argv[2]) / 'key-openings.json').read_text())
    packet = json.loads((HERE / 'packet-openings.json').read_text())
    trace = sqlite3.connect(f"file:{Path(sys.argv[1]) / 'c1/step1/trace.sqlite'}?mode=ro", uri=True)
    input_of = dict(trace.execute('select sequence, input_id from trace'))
    out = {}
    for family in ('codex', 'claude'):
        path = HERE / f'{family}-openings.jsonl'
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line.strip().startswith('{'):
                continue
            row = json.loads(line)
            if ':' in row['ref']:
                continue
            for fact in row.get('lost_facts') or []:
                out.setdefault(fact.get('question'), set()).add(input_of[int(key[row['ref']])])
    return {question: sorted(ids) for question, ids in out.items()}


def article(items, input_id):
    title, publisher, day, text = items.execute('select title, publisher, publication_day, text from items where input_id = ?', (input_id,)).fetchone()
    return {'title': title, 'publisher': publisher, 'day': day, 'text': text}


def main(run_root, keys):
    run_root, keys = Path(run_root), Path(keys)
    store = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    stored_judgements.refuse_split_store(store, 'build_sources')     # it maps a view to its topic by id (clean-<view number>)
    archive = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    judged = [row[0] for row in store.execute('select distinct view_id from judgements order by view_id')]
    sample = sorted(random.Random(SEED).sample(judged, 5), key=lambda v: int(v[1:]))
    flagged = flagged_by_readers()
    entries = []
    for view in sample:
        sha = store.execute('select request_sha256 from judgements where view_id = ? order by seq desc, judgement_id desc limit 1', (view,)).fetchone()[0]
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])
        user = request['messages'][-1]['content']
        linked = [row[0] for row in store.execute(
            'select s.input_id from evidence_links l join evidence_sources s on s.evidence_id = l.evidence_id where l.view_id = ? '
            'group by s.input_id order by max(s.publication_day) desc', (view,))]
        own = f'clean-{view[1:]}'
        chosen = list(dict.fromkeys(flagged.get(own, []) + linked))[:6]
        entries.append({'source': f'run {view}', 'request': user, 'articles': [article(items, i) for i in chosen],
                        'flagged': [i for i in chosen if i in flagged.get(own, [])]})
    july = sqlite3.connect(f"file:{JULY / 'views.sqlite'}?mode=ro", uri=True)
    july_archive = sqlite3.connect(f"file:{JULY / 'archive.sqlite'}?mode=ro", uri=True)
    sha = july.execute("select request_sha256 from judgements where view_id='v16' order by seq desc limit 1").fetchone()[0]
    stored = json.loads(july_archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])
    gold = {i['id']: i for i in json.loads((ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json').read_text())['items']}
    control_articles = list(dict.fromkeys(gold[i]['input_id'] for i in GOLD_ITEMS))
    entries.append({'source': 'positive control: PRD 10 custom-chip group (July, d1, v16)',
                    'request': next(m['content'] for m in stored['messages'] if m['role'] == 'user'),
                    'articles': [article(items, i) for i in control_articles], 'flagged': []})
    order = random.Random(SEED + 1).sample(entries, len(entries))
    packet = [{'question': n, 'request': e['request'], 'articles': [dict(a, ref=f'A{k}') for k, a in enumerate(e['articles'], 1)]} for n, e in enumerate(order, 1)]
    (HERE / 'packet-sources.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    (keys / 'key-sources.json').write_text(json.dumps({str(n): {'source': e['source'], 'flagged': e['flagged']} for n, e in enumerate(order, 1)}, indent=1) + '\n')
    print(f'sources packet: {len(packet)} questions (5 sampled: {sample}; 1 positive control); {sum(len(p["articles"]) for p in packet)} articles; '
          f'{len((HERE / "packet-sources.json").read_text()):,} characters')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
