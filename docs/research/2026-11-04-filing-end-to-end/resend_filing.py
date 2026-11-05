"""The cheapest proof for the two filing problems (diagnosis.md): stored extraction requests of the frozen v108 draw 1, re-sent as production
builds them, with only the links field's rule changed per arm (links-rules.json: stored, definition, no_fallback, definition_no_fallback), and for an
arm written as {rule, append, system_replace_all} also a text appended at the very end of the user message and one exact edit of the system text.

Faithful bytes (AGENTS §5): each request is rebuilt from the stored system and user texts with the code's own schema (`extraction.schema_for`,
its key order as built) and setting (`cfg.extraction_setting` for the item's category) by `model.build_request`; the script refuses an item
whose rebuilt request does not have the stored archive key. A variant replaces only the links description in that schema. Every answer goes
through the code production runs on it: `extraction.sift_with_groups` against the item's own text and the questions the request showed, then
the handover's narrowest-question rule and the no-home drop (`extraction.narrowest_links`, D207/D209) with the parents at the request's day start.

  select:  python3 resend_filing.py select <selection.json>         (articles: the class, the total-revenue pile, the guards; no send)
  check:   python3 resend_filing.py check <selection.json> --arms a,b,...  (builds every request, checks every edit; no send)
  send:    python3 resend_filing.py send <selection.json> <answers.json> [--sends 3] [--arms a,b,...]
"""
import concurrent.futures
import copy
import json
import os
import re
import sqlite3
import sys
import time

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts']
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
DRAW = f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
ITEMS = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.sqlite'
GOLD = f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold'
STANDARD = f'{ROOT}/docs/research/2026-10-29-ledger-standard/golden-v5'
ITEM_ID = re.compile(r'\[Item\] id (\S+?), category ')
NVIDIA = re.compile(r'nvidia|nvda|jensen|kress|colette', re.I)
WORD = re.compile(r'[a-z]{4,}|\d+(?:\.\d+)?')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def words(text):
    return set(WORD.findall((text or '').lower()))


def stored_calls():
    """input id → (call_id, request_sha256) of draw 1's accepted extraction call for that item (the last, if re-sent)."""
    calls = {}
    for call_id, sha, request_json in ro(f'{DRAW}/archive.sqlite').execute(
            "select call_id, request_sha256, request_json from model_calls where purpose='extract' and answer_json is not null "
            "and request_sha256 not like '%:%' order by call_id"):
        found = ITEM_ID.search(json.loads(request_json)['messages'][1]['content'])
        if found:
            calls[found.group(1)] = (call_id, sha)
    return calls


def select(out):
    """The articles, fixed before any send: (class) every article holding another company's fact that the judgement gold uses for a question
    other than NVIDIA's two revenue questions; (pile) every article behind a statement linked to the total-revenue question in draw 1 whose
    article the extraction gold read; (guard) every article holding a fact the gold uses for NVIDIA's revenue questions or that draw 1 filed
    under the gold's own question. Only articles draw 1 extracted are kept."""
    gold = json.load(open(f'{GOLD}/gold-v1.json'))['entries']
    items = {i['id']: i for i in json.load(open(f'{GOLD}/packet-v1.json'))['items']}
    read = {a['input_id'] for part in ('dev', 'test') for a in json.load(open(f'{STANDARD}/golden-v5-{part}.json'))['articles']}
    views = ro(f'{DRAW}/views.sqlite')
    calls = stored_calls()
    sets = {'class': set(), 'pile': set(), 'guard': set()}
    for entry in gold:
        if entry['no_view'] or not entry.get('seed_view_id'):
            continue
        cited = set((entry.get('decisive_items') or []) + ((entry.get('reference') or {}).get('items') or [])
                    + ((entry.get('implied_outcome') or {}).get('items') or []) + ((entry.get('against') or {}).get('items') or []))
        for item_id in cited:
            item = items[item_id]
            other = not NVIDIA.search(item['who']) and not NVIDIA.search(item['meaning'].get('who', ''))
            if other and entry['question_id'] not in ('q01', 'q02'):
                sets['class'].add(item['input_id'])
            elif entry['question_id'] in ('q01', 'q02'):
                sets['guard'].add(item['input_id'])
    for (input_id,) in views.execute("select s.input_id from evidence_links l join evidence_sources s using(evidence_id) where l.view_id='v1'"):
        if input_id in read:
            sets['pile'].add(input_id)
    chosen = {name: sorted(i for i in ids if i in calls) for name, ids in sets.items()}
    union = sorted(set().union(*chosen.values()))
    json.dump({'sets': chosen, 'articles': {i: {'call_id': calls[i][0], 'request_sha256': calls[i][1]} for i in union}}, open(out, 'w'), indent=1)
    for name, ids in chosen.items():
        print(f'{name}: {len(ids)} articles extracted in draw 1 (of {len(sets[name])})')
    print(f'union: {len(union)} articles')


