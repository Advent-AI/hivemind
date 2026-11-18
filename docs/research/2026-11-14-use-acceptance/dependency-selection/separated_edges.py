"""A harness seam for the separation design (D538): the two uses of a dependency edge read two derived relations. No package file
changes; `install()` replaces three functions of `hivemind.views.store` for the life of a proof and `restore()` puts them back.

An edge has a kind. `supports` (D208, D368 item 4): the edge's question is a driver of the question it names. `reads` (D51, PRD 06):
the edge's question reads the conclusion of the question it names.

Where the kind comes from. A writer stores it when it writes the edge: on scratch stores the two production writers are wrapped
(`install_writers`) and the kind goes into a side table beside the row. A row written before any kind was stored is read by one
versioned interpretation of the two writers' own marks (`edge_inventory.py`: every row of the stored ledgers is one or the other):
the seeding module's row (sequence 0, direction 'last_end', on a question created from a seed file) is `supports`; a row written
at an article on a question opened from an article, with a direction label of the matching vocabulary, is `reads`. A row of
neither family without a stored kind is refused (`AmbiguousEdge`): its meaning is not guessed.

  reading relation (judging: the request's block, the order, citations, the queue, the cycle check):
      reads edge (B, A): B reads A.        supports edge (D, R): R reads D.
  narrower relation (filing: the narrowest rule):
      supports edge (D, R): D is the narrower home than R.        a reads edge states none.
"""
import sqlite3

from hivemind import seeding, vocabulary
from hivemind.views import store, writing

_ORIGINAL = {}
ALL_READS = False            # a mutant: every edge taken as `reads` (the kind ignored)
KIND_NOT_STORED = False      # a mutant: the wrapped writers store no kind
DUPLICATES_WRITTEN = False   # a mutant: an edge whose reading pair already exists is written again
MATCHING_LABELS = set(vocabulary.DIRECTIONS) | {'对方第一格是看多', '对方最后一格是看多', '同向', '反向'}


class AmbiguousEdge(RuntimeError):
    pass


def stored_kind(conn, dependency_id):
    try:
        row = conn.execute('select kind from dependency_kinds where dependency_id = ?', (dependency_id,)).fetchone()
    except sqlite3.OperationalError:            # a store that never stored a kind
        return None
    return row[0] if row else None


def kind_of(conn, edge):
    if ALL_READS:
        return 'reads'
    kind = stored_kind(conn, edge['dependency_id'])
    if kind:
        return kind
    seeded = conn.execute("select 1 from views where view_id = ? and lower(substr(created_from_input, 1, 5)) = 'seed:'", (edge['view_id'],)).fetchone()
    if seeded and edge['seq'] == 0 and edge['direction'] == 'last_end':
        return 'supports'
    if not seeded and edge['seq'] > 0 and edge['direction'] in MATCHING_LABELS:
        return 'reads'
    raise AmbiguousEdge(f"dependency {edge['dependency_id']} ({edge['view_id']} -> {edge['depends_on']}) carries no stored kind and neither writer's marks: refused")


def record_kinds(conn, kind, after_id):
    """Stores the kind of every edge written after `after_id`, in the writer's own transaction."""
    if KIND_NOT_STORED:
        return
    conn.execute('create table if not exists dependency_kinds (dependency_id integer primary key, kind text not null)')
    for row in conn.execute('select dependency_id from dependencies where dependency_id > ?', (after_id,)).fetchall():
        conn.execute('insert into dependency_kinds (dependency_id, kind) values (?, ?)', (row[0], kind))


def _last_id(conn):
    return conn.execute('select coalesce(max(dependency_id), 0) from dependencies').fetchone()[0]


def install_writers():
    """Wraps the two production writers so that each stores the kind of the edges it writes."""
    assert 'seed_views' not in _ORIGINAL
    _ORIGINAL.update(seed_views=seeding.seed_views, write=writing.write)

    def seed_views(conn, *args, **kwargs):
        before = _last_id(conn)
        result = _ORIGINAL['seed_views'](conn, *args, **kwargs)
        record_kinds(conn, 'supports', before)
        return result

    def write(conn, *args, **kwargs):
        before = _last_id(conn)
        result = _ORIGINAL['write'](conn, *args, **kwargs)
        record_kinds(conn, 'reads', before)
        return result

    seeding.seed_views, writing.write = seed_views, write


def restore_writers():
    seeding.seed_views, writing.write = _ORIGINAL.pop('seed_views'), _ORIGINAL.pop('write')


