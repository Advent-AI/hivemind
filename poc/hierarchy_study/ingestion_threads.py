"""D144: resolve continuing business subjects in the existing ingestion identity call."""
import argparse
import dataclasses
import fcntl
import json
import re
from pathlib import Path

import ingestion_groups as base
import relation_handoff as control
import study
from hivemind import dispatch, universe
from hivemind.views import matching, store, writing

EXTRA_ITEM = 'gnews:f2bbeb9e369dca841a5a0381'
EXTRACT_THREADS = """ Organize proposed theses by continuing business subject: a product rollout, investment
program, demand cycle or policy process. Name its scope and attach its theses. A subject spans separate metrics,
milestones, customer deployments and dates; describe that process, not a thesis's yes/no question. A company alone
is too broad. Subjects organize research; they are not causal claims or evidence."""
MATCH_THREADS = """ Resolve each business subject to the same continuing development in the thread search
results, or create one. Different milestones, customer deployments and dates within a product rollout or program
retain its identity while remaining distinct theses. A shared company alone is insufficient. Local descriptions
of one development may resolve to one another. Use an offered g-ID, a local t-ID, or empty for a new thread."""
LOCAL_ID = {'type': 'string', 'pattern': r'^t[1-9][0-9]*$'}
THREAD_SCHEMA = study.obj({'id': LOCAL_ID, 'name': study.STRING, 'scope': study.STRING})
MATCH_SCHEMA = study.obj({'id': LOCAL_ID, 'target_thread_id': study.STRING, 'reason': study.STRING})


def extraction_schema():
    result = base.extraction_schema(False)
    result['required'].append('threads')
    result['properties']['threads'] = {'type': 'array', 'items': THREAD_SCHEMA}
    candidate = result['properties']['candidates']['items']
    candidate['required'].append('thread_ids')
    candidate['properties']['thread_ids'] = {'type': 'array', 'items': LOCAL_ID, 'minItems': 1}
    return result


def matching_schema():
    result = base.matching_schema(False)
    result['required'].append('thread_matches')
    result['properties']['thread_matches'] = {'type': 'array', 'items': MATCH_SCHEMA}
    return result


def open_db(path):
    conn = store.open_db(str(path))
    conn.execute('pragma foreign_keys=on')
    conn.executescript('''
        create table if not exists threads (
            thread_id text primary key, name text not null, scope text not null,
            seq integer not null, input_id text not null);
        create table if not exists thread_members (
            thread_id text not null references threads(thread_id),
            view_id text not null references views(view_id), seq integer not null, input_id text not null,
            primary key(thread_id, view_id));
        create virtual table if not exists thread_search using fts5(thread_id UNINDEXED, name, scope);
        create table if not exists ingestion_events (
            seq integer primary key, input_id text unique, result_json text not null);
    ''')
    conn.commit()
    return conn


def validate_extraction(raw):
    errors = study.model.check_schema(raw, extraction_schema())
    if errors:
        raise ValueError('Extraction shape: ' + '; '.join(errors))
    ids = [t['id'] for t in raw['threads']]
    if any(re.fullmatch(LOCAL_ID['pattern'], ident) is None for ident in ids):
        raise ValueError('Local thread IDs must use t followed by a positive integer')
    if len(ids) != len(set(ids)) or any(not t['name'].strip() or not t['scope'].strip() for t in raw['threads']):
        raise ValueError('Threads need unique IDs, names and scope')
    used = set()
    for candidate in raw['candidates']:
        refs = candidate['thread_ids']
        if not refs or len(refs) != len(set(refs)) or set(refs) - set(ids):
            raise ValueError('Each candidate needs nonempty, unique local thread references')
        used.update(refs)
    if set(ids) != used:
        raise ValueError('Every local thread must be used by a candidate')


def thread_context(conn, view_id):
    return [dict(r) for r in conn.execute('''select t.thread_id,t.name,t.scope from threads t
        join thread_members m on m.thread_id=t.thread_id where m.view_id=? order by t.seq,t.rowid''', (view_id,))]


