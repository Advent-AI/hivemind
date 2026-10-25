"""06-views.md step 6: write one item's round into the views database. Themes before objects; a repeat adds a source;
a replacement is ordered by the day it was said (a later-arriving older statement is logged, not linked); a
replaced piece still linked elsewhere links the new piece there too; new views come with rungs, dependencies and
successions; a waiting dependency is resolved when the chain's year is created; the set of views whose reading
changed is returned for the re-judging round."""
import dataclasses
import json
import time

from . import store


@dataclasses.dataclass
class Written:
    changed_views: set
    new_views: dict            # candidate id -> view_id
    evidence_ids: dict         # handover evidence id -> evidence_id
    notes: list


def _next_id(conn, table, column, prefix):
    row = conn.execute(f'select {column} from {table} order by rowid desc limit 1').fetchone()
    last = int(row[0][len(prefix):]) if row and row[0].startswith(prefix) and row[0][len(prefix):].isdigit() else 0
    return f'{prefix}{last + 1}'


def _store_piece(conn, e, seq, item):
    evidence_id = _next_id(conn, 'evidence', 'evidence_id', 'e')
    store.add_evidence(conn, evidence_id=evidence_id, quote=e['quote'], one_line=e['one_line'], speaker=e['speaker'],
                       original_who=e['original_who'], original_day=e['original_day'] or item['publication_day'], tier=e['tier'],
                       event_time=e['event_time'], seq=seq, input_id=item['input_id'])
    store.add_source(conn, evidence_id, item['input_id'], item['category'], item['publication_day'], e.get('location', ''), seq)
    return evidence_id


