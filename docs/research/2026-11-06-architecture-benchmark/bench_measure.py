"""The architecture benchmark's measure (plan-final C-8.1; `benchmark-design.md`, hashed before the paid draws), $0, finished runs only.

Window draws (golden-v5 dev; the 118 articles are the window's), at two points of each arm's own path:
- the extraction stage: each item's checked handover as the ledger stores it (`handovers`), the statements extraction hands to matching;
- the product: the evidence records the ledger holds after matching and writing;
and, per gold matter, where it was lost (not handed over; handed over but not written).
Test draws (golden-v5 test, `bench_test_articles.py`): the extraction stage only.

Counting (D372): a core or supporting gold matter is helpful and counts as reached when a statement from its article is the same matter
(`score_gold.same_matter`, the counting aid of every earlier arm); a not-kept entry counts when a statement carries its sentence and no kept matter;
optional entries are neutral; a statement from a gold article matching no gold entry is an extra (unjudged by the gold). Gold questions (must_open,
may_open) count as covered when a question shares enough words with the gist (`score_ref.same_question`, a counting aid, not a judgement).
The judgement at 2026-07-14 against reader B: `score_judgement.py` per draw, the 22 seed questions. Cost from tokens at the published rates
(`model.PRICES`; cached input not separated: an upper bound). Writes `hits-<arm>.json` (per matter, per draw: handed over, written) for reading.

    PYTHONPATH=src python3 bench_measure.py <arm>=<run>,<run>,<run> [...]           window draws
    PYTHONPATH=src python3 bench_measure.py --test <arm>=<folder>,<folder>,<folder>    test draws
    --reference: score stored runs made before this harness (their pins are not checked; the output says so)"""
import collections
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'src'))
import hivemind.model  # noqa: E402,F401  (this tree's package, loaded before the scoring helpers, whose import chain adds another tree's src)
MAIN = Path('/Users/lchingen/hivemind')
LEDGER_STANDARD = MAIN / 'docs/research/2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER_STANDARD), str(LEDGER_STANDARD / 'final-2026-10-30'), str(MAIN / 'docs/research/2026-10-31-reference-context')]
import final_scores as fs  # noqa: E402   (refuses a gold made for another version of the standard page on import)
import score_gold as sg  # noqa: E402
import score_ref as sr  # noqa: E402

GOLDS = {'dev': LEDGER_STANDARD / 'golden-v5/golden-v5-dev.json', 'test': LEDGER_STANDARD / 'golden-v5/golden-v5-test.json'}
SCORER = MAIN / 'docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py'
D373 = ('Gold concern (D373), disclosed with every score that involves it: a source-only reader found possible scope conflicts in three must_open '
        'entries of gnews:d0f3f83296df884fae64921e; the entries are unchanged and not adjudicated '
        '(docs/research/2026-11-05-parallel-refinement/ruler-conflict-2026-11-05.zh.md).')


def gold(name):
    recorded = (LEDGER_STANDARD / 'golden-v5/golden-v5.sha256').read_text()
    actual = sg.sha(GOLDS[name])
    if actual not in recorded:
        raise SystemExit(f'golden-v5 {name} sha256 {actual[:12]} is not the frozen one: refused')
    return json.loads(GOLDS[name].read_text())['articles'], actual


def score(statements_by_article, questions_by_article, articles):
    """Counts and, per gold matter, whether it was reached."""
    result, reached = collections.Counter(), {}
    for a in articles:
        records = statements_by_article.get(a['input_id'], [])
        kept_gold = [it for it in a['items'] if it['weight'] in ('core', 'supporting', 'optional')]
        optional_spans = [n['span'] for n in a['not_kept'] if n['weight'] == 'optional']
        for index, it in enumerate(a['items']):
            if it['weight'] in ('core', 'supporting'):
                hit = any(sg.same_matter(it, r) for r in records)
                reached[f'{a["input_id"]}#{index}'] = hit
                result[it['weight'] + ' total'] += 1
                result[it['weight'] + ' reached'] += hit

        def carried(r):
            return any(sg.same_matter(it, r) for it in kept_gold) or any(sg.same(span, r['quote']) for span in optional_spans)
        not_kept = [n for n in a['not_kept'] if n['weight'] == 'not_kept']
        result['not-kept kept'] += sum(any(sg.same(n['span'], r['quote']) and not carried(r) for r in records) for n in not_kept)
        result['extras'] += sum(1 for r in records if not any(sg.same_matter(it, r) for it in a['items']) and not any(sg.same(n['span'], r['quote']) for n in a['not_kept']))
        result['statements from gold articles'] += len(records)
        questions = questions_by_article.get(a['input_id'])
        if questions is not None:
            for kind in ('must_open', 'may_open'):
                for gq in a.get('questions', {}).get(kind, []):
                    result[kind + ' total'] += 1
                    result[kind + ' covered'] += any(sr.same_question(gq['gist'], q) for q in questions)
    result['helpful total'] = result['core total'] + result['supporting total']
    result['helpful reached'] = result['core reached'] + result['supporting reached']
    return result, reached


