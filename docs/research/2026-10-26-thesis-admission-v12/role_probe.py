#!/usr/bin/env python3
"""Cheapest proof for a role version (AGENTS §1.4, §6): re-send the stored extraction requests of the gold's items with the system
prompt and schema of another version (the user message is built by the same code for every version ≥ 12), three samples each,
sift them with the shown ids of the stored request, and count which gold must-open keys the candidates propose and which
must-not-open keys they propose. The stored answers of one or more ledgers are scored the same way as controls. Scratch archive only.

  python3 .../role_probe.py --gold <json> --source <run dir with archive.sqlite> [--control <run dir>]... --version v13 --config poc/config/poc-v27.json --archive <scratch> --out <dir> [--samples 3]
"""
import argparse
import collections
import json
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, universe  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite'
EVENT = ('event', 'policy_event')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def stored_requests(archive_path):
    """input_id -> (request, answer) of the last stored extraction call."""
    out = {}
    for r in ro(archive_path).execute("select request_json, answer_json from model_calls where purpose='extract' order by call_id"):
        request = json.loads(r['request_json'])
        user = request['messages'][1]['content']
        if '[Item] id ' in user:
            out[user.split('[Item] id ', 1)[1].split(',', 1)[0]] = (request, json.loads(r['answer_json']))
    return out


def shown_ids(user):
    block = user.split('[Existing theses of these objects]', 1)[1].split('\n\n[', 1)[0] if '[Existing theses of these objects]' in user else ''
    return set(re.findall(r'\n  - (v\d+) \(', block))


def key_matches(uni, c, key):
    if (uni.resolve(c.get('object', '')) or c.get('object')) != (uni.resolve(key['object']) or key['object']):
        return False
    if c.get('measure') != key['measure']:
        return False
    if key['measure'] in EVENT:
        if (c.get('event_type') or 'n/a') != (key.get('event_type') or 'n/a'):
            return False
    else:
        year = uni.canonical_year(uni.resolve(c.get('object', '')) or c.get('object'), c.get('year', '')) if hasattr(uni, 'canonical_year') else c.get('year', '')
        if str(year) != str(key['year']):
            return False
    pattern = key.get('scope_regex') or ''
    return not pattern or bool(re.search(pattern, ' '.join([c.get('scope', ''), c.get('looks_at', ''), c.get('question', '')]), re.I))


def score(uni, case, candidates):
    must = [any(key_matches(uni, c, k) for c in candidates for k in [key] + list(key.get('alternatives') or [])) for key in case['must_open']]
    bad = [any(key_matches(uni, c, key) for c in candidates) for key in case['must_not_open']]
    return sum(must), len(must), sum(bad), len(bad), len(candidates)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gold', required=True); ap.add_argument('--source', required=True); ap.add_argument('--control', action='append', default=[])
    ap.add_argument('--version', required=True); ap.add_argument('--config', required=True); ap.add_argument('--archive', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--samples', type=int, default=3)
    args = ap.parse_args()
    gold = json.loads(pathlib.Path(args.gold).read_text())
    uni = universe.load(ROOT / 'poc' / 'universe.json')
    cfg = config.load(args.config)
    items_db = ro(ITEMS)
    source = stored_requests(pathlib.Path(args.source) / 'archive.sqlite')
    controls = {pathlib.Path(p).name: stored_requests(pathlib.Path(p) / 'archive.sqlite') for p in [args.source] + args.control}
    archive = model.Archive(args.archive)
    system = (ROOT / 'src' / 'hivemind' / 'prompts' / f'role-{args.version}.txt').read_text(encoding='utf-8')
    rows, spent = [], 0.0
    totals = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for case in gold['cases']:
        item_id = case['items'][0]
        if item_id not in source:
            continue
        request, _ = source[item_id]
        item = dict(items_db.execute('select * from items where input_id=?', (item_id,)).fetchone())
        item['object_identifiers'] = json.loads(item['object_identifiers']) if isinstance(item['object_identifiers'], str) else item['object_identifiers']
        shown = shown_ids(request['messages'][1]['content'])
        groups = re.findall(r'\n  - (g\d+) "', request['messages'][1]['content'])
        schema = extraction.schema_for(args.version, groups, sorted(shown))
        setting = cfg.extraction_setting(item['category'])
        row = {'case': case['id'], 'item': item_id, 'arms': {}}
        for name, store_ in controls.items():
            if item_id in store_:
                _, answer = store_[item_id]
                _, cands, _, _ = extraction.sift_with_groups(answer, item, item['text'] or '', shown, uni, english=True, shown_group_ids=groups)
                row['arms'][name] = [score(uni, case, cands)]
        arm = []
        for s in range(args.samples):
            answer = model.call(archive, cfg, setting, system, request['messages'][1]['content'] + f'\n[sample {s + 1}]', schema, 'extraction', 'extract')
            spent += answer.cost_usd
            _, cands, dropped, _ = extraction.sift_with_groups(answer.data, item, item['text'] or '', shown, uni, english=True, shown_group_ids=groups)
            arm.append(score(uni, case, cands))
        row['arms'][args.version] = arm
        for name, scores in row['arms'].items():
            for sc in scores:
                for i in range(5):
                    totals[name][i] += sc[i]
        rows.append(row)
        print(f"{case['id']}: " + ' | '.join(f"{n}: " + ', '.join(f'{m}/{M} must, {b}/{B} bad, {n_} cand' for m, M, b, B, n_ in sc) for n, sc in row['arms'].items()), flush=True)
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    (out / f'role-probe-{args.version}.json').write_text(json.dumps({'rows': rows, 'totals': dict(totals), 'spent_usd': spent}, ensure_ascii=False, indent=1))
    print('totals (must proposed / must total / bad proposed / bad total / candidates), summed over samples:')
    for name, t in totals.items():
        print(f'  {name}: {t}')
    print(f'spent ${spent:.4f}')


if __name__ == '__main__':
    main()
