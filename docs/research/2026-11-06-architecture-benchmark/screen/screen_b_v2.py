"""The screen of results-reading.md §4 (agreed with Codex, r23; Alex, 2026-11-06: "好，按1试一次"): the split's evidence call as it is (poc-split-v3,
split-b-v1) against its revision (poc-split-v4, split-b-v2), with the frozen production extraction (poc-v108) as the same-day reference, on the fixed
article set (next-test-set-20261107.json).

Every request is rebuilt by the production code from the stored state it was first built from (window split draw 1 and control draw 1 for the dev
articles; the fixture ledger for the test articles), and its identity is checked against the stored request: an article whose rebuilt request is
not in the archive is excluded and named. Sends go through the production path (`model.call`; the frozen extraction through `extraction.extract`),
each send with its own new archive, so every send is a fresh answer: current six times (C1–C6), revised three times (R1–R3), production three
times (P1–P3).

    PYTHONPATH=src python3 screen_b_v2.py send        writes screen/sends.json
    PYTHONPATH=src python3 screen_b_v2.py measure     reads screen/sends.json, prints the counts, S_h, S_n and conditions 1–2"""
import concurrent.futures
import itertools
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
ROOT = BENCH.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'scripts'), str(BENCH)]
import hivemind.model  # noqa: E402,F401  (this tree's package before the scoring helpers)
from hivemind import config, extraction, model, split, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402
import preflight_split  # noqa: E402
sys.path.insert(3, '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard')
import score_gold as sg  # noqa: E402

SET = json.loads((BENCH / 'results/next-test-set-20261107.json').read_text())
GOLDS = {'dev': '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json',
         'test': '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json'}
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
UNIVERSE = str(ROOT / 'poc/universe.json')
CURRENT, REVISED, PRODUCTION = (config.load(str(ROOT / f'poc/config/{n}.json')) for n in ('poc-split-v3', 'poc-split-v4', 'poc-v108'))
SENDS = [('C', CURRENT, k) for k in range(1, 7)] + [('R', REVISED, k) for k in range(1, 4)] + [('P', PRODUCTION, k) for k in range(1, 4)]


def identity(setting, spec, provider):
    return model.request_identity(model.build_request(setting, spec[0], spec[1], spec[2], spec[3], provider))[1]


def archived_shas(path, purpose):
    archive = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    return {r[0] for r in archive.execute('select request_sha256 from model_calls where purpose=?', (purpose,))}


def prepare():
    """Per article: its item, the B specs (current and revised) and the production request inputs, each checked against the stored request."""
    items = testdb.open_db(ITEMS)
    prepared, excluded = [], []
    split_dev = store.open_read_only(str(BENCH / 'runs/split-v3-d1/views.sqlite'))
    control_dev = store.open_read_only(str(BENCH / 'runs/control-v108-d1/views.sqlite'))
    b_dev, p_dev = archived_shas(BENCH / 'runs/split-v3-d1/archive.sqlite', 'split_b'), archived_shas(BENCH / 'runs/control-v108-d1/archive.sqlite', 'extract')
    b_test, p_test = archived_shas(BENCH / 'runs/test-split-d1/archive.sqlite', 'split_b'), archived_shas(BENCH / 'runs/test-control-d1/archive.sqlite', 'extract')
    import bench_test_articles
    for part, ids in (('dev', SET['dev_articles']), ('test', SET['test_articles'])):
        for input_id in ids:
            row = items.execute('select * from items where input_id=?', (input_id,)).fetchone()
            item = testdb.item_of(row)
            if part == 'dev':
                step = split_dev.execute("select sequence_no from processing_steps where input_id=? and step='extracted' and result='ok'", (input_id,)).fetchone()
                pstep = control_dev.execute("select sequence_no from processing_steps where input_id=? and step='extracted' and result='ok'", (input_id,)).fetchone()
                if not step or not pstep:
                    excluded.append((input_id, 'not extracted in the stored draw (a merged copy or outside the feed)'))
                    continue
                seq = step[0]
                memory = preflight_split.subjects_before(split_dev, seq)
                uni = universe.load(UNIVERSE)
                split.load_subjects(memory, uni)
                shown = split.latest_library(split_dev, seq)
                p_uni = universe.load(UNIVERSE)
                objects = [o['value'] for o in item.get('object_identifiers') or [] if p_uni.has(o['value'])]
                p_shown = extraction.shown_views(control_dev, PRODUCTION, item, objects)
                b_shas, p_shas = b_dev, p_dev
            else:
                conn = bench_test_articles.fixture_copy()
                uni = universe.load(UNIVERSE)
                shown = split.latest_library(conn, 1)
                p_uni = universe.load(UNIVERSE)
                objects = [o['value'] for o in item.get('object_identifiers') or [] if p_uni.has(o['value'])]
                p_shown = extraction.shown_views(conn, PRODUCTION, item, objects)
                b_shas, p_shas = b_test, p_test
            parts = split.sections(item['text'])
            current = [split.requests(CURRENT, item, text, shown, uni)[2] for text in parts]
            revised = [split.requests(REVISED, item, text, shown, uni)[2] for text in parts]
            if any(identity(CURRENT.split['b'], spec, CURRENT.provider) not in b_shas for spec in current):
                excluded.append((input_id, 'the rebuilt current B request is not the stored one'))
                continue
            setting, system, user, schema = extraction.request_for(PRODUCTION, item, item['text'], p_shown, p_uni)
            if identity(setting, (system, user, schema, 'extraction'), PRODUCTION.provider) not in p_shas:
                excluded.append((input_id, 'the rebuilt production request is not the stored one'))
                continue
            prepared.append({'part': part, 'item': item, 'uni': uni, 'p_uni': p_uni, 'current': current, 'revised': revised, 'p_shown': p_shown,
                             'parts': parts})
    return prepared, excluded


