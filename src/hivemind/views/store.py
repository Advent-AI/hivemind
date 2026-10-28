"""The views database (docs/prd/06-views.md): append-only tables for views, rungs, judgements, evidence, links,
replacements, dependencies, successions, match records, processing steps and the review pool; a trigram
full-text index over the views for the matching lists; the queries the other modules read.

Every table refuses UPDATE and DELETE (triggers). Progress and counts are rows, never updates. There is no item
text here: evidence holds the quoted sentence and the one-line restatement only.
"""
import json
import os
import re
import sqlite3

TABLES = {
    'views': 'view_id text primary key, object_id text, object_kind text, kind text, looks_at text, question text, due_day text, year text, created_seq integer, created_from_input text, created_at text',
    'rungs': 'view_id text, position integer, label text, condition text, lo real, hi real',
    'view_keys': 'view_id text primary key, measure text, scope text, scope_key text, period_start text, period_end text, basis text, unit text, event_type text, seq integer, scope_source text, key_version integer',
    'view_switches': 'id integer primary key autoincrement, view_id text, open integer, reason text, by_whom text, after_seq integer',
    'judgements': 'judgement_id integer primary key autoincrement, view_id text, seq integer, input_id text, rung integer, reasons text, cited_evidence_json text, cited_views_json text, pushes_json text, changed integer, why_changed text, config_checksum text, call_id integer, request_sha256 text, publication_day text, theme_pushes_json text',
    'evidence': 'evidence_id text primary key, quote text, one_line text, speaker text, original_who text, original_day text, tier text, event_time text, created_seq integer, created_from_input text',
    'evidence_sources': 'id integer primary key autoincrement, evidence_id text, input_id text, category text, publication_day text, location text, seq integer',
    'evidence_links': 'id integer primary key autoincrement, evidence_id text, view_id text, seq integer',
    'replacements': 'id integer primary key autoincrement, old_evidence_id text, new_evidence_id text, said_day text, seq integer',   # history: written before D202, read as before
    'revisions': 'id integer primary key autoincrement, old_evidence_id text, new_evidence_id text, said_day text, seq integer',      # D202: the new piece revises the old; both stay in force
    'same_claims': 'id integer primary key autoincrement, old_evidence_id text, new_evidence_id text, seq integer',                    # D204: the matcher read the new piece as the same claim as the old; both stored, both in force
    'dependencies': 'dependency_id integer primary key autoincrement, view_id text, depends_on text, wait_chain_view_id text, wait_year text, direction text, seq integer',
    'dependency_resolutions': 'id integer primary key autoincrement, dependency_id integer, resolved_to text, reason text, seq integer',
    'successions': 'id integer primary key autoincrement, view_id text, succeeds text, seq integer',
    'handovers': 'id integer primary key autoincrement, input_id text, seq integer, handover_json text',
    'match_records': 'id integer primary key autoincrement, seq integer, input_id text, call_no integer, shown_json text, request_sha256 text, call_id integer, decisions_json text, checks_json text, written_json text',
    'processing_steps': 'id integer primary key autoincrement, input_id text, sequence_no integer, step text, result text, reason text, publication_day text, at text',
    'review_pool_entries': 'id integer primary key autoincrement, kind text, key text, example_json text, seq integer',
    'late_statements': 'id integer primary key autoincrement, input_id text, evidence_quote text, reason text, seq integer',
    'unplaced_statements': 'id integer primary key autoincrement, input_id text, seq integer, publication_day text, statement_json text',   # v20: a material statement the placer filed under no thesis; kept for a later placement
    'days_completed': 'id integer primary key autoincrement, day text, seq integer, at text',
    # D149 research groups: an ongoing business subject several distinct theses belong to; membership is decided by extraction and written with the thesis
    'thesis_groups': 'group_id text primary key, name text, scope text, aliases text, created_seq integer, created_from_input text',
    'thesis_group_members': 'id integer primary key autoincrement, group_id text, view_id text, seq integer, input_id text, basis text',
}