def window_draw(run, articles):
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    handed = collections.defaultdict(list)
    for input_id, handover in conn.execute('select input_id, handover_json from handovers'):
        for e in json.loads(handover).get('evidence', []):
            handed[input_id].append({'quote': e.get('quote', ''), 'one_line': e.get('one_line', '')})
    written = collections.defaultdict(list)
    for quote, one_line, input_id in conn.execute('select e.quote, e.one_line, s.input_id from evidence e join evidence_sources s using(evidence_id)'):
        written[input_id].append({'quote': quote, 'one_line': one_line or ''})
    views = [(r[0] + ' ' + (r[1] or ''), r[2] or '') for r in conn.execute('select question, looks_at, created_from_input from views')]
    all_questions = {a['input_id']: [v[0] for v in views] for a in articles}
    stage, stage_hits = score(handed, {}, articles)
    product, product_hits = score(written, all_questions, articles)
    product['questions opened from articles'] = sum(1 for _, source in views if not source.startswith('seed:'))
    product['must_open covered by article-opened'] = sum(
        any(sr.same_question(gq['gist'], v[0]) and not v[1].startswith('seed:') for v in views) for a in articles for gq in a.get('questions', {}).get('must_open', []))
    product['stored records'] = conn.execute('select count(*) from evidence').fetchone()[0]
    product['cost usd x100'] = round(cost(run) * 100)
    losses = collections.Counter('reached' if product_hits[k] else ('handed over, not written' if stage_hits[k] else 'not handed over') for k in product_hits)
    return stage, product, losses, {k: (stage_hits[k], product_hits[k]) for k in product_hits}


def judgement(run):
    printed = subprocess.run([sys.executable, str(SCORER), str(run)], capture_output=True, text=True, check=True).stdout
    return {f'v{int(m.group(1))}': m.group(2) for m in re.finditer(r'^q(\d\d) (agree|DISAGREE|no judgement|no_view|not in run|gold open)', printed, re.M)
            if int(m.group(1)) <= 22}


def cost(run):
    from hivemind import model
    if not Path(model.__file__).resolve().is_relative_to(HERE.parents[2] / 'src'):
        raise SystemExit(f'refused: prices would come from another tree ({model.__file__})')
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    total = 0.0
    for name, tokens_in, tokens_out in archive.execute('select model, sum(input_tokens), sum(output_tokens) from model_calls group by model'):
        price_in, price_out = model.PRICES.get(name, (0.0, 0.0))
        total += (tokens_in or 0) / 1e6 * price_in + (tokens_out or 0) / 1e6 * price_out
    return total


def verify_pins(bench_run, runs, test_mode, reference):
    """Refuse to score unless every run was made by this folder's harness as a paid draw (window: every run entry online; test: its manifest) and
    its pins hold: the scoring files and golds as they are now, and every file two runs both pinned with the same sha256 (code, universe, seeds,
    fixture, items, scoring, and the prompt files both configurations name). Only a file one run alone pinned (its configuration and the prompts
    only it names) may differ. --reference scores stored runs made before this harness and labels them so."""
    if reference:
        print(f'REFERENCE scoring of stored runs made before this harness: pins not checked: {runs}')
        return
    current = {f: sg.sha(f) for f in bench_run.SCORING}
    all_pins = []
    for run in runs:
        path = Path(run) / 'manifest.json'
        if not path.exists():
            raise SystemExit(f'refused: {run} has no harness manifest')
        manifest = json.loads(path.read_text())
        if not test_mode and any(entry.get('offline') for entry in manifest.get('runs', [])):
            raise SystemExit(f'refused: {run} holds an offline gate run, not a paid draw')
        pins = manifest.get('files_sha256') if test_mode else (manifest.get('runs') or [{}])[0].get('files_sha256')
        if not pins:
            raise SystemExit(f'refused: {run} has no pins')
        differ = [f for f, value in current.items() if pins.get(f) != value]
        if differ:
            raise SystemExit(f'refused: {run} ran with other scoring files or golds: {differ}')
        all_pins.append((run, pins))
    versions = {}
    for run, pins in all_pins:
        for name, value in pins.items():
            versions.setdefault(name, {}).setdefault(value, []).append(run)
    differ = {name: by_value for name, by_value in versions.items() if len(by_value) > 1}
    if differ:
        raise SystemExit(f'refused: runs pinned different versions of the same file: '
                         + '; '.join(f'{name}: ' + ' / '.join(f'{v[:12]} in {len(r)} runs' for v, r in by_value.items()) for name, by_value in list(differ.items())[:6]))
    print(f'pins verified for {len(runs)} runs (paid draws of this harness; files both arms use are identical)')


