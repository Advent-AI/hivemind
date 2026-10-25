"""06-views.md step 6: write one item's round into the views database. Themes before objects; a repeat adds a source;
a replacement is ordered by the day it was said (a later-arriving older statement is logged, not linked); a
replaced piece still linked elsewhere links the new piece there too; new views come with rungs, dependencies and
successions; a waiting dependency is resolved when the chain's year is created; the set of views whose reading
changed is returned for the re-judging round."""
import dataclasses
import json
import re
import time

from . import identity, store


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
    # the year is stored in its one canonical spelling so that a waiting dependency's year joins it (D163 plan, period text)
    year = universe.canonical_year(object_id, c['year']) if hasattr(universe, 'canonical_year') else c['year']
    store.create_view(conn, view_id=view_id, object_id=object_id, object_kind=object_kind, kind=c['kind'], looks_at=c['looks_at'],
                      question=c['question'], due_day=c['due_day'], year=year, rungs=c['rungs'], seq=seq, input_id=item['input_id'],
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


def object_id_of(universe, candidate):
    return universe.resolve(candidate['object']) or candidate['object']


def oriented_like(c, previous, notes):
    """06-views: a successor's ladder keeps the predecessor's direction. A numeric ladder written the other way round (rung 1 the
    lowest band where the predecessor's rung 1 is the highest) is the same ladder; it is stored reversed, rungs with their
    labels and bounds, so positions mean the same along the chain. Undecidable pairs are stored as written."""
    from .matching import ladder_direction
    before, after = (ladder_direction(previous) if previous else None), ladder_direction(c['rungs'])
    if before is not None and after is not None and before != after:
        notes.append(f'candidate {c["id"]}: successor ladder reversed to the predecessor\'s direction')
        return dict(c, rungs=list(reversed(c['rungs'])))
    return c


TIER_RANK = {'fact': 3, 'party_statement': 3, 'third_party_view': 2, 'rumour': 1}
ISO_DAY = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def replacement_refused(incoming, old, new_day):
    """06-views, the Replace row: a later account of the same matter by a party entitled to give one (a speaker revises its own
    guidance or forecast, an official confirms or denies a report, the original source revises). Returns the reason a replacement is
    refused, or '' when it may stand: the incoming piece needs a stated day, a tier at least the stored piece's (a view never
    retires a fact or a party's statement), and, when it is a third-party view or a rumour, the same party as the stored piece."""
    from .. import vocabulary
    if not old:
        return ''
    if not ISO_DAY.match(new_day or ''):
        return 'no stated day'
    new_tier, old_tier = vocabulary.canonical('tier', incoming.get('tier')), vocabulary.canonical('tier', old.get('tier'))
    if TIER_RANK.get(new_tier, 0) < TIER_RANK.get(old_tier, 0):
        return f'{new_tier} cannot replace {old_tier}'
    if new_tier in ('third_party_view', 'rumour') \
            and (incoming.get('original_who') or '').strip().casefold() != (old.get('original_who') or '').strip().casefold():
        return f'another party\'s {old_tier.replace("_", " ")}'       # an official confirms or denies; the original source revises
    return ''


class WriteConflict(ValueError):
    """The checked plan no longer fits the writable ledger; no partial write is retained."""


def write(conn, universe, seq, item, handover, checked, second_pass):
    """Write atomically within the caller's transaction; the caller commits the completion marker with it."""
    if not conn.in_transaction:
        conn.execute('begin immediate')
    conn.execute('savepoint view_write')
    try:
        store.ensure_writable_columns(conn)
        result = _write(conn, universe, seq, item, handover, checked, second_pass)
    except Exception:
        conn.execute('rollback to view_write')
        conn.execute('release view_write')
        raise
    conn.execute('release view_write')
    return result


def _write(conn, universe, seq, item, handover, checked, second_pass):
    """second_pass: {(handover evidence id, view_id): (outcome, target_evidence_id, said_day)} for candidate-linked
    evidence compared after the candidates' destinations were known (new views' evidence is simply new)."""
    changed, notes, new_views, evidence_ids = set(), [], {}, {}
    candidate_ids = {c['id'] for c in handover.candidates}
    aliases, problems = identity.batch_plan(handover.candidates, checked.outcomes)
    if problems:
        raise WriteConflict('; '.join(problems))
    created = {}
    # 1. new views, themes first
    order = sorted(handover.candidates, key=lambda c: 0 if c['kind'] == 'theme' else 1)
    for c in order:
        outcome, target, deps = checked.outcomes.get(c['id'], ('skip', None, []))
        if outcome not in ('new', 'succession'):
            continue
        canonical = aliases[c['id']]
        if canonical in created:
            new_views[c['id']] = created[canonical]
            continue
        if store.exact_key_views(conn, c):
            raise WriteConflict(f'candidate {c["id"]}: existing exact identity requires matching')
        object_id = universe.resolve(c['object'])
        if outcome == 'succession' and target:
            c = oriented_like(c, store.rungs_of(conn, target), notes)
        view_id = _create_view(conn, c, object_id, universe.kind(object_id), seq, item, universe)
        new_views[c['id']] = view_id
        created[canonical] = view_id
        if outcome == 'succession' and target:
            store.insert(conn, 'successions', view_id=view_id, succeeds=target, seq=seq)
        changed.add(view_id)
    # 1b. research groups (D149, D165, D166): the groups module plans creations and memberships from the handover's
    #     declarations, the stored groups' names and each new thesis's own text; a merged candidate adds nothing
    from .. import extraction as _extraction
    from . import groups as _groups
    creations, memberships, group_notes = _groups.plan(getattr(handover, 'new_groups', None) or [], _groups.stored_groups(conn), order, new_views,
                                                        _extraction.tracks_a_matter, universe)
    notes.extend(group_notes)
    group_ids = {}
    for creation in creations:
        group_ids[creation['local_id']] = _next_id(conn, 'thesis_groups', 'group_id', 'g')
        objects = sorted({store.view(conn, view_id)['object_id'] for view_id, key, _ in memberships if key == creation['local_id']})
        store.add_group(conn, group_id=group_ids[creation['local_id']], name=creation['name'], scope=creation['scope'], seq=seq, input_id=item['input_id'],
                        object_ids=objects, aliases=creation['aliases'])
    for view_id, key, basis in memberships:
        store.add_member(conn, group_ids.get(key, key), view_id, seq, item['input_id'], basis)
    # 2. dependencies of the new views (candidate ids resolve to the views just created)
    dependencies_written = set()
    for c in order:
        outcome, target, deps = checked.outcomes.get(c['id'], ('skip', None, []))
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
            wait_year = dep['wait_year']
            if wait_year and chain and hasattr(universe, 'canonical_year'):          # the chain's object decides the spelling (FY2027 or 2026)
                chain_view = store.view(conn, chain)
                wait_year = universe.canonical_year(chain_view['object_id'] if chain_view else object_id_of(universe, c), wait_year)
            edge = (view_id, depends_on, chain, wait_year, dep['direction'])
            if edge in dependencies_written:
                continue
            dependencies_written.add(edge)
            store.insert(conn, 'dependencies', view_id=view_id, depends_on=depends_on, wait_chain_view_id=chain, wait_year=wait_year,
                         direction=dep['direction'], seq=seq)
        resolve_waiting(conn, view_id, seq, changed)
    # 3. where each piece of evidence goes
    def destinations(e):
        targets = []
        for link in e['links']:
            if link in new_views:
                targets.append((new_views[link], ('new', None, '')))
            elif link in checked.outcomes and checked.outcomes[link][0] == 'merge':
                targets.append((checked.outcomes[link][1], second_pass.get((e['id'], checked.outcomes[link][1]), ('new', None, ''))))
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
        repeat_of = next((target for _, (outcome, target, _) in targets if outcome == 'repeat' and target), None)
        replacing = [(target, said_day) for _, (outcome, target, said_day) in targets if outcome == 'replace' and target]
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
            refusal = replacement_refused(e, old, new_day)
            if refusal:
                # 06-views: a replacement is a later account of the same matter by a party entitled to give one; anything else is one more piece
                notes.append(f'evidence {e["id"]}: replacement of {target_id} refused ({refusal}); stored as new')
                replacing = []
        if replacing:
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
