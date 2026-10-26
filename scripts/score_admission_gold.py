#!/usr/bin/env python3
"""Score a ledger against the extraction gold (D188).

  python3 scripts/score_admission_gold.py --gold poc/eval/gold/extraction-admission-2026-10-26.json \
      --views poc/data/<run>/views.sqlite [--universe poc/universe.json] [--out report.md]

A gold case names the items it covers, the theses that must open (typed keys with acceptable alternatives), the theses
that must not open, the evidence links that must exist and the links that must not. A thesis matches a key when its
object and measure agree, its year agrees for a quantity (an event's check day is the model's own, D185, so its year is
not compared), its event type agrees for events, and the key's scope pattern (when given) matches the thesis's scope,
focus or question. Score per case: fail when a must-open thesis or an evidence target is missing;
partial when all are present but a must-not-open thesis was created by the case's items or a forbidden link exists; full otherwise; "not processed"
when none of the case's items reached a handover. The census counts the ledger's theses by object, measure and
admission reason (read from the handovers' candidates), and how often a kept candidate named a thesis in folds_into."""
import argparse
import collections
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

from hivemind import universe as universe_module  # noqa: E402

EVENT_MEASURES = ('event', 'policy_event')


def _object(uni, text):
    return uni.resolve(text) or text


def view_matches(view, key_row, key, uni):
    """True when the ledger thesis (its views row and view_keys row) is the thesis the gold key describes."""
    if _object(uni, view['object_id']) != _object(uni, key['object']):
        return False
    if (key_row['measure'] if key_row else None) != key['measure']:
        return False
    if key['measure'] in EVENT_MEASURES:
        if (key_row['event_type'] or 'n/a') != (key.get('event_type') or 'n/a'):     # an event is named by its type and scope; its check day is the model's own (D185), so the year is not compared
            return False
    elif str(view['year']) != str(key['year']):
        return False
    pattern = key.get('scope_regex') or ''
    if pattern:
        haystack = ' '.join([key_row['scope'] or '', view['looks_at'] or '', view['question'] or ''])
        if not re.search(pattern, haystack, re.I):
            return False
    return True


def _views(conn):
    rows = conn.execute('select v.*, k.measure, k.scope, k.event_type from views v left join view_keys k on k.view_id = v.view_id').fetchall()
    return [dict(r) for r in rows]


def views_with_key(conn, key, uni):
    """Every thesis in the ledger matching the key or one of its alternatives."""
    keys = [key] + list(key.get('alternatives') or [])
    out = []
    for row in _views(conn):
        key_row = {'measure': row['measure'], 'scope': row['scope'], 'event_type': row['event_type']}
        if any(view_matches(row, key_row, k, uni) for k in keys):
            out.append(row['view_id'])
    return out


def linked_from(conn, view_id, items):
    marks = ','.join('?' * len(items))
    return conn.execute(f'select 1 from evidence_links l join evidence_sources s on s.evidence_id = l.evidence_id where l.view_id=? and s.input_id in ({marks})',
                        [view_id, *items]).fetchone() is not None


def created_by(conn, view_id, items):
    marks = ','.join('?' * len(items))
    return conn.execute(f'select 1 from views where view_id=? and created_from_input in ({marks})', [view_id, *items]).fetchone() is not None


def _evidence_from(conn, items):
    marks = ','.join('?' * len(items))
    return [dict(r) for r in conn.execute(f'select distinct e.evidence_id, e.quote from evidence e join evidence_sources s on s.evidence_id = e.evidence_id where s.input_id in ({marks})', items)]


def _resolve_target(case, target):
    if isinstance(target, str) and target.startswith('self:'):
        gist = target[len('self:'):]
        for key in case['must_open']:
            if key['gist'] == gist:
                return key
        raise ValueError(f'case {case["id"]}: evidence target names no must_open gist: {gist!r}')
    return target


def link_present(conn, case, link, items, uni):
    target = _resolve_target(case, link['target'])
    target_views = set(views_with_key(conn, target, uni))
    if not target_views:
        return False
    for e in _evidence_from(conn, items):
        if re.search(link['quote_regex'], e['quote'] or '', re.I):
            linked = {r[0] for r in conn.execute('select view_id from evidence_links where evidence_id=?', (e['evidence_id'],))}
            if linked & target_views:
                return True
    return False


def processed(conn, items):
    marks = ','.join('?' * len(items))
    return conn.execute(f'select 1 from handovers where input_id in ({marks})', items).fetchone() is not None


