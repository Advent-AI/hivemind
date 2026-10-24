"""Trace every item of a replay window through the pipeline and write one HTML page to inspect it.

For each item in the test corpus between two days the page shows: how dispatch routed it (and why it did not go
to extraction), what the model wrote for it (every evidence row and every candidate view, from the archived
answer), what the code checks dropped and why (the handover's dropped list), what matching decided for every
candidate and every piece of evidence (and why, in the model's words), what was written to the views database,
and how the day's re-judging read the views it changed. Every number on the page is counted from stored data:
the archive (model answers), the views database (processing steps, handovers, matching records, judgements) and
the corpus. Nothing is sent to a model.

Usage: python3 scripts/trace_items.py --from 2026-02-25 --to 2026-08-15 [--views DB] [--out DIR]
Writes DIR/index.html, DIR/text/<slug>.txt (the item's text), DIR/request/<slug>.txt (the extraction request as
the model saw it) and DIR/answer/<slug>.json (the model's raw answer). Read-only on every database.
"""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import dispatch, extraction, testdb, universe as universe_module  # noqa: E402

ITEM_ID = re.compile(r'【信息】编号 (\S+?)，类别 ')
BLOCK5_LINE = re.compile(r'^\s+- (v\d+)（(.*)$', re.M)
# a key is "sk-" (not the tail of "musk-" or "sk-hynix-…") followed by an unbroken run of 20+ letters and digits
# that holds a digit; URL slugs are hyphen-separated words and never match
SECRET = re.compile(r'(?<![A-Za-z0-9])sk-(?:[A-Za-z0-9_\-]*?)(?=[A-Za-z0-9_]{20,})(?=[A-Za-z_]*\d)[A-Za-z0-9_]{20,}|Bearer\s+(?=[A-Za-z0-9_\-\.]*\d)[A-Za-z0-9_\-\.]{20,}')
QUOTE_CHARS = 400
REASON_CHARS = 400

DROP_CLASSES = [
    ('quote not in item', '原句不在原文里（模型改了字或编了句子）'),
    ('links to nothing shown', '连到不存在的观点编号'),
    ('same quote as', '同一句写了两次（合并成一条，不算杂音）'),
    ('candidate ladder', '梯子格式不对（格数或标签）'),
    ('quarterly number', '季度数当成观点（规则：季度数是证据）'),
    ('is beyond next year', '年份超出明年（规则：不开）'),
    ('due_day not a date', '到期日不是日期'),
    ('not after the item', '到期日不在发布日之后'),
    ('candidate without surviving evidence', '候选观点的证据都被丢了，观点跟着丢'),
]
NOTE_CLASSES = [
    ('linked to nothing kept; not stored', '证据连的候选观点没开，证据没存'),
    ('late older statement', '更早的旧话晚到，不连'),
    ('that candidate was not opened', '依赖的候选观点没开，依赖丢掉'),
    ('cycle', '依赖成环，丢掉'),
]