def search_threads(conn, thread, top_n):
    words = sorted(set(re.findall(r'[a-z0-9]{3,}', (thread['name'] + ' ' + thread['scope']).lower())))
    if not words:
        return []
    query = ' OR '.join('"' + word + '"' for word in words)
    return [dict(r) for r in conn.execute('''select thread_id,name,scope from thread_search
        where thread_search match ? order by bm25(thread_search),rowid limit ?''', (query, top_n))]


def resolve_threads(answer, threads, candidates):
    """Resolve all local aliases before writing; only searched global IDs are eligible."""
    errors = study.model.check_schema(answer, matching_schema())
    if errors:
        raise ValueError('Matching shape: ' + '; '.join(errors))
    values = answer['thread_matches']
    ids = {t['id'] for t in threads}
    if len(values) != len(ids) or {v['id'] for v in values} != ids:
        raise ValueError('Every retained thread needs exactly one identity decision')
    targets = {}
    for value in values:
        source, target = value['id'], value['target_thread_id']
        if not value['reason'].strip():
            raise ValueError('Thread identity decision needs a reason')
        if target and target not in ids and target not in {c['thread_id'] for c in candidates[source]}:
            raise ValueError('Thread target was not offered')
        targets[source] = target
    resolved = {}

    def visit(ident, visiting):
        if ident in resolved:
            return resolved[ident]
        if ident in visiting:
            raise ValueError('Thread identity references form a cycle')
        target = targets[ident]
        root = ident if not target else visit(target, visiting | {ident}) if target in ids else target
        resolved[ident] = root
        return root

    for ident in targets:
        visit(ident, set())
    return resolved


def write_threads(conn, threads, roots, handover, checked, written, seq, item):
    """Preserve candidate attachments after original thesis identities resolve; no commit here."""
    definitions = {t['id']: t for t in threads}
    bindings = []
    for candidate in handover.candidates:
        cid = candidate['id']
        if cid in written.new_views:
            vid = written.new_views[cid]
        elif cid in checked.outcomes and checked.outcomes[cid][0] == matching.OUTCOMES[0]:
            vid = checked.outcomes[cid][1]
        else:
            continue
        for tid in candidate['thread_ids']:
            bindings.append((cid, vid, roots[tid]))
    canonical, affected, records = {}, set(), []
    for _, _, root in bindings:
        if root in canonical:
            continue
        if root in definitions:
            thread = definitions[root]
            gid = writing._next_id(conn, 'threads', 'thread_id', 'g')
            conn.execute('insert into threads values (?,?,?,?,?)',
                         (gid, thread['name'], thread['scope'], seq, item['input_id']))
            conn.execute('insert into thread_search values (?,?,?)', (gid, thread['name'], thread['scope']))
            canonical[root] = gid
        else:
            canonical[root] = root
    for cid, vid, root in bindings:
        gid = canonical[root]
        inserted = conn.execute('insert or ignore into thread_members values (?,?,?,?)',
                                (gid, vid, seq, item['input_id']))
        if inserted.rowcount:
            affected.add(gid)
        records.append({'candidate_id': cid, 'view_id': vid, 'thread_id': gid, 'new_membership': bool(inserted.rowcount)})
    if written.changed_views:
        marks = ','.join('?' for _ in written.changed_views)
        affected.update(r[0] for r in conn.execute(
            f'select distinct thread_id from thread_members where view_id in ({marks})', sorted(written.changed_views)))
    return records, sorted(affected)


def thread_detail(conn, thread_id, seq):
    """Read dated evidence only through the ledger's actual member-to-evidence links."""
    row = conn.execute('select * from threads where thread_id=? and seq<=?', (thread_id, seq)).fetchone()
    if row is None:
        return None
    members = []
    for member in conn.execute('''select v.view_id,v.question,m.seq,m.input_id from thread_members m
            join views v on v.view_id=m.view_id where m.thread_id=? and m.seq<=? order by m.seq,m.rowid''', (thread_id, seq)):
        evidence = [dict(e) for e in conn.execute('''select distinct e.evidence_id,e.quote,e.original_day
            from evidence_links l join evidence e on e.evidence_id=l.evidence_id
            where l.view_id=? and l.seq<=? and e.created_seq<=?
            and not exists(select 1 from replacements r where r.old_evidence_id=e.evidence_id and r.seq<=?)
            order by e.created_seq,e.rowid''', (member['view_id'], seq, seq, seq))]
        members.append(dict(member) | {'evidence': evidence})
    return dict(row) | {'members': members}


