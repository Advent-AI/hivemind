"""How often a stored judgement cited evidence a card-based judgement could not have seen, at no cost (simulation.md §3).

The card is approximated by a memory of the MEMORY most recently cited pieces of the question; what a card-based judgement sees is
that memory plus the evidence linked since the question's previous judgement. A citation outside both "reaches back". It also reports
how many reach-back citations the matcher had marked as the same claim as a piece in view, and prints a random sample of the rest.

usage: python3 reach_back.py <views.sqlite> [memory=40] [sample=6]
"""
import collections
import json
import random
import sqlite3
import sys


def main():
    path = sys.argv[1]
    memory_size = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    sample = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    v = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    v.row_factory = sqlite3.Row
    same = collections.defaultdict(set)
    for r in v.execute('select old_evidence_id, new_evidence_id from same_claims'):
        same[r[0]].add(r[1]); same[r[1]].add(r[0])
    links = collections.defaultdict(list)
    for r in v.execute('select view_id, evidence_id, seq from evidence_links order by id'):
        links[r['view_id']].append((r['seq'], r['evidence_id']))
    text = {r['evidence_id']: (r['one_line'] or '', r['original_who'] or '', r['original_day'] or '') for r in v.execute('select evidence_id, one_line, original_who, original_day from evidence')}
    memory, previous, reach = {}, {}, []
    judged = cited = 0
    for r in v.execute('select view_id, seq, publication_day, cited_evidence_json from judgements order by seq, judgement_id'):
        vid, cites = r['view_id'], json.loads(r['cited_evidence_json'] or '[]')
        if vid in previous:
            seen = set(list(memory[vid])[-memory_size:]) | {e for s, e in links[vid] if previous[vid] < s <= r['seq']}
            judged += 1
            cited += len(cites)
            reach += [(vid, r['publication_day'], e, bool(same[e] & seen)) for e in cites if e not in seen]
        held = memory.setdefault(vid, collections.OrderedDict())
        for e in cites:
            held.pop(e, None)
            held[e] = True
        previous[vid] = r['seq']
    if not judged:
        sys.exit('no re-judgement found')
    judgements_reaching = len({(x[0], x[1]) for x in reach})
    relays = sum(1 for x in reach if x[3])
    print(f'memory {memory_size}: re-judgements {judged}, reaching back {judgements_reaching} ({judgements_reaching / judged:.0%}); '
          f'citations {cited}, reaching back {len(reach)} ({len(reach) / max(cited, 1):.0%}); marked as the same claim as a piece in view {relays} '
          f'({relays / max(len(reach), 1):.0%})')
    random.seed(7)
    rest = [x for x in reach if not x[3]]
    for vid, day, e, _ in random.sample(rest, min(sample, len(rest))):
        line, who, said = text[e]
        print(f'  {day} {vid} {e}: {line[:150]} [{who} {said}]')


if __name__ == '__main__':
    main()
