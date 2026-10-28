"""Control / arm harness over the frozen extraction gold (gold-standard.md §3, §5).

  python3 ab_gold.py replay  [gold.json ...]                 $0: score the snapshot's stored production answer of each article (control ids)
  python3 ab_gold.py send control|themes N [gold.json ...]   N fresh sends per article into scratch archives, scored
  python3 ab_gold.py report                                  the Markdown summary over every scored run in results/

Control = the production request rebuilt at the article's turn (the identity must equal an archived request: production bytes,
AGENTS §5). Arm 'themes' = the same request with every theme thesis open at that turn added to the shown list (proposal A).
Scoring is code (gold-standard.md §3): a raw piece matches a gold statement when the normalised quote and span contain one
another; each gold statement lands in exactly one cell; extra_kept and split are counted per answer. The quote check is this
worktree's extraction.normalise (the punctuation-spacing fix), for the control and the arm alike. Reads only the snapshot."""
import collections, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, ROOT + '/src')
from hivemind import config, extraction, model, universe       # noqa: E402
from hivemind.views import store                              # noqa: E402
SNAP = '/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
RESULTS = os.path.join(HERE, 'results'); os.makedirs(RESULTS, exist_ok=True)
cfg = config.load(ROOT + '/poc/config/poc-v34.json'); uni = universe.load(ROOT + '/poc/universe.json')
v = sqlite3.connect(f'file:{SNAP}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
a = sqlite3.connect(f'file:{SNAP}/archive.sqlite?mode=ro', uri=True)
t = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True); t.row_factory = sqlite3.Row
CREATED = {r['view_id']: r['created_seq'] for r in v.execute('select view_id, created_seq from views')}


def load_gold(paths):
    arts = []
    for p in paths or [os.path.join(HERE, 'gold-extraction.json')]:
        arts += json.load(open(p))['articles']
    return arts


def turn(item_id):
    return v.execute('select min(sequence_no) from processing_steps where input_id=?', (item_id,)).fetchone()[0]


