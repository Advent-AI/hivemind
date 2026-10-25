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
from hivemind import dispatch, extraction, testdb, universe as universe_module, vocabulary  # noqa: E402

# stored requests of both prompt languages (D163): Chinese headers up to extraction v5, English from v6
ITEM_ID = re.compile(r'【信息】编号 (\S+?)，类别 |\[Item\] id (\S+?), category ')
ITEM_HEADER = re.compile(r'【信息】|\[Item\]')
BLOCK5_LINE = re.compile(r'^\s+- (v\d+)\s?[（(](.*)$', re.M)
# a key is "sk-" (not the tail of "musk-" or "sk-hynix-…") followed by an unbroken run of 20+ letters and digits
# that holds a digit; URL slugs are hyphen-separated words and never match
SECRET = re.compile(r'(?<![A-Za-z0-9])sk-(?:[A-Za-z0-9_\-]*?)(?=[A-Za-z0-9_]{20,})(?=[A-Za-z_]*\d)[A-Za-z0-9_]{20,}|Bearer\s+(?=[A-Za-z0-9_\-\.]*\d)[A-Za-z0-9_\-\.]{20,}')
QUOTE_CHARS = 400
REASON_CHARS = 400

DROP_CLASSES = [
    ('quote not in item', 'quote not in the source text (the model changed or invented words)'),
    ('links to nothing shown', 'linked to a thesis id that does not exist'),
    ('same quote as', 'the same sentence written twice (merged into one; not noise)'),
    ('candidate ladder', 'ladder malformed (rung count, labels or bounds)'),
    ('quarterly number', 'a quarterly figure proposed as a thesis (rule: quarterly figures are evidence)'),
    ('is beyond next year', 'year beyond next year (rule: not opened)'),
    ('due_day not a date', 'due day is not a date'),
    ('not after the item', 'due day not after the publication day'),
    ('candidate without surviving evidence', 'all of the candidate\'s evidence was dropped, so the candidate went too'),
    ('invalid period', 'period is not a valid date span'),
]
NOTE_CLASSES = [
    ('linked to nothing kept; not stored', 'evidence linked only to a candidate that did not open; not stored'),
    ('late older statement', 'an older statement arriving late; not linked'),
    ('that candidate was not opened', 'dependency on a candidate that did not open; dropped'),
    ('cycle', 'dependency would form a cycle; dropped'),
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
        return classify(why, DROP_CLASSES, 'other')
    if not links:
        return 'no links written (linked to no thesis)'
    if set(links) & dropped_candidate_ids:
        return 'linked to a candidate the code dropped, so the evidence went too'
    if any(re.fullmatch(r'c\d+', link) and link not in answer_candidate_ids for link in links):
        return 'linked to a candidate id the model never wrote'
    if any(re.fullmatch(r'v\d+', link) and link not in shown_ids for link in links):
        return 'linked to a thesis id it was not shown (another object\'s, or invented)'
    return 'linked to a thesis id that does not exist'


def slug_of(input_id):
    return hashlib.sha1(input_id.encode('utf-8')).hexdigest()[:12]


def trim(text, limit):
    text = text or ''
    return text if len(text) <= limit else text[:limit] + '…'


def route_offline(item, uni):
    """dispatch.route without its writes: the same three questions, in plain words."""
    missing = [field for field in dispatch.REQUIRED if not item.get(field)]
    if missing:
        return 'returned', f'missing fields {missing}'
    if item.get('copy_of'):
        return 'merged', f'a copy of {item["copy_of"]}'
    if item.get('supersedes'):
        return 'not_processed', 'a correction (not supported in the POC)'
    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
    if not objects:
        labelled = [o['value'] for o in item['object_identifiers']]
        return 'not_processed', f'object not on the research list (upstream labelled {labelled or "nothing"})'
    if not any(uni.watches(o, item['category']) for o in objects):
        return 'not_processed', f'category {item["category"]} is not watched for {objects}'
    return 'in_pipeline', ''


def load_extract_calls(archive):
    """Every stored extraction call keyed by the item it was about, parsed from the request's item header (either language)."""
    calls = collections.defaultdict(list)
    rows = archive.execute("select call_id, config_version, model, request_json, answer_json, prompt_chars, input_tokens, output_tokens, "
                           "cost_usd, seconds, created_at from model_calls where purpose='extract' and request_sha256 not like '%:%'")
    for row in rows:
        request = json.loads(row['request_json'])
        user = request['messages'][1]['content']
        found = ITEM_ID.search(user)
        if not found:
            continue
        calls[found.group(1) or found.group(2)].append(dict(row, system=request['messages'][0]['content'], user=user))
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
    if route_kind != 'in_pipeline':
        trace['diagnosis'] = route_kind
        trace['diagnosis_why'] = route_reason
        return trace
    if not steps:
        trace['diagnosis'] = 'not_run'
        trace['diagnosis_why'] = 'the seed period (before %s) ran NVDA material only' % window_start if item['publication_day'] < window_start else 'no processing record'
        return trace
    trace['seq'] = max(s['sequence_no'] for s in steps)
    failed = [s for s in steps if s['result'] == 'failed'] if steps[-1]['result'] == 'failed' else []      # an item resumed after a failure is judged by its last step
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
        for view_id, rest in BLOCK5_LINE.findall(ITEM_HEADER.split(call['user'])[0]):
            shown.append(f'{view_id} ({rest}')
        trace['extract_call'] = {'model': call['model'], 'prompt_chars': call['prompt_chars'], 'input_tokens': call['input_tokens'],
                                 'output_tokens': call['output_tokens'], 'seconds': round(call['seconds'] or 0, 1), 'cost': round(call['cost_usd'] or 0, 4),
                                 'config': call['config_version'], 'candidates_of_item': len(archive_calls.get(input_id, []))}
        trace['cost'] += call['cost_usd'] or 0
        with open(os.path.join(request_dir, slug + '.txt'), 'w', encoding='utf-8') as handle:
            handle.write('=== system ===\n' + call['system'] + '\n\n=== user ===\n' + call['user'])
        with open(os.path.join(answer_dir, slug + '.json'), 'w', encoding='utf-8') as handle:
            json.dump(answer, handle, ensure_ascii=False, indent=1)
    trace['shown_views'] = shown
    shown_ids = {line.split(' (')[0] for line in shown}
    answer_candidate_ids = {c['id'] for c in answer.get('candidates', [])}
    dropped_candidate_ids = answer_candidate_ids - kept_candidate_ids
    raw_evidence = []
    for e in answer.get('evidence', []):
        if e['id'] in kept_evidence_ids:
            status, why, why_class = 'kept', '', ''
        elif e['id'] in dropped:
            status, why = 'dropped', dropped[e['id']]
            why_class = evidence_drop_class(why, e['links'], shown_ids, answer_candidate_ids, dropped_candidate_ids)
        else:
            status, why, why_class = 'dropped', 'kept at first, then left with no thesis to link to (its candidate was dropped)', 'linked to a candidate the code dropped, so the evidence went too'
        raw_evidence.append({'id': e['id'], 'tier': vocabulary.canonical('tier', e['tier']), 'speaker': e['speaker'], 'original_who': e.get('original_who', ''),
                             'original_day': e.get('original_day', ''), 'quote': trim(e['quote'], QUOTE_CHARS), 'one_line': e['one_line'],
                             'links': e['links'], 'status': status, 'why': why, 'why_class': why_class})
    raw_candidates = []
    for c in answer.get('candidates', []):
        if c['id'] in kept_candidate_ids:
            status, why = 'kept', ''
        else:
            status, why = 'dropped', dropped.get(c['id'], '')
        raw_candidates.append({'id': c['id'], 'kind': vocabulary.canonical('kind', c['kind']), 'object': c['object'], 'looks_at': c['looks_at'], 'question': c['question'],
                               'rungs': [f'{vocabulary.canonical("label", r["label"])}: {r["condition"]}' for r in c['rungs']], 'due_day': c['due_day'], 'year': c['year'],
                               'evidence_ids': c['evidence_ids'], 'status': status, 'why': why,
                               'why_class': classify(why, DROP_CLASSES, 'other') if status == 'dropped' else ''})
    trace['raw_evidence'], trace['raw_candidates'] = raw_evidence, raw_candidates
    produced = len(raw_evidence) + len(raw_candidates)
    merged = sum(1 for e in raw_evidence if 'same quote as' in e['why'])
    dropped_evidence = sum(1 for e in raw_evidence if e['status'] == 'dropped') - merged
    dropped_candidates = sum(1 for c in raw_candidates if c['status'] == 'dropped')
    kept_tiers = collections.Counter(vocabulary.canonical('tier', e['tier']) for e in handover['evidence'])
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
            'candidates': [{'id': d['id'], 'outcome': vocabulary.canonical('candidate_outcome', d['outcome']), 'target': d.get('target_view_id', ''), 'reason': trim(d.get('reason', ''), REASON_CHARS),
                            'dependencies': [dict(x, direction=vocabulary.canonical('direction', x.get('direction'))) for x in d.get('dependencies', [])], 'offered': shown_lists.get('candidates', {}).get(d['id'], []),
                            'not_opened': checks.get('not_opened', {}).get(d['id'], '') if vocabulary.canonical('candidate_outcome', d['outcome']) != 'skip' else ''}
                           for d in decisions.get('candidates', [])],
            'evidence': [{'id': d['id'], 'view': d.get('view_id', ''), 'outcome': vocabulary.canonical('evidence_outcome', d['outcome']), 'target': d.get('target_evidence_id', ''),
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
                outcome = vocabulary.canonical('candidate_outcome', d['outcome'])
                if outcome == 'new' and d['id'] in code_not_opened:      # the object is not on the research list: pooled as a suggested theme, not opened
                    outcome_counts['new → review pool (object not on the list)'] += 1
                    pooled += 1
                    continue
                outcome_counts[outcome] += 1
                if outcome == 'skip':
                    not_opened_reasons.append(trim(d.get('reason', ''), REASON_CHARS))
        for d in decisions.get('evidence', []):
            outcome = vocabulary.canonical('evidence_outcome', d['outcome'])
            evidence_outcome_counts[outcome] += 1
            if outcome == 'repeat':
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
        rungs = [f'{vocabulary.canonical("label", r["label"])}: {r["condition"]}' for r in views.execute('select label, condition from rungs where view_id=? order by position', (view_id,))]
        if view:
            new_views.append({'candidate': candidate_id, 'view_id': view_id, 'object': view['object_id'], 'kind': vocabulary.canonical('kind', view['kind']), 'looks_at': view['looks_at'],
                              'question': view['question'], 'due_day': view['due_day'], 'year': view['year'], 'rungs': rungs})
    stored_evidence = views.execute('select count(*) from evidence where created_from_input=?', (input_id,)).fetchone()[0]
    linked_existing = views.execute('select count(distinct evidence_id) from evidence_sources where input_id=? and evidence_id not in (select evidence_id from evidence where created_from_input=?)', (input_id, input_id)).fetchone()[0]
    not_stored = sum(1 for n in written.get('notes', []) if 'not stored' in n)
    trace['written'] = {'changed': written.get('changed', []), 'new_views': new_views, 'notes': [{'text': n, 'class': classify(n, NOTE_CLASSES, 'other')} for n in written.get('notes', [])],
                        'stored_evidence': stored_evidence, 'linked_existing': linked_existing}
    # --- the day's judging of the views this item changed
    judged = []
    watched = set(written.get('changed', [])) | {v['view_id'] for v in new_views}
    if watched:
        marks = ','.join('?' * len(watched))
        rows = views.execute(f'select view_id, seq, input_id, rung, changed, why_changed, reasons from judgements where (input_id=? or input_id=?) and view_id in ({marks}) order by judgement_id',
                             (input_id, f'day:{item["publication_day"]}', *sorted(watched)))
        for r in rows:
            judged.append({'view_id': r['view_id'], 'rung': r['rung'], 'changed': bool(r['changed']), 'why_changed': trim(r['why_changed'], REASON_CHARS), 'reasons': trim(r['reasons'], REASON_CHARS), 'by': 'the day\'s round' if r['input_id'].startswith('day:') else 'after this item'})
    trace['judged'] = judged
    # --- the diagnosis, by rule (stated on the page)
    repeats = evidence_outcome_counts['repeat']
    noise = dropped_evidence + dropped_candidates + outcome_counts['skip'] + pooled + not_stored
    trace['noise'], trace['produced'], trace['repeats'] = noise, produced, repeats
    trace['noise_parts'] = {'evidence dropped by code': dropped_evidence, 'candidates dropped by code': dropped_candidates, 'candidates matching skipped': outcome_counts['skip'],
                            'object not on the list, pooled': pooled, 'evidence not stored (thesis not opened)': not_stored, 'matching repeats (not counted)': repeats, 'same-sentence merges (not counted)': merged}
    if failed:
        trace['diagnosis'] = 'failed'
        trace['diagnosis_why'] = f'{failed[-1]["step"]}: {trim(failed[-1]["reason"], 200)}'
    elif produced == 0:
        trace['diagnosis'] = 'empty_handed'
        trace['diagnosis_why'] = 'the model wrote no evidence and no candidate thesis'
    elif trace['kept']['evidence'] + trace['kept']['candidates'] == 0:
        main = collections.Counter([e['why_class'] for e in raw_evidence if e['status'] == 'dropped'] + [c['why_class'] for c in raw_candidates if c['status'] == 'dropped']).most_common(1)
        trace['diagnosis'] = 'all_dropped'
        trace['diagnosis_why'] = f'the model wrote {produced} items and the code dropped every one; main reason: {main[0][0] if main else "?"}'
    elif noise * 3 >= produced:
        parts = ', '.join(f'{k} {v}' for k, v in trace['noise_parts'].items() if v and 'not counted' not in k)
        trace['diagnosis'] = 'noisy'
        trace['diagnosis_why'] = f'{produced} written, {noise} noise ({parts})'
    elif repeats and repeats * 2 >= trace['kept']['evidence']:
        trace['diagnosis'] = 'mostly_repeats'
        trace['diagnosis_why'] = f'{trace["kept"]["evidence"]} evidence items kept, {repeats} judged repeats by matching: the library already holds the same sentence or number and only gains a source; extraction is right, the article retells'
    else:
        trace['diagnosis'] = 'normal'
        trace['diagnosis_why'] = f'{produced} written, {noise} noise; {stored_evidence} evidence items stored, {len(new_views)} theses opened, the reading of {len(written.get("changed", []))} theses changed'
    trace['cost'] = round(trace['cost'], 4)
    return trace


def route_reason_class(reason):
    """One row per kind of reason in the summary: the object list and the copied item's id vary per item."""
    reason = re.sub(r' \(upstream labelled.*', '', reason)
    reason = re.sub(r'^a copy of \S+', 'a copy of another item', reason)
    return re.sub(r"category (\S+) is not watched for \[.*?\]", r'category \1 is not watched for its objects', reason)


def summarise(traces, from_day, until_day):
    processed = [t for t in traces if t['route'] == 'in_pipeline' and t.get('seq')]
    counter = collections.Counter
    summary = {
        'from': from_day, 'to': until_day, 'items': len(traces),
        'routes': dict(counter(t['route'] for t in traces)),
        'route_reasons': dict(counter(f'{t["route"]}: {route_reason_class(t["route_reason"])}' for t in traces if t['route'] != 'in_pipeline').most_common()),
        'unrun': sum(1 for t in traces if t['diagnosis'] == 'not_run'),
        'processed': len(processed),
        'wrote_something': sum(1 for t in processed if t['produced']),
        'kept_something': sum(1 for t in processed if t['kept']['evidence'] + t['kept']['candidates']),
        'stored_something': sum(1 for t in processed if t['written']['stored_evidence'] or t['written']['new_views'] or t['written']['changed']),
        'diagnoses': dict(counter(t['diagnosis'] for t in processed)),
        'by_category': {}, 'by_publisher_type': {}, 'by_day': {},
        'drop_reasons': dict(counter(e['why_class'] for t in processed for e in t['raw_evidence'] if e['status'] == 'dropped').most_common()),
        'candidate_drop_reasons': dict(counter(c['why_class'] for t in processed for c in t['raw_candidates'] if c['status'] == 'dropped').most_common()),
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
            groups[t[field]]['items'] += 1
            groups[t[field]]['cost'] += t['cost']
        summary[key] = {k: {kk: (round(vv, 2) if kk == 'cost' else vv) for kk, vv in v.items()} for k, v in sorted(groups.items())}
    return summary


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Item-by-item extraction trace</title>
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
.b-normal{background:#dff3e3;color:var(--ok)} .b-noisy{background:#fff1d6;color:var(--warn)} .b-all_dropped,.b-failed{background:#fde0de;color:var(--bad)}
.b-empty_handed{background:#e8e8e4;color:var(--muted)} .b-not_processed,.b-merged,.b-not_run,.b-returned{background:#f1f1ee;color:var(--muted)} .b-mostly_repeats{background:#e3ebf7;color:var(--info)}
.b-kept{background:#dff3e3;color:var(--ok)} .b-dropped{background:#fde0de;color:var(--bad)}
.b-merge{background:#e3ebf7;color:var(--info)} .b-succession{background:#e3ebf7;color:var(--info)} .b-new{background:#dff3e3;color:var(--ok)} .b-skip{background:#fff1d6;color:var(--warn)}
.b-repeat{background:#fff1d6;color:var(--warn)} .b-replace{background:#e3ebf7;color:var(--info)}
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
<h1>Item-by-item extraction trace <span class="muted small" id="range"></span></h1>
<p class="muted">The road every item took: routing (into the pipeline or not) → extraction (what the model wrote, what the code dropped) → matching (where each candidate thesis went, whether evidence is new or a repeat) → writing (what opened, what changed) → the day's re-judging. Every number is counted from stored data; the model was not asked again.</p>
<div class="card small">
<b>How the diagnosis is assigned (a rule, not a person's judgement)</b>
<div class="rule">empty_handed: the model wrote no evidence and no candidate thesis.</div>
<div class="rule">all_dropped: the model wrote something and the code checks dropped every item (quote not in the text, link to a thesis that does not exist, malformed ladder, quarterly figure, year beyond next year, wrong due day, no surviving evidence).</div>
<div class="rule">noisy: noise ≥ one third of what was written. Noise = what the model wrote and was later thrown away: evidence dropped by code + candidates dropped by code + candidates matching judged skip + candidates whose object is not on the research list (review pool only) + evidence not stored because its thesis did not open. A sentence written twice is merged and is not noise.</div>
<div class="rule">mostly_repeats: at least half of the kept evidence was judged repeat by matching (the library already holds the same sentence or number and only gains a source). The extraction wrote nothing useless; the article retells what was said elsewhere, and this is shown apart from noise.</div>
<div class="rule">normal: everything else. <b>The rule counts only what the pipeline can count</b>; whether the stored evidence is about what matters (trivia or a key number) is for you to read.</div>
</div>
<section id="summary"></section>
<h2>Every item</h2>
<div class="filters" id="filters"></div>
<div class="muted small" id="count"></div>
<table id="items"><thead><tr>
<th data-k="day">Day</th><th data-k="category">Category</th><th data-k="publisher">Source</th><th data-k="objects">Objects</th><th data-k="title">Title</th>
<th class="n" data-k="produced" title="evidence / candidate theses the model wrote">Written ev/th</th><th class="n" data-k="kept" title="kept after the code checks">Kept ev/th</th>
<th data-k="outcomes" title="candidates: merge / succession / new / skip; evidence: new / repeat / replace">Matching</th><th class="n" data-k="stored" title="evidence stored / theses opened / theses changed">Written ev/open/chg</th>
<th data-k="diagnosis">Diagnosis</th><th class="n" data-k="cost">Cost $</th>
</tr></thead><tbody id="rows"></tbody></table>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const S = DATA.summary, ITEMS = DATA.items;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const badge = s => `<span class="badge b-${esc(s)}">${esc(s)}</span>`;
document.getElementById('range').textContent = `${S.from} to ${S.to}`;
function table(rows, head){ return `<table><thead><tr>${head.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map((c,i)=>`<td class="${typeof c==='number'?'n':''}">${typeof c==='number'?c:c}</td>`).join('')}</tr>`).join('')}</tbody></table>`; }
function kv(obj, label1, label2){ return table(Object.entries(obj).sort((a,b)=>b[1]-a[1]).map(([k,v])=>[esc(k), v]), [label1, label2]); }
function groupTable(groups, label){
  const diag = ['normal','mostly_repeats','noisy','all_dropped','empty_handed','failed'];
  return table(Object.entries(groups).map(([k,v])=>[esc(k), v['items']||0, ...diag.map(d=>v[d]||0), v['cost']||0]), [label,'items',...diag,'cost $']);
}
(function renderSummary(){
  const el = document.getElementById('summary');
  const funnel = [
    ['items in the corpus for these days', S.items],
    ['routed into the pipeline', (S.routes['in_pipeline']||0)],
    ['of which actually run (the seed period ran NVDA only)', S.processed],
    ['the model wrote something', S.wrote_something],
    ['something survived the code checks', S.kept_something],
    ['written into the library after matching (evidence stored, a thesis opened or changed)', S.stored_something],
  ];
  el.innerHTML = `
  <h2>Overview</h2>
  <div class="cards">${funnel.map(([k,v])=>`<div class="card"><div class="num">${v}</div><div class="muted small">${esc(k)}</div></div>`).join('')}</div>
  <div class="two">
    <div class="card"><h3>Not in the pipeline, and why</h3>${kv(S.route_reasons,'reason','items')}<p class="small muted">not_run ${S.unrun} items: the seed period (before the window) ran NVDA only.</p></div>
    <div class="card"><h3>Diagnoses of the ${S.processed} items run</h3>${kv(S.diagnoses,'diagnosis','items')}<p class="small muted">Cost $${S.cost} (extraction + matching, at the price when the answers were bought). Items whose matching the code returned: ${S.match_refused_items}; answers not matching the handover record: ${S.answer_mismatch}.</p></div>
  </div>
  <div class="two">
    <div class="card"><h3>How much the model wrote, how much was kept</h3>${table([
      ['evidence', S.produced.evidence, S.kept.evidence, S.stored_evidence],
      ['candidate theses', S.produced.candidates, S.kept.candidates, S.new_views]], ['', 'model wrote', 'code kept', 'written to the library'])}
      <p class="small muted">Fewer evidence items are written than kept: the ${S.repeats} judged repeat only gain a source; a candidate merged into an existing thesis opens no new one.</p></div>
    <div class="card"><h3>Matching results</h3><div class="two">${kv(S.outcomes,'where candidates went','items')}${kv(S.evidence_outcomes,'what evidence counts as (one decision per thesis it links to)','decisions')}</div></div>
  </div>
  <div class="two">
    <div class="card"><h3>Why the code dropped evidence</h3>${kv(S.drop_reasons,'reason','items')}</div>
    <div class="card"><h3>Why the code dropped candidates</h3>${kv(S.candidate_drop_reasons,'reason','items')}<h3>Notes at writing</h3>${kv(S.notes,'note','items')}</div>
  </div>
  <div class="card"><h3>Kept evidence by tier</h3>${kv(S.tiers_kept,'tier','items')}</div>
  <div class="card"><h3>By category</h3>${groupTable(S.by_category,'category')}</div>
  <div class="card"><h3>By source type</h3>${groupTable(S.by_publisher_type,'source type')}</div>
  <div class="card"><h3>By day</h3>${groupTable(S.by_day,'day')}</div>`;
})();
const state = {day:'', category:'', ptype:'', diag:'', object:'', q:'', sort:'day', dir:1};
(function renderFilters(){
  const el = document.getElementById('filters');
  const opts = (vals, label) => `<option value="">${label}: all</option>` + [...new Set(vals)].sort().map(v=>`<option>${esc(v)}</option>`).join('');
  el.innerHTML = `
  <select id="f-day">${opts(ITEMS.map(i=>i.day),'day')}</select>
  <select id="f-category">${opts(ITEMS.map(i=>i.category),'category')}</select>
  <select id="f-ptype">${opts(ITEMS.map(i=>i.publisher_type),'source type')}</select>
  <select id="f-diag">${opts(ITEMS.map(i=>i.diagnosis),'diagnosis')}</select>
  <select id="f-object">${opts(ITEMS.flatMap(i=>i.objects),'object')}</select>
  <input id="f-q" placeholder="search title / source / id" size="28">
  <label class="small"><input type="checkbox" id="f-noise"> only items with noise ≥ 1</label>`;
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
  document.getElementById('count').textContent = `${rows.length} items (click a row to expand)`;
  document.getElementById('rows').innerHTML = rows.map((i,n)=>{
    const o=i.outcomes||{}, eo=i.evidence_outcomes||{};
    const outcomes = i.route!=='in_pipeline'||!i.seq ? '' : `${o['merge']||0}/${o['succession']||0}/${o['new']||0}/${o['skip']||0} · ${eo['new']||0}/${eo['repeat']||0}/${eo['replace']||0}`;
    return `<tr class="item" data-id="${esc(i.id)}"><td>${esc(i.day)}</td><td>${esc(i.category)}</td><td>${esc(i.publisher)}<div class="muted small">${esc(i.publisher_type)}</div></td>
    <td>${i.objects.map(esc).join(' ')}</td><td>${esc(i.title)||'<span class="muted">(no title)</span>'}<div class="muted small">${esc(i.id)}</div></td>
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
  const files = `<a href="text/${i.slug}.txt" target="_blank">full source text</a>` + (i.seq?` · <a href="request/${i.slug}.txt" target="_blank">the complete request to the model</a> · <a href="answer/${i.slug}.json" target="_blank">the model's raw answer</a>`:'') + (i.uri?` · <a href="${esc(i.uri)}" target="_blank">source link</a>`:'');
  let out = `<div><b>Diagnosis:</b> ${badge(i.diagnosis)} ${esc(i.diagnosis_why)}</div><div class="small muted">${files} · source ${i.chars} characters</div><div class="quote small" style="margin:6px 0">${esc(i.excerpt)}</div>`;
  out += `<h4>① Routing</h4><div>${esc(i.route)}${i.route_reason?': '+esc(i.route_reason):': the object is on the list and the category is watched; into the pipeline'}</div>`;
  if (!i.seq) return out;
  const c = i.extract_call||{};
  out += `<h4>② Extraction</h4><div class="small muted">model ${esc(c.model)}, request ${c.prompt_chars} characters, ${c.input_tokens} input / ${c.output_tokens} output tokens, ${c.seconds} s, $${c.cost}${c.candidates_of_item>1?` (the archive holds ${c.candidates_of_item} extraction calls for this item; the last one before the "extracted" step is shown)`:''}${i.answer_matches_handover===false?' <b style="color:var(--bad)">answer does not match the handover record</b>':''}</div>`;
  out += `<div class="small"><b>Existing theses shown to the model (${i.shown_views.length})</b>${i.shown_views.length?`<ul>${i.shown_views.map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`:': none yet; everything that should open is a candidate'}</div>`;
  out += `<div><b>Evidence the model wrote (${i.raw_evidence.length})</b></div>` + (i.raw_evidence.length ? table(i.raw_evidence.map(e=>[esc(e.id), badge(e.status)+(e.why?`<div class="small muted">${esc(e.why_class)}<br>${esc(e.why)}</div>`:''), esc(e.tier), esc(e.speaker)+(e.original_who?`<div class="small muted">retelling ${esc(e.original_who)} ${esc(e.original_day)}</div>`:''), `<div class="quote">${esc(e.quote)}</div><div>${esc(e.one_line)}</div>`, e.links.map(esc).join(' ')]), ['id','result','tier','speaker','quote / one line','links']) : '<div class="muted small">none</div>');
  out += `<div style="margin-top:8px"><b>Candidate theses the model wrote (${i.raw_candidates.length})</b></div>` + (i.raw_candidates.length ? table(i.raw_candidates.map(k=>[esc(k.id), badge(k.status)+(k.why?`<div class="small muted">${esc(k.why_class)}<br>${esc(k.why)}</div>`:''), `${esc(k.kind)}<div class="small muted">${esc(k.object)} · ${esc(k.year)} · due ${esc(k.due_day)}</div>`, `<b>${esc(k.question)}</b><div class="small muted">focus: ${esc(k.looks_at)}</div><ol class="small" style="margin:2px 0;padding-left:18px">${k.rungs.map(r=>`<li>${esc(r)}</li>`).join('')}</ol>`, k.evidence_ids.map(esc).join(' ')]), ['id','result','kind','question / ladder','evidence']) : '<div class="muted small">none</div>');
  out += `<h4>③ Matching</h4>`;
  if (!i.match_calls.length) out += `<div class="muted small">no matching: nothing survived extraction</div>`;
  for (const m of i.match_calls){
    out += `<div class="small muted">call ${m.call_no} (${m.call_no<=2?'candidates + evidence linked straight to existing theses':'evidence compared again under the thesis its candidate merged into'}), $${m.cost}, ${m.seconds} s${m.refusals.length?` · <b style="color:var(--bad)">returned by the code</b>: ${m.refusals.map(esc).join('; ')}`:''}</div>`;
    if (m.candidates.length) out += table(m.candidates.map(k=>[esc(k.id), badge(k.outcome)+(k.target?` → ${esc(k.target)}`:'')+(k.not_opened?`<div class="small" style="color:var(--warn)">not opened by the code: the object is not on the research list; pooled as a suggested theme</div>`:''),`<span class="small muted">compared with: ${k.offered.length?k.offered.map(esc).join(' '):'nothing'}</span>`+(k.dependencies.length?`<div class="small muted">dependencies: ${k.dependencies.map(d=>esc(d.view_id)+(d.direction?` (${esc(d.direction)})`:'')+(d.wait_chain_view_id?`, waiting for ${esc(d.wait_chain_view_id)} ${esc(d.wait_year)}`:'')).join('; ')}</div>`:''), esc(k.reason)]), ['candidate','destination','compared with','the model\'s reason']);
    if (m.evidence.length) out += table(m.evidence.map(e=>[esc(e.id)+' → '+esc(e.view), badge(e.outcome)+(e.target?` of ${esc(e.target)}`:'')+(e.said_day?` said on ${esc(e.said_day)}`:''), `<span class="small muted">compared with: ${e.offered.length?e.offered.map(esc).join(' '):'nothing'}</span>`, esc(e.reason)]), ['evidence → thesis','counts as','compared with','the model\'s reason']);
  }
  const w = i.written;
  out += `<h4>④ Writing</h4><div class="small">${w.stored_evidence} new evidence items stored, ${w.linked_existing} existing items gained this source; ${w.new_views.length} theses opened; theses whose reading changed: ${w.changed.length?w.changed.map(esc).join(' '):'none'}</div>`;
  if (w.new_views.length) out += table(w.new_views.map(v=>[`${esc(v.candidate)} → <b>${esc(v.view_id)}</b>`, `${esc(v.kind)}<div class="small muted">${esc(v.object)} · ${esc(v.year)} · due ${esc(v.due_day)}</div>`, `<b>${esc(v.question)}</b><div class="small muted">focus: ${esc(v.looks_at)}</div><ol class="small" style="margin:2px 0;padding-left:18px">${v.rungs.map(r=>`<li>${esc(r)}</li>`).join('')}</ol>`]), ['candidate → thesis','kind','question / ladder']);
  if (w.notes.length) out += `<ul class="small">${w.notes.map(n=>`<li>${esc(n.class)}: <span class="muted">${esc(n.text)}</span></li>`).join('')}</ul>`;
  out += `<h4>⑤ Re-judging</h4>` + (i.judged.length ? table(i.judged.map(j=>[esc(j.view_id), `rung ${j.rung}`, j.changed?'<b>changed</b>':'unchanged', esc(j.by), `<div>${esc(j.why_changed)}</div><div class="small muted">${esc(j.reasons)}</div>`]), ['thesis','judged at','changed','round','why']) : `<div class="muted small">${w.changed.length||w.new_views.length?'the theses this item changed were not judged in the day\'s round (no judgement recorded that day)':'this item changed no thesis, so nothing to re-judge'}</div>`);
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