def process(conn, calls, uni, item, index):
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'input_id': item['input_id'], 'route': route.kind}
    seq = route.sequence_no
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    payload = {'article': {k: item[k] for k in ['input_id', 'title', 'publication_day', 'category', 'text']},
               'objects': [dict(id=k, kind=uni.kind(k)) for k in list(uni.companies) + list(uni.themes)],
               'fiscal_context': [uni.fiscal_note(o['value'], item['publication_day']) for o in item['object_identifiers']],
               'existing_theses': [{k: v[k] for k in ['view_id', 'object_id', 'question', 'looks_at', 'due_day']} |
                                    {'threads': thread_context(conn, v['view_id'])} for v in shown]}
    raw = calls.stage(f'item{index}-extract', base.EXTRACT_PROMPT + EXTRACT_THREADS, payload,
                      extraction_schema(), calls.cfg.extraction_setting(item['category']))
    validate_extraction(raw)
    handover = base.sift(raw, item, shown)
    used = {tid for c in handover.candidates for tid in c['thread_ids']}
    threads = [t for t in raw['threads'] if t['id'] in used]
    candidates = {t['id']: search_threads(conn, t, calls.cfg.search_top_n) for t in threads}
    lists = matching.build_lists(conn, handover, shown, calls.cfg.search_top_n)
    payload = base.match_payload(conn, item, handover, lists, shown, None, [])
    payload.update(threads=threads, thread_candidates=candidates)
    answer = calls.stage(f'item{index}-match', base.MATCH_PROMPT + MATCH_THREADS, payload,
                         matching_schema(), calls.cfg.matching)
    roots = resolve_threads(answer, threads, candidates)
    checked = base.check_matching(conn, uni, answer, handover, lists, shown)
    if checked.refusals:
        raise ValueError('Original matching checks: ' + '; '.join(checked.refusals))
    pending = [(e, checked.outcomes[link][1]) for e in handover.evidence for link in e['links']
               if link in checked.outcomes and checked.outcomes[link][0] == matching.OUTCOMES[0]]
    second = {}
    if pending:
        unique = {e['id']: e for e, _ in pending}
        second_handover = dataclasses.replace(handover, candidates=[], evidence=list(unique.values()))
        lists2 = matching.Lists({}, {(e['id'], vid): matching.rank_evidence(conn, vid, e['one_line'], calls.cfg.search_top_n) for e, vid in pending})
        payload = base.match_payload(conn, item, second_handover, lists2, [], None, [])
        raw2 = calls.stage(f'item{index}-match-evidence', base.MATCH_PROMPT, payload,
                           base.matching_schema(False), calls.cfg.matching)
        check2 = base.check_matching(conn, uni, raw2, second_handover, lists2, [])
        if check2.refusals:
            raise ValueError('Second matching checks: ' + '; '.join(check2.refusals))
        second = check2.evidence
    handover.candidates.sort(key=lambda c: c['kind'] != 'theme')
    written = writing.write(conn, uni, seq, item, handover, checked, second)
    bindings, affected = write_threads(conn, threads, roots, handover, checked, written, seq, item)
    result = {'input_id': item['input_id'], 'seq': seq, 'route': 'written', 'new_views': written.new_views,
              'changed_views': sorted(written.changed_views), 'affected_threads': affected,
              'bindings': bindings, 'dropped': handover.dropped, 'thread_roots': roots,
              'thread_candidates': candidates,
              'threads': [dict(r) for r in conn.execute('select * from threads')],
              'memberships': [dict(r) for r in conn.execute('select * from thread_members')],
              'views': [base.view_record(conn, r[0]) for r in conn.execute('select view_id from views')],
              'details': [thread_detail(conn, r[0], seq) for r in conn.execute('select thread_id from threads')]}
    conn.execute('insert into ingestion_events values (?,?,?)', (seq, item['input_id'], json.dumps(result)))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': result['changed_views'], 'threads': affected}))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result