def context(art):
    """The item, the shown lists (control / themes) and the groups as they stood at the article's turn."""
    item = dict(t.execute('select * from items where input_id=?', (art['input_id'],)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'] or '[]')
    seq = turn(art['input_id'])
    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
    shown = {'control': [], 'themes': []}
    for r in v.execute('select view_id from views where created_seq<? order by created_seq', (seq,)):
        vw = dict(store.view(v, r['view_id']), open=True, depends_on=[], dependencies=[])
        if vw['object_id'] in objects:
            shown['control'].append(vw); shown['themes'].append(vw)
        elif vw['kind'] == 'theme':
            shown['themes'].append(vw)
    # The groups block is state-dependent (member groups plus an FTS top-10 over the index as it stands), so it is taken from the
    # stored production request in its stored order, each group's members as they stood at the turn.
    groups = []
    for gid in stored_group_ids(art['input_id']):
        g = store.group(v, gid)
        members = [m for m in store.members_of_group(v, gid) if CREATED.get(m, 10**9) < seq]
        groups.append(dict(g, members=[{'view_id': m, 'object_id': store.view(v, m)['object_id'], 'looks_at': store.view(v, m)['looks_at']} for m in members]))
    return item, shown, groups


def stored_group_ids(item_id):
    import re
    row = a.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {item_id},%',)).fetchone()
    user = [m['content'] for m in json.loads(row[0])['messages'] if m['role'] == 'user'][0]
    block = re.search(r'\[Research groups\](.*?)\n\n', user, re.S)
    return re.findall(r'^  - (g\d+) "', block.group(1), re.M) if block else []


def archived_identities(item_id):
    return {r[0].split(':')[0] for r in a.execute("select request_sha256 from model_calls where purpose='extract' and request_json like ?", (f'%[Item] id {item_id},%',))}


def latest_stored_answer(item_id):
    row = a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id desc limit 1", (f'%[Item] id {item_id},%',)).fetchone()
    return json.loads(row[0]) if row else None


def overlap(quote, span):
    q, s = extraction.normalise(quote), extraction.normalise(span)
    return bool(q) and bool(s) and (s in q or (len(q) >= 20 and q in s))


def score(art, answer, item, shown, groups, arm):
    """One answer against the article's gold: a cell per statement, extra_kept and split per answer, with the ids behind each."""
    shown_ids = {x['view_id'] for x in shown}; group_ids = [g['group_id'] for g in groups]
    kept, cands, dropped, _ = extraction.sift_with_groups(answer, item, item['text'], shown_ids, uni, english=True, shown_group_ids=group_ids, version='v18')
    kept_by_id = {e['id']: e for e in kept}; drop_reason = dict(dropped)
    raw = answer.get('evidence', [])
    key = 'bears_on_with_themes' if arm == 'themes' else 'bears_on_now'
    cells, matched_raw = {}, set()
    for s in art['statements']:
        spans = [s['span']] + s['also']
        hits = [e for e in raw if any(overlap(e['quote'], sp) for sp in spans)]
        matched_raw.update(e['id'] for e in hits)
        kept_hits = [kept_by_id[e['id']] for e in hits if e['id'] in kept_by_id]
        if kept_hits:
            right = [e for e in kept_hits if set(e['links']) & set(s[key])]
            cell = 'kept_right' if right else 'kept_wrong_link'
            detail = {'pieces': [e['id'] for e in kept_hits], 'links': sorted({l for e in kept_hits for l in e['links']}), 'wanted': s[key]}
        elif hits:
            cell = 'written_dropped'
            detail = {'pieces': [e['id'] for e in hits], 'reasons': [drop_reason.get(e['id'], 'dropped with its target') for e in hits], 'links': sorted({l for e in hits for l in e.get('links', [])})}
        else:
            cell, detail = 'not_written', {}
        cells[s['id']] = {'cell': cell, 'weight': s['weight'], 'split': max(0, len(hits) - 1), **detail}
    extra = [e for e in kept if e['id'] not in matched_raw]
    return {'cells': cells, 'extra_kept': [{'id': e['id'], 'links': e['links'], 'one_line': e['one_line'][:140]} for e in extra],
            'raw_pieces': len(raw), 'kept_pieces': len(kept), 'candidates': [c['question'][:100] for c in cands]}


def run_replay(arts):
    out = []
    for art in arts:
        item, shown, groups = context(art)
        answer = latest_stored_answer(art['input_id'])
        if answer is None:
            print('no stored answer', art['input_id']); continue
        out.append({'arm': 'replay', 'sample': 0, 'input_id': art['input_id'], 'held_out': art['held_out'], **score(art, answer, item, shown['control'], groups, 'control')})
    json.dump(out, open(os.path.join(RESULTS, 'replay.json'), 'w'), indent=1, ensure_ascii=False)
    return out


def run_send(arts, arm, samples):
    out = []
    for art in arts:
        item, shown, groups = context(art)
        setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown[arm], uni, groups)
        _, ident = model.request_identity(model.build_request(setting, system, user, schema, 'extraction', cfg.provider))
        same = ident in archived_identities(art['input_id'])
        print(f"{art['input_id']} {arm}: shown {len(shown[arm])}, user {len(user)} chars, identity archived: {same}")
        if arm == 'control' and not same:
            raise SystemExit('control bytes differ from production (AGENTS §5): ' + art['input_id'])
        def one(sample):
            archive = model.Archive(os.path.join(RESULTS, f'archive-{arm}-s{sample}.sqlite'))     # one scratch archive per sample: an identical request is served from store
            answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract')
            return sample, answer
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=samples) as pool:
            answers = sorted(pool.map(one, range(1, samples + 1)))
        for sample, answer in answers:
            rec = {'arm': arm, 'sample': sample, 'input_id': art['input_id'], 'held_out': art['held_out'], 'cost_usd': answer.cost_usd, 'cached': answer.cached,
                   **score(art, answer.data, item, shown[arm], groups, arm)}
            out.append(rec)
            print(f"  s{sample}: raw {rec['raw_pieces']} kept {rec['kept_pieces']} cells {collections.Counter(c['cell'] for c in rec['cells'].values())} extra {len(rec['extra_kept'])} ${answer.cost_usd:.4f}{' cached' if answer.cached else ''}", flush=True)
    path = os.path.join(RESULTS, f'send-{arm}.json')
    old = json.load(open(path)) if os.path.exists(path) else []
    json.dump(old + out, open(path, 'w'), indent=1, ensure_ascii=False)
    return out


