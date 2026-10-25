"""Isolated organization during the existing extraction, matching and writing path."""
from __future__ import annotations

import argparse
import copy
import dataclasses
import fcntl
import json
from pathlib import Path
import sqlite3

import study
from hivemind import dispatch, extraction, universe, vocabulary
from hivemind.views import matching, store, writing

CORPUS = study.ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'
SEALED = study.ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'
ITEM_IDS = [
    'truenorth:transcript:NVDA:2026-02-25',
    'nvidianews:sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory',
    'gnews:9b084fc0f1583da0df01c45c',
]
KINDS = ['company', 'theme']
TIERS = ['fact', 'party_statement', 'third_party_view', 'rumor']
LABELS = ['strongly_bullish', 'bullish', 'neutral', 'bearish', 'strongly_bearish']
OUTCOMES = ['existing', 'successor', 'new', 'discard']
EVIDENCE_OUTCOMES = ['duplicate', 'replace', 'new']
EXTRACT_PROMPT = """Read the entire supplied article as a financial-research analyst. Extract evidence attached to
the shown existing theses; propose new theses only for distinct questions not already covered. Keep each thesis
to one measurable number or dated event. Propose the company's annual total and largest-segment revenue questions,
annual figures with explicit company guidance, and dated unresolved product, regulatory or transaction milestones.
Quarterly numbers and quarterly guidance are evidence, not separate theses. Do not open questions beyond next year,
routine corporate administration, undated broad strategies or questions whose thresholds cannot yet be specified.
Use the article's publication date and supplied fiscal context. Company operating questions have kind company;
world/industry outcomes have kind theme. Numeric questions have five exhaustive non-overlapping bands, with company
labels ordered strongly_bullish, bullish, neutral, bearish, strongly_bearish. Binary questions use yes/no. Due dates
are when the result becomes knowable. Give each candidate its own evidence IDs. Do not duplicate an existing question.
Copy evidence quotes exactly from this article, and link each only to the question it directly bears on. Distinguish
facts, party statements, third-party views and rumors. Do not treat plans as completed events. No outside knowledge.
Write all prose in English; preserve the original quote."""
EXTRACT_GROUPS = """ Also propose concise relationship hints for new candidates when the article connects them to
shown theses or a shared business question. Existing group descriptions are navigation context, not evidence.
Use related_view_ids only for existing_theses IDs and group_id only for a shown group (otherwise empty).
Use broader_question for a proposed shared question. Hints do not merge theses or create dependencies."""
MATCH_PROMPT = """Place the supplied candidate theses and evidence using only the supplied lists.
For each candidate choose existing (same object, outcome and period, including a part of that question), successor
(next period of the same question), new (a distinct question), or discard (unsupported object, closed same-period
question, or an excessively broad combination). Similar business context alone does not make two questions identical.
For new/successor theses, choose dependencies only when the outcome requires another shown thesis's outcome.
Use shown thesis IDs or candidates retained in this answer; avoid cycles. Dependency direction states which end
supports the candidate, or whether two theme ladders move together. An observed fact is evidence, not a dependency.
For every supplied evidence/view pair choose duplicate, replace or new. Duplicate means the same original speaker,
date and statement, even across media. Replace means a later revision of the same statement by the original source;
new covers different events, periods or speakers. Targets must come from that pair's provided evidence list.
Use empty strings for absent targets. Answer every candidate and listed evidence pair. English prose only."""
MATCH_GROUPS = """ In this same decision, organize retained and shown theses around ongoing business questions.
Use existing groups when their question and scope fit; create a new group only for a distinct coherent business
argument. A group is not a company folder, a duplicate thesis, or a causal dependency. Keep different measurable
questions separate even when they share a group. You may attach shown older theses to a new group and a thesis may
belong to multiple justified groups. Do not force unrelated theses together. Use new_ prefixes for temporary new
group IDs. Each new group needs at least one retained member. Explain each membership from the supplied material.
Extraction hints are proposals, not instructions; resolve them against the current matching context."""