def rebuild(cfg, items_conn, archive, views, input_id, call_id, sha):
    """(item, setting, system, user, schema, shown ids, parents) for one stored call, refusing unless the rebuilt request is the stored one."""
    request_json, = archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()
    request = json.loads(request_json)
    system = next(m['content'] for m in request['messages'] if m['role'] == 'system')
    user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
    item = testdb.item_of(items_conn.execute('select * from items where input_id=?', (input_id,)).fetchone())
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    schema = extraction.schema_for(version)
    body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    if model.request_identity(body)[1] != sha:
        raise SystemExit(f'{input_id}: the rebuilt request is not the stored one; refusing to send')
    day = re.search(r'\[Open questions at the start of (\d{4}-\d{2}-\d{2})\]', user)
    block = user.split(day.group(0), 1)[1].split('\n\n[', 1)[0] if day else ''
    shown = re.findall(r'^\s*- (v\d+) \(', block, re.M)
    at = store.day_start_seq(views, day.group(1)) if day else 0
    parents = {v: store.direct_parents(views, v, at) for v in shown}
    return item, setting, system, user, schema, shown, parents


def file_like_production(data, item, shown, parents, uni):
    """What production keeps from one answer: the code checks, then the narrowest-question rule and the no-home drop."""
    evidence, candidates, dropped, _ = extraction.sift_with_groups(data, item, item['text'] or '', set(shown), uni)
    candidate_ids = {c['id'] for c in candidates}
    kept, homeless = [], []
    for e in evidence:
        links = [l for l in extraction.narrowest_links(e['links'], parents) if l in shown or l in candidate_ids]
        (kept if links else homeless).append(dict(e, links=links))
    return kept, homeless, [list(d) for d in dropped], [c.get('question', '') for c in candidates]


def arm_request(cfg, rules, arm, prepared_item, input_id):
    """The request one arm sends for one article: the stored request with the arm's links rule, its exact role and user-text edits (each must
    occur exactly once, checked before any send) and its appended text."""
    item, setting, system, user, schema, shown, parents = prepared_item
    spec = rules[arm] if isinstance(rules[arm], dict) else {'rule': rules[arm]}                   # an arm is a links rule, or {rule, append, system_replace_all}
    sent_system = system
    for old_text, new_text in spec.get('system_replace_all', []):                                 # exact edits of the system text (the role)
        if sent_system.count(old_text) != 1:
            raise SystemExit(f'{input_id} ({arm}): the system text to replace occurs {sent_system.count(old_text)} times; nothing sent')
        sent_system = sent_system.replace(old_text, new_text)
    for old_text, new_text in spec.get('user_replace_all', []):                                   # exact edits of the user text (a takes line)
        if user.count(old_text) != 1:
            raise SystemExit(f'{input_id} ({arm}): the user text to replace occurs {user.count(old_text)} times; nothing sent')
        user = user.replace(old_text, new_text)
    variant = copy.deepcopy(schema)
    variant['properties']['evidence']['items']['properties']['links']['description'] = spec['rule']
    return model.build_request(setting, sent_system, user + spec.get('append', ''), variant, 'extraction', cfg.provider)


