"""06-views.md step 7: one re-judging round. Open views whose reading changed are judged in dependency order, each
once; a view whose conclusion changed adds its open dependants. The model reads the evidence in force (with each
replaced predecessor), the dependencies' current conclusions and its own last conclusion (for comparison only).
Code checks every citation and that a rung move or a first judgement says changed; one retry, then the item fails.

judging-v1 and v2 ask and answer in Chinese; judging-v3 and later ask and answer in English (D163). The schema, the
request text and the retry note follow the prompt version; every answer is stored in the canonical vocabulary.

judging-v4 and later carry the theme block (D191, D195): an asset thesis is judged with every open, judged theme thesis in
view and answers, in theme_pushes, which way each theme it weighed pushes it; theme theses are judged before asset theses
in a round, and a theme judgement that says changed queues every open asset thesis with evidence in force, once. The
round's queue is derived from the ledger (the day's changed views, the dependants of views judged at this sequence number
with a changed conclusion, and the asset theses a changed theme queues), so a resumed round recovers what an earlier
commit had queued."""
import dataclasses
import json

from .. import config, model, vocabulary
from . import store

PUSHES = vocabulary.PUSHES
LEGACY_PUSHES = list(vocabulary.LEGACY['push'])
ENGLISH_FROM = 3                  # the first judging prompt version written in English
THEME_BLOCK_FROM = 4              # the first judging prompt version with the theme block
THEME_REASONS_CHARS = 300
UPDATED_MARK = 'updated since this thesis was last judged'


def version_number(prompt_version):
    return int(str(prompt_version or '').rpartition('-v')[2] or 0)


def is_english(prompt_version):
    return version_number(prompt_version) >= ENGLISH_FROM


def has_theme_block(prompt_version):
    return version_number(prompt_version) >= THEME_BLOCK_FROM


def schema_for(prompt_version):
    pushes = PUSHES if is_english(prompt_version) else LEGACY_PUSHES
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
    if has_theme_block(prompt_version):
        schema['required'].append('theme_pushes')
        schema['properties']['theme_pushes'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'push'],
                                                                           'properties': {'view_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': pushes}}}}
    return schema


def themes_in_force(conn, view_id, prompt_version):
    """The theme block of an asset thesis: every open theme thesis with a current state, with its rung label and whether a
    changed conclusion was recorded after this thesis's last judgement. Empty for a theme thesis or a version without the block."""
    if not has_theme_block(prompt_version) or store.view(conn, view_id)['object_kind'] == 'theme':
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


SCHEMA = schema_for('judging-v1')          # the shape of the answers stored under judging-v1 and v2


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


def _lines_chinese(conn, view_id, v, rungs, pieces, deps, last):
    lines = [f'观点 {view_id}（{v["object_id"]}，{v["kind"]}，看的是「{v["looks_at"]}」，{v["year"] or ""}，到期 {v["due_day"]}）：{v["question"]}',
             '梯子：' + ' / '.join(f'第 {r["position"]} 格 {r["label"]}：{r["condition"]}' for r in rungs), '',
             f'【这条观点下没被替代的证据，{len(pieces)} 条】']
    for p in pieces:
        src = p['sources'][0] if p['sources'] else {}
        lines.append(f'- {p["evidence_id"]}［{p["tier"]}；{p["speaker"]}；原始来源 {p["original_who"]} {p["original_day"]}；出处 {src.get("input_id")} {src.get("publication_day")}］{p["one_line"]}\n    原句：{p["quote"][:400]}')
        if p.get('replaced'):
            lines.append(f'    它替掉的前一条 {p["replaced"]["evidence_id"]}（{p["replaced"]["original_day"]}）：{p["replaced"]["one_line"]}')
    if deps:
        lines.append('\n【它依赖的观点现在的结论】')
        for d in deps:
            target = d['resolved_to']
            if not target:
                lines.append(f'- 等 {d["wait_chain_view_id"]} 链上 {d["wait_year"]} 年的那条：还没建（{d["direction"]}）')
                continue
            tv = store.view(conn, target)
            state = store.current_state(conn, target)
            flag = '只是历史' if d['resolution'] == 'history_only' else ('关了' if not store.is_open(conn, target) else '开着')
            rung_label = store.rungs_of(conn, target)[state['rung'] - 1]['label'] if state else '还没判'
            lines.append(f'- {target}（{flag}；{d["direction"]}）{tv["question"]}：现在 第 {state["rung"] if state else "-"} 格 {rung_label}；理由：{(state or {}).get("reasons", "")[:600]}')
    if last:
        lines.append(f'\n【上一次的结论（只用来比较）】第 {last["rung"]} 格；理由：{last["reasons"][:800]}')
    else:
        lines.append('\n【上一次的结论】还没有，这是第一次判，changed 必须写 true。')
    lines.append('\n按 JSON schema 交回。cites 只能写上面列出的证据编号，cites_views 只能写上面列出的依赖观点编号。')
    return lines