def translate_controls(data, reverse=False):
    """Adapt this study's protocol enums to the pipeline's canonical vocabulary in memory (D163: the sift reads and returns
    canonical values; its legacy Chinese spellings are also accepted on the way back); never translate article text or
    generated prose."""
    value = copy.deepcopy(data)
    maps = [(KINDS, vocabulary.KINDS, list(vocabulary.LEGACY['kind'])), (TIERS, vocabulary.TIERS, list(vocabulary.LEGACY['tier'])),
            (LABELS, vocabulary.ASSET_LABELS, list(vocabulary.LEGACY['label'])[:5])]
    tables = [dict(zip(canonical, ours)) | dict(zip(legacy, ours)) if reverse else dict(zip(ours, canonical)) for ours, canonical, legacy in maps]
    for candidate in value.get('candidates', []):
        candidate['kind'] = tables[0].get(candidate['kind'], candidate['kind'])
        for rung in candidate['rungs']:
            rung['label'] = tables[2].get(rung['label'], rung['label'])
    for evidence in value.get('evidence', []):
        evidence['tier'] = tables[1].get(evidence['tier'], evidence['tier'])
    return value


def sift(answer, item, shown):
    legacy = translate_controls(answer)
    evidence, candidates, dropped = extraction.sift(legacy, item, item['text'], {v['view_id'] for v in shown})
    restored = translate_controls({'evidence': evidence, 'candidates': candidates}, reverse=True)
    return extraction.Handover(restored['evidence'], restored['candidates'], dropped, 0, '', False, 0)


def extraction_schema(grouped):
    schema = copy.deepcopy(extraction.SCHEMA)
    schema['properties']['evidence']['items']['properties']['tier']['enum'] = TIERS
    schema['properties']['candidates']['items']['properties']['kind']['enum'] = KINDS
    if grouped:
        schema['required'].append('relationship_hints')
        schema['properties']['relationship_hints'] = {'type': 'array', 'items': study.obj({
            'candidate_id': study.STRING, 'related_view_ids': study.STRINGS,
            'group_id': study.STRING, 'broader_question': study.STRING, 'reason': study.STRING})}
    return schema


def matching_schema(grouped):
    schema = copy.deepcopy(matching.SCHEMA)
    schema['properties']['candidates']['items']['properties']['outcome']['enum'] = OUTCOMES
    schema['properties']['evidence']['items']['properties']['outcome']['enum'] = EVIDENCE_OUTCOMES
    if grouped:
        schema['required'] += ['new_groups', 'memberships']
        schema['properties']['new_groups'] = {'type': 'array', 'items': study.obj({
            'id': study.STRING, 'title': study.STRING, 'question': study.STRING, 'scope': study.STRING})}
        schema['properties']['memberships'] = {'type': 'array', 'items': study.obj({
            'thesis_id': study.STRING, 'group_id': study.STRING, 'reason': study.STRING})}
    return schema


def check_matching(conn, uni, answer, handover, lists, shown):
    raw = copy.deepcopy(answer)
    for candidate in raw['candidates']:
        candidate['outcome'] = dict(zip(OUTCOMES, matching.OUTCOMES))[candidate['outcome']]
    for evidence in raw['evidence']:
        evidence['outcome'] = dict(zip(EVIDENCE_OUTCOMES, matching.EVIDENCE_OUTCOMES))[evidence['outcome']]
    legacy = translate_controls({'candidates': handover.candidates, 'evidence': handover.evidence})
    return matching.check(conn, uni, raw, legacy['candidates'], legacy['evidence'], lists, shown)


def open_experiment_db(path):
    conn = store.open_db(str(path))
    conn.execute('pragma foreign_keys=on')
    conn.executescript('''
        create table if not exists research_groups (
            group_id text primary key, title text, question text, scope text, seq integer, input_id text);
        create table if not exists group_members (
            group_id text references research_groups(group_id), view_id text references views(view_id),
            reason text, seq integer, input_id text, primary key(group_id,view_id));
        create table if not exists ingestion_events (
            seq integer primary key, input_id text unique, result_json text);
    ''')
    conn.commit()
    return conn


def visible_groups(conn, ids):
    if not ids:
        return []
    marks = ','.join('?' for _ in ids)
    groups = conn.execute(f'''select distinct g.* from research_groups g join group_members m
                            on m.group_id=g.group_id where m.view_id in ({marks}) order by g.seq,g.group_id''', sorted(ids)).fetchall()
    return [dict(dict(g), members=[r[0] for r in conn.execute('select view_id from group_members where group_id=? order by view_id', (g['group_id'],))]) for g in groups]