def send_one(job):
    arm, cfg, k, entry = job
    archive = model.Archive(str(HERE / f'archives/{arm}{k}.sqlite'))
    item, text = entry['item'], entry['item']['text']
    if arm == 'P':
        handover = extraction.extract(archive, cfg, item, text, entry['p_shown'], entry['p_uni'])
        statements = [{'quote': e['quote'], 'one_line': e.get('one_line', ''), 'links': e['links']} for e in handover.evidence]
        return arm, k, item['input_id'], statements, []
    specs = entry['current'] if arm == 'C' else entry['revised']
    names = split.subject_names(item, entry['uni'])
    filed, unlinked = [], []
    for spec in specs:
        answer = model.call(archive, cfg, cfg.split['b'], spec[0], spec[1], spec[2], spec[3], 'split_b')
        for e in answer.data['evidence']:
            exact = split.source_quote(e['quote'], text, names)
            if exact is None:
                continue
            record = {'quote': exact, 'one_line': e.get('one_line', ''), 'links': e['links']}
            (filed if e['links'] else unlinked).append(record)
    return arm, k, item['input_id'], filed, unlinked


def send():
    prepared, excluded = prepare()
    print(f'articles prepared {len(prepared)} (dev {sum(e["part"] == "dev" for e in prepared)}, test {sum(e["part"] == "test" for e in prepared)}); '
          f'excluded {len(excluded)}')
    for input_id, why in excluded:
        print('  excluded', input_id, why)
    (HERE / 'archives').mkdir(exist_ok=True)
    jobs = [(arm, cfg, k, entry) for arm, cfg, k in SENDS for entry in prepared]
    out, failures = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(send_one, job): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            arm, cfg, k, entry = futures[future]
            try:
                arm, k, input_id, filed, unlinked = future.result()
                out.setdefault(f'{arm}{k}', {})[input_id] = {'part': entry['part'], 'filed': filed, 'unlinked': unlinked}
            except Exception as error:
                failures.append((f'{arm}{k}', entry['item']['input_id'], repr(error)[:300]))
    json.dump({'prepared': [e['item']['input_id'] for e in prepared], 'excluded': excluded, 'failures': failures, 'sends': out},
              open(HERE / 'sends.json', 'w'), ensure_ascii=False)
    print(f'sends written; failures {len(failures)}')
    for f in failures[:10]:
        print('  failed', f)


