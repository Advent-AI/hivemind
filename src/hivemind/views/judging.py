"""06-views.md step 7: one re-judging round. Open views whose reading changed are judged in dependency order, each
once; a view whose conclusion changed adds its open dependants. The model reads the evidence in force (with each
replaced predecessor), the dependencies' current conclusions and its own last conclusion (for comparison only).
Code checks every citation and that a rung move or a first judgement says changed; one retry, then the item fails.

The request is judging-v7 (D354, frozen with steps 3 and 4): no other version is built, and a configuration that names another is
refused before any call. Every answer is stored in the canonical vocabulary.

The theme block (D191, D195): an asset thesis is judged with every open, judged theme thesis in view and answers, in theme_pushes,
which way each theme it weighed pushes it; theme theses are judged before asset theses in a round, and a theme judgement that says
changed queues every open asset thesis with evidence in force, once. The round's queue is derived from the ledger (the day's changed
views, the dependants of views judged at this sequence number with a changed conclusion, and the asset theses a changed theme queues),
so a resumed round recovers what an earlier commit had queued.

The evidence in view (D198): a judgement reads the arrivals and the basis among the evidence in force, not everything in force.

The reference (D260): the rung is the forecast the evidence in force makes most likely, judged against what the market expects
(consensus, guidance, the stated plan); the answer states the reference and the outcome the evidence implies, both stored beside the
rung, and an empty one is refused."""
import dataclasses
import json
import re

from .. import config, model, vocabulary
from . import store

PUSHES = vocabulary.PUSHES
SUPPORTED_VERSIONS = ('judging-v7',)   # D354: the frozen judging prompt
READINGS = 5                      # a piece is shown in the thesis's first five judgements after it arrives
BASIS = 10                        # and while one of the last ten judgements cited it
THEME_REASONS_CHARS = 300
UPDATED_MARK = 'updated since this thesis was last judged'


def require_supported(prompt_version):
    """Refuses a judging prompt version this code does not build, before any request is made."""
    if prompt_version not in SUPPORTED_VERSIONS:
        raise ValueError(f'judging {prompt_version!r} is not built; this code builds only {", ".join(SUPPORTED_VERSIONS)} (D354)')


def evidence_in_view(conn, view_id):
    """(the pieces a judgement of this thesis reads, how many pieces in force are not shown): the arrivals (linked after the
    READINGS-th most recent judgement, or all when there are fewer) and the basis (cited by one of the last BASIS judgements),
    both among the evidence in force."""
    in_force = store.evidence_in_force(conn, view_id)
    recent = store.recent_judgements(conn, view_id, BASIS)
    arrivals_after = recent[READINGS - 1]['seq'] if len(recent) >= READINGS else -1
    basis = {evidence_id for j in recent for evidence_id in j['cites']}
    linked_at = {r['evidence_id']: r['seq'] for r in conn.execute('select evidence_id, seq from evidence_links where view_id=?', (view_id,))}
    shown = [p for p in in_force if linked_at.get(p['evidence_id'], -1) > arrivals_after or p['evidence_id'] in basis]
    return shown, len(in_force) - len(shown)


def schema_for(prompt_version):
    require_supported(prompt_version)
    pushes = PUSHES
    schema = {
        'type': 'object', 'additionalProperties': False,
        'required': ['rung', 'reasons', 'cites', 'cites_views', 'pushes', 'changed', 'why_changed'],
        'properties': {
            'rung': {'type': 'integer'}, 'reasons': {'type': 'string'},
            'cites': {'type': 'array', 'items': {'type': 'string'}}, 'cites_views': {'type': 'array', 'items': {'type': 'string'}},
            'pushes': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['evidence_id', 'push'],
                                                  'properties': {'evidence_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': pushes}}}},
            'changed': {'type': 'boolean'}, 'why_changed': {'type': 'string'},
        },
    }
    schema['required'].append('theme_pushes')
    schema['properties']['theme_pushes'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'push'],
                                                                       'properties': {'view_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': pushes}}}}
    schema['required'][1:1] = STANCE_FIELDS           # after rung: the reference and the implied outcome are written before the reasons
    schema['properties'].update({field: {'type': 'string'} for field in STANCE_FIELDS})
    return schema


