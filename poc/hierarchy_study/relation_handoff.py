"""D143: preserve extraction-owned associations through the real ingestion writer."""
import argparse
import copy
import dataclasses
import fcntl
import json
from pathlib import Path

import ingestion_groups as base
import study
from hivemind import dispatch, extraction, universe
from hivemind.views import matching, store, writing

ASSOCIATION_PROMPT = """ Organize distinct theses around shared business questions while reading this article.
Return associations only when this article provides a reason to connect their outcomes. A shared company alone
is insufficient. Each association names its members, this article's supporting evidence IDs, and why they belong
together. Reuse a shown group's ID when it already asks that shared question (leave question empty); otherwise
leave group_id empty and write the broader question. A new group needs at least two distinct theses. A lone thesis
stays independent. Members may be shown theses or candidates from this answer. Grouping is not thesis identity
or causal dependency. Do not copy each atomic question into a group. Existing group descriptions are navigation
context, not evidence. Do not invent an association when the article supplies no connection."""
ASSOCIATION_SCHEMA = study.obj({
    'group_id': study.STRING, 'question': study.STRING, 'member_ids': study.STRINGS,
    'evidence_ids': study.STRINGS, 'reason': study.STRING,
})


def schema():
    result = base.extraction_schema(False)
    result['required'].append('associations')
    result['properties']['associations'] = {'type': 'array', 'items': ASSOCIATION_SCHEMA}
    return result


def open_db(path):
    conn = base.open_experiment_db(path)
    conn.executescript('''
        create table if not exists associations (
            id integer primary key, group_id text not null references research_groups(group_id),
            reason text not null, seq integer not null, input_id text not null);
        create table if not exists association_members (
            association_id integer references associations(id), view_id text references views(view_id),
            primary key(association_id, view_id));
        create table if not exists association_evidence (
            association_id integer references associations(id), evidence_id text references evidence(evidence_id),
            primary key(association_id, evidence_id));
    ''')
    conn.commit()
    return conn


def prepare_associations(raw, handover, shown, groups):
    """Validate raw references and preserve aliases to surviving, normalized quotes."""
    errors = study.model.check_schema(raw.get('associations'), {'type': 'array', 'items': ASSOCIATION_SCHEMA})
    if errors:
        raise ValueError('Association shape: ' + '; '.join(errors))
    visible = {v['view_id'] for v in shown}
    candidates = {c['id'] for c in raw['candidates']}
    kept = {c['id'] for c in handover.candidates}
    evidence = {e['id']: e for e in raw['evidence']}
    accepted = {extraction.normalise(e['quote']): e['id'] for e in handover.evidence}
    # Use the original check's surviving quotes and links, not its human-readable drop reasons.
    aliases = {e['id']: accepted[extraction.normalise(e['quote'])] for e in raw['evidence']
               if extraction.normalise(e['quote']) in accepted and set(e['links']) & (visible | kept)}
    prepared = []
    for index, association in enumerate(raw['associations']):
        a = copy.deepcopy(association)
        members, sources = set(a['member_ids']), set(a['evidence_ids'])
        if (not members or not sources or not a['reason'].strip()
                or len(members) != len(a['member_ids']) or len(sources) != len(a['evidence_ids'])
                or members - (visible | candidates) or sources - evidence.keys()
                or a['group_id'] not in {g['group_id'] for g in groups} | {''}
                or (bool(a['group_id']) == bool(a['question'].strip()))):
            raise ValueError(f'Invalid association references at {index}')
        a['index'], a['skip_reason'] = index, ''
        if members - (visible | kept):
            a['skip_reason'] = 'member rejected by extraction'
        elif sources - aliases.keys():
            a['skip_reason'] = 'evidence rejected by extraction'
        elif not any(members & set(evidence[e]['links']) for e in sources):
            raise ValueError(f'Association {index} has no evidence linked to a member')
        else:
            a['evidence_ids'] = list(dict.fromkeys(aliases[e] for e in a['evidence_ids']))
        prepared.append(a)
    return prepared


def write_associations(conn, proposals, checked, written, seq, item):
    """Save associations after identities resolve; caller owns the entire transaction."""
    outcomes, affected = [], set()
    for proposal in proposals:
        members, reason = [], proposal['skip_reason']
        for ident in proposal['member_ids']:
            if ident in written.new_views:
                members.append(written.new_views[ident])
            elif ident in checked.outcomes:
                outcome, target, _ = checked.outcomes[ident]
                if outcome == matching.OUTCOMES[0]:
                    members.append(target)
                else:
                    reason = reason or 'member discarded by matching'
            elif store.view(conn, ident):
                members.append(ident)
            else:
                reason = reason or 'member rejected by extraction'
        members = list(dict.fromkeys(members))
        sources = [written.evidence_ids.get(e) for e in proposal['evidence_ids']]
        if not reason and any(e is None for e in sources):
            reason = 'evidence not persisted by original writer'
        if not reason and not proposal['group_id'] and len(members) < 2:
            reason = 'fewer than two distinct resolved theses'
        if not reason and not any(set(store.views_linked_to(conn, e)) & set(members) for e in sources):
            reason = 'persisted evidence has no member destination'
        if reason:
            outcomes.append({'index': proposal['index'], 'status': 'skipped', 'reason': reason})
            continue
        gid = proposal['group_id']
        if not gid:
            gid = writing._next_id(conn, 'research_groups', 'group_id', 'g')
            conn.execute('insert into research_groups values (?,?,?,?,?,?)',
                         (gid, proposal['question'], proposal['question'], '', seq, item['input_id']))
        for vid in members:
            inserted = conn.execute('insert or ignore into group_members values (?,?,?,?,?)',
                                    (gid, vid, proposal['reason'], seq, item['input_id']))
            if inserted.rowcount:
                affected.add(gid)
        record = conn.execute('insert into associations(group_id,reason,seq,input_id) values (?,?,?,?)',
                              (gid, proposal['reason'], seq, item['input_id'])).lastrowid
        conn.executemany('insert into association_members values (?,?)', [(record, v) for v in members])
        conn.executemany('insert into association_evidence values (?,?)', [(record, e) for e in dict.fromkeys(sources)])
        outcomes.append({'index': proposal['index'], 'status': 'written', 'group_id': gid,
                         'members': members, 'evidence_ids': list(dict.fromkeys(sources))})
    if written.changed_views:
        marks = ','.join('?' for _ in written.changed_views)
        affected.update(r[0] for r in conn.execute(
            f'select distinct group_id from group_members where view_id in ({marks})', sorted(written.changed_views)))
    return outcomes, sorted(affected)


