"""Census of unfiled evidence on stored Step 1 runs against the frozen ruler (no model calls).

For each run: the unfiled items; the helpful gold matters they would add if kept (matters the filed items do not already hold); the
not-kept and unmatched items they would add. Uses score_gold_runs (the frozen scorer's own matching). Writes, per run, every unfiled
item that adds a helpful matter, with the theses open at that moment, for reading.

Usage: census_unfiled.py <out.json> <label>=<trace.sqlite> ... [--test]"""
import collections, importlib.util, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('score_gold_runs', ROOT / 'clean-arch/takeover-2026-11-07/score_gold_runs.py')
sgr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sgr)


def rows(trace, include_unfiled):
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    out, unfiled, context = {}, {}, {}
    for seq, input_id, result, before in conn.execute("select sequence, input_id, result, before_state from trace where status='complete' order by sequence"):
        r = json.loads(result)
        kept = r['evidence'] + (r.get('unfiled_evidence', []) if include_unfiled else [])
        out[input_id] = [{'quote': ' '.join(ev['source_passages']), 'quotes': ev['source_passages'], 'one_line': ev['summary']} for ev in kept]
        unfiled[input_id] = r.get('unfiled_evidence', [])
        context[input_id] = {'sequence': seq, 'open_theses': [t['description'] for t in json.loads(before)]}
    return out, unfiled, context


def main():
    out_path = Path(sys.argv[1])
    gold_path = sgr.GOLD.with_name('golden-v5-test.json') if '--test' in sys.argv else sgr.GOLD
    gold = json.loads(gold_path.read_text())
    report = {}
    for spec_arg in [a for a in sys.argv[2:] if '=' in a]:
        label, trace = spec_arg.split('=', 1)
        filed, unfiled, context = rows(trace, False)
        both, _, _ = rows(trace, True)
        articles = [a for a in gold['articles'] if a['input_id'] in filed]
        c_filed, m_filed = sgr.score(articles, filed)
        c_both, m_both = sgr.score(articles, both)
        missed_filed = {(m['input_id'], m['span'][:200]) for m in m_filed}
        missed_both = {(m['input_id'], m['span'][:200]) for m in m_both}
        recovered = [m for m in m_filed if (m['input_id'], m['span'][:200]) not in missed_both]
        helpful = lambda c: c['core matter kept'] + c['supporting matter kept']
        n_unfiled = sum(len(v) for v in unfiled.values())
        print(f"{label}: unfiled items {n_unfiled} in {sum(1 for v in unfiled.values() if v)} articles; helpful filed {helpful(c_filed)} → with unfiled "
              f"{helpful(c_both)} (+{helpful(c_both) - helpful(c_filed)}, core +{c_both['core matter kept'] - c_filed['core matter kept']}); "
              f"not-kept spans {c_filed['items matching a not-kept span']} → {c_both['items matching a not-kept span']}; "
              f"unmatched {c_filed['items matching nothing in the gold']} → {c_both['items matching nothing in the gold']}")
        report[label] = {'recovered': [dict(m, **context[m['input_id']]) for m in recovered],
                         'unfiled': {k: v for k, v in unfiled.items() if v}, 'context': context}
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