def themes_in_force(conn, view_id):
    """The theme block of an asset thesis: every open theme thesis with a current state, with its rung label and whether a
    changed conclusion was recorded after this thesis's last judgement. Empty for a theme thesis."""
    if store.view(conn, view_id)['object_kind'] == 'theme':
        return []
    last = store.current_state(conn, view_id)
    out = []
    for row in conn.execute("select view_id from views where object_kind='theme' order by view_id"):
        theme_id = row['view_id']
        state = store.current_state(conn, theme_id)
        if not state or not store.is_open(conn, theme_id):
            continue
        updated = bool(last) and bool(conn.execute('select 1 from judgements where view_id=? and changed=1 and judgement_id>? limit 1',
                                                   (theme_id, last['judgement_id'])).fetchone())
        rung = store.rungs_of(conn, theme_id)[state['rung'] - 1]
        out.append({'view_id': theme_id, 'view': store.view(conn, theme_id), 'state': state, 'rung_label': rung['label'], 'updated': updated})
    return out


STANCE_FIELDS = ['reference', 'implied_outcome']   # D260: what the market expects, and the figure or date the evidence implies


class JudgementRefused(Exception):
    pass


def topological(conn, view_ids):
    """Dependencies first: a view comes after every view it depends on that is also in the set."""
    remaining = list(dict.fromkeys(view_ids))
    ordered, placed = [], set()
    while remaining:
        progressed = False
        for view_id in list(remaining):
            deps = {d['resolved_to'] for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
            if deps.isdisjoint(set(remaining) - {view_id}) or deps <= placed:
                ordered.append(view_id)
                placed.add(view_id)
                remaining.remove(view_id)
                progressed = True
        if not progressed:                 # a cycle slipped through: keep going in the given order
            ordered.extend(remaining)
            break
    return ordered


def _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes=(), hidden=0):
    """hidden: how many pieces in force are not shown."""
    lines = [f'Thesis {view_id} ({v["object_id"]}, {v["kind"]}, focus "{v["looks_at"]}", {v["year"] or ""}, due {v["due_day"]}): {v["question"]}',
             'Ladder: ' + ' / '.join(f'rung {r["position"]} {r["label"]}: {r["condition"]}' for r in rungs), '',
             f'[Evidence in view under this thesis, {len(pieces)} items]']
    if hidden:
        lines.append(f'[Not shown: {hidden} more pieces in force, read in earlier judgements; the previous conclusion carries them]')
    for p in pieces:
        src = p['sources'][0] if p['sources'] else {}
        lines.append(f'- {p["evidence_id"]} [{p["tier"]}; {p["speaker"]}; original source {p["original_who"]} {p["original_day"]}; from {src.get("input_id")} {src.get("publication_day")}] {p["one_line"]}\n    Quote: {p["quote"][:400]}')
        if p.get('replaced'):
            lines.append(f'    It replaces {p["replaced"]["evidence_id"]} ({p["replaced"]["original_day"]}): {p["replaced"]["one_line"]}')
        if p.get('same_as'):
            lines.append(f'    Opinion, not verified: the matcher read this as the same claim as {", ".join(p["same_as"])}; the argument counts one claim, one more outlet.')
        if p.get('revises'):
            lines.append(f'    Opinion, not verified: the matcher read it as a later version of {p["revises"]["evidence_id"]} ({p["revises"]["original_day"]}); both are in force: {p["revises"]["one_line"]}')
    if deps:
        lines.append('\n[Current conclusions of the theses it depends on]')
        for d in deps:
            target = d['resolved_to']
            if not target:
                lines.append(f'- the {d["wait_year"]} thesis on chain {d["wait_chain_view_id"]}: not yet created ({d["direction"]})')
                continue
            tv = store.view(conn, target)
            state = store.current_state(conn, target)
            flag = 'historical only' if d['resolution'] == 'history_only' else ('closed' if not store.is_open(conn, target) else 'open')
            rung_label = store.rungs_of(conn, target)[state['rung'] - 1]['label'] if state else 'not judged yet'
            lines.append(f'- {target} ({flag}; {d["direction"]}) {tv["question"]}: now rung {state["rung"] if state else "-"} {rung_label}; reasons: {(state or {}).get("reasons", "")[:600]}')
    if themes:
        lines.append(f'\n[Themes in force, {len(themes)}]')
        for theme in themes:
            tv, state = theme['view'], theme['state']
            mark = f'; {UPDATED_MARK}' if theme['updated'] else ''
            lines.append(f'- {theme["view_id"]} ({tv["object_id"]}, due {tv["due_day"]}) {tv["question"]}: now rung {state["rung"]} {theme["rung_label"]}; '
                         f'judged {state["publication_day"]}{mark}; reasons: {(state["reasons"] or "")[:THEME_REASONS_CHARS]}')
    if last:
        lines.append(f'\n[Previous conclusion, for comparison only] rung {last["rung"]}; reasons: {last["reasons"][:800]}')
    else:
        lines.append('\n[Previous conclusion] none: this is the first judgement, so changed must be true.')
    lines.append('\nAnswer per the JSON schema. cites may name only the evidence ids listed above; '
                 + ('cites_views only the dependency thesis ids listed above' if deps else 'cites_views must be empty: this thesis depends on no other thesis')
                 + ('; theme_pushes only the theme ids listed above; a theme id goes only in theme_pushes, never in cites or cites_views' if themes else '') + '.')
    return lines