def score_case(conn, case, uni):
    conn.row_factory = sqlite3.Row
    items = list(case['items'])
    result = {'id': case['id'], 'title': case.get('title', ''), 'score': '', 'missing_must_open': [], 'extra_opened': [], 'missing_links': [], 'forbidden_links': [], 'opened_by_items': []}
    if not processed(conn, items):
        result['score'] = 'not processed'
        return result
    for key in case.get('must_open', []):
        if not any(linked_from(conn, v, items) for v in views_with_key(conn, key, uni)):      # a thesis counts only through this item's evidence
            result['missing_must_open'].append(key['gist'])
    for key in case.get('must_not_open', []):
        if any(created_by(conn, v, items) for v in views_with_key(conn, key, uni)):
            result['extra_opened'].append(key['gist'])
    for link in case.get('evidence_targets', []):
        if not link_present(conn, case, link, items, uni):
            result['missing_links'].append(link['quote_regex'])
    for link in case.get('must_not_link', []):
        if link_present(conn, case, link, items, uni):
            result['forbidden_links'].append(link['quote_regex'])
    marks = ','.join('?' * len(items))
    result['opened_by_items'] = [r[0] for r in conn.execute(f'select view_id from views where created_from_input in ({marks}) order by created_seq', items)]
    if result['missing_must_open'] or result['missing_links']:
        result['score'] = 'fail'
    elif result['extra_opened'] or result['forbidden_links']:          # a wrong attachment costs the full score, not the case
        result['score'] = 'partial'
    else:
        result['score'] = 'full'
    return result


def census(conn):
    conn.row_factory = sqlite3.Row
    rows = _views(conn)
    by_object = collections.Counter(r['object_id'] for r in rows)
    by_measure = collections.Counter(r['measure'] or '(no key)' for r in rows)
    by_opens_as = collections.Counter()
    folds_named = 0
    for (handover_json,) in conn.execute('select handover_json from handovers'):
        for c in json.loads(handover_json).get('candidates', []):
            if 'opens_as' in c:
                by_opens_as[c['opens_as']] += 1
                folds_named += 1 if c.get('folds_into') else 0
    same_key = collections.Counter(f"{r['object_id']} {r['measure']} {r['year']}" for r in rows if r['measure'] not in (None, 'event', 'policy_event'))
    duplicate_keys = {k: n for k, n in sorted(same_key.items()) if n > 1}          # one object, quantity and year held by several theses (scope is wording, log row 43)
    return {'theses': len(rows), 'by_object': dict(sorted(by_object.items())), 'by_measure': dict(sorted(by_measure.items())),
            'by_opens_as': dict(sorted(by_opens_as.items())), 'folds_into_named': folds_named, 'duplicate_keys': duplicate_keys}


def render(gold, results, counts, views_path):
    judged = [r for r in results if r['score'] != 'not processed']
    lines = [f'# Extraction gold `{gold["version"]}` against `{views_path}`', '',
             f'Cases judged: {len(judged)}; ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(r["score"] for r in judged).items()))
             + f'; not processed {len(results) - len(judged)}', '',
             '| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |', '|---|---|---|---|---|---|---|---|---|']
    baseline = {c['id']: c.get('system_v23', {}).get('score', '') for c in gold['cases']}
    for r in results:
        lines.append(f'| {r["id"]} | {r["title"]} | **{r["score"]}** | {baseline.get(r["id"], "")} | {"; ".join(r["missing_must_open"])} | {"; ".join(r["extra_opened"])} | '
                     f'{"; ".join(r["missing_links"])} | {"; ".join(r["forbidden_links"])} | {", ".join(r["opened_by_items"])} |')
    lines += ['', '## Census', '', f'- theses: {counts["theses"]}', f'- by object: {counts["by_object"]}', f'- by measure: {counts["by_measure"]}',
              f'- by admission reason (handover candidates carrying opens_as): {counts["by_opens_as"]}', f'- candidates that named a thesis in folds_into and still opened: {counts["folds_into_named"]}',
              f'- one object, quantity and year held by several theses: {counts["duplicate_keys"]}', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gold', required=True)
    parser.add_argument('--views', required=True)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--out', default=None)
    args = parser.parse_args()
    with open(args.gold, encoding='utf-8') as handle:
        gold = json.load(handle)
    uni = universe_module.load(args.universe)
    conn = sqlite3.connect(f'file:{args.views}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    results = [score_case(conn, case, uni) for case in gold['cases']]
    if not results:
        raise SystemExit('the gold holds no cases: nothing judged')
    text = render(gold, results, census(conn), args.views)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as handle:
            handle.write(text)
    print(text)


if __name__ == '__main__':
    main()
