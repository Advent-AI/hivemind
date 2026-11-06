"""Audit the historical final-ledger word matcher against stored dispatch sequences; no model calls."""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXTRACTION = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0, str(EXTRACTION / 'docs/research/2026-10-31-reference-context'))
import score_ref  # noqa: E402: the actual historical match function and frozen gold


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: historical_coverage_census.py absolute-new-output-file')
    path = Path(sys.argv[1])
    if not path.is_absolute() or path.exists():
        raise ValueError('output must be an absolute new file')
    ledger = ROOT / 'poc/data/parallel-thesis-evidence-input-2026-11-05/views.sqlite'
    conn = sqlite3.connect(ledger.resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    views = [dict(v) for v in conn.execute('select view_id, question, looks_at, created_seq, created_from_input from views')]
    counts, rows = Counter(), []
    for article in score_ref.articles:
        golds = article.get('questions', {}).get('must_open', [])
        if not golds:
            continue
        seqs = conn.execute("select distinct sequence_no from processing_steps where input_id=? and step='dispatched'", (article['input_id'],)).fetchall()
        if len(seqs) != 1:
            counts['article_without_one_dispatch'] += 1
            continue
        seq = seqs[0][0]
        for gold in golds:
            hits = [v for v in views if score_ref.same_question(gold['gist'], v['question'] + ' ' + (v['looks_at'] or ''))]
            before = [v for v in hits if v['created_seq'] < seq]
            same = [v for v in hits if v['created_seq'] == seq]
            after = [v for v in hits if v['created_seq'] > seq]
            counts['gold_questions'] += 1
            counts['final_word_match'] += bool(hits)
            counts['before_word_match'] += bool(before)
            counts['final_only_word_match'] += bool(hits and not before)
            rows.append({'input_id': article['input_id'], 'dispatch_seq': seq, 'gold_gist': gold['gist'],
                         'before': before, 'same_dispatch': same, 'after': after})
    conn.close()
    control = next(r for r in rows if r['input_id'] == 'gnews:d0f3f83296df884fae64921e' and 'DRAM' in r['gold_gist'])
    later_ids = {v['view_id'] for v in control['after']}
    if not {'v22', 'v72'} <= later_ids:
        raise ValueError('known word-match control changed')
    result = {'method': 'Historical score_ref.same_question exact code, applied to the saved finished ledger. Matching is lexical, not a semantic judgment; before is not the same as production day-start.',
              'counts': dict(counts), 'rows': rows}
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
