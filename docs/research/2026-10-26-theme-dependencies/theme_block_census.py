#!/usr/bin/env python3
"""Zero-cost census for the D191 theme block: on a stored ledger, for every judgement of a company thesis, which open theme
theses had a current state at that moment (one-to-all, Alex's rule), which of them belong to a theme the triggering item was
tagged with (the narrower reading), and what a fan-out of changed theme conclusions to every open company thesis would have cost.

  python3 docs/research/2026-10-26-theme-dependencies/theme_block_census.py --ledger /abs/run-dir [--items /abs/items.sqlite]
"""
import argparse
import collections
import json
import sqlite3

ITEMS = '/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite'


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--items', default=ITEMS)
    args = ap.parse_args()
    conn = ro(f'{args.ledger}/views.sqlite')
    items = ro(args.items)
    kind = {r['view_id']: r['object_kind'] for r in conn.execute('select view_id, object_kind from views')}
    theme_of = {r['view_id']: r['object_id'] for r in conn.execute("select view_id, object_id from views where object_kind='theme'")}
    switches = collections.defaultdict(list)
    for r in conn.execute('select view_id, open, after_seq, id from view_switches order by id'):
        switches[r['view_id']].append((r['after_seq'], r['id'], r['open']))
    judgements = [dict(r) for r in conn.execute('select judgement_id, view_id, seq, input_id, changed, rung, publication_day from judgements order by judgement_id')]

    def open_at(view_id, seq):
        state = None
        for after_seq, _, is_open in switches[view_id]:
            if after_seq <= seq:
                state = is_open
        return bool(state)

    def theme_state_before(theme_id, judgement_id):
        rows = [j for j in judgements if j['view_id'] == theme_id and j['judgement_id'] < judgement_id]
        return rows[-1] if rows else None

    def item_themes(view_id, seq):
        """Themes tagged on the items whose evidence is linked to the thesis by this sequence number (judgements carry 'day:<date>', not an item)."""
        out = set()
        for r in conn.execute('select distinct s.input_id from evidence_links l join evidence_sources s on s.evidence_id=l.evidence_id where l.view_id=? and l.seq<=?', (view_id, seq)):
            row = items.execute('select object_identifiers from items where input_id=?', (r['input_id'],)).fetchone()
            if row and row['object_identifiers']:
                out.update(o['value'] for o in json.loads(row['object_identifiers']) if o.get('kind') == 'theme')
        return out

    company_judgements = [j for j in judgements if kind.get(j['view_id']) == 'company']
    with_block, block_sizes, tagged_sizes, same_round_later = 0, [], [], 0
    per_theme = collections.Counter()
    for j in company_judgements:
        in_force = []
        for theme_view in theme_of:
            if open_at(theme_view, j['seq']) and theme_state_before(theme_view, j['judgement_id']):
                in_force.append(theme_view)
            elif open_at(theme_view, j['seq']) and any(t['view_id'] == theme_view and t['seq'] == j['seq'] and t['judgement_id'] > j['judgement_id'] for t in judgements):
                same_round_later += 1        # the theme was judged in the same round but after this company thesis: ordering matters
        tagged = item_themes(j['view_id'], j['seq'])
        tagged_views = [v for v in in_force if theme_of[v] in tagged]
        if in_force:
            with_block += 1
            block_sizes.append(len(in_force))
            for v in in_force:
                per_theme[theme_of[v]] += 1
        tagged_sizes.append(len(tagged_views))
    # fan-out cost: a theme judgement with a changed conclusion, times the open company theses at that moment
    fanout, extra, extra_first = [], set(), set()
    already = {(j['view_id'], j['seq']) for j in judgements}
    seen_theme = set()
    for j in judgements:
        if kind.get(j['view_id']) == 'theme' and j['changed']:
            first = j['view_id'] not in seen_theme
            seen_theme.add(j['view_id'])
            open_companies = [v for v, k in kind.items() if k == 'company' and open_at(v, j['seq'])]
            fanout.append((j['view_id'], j['seq'], j['publication_day'], len(open_companies), 'first' if first else 'later'))
            for v in open_companies:
                if (v, j['seq']) not in already:
                    extra.add((v, j['seq']))
                    if first:
                        extra_first.add((v, j['seq']))
    print(f"ledger {args.ledger}")
    print(f"judgements: {len(judgements)} (company {len(company_judgements)}, theme {len(judgements) - len(company_judgements)}); theme theses {len(theme_of)}")
    print(f"company judgements that would carry a theme block (one-to-all): {with_block} of {len(company_judgements)}")
    if block_sizes:
        print(f"  block size: min {min(block_sizes)}, median {sorted(block_sizes)[len(block_sizes)//2]}, max {max(block_sizes)}; per theme: {dict(per_theme)}")
    print(f"  theme theses judged later in the same round as the company thesis (ordering would change what it sees): {same_round_later}")
    print(f"company judgements with a tagged theme in force (narrow reading, from the item's object identifiers): {sum(1 for s in tagged_sizes if s)}")
    print(f"theme judgements with a changed conclusion: {len(fanout)} ({sum(1 for f in fanout if f[4]=='first')} first judgements); theme change × open company thesis pairs: {sum(f[3] for f in fanout)}")
    print(f"  additional judgement calls under propagation (distinct asset thesis × round, not judged in that round anyway): {len(extra)}, of which from first theme judgements {len(extra_first)}")
    for f in fanout:
        print('   ', f)


if __name__ == '__main__':
    main()