def process(conn, calls, uni, item, index):
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'input_id': item['input_id'], 'route': route.kind}
    seq = route.sequence_no
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    groups = base.visible_groups(conn, {v['view_id'] for v in shown})
    payload = {'article': {k: item[k] for k in ['input_id', 'title', 'publication_day', 'category', 'text']},
               'objects': [dict(id=k, kind=uni.kind(k)) for k in list(uni.companies) + list(uni.themes)],
               'fiscal_context': [uni.fiscal_note(o['value'], item['publication_day']) for o in item['object_identifiers']],
               'existing_theses': [{k: v[k] for k in ['view_id', 'object_id', 'question', 'looks_at', 'due_day']} for v in shown],
               'groups': groups}
    raw = calls.stage(f'item{index}-extract', base.EXTRACT_PROMPT + ASSOCIATION_PROMPT, payload,
                      schema(), calls.cfg.extraction_setting(item['category']))
    handover = base.sift(raw, item, shown)
    proposals = prepare_associations(raw, handover, shown, groups)
    lists = matching.build_lists(conn, handover, shown, calls.cfg.search_top_n)
    payload = base.match_payload(conn, item, handover, lists, shown, None, [])
    answer = calls.stage(f'item{index}-match', base.MATCH_PROMPT, payload,
                         base.matching_schema(False), calls.cfg.matching)
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
    decisions, affected = write_associations(conn, proposals, checked, written, seq, item)
    result = {'input_id': item['input_id'], 'seq': seq, 'route': 'written', 'new_views': written.new_views,
              'changed_views': sorted(written.changed_views), 'affected_groups': affected,
              'association_decisions': decisions, 'evidence_ids': written.evidence_ids, 'dropped': handover.dropped,
              'shown_views': [v['view_id'] for v in shown], 'shown_groups': groups,
              'groups': [dict(r) for r in conn.execute('select * from research_groups')],
              'members': [dict(r) for r in conn.execute('select * from group_members')],
              'views': [base.view_record(conn, r[0]) for r in conn.execute('select view_id from views')],
              'evidence_count': conn.execute('select count(*) from evidence').fetchone()[0]}
    conn.execute('insert into ingestion_events values (?,?,?)', (seq, item['input_id'], json.dumps(result)))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': result['changed_views'], 'groups': affected}))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result


def prepare(out):
    base.prepare(out)
    path = out / 'manifest.json'
    manifest = json.loads(path.read_text())
    manifest['code_sha256'] = study.digest(__file__)
    manifest['base_code_sha256'] = study.digest(base.__file__)
    manifest['contract'] = 'D143 extraction-owned associations; fresh D142 control'
    study.write_json(path, manifest)


def run(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['code_sha256'] != study.digest(__file__) or manifest['base_code_sha256'] != study.digest(base.__file__)
            or manifest['sealed_sha256'] != study.digest(base.SEALED) or manifest['corpus_sha256'] != study.digest(base.CORPUS)
            or manifest['items_sha256'] != study.digest(out / 'items.json')
            or manifest['config_checksum'] != study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum):
        raise ValueError('Frozen experiment changed')
    items = json.loads((out / 'items.json').read_text())
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        streams = []
        for sample in [1, 2, 3]:
            for arm in (['control', 'handoff'] if sample != 2 else ['handoff', 'control']):
                label = f'{sample}-{arm}'
                calls = base.Calls(out, label)
                conn = open_db(out / f'sample-{label}' / 'views.sqlite')
                streams.append((label, arm, calls, conn))
        stop = False
        for index, item in enumerate(items, 1):
            for label, arm, calls, conn in streams:
                failed = out / f'sample-{label}' / 'failed.json'
                if failed.exists() or store.is_processed(conn, item['input_id']):
                    continue
                try:
                    result = (process(conn, calls, uni, item, index) if arm == 'handoff'
                              else base.process(conn, calls, uni, item, index, True))
                    study.write_json(out / f'sample-{label}' / f'item{index}-result.json', result)
                    print(f'WRITTEN {label} item={index} groups={len(result.get("groups", []))}', flush=True)
                except Exception as error:
                    conn.rollback()
                    study.write_json(failed, {'item_index': index, 'error': type(error).__name__ + ': ' + str(error)[:1000]})
                    print(f'FAILED {label} item={index}: {error}', flush=True)
                    if 'budget' in str(error).lower():
                        stop = True
                        break
            if stop:
                break
        for label, arm, calls, conn in streams:
            if store.is_processed(conn, items[-1]['input_id']):
                route = dispatch.route(conn, items[-1], uni)
                study.write_json(out / f'sample-{label}' / 'resend.json', {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    base.report(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run', 'report'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    {'prepare': prepare, 'run': run, 'report': base.report}[args.command](args.out.resolve())