def view_record(conn, ident):
    row = store.view(conn, ident)
    return {k: row[k] for k in ['view_id', 'object_id', 'kind', 'looks_at', 'question', 'due_day', 'year']} | {'rungs': store.rungs_of(conn, ident)}


def match_payload(conn, item, handover, lists, shown, groups, hints):
    ids = {v['view_id'] for v in shown}
    ids.update(v for hits in lists.candidate_lists.values() for v in hits)
    ids.update(vid for _, vid in lists.evidence_lists)
    return {'item': {k: item[k] for k in ['input_id', 'publication_day', 'category']},
            'candidates': handover.candidates, 'candidate_lists': lists.candidate_lists,
            'shown_views': [view_record(conn, ident) for ident in sorted(ids)],
            'evidence': handover.evidence,
            'evidence_pairs': [{'evidence_id': eid, 'view_id': vid,
                                'existing_evidence': [store.evidence(conn, x) for x in values]}
                               for (eid, vid), values in lists.evidence_lists.items()],
            **({'groups': groups, 'relationship_hints': hints} if groups is not None else {})}


def check_groups(answer, checked, visible_ids, groups):
    existing = {g['group_id'] for g in groups}
    new = [g['id'] for g in answer['new_groups']]
    if len(set(new)) != len(new) or any(not ident.startswith('new_') or ident in existing for ident in new):
        raise ValueError('New group IDs must be unique temporary IDs')
    kept = {cid for cid, (outcome, _, _) in checked.outcomes.items() if outcome != matching.OUTCOMES[3]}
    seen = set()
    for membership in answer['memberships']:
        pair = (membership['thesis_id'], membership['group_id'])
        if pair in seen or pair[0] not in visible_ids | kept or pair[1] not in existing | set(new) or not membership['reason'].strip():
            raise ValueError('Invalid group membership reference')
        seen.add(pair)
    if any(g not in {m['group_id'] for m in answer['memberships']} for g in new):
        raise ValueError('New group has no retained member')
    if any(not all(g[k].strip() for k in ['title', 'question', 'scope']) for g in answer['new_groups']):
        raise ValueError('Group needs a title, question and scope')


def write_groups(conn, answer, checked, written, seq, item):
    resolved = {}
    for group in answer['new_groups']:
        ident = writing._next_id(conn, 'research_groups', 'group_id', 'g')
        conn.execute('insert into research_groups values (?,?,?,?,?,?)',
                     (ident, group['title'], group['question'], group['scope'], seq, item['input_id']))
        resolved[group['id']] = ident
    affected = set()
    for member in answer['memberships']:
        ident = member['thesis_id']
        if ident in written.new_views:
            ident = written.new_views[ident]
        elif ident in checked.outcomes:
            outcome, target, _ = checked.outcomes[ident]
            if outcome != matching.OUTCOMES[0]:
                raise ValueError('Unresolved candidate membership')
            ident = target
        group_id = resolved.get(member['group_id'], member['group_id'])
        inserted = conn.execute('insert or ignore into group_members values (?,?,?,?,?)',
                                (group_id, ident, member['reason'], seq, item['input_id']))
        if inserted.rowcount:
            affected.add(group_id)
    changed = sorted(written.changed_views)
    if changed:
        marks = ','.join('?' for _ in changed)
        affected.update(r[0] for r in conn.execute(f'select distinct group_id from group_members where view_id in ({marks})', changed))
    return sorted(affected)


def resolve_hints(hints, checked, written, visible_ids):
    """Diagnostic projection of existing extraction relationships after thesis identities are resolved."""
    relations = []
    for hint in hints:
        candidate = hint['candidate_id']
        if candidate in written.new_views:
            source = written.new_views[candidate]
        elif candidate in checked.outcomes and checked.outcomes[candidate][0] == matching.OUTCOMES[0]:
            source = checked.outcomes[candidate][1]
        else:
            continue
        for target in hint['related_view_ids']:
            if target not in visible_ids:
                raise ValueError('Relationship target was not visible at extraction')
            if source != target:
                relations.append({'source': source, 'target': target, 'question': hint['broader_question'], 'reason': hint['reason']})
    return relations