def _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes=()):
    lines = [f'Thesis {view_id} ({v["object_id"]}, {v["kind"]}, focus "{v["looks_at"]}", {v["year"] or ""}, due {v["due_day"]}): {v["question"]}',
             'Ladder: ' + ' / '.join(f'rung {r["position"]} {r["label"]}: {r["condition"]}' for r in rungs), '',
             f'[Evidence in force under this thesis, {len(pieces)} items]']
    for p in pieces:
        src = p['sources'][0] if p['sources'] else {}
        lines.append(f'- {p["evidence_id"]} [{p["tier"]}; {p["speaker"]}; original source {p["original_who"]} {p["original_day"]}; from {src.get("input_id")} {src.get("publication_day")}] {p["one_line"]}\n    Quote: {p["quote"][:400]}')
        if p.get('replaced'):
            lines.append(f'    It replaces {p["replaced"]["evidence_id"]} ({p["replaced"]["original_day"]}): {p["replaced"]["one_line"]}')
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
    lines.append('\nAnswer per the JSON schema. cites may name only the evidence ids listed above; cites_views only the dependency thesis ids listed above.'
                 + ('; theme_pushes only the theme ids listed above.' if themes else ''))
    return lines


def build_prompt(conn, view_id, prompt_version='judging-v1'):
    v = store.view(conn, view_id)
    rungs = store.rungs_of(conn, view_id)
    pieces = store.evidence_in_force(conn, view_id)
    deps = store.dependencies_of(conn, view_id)
    last = store.current_state(conn, view_id)
    if is_english(prompt_version):
        lines = _lines_english(conn, view_id, v, rungs, pieces, deps, last, themes_in_force(conn, view_id, prompt_version))
    else:
        lines = _lines_chinese(conn, view_id, v, rungs, pieces, deps, last)
    with open(config.prompt_path(prompt_version + '.txt'), encoding='utf-8') as handle:
        return handle.read(), '\n'.join(lines)


def retry_note(prompt_version, errors):
    if is_english(prompt_version):
        return '\n\nThe code returned the previous answer because: ' + '; '.join(errors) + '\nCorrect it and answer again, citing only the listed ids.'
    return '\n\n上一次的答案被代码退回，原因：' + '；'.join(errors) + '\n请改正后再交（只能引用列出的编号）。'


def check_answer(conn, view_id, data, prompt_version='judging-v1'):
    errors = []
    if has_theme_block(prompt_version):
        shown = {theme['view_id'] for theme in themes_in_force(conn, view_id, prompt_version)}
        named = []
        for entry in data.get('theme_pushes', []):
            if entry['view_id'] in named:
                errors.append(f'{entry["view_id"]} is named twice in theme_pushes')
            elif entry['view_id'] not in shown:
                errors.append(f'{entry["view_id"]} is not a theme in force shown to {view_id}')
            named.append(entry['view_id'])
    in_force = {p['evidence_id'] for p in store.evidence_in_force(conn, view_id)}
    deps = {d['resolved_to'] for d in store.dependencies_of(conn, view_id) if d['resolved_to']}
    rungs = store.rungs_of(conn, view_id)
    if not 1 <= data['rung'] <= len(rungs):
        errors.append(f'rung {data["rung"]} outside 1..{len(rungs)}')
    for cited in data['cites']:
        if cited not in in_force:
            errors.append(f'{cited} is not evidence in force under {view_id}' + (' (replaced)' if store.is_replaced(conn, cited) else ''))
    for cited in data['cites_views']:
        if cited not in deps:
            errors.append(f'{cited} is not a dependency of {view_id}')
    for push in data['pushes']:
        if push['evidence_id'] not in in_force:
            errors.append(f'push on {push["evidence_id"]} which is not under {view_id}')
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
                                why_changed=data['why_changed'], config_checksum=cfg.checksum, call_id=answer.call_id,
                                request_sha256=answer.request_sha256, publication_day=item['publication_day'])
    conn.commit()
    return {'view_id': view_id, 'judgement_id': judgement_id, 'rung': data['rung'], 'changed': data['changed'], 'cost': answer.cost_usd, 'cached': answer.cached}