def _create_view(conn, c, object_id, object_kind, seq, item, universe):
    view_id = _next_id(conn, 'views', 'view_id', 'v')
    store.create_view(conn, view_id=view_id, object_id=object_id, object_kind=object_kind, kind=c['kind'], looks_at=c['looks_at'],
                      question=c['question'], due_day=c['due_day'], year=c['year'], rungs=c['rungs'], seq=seq, input_id=item['input_id'],
                      created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    if c.get('measure'):          # keyed candidates (extraction schema v4 and later) carry their key into the ledger
        store.add_key(conn, view_id, c, seq)
    return view_id


def resolve_waiting(conn, new_view_id, seq, changed):
    """A new view on a chain satisfies dependencies waiting for its year on that chain."""
    v = store.view(conn, new_view_id)
    chain = {new_view_id}
    frontier = [new_view_id]
    while frontier:
        current = frontier.pop()
        for row in conn.execute('select succeeds from successions where view_id=?', (current,)):
            if row['succeeds'] not in chain:
                chain.add(row['succeeds'])
                frontier.append(row['succeeds'])
    for dep in conn.execute('select * from dependencies where wait_year=? and wait_chain_view_id is not null', (v['year'],)):
        if dep['wait_chain_view_id'] in chain:
            already = conn.execute('select 1 from dependency_resolutions where dependency_id=?', (dep['dependency_id'],)).fetchone()
            if not already and not store.would_cycle(conn, dep['view_id'], new_view_id):
                store.insert(conn, 'dependency_resolutions', dependency_id=dep['dependency_id'], resolved_to=new_view_id, reason='created', seq=seq)
                changed.add(dep['view_id'])


def write(conn, universe, seq, item, handover, checked, second_pass):
    """second_pass: {(handover evidence id, view_id): (outcome, target_evidence_id, said_day)} for candidate-linked
    evidence compared after the candidates' destinations were known (new views' evidence is simply new)."""
    changed, notes, new_views, evidence_ids = set(), [], {}, {}
    candidate_ids = {c['id'] for c in handover.candidates}
    # 1. new views, themes first
    order = sorted(handover.candidates, key=lambda c: 0 if c['kind'] == '主题观点' else 1)
    for c in order:
        outcome, target, deps = checked.outcomes.get(c['id'], ('不开', None, []))
        if outcome not in ('新观点', '接续'):
            continue
        object_id = universe.resolve(c['object'])
        view_id = _create_view(conn, c, object_id, universe.kind(object_id), seq, item, universe)
        new_views[c['id']] = view_id
        if outcome == '接续' and target:
            store.insert(conn, 'successions', view_id=view_id, succeeds=target, seq=seq)
        changed.add(view_id)
    # 2. dependencies of the new views (candidate ids resolve to the views just created)
    for c in order:
        outcome, target, deps = checked.outcomes.get(c['id'], ('不开', None, []))
        if c['id'] not in new_views:
            continue
        view_id = new_views[c['id']]
        for dep in deps:
            depends_on = dep['view_id']
            if depends_on in new_views:
                depends_on = new_views[depends_on]
            elif depends_on in candidate_ids:
                notes.append(f'dependency {view_id} -> candidate {depends_on} dropped: that candidate was not opened')
                continue
            if depends_on and store.would_cycle(conn, view_id, depends_on):
                notes.append(f'dependency {view_id} -> {depends_on} dropped: cycle')
                continue
            chain = dep['wait_chain_view_id']
            if chain in new_views:
                chain = new_views[chain]
            store.insert(conn, 'dependencies', view_id=view_id, depends_on=depends_on, wait_chain_view_id=chain, wait_year=dep['wait_year'],
                         direction=dep['direction'], seq=seq)
        resolve_waiting(conn, view_id, seq, changed)
    # 3. where each piece of evidence goes
    def destinations(e):
        targets = []
        for link in e['links']:
            if link in new_views:
                targets.append((new_views[link], ('新证据', None, '')))
            elif link in checked.outcomes and checked.outcomes[link][0] == '归入已有的':
                targets.append((checked.outcomes[link][1], second_pass.get((e['id'], checked.outcomes[link][1]), ('新证据', None, ''))))
            elif link in checked.outcomes:
                continue   # a candidate that was not opened: evidence only on it is not stored
            elif (e['id'], link) in checked.evidence:
                targets.append((link, checked.evidence[(e['id'], link)]))
            elif (e['id'], link) in second_pass:
                targets.append((link, second_pass[(e['id'], link)]))
        return targets

    for e in handover.evidence:
        targets = destinations(e)
        if not targets:
            notes.append(f'evidence {e["id"]} linked to nothing kept; not stored')
            continue
        # one piece is stored once however many views it goes to (06-views: 一条证据连几条观点，也只存一条); a repeat
        # under any destination means the piece already exists and is linked on, a replacement under any
        # destination replaces there and links everywhere, a late older statement is logged and linked nowhere
        repeat_of = next((target for _, (outcome, target, _) in targets if outcome == '重复' and target), None)
        replacing = [(target, said_day) for _, (outcome, target, said_day) in targets if outcome == '替代' and target]
        if repeat_of:
            store.add_source(conn, repeat_of, item['input_id'], item['category'], item['publication_day'], e.get('location', ''), seq)
            for view_id, _ in targets:
                if store.link(conn, repeat_of, view_id, seq):
                    changed.add(view_id)       # newly linked existing evidence counts as a change for that view
            evidence_ids[e['id']] = repeat_of
            continue
        if replacing:
            target_id, said_day = replacing[0]
            old = store.evidence(conn, target_id)
            new_day = said_day or e['original_day'] or item['publication_day']
            if old and old['original_day'] and new_day < old['original_day']:
                store.insert(conn, 'late_statements', input_id=item['input_id'], evidence_quote=e['quote'][:500], reason=f'older than {target_id} ({old["original_day"]})', seq=seq)
                notes.append(f'evidence {e["id"]}: late older statement, not linked')
                continue
            stored_id = _store_piece(conn, dict(e, original_day=new_day), seq, item)
            for target_id, _ in replacing:
                if not store.is_replaced(conn, target_id):
                    store.replace(conn, target_id, stored_id, new_day, seq)
                for linked in store.views_linked_to(conn, target_id):
                    if store.link(conn, stored_id, linked, seq) and store.is_open(conn, linked):
                        changed.add(linked)
            for view_id, _ in targets:
                store.link(conn, stored_id, view_id, seq)
                changed.add(view_id)
            evidence_ids[e['id']] = stored_id
            continue
        stored_id = _store_piece(conn, e, seq, item)
        for view_id, _ in targets:
            store.link(conn, stored_id, view_id, seq)
            changed.add(view_id)
        evidence_ids[e['id']] = stored_id
    return Written(changed, new_views, evidence_ids, notes)