class Calls(study.Calls):
    def __init__(self, out, label):
        super().__init__(out, label)
        self.cfg = dataclasses.replace(self.cfg, version='ingestion-groups-v1')

    def stage(self, name, prompt, payload, schema, setting):
        self.setting = setting
        path = self.out / f'sample-{self.sample}' / f'{name}.json'
        if path.exists():
            expected = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False), schema, 'hierarchy_result', self.cfg.provider)
            if json.loads(path.read_text())['request'] != expected:
                raise ValueError('Request changed; do not reuse this run')
        return self.call(name, prompt, payload, schema)


def process(conn, calls, uni, item, index, grouped):
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'input_id': item['input_id'], 'route': route.kind}
    seq = route.sequence_no
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    groups = visible_groups(conn, {v['view_id'] for v in shown}) if grouped else None
    payload = {'article': {k: item[k] for k in ['input_id', 'title', 'publication_day', 'category', 'text']},
               'objects': [dict(id=k, kind=uni.kind(k)) for k in list(uni.companies) + list(uni.themes)],
               'fiscal_context': [uni.fiscal_note(o['value'], item['publication_day']) for o in item['object_identifiers']],
               'existing_theses': [{k: v[k] for k in ['view_id', 'object_id', 'question', 'looks_at', 'due_day']} for v in shown]}
    if grouped:
        payload['groups'] = groups
    raw = calls.stage(f'item{index}-extract', EXTRACT_PROMPT + (EXTRACT_GROUPS if grouped else ''), payload,
                      extraction_schema(grouped), calls.cfg.extraction_setting(item['category']))
    handover = sift(raw, item, shown)
    kept = {c['id'] for c in handover.candidates}
    hints = [h for h in raw.get('relationship_hints', []) if h['candidate_id'] in kept]
    if any(set(h['related_view_ids']) - {v['view_id'] for v in shown} or
           h['group_id'] not in {g['group_id'] for g in groups} | {''} for h in hints):
        raise ValueError('Extraction hint cites unseen thesis or group')
    lists = matching.build_lists(conn, handover, shown, calls.cfg.search_top_n)
    visible = {v['view_id'] for v in shown} | {v for hits in lists.candidate_lists.values() for v in hits}
    groups = visible_groups(conn, visible) if grouped else None
    payload = match_payload(conn, item, handover, lists, shown, groups, hints)
    answer = calls.stage(f'item{index}-match', MATCH_PROMPT + (MATCH_GROUPS if grouped else ''), payload,
                         matching_schema(grouped), calls.cfg.matching)
    checked = check_matching(conn, uni, answer, handover, lists, shown)
    if checked.refusals:
        raise ValueError('Original matching checks: ' + '; '.join(checked.refusals))
    if grouped:
        check_groups(answer, checked, visible, groups)
    pending = [(e, checked.outcomes[link][1]) for e in handover.evidence for link in e['links']
               if link in checked.outcomes and checked.outcomes[link][0] == matching.OUTCOMES[0]]
    second = {}
    if pending:
        unique = {e['id']: e for e, _ in pending}
        second_handover = dataclasses.replace(handover, candidates=[], evidence=list(unique.values()))
        lists2 = matching.Lists({}, {(e['id'], vid): matching.rank_evidence(conn, vid, e['one_line'], calls.cfg.search_top_n) for e, vid in pending})
        payload = match_payload(conn, item, second_handover, lists2, [], None, [])
        raw2 = calls.stage(f'item{index}-match-evidence', MATCH_PROMPT, payload, matching_schema(False), calls.cfg.matching)
        check2 = check_matching(conn, uni, raw2, second_handover, lists2, [])
        if check2.refusals:
            raise ValueError('Second matching checks: ' + '; '.join(check2.refusals))
        second = check2.evidence
    handover.candidates.sort(key=lambda c: c['kind'] != 'theme')
    written = writing.write(conn, uni, seq, item, handover, checked, second)
    affected = write_groups(conn, answer, checked, written, seq, item) if grouped else []
    result = {'input_id': item['input_id'], 'seq': seq, 'route': 'written', 'new_views': written.new_views,
              'changed_views': sorted(written.changed_views), 'affected_groups': affected, 'dropped': handover.dropped,
              'shown_views': sorted(visible), 'shown_groups': groups,
              'groups': [dict(r) for r in conn.execute('select * from research_groups')],
              'members': [dict(r) for r in conn.execute('select * from group_members')],
              'views': [view_record(conn, r[0]) for r in conn.execute('select view_id from views')],
              'evidence_count': conn.execute('select count(*) from evidence').fetchone()[0]}
    conn.execute('insert into ingestion_events values (?,?,?)', (seq, item['input_id'], json.dumps(result)))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': result['changed_views'], 'groups': affected}))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result


