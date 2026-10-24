"""Exit conditions and events. A condition says: for this user and view, if the judgement falls to rung N or worse
(a higher position on the ladder), do this action. `scan` reads the views database's judgement records after a
sequence number and emits, once per judgement, a 'changed' event for any judgement that says changed on a held
view, and a 'crossed' event when the rung crosses the condition. Each event carries the judgement's own cited
evidence (quote, tier, source, day), never today's evidence in force."""
import json
import os
import sqlite3
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import store  # noqa: E402

SCHEMA = """
create table if not exists conditions (condition_id integer primary key autoincrement, user text, view_id text, threshold_rung integer, action text, set_seq integer, set_day text, belief text, created_at text);
create table if not exists events (event_id integer primary key autoincrement, kind text, user text, view_id text, judgement_id integer, rung_before integer, rung_after integer, action text, publication_day text, cited_json text, created_at text, unique (user, judgement_id));
create table if not exists mappings (id integer primary key autoincrement, user text, sentence text, view_id text, difference text, nearest_json text, settlement_day text, call_id integer, created_at text);
"""


def open_db(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def set_condition(conn_agent, user, view_id, threshold_rung, action, set_seq, set_day, belief=''):
    cursor = conn_agent.execute('insert into conditions (user, view_id, threshold_rung, action, set_seq, set_day, belief, created_at) values (?,?,?,?,?,?,?,?)',
                                (user, view_id, threshold_rung, action, set_seq, set_day, belief, time.strftime('%Y-%m-%dT%H:%M:%S')))
    conn_agent.commit()
    return cursor.lastrowid


def record_mapping(conn_agent, user, mapping):
    conn_agent.execute('insert into mappings (user, sentence, view_id, difference, nearest_json, settlement_day, call_id, created_at) values (?,?,?,?,?,?,?,?)',
                       (user, mapping['sentence'], mapping['view_id'], mapping['difference'], json.dumps(mapping['nearest']), mapping['settlement_day'], mapping['call_id'], time.strftime('%Y-%m-%dT%H:%M:%S')))
    conn_agent.commit()


def _cited(conn_views, judgement):
    cited = json.loads(judgement['cited_evidence_json'] or '[]')
    out = []
    for evidence_id in cited:
        e = store.evidence(conn_views, evidence_id)
        if not e:
            continue
        src = e['sources'][0] if e['sources'] else {}
        out.append({'evidence_id': evidence_id, 'quote': e['quote'], 'one_line': e['one_line'], 'tier': e['tier'],
                    'speaker': e['speaker'], 'input_id': src.get('input_id'), 'publication_day': src.get('publication_day')})
    return out


def scan(conn_views, conn_agent, after_seq=0):
    """Emit events for judgements after after_seq on views that some user holds a condition on."""
    held = {}
    for c in conn_agent.execute('select * from conditions order by condition_id'):
        held.setdefault(c['view_id'], []).append(dict(c))
    if not held:
        return []
    events = []
    placeholders = ','.join('?' * len(held))
    rows = conn_views.execute(f'select * from judgements where seq > ? and view_id in ({placeholders}) order by judgement_id', [after_seq] + list(held)).fetchall()
    for j in rows:
        previous = conn_views.execute('select rung from judgements where view_id=? and judgement_id<? order by judgement_id desc limit 1', (j['view_id'], j['judgement_id'])).fetchone()
        before = previous['rung'] if previous else None
        for condition in held[j['view_id']]:
            if j['seq'] <= (condition['set_seq'] or 0):      # the condition was set after that sequence number
                continue
            crossed = (before is None or before < condition['threshold_rung']) and j['rung'] >= condition['threshold_rung']
            # an event for the user is a judgement that moved the rung (or crossed the condition); a judgement that
            # says "changed" but keeps the rung re-weighed its evidence, which the bet card shows and no alert does
            kind = 'crossed' if crossed else ('changed' if j['changed'] and before is not None and before != j['rung'] else None)
            if not kind:
                continue
            try:
                conn_agent.execute('insert into events (kind, user, view_id, judgement_id, rung_before, rung_after, action, publication_day, cited_json, created_at) values (?,?,?,?,?,?,?,?,?,?)',
                                   (kind, condition['user'], j['view_id'], j['judgement_id'], before, j['rung'], condition['action'] if crossed else '',
                                    j['publication_day'], json.dumps(_cited(conn_views, j), ensure_ascii=False), time.strftime('%Y-%m-%dT%H:%M:%S')))
                conn_agent.commit()
            except sqlite3.IntegrityError:
                continue   # one event per judgement per user
            events.append({'kind': kind, 'user': condition['user'], 'view_id': j['view_id'], 'judgement_id': j['judgement_id'],
                           'rung_before': before, 'rung_after': j['rung'], 'day': j['publication_day'], 'action': condition['action'] if crossed else ''})
    return events