JUDGE_WORKERS = 6


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


def queued_by_ledger(conn, seq, themed):
    """What the judgements already committed at this sequence number queued: the dependants of every view whose judgement
    said changed and, when the version carries the theme block and such a view is a theme thesis, every open asset thesis.
    A fresh round finds nothing here; a resumed round finds what the interrupted one had queued in memory."""
    queued = []
    for row in conn.execute('select view_id from judgements where seq=? and changed=1 order by judgement_id', (seq,)):
        queued.extend(store.dependants_of(conn, row['view_id']))
        if themed and store.view(conn, row['view_id'])['object_kind'] == 'theme':
            queued.extend(open_asset_views(conn))
    return queued


def round_of_judgements(archive, cfg, conn, changed_views, seq, item, *, transport=None):
    """Judge the open views in changed_views, dependencies first; a changed conclusion queues open dependants.

    Views that do not depend on each other are judged at the same time: each level of the dependency order is sent
    to the model concurrently (the prompts are built and the answers checked and written in this thread, so the
    database connection never crosses threads). A view waits while anything upstream of it is still pending, so a
    dependant always reads this round's conclusion of its dependency. A view with no evidence in force stays
    unjudged (D59), and a view already judged at this sequence number (a resumed round) is not judged twice.

    With the theme block (judging-v4+): among the views ready to be judged, theme theses go first, so an asset thesis
    reads this round's theme conclusions; a theme judgement that says changed queues every open asset thesis with
    evidence in force. The starting queue adds what the ledger says earlier commits at this sequence number queued."""
    import concurrent.futures

    version = cfg.rejudging.prompt_version
    schema = schema_for(version)
    themed = has_theme_block(version)

    def eligible(view_id):
        return store.is_open(conn, view_id) and not store.has_judgement(conn, view_id, seq) and bool(store.evidence_in_force(conn, view_id))

    def is_theme(view_id):
        return store.view(conn, view_id)['object_kind'] == 'theme'

    pending = [v for v in topological(conn, list(changed_views) + queued_by_ledger(conn, seq, themed)) if eligible(v)]
    done, results = set(), []
    while pending:
        ready = [v for v in pending if upstream(conn, v).isdisjoint(set(pending) - {v})] or pending[:1]
        level = ([v for v in ready if is_theme(v)] or ready) if themed else ready
        prompts = {v: build_prompt(conn, v, version) for v in level}

        def ask(view_id, note=''):
            system, user = prompts[view_id]
            return model.call(archive, cfg, cfg.rejudging, system, user + note, schema, 'judgement', 'judge', transport=transport)

        with concurrent.futures.ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as pool_:
            answers = dict(zip(level, pool_.map(ask, level)))
        for view_id in level:
            answer = answers[view_id]
            errors = check_answer(conn, view_id, answer.data, version)
            if errors:
                answer = ask(view_id, retry_note(version, errors))
                errors = check_answer(conn, view_id, answer.data, version)
                if errors:
                    raise JudgementRefused(f'{view_id}: ' + '; '.join(errors))
            result = _record(conn, cfg, view_id, seq, item, answer)
            done.add(view_id)
            results.append(result)
            if result['changed']:
                queued = store.dependants_of(conn, view_id) + (open_asset_views(conn) if themed and is_theme(view_id) else [])
                for dependant in queued:
                    if dependant not in done and dependant not in pending and eligible(dependant):
                        pending.append(dependant)
        pending = [v for v in topological(conn, pending) if v not in done and eligible(v)]
    return results