def prepare(out):
    if out.exists():
        raise ValueError('Use a new dated experiment directory')
    conn = study.read_only(CORPUS)
    items = []
    for ident in ITEM_IDS:
        row = conn.execute('select * from items where input_id=?', (ident,)).fetchone()
        if row is None or not row['text']:
            raise ValueError('Missing full article')
        item = dict(row)
        item['object_identifiers'] = json.loads(item['object_identifiers'])
        items.append(item)
    conn.close()
    out.mkdir(parents=True)
    study.write_json(out / 'items.json', items)
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    study.write_json(out / 'manifest.json', {'corpus_sha256': study.digest(CORPUS), 'sealed_sha256': study.digest(SEALED),
        'items_sha256': study.digest(out / 'items.json'), 'code_sha256': study.digest(__file__),
        'config_checksum': study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum,
        'max_calls': 48, 'max_estimated_usd': 8})
    print('Prepared three full articles; no seeded theses or groups.')


def run(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['sealed_sha256'] != study.digest(SEALED) or manifest['corpus_sha256'] != study.digest(CORPUS)
            or manifest['items_sha256'] != study.digest(out / 'items.json') or manifest['code_sha256'] != study.digest(__file__)
            or manifest['config_checksum'] != study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum):
        raise ValueError('Frozen run changed')
    items = json.loads((out / 'items.json').read_text())
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        streams = []
        for sample in [1, 2, 3]:
            for arm in (['control', 'grouped'] if sample != 2 else ['grouped', 'control']):
                label = f'{sample}-{arm}'
                calls = Calls(out, label)
                streams.append((label, arm == 'grouped', calls, open_experiment_db(out / f'sample-{label}' / 'views.sqlite')))
        for index, item in enumerate(items, 1):
            for label, grouped, calls, conn in streams:
                failed = out / f'sample-{label}' / 'failed.json'
                if failed.exists():
                    continue
                row = conn.execute('select result_json from ingestion_events where input_id=?', (item['input_id'],)).fetchone()
                if row:
                    continue
                try:
                    result = process(conn, calls, uni, item, index, grouped)
                    study.write_json(out / f'sample-{label}' / f'item{index}-result.json', result)
                    print(f'WRITTEN {label} item={index} groups={len(result.get("groups", []))} new_views={len(result.get("new_views", {}))}', flush=True)
                except Exception as error:
                    conn.rollback()
                    study.write_json(failed, {'item_index': index, 'error': type(error).__name__ + ': ' + str(error)[:1000]})
                    print(f'FAILED {label} item={index}: {type(error).__name__}: {str(error)[:500]}', flush=True)
                    if 'budget' in str(error).lower():
                        break
            else:
                continue
            break
        for label, _, calls, conn in streams:
            if store.is_processed(conn, items[-1]['input_id']):
                route = dispatch.route(conn, items[-1], uni)
                study.write_json(out / f'sample-{label}' / 'resend.json', {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    report(out)


def report(out):
    streams = []
    for path in sorted(out.glob('sample-*')):
        completed = [json.loads(p.read_text()) for p in sorted(path.glob('item*-result.json'))]
        failure = json.loads((path / 'failed.json').read_text()) if (path / 'failed.json').exists() else None
        streams.append({'stream': path.name, 'completed_articles': len(completed), 'failure': failure,
                        'events': completed, 'resend': json.loads((path / 'resend.json').read_text()) if (path / 'resend.json').exists() else None})
    budget = json.loads((out / 'budget.json').read_text())
    result = {'streams': streams, 'attempts': len(budget['attempts']), 'estimated_usd': budget['estimated_spent'],
              'sealed_unchanged': study.digest(SEALED) == json.loads((out / 'manifest.json').read_text())['sealed_sha256']}
    study.write_json(out / 'summary.json', result)
    print(f'FINISHED attempts={result["attempts"]} estimated_usd={result["estimated_usd"]:.6f} sealed_unchanged={result["sealed_unchanged"]}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run', 'report'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    {'prepare': prepare, 'run': run, 'report': report}[args.command](args.out.resolve())
