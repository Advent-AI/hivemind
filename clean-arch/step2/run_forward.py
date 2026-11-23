#!/usr/bin/env python3
"""Run clean Steps 2 and 3 forward over a stored clean Step 1 trace: every kept evidence record, article by article, searched against
the library as it stood after the previous article, compared by Jev, and written to the isolated Step 3 library.

Embeddings come from the repository's embedding helper and are cached by exact text in the output folder; `--seed-cache` takes an
earlier cache keyed the same way. Jev answers are archived in the output folder. `--dry-run` counts texts to embed without sending.

Usage: run_forward.py <step1 trace.sqlite> <output folder> [--seed-cache embeddings.json --seed-items items.json] [--dry-run]"""
import argparse, hashlib, importlib.util, json, sqlite3, sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, jev, model, search  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compare = load('clean_step2_compare', HERE / 'compare.py')
library = load('clean_step3_library', ROOT / 'clean-arch/step3/library.py')
SETTING = config.Setting('clean-step2', 'jev-1.14.0', 'clean-step2', None, 0)


def step1_records(trace):
    """Kept evidence of a completed Step 1 run (unlinked statements included), as Step 3 records grouped by article, with every thesis
    question and, per article, the thesis ids it opened. `trace` may join continuation segments with '+'. An article is numbered by its
    position in the first segment's manifest, so a failed item never shifts the numbers of the articles after it. A record keeps Step 1's
    verified passages beside the model's (None marks a passage not found in the source). A link resolves as the runner resolves it,
    by its type: an existing target must be among the theses shown open, a new one among the theses the answer opened; any other link
    stays out of `thesis_ids` and is listed in `unresolved_thesis_ids` as '<type>:<id>'."""
    questions = {}
    articles = []
    opened = []
    rows = []
    position = None
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        try:
            if position is None:
                position = {iid: n for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
            done = conn.execute("select input_id, request, result, before_state, after_state from trace where status='complete' order by sequence").fetchall()
        finally:
            conn.close()
        rows += [(position[row[0]], *row[1:]) for row in done]
    for seq, request, result, before, after in rows:
        source = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']
        questions.update({t['id']: t['description'] for t in json.loads(after)})
        opened.append(sorted({t['id'] for t in json.loads(after)} - {t['id'] for t in json.loads(before)}))
        answer = json.loads(result)
        local = answer.get('new_thesis_ids', {})
        open_before = {t['id'] for t in json.loads(before)}
        def resolve(link):   # the runner's own rule: an existing target must have been shown open; a new one must have been opened
            if link['target_type'] == 'existing':
                return link['target_id'] if link['target_id'] in open_before else None
            return local.get(link['target_id'])
        def targets(ev, resolved):
            if resolved:
                return sorted({resolve(l) for l in ev['links'] if resolve(l)})
            return sorted({f"{l['target_type']}:{l['target_id']}" for l in ev['links'] if not resolve(l)})
        articles.append([{'id': f"{seq}:{ev['local_id']}", 'article': seq, 'input_id': source['id'], 'title': source.get('title'),
                          'publisher': source['publisher'], 'publication_date': source['publication_date'], 'summary': ev['summary'],
                          'passages': ev['source_passages'], 'verified_passages': ev.get('verified_source_passages'),
                          'original_party': ev['original_party'],
                          'reporting_speaker': ev['reporting_speaker'], 'tier': ev['tier'], 'statement_date': ev['statement_date'],
                          'statement_date_text': ev['statement_date_text'], 'evidence_period': ev['evidence_period'],
                          'figures': ev.get('figures') or [],
                          'thesis_ids': targets(ev, True), 'unresolved_thesis_ids': targets(ev, False)}
                         for ev in answer['evidence']])
    kept = [i for i, a in enumerate(articles) if a]
    return [articles[i] for i in kept], questions, [opened[i] for i in kept]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace')
    parser.add_argument('output')
    parser.add_argument('--seed-cache')
    parser.add_argument('--seed-items')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    out = Path(args.output)
    articles, questions, opened = step1_records(args.trace)
    records = [r for a in articles for r in a]
    texts = sorted({compare.doc_text(r) for r in records} | {compare.query_text(r, questions[t]) for r in records for t in r['thesis_ids']})
    cache_path = out / 'embeddings.json'
    vectors = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    if args.seed_cache and not vectors:   # an earlier cache keyed 'doc:<key>' / 'q1:<key>:<thesis>' over the same items
        seed = json.loads(Path(args.seed_cache).read_text())
        by_key = {r['id']: r for r in records}
        for item in json.loads(Path(args.seed_items).read_text()):
            r = by_key.get(item['key'])
            if r and f"doc:{item['key']}" in seed:
                vectors[compare.doc_text(r)] = seed[f"doc:{item['key']}"]
                for t in r['thesis_ids']:
                    if f"q1:{item['key']}:{t}" in seed:
                        vectors[compare.query_text(r, questions[t])] = seed[f"q1:{item['key']}:{t}"]
    missing = [t for t in texts if t not in vectors]
    print(f'articles {len(articles)}; records {len(records)}; texts {len(texts)}; to embed {len(missing)}')
    if args.dry_run:
        return 0
    out.mkdir(parents=True, exist_ok=True)
    for start in range(0, len(missing), 64):
        chunk = missing[start:start + 64]
        got, _tokens = search.openai_embeddings(chunk)
        vectors.update(zip(chunk, got))
    cache_path.write_text(json.dumps(vectors))
    archive = model.Archive(str(out / 'jev.sqlite'))
    cfg = SimpleNamespace(provider='jev', version='clean-step2', checksum=hashlib.sha256(b'clean-step2-piece-question').hexdigest()[:16])
    ask = lambda state, qs: jev.ask(archive, cfg, SETTING, state, qs, 'clean_step2').data
    store = library.Library()
    decisions = compare.forward(articles, store, vectors, questions, ask, opened=opened)
    (out / 'decisions.json').write_text(json.dumps(decisions, indent=1))
    (out / 'library.json').write_text(json.dumps({'order': store.order, 'groups': store.groups, 'placement': store.placement,
                                                  'judged': [[k[0], k[1], v] for k, v in store.judged.items()], 'later_log': store.later_log,
                                                  'pending': store.pending}, indent=1))
    kinds = {}
    for d in decisions:
        kinds[d['outcome']['kind']] = kinds.get(d['outcome']['kind'], 0) + 1
    print(f"groups {len(store.groups)}; outcomes {kinds}; refused {sum('refused' in d for d in decisions)}; "
          f"several same_statement answers {sum(1 for d in decisions if sum(a['choice'] == 'same_statement' for a in d['answers'].values()) > 1)}; "
          f"later linking: judged {sum(e['judged'] for e in store.later_log)}, linked {sum(len(e['linked']) for e in store.later_log)}, "
          f"pending {sum(len(e['pending']) for e in store.later_log)}")
    refused = sum('refused' in d for d in decisions)
    still_pending = sum(len(ids) for ids in store.pending.values())
    unresolved = sum(len(r['unresolved_thesis_ids']) for r in records)
    if refused or still_pending or unresolved:   # an incomplete run is written for inspection but never reported as a success
        print(f'incomplete: {refused} refused, {still_pending} later-link pairs still pending, {unresolved} unresolved Step 1 links')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