class Calls(base.Calls):
    def __init__(self, out, label):
        super().__init__(out, label)
        self.cfg = dataclasses.replace(self.cfg, version='ingestion-threads-v1')


def fingerprints():
    paths = [Path(__file__), Path(base.__file__), Path(control.__file__),
             study.ROOT / 'src/hivemind/extraction.py', study.ROOT / 'src/hivemind/views/matching.py',
             study.ROOT / 'src/hivemind/views/writing.py', study.ROOT / 'poc/universe.json']
    return {str(p.relative_to(study.ROOT)): study.digest(p) for p in paths}


def prepare(out):
    base.prepare(out)
    conn = study.read_only(base.CORPUS)
    item = dict(conn.execute('select * from items where input_id=?', (EXTRA_ITEM,)).fetchone())
    conn.close()
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    study.write_json(out / 'extra-item.json', item)
    path = out / 'manifest.json'
    manifest = json.loads(path.read_text())
    manifest.update(code_sha256=study.digest(__file__), dependencies=fingerprints(), extra_sha256=study.digest(out / 'extra-item.json'),
                    version='ingestion-threads-v1', control='D143', max_calls=48, max_estimated_usd=8)
    study.write_json(path, manifest)


def verify(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['dependencies'] != fingerprints() or manifest['sealed_sha256'] != study.digest(base.SEALED)
            or manifest['corpus_sha256'] != study.digest(base.CORPUS)
            or manifest['items_sha256'] != study.digest(out / 'items.json')
            or manifest['extra_sha256'] != study.digest(out / 'extra-item.json')
            or manifest['config_checksum'] != study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum):
        raise ValueError('Frozen experiment changed')


def run(out, extra=False):
    verify(out)
    if extra:
        review = json.loads((out / 'core-review.json').read_text())
        if review.get('reviewed_by') != 'assistant' or review.get('core_semantics_passed') is not True:
            raise ValueError('Extra article requires the predefined successful core review')
        events = [(4, json.loads((out / 'extra-item.json').read_text()))]
    else:
        events = list(enumerate(json.loads((out / 'items.json').read_text()), 1))
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        streams = []
        for sample in [1, 2, 3]:
            arms = ['threads'] if extra else ['control', 'threads'] if sample != 2 else ['threads', 'control']
            for arm in arms:
                label = f'{sample}-{arm}'
                calls = Calls(out, label)
                conn = (open_db if arm == 'threads' else control.open_db)(out / f'sample-{label}' / 'views.sqlite')
                streams.append((label, arm, calls, conn))
        stop = False
        for index, item in events:
            for label, arm, calls, conn in streams:
                failed = out / f'sample-{label}' / ('extra-failed.json' if extra else 'failed.json')
                if failed.exists() or store.is_processed(conn, item['input_id']):
                    continue
                try:
                    result = (process if arm == 'threads' else control.process)(conn, calls, uni, item, index)
                    study.write_json(out / f'sample-{label}' / f'item{index}-result.json', result)
                    print(f'WRITTEN {label} item={index} new_views={len(result.get("new_views", {}))}', flush=True)
                except Exception as error:
                    conn.rollback()
                    study.write_json(failed, {'item_index': index, 'error': type(error).__name__ + ': ' + str(error)[:1000]})
                    print(f'FAILED {label} item={index}: {error}', flush=True)
                    if 'budget' in str(error).lower():
                        stop = True
                        break
            if stop:
                break
        last_item = events[-1][1]
        for label, arm, calls, conn in streams:
            if store.is_processed(conn, last_item['input_id']):
                route = dispatch.route(conn, last_item, uni)
                study.write_json(out / f'sample-{label}' / ('extra-resend.json' if extra else 'resend.json'),
                                 {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    base.report(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'core', 'extra', 'report'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    path = args.out.resolve()
    if args.command == 'prepare':
        prepare(path)
    elif args.command == 'report':
        base.report(path)
    else:
        run(path, args.command == 'extra')