def open_read_only(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def classify(text, classes, fallback):
    for needle, label in classes:
        if needle in text:
            return label
    return fallback


def evidence_drop_class(why, links, shown_ids, answer_candidate_ids, dropped_candidate_ids):
    """'links to nothing shown' split by what the link actually pointed at, so the mechanism is visible."""
    if 'links to nothing shown' not in why:
        return classify(why, DROP_CLASSES, '其他')
    if not links:
        return '没写 links（一条观点都没连）'
    if set(links) & dropped_candidate_ids:
        return '连的候选观点被代码丢了，证据跟着丢'
    if any(re.fullmatch(r'c\d+', link) and link not in answer_candidate_ids for link in links):
        return '连到模型没写出来的候选观点编号'
    if any(re.fullmatch(r'v\d+', link) and link not in shown_ids for link in links):
        return '连到没给它看的观点编号（别的对象的，或编出来的）'
    return '连到不存在的观点编号'


def slug_of(input_id):
    return hashlib.sha1(input_id.encode('utf-8')).hexdigest()[:12]


def trim(text, limit):
    text = text or ''
    return text if len(text) <= limit else text[:limit] + '…'


def route_offline(item, uni):
    """dispatch.route without its writes: the same three questions, in plain words."""
    missing = [field for field in dispatch.REQUIRED if not item.get(field)]
    if missing:
        return '退回', f'缺字段 {missing}'
    if item.get('copy_of'):
        return '合并', f'是 {item["copy_of"]} 的转载'
    if item.get('supersedes'):
        return '不处理', '更正稿（POC 不支持）'
    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
    if not objects:
        labelled = [o['value'] for o in item['object_identifiers']]
        return '不处理', f'对象不在研究名单上（上游标的是 {labelled or "空"}）'
    if not any(uni.watches(o, item['category']) for o in objects):
        return '不处理', f'{item["category"]} 这一类对 {objects} 不看'
    return '进流程', ''


def load_extract_calls(archive):
    """Every stored extraction call keyed by the item it was about, parsed from the request's 【信息】 line."""
    calls = collections.defaultdict(list)
    rows = archive.execute("select call_id, config_version, model, request_json, answer_json, prompt_chars, input_tokens, output_tokens, "
                           "cost_usd, seconds, created_at from model_calls where purpose='extract' and request_sha256 not like '%:%'")
    for row in rows:
        request = json.loads(row['request_json'])
        user = request['messages'][1]['content']
        found = ITEM_ID.search(user)
        if not found:
            continue
        calls[found.group(1)].append(dict(row, system=request['messages'][0]['content'], user=user))
    for item_calls in calls.values():
        item_calls.sort(key=lambda c: (c['created_at'], c['call_id']))
    return calls


def pick_call(item_calls, extracted_at):
    """The call whose answer the round used: the last one that had landed when the 'extracted' step was marked."""
    before = [c for c in item_calls if c['created_at'] <= extracted_at]
    return before[-1] if before else (item_calls[-1] if item_calls else None)


def match_outcomes(records):
    """The accepted first call (candidates and straight-linked evidence) and the accepted second call."""
    accepted = {}
    for rec in records:
        checks = json.loads(rec['checks_json'] or '{}')
        if checks.get('refusals'):
            continue
        group = 1 if rec['call_no'] <= 2 else 2
        accepted[group] = rec
    return accepted


def build_item_trace(item, uni, views, archive_calls, archive, text_dir, request_dir, answer_dir, window_start):
    input_id = item['input_id']
    slug = slug_of(input_id)
    route_kind, route_reason = route_offline(item, uni)
    trace = {
        'id': input_id, 'slug': slug, 'day': item['publication_day'], 'category': item['category'],
        'publisher': item.get('publisher') or '', 'publisher_type': item.get('publisher_type') or '',
        'objects': [o['value'] for o in item['object_identifiers']], 'title': item.get('title') or '',
        'uri': item.get('source_uri') or '', 'chars': item.get('text_chars') or len(item.get('text') or ''),
        'route': route_kind, 'route_reason': route_reason, 'excerpt': trim(re.sub(r'\s+', ' ', item.get('text') or ''), 500),
        'steps': [], 'cost': 0.0, 'diagnosis': '', 'diagnosis_why': '', 'noise': 0, 'produced': 0,
    }
    with open(os.path.join(text_dir, slug + '.txt'), 'w', encoding='utf-8') as handle:
        handle.write(f'{input_id}\n{item.get("title") or ""}\n{item.get("publisher")} ({item.get("publisher_type")}) {item["publication_day"]} {item["category"]}\n{item.get("source_uri") or ""}\n\n{item.get("text") or ""}')
    steps = [dict(r) for r in views.execute('select sequence_no, step, result, reason, at from processing_steps where input_id=? order by id', (input_id,))]
    trace['steps'] = [{'seq': s['sequence_no'], 'step': s['step'], 'result': s['result'], 'reason': trim(s['reason'], 600), 'at': s['at']} for s in steps]
    if route_kind != '进流程':
        trace['diagnosis'] = route_kind
        trace['diagnosis_why'] = route_reason
        return trace
    if not steps:
        trace['diagnosis'] = '未跑'
        trace['diagnosis_why'] = '启动期（%s 之前）只跑了 NVDA 的材料' % window_start if item['publication_day'] < window_start else '没有处理记录'
        return trace
    trace['seq'] = max(s['sequence_no'] for s in steps)
    failed = [s for s in steps if s['result'] == 'failed']
    extracted = [s for s in steps if s['step'] == 'extracted']
    # --- extraction: the raw answer and what the code kept
    handover_row = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (input_id,)).fetchone()
    handover = json.loads(handover_row['handover_json']) if handover_row else {'evidence': [], 'candidates': [], 'dropped': []}
    call = pick_call(archive_calls.get(input_id, []), extracted[-1]['at'] if extracted else '9999')
    answer = json.loads(call['answer_json']) if call and call['answer_json'] else {'evidence': [], 'candidates': []}
    kept_quotes = {extraction.normalise(e['quote']) for e in handover['evidence']}
    answer_quotes = {extraction.normalise(e['quote']) for e in answer.get('evidence', [])}
    trace['answer_matches_handover'] = kept_quotes <= answer_quotes
    dropped = {ident: why for ident, why in handover.get('dropped', [])}
    kept_evidence_ids = {e['id'] for e in handover['evidence']}
    kept_candidate_ids = {c['id'] for c in handover['candidates']}
    shown = []
    if call:
        for view_id, rest in BLOCK5_LINE.findall(call['user'].split('【信息】')[0]):
            shown.append(f'{view_id}（{rest}')
        trace['extract_call'] = {'model': call['model'], 'prompt_chars': call['prompt_chars'], 'input_tokens': call['input_tokens'],
                                 'output_tokens': call['output_tokens'], 'seconds': round(call['seconds'] or 0, 1), 'cost': round(call['cost_usd'] or 0, 4),
                                 'config': call['config_version'], 'candidates_of_item': len(archive_calls.get(input_id, []))}
        trace['cost'] += call['cost_usd'] or 0
        with open(os.path.join(request_dir, slug + '.txt'), 'w', encoding='utf-8') as handle:
            handle.write('=== system ===\n' + call['system'] + '\n\n=== user ===\n' + call['user'])
        with open(os.path.join(answer_dir, slug + '.json'), 'w', encoding='utf-8') as handle:
            json.dump(answer, handle, ensure_ascii=False, indent=1)
    trace['shown_views'] = shown
    shown_ids = {line.split('（')[0] for line in shown}
    answer_candidate_ids = {c['id'] for c in answer.get('candidates', [])}
    dropped_candidate_ids = answer_candidate_ids - kept_candidate_ids
    raw_evidence = []
    for e in answer.get('evidence', []):
        if e['id'] in kept_evidence_ids:
            status, why, why_class = '留下', '', ''
        elif e['id'] in dropped:
            status, why = '丢掉', dropped[e['id']]
            why_class = evidence_drop_class(why, e['links'], shown_ids, answer_candidate_ids, dropped_candidate_ids)
        else:
            status, why, why_class = '丢掉', '留下的证据后来没有可连的观点（候选观点没留下）', '连的候选观点被代码丢了，证据跟着丢'
        raw_evidence.append({'id': e['id'], 'tier': e['tier'], 'speaker': e['speaker'], 'original_who': e.get('original_who', ''),
                             'original_day': e.get('original_day', ''), 'quote': trim(e['quote'], QUOTE_CHARS), 'one_line': e['one_line'],
                             'links': e['links'], 'status': status, 'why': why, 'why_class': why_class})
    raw_candidates = []
    for c in answer.get('candidates', []):
        if c['id'] in kept_candidate_ids:
            status, why = '留下', ''
        else:
            status, why = '丢掉', dropped.get(c['id'], '')
        raw_candidates.append({'id': c['id'], 'kind': c['kind'], 'object': c['object'], 'looks_at': c['looks_at'], 'question': c['question'],
                               'rungs': [f'{r["label"]}：{r["condition"]}' for r in c['rungs']], 'due_day': c['due_day'], 'year': c['year'],
                               'evidence_ids': c['evidence_ids'], 'status': status, 'why': why,
                               'why_class': classify(why, DROP_CLASSES, '其他') if status == '丢掉' else ''})
    trace['raw_evidence'], trace['raw_candidates'] = raw_evidence, raw_candidates
    produced = len(raw_evidence) + len(raw_candidates)
    merged = sum(1 for e in raw_evidence if 'same quote as' in e['why'])
    dropped_evidence = sum(1 for e in raw_evidence if e['status'] == '丢掉') - merged
    dropped_candidates = sum(1 for c in raw_candidates if c['status'] == '丢掉')
    kept_tiers = collections.Counter(e['tier'] for e in handover['evidence'])
    trace['kept'] = {'evidence': len(handover['evidence']), 'candidates': len(handover['candidates']), 'tiers': dict(kept_tiers)}
    # --- matching
    records = [dict(r) for r in views.execute('select call_no, shown_json, request_sha256, decisions_json, checks_json from match_records where input_id=? order by id', (input_id,))]
    match_calls = []
    for rec in records:
        decisions = json.loads(rec['decisions_json'] or '{}')
        checks = json.loads(rec['checks_json'] or '{}')
        shown_lists = json.loads(rec['shown_json'] or '{}')
        archive_row = archive.execute('select cost_usd, input_tokens, output_tokens, seconds from model_calls where request_sha256=?', (rec['request_sha256'],)).fetchone()
        cost = (archive_row['cost_usd'] or 0) if archive_row else 0
        trace['cost'] += cost
        match_calls.append({
            'call_no': rec['call_no'], 'cost': round(cost, 4), 'seconds': round(archive_row['seconds'] or 0, 1) if archive_row else None,
            'refusals': checks.get('refusals', []),
            'candidates': [{'id': d['id'], 'outcome': d['outcome'], 'target': d.get('target_view_id', ''), 'reason': trim(d.get('reason', ''), REASON_CHARS),
                            'dependencies': d.get('dependencies', []), 'offered': shown_lists.get('candidates', {}).get(d['id'], []),
                            'not_opened': checks.get('not_opened', {}).get(d['id'], '') if d['outcome'] != '不开' else ''}
                           for d in decisions.get('candidates', [])],
            'evidence': [{'id': d['id'], 'view': d.get('view_id', ''), 'outcome': d['outcome'], 'target': d.get('target_evidence_id', ''),
                          'said_day': d.get('said_day', ''), 'reason': trim(d.get('reason', ''), REASON_CHARS),
                          'offered': shown_lists.get('evidence', {}).get(f'{d["id"]}|{d.get("view_id", "")}', [])}
                         for d in decisions.get('evidence', [])],
        })
    trace['match_calls'] = match_calls
    accepted = match_outcomes(records)
    outcome_counts = collections.Counter()
    evidence_outcome_counts = collections.Counter()
    not_opened_reasons = []
    repeat_reasons = []
    pooled = 0
    for group, rec in accepted.items():
        decisions = json.loads(rec['decisions_json'] or '{}')
        code_not_opened = json.loads(rec['checks_json'] or '{}').get('not_opened', {})
        if group == 1:
            for d in decisions.get('candidates', []):
                if d['outcome'] == '新观点' and d['id'] in code_not_opened:      # the object is not on the research list: pooled as a suggested theme, not opened
                    outcome_counts['新观点→复核池（对象不在名单）'] += 1
                    pooled += 1
                    continue
                outcome_counts[d['outcome']] += 1
                if d['outcome'] == '不开':
                    not_opened_reasons.append(trim(d.get('reason', ''), REASON_CHARS))
        for d in decisions.get('evidence', []):
            evidence_outcome_counts[d['outcome']] += 1
            if d['outcome'] == '重复':
                repeat_reasons.append(trim(d.get('reason', ''), REASON_CHARS))
    trace['outcomes'] = dict(outcome_counts)
    trace['evidence_outcomes'] = dict(evidence_outcome_counts)
    trace['not_opened_reasons'] = not_opened_reasons
    trace['repeat_reasons'] = repeat_reasons
    trace['match_refused'] = sum(1 for m in match_calls if m['refusals'])
    # --- writing
    written_steps = [s for s in steps if s['step'] == 'written' and s['result'] == 'ok']
    written = json.loads(written_steps[-1]['reason']) if written_steps else {'changed': [], 'new': {}, 'notes': []}
    new_views = []
    for candidate_id, view_id in (written.get('new') or {}).items():
        view = views.execute('select * from views where view_id=?', (view_id,)).fetchone()
        rungs = [f'{r["label"]}：{r["condition"]}' for r in views.execute('select label, condition from rungs where view_id=? order by position', (view_id,))]
        if view:
            new_views.append({'candidate': candidate_id, 'view_id': view_id, 'object': view['object_id'], 'kind': view['kind'], 'looks_at': view['looks_at'],
                              'question': view['question'], 'due_day': view['due_day'], 'year': view['year'], 'rungs': rungs})
    stored_evidence = views.execute('select count(*) from evidence where created_from_input=?', (input_id,)).fetchone()[0]
    linked_existing = views.execute('select count(distinct evidence_id) from evidence_sources where input_id=? and evidence_id not in (select evidence_id from evidence where created_from_input=?)', (input_id, input_id)).fetchone()[0]
    not_stored = sum(1 for n in written.get('notes', []) if 'not stored' in n)
    trace['written'] = {'changed': written.get('changed', []), 'new_views': new_views, 'notes': [{'text': n, 'class': classify(n, NOTE_CLASSES, '其他')} for n in written.get('notes', [])],
                        'stored_evidence': stored_evidence, 'linked_existing': linked_existing}
    # --- the day's judging of the views this item changed
    judged = []
    watched = set(written.get('changed', [])) | {v['view_id'] for v in new_views}
    if watched:
        marks = ','.join('?' * len(watched))
        rows = views.execute(f'select view_id, seq, input_id, rung, changed, why_changed, reasons from judgements where (input_id=? or input_id=?) and view_id in ({marks}) order by judgement_id',
                             (input_id, f'day:{item["publication_day"]}', *sorted(watched)))
        for r in rows:
            judged.append({'view_id': r['view_id'], 'rung': r['rung'], 'changed': bool(r['changed']), 'why_changed': trim(r['why_changed'], REASON_CHARS), 'reasons': trim(r['reasons'], REASON_CHARS), 'by': '当天一轮' if r['input_id'].startswith('day:') else '这条之后'})
    trace['judged'] = judged
    # --- the diagnosis, by rule (stated on the page)
    repeats = evidence_outcome_counts['重复']
    noise = dropped_evidence + dropped_candidates + outcome_counts['不开'] + pooled + not_stored
    trace['noise'], trace['produced'], trace['repeats'] = noise, produced, repeats
    trace['noise_parts'] = {'代码丢的证据': dropped_evidence, '代码丢的候选观点': dropped_candidates, '比对判不开': outcome_counts['不开'],
                            '对象不在名单，进复核池': pooled, '证据没存（观点没开）': not_stored, '比对判重复（不计）': repeats, '同句合并（不计）': merged}
    if failed:
        trace['diagnosis'] = '失败'
        trace['diagnosis_why'] = f'{failed[-1]["step"]}：{trim(failed[-1]["reason"], 200)}'
    elif produced == 0:
        trace['diagnosis'] = '空手'
        trace['diagnosis_why'] = '模型一条证据、一条候选观点都没写'
    elif trace['kept']['evidence'] + trace['kept']['candidates'] == 0:
        main = collections.Counter([e['why_class'] for e in raw_evidence if e['status'] == '丢掉'] + [c['why_class'] for c in raw_candidates if c['status'] == '丢掉']).most_common(1)
        trace['diagnosis'] = '全被丢'
        trace['diagnosis_why'] = f'模型写了 {produced} 条，代码全丢；主要原因：{main[0][0] if main else "？"}'
    elif noise * 3 >= produced:
        parts = '，'.join(f'{k} {v}' for k, v in trace['noise_parts'].items() if v and '不计' not in k)
        trace['diagnosis'] = '杂音多'
        trace['diagnosis_why'] = f'写了 {produced} 条，杂音 {noise} 条（{parts}）'
    elif repeats and repeats * 2 >= trace['kept']['evidence']:
        trace['diagnosis'] = '多为重复'
        trace['diagnosis_why'] = f'留下 {trace["kept"]["evidence"]} 条证据，{repeats} 条比对判「重复」：库里已有同一句或同一个数，只加出处；抽取没错，是这篇在复述'
    else:
        trace['diagnosis'] = '正常'
        trace['diagnosis_why'] = f'写了 {produced} 条，杂音 {noise} 条；存了 {stored_evidence} 条证据，开了 {len(new_views)} 条观点，改了 {len(written.get("changed", []))} 条观点的读法'
    trace['cost'] = round(trace['cost'], 4)
    return trace