def report():
    rows = []
    for name in sorted(os.listdir(RESULTS)):
        if name.endswith('.json'):
            rows += json.load(open(os.path.join(RESULTS, name)))
    gold = {s['id']: s for art in load_gold([]) + load_gold([os.path.join(HERE, 'gold-extraction-themes.json')] if os.path.exists(os.path.join(HERE, 'gold-extraction-themes.json')) else []) for s in art['statements']}
    lines = ['# 对照 / 实验打分（代码打的，gold-standard.md §3）\n', '| arm | sample | articles | kept_right | kept_wrong_link | written_dropped | not_written | split | extra_kept | raw | kept | $ |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    by = collections.defaultdict(list)
    for r in rows: by[(r['arm'], r['sample'])].append(r)
    for (arm, sample), rs in sorted(by.items()):
        c = collections.Counter(); core = collections.Counter(); split = extra = raw = kept = 0; cost = 0.0
        for r in rs:
            for sid, cell in r['cells'].items():
                c[cell['cell']] += 1; split += cell['split']
                if cell['weight'] == 'core': core[cell['cell']] += 1
            extra += len(r['extra_kept']); raw += r['raw_pieces']; kept += r['kept_pieces']; cost += r.get('cost_usd', 0) or 0
        lines.append(f"| {arm} | {sample} | {len(rs)} | {c['kept_right']} (core {core['kept_right']}) | {c['kept_wrong_link']} (core {core['kept_wrong_link']}) | {c['written_dropped']} (core {core['written_dropped']}) | {c['not_written']} (core {core['not_written']}) | {split} | {extra} | {raw} | {kept} | {cost:.3f} |")
    lines.append('\n## 每条金标在每次发送落在哪一格\n')
    sids = sorted(gold, key=lambda x: (x.split('-')[0], int(x.split('-')[1])))
    keys = sorted(by)
    lines.append('| 金标 | 分量 | ' + ' | '.join(f'{arm} s{s}' for arm, s in keys) + ' |'); lines.append('|---|---|' + '---|' * len(keys))
    short = {'kept_right': '✓', 'kept_wrong_link': 'link✗', 'written_dropped': 'dropped', 'not_written': '—'}
    for sid in sids:
        cells = []
        for k in keys:
            hit = next((r['cells'][sid] for r in by[k] if sid in r['cells']), None)
            cells.append(short[hit['cell']] + (f"({','.join(hit.get('links', []))})" if hit and hit['cell'] != 'not_written' and hit.get('links') is not None else '') if hit else '')
        lines.append(f"| {sid} | {gold[sid]['weight']} | " + ' | '.join(cells) + ' |')
    lines.append('\n## 多留的（每次发送，前 6 条）\n')
    for (arm, sample), rs in sorted(by.items()):
        for r in rs:
            if r['extra_kept']:
                lines.append(f"- {arm} s{sample} {r['input_id']}: " + ' ‖ '.join(f"{e['id']}→{','.join(e['links'])}: {e['one_line'][:90]}" for e in r['extra_kept'][:6]))
    open(os.path.join(HERE, 'ab-results.md'), 'w').write('\n'.join(lines)); print('\n'.join(lines[:12]))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'replay':
        run_replay(load_gold(sys.argv[2:]))
    elif mode == 'send':
        run_send(load_gold(sys.argv[4:]), sys.argv[2], int(sys.argv[3]))
    elif mode == 'check':
        for art in load_gold(sys.argv[2:]):
            item, shown, groups = context(art)
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown['control'], uni, groups)
            _, ident = model.request_identity(model.build_request(setting, system, user, schema, 'extraction', cfg.provider))
            print(art['input_id'], 'control identity archived:', ident in archived_identities(art['input_id']), '| groups', len(groups), '| themes added', len(shown['themes']) - len(shown['control']))
    elif mode == 'report':
        report()