def table(title, keys, arms, rows):
    print(f'\n{title:40}' + ''.join(f'{n:>24}' for n in arms))
    for key in keys:
        print(f'{key:40}' + ''.join(f'{" ".join(str(r[key]) for r in rows[n]):>24}' for n in arms))


def finished(run):
    out = Path(run) / 'run.out'
    return out.exists() and ('BENCH-DONE' in out.read_text() or 'RUN-ARM-DONE' in out.read_text())


def main():
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    test_mode, reference = '--test' in flags, '--reference' in flags
    arms = dict(a.split('=', 1) for a in sys.argv[1:] if not a.startswith('--'))
    arms = {name: runs.split(',') for name, runs in arms.items()}
    articles, gold_sha = gold('test' if test_mode else 'dev')
    print(f'extraction standard version {fs.page_version()} (page sha256 {sg.sha(fs.PAGE)[:16]}…); golden-v5 {"test" if test_mode else "dev"} sha256 '
          f'{gold_sha[:16]}…, {len(articles)} articles; D372 counting (core + supporting helpful, not-kept unhelpful, optional neutral)')
    print(D373)
    sys.path.insert(0, str(HERE))
    import bench_run
    print('scoring files: ' + '; '.join(f'{Path(f).name} {sg.sha(f)[:12]}' for f in bench_run.SCORING))
    verify_pins(bench_run, [r for runs in arms.values() for r in runs], test_mode, reference)
    counts = ['helpful reached', 'helpful total', 'core reached', 'core total', 'supporting reached', 'supporting total', 'not-kept kept', 'extras',
              'statements from gold articles']
    if test_mode:
        rows = {}
        for name, folders in arms.items():
            rows[name], hits = [], {}
            for draw, folder in enumerate(folders, 1):
                handovers = json.load(open(Path(folder) / 'handovers.json'))
                if len(handovers) != len(articles):
                    raise SystemExit(f'{folder}: {len(handovers)} of {len(articles)} articles; not finished')
                statements = {i: [{'quote': e['quote'], 'one_line': e.get('one_line', '')} for e in h['evidence']] for i, h in handovers.items()}
                questions = {i: [c['question'] + ' ' + (c.get('looks_at') or '') for c in h['candidates']] for i, h in handovers.items()}
                row, reached = score(statements, questions, articles)
                for key, hit in reached.items():
                    hits.setdefault(key, {})[f'd{draw}'] = {'handed_over': hit, 'written': hit}
                row['questions proposed'] = sum(len(h['candidates']) for h in handovers.values())
                row['cost usd x100'] = round(cost(folder) * 100)
                rows[name].append(row)
            (HERE / f'hits-test-{name}.json').write_text(json.dumps({'runs': folders, 'matters': hits}, indent=0))
        table('extraction stage, per draw', counts + ['must_open covered', 'must_open total', 'may_open covered', 'may_open total', 'questions proposed', 'cost usd x100'], arms, rows)
        return
    unfinished = [r for runs in arms.values() for r in runs if not finished(r)]
    if unfinished:
        raise SystemExit(f'not finished: {unfinished}')
    stage_rows, product_rows, loss_rows, judged = {}, {}, {}, {}
    for name, runs in arms.items():
        stage_rows[name], product_rows[name], loss_rows[name], judged[name], hits = [], [], [], [], {}
        for draw, run in enumerate(runs, 1):
            stage, product, losses, matter_hits = window_draw(run, articles)
            stage_rows[name].append(stage)
            product_rows[name].append(product)
            loss_rows[name].append(losses)
            judged[name].append(judgement(run))
            for key, value in matter_hits.items():
                hits.setdefault(key, {})[f'd{draw}'] = {'handed_over': value[0], 'written': value[1]}
        (HERE / f'hits-{name}.json').write_text(json.dumps({'runs': runs, 'matters': hits}, indent=0))
    table('extraction stage (checked handovers), per draw', counts, arms, stage_rows)
    table('product (ledger records), per draw', counts + ['stored records', 'must_open covered', 'must_open covered by article-opened', 'must_open total',
                                                           'may_open covered', 'may_open total', 'questions opened from articles', 'cost usd x100'], arms, product_rows)
    table('helpful matters: where each ends, per draw', ['reached', 'handed over, not written', 'not handed over'], arms, loss_rows)
    print('\njudgement at 2026-07-14 (reader B), seed questions q01-q22')
    seeds = sorted({q for n in arms for o in judged[n] for q in o}, key=lambda v: int(v[1:]))
    print(f'{"question":9}' + ''.join(f'{n:>36}' for n in arms))
    for q in seeds:
        print(f'{q:9}' + ''.join(f'{" ".join(o.get(q, "-")[:8] for o in judged[n]):>36}' for n in arms))
    for n in arms:
        print(f'{n}: agreements per draw {[sum(1 for v in o.values() if v == "agree") for o in judged[n]]}, total {sum(sum(1 for v in o.values() if v == "agree") for o in judged[n])}')


if __name__ == '__main__':
    main()