def route_reason_class(reason):
    """One row per kind of reason in the summary: the object list and the copied item's id vary per item."""
    reason = re.sub(r'（上游标的是.*', '', reason)
    reason = re.sub(r'^是 \S+ 的转载', '同一篇的转载', reason)
    return re.sub(r"这一类对 \[.*?\] 不看", '这一类对它讲的对象不看', reason)


def summarise(traces, from_day, until_day):
    processed = [t for t in traces if t['route'] == '进流程' and t.get('seq')]
    counter = collections.Counter
    summary = {
        'from': from_day, 'to': until_day, 'items': len(traces),
        'routes': dict(counter(t['route'] for t in traces)),
        'route_reasons': dict(counter(f'{t["route"]}：{route_reason_class(t["route_reason"])}' for t in traces if t['route'] != '进流程').most_common()),
        'unrun': sum(1 for t in traces if t['diagnosis'] == '未跑'),
        'processed': len(processed),
        'wrote_something': sum(1 for t in processed if t['produced']),
        'kept_something': sum(1 for t in processed if t['kept']['evidence'] + t['kept']['candidates']),
        'stored_something': sum(1 for t in processed if t['written']['stored_evidence'] or t['written']['new_views'] or t['written']['changed']),
        'diagnoses': dict(counter(t['diagnosis'] for t in processed)),
        'by_category': {}, 'by_publisher_type': {}, 'by_day': {},
        'drop_reasons': dict(counter(e['why_class'] for t in processed for e in t['raw_evidence'] if e['status'] == '丢掉').most_common()),
        'candidate_drop_reasons': dict(counter(c['why_class'] for t in processed for c in t['raw_candidates'] if c['status'] == '丢掉').most_common()),
        'outcomes': dict(sum((counter(t['outcomes']) for t in processed), counter())),
        'evidence_outcomes': dict(sum((counter(t['evidence_outcomes']) for t in processed), counter())),
        'tiers_kept': dict(sum((counter(t['kept']['tiers']) for t in processed), counter())),
        'produced': {'evidence': sum(len(t['raw_evidence']) for t in processed), 'candidates': sum(len(t['raw_candidates']) for t in processed)},
        'kept': {'evidence': sum(t['kept']['evidence'] for t in processed), 'candidates': sum(t['kept']['candidates'] for t in processed)},
        'stored_evidence': sum(t['written']['stored_evidence'] for t in processed),
        'new_views': sum(len(t['written']['new_views']) for t in processed),
        'not_opened': sum(len(t['not_opened_reasons']) for t in processed),
        'repeats': sum(len(t['repeat_reasons']) for t in processed),
        'match_refused_items': sum(1 for t in processed if t['match_refused']),
        'answer_mismatch': sum(1 for t in processed if not t.get('answer_matches_handover', True)),
        'cost': round(sum(t['cost'] for t in processed), 2),
        'notes': dict(counter(n['class'] for t in processed for n in t['written']['notes']).most_common()),
    }
    for key, field in (('by_category', 'category'), ('by_publisher_type', 'publisher_type'), ('by_day', 'day')):
        groups = collections.defaultdict(lambda: counter())
        for t in processed:
            groups[t[field]][t['diagnosis']] += 1
            groups[t[field]]['条数'] += 1
            groups[t[field]]['费用'] += t['cost']
        summary[key] = {k: {kk: (round(vv, 2) if kk == '费用' else vv) for kk, vv in v.items()} for k, v in sorted(groups.items())}
    return summary


