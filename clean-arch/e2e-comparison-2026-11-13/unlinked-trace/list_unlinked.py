"""D456's $0 trace, the listing step: for every view a draw opened that the matching ties to a ruler question, and every decisive item reader
B used for that question, whether the draw kept any evidence from the item's own article, whether that evidence arrived before the view
opened, and whether any of it was linked to the view. Prints every not-linked case with the kept items from that article and the views they
were linked to, for a hand read (the fact-level class is read by Claude, not by this script).

  python3 list_unlinked.py p1 p2 p3 q1 q2 q3 c1 c2 c3
"""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'poc/data'
GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
E = ROOT / 'clean-arch/e2e-comparison-2026-11-13'


def draw_sources():
    full = json.loads((E / 'full-matching-answers/mapping-full-views.json').read_text())
    earlier = json.loads((E / 'matching/mapping-prod.json').read_text())
    sources = {}
    for draw in ('p1', 'p2', 'p3'):
        sources[draw] = (DATA / f'clean-e2e-full-2026-11-13/{draw}/prod/views.sqlite', full[draw])
    for draw in ('c1', 'c2', 'c3'):
        sources[draw] = (DATA / f'clean-e2e-full-2026-11-13/{draw}/judge/draw-{draw}/views.sqlite', full[draw])
    for draw in ('q1', 'q2', 'q3'):
        sources[draw] = (DATA / f'clean-e2e-comparison-2026-11-13/draw-{draw}/views.sqlite', earlier[f'production-{draw}'])
    return sources


def classify(draw, database, mapping, gold, items, show):
    conn = sqlite3.connect(f'file:{database}?mode=ro', uri=True)
    questions = dict(conn.execute('select view_id, question from views'))
    counts = Counter()
    for view, ruler_question in sorted(mapping.items()):
        view_seq = conn.execute('select created_seq from views where view_id=?', (view,)).fetchone()[0]
        for item_id in gold[ruler_question].get('decisive_items', []):
            item = items[item_id]
            kept = conn.execute(
                'select e.evidence_id, e.created_seq, e.one_line, (select group_concat(l.view_id) from evidence_links l where l.evidence_id = e.evidence_id) '
                'from evidence e join evidence_sources s on s.evidence_id = e.evidence_id where s.input_id = ? order by e.created_seq, e.evidence_id',
                (item['input_id'],)).fetchall()
            if not kept:
                counts['not kept'] += 1
                continue
            linked = any(links and view in links.split(',') for _, _, _, links in kept)
            timing = 'before' if min(seq for _, seq, _, _ in kept) < view_seq else 'after or same'
            counts[f'{timing}, {"linked" if linked else "not linked"}'] += 1
            if not linked and show:
                print(f'\n## {draw} {view} (opened seq {view_seq}) = {ruler_question}: {questions[view][:110]}')
                meaning = item['meaning'] if isinstance(item['meaning'], str) else item['meaning'].get('what', '')
                print(f'   decisive {item_id} ({item["day"]}, {item["who"]}): {meaning[:160]} | passage: {item["passage"][:160]}')
                for evidence_id, seq, line, links in kept:
                    names = '; '.join(f'{v}: {questions[v][:50]}' for v in (links or '').split(',') if v)
                    print(f'     {evidence_id} seq {seq} -> [{names}] | {line[:150]}')
    conn.close()
    return counts


def main(draws):
    gold = {e['question_id']: e for e in json.loads((GOLD / 'gold-v1.json').read_text())['entries']}
    items = {i['id']: i for i in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    sources = draw_sources()
    totals = {}
    for draw in draws:
        database, mapping = sources[draw]
        totals[draw] = classify(draw, database, mapping, gold, items, show=True)
    print('\n# counts (article level)')
    for draw, counts in totals.items():
        print(draw, dict(counts))


if __name__ == '__main__':
    main(sys.argv[1:])