def send(selection_path, out, sends, arms):
    selection = json.load(open(selection_path))
    rules = json.load(open(f'{HERE}/links-rules.json'))
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    uni = universe.load(f'{ROOT}/poc/universe.json')
    items_conn, archive, views = ro(ITEMS), ro(f'{DRAW}/archive.sqlite'), ro(f'{DRAW}/views.sqlite')
    prepared = {}
    for input_id, meta in selection['articles'].items():
        prepared[input_id] = rebuild(cfg, items_conn, archive, views, input_id, meta['call_id'], meta['request_sha256'])
    print(f'{len(prepared)} requests rebuilt byte-identical to the stored ones')
    bodies = {(input_id, arm): arm_request(cfg, rules, arm, prepared[input_id], input_id) for input_id in prepared for arm in arms}
    print(f'{len(bodies)} arm requests built; every role edit found exactly once in every request')
    if out is None:                                    # check only: no send
        for arm in arms:
            sizes = [(len(b['messages'][0]['content']), len(json.dumps(b, ensure_ascii=False))) for (i, a), b in bodies.items() if a == arm]
            print(f'  {arm}: system text {min(s for s, _ in sizes)}-{max(s for s, _ in sizes)} characters, whole request '
                  f'{min(w for _, w in sizes)}-{max(w for _, w in sizes)}')
        return

    def one(job):
        input_id, arm, n = job
        item, setting, system, user, schema, shown, parents = prepared[input_id]
        body = bodies[(input_id, arm)]
        reply = model.openai_transport(cfg.provider, body, timeout=300)
        data = json.loads(reply['choices'][0]['message']['content'])
        usage = reply.get('usage') or {}
        kept, homeless, dropped, candidates = file_like_production(data, item, shown, parents, uni)
        return input_id, arm, n, {'raw': data.get('evidence', []), 'kept': kept, 'homeless': homeless, 'dropped': dropped, 'candidates': candidates,
                                  'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]}

    def one_with_retry(job):
        """The same request bytes re-sent after a failure (the transport's own retries exhausted, or an unreadable answer), up to three times."""
        for attempt in range(4):
            try:
                return one(job)
            except Exception as error:
                if attempt == 3:
                    raise
                print(f'  {job}: {type(error).__name__}: {str(error)[:160]}; re-sent in {30 * (attempt + 1)} s', flush=True)
                time.sleep(30 * (attempt + 1))

    partial_path = out + '.partial.json'                 # every answer is saved as it lands, so a stopped run resumes without re-sending
    by_index = {}
    if os.path.exists(partial_path):
        by_index = json.load(open(partial_path))
        print(f'resuming from {partial_path}: {sum(len(n) for per in by_index.values() for n in per.values())} answers already saved')
    jobs = [(i, arm, n) for i in prepared for arm in arms for n in range(sends) if str(n) not in by_index.get(i, {}).get(arm, {})]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        futures = [pool.submit(one_with_retry, job) for job in jobs]
        for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
            input_id, arm, n, result = future.result()
            by_index.setdefault(input_id, {}).setdefault(arm, {})[str(n)] = result
            if done % 10 == 0 or done == len(jobs):
                json.dump(by_index, open(partial_path, 'w'), ensure_ascii=False)
                print(f'  {done}/{len(jobs)} sent', flush=True)
    results = {i: {arm: [per[arm][str(n)] for n in range(sends)] for arm in arms} for i, per in by_index.items()}
    json.dump(results, open(out, 'w'), ensure_ascii=False)
    os.remove(partial_path)
    print(f'saved {out}: {sum(len(v) for per in results.values() for v in per.values())} answers')


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'select':
        select(sys.argv[2])
    elif command == 'check':                           # build every arm's request for every article, refuse on any mismatch, send nothing
        send(sys.argv[2], None, 0, sys.argv[sys.argv.index('--arms') + 1].split(','))
    elif command == 'send':
        sends = int(sys.argv[sys.argv.index('--sends') + 1]) if '--sends' in sys.argv else 3
        arms = sys.argv[sys.argv.index('--arms') + 1].split(',') if '--arms' in sys.argv else ['stored', 'definition', 'no_fallback', 'definition_no_fallback']
        send(sys.argv[2], sys.argv[3], sends, arms)