def build_prompt(conn, view_id, prompt_version):
    require_supported(prompt_version)
    v = store.view(conn, view_id)
    rungs = store.rungs_of(conn, view_id)
    pieces, hidden = evidence_in_view(conn, view_id)
    deps = store.dependencies_of(conn, view_id)
    last = store.current_state(conn, view_id)
    lines = _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes_in_force(conn, view_id), hidden=hidden)
    with open(config.prompt_path(prompt_version + '.txt'), encoding='utf-8') as handle:
        return handle.read(), '\n'.join(lines)


def retry_note(errors):
    return '\n\nThe code returned the previous answer because: ' + '; '.join(errors) + '\nCorrect it and answer again, citing only the listed ids.'


def themes_shown_in(request_text):
    """The theme ids of the block a request carried: the ids the answer may name, whatever the ledger says now."""
    block = request_text.split('\n[Themes in force, ', 1)
    return set(re.findall(r'^- (v\d+) \(', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def evidence_shown_in(request_text):
    """The evidence ids the request listed: the ids the answer may cite and push."""
    block = request_text.split('\n[Evidence in ', 1)
    return set(re.findall(r'^- (e\d+) \[', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def check_answer(conn, view_id, data, request_text=None):
    """request_text: the user message that was sent, so theme and evidence ids are checked against what it carried (a theme may have
    closed or opened since); without it, against what the ledger would show now."""
    errors = []
    shown = themes_shown_in(request_text) if request_text is not None else {theme['view_id'] for theme in themes_in_force(conn, view_id)}
    named = []
    for entry in data.get('theme_pushes', []):
        if entry['view_id'] in named:
            errors.append(f'{entry["view_id"]} is named twice in theme_pushes')
        elif entry['view_id'] not in shown:
            errors.append(f'{entry["view_id"]} is not a theme in force shown to {view_id}')
        named.append(entry['view_id'])
    # the closed set is what the request showed (D198), read from the text that was sent, else computed from the ledger
    allowed = evidence_shown_in(request_text) if request_text is not None else {p['evidence_id'] for p in evidence_in_view(conn, view_id)[0]}
    not_allowed = lambda e: f'{e} is not among the evidence shown to {view_id}'
    bad_push = lambda e: f'push on {e} which was not shown to {view_id}'
    deps = {d['resolved_to'] for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
    rungs = store.rungs_of(conn, view_id)
    if not 1 <= data['rung'] <= len(rungs):
        errors.append(f'rung {data["rung"]} outside 1..{len(rungs)}')
    for cited in data['cites']:
        if cited not in allowed:
            errors.append(not_allowed(cited))
    for cited in data['cites_views']:
        if cited not in deps:
            errors.append(f'{cited} is not a dependency of {view_id}')
    for push in data['pushes']:
        if push['evidence_id'] not in allowed:
            errors.append(bad_push(push['evidence_id']))
    for field in STANCE_FIELDS:
        if not str(data.get(field) or '').strip():
            errors.append(f'{field} is empty: state what the market expects and the figure or date the evidence implies')
    last = store.current_state(conn, view_id)
    if last is None and not data['changed']:
        errors.append('first judgement must say changed')
    if last is not None and last['rung'] != data['rung'] and not data['changed']:
        errors.append(f'rung moved from {last["rung"]} to {data["rung"]} but changed is false')
    return errors


def _record(conn, cfg, view_id, seq, item, answer):
    data = vocabulary.judgement_answer(answer.data)
    judgement_id = store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=item['input_id'], rung=data['rung'],
                                reasons=data['reasons'], cited_evidence_json=json.dumps(data['cites']), cited_views_json=json.dumps(data['cites_views']),
                                pushes_json=json.dumps(data['pushes'], ensure_ascii=False), changed=1 if data['changed'] else 0,
                                theme_pushes_json=json.dumps(data.get('theme_pushes', []), ensure_ascii=False),
                                reference=data.get('reference'), implied_outcome=data.get('implied_outcome'),
                                why_changed=data['why_changed'], config_checksum=cfg.checksum, call_id=answer.call_id,
                                request_sha256=answer.request_sha256, publication_day=item['publication_day'])
    conn.commit()
    return {'view_id': view_id, 'judgement_id': judgement_id, 'rung': data['rung'], 'changed': data['changed'], 'cost': answer.cost_usd, 'cached': answer.cached}


JUDGE_WORKERS = 32     # a day's round is up to 40 judgements of about 16 s each in two dependency levels (themes, then assets); 32 at a time makes a round about two calls long (2026-11-02)


def upstream(conn, view_id):
    """Every view this one depends on, directly or through its dependencies."""
    seen, stack = set(), [view_id]
    while stack:
        for dep in store.dependencies_of(conn, stack.pop()):
            target = dep['resolved_to']
            if target and target not in seen:
                seen.add(target)
                stack.append(target)
    return seen


def open_asset_views(conn):
    return [v for v in store.open_views(conn) if store.view(conn, v)['object_kind'] != 'theme']


def queued_by_change(conn, view_id):
    """What a changed conclusion of this view queues: its dependants and, for a theme thesis, every open asset thesis. The one rule,
    read for a live judgement and for the judgements a resumed round finds committed."""
    queued = store.dependants_of(conn, view_id)
    if store.view(conn, view_id)['object_kind'] == 'theme':
        queued = queued + open_asset_views(conn)
    return queued


def queued_by_ledger(conn, seq):
    """What the judgements already committed at this sequence number queued; a fresh round finds nothing here, a resumed round
    finds what the interrupted one had queued in memory."""
    queued = []
    for row in conn.execute('select view_id from judgements where seq=? and changed=1 order by judgement_id', (seq,)):
        queued.extend(queued_by_change(conn, row['view_id']))
    return queued


def round_of_judgements(archive, cfg, conn, changed_views, seq, item, *, transport=None):
    """Judge the open views in changed_views, dependencies first; a changed conclusion queues open dependants.

    Views that do not depend on each other are judged at the same time: each level of the dependency order is sent
    to the model concurrently (the prompts are built and the answers checked and written in this thread, so the
    database connection never crosses threads). A view waits while anything upstream of it is still pending, so a
    dependant always reads this round's conclusion of its dependency. A view with no evidence in force stays
    unjudged (D59), and a view already judged at this sequence number (a resumed round) is not judged twice.

    Among the views ready to be judged, theme theses go first, so an asset thesis reads this round's theme conclusions; a theme judgement that says changed queues every open asset thesis with
    evidence in force. The starting queue adds what the ledger says earlier commits at this sequence number queued."""
    import concurrent.futures

    version = cfg.rejudging.prompt_version
    schema = schema_for(version)

    def eligible(view_id):
        return store.is_open(conn, view_id) and not store.has_judgement(conn, view_id, seq) and bool(store.rungs_of(conn, view_id)) and bool(store.evidence_in_force(conn, view_id))

    def is_theme(view_id):
        return store.view(conn, view_id)['object_kind'] == 'theme'

    pending = [v for v in topological(conn, list(changed_views) + queued_by_ledger(conn, seq)) if eligible(v)]
    done, results = set(), []
    while pending:
        ready = [v for v in pending if upstream(conn, v).isdisjoint(set(pending) - {v})] or pending[:1]
        level = [v for v in ready if is_theme(v)] or ready
        prompts = {v: build_prompt(conn, v, version) for v in level}

        def ask(view_id, note=''):
            system, user = prompts[view_id]
            return model.call(archive, cfg, cfg.rejudging, system, user + note, schema, 'judgement', 'judge', transport=transport)

        with concurrent.futures.ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as pool_:
            answers = dict(zip(level, pool_.map(ask, level)))
        for view_id in level:
            answer = answers[view_id]
            errors = check_answer(conn, view_id, answer.data, prompts[view_id][1])
            if errors:
                archive.retire(answer.call_id)                 # a refused answer never answers the same request again (a resume re-samples)
                answer = ask(view_id, retry_note(errors))
                errors = check_answer(conn, view_id, answer.data, prompts[view_id][1])
                if errors:
                    archive.retire(answer.call_id)
                    raise JudgementRefused(f'{view_id}: ' + '; '.join(errors))
            result = _record(conn, cfg, view_id, seq, item, answer)
            done.add(view_id)
            results.append(result)
            if result['changed']:
                for dependant in queued_by_change(conn, view_id):
                    if dependant not in done and dependant not in pending and eligible(dependant):
                        pending.append(dependant)
        pending = [v for v in topological(conn, pending) if v not in done and eligible(v)]
    return results