INDEXES = [
    'create index if not exists views_object on views(object_id)',
    'create index if not exists judgements_view on judgements(view_id, judgement_id)',
    # 06-views step 7: a view is judged once per round (one item = one sequence number)
    'create unique index if not exists judgements_once_per_round on judgements(view_id, seq)',
    'create index if not exists links_view on evidence_links(view_id)',
    'create index if not exists links_evidence on evidence_links(evidence_id)',
    'create index if not exists sources_evidence on evidence_sources(evidence_id)',
    'create index if not exists steps_input on processing_steps(input_id, id)',
    'create index if not exists switches_view on view_switches(view_id, id)',
    'create index if not exists deps_view on dependencies(view_id)',
]


def open_db(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    for name, columns in TABLES.items():
        conn.execute(f'create table if not exists {name} ({columns})')
        conn.execute(f"create trigger if not exists {name}_no_update before update on {name} begin select raise(abort, 'append-only'); end")
        conn.execute(f"create trigger if not exists {name}_no_delete before delete on {name} begin select raise(abort, 'append-only'); end")
    for statement in INDEXES:
        conn.execute(statement)
    ensure_writable_columns(conn)
    conn.execute("create virtual table if not exists views_fts using fts5(view_id unindexed, text, tokenize='trigram')")
    conn.execute("create virtual table if not exists groups_fts using fts5(group_id unindexed, text, tokenize='trigram')")
    conn.execute('create index if not exists members_view on thesis_group_members(view_id)')
    conn.commit()
    return conn


def insert(conn, table, **fields):
    columns = list(fields)
    cursor = conn.execute(f'insert into {table} ({",".join(columns)}) values ({",".join("?" * len(columns))})', [fields[c] for c in columns])
    return cursor.lastrowid


# ---------- views ----------

def create_view(conn, *, view_id, object_id, object_kind, kind, looks_at, question, due_day, year, rungs, seq, input_id, created_at):
    insert(conn, 'views', view_id=view_id, object_id=object_id, object_kind=object_kind, kind=kind, looks_at=looks_at,
           question=question, due_day=due_day, year=year, created_seq=seq, created_from_input=input_id, created_at=created_at)
    for position, rung in enumerate(rungs, start=1):
        insert(conn, 'rungs', view_id=view_id, position=position, label=rung['label'], condition=rung['condition'], lo=rung.get('lo'), hi=rung.get('hi'))
    insert(conn, 'view_switches', view_id=view_id, open=1, reason='created', by_whom='matching', after_seq=seq)
    conn.execute('insert into views_fts (view_id, text) values (?, ?)', (view_id, f'{object_id} {looks_at} {question}'))


def view(conn, view_id):
    row = conn.execute('select * from views where view_id=?', (view_id,)).fetchone()
    return dict(row) if row else None


def rungs_of(conn, view_id):
    """The rungs with their bounds when the ledger has them (keyed views); a ledger written before keys has no lo/hi columns."""
    rows = [dict(r) for r in conn.execute('select * from rungs where view_id=? order by position', (view_id,))]
    has_bounds = any(r.get('lo') is not None or r.get('hi') is not None for r in rows) or view_key(conn, view_id) is not None
    return [dict(position=r['position'], label=r['label'], condition=r['condition'],
                 **({'lo': r.get('lo'), 'hi': r.get('hi')} if has_bounds else {})) for r in rows]


def add_key(conn, view_id, key, seq):
    """The view's key (keyed-views-plan.md 2.1), written once with the view."""
    from .. import universe as _universe
    from .identity import is_shared
    scope_source = 'shared' if is_shared(key) else key.get('scope_source', 'model')      # D197: an aggregate's scope is wording
    insert(conn, 'view_keys', view_id=view_id, measure=key['measure'], scope=key.get('scope', ''), scope_key=_universe.scope_key(key.get('scope', '')),
           period_start=key.get('period_start', ''), period_end=key.get('period_end', ''), basis=key.get('basis', 'n/a'), unit=key.get('unit', 'n/a'),
           event_type=key.get('event_type', 'n/a'), seq=seq, scope_source=scope_source, key_version=key.get('key_version'))


def ensure_key_columns(conn):
    """A keyed ledger written before `scope_source` gains the column (append-only forbids updates, not new columns); its
    earlier keys read as model-owned scopes unless the scope is empty."""
    columns = [r[1] for r in conn.execute('pragma table_info(view_keys)')]
    if columns and 'scope_source' not in columns:
        conn.execute('alter table view_keys add column scope_source text')
    if columns and 'key_version' not in columns:
        conn.execute('alter table view_keys add column key_version integer')


def ensure_group_tables(conn):
    """A ledger written before research groups (D165) gains the group tables at its first write; nothing else changes."""
    for name in ('thesis_groups', 'thesis_group_members'):
        conn.execute(f'create table if not exists {name} ({TABLES[name]})')
        conn.execute(f"create trigger if not exists {name}_no_update before update on {name} begin select raise(abort, 'append-only'); end")
        conn.execute(f"create trigger if not exists {name}_no_delete before delete on {name} begin select raise(abort, 'append-only'); end")
    conn.execute("create virtual table if not exists groups_fts using fts5(group_id unindexed, text, tokenize='trigram')")
    conn.execute('create index if not exists members_view on thesis_group_members(view_id)')
    columns = {r[1] for r in conn.execute('pragma table_info(thesis_groups)')}
    if 'aliases' not in columns:
        conn.execute('alter table thesis_groups add column aliases text')
    columns = {r[1] for r in conn.execute('pragma table_info(thesis_group_members)')}
    if 'basis' not in columns:
        conn.execute('alter table thesis_group_members add column basis text')


def ensure_writable_columns(conn):
    """Upgrade columns at a write boundary, including a legacy database restored into an open connection."""
    ensure_key_columns(conn)
    ensure_group_tables(conn)
    columns = {r[1] for r in conn.execute('pragma table_info(rungs)')}
    for field in ('lo', 'hi'):
        if field not in columns:
            conn.execute(f'alter table rungs add column {field} real')
    if 'theme_pushes_json' not in {r[1] for r in conn.execute('pragma table_info(judgements)')}:
        conn.execute('alter table judgements add column theme_pushes_json text')     # D195: judgements written before the theme block read as []


def view_key(conn, view_id):
    if not conn.execute('pragma table_info(view_keys)').fetchone():
        return None
    row = conn.execute('select * from view_keys where view_id=?', (view_id,)).fetchone()
    if not row:
        return None
    key = dict(row)
    if not key.get('scope_source'):
        key['scope_source'] = 'none' if not key['scope'] else 'model'
    return key


def open_views_with_key(conn, object_id, measure, scope_key, period_start, period_end, basis='n/a', unit='n/a', event_type=None):
    """Open views of the object with the same measure, scope and unit whose period overlaps: the ones a candidate must
    be confirmed against before it may open (keyed-views-plan.md 2.5). A basis or unit of n/a on either side matches
    any; GAAP and non-GAAP are two quantities, and so are a level in USD and a growth rate in percent."""
    rows = [dict(r) for r in conn.execute('''select k.* from view_keys k join views v on v.view_id=k.view_id
                                            where v.object_id=? and k.measure=? order by v.rowid''', (object_id, measure))]
    return [r['view_id'] for r in rows if is_open(conn, r['view_id'])
            and (event_type is None or r['event_type'] == event_type)
            and (basis == 'n/a' or r['basis'] == 'n/a' or r['basis'] == basis)
            and (unit == 'n/a' or r['unit'] == 'n/a' or r['unit'] == unit)
            and (r.get('key_version') != 2 or ((scope_key is None or r['scope_key'] == scope_key)
                 and r['period_start'] <= (period_end or '9999') and r['period_end'] >= (period_start or '0000')))]


def exact_key_views(conn, candidate):
    """All open exact identities, independent of a search limit; legacy keys are never automatic identities."""
    from .identity import automatic_key
    target = automatic_key(candidate)
    if target is None:
        return []
    rows = conn.execute('''select k.*, v.object_id from view_keys k join views v on v.view_id=k.view_id
                           where v.object_id=? and k.measure=?''', (candidate['object'], candidate['measure']))
    return [r['view_id'] for r in rows if automatic_key(dict(r), r['object_id']) == target and is_open(conn, r['view_id'])]


def is_open(conn, view_id):
    row = conn.execute('select open from view_switches where view_id=? order by id desc limit 1', (view_id,)).fetchone()
    return bool(row and row['open'])


def close_view(conn, view_id, reason, by_whom, seq):
    insert(conn, 'view_switches', view_id=view_id, open=0, reason=reason, by_whom=by_whom, after_seq=seq)


def open_views(conn):
    rows = conn.execute('select view_id from views').fetchall()
    return [r['view_id'] for r in rows if is_open(conn, r['view_id'])]


def views_of_object(conn, object_id, only_open=True):
    rows = conn.execute('select view_id from views where object_id=? order by created_seq', (object_id,)).fetchall()
    ids = [r['view_id'] for r in rows]
    return [v for v in ids if is_open(conn, v)] if only_open else ids


def has_judgement(conn, view_id, seq):
    return conn.execute('select 1 from judgements where view_id=? and seq=?', (view_id, seq)).fetchone() is not None


def open_read_only(path):
    """The views database for a reader (the agent layer, reports): no schema creation, no writes."""
    conn = sqlite3.connect(f'file:{os.path.abspath(path)}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def current_state(conn, view_id):
    row = conn.execute('select judgement_id, rung, reasons, changed, seq, publication_day from judgements where view_id=? order by judgement_id desc limit 1', (view_id,)).fetchone()
    return dict(row) if row else None


def dependencies_of(conn, view_id):
    """Each dependency with its current target: the resolved view, or the waiting chain and year."""
    out = []
    for dep in conn.execute('select * from dependencies where view_id=? order by dependency_id', (view_id,)):
        dep = dict(dep)
        resolution = conn.execute('select resolved_to, reason from dependency_resolutions where dependency_id=? order by id desc limit 1', (dep['dependency_id'],)).fetchone()
        if resolution:
            dep['resolved_to'], dep['resolution'] = resolution['resolved_to'], resolution['reason']
        else:
            dep['resolved_to'], dep['resolution'] = dep['depends_on'], ('direct' if dep['depends_on'] else 'waiting')
        out.append(dep)
    return out


def dependants_of(conn, view_id):
    direct = [r['view_id'] for r in conn.execute('select view_id from dependencies where depends_on=?', (view_id,))]
    resolved = [r['view_id'] for r in conn.execute(
        'select d.view_id from dependency_resolutions r join dependencies d on d.dependency_id=r.dependency_id where r.resolved_to=?', (view_id,))]
    return sorted(set(direct + resolved))


def would_cycle(conn, view_id, depends_on):
    """True when depends_on already depends, directly or through its dependencies, on view_id."""
    seen, stack = set(), [depends_on]
    while stack:
        current = stack.pop()
        if current == view_id:
            return True
        if current in seen or not current:
            continue
        seen.add(current)
        for dep in dependencies_of(conn, current):
            if dep['resolved_to']:
                stack.append(dep['resolved_to'])
    return False


def views_for_prompt(conn, object_ids, themes=False):
    """05-extraction block 5: the objects' open views plus every view they depend on, open or closed, with who
    depends on whom; question, looks_at and due day only. With themes, every open theme thesis follows the objects' own
    (A, extraction v19): a company item's statement about a theme matter links to the theme thesis instead of being dropped."""
    shown, order = {}, []
    for object_id in object_ids:
        for view_id in views_of_object(conn, object_id):
            if view_id not in shown:
                shown[view_id] = dict(view(conn, view_id), open=True, depends_on=[], dependencies=[])
                order.append(view_id)
    if themes:
        for row in conn.execute("select view_id from views where kind='theme' order by created_seq"):
            if row['view_id'] not in shown and is_open(conn, row['view_id']):
                shown[row['view_id']] = dict(view(conn, row['view_id']), open=True, depends_on=[], dependencies=[])
                order.append(row['view_id'])
        order.sort(key=lambda view_id: shown[view_id]['created_seq'])      # one list in creation order
    for view_id in list(order):
        for dep in dependencies_of(conn, view_id):
            target = dep['resolved_to']
            # depends_on keeps the text the Chinese prompt versions print; dependencies is the same list structured, for any builder
            shown[view_id]['depends_on'].append(target or f'（等 {dep["wait_chain_view_id"]} 这条链上 {dep["wait_year"]} 年的那条）')
            shown[view_id]['dependencies'].append({'view_id': target} if target else {'view_id': None, 'wait_chain_view_id': dep['wait_chain_view_id'], 'wait_year': dep['wait_year']})
            if target and target not in shown:
                record = view(conn, target)
                if record:
                    shown[target] = dict(record, open=is_open(conn, target), depends_on=[], dependencies=[])
                    order.append(target)
    return [dict(shown[v], rungs=rungs_of(conn, v)) for v in order]


def search_views(conn, text, top_n):
    """Trigram full-text search over question + looks_at + object; the top N by rank."""
    words = [w for w in text.replace('？', ' ').replace('，', ' ').split() if len(w) >= 2]
    if not words:
        return []
    query = ' OR '.join('"' + w.replace('"', '') + '"' for w in words[:12])
    try:
        rows = conn.execute('select view_id from views_fts where views_fts match ? order by rank limit ?', (query, top_n)).fetchall()
    except sqlite3.OperationalError:
        return []
    return [r['view_id'] for r in rows]


# ---------- evidence ----------

def add_unplaced(conn, input_id, seq, publication_day, statement):
    insert(conn, 'unplaced_statements', input_id=input_id, seq=seq, publication_day=publication_day, statement_json=json.dumps(statement, ensure_ascii=False))


def add_evidence(conn, *, evidence_id, quote, one_line, speaker, original_who, original_day, tier, event_time, seq, input_id):
    insert(conn, 'evidence', evidence_id=evidence_id, quote=quote, one_line=one_line, speaker=speaker, original_who=original_who,
           original_day=original_day, tier=tier, event_time=event_time, created_seq=seq, created_from_input=input_id)


def add_source(conn, evidence_id, input_id, category, publication_day, location, seq):
    insert(conn, 'evidence_sources', evidence_id=evidence_id, input_id=input_id, category=category, publication_day=publication_day, location=location, seq=seq)


def link(conn, evidence_id, view_id, seq):
    exists = conn.execute('select 1 from evidence_links where evidence_id=? and view_id=?', (evidence_id, view_id)).fetchone()
    if not exists:
        insert(conn, 'evidence_links', evidence_id=evidence_id, view_id=view_id, seq=seq)
        return True
    return False


def replace(conn, old_id, new_id, said_day, seq):
    """Retires old_id (history before D202; kept for the readers and tests of stored ledgers, no longer called by the writer)."""
    insert(conn, 'replacements', old_evidence_id=old_id, new_evidence_id=new_id, said_day=said_day, seq=seq)


def revise(conn, old_id, new_id, said_day, seq):
    """D202: new_id is the matcher's later version of old_id; both stay in force, the judge sees the path."""
    insert(conn, 'revisions', old_evidence_id=old_id, new_evidence_id=new_id, said_day=said_day, seq=seq)


def relate_same(conn, old_id, new_id, seq):
    """D204: the matcher's opinion that new_id restates old_id; a labelled relation, never a merge."""
    insert(conn, 'same_claims', old_evidence_id=old_id, new_evidence_id=new_id, seq=seq)


def same_claim_group(conn, evidence_id):
    """The other pieces related to this one as the same claim, in either direction (empty on a ledger without the table)."""
    if not conn.execute("select 1 from sqlite_master where type='table' and name='same_claims'").fetchone():
        return []
    rows = conn.execute('select old_evidence_id, new_evidence_id from same_claims where old_evidence_id=? or new_evidence_id=?', (evidence_id, evidence_id)).fetchall()
    return sorted(({r['old_evidence_id'] for r in rows} | {r['new_evidence_id'] for r in rows}) - {evidence_id}, key=lambda x: int(x[1:]) if x[1:].isdigit() else x)


def revision_of(conn, evidence_id):
    """None on a ledger written before D202 (no revisions table), which read-only openers cannot extend."""
    if not conn.execute("select 1 from sqlite_master where type='table' and name='revisions'").fetchone():
        return None
    row = conn.execute('select old_evidence_id from revisions where new_evidence_id=? order by id desc limit 1', (evidence_id,)).fetchone()
    return row['old_evidence_id'] if row else None


def recent_judgements(conn, view_id, n):
    """The thesis's last n judgements, newest first: (seq, cited evidence ids)."""
    rows = conn.execute('select seq, cited_evidence_json from judgements where view_id=? order by judgement_id desc limit ?', (view_id, n)).fetchall()
    return [{'seq': r['seq'], 'cites': json.loads(r['cited_evidence_json'] or '[]')} for r in rows]


def is_replaced(conn, evidence_id):
    return bool(conn.execute('select 1 from replacements where old_evidence_id=?', (evidence_id,)).fetchone())


def predecessor_of(conn, evidence_id):
    row = conn.execute('select old_evidence_id from replacements where new_evidence_id=? order by id desc limit 1', (evidence_id,)).fetchone()
    return row['old_evidence_id'] if row else None


def evidence(conn, evidence_id):
    row = conn.execute('select * from evidence where evidence_id=?', (evidence_id,)).fetchone()
    if not row:
        return None
    record = dict(row)
    record['sources'] = [dict(s) for s in conn.execute('select input_id, category, publication_day, location from evidence_sources where evidence_id=? order by id', (evidence_id,))]
    return record


def evidence_in_force(conn, view_id):
    """Evidence linked to the view and not replaced (history), each with its replaced predecessor when there is one and, since D202,
    the piece it revises (both in force)."""
    out = []
    for row in conn.execute('select evidence_id from evidence_links where view_id=? order by id', (view_id,)):
        evidence_id = row['evidence_id']
        if is_replaced(conn, evidence_id):
            continue
        record = evidence(conn, evidence_id)
        previous = predecessor_of(conn, evidence_id)
        record['replaced'] = evidence(conn, previous) if previous else None
        revised = revision_of(conn, evidence_id)
        record['revises'] = evidence(conn, revised) if revised else None
        record['same_as'] = [x for x in same_claim_group(conn, evidence_id) if not is_replaced(conn, x)]
        out.append(record)
    return out


def views_linked_to(conn, evidence_id):
    return [r['view_id'] for r in conn.execute('select view_id from evidence_links where evidence_id=? order by id', (evidence_id,))]


def evidence_ids_under(conn, view_id):
    return [r['evidence_id'] for r in conn.execute('select evidence_id from evidence_links where view_id=?', (view_id,))]


# ---------- processing record and pool ----------

def mark_step(conn, input_id, sequence_no, step, result, reason, publication_day, at):
    insert(conn, 'processing_steps', input_id=input_id, sequence_no=sequence_no, step=step, result=result, reason=reason, publication_day=publication_day, at=at)


def last_step(conn, input_id):
    row = conn.execute('select step, result, sequence_no from processing_steps where input_id=? order by id desc limit 1', (input_id,)).fetchone()
    return dict(row) if row else None


def is_processed(conn, input_id):
    return bool(conn.execute("select 1 from processing_steps where input_id=? and step='handed_over' and result='ok'", (input_id,)).fetchone())


def next_sequence(conn):
    row = conn.execute('select coalesce(max(sequence_no), 0) from processing_steps').fetchone()
    return int(row[0]) + 1


def pool(conn, kind, key, example, seq):
    insert(conn, 'review_pool_entries', kind=kind, key=key, example_json=json.dumps(example, ensure_ascii=False)[:4000], seq=seq)


def last_check(conn, view_id):
    """The last round that read this view: its item's publication day and id (the card's 上次核对 line)."""
    row = conn.execute('select input_id, publication_day from judgements where view_id=? order by judgement_id desc limit 1', (view_id,)).fetchone()
    if row:
        return row['publication_day'], row['input_id']
    row = conn.execute('select s.publication_day, s.input_id from evidence_links l join evidence_sources s on s.evidence_id=l.evidence_id where l.view_id=? order by s.id desc limit 1', (view_id,)).fetchone()
    return (row['publication_day'], row['input_id']) if row else (None, None)


def complete_day(conn, day, seq, at):
    insert(conn, 'days_completed', day=day, seq=seq, at=at)


def last_completed_day(conn):
    row = conn.execute('select day from days_completed order by id desc limit 1').fetchone()
    return row['day'] if row else None


# ---------- research groups (D149) ----------

def add_group(conn, *, group_id, name, scope, seq, input_id, object_ids=(), aliases=()):
    """A research group, created when the first accepted thesis that cites it is written, with the names it goes by; the
    search text carries the objects of its members so that an item about those objects finds it."""
    insert(conn, 'thesis_groups', group_id=group_id, name=name, scope=scope, aliases=json.dumps(list(aliases), ensure_ascii=False), created_seq=seq, created_from_input=input_id)
    conn.execute('insert into groups_fts (group_id, text) values (?, ?)', (group_id, f'{" ".join(object_ids)} {name} {scope} {" ".join(aliases)}'))


def add_member(conn, group_id, view_id, seq, input_id, basis='model'):
    """basis: 'model' when the model cited the group, 'alias:<name>' when the thesis's own text carries the group's name."""
    if conn.execute('select 1 from thesis_group_members where group_id=? and view_id=?', (group_id, view_id)).fetchone():
        return False
    insert(conn, 'thesis_group_members', group_id=group_id, view_id=view_id, seq=seq, input_id=input_id, basis=basis)
    return True


def _group_record(row):
    """A thesis_groups row with its aliases as a list (stored as JSON text)."""
    record = dict(row)
    stored = record.get('aliases')
    record['aliases'] = json.loads(stored or '[]') if isinstance(stored, str) else list(stored or [])
    return record


def group(conn, group_id):
    row = conn.execute('select * from thesis_groups where group_id=?', (group_id,)).fetchone()
    return _group_record(row) if row else None


def groups_of_view(conn, view_id):
    return [_group_record(r) for r in conn.execute('select g.* from thesis_group_members m join thesis_groups g on g.group_id=m.group_id where m.view_id=? order by m.id', (view_id,))]


def members_of_group(conn, group_id):
    return [r['view_id'] for r in conn.execute('select view_id from thesis_group_members where group_id=? order by id', (group_id,))]


def groups_for_prompt(conn, object_ids, text, top_n=10):
    """05-extraction block 5b: the research groups the model may place a candidate in: every group with a member among
    the objects' views, then the top N groups whose name, scope or objects match the item's title and objects (other
    companies included). Each with its member theses' focus, so the model reads what the subject is about."""
    found, order = {}, []
    for object_id in object_ids:
        for row in conn.execute("""select distinct g.* from thesis_groups g join thesis_group_members m on m.group_id=g.group_id
                                   join views v on v.view_id=m.view_id where v.object_id=? order by g.created_seq""", (object_id,)):
            if row['group_id'] not in found:
                found[row['group_id']] = _group_record(row); order.append(row['group_id'])
    words = [w for w in re.findall(r'[A-Za-z0-9][A-Za-z0-9.&-]+', f'{" ".join(object_ids)} {text or ""}') if len(w) >= 3]
    if words:
        query = ' OR '.join('"' + w.replace('"', '') + '"' for w in dict.fromkeys(words[:24]))
        try:
            for r in conn.execute('select group_id from groups_fts where groups_fts match ? order by rank limit ?', (query, top_n)):
                if r['group_id'] not in found:
                    found[r['group_id']] = group(conn, r['group_id']); order.append(r['group_id'])
        except sqlite3.OperationalError:
            pass
    out = []
    for group_id in order:
        members = members_of_group(conn, group_id)
        out.append(dict(found[group_id], members=[{'view_id': v, 'object_id': view(conn, v)['object_id'], 'looks_at': view(conn, v)['looks_at']} for v in members]))
    return out
