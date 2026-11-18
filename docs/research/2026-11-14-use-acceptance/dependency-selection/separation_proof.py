"""The first $0 proof of the separation design (D538): with the two uses of an edge read apart (`separated_edges.py`), the intended
conclusion reaches the real judging path and every statement keeps its home, unrelated filings unchanged, no circle.

A. The unseeded fresh week with the `reads` edge "data-center revenue reads total revenue" (written at the article that opened the
   question): every stored reading of the week is filed again by the production entry point and must equal the stored filing; the
   last day's judging round must show total revenue's conclusion to the data-center judge and change nothing else.
B. A stored seeded draw, whose seventeen edges are `supports`: every stored reading filed again must equal the stored filing (the
   narrowest rule reads them as before); the last day's round, dry with labelled fakes, must judge each supporter before the
   question it supports and show it there, never the other way.
C. Circles across the two kinds, on the seeded state: a `reads` edge that would let two questions read each other is refused; one
   that does not is written and ordered.

  python3 separation_proof.py <scratch folder>        (SEPARATION_MUTANT=unseparated|all-reads: must fail)
"""
import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).parent
sys.path[:0] = [str(ROOT / 'src'), str(HERE), str(HERE.parent / 'dependency-channel')]
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import judging, store  # noqa: E402
import edge_proof  # noqa: E402
import full_day_dry_run  # noqa: E402
import rebuild_seeded_state  # noqa: E402
import separated_edges  # noqa: E402

FRESH = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
SEEDED = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
ITEMS = str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')


def filed_again(folder, run, cfg, uni, days, edge=None):
    """Every stored reading of a run filed again by `extraction.extract` on a scratch copy; returns the statements whose homes differ from the stored filing."""
    folder.mkdir(parents=True)
    for name in ('views.sqlite', 'archive.sqlite'):
        shutil.copy(run / name, folder / name)
    conn, archive = store.open_db(str(folder / 'views.sqlite')), model.Archive(str(folder / 'archive.sqlite'))
    if edge:
        assert separated_edges.add(conn, *edge) if 'dependencies_of' in separated_edges._ORIGINAL else edge_proof.add_edge(conn, edge[0], edge[1])
    stored = {row['input_id']: (row['seq'], json.loads(row['handover_json'])) for row in conn.execute('select input_id, seq, handover_json from handovers')}
    differing, articles = [], 0
    for item in testdb.feed(testdb.open_db(ITEMS), *days):
        if item['input_id'] not in stored:
            continue
        seq, saved = stored[item['input_id']]
        shown = extraction.shown_views(conn, cfg, item, [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])])
        handover = extraction.extract(archive, cfg, item, item['text'], shown, uni, transport=edge_proof.refuse)
        articles += 1
        before = {e['id']: sorted(e['links']) for e in saved['evidence']}
        for e in handover.evidence:
            if sorted(e['links']) != before.get(e['id']):
                differing.append({'article': seq, 'statement': e['id'], 'stored': before.get(e['id']), 'now': sorted(e['links']), 'summary': e['one_line'][:120]})
        if set(before) != {e['id'] for e in handover.evidence} or len(saved['dropped']) != len(handover.dropped):
            differing.append({'article': seq, 'statement': '(the set of statements kept or dropped)'})
    conn.close()
    return articles, differing