PAGE = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>逐条抽取追踪</title>
<style>
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e2e2dd;--ok:#2d7a3a;--warn:#b26a00;--bad:#b3261e;--info:#2b5fa8;--tag:#eef0f3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,"PingFang SC","Noto Sans CJK SC",sans-serif}
main{max-width:1500px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:8px 0}
h2{font-size:17px;margin:24px 0 8px}
h3{font-size:14px;margin:14px 0 6px;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
.num{font-size:24px;font-weight:600}
.muted{color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:5px 7px;text-align:left;vertical-align:top}
th{background:#f0f0ec;white-space:nowrap}
#items > thead th{position:sticky;top:0;cursor:pointer;z-index:1}
td.n,th.n{text-align:right;white-space:nowrap}
.badge{display:inline-block;padding:1px 7px;border-radius:10px;font-size:12px;background:var(--tag);white-space:nowrap}
.b-正常{background:#dff3e3;color:var(--ok)} .b-杂音多{background:#fff1d6;color:var(--warn)} .b-全被丢,.b-失败{background:#fde0de;color:var(--bad)}
.b-空手{background:#e8e8e4;color:var(--muted)} .b-不处理,.b-合并,.b-未跑,.b-退回{background:#f1f1ee;color:var(--muted)} .b-多为重复{background:#e3ebf7;color:var(--info)}
.b-留下{background:#dff3e3;color:var(--ok)} .b-丢掉{background:#fde0de;color:var(--bad)}
.b-归入已有的{background:#e3ebf7;color:var(--info)} .b-接续{background:#e3ebf7;color:var(--info)} .b-新观点{background:#dff3e3;color:var(--ok)} .b-不开{background:#fff1d6;color:var(--warn)}
.b-新证据{background:#dff3e3;color:var(--ok)} .b-重复{background:#fff1d6;color:var(--warn)} .b-替代{background:#e3ebf7;color:var(--info)}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.filters select,.filters input{padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit}
tr.item{cursor:pointer} tr.item:hover{background:#fbfbf8}
tr.detail td{background:#fcfcfa;padding:10px 14px 16px}
.detail h4{margin:12px 0 4px;font-size:13px}
.quote{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#333;white-space:pre-wrap}
.small{font-size:12px}
ul{margin:4px 0;padding-left:18px}
a{color:var(--info)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:900px){.two{grid-template-columns:1fr}}
.rule{border-left:3px solid var(--line);padding-left:10px;margin:6px 0}
</style>
</head>
<body><main>
<h1>逐条抽取追踪 <span class="muted small" id="range"></span></h1>
<p class="muted">每一条信息走过的路：路由（进不进流程）→ 抽取（模型写了什么、代码丢了什么）→ 比对（候选观点去哪、证据算新还是重复）→ 入库（开了什么、改了什么）→ 当天重判。所有数字都从存下来的数据里数出来，没有再问模型。</p>
<div class="card small">
<b>诊断怎么打的（规则，不是人判）</b>
<div class="rule">「空手」：模型一条证据、一条候选观点都没写。</div>
<div class="rule">「全被丢」：模型写了，代码检查把每一条都丢了（原句不在原文、连到不存在的观点、梯子不对、季度数、年份超、到期日错、证据没了）。</div>
<div class="rule">「杂音多」：杂音 ≥ 写出来的三分之一。杂音 = 模型写了、但后面被扔掉的东西：代码丢的证据 + 代码丢的候选观点 + 比对判「不开」的候选观点 + 对象不在研究名单上、只能进复核池的候选观点 + 因为观点没开而没存的证据。同一句写两次只合并，不算杂音。</div>
<div class="rule">「多为重复」：留下的证据里一半以上被比对判「重复」（库里已有同一句或同一个数，只加一个出处）。这不是抽取写了废话，是这篇在复述别处已经说过的话；单独标出来，免得和杂音混在一起。</div>
<div class="rule">「正常」：其余。<b>这个规则只看流程里能数的东西</b>；存进去的证据本身讲的是不是正事（trivia 还是关键数），要你点开看。</div>
</div>
<section id="summary"></section>
<h2>每一条</h2>
<div class="filters" id="filters"></div>
<div class="muted small" id="count"></div>
<table id="items"><thead><tr>
<th data-k="day">日期</th><th data-k="category">类别</th><th data-k="publisher">来源</th><th data-k="objects">对象</th><th data-k="title">标题</th>
<th class="n" data-k="produced" title="模型写了几条证据 / 几条候选观点">写了 证/观</th><th class="n" data-k="kept" title="代码检查后留下几条">留下 证/观</th>
<th data-k="outcomes" title="候选观点：归入 / 接续 / 新 / 不开；证据：新 / 重复 / 替代">比对</th><th class="n" data-k="stored" title="存了几条证据 / 开了几条观点 / 改了几条观点">入库 证/开/改</th>
<th data-k="diagnosis">诊断</th><th class="n" data-k="cost">费用$</th>
</tr></thead><tbody id="rows"></tbody></table>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const S = DATA.summary, ITEMS = DATA.items;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const badge = s => `<span class="badge b-${esc(s)}">${esc(s)}</span>`;
document.getElementById('range').textContent = `${S.from} 到 ${S.to}`;
function table(rows, head){ return `<table><thead><tr>${head.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map((c,i)=>`<td class="${typeof c==='number'?'n':''}">${typeof c==='number'?c:c}</td>`).join('')}</tr>`).join('')}</tbody></table>`; }
function kv(obj, label1, label2){ return table(Object.entries(obj).sort((a,b)=>b[1]-a[1]).map(([k,v])=>[esc(k), v]), [label1, label2]); }
function groupTable(groups, label){
  const diag = ['正常','多为重复','杂音多','全被丢','空手','失败'];
  return table(Object.entries(groups).map(([k,v])=>[esc(k), v['条数']||0, ...diag.map(d=>v[d]||0), v['费用']||0]), [label,'条数',...diag,'费用$']);
}
(function renderSummary(){
  const el = document.getElementById('summary');
  const funnel = [
    ['语料里这段日子的条目', S.items],
    ['路由进流程的', (S.routes['进流程']||0)],
    ['其中真的跑了的（启动期只跑 NVDA）', S.processed],
    ['模型写了东西的', S.wrote_something],
    ['代码检查后还留下东西的', S.kept_something],
    ['比对后写进库的（存了证据、开了或改了观点）', S.stored_something],
  ];
  el.innerHTML = `
  <h2>总览</h2>
  <div class="cards">${funnel.map(([k,v])=>`<div class="card"><div class="num">${v}</div><div class="muted small">${esc(k)}</div></div>`).join('')}</div>
  <div class="two">
    <div class="card"><h3>没进流程的，为什么</h3>${kv(S.route_reasons,'原因','条数')}<p class="small muted">「未跑」${S.unrun} 条：启动期（窗口开始前）只跑了 NVDA。</p></div>
    <div class="card"><h3>跑了的 ${S.processed} 条，诊断</h3>${kv(S.diagnoses,'诊断','条数')}<p class="small muted">费用合计 $${S.cost}（抽取 + 比对，按买答案时的价）。比对被代码退回过的条目 ${S.match_refused_items}；答案和交接记录对不上的 ${S.answer_mismatch}。</p></div>
  </div>
  <div class="two">
    <div class="card"><h3>模型写了多少，留下多少</h3>${table([
      ['证据', S.produced.evidence, S.kept.evidence, S.stored_evidence],
      ['候选观点', S.produced.candidates, S.kept.candidates, S.new_views]], ['', '模型写了', '代码留下', '最后入库'])}
      <p class="small muted">入库的证据少于留下的：比对判「重复」的 ${S.repeats} 条只加出处，不新存；候选观点归入已有观点的也不开新的。</p></div>
    <div class="card"><h3>比对的结果</h3><div class="two">${kv(S.outcomes,'候选观点去哪','条数')}${kv(S.evidence_outcomes,'证据算什么（一条证据连几条观点就判几次）','次数')}</div></div>
  </div>
  <div class="two">
    <div class="card"><h3>代码为什么丢证据</h3>${kv(S.drop_reasons,'原因','条数')}</div>
    <div class="card"><h3>代码为什么丢候选观点</h3>${kv(S.candidate_drop_reasons,'原因','条数')}<h3>入库时的备注</h3>${kv(S.notes,'备注','条数')}</div>
  </div>
  <div class="card"><h3>留下的证据，来源分四层</h3>${kv(S.tiers_kept,'层','条数')}</div>
  <div class="card"><h3>按类别</h3>${groupTable(S.by_category,'类别')}</div>
  <div class="card"><h3>按来源类型</h3>${groupTable(S.by_publisher_type,'来源类型')}</div>
  <div class="card"><h3>按日</h3>${groupTable(S.by_day,'日期')}</div>`;
})();
const state = {day:'', category:'', ptype:'', diag:'', object:'', q:'', sort:'day', dir:1};
(function renderFilters(){
  const el = document.getElementById('filters');
  const opts = (vals, label) => `<option value="">${label}：全部</option>` + [...new Set(vals)].sort().map(v=>`<option>${esc(v)}</option>`).join('');
  el.innerHTML = `
  <select id="f-day">${opts(ITEMS.map(i=>i.day),'日期')}</select>
  <select id="f-category">${opts(ITEMS.map(i=>i.category),'类别')}</select>
  <select id="f-ptype">${opts(ITEMS.map(i=>i.publisher_type),'来源类型')}</select>
  <select id="f-diag">${opts(ITEMS.map(i=>i.diagnosis),'诊断')}</select>
  <select id="f-object">${opts(ITEMS.flatMap(i=>i.objects),'对象')}</select>
  <input id="f-q" placeholder="搜标题 / 来源 / 编号" size="28">
  <label class="small"><input type="checkbox" id="f-noise"> 只看杂音≥1 的</label>`;
  for (const [id,key] of [['f-day','day'],['f-category','category'],['f-ptype','ptype'],['f-diag','diag'],['f-object','object']])
    document.getElementById(id).onchange = e => { state[key]=e.target.value; renderRows(); };
  document.getElementById('f-q').oninput = e => { state.q=e.target.value.toLowerCase(); renderRows(); };
  document.getElementById('f-noise').onchange = e => { state.noise=e.target.checked; renderRows(); };
  document.querySelectorAll('#items th[data-k]').forEach(th => th.onclick = () => { const k=th.dataset.k; if(state.sort===k) state.dir*=-1; else {state.sort=k; state.dir=1;} renderRows(); });
})();
const sortKey = (i,k) => ({day:i.day+i.seq, category:i.category, publisher:i.publisher, objects:i.objects.join(), title:i.title,
  produced:i.produced||0, kept:(i.kept?i.kept.evidence+i.kept.candidates:0), outcomes:Object.values(i.outcomes||{}).reduce((a,b)=>a+b,0),
  stored:(i.written?i.written.stored_evidence+i.written.new_views.length:0), diagnosis:i.diagnosis, cost:i.cost||0})[k];
function renderRows(){
  let rows = ITEMS.filter(i => (!state.day||i.day===state.day)&&(!state.category||i.category===state.category)&&(!state.ptype||i.publisher_type===state.ptype)
    &&(!state.diag||i.diagnosis===state.diag)&&(!state.object||i.objects.includes(state.object))&&(!state.noise||(i.noise||0)>=1)
    &&(!state.q||(i.title+' '+i.publisher+' '+i.id).toLowerCase().includes(state.q)));
  rows.sort((a,b)=>{const x=sortKey(a,state.sort), y=sortKey(b,state.sort); return (x>y?1:x<y?-1:0)*state.dir;});
  document.getElementById('count').textContent = `${rows.length} 条（点一行展开）`;
  document.getElementById('rows').innerHTML = rows.map((i,n)=>{
    const o=i.outcomes||{}, eo=i.evidence_outcomes||{};
    const outcomes = i.route!=='进流程'||!i.seq ? '' : `${o['归入已有的']||0}/${o['接续']||0}/${o['新观点']||0}/${o['不开']||0} · ${eo['新证据']||0}/${eo['重复']||0}/${eo['替代']||0}`;
    return `<tr class="item" data-id="${esc(i.id)}"><td>${esc(i.day)}</td><td>${esc(i.category)}</td><td>${esc(i.publisher)}<div class="muted small">${esc(i.publisher_type)}</div></td>
    <td>${i.objects.map(esc).join(' ')}</td><td>${esc(i.title)||'<span class="muted">（无标题）</span>'}<div class="muted small">${esc(i.id)}</div></td>
    <td class="n">${i.seq?`${i.raw_evidence.length}/${i.raw_candidates.length}`:''}</td><td class="n">${i.seq?`${i.kept.evidence}/${i.kept.candidates}`:''}</td>
    <td class="small">${outcomes}</td><td class="n">${i.seq?`${i.written.stored_evidence}/${i.written.new_views.length}/${i.written.changed.length}`:''}</td>
    <td>${badge(i.diagnosis)}</td><td class="n">${i.cost?i.cost.toFixed(3):''}</td></tr>`;
  }).join('');
  document.querySelectorAll('tr.item').forEach(tr => tr.onclick = () => toggle(tr));
}
function toggle(tr){
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('detail')) { next.remove(); return; }
  const i = ITEMS.find(x => x.id === tr.dataset.id);
  const d = document.createElement('tr'); d.className='detail';
  d.innerHTML = `<td colspan="11"><div class="detail">${detail(i)}</div></td>`;
  tr.after(d);
}
function detail(i){
  const files = `<a href="text/${i.slug}.txt" target="_blank">原文全文</a>` + (i.seq?` · <a href="request/${i.slug}.txt" target="_blank">给模型的完整请求</a> · <a href="answer/${i.slug}.json" target="_blank">模型原始答案</a>`:'') + (i.uri?` · <a href="${esc(i.uri)}" target="_blank">来源链接</a>`:'');
  let out = `<div><b>诊断：</b>${badge(i.diagnosis)} ${esc(i.diagnosis_why)}</div><div class="small muted">${files} · 原文 ${i.chars} 字</div><div class="quote small" style="margin:6px 0">${esc(i.excerpt)}</div>`;
  out += `<h4>① 路由</h4><div>${esc(i.route)}${i.route_reason?'：'+esc(i.route_reason):'：对象在名单上，这一类在看，进流程'}</div>`;
  if (!i.seq) return out;
  const c = i.extract_call||{};
  out += `<h4>② 抽取</h4><div class="small muted">模型 ${esc(c.model)}，请求 ${c.prompt_chars} 字，输入 ${c.input_tokens} / 输出 ${c.output_tokens} tokens，${c.seconds} 秒，$${c.cost}${c.candidates_of_item>1?`（档案里这条有 ${c.candidates_of_item} 次抽取调用，取「抽取完成」那一刻之前最后一次）`:''}${i.answer_matches_handover===false?' <b style="color:var(--bad)">答案和交接记录对不上</b>':''}</div>`;
  out += `<div class="small"><b>给模型看的已有观点（${i.shown_views.length}）</b>${i.shown_views.length?`<ul>${i.shown_views.map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`:'：还没有，该开的都写成候选观点'}</div>`;
  out += `<div><b>模型写的证据（${i.raw_evidence.length}）</b></div>` + (i.raw_evidence.length ? table(i.raw_evidence.map(e=>[esc(e.id), badge(e.status)+(e.why?`<div class="small muted">${esc(e.why_class)}<br>${esc(e.why)}</div>`:''), esc(e.tier), esc(e.speaker)+(e.original_who?`<div class="small muted">转述 ${esc(e.original_who)} ${esc(e.original_day)}</div>`:''), `<div class="quote">${esc(e.quote)}</div><div>${esc(e.one_line)}</div>`, e.links.map(esc).join(' ')]), ['编号','结果','层','谁说的','原句 / 一句话','连到']) : '<div class="muted small">没有</div>');
  out += `<div style="margin-top:8px"><b>模型写的候选观点（${i.raw_candidates.length}）</b></div>` + (i.raw_candidates.length ? table(i.raw_candidates.map(k=>[esc(k.id), badge(k.status)+(k.why?`<div class="small muted">${esc(k.why_class)}<br>${esc(k.why)}</div>`:''), `${esc(k.kind)}<div class="small muted">${esc(k.object)} · ${esc(k.year)} · 到期 ${esc(k.due_day)}</div>`, `<b>${esc(k.question)}</b><div class="small muted">看的是「${esc(k.looks_at)}」</div><ol class="small" style="margin:2px 0;padding-left:18px">${k.rungs.map(r=>`<li>${esc(r)}</li>`).join('')}</ol>`, k.evidence_ids.map(esc).join(' ')]), ['编号','结果','种类','问题 / 梯子','证据']) : '<div class="muted small">没有</div>');
  out += `<h4>③ 比对</h4>`;
  if (!i.match_calls.length) out += `<div class="muted small">没到比对：抽取后没有留下的东西</div>`;
  for (const m of i.match_calls){
    out += `<div class="small muted">第 ${m.call_no} 次调用（${m.call_no<=2?'候选观点 + 直连已有观点的证据':'归入已有观点后的证据再比一次'}），$${m.cost}，${m.seconds} 秒${m.refusals.length?` · <b style="color:var(--bad)">代码退回</b>：${m.refusals.map(esc).join('；')}`:''}</div>`;
    if (m.candidates.length) out += table(m.candidates.map(k=>[esc(k.id), badge(k.outcome)+(k.target?` → ${esc(k.target)}`:'')+(k.not_opened?`<div class="small" style="color:var(--warn)">代码没开：对象不在研究名单上，进复核池当建议主题</div>`:''),`<span class="small muted">给它比的已有观点：${k.offered.length?k.offered.map(esc).join(' '):'没有'}</span>`+(k.dependencies.length?`<div class="small muted">依赖：${k.dependencies.map(d=>esc(d.view_id)+(d.direction?`（${esc(d.direction)}）`:'')+(d.wait_chain_view_id?`，等 ${esc(d.wait_chain_view_id)} ${esc(d.wait_year)}`:'')).join('；')}</div>`:''), esc(k.reason)]), ['候选','去哪','比对清单','模型的理由']);
    if (m.evidence.length) out += table(m.evidence.map(e=>[esc(e.id)+' → '+esc(e.view), badge(e.outcome)+(e.target?` 对 ${esc(e.target)}`:'')+(e.said_day?` 说于 ${esc(e.said_day)}`:''), `<span class="small muted">给它比的已有证据：${e.offered.length?e.offered.map(esc).join(' '):'没有'}</span>`, esc(e.reason)]), ['证据 → 观点','算什么','比对清单','模型的理由']);
  }
  const w = i.written;
  out += `<h4>④ 入库</h4><div class="small">存了 ${w.stored_evidence} 条新证据，另有 ${w.linked_existing} 条已有证据加了这条出处；开了 ${w.new_views.length} 条观点；改了读法的观点：${w.changed.length?w.changed.map(esc).join(' '):'无'}</div>`;
  if (w.new_views.length) out += table(w.new_views.map(v=>[`${esc(v.candidate)} → <b>${esc(v.view_id)}</b>`, `${esc(v.kind)}<div class="small muted">${esc(v.object)} · ${esc(v.year)} · 到期 ${esc(v.due_day)}</div>`, `<b>${esc(v.question)}</b><div class="small muted">看的是「${esc(v.looks_at)}」</div><ol class="small" style="margin:2px 0;padding-left:18px">${v.rungs.map(r=>`<li>${esc(r)}</li>`).join('')}</ol>`]), ['候选 → 观点','种类','问题 / 梯子']);
  if (w.notes.length) out += `<ul class="small">${w.notes.map(n=>`<li>${esc(n.class)}：<span class="muted">${esc(n.text)}</span></li>`).join('')}</ul>`;
  out += `<h4>⑤ 重判</h4>` + (i.judged.length ? table(i.judged.map(j=>[esc(j.view_id), `第 ${j.rung} 格`, j.changed?'<b>变了</b>':'没变', esc(j.by), `<div>${esc(j.why_changed)}</div><div class="small muted">${esc(j.reasons)}</div>`]), ['观点','判在','变没变','哪一轮','为什么']) : `<div class="muted small">${w.changed.length||w.new_views.length?'这条改的观点在当天那一轮没有被判（当天没有重判记录）':'这条没改任何观点的读法，不用重判'}</div>`);
  return out;
}
renderRows();
</script>
</body></html>
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--from', dest='from_day', default='2026-02-25')
    parser.add_argument('--to', dest='until_day', default='2026-08-15')
    parser.add_argument('--window-start', default='2026-07-24', help='first day of the full window; before it only NVDA was run')
    parser.add_argument('--out', default=os.path.join(ROOT, 'poc', 'reports', datetime.date.today().isoformat(), 'trace'))
    args = parser.parse_args()
    for sub in ('', 'text', 'request', 'answer'):
        os.makedirs(os.path.join(args.out, sub), exist_ok=True)
    items_db = testdb.open_db(args.items)
    views = open_read_only(args.views)
    archive = open_read_only(args.archive)
    uni = universe_module.load(args.universe)
    archive_calls = load_extract_calls(archive)
    traces = []
    for item in testdb.feed(items_db, args.from_day, args.until_day):
        traces.append(build_item_trace(item, uni, views, archive_calls, archive, os.path.join(args.out, 'text'), os.path.join(args.out, 'request'),
                                       os.path.join(args.out, 'answer'), args.window_start))
    summary = summarise(traces, args.from_day, args.until_day)
    processed_ids = {t['id'] for t in traces if t.get('seq')}
    recorded = {r[0] for r in views.execute("select distinct input_id from processing_steps where sequence_no>0 and input_id not like 'day:%' and publication_day between ? and ?", (args.from_day, args.until_day))}
    summary['recorded_but_not_in_feed'] = sorted(recorded - processed_ids)
    page = PAGE.replace('__DATA__', json.dumps({'summary': summary, 'items': traces}, ensure_ascii=False).replace('</', '<\\/'))
    if SECRET.search(page):
        raise SystemExit('a credential-looking string would be written; refusing')
    with open(os.path.join(args.out, 'index.html'), 'w', encoding='utf-8') as handle:
        handle.write(page)
    print(f'items {summary["items"]}  routes {summary["routes"]}  processed {summary["processed"]}  diagnoses {summary["diagnoses"]}')
    print(f'produced {summary["produced"]}  kept {summary["kept"]}  stored evidence {summary["stored_evidence"]}  new views {summary["new_views"]}  cost ${summary["cost"]}')
    print(f'answer/handover mismatches {summary["answer_mismatch"]}  recorded but not in feed {len(summary["recorded_but_not_in_feed"])}')
    print('written', os.path.join(args.out, 'index.html'), f'({os.path.getsize(os.path.join(args.out, "index.html")) // 1024} KB)')


if __name__ == '__main__':
    main()