def propose(conn, view_id, depends_on, kind, seq, direction='first_is_bullish'):
    """The writer's steps for one proposed `reads` edge under the rule. When the reading relation already holds the pair: 'already read'
    if the edge that gives it is a `reads` edge with the same direction label (a duplicate: nothing is written); 'conflicting label'
    if it is a `reads` edge with another label (a disagreement, refused, never dropped silently: PRD 06, "a dependency has one
    direction"); 'label undefined' if it is a `supports` edge, whose label ('last_end') no decision or document defines, so equal
    and conflicting cannot be told apart. 'cycle' when the edge would close a circle. Else 'written'."""
    assert kind == 'reads', 'these proofs propose no new supports edge'
    existing = [dep for dep in store.dependencies_of(conn, view_id) if dep['resolved_to'] == depends_on]
    if existing and not DUPLICATES_WRITTEN:
        giving = existing[0]
        if giving['kind'] == 'supports':
            return 'label undefined'
        return 'already read' if giving['direction'] == direction else 'conflicting label'
    if store.would_cycle(conn, view_id, depends_on):
        return 'cycle'
    before = _last_id(conn)
    store.insert(conn, 'dependencies', view_id=view_id, depends_on=depends_on, wait_chain_view_id='', wait_year='', direction=direction, seq=seq)
    record_kinds(conn, 'reads', before)
    conn.commit()
    return 'written'


def _edges(conn):
    return [dict(row) for row in conn.execute('select * from dependencies order by dependency_id')]


def reading_dependencies_of(conn, view_id):
    """What the question reads: its own `reads` edges as stored (with their waiting and successor fields), and each question that supports it."""
    out = [dict(dep, kind='reads') for dep in _ORIGINAL['dependencies_of'](conn, view_id) if kind_of(conn, dep) == 'reads']
    for edge in _edges(conn):
        if edge['depends_on'] == view_id and kind_of(conn, edge) == 'supports':
            out.append({'dependency_id': edge['dependency_id'], 'view_id': view_id, 'depends_on': edge['view_id'], 'resolved_to': edge['view_id'], 'resolution': 'direct',
                        'direction': edge['direction'], 'wait_chain_view_id': '', 'wait_year': '', 'seq': edge['seq'], 'kind': 'supports'})
    return out


def reading_dependants_of(conn, view_id):
    """The questions that read this one: those with a `reads` edge to it (or resolved to it), and the questions it supports."""
    readers = set()
    for edge in _edges(conn):
        if kind_of(conn, edge) == 'supports':
            if edge['view_id'] == view_id:
                readers.add(edge['depends_on'])
        else:
            resolution = conn.execute('select resolved_to from dependency_resolutions where dependency_id = ? order by id desc limit 1', (edge['dependency_id'],)).fetchone()
            if (resolution['resolved_to'] if resolution else edge['depends_on']) == view_id:
                readers.add(edge['view_id'])
    return sorted(readers)


def narrower_parents(conn, view_id, seq=None):
    """The questions this one is the narrower home of: its `supports` edges, written at or before `seq` when given."""
    rows = conn.execute("select * from dependencies where view_id = ? and depends_on != '' and (? is null or seq <= ?) order by dependency_id", (view_id, seq, seq))
    return list(dict.fromkeys(row['depends_on'] for row in rows if kind_of(conn, dict(row)) == 'supports'))


def add(conn, view_id, depends_on, kind, seq, direction='first_is_bullish'):
    """The writer's steps for one edge under the separation: refuse a circle in the reading relation, then insert. Returns whether it was written."""
    reader, read = (view_id, depends_on) if kind == 'reads' else (depends_on, view_id)
    if store.would_cycle(conn, reader, read):
        return False
    assert kind == 'reads', 'these proofs write no new supports edge'
    store.insert(conn, 'dependencies', view_id=view_id, depends_on=depends_on, wait_chain_view_id='', wait_year='', direction=direction, seq=seq)
    conn.commit()
    return True


def install():
    assert 'dependencies_of' not in _ORIGINAL
    _ORIGINAL.update(dependencies_of=store.dependencies_of, dependants_of=store.dependants_of, direct_parents=store.direct_parents)
    store.dependencies_of, store.dependants_of, store.direct_parents = reading_dependencies_of, reading_dependants_of, narrower_parents


def restore():
    store.dependencies_of, store.dependants_of, store.direct_parents = _ORIGINAL.pop('dependencies_of'), _ORIGINAL.pop('dependants_of'), _ORIGINAL.pop('direct_parents')
