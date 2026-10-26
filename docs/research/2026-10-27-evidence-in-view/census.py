"""What the judge would have been shown under each candidate reading rule, measured on stored ledgers ($0).

For every judgement after a thesis's first: F = evidence in force at that round; S = what the rule would show; the loss is a
citation the judge actually made that lies outside S (the judge used something the rule hides). Rules:
  J1  cited by the previous judgement + linked or replaced since it
  J2  J1 + every fact / party_statement piece in force
  J3  cited by any earlier judgement of the thesis + linked or replaced since the previous one
  J4  J3 + every fact / party_statement piece in force
  WK  (K readings) cited by any earlier judgement of the thesis + every piece linked or replaced within the last K judgements
      (a piece is read K times; what no judgement used in K readings leaves the judge's view, staying in force in the ledger)
  MmKk cited by one of the last m judgements + linked or replaced within the last k judgements (the working set also decays)
Run: python3 census.py <views.sqlite> [...]"""
import collections
import json
import sqlite3
import statistics
import sys

STANDING = ('fact', 'party_statement')


def measure(path):
    v = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    v.row_factory = sqlite3.Row
    tier = {r['evidence_id']: r['tier'] for r in v.execute('select evidence_id, tier from evidence')}
    replaced_at = {r['old_evidence_id']: r['seq'] for r in v.execute('select old_evidence_id, seq from replacements')}
    links = collections.defaultdict(list)
    for r in v.execute('select view_id, evidence_id, seq from evidence_links order by id'):
        links[r['view_id']].append((r['evidence_id'], r['seq']))
    new_at = collections.defaultdict(set)
    for r in v.execute('select new_evidence_id, seq from replacements'):
        new_at[r['seq']].add(r['new_evidence_id'])

    def in_force(view_id, seq):
        return [e for e, s in links[view_id] if s <= seq and not (e in replaced_at and replaced_at[e] <= seq)]

    def since(view_id, a, b):
        fresh = {e for e, s in links[view_id] if a < s <= b}
        for s, ids in new_at.items():
            if a < s <= b:
                fresh |= ids
        return fresh

    rules = ('J1', 'J2', 'J3', 'J4', 'W1', 'W2', 'W3', 'W5', 'M3K3', 'M5K3', 'M10K3', 'M10K5')
    sizes = {r: [] for r in rules}
    sizes_big = {r: [] for r in rules}
    lost_j = collections.Counter()
    lost_c = collections.Counter()
    lost_tier = {r: collections.Counter() for r in rules}
    force_sizes, later, cites_total, examples = [], 0, 0, []
    history = collections.defaultdict(list)     # view -> [(judgement_id, seq, cited)]
    for j in v.execute('select view_id, seq, cited_evidence_json, judgement_id from judgements order by judgement_id'):
        cited = set(json.loads(j['cited_evidence_json'] or '[]'))
        earlier = list(history[j['view_id']])              # the judgements before this one (a copy: the list is about to grow)
        history[j['view_id']].append((j['judgement_id'], j['seq'], cited))
        if not earlier:
            continue
        later += 1
        cites_total += len(cited)
        prev_seq, prev_cited = earlier[-1][1], earlier[-1][2]
        ever = set().union(*(c for _, _, c in earlier))
        force = set(in_force(j['view_id'], j['seq']))
        fresh = since(j['view_id'], prev_seq, j['seq'])
        standing = {e for e in force if tier.get(e) in STANDING}
        shown = {'J1': (prev_cited | fresh) & force, 'J3': (ever | fresh) & force}
        shown['J2'] = shown['J1'] | standing
        for k in (1, 2, 3, 5):
            start = earlier[-k][1] if len(earlier) >= k else -1
            shown[f'W{k}'] = (ever | since(j['view_id'], start, j['seq'])) & force
        for m, k in ((3, 3), (5, 3), (10, 3), (10, 5)):
            recent = set().union(*(c for _, _, c in earlier[-m:]))
            start = earlier[-k][1] if len(earlier) >= k else -1
            shown[f'M{m}K{k}'] = (recent | since(j['view_id'], start, j['seq'])) & force
        shown['J4'] = shown['J3'] | standing
        force_sizes.append(len(force))
        for rule in rules:
            sizes[rule].append(len(shown[rule]))
            if len(force) >= 50:
                sizes_big[rule].append(len(shown[rule]))
            lost = cited - shown[rule]
            if lost:
                if rule == 'W3' and len(examples) < 8:
                    examples.append((j['view_id'], j['seq'], sorted(lost)[:3]))
                lost_j[rule] += 1
                lost_c[rule] += len(lost)
                for e in lost:
                    lost_tier[rule][tier.get(e, '?')] += 1
    big = [f for f in force_sizes if f >= 50]
    print(f'\n{path}\n  later judgements {later}, cites {cites_total}; in force: mean {statistics.mean(force_sizes):.1f}, '
          f'max {max(force_sizes)}; judgements with >= 50 in force: {len(big)} (mean {statistics.mean(big):.1f})')
    print('  rule | shown mean (all) | shown mean / max (>=50 in force) | judgements with a hidden cite | hidden cites | hidden by tier')
    for rule in rules:
        print(f'  {rule} | {statistics.mean(sizes[rule]):.1f} | {statistics.mean(sizes_big[rule]):.1f} / {max(sizes_big[rule])} | '
              f'{lost_j[rule]} ({lost_j[rule] / later:.0%}) | {lost_c[rule]} ({lost_c[rule] / cites_total:.1%}) | {dict(lost_tier[rule])}')
    print('  W3 examples (view, seq, hidden cites):', examples)


if __name__ == '__main__':
    for path in sys.argv[1:]:
        measure(path)