def main():
    scratch, mutant = Path(sys.argv[1]), os.environ.get('SEPARATION_MUTANT', '')
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    fresh_cfg, seeded_cfg = config.load(str(ROOT / 'poc/config/poc-v118.json')), config.load(str(ROOT / 'poc/config/poc-v108.json'))
    separated_edges.ALL_READS = mutant == 'all-reads'
    if mutant != 'unseparated':
        separated_edges.install()
    facts = {}
    try:
        # A. the fresh week with the reads edge
        articles, differing = filed_again(scratch / 'a-filing', FRESH, fresh_cfg, uni, ('2026-09-22', '2026-09-28'), edge=('v4', 'v2', 'reads', 13) if mutant != 'unseparated' else ('v4', 'v2'))
        facts[f'A: all {articles} stored filings of the fresh week are unchanged with the reads edge (the company-wide outlook keeps its total-revenue home)'] = articles == 235 and not differing
        print(f'A filing: {articles} articles filed again; statements whose homes differ from the stored filing: {len(differing)}', [(d['article'], d['statement'], d.get('now')) for d in differing][:8])
        same = edge_proof.state_before_the_last_round(scratch / 'a-state', fresh_cfg, uni)
        facts['A: the state before the last round is the stored one'] = all(same.values())
        judging_facts, detail = edge_proof.part_j(scratch / 'a-state', scratch / 'a', fresh_cfg, '')
        narrower = judging_facts.pop('filing reads the new question as the narrower one')          # the unseparated reading of the edge: must no longer hold
        conn = store.open_read_only(str(scratch / 'a' / 'judging' / 'views.sqlite'))
        facts['A: filing reads no narrower home from the reads edge'] = not narrower and store.direct_parents(conn, 'v4') == []
        conn.close()
        facts.update({'A judging: ' + name: held for name, held in judging_facts.items()})
        print('A judging: order', detail['order'], '| line added:', next((line[:150] for line in detail['added_lines'] if line.startswith('- v2 ')), None))

        # B. a seeded draw: its edges are supports
        articles, differing = filed_again(scratch / 'b-filing', SEEDED, seeded_cfg, uni, ('2026-07-01', '2026-07-14'))
        facts[f'B: all {articles} stored filings of the seeded draw are unchanged (the narrowest rule reads the supports edges as before)'] = articles > 200 and not differing
        print(f'B filing: {articles} articles filed again; statements whose homes differ: {len(differing)}', [(d['article'], d['statement'], d.get('now')) for d in differing][:6])
        if mutant != 'unseparated':
            separated_edges.restore()                   # the state before the last round is the stored history: it is rebuilt as stored, outside the seam
        sys.argv = [sys.argv[0], str(scratch / 'b-state')]
        rebuild_seeded_state.main()
        if mutant != 'unseparated':
            separated_edges.install()
        os.environ['D368_MUTANT'] = 'stored-direction'            # the dry run then installs nothing of its own: the round runs under this seam
        for every in (False, True):
            run = full_day_dry_run.one_run(scratch / 'b-state', scratch / ('b-dry-all' if every else 'b-dry-none'), every)
            facts.update({f"B judging ({'every' if every else 'no'} conclusion changes, {run['calls']} calls): {name}": held for name, held in run['expectations'].items()})
        del os.environ['D368_MUTANT']

        # C. circles across the two kinds, on the seeded state
        work = scratch / 'c'
        shutil.copytree(scratch / 'b-state', work)
        conn = store.open_db(str(work / 'views.sqlite'))
        seq = store.next_sequence(conn) - 1
        facts['C: a reads edge that would let data-center revenue and total revenue read each other is refused'] = separated_edges.add(conn, 'v2', 'v1', 'reads', seq) is False
        facts['C: a reads edge that closes no circle is written (the Vera CPU question reads the Rubin shipping question)'] = separated_edges.add(conn, 'v19', 'v7', 'reads', seq) is True
        order = judging.topological(conn, ['v1', 'v2', 'v19', 'v7'])
        facts['C: the order follows both kinds (Rubin shipping, then Vera CPU, then data-center revenue, then total revenue)'] = order == ['v7', 'v19', 'v2', 'v1']
        facts['C: the new reads edge gives filing no narrower home; the supports edges still do'] = store.direct_parents(conn, 'v19') == ['v2'] and store.direct_parents(conn, 'v2') == ['v1']
        facts['C: the opposite reads edge would now be refused'] = store.would_cycle(conn, 'v7', 'v19')
        print('C: order of the four questions:', order, '| what Vera CPU reads:', [d['resolved_to'] for d in store.dependencies_of(conn, 'v19')], '| what data-center revenue reads:', sorted(d['resolved_to'] for d in store.dependencies_of(conn, 'v2')))
        conn.close()
    finally:
        if mutant != 'unseparated':
            separated_edges.restore()
    print()
    for name, held in facts.items():
        print(f"  {'ok  ' if held else 'FAIL'} {name}")
    if not mutant:
        (HERE / 'separation-proof.json').write_text(json.dumps(facts, indent=1) + '\n')
    if not all(facts.values()):
        raise SystemExit(1)
    print(f'\nPASS: all {len(facts)} registered expectations hold (labelled fakes for every judgement not in a stored archive; no package or frozen file changed)')


if __name__ == '__main__':
    main()
