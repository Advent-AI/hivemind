#!/usr/bin/env python3
"""For one ruler question, side by side across the three saved D392 clean draws (and production's control draws): the rung path, the
final judgement, and for each of the gold's decisive items whether the draw's evidence under the question carries it, was shown to
the judge on the last day, and was cited. Read-only; no model call.

An item of the gold packet is matched to evidence by its article (`input_id`) and, within that article, by the evidence whose quote
shares the most words with the item's passage (a lead for a reader, not an identity: every match is printed with its quote).

Usage: trace_question.py <question id, e.g. q17> <output json>"""
import collections, glob, json, re, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
DRAWS = ROOT / 'poc/data/clean-e2e-2026-11-09'
WINDOW_END = '2026-07-14'
WORD = re.compile(r"[a-z0-9$%.,]+")


def words(text):
    return {w.strip('.,') for w in WORD.findall((text or '').lower()) if len(w.strip('.,')) > 2}


def runs():
    for draw in (1, 2, 3):
        yield f'clean-d{draw}', Path(sorted(glob.glob(str(DRAWS / f'stage2-clean-d{draw}/judged*')))[-1])
    for draw in (1, 3, 4):
        views = sorted(glob.glob(str(DRAWS / f'stage2-control-d{draw}/**/views.sqlite'), recursive=True))
        if views:
            yield f'control-d{draw}', Path(views[0]).parent


def main(question_id, output_path):
    gold = {e['question_id']: e for e in json.loads((GOLD / 'gold-v1.json').read_text())['entries']}[question_id]
    view_id = gold['seed_view_id']
    items = {i['id']: i for i in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    decisive = list(dict.fromkeys((gold.get('decisive_items') or []) + (gold['implied_outcome'].get('items') or [])
                                  + ((gold.get('against') or {}).get('items') or []) + ((gold.get('reference') or {}).get('items') or [])))
    report = {'question': gold['question'], 'view': view_id, 'gold': {'implied': gold['implied_outcome'], 'reference': gold['reference'],
              'against': gold.get('against')}, 'items': {i: {name: items[i].get(name) for name in ('day', 'title', 'input_id', 'passage', 'who')} for i in decisive},
              'runs': {}}
    for label, folder in runs():
        conn = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        judgements = [dict(r) for r in conn.execute('select publication_day, rung, cited_evidence_json, reasons, implied_outcome, call_id, request_sha256 '
                                                     'from judgements where view_id=? and publication_day<=? order by judgement_id', (view_id, WINDOW_END))]
        rungs = [dict(r) for r in conn.execute('select position, label, lo, hi from rungs where view_id=? order by position', (view_id,))]
        linked = {r['evidence_id']: dict(r) for r in conn.execute(
            'select e.evidence_id, e.quote, e.one_line, e.tier, e.original_who, l.seq, s.input_id, s.publication_day from evidence_links l '
            'join evidence e on e.evidence_id=l.evidence_id join evidence_sources s on s.evidence_id=e.evidence_id where l.view_id=?', (view_id,))}
        all_evidence = collections.defaultdict(list)
        for r in conn.execute('select e.evidence_id, e.quote, e.one_line, s.input_id from evidence e join evidence_sources s on s.evidence_id=e.evidence_id'):
            all_evidence[r['input_id']].append(dict(r))
        last = judgements[-1] if judgements else None
        shown_last = []
        requests_file = folder / 'judge-requests.json'
        if requests_file.exists():
            shown_last = next((r['shown'] for r in reversed(json.loads(requests_file.read_text())) if r['view'] == view_id and r['day'] <= WINDOW_END), [])
        else:   # production's runs: read the shown list from the archived request of the last judgement
            archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
            row = archive.execute('select request_json from model_calls where call_id=?', (last['call_id'],)).fetchone() if last else None
            if row:
                text = json.loads(row[0])['messages'][-1]['content']
                block = text.split('\n[Evidence in ', 1)
                shown_last = re.findall(r'^- (e\d+) \[', block[1].split('\n\n[', 1)[0], re.M) if len(block) == 2 else []
        cited_last = json.loads(last['cited_evidence_json'] or '[]') if last else []
        per_item = {}
        for item_id in decisive:
            item = items[item_id]
            candidates = all_evidence.get(item['input_id'], [])
            best = max(candidates, key=lambda e: len(words(e['quote']) & words(item['passage'])), default=None)
            overlap = len(words(best['quote']) & words(item['passage'])) / max(len(words(item['passage'])), 1) if best else 0
            matched = best if overlap >= 0.5 else None
            per_item[item_id] = {'article written': bool(candidates), 'evidence': matched['evidence_id'] if matched else None,
                                 'word overlap': round(overlap, 2), 'under the question': bool(matched) and matched['evidence_id'] in linked,
                                 'shown on the last day': bool(matched) and matched['evidence_id'] in shown_last,
                                 'cited on the last day': bool(matched) and matched['evidence_id'] in cited_last,
                                 'quote': (matched or best or {}).get('quote', '')[:240]}
        chosen = rungs[last['rung'] - 1] if last else None
        lo, hi = (chosen['lo'], chosen['hi']) if chosen else (None, None)
        implied = gold['implied_outcome']
        agree = None if not last else ((chosen['label'].lower() == 'yes') == bool(implied['yes_no']) if implied.get('yes_no') is not None
                                        else (lo is None or implied['high'] >= lo) and (hi is None or implied['low'] < hi))
        report['runs'][label] = {'folder': str(folder), 'agrees': agree, 'rung path': [(j['publication_day'], j['rung']) for j in judgements],
                                 'final implied_outcome': last['implied_outcome'] if last else None, 'final reasons': last['reasons'] if last else None,
                                 'linked': len(linked), 'shown on the last day': len(shown_last), 'items': per_item}
    Path(output_path).write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(f"{question_id} {gold['question']}\ngold: {gold['implied_outcome']['text'][:300]}")
    header = f"{'item':<6}{'day':<12}" + ''.join(f'{label:>12}' for label in report['runs'])
    print(header)
    for item_id in decisive:
        cells = []
        for label, run in report['runs'].items():
            cell = run['items'][item_id]
            cells.append('cited' if cell['cited on the last day'] else 'shown' if cell['shown on the last day'] else 'linked' if cell['under the question']
                         else 'elsewhere' if cell['evidence'] else 'unmatched' if cell['article written'] else 'no record')
        print(f"{item_id:<6}{items[item_id]['day']:<12}" + ''.join(f'{c:>12}' for c in cells) + f"  {items[item_id]['passage'][:90]}")
    print(f"{'agrees':<18}" + ''.join(f"{str(run['agrees']):>12}" for run in report['runs'].values()))
    for label, run in report['runs'].items():
        print(f"{label}: {' '.join(day[5:] + ':' + str(rung) for day, rung in run['rung path'])} | linked {run['linked']}, shown last day {run['shown on the last day']}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
