"""One view in the shape the front end reads: the ladder, every judgement round with the model's reason and the
evidence it cited, the evidence in force with tiers, speakers and sources, dependencies, replacements and the freeze
switches. The same shaping writes the mock's data file (scripts/mock_data.py) and answers POST /ideas, so the front
end's adapter reads both. Read-only on every database. With `as_of`, rows written after that day are left out."""
import json
from datetime import date

from . import service


def item_lookup(items_db):
    """input id → title, publisher and category of a stored item, from the items database (or the id alone when the
    database is not given or does not hold it)."""
    cache = {}

    def item_of(input_id):
        if input_id not in cache:
            row = items_db.execute('select title, publisher, publisher_type, category, publication_day, source_uri from items where input_id=?', (input_id,)).fetchone() if items_db is not None else None
            cache[input_id] = dict(row) if row else {'title': input_id, 'publisher': '', 'publisher_type': '', 'category': '', 'publication_day': '', 'source_uri': ''}
        return cache[input_id]
    return item_of


def _visible(views_db, seq, as_of):
    return as_of is None or service.visible(views_db, seq, as_of)


def view_bundle(views_db, item_of, view_id, as_of=None):
    v = views_db.execute('select * from views where view_id=?', (view_id,)).fetchone()
    if v is None:
        raise KeyError(view_id)
    columns = {r[1] for r in views_db.execute('pragma table_info(rungs)')}
    bounds = ', lo, hi' if {'lo', 'hi'} <= columns else ''          # a ledger written before keys has no bounds; the adapter then reads the prose
    rungs = [dict(r) for r in views_db.execute(f'select position, label, condition{bounds} from rungs where view_id=? order by position', (view_id,))]
    switches = [dict(r) for r in views_db.execute('select open, reason, after_seq from view_switches where view_id=? order by id', (view_id,))
                if _visible(views_db, r['after_seq'], as_of)]
    for switch in switches:
        switch['day'] = service.day_of_seq(views_db, switch['after_seq'])
    judgements = []
    for j in views_db.execute('select * from judgements where view_id=? order by judgement_id', (view_id,)):
        if as_of is not None and j['publication_day'] > as_of:
            continue
        judgements.append({'id': str(j['judgement_id']), 'day': j['publication_day'], 'seq': j['seq'], 'rung': j['rung'], 'changed': bool(j['changed']),
                           'why_changed': j['why_changed'], 'reasons': j['reasons'], 'cited': json.loads(j['cited_evidence_json'] or '[]'),
                           'cited_views': json.loads(j['cited_views_json'] or '[]'), 'pushes': json.loads(j['pushes_json'] or '[]'),
                           'from_item': j['input_id']})
    evidence = []
    for e in views_db.execute('select e.*, l.seq as linked_seq from evidence_links l join evidence e on e.evidence_id=l.evidence_id where l.view_id=? order by l.id', (view_id,)):
        if not _visible(views_db, e['linked_seq'], as_of):
            continue
        sources = [dict(s) for s in views_db.execute('select input_id, publication_day, seq from evidence_sources where evidence_id=? order by id', (e['evidence_id'],))
                   if _visible(views_db, s['seq'], as_of)]
        replaced_by = views_db.execute('select new_evidence_id, said_day, seq from replacements where old_evidence_id=?', (e['evidence_id'],)).fetchone()
        if replaced_by is not None and not _visible(views_db, replaced_by['seq'], as_of):
            replaced_by = None
        replaces = views_db.execute('select old_evidence_id from replacements where new_evidence_id=?', (e['evidence_id'],)).fetchone()
        first = sources[0] if sources else {'input_id': e['created_from_input'], 'publication_day': '', 'seq': e['created_seq']}
        item = item_of(first['input_id'])
        evidence.append({'id': e['evidence_id'], 'one_line': e['one_line'], 'quote': e['quote'], 'tier': e['tier'], 'speaker': e['speaker'],
                         'original_who': e['original_who'], 'original_day': e['original_day'], 'event_time': e['event_time'],
                         'day': first['publication_day'] or item['publication_day'], 'seq': first['seq'], 'linked_seq': e['linked_seq'],
                         'arrival_day': service.day_of_seq(views_db, e['linked_seq']),
                         'source': {'title': item['title'], 'publisher': item['publisher'], 'publisher_type': item['publisher_type'],
                                    'category': item['category'], 'uri': item['source_uri']},
                         'outlets': len(sources), 'replaced_by': {'new_evidence_id': replaced_by['new_evidence_id'], 'said_day': replaced_by['said_day']} if replaced_by else None,
                         'replaces': replaces['old_evidence_id'] if replaces else None})
    dependencies = [dict(r) for r in views_db.execute('select depends_on, direction, wait_year, seq from dependencies where view_id=? order by dependency_id', (view_id,))
                    if _visible(views_db, r['seq'], as_of)]
    for dependency in dependencies:
        dependency['day'] = service.day_of_seq(views_db, dependency['seq'])
    dependants = sorted({r['view_id'] for r in views_db.execute('select view_id, seq from dependencies where depends_on=?', (view_id,)) if _visible(views_db, r['seq'], as_of)},
                        key=lambda s: (len(s), s))
    created = item_of(v['created_from_input'])
    return {'view_id': view_id, 'object': v['object_id'], 'kind': v['kind'], 'looks_at': v['looks_at'], 'question': v['question'],
            'due_day': v['due_day'], 'year': v['year'], 'created_seq': v['created_seq'], 'created_day': created['publication_day'] or service.day_of_seq(views_db, v['created_seq']),
            'created_from': {'title': created['title'], 'publisher': created['publisher'], 'category': created['category']},
            'rungs': rungs, 'open': not any(not s['open'] for s in switches), 'switches': switches,
            'judgements': judgements, 'evidence': evidence, 'dependencies': dependencies, 'dependants': dependants}


def days(views_db, as_of=None):
    """The completed days the front end's time axis runs over, up to as_of."""
    return [r[0] for r in views_db.execute('select day from days_completed order by day') if as_of is None or r[0] <= as_of]


def thesis_bundles(views_db, items_db, view_ids, as_of=None):
    """Complete, dated UI inputs for caller-selected theses; no search, model call or ledger write."""
    as_of = as_of or service.default_as_of(views_db)
    date.fromisoformat(as_of)
    if not isinstance(view_ids, list) or not view_ids or any(not isinstance(id, str) or not id for id in view_ids):
        raise ValueError('thesis_bundles needs a non-empty list of view ids')
    lookup = item_lookup(items_db)
    records = []
    for view_id in dict.fromkeys(view_ids):
        row = views_db.execute('select * from views where view_id=?', (view_id,)).fetchone()
        if row is None or not service.view_exists(views_db, row, as_of):
            raise KeyError(f'{view_id} is not available as of {as_of}')
        records.append(view_bundle(views_db, lookup, view_id, as_of))
    return {'as_of': as_of, 'days': days(views_db, as_of), 'views': records}