def score(statements_by_article, golds):
    total = {'helpful': 0, 'not_kept': 0, 'additions': 0, 'statements': 0, 'links': 0}
    for input_id, records in statements_by_article.items():
        a = golds[input_id]
        kept_gold = [it for it in a['items'] if it['weight'] in ('core', 'supporting', 'optional')]
        optional = [n['span'] for n in a['not_kept'] if n['weight'] == 'optional']
        total['helpful'] += sum(1 for it in a['items'] if it['weight'] in ('core', 'supporting') and any(sg.same_matter(it, r) for r in records))
        carried = lambda r: any(sg.same_matter(it, r) for it in kept_gold) or any(sg.same(s, r['quote']) for s in optional)
        total['not_kept'] += sum(1 for n in a['not_kept'] if n['weight'] == 'not_kept' and any(sg.same(n['span'], r['quote']) and not carried(r) for r in records))
        total['additions'] += sum(1 for r in records if not any(sg.same_matter(it, r) for it in a['items']) and not any(sg.same(n['span'], r['quote']) for n in a['not_kept']))
        total['statements'] += len(records)
        total['links'] += sum(len(r['links']) for r in records)
    return total


def measure():
    data = json.loads((HERE / 'sends.json').read_text())
    if data['failures']:
        raise SystemExit(f'not decidable: {len(data["failures"])} sends returned no answer; re-send them first')
    golds = {a['input_id']: a for g in GOLDS.values() for a in json.load(open(g))['articles']}
    articles = data['prepared']
    helpful_total = sum(1 for i in articles for it in golds[i]['items'] if it['weight'] in ('core', 'supporting'))
    rows = {}
    for name, by_article in sorted(data['sends'].items()):
        missing = [i for i in articles if i not in by_article]
        if missing:
            raise SystemExit(f'not decidable: send {name} lacks {len(missing)} articles')
        rows[name] = score({i: by_article[i]['filed'] for i in articles}, golds)
        rows[name]['unlinked'] = sum(len(by_article[i]['unlinked']) for i in articles)
    print(f'articles {len(articles)}; helpful matters in the gold {helpful_total}; excluded {len(data["excluded"])}')
    for name in sorted(rows, key=lambda n: (n[0] != 'C', n[0] != 'R', n)):
        r = rows[name]
        print(f'  {name}: helpful {r["helpful"]}, not-kept {r["not_kept"]}, additions {r["additions"]}, statements {r["statements"]}, '
              f'links/statement {r["links"] / max(r["statements"], 1):.2f}, unlinked {r["unlinked"]}')
    mean = lambda names, key: sum(rows[n][key] for n in names) / len(names)
    current = [f'C{k}' for k in range(1, 7)]
    splits = [(list(a), [c for c in current if c not in a]) for a in itertools.combinations(current, 3)]
    s_h = max(abs(mean(a, 'helpful') - mean(b, 'helpful')) for a, b in splits)
    s_n = max(abs(mean(a, 'not_kept') - mean(b, 'not_kept')) for a, b in splits)
    c13, c46, r13, p13 = ['C1', 'C2', 'C3'], ['C4', 'C5', 'C6'], ['R1', 'R2', 'R3'], ['P1', 'P2', 'P3']
    gain = mean(r13, 'helpful') - mean(c13, 'helpful')
    line = max(0.03 * helpful_total, s_h)
    print(f'S_h {s_h:.2f} ({s_h / helpful_total:.1%} of the helpful total); S_n {s_n:.2f}')
    if s_h > 0.06 * helpful_total:
        print('condition 1: NOT DECIDABLE (S_h above 6% of the helpful total)')
    else:
        print(f'condition 1 (gain): R mean − C1–C3 mean = {gain:.2f}; line {line:.2f} → {"PASS" if gain > line else "FAIL"}; '
              f'self-check C4–C6 − C1–C3 = {mean(c46, "helpful") - mean(c13, "helpful"):.2f} (must not exceed the line: '
              f'{"holds" if mean(c46, "helpful") - mean(c13, "helpful") <= line else "BROKEN"})')
    bound = mean(p13, 'not_kept') + s_n
    print(f'condition 2 (not-kept): R mean {mean(r13, "not_kept"):.2f}; bound P mean {mean(p13, "not_kept"):.2f} + S_n {s_n:.2f} = {bound:.2f} → '
          f'{"PASS" if mean(r13, "not_kept") <= bound else "FAIL"}; self-check C4–C6 mean {mean(c46, "not_kept"):.2f} '
          f'{"holds" if mean(c46, "not_kept") <= bound else "NOT DECIDABLE"}')
    for arm in (c13, c46, r13, p13):
        print(f'  mean additions per send {"".join(arm[0][0])}{arm[0][1]}–{arm[-1][1]}: {mean(arm, "additions"):.2f}')


if __name__ == '__main__':
    {'send': send, 'measure': measure}[sys.argv[1]]()
