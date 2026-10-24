"""06-views.md step 7: one re-judging round. Open views whose reading changed are judged in dependency order, each
once; a view whose conclusion changed adds its open dependants. The model reads the evidence in force (with each
replaced predecessor), the dependencies' current conclusions and its own last conclusion (for comparison only).
Code checks every citation and that a rung move or a first judgement says changed; one retry, then the item fails."""
import dataclasses
import json
import os

from .. import config, model
from . import store

PROMPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
PUSHES = ['推向第一格', '推向最后一格', '不推']

SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'required': ['rung', 'reasons', 'cites', 'cites_views', 'pushes', 'changed', 'why_changed'],
    'properties': {
        'rung': {'type': 'integer'}, 'reasons': {'type': 'string'},
        'cites': {'type': 'array', 'items': {'type': 'string'}}, 'cites_views': {'type': 'array', 'items': {'type': 'string'}},
        'pushes': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['evidence_id', 'push'],
                                              'properties': {'evidence_id': {'type': 'string'}, 'push': {'type': 'string', 'enum': PUSHES}}}},
        'changed': {'type': 'boolean'}, 'why_changed': {'type': 'string'},
    },
}


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


def build_prompt(conn, view_id, prompt_version='judging-v1'):
    v = store.view(conn, view_id)
    rungs = store.rungs_of(conn, view_id)
    pieces = store.evidence_in_force(conn, view_id)
    deps = store.dependencies_of(conn, view_id)
    last = store.current_state(conn, view_id)
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
    with open(config.prompt_path(prompt_version + '.txt'), encoding='utf-8') as handle:
        return handle.read(), '\n'.join(lines)


def check_answer(conn, view_id, data):
    errors = []
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
    data = answer.data
    judgement_id = store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=item['input_id'], rung=data['rung'],
                                reasons=data['reasons'], cited_evidence_json=json.dumps(data['cites']), cited_views_json=json.dumps(data['cites_views']),
                                pushes_json=json.dumps(data['pushes'], ensure_ascii=False), changed=1 if data['changed'] else 0,
                                why_changed=data['why_changed'], config_checksum=cfg.checksum, call_id=answer.call_id,
                                request_sha256=answer.request_sha256, publication_day=item['publication_day'])
    conn.commit()
    return {'view_id': view_id, 'judgement_id': judgement_id, 'rung': data['rung'], 'changed': data['changed'], 'cost': answer.cost_usd, 'cached': answer.cached}


def judge_one(archive, cfg, conn, view_id, seq, item, *, transport=None):
    system, user = build_prompt(conn, view_id, cfg.rejudging.prompt_version)
    note = ''
    for attempt in range(2):
        answer = model.call(archive, cfg, cfg.rejudging, system, user + note, SCHEMA, 'judgement', 'judge', transport=transport)
        errors = check_answer(conn, view_id, answer.data)
        if not errors:
            return _record(conn, cfg, view_id, seq, item, answer)
        note = '\n\n上一次的答案被代码退回，原因：' + '；'.join(errors) + '\n请改正后再交（只能引用列出的编号）。'
    raise JudgementRefused(f'{view_id}: ' + '; '.join(errors))


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


def round_of_judgements(archive, cfg, conn, changed_views, seq, item, *, transport=None):
    """Judge the open views in changed_views, dependencies first; a changed conclusion queues open dependants.

    Views that do not depend on each other are judged at the same time: each level of the dependency order is sent
    to the model concurrently (the prompts are built and the answers checked and written in this thread, so the
    database connection never crosses threads). A view waits while anything upstream of it is still pending, so a
    dependant always reads this round's conclusion of its dependency. A view with no evidence in force stays
    还没判 (D59), and a view already judged at this sequence number (a resumed round) is not judged twice."""
    import concurrent.futures

    def eligible(view_id):
        return store.is_open(conn, view_id) and not store.has_judgement(conn, view_id, seq) and bool(store.evidence_in_force(conn, view_id))

    pending = [v for v in topological(conn, changed_views) if eligible(v)]
    done, results = set(), []
    while pending:
        level = [v for v in pending if upstream(conn, v).isdisjoint(set(pending) - {v})] or pending[:1]
        prompts = {v: build_prompt(conn, v, cfg.rejudging.prompt_version) for v in level}

        def ask(view_id, note=''):
            system, user = prompts[view_id]
            return model.call(archive, cfg, cfg.rejudging, system, user + note, SCHEMA, 'judgement', 'judge', transport=transport)

        with concurrent.futures.ThreadPoolExecutor(max_workers=JUDGE_WORKERS) as pool_:
            answers = dict(zip(level, pool_.map(ask, level)))
        for view_id in level:
            answer = answers[view_id]
            errors = check_answer(conn, view_id, answer.data)
            if errors:
                note = '\n\n上一次的答案被代码退回，原因：' + '；'.join(errors) + '\n请改正后再交（只能引用列出的编号）。'
                answer = ask(view_id, note)
                errors = check_answer(conn, view_id, answer.data)
                if errors:
                    raise JudgementRefused(f'{view_id}: ' + '; '.join(errors))
            result = _record(conn, cfg, view_id, seq, item, answer)
            done.add(view_id)
            results.append(result)
            if result['changed']:
                for dependant in store.dependants_of(conn, view_id):
                    if dependant not in done and dependant not in pending and eligible(dependant):
                        pending.append(dependant)
        pending = [v for v in topological(conn, pending) if v not in done and eligible(v)]
    return results
