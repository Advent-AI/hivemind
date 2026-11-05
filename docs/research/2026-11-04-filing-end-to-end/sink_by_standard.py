"""What the total-revenue question's pile is, by the frozen rulers rather than by my reading (AGENTS §7.1): every statement linked to the
question in a frozen v108 draw, set beside the frozen extraction gold (golden-v5: per article, the matters kept with their weight and the
spans not kept with the standard's row) and the frozen judgement gold (gold-v1: which questions reader B cites each kept matter for).

For a statement whose article the extraction gold read, the closest gold span (kept or not kept) by shared figures and words is taken and
printed beside it, so every match is read; a statement whose article the gold did not read is counted apart.

usage: python3 sink_by_standard.py <draw folder> <question view id> [--list]
"""
import collections
import json
import re
import sqlite3
import sys

STANDARD = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5'
JUDGEMENT = '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold'
WORD = re.compile(r'[a-z]{4,}|\d+(?:\.\d+)?')


def words(text):
    return set(WORD.findall((text or '').lower()))


def main():
    folder, view_id = sys.argv[1], sys.argv[2]
    listing = '--list' in sys.argv
    articles = {}
    for part in ('dev', 'test'):
        for article in json.load(open(f'{STANDARD}/golden-v5-{part}.json'))['articles']:
            articles[article['input_id']] = article
    packet = json.load(open(f'{JUDGEMENT}/packet-v1.json'))['items']
    by_passage = {(i['input_id'], i['passage']): i['id'] for i in packet}
    cited_for = collections.defaultdict(set)
    for entry in json.load(open(f'{JUDGEMENT}/gold-v1.json'))['entries']:
        for field in ('reference', 'implied_outcome', 'against'):
            for item_id in ((entry.get(field) or {}).get('items') or []):
                cited_for[item_id].add(entry['question_id'])
        for item_id in entry.get('decisive_items') or []:
            cited_for[item_id].add(entry['question_id'])
    views = sqlite3.connect(f'file:{folder}/views.sqlite?mode=ro', uri=True)
    rows = views.execute('select e.evidence_id, e.quote, e.one_line, (select input_id from evidence_sources s where s.evidence_id=e.evidence_id order by rowid limit 1) '
                         'from evidence_links l join evidence e using(evidence_id) where l.view_id=? order by l.id', (view_id,)).fetchall()
    tally, out = collections.Counter(), []
    for evidence_id, quote, one_line, input_id in rows:
        others = [r[0] for r in views.execute('select view_id from evidence_links where evidence_id=? and view_id<>?', (evidence_id, view_id))]
        article = articles.get(input_id)
        if not article:
            tally['article not in the extraction gold'] += 1
            out.append((evidence_id, 'not read by gold', '', '', one_line, others))
            continue
        mine = words(quote + ' ' + one_line)
        spans = [('kept', i['weight'], i['span'], i) for i in article['items']] + [('not kept', n['row'], n['span'], n) for n in article['not_kept']]
        best = max(spans, key=lambda s: len(mine & words(s[2])), default=None)
        if not best or len(mine & words(best[2])) < 3:
            tally['article read, no matching gold span'] += 1
            out.append((evidence_id, 'no span', '', '', one_line, others))
            continue
        status, label, span, raw = best
        if status == 'kept':
            item_id = by_passage.get((input_id, span))
            questions = sorted(cited_for.get(item_id, set())) if item_id else []
            key = f'kept {label}; reader B cites it for ' + (', '.join(questions) if questions else 'no question')
            tally[f'kept {label}'] += 1
            tally['  of which cited for q01' if 'q01' in questions else ('  of which cited only for other questions' if questions else '  of which cited for no question')] += 1
        else:
            key = 'not kept: ' + label[:60]
            tally['not kept by the standard'] += 1
        out.append((evidence_id, key, span[:110], '', one_line, others))
    print(f'{folder} {view_id}: {len(rows)} linked statements')
    for k, n in tally.items():
        print(f'  {k}: {n}')
    if listing:
        for evidence_id, key, span, _, one_line, others in out:
            print(f'\n{evidence_id} [{key}] also {others}\n    ledger: {one_line[:170]}\n    gold:   {span}')


if __name__ == '__main__':
    main()
