"""Score clean Step 1 traces and frozen production draws against golden-v5 with the frozen scorer's own matching (D244, D372).

The matching functions come from docs/research/2026-10-29-ledger-standard/score_gold.py unchanged: a clean item counts for a gold
entry when one of its source passages matches the entry's span (`same`), and for its matter when `same_matter` holds on the item's
passages and summary. Helpful = core + supporting (D372); optional entries are neutral; not-kept entries count as noise kept. A score
is a lead: misses are written out for reading.

Usage: score_gold_runs.py <out.json> <label>=<trace.sqlite>[+<segment trace.sqlite>] ... [--production] [--test]

`--test` scores against golden-v5-test.json and, with --production, production's one stored test draw (test-control-d1)."""
import collections, hashlib, json, re, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / 'docs/research/2026-10-29-ledger-standard'
sys.path.insert(0, str(LEDGER))
import score_gold  # noqa: E402

GOLD = LEDGER / 'golden-v5/golden-v5-dev.json'
PAGE = ROOT / 'docs/prd/05-extraction-standard.html'
PRODUCTION = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/runs')


def clean_statements(traces):
    """Completed answers of a run, from its trace and any continuation segments ('a.sqlite+b.sqlite')."""
    rows = {}
    for trace in traces.split('+'):
        conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
        for input_id, result in conn.execute("select input_id, result from trace where status='complete'"):
            rows[input_id] = [{'quote': ' '.join(ev['source_passages']), 'quotes': ev['source_passages'], 'one_line': ev['summary']}
                              for ev in json.loads(result)['evidence']]
    return rows


def production_statements(draw):
    if (PRODUCTION / draw / 'handovers.json').exists():
        return {input_id: [{'quote': ev['quote'], 'quotes': [ev['quote']], 'one_line': ev['one_line']} for ev in h['evidence']]
                for input_id, h in json.loads((PRODUCTION / draw / 'handovers.json').read_text()).items()}
    conn = sqlite3.connect(f'file:{PRODUCTION / draw / "views.sqlite"}?mode=ro', uri=True)
    return {input_id: [{'quote': ev['quote'], 'quotes': [ev['quote']], 'one_line': ev['one_line']} for ev in json.loads(h)['evidence']]
            for input_id, h in conn.execute('select input_id, handover_json from handovers')}


def score(articles, statements):
    counts, misses = collections.Counter(), []
    for article in articles:
        found = statements.get(article['input_id'])
        if found is None:
            counts['articles without an answer'] += 1
            continue
        counts['articles'] += 1
        counts['items returned'] += len(found)
        for entry in article['items']:
            weight = entry['weight']
            sentence = any(any(score_gold.same(entry['span'], q) for q in s['quotes']) for s in found)
            matter = any(score_gold.same_matter(entry, s) for s in found)
            counts[f'{weight} total'] += 1
            counts[f'{weight} sentence kept'] += sentence
            counts[f'{weight} matter kept'] += matter
            if weight in ('core', 'supporting') and not matter:
                misses.append({'input_id': article['input_id'], 'weight': weight, 'span': entry['span'][:300]})
        for s in found:
            gold_hit = any(any(score_gold.same(e['span'], q) for q in s['quotes']) for e in article['items'])
            rejected = [nk for nk in article['not_kept'] if any(score_gold.same(nk['span'], q) for q in s['quotes'])]
            if gold_hit:
                counts['items matching a gold entry'] += 1
            elif rejected and all(nk['weight'] == 'not_kept' for nk in rejected):
                counts['items matching a not-kept span'] += 1
            elif rejected:
                counts['items matching an optional span'] += 1
            else:
                counts['items matching nothing in the gold'] += 1
    return counts, misses


def main():
    out, specs = Path(sys.argv[1]), [a for a in sys.argv[2:] if '=' in a]
    gold_path = GOLD.with_name('golden-v5-test.json') if '--test' in sys.argv else GOLD
    recorded = dict(line.split()[::-1] for line in (GOLD.parent / 'golden-v5.sha256').read_text().splitlines() if line.strip())
    if hashlib.sha256(gold_path.read_bytes()).hexdigest() != recorded[gold_path.name]:
        raise SystemExit(f'refused: {gold_path.name} does not match golden-v5.sha256')
    gold = json.loads(gold_path.read_text())
    page_version = int(re.search(r'<meta name="standard-version" content="(\d+)">', PAGE.read_text()).group(1))
    if gold['standard_version'] != page_version:
        raise SystemExit(f'refused: gold version {gold["standard_version"]}, page version {page_version}')
    header = {'gold': str(gold_path.relative_to(ROOT)), 'gold_sha256': hashlib.sha256(gold_path.read_bytes()).hexdigest(),
              'page_sha256': hashlib.sha256(PAGE.read_bytes()).hexdigest(), 'standard_version': page_version}
    print(json.dumps(header))
    runs = {label: clean_statements(path) for label, path in (s.split('=', 1) for s in specs)}
    if '--production' in sys.argv:
        for draw in (('test-control-d1',) if '--test' in sys.argv else ('control-v108-d1', 'control-v108-d2', 'control-v108-d3')):
            runs[draw] = production_statements(draw)
    common = set.intersection(*(set(rows) for rows in runs.values()))
    articles = [a for a in gold['articles'] if a['input_id'] in common]
    print(f'articles scored (present in every run): {len(articles)}')
    report = {'header': header, 'articles': len(articles), 'runs': {}}
    for label, rows in runs.items():
        counts, misses = score(articles, rows)
        helpful_total = counts['core total'] + counts['supporting total']
        helpful_matter = counts['core matter kept'] + counts['supporting matter kept']
        report['runs'][label] = {'counts': dict(counts), 'misses': misses}
        print(f"{label:18s} helpful matter kept {helpful_matter}/{helpful_total}  core {counts['core matter kept']}/{counts['core total']}  "
              f"items {counts['items returned']}  not-kept spans kept {counts['items matching a not-kept span']}  "
              f"optional {counts['items matching an optional span']}  unmatched {counts['items matching nothing in the gold']}")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
