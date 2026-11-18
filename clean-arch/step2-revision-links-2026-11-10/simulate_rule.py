#!/usr/bin/env python3
"""What each candidate rule writes, exactly, on the three saved D392 clean draws. No model call: the adapter's own writing code runs over
each saved draw with judging switched off, once per rule, and the ledgers are compared row by row.

Rules for a record that Step 2 judged a later version of an older one:
- carry:     the record takes every question link of the older record (the adapter as it is; D202's rule)
- never:     the relation is written, no link is written on it
- unfiled:   the record takes the older record's links only when Step 1 filed it under no thesis at all

The adapter is not edited. Its one call that reads the older record's links (`store.views_linked_to`, called only in the carrying
loop, right after `store.revise` names the pair) is answered by the rule here. Checks, each failing the run:
1. under `carry`, the evidence, sources, links, relations and repeat relations equal the saved run's, row for row;
2. under the other rules, every table but the links equals `carry`'s, and the links missing are exactly the ones census.py found
   (all of them for `never`; those of records Step 1 filed under some thesis for `unfiled`), with no link added.

Usage: simulate_rule.py <census json> <new scratch folder> <output json>"""
import collections, contextlib, glob, json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import adapter as e2e_adapter  # noqa: E402
from hivemind import model  # noqa: E402
from hivemind.views import store  # noqa: E402

DRAWS = ROOT / 'poc/data/clean-e2e-2026-11-09'
WRITTEN_TABLES = ('views', 'rungs', 'evidence', 'evidence_sources', 'evidence_links', 'revisions', 'same_claims')
RULES = ('carry', 'never', 'unfiled')


def refuse(*arguments, **keywords):
    raise SystemExit('a simulation reached a model call or a credential')


def clean_thesis_judged(saved):
    """The clean-opened thesis the saved run judged as the ruler's Ohio question (adapter `--q23`), or None: the one view that is not a seed."""
    with contextlib.closing(sqlite3.connect(f'file:{saved}?mode=ro', uri=True)) as conn:
        extra = [view_id for (view_id,) in conn.execute('select view_id from views') if view_id not in e2e_adapter.SEED_IDS]
    if len(extra) > 1:
        raise SystemExit(f'{saved} holds more than one view that is not a seed: {extra}')
    return extra[0] if extra else None


def write_draw(draw, rule, output, q23):
    """The adapter's writes for one draw under one rule, no judging. Returns the ledger path."""
    trace = f"{DRAWS}/stage2-clean-d{draw}/trace.sqlite+{DRAWS}/stage2-clean-d{draw}-segment-2/trace.sqlite"
    pair, current = {}, {}
    production_revise, production_linked = store.revise, store.views_linked_to
    production_judge, production_article = e2e_adapter.Adapter.judge, e2e_adapter.Adapter.article

    def article(self, k, records, library, revisions_by_record, later_entries, changed):
        current['adapter'], current['records'] = self, records          # the records of the article being written, as Step 1 gave them
        return production_article(self, k, records, library, revisions_by_record, later_entries, changed)

    def revise(conn, old_id, new_id, said_day, seq):
        pair['new'] = new_id
        return production_revise(conn, old_id, new_id, said_day, seq)

    def views_linked_to(conn, evidence_id):
        if rule == 'never':
            return []
        if rule == 'unfiled':
            record = next(r for r in current['records'] if current['adapter'].evidence_of.get(r['id']) == pair['new'])
            if record['thesis_ids']:
                return []
        return production_linked(conn, evidence_id)

    store.revise, store.views_linked_to = revise, views_linked_to
    e2e_adapter.Adapter.judge = lambda self, day, seq, changed: []
    e2e_adapter.Adapter.article = article
    model.openai_transport, model._key = refuse, refuse
    try:
        adapter = e2e_adapter.replay(trace, DRAWS / f'stage2-clean-d{draw}-segment-2/step2', output, transport=refuse, cap_usd=0.0, q23=q23)
        adapter.conn.close()
    finally:
        store.revise, store.views_linked_to = production_revise, production_linked
        e2e_adapter.Adapter.judge, e2e_adapter.Adapter.article = production_judge, production_article
    return Path(output) / 'views.sqlite'


def rows_of(path, table):
    with contextlib.closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as conn:
        columns = [row[1] for row in conn.execute(f'pragma table_info({table})') if row[1] != 'id']   # a row number shifts when a link is not written
        return conn.execute(f"select {', '.join(columns)} from {table} order by rowid").fetchall()


def main(census_path, scratch, output_path):
    census = json.loads(Path(census_path).read_text())
    scratch = Path(scratch).resolve()
    report, failures = [], []
    for draw in (1, 2, 3):
        saved = Path(sorted(glob.glob(str(DRAWS / f'stage2-clean-d{draw}/judged*')))[-1]) / 'views.sqlite'
        q23 = clean_thesis_judged(saved)
        ledgers = {rule: write_draw(draw, rule, scratch / f'd{draw}-{rule}', q23) for rule in RULES}
        for table in WRITTEN_TABLES:
            if rows_of(saved, table) != rows_of(ledgers['carry'], table):
                failures.append(f'draw {draw}: under carry, table {table} differs from the saved run')
        carried = [(c['new']['evidence'], c['question'], bool(c['new']['step1_theses'])) for c in census['carried'] if c['draw'] == draw]
        expected_missing = {'never': {(e, v) for e, v, _ in carried}, 'unfiled': {(e, v) for e, v, own in carried if own}}
        baseline_links = collections.Counter((e, v) for e, v, _ in rows_of(ledgers['carry'], 'evidence_links'))
        row = {'draw': draw, 'clean thesis judged as the Ohio question': q23, 'links under carry': sum(baseline_links.values())}
        for rule in ('never', 'unfiled'):
            for table in WRITTEN_TABLES:
                if table != 'evidence_links' and rows_of(ledgers['carry'], table) != rows_of(ledgers[rule], table):
                    failures.append(f'draw {draw}: under {rule}, table {table} differs from carry')
            links = collections.Counter((e, v) for e, v, _ in rows_of(ledgers[rule], 'evidence_links'))
            missing, added = set(baseline_links - links), set(links - baseline_links)
            if missing != expected_missing[rule] or added:
                failures.append(f'draw {draw}: under {rule}, missing {sorted(missing ^ expected_missing[rule])} differ from the census, added {sorted(added)}')
            kept_order = [pair for pair in rows_of(ledgers['carry'], 'evidence_links') if (pair[0], pair[1]) not in missing]
            if kept_order != rows_of(ledgers[rule], 'evidence_links'):
                failures.append(f'draw {draw}: under {rule}, the links that remain are not in the order carry wrote them')
            row[f'links under {rule}'] = sum(links.values())
            row[f'links not written under {rule}'] = sorted(f'{e}->{v}' for e, v in missing)
        report.append(row)
        print(json.dumps(row))
    result = {'passed': not failures, 'failures': failures, 'tables compared': list(WRITTEN_TABLES), 'draws': report}
    Path(output_path).write_text(json.dumps(result, indent=1))
    print('PASSED' if not failures else 'FAILED:\n' + '\n'.join(failures))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main(*sys.argv[1:4])
